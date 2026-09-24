# Building Chrome extensions for Notion — field guide

Everything learned from three extensions built against Notion's web app:

- **Notion Minimal Comments** (2026-07) — DOM automation; drives synthetic clicks
  through Notion's own menus.
- **Notion Chat Sweeper** (2026-08) — API + record-cache; reads Notion's internal
  data store and posts transactions directly. Built *and shipped*: Parts 3.7, 5.6
  and 9 come from the implementation, not the discovery phase, and could not have
  been learned any other way.
- **Notion AI Usage** (2026-08, repaired 2026-09) — drives Notion's *settings*
  surface, after first proving that the value it wanted was unreachable any other
  way. Parts 3.8, 5.2, 5.4 and 8 carry what that search turned up; the negative
  result in 3.8 is the most reusable thing in it. Then Notion rearranged the
  sidebar and it broke outright, which is where the position rule in 5.1 and the
  parked-popup / `aria-expanded` findings in 5.2 come from — those are the only
  parts of this guide so far written from a *regression* rather than a build, and
  they are the ones most likely to save you a session.

They took different approaches, which is why between them they cover most of what
you need. Everything below was verified live against a real logged-in account,
not inferred from documentation — there is no documentation.

---

## How to use this document

**You are probably an AI assistant** being handed this by Josh at the start of a
new Notion extension project. Read the whole thing before proposing an
architecture; the world-selection decision in Part 2 is hard to reverse later.

**Josh is not a DevTools person.** He can paste a snippet into the console and
paste the output back, and he does it well and patiently. He cannot be asked to
"find the right request" or "grab the selector." Every instruction must be
click-by-click. Part 10 covers how to run that loop.

### ⚠️ Verify before you build

Notion ships changes constantly. This guide was accurate on **2026-08-04**
against client version `23.13.20260803.1816`. The verification block in Part 0
takes ninety seconds and tells you which parts still hold.

Re-confirmed later the same day against `23.13.20260804.1857`: the fiber walk in
3.1, the table-map path in 3.3, every DOM anchor in 5.1, Trusted Types being
enforced, and constructable stylesheets surviving Notion's CSP. The write path
(Part 4) was *not* re-checked on that build.

**Re-verified 2026-09-02 against `23.13.20260903.0022`**, after Notion AI Usage
stopped working. Two things in this document had gone stale, and both had been
stated as verified facts:

- **The sidebar was rearranged.** The workspace switcher moved from the top to
  the bottom; search / inbox / new-page took the top. Any locator using screen
  position broke. See the new rule in **5.1**.
- **The overlay is no longer empty at rest.** Dismissed popups stay mounted with
  real layout boxes, so the standard rect-only `visible()` helper — used by
  nearly every locator here — now reports closed menus as open. Ask the
  trigger's `aria-expanded` instead. See **5.2**; this one needs a change to code
  you have already written, and it carries a second warning about
  `checkVisibility()` that is worth reading before you reach for the obvious
  fix.

Still true on that build: every other anchor in 5.1, the settings id convention,
the ids-vs-no-ids tab discriminator, Trusted Types enforced, constructable
stylesheets, synthetic clicks (5.3), and the retry discipline in 5.4. Part 4
(writing) was not re-checked.

The same pass re-verified **Notion Minimal Comments** end to end — nothing there
was broken — and added **3.9**, which is the most reusable thing to come out of
it: page-level settings live on the block record and are readable with a plain
same-origin `fetch` from the **isolated** world, so a MAIN-world script is often
unnecessary. 3.9 also carries the 200-with-a-stub trap, which is the kind of bug
that produces a confident wrong answer rather than an error.

**If any check fails, stop and tell Josh which one, before writing code.** Do not
quietly work around a failed check — a wrong assumption here surfaces later as a
silent no-op, which is the worst failure mode Notion extensions have. Every
project has lost time to exactly that; the only one that caught it cheaply did so
because the shipped locators were run against the live app before shipping
(Part 9).

---

## Part 0 — Verification snippet

Have Josh open `https://app.notion.com`, log in, open a page with at least one
comment, click the **Chat** tab in the sidebar once, then paste this into the
DevTools Console (Cmd+Option+I → Console) and paste the output back.

```js
(() => {
  const out = [], H = document.documentElement;
  out.push('origin: ' + location.origin + '   path: ' + location.pathname.slice(0, 60));
  out.push('client version: ' + H.dataset.notionVersion + '   notion-html: ' + H.dataset.notionHtml);
  out.push('');
  out.push('--- STABLE DOM ANCHORS ---');
  [['#sidebar-tabpanel-chats', 'chat sidebar panel'],
   ['.notion-sidebar-container', 'left sidebar'],
   ['.notion-sidebar-switcher', 'workspace switcher'],
   ['.notion-page-content', 'page content'],
   ['.notion-overlay-container', 'overlay root'],
   ['[aria-label="Actions"]', 'page ••• button'],
   ['.notion-topbar, [class*="topbar"]', 'topbar']]
    .forEach(([sel, label]) => out.push(`  ${document.querySelector(sel) ? 'OK  ' : 'MISS'} ${label}  (${sel})`));

  // 5.1 — where things are is NOT a locator, but printing it tells you at a
  // glance whether Notion has rearranged the sidebar again.
  const sw = document.querySelector('.notion-sidebar-switcher');
  if (sw) { const r = sw.getBoundingClientRect();
    out.push(`  switcher at top:${Math.round(r.top)} left:${Math.round(r.left)} ` +
             `${Math.round(r.width)}x${Math.round(r.height)}   ` +
             `(bottom of an ${innerHeight}px viewport as of 2026-09; was the top in 2026-08)`); }

  // 5.2 — the overlay was empty at rest in 2026-08 and is NOT in 2026-09.
  const ovIdle = (document.querySelector('.notion-overlay-container') || {}).textContent;
  out.push('  overlay textContent empty at rest: ' +
           (ovIdle !== undefined ? String(ovIdle).trim() === '' : 'n/a') +
           '   (false is EXPECTED now — parked popups, 5.2)');
  {
    // Parked-popup detector. checkVisibility is used here as a DIAGNOSTIC only —
    // do not copy it into a locator, see the warning in 5.2. This line is only
    // meaningful in a foreground tab; in a hidden one every row reads invisible.
    out.push('  tab visible (required for the next line): ' +
             (document.visibilityState === 'visible'));
    const ov = document.querySelector('.notion-overlay-container');
    const rows = ov ? [...ov.querySelectorAll('[role="button"],[role="menuitem"],[role="option"]')] : [];
    const boxed = rows.filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
    const real  = boxed.filter(e => e.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true }));
    out.push(`  overlay rows with a box: ${boxed.length}   of those actually painted: ${real.length}` +
             (boxed.length > real.length ? '   <-- PARKED POPUP PRESENT (5.2)' : ''));
    // The signal you should actually build on:
    const trig = [...document.querySelectorAll('[aria-haspopup][aria-expanded]')]
      .filter(e => e.getAttribute('aria-expanded') === 'true');
    out.push('  triggers currently reporting aria-expanded="true": ' + trig.length +
             '   (this is the openness test to use — 5.2)');
  }
  out.push('  Trusted Types enforced: ' +
           !!(window.trustedTypes && window.trustedTypes.defaultPolicy !== undefined));
  out.push('');
  out.push('--- REACT FIBER ACCESS ---');
  const anyEl = document.querySelector('#sidebar-tabpanel-chats *') || document.body;
  const fk = Object.keys(anyEl).find(k => k.startsWith('__reactFiber$'));
  out.push('  fiber key present: ' + !!fk + (fk ? ' (' + fk.slice(0, 20) + '…)' : ''));
  out.push('');
  out.push('--- RECORD CACHE ---');
  let ctx = null;
  const probe = el => {
    const k = Object.keys(el).find(k => k.startsWith('__reactFiber$'));
    if (!k) return null;
    let f = el[k];
    for (let i = 0; i < 40 && f; i++, f = f.return) {
      const p = f.memoizedProps; if (!p) continue;
      for (const v of Object.values(p))
        if (v && typeof v === 'object' && v.inMemoryRecordCache &&
            typeof v.inMemoryRecordCache.forEachRecordOfTable === 'function' &&
            typeof v.userId === 'string')
          return { cache: v.inMemoryRecordCache, userId: v.userId };
    }
    return null;
  };
  for (const root of [document.getElementById('sidebar-tabpanel-chats'), document.body]) {
    if (!root) continue;
    for (const el of root.querySelectorAll('*')) { ctx = probe(el); if (ctx) break; }
    if (ctx) break;
  }
  out.push('  cache found: ' + !!ctx);
  if (ctx) {
    out.push('  forEachRecordOfTable source: ' +
      String(ctx.cache.forEachRecordOfTable).slice(0, 160).replace(/\s+/g, ' '));
    let n = 0, titled = 0;
    try {
      ctx.cache.forEachRecordOfTable({ userId: ctx.userId, table: 'thread',
        fn: ({ model }) => { n++;
          let d; try { d = model.getKeyValue('data'); } catch (e) {}
          if (d && d.title) titled++; } });
      out.push(`  threads enumerated: ${n}   with titles via getKeyValue('data'): ${titled}`);
    } catch (e) { out.push('  ENUMERATION FAILED: ' + e.message); }
    try {
      const tables = ctx.cache.data.data[ctx.userId].inner.data;
      out.push('  tables in cache: ' + [...tables.keys()].join(', '));
    } catch (e) { out.push('  table map not reachable at the documented path: ' + e.message); }
  }
  out.push('');
  out.push('--- WRITE ENDPOINT (harmless no-op probe) ---');
  fetch('/api/v3/syncRecordValues', { method: 'POST', credentials: 'include',
    headers: { 'content-type': 'application/json' }, body: '{}' })
    .then(r => { out.push('  /api/v3/syncRecordValues reachable, status ' + r.status +
                          ' (400 expected — it wants a pointer)');
      window.__vfy = out.join('\n'); console.log(window.__vfy);
      console.log('\n=== now run:  copy(__vfy)'); })
    .catch(e => { out.push('  UNREACHABLE: ' + e.message);
      window.__vfy = out.join('\n'); console.log(window.__vfy); });
})();
```

**Reading the result**

| Line | If it fails |
|---|---|
| `origin` not `app.notion.com` | Notion moved again. Update all `matches` and `host_permissions`. |
| Any `MISS` under stable anchors | That anchor was renamed. Part 5 lists what to look for instead. |
| `switcher at top:` is nowhere near the bottom | The sidebar was rearranged again. Fine *if* your locator ignores position (5.1) — check that it does. |
| `overlay rows with a box` > `actually painted` | Parked popups are live on this build. A rect-only `visible()` is unsafe — gate on `aria-expanded` (5.2). |
| `tab visible: false` | Re-run it in a foreground tab; the parked-popup line means nothing otherwise, for exactly the reason 5.2 warns about. |
| `aria-expanded="true"` count is non-zero at rest | Something is genuinely open. Close all menus and re-run. |
| `fiber key present: false` | React internals changed; the fiber walk (Part 3) needs re-derivation. Stop and say so. |
| `cache found: false` | Part 3 is stale. Fall back to DOM automation (Part 5) or re-derive. |
| `forEachRecordOfTable source` differs from Part 3 | Read the new signature off the printed source and adapt. |
| `with titles` much lower than `threads enumerated` | The lazy-field accessor changed. See Part 3.4. |

---

## Part 1 — Environment

| Fact | Value | Confidence |
|---|---|---|
| Web app origin | `https://app.notion.com` | verified 2026-08 |
| Legacy origin | `https://www.notion.so` — redirects; still match it | verified |
| Page URL shape | `/p/<workspace>/<Title>-<32hex>` | verified |
| AI chat URL shape | `/chat?t=<32hex, dashless>` | verified |
| Peek/side preview | id lives in the **query** (`?p=<id>`), not the path | verified 2026-07 |
| Client version | `document.documentElement.dataset.notionVersion` | verified |
| Platform marker | `document.documentElement.dataset.notionHtml` = `"web"` | verified |
| Content in top frame | yes — `all_frames` can stay off; iframes are external embeds | verified |
| Trusted Types | **enforced** — confirmed, not assumed; never use HTML-string sinks | verified 2026-08 |
| Modal surfaces | **not URL-addressable** — `location` does not change when one opens | verified 2026-08 |

**Not every surface has a URL.** Settings is the worked example: opening it leaves
`location.href` byte-identical, so there is no deep link to a settings section and
no way to restore one by navigating. Check before you design around a URL — if a
surface can't be addressed, reaching it means driving the UI (Part 5), and that
changes your architecture.

**Always extract page ids from `location.pathname` only.** Peek previews put a
different id in the query string, and reading it triggers action on a page the
user is merely previewing. This was a real bug class in the first extension.

IDs appear in two forms and you will meet both: **dashed UUID**
(`3b110b79-03aa-8063-acd7-00a9fe70e286`) in API payloads and React props, and
**dashless 32-hex** (`3b110b7903aa8063acd700a9fe70e286`) in URLs. Convert freely;
they are the same value.

---

## Part 2 — Choosing your world

This is the first architectural decision and the expensive one to reverse.

Chrome runs content scripts in an **isolated world**: same DOM, separate
JavaScript context. Expando properties the page sets on DOM nodes — including
React's `__reactFiber$…` — are **invisible** from there. So are the page's own
functions.

| You need to… | World | Why |
|---|---|---|
| Click Notion's buttons and menus | ISOLATED | DOM access is all you need; keep `chrome.*` |
| Drive a surface that has no URL (settings, dialogs) | ISOLATED | it is still only clicks |
| Read record ids, titles, or any Notion state | **MAIN** | Only reachable through React fibers |
| Read a value that lives only in component props (3.8) | **MAIN** | same fibers, different walk |
| Call `/api/v3/` with the user's session | either | Same-origin `fetch` + `credentials:'include'` works in both |
| Use `chrome.storage`, popup, commands | ISOLATED (or a bridge) | MAIN has no `chrome.*` at all |

```json
"content_scripts": [{ "matches": [...], "js": ["content.js"],
                      "run_at": "document_idle", "world": "MAIN" }]
```

### The bridge pattern

If you need MAIN-world data *and* `chrome.*` (a toolbar popup, a keyboard
command, `chrome.storage`), run both and relay between them:

```
popup.js ──chrome.tabs.sendMessage──▶ bridge.js (ISOLATED) ──CustomEvent──▶ content.js (MAIN)
         ◀───────────────────────────          ◀───────────────────────────
```

```js
// bridge.js — ISOLATED. Forwards messages. Nothing else.
chrome.runtime.onMessage.addListener((msg, _s, respond) => {
  if (msg && msg.ns === 'yourprefix') {
    window.dispatchEvent(new CustomEvent('yourprefix:cmd', { detail: msg }));
    respond({ ok: true });
  }
  return true;
});
window.addEventListener('yourprefix:state', e => {
  try { chrome.storage.local.set({ yourprefixState: e.detail }); } catch (err) {}
});
```

### What you give up in MAIN world

- **No `chrome.*`**, including `chrome.runtime?.id` — so the orphan-detection
  trick from Part 6 doesn't work. Use a window sentinel instead.
- **Shared global namespace with the page.** Wrap everything in an IIFE and
  expose exactly one global.
- **No isolation from page scripts.** Notion could in principle observe you. This
  matters for nothing in practice, but don't put secrets there.

`localStorage` works in both (it is per-origin, not per-world).

---

## Part 3 — Reading Notion's data

This is the big one. Notion keeps a client-side record store containing
everything it has synced, and it is fully readable from MAIN world. **Reading
from the store beats scraping the DOM on every axis**: real titles, real
timestamps, no virtualization, no hashed classes, no layout dependence.

### 3.1 Getting a handle on the cache

```js
function findCache() {
  const probe = el => {
    const k = Object.keys(el).find(k => k.startsWith('__reactFiber$'));
    if (!k) return null;
    let f = el[k];
    for (let i = 0; i < 40 && f; i++, f = f.return) {
      const p = f.memoizedProps;
      if (!p) continue;
      for (const v of Object.values(p)) {
        if (v && typeof v === 'object' && v.inMemoryRecordCache &&
            typeof v.inMemoryRecordCache.forEachRecordOfTable === 'function' &&
            typeof v.userId === 'string') {
          return { cache: v.inMemoryRecordCache, userId: v.userId,
                   spaceId: v.model && v.model.space_id };
        }
      }
    }
    return null;
  };
  for (const root of [document.getElementById('sidebar-tabpanel-chats'),
                      document.querySelector('.notion-page-content'),
                      document.body]) {
    if (!root) continue;
    for (const el of root.querySelectorAll('*')) { const hit = probe(el); if (hit) return hit; }
  }
  return null;
}
```

Walking `f.return` climbs the fiber tree toward the root; store objects are
passed as props several levels above the leaf DOM node, typically 20–25 hops.
Scoping the search to a small container first is a large speed win; the
`document.body` fallback keeps it working when that container isn't rendered.

### 3.2 Enumerating a table

Signature read directly from Notion's minified source:

```
forEachRecordOfTable({ userId, table, fn })   // fn receives ({ model, role })
forEachRecord({ userId, fn, signal, shouldIncludeCacheFallbackRecords })
getEntry(key, opts)      getRecord(key, opts)
```

```js
function listRecords(ctx, table) {
  const out = [];
  ctx.cache.forEachRecordOfTable({
    userId: ctx.userId, table,
    fn: ({ model, role }) => out.push({ model, role })
  });
  return out;
}
```

**Records with `role: "none"` are skipped by this method.** If a count from here
disagrees with a count from the DOM by one or two, that is usually why.

**Larger disagreements are normally the DOM's fault, not the cache's.** Notion
virtualizes long sidebar lists — rows scrolled past are unmounted — so a DOM walk
routinely sees a subset. `cache > DOM` is the ordinary state and means nothing.
The direction that matters is `DOM > cache`: the UI knows about a record your
enumerator missed.

Cross-check and warn, but **warn asymmetrically**. Make "visible in the UI,
absent from my list" loud, and "in my list, not currently rendered" quiet. One
warning style for both fires on nearly every scan and stops meaning anything —
Chat Sweeper shipped a single amber banner for both cases and Josh reasonably
read the routine one as a fault.

### 3.3 Tables that exist

Full list read off one workspace on 2026-08-04 (`Map(26)` — it was `Map(21)` a
day earlier, so **treat this as a sample, never a fixed set**; the map grows as
the session touches more features):

```
notion_user   user_root      user_settings   space_view    sidebar_section
space         space_user     block           collection    collection_view
layout        prompt         workflow        thread        activity
notification  access_request discussion      comment       follow
bot           external_authentication        integration
page_visit    page_exit      workflow_artifact
```

`thread` holds AI chats. `block` holds pages and blocks. `collection` holds
databases. `discussion` + `comment` hold comments. `workflow` + `prompt` +
`workflow_artifact` are the agents/Workers surface.

Enumerate rather than assume — the map is right there:

```js
[...ctx.cache.data.data[ctx.userId].inner.data.keys()]
```

### 3.4 ⚠️ Lazy fields — the biggest trap in this document

A cached `model` exposes **scalars as plain properties** but keeps most fields
lazy behind an accessor:

```js
model.id          // ✅ works
model.table       // ✅ works
model.data        // ❌ undefined — always
model.alive       // ❌ undefined — always

model.getKeyValue('data')          // ✅ { icon, title, usage_summary, … }
model.getKeyValue('alive')         // ✅ true | false
model.getKeyValue('created_time')  // ✅ epoch ms
model.getKeyValue('updated_time')  // ✅ epoch ms

model.getKeyStore('data').getValue()   // equivalent, via the store object
```

`getKeyValue` is literally `e => n[e]` over a closed-over record. There is also a
`model.value` object holding the raw record, but reading through `getKeyValue`
is what Notion's own components do.

This trap cost roughly six probe rounds during the Chat Sweeper build. Symptom:
enumeration returns the right *number* of records with every title showing as
undefined. If you see that, this is why.

```js
const kv = (m, k) => { try { return m.getKeyValue(k); } catch (e) { return undefined; } };
```

### 3.5 Record shape — `thread` as the worked example

```json
{
  "id": "3b110b79-03aa-8004-9f2f-00a9d8bd60ce",
  "version": 64,
  "space_id": "…", "parent_id": "…", "parent_table": "space",
  "alive": true,
  "type": "workflow",
  "created_source": "ai_module",
  "created_time": 1785729872609,
  "updated_time": 1785731848617,
  "created_by_id": "…", "created_by_table": "notion_user",
  "updated_by_id": "…", "updated_by_table": "notion_user",
  "messages": ["<uuid>", "…"],
  "data": { "icon": "/icons/chat_lightgray.svg", "title": "…",
            "usage_summary": { "input_tokens": 148142, "…": "…" } }
}
```

The pattern generalizes: `alive` is the soft-delete flag, `data` holds the
user-visible payload, `parent_table` + `parent_id` give the hierarchy,
timestamps are epoch milliseconds.

### 3.6 What the cache does *not* contain

**Soft-deleted records survive in the cache for the rest of the session, with
their data intact — but vanish on reload.** The server stops syncing them down.

Verified: delete a thread, `alive` flips to `false` locally and the title stays
readable indefinitely. Reload → the record is gone entirely, and no amount of
digging recovers it.

**Consequence for any undo feature:** in-session undo is free. Anything crossing
a reload needs your own journal in `localStorage` — snapshot `{id, title,
timestamps}` on each run, and treat "in my journal but absent from the live set"
as deleted. And be honest that records deleted *before your extension existed*
are unrecoverable, because nothing on the machine remembers them.

### 3.7 ⚠️ The cache lags your own writes

**Found during the Chat Sweeper build; the most confusing bug of the project.**
After `saveTransactionsFanout` returns `200`, the record cache keeps reporting
the *old* value for a second or more. Notion's own sidebar updates immediately;
`getKeyValue('alive')` does not.

The log line that gave it away, written straight after a successful delete:

```
scan: cache 45 dom 44 dead 0     ← 45 alive, ZERO dead, one just deleted
```

Every symptom looks like a broken write:

- The delete appears to do nothing — the row leaves Notion's UI but stays in your list.
- Deleting the same record *twice* "works", because the cache caught up in between.
- **Restore looks inverted**: the record returns to Notion's UI and disappears
  from yours, because the cache still reports it dead.

**Never re-read the cache immediately after a write and trust the answer.**

Treat a `200` as better evidence than a fresh read, via a self-draining override:

```js
const confirmed = new Map();                    // id -> { value, at }
const onWriteOk = (id, value) => confirmed.set(id, { value, at: Date.now() });

function readRecords() {
  const all = enumerate();                      // your listThreads() equivalent
  const now = Date.now();
  for (const [id, v] of confirmed)              // expire: a write to a record the
    if (now - v.at > 60000) confirmed.delete(id);  // cache never returns would pin forever
  for (const r of all) {
    const v = confirmed.get(r.id);
    if (!v) continue;
    if (r.alive === v.value) confirmed.delete(r.id);   // cache agreed — drop it
    else r.alive = v.value;                            // cache stale — override
  }
  return all;
}
```

Then re-scan a couple of times after a run (~900 ms and ~2600 ms) so the map
drains by itself, and log the pending count — it should reach zero within
seconds.

**This interacts with the cross-check in 3.2.** Right after a bulk delete your
list has dropped the records but the UI may not have, which is exactly the
`DOM > cache` shape that should be loud. Suppress the warning for ids with a
pending confirmed write, or a 40-record delete announces that 40 records are
missing at the very moment you delete them.

### 3.8 ⚠️ Some values exist *only* as component props

Parts 3 and 4 can make the record cache look exhaustive. It isn't. Notion
displays plenty of values that are in no cached record and behind no endpoint
you can call — they are computed server-side, handed to one component, and
rendered. **Nothing on the page remembers them once that component unmounts.**

This matters before you write any code, because it decides whether a
"show me X without opening the UI" extension is possible at all. If X only
exists as props of a mounted component, a headless panel cannot be built — you
either drive the UI to the screen that shows X (Part 5), or you pick a
different value.

**Prove reachability first, cheapest source first.** Stop at the first hit:

| # | Source | How | Cost |
|---|---|---|---|
| 1 | Record cache | 3.1 → 3.3 | free, no UI |
| 2 | An API response | wrap `fetch` (4.3), then open the UI **once** and read what came back | one click-through |
| 3 | Response headers | `r.headers.forEach(…)` on any `/api/v3/` call | seconds |
| 4 | Hook state / query cache | walk `f.memoizedState.next…` above the node | minutes |
| 5 | Component props | below | minutes |

Reaching 5 is the negative result: **not reachable headlessly.** Say so plainly
and change the design rather than shipping an approximation — see the warning
about lookalike values at the end of this section.

```js
// Walk UP from a rendered node collecting props whose keys match a pattern.
// 3.1 walks the same tree looking for one known object; this looks for values
// when you don't yet know what you're looking for.
function propsAbove(node, re, hops = 30) {
  const k = Object.keys(node).find(x => x.startsWith('__reactFiber$'));
  if (!k) return [];
  const out = [];
  for (let f = node[k], i = 0; i < hops && f; i++, f = f.return) {
    const p = f.memoizedProps;
    if (!p || typeof p !== 'object') continue;
    for (const key of Object.keys(p)) {
      if (key === 'children' || !re.test(key)) continue;
      let v;
      try { v = JSON.parse(JSON.stringify(p[key])); }
      catch (e) { v = String(p[key]).slice(0, 80); }
      out.push({ hop: i, key, value: v });
    }
  }
  return out;
}

// Find the node that renders the number, then ask what fed it:
const node = [...document.querySelectorAll('[role="dialog"] *')]
  .find(e => /^\d+% used$/.test((e.textContent || '').trim()));
propsAbove(node, /usage|limit|percent|reset|quota|period/i);
```

The owning component sits **5–10 hops up**, much shallower than the 20–25 hops
to a store. One call returned the whole shape:

```js
{ percentUsed: 70.72, resetsInMs: 21011289,
  monthlyUsage: { percentUsed: 22.54, periodEndMs: 1787091712000 } }
```

**Then grep the bundles for one of those prop names** to learn the full type,
including states the UI isn't currently in. `resetsInMs` appeared in three
chunks alongside `limit`, `window`, `retryAfterSeconds`, `within_limit`,
`rate_limited`, `not_applicable` and `billing_period` — which named the value as
a rate-limit status object and explained why no settings endpoint returns it.
Prop names *are* string literals in the bundles even when endpoint names are not
(Part 8).

> ⚠️ **The dangerous part of this is the lookalike.** The same screen usually
> offers a *different* number that you can fetch easily, and it is very tempting
> to ship that instead. A workspace's AI **credit** balance is one call away
> (`getAIUsageEligibilityV2`); the AI **allowance** bars beside it are not. They
> disagreed by a factor of thirty — 0.67% against 23% — because they meter
> different things, and Notion says so in small print on the panel itself.
> Reaching for the fetchable neighbour and relabelling it is the single easiest
> way to ship something confidently wrong.

---

### 3.9 Reading a record **without** the MAIN world

3.1–3.8 reach Notion's state through React fibers, which forces `world: "MAIN"`
and costs you `chrome.*` (Part 2). For **page-level settings** you often don't
need any of that: the same values are in the page's block record, and
`/api/v3/syncRecordValues` is a same-origin POST that works fine from the
ISOLATED world with `credentials: 'include'`.

```js
const res = await fetch('/api/v3/syncRecordValues', {
  method: 'POST', credentials: 'include',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ requests: [{ pointer: { table: 'block', id }, version: -1 }] }),
});
const rec = (await res.json()).recordMap.block[id];
const v = rec.value && rec.value.value ? rec.value.value : rec.value;  // both shapes shipped
```

`id` must be the **dashed** UUID; URLs give you dashless 32-hex (Part 1).
No `spaceId` is required in the pointer.

Useful fields on a page block, verified 2026-09:

| Field | Meaning |
|---|---|
| `parent_table` | `"space"` = standalone page, `"collection"` = database row page |
| `format.page_section_visibility.margin_comments` | `"inline"` = inline comments Default, `"minimal"` = Minimal, **key absent** = Default |
| `format.page_section_visibility.comments` | page-discussion section visibility |
| `format.page_icon`, `format.page_full_width`, `format.page_small_text` | the other ••• → Customize page toggles |

That `margin_comments` value is worth calling out: it is a setting with **no DOM
representation at all** (checked every attribute and class on the page-content
container and its ancestors), so a DOM-only extension cannot read it — and it is
what one of these extensions had spent a whole discovery phase failing to find.
`parent_table` likewise replaces "open the ••• menu and look for *Customize
layout*" as a standalone-vs-database test.

**This is the cheap middle ground between 3.8 and Part 5.** Before you commit to
a MAIN-world script and a bridge to read some piece of state, check whether it is
just a field on the block record.

#### ⚠️ Trap: "I can't read that" comes back as **HTTP 200**

`syncRecordValues` does not 4xx on a record you cannot see or that does not
exist. It returns 200 with a stub:

```js
{ spaceId: "…", value: { role: "none" } }     // no id, no type, no format
```

Every optional-chaining read on that object yields `undefined` — which is
indistinguishable from *"the field is legitimately absent"*. If your code treats
an absent field as a meaningful default (and above, absent `margin_comments`
genuinely **does** mean Default), an unreadable record silently becomes a
confident wrong answer, in whichever direction your default points.

This bit an extension during its own test matrix: an unreadable page returned
"Default", which was the verdict meaning *go modify this page*. Every other
failure path in that probe failed toward doing nothing; this one failed toward
the only outcome that writes.

**Always require positive proof you read a real record before trusting any
absence:**

```js
if (!v || !v.id) return 'UNKNOWN';   // stub, or no record at all
```

Test it deliberately — probe an all-zeros id and a malformed id and assert you
get your "don't know" verdict, not your default.

---

## Part 4 — Writing to Notion

### 4.1 The one endpoint that matters

```
POST https://app.notion.com/api/v3/saveTransactionsFanout
```

Every edit in the product flows through this. Rename a page, toggle a setting,
delete a chat — all the same call with a different operation.

```js
async function transact(operations, ctx = {}) {
  const tx = {
    id: crypto.randomUUID(),
    debug: { userAction: ctx.userAction || 'unknown', clientCommitTimeMs: Date.now() },
    operations: [].concat(operations)
  };
  if (ctx.spaceId) tx.spaceId = ctx.spaceId;
  const res = await fetch('/api/v3/saveTransactionsFanout', {
    method: 'POST', credentials: 'include',
    headers: Object.assign({ 'content-type': 'application/json' }, ctx.headers || {}),
    body: JSON.stringify({ requestId: crypto.randomUUID(), transactions: [tx] })
  });
  return { ok: res.ok, status: res.status, body: res.ok ? null : await res.text() };
}
```

### 4.2 Operation anatomy

```json
{
  "pointer": { "table": "thread", "id": "<uuid>", "spaceId": "<uuid>" },
  "path": [],
  "command": "update",
  "args": { "alive": false }
}
```

- **`pointer`** — which record. `spaceId` is optional (verified).
- **`path`** — which sub-field. `[]` means the record root; `["data","title"]`
  would target a nested value.
- **`command`** — `update` (merge args), `set` (replace at path). Others exist
  (`listAfter`, `listBefore`, `listRemove` for ordered collections) but were not
  exercised.
- **`args`** — the payload.

`requestId` and `transactions[].id` must be **fresh UUIDs on every request**.
`debug.userAction` is telemetry; copying the string the real client sends is the
conservative choice, and you find it by watching your own click in the Network
tab.

### 4.3 Authentication — simpler than expected

**The session cookie alone is sufficient.** A same-origin `fetch` with
`credentials: 'include'` authenticates. Removing each of these individually and
all together still returned `200`:

```
x-notion-active-user-header   x-notion-space-id
notion-client-version         notion-audit-log-platform
```

> ⚠️ That test used a no-op write (`alive: true` on an already-alive record).
> Notion may validate a no-op more loosely than a destructive one. **Send what
> the real client sends when you have it; never refuse to run when you don't.**

This is why an extension beats an external script: no `token_v2` extraction, no
expiry handling, no cookie jar.

**Learning the headers anyway** — wrap `fetch` at startup and record them from
Notion's own traffic. This is version-proof, since `notion-client-version`
changes on every deploy:

```js
const learned = {};
const orig = window.fetch;
window.fetch = function (...args) {
  try {
    const r = args[0], init = args[1] || {};
    const url = typeof r === 'string' ? r : r.url;
    if (/\/api\/v3\//.test(url)) {
      const h = new Headers((init && init.headers) || (r instanceof Request ? r.headers : undefined));
      for (const k of ['x-notion-active-user-header', 'x-notion-space-id',
                       'notion-client-version', 'notion-audit-log-platform']) {
        const v = h.get(k); if (v) learned[k] = v;
      }
    }
  } catch (e) {}
  return orig.apply(this, args);
};
```

Notion fires background requests constantly, so this populates within seconds.
**The wrapper must pass every call through untouched.** Fallback for the version
string: `document.documentElement.dataset.notionVersion`.

### 4.4 Batching and rate limits

`transactions` and `operations` are both arrays. Notion's client sends one of
each; the API accepts many. Measured:

| Operations in one request | Result |
|---|---|
| 10 | 200, 272 ms |
| 25 | 200, 356 ms |
| 42 | 200, 955 ms |
| 15 parallel requests | all 200, 4481 ms total |

Again: measured on no-ops. **Default to chunks of ~10, serialised**, and make it
a config value. On `429`/`5xx`: back off `[1000, 3000, 8000]` ms, retry the
chunk, then retry its items individually so one bad id doesn't sink the rest.

### 4.5 Soft delete

Notion deletes by flag, not erasure:

```js
// delete
{ alive: false, current_inference_id: null, current_inference_lease_expiration: null }
// restore
{ alive: true }
```

Verified for `thread`, including restore after a full page reload. **This means
undo is buildable for things Notion itself offers no undo for.** Check whether
your target table uses `alive` the same way before promising it.

Note also that AI chats deleted this way do **not** appear in Notion's Trash —
soft-deleted is not the same as trashed.

**`alive` is one field, not "the state of the record."** A *pinned* AI chat that
was deleted and then restored came back **unpinned** — pinning lives elsewhere
and the restore does not touch it. Check what else your users will expect to
survive the round trip before promising a clean undo.

**Your journal is the only handle.** Deletion is a flag and dead records leave
the cache on reload (3.6), so the id you stored is the sole route back.
Discarding your own record is therefore irreversible *for you* while changing
nothing on Notion's side. If you offer the user a way to prune that list, say it
in exactly those terms — "delete permanently" would be claiming something the
action does not do.

**"When it was deleted" is not `updated_time`.** A record untouched for a year
can be deleted a minute ago. Derive "when it went away" from your own journal and
undo-log timestamps, and fall back to `updated_time` only as a last resort.
Getting this backwards sorts a just-deleted record to the bottom of an undo list,
and any age cutoff hides it instantly.

**Notion deletes records on its own.** Two empty, untitled AI chats vanished from
a workspace within an hour with no user or extension action. Any journal-based
undo will therefore surface deletions its user did not make. That is the feature
working — but say so, or it reads as a bug.

### 4.6 Other endpoints seen

Observed in traffic; mostly undocumented. Useful for orientation:

```
syncRecordValues              fetch specific records by pointer
syncRecordValuesSpaceInitial  the big background sync (2–4 MB; floods the Network tab)
syncRecordValuesMain          incremental sync
syncRecordValuesSpace         needs (table, id) or pointer — not a list endpoint
loadCachedPageChunkV2         page content
getSpaces                     workspace list
search                        search (payload shape is fiddly; expect 400s while guessing)
getBacklinksForBlockInitial   backlinks
getUserNotificationsInitial   inbox
getInferenceTranscriptsUnreadCount   unread AI chat count
getPageVisitors, recordPageExit, getPresenceAuthorizationToken, getAssetsJsonV2
```

**There is no "list all records of a table" endpoint.** Enumeration comes from
the record cache (Part 3) or the DOM.

---

## Part 5 — The DOM

Only reach for the DOM when the cache can't answer — driving Notion's UI, or
cross-checking a list.

### 5.1 Stable anchors

Notion ships **hashed atomic CSS** (`x78zum5`, `xjp7ctv`, `xuxw1ft`). Those rot
without notice. **Never key a locator on a bare hashed class.** These survived
across a year and a major sidebar rewrite:

| Selector | What |
|---|---|
| `#sidebar-tabpanel-chats` | AI chat sidebar panel |
| `[aria-labelledby="sidebar-tab-chats"]` | same, structural fallback |
| `.notion-sidebar-container` | left sidebar root |
| `.notion-page-content` | page body |
| `.notion-overlay-container` | overlay/menu root |
| `.notion-topbar` | top bar |
| `[aria-label="Actions"]` | the page `•••` button |
| `[aria-label="Close"]` scoped to a dialog | that dialog's close button |
| `.notion-margin-discussion-item` | expanded margin comment |
| `svg.commentFilled`, `svg.commentFilledSmall` | comment icons |
| `[data-notion-version]` on `<html>` | client version |
| `[role="dialog"][aria-label="Settings & members"]` | the settings modal |
| `.notion-sidebar-switcher` | the workspace switcher (opens the menu with **Settings** in it) |
| `#settings-tab-<name>`, `[data-testid="settings-tab-<name>"]` | a settings left-nav entry |
| `#settings-tabpanel-<name>` | that entry's panel |

Topbar buttons carry stable `aria-label`s: `Lock sidebar open`, `Share`, `Copy
link`, `Page info`, `Comments`, `Favorite`, `Actions`.

**Notion's tabbed surfaces follow one id convention, and it is the best handle
in the whole app:**

```
<surface>-tab-<name>        the control
<surface>-tabpanel-<name>   the panel it reveals
```

`sidebar-tab-chats` / `sidebar-tabpanel-chats` and `settings-tab-ai` /
`settings-tabpanel-ai` are the same pattern. When you meet a new tabbed surface,
**guess the id from the convention and verify it** before falling back to text.
These ids are real ids, not hashed classes: they don't rot the way 5.1's opening
paragraph warns about, they're language-independent, and they survive
redesigns that move the thing across the screen. Known `<surface>` values:
`sidebar`, `settings`. Known settings `<name>` values include `settings`
(General), `ai`, `billing`.

**Where two tab rows are nested, the outer one carries ids and the inner one
does not.** Settings shows both at once: the left nav is `role="tab"` with
`settings-tab-*` ids, and the sub-tabs inside a section are `role="tab"` with no
id at all. That asymmetry is the cleanest way to tell them apart —

```js
const subTabs = [...dlg.querySelectorAll('[role="tab"]')]
  .filter(t => !/^settings-tab-/.test(t.id || ''));
```

— and it's far more durable than "the second row from the top", because it
doesn't care where either row is laid out.

**⚠️ Position is not a locator, and "structural" does not mean "coordinates".**
This is the single most expensive lesson of 2026-09. An extension pinned the
workspace switcher with `getBoundingClientRect().top < 200`, because it sat at
the top of the sidebar and that read as a nice durable structural fact. In
`23.13.20260903.0022` Notion **moved it to the bottom** — search / inbox /
new-page took over the top, and the switcher became the last row at `top 770`.
The filter matched nothing, and the extension died at step one with no error
worth the name. Nothing else in that flow had changed.

Rects earn their keep for *disambiguating* (a 194×28 row is not a 20×20 `…`
button) and for sanity checks. They are worthless as identity. Prefer, in order:
a semantic class, a real id, an `aria-label`, the item's own role plus its text,
its ancestry — and only then its size. Never its place on the screen.

**When you genuinely cannot tell two candidates apart, don't guess — verify by
outcome.** Return a *ranked list* from the locator and let the caller click each
in turn, keeping whichever one actually produced the thing you were after:

```js
for (const el of candidates()) {
  click(el);
  hit = await waitFor(theThingYouWanted, 2500);
  if (hit) break;
  await dismiss(el);            // they are toggles; clean up before the next try
}
```

That loop is the only locator strategy in this document that survives a rename
you have not seen yet, and it costs about two seconds in the failure case. Use
it wherever the target is a menu whose contents you can recognise.

**Locator discipline:** at least two strategies per target, make the last one
structural (role, aria, ancestry) rather than a class — and if the last one is
still ambiguous, verify by outcome rather than picking.

### 5.2 Menus and overlays

- Page `•••` menu items are `role="option"`. Sub-choosers use `role="menuitem"`.
  Do not assume `menuitem`.
- **Trap:** the left sidebar contains an always-visible `role="menu"` *outside*
  `.notion-overlay-container`. "Is a menu open?" must mean *a visible
  menu/dialog/listbox **inside** the overlay container*, or you will always
  believe a menu is open.
- **Trap:** some menu labels also exist as page-header buttons outside any menu
  (e.g. "Customize layout" on database pages). Scope every menu-item scan to the
  overlay container.
- With a menu open, visible popups appear as `div[role="menu"]`,
  `div[role="dialog"]`, `div[role="listbox"]`, sometimes nested.

- **⚠️ Trap, and the expensive one: the popup *container's* role is not stable.
  Never require it as an ancestor.** The same control's popup was observed
  rendering its rows inside `[role="dialog"][aria-modal="true"]` on one open and
  inside `[role="menu"]` on another, with both elements present in the overlay
  either time. A locator written as:

  ```js
  ov.querySelectorAll('[role="menu"] [role="button"]')   // ✗ over-tight
  ```

  passed in probing, then timed out on a real run **with the menu plainly open on
  screen** — a perfect silent no-op, and indistinguishable at a glance from the
  pre-hydration swallow in 5.4.

  Scoping to `.notion-overlay-container` is the whole of the rule above; it
  exists to exclude the sidebar's always-visible `role="menu"`, which is
  *outside* the container. Adding a container-role ancestor on top of that buys
  nothing and costs a session. Match the **item's** own role and its text:

  ```js
  ov.querySelectorAll('[role="button"], [role="menuitem"], [role="option"]')  // ✓
  ```

  Generalised: in Notion's overlay, `menu` / `dialog` / `listbox` are
  interchangeable wrappers around the same rows. Treat the container as *"is
  something open?"* only, never as part of the path to an item.

- **⚠️ Trap, and the subtle one: a dismissed popup is PARKED, not unmounted —
  and its rows keep real layout boxes.** This guide used to say "the overlay
  container is empty when nothing is open; `textContent` is `""` at rest", and
  built the cheap "is this item on screen right now?" check on top of it. As of
  `23.13.20260903.0022` **that is false.** Dismiss the workspace popup by
  clicking one of its rows and Notion keeps the whole thing mounted, hidden in a
  way that still gives every row a non-zero `getBoundingClientRect()` and a
  non-null `offsetParent`.

  Measured on the same "Settings" row, parked vs genuinely open:

  | Signal | Parked | Open |
  |---|---|---|
  | `getBoundingClientRect()` | **273×27** | 284×28 |
  | `offsetParent === null` | false | false |
  | overlay `textContent` | 207 chars | 207 chars |
  | `checkVisibility({checkOpacity, checkVisibilityCSS})` | false | true |
  | `document.elementFromPoint` at its centre hits it | false | true |
  | **trigger's `aria-expanded`** | **`"false"`** | **`"true"`** |

  So the `width > 0 && height > 0` visibility helper that nearly every locator in
  this guide leans on now reports a **closed** menu as open. The failure it
  produces is the nastiest kind: the extension that hit this went on clicking the
  parked row and *kept working*, just four times slower, with a silent dependency
  on a menu Notion no longer considers open.

  **The fix is `aria-expanded` on the control that opens the popup.** Notion
  maintains it correctly, it is semantic, and — see the warning below — it is the
  only candidate that does not have a second failure mode:

  ```js
  const expanded = (el) => !!el && el.getAttribute('aria-expanded') === 'true';

  // Gate every "is the row on screen?" question on the trigger, not the DOM.
  let item = triggers.some(expanded) ? menuItem() : null;

  if (!item) {
    for (const t of triggers) {
      if (expanded(t)) await dismiss(t);      // open, but not the menu we want
      click(t);
      item = await waitFor(() => (expanded(t) ? menuItem() : null), 2500);
      if (item) break;
      await dismiss(t);
    }
  }
  ```

  It also gives you a reliable dismissal condition, which `textContent` never
  did: wait for `!expanded(trigger)` rather than for the overlay to look empty.

- **⚠️⚠️ Do NOT reach for `Element.checkVisibility()` here — it breaks in hidden
  tabs.** The table above makes `checkVisibility({checkOpacity: true})` look like
  the obvious answer to the parking problem. It is, in a foreground tab. It was
  written, shipped and reverted inside half an hour, and this is the more
  valuable half of the finding:

  **Notion's popups animate in from `opacity: 0`, and CSS animations do not
  advance in a tab that is not visible.** In a tab with
  `document.visibilityState === "hidden"`, the opacity of a *genuinely open*
  menu stays 0 indefinitely. Measured: menu open, `aria-expanded="true"`, all ten
  rows laid out at real on-screen coordinates, `checkVisibility({checkOpacity:
  true})` **false on every one of them**, with the animated ancestor parked at
  `opacity: 0, transform: matrix(0.96, …)`.

  This bites any extension driven from a keyboard command or the service worker,
  because the tab you are told to drive is not reliably the tab in front —
  `chrome.windows.update({focused: true})` does not always win, and tabs in other
  windows are hidden by definition. A locator that only works in the foreground
  is a locator that fails exactly when the user is doing something else.

  Dropping `checkOpacity` doesn't rescue it: parking is not a `display` or
  `visibility` change, so `checkVisibilityCSS` alone cannot see it either. There
  is no configuration of `checkVisibility()` that answers this question. Use the
  ARIA state.

  Generalised, and worth carrying to every other Notion surface: **ask the
  control, not the popup.** Paint-derived signals (rects, opacity, hit-testing)
  answer "what would a user see right now", which is a different question from
  "what state is this widget in", and the two diverge in hidden tabs, during
  animations, and while something is parked.

### 5.3 Synthetic clicks

React ignores a bare `element.click()` in many cases. Escalate through a full
pointer sequence:

```
pointerover → pointerenter → pointermove → pointerdown → mousedown
→ focus → pointerup → mouseup → click
```

Dispatch with real coordinates from `getBoundingClientRect()`, `bubbles: true`,
and verify the expected effect appeared rather than assuming it did.

### 5.4 ⚠️ Notion's DOM lies about readiness

**The single most expensive bug in this codebase's history.** The topbar exists
and passes a visibility check *well before React attaches handlers to it*. A
perfectly good click dispatched at 1.6 s into a page load is silently swallowed —
no error, no effect.

Mitigations, all of them:

- **Settle** ~2.5 s after page-ready before the first interaction.
- **Retry with backoff** (`[1500, 4000, 9000]`). Never record a terminal failure
  on the first attempt.
- **Verify each step** by waiting for its expected effect, not by assuming.

- **⚠️ Make every rung of the ladder idempotent.** Retrying only helps if attempt
  N+1 starts from a state attempt N didn't poison, and the usual poisoner is a
  **toggle**. If a step opens something by clicking a control that also closes
  it, a retry that blindly re-clicks *undoes* the previous attempt — so every
  remaining rung fails the same way and the ladder can never recover. It looks
  exactly like a dead locator. Check for the effect before repeating the cause:

  ```js
  let item = findMenuItem();                  // did an earlier attempt open it?
  if (!item) {
    click(toggleControl);
    item = await waitFor(findMenuItem, 5000);
  }
  ```

  This is safe precisely because the overlay is empty at rest (5.2). Ask the
  same question of any step whose control is a toggle — sidebar collapse,
  disclosure triangles, filter chips.

- **Assert on ARIA state, not on rendered text.** `aria-selected="true"` and
  `aria-expanded="true"` are the real success conditions and cost nothing extra.
  Scraping for display text instead ties you to one language, and it breaks on
  empty states — a usage panel reading "No usage" is just as successfully open as
  one reading "71% used", but a `/% used/` check calls it a failure and burns the
  whole retry ladder before reporting a bug that doesn't exist.

**Timing, measured** (settings surface, warm client): a four-click chain
completes in **~0.7 s** when the target surface's bundle is already loaded and
**~4 s** on the first open after a page load, because these surfaces are lazily
chunked. Budget the second number for any first interaction, or your timeouts
will fire on a run that was about to succeed.

### 5.5 ⚠️ Rendering depends on viewport width

Notion renders a **Default**-mode margin comment as the same small count icon it
uses for **Minimal** mode when the viewport is too narrow to lay out the margin
column. Measured on one page, one setting, changing only window width:

| Viewport | Setting | Rendered |
|---|---|---|
| 1440px | Default | `.notion-margin-discussion-item` (expanded) |
| 1100px | Default | count icon |
| 1020px | Default | `role=button aria-label="1 comment"` |

The narrow-Default icon is byte-identical to the true Minimal icon. **No DOM
inspection can separate them.** The breakpoint sits between 1100 and 1150 px and
moves with the sidebar.

The general lesson: **before concluding that a DOM signal means a state, check
whether it also appears in some other state under a different layout.** Test at
several window widths.

### 5.6 Coexisting with Notion's UI

If you inject a panel rather than driving Notion's own controls:

- **Never steal focus, and never swallow a keystroke meant for Notion.** `/`
  opens Notion's slash menu inside any contenteditable and `Esc` closes Notion's
  overlays, so both are live ammunition. Gate every shortcut on "is the user
  typing in the page?", and only `preventDefault()` on a path that actually did
  something:

  ```js
  function typingInPage() {
    const a = document.activeElement;
    if (!a || a === document.body || a === document.documentElement) return false;
    if (myPanel.contains(a)) return false;
    return a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' ||
           a.tagName === 'SELECT' || a.isContentEditable;
  }
  ```

- **"Does my panel have focus?" usually cannot be answered by
  `document.activeElement`** — a panel that must not steal focus doesn't have it.
  Track a flag set from a capture-phase `mousedown` instead.

- **A synchronous action with no visual feedback reads as broken.** A rescan
  button set `'scanning…'` and finished in the same tick, so the browser never
  painted it: the button looked completely dead while working perfectly. Show the
  *result* for a second or two rather than a transient "working" state.

- **Any message you want to persist must survive your own re-render.** If
  `render()` rebuilds the status line from current state, a result written
  directly into the DOM is wiped by the next render — including one fired by a
  delayed re-scan seconds later. Keep sticky text in state, not in the node.

- **Dark Reader.** Josh runs it. A panel that commits to its own dark palette
  came through untouched, but `data-darkreader-ignore` on the root nodes plus
  `color-scheme: dark` is cheap insurance.

---

## Part 6 — Lifecycle

### 6.1 Navigation

Notion is a SPA; the content script loads once and survives every in-app
navigation.

**Do not patch `history.pushState`.** From the isolated world you'd be patching a
different function object than the page's, so it never fires. From MAIN world it
works, but polling is simpler and adequate.

```js
let lastUrl = location.href;
setInterval(() => {
  if (location.href !== lastUrl) { lastUrl = location.href; onNavigate(location.href); }
}, 400);
window.addEventListener('popstate', () => onNavigate(location.href));
```

### 6.2 Double injection and orphaning

```js
if (window.__yourprefixInstalled) { /* stand down silently */ }
else { window.__yourprefixInstalled = true; /* … */ }
```

In ISOLATED world you can also detect being orphaned by an extension reload:

```js
const isOrphaned = () => { try { return !chrome.runtime?.id; } catch (e) { return true; } };
```

When true, tear down — otherwise the old script spams `Extension context
invalidated`. **In MAIN world this is unavailable**; the sentinel is all you get.

**Reloading an unpacked extension does not update already-open tabs.** Reload the
extension, *then* the tab. A tool that "stopped working mid-test" is almost
always this.

**Print a build number on boot.** One constant, bumped on every change, logged at
startup and mirrored into the DOM (7.1). `installed v1.0.4` in the console is
instant proof that a tab actually picked up new code. Without it the
reload-order mistake above is silent, and you spend a whole test round
diagnosing a bug you already fixed.

### 6.3 Hidden tabs

`document.hidden` is true for background tabs, minimized windows, fully occluded
windows, and windows on an inactive macOS Space. Chrome throttles hard: `rAF`
stops, timers clamp to ~1 s. Don't burn a time budget while hidden — pause it and
resume on `visibilitychange`.

### 6.4 Trusted Types

**Enforced — confirmed on 2026-08-04, not assumed** (`window.trustedTypes &&
window.trustedTypes.defaultPolicy !== undefined` is true on `app.notion.com`).
Build every node with `createElement` + `textContent` + `appendChild`. **No
`innerHTML`, `insertAdjacentHTML`, `document.write`, or injected `<script>`
tags** — including for `<style>` blocks, where `style.textContent = css` is the
correct form.

For stylesheets there is a strictly safer form still. An injected `<style>`
element is subject to the page's `style-src` CSP; a **constructable stylesheet is
pure CSSOM and cannot be blocked by CSP at all**:

```js
try {
  const sheet = new CSSStyleSheet();
  sheet.replaceSync(CSS);
  document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
} catch (e) {
  const el = document.createElement('style');
  el.textContent = CSS;                    // Trusted-Types-safe fallback
  (document.head || document.documentElement).appendChild(el);
}
```

Setting geometry through `el.style.foo = …` is likewise CSSOM and equally safe —
only the `style` **attribute** parsed from markup is CSP-restricted. Notion was
never observed blocking inline styles, so this is precaution rather than a fix
for a known failure; it costs three lines.

The constructable-stylesheet path was exercised directly against Notion's CSP on
2026-08-04 and applied cleanly, including from the **page's own world**, which is
the stricter test — a content script gets more latitude than the page does. So
the `try` branch is the one that actually runs; the `<style>` fallback is there
for old surfaces, not because it is needed today.

---

## Part 7 — Debugging

### 7.1 ⚠️ Content-script logs are invisible from outside

Content scripts log into an **isolated console context**. Page JavaScript, CDP
console capture, and automation harnesses cannot read them. An absent log line
proves *nothing* about whether your script ran. This cost a full session once.

**Always mirror recent events into the DOM:**

```js
const ring = [];
const mirror = parts => {
  ring.push(`+${Math.round(performance.now())}ms ${parts.join(' ')}`);
  while (ring.length > 20) ring.shift();
  document.documentElement.dataset.yourprefixLog = ring.join(' || ');
};
```

Then anyone — you, Josh, a script — can read
`document.documentElement.dataset.yourprefixLog`. This turns "it does nothing"
into a specific, recorded failure roughly every time.

In DevTools you can also switch the console's context dropdown from `top` to the
extension's world, but the DOM mirror is faster and works everywhere.

### 7.2 ⚠️ External probes report wrong timings

An injected probe (`Runtime.evaluate`, an automation tool) isn't scheduled while
the renderer is busy booting Notion, so it reports everything as appearing at the
moment *it* finally ran. During one session, external probes claimed
`.notion-page-content` first appeared at 8.3 s, 9.1 s and 18.7 s. The extension's
own in-page log said **99 ms and 365 ms** for the same loads.

**Only trust timings measured from inside the page.** An entire wrong hypothesis
was built on those external numbers.

**A hidden tab will also blow the probe's own timeout, and lie about why.**
Chrome clamps timers to ~1 s in a background tab (6.3), so a poll written as
`setTimeout(…, 120)` runs at roughly one-eighth speed. A probe that completes in
~8 s foregrounded ran past **45 s** hidden and was killed with *"the renderer may
be frozen or unresponsive"* — it was neither; it was throttled. Foreground the
tab before driving it, or keep each probe short.

Either way, **write every wait against a `Date.now()` deadline rather than a tick
count**, in probes and in shipped code alike. `for (let i = 0; i < 40; i++)` with
a 120 ms sleep silently becomes an eight-second budget instead of five when the
tab goes to the background; a deadline stays honest.

### 7.3 DevTools quirks worth knowing

- **`copy()` does not work inside async callbacks.** `copy` is a command-line API
  binding available only during synchronous evaluation. Inside a `.then()` or
  `.finally()` it throws `copy is not defined`. Stash the string on `window` and
  have the user run `copy(__whatever)` on its own line.
- **`$0`** is the currently inspected element. Right-click → Inspect, then
  operate on `$0` — this is the fastest way to hand you a DOM node.
- **Network filter box** takes plain substrings and `-term` to exclude.
- **The red record toggle** freezes the Network log — invaluable, because
  `syncRecordValuesSpaceInitial` floods it with 2–4 MB entries.
- **Right-click a request → Copy → Copy as fetch** captures method, URL, headers
  and body in one paste. Prefer it over "Copy as cURL", which includes the
  `cookie` header. Tell the user to delete any `"cookie":` line before pasting.
- Notion logs its own `ClientError` lines. Not yours.

### 7.4 Symptom table

| Symptom | First suspect |
|---|---|
| Nothing happens, no error | Click swallowed pre-hydration (5.4). Raise settle time before touching locators |
| Worked for weeks, now fails at the very first step | A locator pinned to screen position; Notion moved the control (5.1) |
| "A menu is open" is true forever after the first run | Dismissed popups stay mounted; gate on the trigger's `aria-expanded` (5.2) |
| Flow works but is several times slower than it was | Same — you are clicking a parked row instead of opening the real menu (5.2) |
| Works when you watch it, fails when you don't | An entry animation stuck at `opacity: 0` in a hidden tab, plus an opacity-aware visibility test (5.2) |
| Enumeration returns records, all fields undefined | Lazy fields (3.4) — use `getKeyValue` |
| Enumeration returns nothing | Wrong method signature; read the minified source |
| Delete "does nothing", but Notion's own UI updated | Cache lags the write (3.7). Don't re-read straight after a `200` |
| Doing it twice works, once doesn't | Same — the cache caught up in between (3.7) |
| Restore inverted: back in Notion, gone from your list | Same (3.7) |
| Counts disagree between cache and DOM | `role: "none"` records are skipped (3.2), or sidebar virtualization if `cache > DOM` |
| A button looks dead but its work happened | Synchronous action never painted its "working" state (5.6) |
| Works wide, fails narrow | Viewport-dependent rendering (5.5) |
| "Menu is always open" | Sidebar's always-visible `role="menu"` (5.2) |
| Locator times out while the thing is plainly on screen | Over-tight ancestor in the selector — popup roles are unstable (5.2) |
| A step "fails" but the screen looks right | Confirming by scraping display text instead of ARIA state (5.4) |
| Every rung of the retry ladder fails identically | A toggle control being re-clicked, undoing the last attempt (5.4) |
| A grep for the endpoint name finds nothing | Names are built from a template, not literals (8). Watch the network instead |
| A value is on screen but in no record and no response | It exists only as component props (3.8) |
| A setting has no DOM representation anywhere | Look at `format.*` on the page block — plain `fetch`, no MAIN world (3.9) |
| An API-derived check is confidently wrong on some pages | Unreadable record returned 200 + a stub; you defaulted on an absent field (3.9) |
| Two "usage" numbers disagree wildly | They are different quotas — check what the UI actually labels them (3.8) |
| Probe killed as "renderer unresponsive" | Background-tab timer clamping, not a hang (7.2) |
| Stopped working mid-session | Extension reloaded but tab wasn't (6.2) |
| Works in one tab, not another | `localStorage` flag set globally (it is per-origin) |
| `Extension context invalidated` spam | Orphaned script; add the `chrome.runtime?.id` guard |

---

## Part 8 — Discovery methodology

How to work out a mechanism Notion doesn't document. This sequence found the
delete endpoint in about four minutes.

**1. Make the action happen once, by hand, and watch the write.**
Network tab → Fetch/XHR → filter `saveTransactionsFanout` → clear → perform the
action → exactly one row appears. **Copy as fetch.** The `debug.userAction`
string in the body names the internal action, which is a strong search term for
everything related.

**2. Replay it.** Change the id, fire it from the console. If it works, you have
the write path and can stop reverse-engineering the UI entirely.

**3. Find the read path.** Reading is usually *not* a matching endpoint — it's the
record cache. Get a cache handle (3.1), enumerate the table (3.2), remember lazy
fields (3.4).

**4. When a method's signature is unknown, read it.** Minification preserves
destructuring:

```js
String(cache.forEachRecordOfTable)
// forEachRecordOfTable({userId:e,table:t,fn:r}){…}
```

That one line replaced four rounds of guessing. **Read the source before guessing
a signature.**

**⚠️ But do not go looking for *endpoint names* in the bundles — they are not
there.** Notion builds request URLs as `` `/api/v3/${name}` `` from a generated
client, so the names never appear as literals. Grepping all 758 loaded chunks
(39 MB) for `api/v3/<something>` returned **zero** matches — including for
`getAIUsageEligibilityV2`, an endpoint that had just been watched flying past in
the Network tab. This looks exactly like "the feature doesn't exist" and isn't.

What *is* greppable is **prop, field and i18n key names**, which survive
minification as object keys and string literals. So the order is: **network tab
for endpoint names, bundles for shapes.** Grepping the bundles for a field name
you already have tells you the states you haven't seen yet — one search on
`resetsInMs` surfaced `within_limit`, `rate_limited`, `not_applicable` and
`retryAfterSeconds`, i.e. the whole type union, from a UI that was only ever
showing one of them.

```js
// Grep every loaded chunk. They come from the HTTP cache, so this is fast.
const NEEDLE = 'resetsInMs';
const urls = performance.getEntriesByType('resource').map(e => e.name)
  .filter(n => /\.js(\?|$)/.test(n) && n.startsWith(location.origin));
const hits = [];
for (const u of urls) {
  const t = await fetch(u).then(r => r.text()).catch(() => '');
  if (!t.includes(NEEDLE)) continue;
  const i = t.indexOf(NEEDLE);
  hits.push({ file: u.split('/').pop(), ctx: t.slice(i - 700, i + 400) });
}
hits;
```

**Lazily-chunked surfaces aren't loaded until you open them**, so run this
*after* clicking to the screen you care about — a first pass that finds nothing
may only mean the code isn't downloaded yet.

**5. Probe permissions empirically.** Remove one header at a time and re-fire.
Use a *no-op* write (set a field to the value it already has) so probes can't
damage anything — but remember the result is only strictly proven for no-ops.

**6. Test the negative case.** "Does this still work after a reload?" and "does
this appear in a state I don't expect?" are where the silent bugs live.

**Guard rails while probing:** operate only on records whose title matches a
throwaway prefix (`zz`), and refuse anything else in the probe itself. Both
projects used this and neither ever damaged real data.

---

## Part 9 — Verifying without Notion

Part 8 is how you learn what Notion does. This is the other half: how to check
that *your code* does the right thing before spending the user's real data and
real attention on it.

The Chat Sweeper build verified chunking, the retry ladder, the exact request
payload and every panel interaction against a **stub**, before Josh loaded the
extension once. It repeatedly caught bugs one step earlier than he would have.

### 9.1 Stub the record cache

Everything in Part 3 is plain JavaScript, so it can be faked in a static HTML
page: a fiber expando pointing at an object carrying `inMemoryRecordCache` and
`userId`, plus records whose fields are **lazy behind `getKeyValue`** exactly as
in 3.4. Reproducing the trap is the point — a stub with plain properties would
let 3.4 bugs through.

```js
const lazy = { data: { title }, alive, created_time: t, updated_time: t };
const record = {
  id, table: 'thread',
  data: undefined, alive: undefined,       // lazy on purpose — the 3.4 trap
  getKeyValue(k) { return lazy[k]; }
};
const store = {
  userId: 'user-mock', model: { space_id: 'space-mock' },
  inMemoryRecordCache: {
    forEachRecordOfTable({ userId, table, fn }) {
      if (table === 'thread') records.forEach(model => fn({ model, role: 'editor' }));
    }
  }
};
const host = document.createElement('div');
host.__reactFiber$mock = { memoizedProps: { chatStore: store }, return: null };
```

Add sibling rows carrying `{ memoizedProps: { threadStore: { id } } }` and your
DOM cross-check has something to compare against as well. Include a row with no
such prop to stand in for an agent, and confirm it never reaches your list.

### 9.2 Stub `fetch` *before* your script loads

Put the capture stub in a `<script>` **above** your content script, so it becomes
the `origFetch` your code captures at startup. Now you can assert on the exact
body you would have sent, and answer `200` without a server:

```js
window.__sent = [];
const real = window.fetch.bind(window);
window.fetch = function (input, init) {
  const url = typeof input === 'string' ? input : (input && input.url) || '';
  if (url.includes('/api/v3/')) {
    window.__sent.push({ url, init, body: init && JSON.parse(init.body) });
    return Promise.resolve(new Response('{}', { status: 200 }));
  }
  return real(input, init);
};
```

This is what confirmed that 11 selected records became two requests of 10 and 1
operations, each with fresh UUIDs and the right `pointer` and `args` — none of
which is visible from the UI. Fire a fake Notion API call through the same stub
and you also exercise the header-learning wrapper from 4.3.

### 9.3 Reproduce the bug in the stub before fixing it

When the cache-lag bug (3.7) turned up, the stub was changed to apply writes to
the fake sidebar immediately and to the fake record **1500 ms later**. That
converted a confusing live symptom into a repeatable one, and let the fix be
checked at 300 ms, 1.4 s and 3.2 s after the write. Far better than iterating
against the real app, where each cycle costs the user a reload and a screenshot.

### 9.4 Test the shipped source, not a paraphrase

For tricky pure logic, slice the function text out of the real file and evaluate
it, so the test cannot drift from what ships:

```js
const SRC = fs.readFileSync('content.js', 'utf8');
const a = SRC.indexOf('function rangeClick('), b = SRC.indexOf('\n  }\n', a);
const rangeClick = new Function(SRC.slice(a, b + 4) + '; return rangeClick;')();
```

Selection ranges, retry ladders and relative-time formatting all repay this. Note
in the maintenance log that renaming the function breaks the extraction.

### 9.5 ⚠️ What a stub cannot tell you

**A stub written from a spec validates your code against the spec's description
of Notion — not against Notion.** Wherever the spec is wrong, the stub is wrong
in the same direction and cheerfully agrees with itself. It is a consistency
check, not a truth check. Josh made this point during the build and was right.

So always name what it structurally cannot cover, and treat those as unverified
until the user confirms them live:

- whether the fiber walk finds the real store
- whether `getKeyValue` still resolves real fields
- extensions that reshape the page (Dark Reader)
- real counts, real titles, real latency
- whether the write is *accepted* — a stub returns `200` for anything

Those five were the open list at Chat Sweeper's first checkpoint. All of them
closed on a single screenshot from the user, which is the point: state the gap
plainly and it gets closed in one round instead of being quietly assumed.

---

## Part 10 — Working with Josh

He is patient and precise, follows instructions exactly, and will run as many
console snippets as you need. He is not a DevTools person and should not be asked
to interpret anything.

**Do:**

- One self-contained snippet per message, ending with instructions to run
  `copy(__something)` and paste back.
- Say what the snippet is *for* in one sentence before the code.
- Give exact clicks: which tab, which button, what to type.
- State plainly whether a snippet is read-only or will change something.
- Ask him to rename throwaway records to `zztest1`, `zztest2`, `zztest3` before
  any destructive testing, and guard your snippets on that prefix.
- Prototype UI in the console before writing it into the extension. A console
  script runs in the same JavaScript world a MAIN-world content script does, so
  what works there works there. This let the entire Chat Sweeper panel be built
  and approved before a single extension file existed.
- Report what a test actually proved, and say plainly when it proved nothing. At
  one checkpoint the cross-check had been *skipped* rather than passed, because
  the Chat tab was closed; an absent warning is not a pass, and saying so cost
  one message and saved a false conclusion.
- Expect him to push back on interaction design with concrete reasoning, and take
  it seriously — he overruled a shift-click model that had been built to match a
  written acceptance test, and he was right. Then record the resolution *and the
  reasoning* in the maintenance log so a later session doesn't quietly revert it.

**Don't:**

- Ask him to "find the request" or "grab the selector."
- Send several probes at once.
- Use `copy()` inside async code (7.3).
- Declare something impossible after one failed probe — several apparent dead
  ends in the Chat Sweeper build were wrong call signatures, not absent features.

He has a limited Claude Code budget and a larger chat budget, so **resolve as
much as possible in chat before handing anything to Claude Code.** Verified code
in a spec is worth far more than instructions to go discover it.

---

## Part 11 — Safety rules for destructive extensions

Both projects landed on the same set. Adopt them unless there's a reason not to.

1. **Target one table, explicitly.** If a target didn't come from your own
   enumerator, refuse it.
2. **Dry-run mode, default on** until the flow is verified end to end. It
   enumerates, logs what it *would* do, and sends zero requests.
3. **No destructive action without an explicit click** on a control labelled with
   the count. Never on page load.
4. **Write the undo record before attempting the change.** If the write fails,
   don't start.
5. **Confirmation shows names, not just a count.** A count can't reveal a
   mis-selection; a list can.
6. **A cap plus a second confirmation** above some threshold.
7. **Nothing leaves the browser.** No analytics, no remote endpoints.
8. **Never present a silently wrong list.** If two enumeration sources disagree,
   show a warning with both numbers.
9. **Be honest about recovery limits in the README.** If records deleted before
   install are unrecoverable, say so plainly rather than implying otherwise.
10. **Label irreversibility accurately.** An action that discards your own record
    but changes nothing server-side is not "delete permanently" — say what it
    actually does. And when exactly one action in the tool is genuinely
    unrecoverable, make its confirmation visibly blunter than all the others.
11. **Show the mode.** While a safety rail is in force — dry run, or a temporary
    low cap during staged rollout — put it on screen in a colour that can't be
    mistaken for the armed state. Chat Sweeper used a blue "DRY RUN" bar and a
    red "LIVE — capped at 1 per run" bar; neither leaves any doubt, and the bar
    disappearing is itself the signal that the rails are off.

---

## Part 12 — Trap index

Everything that cost real time, in one list.

| # | Trap | Part |
|---|---|---|
| 1 | Content-script logs invisible outside the isolated world | 7.1 |
| 2 | External timing probes report wrong numbers | 7.2 |
| 3 | DOM ready ≠ React ready; early clicks silently swallowed | 5.4 |
| 4 | Cached fields are lazy; `model.data` is always undefined | 3.4 |
| 5 | Method signatures are option objects — read the minified source | 8 |
| 6 | Dead records vanish from the cache on reload | 3.6 |
| 7 | Viewport width changes what state the DOM appears to be in | 5.5 |
| 8 | Sidebar has an always-visible `role="menu"` outside the overlay | 5.2 |
| 9 | Menu labels duplicated as page-header buttons | 5.2 |
| 10 | `copy()` unavailable in async callbacks | 7.3 |
| 11 | `pushState` patching never fires from the isolated world | 6.1 |
| 12 | Extension reload orphans scripts in open tabs | 6.2 |
| 13 | `localStorage` is per-origin, not per-tab | 6.3 |
| 14 | Peek previews put the id in the query, not the path | 1 |
| 15 | Hashed atomic CSS classes rot without notice | 5.1 |
| 16 | `role: "none"` records are skipped by `forEachRecordOfTable` | 3.2 |
| 17 | MAIN world has no `chrome.*` at all | 2 |
| 18 | Trusted Types blocks every HTML-string sink | 6.4 |
| 19 | Permission probes on no-ops don't prove destructive permissions | 4.3 |
| 20 | Soft-deleted ≠ trashed; it may not appear in Notion's Trash | 4.5 |
| 21 | The record cache lags your own confirmed writes by ~1 s | 3.7 |
| 22 | Sidebar virtualization makes `cache > DOM` the normal state | 3.2 |
| 23 | `updated_time` is not a deletion time | 4.5 |
| 24 | Restoring `alive` does not restore other state (e.g. pinning) | 4.5 |
| 25 | Notion deletes empty records on its own; your journal will show it | 4.5 |
| 26 | A synchronous UI action with no feedback looks broken | 5.6 |
| 27 | `/` and `Esc` belong to Notion — gate every shortcut | 5.6 |
| 28 | A re-render wipes status text written straight into the DOM | 5.6 |
| 29 | A stub built from a spec can only ever confirm the spec | 9.5 |
| 30 | Overlay popup container role is unstable — never require `role="menu"` as an ancestor | 5.2 |
| 31 | A toggle control makes a naive retry undo the previous attempt, so the ladder never recovers | 5.4 |
| 32 | Confirming a step by scraping display text breaks on empty states and other languages | 5.4 |
| 33 | Endpoint names are not literals in the bundles — URLs are built from a template | 8 |
| 34 | Lazily-chunked surfaces aren't in the bundles until you open them | 8 |
| 35 | Some displayed values exist only as component props — no record, no endpoint | 3.8 |
| 36 | The easily-fetched neighbouring metric is usually a *different* quota | 3.8 |
| 37 | Modal surfaces have no URL; you cannot deep-link to a settings section | 1 |
| 38 | Tick-counted waits silently shrink under background-tab throttling — use deadlines | 7.2 |
| 39 | A locator pinned to screen position dies the day Notion moves the control — rects are for disambiguation, never identity | 5.1 |
| 40 | A dismissed popup stays mounted with real layout boxes; a rect-only `visible()` calls a closed menu open — ask the trigger's `aria-expanded` | 5.2 |
| 41 | The overlay is **no longer** empty at rest — `textContent === ''` is a stale test | 5.2 |
| 42 | `checkVisibility({checkOpacity})` looks like the fix for 40 and is a trap: entry animations never advance in a hidden tab, so an open menu reads as invisible forever | 5.2 |
| 43 | Off-screen ≠ hidden: a collapsed sidebar's controls are laid out at negative coordinates and synthetic clicks on them still work | 5.2 |
| 44 | Notion's `⌘,` does not open Settings from a synthetic KeyboardEvent — don't design around it | 5.6 |
| 45 | `/api/v3/syncRecordValues` answers "can't read that" with **200** and a `{role}` stub — an absent field then looks like a legitimate default | 3.9 |
| 46 | Page settings are on the block record and reachable by plain `fetch` — check there before committing to a MAIN-world script | 3.9 |

---

## Appendix — starter manifest

MAIN world plus bridge, for an extension that reads Notion state and needs a
toolbar popup.

```json
{
  "manifest_version": 3,
  "name": "Your Notion Extension",
  "version": "1.0.0",
  "description": "…",
  "host_permissions": ["https://app.notion.com/*", "https://www.notion.so/*"],
  "permissions": ["storage"],
  "action": { "default_popup": "popup.html" },
  "commands": {
    "toggle-panel": {
      "suggested_key": { "default": "Ctrl+Shift+K", "mac": "Command+Shift+K" },
      "description": "Open or close the panel"
    }
  },
  "background": { "service_worker": "background.js" },
  "content_scripts": [
    { "matches": ["https://app.notion.com/*", "https://www.notion.so/*"],
      "js": ["bridge.js"], "run_at": "document_idle", "world": "ISOLATED" },
    { "matches": ["https://app.notion.com/*", "https://www.notion.so/*"],
      "js": ["content.js"], "run_at": "document_idle", "world": "MAIN" }
  ]
}
```

For a pure DOM-automation extension, drop `bridge.js`, the popup and the
commands, and run a single content script with no `world` key (defaults to
ISOLATED).

---

*Verified 2026-08-04 against Notion client `23.13.20260803.1816`, Chrome 150,
macOS; partially re-verified the same day against `23.13.20260804.1857` (see the
note under "Verify before you build" for exactly which parts). Sources: Notion
Minimal Comments (2026-07), Notion Chat Sweeper (2026-08, discovery and build)
and Notion AI Usage (2026-08, discovery and build). Re-run Part 0 before trusting
any of it.*
