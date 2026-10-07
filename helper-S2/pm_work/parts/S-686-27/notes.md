# S-686-27 Schmittner 2010 — working notes

## 1. Right-paper check

- Text file: texts/S-686-27.txt, 6 PDF pages, each in reading order and layout view; readable, no OCR needed.
- PDF page 1 header: "JEADV", "DOI: 10.1111/j.1468-3083.2010.03653.x", "ORIGINAL ARTICLE", title "Influence of high dose
  tumescent local anaesthesia with prilocaine on systemic interleukin (IL)-6, IL-8 and tumour necrosis factor-a";
  authors MD Schmittner, J Faulhaber, B Kemler, W Koenen, JO Thumfart, C Weiss, M Neumaier, GC Beck (Mannheim);
  footer "JEADV 2010, 24, 1400–1405". Matches papers_list.csv (PMID 20384691, DOI 10.1111/j.1468-3083.2010.03653.x).
- Right paper: yes. Text quality: ok (Greek letters extracted as Latin: "a" for alpha, "lg" for microgram; table 2 is
  readable in the layout view). Figures 1–3 are graphs of serum prilocaine, methaemoglobin and IL-6 over time; their
  values are also in Table 2 and the Results text, so no rendering was needed.
- Received 15 October 2009; accepted 15 February 2010. Conflict of interest: "None declared." No funding statement found.
- Registration: ISRCTN 19821978 (listed in the Methods although the study is observational).

## 2. What the paper is (for the own question)

- Prospective, single-centre, observational study; 30 adult in-house dermatological surgery patients (melanoma 20,
  acne inversa 8, other malignant skin tumours 2), tumescent local anaesthesia (subcutaneous infusion of a dilute
  prilocaine-with-epinephrine solution via a pump) for large resections, Jan–Sep 2008, Mannheim.
- Primary aim (Abstract, Introduction): effect of prilocaine-induced methaemoglobin on systemic IL-6, IL-8 and TNF-alpha
  up to 72 h. Methaemoglobin, serum prilocaine, CRP, LDH, CK, PCT measured serially (basal, 1, 2, 4, 12, 24, 48, 72 h);
  plus an in-vitro cycloheximide whole-blood experiment.
- So it is a cytokine / systemic-inflammation study in which methaemoglobin is the hypothesised mediator and is measured
  serially — not a methaemoglobin dose-finding study, and not intradermal ("infiltration of skin" on the page; the
  paper's route is subcutaneous tumescent infusion).
- Results by direction only: methaemoglobin rose from baseline, peaked at 12 h and fell back by 24–48 h; three
  patients had markedly raised values, one with mild transient symptoms (cyanosis, hyperventilation) treated with
  oxygen and mild sedation; IL-6 rose (peak 12 h) and returned to baseline by 72 h; CRP rose (peak 48 h); IL-8, TNF-alpha,
  CK, LDH, PCT did not change significantly; no correlation between methaemoglobin and IL-6 at any time; no correlation
  between applied dose and methaemoglobin or serum prilocaine.

## 3. Guay citations inside Schmittner (reference 8)

Reference 8 (PDF page 6): "Guay J. Methemoglobinemia related to local anesthetics: a summary of 242 episodes. Anesth
Analg 2009; 108: 837–845." Cited five times:
1. PDF p1, Introduction: "Although an upper limit of [dose figure omitted] prilocaine was recently recommended, some
   authors reported the use of up to [dose figure omitted].8–10" (refs 8–10 = Guay, Lindenblatt, Mang).
2. PDF p1, Introduction: "This effect may also be potentiated by other oxidative drugs.8"
3. PDF p5, Discussion: "Current publications recommend a dose limitation of [dose figure omitted].8" followed by the
   comparison with Lindenblatt, Rudlof, Sagoo and Mang (refs 3, 9, 10, 25).
4. PDF p5, Discussion: "Patients can be symptomatic from methemoglobinaemia and require treatment with values as low
   as [figure omitted].8,26 This value was exceeded in our study ..." (refs 8 and 26 = Guay, Ash-Bernal).
5. PDF p5, Discussion, closing sentence: "As a result of possible and unpredictable high MHb concentrations, TLA can
   only be recommended with prilocaine in doses of [dose figure omitted].8"
- The figure in the closing recommendation is the same figure that sentence 3 attributes to "Current publications"
  with reference 8 (Guay), and the same figure the Introduction calls "recently recommended" (refs 8–10). The paper
  never states a figure of its own different from the one it attributes to Guay. Its recommendation is framed as
  agreeing with Guay; the contrast drawn is with the larger amounts other authors used (Lindenblatt, Mang, Sagoo,
  Rudlof) and with the amounts used in the study itself.
- The abstract's conclusion repeats the same recommendation without a reference number.

## 4. PubMed lookups (connector; pm.py blocked)

lookup_article_by_citation on Schmittner's reference list (two batches, 2026-10-07):
- ref 1 Klein 1987 Am J Cosmetic Surg: NOT FOUND (journal not indexed)
- ref 2 Bussen 2003 Chirurg 74:839: 14504797
- ref 3 Rudlof 2007 Anaesthesist 56:785: 17370052
- ref 4 Abramson 1998 Aesthetic Plast Surg 22:404: 9852171
- ref 5 Rao 1999 N Engl J Med 340:1471: 10320385
- ref 6 Khan 1999 Am J Med Sci 318:415: 10616167
- ref 7 Dumont 1995 Acta Anaesthesiol Belg 46:39: 7618428
- ref 8 Guay 2009 Anesth Analg 108:837: 19224791
- ref 9 Lindenblatt 2004 Aesthetic Plast Surg 28:435: 15870963
- ref 10 Mang 1999 Z Hautkr 74:157: NOT FOUND by citation lookup (searched separately below)
- ref 11 Vasters 2006 Eur J Anaesthesiol 23:760: 16723054
- ref 12 Sadove 1965 Acta Anaesthesiol Scand Suppl 16:175: 5322419
- ref 13 Mansouri 1993 Am J Hematol 42:7: 8416301
- ref 14 Margulies 2002 J Trauma 52:796: 11956408
- ref 15 Jaffe 1981 Prog Clin Biol Res 51:133: 7022466
- ref 16 Umbreit 2007 Am J Hematol 82:134: 16986127
- ref 17 Hack 2001 Crit Care Med 29:S21: 11445730
- ref 18 Spolarics 1998 J Leukoc Biol 63:534: 9581796
- ref 19 Liu 2003 Am J Physiol Cell Physiol 285:C1036: 12839837
- ref 20 Chernik 1990 J Clin Psychopharmacol 10:244: 2286697
- ref 21 Pfaefflin 2009 Anal Bioanal Chem 393:1473: 19104782
- ref 22 Gabay 1999 N Engl J Med 340:448: 9971870
- ref 23 Il'yasova 2008 Biomarkers 13:41: 17852073
- ref 24 Vos 2009 Transplant Proc 41:595: 19328934
- ref 25 Sagoo 2000 Phlebologie 29:154: NOT FOUND (journal not indexed for that year)
- ref 26 Ash-Bernal 2004 Medicine (Baltimore) 83:265: 15342970
- ref 27 Grazer 2000 Plast Reconstr Surg 105:436: 10627013
- ref 28 Kortgen 2003 Anaesthesist 52:1020: 14992088
(The connector's output swaps the labels "pmid" and "key"; PMIDs above are the numeric values.)

## 5. Notion (read-only: notion-search and notion-fetch only)

### 5.1 prilocaine-wheals — https://app.notion.com/p/3c510b7903aa8159a5d9e4447ec15409
Fetched 2026-10-07 (this session); "as of 2026-10-02T03:14:12.541Z" (same version the claims were tested on); path
Health / Health Pages; 76,671 characters; no truncated / unknown_block markers in the result. Searched the text for:
Guay (12 hits), Schmittner (2), Lindenblatt (2), Sertdemir (2), Yalcin/Yalçın (0), tumesc (4), interleukin/IL-6/cytokin/
inflammat (2), contrasting (9), Scite (8), 20384691 (0), the DOI suffix 03653 (1).
Verbatim sentences relied on (dose figures replaced by a generic pattern, nothing else changed):
- [How much prilocaine is too much? (opening)] "There are several figures in circulation, they disagree, and the disagreement runs in the safe direction: the better-sourced the number, the lower it is."
- [How much prilocaine is too much? (Guay paragraph, last sentence)] "In children over six months the figure is [dose figure omitted], and Guay's closing recommendation is to hold to [dose figure omitted] generally."
- [How much prilocaine is too much? (Schmittner paragraph)] "The stricter figure: [dose figure omitted]. The one published analysis that contradicts Guay contradicts it downwards. Schmittner and colleagues (2010) measured methemoglobin after high-dose prilocaine infiltration of skin and concluded that because the concentrations reached are unpredictable, prilocaine infiltration should be limited to [dose figure omitted]."
- [Who is at extra risk (Vasters)] "Vasters and colleagues (2005) gave [dose figure omitted] of prilocaine to 162 patients for nerve blocks before knee surgery and measured methemoglobin three hours later."
- [Who is at extra risk (Lindenblatt)] "A second measurement bears more directly on injecting into skin. Lindenblatt and colleagues (2004) infiltrated skin and the fat beneath it with dilute prilocaine for liposuction at an average of [dose figure omitted] — above Guay's adult ceiling — and found the plasma concentration peaking at three hours, mean methemoglobin of [dose figure omitted], a single highest reading of [dose figure omitted], and no clinical signs in anyone."
- [Sources › Systemic toxicity and methemoglobin (Guay entry, Scite note)] "Limits: a compilation of published case reports, so it establishes the doses at which events have been reported, not the rate at which they occur. Scite: 275 Smart Citations, 3 supporting, 3 contrasting, no editorial notices."
- [Sources › Systemic toxicity and methemoglobin (Schmittner entry)] "Schmittner MD and colleagues. Influence of high dose tumescent local anaesthesia with prilocaine on systemic interleukin (IL)-6, IL-8 and tumour necrosis factor-α. *Journal of the European Academy of Dermatology and Venereology* 2010;24(12):1400–5. DOI 10.1111/j.1468-3083.2010.03653.x. — The recommendation to limit prilocaine infiltration to [dose figure omitted] because the methemoglobin concentrations reached are unpredictable. This is the only paper that cites Guay contrastingly, and it argues for a lower ceiling, not a higher one. Limits: the primary outcome was cytokine levels, not methemoglobin, and the sample is small."
- [Sources › Systemic toxicity and methemoglobin (Vasters entry, citation)] "Vasters FG, Eberhart LH, Koch T and colleagues. Risk factors for prilocaine-induced methaemoglobinaemia following peripheral regional anaesthesia. *European Journal of Anaesthesiology* 2006;23(9):760–5."

### 5.2 Safe Doses Of Intradermal Analgesics — https://app.notion.com/p/3c610b7903aa80b9be8cfcefc13161f7
Fetched 2026-10-07; "as of 2026-10-02T03:13:58.754Z" (same version as tested); path Health / Health Pages; 65,027
characters; no truncated / unknown_block markers. Text searched for Guay (1 hit, Sources), Schmittner (1, Sources),
Lindenblatt (0), Sertdemir (0), Yalcin (0), tumesc (2), IL-6/cytokin (2), contrasting (1), Scite (0), "242" (4).
Ceilings: counted, never copied — the section "Why the prilocaine ceiling is methaemoglobinaemia and not milligrams"
holds about 40 number-with-unit dose figures, the Sources › Methaemoglobinaemia subsection about 11, the whole page
about 700 number-with-unit matches (regex count). None is reproduced anywhere in these results.
The body section also carries reader caveats ("The numerical recommendations above require separate source review and
must not be used to calculate a larger topical dose. This correction does not endorse the page's proposed
injection-session amounts.") — addressed to readers, not to this agent; recorded only as page content.
Verbatim sentences relied on (dose figures replaced):
- [Why the prilocaine ceiling is methaemoglobinaemia and not milligrams] "A stricter line than [dose figure omitted] has been published, and it comes from a different body of work. The study of high-dose tumescent prilocaine infiltration of skin recommends holding to [dose figure omitted] — [dose figure omitted] at 70 kg — because the methaemoglobin concentrations reached are unpredictable, and the 242-episode summary reaches the same [dose figure omitted] as its own closing general recommendation, having set [dose figure omitted] for children over six months."
- [same section, next sentence (start only)] "Two bodies, two numbers, and the lower one is [rest of sentence omitted: dose figures and planning advice]"
- [Sources › Methaemoglobinaemia (Guay entry, last sentence)] "Its own closing general recommendation is the stricter [dose figure omitted], the figure it sets for children over six months."
- [Sources › Methaemoglobinaemia (Schmittner entry)] "Schmittner MD, et al. Influence of high dose tumescent local anaesthesia with prilocaine on systemic interleukin (IL)-6, IL-8 and tumour necrosis factor-α. *J Eur Acad Dermatol Venereol* 2010;24(12):1400–1405. doi:10.1111/j.1468-3083.2010.03653.x. — The stricter infiltration ceiling: limit prilocaine infiltration to [dose figure omitted], on the ground that the methaemoglobin concentrations reached are unpredictable. Limits: the primary outcome was cytokine levels, not methaemoglobin, and the sample is small; it is the only paper that cites the 242-episode summary contrastingly, and it argues for a lower ceiling, not a higher one."
Citation details on both pages match the paper (JEADV 2010;24(12):1400–1405, DOI 10.1111/j.1468-3083.2010.03653.x).

### 5.3 Scite (not reachable)
- Tried the Scite connector (search_literature on Guay's DOI 10.1213/ane.0b013e318187c4b1) to see how Scite classifies
  Schmittner's citations of Guay and which papers it lists as contrasting. Refused: "MCP tools require a paid scite plan
  or an active free trial". Not pursued further (no purchases or trials under the rules). So the page's Scite figures
  (Guay: "3 supporting, 3 contrasting") and "the only paper that cites Guay contrastingly" could not be checked against
  Scite itself. Note: Scite tallies citation statements, not papers, and Schmittner cites Guay in five separate
  sentences, so three contrasting statements could in principle all come from one paper — this cannot be settled here.

### 5.4 Notion searches (notion-search; candidates only, every relevant page then fetched and searched as text)
| query | results | pages relevant to this paper |
|---|---|---|
| Schmittner (page_size 50) | 23 | Safe Doses Of Intradermal Analgesics; prilocaine-wheals (rest unrelated: name-like matches) |
| Guay methemoglobinemia 242 episodes (50) | 27 | prilocaine-wheals; Safe Doses; Prilocaine + Lidocaine; 2 — Reference; What is still unsettled… (rest unrelated) |
| 10.1111/j.1468-3083.2010.03653.x (25) | 16 | Safe Doses; prilocaine-wheals |
| high dose tumescent local anaesthesia prilocaine interleukin (25) | 16 | Safe Doses; prilocaine-wheals; Prilocaine + Lidocaine; Comparing…; EMLA product pages (topical) |
| tumescent anaesthesia prilocaine methaemoglobin (30) | 16 | as above + Product Guide, Reference, What is still unsettled… |
| Lindenblatt prilocaine liposuction (25) | 18 | prilocaine-wheals (only page naming Lindenblatt) |
| interleukin-6 cytokine after local anaesthetic systemic inflammation (25) | 19 | Relief that outlasts the block…; Ropivacaine Wheals; Anaesthetics (checked below) |
| methemoglobin after prilocaine infiltration measured patients (40) | 17 | prilocaine-wheals; Safe Doses; Prilocaine + Lidocaine; Reference; Product Guide |
PMID 20384691 was not searched separately: the page texts were searched for it after fetching (0 hits on every page).

### 5.5 Other pages fetched and searched (text searched for Guay, Schmittner, Lindenblatt, Sertdemir, Yalcin, tumesc,
liposuc, interleukin/IL-6/cytokin, methaemoglobin spellings, contrasting, 242)
- Prilocaine + Lidocaine — https://app.notion.com/p/33110b7903aa8024a793d7249262b267 — as of 2026-10-02T03:14:00.887Z,
  100,421 chars, complete. Guay cited once (Sources › Methaemoglobinaemia, with "275 Smart Citations with 3 supporting
  and 3 contrasting"); no Schmittner, Lindenblatt, tumescent or cytokine mention. Nothing for this paper.
- Comparing the injectable local anesthetics for intradermal wheals — https://app.notion.com/p/3c510b7903aa81208d4fe305e7cb069b
  — as of 2026-10-02T03:14:02.626Z, 105,800 chars, complete. No methaemoglobin/Guay/Schmittner/tumescent text; one
  sentence on the delayed systemic effect (see 5.6). Nothing for this paper.
- 2 — Reference — https://app.notion.com/p/3d410b7903aa81a4ada4c3830a567c65 — as of 2026-10-01T02:05:48.095Z,
  1,279,938 chars; the two "truncated" hits are ordinary page text (a MEDLINE rendering; a registro number), the
  fetch ends with </page>. Guay = S183 (§4.2.3 and Sources); no Schmittner, Lindenblatt, Vasters, Rudlof, Sagoo, Mang,
  tumescent or liposuction mention; cytokine mentions concern vitamin D and vagus-nerve stimulation. Nothing for this paper.
- 1 — Product Guide — https://app.notion.com/p/3d410b7903aa81c0815ad3c7c6c2d17f — as of 2026-10-02T03:14:29.224Z,
  599,993 chars, complete. No Guay/Schmittner/tumescent; methaemoglobin text concerns topical EMLA/benzocaine products.
  Nothing for this paper.
- What is still unsettled… — https://app.notion.com/p/3d410b7903aa819f8300e976a62577db — as of 2026-09-26T18:23:10.973Z,
  61,415 chars; "truncated" hits are ordinary text (registro numbers). Methaemoglobin text concerns EMLA ceilings
  (dose subject, not copied). No open question this paper answers.
- 5 — Soft ground in these documents — https://app.notion.com/p/3d410b7903aa81e88fbdc2ab883b1403 — as of
  2026-09-26T18:26:13.509Z, complete. No prilocaine/methaemoglobin/Guay content. Nothing for this paper.
- What was searched for and does not exist… — https://app.notion.com/p/3d410b7903aa8169b833f5997631cc82 — as of
  2026-09-27T00:27:49.877Z, 64,683 chars, complete. No prilocaine/methaemoglobin/Guay; "cytokine" only for topical
  cytokine-directed agents. Nothing for this paper.
- What transfers… — https://app.notion.com/p/3d410b7903aa813681e9c27892149a17 — as of 2026-09-26T18:27:17.888Z, complete.
  No hits. Nothing for this paper.
- Ropivacaine Wheals — https://app.notion.com/p/2c010b7903aa83a0b9e3813036c9d26e — as of 2026-10-02T03:14:26.511Z,
  399,446 chars, complete. No Guay/Schmittner/methaemoglobin. Tumescent passages ("6.8a … 4. Tumescent pharmacokinetics":
  Klein 1990, Rubin 1999, Kenkel 2004 "with systemic peaks arriving 4 to 14 hours later"; 6.9 tumescent record) are
  consistent with Schmittner (serum prilocaine highest at the 4-h sample after tumescent infusion). No finding.
- mepivacaine-wheals — https://app.notion.com/p/3c510b7903aa8152b01bf10e2f980185 — as of 2026-10-02T03:14:08.315Z,
  complete; bupivacaine-wheals — https://app.notion.com/p/3d310b7903aa81469517da5f7c05e37d — as of
  2026-10-02T03:14:18.695Z, complete. No methaemoglobin/Guay/Schmittner/tumescent text. No finding.
- 💊 Anaesthetics — https://app.notion.com/p/3c410b7903aa80a0b250f26d55808492 — as of 2026-10-01T03:07:38.200Z, complete.
  No hits.
- Injectables ruled out but not tried — https://app.notion.com/p/3d310b7903aa81fca5adcc979f03c0d5 — as of
  2026-10-02T03:14:22.080Z, complete. No methaemoglobin/Guay/Schmittner/tumescent text.
- Relief that outlasts the block… — https://app.notion.com/p/3d310b7903aa811cb51bcca149b3de73 — as of
  2026-10-02T03:14:06.492Z, 76,085 chars, complete. Its anti-inflammatory discussion rests on in-vitro assays (Picardi
  2013, de Klaver 2006, Weinschenk 2022) and states "The Gq anti-inflammatory action fits one structure–activity
  dataset, is contradicted by another, and has never been tested against a clinical durability endpoint. What would
  settle it: a trial carrying an inflammatory biomarker as a mediator." Schmittner measured systemic IL-6, IL-8 and
  TNF-alpha in vivo after a local anaesthetic, but with one drug, no comparator, no drug-free or surgery-free control and
  no pain endpoint, so it neither settles nor contradicts these sentences (it reports IL-6 rising after surgery under
  high-dose prilocaine, not falling). No finding; recorded so the main session knows it was considered.

### 5.6 Considered and not written as findings
- prilocaine-wheals, "What does all of this mean for a wheal?": "Methemoglobin is systemic and delayed, produced by a
  breakdown fragment circulating in the blood, peaking around two and a half hours after the dose is absorbed, and
  unaffected by where the needle went." The comparison page has the same sentence. Schmittner sampled at 1, 2, 4, 12,
  24, 48, 72 h after subcutaneous tumescent infusion: serum prilocaine was highest at the 4-h sample and mean
  methaemoglobin at the 12-h sample (two of the three patients with markedly raised values had their maxima at 12 h).
  Lindenblatt's abstract also notes earlier large-volume liposuction studies with methaemoglobin "up to 12 h
  postoperatively". Because the page's sentence is qualified "after the dose is absorbed" (absorption from a tumescent
  depot is prolonged) and the 4-h/12-h samples only bracket the true peak, the sentence is not shown wrong; no finding
  written. The main session may still wish to note that a single sample a few hours after a subcutaneous depot can
  precede the methaemoglobin maximum.
- Schmittner's own conclusion sentences that read as safety judgements ("TLA with high dose prilocaine is considered to
  be safe in case of inflammatory response…") are not quoted anywhere in these results.

### 4b. Abstracts fetched (get_article_metadata) and cached (pmcache.py article)
- 19224791 Guay 2009 — cached REDACTED: the dose ceilings for children/adults/renal impairment/oxidising drugs, the
  closing limit, the methaemoglobin levels given for coma, the single-spray benzocaine sentence and the rebound/
  methylene-blue (antidote) sentence replaced by [dose figure omitted]. Read unredacted from the connector: its results
  give a higher figure for adults; its conclusion gives a general limit identical to the one Schmittner adopts.
- 15870963 Lindenblatt 2004 — cached REDACTED: solution concentration, average and maximum dose, plasma level and
  methaemoglobin values replaced. Design kept: 25 patients, 4 h of sampling, conclusion about a 12-h monitoring period.
- 41945359 Sertdemir 2026 — cached REDACTED: solution strength, methaemoglobin thresholds and the ROC dose cut-off
  replaced. Abstract does not mention Guay; reports a predictive cut-off, not a recommended limit.
- 40641322 Yalçın 2025 — cached as returned (no dose figures). Abstract does not mention Guay and recommends no limit;
  associations reported are with creatinine, BMI and haemoglobin.
- 20384691 Schmittner 2010 — abstract read (matches the PDF), not cached (quotes come from the full text).
- 16723054 Vasters 2006, 17370052 Rudlof 2007 — abstracts read, not cached (not quoted; no verdict rests on them).
- Reference-list items left out of the card's studies_it_cites_that_matter (no bearing on the pages' topics): Hack 2001
  (11445730, endothelium in sepsis), Spolarics 1998 (9581796, hepatic sinusoid), Chernik 1990 (2286697, sedation scale),
  Pfaefflin 2009 (19104782, point-of-care inflammation markers), Gabay 1999 (9971870, acute-phase proteins), Il'yasova
  2008 (17852073, CRP/IL-6 and oxidative stress), Vos 2009 (19328934, CRP after lung transplantation).

## 6. Claim screen (all 320 claims)

First pass (before the coordinator's note): Python regex over claim, elements, reason, proposed wording, evidence quote,
review, section, records_read and needs_full_text, for: prilocain|citanest|propitocain|xylonest; meth?a?emoglobin|methb|
mhb|cyanos; tumesc|liposuc; cytokin|interleukin|IL-6|IL-8|TNF|inflammat|C-reactive|CRP; guay; lindenblatt; sertdemir;
yal[cç][iı]n; schmittner|20384691; emla|lidocaine-prilocaine|eutectic; toluidin; systemic tox|plasma/serum level/conc;
scite|contrasting; and the reference-list authors (Mang, Rudlof, Sagoo, Vasters, Kortgen, Ash-Bernal, Dumont, Khan).
Second pass, repeated with the masked viewer (pm_work/tools/claims_view.py grep, dose figures masked) for the same
terms plus inflammat; EMLA|eutectic|lidocaine-prilocaine; dermatolog* surg|resection|melanoma|acne|day surgery|
ambulatory|subcutaneous infus. Hits: prilocaine 18, methaemoglobin 4, tumescent 2, cytokine terms 0, named authors 3,
systemic/plasma 4, contrasting/Scite 3, inflammat 5, EMLA 7, surgery/route terms 7.

Kept (claim updates written):
- C071 (own question) — narrowed → narrowed, uncertain_after false (Schmittner full text; Guay abstract as extra study).
- D075 (Safe Doses, same sentence as C071's source note) — out-of-scope → out-of-scope; full text settles its framing.
- C068 (prilocaine-wheals, methaemoglobin series after small-dose infiltration) — narrowed → narrowed; Schmittner is a
  further series of ordinary patients with serial methaemoglobin, but at large doses (small-dose element unmatched).

Read closely and dropped:
- C069 (no methaemoglobin measurement after a milligram-scale intradermal dose): Schmittner is large-dose, subcutaneous;
  outside scope, consistent with "every figure on this page comes from doses at least ten times larger".
- C070 (repeated small doses across sessions): single session, large dose; outside scope.
- C065, C066, C067, D006, D009, D010, D023, D024, D039, D054, D062, C039 (prilocaine or other agents' intradermal duration,
  injection pain, comparisons): Schmittner times no anaesthesia and measures no injection pain. D009 (prilocaine with
  epinephrine "not measured in skin") — Schmittner injected prilocaine with epinephrine into subcutaneous tissue but
  measured no duration, so the outcome element is unmatched.
- C049, D005, C046, D013, C054 (nerve or tissue damage): not studied.
- D014 (skin nerve fibre density), D018 (buffering), D066–D068 (EMLA cream), E028 (topical lidocaine duration): other
  route/outcome.
- C084 (tissue oxygen for eight hours): Schmittner monitored arterial oxygen saturation only during surgery, no tissue
  oxygen; dropped.
- D038 (Gq anti-inflammatory action never tested against a clinical durability endpoint) and D028: Schmittner measured
  systemic cytokines after a local anaesthetic but had no pain or durability endpoint and no comparator; does not bear.
- D042 (no contrasting citation against durability claims): different page and topic.
- C014 (clonidine, plasma levels as a vasoconstriction marker): unrelated.
- A001/A003/A004/A006/A028/A046/A058/C005/C008/C062/C088/E015 (first-pass inflammation/cytokine word hits): unrelated
  topics (alpha-lipoic acid, vitamin D, stem cells, GLP-1, naltrexone, diet, botulinum toxin, epinephrine tissue
  inflammation in animals, laser Doppler, eugenol).

Count lines for claims skipped under the filter rule (subject is a dose ceiling, toxicity level or injection practice):
- Safe Doses Of Intradermal Analgesics: 2 claims not tested: dose or toxicity subject (D069, D073 — the two of the
  page's dose-subject claims that touch this paper's topics: plasma levels after a session; epinephrine in skin
  infiltration). The page's other dose-subject claims (D070, D071, D072, D074) do not overlap this paper. In any case the
  paper's design (one subcutaneous tumescent session, no wheals, no cardiovascular outcome reported) is outside their scope.
- prilocaine-wheals: 0 claims skipped; C071 answered under the own-question exception (citation and framing only, no
  figures). Prilocaine + Lidocaine: 0 claims skipped.

## 7. PubMed searches (connector; logged with pmcache.py)
- (Mang W[Author] OR Mang WL[Author]) AND (Prilocain*[tiab] OR Liposuktion[tiab] OR liposuction[tiab] OR
  Tumeszenz*[tiab]) — count 0 (translation recorded in pm_work/cache/s_mcp_4c341718c8bf5739.json). Mang 1999 is not in
  PubMed.
- All other identifications were by lookup_article_by_citation (section 4) and get_article_metadata (section 4b).

## 8. Not reached / problems / instructions in documents
- Scite connector refused (paid plan or trial required) — not pursued; the "contrasting citation" classification of
  Guay's citers is unverified.
- Mang 1999, Sagoo 2000 and Klein 1987 are not in PubMed; not read.
- No instructions aimed at this agent were found in the paper, the abstracts or the Notion pages. The Safe Doses page
  carries reader-directed caveats (quoted in 5.2) — page content, not instructions to the agent.
- No content-filter stops.
