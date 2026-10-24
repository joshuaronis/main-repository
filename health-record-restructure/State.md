# health-record 2026-10-24 — State

**Claims**: the skill health-record (its 2026-10-24 release, `SKILL.md` md5 `267a832da408ed34ede1abd289e94645`, the copy Josh uploaded to this session, identical to `Skills/health-record/Releases/health-record 2026-10-24.zip`). No instruction of the folder is rewritten. Running in a Claude Code cloud session (branch `claude/elegant-newton-yd228c` of joshuaronis/main-repository). **Status: closed**, 2026-10-24 (UTC): released as `health-record-2026-10-24-0858` (`SKILL.md` md5 `a559cab3d323e7fe85189c9a61577d1d`); the notes for `Skills/health-record/` delivered as a zip; nothing moved in Josh's own folder, which was attached as a copy.

The folder was attached as a copy (`Skill Updates copy.zip`, with `Skills/health-record/` sent separately as `health-record copy.zip`), so nothing here is written into it: the write-back is delivered as the files that would sit under `Skills/health-record/`, and the release zip, for Josh to place.

## Josh's words (2026-10-24, this session)

- «Make sure that all functionality is kept, and that no contradictions or bugs are introduced.»
- «If you use subagents, please don't use them on Fable 5.1 … Use them on Opus 5.5. Or, alternatively, you can do it without subagents at all. Sometimes that works better, so long as you keep extremely detailed notes.»
- Later in the session: «you can also run more than 2 subagents at a time next time, but you really need to make sure that their reports don't mess things up, you need to audit all of their suggestions and make sure functionality is being preserved and there are no bugs or contradictions presented.» And: «Besides giving me the final skill and the final version of it and notes and info that would help improve it in the future that I should add under its subfolder in "skill updates" at the end I want you to give me any advice that you have for the folder itself, if it could be better in any way. GIve this last part to me as a prompt, since another session will take care of it.» Earlier: «What I'm really afraid will happen with subagents is that they'll introduce more and more contradictions each time, or undo the previous one's work with their suggestions. So you have to be really careful when you audit their fixes.» And: «you can run through the skill yourself a couple times as Fable 5.1, without using subagents, keeping really good notes».
- The prompt: «restructure my health-record skill into a short main file plus reference files, so that a chat using it loads only what its task needs, without losing anything the skill does. … Don't write anything in Notion: this job changes the skill's files, not my record.» «It changes the layout, not the rules: nothing is lost and nothing changes meaning. The main file keeps the opening (load the connector rules and the standing instructions first), the routing table and whatever every run needs. The menu goes in a reference file, opened only when I don't name a task. Each reference file holds sections a run reads only for some tasks, and the routing table says when to open which.» «A layout under which existing references keep working as written beats one that needs them rewritten. References by position, such as "above" or "below", break when they cross into another file.» «Split only at real section boundaries.» «After a compaction, Claude Code keeps only the first 5,000 tokens of a SKILL.md, about 20,000 characters (Claude Code's documentation, 2026-10-18)». «Text moved by script, cut at section boundaries, never retyped». «Check it by script and by reader … At least one independent reader, a sub-agent given the old and new text … Report, in a table, how much a run following each route loads before and after.» «The skill never names another skill or gives another skill's file path, and its description stays within 1,024 characters». «Give me back, in this chat, only what should be added to the notes folder's health-record section … Include the restructured skill as a zip of a folder named health-record holding SKILL.md and its reference files. Don't install it; I upload it myself.» «The testing is done, so don't repeat it.» «Don't read my other skills.»

## Settings (Process.md)

- Goal: the restructure above. Change type: structural (large). **Depth: Deep** (a structural change that isn't small). Bar: strict (skill over 30,000 characters). Stopping: a change Josh decided — the fix check (script + independent readers) is the last round; repairs are checked. Checkpoints: Josh said to work until done and ask only for what only he can do, so the Phase 2 checkpoint is not taken; every design call is logged below with how to undo it. Helpers: readers on Opus 5.5 only (his word); the editor does everything else. Budget: none set.
- Knowledge folder: the copy; README read in full, then Process.md, Long skills/Method.md, the briefs and scripts, and the health-record notes (About, Open items, Decisions, Lessons, Changelog, Judged list) before planning.
- Environments: Claude Code (SKILL.md auto-loaded; after a compaction only its first ~5,000 tokens stay; reference files read with the file tool, relative to the skill folder) and claude.ai chats (the skill uploaded as a zip; reference files load only when opened — Josh's own test, not repeated).

## Requirements

- R1 Main file holds the opening, the routing table and what every run needs; a run that opens no reference file still meets every cross-task rule and every end-of-run obligation. Test: list the rules the text itself says every run owes; each is in SKILL.md.
- R2 The menu is in its own reference file, opened only on a bare or vague invocation, together with the instructions for printing it. Test: the bare-invocation route loads SKILL.md + menu (+ §2 for the two queries' identifiers) and nothing else.
- R3 Each reference file holds sections a run reads only for some tasks; the routing table (with the file table) says when to open which; every reference file is named by path in SKILL.md; pointers say when to open. Test: script — every `references/*.md` path occurs in SKILL.md.
- R4 Nothing lost, nothing changes meaning: every line of the old text appears in exactly one new file; text moved by script at section boundaries; the only differences are pointers changed or added on purpose, each listed. Test: script coverage + diff of the reassembled text against the original.
- R5 Every way of asking, including a number from the menu, leads to the file that does the work. Test: a routing row for a bare number; reader walks "7", "run 13", "17 and 18".
- R6 Mid-task situations are caught by SKILL.md before the handling file is open. Test: a sentence in SKILL.md that a row applies whenever its situation arises; reader walks a read that turns into a write, a correction met during item 2, a user stating a fact mid-evaluation.
- R7 Cross-references, internal and external, still lead to their section, and a reader in any file can tell which file holds it; no positional reference crosses a file. Test: xref_check on the reassembled text; a cross-file resolver for every `§N, *Title*` and bare `§N`; the positional-pointer list reviewed (positional.txt), none crossing.
- R8 The pointers added follow the skill's own text rules (a pointer names a section and subsection and carries no gloss; no count of a growable list; no false only/never). Test: read each added line against line 61's rules.
- R9 Shared terms, exceptions and precedence are reachable on the route that applies them: §2's definitions reached from every file via the map; the opening's precedence stays in SKILL.md. Test: reader.
- R10 Text that works whole stays whole: the menu block with its instructions (lines 96–242), every table, numbered steps, §10's templates in code blocks, §3's property table. Test: cuts only at `##`/`###` boundaries of the original; code fences balanced per file.
- R11 Deliberate repetitions stay with their surrounding text (nothing deduplicated). Test: coverage (R4).
- R12 What the skill hands to sub-agents (§6, *Delegating the research*) is unchanged and reachable. Test: reader.
- R13 Long chats: the opening, the file table with the reopen rule, the routing table and the cross-task rules sit in SKILL.md's first ~20,000 characters; SKILL.md says to reopen any file, itself included, whenever its text is no longer in view. Test: measure the offset of the end of the cross-task rules; reader walks a resumed item 20 after a compaction.
- R14 Revisability: the file table in SKILL.md and each reference file's header say which file holds what; Lessons.md's *What must change together* lists the parts across files; Changelog, About and Open items updated. Test: notes written.
- R15 Economy: boundaries drawn from what tasks load together; per-route load table before/after; few files; each long file opens with the list of sections it holds. Test: the table in the delivery.
- R16 Checks: script and at least one independent reader (Opus 5.5) given old and new text, walking each kind of task, one switching mid-task, one resumed after compaction. Test: the readers' outputs, judged.
- R17 Never names another skill or its path; description ≤ 1,024 characters. Test: grep; measure.
- R18 Delivery: the notes for `Skills/health-record/` only, and the stamped release zip; nothing written in Notion; nothing installed. Test: the delivery message.
- R19 (derived, from the README) Release through `release.py`, which stamps the name, folder, zip and title with the UTC date and time (Josh, 2026-10-24); the notes keep the plain name.

## Invariants

Every rule's meaning and wording (save the pointers listed under *Edits*); the section numbers and every heading title; the frontmatter description; the house style; no other skill named; the connector rules and the standing instructions loaded first; the menu block printed verbatim; nothing in Notion changed.

## Inventory

For a general structural change at Deep, the skill's own map of sections and subsections (measure.py's output, 2026-10-24) is the inventory: 12 `##` sections, 70 `###`/`####` subsections, 1,670 lines, 441,536 characters. Every line is mapped to one destination below; nothing is removed.

## Design (Phase 2), with the reasons

**Cut points are the original section boundaries, one `##` section per file, except §0, which is cut at three of its `###` boundaries**, because §0 alone serves three audiences (printing the menu; running an item; every run's upkeep). Why not cut §2, §7 or §10 by subsection: positional.txt lists every "above"/"below"/"this section" pointer with its home; all 290 of them point inside their own `##` section except nine in §0 (menu lines 90 ×2, 92, 98; items 268, 274, 276, 318, 339). Cutting §7 between its reading half and its propagation half would cross about twenty such pointers (*Writing a page* → *Consolidating pages*, *Revisions*; the table → *Editing an existing page*, *Consolidating pages*; the fan-out and *Classify before writing* → *Revisions*, the table), each needing a rewrite; the same for §2 (`By hand`, *Every research page is a row*, *A page found beneath a row comes up*, the queue) and §10. The prompt prefers a layout under which references keep working as written.

**Files** (all paths within the skill folder):

| File | Original lines | Holds |
|---|---|---|
| `SKILL.md` | 1–15, 16–81, 355–370, 371–457, 1660–1670 | frontmatter, title, opening; [new: files paragraph, file table, reopen rule]; routing table [new row: a number from the menu] and the cross-task rules; [new heading] §0's *Every run leaves the record better organised than it found it*; §1; §11; *Revising these rules* |
| `references/menu.md` | 82–243 | §0's heading and opening paragraphs, *What to print — the exact words*, the menu block (markers included), *Before you pick* |
| `references/items.md` | 244–354 | [new heading] §0's *Item 20*, *Item 22*, *Band A*–*Band D*, *Before any of this has ever been run*, *When a heavy pass is actually due* |
| `references/record.md` | 458–621 | §2 |
| `references/buying.md` | 622–839 | §3, §4 (§3 points "below" into §4's lists, line 629, so they share a file) |
| `references/evaluating.md` | 840–992 | §5, §6 |
| `references/research.md` | 993–1124, 1292–1341 | §7's first part (*Finding what exists* to *Recording a compounded or made-to-order product*) and §8 |
| `references/changes.md` | 1125–1291 | [new heading] §7's second part (*Consolidating pages* to *Classify before writing*) |
| `references/sweeps.md` | 1342–1407 | §9 |
| `references/writing.md` | 1408–1659 | §10 |

Why these groupings: §3+§4 forced by a pointer and by use (every buying-table route owes both); §5+§6 are the product-research pair (sourcing feeds evaluation, §6's opening); §7 is cut at *Consolidating pages* because the first route-load table (2026-10-24, before the cut) showed the product routes at 77% of the original, pulling all of §7 for four subsections of its first half — the cut costs fifteen pointer rewrites, each mechanical and checked, and brings those routes to 66%; §8 goes with §7's first part because *Finding what exists* leans on §8 for whether a Meta row is live and §5/§6 write Absences there; §9 stands alone because only sweeps (items 15, 16, 19 and "fix these rows") need it, and the sweep route already opens items.md for *When a heavy pass is actually due*; §10 stands alone because every write needs it and nothing else does; §2 stands alone because nearly every route needs it and it is the shared vocabulary.

Why §1, §11 and the upkeep are in SKILL.md: §1 is the report, the plain-English rule and the four irreversible acts, owed by every run that reports (all of them); the upkeep is owed by every run (line 65); §11 and *Revising these rules* are tiny and cross-task.

**Order in SKILL.md**: opening → files paragraph, file table, reopen rule → routing table and cross-task rules → §0's upkeep → §1 → §11 → *Revising these rules*. The opening and the file table come first so that the reopen rule and the map survive a compaction; the routing table and cross-task rules follow and are measured to end inside the first ~19,500 characters.

**Headers**: each reference file opens with a title, a paragraph saying what it is part of, what SKILL.md holds, when to open and reopen a file, the list of sections and subsections it holds, and one line mapping every section to its file (identical in every file, generated from one table in the build script).

## Edits (pointers changed on purpose), each exact, each once

- menu, line 90: "reading the unsettled rows out to be picked from (below)" → "… (§0, item 7)".
- menu, line 90: "which is the whole design of those items (below) rather than a scope question owed here" → "… (§0, items 20 and 22) …".
- menu, line 92: "and the upkeep at the end of this section." → "and the upkeep (§0, *Every run leaves the record better organised than it found it*)."
- menu, line 98: "The numbered items further down this section are written for you" → "The numbered items, in `references/items.md`, are written for you".
- items, lines 268, 274, 276 (a heading), 318, 339: "the upkeep at the end of this section" → "the upkeep (§0, *Every run leaves the record better organised than it found it*)".
- §7, crossing the cut at *Consolidating pages*: lines 1019, 1035, 1045, 1049, 1050, 1051, 1072, 1102, 1115 (first part, "below" → `§7, *Title*`) and 1139, 1140, 1171, 1203, 1208, 1276 (second part, "above" → `§7, *Title*`).
- SKILL.md, line 1670: "Revised: 2026-10-24." → the release date.

Additions: the files paragraph, file table and reopen rule after line 12; one routing row after line 59; the `## §0 …` heading and one sentence before line 355; a `## §0 …` heading at the top of items.md's text; each reference file's header.

## Decisions log (calls made for Josh, each with how to undo)

- D1 No Phase 2 checkpoint, per his instruction to work until done. Undo: none needed; the design is above for review.
- D2 §7 cut at *Consolidating pages* into `research.md` (with §8) and `changes.md`, with fifteen "(*Title*, above/below)" pointers rewritten as `§7, *Title*` and one bare title reference (old line 1088) left: taken after the first load table showed the product routes at 77% with §7 whole, 66% with it cut. Undo: rejoin the two files and restore the fifteen pointers (the build script's EDITS list holds each old text).
- D3 Six "the upkeep at the end of this section" phrases rewritten to the full `§0, *Every run leaves the record better organised than it found it*` form rather than to a bare "(§0)", because §0 now has three homes and a bare §0 pointer no longer says which. Undo: restore the phrase and move the upkeep into items.md (then every run would have to open items.md).
- D4 The standing instructions were not read from Notion for this job: it changes no rule, keeps every section number and title that an instruction could name, and Josh asked that nothing be done in Notion; the notes' list of 2026-10-24 (three rows in force) stands. Undo: read the `Open` rows before the next rule change, as Lessons.md says.
- D5 Release stamped by `release.py` (Josh's decision of 2026-10-24 on names), so the delivered folder and zip are `health-record-<YYYY-MM-DD-HHMM>`, not the plain `health-record` the prompt names. Undo: rename the folder and the frontmatter `name:`/title back to `health-record` before uploading.
- D6 `references/record.md` is to be opened by any run that reads or writes a table, whether or not its row names §2 (a sentence added to SKILL.md): §2 holds the identifiers every Notion call needs, which the single file supplied implicitly. Undo: delete the sentence.

## To do

- [x] Read the folder, the notes, the skill (nine parts), the sibling (then set aside at Josh's word).
- [x] Measure sections; list positional pointers; choose the cut points.
- [x] Build the files by script; manifest of moves and edits (build_split.py; out/manifest.json).
- [x] Script checks: coverage, reassembled diff, xref_check, cross-file resolver, positional pointers, reachability, sizes, description, no other skill named, fences (check_split.py: 0 problems; xref_check on the concatenation: none unresolved).
- [x] Per-route load table (route_loads.md): mean 47% of the original; product routes 66%; the sweep 77%; the light routes 18–23%. SKILL.md's cross-task rules end at 19,983 characters.
- [x] Readers (Opus 5.5): two, old and new text, task walks including a mid-task switch and a post-compaction resume (running since 2026-10-24 about 07:40 UTC); judge every finding against the text and the judged list; repair only what survives.
- [x] Repairs already queued from my own passes, to apply in one rebuild once the readers have returned: F1 ("that table" → the table under *What you are probably being asked*, in the files block and in every header's common sentence); F3 (items.md header and the table of files name *Band A*, *Band B*, *Band C* and *Band D*); F4 (menu.md header and the table of files: *Before you pick* is inside the menu block, not beside it).
- [x] Convergence round (Josh, 2026-10-24: more than two helpers at a time is fine): three fresh Opus readers at once on the repaired text — task walks forward; task walks reversed; every new or changed line with its parallels and premises across files, and the headers. Stop when what they confirm is nothing or a few narrow cases; otherwise another round.
- [x] Own passes between rounds (cold read; seams by search; every-run obligations; headers by script; the changed-lines re-read).
- [x] Folder advice, as a prompt for another session (`folder_advice_prompt.md`, delivered) (Josh, 2026-10-24): what this job found wanting in the folder — single-text scripts and briefs against a multi-file skill, the md5 listing doubled across About and the changelog for ten files, release.py's stamped title, where cloud sessions keep working files, prompts that predate the stamping rule.
- [x] Cold read of SKILL.md and each header.
- [x] Release with release.py in a replica of the folder; md5s (finalize.py).
- [x] Write back: About, Changelog, Lessons, Open items, Decisions, Judged list — verify_notes.py and check_folder.py pass on the replica.
- [x] Deliver: the notes zip, the skill zip, the folder-advice prompt, Josh's own steps (the final message).

## Lessons as they happen

- (2026-10-24) The read tool truncates the skill's long lines; `number_and_split.py` with the default fold made nine readable parts. A measurement script over `##`/`###` spans gave the sizes the design needed in one pass.
- (2026-10-24) A grep for "above", "below", "this section", "end of this", "further down" with 110 characters of context was enough to classify every positional pointer by hand in one reading; the result decided the design (only §0 can be cut by subsection without rewriting pointers; §7 at the cost of fifteen).
- (2026-10-24) The folder's xref_check.py caught a defect in my own new text on the first build: a map line reading "§11, *Revising these rules*" parses as a pointer to a subsection that does not exist. Run it on the concatenation of every file after any edit to a header or map.
- (2026-10-24) The first load table, computed before the readers ran, changed the design (D2): compute it as soon as a candidate exists, not at the end.

## Own pass (Fable 5.1), lens: cold read of SKILL.md, then the seams by search — 2026-10-24, while readers A and B run

- **F1 (to fix once the readers have returned, so their files do not change under them)**: in the files block, "**Open a file when that table, or a pointer, names a section it holds**" follows "named by its path in the table of files below", so "that table" reads as the table of files, not the routing table; the same shape is in every reference file's header ("its table of files says which file holds every other section. **Open this file when that table, or a pointer, …**"). Introduced by my own trim of the block (the untrimmed wording named the table under *What you are probably being asked*). Repair: name the routing table explicitly in both places; cost about 45 characters in the first part of SKILL.md.
- **F2 (judged, left)**: old line 1547 (§10, *Updating an existing row*, now writing.md) says "The rules in this file were derived from cases"; "this file" now reads as writing.md. The files block defines *this document* and *these rules* as all the files but cannot define *this file* the same way, since the headers use "this file" for the reference file. No run acts differently; the fix would retype moved text; left, for the next change of that passage to turn into "these rules".
- Bare `(§0)` pointers (23) and bare `(§7)` pointers (21), each read with its sentence: the words beside each say which part (item 1's counts, the menu's *Waiting* line, the upkeep, a band's budget; a `Revisions` line, classifying a cluster, `Sources` as an index), and the table of files names the file for each part. None rewritten.
- "the opening" (26 uses) and "this document" (25 uses) in the moved text keep their sense under the files block's definitions.
- Scenario 13 (resumed after a compaction), walked on SKILL.md's first part alone: the reopen rule, the table of files and the routing row for "Catch up" are in view; the run reopens items.md (item 20), record.md (the queue's statuses), changes.md (§7's table) and writing.md before writing, and SKILL.md whole for §1 and the upkeep before reporting; the opening's rule on retained full text covers the connector rules and the standing instructions. No gap.
- Scenario 12 (a switch midway): line 29's rule sends the run to the "They discontinued it" row (changes.md, record.md, writing.md) and the "A fact that changes something already recorded" row (changes.md, research.md for §8); the paragraph under §7's table settles "the research says 400" against "I take 400"; §2's own-use rule is in record.md, already open for item 2. No gap.
- Scenario 14 (no reference file opened): the opening's precedence, the four cross-task rules, the overriding rules, the upkeep, §1's report rules, the four irreversible acts, the plain-English table and §11 are all in SKILL.md. No gap.

## Findings judged so far

- F2 above, left below the bar.

## How to resume

Working files are under `/tmp/claude-0/-home-user-main-repository/eadcf731-b6d3-5f3b-b82b-d927801b38cb/scratchpad/hr_job/`: `frozen/SKILL.md` (the original), `scripts/` (measure.py, positional.py, build_split.py, check_split.py), `out/health-record/` (the built skill), `positional.txt`, this file. Everything is rebuilt from `frozen/SKILL.md` by `build_split.py`.

## Round 1 — readers A and B (Opus 5.5), 2026-10-24, on the first candidate (SKILL.md `bc21c06f…`)

A: 16 scenarios, 0 serious, 4 minor (about 598,000 tokens, 32 minutes). B: 16 scenarios, 0 serious, 4 minor (about 589,000 tokens, 30 minutes). Three findings were the same from both; every finding was checked against the text before it moved. Judged:

- **Accepted, A1 = B1**: the routing row for a number from the menu reached items.md only, while old line 90 (what a pick fixes and leaves open; read the candidates back; items 17–19 take no subset) is in menu.md. Fix taken: the row also names §0's opening paragraphs (`references/menu.md`). Weighed and not taken: moving old line 90 into items.md (a cut inside §0's opening paragraphs, not at a heading, and "§0's opening paragraphs" would then span two files in every map).
- **Accepted, A4 = B2**: the files block said "§1 and §11; every other section is in a reference file" with *Revising these rules* in SKILL.md. Fixed in the block.
- **Accepted, A3 = B3**: items.md (old 246) "one clause in the block" names the menu block, now in menu.md. Rewritten "one clause in the menu block (§0, *What to print — the exact words*)" — B's form, the skill's pointer shape, rather than A's path form.
- **Accepted, A2**: the opening's "anything below" read literally reaches only SKILL.md's rules; "anything in this document", which the files block defines. The other two "below"s in that sentence point at SKILL.md's own later rules and stay.
- **Accepted, B4**: record.md (old 562) pointed at a bold entry inside §7's *Substance-level against product-level*, which no §7 file's list names; now names the subsection too. A scan (bold-entry pointers into split sections) found this the only such case.
- **Set aside, both readers' notes**: "this file" (F2); bare (§0)/(§7); nickname pointers into §7; bare title references across the §7 cut (old 1088, 1129); informal pointers to the menu; the wider record.md rule; the unrouted empty-result rule (same as the old text). *Before you pick* and "that table" were already queued (F4, F1) and are fixed.

Also applied: F1, F3, F4 from my own pass. Rebuilt; every script check passes; the first part ends under 20,000 characters again after two trims of my own text; 27 pointer rewrites in all (9 in §0, 15 in §7, 3 elsewhere).

## Round 2 — the convergence round: three fresh readers at once (Opus 5.5)

Lenses: C — task walks forward on the repaired text; D — task walks reversed, structure lens; E — every new or changed line (headers, files block, table of files, new row, new headings, the 27 rewrites) with its parallels and premises across files, plus the first part as a compaction leaves it. Stop if what they confirm is nothing or a few narrow loose ends; otherwise another round.

### Round 2, reader C (forward walks): 16 scenarios, 0 findings (about 537,000 tokens, 22 minutes)

Set-asides worth acting on cheaply, queued for the round-2 rebuild: every header's common sentence still lists SKILL.md's holdings as "§1 and §11" without *Revising these rules* (a parallel of the round-1 files-block repair; not false, but made consistent); the cross-task rules end at 20,052 characters, 52 over the stated figure — trim my own text in the files block by about 60 characters (no meaning changes). Set aside as C did: the repaired items.md pointer names *What to print — the exact words* for the menu block, which that subsection introduces; the bare-20/21/22 rows need no menu.md; record.md's bare "(*Revising these rules*)" is a title, placed by the table of files.

### Round 2, reader D (reverse walks, structure lens): 16 scenarios, 0 findings (about 579,000 tokens, 25 minutes)

Set-asides agree with C's and round 1's: the headers' "§1 and §11" (queued for consistency); the 20,052-character first part (queued trims); row 77's upkeep against item 21's carve-out (the item's note governs, as in the old row 75); the two §7 files' title labels; SKILL.md line 102's dash list not naming two subsections (no "only"; the table names them); the map repeated in ten places (a maintenance cost, recorded in Lessons); changes.md's `Availability` row saying "the pick" without its own §6 pointer (unchanged old text). Mechanical sweep clean.

### Round 2, reader E (changed lines, parallels, premises): 3 lenses, 1 minor finding (about 575,000 tokens, 26 minutes)

- **Accepted, E1**: §2's queue paragraph (old 546, record.md) — "that comparison is free, both being in front of you" rested on §7's table being in the same loaded text; now in changes.md. Repaired with E's wording ("costs no read of the record, the option list being in front of you and that table in §7, *What each kind of change makes possibly wrong*"); the rule unchanged. The one rewrite beyond a pointer; logged in Decisions. A grep of the old text for other reasons resting on what is loaded ("in front of you", "already loaded", "in view", "the text above/below") found no other.
- Also applied after round 2: the headers' common sentence names *Revising these rules*; six phrases of the files block shortened (no meaning changed); the cross-task rules now end at 20,005 characters. 28 text changes in all: 27 pointers (9 §0, 15 §7, 3 elsewhere) and E1.
- All scripts pass on the rebuilt text (SKILL.md md5 before stamping 79439afd…). Round 3 = reader F, a targeted check of the round-2 repairs only (SKILL.md and record.md whole, headers, search the rest). Stop after F unless it finds something broader than a loose end.

Stopping rule applied: round 2 (three fresh readers repeating round 1's lenses plus a new one on the fixed text) confirmed one narrow case; fixed; its check is round 3.

### Round 3, reader F (targeted check of the round-2 repairs): 0 findings (about 214,000 tokens, 11 minutes). Stopped.

Helper cost in all: six readers, about 3.1 million tokens on Opus 5.5.

### After the release: the stamp adds 32 characters

`release.py` stamps the `name:` line and the title of `SKILL.md` (16 characters each), so the released `SKILL.md` is 41,303 characters: the files block ends at 6,548, the routing table at 14,430, the cross-task rules at 20,037 (20,465 bytes). The notes were first filled from the build (41,271 / 6,516 / 14,398 / 20,005) and corrected; `finalize.py` now measures the released zip and asserts that the release differs from the build only in those two lines. Lesson: measure what is uploaded, not what was checked, whenever a release step rewrites anything.
