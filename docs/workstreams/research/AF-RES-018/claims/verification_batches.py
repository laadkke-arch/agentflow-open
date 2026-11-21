#!/usr/bin/env python3
"""Freeze condition-hidden fact-check packets after the sampled claims are committed."""
import argparse,collections,datetime,hashlib,json,random,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):
 f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def prepare(commit):
 assert commit,'Pass the remote commit that froze claims/SAMPLE.json before verification'
 repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
 rel=(ROOT/'claims/SAMPLE.json').relative_to(repo).as_posix()
 blob=subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)
 assert blob==(ROOT/'claims/SAMPLE.json').read_bytes(),'Sample differs from the committed selection'
 subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=ROOT,check=True)
 sample=load('claims/SAMPLE.json');claims=list(sample['claims']);random.Random(18018).shuffle(claims)
 meta={r['id']:r for r in load('questions/metadata.json')};manifest=[]
 for start in range(0,len(claims),10):
  number=start//10+1;rows=[]
  for c in claims[start:start+10]:
   raw=load(c['source_file'])['raw_response'];a,b=c['source_start'],c['source_end']
   assert raw[a:b]==c['source_quote']
   # The local paragraph plus surrounding characters preserves nearby caveats.
   left=max(0,raw.rfind('\n\n',0,a));right=raw.find('\n\n',b)
   if right<0:right=len(raw)
   context=raw[max(0,min(left,a-240)):min(len(raw),max(right,b+240))]
   rows.append({k:c.get(k) for k in ['id','qid','candidate','claim','claim_type','source_quote','supplied_urls','reference_kind']}|
               {'claim_context':context,'question_cohort':meta[c['qid']]['cohort'],'question_date':meta[c['qid']]['date'],'temporal_basis':'current'})
  inp=f'claims/verify-inputs/batch-{number:02d}.json';out=f'claims/verified/batch-{number:02d}.json'
  save(inp,{'batch':number,'rules':'claims/RULES.md','claims':rows,'output':out,
    'instructions':'Read only this packet and claims/RULES.md. Verify every fixed claim against current official documents or public code, preserving product/version/plan/platform and nearby caveats. Never replace a difficult claim. No source-thread answers, gold, runs, sample key, conditions or other judgments. Record actual opened URLs/UTC/sections and paraphrased findings; failed opens and snippets go in excluded_readings. Unknown is not false. False error type is a possible classification, not a proved causal mechanism. Record original assessment prose in raw_response.',
    'output_fields':['batch','judge','displayed_model_label','started_at_utc','ended_at_utc','claims','readings','excluded_readings','queries','raw_response','limitations'],
    'claim_fields':['id','verdict','evidence_url','evidence_urls','checked_at_utc','confirmed','scope','error_type','error_type_basis','limitations'],
    'reading_fields':['url','accessed_at_utc','title','version_or_date','sections_read','confirmed','limits','level'],
    'verdict_values':['true','false','unknown']})
  manifest.append({'batch':number,'input':inp,'output':out,'claim_ids':[r['id'] for r in rows]})
 save('claims/verification-manifest.json',{'sample_commit':commit,'sample_sha256':hashlib.sha256(blob).hexdigest(),'seed':18018,'batches':manifest})
 print({'sample_commit':commit,'claims':len(claims),'batches':len(manifest)})
def combine():
 manifest=load('claims/verification-manifest.json');sample=load('claims/SAMPLE.json')['claims'];byid={c['id']:c for c in sample}
 assert hashlib.sha256((ROOT/'claims/SAMPLE.json').read_bytes()).hexdigest()==manifest['sample_sha256']
 result=[];seen=set();sources=[];excluded=[];coverage=[]
 for b in manifest['batches']:
  v=load(b['output']);rows=v['claims'];assert v.get('judge') and v.get('displayed_model_label') and v.get('raw_response')
  assert len(rows)==len(b['claim_ids']) and {r['id'] for r in rows}==set(b['claim_ids'])
  for r in rows:
   assert r['id'] not in seen and r['verdict'] in ['true','false','unknown'];seen.add(r['id'])
   for f in ['evidence_url','checked_at_utc','confirmed','scope','error_type','limitations']:assert f in r,(r['id'],f)
   if r['verdict']=='false':assert r['error_type'] in ['outdated_information','product_confusion','version_or_plan_scope_omission','unsupported_generalization'] and r.get('error_type_basis')
   if r['verdict'] in ['true','false']:assert r['evidence_url'] and r.get('evidence_urls')
   result.append({**byid[r['id']],**r,'judge':v['judge'],'judge_model_label':v['displayed_model_label'],'verification_file':b['output'],'temporal_basis':'current'})
  for i,r in enumerate(v.get('readings',[])):
   for f in ['url','accessed_at_utc','title','version_or_date','sections_read','confirmed','limits','level']:assert f in r,(b['output'],f)
   assert r['level'] in ['D1','D2','D3-fetch'],('unread source may not support verified claim',r)
   sources.append({'id':f'CLSRC-{b["batch"]:02d}-{i+1:03d}',**r,'source_type':r.get('source_type','current official document or public code'),
                   'used_in':['Q6','Q8'],'counted_as':'claim_verification_not_methods','verification_file':b['output']})
  excluded.extend({'verification_file':b['output'],**r} for r in v.get('excluded_readings',[]))
  coverage.append({'batch':b['batch'],'claims':len(rows),'judge':v['judge'],'displayed_model_label':v['displayed_model_label'],'file':b['output']})
 assert seen==set(byid) and len(result)==len(sample)
 result.sort(key=lambda r:(r['condition'],r['qid'],r['id']))
 save('claims/CLAIMS.json',result);save('claims/verification-coverage.json',{'sample_commit':manifest['sample_commit'],'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'batches':coverage,'claim_counts':dict(collections.Counter(c['condition'] for c in result))})
 save('evidence/claim-readings.json',{'sources':sources,'excluded':excluded})
 print({'claims':len(result),'sources':len(sources),'excluded_readings':len(excluded)})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--sample-commit');p.add_argument('--combine',action='store_true');a=p.parse_args()
 if a.prepare:prepare(a.sample_commit)
 if a.combine:combine()
