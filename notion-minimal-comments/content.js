/* ==========================================================================
 * Notion Minimal Comments — content.js
 * Manifest V3, content-script-only. See README.md and the build spec.
 *
 * One sectioned file:
 *   §0  Window sentinel (double-injection guard) + boot wrapper
 *   §1  CONFIG (single source of truth)
 *   §2  Util: logging / debug / matchers
 *   §3  Session state
 *   §4  Orphan self-destruct + cleanup registry
 *   §5  Nav-watcher (poll + popstate) and onNavigate / pageId
 *   §6  locate() + waitFor() + visibility helpers
 *   §7  detectCommentState()
 *   §8  clickEl() React-safe escalation + user-abort guard
 *   §9  Automation state machine (steps, shield, cleanup, dead-man)
 *   §10 Orchestrator: scheduleChecks()
 *   §11 Debug surface (window.__nmc)
 *   §12 Boot
 *
 * TRAP NOTES (do not "optimize" away without reading the spec §0):
 *   - No history.pushState patching (isolated world can't reach page's fn).
 *   - No chrome.* except one guarded read of chrome.runtime?.id (§4).
 *   - No HTML-string sinks anywhere (Trusted Types). createElement only.
 *   - pageId from location.pathname ONLY (peek previews live in the query).
 * ========================================================================== */

/* ------------------------------------------------------------------ §0 ---- */
/* Window sentinel: if a second copy of this script is ever injected into the
 * same document, the first one already owns the world — the second must do
 * nothing at all. Everything below runs inside the else-branch IIFE. */
if (window.__nmcInstalled) {
  // Another instance is already live in this document. Stand down silently.
} else {
  window.__nmcInstalled = true;

  (function () {
    'use strict';

    /* -------------------------------------------------------------- §1 ---- */
    const CONFIG = {
      flickerShield: true,
      urlPollMs: 400,
      // How long we keep WATCHING one page for a Default-mode comment to show
      // up, measured from page-ready. Notion hydrates margin comments lazily
      // and unpredictably late (measured: nothing at all rendered for the first
      // 8.5s of a load), so a single check at page-ready reads an empty page and
      // wrongly concludes "no comments" — that was the original bug. This is an
      // observer-driven window, not a fixed set of samples. Time spent with the
      // tab hidden does not count against it. When it expires we stop dead;
      // there is no background polling. Add a comment later → reload.
      watchWindowMs: 45000,
      // Backstop poll inside the watch window, for mode changes that produce no
      // mutation the observer sees (attribute-only / offscreen reflow).
      watchBackstopMs: 500,
      // Notion's topbar exists in the DOM well before React has attached
      // handlers to it: measured a run starting 1.6s after load whose ••• click
      // was simply swallowed ("open-more:expect(fallback): timeout"). Let the
      // page settle this long after page-ready before the first attempt.
      settleMs: 2500,
      // A swallowed click is transient, so a failed run is retried with backoff
      // instead of being written off. Only after this many attempts do we
      // record a terminal FAILED.
      maxRunAttempts: 4,
      retryBackoffMs: [1500, 4000, 9000],
      // Closing what we opened is verified, not fired-and-forgotten: press
      // Escape, re-check, repeat. 6 × 220ms ≈ 1.3s worst case, which is also
      // the longest the flicker shield can stay up.
      dismissAttempts: 6,
      dismissIntervalMs: 220,
      // Do not start a run within this long of the user's last real keystroke
      // or click. Below ~1s we routinely start a run into someone still typing
      // and immediately abort it.
      userIdleMs: 1500,
      maxRunsPerSession: 60,
      // Tiebreaker probe (§7b). Only consulted when the DOM is AMBIGUOUS —
      // i.e. the page shows margin count icons, which mean either true Minimal
      // or narrow-viewport Default and are byte-identical in both cases. Never
      // fires on the common paths, so a normal page-load still does no
      // network at all.
      modeProbe: { enabled: true, timeoutMs: 4000 },
      // pageReady raised from 15000: measured Notion loads where the topbar and
      // page content did not exist until 18.7s. At 15s this gate expired and
      // stamped the page FAILED — a TERMINAL status — so the watch never
      // started and nothing ever happened, silently. A slow load is not a
      // permanent failure, so the timeout is now generous AND non-fatal.
      timeouts: { pageReady: 30000, step: 4000, verify: 2000, runHardTimeoutMs: 10000 },

      // CSS selector used only to build the flicker shield <style>. Confirm the
      // overlay container class in Phase 0 H. If it does not resolve at run
      // time we simply proceed without a shield (spec §6.5 step 2).
      shieldSelector: '.notion-overlay-container',

      // Ordered (root)=>Element|null strategies; first CONNECTED+VISIBLE hit
      // wins. Keep >=2 strategies each; the last should be structural
      // (role/position), never a bare class. Fill the empty ones from Phase 0.
      locators: {
        topbar: [
          () => document.querySelector('.notion-topbar'),
          () => document.querySelector('[class*="topbar"]'),
        ],
        pageContent: [
          () => document.querySelector('.notion-page-content'),
          () => document.querySelector('[class*="page-content"]'),
        ],
        // Phase 0 A — the ••• button. Strategies to add:
        //   aria-label match; legacy class; last [role="button"] in the
        //   topbar actions cluster.
        moreButton: [
          // Phase 0: the ••• button is aria-label="Actions" on app.notion.com.
          () => document.querySelector('[aria-label="Actions"]'),
          // Structural fallback: right-most ICON-ONLY, UNLABELLED-BY-NAME button
          // in the top strip.
          //
          // The old version of this was just "last visible button in the top
          // strip", which is one position away from Favorite and two from the
          // breadcrumb. Measured live order:
          //   Lock sidebar open | Testing (breadcrumb) | Edited just now |
          //   Share | Copy link | Comments | Favorited | Actions
          // If Actions is briefly missing during load, that fallback would
          // happily click Favorite (silently un-stars the page) or the
          // breadcrumb (navigates away). A wrong click here is worse than no
          // click, so we now require the candidate to carry no visible text
          // (Actions is icon-only; the breadcrumb and "Edited just now" are not)
          // and to not be one of the known named controls.
          () => {
            // Every named control that can share the top strip. This list is
            // the whole safety of this fallback, so it is deliberately
            // over-inclusive: a name missing from it is a candidate we might
            // click by mistake. `close/open/expand/collapse sidebar` added
            // 2026-09-02 — the sidebar toggle is labelled "Lock sidebar open"
            // only while the sidebar is pinned; unpinned it reads "Close
            // sidebar" / "Open sidebar", which the original list missed.
            const KNOWN = /^(lock sidebar|unlock sidebar|close sidebar|open sidebar|expand sidebar|collapse sidebar|share|copy link|page info|comments?|favorite|favorited|unfavorite|updates|search|home|settings|back|forward|inbox|new page|help)/i;
            const b = [...document.querySelectorAll('[role="button"],button')]
              .filter((x) => {
                const r = x.getBoundingClientRect();
                if (!(r.top < 70 && r.width > 0 && r.height > 0)) return false;
                if ((x.textContent || '').trim() !== '') return false;
                return !KNOWN.test((x.getAttribute('aria-label') || '').trim());
              });
            return b[b.length - 1] || null;
          },
        ],
        // "Overlay" = an OPEN popup (menu/dialog/listbox) inside Notion's
        // overlay container. The container itself always exists, and the
        // sidebar has an always-visible role="menu", so we must scope to the
        // container and return the open popup, not the container.
        overlay: [
          () => {
            const c = document.querySelector('.notion-overlay-container')
              || [...document.querySelectorAll('div')].find((d) => /overlay/i.test(d.className));
            if (!c) return null;
            return [...c.querySelectorAll('[role="menu"],[role="dialog"],[role="listbox"]')]
              .find((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; }) || null;
          },
        ],
        // Phase 0 B/C — the "Inline comments" row inside the ••• (or Customize
        // page) menu. Prefer a role+text scan, not a class.
        inlineRow: [
          // Find the VISIBLE "Inline comments" label (role="presentation"),
          // then walk up to the row that also contains its value. Document-wide
          // on purpose: this label only exists in the open Customize panel, and
          // Notion nests popups (menu/dialog/listbox) unpredictably.
          () => {
            const lbl = [...document.querySelectorAll('[role="presentation"]')]
              .find((e) => /^inline comments$/i.test((e.textContent || '').trim())
                && e.getBoundingClientRect().width > 0);
            if (!lbl) return null;
            let row = lbl;
            for (let i = 0; i < 8 && row.parentElement; i++) {
              row = row.parentElement;
              if (/default|minimal/i.test(row.textContent || '')) break;
            }
            return row;
          },
        ],
        // Phase 0 C — the Default/Minimal value control (chevron) in that row.
        valueControl: [
          // The role=button (aria-haspopup="dialog") inside the Inline comments
          // row; its text is the current value ("Default" / "Minimal").
          () => {
            const lbl = [...document.querySelectorAll('[role="presentation"]')]
              .find((e) => /^inline comments$/i.test((e.textContent || '').trim())
                && e.getBoundingClientRect().width > 0);
            if (!lbl) return null;
            let row = lbl;
            for (let i = 0; i < 8 && row.parentElement; i++) {
              row = row.parentElement;
              if (/default|minimal/i.test(row.textContent || '')) break;
            }
            return row.querySelector('[role="button"][aria-haspopup]') || row.querySelector('[role="button"]') || null;
          },
        ],
        // Phase 0 C — the "Minimal" option in the opened chooser list.
        minimalOption: [
          // The "Minimal" item in the opened chooser (role="menuitem" as of
          // 2026-09, but scan several roles — Notion's overlay swaps
          // menu/option/button freely). Visible-only; the caller excludes the
          // value control itself.
          //
          // Scoped to the overlay CONTAINER, not the document: "Minimal" is an
          // ordinary English word and a page could easily contain a button or
          // toggle with that label. Scoping to the overlay is the standing rule
          // for every menu-item scan in this codebase. Falls back to
          // document-wide only if the container itself cannot be found.
          () => {
            const oc = document.querySelector('.notion-overlay-container')
              || [...document.querySelectorAll('div')].find((d) => /overlay/i.test(d.className))
              || document;
            return [...oc.querySelectorAll('[role="menuitem"],[role="option"],[role="button"]')]
              .find((e) => /^minimal$/i.test((e.textContent || '').trim())
                && e.getBoundingClientRect().width > 0) || null;
          },
        ],

        // ---- Detector inputs -------------------------------------------------
        // REQUIRED before the extension can ever act. Left empty on purpose:
        // with these empty, detectCommentState() returns NONE, so the automation
        // never runs and no menu ever opens. DO NOT guess these — fill only from
        // Phase 0 F (preferred) / D / E / G.
        modeSignal: [
          // Phase 0 F — attr/class on the page-content container (or a stable
          // descendant) that differs by inline-comment mode, independent of
          // whether a comment is currently on screen. If found, this is the
          // primary detector. Provide a way to read the mode from it below
          // via readModeFromSignal().
        ],
        defaultCommentPreview: [
          // Phase 0 (B-default): DEFAULT mode renders the margin preview as
          // .notion-margin-discussion-item (author + text, ~308x74). It lives
          // OUTSIDE .notion-page-content, so search the whole document.
          () => document.querySelector('.notion-margin-discussion-item'),
          () => document.querySelector('[class*="margin-discussion"]'),
        ],
        minimalCommentIcon: [
          // Phase 0 (B-minimal): MINIMAL mode renders a margin count icon —
          // role=button with aria-label "N comment(s)" wrapping svg.commentFilledSmall.
          () => [...document.querySelectorAll('[role="button"][aria-label]')]
            .find((e) => /^\d+\s+comments?$/i.test(e.getAttribute('aria-label') || '')) || null,
          () => {
            const svg = document.querySelector('svg.commentFilledSmall, svg[class*="commentFilledSmall"]');
            return svg ? (svg.closest('[role="button"]') || svg) : null;
          },
        ],
      },

      // Case-insensitive regex arrays; locale-extensible in one place.
      matchers: {
        customizePage: [/customize page/i],
        customizeLayout: [/customize layout/i],
        inlineCommentsRow: [/inline comments/i],
        minimal: [/^minimal$/i],
        default_: [/^default$/i],
      },
    };

    /* -------------------------------------------------------------- §2 ---- */
    const LOG_PREFIX = '[NMC]';
    const isDebug = () => {
      try { return localStorage.getItem('nmc_debug') === '1'; } catch { return false; }
    };
    const isOff = () => {
      try { return localStorage.getItem('nmc_off') === '1'; } catch { return false; }
    };
    // ---- Observability mirror -------------------------------------------
    // A content script logs into its ISOLATED world. Those lines show up in
    // DevTools, but nothing outside the extension can read them — not the page,
    // not CDP console capture, not an automation harness. Debugging this
    // extension from outside was therefore blind guessing.
    // The DOM, unlike the console, IS shared. So under nmc_debug=1 we mirror a
    // short ring of recent events onto <html data-nmc-log>, which anything can
    // read with one selector:
    //     document.documentElement.dataset.nmcLog
    // Costs one setAttribute per event, and only when debugging.
    const MIRROR_MAX = 16;
    const mirrorRing = [];
    const mirror = (parts) => {
      if (!isDebug()) return;
      try {
        mirrorRing.push(`+${Math.round(now())}ms ${parts.join(' ')}`);
        while (mirrorRing.length > MIRROR_MAX) mirrorRing.shift();
        document.documentElement.setAttribute('data-nmc-log', mirrorRing.join(' || '));
      } catch { /* noop */ }
    };
    const flat = (a) => a.map((x) => {
      if (typeof x === 'string' || typeof x === 'number') return String(x);
      if (x instanceof Error) return x.message;
      try { return JSON.stringify(x); } catch { return String(x); }
    });

    const log = (...a) => { console.info(LOG_PREFIX, ...a); mirror(flat(a)); };
    const warn = (...a) => { console.warn(LOG_PREFIX, ...a); mirror(['WARN', ...flat(a)]); };
    const dbg = (...a) => { if (isDebug()) { console.info(LOG_PREFIX, '[dbg]', ...flat(a)); mirror(flat(a)); } };

    const matchAny = (text, regexArray) => {
      const t = (text || '').trim();
      return !!t && regexArray.some((re) => re.test(t));
    };

    const now = () => (typeof performance !== 'undefined' ? performance.now() : Date.now());

    /* -------------------------------------------------------------- §3 ---- */
    // Status ∈ {DONE, FAILED, NOT_APPLICABLE, SKIPPED_BY_USER}. Terminal =
    // stop re-evaluating this pageId for the rest of the session. In-memory
    // only — never persisted (a page can revert to Default from another
    // device; the DOM pre-check is the free source of truth each session).
    const STATUS = {
      DONE: 'DONE',
      FAILED: 'FAILED',
      NOT_APPLICABLE: 'NOT_APPLICABLE',
      SKIPPED_BY_USER: 'SKIPPED_BY_USER',
    };
    const TERMINAL = new Set([STATUS.DONE, STATUS.FAILED, STATUS.NOT_APPLICABLE, STATUS.SKIPPED_BY_USER]);

    const sessionState = new Map(); // pageId -> Status
    let runsThisSession = 0;
    let running = false;            // automation lock
    let currentRunPageId = null;    // pageId of the in-flight automation
    let lastHref = null;            // nav-watcher dedupe
    let lastNavPageId = null;       // debounce onNavigate by pageId
    let activeWatch = null;         // the single in-flight page watch (§10)
    const exhaustedThisSession = new Set(); // pageIds whose watch window expired finding only NONE

    const setStatus = (pageId, status) => {
      sessionState.set(pageId, status);
      log(`${pageId} → ${status}`);
    };

    /* -------------------------------------------------------------- §4 ---- */
    // Everything that must be torn down when this content-script instance dies
    // (extension reload → orphaned script) or is disabled.
    let destroyed = false;
    let pollTimer = null;
    const teardownFns = [];
    const onTeardown = (fn) => { teardownFns.push(fn); };

    const selfDestruct = () => {
      if (destroyed) return;
      destroyed = true;
      try { if (pollTimer) clearInterval(pollTimer); } catch { /* noop */ }
      pollTimer = null;
      // Best-effort: also close any overlay we might have opened and drop the
      // shield, so an orphaned instance never leaves the page wedged.
      try { removeShield(); } catch { /* noop */ }
      for (const fn of teardownFns.splice(0)) {
        try { fn(); } catch { /* noop */ }
      }
      dbg('selfDestruct: instance torn down');
    };

    // The ONLY chrome.* access in the extension. An orphaned content script
    // (left running after the user reloads the unpacked extension) throws or
    // reads a null runtime id here on its next tick, and tears itself down.
    const isOrphaned = () => {
      try { return !chrome.runtime || !chrome.runtime.id; } catch { return true; }
    };

    /* -------------------------------------------------------------- §5 ---- */
    // pageId from PATHNAME ONLY. Peek/side previews put the id in the query
    // (?p=<id>); extracting from the whole href would make us act on a peeked
    // page whose topbar/menu differ. 32 hex chars, dashless.
    const PAGE_ID_RE = /([0-9a-f]{32})/;
    const extractPageIdFromPathname = (url) => {
      let pathname;
      try { pathname = new URL(url, location.origin).pathname; } catch { return null; }
      const m = pathname.replace(/-/g, '').match(PAGE_ID_RE);
      return m ? m[1] : null;
    };

    const tick = () => {
      if (destroyed) return;
      if (isOrphaned()) { selfDestruct(); return; }
      const href = location.href;
      if (href !== lastHref) {
        lastHref = href;
        onNavigate(href);
      }
    };

    const onNavigate = (url) => {
      if (destroyed) return;
      if (isOff()) { dbg('nmc_off=1 → onNavigate no-op'); return; }

      const pageId = extractPageIdFromPathname(url);
      if (!pageId) { dbg('nav: no pathname page id → ignore', url); return; }
      dbg('nav →', pageId);

      // Debounce: same id as the one already in progress / just handled.
      if (pageId === lastNavPageId && (running || sessionState.has(pageId) || exhaustedThisSession.has(pageId))) {
        return;
      }

      // Rapid nav mid-run onto a *different* page: abort the in-flight run and
      // let the old page re-evaluate on a future revisit (leave its status
      // unset). §9 edge case 1.
      if (running && currentRunPageId && currentRunPageId !== pageId) {
        dbg('nav to different page mid-run → abort current run', { from: currentRunPageId, to: pageId });
        requestAbort();
      }

      lastNavPageId = pageId;

      if (sessionState.has(pageId) && TERMINAL.has(sessionState.get(pageId))) {
        dbg('nav: terminal status, skip', pageId, sessionState.get(pageId));
        return;
      }
      if (runsThisSession >= CONFIG.maxRunsPerSession) {
        warn('run cap reached this session; not acting');
        return;
      }

      // Hidden tabs are handled INSIDE the watch (§10): it starts, but never
      // evaluates or clicks while document.hidden, and its window does not
      // burn down. §9 edge case 2.
      scheduleChecks(pageId);
    };

    /* -------------------------------------------------------------- §6 ---- */
    const isVisible = (el) => {
      if (!el || !el.isConnected) return false;
      const rect = el.getBoundingClientRect();
      if (!rect || rect.width === 0 || rect.height === 0) return false;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      return true;
    };

    // Returns the first connected+visible element from CONFIG.locators[name].
    // Ambiguity guard: strategies must each yield <=1 element; a strategy that
    // is expected to be unique but matches many is treated as a miss (we log
    // and move on rather than guess). Callers can pass a root element.
    const locate = (name, root) => {
      const strategies = CONFIG.locators[name] || [];
      for (let i = 0; i < strategies.length; i++) {
        let el;
        try { el = strategies[i](root); } catch (e) { dbg(`locate ${name}[${i}] threw`, e); continue; }
        if (!el) continue;
        if (el instanceof Element && isVisible(el)) return el;
      }
      return null;
    };

    // waitFor: check now; else MutationObserver on body (childList+subtree),
    // re-running the predicate throttled via rAF, plus a 250ms interval
    // backstop for attribute-only changes. Reject with `label` on timeout.
    // Never a bare setTimeout sleep. Predicate must re-query fresh each call.
    const waitFor = (predicate, { timeout = CONFIG.timeouts.step, label = 'waitFor' } = {}) =>
      new Promise((resolve, reject) => {
        const started = now();
        let settled = false;
        let observer = null;
        let backstop = null;
        let deadline = null;
        let rafPending = false;

        const cleanupWait = () => {
          try { if (observer) observer.disconnect(); } catch { /* noop */ }
          try { if (backstop) clearInterval(backstop); } catch { /* noop */ }
          try { if (deadline) clearTimeout(deadline); } catch { /* noop */ }
          observer = null; backstop = null; deadline = null;
        };

        const attempt = () => {
          if (settled || destroyed) return;
          let result;
          try { result = predicate(); } catch (e) { dbg(`${label}: predicate threw`, e); return; }
          if (result) {
            settled = true;
            cleanupWait();
            dbg(`${label}: resolved in ${Math.round(now() - started)}ms`);
            resolve(result);
          }
        };

        const scheduleAttempt = () => {
          if (rafPending || settled) return;
          rafPending = true;
          requestAnimationFrame(() => { rafPending = false; attempt(); });
        };

        // Immediate check.
        attempt();
        if (settled) return;

        observer = new MutationObserver(scheduleAttempt);
        try {
          observer.observe(document.body, { childList: true, subtree: true, attributes: true });
        } catch { /* body may be missing very early; backstop still covers us */ }
        backstop = setInterval(attempt, 250);
        deadline = setTimeout(() => {
          if (settled) return;
          settled = true;
          cleanupWait();
          reject(new Error(`${label}: timeout after ${timeout}ms`));
        }, timeout);
      });

    const overlayVisible = () => !!locate('overlay');

    /* -------------------------------------------------------------- §7 ---- */
    // Read mode from a DOM signal element, if one is ever configured.
    // CONFIG.locators.modeSignal is still empty: searched again 2026-09-02 and
    // the mode is NOT exposed in the DOM in any form (no attribute, no class,
    // no data-* on .notion-page-content or any ancestor). It lives only in the
    // page record — see modeFromRecord() below. Kept as a hook because a DOM
    // signal, if Notion ever ships one, would beat a network round trip.
    // Return 'DEFAULT' | 'MINIMAL' | null.
    const readModeFromSignal = (el) => {
      if (!el) return null;
      return null;
    };

    /* -------------------------------------------------------------- §7b --- */
    // The authoritative mode signal, and the answer to the "Phase 0 F" question
    // this extension was designed around and shipped without.
    //
    // Notion stores it on the page block as:
    //     format.page_section_visibility.margin_comments
    //         "inline"   → Default   (expanded previews in the margin)
    //         "minimal"  → Minimal   (count icons)
    //         ABSENT     → Default   (never set; Notion's default is inline)
    //
    // The same response also carries `parent_table` ("space" = standalone,
    // "collection" = database row), which the probe reports as 'DATABASE'.
    //
    // Verified live 2026-09-02 by flipping the setting and re-reading: the
    // value tracked the UI both ways, and an untouched page had no
    // page_section_visibility key at all.
    //
    // WHY THIS IS A TIEBREAKER AND NOT THE PRIMARY DETECTOR. The DOM is still
    // what decides *whether this page has inline comments at all* — the record
    // does not carry that (discussions live on the child blocks, not the page
    // block, so answering it via the API would mean walking the whole page).
    // Keeping the DOM in that role is also what stops the extension writing to
    // pages that never needed it: a comment-free page reads "inline" here, and
    // acting on that would mark it edited, for every viewer, for nothing.
    //
    // So: DOM answers "are there comments?", this answers "which mode?", and it
    // is only asked when the DOM genuinely cannot tell (count icons showing).
    //
    // Read-only. syncRecordValues is a POST but changes nothing; the extension
    // still never writes through the API.
    const dashify = (id32) => (/^[0-9a-f]{32}$/i.test(id32)
      ? id32.replace(/^(.{8})(.{4})(.{4})(.{4})(.{12})$/, '$1-$2-$3-$4-$5')
      : id32);

    // pageId -> 'DEFAULT' | 'MINIMAL' | 'DATABASE' | 'UNKNOWN' | Promise (in
    // flight). Single-flight and cached for the session: at most one request
    // per page, ever.
    //
    // Session-scoped, so it can go stale if the setting is changed from another
    // device — or by you, by hand, in this tab. The rare miss that buys: set a
    // page back to Default *while the window is narrow*, revisit it without
    // reloading, and we will trust the cached "MINIMAL" and skip it. A reload
    // clears it. That is the same session-scoped staleness `sessionState`
    // already accepts (see "No persistence" in the README), and the alternative
    // — re-probing on every revisit — spends requests on the one case where the
    // answer almost never changes.
    const modeCache = new Map();

    const fetchMode = async (pageId) => {
      const id = dashify(pageId);
      const ctl = typeof AbortController === 'function' ? new AbortController() : null;
      const timer = ctl ? setTimeout(() => ctl.abort(), CONFIG.modeProbe.timeoutMs) : null;
      try {
        const res = await fetch('/api/v3/syncRecordValues', {
          method: 'POST',
          credentials: 'include',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ requests: [{ pointer: { table: 'block', id }, version: -1 }] }),
          signal: ctl ? ctl.signal : undefined,
        });
        if (!res.ok) return 'UNKNOWN';
        const json = await res.json();
        const rec = json && json.recordMap && json.recordMap.block && json.recordMap.block[id];
        if (!rec) return 'UNKNOWN';
        // Notion has shipped both {value:{...}} and {value:{value:{...}}}.
        const v = rec.value && rec.value.value ? rec.value.value : rec.value;
        if (!v) return 'UNKNOWN';

        // ⚠️ A record we cannot read still comes back **200**, shaped
        // `{spaceId, value: {role}}` — a value carrying nothing but a role, no
        // id, no type, no parent_table. Without this guard that empty record
        // falls through to "margin_comments is absent" and returns DEFAULT,
        // and DEFAULT is the verdict that says *go convert the page*. Getting
        // that wrong is the only failure mode here that costs a write, so
        // require positive proof we actually read the block. Caught in testing
        // 2026-09-02 by probing a nonexistent id.
        if (!v.id) return 'UNKNOWN';

        // Free, from the response we already have: parent_table is "space" for
        // a standalone page and "collection" for a database row page. It
        // dominates the mode — inline-comment mode on a database item is
        // governed by the database layout, not the page — so answer that first.
        //
        // This is deliberately NOT hoisted into a pre-check that runs on every
        // page: that would mean a network call on every commented database page
        // just to avoid a menu we open harmlessly today. Here the request has
        // already happened, so reading one more field is free, and it saves
        // opening the ••• menu purely to discover "Customize layout".
        if (v.parent_table === 'collection') return 'DATABASE';

        const mc = v.format && v.format.page_section_visibility
          && v.format.page_section_visibility.margin_comments;
        if (mc === 'minimal') return 'MINIMAL';
        if (mc === 'inline' || mc === undefined || mc === null) return 'DEFAULT';
        dbg('mode probe: unrecognised margin_comments value', mc);
        return 'UNKNOWN';
      } catch (e) {
        dbg('mode probe failed', (e && e.message) || e);
        return 'UNKNOWN';
      } finally {
        if (timer) clearTimeout(timer);
      }
    };

    // Synchronous accessor for the watch loop: returns a verdict if we have
    // one, or null while a request is in flight (the watch just keeps going and
    // will see it on a later tick).
    const modeProbe = (pageId) => {
      if (!CONFIG.modeProbe.enabled) return 'UNKNOWN';
      const hit = modeCache.get(pageId);
      if (typeof hit === 'string') return hit;
      if (hit) return null;                       // already in flight
      const p = fetchMode(pageId).then((verdict) => {
        modeCache.set(pageId, verdict);
        dbg('mode probe', pageId, '→', verdict);
        // We resolved after the tick that asked; poke the watch so the answer
        // is acted on now rather than on the next 500ms backstop.
        if (activeWatch && activeWatch.pageId === pageId) activeWatch.evaluate();
        return verdict;
      });
      modeCache.set(pageId, p);
      return null;
    };

    // Classify inline-comment mode for the current page.
    //   'DEFAULT_VISIBLE'   → run automation
    //   'COUNT_ICONS'       → comments exist, but the mode is AMBIGUOUS from the
    //                         DOM alone; the caller breaks the tie with
    //                         modeProbe() (§7b)
    //   'NONE'              → do nothing (a later check may find it)
    //
    // THE COUNT ICON DOES NOT PROVE THE SETTING IS MINIMAL (measured
    // 2026-07-25). Notion falls back to the same margin count icon for a
    // DEFAULT-mode page whenever the viewport is too narrow to lay out the
    // margin column — the flip is between 1100px and 1150px with the sidebar
    // collapsed, and moves with the sidebar. Same page, same setting, no
    // reload, only the window width changed:
    //   1440px → .notion-margin-discussion-item (expanded preview)
    //   1020px → role=button aria-label="1 comment" + svg.commentFilledSmall
    // That is the *identical* markup true Minimal produces, so no amount of DOM
    // inspection can separate them. Only the Customize page panel knows.
    //
    // WE DELIBERATELY DO NOT GO LOOK. The goal of this extension is that you
    // don't have expanded comment boxes shoved in your face; it is not to
    // normalise a stored setting. A count icon means you are already seeing
    // what you wanted, whatever the setting happens to say — so there is
    // nothing to fix, and opening the ••• menu on every commented page to
    // discover that would be pure cost. This is self-correcting: widen the
    // window past the breakpoint, the expanded previews appear, the detector
    // reads DEFAULT_VISIBLE on the next visit and converts for real.
    //
    // Because that verdict is about the current window and not about the page,
    // it deliberately leaves sessionState UNSET rather than stamping DONE — so
    // re-navigating re-evaluates at the new width.
    //
    // UPDATE 2026-09-02: the tie IS now breakable. §7b reads the real setting
    // off the page record, so 'COUNT_ICONS' is no longer a dead end — a
    // narrow-viewport Default page gets converted instead of being skipped.
    // The paragraphs above are kept because the DOM-level ambiguity they
    // describe is still exactly as real; what changed is that we stopped
    // needing to resolve it from the DOM.
    // Prefers the Phase-0-F mode signal (comment-position independent); falls
    // back to preview heuristics scoped to the page-content container, keying
    // on INLINE previews only (ignore page-discussion / resolved — Phase 0 G).
    const detectCommentState = () => {
      // 1) Preferred: mode signal.
      const signalEl = locate('modeSignal', locate('pageContent') || undefined);
      const mode = readModeFromSignal(signalEl);
      if (mode === 'DEFAULT') return 'DEFAULT_VISIBLE';
      if (mode === 'MINIMAL') return 'MINIMAL_ONLY';

      // 2) Fallback: preview heuristics.
      const content = locate('pageContent') || undefined;
      const hasDefault = !!locate('defaultCommentPreview', content);
      const hasMinimal = !!locate('minimalCommentIcon', content);
      if (hasDefault) return 'DEFAULT_VISIBLE';
      // Count icons prove comments EXIST but not which mode produced them —
      // see the block comment above. The caller asks §7b.
      if (hasMinimal) return 'COUNT_ICONS';
      return 'NONE';
    };

    /* -------------------------------------------------------------- §8 ---- */
    // User-abort guard. Real (isTrusted) pointerdown/keydown from the user
    // aborts the run so we never fight them. Our synthetic events are
    // isTrusted:false, so we never trip ourselves.
    let aborted = false;
    let abortArmed = false;

    // Always-on record of when the user last really touched the page. The
    // abort guard below is reactive — it kills a run already underway. This is
    // preventive: we simply do not START a run while the user is mid-keystroke,
    // which is precisely the moment automation is most likely to fire (you
    // just typed a comment, so a Default preview just appeared).
    let lastRealInputAt = 0;
    const noteRealInput = (e) => { if (e && e.isTrusted === true) lastRealInputAt = now(); };
    const userIsActive = () => (now() - lastRealInputAt) < CONFIG.userIdleMs;
    window.addEventListener('pointerdown', noteRealInput, true);
    window.addEventListener('keydown', noteRealInput, true);
    onTeardown(() => {
      window.removeEventListener('pointerdown', noteRealInput, true);
      window.removeEventListener('keydown', noteRealInput, true);
    });

    const onRealInput = (e) => { if (e && e.isTrusted === true) { aborted = true; dbg('user input → abort'); } };
    const armAbortGuard = () => {
      if (abortArmed) return;
      aborted = false;
      abortArmed = true;
      window.addEventListener('pointerdown', onRealInput, true);
      window.addEventListener('keydown', onRealInput, true);
    };
    const disarmAbortGuard = () => {
      if (!abortArmed) return;
      abortArmed = false;
      window.removeEventListener('pointerdown', onRealInput, true);
      window.removeEventListener('keydown', onRealInput, true);
    };
    const requestAbort = () => { aborted = true; };
    const throwIfAborted = () => { if (aborted) { const e = new Error('SKIPPED_BY_USER'); e.__abort = true; throw e; } };

    // clickEl: React-safe escalation. React listens on the app root and menu
    // items live in portals; a dispatched event may never reach React, and
    // items often act on pointerdown/mousedown, not click. So fire a full
    // pointer+mouse sequence, then CONFIRM the intended effect (`expect`),
    // then fall back to native .click(), then re-confirm.
    const POINTER_SEQ = ['pointerover', 'pointerenter', 'pointermove', 'pointerdown'];
    const POINTER_TAIL = ['pointerup'];
    const dispatchSynthetic = (el, type, cx, cy) => {
      const base = { bubbles: true, cancelable: true, composed: true, view: window, clientX: cx, clientY: cy };
      let ev;
      if (type.startsWith('pointer')) {
        ev = new PointerEvent(type, { ...base, pointerId: 1, pointerType: 'mouse', isPrimary: true, button: 0 });
      } else {
        ev = new MouseEvent(type, { ...base, button: 0 });
      }
      el.dispatchEvent(ev);
    };

    const clickEl = async (el, { expect, timeout = 700, label = 'click' } = {}) => {
      if (!el || !el.isConnected) { const e = new Error('stale'); e.__stale = true; throw e; }
      throwIfAborted();

      try { el.scrollIntoView({ block: 'nearest' }); } catch { /* noop */ }

      let rect = el.getBoundingClientRect();
      if (!rect || rect.width === 0 || rect.height === 0) {
        // Give layout a beat to produce a real box before we compute coords.
        try {
          await waitFor(() => {
            const r = el.getBoundingClientRect();
            return r && r.width > 0 && r.height > 0 ? r : null;
          }, { timeout: 500, label: `${label}:rect` });
          rect = el.getBoundingClientRect();
        } catch {
          const e = new Error('stale'); e.__stale = true; throw e; // zero-rect → treat as stale
        }
      }
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;

      const seq = [...POINTER_SEQ, 'mousedown', ...POINTER_TAIL, 'mouseup', 'click'];
      for (const type of seq) {
        throwIfAborted();
        if (!el.isConnected) { const e = new Error('stale'); e.__stale = true; throw e; }
        dispatchSynthetic(el, type, cx, cy);
      }

      if (!expect) return true;

      try {
        await waitFor(expect, { timeout, label: `${label}:expect` });
        return true;
      } catch {
        // Fallback: native activation, then a short re-confirm.
        throwIfAborted();
        if (el.isConnected) { try { el.click(); } catch { /* noop */ } }
        await waitFor(expect, { timeout: 400, label: `${label}:expect(fallback)` });
        return true;
      }
    };

    /* -------------------------------------------------------------- §9 ---- */
    let shieldEl = null;
    const addShield = () => {
      if (!CONFIG.flickerShield || shieldEl) return;
      try {
        const style = document.createElement('style');
        style.id = 'nmc-shield';
        // opacity:0 only — keeps layout boxes so our getBoundingClientRect
        // clicks still work; display/visibility would break locate/click.
        style.textContent = `${CONFIG.shieldSelector}{opacity:0 !important;}`;
        (document.head || document.documentElement).appendChild(style);
        shieldEl = style;
      } catch (e) { dbg('addShield failed (proceeding without shield)', e); }
    };
    function removeShield() {
      const existing = shieldEl || document.getElementById('nmc-shield');
      if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
      shieldEl = null;
    }

    const pressEscape = () => {
      for (const type of ['keydown', 'keyup']) {
        const ev = new KeyboardEvent(type, { key: 'Escape', code: 'Escape', keyCode: 27, which: 27, bubbles: true, cancelable: true });
        document.body.dispatchEvent(ev);
      }
    };

    // Dismiss whatever we opened, VERIFYING that it actually closed, then drop
    // the shield.
    //
    // The old version fired Escape twice, 60ms apart, and hoped. Measured
    // failure on a heavy page (66k DOM nodes): picking "Minimal" took 455ms,
    // both Escapes landed during the chooser's closing animation and were
    // swallowed, and the Customize panel underneath stayed open — then the
    // shield was removed, so the user was left looking at a menu the extension
    // had opened. Escape on document.body is the right target (verified: it
    // closes the panel immediately when the animation is not in flight); the
    // bug was purely that we never checked.
    //
    // The shield stays up until the overlay is actually gone, so a stuck panel
    // is not revealed mid-dismissal — but it is ALWAYS removed at the end of
    // the bounded loop, so we can never leave the page dimmed.
    const dismissOverlaysThenUnshield = () => {
      let attempts = 0;
      const tick = () => {
        if (destroyed) { removeShield(); return; }
        if (!overlayVisible()) { removeShield(); return; }
        // Never fight the user for a menu they just opened themselves.
        if (attempts >= CONFIG.dismissAttempts || userIsActive()) {
          warn('overlay still open after', attempts, 'escape attempts — unshielding anyway');
          removeShield();
          return;
        }
        attempts++;
        try { pressEscape(); } catch { /* noop */ }
        setTimeout(tick, CONFIG.dismissIntervalMs);
      };
      tick();
    };

    let deadMan = null;
    const cleanup = () => {
      dismissOverlaysThenUnshield();
      disarmAbortGuard();
      if (deadMan) { clearTimeout(deadMan); deadMan = null; }
      running = false;
      currentRunPageId = null;
    };

    // Re-locate helper used by steps: runs clickEl, and on a `stale` throw
    // re-locates the element once and retries the same click.
    const clickWithStaleRetry = async (locateFn, opts) => {
      let el = locateFn();
      if (!el) throw new Error(`${opts.label || 'click'}: locate miss`);
      try {
        return await clickEl(el, opts);
      } catch (e) {
        if (e && e.__stale) {
          dbg(`${opts.label}: stale → re-locate once`);
          el = locateFn();
          if (!el) throw new Error(`${opts.label || 'click'}: locate miss (after stale)`);
          return await clickEl(el, opts);
        }
        throw e;
      }
    };

    const valueControlText = () => {
      const vc = locate('valueControl', locate('overlay') || undefined);
      return vc ? (vc.textContent || '').trim() : '';
    };

    // The full step chain (§6.5). Returns a Status.
    const runAutomation = async (pageId) => {
      running = true;
      currentRunPageId = pageId;
      runsThisSession++;
      const started = now();

      // Dead-man switch: a wedged run can never leave overlays open / lock stuck.
      deadMan = setTimeout(() => { warn('dead-man timeout → forcing cleanup'); cleanup(); }, CONFIG.timeouts.runHardTimeoutMs);

      armAbortGuard();

      try {
        // Step 1 — pre-flight: if any overlay is already open, the user has
        // something open. Never close it; retry on a later scheduled slot.
        if (overlayVisible()) {
          dbg('pre-flight: overlay already open → yield');
          return null; // leave status unset; a later check retries
        }

        // Step 2 — flicker shield.
        addShield();

        // Step 3 — open the ••• menu.
        throwIfAborted();
        await clickWithStaleRetry(
          () => locate('moreButton', locate('topbar') || undefined),
          { label: 'open-more', expect: () => overlayVisible(), timeout: CONFIG.timeouts.step }
        );

        // Step 4 — find the Inline-comments row (adaptive).
        throwIfAborted();
        let inlineRow = null;
        try {
          inlineRow = await waitFor(() => locate('inlineRow', locate('overlay') || undefined), { timeout: 1200, label: 'inline-row-direct' });
        } catch { /* not directly present — try Customize page */ }

        if (!inlineRow) {
          // Scope the item scan to the overlay CONTAINER (not one popup — the
          // ••• menu is menu+dialog+listbox nested) and visible items only.
          // Must not be document-wide: on database pages "Customize layout"
          // also exists as a page-header button outside any menu.
          const menuItems = () => {
            const oc = document.querySelector('.notion-overlay-container')
              || [...document.querySelectorAll('div')].find((d) => /overlay/i.test(d.className));
            return [...(oc || document).querySelectorAll('[role="menuitem"],[role="option"],[role="button"]')]
              .filter(isVisible);
          };
          const menuTexts = () => menuItems().map((e) => (e.textContent || '').trim()).filter(Boolean);

          const items = menuItems();
          const customizePage = items.find((e) => matchAny(e.textContent, CONFIG.matchers.customizePage));
          const customizeLayout = items.find((e) => matchAny(e.textContent, CONFIG.matchers.customizeLayout));

          if (customizeLayout && !customizePage) {
            // Database page — governed by database layout. Not our case.
            dbg('found "Customize layout" (database page) — items:', menuTexts());
            return STATUS.NOT_APPLICABLE;
          }

          if (customizePage) {
            await clickEl(customizePage, { label: 'customize-page', expect: () => !!locate('inlineRow', locate('overlay') || undefined), timeout: CONFIG.timeouts.step });
            inlineRow = locate('inlineRow', locate('overlay') || undefined);
          }

          if (!inlineRow) {
            dbg('no inline-comments row and no Customize page — items:', menuTexts());
            return STATUS.NOT_APPLICABLE;
          }
        }

        // Step 5 — read current value; if already Minimal, we're done.
        throwIfAborted();
        if (matchAny(valueControlText(), CONFIG.matchers.minimal)) {
          dbg('value already Minimal');
          return STATUS.DONE;
        }

        // Step 6 — open the chooser and pick Minimal.
        throwIfAborted();
        await clickWithStaleRetry(
          () => locate('valueControl', locate('overlay') || undefined),
          { label: 'open-value', expect: () => !!locate('minimalOption', locate('overlay') || undefined), timeout: CONFIG.timeouts.step }
        );

        throwIfAborted();
        await clickWithStaleRetry(
          () => {
            const vc = locate('valueControl', locate('overlay') || undefined);
            const opt = locate('minimalOption', locate('overlay') || undefined);
            // Exclude the value control itself from being treated as the option.
            return opt && opt !== vc ? opt : null;
          },
          { label: 'pick-minimal', expect: () => matchAny(valueControlText(), CONFIG.matchers.minimal), timeout: CONFIG.timeouts.step }
        );

        // Step 7 — hard verify.
        throwIfAborted();
        await waitFor(() => matchAny(valueControlText(), CONFIG.matchers.minimal), { timeout: CONFIG.timeouts.verify, label: 'verify-minimal' });

        return STATUS.DONE;
      } catch (e) {
        if (e && e.__abort) return STATUS.SKIPPED_BY_USER;
        warn('automation failed:', e && e.message ? e.message : e);
        return STATUS.FAILED;
      } finally {
        cleanup();
        dbg(`automation finished in ${Math.round(now() - started)}ms`);
      }
    };

    // Step 8 — soft verify (log-only; never flips status).
    const softVerify = () => {
      setTimeout(() => {
        try {
          if (detectCommentState() === 'DEFAULT_VISIBLE') {
            warn('soft-verify: body still shows Default previews (control confirmed Minimal; render may lag) — check detector locators if persistent');
          }
        } catch { /* noop */ }
      }, 3000);
    };

    /* -------------------------------------------------------------- §10 --- */
    const locateReady = () => locate('pageContent') && locate('moreButton', locate('topbar') || undefined);

    const scheduleChecks = async (pageId) => {
      // Await page readiness: page-content AND ••• button both locate.
      try {
        await waitFor(locateReady, { timeout: CONFIG.timeouts.pageReady, label: 'page-ready' });
        dbg('page-ready ok', pageId);
      } catch {
        // NOT fatal, and deliberately NOT stamped FAILED. This gate used to
        // write a terminal FAILED here, which meant one slow Notion load killed
        // the page for the whole session with no retry and no visible symptom.
        // Start the watch anyway: it only acts once it actually sees a Default
        // preview, and runAutomation re-locates the ••• button itself at that
        // point. If the page really never becomes usable, the watch expires
        // harmlessly and leaves the status unset so a reload retries.
        warn('page-ready timed out after', CONFIG.timeouts.pageReady, 'ms — watching anyway', pageId);
      }

      startWatch(pageId);
    };

    // Observer-driven watch over one pageId.
    //
    // WHY NOT A FIXED SAMPLE SCHEDULE: v1 sampled the detector at ready+0s,
    // +3s and +8s and then marked the page `exhausted` forever. Notion hydrates
    // the margin comment column lazily — routinely later than 8s on a cold
    // load, and effectively never while the tab is backgrounded. Every one of
    // those misses looked exactly like "the extension does nothing", with no
    // failure and no retry. So instead we watch continuously until we get a
    // definite answer, and we do not let hidden time count against the budget.
    const startWatch = (pageId) => {
      if (activeWatch) activeWatch.stop();

      let stopped = false;
      let evaluating = false;
      let observer = null;
      let backstop = null;
      let rafPending = false;
      let remainingMs = CONFIG.watchWindowMs;
      let countingSince = document.hidden ? null : now();
      let failures = 0;
      let notBefore = now() + CONFIG.settleMs;   // let React finish attaching

      const stop = (why) => {
        if (stopped) return;
        stopped = true;
        try { if (observer) observer.disconnect(); } catch { /* noop */ }
        try { if (backstop) clearInterval(backstop); } catch { /* noop */ }
        observer = null; backstop = null;
        if (activeWatch && activeWatch.pageId === pageId) activeWatch = null;
        dbg('watch stopped', pageId, why);
      };

      // Budget is consumed only while the tab is visible — a page opened in a
      // background tab keeps its full window for when the user focuses it.
      const budgetLeft = () => {
        const spent = countingSince === null ? 0 : now() - countingSince;
        return remainingMs - spent;
      };
      const pauseBudget = () => {
        if (countingSince !== null) { remainingMs -= now() - countingSince; countingSince = null; }
      };
      const resumeBudget = () => { if (countingSince === null) countingSince = now(); };

      const evaluate = async () => {
        if (stopped || evaluating) return;
        if (destroyed || isOff()) { stop('destroyed/off'); return; }
        if (extractPageIdFromPathname(location.href) !== pageId) { stop('navigated away'); return; }
        if (sessionState.has(pageId) && TERMINAL.has(sessionState.get(pageId))) { stop('terminal'); return; }
        if (runsThisSession >= CONFIG.maxRunsPerSession) { stop('run cap'); return; }

        // Never detect or click against a hidden tab: Notion does not render
        // the margin column there, so the detector would read a false NONE.
        if (document.hidden) { pauseBudget(); return; }
        resumeBudget();

        if (running) return;               // a run owns the lock; never stop mid-run

        // Window expired without ever seeing a comment. Stop completely — no
        // background polling. The watch exists to cover Notion's slow, ragged
        // hydration right after a load, not to supervise the page forever. If
        // you add a comment much later, a reload picks it up.
        // Checked BEFORE the notBefore gate on purpose: a 9s retry backoff
        // would otherwise hold us in this function past the end of the budget.
        if (budgetLeft() <= 0) {
          exhaustedThisSession.add(pageId);
          dbg('watch window expired finding only NONE (status left unset)', pageId);
          stop('window expired');
          return;
        }

        if (userIsActive()) return;        // they are typing; retry on a later tick
        if (now() < notBefore) return;     // settling, or backing off after a failed run

        evaluating = true;
        try {
          const state = detectCommentState();
          dbg(`detect ${pageId} → ${state} (${Math.round(budgetLeft())}ms left)`);

          // Definitive Minimal — only reachable if a DOM mode signal is ever
          // configured (CONFIG.locators.modeSignal). No tie to break.
          if (state === 'MINIMAL_ONLY') { dbg('mode signal says Minimal; nothing to do', pageId); stop('looks minimal'); return; }

          // Count icons: comments exist, but this markup is byte-identical for
          // true Minimal and for narrow-viewport Default. Break the tie with
          // the page record (§7b) instead of guessing.
          //
          // Before this existed the extension simply stopped here, which meant
          // a genuinely Default page never got converted for as long as you
          // worked below the ~1100-1150px breakpoint — the second and worse of
          // the two silent no-ops in MAINTENANCE-LOG §2.
          if (state === 'COUNT_ICONS') {
            const mode = modeProbe(pageId);
            if (mode === null) return;             // in flight; it will poke us

            // Database row page — governed by the database layout, same verdict
            // the ••• menu would have given us via "Customize layout", but
            // without opening anything. Terminal: this is a fact about the
            // page, not about the window.
            if (mode === 'DATABASE') {
              dbg('record says database row page → NOT_APPLICABLE (no menu opened)', pageId);
              setStatus(pageId, STATUS.NOT_APPLICABLE);
              stop(STATUS.NOT_APPLICABLE);
              return;
            }

            if (mode === 'DEFAULT') {
              dbg('count icons but record says Default (narrow viewport) → converting', pageId);
              // fall through to runAutomation below
            } else {
              // MINIMAL, or UNKNOWN because the probe failed. Either way, stop
              // and leave the status UNSET — exactly the old behaviour, so a
              // failed probe can never make things worse than not having one.
              dbg(mode === 'MINIMAL' ? 'record confirms Minimal; nothing to do'
                                     : 'mode probe unavailable; treating as minimal (unchanged behaviour)', pageId);
              stop('looks minimal');
              return;
            }
          } else if (state !== 'DEFAULT_VISIBLE') {
            return;                                 // NONE → keep watching
          }

          const result = await runAutomation(pageId);
          if (result === STATUS.DONE) { setStatus(pageId, STATUS.DONE); softVerify(); stop('done'); return; }
          // SKIPPED_BY_USER is NOT a verdict about the page — it means we
          // picked a bad moment. Recording it as terminal is how "I typed a
          // comment and then nothing ever happened" used to occur: the run
          // fired into the user's keystrokes, aborted, and the page was
          // written off for the session. Keep watching instead; userIsActive()
          // will hold us off until they pause.
          if (result === STATUS.SKIPPED_BY_USER) { dbg('aborted by user; staying on watch', pageId); return; }

          // A FAILED run is usually transient — most often a ••• click
          // swallowed because React had not attached handlers yet. Recording it
          // as terminal on the first miss killed the page for the session.
          // Retry with backoff and only give up after maxRunAttempts.
          if (result === STATUS.FAILED) {
            failures++;
            if (failures < CONFIG.maxRunAttempts) {
              const wait = CONFIG.retryBackoffMs[Math.min(failures - 1, CONFIG.retryBackoffMs.length - 1)];
              notBefore = now() + wait;
              dbg(`run failed (${failures}/${CONFIG.maxRunAttempts}); retrying in ${wait}ms`, pageId);
              return;
            }
            setStatus(pageId, STATUS.FAILED); stop('failed'); return;
          }

          if (result && TERMINAL.has(result)) { setStatus(pageId, result); stop(result); return; }
          // result === null → yielded (a user overlay was open). Keep watching.
        } finally {
          evaluating = false;
        }
      };

      const scheduleEvaluate = () => {
        if (rafPending || stopped) return;
        rafPending = true;
        requestAnimationFrame(() => { rafPending = false; evaluate(); });
      };

      observer = new MutationObserver(scheduleEvaluate);
      try {
        observer.observe(document.body, { childList: true, subtree: true, attributes: true });
      } catch { /* backstop still covers us */ }
      backstop = setInterval(evaluate, CONFIG.watchBackstopMs);

      activeWatch = { pageId, stop, evaluate };
      onTeardown(stop);
      dbg('watch started', pageId, `${CONFIG.watchWindowMs}ms visible-time budget`);
      evaluate();
    };

    /* -------------------------------------------------------------- §11 --- */
    if (isDebug()) {
      window.__nmc = {
        config: CONFIG,
        state: () => ({
          sessionState: Object.fromEntries(sessionState),
          runsThisSession,
          running,
          currentRunPageId,
          exhausted: [...exhaustedThisSession],
          pageId: extractPageIdFromPathname(location.href),
          watching: activeWatch ? activeWatch.pageId : null,
          hidden: document.hidden,
        }),
        detect: detectCommentState,
        // Ask the record what the mode really is, ignoring the cache. Returns a
        // promise so it is usable straight from the console.
        mode: () => fetchMode(extractPageIdFromPathname(location.href)),
        modeCache: () => Object.fromEntries(
          [...modeCache].map(([k, v]) => [k, typeof v === 'string' ? v : 'in-flight'])),
        runNow: () => {
          const pageId = extractPageIdFromPathname(location.href);
          if (!pageId) { warn('runNow: no page id in pathname'); return; }
          sessionState.delete(pageId);
          exhaustedThisSession.delete(pageId);
          modeCache.delete(pageId);
          scheduleChecks(pageId);
        },
      };
      dbg('debug surface installed as window.__nmc');
    }

    /* -------------------------------------------------------------- §12 --- */
    onTeardown(() => { window.__nmcInstalled = false; });
    window.addEventListener('popstate', tick);
    onTeardown(() => window.removeEventListener('popstate', tick));

    // Regaining visibility is the single most informative moment there is:
    // Notion only now renders the margin column, so a page that read NONE the
    // whole time it was backgrounded becomes readable. Nudge the live watch,
    // or start one if this page has no verdict yet.
    const onVisibility = () => {
      if (destroyed || document.hidden || isOff()) return;
      const pageId = extractPageIdFromPathname(location.href);
      if (!pageId) return;
      if (sessionState.has(pageId) && TERMINAL.has(sessionState.get(pageId))) return;
      if (activeWatch && activeWatch.pageId === pageId) { activeWatch.evaluate(); return; }
      exhaustedThisSession.delete(pageId);
      scheduleChecks(pageId);
    };
    document.addEventListener('visibilitychange', onVisibility);
    onTeardown(() => document.removeEventListener('visibilitychange', onVisibility));

    pollTimer = setInterval(tick, CONFIG.urlPollMs);
    log('loaded');

    // Evaluate the already-loaded page once at startup.
    lastHref = location.href;
    onNavigate(location.href);
  })();
}
