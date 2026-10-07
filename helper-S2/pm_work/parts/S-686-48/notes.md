# S-686-48 — Varghese 2024, EMLA versus amethocaine gel in children (pairwise meta-analysis)

Worker notes. Page numbers are PDF page numbers of the 6-page PDF. Dose and strength figures are written as
[dose figure omitted] throughout.

## 1. Right-paper check

- PDF and text: `papers/S-686-48 - Varghese 2024 - ...pdf`, `texts/S-686-48.txt` (6 PDF pages, journal pages 51-56).
- PDF page 1: title "Eutectic mixture of local anesthetics and amethocaine as topical anesthetics in pediatrics: a
  meta-analysis"; authors Kathryn S. Varghese, Adham Ahmed, Dave M. Mathew, Peter J. Fusco, Mabel N. Abraham (CUNY School
  of Medicine; Feinstein Institutes); "Pediatric Research (2024) 96:51–56; https://doi.org/10.1038/s41390-024-03113-7";
  received 15 Sep 2023, accepted 27 Jan 2024, published online 1 Mar 2024. Matches PMID 38429571 / DOI
  10.1038/s41390-024-03113-7 in common/papers_list.csv. No person_note for this paper. Right paper: yes.
- Text quality: ok. All 6 pages present in reading order and layout view; Table 1 (PDF page 3) and the six forest
  plots (Figs. 1-6, PDF pages 3-5) are in the text. PDF pages 3, 4 and 5 were rendered at 110 dpi and checked by eye:
  every study-level and pooled estimate, CI and I2 in the text matches the figures; Fig. 5 lists "Ormandy, 1998" with
  no estimate (three studies contribute, chi-square df 2). Supplementary material (search strategy, PRISMA flow,
  Newcastle-Ottawa scores, Supplementary Table 4 with the included-study citations, sensitivity analyses) is online
  only and not in the packet; the included trials other than van Kan 1997 are not in the paper's reference list, so
  they were identified in PubMed (section 3).

## 3. PubMed (connector; pm.py blocked). Searches logged in pm_work/searches_log.tsv and pm_work/cache/s_mcp_*.json

Searches (query, count):
- `(amethocaine OR tetracaine OR Ametop) AND (EMLA OR lidocaine-prilocaine OR lignocaine-prilocaine) AND (child OR
  children OR paediatric OR pediatric) AND 1997:1999[dp]` — 14 (all 14 read by title/abstract; none is "Ormandy 1998").
- `Ormandy[Author] AND (amethocaine OR tetracaine OR EMLA OR anaesthesia OR anesthesia OR cannulation)` — 1 (PMID 16700163,
  a haemodialysis practice survey; not the trial).
- `(amethocaine OR tetracaine OR Ametop) AND (EMLA OR prilocaine) AND (cannulation OR venous OR intravenous) AND
  (induction OR "day case" OR "day surgery" OR daycase)` — 1 (PMID 20458453, Soltesz 2010, heated lidocaine-tetracaine
  patch vs EMLA patch, 200 children; not the trial).
- `(amethocaine OR Ametop OR "tetracaine gel") AND (EMLA OR "lidocaine-prilocaine" OR "lignocaine-prilocaine")` — 125
  (all titles of the 1990-2000 records read; abstracts read for 13 unfamiliar ones; no 1998 Scottish day-case trial).
- `Lander J[Author] AND (EMLA OR amethocaine) AND Cochrane` — 3 (16856039 the 2006 review; 24627224 the withdrawal
  notice; 15495086 a circumcision review, irrelevant).

Citation lookups (lookup_article_by_citation, then get_article_metadata to confirm title, population and design):
- Included trials: Arrowsmith 2000 = 10735838 (single-blind, 120 children, venous cannulation); McCafferty 1997 =
  9135307 (double-blind, EMLA vs amethocaine vs placebo on areas of facial port-wine stains, 29 patients, pulsed dye
  laser; MeSH "Adolescent", "Adult", no "Child"; Varghese's Table 1 gives the inclusion criterion "age more than 12 yr");
  Bishai 1999 = 10469814 (randomised blinded crossover, 39 children 5-16 y with cancer, Port-a-Cath puncture); Newbury
  2009 = 19546268 (parallel double-blind RCT, ED; first-attempt success analysed in 679 children, pain observed in 65;
  Varghese's Table 1 lists 32 + 33 = 65); Arendts 2008 = 18292082 (double-blind RCT, 177 analysed of 203, 12 months-12 y,
  ED); Choy 1999 = 10519337 (single-blind RCT, 34 children 1-14 y, venepuncture); Romsing 1999 = 10472236 (double-blind
  RCT, 60 children 3-15 y, three groups of 20); van Kan 1997 = 9043560 (open randomised trial, 66 inpatients 1-15 y,
  venipuncture; the one included trial whose abstract reports EMLA as more efficacious; it appears in none of Figs. 1-6);
  Lawson 1995 = 7547043 (open study of amethocaine in 148 children, then single-blind comparison with EMLA in 94
  patients with the same application time for both, shorter than EMLA's labelled minimum; Varghese lists 55 + 55);
  "Ormandy 1998" (Scotland, day-case surgical unit, 103 + 109, listed as a comparative study) = not found in PubMed by
  author or by topic; identity not checkable without Supplementary Table 4.
- Reviews discussed: Pywell 2015 = 25351196 (3 RCTs; RR 1.046, CI 0.975 to 1.122, p=0.211; Varghese calls it "a 2017
  meta-analysis"); Taddio 2002 = 11918521 (8 studies; equal when used as labelled, tetracaine better at equal
  application times; Varghese says "in 2001").
- Not cited by Varghese: Lander 2006 Cochrane = 16856039 (6 RCTs, 534 children; amethocaine reduced the risk of pain,
  RR 0.78, 95% CI 0.62 to 0.98); withdrawal notice = 24627224 ("At 23 May 2013 ... withdrew this review as the authors
  were no longer available to complete the update").
- Background references (PMID by citation match; titles confirmed where marked *): Fein 2012 = 23109683; Hallen 1982 =
  7125278; Hallen 1984 = 6496911; Maunuksela 1986 = 3535860; Cooper 1987 = 3328685; Manner 1987 = 3434165*; Robieux 1991
  = 2040936*; Lander 1996 = 8867250; Soliman 1988 = 3285736; Gajraj 1994 = 7818623; Sawyer 2009 = 19151049* (adult
  volunteers); Browne 1999 = 10566919* (adult volunteers); O'Connor 1995 = 7640129 (adults); Molodecka 1994 = 8110569;
  Small 1988 = 3052676 (split skin grafts); Woolfson 1990 = 2206789; Doyle 1993 = 8285323; Bjerring 1989 = 2532919*
  (EMLA biphasic vascular response, healthy adults); Mace 2020 = 33181789*; Hsu (UpToDate) no PMID.
- Cached abstracts (pm_work/cache/a_<pmid>.json): 38429571, 25351196, 16856039, 24627224, 11918521, 9135307, 18292082,
  19546268, 7547043, 9043560 (redacted: one serum metabolite concentration range replaced by [dose figure omitted]).

## 2. The paper in the terms the claims need (own question)

- 10 studies in Table 1 (8 labelled RCT, Lawson 1995 and "Ormandy 1998" labelled comparative study). Text: "A total of
  892 pediatric patients were pooled, of whom 448 underwent topical anesthesia with EMLA cream and 473 underwent topical
  anesthesia with amethocaine gel" (p2) — the arms sum to 921 (= Table 1 totals); "over 890" in the discussion (p4).
- Pooled results as printed (EMLA vs amethocaine; studies per outcome from Figs. 1-6):
  first-attempt cannulation success RR 0.98 (0.97-0.99), p 0.017, I2 0%, 3 studies (Arendts, Newbury, Ormandy);
  child-reported absence of pain RR 0.58 (0.41-0.82), p 0.011, I2 20.2%, 5 (Arrowsmith, Lawson, McCafferty, Ormandy, Romsing);
  child-reported VAS SMD 0.43 (-1.46 to 2.31), p 0.525, I2 92.8%, 4 (Bishai, Choy, McCafferty, Newbury);
  parent-reported VAS SMD -0.05 (-0.64 to 0.54), p 0.478, I2 0%, 2 (Bishai, Choy);
  observed pain score SMD -0.45 (-2.27 to 1.38), p 0.405, I2 88.6%, 3 contributing (Choy, Lawson, Romsing; Ormandy listed, no estimate);
  child-reported acceptable anaesthesia RR 0.73 (0.34-1.55), p 0.118, I2 0%, 2 (Lawson, McCafferty).
- van Kan 1997 (Table 1, ref 15) contributes to none of the six forest plots.
- Worker's recomputation (scratchpad hk_check.py, from the plotted study estimates and CIs): random-effects with the
  Hartung-Knapp adjustment reproduces all six printed intervals and p values (Fig. 1: 0.98 [0.97; 0.99] p 0.017; Fig. 6:
  0.73 [0.34; 1.59] p 0.12; Fig. 2: 0.58 [0.41; 0.81] p 0.011; Figs. 3-5 likewise). Ordinary DerSimonian-Laird pooling of
  the same estimates: Fig. 1 RR 0.98 [0.89; 1.09] p 0.72 (none of the three trials significant alone); Fig. 6 RR 0.73
  [0.61; 0.87] (both trials favour amethocaine alone); Fig. 2 RR 0.58 [0.46; 0.73]. So the "significant" first-attempt
  result and the "no difference" acceptable-anaesthesia result depend on the pooling method; the absence-of-pain result
  does not.
- Newbury 2009 in Fig. 1: plotted 0.99 [0.75; 1.31] is what about 32 children per arm give (e.g. 24/32 vs 25/33); the
  trial analysed first-attempt success in 679 children (75.8% vs 73.9%).
- Quality: Newcastle-Ottawa Scale (observational-study tool) only, all ">seven asterisks ... good quality"; no Cochrane
  risk-of-bias assessment of the RCTs, no GRADE/certainty rating. Discussion says the analysis "was limited to
  observational studies", contradicting Table 1. Calls itself "the first and most comprehensive review on the topic"
  without citing Lander 2006 (Cochrane, 6 RCTs, 534 children); cites Taddio 2002 (8 studies) and Pywell 2015 (3 RCTs).
- Citation slips inside the paper: Pywell is "a 2017 meta-analysis" in the text but Emerg Med J 2015 in ref 26; Taddio
  "in 2001" in the text, Ann Pharmacother 2002 in ref 27; methods "risk ratios (OR)".
- Population check: McCafferty 1997 (laser, port-wine stain; Table 1 inclusion "age more than 12 yr"; PubMed MeSH
  Adolescent + Adult, no Child) is the one included study outside paediatric needle procedures; it feeds Figs. 2, 3, 6.
  No included study is in non-procedural pain.

## 4. Notion (read-only: notion-search and notion-fetch only)

Searches (query -> number of results; results treated as candidates only):
- "Varghese 2024 EMLA amethocaine meta-analysis" (page_size 25) -> 15: Injectables ruled out but not tried; Product Guide;
  Prilocaine + Lidocaine; EMLA anaesthetic disc (US, discontinued); Reference; EMLA cream/patch product rows (UK, Germany,
  Spain); Anestecin rows (Colombia); Health Pages - Meta.
- "38429571" (25) -> 25, none relevant by title (Product Guide, Dysport rows, unrelated journal pages).
- "s41390-024-03113-7" (25) -> 21, none relevant (DOI-fragment noise).
- "amethocaine Ametop tetracaine gel EMLA children cannulation" (40) -> 15: Reference; Prilocaine + Lidocaine; LloydsPharmacy
  seller page; Ametop Gel 4% LloydsPharmacy product row; EMLA crema Aspen Mexico rows (La Comer, Farmalisto, Farmacias del
  Ahorro, Paris, Klyns, Guadalajara: highlight mentions "paediatric tetracaine evidence"); Product Guide; Medino; Well
  Pharmacy; emc; EMLA LloydsPharmacy row.
- "Lander Cochrane review withdrawn EMLA amethocaine needle" (25) -> 15: Prilocaine + Lidocaine; Reference; Product Guide;
  EMLA parches Mexico rows; Emulus rows (Germany); Anestecin rows; Injectables ruled out; EMLA disc.

Pages fetched:
- Prilocaine + Lidocaine, https://app.notion.com/p/33110b7903aa8024a793d7249262b267, as of 2026-10-02T03:14:00.887Z;
  100,421 chars (saved tool-result file); no truncated / unknown_block flags. Varghese, Pywell, Zhao, Stavleu, Taddio:
  0 hits. Lander / Cochrane: the [S-S] source entry (Sources section, just above "### Calculations withdrawn and remaining
  limits"). Verbatim sentences relied on:
  - "The withdrawal is administrative rather than a finding of error, and the 2006 analysis stands as published, but it
    is no longer a current Cochrane review and nothing has replaced it." (= D068)
  - "**[S-S] Lander JA, Weltman BJ, So SS.** EMLA and amethocaine for reduction of children's pain associated with needle
    insertion. ... — six trials, **534 children aged three months to 15 years**: amethocaine significantly reduced the
    risk of pain against this cream on the combined pain metric, **RR 0.78 (95% CI 0.62–0.98)**; on child self-report
    **RR 0.63 (0.45–0.87)**; for intravenous cannulation specifically **RR 0.70 (0.55–0.88)**." (matches the cached
    Lander abstract; withdrawal date 23 May 2013 and PMID 24627224 match the notice) — correct, no finding.
  - "Paediatric needle-procedure comparisons with tetracaine do not settle adult neuropathic-pain treatment." — accurate.
  - The depth/duration section cites Bjerring 1990 [S-J] and Evers [S-H]; Varghese's own duration statements come from
    UpToDate (secondary), so they are not used against it.
  - The page also carries dose-ceiling and methaemoglobin-threshold passages ([S-...] Guay entry and label entries):
    not read further, not copied (filter rule).
- 2 — Reference — Topical Treatments for Small Fiber Neuropathy, https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65,
  as of 2026-10-01T02:05:48.095Z; 1,279,938 chars (saved tool-result file, searched with Python); no truncated /
  unknown_block flags (the two "truncated" string hits are page prose). Counts: EMLA 42, amethocaine 13, tetracaine 22,
  Lander 1, Cochrane 80, Zhao 3, Varghese 0, Pywell 0, Taddio 0, Stavleu 0, cannulat 6. Every amethocaine / Lander /
  cannulation hit read in context (§4.4 Tetracaine; S182 register entry; §4.2.4 products; §4.1.8 Telica lines;
  dose-ceiling passages in §2.7, §4.1.7, §4.2.3, §4.3, §9.7 and S183 skipped under the filter rule, not copied).
  Verbatim sentences relied on (§4.4 Tetracaine):
  - "What it costs the claim is currency, not validity: the estimates are frozen at a 2006 search, **Cochrane no longer
    stands behind them as up to date**, and nothing has replaced the review on that exact head-to-head \[S182\]."
  - "**The comparison is carried instead by an independent replication that is current**: a network meta-analysis of
    **40 randomised trials in 4,481 children** ranked amethocaine first of nine methods with a probability of **57.6%**
    \[S182\]."
  - "**That reopens a prilocaine-free option this reference closes elsewhere.** The pre-capsaicin anaesthetic in §4.2.4
    is the one place a prilocaine-containing product is accepted for want of an alternative, and amethocaine 4% is an
    alternative that beat that product in a Cochrane review whose analysis stands and whose currency does not, and again
    in a 2025 network meta-analysis that is current."
  - S182 register entry: Lander 2006 figures and withdrawal details match the cached abstracts; it says "any trial after
    the 2006 search is outside it" (accurate) and does not repeat "nothing has replaced".
  - §4.2.4: "**The one exception.** A topical anaesthetic is used before capsaicin 8% patch application, and EMLA is the
    one Mexican pharmacies stock. **Pliaglis** — see §4.4 — carries a higher anaesthetic load without prilocaine and is
    the better pre-treatment where a pharmacy will order it." (rests on load and prilocaine-free reasoning about a
    different product; Varghese does not test Pliaglis — no finding.)
- 1 — Product Guide — Topical Treatments for Small Fiber Neuropathy, https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f,
  as of 2026-10-02T03:14:29.224Z; 599,993 chars (saved file); no truncated / unknown_block flags. Counts: EMLA 35,
  amethocaine 4, tetracaine 20, Pliaglis 9, Lander 0, Varghese 0, Pywell 0, Zhao 0, cannulat 0. Read in context (masked
  reader, own helper nf_s48.py; note: another worker overwrote the shared scratchpad nf.py at 23:47 with a benign masked
  version, so this worker switched to uniquely named helpers). Verbatim sentences relied on:
  - "## Ranks 19 to 23 · On the list, and not to buy" > "### 19 · EMLA cream ...": "Ask the clinic what it uses and
    whether it cools, buy nothing before that answer, and where it wants a cream, ask about **amethocaine [dose figure
    omitted]**, which is prilocaine-free and beat this one in a Cochrane review — a review Cochrane **withdrew on 23 May
    2013** because its authors could not complete an update, alleging no error in it, and whose result a current network
    meta-analysis of **40 trials in 4,481 children** reproduces."
  - "### Tetracaine": "**That Cochrane review was withdrawn on 23 May 2013**, because its authors were no longer available
    to complete an update; the notice alleges no error, so the analysis stands and only its currency does not, and the
    network meta-analysis is the current replication of the same comparison. **That reopens the pre-Qutenza question**:
    amethocaine [dose figure omitted] is a prilocaine-free alternative that beat the lidocaine-prilocaine cream in a
    Cochrane review that is withdrawn but unretracted, and again in a network meta-analysis that is current."
  - Pliaglis and Telica entries: product and load statements, no EMLA-vs-amethocaine evidence claim — no finding.
- Pain biology, ion channels, and topical anesthetics for small fiber neuropathy, https://app.notion.com/p/34210b7903aa8002aad4eba9787cb947,
  as of 2026-09-26T18:29:03.713Z; 170,980 chars; no truncated / unknown_block flags. EMLA 0, amethocaine 0, Lander 0,
  child 0, cannulat 0. Relevant only: "**5.2.5 Duration and clearance from the tissue**<br>Topical lidocaine provides
  \~35–45 minutes of skin numbing in the procedural setting — the figure behind pre-needle creams." and 8.2.1 "For
  lidocaine, topical effect lasts \~35–45 minutes."; Part 13 open item 6 = claim E028. Varghese's duration statements
  are secondary (UpToDate), for EMLA and amethocaine rather than plain lidocaine, and E028's reason already holds
  primary figures, so no Notion finding; an other-claim entry for E028 records the screen (verdict unchanged).
- 5 — Soft ground in these documents, https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403, as of
  2026-09-26T18:26:13.509Z; full text in the tool result; no flags. Nothing on EMLA, amethocaine, Lander or children.
  Its rule "A pooled effect estimate printed beside a participant total is unreliable in this literature" applied to this
  worker's own wording: every Varghese estimate below names its own number of studies, not the 892 total.
- What is still unsettled across these pages, and what would settle each one, https://app.notion.com/p/3d410b7903aa819f8300e976a62577db,
  as of 2026-09-26T18:23:10.973Z; 61,415 chars; no flags (the "truncat" hits are prose about registro suffixes). EMLA 6
  (registro suffix and AEMPS area notice — dose subject, not used), amethocaine 1 (intradermal slopes, Willatts and
  Reynolds 1985), Lander 0, Cochrane 0, cannulation 0. No open question on topical EMLA versus amethocaine. No finding.
- What was searched for and does not exist, https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82, as of
  2026-09-27T00:27:49.877Z; 64,683 chars; no flags; EMLA / amethocaine / tetracaine / Lander / Cochrane / children /
  cannulation all 0. No finding.
- Looking For Pain Numbing Creams In Mexico, the US, Colombia, & Europe (hub), https://app.notion.com/p/3d210b7903aa80e8a502ffa1e92e930e,
  as of 2026-09-26T18:19:45.689Z; full text read; no literature statement on EMLA versus amethocaine ("Procedural creams
  such as EMLA, LMX4, Ametop and Pliaglis have formulation-specific area, time and dressing instructions"). No finding.
- Duplicate or Superceded - DELETE ME — 3 — Product Guide, Plain English, https://app.notion.com/p/3d410b7903aa81ac9233cb71f5e5b038,
  as of 2026-10-01T03:54:25.660Z; 1,051,542 chars; no flags. Repeats the Product Guide's amethocaine sentences ("The
  network meta-analysis is the current replication of the same comparison." / "**That reopens the pre-Qutenza
  question**: amethocaine ... beat the lidocaine-prilocaine cream in a Cochrane review that is withdrawn but unretracted,
  and again in a network meta-analysis that is current." / "**Do raise amethocaine [dose figure omitted] with the clinic
  if you go for a capsaicin patch**, because for that one job it is the best-supported option and it avoids prilocaine
  entirely."). Page is marked for deletion: mentioned in the Product Guide findings' notes, no separate finding.
- Ametop Gel 4 % ... LloydsPharmacy (United Kingdom), https://app.notion.com/p/3e210b7903aa812e855bfbac7a98f70e, as of
  2026-09-24T21:43:54.911Z: "Its established role is procedural skin anaesthesia; paediatric venepuncture findings do not
  establish repeated treatment of neuropathic symptoms." and "Paediatric needle-procedure evidence does not establish
  routine neuropathic treatment or automatic suitability before a capsaicin procedure." — accurate; no finding.
- EMLA crema (Aspen México) ... La Comer via Rappi (Mexico), https://app.notion.com/p/3e010b7903aa816396ade36fc70f4741, as
  of 2026-09-24T21:42:20.148Z: "the prior contradictory cooling comparisons and paediatric tetracaine evidence do not prove
  general EMLA treatment failure" — accurate; the other EMLA Mexico rows carry the same template text (seen in search
  highlights). No finding.
- Pliaglis (Andrómaco) ... (Mexico), https://app.notion.com/p/3e010b7903aa8149836bfd379ce36a84, as of
  2026-09-21T12:39:06.670Z: "Absence of prilocaine does not prove superiority over EMLA" — accurate; no finding.
- Injectables ruled out but not tried, https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5, as of
  2026-10-02T03:14:22.080Z; 72,962 chars; no flags; EMLA 0, topical amethocaine statements 0 (amethocaine there is
  intradermal; claims D045-D052). No finding.
- Further searches: "amethocaine before Qutenza capsaicin patch prilocaine-free alternative" (25) -> 14 (Product Guide,
  Reference, Prilocaine + Lidocaine, Pliaglis Mexico, Qutenza rows, pain-clinic list); "network meta-analysis 4,481
  children local analgesia venipuncture Zhao" (25) -> 15 (wheal pages, Relief page, Meta rows on wheals; no new page on
  this comparison).

## 2b. Claim screen (all 320 claims in common/claims_all.json, masked viewer pm_work/tools/claims_view.py)

Regexes run (grep over claim, elements, reason, proposed wording, review, evidence quote), with hit counts:
- `EMLA|prilocaine|tetracaine|amethocaine|ametop` — 26; `Lander|Cochrane|Pywell|Zhao|Stavleu|Taddio|Varghese|38429571` — 7;
  `\bchild|children|p(a)?ediatric|infant|neonat|adolescen` — 4; `cannulat|venepunct|venipunct|needle[- ]procedure|needle
  insertion|IV insertion|catheter insertion|port-a-cath|laser` — 9; `topical|cream|\bgel\b|numbing` — 45;
  `onset|depth of|how deep|penetrat|duration of (anaesthesia|anesthesia|action|numbness)|application time|occlus` — 26;
  `Synera|Rapydan|Pliaglis|LMX|liposomal lidocaine|S-Caine|Zingo|Ametop|Maxilene|Topicaine|benzocaine` — 2;
  `blanch|erythema|vasodilat|biphasic` — 5; `meta-analys|systematic review|pooled|no review|nothing has replaced|superseded|withdrawn` — 19;
  all E-claims listed (45); author names of every included trial and cited study — 0; PMIDs of the included trials,
  reviews and key references — only D068 (its records hold Pywell 25351196, Zhao 40055583, Stavleu 39933876).
Read closely and kept:
- D068 (own question) — refuted kept; extra-study Pywell 2015 also refuted (standing verdict kept).
- E028 (Pain biology, "35-45 minute figure") — Varghese states procedural durations (secondary); no 35-45 minute figure;
  confirmed kept (other-claim entry).
Read closely and dropped (the paper does not bear on them):
- D066, D067 (Prilocaine + Lidocaine; EMLA in neuropathic pain) — Varghese is procedural pain in children only.
- C037, D045, D046, D049 (intradermal tetracaine/amethocaine timing and weal) — Varghese is topical, not intradermal.
- E019, E023 (topical combinations / lidocaine with capsaicin) and the other E-claims (SFN, eugenol, menthol, capsaicin,
  ion channels) — no overlap in drug, population or outcome.
- C015, C016, C018, C019 (blanching / vascular supersensitivity with intradermal adjuvants) — Varghese mentions EMLA's
  biphasic vascular response only as background (Bjerring 1989), not for wheals.
- A065, A070, A071, C010, C022, C057, D032 and other "only meta-analysis" claims — different interventions.
Not tested under the filter rule (dose or toxicity subject; text not written out):
- prilocaine-wheals: 4 claims not tested: dose or toxicity subject (surfaced by the prilocaine regex).
- Safe Doses Of Intradermal Analgesics: 1 claim not tested: dose or toxicity subject (surfaced by the topical regex).
(None of them bears on Varghese, which mentions methaemoglobinaemia only qualitatively.)

## 5. Not reached, and instructions found inside documents

- Not reached: Varghese's online supplement (search strategy, PRISMA flow, Newcastle-Ottawa scores, Supplementary Table 4
  with the included-study citations, leave-one-out plots) — so "Ormandy 1998" stays unidentified (not in PubMed by author
  or topic). The included trials were checked by PubMed abstract only, not full text. No paywall, login or bot check was
  attempted.
- Instructions inside documents: none aimed at this worker in the paper, the abstracts or the Notion pages (the Notion
  pages' advice sentences are addressed to their reader and were treated as data). The PubMed connector appends a
  boilerplate "important legal notice" asking users to attribute PubMed and link DOIs; treated as tool boilerplate (the
  outputs cite PMIDs and DOIs in any case).
- Shared scratchpad: another worker overwrote the scratchpad helper nf.py at 23:47 UTC with its own benign, masking
  version; this worker switched to uniquely named helpers (nf_s48.py, sent_s48.py, hk_check.py). No effect on results.
- Content filter: no write was stopped.

## 6. Results written

- Card: results_S2/paper_cards/S-686-48.json (16 key-result quotes, 10 author-limitation quotes, 32 cited studies).
- Claim updates (3): D068 own-question refuted -> refuted (uncertain_after false); D068 extra-study Pywell 2015
  (PMID 25351196) refuted -> refuted; E028 other-claim confirmed -> confirmed.
- Extra studies (2): Pywell 2015 (25351196); Cochrane withdrawal notice (24627224).
- Notion findings (5): F01 Prilocaine + Lidocaine [S-S] outdated low; F02 Reference §4.4 outdated medium; F03 Reference
  §4.4 ranking-reweigh medium; F04 Product Guide Tetracaine ranking-reweigh medium; F05 Product Guide rank 19 EMLA
  ranking-reweigh medium.
