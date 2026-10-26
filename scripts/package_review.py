"""Build the judge archive from unchanged saved data and current artifacts.

This is packaging, not experiment generation or recalibration. The historical
archive is read-only; all three exported JSONL files must stay byte-identical.
"""
import hashlib,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT/'review'
ORIGINAL_ARCHIVE_SHA='bc5c01665f8863934ba6cc0b46c17d8abe74f7752d3a451e71a41d61ab2584a2'
DATA_SHA={
 'data/public-trajectories.jsonl':'50bd552239ecdbde047362a18538c2d4668e2a4513a5202308c1196d2fd7ad25',
 'data/oracle-labels.jsonl':'1449d41d1c756554b9e8ddaa51602758b3cc06f8e3a9fe6ef6536557beedd71b',
 'data/monitor-evidence-and-outputs.jsonl':'034347d83bafbfc201284d185b0ab84bd33cb6be6ba4b002be27f9de6ac0f953',
}
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
 REVIEW.mkdir(exist_ok=True);figures=REVIEW/'figures';figures.mkdir(exist_ok=True)
 old=ROOT/'pilot/submission/local-reproducibility-bundle.zip'
 assert sha(old.read_bytes())==ORIGINAL_ARCHIVE_SHA,'Historical input archive changed'
 metrics=ROOT/'pilot/submission/metrics.json'
 assert sha(metrics.read_bytes())=='a05277e28f22e85b92dee50869707d3bd75a739ac5bb96f78b9a9098db0f6850'
 payload={}
 with zipfile.ZipFile(old) as source:
  for name,digest in DATA_SHA.items():
   data=source.read(name);assert sha(data)==digest;payload[name]=data
  payload['replay.py']=source.read('replay.py')
 result=(ROOT/'pilot/submission/metrics.md').read_text(encoding='utf-8')
 result=result.replace('Automatic event-based labels are provisional until two independent score-blind human reviews.','Outcomes use frozen event-based automatic labels. Agreement, execution and harm are separate; assigned condition is not the outcome.')
 (REVIEW/'RESULTS.md').write_text(result,encoding='utf-8',newline='\n')
 with zipfile.ZipFile(ROOT/'pilot/submission/final-report.docx') as document:
  for i,name in enumerate(['implementation-auroc','paired-comparisons','attempt-vs-implementation'],1):
   data=document.read(f'word/media/final-{i}.png');(figures/(name+'.png')).write_bytes(data);payload['figures/'+name+'.png']=data
 for target,source in {
   'report.pdf':'pilot/submission/final-report.pdf','report.docx':'pilot/submission/final-report.docx',
   'metrics.json':'pilot/submission/metrics.json','metrics.md':'review/RESULTS.md',
   'FORMULAS.md':'pilot/submission/FORMULAS.md','run-provenance.json':'pilot/submission/run-provenance.json',
   'cost-summary.json':'pilot/submission/cost-summary.json','authors.json':'pilot/submission/authors.json',
   'requirements.txt':'pilot/requirements-review.txt','data/DATA_CARD.md':'review/DATA_CARD.md',
   'NOTICE.md':'NOTICE.md','CITATION.cff':'CITATION.cff',
   'provenance/original-frozen-hashes.json':'pilot/frozen/hashes.json',
   'reproducibility/pilot/analysis.py':'pilot/analysis.py','reproducibility/pilot/core.py':'pilot/core.py',
   'reproducibility/pilot/__init__.py':'pilot/__init__.py',
   'reproducibility/pilot/patches/upstream.py':'pilot/patches/upstream.py',
   'reproducibility/pilot/frozen/config.json':'pilot/frozen/config.json',
   'reproducibility/pilot/frozen/calibration.json':'pilot/frozen/calibration.json',
 }.items():payload[target]=(ROOT/source).read_bytes()
 payload['README.md']=b'''# Track 2.2 judge reproducibility package

Read report.pdf first. This is the current Apart-template manuscript, not the
historical expanded report in the original local bundle. Dataset bytes, model
scores, outcome labels, thresholds and analysis code are unchanged.

Python 3.12 on a CPU:
  python -m pip install -r requirements.txt
  python verify.py
  python replay.py

The first check uses only the Python standard library. Full replay can take
several minutes: it recomputes 5000 whole-family bootstrap draws for both targets
and paired comparisons and requires exact equality with metrics.json. No model,
API key, Modal login, GPU or Docker is needed. The reference environment is
Windows/Python 3.12 with the pinned numerical package versions.

Data contain 12 development and 48 held-out episodes with 240 monitor records.
Read data/DATA_CARD.md before interpreting the operational automatic outcomes.
Private plans/messages and generation journals are absent. Oracle labels are
evaluation-only and must never be supplied as monitor evidence.

bundle-manifest.json verifies this archive's payload. The original complete
freeze manifest is retained in provenance/ for provenance only; this small
analysis archive omits complete-workspace development evidence/candidates.
Use the full GitHub checkout for the complete freeze and 23 component tests:
https://github.com/spacenets7/words-vs-actions-collusion
'''
 payload['verify.py']=b'''import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'bundle-manifest.json').read_text())
for name,expected in manifest.items():
 p=(root/name).resolve()
 assert p.is_relative_to(root),name
 assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==expected,name
read=lambda name:[json.loads(s) for s in (root/name).read_text().splitlines() if s]
assert len(read('data/public-trajectories.jsonl'))==60
assert len(read('data/monitor-evidence-and-outputs.jsonl'))==240
print('Bundle hashes verified: 60 episodes, 240 monitor records. No model/API calls.')
'''
 manifest={name:sha(data) for name,data in sorted(payload.items())}
 payload['bundle-manifest.json']=json.dumps(manifest,indent=2).encode()
 archive=REVIEW/'reproducibility.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for name,data in sorted(payload.items()):
   assert '__pycache__' not in name and not name.endswith('.pyc')
   info=zipfile.ZipInfo(name,date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,data)
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 files=['pilot/submission/final-report.pdf','pilot/submission/final-report.docx','pilot/submission/metrics.json',
        'pilot/submission/template-report-quality.json','pilot/submission/run-provenance.json',
        'pilot/frozen/config.json','pilot/frozen/calibration.json','pilot/frozen/hashes.json',
        'review/reproducibility.zip','review/DATA_CARD.md','review/RESULTS.md',
        'review/figures/implementation-auroc.png','review/figures/paired-comparisons.png',
        'review/figures/attempt-vs-implementation.png']
 record={'schema_version':1,'project':'Words Actions and Evidence in Collusion Detection',
         'date':'2026-10-26','repository':'https://github.com/spacenets7/words-vs-actions-collusion',
         'frozen_config_hash':'10e684f850295c7d8a29c06ee695cc56604908631c5c2e44fa1a9e3767205414',
         'files':{name:sha((ROOT/name).read_bytes()) for name in files},'original_dataset_exports':DATA_SHA,
         'original_archive_sha256':ORIGINAL_ARCHIVE_SHA,'model_api_calls':0}
 (REVIEW/'manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8',newline='\n')
 print('Built',archive,'with',len(payload),'files and unchanged JSONL exports.')

if __name__=='__main__':main()
