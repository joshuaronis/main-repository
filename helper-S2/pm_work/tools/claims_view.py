"""Prints claims from common/claims_all.json with every dose-like figure masked as [dose figure omitted], so claims can be
screened without bringing amounts, concentrations or ceilings into the conversation.
  python3 pm_work/tools/claims_view.py grep '<regex>' [--fields claim,elements,verdict,reason,proposed,review,evidence]
      lists every claim whose text (claim, elements, reason, proposed wording, review, evidence quote) matches the regex
  python3 pm_work/tools/claims_view.py show C046 D013 ...   prints those claims in full (masked)
Default fields for grep: claim id, page, verdict and the claim sentence (first 300 characters)."""
import json, re, sys

UNIT = (r"(?:mg|g|kg|mcg|µg|μg|ug|ng|pg|microg|micrograms?|milligrams?|grams?|nanograms?|mL|ml|cc|l|L|µl|μl|µL|μL|millilit(?:re|er)s?|microlit(?:re|er)s?|%|percent|per\s*cent|mmol|µmol|μmol|mM|µM|μM|nM|IU|U|units?|"
        r"cartridges?|carpules?|ampoules?|ampules?|vials?|injections?|sites?|punctures?|deposits?|wheals?|blebs?|"
        r"points?|times|doses?)")
DOSE = re.compile(r"(?<![\w.])\d[\d.,]*\s*(?:–|-|to)?\s*\d*[\d.,]*\s*" + UNIT + r"(?![\w])|\b1\s*:\s*\d{2,3}[ ,.]?\d{3}\b|"
                  r"\b\d[\d.,]*\s*(?:mg|µg|μg|mcg|microg)\s*/\s*(?:kg|mL|ml)\b", re.I)


def mask(s):
    return DOSE.sub("[dose figure omitted]", s or "")


def text(c):
    return " ".join([c.get("claim", ""), json.dumps(c.get("elements_said_absent", {}), ensure_ascii=False),
                     c.get("reason", ""), c.get("proposed_wording", ""), c.get("review", ""), c.get("evidence_quote", "")])


def main():
    cl = json.load(open("common/claims_all.json", encoding="utf-8"))
    if sys.argv[1] == "grep":
        rx = re.compile(sys.argv[2], re.I)
        hits = [c for c in cl if rx.search(text(c))]
        for c in hits:
            print(f"{c['claim_id']} | {c['verdict']}{' (uncertain)' if c.get('uncertain') else ''} | {c['page'][:45]} | "
                  f"{mask(c['claim'])[:300]}")
        print(f"{len(hits)} of {len(cl)} claims match")
    elif sys.argv[1] == "show":
        want = set(sys.argv[2:])
        for c in cl:
            if c["claim_id"] in want:
                print("=" * 80)
                print(f"{c['claim_id']} | {c['page']} | {c['section']}")
                print("CLAIM:", mask(c["claim"]))
                print("ELEMENTS:", mask(json.dumps(c["elements_said_absent"], ensure_ascii=False)))
                print(f"VERDICT: {c['verdict']} | uncertain={c.get('uncertain')} | evidence PMID {c.get('evidence_pmid')}")
                print("EVIDENCE QUOTE:", mask(c.get("evidence_quote")))
                print("PROPOSED:", mask(c.get("proposed_wording")))
                print("REASON:", mask(c.get("reason")))
                print("REVIEW:", mask(c.get("review")))
                print("NEEDS FULL TEXT:", mask(json.dumps(c.get("needs_full_text"), ensure_ascii=False)))
                rr = c.get("records_read") or []
                for r in rr:
                    print("  RECORD:", mask(json.dumps(r, ensure_ascii=False))[:400])
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
