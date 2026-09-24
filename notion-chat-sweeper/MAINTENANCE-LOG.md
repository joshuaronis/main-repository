# Maintenance log — Notion Chat Sweeper

Things that cost time to discover. Read this before "simplifying" anything.

## Seeded from the build spec

- **Lazy fields.** `model.data` is `undefined`; you must call
  `model.getKeyValue('data')`. Same for `alive`, `created_time`,
  `updated_time`. `id` and `table` are plain properties. This cost several
  probes to find — don't "simplify" it away.
- **The real signature** is `forEachRecordOfTable({userId, table, fn})` — one
  options object, and the callback key is `fn`, not `callback`. Read from
  Notion's minified source; re-read it if enumeration ever breaks.
- **MAIN world means no `chrome.*`.** Reaching for `chrome.storage` in
  `content.js` means you're in the wrong file — use the bridge.
- **Console logs are hard to extract.** Read `dataset.ncsLog`.
- **Hashed classes rot; the fiber walk does not.** `#sidebar-tabpanel-chats` is
  the stable DOM anchor.
- **Headers and `spaceId` verified optional — but only on no-op restores.** If
  deletes start failing while restores succeed, re-add available context first.
- **Dead threads vanish from the cache on reload.** The journal is the only
  bridge across a reload.
- **Reloading the unpacked extension does not update open tabs.** Reload the
  extension, *then* the tab.
- **`localStorage` is per-origin, not per-tab.**
- **Deleted chats never reach Notion's Trash.** Our restore path is the only
  recovery.

## Added during the build

- **The Restore tab's time column is when the chat WENT AWAY, not when it was
  last used.** These are wildly different: a chat untouched for a year can be
  deleted a minute ago. `restoreCandidates()` builds a `goneAt` map — undo-log
  run time (exact) beats journal `lastSeen` (close enough) beats the thread's
  own `updated_time` (last resort only).

  This became load-bearing when the 30-day display filter went in: sorting or
  filtering on `updated_time` would have hidden a chat *the moment you deleted
  it* if the chat itself happened to be old. Caught in the mock by deleting a
  one-year-old chat and checking it read `now`. If you touch this, re-run that
  case.

- **`restoreMaxAgeDays` HIDES, it does not delete.** The journal keeps growing to
  `journalMax`, and `Download record` still exports everything. This must never
  destroy the only record that a chat existed. `session` entries are exempt —
  they're from this session by definition. The footer says how many are hidden,
  because a list that silently shrinks looks like data loss.

- **Restoring does not bring back pinned status.** Confirmed live: a pinned chat
  that was deleted and restored came back unpinned. `alive` is the only field
  the restore writes; pinning lives somewhere else and was never part of the
  discovery. Would need fresh probing to support.

- **The poll is fingerprint-gated, and that's the whole point.** Every 4s while
  the panel is open it calls `listThreads()` only — cheap, ~45 records off the
  in-memory cache — and compares `rawSignature()` (sorted alive ids). A full
  `rescan()` runs only when that string changes, because rescan drags in
  `domThreadIds()`, which is `querySelectorAll('*')` over the sidebar plus a
  fiber walk per element. Polling *that* every 4s would be wasteful. Idle while
  a run is in flight or the panel is closed.

  `lastSig` is recorded in `readThreads()` **before** the `confirmedAlive`
  overrides are applied, so it tracks the real cache rather than our corrected
  view. Otherwise the poll would never fire while an override was in force.

- **Forget is three writes plus a suppression list, and no network call.**
  `forget()` purges the journal, purges the undo log (dropping runs left empty),
  and records the id in `ncs_forgotten`. The suppression list is the part that's
  easy to miss: a chat deleted this session is still sitting in Notion's record
  cache with `alive: false`, so purging our own records alone would not remove
  it from the list — it would reappear on the next scan as a `session`
  candidate. Verified by forgetting a session-source entry and rescanning.

  `ncs_forgotten` entries expire after `FORGET_TTL_MS` (7 days). They only need
  to outlive the current page: after a reload the record is gone from Notion's
  cache and the journal and log are already purged, so nothing can resurface.

  **Forget cannot delete anything from Notion** and must never be labelled as
  if it does. Deletion there is a soft flag and dead threads never reach the
  Trash; forgetting just discards our handle. It is, however, the only
  irreversible action in the extension — hence the blunt confirmation.

- **Shift-click lives in one place now.** `rangeClick(shiftKey, items, i,
  selSet, anchor)` is shared by both tabs, each with its own anchor object
  (`delAnchor`, `resAnchor`). The unit tests extract this function by name from
  source — if you rename it, update `test-logic.js`.

- **Restore candidates come from three sources, merged richest-first.** Cache
  (`session`) beats journal beats undo log, deduplicated by id. The cache entry
  is preferred because it still carries the real title and timestamps; the
  journal is the only one that survives a page reload; the undo log is the
  backstop for anything evicted from the journal.

- **Restore targets legitimately bypass the live-scan gate.** Hard rule 1 says
  only ids from `listThreads()` may be touched. Journal and undo-log ids came
  from `listThreads()` on an *earlier* scan — that is precisely how they were
  recorded — so `refreshRestore()` adds them back into `known`. Don't "tighten"
  this to the current scan only; it would make restore impossible, which is the
  whole point of the extension.

- **`confirmedAlive` entries expire after `CONFIRM_TTL_MS` (60s).** Restoring a
  thread the cache no longer holds means the override can never be matched
  against a record, so it would sit in the map forever. The cache normally
  agrees within about a second; a minute is a generous ceiling.

- **The run picker hides restore runs.** Every run gets an undo-log entry,
  including restores, but a restore run has nothing to undo and would show as
  "0 deleted". Filtered to runs with at least one `deleted` item.

- **THE BIG ONE: `inMemoryRecordCache` lags a confirmed write by a second or
  more.** Found at Checkpoint B on 2026-08-03, live. After a delete returns
  `200`, `getKeyValue('alive')` still reports `true` for that thread. Notion's
  own sidebar drops the row immediately, so the two disagree. The console line
  that gave it away:

  ```
  scan: cache 45 dom 44 dead 0        <- 45 alive, ZERO dead, right after a
                                         successful delete of one of them
  ```

  Symptoms if you undo the fix: deleting appears to do nothing (the chat leaves
  the sidebar but stays in the panel); deleting the same chat twice "works",
  because by the second attempt the cache has caught up; and restore looks
  *inverted* — the chat returns to Notion's sidebar but vanishes from the panel,
  since the cache still reports it dead.

  **The fix is `confirmedAlive`**, a `Map` of id → the alive value the server
  confirmed. `rescan()` applies it on top of every cache read and deletes the
  entry as soon as the cache agrees, so it is self-draining and never lies —
  a `200` is simply better evidence than a stale read. `reconcile()` then
  re-scans at 900ms and 2600ms to drain it. Watch `pending N` in the debug log:
  it should go to 0 within a few seconds of any run.

  This refines spec §1.6, which is right that dead threads keep `alive: false`
  and their titles in-session, but says nothing about *when* the flag flips.
  Never rescan straight after a write and trust the result.

- **The footer message must survive a re-render.** `render()` rebuilds the
  status line from the selection, so anything written directly to
  `status.textContent` gets wiped by the next render — including the reconcile
  rescans above, which fire up to 2.6s after a run and would erase
  "done — 1 deleted". Sticky text goes through `say()`/`statusMsg`; any handler
  that changes the selection calls `touch()` to clear it.

- **`BUILD` in content.js is bumped on every change.** The boot log prints it,
  so `installed (live) v1.0.2` in the console proves a tab actually picked up
  the new code. Reloading the extension without reloading the tab is silent
  otherwise, and it wastes a whole test round.

- **Shift-click uses a MOVING anchor — do not "fix" this back.** The anchor
  follows every click, shift-clicks included, exactly as Appendix A had it.
  So `click 3 → shift-click 9 → shift-click 6` leaves **3, 4, 5** selected.

  Spec §8 test 6 originally expected 7–9 to remain, which requires a sticky
  anchor. **That test was wrong** and the spec has been corrected. It was built
  the sticky way once and reverted on 2026-08-03. The reasoning, from Josh:
  shift-click here *toggles* a range rather than replacing it, so after
  shift-clicking row 9 your attention is at row 9, and a following shift-click
  at 6 should read as "from 9 back to 6" and trim the tail. A sticky anchor
  computes from row 3 — possibly scrolled out of view — and trimming from the
  middle would eat the front of the selection instead. Overshooting a range and
  pulling it back is the common gesture, and only the moving anchor does it in
  one click.

  The anchor is stored as a thread **id**, not an index, so it survives
  filtering and re-sorting. That part is worth keeping.
- **Styles go in via `adoptedStyleSheets`, not a `<style>` tag.** A page
  `style-src` CSP can block an injected `<style>` element; constructable
  stylesheets are pure CSSOM and can't be blocked. There's a `<style>` fallback
  if the constructor ever throws. All dynamic geometry is set through
  `el.style.foo = …`, which is also CSSOM and equally safe.
- **`threadOp` deliberately uses the captured `origFetch`**, not the wrapped
  `window.fetch`. Keeps our own requests out of the header-learning path, and
  means a later Notion re-wrap of `fetch` can't affect us.
- **`buildCtx` omits `notion-audit-log-platform` when it hasn't been seen.**
  Every other field has a specified fallback (`dataset.notionVersion`,
  `findCache()`); this one doesn't, and the spec says never guess.
- **A 1-off count mismatch is expected, not a bug.** During discovery the DOM
  walk found 42 while cache enumeration returned 41 in one run, and 42 after a
  reload. A difference of exactly 1 is the known `role: "none"` record that
  `forEachRecordOfTable` skips. Read both numbers off the banner and carry on.
  A gap **greater than 1**, or a chat visible in the sidebar that never appears
  in the panel, is worth stopping for. The banner reports the numbers either
  way and deliberately does not special-case 1 — hiding it would defeat the
  point of hard rule 8.
- **The cross-check uses two separate elements, and the colours are load-bearing.**
  `.ncs-banner` is amber and means something is wrong: a chat is visible in the
  sidebar but missing from the list. `.ncs-note` is grey and is purely
  informational: some listed rows aren't currently mounted in the sidebar,
  which is just Notion's virtualisation and happens on almost every scan.

  These started as one amber element and Josh reasonably read the routine note
  as a warning. Never colour the virtualisation note amber again — if the quiet
  case looks like the loud case, the loud case stops meaning anything.

  The grey note counts `rows.length - unrendered`, **not** `domIds.size`. The
  latter includes any sidebar row that isn't in our list at all, so when the
  amber case fires too the numbers would contradict each other.

  The DOM cross-check compares against **alive** rows only, since dead
  in-session threads are in the cache but never in the sidebar.

- **`older than N days` filters the view; it does not select.** Josh's call, and
  it's the better primitive: it composes with the title filter, lets you just
  *look* at old chats without disturbing a selection, and still selects them in
  two clicks via `+ shown`. The button is a toggle and lights up accent while
  active. Editing the number box retunes it live, but only while it's on.

- **A rescan needs visible feedback because it is synchronous.** Setting
  "scanning…" and then finishing in the same tick means the browser never
  paints it, so ↻ looked completely dead even though it was working. `flash()`
  puts the result in the status line for 1.8s instead. Any future
  fast-and-synchronous action needs the same treatment.

- **Buttons are `white-space: nowrap; flex-shrink: 0`.** The control rows are
  tight at 340px, and without this "older than" wraps to two lines as soon as
  anything beside it grows.
- **Keyboard shortcuts check `typingInPage()` first.** `/` opens Notion's own
  slash menu in its editor, so hijacking it would be a real regression.
  `preventDefault` is only ever called on a path that actually did something.
- **`Cmd/Ctrl+A` uses a `panelTouched` flag**, set by a capture-phase
  `mousedown`, rather than real DOM focus — the panel is not allowed to steal
  focus, so it can't rely on `document.activeElement` being inside it.
