/* Notion Chat Sweeper — background.js  (MV3 service worker)
 *
 * Sole job: catch the keyboard command and relay it to the active Notion tab,
 * where bridge.js forwards it into the page.
 */

const NOTION = /^https:\/\/(app\.notion\.com|www\.notion\.so)\//;

chrome.commands.onCommand.addListener(async (command) => {
  if (command !== 'toggle-panel') return;
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id || !NOTION.test(tab.url || '')) return;
    await chrome.tabs.sendMessage(tab.id, { ncs: true, cmd: 'togglePanel' });
  } catch (err) {
    // No receiver in that tab (extension reloaded but tab not). Nothing useful
    // to do from here; the popup explains the reload-the-tab step.
  }
});
