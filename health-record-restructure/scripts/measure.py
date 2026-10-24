import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
lines = t.split('\n')
# headings with line numbers (1-based)
heads = [(i+1, l) for i, l in enumerate(lines) if re.match(r'^#{1,4} ', l)]
# code fences to skip headings inside code blocks
fence = False; real = []
for i, l in enumerate(lines):
    if l.lstrip().startswith('```'):
        fence = not fence; continue
    if not fence and re.match(r'^#{1,4} ', l):
        real.append((i+1, l))
# size of each heading's span up to next heading of same or higher level
def level(h): return len(h.split(' ')[0])
out = []
for k, (ln, h) in enumerate(real):
    lv = level(h)
    end = len(lines)
    for ln2, h2 in real[k+1:]:
        if level(h2) <= lv:
            end = ln2 - 1; break
    size = sum(len(x)+1 for x in lines[ln-1:end])
    out.append((ln, end, lv, size, h))
for ln, end, lv, size, h in out:
    print(f"{ln:5d}-{end:5d} L{lv} {size:7d}  {h[:90]}")
print("TOTAL", len(t))
