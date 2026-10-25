import json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'reproducibility'))
from pilot.analysis import analyze,write_report
read=lambda p:[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x]
eps=read(root/'data/public-trajectories.jsonl')
labels={x['episode_id']:x for x in read(root/'data/oracle-labels.jsonl')}
for e in eps:
 o=labels[e['episode_id']];e['oracle']={'condition':o['condition'],'typology':o['descriptive_typology']};e['labels']=o['automatic_labels']
scores={}
for x in read(root/'data/monitor-evidence-and-outputs.jsonl'):
 if x['output'] is not None:scores.setdefault(x['episode_id'],{})[x['view']]=x['output']
c=json.loads((root/'reproducibility/pilot/frozen/config.json').read_text())
m=analyze(eps,scores,c['development_families'])
(root/'replayed-metrics.json').write_text(json.dumps(m,indent=2))
write_report(m,root/'replayed-metrics.md')
expected=json.loads((root/'metrics.json').read_text())
assert m==expected,'Replayed metrics differ from saved output'
print('Exact metrics replay passed without model/API calls.')
