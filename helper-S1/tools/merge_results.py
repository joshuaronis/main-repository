"""Merge the per-worker files in results_S1/parts/ into the hand-back files the handover asks for.

Workers write one file each so they never collide; this folds them together into
  results_S1/claim_updates.json
  results_S1/extra_studies.json
  results_S1/notion_findings.json
  results_S1/wheal_claims.json      (filled-in claims replace their placeholders)
  results_S1/papers_status.csv
and prints the counts REPORT.md needs.

Run from the helper-S1 directory:  python3 tools/merge_results.py
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict

R = "results_S1"
P = f"{R}/parts"


def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"  !! unreadable {path}: {e}", file=sys.stderr)
        return None


def merge_lists(pattern):
    out, seen_files = [], []
    for f in sorted(glob.glob(f"{P}/{pattern}")):
        d = load(f)
        if isinstance(d, list):
            out.extend(d)
            seen_files.append(os.path.basename(f))
        elif d is not None:
            out.append(d)
            seen_files.append(os.path.basename(f))
    return out, seen_files


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def quote_in_text(quote, path):
    """quotecheck.py's own matching: ignore spacing/case/punctuation, and treat
    an ellipsis or a [bracketed omission] as a split between parts."""
    try:
        body = norm(open(path, encoding="utf-8", errors="replace").read())
    except OSError:
        return False
    parts = [norm(x) for x in re.split(r"\.\.\.|\u2026|\[[^\]]*\]", quote or "")]
    parts = [x for x in parts if len(x) > 10]
    return bool(parts) and all(x in body for x in parts)


def pmid_to_paper():
    """So a quote cited by PMID is checked against a full text we actually hold."""
    m = {}
    for row in csv.DictReader(open("common/papers_list.csv", encoding="utf-8")):
        pid, pm = row.get("paper_id", "").strip(), (row.get("pmid") or "").strip()
        if pid and pm and os.path.exists(f"texts/{pid}.txt"):
            m[pm] = pid
    return m


def main():
    # ---- claim updates -------------------------------------------------
    updates, files = merge_lists("*_claim_updates.json")
    p2p = pmid_to_paper()
    repointed = skipped_repoint = 0
    for u in updates:
        # If the deciding source is a paper whose full text we hold, point the
        # checker at that text -- but only when the quote actually matches it.
        # texts/S-686-40.txt is an OCR of a two-column scan whose columns
        # interleave, so quotes from it verify against the abstract and not
        # against the extracted text; those stay on the PMID.
        if not u.get("paper_id") and u.get("pmid") in p2p:
            cand = p2p[u["pmid"]]
            if quote_in_text(u.get("quote"), f"texts/{cand}.txt"):
                u["paper_id"] = cand
                repointed += 1
            else:
                skipped_repoint += 1
    json.dump(updates, open(f"{R}/claim_updates.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(f"  quote source      {repointed} re-pointed to a held full text, "
          f"{skipped_repoint} left on the PMID (quote does not match the extracted text)")

    # ---- reconcile the claims several workers judged ---------------------
    # Each worker judges a claim against its OWN paper only, so "confirmed" from
    # one worker means "my paper does not refute this", not "nothing refutes it".
    # The merged verdict is therefore the strongest finding across workers:
    # refuted > narrowed > confirmed. out-of-scope is a different axis and only
    # wins when it is the only verdict offered.
    RANK = {"refuted": 3, "narrowed": 2, "confirmed": 1, "out-of-scope": 0}
    groups = defaultdict(list)
    for u in updates:
        groups[u.get("claim_id")].append(u)

    recon, verdicts = [], []
    for cid, us in sorted(groups.items()):
        scored = sorted(
            us,
            key=lambda u: (RANK.get(u.get("new_verdict"), -1),
                           0 if u.get("uncertain_after") else 1,
                           len((u.get("proposed_wording") or "").strip())),
            reverse=True)
        win = scored[0]
        merged = win.get("new_verdict")
        # settled if any worker reaching the merged verdict settled it
        unc = not any(not u.get("uncertain_after")
                      for u in us if u.get("new_verdict") == merged)
        for u in us:
            u["merged_verdict"] = merged
            u["is_merged_source"] = (u is win)
        offered = sorted({u.get("new_verdict") for u in us})
        if len(us) > 1:
            recon.append({
                "claim_id": cid,
                "entries": len(us),
                "verdicts_offered": {u.get("paper_id") or u.get("pmid") or "?":
                                     u.get("new_verdict") for u in us},
                "merged_verdict": merged,
                "merged_from": win.get("paper_id") or win.get("pmid"),
                "uncertain_after_merge": unc,
                "conflict": len(offered) > 1,
                "rule": ("strongest finding wins: each worker judged only against its own paper, "
                         "so a weaker verdict means that paper did not settle it"),
            })
        verdicts.append({
            "claim_id": cid,
            "old_verdict": win.get("old_verdict"),
            "merged_verdict": merged,
            "uncertain_after": unc,
            "decided_by": win.get("paper_id") or win.get("pmid"),
            "papers_that_judged_it": [u.get("paper_id") or u.get("pmid") for u in us],
            "proposed_wording": win.get("proposed_wording"),
            "reason": win.get("reason"),
        })
    json.dump(recon, open(f"{R}/reconciliations.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    json.dump(verdicts, open(f"{R}/claim_verdicts.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    nconf = sum(1 for r in recon if r["conflict"])
    print(f"  reconciled        {len(recon)} claims judged by more than one paper, "
          f"{nconf} with differing verdicts -> results_S1/reconciliations.json")

    # ---- extra studies -------------------------------------------------
    extras, _ = merge_lists("*_extra_studies.json")
    byp = {}
    for e in extras:                     # one row per PMID, merging claim lists
        k = e.get("pmid") or e.get("citation", "")[:60]
        if k in byp:
            a = byp[k]
            a["bears_on_claim_ids"] = sorted(set(a.get("bears_on_claim_ids", []))
                                             | set(e.get("bears_on_claim_ids", [])))
            if e.get("found_in_paper") not in (a.get("found_in_paper") or ""):
                a["found_in_paper"] = f"{a.get('found_in_paper')}; {e.get('found_in_paper')}"
        else:
            byp[k] = dict(e)
    extras = list(byp.values())
    json.dump(extras, open(f"{R}/extra_studies.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    # ---- notion findings, renumbered S1-Fnnn ---------------------------
    findings, _ = merge_lists("*_notion_findings.json")
    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get((f.get("importance") or "").lower(), 3),
                                 f.get("paper_id", ""), f.get("finding_id", "")))
    for i, f in enumerate(findings, 1):
        f["worker_finding_id"] = f.get("finding_id", "")
        f["finding_id"] = f"S1-F{i:03d}"
    json.dump(findings, open(f"{R}/notion_findings.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    # ---- wheal claims: filled-in versions replace the placeholders ------
    claims = {c["claim_id"]: c for c in load(f"{R}/wheal_claims.json")}
    filled = 0
    for f in sorted(glob.glob(f"{P}/wheal_*.json")):
        d = load(f)
        for c in d or []:
            if c.get("claim_id") in claims and c.get("verdict"):
                claims[c["claim_id"]] = c
                filled += 1
    # The handover's wheal schema names the field evidence_pmid, but
    # common/tools/quotecheck.py resolves a cached abstract from "pmid".
    # Mirror it rather than editing the packet's tool, so the provided checker
    # validates these quotes as-is.
    for c in claims.values():
        if c.get("evidence_pmid") and not c.get("pmid"):
            c["pmid"] = c["evidence_pmid"]
    # some workers wrote needs_full_text as bare strings; coerce to the schema's objects
    pm = re.compile(r"\b(?:PMID\s*)?(\d{7,8})\b")
    for c in claims.values():
        nf = c.get("needs_full_text") or []
        fixed = []
        for x in nf:
            if isinstance(x, str):
                m = pm.search(x)
                fixed.append({"pmid": m.group(1) if m else "", "doi": "", "question": x})
            elif isinstance(x, dict):
                fixed.append({"pmid": str(x.get("pmid") or ""), "doi": x.get("doi") or "",
                              "question": x.get("question") or ""})
        c["needs_full_text"] = fixed
    ordered = sorted(claims.values(), key=lambda c: c["claim_id"])
    json.dump(ordered, open(f"{R}/wheal_claims.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    # ---- wheal summary --------------------------------------------------
    skipped = load(f"{R}/wheal_skipped.json") or {}
    pages = {}
    for c in ordered:
        p = pages.setdefault(c["page"], {"page": c["page"], "url": c["page_url"],
                                         "as_of": c["page_version"], "tested": 0,
                                         "verdicts": Counter(), "uncertain": 0,
                                         "not_yet_tested": 0})
        p["tested"] += 1
        if c.get("verdict"):
            p["verdicts"][c["verdict"]] += 1
            if c.get("uncertain"):
                p["uncertain"] += 1
        else:
            p["not_yet_tested"] += 1
    summary = []
    for p in pages.values():
        summary.append({
            "page": p["page"], "url": p["url"], "as_of": p["as_of"],
            "fetched": "2026-10-08 (read-only)",
            "claims_tested": p["tested"] - p["not_yet_tested"],
            "claims_extracted": p["tested"],
            "claims_not_yet_tested": p["not_yet_tested"],
            "claims_skipped_dose_or_toxicity_subject": len(skipped.get(p["page"], [])),
            "skipped_detail": skipped.get(p["page"], []),
            "verdicts": dict(p["verdicts"]),
            "uncertain": p["uncertain"]})
    json.dump(summary, open(f"{R}/wheal_summary.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    # ---- papers_status.csv ---------------------------------------------
    cols = ["paper_id", "right_paper", "text_ok", "own_question_answered",
            "claims_rejudged", "notion_findings", "notes"]
    rows, byid = [], {}
    for f in sorted(glob.glob(f"{P}/*_status.json")):
        d = load(f)
        if isinstance(d, dict):
            r = {c: d.get(c, "") for c in cols}
            rows.append(r)
            byid[r["paper_id"]] = r
    # a *_status2.json records a second pass over a paper whose earlier steps were
    # done elsewhere (steps D and E for the two scanned papers); fold it into the row
    for f in sorted(glob.glob(f"{P}/*_status2.json")):
        d = load(f)
        if not isinstance(d, dict):
            continue
        r = byid.get(d.get("paper_id"))
        if r is None:
            r = {c: "" for c in cols}
            r["paper_id"] = d.get("paper_id", "")
            rows.append(r)
            byid[r["paper_id"]] = r
        for k in ("claims_rejudged", "notion_findings"):
            try:
                r[k] = int(r.get(k) or 0) + int(d.get(k) or 0)
            except (TypeError, ValueError):
                pass
        r["notes"] = (str(r.get("notes") or "").rstrip(". ")
                      + f". Second pass ({d.get('steps','D+E')}): {d.get('notes','')}").strip(". ")
    # Workers sometimes put prose where the column wants a word or a count.
    # Coerce the shape and push the prose into notes rather than losing it.
    OK = {"yes", "partly", "no", ""}
    for r in rows:
        v = str(r.get("own_question_answered") or "").strip()
        if v.lower() not in OK:
            first = v.lower().split()[0].strip(".,;:()") if v.split() else ""
            r["own_question_answered"] = first if first in OK else "see notes"
            r["notes"] = f"own_question_answered (as written): {v} | " + str(r.get("notes") or "")
        for k in ("claims_rejudged", "notion_findings"):
            v = str(r.get(k) or "").strip()
            if v and not v.isdigit():
                m = re.match(r"\s*(\d+)", v)
                r[k] = m.group(1) if m else ""
                r["notes"] = f"{k} (as written): {v} | " + str(r.get("notes") or "")
        r["notes"] = re.sub(r"\s+", " ", str(r.get("notes") or "")).strip()

    with open(f"{R}/papers_status.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    # ---- counts for REPORT.md -------------------------------------------
    changed = [u for u in updates
               if (u.get("old_verdict") or "").split(" (")[0] != (u.get("new_verdict") or "")]
    print(f"claim_updates      {len(updates):4d}  from {len(files)} worker files")
    print(f"  verdict changes  {len(changed):4d}")
    for u in sorted(changed, key=lambda x: x.get("claim_id", "")):
        print(f"    {u.get('claim_id','?'):8s} {u.get('old_verdict','?')} -> {u.get('new_verdict','?')}"
              f"   [{u.get('paper_id') or u.get('pmid') or '-'}]")
    print(f"extra_studies      {len(extras):4d}")
    print(f"notion_findings    {len(findings):4d}  " +
          str(dict(Counter((f.get('importance') or '?').lower() for f in findings))))
    print("  by kind          " + str(dict(Counter(f.get("kind", "?") for f in findings))))
    print(f"wheal claims       {len(ordered):4d}  filled {filled}, "
          f"untested {sum(1 for c in ordered if not c.get('verdict'))}")
    print("  verdicts         " + str(dict(Counter(c.get("verdict") or "(not yet tested)"
                                                   for c in ordered))))
    print(f"papers_status rows {len(rows):4d}")


main()
