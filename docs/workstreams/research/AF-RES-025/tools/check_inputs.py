#!/usr/bin/env python3
"""Check sealed case/query inputs without invoking any search or changing inputs."""
import argparse
import collections
import hashlib
import json
import pathlib

BASE=pathlib.Path(__file__).resolve().parents[1]
REPO=BASE.parents[3]
p=argparse.ArgumentParser()
p.add_argument('--allow-partial',action='store_true')
a=p.parse_args()

def read_lines(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

questions=[]
queries=[]
for stream in sorted((BASE/'streams').glob('*')):
    qfile=stream/'questions.jsonl'
    rfile=stream/'queries.jsonl'
    if qfile.exists(): questions.extend(read_lines(qfile))
    if rfile.exists(): queries.extend(read_lines(rfile))
errors=[]
checks=[]

def check(condition, detail):
    checks.append({'passed':bool(condition),'detail':detail})
    if not condition: errors.append(detail)

qids=[q['id'] for q in questions]
check(len(qids)==len(set(qids)),'unique question IDs')
if not a.allow_partial:
    check(set(qids)=={f'Q{i:02}' for i in range(1,13)},'12 planned question IDs')
    check(collections.Counter(q['scope'] for q in questions)=={'whole':6,'part':6},'six whole and six part cases')
byq={q['id']:q for q in questions}
for q in questions:
    input_file=REPO/q['input_path']
    check(input_file.is_file(),q['id']+' full first draft accessible in local input cache')
    if input_file.is_file():
        check(hashlib.sha256(input_file.read_bytes()).hexdigest()==q['input_sha256'],q['id']+' input hash matches')
    check('2021-01-01'<=q['date'][:10]<='2024-12-31',q['id']+' first design date in locked period')
    check(bool(q.get('initial_url')) and bool(q.get('initial_sections')),q['id']+' source and read locations')
    check(bool(q.get('mandatory_predicates')),q['id']+' mandatory predicates recorded')
    rs=[r for r in queries if r['question_id']==q['id']]
    check({r['route'] for r in rs}=={'G','R'} and len(rs)==2,q['id']+' paired G/R query rows')
    if len(rs)!=2:continue
    for r in rs:
        check(r['input_path']==q['input_path'] and r['input_sha256']==q['input_sha256'],r['id']+' same full draft')
        check(0<len(r['query_strings'])<=3,r['id']+' at most 3 sealed queries')
        check(r['engine']=='system1_search_query',r['id']+' same engine')
        check(r['results_seen_before_seal'] is False,r['id']+' result-free query declaration')
        check(r['order']==(1 if ((int(q['id'][1:])%2==1)==(r['route']=='G')) else 2),r['id']+' alternating route order')
    check(rs[0]['site_scope']==rs[1]['site_scope'] and rs[0]['language']==rs[1]['language'],q['id']+' same public scope/language')
    check(rs[0]['budget']==rs[1]['budget'],q['id']+' equal budget ceilings')
result={'mode':'partial diagnostic' if a.allow_partial else 'input seal check','question_count':len(questions),'route_count':len(queries),'checks':checks,'errors':errors,'passed':not errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
