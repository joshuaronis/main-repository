# S-686-07 — Effendy 2015, EMLA daily for ten days on leg ulcers (research letter)

Writing rules followed throughout: no plasma concentrations, no methaemoglobin values, no amount of cream,
no ulcer area covered, no toxicity threshold. The letter's introduction quotes a CNS-toxicity threshold, and its
discussion gives a parenteral prilocaine methaemoglobinaemia dose and the prilocaine content of the applied
amount; none of these is copied anywhere. Accumulation is described by direction only.

## 1. Right-paper check

- Text: `texts/S-686-07.txt`, 3 PDF pages, from
  `papers/S-686-07 - Effendy 2015 - Plasma concentrations and analgesic efficacy of lidocaine and prilocaine in leg ulcer-related pain during daily app.pdf`.
- PDF p. 1 title: "Plasma concentrations and analgesic efficacy of lidocaine and prilocaine in leg ulcer-related pain
  during daily application of lidocaine–prilocaine cream (EMLATM) for 10 days"; "DOI: 10.1111/bjd.13605";
  running foot "British Journal of Dermatology (2015) 173, pp259–261"; "Research letter".
- Byline (PDF p. 3): I. Effendy, A. Gelber, P. Lehmann, G. Huledal, S. Lillieborg (Bielefeld; Wuppertal;
  AstraZeneca, Södertälje).
- PubMed connector `get_article_metadata` 25494699: same title, Br J Dermatol 2015;173(1):259-61,
  DOI 10.1111/bjd.13605, authors Effendy I, Gelber A, Lehmann P, Huledal G, Lillieborg S; "[Abstract not
  available]"; publication types Clinical Study, Multicenter Study; PubMed date 2015-05-12 (the PDF's copyright
  line says 2014, the issue is 2015). Cached as `pm_work/cache/a_25494699.json`. **Right paper: yes.**
  Author list and page range in the task match the PDF and PubMed (five authors; pp. 259–261).
- person_note (papers_list.csv): "Earlier free Nexus request remains on record; paper later obtained through
  Sci-Hub Research." Nothing about another version or DOI; the PDF is the published letter.
- Text quality: ok. Extraction oddities: decimal points are dropped ("0·49" appears as "049", "P < 0·001" as
  "P < 0001"), the superscript minus is lost ("ng mL 1"), "Mölnlycke" appears as "M€ olnlycke". PDF pages 2 and 3
  were rendered to check Fig. 1 and the P values: Fig. 1 holds only day-10 plasma curves (lidocaine, prilocaine,
  sum), no methaemoglobin panel; the text gives P < 0·001 for the pain fall (PDF p. 3) and the Table 1 footnote
  gives P < 0·01 for the same comparison (minor inconsistency in the letter).
- Internal inconsistency in the letter: the methods say pre-dose samples were drawn "immediately before the start
  of application of EMLA on days 2, 4, 6 and 8" (PDF p. 1); the results report "Mean predose samples taken before
  EMLA application on days 3, 5, 7 and 9" (PDF p. 3).
- No instructions aimed at the reader inside the paper.
- The PubMed connector appends an "important legal notice" to metadata results asking for PubMed attribution and
  DOI links. That is the connector's own boilerplate, not text inside a paper or page; DOIs are recorded anyway.

## 2. The paper in the terms the claims need

- Design: open, uncontrolled, multicentre study (five dermatology departments, Germany), sponsor AstraZeneca.
  No placebo or comparator arm.
- Population: 25 adults with leg ulcers (23 needing sharp debridement, 2 not needing it but with chronic ulcer
  pain); aetiology venous 17, arteriovenous 5, vasculitic 3; 15 of 25 had moderate or severe chronic ulcer pain at
  enrolment (VRS). The words "neuropathic", "neuropathy" and "neuralgia" do not occur anywhere in the letter; no
  diabetic or neuropathic ulcer is listed among the aetiologies.
- Intervention: EMLA cream applied daily to the ulcer under cling film, wiped off after one hour, followed by sharp
  curette debridement on days 1–5 and up to day 10 when indicated; hydrocolloid or silicone dressings between
  treatments; compression on venous ulcers. (Amount of cream and maximum treated area: not written, per the
  paper-specific rules.)
- Exposure duration (asked by D066): one hour of contact per day ("After 1 h, any remaining cream was wiped
  away", PDF p. 1), daily for ten days, so about ten hours of cumulative contact. Recorded only here, in the card
  and in D066's reason.
- Outcomes: plasma lidocaine and prilocaine (LC-MS/MS) at serial times after the first (day 1) and last (day 10)
  application and pre-dose on alternate days; Cmax day 1 vs day 10 with two-sided 95% CIs; P90 of Cmax with a
  one-sided upper confidence limit; regression of Cmax on age, ulcer area, ulcer type and day; daily
  pre-application rating of current ulcer pain on a 100-mm VAS ruler (first of several "standard questions",
  the others not described); ulcer area on days 1 and 10; observed symptoms of systemic toxicity.
- NOT measured / not reported: methaemoglobin (no measurement, no result; the only mention of
  methaemoglobinaemia is a general statement about parenteral prilocaine, a dose-threshold sentence not copied);
  pain during debridement (not reported in the letter); quantitative sensory testing; any neuropathic-pain
  measure; a control group.
- Results (direction only): Cmax at day 1 and day 10 similar for lidocaine, prilocaine and the sum, 95% CIs of the
  differences include zero; pre-dose samples low ("minimal residual concentrations 24 h after the previous
  treatment"); "no apparent accumulation over 10 days"; Cmax rose with ulcer area, not with age or ulcer type; no
  symptoms of systemic toxicity observed. Pain: among patients with moderate or severe pain at enrolment, median
  pre-treatment VAS 75 on day 1 fell gradually to 21 by day 10 (P < 0·001; Table 1 range 0–72 on day 10).
  Ulcer area fell over ten days in the debridement group.
- Discussion: cites Purcell 2012 (single case, EMLA as a primary dressing left overnight on a painful leg ulcer,
  pain falling over three weeks) and says use in painful leg ulcers "deserves further study"; cites Aps & Reynolds
  1976 for biphasic vasoactivity of local anaesthetics (pallor / erythema at removal), noting similar frequencies
  with placebo cream (from earlier placebo-controlled data, not this study).
- Funding: AstraZeneca; S.L. an AstraZeneca employee, G.H. an employee during the study.

## 3. PubMed (connector; pm.py blocked by network policy). Every search is logged in pm_work/searches_log.tsv

Lookups and metadata:
- `get_article_metadata` 25494699 (Effendy 2015): no abstract in PubMed; metadata cached (a_25494699.json).
- `lookup_article_by_citation` for the reference list (the connector returns the PMID in the field `key`):
  ref 1 Jones 2006 -> 16835511; ref 2 Hofman 1997 -> 9256727; ref 3 Noonan 1998 (Phlebology) -> NOT FOUND;
  ref 4 Holm 1990 -> 1969197; ref 5 Lok 1999 -> 10025747; ref 6 Agrifoglio 2000 (Phlebology) -> NOT FOUND;
  ref 7 Rosenthal 2001 -> 12964231 (J Wound Care 2001;10(1):503-5, checked); ref 8 Briggs 2012 -> 23152206;
  ref 9 Hansson 1993 -> 8105630; ref 12 Scott & Huskisson 1976 -> 1026900; ref 13 Purcell 2012 -> 22886329;
  ref 14 Enander Malmros 1990 -> 1972836; ref 15 Aps & Reynolds 1976 -> 1023952.
  Ref 10 (Covino & Wildsmith 1998) is a book chapter and ref 11 (Hahn & Meeker 1991) a statistics book: no PMID.
- Searches confirming the two not-found references are not indexed:
  `Agrifoglio G[Author] AND (EMLA OR debridement OR leg ulcer)` -> count 0;
  `Noonan L[Author] AND Burge SM[Author]` -> count 0.
- Abstracts read: Lok 1999, Hansson 1993, Enander Malmros 1990, Holm 1990, Aps & Reynolds 1976, Rosenthal 2001,
  Briggs 2012, Purcell 2012, Jones 2006, Hofman 1997; and the records the requesting claims rely on:
  Essink-Tebbes 1999 (10333129), Moghtaderi 2009 (19845100), Attal 1999 (10353509).
  Cached for quoting: a_10025747 (Lok), a_8105630 (Hansson), a_28727591 (Purcell 2017). Not cached: abstracts
  that carry measured plasma figures, cream amounts or toxicity comparisons and that I do not quote
  (Enander Malmros, Holm, Stymne, Essink-Tebbes).
- Topic search (wildcard-limited by the connector, so written without truncation):
  `(EMLA[tiab] OR "lidocaine-prilocaine"[tiab] OR "lidocaine/prilocaine"[tiab] OR "Lidocaine, Prilocaine Drug
  Combination"[Mesh]) AND (ulcer[tiab] OR ulcers[tiab] OR wound[tiab] OR wounds[tiab] OR debridement[tiab]) AND
  (methemoglobin[tiab] OR methaemoglobin[tiab] OR methemoglobinemia[tiab] OR methaemoglobinaemia[tiab] OR
  "plasma concentration"[tiab] OR "plasma concentrations"[tiab] OR "plasma levels"[tiab] OR accumulation[tiab] OR
  repeated[tiab] OR daily[tiab])` -> count 21 (translation: the same terms as Title/Abstract plus the MeSH
  heading). All 21 read. Relevant beyond the reference list:
  - Purcell 2017 Adv Skin Wound Care, 28727591: pilot randomised trial, 60 participants with painful chronic leg
    ulcers of varied aetiology, EMLA daily for four weeks as a primary dressing vs standard wound care; pain
    lower during and after dressing change across the four weeks. Companion reports: 28836470 (wound healing
    and quality of life: no inhibition of healing) and 30002870 (feasibility).
  - Stymne & Lillieborg 2001 Br J Dermatol, 11703277: single 24-hour application on painful leg ulcers in 10
    patients, plasma lidocaine and prilocaine followed to 27 h; "analgesic efficacy of EMLA for the relief of
    chronic ulcer pain deserves further study" (figures in the abstract not copied).
  - Hoffmann 2024 Dermatol Ther, 38568445: case of an adult with methaemoglobinaemia and systemic toxicity after
    EMLA on a leg ulcer before debridement (case figures not copied).
  - Vanscheidt 2001 Eur J Dermatol, 11275800: review of 13 EMLA debridement investigations; repeated treatment
    did not change ulcer bacterial flora.
  - Claeys 2011 (20569291): randomised open trial, cream vs nitrous oxide over repeated debridement sessions.
  - Blanke 2003 (12972901): records review, 1084 patients, sharp debridement under the cream; no clinical
    methaemoglobinaemia observed (not measured).
  - Book 2009 (19212728): infant with scalds, methaemoglobinaemia after the cream on injured skin (case).
  - Lillieborg & Aanderud 2017 (29119061): plasma levels after single application to burns; Rangatchew 2024
    (39018678) review of the cream in burns; Al-Musawi 2016 (27397548) mice, higher plasma levels when a
    lidocaine-prilocaine gel is put into lacerations; Eroglu 2001 (11587465) mice, repeated application on
    sutured incisions with no adverse effect on healing; Zempsky 1997 (9250639) children's lacerations;
    Chang 2011 (21630059) and Seeman 2020 (32598070) not relevant.
- No methaemoglobin measurement across repeated sessions on ulcers or wounds was found in this set; the only
  repeated-dosing methaemoglobin measurement for topical lidocaine-prilocaine remains Essink-Tebbes 1999
  (preterm neonates, intact heel skin).

## 2b. Claim screen (all 320 claims in common/claims_all.json)

Method: a script over claim text, elements, evidence quote, proposed wording, reason, review, records_read and
needs_full_text, with these regex groups: EMLA / eutectic / lidocaine-prilocaine (all spellings); prilocaine /
Citanest / propitocaine; meth(a)emoglobin / metHb / o-toluidine; plasma / serum level / blood level / systemic
absorption / pharmacokinetic / Cmax; ulcer / wound / debridement; repeated / daily / accumulat / cumulative /
tachyphyla / successive / across sessions; authors (Effendy, Essink, Moghtaderi, Attal, Lok, Hansson, Enander,
Malmros, Holm, Aps, Reynolds, Purcell, Lillieborg, Huledal, Briggs, Agrifoglio, Rosenthal, Kopecky); PMIDs/DOI
(25494699, bjd.13605, 10333129, 19845100, 10353509, 10025747, 8105630, 1972836, 1969197, 1023952); vasoactivity /
vasodilat / biphasic / pallor / blanching / erythema. 127 claims hit; a second pass searched absorption / broken
or damaged skin / trough / washout / clearance / tachyphylaxis / tolerance wording (7 more hits, all already seen),
and every claim mentioning Aps or PMID 1023952 (only C036 and D008, which cite the 1978 Aps paper, not 1976).

Read closely and KEPT (entries written):
- C070 (own question) and D066 (own question).
- D069 (Safe Doses): its reason cites Effendy 2015 as topical repeated-exposure plasma sampling; full text
  confirms; verdict confirmed kept (other-claim entry).
- D072 (Safe Doses): tested as an absence of clearance/accumulation measurement between repeated sessions; its
  reason says nothing measures washout or accumulation between repeated cutaneous sessions, which Effendy (and
  Lok 1999) did for the topical route; verdict confirmed kept because the claim is about injection sessions
  (other-claim entry). Treated as an accumulation-measurement claim, which is how it was tested; its interval
  figure is not copied anywhere.
- C070 also gets an extra-study entry from Hansson 1993 (Effendy ref. 9).

Read closely and DROPPED (Effendy and its references do not bear on them):
- prilocaine-wheals: C065, C066, C067 (intradermal prilocaine duration — Effendy times nothing), C068, C069
  (methaemoglobin after small injected doses — Effendy measured no methaemoglobin and injected nothing).
- Prilocaine + Lidocaine: D067 (placebo-controlled neuropathic RCT — Effendy is uncontrolled and not
  neuropathic), D068 (paediatric meta-analyses).
- Intradermal wheal literature page: C039 (Swerdlow / Wightman uniqueness; Aps & Reynolds 1976 has no
  adrenaline or preservative arm), C036, C037, C046, C047.
- Relief that outlasts the block: D033 (neuropathic pain with documented skin numbness — Effendy is neither),
  D034, D039, D040, D044.
- Comparing injectables: D000 (flow recording past 90 min at a wheal — Aps & Reynolds observed vasoactivity
  but recorded no flow), D001, D005, D006, D009, D010, D014, D015, D018, D023, D024 (Willatts six-agent
  uniqueness — Aps & Reynolds 1976 has two agents), D002, D008, D021, D025.
- Lidocaine with epinephrine wheals: C072 (already refuted; Aps 1976 would be one more intradermal study),
  C073, C075, C077, C082, C083, C085, C087, C088, C092, C093, C094.
- Adjuvants page C013-C028; articaine page C049, C052, C054, C063; botulinum C006, C007, C012; procaine
  D053-D062; injectables ruled out D045-D052; topical page E003-E028; menthol page E030-E044; SFN pages A011-A087;
  T01-T08 (T02 is intradermal wheals for neuropathic pain — not topical, not Effendy). All matched only on
  generic words (daily, repeated, plasma, wound, author surnames such as Attal or Holm in other papers).

Claims not tested: dose or toxicity subject (counted only, text not written):
- Safe Doses Of Intradermal Analgesics: 4 claims not tested: dose or toxicity subject (D071, D073, D074, D075).
- prilocaine-wheals: 1 claim not tested: dose or toxicity subject (C071; it is also S-686-27's own question).

## 4. Notion (read-only: notion-search and notion-fetch only)

Searches (all with max_highlight_length 0 after the first, so personal Health History text stays out):
- "Effendy 2015" (25 results; semantic noise on "2015"; candidates: What is still unsettled, articaine-wheals,
  bupivacaine-wheals, What was searched for, Pain biology/topical anesthetics, Who paid for the evidence...);
- "25494699" (25; only Health History entries and unrelated pages — no page carries the PMID per search);
- "bjd.13605" (25; Who paid for the evidence (another BJD DOI), SFN routing page, Health History noise);
- "Effendy leg ulcer EMLA plasma concentrations ten days" (15: Reference, Product Guide, Prilocaine + Lidocaine,
  EMLA product rows in Buying Decisions & Info);
- "EMLA cream lidocaine prilocaine" (13: EMLA product rows UK/Mexico/Spain, Prilocaine + Lidocaine, Product Guide);
- "prilocaine methemoglobin repeated application accumulation" (16: prilocaine-wheals, Safe Doses, Prilocaine +
  Lidocaine, Reference, Product Guide, Pliaglis row, generic EMLA US row, "Pass in progress — topical pain market
  and safety correction (2026-09-21)" in Outstanding Work, Comparing injectables, Anestecin rows (Colombia),
  EMLA Mexico rows).

Pages fetched (as-of = page_version):
- prilocaine-wheals, https://app.notion.com/p/3c510b7903aa8159a5d9e4447ec15409, as of 2026-10-02T03:14:12.541Z
  (same version the claims were tested on); 76,671 chars, saved to a tool-result file; no truncated /
  unknown_block flags in the text. Does NOT cite Effendy (no "Effendy", no "ulcer"). Sentences relied on:
  - What is not known: "**Whether repeated small prilocaine doses accumulate any methemoglobin effect across
    sessions is unstudied.** The mechanism suggests they should not — the body converts methemoglobin back
    continuously, and a dose is cleared long before the next session — but no measurement of repeated dosing at
    this scale was found."
  - Sources › What has no source: "**No data on repeated prilocaine wheal sessions of any kind** — not on
    accumulated methemoglobin, not on local tissue change, not on whether the effect holds up over time."
  - (read, no finding) Sources › Topical prilocaine, Taddio 1998 entry: neonatal methaemoglobin bound "bounds
    nothing about adult-sized applications" — Effendy measured no methaemoglobin, so it does not change this.
  - Dose-ceiling passages on this page (the cream's prilocaine content against the injected ceiling; the
    methaemoglobin dose cut-off) were read and not copied.
- Prilocaine + Lidocaine, https://app.notion.com/p/33110b7903aa8024a793d7249262b267, as of 2026-10-02T03:14:00.887Z
  (same version tested); 100,421 chars, tool-result file; no truncated / unknown_block flags. Does NOT cite
  Effendy by name. Sentences relied on:
  - Does it relieve neuropathic pain?: "**Eleven patients, postherpetic neuralgia, the only study of repeated daily
    use.**" and Sources › Neuropathic pain, Attal entry: "the only dataset anywhere testing repeated daily
    application in an established neuropathic pain state" — both are claim D066 (own-question entry); no separate
    finding, since the claim record already carries the section and the same sentences.
  - Amount, area and absorption: "The label includes large-area hospital procedures and studies on leg ulcers;
    the former claim that no study ever involved legs, or that a [dose figure omitted] toxicity report was the largest published
    exposure, was too broad. None of this establishes repeated bilateral whole-leg treatment of idiopathic
    small-fibre burning." — read; correct as it stands (Effendy is repeated daily treatment of a capped ulcer area,
    not whole-leg SFN treatment); no finding. (This section is dose-heavy; no figures copied.)
  - What is still unknown: "Which amount, treated area and contact time would balance local benefit and systemic
    exposure for repeated neuropathic-pain use. Procedural instructions and PK study conditions do not answer that
    question." — dose subject; Effendy (non-neuropathic PK study) does not answer it; no finding.
- Safe Doses Of Intradermal Analgesics, https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7, as of
  2026-10-02T03:13:58.754Z (same version tested); 66,007-char result, tool-result file; no truncation flags.
  Does NOT cite Effendy. Ceilings read and counted, never copied (claims D071, D073, D074, D075 not tested: dose
  or toxicity subject; plus page passages on per-weight thresholds, cardiac epinephrine caps, a case dose, and
  label maxima, none of which Effendy bears on). Passages relied on:
  - What is still unknown: the D069 sentence ("...What would settle it: a plasma level drawn at [dose figure
    omitted] minutes after a full session, which no published study of wheal therapy has done for any agent.")
    — covered by my D069 other-claim entry (Effendy is topical, not wheal therapy).
  - Sources › What has no source: "**The safe interval between sessions on any of these agents.** [dose figure
    omitted] is the floor the published series work to, and it rests on those series' schedules rather than on a
    clearance measurement." — covered by my D072 other-claim entry.
  - What is still unknown: an open question whether a prilocaine methaemoglobin threshold holds for repeated
    exposure — threshold subject; Effendy measured no methaemoglobin; not answered; no finding.
  - Route and absorption section: product-specific topical PK examples (label figures) — nothing Effendy
    contradicts; no finding.
- Pain biology, ion channels, and topical anesthetics for small fiber neuropathy,
  https://app.notion.com/p/34210b7903aa8002aad4eba9787cb947, as of 2026-09-26T18:29:03.713Z; 171,915-char result,
  tool-result file; no truncation flags. Does NOT cite Effendy; mentions the cream only via Buckley 1993 (plasma
  levels by site and on diseased skin). Read §5.1.3–5.1.4 ("broken or inflamed skin, occlusion, prolonged contact,
  a thin or highly vascular site" move exposure upward; "Area and strength decide whether the low-exposure
  argument applies") — consistent with Effendy (peak levels rose with ulcer area; no accumulation; minimal levels
  a day later); no finding. §5.2.7 and 12.1.6 (daily lidocaine during capsaicin courses never tested — E019) — not
  touched by Effendy. Toxicity figures on this page read, not copied.
- 2 — Reference — Topical Treatments for Small Fiber Neuropathy, https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65,
  as of 2026-10-01T02:05:48.095Z; 1,279,938 chars of text in a tool-result file; searched with Python. The only
  "truncated" strings are in body text (a MEDLINE-truncated sentence; a truncated registry number), not fetch
  flags; no unknown_block flags. Counts: Effendy 0, 25494699 0, bjd.13605 0, Essink 0, Moghtaderi 0, Lok 0,
  Hansson 0, Enander 0, Holm 0, Purcell 0, Stymne 2 (S58), Attal 9 (most are other Attal papers), EMLA 42,
  prilocaine 53, ulcer 36. Effendy is NOT in the source register S1–S457. Sentences relied on (verbatim):
  - §4.2 header line: "**Magnitude MODEST, and UNKNOWN against placebo in established neuropathic pain · ... ·
    Evidence SERIES (n=12) + SERIES (n=11) + 2 CASES, all uncontrolled — plus one randomised placebo-controlled
    trial, n=46, which tested prevention and not treatment**" (omits Moghtaderi 2009 — D066/D067 territory; noted
    for the main session, no separate finding from this paper).
  - §4.2.1: "**Eleven more, also post-herpetic, are the only people anywhere given repeated daily EMLA in an
    established neuropathic pain state**" (same error as D066 -> finding, decided by Moghtaderi 2009).
  - §4.2.1: "**That is the one EMLA dataset describing the regimen this reference is evaluating, and its
    responder predictor is the one §9.3 is built around — preserved thermal function.**" (-> finding).
  - §4.2.1: "**The extensive remainder of the EMLA literature is procedural anaesthesia, which is a different
    question again.**" (-> finding; Effendy's outcome is chronic ulcer pain, not procedural pain).
  - Sources › S451 ("EMLA in neuropathic pain — the whole of it, and the one randomised trial in it."): "Attal
    1999 is the only test of a **repeated daily** regimen anywhere in this literature, and it has 11 patients."
    (same error as D066 -> finding, decided by Moghtaderi 2009). The S451 title's "the one randomised trial in
    it" is D067 territory (Flondell, Fassoulaki 2005, Moghtaderi) — noted only.
  - §2.5 and §9.10 (Skin integrity) and §4.2.2 cite Stymne 2001 [S58], a single 24-hour application to leg
    ulcers — correct as written; Effendy adds repeated daily ulcer data but nothing there is wrong; no finding.
  - §4.2.3 "No study has modelled chronic bilateral whole-leg application of a prilocaine product." — dose
    section; Effendy (capped ulcer area, ten days) does not model whole-leg application; correct; no finding.
