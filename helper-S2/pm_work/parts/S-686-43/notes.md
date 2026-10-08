# S-686-43 — Flondell 2017, carpal tunnel syndrome treated with guided brain plasticity (RCT)

Writing rules applied throughout: no drug amount or concentration of the cream is written anywhere (they appear as
`[dose figure omitted]`); the application frequency and contact time appear only as what the study did, in the paper
card and in the D066 `reason`, as the orchestrator's task allows; quotes that carry the frequency are masked.

## 1. Right-paper check

- Text file: `texts/S-686-43.txt`, 7 PDF pages, from
  `papers/S-686-43 - Flondell 2017 - Carpal tunnel syndrome treated with guided brain plasticity a randomised controlled study.pdf`
  (publisher PDF, iText, created 16 Jul 2016; born-digital text layer, no OCR needed).
- PDF page 1 is the Taylor & Francis cover page ("Journal of Plastic Surgery and Hand Surgery"; "To cite this
  article: Magnus Flondell, Birgitta Rosen, Gert Andersson & Anders Björkman (2016)"; DOI 10.1080/2000656X.2016.1205503;
  "Published online: 12 Jul 2016").
- PDF page 2: running head "JOURNAL OF PLASTIC SURGERY AND HAND SURGERY, 2016", DOI 10.1080/2000656X.2016.1205503,
  "ORIGINAL ARTICLE", title "Carpal tunnel syndrome treated with guided brain plasticity: a randomised, controlled
  study", authors Magnus Flondell, Birgitta Rosen, Gert Andersson, Anders Björkman (Lund University / Skåne University
  Hospital, Malmö); received 6 Dec 2015, revised 9 May 2016, accepted 16 May 2016, published online 11 July 2016.
  Journal pages of the advance-online version run 1–6 (PDF pages 2–7).
- Matches the assigned paper (PMID 27403887, DOI 10.1080/2000656X.2016.1205503; the 2017 issue publication is the
  same article; person_note in common/papers_list.csv says the same). **Right paper: yes.**
- Text quality: **ok** (born-digital). Extraction oddities: "®" after EMLA and Excel/Viking Select extracted as "V"
  ("EMLAV"), "=" as "¼", "ö" split as "€o" (Malm€o, Bj€orkman), stray "R" lines from the margin marks, "µm" as "lm".
  Figure 1 (CONSORT flow chart, PDF p. 4) is an image: rendered at 110 dpi and read (numbers in section 1a). Table 2
  (PDF p. 5) checked in the layout view. Nothing missing: abstract, introduction, methods, results, discussion,
  acknowledgements (funding), disclosure, 24 references.
- No instructions aimed at the reader were found inside the paper.

### 1a. Figure 1 (CONSORT, rendered PDF p. 4) — read from the image
Assessed for eligibility 305; excluded 235 (did not meet inclusion criteria 130; declined 48; one or more exclusion
criteria 57); randomised 70. Placebo: allocated 36, received 36, lost 0, analysed 36. EMLA: allocated 34, received 34,
"Lost to follow-up (n=2 withdrew after first treatment due to local discomfort)", discontinued 2, analysed 32.
(Note: the results text says "No treatment-related adverse events were observed in any of the groups" (PDF p. 5),
while the flow chart records two withdrawals for local discomfort after the first treatment.)

## 1b. What the paper reports on pain (searched in the reading-order text of all 7 pages)

- "pain": 1 hit only, in the introduction (PDF p. 2): "Patients experience discomfort and often pain in the hand, as
  well as impaired hand function [3]." No pain measure anywhere in methods, results, tables or discussion.
- "numb", "tingl", "paraesth"/"paresth", "night"/"noctur", "weak", "analges": no hit in any symptom sense (the 3 "numb"
  hits are "number"/"numbers"; the 1 "tingl" hit is inside "Interestingly").
- The only VAS is satisfaction with treatment (0 'not satisfied at all' to 100 'maximally satisfied', PDF pp. 3-4).
- The SSS is reported only as one mean (SD) per arm at baseline and 8 weeks (Table 2, PDF p. 5: "BCTQ, Symptom
  Severity Scale (SSS, 0–5)"; the text on p. 5 says the scale "goes from 1–5"). No item-level or subscale breakdown.
- Blinding: "To ensure blinding of the investigators performing direct assessments, application and subsequent removal
  of EMLA® or placebo was performed by the same researcher (MF), who randomised and informed the participants"; "Two
  therapists – who were blind regarding the treatment ... carried out all the direct assessments and administered the
  PROMs" (PDF p. 3). Placebo "visually and cosmetically identical" (PDF p. 3). The words "double-blind" and "patients
  were blinded" do not appear.

## 3. PubMed (PubMed MCP connector; eutils blocked for pm.py) — records cached with pmcache.py

- get_article_metadata 27403887 (this paper): J Plast Surg Hand Surg 2017;51(3):159-164, e-pub 12 Jul 2016, types
  Journal Article + Randomized Controlled Trial. Cached a_27403887.json.
- get_article_metadata 39545073 (Flondell 2024, named in D067's proposed wording): J Brachial Plex Peripher Nerve Inj
  2024;19(1):e31-e41, PMC11563718. Cached a_39545073.json. Full text read via get_full_text_article PMC11563718:
  separate cohort (24 patients with unilateral CTS, ethics DNr 269–2008 amendment 23–2011, recruited over 4 years;
  this paper's approval is Lund 1062–03); same forearm regimen ("applied to the volar aspect of the forearm ... on the
  same side as the CTS for 90 minutes"; "participants administered [dose figure omitted] themselves at gradually increasing
  intervals for 8 weeks"); both groups did daily sensibility training; "Primary clinical outcome was longitudinal
  changes in tactile discrimination (2PD) within the two groups ... Secondary outcomes are dexterity, SSS, and
  QuickDASH"; randomisation error (one patient received placebo instead of EMLA: EMLA 11, placebo 13); "There were no
  significant differences in any clinical analyses between the EMLA and placebo groups"; SSS improved within the
  placebo group only (EMLA n.s.); fMRI: larger S1 activation after EMLA. No pain measure; the tactile stimulus "was
  intended to resemble touch but well below forced touch or pain".
- lookup_article_by_citation, reference list (24 refs; ref 16 is a book chapter without PMID): r1 Dale 2013 23423472;
  r2 Atroshi 1999 10411196; r3 Katz 1990 2324471; r4 Gerritsen 2002 11993525; r5 Ashworth 2011 22018420; r6 Scholten
  2007 17943805; r7 Taylor 2009 19737843; r8 Björkman 2010 20508542; r9 Duffau 2006 17049865; r10 Rosén 2006 16352379
  (J Hand Surg Br 31:126-32; the paper prints the volume as "13"); r11 Björkman 2004 15548216; r12 Rosén 2011 21524297
  (J Occup Med Toxicol 6:13; the paper prints "2011;13:3104948", i.e. article number and PMCID run together); r13
  Björkman 2009 19250441; r14 Atroshi 2013 24026316; r15 Leite 2006 17054773; r17 Lundborg 2007 17985560; r18 Levine
  1993 8245050; r19 Wewers 1990 2197679; r20 Bell-Krotoski 1993 8393725; r21 Katz 2002 12050342; r22 Schmid 2014
  25348629; r24 Jerosch-Herold 2011 22032626; r23 Tang 2015 (Plast Reconstr Surg 135:199) NOT FOUND by citation
  lookup; search `Tang DT[Author] AND "Nerve entrapment: update"[Title]` -> 0.
- get_article_metadata 8245050 (Levine 1993, the BCTQ), 17054773 (Leite 2006), 17985560 (Lundborg 2007), 16352379
  (Rosén 2006), 21524297 (Rosén 2011): all cached. Levine's abstract gives the score range ("5 points is the worst
  score and 1 point is the best score for each scale") but not the items.
- get_full_text_article PMC1624826 (Leite 2006): "the Symptom Severity Scale (SSS) which has 11 questions and uses a
  five-point rating scale"; "Each scale generates a final score (sum of individual scores divided by number of items)
  which ranges from 1 to 5". No item list.
- search `"Boston Carpal Tunnel Questionnaire"[tiab] AND ("Rasch"[tiab] OR "factor structure"[tiab] OR "items"[tiab])
  AND "symptom severity"[tiab] AND free full text[sb]` -> 6 (41374417, 41231164, 38948689, 33455019, 32919457,
  31867174); metadata read for all 6.
- get_full_text_article PMC7488577 (Multanen 2020, PMID 32919457, Rasch analysis of the BCTQ): "The Symptom Severity
  Scale consists of 11 items assessing pain, paresthesia, numbness, weakness, nocturnal symptoms, and difficulty of
  grasping"; "The first testlet comprised the five items on pain (items 1-5) and the other testlet the remaining six
  items on numbness, tingling, weakness, or fine motor skills of the hand (items 6-11)"; item wordings quoted there
  include item 5 "How long on average does an episode of pain last during the daytime?" and item 7 "Do you have
  weakness in your hand or wrist?". Deng 2019 (PMID 31867174, abstract) likewise splits the SSS into paresthesia
  (primary symptom) and pain (secondary symptom) items.
- SSS item content, as given in Levine 1993 and reproduced in these free sources: items 1-5 pain (1 severity of hand or
  wrist pain at night; 2 how often pain woke you at night; 3 pain in the daytime; 4 how often daytime pain; 5 how long
  an episode of daytime pain lasts); 6 numbness (loss of sensation); 7 weakness; 8 tingling; 9 severity of numbness or
  tingling at night; 10 how often numbness or tingling woke you at night; 11 difficulty grasping and using small
  objects. Night items: 1, 2, 9, 10. Score = mean of the 11 items (1 best, 5 worst).

- Later lookups: get_article_metadata 25348629 (Schmid 2014), 15548216 (Björkman 2004), 19250441 (Björkman 2009),
  24026316 (Atroshi 2013), 11993525 (Gerritsen 2002) — read for the card; Schmid 2014 and Björkman 2004 cached
  (Björkman 2009 and Atroshi 2013 not cached: they decide nothing and their abstracts carry application or injection
  amounts). Search `"nerve entrapment"[Title] AND update[Title] AND "Plast Reconstr Surg"[Journal] AND 2015[dp]` -> 1
  (25539328 = Tang 2015, ref 23; metadata read).

## 2. Claim screen (all 320 claims in common/claims_all.json, masked viewer `pm_work/tools/claims_view.py grep`)

Regexes run (hits): `carpal|\bCTS\b|median nerve|entrapment|compression neuropath` (5: A047, A053, D066, D067, E041);
`Flondell|Bj(ö|o)rkman|Lundborg|Ros(é|e)n\b|27403887|39545073` (2: D066, D067);
`plasticity|relearning|re-?education|deafferent|forearm|sensory training` (18, all but D067 via "forearm" =
healthy-volunteer forearm skin); `Boston|BCTQ|symptom.severity|Levine` (1: D067);
`EMLA|lidocaine.prilocaine|prilocaine.lidocaine|eutectic|lignocaine.prilocaine|lidocaine/prilocaine` (7: C039, C070,
D014, D066, D067, D068, E028); `placebo cream|vehicle|placebo-controlled|placebo controlled|sham` (68);
`vibration|nerve repair|nerve injur|transect` (8); `two-point|monofilament|tactile|sensibility|QuickDASH|\bDASH\b|touch
threshold|Semmes` (1: C025); `cortex|cortical|somatosensory|fMRI|\bbrain\b` (0);
`Moghtaderi|Attal|Fassoulaki|post-?herpetic|mastectomy` (18); `repeated (daily )?application|daily application|repeated
use|repeated applications|repeatedly` (7); `topical an(a)?esth|numbing cream|an(a)?esthetic cream|\bcream\b` (10);
`methylprednisolone|corticosteroid|Atroshi|triamcinolone|steroid injection` (4); `Schmid|intraepidermal nerve
fib.*(entrapment|compression)|entrapment neuropathy` (0); `neuropathic.pain.endpoint|pain endpoint|composite|symptom
score|patient-reported` (3); `(topical|patch|plaster).{0,40}lidocaine|lidocaine.{0,40}(topical|patch|plaster)` (13);
`only (randomi[sz]ed|placebo|controlled|blinded)[^.]{0,60}(topical|cream|an(a)?esthetic)` (5); `hand|wrist|finger` (10).

Read closely (claims_view.py show) and decided:
- D067 (own question) -> own-question entry, narrowed -> narrowed; plus extra-study entry (Flondell 2024).
- D066 (orchestrator asked for the Flondell element) -> other-claim entry, refuted -> refuted.
- A047 (PEA, CTS counted as neuropathic pain): kept only as a consistency point for D067 (the record already counts a
  carpal tunnel trial as a neuropathic-pain trial); the paper does not bear on PEA. No entry.
- E041 (menthol; CTS trial counted in "Does menthol relieve neuropathic pain?"): consistency point only. No entry.
- A053 (ESWT in SFN): CTS appears only among excluded hits. Dropped.
- D033 ("Eight papers is the entire world literature on cutaneous anaesthesia for neuropathic pain in which the skin was
  demonstrably numbed"): this trial numbed forearm skin remote from the symptomatic territory, did not document the
  numbness, and had no pain-relief endpoint, so it does not join that literature. Dropped (no entry).
- D041 ("No study has treated one limb and observed the other"; outcome element = pain in the other limb): this trial
  treated and observed the same side; Flondell 2024 tested the contralateral hand's sensibility, not pain. Dropped.
- E028 (35-45 minute topical lidocaine figure): no anaesthesia-duration measurement here. Dropped.
- E005 (topicals in idiopathic SFN), E006, E008, E019, E027, D014, D065, C070, C039, D068, T02: different population,
  drug, route or outcome; nothing in the paper bears on them. Dropped.
- C028/C022 (steroid adjuvants, repeated intradermal): Atroshi 2013 (ref 14) is a single carpal-tunnel steroid
  injection, not intradermal or repeated. Dropped.

Claims surfaced by the greps whose subject is a dose ceiling, toxicity, preparation or injection technique (not
opened in full, not re-judged; none bears on this paper):
- Comparing the injectable local anesthetics for intradermal wheals: 1 claim not tested: dose or toxicity subject
- articaine-wheals: 1 claim not tested: dose or toxicity subject
- Safe Doses Of Intradermal Analgesics: 2 claims not tested: dose or toxicity subject
- 💉 Lidocaine With Epinephrine Wheals: 1 claim not tested: dose or toxicity subject
- Prilocaine + Lidocaine: 0 claims not tested: dose or toxicity subject (D066, D067, D068 all screened)

## 4. Notion (read-only: notion-search and notion-fetch only)

### Pages fetched
- "Prilocaine + Lidocaine" — https://app.notion.com/p/33110b7903aa8024a793d7249262b267 — as of
  2026-10-02T03:14:00.887Z (same version the claims were tested on); 101,635 characters, saved to a tool-results file and
  parsed as JSON (`text` field); no `truncated`, `unknown_block_count` or `unknown_block_ids` present; verification
  unverified. Terms searched in the text: Flondell, Björkman/Bjorkman/Bjørkman, Lundborg, Rosén/Rosen, plasticity,
  relearning, re-education/reeducation, carpal/CTS, Boston/BCTQ, symptom severity, 27403887, 2000656X, Moghtaderi,
  Effendy: 0 hits each. The page does not cite Flondell 2017 or any carpal tunnel study. "forearm" 1 hit ([S-Q]
  Christensen 2021, healthy-volunteer forearms; irrelevant). Sentences relied on (verbatim, dose figures masked):
  - Description property: "Its neuropathic-pain evidence is thin and almost entirely uncontrolled — a twelve-patient
    series, an eleven-patient series, two case reports, and one placebo-controlled trial that prevented post-mastectomy
    pain rather than treating an established one — while the enormous literature behind it is procedural anaesthesia."
  - Section "Does it relieve neuropathic pain?": "**The reviewed treatment evidence consists of small uncontrolled PHN
    series and case reports.** These concern postherpetic neuralgia or surgical nerve injury, not established efficacy
    for idiopathic small-fibre neuropathy. This is a description of the studies reviewed, not an exhaustive count of all
    research." (hedged; accurate on its natural reading; no finding)
  - Same section: "**One placebo-controlled randomised trial exists with a neuropathic-pain endpoint, and it is
    prevention rather than treatment.**" (= D067; handled by the claim update)
  - Same section: "- **Eleven patients, postherpetic neuralgia, the only study of repeated daily use.**" (= D066)
  - Same section: "**Clinical assessment:** EMLA has an established procedural role and limited, indirect evidence for
    neuropathic symptoms." (accurate; no finding)
  - Sources [S-B]: "— the only dataset anywhere testing repeated daily application in an established neuropathic pain
    state, 5 h/day for six days, with quantitative sensory testing" (= D066)
  - Sources [S-D]: "— the only randomised placebo-controlled trial with a neuropathic-pain endpoint: n=46" (= D067)
- "Lidocaine [dose figure omitted] + prilocaine [dose figure omitted] cream (generic EMLA, ANDA), [pack size omitted] (multi-tube pack), Rx (United States)" (Buying Decisions &
  Info) — https://app.notion.com/p/3e310b7903aa81babfe6c4dc1ffeff35 — as of 2026-09-24T21:49:39.792Z; not truncated, no
  unknown blocks; verification unverified. (The row's title strengths are product identity, not quoted further.)
  Sentences relied on (verbatim):
  - Why: "Good: Met Intended Purpose is Kinda — two small uncontrolled studies of EMLA itself in postherpetic neuralgia
    reported improvement, a positive result however weak, and no placebo-controlled trial in established neuropathic
    pain is indexed in PubMed."
  - Why For Purpose: "EMLA has two small uncontrolled studies of its own in postherpetic neuralgia and one
    placebo-controlled trial of prevention after breast surgery; no placebo-controlled trial in established neuropathic
    pain is indexed in PubMed, so its evidence is weak"
  - Body, What would change this: "Nothing short of a placebo-controlled trial in established neuropathic pain."
  (The row also carries label amounts and a methaemoglobin threshold in other fields; not copied.)
- "Lidocaine [dose figure omitted] + prilocaine [dose figure omitted] cream (generic EMLA, ANDA), [pack size omitted] tube, Rx — HealthWarehouse.com (United States)"
  — https://app.notion.com/p/3e310b7903aa81a4922ef2f324ea30d9 — as of 2026-09-24T21:49:02.035Z; not truncated. Why,
  Why For Purpose and What would change this: the same three sentences as the multi-tube pack row, verbatim (checked).
- "Lidocaine [dose figure omitted] + prilocaine [dose figure omitted] cream (generic EMLA, ANDA), GoodRx default pack, not recorded, Rx (United States)"
  — https://app.notion.com/p/3e310b7903aa81a59629e016121bfaf2 — as of 2026-09-24T21:48:22.938Z; not truncated. Why and
  Why For Purpose: the same two sentences verbatim. What would change this: "A placebo-controlled trial of lidocaine
  with prilocaine in established neuropathic pain would move the fit either way; a lower price moves only the ranking
  between sellers."
- "EMLA anaesthetic disc (AstraZeneca) lidocaine [dose figure omitted] + prilocaine [dose figure omitted] — discontinued (United States)" —
  https://app.notion.com/p/3e310b7903aa81fcb0b8d115f0c3a8b3 — as of 2026-09-24T03:35:51.596Z; not truncated.
  Why For Purpose (verbatim): "Its one placebo-controlled trial is prevention, not treatment: perioperative EMLA reduced
  chronic pain three months after breast-cancer surgery in 46 women \[Fassoulaki 2000, *Reg Anesth Pain Med*,
  doi:10.1053/rapm.2000.7812\]." What would change this: "A US relaunch. To Yes: a controlled trial of the lidocaine and
  prilocaine emulsion as a treatment for neuropathic pain." (accurate; Flondell is not such a trial)
- "EMLA crema (Aspen México) ... tubo [pack size omitted] — Farmalisto (Mexico)" — https://app.notion.com/p/3e010b7903aa81e38a4cdc9e8552cac5
  — as of 2026-09-24T21:42:05.371Z; not truncated. Why For Purpose: "The 46-person breast-surgery trial studied
  prevention, not treatment of established neuropathic pain." (accurate; no absence claim; no finding). Sibling Mexican
  EMLA crema rows (Klyns, La Comer via Rappi, París, del Ahorro) show the same highlight in search; not fetched.
- "EMLA Cream [dose figure omitted] (Aspen) ... [pack size omitted] tube with applicator, cutaneous — Medino (United Kingdom)" —
  https://app.notion.com/p/3e210b7903aa81d5afc8f80bdc8394a1 — as of 2026-09-24T21:35:08.168Z; not truncated. Evidence
  stated as "EMLA's two small uncontrolled studies in postherpetic neuralgia" (hedged, no absence claim; no finding).
- "2 — Reference — Topical Treatments for Small Fiber Neuropathy" — https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65
  — as of 2026-10-01T02:05:48.095Z; 1,279,938 characters in `text`, saved to a tool-results file and parsed; no
  `truncated` key or unknown blocks (the word "truncated" occurs twice inside content); ends with </content></page>.
  Hits: Flondell 0, Björkman/Bjorkman/Bjørkman 0, Lundborg 0, Rosén/Rosen 0, relearning 0, re-education 0, BCTQ 0,
  27403887 0, 2000656X 0, Moghtaderi 0; carpal tunnel 15 (menthol §4.26 and S144 Sundstrup; curcumin §4.45.7 and S268
  Sharifi Razavi 2024, graded "RCT-ADJACENT (carpal tunnel syndrome, n=70, placebo-gel-controlled)" on the Boston SSS;
  Fisionerv §4.46; topical-agents-not-found table §4.50; acetyl-L-carnitine §6.12.2), EMLA 42, Boston 2 (both the
  curcumin trial's SSS), plasticity 1 (S126, irrelevant), guided 4 (CBT, irrelevant), forearm 11 (healthy forearm skin;
  EMLA plasma data). Sentences relied on (verbatim, dose figures masked):
  - §4.2 evidence line: "**Magnitude MODEST, and UNKNOWN against placebo in established neuropathic pain · Duration 60
    minutes under occlusion for reliable dermal anaesthesia, about 2 hours afterwards · Evidence SERIES (n=12) + SERIES
    (n=11) + 2 CASES, all uncontrolled — plus one randomised placebo-controlled trial, n=46, which tested prevention and
    not treatment**"
  - §4.2.1 lead: "**Four uncontrolled reports, and one randomised trial that asked a different question.**"
  - §4.2.1: "**A randomised placebo-controlled trial with a neuropathic endpoint exists, and it is a prevention trial.**"
    (existence statement, accurate; no finding)
  - §4.2.1: "**It is not a test of putting EMLA on skin that already burns**, which is the use this reader is
    considering, and nothing in it transfers to that use."
  - S451 title: "**S451.** EMLA in neuropathic pain — the whole of it, and the one randomised trial in it."
  - S451: "The four uncontrolled reports come to **25 patients between them**, **every one post-herpetic or causalgic and
    none idiopathic**; all are open, none has a placebo arm, and the largest of them is from 1989."
  - §4.26.1 (menthol, for consistency): "**A placebo-controlled randomised trial of topical menthol in a neuropathic
    population does exist, and it is at [dose figure omitted].** A **triple-blind randomised placebo-controlled
    crossover** trial in **carpal tunnel syndrome** — an entrapment neuropathy — ..."
  - §4.45.7 (curcumin, for consistency): "Evidence RCT-ADJACENT (carpal tunnel syndrome, n=70, placebo-gel-controlled)"
    and "Boston Carpal Tunnel Questionnaire Symptom Severity Scale between groups **p=0.021**".
  - Earlier findings S2-F036/F037/F038 (S-686-07 worker) already cover the D066 part of §4.2.1 and S451 and say the
    "one randomised trial"/placebo-arm part is left to this session.
- "1 — Product Guide — Topical Treatments for Small Fiber Neuropathy" — https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f
  — as of 2026-10-02T03:14:29.224Z; 599,993 characters in `text`, saved to a file and parsed; no truncation keys; ends
  with </content></page>. Hits: Flondell 0, Björkman 0, Lundborg 0, Rosén 0, plasticity 0, relearning 0, BCTQ 0,
  27403887 0, Moghtaderi 0, Fassoulaki 0; carpal tunnel 7 (menthol rank 13 "Evidence RCT-ADJACENT (carpal tunnel
  syndrome, placebo-controlled crossover)"; curcumin gel "Evidence RCT-ADJACENT (carpal tunnel syndrome, n=70,
  placebo-gel-controlled)" with its Boston SSS result; menthol rubs set aside), EMLA 35. Sentences relied on (verbatim,
  dose figures masked):
  - Ranks 19-23 intro: "one, EMLA, rests on two small uncontrolled series of its own and is not ruled out"
  - Rank 19 entry ("### 19 · EMLA cream — lidocaine [dose figure omitted] + prilocaine [dose figure omitted], [pack
    size]") evidence line: "**Magnitude MODEST, and UNKNOWN against placebo in established nerve pain · Duration about 2
    hours after 60 minutes under occlusion · Evidence SERIES (n=12) + SERIES (n=11) + 2 CASES — plus one randomised
    placebo-controlled trial of prevention, not treatment**"
  - Rank 19 entry: "Its evidence in neuropathic pain is **two uncontrolled series — twelve patients and eleven — and two
    single-patient case reports**, every one of them post-herpetic or causalgic rather than idiopathic, none with a
    placebo arm and none running longer than six days, so it is not buying anything the plain ointment does not."
    ("none with a placebo arm" describes those four reports and is accurate for them; the Moghtaderi omission is
    S2-F039.)
  - Part Two "### EMLA patches, [dose figure omitted] × 2 — 238 MXN" evidence line: "**Magnitude MODEST, and UNKNOWN
    against placebo in established nerve pain · Duration about 2 hours · Evidence SERIES (n=12) + SERIES (n=11) + 2 CASES
    — plus one randomised placebo-controlled trial of prevention, not treatment**"
- "EMLA Pflaster (Aspen) ... [pack size omitted], cutaneous — cleverapo (Germany)" — https://app.notion.com/p/3e210b7903aa8184a79acac0d4f91989
  — as of 2026-09-24T15:08:29.645Z; not truncated. Evidence stated as "its neuropathic evidence is weak: EMLA's two small
  uncontrolled studies in postherpetic neuralgia, Stow 1989 and Attal 1999" (hedged; no absence claim; no finding).
- "What is still unsettled across these pages, and what would settle each one" — https://app.notion.com/p/3d410b7903aa819f8300e976a62577db
  — as of 2026-09-26T18:23:10.973Z; 61,415 chars; complete (ends </page>), no truncation keys. Flondell/Björkman/
  Lundborg/Rosén/plasticity/relearning/carpal/Boston/Fassoulaki/Attal/Moghtaderi: 0. EMLA 6 hits, all about the
  Mexican registro suffix and an AEMPS large-area notice (ceiling subject; not opened further). No open question on
  EMLA's neuropathic evidence, carpal tunnel or sensory relearning. No finding.
- "5 — Soft ground in these documents" — https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 — as of
  2026-09-26T18:26:13.509Z; complete. Nothing on EMLA's neuropathic evidence, carpal tunnel or sensory relearning (S451
  appears only as individually checked for retraction notices). No finding.
- "What was searched for and does not exist, so it is not searched for again" — https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82
  — as of 2026-09-27T00:27:49.877Z; 64,683 chars; complete. EMLA 0, prilocaine 0, Flondell 0; carpal 2 (vitamin B12
  phonophoresis registration; topical curcumin in CTS). No finding.
- "Non-drug treatments for SFN — what survives blinding, and what you can get in Mexico" — https://app.notion.com/p/3d410b7903aa81459170f45b4b02f289
  — as of 2026-09-22T09:09:37.946Z; 124,038 chars; complete. plasticity, relearning, re-education, deafferent, forearm,
  carpal, EMLA, prilocaine: 0. ("anaesthe" 3 hits: compression stockings as occlusion; no interaction data with
  intradermal anaesthetic.) No finding.
- "Alternative Treatments For Growing Back Nerves In SFN" — https://app.notion.com/p/1d410b7903aa80b684fce440ab72ee3d —
  as of 2026-09-26T18:25:56.958Z; 175,566 chars; complete. relearning, re-education, deafferent, forearm, EMLA: 0;
  plasticity 1 (acupuncture, BDNF); carpal 2 (acetyl-L-carnitine after carpal tunnel release, Olson 2019). No finding.

### Notion searches (notion-search; results are candidates only, each relevant page fetched)
- "Flondell" (25 results): no page about this paper (LMX4 rows, Product Guide, apondo, etc. — semantic matches).
- "Carpal tunnel syndrome treated with guided brain plasticity" (17): menthol/curcumin CTS product rows, Uridine,
  L-Carnitine, Reference, Product Guide, Health History entries on "brain plasticity" (personal, left alone).
- "lidocaine and prilocaine cream generic United States placebo-controlled trial established neuropathic pain" (15):
  the three US generic EMLA rows, the EMLA disc row, UK and Mexican EMLA rows, Reference, Product Guide.
- "EMLA no placebo-controlled trial in established neuropathic pain is indexed in PubMed" (15): the same EMLA rows,
  Mexican EMLA crema and parches rows, Colombian Anestecin row (highlights hedged).
- "sensory relearning forearm anaesthesia guided plasticity" (17): stem-cell, TENS, desensitisation pages — none on
  sensory relearning or forearm anaesthesia.
- "Björkman Lundborg Rosén cutaneous forearm deafferentation EMLA hand sensibility" (25): EMLA product rows (UK,
  Spain, Mexico, Germany), Product Guide, Prilocaine + Lidocaine, and "Lidocaine With Epinephrine Wheals" (its Lundborg
  hit is Selander, Brattsand, Lundborg, Nordborg — a different, intraneural-injection paper; not this topic).
- "27403887" (10) and "10.1080/2000656X.2016.1205503" (10): no page cites the PMID or DOI.
- `"no placebo-controlled trial in established neuropathic pain is indexed in PubMed"` (15): no further EMLA row
  surfaced (semantic search; not used to decide absence).
- Not fetched (search highlights hedged; listed so the main session can check them if it wants every location):
  Mexican EMLA crema rows at Klyns, La Comer via Rappi, París, del Ahorro, Guadalajara; Mexican EMLA parches rows
  (Guadalajara, San Pablo, del Ahorro); UK EMLA rows (Medino [pack sizes omitted], LloydsPharmacy ×4, Well);
  Spain EMLA [pack size omitted]; German EMLA Pflaster rows (ayvita, Aponeo, Pharmeo, apondo, Sparmed, Meine OnlineApo);
  Colombian Anestecin (Locatel). The fetched representatives of these groups (Farmalisto, Medino [pack size omitted], cleverapo) carry
  no absence sentence.

## 3b. Further PubMed work ("beyond": other trials of the cream in carpal tunnel syndrome and guided plasticity)

- search `(EMLA[tiab] OR "lidocaine-prilocaine"[tiab] OR "lidocaine/prilocaine"[tiab] OR "prilocaine-lidocaine"[tiab] OR
  "eutectic mixture"[tiab] OR "Lidocaine, Prilocaine Drug Combination"[Mesh]) AND ("carpal tunnel"[tiab] OR "median
  nerve"[tiab] OR entrapment[tiab] OR "compression neuropathy"[tiab])` -> 17. Metadata read for all unfamiliar ones:
  40107421, 37279742, 33708996 (nanoparticle "entrapment efficiency", irrelevant); 35342267 and 29173870 (EMLA
  skin-wrinkling test as a diagnostic in CTS, with the Boston SSS and NPSI as correlates — diagnosis, not treatment);
  14571460 (EMLA vasoconstriction test in CTS, diagnostic); 22118874, 7486304 (nerve-block cohorts for carpal tunnel
  release with EMLA for needle pain); 12367547 Lawrence 2002 and 11062570 Avramidis 2000 (RCTs of EMLA before the
  local-anaesthetic injection for carpal tunnel release — procedural pain, not neuropathic pain); 11560444 (letter);
  19251262 (chromatography), 19163212 (rat sonophoresis). Treatment trials of the cream in CTS: Moghtaderi 2009
  (19845100, D066 record), Flondell 2017, Flondell 2024 only.
- search `("forearm anaesthesia"[tiab] OR "forearm anesthesia"[tiab] OR "cutaneous anaesthesia"[tiab] OR "cutaneous
  anesthesia"[tiab] OR "selective temporary anaesthesia"[tiab] OR "selective temporary anesthesia"[tiab] OR
  deafferentation[tiab] OR "guided plasticity"[tiab]) AND (EMLA[tiab] OR "local anaesthetic cream"[tiab] OR "local
  anesthetic cream"[tiab] OR "anaesthetic cream"[tiab] OR "anesthetic cream"[tiab] OR "Lidocaine, Prilocaine Drug
  Combination"[Mesh]) AND (hand[tiab] OR sensibility[tiab] OR sensory[tiab] OR neuropathy[tiab])` -> 21 (PubMed's
  translation folds the two "selective temporary" phrases away). Metadata read for the 14 unfamiliar ones:
  - 26270587 Strauss 2015, Pain: double-blind placebo-controlled study, 12 patients with chronic unilateral CRPS I of the
    hand, anaesthetic cream on the affected forearm; "Pain intensity was not modulated after intervention." Decides D067
    (extra-study entry, refuted, uncertain). Abstract does not name the cream; no PMC copy (convert_article_ids: none).
    Full text read free in the first author's Greifswald dissertation at the German National Library
    (https://d-nb.info/113254338X/34, surfaced by a Firecrawl web search; read with the Parallel web_fetch tool): EMLA
    (AstraZeneca) against an aqueous placebo cream ("Aqueous Cream B.P., AquaDerm"); "pseudorandomized double blind
    design ... in two separate sessions"; "The order of the verum and placebo session was randomized with 6 of 12
    participants receiving placebo cream in the first session"; washout at least 5 days; "Pain intensity was assessed at
    rest before and after each session with self-rating on a visual analogue scale (VAS; 10 cm)"; "Pain was not altered
    during intervention (F(1,10)= 0.52; n.s.)"; two of 12 were pain-free on the day; mean symptom duration 30 months.
    (The application amount in that text is not copied here.)
  - 20636964 Lundborg 2010, Diabet Med: double-blind RCT, 37 people with diabetes and impaired foot sensibility, the
    cream or placebo cream once on the lower leg; touch thresholds of the sole improved. Sensory endpoint only.
    extra_studies entry (bears on how D067's wording describes what exists).
  - 19597277 Hassan-Zadeh 2009: randomised double-blind, nerve repair, a "Lidocaine-PTC" cream (not stated to be the
    lidocaine-prilocaine eutectic) repeatedly over 2 weeks on the forearm; sensory outcomes. Not used (cream identity
    unclear; no pain endpoint).
  - 18382287 Björkman 2008 (case report, plexus injury, Braille reading regained after repeated forearm anaesthesia at
    increasing intervals) and 18188784 Rosén 2008 (case report, vibration-and-compression neuropathy, repeated forearm
    EMLA): further non-daily repeated-application cases in established nerve injury/neuropathy; case reports, not
    needed for D066's verdict; not cached.
  - 21454817 Weiss 2011, 22915119 Sens 2012, 23735321 Sens 2013, 30151000 Sens 2018 (stroke; forearm deafferentation,
    some placebo-controlled crossover), 23221418 Petoe 2012 (healthy, EMLA vs placebo RCT), 19656355 Ageberg 2009 and
    22574814 Ageberg 2012 (knee; healthy and ACL injury; no effect), 19033877 Rosén 2009 (healthy lower leg), 15351377
    Yildiz 2004 (facial anaesthesia, healthy): no neuropathic or pain population; not used.
  - Björkman 2005 (contralateral deafferentation in nerve-injured hands), named by the orchestrator: not retrieved by
    these searches and not cited by this paper; not needed for any verdict (D041's outcome element is pain in the other
    limb; D041 already refuted on Casale 2009). Not looked up further.
- search `("anesthetic cream"[tiab] OR "anaesthetic cream"[tiab] OR "local anesthetic cream"[tiab] OR "local anaesthetic
  cream"[tiab] OR "topical anesthesia"[tiab] OR "topical anaesthesia"[tiab] OR "cutaneous anesthesia"[tiab] OR
  "cutaneous anaesthesia"[tiab]) AND (neuropathic[tiab] OR neuralgia[tiab] OR neuropathy[tiab] OR "complex
  regional"[tiab] OR CRPS[tiab] OR phantom[tiab] OR "nerve injury"[tiab] OR allodynia[tiab]) AND (placebo[tiab] OR
  sham[tiab] OR vehicle[tiab])` -> 5 (39545073, 27403887, 26270587, 19597277, 19033877): no further trial whose
  abstract hides the cream's name.
- convert_article_ids 26270587, 20636964, 19597277: no PMCID for any.
- Cached: a_26270587 (Strauss 2015), a_20636964 (Lundborg 2010).

## 4b. Notion decisions after Strauss 2015

- The record counts CRPS within its neuropathic-pain evidence (Reference §1.4 "Topical diclofenac, n=28, postherpetic
  neuralgia and CRPS"; §4.11.6 the CRPS intradermal botulinum trial as the controlled test of the route; §4.17.1
  "refractory focal neuropathic pain — a mix of postherpetic neuralgia, painful diabetic neuropathy, chronic
  post-surgical pain, complex regional pain syndrome and vulvodynia"), and the D067 searches included "complex
  regional". On that scope Strauss 2015 is a placebo-controlled trial with a pain measure in an established pain state,
  so the eight findings now rest on it (paper_id "", pmid 26270587, quote from its cached abstract), with Flondell 2017
  and 2024 named in each corrected wording and note. All stay low: CRPS I does not meet the IASP definition of
  neuropathic pain (ambiguity), and every one of these trials put the cream on the forearm, so no verdict or rank
  change follows.

## 5. Not reached, and instructions found inside documents

- Not reached (no free copy, not attempted behind a wall): the journal versions of Strauss 2015 (LWW) and Lundborg 2010
  (Wiley); Levine 1993's full text (JBJS) — its item content was taken from the free full texts of Multanen 2020 (PMC)
  and Leite 2006 (PMC), and the standard item list of the published instrument. Strauss 2015's full text was read in
  its free reprint in the first author's dissertation (German National Library); nothing was bought, no login used.
- Not fetched in Notion: sibling EMLA product rows whose group representative carried no absence sentence (listed in
  section 4); Health History entries on "brain plasticity" (personal entries, not literature).
- Instructions inside documents: none in the paper, the abstracts, the full texts or the Notion pages. Tool-level
  notices only: the PubMed connector's "important legal notice" asking for PubMed attribution with DOI links, and a
  Firecrawl hint that its account is low on credits — neither is document content, both noted here for completeness.
- Content-filter stops: none.

## 6. Final s2check (python3 pm_work/tools/s2check.py S-686-43)

card: no "!!"; "??" only for allowed figures (study statistics, scale units, patient percentages, a two-point distance,
and the frequency the exception allows). claim_updates 4 items, 4 quotes found, 0 not found ("??" only the scale-unit
change in D067's reason and the allowed frequency in D066's reason). extra_studies 9 items, 9 abstract quotes found,
0 not found. notion_findings 8 items, 8 quotes found, 0 not found. All JSON files load.
