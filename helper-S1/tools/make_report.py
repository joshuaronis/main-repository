"""Generate the data sections of REPORT.md from the merged results.

Prose sections are written by hand into REPORT_prose.md; this script produces
REPORT_data.md, and `python3 tools/make_report.py --assemble` concatenates the two
into REPORT.md so the numbers in the report are always the numbers in the files.
"""
import csv, glob, json, os, sys
from collections import Counter, defaultdict

R = "results_S1"
L = []
def w(s=""): L.append(s)


DOSE = __import__("re").compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:%|per\s?cent|percent|mg/kg|mg|mL|ml|mEq|\u00b5g|mcg)\b|\b1\s*:\s*\d{3,}\b",
    __import__("re").I)


def redact(t):
    """The dose-figure exception covers the paper card and a claim update's reason.
    REPORT.md is neither, so any figure quoted out of those fields is stripped here."""
    return DOSE.sub("[dose figure omitted]", t or "")


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return default if default is not None else []


def main():
    updates = load(f"{R}/claim_updates.json")
    extras = load(f"{R}/extra_studies.json")
    findings = load(f"{R}/notion_findings.json")
    claims = load(f"{R}/wheal_claims.json")
    summary = load(f"{R}/wheal_summary.json")
    skipped = load(f"{R}/wheal_skipped.json", {})
    status = list(csv.DictReader(open(f"{R}/papers_status.csv", encoding="utf-8"))) \
        if os.path.exists(f"{R}/papers_status.csv") else []
    cards = {os.path.basename(p)[:-5]: load(p, {})
             for p in glob.glob(f"{R}/paper_cards/*.json")}

    base = lambda v: (v or "").split(" (")[0].strip()
    changes = [u for u in updates if base(u.get("old_verdict")) != base(u.get("new_verdict"))]

    # ---------------- 2. Counts ----------------
    w("## 2. Counts")
    w()
    w(f"- **Papers read in full: {len(cards)} of 13.** "
      f"{sum(1 for c in cards.values() if c.get('right_paper'))} confirmed as the right paper.")
    w(f"- **Claim re-judgements written: {len(updates)}**, covering "
      f"{len({u.get('claim_id') for u in updates})} distinct claims. "
      f"**{len(changes)} changed verdict.**")
    k = Counter(u.get("kind", "?") for u in updates)
    w(f"  - by kind: " + ", ".join(f"{v} {kk}" for kk, v in sorted(k.items())))
    w(f"  - still uncertain after the full text: "
      f"{sum(1 for u in updates if u.get('uncertain_after'))}")
    w(f"- **New wheal-page claims extracted and tested: {len(claims)}** "
      f"({', '.join(f'{v} {kk}' for kk, v in sorted(Counter(c['claim_id'][:3] for c in claims).items()))}).")
    vc = Counter(c.get("verdict") or "(untested)" for c in claims)
    w(f"  - verdicts: " + ", ".join(f"**{v} {kk}**" for kk, v in sorted(vc.items(), key=lambda x: -x[1])))
    w(f"  - left uncertain: {sum(1 for c in claims if c.get('uncertain'))}")
    nskip = sum(len(v) for v in skipped.values())
    w(f"  - **{nskip} further claims counted but not written out**, because their subject is a "
      f"dose ceiling, a toxicity threshold, or how to mix, buffer or dilute a solution: " +
      "; ".join(f"{pg} {len(v)}" for pg, v in skipped.items()))
    w(f"- **Extra studies recorded: {len(extras)}**, found through the papers' reference lists "
      f"and discussions.")
    fi = Counter((f.get("importance") or "?").lower() for f in findings)
    w(f"- **Notion findings: {len(findings)}** — " +
      ", ".join(f"**{fi.get(x,0)} {x}**" for x in ("high", "medium", "low")) + ".")
    fk = Counter(f.get("kind", "?") for f in findings)
    w(f"  - by kind: " + ", ".join(f"{v} {kk}" for kk, v in sorted(fk.items(), key=lambda x: -x[1])))
    w()

    # ---------------- per-page table ----------------
    if summary:
        w("### The three wheal pages")
        w()
        w("| Page | as of | extracted | tested | skipped (dose/toxicity/preparation) | refuted | narrowed | confirmed | out-of-scope |")
        w("|---|---|---|---|---|---|---|---|---|")
        for s in summary:
            v = s.get("verdicts", {})
            w(f"| {s['page']} | {s['as_of']} | {s['claims_extracted']} | {s['claims_tested']} | "
              f"{s['claims_skipped_dose_or_toxicity_subject']} | {v.get('refuted',0)} | "
              f"{v.get('narrowed',0)} | {v.get('confirmed',0)} | {v.get('out-of-scope',0)} |")
        w()

    # ---------------- 3. one line per paper ----------------
    w("## 3. What each paper settled")
    w()
    byp = defaultdict(list)
    for u in updates:
        if u.get("paper_id"):
            byp[u["paper_id"]].append(u)
    fbyp = Counter(f.get("paper_id") for f in findings)
    for pid in sorted(cards):
        c = cards[pid]
        st = next((s for s in status if s["paper_id"] == pid), {})
        ch = [u for u in byp.get(pid, []) if base(u.get("old_verdict")) != base(u.get("new_verdict"))]
        w(f"- **{pid} — {c.get('citation','?')}** · own question: "
          f"{st.get('own_question_answered','?')} · {len(byp.get(pid,[]))} claims re-judged"
          f"{', ' + str(len(ch)) + ' changed' if ch else ''} · {fbyp.get(pid,0)} Notion findings.")
    w()

    # ---------------- 4. every verdict change ----------------
    w("## 4. Every verdict change")
    w()
    if not changes:
        w("None.")
    else:
        w("| claim | old | new | source | what decided it |")
        w("|---|---|---|---|---|")
        for u in sorted(changes, key=lambda x: (x.get("claim_id") or "")):
            src = u.get("paper_id") or (f"PMID {u['pmid']}" if u.get("pmid") else "-")
            why = redact((u.get("reason") or "").split(". ")[0][:150])
            w(f"| {u.get('claim_id','?')} | {u.get('old_verdict','?')} | {u.get('new_verdict','?')} | {src} | {why} |")
    w()
    wch = [c for c in claims if c.get("verdict") in ("refuted", "narrowed")]
    w(f"### New wheal-page claims that did not hold as written ({len(wch)} of {len(claims)})")
    w()
    w("| claim | page | verdict | what exists |")
    w("|---|---|---|---|")
    for c in sorted(wch, key=lambda x: x["claim_id"]):
        why = redact((c.get("reason") or "").split(". ")[0][:150])
        w(f"| {c['claim_id']} | {c['page'].replace('-wheals','')} | {c['verdict']} | {why} |")
    w()

    # ---------------- 5. high-importance findings ----------------
    hi = [f for f in findings if (f.get("importance") or "").lower() == "high"]
    w(f"## 5. High-importance Notion findings ({len(hi)})")
    w()
    for f in hi:
        pg = (f.get("page") or "?")
        sec = (f.get("section") or "").strip()
        note = redact((f.get("notes") or f.get("corrected_wording") or "").split(". ")[0][:190])
        w(f"- **{f['finding_id']} · {pg}" + (f" › {sec}" if sec else "") +
          f"** — *{f.get('kind','?')}*, from {f.get('paper_id','?')}. {note}")
    w()


if __name__ == "__main__":
    if "--assemble" in sys.argv:
        prose = open("REPORT_prose.md", encoding="utf-8").read() if os.path.exists("REPORT_prose.md") else ""
        data = open("REPORT_data.md", encoding="utf-8").read()
        head, _, tail = prose.partition("<!--DATA-->")
        open("REPORT.md", "w", encoding="utf-8").write(head + data + tail)
        print("REPORT.md written")
    else:
        main()
        open("REPORT_data.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
        print("\n".join(L[:40]))
        print(f"\n[REPORT_data.md written, {len(L)} lines]")
