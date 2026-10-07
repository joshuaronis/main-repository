# S-686-42 Alam 2010: working notes

Content-filter rule for this paper (from the orchestrator): the threshold, every measured serum level and every amount
of lidocaine given are never written here. Results appear only as direction, or as whether any subject reached the
authors' toxicity threshold. The number of injection episodes and the sampling schedule appear only as methods facts.

## 1. Right-paper check

- PDF: `papers/S-686-42 - Alam 2010 - Safety of peak serum lidocaine concentration after Mohs micrographic surgery a prospective cohort study.pdf`, 6 PDF pages.
  Text: `texts/S-686-42.txt` (reading order plus layout view). It is readable, with no OCR needed. PDF page 2 reading order
  interleaves the two columns with the capsule-summary box, so quotes from page 2 use only runs that are unbroken.
- Title, authors and journal match the request: Alam M, Ricci D, Havey J, Rademaker A, Witherspoon J, West DP.
  "Safety of peak serum lidocaine concentration after Mohs micrographic surgery: A prospective cohort study".
  J Am Acad Dermatol 2010;63:87-92 (journal pages 87-92, PDF pages 1-6). It was published online on 12 May 2010 and
  accepted on 30 August 2009. ClinicalTrials.gov NCT00793169.
- The PDF prints `doi:10.1016/j.jaad.2009.08.046` (PDF page 1, line 66 of the text file).
- PubMed (connector, get_article_metadata 20462662): DOI 10.1016/j.jaad.2009.08.046, PII S0190-9622(09)01200-6, J Am Acad
  Dermatol 2010;63(1):87-92, epub 2010-05-11. **The PDF and PubMed agree: the correct DOI is 10.1016/j.jaad.2009.08.046.**
  - `common/papers_list.csv` also gives 10.1016/j.jaad.2009.08.046, which is correct.
  - `common/claims_all.json` D069 `needs_full_text` gives 10.1016/j.jaad.2009.09.061, which is wrong for this paper
    (see section 3 for what that DOI resolves to).
  - Josh's person_note says "Spreadsheet DOI differs from the DOI printed in the requested title/author/year PDF". The
    PDF is the right paper (title and PMID match). The spreadsheet DOI that differs is the .09.061 one.
- The full text was read in full: abstract, introduction, methods, results, Table I, Fig 1/2 legends, discussion,
  limitations and all 10 references.
- Internal inconsistencies in the paper (methods and counts only, no levels):
  - The Results text says "5 with undetectable lidocaine levels at all time points, and 14 with at least one detectable
    level". Table I lists 5 subjects with a detectable peak and 14 with none. Fig 1's legend and the text "greatest number
    ... at the sixth blood draw (5 patients)" fit the table. So the text sentence appears to swap the two counts.
  - "no follow-up beyond the 6 hours of the study procedure" (p3) vs "blood draws were collected over a maximum of 8
    hours" (p3) and "up to 8 hours (maximum 7.8 hours, mean 4.4 hours)" (p5).
  - 20 enrolled; 1 withdrew after the first draw; complete data on 19. The discussion still uses "20 patients" as its
    denominator.

## 2. Claim screen (all 320 claims in common/claims_all.json)

Regex over claim text, elements, reason, proposed wording, review, records_read and needs_full_text (counts of claims hit):
plasma 15; serum 4; blood level/concentration/sampling/draw 1 (D069); pharmacokin 11; systemic 12; absor 4;
tumescen 4 (C054 C071 D069 D073); Mohs 2 (D048 D069); liposuc 4; Alam / 20462662 / jaad 1 each (D069 only);
Alam's reference authors: Ostad, Rubin, Klein, Butterwick, Hanke, Lillis, Thomson, Becker all 0; Foldes 1 (D023, which is
Foldes & McNall 1952, a different paper); D069 records: Burk 2 (D069 D073), Brown 2 (D069 D073), Riff 1, Sato 2 (D069
D072), Effendy 3 (C070 D066 D069); repeat 40; re-dose 0; session 15; toxic 23; ceiling 7; maxim 7; half-life 0;
head-and-neck/scalp/face 11; dermatologic surgery/skin cancer/excision 11; infiltrat 62; peak 2 (C068 D069); Cmax 0;
accumul 3; wheal 54; tachycardia/heart rate/haemodynamic 2 (D073 D074); bicarbon/buffer 6; chromatograph/assay 1;
toxicity symptoms 0; liver/hepatic/elderly 6; volume 17; total/cumulative 4; surg 16.

Read closely (sentence, elements, verdict, reason), with the decision for each:
- D069 (own question). Re-judged, see claim_updates.
- D072 (Safe Doses, "safe interval between sessions ... rests on those series' schedules rather than on a clearance
  measurement", confirmed). KEPT as other-claim. Its reason says "the only repeated-administration concentration data
  found (Sato 2022) are within a single session". Alam 2010 is a second within-session repeated-administration serum
  dataset. It measured nothing between sessions (single visit, no follow-up after the procedure day), so the verdict
  stays confirmed. Written without any interval figure.
- D070 (Safe Doses, ropivacaine cutaneous/subcutaneous infiltration in chronic pain). Dropped: Alam is lidocaine in
  surgery and has no chronic pain population.
- D048 (liposomal bupivacaine intradermal). Dropped: Alam has no liposomal bupivacaine.
- D066, C070, C069, C068 (EMLA / prilocaine / methaemoglobin). Dropped: different drug, route and outcome.
- C054 (articaine intradermal). Dropped: different drug.
- C013, C014, C023, C043, C025 (adjuvants, sustained release). Dropped: Alam has no adjuvant comparison.
- C077 (layer-resolved skin concentration). Dropped: Alam measured serum only.
- D023 (procaine intradermal, Foldes & McNall 1952). Dropped: Alam cites Foldes et al 1960 (IV toxicity), a different
  paper, and it does not bear on intradermal procaine duration.
- D034 (procaine in dermis over time). Dropped: serum lidocaine, not dermal procaine.
- A011, A036, A038, A054, A087, D041, E033, E035, E037, C049, C055, D004, D013, D016, D064, C086, C089, D015, D029, D033,
  D044, C028, E019, E032, A014, A056, A064, A080, C008, E036, E044, A059, C063, D065, E018, A049. Dropped: no overlap
  in drug, route, population, outcome or design (they came up on generic words such as systemic, repeated, session,
  toxic, plasma (platelet-rich plasma), liver (from "delivered")).
- C081 (Lidocaine With Epinephrine Wheals, uniqueness of an intradermal onset/duration study). Dropped: Alam did not
  measure onset or duration of anaesthesia.

Skipped under the filter rule (dose, toxicity, ceiling or recipe subject; text not written out, only counted):
- Safe Doses Of Intradermal Analgesics: 4 claims not tested: dose or toxicity subject (D071, D073, D074, D075).
  None of them turns on serum lidocaine after skin infiltration in any case. D069 is my own question and is answered
  under the hand-over's exception.
- prilocaine-wheals: 1 claim not tested: dose or toxicity subject (C071).
- Comparing the injectable local anesthetics for intradermal wheals: 3 claims not tested: recipe (buffering) subject
  (D012, D017, D018). Alam does not study buffering in any case.
- 💉 Lidocaine With Epinephrine Wheals: 1 claim not tested: recipe (mixing/dilution) subject (C091).

## 3. PubMed (connector; eutils blocked, so pm.py cannot run). Cache written with pm_work/tools/pmcache.py

- get_article_metadata 20462662: Alam 2010, DOI 10.1016/j.jaad.2009.08.046, J Am Acad Dermatol 63(1):87-92. Saved as
  pm_work/cache/a_20462662.json with `--redacted`: the solution recipe, the amounts given and the serum levels were
  replaced by [dose figure omitted]. Affiliations and MeSH were left out of the pasted object; the title and the rest
  of the abstract are verbatim.
- search `10.1016/j.jaad.2009.09.061[doi]`: count 0, translation `10.1016/j.jaad.2009.09.061[doi]`. That DOI does not
  resolve to any PubMed record. It is the DOI given for this paper in claims_all.json D069 needs_full_text, and it is
  wrong. (The connector's convert_article_ids returned a rate-limit error on the first try.)
- search `10.1016/j.jaad.2009.08.046[doi]`: count 1 (20462662), translation `"10 1016 j jaad 2009 08 046"[Publisher ID]`.
- lookup_article_by_citation for references 1-9 (the connector returned the PMID in the `key` field):
  1 Thomson 1973 Ann Intern Med 78:499 -> 4694036 (no abstract; DOI 10.7326/0003-4819-78-4-499)
  2 Butterwick 1999 Dermatol Surg 25:681 -> 10491056 (PubMed pages 681-5; Alam's list says 681-90)
  3 Becker & Reed 2006 Anesth Prog 53:98 -> 17175824 (PMC1693664)
  4 Foldes 1960 JAMA 172:1493 -> NOT FOUND by citation; search `Foldes FF[Author] AND JAMA[Journal] AND 1960[dp] AND
    toxicity` count 0; title search `comparison of toxicity of intravenously given local anesthetic agents in man`
    count 1 -> 13823696 (no abstract; DOI 10.1001/jama.1960.03020140029007)
  5 Hanke 1995 Dermatol Surg 21:459 -> 7743109
  6 Klein & Kassarjdian 1997 Dermatol Surg 23:1169 -> 9426661 (case report, no abstract)
  7 Lillis 1990 Dermatol Clin 8:439 -> 2199106
  8 Ostad 1996 Dermatol Surg 22:921 -> 9063507 (its title carries a dose figure, written here as "Tumescent
    anesthesia with a lidocaine dose of [dose figure omitted] is safe for liposuction")
  9 Rubin 2005 Plast Reconstr Surg 115:1744 -> 15861085 (randomised crossover, neck vs thigh subcutaneous tumescent
    injection in 8 volunteers, plasma sampled for 14 h; PubMed's last author is May JW, Alam's list says "Maw JW Jr")
  10 Hospira package insert 2008: no PMID.
- Abstracts read (metadata call for all eight). None of the cited studies decides a claim: all are tumescent or
  subcutaneous surgical infiltration, IV toxicity, IV pharmacokinetics, surveys or reviews. None is intradermal wheal
  therapy (D069), none measures anything between repeated sessions (D072), and none tests a claim on another page.
  So extra_studies.json is [].

## 4. Notion (read-only: notion-search and notion-fetch only)

### Searches (query, results returned; page_size 25)
1. `Alam 2010 Mohs serum lidocaine`: 24 results, all topical-lidocaine product pages (Buying Decisions & Info) plus the
   Reference. None shows Alam in its highlight (highlights decide nothing; pages fetched below).
2. `20462662`: 25 results, all unrelated (Health History, Todoist extracts). No page shows the PMID.
3. `jaad.2009.09.061`: 25 results, all unrelated (matched on dates).
4. `10.1016/j.jaad.2009.08.046`: 18 results, all unrelated other-DOI pages (diabres, fshw, ebiom ...).
5. `Mohs micrographic surgery peak serum lidocaine concentration`: 19 results: Reference, Lidocaine With Epinephrine
   Wheals, Injectables ruled out but not tried, Product Guide, Ropivacaine Wheals, Safe Doses, Prilocaine + Lidocaine,
   OTC IV Options (Mexico), and topical lidocaine product pages.

### Pages fetched
- **Safe Doses Of Intradermal Analgesics**, https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7, as of
  2026-10-02T03:13:58.754Z (= the version tested). Not truncated, no unknown blocks; 65,027 characters, saved to a
  tool-results file and searched with Python.
  - Alam / Mohs / 20462662 / jaad / micrographic / serum / Sato / Burk / Brown / Riff / Effendy / Ostad / Rubin /
    Klein / Butterwick / Hanke / Becker / Foldes / Thomson / liposuction: **0 hits each**. The page does not cite Alam
    or any of its references. tumescen: 2 hits, both in the prilocaine methaemoglobin passages (ceiling subject, not
    used).
  - D069 sentence ("What is still unknown", verbatim, figures omitted): "**Whether any of these ceilings describes what
    happens at a wheal volume.** Every maximum in the table is a single-procedure convention written for infiltration
    and nerve block, not a threshold derived from measured plasma concentrations after dozens of [dose figure omitted]
    intradermal deposits. *What would settle it:* a plasma level drawn at [dose figure omitted] minutes after a full
    session, which no published study of wheal therapy has done for any agent."
    The literature-absence part stays true after Alam (Alam is surgical infiltration of one site, not wheal therapy),
    so there is no finding. The first two sentences have a ceiling subject and are not judged.
  - D072 bullet ("What has no source", verbatim, figure omitted): "**The safe interval between sessions on any of
    these agents.** [dose figure omitted] is the floor the published series work to, and it rests on those series'
    schedules rather than on a clearance measurement." Alam measured nothing between sessions, so this stays true and
    there is no finding. Only the claim's reason in claims_all.json changes (see claim_updates).
  - The rest of the page (label table, label sources, prilocaine, epinephrine and Mexican-availability sections, and
    the D071/D073 bullets) has ceiling, toxicity or antidote subjects. It was read only to confirm that no
    sentence turns on serum lidocaine after skin infiltration or on repeated dosing within a session. None does, apart
    from the route/absorption section's general statement that absorption after tissue injection has a time course.
    That statement is consistent with Alam and needs no finding.
- **💉 Lidocaine With Epinephrine Wheals**, https://app.notion.com/p/3c610b7903aa801c906fcde8b5c43674, as of
  2026-09-26T18:28:27.736Z. Not truncated, no unknown blocks; 332,305 characters. The two "truncated" strings in the text
  are prose about truncated abstracts, not truncation notices, and the page ends normally.
  Alam / Mohs / 20462662 / serum / plasma level / blood level / Sato / Burk / Rubin / Ostad / Butterwick: 0 hits.
  jaad: 2 (Krunic 2004, Vent 2020: other papers). tumescen: 4 and Klein: 4 (Klein 1990 tumescent record, cited as the
  safety record for repeated dilute epinephrine in skin). The "Systemic effects, for the record" passages are
  per-session epinephrine amounts set against ceilings (ceiling subject, not used). No sentence on serum lidocaine after
  infiltration, so no finding.
- **Comparing the injectable local anesthetics for intradermal wheals**, https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b,
  as of 2026-10-02T03:14:02.626Z. Not truncated; 105,800 characters. Alam, serum, plasma level, tumescent and Alam's
  reference authors: 0 hits. Foldes: 3 hits, all Foldes & McNall 1952 (the D023 paper, not Alam's Foldes 1960).
  pharmacokinetic: 3 hits (Kopacz & Bernards clonidine; Ginosar 2016). No finding.
- **🚫 Injectables ruled out but not tried**, https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5, as of
  2026-10-02T03:14:22.080Z. Not truncated; 72,962 characters. Alam, serum, plasma level, tumescent and Mohs: 0 hits. The
  "systemic" hits are dibucaine toxicity and a sustained-release formulation's systemic toxicity (toxicity subject,
  not used). No finding.
- **Ropivacaine Wheals** (S1 tests it; findings only), https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e, as of
  2026-10-02T03:14:26.511Z. Not truncated; 399,446 characters. Alam / Mohs / Sato / craniotomy / Burk / Ostad /
  Butterwick: 0 hits. Rubin 2 and Klein 2 (Klein 1990, Rubin 1999, Kenkel 2004 as tumescent PK; Rubin 1999 is a
  different Rubin paper from Alam's Rubin 2005, so this is not a citation error). Riff 1 (Riff 2018 in 15.3). The page's
  plasma-level material in Part IV and the Revisions carries toxicity thresholds and was not used.
  - Section 6.8a "Four adjacent literatures on repeated or prolonged exposure", verbatim (formatting tags dropped):
    "None of these is about ropivacaine wheals in neuropathic skin. Each covers one of the four causal exposures that
    10.8 says need separating, and together they mark the outer edge of what is known."
    Item 4, verbatim: "4. Tumescent pharmacokinetics — the dilute-and-large-volume extreme. Klein 1990, Rubin 1999 and
    Kenkel 2004 show delayed absorption under dilute epinephrine with high tissue pressure and very large subcutaneous
    volumes, with systemic peaks arriving 4 to 14 hours later." and "Directly relevant to the safety record in 10.4 and
    6.9; it says nothing about free-drug kinetics in a [dose figure omitted] intradermal wheal."
    -> Finding F01 (understated, low): the edge drawn there leaves out within-session repeated infiltration with serial
    serum sampling (Alam 2010; also Sato 2022 for ropivacaine itself, in D069's records). This is not a claim test
    (S1 tests this page).
  - Section 13 (open gaps, 16 items) has no gap about blood levels after a wheal session. Gap 15 ("No study varies
    them", the exposure variables of wheal protocols) is unaffected: Alam varied nothing by design.
- **mepivacaine-wheals** (S1; findings only), https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185, as of
  2026-10-02T03:14:08.315Z. Not truncated; 67,421 characters. Alam, tumescent, serum and Alam's reference authors: 0 hits.
  The blood-level passage concerns mepivacaine vs lidocaine clearance (Brown 1975 newborns, Prieto-Alvarez 2002 IV
  regional), verbatim: "Both measurements are of drug in the bloodstream rather than in skin, and neither tells you
  directly how fast a wheal empties." Alam does not bear on it. No finding.
- **bupivacaine-wheals** (S1; findings only), https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d, as of
  2026-10-02T03:14:18.695Z. Not truncated; 84,250 characters. Alam, serum, tumescent and Alam's reference authors: 0 hits.
  The session and interval passages are label ceiling/interval material (not used). No finding.
- **2 — Reference**, https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65, as of 2026-10-01T02:05:48.095Z.
  1,279,938 characters, searched with Python; not truncated (the two "truncated" strings are prose about a
  MEDLINE-truncated sentence and a truncated registro suffix, and the page ends normally).
  - Source register: "Alam" appears twice, both as **Alam 2017, PLoS One, PMID 28719619** (corneal confocal
    microscopy, in S453 and a revision note), a different paper. Alam 2010, 20462662, jaad.2009.08.046/.09.061, Mohs and
    micrographic: 0 hits. Alam's reference authors: 0 (the one "Becker" is Ubbink ... Becker PJ 1987, S194, a different
    paper). jaad: 2 hits, both Fujimoto 2023 oxybutynin. So no citation of Alam 2010 and no citation error.
  - Its serum/plasma material is topical-lidocaine pharmacokinetics (S53-S63, §2.2). The injection passages in §4.9
    (session totals, doses adding across agents, session intervals, delayed-onset toxicity, antidote) are ceiling,
    frequency, toxicity or antidote subjects and are not judged (filter rule). Alam bears on none of the topical
    statements.
- **1 — Product Guide**, https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f, as of 2026-10-02T03:14:29.224Z.
  599,993 characters; not truncated. Only Alam 2017 (PMID 28719619, revision note). No Alam 2010, Mohs or Alam reference
  authors. The "Injectables" section is ceiling/toxicity/antidote material (not judged). Its governing sentence,
  verbatim: "No randomised trial of cutaneous or subcutaneous local anaesthetic infiltration for established chronic
  peripheral neuropathic pain was located for lidocaine, procaine or ropivacaine." Alam (a surgical cohort, no pain
  population) does not bear on it. No finding; no ranking rests on Alam.
- **🕳️ What was searched for and does not exist ...**, https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82, as of
  2026-09-27T00:27:49.877Z. Not truncated; 64,683 characters. No entry on blood levels after injected local
  anaesthetic; Alam etc. 0 hits. No finding.
- **5 — Soft ground in these documents**, https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403, as of
  2026-09-26T18:26:13.509Z. Fetched whole (short page). Nothing on injected local anaesthetics or blood levels. No
  finding.
- **What is still unsettled across these pages ...**, https://app.notion.com/p/3d410b7903aa819f8300e976a62577db, as of
  2026-09-26T18:23:10.973Z. Not truncated (the two "truncated" strings are prose about a registro suffix); 61,415
  characters. No open question about serum or plasma levels after skin infiltration or about repeated dosing within a
  session. Foldes hits are Foldes & McNall 1952. No open question answered.
- Other pages the searches surfaced, fetched and scanned with the same terms (none cites Alam or its references, none
  makes a literature statement on serum lidocaine after infiltration; no finding):
  Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection Routing Analysis (39410b7903aa8046b3eef25af516245f,
  as of 2026-09-26T18:19:51.310Z; its depot-clearance section is about duration and blood flow at the site);
  🔬 The intradermal wheal literature nobody cites (3d410b7903aa8107a042d4e7f6540c1a, as of 2026-10-02T03:14:04.610Z);
  prilocaine-wheals (3c510b7903aa8159a5d9e4447ec15409, as of 2026-10-02T03:14:12.541Z; its plasma material is
  prilocaine/methaemoglobin, Lindenblatt 2004, with ceiling subjects); adjuvants-without-a-vasoconstrictor
  (3d310b7903aa81fbb5b9e999637c362a, as of 2026-10-02T03:14:20.685Z; its "Sato" is Sato & Perl 1991); ⏳ Relief that
  outlasts the block (3d310b7903aa811cb51bcca149b3de73, as of 2026-10-02T03:14:06.492Z); Procaine / Novocaine
  (31910b7903aa80d1a022fa3b5cb01b5c, as of 2026-09-26T18:25:29.323Z; one sentence linking label ceilings to plasma
  concentrations at surgical sites has a ceiling subject and is not judged); ⚠️ Neurop injectable
  (11cfaa6187ca4350b7ac6e6c4d29c78f, as of 2026-09-28T09:06:10.938Z; B6 product); Prilocaine + Lidocaine
  (33110b7903aa8024a793d7249262b267, as of 2026-10-02T03:14:00.887Z; topical EMLA). None truncated.
  On the Lidocaine With Epinephrine Wheals page, the "The neck is not the leg" passage is about skin blood flow
  (capillary density), not serum levels, so no finding.

### Further searches
6. `plasma level blood concentration after a session of intradermal wheals local anaesthetic`: 17 results (Ropivacaine
   Wheals, Routing Analysis, Comparing, mepivacaine, wheal literature, Needle Size, prilocaine, Lidocaine With
   Epinephrine, a tattoo-anaesthetic group page, adjuvants, a Health History entry, Why Is AUC Important, Plasma
   Heparin, intradermal botulinum product, pyridoxine page, blood-viscosity page, a Health History entry).
7. `tumescent lidocaine serum peak hours liposuction`: 19 results (Reference, Pain biology page, topical lidocaine and
   EMLA product pages, Product Guide, Health History entries).
8. `serum concentration repeated injections within one session craniotomy ropivacaine Sato`: 15 results (pages already
   fetched, plus "Results" (procaine), Neurop injectable and Health History entries). No page cites Sato 2022.
9. `Rubin tumescent lidocaine above the clavicles neck absorption`: 15 results (Reference, Pain biology, Product Guide,
   Lidocaine With Epinephrine Wheals, product pages, Health History).
10. `S-686-42`: 20 results, none holding the ID (matched on "S" and "686" in unrelated pages). The paper-request
    spreadsheet with the differing DOI is not in Notion as far as search shows.
11. `Safety of peak serum lidocaine concentration after Mohs micrographic surgery`: 15 results, all pages already
    fetched, or Health History entries (left alone), Future Medications For Urge To Tense and OTC IV Options in Mexico
    (unrelated to skin infiltration). Not fetched: the last two, and Needle Size / Why Is AUC Important / Plasma
    Heparin (explainer or unrelated pages whose subjects are not the literature on serum levels after infiltration).
Health History entries were not opened (they record Josh's own experiences).

### Result of step E
- Alam 2010 is not cited on any Notion page fetched (Safe Doses, Lidocaine With Epinephrine Wheals, Comparing,
  Injectables ruled out, the three wheal pages, Reference register, Product Guide, the three open-question pages, and the
  other surfaced pages). So there is no citation-error finding for its DOI or PMID on Notion. The wrong DOI
  (10.1016/j.jaad.2009.09.061) exists only in common/claims_all.json D069 needs_full_text.
- 1 finding: F01 (Ropivacaine Wheals 6.8a, understated, low).

## 5. Not reached, and instructions found inside documents
- Not fetched: "What transfers from diabetic neuropathy trials ..." and the "Looking For Pain Numbing Creams" hub
  (topical scope; no topic search surfaced them), plus articaine-wheals, botulinum-toxin-wheals, Pain biology, Menthol,
  Non-drug treatments, Systemic drugs and the two Alternative Treatments pages. Their claims were screened in
  claims_all.json and none bears on Alam.
- PubMed convert_article_ids returned one rate-limit error; the DOI check was done with search_articles instead.
- Instructions inside documents (data, ignored):
  - Ropivacaine Wheals §0.0.2 "Operating instructions for the AI reading this" (tutoring preferences such as "One claim
    per reply", "Do not ask him questions unless he has invited them", "Do not warn him") and, in §4.5, "Do not repeat
    the 'never measured' claim."
  - "Note for the health skills — 2026-10-02" callouts at the top of Safe Doses, Prilocaine + Lidocaine, the Product
    Guide and other injection pages (about keeping dose limits there).
  None was acted on.
