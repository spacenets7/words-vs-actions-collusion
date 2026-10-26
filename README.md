# Words, Actions and Evidence in Collusion Detection

Track 2.2 pilot for the [Apart AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25).

Repository: [spacenets7/words-vs-actions-collusion](https://github.com/spacenets7/words-vs-actions-collusion) · private project backup.

**Author:** Siddeshwar U S · **Affiliation:** MIT, Manipal · **Team:** spacenets

Can a monitor distinguish harmful collusion from legitimate cooperation, independent deception and unexecuted plans? This project compares public words, executed actions, their raw union and a structured claim-versus-outcome report in a repeated public-goods game with five agents and ten rounds.

## Read the outputs

- [Research report (PDF)](pilot/submission/report.pdf) and [editable manuscript](pilot/submission/report.md): nine pages, seven main-text pages, ten numbered equations, seven tables and four figures.
- [Five downloadable PNG graphs](pilot/figures_png/README.md) and [graph ZIP](pilot/figures_png/track_2_2_png_graphs.zip).
- [Metrics and uncertainty](pilot/results/metrics.md), [formula reference](pilot/submission/FORMULAS.md) and [verified presentation checks](pilot/submission/presentation-verification.json).
- [Self-contained offline analysis bundle](pilot/submission/local-reproducibility-bundle.zip): sanitized trajectories, separate automatic labels, monitor evidence, analysis code and exact metrics replay.
- [Paper audit findings](audit/FINDINGS.md) and [how all 22 findings informed this project](pilot/AUDIT_IMPLEMENTATION_MAP.md).
- [Current status](pilot/STATUS.md), [iteration history](pilot/iterations.md), [submission handoff](pilot/submission/HANDOFF.md) and [original project plan](TRACK_2_2_END_TO_END_PLAN_v2.md).

## Completed experiment

There are 12 development episodes and 48 held-out episodes from eight held-out families, with 240 valid monitor outputs overall. Configuration, model revisions, thresholds and label definitions were frozen before held-out execution. The agent is Qwen2.5-3B-Instruct and the auditor is Qwen3-4B-Instruct-2507; exact revisions and settings are in [the frozen configuration](pilot/frozen/config.json).

| Monitor view | Held-out implementation AUROC |
|---|---:|
| V1: public words | 0.597 |
| V2: actions and payoffs | 0.843 |
| V3: both, raw | 0.719 |
| V4: structured claim/outcome report | 0.731 |

The paired V4 minus V2 AUROC difference is -0.112, with a 95% family-bootstrap interval of [-0.215, 0.029]. These data do not establish a consistent advantage from combining words and actions. The report retains all failed controls and reports uncertainty.

**Research status:** labels are automatic and await two independent human reviews and adjudication. Public communication in the hidden-collusion and independent-deception conditions is deliberately controlled; this does not measure natural concealment ability. Public observations alone cannot generally identify a private agreement. Three hidden-collusion episodes failed the automatic implementation gate and remain in the analysis. Author approval and the external Apart submission remain pending.

## Replay the saved analysis without a model or API

The archive is the portable analysis entry point. Its public trajectories exclude private negotiation and private plans; its separate oracle-label file is available for evaluation.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy scipy scikit-learn
Expand-Archive -LiteralPath .\pilot\submission\local-reproducibility-bundle.zip -DestinationPath .\tmp\replay
.\.venv\Scripts\python.exe .\tmp\replay\replay.py
```

The replay recomputes the saved metrics, including 5,000 paired family-bootstrap draws, and requires exact JSON equality. It makes no model or API calls. Use an empty destination for a new extraction. The archived analysis dependencies and model/source provenance are included for reproducibility.

## Work with the complete pipeline

The runtime is separate from the untouched upstream checkout. Clone the pinned dependency locally before the upstream-equivalence tests:

```powershell
python -m venv pilot/env
.\pilot\env\Scripts\python.exe -m pip install -r pilot/requirements-verified.txt
git clone https://github.com/Jerick-1380/LLM-Trust-Breaking pilot/repos/LLM-Trust-Breaking
git -C pilot/repos/LLM-Trust-Breaking checkout fd11aca351e52c65c929e1a7d46d9f087f237adf
.\pilot\env\Scripts\python.exe -m pilot.cli verify-freeze
.\pilot\env\Scripts\python.exe -m unittest discover -s pilot/tests -v
```

The delivered checkout passed 23 tests. The [implementation guide](pilot/README.md) describes offline fixtures, private-channel isolation, caching, labels and monitor views. [The adapter notes](pilot/patches/README.md) explain upstream reuse and the decision to implement a separate controller. [The frozen run script](pilot/RUN_FULL_DESIGN.ps1) documents the paid execution entry point; running it is not necessary to inspect or replay the completed results. New cloud generation requires locally authenticated Modal credentials, GPU access and budget reservations. Preserve the spend ledger and held-out checkpoints.

Report construction additionally uses [the report requirements](pilot/requirements-report.txt), a suitable math font and Poppler for rendering. Full report regeneration and presentation verification also use local run journals omitted from this repository; the included PDF and portable analysis replay are the delivered outputs.

## Repository and data boundaries

This private repository preserves the project's source and Git history, development configurations, frozen configuration and development snapshot, own paper-audit reports/scripts, costs, aggregate results, figures and submission artifacts. The development snapshot includes private oracle material; it must never be supplied to a monitor as evidence. Treat a future public release as a separate data and licensing review.

Credentials, environments, model weights, caches, paid-run journals, human-review packets, third-party checkouts, original paper PDFs, extracted full paper text and downloaded tools are excluded. The audit's own reports and numeric checks are included; reproducing those checks requires the separately acquired inputs described in [audit/REPRODUCE.md](audit/REPRODUCE.md). Their original local-file links may require those inputs. Third-party code and model licenses remain with their authors; no project-wide release license has been selected.

The latest saved Modal closed-interval usage report is **$5.41625951**. The runtime estimate overlaps that report; the **$7.60398478** billed/reserved envelope includes unsettled reservations and a setup/storage allowance and is not an additional charge. External API spend was $0. See [cost-summary.json](pilot/submission/cost-summary.json) for the billing interval and caveats. Repository packaging does not launch GPU jobs.
