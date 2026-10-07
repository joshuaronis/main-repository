"""Save PubMed *connector* results in the same cache format as common/tools/pm.py.

Why: this container's network policy blocks eutils.ncbi.nlm.nih.gov, so pm.py cannot run here. Searches and abstracts were
taken from the PubMed MCP connector (search_articles / get_article_metadata) and written here verbatim, so that
common/tools/quotecheck.py can check quotes against ./pm_work/cache/a_<pmid>.json exactly as with pm.py.

  python3 pm_work/pmsave.py article  < one JSON object or a list (fields: pmid, year, first_author, title, journal,
                                        pubtypes, doi, pmcid, abstract)
  python3 pm_work/pmsave.py search   < {"query":..., "count":..., "translation":..., "pmids":[...]}  (records filled
                                        from cached articles when present)
"""
import hashlib, json, os, sys, time
D = os.path.join(os.getcwd(), "pm_work")
CACHE = f"{D}/cache"
os.makedirs(CACHE, exist_ok=True)
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
kind = sys.argv[1]
data = json.load(sys.stdin)
if kind == "article":
    for r in (data if isinstance(data, list) else [data]):
        r.setdefault("pubtypes", []); r.setdefault("doi", ""); r.setdefault("pmcid", "")
        r["source"] = f"PubMed connector get_article_metadata, retrieved {now}"
        json.dump(r, open(f"{CACHE}/a_{r['pmid']}.json", "w"), ensure_ascii=False, indent=1)
        print("saved article", r["pmid"], "|", r["title"][:90])
elif kind == "search":
    q, retmax = data["query"], data.get("retmax", 100)
    key = hashlib.sha1(f"{q}|{retmax}".encode()).hexdigest()[:16]
    recs = []
    for p in data["pmids"]:
        f = f"{CACHE}/a_{p}.json"
        recs.append(json.load(open(f)) if os.path.exists(f) else {"pmid": p})
    res = {"query": q, "retmax": retmax, "count": data["count"], "translation": data.get("translation", ""),
           "errors": {}, "warnings": {}, "date_searched": now, "records": recs,
           "source": "PubMed connector search_articles (eutils blocked by the container's network policy)",
           "note": data.get("note", "")}
    json.dump(res, open(f"{CACHE}/s_{key}.json", "w"), ensure_ascii=False, indent=1)
    print(f"saved search s_{key}: count {data['count']}, {len(recs)} pmids")
