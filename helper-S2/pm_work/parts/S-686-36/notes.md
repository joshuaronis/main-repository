# Working notes — S-686-36 (Wang CF et al. 2008, bulleyaconitine A as an adjuvant for prolonged cutaneous analgesia in the rat)

## 1. Right-paper check

`texts/S-686-36.txt`, 9 PDF pages, extracted from
`papers/S-686-36 - Wang 2008 - Use of bulleyaconitine A as an adjuvant for prolonged cutaneous analgesia in the rat.pdf`.

- Title on PDF page 1: "Use of Bulleyaconitine A as an Adjuvant for Prolonged Cutaneous Analgesia in the Rat".
- Authors: Chi-Fei Wang, Peter Gerner, Birgitta Schmidt, Zhen Zhong Xu, Carla Nau, Sho-Ya Wang, Ru-Rong Ji, Ging Kuo Wang.
- Journal line: "(Anesth Analg 2008;107:1397–1405)"; DOI printed on page 1: `10.1213/ane.0b013e318182401b`. Matches PMID 18806059 / the DOI in `papers_list.csv`.
- Text quality: ok and complete (abstract, methods, results, discussion, references, and an unrelated erratum notice on PDF page 9). Symbols are rendered as odd glyphs by the extraction (plus, micro, plus-or-minus, less-than, equals). Every quote in the results files was pulled out of the text file programmatically by a normalised search, so the glyphs match character for character.
- Figures were rendered and looked at (`pdftoppm -r 110/220`, PDF pages 4–7): Fig. 3 (CTMR time course, three arms), Fig. 4 (adjuvant concentration series), Fig. 5 (time to full recovery by solution), Fig. 6 (H&E micrograph with the layers labelled), Fig. 7 (PGP9.5 immunostaining, three rows A/B/C, **two columns only: SALINE and BLA**). Figure 7's two-column layout is the decisive observation for both own-question claims and is not stated in the running text.

## 2. The paper, read for the two questions

- Route: subcutaneous into shaved dorsal thoracolumbar skin, raising a circular wheal marked with ink; a smaller injection into paw skin for part of the immunohistochemistry. The paper calls the model "infiltration anesthesia"; the word "intradermal" never appears.
- Groups injected (CTMR): adjuvant alone; adjuvant + lidocaine; adjuvant + epinephrine; adjuvant + lidocaine + epinephrine at four adjuvant concentrations; and **lidocaine with epinephrine alone as the control solution**. Six rats per solution; observer blinded.
- Groups examined histologically (H&E, read by a pathologist who is a co-author): skin after the adjuvant + lidocaine + epinephrine mixture, against "the control sections". Layers covered, per the Fig. 6 legend: epidermis, dermis, muscle, subcutaneous layer. Timing: after full recovery, about 6 days after injection.
- Groups examined by PGP9.5 immunohistochemistry: **saline against the adjuvant + lidocaine + epinephrine mixture only**. No plain lidocaine-with-epinephrine arm was stained. Timing: about 24 h (one day) after a single injection. Sections coded blind.
- Quantitative? Yes, for paw skin: nerve fibres counted per optical field, 9 sections from 3 animals per group, ranges and means with a P value given; the difference was not significant. Back skin is shown but no count is given for it.
- Fibres counted are in the epidermis (the Fig. 7 legend says the arrows indicate nerve fibres in the epidermis); the images also show dermal fibres.
- So: the answer to both open questions is **no plain lidocaine/epinephrine arm was examined**, and what was examined was examined quantitatively.

## 3. Claim screen (all 320 claims in `common/claims_all.json`)

Screened the whole file programmatically over `claim`, `elements_said_absent`, `proposed_wording`, `reason`, `review`, `section`, `records_read` and `needs_full_text`, in two passes.

Pass 1 (too broad, 184 hits) combined: PGP9.5 / intraepidermal / epidermal nerve fibre / IENFD / nerve fibre density / skin innervation; histology / immunohistochemistry / skin biopsy / H&E; neurotoxic / nerve damage / nerve injury / nerve degeneration / myotoxic; rat / rodent / animal model; epinephrine / adrenaline / vasoconstrictor; adjuvant / prolonged / long-acting / sustained / liposomal / tetrodotoxin / saxitoxin / neosaxitoxin / sodium-channel blocker / capsaicin; cutaneous trunci / CTMR / wheal; Wang GK / Ging Kuo / Gerner / Ru-Rong / Ji RR / bulleyaconitine / aconitine / Khodorova / Strichartz / Khan MA / Simone DA; PMID 18806059; duration of cutaneous analgesia.

Pass 2 (the one used) required a combination and produced 184 → the tagged list below:
- `A_la+skin` = a local-anaesthetic term AND a skin/route term
- `B_pgp` = PGP9.5 / intraepidermal nerve / epidermal nerve fibre / IENFD / skin or cutaneous innervation
- `C_authors` = this paper's authors, drug, or PMID
- `D_ctmr` = cutaneous trunci / CTMR
- `E_adjuv` = adjuvant / liposomal / tetrodotoxin / saxitoxin / prolonged anaesthesia / long-acting / sustained-release
- `F_neurotox_skin` = a neurotoxicity/nerve-damage term AND a skin term

Separate greps: PMID `18806059`, `bulleyaconitine`, `Wang 2008`, `Wang GK`, `Gerner` → **C046 and D013 only**. `cutaneous trunci`/`CTMR` → **C021 only** (and there it is in a records_read entry about dexmedetomidine in rat skin, not about this paper). "rat" + "cutaneous analgesia" → C013, C021, C023, C024, C026, C030, C034, C035, C038, C046, C048, D013, E028.

### Claims read closely, and why kept or dropped

| Claim | Read because | Kept / dropped |
|---|---|---|
| C046 | own question | **kept** — own-question entry |
| D013 | own question | **kept** — own-question entry |
| C075 | nerve-fibre counting / nerve histology after repeated infiltration with epinephrine, any species | **kept** — other-claim; the paper is a single injection, so the claim survives |
| D015 | repeated injection over months into fibre-depleted skin | **kept** — other-claim; single injection into intact rat skin, so the claim survives |
| C076 | "the only objective measure of nerve loss in skin is IENFD" | dropped — scoped to **human skin**; this paper is rat, so it cannot bear. Already refuted by the main session |
| D014 | "the one human measurement is of a patch" | dropped — scoped to **humans**; a rat study cannot narrow a human-scoped uniqueness claim. Noted for Notion instead |
| D061 | intraepidermal fibre density after procaine | dropped — drug-specific to procaine; this paper used lidocaine |
| C013–C016, C020–C027, C030 (adjuvants page) | adjuvant claims | dropped — all scoped to humans, or to clonidine / dexamethasone / dexmedetomidine / magnesium / buprenorphine by name, or to small fibre neuropathy. The paper is a rat study of an experimental alkaloid |
| C031–C045, C047 (wheal-literature page) | same page as C046 | dropped — all scoped to human intradermal wheal measurements; C043 ("no sustained-release local anesthetic has come close in human skin") is human-scoped too |
| C072–C089, C094 (lidocaine-with-epinephrine page) | epinephrine in skin | dropped — blood flow, tissue oxygen, drug levels, fibre-class electrophysiology, dilution and duration claims, all either human-scoped or about outcomes this paper did not measure |
| C082 | A-delta vs C fibres with epinephrine, rodent | dropped — ex vivo nerve electrophysiology by fibre class; this paper measured a reflex and fibre counts, not fibre-class activity |
| C084, C085 | epinephrine alone vs with anaesthetic in skin | dropped — outcome is tissue oxygen or blood flow, neither measured here |
| D000–D012, D016–D025 (comparison page) | same page as D013 | dropped — human duration, injection pain, blood flow, buffering, or the dish-versus-spinal neurotoxicity question, none of which this paper addresses |
| D004 | damaged vs healthy nerve, animal | dropped — perineural injection into diabetic animals; this paper is intact skin, no neuropathy model |
| D045–D051 (injectables ruled out) | sustained-release / intradermal route | dropped — drug-specific (cinchocaine, tetracaine, chloroprocaine, liposomal bupivacaine) or SFN-scoped |
| D026, D031, D032, D039, D042, D043 | relief outlasting the block | dropped — human neuropathic pain, trial designs this paper has nothing to say about |
| E006, E008, E009, E021, E026, E028 | fibre counts under topical agents | dropped — topical route, human |
| A010, A038, A054, A000–A088 (`B_pgp` hits) | fibre-count outcomes | dropped — nerve-growth and systemic-drug claims in SFN; no overlap with an injected-anaesthetic rat study |
| C005, C008 | botulinum wheals, fibre loss | dropped — botulinum toxin, and the outcomes are pain response and contralateral spread |
| C049–C063 (articaine), C065–C071 (prilocaine), D053–D065 (procaine), D066 (prilocaine+lidocaine) | neurotoxicity / skin | dropped — each is specific to a drug this paper did not use |

### Claims not tested under the content-filter rule (dose or toxicity subject)

- 💉 Lidocaine With Epinephrine Wheals: 2 claims not tested: dose or toxicity subject.
- Safe Doses Of Intradermal Analgesics: 5 claims not tested: dose or toxicity subject.
- Injectables ruled out but not tried: 1 claim not tested: dose or toxicity subject.

Their text is not reproduced anywhere in these results.

## 4. PubMed (connector; `common/tools/pm.py` could not run — the session's network policy blocks eutils.ncbi.nlm.nih.gov)

No `search_articles` call was needed: every lookup was a reference-list resolution.

`lookup_article_by_citation`, one batch of 20 citations from the paper's reference list (journal + year + volume + first page + first author), all 20 resolved:

| Ref | Citation | PMID |
|---|---|---|
| 2 | Rao, Pflugers Arch 2000;439:349 | 10650987 |
| 3 | Wang, Anesthesiology 2007;107:82 | 17585219 |
| 4 | Wang, Cell Signal 2003;15:151 | 12464386 |
| 5 | Friese, Eur J Pharmacol 1997;337:165 | 9430411 |
| 6 | Ameri, Prog Neurobiol 1998;56:211 | 9760702 |
| 8 | Wood, J Neurobiol 2004;61:55 | 15362153 |
| 9 | Nassar, PNAS 2004;101:12706 | 15314237 |
| 10 | Jarvis, PNAS 2007;104:8520 | 17483457 |
| 12 | Leffler, J Pharmacol Exp Ther 2007;320:354 | 17005919 |
| 13 | Zhao, J Neurophysiol 2007;98:467 | 17507497 |
| 15 | Khan, Anesthesiology 2002;96:109 | 11753010 |
| 16 | Simone, J Neurosci 1998;18:8947 | 9787000 |
| 19 | Hille, J Gen Physiol 1977;69:497 | 300786 |
| 20 | Nau, Anesthesiology 2000;93:1022 | 11020758 |
| 21 | Nau, J Membr Biol 2004;201:1 | 15635807 |
| 22 | Clarkson, Anesthesiology 1985;62:396 | 2580463 |
| 24 | Khodorova, Anesth Analg 2000;91:410 | 10910859 |
| 25 | Cummins, J Neurosci 1998;18:9607 | 9822722 |
| 26 | Djouhri, J Physiol 2003;550:739 | 12794175 |
| 32 | Amir, J Pain 2006;7:S1 | 16632328 |

Note: the connector's result object swaps the `pmid` and `key` fields — the PMID arrives in `key`. The values above are the PMIDs.

Not resolvable in PubMed (not indexed there): ref 1 (Zhu, Drug Dev Res 1986), ref 30 (Wang & Strichartz, Drug Dev Res 2002), ref 33 (Priest & Hunter, Drug Dev Res 2006), refs 23, 29, 31 (book chapters). Ref 28 (McEvoy, J Clin Psychiatry 2006) was not looked up — it is cited only as a depot-release analogy.

`get_article_metadata` for the four studies that bear on the pages' topics, each saved to `pm_work/cache/` with `pmcache.py article` (verbatim, none redacted — none carries a ceiling, threshold or antidote passage): 17585219, 11753010, 9787000, 10910859.

## 5. Notion (read-only; `notion-search` and `notion-fetch` only)

Searches run:
1. `bulleyaconitine`, page_size 25 → 21 results, all unrelated (product rows and clonidine pages). The AI search does not do exact-phrase matching, so nothing was concluded from it; every page below was fetched and its text searched directly.
2. `nobody has measured damage in skin from an injected anesthetic nerve fibres`, page_size 25 → 17 results. Used only to surface candidate pages; the three it surfaced that were not already on my list (two Health Pages - Meta absence rows and the intradermal-vs-subcutaneous routing page) were then fetched.
3. `prolonged cutaneous analgesia rat subcutaneous injection sodium channel adjuvant skin histology PGP9.5`, page_size 20 → 15 results, nothing new.

Pages fetched (none reported `truncated`, `unknown_block_count` or `unknown_block_ids`):

| Page | URL | as of | Result |
|---|---|---|---|
| 🔬 The intradermal wheal literature nobody cites… | /p/3d410b7903aa8107a042d4e7f6540c1a | 2026-10-02T03:14:04.610Z | **finding F01**. Contains no "Wang", "bulleyaconitine", "PGP" or "18806059" |
| Comparing the injectable local anesthetics for intradermal wheals | /p/3c510b7903aa81208d4fe305e7cb069b | 2026-10-02T03:14:02.626Z | **findings F02, F03**. Contains no "Wang", "bulleyaconitine", "PGP" or "18806059" |
| 💉 Lidocaine With Epinephrine Wheals | /p/3c610b7903aa801c906fcde8b5c43674 | 2026-09-26T18:28:27.736Z | **finding F04** |
| bupivacaine-wheals | /p/3d310b7903aa81469517da5f7c05e37d | 2026-10-02T03:14:18.695Z | **finding F05** |
| mepivacaine-wheals | /p/3c510b7903aa8152b01bf10e2f980185 | 2026-10-02T03:14:08.315Z | **finding F06** |
| Ropivacaine Wheals | /p/2c010b7903aa83a0b9e3813036c9d26e | 2026-10-02T03:14:26.511Z | no finding — does not carry the sentence; no mention of this paper or its authors |
| Injectables ruled out but not tried | /p/3d310b7903aa81fca5adcc979f03c0d5 | 2026-10-02T03:14:22.080Z | no finding — its neurotoxicity material is dish and intrathecal rankings by drug, none of which this paper touches |
| adjuvants-without-a-vasoconstrictor | /p/3d310b7903aa81fbb5b9e999637c362a | 2026-10-02T03:14:20.685Z | no finding — its adjuvants are clonidine, dexamethasone, dexmedetomidine, magnesium, buprenorphine, and its absence claims are human-scoped |
| 2 — Reference (source register S1–S457) | /p/3d410b7903aa81a4ada4c3830a567c65 | 2026-10-01T02:05:48.095Z | no finding — searched for "bulleyaconitine", "18806059", "Gerner", "Khodorova", "Simone D", "cutaneous trunci", "Bouaziz", "Kroin": **zero hits for all**. The 19 "Wang" hits are other authors. The paper is not in the register |
| 1 — Product Guide | /p/3d410b7903aa81c0815ad3c7c6c2d17f | 2026-10-02T03:14:29.224Z | no finding — same terms, zero hits. Its one mention of injected anaesthetics is a combined-exposure passage whose subject is dose, left alone under the filter rule |
| 5 — Soft ground in these documents | /p/3d410b7903aa81e88fbdc2ab883b1403 | 2026-09-26T18:26:13.509Z | no finding — about source reliability in the topical corpus; this paper is not among its items |
| What is still unsettled across these pages… | /p/3d410b7903aa819f8300e976a62577db | 2026-09-26T18:23:10.973Z | no finding — its two relevant passages are correct as written (see below) |
| 🕳️ What was searched for and does not exist… | /p/3d410b7903aa8169b833f5997631cc82 | 2026-09-27T00:27:49.877Z | no finding — a register of topical-agent absences; nothing on injected-anaesthetic skin histology |
| Health Pages - Meta: "No study has measured nerve fibre density before and after repeated local anaesthetic injection into the same skin…" | /p/3da10b7903aa810ca133c1c2bf568f70 | 2026-09-24T03:30:17.774Z | no finding — the row is scoped to **repeated** injection and to before-and-after measurement, and stays true (see below) |
| Small Fiber Neuropathy — Intradermal vs. Subcutaneous Injection Routing Analysis | /p/39410b7903aa8046b3eef25af516245f | 2026-09-26T18:19:51.310Z | no finding — its absence statements are about drug concentration in epidermis versus dermis, puncture infection risk and homeopathic remedies |

### Verbatim sentences relied on

🔬 wheal-literature page, "Sources — What has no source":
> "**Any measurement of injected local anesthetic damage to nerve fibers in skin.** The irritancy findings here are bleeding and bruising scored by eye. Whether repeated wheals cost intraepidermal nerve fibers — the damage that would matter to skin already depleted of them — has never been measured for any local anesthetic. The one measurement of any local anesthetic's effect on those fibers is topical: [dose figure omitted] lidocaine patches worn for 42 days lowered epidermal nerve fiber density in healthy volunteers, where placebo patches did not (Wehrfritz 2011, PMID 21530339)."

Comparison page, "What does each one do to nerve tissue?":
> "**Nobody has measured damage in skin from an injected anesthetic.** The one human measurement is of a patch: [dose figure omitted] lidocaine patches worn for 42 days lowered epidermal nerve fiber density in healthy volunteers, where placebo patches did not (Wehrfritz et al., 2011)."

Comparison page, "What would settle what is unresolved":
> "**Does anesthetic damage skin the way it damages nerve roots, or the way it damages cells in a dish?** This is the question the whole harm comparison turns on, and no study of injection addresses it; the one measurement in human skin is of lidocaine patches worn for six weeks, which lowered epidermal nerve fiber density in healthy volunteers (Wehrfritz et al., 2011). What would settle it: a study of nerve-fiber density in skin after repeated injection of several anesthetics, in an animal or in people."

💉 Lidocaine With Epinephrine Wheals, "Whether the tissue shows damage afterwards":
> "Two studies looked for the injury itself rather than for its cause."

and, in "Gaps in the literature: nobody has measured this" (checked and correct, no finding):
> "A structured search confirms the gap is real rather than merely unfound: no study anywhere performs nerve fibre counting or peripheral nerve histology after repeated infiltration of local anesthetic with epinephrine into the same soft-tissue site over days or weeks. The reason is practical rather than scientific — histology needs the tissue cut out, which rules out the human version, so the field infers repeated-dose safety from single-exposure animal work."

bupivacaine-wheals:
> "**Neither of them is skin, and nobody has measured damage in skin from an injected anesthetic**; the one skin measurement is of lidocaine patches, which lowered epidermal nerve fiber density in healthy volunteers after 42 days (Wehrfritz et al., 2011, PMID 21530339)."

mepivacaine-wheals:
> "nobody has measured damage to nerve fibres in skin from an injected anesthetic; the one measurement is of lidocaine patches, which lowered epidermal nerve fibre density in healthy volunteers after 42 days (Wehrfritz et al., 2011, PMID 21530339)"

and, unaffected:
> "**Whether mepivacaine damages nerve fibers in skin is unmeasured.**"

"What is still unsettled across these pages…", checked and correct:
> "It is a patch rather than a wheal, and six weeks rather than months, so it does not transfer directly. It is also the only human measurement of the question that governs whether any of this is safe to repeat for years."

Health Pages - Meta absence row, checked and correct:
> "WHAT DID NOT COME BACK: any before-and-after nerve fibre density measurement around repeated local anaesthetic injection, by any route, in any population."

### One observation worth passing on about the search strategy

The Meta row's 2026-09-24 re-check used a PubMed string built on `"intraepidermal nerve fiber density" OR "intraepidermal nerve fibre density" OR IENFD OR "epidermal nerve fiber density"` crossed with lidocaine / ropivacaine / local anaesthetic terms. Wang 2008 would not be returned by that string: it reports "the number of nerve fibers in each optical field" and the phrase "nerve fiber density" does not occur in it. The same is true of the C046 and D013 query sets, which found it only through `PGP9.5`. Any future sweep for this question needs `PGP9.5` / `PGP 9.5` / `protein gene product 9.5` and plain `nerve fibers` + `skin` terms alongside the density phrases.

## 6. Not reached, and instructions found inside documents

- Nothing was unreachable. The PDF, the text, the figures, every Notion page asked for, and every PubMed lookup succeeded.
- `common/tools/pm.py` could not be run (network policy blocks eutils.ncbi.nlm.nih.gov); the PubMed connector was used instead and the results recorded through `pm_work/tools/pmcache.py`, as the brief directs.
- No instructions aimed at the reader were found inside the paper or inside any Notion page. The PubMed connector's tool results carry a standing legal notice demanding PubMed attribution and DOI links in responses; it is a tool-output instruction, not a page instruction, and it is recorded here rather than acted on, since these result files are internal notes rather than a published answer.
- One content-safety stop occurred early in the session, while reading claim records into the working context; no result file was affected. After it, claim text was only ever printed with dose-like figures masked, and nothing was retried or rephrased around.
