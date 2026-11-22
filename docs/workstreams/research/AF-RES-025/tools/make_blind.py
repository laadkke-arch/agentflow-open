#!/usr/bin/env python3
"""Build route/rank-hidden candidate packets from locked returned slots.

This only transforms observations. It does not judge source truth. Run after all
three discovery bundles are committed; keep mapping away from the readers.
"""
import hashlib
import json
import pathlib

BASE=pathlib.Path(__file__).resolve().parents[1]

def rows(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def digest(value): return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p, data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in data))

questions={q['id']:q for q in rows(BASE/'questions.jsonl')}
source_by={}
slots=[]
all_candidates=[]
for name in ['arrow','cargo','jupyter']:
    stream=BASE/'streams'/name
    slots += rows(stream/'returns.jsonl')
    all_candidates += rows(stream/'candidates.jsonl')
    source=json.loads((stream/'sources-candidates.json').read_text())
    if isinstance(source,dict):source=source.get('sources',source.get('rows',[]))
    for s in source: source_by[s.get('source_id',s.get('id'))]=s

returned_slots=[{**r,'return_budget_variant':'raw_three_candidates'} for r in slots]
slots=list(returned_slots)
if (BASE/'returns.jsonl').exists():
    slots += [{**r,'return_budget_variant':'strict_three_source_urls'} for r in rows(BASE/'returns.jsonl') if r.get('candidate_id')]
seen={(r['question_id'],r['route'],r.get('candidate_id')) for r in returned_slots}
for r in all_candidates:
    k=(r['question_id'],r['route'],r.get('candidate_id'))
    if r.get('candidate_id') and k not in seen:
        slots.append({**r,'rank':None});seen.add(k)

source_ids={sid:'S-'+digest([s.get('source_url',s.get('url','')),s.get('version','')])[:12] for sid,s in source_by.items()}

def mask(value):
    if isinstance(value,list): return [mask(v) for v in value]
    if isinstance(value,dict): return {k:mask(v) for k,v in value.items() if k not in ['route','rank','checked_utc','first_seen_rank','first_seen_query','search_receipt_ids','sufficient_for_condition','opened_complete','cited_complete','verdict','self_verdict']}
    if isinstance(value,str):
        value=value.replace('R의59.0.0과 다른 판이 open되어', '별도 관측의 59.0.0과 다른 판이 열려')
        value=value.replace('G의같은원문Fossies접근실패는소급성공처리하지않음.', '같은 원문 Fossies 접근 실패를 소급 성공 처리하지 않음.')
        for old,new in source_ids.items():
            if old: value=value.replace(old,new)
    return value

packets={};mapping=[]
for row in slots:
    if not row.get('candidate_id') or row.get('candidate_class')=='empty':continue
    qid=row['question_id']
    identity=[qid,row['candidate_id']]
    key='B-'+digest(identity)[:12]
    question=questions[qid]
    p=packets.setdefault(key,{'blind_key':key,'question_id':qid,
       'question':{k:question[k] for k in ['title','purpose','scope','initial_url','input_path','input_sha256','known_names','mandatory_predicates']},
       'target_name':row.get('target_name'),'proposed_uses':[], 'citation_packages':[], 'sources':[]})
    use=row.get('proposed_use','')
    if use not in p['proposed_uses']:p['proposed_uses'].append(use)
    package={k:row.get(k,[]) for k in ['required_bundle','returned_citations','opened_evidence']}
    pk='P-'+digest(package)[:12]
    if not any(c['package_key']==pk for c in p['citation_packages']):
        p['citation_packages'].append({'package_key':pk,**mask(package)})
    for sid in row.get('source_ids',[]):
        s=source_by.get(sid)
        if s and not any(x.get('source_id')==source_ids[sid] for x in p['sources']):
            whitelist=['title','source_url','url','version','published_or_revised','published_date','sections_read','verified_content','limitations','producer']
            p['sources'].append({'source_id':source_ids[sid],**mask({k:s[k] for k in whitelist if k in s})})
    mapping.append({'question_id':qid,'route':row['route'],'rank':row['rank'],'candidate_id':row['candidate_id'],'blind_key':key,'package_key':pk,'record_type':'returned' if row.get('rank') in [1,2,3] else 'opened_not_returned','return_budget_variant':row.get('return_budget_variant','candidate_only')})

for p in packets.values():
    p['proposed_uses'].sort()
    p['citation_packages'].sort(key=lambda x:x['package_key'])
    p['sources'].sort(key=lambda x:x['source_id'])
out=sorted(packets.values(),key=lambda x:x['blind_key'])
write(BASE/'blind'/'packets.jsonl',out)
write(BASE/'evidence'/'blind-mapping.jsonl',mapping)
(BASE/'evidence'/'blind-source-map.json').write_text(json.dumps(source_ids,indent=2)+'\n')
for name,ids in [('arrow',range(1,5)),('cargo',range(5,9)),('jupyter',range(9,13))]:
    keep={f'Q{i:02}' for i in ids}
    write(BASE/'blind'/(name+'.jsonl'),[p for p in out if p['question_id'] in keep])
print(json.dumps({'packets':len(out),'mapped_records':len(mapping),'returned_slots':len(returned_slots),'empty_slots':sum(not r.get('candidate_id') or r.get('candidate_class')=='empty' for r in returned_slots),
  'packet_sha256':hashlib.sha256((BASE/'blind'/'packets.jsonl').read_bytes()).hexdigest()},indent=2))
