# S-686-23 — Rames 2026, perioperative liposomal bupivacaine in dermatologic surgery

Writing rule followed throughout: no drug amount, concentration, volume, injection count or interval figure is written
in these notes, the card or the claim updates; where a sentence carried one it reads `[dose figure omitted]`. The
paper's saline-dilution technique for large wounds is mentioned only as "described", without ratios or volumes.

## 1. Right-paper check

- Text file: `texts/S-686-23.txt`, 5 PDF pages, from
  `papers/S-686-23 - Rames 2026 - The Safety of Perioperative Liposomal Bupivacaine Injections in Dermatologic Surgery Patients.pdf`.
- PDF page 1: title "The Safety of Perioperative Liposomal Bupivacaine Injections in Dermatologic Surgery Patients";
  authors "Melissa M. Rames, MD,* Jorge A. Rios-Duarte, MD,* and Nahid Y. Vidal, MD†" (Mayo Clinic, Rochester,
  Minnesota); journal line "Dermatol Surg 2026;52:743– 747"; "http://dx.doi.org/10.1097/DSS.0000000000005031".
  Matches the assigned paper (PMID 41603645, DOI 10.1097/DSS.0000000000005031). **Right paper: yes.**
  `person_note` in `common/papers_list.csv` is empty for this paper.
- Text quality: **ok**, complete (abstract, introduction, methods, results, Table 1 over PDF pp. 3–4, discussion,
  limitations, references 1–23). Extraction oddities to know when quoting: "=" is "5" ("n 5 85"), "≥" is "$"
  ("Patients $18 years old"), "<" is "," ("Patients ,18 years old"), ">" is "." ("(.90%)"), "±" is "6"
  ("acetaminophen 6 nonsteroidal"), "+" is "1" in one place; the umlaut of reference 10 (Mörwald) is split off.
- Internal inconsistencies in the paper itself (not extraction errors): the abstract says "140 LB administrations and
  129 patients", excisions "n 5 88, 62.9%", Mohs "n 5 49, 35%", hidradenitis "n 5 77, 55%", neoplasms "n 5 56, 40%",
  and "no adverse events in 134 out of 136 patients"; the Results and Table 1 say 136 administrations in 127
  patients, excisions 85 (62.5%), Mohs 48 (35.3%), hidradenitis 74 (54.4%), neoplasms 56 (41.2%). Repair types differ
  between text (partial/guided closure 55, 39.3%; secondary intention 52, 38.2%) and Table 1 (52, 38.2%; 51, 37.5%);
  median total wound length is 15.4 cm in abstract and table, 15.5 cm in the text. The "72 hours" duration statement
  in the introduction cites reference 3 (Firoz 2010, a Mohs pain survey), not the label.
- No instructions aimed at the reader were found inside the paper.

## 2. Claim screen (all 320 claims in common/claims_all.json)

Method: Python regex over claim text, elements, reason, proposed wording, evidence quote, review, records read and
needs_full_text (a first pass that also included the query strings was too noisy, because most anaesthetic queries
OR-in bupivacaine). Term sets used:
1. liposom, exparel, sustained, extended-release, long-acting, slow-release, depot, microparticle, microsphere,
   posimir, xaracoll, zynrelef, HTX-011, SABER, DepoFoam, SKY0402, multivesicular → 22 claims (with query strings).
2. bupivacaine, marcaine, exparel, liposom (non-query fields) → 57 claims.
3. systemic toxicity, LAST, toxicit, cardiotox, seizure, overdose, plasma, intravascular, antidote, lipid emulsion → 33.
4. mohs, dermatolog, surgical site, excision, hidradenitis, nausea, adverse event, chart review, retrospective,
   postoperative, skin graft, donor site, wound → 40.
5. case report, been reported, no case, no report, systemic, side effect, harm, complication, infiltrat,
   subcutaneous → 114 (read the plausible ones only; see below).
6. admix, compatib, displac, same syringe, mixture, mixed with → 21.
7. cited authors and PMIDs: Apseloff, Rames, Viscusi, Dagenais, Aggarwal, Kharitonov, Artz, Jensen, Zadrazil, Sessler,
   Ilfeld, Gitman, Mörwald, Mulroy, El-Boghdadly, Manson, Limthongkul, Sniezek, Firoz, Giordano, Soltani, Grant,
   Chang, Jin, 41603645, 23458225, 15220782 → 12 (+2 for "Jin", both unrelated).

Read closely, with the decision:
- **D048** (own question) — kept; see claim_updates.
- **D045, D046, D047, D049, D052** (same page; cinchocaine/tetracaine/ropivacaine wheals, citation behaviour) — dropped:
  no overlap with liposomal bupivacaine or dermatologic surgery.
- **D050** (no measurement of any of the page's drugs, liposomal bupivacaine included, in neuropathic leg skin) —
  dropped: Rames has no neuropathy population and measured no duration; its sites were mostly axillae, groin,
  anogenital, face and scalp.
- **D051** (no trial of these drugs given intradermally in small fibre neuropathy) — dropped: no SFN population, no
  intradermal route.
- **C043** (sustained-release anaesthetics in human skin; already refuted on Grant 2004 and bupivacaine microcapsules)
  — read; Rames measured no duration of skin anaesthesia. Its reference 5 (Jensen 2024, extended-release microparticle
  bupivacaine given subcutaneously to volunteers) is looked up below as a possible further human example; it cannot
  change a "refuted" verdict.
- **C032** (no post-1994 data on pain of infiltration and duration of dermal bupivacaine; narrowed) — read; Rames
  measured neither. Its reference 19 (Apseloff 2013) is subcutaneous liposome bupivacaine onset in volunteers, already
  in D048's records; not intradermal, so no change.
- **C033, C040** (ester–amide mixtures; bupivacaine–lidocaine intradermal mixtures) — dropped: Rames did not mix
  liposomal bupivacaine with another anaesthetic in a syringe and measured no duration.
- **C023, C026, C027, D019** (adjuvants in skin) — dropped: no adjuvant in Rames.
- **D004, D064, C049, C059, D005, D013, D016** (nerve injury/neurotoxicity) — dropped: Rames recorded no nerve
  outcome.
- **D006, D008, D021, D053, C035, C036** (intradermal duration of plain bupivacaine/ropivacaine/levobupivacaine) —
  dropped: no duration measured in Rames.
- **D020, D026, D027, D030–D044** (relief outlasting the block; SFN trials; Ilfeld 2021 phantom-limb trial) — dropped:
  no pain-durability or neuropathic outcome in Rames. Note: Rames' reference 22 is a different Ilfeld 2021 paper (a
  narrative review of liposomal bupivacaine by infiltration or nerve block), not the phantom-limb trial those claims
  name.
- **C092, C094** (epinephrine necrosis; matched "artz" inside "Hartzell") — dropped.
- **D007, D009, D023** (articaine, prilocaine, procaine in skin) — dropped.
- **T01–T08** — dropped (lipoic acid, wheal trials in neuropathic pain, capsaicin, diclofenac, menthol).

Count lines for claims skipped under the filter rule (subject is a dose ceiling, toxicity threshold, injection
interval or similar, and the claim overlaps with Rames' dosing, labelled-maximum or repeat-administration passages, so it
would otherwise have been read against it):
- Safe Doses Of Intradermal Analgesics: 3 claims not tested: dose or toxicity subject (D069, D071, D072).
  (Three more claims on that page are also dose-ceiling subjects but have no overlap with this paper — epinephrine
  limits and a methaemoglobin citation, D073–D075 — so they were dropped as irrelevant rather than skipped; D070, about
  ropivacaine infiltration in chronic pain, was read and dropped: no overlap.)
- No other page had a dose- or toxicity-subject claim that overlaps with this paper.

Result of the screen: only D048 is decided by this paper. No other claim's verdict is changed by it.

### 2b. Re-screen with the masked viewer (brief §6), after the coordinator's message
`python3 pm_work/tools/claims_view.py grep '<regex>'` (dose figures masked):
- 'liposom|exparel|sustained|extended.release|long.acting|depot|microparticle|microcapsule|methoxyflurane' → 15 claims:
  C013, C023, C032, C042, C043, D003, D019, D034, D045, D048, D050, D051, D058, D071, E041. New compared with §2:
  **C042** (methoxyflurane microdroplets never followed up or replicated; "nothing in the class has replaced it";
  narrowed). Read with `show C042`: its elements are the lecithin-coated microdroplet/microcrystal approach after 1991;
  neither Rames nor its references (Jensen 2024 is a PLGA microparticle; Exparel a multivesicular liposome) match that
  intervention → dropped, no update. The others were already read in §2.
- 'Mohs|dermatolog|hidradenitis|surgical site|excision|chart review|nausea|skin graft|donor site' → 3 (A045, D048,
  E015; A045 and E015 are unrelated — a drug with no trial, topical eugenol).
- 'systemic tox|\bLAST\b|seizure|cardiotox|intravascular' → 2 (A025 registry record; C023 adjuvants) — unrelated.
- cited-author names → 39, all name collisions in unrelated topics except D048 and C032 (both already read).
Strict-elements check (brief §6) on D048: elements are humans + the marketed product + intradermal route. No source
matches all three: Rames and Apseloff (humans, marketed product) are subcutaneous/infiltration; Grant 2004 (humans,
intradermal) is an unmarketed formulation; Hixon 2023 (intradermal layer) is dogs and the veterinary product, and
animals are outside D048's population. So "confirmed" holds under the strict rule.

## 3. PubMed (connector; pm.py blocked by network policy). Every search logged with pmcache.py.

Own-record check: `get_article_metadata 41603645` → Rames MM, Rios-Duarte JA, Vidal NY. Dermatol Surg 2026;52(8):743-747,
DOI 10.1097/DSS.0000000000005031, article type "Journal Article"; abstract cached as `a_41603645.json` (no ceiling,
threshold or antidote passage in it, so not redacted). Matches the PDF.

Reference list → PMIDs (`lookup_article_by_citation`; note: the connector returns the PMID in the field labelled
"key" and echoes my key in "pmid"):
- 1 Limthongkul 2013 → 23464845; 2 Sniezek 2011 → 21561527; 3 Firoz 2010 → 20542176; 4 Giordano 2020 → 31592922
  (Mohs postoperative pain and oral analgesics — acetaminophen, ibuprofen, codeine, opioid prescribing; no local-anaesthetic,
  neuropathic-pain or skin-anaesthesia content, so left out of the card's studies_it_cites_that_matter on purpose).
- 5 Jensen 2024 → 38482995; 6 Aggarwal 2018 → 28538107; 8 Viscusi 2014 → 23446090; 9 Gitman 2018 → 29303925;
  10 Mörwald 2017 → 28079735; 11 Mulroy 2002 → 12430104; 13 Dagenais 2018 → 29745266; 14 Kharitonov 2014 → 24393760;
  15 Chang 2022 → 36054055; 16 Artz 2021 → 34034954; 17 Manson 2020 → 32833710; 19 Apseloff 2013 → 23458225;
  20 Zadrazil 2024 → 38558118; 21 Sessler 2025 → 39520051; 22 Ilfeld 2021 → 33372949; 23 Jin 2021 → 33687173.
- 7 Carroll 2023 (J Anesthesiol Pain Ther) and 12 El-Boghdadly & Chin 2017 (Obstet Anesth Dig, a digest) →
  NOT_FOUND (journals not indexed). The El-Boghdadly & Chin CPD article first appeared in Can J Anaesth 2016 (not
  looked up further; it is a toxicity review).
- 18 is the FDA Exparel prescribing information (2023), not a PubMed record.

Abstracts read (get_article_metadata): 36054055 Chang 2022 (no abstract: research letter); 34034954 Artz 2021 (donor-site
"field block", retrospective cohort, 58 patients); 23458225 Apseloff 2013 (abstract: liposome bupivacaine given
"subcutaneous" in volunteers' arms; **but PubMed's MeSH indexing lists "Injections, Intradermal"** — an indexing
mismatch; full text not free: no PMC id); 38482995 Jensen 2024 (PLGA microparticle extended-release bupivacaine,
subcutaneous, phase 1 dose-ascending, male volunteers; contains a systemic-toxicity passage with dose and plasma figures —
not quoted; if cached it is redacted); 23446090 Viscusi 2014 (pooled 10 RCTs, liposome bupivacaine given "locally at the
surgical site"); 24393760 Kharitonov 2014 (compatibility review; contains mixing/interval/ratio instructions — not
quoted); 33372949 Ilfeld 2021 (review of 76 RCTs; infiltrated LB rarely better than plain bupivacaine); 38558118
Zadrazil 2024 (volunteer ulnar blocks, LB vs plain bupivacaine).

Search S1 (2026-10-07): ("liposomal bupivacaine"[tiab] OR "liposome bupivacaine"[tiab] OR "bupivacaine liposome"[tiab]
OR exparel[tiab]) AND (intradermal[tiab] OR intracutaneous[tiab] OR wheal[tiab] OR wheals[tiab] OR
"Injections, Intradermal"[Mesh] OR subdermal[tiab] OR dermal[tiab]) → **COUNT 4**; translation as typed, each term
mapped to [Title/Abstract], MeSH term to "injections, intradermal"[MeSH Terms]. Records: 38241783 Hixon 2023 (dogs,
veterinary bupivacaine liposome suspension infiltrated "in the muscle/fascia, subcutaneous tissue, and intradermal layer
during closure"; RCT vs saline; animal, veterinary product); 23458225 Apseloff 2013 (hit via the MeSH tag only; abstract
says subcutaneous); 15220782 Grant 2004 (human intradermal, academic liposomal formulation — already in D048's records);
8853095 Mowat 1996 (guinea-pig intradermal wheal model, academic unilamellar liposomes). **No human intradermal study of
the marketed product.**

Search S2 (2026-10-07): ("liposomal bupivacaine"[tiab] OR "liposome bupivacaine"[tiab] OR "bupivacaine liposome"[tiab]
OR exparel[tiab]) AND (Mohs[tiab] OR dermatolog*[tiab] OR "skin cancer"[tiab] OR "cutaneous surgery"[tiab] OR
"skin surgery"[tiab] OR hidradenitis[tiab] OR "skin graft"[tiab] OR "donor site"[tiab] OR
"Dermatologic Surgical Procedures"[Mesh] OR "Mohs Surgery"[Mesh]) → **COUNT 23**, all 23 screened by abstract:
- dermatologic surgery: 41603645 Rames 2026 (this paper); 36054055 Chang 2022 Mohs matched cohort (letter, no
  abstract); 34791645 Yadlapati 2021 "Liposomal bupivacaine infiltration as an effective option ... after Mohs surgery"
  (letter, no abstract); 30148736 Sorenson & Chesnut 2019 review of LB in dermatologic surgery (no abstract);
  31638506 Lewis 2019 skin-cancer resections, LB as "preincision local anesthetic" in 64 of 120 (route not stated).
  None of the four without full text can be read for route (no PMC copy).
- skin-graft donor sites: 34034954 Artz 2021 ("field block"); 34216466 Egan 2021 RCT ("dilute liposomal bupivacaine
  infiltration in a similar fashion" to "standard subcutaneous infiltration"; no benefit over lidocaine);
  34862091 Sadeq 2021 (donor-site infiltration, adolescents/young adults, differences "most likely not clinically
  significant"); 31420265 Boyd 2019 (donor sites, case-control); 29375852 Dissanaike 2017 (case series; free in PMC,
  PMC5771936 — read below); 42580963 Soltani 2026 (already in D050's records).
- bone-graft donor sites, TAP and nerve blocks, breast reconstruction, cleft reviews: 42563223, 41889529, 41885634,
  41042058, 40483489, 40071938, 39894934, 39819091, 38726040, 34183559, 31648962, 29879000 — none intradermal.

Free-copy check (web search, Parallel Search, 2026-10-07): queries "Chang Murad Schmults liposomal bupivacaine Mohs
matched cohort", "liposomal bupivacaine large complex Mohs resections Dermatologic Surgery 2022", "Yadlapati liposomal
bupivacaine infiltration Mohs surgery" → no free copy of Chang 2022 or Yadlapati 2021; Sorenson 2019 not found free
either. Their routes cannot be read (paywalled, no abstract) — recorded as not reached.

PMC full text read: PMC5771936, Dissanaike 2017 (case series, burn donor sites, two cohorts): the marketed product was
"infiltrated into the skin donor site prior to harvesting" after saline dilution, in one cohort admixed with a
tumescent solution; no tissue plane is named and "intradermal" does not occur. Not an intradermal study. (Dose and
dilution figures in it not copied.)

## 4. Notion (read-only: notion-fetch and notion-search only)

### 4a. "🚫 Injectables ruled out but not tried" — https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5
Fetched 2026-10-07; first line "as of 2026-10-02T03:14:22.080Z" (= the version the claims were tested on); saved to file
by the tool (72,962 characters of text); no `truncated`, `unknown_block_count` or `unknown_block_ids` markers in the
text. Path: Health / Health Pages; verification unverified.
Mentions of the paper: none ("Rames", "Mohs", "dermatolog", "Apseloff", "41603645": 0 hits each). Exparel/liposom: 16/48
hits, all in the recommendation bullet, the section "Liposomal bupivacaine and the sustained-release class" and Sources.
Verbatim sentences relied on (dose figures omitted where present):
- Section "The needle settles it before the evidence does": "**The label is also explicit about which routes were
  never studied.** Approved: single-dose **infiltration** and **interscalene brachial plexus nerve block**. Explicitly
  not recommended because not evaluated: **epidural, intrathecal, intravascular, intra-articular, and regional nerve
  blocks other than interscalene.** Contraindicated: obstetrical paracervical block. **Intradermal injection appears
  nowhere — neither permitted nor prohibited, simply never studied with the marketed product.**" (the D048 sentence;
  the next sentence of the paragraph is an admixture/interval instruction and is not copied).
- Sources › Liposomal and sustained-release › EXPAREL label entry: "Approved: single-dose **infiltration** (age 6 and
  over) and **interscalene brachial plexus nerve block** (adults)." ... "\"EXPAREL has not been evaluated for the
  following uses and, therefore, is not recommended for these types of analgesia or routes of administration\":
  **epidural, intrathecal, regional nerve blocks other than interscalene brachial plexus, intravascular or
  intra-articular use.**" ... "**Limits:** **intradermal injection is named nowhere on the label** — it is neither
  permitted nor prohibited, simply not evaluated, so the argument on this page is that a wheal needle is finer than the
  label allows, not that the label forbids the route; the label does not state the particle size; the label read was
  the 2021 revision plus a secondary prescribing-information mirror, and a later revision may exist." (the same entry
  also lists dilution, admixture, interval and maximum-dose figures — not copied.)
- Checked and correct against the abstracts of Rames' own references: the Ilfeld 2021 summary (76 RCTs; 4 of 36;
  11 of 12; 16 of 19 vs 4 of 28; the closing quotation) and the Zadrazil 2024 volunteer ulnar-block result (8 of 25 vs
  25 of 25; residual blockade beyond 3.5 days) — no finding. The LIQ865 (Jensen 2024) bullet matches its abstract except
  that the quoted "prohibit clinical application" reads "prohibits" in the abstract (grammatical adaptation; no finding).
- Page header callout (data, not an instruction to me): a dated note "for the health skills" that the page's dose limits
  stay as the person's injection-safety reference by his ruling. Nothing copied from those limits.

### 4b. Notion searches (notion-search; results are candidates only — every page used was fetched and grepped)
| query | page_size | results | relevant pages surfaced |
|---|---|---|---|
| Rames liposomal bupivacaine dermatologic surgery | 25 | 18 | Injectables ruled out; Permanent-Harm Risk (Urge To Tense); Needle Size; bupivacaine-wheals; Comparing…; prilocaine-wheals; adjuvants…; wheal literature; What is still unsettled; product pages (topical liposomal lidocaine, not relevant) |
| Exparel | 50 | 23 | Injectables ruled out; Needle Size; Permanent-Harm Risk; Future Medications For Urge To Tense; Reference; Product Guide; Routing Analysis; unrelated pages |
| liposomal bupivacaine | 50 | 21 | as above + Research; Relief that outlasts the block |
| Mohs surgery local anesthetic | 25 | 16 | wheal pages, Research, Meta pages — no Mohs content found on fetch |
| local anesthetic systemic toxicity | 25 | 15 | What it is & How it works; Product Guide; Injectables; Reference; Safe Doses; Anaesthetics; a Health History entry (left alone) |
| sustained-release bupivacaine skin intradermal days | 25 | 15 | Injectables; wheal literature; What is still unsettled; Relief…; Needle Size; Comparing…; bupivacaine-wheals; Routing Analysis |
| Apseloff liposome bupivacaine volunteers subcutaneous | 25 | 15 | no page mentions Apseloff |
| liposomal bupivacaine intradermal injection never studied | 25 | 15 | same set |
| 10.1097/DSS.0000000000005031 | 25 | 21 | unrelated (Health History entries, CoQ10, senolytics) — no page cites the DOI |

### 4c. Pages fetched (all via notion-fetch; text saved and searched with Python; no fetch carried truncated /
unknown_block markers — the two "truncated" hits on the Reference and on What is still unsettled are page prose about a
registration number, not fetch truncation)
| page | url | as of | Rames / topic hits |
|---|---|---|---|
| 🚫 Injectables ruled out but not tried | https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5 | 2026-10-02T03:14:22.080Z | see 4a; findings F01, F02 |
| What is still unsettled across these pages… | https://app.notion.com/p/3d410b7903aa819f8300e976a62577db | 2026-09-26T18:23:10.973Z | no liposomal/Exparel/Rames; methoxyflurane entry → F03 |
| 🕳️ What was searched for and does not exist… | https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82 | 2026-09-27T00:27:49.877Z | 0 hits for liposom, Exparel, Rames, Mohs, bupivacaine, sustained-release; no finding |
| 5 — Soft ground in these documents | https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 | 2026-09-26T18:26:13.509Z | read in full; no liposomal or dermatologic-surgery content; no finding |
| 2 — Reference (S1–S457) | https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65 | 2026-10-01T02:05:48.095Z | 1,279,938 chars; 0 hits for liposom, Exparel, Rames, Mohs, Apseloff, Ilfeld, Viscusi, Dagenais, Aggarwal, Kharitonov; S181 = Gitman & Barrington 2018 (Rames ref 9, an incidence review; nothing in Rames contradicts the entry); one nearby passage is an antidote passage — not copied |
| 1 — Product Guide | https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f | 2026-10-02T03:14:29.224Z | 599,993 chars; 0 hits for liposom, Exparel, Rames, Mohs, sustained/extended-release; cardiotoxicity passages are toxicity subjects — not used |
| bupivacaine-wheals (tested by another session) | https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d | 2026-10-02T03:14:18.695Z | liposomal only as Grant 2004, correctly called "never marketed"; no Exparel; no finding |
| Comparing the injectable local anesthetics for intradermal wheals | https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b | 2026-10-02T03:14:02.626Z | Grant 2004 only; its "Ilfeld 2021" is the phantom-limb trial (Pain 2021), not Rames' ref 22; no finding |
| Safe Doses Of Intradermal Analgesics | https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7 | 2026-10-02T03:13:58.754Z | grepped only (no ceilings read into notes): 0 hits for liposom, Exparel, Rames, Mohs, dermatolog, FAERS, Viscusi, Gitman; no finding |
| 💉 Needle Size for Intradermal Injections | https://app.notion.com/p/21f74377f6384dc7a9760ea6709e69c0 | 2026-09-25T07:30:00.218Z | Exparel statements are label/needle/technique content; the two route statements ("the approved routes are infiltration and perineural block, and intradermal injection is not among them"; "the label route does not include intradermal injection in any case") stay true after the 2023 label update and agree with Rames; no finding. The page carries ceilings and injection technique — nothing copied |
| Permanent-Harm Risk Of The Candidates For The Urge To Tense | https://app.notion.com/p/3e510b7903aa812b9b8bfc7e2135a943 | 2026-10-01T03:15:21.643Z | row "Magnesium with local anaesthetic; perineural dexamethasone; liposomal bupivacaine": permanent harms "Liposomal bupivacaine: bupivacaine is the most myotoxic local anaesthetic; systemic toxicity." frequency "No frequency found." Rames gives only a zero-event count for systemic toxicity in 136 dermatologic administrations, not a permanent-harm frequency → no finding. Its source list reads the Exparel label "version of 2025-12-12 — label read: section 5" (noted in F02) |
| Future Medications For Urge To Tense | https://app.notion.com/p/3ce10b7903aa80598dcedb7228a25ef5 | 2026-10-05T05:40:31.473Z | Zadrazil 2024 summary consistent with Rames' account of ref 20; "72 hours" sentence → F04 |
| Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection Routing Analysis | https://app.notion.com/p/39410b7903aa8046b3eef25af516245f | 2026-09-26T18:19:51.310Z | no Exparel/liposomal-bupivacaine text (one "liposomes" hit is about CoQ10); no finding |
| 🔬 The intradermal wheal literature nobody cites… | https://app.notion.com/p/3d410b7903aa8107a042d4e7f6540c1a | 2026-10-02T03:14:04.610Z | holds C043's two sentences ("No sustained-release local anesthetic developed since has come close in human skin."; Sources: "The only human formulation on record that has produced days of skin anesthesia from a single intradermal dose.") — already refuted by the main session (C043); Jensen 2024 added to extra_studies; no separate finding (same sentences as the claim) |
| 💊 Anaesthetics | https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492 | 2026-10-01T03:07:38.200Z | 0 hits for liposom, Exparel, Rames, Mohs, dermatolog; no finding |
| Research (procaine) | https://app.notion.com/p/32a10b7903aa80ba9acdc20255958302 | 2026-09-26T18:24:59.524Z | read in full; procaine mechanism page, no liposomal content; no finding |

### 4d. Verbatim sentences behind the findings (markdown bold markers dropped; words verbatim; no dose figures in them)
- F01 (Injectables › The needle settles it before the evidence does): "The label is also explicit about which routes were
  never studied. Approved: single-dose infiltration and interscalene brachial plexus nerve block. Explicitly not
  recommended because not evaluated: epidural, intrathecal, intravascular, intra-articular, and regional nerve blocks
  other than interscalene."
- F02 (Injectables › Sources › Liposomal and sustained-release › EXPAREL label entry): "Approved: single-dose
  infiltration (age 6 and over) and interscalene brachial plexus nerve block (adults)." … "\"EXPAREL has not been
  evaluated for the following uses and, therefore, is not recommended for these types of analgesia or routes of
  administration\": epidural, intrathecal, regional nerve blocks other than interscalene brachial plexus, intravascular
  or intra-articular use." … "the label read was the 2021 revision plus a secondary prescribing-information mirror, and a
  later revision may exist."
- F03 (What is still unsettled › Which claims rest on one study nobody has repeated): "Days of skin anaesthesia from
  lecithin-coated methoxyflurane microdroplets. Four to eight days of human skin anaesthesia, from a 1991 paper read as
  an abstract only. It is the only human formulation that has ever produced days rather than hours of skin block. It was
  never developed, nothing in the sustained-release class since comes close, and nobody has looked at why it stopped."
- F04 (Future Medications For Urge To Tense › Tier 1 › 1. Magnesium (local injection — optimize, extend, and
  characterize), bullet "Other duration-extension routes worth raising in the same conversation"): "liposomal
  formulations extend local anesthetic effect from 6–8 hours to as much as 72 (Yang et al., Front Pain Res 2026).
  Neither has been used for this indication, but they define the space of “the same relief, lasting longer.”"

### 4e. Observation outside this paper's reach (not a finding: nothing in Rames or its references settles it)
- Injectables page, "The rest of the class": "Nothing in this class is marketed anywhere except Exparel." To my
  knowledge other sustained-release bupivacaine products have been approved in the US since 2020 (a bupivacaine collagen
  implant, a bupivacaine–meloxicam extended-release solution, and a bupivacaine solution in a sucrose-acetate depot
  vehicle). Not checked against a source in this session; flagged for the main session only.

## 5. Results written
- Card: `results_S2/paper_cards/S-686-23.json` (16 key results, 4 author limitations, 19 cited studies; refs 1–4 left
  out on purpose, see §3). Card quotes checked against the text with quotecheck's normalisation (all found).
- Claim updates (1): D048 own-question, confirmed → confirmed, uncertain_after false (route stated as local
  infiltration, subcutaneous plane only; "intradermal" never used).
- Extra studies (2): Apseloff 2013 (23458225) → D048, no change; Jensen 2024 (38482995) → C043: on its own it matches
  the first sentence's elements but not the second sentence's intradermal element; C043's verdict already rests on
  other sources, so no claim update (brief §6: an extra study carries only what it alone supports).
- Notion findings (4): F01, F02 outdated label route list on "Injectables ruled out but not tried" (main text and
  Sources; low); F03 overstated "only human formulation that has ever produced days … of skin block" on "What is still
  unsettled" (medium; rests on Jensen 2024); F04 overstated "as much as 72" hours on "Future Medications For Urge To
  Tense" (low; rests on Ilfeld 2021). F02 and F04 are ambiguous on their natural reading (brief §6), so both are
  low with the reason stated in their notes.
- Considered and not recorded as findings: the D048 sentence itself (right; not marked unverified); the Ilfeld 2021 and
  Zadrazil 2024 summaries on the Injectables page (correct against their abstracts); C043's own sentences on the wheal
  literature page (already a refuted claim; Jensen added as an extra study instead); the "No frequency found" cell for
  liposomal bupivacaine on "Permanent-Harm Risk…" (Rames reports a zero count of systemic toxicity in one setting, not a
  permanent-harm frequency).

## 6. Not reached, and instructions found in documents
- Not reached (paywalled, no abstract, no free copy found): Chang 2022 Mohs letter (36054055), Yadlapati 2021 Mohs
  letter (34791645), Sorenson & Chesnut 2019 review (30148736); Apseloff 2013 full text (no PMC copy); Carroll 2023 and
  El-Boghdadly & Chin 2017 are not in PubMed. Their injection routes could not be read; recorded in D048's reason.
- `convert_article_ids` hit the connector's rate limit twice; not needed (PMC ids are in the metadata records).
- Instructions inside documents: none aimed at me. The Injectables page opens with a dated callout addressed "for the
  health skills" about keeping its dose limits (the person's own ruling) — data; nothing copied. The "Research" page
  ends with a chat-style line ("Please let me know when you are ready to proceed to Part 4…") — leftover text, ignored.
- Content filter: no write was stopped.
