"""Extract each packet PDF to texts/<paper_id>.txt with page markers (pdftotext -layout, one call per page)."""
import glob, os, re, subprocess, sys
os.makedirs("texts", exist_ok=True)
for pdf in sorted(glob.glob("papers/*.pdf")):
    pid = os.path.basename(pdf).split(" - ")[0]
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    out = []
    for p in range(1, pages + 1):
        t = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf, "-"], capture_output=True, text=True).stdout
        out.append(f"\n===== PDF PAGE {p} of {pages} =====\n{t}")
    open(f"texts/{pid}.txt", "w", encoding="utf-8").write("".join(out))
    words = len(re.findall(r"[A-Za-z]{3,}", "".join(out)))
    print(f"{pid}: {pages} pages, {words} words")
