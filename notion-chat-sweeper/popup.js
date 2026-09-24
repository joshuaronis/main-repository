/* Notion Chat Sweeper — popup.js
 *
 * Talks to the page through bridge.js. Reads state out of chrome.storage.local,
 * which bridge.js keeps up to date from the panel's own ncs:state events.
 */

const NOTION = /^https:\/\/(app\.notion\.com|www\.notion\.so)\//;

const subEl = document.getElementById('sub');
const openB = document.getElementById('open');
const broomB = document.getElementById('broom');
const runEl = document.getElementById('run');

let tabId = null;
let broomVisible = true;

async function activeNotionTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  // host_permissions covers app.notion.com / www.notion.so, so tab.url is
  // readable for exactly the tabs we care about without the "tabs" permission.
  return tab && NOTION.test(tab.url || '') ? tab : null;
}

function send(msg) {
  if (tabId == null) return Promise.resolve(null);
  return chrome.tabs.sendMessage(tabId, Object.assign({ ncs: true }, msg)).catch(() => null);
}

function ago(ms) {
  const s = Math.round((Date.now() - ms) / 1000);
  if (s < 60) return 'just now';
  if (s < 3600) return Math.floor(s / 60) + 'm ago';
  if (s < 86400) return Math.floor(s / 3600) + 'h ago';
  return Math.floor(s / 86400) + 'd ago';
}

function paint(state) {
  if (!state) return;
  broomVisible = state.broomVisible !== false;
  broomB.textContent = broomVisible ? 'Hide broom' : 'Show broom';
  const bits = [];
  if (typeof state.chats === 'number') bits.push(state.chats + ' chats');
  if (state.panelOpen) bits.push('panel open');
  if (state.dryRun) bits.push('DRY RUN');
  if (bits.length) subEl.textContent = bits.join(' · ');

  if (state.lastRun) {
    const r = state.lastRun;
    runEl.textContent = `Last run: ${r.done} ${r.alive ? 'restored' : 'deleted'}` +
      (r.failed ? `, ${r.failed} failed` : '') + ` — ${ago(r.at)}`;
  }
}

async function init() {
  const tab = await activeNotionTab();
  if (!tab) {
    subEl.textContent = 'Open a Notion tab to use this.';
    openB.disabled = true;
    broomB.disabled = true;
    return;
  }
  tabId = tab.id;

  const stored = await chrome.storage.local.get('ncsState');
  if (stored.ncsState) paint(stored.ncsState);
  else subEl.textContent = 'ready';

  // Confirm the panel is actually live in this tab. If the extension was
  // reloaded but the tab wasn't, there is no receiver and this comes back null.
  const pong = await send({ cmd: 'getState' });
  if (!pong) {
    subEl.textContent = 'Reload the Notion tab (⌘R) to finish loading.';
    openB.disabled = true;
    broomB.disabled = true;
    return;
  }
  setTimeout(async () => {
    const fresh = await chrome.storage.local.get('ncsState');
    paint(fresh.ncsState);
  }, 60);
}

openB.onclick = async () => { await send({ cmd: 'openPanel' }); window.close(); };

broomB.onclick = async () => {
  broomVisible = !broomVisible;
  broomB.textContent = broomVisible ? 'Hide broom' : 'Show broom';
  await send({ cmd: 'setBroom', visible: broomVisible });
};

init();
