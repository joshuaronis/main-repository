# Build "Notion Chat Complete Exporter"

You are the senior engineer on this project. You will design, research, implement, test, and package a Chrome Manifest V3 extension named **Notion Chat Complete Exporter**. It lets Josh point at a Notion AI chat and export **the entire conversation**: every user and assistant message, in order, each with everything nested inside it. That includes collapsed reasoning, steps, tool calls and their results, file previews, terminal commands and output, and every tab panel. Josh does not want only the text visible at a glance.

Work through to a finished, tested, packaged extension. Do not stop at a plan, an architecture proposal, snippets, or setup instructions, and do not pause to present a plan for approval. Keep your plan and intermediate analysis in your own working process.

---

## 1. Your environment and how to work in it

You are running on Josh's own computer, with:

- **Chrome control.** A browser-control connector attached to Josh's everyday Chrome, which is signed in to Notion. Use it to open Notion chats, read the page structure, run JavaScript in the page, click non-destructive controls, and test the extension on the real interface.
- **A local terminal.** Use it for files, package managers, builds, test runners, and headless browsers.
- **Web access.** Use it for research (Section 3).
- **Reference material Josh has given you:**
  - a folder containing `NOTION-EXTENSION-FIELD-GUIDE.md` and three of his earlier extensions: `notion-ai-usage/`, `notion-chat-sweeper/`, and `notion-minimal-comments/`, which has a `ground-truth/` folder of live captures;
  - screenshots of the chat structures described in Section 7.

Create the new project as a sibling folder named `notion-chat-complete-exporter/`, next to the reference folder. Treat the reference folder as read-only: never modify, reformat, or rebuild anything in it.

### Josh's time

Josh wants this to run on its own until it is finished. He is not a DevTools person and should never be asked to find a selector, inspect a request, or interpret console output. You have the tools to do all of that yourself.

There is one step you may genuinely be unable to automate: browser-control tools usually cannot operate `chrome://extensions`, so loading or reloading an unpacked extension may need his hands. Before asking, keep that need to a minimum:

- **Prototype in the page first.** JavaScript run through Chrome control normally executes in the page's own JavaScript world, the same one a MAIN-world content script uses (field guide Part 10 relies on this for console prototyping). Confirm that once. Build your extraction code as a bundle that can also be injected directly into the page, with a thin shim standing in for `chrome.*`. That way you can run the complete picker, traversal, and extraction on real chats without the extension being loaded. Iterate this way until extraction is correct.
- **Then ask once, click by click.** When you need the real extension loaded, give Josh exact steps: open `chrome://extensions`, turn on **Developer mode** (top right), click **Load unpacked**, choose the `dist` folder at its full path, then reload the Notion tab with ⌘R. For a later rebuild, tell him to click the extension's reload arrow and then reload the Notion tab. The field guide (Part 6.2) explains why both steps are needed. Group these requests so each one covers a whole round of testing.

Nothing else is a reason to stop and ask. If one inspection or automation method fails, try another.

### Access and permission

You have Josh's permission to use every connector and development tool available, including:

- Chrome control, and JavaScript executed in the Notion page for inspecting document structure, attributes, event behaviour, accessibility labels, and rendered content;
- Playwright, Puppeteer, or headless Chromium for fixture tests. These run against local fixture files, never against Josh's signed-in profile;
- local terminal commands, scripts, test runners, package managers, build tools, and file inspection;
- clicking non-destructive disclosure controls, tabs, "show more" controls, and similar interface elements to reveal content for inspection and testing;
- scrolling chats to load earlier or later messages.

You may inspect any of Josh's existing Notion AI chats and operate their reveal controls. You must not:

- type into the chat composer, send a message, regenerate, retry, or rate a response. Watch keyboard events in particular: never dispatch Enter or text input while focus could be in the composer;
- edit, rename, move, pin, or delete any page or chat;
- trigger any action unrelated to revealing and reading chat content;
- collect cookies, authentication tokens, credentials, or unrelated page data;
- call Notion's private backend endpoints (`/api/v3/…`) to obtain content;
- copy real chat text into the repository. Test fixtures must be synthetic: reproduce the structure you observed and fill it with invented text.

---

## 2. Read before you build

Read in this order, fully, before writing production code.

1. **`NOTION-EXTENSION-FIELD-GUIDE.md`, all of it.** It is written for an AI assistant starting a new Notion extension. It was verified live against Josh's account across three projects, and it records traps that each cost hours. Run its **Part 0 verification snippet** through Chrome control first; that snippet tells you which parts still hold on the current Notion build. Parts that matter directly here:
   - **Part 1**, environment: the origins `https://app.notion.com` and `https://www.notion.so` (both need matching), and the AI chat URL shape `/chat?t=<32hex>`. Trusted Types is enforced, so never assign HTML strings to page sinks. Content lives in the top frame.
   - **Part 2**, choosing ISOLATED versus MAIN world, and the bridge pattern for relaying between them.
   - **Part 3**, Notion's in-page record cache. AI chats are `thread` records, and each carries an ordered `messages` array of IDs (3.5). Fields are lazy (3.4).
   - **Part 5**, the DOM: stable anchors (5.1), and the rule that locators must never depend on screen position. Overlays, parked popups, and why `aria-expanded` is more trustworthy than rectangles (5.2). Synthetic clicks (5.3). **DOM ready is not React ready (5.4)**, so a click that arrives too early is silently swallowed, and a naive retry on a toggle undoes the previous attempt. Viewport width changes rendering (5.5). Coexisting with Notion's own shortcuts: `/` and `Esc` belong to Notion (5.6).
   - **Part 6**, lifecycle: single-page navigation, double injection, and scripts orphaned when the extension reloads.
   - **Part 7**, debugging: content-script logs are invisible from outside, tick-counted waits shrink in background tabs (use deadlines), and `copy()` is unavailable inside async callbacks.
   - **Part 12**, the trap index. Check your design against every row.
2. **The three extensions' source**, READMEs and `MAINTENANCE-LOG.md` files. Look for tested approaches to manifest configuration, content-script injection, popup ↔ service worker ↔ content-script messaging, recognising Notion surfaces, surviving Notion's re-renders, overlays, and packaging. `notion-chat-sweeper` already works with AI chat threads. Reuse code only where its behaviour fits, and keep any required attribution comments.
3. **`notion-minimal-comments/ground-truth/`**, as an example of how live captures were recorded. Keep your own development notes in the same spirit (Section 11).

The guide's facts are dated. Where the live page disagrees with it, the live page wins. Record the disagreement in your development notes.

---

## 3. Research existing work

Before designing the traversal and serialisation, search GitHub and the web for:

- existing Notion AI chat exporters, if any exist;
- mature exporters for other AI chat interfaces (ChatGPT, Claude, Gemini, Perplexity) and how they handle long or virtualised conversations, collapsed reasoning, code blocks, tool output, and Markdown fence safety;
- DOM-to-Markdown libraries and their handling of tables, nested lists, and inline code containing backticks;
- open-source HTML sanitisers suitable for an extension. Weigh their size against writing a small allow-list sanitiser.

Read the relevant source, not just the READMEs. Take techniques, not assumptions: Notion's structure must still be confirmed live. Respect licences, and record in the README anything you reuse and its licence.

---

## 4. What the extension does

### Primary workflow

1. Josh opens a Notion AI chat and clicks the extension icon.
2. He clicks **Export this chat**. If more than one chat is present on the page, for example a full-page chat and the AI side panel, he clicks **Pick a chat** instead, which enters selection mode.
3. In selection mode, the chat under the pointer is outlined, and he clicks the one he wants.
4. The extension walks the whole conversation from its first message to its last. It reveals and extracts every part of every message, and restores the interface.
5. A preview shows the result and lets him copy or download it.

### Selection mode

While selection mode is active:

- draw a visible outline around the exact region that will be exported, labelled with what it is (for example "Chat: <title>, N messages loaded");
- update the outline as the pointer moves;
- cancel on Escape, without letting Notion also act on that Escape (field guide 5.6);
- stop the selecting click from activating any link or button underneath;
- change nothing in the chat.

### Single-message export (secondary)

The same machinery can export one message, so offer it as a secondary mode: **Pick a message**. It highlights and labels the logical message under the pointer as a user message, an assistant message, or an unknown candidate. It offers **wider** and **narrower** controls for when nested containers make the boundary ambiguous, and it exports that one message in the same formats. A right-click context-menu item, **Export this message**, may also be added if it can be made reliable. The whole-chat workflow is the one that must work.

### What a "logical message" is

A chat export is an ordered list of logical messages. A logical message is one complete user message or one complete assistant message. An assistant message's boundary includes every reasoning section, step, tool call, tool result, command, output, file preview, error, citation, attachment, and the final answer nested beneath that response, and it never absorbs the message before or after it. Getting this boundary right matters even in whole-chat mode, because every block in the export must be attributed to the correct message.

---

## 5. Content that must be extracted

For **every** message in the chat, extract the exact text and meaningful structure of everything it contains. At minimum:

- the user's input text;
- the assistant's final output text;
- "Thought", "Thinking", "Reasoning", and "Activity" content, whether visible or initially collapsed;
- parent disclosures such as "2 steps" or "3 steps" that hold several reasoning or tool events;
- every step title;
- tool-call names;
- tool providers and tool types, such as "Computer Alpha / File" or "Computer Alpha / Terminal";
- tool-call arguments where the interface displays them;
- tool-call status, progress, success, failure, warning, and retry labels;
- tool results;
- file-operation cards, filenames, and file contents or code previews;
- terminal cards, the complete command text, and the complete terminal output;
- errors, warnings, and diagnostic text;
- headings, paragraphs, lists, quotations, tables, code blocks, inline code, and mathematical text;
- links, with both their labels and destinations;
- citations and cited-page labels;
- page, database, person, agent, and other Notion mentions;
- attached-file names and whatever attachment metadata the interface exposes;
- image alternative text, captions, accessible labels, and source URLs where exposed;
- timestamps, role labels, model labels, and other message metadata where present;
- controls or status labels whose text carries information about what happened;
- anything inside a message that matches none of the above, preserved as an **unknown** block rather than dropped.

For the chat as a whole, also capture the chat title, the page URL, the surface it was exported from (full page or side panel), and any chat-level metadata the interface shows.

**Preserve source order** within each message and across the chat. If a message shows a thought, then a tool call, then another thought, then the final answer, the export has them in that order.

**Do not summarise, rewrite, normalise, or clean up** extracted text. The export is evidence of what the interface displayed. Preserve punctuation, line breaks, code indentation, shell commands, terminal output, and error messages as closely as the browser provides them.

The extension exports what Josh can reveal through ordinary interface controls. That boundary does not permit omitting reasoning: a Thought or Reasoning section reachable through a normal disclosure is part of the message and must be exported.

---

## 6. Revealing everything in a whole chat

### The conversation itself

A long chat is probably not fully present in the document at once. Notion may load earlier messages only when the user scrolls up, and it may unmount messages that are off screen. Find out which of these happens, live, on a chat long enough to need scrolling. Then:

- identify the chat's scroll container through the adapter (Section 8);
- record its initial scroll position;
- walk the conversation from its first message to its last, loading earlier messages as needed, and process each message once. Key messages by stable identifiers where the DOM exposes them, and otherwise by structural and textual signatures, so that a message rendered twice is not exported twice;
- restore the initial scroll position afterwards.

**Completeness check.** Notion's in-page record cache holds the chat's `thread` record, whose `messages` array lists the conversation's message IDs in order (field guide 3.5). Reading it requires the MAIN world (Part 2). Use it for exactly two things: to know how many messages to expect, and to detect messages the walk missed. Do not use it as a source of content; the export's content comes from the rendered interface. The array may include entries that the interface never renders as a message, such as tool or system records, so establish the mapping live rather than assuming one ID equals one visible message. When the count of messages exported and the count expected disagree in a way the mapping does not explain, show both numbers as a warning in the preview and in the diagnostics. Never present a silently incomplete export (field guide Part 11, rule 8).

**Chat surfaces.** Find every place Josh's Notion renders an AI chat: the full-page chat at `/chat?t=…`, the AI side panel, and any other surface you discover. Support each one you find, or report clearly that a surface is unsupported.

### Disclosures inside each message

Some messages show a disclosure labelled "Thought" whose reasoning text appears only after its arrow is clicked. Some first show a parent such as "2 steps", with separate nested Thought or tool-call disclosures inside it. The extension must reveal these automatically before extracting:

- record which disclosure controls were initially open and which were closed;
- search only inside the message being processed;
- recognise real disclosure controls by semantic evidence: `aria-expanded`, `aria-controls`, `details`/`summary`, accessibility roles, and behaviour confirmed during live inspection;
- open collapsed parents before searching for nested disclosures;
- open nested Thought, Thinking, Reasoning, Activity, step, tool, file, terminal, and "show more" disclosures;
- wait for the newly revealed content to render;
- re-inspect the expanded subtree, because opening one control may create more;
- repeat until no new relevant disclosure appears, or until a bounded limit on time and iterations is reached;
- never click links, submit buttons, retry buttons, destructive buttons, feedback controls, or unrelated page controls;
- confirm each click took effect by reading the control's state, not by scraping display text. Retry a click that did not register without toggling it back (field guide 5.4);
- record a diagnostic for any relevant disclosure that could not be opened;
- restore every disclosure to its original state after extraction, unless Josh turns restoration off in the extension's settings.

Use a `MutationObserver` or an equivalent stability check rather than fixed sleeps alone, and enforce every wait with a wall-clock deadline.

Across a whole chat, find out live whether Notion remembers a disclosure's state when a message is unmounted and remounted during scrolling. Choose the processing order accordingly. One option is to reveal, extract, and restore each message before moving on. Whatever you choose, the interface must end in its original state and the export must say whether it did.

### Tabs and alternate panels

Some tool cards have tabs, such as "Command" and "Output". Only one panel is visible at a time, but all of them belong to the message. For every tab list inside a message:

- record the initially selected tab;
- activate each tab in turn and wait for its panel to render;
- extract and label each panel's content;
- avoid duplicating content that several tabs share;
- restore the originally selected tab.

Apply the same process to file-preview modes, details panels, and any other mutually exclusive views that live inspection shows contain distinct content. A terminal export is incomplete if it has the command without the output, or the output without the command.

### Long, clipped, and dynamic content

Do not assume the text visible in the viewport is all of an element's text. Account for:

- CSS overflow that clips text visually while the full text remains in the document;
- "show more" controls;
- internally scrollable code and output panels;
- content rendered only after a panel opens;
- virtualised regions, which remove off-screen rows and recreate them on scroll;
- open shadow roots;
- same-origin frames.

Prefer reading the document structure when the full content is already there. Where a region is truly virtualised, walk it, collect the rendered fragments in order, deduplicate them with stable structural and textual signatures, and restore the region's scroll position afterwards.

Where a closed shadow root, cross-origin frame, canvas-only surface, or other browser boundary makes text unreachable, record that region in the diagnostics. Never report an extraction as complete when a known region could not be read.

---

## 7. Structures the extractor must handle

The live page is the source of truth, but the extractor must handle the structures shown in Josh's screenshots:

- **Collapsed reasoning.** A parent labelled "2 steps" contains a nested disclosure labelled "Thought". Several paragraphs of reasoning appear only once it is opened, and the final assistant answer sits below the steps.
- **File tool call.** A step titled "Wrote audit_isolation.py" contains a card labelled "Computer Alpha / File", a filename chip reading `audit_isolation.py`, a long Python code preview, and a control at the bottom that reveals or scrolls to more content.
- **Terminal tool call.** A step titled "Recheck run pages and prompts" contains a card labelled "Computer Alpha / Terminal" with separate "Command" and "Output" tabs and a shell command. Another Thought section follows the terminal operation, and the assistant's ordinary response comes after the steps.

An export of a chat containing any of these must include every listed element and the complete text of every relevant disclosure and tab.

---

## 8. Finding things: the Notion adapter

Inspect the live page before settling any selector. Notion's generated class names change between releases (field guide 5.1), so prefer, in this order:

1. stable data attributes confirmed by inspection;
2. accessibility roles, labels, names, and expanded-state attributes;
3. semantic elements and relationships;
4. repeated structural patterns;
5. visible labels combined with verified ancestor relationships;
6. generated class names, only as a last resort.

Put all of this in **one Notion adapter module**: locating chat surfaces, the scroll container, message boundaries, roles, disclosures, tab lists, tool cards, and the thread-record lookup. Nothing outside the adapter should contain a Notion selector. Give the adapter several strategies per lookup, in priority order, and have it report which strategy succeeded. When Notion changes its interface, the repair should then touch the adapter alone.

For message boundaries, score candidate ancestors rather than taking the first large container. Evidence includes:

- a role or message label;
- the presence of exactly one response body;
- ownership of nested step and tool-call cards;
- separation from adjacent messages;
- repeated sibling structure shared with other turns;
- accessibility relationships;
- being the smallest ancestor that contains the full message but not the next one.

If boundary confidence is low in whole-chat mode, still export, and flag the affected messages in the diagnostics. In single-message mode, show the proposed boundary with wider and narrower controls. In either mode, never silently export the entire page as one message.

---

## 9. Export formats

Provide four representations of each export:

- **Markdown**;
- **plain text**;
- **structured JSON**;
- **sanitised HTML** of the extracted subtree, after every relevant state has been visited.

The preview has one tab per format and buttons for **Copy Markdown**, **Copy plain text**, **Copy JSON**, **Download** for each format, **Download all as ZIP** (if a small ZIP writer suffices; otherwise four separate downloads are acceptable), **Export again**, and **Pick again**.

Filenames are deterministic and contain the chat title (made safe for filenames), the export scope (`chat` or the message's role), and the extraction timestamp.

### Markdown

The Markdown must be readable without the original page and keep source order. A whole-chat export has one section per message, headed with its position and role (for example "Message 3 · Assistant"), and inside each message uses descriptive headings where the source supports them: User message, Assistant message, Thinking or Reasoning, Activity steps, Tool call, Tool input, Tool result, File, Command, Output, Error, Final response. Extraction diagnostics go at the end.

- Do not add a heading when the source lacks evidence for the label. Put unknown content under **Unclassified content**.
- Label a code fence with a language only when the source identifies it or the inference is reliable; otherwise use an unlabelled fence.
- Code containing backticks must never break its fence. Use a fence longer than the longest backtick run inside.
- Render links with both label and destination, and a bare destination when a link has no label.

### JSON

Define a versioned JSON schema, document it in the README, and ship it as a JSON Schema file that the tests validate against. It contains at least:

- schema version, source application, page URL, page or chat title, chat surface, extraction timestamp, and extension version;
- export scope (whole chat or single message), and messages expected versus exported, with how "expected" was determined;
- an ordered array of messages, each with its index, role, boundary information, stable identifier where available, and metadata;
- within each message, ordered content blocks, each with:
  - the exact extracted text and a semantic block type;
  - an order index, and a nesting depth or parent identifier;
  - source-element metadata useful for debugging, and the initial disclosure or tab state;
  - where applicable: tool provider, tool type, status, arguments, command, output, filename, and link metadata;
  - sanitised HTML for the block where useful;
- diagnostics, unresolved or inaccessible regions, and whether the original interface state was restored.

Block types cover at least ordinary text, headings, lists, quotations, tables, code, reasoning, activity steps, tool calls, tool results, files, terminal commands, terminal output, links, images, errors, unknown content, and final responses. Add types where live inspection shows a need. Never group all thoughts or all tool calls together if doing so would change their sequence.

### Sanitised HTML

Remove scripts, inline event handlers, executable URLs, the extension's own controls, unrelated page chrome, hidden authentication or application state, and attributes that expose private implementation data without helping reproduce the content. Keep the structural elements, text, links, code, tables, and accessibility labels needed to understand the chat. Build it by cloning and walking nodes, not by pushing HTML strings through page sinks (Trusted Types, field guide 6.4).

---

## 10. Preview, diagnostics, and errors

After extraction, the preview shows:

- messages exported, and messages expected;
- counts of user and assistant messages;
- counts of ordinary text blocks, reasoning sections, activity steps, tool calls, and tool results;
- tabs visited and disclosures opened;
- unresolved controls and inaccessible regions;
- whether the original interface state, including scroll position, was restored.

JSON and Markdown carry an optional diagnostics section naming the selector strategies used, missing panels, timeouts, truncated virtualised regions, unsupported element types, low-confidence boundaries, and any shortfall against the expected message count. Diagnostics never mix with the extracted text. They are stored locally only.

User-facing errors distinguish at least: no chat found, no message found, low-confidence boundary, disclosure did not open, the conversation could not be fully loaded, and unsupported content. If Notion has replaced its chat structure entirely, fail with diagnostics. Never capture the whole page and never report an empty export as a success.

---

## 11. Architecture

- **Manifest V3.** Match the conventions of Josh's existing extensions (plain files, the bridge pattern, the icon set) unless they conflict with a requirement here. Use TypeScript with a small build step unless the existing projects give a strong reason not to; a bundler becomes useful once the code is split into the modules below.
- **Separate modules** for: the Notion adapter; the picker and overlay; disclosure, tab, and scroll traversal; semantic extraction; serialisation (one serialiser per format); the sanitiser; and the popup or side-panel UI. A Notion change should never require touching Markdown or JSON generation.
- **World choice.** The thread-record lookup needs the MAIN world, while `chrome.*`, clipboard, and downloads need the extension side. Choose a split and a bridge following field guide Part 2.
- **Permissions.** Request the narrowest set the implementation uses. Host permissions are `https://app.notion.com/*` and `https://www.notion.so/*` unless inspection shows otherwise. Candidates are `activeTab`, `scripting`, `storage`, `downloads`, `clipboardWrite`, and `contextMenus`. Confirm each against the code and remove any that are unused.
- **Local only.** No remote scripts, no remote code execution, no telemetry, no analytics, and no network calls carrying chat content.
- **Page styles.** Styles for the overlay and any in-page UI must not inherit Notion's rules. Use a shadow root or strict resets, and avoid HTML-string sinks.
- **Resilience:**
  - several selector strategies, with adapter-level diagnostics;
  - a `MutationObserver` for single-page navigation and chats mounted dynamically;
  - protection against duplicate listener registration and double injection (field guide 6.2);
  - cleanup whenever selection mode ends;
  - finite limits on every traversal;
  - restoration of interface state in a `finally` path, so it runs even when extraction fails.

The finished project contains: `manifest.json`, the service worker if required, content scripts, the adapter, picker and overlay, traversal, extraction, serialisers, sanitiser, popup UI, styles, icons, the JSON Schema, automated tests, synthetic DOM fixtures, a README with installation and usage instructions, `DEV-NOTES.md` recording the live structures you found, the evidence for each selector, and every disagreement with the field guide, a `MAINTENANCE-LOG.md` in the style of Josh's other extensions, a built `dist/` directory, and a packaged ZIP of `dist/`.

---

## 12. Testing

### Automated tests, on synthetic fixtures

Build DOM fixtures that reproduce the structures you found live, filled with invented text. They must include:

- a whole chat of several turns, with user and assistant messages alternating;
- a chat long enough to exercise scrolling, with a simulated lazy-loading or virtualised container matching the behaviour you observed;
- an ordinary user message and an ordinary assistant answer;
- a collapsed parent steps disclosure, with a collapsed Thought nested inside it;
- several thoughts and tool calls in a specific order;
- a file tool card with a filename and multi-line indented code;
- a terminal tool card with Command and Output tabs, in two variants: Output initially selected, and Command initially selected;
- a "show more" control;
- a long, internally scrollable output;
- an unsuccessful tool call with an error;
- an unknown block;
- links, mentions, a table, and code containing backticks;
- a fixture where one panel fails to open.

The tests must verify that:

- every message in the chat is exported exactly once, in order, and no block is attributed to the wrong message;
- collapsed reasoning is included, and both parent and nested disclosures are traversed;
- Command and Output are both included whichever tab was initially selected;
- file contents keep their indentation;
- source order is preserved within and across messages;
- repeated traversal and re-rendered messages do not duplicate content;
- unknown blocks survive, and links keep their destinations;
- every traversal terminates;
- every opened disclosure, changed tab, and scroll position returns to its original state;
- Markdown fences stay valid;
- JSON validates against the schema;
- sanitised HTML contains no scripts or inline event handlers;
- extraction still returns useful partial output with diagnostics when one panel fails;
- a shortfall against the expected message count produces a visible warning.

### Live verification on Josh's Notion

After the automated tests pass, test on the real interface through Chrome control: first by in-page injection, then with the unpacked extension loaded. Use at least:

- a chat with collapsed reasoning and visible final answers;
- a chat containing a file tool call;
- a chat containing a terminal tool call with Command and Output tabs;
- a chat long enough to need scrolling;
- the AI side panel, if Josh's Notion has one.

For each:

- pick the chat, and check the outline covers exactly that chat;
- export it;
- compare the export against every text-bearing region reachable through the ordinary interface, message by message;
- confirm that the message count matches, collapsed reasoning appears, tool cards appear in order, every tab panel appears, and code and command output are complete;
- confirm the page returns to its original disclosure, tab, and scroll state;
- test copying and downloading.

Then reload the Notion tab and repeat one export. Also test single-message export on one message from each chat type.

Fix every material failure, re-run the automated tests after each material fix, rebuild, and re-verify live. Do not claim a live test passed unless you performed it. If some check could not be run, say exactly which one and why.

---

## 13. Definition of done

The project is done when all of these are true:

- the source project exists and builds without errors;
- the build loads as a Manifest V3 extension;
- the picker identifies a chat, and single-message mode identifies one logical message;
- a whole-chat export contains every message, in order, with no message missing or duplicated, or else visibly reports a shortfall;
- ordinary input and output, collapsed reasoning, nested steps, tool calls and results, file cards with complete code, and both terminal panels are included;
- source order is preserved, and content never leaks between messages;
- Markdown, plain text, JSON, and sanitised HTML exports work;
- copying to the clipboard and downloading files work;
- the interface's original state is restored;
- automated tests pass, and live tests pass as far as the environment permits;
- all data is stored and processed locally;
- the README, DEV-NOTES, and MAINTENANCE-LOG exist;
- `dist/` exists, and the ZIP exists.

---

## 14. Final report

Return only after completing as much implementation and verification as the environment permits. When ambiguity remains, choose the behaviour that captures more user-visible content while preserving order, keeping messages separate, and restoring the interface. A limitation does not license omitting a required feature before trying the available methods.

Report:

- the project directory, the built extension directory, and the ZIP path;
- how to load the unpacked build into Chrome, click by click;
- how to export a chat, and how to export a single message;
- which automated tests ran and passed;
- which live tests you performed and their results;
- every remaining limitation, stated precisely;
- which files or modules to edit if a future Notion change breaks chat or message detection.
