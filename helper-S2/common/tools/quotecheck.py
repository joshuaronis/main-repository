"""Checks that every quote in a results file appears in its source text.
usage: python3 tools/quotecheck.py <results.json> <texts_dir> [pm_work_dir]
Each item needs "quote" and either "paper_id" (its text is <texts_dir>/<paper_id>.txt) or "pmid" (the abstract cached by
tools/pm.py in <pm_work_dir>/cache/a_<pmid>.json). Spacing, case and punctuation are ignored; "…" or "..." split a quote into
parts that must each be found. Prints every quote not found."""
import json, os, re, sys

def n(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())

res, tdir = sys.argv[1], sys.argv[2]
pmw = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.getcwd(), "pm_work")
items = json.load(open(res, encoding="utf-8"))
bad = ok = 0
for i, it in enumerate(items):
    q = it.get("quote") or it.get("evidence_quote") or ""
    if not q:
        continue
    src = ""
    if it.get("paper_id") and os.path.exists(os.path.join(tdir, it["paper_id"] + ".txt")):
        src = open(os.path.join(tdir, it["paper_id"] + ".txt"), encoding="utf-8", errors="replace").read()
    elif it.get("pmid") and os.path.exists(os.path.join(pmw, "cache", f"a_{it['pmid']}.json")):
        a = json.load(open(os.path.join(pmw, "cache", f"a_{it['pmid']}.json")))
        src = a["title"] + " " + a["abstract"]
    body = n(src)
    parts = [n(p) for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q) if len(n(p)) > 10]
    if body and parts and all(p in body for p in parts):
        ok += 1
    else:
        bad += 1
        print(f"NOT FOUND #{i} ({it.get('paper_id') or it.get('pmid') or 'no source'}): {q[:160]}")
print(f"{ok} quotes found, {bad} not found")
