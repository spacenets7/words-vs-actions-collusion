"""Append concise recoverable progress without recording credentials."""
from pathlib import Path
from datetime import datetime,timezone
from .core import load

def require_funding(path='pilot/funding.json'):
    funding=load(path)
    if not funding['compute_enabled']:
        raise RuntimeError('GPU runs paused: waiting for the reported Modal credits to arrive.')
    if funding['reported_credit_usd']<.75:
        raise RuntimeError('Available credit is below the conservative $0.75 batch reservation.')
    return funding

def record(message):
    ledger=load('pilot/spend.json') if Path('pilot/spend.json').exists() else {'reservations':[]}
    reserved=sum(e['reserved_usd'] for e in ledger['reservations'])
    estimate=sum(e.get('measured_estimate_usd',0) for e in ledger['reservations'])
    note=(f'\n### Progress {datetime.now(timezone.utc).isoformat()}\n{message}\n'
          f'Modal conservative reserved ceiling: ${reserved:.2f}; completed-runtime estimate: ${estimate:.4f}. '
          'Actual billed usage requires dashboard reconciliation. External API spend: $0.\n')
    with Path('pilot/STATUS.md').open('a',encoding='utf-8') as f:f.write(note)
