"""Read-only integrity/coverage checks for judges; no model or network calls."""
import hashlib,json,re,zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote,urlsplit
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
STATEMENT='We used GPT-6.1 to brainstorm approaches and help draft sections, and GPT Astra for assistance in building out notebooks. Numerical results were checked through independent payoff calculations, automated tests and exact offline replay.'
def sha(data):return hashlib.sha256(data).hexdigest()
def rows(data):return [json.loads(s) for s in data.decode('utf-8').splitlines() if s]
def keys(value):
 if isinstance(value,dict):
  for k,v in value.items():yield k;yield from keys(v)
 elif isinstance(value,list):
  for v in value:yield from keys(v)

def verify():
 manifest=json.loads((ROOT/'review/manifest.json').read_text())
 for name,expected in manifest['files'].items():
  path=(ROOT/name).resolve();assert path.is_relative_to(ROOT),name
  assert path.is_file() and sha(path.read_bytes())==expected,name
 original=json.loads((ROOT/'pilot/frozen/hashes.json').read_text())
 for name,expected in original.items():assert sha((ROOT/name).read_bytes())==expected,'Changed original freeze: '+name
 config=json.loads((ROOT/'pilot/frozen/config.json').read_text())
 digest=sha(json.dumps(config,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode())
 assert digest==manifest['frozen_config_hash']
 archive=ROOT/'review/reproducibility.zip'
 with zipfile.ZipFile(archive) as z:
  names=set(z.namelist());assert z.testzip() is None
  assert not any('__pycache__' in n or n.endswith('.pyc') or Path(n).name in ['.env','.modal.toml','development.json'] for n in names)
  inside=json.loads(z.read('bundle-manifest.json'));assert names==set(inside)|{'bundle-manifest.json'}
  required={'reproducibility/pilot/analysis.py','reproducibility/pilot/core.py',
            'reproducibility/pilot/__init__.py','reproducibility/pilot/patches/upstream.py',
            'reproducibility/pilot/frozen/config.json','replay.py','verify.py'}
  assert required<=names,'Incomplete portable replay dependencies'
  for name,expected in inside.items():assert sha(z.read(name))==expected,name
  for name,expected in manifest['original_dataset_exports'].items():assert sha(z.read(name))==expected,name
  assert z.read('report.pdf')==(ROOT/'pilot/submission/final-report.pdf').read_bytes()
  assert z.read('metrics.json')==(ROOT/'pilot/submission/metrics.json').read_bytes()
  public=rows(z.read('data/public-trajectories.jsonl'));oracle=rows(z.read('data/oracle-labels.jsonl'));monitor=rows(z.read('data/monitor-evidence-and-outputs.jsonl'))
 assert len(public)==len(oracle)==60 and len(monitor)==240
 ids={e['episode_id'] for e in public};assert len(ids)==60
 labels={e['episode_id']:e for e in oracle};assert set(labels)==ids
 dev=set(config['development_families']);test=set(config['test_families'])
 assert {e['family_id'] for e in public}==dev|test
 assert sum(e['family_id'] in dev for e in public)==12
 heldout=[e for e in public if e['family_id'] in test];assert len(heldout)==48
 assert all(e['valid'] and len(e['rounds'])==10 for e in public)
 assert Counter(labels[e['episode_id']]['condition'] for e in heldout)==dict.fromkeys(['B','G','I','T','O','H'],8)
 positives=sum(bool(labels[e['episode_id']]['automatic_labels']['implementation']) for e in heldout);assert positives==13
 assert sum(bool(labels[e['episode_id']]['automatic_labels']['agreement']) for e in heldout)==21
 forbidden={'oracle','private','plans','own_plan','assigned_pair','condition','labels'}
 for e in public:
  assert set(e)=={'episode_id','family_id','config_hash','valid','rounds'}
  assert not forbidden.intersection(keys(e)),e['episode_id']
 seen=set()
 for record in monitor:
  identity=(record['episode_id'],record['view']);assert identity not in seen;seen.add(identity)
  assert record['episode_id'] in ids and record['view'] in ['V1','V2','V3','V4']
  assert record['output'] is not None and not record['output'].get('invalid',False)
  assert not forbidden.intersection(keys(record['evidence'])),identity
 assert seen=={(e,v) for e in ids for v in ['V1','V2','V3','V4']}
 metrics=json.loads((ROOT/'pilot/submission/metrics.json').read_text());cal=json.loads((ROOT/'pilot/frozen/calibration.json').read_text())
 for key,block in [('primary',metrics),('attempt',metrics['attempt_detection'])]:
  for view,r in cal[key].items():assert block['views'][view]['threshold']==r['threshold']
 for view in ['V1','V2','V3','V4']:assert metrics['views'][view]['n']==48 and not metrics['views'][view]['excluded_test_ids']
 reader=PdfReader(ROOT/'pilot/submission/final-report.pdf');texts=[p.extract_text() or '' for p in reader.pages]
 assert len(texts)==13 and next(i for i,t in enumerate(texts) if t.strip().startswith('References'))==6
 pdftext=' '.join('\n'.join(texts).split());assert pdftext.split('LLM Usage Statement ',1)[1].strip()==STATEMENT
 assert '(private; access requires authorization)' not in pdftext
 assert not re.search(r'human review|adjudicat|pending|provisional',pdftext,re.I)
 # Validate the canonical review navigation, not historical source-audit links to omitted inputs.
 for name in ['README.md','JUDGES.md','REPRODUCIBILITY.md','NOTICE.md','review/DATA_CARD.md']:
  source=ROOT/name
  for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',source.read_text(encoding='utf-8')):
   if urlsplit(target).scheme or target.startswith('#'):continue
   path=(source.parent/unquote(target.split('#')[0])).resolve();assert path.exists(),f'{name}: broken link {target}'
 return {'original_frozen_files_verified':len(original),'review_files_verified':len(manifest['files']),
         'episodes':60,'development_episodes':12,'held_out_episodes':48,'monitor_outputs':240,
         'held_out_implementation_positives':13,'held_out_attempt_positives':21,
         'monitor_private_key_isolation':'passed','unchanged_thresholds':'passed',
         'pdf_pages':13,'main_text_pages':6,'exact_llm_statement':'passed','model_api_calls':0}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
