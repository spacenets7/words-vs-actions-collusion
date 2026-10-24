# Development iterations

## 24 October: funded development loop resumed
- User confirmed credits ready; funding enabled at reported $50, development cap still $20.
- Rechecking offline invariants, then trying 3B contract/allocation candidates before increasing model size.
- Held-out families remain untouched. No additional API provider is used.
- First funded launch stopped before the GPU entry point because Modal's console checkmark could not encode under Windows cp1252. Added explicit UTF-8 to child Python; no inference output was produced.
- UTF-8 retry exposed a packaging bug: SDK ignore paths are mount-relative, so a local is_file() test accidentally admitted the changing log. Replaced it with an exact cloud-source allowlist. Build stopped before inference; GPU ledger still empty.
- Root cause of the remaining log error was Modal's implicit entrypoint package mount, independent of the explicit filter. Disabled include_source and replaced recursive source discovery with five explicit local-file mounts. This also avoids walking the large local environment and cloned repositories.
- Image build then succeeded: CUDA/Python base (109.58 s), vLLM dependency layer (28.84 s), environment layer (12.37 s). These timings are not billing records.
- Modal rejected GPU registration: `Please add a payment method to use L4 GPU functions.` No GPU function, agent generation or monitor scoring started. User said they will add the payment method and notify this chat.
- Setup allowance $1.00 reserved conservatively; actual image-build/storage bill unreconciled. GPU inference $0, other API spend $0. No model winner selected and no held-out data touched.
- Offline regression suite now 12/12 passing. Source/image setup is saved so development can resume after GPU eligibility is enabled.

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

## Qwen2.5-3B-Instruct-contract
Started 2026-10-24 23:08:27 local time; development family 1001, 3 rounds.

## Qwen2.5-3B-Instruct-contract
Started 2026-10-24 23:09:31 local time; development family 1001, 3 rounds.

## Qwen2.5-3B-Instruct-contract
Started 2026-10-24 23:11:14 local time; development family 1001, 3 rounds.

## Qwen2.5-3B-Instruct-contract
Started 2026-10-24 23:12:58 local time; development family 1001, 3 rounds.
