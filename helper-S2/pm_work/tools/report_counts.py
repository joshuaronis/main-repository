"""Counts for REPORT.md, computed from the merged results in results_S2/ (run from helper-S2/).
  python3 pm_work/tools/report_counts.py"""
import collections, csv, json

cu = json.load(open("results_S2/claim_updates.json", encoding="utf-8"))
es = json.load(open("results_S2/extra_studies.json", encoding="utf-8"))
nf = json.load(open("results_S2/notion_findings.json", encoding="utf-8"))
st = list(csv.DictReader(open("results_S2/papers_status.csv", encoding="utf-8")))
print(f"papers merged: {len(st)}")
print(f"claim updates: {len(cu)} entries on {len({c['claim_id'] for c in cu})} distinct claims")
print("  by kind:", dict(collections.Counter(c["kind"] for c in cu)))
ch = [c for c in cu if c["old_verdict"] != c["new_verdict"]]
print(f"  verdict changes: {len(ch)} entries on {len({c['claim_id'] for c in ch})} claims")
print("  changes from -> to:", dict(collections.Counter(f"{c['old_verdict']} -> {c['new_verdict']}" for c in ch)))
for c in ch:
    src = c["paper_id"] or f"PMID {c['pmid']}"
    print(f"    {c['claim_id']} {c['old_verdict']} -> {c['new_verdict']} ({c['kind']}; {src})")
print("  uncertain_after true:", [c["claim_id"] for c in cu if c.get("uncertain_after")])
print(f"extra studies: {len(es)} ({len({e['pmid'] for e in es})} distinct PMIDs)")
print(f"Notion findings: {len(nf)}")
print("  by kind:", dict(collections.Counter(f["kind"] for f in nf)))
print("  by importance:", dict(collections.Counter(f["importance"] for f in nf)))
print("  by page:", dict(collections.Counter(f["page"] for f in nf)))
for f in nf:
    if f["importance"] == "high":
        print(f"    HIGH {f['finding_id']} | {f['page']} | {f['kind']} | {f['sentence_as_it_stands'][:120]}")
