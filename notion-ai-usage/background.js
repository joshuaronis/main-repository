/* Notion AI Usage — background.js  (MV3 service worker)
 *
 * Owns the keyboard shortcut and works out which tab to drive. The actual
 * clicking lives in content.js.
 *
 * The shortcut is a Chrome command rather than a page-level keydown listener
 * on purpose: it fires wherever Josh is, and it can never swallow a keystroke
 * that Notion wanted (field guide 5.6).
 */

const NOTION_URLS = ['https://app.notion.com/*', 'https://www.notion.so/*'];
const NOTION_RE = /^https:\/\/(app\.notion\.com|www\.notion\.so)\//;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* Returns the failure so callers can `return setProblem(...)` and still hand
   the popup something it can render. Returning undefined here once made a
   failed run report "Opened." */
async function setProblem(message) {
  try {
    await chrome.storage.local.set({ nauLastError: { message, at: Date.now() } });
    await chrome.action.setBadgeText({ text: '!' });
    await chrome.action.setBadgeBackgroundColor({ color: '#b4483a' });
    setTimeout(() => { chrome.action.setBadgeText({ text: '' }).catch(() => {}); }, 8000);
  } catch (e) { /* nothing useful to do from here */ }
  return { ok: false, error: message };
}

async function clearProblem() {
  try {
    await chrome.storage.local.remove('nauLastError');
    await chrome.action.setBadgeText({ text: '' });
  } catch (e) {}
}

/** Wait until a tab has finished loading. */
async function waitForComplete(tabId, ms = 25000) {
  const deadline = Date.now() + ms;
  while (Date.now() < deadline) {
    try {
      const tab = await chrome.tabs.get(tabId);
      if (tab.status === 'complete') return true;
    } catch (e) { return false; }
    await sleep(300);
  }
  return false;
}

/**
 * Find the tab to drive, in order of least surprise:
 *   1. the tab Josh is looking at, if it is Notion
 *   2. another Notion tab in this window
 *   3. a Notion tab in any window
 *   4. a new tab
 */
async function resolveTab() {
  const [active] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (active && NOTION_RE.test(active.url || '')) return { tab: active, fresh: false };

  let [tab] = await chrome.tabs.query({ url: NOTION_URLS, currentWindow: true });
  if (!tab) [tab] = await chrome.tabs.query({ url: NOTION_URLS });

  if (tab) {
    await chrome.tabs.update(tab.id, { active: true });
    try { await chrome.windows.update(tab.windowId, { focused: true }); } catch (e) {}
    return { tab, fresh: false };
  }

  const created = await chrome.tabs.create({ url: 'https://app.notion.com/' });
  return { tab: created, fresh: true };
}

/**
 * Talk to content.js, retrying while the tab is still booting.
 *
 * A tab that was open when the extension was reloaded holds an orphaned
 * content script and will never answer (field guide 6.2). That case is worth
 * naming explicitly, because "the shortcut stopped working" is almost always
 * this and the fix is just reloading the tab.
 */
async function sendWithRetry(tabId, msg, ms) {
  const deadline = Date.now() + ms;
  let lastErr = null;
  for (;;) {
    try {
      return await chrome.tabs.sendMessage(tabId, msg);
    } catch (e) {
      lastErr = e;
      if (Date.now() >= deadline) throw lastErr;
      await sleep(400);
    }
  }
}

async function openAiUsage() {
  let target;
  try {
    target = await resolveTab();
  } catch (e) {
    return setProblem('Could not find or open a Notion tab.');
  }

  const { tab, fresh } = target;

  if (fresh) await waitForComplete(tab.id);

  // A cold tab needs longer than a warm one: Notion's own boot is slow, and
  // content.js only starts answering at document_idle.
  const budget = fresh ? 30000 : 4000;

  try {
    await sendWithRetry(tab.id, { nau: true, cmd: 'ping' }, budget);
  } catch (e) {
    return setProblem(
      'That Notion tab is not listening. If you just reloaded the extension, ' +
      'reload the Notion tab too — reloading an unpacked extension does not ' +
      'update tabs that were already open.'
    );
  }

  await clearProblem();
  try {
    const res = await chrome.tabs.sendMessage(tab.id, { nau: true, cmd: 'openAiUsage' });
    if (res && res.ok === false) await setProblem(res.error || 'Could not open the AI usage tab.');
    return res;
  } catch (e) {
    return setProblem('Lost contact with the Notion tab mid-run.');
  }
}

chrome.commands.onCommand.addListener((command) => {
  if (command === 'open-ai-usage') openAiUsage();
});

chrome.runtime.onMessage.addListener((msg, _sender, respond) => {
  if (msg && msg.nauPopup === 'openAiUsage') {
    openAiUsage().then((r) => { try { respond(r || { ok: false }); } catch (e) {} });
    return true;
  }
});
