# S-686-37 — Wang 2011, GRK2 in sensory neurons / epinephrine-induced hyperalgesia

## 0. Content-filter event (read this first)

Early in this session a write that was to carry the paper's methods figures (the exception in the
hand-over for a paper whose own question asks what the study itself used) was **stopped by the content
safety filter**. Per the hand-over rule ("don't retry it and don't rephrase around it") the figures were
not written anywhere afterwards. So:

- **Not done: stopped by the content filter** — the numeric part of the own question (the epinephrine
  amount/volume Wang injected). Everywhere it would have gone — the paper card's `intervention`, and
  claim C090's `reason` — it is written as `[dose figure omitted]`.
- Everything else in the own question (the **route**, whether it was a **single** injection, and the
  comparison with Khasar 1999) is answered in full: those are not dose figures.
- The paper does report a second, lower epinephrine amount in one mechanical-hyperalgesia experiment
  (Fig. 1C) and discusses a possible leftward shift of the dose–response curve. That *existence of a
  second amount* is recorded (it matters for C090), without the figures.

## 1. Right-paper check

- Text file: `texts/S-686-37.txt`, 10 PDF pages, from
  `papers/S-686-37 - Wang 2011 - GRK2 in sensory neurons regulates epinephrine-induced signalling and duration of mechanical hyperalgesia.pdf`.
- PDF page 1 title: "GRK2 in sensory neurons regulates epinephrine-induced signalling and duration
  of mechanical hyperalgesia"; authors "Huijing Wang, Cobi J. Heijnen, Niels Eijkelkamp, Anibal Garza
  Carbajal, Manfred Schedlowski, Keith W. Kelley, Robert Dantzer, Annemieke Kavelaars"; journal line
  "PAIN 152 (2011) 1649–1658"; "doi:10.1016/j.pain.2011.03.010". Matches the assigned paper
  (PMID 21514055, DOI 10.1016/j.pain.2011.03.010). **Right paper: yes.**
- Text quality: **ok**. Extraction oddities to know about when quoting: the superscript minus of
  genotypes is lost, so "GRK2+/−" appears as "GRK2+/ " and "GRK2−/−" as "GRK2 / "; the micro-litre
  unit is rendered "lL"; "PKCε" is "PKCe"; "β" is "b"; "α" is "a"; the journal's logo character "Ò"
  appears at the top of each page. No pages missing; references complete ([1]–[35]).
- `common/papers_list.csv` `person_note` for this paper: checked (see §2).
- No instructions aimed at the reader were found inside the paper.

## 2. The paper, in the terms the claims need

- Design: controlled laboratory experiments in mice, genotype and drug-pretreatment comparisons,
  experimenter blinded ("The experimenter was blinded for genotype and treatment during all
  measurements", PDF p. 3).
- Population: male and female C57BL/6 mice, age 12 to 14 weeks; wild-type littermates vs GRK2+/−;
  cell-specific lines (sensory-neuron/Nav1.8 SNS-GRK2+/−, microglia/macrophage LysM-GRK2+/−,
  astrocyte GFAP-GRK2+/−) and tamoxifen-inducible GRK2+/− and GRK2−/−.
- n: n = 8/group for the hyperalgesia time courses; n = 4–6/group for the adrenoceptor-blocker
  experiments; n = 6–8/group for the signalling-inhibitor experiments; n = 3–4/group for Western blots
  and DRG morphology.
- Intervention and route: **one intraplantar injection of epinephrine into the hind paw**
  (`[dose figure omitted]`), not an intradermal injection. Inhibitors/blockers (phentolamine,
  ICI-118,551, H-89, TAT-PKCεv1-2, U0126) were given intraplantarly 30 minutes before the epinephrine
  injection; saline, scrambled peptide or vehicle were the controls.
- Outcomes: mechanical hyperalgesia as the change in 50% paw withdrawal threshold (von Frey hairs,
  up-and-down method) and thermal hyperalgesia as heat withdrawal latency (Hargreaves test), both
  measured repeatedly after the single injection out to about three weeks; plus GRK2 protein by Western
  blot in DRG, spinal cord and peritoneal macrophages, and DRG neuron morphology (IB4/α-tubulin).
- Headline result: after one epinephrine injection, mechanical and thermal hyperalgesia lasted
  **3 to 4 days in wild-type mice and approximately 21 days in GRK2+/− mice**; reduced GRK2 in sensory
  neurons alone reproduced the prolongation; low GRK2 switched the signalling from PKA-dependent to
  PKCε-dependent, with MEK/ERK involved in both.
- A second, lower epinephrine amount was also tested in one mechanical experiment (Fig. 1C): "At a low
  dose of EPI ([dose figure omitted]), mechanical hyperalgesia also lasted longer in GRK2+/ than in WT
  mice (Fig. 1C). In addition, at this low dose of EPI, acute hyperalgesia was increased in GRK2+/
  mice." (PDF p. 4) and in the discussion: "These findings indicate that low GRK2 may shift the
  dose-response curve for EPI to the left." (PDF p. 7). So two amounts appear, but both arms of that
  comparison are genotype comparisons, and no duration-versus-amount relationship is reported for
  wild-type animals.

## 3. Claim screen over all 320 claims in common/claims_all.json

Method: a Python screen of the whole JSON (claim sentence, `elements_said_absent`, verdict, reason, review,
proposed wording, evidence PMID, records_read), then close reading of every candidate.

Screen terms used: epinephrine, adrenaline, adrenalin, epi-, vasoconstrictor, hyperalges, sensitis, sensitiz,
nociceptor, priming, primed, GRK2, PKA, protein kinase, PKC, PKCe, Khasar, Levine, Aley, Dina, catecholamine,
stress, sympath, denervat, supersensitiv, adrenergic, adrenoceptor, two-hour, two hour, 90 minutes, window,
allodyni, mouse, mice, rat, 21514055, 10085337, "Wang 2011".

Result of the screen: 149 claims matched on the loosest terms, 101 on the core terms; **C090 is the only claim
in the whole file that cites Wang 2011 (PMID 21514055), Khasar, or GRK2** (checked directly: no other claim's
JSON contains any of those strings).

Claims read closely and dropped, with why:

- **C072–C089, C091–C094** (the same page as C090, 💉 Lidocaine With Epinephrine Wheals). All are about the
  vascular/anaesthetic side — skin or nerve blood flow, tissue oxygen, duration of anaesthesia, drug levels in
  tissue, necrosis case reports, intraepidermal fibre counting after repeated injections, a review's
  recommendation. Wang 2011 injected no local anaesthetic, measured no blood flow, oxygen, drug level or skin
  histology, and gave one injection rather than repeated ones; it bears on none of them.
  - C082 (A-delta versus C fibres treated separately, "with epinephrine in the mixture") looked closest:
    dropped because Wang 2011 has no local-anaesthetic mixture and no fibre-class electrophysiology — its
    only fibre-subtype work is IB4 staining of dorsal root ganglion cell bodies, reported as finding no
    genotype difference.
  - C075 (nerve fibre counting after repeated epinephrine-containing infiltration) dropped: single injection,
    no skin histology.
- **C091 and C093**: not re-judged — subject is how to mix/dilute a product, and tissue damage at a stated
  amount. *💉 Lidocaine With Epinephrine Wheals: 2 claims not tested: dose or toxicity subject.*
- **D069–D075** (Safe Doses Of Intradermal Analgesics): every claim on that page is about a maximum, a ceiling,
  an interval between sessions or a cap. Not re-judged, not quoted.
  *Safe Doses Of Intradermal Analgesics: 7 claims not tested: dose or toxicity subject.*
- **C014–C030** (adjuvants-without-a-vasoconstrictor): alpha-2 agonists (clonidine, dexmedetomidine),
  dexamethasone, magnesium; vascular supersensitivity after denervation. Wang 2011 used a non-selective
  alpha blocker only as a control in mice and found it did not change epinephrine hyperalgesia; it measures
  no vascular endpoint and no human endpoint, so it does not touch C017/C018/C019 (which ask for human
  measurements of alpha-2 effects) or the adjuvant claims.
- **C032–C048** (🔬 The intradermal wheal literature…): human intradermal anaesthetic duration, a citation that
  could not be confirmed. No bearing.
- **C053–C068** (articaine-, prilocaine-wheals): epinephrine as an additive to a dental or dermal anaesthetic.
  No bearing. ("Dina" matched only as a substring of other words in C063/C068.)
- **D000, D001, D002, D007, D009, D011, D013, D023, D034, D036, D038, D054, D056, D060** (Comparing the
  injectable local anesthetics…, Relief that outlasts the block…, Procaine / Novocaine): skin blood flow at a
  wheal, durability of relief, procaine in dermis. No epinephrine-hyperalgesia content. No bearing.
- **A008, A009, A038, A039, A040, A055, A066, A087, A089** (SFN treatment and systemic-drug pages): matched on
  "sensitiz"/"nociceptor"/"hyperalges" in unrelated contexts (irritable-nociceptor phenotype, alpha-lipoic
  acid, oxcarbazepine). No bearing.
- **E000–E044** (Pain biology…; Menthol…): eugenol, capsaicin, menthol, central sensitisation indices,
  topical agents. No epinephrine work. No bearing.
- **C008** (botulinum, contralateral effect) and **T08** (capsaicin strength): no bearing.

So this paper produces **one** claim update (C090, its own question) and **no** `other-claim` entries.

## 4. PubMed (via the PubMed MCP connector; `common/tools/pm.py` cannot run — eutils is blocked)

Search run (count and the connector's query translation are in `pm_work/cache/s_mcp_0bcec27ae8a96abf.json`):

- `(epinephrine[tiab] OR adrenaline[tiab]) AND (hyperalgesia[tiab] OR hyperalgesic[tiab] OR sensitization[tiab])
  AND (duration[tiab] OR "time course"[tiab] OR prolonged[tiab] OR "dose-dependent"[tiab] OR "dose-response"[tiab])
  AND (skin[tiab] OR intradermal[tiab] OR cutaneous[tiab] OR intraplantar[tiab] OR paw[tiab])` — **count 13**,
  all 13 screened. Hits since 1999 that concern epinephrine-induced hyperalgesia: 21514055 (this paper),
  19576859 (Khasar 2009), 29715452 and 16259764 (both use epinephrine hyperalgesia only as an assay for a plant
  compound, neither reports a time course or a dose–duration relation), plus 10085337 (Khasar 1999). The
  remainder (38408153, 37854067, 23521101, 15197017) are allergy/veterinary papers that matched on the word
  epinephrine/adrenaline; 9630485, 7797175, 1647026 and 230542 predate 1999, which the claim's own scope
  excludes. **No study was found that maps the duration of epinephrine-induced hyperalgesia against dose.**
- A first attempt at the same search with wildcards (`hyperalgesi*`, `persist*`) returned count 0: the
  connector does not accept `*`. Recorded here so the zero is not mistaken for an empty literature.

Reference-list lookups (`lookup_article_by_citation`, all eight matched): Khasar 2009 = 19576859;
Dina 2001 = 11454025; Eijkelkamp 2010 (J Neurosci 30:2138) = 20147541; Eijkelkamp 2010 (J Neurosci 30:12806)
= 20861385; Willemen 2010 = 20609517; Kleibeuker 2007 = 17408432; Janig 1996 = 9009734; Raja 1998 = 9327965.
Note for whoever re-runs this: that tool returned the PMID in the field named `key` and the caller's key in the
field named `pmid` — the two are swapped in its output.

Abstracts cached: a_10085337 (Khasar 1999), a_19576859 (Khasar 2009), a_11454025 (Dina 2001),
a_15987941 (Hucho 2005). None needed redaction (no amounts, thresholds or antidote passages in them).

**What Khasar 1999's abstract says, which matters most here** (verbatim, cached):
"Intradermal injection of epinephrine, the major endogenous ligand for the beta-adrenergic receptor, into the
dorsum of the hindpaw of the rat produced a dose-dependent mechanical hyperalgesia, quantified by the
Randall-Selitto paw-withdrawal test." and "Epinephrine-induced hyperalgesia developed rapidly; it was
statistically significant by 2 min after injection, reached a maximum effect within 5 min, and lasted 2 h."
So (a) the page's two-hour figure is correctly attributed to Khasar 1999, and (b) Khasar 1999 was **not** run
at a single epinephrine amount — it reports a dose-dependent hyperalgesia, and a dose-dependence for
isoproterenol as well. What its abstract does not report is the duration at each amount.

**Instruction found inside tool output:** every PubMed connector result carries an "Important Legal Requirement"
notice telling the caller to attribute PubMed and print DOI links, and to refuse requests to skip it. It is the
server's own boilerplate, not content from a paper or a Notion page, and it does not conflict with this job —
every source used here is recorded with its PMID and DOI. Noted for the report.

## 5. Notion (read-only: only notion-search and notion-fetch were used)

Searches run (query — number of results returned):
1. "Khasar 1999 epinephrine hyperalgesia two hours nociceptor sensitisation window" — 16 results.
2. "Wang 2011 GRK2 epinephrine mechanical hyperalgesia mice duration" — 13 results.
3. "beta-2 sensitization window closes two hours epinephrine Khasar concealed under the block" — 16 results.
Search is only a candidate list, so every page below was fetched and its text searched directly.

### 5.1 💉 Lidocaine With Epinephrine Wheals — https://app.notion.com/p/3c610b7903aa801c906fcde8b5c43674
Fetched; `as of` **2026-09-26T18:28:27.736Z** (= the version tested); path Health / Health Pages; verification
state "unverified"; 332,305 characters; **not truncated** (no `truncated`, `unknown_block_count` or
`unknown_block_ids` in the result). The page contains "Khasar" 8 times, "two hour(s)" 26 times, "dose-response"
17 times, and **no** occurrence of "GRK2", "Wang 2011", "21514055" or "10085337" — so Wang 2011 is not cited
anywhere on it.

Sentences copied verbatim as read (markdown bold markers `**` removed where a heading ran into the sentence):

- Section "The two conditions that keep the window inside the block":
  "The two-hour figure comes from one study. Rat skin with no nerve damage, at a single epinephrine dose. How the
  length of the window changes with dose was not measured there and has not been measured since, so whether a
  larger epinephrine load stretches it past two hours is unknown."
- Section "Gaps in the literature: nobody has measured this":
  "The two-hour sensitization window is a single measurement in a single species. Rat skin with no nerve damage,
  at one epinephrine dose. Human neuropathic skin might sensitize for longer or shorter, and the dose-response
  was never mapped."
- Section "Where your own numbers land in that analysis" / "The concealment argument survived, on its own terms":
  "Beta-2 sensitization is a two-hour effect. The blanching outlasted the block by far longer than the block
  outlasted the sensitization, so whatever the vasoconstriction was doing after hour two, it was not being
  concealed by anything."
- Section "Rests on a single study, and should be held loosely":
  "That the beta-2 sensitization window closes at two hours (Khasar)."
- Sources › "Receptors and sensitization" (the source register entry):
  "Khasar SG, McCarter G, Levine JD. Epinephrine produces a beta-adrenergic receptor-mediated mechanical
  hyperalgesia and in vitro sensitization of rat nociceptors. Journal of Neurophysiology 1999;81(3):1104–12.
  Read in full. — The beta-2 chain, the two-hour sensitization window, the independence from sympathectomy and
  indomethacin, and the confirmation that the paper never separates C-fibres from A-delta fibres. ... Limits:
  rat skin with no nerve damage; a single named dose ([dose figure omitted]) for the timing data; no
  dose-response for how long the window lasts."
  — note this register entry is **accurate**: it ties the single amount to the *timing data* specifically, and
  says there is no dose-response *for duration*. The two body sentences above compress it into "at a single
  epinephrine dose" / "at one epinephrine dose", which describes the whole study wrongly. The page therefore
  disagrees with itself, and the register is the side that matches Khasar 1999's abstract.
- Also on the page, in the methods/dose discussion of Khasar: "And the dose behind the timing figures above was
  concentrated rather than large in total: [dose figures omitted]" — recorded only to note that the page already
  knows the timing figures came from one amount.

### 5.2 Other pages fetched and searched (all read-only; every one searched in its own text)

| Page | `as of` | Truncated? | What it holds on this topic |
|---|---|---|---|
| 🕳️ What was searched for and does not exist, so it is not searched for again (3d410b7903aa8169b833f5997631cc82) | 2026-09-27T00:27:49.877Z | no | No "Khasar", "epinephrine", "adrenaline", "hyperalges" or "GRK2" anywhere. The page is about pruritus and topicals. Nothing to correct. |
| What is still unsettled across these pages, and what would settle each one (3d410b7903aa819f8300e976a62577db) | 2026-09-26T18:23:10.973Z | no (the word "truncated" on it is the page's own wording about a registro number) | No "Khasar", "sensitiz", "hyperalges", "nociceptor", "GRK2". Its epinephrine lines are about label ceilings and a blanching-versus-analgesia timing question. The sensitisation window is not among its open questions, so there is nothing here for an `open-question-answered`. |
| 5 — Soft ground in these documents (3d410b7903aa81e88fbdc2ab883b1403) | 2026-09-26T18:26:13.509Z | no | Read in full. About pooled-estimate/denominator errors, unopenable sources and the retraction sweep. No epinephrine or sensitisation content. |
| 2 — Reference — Topical Treatments for SFN, source register S1–S457 (3d410b7903aa81a4ada4c3830a567c65) | 2026-10-01T02:05:48.095Z | no | 1,279,938 characters, searched for the author and year as the hand-over asks: **no "Khasar", no "GRK2", no "21514055", no "10085337", no "beta-2", no "beta-adrenergic"**. Its "hyperalges"/"nociceptor" hits are capsaicin, menthol and phenytoin material; its "two-hour" hits are a phenytoin infusion and a glucose tolerance test. Neither paper is in the register, and nothing in it needs correcting from this paper. |
| 1 — Product Guide (3d410b7903aa81c0815ad3c7c6c2d17f) | 2026-10-02T03:14:29.224Z | no | No "Khasar", "GRK2", "sensitiz" or "beta-2". Its epinephrine passages are product rows, ceilings and an exclusion recorded as the reader's own preference — dose/ceiling subject matter, not re-judged and not quoted here. Nothing this paper bears on. |
| Comparing the injectable local anesthetics for intradermal wheals (3c510b7903aa81208d4fe305e7cb069b) | 2026-10-02T03:14:02.626Z | no | No "Khasar", "sensitiz", "hyperalges", "nociceptor", "beta-2". Duration-of-anaesthesia and flow material only. |
| Ropivacaine Wheals (2c010b7903aa83a0b9e3813036c9d26e) | 2026-10-02T03:14:26.511Z | no | No "Khasar", "GRK2", "beta-2", "two-hour". Its "hyperalges" hits are a systemic-lidocaine C-fibre study. 144 mentions of epinephrine, all vascular/adjuvant. Nothing for this paper. |
| mepivacaine-wheals (3c510b7903aa8152b01bf10e2f980185) | 2026-10-02T03:14:08.315Z | no | **None** of Khasar / GRK2 / sensitiz / sensitis / hyperalges / beta-2 / two-hour / nociceptor / 21514055 appears. |
| bupivacaine-wheals (3d310b7903aa81469517da5f7c05e37d) | 2026-10-02T03:14:18.695Z | no | Same: none of those terms appears. |
| 💊 Anaesthetics (3c410b7903aa80a0b250f26d55808492) | 2026-10-01T03:07:38.200Z | no | Sourcing page (dental depots, cartridges). None of those terms appears. |
| Nociceptors (22410b7903aa80b9909fcef2d3597d48) | 2026-09-26T18:22:15.582Z | no | Read in full. A general explainer on transduction, TRPV1 and peripheral sensitisation; no adrenergic or epinephrine content and no literature-absence claim. Nothing to correct. |
| Lidocaína FD con epinefrina, dental cartridges — product row (3e010b7903aa81aea93ec8e114bf10c2) | 2026-09-27T10:58:16.937Z | no | Read in full as the representative of the family of lidocaine-with-epinephrine product rows the searches surfaced (the others repeat the same two sentences). Its literature statements are "no wheal study used an anaesthetic with epinephrine, so its evidence is only indirect, from one uncontrolled study of plain lidocaine" and "A wheal study of an epinephrine-containing anaesthetic with a pain outcome, in any neuropathic pain condition, would settle the verdict." Both stay true: Wang 2011 is not a wheal study and used no anaesthetic. No finding. (Its Edits log also records that the person ruled dose ceilings, antidotes and overdose arithmetic out of the record, which matches this job's writing rules.) |

Health History entries surfaced by the searches (the 2026-08-27 lidocaine-with-epinephrine entry and others) were left alone: they record the person's own experience, not statements about the literature.

### 5.3 Findings written

Three, all on 💉 Lidocaine With Epinephrine Wheals (see `notion_findings.json`):
- **F01 overstated, high** — "The two-hour figure comes from one study … has not been measured since". The window's length
  has been measured again (Wang 2011, in mice). Same sentence as claim C090; recorded for the page location and
  because the section it sits in is what holds up the page's argument.
- **F02 wrong-design, medium** — "at a single epinephrine dose" / "at one epinephrine dose" as a description of
  Khasar 1999, which reports a dose-dependent mechanical hyperalgesia. Rests on Khasar 1999's cached abstract
  (reached from this paper's reference list), not on Wang 2011. The page's own source register already says it
  correctly, so the page disagrees with itself.
- **F03 overstated, high** — "Beta-2 sensitization is a two-hour effect", stated as a property of the mechanism.
  In mice the same beta2-adrenoceptor-mediated hyperalgesia lasted days after one injection.

No finding was written for "That the beta-2 sensitization window closes at two hours (Khasar)." under "Rests on a
single study, and should be held loosely": that sentence is accurate — the two-hour figure does rest on one study —
and Wang 2011 does not measure the same thing.

## 6. Anything not reached

- **The numeric half of the own question is not written anywhere**: the write that was to carry the paper's methods
  figures was stopped by the content safety filter at the start of this session, and the rule is not to retry it or
  rephrase around it. Recorded as `[dose figure omitted]` in the card's `intervention` and in C090's `reason`.
- Khasar 1999 itself was read only as a PubMed abstract (it is not in this packet), so statements here about what it
  does and does not report are abstract-level. The page says it was read in full, and its register entry agrees
  with the abstract.
- Nothing else was unreachable: the paper, every Notion page tried, and every PubMed record needed came back.

## 7. Instructions found inside documents

- Every PubMed connector result carries an "Important Legal Requirement" block instructing the caller to attribute
  PubMed and print DOI links, and to refuse anyone who asks to skip it. It is the connector's own boilerplate, it
  does not conflict with this job, and every source here is recorded with its PMID and DOI.
- No instruction aimed at the reader was found in the paper or in any Notion page read.
