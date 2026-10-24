#!/usr/bin/env python3
"""Each reference file's header against its contents: every italic title in its "This file holds" line is a
heading in the file (outside the menu block and code fences), every ### heading of the file outside those is
listed, and the ten "Sections by file:" lines are identical. Usage: check_headers.py OUTDIR"""
import os, re, sys
out = sys.argv[1]
refs = sorted(f for f in os.listdir(os.path.join(out, "references")))
maps = set(); problems = []
for f in refs:
    path = os.path.join(out, "references", f)
    lines = open(path, encoding="utf-8").read().split("\n")
    holds = next(l for l in lines if l.startswith("**This file holds**"))
    holds = holds.replace("**This file holds**", "")
    listed = [re.sub(r"\s+", " ", t).strip() for t in re.findall(r"\*([^*]+)\*", holds)]
    mapline = next(l for l in lines if l.startswith("Sections by file:"))
    maps.add(mapline)
    # headings in the file body, outside fences and outside the menu block
    fence = False; inmenu = False; heads = []; menuheads = []
    for l in lines:
        if l.lstrip().startswith("```"): fence = not fence; continue
        if fence: continue
        if "<!-- menu starts -->" in l: inmenu = True
        if "<!-- menu ends -->" in l: inmenu = False
        m = re.match(r"^#{3,4} (.*)$", l)
        if m:
            (menuheads if inmenu else heads).append(re.sub(r"\s+", " ", m.group(1)).strip())
    for t in listed:
        if not any(h == t or h.startswith(t) for h in heads + menuheads):
            # titles that are not headings: a range marker or a described item
            problems.append(f"{f}: listed title not a heading in the file: *{t}*")
    for h in heads:
        if not any(h == t or h.startswith(t) for t in listed):
            problems.append(f"{f}: heading not listed in the header: {h[:80]}")
    print(f"{f}: {len(listed)} titles listed, {len(heads)} headings in the body")
print("map lines identical across files:", len(maps) == 1)
print("PROBLEMS:", len(problems))
for p in problems: print("  -", p)
