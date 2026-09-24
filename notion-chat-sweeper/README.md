# Notion Chat Sweeper

A Manifest V3 Chrome extension (loaded unpacked) that bulk-deletes and restores
Notion AI chat threads.

Notion's own UI deletes chats one at a time and **cannot undo a deletion** —
deleted chats never reach Notion's Trash. This extension does both: bulk delete,
and restore.

## Install

1. Open `chrome://extensions`.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked** and pick this folder.
4. Open Notion, click the **Chat** tab, and reload the tab (⌘R).

Reloading the extension does **not** update already-open tabs. Reload the
extension, *then* the tab.

## Use

- Click the 🧹 button (drag it anywhere; the position is remembered).
- Or press **⌘⇧K** / **Ctrl+Shift+K**.
- Or click the extension's toolbar icon → **Open panel**.

The toolbar popup can hide the broom. The keyboard shortcut and the popup button
still open the panel when it's hidden, so it can't get lost.

### Selecting

| Control | What it does |
|---|---|
| filter box | narrows the list by title; `/` focuses it |
| `+ shown` / `− shown` | select / deselect everything currently shown |
| `all` / `none` / `invert` | across all chats, not just shown ones |
| `newest N` | selects the N most recently updated shown chats |
| `older than N days` | **narrows the view** to chats not updated in N days; click again to clear. Combine with `+ shown` to select them |
| sort | newest / oldest / by title |
| click, then shift-click | selects the range; shift-click again to pull it back |
| ↻ | re-reads the list from Notion and re-checks it against the sidebar |

`older than N days` filters rather than selects, so it stacks with the title
filter and you can just *look* at your old chats without touching the
selection. Two clicks — `older than`, then `+ shown` — to select them all.

Selection is by chat, so it survives filtering and re-sorting. Hover any row to
see its exact last-updated time.

## Restoring — read this part

The **Restore** tab lists every chat we can still bring back, newest first, each
tagged with where we know about it from:

| Tag | Source |
|---|---|
| `session` | still in Notion's cache, deleted since this page loaded |
| `journal` | recorded by the panel before it went away; survives reloads |
| `log` | from a run's undo log |

The time on each row is **when the chat went away**, not when you last used it.

Tick the ones you want — click and shift-click selects a range, same as the
Delete tab — and hit **Restore N**. The run picker below restores an entire past
run in one go; the last five are kept. **Download record** saves the undo log
and journal as JSON; that's a convenience, not the safety net. Restore is the
safety net.

### Forget

**Forget N** drops this extension's record of the selected chats, to stop the
list growing without limit.

It cannot delete anything from Notion. Deletion there is a soft flag and dead
chats never reach the Trash, so a forgotten chat simply stays deleted and
invisible forever — you just lose the only handle that could have brought it
back. It sends no network request at all; it edits local storage only.

**This is the one irreversible action in the extension.** Everything else is a
flag Notion can flip back.

Two things to know:

- Anything that went more than **30 days** ago is hidden to keep the list
  usable. It is only hidden — the footer tells you how many, and
  `Download record` still contains them. Change `restoreMaxAgeDays` in
  `content.js` to adjust.
- **Restoring does not re-pin a pinned chat.** The chat comes back; its pin
  doesn't.


Deletion is a soft flag flip on Notion's side, not an erase, which is why
restore works at all. What we can restore depends on whether we still know the
chat's ID:

- **Deleted this session** — still in Notion's in-memory cache, with its title.
  Free.
- **Deleted after the extension was installed** — recorded in the journal
  (`ncs_journal` in localStorage), written every time the panel opens. This also
  covers chats you deleted **by hand** through Notion's ••• menu, or on your
  phone, as long as the panel had seen them at least once.
- **Deleted before the extension was installed** — **cannot be restored.**
  Nothing on this machine records that those chats ever existed. There is no
  workaround.

`Undo last` restores everything the most recent run deleted.

Both the journal and the undo log live in `localStorage`, which is per-origin,
not per-tab — but it is per-browser-profile. They don't sync to another machine.

## Safety

- Nothing leaves the browser. The only network call is a same-origin POST to
  `app.notion.com/api/v3/saveTransactionsFanout`.
- Only chats are targeted — never pages, agents, databases, or meeting notes.
  Anything that didn't come out of the thread enumeration is refused outright.
  Your custom agents don't appear in the list at all.
- Deletion needs an explicit click on a button labelled with the count, and the
  confirmation dialog lists the actual titles.
- Over 25 selected asks a second time. A hard cap limits any single run.
- The undo log is written before the first request. If that write fails, the run
  doesn't start.

## Debugging

The last 20 events are mirrored into a DOM attribute, because copying console
output out of DevTools is a nuisance. Paste this into the Console:

```js
document.documentElement.dataset.ncsLog
```

`window.__ncs` also exposes `listThreads()`, `findCache()`, `buildCtx()`,
`runs()`, `journal()`, and `rescan()`.

## Files

```
manifest.json
content.js          the panel; MAIN world; one sectioned file
bridge.js           ~15 lines, ISOLATED world — message relay only
background.js       keyboard command relay
popup.html / popup.js
MAINTENANCE-LOG.md  things that cost time to discover — read before changing
```

`content.js` runs in the MAIN world because React's `__reactFiber$…` expandos
are invisible from a content script's isolated world, and the whole enumeration
depends on them. MAIN-world scripts get no `chrome.*` APIs, hence `bridge.js`.
