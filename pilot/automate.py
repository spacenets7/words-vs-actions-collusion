"""Local supervisor around the immutable experiment; never changes its design."""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'pilot' / 'automation-state.json'
LOCK = ROOT / 'pilot' / '.automation.lock'


def now():
    return datetime.now(timezone.utc).isoformat()


def update(stage, **extra):
    from .core import save, load
    prior = load(STATE) if STATE.exists() else {}
    save(STATE, {**prior, 'stage': stage, 'updated_utc': now(), **extra})


def banner(message):
    path = ROOT / 'pilot' / 'STATUS.md'
    text = path.read_text(encoding='utf-8')
    if '<!-- automation:start -->' in text:
        start = text.index('<!-- automation:start -->')
        end = text.index('<!-- automation:end -->', start) + len('<!-- automation:end -->')
        text = text[:start] + text[end:].lstrip('\n')
    first, rest = text.split('\n', 1)
    note = f'\n\n<!-- automation:start -->\n## Live automated execution\n\n{message}\n\nUpdated {now()}. Earlier readiness statements below describe the pre-execution freeze.\n<!-- automation:end -->\n\n'
    path.write_text(first + note + rest.lstrip('\n'), encoding='utf-8', newline='\n')


def run():
    os.chdir(ROOT)
    # Atomic lock prevents duplicate paid runs. A stale lock requires inspecting
    # the recorded PID before explicit removal; it is never removed on a guess.
    with LOCK.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps({'pid': os.getpid(), 'started_utc': now()}))
    try:
        if sys.platform == 'win32':
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
        update('preflight', pid=os.getpid(), started_utc=now(),
               authorization='User requested all remaining automation and authorized extra Modal credit if needed.',
               expected_test_families=list(range(2001, 2009)),
               frozen_manifest_sha256=hashlib.sha256(Path('pilot/frozen/hashes.json').read_bytes()).hexdigest(),
               human_review='Pending; no automated or agent check is an independent human review.')
        subprocess.run([sys.executable, '-X', 'utf8', '-m', 'pilot.cli', 'verify-freeze'], check=True)
        shell = shutil.which('pwsh') or shutil.which('powershell')
        if not shell:
            raise RuntimeError('PowerShell is required for the frozen full-design entry point')
        update('running_frozen_design')
        banner('The user authorized held-out execution. The frozen full design is running automatically, followed by checks, analysis and a local report/package draft. Independent human labels and author details remain pending. Prompts, model revisions and development thresholds stay frozen; the $20 admission cap remains active.')
        subprocess.run([shell, '-NoProfile', '-File', 'pilot/RUN_FULL_DESIGN.ps1'], check=True)
        update('reconciling')
        subprocess.run([sys.executable, '-X', 'utf8', '-m', 'pilot.reconcile'], check=True)
        update('building_deliverables')
        from .deliver import build
        result = build()
        subprocess.run([sys.executable, '-X', 'utf8', '-m', 'pilot.cli', 'verify-freeze'], check=True)
        update('complete_provisional', completed_utc=now(), deliverables=result)
        banner('Automated execution, integrity checks, analysis and the local report/package draft are complete. See pilot/submission/README.md and pilot/results. Results use provisional automatic labels. Independent human review, authorship details, official-template check and final submission remain human tasks. No external submission or publication was made.')
        print('AUTOMATION COMPLETE:', json.dumps(result), flush=True)
    except BaseException as exc:
        update('stopped', stopped_utc=now(), error_type=type(exc).__name__, error=str(exc)[:1200])
        banner('Automation stopped safely. Inspect pilot/automation-state.json and pilot/automation.stderr.log / automation.stdout.log. Completed outputs and reservations are retained; no budget reset or design retuning was performed.')
        raise
    finally:
        if sys.platform == 'win32':
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        LOCK.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['run', 'status', 'finish'])
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.command == 'run':
        run()
    elif args.command == 'finish':
        from .deliver import build
        print(json.dumps(build(), indent=2))
    else:
        from .core import load
        state = load(STATE) if STATE.exists() else {'stage': 'not_started'}
        state['completed_family_files'] = [f for f in range(2001, 2009)
            if Path(f'pilot/runs/test-{f}-all.json').exists()]
        print(json.dumps(state, indent=2))


if __name__ == '__main__':
    main()
