"""PubMed helper (shared rate limit, cached results) for S-686 (absence-claim refutation searches). Shared by several workers: a lock file keeps all
callers together under NCBI's 3-requests-per-second limit, and every result is cached under ./pm_work/cache/ (or $PM_DIR/cache/).

  python3 tools/pm.py search "<PubMed query>" [retmax=100]   -> count, PubMed's query translation, then one line per record:
                                                           PMID | year | first author | title | journal | publication types
  python3 tools/pm.py abstracts PMID[,PMID...]                -> title, publication types, PMCID if free in PMC, and the abstract
"""
import fcntl, hashlib, json, os, sys, time, xml.etree.ElementTree as ET
import requests

D = os.environ.get("PM_DIR", os.path.join(os.getcwd(), "pm_work"))
os.makedirs(D, exist_ok=True)
CACHE = f"{D}/cache"
os.makedirs(CACHE, exist_ok=True)
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
UA = {"User-Agent": "literature-check/1.0 (absence-claim searches; private research record)"}


def _call(path, data):
    lockf = open(f"{D}/.pm.lock", "a+")
    for k in range(8):
        fcntl.flock(lockf, fcntl.LOCK_EX)
        try:
            lockf.seek(0)
            try:
                last = float(open(f"{D}/.pm.last").read() or 0)
            except (OSError, ValueError):
                last = 0.0
            wait = 0.4 - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            open(f"{D}/.pm.last", "w").write(str(time.time()))
        finally:
            fcntl.flock(lockf, fcntl.LOCK_UN)
        try:
            r = requests.post(EU + path, data=data, headers=UA, timeout=90)
            if r.status_code == 200 and "API rate limit exceeded" not in r.text[:300]:
                return r.text
        except requests.RequestException:
            pass
        time.sleep(1.5 * (k + 1))
    raise SystemExit(f"PubMed did not answer after 8 tries: {path}")


def _parse(xml):
    out = []
    root = ET.fromstring(xml)
    for art in root.findall("PubmedArticle"):
        mc = art.find("MedlineCitation")
        a = mc.find("Article")
        ids = {e.get("IdType"): (e.text or "").strip() for e in art.findall("PubmedData/ArticleIdList/ArticleId")}
        abst = []
        for t in a.findall("Abstract/AbstractText"):
            lab = t.get("Label")
            txt = "".join(t.itertext()).strip()
            abst.append(f"{lab}: {txt}" if lab else txt)
        y = a.findtext("Journal/JournalIssue/PubDate/Year") or (a.findtext("Journal/JournalIssue/PubDate/MedlineDate") or "")[:4]
        out.append({"pmid": mc.findtext("PMID"), "year": y,
                    "first_author": a.findtext("AuthorList/Author/LastName") or a.findtext("AuthorList/Author/CollectiveName") or "",
                    "title": "".join(a.find("ArticleTitle").itertext()).strip() if a.find("ArticleTitle") is not None else "",
                    "journal": a.findtext("Journal/ISOAbbreviation") or a.findtext("Journal/Title") or "",
                    "pubtypes": [e.text for e in a.findall("PublicationTypeList/PublicationType")],
                    "doi": ids.get("doi", ""), "pmcid": ids.get("pmc", ""), "abstract": "\n".join(abst)})
    return out


def search(q, retmax=100):
    key = hashlib.sha1(f"{q}|{retmax}".encode()).hexdigest()[:16]
    cf = f"{CACHE}/s_{key}.json"
    if os.path.exists(cf):
        res = json.load(open(cf))
    else:
        js = json.loads(_call("esearch.fcgi", {"db": "pubmed", "term": q, "retmax": retmax, "retmode": "json", "sort": "relevance"}))
        er = js["esearchresult"]
        ids = er.get("idlist", [])
        recs = _parse(_call("efetch.fcgi", {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"})) if ids else []
        order = {p: i for i, p in enumerate(ids)}
        recs.sort(key=lambda r: order.get(r["pmid"], 1e9))
        res = {"query": q, "retmax": retmax, "count": int(er.get("count", 0)), "translation": er.get("querytranslation", ""),
               "errors": er.get("errorlist", {}), "warnings": er.get("warninglist", {}),
               "date_searched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "records": recs}
        json.dump(res, open(cf, "w"), ensure_ascii=False, indent=1)
        for r in recs:
            json.dump(r, open(f"{CACHE}/a_{r['pmid']}.json", "w"), ensure_ascii=False, indent=1)
    print(f"COUNT {res['count']} (showing {len(res['records'])}) | searched {res['date_searched']}")
    print(f"TRANSLATION {res['translation']}")
    if res["errors"] and any(res["errors"].values()):
        print("ERRORS", res["errors"])
    if res["warnings"] and any(res["warnings"].values()):
        print("WARNINGS", res["warnings"])
    for r in res["records"]:
        print(f"{r['pmid']} | {r['year']} | {r['first_author']} | {r['title']} | {r['journal']} | {'; '.join(r['pubtypes'])}")


def abstracts(pmids):
    need = [p for p in pmids if not os.path.exists(f"{CACHE}/a_{p}.json")]
    if need:
        for r in _parse(_call("efetch.fcgi", {"db": "pubmed", "id": ",".join(need), "retmode": "xml"})):
            json.dump(r, open(f"{CACHE}/a_{r['pmid']}.json", "w"), ensure_ascii=False, indent=1)
    for p in pmids:
        try:
            r = json.load(open(f"{CACHE}/a_{p}.json"))
        except OSError:
            print(f"== {p}: not found\n")
            continue
        print(f"== {r['pmid']} | {r['year']} | {r['first_author']} | {r['title']} | {r['journal']} | {'; '.join(r['pubtypes'])} | "
              f"doi {r['doi'] or '-'} | {('free in PMC: ' + r['pmcid']) if r['pmcid'] else 'not in PMC'}")
        print(r["abstract"] or "(no abstract in PubMed)")
        print()


if __name__ == "__main__":
    if sys.argv[1] == "search":
        search(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 100)
    elif sys.argv[1] == "abstracts":
        abstracts([p.strip() for p in sys.argv[2].split(",") if p.strip()])
