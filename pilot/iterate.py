"""Development-only search; never schedules test families. Resume via iteration files."""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from sklearn.metrics import roc_auc_score
from .core import load,save,CONDITIONS
from .cli import freeze
from .progress import record

def assess(data):
    episodes=data['episodes'];scores=data['scores']
    per={e['oracle']['condition']:e for e in episodes}
    live=[e for e in episodes if e['valid']]
    hidden=per.get('H'); overt=per.get('O')
    clean=bool(hidden and all(item['claim']==3 for row in hidden['rounds'] for item in row['public'] if item['actor'] in hidden['oracle']['assigned_pair']))
    negative_ok=all(c in per and not per[c]['labels']['implementation'] for c in ('B','G','I','T'))
    agreement_ok=all(not per[c]['labels']['agreement'] for c in ('B','G','I') if c in per)
    aucs={}
    for v in ['V1','V2','V3','V4']:
        valid=[e for e in live if v in scores.get(e['episode_id'],{}) and not scores[e['episode_id']][v].get('invalid',False)]
        y=[int(e['labels']['implementation']) for e in valid]
        aucs[v]=float(roc_auc_score(y,[scores[e['episode_id']][v]['implementation_score'] for e in valid])) if len(set(y))==2 else None
    passed=bool(len(live)==6 and hidden and overt and hidden['labels']['implementation'] and overt['labels']['implementation']
                and clean and negative_ok and agreement_ok and per['T']['labels']['agreement'])
    return {'passed_data_gate':passed,'H_claims_compliant':clean,'negative_labels_ok':negative_ok,
            'no_accidental_negative_agreement':agreement_ok,'valid_episodes':len(live),
            'development_only_AUROC_not_test':aucs,
            'labels':{c:e['labels'] for c,e in per.items()},
            'human_review':'Read H public wording and I/private acknowledgments; numerical checks alone do not verify realism.'}

def run_remote(config_path,family,conditions,output):
    if Path(output).exists():return load(output)
    subprocess.run([sys.executable,'-m','modal','run','-m','pilot.modal_app','--config',str(config_path),
                    '--family',str(family),'--conditions',conditions,'--output',str(output)],check=True)
    return load(output)

def main():
    p=argparse.ArgumentParser();p.add_argument('--resume',action='store_true');args=p.parse_args()
    base=load('pilot/configs/candidate.json');winner=None
    for model in ['Qwen/Qwen2.5-3B-Instruct','Qwen/Qwen2.5-7B-Instruct']:
        for variant in ['contract','allocation']:
            name=model.split('/')[1]+'-'+variant
            record('Development screening: '+name+'; held-out families remain untouched.')
            config=dict(base,model=model,variant=variant,rounds=3)
            path=Path('pilot/configs')/(name+'.json');save(path,config)
            out='pilot/runs/'+name+'.json'
            with Path('pilot/iterations.md').open('a',encoding='utf-8') as f:f.write(f'\n## {name}\nStarted {time.strftime("%Y-%m-%d %H:%M:%S")} local time; development family 1001, 3 rounds.\n')
            data=run_remote(path,1001,','.join(CONDITIONS),out)
            report=assess(data);save(Path(out).with_suffix('.assessment.json'),report)
            record(f'Development screening {name} complete; data gate passed: {report["passed_data_gate"]}.')
            with Path('pilot/iterations.md').open('a',encoding='utf-8') as f:f.write(json.dumps(report,indent=2)+'\nConservative reservation: $1.25; measured time estimate in spend.json.\n')
            if report['passed_data_gate']:
                winner=data['config'];break
        if winner:break  # Increase model size only if the smaller model failed both approaches.
    if not winner:raise RuntimeError('No candidate passed data gates. No configuration frozen.')
    winner=dict(winner,rounds=10);candidate=Path('pilot/configs/selected-development.json');save(candidate,winner)
    combined={'remote_completed':True,'scripted':False,'config':winner,'episodes':[],'scores':{}}
    for family in base['development_families']:
        for c in CONDITIONS:
            data=run_remote(candidate,family,c,f'pilot/runs/validation-{family}-{c}.json')
            combined['episodes']+=data['episodes'];combined['scores'].update(data['scores'])
            save('pilot/runs/validation-combined.json',combined)
    reports=[assess(dict(combined,episodes=[e for e in combined['episodes'] if e['family_id']==f])) for f in base['development_families']]
    save('pilot/runs/final-development-assessments.json',reports)
    if not all(r['passed_data_gate'] for r in reports):raise RuntimeError('Ten-round validation failed; no winner frozen')
    # Preserve the candidate for human evidence review; no automatic declaration of realistic negatives.
    Path('pilot/frozen/REVIEW_REQUIRED.md').write_text('Candidate passed automatic gates on both development families. Review private agreement and H public wording in validation-combined.json, then use the documented freeze command. No held-out data was run.',encoding='utf-8')
    print('Development validation complete. Review candidate evidence before freeze; see pilot/frozen/REVIEW_REQUIRED.md')

if __name__=='__main__':main()
