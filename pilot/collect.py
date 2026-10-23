import argparse
from pathlib import Path
from .core import load,save,canonical

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    # Only final validation and scheduled test records: no screening runs or fixtures.
    files=sorted(Path('pilot/runs').glob('validation-*-?.json'))+sorted(Path('pilot/runs').glob('test-*-?.json'))
    episodes={};scores={};config_hashes=set()
    for file in files:
        data=load(file)
        if data.get('scripted') or not data.get('remote_completed'):raise ValueError('Not completed model output')
        for e in data['episodes']:
            eid=e['episode_id']
            if eid in episodes and canonical(episodes[eid])!=canonical(e):raise ValueError('Conflicting episode')
            episodes[eid]=e;config_hashes.add(e['config_hash'])
        scores.update(data['scores'])
    if not episodes:raise ValueError('No actual validation/test records found')
    save(a.output,{'episodes':list(episodes.values()),'scores':scores,'files':[str(p) for p in files],
                   'note':'Generation config hashes can differ only by explicit test execution flag; inspect provenance.'})

if __name__=='__main__':main()
