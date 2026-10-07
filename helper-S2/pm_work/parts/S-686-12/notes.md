# S-686-12 Hopman 2017 — working notes

## 1. Right-paper check
- PDF: `papers/S-686-12 - Hopman 2017 - Articaine and neurotoxicity - a review.pdf`, 6 pages, A4, created 2 Oct 2017 (InDesign).
- Title on PDF page 1: "Articaine and neurotoxicity – a review"; authors A. J. G. Hopman, J. A. Baart and H. S. Brand
  (ACTA / VU Medical Centre, Amsterdam); "Refereed Paper. Accepted 31 July 2017"; "DOI: 10.1038/sj.bdj.2017.782".
- Running footer: "BRITISH DENTAL JOURNAL | Advance Online Publication | OCTOBER 3 2017" — this is the advance-online
  version (pages 1–6), not the paginated print issue (Br Dent J 2017;223:501-506). Same article, same DOI; page numbers
  used everywhere are PDF pages 1–6.
- Matches papers_list.csv (PMID 28972589, DOI 10.1038/sj.bdj.2017.782). Right paper: yes.
- Text quality: ok. Reading-order text checked against renders of PDF pages 1 and 5 (pdftoppm, 70 dpi) — identical.
  Table 1 (PDF page 3) read in the layout view. Fig. 1 (PRISMA flow, PDF page 2) is text in the extraction.
- No funding statement and no conflict-of-interest statement anywhere in the PDF (grep + visual check of pages 1 and 5);
  only an acknowledgement for linguistic correction (PDF page 5).

## 1b. Every "Hillerup" in the paper (grep -i hillerup over the whole text; three mentions, all = reference 21)
1. PDF page 3, Table 1 row: "2001–2007 | DNK | 78% | 41% | – | Data from the DMA, a Danish national database for
   prescription medication. Marketshare based on data DMA. | Hillerup et al., 2011" (+ subgroup row "Subgroup of patients
   examined by oral surgeon.").
2. PDF page 5 (Discussion): "Therefore, the overrepresentation of sensibility disorders for articaine might be related by
   the use of articaine by younger, less experienced dentists. This suggestion is rejected by Hillerup and colleagues.21
   In their investigation, 11 patients had damage to two branches of the trigeminal nerve. This is considered highly
   improbable as the result of mechanical damage done by an injection needle."
3. PDF page 6, reference 21: "Hillerup S, Jensen R H, Ersbøll B K. Trigeminal nerve injury associated with injection of
   local anaesthetics: needle lesion or neurotoxicity? J Am Dent Assoc 2011; 142: 531–539."
- Reference 21 is also cited without the name on PDF page 4 ("Another study in Denmark used data from the Danish Medicines
  Agency.21" and "...with a market share of 19.4%.21") and PDF page 5 ("while used in a concentration of 3% the opposite
  was found.21" — a prilocaine formulation figure, not quoted in results).
- No mention anywhere of: sciatic, electrophysiology, stereology, Anesth Analg 2011, Bakke, Larsen, Thomsen, Gerds.
  The only "Anesth Analg" reference is Malet 2015 (ref 29).
- 34 references in total; none is Hillerup, Bakke, Larsen, Thomsen & Gerds 2011.

