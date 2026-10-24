"""Ephemeral, authenticated Modal RPC batch. No public endpoint or embedded secrets.

Development command: python -m modal run -m pilot.modal_app --config ...
Each invocation has a 30-minute GPU timeout, one replica, no platform retries.
Local ledger reserves $0.75 before each trial (above a full L4/2CPU/16GiB timeout).
Do not change the hardware without updating the reservation and budget logic.
"""
import time
from pathlib import Path
import modal
from .core import Cached, generate_episode, score_episode, load, save, digest, CONDITIONS,budget_total

app=modal.App('collusion-track22-pilot',include_source=False)
state=modal.Volume.from_name('collusion-track22-pilot-state',create_if_missing=True)
def exclude_upload(path):
    # SDK paths are relative to its mount, not to cwd. Never stat relative paths.
    # An exact allowlist also prevents changing log files from entering builds.
    value=path.as_posix().removeprefix('pilot/')
    return value not in {'__init__.py','core.py','modal_app.py','progress.py','patches','patches/upstream.py'}
image=(modal.Image.from_registry('nvidia/cuda:12.9.0-devel-ubuntu22.04',add_python='3.12')
       .entrypoint([]).uv_pip_install('vllm==0.21.0')
       .env({'HF_HOME':'/state/hf','VLLM_CACHE_ROOT':'/state/vllm'}))
for relative in ['__init__.py','core.py','modal_app.py','progress.py','patches/upstream.py']:
    image=image.add_local_file(str(Path(__file__).resolve().parent/relative),'/root/pilot/'+relative)

@app.function(image=image,gpu='L4',cpu=2,memory=16384,timeout=1800,
              max_containers=1,scaledown_window=2,retries=0,volumes={'/state':state})
def batch(config,families,conditions,episodes_to_score=None):
    from huggingface_hub import model_info
    from vllm import LLM,SamplingParams
    from vllm.sampling_params import StructuredOutputsParams
    import json
    started=time.monotonic()
    revision=config.get('revision') or model_info(config['model']).sha
    config=dict(config,revision=revision)
    separate=bool(config.get('monitor_model') and config['monitor_model']!=config['model'])
    if separate:
        config=dict(config,monitor_revision=config.get('monitor_revision') or model_info(config['monitor_model']).sha)
    active_model=(config.get('monitor_model') or config['model']) if episodes_to_score is not None else config['model']
    active_revision=(config.get('monitor_revision') or revision) if episodes_to_score is not None else revision
    save(Path('/state/manifests')/(digest(config)+'.json'),config);state.commit()
    llm=LLM(model=active_model,revision=active_revision,dtype='bfloat16',
            max_model_len=config['context_limit'],gpu_memory_utilization=.90,
            max_num_seqs=2,trust_remote_code=False,enforce_eager=True)
    state.commit()
    tokenizer=llm.get_tokenizer(); journal=[];calls={}
    cache_dir=Path('/state/calls');cache_dir.mkdir(exist_ok=True)
    def complete(req):
        key=digest([active_model,active_revision,req])
        if key in calls:return calls[key]
        cached=cache_dir/(key+'.json')
        if cached.exists():
            item=load(cached);journal.append(dict(item,cache_hit=True));calls[key]=item['response'];return item['response']
        text=tokenizer.apply_chat_template([{'role':'system','content':req['system']},
              {'role':'user','content':req['user']}],tokenize=False,add_generation_prompt=True)
        prompt_tokens=len(tokenizer.encode(text,add_special_tokens=False))
        if prompt_tokens+req['max_tokens']>config['context_limit']:
            raise ValueError('Context overflow: no silent truncation')
        params=SamplingParams(temperature=req['temperature'],max_tokens=req['max_tokens'],seed=req['seed'],
            structured_outputs=StructuredOutputsParams(json=req['response_schema']) if req.get('response_schema') else None)
        t=time.monotonic();result=llm.generate([text],params,use_tqdm=False)[0]
        answer=result.outputs[0].text.strip();calls[key]=answer
        # Exact evidence logged, never credentials; no ambient environment serialized.
        journal.append({'key':key,'model':active_model,'revision':active_revision,'request':req,'response':answer,'input_tokens':prompt_tokens,
                        'output_tokens':len(result.outputs[0].token_ids),'seconds':time.monotonic()-t})
        save(cached,journal[-1])
        if len(journal)%17==0:state.commit()
        return answer
    episodes=[];scores={}
    schedule=episodes_to_score if episodes_to_score is not None else [(f,c) for f in families for c in conditions]
    for item in schedule:
        if episodes_to_score is not None:
            e=item;family=e['family_id'];condition=e['oracle']['condition']
            if family not in families or condition not in conditions or e['config_hash']!=digest(config):
                raise ValueError('Monitor phase received mismatched generation provenance')
        else:
            family,condition=item;e=generate_episode(complete,config,family,condition)
        episodes.append(e)
        if e['valid'] and (not separate or episodes_to_score is not None):scores[e['episode_id']]=score_episode(complete,e,config)
        save(Path('/state/episodes')/(digest([config,family,condition])+'.json'),
             {'episode':e,'scores':scores.get(e['episode_id'])})
        state.commit()
        print(f'Completed family {family}, condition {condition}: valid={e["valid"]}, implemented={e["labels"]["implementation"]}',flush=True)
    return {'remote_completed':True,'scripted':False,'config':config,'episodes':episodes,
            'stage':'monitor' if episodes_to_score is not None else ('generation' if separate else 'complete'),
            'active_model':active_model,'active_revision':active_revision,
            'scores':scores,'calls':journal,'gpu_function_seconds':time.monotonic()-started,
            'source_hashes':{str(p.relative_to(Path('/root'))):__import__('hashlib').sha256(p.read_bytes()).hexdigest()
                for p in [Path('/root/pilot')/s for s in ['core.py','modal_app.py','progress.py','patches/upstream.py']]},
            'versions':{s:__import__('importlib.metadata',fromlist=['version']).version(s) for s in ['vllm','torch','transformers']},
            'billing_note':'Measured function time, not an authoritative Modal invoice.'}

@app.local_entrypoint()
def main(config:str='pilot/configs/candidate.json',family:int=1001,conditions:str='B,G,I,T,O,H',
         output:str='pilot/runs/dev-initial.json',execute_test:bool=False):
    from .progress import require_funding
    funding=require_funding()
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
    separate=bool(c.get('monitor_model') and c['monitor_model']!=c['model'])
    if separate:
        generation_path=output+'.generation.json'
        if Path(generation_path).exists():
            generated=load(generation_path)
            expected=dict(c)
            for key in ('revision','monitor_revision'):
                if not expected.get(key):expected[key]=generated['config'][key]
            if digest(expected)!=digest(generated['config']):raise ValueError('Generation checkpoint mismatch')
        else:
            generated=run_stage(funding,c,family,cs,generation_path)
        scored=run_stage(funding,generated['config'],family,cs,output+'.monitor.json',generated['episodes'])
        data=dict(generated,scores=scored['scores'],stage='complete',calls=generated['calls']+scored['calls'],
            gpu_function_seconds=generated['gpu_function_seconds']+scored['gpu_function_seconds'],
            monitor_provenance={k:scored.get(k) for k in ('active_model','active_revision','source_hashes','versions')})
        save(output,data)
        print('Saved combined agent/monitor result:',output)
    else:run_stage(funding,c,family,cs,output)


def run_stage(funding,c,family,cs,output,episodes_to_score=None):
    if Path(output).exists():
        existing=load(output)
        if digest(existing['config'])!=digest(c):raise ValueError('Existing phase configuration mismatch')
        return existing
    ledger_path=Path('pilot/spend.json');ledger=load(ledger_path) if ledger_path.exists() else {'reservations':[]}
    reserved=budget_total(ledger)
    reservation=.75  # Full 1800s resource estimate is $0.511; setup/storage has a separate $1 reserve.
    if reserved+reservation>min(20,funding['loop_cap_usd'],funding['reported_credit_usd']):
        raise ValueError('Modal batch exceeds the loop cap or available-credit envelope')
    entry={'reserved_usd':reservation,'state':'reserved','config_hash':digest(c),'family':family,
           'conditions':cs,'output':output,'time_unix':time.time(),'app_id':app.app_id}
    ledger['reservations'].append(entry);save(ledger_path,ledger)
    from .progress import record
    record(f'Reserved development/test batch for family {family}, conditions {cs}, output {output}.')
    try:
        data=batch.remote(c,[family],cs,episodes_to_score=episodes_to_score)
        save(output,data)
        entry.update(state='completed',measured_estimate_usd=data['gpu_function_seconds']*1.021392/3600,
                     seconds=data['gpu_function_seconds'])
        print('Saved development/test output:',output,'; GPU seconds:',round(data['gpu_function_seconds']))
        return data
    except BaseException:
        entry['state']='failed_or_interrupted_reservation_retained'
        raise
    finally:
        save(ledger_path,ledger)
        record(f'Batch state: {entry["state"]}; output {output}.')
