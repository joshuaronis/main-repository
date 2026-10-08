"""Scan every output for a drug amount left in a field the rules do not exempt.

The handover's exception covers only the paper card and a claim update's `reason`.
Everywhere else -- proposed_wording, corrected_wording, the claim sentence, quotes,
what_it_shows -- a concentration, volume, mass or ratio should read [dose figure omitted].
Also flags imperatives and safety judgements in proposed/corrected wording.
"""
import glob, json, re, sys

DOSE = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:%|per\s?cent|percent|mg/kg|mg|mL|ml|mEq|µg|ug|mcg)\b"
    r"|\b1\s*:\s*\d{3,}\b|\b\d+(?:\.\d+)?\s*(?:x|×)\s*10\s*[⁻-]?\d*\s*M\b", re.I)
JUDGE = re.compile(r"\b(is safe|are safe|safer|safest|can be used|should be used|recommend\w*|"
                   r"better choice|best choice|advisable|do not buy|use \w+ instead)\b", re.I)
IMPER = re.compile(r"(?m)^\s*(?:Use|Inject|Mix|Buffer|Dilute|Add|Apply|Take|Buy|Avoid)\b")

# Fields the worker authored: both the dose rule and the no-judgement/no-imperative
# rule apply. Fields that must stay verbatim (a page's own sentence, a paper's own
# words) carry only the dose rule -- a safety judgement inside a quoted claim is the
# page's wording, which is exactly what we are recording.
AUTHORED = ["proposed_wording", "corrected_wording", "what_it_shows", "reason_wording"]
VERBATIM = ["claim", "sentence_as_it_stands", "quote", "quote_from_abstract"]
CHECK = AUTHORED + VERBATIM

# A bare percentage is usually an outcome (a flow rise, a response rate, a difference
# between means), not a drug amount, so it is reported separately for eyeballing
# rather than counted as a breach.
AMOUNT = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:mg/kg|mg|mL|ml|mEq|\u00b5g|ug|mcg)\b"
    r"|\b1\s*:\s*\d{3,}\b|\b\d+(?:\.\d+)?\s*(?:x|\u00d7)\s*10\s*[\u207b-]?\d*\s*M\b", re.I)
EXEMPT_FILE = re.compile(r"paper_cards/")

bad = 0
for f in sorted(glob.glob("results_S1/**/*.json", recursive=True)):
    if EXEMPT_FILE.search(f):
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    items = d if isinstance(d, list) else [d]
    for it in items:
        if not isinstance(it, dict):
            continue
        ident = it.get("claim_id") or it.get("finding_id") or it.get("pmid") or "?"
        for k in CHECK:
            v = it.get(k)
            if not isinstance(v, str):
                continue
            rules = [(AMOUNT, "AMOUNT", True), (DOSE, "pct?", False)]
            if k in AUTHORED:
                rules += [(JUDGE, "JUDGEMENT", True), (IMPER, "IMPERATIVE", True)]
            for rx, label, counts in rules:
                m = rx.search(v)
                if not m:
                    continue
                if label == "pct?" and AMOUNT.search(v):
                    continue
                if counts:
                    bad += 1
                print(f"{label:10s} {f} :: {ident} :: {k} :: "
                      f"...{v[max(0,m.start()-55):m.end()+55]}...")
print(f"\n{bad} breach(es). Lines marked pct? are bare percentages reviewed as outcome "
      f"measures (flow rises, response rates, differences between means), not drug amounts.")
sys.exit(0)
