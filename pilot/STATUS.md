# Track 2.2 pilot status

Offline pipeline built; 12 tests pass. User confirmed Modal credits ready on 24 October 2026. CUDA/vLLM inference image built and cached. Real development trials are blocked by Modal's requirement to add a payment method before using L4 GPUs. User will add it and notify this chat. The original $20 cap remains; no configuration frozen yet.
The spec is copied to the workspace root; Section 21 takes precedence. No winning configuration is frozen.

## Works
- Untouched upstream clone under pilot/repos/ at fd11aca351e52c65c929e1a7d46d9f087f237adf; changes isolated to pilot/patches runtime adapter and independent controller.
- Public Goods, five agents, ten-round default, private pair channel, six per-agent condition prompts, controller-enforced T actions.
- Own agreement, execution, harm labels; third-action category; strict parse/action validation.
- Four allowlisted monitor views, all-pair table, cached requests, exact binomial rate intervals, paired family bootstrap, calibrated score ensembles.
- All 12 tests passed, including controller/monitor round trip, invalid responses, ensemble regression checks and cloud source-upload isolation.
- Offline smoke: 18 three-round scripted episodes and 72 views. These are fixtures, not real model observations.
- Local environment installed; Modal SDK imports; persistent cloud response cache and per-episode recovery implemented.

## Does not work yet / unvalidated
- Authentication works and image builds completed. Modal then rejected GPU registration with `Please add a payment method to use L4 GPU functions.` No remote GPU function has started.
- Model-serving image, throughput, role adherence, H public wording, I independence, monitor difficulty and realistic model-generated negatives have not been validated.
- Candidate search is implemented but no model iteration has run. No empirically validated frozen config exists.

## Commands
Run from the project root in PowerShell:
```
.\pilot\env\Scripts\python.exe -m unittest discover -s pilot/tests -v
.\pilot\env\Scripts\python.exe -m pilot.cli smoke
.\pilot\env\Scripts\python.exe -m modal setup
.\pilot\env\Scripts\python.exe -m pilot.iterate --resume
```
Then review real development evidence and freeze using pilot/frozen/README.md.
Exact held-out execution/collection/analysis commands are in pilot/README.md;
they intentionally require a validated freeze and explicit --execute-test flag.

At this build handoff: Modal spend initiated by this pilot $0; external API spend $0. Later runtime progress entries below carry updated reservations and estimates.
No held-out trajectories generated or inspected. Development-only tuning required.

Human action: add a payment method in Modal Billing (or arrange an organizer GPU-access exemption), then notify this chat. Credits and authentication are ready; neither needs repeating.

Budget protection: each actual remote batch reserves $1.25 against a $20 loop cap; failures retain reservations. Measured runtime estimates and conservative reservations are separate from actual Modal billed totals. No spend ledger exists yet because authentication failed before the local entry point.

Funding gate: pilot/funding.json now enables the confirmed $50 credit envelope while retaining the $20 cap. Platform GPU eligibility is the remaining blocker.

## Spend at latest checkpoint
- GPU inference: $0; zero agent/monitor calls executed.
- Other API spend: $0.
- Image-build/storage billed total: not yet reconciled with the Modal dashboard; do not represent it as zero.
- Conservative setup allowance in pilot/spend.json: $1.00 reserved, not a measured bill. It reduces the remaining loop envelope to $19 before per-batch reservations.
- Held-out generations: zero. Empirical freeze: absent, intentionally.

## Setup fixes completed on 24 October
- Force UTF-8 for Windows Modal subprocess output.
- Disable Modal's implicit source-package mount; upload only five explicit required Python files. This fixes changing-log build errors and avoids mounting the environment, clones or data.
- Cached image includes vLLM 0.21.0 on CUDA 12.9/Python 3.12. The image has built; GPU serving and model behavior remain unvalidated.
- Resume command after GPU access is ready: `.\pilot\env\Scripts\python.exe -X utf8 -m pilot.iterate --resume`.

### Progress 2026-10-24T17:38:27.035687+00:00
Development screening: Qwen2.5-3B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $0.00; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T17:39:31.615102+00:00
Development screening: Qwen2.5-3B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $0.00; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T17:41:14.429826+00:00
Development screening: Qwen2.5-3B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $0.00; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T17:42:58.163143+00:00
Development screening: Qwen2.5-3B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $0.00; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.
