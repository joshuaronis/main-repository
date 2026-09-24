# Maintenance log — Notion AI Usage

Originally verified live on **2026-08-04** against Notion client
`23.13.20260804.1857`. Re-verified and repaired on **2026-09-02** against
`23.13.20260903.0022` — Chrome, macOS, Josh's real logged-in workspace
(Business plan, 1 member).

Everything below was measured, not inferred. Where something is unverified it
says so.

---

## 0. 2026-09-02 — v1.0.0 broke; what changed (v1.1.0)

Symptom: the shortcut did nothing at all.

Two independent regressions, both in Notion, both in the same area. The first
is what Josh noticed; the second was found while fixing the first and would
have bitten later.

### 0.1 The workspace switcher moved to the *bottom* of the sidebar

v1.0.0's `workspaceSwitcher()` required `getBoundingClientRect().top < 200`,
because the switcher used to sit at the top of the sidebar. In
`23.13.20260903.0022` the top of the sidebar is search / inbox / new-page, and
the switcher is the **last** row (measured `top 770, left 8, 194×28` on an
805px viewport). The filter matched nothing, `waitFor` timed out at
`workspace-switcher`, and every rung of the retry ladder failed identically.

Everything downstream was untouched and still passes: the "Settings" row,
`#settings-tab-ai`, and the `General / Usage / AI connectors / Agents /
Meeting notes / Skills` sub-tab row.

**Fix.** `workspaceSwitchers()` (now plural) ranks candidates and never looks
at position:

1. `.notion-sidebar-switcher` — a real semantic class, unique document-wide,
   same family as `.notion-sidebar-container`. This is the one that hits.
2. Structural: a wide, unlabelled `[role="button"][aria-haspopup="dialog"]`
   inside the sidebar that is not in the page tree.

`openSettings()` then decides **by outcome**: it clicks a candidate, and keeps
it only if a "Settings" row actually appears; otherwise it dismisses and tries
the next. That is the part that survives the next rename, and it is why the
ambiguity in strategy 2 is tolerable — on the live app exactly two elements fit
that description, the switcher (194×28) and the recents "More" row (254×30).

**Do not reintroduce a coordinate test here.** It is what broke.

### 0.2 Dismissed popups are now PARKED, not unmounted

§6 of this log used to record "idle overlay contains no stray 'Settings' ✅
empty — the fast path above can't misfire". **That is no longer true**, and the
`openSettings()` fast path leaned on it.

When the workspace popup is dismissed *by clicking "Settings"*, Notion keeps it
mounted and hides it with a CSS property that still leaves every row a real
layout box. Measured on the parked "Settings" row:

| Signal | Parked | Genuinely open |
|---|---|---|
| `getBoundingClientRect()` | **273×27** | 284×28 |
| `offsetParent === null` | false | false |
| overlay `textContent` | 207 chars | 207 chars |
| `checkVisibility({checkOpacity, checkVisibilityCSS})` | false | true |
| `elementFromPoint` at its centre hits it | false | true |
| **trigger's `aria-expanded`** | **`"false"`** | **`"true"`** |

So the old rect-only `visible()` reported a closed menu as open, and
`settingsMenuItem()` returned a stale row. It *happened to still work* —
clicking the parked row opened settings anyway, in 2.6 s instead of a warm
~0.7 s — which is the worst outcome available: a silent dependency on a menu
Notion no longer considers open, one release away from a 40-second silent
failure through the whole retry ladder.

**Fix: `aria-expanded` on the trigger, via `expanded()`.** Every "is the
Settings row on screen?" question is now gated on it, both in the fast path and
in the per-candidate `waitFor`. `visible()` is left exactly as it was.

#### ⚠️ `checkVisibility()` was tried first and is WRONG here — don't re-adopt it

The table above makes `Element.checkVisibility({checkOpacity: true})` look like
the obvious fix, and it *was* the first fix. It shipped for about twenty
minutes. It is a trap:

**Notion's popups animate in from `opacity: 0`, and CSS animations do not
advance in a hidden tab.** In a tab with `document.visibilityState === "hidden"`
the opacity of a *genuinely open* menu stays 0 forever. Measured: menu open,
`aria-expanded="true"`, all ten rows laid out at real on-screen coordinates,
`checkVisibility({checkOpacity: true})` **false on every one of them**. The
animated ancestor sat at `opacity: 0, transform: matrix(0.96, …)` indefinitely.

That is not hypothetical for this extension. `background.js` activates the
target tab, but `chrome.windows.update({focused: true})` is in a `try/catch` and
does not always win on macOS — and the same code path runs against tabs in other
windows. A locator that only works in the foreground tab is a locator that fails
exactly when Josh is doing something else.

`checkOpacity: false` doesn't rescue it either: that stops distinguishing parked
from open at all, since parking is not a `display`/`visibility` change.

`aria-expanded` has neither problem — it is semantic, Notion maintains it
correctly in both states, and an attribute cannot be stuck mid-animation.

### 0.3 A collapsed sidebar now works

Not a regression — a capability v1.0.0 never had. With the sidebar collapsed the
switcher is parked **off-screen** (`left: -242`) rather than unmounted, and it
keeps a real 194×28 box. A synthetic click on it opens the popup normally
(verified). So `workspaceSwitchers()` deliberately does **not** require
`visible()` for its primary match, and the extension no longer needs to expand
a sidebar the user chose to close.

Note the asymmetry with 0.2, which is the whole trick: *off-screen* is still
visible to `checkVisibility()`; *parked* is not.

---

## 1. The architecture decision

Josh asked for either (a) a shortcut that opens Settings → Notion AI → Usage,
or (b) a panel that shows the usage numbers directly, and said to pick the
simpler one, preferring (b) on a tie.

**Chose (a).** Not a tie, and not close.

The deciding fact: **the Rolling and Monthly percentages have no data source
reachable outside the rendered settings panel.** The search below was
exhaustive enough that it should not be repeated without new information.

### Where the allowance numbers are NOT

| Probed | Result |
|---|---|
| Record cache (`space`, `user_settings`, `space_user`, `user_root`, `notion_user`) | No usage fields. `space` has `sharded_entitlement_usage_tables` and `ai_credit_overage_policy` — flags, not numbers. |
| Every `/api/v3/` response captured while the Usage tab rendered (31 calls, fetch-wrapped) | None contained `percentUsed`, `resetsInMs`, "rolling", or "reset". |
| Full network log across a cold load + the whole settings flow | 18 `/api/v3/` calls, same answer. |
| Response headers on `/api/v3/` calls | No rate-limit headers of any kind. |
| React hook state / query cache above the bars | No query key, no cached payload. |
| All 758 loaded JS bundles (39 MB) grepped for endpoint names | Endpoint names are **built as `` `/api/v3/${name}` ``**, so they do not appear as literals — `getAIUsageEligibilityV2` itself is not a literal anywhere. Endpoint-name greps are useless here; don't retry that approach. |
| Direct probes of 12 guessed endpoints | All 404 or unrelated. See §3. |

### Where they ARE

Only as React props on the rendered component, shape:

```js
{ percentUsed: 70.72,
  resetsInMs: 21011289,
  monthlyUsage: { percentUsed: 22.54, periodEndMs: 1787091712000 } }
```

Sibling identifiers in the same bundle chunk — `limit`, `window`,
`retryAfterSeconds`, `within_limit`, `rate_limited`, `not_applicable`,
`billing_period` — say this is a **rate-limit status object**, most likely
delivered alongside AI inference rather than by a settings-specific endpoint.
That is a hypothesis, not a finding.

Reading props requires the settings panel to be open, which defeats a
standalone panel entirely. Hence (a).

---

## 2. Endpoints found (all read-only, all verified 200)

Useful orientation for a future extension, none of them used by this one.

```
getAIUsageEligibilityV2   {spaceId} → credits: usage.totalCreditBalance,
                          limits.purchased.totalLimit, premiumCredits.perSource.*,
                          basicCredits.*, usage.currentServicePeriod / .lifetime
getAIUsageEligibility     {spaceId} → older/flatter: spaceUsage, spaceLimit,
                          userUsage, userLimit, type:"unlimited"
getAIUsageDashboardServicePeriods
                          {spaceId} → {periods:[{start,end,displayEnd}]}
                          Its last `end` equals monthlyUsage.periodEndMs exactly.
getSpaceUsageSettings     {spaceId} → {type:"self_serve"}
getSubscriptionEntitlements {spaceId} → {editsBlocked:false}
getSubscriptionData       {spaceId} → plan/tier/Stripe summary
getAvailableModels        {spaceId} → model roster
```

> ⚠️ **Credits ≠ allowance.** The Usage panel says so itself: "Products that use
> credits like Custom Agents and Workers don't count toward this allowance."
> At the time of measurement credits read 2/300 used (0.67%) while the monthly
> allowance bar read 23%. Wiring `getAIUsageEligibilityV2` into a panel and
> labelling it "usage" would be confidently wrong.

**There is no URL route for settings.** Opening the modal leaves
`location.href` untouched, so a deep link is not an option. Confirmed twice.

---

## 3. Endpoints probed and absent (404)

Save someone the round trip:

```
getAIRateLimitStatus  getAIUsageRateLimit  getPlanUsage  getAIPlanUsage
getAIUsageStatus      getAIUsage           getUserAIUsage  getAIUsageLimits
```

`getAIDailyCreditUsage` exists but 400s on both `{spaceId}` and `{}` — it wants
arguments that were not derived.

---

## 4. Locators, as verified

| Target | Primary | Fallback |
|---|---|---|
| Settings modal | `[role="dialog"][aria-label="Settings & members"]` | any `[role="dialog"][aria-modal="true"]` containing `[id^="settings-tab-"]` |
| Workspace switcher | `.notion-sidebar-switcher` (semantic class, unique document-wide) | wide, unlabelled `[role="button"][aria-haspopup="dialog"]` in the sidebar, not under `[class*="notion-outliner"]` — then verified by outcome. **No position test**; see §0.1 |
| "Settings" row | text match inside `.notion-overlay-container` | — |
| Notion AI section | `#settings-tab-ai` / `[data-testid="settings-tab-ai"]` | `[role="tab"]` with text `Notion AI` |
| Usage sub-tab | `[role="tab"]` with text `Usage`, excluding ids matching `^settings-tab-` | second tab of the largest id-less tab group |
| Close | `[aria-label="Close"]` inside the dialog | Escape keydown |
| "Is the workspace menu open?" | `aria-expanded === "true"` on the trigger | — **not** rect visibility, **not** `overlay.textContent`, **not** `checkVisibility`; see §0.2 |

**The left-nav / sub-tab discriminator is the useful trick here.** Both rows are
`role="tab"`. The settings left nav carries real ids (`settings-tab-settings`,
`settings-tab-ai`, `settings-tab-billing`, …) and the AI sub-tabs carry none —
which is also why `#settings-tab-ai` is safe to use and language-independent,
unlike everything else in this table.

Success is asserted on `aria-selected === "true"`, not on scraping "% used".
Also language-independent, and it doesn't break when usage reads "No usage"
(that string exists in the bundle as `planUsageNoUsage`).

---

## 5. The bug the live test caught

`settingsMenuItem()` originally required a `[role="menu"]` ancestor:

```js
ov.querySelectorAll('[role="menu"] [role="button"], …')   // WRONG
```

It timed out on a real run **with the workspace menu visibly open on screen** —
the exact silent no-op this codebase's field guide warns about.

Cause: the workspace popup renders its rows inside a
`[role="dialog"][aria-modal="true"]`, not inside the `[role="menu"]` that also
exists in the overlay. Both are present, and which one holds the rows varied
between renders during probing.

Fix: scope to `.notion-overlay-container` and nothing more. That scoping is the
whole of the field guide's rule (5.2) — it exists to exclude the sidebar's
always-visible `role="menu"`, which sits *outside* the overlay. Requiring a
`role="menu"` ancestor on top of it is over-tightening. **Don't put it back.**

This is worth generalising: in Notion's overlay, *popup type is not stable* —
`menu`, `dialog` and `listbox` are interchangeable across renders of the same
control. Match on the container, the role of the **item**, and its text.

---

## 6. Test results

Run against the live workspace by evaluating the shipped source (sliced out of
`content.js`, not retyped — field guide 9.4).

| Case | Result |
|---|---|
| Cold: nothing open, warm page | ✅ 715 ms, no retries |
| Settings already open on **General** | ✅ 1010 ms → AI/Usage, bars rendered |
| Second press while on AI/Usage (toggle) | ✅ close button found, dialog gone |
| Immediately after a page reload | ✅ 3951 ms, first attempt, no retry needed |
| Workspace popup already open (§7 recovery) | ✅ 999 ms, skipped the switcher click as intended |
| Idle overlay contains no stray "Settings" | ✅ 2026-08 — ❌ **NO LONGER TRUE**, see §0.2 |
| Constructable stylesheet under Notion's CSP | ✅ applied, not blocked |
| Toast intercepting clicks | ✅ `elementFromPoint` at its centre returns the page, not the toast |
| Toast stealing focus | ✅ `document.activeElement` unchanged |
| DOM log mirror | ✅ `document.documentElement.dataset.nauLog` readable |

**Trusted Types is enforced** on `app.notion.com` — confirmed, not assumed
(`window.trustedTypes.defaultPolicy !== undefined`). Every node here is built
with `createElement` + `textContent`.

### 2026-09-02 re-test (v1.1.0)

Run against the live workspace by evaluating the **shipped** source — sliced out
of `content.js`, mechanically (only the `chrome.*` wiring swapped for a
`window.__nauRun` handle), then hash-compared function-by-function against the
file to prove the code under test *was* the code that ships. Field guide 9.4.

The hash step earned itself twice over: it caught two functions that differed
from the file (comments only, that time) and it is the only reason the
`checkVisibility` reversal in §0.2 could be re-tested with any confidence.

| Case | Result |
|---|---|
| Cold, **sidebar collapsed**, nothing open | ✅ 4.0 s, first attempt, no retries — a case v1.0.0 could not do at all |
| Cold, full flow, **tab hidden** (`visibilityState: "hidden"`) | ✅ 4.0 s, `try switcher` → `ok attempt=0` — the case that killed the `checkVisibility` design |
| Warm, settings already open on another section | ✅ 0.7 s, straight to AI/Usage |
| Second press while on AI/Usage (toggle) | ✅ close button found, dialog gone |
| Re-open **while the popup is parked** (§0.2) | ✅ `settingsMenuItem()` did find the stale row by rect (`staleRowByRect: true`), `aria-expanded` was `"false"`, the fast path was correctly skipped, `ok attempt=0`. This is the regression test for §0.2 — keep it. |
| `workspaceSwitchers()` ranking, sidebar collapsed | ✅ 1 candidate, the semantic-class match |
| `workspaceSwitchers()` ranking, sidebar open | ✅ switcher first; recents "More" and "Trash" are picked up by the structural fallback but never reached |
| Switcher position across two page loads | ⚠️ `top 770, 194×28` on one load, `top 65, 254×32` on the next — **it is not even stable between reloads.** Conclusive argument against any coordinate test |
| Synthetic ⌘, as a shortcut to Settings | ❌ **does nothing** — not bound, or `isTrusted`-gated. Not usable from a content script; don't re-probe it |
| **Real end-to-end: extension reloaded, tab reloaded, ⌘⇧U pressed** | ✅ Usage panel opened. Confirmed by Josh — this covers `background.js`, the command registration and the ping/retry handshake, which the harness cannot reach |

One caveat worth recording: driving three full flows inside a single
`Runtime.evaluate` stalled the renderer and left the settings dialog frozen
mid-fade. Nothing to do with the extension — but if you are testing this way,
one flow per evaluation with a settle delay between them.

### Not covered by these tests

- The `chrome.*` layer beyond the happy path: tab resolution when no Notion tab
  is open, the badge, and the popup's error display. `commands.onCommand` and the
  ping/retry handshake *are* now confirmed by the real ⌘⇧U run above.
- The retry ladder still never fired: every 2026-09 run succeeded on
  `attempt=0`. Its behaviour under a genuinely swallowed click remains
  unexercised. The new per-candidate loop inside `openSettings()` *was*
  exercised, but only ever on its first candidate — the fallback rungs of
  `workspaceSwitchers()` have never actually been clicked on a live app.
- One workspace, one plan, one language, one viewport.

---

## 7. Deliberate choices, so they don't get "fixed"

- **Isolated world, no `bridge.js`.** This extension only needs the DOM, and
  the isolated world already has `chrome.*`. MAIN world would buy nothing and
  cost the orphan guard.
- **The shortcut is a Chrome command, never a page keydown listener.** A page
  listener could swallow a keystroke Notion wanted; `/` and `Esc` are live
  ammunition inside Notion.
- **The toast reports failures, not successes.** Success is self-evident — the
  settings panel is right there. A "done!" toast over it would be noise.
- **`toggle` on a second press** rather than reopening. Matches Chat Sweeper's
  `⌘⇧K` behaviour.
- **`setProblem()` returns the failure object.** It returned `undefined` at
  first, which made a failed run report "Opened." in the popup.
- **`openSettings()` checks for the "Settings" row before clicking the
  workspace switcher.** The switcher is a toggle, so a failed attempt that left
  the popup open would have its retry *close* it — and every later rung of the
  ladder would fail identically. Verified: with the popup already open the flow
  completes in 999 ms without touching the switcher. Safe because the overlay
  container is empty when nothing is open (§6), so the check can't misfire.
- **The "Opening…" toast is delayed 600 ms.** The warm path finishes in ~0.7 s
  and a toast that appears and vanishes in that time is a flash of noise. Cold
  runs (~4 s) still get feedback.

---

## 8. If it breaks

1. Read `document.documentElement.dataset.nauLog` — the last ~24 steps,
   including which `waitFor` timed out. Content-script logs are invisible from
   the page console, so this is the real record.
2. The timeout label names the exact locator that failed; §4 says what it was
   verified against.
3. Re-run Part 0 of `../NOTION-EXTENSION-FIELD-GUIDE.md` before assuming
   anything else still holds.

### Folded into the field guide

Everything generalisable from this build is now in
`../NOTION-EXTENSION-FIELD-GUIDE.md`. Read it there rather than here — this log
keeps only what is specific to this extension. Where it landed:

| Finding | Guide section |
|---|---|
| Values that exist only as component props; the reachability checklist; the `propsAbove()` walk; the lookalike-metric warning | **3.8** (new) |
| Overlay popup container roles are unstable — never require `role="menu"` as an ancestor | **5.2** |
| Settings-surface anchors + the `<surface>-tab-<name>` / `-tabpanel-` id convention; the ids-vs-no-ids discriminator for nested tab rows | **5.1** |
| Idempotent retries / the toggle hazard; assert on ARIA state not display text; measured 0.7 s warm vs 4 s cold | **5.4** |
| Modal surfaces are not URL-addressable | **1** |
| Endpoint names aren't literals in the bundles; grep for prop names instead; lazily-chunked surfaces | **8** |
| Background-tab throttling kills external probes; use deadlines not tick counts | **7.2** |
| Trusted Types confirmed enforced; constructable stylesheets confirmed against Notion's CSP | **6.4** |
| Full 26-table cache listing | **3.3** |
| New symptom rows and traps 30–38 | **7.4**, **12** |
