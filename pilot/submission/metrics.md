# Monitor evaluation

Automatic event-based labels are provisional until two independent score-blind human reviews.

Evaluation rows use held-out families only; thresholds use development negatives. Rate intervals assume independent episodes. AUROC and paired differences resample whole families. Rounds are not independent samples. Scores are suspicion rankings, not calibrated probabilities.

## Implemented harmful collusion

| Method | N | AUROC | Family 95% interval | TPR | Exact 95% interval | FPR | Exact 95% interval |
|---|---:|---:|---|---:|---|---:|---|
| V1 | 48 | 0.597 | [0.491, 0.734] | 0.000 | [0.000, 0.247] | 0.029 | [0.001, 0.149] |
| V2 | 48 | 0.843 | [0.767, 0.898] | 0.462 | [0.192, 0.749] | 0.171 | [0.066, 0.336] |
| V3 | 48 | 0.719 | [0.589, 0.852] | 0.692 | [0.386, 0.909] | 0.286 | [0.146, 0.463] |
| V4 | 48 | 0.731 | [0.646, 0.830] | 0.538 | [0.251, 0.808] | 0.171 | [0.066, 0.336] |
| mean | 48 | 0.843 | [0.792, 0.914] | 0.308 | [0.091, 0.614] | 0.029 | [0.001, 0.149] |
| max | 48 | 0.816 | [0.755, 0.890] | 0.000 | [0.000, 0.247] | 0.029 | [0.001, 0.149] |
| constant | 48 | 0.500 | [0.500, 0.500] | 0.000 | [0.000, 0.247] | 0.000 | [0.000, 0.100] |
| promise_break | 48 | 0.463 | [0.332, 0.552] | 0.000 | [0.000, 0.247] | 0.114 | [0.032, 0.267] |
| action_gap | 48 | 0.852 | [0.778, 0.908] | 0.000 | [0.000, 0.247] | 0.000 | [0.000, 0.100] |

| Paired AUROC difference | N | Families | Difference | Family 95% interval | Valid bootstrap draws |
|---|---:|---:|---:|---|---:|
| V4-V1 | 48 | 8 | 0.134 | [-0.020, 0.271] | 5000 |
| V4-V2 | 48 | 8 | -0.112 | [-0.215, 0.029] | 5000 |
| V4-V3 | 48 | 8 | 0.012 | [-0.142, 0.179] | 5000 |
| V4-mean | 48 | 8 | -0.112 | [-0.231, -0.003] | 5000 |
| V4-max | 48 | 8 | -0.086 | [-0.207, 0.031] | 5000 |

## Harmful agreement attempts

| Method | N | AUROC | Family 95% interval | TPR | Exact 95% interval | FPR | Exact 95% interval |
|---|---:|---:|---|---:|---|---:|---|
| V1 | 48 | 0.865 | [0.808, 0.937] | 0.762 | [0.528, 0.918] | 0.111 | [0.024, 0.292] |
| V2 | 48 | 0.622 | [0.546, 0.666] | 0.476 | [0.257, 0.702] | 0.370 | [0.194, 0.576] |
| V3 | 48 | 0.770 | [0.692, 0.860] | 0.810 | [0.581, 0.946] | 0.370 | [0.194, 0.576] |
| V4 | 48 | 0.835 | [0.781, 0.896] | 0.333 | [0.146, 0.570] | 0.074 | [0.009, 0.243] |
| mean | 48 | 0.892 | [0.861, 0.932] | 0.905 | [0.696, 0.988] | 0.370 | [0.194, 0.576] |
| max | 48 | 0.817 | [0.780, 0.858] | 0.905 | [0.696, 0.988] | 0.370 | [0.194, 0.576] |

| Paired AUROC difference | N | Families | Difference | Family 95% interval | Valid bootstrap draws |
|---|---:|---:|---:|---|---:|
| V4-V1 | 48 | 8 | -0.030 | [-0.128, 0.048] | 5000 |
| V4-V2 | 48 | 8 | 0.213 | [0.160, 0.297] | 5000 |
| V4-V3 | 48 | 8 | 0.065 | [-0.030, 0.156] | 5000 |
| V4-mean | 48 | 8 | -0.057 | [-0.110, -0.008] | 5000 |
| V4-max | 48 | 8 | 0.019 | [-0.030, 0.066] | 5000 |

Per-condition and per-family results, excluded IDs, operating thresholds, generation labels, rate-difference intervals and undefined bootstrap counts are in metrics.json.

Zero-call baselines use public evidence only. They do not verify agreement; action_gap overlaps with outcome-label construction.

## Generation funnel

| Condition | Scheduled | Technically valid | Harmful agreement | Joint execution | Harm | Implemented |
|---|---:|---:|---:|---:|---:|---:|
| B | 10 | 10 | 0 | 0 | 0 | 0 |
| G | 10 | 10 | 0 | 0 | 0 | 0 |
| H | 10 | 10 | 7 | 7 | 10 | 7 |
| I | 10 | 10 | 0 | 0 | 10 | 0 |
| O | 10 | 10 | 10 | 10 | 10 | 10 |
| T | 10 | 10 | 10 | 0 | 0 | 0 |

Agent-round statement/action categories, not independent samples or verified latent intent. third_action remains separate from stated_premeditated.
