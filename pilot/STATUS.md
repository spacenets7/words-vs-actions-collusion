# Track 2.2 pilot status

Offline pipeline built. Modal authentication verified by a successful read-only remote app-list request on 23 October 2026. GPU runs are paused for funding: user reports $1 available and expects $50 in 6-7 hours.
The spec is copied to the workspace root; Section 21 takes precedence. No winning configuration is frozen.

## Works
- Untouched upstream clone under pilot/repos/ at fd11aca351e52c65c929e1a7d46d9f087f237adf; changes isolated to pilot/patches runtime adapter and independent controller.
- Public Goods, five agents, ten-round default, private pair channel, six per-agent condition prompts, controller-enforced T actions.
- Own agreement, execution, harm labels; third-action category; strict parse/action validation.
- Four allowlisted monitor views, all-pair table, cached requests, exact binomial rate intervals, paired family bootstrap, calibrated score ensembles.
- All 11 tests passed, including actual controller/monitor round trip, invalid responses and ensemble regression checks.
- Offline smoke: 18 three-round scripted episodes and 72 views. These are fixtures, not real model observations.
- Local environment installed; Modal SDK imports; persistent cloud response cache and per-episode recovery implemented.

## Does not work yet / unvalidated
- Earlier Modal probe failed with missing credentials; authentication now works. No remote GPU function has started.
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

Human action: notify this chat once the credits have actually arrived. Then verify credit/GPU eligibility and enable pilot/funding.json before continuing the already authorized development loop. Authentication setup no longer needs repeating.

Budget protection: each actual remote batch reserves $1.25 against a $20 loop cap; failures retain reservations. Measured runtime estimates and conservative reservations are separate from actual Modal billed totals. No spend ledger exists yet because authentication failed before the local entry point.

Funding gate: pilot/funding.json disables GPU execution while only $1 is available. Both search and individual batches check the gate. Read-only authentication check incurred no pilot compute spend; total initiated Modal/API spend remains $0.
