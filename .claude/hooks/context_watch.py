#!/usr/bin/env python3
"""Context watcher for long Claude Code sessions.

Hook modes read the hook's JSON on stdin and always exit 0, so they never block:
  start          SessionStart, any source but compact. Locally it brings the
                 installed watcher in step with the skill's copy synced from
                 claude.ai (install_watcher.py --sync) and says what it found or
                 changed; in a cloud session it compares the repository's copy
                 with that one and tells Claude to update main when they differ.
                 With no synced copy it says so, with how to act on the notice's
                 keywords without the skill. Loading the skill is the owner's
                 preferences' job, which reach every session.
  watch          PostToolBatch and UserPromptSubmit. Once the context comes
                 within 60,000 tokens of compaction, adds one short note to
                 Claude's context asking for the handoff file; silent otherwise,
                 and silent right after a compaction, which starts the count again.
  after-compact  SessionStart with matcher "compact". Finds the session's notes
                 under session-notes/ (in the hook's cwd, CLAUDE_PROJECT_DIR, any
                 scratchpad_dir the input gives, and a cloud session's scratchpad,
                 found by its session id) and prints the newest handoff.md whole,
                 flagged as already used when it ends with a Resumed line; with no
                 handoff, the start of the newest progress file, else of the newest
                 note. It also asks Claude to load the owner's skill again with the
                 Skill tool, as the owner's preferences ask after every compaction,
                 since an invoked skill may not come back.
                 Output stays under the 10,000 characters a hook may add.
Manual mode:
  check          Run by Claude or the owner, from the working folder. Prints the
                 transcript's path, the context size, where automatic compaction
                 is expected, where the note comes, whether the hooks have run in
                 this session and which settings files (the user's, this folder's)
                 hold them, whether the installed copies match this skill's
                 version, and the one-line leave recommendation. Just after a
                 compaction the size is the summary's alone; the overhead comes on
                 top with the next request.
  recommend      Every option at this size, formatted and explained, with its hours
                 and list-price costs, for Claude to relay in chat (alias status);
                 the notice points to it.
  away [long|<time>]  Print the plan for an absence: pings until the owner is back;
                 with "long" (past the limit the footer states), from 60% a handoff
                 and /compact first, below 60% no pings at all. A stated time (3h,
                 90m, overnight = 12h, 2d) is compared with that limit instead.
                 Claude follows the printout, so the per-turn thinking stays trivial.
  footer         Stop hook: emit the recommendation as a systemMessage, shown to
                 the owner after the reply and NOT added to Claude's context, so
                 it costs no tokens on any turn: one line, the tokens used and, for
                 each length of absence, the keyword to send and what it costs, so
                 the hours where pings stop paying show; `status` gives the rest.

Context = input + cache_creation + cache_read tokens of the newest main-chain
assistant message in the transcript, skipping synthetic and zero-usage ones.
The transcript format is undocumented and may lag one message. The watcher
costs no usage: it reads the transcript tail on this machine in a few tens of
milliseconds. It keeps its state in context-watch/ in Claude Code's
configuration folder, ~/.claude or CLAUDE_CONFIG_DIR, where it also finds the
user settings and the transcripts.

Settings, all optional, as environment variables:
  CONTEXT_WATCH_FINAL   the note, in tokens (default 60,000 below compaction)
  CONTEXT_WATCH_REMIND  an earlier note, in tokens (default: none; ignored unless
                        at least 2% of the window, 20,000 on 1M, below the note)
The offset is for a 1M window and scales with a smaller one; where the
auto-compact window is under half the model's, it is taken of that window
instead.
Claude Code's own CLAUDE_CODE_AUTO_COMPACT_WINDOW and
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE are read to place compaction: at the override's
percentage (80 in cloud sessions) of the window less 20,000 tokens, which six
cloud compactions seen on 2026-10-17 and 18 fit, but never later than the
window less 33,000, the documented default (about 967,000 on 1M) that applies
without the override.
The window is that variable, else autoCompactWindow in the user settings (the
model's own entry under modelSettings, else the top level), else the model's
window, 200,000 with CLAUDE_CODE_DISABLE_1M_CONTEXT set; it is kept between
100,000 and the model's window.
"""
import datetime
import glob
import json
import os
import re
import subprocess
import sys
import time

NOTES_DIR = "session-notes"
ONE_M_MODELS = ("opus-5", "sonnet-5", "haiku-5", "fable", "mythos", "opus-4-7", "opus-4-8")
SUMMARY_RESERVE = 20_000     # held back for the summary; fits every compaction seen
AUTOCOMPACT_BUFFER = 13_000  # with the reserve, the documented ~967,000 on a 1M window
MIN_WINDOW = 100_000         # the smallest auto-compact window Claude Code takes
VERSION = "2026-10-20.5"     # this release; install_watcher.py compares the files themselves
SKILL_NAME = "ai-best-practices"
PING_GAP = 50                # minutes between keep-warm pings, inside the cache's one-hour lifetime
READ_PRICE = 0.20            # $ per million tokens read from the cache, Opus 5.5's list price (#805)
WRITE_PRICE = 8.00           # $ per million written at the one-hour price: what a cold return pays (#805)
COMPACT_EXTRA = 0.95         # $ a compaction adds to its read: the summary's output, $0.08-0.35 (#805), and the
                             # rebuild after it, $0.38-0.69 in 10 and $1.02-1.11 in 4 of one cloud session's 14
                             # compactions of 2026-10-17 to 20 (#807.2)
COMPACTED = 140_000          # tokens after a compaction, overhead included: 113,000-152,000 in those 14


def config_dir():
    """Claude Code's configuration folder: CLAUDE_CONFIG_DIR, else ~/.claude."""
    return os.path.expanduser(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude")


def num(v):
    """A token count from the transcript, or 0 when it is missing or not a number."""
    return v if isinstance(v, int) and not isinstance(v, bool) else 0


def read_tail_usage(path, max_bytes=8 << 20, chunk=256 << 10):
    """Return (context_tokens, model, compacted) from the transcript's tail.

    compacted is True when a compaction boundary is newer than every usable
    assistant message; context_tokens is then the boundary's postTokens, if any,
    which count the summary only, and the scan goes on back past the boundary for
    the model, so that the window is still known.
    """
    if not isinstance(path, str) or not path:
        return None, None, False
    try:
        size = os.path.getsize(path)
        f = open(path, "rb")
    except OSError:
        return None, None, False
    with f:
        pos, carry, read, boundary = size, b"", 0, None
        while pos > 0 and read < max_bytes:
            step = min(chunk, pos)
            pos -= step
            f.seek(pos)
            block = f.read(step) + carry
            read += step
            lines = block.split(b"\n")
            carry = lines[0] if pos > 0 else b""
            for raw in reversed(lines[1:] if pos > 0 else lines):
                if not raw.strip():
                    continue
                try:
                    d = json.loads(raw)
                except ValueError:
                    continue
                if not isinstance(d, dict):
                    continue
                if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
                    if boundary is None:   # the newest boundary; older ones do not matter
                        meta = d.get("compactMetadata")
                        boundary = num(meta.get("postTokens")) if isinstance(meta, dict) else 0
                    continue
                msg = d.get("message")
                if d.get("type") != "assistant" or d.get("isSidechain") or not isinstance(msg, dict):
                    continue
                u = msg.get("usage")
                if not isinstance(u, dict) or msg.get("model") == "<synthetic>":
                    continue
                ctx = num(u.get("input_tokens")) + num(u.get("cache_creation_input_tokens")) \
                    + num(u.get("cache_read_input_tokens"))
                if ctx:
                    model = str(msg.get("model") or "")
                    if boundary is not None:   # compacted since this message: its model, the summary's size
                        return boundary or None, model, True
                    return ctx, model, False
    return boundary or None, None, boundary is not None


def canonical_model(name):
    """A model name without a [1m] suffix or a date suffix, for exact matching."""
    name = re.sub(r"\[1m\]$", "", str(name or "").strip().lower())
    return re.sub(r"[-@]\d{8}$", "", name)


def user_auto_compact_window(model):
    """autoCompactWindow from the user settings: the model's own entry under
    modelSettings, matched by exact canonical name, else the top level. None for
    "auto", for a value that is not a token count, or when nothing can be read."""
    try:
        with open(os.path.join(config_dir(), "settings.json"), encoding="utf-8") as f:
            s = json.load(f)
        if not isinstance(s, dict):
            return None
        value = s.get("autoCompactWindow")
        entries = s.get("modelSettings")
        if model and isinstance(entries, dict):
            for name, cfg in entries.items():
                if isinstance(cfg, dict) and "autoCompactWindow" in cfg \
                        and canonical_model(name) == canonical_model(model):
                    value = cfg["autoCompactWindow"]   # "auto" here means the model's own window
                    break
        if isinstance(value, str) and value.strip().isdigit():
            value = int(value)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not value > 0:
            return None
        return int(value)
    except Exception:
        return None


def env_tokens(name, default):
    """A positive token count from an environment variable, else the default."""
    try:
        value = int(float(os.environ.get(name) or default))
    except (ValueError, OverflowError):
        return default
    return value if value > 0 else default


def thresholds(ctx, model):
    """Return (window, trigger, remind, final, rearm, source): the model's window,
    where compaction is expected, the optional earlier note (None unless
    CONTEXT_WATCH_REMIND sets one at least 2% of the window below the note), the note, the size below
    which the notes are armed again, and what set the window."""
    no1m = os.environ.get("CLAUDE_CODE_DISABLE_1M_CONTEXT", "").strip().lower() in ("1", "true")
    big = ctx and ctx > 200_000 or not no1m and any(m in (model or "") for m in ONE_M_MODELS)
    window = 1_000_000 if big else 200_000
    acw, source = user_auto_compact_window(model), "autoCompactWindow setting"
    m = re.match(r"\s*(\d+)", os.environ.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW", ""))
    if m and int(m.group(1)) > 0:
        acw, source = int(m.group(1)), "CLAUDE_CODE_AUTO_COMPACT_WINDOW"
    elif not acw:
        acw, source = window, "the model's window"
    acw = max(MIN_WINDOW, min(acw, window))
    effective = acw - SUMMARY_RESERVE
    trigger = effective - AUTOCOMPACT_BUFFER
    try:
        pct = float(os.environ.get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", ""))
    except ValueError:
        pct = None
    pct = pct if pct and 0 < pct <= 100 else None
    rule = "window - 33,000"
    if pct and int(effective * pct / 100) < trigger:
        trigger, rule = int(effective * pct / 100), "%g%% of (window - 20,000)" % pct
    scale = acw if acw < window // 2 else window   # a much smaller window sets the offset
    final = env_tokens("CONTEXT_WATCH_FINAL", trigger - 60_000 * scale // 1_000_000)
    remind = env_tokens("CONTEXT_WATCH_REMIND", 0) or None
    if remind and remind > final - scale // 50:
        remind = None   # an earlier note too close to the note adds nothing
    return window, trigger, remind, final, (remind or final) - scale // 20, \
        "%s %s; %s" % (source, format(acw, ","), rule)


def state_path(session_id):
    name = re.sub(r"[^A-Za-z0-9_-]", "_", str(session_id or "unknown"))
    return os.path.join(config_dir(), "context-watch", name + ".json")


def load_state(p):
    try:
        st = json.load(open(p))
    except (OSError, ValueError):
        return {"stage": 0}
    return st if isinstance(st, dict) else {"stage": 0}


def save_state(p, st):
    st["t"] = time.time()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f)
    os.replace(tmp, p)


def emit(event, text, shown=None):
    out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}
    if shown:
        out["systemMessage"] = shown   # shown to the owner, never added to Claude's context
    print(json.dumps(out))


def skill_folder():
    """The skill's folder: the one this script sits in, when it is the skill's own copy, else the newest copy
    synced from claude.ai into the configuration folder's skills/synced/, else None."""
    own = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.isfile(os.path.join(own, "SKILL.md")) and os.path.isfile(os.path.join(own, "scripts", "install_watcher.py")):
        return own
    hits = [os.path.dirname(p) for p in glob.glob(os.path.join(glob.escape(config_dir()), "skills", "synced", "*",
                                                               SKILL_NAME, "SKILL.md"))]
    hits = [h for h in hits if os.path.isfile(os.path.join(h, "scripts", "install_watcher.py"))]
    return max(hits, key=os.path.getmtime) if hits else None


def installer(skill, args):
    """install_watcher.py from the skill's folder, with --json: its report, or one carrying an error."""
    try:
        r = subprocess.run([sys.executable, os.path.join(skill, "scripts", "install_watcher.py")] + args + ["--json"],
                           capture_output=True, text=True, timeout=25)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:   # an installer that cannot run is reported, never raised
        return {"error": "the installer did not run (%s)" % e, "differences": [], "current": False}


def sync_line(r, version_shown):
    """(line for Claude, line shown to the owner) after a local --sync."""
    if r.get("updated"):
        names = {"script": "the watcher script", "hooks": "its hooks", "BASH_MAX_TIMEOUT_MS": "BASH_MAX_TIMEOUT_MS",
                 "skill copy": "your personal copy of the skill, moved to ~/.ai-best-practices-backups"}
        what = ", ".join(names.get(x, x) for x in r.get("differences") or []) or "its files"
        return ("The watcher was just updated to the skill's version %s (%s)." % (r.get("version"), what),
                "ai-best-practices: the watcher updated itself to the version on claude.ai, %s (changed: %s)." % (r.get("version"), what))
    if r.get("error"):
        return ("The watcher could not update itself (%s); its old copies keep running. Tell the owner in one line "
                "and offer to look into it with the skill's repair guide; do not run the installer again unasked." % r["error"],
                "ai-best-practices: the watcher could not update itself; Claude can say why.")
    return ("The watcher's installed copies match the skill (version %s)." % version_shown, None)


def installed_copy():
    """True when this script is the copy the user settings' hooks run, <config>/hooks/context_watch.py, the one a
    local session's start hook keeps in step; never the skill's own copy, nor a repository's, whose start hook in a
    local session must not install anything into the user settings."""
    return os.path.realpath(os.path.abspath(__file__)) == os.path.realpath(os.path.join(config_dir(), "hooks",
                                                                                     "context_watch.py"))


def watch(d):
    if d.get("agent_id"):
        return
    ctx, model, compacted = read_tail_usage(d.get("transcript_path") or "")
    p = state_path(d.get("session_id"))
    if compacted:   # the newest entry is a compaction: start the count again, say nothing
        save_state(p, {"stage": 0})
        return
    if not ctx:   # no size yet (a new session's first prompt): still record that the hooks run, for check
        save_state(p, load_state(p))
        return
    window, trigger, remind, final, rearm, _ = thresholds(ctx, model)
    st = load_state(p)
    if str(d.get("prompt") or "").lstrip().startswith("// Keep-warm ping"):
        st["ctx"] = ctx   # a ping's turn replies ✓ only, so a note given now would be used up unread
        save_state(p, st)
        return
    if ctx < rearm:
        st["stage"] = 0
    note = None
    if ctx >= final and st.get("stage", 0) < 2:
        st["stage"] = 2
        left = max(trigger - ctx, 0)
        note = ("Context check (the owner's long-session watcher): about {:,} tokens; automatic compaction is "
                "expected near {:,}, roughly {:,} tokens away, and its summary will replace the conversation. "
                "Write the handoff file now, in either mode (session-notes/<topic>/handoff.md, outside the "
                "checkout, by the owner's ai-best-practices skill, Recommendations and keywords, read again if "
                "it is not in your context), and keep it current with one-line edits until the compaction. If "
                "the owner is following the session, also end this turn with the line \"About {:,} tokens "
                "before automatic compaction. The handoff file is saved; if this is a good break, type /compact "
                "(Claude Code's command that shrinks the chat to a summary; I can't run it myself).\"; working "
                "alone, carry on."
                ).format(ctx, trigger, left, left // 1000 * 1000)
    elif remind and ctx >= remind and st.get("stage", 0) < 1:
        st["stage"] = 1
        note = ("Context check (the owner's long-session watcher): this conversation is about {:,} tokens, {}% of "
                "its {:,}-token window; automatic compaction is expected near {:,}. This is the earlier note "
                "set with CONTEXT_WATCH_REMIND and calls for nothing; the note that compaction is near comes "
                "later.").format(ctx, ctx * 100 // window, window, trigger)
    st["ctx"] = ctx
    save_state(p, st)
    if note:
        emit(d.get("hook_event_name") or "PostToolBatch", note)


def find_notes(dirs):
    """Every note under session-notes/ in the given folders, newest first; a
    folder name holding glob characters is taken literally, and links that lead
    nowhere are skipped."""
    files = []
    for base in dirs:
        root = os.path.join(glob.escape(base), NOTES_DIR)
        for f in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
            if f not in files and os.path.isfile(f):
                files.append(f)
    return sorted(files, key=os.path.getmtime, reverse=True)


def scratchpads(session_id):
    """A cloud session's scratchpad, /tmp/claude-<uid>/<project>/<session id>/scratchpad, where its
    notes live outside the checkout; found by the session id the hook's input carries."""
    sid = re.sub(r"[^A-Za-z0-9_-]", "", str(session_id or ""))
    if not sid:
        return []
    return sorted(p for p in glob.glob(os.path.join("/tmp", "claude-*", "*", sid, "scratchpad")) if os.path.isdir(p))


RELOAD = ("The owner's preferences ask for their ai-best-practices skill again after every compaction: load it with "
          "the Skill tool before acting on the handoff or on the owner's next message (on a keep-warm ping's turn, "
          "leave it for that message), since a skill invoked before a compaction may not come back with it (in one "
          "cloud session three invoked on 2026-10-19 never did, while one invoked on 2026-10-20 came back after the "
          "next two).")
KEYWORDS_WITHOUT_SKILL = ("The after-reply notice works without it: on \"away\" or \"away long\", run python3 %s "
                          "away (or away long) and follow what it prints; on \"wrap\", save a handoff file in "
                          "session-notes/<topic>/handoff.md and ask the owner to type /compact; on the owner's next "
                          "ordinary message, cancel any pings left.")
NO_SKILL = ("No copy of the owner's ai-best-practices skill synced from claude.ai was found (it may not be uploaded "
            "there, or Claude Code may still be downloading it), so the watcher's installed copies were not checked. "
            "If the Skill tool cannot load the skill either, tell the owner once (on a keep-warm ping's turn, leave "
            "this for their next message). " + KEYWORDS_WITHOUT_SKILL)


def reload_text():
    """RELOAD, and where no synced copy of the skill is found, how to act on the notice's keywords without it, since
    the start note that said so may not have come through the compaction."""
    if skill_folder():
        return RELOAD
    return RELOAD + " If the Skill tool cannot load it: " + KEYWORDS_WITHOUT_SKILL % os.path.abspath(__file__)


def after_compact(d):
    if d.get("agent_id"):
        return
    dirs = []
    for x in [d.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"), d.get("scratchpad_dir")] \
            + scratchpads(d.get("session_id")) + [config_dir()]:
        if isinstance(x, str) and x and x not in dirs:
            dirs.append(x)
    notes = find_notes(dirs)
    files = notes[:8]   # the listing; the file shown is chosen from all of them
    save_state(state_path(d.get("session_id")), {"stage": 0})
    if not files:
        emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
             "No %s/ folder was found under %s; if the session kept notes elsewhere, they are the reliable "
             "record of what was decided and what remains. %s"
             % (NOTES_DIR, " or ".join(dirs) or "the working folder", reload_text()))
        return
    now = time.time()
    base = dirs[0].rstrip(os.sep) + os.sep

    def show(f):
        return os.path.relpath(f, dirs[0]) if f.startswith(base) else f

    listing = "; ".join("%s (%d min ago)" % (show(f), (now - os.path.getmtime(f)) // 60) for f in files)
    handoff = next((f for f in notes if os.path.basename(f).lower() == "handoff.md"), None)   # newest first
    lead = handoff or next((f for f in notes if "progress" in os.path.basename(f).lower()), files[0])
    try:
        text = open(lead, errors="replace").read(12000)
    except OSError:
        text = ""
    if handoff:
        last = next((l.strip() for l in reversed(text.splitlines())
                     if l.strip() and not l.strip().startswith("<!--")), "")
        if last.lstrip("-* ").lower().startswith("resumed"):
            advice = ("It ends with a Resumed line, so it was already used after an earlier compaction: "
                      "treat it as history unless the summary says otherwise.")
        else:   # the transcript does not yet hold this compaction's record when the hook runs (seen 2026-10-20)
            advice = ("Read it first. If a message from the owner follows this note, as after a /compact they typed "
                      "at a break, act on that message rather than on the handoff's next step: if it is away, just "
                      "set up the pings; if it is a keep-warm ping, reply with only ✓. If none follows, the "
                      "compaction came on its own mid-task: continue from the handoff, even if it was written well "
                      "before. Once you act on it, add a line \"Resumed <UTC time>\" just before its <!-- end --> "
                      "marker.")
        emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
             "The handoff, %s, follows. %s %s Working notes on disk, newest first: %s.\n\n%s"
             % (show(lead), advice, reload_text(), listing, text[:6000]))
        return
    emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
         "%s Working notes on disk, newest first: %s. The start of %s follows.\n\n%s"
         % (reload_text(), listing, show(lead), text[:4000]))


def start(d):
    """SessionStart, any source but compact (after-compact covers that): keep the watcher's installed copies in step
    with the skill's copy synced from claude.ai, or say that none was found. The owner's preferences, which reach
    every session, have Claude load the skill (the owner, 2026-10-20)."""
    if d.get("agent_id") or d.get("source") == "compact":
        return
    lines, shown = [], None
    skill = skill_folder()
    if not skill:
        lines.append(NO_SKILL % os.path.abspath(__file__))
    elif is_cloud():
        repo = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd")
        r = installer(skill, ["--check", "--repo", repo]) if isinstance(repo, str) and repo else {}
        if r.get("installed") and r.get("differences"):
            lines.append("This repository's watcher differs from the skill's version %s (%s): update main now as the "
                         "skill's session rules say (in a worktree of origin/main, python3 %s --repo <worktree>, "
                         "then commit only .claude/ and push it to main, under the owner's standing go-ahead of "
                         "2026-10-20), and tell the owner in one line; on a keep-warm ping's turn, leave this for "
                         "their next message." % (r.get("version"), ", ".join(r["differences"]),
                                                  os.path.join(skill, "scripts", "install_watcher.py")))
        elif r.get("current"):
            lines.append("This repository's watcher matches the skill (version %s)." % r.get("version"))
        elif r.get("error"):
            lines.append("The watcher could not compare this repository's copy with the skill's (%s); run check."
                         % r["error"])
    elif installed_copy():
        r = installer(skill, ["--sync"])
        save_state(state_path(d.get("session_id")), load_state(state_path(d.get("session_id"))))   # for check
        line, shown = sync_line(r, r.get("version"))
        lines.append(line)
    if lines:
        emit("SessionStart", " ".join(lines), shown)


def find_transcript():
    projects = os.path.join(config_dir(), "projects")
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if sid:
        hits = glob.glob(os.path.join(projects, "*", glob.escape(sid) + ".jsonl"))
        if hits:
            return hits[0], sid
    proj = os.path.join(projects, re.sub(r"[^A-Za-z0-9]", "-", os.getcwd()))
    hits = sorted(glob.glob(os.path.join(proj, "*.jsonl")), key=os.path.getmtime, reverse=True)
    if not hits:
        hits = sorted(glob.glob(os.path.join(projects, "*", "*.jsonl")), key=os.path.getmtime, reverse=True)
    return (hits[0], os.path.basename(hits[0])[:-6]) if hits else (None, None)


def installed_in():
    """The settings files, the user's and this folder's, that hold a hook running this script."""
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    found, seen = [], set()
    for p in (os.path.join(config_dir(), "settings.json"), os.path.join(proj, ".claude", "settings.json"),
              os.path.join(proj, ".claude", "settings.local.json")):
        real = os.path.realpath(p)
        if real in seen:
            continue
        seen.add(real)
        try:
            hooks = json.load(open(p)).get("hooks")
        except (OSError, ValueError, AttributeError):
            continue
        if "context_watch.py" in json.dumps(hooks):
            found.append(p.replace(os.path.expanduser("~"), "~", 1))
    return found


def hooks_line(sid):
    """Whether the watcher's hooks have run in this session, and where they are installed."""
    p, where = state_path(sid), installed_in()
    if os.path.exists(p):
        return "yes, last ran %d s ago%s" % (time.time() - os.path.getmtime(p),
                                              " (installed in %s)" % ", ".join(where) if where else "")
    if where:
        return ("installed in %s, but none has run in this session yet: they run on the next prompt or tool call, "
                "so check again after one; if they still have not, restart the session (a cloud session loads "
                "them only when it starts or its worker restarts)" % ", ".join(where))
    return "none has run in this session, and none is installed in the user settings or this folder's .claude/"


def copies_line():
    """Whether the installed watcher matches the skill's copy: the repository's in a cloud session, else the
    user settings' and the hooks folder's; with the command that brings it in step."""
    skill = skill_folder()
    if not skill:
        return ("installed copies: not compared, since this script is not in the skill's folder and no copy of the "
                "skill synced from claude.ai is under %s" % os.path.join(config_dir(), "skills", "synced"))
    inst = os.path.join(skill, "scripts", "install_watcher.py")
    repo = (os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()) if is_cloud() else None
    r = installer(skill, ["--check"] + (["--repo", repo] if repo else []))
    where = repo or r.get("settings") or "the user settings"
    if r.get("error"):
        return "installed copies: not compared (%s)" % r["error"]
    if not r.get("installed"):
        return "installed copies: no watcher installed for %s (install it only at the owner's word)" % where
    if r.get("differences"):
        fix = ("update main from a worktree of origin/main with python3 %s --repo <worktree>, commit .claude/ and "
               "push it" % inst) if repo else "run python3 %s" % inst
        return ("installed copies: differ from this skill's version %s in %s, at %s: %s%s"
                % (r.get("version"), ", ".join(r["differences"]), where, fix,
                   "".join("; note: " + n for n in r.get("notes") or [])))
    return ("installed copies: the same as this skill's version %s, at %s%s"
            % (r.get("version"), where, "".join("; note: " + n for n in r.get("notes") or [])))


def check():
    path, sid = find_transcript()
    if not path:
        print("No Claude Code transcript found under %s." % os.path.join(config_dir(), "projects"))
        return
    ctx, model, compacted = read_tail_usage(path)
    print("transcript: %s" % path)
    if not ctx:
        print("No context size found yet%s." % (" since the compaction" if compacted else ""))
        print("watcher hooks: %s" % hooks_line(sid))
        print(copies_line())
        return
    window, trigger, remind, final, _, src = thresholds(ctx, model)
    print("context: %s tokens (%d%% of a %s window)%s" % (format(ctx, ","), ctx * 100 // window,
          format(window, ","), ", just compacted (summary only; overhead comes on top)" if compacted else ""))
    print("automatic compaction expected near: %s (%s)" % (format(trigger, ","), src))
    print("note at: %s%s" % (format(final, ","), "; earlier note at: %s" % format(remind, ",") if remind else ""))
    print("watcher hooks: %s" % hooks_line(sid))
    print(copies_line())
    _, reco = band_reco(ctx, window, trigger, final)
    print("recommendation: %s" % reco)


def is_cloud():
    """True in a Claude Code cloud session, which sets CLAUDE_CODE_REMOTE."""
    return os.environ.get("CLAUDE_CODE_REMOTE", "").strip().lower() in ("1", "true", "yes")


def suggestions_off():
    """Prompt suggestions off: the variable, which overrides the user settings'
    promptSuggestionEnabled (decision 7)."""
    sugg = os.environ.get("CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION", "").strip().lower()
    if sugg:
        return sugg in ("false", "0", "no", "off")
    try:
        with open(os.path.join(config_dir(), "settings.json"), encoding="utf-8") as f:
            s = json.load(f)
        return isinstance(s, dict) and s.get("promptSuggestionEnabled") is False
    except Exception:
        return False


def long_background():
    """A cloud session's background command may run past 2 hours, so one keep-awake
    command covers 12 hours; a local session has no such limit."""
    if not is_cloud():
        return True
    try:
        return int(float(os.environ.get("BASH_MAX_TIMEOUT_MS") or 0)) > 2 * 3600 * 1000
    except ValueError:
        return False


def one_read_pings():
    """True when a keep-warm ping costs one read of the context: prompt suggestions off and, in a cloud session, no
    keep-awake restart every 2 hours."""
    return suggestions_off() and long_background()


def pings_that_pay():
    """How many pings, 50 minutes apart, cost as much as one cold return (#807.2): about 40 with one-read pings, 22
    where 2-hour keep-awake restarts add a turn, 20 with prompt suggestions on, 12 with both."""
    if suggestions_off():
        return 40 if long_background() else 22
    return 20 if long_background() else 12


def reads_per_ping():
    """Reads of the whole context a ping costs on average: 1, about 1.8, 2 or about 3.3, by pings_that_pay()."""
    return 40 / pings_that_pay()


def money(x):
    """List-price dollars, in cents below a dollar."""
    return "%d¢" % max(1, round(x * 100)) if x < 0.995 else "$%.2f" % x


def costs(ctx, window=1_000_000):
    """What the advice rests on, in list-price dollars at Opus 5.5's prices: pings an hour at this size and at a
    compacted one, a cold return, a compaction, and the hours of pings that cost as much as each. A ping reads the
    context once per read; a cold return writes it all at the one-hour price (#805, #807.2). A compaction reads it once
    and adds COMPACT_EXTRA, its first ping after it being the rebuild, so decision 4's limit is where N pings at this
    size cost as much as the compaction and N - 1 pings at the compacted size, and never past the cold-return limit.
    The compaction's figures were measured on a 1M window and scale with a smaller one."""
    scale = window / 1_000_000
    c, s, r = ctx / 1e6, COMPACTED * scale / 1e6, reads_per_ping()
    ping, small = READ_PRICE * c * r, READ_PRICE * s * r
    compact = READ_PRICE * c + COMPACT_EXTRA * scale
    cold_hours = round(pings_that_pay() * PING_GAP / 60)
    if ping > small:
        compact_hours = min(cold_hours, max(1, round((compact - small) / (ping - small) * PING_GAP / 60)))
    else:
        compact_hours = cold_hours   # compacting would save nothing a ping costs
    return {"hour": ping * 60 / PING_GAP, "small_hour": small * 60 / PING_GAP, "ping": ping,
            "cold": WRITE_PRICE * c, "compact": compact, "cold_hours": cold_hours, "compact_hours": compact_hours,
            "repay": max(1, round(compact / max(READ_PRICE * (c - s), 1e-9))),
            "reads": ("reads the chat once from the cache" if r < 1.2 else
                      "costs about two reads of the chat from the cache (%s)" % (
                          "prompt suggestions are on" if not suggestions_off() else
                          "with the keep-awake command restarted every 2 hours") if r < 2.5 else
                      "costs about three reads of the chat from the cache (prompt suggestions on, keep-awake "
                      "restarted every 2 hours)")}


def limit_hours(ctx, window, final):
    """The band's limit for plain "away": below 60%, as long as pings cost less than a cold return; from 60% to the
    note, as long as they cost less than compacting first (decision 4); near the point, none."""
    k = costs(ctx, window)
    if ctx >= final:
        return 0
    return k["cold_hours"] if ctx < window * 60 // 100 else k["compact_hours"]


def band_reco(ctx, window, trigger, final, verbose=False):
    """Return (band, recommendation) for the current size, as prepared text so the decision is a lookup, not a
    computation. The short form is one line for Claude's own in-context use (`check`'s last line, which a reply ends
    with where no notice is installed). verbose gives the full list for `status`, in markdown, which Claude relays in
    chat as printed: the size and what the band means, then every option at that size as a bullet with its hours and
    costs, explained in indented ones; the notice after each reply is notice_line(), one line from the same figures
    (the owner's requests, 2026-10-20). The owner sends "away" (or says they are leaving), "away long" past the band's
    limit, or either with a task, which Claude does first, deciding at the size then reached:
      band 0  below 60% of the window: pings until back, which cost less than a cold return for ~33 h one-read;
              "away long" past that: let the cache go cold (no compaction, decision 3)
      band 1  60% up to the note point: pings cost less than compacting first for ~9 h at 600k, ~8 at the cloud
              note, ~6 at a local one (half that with two-read pings, decision 4); "away long" past that:
              handoff + /compact; "wrap" to compact now at a break
      band 2  within the note margin of the point: "wrap" at a break, and handoff + /compact before any absence."""
    c, p, pct = ctx // 1000, trigger // 1000, min(ctx * 100 // max(trigger, 1), 99)
    k, hours = costs(ctx, window), limit_hours(ctx, window, final)
    gloss = "Claude Code's command that shrinks the chat to a summary, which I cannot run myself"
    machine = ("  - This cloud session needs nothing from your computer meanwhile; it can be off." if is_cloud() else
               "  - Keep the computer awake and this session open meanwhile, since the pings run there (desktop app: "
               "Settings > This computer > System > Keep computer awake).")
    head = "**Long-session advisor** · %dk of %dk tokens used (%d%% of the way to automatic compaction)" % (c, p, pct)
    foot = ("_Costs are list-price equivalents at Opus 5.5's prices, a cached read $0.20 per million tokens and a "
            "cache write $8, which your plan's usage bars follow about in step (a point of the five-hour bar is about "
            "$8.40 on Max 20x, $0.42 on Pro); a compaction's cost varies by about half either way. The one-line notice "
            "under each reply is free: you see it, and it never enters my context. Worked out from this account's "
            "measurements, 17–20 October 2026._")
    hour = ["- **Away under an hour** → send nothing",
            "  - Within your plan's usage the chat's memory cache stays warm for an hour, so your next message is a "
            "cheap warm read."]
    back = ["- **Back** → just write as usual",
            "  - Your first message cancels the pings left, and I tell you in one line whether the chat stayed warm."]
    ping = ("  - A one-character ping every 50 minutes until you are back; each %s, about %s at this size, about %s "
            "an hour." % (k["reads"], money(k["ping"]), money(k["hour"])))

    def timed(h):
        return ['- **"away" with a time**, such as "away 10h", "away overnight" or "away 2d" → when you are unsure '
                'which fits',
                "  - I compare it with the %d-hour limit above and do whichever fits." % h]

    if ctx >= final:
        band = 2
        due = "due in ~%dk" % (p - c) if p > c else "due now"
        short = ('%dk/%dk · compaction %s · at a break, "wrap" (I save a handoff file, then you type '
                 '/compact) · leaving over 1h, "away" (the same, then pings until you are back)' % (c, p, due))
        long = [head, "", "Automatic compaction is close, %s: it will summarise the chat in place soon, mid-task if "
                "it comes to that." % ("about %dk tokens away" % (p - c) if p > c else "due at the next request"), "",
                '- **"wrap"** → suggested, at a clean break',
                "  - I save a handoff file with everything needed to carry on (the task, what is done, what is next), "
                "then you type /compact (%s), so it happens at this break rather than mid-task." % gloss,
                "  - It costs nothing extra, since the compaction is due anyway.",
                '- **"away"**, or just say you are leaving → for over an hour',
                "  - The same handoff file and /compact first, then a ping every 50 minutes keeps the smaller chat warm "
                "until you are back, about %s an hour." % money(k["small_hour"]),
                machine,
                "- **Away under an hour** → send nothing",
                "  - The cache stays warm for an hour; the compaction comes once work goes on, so a \"wrap\" first is "
                "still worth it at a clean break.",
                '- **A task in the same message as "away"** → task first',
                "  - I do the task, keeping the handoff file current, so nothing is lost if the chat compacts on its "
                "own meanwhile; then I keep it warm while that pays.",
                "- **Otherwise** → just carry on",
                "  - It compacts on its own, and the handoff file I keep means nothing is lost."] + back
    elif ctx >= window * 60 // 100:
        band = 1
        short = ('%dk/%dk · away 1–%dh, "away" (pings until you are back, ~%s/h) · longer, "away long" (a handoff '
                 'file, you type /compact, ~%s, then pings, ~%s/h) · at a break, "wrap" (a handoff file, then you '
                 'type /compact)' % (c, p, hours, money(k["hour"]), money(k["compact"]), money(k["small_hour"])))
        long = [head, "", "This chat is past 60% of its window, where compacting starts to pay against a long "
                "absence.", ""] + hour + [
                '- **"away"**, or just say you are leaving → I keep the chat warm, for absences up to about %d hours'
                % hours, ping,
                "  - Past about %d hours that adds up to more than compacting first: about %s for the summary and the "
                "rebuild after it, after which pings cost about %s an hour." % (hours, money(k["compact"]),
                                                                                money(k["small_hour"])),
                "  - If automatic compaction comes near while you are gone, I save the handoff file first.",
                machine,
                '- **"away long"** → for longer absences, say overnight',
                "  - I save a handoff file (the task, what is done, what is next) and ask you to type /compact before "
                "you go (%s)." % gloss,
                "  - Then I keep the smaller chat warm, about %s an hour." % money(k["small_hour"])] + timed(hours) + [
                '- **A task in the same message as "away" or "away long"** → task first',
                "  - I do the task, then decide by the size the chat has reached, since no one can know beforehand "
                "how much a task adds.",
                "  - With you gone I cannot ask for /compact, so where one is due I save the handoff file instead, and "
                "keep the chat warm, which still costs less than a cold start (about %s now) for about %d hours."
                % (money(k["cold"]), k["cold_hours"]),
                '- **"wrap"** → staying, but at a clean break',
                "  - I save the handoff file, then you type /compact, so the chat compacts at this break rather than "
                "mid-task, and nothing is lost.",
                "  - About %s, repaid within about %d requests, since each later one reads a smaller chat."
                % (money(k["compact"]), k["repay"])] + back
    else:
        band = 0
        floor = window * 60 // 100 // 1000
        short = ('%dk/%dk · away 1–%dh, "away" (pings until you are back, ~%s/h) · longer, "away long" (no pings; '
                 'one cold start on return, ~%s) · compacting not worth it below %dk'
                 % (c, p, hours, money(k["hour"]), money(k["cold"]), floor))
        long = [head, "", "This chat is below 60% of its window, so compacting is not worth it yet: for an absence the "
                "choice is between keeping the chat warm with pings and letting it go cold.", ""] + hour + [
                '- **"away"**, or just say you are leaving → I keep the chat warm, for absences up to about %d hours'
                % hours, ping,
                "  - Past about %d hours the pings add up to more than one cold start, about %s at this size: your "
                "first message after an hour away rewrites the whole chat to the cache." % (hours, money(k["cold"])),
                machine,
                '- **"away long"** → for longer absences, say days',
                "  - No pings: your first message back pays the cold start once, about %s." % money(k["cold"]),
                "  - If your next task is unrelated to this chat, a new session is cheaper still."] + timed(hours) + [
                '- **A task in the same message as "away" or "away long"** → task first',
                "  - I do the task, then decide by the size the chat has reached whether pings still pay, since no "
                "one can know beforehand how much a task adds."] + back + [
                "- **/compact** → not yet",
                "  - Compacting saves little below %dk, and the summary loses detail." % floor]
    return band, ("\n".join(long + ["", foot]) if verbose else short)


def footer(d):
    """Stop hook: show the owner the notice without spending any tokens. A hook's systemMessage reaches the owner on
    any platform and is not added to Claude's context; only async hooks feed Claude, and this one is not async."""
    if d.get("agent_id"):
        return
    ctx, model, compacted = read_tail_usage(d.get("transcript_path") or "")
    if not ctx or compacted:
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    print(json.dumps({"systemMessage": notice_line(ctx, window, trigger, final)}))


def notice_line(ctx, window, trigger, final):
    """The notice, on one line: the apps print "Stop says:" before every line of a hook's message, whatever the line
    break, and render no markdown (seen 2026-10-20). So it gives the size, then for each length of absence the
    keyword and what it costs, so that the hours where pings stop paying show at a glance, parted by " | "; `status`
    gives the full list, explained (the owner's requests, 2026-10-20)."""
    c, p, pct = ctx // 1000, trigger // 1000, min(ctx * 100 // max(trigger, 1), 99)
    k, hours = costs(ctx, window), limit_hours(ctx, window, final)
    awake = "" if is_cloud() else ", computer awake"
    size = "Tokens used: %dk of %dk (%d%%)" % (c, p, pct)
    under = "Away under 1 h: nothing"
    unsure = 'Unsure: "away 10h" → I pick'
    task = 'With a task: "away" + task → done first'
    status = 'All options explained: "status"'
    if ctx >= final:
        parts = [size + (", compaction due in ~%dk" % (p - c) if p > c else ", compaction due now"),
                 'Suggested at a break: "wrap" → handoff, you type /compact',
                 'Away over 1 h: "away" → the same, then pings, ~%s/h%s' % (money(k["small_hour"]), awake),
                 under, task, status]
    elif ctx >= window * 60 // 100:
        parts = [size, under,
                 '1–%d h: "away" → pings, ~%s/h%s' % (hours, money(k["hour"]), awake),
                 'Over %d h: "away long" → handoff, you type /compact (~%s), then pings, ~%s/h'
                 % (hours, money(k["compact"]), money(k["small_hour"])),
                 'At a break: "wrap" → handoff, you type /compact', unsure, task, status]
    else:
        parts = [size, under,
                 '1–%d h: "away" → pings, ~%s/h%s' % (hours, money(k["hour"]), awake),
                 'Over %d h: "away long" → no pings, one cold start on return (~%s)' % (hours, money(k["cold"])),
                 unsure, task, status]
    return " | ".join(parts)


def recommend():
    """`status`: every option at this size, formatted in markdown and explained, for Claude to relay in chat as
    printed; the notice after each reply gives one line of it."""
    path, _ = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    if not ctx:
        print("context size not found yet%s." % (" since the compaction" if compacted else ""))
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    _, reco = band_reco(ctx, window, trigger, final, verbose=True)
    print(reco)


def parse_duration(s):
    """Minutes from '3h', '90m', '2h30m', '2d' or '2 days', '1w', 'overnight'/'night'
    (=12h), or a bare number of hours. None when nothing usable is given (a bare 'away')."""
    s = (s or "").strip().lower()
    if not s or s == "away":
        return None
    per = {"m": 1, "h": 60, "d": 24 * 60, "w": 7 * 24 * 60, "": 60}
    total, found = 0, False
    for n, unit in re.findall(r"(\d+)\s*([hmdw]?)", s):
        total += int(n) * per[unit]
        found = True
    if found and total > 0:
        return total
    for word, mins in (("weekend", 60 * 60), ("week", 7 * 24 * 60), ("tomorrow", 16 * 60),
                       ("overnight", 12 * 60), ("night", 12 * 60), ("day", 24 * 60)):
        if word in s:
            return mins
    return None


def ping_times(n, gap=50):
    """n times, gap minutes apart from now, none on :00 or :30: each a UTC date and time,
    with the machine's local time beside it for a scheduler that takes local time."""
    now = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
    out, t = [], now
    for _ in range(max(0, n)):
        t += datetime.timedelta(minutes=gap)
        show = t + datetime.timedelta(minutes=2) if t.minute in (0, 30) else t
        out.append("%s (local %s)" % (show.strftime("%Y-%m-%d %H:%MZ"), show.astimezone().strftime("%a %Y-%m-%d %H:%M")))
    return out


def away(arg):
    """Print the whole leave plan, so Claude only has to follow it. No duration is
    needed: pings run until the owner's next message, which cancels the rest, so
    only those sent while away are paid for. The owner adds "long" only when the
    absence will pass the band's limit, which the notice states; by decisions 3 and
    4, below 60% that means letting the cache go cold, from 60% to the note a
    handoff and /compact first, and within the note's margin plain "away" already
    means that. A duration still works: it counts as long when it passes the limit."""
    path, _ = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    if not ctx:
        print('context size not found; run "check" first, then decide by decisions 3 and 4.')
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    band, reco = band_reco(ctx, window, trigger, final)
    limit = limit_hours(ctx, window, final)
    pay = pings_that_pay()
    pay_hours = round(pay * PING_GAP / 60)
    a = (arg or "").strip().lower()
    if a in ("", "away", "short"):
        long_away = False
    elif a in ("long", "longer", "days", "for days", "a long time"):
        long_away = True
    else:
        mins = parse_duration(a)
        if not mins:
            print('not understood: "%s". Run "away", "away long", or "away" with a time such as 10h, overnight, '
                  'tomorrow, weekend or 3d.' % a)
            return
        long_away = mins > limit * 60
    print("context: %s tokens (%d%% of %s); compaction near %s; %s"
          % (format(ctx, ","), ctx * 100 // window, format(window, ","), format(trigger, ","),
             "away long" if long_away else "away"))
    print("if work is under way, or the owner left a task with this: do it first; when it is done, run away again, "
          "which decides afresh at the size then reached (pings, a handoff first, or letting the cache go cold), and "
          "follow that, leaving out any step the owner would have to take, such as /compact")
    if band == 0 and long_away:
        print("plan: no pings and no compaction. Past about %d hours pings cost more than one cold return, and "
              "below 60%% compacting is not worth the lost detail, so let the cache go cold (a fresh session is "
              "cheaper if the next task is unrelated). Say so in one line." % pay_hours)
        if not is_cloud() and not os.environ.get("CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS"):
            print("  terminal: a session of 200,000 tokens or more compacts itself after about 54 idle minutes unless "
                  "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS is set (the installer sets 600000, decision 3); say so if it applies")
        return
    cloud = is_cloud()
    hours = (12 if long_background() else 2) if cloud else 33
    batch = min(pay, (hours * 60 - 55 + 49) // 50)
    if band == 2 or (band == 1 and long_away):
        print("plan: handoff and /compact first, then pings at the smaller size")
        print("  1. write or refresh the handoff file (session-notes/<topic>/handoff.md) and say in one line where it "
              "is and what it covers")
        print('  2. end the reply with: "Ready: type /compact (Claude Code\'s command that shrinks the chat to a '
              'summary; I can\'t run it myself) before you go."')
        print("  3. in the same turn, schedule the pings below; they keep the chat warm, compacted once the owner "
              "has typed /compact")
    else:
        print("plan: pings until the owner is back (pinging beats %s for up to about %d hours)"
              % ("a cold return" if band == 0 else "compacting at this size", limit))
    print("pings: %d one-shot tasks, 50 minutes apart, covering about %d hours: %s"
          % (batch, round(batch * 50 / 60), ", ".join(ping_times(batch))))
    print('  each prompt: "// Keep-warm ping. Reply with only ✓."; create the whole batch in one message')
    if cloud:
        print("  cloud: first leave the repository's checkout clean where the owner's rules allow (commit and push, or "
              "keep files outside it): the environment's Stop hook asks for a commit at the end of every turn while it "
              "is not, a second request on every ping; if it cannot be, say in one line that each ping costs double. On "
              "a ping's turn that request gets the same reply, ✓, and nothing is committed")
        print("  cloud: also start, with run_in_background and a timeout of %d ms, the keep-awake command "
              "`while :; do date -u +%%FT%%TZ >> /tmp/keep-awake.log; sleep 60; done`; when it ends with the "
              "owner still away, start it again and schedule the next batch, up to %d pings (about %d hours) "
              "in all" % (hours * 3600 * 1000, pay, pay_hours))
    else:
        print("  local: say in the reply that the pings need the computer awake and this session left open (desktop "
              "app: Settings > This computer > System > Keep computer awake)")
        if not os.environ.get("CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS"):
            print("  terminal: a session of 200,000 tokens or more compacts itself after about 54 idle minutes "
                  "unless CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS is set (the installer sets 600000); the pings prevent it")
    print("  on the owner's next ordinary message: cancel the pings left (list the scheduled tasks and delete "
          "each), stop the keep-awake command, read /tmp/keep-awake.log if there is one, and report in one line")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode in ("-h", "--help", "help"):
        print(__doc__)
        return
    if mode == "check":
        check()
        return
    if mode in ("recommend", "status"):
        recommend()
        return
    if mode == "away":
        away(" ".join(sys.argv[2:]))
        return
    try:
        d = json.load(sys.stdin)
        if not isinstance(d, dict):
            return
        if mode == "watch":
            watch(d)
        elif mode == "start":
            start(d)
        elif mode == "after-compact":
            after_compact(d)
        elif mode == "footer":
            footer(d)
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
