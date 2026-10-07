# S-686-47 — Troullos 1987, plasma epinephrine and cardiovascular response after dental local anaesthesia

Writing rules applied throughout: no drug amount, concentration, volume, number of injection sites or frequency
is written anywhere (they appear as `[dose figure omitted]`); no plasma epinephrine level is written as a figure;
percentages of change in heart rate or blood pressure are kept out of all wording; the conventional limits are
named only as "above" or "below", never with their figures.

## 1. Right-paper check

- Text file: `texts/S-686-47.txt`, 4 PDF pages, from
  `papers/S-686-47 - Troullos 1987 - Plasma epinephrine levels and cardiovascular response to high administered doses of epinephrine contained in local .pdf`
  (scan with an OCR text layer, PDF created 2007 by "Apex PDFWriter").
- PDF page 1: "PRELIMINARY COMMUNICATION"; title "Plasma Epinephrine Levels and Cardiovascular Response to High
  Administered Doses of Epinephrine Contained in Local Anesthesia"; authors "Emanuel S. Troullos, D.M.D., David S.
  Goldstein, M.D., Ph.D., Kenneth M. Hargreaves, D.D.S., Ph.D., Raymond A. Dionne, D.D.S., Ph.D."; "Pain Research
  Clinic, National Institute of Dental Research, Bethesda, Maryland"; running footer "ANESTHESIA PROGRESS" /
  "JANUARY/FEBRUARY 1987"; journal pages 10-13; "Received December 8, 1986; accepted January 23, 1987".
  Matches the assigned paper (PMID 3472472, Anesth Prog 1987, no DOI). **Right paper: yes.**
- `person_note` in common/papers_list.csv: "Earlier free Nexus request remains on record; paper later obtained
  through Sci-Hub Research." (how the copy reached the packet; nothing for this session to do — the PDF was
  already in the packet and no further copy was sought.)
- Text quality: **ocr, readable**. All four page images were rendered (pdftoppm, 110 dpi) and compared with the
  text where numbers matter: subject numbers (15; men 9, women 6; groups 10 and 5), mean age, ASA class,
  sampling times (1, 4, 8, 12, 20 min), F/d.f./p values and the adverse-event counts all match the images.
  OCR oddities: "µg" appears as "ug", ",ug", "jig" or "Ag"; superscript reference numbers are run into the text
  (e.g. "effect.1'2", "terminals.1416", "Clutter et a/.\"7"); the Fig. 1 axis labels are garbled in the
  text layer but legible in the image; Table 1 has some lost "±" signs ("387.046b,c" = "387.0±46b,c").
  Nothing is missing: summary, introduction, methods, results, Fig. 1 (3 panels), Table 1, discussion and
  17 references are all present. The paper has no abstract other than the "Summary", no funding statement
  and no conflict-of-interest statement.
- No instructions aimed at the reader were found inside the paper.

## 2. Claim screen (all 320 claims in common/claims_all.json)

Fields searched: claim, elements_said_absent, reason, proposed_wording, evidence_quote, review, records_read,
needs_full_text (script in the session scratchpad, `s47/screen.py`). Term groups and hit counts:
- epinephrine / adrenaline: 60 claims (C014 C015 C017-C022 C024 C032 C034-C036 C039 C040 C046 C048 C053 C054 C056
  C060 C062 C066 C067 C072-C087 C089-C094 D000-D002 D007 D009 D011 D013 D023 D034 D054 D056 D069 D073 D074 E027)
- catecholamine / noradrenaline / norepinephrine: 8 (C017 C018 C019 C084 C094 D073 D074 E027)
- plasma / serum / blood level / systemic absorption / circulating: 19 (A003 A004 A011 C014 C054 C069 C070 C071
  C077 C088 D023 D034 D066 D069 D070 D071 D072 D073 D074)
- haemodynamic / heart rate / blood pressure / cardiac / cardiovascular / coronary / ischaemia / arrhythmia /
  hypertension: 15 (A000 A002 A029 A032 A055 C068 C069 C071 C089 C092 C094 D065 D073 D074 E000)
- dental / cartridge / oral surgery / third molar / intraoral / inferior alveolar: 14 (C044 C056 C057 C060 C067
  C068 C078 C079 C080 D073 D074 E012 E014 E016)
- authors and PMID (troullos, dionne, goldstein, hargreaves, 3472472, and the cited/related authors chernow,
  cioffi, niwa, neves, vanderheyden, cassidy, clutter, holroyd, cheraskin, fiset): 2 (C094 — a different Goldstein
  paper, 1986, PMID 3517118, in records_read; D074)
- tremor / vasovagal / anxiety / syncope: 1 (C008, botulinum toxin crossover — irrelevant)
- second sweep over claim text and elements for: systemic, absorb, palpitation, side effect, adverse, heart, pulse,
  toxic, overdose, ceiling, maximum, caps, 1987, healthy volunteer, young, oral surgery, extraction, molar, mouth,
  intraoral: 29 claims, each looked at (A036 A037 A054 A059 C000 C025 C029 C031 C046 C047 C050 C054 C056 C061 C064
  C071 D004 D007 D014 D016 D040 D041 D050 D063 D069 D071 D073 D075 E035 E037).
85 claims hit at least one group; all were read at least at claim + elements level, and these were read in full
(claim, elements, verdict, evidence, proposed wording, reason, records_read): C014 C017 C018 C019 C054 C068 C069
C071 C077 C084 C088 C089 C092 C094 D023 D034 D069 D070 D071 D072 D073 D074 D075 E027.

Kept: **D074 only** (own question; see section 3).

Dropped, with reason:
- C094 (catecholamine clearance versus drainage as risk factors for skin ischaemia): Troullos measured systemic
  absorption after intraoral injection, not skin ischaemia or local clearance mechanisms; the Goldstein in its
  records is a different paper.
- C072-C087, C089-C093 (Lidocaine With Epinephrine Wheals: skin blood flow, tissue oxygen, nerve effects, duration,
  necrosis, concentration series): all concern local tissue effects or duration; Troullos has no local or duration
  outcome. C089 (Neal 2003 the only review of epinephrine's nerve effects): Troullos is a primary study of systemic
  effects, not a review of nerve effects.
- C014 C015 C017-C022 C024 (clonidine / alpha-2 / denervation supersensitivity / adjuvants): different drugs and
  outcomes.
- C031 C044 C047 D040 D050 D063 C029 C046 D014 (healthy-volunteer / mouth-tissue duration figures): about duration
  or nerve-fibre figures; Troullos measured neither.
- C054 C056 C057 C060 C062 C053 C066 C067 D000-D002 D007 D009 D011 D013 D023 D034 D054 D056 D065 D066 (articaine,
  prilocaine, procaine, ropivacaine duration, flow, damage, injection pain): no overlap in drug, outcome or design.
- C068 C069 C071 (methaemoglobin series): different outcome; C071 also has a dose limit as part of its subject.
- C077 (drug concentration in epidermis versus dermis): Troullos measured plasma, not skin layers.
- C088 (laser Doppler after a plain lidocaine wheal in neuropathic skin): no overlap.
- D070 (ropivacaine infiltration in chronic pain): no overlap.
- D075 (citation classification, methaemoglobin): out of scope already; no overlap.
- E027, E012, E014, E016, A-series and E035/E037 hits: matched only on generic words (norepinephrine reuptake
  inhibitors, dental eugenol trial, heart/pulse words in unrelated contexts).

Claims skipped under the filter rule (subject is a dose ceiling, a toxicity threshold, an inter-session interval or
a preparation step) among the candidates above — counted, text not written out, not re-judged:
- Safe Doses Of Intradermal Analgesics: 4 claims not tested: dose or toxicity subject (D069, D071, D072, D073).
  For D073 (whether the per-appointment epinephrine figures apply outside the mouth), note also that Troullos is an
  intraoral study and would add nothing to a limb-infiltration question in any case.
- 💉 Lidocaine With Epinephrine Wheals: 1 claim not tested: preparation / mixing subject (C091).
- articaine-wheals: 1 claim not tested: dose or toxicity subject (C064).
D074 is also a ceiling-adjacent claim; it is answered only because it is this paper's own question, in the limited
way the hand-over allows ("above" / "below" the conventional limit, no figures).

## 3. PubMed (connector; eutils blocked)
- get_article_metadata 3472472: "Plasma epinephrine levels and cardiovascular response to high administered doses of
  epinephrine contained in local anesthesia." Anesth Prog 1987;34(1):10-3; authors Troullos ES, Goldstein DS,
  Hargreaves KM, Dionne RA; Journal Article; no DOI; **free PMC copy PMC2186227**. Matches the PDF. (Abstract not
  cached: it carries the administered amounts, which this paper's rule keeps out of every file, and no quote is taken
  from it.)
- lookup_article_by_citation, all 17 references in one batch (the tool returns the PMID in the "key" field):
  r1 Holroyd 1960 → 13715514; r3 JADA 1955;50:108 (New York Heart Association report) → NOT FOUND; r5 Cheraskin 1959 →
  13610589; r6 Fiset 1986 → 3465257; r7 Chernow 1983 → 6639234; r8 Cioffi 1985 → 3861687; r9 Dionne 1984 → 6731889;
  r10 Goldstein 1982 → 7134364; r11 Cassidy 1986 → 3544965; r12 Nelson 1974 → 4430113; r13 Goldstein 1981 → 7207028;
  r14 Vincent 1982 → 6282296; r15 Majewski 1983 → 6304105; r16 Rand 1984 → 6321064; r17 Clutter 1980 → 6995479.
  Refs 2 (Malamed, Handbook of Local Anesthesia, 1st ed., 1980) and 4 (ADA, Accepted Dental Therapeutics, 40th ed.,
  1984) are books, no PMID.
- get_article_metadata for all 15 PMIDs above: abstracts read where present (Holroyd, Cheraskin, Nelson, Goldstein
  1981: "[Abstract not available]"). Citation errors inside the paper's own reference list: ref 11 Cassidy is given as
  1987 (PubMed: 1986;33(6):289-97); ref 17 Clutter is given as 1984 (PubMed: 1980;66(1):94-101); ref 1 third author
  "Welsh" (PubMed: Welch); ref 6 second author "Ramsey" and fourth "Weinsein" (PubMed: Ramsay, Weinstein).
- get_article_metadata 11740477 (Niwa 2001) and 17589629 (Neves 2007): checked that D074's existing wording describes
  them correctly — Niwa: 27 patients with cardiovascular disease (NYHA I–III), impedance cardiography after an
  intraoral injection of lidocaine with epinephrine; Neves: randomised, 62 patients with coronary artery disease, lidocaine with vs without
  epinephrine, 24-hour ambulatory blood pressure and dynamic ECG. Both descriptions hold.
- search_articles (max 40): `(plasma epinephrine OR plasma catecholamine*) AND (dental OR intraoral OR oral surgery)
  AND (local anesthe* OR lidocaine) AND (cardiac OR cardiovascular disease OR coronary OR hypertensive)` →
  **count 39**, all 39 returned and screened by title/abstract (cache s_mcp_6f2a79d74cfc7b33.json). PubMed's
  translation expands "plasma epinephrine" to plasma[MeSH/All] AND epinephrine[Supplementary Concept/MeSH/All]
  (adrenalin, adrenaline, epinephrin…), "dental" to dental health services[MeSH] OR dental, "oral surgery" to
  surgery, oral[MeSH] OR oral surgical procedures[MeSH], and the disease terms to heart[MeSH] OR cardiac OR
  cardiovascular diseases[MeSH] OR coronary OR hypertension[MeSH] OR hypertensive.
  Kept (bear on D074; abstracts cached):
  - 2213464 Davenport 1990, J Periodontol — double-blind crossover trial in 9 stable cardiovascular-disease patients,
    lidocaine with epinephrine vs plain lidocaine during periodontal surgery; plasma epinephrine rose within minutes
    with no significant change in heart rate or mean arterial pressure. Amount not stated in the abstract. Cached
    with its plasma-level figures replaced by [dose figure omitted] (--redacted), because this paper's rule keeps
    plasma epinephrine levels out of every file; nothing else in it was changed.
  - 9481971 Meechan 1997, Anesth Prog — 14 patients under treatment for hypertension, blood pressure, heart rate and
    plasma potassium before and after an epinephrine-containing dental anaesthetic; the amount (from the volume and
    concentration in the abstract) is above the conventional cardiac-patient figure. Comparative study of two
    antihypertensive-drug groups, not a trial of epinephrine against none. Cached verbatim (no ceiling in it).
  Noted, not kept: 2978662 Hirai 1988 (hypertensive patients, haemodynamics and plasma catecholamines during dental
  treatment; Japanese, no abstract — content not verifiable); 2527244 Troullos 1989 J Clin Endocrinol Metab (same
  NIDR group, 26 awake third-molar patients, double-blind, epinephrine vs no epinephrine, plasma epinephrine,
  beta-endorphin, pulse and systolic pressure — a later companion study, healthy patients); 2099281 Sakurai 1990,
  2808867 Knoll-Köhler 1989, 3145958 Salonen 1988, 6948029 Tolas 1982, 16170480 Takahashi 2005, 16182162 Viana 2005,
  16037765 Meral 2005, 17082283 Hersh 2006, 8448101 Lipp 1993, 11409642 Nakamura 2001 (all healthy volunteers or
  healthy patients, plasma epinephrine and/or haemodynamics after epinephrine-containing dental anaesthesia — none in
  cardiac patients); the rest are reviews, animal work, other drugs or other questions (41710613, 26780408, 20681379,
  15917682, 10472225, 9681407, 9075040, 9206410, 7607744, 7992901, 1842159, 1911676, 1925848, 2132316, 1971472,
  2507667, 3205554, 3582472, 3009759, 5078436).
- Connector notice: every get_article_metadata result carried an "important_legal_notice" asking for PubMed
  attribution and DOI links. It is the connector's own boilerplate, not text inside a paper; PMIDs and DOIs are given
  in the result files anyway.

## 4. Notion (read-only: only notion-search and notion-fetch were used)

### 4.1 Safe Doses Of Intradermal Analgesics
- Fetched https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7 — "as of 2026-10-02T03:13:58.754Z" (same version
  the main session tested); 65,027 characters, saved by the tool to a file and searched with Python; no
  `truncated` / `unknown_block_count` / `unknown_block_ids` markers present. Path: Health / Health Pages; verification
  "unverified".
- **The page does not cite Troullos 1987.** Searched the fetched text for: Troullos, troullos, 3472472, 1987,
  Goldstein, Dionne, Hargreaves, "Anesth Prog", "Anesthesia Progress", the paper's own amount phrase ([dose figure omitted]), "high administered",
  "Plasma Epinephrine", "plasma epinephrine", "New York Heart", 1955, Niwa, Neves, Malamed, Chernow, Cassidy,
  Vanderheyden, pubmed, doi.org — 0 hits for each. The paper reached D074 through the main session's PubMed search
  (it is in D074's records_read), not through a citation on the page.
- D074's sentence sits in "Sources" › "### Epinephrine", in the Bennett CR, Monheim's Local Anesthesia and Pain
  Control in Dental Practice, 7th ed., 1984 entry (the cardiac-disease figure). Verbatim, figures omitted:
  "**Limits:** a textbook recommendation from 1984 with no supporting trial; later reviews state plainly that
  scientific evidence supporting this dose is lacking. It is here because it is the figure clinicians actually work
  to, not because it is measured." (In claims_all.json the year "1984" was itself replaced by [dose figure omitted].)
  So "the conventional cardiac-patient limit" in D074 is Bennett's 1984 cardiac-disease figure, the lower of the two
  epinephrine figures on the page.
- Other epinephrine passages read in context: "## Epinephrine has its own ceiling" (both per-appointment figures,
  a ratio-to-amount table, row-by-row arithmetic, and an own-use passage), "## What is still unknown", "### Where the
  maxima come from", the Moodley 2017 entry (healthy-adult figure) and the Liu 1994 entry. Every epinephrine
  sentence there either has a ceiling or dose arithmetic as its subject (counted, not copied), is the user's own use
  (marked "Own-use marker (2026-10-01)"), or concerns duration and skin blood flow, which Troullos does not touch.
- Count for this page, sentences whose subject is a ceiling and which touch the paper's topic: 2 sentences not made
  findings: dose or toxicity subject (the Moodley entry's Limits note on the healthy-adult figure, and the section
  "Epinephrine has its own ceiling"). Note for the main session, without figures: Troullos reports plasma epinephrine
  rises, haemodynamic changes and adverse reactions (tremor, one vasovagal reaction) in young healthy patients after
  an amount below the healthy-adult figure that the page and the paper both cite ("submaximal" in the paper's words);
  that bears on the healthy-adult figure's Limits note, whose subject is a ceiling, so it is not made a finding here.
- The opening "Route and absorption" passage says absorption after tissue injection has a time course and is
  site-dependent (lower blood levels after subcutaneous administration than after more vascular blocks). Troullos is
  consistent with it (rapid uptake from vascular oral tissue, peak at the first sample); no finding.
- The page carries a callout addressed to "the health skills" (2026-10-02) recording the user's ruling to keep the
  dose limits on this page. It is record-maintenance data, not an instruction to this session; nothing was done
  with it.
- Findings from this page: none from Troullos beyond the D074 claim update (see section 5).

### 4.2 Notion searches (AI search; results are candidates only — every page relied on was fetched and grepped)
| query | page_size | results | relevant pages surfaced |
|---|---|---|---|
| Troullos | 25 | 25 | none (journal, Spanish/German vocabulary, Health History, Todoist extracts — no exact match) |
| plasma epinephrine after dental local anesthesia heart rate blood pressure | 25 | 14 | prilocaine-wheals, Safe Doses, Procaine / Novocaine, Lidocaine With Epinephrine Wheals, bupivacaine-wheals, articaine-wheals, Anaesthetics, the intradermal wheal literature page, 6 lidocaine-with-epinephrine product pages (Buying Decisions & Info) |
| epinephrine cardiac patients local anaesthetic cardiac dose limit | 25 | 14 | Safe Doses, Needle Size for Intradermal Injections, Lidocaine With Epinephrine Wheals, Anaesthetics, Procaine / Novocaine, Ropivacaine Wheals, Comparing the injectable local anesthetics, a Health History plan entry (2026-08-22), bupivacaine-wheals, SFN intradermal vs subcutaneous routing analysis, articaine-wheals, product pages, an Outstanding Work page |
| systemic effects of epinephrine absorbed from injection palpitations tremor | 25 | 15 | same cluster, plus Health History entry 2026-08-27 and "Permanent-Harm Risk Of The Candidates For The Urge To Tense" |
| Dionne Goldstein Hargreaves epinephrine | 25 | 15 | same cluster (no author match) |
| 3472472 | 25 | 25 | none (Health History food/worry entries, Todoist extracts — no match) |
| Plasma epinephrine levels and cardiovascular response to high administered doses of epinephrine contained in local anesthesia | 25 | 15 | same cluster plus prilocaine-wheals (Cecanho 2006 felypressin entry) and Pisacaína product pages |

### 4.3 💉 Lidocaine With Epinephrine Wheals
- Fetched https://app.notion.com/p/3c610b7903aa801c906fcde8b5c43674 — "as of 2026-09-26T18:28:27.736Z" (same as the
  version tested); 332,305 characters, saved to a file and searched with Python; no truncated / unknown-block markers
  (the word "truncated" occurs twice, both in the page's own prose about abstracts).
- **Does not cite Troullos 1987**: 0 hits for Troullos, 3472472, Dionne, Hargreaves, "New York Heart", 1955, Niwa,
  Neves, Chernow, Cioffi, Cassidy, Clutter, Holroyd, Cheraskin, Fiset, Malamed, Monheim, "plasma epinephrine",
  "Anesth Prog". The "1987" hits are Larrabee 1987 and Flavahan 1987; "Goldstein" is Eisenhofer, Esler, Goldstein,
  Kopin 1990 (neuronal removal of circulating catecholamines); "Bennett" is Bennett GJ (Drummond 2014).
- Passages on systemic epinephrine, read in context:
  - "### The quantity, so the scale does not get lost" (in "What narrows the margin in a neuropathic leg"): the
    amount in a wheal and a session set against the dental per-appointment figures and an auto-injector, ending
    "**Systemic effect is not the concern here.** The local effect on the injected patch of skin is, and that is set
    by the concentration in the fluid touching those vessels rather than by the total in the body." Subject: a
    ceiling comparison and a safety judgement — counted, not made a finding.
  - "### Systemic effects, for the record": first sentence sets a session's amount against the per-appointment
    figures (ceiling subject, counted); then "Palpitations, tremor or a pounding headache after a session would be
    unexpected enough to be worth reporting rather than tolerating." (advice, not a literature statement); then
    "Two studies bear on this from the other side. Dunlevy’s 81 patients and O’Malley’s 23, all under general
    anesthesia with volatile agents that make the heart more sensitive to adrenaline, and all receiving [dose figure
    omitted] of epinephrine-containing solution — [dose figure omitted] the volume of a single wheal — recorded no
    adverse cardiac events, no raised blood pressure and no fast heart rate in any group, including [dose figure
    omitted]." That sentence is accurate as written and does not claim exclusivity, so no finding. For the main
    session's information only: direct measurements of plasma epinephrine and haemodynamics in awake patients after
    epinephrine-containing dental local anaesthesia also exist (Troullos 1987, PMID 3472472, an amount far larger than
    any wheal session; Chernow 1983, PMID 6639234, an inferior alveolar nerve block, randomised double-blind
    crossover), and Troullos is the one that reports tremor in patients with the highest plasma epinephrine.
- Count for this page: 2 passages not made findings: dose or toxicity subject (the two subsections above).
- Findings from this page: none.

### 4.4 💉 Needle Size for Intradermal Injections (surfaced by search)
- Fetched https://app.notion.com/p/21f74377f6384dc7a9760ea6709e69c0 — "as of 2026-09-25T07:30:00.218Z"; returned
  inline in full (no truncation markers).
- Does not cite Troullos (no Troullos / 1987 / 3472472 / plasma epinephrine / Dionne / Goldstein / Hargreaves).
- Epinephrine passages: the articaine-cartridge arithmetic against both per-appointment epinephrine figures, and a
  source entry "Malamed’s [dose figure omitted] epinephrine limit, as quoted in the Journal of the Canadian Dental
  Association clinical Q&A on epinephrine in patients with cardiovascular disease" with "Limits: a widely quoted
  expert recommendation rather than a trial result, framed per dental appointment; the article states it as the most
  frequently quoted suggestion, not as a consensus threshold." Both have a ceiling as their subject — counted, not
  made findings. Troullos does not bear on who first proposed the cardiac figure (it cites neither Malamed nor
  Bennett for it; see the card), so it settles nothing here. Side observation for the main session (not a finding,
  not from this paper): this page attributes the cardiac-disease quotation to Malamed, while Safe Doses attributes
  the same quotation to Bennett CR, Monheim's 7th ed., 1984.
- Count for this page: 2 passages not made findings: dose or toxicity subject.

### 4.5 💊 Anaesthetics (surfaced by search)
- Fetched https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492 — "as of 2026-10-01T03:07:38.200Z"; 55,346
  characters, saved to a file; no truncation markers.
- Does not cite Troullos. Epinephrine appears only in product/sourcing tables, the Kopacz 1989 and Cederholm 1992 /
  1994 skin-blood-flow summaries, and revision notes. The "Safety before purchase" section describes local-anaesthetic
  systemic toxicity and its hospital treatment (toxicity / antidote subject) — counted, not made a finding.
- Count for this page: 1 passage not made a finding: dose or toxicity subject. Findings: none.

### 4.6 Other pages fetched and grepped (all read-only; none cites Troullos 1987)
| page | url | as of | size / truncation | what was looked at | result |
|---|---|---|---|---|---|
| Comparing the injectable local anesthetics for intradermal wheals | https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b | 2026-10-02T03:14:02.626Z | 105,800 chars, file; no markers | Troullos / authors / plasma / systemic / cardiac | no Troullos; only "systemic" is prilocaine methaemoglobin (toxicity subject); no finding |
| articaine-wheals | https://app.notion.com/p/3c510b7903aa816f989ad4276f79887e | 2026-10-02T03:14:14.446Z | 65,980 chars, file; no markers | same | no Troullos ("Anesthesia Progress" hit is Albalawi 2018); BP/HR mentions are a dental trial comparing two articaine concentrations; no finding |
| Ropivacaine Wheals (other session tests it; findings only) | https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e | 2026-10-02T03:14:26.511Z | 399,446 chars, file; no markers | same | no Troullos (1987 hits = Winsor, Larrabee, Åkerman & Evers, Covino; Anesth Prog hits = Kimi 2012, Yamashiro 2016; Bennett = Xiao & Bennett 2008); nothing on systemic epinephrine; no finding |
| mepivacaine-wheals (findings only) | https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185 | 2026-10-02T03:14:08.315Z | 67,421 chars, file; no markers | same | no Troullos; no systemic / cardiac / heart-rate statements; no finding |
| bupivacaine-wheals (findings only) | https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d | 2026-10-02T03:14:18.695Z | 84,250 chars, file; no markers | same | no Troullos; "cardiac" hits are bupivacaine cardiotoxicity (toxicity subject, 3 passages counted); no finding |
| 2 — Reference (source register S1–S457) | https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65 | 2026-10-01T02:05:48.095Z | 1,279,938 chars, file; no markers ("truncated" twice in prose) | Troullos, 3472472, Goldstein, Dionne, Hargreaves, 1987, 1955, Bennett, and all 17 epinephrine mentions | **no register entry for Troullos**; 1987 / 1955 / Bennett hits are other works; epinephrine mentions are label ceilings, a toxicity-management passage and the reader's own exclusion of epinephrine products — counted, no finding |
| 1 — Product Guide | https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f | 2026-10-02T03:14:29.224Z | 599,993 chars, file; no markers | same | no Troullos; epinephrine products "excluded here on the reader’s instruction after a bad reaction to injected epinephrine, not on the evidence"; palpitation/tremor hits are local-anaesthetic toxicity signs (toxicity subject); no ranking rests on Troullos; no finding |
| 5 — Soft ground in these documents | https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 | 2026-09-26T18:26:13.509Z | inline, complete | whole page read | no epinephrine content at all; no finding |
| What is still unsettled across these pages… | https://app.notion.com/p/3d410b7903aa819f8300e976a62577db | 2026-09-26T18:23:10.973Z | 61,415 chars, file; no markers | Troullos / epinephrine / systemic / cardiac | no question about systemic epinephrine, plasma levels or the cardiac-patient figure; no open question answered |
| What was searched for and does not exist… | https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82 | 2026-09-27T00:27:49.877Z | 64,683 chars, file; no markers | same | no epinephrine entries; no finding |
| prilocaine-wheals (surfaced by search) | https://app.notion.com/p/3c510b7903aa8159a5d9e4447ec15409 | 2026-10-02T03:14:12.541Z | 76,671 chars, file; no markers | felypressin-vs-epinephrine cardiovascular sentences (Inagawa 2010 rabbits; Kyosaka 2019 older adults) | not contradicted by Troullos (heart rate up with epinephrine is consistent); methaemoglobin / antidote passages counted; no finding |
| Procaine / Novocaine (surfaced by search) | https://app.notion.com/p/31910b7903aa80d1a022fa3b5cb01b5c | 2026-09-26T18:25:29.323Z | 51,850 chars, file; no markers | same | no cardiac / systemic / heart statements; no finding |
| Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection Routing Analysis | https://app.notion.com/p/39410b7903aa8046b3eef25af516245f | 2026-09-26T18:19:51.310Z | 100,336 chars, file; no markers | same | no Troullos; "systemic" hits are general local-vs-systemic delivery; no finding |
| 🔬 The intradermal wheal literature nobody cites… | https://app.notion.com/p/3d410b7903aa8107a042d4e7f6540c1a | 2026-10-02T03:14:04.610Z | 76,264 chars, file; no markers | same | no Troullos; no finding |
| adjuvants-without-a-vasoconstrictor | https://app.notion.com/p/3d310b7903aa81fbb5b9e999637c362a | 2026-10-02T03:14:20.685Z | 95,940 chars, file; no markers | same | no Troullos; one mixing passage (recipe subject) counted; no finding |
| PiSA Lidocaína/Epinefrina … dental cartridge (Buying Decisions & Info) | https://app.notion.com/p/3e010b7903aa81059294ec5f6c29f711 | 2026-09-27T10:59:06.263Z | inline, complete | literature statements | only "no wheal study used an anaesthetic with epinephrine…" (Troullos is not a wheal study; no pain outcome); no finding |
Not fetched: "What transfers from diabetic neuropathy trials…" (not on this paper's topic) and the topical hub; Health
History entries that surfaced (2026-08-22 plan, 2026-08-27 result) are the person's own experiences, not literature
statements, and were left alone.

Counts of passages not made findings because their subject is a ceiling, toxicity threshold, antidote or recipe
(touching this paper's topic only): Safe Doses 2; Lidocaine With Epinephrine Wheals 2; Needle Size 2; Anaesthetics 1;
bupivacaine-wheals 3; Reference 3 (label ceilings, toxicity management, a second ceiling passage); Product Guide 3
(ceilings, toxicity signs, toxicity management); prilocaine-wheals 2 (methaemoglobin signs and treatment);
adjuvants-without-a-vasoconstrictor 1 (mixing passage).

**Notion findings: none.** No page cites Troullos 1987; no sentence on any page read is made wrong, overstated or
understated by it; nothing marked unverified is verified by it; no open question is answered by it.

## 5. Own question and results written

**Own question** ("how many subjects, were any cardiac patients included, and what total epinephrine amount was given
relative to the conventional cardiac limit?"): 15 subjects (10 lidocaine with epinephrine, 5 plain mepivacaine), open
parallel-group design not described as randomised; **no cardiac patients** — all were young healthy ASA I oral-surgery
outpatients (PDF p. 1); the total epinephrine given was **above** the conventional cardiac-patient limit (the Bennett
1984 figure on Safe Doses). For context, without figures: it was **below** the ADA maximum for healthy patients that the
paper cites (hence the authors' word "submaximal", p. 4) and **below** the older 1955 New York Heart Association figure
for cardiac patients that the paper also cites (p. 1).

Files:
- results_S2/paper_cards/S-686-47.json — card; 17 key-result quotes, 3 author-limitation quotes, 17 cited works
  (14 with PMIDs; the 1955 NYHA report, Malamed's handbook and ADA Accepted Dental Therapeutics have none).
- pm_work/parts/S-686-47/claim_updates.json — 3 entries, all D074: own-question (narrowed → narrowed, deciding quote
  p. 1, uncertain_after false) and two extra-study entries (Davenport 1990, Meechan 1997; narrowed → narrowed).
  The proposed wording for D074 is the same in all three entries; it changes the main session's wording in three
  ways: Troullos is now described as young healthy patients with no cardiac patients and an amount "above the
  figure" (not "a much larger amount"); Davenport 1990 and Meechan 1997 are added as cardiovascular-patient studies;
  "textbook recommendation" is written "textbook figure" (the year 1984 restored — claims_all.json had replaced the
  year itself with [dose figure omitted]).
- pm_work/parts/S-686-47/extra_studies.json — 2 entries (2213464, 9481971), both bearing on D074, both found by the
  PubMed search this paper prompted, neither in its reference list.
- pm_work/parts/S-686-47/notion_findings.json — [] (no findings; see 4.x).
- PubMed cache: a_2213464.json (redacted: plasma levels), a_9481971.json, s_mcp_6f2a79d74cfc7b33.json.
- s2check: clean on the first run (no !! or ?? lines; 3 claim-update quotes and 2 abstract quotes found).

## 6. Not reached, problems, instructions found
- Nothing unreachable: the PDF was in the packet; PubMed lookups and the Notion pages all returned. The 1955 New York
  Heart Association report (JADA 1955;50:108) is not in PubMed, so its content was not checked beyond the paper's own
  description; Holroyd 1960, Cheraskin 1959 and Hirai 1988 have no PubMed abstract.
- The task prompt said the Safe Doses page cites this paper; the fetched page (same version the main session tested)
  does not — Troullos entered D074 through the main session's own search (records_read).
- No content-filter stops.
- No instructions aimed at this session were found in the paper or the abstracts. Notion text addressed to "the
  health skills" (the Safe Doses callout recording the user's ruling to keep dose limits on that page) and product-page
  edit logs recording the user's rulings are record-maintenance data, not instructions to this session; nothing was
  done with them. The PubMed connector's "important_legal_notice" (attribution request) is connector boilerplate.
