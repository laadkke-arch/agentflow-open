#!/usr/bin/env python3
"""Prepare condition-hidden judging jobs from the already registered coverage."""
import argparse,collections,datetime,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def prepare():
 assert not (ROOT/'judging/key.json').exists(),'Key already revealed; refuse new blinded preparation'
 plan=load('judging/plan.json');order=load('judging/batch-order.json')['qids'];manifest=[]
 for judge in plan['judges']:
  qids=[q for q in order if q in judge['qids']];assert set(qids)==set(judge['qids'])
  for start in range(0,len(qids),4):
   batch=start//4+1;selected=qids[start:start+4];job=judge['judge_id']+f'-{batch:02d}'
   row_ids=[]
   for q in selected:row_ids.extend(r['row_id'] for r in load(f'judging/normalized/{q}.json')['rows'])
   packet={'job_id':job,'judge_id':judge['judge_id'],'requested_model_route':judge['requested_model'],
    'read_only_rules':'judging/RULES.md','qids':selected,
    'inputs':[{'question':f'judging/question-inputs/{q}.json','candidates':f'judging/normalized/{q}.json'} for q in selected],
    'output':f'judging/blind-raw/{job}.json',
    'instructions':'Read only this packet, judging/RULES.md and its listed question/candidate inputs. Execute an original-question read command if present without reading its helper. Do not read runs, gold, keys, other judgments or repository history. Read current official sources for candidates when accessible; never open the source question/answer thread. Judge every row independently, including repeated entities; a difference must follow its factual scope, not format. Keep actual raw judgment text and actual UTC/source observations. Do not infer condition.',
    'output_fields':['job_id','judge_id','requested_model_route','displayed_model_label','started_at_utc','ended_at_utc','rows','raw_response','readings','excluded_readings','queries','limitations'],
    'reading_fields':['url','accessed_at_utc','title','version_or_date','sections_read','confirmed','limits','level'],
    'row_fields':['row_id','relevance','L','E','H','T','label','must_violations','evidence_urls','reason','checked_at_utc','judge_model_label','limitations'],
    'H_format':'Per-must array or object preserving condition/polarity/scope and pass/fail/unknown/not_in_scope; empty if no must. A scalar is accepted only with equivalent must_violations detail.'}
   path=f'judging/judge-inputs/{job}.json';save(path,packet)
   manifest.append({'job_id':job,'judge_id':judge['judge_id'],'requested_model_route':judge['requested_model'],'input':path,'output':packet['output'],'qids':selected,'row_ids':row_ids})
 save('judging/judge-manifest.json',manifest);print({'jobs':len(manifest),'rows_by_judge':dict(collections.Counter({j['judge_id']:sum(len(b['row_ids']) for b in manifest if b['judge_id']==j['judge_id']) for j in plan['judges']}))})
def validate(partial=False):
 manifest=load('judging/judge-manifest.json');seen=collections.defaultdict(set);reports=[];errors=[]
 allowed={'relevance':{'1','N','0','U'},'L':{'ok','broken','missing'},'E':{'supported','contradicted','unknown'},'T':{'not_needed','mapped','analogy_only','unknown'},'label':{'DIRECT_DOCUMENTED','INSUFFICIENT','CONDITIONAL_TRANSFER','SURFACE_OR_CONSTRAINT_MISMATCH'}}
 for b in manifest:
  if not (ROOT/b['output']).exists():
   if not partial:errors.append('Missing '+b['output'])
   continue
  j=load(b['output']);rs=j.get('rows',[]);ids=[r.get('row_id') for r in rs]
  if j.get('judge_id')!=b['judge_id'] or set(ids)!=set(b['row_ids']) or len(ids)!=len(set(ids)):errors.append('Coverage '+b['job_id'])
  if not j.get('raw_response') or not j.get('displayed_model_label'):errors.append('Missing raw/model '+b['job_id'])
  for r in rs:
   for f,options in allowed.items():
    if str(r.get(f)) not in options:errors.append(f'Invalid {f} {b["job_id"]} {r.get("row_id")}')
   for f in ['H','must_violations','evidence_urls','reason','checked_at_utc','judge_model_label','limitations']:
    if f not in r:errors.append(f'Missing {f} {r.get("row_id")}')
   if r.get('row_id') in seen[b['judge_id']]:errors.append('Duplicate '+str(r.get('row_id')))
   seen[b['judge_id']].add(r.get('row_id'))
  for reading in j.get('readings',[]):
   for field in ['url','accessed_at_utc','title','version_or_date','sections_read','confirmed','limits','level']:
    if field not in reading:errors.append(f'Missing source {field} {b["job_id"]}')
  reports.append({'job_id':b['job_id'],'judge_id':b['judge_id'],'rows':len(rs),'requested_model_route':b['requested_model_route'],'displayed_model_label':j.get('displayed_model_label'),'readings':len(j.get('readings',[]))})
 result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'planned_jobs':len(manifest),'completed_jobs':len(reports),'jobs':reports,'errors':errors}
 if not partial:save('judging/coverage-audit.json',result)
 print(json.dumps(result,ensure_ascii=False));assert not errors,'Judgment validation errors'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--partial',action='store_true');a=p.parse_args()
 if a.prepare:prepare()
 if a.validate:validate(a.partial)
