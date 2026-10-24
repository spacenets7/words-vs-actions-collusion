"""Read vendor billing; settle completed apps without resetting old reservations."""
import argparse
import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
from .core import load,save,budget_total

def settle(ledger,rows,finished,now):
    if any(e['state']=='reserved' for e in ledger['reservations']):
        raise ValueError('Wait for the active Modal command to finish before reconciling')
    grouped=defaultdict(list)
    for e in ledger['reservations']:
        if e.get('app_id'):grouped[e['app_id']].append(e)
    totals=defaultdict(Decimal)
    for row in rows:totals[row['object_id']]+=Decimal(row['cost'])
    closed_hour=now.replace(minute=0,second=0,microsecond=0).timestamp()
    if not rows:return []
    report_end=max(datetime.fromisoformat(r['interval_start']).replace(tzinfo=timezone.utc).timestamp()+3600 for r in rows)
    closed_hour=min(closed_hour,report_end)
    changes=[]
    for app_id,entries in grouped.items():
        if app_id not in totals or any(e['state']!='completed' for e in entries):continue
        # All calls in this app must have finished before the last closed hour,
        # plus a five-minute lag allowance. Recent/live apps retain reservations.
        ends=[finished.get(e.get('output')) for e in entries]
        if any(t is None or t+300>closed_hour for t in ends):continue
        if all('settled_billed_usd' in e for e in entries) and Decimal(str(sum(e['settled_billed_usd'] for e in entries)))==totals[app_id]:continue
        for i,e in enumerate(entries):
            e['settled_billed_usd']=float(totals[app_id]) if i==0 else 0
            e['settlement_note']='Full app total allocated once across its completed phases; original reservations retained.'
        changes.append({'app_id':app_id,'billed_usd':float(totals[app_id]),'phases':len(entries)})
    return changes

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',default='pilot/runs/billing-latest.json')
    p.add_argument('--use-existing-report',action='store_true');a=p.parse_args()
    ledger=load('pilot/spend.json')
    if any(e['state']=='reserved' for e in ledger['reservations']):raise ValueError('A Modal phase is still active; do not reconcile yet')
    if not a.use_existing_report:
        result=subprocess.run([sys.executable,'-X','utf8','-m','modal','billing','report','--start','2026-10-23',
            '--resolution','h','--show-resources','--json'],check=True,capture_output=True,encoding='utf-8')
        Path(a.report).parent.mkdir(parents=True,exist_ok=True);Path(a.report).write_text(result.stdout,encoding='utf-8')
    # Recover IDs from older CLI logs that predate explicit app_id ledger fields.
    mapping={}
    for path in [Path('pilot/dev-loop-ready.log'),Path('pilot/protocol2.log'),Path('pilot/protocol3.log'),Path('pilot/protocol4.log')]:
        if not path.exists():continue
        text=path.read_text(encoding='utf-8',errors='replace')
        for match in re.finditer(r'Saved development/test output:\s*(pilot/runs/\S+\.json)',text):
            prior=re.findall(r'https://modal.com/apps/[^/]+/[^/\s]+/(ap-[A-Za-z0-9]+)',text[:match.start()])
            if prior:mapping[match.group(1)]=prior[-1]
    finished={}
    for e in ledger['reservations']:
        out=e.get('output')
        if not e.get('app_id') and out in mapping:e['app_id']=mapping[out]
        if out and Path(out).exists():finished[out]=Path(out).stat().st_mtime
    rows=load(a.report);now=datetime.now(timezone.utc)
    changes=settle(ledger,rows,finished,now)
    report_hash=hashlib.sha256(Path(a.report).read_bytes()).hexdigest()
    ledger.setdefault('billing_reconciliations',[]).append({'utc':now.isoformat(),'report':a.report,
        'report_sha256':report_hash,'settled_apps':changes,'committed_usd':budget_total(ledger),
        'note':'Only completed apps whose full intervals have closed; current-hour charges remain reserved.'})
    save('pilot/spend.json',ledger)
    from .progress import record
    record(f'Reconciled {len(changes)} completed app(s) from authenticated vendor billing. Original reservations retained; current budget envelope ${budget_total(ledger):.4f}.')
    print('Vendor-reconciled completed apps:',changes,'; committed budget:',round(budget_total(ledger),4))

if __name__=='__main__':main()
