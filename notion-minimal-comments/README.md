# Notion Minimal Comments

A Manifest V3 Chrome extension (loaded unpacked) that automatically sets
**Inline comments → Minimal** on standalone Notion pages in the web app at
`https://www.notion.so`, silently. It drives the same synthetic clicks a human
would — no background worker, no storage, and nothing is ever *written* through
Notion's API. It makes one read-only API call, in one ambiguous case; see
**Network** below.

> **⚠️ Reload the extension once.** The copy running in Chrome is v1.1.0 as of
> the live test, but two later commits (the unreadable-record guard and the
> `DATABASE` short-circuit) are on disk only. `chrome://extensions` → Reload ↻,
> then reload any open Notion tab. Nothing is broken until you do — the running
> version was verified end to end — these are a safety fix and an optimisation.
>
> **Status: verified live 2026-09-02** against Notion client
> `23.13.20260903.0022`. Every locator and both decision paths still work
> unchanged — see `MAINTENANCE-LOG.md` §0b for the full re-verification.
>
> **The mode signal was found (2026-09-02).** The setting this extension is
> about is stored on the page record at
> `format.page_section_visibility.margin_comments` (`"inline"` = Default,
> `"minimal"` = Minimal, absent = Default). It is *not* in the DOM, but it is
> readable from the isolated world with one read-only same-origin `fetch`.
> It is now used as a **tiebreaker** — see "The count icon is ambiguous" below.
> `CONFIG.locators.modeSignal` stays empty: that hook is for a *DOM* signal,
> and there still isn't one.
>
> Still a known no-op: a long virtualized page with every comment off-screen.
> The DOM is still what decides whether a page has comments at all.

## Install (load unpacked)
1. Open `chrome://extensions`.
2. Enable **Developer mode** (top right).
3. Click **Load unpacked** and select this folder.
4. **Reload any already-open Notion tab once** — content scripts do not inject
   into tabs that were open before the extension loaded.

Keep the folder at a stable path. If you move or rename it, Chrome disables the
extension and you must re-load it.

## Dev loop
After editing files: click the **reload icon** on the extension card in
`chrome://extensions`, then **reload the Notion tab** (open tabs keep running
the old script until reloaded). Check the card's **Errors** button if something
looks off. The old (orphaned) script self-destructs on its next poll tick
(~400ms) via the guarded `chrome.runtime?.id` check, so you should not see
`Extension context invalidated` spam.

## Scope
`https://app.notion.com/*` (the current Notion web app) and legacy
`https://www.notion.so/*`. **Not** the desktop/mobile apps, **not** published
`notion.site` pages, **not** custom domains.

## What it does / does not touch
- **Standalone pages** (not in a database): inline-comment mode is per page, so
  this is the only case the extension acts on. When a Default-mode signal (or a
  visible Default preview) is detected, it opens `•••`, sets Inline comments to
  Minimal, and verifies the change.
- **Database row pages**: governed by the database layout ("Customize layout" /
  "Apply to all pages"), which Notion sets for the whole database. The extension
  detects "Customize layout" as the back-out signal and marks the page
  `NOT_APPLICABLE` without modifying it.

## Shared-setting caveat
The change is stored on the page: it marks the page **edited** and applies for
**all viewers and devices**, not just you. Accepted by design.

## Network

One request, in one situation: when a page shows margin **count icons**, the
extension asks `POST /api/v3/syncRecordValues` (read-only, same-origin, your own
session) which mode the page is actually in. That is the only ambiguous case in
the whole design — see below. A normal Default page and a page with no comments
do no network at all. Nothing is ever written through the API; every change is
still made by clicking Notion's own controls.

The same response also says whether the page is a database row, so in that one
case the extension can back out with `NOT_APPLICABLE` without opening the •••
menu at all.

If the request fails, or comes back for a page it cannot read, the verdict is
`UNKNOWN` and the extension stops — the same thing it did before this existed.

Turn it off with `CONFIG.modeProbe.enabled = false`; the extension then behaves
exactly as it did before 2026-09-02.

## Flags (set in DevTools console, per Notion tab)
- `localStorage.setItem('nmc_off','1')` — kill switch. `onNavigate` becomes a
  no-op; nothing happens until you remove the flag. (Works in all modes.)
- `localStorage.setItem('nmc_debug','1')` — verbose step-level logging, detector
  results per scheduled check, and menu-item texts on a step-3 miss. Also
  exposes `window.__nmc` (debug only):
  - `window.__nmc.state()` — session state snapshot.
  - `window.__nmc.detect()` — run the detector now.
  - `window.__nmc.runNow()` — clear this page's status and re-evaluate.
  - `window.__nmc.config` — the live CONFIG.
  - `window.__nmc.mode()` — ask the page record what the inline-comment mode
    really is, bypassing the cache. Returns a promise resolving to
    `'DEFAULT' | 'MINIMAL' | 'UNKNOWN'`.
  - `window.__nmc.modeCache()` — what the tiebreaker has resolved this session.
  - `state()` also reports `watching` (the pageId of the live watch, or `null`)
    and `hidden` (whether the tab is currently backgrounded — a hidden tab is
    watched but never acted on).
- Remove a flag with `localStorage.removeItem('nmc_off')` (or `nmc_debug`).

All logs are prefixed `[NMC]`. Normal mode logs only `pageId → STATUS`
transitions.

## Peek / side previews
Peek previews put the page id in the URL **query** (`?p=<id>`), not the path.
The extension extracts the id from `location.pathname` only, so peeks never
trigger a run. (No peek handling in v1.)

## Manual acceptance tests
The sandbox can't drive a logged-in Notion; validate these yourself after
filling Phase 0. All should pass:

1. Standalone page, Default-visible comment → within ~2s comments collapse to
   margin icons; brief shielded blink at most; "Edited just now" shows.
2. Reopen it → nothing happens; no menu opens.
3. Standalone page, no comments → nothing ever happens (verify in debug logs).
4. Database item page, Default comments → menu opens once, finds "Customize
   layout" → `NOT_APPLICABLE`; page unmodified.
5. Fast A→B→C nav across commented pages → no errors, no stuck overlays.
6. Type immediately after opening a commented page → run aborts
   (`SKIPPED_BY_USER`); all keystrokes land; no menu left open.
7. Commented page in a background tab, focus later → conversion on focus, not
   before.
8. Open a peek/side-preview of a Default-comment page → no run fires.
9. `nmc_debug=1`: step logs appear. Break one locator (edit CONFIG to nonsense)
   → graceful `FAILED`, overlays closed, no retry loop, page usable.
10. `nmc_off=1`: nothing happens until the flag is removed.
11. Reload the unpacked extension while a Notion tab is open, keep using that
    tab without reloading → no `Extension context invalidated` spam; orphaned
    script self-destructs within one poll tick; after reloading the tab it works.
12. Direct-row vs Customize-page: verify step 4's adaptive path on whichever
    variant your Notion shows (both if possible).

## Debugging from outside the extension
Content-script logs live in an **isolated world** — page JavaScript, CDP console
capture and automation harnesses cannot read them, so an absent `[NMC] loaded`
proves nothing. Under `nmc_debug=1` the extension therefore mirrors its recent
events into the shared DOM:

```js
document.documentElement.dataset.nmcLog
// "+412ms loaded || +1180ms nav → 0f42… || +9210ms page-ready ok || …"
```

Read that instead of the console. See `MAINTENANCE-LOG.md` §0 for the rest of
the traps (they cost a whole session once).

## Maintenance playbook (Notion's DOM changes)
Notion ships DOM changes that break class selectors. When it stops working,
re-run the Phase 0 snippets (`ground-truth/PHASE-0-CAPTURE.md`), diff against
your saved captures, and update the relevant `CONFIG.locators` / `matchers`.

**Before anything else:** set `nmc_debug=1`, reload, and read
`document.documentElement.dataset.nmcLog`. It tells you which step died. Nearly
every "it does nothing" turns out to be a recorded, specific failure.

| Symptom | Suspect |
|---|---|
| `open-more: expect timeout` in the log | Click swallowed pre-hydration — raise `settleMs`. Not a locator problem |
| Log stops after `detect → NONE` repeatedly | Detector; check whether the window is narrow (count icon ≠ Minimal) |
| No `data-nmc-log` attribute at all | `nmc_debug` unset, or the content script really did not inject (reload extension **then** tab) |
| Nothing happens on any page | `moreButton` / `topbar`, or the nav-watcher. First rule out timing: with `nmc_debug=1` you should see a `detect … → NONE/DEFAULT_VISIBLE` line every ~500ms. If you see no `[NMC] loaded` at all, the content script never injected (reload the unpacked extension, then the tab) |
| Menu opens then FAILED at step 3 | `inlineRow` / `customizePage` |
| Page reverts to Default / wrong result | `valueControl` / `minimalOption`, or the detector locators |
| Acts on pages it shouldn't | Detector too broad — check `modeSignal` / preview scoping and the inline-vs-discussion distinction (Phase 0 G) |

Keep ≥2 strategies per locator; the last should be structural (role/position),
not a bare class.

## Architecture notes / deliberate non-choices
- **Content-script-only.** One `setInterval` set up at document load survives
  all in-app SPA navigations — no re-injection, no `webNavigation`, no service
  worker.
- **No `history.pushState` patch** — the isolated world's `pushState` is a
  different function than the page's, so a patch never fires. Navigation is
  detected by polling `location.href` + `popstate`.
- **No HTML-string sinks** (`innerHTML` / `insertAdjacentHTML` / `document.write`
  / injected `<script>`), so we stay safe under Trusted Types. Every node is
  built with `createElement` + `textContent` + `appendChild`.
- **`all_frames` off** — Notion's editor/topbar/comments live in the top
  document; iframes are only external embeds we don't touch.
- **No persistence** — the setting can change from another device, so a stored
  "DONE" could wrongly skip a reverted page. The DOM pre-check is recomputed each
  session.
- **Settle, then retry with backoff (changed 2026-07-25).** *This was the actual
  bug.* Notion's topbar is in the DOM and passes `isVisible()` well before React
  has attached handlers to it, so a run starting ~1.6s into a load dispatches a
  perfectly good click at the ••• button and Notion simply ignores it. v1 then
  recorded that as `FAILED`, which is **terminal** — one swallowed click killed
  the page for the whole session. Caught verbatim in `data-nmc-log`:

  ```
  +1621ms detect → DEFAULT_VISIBLE
  +6027ms WARN automation failed: open-more:expect(fallback): timeout after 400ms
  +6028ms → FAILED   +6028ms watch stopped
  ```

  Now: `settleMs` (2.5s) before the first attempt, and a failed run is retried
  (`retryBackoffMs` `[1500, 4000, 9000]`, `maxRunAttempts` 4) before any terminal
  `FAILED` is recorded. See `MAINTENANCE-LOG.md` §3, including what was ruled
  out (it is not the flicker shield and not a stale locator).
- **Continuous watch, not fixed samples (changed 2026-07-25).** v1 sampled the
  detector at page-ready +0s/+3s/+8s and then marked the page `exhausted` for the
  session — silent, permanent, no retry. Replaced with a `MutationObserver` +
  500ms backstop watch over a **45s budget that only counts visible time**, so a
  page opened in a background tab keeps its full window for when you focus it;
  `visibilitychange → visible` also re-arms a watch on a page with no verdict
  yet. On expiry it **stops dead** — no background polling. Add a comment much
  later, and a reload picks it up.
  (Honest note: this shape is bad regardless, but it was probably *not* what you
  were hitting — see `MAINTENANCE-LOG.md` §1 and §3b for why the timings that
  implicated it were measurement artifacts.)
- **`SKIPPED_BY_USER` is no longer terminal (changed 2026-07-25).** It is not a
  verdict about the page — it means we picked a bad moment. Recording it as
  terminal produced the same silent failure as the sampling bug: you type a
  comment, the new Default preview immediately fires a run *into* your
  keystrokes, the abort guard kills it, and the page is written off for the rest
  of the session. The watch now continues instead. Paired with a preventive
  check — `userIdleMs` (1.5s) since the last `isTrusted` keydown/pointerdown —
  so we decline to start a run into someone mid-sentence rather than starting
  one and aborting it.
- **The margin count icon does not mean Minimal (found 2026-07-25).** This was
  the second silent no-op, and the worse of the two. Notion falls back to the
  *same* margin count icon for a **Default**-mode page whenever the viewport is
  too narrow to lay out the margin column. Measured on one page, one setting, no
  reload, changing only window width:

  | Viewport | Inline comments setting | Rendered |
  |---|---|---|
  | 1440px | Default | `.notion-margin-discussion-item` (expanded preview) |
  | 1020px | Default | `role=button aria-label="1 comment"` + `svg.commentFilledSmall` |

  The flip is between 1100px and 1150px with the sidebar collapsed, and moves
  with the sidebar. The narrow-Default icon is byte-identical to the true
  Minimal icon — same `aria-label`, same svg class — so **no DOM inspection can
  separate them.** Only the Customize page panel knows the truth.

  **Resolved 2026-09-02 — we now ask the record, not the DOM.** The last line
  of the original note said "if `modeSignal` is ever found, it supersedes all of
  this". It was found, so this is what happens now:

  - the DOM still decides **"does this page have inline comments?"** — count
    icons prove they exist;
  - the page record decides **"which mode?"** —
    `format.page_section_visibility.margin_comments`.

  So a count icon no longer ends the story. If the record says `minimal`, we
  stop, as before. If it says `inline`, the page really is in Default and only
  *looks* converted because the window is narrow — so we convert it for real.

  The split matters: the record cannot tell us whether a page has comments
  (discussions hang off the child blocks, not the page block), and using it as
  the primary trigger would make the extension write to comment-free pages —
  marking them edited, for every viewer, for nothing.

  If the probe fails for any reason — offline, non-200, unexpected shape — the
  verdict falls back to "treat as minimal and stop", which is exactly the old
  behaviour. A broken probe cannot make this worse than not having one.

  Either way the watch stops with `sessionState` left **unset**, because the
  verdict is about the current window rather than the page, so re-navigating
  re-evaluates.

  *Still rejected:* gating the icon on a viewport-width constant. The breakpoint
  is a Notion internal that shifts with sidebar state; the record is the actual
  answer.
- **The mode probe is a tiebreaker, not the detector (added 2026-09-02).** See
  the count-icon note above for why the DOM keeps the "are there comments?"
  question. Consequences worth keeping: the common paths still do no network,
  a comment-free page is still never touched, and `CONFIG.modeProbe.enabled =
  false` restores the pre-2026-09 behaviour exactly.
- **No MAIN-world script, still.** The mode lives in the page record, which the
  field guide reaches through React fibers from the MAIN world — but the same
  value comes back from a same-origin `fetch` that works fine in the isolated
  world. That kept the single-file, no-bridge architecture intact.
- **Documented upgrade path (not built):** a `world:"MAIN"` history-patch relay
  for instant SPA-nav detection, if polling latency ever matters.
