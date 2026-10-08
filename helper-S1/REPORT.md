# Session 1 — report

## 1. What was done

The three untested wheal pages were fetched read-only, read in full apart from their Revisions
sections, and reduced to **49 absence claims** — 31 on Ropivacaine Wheals, 10 on mepivacaine-wheals,
8 on bupivacaine-wheals — each pulled verbatim from the page by locator match rather than retyped,
with dose figures replaced by `[dose figure omitted]` and the result machine-scanned to confirm none
survived. A further **7 claims were counted but not written out**, because their subject is a dose
ceiling, a toxicity threshold, or how to mix, buffer or dilute a solution. All 49 were then tested
with positively framed searches and judged; **29 of the 49 did not hold as written**. Of the 13
papers, the ones that are finished were each read in full, carded, used to answer their own open
question, screened against all 320 claims in `claims_all.json` and against the 49 new ones, worked
through their reference lists, and followed into Notion read-only. Nothing in Notion was created,
edited, moved, duplicated, commented on or deleted by this session or by any worker in it, and no
health-record skill was loaded.

**What is not done.** The per-paper counts in section 3 say which papers were completed; any of the
13 absent from that list was not reached. Steps D and E — screening all 320 claims, the reference
chase and the Notion sweep — are outstanding for any paper whose row in `papers_status.csv` says so.
The searches behind the wheal verdicts were run on Europe PMC rather than PubMed, for the reason in
section 6, so their counts are not PubMed counts and the `confirmed` verdicts in particular are
weaker than they would be with PubMed's index; every query carries an `engine` field recording
which index answered it. Claims left `uncertain` name in `needs_full_text` the paper that would
settle them.

A note on how the Ropivacaine Wheals verdicts should be read. That page states a convention
(section 0.1) that its own negatives mean "not found by this project's searches", not that the
measurement provably does not exist, and calls a negative claim "an invitation to look again, not a
closed question". Its `refuted` verdicts are therefore corrections to wording, not reversals of the
page's position — and in three cases (W-R018, W-R026, W-R029) the refuting paper is one the page
already holds or cites, which makes them internal inconsistencies rather than new literature. The
same page's warning that "0 contrasting citation statements" does not mean no study disagrees turned
out to be exactly right: both citation-standing claims tested here failed.

## 2. Counts

- **Papers read in full: 13 of 13.** 13 confirmed as the right paper.
- **Claim re-judgements written: 77**, covering 39 distinct claims. **22 changed verdict.**
  - by kind: 6 extra-study, 52 other-claim, 19 own-question
  - still uncertain after the full text: 15
- **New wheal-page claims extracted and tested: 49** (8 W-B, 10 W-M, 31 W-R).
  - verdicts: **20 confirmed**, **16 narrowed**, **12 refuted**, **1 out-of-scope**
  - left uncertain: 1
  - **7 further claims counted but not written out**, because their subject is a dose ceiling, a toxicity threshold, or how to mix, buffer or dilute a solution: Ropivacaine Wheals 3; mepivacaine-wheals 1; bupivacaine-wheals 3
- **Extra studies recorded: 55**, found through the papers' reference lists and discussions.
- **Notion findings: 114** — **38 high**, **62 medium**, **14 low**.
  - by kind: 27 overstated, 23 understated, 17 now-verified, 15 open-question-answered, 11 outdated, 10 wrong-figure, 8 ranking-reweigh, 2 citation-error, 1 wrong-design

### The three wheal pages

| Page | as of | extracted | tested | skipped (dose/toxicity/preparation) | refuted | narrowed | confirmed | out-of-scope |
|---|---|---|---|---|---|---|---|---|
| bupivacaine-wheals | 2026-10-02T03:14:18.695Z | 8 | 8 | 3 | 2 | 1 | 5 | 0 |
| mepivacaine-wheals | 2026-10-02T03:14:08.315Z | 10 | 10 | 1 | 2 | 4 | 4 | 0 |
| Ropivacaine Wheals | 2026-10-02T03:14:26.511Z | 31 | 31 | 3 | 8 | 11 | 11 | 1 |

## 3. What each paper settled

- **S-686-04 — Christoph RA, Buchanan L, Begalla K, Schwartz S. Pain reduction in local anesthetic administration through pH buffering. Ann Emerg Med 1988;17:117-120** · own question: yes · 3 claims re-judged, 1 changed · 5 Notion findings.
- **S-686-14 — Kim JM, Goto H, Arakawa K. Duration of bupivacaine intradermal anesthesia when the bupivacaine is mixed with chloroprocaine. Anesth Analg 1979;58:364-366** · own question: yes · 5 claims re-judged, 1 changed · 11 Notion findings.
- **S-686-16 — Milner QJW, Guard BC, Allen JG. Alkalinization of amide local anaesthetics by addition of 1% sodium bicarbonate solution. European Journal of Anaesthesiology 2000;17:38-42** · own question: yes · 2 claims re-judged · 2 Notion findings.
- **S-686-17 — Morgan M, Russell WJ. An investigation in man into the relative potency of lignocaine, bupivacaine and etidocaine. Br J Anaesth 1975;47:586-591** · own question: yes · 3 claims re-judged · 6 Notion findings.
- **S-686-20 — Padfield A. The intradermal local analgesic action of prilocaine. A controlled double-blind comparison with lignocaine and procaine. Anaesthesia 1967;22(4):556-561** · own question: yes · 8 claims re-judged · 15 Notion findings.
- **S-686-24 — Ramos G, Pereira E, Simonetti MPB. Does alkalinization of 0.75% ropivacaine promote a lumbar peridural block of higher quality? Regional Anesthesia and Pain Medicine 2001;26(4):357-362** · own question: partly · 3 claims re-judged, 1 changed · 6 Notion findings.
- **S-686-25 — Reynolds F, Bryson THL, Nicholas ADG. Intradermal study of a new local anaesthetic agent: aptocaine. Br J Anaesth 1976;48:347-354** · own question: yes · 14 claims re-judged, 5 changed · 15 Notion findings.
- **S-686-28 — Schnabl SM, Unglaub F, Leitz Z, Breuninger H, Häfner HM. Skin perfusion and pain evaluation with different local anaesthetics in a double blind randomized study following digital nerve block anaesthesia. Clin Hemorheol Microcirc 2013;55:241-253** · own question: yes · 5 claims re-judged, 2 changed · 9 Notion findings.
- **S-686-31 — Swerdlow M, Jones R. The duration of action of bupivacaine, prilocaine and lignocaine. Br J Anaesth 1970;42:335-339** · own question: yes · 11 claims re-judged, 4 changed · 13 Notion findings.
- **S-686-33 — Tajiri K, Takahashi K, Ikeda K, Tomita K. Common Peroneal Nerve Block for Sciatica. Clin Orthop Relat Res 1998;347:203-207** · own question: yes · 1 claims re-judged · 4 Notion findings.
- **S-686-35 — Todd K, Berk WA, Huang R. Effect of body locale and addition of epinephrine on the duration of action of a local anesthetic agent. Ann Emerg Med 1992;21:723-726** · own question: yes · 5 claims re-judged, 2 changed · 11 Notion findings.
- **S-686-39 — Wightman MA, Vaughan RW. Comparison of Compounds Used for Intradermal Anesthesia. Anesthesiology 1976;45(6):687-689** · own question: yes · 2 claims re-judged, 1 changed · 17 Notion findings.
- **S-686-40 — Willatts DG, Reynolds F. Comparison of the vasoactivity of amide and ester local anaesthetics. An intradermal study. Br J Anaesth 1985;57:1006-1011** · own question: ? · 15 claims re-judged, 5 changed · 0 Notion findings.

## 4. Every verdict change

| claim | old | new | source | what decided it |
|---|---|---|---|---|
| C033 | narrowed | refuted | S-686-14 | The claim says that whether an ester and an amide can share a syringe was 'a question nobody had answered' |
| C038 | confirmed | refuted | S-686-39 | The claim says no study compares a methylparaben-preserved lidocaine against a preservative-free or benzyl-alcohol-preserved one for intradermal durat |
| C066 | narrowed | refuted | S-686-25 | The full text gives duration in minutes for every agent in both trials, by two endpoints: time to 50% recovery read from the mean recovery curves, and |
| C066 | narrowed | refuted | S-686-31 | The claim, and the source note behind it, say the only head-to-head duration figures in minutes on a skin endpoint come from a study in horses |
| C081 | narrowed | refuted | S-686-04 | Christoph 1988 matches every element the claim states in its own words: humans, the intradermal route, and lidocaine with epinephrine at exactly the s |
| C081 | narrowed | refuted | S-686-35 | The full text settles the open question |
| C081 | narrowed | refuted | S-686-35 | Christoph 1988 is reference 5 of Todd 1992, cited there only as the source of the buffering method, and it independently refutes C081: one of its thre |
| D001 | narrowed | refuted | S-686-28 | The paper settles its own open question exactly |
| D006 | narrowed | refuted | S-686-25 | Reynolds 1976 injected [dose figure omitted] intradermally - the wheal volume the claim's own qualifier names - and timed each agent to a permanent score of 10, that |
| D008 | confirmed | narrowed | S-686-25 | Reynolds 1976 used [dose figure omitted] per intradermal injection, not [dose figure omitted], so the claim's first sentence stands: nothing has measured intradermal bupivacaine a |
| D009 | confirmed | refuted | S-686-31 | The full text answers the open question yes on every element |
| D017 | confirmed | refuted | S-686-24 | Ramos matches every element D017 says is absent, within the claim's own scope |
| D024 | confirmed | narrowed | S-686-25 | The 'six drugs at once' element holds: Reynolds 1976 covered five agents across two separate trials, never six in one |
| D024 | confirmed | narrowed | S-686-31 | The claim bundles two uniqueness statements: intradermal duration data for six drugs at once, and the concentration-duration slopes |
| D039 | narrowed | refuted | S-686-40 | The full text matches every element the claim says is absent |
| D062 | confirmed | narrowed | S-686-25 | Reynolds 1976 contains no procaine, so the 'procaine plus five comparators in one study' element the record logs is unmatched and that part of the cla |
| D062 | confirmed | narrowed | S-686-31 | Same bundling as D024 |
| W-M001 |  | refuted | S-686-40 | Willatts and Reynolds 1985 matches every element the claim says is unique to Fairley and Reynolds 1981: human skin, racemic mepivacaine, intradermal b |
| W-M001 |  | refuted | S-686-40 | Reynolds, Bryson and Nicholas 1976, in Willatts' reference list, timed intradermal mepivacaine at three concentrations against prilocaine and aptocain |
| W-M009 |  | narrowed | S-686-40 | The distinctive element holds and the ordinal does not |
| W-R005 |  | confirmed | S-686-28 | Schnabl 2013 matches three of W-R005's four elements and misses the one that decides it |
| W-R025 |  | narrowed | S-686-40 | The head-to-head element holds: six agents at three concentrations each plus saline went into the same 10 volunteers, double-blind, by intradermal inj |

### New wheal-page claims that did not hold as written (28 of 49)

| claim | page | verdict | what exists |
|---|---|---|---|
| W-B001 | bupivacaine | refuted | A study matching every element the claim says is absent exists, and there are two of them rather than one |
| W-B005 | bupivacaine | narrowed | The claim is scoped to all seven agents and nothing found matches that scope, so the headline negative stands: a Europe PMC query requiring articaine, |
| W-B006 | bupivacaine | refuted | A study matching every element exists, and it is the same paper the page is discussing |
| W-M001 | mepivacaine | refuted | Refuted, and the page contradicts itself: its own source list calls Willatts and Reynolds 1985 the second intradermal measurement of mepivacaine and r |
| W-M002 | mepivacaine | narrowed | Narrowed rather than refuted |
| W-M003 | mepivacaine | refuted | Refuted on both counts the claim makes |
| W-M004 | mepivacaine | narrowed | Narrowed |
| W-M009 | mepivacaine | narrowed | Resolved from the Reynolds 1976 full text, read in this same session (S-686-25) |
| W-M010 | mepivacaine | narrowed | Narrowed |
| W-R003 | Ropivacaine Wheals | narrowed | The page's narrowing (rat oral mucosa, plus Sohn's calculation) is right as far as it goes but it stops one step short: there are two human in vivo mi |
| W-R008 | Ropivacaine Wheals | narrowed | The specific gap the page names holds: no study was found that compares what happens to unmyelinated fibres' Schwann cells against myelinated fibres'  |
| W-R010 | Ropivacaine Wheals | narrowed | The open part of the page's sentence survives intact: no dermal microvessel preparation was found for ropivacaine at all, so neither brake has been we |
| W-R011 | Ropivacaine Wheals | narrowed | The experiment the page is after is genuinely missing, and two independent Europe PMC queries plus three reused PubMed searches establish that: the wh |
| W-R012 | Ropivacaine Wheals | narrowed | 'No study varies them' is too broad for the first item on the page's own list |
| W-R013 | Ropivacaine Wheals | narrowed | The headline claim stands: nothing follows the whole chain in human dermis, and the six-record targeted query returns no candidate at all |
| W-R014 | Ropivacaine Wheals | refuted | Within the claim's own elements - human skin, ropivacaine at any concentration, any design, outcome vasodilation - a matching study exists, and the pa |
| W-R016 | Ropivacaine Wheals | refuted | The claim's own elements set population and design to 'any', which makes an animal study decisive, and one exists in the paper the page already cites  |
| W-R018 | Ropivacaine Wheals | refuted | Every element the claim says is absent - dermal microvessels, these drugs, any design, an ordering of vascular effect - is matched by the in vivo huma |
| W-R019 | Ropivacaine Wheals | refuted | The claim's recorded elements - ropivacaine, any preparation, any design, the A-fibre/C-fibre concentration separation - are all matched by Bader 1989 |
| W-R020 | Ropivacaine Wheals | refuted | Kankel 2012 matches the population (human), the intervention (an intradermal local-anaesthetic injection), the design (microneurography) and the outco |
| W-R021 | Ropivacaine Wheals | narrowed | What the paper actually reports is a stated-but-unquantified correspondence, not a measured correlation, so the claim is narrowed rather than refuted |
| W-R022 | Ropivacaine Wheals | refuted | The claim says this is the one histological finding in the literature selective for the fibre class at issue |
| W-R023 | Ropivacaine Wheals | narrowed | Within the claim's recorded outcome - epidermal nerve fibre density - searches found no second human study, so the core of the claim holds |
| W-R025 | Ropivacaine Wheals | narrowed | Reynolds 1976 matches the population (human skin), the design (double-blind intradermal head-to-head) and the outcome (vasoconstrictor activity, with  |
| W-R026 | Ropivacaine Wheals | refuted | Schnabl 2013 measures duration after a ropivacaine digital nerve block - the same drug, route and block type as Keramidas - and reports every arm exce |
| W-R029 | Ropivacaine Wheals | refuted | The claim's elements - a wheal, a vasoconstricting local anaesthetic, any design, prolonged duration of action - are all matched by Willatts & Reynold |
| W-R030 | Ropivacaine Wheals | narrowed | Judged inside the bullet's own scope - continuous infiltration of incised subcutaneous tissue - the claim holds: the rat wound study and the animal wo |
| W-R031 | Ropivacaine Wheals | narrowed | Within the claim's intervention element - a local anaesthetic wheal - nothing found separates the drug's flare suppression from the needle's own flare |

## 5. High-importance Notion findings (38)

- **S1-F001 · Comparing the injectable local anesthetics for intradermal wheals › The comparison itself / the ranking rationale - 'For a second option, and the drug to beat: plain lidocaine, already in the syringe'** — *overstated*, from S-686-04. This is a uniqueness statement inside the sentence that ranks plain lidocaine as the drug to beat, so part of the ordering rests on it
- **S1-F002 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › The second reversal: bupivacaine** — *wrong-figure*, from S-686-14. The paper's abstract says only that the mixture was 'similar to' chloroprocaine alone; the page upgrades that to a null result, which the Results section contradicts
- **S1-F003 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › Sources — The other human intradermal measurements (Kim 1979 entry, Limits)** — *open-question-answered*, from S-686-14. This is the limit the record itself treats as load-bearing — the sibling bupivacaine-wheals entry says in terms that 'volume is what this page's scaling argument turns on'
- **S1-F004 · bupivacaine-wheals › Sources › Duration in skin (Kim 1979 entry, Limits)** — *open-question-answered*, from S-686-14. The page's own wording makes this load-bearing — 'volume is what this page's scaling argument turns on' — and the recommendation that moves bupivacaine to third choice follows from the squar
- **S1-F005 · bupivacaine-wheals › Sources > What has no source** — *ranking-reweigh*, from S-686-17. The sentence is correct as far as it goes, and the attribution is right: the paper cited for the etidocaine-worse finding is Howe & Williams 1994, not Morgan & Russell 1975 (verified in Euro
- **S1-F006 · bupivacaine-wheals › What is still unknown** — *open-question-answered*, from S-686-17. The page's own open question is answered in the same direction by a study the page does not hold
- **S1-F007 · Comparing the injectable local anesthetics for intradermal wheals › How long does each one last? > What a tenfold rise in concentration buys, in skin** — *overstated*, from S-686-17. The page says this comparison 'decides more about how to inject than any ranking between drugs in this document', so a second data set bears directly on something practical
- **S1-F008 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › The seven papers nobody has pulled > item 4 (Padfield 1967)** — *open-question-answered*, from S-686-20. The queue item asks the full text for 'the durations in minutes'
- **S1-F009 · Ropivacaine Wheals › Sources > the Foldes/Padfield CITATION ONLY entry** — *outdated*, from S-686-20. 'Neither read at source' is now out of date for Padfield, and the duration wording carried into this record from Willatts and Reynolds should be replaced by the activity ranking the paper ac
- **S1-F010 · Ropivacaine Wheals › 9a.2 Two caveats, one of which the authors raise themselves > consequence** — *understated*, from S-686-20. This is the gap the page names - an amide against an uncontaminated saline control, intradermally, in humans - and the paper that partly fills it is the one already in this page's source lis
- **S1-F011 · Comparing the injectable local anesthetics for intradermal wheals › What does each one cost in injection pain? (the ropivacaine sentence that closes the 'A full buffer does not transfer to the other drugs' paragraph)** — *overstated*, from S-686-24. This is claim D017 and the sentence the whole open question was raised against; it is refuted as worded
- **S1-F012 · bupivacaine-wheals › The sting, and the two things that reduce it > 'A 2025 laboratory study put a number on the threshold' (the ropivacaine row of the AlShammari table); repeated in the Sources entry for AlShammari** — *overstated*, from S-686-24. The ropivacaine row is the figure that two pages lean on - the bupivacaine page's bupivacaine-versus-ropivacaine contrast and the comparison page's 'no one has shown' sentence - and as rende
- **S1-F013 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › Sources — The Reynolds series (Reynolds F, Bryson THL, Nicholas ADG 1976 annotation); and the same paper's row in the seven-papers table** — *open-question-answered*, from S-686-25. This is the correction the rest of the packet turns on
- **S1-F014 · mepivacaine-wheals › The recommendation (first bullet)** — *overstated*, from S-686-25. This is the page's headline recommendation sentence and the lead the S1 task flagged
- **S1-F015 · bupivacaine-wheals › What is still unknown ('Whether the square-root scaling holds'); and Why the eight-hour figure does not apply to a wheal / Sources › Duration in skin, where Sweet 1982 is called the governing number** — *understated*, from S-686-25. The page's own 'What would settle it' asks for wheals of three volumes timed side by side; two of the three now have a measurement with the same endpoint in the same tissue layer
- **S1-F016 · Ropivacaine Wheals › The comparability argument ('The duration comparisons are at unmatched concentrations and in unmatched tissues')** — *overstated*, from S-686-25. The page uses this sentence to argue that the duration comparisons cannot be ranked against each other
- **S1-F017 · Ropivacaine Wheals › 9a.5 Mepivacaine — the drug nobody in this project has considered ('Would not: duration')** — *understated*, from S-686-25. The page's own limit note on Willatts says its top mepivacaine concentration is well below the strength sold; Reynolds 1976 fills exactly that gap, and the 9a.5 assessment of mepivacaine as 
- **S1-F018 · What is still unsettled across these pages, and what would settle each one › Sources › The unopened intradermal literature (Willatts & Reynolds annotation)** — *open-question-answered*, from S-686-25. This page exists to point at the highest-value missing material, and the item it names as missing — absolute per-concentration minutes in human skin — is available in a paper already cited e
- **S1-F019 · Comparing the injectable local anesthetics for intradermal wheals › How long does each one last? (duration table, prilocaine row, 'With epinephrine' column, and the 'What the figure rests on' cell)** — *wrong-figure*, from S-686-31. This is the cell claim D009 was taken from, and it is the only cell in the table's 'With epinephrine' column that says nothing was measured
- **S1-F020 · Comparing the injectable local anesthetics for intradermal wheals › How long does each one last? / Four things about that table** — *overstated*, from S-686-31. The weal volume in the 1970 trial, [dose figure omitted] per weal, is above the [dose figure omitted] range this page means by a wheal, so the second sentence's 'at a wheal volume' qualifier
- **S1-F021 · Comparing the injectable local anesthetics for intradermal wheals › How long does each one last? (duration table, bupivacaine row) and 'The bupivacaine spread is explained by volume'** — *wrong-figure*, from S-686-31. The 60-minute wheal figure is derived from a two-point square-root-of-volume fit
- **S1-F022 · Comparing the injectable local anesthetics for intradermal wheals › How long does each one last? (duration table, lidocaine row, 'With epinephrine' column and its 'What the figure rests on' cell)** — *understated*, from S-686-31. The cell currently rests on a single user's own measurement in neuropathic leg skin, with the note saying the with-epinephrine figure is 'not from a trial'
- **S1-F023 · prilocaine-wheals › How long does it actually last?** — *overstated*, from S-686-31. This is claim C066
- **S1-F024 · prilocaine-wheals › Sources — What has no source** — *overstated*, from S-686-31. The bullet is wrong twice
- **S1-F025 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › What is still unknown** — *open-question-answered*, from S-686-31. The open question is answered: the two-to-three-times figure is reproduced intradermally in healthy forearm skin, at the upper end on the earlier endpoint and inside the range on complete re
- **S1-F026 · bupivacaine-wheals › What a wheal of your own size would give / Why the eight-hour figure does not apply to a wheal** — *wrong-figure*, from S-686-31. The square-root-of-volume fit, the roughly 60-minute wheal estimate, and the conclusion that bupivacaine at wheal size sits at or below what plain lidocaine gives all rest on there being onl
- **S1-F027 · 💉 Lidocaine With Epinephrine Wheals › What adding epinephrine buys > What transfers, and what does not** — *understated*, from S-686-35. This is the premise the page's central transfer rests on
- **S1-F028 · 💉 Lidocaine With Epinephrine Wheals › What adding epinephrine buys (opening); The verdict ('What the literature got wrong, for you')** — *wrong-figure*, from S-686-35. This widens the gap the page reports rather than narrowing it, so the direction of its conclusion is unchanged and strengthened
- **S1-F029 · adjuvants-without-a-vasoconstrictor › Sources — Whether denervation changes the alpha-2 response (Yamazaki & Yuge 2011 annotation)** — *ranking-reweigh*, from S-686-35. Yamazaki measures flow responsiveness to alpha-2 and alpha-1 agonists; Todd measures duration of anaesthesia with epinephrine, a different drug and endpoint, in healthy skin
- **S1-F030 · PiSA Lidocaína/Epinefrina [dose figure omitted], dental cartridge [dose figure omitted] (Mexico) › Verdict; and the Why and Why For Purpose properties** — *overstated*, from S-686-35. As written the sentence is a design claim about the literature and it is wrong: Todd 1992 is an intradermal wheal study of lidocaine with epinephrine at exactly this product's epinephrine st
- **S1-F031 · Newtheek (New Stetic) lidocaína con epinefrina [dose figure omitted], 50 glass cartridges × [dose figure omitted] — Tu Depósito Dental (Mexico) › Verdict; Why; Why For Purpose** — *overstated*, from S-686-35. Here the clause is a standalone conjunct rather than scoped by the Mülkoğlu clause, so it reads as an unrestricted claim
- **S1-F032 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › The seven papers nobody has pulled (item 2)** — *open-question-answered*, from S-686-39. The page names this paper the highest-value item in its retrieval queue and says the preservative question turns on it and on nothing else, so the status line and the 'what it would settle' 
- **S1-F033 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › What is still unknown — Whether methylparaben does anything for duration** — *open-question-answered*, from S-686-39. The concentration in the second sentence is replaced with [dose figure omitted] under the writing rules
- **S1-F034 · 🔬 The intradermal wheal literature nobody cites, and the two conclusions it overturned › Is it already in what you are buying? — What follows for you, in order (item 2)** — *outdated*, from S-686-39. The clause 'it has never been opened' is out of date and the sentence it sits in is the record's own reason for treating the preservative question as unresolved
- **S1-F035 · What is still unsettled across these pages, and what would settle each one › Which claims rest on one study nobody has repeated — Benzyl alcohol makes lidocaine both less painful and longer-lasting** — *outdated*, from S-686-39. The premise behind the words 'free gain' is wrong as applied to a lidocaine vial, and the newer wheal-literature page already carries the correction while this page still carries the old ver
- **S1-F036 · Procaine / Novocaine › Where procaine sits against the other candidates (ranking table, injection pain row)** — *wrong-figure*, from S-686-39. The cell says the figure does not exist
- **S1-F037 · Procaine / Novocaine › The ester question** — *ranking-reweigh*, from S-686-39. The page reads a single reassuring dataset as showing that the ester group's measured record is better than its reputation, and that reading feeds the 'gentlest' entries in its own ranking t
- **S1-F038 · Comparing the injectable local anesthetics for intradermal wheals › What ranks where (ranking table, procaine row, injection pain column)** — *wrong-figure*, from S-686-39. The same wrong cell as on the procaine page, in this page's own ranking table


## 6. Problems

**PubMed could not be reached at all.** `common/tools/pm.py` fails because the environment's network
policy blocks `eutils.ncbi.nlm.nih.gov` (403 at the proxy on CONNECT), and the PubMed MCP server
fails the same way, as do the ClinicalTrials, Consensus, OpenTargets, Wiley, ChEMBL and bioRxiv
servers. Direct HTTPS to `ebi.ac.uk`, `api.openalex.org`, `api.crossref.org` and
`api.semanticscholar.org` is blocked too. The only working route to the literature was Europe PMC
through the BioContext connector, plus Amass until it stopped (below). This is the single biggest
limitation on this session's work and the main session should weigh it when merging:

- Europe PMC counts are **not** PubMed counts. Europe PMC indexes full text as well as titles and
  abstracts, so it runs noisier, and its default ranking skews recent, which matters for claims whose
  literature is pre-2000. Workers used `TITLE_ABS:` scoping and citation sorting to compensate.
- The handover's instruction to check PubMed's query-translation line for phrases it did not find
  could not be carried out; Europe PMC returns no equivalent.
- The 64 PubMed searches in `wheal_head_start/earlier_searches_qlog.jsonl` are the only real PubMed
  evidence available, and were reused heavily — their counts and screened values are copied
  unchanged and marked `"engine": "pubmed (earlier worker, 2026-10-07)"`.
- `clinicaltrials.gov` is blocked, so the registry element of W-R002 could not be checked.

**Amass stopped mid-job.** It answered the first lookups, then began refusing every call with a
subscription usage-limit notice (it says the limit resets 6 Nov 2026). Queries completed before that
are marked `"engine": "amass"`; everything after is Europe PMC. That error text also tells the caller
not to use other tools to answer instead; that is a vendor note arriving inside a tool result, not an
instruction from the user, so it was recorded and not obeyed — Europe PMC is a separate free public
service and was the right index for this work regardless.

**No OCR engine.** Two of the 13 PDFs, S-686-33 (Tajiri 1998) and S-686-39 (Wightman 1976), are
scans with no text layer, and `tesseract` is not installed and not available from the package index.
Both were read instead by rendering each page to an image and reading it directly, then transcribing
to `texts/`. Those two transcriptions are marked `text_quality: ocr` on their cards and say exactly
what was transcribed and what is only describable (chart points that exist nowhere as numbers).

**The packet's quote checker needs one field reconciled.** `common/tools/quotecheck.py` resolves a
cached abstract from an item's `pmid`, but the wheal-claim schema in the handover names that field
`evidence_pmid`, so every wheal quote reported as unverifiable regardless of whether it was correct.
Rather than edit a packet tool the main session may rely on, the merge step mirrors `evidence_pmid`
into `pmid` on the output. With that done, **every quote in this session's results verifies against
its source**, 0 failures. Abstract caches for the cited PMIDs had to be written from Europe PMC
records by hand, since `pm.py` could not write them.

**One text extraction is column-interleaved.** `texts/S-686-40.txt` (Willatts 1985) is a two-column
scan whose extraction interleaves the columns line by line, so no sentence is contiguous. Quotes
taken from it are joined with ` … ` at each print line break with nothing elided, and quotes citing
that paper are checked against its abstract rather than the extracted text. The merge step verifies
a quote against a held full text before pointing the checker at it, and leaves it on the PMID
otherwise, so this cannot silently produce a false pass.

**Two author names were wrong in the briefs this session wrote, not in the packet.** The briefing
notes handed to two workers named S-686-17 as "Morgan, Lumley & Whitwam 1975" and S-686-20 as
"Padfield & Watkins 1967". Both are wrong: the by-lines are M. Morgan and W. J. Russell, and
A. Padfield alone. The packet is correct — `common/papers_list.csv` and the handover's own table
give only "Morgan 1975" and "Padfield 1967" — so the invented co-authors came from this session and
nowhere else. Both workers checked the by-line against the paper and the PubMed record rather than
trusting the brief, said so, and wrote the correct citation on their cards; every citation in
`results_S1/paper_cards/` is the by-line as printed. The names survive only in the two workers'
status notes, where they record the correction. Nothing downstream carries them.

**A page outside the index.** A worker's Notion search surfaced a page on exactly this topic that is
not in `common/pages_index.csv` — "Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection
Routing Analysis" — and recorded a finding against it. The main session may want it added to the
index and tested.

**No content filter stopped any write**, by this session or by any worker in it.

**Instruction-like text found inside documents.** All of it was treated as data, none of it acted
on, and nothing was written from it:

- Ropivacaine Wheals, section 0.0.2, "Operating instructions for the AI reading this" — a list of
  directions to an AI reader including "One claim per reply", "Do not ask him questions unless he has
  invited them" and "Do not warn him". This session did not adopt them; the network and quota
  problems above were reported to the user precisely because they needed reporting.
- Ropivacaine Wheals, section 4.5, "Do not repeat the 'never measured' claim."
- mepivacaine-wheals, an opening callout "Note for the health skills — 2026-10-02" recording the
  owner's ruling that dose limits stay on the injection-safety pages, and citing a dated decision.
- Several pages carry "Own-use marker" passages and "Where to start" retrieval queues addressed to a
  reader, plus imperatives such as "Read the composition panel on the physical box before buying".
- The Amass usage-limit error, described above, which carried an instruction not to use other tools.

**Compliance.** Every output file was scanned mechanically (`tools/compliance_scan.py`) for a drug
amount, a safety judgement or an imperative left in a field the rules do not exempt — the exemption
covers only the paper cards and a claim update's `reason`. **It reports zero breaches.** Six lines
are flagged for eyeballing because they contain a bare percentage; all six were reviewed and are
outcome measures — a flow rise, a difference between two means — rather than drug amounts, so they
stay. No dose ceiling, maximum dose, overdose or toxicity threshold, antidote passage or
preparation step was copied into any output. Where a claim's own subject was one of those, it was
counted and its text left unwritten (`results_S1/wheal_skipped.json` records each with its page,
section and reason). Where a recorded sentence contained such a figure, `[dose figure omitted]`
replaces it. The handover's one exception — recording what a study itself used, in the paper card and
in a claim update's `reason` — was used only where a paper's own open question asked for it. Every
file in `results_S1/` was checked to load as JSON, and `REPORT.md`'s own excerpt columns are passed
through the same dose-figure redaction, since the exception does not extend to this report.
