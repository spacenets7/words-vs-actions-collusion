# Track 2.2 pilot status

Updated 25 October 2026 (Asia/Calcutta). GPU access works. The 3B protocol-3 agent setup passes all six three-round generation gates: O/H execute harmful agreements, H public text is clean, I independently causes harm without agreement, and T talks but executes policy. The original monitor and example-anchored monitor failed. A reason-first monitor re-score on the same cached development trajectories is running. No winning configuration frozen yet; ten-round validation is still required. Held-out families generated/inspected: ZERO.

## Works
- Public Goods pipeline: five agents, private pair channel, six conditions, strict actions, T controller, own agreement/execution/harm labels.
- Upstream pinned to fd11aca351e52c65c929e1a7d46d9f087f237adf; adapter in pilot/patches, upstream unchanged. Section 21 overrides Sections 3-4 of the copied spec.
- Four allowlisted monitor views, all-ten-pair report, persistent Modal request cache, view-specific metrics, exact rate intervals, paired family bootstrap.
- Thirteen offline tests passed; arithmetic and private-evidence leak tests included.
- Modal L4 serves Qwen2.5 3B and 7B through vLLM 0.21.0. Revisions and exact requests/responses saved locally and in authenticated Modal Volume.

## Current limitations
- Original prompt variants had malformed JSON, H public disclosures, incomplete agreement acknowledgments, and weak H execution. These runs are retained as failed iterations.
- Protocol 2 adds formatting constraints without choosing actions, clearer stage instructions, and a stricter I hard-negative check. Final ten-round validation remains pending.
- Same open model currently generates and monitors in separate requests. Monitor scores are not ground truth. Two independent human label reviews are still required for reportable research.

## Spend
- First four completed batches: measured-resource estimate $0.5845, not a Modal invoice.
- Reservation ceiling before protocol 2: $6.00, including $1 setup/storage allowance and four $1.25 reservations.
- Future batches reserve $0.75 each: above estimated $0.511 for the full 30-minute function timeout. Earlier reservations stay unchanged; stop before $20 accumulated reservations.
- Exact current numbers: pilot/spend.json and progress entries below. External API spend $0. Authenticated billing reconciliation: pilot/billing-report-summary.json attributes $0.64742364 to this app through reported closed intervals (17:00-19:00 UTC); subsequent runs are not yet in that report. Live account snapshot showed $0.77 usage, credits covering it, $0 cash charges. These are partial/delayed totals, not a final invoice.

## Commands / human needs
- Offline checks: `.\pilot\env\Scripts\python.exe -X utf8 -m unittest discover -s pilot/tests -v`.
- Current trial log: pilot/protocol4.log. Candidate: pilot/configs/Qwen2.5-3B-Instruct-protocol4.json.
- Validation runner: `python -m pilot.iterate --candidate pilot/configs/Qwen2.5-3B-Instruct-protocol4.json`; it reuses the completed screen, checks gates, then validates ten rounds on both development families. Do not start concurrently with the current screen.
- Held-out one-command runner: `.\pilot\RUN_FULL_DESIGN.ps1` (syntax checked, never executed); step-by-step commands in pilot/README.md; DO NOT run before a validated freeze. This build never executes held-out families.
- No credential or payment action currently needed.

## Progress history (UTC timestamps)

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

### Progress 2026-10-24T18:44:38.866723+00:00
Development screening: Qwen2.5-3B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $1.00; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:44:51.586799+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-3B-Instruct-contract.json.
Modal conservative reserved ceiling: $2.25; completed-runtime estimate: $0.0000. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:52:35.522314+00:00
Batch state: completed; output pilot/runs/Qwen2.5-3B-Instruct-contract.json.
Modal conservative reserved ceiling: $2.25; completed-runtime estimate: $0.1174. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:52:41.244351+00:00
Development screening Qwen2.5-3B-Instruct-contract complete; data gate passed: False.
Modal conservative reserved ceiling: $2.25; completed-runtime estimate: $0.1174. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:52:41.254098+00:00
Development screening: Qwen2.5-3B-Instruct-allocation; held-out families remain untouched.
Modal conservative reserved ceiling: $2.25; completed-runtime estimate: $0.1174. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:52:50.046551+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-3B-Instruct-allocation.json.
Modal conservative reserved ceiling: $3.50; completed-runtime estimate: $0.1174. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:57:29.148021+00:00
Batch state: completed; output pilot/runs/Qwen2.5-3B-Instruct-allocation.json.
Modal conservative reserved ceiling: $3.50; completed-runtime estimate: $0.1893. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:57:34.419420+00:00
Development screening Qwen2.5-3B-Instruct-allocation complete; data gate passed: False.
Modal conservative reserved ceiling: $3.50; completed-runtime estimate: $0.1893. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:57:34.421315+00:00
Development screening: Qwen2.5-7B-Instruct-contract; held-out families remain untouched.
Modal conservative reserved ceiling: $3.50; completed-runtime estimate: $0.1893. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T18:57:43.421653+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-7B-Instruct-contract.json.
Modal conservative reserved ceiling: $4.75; completed-runtime estimate: $0.1893. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:14:21.705365+00:00
Batch state: completed; output pilot/runs/Qwen2.5-7B-Instruct-contract.json.
Modal conservative reserved ceiling: $4.75; completed-runtime estimate: $0.4659. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:14:27.799443+00:00
Development screening Qwen2.5-7B-Instruct-contract complete; data gate passed: False.
Modal conservative reserved ceiling: $4.75; completed-runtime estimate: $0.4659. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:14:27.803442+00:00
Development screening: Qwen2.5-7B-Instruct-allocation; held-out families remain untouched.
Modal conservative reserved ceiling: $4.75; completed-runtime estimate: $0.4659. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:14:40.241704+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-7B-Instruct-allocation.json.
Modal conservative reserved ceiling: $6.00; completed-runtime estimate: $0.4659. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:22:04.300347+00:00
Batch state: completed; output pilot/runs/Qwen2.5-7B-Instruct-allocation.json.
Modal conservative reserved ceiling: $6.00; completed-runtime estimate: $0.5845. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T19:22:10.119491+00:00
Development screening Qwen2.5-7B-Instruct-allocation complete; data gate passed: False.
Modal conservative reserved ceiling: $6.00; completed-runtime estimate: $0.5845. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:37:23.579419+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-3B-Instruct-protocol2.json.
Modal conservative reserved ceiling: $6.75; completed-runtime estimate: $0.5845. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:39:07.681014+00:00
Initial four real screens failed. Testing protocol 2 on 3B with JSON-schema decoding and clearer stage instructions. Earlier data retained; no held-out generation.
Modal conservative reserved ceiling: $6.75; completed-runtime estimate: $0.5845. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:44:57.730180+00:00
Batch state: completed; output pilot/runs/Qwen2.5-3B-Instruct-protocol2.json.
Modal conservative reserved ceiling: $6.75; completed-runtime estimate: $0.7045. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:46:45.521528+00:00
Protocol 2 valid 6/6 and successful O/H; failed I hard-negative and T agreement gates. Starting protocol 3 on 3B; no held-out data.
Modal conservative reserved ceiling: $6.75; completed-runtime estimate: $0.7045. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:46:54.272022+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-3B-Instruct-protocol3.json.
Modal conservative reserved ceiling: $7.50; completed-runtime estimate: $0.7045. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:49:54.456958+00:00
Modal Usage & Billing read-only check: account usage $0.77, credits applied $0.77, cash charges $0.00, account credits $79.23. Live display is delayed/internally asynchronous; snapshot saved, final reconciliation pending.
Modal conservative reserved ceiling: $7.50; completed-runtime estimate: $0.7045. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:54:27.914543+00:00
Batch state: completed; output pilot/runs/Qwen2.5-3B-Instruct-protocol3.json.
Modal conservative reserved ceiling: $7.50; completed-runtime estimate: $0.8234. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:57:23.745970+00:00
Protocol 3 passed generation gates but monitor AUROC failed. Re-scoring same development trajectories with reason-first monitor and final deterministic tables; no larger agent model and no held-out data.
Modal conservative reserved ceiling: $7.50; completed-runtime estimate: $0.8234. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T22:57:32.259696+00:00
Reserved development/test batch for family 1001, conditions ['B', 'G', 'I', 'T', 'O', 'H'], output pilot/runs/Qwen2.5-3B-Instruct-protocol4.json.
Modal conservative reserved ceiling: $8.25; completed-runtime estimate: $0.8234. Actual billed usage requires dashboard reconciliation. External API spend: $0.

### Progress 2026-10-24T23:03:01.328244+00:00
Batch state: completed; output pilot/runs/Qwen2.5-3B-Instruct-protocol4.json.
Modal conservative reserved ceiling: $8.25; completed-runtime estimate: $0.9092. Actual billed usage requires dashboard reconciliation. External API spend: $0.
