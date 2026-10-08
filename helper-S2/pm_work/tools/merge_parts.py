"""Rebuilds results_S2/ lists from the per-paper parts in pm_work/parts/<paper_id>/, in the hand-over's paper order,
for the papers listed as reviewed in pm_work/parts/merged.txt (one paper id per line).
  python3 pm_work/tools/merge_parts.py
Notion finding ids are renumbered S2-F001, S2-F002, … in that order; the map from each provisional id is written to
pm_work/parts/finding_id_map.json. papers_status.csv is rebuilt from each part's status.json."""
import csv, json, os

ORDER = ["S-686-37", "S-686-36", "S-686-42", "S-686-47", "S-686-44", "S-686-38", "S-686-27", "S-686-23", "S-686-07",
         "S-686-48", "S-686-43", "S-686-05", "S-686-18", "S-686-01", "S-686-12"]
P = "pm_work/parts"
done = [l.strip() for l in open(f"{P}/merged.txt")] if os.path.exists(f"{P}/merged.txt") else []
cu, es, nf, st, idmap = [], [], [], [], {}
for pid in ORDER:
    if pid not in done:
        continue
    d = f"{P}/{pid}"
    load = lambda n: json.load(open(f"{d}/{n}.json", encoding="utf-8")) if os.path.exists(f"{d}/{n}.json") else []
    cu += load("claim_updates")
    es += load("extra_studies")
    for f in load("notion_findings"):
        new = f"S2-F{len(nf) + 1:03d}"
        idmap[f"{pid}:{f.get('finding_id')}"] = new
        f = dict(f, finding_id=new)
        nf.append(f)
    if os.path.exists(f"{d}/status.json"):
        st.append(json.load(open(f"{d}/status.json", encoding="utf-8")))
# the same Notion sentence flagged from two papers: cross-reference the findings in their notes
import re as _re
def _norm(t):
    return _re.sub(r"[^a-z0-9]", "", _re.sub(r"\[[^\]]*\]", "", (t or "").lower()))
for a in nf:
    for b in nf:
        if a is not b and a["page_url"].split("?")[0] == b["page_url"].split("?")[0] \
                and _norm(a["sentence_as_it_stands"]) == _norm(b["sentence_as_it_stands"]):
            src = b.get("paper_id") or f"PMID {b.get('pmid')}"
            a["notes"] = (a.get("notes") or "") + f" Same sentence also flagged as {b['finding_id']} (from {src})."
os.makedirs("results_S2", exist_ok=True)
for name, items in (("claim_updates", cu), ("extra_studies", es), ("notion_findings", nf)):
    json.dump(items, open(f"results_S2/{name}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(idmap, open(f"{P}/finding_id_map.json", "w"), indent=1)
cols = ["paper_id", "right_paper", "text_ok", "own_question_answered", "claims_rejudged", "notion_findings", "notes"]
with open("results_S2/papers_status.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for s in st:
        w.writerow({k: s.get(k, "") for k in cols})
print(f"merged {len(done)} papers: {len(cu)} claim updates, {len(es)} extra studies, {len(nf)} Notion findings, "
      f"{len(st)} status rows")
