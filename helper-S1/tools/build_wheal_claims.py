"""Assemble results_S1/wheal_claims.json from an explicit triage spec.

Claim text is pulled verbatim from the fetched page (markup stripped), then the listed
`omit` substrings are replaced with [dose figure omitted]. Nothing is retyped by hand,
so the recorded sentence is the page's own wording minus the omissions.

Each spec entry: (claim_id, page_key, line, sent_idx | None, sections, elements, omit, note)
  line     1-based line number in notion_pages/<page_key>.md
  sent_idx which sentence of that line to take (0-based); None = whole cleaned line
  also_at  extra "line: section" places the same claim appears
"""
import json, re, sys

PAGES = {
    "R": ("ropivacaine", "Ropivacaine Wheals",
          "https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e", "2026-10-02T03:14:26.511Z"),
    "M": ("mepivacaine", "mepivacaine-wheals",
          "https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185", "2026-10-02T03:14:08.315Z"),
    "B": ("bupivacaine", "bupivacaine-wheals",
          "https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d", "2026-10-02T03:14:18.695Z"),
}

def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.replace('\\"', '"').replace("\\$", "$").replace("\\~", "~").replace("\\<", "<").replace("\\[", "[").replace("\\]", "]")
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = s.replace("**", "").replace("\\t", " ")
    s = re.sub(r"\b(FULLTEXT|ABSTRACT-ONLY|ABSTRACT|PAYWALLED|INFERENCE|DERIVED|AUDIT-READ|UNSOURCED|CITATION ONLY|FULL TEXT HELD)\b\s*", "", s)
    s = s.replace("\\<", "<").replace("\\>", ">")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def sentences(t):
    t = re.sub(r"^[-*\s]*\d+\.\s*", "", t)          # leading list number
    t = re.sub(r"^[-*\s]+", "", t)                      # leading bullet
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\"'(\d])", t)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if out and (len(p) < 18 or re.fullmatch(r"[\d.\s]+", out[-1])):
            out[-1] = (out[-1] + " " + p).strip()
        else:
            out.append(p)
    return out


def pick(line_text, locators):
    """Return the sentence(s) containing each locator, joined in order."""
    ss = sentences(clean(line_text))
    chosen = []
    for loc in locators:
        hit = next((s for s in ss if loc in s), None)
        if hit is None:
            raise LookupError(loc)
        if hit not in chosen:
            chosen.append(hit)
    return " ".join(chosen)

E = lambda pop="", iv="", de="", out="", oth="": {
    "population": pop, "intervention": iv, "design": de, "outcome": out, "other": oth}

# ---------------------------------------------------------------- triage spec
SPEC = [
 # ---- Ropivacaine Wheals: section 13 "The open gaps" is the core register
 ("W-R001","R",2703,["Nobody has measured neuropathic pain relief from an intradermal ropivacaine wheal at any concentration"],["13. The open gaps (gap 1)","5.6","9a.6"],
  E("people with neuropathic pain / SFN","intradermal ropivacaine wheal, any concentration","any","neuropathic pain relief"),
  [],"page states the gap is PARTIAL and that an earlier version overstated it; local-infiltration hits for neuropathic pain are listed at lines 2705-2708"),
 ("W-R002","R",2709,["Nobody has used ropivacaine wheals for small fibre neuropathy","No trial exists"],["13. The open gaps (gap 2)"],
  E("small fibre neuropathy","ropivacaine wheals","trial","any"),[],""),
 ("W-R003","R",2710,["Local tissue concentration over time at a wheal in human skin has never been MEASURED"],["13. The open gaps (gap 3)","4.11 item 1","4.5"],
  E("human skin","ropivacaine wheal","any","local tissue concentration over time"),
  [],"page already narrows this: measured in rat oral mucosa (Kimi 2012, Yamashiro 2016)"),
 ("W-R004","R",2711,["Flux and block duration have never been measured in the same wheal"],["13. The open gaps (gap 4)","4.11 item 3","5.8.3"],
  E("human skin","local anaesthetic wheal","any","skin blood flux AND block duration in the same wheal"),
  [],"page lists three partial hits (Yamashiro 2016, Bernards & Kopacz 1999, Liu 1995)"),
 ("W-R005","R",2712,["Skin blood flow at a ropivacaine wheal has never been recorded past 90 minutes"],["13. The open gaps (gap 5)","4.11 item 2","10.2"],
  E("human skin","ropivacaine wheal","any","skin blood flow beyond 90 minutes"),
  [],"page records Haefner 2008 to 24 h at a fingerpad after a digital block as a near miss"),
 ("W-R006","R",2714,["The procaine/ropivacaine version has never been tested, in any tissue"],["13. The open gaps (gap 7)","9.2"],
  E("any tissue","procaine followed by ropivacaine","any","ester-metabolite interference with block"),[],""),
 ("W-R007","R",2715,["Whether repeated ropivacaine over months does anything to skin that has already lost fibres"],["13. The open gaps (gap 8)","6.8a"],
  E("skin that has already lost nerve fibres","repeated ropivacaine over months","any","cumulative tissue effect / IENFD"),[],""),
 ("W-R008","R",2716,["Whether ropivacaine shares the unmyelinated-Schwann-cell selectivity"],["13. The open gaps (gap 9)","6.5"],
  E("unmyelinated fibres","ropivacaine","histological","Schwann cell selectivity"),
  [],"Kalichman 1989 tested chloroprocaine, procaine, etidocaine and lidocaine, not ropivacaine"),
 ("W-R009","R",2717,["Which way the toxicity ranking actually goes"],["13. The open gaps (gap 10)","6.1","6.2"],
  E("any","ropivacaine vs other local anaesthetics","any","relative local neurotoxicity ranking"),
  [],"four studies each way plus a review stating no consensus; recorded as unsettled rather than as an absence"),
 ("W-R010","R",2718,["What remains open is which brake dominates in dermal microvessels"],["13. The open gaps (gap 11)","4.10a"],
  E("dermal microvessels","ropivacaine","any","which relaxation brake dominates"),
  [],"gap marked LARGELY CLOSED by Ok 2013 in rat aorta; what is open is the dermal microvessel case"),
 ("W-R011","R",2721,["Nothing has ever been measured in neuropathic human skin after an injected local anaesthetic"],["13. The open gaps (gap 14)","4.7"],
  E("neuropathic human skin","injected local anaesthetic","any","local vascular response vs untreated, needle-only and saline controls"),
  [],"page calls this the most directly relevant missing experiment"),
 ("W-R012","R",2722,["No study varies them"],["13. The open gaps (gap 15)","10.8"],
  E("any","volume per wheal, number of wheals, treated area, spacing, session interval, site rotation","any","any outcome"),
  [],"page frames this as a gap in its own question rather than in the literature"),
 ("W-R013","R",2723,["The causal chain has never been observed end to end in the target tissue"],["13. The open gaps (gap 16)"],
  E("human dermis","ropivacaine wheal","any","the full causal chain end to end"),[],""),
 # ---- Ropivacaine: elsewhere on the page
 ("W-R014","R",1378,["There is still no measured vasodilation from ropivacaine in skin at any concentration"],["The correction to the project's question 8","0.0.1 (line 143)"],
  E("human skin","ropivacaine, any concentration","any","vasodilation"),[],""),
 ("W-R015","R",2319,["No study has compared any two of these drugs for neuropathic pain relief from an intradermal wheal"],["9a.6 What the comparison cannot tell him"],
  E("any","any two of the compared local anaesthetics","comparative study","neuropathic pain relief from an intradermal wheal"),[],""),
 ("W-R016","R",350,["The first 20 minutes of a wheal have never been characterised for ropivacaine at all"],["The shape of the needle-trauma curve"],
  E("any","ropivacaine wheal","any","the first 20 minutes of the response"),[],""),
 ("W-R017","R",349,["There is no clean drug-only reading at any timepoint"],["The shape of the needle-trauma curve"],
  E("any","local anaesthetic wheal","any","a drug-only reading separated from the puncture response"),[],""),
 ("W-R018","R",1279,["The ordering in dermal microvessels has never been measured for any of these drugs"],["The problem: this predicts the wrong answer for skin"],
  E("dermal microvessels","ropivacaine, lidocaine and the other compared drugs","any","ordering of vascular effect"),[],""),
 ("W-R019","R",1730,["The separation has never been measured for ropivacaine in any preparation"],["Two more confirmations, and then the caveats","10.4"],
  E("any preparation","ropivacaine","any","the A-fibre / C-fibre concentration separation"),[],""),
 ("W-R020","R",1731,["Nobody has recorded a cutaneous C-fibre during a local anaesthetic wheal in a human"],["Two more confirmations, and then the caveats"],
  E("human","local anaesthetic wheal","microneurography","cutaneous C-fibre recording"),[],""),
 ("W-R021","R",3053,None,["15.7 Papers named but not obtained","Supporting literature collected by Newton 2004 (line 1071)"],
  E("any","epinephrine / local anaesthetic","any","direct vasoconstriction-duration correlation"),
  [],"only-study claim about Liu 1995"),
 ("W-R022","R",1902,["This is the one histological finding in the literature that is selective for the fibre class at issue"],["6.5 The finding that matters most for small fibre neuropathy"],
  E("any","local anaesthetics","histological","selectivity for the unmyelinated fibre class"),
  [],"only-study claim about Kalichman 1989"),
 ("W-R023","R",1924,["the only measurement in humans of what prolonged local-anaesthetic exposure does"],["6.7 The human measurement"],
  E("humans","prolonged local-anaesthetic exposure","any","epidermal nerve fibre density"),
  [],"only-study claim about Wehrfritz 2011"),
 ("W-R024","R",1991,["the only one in the right tissue by the right route"],["9.1 The intradermal experiment, in humans"],
  E("human skin","ester plus amide mixture","intradermal, double-blind","block duration"),
  [],"only-study claim about Kim 1979"),
 ("W-R025","R",2301,["the most consistent vasoconstrictor of the six drugs ever compared head to head"],["9a.5 Mepivacaine","9a.2 The only six-drug human intradermal head-to-head"],
  E("human skin","six local anaesthetics","head-to-head intradermal","vasoactivity"),
  [],"only-study claim about Willatts & Reynolds 1985"),
 ("W-R026","R",2877,["no paper has contradicted the 21.5-hour duration"],["15.2 Duration"],
  E("any","ropivacaine","any","contradiction of the 21.5-hour duration"),
  [],"citation-standing claim; the page's own convention at 0.1 warns that zero contrasting citation statements does not mean no study disagrees"),
 ("W-R027","R",732,["gives the complete ordering that no single paper provides"],["4.4 The full concentration ladder"],
  E("human skin","ropivacaine concentration ladder","any","the complete ordering"),
  [],"only-source claim about the Cederholm 1994 dissertation"),
 ("W-R028","R",886,["It calculates the expected local tissue concentration, which nobody else has done"],["An independent replication of the peak"],
  E("any","ropivacaine","calculation","expected local tissue concentration"),
  [],"only-study claim about Sohn 2012"),
 ("W-R029","R",730,["Nobody has shown it in a wheal"],["What else the paper establishes"],
  E("a wheal","vasoconstricting local anaesthetic","any","prolonged duration of action"),[],""),
 ("W-R030","R",1935,["no study measures innervation"],["6.8a Four adjacent literatures on repeated or prolonged exposure"],
  E("any","repeated or prolonged local anaesthetic exposure","any","innervation"),[],""),
 ("W-R031","R",1055,["a third term nobody has separated"],["The flare is measurably blunted in neuropathic skin"],
  E("any","local anaesthetic wheal","any","separation of drug-suppressed flare from needle-created flare"),[],""),
 # ---- mepivacaine-wheals
 ("W-M001","M",18,["The only study that measured it in human skin"],["The recommendation"],
  E("human skin","mepivacaine","pinprick over an intradermal bleb","duration / recovery"),
  [],"only-study claim about Fairley & Reynolds 1981; the page's own source list calls Willatts & Reynolds 1985 the second such measurement"),
 ("W-M002","M",183,["That mepivacaine does not raise blood flow at 3 percent"],["What has no source","What does mepivacaine do to skin blood vessels (line 53)","Skin: vessels and duration (line 151)"],
  E("human skin","mepivacaine at the strength sold plain","any","skin blood flow"),
  ["3 percent"],"the strength sold plain was measured by neither cited study"),
 ("W-M003","M",101,["the only one performed on human cells"],["What does the laboratory say about damage"],
  E("human cells","mepivacaine vs lidocaine","laboratory study","relative toxicity"),
  [],"only-study claim"),
 ("W-M004","M",110,["because the trials cannot tell the two apart in either direction"],["What does the human evidence say about nerve damage"],
  E("any","mepivacaine vs lidocaine","randomised trials","neurologic symptoms"),[],""),
 ("W-M005","M",120,["nobody has measured damage to nerve fibres in skin from an injected anesthetic"],["What does the human evidence say about nerve damage","What is not known (line 146)"],
  E("skin","any injected local anaesthetic","any","damage to nerve fibres"),
  ["3 percent"],"the page pairs this with Wehrfritz 2011, which measured lidocaine patches rather than an injection"),
 ("W-M006","M",144,["Nobody has measured skin blood flow after a mepivacaine wheal for longer than an hour"],["What is not known"],
  E("any","mepivacaine wheal","any","skin blood flow beyond one hour"),[],""),
 ("W-M007","M",146,["Whether mepivacaine damages nerve fibers in skin is unmeasured","No such study exists for any local anesthetic"],["What is not known"],
  E("skin","mepivacaine and any local anaesthetic","any","nerve fibre damage"),[],""),
 ("W-M008","M",185,["No study has tested the assumption in either direction"],["What has no source","What is not known (line 147)"],
  E("skin","anything measured in spinal anaesthesia","any","transferability to skin"),[],""),
 ("W-M009","M",150,["the only one that times it against lidocaine and prilocaine in the same volunteers"],["Skin: vessels and duration"],
  E("same volunteers","mepivacaine vs lidocaine vs prilocaine","intradermal timing","duration"),
  [],"only-study claim about Willatts & Reynolds 1985"),
 ("W-M010","M",151,["the finding has never been directly tested again"],["Skin: vessels and duration"],
  E("any","mepivacaine","direct retest","skin blood flow finding"),
  [],"citation-standing claim about Guinard; zero contrasting citation statements is not the same as no disagreeing study"),
 # ---- bupivacaine-wheals
 ("W-B001","B",360,["Whether 0.5 percent really outlasts 0.25 percent in skin"],["What is still unknown","Does raising the strength help? (lines 80, 84)","What to buy in Mexico (line 350)"],
  E("human skin","bupivacaine at different strengths","any","duration"),
  ["0.5 percent","0.25 percent"],"the page reports one study that tested three strengths and the same authors' later contrary description of their own work"),
 ("W-B002","B",153,["nobody has measured damage in skin from an injected anesthetic"],["The toxicity paradox"],
  E("skin","any injected local anaesthetic","any","nerve damage"),
  [],"same claim as W-M005 on a different page"),
 ("W-B003","B",415,["Every duration, pain and blood-flow figure on this page comes from healthy volunteers"],["What has no source","What is still unknown (line 358)"],
  E("neuropathic leg skin","bupivacaine wheal","any","duration, pain and blood flow"),[],""),
 ("W-B004","B",359,["Whether the square-root scaling holds"],["What is still unknown"],
  E("human skin","wheals of different volumes of the same solution","side-by-side timing","duration"),
  [],"the page's 60-minute estimate is an interpolation between two studies differing in tissue layer, endpoint and country"),
 ("W-B005","B",413,["No study has compared all seven for injection pain intradermally"],["What has no source","What is still unknown (line 361)"],
  E("any","all seven compared agents","intradermal comparison","injection pain"),
  [],"the trial usually cited compared three agents and found etidocaine worse"),
 ("W-B006","B",364,["Whether the Schwann cell threshold means anything at wheal exposure times","It has not been done for any drug"],["What is still unknown"],
  E("any","local anaesthetic at wheal exposure times","time-course","Schwann cell threshold"),[],""),
 ("W-B007","B",365,["Whether repeated bupivacaine over months changes skin that has already lost fibers","Unstudied, as it is for every drug in this group"],["What is still unknown"],
  E("skin that has already lost fibres","repeated bupivacaine over months","any","change in skin / IENFD"),[],""),
 ("W-B008","B",412,["No source was found for 40.5 mm"],["What has no source"],
  E("any","plain bupivacaine","any","the circulating injection-pain figure"),
  [],"a sourcing claim about a figure in circulation; the figure is a pain score in mm, not a drug amount"),
]

# claims counted but not written out, because their subject is a dose ceiling,
# a toxicity threshold, or how to prepare, mix, dilute or inject a drug
SKIPPED = {
 "Ropivacaine Wheals": [
   {"line": 2024, "section": "9.3 pH decides the outcome of a mixture", "reason": "solution preparation / pH of mixtures"},
   {"line": 2528, "section": "10.5 What argues against, honestly", "reason": "dilution of an ampoule"},
   {"line": 2656, "section": "11.2 Dilution arithmetic", "reason": "mixing and dilution"}],
 "mepivacaine-wheals": [
   {"line": 186, "section": "What has no source", "reason": "sterility of a dilution procedure"}],
 "bupivacaine-wheals": [
   {"line": 402, "section": "The dose ceiling", "reason": "dose ceiling"},
   {"line": 363, "section": "What is still unknown", "reason": "lethal-concentration figure (toxicity threshold)"},
   {"line": 414, "section": "What has no source", "reason": "lethal-concentration figure (toxicity threshold)"}],
}

OMIT = "[dose figure omitted]"

def build():
    texts = {k: open(f"notion_pages/{v[0]}.md", encoding="utf-8").read().split("\n")
             for k, v in PAGES.items()}
    out = []
    for cid, pk, line, si, sections, elements, omit, note in SPEC:
        slug, title, url, ver = PAGES[pk]
        raw = texts[pk][line - 1]
        if si is None:
            text = clean(raw)
        else:
            try:
                text = pick(raw, si if isinstance(si, list) else [si])
            except LookupError as e:
                print(f"  !! {cid}: locator not found on line {line}: {e}", file=sys.stderr)
                continue
        for o in omit:
            if o not in text:
                print(f"  !! {cid}: omit string {o!r} not present", file=sys.stderr)
            text = text.replace(o, OMIT)
        out.append({
            "claim_id": cid, "page": title, "page_url": url, "page_version": ver,
            "section": "; ".join(sections),
            "claim": text,
            "elements_said_absent": elements,
            "queries": [], "records_read": [],
            "verdict": "", "uncertain": None,
            "evidence_pmid": "", "quote": "", "proposed_wording": "",
            "reason": "", "needs_full_text": [],
            "_source_line": line, "_note": note,
        })
    return out

if __name__ == "__main__":
    claims = build()
    json.dump(claims, open("results_S1/wheal_claims.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    json.dump(SKIPPED, open("results_S1/wheal_skipped.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    from collections import Counter
    print("claims written:", len(claims), dict(Counter(c["claim_id"][:3] for c in claims)))
    print("skipped (dose/toxicity/preparation subject):",
          {k: len(v) for k, v in SKIPPED.items()})
