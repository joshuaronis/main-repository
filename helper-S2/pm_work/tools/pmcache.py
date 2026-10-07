"""Records PubMed results obtained through the PubMed connector (MCP), for sessions whose network blocks
eutils.ncbi.nlm.nih.gov so that common/tools/pm.py cannot run.

Writes the same cache that pm.py writes, so common/tools/quotecheck.py can check quotes taken from abstracts:
  pm_work/cache/a_<pmid>.json      one article, pm.py's fields (pmid, year, first_author, title, journal, pubtypes,
                                   doi, pmcid, abstract) plus "source", "retrieved" and "redacted"
  pm_work/cache/s_mcp_<key>.json   one search: query, count, translation, pmids returned, date searched, who ran it
  pm_work/searches_log.tsv         one line per search: date, paper, count, query

usage (run from helper-S2/, paste the connector's JSON result on stdin):
  python3 pm_work/tools/pmcache.py article --paper S-686-37 [--redacted] < result.json
        result.json = the get_article_metadata result ({"articles": [...]}), a list of articles, or one article
  python3 pm_work/tools/pmcache.py search --paper S-686-37 [--max 20] < result.json
        result.json = the search_articles result (pmids, total_count, query, query_translation)
--redacted marks an abstract in which a dose ceiling, toxicity or overdose threshold or antidote passage was
replaced by [dose figure omitted] before saving.
"""
import hashlib, json, os, sys, time

D = os.environ.get("PM_DIR", os.path.join(os.getcwd(), "pm_work"))
CACHE = os.path.join(D, "cache")
os.makedirs(CACHE, exist_ok=True)


def arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--") else True
    return default


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def article(a, paper, redacted):
    ids = a.get("identifiers", {}) or {}
    pmid = str(ids.get("pmid") or a.get("pmid") or "").strip()
    if not pmid:
        raise SystemExit("article without a PMID: " + json.dumps(a)[:200])
    authors = a.get("authors") or []
    fa = (authors[0].get("last_name") or authors[0].get("collective_name") or "") if authors else ""
    jr = a.get("journal") or {}
    rec = {"pmid": pmid,
           "year": str((a.get("publication_date") or {}).get("year") or a.get("year") or ""),
           "first_author": fa,
           "title": a.get("title") or "",
           "journal": jr.get("iso_abbreviation") or jr.get("title") or "" if isinstance(jr, dict) else str(jr),
           "pubtypes": a.get("article_types") or a.get("pubtypes") or [],
           "doi": ids.get("doi") or a.get("doi") or "",
           "pmcid": ids.get("pmc") or ids.get("pmcid") or a.get("pmcid") or "",
           "abstract": a.get("abstract") or "",
           "source": "PubMed MCP connector (get_article_metadata); eutils blocked by the session's network policy",
           "retrieved": now(), "retrieved_for": paper, "redacted": bool(redacted)}
    json.dump(rec, open(os.path.join(CACHE, f"a_{pmid}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"saved a_{pmid}.json | {rec['year']} | {fa} | {rec['title'][:90]} | abstract {len(rec['abstract'])} chars"
          f"{' | REDACTED' if redacted else ''}")


def main():
    mode, paper = sys.argv[1], arg("--paper", "")
    data = json.loads(sys.stdin.read())
    if mode == "article":
        arts = data.get("articles") if isinstance(data, dict) and "articles" in data else data
        arts = arts if isinstance(arts, list) else [arts]
        for a in arts:
            article(a, paper, arg("--redacted", False))
    elif mode == "search":
        q = data.get("query", "")
        mx = int(arg("--max", data.get("returned_count") or 20))
        key = hashlib.sha1(f"{q}|{mx}".encode()).hexdigest()[:16]
        rec = {"query": q, "max_results": mx, "count": data.get("total_count"),
               "translation": data.get("query_translation", ""), "pmids": data.get("pmids", []),
               "date_searched": now(), "searched_for": paper,
               "source": "PubMed MCP connector (search_articles); eutils blocked by the session's network policy"}
        json.dump(rec, open(os.path.join(CACHE, f"s_mcp_{key}.json"), "w"), ensure_ascii=False, indent=1)
        with open(os.path.join(D, "searches_log.tsv"), "a", encoding="utf-8") as f:
            f.write(f"{rec['date_searched']}\t{paper}\t{rec['count']}\t{q}\n")
        print(f"saved s_mcp_{key}.json | COUNT {rec['count']} | {len(rec['pmids'])} PMIDs | {q[:120]}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
