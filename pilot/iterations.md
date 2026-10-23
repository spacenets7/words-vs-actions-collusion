# Development iterations

## Setup
- Read v2 Section 21 and audit pitfalls. Use own labels; reject invalid numeric actions; no imported upstream typology or TraceGuard weights.
- Local pinned clone chosen to reuse the already audited checkout, avoiding a redundant remote download. Source remains unchanged; runtime patches will live under patches/.
- System Python venv bootstrap and system Git clone failed on Windows subprocess permissions; trying bundled runtime.
- Paid inference calls: none. Modal spend: $0; other spend: $0.
