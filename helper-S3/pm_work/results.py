"""Results writer for S3. Every quote is checked (same normalisation as common/tools/quotecheck.py) before it is saved;
Notion sentences are checked against the session's Notion page cache (kept outside the repository).
Import from a heredoc:  import sys; sys.path.insert(0, "pm_work"); from results import *"""
import csv, json, os, re
R = "results_S3"
os.makedirs(f"{R}/paper_cards", exist_ok=True)
NCACHE = "/tmp/claude-0/-home-user-main-repository/2b920992-9cb1-5ba1-ac2a-afc4cbfc18fd/scratchpad/notion_cache"

def n(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())
def parts(q): return [n(p) for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q) if len(n(p)) > 10]
def src_text(paper_id="", pmid=""):
    if paper_id and os.path.exists(f"texts/{paper_id}.txt"):
        return open(f"texts/{paper_id}.txt", encoding="utf-8", errors="replace").read()
    if pmid and os.path.exists(f"pm_work/cache/a_{pmid}.json"):
        a = json.load(open(f"pm_work/cache/a_{pmid}.json")); return a["title"] + " " + a["abstract"]
    return ""
def check(q, paper_id="", pmid=""):
    body = n(src_text(paper_id, pmid)); ps = parts(q)
    ok = bool(body) and bool(ps) and all(p in body for p in ps)
    if not ok: raise SystemExit(f"QUOTE NOT FOUND ({paper_id or pmid}): {q[:200]}")
def check_notion(sentence, slug):
    body = n(open(f"{NCACHE}/{slug}.txt", encoding="utf-8").read().replace("\\n", " "))
    ps = parts(sentence)
    if not (ps and all(p in body for p in ps)): raise SystemExit(f"NOTION SENTENCE NOT FOUND in {slug}: {sentence[:200]}")
def _load(f):
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
def _save(f, items):
    json.dump(items, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def write_card(card):
    for k in card.get("key_results", []) + card.get("author_limitations", []):
        if k.get("quote"): check(k["quote"], paper_id=card["paper_id"])
    _save(f"{R}/paper_cards/{card['paper_id']}.json", card); print("card", card["paper_id"])
def add_claim_update(u):
    if u.get("quote"): check(u["quote"], paper_id=u.get("paper_id", ""), pmid="" if u.get("paper_id") else u.get("pmid", ""))
    f = f"{R}/claim_updates.json"; items = [i for i in _load(f) if not (i["claim_id"] == u["claim_id"] and i.get("paper_id") == u.get("paper_id") and i.get("pmid") == u.get("pmid") and i["kind"] == u["kind"])]
    items.append(u); _save(f, items); print("claim update", u["claim_id"], u["kind"], u["old_verdict"], "->", u["new_verdict"])
def add_extra(e):
    if e.get("quote_from_abstract"): check(e["quote_from_abstract"], pmid=e["pmid"])
    f = f"{R}/extra_studies.json"; items = [i for i in _load(f) if i["pmid"] != e["pmid"]]
    items.append(e); _save(f, items); print("extra study", e["pmid"])
def add_finding(fd, slug):
    check_notion(fd["sentence_as_it_stands"], slug)
    if fd.get("quote"): check(fd["quote"], paper_id=fd.get("paper_id", ""), pmid=fd.get("quote_pmid", ""))
    f = f"{R}/notion_findings.json"; items = _load(f)
    key = (fd["page_url"], fd["section"], fd["sentence_as_it_stands"])
    old = [i for i in items if (i["page_url"], i["section"], i["sentence_as_it_stands"]) == key]
    fd["finding_id"] = old[0]["finding_id"] if old else f"S3-F{len(items) + 1:03d}"
    items = [i for i in items if (i["page_url"], i["section"], i["sentence_as_it_stands"]) != key] + [fd]
    items.sort(key=lambda i: i["finding_id"]); _save(f, items); print("finding", fd["finding_id"], fd["kind"], fd["importance"], "|", fd["page"][:50])
def add_status(row):
    f = f"{R}/papers_status.csv"; cols = ["paper_id", "right_paper", "text_ok", "own_question_answered", "claims_rejudged", "notion_findings", "notes"]
    rows = list(csv.DictReader(open(f, encoding="utf-8"))) if os.path.exists(f) else []
    rows = [r for r in rows if r["paper_id"] != row["paper_id"]] + [row]
    w = csv.DictWriter(open(f, "w", encoding="utf-8", newline=""), fieldnames=cols); w.writeheader(); w.writerows(rows); print("status", row["paper_id"])
