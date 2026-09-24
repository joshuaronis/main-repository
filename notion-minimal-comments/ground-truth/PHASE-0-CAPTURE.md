# Phase 0 — ground-truth capture (REQUIRED before the extension can act)

Run each snippet in DevTools **on a real logged-in Notion page** and paste the
output back (or save it into a file here, e.g. `A-topbar.txt`, `B-menu.txt`).
The extension ships **inert**: its detector locators are empty, so it opens no
menus and changes nothing until these are filled into `CONFIG.locators` in
`content.js`.

Use a **standalone page (not a database row) that has at least one inline
comment**, unless a step says otherwise. Most snippets `copy(...)` to the
clipboard. If any prints `MISS`, the class name changed — Inspect the element
directly and paste the reality.

---

## A. Topbar + `•••` button
```js
copy(document.querySelector('.notion-topbar')?.outerHTML
  ?? document.querySelector('[class*="topbar"]')?.outerHTML ?? 'MISS: topbar');
```
Then Inspect the `•••` button and paste its `outerHTML` + its parent.
**Report:** tag, `aria-label`, `role`, class(es); is it reliably the **last**
`[role="button"]` in the topbar actions cluster?

## B. `•••` menu contents
Click `•••`, then:
```js
copy([...document.querySelectorAll('[role="menuitem"],[role="menu"] [role="button"],[role="menu"] div')]
  .map(e => `${e.getAttribute('role')||''} | ${(e.textContent||'').trim().slice(0,60)}`)
  .filter(s => s.split('|')[1]?.trim()).slice(0,120).join('\n'));
```
```js
copy((document.querySelector('.notion-overlay-container')
  ?? [...document.querySelectorAll('div')].find(d => /overlay/i.test(d.className)))
  ?.outerHTML?.slice(0,60000) ?? 'MISS: overlay');
```
**Answer:** is there an "Inline comments" row **directly**, or only "Customize
page" to click first?

## C. Inline-comments control + options
With the row visible, Inspect the clickable value control ("Default"/"Minimal" +
chevron); paste its `outerHTML` + the row container. Then click it to open the
Default/Minimal chooser and dump the overlay again (snippet from B).
**Identify:** the "Minimal" option element, and which element carries the
selected/checkmark state. Does the chooser open on click or on hover?

## D. DEFAULT-mode inline comment rendering
On a Default page scrolled to a visible inline comment, paste the smallest
wrapper of that preview (+1–2 ancestors).

## E. MINIMAL-mode rendering
Same on a Minimal page (the margin count icon).

## F. Mode signal hunt (critical for long virtualized pages)
On a Default page **and** again on a Minimal page, run and compare:
```js
const c = document.querySelector('.notion-page-content') || document.body;
copy([...c.querySelectorAll('*')].slice(0,4000)
  .flatMap(e => [...e.attributes].map(a => `${a.name}=${a.value}`.slice(0,80)))
  .filter(s => /comment|discussion|inline|minimal/i.test(s))
  .filter((v,i,a)=>a.indexOf(v)===i).join('\n') || 'no comment-ish attributes found');
```
If a stable attribute/class differs by **mode independent of comment presence**,
that's the preferred detector (`CONFIG.locators.modeSignal` + `readModeFromSignal`).

## G. Inline vs page-level comments
Capture a page whose only comment is a **page discussion** (top-of-page), and
one with a **resolved** comment. Paste how each renders, so the detector keys on
inline previews only and ignores those.

## H. Overlay vs React root
```js
const ov = document.querySelector('.notion-overlay-container')
  ?? [...document.querySelectorAll('div')].find(d=>/overlay/i.test(d.className));
const root = document.querySelector('#notion-app') ?? document.body.firstElementChild;
copy(`overlay parent: ${ov?.parentElement?.id||ov?.parentElement?.className}\n`
   +`root: ${root?.id||root?.className}\noverlay inside root? ${root?.contains(ov)}`);
```

## I. Page-content + top-document sanity
```js
copy(`content in top doc: ${!!document.querySelector('.notion-page-content, [class*="page-content"]')}\n`
   +`frames: ${window.top===window.self}`);
```

---

### What must be filled before the extension may act
- `moreButton`, `inlineRow`, `valueControl`, `minimalOption` locators — each
  backed by captured HTML (A / B / C).
- The detector: `modeSignal` + `readModeFromSignal` (from F, preferred), **or**
  `defaultCommentPreview` + `minimalCommentIcon` (D / E, scoped inline-only per G).
- The direct-row-vs-Customize-page answer (B).
- `shieldSelector` confirmed against the real overlay class (H).

Do **not** guess the detector. If F/D/E can't be captured cleanly, say so and
we'll get better captures rather than opening the menu on every page.
