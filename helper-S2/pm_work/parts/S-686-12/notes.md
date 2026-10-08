# S-686-12 Hopman 2017 — working notes

## 1. Right-paper check
- PDF: `papers/S-686-12 - Hopman 2017 - Articaine and neurotoxicity - a review.pdf`, 6 pages, A4, created 2 Oct 2017 (InDesign).
- Title on PDF page 1: "Articaine and neurotoxicity – a review"; authors A. J. G. Hopman, J. A. Baart and H. S. Brand
  (ACTA / VU Medical Centre, Amsterdam); "Refereed Paper. Accepted 31 July 2017"; "DOI: 10.1038/sj.bdj.2017.782".
- Running footer: "BRITISH DENTAL JOURNAL | Advance Online Publication | OCTOBER 3 2017" — this is the advance-online
  version (pages 1–6), not the paginated print issue (Br Dent J 2017;223:501-506). Same article, same DOI; page numbers
  used everywhere are PDF pages 1–6.
- Matches papers_list.csv (PMID 28972589, DOI 10.1038/sj.bdj.2017.782). Right paper: yes.
- Text quality: ok. Reading-order text checked against renders of PDF pages 1 and 5 (pdftoppm, 70 dpi) — identical.
  Table 1 (PDF page 3) read in the layout view. Fig. 1 (PRISMA flow, PDF page 2) is text in the extraction.
- No funding statement and no conflict-of-interest statement anywhere in the PDF (grep + visual check of pages 1 and 5);
  only an acknowledgement for linguistic correction (PDF page 5).

## 1b. Every "Hillerup" in the paper (grep -i hillerup over the whole text; three mentions, all = reference 21)
1. PDF page 3, Table 1 row: "2001–2007 | DNK | 78% | 41% | – | Data from the DMA, a Danish national database for
   prescription medication. Marketshare based on data DMA. | Hillerup et al., 2011" (+ subgroup row "Subgroup of patients
   examined by oral surgeon.").
2. PDF page 5 (Discussion): "Therefore, the overrepresentation of sensibility disorders for articaine might be related by
   the use of articaine by younger, less experienced dentists. This suggestion is rejected by Hillerup and colleagues.21
   In their investigation, 11 patients had damage to two branches of the trigeminal nerve. This is considered highly
   improbable as the result of mechanical damage done by an injection needle."
3. PDF page 6, reference 21: "Hillerup S, Jensen R H, Ersbøll B K. Trigeminal nerve injury associated with injection of
   local anaesthetics: needle lesion or neurotoxicity? J Am Dent Assoc 2011; 142: 531–539."
- Reference 21 is also cited without the name on PDF page 4 ("Another study in Denmark used data from the Danish Medicines
  Agency.21" and "...with a market share of 19.4%.21") and PDF page 5 ("while used in a concentration of 3% the opposite
  was found.21" — a prilocaine formulation figure, not quoted in results).
- No mention anywhere of: sciatic, electrophysiology, stereology, Anesth Analg 2011, Bakke, Larsen, Thomsen, Gerds.
  The only "Anesth Analg" reference is Malet 2015 (ref 29).
- 34 references in total; none is Hillerup, Bakke, Larsen, Thomsen & Gerds 2011.

## 2. Claim screen (all 320 claims, masked viewer pm_work/tools/claims_view.py)
Regexes run with `claims_view.py grep` (claim, elements, reason, proposed, review, evidence quote):
- `articain` -> 22 claims (C049–C064 except C058/C059/C062 text, C078, C079, C080, C084, D000, D005, D006, D007, D053)
- `paraesth|paresth` -> 6 (A091, C050, C056, C057, D015, D033)
- `neurotox` -> 7 (A089, C050, C055, C057, C089, D004, D016)
- `nerve (injur|damage)|neuropath.*(injection|block)` -> 38 (botulinum, adjuvant, procaine, SFN pages + articaine set)
- `lingual|trigeminal|alveolar|mandibular` -> 10; `market share|adverse event|pharmacovigil|yellow card|FAERS` -> 1 (C056)
- `Hillerup|Garisto|Gaffen|Haas|Pogrel|Piccinni|Legarth|Rahn|Zahedi|Nickel|Malamed` -> 6 (C049–C052, C056, D005)
- `Malet|Werdehausen|Ribeiro|Baroni|Hopman|28972589|Lambert|Saray|Jeng|Oertel|Brandt|Yapp|Becker` -> 6 (C050, C052, C053, C061, C062, C064)
- `prilocaine` -> 18; `dental|dentist|oral surg|mouth` -> 10; `concentration-dependent|higher concentration|...` -> 5;
  `cell culture|cell line|neuroblastoma|in vitro|cytotox` -> 5; `only (review|systematic)|systematic review|no review` -> 6.
Read closely (claims_view.py show): C049–C064, D004, D005, D007, D013, D016, C031, C067, C093.
Kept (Hopman bears on them):
- C050 own question.
- C057 "The one systematic attempt to settle the question came out undecided" — Hopman 2017 is itself a literature review
  of articaine neurotoxicity/paraesthesia with a two-database search, PRISMA flow and dual full-text reading, and it ends
  undecided -> a second systematic attempt (predates Stirrup & Crean 2019).
- C061 "no citing paper has contradicted it" (papers citing Malet 2015) — Hopman cites Malet 2015 (ref 29) and reports its
  ranking without contradicting it -> one more citing paper that agrees; verdict unchanged (da Silva 2022/Rodrigues da Silva 2025).
- C056 prospective study of a defined population — Hopman describes Malamed 2001 (ref 5): phone follow-up of 1,325
  people, paraesthesia lasting from under a day to 18 days -> supports the existing narrowed verdict.
- C063 "The evidence of harm comes entirely from drug delivered inside a nerve sheath" (elements include cell culture) —
  Hopman's refs 27–29 (Werdehausen 2009, 2012; Malet 2015): articaine killed neuronal (neuroblastoma) cells in culture in a
  concentration-dependent way; ref 26 Ribeiro 2003: articaine in rat subcutaneous tissue caused an inflammatory reaction.
- D005 (and C049 in part) — Hopman's ref 10, Saray 2003: single intrafascicular lidocaine injection in rat sciatic nerve,
  oxidative-damage marker and walking-track impairment for weeks -> another source for the existing refuted verdict.
Dropped (read, Hopman does not bear on them):
- C049 (design element histology/morphometry not met by Saray; already refuted by Farber 2013); C051 (Hopman discusses no
  intraneural articaine study); C052 (Hopman's animal studies: Ribeiro 2003 implant, Baroni 2013 24 h — no stereology;
  consistent with confirmed, nothing to add); C053 (Hopman only re-describes Baroni 2013; the Baroni full text is S-686-01's;
  Hopman adds no second perineural study); C054/D007 (Ribeiro 2003 is implantation of soaked paper cones under rat skin, not
  an injection into skin, and no duration); C055, C058, C059, C060 (no 2-vs-4 concentration trials in Hopman), C062 (Hopman
  does not report Baroni's adrenaline-only arm result), C064 (Hopman gives no concentration-to-LC50 ratio); C031 (Hopman is a
  modern review but quotes no anaesthetic-duration figures — not a review "that sets the rankings"); C067 (prilocaine
  duration — not in Hopman); C093 (Hopman says only that articaine and lidocaine inflammatory responses did not differ in
  Baroni 2013; Baroni's own text is S-686-01's); D004, D013, D016 (no diabetic-nerve, skin-nerve-fibre or tissue-ranking
  study in Hopman).
- Filter-rule skips: no claim on the articaine-wheals or comparison pages that Hopman bears on has a dose-ceiling,
  toxicity-threshold, antidote or injection-recipe subject; none skipped for this paper. (D073 "epinephrine caps … per
  dental cartridge" seen in the `dental` grep — Safe Doses Of Intradermal Analgesics: 1 claim not tested: dose or toxicity
  subject; not re-judged.)

## 3. PubMed (connector; every search piped to pmcache.py; count shown)
- `Hillerup S[Author] AND articaine` -> COUNT 3: 21531935 (Hillerup, Jensen & Ersbøll, J Am Dent Assoc 2011;142:531-9 =
  Hopman ref 21), 21467556 (Hillerup, Bakke, Larsen, Thomsen & Gerds, Anesth Analg 2011;112:1330-8 = the rat sciatic-nerve
  study, CONFIRMED PMID 21467556), 16343853 (Hillerup & Jensen, Int J Oral Maxillofac Surg 2006;35:437-43).
  Abstract of 21467556 (already cached, redacted, by S-686-01; not overwritten): intraneural saline vs two articaine
  concentrations only — no other anaesthetic compared; 3-week electrophysiology + stereology.
- lookup_article_by_citation (Hopman refs): r2 22822998, r3 17175824, r4 21531931, r5 11217590, r6 10916328, r7 20592403,
  r8 8017646, r9 21273966, r10 14515234, r11 21628435, r13 7736335, r15 19840499, r16 17612365, r17 23316560,
  r18 25420896, r19 9435991, r26 14959905, r27 19700777, r28 22012177, r29 25514420, r30 22458536, r31 2077986,
  r32 22369553, r33 ambiguous -> 12733413 (Malamed, Allergy and toxic reactions to local anesthetics, Dent Today 2003;22:114-21;
  the other candidate 12901057 is an AED article), r34 12636123. r21 = 21531935 (search above).
  Not in PubMed: r1 (book), r12 (book chapter), r14 Haas & Lennon 1996 J Dent Res abstract, r20 Legarth 2005, r22 Rahn 2000,
  r23/r24 NMT reports, r25 Zahedi 2012 (thesis).
- `Legarth J[Author] AND lingual` -> COUNT 0; `Tandlaegebladet[Journal] AND lingualis` -> COUNT 0.
- `Rahn R[Author] AND Ultracain` -> COUNT 3 (10588556 Oertel 1999, 9435991 Oertel 1997 = ref 19, 1816813 Rahn 1991) — the ZWR
  2000 paper is not among them; `Rahn R[Author] AND 2000[dp] AND (Nebenwirkungen OR Lokalanästhesie OR local anesthesia)` -> 0.
- `Haas DA[Author] AND Lennon D[Author]` -> COUNT 2 (7736335 = ref 13; 7736333 = their 1993 Ontario use survey, the source
  of the market-share figure). The 1996 J Dent Res abstract (ref 14) is not in PubMed.
- Abstracts read: 21467556, 21531935, 16343853, 19700777, 22012177, 25514420, 14959905, 14515234, 8017646, 11217590,
  20592403, 19840499, 7736335, 7736333, 25420896, 17612365, 23316560, 12636123, 2077986, 12901057, 12733413, 10588556, 1816813.
- Cached (pmcache.py article): 19700777, 22012177 (verbatim); 25514420 (LD50 values -> [dose figure omitted], --redacted);
  14959905, 14515234, 21531935 (concentration figures -> [dose figure omitted], --redacted, as S-686-01 did for 21467556).
- Abstract-vs-Hopman checks: Ribeiro 2003 abstract says articaine and mepivacaine caused less inflammation than bupivacaine
  and lidocaine the least (Hopman: articaine higher than lidocaine, "comparable with the other anaesthetics"); Gaffen & Haas
  2009: 182 reports 1999–2008, 64 of them in 2006–2008 (Hopman p3: "When the period between 1999 and 2008 was studied, 64
  cases of paraesthesia were identified" — the 64 belong to 2006–2008); Lambert 1994 exposed desheathed bullfrog sciatic
  nerves in vitro (Hopman p1 calls it "Direct injection"); Werdehausen 2009 ranks procaine equal to articaine (Hopman lists
  articaine as least toxic, omitting procaine). None of these slips bears on a claim.
- Brief's examples Skjevik 2011 and Hillerup 2006 are NOT cited or discussed by Hopman (grep: no "Skjevik"; Hillerup only ref
  21). Hillerup & Jensen 2006 = PMID 16343853 (found in the Hillerup search above).

## 4. Notion (read-only: notion-search and notion-fetch only)
### Searches (query -> number of results returned; page_size 25)
- "Hopman articaine neurotoxicity review" -> 18 (articaine-wheals, Comparing…, Procaine / Novocaine, Reference, Injectables
  ruled out but not tried, Ropivacaine Wheals, bupivacaine-wheals, mepivacaine-wheals, "Results", Safe Doses…, What is still
  unsettled…, Product Guide, Rugby Dibucaine product page, two Turbocaína Zeyco articaína product pages, Folic Acid, Needle
  Size for Intradermal Injections, Longer Relief Intradermal Wheals). No highlight contains "Hopman".
- "28972589" -> 25, none relevant (no page shows the PMID; unrelated hits on numbers).
- "sj.bdj.2017.782" -> 20; only articaine-wheals is relevant and its hit is the Yapp 2011 BDJ DOI (sj.bdj.2011.240), not Hopman.
### articaine-wheals — https://app.notion.com/p/3c510b7903aa816f989ad4276f79887e — as of 2026-10-02T03:14:14.446Z
(= the version the claims were tested on). Fetch saved to file; parsed as JSON; no truncated / unknown_block_count /
unknown_block_ids keys present; text 65,980 characters.
Term counts in the fetched text: Hopman 0; 28972589 0; "Br Dent"/"British Dental" only Yapp 2011 and Stirrup & Crean 2019;
Hillerup 17; Malet 6; Werdehausen 0; Malamed 0; Ribeiro 0; Baroni 6; Garisto 2; Gaffen 1; Haas 4; Piccinni 2; Pogrel 0;
Stirrup 2; Goffin 2; Skjevik 0. => the page does not cite Hopman 2017 anywhere.
Verbatim sentences relied on (dose figures replaced):
- (What happens when articaine is injected into a nerve?) "The finding still stands. Twenty-nine papers have cited it in the
  fifteen years since. **None of them contradicts it**, and the paper carries no retraction, correction or expression of
  concern. Later reviews describe it accurately and draw the obvious conclusion from it — that anesthetic concentration
  should be kept as low as the job allows."
- (What do the reports from dental practice show?) "The one systematic attempt to settle the question came out undecided."
  followed by the Stirrup and Crean (2019) description; Sources entry for Stirrup & Crean: "The only systematic attempt to
  answer the question, and it comes out undecided".
- (same section) "Haas and Lennon reviewed 21 years of reports from dentists in Ontario, Canada. The overall risk of
  paresthesia after a local anesthetic injection was about **1 in 785,000 injections**." (an event incidence, not a dose).
- (Sources — Reports from dental practice) "**Piccinni C and colleagues.** Paraesthesia after local anaesthetics: an
  analysis of reports to the FDA Adverse Event Reporting System. *Basic and Clinical Pharmacology and Toxicology* 2015. —
  Among all local anesthetics, only articaine and prilocaine produced a paraesthesia signal, strongest in dentistry.
  Limits: as above." ("above" = the Garisto entry: "Limits: voluntary reports compared against sales, which cannot separate
  events from reporting behaviour.")
- (What does the laboratory say about damage to nerve cells?) heading answer "That articaine is among the gentlest of the
  group." … "That does not make the measurement wrong, and no citing paper has contradicted it. It does mean the single most
  favourable published fact about articaine's safety was produced by the company that sells it, and it should be weighted
  accordingly." … "A second cell-line study compared the drugs as they come out of the cartridge." (Albalawi 2018).
  Sources (Malet entry): "Limits: **the first author's affiliation is Scientific Affairs, Septodont, which manufactures
  articaine and sells it in Mexico as Medicaine** — the most favourable published safety fact about the drug comes from its
  maker." (Malet's and the page's lethal-concentration values are toxicity figures: not copied anywhere.)
- (What is not known) "**The true rate of paresthesia attributable to articaine is unresolved and may not be resolvable**
  from the data that exists, because voluntary reporting cannot separate a drug that causes more events from a drug that
  attracts more reports. What would settle it: a prospective study following a defined population of injections rather
  than collecting reports. None exists." (C056; covered by the claim update, no separate finding.)
- Also read: the Hillerup design paragraph, the Baroni paragraph, "How can articaine be gentle in a dish…", the
  practical-steps list (C063 sentence; the injection-technique sentence beside it is not reproduced), "What is not known",
  and the Sources entries for Malet, Albalawi, Hillerup, Baroni, Goffin, Haas & Lennon, Garisto, Piccinni, Stirrup & Crean.
### Other pages fetched (all parsed from saved JSON; none had truncated / unknown_block_count / unknown_block_ids set;
### "Hopman", "28972589" and the Hopman DOI occur on none of them)
- Comparing the injectable local anesthetics for intradermal wheals — https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b
  — as of 2026-10-02T03:14:02.626Z. Hillerup 2 (the rat study only), Malet 7, Werdehausen 2 (both for ropivacaine vs
  lidocaine), paraesthesia 1 (reporting described as the weakest source). Relevant sentence, accurate on its natural reading
  (no finding): "**The dish ranking also comes with an interest.** The first author of the study behind it works in
  Scientific Affairs at Septodont, which manufactures articaine and sells it in Mexico, and the paper's stated conclusion is
  that "among dental anesthetics, articaine is the least neurotoxic"." (The page's lethal-concentration arithmetic is a
  toxicity-figure passage: not read further, not copied.)
- Injectables ruled out but not tried — https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5 — as of
  2026-10-02T03:14:22.080Z. Cites Werdehausen 2009 (PMID 19700777) and 2012 (PMID 22012177) in its tetracaine section and
  gives their orderings with articaine at the gentle end, matching the abstracts. No finding.
- Ropivacaine Wheals — https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e — as of 2026-10-02T03:14:26.511Z
  (399,446 chars; findings only, S1 tests it). Section "6.8a Four adjacent literatures on repeated or prolonged exposure":
  "**1. Dental repeated injection — the closest thing to a repeated same-site human record.** `ABSTRACT-ONLY` Dentistry
  injects local anaesthetic into small tissue volumes repeatedly over decades. Pogrel 2000, Hillerup 2011 and Gaffen & Haas
  2009 establish that **persistent paraesthesia after dental blocks is real but rare**, with **articaine and prilocaine
  disproportionately implicated**, and an unresolved debate over whether the cause is needle trauma or the neurotoxicity of
  concentrated agent. `INFERENCE` Relevant because it is the only body of human evidence on cumulative local anaesthetic
  exposure at a site — but it concerns **nerve-trunk blocks with [dose figure omitted] solutions**, not dermal wheals, and
  it never measures fibre density." Same three sources listed again under "Adjacent literatures on repeated or prolonged
  exposure" (all ABSTRACT-ONLY). No full citation for "Hillerup 2011" anywhere on the page (ambiguous between PMID 21531935
  and PMID 21467556; the dental-paraesthesia context points to 21531935).
- mepivacaine-wheals — https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185 — as of 2026-10-02T03:14:08.315Z; and
  bupivacaine-wheals — https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d — as of 2026-10-02T03:14:18.695Z.
  Articaine appears only in the Malet three-band grouping (matches Hopman's account). No finding.
- 2 — Reference — https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65 — as of 2026-10-01T02:05:48.095Z
  (1,279,938 chars; the two "truncated" strings in the text are page content about MEDLINE/Vademécum truncation, not fetch
  truncation). articaine 10 mentions, all in §4.9.3 "Ropivacaine and articaine injectables" and dose/label lines; Hillerup,
  Malet, Garisto, Haas, Hopman 0. Sentence relied on: "**Articaine carries the field’s one clinical argument that
  concentration itself is neurotoxic.** A Danish registry study found neurosensory disturbance markedly over-represented for
  articaine [dose figure omitted] in mandibular blocks and attributed it to the drug rather than the needle; …" The rest of
  that paragraph (a trial, an umbrella review, and a concentration recommendation) is not reproduced. The same section's
  dose-ceiling lines are not reproduced (filter rule).
- 1 — Product Guide — https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f — as of 2026-10-02T03:14:29.224Z
  (599,993 chars). Articaine appears only in the two Turbocaína product rows and label-ceiling lines (not reproduced);
  "excluded on the reader’s instruction rather than on any evidence about articaine itself". No finding.
- 5 — Soft ground in these documents — https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 — as of
  2026-09-26T18:26:13.509Z (fetched inline, read in full): no articaine, dental or nerve-injury content. No finding.
- What is still unsettled… — https://app.notion.com/p/3d410b7903aa819f8300e976a62577db — as of 2026-09-26T18:23:10.973Z.
  Articaine only inside the Malet lethal-concentration line (toxicity figures: not copied); ropivacaine-vs-lidocaine entry
  cites Werdehausen consistently with Hopman. No finding.
- What was searched for and does not exist… — https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82 — as of
  2026-09-27T00:27:49.877Z: no articaine, dental, paraesthesia, injected-anaesthetic or cell-culture entry. No finding.
- What transfers from diabetic neuropathy trials… — https://app.notion.com/p/3d410b7903aa813681e9c27892149a17 — as of
  2026-09-26T18:27:17.888Z: "paraesth"/"neurotox" hits are acetyl-L-carnitine trials only. No finding.
- prilocaine-wheals — https://app.notion.com/p/3c510b7903aa8159a5d9e4447ec15409 — as of 2026-10-02T03:14:12.541Z.
  Sentences relied on: "**On the unfavourable side: the [dose figure omitted] dental solution carries the strongest
  paresthesia signal of any local anesthetic.**"; "An earlier review of 21 years of Canadian reports put the absolute rates
  in perspective: about 1 in [dose figure omitted] overall, about 1 in 1,250,000 for the 2 and [dose figure omitted]
  solutions, and about 1 in 588,000 for [dose figure omitted] prilocaine (Haas and Lennon, 1995)." (the masked first figure
  is the 1-in-785,000 incidence, masked only because the viewer treats "injections" as a unit); Sources (Haas & Lennon):
  "Limits: voluntary reports over 21 years divided by estimated injection counts, so both numerator and denominator are
  approximate; and the rates are for dental injections, overwhelmingly lower-jaw nerve blocks." Piccinni Sources entry
  describes its design correctly ("spontaneous reports with no denominator, so this measures reporting patterns rather than
  incidence"). Methaemoglobin threshold and label-ceiling lines on this page: not read further, not copied.
- Turbocaína Zeyco articaína, 50 dental cartridges — https://app.notion.com/p/3e010b7903aa811396d4de6b6f5dbd32 — as of
  2026-09-24T01:13:13.976Z; and 50 glass cartridges — https://app.notion.com/p/3e010b7903aa814c8faec76e19774fd7 — as of
  2026-09-24T01:13:57.010Z (Buying Decisions & Info). Literature statement: "no wheal study used articaine or an anaesthetic
  with epinephrine, so its evidence is indirect twice over, from one uncontrolled study of plain lidocaine." Hopman has no
  wheal study; no finding. (Their Edits property quotes removed dose-ceiling text: not reproduced.)
- Anaesthetics (hub) — https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492 — as of 2026-10-01T03:07:38.200Z: no
  articaine/paraesthesia/neurotoxicity statement (one "<unknown" string in the text, not near any relevant content).
- Safe Doses Of Intradermal Analgesics — https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7 — as of
  2026-10-02T03:13:58.754Z: articaine 24 mentions, all dose/label content; no neurotoxicity, paraesthesia or Hillerup
  statement. Not read further (filter rule). No finding.
- Needle Size for Intradermal Injections — https://app.notion.com/p/21f74377f6384dc7a9760ea6709e69c0 — as of
  2026-09-25T07:30:00.218Z (returned inline): articaine only as a cartridge/packaging and dose-arithmetic item; no literature
  statement Hopman bears on. Nothing reproduced.
- Lidocaine With Epinephrine Wheals — https://app.notion.com/p/3c610b7903aa801c906fcde8b5c43674 — as of
  2026-09-26T18:28:27.736Z: "The neurotoxicity literature on local anesthetics points at the anesthetic’s own
  concentration and the length of exposure rather than at anything else in the vial." — consistent with Hopman's
  concentration explanation. No finding.
- The intradermal wheal literature nobody cites… — https://app.notion.com/p/3d410b7903aa8107a042d4e7f6540c1a — as of
  2026-10-02T03:14:04.610Z: no articaine content. No finding.
- Procaine / Novocaine — https://app.notion.com/p/31910b7903aa80d1a022fa3b5cb01b5c — as of 2026-09-26T18:25:29.323Z.
  Section "The ester question": "The amides — lidocaine, mepivacaine, bupivacaine, ropivacaine, prilocaine, articaine — are
  joined by an amide bond instead, are not cut in plasma, and are cleared by the liver." Hopman p1: articaine's thiophene
  ring "also contains an additional ester group"; Hopman's ref 19 (Oertel 1997, PMID 9435991): the ester group "is quickly
  hydrolysed by esterases" and "blood and serum are the sites of metabolism". -> finding.
- adjuvants-without-a-vasoconstrictor — https://app.notion.com/p/3d310b7903aa81fbb5b9e999637c362a — as of
  2026-10-02T03:14:20.685Z: no articaine/Hillerup/paraesthesia content. No finding.
- Results (procaine neural therapy) — https://app.notion.com/p/32a10b7903aa804bac71f3523e07a298 — as of
  2026-09-13T07:38:52.775Z; Research — https://app.notion.com/p/32a10b7903aa80ba9acdc20255958302 — as of
  2026-09-26T18:24:59.524Z; Permanent-Harm Risk Of The Candidates For The Urge To Tense —
  https://app.notion.com/p/3e510b7903aa812b9b8bfc7e2135a943 — as of 2026-10-01T03:15:21.643Z; Longer Relief Intradermal
  Wheals — https://app.notion.com/p/3c410b7903aa80e39bdafb3c09285c07 — as of 2026-09-14T01:21:23.625Z (an empty link hub):
  no articaine or dental-paraesthesia content. No finding.
### Further Notion searches
- "articaína cartuchos dental" -> 23; "Medicaine Septodont articaine epinephrine" -> 17; "articaine paresthesia nerve damage
  dental reports" -> 16; "Hillerup articaine sciatic nerve" -> 16; "Garisto paresthesia FDA adverse event local anesthetic"
  -> 17; "Haas Lennon paresthesia Ontario 21 year" -> 20. Every relevant page they surfaced is listed above; no articaine
  product page other than the two Turbocaína rows exists in Buying Decisions & Info (Medicaine and Quanteek appear only in
  the articaine-wheals availability table).
### Instructions found inside documents
- None aimed at this work. The "Research" page contains leftover chat text ("Please let me know when you are ready to
  proceed to Part 4…"), which is page content, not an instruction to me; ignored.

## 5. Results written and checks
- Card: results_S2/paper_cards/S-686-12.json. Parts: claim_updates.json (8 entries, 7 claims), extra_studies.json (9),
  notion_findings.json (11), status.json.
- s2check (run twice): no `!!` lines; quotecheck 8/8 claim-update quotes, 9/9 abstract quotes, 11/11 finding quotes found.
  After trimming the incidence ratio from the Haas & Lennon extra-study quote and from F03's notes, the remaining `??`
  lines are: F03 sentence_as_it_stands (the verbatim Notion sentence's "1 in 785,000 injections" — an event incidence,
  not a dose) and percentages of cases/market share in F09/F10 notes and the F10 quote — allowed.
- Not done / could not reach: nothing paywalled was needed (all abstracts via the PubMed connector). Not in PubMed: Hopman
  refs 1, 12, 14, 20, 22, 23, 24, 25. Baroni's full text was not read here (S-686-01 has it); the count of twenty-nine
  citing papers in C050 was not judged (as instructed).
- No content-filter stop occurred.
- Cache note: S-686-01 re-saved a_19700777 (Werdehausen 2009) and a_14959905 (Ribeiro 2003, unredacted) a few minutes
  after I cached them; my abstract quotes from both still match their versions (quotecheck 9/9).
- Temporary working files (Notion text extracts parsed from the saved fetches, and three small helper scripts) were kept
  only in the session scratchpad (notion_S-686-12/, tools_S-686-12/), not in the repository.
