#!/usr/bin/env python3
"""Check a split of the health-record skill against the original.

Usage: check_split.py FROZEN OUTDIR MANIFEST

1. Coverage: every original line of 25+ characters occurs in exactly one new file, byte for byte,
   except the lines an edit in the manifest changed; every new-file line of 25+ characters that
   matches no original line is printed (these must all be headers, the files block, headings or edits).
2. Reassembly: the moved pieces, taken from the NEW files in original order, diffed against the
   original; every hunk is printed (expected: only the manifest's edits).
3. Cross-references: every `§N, *Title*` (and `§N *Title*` in a table) over all files resolves to a
   heading or bold entry of section N in SOME file (xref_check's rule), and the file holding it is
   named in SKILL.md's table of files for §N. Bare `§N` pointers: N has a row in the table of files.
4. Positional pointers: every `(*Title*, above|below)` resolves inside its own file; the bare
   above/below/this-section phrases are counted per file (reviewed by hand in positional.txt).
5. Reachability: every reference file's path is in SKILL.md; every file carries the one-line map
   naming every file; code fences balance in every file; the lines inside fences are unchanged.
6. Frontmatter: name, description length; no other skill named.
Exit 1 on any problem. Python 3, standard library only.
"""
import difflib, json, os, re, sys

FROZEN, OUTDIR, MANIFEST = sys.argv[1:4]
orig = open(FROZEN, encoding="utf-8").read().split("\n")
if orig[-1] == "":
    orig = orig[:-1]
man = json.load(open(MANIFEST, encoding="utf-8"))
files = {}
for path in man["files"]:
    t = open(os.path.join(OUTDIR, path), encoding="utf-8").read()
    files[path] = t[:-1].split("\n") if t.endswith("\n") else t.split("\n")
problems = []

# ---- 1. coverage -------------------------------------------------------------
edited_old = set()
for e in man["edits"]:
    for ln in orig:
        if e["old"] in ln:
            edited_old.add(ln)
index = {}
for path, lines in files.items():
    for i, ln in enumerate(lines, 1):
        index.setdefault(ln, []).append((path, i))
print("== 1. coverage ==")
missing, multi = [], []
for i, ln in enumerate(orig, 1):
    if len(ln) < 25:
        continue
    hits = index.get(ln, [])
    if ln in edited_old:
        if hits:
            problems.append(f"edited original line {i} still present verbatim at {hits}")
        continue
    if not hits:
        missing.append(i)
    elif len(hits) > 1:
        multi.append((i, hits))
print(f"original lines of 25+ chars: {sum(1 for l in orig if len(l) >= 25)}; edited: {len(edited_old)}; missing: {missing}; duplicated: {multi}")
if missing or multi:
    problems.append(f"coverage: missing {missing}, duplicated {multi}")
orig_set = set(orig)
print("-- new-file lines of 25+ chars that match no original line (must be headers, the files block, new headings or edits):")
new_only = 0
for path, lines in files.items():
    for i, ln in enumerate(lines, 1):
        if len(ln) >= 25 and ln not in orig_set:
            new_only += 1
            print(f"  {path}:{i}: {ln[:140]}{'…' if len(ln) > 140 else ''}")
print(f"-- {new_only} such lines")
# short lines: counts
for key in ("", "---"):
    o = sum(1 for l in orig if l == key); n = sum(sum(1 for l in ls if l == key) for ls in files.values())
    print(f"-- lines equal to {key!r}: original {o}, new {n}")

# ---- 2. reassembly -----------------------------------------------------------
print("\n== 2. reassembly diff (moved pieces from the new files, in original order) ==")
pieces = []
for path, plist in man["files"].items():
    for p in plist:
        if p["kind"] == "orig":
            pieces.append((p["orig_start"], p["orig_end"], path, p["new_start"], p["new_end"]))
pieces.sort()
covered = []
reassembled = []
for a, b, path, na, nb in pieces:
    covered.append((a, b))
    reassembled += files[path][na - 1:nb]
# every original line covered exactly once by the pieces
cov = [0] * (len(orig) + 1)
for a, b in covered:
    for k in range(a, b + 1):
        cov[k] += 1
bad = [k for k in range(1, len(orig) + 1) if cov[k] != 1]
print(f"pieces: {len(pieces)}; original lines covered other than once: {bad}")
if bad:
    problems.append(f"pieces do not cover the original exactly once: {bad}")
hunks = list(difflib.unified_diff(orig, reassembled, "original", "reassembled", n=0, lineterm=""))
diffs = [h for h in hunks if h.startswith(("-", "+")) and not h.startswith(("---", "+++"))]
print(f"diff lines: {len(diffs)} (each edit gives one - and one +)")
for h in hunks:
    if h.startswith(("@@", "-", "+")) and not h.startswith(("---", "+++")):
        print("  " + h[:200] + ("…" if len(h) > 200 else ""))
expected_minus = len(man["edits"])
if len([d for d in diffs if d.startswith("-")]) != expected_minus:
    problems.append(f"reassembly: {len([d for d in diffs if d.startswith('-')])} changed lines, {expected_minus} edits expected")

# ---- 3. cross-references -----------------------------------------------------
print("\n== 3. cross-references ==")
def norm(s): return re.sub(r"\s+", " ", s).strip()
heads, bolds, where = {}, {}, {}   # sec -> set of titles; where[(sec,title)] -> file
for path, lines in files.items():
    sec, fence = None, False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence; continue
        if fence:
            continue
        m = re.match(r"^## (?:§(\d+)\b|(\d+)\. )", line)
        if m:
            sec = m.group(1) or m.group(2)
            heads.setdefault(sec, set()); bolds.setdefault(sec, set()); where.setdefault(sec, set()).add(path)
            continue
        if re.match(r"^## ", line):
            sec = None; continue
        if sec is None:
            continue
        m = re.match(r"^#{3,4} (.*)$", line)
        if m:
            heads[sec].add((norm(m.group(1)), path)); continue
        for b in re.findall(r"\*\*(.+?)\*\*", line):
            bolds[sec].add((re.sub(r"^\d+\. ", "", norm(b)), path))
# the table of files in SKILL.md: path -> set of section numbers
skill = "\n".join(files["SKILL.md"])
table_map = {}
for row in re.findall(r"^\| `([^`]+)` \| (.+) \|$", skill, re.M):
    secs = set(re.findall(r"§(\d+)", row[1]))
    table_map[row[0]] = secs
print("table of files:", {k: sorted(v, key=int) for k, v in table_map.items()})
def files_for_section(sec):
    return {p for p, s in table_map.items() if sec in s}
unresolved, misfiled, bare_unmapped = [], [], []
ptr_count = 0
for path, lines in files.items():
    text = "\n".join(lines)
    for m in re.finditer(r"§(\d+)(?:\.\d+)?(,?) \*([^*]+)\*", text):
        s, title = m.group(1), norm(m.group(3))
        if not m.group(2) and title[:1].islower():
            continue
        ptr_count += 1
        ln = text.count("\n", 0, m.start()) + 1
        if s not in heads:
            unresolved.append((path, ln, m.group(0), "no such section")); continue
        tf = {p for (h, p) in heads[s] if h == title or h.startswith(title)} | {p for (b, p) in bolds[s] if b.startswith(title)}
        if not tf:
            unresolved.append((path, ln, norm(m.group(0)), "title not found")); continue
        if not (tf & files_for_section(s)):
            misfiled.append((path, ln, norm(m.group(0)), sorted(tf)))
    for m in re.finditer(r"§(\d+)", text):
        if m.group(1) not in heads:
            bare_unmapped.append((path, text.count("\n", 0, m.start()) + 1, m.group(0)))
        elif not files_for_section(m.group(1)):
            bare_unmapped.append((path, text.count("\n", 0, m.start()) + 1, m.group(0) + " (section not in the table of files)"))
print(f"titled pointers checked: {ptr_count}; unresolved: {unresolved}; target file not named in the table of files for that section: {misfiled}")
print(f"bare §N with no section or no table row: {sorted(set(bare_unmapped))[:20]}")
print("sections and their files:", {k: sorted(v) for k, v in sorted(where.items(), key=lambda kv: int(kv[0]))})
if unresolved or misfiled or bare_unmapped:
    problems.append("cross-references: see section 3")

# ---- 4. positional pointers -------------------------------------------------
print("\n== 4. positional pointers ==")
pos_bad = []
for path, lines in files.items():
    text = "\n".join(lines)
    titles = set()
    fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence; continue
        if fence: continue
        m = re.match(r"^#{2,4} (.*)$", line)
        if m: titles.add(norm(m.group(1)))
        for b in re.findall(r"\*\*(.+?)\*\*", line):
            titles.add(re.sub(r"^\d+\. ", "", norm(b)))
    for m in re.finditer(r"\*([^*]+)\*,? (above|below)\b", text):
        title = norm(m.group(1))
        ok = any(t == title or t.startswith(title) for t in titles)
        if not ok:
            pos_bad.append((path, text.count("\n", 0, m.start()) + 1, norm(m.group(0))[:80]))
    counts = {w: len(re.findall(w, text)) for w in (r"\babove\b", r"\bbelow\b", r"this section", r"end of this section", r"further down")}
    print(f"  {path}: {counts}")
print(f"titled positional pointers whose title is not in the same file: {pos_bad}")
if pos_bad:
    problems.append(f"positional: {pos_bad}")

# ---- 5. reachability, maps, fences ------------------------------------------
print("\n== 5. reachability and fences ==")
refs = [p for p in files if p != "SKILL.md"]
for p in refs:
    if p not in skill:
        problems.append(f"{p} is not named in SKILL.md")
    for q in files:
        if q not in "\n".join(files[p]):
            problems.append(f"{p} does not name {q} in its map")
print("every reference file named in SKILL.md:", all(p in skill for p in refs))
print("every file names every file:", all(q in "\n".join(files[p]) for p in refs for q in files))
def fenced_lines(lines):
    out, fence = [], False
    for l in lines:
        if l.lstrip().startswith("```"):
            fence = not fence; out.append(l); continue
        if fence: out.append(l)
    return out, fence
of, _ = fenced_lines(orig)
nf = []
for p, ls in files.items():
    f, open_ = fenced_lines(ls)
    if open_:
        problems.append(f"{p}: an unclosed code fence")
    nf += f
print(f"fenced lines: original {len(of)}, new {len(nf)}, identical as a multiset: {sorted(of) == sorted(nf)}")
if sorted(of) != sorted(nf):
    problems.append("fenced content differs")
# tables: every table row of the original is in exactly one file (covered by 1.); count rows
print("table rows: original", sum(1 for l in orig if l.startswith("|")), "new", sum(1 for ls in files.values() for l in ls if l.startswith("|")))

# ---- 6. frontmatter -----------------------------------------------------------
print("\n== 6. frontmatter and names ==")
fm = re.match(r"---\n(.*?)\n---\n", skill, re.S)
name = re.search(r"(?m)^name:\s*(.*)$", fm.group(1)).group(1).strip()
desc = re.search(r"(?m)^description:\s*(.*)$", fm.group(1)).group(1).strip().strip('"')
print(f"name: {name}; description: {len(desc)} chars (limit 1,024)")
if len(desc) > 1024:
    problems.append("description over 1,024")
for p, ls in files.items():
    for i, l in enumerate(ls, 1):
        if re.search(r"health-history|health-record-edits|cgpt-|ai-best-practices", l):
            problems.append(f"{p}:{i} names another skill: {l[:100]}")
print("other skills named:", [x for x in problems if "another skill" in x] or "none")
sizes = {p: (len("\n".join(ls)) + 1, len(("\n".join(ls) + "\n").encode("utf-8"))) for p, ls in files.items()}
print("\nsizes (chars, bytes):", sizes)
print("total chars:", sum(v[0] for v in sizes.values()), "original:", len("\n".join(orig)) + 1)
print("\nPROBLEMS:", len(problems))
for p in problems:
    print("  -", p)
sys.exit(1 if problems else 0)
