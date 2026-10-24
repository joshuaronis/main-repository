import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
lines = t.split('\n')
PLAN = [("main",1,15),("main",16,81),("menu",82,243),("items",244,354),("main",355,370),("main",371,457),
        ("record",458,621),("buying",622,839),("evaluating",840,992),("research",993,1341),("sweeps",1342,1407),
        ("writing",1408,1659),("main",1660,1670)]
def file_of(n):
    for f,a,b in PLAN:
        if a<=n<=b: return f
    return "?"
pats = [r'\babove\b', r'\bbelow\b', r'this section', r'further down', r'end of this', r'in this section', r'the paragraph under', r'the next paragraph', r'the sentence above', r'two lines above', r'the table above', r'the list below', r'the block below', r'the block', r'\bearlier\b']
rx = re.compile('|'.join(pats))
for i, l in enumerate(lines, 1):
    for m in rx.finditer(l):
        a = max(0, m.start()-110); b = min(len(l), m.end()+60)
        print(f"{i:5d} [{file_of(i):10s}] {m.group(0):15s} …{l[a:b]}…")
