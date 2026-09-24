/* Notion AI Usage — content.js  (ISOLATED world)
 *
 * Drives Notion's own chrome: workspace switcher → Settings → Notion AI →
 * Usage. That is pure DOM automation, so the isolated world is enough (field
 * guide Part 2) and chrome.* is available directly — no MAIN-world script and
 * no bridge.js.
 *
 * Nothing here writes to Notion. Every action is a click Josh could have made
 * himself, and the only state we touch is which settings tab is showing.
 *
 * Shortcut handling lives in background.js on purpose: we never add a keydown
 * listener to the page, so there is no way to swallow a keystroke Notion wanted
 * (field guide 5.6 — `/` and `Esc` are live ammunition inside Notion).
 */

(() => {
  'use strict';

  const BUILD = '1.1.0';

  // 6.2 — a second injection stands down silently rather than double-driving
  // the UI. Reloading the extension does NOT update already-open tabs; the
  // build number below is how you tell whether a tab picked up new code.
  if (window.__nauInstalled) return;
  window.__nauInstalled = true;

  /* ------------------------------------------------------------------ *
   * Logging
   *
   * 7.1 — content-script logs live in an isolated console context that
   * nothing outside can read. Mirror them into the DOM so "it did nothing"
   * can always be turned into a specific recorded failure:
   *
   *   document.documentElement.dataset.nauLog
   * ------------------------------------------------------------------ */
  const ring = [];
  function log(...parts) {
    ring.push('+' + Math.round(performance.now()) + 'ms ' + parts.join(' '));
    while (ring.length > 24) ring.shift();
    try { document.documentElement.dataset.nauLog = ring.join(' || '); } catch (e) {}
    try { console.log('[notion-ai-usage]', ...parts); } catch (e) {}
  }

  // 6.2 — an orphaned script (extension reloaded, tab not) should go quiet
  // instead of spamming "Extension context invalidated".
  const isOrphaned = () => {
    try { return !chrome.runtime || !chrome.runtime.id; } catch (e) { return true; }
  };

  /* ------------------------------------------------------------------ *
   * DOM helpers
   * ------------------------------------------------------------------ */

  const text = (el) => (el && el.textContent ? el.textContent.trim() : '');

  // Rect-only, on purpose.
  //
  // `Element.checkVisibility({checkOpacity:true})` was tried here first, to see
  // through the parked popups described at expanded() below, and it works — in
  // a foreground tab. It is a trap in a background one: Notion's popups animate
  // in from `opacity: 0`, CSS animations do not advance in a hidden tab, so the
  // opacity of a *genuinely open* menu stays 0 indefinitely and every locator
  // built on it fails. Measured 2026-09-02 in a tab with
  // `document.visibilityState === "hidden"`: menu open, `aria-expanded="true"`,
  // rows laid out at real coordinates, `checkVisibility({checkOpacity:true})`
  // false on all ten of them.
  //
  // That matters because this extension can be asked to drive a tab that is not
  // in front. Openness is answered by ARIA instead — see expanded().
  function visible(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  // 5.3 — React ignores a bare .click() in many cases. Escalate through the
  // full pointer sequence with real coordinates.
  function click(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const opts = {
      bubbles: true, cancelable: true, composed: true, view: window,
      clientX: r.left + r.width / 2, clientY: r.top + r.height / 2,
      button: 0, buttons: 1, pointerId: 1, isPrimary: true, pointerType: 'mouse'
    };
    const fire = (type) => {
      const Ctor = type.startsWith('pointer') ? PointerEvent : MouseEvent;
      el.dispatchEvent(new Ctor(type, opts));
    };
    ['pointerover', 'pointerenter', 'pointermove', 'pointerdown', 'mousedown'].forEach(fire);
    try { el.focus && el.focus({ preventScroll: true }); } catch (e) {}
    ['pointerup', 'mouseup', 'click'].forEach(fire);
    return true;
  }

  // Deadline-based rather than tick-based: background tabs clamp timers to
  // ~1s (6.3), and a tick-counting loop would silently shorten its own budget.
  async function waitFor(fn, ms, label) {
    const deadline = Date.now() + ms;
    for (;;) {
      let v = null;
      try { v = fn(); } catch (e) { v = null; }
      if (v) return v;
      if (Date.now() >= deadline) { log('timeout', label || ''); return null; }
      await new Promise((r) => setTimeout(r, 120));
    }
  }

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  /* ------------------------------------------------------------------ *
   * Locators
   *
   * 5.1 — at least two strategies per target, the last one structural.
   * Never key on a hashed atomic class; those rot without notice.
   * ------------------------------------------------------------------ */

  // The settings modal. `aria-label` is the readable handle; the structural
  // fallback is "a modal dialog that contains the settings left-nav".
  function settingsDialog() {
    const byLabel = document.querySelector('[role="dialog"][aria-label="Settings & members"]');
    if (visible(byLabel)) return byLabel;
    for (const d of document.querySelectorAll('[role="dialog"][aria-modal="true"]')) {
      if (!visible(d)) continue;
      if (d.querySelector('[id^="settings-tab-"], [data-testid^="settings-tab-"]')) return d;
    }
    return null;
  }

  // The workspace switcher.
  //
  // 5.1 — POSITION IS NOT A LOCATOR. This function used to require
  // `top < 200`, because the switcher sat at the top of the sidebar. In
  // client `23.13.20260903.0022` Notion moved it to the *bottom* (top ≈ 770 on
  // an 805px viewport) and put search / inbox / new-page at the top instead.
  // The filter then matched nothing and every run died at step one. Do not
  // reintroduce a coordinate test here; rank and verify instead.
  //
  // Returns a ranked *list*, because the structural fallback cannot tell the
  // switcher from the page tree's own "More" row with certainty. openSettings()
  // picks the winner by outcome — did a "Settings" row actually appear? — which
  // is the only test that stays true across a rename.
  function workspaceSwitchers() {
    const out = [];
    const push = (el) => { if (el && out.indexOf(el) === -1) out.push(el); };

    // 1. Semantic class, unique document-wide. Same family as
    //    .notion-sidebar-container / .notion-overlay-container — not a hashed
    //    atomic class, so it is safe to key on.
    //
    //    Visibility is deliberately NOT required. With the sidebar collapsed
    //    the switcher is parked off-screen (left: -242) rather than unmounted,
    //    and a synthetic click on it still opens the popup — verified
    //    2026-09-02. That is what lets the shortcut work without expanding a
    //    sidebar the user chose to close; the old code could not run at all in
    //    that state.
    document.querySelectorAll('.notion-sidebar-switcher').forEach(push);

    const sb = document.querySelector('.notion-sidebar-container') ||
               document.querySelector('[class*="notion-sidebar"]');
    if (!sb) return out;

    // 2. Structural: a wide, unlabelled popup trigger inside the sidebar that
    //    is not part of the page tree. Measured on the live app, exactly two
    //    elements fit that description — the switcher (194×28) and the recents
    //    "More" row (254×30) — which is why the outliner exclusion is here and
    //    why the caller still verifies. Everything else in the sidebar that
    //    opens a dialog carries an aria-label ("New page", "Help, contact,
    //    more…") or is a 0×0 placeholder.
    [...sb.querySelectorAll('[role="button"][aria-haspopup="dialog"]')]
      .filter((el) => visible(el))
      .filter((el) => !el.getAttribute('aria-label'))
      .filter((el) => el.getBoundingClientRect().width > 100)
      .filter((el) => !el.closest('[class*="notion-outliner"]'))
      .forEach(push);

    return out;
  }

  // 5.2 — the sidebar carries an always-visible role="menu" OUTSIDE the overlay
  // container. Every menu scan must be scoped to `.notion-overlay-container`
  // or you will always believe a menu is open.
  //
  // Scoping to the overlay is the whole rule, and nothing more. The workspace
  // popup renders as a role="dialog" in some renders and a role="menu" in
  // others — its rows are plain role="button" divs either way. An earlier
  // version of this function also required a role="menu" ancestor and died
  // exactly the way this codebase's worst bugs die: silently, on a real run,
  // with the menu visibly open on screen. Do not put the ancestor back.
  //
  // The visible() call is load-bearing for a second reason now: a dismissed
  // workspace popup stays mounted, so without it this returns a stale row from
  // a menu that is not on screen. See visible().
  function settingsMenuItem() {
    const ov = document.querySelector('.notion-overlay-container');
    if (!ov) return null;
    const items = [...ov.querySelectorAll('[role="button"], [role="menuitem"], [role="option"]')];
    return items.find((el) => visible(el) && text(el) === 'Settings') || null;
  }

  // Language-independent: `settings-tab-ai` is a real id, not a hashed class.
  function aiNavTab() {
    const byId = document.querySelector('#settings-tab-ai') ||
                 document.querySelector('[data-testid="settings-tab-ai"]');
    if (visible(byId)) return byId;
    const dlg = settingsDialog();
    if (!dlg) return null;
    return [...dlg.querySelectorAll('[role="tab"]')].find((t) => text(t) === 'Notion AI') || null;
  }

  // The Usage sub-tab has no id of its own, but it is reliably distinguishable
  // from the left-nav: left-nav tabs carry `settings-tab-*` ids, sub-tabs don't.
  function usageSubTab() {
    const dlg = settingsDialog();
    if (!dlg) return null;
    const subTabs = [...dlg.querySelectorAll('[role="tab"]')].filter((t) => {
      if (!visible(t)) return false;
      const id = t.id || '';
      const tid = (t.dataset && t.dataset.testid) || '';
      return !/^settings-tab-/.test(id) && !/^settings-tab-/.test(tid);
    });
    const byLabel = subTabs.find((t) => text(t) === 'Usage');
    if (byLabel) return byLabel;

    // Structural fallback: the sub-tab row is the largest group of id-less
    // tabs sharing a parent, and Usage is the second entry in it.
    const groups = new Map();
    for (const t of subTabs) {
      const key = t.closest('[role="tablist"]') || t.parentElement;
      if (!key) continue;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(t);
    }
    let best = null;
    for (const arr of groups.values()) if (!best || arr.length > best.length) best = arr;
    return best && best.length > 1 ? best[1] : null;
  }

  const selected = (el) => !!el && el.getAttribute('aria-selected') === 'true';

  function closeButton(dlg) {
    return [...dlg.querySelectorAll('[role="button"], button')]
      .find((el) => visible(el) && /^close$/i.test(el.getAttribute('aria-label') || '')) || null;
  }

  // "Is this trigger's popup open?" — and the only signal that answers it
  // correctly in every state we have measured.
  //
  // The obvious tests are all wrong here. Notion now PARKS a dismissed popup
  // instead of unmounting it: after the workspace menu is dismissed by clicking
  // "Settings", its markup stays in the overlay and every row keeps a real
  // layout box (measured: the parked "Settings" row is 273x27, with a non-null
  // offsetParent). So:
  //
  //   - `overlayContainer.textContent === ''` — the check the older notes in
  //     this repo relied on — is false at rest now. Parked markup has text.
  //   - a rect-based visible() calls that parked row "on screen".
  //   - checkVisibility() sees through the parking but breaks in hidden tabs,
  //     for the reason written up at visible().
  //
  // aria-expanded is none of those things: Notion maintains it correctly
  // ("true" open, "false" parked, verified in both states), it is semantic, and
  // it cannot be affected by an animation that never ran. Gate every "is the
  // Settings row on screen?" question on it.
  const expanded = (el) => !!el && el.getAttribute('aria-expanded') === 'true';

  // Close a popup we opened ourselves, so the next candidate starts clean.
  //
  // 5.6 says `/` and `Esc` are live ammunition inside Notion — that is about
  // *listening* for keys, which this extension still never does. Dispatching an
  // Escape at a menu we just opened is the same escape hatch closeButton()
  // already falls back to, and it cannot swallow anything.
  async function dismissPopup(trigger) {
    document.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Escape', code: 'Escape', keyCode: 27, which: 27,
      bubbles: true, cancelable: true
    }));
    if (await waitFor(() => !expanded(trigger), 1200, 'dismiss-escape')) return;
    click(trigger);                           // they toggle
    await waitFor(() => !expanded(trigger), 1200, 'dismiss-toggle');
  }

  /* ------------------------------------------------------------------ *
   * Toast
   *
   * 6.4 — Trusted Types is assumed enforced: build nodes with createElement +
   * textContent, and use a constructable stylesheet, which is pure CSSOM and
   * cannot be blocked by CSP at all.
   *
   * 5.6 — never steal focus. pointer-events stays off so this can never
   * intercept a click meant for Notion.
   * ------------------------------------------------------------------ */
  const CSS = `
    .nau-toast {
      position: fixed; right: 18px; bottom: 18px; z-index: 2147483000;
      max-width: 320px; padding: 10px 14px; border-radius: 8px;
      font: 13px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #252525; color: #e6e6e6; border: 1px solid #3a3a3a;
      box-shadow: 0 6px 20px rgba(0,0,0,.35);
      pointer-events: none; opacity: 0; transition: opacity .14s ease;
      color-scheme: dark;
    }
    .nau-toast[data-show="1"] { opacity: 1; }
    .nau-toast[data-kind="error"] { border-color: #7c3f34; background: #2e1f1c; }
    .nau-toast b { color: #fff; font-weight: 600; }
  `;

  let sheetInstalled = false;
  function installStyles() {
    if (sheetInstalled) return;
    sheetInstalled = true;
    try {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(CSS);
      document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
    } catch (e) {
      const el = document.createElement('style');
      el.textContent = CSS;                   // Trusted-Types-safe fallback
      (document.head || document.documentElement).appendChild(el);
    }
  }

  let toastEl = null;
  let toastTimer = null;
  function toast(message, kind) {
    installStyles();
    if (!toastEl || !toastEl.isConnected) {
      toastEl = document.createElement('div');
      toastEl.className = 'nau-toast';
      // Dark Reader leaves a self-declared dark palette alone, but this is
      // three characters of insurance (5.6).
      toastEl.setAttribute('data-darkreader-ignore', 'true');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = message;            // no HTML-string sinks
    toastEl.setAttribute('data-kind', kind || 'info');
    toastEl.setAttribute('data-show', '1');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      if (toastEl) toastEl.setAttribute('data-show', '0');
    }, kind === 'error' ? 6000 : 1600);
  }

  function hideToast() {
    clearTimeout(toastTimer);
    if (toastEl) toastEl.setAttribute('data-show', '0');
  }

  /* ------------------------------------------------------------------ *
   * The flow
   * ------------------------------------------------------------------ */

  // Where are we already? Lets the shortcut act as a toggle, and lets a
  // re-run skip steps Notion has already done for us (it remembers the last
  // settings tab you were on).
  function currentState() {
    const dlg = settingsDialog();
    if (!dlg) return { dlg: null, onAi: false, onUsage: false };
    const ai = aiNavTab();
    const usage = usageSubTab();
    return { dlg, onAi: selected(ai), onUsage: selected(ai) && selected(usage) };
  }

  async function openSettings() {
    if (settingsDialog()) return true;

    const cands = await waitFor(
      () => { const c = workspaceSwitchers(); return c.length ? c : null; },
      6000, 'workspace-switcher'
    );
    if (!cands) return { error: 'Could not find the workspace button in the sidebar.' };

    // A failed attempt can leave the workspace popup open. Clicking the
    // switcher again would toggle it *shut*, so every later attempt on the
    // retry ladder would fail the same way and the ladder could never recover.
    // Observed while probing; check for the row first.
    //
    // But ask the trigger whether its menu is open, not the DOM — a parked
    // popup leaves a "Settings" row that looks perfectly on-screen. See
    // expanded().
    let item = cands.some(expanded) ? settingsMenuItem() : null;

    if (!item) {
      // Decide by outcome, not by identity. The first candidate is the one
      // matched on a semantic class and is expected to win outright; the rest
      // exist so a rename cannot strand us. A candidate that opens something
      // without a "Settings" row is dismissed and the next one tried.
      for (const ws of cands) {
        if (expanded(ws)) await dismissPopup(ws);   // open, but not what we want
        log('try switcher', (text(ws) || '(unlabelled)').slice(0, 24));
        click(ws);
        item = await waitFor(
          () => (expanded(ws) ? settingsMenuItem() : null),
          2500, 'settings-menu-item'
        );
        if (item) break;
        await dismissPopup(ws);
      }
    }
    if (!item) return { error: 'Opened the workspace menu but found no "Settings" item.' };

    click(item);
    const dlg = await waitFor(settingsDialog, 12000, 'settings-dialog');
    if (!dlg) return { error: 'Clicked Settings but the settings window never appeared.' };
    return true;
  }

  async function gotoAiUsage() {
    const ai = await waitFor(aiNavTab, 8000, 'ai-nav-tab');
    if (!ai) return { error: 'Settings opened but there is no "Notion AI" section in it.' };
    if (!selected(ai)) {
      click(ai);
      const ok = await waitFor(() => selected(aiNavTab()), 8000, 'ai-tab-selected');
      if (!ok) return { error: 'Clicked "Notion AI" but the section never opened.' };
    }

    const usage = await waitFor(usageSubTab, 8000, 'usage-sub-tab');
    if (!usage) return { error: 'On Notion AI, but could not find the "Usage" tab.' };
    if (!selected(usage)) {
      click(usage);
      // aria-selected is the real success condition and it is language-
      // independent, unlike scraping for "% used".
      const ok = await waitFor(() => selected(usageSubTab()), 8000, 'usage-tab-selected');
      if (!ok) return { error: 'Clicked "Usage" but the tab never became active.' };
    }
    return true;
  }

  // 5.4 — Notion's DOM lies about readiness: the chrome exists and passes a
  // visibility check well before React attaches handlers, and a click landed
  // in that window is silently swallowed. So: never treat the first attempt
  // as terminal. Retry the whole flow on a backoff ladder.
  const LADDER = [0, 1500, 4000];

  let running = false;

  async function run(opts) {
    if (isOrphaned()) return;
    if (running) { log('already-running'); return; }
    running = true;
    try {
      const state = currentState();

      // Already exactly where the shortcut takes you → treat the shortcut as
      // a toggle and close, which is what a second press obviously means.
      if (state.dlg && state.onUsage && !(opts && opts.noToggle)) {
        log('toggle-close');
        const x = closeButton(state.dlg);
        if (x) click(x);
        else state.dlg.dispatchEvent(new KeyboardEvent('keydown', {
          key: 'Escape', code: 'Escape', keyCode: 27, which: 27,
          bubbles: true, cancelable: true
        }));
        hideToast();
        return { ok: true, closed: true };
      }

      // The warm path finishes in well under a second, and a toast that
      // appears and vanishes in 700ms is just a flash of noise. Show it only
      // if this is actually going to take a moment (cold page ≈ 4s).
      const pending = setTimeout(() => toast('Opening Notion AI usage…'), 600);

      let last = null;
      for (let attempt = 0; attempt < LADDER.length; attempt++) {
        if (isOrphaned()) return;
        if (LADDER[attempt]) {
          log('retry in', LADDER[attempt] + 'ms');
          await sleep(LADDER[attempt]);
        }

        const opened = await openSettings();
        if (opened !== true) { last = opened.error; log('step-failed', last); continue; }

        const done = await gotoAiUsage();
        if (done !== true) { last = done.error; log('step-failed', last); continue; }

        log('ok attempt=' + attempt);
        clearTimeout(pending);
        hideToast();
        return { ok: true };
      }

      log('failed', last || 'unknown');
      clearTimeout(pending);
      toast(last || 'Could not open the AI usage tab.', 'error');
      return { ok: false, error: last };
    } finally {
      running = false;
    }
  }

  /* ------------------------------------------------------------------ *
   * Wiring
   * ------------------------------------------------------------------ */

  chrome.runtime.onMessage.addListener((msg, _sender, respond) => {
    if (!msg || msg.nau !== true) return;
    if (msg.cmd === 'ping') { respond({ ok: true, build: BUILD }); return; }
    if (msg.cmd === 'openAiUsage') {
      run(msg.opts).then((r) => { try { respond(r || { ok: false }); } catch (e) {} });
      return true;   // keep the channel open for the async reply
    }
  });

  log('installed v' + BUILD);
})();
