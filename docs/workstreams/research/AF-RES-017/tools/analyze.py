"""Reproducible ledger normalization and arithmetic; no network or source inference."""
import json, re, statistics, collections, hashlib
from pathlib import Path

P = Path(__file__).resolve().parents[1]
STOP = set('a an the and or of to for in on at by with from as is are was were be been being this that these those it its can could will would should may might have has had do does did not no into through using use used without while across each any all both only also than then their our your we they you i'.split())
def read(path): return json.loads((P/path).read_text())
def write(path, data):
    q=P/path; q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def tokens(s):
    words=re.findall(r'[a-z0-9]+',s.lower())
    def singular(w):
        if len(w)>4 and w.endswith('ies'): return w[:-3]+'y'
        if len(w)>3 and w.endswith('s') and not w.endswith(('ss','us','is')): return w[:-1]
        return w
    return sorted({singular(w) for w in words if w not in STOP})
def value(x):
    if isinstance(x,dict):return x.get('value',x.get('text',str(x)))
    return x
def summary(values):
    return {'n':len(values),'median':statistics.median(values),'min':min(values),'max':max(values)} if values else {'n':0,'median':None,'min':None,'max':None}

cases=read('cases/CASES.json')
byid={c['id']:c for c in cases}
baseline={}
for row in read('evidence/root/current-search.json')['rows']:
    baseline[row['id']]={'query':row['q'],'current_easy_hit':row['current_easy_hit'],'reason':row['reason'],'at_utc':row['at_utc'],'source':'evidence/root/current-search.json','body_verified':row['current_easy_hit']=='yes','retrospective_leakage':row['retrospective_leakage']}
for row in read('evidence/prs/simple-search-controls.json'):
    hit=row.get('current_easy_hit',False)
    baseline[row['id']]={'query':row['query'],'current_easy_hit':('yes' if hit else 'no'),'body_verified':row.get('body_verified',False),'reason':row.get('result'),'at_utc':row['at_utc'],'source':'evidence/prs/simple-search-controls.json','retrospective_leakage':row.get('retrospective_leakage')}
    if hit and not row.get('body_verified'):baseline[row['id']]['current_easy_hit']='unknown'
for row in read('evidence/blogs/ordinary-query-diagnostic.json')['cases']:
    raw=row.get('target_hit')=='hit'
    body=row.get('body_verified',False)
    leak=row.get('retrospective_leak',False) or row.get('retrospective_leakage_detected',False)
    explicit=row.get('current_easy_hit')
    if explicit is not None:
        hit='yes' if explicit is True or explicit=='yes' else ('excluded_leak' if leak else 'no')
    else:hit='excluded_leak' if leak else ('yes' if raw and body else ('unknown' if raw else 'no'))
    baseline[row['case_id']]={'query':row['query'],'current_easy_hit':hit,'body_verified':body,'target_seen_in_results':raw,'retrospective_leakage':leak,'reason':row.get('body_verification_note',row.get('interpretation_limit')),'at_utc':row.get('run_date_utc'),'source':'evidence/blogs/ordinary-query-diagnostic.json'}

metrics=collections.defaultdict(list)
for c in cases:
    desc=c.get('official_description') or c.get('official_target_description') or {}
    c['official_description']=desc
    need=c['need_statement']; need['word_count']=len(need['text'].split())
    need.setdefault('author','작업자 요약; source wording is not a contemporaneous user query')
    c.setdefault('coding_author','A: 작업자 / 내부 수집 담당; GPT-6 Astra Pro')
    nt=tokens(need['text']);dt=tokens(desc.get('text',''))
    c['lexical_overlap']={'shared_core_token_count':len(set(nt)&set(dt)) if dt else None,'shared_core_tokens':sorted(set(nt)&set(dt)),'need_tokens':nt,'official_description_tokens':dt,'algorithm':'LEX-v1; exact lowercased alphanumeric unique tokens, fixed stoplist, simple suffix normalization','description_source_url':desc.get('source_url',desc.get('url')),'limit':'Short selected official excerpt or marked paraphrase; not semantic similarity, historical discoverability, or full-page vocabulary.','computed_by':'deterministic tools/analyze.py'}
    if not dt:c['lexical_overlap']['unconfirmed_reason']='미확인(해당 시점 기능의 공식 설명 본문 확보 필요)'
    c['current_search_diagnostic']=baseline[c['id']]
    prominence=c.get('prominence_at_decision')
    if isinstance(prominence,str):c['prominence_at_decision']={'verdict':'unknown','reason':prominence}
    c['historical_retrievability']={'verdict':'unknown','reason':'No decision-date query replay with historically admissible indexed candidates; existence alone is insufficient.'}
    dd=c['decision_date'];fd=c['discovery_date']
    decision_dated=bool(re.match(r'^\d{4}-\d{2}',dd))
    discovery_dated=bool(re.match(r'^\d{4}-\d{2}',fd))
    actual_outcome=not c['outcome'].startswith('미확인')
    c['episode_eligibility']={'initial_decision_month_documented_or_public_code_proxy':decision_dated,'discovery_or_assessment_month_documented':discovery_dated,'external_entity_identified':bool(c['missed'].get('name')),'public_outcome_record':actual_outcome,'minimum_dated_episode_criteria_met':decision_dated and discovery_dated and actual_outcome,'scope_note':'Dates of first public custom code are proxies, not proof of the private initial decision. Known-rejected controls need a dated assessment, not an invented discovery.'}
    c.setdefault('strict_late_discovery_eligible',False)
    for key,m in c['cost_indicators'].items():
        v=m.get('value') if isinstance(m,dict) else None
        if isinstance(v,(int,float)) and not isinstance(v,bool) and not m.get('comparison'):
            metrics[key].append({'case_id':c['id'],'value':v,'unit':m.get('unit'),'qualification':m.get('scope',m.get('qualifier',m.get('note',''))),'evidence':m.get('evidence')})
    c['cost_status']='reported_metric' if c['cost_indicators'] else '비용 미확인(변경 diff·실제 이행 일정·작성자 비용 진술 추가 확보 필요)'
write('cases/CASES.json',cases)
write('evidence/lexical-protocol.json',{'id':'LEX-v1','stopwords':sorted(STOP),'token_pattern':'[a-z0-9]+','normalization':['lowercase','ies suffix if length>4 becomes y','final s removed if length>3 except ss/us/is','unique token sets','no synonyms or stemming beyond these suffixes'],'word_limit':25,'need_author':'worker paraphrase unless explicitly marked quote','official_description_selection':'collector-selected <=25-word excerpt/title/headline; root sources retain marked paraphrases','warning':'Post-outcome excerpt and need selection can inflate or suppress overlap. Use as descriptive proxy only.'})
write('evidence/current-search-summary.json',{'window':'2026-11-21 UTC current index','queries':len(baseline),'count':dict(collections.Counter(x['current_easy_hit'] for x in baseline.values())),'cases':baseline,'interpretation':'One target-free 1–2 noun query per case; collector knows target. Body verification required for hit. Current nonhit is not proof that ordinary search cannot help; current hit is not proof of zero product value. Historical retrieval and counterfactual benefit remain unknown.'})
stats={'observed_records':len(cases),'source_family':dict(collections.Counter(c['source_family'] for c in cases)),'organization':dict(collections.Counter(c['organization'] for c in cases)),'form':dict(collections.Counter(c['missed_form'] for c in cases)),'contribution':dict(collections.Counter(c['missed_contribution'] for c in cases)),'relation':dict(collections.Counter(c['missed_relation'] for c in cases)),'late_status':dict(collections.Counter(c['late_discovery_status'] for c in cases)),'outcome':dict(collections.Counter(c['outcome'] if not c['outcome'].startswith('미확인') else '미확인' for c in cases)),'existence':dict(collections.Counter(c['existed_at_decision']['verdict'] for c in cases)),'strict_late_ids':[c['id'] for c in cases if c['strict_late_discovery_eligible']],'minimum_dated_episode_ids':[c['id'] for c in cases if c['episode_eligibility']['minimum_dated_episode_criteria_met']],'cost_unconfirmed_ids':[c['id'] for c in cases if not c['cost_indicators']],'numeric_cost_ids':sorted({v['case_id'] for values in metrics.values() for v in values}),'cost_metrics':{k:{**summary([x['value'] for x in v]),'observations':v} for k,v in metrics.items()},'lexical_overlap':summary([c['lexical_overlap']['shared_core_token_count'] for c in cases if c['lexical_overlap']['shared_core_token_count'] is not None]),'current_search':dict(collections.Counter(x['current_easy_hit'] for x in baseline.values())),'by_relation':{}}
for rel in sorted(stats['relation']):
    rows=[c for c in cases if c['missed_relation']==rel];ids={c['id'] for c in rows}
    stats['by_relation'][rel]={'n':len(rows),'ids':sorted(ids),'existed_yes':sum(c['existed_at_decision']['verdict']=='yes' for c in rows),'well_known':sum(c['prominence_at_decision']['verdict']=='well_known' for c in rows),'overlap':summary([c['lexical_overlap']['shared_core_token_count'] for c in rows if c['lexical_overlap']['shared_core_token_count'] is not None]),'metrics':{k:summary([x['value'] for x in vv if x['case_id'] in ids]) for k,vv in metrics.items() if any(x['case_id'] in ids for x in vv)}}
write('evidence/statistics.json',stats)
print(json.dumps({k:stats[k] for k in ['observed_records','source_family','late_status','outcome','existence','strict_late_ids','minimum_dated_episode_ids','cost_unconfirmed_ids','lexical_overlap','current_search']},ensure_ascii=False))
