#!/usr/bin/env python3
"""Release the split skill into the replica of the notes folder, fill the notes' placeholders, check, and
assemble the delivery.

Usage: finalize.py SCRATCHPAD [--dry-run]
  SCRATCHPAD  the session scratchpad holding hr_job/, hr_notes/, replica/, skill_updates/

Steps: (1) release.py on hr_job/out/health-record from replica/Skill Updates (stamps, zips, prints md5s);
(2) fill <STAMP>, <STAMP-NAME>, <SKILL-MD5> and refresh the md5 list, the sizes and the offsets in the five
notes; (3) verify_notes.py (old notes vs new) and check_folder.py on the replica; (4) write delivery/ with
the notes zip, the skill zip and the folder-advice prompt. Python 3, standard library only.
"""
import os, re, shutil, subprocess, sys, zipfile

S = sys.argv[1]
DRY = "--dry-run" in sys.argv
SKIP = "--skip-release" in sys.argv   # the newest release in Releases/ was already cut; reuse it
JOB = os.path.join(S, "hr_job")
OUT = os.path.join(JOB, "out", "health-record")
REPL = os.path.join(S, "replica", "Skill Updates")
NOTES = os.path.join(REPL, "Skills", "health-record")
OLDNOTES = os.path.join(S, "hr_notes", "health-record copy")
FILES = ["SKILL.md"] + ["references/" + f for f in sorted(os.listdir(os.path.join(OUT, "references")))]

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)}\n{r.stdout}{r.stderr}")
    return r

# ---- 1. release ---------------------------------------------------------------
if SKIP:
    import hashlib
    rd = os.path.join(NOTES, "Releases")
    newest = sorted(z for z in os.listdir(rd) if re.fullmatch(r"health-record-\d{4}-\d{2}-\d{2}-\d{4}\.zip", z))[-1]
    stamp_name = newest[:-4]; stamp = stamp_name[len("health-record-"):]
    md5 = {}
    with zipfile.ZipFile(os.path.join(rd, newest)) as zf:
        for n in zf.namelist():
            if not n.endswith("/"):
                md5[n.split("/", 1)[1]] = hashlib.md5(zf.read(n)).hexdigest()
    print("reusing", newest)
else:
    r = run([sys.executable, "-I", "release.py", OUT] + (["--dry-run"] if DRY else []), REPL)
    if r.returncode != 0:
        sys.exit("release.py failed")
    m = re.search(r"(?:wrote|would write) Skills/health-record/Releases/(health-record-(\d{4}-\d{2}-\d{2}-\d{4}))\.zip", r.stdout)
    stamp_name, stamp = m.group(1), m.group(2)
    md5 = dict(re.findall(r"^  (\S+)  ([0-9a-f]{32})$", r.stdout, re.M))
assert set(md5) == set(FILES), (set(md5) ^ set(FILES))
print("stamp:", stamp, "| SKILL.md md5:", md5["SKILL.md"])
if DRY:
    sys.exit(0)

# ---- 2. the notes -------------------------------------------------------------
# Measure the RELEASED files, not the build: release.py stamps the name and the title of SKILL.md
# (two lines, 32 characters more), and the notes quote the sizes and offsets of what Josh uploads.
with zipfile.ZipFile(os.path.join(NOTES, "Releases", stamp_name + ".zip")) as zf:
    released = {n.split("/", 1)[1]: zf.read(n).decode("utf-8") for n in zf.namelist() if not n.endswith("/")}
assert set(released) == set(FILES), (set(released) ^ set(FILES))
for f in FILES:   # the release differs from the build only in SKILL.md's name line and title line
    a = open(os.path.join(OUT, f), encoding="utf-8").read().split("\n"); b = released[f].split("\n")
    differing = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y] + ([] if len(a) == len(b) else ["length"])
    assert differing == ([2, 6] if f == "SKILL.md" else []), (f, differing)
sizes = {f: len(released[f]) for f in FILES}
total = sum(sizes.values())
skill = released["SKILL.md"]
i = skill.find("**Some further rules override everything else in this document"); end_rules = skill.find("\n", i)
end_block = skill.find("## What you are probably being asked")
j = skill.find("| The ask |"); end_table = skill.find("\n\n", j)
md5_list = "; ".join(f"`{f}` `{md5[f]}`" for f in FILES)
loads = open(os.path.join(JOB, "route_loads.md"), encoding="utf-8").read()
mean = re.search(r"\*mean over the rows\* \| \| [\d,]+ \| [\d,]+ \| (\d+)%", loads).group(1)

def edit(name, pairs):
    p = os.path.join(NOTES, name); t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        if isinstance(old, re.Pattern):
            t, n = old.subn(new, t)
        else:
            n = t.count(old); t = t.replace(old, new)
        if isinstance(old, re.Pattern) or old not in ("<STAMP-NAME>", "<STAMP>", "<SKILL-MD5>"):
            assert n >= 1, (name, old if isinstance(old, str) else old.pattern)
    open(p, "w", encoding="utf-8").write(t)

common = [("<STAMP-NAME>", stamp_name), ("<STAMP>", stamp), ("<SKILL-MD5>", md5["SKILL.md"])]
edit("Changelog.md", common + [(re.compile(r"→ ten files: .*?\. 441,536 → [\d,]+ characters in all"),
                                f"→ ten files: {md5_list}. 441,536 → {total:,} characters in all")])
about_pairs = common + [(re.compile(r"ten files, [\d,]+ characters in all"), f"ten files, {total:,} characters in all"),
                        (re.compile(r"end at about [\d,]+ characters, the cross-task rules at about [\d,]+"),
                         f"end at about {end_table:,} characters, the cross-task rules at about {end_rules:,}"),
                        (re.compile(r"on average \d+% of the one-file version"), f"on average {mean}% of the one-file version")]
for f in FILES:
    about_pairs.append((re.compile(r"(\| `" + re.escape(f) + r"` \| )[\d,]+( \|)"), lambda mm, f=f: f"{mm.group(1)}{sizes[f]:,}{mm.group(2)}"))
edit("About.md", about_pairs)
edit("Open items.md", common + [(re.compile(r"The cross-task rules end at [\d,]+ characters"), f"The cross-task rules end at {end_rules:,} characters"),
                                (re.compile(r"ends at about [\d,]+ and the routing table at about [\d,]+"), f"ends at about {end_block:,} and the routing table at about {end_table:,}")])
edit("Lessons.md", common + [(re.compile(r"end at [\d,]+; anything added"), f"end at {end_rules:,}; anything added"),
                             (re.compile(r"about [\d,]+ characters in ten files"), f"about {total:,} characters in ten files")])
edit("Decisions and do-not-fix.md", common)
edit("Judged list.md", common)
for name in os.listdir(NOTES):
    if name.endswith(".md"):
        t = open(os.path.join(NOTES, name), encoding="utf-8").read()
        assert "<STAMP" not in t and "<SKILL-MD5>" not in t, (name, "placeholder left")

# ---- 3. checks ----------------------------------------------------------------
if run([sys.executable, "-I", "verify_notes.py", OLDNOTES, NOTES], REPL).returncode != 0:
    sys.exit("verify_notes.py failed")
if run([sys.executable, "-I", "check_folder.py"], REPL).returncode != 0:
    sys.exit("check_folder.py failed")

# ---- 4. delivery --------------------------------------------------------------
D = os.path.join(JOB, "delivery")
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
notes_zip = os.path.join(D, f"health-record-notes-{stamp}.zip")
with zipfile.ZipFile(notes_zip, "w", zipfile.ZIP_DEFLATED) as zf:
    for name in sorted(os.listdir(NOTES)):
        if name.endswith(".md"):
            zf.write(os.path.join(NOTES, name), f"Skills/health-record/{name}")
    zf.write(os.path.join(NOTES, "Releases", stamp_name + ".zip"), f"Skills/health-record/Releases/{stamp_name}.zip")
shutil.copy(os.path.join(NOTES, "Releases", stamp_name + ".zip"), os.path.join(D, stamp_name + ".zip"))
shutil.copy(os.path.join(JOB, "folder_advice_prompt.md"), os.path.join(D, "folder-advice-prompt.md"))
fd = os.path.join(REPL, "for deletion")
moved = [os.path.join(dp, f) for dp, _, fs in os.walk(fd) for f in fs] if os.path.isdir(fd) else []
print("delivery:", sorted(os.listdir(D)))
print("moved into for deletion/ by release.py:", [os.path.relpath(p, REPL) for p in moved])
print("DONE", stamp_name)
