"""Extract page-delimited layout text, tables, PDF links, and hashes offline."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "audit" / "text"
OUT.mkdir(parents=True, exist_ok=True)
manifest = []
for path in sorted((ROOT / "papers").glob("*.pdf")):
    reader = PdfReader(path)
    links = []
    for n, page in enumerate(reader.pages, 1):
        for annotation in page.get("/Annots", []):
            obj = annotation.get_object()
            uri = obj.get("/A", {}).get("/URI")
            if uri:
                links.append({"page": n, "uri": str(uri)})
    executable = shutil.which("pdftotext")
    if executable:
        subprocess.run([executable, "-layout", str(path), str(OUT / (path.stem + ".layout.txt"))], check=True)
    texts, tables = [], []
    with pdfplumber.open(path) as pdf:
        for n, page in enumerate(pdf.pages, 1):
            texts.append(f"\n\n===== PDF PAGE {n} =====\n\n" + (page.extract_text(layout=False) or ""))
            for table in page.extract_tables():
                tables.append({"page": n, "rows": table})
    (OUT / (path.stem + ".txt")).write_text("\n".join(texts), encoding="utf-8")
    (OUT / (path.stem + ".links.json")).write_text(json.dumps(links, indent=2), encoding="utf-8")
    (OUT / (path.stem + ".tables.json")).write_text(json.dumps(tables, indent=2), encoding="utf-8")
    record = {"file": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "pages": len(reader.pages), "pdftotext": bool(executable)}
    manifest.append(record)
    print(json.dumps(record), flush=True)
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
