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
