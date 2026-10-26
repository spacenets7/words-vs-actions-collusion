# Reproduce the saved results

## Prerequisites

Use Python 3.12 and a CPU. The review path needs no API keys, cloud login, Docker, model weights or GPU. Network access is used only to clone/download code and install packages. The analysis then uses local saved records.

```text
git clone https://github.com/spacenets7/words-vs-actions-collusion.git
cd words-vs-actions-collusion
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux or macOS
source .venv/bin/activate
```

Then install the pinned numerical and PDF packages:

```text
python -m pip install -r pilot/requirements-review.txt
```

The saved analysis uses NumPy 2.3.5, SciPy 1.18.1 and scikit-learn 1.9.1. The automated reference replay uses Windows/Python 3.12, matching the original numerical environment. The scripts also run on other operating systems; exact floating-point equality is enforced rather than silently relaxing discrepancies.

## 1 Verify the package and freeze

```text
python scripts/verify_review.py
```

Expected checks include the current report/ZIP hashes, all original frozen source/config hashes, exact byte identity of the saved metrics and data exports, 12 development plus 48 held-out records, 240 accepted monitor records, no oracle/private keys in public evidence, unchanged calibration and the final report's exact LLM statement. This is an integrity check, not a claim that arithmetic proves latent intent.

## 2 Replay the complete statistics

```text
python scripts/replay_results.py
```

The wrapper checks the package, extracts it into a fresh directory under ignored `tmp/`, then runs the bundled replay. It recomputes all saved metrics, including 5,000 whole-family bootstrap draws for both targets and paired comparisons. A full run can take several minutes on CPU. Successful completion prints:

```text
Exact metrics replay passed without model/API calls.
```

The result must match the complete saved metrics JSON exactly. Invalid or missing values are not imputed as zero. No prompts, labels, thresholds or test records are changed. The new directory also contains `replayed-metrics.json` and `replayed-metrics.md` for inspection.

For a standalone archive, extract [review/reproducibility.zip](review/reproducibility.zip), install its `requirements.txt`, run `python verify.py`, then `python replay.py`. `bundle-manifest.json` hashes every included payload. This archive verifies its own subset; it does not pretend that the partial source archive can run the original complete-workspace freeze check.

## 3 Run the 23 component and delivery tests

This deeper check also fetches the pinned upstream game and installs the SDK/reporting dependencies. It does not authenticate Modal or run GPU inference.

```text
python -m pip install -r pilot/requirements-verified.txt -r pilot/requirements-report.txt
git clone https://github.com/Jerick-1380/LLM-Trust-Breaking pilot/repos/LLM-Trust-Breaking
git -C pilot/repos/LLM-Trust-Breaking checkout fd11aca351e52c65c929e1a7d46d9f087f237adf
python -m pilot.cli verify-freeze
python -m unittest discover -s pilot/tests -v
```

If the upstream checkout already exists, verify its revision instead of cloning over it. Delivery tests use the committed development snapshot and a saved development-metrics fixture; they do not require the author's ignored local run folder. Frozen experimental source remains unchanged.

The payoff tests require all-3 to yield 6.5 per agent and welfare 32.5, and pair zeros with three 3s to yield 7.7/4.7 and welfare 29.5. Other checks cover private-channel isolation, refusal/invalidity handling, event-linked agreement, cache behavior, calibration, family pairing and detection of saved-artifact tampering.

## Continuous verification and provenance

[GitHub Actions](https://github.com/spacenets7/words-vs-actions-collusion/actions/workflows/review.yml) runs these checks on a fresh checkout, with read-only repository permissions and no model-provider secrets. It has no Modal run step. The original experiment configuration is `10e684f850295c7d8a29c06ee695cc56604908631c5c2e44fa1a9e3767205414`; its frozen manifest is `3c3ccbfe95b31e3c96808a4b904c8e8089483a542d070563dfeffac9fcf662cc`.

Regenerating model trajectories is a different, paid experiment and is not a reproduction requirement here. Report rendering also has separate Word/font/Poppler dependencies. Those operations are documented in the source history and do not run during numerical review.
