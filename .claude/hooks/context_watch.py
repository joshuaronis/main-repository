#!/usr/bin/env python3
"""Context watcher for long Claude Code sessions.

Hook modes read the hook's JSON on stdin and always exit 0, so they never block:
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
                 note. Output stays under the 10,000 characters a hook may add.
Manual mode:
  check          Run by Claude or the owner, from the working folder. Prints the
                 transcript's path, the context size, where automatic compaction
                 is expected, where the note comes, whether the hooks have run in
                 this session, and the one-line leave recommendation. Just after a
                 compaction the size is the summary's alone; the overhead comes on
                 top with the next request.
  recommend      One line: size, point and the leave recommendation (alias status).
  away <dur>     Print the ping/compact plan for an absence: 3h, 90m, 2h30m,
                 overnight (=12h), or a bare number of hours. Claude follows the
                 printout, so the per-turn thinking stays trivial.
  footer         Stop hook: emit the recommendation as a systemMessage, shown to
                 the owner after the reply and NOT added to Claude's context, so
                 it costs no tokens on any turn.

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
import sys
import time

NOTES_DIR = "session-notes"
ONE_M_MODELS = ("opus-5", "sonnet-5", "haiku-5", "fable", "mythos", "opus-4-7", "opus-4-8")
SUMMARY_RESERVE = 20_000     # held back for the summary; fits every compaction seen
AUTOCOMPACT_BUFFER = 13_000  # with the reserve, the documented ~967,000 on a 1M window
MIN_WINDOW = 100_000         # the smallest auto-compact window Claude Code takes


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


def emit(event, text):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


def watch(d):
    if d.get("agent_id"):
        return
    ctx, model, compacted = read_tail_usage(d.get("transcript_path") or "")
    p = state_path(d.get("session_id"))
    if compacted:   # the newest entry is a compaction: start the count again, say nothing
        save_state(p, {"stage": 0})
        return
    if not ctx:
        return
    window, trigger, remind, final, rearm, _ = thresholds(ctx, model)
    st = load_state(p)
    if ctx < rearm:
        st["stage"] = 0
    note = None
    if ctx >= final and st.get("stage", 0) < 2:
        st["stage"] = 2
        note = ("Context check (the owner's long-session watcher): about {:,} tokens; automatic compaction is "
                "expected near {:,}, roughly {:,} tokens away, and its summary will replace the conversation. "
                "Write the handoff file now, in either mode (session-notes/<topic>/handoff.md, outside the "
                "checkout, by the skill's Recommendations and keywords), and keep it current with one-line "
                "edits until the compaction. If the owner is following the session, also end this turn with "
                "the one line that compaction is near; working alone, carry on."
                ).format(ctx, trigger, max(trigger - ctx, 0))
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


def after_compact(d):
    if d.get("agent_id"):
        return
    dirs = []
    for x in [d.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR"), d.get("scratchpad_dir")] \
            + scratchpads(d.get("session_id")):
        if isinstance(x, str) and x and x not in dirs:
            dirs.append(x)
    notes = find_notes(dirs)
    files = notes[:8]   # the listing; the file shown is chosen from all of them
    save_state(state_path(d.get("session_id")), {"stage": 0})
    if not files:
        emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
             "No %s/ folder was found under %s; if the session kept notes elsewhere, they are the reliable "
             "record of what was decided and what remains." % (NOTES_DIR, " or ".join(dirs) or "the working folder"))
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
        else:
            advice = ("Read it first and continue from it, even if the compaction came well after it was "
                      "written; after acting on it, add a line \"Resumed <UTC time>\" at its end.")
        emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
             "The handoff, %s, follows. %s Working notes on disk, newest first: %s.\n\n%s"
             % (show(lead), advice, listing, text[:6000]))
        return
    emit("SessionStart", "Context check (the owner's long-session watcher): the conversation was just compacted. "
         "Working notes on disk, newest first: %s. The start of %s follows.\n\n%s"
         % (listing, show(lead), text[:4000]))


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


def check():
    path, sid = find_transcript()
    if not path:
        print("No Claude Code transcript found under %s." % os.path.join(config_dir(), "projects"))
        return
    ctx, model, compacted = read_tail_usage(path)
    if not ctx:
        print("transcript: %s\nNo context size found yet%s." % (path, " since the compaction" if compacted else ""))
        return
    window, trigger, remind, final, _, src = thresholds(ctx, model)
    p = state_path(sid)
    seen = os.path.exists(p) and "yes, last ran %d s ago" % (time.time() - os.path.getmtime(p)) or "not in this session"
    print("transcript: %s" % path)
    print("context: %s tokens (%d%% of a %s window)%s" % (format(ctx, ","), ctx * 100 // window,
          format(window, ","), ", just compacted (summary only; overhead comes on top)" if compacted else ""))
    print("automatic compaction expected near: %s (%s)" % (format(trigger, ","), src))
    print("note at: %s%s" % (format(final, ","), "; earlier note at: %s" % format(remind, ",") if remind else ""))
    print("watcher hooks: %s" % seen)
    _, reco = band_reco(ctx, window, trigger, final)
    print("recommendation: %s" % reco)


def one_read_pings():
    """True when a keep-warm ping costs one read of the context, so decision 4's
    limit is about 8 hours rather than 4: prompt suggestions off (the variable,
    else the user settings' promptSuggestionEnabled), and in a cloud session a
    background command allowed past 2 hours, so the keep-awake command needs no
    restart every 2 hours."""
    sugg = os.environ.get("CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION", "").strip().lower()
    off = sugg in ("false", "0", "no", "off")
    if not sugg:
        try:
            with open(os.path.join(config_dir(), "settings.json"), encoding="utf-8") as f:
                s = json.load(f)
            off = isinstance(s, dict) and s.get("promptSuggestionEnabled") is False
        except Exception:
            pass
    if not os.environ.get("CLAUDE_CODE_REMOTE"):
        return off
    try:
        long_bg = int(float(os.environ.get("BASH_MAX_TIMEOUT_MS") or 0)) > 2 * 3600 * 1000
    except ValueError:
        long_bg = False
    return off and long_bg


def band_reco(ctx, window, trigger, final, verbose=False):
    """Return (band, leave recommendation) for the current size, as prepared text
    so the decision is a lookup, not a computation. verbose gives the footer's
    several-sentence version, which the owner reads and Claude's context never
    holds; the short form is for Claude's own in-context use. The owner sends
    "away", or "away long" past the limit the text states:
      band 0  below 60% of the window: pings until back, which pay for ~33 h;
              "away long" past that: let the cache go cold (no compaction, decision 3)
      band 1  60% up to the note point: pings beat compacting for ~8 h (4 with
              two-read pings, decision 4); "away long" past that: handoff + /compact
      band 2  within the note margin of the point: handoff + /compact for any absence."""
    c, p, pct = ctx // 1000, trigger // 1000, min(ctx * 100 // max(trigger, 1), 99)
    limit = 8 if one_read_pings() else 4
    if ctx >= final:
        band, short = 2, '%dk/%dk · compaction near; leaving over 1h: "away", then /compact at this break' % (c, p)
        long = ("Long-session advisor (free; it shows after each reply). Automatic compaction is close: %dk "
                "tokens of %dk, about %d%%, and it will soon summarise this chat in place. Good moment to compact "
                "now, while you are here? Send \"wrap\": I save a handoff file with everything needed to carry on "
                "(the task, what is done, what is next), then you type /compact, so it happens at this clean "
                "break rather than mid-task. Leaving it alone for more than an hour? Send \"away\" instead: the "
                "same handoff and /compact, then I keep the smaller chat warm with pings until you are back. "
                "Otherwise just carry on: it will compact on its own, and the handoff file I keep means nothing "
                "is lost. When you are back, just write as usual." % (c, p, pct))
    elif ctx >= window * 60 // 100:
        band, short = 1, ('%dk/%dk · leaving over 1h: back within ~%dh "away" (pings); longer "away long" '
                          '(handoff, then /compact)' % (c, p, limit))
        long = ("Long-session advisor (free; it shows after each reply). Leaving this chat alone for more than "
                "an hour? At this size, keeping it warm with pings is cheaper than compacting for absences up "
                "to about %d hours. Back within that? Send \"away\" and I ping it every 50 minutes until you "
                "return. Gone longer, say overnight? Send \"away long\": I save a handoff file and ask you to "
                "type /compact before you go, since I cannot compact myself, then keep the smaller chat warm. "
                "It is at %dk tokens, about %d%% of the way to automatic compaction near %dk. Want to compact "
                "now anyway, at a clean break? Send \"wrap\": I save the handoff file so nothing is lost, then "
                "you type /compact. When you are back, just write as usual." % (limit, c, pct, p))
    else:
        band, short = 0, '%dk/%dk · leaving over 1h: "away" (pings); compacting not worth it yet' % (c, p)
        long = ("Long-session advisor (free; it shows after each reply). Leaving this chat alone for more than "
                "an hour? Send \"away\" and I keep its memory cache warm with a cheap ping every 50 minutes "
                "until you are back, so your next message is not a costly cold reload. That pays for absences "
                "up to about 33 hours; gone longer than that, say for days? Send \"away long\" and I let it go "
                "cold instead, since nothing is worth paying for that long. It is at %dk tokens, about %d%% of "
                "the way to automatic compaction near %dk; compacting is not worth it below 600k, where it "
                "saves little and the summary loses detail. When you are back, just write as usual." % (c, pct, p))
    return band, (long if verbose else short)


def footer(d):
    """Stop hook: show the owner the recommendation without spending any tokens.
    A hook's systemMessage reaches the owner on any platform and is not added to
    Claude's context; only async hooks feed Claude, and this one is not async."""
    if d.get("agent_id"):
        return
    ctx, model, compacted = read_tail_usage(d.get("transcript_path") or "")
    if not ctx or compacted:
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    _, reco = band_reco(ctx, window, trigger, final, verbose=True)
    print(json.dumps({"systemMessage": reco}))


def recommend():
    """One line for the owner's `status`/`recommend`, when the footer is not
    installed: the band's prepared recommendation, from the transcript tail."""
    path, _ = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    if not ctx:
        print("context size not found yet%s." % (" since the compaction" if compacted else ""))
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    _, reco = band_reco(ctx, window, trigger, final, verbose=True)
    print(reco)


def parse_duration(s):
    """Minutes from '3h', '90m', '2h30m', 'overnight'/'night' (=12h), or a bare
    number of hours. None when nothing usable is given (a bare 'away')."""
    s = (s or "").strip().lower()
    if not s or s == "away":
        return None
    if s in ("overnight", "night"):
        return 12 * 60
    total, found = 0, False
    for n, unit in re.findall(r"(\d+)\s*([hm]?)", s):
        n = int(n)
        total += n if unit == "m" else n * 60
        found = True
    return total if found and total > 0 else None


def ping_times(n, gap=50):
    """n UTC clock times, gap minutes apart from now, none on :00 or :30."""
    now = datetime.datetime.now(datetime.timezone.utc).replace(second=0, microsecond=0)
    out, t = [], now
    for _ in range(max(0, n)):
        t += datetime.timedelta(minutes=gap)
        show = t + datetime.timedelta(minutes=2) if t.minute in (0, 30) else t
        out.append(show.strftime("%H:%MZ"))
    return out


def away(arg):
    """Print the whole leave plan, so Claude only has to follow it. No duration is
    needed: pings run until the owner's next message, which cancels the rest, so
    only those sent while away are paid for. The owner adds "long" only when the
    absence will pass the limit the footer states; by decisions 3 and 4, below 60%
    that means letting the cache go cold, from 60% to the note a handoff and
    /compact first, and within the note's margin plain "away" already means that.
    A duration still works: it counts as long when it passes the band's limit."""
    path, _ = find_transcript()
    ctx, model, compacted = read_tail_usage(path) if path else (None, None, False)
    if not ctx:
        print('context size not found; run "check" first, then decide by decisions 3 and 4.')
        return
    window, trigger, remind, final, _, _ = thresholds(ctx, model)
    band, reco = band_reco(ctx, window, trigger, final)
    limit = 8 if one_read_pings() else 4
    a = (arg or "").strip().lower()
    if a in ("", "away", "short"):
        long_away = False
    elif a in ("long", "longer", "overnight", "night", "days"):
        long_away = True
    else:
        mins = parse_duration(a)
        long_away = bool(mins) and mins > (33 if band == 0 else limit) * 60
    print("context: %s tokens (%d%% of %s); compaction near %s; %s"
          % (format(ctx, ","), ctx * 100 // window, format(window, ","), format(trigger, ","),
             "away long" if long_away else "away"))
    if band == 0 and long_away:
        print("plan: no pings and no compaction. Past about 33 hours pings cost more than one cold return, and "
              "below 60% compacting is not worth the lost detail, so let the cache go cold (a fresh session is "
              "cheaper if the next task is unrelated). Say so in one line.")
        print("recommendation line: %s" % reco)
        return
    cloud = bool(os.environ.get("CLAUDE_CODE_REMOTE"))
    try:
        bms = int(float(os.environ.get("BASH_MAX_TIMEOUT_MS") or 0))
    except ValueError:
        bms = 0
    hours = (12 if bms > 2 * 3600 * 1000 else 2) if cloud else 33
    batch = min(40, (hours * 60 - 55 + 49) // 50)
    if band == 2 or (band == 1 and long_away):
        print("plan: handoff and /compact first, then pings at the smaller size")
        print("  1. write or refresh the handoff file (session-notes/<topic>/handoff.md) and show it as the last chat line")
        print('  2. end the reply with: "Ready: type /compact before you go."')
        print("  3. in the same turn, schedule the pings below; they keep the compacted chat warm")
    else:
        print("plan: pings until the owner is back (pinging beats %s)"
              % ("a cold return for up to about 33 hours" if band == 0
                 else "compacting at this size for up to about %d hours" % limit))
    print("pings: %d one-shot tasks, 50 minutes apart, covering the next %d hours: %s"
          % (batch, hours, ", ".join(ping_times(batch))))
    print('  each prompt: "// Keep-warm ping. Reply with only ✓."; create the whole batch in one message')
    if cloud:
        print("  cloud: also start the keep-awake background command with a %d-hour timeout; when it ends with the "
              "owner still away, restart it and schedule the next %d hours, up to 40 pings (about 33 hours) in all"
              % (hours, hours))
    else:
        print("  local: keep the computer awake while away")
    print("  on the owner's next ordinary message: cancel the pings left and stop the keep-awake command")
    print("recommendation line: %s" % reco)


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
        away(sys.argv[2] if len(sys.argv) > 2 else "")
        return
    try:
        d = json.load(sys.stdin)
        if not isinstance(d, dict):
            return
        if mode == "watch":
            watch(d)
        elif mode == "after-compact":
            after_compact(d)
        elif mode == "footer":
            footer(d)
    except Exception:
        pass


if __name__ == "__main__":
    main()
    sys.exit(0)
