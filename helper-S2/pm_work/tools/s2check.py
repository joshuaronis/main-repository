"""Checks one paper's results (or the merged results) before they are merged or handed back.
usage (from helper-S2/):  python3 pm_work/tools/s2check.py S-686-37      -> checks pm_work/parts/S-686-37/ and its card
                          python3 pm_work/tools/s2check.py merged         -> checks results_S2/
Checks: every JSON file loads and has the fields the hand-over's schema names; verdicts and kinds use the allowed values;
quotes are found in their sources (as common/tools/quotecheck.py does); and it flags, for a person to look at, text that
may carry a dose figure (a number with a unit of amount, concentration, volume, count of injections or frequency, or a
dilution ratio) or advice wording (safe, recommended, should, ...) in the fields where neither may appear."""
import json, os, re, subprocess, sys

CU = ["claim_id", "paper_id", "pmid", "kind", "old_verdict", "new_verdict", "uncertain_after", "quote", "page",
      "proposed_wording", "reason"]
ES = ["pmid", "citation", "found_in_paper", "bears_on_claim_ids", "what_it_shows", "quote_from_abstract"]
NF = ["finding_id", "paper_id", "page", "page_url", "page_version", "section", "sentence_as_it_stands", "kind", "quote",
      "page_in_paper", "corrected_wording", "importance", "notes"]
CARD = ["paper_id", "citation", "pmid", "doi", "right_paper", "text_quality", "design", "population", "n", "setting",
        "intervention", "comparator", "route", "duration", "outcomes", "key_results", "author_limitations",
        "funding_conflicts", "studies_it_cites_that_matter"]
VERDICTS = {"confirmed", "narrowed", "refuted", "out-of-scope"}
KINDS = {"own-question", "other-claim", "extra-study"}
NKINDS = {"wrong-figure", "wrong-design", "overstated", "understated", "now-verified", "outdated", "citation-error",
          "open-question-answered", "ranking-reweigh"}
UNIT = (r"(?:mg|g|kg|mcg|µg|μg|ug|ng|pg|microg|micrograms?|milligrams?|grams?|nanograms?|mL|ml|cc|l|L|µl|μl|µL|μL|millilit(?:re|er)s?|microlit(?:re|er)s?|%|percent|per\s*cent|mmol|µmol|μmol|mM|µM|μM|nM|IU|U|units?|"
        r"cartridges?|carpules?|ampoules?|ampules?|vials?|injections?|sites?|punctures?|deposits?|wheals?|blebs?|"
        r"points?|times|sessions?|doses?|applications?|patches?|tubes?)")
DOSE = re.compile(r"(?<![\w.])\d[\d.,]*\s*(?:–|-|to)?\s*\d*[\d.,]*\s*" + UNIT + r"(?![\w])|\b1\s*:\s*\d{2,3}[ ,.]?\d{3}\b|"
                  r"mg\s*/\s*kg|µg\s*/\s*kg|μg\s*/\s*kg|µg\s*/\s*mL|μg\s*/\s*mL|ng\s*/\s*mL|mg\s*/\s*mL", re.I)
ADVICE = re.compile(r"\b(safe|safer|safely|safety margin|can be used|recommend\w*|should|must|avoid|better choice|"
                    r"preferred|prefer|use it|try|consider)\b", re.I)


def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:  # noqa
        print(f"  !! {p}: does not load: {e}")
        return None


def flag(where, field, text, advice=False):
    if not isinstance(text, str) or not text:
        return
    for m in DOSE.finditer(text):
        s = text[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        print(f"  ?? dose-like figure in {where} {field}: …{s}…")
    if advice:
        for m in ADVICE.finditer(text):
            s = text[max(0, m.start() - 60):m.end() + 40].replace("\n", " ")
            print(f"  ?? advice wording in {where} {field}: …{s}…")


def keys(items, req, name):
    for i, it in enumerate(items):
        miss = [k for k in req if k not in it]
        if miss:
            print(f"  !! {name} #{i}: missing {miss}")


def main():
    tgt = sys.argv[1]
    if tgt == "merged":
        base, cards = "results_S2", sorted(os.listdir("results_S2/paper_cards"))
        files = {k: f"results_S2/{k}.json" for k in ("claim_updates", "extra_studies", "notion_findings")}
        cards = [f"results_S2/paper_cards/{c}" for c in cards if c.endswith(".json")]
    else:
        base = f"pm_work/parts/{tgt}"
        files = {k: f"{base}/{k}.json" for k in ("claim_updates", "extra_studies", "notion_findings")}
        cards = [f"results_S2/paper_cards/{tgt}.json"]
    for c in cards:
        card = load(c)
        if card is None:
            continue
        print(f"card {c}")
        keys([card], CARD, "card")
        for k, v in card.items():
            if isinstance(v, str):
                flag("card", k, v)
            elif isinstance(v, list):
                for j, x in enumerate(v):
                    for kk, vv in (x.items() if isinstance(x, dict) else []):
                        flag("card", f"{k}[{j}].{kk}", vv)
    for name, p in files.items():
        if not os.path.exists(p):
            print(f"{name}: no file ({p})")
            continue
        items = load(p)
        if items is None:
            continue
        if not isinstance(items, list):
            print(f"  !! {p} is not a list")
            continue
        print(f"{name}: {len(items)} items")
        if name == "claim_updates":
            keys(items, CU, name)
            for it in items:
                w = f"{it.get('claim_id')}/{it.get('kind')}"
                if it.get("new_verdict") not in VERDICTS or it.get("old_verdict") not in VERDICTS:
                    print(f"  !! {w}: verdict not one of {sorted(VERDICTS)}: {it.get('old_verdict')} -> {it.get('new_verdict')}")
                if it.get("kind") not in KINDS:
                    print(f"  !! {w}: kind {it.get('kind')}")
                flag(w, "quote", it.get("quote"))
                flag(w, "proposed_wording", it.get("proposed_wording"), advice=True)
                flag(w, "reason", it.get("reason"))
        elif name == "extra_studies":
            keys(items, ES, name)
            for it in items:
                flag(it.get("pmid"), "what_it_shows", it.get("what_it_shows"))
                flag(it.get("pmid"), "quote_from_abstract", it.get("quote_from_abstract"))
        else:
            keys(items, NF, name)
            for it in items:
                w = it.get("finding_id")
                if it.get("kind") not in NKINDS:
                    print(f"  !! {w}: kind {it.get('kind')}")
                if it.get("importance") not in ("high", "medium", "low"):
                    print(f"  !! {w}: importance {it.get('importance')}")
                flag(w, "sentence_as_it_stands", it.get("sentence_as_it_stands"))
                flag(w, "quote", it.get("quote"))
                flag(w, "corrected_wording", it.get("corrected_wording"), advice=True)
                flag(w, "notes", it.get("notes"))
        if name in ("claim_updates", "notion_findings"):
            r = subprocess.run([sys.executable, "common/tools/quotecheck.py", p, "texts/"], capture_output=True, text=True)
            print("  quotecheck: " + r.stdout.strip().replace("\n", "\n  "))
        if name == "extra_studies":
            # quote_from_abstract is checked against the cached abstract
            tmp = [{"pmid": it.get("pmid"), "quote": it.get("quote_from_abstract")} for it in items]
            tp = f"{base}/.es_quotes.json"
            json.dump(tmp, open(tp, "w"))
            r = subprocess.run([sys.executable, "common/tools/quotecheck.py", tp, "texts/"], capture_output=True, text=True)
            os.remove(tp)
            print("  quotecheck (abstract quotes): " + r.stdout.strip().replace("\n", "\n  "))


if __name__ == "__main__":
    main()
