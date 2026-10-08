# S-686-18 — Mülkoğlu C, Nacır B. Notalgia paresthetica: clinical features, radiological evaluation, and a novel therapeutic option. BMC Neurol 2020;20:191. PMID 32416719, DOI 10.1186/s12883-020-01773-6

## 1. Right-paper check

- PDF: `papers/S-686-18 - Mülkoğlu 2020 - Notalgia paresthetica clinical features radiological evaluation and a novel therapeutic option.pdf`; text `texts/S-686-18.txt` (8 PDF pages, each in reading order and layout view). Text is clean born-digital extraction; no OCR needed.
- PDF page 1 header: "Mülkoğlu and Nacır BMC Neurology (2020) 20:191", "https://doi.org/10.1186/s12883-020-01773-6", title "Notalgia paresthetica: clinical features, radiological evaluation, and a novel therapeutic option", authors Cevriye Mülkoğlu and Barış Nacır. Matches papers_list.csv row (PMID 32416719, DOI 10.1186/s12883-020-01773-6, BMC Neurol, 2020, 8 pages). person_note column: empty.
- Right paper: yes. Whole paper read: abstract, background, methods, results, Tables 1–3, Fig. 1–2 legends, discussion, limitations, conclusion, declarations, references 1–33.

## Reading notes (what the paper does)

- Authors call the study "cross-sectional". 80 patients (45 NP; 35 dorsalgia without NP as a control group for the clinical/radiological comparison), outpatient PM&R clinic, Ankara, Aug 2018 – Jun 2019.
- Treatment part: lidocaine injections "planned for the 22 patients in the NP group" (p3); "Topical capsaicin was prescribed to the remaining patients in the NP group" (p3) — no results reported for the capsaicin patients and no lidocaine-vs-capsaicin comparison. 2 of 22 did not come to the second injection and were excluded; evaluation on 20 (p4–5). How the 22 were chosen is not stated. No randomisation, no blinding, no sham/saline arm. Authors: "We also did not have a control group with NP who did not undergo lidocaine treatment." (p7)
- Route/procedure (methods figures kept out of the notes; they are in the card only as the exception allows for sessions and spacing): lidocaine diluted with saline, given intradermally at pencil-marked points around the hyperpigmented patch and segmentally along the C2–T6 spinous processes; "Small bumps appeared on the skin." (p3). [dose figure omitted] (the session schedule is given in the card only).
- Outcomes: VAS-pain and VAS-pruritus (0–10) at day 0, week 2, week 4, month 3 (Table 3, p5); adverse effects "at the follow-up visits at the second and fourth weeks" (p5). Whether week-2/week-4 VAS was taken before or after that visit's injection is not stated; the results sentence says "After the third session of lidocaine injection, the VAS-pain and VAS-pruritus scores were significantly decreased at the second- and fourthweek follow-up" (p5), which does not fit the schedule (third session was at week 4).
- Sensory examination: a neurologic examination "for motor and sensorial functions" at enrolment (p3); hypoesthesia at baseline in 18/45 NP patients ([dose figure omitted]) (p4, Table 1) — a disease feature, not a post-injection finding. NO post-injection sensory testing (no pinprick, touch, threshold), no patient report of numbness, no record of the duration of the block. The words "numb", "anesthe/anaesthe" (other than "local anesthetic(s)"/"Topical anesthetics"/"therapeutic local anesthesia"), "pinprick", "sensory test" do not occur in any post-injection context (checked by grep, below).
- Novelty framing: title "a novel therapeutic option"; abstract: the literature has IV and topical lidocaine for NP, "We also investigated the effect of intradermal lidocaine injection" (p1). Authors cite their own 2018 case report (ref 12: Mülkoğlu, Nacir, Genç, Int J Dermatol 2018;57(9):e70–1, "neural therapy") of a 73-year-old man given local lidocaine injections into the upper back, VAS from 7 to 1 at week 2 (p2). They do not state that the 2020 study is the first; they frame the method as therapeutic local anaesthesia (neural therapy), citing Egli 2015 and Fischer 2003 (p7).
- Funding: "Not applicable." Competing interests: none declared (p7).

## 2. Claim screen (all 320 claims in common/claims_all.json, read through pm_work/tools/claims_view.py, masked)

Regexes run with `claims_view.py grep` (they search claim, elements, reason, proposed wording, review and evidence quote),
with the number of claims hit:
- `notalgia|M[uü]lko[gğ]lu|Nac[iı]r|32416719|12883-020|BMC Neurol` 3 (A091, D015, D033)
- `prurit|itch` 4 (C041, C045: their reasons mention intradermal studies that measured injection itch; E013, E014: a
  clove-oil pruritus trial in their reasons. None is about neuropathic itch or notalgia; dropped)
- `Vlassakov|eight papers|world literature|demonstrabl|numbed|numbness|skin anaesthesia|skin anesthesia|cutaneous an(a)?esthesia` 19
- `intradermal lidocaine|lidocaine wheal|intradermal (injection|anaesth|anesth)|intracutaneous|papule|quaddel|neural therapy|Huneke|mesotherap|Egli|Fischer L` 37
- `outlast|outlived|longer than the (block|...)|beyond the (block|duration)|...|durab|weeks of relief|months of relief|three months|3 months` 15
- `uncontrolled|case series|case report|open[- ]label|denominator|single[- ]arm|before[- ]after` 40
- `no (randomi[sz]ed |controlled |placebo[- ]controlled )?trial|never been trialled|...|never been tested|no study` 85
- `dilut|saline` 34; `dilut` 7; `buffer|bicarbonate|mix(ed|ing)? (with|fresh)|prepar` 13
- `capsaicin` 18; `intravenous lidocaine|lidocaine infusion|IV lidocaine|lidocaine patch|lidocaine plaster` 9
- `entrapment|dorsal ram|posterior ram|paravertebral|spinal nerve|radiculopath|cervical|epidural` 8
- `sessions|repeated (injection|wheal|session)|weekly|every two weeks|fortnight` 11
- `Egli|neural therap|Neuraltherap|Fischer` 5; cited NP authors `Chtompel|Cruz|Williams EH|Marcaine|Eisenberg|Andersen HH|Ansari|Maciel|Savk|Raison|Pagliarello` 0
- `zoster|postherpetic|PHN|Attal|Rowbotham|Cui ` 22

Read closely with `claims_view.py show` (sentence, elements, verdict, reason, records), with the decision:
- D033 (own question). Re-judged, see claim_updates.
- D015 (Comparing…, "What does repeated injection over months do to skin that has already lost nerve fibers? Unstudied
  for every drug here.", confirmed). KEPT as other-claim: its reason names Mülkoğlu 2020 as the closest study ("a
  [dose figure omitted] intradermal lidocaine series in notalgia paresthetica that measured only symptoms"). Full text confirms:
  [dose figure omitted] over a four-week course, VAS pain/itch only, no skin or nerve-fibre examination, no biopsy. Stays confirmed.
- T02 (job title claim, "No controlled study tests anaesthetic-only intradermal wheals for chronic neuropathic pain…",
  narrowed). KEPT as other-claim: Mülkoğlu is an anaesthetic-only (lidocaine in saline, no steroid) intradermal papule
  series in a chronic neuropathic condition, but without a comparison arm for the treatment, so it is one more
  uncontrolled study and does not change the verdict.
- C047 (wheal literature page, "Any of this literature in neuropathic skin…", duration of intradermal anaesthesia in
  neuropathic skin, confirmed) and D040 (Relief page, duration or vasoactivity of intradermal anaesthetic in neuropathic
  skin, confirmed). KEPT as other-claim: Mülkoğlu injected intradermal lidocaine into affected skin in a sensory
  neuropathy, the nearest candidate, but measured no duration of anaesthesia and no vasoactivity. Both stay confirmed.
- D026, D020 (one dummy-controlled test in neuropathic pain), D027 (only controlled positive durable trial used
  ropivacaine), D029 (only saline-controlled papule trial), D057 (one randomised trial in the field), D036 (head-to-head
  LA comparison on durability), D041 (treat one limb, observe the other), D042 (no contrasting citation), D043 (Ilfeld
  follow-on), D044 (session spacing comparison). Dropped: each turns on a controlled, randomised, sham, head-to-head or
  spacing-comparison design; Mülkoğlu has none of these (single uncontrolled lidocaine group; the capsaicin-prescribed
  remainder were not reported or compared). Its relief to three months is uncontrolled and does not bear on any of them.
- D030, D031 (SFN populations). Dropped: notalgia paresthetica is not small fibre neuropathy and the paper does not call
  it one.
- D032 (Vlassakov as the only systematic analysis). Dropped: Mülkoğlu is not a review.
- D034, D035, D037, D039, D053–D065 procaine claims (incl. D063 procaine duration in denervated skin). Dropped: procaine;
  Mülkoğlu used lidocaine and compared no anaesthetics.
- D038 (Gq anti-inflammatory action vs durable endpoint). Dropped: no mechanism or biomarker measured.
- D028 (out-of-scope). Dropped.
- A091 (suzetrigine; its reason lists a 2026 notalgia paresthetica case report). Dropped: suzetrigine, not lidocaine.
- A054 (no trial comparing a systemic drug with an LA infiltration protocol). Dropped: the only other NP treatment in
  Mülkoğlu is topical capsaicin, not a systemic drug, and no comparison was reported.
- C046, D013 (LA damage to skin nerve fibres), C075 (months of epinephrine wheals in denervated skin), C028 (adjuvant
  validated for repeated intradermal injection). Dropped: no histology, no epinephrine, no adjuvant.
- E006, E007, E009, E019, E027 (topical lidocaine claims). Dropped: Mülkoğlu cites one topical lidocaine-patch case
  (Cruz 2018) in NP, which is not SFN, HIV neuropathy or a capsaicin-course combination; it does not bear on them.
- C041, C045, E013, E014 and the remaining hits (A0xx device/regeneration claims, botulinum, menthol, articaine,
  prilocaine, epinephrine vasoactivity claims) came up on generic words (trial, sessions, saline, three months, …).
  Dropped: no overlap in drug, route, population, outcome or design.

Skipped under the filter rule (dose, toxicity, ceiling or recipe subject; text not written out, only counted):
- Safe Doses Of Intradermal Analgesics: 6 claims not tested: dose or toxicity subject (D069, D071, D072, D073, D074,
  D075). D069, D071 and D072 would otherwise touch Mülkoğlu's repeated intradermal lidocaine sessions; D073–D075 are
  epinephrine subjects that it does not touch. (D070 is ropivacaine-specific and was dropped for no overlap.)
- Comparing the injectable local anesthetics for intradermal wheals: 3 claims not tested: recipe (buffering) subject
  (D012, D017, D018).
- 💉 Lidocaine With Epinephrine Wheals: 1 claim not tested: recipe (mixing/dilution) subject (C091).
- prilocaine-wheals: 1 claim not tested: dose or toxicity subject (C071).
- No claim in the 320 has lidocaine-with-saline dilution as its subject (grep `dilut` hits: C009, C026, C078, C087,
  C091, C092, D033; only C091 is a preparation subject, counted above; D033 hit through its evidence quote).

## 4. Notion (read-only: notion-search and notion-fetch only)

### Fetch 1 — "⏳ Relief that outlasts the block — and whether the whole list is optimising the wrong thing"
- URL https://app.notion.com/p/3d310b7903aa811cb51bcca149b3de73 ; fetch says "as of 2026-10-02T03:14:06.492Z" (same as
  the version tested in claims_all.json); path Health / Health Pages; verification unverified. Result too large to show
  (76,940 characters), saved to a file and parsed as JSON; text 76,085 characters. No `truncated`, `unknown_block_count`
  or `unknown_block_ids` in the result: the text is complete.
- Searched the text for Mülkoğlu / Mulkoglu / Nacır / Nacir / notalgia / Notalgia / 32416719 / 12883: 0 hits. The page
  does not cite Mülkoğlu 2020 or mention notalgia paresthetica.
- Vlassakov: 7 mentions. The D033 passage (section "What the uncontrolled series claim, and what their denominators
  are"), verbatim (dose figures masked where present):
  - "**Vlassakov, 2012, in *Journal of Anesthesia & Clinical Research*.** The same author narrowed the question from
    nerve blocks to **skin** — the only systematic analysis of this reader's exact route in this reader's exact class of
    condition. Entry required a **demonstrated anaesthetic effect on skin**. Neuraxial blocks, sympathetic blocks and
    named peripheral nerve blocks were excluded, as were migraine, complex regional pain syndrome, herpes zoster under
    three months, visceral pain, cancer pain and acute postoperative pain."
  - "**A reference list of 369 articles reduced to 8 publications.**"
  - "**Eight papers is the entire world literature on cutaneous anaesthesia for neuropathic pain in which the skin was
    demonstrably numbed.** That is the size of the field. The "more than half" figure is stated without a denominator,
    the paper is paywalled, and the selection rule — the anaesthetic must have worked — can itself select for positive
    reports."
  - Same section, just before: "**Egli and colleagues, 2015, in *BMC Complementary and Alternative Medicine*.** **280
    referred refractory chronic pain patients** given procaine or lidocaine alone, [dose figure omitted]. … The authors state outright that **"the specific contribution of the intervention to these
    results cannot be determined"** and call for controlled trials." (Egli 2015 is Mülkoğlu's reference 29.)

## 3. PubMed (connector; eutils blocked, so pm.py cannot run). Cache written with pm_work/tools/pmcache.py

- get_article_metadata 32416719: Mülkoğlu C, Nacır B, BMC Neurol 2020;20(1):191, PMC7229619, DOI 10.1186/s12883-020-01773-6.
  PubMed indexes it with article types "Clinical Trial", "Journal Article" and MeSH "Cross-Sectional Studies". Saved as
  pm_work/cache/a_32416719.json with `--redacted`: the dilution recipe sentence and the spacing between injection points
  were replaced by [dose figure omitted]; the rest of the abstract is verbatim.
- search `Vlassakov KV[Author] AND Kissin I[Author]`: count 12, translation `(vlassakov, kv[Author] OR vlassakov
  kv[Author]) AND kissin i[Author]`. Only 21372279 (Vlassakov, Narang, Kissin 2011, Anesth Analg 112(6):1487-93,
  peripheral nerve blockade for neuralgias, 12 case reports/series) is on topic; the others are scientometric papers.
  Read its abstract (not cached; not quoted).
- search `Vlassakov[Author] AND (cutaneous OR skin OR infiltration OR topical)`: count 5 (34147158, 33988528, 28195898,
  26431146, 26297210; none from 2011–2013). search `Vlassakov[Author]` 2011–2013: count 3 (23797663, 23662765,
  21372279: two retrolaminar-block papers and the 2011 review). search `Kissin I[Author] AND (neuropathic OR neuralgia OR
  cutaneous OR skin)` 2010–2014: count 6 (25187736, 23874119, 23152698, 22494921, 21372279, 20185657); 22494921 is
  Kissin's 2012 letter "How does the lidocaine patch ([dose figure omitted]) relieve pain?" (no abstract). Conclusion: the 2012 cutaneous
  analysis is not in PubMed. (All four searches are cached via pmcache.py; the date-limited ones are recorded with the date range in the
  query text.)
- OpenAlex connector: W2332856010, "Cutaneous Anesthesia in Neuropathic Pain: Systematic Analysis", Kamen V. Vlassakov,
  J Anesth Clin Res 2012;3(3), DOI 10.4172/2155-6148.1000199, oa_status closed, referenced_works_count 0 (no reference
  list in OpenAlex). Its abstract (OpenAlex): "There are many reviews on topical local anesthetics that provide pain
  relief without skin anesthesia, the aim of this review is to analyze studies on neuropathic pain treated with
  cutaneous anesthesia. The reference list of 369 articles was reduced to 8 publications that met inclusion criteria
  (presence of anesthetic effect was a requirement). … With the single skin anesthesia treatment, both separately and
  collectively, the reviewed publications reported that more than half of the patients had complete pain relief, often
  lasting much longer (days or weeks) than the anesthesia."
- Full text of Vlassakov 2012 NOT reached: api.crossref.org and doi.org refused by the session's network policy
  (CONNECT 403, not retried or worked around); the Jina reader connector returned HTTP 401 for the DOI; ResearchGate
  (login/bot wall) not tried. So the identity of the eight included papers is unknown.
- get_article_metadata 10353509 (Attal 1999, Pain 81:203-9, EMLA in PHN, n = 11): "In the acute situation, EMLA produced
  an overall anaesthetic effect without significantly reducing spontaneous ongoing pain and mechanical allodynia.
  Repeated applications significantly reduced paroxysmal pain and both the dynamic and static subtypes of mechanical
  hyperalgesia." Cached (not redacted: no dose figures in it). Used in the D033 reason only.
- get_article_metadata 2594392 (Rowbotham & Fields 1989, PHN, local anaesthetic skin infiltration, 12 patients): read,
  not cached, not quoted.
- lookup_article_by_citation for Mülkoğlu's references (connector returns the PMID in the `key` field):
  1 Howard 2018 29243804; 2 Chtompel 2017 29151570; 3 Maciel 2014 25054742; 4 Low 2017 29180561; 5 Savk & Savk 2004
  15097973; 6 Cohen 2017 29188163; 7 Marcusson 1990 1980988; 8 Robbins StatPearls 29262015 (given in the reference);
  9 Shin 2014 24966642; 10 Ansari 2019/2020 30942103 (J Dermatolog Treat 2020;31(4):424-432, epub 2019; the paper cites
  it as "2019;3:1–9"); 11 da Cruz & Antunes 2018 30439740; 12 Mülkoğlu, Nacir, Genç 2018 29911324 (letter, no
  abstract); 13 Ellis 2013 23785628; 14 Bernhard 1997 9111839; 15 Raison-Peyron 1999 10461640; 16 Pagliarello 2017
  28646529; 17 Weber 1988 2831253; 18 Layton 1991 1934572; 19 Terzi 2016 28360775; 20 Savk 2005 15928634; 21 Alai 2010
  20349681; 22 Eisenberg 1997 9418774 (no abstract); 23 Pérez-Pérez 2011 22256623; 24 Andersen 2016 26848223; 25
  Zagarella 2016 26499931; 26 Sahhar 2018 28805241; 27 Fleischer 2011 21279307; 28 Williams 2010 19790177; 29 Egli 2015
  26115657; 30 Fischer 2003 14694543 (German); 31 Bahekar 2007 17967586; 32 Cornelissen 2009 19874535; 33 Fukai 2009
  20002756.
- get_article_metadata read for 29911324, 26115657, 29151570, 30439740, 19790177, 30942103, 9418774, 26848223, 14694543,
  19874535, 22256623, 29243804. Cached (verbatim, nothing to redact): 26115657 (Egli), 29151570 (Chtompel).
- None of the cited studies decides a claim (see section 2 and the card): the anaesthetic ones are case reports
  (Chtompel IV infusion; da Cruz topical anaesthetic plus exercises; Mülkoğlu 2018 local lidocaine injections, a letter
  without abstract; Williams 2010 a diagnostic bupivacaine block before surgery) or Egli's uncontrolled neural-therapy
  series, which the Relief page already cites accurately. extra_studies.json is therefore [].

### Notion searches (query → results; search used only to find candidates)
- "notalgia" (page_size 25) → 25 results: 1 Health Pages - Meta page (the T02 finding page, 3da10b7903aa8123b623fcaad4241eea)
  and 24 Buying Decisions & Info product pages (lidocaine, lidocaine-epinephrine dental cartridges, ropivacaine,
  procaine, articaine, Zingo, an intradermal botulinum toxin clinic session).
- "Mülkoğlu" (25) → 25 results, same set plus a few more product pages; "32416719" (25) → 25; "Mulkoglu" (50) → 30;
  "12883-020-01773-6" (50) → 50 results, of which only the product pages above and procain-Loges cite the DOI; the rest
  are unrelated hits on the digits (Health History guanfacine entries, a visa page, B6 pages, etc.). Union of pages that
  cite the paper: the Meta page and 37 product pages (listed in section 4b). No treatment page and no analysis page
  (Reference, Product Guide, open-question pages) came up for these queries; they are fetched and searched directly.

### Fetch 2 — Health Pages - Meta: "No controlled study tests anaesthetic-only intradermal wheals for chronic neuropathic
pain, and none exists in small fibre neuropathy; the one protocol found with its parameters and an outcome is
uncontrolled, in notalgia paresthetica"
- URL https://app.notion.com/p/3da10b7903aa8123b623fcaad4241eea ; "as of 2026-09-24T03:29:24.240Z"; returned inline; no
  truncated/unknown-block flags; the page body is blank and everything is in properties (Finding, Evidence / Receipt).
  This is the page of claim T02.
- Verbatim (methods figures masked): "WHAT A LATER SEARCH FOUND, 2026-09-22 (PubMed; full text read 2026-09-23): Mülkoğlu
  2020 (PMID 32416719, BMC Neurol, doi:10.1186/s12883-020-01773-6) diluted [dose figure omitted] lidocaine in [dose figure
  omitted] saline and injected it intradermally as [dose figure omitted] wheals at [dose figure omitted] intervals around
  the hyperpigmented patch and along C2–T6, in [dose figure omitted], in 22 people with notalgia paresthetica, a
  sensory neuropathy of the upper back with burning in about half. In the 20 evaluated, pain and itch VAS were lower at
  2 and 4 weeks and stayed lower at 3 months. There was no untreated control group, and no needle gauge or measured
  depth is given. It answers the first half of the finding as logged on 2026-09-12; the small fibre neuropathy half
  stands, and no controlled wheal study came back."
- Checked against the full text: every element matches (22 planned, 20 evaluated, [dose figure omitted], VAS
  pain and itch at 2 and 4 weeks and 3 months, no NP control without lidocaine, no needle gauge or depth). The methods
  figures as written match p3. "burning in about half" is 22/45 of the NP group ([dose figure omitted]), not of the treated 22; accurate on
  its natural reading. The page does not mention that the other NP patients were prescribed topical capsaicin with no
  outcomes reported, nor whether the skin was numbed; neither omission makes a sentence wrong. No finding.

### 4b. Product pages (Buying Decisions & Info) that cite the paper
Union from the searches (37 pages): Pisacaina lidocaína 10 ampolletas — Farmacia La Paz (3e010b7903aa8142b933c65fd9fa530e);
Naropin 7.5 — Vitau (…81ac9405ef7f25d76c21); Intradermal botulinum toxin A session (…81a29972e7d5c6e300c1); Pisacaina
lidocaína frasco [dose figure omitted] — San Pablo (…81328f58e0548d56977e); Prodacid procaina [dose figure omitted] (…81939420d7daced60e18); Lidocaína FD
Zeyco plastic — Odontodo (3e810b7903aa81e6901bdb4927cb8941); Pisacaina lidocaína frasco [dose figure omitted] — Farmacia La Paz
(…81d08162ec8ca7043855); Ropiconest 7.5 — Vitau (…81a5ac8fc0ebfff97715); Prodacid procaina [dose figure omitted] (…81d29314c01e57094a19);
FD Zeyco glass — Dentiprime (3e810b7903aa81179ba4f4314a8a4b49); FD Zeyco plastic — Dentalmex (…812a9dccd6310c447c3f);
Turbocaína glass (3e010b7903aa814c8faec76e19774fd7); PiSA Lidocaína/Epinefrina cartridge (…81059294ec5f6c29f711);
Ropiconest 7.5 — Curitek (…8147adc8f9881ba7856e); Pisacaína con epinefrina [dose figure omitted] — Curitek (…817187d5f2d6dfde7486);
Newtheek — Tu Depósito Dental (3e810b7903aa81e0bb6bd09d27b3356e); FD Zeyco plastic — Dental Shop (…81f3b52bde401944a917);
FD Zeyco glass — Dental Shop (…81469826edb8fa72b8ee); Pisacaina lidocaína [dose figure omitted] frasco — Farmacia La Paz
(3e010b7903aa810992e3c8ca67e5b188); FD Zeyco — Gómez Farías (3e810b7903aa81aba073c265c7bad2b5); Newtheek — Paradentum
(…81fe9870f3207bc463c8); Turbocaína dental cartridges (3e010b7903aa811396d4de6b6f5dbd32); FD Zeyco — Tu Depósito Dental
(3e810b7903aa81cd8d73c4498ad88e81); Lidocaína FD con epinefrina [dose figure omitted] (3e010b7903aa81aea93ec8e114bf10c2); FD Zeyco
(with epinephrine) 50 dental cartridges (…81ab9759c0273f2ab981); Ropiconest [dose figure omitted]/mL — La Paz (…81f1b482c79e7537bb8b);
Anestésico lidocaína FD Zeyco glass (…81f49ea2d8a7452425e9); Ropiconest 7.5 — La Paz (…81db8c31e4a679616015); Zingo
(3e310b7903aa81e6b472ede6a8dbcee6); procain-Loges [dose figure omitted] — Shop Apotheke (3e410b7903aa817db459c71524b826a3); FD Zeyco — VQ
(3e810b7903aa81a2b5c1d65aaf65790d); Pisacaína con epinefrina — Farmacias Guadalajara (3e010b7903aa819f8792c73cd4e8e688);
Newtheek — Gómez Farías (3e810b7903aa81ca9de4d1a2a3a11675); FD Zeyco glass — Juárez (…81eda2b4d7db917d53cf); Newtheek —
Tu Universo Dental (…81a89e62fdab8c6882a3); Pisacaina con epinefrina frasco — Farmacia La Paz (3e010b7903aa81869136f471686598c6).
(Prefix 3e010b7903aa / 3e810b7903aa elided after the first of each.)

The search highlights show a few repeated templates. Fetching all 37 would not fit; one page of each template was
fetched and read in full, and the rest are listed as not fetched (their wording is known only from search highlights,
which is not used to decide anything).

Fetch 3 — "Lidocaína FD Zeyco ([dose figure omitted] with epinephrine [dose figure omitted]), 50 plastic cartridges × [dose figure omitted] — Odontodo (Mexico)"
(dental-depot template). URL https://app.notion.com/p/3e810b7903aa81e6901bdb4927cb8941 ; "as of 2026-09-27T10:42:33.361Z";
inline; no truncation flags. Verbatim (product strengths and prices are the page's, not methods figures):
- Why For Purpose: "Kinda, as on the product's other rows: right drug and route, and the evidence for the purpose is only
  indirect — no wheal study used an epinephrine-containing solution, and the one wheal protocol with a pain outcome, in
  notalgia paresthetica, used plain lidocaine and was uncontrolled (Mülkoğlu 2020, PMID 32416719)."
- Verdict: "Needs More Research, and Kinda for the purpose: no wheal study used an anaesthetic with epinephrine, so its
  evidence is only indirect, from one uncontrolled study of plain lidocaine."
- Sources: "Mülkoğlu 2020, BMC Neurol, PMID 32416719 — abstract read by the pain-evidence audit, 2026-09-22."
- Research Pages links the T02 Meta page "(one uncontrolled wheal protocol with an outcome; none in small fibre neuropathy)".
- Against the full text: "used plain lidocaine" — the paper names only a lidocaine ampoule and saline (p3), no
  vasoconstrictor; "uncontrolled" — no NP control without lidocaine (p7); both true. The source is marked as read from
  the abstract only, and the abstract alone does not say there was no control group → now-verified (low), F01.
  "the one wheal protocol with a pain outcome" — on its natural reading "the only one"; the paper itself (p2) cites the
  same group's earlier case (2018) of local lidocaine injections into the upper back with a pain outcome in NP; route not
  stated as intradermal in the 2020 text. Ambiguous → see F02 decision below.

Fetch 4 — "Lidocaína FD [dose figure omitted] con epinefrina, [dose figure omitted] × [dose figure omitted] (Mexico)" (marketplace-cartridge template).
URL https://app.notion.com/p/3e010b7903aa81aea93ec8e114bf10c2 ; "as of 2026-09-27T10:58:16.937Z"; inline; no truncation flags.
(The page's Edits property quotes removed dose-ceiling text; not copied here.) Verbatim, figures masked:
- Why For Purpose: "Kinda, judged on what the listing states: right drug and route, and the evidence for the purpose is
  only indirect. The one wheal protocol with a pain outcome in a chronic neuropathic condition that PubMed indexes used
  plain lidocaine diluted to about [dose figure omitted], in 20 people with notalgia paresthetica, and was uncontrolled
  \[Mülkoğlu 2020, *BMC Neurol*, doi:10.1186/s12883-020-01773-6\]; no wheal study used an epinephrine-containing
  solution, and none is in small fibre neuropathy."
- Sources: "Mülkoğlu 2020, BMC Neurol, PMID 32416719, https://pubmed.ncbi.nlm.nih.gov/32416719/ — abstract read by the
  pain-evidence audit, 2026-09-22."
- Against the full text: dilution as stated matches p3 (not written here); "20 people" = the 20 evaluated of 22 treated
  (p4–5); "uncontrolled" true (p7). These come from the full text, which this page marks as unread → now-verified (low).
  "The one wheal protocol with a pain outcome in a chronic neuropathic condition that PubMed indexes" → see F03.

Fetch 5 — "Pisacaina lidocaína [dose figure omitted], 10 ampolletas × [dose figure omitted] — Farmacia La Paz (Mexico)" (plain-lidocaine template, "full
text read"). URL https://app.notion.com/p/3e010b7903aa8142b933c65fd9fa530e ; "as of 2026-09-27T16:20:44.273Z"; inline; no
truncation flags. (The page's Edits and How to take it carry dose and session arithmetic; not copied.) Verbatim, masked:
- Why: "Good: wheals of plain lidocaine made from these ampoules by the dilution the one wheal study in a neuropathic
  condition describes are the form that study used, and it reported improvement without a control group."
- Why For Purpose: "Kinda: right form and route, and the evidence for the purpose is weak. The one wheal protocol with an
  outcome in a chronic neuropathic condition that PubMed indexes — [dose figure omitted] intradermal wheals at [dose
  figure omitted] intervals, [dose figure omitted], in 20 people with notalgia paresthetica — reported lower
  pain at 2 and 4 weeks and at 3 months but was uncontrolled \[Mülkoğlu 2020, *BMC Neurol*,
  doi:10.1186/s12883-020-01773-6\]; small fibre neuropathy itself was not studied, and no study compares [dose figure omitted] with [dose figure omitted]
  lidocaine for pain relief, so nothing separates this pack from the [dose figure omitted] vial on evidence."
- Verdict (body): "Good, and Kinda for the purpose: wheals of plain lidocaine made from these ampoules by the one wheal
  study's dilution are the form that study tested, and it reported improvement without a control group."
- Sources: "(Mülkoğlu 2020, intradermal lidocaine wheals in notalgia paresthetica; full text read 2026-09-23)."
- Against the full text: methods, n, schedule, outcomes and "uncontrolled" all match. Not stated anywhere on the page:
  that the paper never reports whether the treated skin became numb, and that the week-2 and week-4 scores were taken
  at visits that were also injection visits (the paper does not say before or after the injection). Neither omission
  makes a sentence wrong. "the one wheal study in a neuropathic condition" / "The one wheal protocol with an outcome in
  a chronic neuropathic condition that PubMed indexes" → F03 (low, ambiguous): the paper itself (p2) cites the same
  group's earlier PubMed-indexed case of local lidocaine injections into the upper back in NP with a pain outcome
  (Mülkoğlu, Nacir, Genç 2018, PMID 29911324, a letter with no abstract; route not stated as intradermal in the 2020 text).

Relief page (Fetch 1), further passages relied on (verbatim, masked):
- Section "What is still unknown" (char ~42171): "**Whether relief outlasting the block happens in small fibre
  neuropathy at all.** Every series is in neuralgia after nerve injury, phantom limb pain, vulvodynia, back pain or
  myofascial pain. *What would settle it:* a sham-controlled trial in small fibre neuropathy. None exists, and none is
  registered on [ClinicalTrials.gov](http://ClinicalTrials.gov)."
  → Mülkoğlu 2020 is a series (uncontrolled, 20 evaluated) of intradermal lidocaine papules in notalgia paresthetica, a
  sensory neuropathy, with lower pain and itch to three months; it is not in the list and the page does not cite it.
  The "Every series" sentence is not a tested claim (grep 'Every series|vulvodynia|Weinschenk' → no such claim; D030 is
  the sham-controlled-SFN half). → F04 (understated, low). (Not from my paper and so not a finding: PHN series such as
  Rowbotham 1989, local anaesthetic skin infiltration, 12 patients, are also outside the list.)
- Same section: "**What is in the eight papers.** The systematic analysis of cutaneous anaesthesia reports "more than
  half of patients" without a denominator, and the paper is paywalled. *What would settle it:* the full text of *J
  Anesth Clin Res* 2012;3(3):199 and its reference list — those eight primary papers are the closest thing that exists
  to evidence for what he is doing." Not answered: the full text could not be reached here either (section 3).
- Same section: "**Whether an intradermal wheal can produce what a six-day perineural infusion produced.** … *What would
  settle it:* a trial of repeated intradermal wheals against saline wheals with a one-month primary endpoint. The
  Colombian trial is the only attempt and stopped at 21 days." Mülkoğlu has no saline arm, so it is not such an attempt;
  no finding.
- Sources › The uncontrolled series lists Weinschenk 2022, Gerhardt 2025, Egli 2015, Vlassakov 2011, Vlassakov 2012,
  Vinyes 2023; no notalgia paper. Egli 2015 (Mülkoğlu's ref 29) is summarised accurately against its abstract; the four
  outcome groups the page copies from the abstract (41 + 126 + 52 + 60) sum to 279 of 280, which neither the abstract
  nor the page remarks on; the sentence is accurate, so no finding (noted for the main session only).
- "What the citation record shows": "Vlassakov 2012 … has no citations indexed at all." (scite). OpenAlex lists 1 citing
  work (2015). Not from my paper; no finding.

Fetch 6 — "Comparing the injectable local anesthetics for intradermal wheals" (D015's page). URL
https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b ; "as of 2026-10-02T03:14:02.626Z"; saved to file (106,796
characters), parsed, text 105,800 characters; no truncation flags. Mülkoğlu / Mulkoglu / Nacır / notalgia / 32416719: 0
hits; Vlassakov 0. D015's sentence (char ~65085), verbatim: "**What does repeated injection over months do to skin that
has already lost nerve fibers?** Unstudied for every drug here. The only objective measure is a count of nerve fibers in
a small skin biopsy, …" — the paper does not change it (other-claim entry). No finding.

Fetch 7 — "Ropivacaine Wheals" (tested by S1; findings only). URL https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e ;
"as of 2026-10-02T03:14:26.511Z"; saved to file (403,224 characters), text 399,446; no truncation flags. Mülkoğlu: 10 hits.
Verbatim, masked:
- 12.3a "Protocol design from the closest existing intervention" (char ~280500): "One wheal protocol with a local
  anaesthetic and a pain outcome has been published: [dose figure omitted] of [dose figure omitted] lidocaine diluted in
  [dose figure omitted] of saline, [dose figure omitted] wheals [dose figure omitted] apart, [dose figure omitted], with pain
  lower at 2 and 4 weeks and at 3 months in 20 people with notalgia paresthetica, uncontrolled, and none in small fibre
  neuropathy (Mülkoğlu 2020, PMID 32416719)."
- Section 13, gap 1 (char ~285215): "So local anaesthetic infiltration for neuropathic pain has been tried and has some
  evidence behind it. What has been reported only once is an anaesthetic-only wheal protocol with per-wheal volume,
  spacing, a repeated-session schedule and a pain outcome: [same figures, masked] … in 20 people with notalgia
  paresthetica, uncontrolled (Mülkoğlu 2020, PMID 32416719) — and nothing at all in small fibre neuropathy." Revised
  statement: "the intervention class is not novel; this specific protocol is unstudied."
- Edits log 2026-09-24 records the narrowing that introduced these sentences; it also says "Left alone: the statement
  that nobody has measured neuropathic relief from a ropivacaine wheal, which still holds." (true: Mülkoğlu is lidocaine).
- Against the full text: all methods, schedule, n and outcome details match p3–5 and Table 3. The section-13 sentence is
  narrow (stated per-wheal volume, spacing, schedule and pain outcome) and the paper does not contradict it. The 12.3a
  sentence drops those qualifiers ("One wheal protocol with a local anaesthetic and a pain outcome has been published");
  the paper itself cites the same authors' earlier PubMed-indexed case of local lidocaine injections into the upper back
  with a pain outcome (p2, ref 12) → F05 (overstated, low, ambiguous because the 2020 text does not give that case's
  route). (Other wheal studies with a pain outcome that the record already holds — e.g. the Colombian procaine papule
  trial on the Relief page, Loughnan 2009 in D029 — would also bear on the 12.3a wording but are not from my paper; S1
  tests this page.)

Fetch 8 — "🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned". URL
https://app.notion.com/p/3d410b7903aa8107a042d4e7f6540c1a ; "as of 2026-10-02T03:14:04.610Z"; saved to file (77,118 characters),
text 76,264; no truncation flags. Mülkoğlu/notalgia: 0 hits. C047's sentence (char ~73922): "**Any of this literature in
neuropathic skin.** Every subject in every study on this page was a healthy volunteer, most of them in their twenties,
injected in the flexor forearm." True of the studies on that page; the paper measured no duration. No finding.

Fetch 9 — "💉 Lidocaine With Epinephrine Wheals". URL https://app.notion.com/p/3c610b7903aa801c906fcde8b5c43674 ; "as of
2026-09-26T18:28:27.736Z"; saved to file (334,407 characters), text 332,305; the two "truncated" strings in it are page
prose (about truncated abstracts), not fetch flags; the text ends with </content></page>. Mülkoğlu/notalgia/Vlassakov/
"wheal protocol"/"pain outcome": 0 hits. No finding.

Fetch 10 — "Procaine / Novocaine". URL https://app.notion.com/p/31910b7903aa80d1a022fa3b5cb01b5c ; "as of 2026-09-26T18:25:29.323Z";
saved to file (52.3 KB, wrapped), text 51,850; no truncation flags. Mülkoğlu/notalgia: 0 hits (the page does not cite it).
(The page's Description and "The maximum dose" section carry dose ceilings; not read into notes.) Verbatim, masked:
- The recommendation (char ~4597): "… What procaine is for is **resting a site** — varying what the skin is exposed to
  between sessions of whichever drug is doing the analgesic work — and, if the relief that outlasts a block is real,
  procaine is the drug that literature actually uses."
- "Where procaine sits against the other candidates" (char ~20762): "**If the object is relief that outlasts the block,
  procaine is the drug the literature actually uses, and its shortness is not a defect.** The published infiltration
  series are procaine series: **[dose figure omitted] procaine at [dose figure omitted] a session ([dose figure omitted])
  over [dose figure omitted] in 45 women with severe chronic vulvodynia — …** A second series of **280 referred refractory
  chronic-pain patients** treated with procaine or lidocaine alone, … Neither is controlled, neither is a neuropathy
  cohort, and the second set of authors state outright that the specific contribution of the intervention cannot be
  determined."
- "What is still unknown" (char ~31777): "**Whether procaine's short block matters at all.** Every duration figure on this
  page assumes the object is hours of numbness. The uncontrolled series that report months of benefit used the
  shortest-acting drug in the group and did not compare it against any other. *What would settle it:* a randomised
  comparison of procaine against a long-acting agent on a one-month endpoint, which has never been done."
- Against the paper: Mülkoğlu 2020 is a published uncontrolled series of intradermal lidocaine (not procaine) papules in
  a neuropathic condition, reporting lower pain and itch to three months. So "The published infiltration series are
  procaine series" and "procaine is the drug the literature actually uses" overstate (the page's own second series was
  procaine or lidocaine; the notalgia series was lidocaine and is a neuropathy cohort) → F06 (overstated, medium: the
  page's recommendation repeats the claim). "The uncontrolled series that report months of benefit used the
  shortest-acting drug in the group" overstates for the same reason → F07 (overstated, low). None of these sentences is
  a tested claim (grep 'procaine series|literature actually uses|shortest-acting|infiltration series|report months of
  benefit' → 0 claims).

Fetch 11 — "mepivacaine-wheals". URL https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185 ; "as of 2026-10-02T03:14:08.315Z";
saved (68,028 characters), text 67,421; no flags. Mülkoğlu/notalgia/Vlassakov/"wheal protocol"/"pain outcome"/series: 0.
Fetch 12 — "bupivacaine-wheals". URL https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d ; "as of 2026-10-02T03:14:18.695Z";
saved (85,199 characters), text 84,250; no flags. Same searches: 0 hits. No findings on either.

Fetch 13 — "2 — Reference — Topical Treatments for Small Fiber Neuropathy". URL
https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65 ; "as of 2026-10-01T02:05:48.095Z"; saved (1,286,736 characters),
text 1,279,938; the two "truncated" strings are prose (MEDLINE-truncated abstract; a truncated pack number), and the
text ends with </content></page>: complete. Searched with Python only.
- Mülkoğlu / Mulkoglu / Nacır / notalgia / 32416719 / 12883-020 / "BMC Neurol" / its title words: 0 hits. The paper is not
  in the source register S1–S457. Egli: 0 hits; Egli's title words ("Long-term results of therapeutic local
  anesthesia", "neural therapy) in 280"): 0 hits. Vlassakov, Chtompel: 0 hits.
- §4.9 "Injected local anaesthetics — the current regimen" (char 146839–159619). This section also carries dose
  ceilings, ceiling arithmetic and an antidote passage; none of it is copied here. Passages relied on, verbatim, masked
  (session counts masked too):
  - header line (char ~146900): "**Magnitude UNKNOWN by this route in this condition · Duration published for procaine
    and lidocaine in other neuropathic conditions, median 24.1 months in the largest series · Evidence NONE in small
    fibre neuropathy; two randomised trials in adjacent conditions**"
  - (char ~148699): "Intradermal lidocaine at **[dose figure omitted] in [dose figure omitted]**, [dose figure omitted],
    held pain and itch down **to three months**." No source tag. This is Mülkoğlu 2020 (only notalgia paresthetica
    has pain and itch outcomes with this design). Its masked figures were checked privately against p3 and match; the
    session count and spacing match too. Population, n and design are not stated, and no source is given → F08.
  - (char ~149081–149224): "**Repeated infiltration is cumulative, not diminishing.** Every series reporting the
    question escalates rather than tapers — [dose figure omitted], [dose figure omitted], a median of [dose figure
    omitted] in the first year across **280 referred refractory chronic-pain patients** given procaine or lidocaine
    alone, of whom **[dose figure omitted] needed less analgesia or none** at one year \[S174\]." The 280-patient series
    is Egli 2015 (Mülkoğlu's ref 29); register entry S174 (char 913467) lists Weinschenk 2016 (pharyngeal procaine,
    17 patients), Weinschenk 2022 (vulvodynia, 45 women) and Kastelik 2025, not Egli → F09 (citation-error).
    (Mülkoğlu's own course was fixed, not escalating, and its pain fell further between week 2 and week 4 — consistent
    with "cumulative"; no finding on that part.)
  - The 24.1-month median in the header belongs to the 45-woman vulvodynia series (char ~148439, tagged S174), which
    S174 itself calls "a chronic pelvic pain one and not a neuropathy one"; the largest series in the section (280,
    Egli) reports status at one year, not a duration → F10 (wrong-figure, medium).
  - Also in §4.9 (not from my paper; for the main session): a "double-blind three-arm trial of intra-epidermal and
    intra-dermal mesotherapy in complex regional pain syndrome type 1, n=31" with lidocaine is described under
    "Randomised"; it may bear on T02 ("No controlled study tests anaesthetic-only intradermal wheals for chronic
    neuropathic pain"), depending on its arms. Not checked here.
- §3.2 (char 78741): "**No randomised trial of cutaneous or subcutaneous local anaesthetic infiltration for established
  small fibre neuropathy was located, for lidocaine, procaine or ropivacaine.**" — true; the paper is not SFN and not
  randomised. "**Procaine**: the infiltration series above are the evidence; no modern randomised trial of local procaine
  infiltration in chronic peripheral neuropathic pain was located." — not affected (lidocaine paper). No finding.

Fetch 14 — "1 — Product Guide — Topical Treatments for Small Fiber Neuropathy". URL
https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f ; "as of 2026-10-02T03:14:29.224Z"; saved (602,569 characters), text
599,993; no flags. Mülkoğlu / notalgia / 32416719 / Vlassakov / Egli / "one wheal" / "wheal protocol" / "procaine series":
0 hits. Its wheal passages (char ~234500–239600) are injection technique and dose arithmetic (filter subject); not
read further and not copied. No finding.

Fetch 15 — "5 — Soft ground in these documents". URL https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 ; "as of
2026-09-26T18:26:13.509Z"; inline; no flags. Nothing on the paper, wheals, neural therapy or Vlassakov. No finding.

Fetch 16 — "What is still unsettled across these pages, and what would settle each one". URL
https://app.notion.com/p/3d410b7903aa819f8300e976a62577db ; "as of 2026-09-26T18:23:10.973Z"; saved (61.3 KB, wrapped), text
61,415; the two "truncated" strings are prose (a registro printed truncated); text ends with </content></page>.
Mülkoğlu/notalgia: 0 hits. Verbatim:
- Section "Which primary sources are unread, and what each would settle" (char ~7346): "**Full text of *J Anesth Clin
  Res* 2012;3(3):199.** A systematic analysis of cutaneous anaesthesia reporting that **"more than half of patients"**
  benefited, with **no denominator**. The paper is paywalled and its eight primary references are the closest thing
  that exists to evidence for repeated intradermal wheals as a technique in use. **What would settle it:** the full text
  and its reference list. … **Confidence in the current reading:** low."
- Summary bullet (char ~4196): "A second paywalled paper's reference list is the closest thing that exists to evidence
  for repeated intradermal wheals as a technique (see "Which primary sources are unread, and what each would settle")."
- Against the paper: Mülkoğlu 2020 is a published, free (PMC7229619) series of repeated intradermal lidocaine papules in
  a sensory neuropathy with its schedule stated and outcomes to three months; Vlassakov's abstract (OpenAlex) describes
  outcomes "With the single skin anesthesia treatment". So "the closest thing that exists to evidence for repeated
  intradermal wheals" overstates → F11 (overstated, low; the summary bullet repeats it). The open question itself (what
  the eight papers are) is not answered: the full text was not reachable here either.
- Relief page, same idea (section "What is still unknown"): "those eight primary papers are the closest thing that exists
  to evidence for what he is doing." → F12 (overstated, low). Related tested claim: D032's also-text "the closest paper
  in existence to what this reader is doing" → other-claim entry (narrowed stays narrowed).

Fetch 17 — "🕳️ What was searched for and does not exist, so it is not searched for again". URL
https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82 ; "as of 2026-09-27T00:27:49.877Z"; saved (65,488 characters), text
64,683; no flags. Mülkoğlu/notalgia: 0. Its intradermal entries (topical vs injected procaine; largest intradermal
botulinum field) are not touched by the paper. No finding.
Fetch 18 — "🔀 What transfers from diabetic neuropathy trials to idiopathic small fiber neuropathy, and what does not". URL
https://app.notion.com/p/3d410b7903aa813681e9c27892149a17 ; "as of 2026-09-26T18:27:17.888Z"; saved (100,310 characters), text
99,131; no flags. Mülkoğlu/notalgia/Vlassakov/wheal/outlast/neural therapy: 0. No finding.
Fetch 19 — "💊 Anaesthetics" (sourcing page linked from the product rows). URL https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492 ;
"as of 2026-10-01T03:07:38.200Z"; saved (56,562 characters), text 55,346; no flags. Mülkoğlu/notalgia/"one wheal"/"wheal
protocol"/uncontrolled: 0. No finding.
Fetch 20 — "🚫 Injectables ruled out but not tried". URL https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5 ; "as of
2026-10-02T03:14:22.080Z"; saved (73,884 characters), text 72,962; no flags. Mülkoğlu/notalgia: 0. No finding.
Fetch 21 — "Safe Doses Of Intradermal Analgesics" (dose subject: checked for mentions only, no context printed). URL
https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7 ; "as of 2026-10-02T03:13:58.754Z"; saved (66,007 characters), text
65,027; no flags. Mülkoğlu/notalgia/32416719/DOI: 0. Not read further.
Fetch 22 — Zingo row, https://app.notion.com/p/3e310b7903aa81e6b472ede6a8dbcee6 , "as of 2026-09-24T01:39:32.694Z", inline, no
flags. Why For Purpose: "… The one wheal protocol with a pain outcome in a chronic neuropathic condition that PubMed
indexes placed [dose figure omitted] wheals of diluted lidocaine at [dose figure omitted] intervals around the affected
patch and along C2–T6, in [dose figure omitted] \[Mülkoğlu 2020, *BMC Neurol*, doi:10.1186/s12883-020-01773-6\]."
Sources: "… — abstract read by the pain-evidence audit, 2026-09-22." Details match p3 (listed in F02's notes).
Fetch 23 — procain-Loges row, https://app.notion.com/p/3e410b7903aa817db459c71524b826a3 , "as of 2026-09-24T21:35:33.726Z",
inline, no flags. Why For Purpose: "… No controlled study tests anaesthetic-only intradermal wheals for chronic neuropathic
pain, and none exists in small fibre neuropathy; the one protocol with its parameters and an outcome used lidocaine, was
uncontrolled, and was in notalgia paresthetica \[Mülkoğlu 2020, …\]." Verdict body: "… the one uncontrolled wheal study
used lidocaine, and procaine has never been compared with lidocaine." Accurate apart from the "the one" wording (F03 notes).
Not fetched (wording known only from search highlights; no finding made on them): the other 32 product rows listed in 4b,
including the intradermal botulinum toxin clinic row (highlight: "uncontrolled wheal protocol with an outcome, in
notalgia paresthetica; none in small fibre neuropathy").

### 4c. Notion findings written (pm_work/parts/S-686-18/notion_findings.json)
F01 now-verified low (Odontodo dental-depot row: "used plain lidocaine and was uncontrolled", source marked abstract-only);
F02 now-verified low (marketplace cartridge row: dilution, 20 people, uncontrolled, source marked abstract-only; Zingo too);
F03 overstated low (Pisacaina ampolletas row: "the one wheal study in a neuropathic condition"; same group's 2018 case);
F04 understated low (Relief page: "Every series is in …" omits the notalgia series);
F05 overstated low (Ropivacaine Wheals 12.3a: "One wheal protocol with a local anaesthetic and a pain outcome has been published");
F06 overstated medium (Procaine: "The published infiltration series are procaine series" / "procaine is the drug the literature actually uses");
F07 overstated low (Procaine: "The uncontrolled series that report months of benefit used the shortest-acting drug");
F08 citation-error medium (Reference §4.9: sentence describing this paper has no source; paper not in register);
F09 citation-error medium (Reference §4.9: 280-patient Egli series tagged S174, which does not list it) — rests on Egli 2015;
F10 wrong-figure medium (Reference §4.9 header: "median 24.1 months in the largest series") — rests on Egli 2015;
F11 overstated low (What is still unsettled: Vlassakov's eight "the closest thing that exists to evidence for repeated intradermal wheals");
F12 overstated low (Relief page, What is still unknown: "the closest thing that exists to evidence for what he is doing").

### Claim updates written (pm_work/parts/S-686-18/claim_updates.json)
D033 own-question narrowed → narrowed, uncertain_after true (paper did not document numbness; verdict now rests on the
claim's description of its source; Attal 1999 / Cui 2017 decide refuted-or-not). D015 other-claim confirmed → confirmed.
T02 other-claim narrowed → narrowed (and identifies T02's page: the Meta finding page). C047 and D040 other-claim
confirmed → confirmed. D032 other-claim narrowed → narrowed, uncertain_after true ("closest paper in existence" wording).
extra_studies.json: [] (no cited study decides a claim; Egli 2015 is used only for F09/F10).
Card: references 31 (Bahekar 2007, periodontitis and coronary disease, PMID 17967586) and 33 (Fukai 2009, tooth number and
physical complaints, PMID 20002756), cited in the neural-therapy passage, are left out of studies_it_cites_that_matter as
unrelated to any topic in the pages; ref 32 (Cornelissen 2009) is included as marginal.

## 5. Not reached, and text addressed to agents
- Not reached: the full text of Vlassakov 2012 (J Anesth Clin Res 2012;3(3):199, DOI 10.4172/2155-6148.1000199):
  doi.org and api.crossref.org refused by the session's network policy (not worked around); Jina reader HTTP 401;
  OpenAlex marks it closed with no reference list. So the eight included papers, and whether Attal 1999 is one of them,
  remain unknown. The 2018 case letter (PMID 29911324) has no abstract and was not sought in full text.
- Not fetched: 32 of the 37 product rows that cite the paper (one or more of each wording template were fetched).
- Text addressed to agents, treated as data and not acted on: the Relief page opens with a callout "Note for the health
  skills — 2026-10-02" about keeping that page's dose limits; several pages carry "Own-use marker" notes asking that a
  passage be moved to Stack & Experience History. Neither is addressed to this work; nothing was done with them. No
  instruction aimed at this work was found in the paper, the abstracts or the Notion pages.
- No content-filter stop occurred. Dose-ceiling, ceiling-arithmetic and antidote passages met in Reference §4.9, the
  Product Guide and product-row Edits logs were not copied anywhere.
