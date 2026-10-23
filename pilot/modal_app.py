"""Ephemeral, authenticated Modal RPC batch. No public endpoint or embedded secrets.

Development command: python -m modal run -m pilot.modal_app --config ...
Each invocation has a 30-minute GPU timeout, one replica, no platform retries.
Local ledger reserves $1.25 before each trial (above a full L4/2CPU/16GiB timeout).
Do not change the hardware without updating the reservation and budget logic.
"""
import time
from pathlib import Path
import modal
from .core import Cached, generate_episode, score_episode, load, save, digest, CONDITIONS

app=modal.App('collusion-track22-pilot')
state=modal.Volume.from_name('collusion-track22-pilot-state',create_if_missing=True)
def exclude_upload(path):
    # Explicitly exclude environments, credentials, clones, results and oracle data.
    return path.name.startswith('.') or any(p in {'env','.venv','repos','runs','cache','.git','tests','frozen','configs','__pycache__'} for p in path.parts) or (path.is_file() and path.suffix!='.py')
image=(modal.Image.from_registry('nvidia/cuda:12.9.0-devel-ubuntu22.04',add_python='3.12')
       .entrypoint([]).uv_pip_install('vllm==0.21.0')
       .env({'HF_HOME':'/state/hf','VLLM_CACHE_ROOT':'/state/vllm'})
       .add_local_python_source('pilot',ignore=exclude_upload))

@app.function(image=image,gpu='L4',cpu=2,memory=16384,timeout=1800,
              max_containers=1,scaledown_window=2,retries=0,volumes={'/state':state})
def batch(config,families,conditions):
    from huggingface_hub import model_info
    from vllm import LLM,SamplingParams
    import json
    started=time.monotonic()
    revision=config.get('revision') or model_info(config['model']).sha
    config=dict(config,revision=revision)
    save(Path('/state/manifests')/(digest(config)+'.json'),config);state.commit()
    llm=LLM(model=config['model'],revision=revision,dtype='bfloat16',
            max_model_len=config['context_limit'],gpu_memory_utilization=.90,
            max_num_seqs=2,trust_remote_code=False,enforce_eager=True)
    state.commit()
    tokenizer=llm.get_tokenizer(); journal=[];calls={}
    cache_dir=Path('/state/calls');cache_dir.mkdir(exist_ok=True)
    def complete(req):
        key=digest([config['model'],revision,req])
        if key in calls:return calls[key]
        cached=cache_dir/(key+'.json')
        if cached.exists():
            item=load(cached);journal.append(dict(item,cache_hit=True));calls[key]=item['response'];return item['response']
        text=tokenizer.apply_chat_template([{'role':'system','content':req['system']},
              {'role':'user','content':req['user']}],tokenize=False,add_generation_prompt=True)
        prompt_tokens=len(tokenizer.encode(text,add_special_tokens=False))
        if prompt_tokens+req['max_tokens']>config['context_limit']:
            raise ValueError('Context overflow: no silent truncation')
        params=SamplingParams(temperature=req['temperature'],max_tokens=req['max_tokens'],seed=req['seed'])
        t=time.monotonic();result=llm.generate([text],params,use_tqdm=False)[0]
        answer=result.outputs[0].text.strip();calls[key]=answer
        # Exact evidence logged, never credentials; no ambient environment serialized.
        journal.append({'key':key,'request':req,'response':answer,'input_tokens':prompt_tokens,
                        'output_tokens':len(result.outputs[0].token_ids),'seconds':time.monotonic()-t})
        save(cached,journal[-1])
        if len(journal)%17==0:state.commit()
        return answer
    episodes=[];scores={}
    for family in families:
        for condition in conditions:
            e=generate_episode(complete,config,family,condition)
            episodes.append(e)
            if e['valid']:scores[e['episode_id']]=score_episode(complete,e,config)
            save(Path('/state/episodes')/(digest([config,family,condition])+'.json'),
                 {'episode':e,'scores':scores.get(e['episode_id'])})
            state.commit()
    return {'remote_completed':True,'scripted':False,'config':config,'episodes':episodes,
            'scores':scores,'calls':journal,'gpu_function_seconds':time.monotonic()-started,
            'billing_note':'Measured function time, not an authoritative Modal invoice.'}

@app.local_entrypoint()
def main(config:str='pilot/configs/candidate.json',family:int=1001,conditions:str='B,G,I,T,O,H',
         output:str='pilot/runs/dev-initial.json',execute_test:bool=False):
    c=load(config);cs=conditions.split(',')
    if any(x not in CONDITIONS for x in cs):raise ValueError('Unknown condition')
    if Path(output).exists():raise ValueError('Output already exists; reuse it, do not silently pay again')
    if family not in c['development_families']:
        if not execute_test or not config.replace('\\','/').startswith('pilot/frozen/'):
            raise ValueError('Held-out run requires frozen config and explicit --execute-test')
        if family not in c['test_families']:raise ValueError('Unscheduled family')
        from .cli import main as unused
        import hashlib
        for p,h in load('pilot/frozen/hashes.json').items():
            if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Frozen hash mismatch')
        c=dict(c,allow_test_execution=True)
    ledger_path=Path('pilot/spend.json');ledger=load(ledger_path) if ledger_path.exists() else {'reservations':[]}
    reserved=sum(x['reserved_usd'] for x in ledger['reservations'])
    if reserved+1.25>20:raise ValueError('Modal budget exhausted: conservative reservations reach $20')
    entry={'reserved_usd':1.25,'state':'reserved','config_hash':digest(c),'family':family,
           'conditions':cs,'output':output,'time_unix':time.time()}
    ledger['reservations'].append(entry);save(ledger_path,ledger)
    from .progress import record
    record(f'Reserved development/test batch for family {family}, conditions {cs}, output {output}.')
    try:
        data=batch.remote(c,[family],cs)
        save(output,data)
        entry.update(state='completed',measured_estimate_usd=data['gpu_function_seconds']*1.021392/3600,
                     seconds=data['gpu_function_seconds'])
        print('Saved development/test output:',output,'; GPU seconds:',round(data['gpu_function_seconds']))
    except BaseException:
        entry['state']='failed_or_interrupted_reservation_retained'
        raise
    finally:
        save(ledger_path,ledger)
        record(f'Batch state: {entry["state"]}; output {output}.')
