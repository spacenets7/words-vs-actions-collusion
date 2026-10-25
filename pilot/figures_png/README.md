# Track 2.2 result graphs

Five 3500 x 2250 PNGs rasterized from vector ReportLab figures at300 dpi. Source: saved held-out metrics and quality checks; no new model calls, recomputation of scores, label changes or threshold changes. All estimates use48 held-out episodes across8 families. Automatic labels await independent human adjudication.

1. 01_monitor_auroc: all nine methods and95% family-bootstrap intervals.
2. 02_paired_auroc_differences: V4 minus prespecified comparators, family intervals and per-family dots.
3. 03_condition_flag_rates: flagged/eligible counts at frozen thresholds. These are flag rates, not accuracies; H has a mixture of outcomes.
4. 04_generation_outcomes: distinct unauthorized agreement, agreed-plan execution, harm and implemented-collusion counts.
5. 05_attempt_vs_implementation: separate attempt and implemented-outcome targets, not a treatment-effect comparison.

No consistent structured-hybrid advantage is established. The three H implementation-gate failures are retained. Do not interpret overlapping intervals as proof of equivalence; no multiplicity-adjusted significance claim is made. Zero-call action-gap baseline overlaps outcome construction.

Regenerate locally: pilot/env/Scripts/python.exe -m pilot.plot_results_png
Source metrics JSON remains unchanged. See ../AUDIT_IMPLEMENTATION_MAP.md for how the paper audit informed the project.
