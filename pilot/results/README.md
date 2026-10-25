# Evaluation scope

metrics.json and metrics.md preserve the frozen analysis output. Primary/attempt performance tables, condition breakdowns, family breakdowns and paired comparisons use held-out families 2001-2008 only (48 episodes). Thresholds use the 12 frozen development episodes in families 1001/1002. The descriptive generation_funnel and typology counts in these original files pool development plus held-out data (60 episodes, 10 per assigned condition). The report's Table 3 and submission/quality-checks.json give the separate held-out-only funnel (eight per condition).

Automatic labels remain provisional. There are 13 implemented-collusion positives (8 O, 5 H) and 35 negatives under the frozen event-based rule. Three assigned H cases are harmful but fail the agreement/implementation gate and are retained. Assigned condition is not the outcome label. No prompt/threshold tuning or scientific replacement was performed after test generation. Human reviews have not been completed.

The independent source/data exports replay the saved metrics exactly using replay.py, without model calls. See ../submission for the PDF draft, editable source, uncertainty figures, quality checks, cost summary and local bundle. These are local artifacts; nothing has been submitted or published.
