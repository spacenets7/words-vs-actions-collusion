# Development iterations

## Setup
- Read v2 Section 21 and audit pitfalls. Use own labels; reject invalid numeric actions; no imported upstream typology or TraceGuard weights.
- Local pinned clone chosen to reuse the already audited checkout, avoiding a redundant remote download. Source remains unchanged; runtime patches will live under patches/.
- System Python venv bootstrap and system Git clone failed on Windows subprocess permissions; trying bundled runtime.
- Paid inference calls: none. Modal spend: $0; other spend: $0.

## Offline architecture and first validation
- Used a thin controller rather than modify both upstream queued/nonqueued paths. Runtime adapter in patches/ loads actual build_game_params without importing credential settings; arithmetic compared against PublicGoodsGame.
- Removed automatic upstream judge/reflection and typology. Added strict validation, separate oracle, typed requests, four views and all-ten-pair table.
- First eight tests passed after correcting floating-point evaluation order and using workspace-local temporary files. Added controller/monitor round-trip and malformed-response tests.
- Smoke created 18 scripted three-round fixtures / 72 views. These are not empirical pilot data and cannot select a frozen model.
- Installed Modal 1.6.2 and local statistics dependencies. Windows setup/commit required escalated filesystem/process access; succeeded.

## Modal connection probe
- Attempted development-only O/H invocation on family 1001 with candidate config.
- Result: `Token missing. Could not authenticate client.` No remote GPU batch started, no model revision resolved, no generation or monitor calls ran.
- Actual initiated Modal spend $0; other API spend $0; reserved spend $0 (entry point not reached).
- Waiting for local Modal authentication. Planned search tries 3B with contract vs allocation prompts first, increasing to 7B only if both small-model approaches fail.

## Authentication recheck and funding hold
- Read-only `modal app list --json` succeeded (zero apps returned). Authentication works.
- User reports only $1 credit currently, with $50 expected in 6-7 hours.
- No GPU launched. Added funding gate to search and single-batch entry point; it remains disabled until credits are confirmed.
- Modal compute spend $0; other API spend $0. No held-out data touched.
