#!/usr/bin/env python3
"""Verify actual run coverage, check identity/order, budgets and pre-injection hashes."""
import argparse,collections,datetime,json
from common import ROOT,load,save,parse_time,document_counts
from runner_audit import audit
def main(partial,write):
    order=load('questions/dispatch.json')['order'];state=load('runs/DISPATCH_STATE.json')['assigned']
    assigned={r['dispatch_index']:r for r in state};checks={q['qid']:q['checks'] for q in load('gold/checks.json')['questions']}
    rows=[];errors=[];missing=[];models=collections.Counter();agents=[]
    for d in order:
        run=load(d['output']);s=assigned.get(d['dispatch_index'])
        if not run or len(run.get('checks',[]))!=3:
            missing.append(d['output']);continue
        receipt=load(f'runs/freeze/{d["condition"]}-{d["qid"]}.json')
        if not receipt:errors.append({'path':d['output'],'error':'missing pre-injection receipt'});continue
        a=audit(ROOT/d['output'],receipt)
        if a['errors']:errors.append(a)
        expected=[c['check_id'] for c in checks[d['qid']]];actual=[c.get('check_id') for c in run['checks']]
        if actual!=expected:errors.append({'path':d['output'],'error':'check IDs/order differ from frozen input'})
        if not s or s['phase']!='completed':errors.append({'path':d['output'],'error':'parent completion audit missing'})
        else:agents.append(s['agent'])
        if not run['raw_response'].strip():errors.append({'path':d['output'],'error':'empty raw response'})
        if run.get('checks_started_at_utc') and parse_time(run['checks_started_at_utc'])<parse_time(receipt['receipt_at_utc']):
            errors.append({'path':d['output'],'error':'checks started before parent freeze receipt'})
        models[str(run.get('model_label','unreported'))]+=1
        rows.append({'dispatch_index':d['dispatch_index'],'qid':d['qid'],'condition':d['condition'],
                     'agent':s['agent'] if s else None,'checks':len(run['checks']),
                     'candidates':len(run['candidates']),'queries':len(run['queries']),
                     'declared_open_budget':run['budget']['opened_pages'],**document_counts(run['opened_documents']),
                     'exposures':len(run.get('exposures',[])),'warnings':a['warnings'],
                     'started_at_utc':run['started_at_utc'],'ended_at_utc':run['ended_at_utc']})
    if len(agents)!=len(set(agents)):errors.append({'error':'execution-agent reuse across assigned runs'})
    if missing and not partial:errors.append({'error':'incomplete required runs','paths':missing})
    result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'expected_runs':len(order),'completed_runs':len(rows),'completed_checks':sum(r['checks'] for r in rows),
            'full_question_pairs':sum(all(any(r['qid']==q['id'] and r['condition']==c for r in rows) for c in ['A','P']) for q in load('questions/metadata.json')),
            'fresh_agent_assignments':len(set(agents)),'model_labels':dict(models),'partial_audit':partial,
            'missing':missing,'errors':errors,'rows':rows,
            'isolation_limit':'Fresh fork_turns=none assignments and executor self-reports; file restrictions were instructional, not OS sandbox isolation.'}
    if write:save('analysis/run-inventory.json',result)
    print(json.dumps({k:result[k] for k in ['expected_runs','completed_runs','completed_checks','full_question_pairs','fresh_agent_assignments','errors']},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');p.add_argument('--write',action='store_true');a=p.parse_args();main(a.partial,a.write)
