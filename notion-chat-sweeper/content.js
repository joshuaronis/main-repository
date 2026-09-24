/* Notion Chat Sweeper — content.js  (MAIN world)
 *
 * Runs in the page's own JS context so React's __reactFiber$… expandos are
 * visible. That means NO chrome.* APIs in this file — persistence is
 * localStorage, and anything the popup needs goes out through bridge.js.
 *
 * §0  Sentinel + boot guard      §6  Journal + undo log
 * §1  CONFIG                     §7  Panel UI
 * §2  Logging + debug mirror     §8  Run loop
 * §3  Context learning           §9  Bridge listener
 * §4  findCache + listThreads    §10 Debug surface (window.__ncs)
 * §5  threadOp                   §11 Boot
 */

(() => {
  'use strict';

  /* ══ §0  Sentinel + boot guard ═══════════════════════════════════════════
   * MAIN-world scripts can't check chrome.runtime?.id to detect being orphaned,
   * so a second injection just stands down. Reload the extension, THEN the tab. */
  if (window.__ncsInstalled) return;
  window.__ncsInstalled = true;

  /* ══ §1  CONFIG ═════════════════════════════════════════════════════════ */
  const BUILD = '1.1.0';    // bumped on every change, so the boot log proves
                            // which build a tab actually has loaded

  const CONFIG = {
    chunkSize: 10,          // 42-at-once was verified, but only on no-op restores
    maxPerRun: 200,         // PHASE 3: cap lifted
    confirmThreshold: 25,   // second confirmation above this many
    retryBackoffMs: [1000, 3000, 8000],
    dryRun: false,          // PHASE 2: armed. Deletes are real from here on.
    undoRunsKept: 5,
    journalMax: 2000,
    restoreMaxAgeDays: 30,  // hides old restore candidates; does NOT delete them
    broomVisible: true
  };

  const K = {               // localStorage keys (per-origin, not per-tab)
    pos: 'ncs_pos',
    cfg: 'ncs_config',
    undo: 'ncs_undo',
    journal: 'ncs_journal',
    forgotten: 'ncs_forgotten'
  };

  const readJSON = (key, fallback) => {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  };
  const writeJSON = (key, value) => localStorage.setItem(key, JSON.stringify(value));

  // Only user-tweakable bits are persisted; the safety values stay in code.
  Object.assign(CONFIG, (() => {
    const saved = readJSON(K.cfg, {});
    const out = {};
    if (typeof saved.broomVisible === 'boolean') out.broomVisible = saved.broomVisible;
    return out;
  })());
  const saveCfg = () => writeJSON(K.cfg, { broomVisible: CONFIG.broomVisible });

  /* ══ §2  Logging + debug mirror ═════════════════════════════════════════
   * Console output is awkward to copy out of DevTools, so the last 20 events
   * also live in document.documentElement.dataset.ncsLog — one copy-paste. */
  const LOG_MAX = 20;
  const logBuf = [];

  function log(...parts) {
    const msg = parts
      .map((p) => (typeof p === 'string' ? p : (() => {
        try { return JSON.stringify(p); } catch (e) { return String(p); }
      })()))
      .join(' ');
    const stamp = new Date().toTimeString().slice(0, 8);
    logBuf.push(stamp + ' ' + msg);
    if (logBuf.length > LOG_MAX) logBuf.shift();
    try {
      document.documentElement.dataset.ncsLog = JSON.stringify(logBuf);
    } catch (e) { /* ignore */ }
    console.log('[NCS]', msg);
  }

  /* ══ §3  Context learning ═══════════════════════════════════════════════
   * Every header and field the real client sends is included when we have it.
   * Verified optional — but only on no-op restores, so we don't lean on that.
   * A value we never see is simply omitted. Never blocks, never guesses. */
  const WANTED = [
    'x-notion-active-user-header',
    'x-notion-space-id',
    'notion-client-version',
    'notion-audit-log-platform'
  ];
  const learned = Object.create(null);
  const origFetch = window.fetch;

  function absorbHeaders(h) {
    if (!h) return;
    try {
      if (typeof h.forEach === 'function' && !Array.isArray(h)) {
        h.forEach((v, k) => {
          const lk = String(k).toLowerCase();
          if (WANTED.indexOf(lk) !== -1 && v) learned[lk] = String(v);
        });
        return;
      }
      const pairs = Array.isArray(h) ? h : Object.keys(h).map((k) => [k, h[k]]);
      for (const [k, v] of pairs) {
        const lk = String(k).toLowerCase();
        if (WANTED.indexOf(lk) !== -1 && v) learned[lk] = String(v);
      }
    } catch (e) { /* ignore */ }
  }

  function wrapFetch() {
    window.fetch = function (input, init) {
      try {
        const url = typeof input === 'string' ? input
          : (input && typeof input.url === 'string' ? input.url : '');
        if (url.indexOf('/api/v3/') !== -1) {
          if (input && input.headers) absorbHeaders(input.headers);
          if (init && init.headers) absorbHeaders(init.headers);
        }
      } catch (e) { /* never let learning break a page request */ }
      return origFetch.apply(this, arguments);
    };
  }

  // Builds the {headers, spaceId} passed to threadOp. Specified fallbacks only.
  function buildCtx() {
    const c = findCache();
    const headers = {};
    const missing = [];

    const put = (key, value) => { if (value) headers[key] = String(value); else missing.push(key); };
    put('x-notion-active-user-header',
      learned['x-notion-active-user-header'] || (c && c.userId));
    put('x-notion-space-id',
      learned['x-notion-space-id'] || (c && c.spaceId));
    put('notion-client-version',
      learned['notion-client-version'] || document.documentElement.dataset.notionVersion);
    put('notion-audit-log-platform',
      learned['notion-audit-log-platform']); // no sane fallback — omit rather than guess

    if (missing.length) log('ctx: proceeding without', missing.join(','));
    const spaceId = headers['x-notion-space-id'] || undefined;
    return { headers, spaceId };
  }

  /* ══ §4  findCache + listThreads ═══════════════════════════════════════
   * Enumeration comes from Notion's in-memory record cache, not the DOM. That
   * gives real titles, timestamps and `alive` state for free — which is what
   * makes age-based selection and sorting possible at all. */
  let cachedCtx = null;

  function findCache() {
    if (cachedCtx && cachedCtx.cache &&
        typeof cachedCtx.cache.forEachRecordOfTable === 'function') return cachedCtx;

    const probe = (el) => {
      const k = Object.keys(el).find((key) => key.startsWith('__reactFiber$'));
      if (!k) return null;
      let f = el[k];
      for (let i = 0; i < 40 && f; i++, f = f.return) {
        const p = f.memoizedProps;
        if (!p) continue;
        let values;
        try { values = Object.values(p); } catch (e) { continue; }
        for (const v of values) {
          if (v && typeof v === 'object' && v.inMemoryRecordCache &&
              typeof v.inMemoryRecordCache.forEachRecordOfTable === 'function' &&
              typeof v.userId === 'string') {
            return {
              cache: v.inMemoryRecordCache,
              userId: v.userId,
              spaceId: v.model && v.model.space_id
            };
          }
        }
      }
      return null;
    };

    // Sidebar first purely for speed; the body fallback keeps this working when
    // the Chat tab isn't open.
    for (const root of [document.getElementById('sidebar-tabpanel-chats'), document.body]) {
      if (!root) continue;
      for (const el of root.querySelectorAll('*')) {
        let hit = null;
        try { hit = probe(el); } catch (e) { continue; }
        if (hit) { cachedCtx = hit; return hit; }
      }
    }
    return null;
  }

  /* `data`, `alive`, `created_time`, `updated_time` are LAZY — reading
   * model.data directly returns undefined. They must come through
   * getKeyValue(). `id` and `table` are plain properties. Don't "simplify". */
  function listThreads() {
    const ctx = findCache();
    if (!ctx) return null;
    const kv = (m, key) => { try { return m.getKeyValue(key); } catch (e) { return undefined; } };
    const out = [];
    try {
      ctx.cache.forEachRecordOfTable({
        userId: ctx.userId,
        table: 'thread',
        fn: ({ model }) => {
          if (!model || typeof model.id !== 'string') return;
          const data = kv(model, 'data') || {};
          out.push({
            id: model.id,
            title: data.title || '(untitled)',
            icon: data.icon,
            alive: kv(model, 'alive') !== false,
            created: kv(model, 'created_time'),
            updated: kv(model, 'updated_time'),
            type: kv(model, 'type')
          });
        }
      });
    } catch (e) {
      log('listThreads failed:', e.message);
      return null;
    }
    return out.sort((a, b) => (b.updated || 0) - (a.updated || 0));
  }

  /* DOM walk — cross-check only. Agents ("Sultan", "New agent") yield null and
   * drop out automatically; pinning moves a row rather than cloning it. */
  const threadIdFromEl = (el) => {
    const k = Object.keys(el).find((key) => key.startsWith('__reactFiber$'));
    if (!k) return null;
    let f = el[k];
    for (let i = 0; i < 30 && f; i++, f = f.return) {
      const p = f.memoizedProps;
      if (p && p.threadStore && typeof p.threadStore.id === 'string') return p.threadStore.id;
    }
    return null;
  };

  function domThreadIds() {
    const root = document.getElementById('sidebar-tabpanel-chats');
    if (!root) return null;                    // Chat tab not open — skip the check
    const ids = new Set();
    for (const el of root.querySelectorAll('*')) {
      let id = null;
      try { id = threadIdFromEl(el); } catch (e) { continue; }
      if (id) ids.add(id);
    }
    return ids;
  }

  /* ══ §5  threadOp ══════════════════════════════════════════════════════ */
  async function threadOp(ids, alive, ctx = {}) {
    const list = [].concat(ids);
    const ops = list.map((id) => ({
      pointer: ctx.spaceId ? { table: 'thread', id, spaceId: ctx.spaceId }
                           : { table: 'thread', id },
      path: [],
      command: 'update',
      args: alive
        ? { alive: true }
        : { alive: false, current_inference_id: null, current_inference_lease_expiration: null }
    }));
    const tx = {
      id: crypto.randomUUID(),
      debug: {
        userAction: 'agentChat.threadPersistenceActions.deleteThread',
        clientCommitTimeMs: Date.now()
      },
      operations: ops
    };
    if (ctx.spaceId) tx.spaceId = ctx.spaceId;

    try {
      // origFetch, not window.fetch: skips our own learning wrapper. The URL is
      // relative, so this is same-origin by construction — nothing leaves Notion.
      const res = await origFetch('/api/v3/saveTransactionsFanout', {
        method: 'POST',
        credentials: 'include',
        headers: Object.assign({ 'content-type': 'application/json' }, ctx.headers || {}),
        body: JSON.stringify({ requestId: crypto.randomUUID(), transactions: [tx] })
      });
      return { ok: res.ok, status: res.status, body: res.ok ? null : await res.text() };
    } catch (e) {
      return { ok: false, status: 'ERR', body: e.message };
    }
  }

  /* ══ §6  Journal + undo log ════════════════════════════════════════════
   * Dead threads stay in the cache with their titles until a page reload, then
   * the server stops syncing them and they're gone. The journal is the only
   * bridge across that reload — and it also catches deletions made outside the
   * extension, by hand or on the phone. */
  function updateJournal(aliveRows) {
    try {
      const j = readJSON(K.journal, {}) || {};
      const now = Date.now();
      for (const r of aliveRows) {
        j[r.id] = { title: r.title, created: r.created, updated: r.updated, lastSeen: now };
      }
      const ids = Object.keys(j);
      if (ids.length > CONFIG.journalMax) {
        ids.sort((a, b) => (j[a].lastSeen || 0) - (j[b].lastSeen || 0));
        for (let i = 0; i < ids.length - CONFIG.journalMax; i++) delete j[ids[i]];
      }
      writeJSON(K.journal, j);
    } catch (e) {
      log('journal write failed:', e.message);
    }
  }

  const readRuns = () => readJSON(K.undo, []) || [];

  /* Forgetting drops OUR record of a chat. It cannot delete anything from
     Notion — deletion there is a soft flag and dead threads never reach the
     Trash — so the chat simply stays deleted and invisible, and we lose the
     only handle that could have restored it. Genuinely irreversible for us. */
  const FORGET_TTL_MS = 7 * 86400000;

  function readForgotten() {
    const f = readJSON(K.forgotten, {}) || {};
    // Entries only need to outlive the current page: after a reload the record
    // is gone from Notion's cache and we've already purged journal and log, so
    // nothing can resurface. A week is a generous margin.
    const cutoff = Date.now() - FORGET_TTL_MS;
    let dropped = false;
    for (const id of Object.keys(f)) if (f[id] < cutoff) { delete f[id]; dropped = true; }
    if (dropped) writeJSON(K.forgotten, f);
    return f;
  }

  function forget(ids) {
    const now = Date.now();
    // 1. Suppression list — covers records still sitting dead in Notion's cache.
    const f = readForgotten();
    for (const id of ids) f[id] = now;
    writeJSON(K.forgotten, f);
    // 2. Out of the journal.
    const j = readJSON(K.journal, {}) || {};
    for (const id of ids) delete j[id];
    writeJSON(K.journal, j);
    // 3. Out of the undo log, dropping any run left with nothing in it.
    const runs = readRuns()
      .map((r) => Object.assign({}, r, { items: r.items.filter((i) => !ids.includes(i.id)) }))
      .filter((r) => r.items.length);
    writeJSON(K.undo, runs);
    log('forgot', ids.length, 'chat(s) — no longer restorable');
  }

  // Hard rule 4: this must succeed before a run starts. Throws on failure.
  function startRun(targets) {
    const run = {
      runId: crypto.randomUUID(),
      startedAt: new Date().toISOString(),
      items: targets.map((t) => ({ id: t.id, title: t.title, status: 'pending' }))
    };
    const all = readRuns();
    all.unshift(run);
    writeJSON(K.undo, all.slice(0, CONFIG.undoRunsKept));
    return run;
  }

  function persistRun(run) {
    try {
      const all = readRuns();
      const i = all.findIndex((r) => r.runId === run.runId);
      if (i === -1) all.unshift(run); else all[i] = run;
      writeJSON(K.undo, all.slice(0, CONFIG.undoRunsKept));
    } catch (e) {
      log('undo log update failed:', e.message);
    }
  }

  /* ══ §7  Panel UI ══════════════════════════════════════════════════════ */
  const CSS = `
.ncs-launcher{position:fixed;z-index:2147483000;width:34px;height:34px;border-radius:50%;
  background:#1f1f1f;color:#e8e8e8;border:1px solid #3a3a3a;display:flex;align-items:center;
  justify-content:center;cursor:grab;font-size:15px;user-select:none;
  box-shadow:0 2px 10px rgba(0,0,0,.4);font-family:system-ui,sans-serif;color-scheme:dark}
.ncs-launcher.ncs-dragging{cursor:grabbing}
.ncs-panel{position:fixed;z-index:2147482999;width:340px;max-height:72vh;background:#1f1f1f;
  color:#e8e8e8;border:1px solid #3a3a3a;border-radius:8px;display:flex;flex-direction:column;
  font-family:system-ui,-apple-system,sans-serif;font-size:12px;
  box-shadow:0 8px 32px rgba(0,0,0,.5);overflow:hidden;color-scheme:dark}
.ncs-hidden{display:none !important}
.ncs-head{display:flex;align-items:center;gap:8px;padding:9px 11px;border-bottom:1px solid #3a3a3a}
.ncs-title{font-weight:600;font-size:12px}
.ncs-count{color:#9a9a9a;font-size:11px;flex:1}
.ncs-btn{background:#2a2a2a;color:#e8e8e8;border:1px solid #3a3a3a;border-radius:5px;
  padding:4px 8px;font-size:11px;cursor:pointer;font-family:inherit;line-height:1.2;
  white-space:nowrap;flex-shrink:0}
.ncs-btn:hover{background:#343434}
.ncs-btn:disabled{opacity:.45;cursor:default}
.ncs-btn.ncs-btn-on{background:#e0785a;color:#111;border-color:#e0785a;font-weight:600}
.ncs-btn.ncs-btn-on:hover{background:#e88a6e}
.ncs-btn-icon{padding:2px 6px}
.ncs-btn-primary{background:#e0785a;color:#111;border:none;font-weight:600;flex:1}
.ncs-btn-primary:hover{background:#e88a6e}
.ncs-banner{padding:7px 11px;border-bottom:1px solid #3a3a3a;background:rgba(224,168,60,.12);
  color:#e8b45a;font-size:11px;line-height:1.45}
/* Informational, NOT a warning. Amber is reserved for .ncs-banner so that a
   real problem never has to compete with routine sidebar virtualisation. */
.ncs-note{padding:7px 11px;border-bottom:1px solid #3a3a3a;color:#8a8a8a;
  font-size:11px;line-height:1.45}
/* Which mode we're in must never be a guess: blue = safe, red = armed. */
.ncs-mode{padding:5px 11px;border-bottom:1px solid #3a3a3a;font-size:11px;
  font-weight:600;letter-spacing:.02em}
.ncs-mode-dry{background:rgba(90,150,224,.12);color:#8ab4e8}
.ncs-mode-live{background:rgba(224,90,90,.14);color:#f08a8a}
.ncs-frow{display:flex;gap:5px;padding:8px 11px;border-bottom:1px solid #3a3a3a}
.ncs-crow{display:flex;gap:5px;align-items:center;padding:0 11px 8px}
.ncs-crow.ncs-crow-top{padding-top:8px}
.ncs-crow.ncs-crow-end{border-bottom:1px solid #3a3a3a}
.ncs-input{background:#2a2a2a;color:#e8e8e8;border:1px solid #3a3a3a;border-radius:5px;
  padding:4px 7px;font-size:11px;font-family:inherit}
.ncs-input-flex{flex:1;min-width:0}
/* Wide enough for three digits. Spinners are hidden because they overlay the
   text at this size and were clipping the value. */
.ncs-input-num{width:48px;flex-shrink:0}
.ncs-input-num::-webkit-inner-spin-button,
.ncs-input-num::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
.ncs-spacer{flex:1}
.ncs-label{color:#9a9a9a;font-size:11px}
.ncs-select{background:#2a2a2a;color:#e8e8e8;border:1px solid #3a3a3a;border-radius:5px;
  padding:3px 4px;font-size:11px;font-family:inherit}
.ncs-tabs{display:flex;border-bottom:1px solid #3a3a3a}
.ncs-tab{flex:1;background:transparent;border:none;border-bottom:2px solid transparent;
  color:#9a9a9a;padding:7px 0;font-size:11px;font-family:inherit;cursor:pointer}
.ncs-tab:hover{color:#e8e8e8;background:rgba(255,255,255,.03)}
.ncs-tab.ncs-tab-on{color:#e8e8e8;border-bottom-color:#e0785a;font-weight:600}
.ncs-view{display:flex;flex-direction:column;flex:1;min-height:0;overflow:hidden}
.ncs-info{padding:8px 11px;color:#8a8a8a;font-size:11px;line-height:1.45;
  border-bottom:1px solid #3a3a3a}
.ncs-src{color:#6f6f6f;font-size:9px;letter-spacing:.04em;flex-shrink:0;text-transform:uppercase}
.ncs-list{overflow-y:auto;flex:1;min-height:80px}
.ncs-row{display:flex;align-items:center;gap:8px;padding:5px 11px;cursor:pointer;user-select:none}
.ncs-row:hover{background:rgba(255,255,255,.04)}
.ncs-row.ncs-on{background:rgba(224,120,90,.14)}
.ncs-row.ncs-on:hover{background:rgba(224,120,90,.2)}
.ncs-check{width:13px;height:13px;flex-shrink:0;border-radius:3px;border:1px solid #3a3a3a;
  color:#111;font-size:10px;line-height:13px;text-align:center}
.ncs-on .ncs-check{border-color:#e0785a;background:#e0785a}
.ncs-rtitle{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ncs-rtime{color:#9a9a9a;font-size:10px;flex-shrink:0}
.ncs-empty{color:#9a9a9a;padding:14px 11px;text-align:center}
.ncs-foot{padding:9px 11px;border-top:1px solid #3a3a3a;display:flex;flex-direction:column;gap:7px}
.ncs-status{color:#9a9a9a;font-size:11px;line-height:1.4}
.ncs-bar{display:flex;gap:5px}
`;

  function installStyles() {
    // Constructable stylesheet first: it's pure CSSOM, so a page style-src CSP
    // can't block it the way it could block an injected <style> element.
    try {
      const sheet = new CSSStyleSheet();
      sheet.replaceSync(CSS);
      document.adoptedStyleSheets = document.adoptedStyleSheets.concat(sheet);
      return;
    } catch (e) { /* fall through */ }
    const el = document.createElement('style');
    el.textContent = CSS;                       // textContent, never innerHTML
    (document.head || document.documentElement).appendChild(el);
  }

  // Every node is built with createElement + textContent. Trusted Types are
  // active on Notion: no innerHTML, no insertAdjacentHTML, no injected <script>.
  const E = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };
  const btn = (label, cls, tip) => {
    const b = E('button', 'ncs-btn' + (cls ? ' ' + cls : ''), label);
    b.type = 'button';
    if (tip) b.title = tip;
    return b;
  };

  function relTime(ms) {
    if (!ms) return '';
    const d = Date.now() - ms;
    if (d < 0) return 'now';
    const m = Math.floor(d / 60000);
    if (m < 1) return 'now';
    if (m < 60) return m + 'm';
    const h = Math.floor(m / 60);
    if (h < 24) return h + 'h';
    const dy = Math.floor(h / 24);
    if (dy < 7) return dy + 'd';
    if (dy < 30) return Math.floor(dy / 7) + 'w';
    if (dy < 365) return Math.floor(dy / 30) + 'mo';
    return Math.floor(dy / 365) + 'y';
  }
  const absTime = (ms) => (ms ? new Date(ms).toLocaleString() : 'no timestamp');

  // ── state ──
  let rows = [];              // alive threads, current sort order
  let known = new Set();      // every id enumerated this scan — hard rule 1 gate
  const sel = new Set();
  const delAnchor = { id: null };   // shift-click anchors, one per tab
  const resAnchor = { id: null };
  let filter = '';
  let ageDays = null;         // null = age filter off; otherwise "older than N days"
  let sortMode = 'newest';
  let running = false;
  let stopRequested = false;
  let lastFailed = [];
  let statusMsg = null;       // sticky footer message; survives a re-render
  let rcands = [];            // restore candidates, newest first
  let rHidden = 0;            // aged-out candidates, hidden but not forgotten
  const rsel = new Set();     // restore-tab selection, separate from `sel`
  /* id -> the alive value the server has CONFIRMED for it. Notion's record
     cache lags a write by up to a second or two, so a 200 is better evidence
     than a fresh read. Entries drop out as soon as the cache agrees. */
  const confirmedAlive = new Map();
  let panelTouched = false;   // proxy for "panel has focus" without stealing it

  // ── nodes ──
  const launcher = E('div', 'ncs-launcher', '🧹');
  launcher.title = 'Chat Sweeper — click to open, drag to move';
  launcher.setAttribute('data-darkreader-ignore', '');

  const panel = E('div', 'ncs-panel ncs-hidden');
  panel.setAttribute('data-darkreader-ignore', '');

  const savedPos = readJSON(K.pos, null);
  if (savedPos && savedPos.top) {
    launcher.style.top = savedPos.top;
    launcher.style.left = savedPos.left;
    launcher.style.right = 'auto';
    launcher.style.bottom = 'auto';
  } else {
    launcher.style.top = '56px';
    launcher.style.right = '16px';
  }

  const head = E('div', 'ncs-head');
  const countEl = E('div', 'ncs-count', '…');
  const rescanB = btn('↻', 'ncs-btn-icon', 'Rescan');
  const closeB = btn('✕', 'ncs-btn-icon', 'Close (Esc)');
  head.append(E('div', 'ncs-title', 'Chat Sweeper'), countEl, rescanB, closeB);

  const banner = E('div', 'ncs-banner ncs-hidden');   // amber: something is wrong
  const note = E('div', 'ncs-note ncs-hidden');       // grey: just so you know
  // Shown while dry-running, and while a low cap is in force. Goes away only
  // once the extension is both armed and uncapped.
  const modeBadge = E('div', 'ncs-mode');
  function syncMode() {
    const capped = CONFIG.maxPerRun <= 5;
    modeBadge.className = 'ncs-mode ' + (CONFIG.dryRun ? 'ncs-mode-dry' : 'ncs-mode-live');
    modeBadge.textContent = CONFIG.dryRun
      ? 'DRY RUN — no requests will be sent'
      : `LIVE — deletes are real, capped at ${CONFIG.maxPerRun} per run`;
    if (!CONFIG.dryRun && !capped) modeBadge.classList.add('ncs-hidden');
  }

  const fRow = E('div', 'ncs-frow');
  const fIn = E('input', 'ncs-input ncs-input-flex');
  fIn.type = 'text';
  fIn.placeholder = 'filter titles…  ( / )';
  const fAll = btn('+ shown', null, 'Select every row currently shown');
  const fNone = btn('− shown', null, 'Deselect every row currently shown');
  fRow.append(fIn, fAll, fNone);

  const cRow1 = E('div', 'ncs-crow ncs-crow-top');
  const bAll = btn('all', null, 'Select all chats');
  const bNone = btn('none', null, 'Clear the selection');
  const bInvert = btn('invert', null, 'Invert the selection across all chats');
  const sortSel = E('select', 'ncs-select');
  for (const [v, t] of [['newest', 'newest first'], ['oldest', 'oldest first'], ['title', 'by title']]) {
    const o = E('option', null, t);
    o.value = v;
    sortSel.append(o);
  }
  sortSel.title = 'Sort order';
  cRow1.append(bAll, bNone, bInvert, E('div', 'ncs-spacer'), sortSel);

  const cRow2 = E('div', 'ncs-crow ncs-crow-end');
  const bNewest = btn('newest', null, 'Select the N most recently updated shown chats');
  const nIn = E('input', 'ncs-input ncs-input-num');
  nIn.type = 'number';
  nIn.min = '1';
  nIn.value = '10';
  const bOlder = btn('older than', null,
    'Show only chats not updated in N days (click again to clear)');
  const dIn = E('input', 'ncs-input ncs-input-num');
  dIn.type = 'number';
  dIn.min = '1';
  dIn.value = '30';
  cRow2.append(bNewest, nIn, E('div', 'ncs-spacer'), bOlder, dIn, E('div', 'ncs-label', 'days'));

  const list = E('div', 'ncs-list');

  const foot = E('div', 'ncs-foot');
  const status = E('div', 'ncs-status', '0 selected');
  const bar = E('div', 'ncs-bar');
  const bDel = btn('Delete', 'ncs-btn-primary');
  const bStop = btn('Stop', 'ncs-hidden');
  const bRetry = btn('Retry failed', 'ncs-hidden');
  const bUndo = btn('Undo last', null, 'Restore everything deleted in the last run');
  bar.append(bDel, bStop, bRetry, bUndo);
  foot.append(status, bar);

  // ── Restore view ──
  const rList = E('div', 'ncs-list');
  const rInfo = E('div', 'ncs-info');
  const rFoot = E('div', 'ncs-foot');
  const rStatus = E('div', 'ncs-status', '');
  const rBar = E('div', 'ncs-bar');
  const bRestore = btn('Restore', 'ncs-btn-primary');
  const bForget = btn('Forget', null,
    'Drop this extension\'s record of the selected chats. They stay deleted in Notion and can never be restored after this.');
  const bDownload = btn('Download record', null,
    'Save the undo log and journal as JSON. Convenience, not the safety net — Restore is.');
  rBar.append(bRestore, bForget);
  const rBar2 = E('div', 'ncs-bar');
  const runSel = E('select', 'ncs-select');
  runSel.style.flex = '1';
  runSel.style.minWidth = '0';
  const bUndoRun = btn('Undo run');
  rBar2.append(runSel, bUndoRun);
  rFoot.append(rStatus, rBar, rBar2);

  const rCtl = E('div', 'ncs-crow ncs-crow-top ncs-crow-end');
  const rAll = btn('all', null, 'Select every recoverable chat');
  const rNone = btn('none', null, 'Clear the selection');
  rCtl.append(rAll, rNone, E('div', 'ncs-spacer'), bDownload);

  const tabs = E('div', 'ncs-tabs');
  const tabDel = E('button', 'ncs-tab ncs-tab-on', 'Delete');
  const tabRes = E('button', 'ncs-tab', 'Restore');
  tabDel.type = 'button';
  tabRes.type = 'button';
  tabs.append(tabDel, tabRes);

  const deleteView = E('div', 'ncs-view');
  deleteView.append(fRow, cRow1, cRow2, list, foot);
  const restoreView = E('div', 'ncs-view ncs-hidden');
  restoreView.append(rInfo, rCtl, rList, rFoot);

  panel.append(head, tabs, banner, note, modeBadge, deleteView, restoreView);

  // ── rendering ──
  // "older than N days" narrows the VIEW rather than ticking rows, so it
  // composes with the title filter and with "+ shown".
  /* Shared by both tabs. MOVING anchor — it follows EVERY click, shift-clicks
     included, so an overshot range trims from the end you just clicked. See
     §8 test 6 in the spec and MAINTENANCE-LOG.md before changing this. */
  function rangeClick(shiftKey, items, i, selSet, anchor) {
    const id = items[i].id;
    const at = anchor.id ? items.findIndex((x) => x.id === anchor.id) : -1;
    if (shiftKey && at !== -1) {
      const want = !selSet.has(id);
      for (let j = Math.min(at, i); j <= Math.max(at, i); j++) {
        if (want) selSet.add(items[j].id); else selSet.delete(items[j].id);
      }
    } else {
      if (selSet.has(id)) selSet.delete(id); else selSet.add(id);
    }
    anchor.id = id;
  }

  const matches = (r) => {
    if (filter && !r.title.toLowerCase().includes(filter)) return false;
    if (ageDays != null && (r.updated || 0) >= Date.now() - ageDays * 86400000) return false;
    return true;
  };
  const visible = () => rows.filter(matches);
  const filtering = () => !!filter || ageDays != null;

  function sortRows() {
    if (sortMode === 'title') {
      rows.sort((a, b) => a.title.localeCompare(b.title));
    } else if (sortMode === 'oldest') {
      rows.sort((a, b) => (a.updated || 0) - (b.updated || 0));
    } else {
      rows.sort((a, b) => (b.updated || 0) - (a.updated || 0));
    }
  }

  function render() {
    while (list.firstChild) list.removeChild(list.firstChild);
    const vis = visible();

    if (!vis.length) {
      list.append(E('div', 'ncs-empty', rows.length ? 'nothing matches that filter' : 'no chats found'));
    }

    vis.forEach((r, i) => {
      const on = sel.has(r.id);
      const row = E('div', 'ncs-row' + (on ? ' ncs-on' : ''));
      row.append(E('span', 'ncs-check', on ? '✓' : ''));
      const t = E('div', 'ncs-rtitle', r.title);
      t.title = r.title + '\n' + absTime(r.updated);
      row.append(t);
      const time = E('div', 'ncs-rtime', relTime(r.updated));
      time.title = absTime(r.updated);
      row.append(time);

      row.onclick = (e) => { rangeClick(e.shiftKey, vis, i, sel, delAnchor); touch(); };
      list.append(row);
    });

    countEl.textContent = rows.length + ' chat' + (rows.length === 1 ? '' : 's') +
      (filtering() ? ` · ${vis.length} shown` : '');
    const shown = vis.filter((r) => sel.has(r.id)).length;
    status.textContent = statusMsg ||
      (sel.size + ' selected' + (filtering() ? ` (${shown} shown)` : ''));
    bDel.textContent = 'Delete ' + sel.size + (CONFIG.dryRun ? ' (dry)' : '');
    bDel.disabled = !sel.size || running;
    bUndo.disabled = running;
    bRetry.classList.toggle('ncs-hidden', running || !lastFailed.length);
    paintRestore();          // keeps the other tab's buttons in step
  }

  function fill(el, lines) {
    while (el.firstChild) el.removeChild(el.firstChild);
    if (!lines.length) { el.classList.add('ncs-hidden'); return; }
    lines.forEach((line, i) => {
      if (i) el.append(document.createElement('br'));
      el.append(document.createTextNode(line));
    });
    el.classList.remove('ncs-hidden');
  }

  // Any user action that changes what's selected or shown drops the sticky
  // message and goes back to the live selection summary.
  const touch = () => { statusMsg = null; render(); };

  function say(msg, holdMs) {
    statusMsg = msg;
    clearTimeout(say.timer);
    if (holdMs) say.timer = setTimeout(touch, holdMs);
    render();
  }

  // Transient status text — the scan is synchronous, so without this a rescan
  // finishes before the browser can paint and looks like it did nothing.
  const flash = (msg) => say(msg, 1800);

  /* Every read of the thread list goes through here.
     Notion's record cache lags a confirmed write — after a successful delete it
     still reports the thread as alive for a second or more, and after a restore
     it still reports it dead. Trust the 200 until the cache agrees, otherwise
     the panel shows a chat it just deleted (and hides one it just brought
     back). Overrides drain themselves. See MAINTENANCE-LOG.md. */
  const CONFIRM_TTL_MS = 60000;

  // Cheap fingerprint of the live set, used by the poll to decide whether a
  // full rescan (which includes the expensive sidebar DOM walk) is warranted.
  const rawSignature = (all) => all.filter((r) => r.alive).map((r) => r.id).sort().join('|');
  let lastSig = null;

  function readThreads() {
    const all = listThreads();
    if (all === null) return null;
    lastSig = rawSignature(all);      // before overrides — this tracks the cache
    // An override for a thread the cache never returns (restoring something
    // deleted long ago) would otherwise sit here forever. The cache catches up
    // in about a second, so a minute is a generous ceiling.
    const now = Date.now();
    for (const [id, v] of confirmedAlive) {
      if (now - v.at > CONFIRM_TTL_MS) confirmedAlive.delete(id);
    }
    for (const r of all) {
      const v = confirmedAlive.get(r.id);
      if (!v) continue;
      if (r.alive === v.alive) confirmedAlive.delete(r.id);
      else r.alive = v.alive;
    }
    return all;
  }

  function rescan() {
    const all = readThreads();
    if (all === null) {
      rows = [];
      known = new Set();
      fill(banner, ['Could not reach Notion\'s record cache. Open the Chat tab and reload the page (⌘R).']);
      fill(note, []);
      log('rescan: findCache/listThreads returned nothing');
      render();
      refreshRestore(null);
      return;
    }

    known = new Set(all.map((r) => r.id));
    rows = all.filter((r) => r.alive);
    sortRows();
    for (const id of [...sel]) if (!rows.some((r) => r.id === id)) sel.delete(id);
    if (delAnchor.id && !rows.some((r) => r.id === delAnchor.id)) delAnchor.id = null;

    // Cross-check against the sidebar. Never present a list that silently
    // disagrees with what he can see.
    const domIds = domThreadIds();
    const warnings = [];
    const notes = [];
    if (domIds) {
      // Ids with a live override are excluded: we just deleted them and the
      // sidebar hasn't caught up. Warning there would fire on every bulk run.
      const missing = [...domIds].filter(
        (id) => !rows.some((r) => r.id === id) && !confirmedAlive.has(id));
      const unrendered = rows.filter((r) => !domIds.has(r.id)).length;
      if (missing.length) {
        // The direction that actually matters: the sidebar knows about a chat
        // this list doesn't. Everything else is routine virtualisation.
        warnings.push(`⚠ ${missing.length} chat(s) visible in the sidebar are missing from this list — sidebar ${domIds.size}, list ${rows.length}.`);
      }
      if (unrendered) {
        // rows.length - unrendered, NOT domIds.size: the latter would count any
        // sidebar row that isn't in our list at all (the warning case above).
        notes.push(`Sidebar is showing ${rows.length - unrendered} of these ${rows.length} rows — Notion drops the ones you scroll past. The list above is complete.`);
      }
      log('scan: cache', rows.length, 'dom', domIds.size,
        'dead', all.length - rows.length, 'pending', confirmedAlive.size);
    } else {
      log('scan: cache', rows.length, 'pending', confirmedAlive.size,
        '(chat tab closed — no cross-check)');
    }
    fill(banner, warnings);
    fill(note, notes);

    updateJournal(rows);
    render();
    refreshRestore(all);
    emitState();
  }

  /* ── Restore tab ──
     Three sources feed one list, deduplicated by id and richest-first. Chats
     deleted BEFORE the extension was installed are absent from all three and
     cannot be recovered — nothing on this machine records that they existed. */
  function restoreCandidates(all) {
    const liveIds = new Set(all.filter((r) => r.alive).map((r) => r.id));
    const j = readJSON(K.journal, {}) || {};
    const runs = readRuns();

    /* Best estimate of when each chat WENT AWAY. An undo-log run is exact; the
       journal's lastSeen is the last time the panel saw it alive, which is close
       enough. A thread's own updated_time is NOT a deletion time — a chat
       untouched for months can be deleted a minute ago — so it is the last
       resort only. Getting this wrong would age out chats you just deleted. */
    const goneAt = new Map();
    for (const run of runs) {
      const at = Date.parse(run.startedAt) || 0;
      for (const it of run.items) {
        if (it.status === 'deleted' && !goneAt.has(it.id)) goneAt.set(it.id, at);
      }
    }
    for (const id of Object.keys(j)) {
      if (!goneAt.has(id) && j[id].lastSeen) goneAt.set(id, j[id].lastSeen);
    }

    const forgotten = readForgotten();
    const out = new Map();
    const add = (id, title, src, fallbackWhen) => {
      if (liveIds.has(id) || out.has(id) || forgotten[id]) return;   // first source wins
      out.set(id, { id, title: title || '(untitled)', src,
        when: goneAt.get(id) || fallbackWhen || 0 });
    };

    // a. Dead in the cache right now — best data, still carries the real title.
    //    Free, but only until a page reload; then Notion stops syncing it.
    for (const r of all) if (!r.alive) add(r.id, r.title, 'session', r.updated);
    // b. The journal — survives a reload, and catches deletions made by hand or
    //    on the phone.
    for (const id of Object.keys(j)) add(id, j[id].title, 'journal', j[id].updated);
    // c. The undo log, for anything already evicted from the journal.
    for (const run of runs) {
      const at = Date.parse(run.startedAt) || 0;
      for (const it of run.items) {
        if (it.status === 'deleted') add(it.id, it.title, 'log', at);
      }
    }

    /* Age out the display so the list stays usable — the journal keeps growing
       to journalMax regardless, and Download record still contains everything.
       Hiding, not deleting: this must never destroy the only record that a chat
       existed. Session entries are exempt; they are by definition from today. */
    const cutoff = Date.now() - CONFIG.restoreMaxAgeDays * 86400000;
    const list = [...out.values()];
    const shown = list.filter((c) => c.src === 'session' || (c.when || 0) >= cutoff);
    rHidden = list.length - shown.length;
    return shown.sort((a, b) => (b.when || 0) - (a.when || 0));
  }

  function refreshRestore(all) {
    rcands = all ? restoreCandidates(all) : [];
    // Every one of these ids came out of listThreads() on this scan or an
    // earlier one — that is how they reached the journal and the undo log — so
    // hard rule 1 still holds.
    for (const c of rcands) known.add(c.id);
    for (const id of [...rsel]) if (!rcands.some((c) => c.id === id)) rsel.delete(id);
    refreshRuns();
    paintRestore();
  }

  function paintRestore() {
    while (rList.firstChild) rList.removeChild(rList.firstChild);
    if (!rcands.length) rList.append(E('div', 'ncs-empty', 'nothing to restore'));

    rcands.forEach((c, i) => {
      const on = rsel.has(c.id);
      const row = E('div', 'ncs-row' + (on ? ' ncs-on' : ''));
      row.append(E('span', 'ncs-check', on ? '✓' : ''));
      const t = E('div', 'ncs-rtitle', c.title);
      t.title = c.title + '\ngone around ' + absTime(c.when);
      row.append(t);
      row.append(E('div', 'ncs-src', c.src));
      // This column is how long ago it went, not when the chat was last used.
      const time = E('div', 'ncs-rtime', relTime(c.when));
      time.title = 'gone around ' + absTime(c.when);
      row.append(time);
      row.onclick = (e) => {
        rangeClick(e.shiftKey, rcands, i, rsel, resAnchor);
        paintRestore();
      };
      rList.append(row);
    });

    rInfo.textContent = 'Chats deleted before this extension was installed can\'t be restored — nothing on this machine records that they existed.';
    bRestore.textContent = 'Restore ' + rsel.size;
    bRestore.disabled = !rsel.size || running;
    bForget.textContent = 'Forget ' + rsel.size;
    bForget.disabled = !rsel.size || running;
    bDownload.disabled = running;
    rAll.disabled = !rcands.length || running;
    rNone.disabled = !rsel.size || running;
    // Say so when entries are hidden — silently shrinking the list would look
    // like data loss, and the entries are still in the downloadable record.
    const aged = rHidden ? ` · ${rHidden} older than ${CONFIG.restoreMaxAgeDays}d hidden` : '';
    rStatus.textContent = rcands.length
      ? `${rcands.length} recoverable · ${rsel.size} selected${aged}`
      : (rHidden ? `nothing in the last ${CONFIG.restoreMaxAgeDays} days${aged}`
                 : 'nothing recoverable yet');
  }

  function refreshRuns() {
    // Only runs that actually deleted something — a restore run has nothing to
    // undo and would just clutter the picker.
    const runs = readRuns().filter((r) => r.items.some((i) => i.status === 'deleted'));
    const keep = runSel.value;
    while (runSel.firstChild) runSel.removeChild(runSel.firstChild);
    if (!runs.length) {
      const o = E('option', null, 'no runs recorded');
      o.value = '';
      runSel.append(o);
      runSel.disabled = true;
      bUndoRun.disabled = true;
      return;
    }
    runSel.disabled = false;
    bUndoRun.disabled = running;
    for (const run of runs) {
      const n = run.items.filter((i) => i.status === 'deleted').length;
      const when = new Date(run.startedAt);
      const o = E('option', null,
        `${when.toLocaleDateString()} ${when.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} — ${n} deleted`);
      o.value = run.runId;
      runSel.append(o);
    }
    if (keep && runs.some((r) => r.runId === keep)) runSel.value = keep;
  }

  // ── control wiring ──
  fIn.oninput = () => { filter = fIn.value.trim().toLowerCase(); touch(); };
  fAll.onclick = () => { visible().forEach((r) => sel.add(r.id)); touch(); };
  fNone.onclick = () => { visible().forEach((r) => sel.delete(r.id)); touch(); };
  bAll.onclick = () => { rows.forEach((r) => sel.add(r.id)); touch(); };
  bNone.onclick = () => { sel.clear(); delAnchor.id = null; touch(); };
  bInvert.onclick = () => {
    rows.forEach((r) => { if (sel.has(r.id)) sel.delete(r.id); else sel.add(r.id); });
    touch();
  };
  sortSel.onchange = () => { sortMode = sortSel.value; sortRows(); touch(); };
  bNewest.onclick = () => {
    // Independent of the display sort — "newest" always means by updated time.
    const n = Math.max(0, parseInt(nIn.value, 10) || 0);
    sel.clear();
    visible().slice().sort((a, b) => (b.updated || 0) - (a.updated || 0))
      .slice(0, n).forEach((r) => sel.add(r.id));
    delAnchor.id = null;
    touch();
  };
  // Toggles the view filter on and off. To SELECT the old chats, turn it on
  // and then hit "+ shown".
  const syncOlder = () => bOlder.classList.toggle('ncs-btn-on', ageDays != null);
  bOlder.onclick = () => {
    ageDays = ageDays == null ? Math.max(0, parseInt(dIn.value, 10) || 0) : null;
    syncOlder();
    touch();
  };
  dIn.oninput = () => {
    if (ageDays == null) return;                 // not filtering yet — nothing to update
    ageDays = Math.max(0, parseInt(dIn.value, 10) || 0);
    touch();
  };
  rescanB.onclick = () => {
    rescan();
    flash(`rescanned — ${rows.length} chat${rows.length === 1 ? '' : 's'}`);
  };
  closeB.onclick = () => closePanel();

  // ── open / close / drag ──
  const isOpen = () => !panel.classList.contains('ncs-hidden');

  function place() {
    const r = launcher.getBoundingClientRect();
    const left = Math.max(8, Math.min(window.innerWidth - 348, r.right - 340));
    panel.style.left = left + 'px';
    panel.style.top = (r.bottom + 8) + 'px';
    panel.style.right = 'auto';
  }

  function openPanel() {
    if (isOpen()) return;
    panel.classList.remove('ncs-hidden');
    // If the broom is hidden there's no launcher to anchor to, so park it
    // top-right rather than wherever the invisible launcher happens to sit.
    if (CONFIG.broomVisible) place();
    else { panel.style.left = 'auto'; panel.style.right = '16px'; panel.style.top = '56px'; }
    rescan();
    emitState();
  }
  function closePanel() {
    panel.classList.add('ncs-hidden');
    emitState();
  }
  function togglePanel() { isOpen() ? closePanel() : openPanel(); }

  function applyBroom() {
    launcher.classList.toggle('ncs-hidden', !CONFIG.broomVisible);
  }

  let drag = null;
  launcher.onmousedown = (e) => {
    drag = { x: e.clientX, y: e.clientY, moved: false, r: launcher.getBoundingClientRect() };
    launcher.classList.add('ncs-dragging');
    e.preventDefault();
  };
  window.addEventListener('mousemove', (e) => {
    if (!drag) return;
    if (Math.abs(e.clientX - drag.x) > 3 || Math.abs(e.clientY - drag.y) > 3) drag.moved = true;
    launcher.style.left = (drag.r.left + e.clientX - drag.x) + 'px';
    launcher.style.top = (drag.r.top + e.clientY - drag.y) + 'px';
    launcher.style.right = 'auto';
    launcher.style.bottom = 'auto';
    if (isOpen()) place();
  });
  window.addEventListener('mouseup', () => {
    if (!drag) return;
    launcher.classList.remove('ncs-dragging');
    if (!drag.moved) togglePanel();
    else writeJSON(K.pos, {
      top: launcher.style.top, left: launcher.style.left, right: 'auto', bottom: 'auto'
    });
    drag = null;
  });

  // ── keyboard: must never swallow a keystroke meant for Notion ──
  function typingInPage() {
    const a = document.activeElement;
    if (!a || a === document.body || a === document.documentElement) return false;
    if (panel.contains(a)) return false;
    const tag = a.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || a.isContentEditable;
  }

  document.addEventListener('mousedown', (e) => {
    panelTouched = panel.contains(e.target) || launcher.contains(e.target);
  }, true);

  window.addEventListener('keydown', (e) => {
    if (!isOpen() || typingInPage()) return;
    const inFilter = document.activeElement === fIn;

    if (e.key === 'Escape') {
      closePanel();
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    if (e.key === '/' && !inFilter) {
      fIn.focus();
      fIn.select();
      e.preventDefault();
      return;
    }
    if ((e.metaKey || e.ctrlKey) && (e.key === 'a' || e.key === 'A') && panelTouched && !inFilter) {
      visible().forEach((r) => sel.add(r.id));
      touch();
      e.preventDefault();
      return;
    }
  }, true);

  /* ══ §8  Run loop ══════════════════════════════════════════════════════
   * Serialised chunks. A single failure never aborts a run: retry the chunk
   * with backoff, then retry its items individually so one bad ID doesn't sink
   * nine good ones, then mark and carry on. */
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  async function sendChunk(ids, alive, ctx) {
    for (let attempt = 0; attempt <= CONFIG.retryBackoffMs.length; attempt++) {
      const res = await threadOp(ids, alive, ctx);
      if (res.ok) return res;
      const retryable = res.status === 429 || res.status === 'ERR' ||
        (typeof res.status === 'number' && res.status >= 500);
      if (!retryable || attempt === CONFIG.retryBackoffMs.length) return res;
      log('chunk', res.status, '— backing off', CONFIG.retryBackoffMs[attempt] + 'ms');
      await sleep(CONFIG.retryBackoffMs[attempt]);
    }
  }

  function titleList(targets) {
    const shown = targets.slice(0, 8).map((t) => '  • ' + t.title).join('\n');
    const rest = targets.length - 8;
    return shown + (rest > 0 ? `\n  …and ${rest} more` : '');
  }

  async function runOp(targets, alive) {
    if (running) return;
    const verb = alive ? 'Restore' : 'Delete';

    // Hard rule 1: nothing that didn't come out of listThreads() gets touched.
    const foreign = targets.filter((t) => !known.has(t.id));
    if (foreign.length) {
      alert(`Refusing to ${verb.toLowerCase()}: ${foreign.length} target(s) did not come from the thread list.`);
      log('refused — targets not from listThreads');
      return;
    }
    if (!targets.length) return;

    if (targets.length > CONFIG.maxPerRun) {
      alert(`${targets.length} selected, but the hard cap is ${CONFIG.maxPerRun} per run.\n\nNothing was ${alive ? 'restored' : 'deleted'}. Select fewer and try again.`);
      log('refused — over maxPerRun', CONFIG.maxPerRun);
      return;
    }

    const tail = alive ? '' : '\n\nUndo last will bring them back.';
    if (!confirm(`${verb} ${targets.length} chat${targets.length === 1 ? '' : 's'}?\n\n${titleList(targets)}${tail}`)) return;
    if (targets.length > CONFIG.confirmThreshold &&
        !confirm(`That's ${targets.length} chats — over the ${CONFIG.confirmThreshold} threshold.\n\nAre you sure?`)) return;

    if (CONFIG.dryRun) {
      log('DRY RUN', verb.toLowerCase(), targets.length, 'ids:', targets.slice(0, 5).map((t) => t.id).join(','));
      status.textContent = `dry run — would ${verb.toLowerCase()} ${targets.length}, sent 0 requests`;
      alert(`DRY RUN\n\nWould ${verb.toLowerCase()} ${targets.length} chat(s). Zero requests were sent.\n\nDetails are in document.documentElement.dataset.ncsLog`);
      return;
    }

    // Hard rule 4: the undo log is written before anything is attempted. If this
    // throws, the run does not start.
    let run;
    try {
      run = startRun(targets);
    } catch (e) {
      alert(`Could not write the undo log, so nothing was ${alive ? 'restored' : 'deleted'}.\n\n${e.message}`);
      log('ABORT — undo log write failed:', e.message);
      return;
    }

    running = true;
    stopRequested = false;
    lastFailed = [];
    bStop.classList.remove('ncs-hidden');
    bDel.classList.add('ncs-hidden');
    touch();                               // drop the previous run's message

    const ctx = buildCtx();
    let done = 0;
    const failed = [];

    for (let i = 0; i < targets.length; i += CONFIG.chunkSize) {
      if (stopRequested) break;
      const chunk = targets.slice(i, i + CONFIG.chunkSize);
      statusMsg = `${alive ? 'restoring' : 'deleting'} ${Math.min(i + chunk.length, targets.length)} of ${targets.length}…`;
      status.textContent = statusMsg;      // set directly: no full re-render mid-run

      const res = await sendChunk(chunk.map((t) => t.id), alive, ctx);
      if (res.ok) {
        done += chunk.length;
        chunk.forEach((t) => succeeded(run, t.id, alive));
      } else {
        log('chunk failed', res.status, '— retrying items individually');
        for (const t of chunk) {
          if (stopRequested) break;
          const one = await threadOp([t.id], alive, ctx);
          if (one.ok) { done++; succeeded(run, t.id, alive); }
          else { failed.push(t); mark(run, t.id, 'failed'); log('failed', t.id, one.status); }
        }
      }
      persistRun(run);
    }

    running = false;
    lastFailed = failed;
    bStop.classList.add('ncs-hidden');
    bDel.classList.remove('ncs-hidden');
    if (!failed.length) sel.clear();
    else { sel.clear(); failed.forEach((t) => sel.add(t.id)); }
    rescan();
    say(`done — ${done} ${alive ? 'restored' : 'deleted'}` +
      (failed.length ? `, ${failed.length} failed` : '') +
      (stopRequested ? ' (stopped)' : ''));
    reconcile();
    log('run done:', done, alive ? 'restored' : 'deleted', failed.length, 'failed');
    emitState({ done, failed: failed.length, alive, at: Date.now() });
  }

  function mark(run, id, statusValue) {
    const item = run.items.find((x) => x.id === id);
    if (item) item.status = statusValue;
  }

  function succeeded(run, id, alive) {
    mark(run, id, alive ? 'restored' : 'deleted');
    // Ground truth until the cache catches up; expires via CONFIRM_TTL_MS.
    confirmedAlive.set(id, { alive, at: Date.now() });
  }

  // The cache settles asynchronously, so re-read it a couple of times after a
  // run to drain `confirmedAlive` and let the sidebar cross-check re-settle.
  function reconcile() {
    clearTimeout(reconcile.a);
    clearTimeout(reconcile.b);
    reconcile.a = setTimeout(() => { if (!running) rescan(); }, 900);
    reconcile.b = setTimeout(() => { if (!running) rescan(); }, 2600);
  }

  bDel.onclick = () => runOp(rows.filter((r) => sel.has(r.id)), false);
  bStop.onclick = () => { stopRequested = true; status.textContent = 'stopping after this chunk…'; };
  bRetry.onclick = () => { const f = lastFailed.slice(); lastFailed = []; runOp(f, false); };

  bUndo.onclick = async () => {
    const last = readRuns()[0];
    if (!last) return alert('No run recorded yet.');
    const items = last.items.filter((i) => i.status === 'deleted');
    if (!items.length) return alert('Nothing to restore in the last run.');
    if (CONFIG.dryRun) {
      log('DRY RUN undo', items.length);
      return alert(`DRY RUN\n\nWould restore ${items.length} chat(s). Zero requests were sent.`);
    }
    // Undo targets come from the undo log, not the live list, so the hard-rule
    // gate has to be widened to include them for this call.
    items.forEach((i) => known.add(i.id));
    await runOp(items.map((i) => ({ id: i.id, title: i.title })), true);
  };

  // ── Restore tab wiring ──
  function showTab(which) {
    const del = which === 'delete';
    tabDel.classList.toggle('ncs-tab-on', del);
    tabRes.classList.toggle('ncs-tab-on', !del);
    deleteView.classList.toggle('ncs-hidden', !del);
    restoreView.classList.toggle('ncs-hidden', del);
  }
  tabDel.onclick = () => showTab('delete');
  tabRes.onclick = () => { showTab('restore'); rescan(); };

  bRestore.onclick = () => runOp(
    rcands.filter((c) => rsel.has(c.id)).map((c) => ({ id: c.id, title: c.title })), true);

  rAll.onclick = () => { rcands.forEach((c) => rsel.add(c.id)); paintRestore(); };
  rNone.onclick = () => { rsel.clear(); resAnchor.id = null; paintRestore(); };

  bForget.onclick = () => {
    const targets = rcands.filter((c) => rsel.has(c.id));
    if (!targets.length) return;
    // Deliberately blunt. This is the one action in the extension with no way
    // back — everything else is a flag flip Notion can undo.
    if (!confirm(
      `Forget ${targets.length} chat${targets.length === 1 ? '' : 's'}?\n\n` +
      `${titleList(targets)}\n\n` +
      'This deletes this extension\'s record of them. They stay deleted in Notion, ' +
      'and you will never be able to restore them from here again.\n\n' +
      'This cannot be undone.')) return;
    forget(targets.map((c) => c.id));
    rsel.clear();
    resAnchor.id = null;
    rescan();
    // The restore tab has its own footer, so this can't go through say().
    rStatus.textContent = `forgotten — ${targets.length} no longer restorable`;
    clearTimeout(bForget.timer);
    bForget.timer = setTimeout(paintRestore, 4000);
  };

  bUndoRun.onclick = () => {
    const run = readRuns().find((r) => r.runId === runSel.value);
    if (!run) return alert('Pick a run first.');
    const items = run.items.filter((i) => i.status === 'deleted');
    if (!items.length) return alert('That run has nothing left to restore.');
    items.forEach((i) => known.add(i.id));
    runOp(items.map((i) => ({ id: i.id, title: i.title })), true);
  };

  // Convenience, not the safety net — Restore is the safety net.
  bDownload.onclick = () => {
    const payload = { exportedAt: new Date().toISOString(),
      runs: readRuns(), journal: readJSON(K.journal, {}) };
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `notion-chat-sweeper-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    log('record downloaded');
  };

  /* ══ §9  Bridge listener ═══════════════════════════════════════════════ */
  function emitState(lastRun) {
    try {
      const detail = {
        installed: true,
        broomVisible: CONFIG.broomVisible,
        panelOpen: isOpen(),
        chats: rows.length,
        dryRun: CONFIG.dryRun,
        at: Date.now()
      };
      if (lastRun) { detail.lastRun = lastRun; emitState.last = lastRun; }
      else if (emitState.last) detail.lastRun = emitState.last;
      window.dispatchEvent(new CustomEvent('ncs:state', { detail }));
    } catch (e) { /* ignore */ }
  }

  window.addEventListener('ncs:cmd', (e) => {
    const msg = e.detail || {};
    if (msg.cmd === 'togglePanel') togglePanel();
    else if (msg.cmd === 'openPanel') openPanel();
    else if (msg.cmd === 'setBroom') {
      CONFIG.broomVisible = !!msg.visible;
      saveCfg();
      applyBroom();
      log('broom', CONFIG.broomVisible ? 'shown' : 'hidden');
      emitState();
    } else if (msg.cmd === 'getState') emitState();
  });

  /* ══ §10  Debug surface ════════════════════════════════════════════════ */
  window.__ncs = {
    CONFIG,
    log: () => logBuf.slice(),
    listThreads,
    domThreadIds,
    findCache,
    buildCtx,
    learned,
    rows: () => rows.slice(),
    runs: readRuns,
    journal: () => readJSON(K.journal, {}),
    open: openPanel,
    close: closePanel,
    rescan,
    forget: () => { cachedCtx = null; return 'cache handle dropped — next rescan re-probes'; }
  };

  /* ══ §11  Boot ═════════════════════════════════════════════════════════ */
  installStyles();
  wrapFetch();
  document.body.append(launcher, panel);
  applyBroom();
  syncMode();

  // Notion is an SPA; if a route change ever detaches our nodes, put them back.
  setInterval(() => {
    if (!launcher.isConnected || !panel.isConnected) {
      document.body.append(launcher, panel);
      log('re-attached after DOM detach');
    }
  }, 2000);

  /* Light poll so a chat deleted by hand in Notion — or a new one appearing —
     shows up without pressing ↻. Only reads the record cache (~45 records, a
     fraction of a millisecond) and compares a fingerprint; the expensive part,
     the sidebar DOM walk, only runs when something actually changed. Idle when
     the panel is closed or a run is in flight. */
  setInterval(() => {
    if (!isOpen() || running) return;
    const all = listThreads();
    if (!all || rawSignature(all) === lastSig) return;
    log('poll: chat list changed');
    rescan();
  }, 4000);

  log('installed', CONFIG.dryRun ? '(DRY RUN)' : '(live)', 'v' + BUILD);
  emitState();
})();
