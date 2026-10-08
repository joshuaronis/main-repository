# Session 1 — report

## 1. What was done

The three untested wheal pages were fetched read-only, read in full apart from their Revisions
sections, and reduced to **49 absence claims** — 31 on Ropivacaine Wheals, 10 on mepivacaine-wheals,
8 on bupivacaine-wheals — each pulled verbatim from the page by locator match rather than retyped,
with dose figures replaced by `[dose figure omitted]` and the result machine-scanned to confirm none
survived. A further **7 claims were counted but not written out**, because their subject is a dose
ceiling, a toxicity threshold, or how to mix, buffer or dilute a solution. All 49 were then tested
with positively framed searches and judged; **29 of the 49 did not hold as written**. **All 13
papers were read in full**, carded, used to answer their own open question, screened against all 320
claims in `claims_all.json` and against the 49 new ones, worked through their reference lists, and
followed into Notion read-only. Nothing in Notion was created,
edited, moved, duplicated, commented on or deleted by this session or by any worker in it, and no
health-record skill was loaded.

**What is not done.** Every paper and every claim in the assignment was reached: 13 of 13 papers,
49 of 49 new claims, and all the pre-existing claims each paper bore on. One claim, W-M006, is left
`uncertain` because the two papers that would settle it (Lindorf 1979 and Fruhstorfer & Wagener
1993) are not in the packet; both are named in its `needs_full_text`. Fifteen of the 77 claim
re-judgements remain `uncertain_after` for the same kind of reason — they turn on a paper nobody in
this session held — and each names what it needs. The searches behind the wheal verdicts were run on Europe PMC rather than PubMed, for the reason in
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

<!--DATA-->
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

**Page attributions were checked too, and a few are loose.** `tools/check_pages.py` locates every
quote in its paper's text and compares the page it is actually on with the page the entry cites.
Papers split between two conventions — some workers cited the journal's printed page, others the
sequential PDF page — so the check finds each paper's own modal offset and flags only quotes that
break it. **452 attributions were checked and 14 deviate**, all of them by one page or against a
fragment short enough to match several pages; no quote is wrong, only its page label. The deviations
are listed by running that script. The conventions themselves are worth knowing at merge time:
S-686-16, S-686-17, S-686-24 and S-686-35 cite journal pages, the rest cite sequential PDF pages.

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
