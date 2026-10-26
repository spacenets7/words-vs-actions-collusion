"""Print complete numbered pages from pdftotext -layout output."""
import argparse
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
p = argparse.ArgumentParser()
p.add_argument("paper")
p.add_argument("pages", help="Comma-separated page numbers/ranges, e.g. 1-4,9")
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
pages = (root / "audit" / "text" / (a.paper + ".layout.txt")).read_text(encoding="utf-8").split("\f")
for spec in a.pages.split(","):
    bounds = [int(n) for n in spec.split("-")]
    for n in range(bounds[0], bounds[-1] + 1):
        print(f"\n===== PDF PAGE {n} =====\n{pages[n-1]}")
