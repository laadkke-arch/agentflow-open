"""Normalize the sealed-arm records; preserve raw files and uncertainty.

Run from repository root with python -B. No network or product execution.
"""
import collections
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]

def read_jsonl(path):
    rows = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            raise ValueError(f'blank JSONL line {path}:{n}')
        rows.append(json.loads(line))
    return rows

def write_jsonl(path, rows):
    path.write_text(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in rows))

def canonical(url):
    if not url:
        return None
    u = urlsplit(url)
    # Preserve identity-bearing query parameters (e.g. CiteSeer DOI).
    query = u.query if u.hostname and 'citeseerx' in u.hostname else ''
    return urlunsplit((u.scheme, u.netloc.lower(), u.path.rstrip('/'), query, ''))

def lineage(row):
    url = row.get('original_url') or row.get('canonical_document_url') or ''
    m = re.search(r'github\.com/([^/]+/[^/]+)/(?:issues|pull)/(\d+)', url)
    if m:
        return f'github:{m[1]}:issue:{m[2]}'
    m = re.search(r'gitlab\.com/(.+?)/-/(?:issues|work_items)/(\d+)', url)
    if m:
        return f'gitlab:{m[1]}:issue:{m[2]}'
    return row.get('lineage_id') or canonical(url)

def string(value):
    if value is None:
        return ''
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(',', ':'))

queries = read_jsonl(ROOT/'queries.jsonl')
q_index = {q['query_id']: q for q in queries}
problems = read_jsonl(ROOT/'problems.jsonl')
p_index = {p['problem_id']: p for p in problems}
base_path = ROOT/'evidence/recruitment-sources.jsonl'
if not base_path.exists():
    raise ValueError('Create immutable recruitment-sources.jsonl before the first assembly')
sources_raw = read_jsonl(base_path)
runs_raw, judgments_raw, costs = [], [], []
for arm in ('A','B'):
    arm_dir = ROOT/'arms'/arm
    for row in read_jsonl(arm_dir/'sources.jsonl'):
        row = dict(row)
        row['raw_record_file'] = f'arms/{arm}/sources.jsonl'
        sources_raw.append(row)
    runs_raw += read_jsonl(arm_dir/'runs.jsonl')
    judgments_raw += read_jsonl(arm_dir/'judgments.jsonl')
    raw_cost = read_jsonl(arm_dir/('accesses.jsonl' if arm=='A' else 'costs.jsonl'))
    for r in raw_cost:
        op=r['operation']
        search=int(op=='search')
        new=int(op in ('open','REST_issue_body_read','first_original_open'))
        extra=int(op in ('find','same_document_line_open','same_document_find','same_source_line_open'))
        if arm=='B':
            search=r.get('query_attempts',search)
            new=r.get('new_original_open_attempts',new)
            extra=r.get('same_document_access_attempts',extra)
        costs.append({'cost_id':r.get('access_id') or r.get('cost_id'), 'problem_id':r['problem_id'], 'arm':arm,
                      'operation':op,'query_attempts':search, 'new_url_open_attempts':new,
                      'same_document_extra_accesses':extra,'research_operations':r.get('attempts',r.get('tool_calls',1)),
                      'retries':int(r.get('retry',False)) if arm=='A' else r.get('retries',0),
                      'status':r['status'],'source_id':r.get('source_id'),'started_utc':r.get('started_utc'),
                      'finished_utc':r.get('completed_utc',r.get('finished_utc')),
                      'monetary_cost':None,'monetary_cost_status':'not_measured',
                      'raw_record_file':f'arms/{arm}/'+('accesses.jsonl' if arm=='A' else 'costs.jsonl')})
supplement = ROOT/'evidence/supplemental-sources.jsonl'
if supplement.exists():
    sources_raw += read_jsonl(supplement)
overrides_path = ROOT/'evidence/lineage-overrides.json'
overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
seen, sources = {}, []
for r in sources_raw:
    s=dict(r)
    lid=overrides.get(s['source_id'],lineage(s))
    s['reader_lineage_id']=s.get('lineage_id')
    s['lineage_id']=lid
    s['reader_count_toward_minimum']=s.get('count_toward_minimum',False)
    can_count=bool(s.get('direct_read')) and bool(s.get('count_toward_minimum'))
    s['count_toward_minimum']=can_count and lid not in seen
    s['minimum_count_duplicate_of']=seen.get(lid)
    if s['count_toward_minimum']:
        seen[lid]=s['source_id']
    s.setdefault('version',s.get('version_or_date',s.get('version_date')))
    s.setdefault('role','trial_return')
    sources.append(s)
source_index={s['source_id']:s for s in sources}
if len(source_index)!=len(sources):
    raise ValueError('duplicate source_id')
runs=[]
for r in runs_raw:
    q=q_index[r['query_id']]
    if r['query']!=q['query']:
        raise ValueError('query drift '+r['query_id'])
    sid=r.get('source_id')
    s=source_index.get(sid,{})
    url=r.get('original_url') or r.get('actual_url')
    runs.append({'rank_id':r['rank_id'],'problem_id':r['problem_id'],'arm':r['arm'],
                 'query_id':r['query_id'],'query':r['query'],'query_number':r['query_number'],
                 'original_rank':r['original_rank'],'rank_basis':r.get('rank_basis'),
                 'slot_present':r.get('returned_slot_present',r.get('slot_state')=='returned'),
                 'original_url':url,'canonical_url':canonical(url),'title':r.get('title'),
                 'source_id':sid,'lineage_id':s.get('lineage_id'),
                 'tool_reference_id':r.get('tool_reference_id') or r.get('tool_ref_id'),
                 'search_url':r.get('search_url') or r.get('search_request_uri'),
                 'search_url_kind':'tool audit locator; not exposed engine HTML URL',
                 'actual_query_payload':r.get('actual_tool_payload') or r.get('query_payload'),
                 'query_started_utc':r.get('query_started_utc') or r.get('started_utc'),
                 'query_completed_utc':r.get('query_completed_utc') or r.get('returned_utc'),
                 'duplicate_url_of':r.get('duplicate_url_of') or r.get('duplicate_of_rank_id'),
                 'duplicate_document_of':r.get('duplicate_document_of') or r.get('duplicate_of_rank_id'),
                 'inspection_status':r.get('inspection_status'),'direct_read':s.get('direct_read',False),
                 'raw_record_file':f'arms/{r["arm"]}/runs.jsonl'})
runs.sort(key=lambda r:(r['problem_id'],r['arm'],r['query_number'],r['original_rank']))
rank_index={r['rank_id']:r for r in runs}
if len(rank_index)!=len(runs):
    raise ValueError('duplicate rank_id')
expected={q['query_id'] for q in queries}
for qid in expected:
    ranks=sorted(r['original_rank'] for r in runs if r['query_id']==qid)
    if ranks!=[1,2,3,4,5]:
        raise ValueError('not yet complete: '+qid+' '+str(ranks))
judgments=[]
for j in judgments_raw:
    r=rank_index[j['rank_id']]
    conditions=j.get('conditions',{})
    c1=conditions.get(r['problem_id']+'-C1',{})
    c2=conditions.get(r['problem_id']+'-C2',{})
    accepted=bool(j.get('accepted_as_complete_solution',j.get('verified_fit',False)))
    if accepted and not(c1.get('status')=='support' and c2.get('status')=='support'):
        raise ValueError('accepted without both conditions supported '+j['rank_id'])
    judgments.append({'rank_id':r['rank_id'],'problem_id':r['problem_id'],'arm':r['arm'],
        'query_id':r['query_id'],'original_rank':r['original_rank'],'source_id':r['source_id'],
        'lineage_id':r['lineage_id'],'original_url':r['original_url'],'classification':j['classification'],
        'inspection_status':j.get('inspection_status'),'C1_status':c1.get('status','unknown'),
        'C1_evidence':string(c1),'C2_status':c2.get('status','unknown'),'C2_evidence':string(c2),
        'direct_component_or_transfer_principle':string(j.get('reuse_kind',j.get('part_vs_transfer_principle'))),
        'operation_variable_purpose_mapping':string(j.get('operation_variable_purpose_mapping')),
        'minimal_rejection_counterexample':j.get('minimal_rejection_counterexample'),
        'new_action_or_test':string(j.get('new_actions') or {'action':j.get('new_action'),'test':j.get('new_test')}),
        'new_design_choice':string(j.get('new_design_choice',j.get('design_choice'))),
        'next_check':string(j.get('next_check')),'confirmed_fit':str(accepted).lower(),
        'integration_executed':'false','raw_record_file':f'arms/{r["arm"]}/judgments.jsonl'})
judgments.sort(key=lambda j:(j['problem_id'],j['arm'],j['query_id'],j['original_rank']))
if len(judgments)!=90 or {j['rank_id'] for j in judgments}!=set(rank_index):
    raise ValueError('judgment/rank mismatch')
write_jsonl(ROOT/'runs.jsonl',runs)
write_jsonl(ROOT/'sources.jsonl',sources)
write_jsonl(ROOT/'evidence/costs.jsonl',costs)
write_jsonl(ROOT/'evidence/agent-judgments.jsonl',judgments_raw)
with (ROOT/'judgments.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(judgments[0]),lineterminator='\n');writer.writeheader();writer.writerows(judgments)

arm_stats=[]
for pid in p_index:
    for arm in ('A','B'):
        rr=[r for r in runs if r['problem_id']==pid and r['arm']==arm]
        cc=[c for c in costs if c['problem_id']==pid and c['arm']==arm]
        ss=[s for s in sources if s.get('problem_id')==pid and s.get('arm')==arm]
        jj=[j for j in judgments if j['problem_id']==pid and j['arm']==arm]
        arm_stats.append({'problem_id':pid,'arm':arm,'rank_slots':len(rr),'present_slots':sum(r['slot_present'] for r in rr),
          'distinct_returned_urls':len({r['canonical_url'] for r in rr if r['slot_present']}),
          'distinct_returned_lineages':len({r['lineage_id'] for r in rr if r['slot_present']}),
          'direct_read_source_records':sum(bool(s.get('direct_read')) for s in ss),
          'direct_read_lineages':len({s['lineage_id'] for s in ss if s.get('direct_read')}),
          'confirmed_fit_ranks':sum(j['confirmed_fit']=='true' for j in jj),
          **{k:sum(c[k] for c in cc) for k in ['query_attempts','new_url_open_attempts','same_document_extra_accesses','research_operations','retries']}})
pair_stats=[]
for pid in p_index:
    rr=[r for r in runs if r['problem_id']==pid and r['slot_present']]
    lineage_sets={a:{r['lineage_id'] for r in rr if r['arm']==a} for a in ('A','B')}
    canonical_sets={a:{r['canonical_url'] for r in rr if r['arm']==a} for a in ('A','B')}
    direct={r['lineage_id'] for r in rr if r['direct_read']}
    direct_urls={canonical(s['original_url']) for s in sources if s.get('problem_id')==pid and s.get('arm') in ('A','B') and s.get('direct_read')}
    fit={a:any(j['confirmed_fit']=='true' for j in judgments if j['problem_id']==pid and j['arm']==a) for a in ('A','B')}
    outcome='common' if all(fit.values()) else ('A_only' if fit['A'] else ('B_only' if fit['B'] else 'neither_confirmed'))
    pair_stats.append({'problem_id':pid,'strict_original_revision_verified':False,'executed_pair':True,
      'returned_url_union':len(canonical_sets['A']|canonical_sets['B']),
      'returned_url_intersection':len(canonical_sets['A']&canonical_sets['B']),
      'direct_read_url_union':len(direct_urls),
      'returned_lineage_union':len(lineage_sets['A']|lineage_sets['B']),
      'returned_lineage_intersection':len(lineage_sets['A']&lineage_sets['B']),
      'direct_read_lineage_union':len(direct),'confirmed_fit_outcome':outcome,
      'uninspected_or_unknown_ranks':sum(not r['direct_read'] for r in rr),
      'boundary':'neither_confirmed is an observed search outcome, not proof that the complete return union or web has no fit'})
trial_sources=[s for s in sources if s.get('role')=='trial_return']
summary={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'input_freeze_sha':'03d1e436cfa7dc209b57b19508ef4b2e75942824',
 'planned_queries':18,'actual_queries':sum(c['query_attempts'] for c in costs),'planned_rank_slots':90,'actual_rank_rows':len(runs),
 'source_rows':len(sources),'independent_works_counted':sum(s['count_toward_minimum'] for s in sources),
 'minimum_count_lineages':sorted(s['lineage_id'] for s in sources if s['count_toward_minimum']),
 'counted_works_by_first_role':dict(collections.Counter(s['role'] for s in sources if s['count_toward_minimum'])),
 'trial_return_url_union':len({r['canonical_url'] for r in runs if r['slot_present']}),
 'trial_direct_read_url_union':len({canonical(s['original_url']) for s in sources if s.get('arm') in ('A','B') and s.get('direct_read')}),
 'trial_return_lineage_union':len({r['lineage_id'] for r in runs if r['slot_present']}),
 'trial_direct_read_lineage_union':len({r['lineage_id'] for r in runs if r['direct_read']}),
 'strict_pair_denominator':0,'observed_pair_denominator':3,
 'arm_stats':arm_stats,'pair_stats':pair_stats,'confirmed_fit_outcomes':dict(collections.Counter(r['confirmed_fit_outcome'] for r in pair_stats)),
 'worldwide_recall':None,'author_decision_change':None,'time_saved':None,'actual_monetary_cost':None}
(ROOT/'evidence/counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
