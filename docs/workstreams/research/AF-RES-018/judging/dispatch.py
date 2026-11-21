#!/usr/bin/env python3
"""Parent-observed fresh-context assignment receipts; no relevance scoring."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(p):return json.loads((ROOT/p).read_text())
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def main(job_id,agent,complete):
    manifest=load('judging/judge-manifest.json')
    job=next(r for r in manifest if r['job_id']==job_id)
    path=ROOT/'judging/dispatch-state.json'
    data=json.loads(path.read_text()) if path.exists() else {'assignments':[],'limits':'Parent-observed assignment/completion timestamps, not server-side request timing. Fresh contexts are instruction-isolated, not OS-isolated. Requested model route and actual displayed label are separate.'}
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    found=[r for r in data['assignments'] if r['job_id']==job_id]
    if complete:
        assert len(found)==1
        output=load(job['output']);r=found[0]
        assert r['phase']=='assigned'
        r.update(phase='completed',completion_observed_at_utc=now,output_sha256=digest(job['output']),displayed_model_label=output['displayed_model_label'])
    else:
        assert agent and not found
        packet=load(job['input']);files=[job['input'],'judging/RULES.md']+[p for x in packet['inputs'] for p in x.values()]
        data['assignments'].append({'job_id':job_id,'agent':agent,'judge_id':job['judge_id'],'requested_model_route':job['requested_model_route'],
          'fork_turns':'none','phase':'assigned','assignment_observed_at_utc':now,'input_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'input_sha256':{p:digest(p) for p in files},'output':job['output'],
          'authorization':'User requests fresh-context internal separate judging and another model configuration when selectable.'})
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'job_id':job_id,'phase':'completed' if complete else 'assigned','observed_at_utc':now}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('job_id');p.add_argument('--agent');p.add_argument('--complete',action='store_true');a=p.parse_args();main(a.job_id,a.agent,a.complete)
