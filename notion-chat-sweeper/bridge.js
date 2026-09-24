/* Notion Chat Sweeper — bridge.js  (ISOLATED world)
 *
 * The panel has to run in the MAIN world to see React's __reactFiber$ expandos,
 * but MAIN-world scripts get no chrome.* APIs. This file is the only piece that
 * can see both sides, so it does nothing except relay:
 *
 *   popup/background --chrome.runtime--> here --CustomEvent--> content.js
 *   content.js --CustomEvent--> here --chrome.storage--> popup
 */

chrome.runtime.onMessage.addListener((msg, _sender, respond) => {
  if (msg && msg.ncs) {
    window.dispatchEvent(new CustomEvent('ncs:cmd', { detail: msg }));
    respond({ ok: true });
  }
  return true;
});

// content.js mirrors its state out here so the popup has something to read
// without needing to talk to the page at all.
window.addEventListener('ncs:state', (e) => {
  try {
    chrome.storage.local.set({ ncsState: e.detail });
  } catch (err) {
    /* extension context invalidated after a reload — harmless, tab reload fixes it */
  }
});
