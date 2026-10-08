"""Extract each packet PDF to texts/<paper_id>.txt with page markers.

Each page is written twice: first as `pdftotext -layout` (the format the hand-over asks for), then as pdftotext's default
reading-order output, under a second marker. Two-column layout interleaves the columns line by line, so a sentence that
runs over several lines is not contiguous in the -layout text; the reading-order copy keeps it whole, so that
common/tools/quotecheck.py can find verbatim quotes. Page numbers in results are PDF page numbers (see markers).
Typographic ligatures (U+FB00–FB06, e.g. \uFB01 for "fi") are expanded to plain letters, because quotecheck.py drops
non-ASCII characters and would otherwise read "\uFB01ber" as "ber"."""
LIG = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl", "\ufb03": "ffi", "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st"}
def unlig(s):
    for k, v in LIG.items(): s = s.replace(k, v)
    return s
import glob, os, re, subprocess
os.makedirs("texts", exist_ok=True)
for pdf in sorted(glob.glob("papers/*.pdf")):
    pid = os.path.basename(pdf).split(" - ")[0]
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    out = []
    for p in range(1, pages + 1):
        lay = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf, "-"], capture_output=True, text=True).stdout
        raw = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), pdf, "-"], capture_output=True, text=True).stdout
        out.append(f"\n===== PDF PAGE {p} of {pages} (pdftotext -layout) =====\n{lay}"
                   f"\n===== PDF PAGE {p} of {pages} (reading order, same page) =====\n{raw}")
    open(f"texts/{pid}.txt", "w", encoding="utf-8").write(unlig("".join(out)))
    words = len(re.findall(r"[A-Za-z]{3,}", "".join(out)))
    print(f"{pid}: {pages} pages, {words} words (both copies)")
