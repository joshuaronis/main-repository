# Maintenance log

**Read this before debugging anything.** `README.md` says how the extension is
meant to work. This file says how it has actually failed, how we proved it, and
which tools lie to you along the way.

---

## 0. How to observe this extension at all

This is the single biggest time sink, so it goes first.

A content script runs in an **isolated world**. Its `console.info` lines appear
in DevTools, but **nothing outside the extension can read them** — not page
JavaScript, not CDP console capture, not a browser-automation harness. During
the 2026-07-25 session, "no `[NMC]` lines in the console" was mistaken for "the
script never loaded", when in fact it was loaded and working. `window.__nmc` has
the same problem: it lives on the isolated `window`, so page context cannot see
it. In DevTools you must switch the console's context dropdown from `top` to
the extension's world to reach it.

**Therefore:** under `nmc_debug=1` the extension mirrors a ring of its recent
events into the shared DOM, where anything can read them:

```js
document.documentElement.dataset.nmcLog
// "+412ms loaded || +1180ms nav → 0f42… || +9210ms page-ready ok || …"
```

That attribute is the intended debugging surface for anything driving the page
from outside. Prefer it over the console.

### Signals that are readable from page context
| Question | Check |
|---|---|
| Did it run? | `document.documentElement.dataset.nmcLog` (needs `nmc_debug=1`) |
| Is a run happening right now? | `document.getElementById('nmc-shield')` exists during a run |
| Is the page Default? | `document.querySelector('.notion-margin-discussion-item')` |
| Is the page showing icons? | `[role="button"][aria-label="N comment"]` — **see §2, this does not mean Minimal** |

---

## 0b. 2026-09-02 re-verification + the mode signal (v1.1)

Re-verified live against Notion client `23.13.20260903.0022` on scratch pages
created for the purpose (`NMC Test A/B/C`, plus an `NMC Test DB` database), not
on real content.

### Nothing was broken

Every locator and both decision paths still work **unchanged**. This is the full
pass:

| Target | Result |
|---|---|
| `topbar` `.notion-topbar` | ✅ |
| `pageContent` `.notion-page-content` | ✅ |
| `moreButton` `[aria-label="Actions"]` | ✅ |
| `moreButton` structural fallback | ✅ resolves uniquely — but see §5d |
| `overlay` (open popup inside the overlay container) | ✅ true with menu open, false after Escape |
| `inlineRow` (`[role="presentation"]` "Inline comments" → walk up ≤8) | ✅ `"Inline commentsDefault"`, 290×28 |
| `valueControl` (`[role="button"][aria-haspopup]` in that row) | ✅ text `Default`/`Minimal`, `aria-haspopup="dialog"` |
| `minimalOption` (`role="menuitem"` "Minimal") | ✅ |
| `defaultCommentPreview` `.notion-margin-discussion-item` | ✅ ×3, 308×94 |
| `minimalCommentIcon` (`aria-label="N comment"` + `svg.commentFilledSmall`) | ✅ ×3 after switching |
| Standalone page → "Customize page" in ••• | ✅ |
| Database row page → "Customize layout", no "Customize page" | ✅ → `NOT_APPLICABLE`, page untouched |
| Full end-to-end via the installed extension | ✅ **1469 ms**, trace below |

The end-to-end run, straight out of `data-nmc-log`:

```
+220085ms detect … → DEFAULT_VISIBLE (44990ms left)
+220262ms open-more:expect: resolved in 168ms
+221499ms customize-page:expect: resolved in 32ms
+221508ms open-value:expect: resolved in 8ms
+221553ms pick-minimal:expect: resolved in 39ms
+221554ms verify-minimal: resolved in 0ms
+221555ms automation finished in 1469ms
```

Note `44990ms left` at `+220085ms`: the page had been open in a hidden tab for
~216 s and the visible-time budget had not burned down at all. The hidden-tab
accounting in §10 works exactly as designed.

Also re-checked because the sibling extension (Notion AI Usage) was broken by it
the same day: **dismissed ••• menus are properly unmounted**, not parked. After
Escape, `popupCount` is 0 and `overlayVisible()` is false. The pre-flight
"overlay already open → yield" check cannot get stuck. (Notion *does* park some
popups now — it parks the workspace switcher menu — so this is worth re-testing
whenever the overlay behaviour looks odd.)

### The mode signal exists — §2 is now resolvable

`format.page_section_visibility.margin_comments` on the page block:

| Value | Means |
|---|---|
| `"inline"` | Default (expanded margin previews) |
| `"minimal"` | Minimal (count icons) |
| key absent | Default — Notion's default, never explicitly set |

Verified by flipping the setting through the UI and re-reading the record both
ways, and by checking an untouched page (no `page_section_visibility` key at
all).

It is **not in the DOM** — checked `.notion-page-content` and its ancestors for
any attribute, class or `data-*`. Nothing. So `CONFIG.locators.modeSignal` stays
empty; that hook is for a DOM signal.

It *is* reachable from the isolated world with a plain same-origin
`fetch('/api/v3/syncRecordValues')`, which is why adopting it did **not** require
a MAIN-world script or a bridge.

Bonus from the same record: `parent_table` is `"space"` for a standalone page
and `"collection"` for a database row page.

**Adopted, but only inside the probe.** Not as a general pre-check — that would
trade a harmless menu open for a network call on every commented database page.
But once the probe has already fetched the record, reading one more field is
free, and it removes a small regression the tiebreaker would otherwise have
introduced: before v1.1, a narrow window on a commented database page stopped at
`MINIMAL_ONLY` and opened nothing; with a naive tiebreaker it would have probed,
read "Default", opened the ••• menu and backed out on "Customize layout". Now
the probe returns `DATABASE` and the watch stops with `NOT_APPLICABLE` without
opening anything. The wide-window path is untouched and still uses the menu.

### What was adopted, and the shape of it

A **tiebreaker only** (§7b, `modeProbe`). The DOM keeps the question it is good
at; the record answers the one it cannot.

- DOM: *does this page have inline comments?* — count icons prove they do.
- Record: *which mode?*

Why not make the record the primary detector: it cannot answer the first
question (discussions hang off the child blocks, not the page block), and a
comment-free page reads `inline`. Acting on that would mark pages edited — for
every viewer, since this setting is shared — for nothing.

Consequences, deliberately:

- A normal Default page and a page with no comments do **zero** network.
- One request per page per session, cached and single-flight, only when count
  icons are showing.
- Probe failure (offline, non-200, unexpected shape) → verdict `UNKNOWN` →
  treated as minimal → stop. That is byte-for-byte the pre-2026-09 behaviour, so
  a broken probe can never be worse than not having one.
- `CONFIG.modeProbe.enabled = false` restores the old behaviour exactly.

### The tiebreaker, verified live

Reproduced end to end at `innerWidth: 746` on a page whose record said `inline`.
Notion's narrow-viewport fallback (§2) **still exists** on
`23.13.20260903.0022`: 0 margin previews, 3 count icons, setting untouched.

```
+4645ms detect … → COUNT_ICONS (42499ms left)
+4824ms mode probe … → DEFAULT
+4825ms detect … → COUNT_ICONS (42320ms left)
+4825ms count icons but record says Default (narrow viewport) → converting
+4873ms open-more:expect: resolved in 46ms
+6099ms customize-page:expect: resolved in 22ms
+6114ms open-value:expect: resolved in 14ms
+6148ms pick-minimal:expect: resolved in 31ms
+6148ms verify-minimal: resolved in 0ms
+6149ms automation finished in 1324ms
```

Read that trace closely, because it exercises every piece of §7b:

- `COUNT_ICONS` instead of the old `MINIMAL_ONLY` — the DOM correctly reports
  "comments exist, mode unknown" rather than guessing.
- `mode probe → DEFAULT` **179 ms** after the verdict. One request.
- The **second** `detect` line one millisecond later is the probe's
  `activeWatch.evaluate()` poke landing — the answer is acted on immediately
  instead of waiting for the next 500 ms backstop tick.
- Then the ordinary click chain, 1324 ms, and the record afterwards reads
  `minimal`.

**Before this change that page was a permanent no-op** for as long as the window
stayed narrow: the old detector returned `MINIMAL_ONLY`, the watch stopped, and
nothing ever happened. That is what §2 had been describing as acceptable.

Also confirmed by the same run: the reload really did pick up v1.1.0 (the
`COUNT_ICONS` verdict does not exist in v1.0.0), and the wide-window path still
takes the ordinary `DEFAULT_VISIBLE` route with **no network at all** — measured
separately at 1349 px, converting in 1396 ms with no `mode probe` line.

### ⚠️ Bug found in the probe itself, during its own testing

Worth recording because the failure was silent and pointed the *unsafe* way.

An unreadable or nonexistent block does **not** produce an error. It comes back
**HTTP 200** shaped:

```js
{ spaceId: "…", value: { role: "none" } }        // no id, no type, no parent_table
```

The first version of `fetchMode` walked that straight through: `v` is truthy,
`parent_table` is not `"collection"`, `margin_comments` is absent — and absence
of `margin_comments` legitimately means Default. So an unreadable record
returned **`DEFAULT`**, which is the verdict that says *go convert this page*.
Every other failure in this probe fails toward "do nothing"; this one failed
toward the only outcome that writes.

Caught by probing a nonexistent id (`00000000…`) as part of the probe's own test
matrix, not by reasoning about it. Fixed with `if (!v.id) return 'UNKNOWN'` —
positive proof we actually read a block before trusting anything about it.

Verdict matrix, verified live after the fix:

| Input | Result |
|---|---|
| standalone page, record says `minimal` | `MINIMAL` |
| standalone page, `page_section_visibility` absent | `DEFAULT` |
| database row page | `DATABASE` |
| nonexistent id (200 + `{role}`) | `UNKNOWN` ✅ was `DEFAULT` |
| malformed id | `UNKNOWN` |

**Generalisable, and the reason this is in the log:** `/api/v3/` answers "I
can't show you that" with a 200 and a stub, not a 4xx. Never infer a default
from a missing field without first confirming you read a real record.

### Still not covered

- A probe failure in the wild (offline / genuine non-200). The fallback path is
  `UNKNOWN → treat as minimal → stop`, which is the pre-2026-09 behaviour by
  construction, and the `{role}` stub case above is now covered, but a real
  network failure has not been exercised.
- The `DATABASE` short-circuit end-to-end through the running extension. The
  function was verified against the live record for all five inputs above; the
  branch that consumes it is four lines and mirrors the existing
  `NOT_APPLICABLE` handling.

---

## 1. Environment facts, measured live (2026-07-25, app.notion.com)

These are numbers, not guesses. Re-measure before trusting them again.

- **Beware: measuring page timings from OUTSIDE the page gives wrong numbers.**
  An injected probe (`javascript_tool`, CDP `Runtime.evaluate`, etc.) does not
  get scheduled while the renderer is busy booting Notion, so it reports
  everything as appearing at the moment *it* finally ran. External probes during
  this session claimed `.notion-page-content` first appeared at **8.3s, 9.1s and
  18.7s**. The extension's own in-page log for the same loads says
  `page-ready: resolved in 99ms` and `365ms`, with a `DEFAULT_VISIBLE` detection
  at **1.6s**. The in-page numbers are the true ones. An early hypothesis built
  on the external numbers ("Notion hydrates comments very late") was wrong; see
  §3.
- **A hidden tab renders nothing relevant.** `document.hidden` is true not only
  for background tabs but for a minimized window, a window fully occluded by
  another window, and a window on a non-active macOS Space. Chrome also throttles
  hidden pages hard: `requestAnimationFrame` stops, timers clamp to ~1s.
- **Window width changes what a Default page looks like.** See §2.
- **`localStorage` is per-origin, not per-tab.** Setting `nmc_off` in one Notion
  tab disables the extension in *every* Notion tab. Easy to leave set by
  accident and then debug a "broken" extension that you yourself switched off.
- **Reloading the unpacked extension orphans content scripts in open tabs.** They
  self-destruct on the next poll tick (by design, §4 of `content.js`) and the new
  code does **not** inject into already-open tabs. Always reload the extension
  *and then* the tab. A conversion that "stopped working mid-test" is usually
  this.

---

## 2. Bug: the margin count icon does not mean Minimal

> **RESOLVED 2026-09-02 — see §0b.** The ambiguity described below is still
> exactly as real, but it is no longer a dead end: the mode is now read from
> the page record when count icons are showing. Read this section for *why* the
> DOM cannot answer it, then §0b for what answers it instead.

**Symptom.** On a narrow window the extension never converts anything. No error.

**Cause.** When the viewport is too narrow to lay out the margin column, Notion
draws a **Default**-mode comment using the same small count icon it uses for
Minimal mode. Measured on one page, one setting, no reload, changing only width:

| Viewport | Setting | Rendered |
|---|---|---|
| 1440px | Default | `.notion-margin-discussion-item` (expanded preview) |
| 1150px | Default | expanded preview |
| 1100px | Default | count icon |
| 1020px | Default | `role=button aria-label="1 comment"` + `svg.commentFilledSmall` |
| 721px | Default | count icon |

Breakpoint is between **1100px and 1150px** with the sidebar collapsed, and it
moves with the sidebar. The narrow-Default icon is byte-identical to the true
Minimal icon — same `aria-label`, same svg class — so the two are
**indistinguishable from the DOM**. v1 read the icon as proof of Minimal,
stamped `DONE`, and stopped watching.

**Resolution (deliberate).** A count icon means the user is already seeing what
they wanted, whatever the setting says, so there is nothing to fix and we do
nothing. We do *not* open the menu to check the real value — that would be cost
paid for correctness about a setting the user cannot see. Self-correcting: widen
the window, the previews appear, the next visit converts. `MINIMAL_ONLY` leaves
`sessionState` **unset** because the verdict is about the window, not the page.

---

## 3. Bug (PRIMARY, confirmed): the ••• click is swallowed early in the load

**Symptom.** Open a page with a Default comment, wait forever, nothing happens.
No error, no menu flash. The user's original report.

**Cause.** Caught red-handed once `data-nmc-log` existed. Two consecutive loads:

```
+1255ms loaded
+1256ms nav → 0f42…
+1621ms page-ready ok               (resolved in 365ms)
+1621ms watch started
+1621ms detect → DEFAULT_VISIBLE
+6027ms WARN automation failed: open-more:expect(fallback): timeout after 400ms
+6028ms → FAILED
+6028ms watch stopped FAILED
```

Notion's topbar is in the DOM and passes `isVisible()` long before React has
attached handlers to it. The run therefore starts ~1.6s in, dispatches a
perfectly good click at the right element, and Notion ignores it. `expect`
(`overlayVisible`) never becomes true, the native `.click()` fallback is also
ignored, and the run throws. That result was then written as `STATUS.FAILED`,
which is in `TERMINAL` — so one swallowed click killed the page for the whole
session. Hence "no matter how long I wait."

**Ruled out along the way**, each by direct measurement:
- *The flicker shield hides the menu from the detector.* No — applying the exact
  same `.notion-overlay-container{opacity:0!important}` and clicking gave `OPEN`
  on the first 250ms sample. `opacity` does not affect `getBoundingClientRect`.
- *The locator clicked the wrong button.* No — the same click at a settled time
  works, and the side effects rule it out: clicking Share would have opened a
  dialog (which `overlayVisible` WOULD have seen), the breadcrumb would have
  navigated, Favorite would have un-starred the page. None happened.
- *The DOM drifted.* No — see §6.

**Resolution.** Three parts:
1. `settleMs` (2500) after page-ready before the first attempt.
2. A failed run is retried with backoff (`retryBackoffMs` `[1500, 4000, 9000]`,
   `maxRunAttempts` 4) instead of being written off on the first miss.
3. Only after the attempts are exhausted is a terminal `FAILED` recorded.

Worst case is ~32s of retries, which fits inside the 45s watch budget.

## 3b. Fragility (real, but NOT the original trigger): fixed sample schedule

v1 sampled the detector at page-ready +0s, +3s, +8s and then added the page to
`exhaustedThisSession` permanently. This was initially blamed for the user's
report, on the strength of external timing measurements that turned out to be
measurement artifacts (§1). With true in-page timings — comments detectable at
1.6s — the +0s sample would usually have caught them, so this was probably not
what the user was hitting.

It is still replaced, because three fixed samples with a permanent give-up is a
bad shape for a page whose render timing you do not control: it fails silently
and never retries. It is now a `MutationObserver` + 500ms backstop watch over a
45s budget that **only counts visible time**, so a page opened in a background
tab keeps its full window for when it is focused. On expiry it stops dead — no
background polling; a later comment is picked up by a reload.

---

## 4. Bug: `pageReady` timeout stamped a terminal FAILED

**Symptom.** Same as §3 — silent, permanent no-op on a page.

**Cause.** `scheduleChecks` gated on `waitFor(locateReady, 15000)`, and on
timeout wrote `STATUS.FAILED`, which is in `TERMINAL`. Given a measured 18.7s
load, one slow page load killed that page for the entire session with no retry
and no visible symptom.

**Resolution.** Timeout raised to 30s **and made non-fatal**: on timeout we log
and start the watch anyway, leaving the status unset so a reload retries.

---

## 5. Bug: `SKIPPED_BY_USER` was terminal

**Symptom.** Type a comment, and the extension never collapses it.

**Cause.** A new Default preview appears the instant you finish typing, which
fires a run *into* your keystrokes. The abort guard correctly kills the run —
and then the result was recorded as terminal, writing the page off for the
session.

**Resolution.** `SKIPPED_BY_USER` no longer sets a status; the watch continues.
Paired with a preventive gate, `userIdleMs` (1.5s since the last `isTrusted`
keydown/pointerdown), so we decline to *start* a run into someone mid-sentence
rather than starting one and aborting it.

---

## 5b. Hazard: the `moreButton` structural fallback could click the wrong thing

Not observed firing, but one position away from doing damage, so it was
tightened. The old fallback was "last visible `[role=button]` with `top < 70`".
Measured live order of that strip:

```
Lock sidebar open | Testing (breadcrumb) | Edited just now |
Share | Copy link | Comments | Favorited | Actions
```

`Actions` is last *when it is present*. If it is briefly absent during load —
exactly the window in which §3 shows this code running — the fallback would
return **Favorited** (silently un-stars the page) or, further back, the
breadcrumb (navigates away). A wrong click is worse than no click.

The fallback now additionally requires the candidate to have **no visible text**
(`Actions` is icon-only; the breadcrumb and "Edited just now" are not) and to
not match a list of known named controls. If Notion ever renames `Actions`
entirely, this fails loudly with `FAILED` rather than clicking something random.

---

## 5d. Hazard (fixed 2026-09-02): the `moreButton` KNOWN list had gone stale

§5b hardened the structural fallback by requiring the candidate to be icon-only
**and** not one of the known named top-strip controls. That safety depends
entirely on the `KNOWN` list being complete, and the 2026-09 sidebar rewrite
added labels it did not have.

Measured on a page with the sidebar open, listing what the fallback considered:

| | Candidates the fallback would accept |
|---|---|
| Old `KNOWN` | `Close sidebar`, `Inbox`, `New page`, `Actions` |
| New `KNOWN` | `Actions` |

It still picked `Actions` — but only because `Actions` happens to sit last in
DOM order, which is exactly the kind of accident §5b exists to stop relying on.
Three wrong candidates were one re-order away from being clicked, and one of
them (`Close sidebar`) is a visible state change.

Added: `close sidebar`, `open sidebar`, `expand sidebar`, `collapse sidebar`,
`inbox`, `new page`, `help`. The list is deliberately over-inclusive — a name
missing from it is a candidate we might click by mistake, while a name wrongly
in it only costs us the fallback (and the primary `[aria-label="Actions"]`
lookup is what actually runs).

**When Notion changes the topbar, re-run this check**, not just the `Actions`
lookup.

---

## 5e. Hardening (2026-09-02): `minimalOption` was document-wide

`minimalOption` scanned the whole document for a visible element whose text is
exactly "Minimal", including `[role="button"]` — while being *called* with the
overlay as a root it ignored. "Minimal" is an ordinary English word; a page
containing a button or toggle labelled that way could have been clicked instead
of the chooser item.

Never observed in the wild, and partly covered by the caller's `opt !== vc`
guard, but it violated the standing rule that every menu-item scan is scoped to
the overlay container. Now scoped, with a document-wide fallback only if the
container itself cannot be found.

---

## 5c. Bug: the Customize panel was left open after a successful run

**Symptom.** The conversion works, but the user is left looking at the ••• →
Customize page panel that the extension opened. Only reproduced on a heavy page.

**Cause.** `cleanup()` fired Escape twice, 60ms apart, and never checked. On a
66k-DOM-node page `pick-minimal` took **455ms** (vs ~40ms on a light page), so
both Escapes landed during the chooser's closing animation and were swallowed.
The Customize panel underneath survived — and `removeShield()` then ran
immediately, so the panel became fully visible.

Escape on `document.body` is the correct target; verified directly that it
closes the panel instantly when no animation is in flight. The bug was purely
fire-and-forget.

**Resolution.** `dismissOverlaysThenUnshield()`: press Escape, re-check
`overlayVisible()`, repeat up to `dismissAttempts` (6) at `dismissIntervalMs`
(220ms). The shield is held up until the overlay is actually gone so a stuck
panel is never revealed mid-dismissal, but it is **always** removed at the end of
the bounded loop, so the page can never be left dimmed. The loop also bails if
`userIsActive()`, so it never fights the user for a menu they just opened.

**Lesson (the same one as §3 and §5).** Every place this extension "does an
action and assumes it worked" eventually breaks on a slow page. `clickEl` already
had `expect`-then-verify; cleanup did not. Timings that hold on a small page can
be 10× longer on a real one.

---

## 6. Confirmed NOT problems

Worth recording so nobody re-investigates them.

- **The locators are fine.** Every one was driven by hand against the live page
  on 2026-07-25: `[aria-label="Actions"]` → `Customize page` → the
  `role="presentation"` "Inline comments" label → its
  `[role="button"][aria-haspopup="dialog"]` value control → the `role="menuitem"`
  "Minimal" option. Notion's DOM had not drifted.
- **Resolved comments do not trip the detector.** After resolving, the margin
  item and count icon both disappear; only a `discussion-id-…` span remains in
  the text, and the detector does not key on it. Correctly reads `NONE`.
- **A single synthetic click on `Actions` occasionally does not open the menu**
  right after load. `clickEl`'s `expect` + native `.click()` fallback + stale
  re-locate already cover this; do not treat one miss as a broken locator.
- **The Customize page panel now shows three rows** (Page discussions, Table of
  contents, Inline comments) — "Backlinks" is gone since the Phase 0 capture.
  Page discussions and Table of contents are `role="switch"` toggles with no
  value text; only Inline comments has a value control. The walk-up in
  `inlineRow` / `valueControl` anchors on the "Inline comments" label and stops
  at the first ancestor containing `default|minimal`, which resolves correctly.

---

## 6b. Verified working — full pass, 2026-07-26, build with settle + retry

All run against live `app.notion.com`, reading `data-nmc-log` for ground truth.

| # | Scenario | Result |
|---|---|---|
| 1 | Standalone page, Default comment, reload | **PASS** — `DEFAULT_VISIBLE` at +4391ms (2502ms after watch start = `settleMs`), `open-more` resolved in **57ms**, `DONE` at +5747ms |
| 2 | Already-Minimal page, reload | **PASS** — `MINIMAL_ONLY` → "nothing to do", no shield ever appeared, no menu opened |
| 3 | Narrow window (1000px), setting genuinely Default | **PASS** — renders count icon → `MINIMAL_ONLY`, page untouched (intended, see §2) |
| 4 | Widen to 1440px, reload | **PASS** — self-corrects: `DEFAULT_VISIBLE` → `DONE` in 5.5s |
| 5 | SPA nav away + `history.back()`, no reload | **PASS** — other page detected `NONE` and ignored; popstate caught; old watch stopped cleanly; new watch → `DONE` at +42873ms |
| 6 | Database row page ("Compact Sets…") | **PASS** — menu has *Customize layout*, no *Customize page* → `NOT_APPLICABLE`. Also confirmed the documented trap: exactly **1** "Customize layout" `role=button` exists OUTSIDE the overlay container, so the step-4 scan must stay container-scoped |
| 7 | `nmc_off=1` kill switch | **PASS** — `nmc_off=1 → onNavigate no-op`, nothing else logged |
| 8 | Hidden-tab budget pause | **PASS** — observed `detect` at +19108ms with `44999ms left`, i.e. backgrounded time did not consume the budget |
| 9 | **Heavy page** — "The Laplacian and Harmonic Functions", 66k DOM nodes / 707 blocks / 81KB text | **PASS** — converted. Content-script boot was delayed to +6201ms (vs ~1s on a light page), but `page-ready` still resolved in 843ms and `open-more` in **77ms**. Page weight delays `document_idle` — i.e. the boot — rather than click reliability, so `settleMs` scales naturally and did not need raising. Exposed §5c |
| 10 | Heavy page, no comments at all | **PASS** — sat on `detect → NONE` for the full 45s budget, then expired cleanly |
| 11 | **Heaviest page** — "08 - Differential Equations Notes 1", 71.5k DOM nodes / 1274 blocks / 105KB text | **PASS** — `open-more` 66ms, `pick-minimal` **698ms** (slowest observed), `DONE` at +15897ms, panel closed, no shield left behind |
| 12 | §5c panel-dismissal fix, re-run under the failing condition | **PASS** — `pick-minimal` took 504ms (same slow path that broke it) and `PANEL_LEFT_OPEN: 0`, vs `1` before the fix |

**Timing scaling across page weights** (why `settleMs` did not need raising):

| Page | DOM nodes | script boot | page-ready | `open-more` | `pick-minimal` |
|---|---|---|---|---|---|
| Testing (scratch) | ~4k | ~1.0s | 99–972ms | 49–57ms | 34–40ms |
| Laplacian | 66k | 6.2s | 843ms | 77ms | 455–504ms |
| Diff-Eq Notes 1 | 71.5k | ~11s | ~1s | 66ms | 698ms |

Page weight inflates the **content-script boot** (`document_idle` waits for the
page) and the **menu interactions**, but not the ••• click itself. So `settleMs`
is measured from page-ready, which already arrives late on a heavy page — it
scales for free. What *did* need to scale was anything with a fixed short
deadline, which is exactly what §5c was.

The decisive before/after on the primary bug, same click and same locator:

```
before:  +6027ms open-more:expect(fallback): timeout after 400ms  → FAILED (terminal)
after:   +4451ms open-more:expect: resolved in 57ms               → DONE
```

## 7. Open / unverified

- **Phase 0 F — no mode signal found.** There is still no
  comment-position-independent attribute that reveals the mode. If one is ever
  found, `modeSignal` + `readModeFromSignal()` supersede the whole §2 mess.
- **Phase 0 G — page-level discussions.** Never captured with a live page-level
  comment. `.notion-margin-discussion-item` is margin-specific so page
  discussions *should not* match, but this is unproven. If a page whose only
  comments are page-level ever triggers a run, start here.
- **Database row pages — menu shape verified (§6b #6), end-to-end run not.**
  Confirmed the menu presents *Customize layout* and no *Customize page*, which
  is what drives the back-out. Not verified by actually putting a Default inline
  comment on a database row and watching a real run reach `NOT_APPLICABLE`,
  because that meant editing a real page rather than the scratch one.
- **Long virtualized pages** where every comment is scrolled off-screen still
  read `NONE`. Known and accepted.
