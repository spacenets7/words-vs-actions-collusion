import argparse
from pathlib import Path
from .core import load,save,canonical,digest

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    # Only final validation and scheduled test records: no screening runs or fixtures.
    files=[Path('pilot/frozen/development.json')]+[p for p in sorted(Path('pilot/runs').glob('test-*.json'))
        if not p.name.endswith(('.generation.json','.monitor.json'))]
    frozen=load('pilot/frozen/config.json')
    episodes={};scores={};config_hashes=set()
    for file in files:
        data=load(file)
        if data.get('scripted') or not data.get('remote_completed'):raise ValueError('Not completed model output')
        normalized=dict(data['config']);normalized['allow_test_execution']=False
        if digest(normalized)!=digest(frozen):raise ValueError('Result does not match frozen generation configuration: '+str(file))
        for e in data['episodes']:
            eid=e['episode_id']
            if eid in episodes and canonical(episodes[eid])!=canonical(e):raise ValueError('Conflicting episode')
            episodes[eid]=e;config_hashes.add(e['config_hash'])
        scores.update(data['scores'])
    if not episodes:raise ValueError('No actual validation/test records found')
    save(a.output,{'episodes':list(episodes.values()),'scores':scores,'files':[str(p) for p in files],
                   'note':'Generation config hashes can differ only by explicit test execution flag; inspect provenance.'})

if __name__=='__main__':main()
