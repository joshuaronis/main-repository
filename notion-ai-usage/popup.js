/* Notion AI Usage — popup.js
 *
 * A fallback for the shortcut and, more importantly, the place where a
 * failure gets explained. background.js can't show UI, so it parks the last
 * error in chrome.storage and this reads it back.
 */

const NOTION_RE = /^https:\/\/(app\.notion\.com|www\.notion\.so)\//;

const $ = (id) => document.getElementById(id);

function say(message, kind) {
  const el = $('status');
  el.textContent = message || '';
  if (kind) el.setAttribute('data-kind', kind);
  else el.removeAttribute('data-kind');
}

/* Show the shortcut that is actually bound, not the one we asked for —
   Chrome silently drops a suggested key when something else already owns it,
   and a popup insisting on ⌘⇧U when nothing is bound is worse than useless. */
async function showShortcut() {
  try {
    const cmds = await chrome.commands.getAll();
    const cmd = cmds.find((c) => c.name === 'open-ai-usage');
    if (cmd && cmd.shortcut) {
      $('kbd').textContent = cmd.shortcut;
    } else {
      $('kbd').textContent = 'not set';
      say('No keyboard shortcut is bound. Set one at chrome://extensions/shortcuts.', 'error');
    }
  } catch (e) { /* leave the default label */ }
}

async function showContext() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const onNotion = tab && NOTION_RE.test(tab.url || '');
  $('sub').textContent = onNotion
    ? 'On Notion — ready.'
    : 'Not on Notion — will switch to a Notion tab.';
}

async function showLastError() {
  const { nauLastError } = await chrome.storage.local.get('nauLastError');
  // Only surface something recent; a week-old failure is just noise.
  if (nauLastError && Date.now() - nauLastError.at < 10 * 60 * 1000) {
    say('Last run: ' + nauLastError.message, 'error');
  }
}

$('open').addEventListener('click', async () => {
  const btn = $('open');
  btn.disabled = true;
  say('Opening…');
  try {
    const res = await chrome.runtime.sendMessage({ nauPopup: 'openAiUsage' });
    if (res && res.ok === false) say(res.error || 'Could not open the AI usage tab.', 'error');
    else if (res && res.closed) say('Closed.');
    else say('Opened.');
  } catch (e) {
    say('The extension did not respond. Try reloading the Notion tab.', 'error');
  }
  btn.disabled = false;
  // The settings modal is in the page behind this popup; get out of the way.
  setTimeout(() => window.close(), 500);
});

$('shortcuts').addEventListener('click', (e) => {
  e.preventDefault();
  chrome.tabs.create({ url: 'chrome://extensions/shortcuts' });
});

showShortcut();
showContext();
showLastError();
