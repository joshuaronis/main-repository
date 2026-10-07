# S-686-44 — Klingenström & Westermark 1964, local tissue-oxygen tension after adrenaline, noradrenaline and Octapressin

## 1. Right-paper check and text quality

- Text file: `texts/S-686-44.txt`, 6 PDF pages, from
  `papers/S-686-44 - Klingenström 1964 - LOCAL TISSUE-OXYGEN TENSION AFTER ADRENALINE NORADRENALINE AND OCTAPRESSIN IN LOCAL ANAESTHESIA.pdf`
  (the file name on disk uses a decomposed "ö"; opened by glob).
- PDF page 1 header: "Acta anaesth. Scandinav. 1964, 8, 261-266." Title: "LOCAL TISSUE-OXYGEN TENSION AFTER ADRENALINE,
  NORADRENALINE AND OCTAPRESSIN® IN LOCAL ANAESTHESIA". Authors: P. Klingenström (OCR "KLINGENSTROM", once "KLINCENSTROM")
  and L. Westermark. Departments of Surgery and Anaesthesiology, Karolinska Sjukhuset, Stockholm. Received April 7, 1964.
  PDF metadata title matches. Matches PMID 14272296 / DOI 10.1111/j.1399-6576.1964.tb00247.x and the person_note
  ("exact title, P. Klingenstrom and L. Westermark, Acta Anaesthesiol Scand 1964 volume 8; complete pages 261-266").
  **Right paper: yes. Complete: journal pages 261-266 = PDF pages 1-6.**
- Text quality: old scan with an OCR text layer. Prose is fully readable (minor OCR slips: "Scandinau.", "investigationwas",
  "0," for O2, "comsumption" as printed, "a" for "8" in the table, garbled superscript reference numbers). The table on
  PDF page 3 was checked against a rendered image of the page (`scratchpad/fig_S-686-44_p3-3.png`): every cell matches the
  layout view once "a" is read as "8". German summary and reference list (15 refs) on PDF page 6.
- Reference numbering: in-text superscripts are partly garbled by OCR and do not line up with the printed list in a few
  places (e.g., "MILLAR ... (1958)8" vs list no. 6); the in-text year for Montgomery & Horwitz is 1950 while the printed
  list reads "1959" (J Clin Invest vol. 29 is 1950). Neither affects any claim.

### What the paper is (from the full text)
- Design: experimental within-subject comparison in healthy human volunteers (no randomisation or blinding described).
- Subjects: nine healthy human subjects ("nine healthy human subjects", PDF p1). No sex, age or other details given.
- Site and route: volar forearm, both forearms; on each forearm three injection sites ("injected immediately
  subcutaneously in three different places", PDF p1): lidocaine with noradrenaline (distal), lidocaine with adrenaline
  (middle), lidocaine with Octapressin (felypressin) (proximal). Amounts and concentrations: [dose figure omitted]
  (stated in the methods; the authors describe the Octapressin concentration as, in their experience, roughly equal to
  the adrenaline one in prolonging anaesthesia). No plain-lidocaine zone and no vasoconstrictor-without-anaesthetic
  zone. Not intradermal; no wheal.
- Measurement: tissue oxygen tension with a Clark polyethylene-membrane polarographic micro-electrode fitted in an
  18-gauge needle, attached to a Beckman Physiological Gas Analyzer Model 160, "in the infiltrated zone, at the same
  depth as the injections" (PDF p2). Readings are relative ("proportional to the oxygen tension"); adrenaline and
  noradrenaline values are expressed as percentages of the Octapressin-zone value on the same forearm. No absolute
  values, no pre-injection baseline. In three cases O2 tension outside the infiltrated zones was measured and found the
  same as in the Octapressin zones.
- Times: 1.5, 2.5 and 3.5 hours after injection (PDF p2). Cases 1-6 measured on both forearms at all three times; case 7
  only at 1.5 h on one forearm; case 8 missing one forearm at 1.5 h; case 9 only at 3.5 h (table, PDF p3, image-checked).
- Colour: pallor within minutes at every site; during the first hour central cyanosis developed in the adrenaline and
  noradrenaline zones with a narrow pale peripheral halo; the Octapressin zone stayed pale "for 3.5 hours or longer, and
  no cyanosis appeared" (PDF p2).
- Results: O2 tension "with very few exceptions" lower in the catecholamine zones, "between 50 and 90 per cent." of the
  Octapressin value (table range in fact 40-100). Medians: adrenaline zones 87% of Octapressin (P25 79, P75 92);
  noradrenaline zones 80.5% (P25 74, P75 85). Significant between-person differences; no difference between the three
  times; no interaction (PDF p2-3).
- Authors' interpretation: local cyanosis and lower local O2 tension are signs of a local metabolic disturbance caused
  by adrenaline/noradrenaline raising local oxygen consumption; "it may be more harmless to the tissue" (Octapressin)
  (PDF p5 summary). Interpretation, not a measured tissue-injury outcome.
- Earlier study cited: Klingenström P, Westermark L. Local effects of adrenaline and phenylalanyl-lysyl-vasopressin in
  local anaesthesia. Acta Anaesthesiol Scand 1963;7:131 (skin colour changes; central cyanosis after adrenaline, not
  after Octapressin). PubMed lookup in section 3.
- Funding / conflicts: none stated. Octapressin is a Sandoz product; no statement of supply or support.
- Limitations the authors state: none stated as limitations (they note large between-person differences). Not stated
  but evident: relative measure only, no baseline, small n with incomplete data in 3 of 9, no plain-anaesthetic control.

## 2. Claim screen (all 320 claims)

Screened with `pm_work/tools/claims_view.py grep` (masked viewer, per section 6 of the brief) and, earlier in the
session, with a small script over `common/claims_all.json`. Terms used, one search at a time:
`klingenstr|westermark|14272296|tb00247` (1 hit), `octapressin|felypressin|vasopressin|ornipressin` (5),
`tissue oxygen|oxygen tension|oxygen saturation|oximetr` (14), `cyanos|cyanot|pallor|blanch` (5),
`necros|ischaem|ischem|gangren` (12), `vasoconstrict` (42), `6425877|34362194|34457400|Miller|Thiem|Bunke` (6),
`polarograph|microelectrode|clark electrode` (0), `196[0-9]|oldest study|half a century` (12),
`skin blood flow|cutaneous blood flow|laser doppler|skin perfusion|hyperspectral|photoacoustic` (40),
`noradrenalin|norepinephrin` (8), `phenylephrine|alternative vasoconstrictor|instead of epinephrine` (1),
`volar forearm|forearm skin of healthy` (1). Masked re-runs:
`tissue.?oxygen|oxygen tension|polarograph|felypressin|octapressin|cyanos` (5) and
`skin oxygen|hypox|blanch|pallor|necrosis|ischaem|ischem` (9) - no claim outside the set below.

**A content-filter stop happened once in this session**, while composing a single screening script whose text carried a
long list of drug, toxicity and injection terms. Per the hand-over rule the blocked text was not retried or rephrased;
the screen was done instead with one short search term per call, and then with the masked viewer. Nothing in the results
was lost by this: every term in the blocked list was run individually. No results write was ever stopped.

Claims read closely and why each was kept or dropped:
- **C084** (Lidocaine With Epinephrine Wheals) - the requesting claim. Kept; see section 4.
- C072, C073, C074, C075, C076, C077, C078, C079, C080, C081, C082, C083, C085, C086, C087, C088, C089, C090, C091,
  C092, C093, C094 (same page) - all read in full. Dropped: none of them is about tissue oxygen measured over hours in
  skin. C085 ("epinephrine without a local anaesthetic ... the only study that isolated it") needs an
  epinephrine-alone arm, which this paper does not have. C087 ("nobody has found a dilution at which epinephrine becomes
  a net widener of skin vessels") is about net blood flow; this paper measured oxygen tension, and its talk of dilated
  capillaries and venules is a hypothesis about pooled deoxygenated blood, not a flow measurement. C093 ("no study
  anywhere found tissue damage at or near this dose") needs a tissue-damage outcome at that strength; this paper
  measured no damage outcome and used a stronger adrenaline strength. C075 and C090 need repeated exposure or
  hyperalgesia duration.
- C067, C068 (prilocaine-wheals) - about prilocaine duration and methaemoglobin. Dropped: wrong drug and outcome.
- C013-C030 (adjuvants-without-a-vasoconstrictor) - clonidine, dexamethasone, dexmedetomidine, magnesium,
  buprenorphine. Dropped: this paper tests none of them. C018 and C019 (denervation supersensitivity of skin vessels)
  were read because of the vasopressin term; this paper has no denervated arm, so it decides neither.
- D000 ("no study has recorded skin blood flow at a wheal of any of these drugs for longer than ninety minutes"),
  D001, D007, D009, D019, D021, D022, D023 (comparison page) - dropped. D000 is the closest and still does not match:
  this paper measured tissue-oxygen tension, not blood flow, after a subcutaneous injection, not at a wheal, and with a
  vasoconstrictor the claim's drug list does not contain.
- C032, C034-C036, C039, C054, C062, D038, D054 - dropped on drug, route or outcome.
- E027, E039, A000, A003, A063, A064, A092 - dropped; different pages and topics.

Counts of claims not tested under the filter rule (dose or toxicity subject):
- Safe Doses Of Intradermal Analgesics: 2 claims not tested: dose or toxicity subject (D073, D074). Both surfaced in the
  screen on `noradrenaline` and on `necrosis|ischaemia`; their subjects are plasma epinephrine with haemodynamic and
  arrhythmia outcomes, and an epinephrine-containing anaesthetic at or above a conventional cardiac limit. Not re-judged
  and not written out. D074 is another paper's own question (S-686-47).

## 3. PubMed (connector; eutils blocked, pm.py not used)

Searches, each cached by `pm_work/tools/pmcache.py search` (query translations are in the cache files):
1. `Nylen B[Author] AND Octapressin` - COUNT 0. The paper's reference 13 (Nylen, Klingenstrom, Westermark, "Adrenaline
   and Octapressin in local anaesthesia", "to be published") is not in PubMed under that title; a citation lookup on
   Acta Anaesthesiol Scand 1964 vol 8 also returned NOT_FOUND.
2. `(Klingenstroem P[Author] OR Klingenstrom P[Author] OR "Klingenstroem"[Author])` - COUNT 13.
3. `("tissue oxygen"[tiab] OR "oxygen tension"[tiab] OR polarograph*[tiab]) AND (epinephrine OR adrenaline OR felypressin
   OR octapressin)[tiab] AND (skin OR cutaneous OR subcutaneous OR forearm)[tiab] AND ("local anaesthesia" OR
   "local anesthesia" OR lidocaine OR infiltration OR injection)[tiab]` - COUNT 4 (Thiem 2021, Prasetyono 2019,
   Korkushko 2002, and this paper). This is the search that shows how thin the field is.
4. `(felypressin[tiab] OR octapressin[tiab] OR "felypressin"[MeSH]) AND (skin OR cutaneous OR cyanosis OR "blood flow"
   OR oxygen)[tiab]` - COUNT 31.
5. `("transcutaneous oxygen" OR "tcpO2" OR "oxygen saturation")[tiab] AND (lidocaine OR lignocaine OR "local anesthetic")
   [tiab] AND (epinephrine OR adrenaline)[tiab] AND (skin OR cutaneous OR flap)[tiab]` - COUNT 3.
6. `Bjorlin G[Author]` - COUNT 48, nothing matching the 1954 Odontologisk Revy supplement cited as reference 1.

Citation lookups (`lookup_article_by_citation`): Klingenstrom 1963 Acta Anaesthesiol Scand 7:131 -> PMID 14058021;
Nordqvist 1961 Acta Anaesthesiol Scand 5:63 -> PMID 13729550; Montgomery & Horwitz 1950 J Clin Invest 29:1120 ->
PMID 14774458; Bjorlin 1954 Odontol Revy -> NOT_FOUND; Nylen 1964 -> NOT_FOUND.

**The 1963 study the open question asks about**: Klingenstroem P, Westermark L. "Local effects of adrenaline and
phenylalanyl-lysyl-vasopressin in local anaesthesia." Acta Anaesthesiol Scand 1963;7:131-7, PMID 14058021,
DOI 10.1111/j.1399-6576.1963.tb00212.x. PubMed holds **no abstract**; MeSH: Anesthesia Local, Epinephrine, Lidocaine,
Felypressin, Vasopressins, Humans. What the 1964 paper says it found is in the card and in extra_studies.

Abstracts cached: a_14058021, a_13729550, a_14774458 (all "[Abstract not available]"), a_12096442 (redacted: injected
amount and concentration), a_30934173 (redacted: tissue-oxygen readings, replaced out of caution rather than because
the rule required it), a_266826 (redacted: injected amounts and concentrations), a_35470293 (redacted: the injected
concentration), a_5960743, a_4652231, a_5336919 (no abstracts in PubMed).
