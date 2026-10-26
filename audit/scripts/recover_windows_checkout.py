"""Recover readable blobs after a Windows checkout fails on colon filenames.

Does not alter Git history/index. Excludes Windows-invalid paths and writes only
inside the explicitly selected repository. Records excluded names for provenance.
"""
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path
root = Path(__file__).resolve().parents[2]
repo = root / "repos/cotrh-blue-team"
archive = subprocess.run(["git", "-c", "core.protectNTFS=false", "-C", str(repo), "archive", "--format=zip", "HEAD"], check=True, capture_output=True).stdout
skipped, written = [], 0
with zipfile.ZipFile(io.BytesIO(archive)) as z:
    for info in z.infolist():
        if re.search(r'[<>:"|?*]', info.filename) or any(p in {"..", ".git"} for p in Path(info.filename).parts):
            skipped.append(info.filename)
            continue
        destination = (repo / info.filename).resolve()
        if not destination.is_relative_to(repo.resolve()):
            raise ValueError(info.filename)
        if info.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(z.read(info))
            written += 1
(root / "audit/evidence/windows_checkout.json").write_text(json.dumps({"written": written, "skipped": skipped}, indent=2), encoding="utf-8")
print(f"Recovered {written} files; skipped {len(skipped)} Windows-invalid paths")
