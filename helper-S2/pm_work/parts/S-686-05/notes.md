# S-686-05 Cui 2017 (advance access 2016): working notes

Filter rule kept for this paper: the regimen's numbers (amount of steroid, points per session, number and spacing of
sessions, total volume per session) appear only in the paper card and in the `reason` of C028 and D071, each as one short
sentence of what the study did. How the mixture was made up (its strengths and proportions) is written nowhere; it is
"a local anaesthetic–steroid mixture" with [dose figure omitted]. These notes carry no regimen figures.

## 1. Right-paper check

- PDF: `papers/S-686-05 - Cui 2017 - Effect of Repetitive Intracutaneous Injections with Local Anesthetics and Steroids
  for Acute Thoracic Herpes Zoster.pdf`, 7 PDF pages. Text: `texts/S-686-05.txt` (reading order plus layout view),
  readable, no OCR needed. Extraction oddities: "=" appears as "¼", "+" as "þ", "±" as "6", "≥" dropped (e.g. "VAS  4").
- PDF page 1 header: "Pain Medicine Advance Access published August 4, 2016 / Pain Medicine 2016; 0: 1–7 /
  doi: 10.1093/pm/pnw190". Title "Effect of Repetitive Intracutaneous Injections with Local Anesthetics and Steroids for
  Acute Thoracic Herpes Zoster and Incidence of Postherpetic Neuralgia". Authors Ji-zheng Cui, Xiao-bao Zhang, Pin Zhu,
  Zhi-bin Zhao, Zhu-sheng Geng, Yun-hai Zhang, Liang Tian, Heng-fei Luan, Ji-ying Feng (First People's Hospital of
  Lianyungang, Jiangsu, China). This matches the request (PMID 27492741, DOI 10.1093/pm/pnw190). Josh's person_note:
  the PDF is the 2016 advance-access version of the 2017 issue article; same DOI, title and authors. Right paper.
- Whole paper read: abstract, introduction, methods, results, Tables 1–4, Figure 1 (rendered PDF page 3 at 110 dpi:
  a dermatome chart with the axillary, midclavicular and subscapular lines and the T4–T6 band marked; it shows no
  individual injection points), discussion, limitations, conclusions, references 1–28.
- What the paper is: a single-centre randomised trial (China, July 2010 to June 2013) in 96 randomised adults aged 50–80
  with acute thoracic herpes zoster within 7 days of rash onset (93 completed: 47 intracutaneous, 46 control). Control =
  standard treatment (oral acyclovir plus tramadol as rescue). Intervention = the same plus repetitive intracutaneous
  injections of a local anaesthetic–steroid mixture (ropivacaine with methylprednisolone) along the midclavicular,
  axillary and subscapular lines of the affected dermatomes and into areas of eruption or pain. Outcomes: VAS pain,
  duration of pain and of eruption, PHN incidence at 1, 3 and 6 months (PHN = any pain related to the outbreak),
  EuroQol VAS, tramadol use, side effects.
- The steroid is METHYLPREDNISOLONE, not dexamethasone (PDF pages 2, 4, 5 and 6). Regimen numbers: in the card only.
- Internal inconsistencies (design facts, no dose figures):
  - Called "a prospective randomized placebo-controlled clinical trial" (p2) and "this randomized, placebo-controlled
    study" (p4), but the control arm as described received standard treatment only; no placebo or sham injection is
    described. Assessor blinding: "all follow-up was conducted by a second blinded doctor" (p2); the injecting doctor
    was not blinded; patient blinding is not described.
  - The abstract says "Ninety-three patients ... were randomly assigned"; the results say 96 were randomised (48 per
    arm), 93 completed. The sample-size paragraph says "98 patients were included".
  - The methods say side effects were recorded, but the results describe them only in words (injection pain the most
    common; bruising in some, especially older patients; no abscesses, cutaneous atrophy, scarring, etc.); only
    drowsiness and nausea/vomiting are counted per arm (Table 1, Table 3 text).
  - Number of injection points per session is not stated; it is implied by the per-point volume range and the fixed
    total volume per session (see card).
  - Limitations sentence prints "the frequency of rejection" (both views; probably meant "injection").

## 2. Claim screen (all 320 claims, masked viewer `pm_work/tools/claims_view.py`)

Regexes run with `claims_view.py grep` (hits in brackets):
- `27492741|pnw190|\bCui\b` (2: D070, D071 — Cui appears in their reason/records); `herpe|zoster|shingles|postherpetic|\bPHN\b` (18);
  `intracutaneous` (7); `steroid|methylpred|triamcinolone|dexameth|glucocortic` (14); `ropivacaine` (22); `mesotherap` (2);
  `repeated|repetitive|weekly|session` (32); `world literature|entire|eight papers|only (randomi[sz]ed|controlled|trial)|no (randomi[sz]ed|controlled) trial` (28);
  `(intradermal|wheal|infiltrat|cutaneous).{0,80}(trial|randomi|neuropath)|(trial|randomi|neuropath).{0,80}(intradermal|wheal|infiltrat|cutaneous)` (36).
- The masked `show` view was read for: C028, D071 (own question); D070, D072, T02, A054, D029, D033, D027, D026, D020,
  C023, D019, C025, C029, C001, C047, D032, D066, D067.

Kept (entries written):
- C028, D071: own question (both stay narrowed; regimen answered in the card and the two reasons only).
- D029 (other-claim, refuted -> refuted): Cui 2017 calls itself "placebo-controlled" but has no saline/sham arm; adds no
  saline-controlled trial; the claim's records already list it as "no saline arm" — the full text confirms that.
- D033 (other-claim, narrowed -> narrowed, uncertain stays): Cui 2017 documented no skin numbness, so it does not count
  among the later reports that meet "demonstrably numbed"; the narrowing rests on other sources (Mülkoğlu: S-686-18).
- D070 (other-claim, refuted -> refuted): Cui 2017 (and Cui 2018) are acute zoster, not chronic pain; the current
  proposed wording lists Cui 2018 as chronic-pain evidence — wording corrected.
- D072 (other-claim, confirmed -> narrowed): absence holds (no clearance measurement), but the clause that the published
  series work to the page's floor ([dose figure omitted]) is contradicted by Cui 2017's more closely spaced sessions (and Nguyen 2021, extra study).
  D072's subject ("the safe interval between sessions") is close to a dose-frequency subject; I judged it because two
  earlier workers (S-686-07, S-686-42) judged it as a literature claim, and I wrote no interval figure outside the card
  and the D071 reason.
- Extra-study entries (from PubMed searches prompted by Cui; none in its reference list): A054 (Xu 2013, confirmed ->
  refuted); D072 (Nguyen 2021, -> narrowed); D026, D020, T02 (Xiao 2010, narrowed -> narrowed); D032 (Kim 2021,
  narrowed -> narrowed).

Read closely and dropped:
- A054 for Cui 2017 itself: add-on design (both arms on the same systemic treatment), so Cui alone confirms; folded into
  the Xu 2013 entry's reason instead of a separate entry.
- D020, D026, D027 (dummy/sham-controlled durable-effect claims): design element is placebo/sham-controlled; Cui 2017 had
  no dummy injection despite its "placebo-controlled" label, so it cannot match. (Xiao 2010 entered as an extra study.)
- D032: Cui 2017 is a trial, not a systematic analysis (Kim 2021 entered as an extra study).
- T02: Cui's injections were not anaesthetic-only, population acute (Xiao 2010 entered as an extra study).
- C023, D019 (dexamethasone/adjuvant + LA, outcome duration of skin anaesthesia): Cui used methylprednisolone and
  measured no anaesthesia duration; no LA-alone arm, so the steroid's effect is not isolated. Dropped.
- C025 (magnesium), C029 (drugs on the adjuvants page in neuropathic leg skin), C013, C022, C024, C026, C030: other drugs
  or other outcomes. Dropped.
- C001 (botulinum grid in allodynic skin): different drug. Dropped.
- C047 (intradermal LA duration in neuropathic skin): Cui measured no anaesthesia duration. Dropped.
- D015 (repeated injection over months in fibre-depleted skin): Cui's course was one week; skin outcomes reported only
  as "no cutaneous atrophy or scarring encountered". Dropped.
- D036 (head-to-head of two LAs), D040, D044, D055 (ester), D063 (procaine), D066/D067 (topical lidocaine-prilocaine;
  Herr 2002's cream arm is acute zoster and not placebo-controlled, so it decides neither), D031/D030/D051 (SFN only),
  C046/C075 (nerve-fibre measurement), A041/A044/A049/A059/A066, C004/C011, E0xx: no overlap. Dropped.

Filter-rule skips (counted, not judged):
- Safe Doses Of Intradermal Analgesics: 4 claims not tested: dose or toxicity subject (D069, D073, D074, D075). Cui 2017
  measured no plasma level, so it would not bear on D069 in any case.
- adjuvants-without-a-vasoconstrictor: 1 claim not tested: dose subject (C021).

## 3. PubMed (connector; eutils blocked) — every search and lookup

Searches (all cached with pmcache.py; count = PubMed total):
1. `Manchikanti[Author] AND Hirsch[Author] AND "epidural steroid" AND neurological complications AND 2015[pdat]` — 1 (25795154, ref 16).
2. `Herr H[Author] AND (postherpetic OR zoster)` — 1 (12378018, ref 17).
3. `dexamethasone AND (intradermal OR intracutaneous OR intra-cutaneous OR "subcutaneous injection" OR "local infiltration" OR "local injection") AND (zoster OR postherpetic)` — 1 (35793178: Li 2022, dexamethasone into the Gasserian ganglion with pulsed radiofrequency; not a skin route).
4. `(clonidine OR dexmedetomidine OR magnesium OR buprenorphine) AND (intradermal OR intracutaneous OR intra-cutaneous OR "subcutaneous injection" OR "local infiltration") AND (zoster OR postherpetic)` — 0.
5. `(intracutaneous OR intra-cutaneous OR intradermal OR "subcutaneous injection" OR "subcutaneous injections" OR "local infiltration") AND (zoster OR postherpetic) AND (ropivacaine OR lidocaine OR bupivacaine OR "local anesthetic" OR "local anaesthetic" OR "local anesthetics")` — 23. All 23 records read (titles/abstracts):
   39484052 Wang & Lin 2024 meta-analysis, subcutaneous botulinum toxin in Chinese PHN (14 RCTs; subcutaneous, not intradermal);
   39057822 Lim 2024 Singapore zoster guideline review (mentions subcutaneous or intracutaneous LA+steroid injection);
   34593669 Kim 2021 NMA (extra study, D032); 33855194 Nguyen 2021 (extra study, D072);
   32524145 Dai 2020 ultrasound-mediated lidocaine/capsaicin vs intradermal lidocaine in zoster allodynia — RETRACTED, not used;
   31151330 Lin 2019 review (already in D032 records); 29153295 Cui 2018 (sister trial; already in records);
   28727702 Ni 2017 RCT, standard therapy vs plus subcutaneous triamcinolone + lidocaine in acute zoster (no placebo injection; schedule not in abstract; add-on);
   27777201 Cui 2016 (Chinese) RCT, [dose figure omitted] course of intradermal methylene blue + lidocaine vs intradermal lidocaine in elderly acute zoster (already in T02 reason);
   27492741 Cui 2017 (this paper); 26815265 Riopelle 2016 case letter; 26814241 Xu 2016 and 26200815 Xu 2015 RCTs, local methylcobalamin + lidocaine vs IM methylcobalamin + local lidocaine (lidocaine in all arms);
   24363852 Min 2013 epidural port case reports; 24196971 Xu 2014 RCT, TENS + local cobalamin / lidocaine / both in PHN (no systemic or placebo arm);
   23566267 Xu 2013 RCT (extra study, A054); 22004501 Puri 2011 modified Jaipur block series in PHN (subcutaneous LA + methylprednisolone, repeated injections; intervals not in abstract);
   21134121 Xiao 2010 RCT (extra study, D026/D020/T02); 16300701 Amjad 2005 RCT, triamcinolone + lignocaine vs lignocaine alone by local infiltration in PHN, [dose figure omitted] injections at intervals of [dose figure omitted] (already in T02 reason; consistent with the page's floor);
   16013891 Hempenstall 2005 (ref 15); 10776191 Edwards 1999 review of systemic lidocaine; 8219524 Devulder 1993 case report (subcutaneous lidocaine infusion); 3098751 Stadtner 1986 letter, intradermal Xylocaine for acute zoster (no abstract).
Lookups: `lookup_article_by_citation` for refs 1, 3-15, 18-28 (results in the card); ref 2 (Miller 1993, Rev Med Microbiol) not looked up (not a PubMed journal; epidemiology). `get_article_metadata` read for 27492741 (this paper: Pain Med 2017;18(8):1566-1572), 7203770, 992927, 9521026, 12378018, 29153295, 35480541 (Zhang 2022 meta-analysis, 10 RCTs of LA+steroid injection for PHN prevention), 35793178, 11087880, 16427490, 24528531, and the 23 hits above. `get_full_text_article` PMC8494957 (Kim 2021): reference numbers stripped in the PMC text, so the included-trial list could not be matched to Cui 2017.
Cached abstracts (pmcache.py article): 7203770, 992927, 12378018, 9521026 (no abstract), 23566267, 33855194, 21134121, 34593669. Authors lists were shortened to the first author when pasting; titles and abstracts verbatim. Cui 2018's abstract (regimen figures) was read but not cached: nothing is quoted from it; its title in the claims' records carries the point used (acute zoster).

## 4. Notion (read-only: notion-search and notion-fetch only)

Searches (page_size 25; count = results returned):
1. "Cui 2017 intracutaneous injections herpes zoster" — 20 (no page names Cui 2017; candidates: Results, SFN routing analysis, Procaine, Relief that outlasts the block, product rows).
2. "27492741" — 25 (all unrelated semantic matches; no page holds the PMID per search — to be checked by fetch on the pages below).
3. "postherpetic neuralgia intradermal injection steroid" — 20 (Reference; Results; capsaicin/EMLA product rows; intradermal botulinum session row).
4. "Cui ropivacaine methylprednisolone" — 20 (Reference shows other Cui authors, S265 and S390; ropivacaine product rows say "no wheal study of ropivacaine with a pain outcome exists").
5. "zoster intracutaneous local anaesthetic steroid trial postherpetic neuralgia prevention" — 19.
6. "systemic drug compared with local anaesthetic infiltration protocol" — 14 (List Of Alternative Treatments holds A054's sentence; a Health Pages - Meta entry holds T02's sentence as its title).

Fetches (as of = page version; truncation checked on every fetch):
- adjuvants-without-a-vasoconstrictor, https://app.notion.com/p/3d310b7903aa81fbb5b9e999637c362a, as of 2026-10-02T03:14:20.685Z,
  95,940 chars, no truncated / unknown-block flags. No mention of Cui, zoster, herpes, intracutaneous or methylprednisolone.
  C028's sentence stands verbatim in "What has no source": "Any dose of clonidine, dexamethasone, dexmedetomidine,
  magnesium or buprenorphine validated for repeated intradermal injection in anyone, for any indication." Cui 2017 (a
  methylprednisolone trial) leaves it accurate, so no finding.
- Safe Doses Of Intradermal Analgesics, https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7, as of
  2026-10-02T03:13:58.754Z, 65,027 chars, no truncation flags. Searched only (masked viewer); its ceilings were not copied
  (count only). No mention of Cui, zoster or intracutaneous injection. Sentences relied on (figures masked):
  - "What has no source": "The safe interval between sessions on any of these agents. [dose figure omitted] is the floor
    the published series work to, and it rests on those series' schedules rather than on a clearance measurement." The
    page names no series here, so it reads as a general statement about published schedules -> finding F01 (Cui 2017's
    sessions were more closely spaced; Nguyen 2021 consecutive-day).
  - "What has no source": "That any of these maxima is the right ceiling for repeated intradermal wheals. Every figure in
    the table is a single-procedure infiltration or nerve-block convention. No label, and no study, addresses a session of
    dozens of [dose figure omitted] deposits repeated weekly over months." Cui 2017 leaves it standing (a short course, not months)
    -> no finding.
  - Naropin entry "Limits": "the infiltration figures are surgical-field figures, not cutaneous-wheal figures, and no study
    of cutaneous or subcutaneous ropivacaine infiltration exists in any chronic pain condition." Already refuted by Lemos
    2010 (main session, D070); Cui is acute zoster and adds nothing new here -> no finding of mine.
  - "What is still unknown": the plasma-level point (no published study of wheal therapy has drawn plasma levels) — Cui
    2017 drew none either -> no finding.
- Relief that outlasts the block, https://app.notion.com/p/3d310b7903aa811cb51bcca149b3de73, as of 2026-10-02T03:14:06.492Z,
  76,085 chars, no truncation flags. No mention of Cui, intracutaneous zoster trials or methylprednisolone. Sentences read:
  - "The durable effect is real, it has been measured against a dummy injection exactly once in neuropathic pain, and it
    fades." (D026; Xiao 2010 extra-study entry covers it; no separate finding, as it would only repeat the claim update.)
  - Vlassakov 2012 annotation: "Neuraxial blocks, sympathetic blocks and named peripheral nerve blocks were excluded, as
    were migraine, complex regional pain syndrome, herpes zoster under three months, visceral pain, cancer pain and acute
    postoperative pain." -> added to the D033 entry's reason (acute-zoster trials fall outside the eight-paper criteria).
  - "Eight papers is the entire world literature on cutaneous anaesthesia for neuropathic pain in which the skin was
    demonstrably numbed." (D033; Cui adds nothing against it; no finding.)
  - "Villamizar Olarte and Rojas de Rangel, 2017 ... The only saline-controlled trial of intradermal papules found." and
    "The Colombian trial is the only attempt and stopped at 21 days." (D029; Cui 2017 has no saline arm; no finding.)
  - "Here is what nobody else has run." list (Kastelik 2025 S3 analysis, Imamura 2016, Villamizar Olarte 2017): Xiao 2010
    is postherpetic neuralgia, not nerve injury, so it does not contradict the Kastelik item; no finding.
- List Of Alternative Treatments For SFN (Not Including Nerve Growth), https://app.notion.com/p/1d410b7903aa8050b4f4fb12508d2862,
  as of 2026-09-26T18:23:49.097Z, 79,250 chars, no truncation flags. No mention of Cui, zoster or methylcobalamin. Last
  bullet of its unknowns: "Any comparison of these drugs against the intradermal wheals he already uses. No trial has
  ever compared a systemic drug against a local-anaesthetic infiltration protocol in this or any neuropathy." The bold
  item ("these drugs" = the page's systemic neuropathic-pain drugs) stands; the second sentence generalises to any
  systemic drug and any neuropathy, which Xu 2013 contradicts -> finding (extra-study based, low).
- Health Pages - Meta entry "No controlled study tests anaesthetic-only intradermal wheals for chronic neuropathic pain, and
  none exists in small fibre neuropathy; the one protocol found with its parameters and an outcome is uncontrolled, in
  notalgia paresthetica", https://app.notion.com/p/3da10b7903aa8123b623fcaad4241eea, as of 2026-09-24T03:29:24.240Z, blank
  body, properties only. Its receipt lists Amjad 2005 and "Cui 2016 (PMID 27777201) and similar acute-zoster trials use
  intradermal lidocaine only as a co-intervention alongside valaciclovir or methylene blue and do not isolate the
  anaesthetic". The Finding is precise to intradermal wheals; Xiao 2010 (subcutaneous) and Cui 2017 (steroid
  co-injected, acute) leave it accurate -> no finding. (Meta entries are not edited by anyone but Josh in any case.)
- Five ropivacaine product rows (Buying Decisions & Info), all with Intended Purpose "Intradermal anaesthetic wheals for
  burning pain from small fiber neuropathy", Decision "Needs More Research", Met Intended Purpose "Kinda", each saying in
  Why and the body Verdict "no wheal study of ropivacaine with a pain outcome exists, so its evidence [for the purpose] is
  only indirect, from one uncontrolled [study of lidocaine wheals / lidocaine study]", in Why For Purpose "No wheal study of
  ropivacaine with a pain outcome is indexed in PubMed" (La Paz [dose figure omitted] row; Curitek; both Vitau rows) or
  "no wheal study of ropivacaine with a pain outcome exists, and none in small fibre neuropathy" (La Paz higher-strength
  row), and in "What would change this": "A wheal study of ropivacaine with a pain outcome, in any neuropathic pain
  condition, would settle the verdict." Product strengths and amounts on these rows were not copied.
  - Ropiconest — Farmacia La Paz (lower strength), https://app.notion.com/p/3e010b7903aa81f1b482c79e7537bb8b, as of 2026-09-27T06:02:01.494Z.
  - Ropiconest — Farmacia La Paz (higher strength), https://app.notion.com/p/3e010b7903aa81db8c31e4a679616015, as of 2026-09-27T06:19:42.330Z.
  - Ropiconest — Curitek, https://app.notion.com/p/3e010b7903aa8147adc8f9881ba7856e, as of 2026-09-27T06:19:06.629Z.
  - Naropin — Vitau, https://app.notion.com/p/3e010b7903aa81ac9405ef7f25d76c21, as of 2026-09-27T06:16:15.263Z.
  - Ropiconest — Vitau, https://app.notion.com/p/3e010b7903aa81a5ac8fc0ebfff97715, as of 2026-09-27T06:20:19.898Z.
  None of the five fetches was truncated (single-page JSON returned in full). Cui 2017 is a PubMed-indexed randomised
  trial (MeSH "Injections, Intradermal", "Ropivacaine") of repeated intracutaneous injections of ropivacaine mixed with
  methylprednisolone, with pain outcomes (VAS, duration of pain, PHN incidence) in acute herpes zoster; Cui 2018 is a
  single intracutaneous injection of the same mixture against saline. So the absolute absence is overstated; the caveats
  (steroid co-injected; acute zoster, not established neuropathic pain or small fibre neuropathy) go in the corrected
  wording. Findings F02-F06, one per row; F03-F06 repeat F02 at further locations.
- Ropivacaine Wheals (tested by session S1; findings only), https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e, as of
  2026-10-02T03:14:26.511Z, 399,446 chars, no truncation flags. Searched with the masked viewer. No mention of Cui 2017,
  Cui 2018, ropivacaine-with-methylprednisolone or "intracutaneous" zoster trials. Sentences relied on (figures masked):
  - Section 13, gap 1: "Nobody has measured neuropathic pain relief from an intradermal ropivacaine wheal at any
    concentration — but the gap is a PARTIAL one and this page previously stated it too absolutely." Its search list:
    "Cui 2016 and similar acute-zoster trials use intradermal lidocaine as an active control or co-intervention, always
    alongside valaciclovir, methylene blue, corticosteroids, methylcobalamin or nerve blocks. None isolates the anaesthetic
    effect." Then: "What has been reported only once is an anaesthetic-only wheal protocol with per-wheal volume, spacing,
    a repeated-session schedule and a pain outcome: [Mülkoğlu 2020] ... — and nothing at all in small fibre neuropathy."
    -> F07 (the lidocaine-only summary misses the two ropivacaine trials; the "anaesthetic-only" sentence is accurate).
  - Section 13, gap 2: "Nobody has used ropivacaine wheals for small fibre neuropathy. No trial exists." -> stands.
  - Section 13, item 8: "Whether repeated ropivacaine over months does anything to skin that has already lost fibres.
    Unstudied, exactly as for repeated epinephrine." -> stands (Cui's course was one week, no fibre measurement).
  - 12.3a: "One wheal protocol with a local anaesthetic and a pain outcome has been published: [Mülkoğlu 2020, figures
    masked] ... The nearest randomised design is intradermal botulinum toxin A for painful diabetic neuropathy" -> F08.
  - 12.3a also lists "Xiao 2010, a post-herpetic neuralgia trial using subcutaneous botulinum toxin A ... against ...
    lidocaine and saline" as an entry point — so the record knows Xiao 2010 (as a botulinum trial).
- Comparing the injectable local anesthetics for intradermal wheals, https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b,
  as of 2026-10-02T03:14:02.626Z, 105,800 chars, no truncation flags. No Cui / zoster / intracutaneous. Holds D020 ("It has
  been tested against a dummy injection once, in neuropathic pain, and it held.") and D015 ("What does repeated injection
  over months do to skin that has already lost nerve fibers? Unstudied for every drug here.") as tested; Xiao 2010 covers
  D020 through the claim update; no separate finding.
- The intradermal wheal literature nobody cites, https://app.notion.com/p/3d410b7903aa8107a042d4e7f6540c1a, as of
  2026-10-02T03:14:04.610Z, 76,264 chars, no truncation flags. No Cui / zoster; C047 sentence ("Every subject in every study
  on this page was a healthy volunteer") stands. No finding.
- mepivacaine-wheals (S1), https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185, as of 2026-10-02T03:14:08.315Z, 67,421
  chars: no hits for Cui / zoster / intracutaneous / steroid / pain outcome. No finding.
- bupivacaine-wheals (S1), https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d, as of 2026-10-02T03:14:18.695Z, 84,250
  chars: only the Howe 1994 and Hanna 2009 injection-pain passages matched; nothing Cui bears on. No finding.
- Anaesthetics, https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492, as of 2026-10-01T03:07:38.200Z, 55,346 chars: no
  hits (Cui, zoster, intracutaneous, pain outcome, "no wheal"). No finding.
- 2 — Reference (source register S1–S457), https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65, as of
  2026-10-01T02:05:48.095Z, 1,279,938 chars (saved to file, searched with Python; the word "truncated" occurs only in page
  prose, no truncation metadata). Cui 2017 is not in the register (S265 is Cui Y 2016, burning mouth; S390 is Ju ZY ... Cui
  HS 2017, acupuncture Cochrane). No PMID 27492741 or DOI pnw190. Sentences relied on:
  - 3.2: "No randomised trial of cutaneous or subcutaneous local anaesthetic infiltration for established small fibre
    neuropathy was located, for lidocaine, procaine or ropivacaine." (stands) ... "two further randomised trials exist in
    adjacent indications" ... "Ropivacaine: the trial literature is perioperative prevention of chronic pain, not treatment
    of established pain, and is mixed — negative in 236 breast-surgery patients (P=0.37), weakly positive in 52 craniotomy
    patients." -> F10.
  - 4.9: "No evidence exists on local-anaesthetic wheal therapy in small fibre neuropathy specifically, by any design, and
    no study of cutaneous or subcutaneous ropivacaine infiltration exists in any chronic pain condition." -> second location
    of D070's sentence (main session's Lemos 2010 refutation covers it); noted in F10, not a separate finding.
  - 4.9: "Repeated infiltration is cumulative, not diminishing. Every series reporting the question escalates rather than
    tapers ..." -> Amjad 2005's lidocaine-only arm fell from 6 to 12 weeks, but measured after the course ended; not
    decisive; no finding.
  - 7.2.4: "No randomised trial of cutaneous or subcutaneous local anaesthetic infiltration for established chronic
    peripheral neuropathic pain was located for lidocaine, procaine or ropivacaine, so there is no published duration of
    analgesia per session ..." -> F11 (Xiao 2010; Amjad 2005 named from the claims record).
  - The section 4.9 passages around these sentences carry label maximum doses and toxicity text; read masked, not copied.
- 1 — Product Guide, https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f, as of 2026-10-02T03:14:29.224Z, 599,993 chars
  (saved to file, searched with Python; no truncation metadata). Cui 2017 is not cited. Sentences relied on:
  - Injectables, opening: "One finding governs the whole section. No randomised trial of cutaneous or subcutaneous local
    anaesthetic infiltration for established chronic peripheral neuropathic pain was located for lidocaine, procaine or
    ropivacaine. There is no published duration of analgesia per session for any of them in this condition, which means
    there is no measured baseline for a topical substitute to be compared against." -> F12 (Xiao 2010; high because the
    section's rankings are said to rest on it).
  - Ropiconest entry: "The ropivacaine trial literature is perioperative prevention of chronic pain rather than treatment
    of established pain, and it is mixed: negative in 236 breast-surgery patients, weakly positive in 52 craniotomy
    patients." -> F13 (second location of F10).
  - Ropiconest entry header "Magnitude UNKNOWN by this route in this condition · Duration not documented in this
    indication · Evidence NONE" (small fibre neuropathy) -> stands.
- 5 — Soft ground in these documents, https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403, as of 2026-09-26T18:26:13.509Z,
  returned in full (no truncation). Nothing on Cui, zoster, intracutaneous injection or ropivacaine trials. No finding.
- What is still unsettled across these pages, https://app.notion.com/p/3d410b7903aa819f8300e976a62577db, as of
  2026-09-26T18:23:10.973Z, 61,415 chars (nested save format; the word "truncated" occurs only in page prose about registro
  numbers). No Cui. Sentences relied on: "The paper is paywalled and its eight primary references are the closest thing that
  exists to evidence for repeated intradermal wheals as a technique in use." and, under The recommendation, "A second
  paywalled paper's reference list is the closest thing that exists to evidence for repeated intradermal wheals as a
  technique" -> F14. Its cell-culture toxicity figures (lethal concentrations) were seen masked-in-part and not copied.
- What was searched for and does not exist, https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82, as of
  2026-09-27T00:27:49.877Z, 64,683 chars, no truncation flags. Entries on topical procaine, botulinum field size, geranium
  oil; nothing on zoster skin-injection trials, repeated sessions or ropivacaine. No finding.
- What transfers from diabetic neuropathy trials to idiopathic small fiber neuropathy, https://app.notion.com/p/3d410b7903aa813681e9c27892149a17,
  as of 2026-09-26T18:27:17.888Z, 99,131 chars: one hit (a list of treatment page names). No finding.
- Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection Routing Analysis, https://app.notion.com/p/39410b7903aa8046b3eef25af516245f,
  as of 2026-09-26T18:19:51.310Z, 100,336 chars. Homeopathic injectables; "one real supportive trial" is the MOZArT knee
  trial; it repeats the Villamizar Olarte 2017 "only placebo-controlled trial of intradermal papules located" sentence (a
  second location of D029's refuted sentence, covered by the main session's Loughnan 2009 refutation; Cui adds nothing).
  No finding of mine.
- Results (neural therapy summaries), https://app.notion.com/p/32a10b7903aa804bac71f3523e07a298, as of 2026-09-13T07:38:52.775Z,
  returned in full. Entry "A Randomized Controlled Trial of a Multifaceted Integrated Complementary-Alternative Therapy for
  Chronic Herpes Zoster-Related Pain": "Main Authors: Stefan Weinschenk, et al." / "56 patients ... were randomized. The
  immediate treatment group received [dose figure omitted] Procaine Neural Therapy [dose figure omitted]." / "Pain scores
  (VAS) dropped significantly from 7.2 to 2.3 within the first three weeks." / "This provides objective proof that repeated
  Procaine blockades can force a long-lasting 'reset' ..." PubMed 22502623 (get_article_metadata, cached): Hui F, Boyle E,
  Vayda E, Glazier RH, Altern Med Rev 2012; 59 randomised; four-part CAM package; wait-list control -> F15, F16.
- Further searches: "methylcobalamin local injection herpetic neuralgia lidocaine" — 17 results (Studies; Versatis, EMLA
  and Anestecin product rows; B12 & B9; Injected Hydroxocobalamin page; German Medicines page); "triamcinolone injection
  herpes zoster skin" — 20 results (Results; Vitamin C; routing analysis; Comparing; Health History entries; product rules) —
  no page mentions Epstein, Chiarello or intralesional triamcinolone in zoster.
- Studies (B12 & B9), https://app.notion.com/p/31b10b7903aa80e1ac4bd02944509fc4, as of 2026-10-01T03:11:37.437Z, returned in
  full. Entry "2. Xu et al. (2013/2015) - Local vs. Systemic Methylcobalamin for Herpetic Neuralgia": "Patients were
  randomized to receive either local subcutaneous injections of methylcobalamin ([dose figure omitted]) plus lidocaine,
  intramuscular methylcobalamin, or oral methylcobalamin for [dose figure omitted]." ... "The incidence of postherpetic
  neuralgia was 1.1% at 3 months." -> F17 (Xu 2013 arms per its abstract; 1.1% is Xu 2016's figure). The page's B6 harm
  section and dose figures were not copied.
- Injectables still to try, https://app.notion.com/p/3d310b7903aa80d5a837cf30ed38c384, as of 2026-09-13T07:27:36.033Z: an index
  page (one mention of the Ropivacaine Wheals page). No finding.
- Injectables ruled out but not tried, https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5, as of 2026-10-02T03:14:22.080Z,
  72,962 chars: no hits for Cui / zoster / intracutaneous / steroid / pain outcome. No finding.
- Not fetched: "Prilocaine + Lidocaine" and "Procaine / Novocaine" treatment pages (their claims D053-D068 were screened in
  claims_all and none bears on Cui; searches did not surface zoster skin-injection statements on them); the Health History
  entries the searches surfaced (personal experiences, left alone per the brief).

Findings written (17): F01 Safe Doses (the stated inter-session floor; wrong-figure, medium); F02-F06 five ropivacaine product rows ("no
wheal study of ropivacaine with a pain outcome exists"; overstated, high); F07, F08 Ropivacaine Wheals gap 1 and 12.3a
(overstated, medium; S1's page, findings only); F09 List Of Alternative Treatments (A054 sentence, Xu 2013; overstated,
low); F10 Reference 3.2 ropivacaine anchor (overstated, medium); F11 Reference 7.2.4 (Xiao 2010; overstated, medium); F12
Product Guide injectables governing finding (Xiao 2010; overstated, high); F13 Product Guide Ropiconest entry (= F10,
medium); F14 What is still unsettled ("closest thing that exists"; overstated, medium); F15, F16 Results page (Hui 2012
misattributed to Weinschenk; package described as procaine alone, figures misread; citation-error and wrong-design,
medium); F17 Studies (B12) page (Xu trials merged; wrong-design, medium).

## 5. Not reached, problems, instructions found

- Chiarello 1998 (PMID 9521026): no abstract in PubMed and no free full text tried (paywalled journal); described in the card
  from Cui's own account only.
- Cui 2018 (PMID 29153295): abstract read, full text not needed.
- Kim 2021 (PMC8494957): full text read through the PubMed connector, but reference numbers are stripped, so its inclusion of
  Cui 2017 is inferred from the one-trial intracutaneous nodes, not read.
- Herr 2002 (PMC3054950) full text not read (abstract sufficed: decides no claim).
- Dai 2020 (PMID 32524145) is flagged "Retracted Publication" in PubMed; not used anywhere.
- Mülkoğlu 2020's full-text question belongs to S-686-18; D033's uncertainty is left for that worker.
- No content-filter stops. No instructions aimed at the reader/agent were found in the paper, the abstracts or the Notion
  pages (the Reference's "Own-use marker" notes are addressed to Josh's record-keeping, not to this work).
- Notion was used read-only throughout: only notion-search and notion-fetch were called.
