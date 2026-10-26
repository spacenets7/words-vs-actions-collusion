"""Verify/extract a fresh judge bundle, then run exact offline statistics replay."""
import subprocess,sys,tempfile,zipfile
from pathlib import Path
from verify_review import verify,ROOT

if __name__=='__main__':
 print('Verifying the review package and frozen configuration...',flush=True)
 result=verify();print(f"Verified {result['episodes']} episodes and {result['monitor_outputs']} monitor outputs.",flush=True)
 parent=ROOT/'tmp';parent.mkdir(exist_ok=True)
 folder=Path(tempfile.mkdtemp(prefix='judge-replay-',dir=parent)).resolve()
 with zipfile.ZipFile(ROOT/'review/reproducibility.zip') as z:
  for name in z.namelist():assert (folder/name).resolve().is_relative_to(folder),name
  z.extractall(folder)
 print('Fresh extraction:',folder,flush=True)
 subprocess.run([sys.executable,str(folder/'verify.py')],check=True,cwd=folder)
 print('Recomputing both targets and 5000-draw family bootstraps; allow several minutes. No model/API calls.',flush=True)
 subprocess.run([sys.executable,'-X','utf8',str(folder/'replay.py')],check=True,cwd=folder)
