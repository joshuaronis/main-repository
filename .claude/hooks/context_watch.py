#!/usr/bin/env python3
"""Context watcher for long Claude Code sessions.

Hook modes read the hook's JSON on stdin and always exit 0, so they never block:
  start          SessionStart, any source but compact. Locally it brings the
                 installed watcher in step with the skill's copy synced from
                 claude.ai (install_watcher.py --sync) and says what it found or
                 changed; in a cloud session it compares the repository's copy
                 with that one and tells Claude to update main when they differ.
                 With no synced copy it says so, with how to act on the notice's
                 keywords without the skill. In a local session, which gets no
                 claude.ai preferences, it also asks Claude to load the skill
                 unless a CLAUDE.md the session reads names it.
  watch          PostToolBatch and UserPromptSubmit. Once the context comes
                 within 80,000 tokens of compaction, adds one short note to
                 Claude's context asking for the handoff file, and records when,
                 so the notice can say once it is saved; silent otherwise, and
                 silent right after a compaction, which starts the count again.
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
  recommend      Everything the advice rests on at this size, formatted and
                 explained, with list-price costs, for Claude to relay in chat
                 (alias status); the notice points to it.
  away [long]    Print the plan for an absence: any work finished first, the
                 handoff written when compaction is near, then pings until the
                 owner is back, for up to about 33 hours, or with "long", for an
                 absence past that, no pings; never a step of the owner's, who
                 has left. Other words after it, such as a time, change nothing. Claude follows the printout, so the per-turn thinking
                 stays trivial.
  footer         Stop hook: emit the recommendation as a systemMessage, shown to
                 the owner after the reply and NOT added to Claude's context, so
                 it costs no tokens on any turn: one line, the tokens used; near
                 compaction, whether the handoff is saved, with the suggestion to
                 type /compact at a break or on return; and what "away" and "away
                 long" do and cost; `status` gives the rest.

Context = input + cache_creation + cache_read tokens of the newest main-chain
assistant message in the transcript, skipping synthetic and zero-usage ones.
The transcript format is undocumented and may lag one message. The watcher
costs no usage: it reads the transcript tail on this machine in a few tens of
milliseconds. It keeps its state in context-watch/ in Claude Code's
configuration folder, ~/.claude or CLAUDE_CONFIG_DIR, where it also finds the
user settings and the transcripts.

Settings, all optional, as environment variables:
  CONTEXT_WATCH_FINAL   the note, in tokens (default 80,000 below compaction)
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
VERSION = "2026-10-21.4"     # this release; install_watcher.py compares the files themselves
SKILL_NAME = "ai-best-practices"
PING_GAP = 50                # minutes between keep-warm pings, inside the cache's one-hour lifetime
READ_PRICE = 0.20            # $ per million tokens read from the cache, Opus 5.5's list price (#805)
WRITE_PRICE = 8.00           # $ per million written at the one-hour price: what a cold return pays (#805)
COMPACT_EXTRA = 0.95         # $ a compaction adds to its read: the summary's output, $0.08-0.35 (#805), and the
                             # rebuild after it, $0.38-0.69 in 10 and $1.02-1.11 in 4 of one cloud session's 14
                             # compactions of 2026-10-17 to 20 (#807.2)
COMPACTED = 140_000          # tokens after a compaction, overhead included: 113,000-152,000 in those 14
NOTE_MARGIN = 80_000         # the note, the handoff and the notice's /compact suggestion, this far before compaction:
                             # about 70% of a cloud session's window, 89% of a local one's (the owner, 2026-10-21)


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
    final = env_tokens("CONTEXT_WATCH_FINAL", trigger - NOTE_MARGIN * scale // 1_000_000)
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


def version_key(v):
    """A VERSION such as 2026-10-20.5 as a pair that sorts by release; None when absent or unreadable."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})\.(\d+)$", str(v or ""))
    return (m.group(1), int(m.group(2))) if m else None


def newer_installed(r):
    """True when an installer's report shows the installed watcher newer than the copy it compared it with, worked
    out here from the two versions, since an older installer does not report it."""
    have, new = version_key(r.get("installed_version")), version_key(r.get("version"))
    return bool(r.get("newer_installed") or (have and new and have > new))


def sync_line(r, version_shown):
    """(line for Claude, line shown to the owner) after a local --sync."""
    if newer_installed(r) and not r.get("updated"):
        return ("The installed watcher, version %s, is newer than the skill synced from claude.ai, version %s, so it "
                "was left as it is: tell the owner once that the newer skill has not reached claude.ai yet (on a "
                "keep-warm ping's turn, leave this for their next message)." % (r.get("installed_version"),
                                                                                 r.get("version")), None)
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
        st.pop("note_at", None)
    note = None
    if ctx >= final and st.get("stage", 0) < 2:
        st["stage"], st["note_at"] = 2, time.time()   # a handoff saved after this is the one the notice can call saved
        left = max(trigger - ctx, 0)
        note = ("Context check (the owner's long-session watcher): about {:,} tokens; automatic compaction is "
                "expected near {:,}, roughly {:,} tokens away, and its summary will replace the conversation. "
                "Write the handoff file now (session-notes/<topic>/handoff.md, outside the checkout, by the owner's "
                "ai-best-practices skill, Recommendations and keywords, read again if it is not in your context), "
                "then carry on with the work: never stop, end a turn or wait for the compaction, and never ask the "
                "owner to compact, since the notice under each reply tells them. Until the compaction, keep the "
                "handoff current in every turn that moves the work on and after each step of a long one, with "
                "small, targeted edits sent alongside tool calls the work already makes."
                ).format(ctx, trigger, left)
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


RELOAD = ("The owner wants their ai-best-practices skill loaded again after every compaction: load it with "
          "the Skill tool before acting on the handoff or on the owner's next message (on a keep-warm ping's turn, "
          "leave it for that message), since a skill invoked before a compaction may not come back with it (in one "
          "cloud session three invoked on 2026-10-19 never did, while one invoked on 2026-10-20 came back after the "
          "next two).")
KEYWORDS_WITHOUT_SKILL = ("The after-reply notice works without it: on \"away\" or \"away long\", run python3 %s "
                          "away (or away long) and follow what it prints; on the owner's next ordinary message, cancel "
                          "any pings left.")
NO_SKILL = ("No copy of the owner's ai-best-practices skill synced from claude.ai was found (it may not be uploaded "
            "there, or Claude Code may still be downloading it), so the watcher's installed copies were not checked. "
            "If the Skill tool cannot load the skill either, tell the owner once (on a keep-warm ping's turn, leave "
            "this for their next message). " + KEYWORDS_WITHOUT_SKILL)


LOAD_LOCAL = ("Load the owner's ai-best-practices skill with the Skill tool before the first task (on a keep-warm "
              "ping's turn, leave it for their next message): the owner wants it in every session, and a local session "
              "receives no claude.ai preferences, while no CLAUDE.md this session reads names it.")


def preferences_name_skill(d):
    """True when a CLAUDE.md that a local session reads at launch names this skill: the user's, where the owner's
    preferences live locally, or the project's."""
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or os.getcwd()
    for p in (os.path.join(config_dir(), "CLAUDE.md"), os.path.join(proj, "CLAUDE.md"),
              os.path.join(proj, ".claude", "CLAUDE.md"), os.path.join(proj, "CLAUDE.local.md")):
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                if SKILL_NAME in f.read():
                    return True
        except OSError:
            continue
    return False


def reload_text():
    """RELOAD, and where no synced copy of the skill is found, how to act on the notice's keywords without it, since
    the start note that said so may not have come through the compaction."""
    if skill_folder():
        return RELOAD
    return RELOAD + " If the Skill tool cannot load it: " + KEYWORDS_WITHOUT_SKILL % os.path.abspath(__file__)


def notes_dirs(d):
    """The folders whose session-notes/ the watcher searches, in this order: the hook's cwd, CLAUDE_PROJECT_DIR, any
    scratchpad_dir the input gives, a cloud session's scratchpad, found by its session id, and Claude Code's
    configuration folder, where a local session without a scratchpad keeps its notes."""
    dirs = []
    for x in [d.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"), d.get("scratchpad_dir")] \
            + scratchpads(d.get("session_id")) + [config_dir()]:
        if isinstance(x, str) and x and x not in dirs:
            dirs.append(x)
    return dirs


def handoff_ready(d):
    """True when a handoff.md among the session's notes was saved after the watcher's note, so that the notice can
    tell the owner it is ready for their /compact; False before the note, or with none saved since."""
    t = load_state(state_path(d.get("session_id"))).get("note_at")
    if not t:
        return False
    try:
        return any(os.path.basename(f).lower() == "handoff.md" and os.path.getmtime(f) >= t
                   for f in find_notes(notes_dirs(d)))
    except OSError:
        return False


def after_compact(d):
    if d.get("agent_id"):
        return
    dirs = notes_dirs(d)
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
    with the skill's copy synced from claude.ai, or say that none was found. A cloud session's claude.ai preferences
    have Claude load the skill; a local session gets none, so there the note asks for it unless a CLAUDE.md the
    session reads names the skill (the owner's test, 2026-10-20)."""
    if d.get("agent_id") or d.get("source") == "compact":
        return
    lines, shown = [], None
    skill = skill_folder()
    if not skill:
        lines.append(NO_SKILL % os.path.abspath(__file__))
    elif is_cloud():
        repo = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd")
        r = installer(skill, ["--check", "--repo", repo]) if isinstance(repo, str) and repo else {}
        if r.get("installed") and r.get("differences") and newer_installed(r):
            lines.append("This repository's watcher, version %s, is newer than the skill synced from claude.ai, "
                         "version %s: leave main as it is, and tell the owner once that the newer skill has not "
                         "reached claude.ai yet (on a keep-warm ping's turn, leave this for their next message)."
                         % (r.get("installed_version"), r.get("version")))
        elif r.get("installed") and r.get("differences"):
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
        r = installer(skill, ["--check"])
        if not newer_installed(r):   # an older installer's --sync would replace a newer copy
            r = installer(skill, ["--sync"])
        save_state(state_path(d.get("session_id")), load_state(state_path(d.get("session_id"))))   # for check
        line, shown = sync_line(r, r.get("version"))
        lines.append(line)
    if skill and not is_cloud() and not preferences_name_skill(d):
        lines.insert(0, LOAD_LOCAL)
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
    if r.get("differences") and newer_installed(r):
        return ("installed copies: newer than this skill's version %s (%s, at %s): leave them as they are; the newer "
                "skill has not reached claude.ai yet" % (r.get("version"), r.get("installed_version"), where))
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
    ready = ctx >= final and handoff_ready({"cwd": os.getcwd(), "session_id": sid})
    _, reco = band_reco(ctx, window, trigger, final, ready=ready)
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
    """What the advice rests on, in list-price dollars at Opus 5.5's prices: a ping and pings an hour at this size, a
    cold return, a compaction, the size it leaves, the requests it takes to repay itself, and the hours of pings that
    cost as much as one cold return. A ping reads the context once per read and a cold return writes it all at the
    one-hour price (#805, #807.2), so those hours are the same at every size. A compaction reads the context once and
    adds COMPACT_EXTRA, leaving about COMPACTED; its figures were measured on a 1M window and scale with a smaller
    one."""
    scale = window / 1_000_000
    c, s, r = ctx / 1e6, COMPACTED * scale / 1e6, reads_per_ping()
    ping = READ_PRICE * c * r
    compact = READ_PRICE * c + COMPACT_EXTRA * scale
    return {"hour": ping * 60 / PING_GAP, "ping": ping, "cold": WRITE_PRICE * c, "compact": compact,
            "after": int(COMPACTED * scale), "cold_hours": round(pings_that_pay() * PING_GAP / 60),
            "repay": max(1, round(compact / max(READ_PRICE * (c - s), 1e-9))),
            "reads": ("reads the chat once from the cache" if r < 1.2 else
                      "costs about two reads of the chat from the cache (%s)" % (
                          "prompt suggestions are on" if not suggestions_off() else
                          "with the keep-awake command restarted every 2 hours") if r < 2.5 else
                      "costs about three reads of the chat from the cache (prompt suggestions on, keep-awake "
                      "restarted every 2 hours)")}


def band_reco(ctx, window, trigger, final, verbose=False, ready=False):
    """Return (band, recommendation) for the current size, as prepared text so the decision is a lookup: band 0 below
    the note, 1 from it. The short form is one line for Claude's own use (`check`'s last line, which a reply ends
    with where no notice is installed); verbose gives the full explanation for `status`, in markdown, which Claude
    relays as printed. One keyword leaves, "away": pings until the owner is back, for at most the pings that cost one
    cold return; for a longer absence the owner sends nothing. Claude prepares a compaction and never waits on one:
    from the note it writes the handoff, and the advice suggests /compact at a break or on return (the owner,
    2026-10-21). `ready` says whether the handoff has been saved since the note."""
    c, p, pct = ctx // 1000, trigger // 1000, min(ctx * 100 // max(trigger, 1), 99)
    k = costs(ctx, window)
    hours, n = k["cold_hours"], pings_that_pay()
    gloss = "Claude Code's command that shrinks the chat to a summary, which I cannot run myself"
    machine = ("  - This cloud session needs nothing from your computer meanwhile; it can be off." if is_cloud() else
               "  - Keep the computer awake and this session open meanwhile, since the pings run there (desktop app: "
               "Settings > This computer > System > Keep computer awake).")
    head = "**Long-session advisor** · %dk of %dk tokens used (%d%% of the way to automatic compaction)" % (c, p, pct)
    foot = ("_Costs are list-price equivalents at Opus 5.5's prices, a cached read $0.20 per million tokens and a "
            "cache write $8, which your plan's usage bars follow about in step (a point of the five-hour bar is about "
            "$8.40 on Max 20x, $0.42 on Pro); a compaction's cost varies by about half either way. The one-line notice "
            "under each reply is free: you see it, and it never enters my context. Worked out from this account's "
            "measurements, 17–21 October 2026._")
    pings = ('pings until you are back, ~%s/h; cheaper than a cold start for ~%dh) · longer, "away long" (no pings; '
             'one cold start on return, ~%s' % (money(k["hour"]), hours, money(k["cold"])))
    leave = [
        '- **"away"**, or just say you are leaving → pings until you are back',
        "  - If I am working, I finish first. Then a one-character ping every 50 minutes; each %s, about %s at this "
        "size, about %s an hour." % (k["reads"], money(k["ping"]), money(k["hour"])),
        "  - They stop by themselves after %d pings, about %d hours, when they have cost what one cold start would. "
        "That holds at any size: a ping reads the chat from the cache and a cold start writes it all again, at 40 "
        "times a read's price, so both grow with the chat." % (n, hours),
        machine,
        "  - You can leave as soon as you send it: nothing in the plan waits for you.",
        '- **"away long"** → for an absence of more than about %d hours, such as a weekend' % hours,
        "  - No pings: your first message back pays one cold start, about %s at this size, less than pinging that long "
        "would; if the next task is unrelated to this chat, a new session is cheaper still." % money(k["cold"]),
        "  - As with \"away\", I finish any work first, and near the compaction point I still save the handoff, so you "
        "can type /compact when you are back."]
    if is_cloud():
        leave.append("  - If the cloud machine restarts while you are away, it stops my keep-awake command and drops "
                     "the scheduled pings; its notice wakes me, and I schedule the rest again (about 40–50¢ each "
                     "time; it happened twice on 21 October 2026).")
    leave += ["- **Back** → just write as usual",
              "  - Your first message cancels the pings left, and I tell you in one line whether the chat stayed warm.",
              "- **Effort** → no need to lower it before you leave",
              "  - A ping's reply is one character with no thinking, so it costs only the read, which effort does not "
              "change (measured 21 October 2026)."]
    if ctx >= final:
        band = 1
        where = "about %dk tokens away" % (p - c) if p > c else "due at the next request"
        due = "due in ~%dk" % (p - c) if p > c else "due now"
        saved = ("handoff saved: type /compact at a break or when back (~%s)" if ready else
                 "handoff not saved yet: I write it, then you type /compact at a break (~%s)") % money(k["compact"])
        short = '%dk/%dk · compaction %s · %s · leaving, "away" (%s)' % (c, p, due, saved, pings)
        lines = [head, "", "Automatic compaction is %s and would summarise the chat in place, mid-task if it comes to "
                 "that. I prepare it, and you choose when." % where, "",
                 "- **/compact** → at your next break, or as soon as you are back",
                 "  - " + ("The handoff file is saved, with what is done and what is next, and I keep it current."
                           if ready else "I write the handoff file first, with what is done and what is next; this "
                           "list and the notice say when it is saved."),
                 "  - Then type /compact (%s): about %s, leaving about %dk tokens, which repays itself within about %d "
                 "requests if you go on working." % (gloss, money(k["compact"]), k["after"] // 1000, k["repay"]),
                 "  - If you leave first, the pings keep the chat warm until you are back; compact then."] + leave
    else:
        band = 0
        short = '%dk/%dk · leaving, "away" (%s) · /compact not yet: suggested from ~%dk' % (c, p, pings, final // 1000)
        lines = [head, "", "Compaction is not due yet, so for an absence the choice is pings or a cold start, and "
                 "pings win for any absence under about %d hours." % hours, ""] + leave + [
                 "- **/compact** → not yet",
                 "  - Automatic compaction is about %dk tokens away. From about %dk, %dk before it, I write a handoff "
                 "file and the notice suggests /compact at a break or when you are back, so the summary comes at a "
                 "break rather than mid-task; before then, compacting saves little and the summary loses detail."
                 % (p - c, final // 1000, (trigger - final) // 1000)]
    return band, ("\n".join(lines + ["", foot]) if verbose else short)


def footer(d):
    """Stop hook: show the owner the notice without spending any tokens. A hook's systemMessage reaches the owner on
    any platform and is not added to Claude's context; only async hooks feed Claude, and this one is not async."""
    if d.get("agent_id"):
        return
    ctx, model, compacted = read_tail_usage(d.get("transcript_path") or "")
    if not ctx or compacted:
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    ready = ctx >= final and handoff_ready(d)
    print(json.dumps({"systemMessage": notice_line(ctx, window, trigger, final, ready)}))


def notice_line(ctx, window, trigger, final, ready=False):
    """The notice, on one line: the apps print "Stop says:" before every line of a hook's message and render no
    markdown (seen 2026-10-20). The size; from the note, whether the handoff is saved, with the suggestion to type
    /compact at a break or on return; then what "away" does and costs, parted by " | "; `status` explains the rest
    (the owner's requests, 2026-10-20 and 21)."""
    c, p, pct = ctx // 1000, trigger // 1000, min(ctx * 100 // max(trigger, 1), 99)
    k = costs(ctx, window)
    awake = "" if is_cloud() else ", computer awake"
    parts = ["Tokens used: %dk of %dk (%d%%)" % (c, p, pct)]
    if ctx >= final:
        parts[0] += ", compaction due in ~%dk" % (p - c) if p > c else ", compaction due now"
        parts.append(("Handoff saved: type /compact at a break or when you're back (~%s)" if ready else
                      "Handoff not saved yet: I write it, then you type /compact at a break (~%s)") % money(k["compact"]))
    parts += ['Leaving: "away" → pings until you\'re back, ~%s/h%s, cheaper than a cold start for ~%d h'
              % (money(k["hour"]), awake, k["cold_hours"]),
              'Longer: "away long" → no pings, one cold start on return (~%s)' % money(k["cold"]),
              'All explained: "status"']
    return " | ".join(parts)


def recommend():

    """`status`: everything the advice rests on at this size, formatted in markdown and explained, for Claude to
    relay in chat as printed; the notice after each reply gives one line of it."""
    path, sid = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    if not ctx:
        print("context size not found yet%s." % (" since the compaction" if compacted else ""))
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    ready = ctx >= final and handoff_ready({"cwd": os.getcwd(), "session_id": sid})
    _, reco = band_reco(ctx, window, trigger, final, verbose=True, ready=ready)
    print(reco)


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
    """Print the whole leave plan, so Claude only has to follow it. The owner leaves as soon as they send "away" (the
    owner, 2026-10-20), so the plan never has a step of theirs: Claude finishes any work first, writes the handoff when
    compaction is near, so that the owner can type /compact when back, and pings until the owner's next message, for
    at most the pings that cost one cold return, or, with "long", for an absence past that, no pings at all (the owner,
    2026-10-21). Other words after "away", such as a time, change nothing."""
    path, sid = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    pay = pings_that_pay()
    pay_hours = round(pay * PING_GAP / 60)
    if not ctx:
        print('context size not found; run "check" first. The plan is the same at any size: pings until the owner '
              "is back, at most %d (about %d hours)." % (pay, pay_hours))
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    extra = (arg or "").strip()
    long_away = extra.lower() in ("long", "longer", "days", "for days", "a long time")
    print("context: %s tokens (%d%% of %s); compaction near %s; %s"
          % (format(ctx, ","), ctx * 100 // window, format(window, ","), format(trigger, ","),
             "away long: no pings" if long_away else "away: pings"))
    print("if work is under way, or the owner left a task with this: finish it first, then run away again, which "
          "plans from the size then reached; the owner left when they sent it, so ask nothing of them and plan no "
          "step of theirs")
    if extra.lower() not in ("", "away") and not long_away:
        print('  "%s" after "away" changes nothing: the pings stop by themselves after about %d hours; an absence '
              'past that is "away long"' % (extra, pay_hours))
    if ctx >= final:
        if handoff_ready({"cwd": os.getcwd(), "session_id": sid}):
            print("handoff: saved since the note; keep it current with a small, targeted edit for anything done since, so "
                  "that it is right whenever the compaction comes, the owner's /compact or the automatic one")
        else:
            print("handoff first: compaction is near (the note is at %s), so write the handoff file "
                  "(session-notes/<topic>/handoff.md, outside the checkout) before the pings; the notice then tells "
                  "the owner it is saved and to type /compact when back. Never wait for that compaction"
                  % format(final, ","))
    if long_away:
        print("plan: no pings: the cache goes cold, and the owner's first message back pays one cold start, about %s "
              "at this size, less than pinging past about %d hours. Say so in one line, with a new session as the "
              "cheaper choice if the next task is unrelated." % (money(costs(ctx, window)["cold"]), pay_hours))
        if not is_cloud() and not os.environ.get("CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS"):
            print("  terminal: a session of 200,000 tokens or more compacts itself after about 54 idle minutes unless "
                  "CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS is set (the installer sets 600000, decision 3); say so if it "
                  "applies")
        return
    cloud = is_cloud()
    hours = (12 if long_background() else 2) if cloud else 33
    batch = min(pay, (hours * 60 - 55 + 49) // 50)
    print("plan: pings until the owner is back, at most %d (about %d hours), when they have cost what one cold start "
          "would" % (pay, pay_hours))
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
        print("  cloud: if a notice says the keep-awake command stopped before its time, the container restarted and "
              "the scheduled pings are gone too (the scheduler lists none): schedule the rest of the batch again from "
              "now, 50 minutes apart, and start the keep-awake command again; they count toward the %d" % pay)
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
