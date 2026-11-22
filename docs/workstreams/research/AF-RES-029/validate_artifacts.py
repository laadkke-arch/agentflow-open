"""Research-artifact validation; no supplier behavior or runtime is inferred."""
import argparse, hashlib, json, subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urldefrag

P=Path(__file__).resolve().parent
REPO=P.parents[3]

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--require-routes',action='store_true');parser.add_argument('--output');args=parser.parse_args()
 findings=[]
 def record(condition,met,evidence,note=''):
  findings.append(dict(condition=condition,met=bool(met),evidence=evidence,note=note))
 qs=[json.loads(x) for x in (P/'questions.jsonl').read_text().splitlines() if x.strip()]
 record('twelve_unique_events',len(qs)==12 and len({x['id'] for x in qs})==12,'questions.jsonl')
 for ledger in ['go','python','numpy']:
  rows=[x for x in qs if x['ledger'].lower()==ledger]
  record('quota_'+ledger,len(rows)==4 and sum(x['scope']=='whole' for x in rows)==2 and sum(x['scope']=='partial' for x in rows)==2,'questions.jsonl')
 for name in ['input-seal.json','common-seal.json','route-seal.json','masked-seal.json']:
  f=P/'evidence'/name
  if f.exists():
   s=json.loads(f.read_text());bad=[]
   for k,v in s.get('files',{}).items():
    fp=P/k
    if not fp.exists() or hashlib.sha256(fp.read_bytes()).hexdigest()!=v:bad.append(k)
   record('hashes_'+name,not bad,str(f.relative_to(P)),json.dumps({'sealed_files':len(s.get('files',{})),'mismatches':bad}))
 counters=[]
 for q in qs:
  qid=q['id'];d=P/'common'/qid;f=d/'baseline-return.json'
  record(qid+'_common_present',f.exists(),str(f.relative_to(P)))
  opens=list(d.glob('open-*.json'));record(qid+'_common_open_cap',len(opens)<=2,str(d.relative_to(P)),f'{len(opens)} actual open receipts')
  s=json.loads((d/'search.json').read_text());request=s['request'];query=request.get('system2_search_query',[])
  record(qid+'_literal_neutral',len(query)==1 and query[0]['q']==q['neutral_query'],str((d/'search.json').relative_to(P)))
  start=json.loads((d/'start.json').read_text());hits=start.get('top_ten',start.get('search_results',[]))
  record(qid+'_ten_provided_ranks',len(hits)==10 and [x['rank'] for x in hits]==list(range(1,11)),str((d/'start.json').relative_to(P)))
  for route in ['C','A','B']:
   d=P/'common'/qid if route=='C' else P/'routes'/route/qid
   f=d/('baseline-return.json' if route=='C' else 'return.json')
   if not f.exists():
    if args.require_routes:record(qid+'_'+route+'_return_present',False,str(f.relative_to(P)))
    continue
   ret=json.loads(f.read_text());cand=ret['candidates'];urls=list(dict.fromkeys(urldefrag(c['url'])[0] for x in cand for c in x['citations']))
   gate=ret.get('serialization_gate',{})
   record(qid+'_'+route+'_original_return_gate',len(cand)<=3 and len(urls)<=3 and [x['rank'] for x in cand]==list(range(1,len(cand)+1)) and gate.get('candidate_count')==len(cand) and gate.get('url_count')==len(urls) and gate.get('posthoc_truncation') is False,str(f.relative_to(P)))
   budget=ret.get('budget',{});nav=budget.get('navigation',0);body=budget.get('body_opens',0)
   if route!='C':
    receipts=[]
    for rf in sorted(d.rglob('*.json')):
     rd=json.loads(rf.read_text())
     if isinstance(rd,dict) and 'request' in rd and 'response' in rd:
      receipts.append((rf,rd))
    actual_nav=sum(x.get('navigation_debit',x.get('budget_debit',{}).get('navigation',0)) for _,x in receipts)
    actual_body=sum(x.get('body_open_debit',x.get('budget_debit',{}).get('body_opens',0)) for _,x in receipts)
    record(qid+'_'+route+'_receipt_budget',nav==actual_nav and body==actual_body and nav<=2 and body<=4,str(d.relative_to(P)),json.dumps({'declared':[nav,body],'receipt_debits':[actual_nav,actual_body],'network_receipts':len(receipts)}))
    if route=='A':
     literal=[z['q'] for _,x in receipts for z in x['request'].get('system2_search_query',[])]
     record(qid+'_A_queries_frozen',len(literal)<=2 and sorted(literal)==sorted(q['a_queries'][:len(literal)]),str(d.relative_to(P)))
    else:
     record(qid+'_B_no_web_search',not any(x['request'].get('system2_search_query') or x['request'].get('system1_search_query') for _,x in receipts),str(d.relative_to(P)))
   counters.append({'question_id':qid,'route':route,'navigation':nav,'body_opens':body,'candidates':len(cand),'document_urls':len(urls),'started_utc':ret.get('started_utc'),'ended_utc':ret.get('ended_utc',gate.get('checked_utc'))})
 for q in qs:
  rr={x['route']:x for x in counters if x['question_id']==q['id']}
  first,second=('A','B') if int(q['id'][1:])%2 else ('B','A')
  if first in rr and second in rr:
   a=rr[first].get('ended_utc');b=rr[second].get('started_utc')
   record(q['id']+'_alternation',bool(a and b and datetime.fromisoformat(a.replace('Z','+00:00'))<=datetime.fromisoformat(b.replace('Z','+00:00'))),'routes/'+q['id'],f'{first} end {a}; {second} start {b}')
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 changed=subprocess.check_output(['git','diff','--name-only','172c6bc37bdf91b91c86b9b3be29cb5b44fa4971','HEAD'],cwd=REPO,text=True).splitlines()
 record('committed_paths_owned',all(x.startswith('docs/workstreams/research/AF-RES-029/') for x in changed),'git diff initial-integration HEAD',f'{len(changed)} committed paths')
 result={'checked_utc':datetime.now(timezone.utc).isoformat(),'target_head':head,'command_arguments':vars(args),'findings':findings,'counters':counters,'failed_conditions':[x['condition'] for x in findings if not x['met']],'scope':'Artifact bookkeeping only; no supplier behavior execution and no semantic success inference.'}
 if args.output:
  dest=(P/args.output).resolve();assert dest.is_relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'target_head':head,'conditions':len(findings),'failed':result['failed_conditions'],'observations':len(counters)}))
 return int(bool(result['failed_conditions']))

if __name__=='__main__':raise SystemExit(main())
