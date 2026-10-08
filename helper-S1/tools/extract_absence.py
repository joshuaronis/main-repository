"""Find candidate absence claims in a fetched Notion page.
Usage: python3 tools/extract_absence.py notion_pages/<page>.md [--section-list]
Prints: line no | nearest heading | candidate sentence (and flags dose-like numbers).
"""
import re, sys, json

PATTERNS = [
    r"\bno (?:published |human |randomi[sz]ed |controlled |direct |head-to-head |such |other |single )*(?:trial|study|studies|rct|experiment|measurement|data|evidence|comparison|report|paper|literature|series|record|figure|number)\b",
    r"\bnot? (?:been )?(?:ever )?(?:been )?(?:tested|measured|compared|studied|reported|published|run|done|assessed|quantified|established|examined|investigated|replicated|attempted|tried|timed|recorded)\b",
    r"\bnever (?:been )?(?:tested|measured|compared|studied|reported|published|run|done|assessed|quantified|examined|investigated|replicated|timed|recorded|looked)\b",
    r"\bnobody (?:has )?(?:ever )?\w+",
    r"\bno one (?:has )?(?:ever )?\w+",
    r"\bthe only (?:study|trial|paper|measurement|data|source|report|series|figure|one)\b",
    r"\bonly (?:study|trial|paper|measurement|report)\b",
    r"\bthere is no\b", r"\bthere are no\b", r"\bthere has been no\b", r"\bthere have been no\b",
    r"\bno(?:body|thing) \w+ (?:has|have)\b",
    r"\bhas not been\b", r"\bhave not been\b", r"\bhas never been\b", r"\bhave never been\b",
    r"\bdoes not exist\b", r"\bdo not exist\b", r"\bno such\b",
    r"\bunmeasured\b", r"\buntested\b", r"\bunstudied\b", r"\bunpublished\b", r"\bunknown\b", r"\bunanswered\b",
    r"\bremains? (?:un|without)\w*", r"\bis absent\b", r"\bare absent\b",
    r"\bno(?:t a)? single\b", r"\bzero (?:trial|study|studies|data)\b",
    r"\bwe do not know\b", r"\bit is not known\b", r"\bis not known\b", r"\bnot known\b",
    r"\bno trace\b", r"\bfound nothing\b", r"\bnothing (?:was )?found\b", r"\bturned up nothing\b",
    r"\bno (?:one|body) (?:has|had)\b", r"\blacks?\b", r"\bgap\b", r"\bmissing\b",
    r"\bcannot tell\b", r"\bcannot say\b", r"\bcannot be (?:known|answered|established)\b",
    r"\bno human\b", r"\bno animal\b", r"\bin no (?:study|trial)\b",
    r"\bsearched for (?:and|but) (?:does |did )?not\b", r"\bdoes not appear to exist\b",
]
RX = re.compile("|".join(PATTERNS), re.I)
# dose-like: percentage strengths, mg, mL, mEq, units, injection counts
DOSE = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:%|mg|ml|m[Ll]|mEq|µg|ug|mcg|units?|U/|:\d{3,})|\b1\s*:\s*\d{3,}", re.I)

def sentences(text):
    # split on sentence enders but keep decimals/abbrevs mostly intact
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"'(])", text)
    return [p.strip() for p in parts if p.strip()]

def clean(line):
    s = line
    s = re.sub(r"<[^>]+>", " ", s)            # tags
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # md links
    s = s.replace("\\\"", '"').replace("\\n", " ")
    s = re.sub(r"[|]{1}", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def main():
    path = sys.argv[1]
    t = open(path, encoding="utf-8").read()
    lines = t.split("\n")
    # drop Revisions / changelog to end
    stop = len(lines)
    for i, l in enumerate(lines):
        if re.match(r"^#{1,6}\s*(Revisions|Changelog|Change log|Revision history)\b", l.strip(), re.I):
            stop = i
            break
    heading = ""
    out = []
    for i in range(stop):
        raw = lines[i]
        s = raw.strip()
        if re.match(r"^#{1,6}\s", s):
            heading = re.sub(r"^#+\s*", "", s)
            continue
        c = clean(raw)
        if len(c) < 25:
            continue
        for sent in sentences(c):
            if len(sent) < 25:
                continue
            if RX.search(sent):
                out.append({"line": i + 1, "heading": heading, "sentence": sent,
                            "dose_flag": bool(DOSE.search(sent))})
    print(f"# {path}: scanned {stop} of {len(lines)} lines (Revisions cut at {stop}); {len(out)} candidates")
    json.dump(out, open(path.replace(".md", "_candidates.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for o in out:
        print(f"{o['line']}\t{'DOSE' if o['dose_flag'] else '    '}\t[{o['heading'][:46]}]\t{o['sentence'][:300]}")

main()
