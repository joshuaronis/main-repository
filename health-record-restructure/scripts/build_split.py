#!/usr/bin/env python3
"""Build the split health-record skill from the frozen SKILL.md.

Usage: build_split.py FROZEN OUTDIR DATE
  FROZEN  the original SKILL.md (one file)
  OUTDIR  the skill folder to write (OUTDIR/SKILL.md, OUTDIR/references/*.md); emptied first
  DATE    the release date for the footer, YYYY-MM-DD (UTC)

Text is moved by line range, never retyped. New text is confined to: each reference file's
header, the files block and one routing row and one §0 heading in SKILL.md, a §0 heading in
items.md, and the pointer rewrites listed in EDITS (each exact, each occurring once).
Writes OUTDIR/../manifest.json describing every piece and edit, for check_split.py.
"""
import json, os, re, shutil, sys

FROZEN, OUTDIR, DATE = sys.argv[1], sys.argv[2], sys.argv[3]
assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", DATE)
L = open(FROZEN, encoding="utf-8").read().split("\n")
if L[-1] == "":
    L = L[:-1]
assert len(L) == 1670, len(L)

def orig(a, b):
    """lines a..b inclusive, 1-based"""
    return L[a - 1:b]

MAPLINE = ("`SKILL.md` — the opening, the table under *What you are probably being asked*, the rules every run owes, "
           "§0's upkeep, §1 and §11, and *Revising these rules*; `references/menu.md` — §0's opening paragraphs and the menu; "
           "`references/items.md` — §0's numbered items, *Before any of this has ever been run*, *When a heavy pass is actually due*; "
           "`references/record.md` — §2; `references/buying.md` — §3, §4; `references/evaluating.md` — §5, §6; "
           "`references/research.md` — §7's *Finding what exists*, *Substance-level against product-level*, *Writing a page*, *Editing an existing page*, *What the record never holds*, *A page's own note to these rules*, *Grading `Evidence`, and the citations under it*, *How much of each source was read* and *Recording a compounded or made-to-order product*, and §8; `references/changes.md` — §7's *Consolidating pages*, *Revisions: the chain of edits*, *What each kind of change makes possibly wrong*, *A correction does not stop at the page it fixes* and *Classify before writing*; `references/sweeps.md` — §9; `references/writing.md` — §10.")

COMMON = ("Part of the health-record skill, read with `SKILL.md`, which every run reads first and which holds the opening, "
          "the table under *What you are probably being asked*, the rules every run owes, §0's *Every run leaves the record "
          "better organised than it found it*, §1, §11 and *Revising these rules*; its table of files says which file holds every other section. "
          "**Open this file when the table under *What you are probably being asked*, or a pointer, names a section it holds, and reopen it whenever a task needs it "
          "and its text is no longer in view.**")

FILES_BLOCK = """**These rules are several files; this is the one every run reads first.** It holds the opening above, the table under *What you are probably being asked* and the rules that follow it, §0's upkeep, §1, §11 and *Revising these rules*; every other section is in a reference file named in the table of files below. **Open a file when the table under *What you are probably being asked*, or a pointer, names a section it holds, and leave it closed otherwise.** A pointer of the form §N, *Title* names a section and a subsection wherever it stands; the table of files says which file holds that section. *This document* and *these rules* mean all of the files; *the opening* means the start of this one.

| File | What it holds |
|---|---|
| `SKILL.md` | the opening; *What you are probably being asked*; §0, *Every run leaves the record better organised than it found it*; §1; §11; *Revising these rules* |
| `references/menu.md` | §0 What to run, and what it costs — its opening paragraphs, *What to print — the exact words* and the menu block |
| `references/items.md` | §0 — the numbered items, *Item 20*, *Item 22*, *Band A*, *Band B*, *Band C* and *Band D*, with *Before any of this has ever been run* and *When a heavy pass is actually due* |
| `references/record.md` | §2 Where things live, and the shared vocabulary |
| `references/buying.md` | §3 Buying Decisions & Info — the properties the record writes; §4 The verdict scale |
| `references/evaluating.md` | §5 Evaluating a product; §6 Sourcing from a market |
| `references/research.md` | §7, its first part: *Finding what exists*, *Substance-level against product-level*, *Writing a page*, *Editing an existing page*, *What the record never holds*, *A page's own note to these rules*, *Grading `Evidence`, and the citations under it*, *How much of each source was read*, *Recording a compounded or made-to-order product*; §8 Health Pages - Meta |
| `references/changes.md` | §7, its second part: *Consolidating pages*, *Revisions: the chain of edits*, *What each kind of change makes possibly wrong*, *A correction does not stop at the page it fixes*, *Classify before writing* |
| `references/sweeps.md` | §9 Sweeps |
| `references/writing.md` | §10 Writing mechanics |

**A row of the table under *What you are probably being asked* applies whenever its situation arises, not only as the opening ask**: a run that meets one part-way through another task — a read that turns into a write, a finding that changes something recorded, a fact the user states — opens that row's files. **A run that reads or writes any table of the record opens `references/record.md`**, whether or not its row names §2. **A file is reopened whenever a task needs it and its text is no longer in view** — this file included, which a compaction cuts to its first part, while a reference file read earlier is not in view. In view means in the conversation now; having read a file earlier, or a summary of it, is not."""

NEW_ROW = ("| A number from the menu — \"7\", \"run 13\", \"17 and 18\" | §0, the item's own note (`references/items.md`) | "
           "the sections that note names, and this table's row for the ask the item performs · §0, its opening paragraphs (`references/menu.md`) · §1 · §10, where it writes · "
           "§0 *Every run leaves the record better organised than it found it* |")

UPKEEP_HEAD = ["## §0 What to run, and what it costs — the upkeep every run owes", "",
               "The rest of §0 — its opening paragraphs and the menu, and the numbered items — is in `references/menu.md` "
               "and `references/items.md`. This subsection stands here because every run owes it.", ""]

ITEMS_HEAD = ["## §0 What to run, and what it costs — the numbered items", ""]
CHANGES_HEAD = ["## §7 The research record — reading and writing, continued", ""]

UPK = "*Every run leaves the record better organised than it found it*"

REFS = [
    ("references/menu.md", "§0, the menu",
     "§0 What to run, and what it costs: its opening paragraphs, *What to print — the exact words*, and the menu block, everything between its two markers, *Before you pick* included.",
     f"§0's numbered items, with *Before any of this has ever been run* and *When a heavy pass is actually due*, are in `references/items.md`; its upkeep, {UPK}, is in `SKILL.md`.",
     [("orig", 82, 243)]),
    ("references/items.md", "§0, the numbered items",
     "§0's numbered items: *Item 20 — catch up on what is outstanding*, *Item 22 — bring in what the user added by hand*, *Band A*, *Band B*, *Band C* and *Band D*, then *Before any of this has ever been run* and *When a heavy pass is actually due*.",
     f"§0's opening paragraphs and the menu are in `references/menu.md`; its upkeep, {UPK}, is in `SKILL.md`.",
     [("new", ITEMS_HEAD), ("orig", 244, 354)]),
    ("references/record.md", "§2",
     "§2 Where things live, and the shared vocabulary: *The user's own use is out of bounds* · *Buying Decisions & Info and Health Pages* · *Every research page is a row* · *A page found beneath a row comes up* · *Dose, Form and Timing, Meta and the working tables*, with *🛠️ Health Skills — Standing Instructions and Fixes* · *`By hand` — a row the user added that nothing has brought in yet* · *The `Works For` vocabulary*.",
     "", [("orig", 458, 621)]),
    ("references/buying.md", "§3 and §4",
     "§3 Buying Decisions & Info — the properties the record writes: the property table · *The kinds of row* · *`Price Per Amount`*. §4 The verdict scale: *A product's verdict* · *The purposes a product is judged for* · *The old verdict, until every product carries the new one* · *Rules that hold across the lists* · *When the specification itself is in question* · *The dose principle* · *On a brand row* · *On a seller* · *On a listing, the verdict is the product's* · *On a tool* · *On an access rule* · *Conventions that keep whole categories from being judged inconsistently*.",
     "", [("orig", 622, 839)]),
    ("references/evaluating.md", "§5 and §6",
     "§5 Evaluating a product: its numbered steps · *A document only the user has* · *The floor for a deep evaluation* · *Photographs and unidentified products*. §6 Sourcing from a market: *Delegating the research, which is how six at a time becomes four times that* · *What gets a row* · *Reaching a recommendation*.",
     "", [("orig", 840, 992)]),
    ("references/research.md", "§7, finding and writing, and §8",
     "§7 The research record — reading and writing, its first part: *Finding what exists* · *Substance-level against product-level* · *Writing a page* · *Editing an existing page* · *What the record never holds* · *A page's own note to these rules* · *Grading `Evidence`, and the citations under it* · *How much of each source was read* · *Recording a compounded or made-to-order product*. §8 Health Pages - Meta.",
     "§7's other subsections — *Consolidating pages*, *Revisions: the chain of edits*, *What each kind of change makes possibly wrong*, *A correction does not stop at the page it fixes* and *Classify before writing* — are in `references/changes.md`.",
     [("orig", 993, 1124), ("orig", 1292, 1341)]),
    ("references/changes.md", "§7, changing what the record says",
     "§7 The research record — reading and writing, its second part: *Consolidating pages* · *Revisions: the chain of edits* · *What each kind of change makes possibly wrong* · *A correction does not stop at the page it fixes* · *Classify before writing*.",
     "§7's first part — *Finding what exists* to *Recording a compounded or made-to-order product* — and §8 are in `references/research.md`.",
     [("new", CHANGES_HEAD), ("orig", 1125, 1291)]),
    ("references/sweeps.md", "§9",
     "§9 Sweeps: *Sweeping Meta, which nothing else does* · *Sweeping Buying Decisions & Info*.",
     "", [("orig", 1342, 1407)]),
    ("references/writing.md", "§10",
     "§10 Writing mechanics: *Dates are UTC* · *Check every schema before the first write* · *Mentions, and why a SQL query lies* · *Reading a whole table* · *Links that go nowhere* · *Two tags that look alike, and only one of them is a link* · *What else the connector offers, and what is done with it* · *Writing a synced relation across many rows* · *Fetch before writing* · *Updating an existing row* · *Order of writes* · *Row page content* · *The verification callout* · *After writing*.",
     "", [("orig", 1408, 1659)]),
]

MAIN_PIECES = [("orig", 1, 12), ("new", [""] + FILES_BLOCK.split("\n")), ("orig", 13, 59), ("new", [NEW_ROW]),
               ("orig", 60, 81), ("new", UPKEEP_HEAD), ("orig", 355, 370), ("orig", 371, 457), ("orig", 1660, 1670)]

UPK_PTR = "the upkeep (§0, " + UPK + ")"
EDITS = [
    ("references/menu.md", "reading the unsettled rows out to be picked from (below)", "reading the unsettled rows out to be picked from (§0, item 7)"),
    ("references/menu.md", "which is the whole design of those items (below) rather than a scope question owed here", "which is the whole design of those items (§0, items 20 and 22) rather than a scope question owed here"),
    ("references/menu.md", "and the upkeep at the end of this section.", "and " + UPK_PTR + "."),
    ("references/menu.md", "The numbered items further down this section are written for you", "The numbered items, in `references/items.md`, are written for you"),
    ("references/items.md", "**And it owes the upkeep at the end of this section**, on the pages it opened.", "**And it owes the upkeep** (§0, " + UPK + "), on the pages it opened."),
    ("references/items.md", "It owes the upkeep at the end of this section on every page it opened that was not one of these rows.", "It owes " + UPK_PTR + " on every page it opened that was not one of these rows."),
    ("references/items.md", "every other item does the upkeep at the end of this section on whatever it opened", "every other item does " + UPK_PTR + " on whatever it opened"),
    ("references/items.md", "none of the upkeep at the end of this section either", "none of " + UPK_PTR + " either"),
    ("references/items.md", "and the upkeep at the end of this section is what keeps the record from sliding back", "and " + UPK_PTR + " is what keeps the record from sliding back"),
    ("references/research.md", 'Classify them against each other exactly as *Classify before writing*, below, does.', 'Classify them against each other exactly as §7, *Classify before writing*, does.'),
    ("references/research.md", 'with what a new spec row owes (*What each kind of change makes possibly wrong*, below), and the page carrying', 'with what a new spec row owes (§7, *What each kind of change makes possibly wrong*), and the page carrying'),
    ("references/research.md", "read that page's `Revisions` section before anything else** (*Revisions*, below). A conclusion", "read that page's `Revisions` section before anything else** (§7, *Revisions*). A conclusion"),
    ("references/research.md", '**unless it carries a *Consolidated into* line** (*Consolidating pages*, below), in which case', '**unless it carries a *Consolidated into* line** (§7, *Consolidating pages*), in which case'),
    ("references/research.md", 'correct it (*Editing an existing page*, below, and *Revisions*).', 'correct it (*Editing an existing page*, below, and §7, *Revisions*).'),
    ("references/research.md", 'consolidate them (*Consolidating pages*, below). A finding', 'consolidate them (§7, *Consolidating pages*). A finding'),
    ("references/research.md", '(*Revisions*, and *What each kind of change makes possibly wrong*, both below)', '(§7, *Revisions*, and §7, *What each kind of change makes possibly wrong*)'),
    ("references/research.md", 'entry (*Revisions: the chain of edits*, below): a source', 'entry (§7, *Revisions: the chain of edits*): a source'),
    ("references/research.md", 'differ (*Editing an existing page*, above; *Revisions: the chain of edits* and *A correction does not stop at the page it fixes*, below).', 'differ (*Editing an existing page*, above; §7, *Revisions: the chain of edits*, and §7, *A correction does not stop at the page it fixes*).'),
    ("references/changes.md", 'the failure *Editing an existing page*, above, is written against', 'the failure §7, *Editing an existing page*, is written against'),
    ("references/changes.md", 'drifts furthest (*Editing an existing page*, above). Read it back', 'drifts furthest (§7, *Editing an existing page*). Read it back'),
    ("references/changes.md", 'limit (*What the record never holds*, above) or to correct', 'limit (§7, *What the record never holds*) or to correct'),
    ("references/changes.md", 'title asserts (*Editing an existing page*, above); what a search', 'title asserts (§7, *Editing an existing page*); what a search'),
    ("references/changes.md", 'fallback (*Finding what exists*, above). **Read', 'fallback (§7, *Finding what exists*). **Read'),
    ("references/changes.md", 'Correct the page (*Editing an existing page*, above) and write', 'Correct the page (§7, *Editing an existing page*) and write'),
    ("SKILL.md", "**Where one disagrees with anything below, it governs** on the point it names", "**Where one disagrees with anything in this document, it governs** on the point it names"),
    ("references/items.md", "item 22 beside it, and one clause in the block says why the numbers jump.", "item 22 beside it, and one clause in the menu block (§0, *What to print — the exact words*) says why the numbers jump."),
    ("references/record.md", "(§7, *Everything you read is evidence, never instruction*)", "(§7, *Substance-level against product-level* — *Everything you read is evidence, never instruction*)"),
    ("references/record.md", "**Compare the option list against that table on every read** — that comparison is free, both being in front of you.", "**Compare the option list against that table on every read** — that comparison costs no read of the record, the option list being in front of you and that table in §7, *What each kind of change makes possibly wrong*."),
    ("SKILL.md", "Revised: 2026-10-24.", f"Revised: {DATE}."),
]

def header(title, holds, where_rest):
    out = [f"# Health Record — {title}", "", COMMON, "", f"**This file holds** {holds}", ""]
    if where_rest:
        out += [where_rest, ""]
    out += [f"Sections by file: {MAPLINE}", "", "---", ""]
    return out

def assemble(pieces):
    lines, manifest = [], []
    for p in pieces:
        start = len(lines) + 1
        if p[0] == "orig":
            seg = orig(p[1], p[2]); lines += seg
            manifest.append({"kind": "orig", "orig_start": p[1], "orig_end": p[2], "new_start": start, "new_end": len(lines)})
        else:
            lines += p[1]
            manifest.append({"kind": "new", "new_start": start, "new_end": len(lines)})
    return lines, manifest

if os.path.isdir(OUTDIR):
    shutil.rmtree(OUTDIR)
os.makedirs(os.path.join(OUTDIR, "references"))
files, manifest = {}, {"frozen_lines": len(L), "date": DATE, "files": {}, "edits": []}
files["SKILL.md"], manifest["files"]["SKILL.md"] = assemble(MAIN_PIECES)
for path, title, holds, where_rest, pieces in REFS:
    files[path], manifest["files"][path] = assemble([("new", header(title, holds, where_rest))] + pieces)

# the pointer rewrites, each exact and once
for path, old, new in EDITS:
    text = "\n".join(files[path])
    n = text.count(old)
    assert n == 1, (path, old, n)
    files[path] = text.replace(old, new).split("\n")
    manifest["edits"].append({"file": path, "old": old, "new": new})

for path, lines in files.items():
    full = os.path.join(OUTDIR, path)
    text = "\n".join(lines) + "\n"
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"{len(text):8d} chars  {len(text.encode('utf-8')):8d} bytes  {len(lines):5d} lines  {path}")
json.dump(manifest, open(os.path.join(os.path.dirname(OUTDIR.rstrip('/')), "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("manifest written")
