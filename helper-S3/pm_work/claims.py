"""Claim helper. python3 pm_work/claims.py show ID[,ID..]   |   python3 pm_work/claims.py grep REGEX [REGEX2 ...] (all must match, case-insensitive, over claim+elements+wording+reason)"""
import json, re, sys
C = json.load(open("common/claims_all.json", encoding="utf-8"))
by = {c["claim_id"]: c for c in C}
def show(c, full=True):
    print(f"=== {c['claim_id']} | {c['page']} | verdict: {c['verdict']} | uncertain: {c['uncertain']} | evidence PMID {c['evidence_pmid']}")
    print("SECTION:", c["section"])
    print("CLAIM:", c["claim"])
    print("ELEMENTS:", json.dumps(c["elements_said_absent"], ensure_ascii=False))
    if full:
        print("EVIDENCE QUOTE:", c["evidence_quote"])
        print("PROPOSED:", c["proposed_wording"])
        print("REASON:", c["reason"])
        print("REVIEW:", c["review"])
        print("NEEDS FULL TEXT:", json.dumps(c["needs_full_text"], ensure_ascii=False))
        print("QUERIES:", "; ".join(f"[{q.get('count')}] {q['query'][:160]}" for q in c["queries"]))
        for r in c["records_read"]:
            print("  REC", r.get("pmid"), r.get("year"), r.get("first_author"), "|", (r.get("title") or "")[:110], "|", r.get("design"), "|", r.get("matches"))
    print()
if sys.argv[1] == "show":
    for i in sys.argv[2].split(","):
        show(by[i.strip()])
elif sys.argv[1] == "grep":
    pats = [re.compile(p, re.I) for p in sys.argv[2:]]
    n = 0
    for c in C:
        blob = " ".join([c["claim"], json.dumps(c["elements_said_absent"], ensure_ascii=False), c["proposed_wording"], c["reason"], c["section"]])
        if all(p.search(blob) for p in pats):
            n += 1
            print(f"{c['claim_id']} [{c['verdict']}{' ?' if c['uncertain'] else ''}] {c['page'][:40]} :: {c['claim'][:230]}")
    print(f"-- {n} claims")
