#!/usr/bin/env python3
"""For each row of the routing table in the new SKILL.md, the files a run following it opens and
their total size, against the whole original file.

Usage: route_loads.py FROZEN OUTDIR

A row's files: SKILL.md always; the file holding each §N the row names (both columns); for §0,
the part the words beside it name (menu / item, items, Before any of this, When a heavy pass → items /
the upkeep → SKILL.md); and references/record.md for every row but one that reads or writes no table
(SKILL.md says a run that reads or writes any table opens it). Prints a markdown table.
"""
import os, re, sys

FROZEN, OUTDIR = sys.argv[1:3]
orig_size = len(open(FROZEN, encoding="utf-8").read())
files = ["SKILL.md", "references/menu.md", "references/items.md", "references/record.md", "references/buying.md",
         "references/evaluating.md", "references/research.md", "references/changes.md", "references/sweeps.md", "references/writing.md"]
size = {f: len(open(os.path.join(OUTDIR, f), encoding="utf-8").read()) for f in files}
SEC = {"1": "SKILL.md", "11": "SKILL.md", "2": "references/record.md", "3": "references/buying.md", "4": "references/buying.md",
       "5": "references/evaluating.md", "6": "references/evaluating.md", "8": "references/research.md",
       "9": "references/sweeps.md", "10": "references/writing.md"}
skill = open(os.path.join(OUTDIR, "SKILL.md"), encoding="utf-8").read()
tbl = re.search(r"\| The ask \| Where the work is done \| What the task also owes \|\n\|---\|---\|---\|\n((?:\|.*\|\n)+)", skill).group(1)
rows = [r for r in tbl.strip("\n").split("\n")]
NO_TABLE = {"Should I be taking this?"}   # rows whose run reads or writes no table
out = ["| The ask | Files a run following the row opens | Chars after | Chars before | Loads |", "|---|---|---|---|---|"]
tot_after = 0
for r in rows:
    cells = [c.strip() for c in r.strip("|").split(" | ")]
    ask, work, owes = cells[0], cells[1], cells[2]
    opened = {"SKILL.md"}
    for cell in (work, owes):
        for m in re.finditer(r"§(\d+)(?:\.\d+)?([^§|]*)", cell):
            n, tail = m.group(1), m.group(2)
            if n == "0":
                t = tail.lower()
                if "menu" in t and "item" not in t:
                    opened.add("references/menu.md")
                elif "every run leaves" in t or "upkeep" in t:
                    pass  # SKILL.md
                elif "item" in t or "before any of this" in t or "when a heavy pass" in t:
                    opened.add("references/items.md")
                else:
                    opened.add("references/items.md")   # a bare §0 beside "the scoreboard" etc.: the items' half
            elif n == "7":
                t = tail.lower()
                a = any(k in t for k in ("finding what exists", "substance-level", "writing a page", "editing an existing", "never holds", "own note", "grading", "how much of each source", "compounded", "the ladder", "the meta query", "alias rule"))
                b = any(k in t for k in ("consolidating", "revisions", "what each kind", "correction does not stop", "classify", "fan-out"))
                if a: opened.add("references/research.md")
                if b: opened.add("references/changes.md")
                if not a and not b:
                    opened.add("references/research.md"); opened.add("references/changes.md")
            elif n in SEC:
                opened.add(SEC[n])
    if not any(k in ask for k in NO_TABLE):
        opened.add("references/record.md")
    chars = sum(size[f] for f in opened)
    tot_after += chars
    names = ", ".join(f.replace("references/", "") for f in files if f in opened)
    out.append(f"| {ask[:70]} | {names} | {chars:,} | {orig_size:,} | {chars / orig_size:.0%} |")
out.append(f"| *mean over the rows* | | {round(tot_after / len(rows)):,} | {orig_size:,} | {tot_after / len(rows) / orig_size:.0%} |")
print("\n".join(out))
print()
print("file sizes (chars):", {k.replace("references/", ""): v for k, v in size.items()})
print("new total:", sum(size.values()), "original:", orig_size)
