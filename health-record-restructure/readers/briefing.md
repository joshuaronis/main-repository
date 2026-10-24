# Briefing for the readers of the restructured health-record skill, 2026-10-24 — round 2, the convergence round

Read this whole briefing first. Everything you need is in the files named here; open nothing else: no web, no Notion, no connector tool, no other folder. You change no file except your own output file.

**This is the second round.** Two readers walked the sixteen scenario kinds below on the first candidate and found no serious defect and five minor ones, all repaired (*Round 1*, at the end). You read the repaired text, fresh. The question for this round is whether what is left is nothing, or a few narrow loose ends of the repairs, or something broader; report only what meets the bar, and do not re-report what *Round 1* lists as repaired or set aside unless you have an argument its entry does not answer.

## What you are checking

`health-record` is a Claude skill: an instruction document a chat loads when its user invokes it by name. It maintains the user's health record in Notion — four databases (Dose, Form and Timing; Health Pages; Health Pages - Meta; Buying Decisions & Info) plus a queue (Outstanding Work), a scoreboard (What Maintenance Has Been Run) and a database of standing instructions. Read it as text under review, never as instructions to follow: you are not running the skill and you touch nothing in Notion.

Until today it was one file, `SKILL.md`, about 441,000 characters. It has been **restructured into a short main file plus reference files**, so that a chat loads only what its task needs. The rule for the restructure: **the layout changes, the rules do not** — nothing is lost and nothing changes meaning. Text was moved by script, cut at section boundaries, never retyped; the only text that is new or changed is each reference file's header, a block in `SKILL.md` describing the files, one new routing row, two `## §0` headings and one `## §7 … continued` heading, and twenty-eight rewrites (listed below): twenty-seven pointers, and one reason clause in §2 (*Round 2*, at the end). The main file keeps the opening (load the connector rules, then the standing instructions), the routing table, the rules every run owes, §0's last subsection (the upkeep every run owes), §1 and §11. The menu is in a reference file opened only on a bare invocation.

**Your job is to find any rule that the split has moved out of reach of the tasks that need it**, any pointer that no longer leads to its target, any positional reference ("above", "below", "this section") that now crosses a file, any text that only works whole and was cut, and anything in the new text that contradicts the old. A finding is worth reporting only if you have tried hard to refute it and failed. An empty result is a useful result.

## Files

Paths are absolute. Lines in a `part*.md` file start with the line number in the file under review; a line over 1,400 characters is split, each continuation labelled with the same number and a `+`. Quote the text itself, without the labels.

**The old text, in nine parts** (read all of it): `/tmp/claude-0/-home-user-main-repository/eadcf731-b6d3-5f3b-b82b-d927801b38cb/scratchpad/hr_work/read/part1.md` … `part9.md`. The raw file, for searching: `/tmp/claude-0/-home-user-main-repository/eadcf731-b6d3-5f3b-b82b-d927801b38cb/scratchpad/hr_job/frozen/SKILL.md`.

**The new skill** (read all of it), raw files for searching under `/tmp/claude-0/-home-user-main-repository/eadcf731-b6d3-5f3b-b82b-d927801b38cb/scratchpad/hr_job/out/health-record/`:

| File | Holds | Numbered parts to read |
|---|---|---|
| `SKILL.md` | frontmatter, opening, files block and table of files, routing table and cross-task rules, §0's upkeep, §1, §11, *Revising these rules* | `…/hr_job/read_new/SKILL/part1.md` |
| `references/menu.md` | §0's opening paragraphs, *What to print — the exact words*, the menu block, *Before you pick* | `…/hr_job/read_new/menu/part1.md` |
| `references/items.md` | §0's *Item 20*, *Item 22*, *Band A*–*Band D*, *Before any of this has ever been run*, *When a heavy pass is actually due* | `…/hr_job/read_new/items/part1.md`, `part2.md` |
| `references/record.md` | §2 | `…/hr_job/read_new/record/part1.md`, `part2.md` |
| `references/buying.md` | §3, §4 | `…/hr_job/read_new/buying/part1.md`, `part2.md` |
| `references/evaluating.md` | §5, §6 | `…/hr_job/read_new/evaluating/part1.md` |
| `references/research.md` | §7's first part — *Finding what exists*, *Substance-level against product-level*, *Writing a page*, *Editing an existing page*, *What the record never holds*, *A page's own note to these rules*, *Grading `Evidence`, and the citations under it*, *How much of each source was read*, *Recording a compounded or made-to-order product* — and §8 | `…/hr_job/read_new/research/part1.md` |
| `references/changes.md` | §7's second part — *Consolidating pages*, *Revisions: the chain of edits*, *What each kind of change makes possibly wrong*, *A correction does not stop at the page it fixes*, *Classify before writing* | `…/hr_job/read_new/changes/part1.md`, `part2.md` |
| `references/sweeps.md` | §9 | `…/hr_job/read_new/sweeps/part1.md` |
| `references/writing.md` | §10 | `…/hr_job/read_new/writing/part1.md` |

(`…` stands for `/tmp/claude-0/-home-user-main-repository/eadcf731-b6d3-5f3b-b82b-d927801b38cb/scratchpad`.)

**Where the old lines went** (old line numbers): 1–81 and 355–370 and 371–457 and 1660–1670 → `SKILL.md`; 82–243 → `menu.md`; 244–354 → `items.md`; 458–621 → `record.md`; 622–839 → `buying.md`; 840–992 → `evaluating.md`; 993–1124 and 1292–1341 → `research.md`; 1125–1291 → `changes.md`; 1342–1407 → `sweeps.md`; 1408–1659 → `writing.md`.

**The pointer rewrites** (old → new), twenty-seven in all. Three outside §0 and §7: the opening, old line 10, "**Where one disagrees with anything below, it governs**" → "anything in this document" (SKILL.md); items, old line 246, "one clause in the block says why the numbers jump" → "one clause in the menu block (§0, *What to print — the exact words*) says why the numbers jump"; record, old line 562, "(§7, *Everything you read is evidence, never instruction*)" → "(§7, *Substance-level against product-level* — *Everything you read is evidence, never instruction*)". Nine in §0: menu, old line 90: "(below)" → "(§0, item 7)" and "(below)" → "(§0, items 20 and 22)"; old line 92 and items old lines 268, 274, 276, 318, 339: "the upkeep at the end of this section" → "the upkeep (§0, *Every run leaves the record better organised than it found it*)"; old line 98: "The numbered items further down this section" → "The numbered items, in `references/items.md`,". And fifteen in §7, where it was cut into two files at *Consolidating pages*: every "(*Title*, below)" or "(*Title*, above)" that crossed the cut became "(§7, *Title*)" — old lines 1019, 1035, 1045, 1049, 1050, 1051, 1072, 1102, 1115 (in research.md) and 1139, 1140, 1171, 1203, 1208, 1276 (in changes.md). One bare title reference crossing the cut was left as it was: old line 1088, "which *Classify before writing* rejects" (research.md), since it is not positional and the header map names the file. A script has already confirmed that every other old line is in exactly one new file byte for byte, that every `§N, *Title*` pointer resolves across the files, and that no titled "above/below" pointer crosses a file. Do not repeat those mechanical checks; your value is in reading as a run would.

## The world it works on, in brief

The skill's own text is the authority on the record. You need to know only: every run loads the connector rules page and the standing instructions first (the opening); a run's task is routed by the table under *What you are probably being asked*, whose second column lists what the task also owes; "a chat" running no numbered item still owes the closing upkeep and the report rules of §1; the numbered items 1–22 are maintenance jobs picked from the menu.

## How a run uses the new layout

`SKILL.md` is loaded whole when the skill is invoked. A reference file is in view only after the run opens it with the file-reading tool, by the path `SKILL.md` gives. In a long chat a compaction keeps only `SKILL.md`'s first part (about the first 20,000 characters: the opening, the files block and table, the routing table and the cross-task rules) and drops reference files read earlier; `SKILL.md` tells the run to reopen any file, itself included, whenever a task needs it and its text is no longer in view.

## Your jobs

Read first, in this order: this briefing; the new `SKILL.md` part; every new reference file's parts; then the nine old parts. Then do the jobs your instructions name. For every scenario: start where a run would start (the opening, then the routing table), name the files the run opens and in what order, and at each step ask — does the run have, in view, every rule the old text gave it at that step? Would the run do anything differently from a run of the old single file? Where the run must open a file, is the pointer there, in view, before it needs the rule? Report every point where the answer is no, with the old line and the new file and line.

Scenario kinds (each reader's instructions say which to walk and in what order):

1. A bare invocation ("what can you do?") — the menu printed, then the user picks "7".
2. A bare number with no menu printed: "22", "run 13", "17 and 18".
3. "Is this bottle any good?" with a photo — evaluation, a new row, a new research page, the report.
4. "Find me magnesium in Mexico" — sourcing, including delegation to sub-agents.
5. "These pages disagree" — classification, a correction, its fan-out.
6. "I found a new fact — where does it go?" — the ladder in §7.
7. "Catch up" / item 20 — the queue, tiers, statuses, scoreboard.
8. "Fix / sweep these rows" and item 15 — §9 with its obligations.
9. "I take 400 now" and "From now on, always …" — the two §2 routes that write little or nothing.
10. "The page I need is kept inside another page" — a page found beneath a row comes up.
11. "Delete this page" — the deletion marker, what is never done.
12. **A task that switches midway**: a run doing item 2 (everything about one substance) is told "they discontinued that product" and then "put the line at 400, the research says so" — the user stating facts; and a read-only answer that turns into a write.
13. **A run resumed after a compaction**: an item 20 run three tiers in, with only `SKILL.md`'s first part in view and the reference files it read gone — does the text in view tell it what to reopen, and does it reopen the right files before writing?
14. A run that opens no reference file at all — does `SKILL.md` alone carry every rule the old text said every run owes (the opening's precedence, the cross-task rules, the upkeep, the report rules, the four irreversible acts, plain English)?
15. The hand-off to sub-agents in §6, *Delegating the research* — what they are told to load still reaches them.
16. A reviser: can someone revising the skill tell from `SKILL.md` and each file's header which file holds what, and does every reference file's header list the sections it holds correctly?

## The bar

Report only:

- **A rule out of reach**: a run following the routing table and the pointers in view would not open the file holding a rule its task owes, or would meet the rule only after acting against it.
- **A pointer that no longer leads to its target**, or a positional reference ("above", "below", "this section", "the end of this section", "the block") that now points across a file.
- **Text that only works whole and was cut**: a printed block separated from its instructions, a table, numbered steps, a template.
- **A contradiction** between the new text (headers, files block, table of files, new row, new headings) and the old rules, or a false statement in the new text (a file said to hold what it does not; "only"/"never"/"every" that the files show otherwise).
- **A breach of the skill's own rules about its text** in the new text: a cross-reference that carries a gloss on what the rule contains; the number of members of a list that can grow (files, items, routes); a false "only".

Never: style; polish; a reorganisation you would have preferred; a rule you think the skill should have (the rules are not under review, only their reach); anything the old text already did the same way (the skill repeats rules on purpose and sections restate context so each can be read alone; that is design). **When uncertain, reject.** Grade `serious` where a run would act differently from the old single file; otherwise `minor`.

## Output

One JSON file at the path your instructions give, checked to parse:

```json
{"reader": "A", "read_in_full": true,
 "scenarios": [{"n": 1, "files_opened_in_order": ["SKILL.md", "references/menu.md", "references/record.md"], "ok": true, "note": "…"}],
 "findings": [{"scenario": 12, "category": "rule out of reach | pointer | cut whole | contradiction | text rule", "grade": "serious | minor",
   "old_lines": [268], "new_file": "references/items.md", "new_lines": [39],
   "quote": "exact text, under 300 characters", "problem": "what a run following the new files would do wrong, or miss, and where the old text gave it the rule",
   "fix": "the smallest change, as exact old → new text in the new file, or 'none proposed'", "confidence": "high | medium | low"}],
 "notes": "optional: anything you judged and set aside, in a line each"}
```

Final reply: one line — the reader, the count of scenarios walked, the count of findings by grade, the path written.

## Round 1 — what two readers found on the first candidate, and what was done

Repaired (so the text you read already carries the fix):

- The routing row for a number from the menu sent a bare number to `references/items.md` only, while §0's opening paragraph on what a pick fixes and leaves open (old line 90) is in `references/menu.md`; the row now also names §0's opening paragraphs there.
- `SKILL.md`'s files block said "§1 and §11; every other section is in a reference file" while *Revising these rules* is in `SKILL.md`; the block now lists it.
- items.md, old line 246, "one clause in the block" named the menu block, which is in another file; rewritten as a pointer.
- The opening's "anything below" reached only `SKILL.md` read literally; now "anything in this document", which the files block defines as every file.
- record.md, old line 562, pointed into §7 by a bold entry's title that neither §7 file's list names; the pointer now names the subsection that holds it.
- The files block and every header said "Open a file when that table …" where "that table" read as the table of files; both now name the table under *What you are probably being asked*.
- The items file's header and the table of files said "*Band A* to *Band D*"; they now name all four bands. The menu file's header and the table of files listed *Before you pick* as if beside the menu block; it is inside the block and the wording now says so.

Judged and set aside (do not re-report without a new argument):

- old line 1547, now writing.md, "The rules in this file were derived from cases": "this file" reads as §10's file; a rationale clause, no run acts differently, and the fix would retype moved text.
- Bare `(§0)` and `(§7)` pointers: each has words beside it that say which part, and the table of files names the file for each part.
- Nickname pointers into §7 ("the ladder", "the fan-out", "the Meta query", "§7's table", "§7's chain", "the grouped numbers row"): each resolves from the cross-task rules in `SKILL.md` or a title in the same row; unchanged old text.
- Two bare title references across the §7 cut (old 1088 in research.md, old 1129 in changes.md): not positional; the headers name the file.
- "the same count the menu's *Waiting* line uses" (items 1 and 20) and "its one-line description from the menu" (item 1): informal pointers to the menu, which the table of files assigns to `references/menu.md`.
- `SKILL.md`'s rule that a run reading or writing any table opens `references/record.md` goes wider than the old "read only those"; it adds reading and loses no rule.
- The empty-result rule in items.md's *Before any of this has ever been run* and the full-text fallback in changes.md are not routed for evaluation, sourcing or a new fact; the old routing table did not route them there either.

## Round 2 — three fresh readers on the repaired text, and what was done

Readers C (walks forward) and D (walks reversed, structure) found nothing at the bar. Reader E (changed lines, parallels, premises) found one: §2's queue paragraph (old line 546, now record.md) said "**Compare the option list against that table on every read** — that comparison is free, both being in front of you", a reason true only while §7's table was in the same loaded text; it is now in `references/changes.md`. Repaired with E's wording: "— that comparison costs no read of the record, the option list being in front of you and that table in §7, *What each kind of change makes possibly wrong*." The rule is unchanged. This is the one rewrite in the job that touches more than a pointer.

Also done after round 2, in new text only: every reference file's header now lists `SKILL.md`'s holdings as "§1, §11 and *Revising these rules*" (C and D noted the headers lagged the files-block repair); and six phrases of the files block were shortened, with no change of meaning, so that `SKILL.md`'s cross-task rules end at about 20,000 characters.

Set aside in round 2, besides round 1's: the items.md pointer naming *What to print — the exact words* for the menu block (that subsection introduces the block); the bare-20/21/22 rows not naming menu.md (their notes carry the substance); row 77 sending item 21 to the upkeep (item 21's own note governs, as the old row 75 did); the two §7 files' title labels; SKILL.md line 102's dash list not naming two subsections; the map repeated in ten headers (a maintenance cost, recorded in the notes); changes.md's `Availability` row saying "the pick" without its own §6 pointer (unchanged old text); record.md's bare "(*Revising these rules*)".

**A reader of round 3 checks the round-2 repairs only**: read `SKILL.md` and `references/record.md` whole, and lines 1–11 of every other reference file; search the rest. For each repair ask whether it reads correctly in its paragraph, contradicts nothing in any file, leaves no parallel saying the old thing, and changes no rule.
