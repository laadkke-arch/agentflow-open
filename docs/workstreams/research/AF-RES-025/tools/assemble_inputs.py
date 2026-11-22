#!/usr/bin/env python3
"""Normalize preregistered stream ledgers, retaining their original records separately."""
import collections
import csv
import hashlib
import json
import pathlib
from datetime import datetime, timezone

BASE=pathlib.Path(__file__).resolve().parents[1]
REPO=BASE.parents[3]

def lines(p): return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def jl(p,rs): p.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rs))
questions=[];queries=[];frames=[];sources=[]
for name in ['arrow','cargo','jupyter']:
    stream=BASE/'streams'/name
    qs=lines(stream/'questions.jsonl')
    for q in qs:
        q=dict(q);q['scope']={'partial':'part'}.get(q['scope'],q['scope']);q['stream']=name
        questions.append(q)
    for row in lines(stream/'queries.jsonl'):
        row=dict(row);row['stream']=name;row['id']=row['question_id']+'-'+row['route']
        row['budget_as_recorded']=row['budget']
        row['budget']={'max_queries':3,'max_results_per_query':10,'max_candidate_original_opens':5,'max_final_candidates':3}
        row['results_seen_before_seal']=row.get('results_seen_before_seal',False)
        row['sealed_at_utc']=row.get('sealed_at_utc',row.get('sealed_utc',row.get('prepared_utc')))
        row['model']='GPT-6 Astra Pro; same inherited session model'
        row['site_scope']='public web; no domain restriction; evidence must be primary originals'
        row['restore_command']=('python docs/workstreams/research/AF-RES-025/streams/arrow/restore_inputs.py' if name=='arrow' else 'git checkout supplies fixed licensed input bytes')
        queries.append(row)
    with (stream/'frame.csv').open(newline='') as f:
        for ordinal,row in enumerate(csv.DictReader(f),1):
            qid=row.get('question_id','')
            q=next((q for q in qs if q['id']==qid),None)
            url=row.get('url') or row.get('metadata_url') or ''
            frames.append({'stream':name,'frame_id':row.get('frame_id') or f'CG-F{ordinal:02}',
              'ledger':row.get('ledger') or 'rust-lang/rfcs T-cargo PR metadata',
              'ledger_rank':row.get('ledger_ordinal') or row.get('ledger_rank') or row.get('rank') or ordinal,
              'title':row.get('title',''),'metadata_url':url,
              'first_publication_date':(q['date'] if q else row.get('sort_date_utc') or row.get('first_publication_date') or row.get('created_at') or row.get('pr_created_at') or ''),
              'decision':row.get('decision',''),'reason':row.get('reason',''),'question_id':qid,
              'scope':(q['scope'].replace('partial','part') if q else row.get('scope','')),
              'fixed_initial_url':(q['initial_url'] if q else row.get('fixed_initial_url') or row.get('initial_url') or ''),
              'fixed_version':(q.get('initial_commit') or q.get('initial_version') if q else row.get('initial_version') or row.get('first_draft_sha') or row.get('initial_commit') or ''),
              'input_sha256':q['input_sha256'] if q else '',
              'stream_record':str((stream/'frame.csv').relative_to(BASE))+':'+str(ordinal+1)})
    ss=json.loads((stream/'sources.json').read_text())
    if isinstance(ss,dict):ss=ss.get('sources',ss.get('rows',[]))
    for s in ss:
        s=dict(s);s['stream']=name;sources.append(s)
questions.sort(key=lambda x:x['id']);queries.sort(key=lambda x:(x['question_id'],x['order']))
jl(BASE/'questions.jsonl',questions);jl(BASE/'queries.jsonl',queries)
with (BASE/'frame.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(frames[0]),lineterminator='\n');w.writeheader();w.writerows(frames)
dump(BASE/'evidence'/'initial-sources.json',sources)
dump(BASE/'sources.json',sources)
locked={}
for name in ['questions.jsonl','queries.jsonl','frame.csv','evidence/initial-sources.json','SCOPE.md','DATA_CONTRACT.md']:
    p=BASE/name;locked[name]=hashlib.sha256(p.read_bytes()).hexdigest()
for q in questions:
    p=REPO/q['input_path'];locked[q['input_path'].split('AF-RES-025/',1)[1]]=hashlib.sha256(p.read_bytes()).hexdigest()
receipt={'sealed_at_utc':datetime.now(timezone.utc).isoformat(),'question_count':len(questions),'route_count':len(queries),
 'query_count':sum(len(q['query_strings']) for q in queries),'scope_counts':dict(collections.Counter(q['scope'] for q in questions)),
 'project_counts':dict(collections.Counter(q['project'] for q in questions)),
 'frame_rows':len(frames),'input_file_sha256':locked,'candidate_searches_before_lock':0,
 'mail_fulltext_storage':'Arrow raw originals are restored by Message-ID from public archive with exact hash; copyrighted mail bodies are not republished in Git.'}
dump(BASE/'evidence'/'input-lock.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='input_file_sha256'},ensure_ascii=False,indent=2))
