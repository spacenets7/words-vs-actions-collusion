# Reproducing the audit

Run from the workspace in PowerShell:

```powershell
& .\audit\scripts\run_checks.ps1
```

Use `-Reextract` to regenerate page text, table extraction, PDF hashes and `pdftotext -layout` output first. Python requires numpy, pandas, pdfplumber and pypdf; the wrapper defaults to this machine's bundled Python. A different executable can be supplied with `-PythonExe`. The Poppler tools are retained in `audit/tools/`.

The verification script uses original source functions and synthetic scores/actions to test implementation contracts, plus arithmetic from the supplied PDF tables and released aggregate CSVs. It makes no network calls and never loads a model provider. It does not rerun model generation, Docker environments, or the papers' full evaluation pipelines. On this Windows host, asyncio stalled inside the restricted sandbox; the successful verification ran outside it.

- `text/manifest.json`: source PDF hashes, page counts and layout-text hashes.
- `text/*.layout.txt`: requested Poppler extraction; page boundaries are form feeds.
- `text/*.txt`, `*.tables.json`, `*.links.json`: independent extraction and PDF hyperlink inventory.
- `evidence/verification.json` and `verification.log`: numeric checks and component results.
- `evidence/findings.json`: machine-readable records used by the report builder.
- `evidence/report_validation.json`: completeness and local-link checks.
- `evidence/*-p*.png`: rendered evidence pages.
- `evidence/control_arena-14.2.0.whl` and extracted formatter files: source-only inspection of TraceGuard's locked dependency; no installation.
- `evidence/windows_checkout.json`: four Windows-invalid completed-ID paths skipped when recovering the BCB Git archive.

Repository revisions are recorded in the reports and verification JSON. Repositories were cloned at their available default heads, not at an inferred paper commit. The BCB checkout was recovered with `recover_windows_checkout.py`; its Git index still reflects the checkout failure, so use the recorded HEAD and source files rather than treating its working-tree status as an author change.

Arike's two repository URLs came from PDF p.10. No SCHEME-specific code/data link was present in its PDF; the Inspect Scout dependency link does not supply the benchmark. Arike's private SHADE-Arena and external bulk logs were not acquired. Unverifiable results and possible alternative explanations are kept in each report's COULD NOT VERIFY section and are not counted as confirmed errors.
