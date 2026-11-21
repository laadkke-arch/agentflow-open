#!/usr/bin/env python3
"""Parent-side bookkeeping. Never called by a blinded experimental executor."""
from pathlib import Path
import argparse,json,datetime
from runner_audit import audit
ROOT=Path(__file__).resolve().parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=argparse.ArgumentParser();p.add_argument('--assign',type=int);p.add_argument('--checks',nargs=2,metavar=('CONDITION','QID'));p.add_argument('--complete',type=int);p.add_argument('--next',action='store_true');a=p.parse_args()
order=read('questions/dispatch.json')['order'];state=read('runs/DISPATCH_STATE.json')
if a.assign:
    row=dict(order[a.assign-1]);assert row['dispatch_index']==a.assign
    assert not any(r['dispatch_index']==a.assign for r in state['assigned'])
    row.update(agent='/root/run_'+str(a.assign).zfill(3),phase='discovery_assigned',assignment_recorded_at_utc=now())
    state['assigned'].append(row);write('runs/DISPATCH_STATE.json',state);print(json.dumps(row))
elif a.checks:
    cond,qid=a.checks
    receipt=ROOT/'runs/freeze'/f'{cond}-{qid}.json';assert receipt.exists(),'Freeze before injection'
    checks=next(q['checks'] for q in read('gold/checks.json')['questions'] if q['qid']==qid)
    payload=[{'check_id':c['check_id'],'name':c['name'],'url':c['url']} for c in checks]
    print('Discovery freeze recorded. Now judge these three candidates in this exact order. Return keep or exclude plus a concrete reason for each. Follow your condition rules (A free judgment; P steps4–5). Use only the remaining shared12-query/20-open budget. Do not edit frozen raw_response, candidates or existing log entries. Append checks/new queries/new documents, final budget, checks_started_at_utc/checks_ended_at_utc and final ended_at_utc in your same assigned run file. If URL is null, judge the named proposed approach without opening the source thread. No other inputs. Candidates:')
    print(json.dumps(payload,ensure_ascii=False))
    row=next(r for r in state['assigned'] if r['condition']==cond and r['qid']==qid)
    row['phase']='checks_ready';row['check_payload_prepared_at_utc']=now();write('runs/DISPATCH_STATE.json',state)
elif a.complete:
    row=next(r for r in state['assigned'] if r['dispatch_index']==a.complete)
    run=read(row['output']);assert len(run.get('checks',[]))==3
    checked=audit(ROOT/row['output'],read(f'runs/freeze/{row["condition"]}-{row["qid"]}.json'))
    assert not checked['errors'],checked
    row['integrity_audit']=checked
    row['phase']='completed';row['completion_observed_at_utc']=now();write('runs/DISPATCH_STATE.json',state)
    print(json.dumps({'completed':a.complete,'qid':row['qid'],'condition':row['condition']}))
elif a.next:
    used={r['dispatch_index'] for r in state['assigned']}
    print(json.dumps([r for r in order if r['dispatch_index'] not in used][:6],ensure_ascii=False,indent=2))
    print('Assigned phases:',json.dumps({r['dispatch_index']:r['phase'] for r in state['assigned']}))
