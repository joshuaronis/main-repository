# Notion AI Usage

One keystroke to see how much Notion AI allowance you have left.

`⌘⇧U` opens Notion's own **Settings → Notion AI → Usage** panel — the one with
the *Rolling* and *Monthly* bars. Press it again to close.

It works from anywhere in Chrome: if the tab you're on isn't Notion, it
switches to a Notion tab, and if you don't have one open it opens one.

---

> **⚠️ Reload the extension once.** You reloaded it partway through the
> 2026-09-02 repair, so the copy running in Chrome may predate the final
> revision (the `aria-expanded` handling for parked popups). The shortcut works
> either way — that was confirmed live — but `chrome://extensions` → Reload ↻
> then reloading the Notion tab gets you the finished version.

## Install

1. `chrome://extensions` → turn on **Developer mode**
2. **Load unpacked** → pick this folder
3. Open (or reload) a Notion tab

> **Reloading the extension does not update tabs that are already open.**
> Reload the extension *and then* the Notion tab. A shortcut that "stopped
> working" is almost always this.

### The shortcut

`⌘⇧U` (Mac) / `Ctrl+Shift+U` (Windows/Linux). Chrome silently drops a
suggested shortcut if something else already claims it, so the popup shows the
key that is *actually* bound — if it says "not set", pick your own at
`chrome://extensions/shortcuts`.

The toolbar button does the same thing, and is the place failures get
explained.

---

## Why it drives the UI instead of just showing you the numbers

The obvious version of this extension is a little panel that prints your usage
without opening anything. That was the first choice, and it was abandoned after
measurement, not on taste:

**The Rolling and Monthly percentages have no reachable data source.** They are
not in Notion's client-side record cache, not in the response of any
`/api/v3/` call the Usage panel makes, not in any response header, and not
recoverable from the JS bundles. The only place those numbers exist in the
browser is as React props on the rendered bars — which means the settings panel
has to be open for them to exist at all, which defeats the entire point of a
standalone panel.

What *is* reachable is the separate **credits** balance, via
`POST /api/v3/getAIUsageEligibilityV2` with `{spaceId}`. That is a different
quota from the allowance bars — Notion says so on the panel itself: "Products
that use credits like Custom Agents and Workers don't count toward this
allowance." Showing credits and calling it usage would have been wrong.

So the extension does the reliable thing: it performs the four clicks for you,
in about a second.

See `MAINTENANCE-LOG.md` for what was probed and ruled out, so nobody re-runs
that search from scratch.

---

## What it actually does

Four synthetic clicks against Notion's own controls:

```
workspace name (bottom of sidebar)  →  "Settings"  →  "Notion AI"  →  "Usage"
```

It works whether the sidebar is open or collapsed — a collapsed sidebar is
parked off-screen rather than unmounted, so the click still lands and your
sidebar is left exactly as you had it.

- **It never writes anything.** No `saveTransactions`, no API calls at all.
  Every action is a click you could have made yourself, and the only state it
  changes is which settings tab is showing.
- **Nothing leaves the browser.** No analytics, no remote endpoints.
- **It never touches your keyboard input inside Notion.** The shortcut is a
  Chrome command handled outside the page, so there is no page-level key
  listener that could swallow a keystroke Notion wanted — which matters,
  because `/` opens Notion's slash menu and `Esc` closes its overlays.
- **The workspace button is found by what it is, not where it is.** Notion
  moved it from the top of the sidebar to the bottom in September 2026 and
  broke v1.0.0 outright; the locator now matches a semantic class and, failing
  that, tries each plausible candidate and keeps whichever one actually
  produces a "Settings" row.
- Each step is verified before the next one runs, and the whole sequence
  retries on a `[0, 1500, 4000] ms` ladder. Notion's DOM reports itself ready
  well before React attaches handlers, and a click landed in that window is
  swallowed with no error at all.

Measured on a real workspace: **~0.7 s** warm, **~4 s** on a freshly loaded
page (the settings bundle is lazy-loaded).

---

## When it doesn't work

The toolbar popup shows the last failure. A toast in the page shows it too.

| What you see | What it means |
|---|---|
| "That Notion tab is not listening" | Extension reloaded, tab wasn't. Reload the tab. |
| "Could not find the workspace button…" | Notion moved or renamed it again. See the maintenance log — the locator is deliberately position-independent, so this means the element itself changed. |
| "…found no 'Settings' item" | Notion renamed the menu entry. See the maintenance log. |
| "…no 'Notion AI' section in it" | Your account/plan doesn't show that settings section. |
| Nothing at all happens | Check `document.documentElement.dataset.nauLog` in the console — the last ~24 steps are mirrored there, because content-script logs are invisible from the page's own console. |

---

## Files

| File | Role |
|---|---|
| `manifest.json` | MV3. One content script, isolated world. |
| `background.js` | Owns the shortcut; decides which tab to drive. |
| `content.js` | The locators and the click sequence. |
| `popup.html` / `popup.js` | Fallback button, bound-shortcut display, last error. |
| `generate_icons.py` | Redraws the icons. Needs Pillow. |
| `MAINTENANCE-LOG.md` | What was verified live, what broke, and why the code looks like it does. |

There is no MAIN-world script and no `bridge.js`. This extension only needs the
DOM, and the isolated world already has `chrome.*` — the bridge pattern would
be pure overhead here.
