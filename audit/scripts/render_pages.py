"""Render selected evidence pages with Poppler, without changing the PDFs."""
import argparse
import shutil
import subprocess
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument("paper")
p.add_argument("pages")
p.add_argument("--dpi", type=int, default=110)
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
binary = shutil.which("pdftoppm") or str(root / "audit/tools/poppler-26.09.0/Library/bin/pdftoppm.exe")
for spec in a.pages.split(","):
    bounds = [int(x) for x in spec.split("-")]
    for n in range(bounds[0], bounds[-1] + 1):
        prefix = root / "audit/evidence" / f"{a.paper}-p{n}"
        subprocess.run([binary, "-f", str(n), "-l", str(n), "-r", str(a.dpi), "-singlefile", "-png", str(root / "papers" / (a.paper + ".pdf")), str(prefix)], check=True)
        print(str(prefix) + ".png")
