"""Check each quote's page attribution is internally consistent for its paper.

texts/<id>.txt is marked with sequential PDF pages (===== PAGE n =====), but most
workers cite the journal's printed page. Both are fine; what matters is that one
paper uses one convention throughout. So: find each paper's modal offset between
the cited page and the page the quote is actually on, report it, and flag only the
quotes that break it.
"""
import glob, json, os, re
from collections import Counter, defaultdict

def n(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())

PAGES = {}
def pages_of(pid):
    if pid in PAGES: return PAGES[pid]
    p = f"texts/{pid}.txt"
    out = None
    if os.path.exists(p):
        parts = re.split(r"=====\s*PAGE\s+(\d+)\s*=====",
                         open(p, encoding="utf-8", errors="replace").read())
        out = {int(parts[i]): n(parts[i + 1]) for i in range(1, len(parts), 2)}
    PAGES[pid] = out
    return out

def locate(q, pg):
    frag = [x for x in (n(p) for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q)) if len(x) > 10]
    if not frag: return []
    hits = sorted(p for p, body in pg.items() if all(x in body for x in frag))
    if not hits:
        longest = max(frag, key=len)
        hits = sorted(p for p, body in pg.items() if longest in body)
    return hits

rows = defaultdict(list)   # pid -> (file, claimed, actual_pages, quote)
for f in sorted(glob.glob("results_S1/paper_cards/*.json")) + sorted(glob.glob("results_S1/parts/*.json")):
    try: d = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    for it in (d if isinstance(d, list) else [d]):
        if not isinstance(it, dict): continue
        pid = it.get("paper_id")
        if not pid or not pages_of(pid): continue
        quotes = []
        pnum = it.get("page_in_paper") if "page_in_paper" in it else it.get("page")
        if it.get("quote"): quotes.append((it["quote"], pnum))
        for k in ("key_results", "author_limitations"):
            for q in it.get(k) or []:
                if isinstance(q, dict) and q.get("quote"):
                    quotes.append((q["quote"], q.get("page")))
        for q, claimed in quotes:
            if claimed in (None, "", 0): continue
            try: claimed = int(claimed)
            except (TypeError, ValueError): continue
            hits = locate(q, pages_of(pid))
            if hits: rows[pid].append((f, claimed, hits, q))

bad = tot = 0
for pid in sorted(rows):
    offs = Counter(c - h[0] for _, c, h, _ in rows[pid])
    off, nmode = offs.most_common(1)[0]
    conv = "sequential PDF pages" if off == 0 else f"journal pages (offset {off:+d})"
    odd = [(f, c, h, q) for f, c, h, q in rows[pid] if (c - h[0]) != off]
    tot += len(rows[pid]); bad += len(odd)
    print(f"{pid}: {len(rows[pid]):3d} quotes, {conv}, {nmode} agree, {len(odd)} deviate")
    for f, c, h, q in odd:
        print(f"    says p{c}, text page {h} (expected p{h[0]+off}) :: {os.path.basename(f)} :: {q[:70]}")
print(f"\n{tot} page attributions checked, {bad} inconsistent with their paper's own convention")
