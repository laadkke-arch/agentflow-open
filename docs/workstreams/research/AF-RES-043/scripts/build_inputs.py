"""Build frozen AF-RES-043 stimuli and provenance from reviewed collection files.

No network, no model calls, no files outside this task. Run only before the
input seal; subsequent corrections require an amendment and a new file version.
"""
from pathlib import Path
import csv
import hashlib
import json

P = Path(__file__).resolve().parents[1]

def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def jl(path, rows):
    path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))

def write_csv(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})

collections = {name: json.loads((P/'collection'/name/'cases.json').read_text()) for name in ['natural','statistics','journals']}
cases=[]
for raw in collections['natural']:
    cid=raw['case_id']
    b=(f"소비 문서: {raw['consumer_title']}; pandas 1.5.3" if cid.startswith('N-P') else f"소비 문서: {raw['consumer_title']}; statsmodels 0.14.0")
    b+=f"\n소비 문서 시점: {raw['consumer_date']}\n관측 목적(요약): {raw['observed_purpose']}\n소비자가 명시한 대상 판: {raw['consumer_explicit_target_version']}\n원 href: {raw['original_raw_href']}"
    if cid=='N-S-01':
        b+='\n소비 예제 출력: 1926-07 Mkt-RF=2.96; 출력의 마지막 월은 2023-03. 원출력 복원과 오늘의 수정 계열 중 사용할 시간 의도는 명시되지 않았다.'
    if cid=='N-S-02':
        b+='\n소비 문서 고지(요약): 비교하는 Stata 예제와 데이터가 다르다.'
    l=(f"추가 판 주소: {raw['L']['url']}\n판: {raw['reconstructed_target_edition']}\n절 위치: {raw['L']['locator']}" if raw['L']['version_pinned'] else f"추가 위치(판 미확인): {raw['L']['url']}\n절 위치: {raw['L']['locator']}")
    xtext=raw['X']['text']
    if cid=='N-P-01': xtext='regular expression matching operations'
    if cid=='N-P-02': xtext='homogeneous array of fixed-size items'
    cquestion='관측된 소비 목적을 지금 수행할 때 원 href가 가리키는 설명·자료를 유지/교체/보류하는가? 선택된 좁은 주장과 목적만 판단한다.'
    if cid=='N-S-01': cquestion='60개월 이동 회귀 예제를 지금 수행할 때 이 참조와 월별 자료의 사용을 유지/교체/보류하는가? 원출력 복원과 현행 수정 계열 사용의 구분이 필요한지 명시한다.'
    hquestion='소비 문맥에 대응하는 과거 발행판의 해당 설명 또는 레코드를 확인했는가? 실제 도착한 판·절·문구를 보고하고, 소비자가 실제 사용한 판과 연구에서 추가한 판을 구별한다.'
    cases.append(dict(case_id=cid,stratum='natural',frame_id=raw['frame_id'],consumer_source_id=raw['consumer_source_id'],consumer_url=raw['consumer_url'],consumer_date=raw['consumer_date'],consumer_locator=raw['consumer_locator'],purpose=raw['observed_purpose'],original_href=raw['original_raw_href'],B_original_href_version_pinned=raw['B_already_pinned'],consumer_target_version_confirmed=False,old_url=raw['old_target_url'],old_locator=raw['old_target_locator'],old_version=raw['reconstructed_target_edition'],old_source_id=raw['old_target_source_id'],current_url=raw['current_target_url'],current_locator=raw['current_target_locator'],current_source_ids=raw['current_criterion_source_ids'],notice_url='미확인',notice_locator='미확인',B=b,L=l,X='저장 발췌: '+xtext,X_available=raw['X']['available'],X_contains_version_or_url_cue=raw['X']['contains_version_cue'],X_source_id=raw['X']['source_id'],X_locator=raw['X']['locator'],L_version_pinned=raw['L']['version_pinned'],L_kind=raw['L']['locator_kind'],L_granularity=raw['L']['granularity'],L_existed_at_consumption=raw['L']['existed_at_consumer_time'],L_existence_source_id=raw['L']['existence_source_id'],C_question=cquestion,H_question=hquestion,C_expected=raw['current_gold_action'],C_criterion_confirmed=raw['current_criterion_confirmed'],C_criterion_url=raw['current_target_url'],C_criterion_locator=raw['current_target_locator'],C_independent_edition=raw['current_criterion_independent_edition'],C_scope=raw['current_gold_scope'],C_hold_reason=raw.get('current_gold_hold_reason','해당 없음'),H_expected='publisher_edition_match',H_criterion_confirmed=raw['historical_strict_criterion_confirmed'],H_criterion_url=raw['old_target_url'],H_criterion_locator=raw['old_target_locator'],H_independent_edition=False,H_reconstructed_criterion_confirmed=raw['historical_reconstructed_criterion_confirmed'],limitations=raw['limits'],raw_case_file='collection/natural/cases.json',raw_case_id=cid))

for raw in collections['statistics']:
    cid=raw['case_id']; con=raw['consumer']; tar=raw['target']; e=raw['element_facts']
    b=f"소비 문서: {con['title']}; {con['publication_date']}.\n소비 목적(원문 요약): {con['purpose_observed']}\n소비자가 명시한 판: {con['explicit_edition']}\n소비 본문 문맥: {tar['reference_period']} 실질 GDP 증가율 최초 추계 {tar['original_value']}%; 단위 {tar['units']}.\n원 href: {con['original_href']}"
    x='저장 발췌: '+('1.6 percent' if cid=='T01' else '0.6%')
    cs=raw['tasks']['C']['criterion_sources']; hs=raw['tasks']['H']['criterion_sources']
    cases.append(dict(case_id=cid,stratum='correction_first',frame_id='R-S',consumer_source_id=raw['consumer_source_id'],consumer_url=con['url'],consumer_date=con['publication_date'],consumer_locator=con['href_locator'],purpose=con['purpose_observed'],original_href=con['original_href'],B_original_href_version_pinned=e['B_original_href_version_pinned'],consumer_target_version_confirmed=True,old_url=tar['original_url'],old_locator=tar['original_locator'],old_version=tar['original_publication_date'],old_source_id=e['X_source_id'],current_url=tar['current_same_period_source'],current_locator='동일 기준기간 행; collection/statistics/cases.json 및 해당 source locator 참조',current_source_ids=[s['source_id'] for s in cs],notice_url=raw['notice']['url'],notice_locator=raw['notice']['locator'],B=b,L=raw['L'],X=x,X_available=True,X_contains_version_or_url_cue=False,X_source_id=e['X_source_id'],X_locator=e['X_locator'],L_version_pinned=True,L_kind='dated_publisher_release',L_granularity='dated statistical release',L_existed_at_consumption=e['L_existed_at_consumer_time'],L_existence_source_id=e['L_existence_evidence'],C_question=raw['tasks']['C']['prompt']+' 판단 대상: '+raw['tasks']['C']['action_object'],H_question=raw['tasks']['H']['prompt'],C_expected=raw['tasks']['C']['expected_action'],C_criterion_confirmed=True,C_criterion_url=cs[-1]['url'],C_criterion_locator=cs[-1]['locator'],C_independent_edition=True,C_scope=raw['tasks']['C']['required_support'],C_hold_reason='해당 없음',H_expected='publisher_edition_match',H_criterion_confirmed=True,H_criterion_url=hs[0]['url'],H_criterion_locator=hs[0]['locator'],H_independent_edition=raw['sensitivity']['S_I_H_direct_publisher_edition'],H_reconstructed_criterion_confirmed=True,reference_period=tar['reference_period'],vintage_values=raw['vintage_values'],limitations=raw['limitations'],raw_case_file='collection/statistics/cases.json',raw_case_id=cid))

for raw in collections['journals']:
    cid=raw['case_id'];con=raw['consumer'];tar=raw['target'];c=raw['tasks']['C'];h=raw['tasks']['H']
    b=f"소비 문서: {con['title']}; {con['published']}, {con['version']}.\n소비 목적(원문 요약): {con['observed_purpose']}\n명시 인용판: {con['explicit_target_version']}\n원 href: {con['actual_target_href']}"
    if cid=='J01': b+='\n소비 문서의 실제 분석 인원은 3,806명이다. 원 논문의 코호트 설명을 참조한다.'
    x='저장 발췌: '+('Three thousand seven hundred and sixteen' if cid=='J01' else 'numerous mitochondrial genes')
    cq='관측된 소비 목적에서 원 href의 '+c['focus']+'을 지금 재사용할 때 그 주장을 유지/교체/보류하는가?'
    if cid=='J01': cq+=' 판단 대상은 원 논문의 코호트 인원 주장이다. 소비 문서 자체의 3,806명 수치를 수정하라는 질문이 아니다.'
    hq='소비자가 명시한 2018 발행저작에서 '+('sepsis 분류 환자수' if cid=='J01' else 'mTERF22의 여러 미토콘드리아 유전자 발현 역할')+'에 관한 원문을 확인했는가? 그 판의 실제 문구를 보고하고 X가 있으면 대조한다.'
    cases.append(dict(case_id=cid,stratum='correction_first',frame_id='R-J',consumer_source_id=con['source_id'],consumer_url=con['opened_fulltext_url'],consumer_date=con['published'],consumer_locator=con['locator'],purpose=con['observed_purpose'],original_href=con['actual_target_href'],B_original_href_version_pinned=True,consumer_target_version_confirmed=True,old_url=tar['old_url'],old_locator=tar['locator'],old_version=tar['version'],old_source_id=tar['source_id'],current_url=raw['correction']['url'],current_locator=raw['correction']['locator'],current_source_ids=c['criterion_source_ids'],notice_url=raw['correction']['url'],notice_locator=raw['correction']['locator'],B=b,L=raw['L'],X=x,X_available=True,X_contains_version_or_url_cue=False,X_source_id=raw['X_metadata']['source_id'],X_locator=raw['X_metadata']['locator'],L_version_pinned=False,L_work_specific=True,L_kind='work_specific_direct_publisher_locator',L_granularity='2018 work; immutable publication-version address 미확인',L_existed_at_consumption=raw['L_metadata']['existed_at_consumer_date'],L_existence_source_id=raw['L_metadata']['historical_existence_evidence'],C_question=cq,H_question=hq,C_expected=c['expected_action'],C_criterion_confirmed=c['criterion_confirmed'],C_criterion_url=c['criterion_url'],C_criterion_locator=c['criterion_locator'],C_independent_edition=c['independent_publication_criterion'],C_scope=c['expected_action_target'],C_hold_reason='해당 없음',H_expected='publisher_edition_match',H_criterion_confirmed=h['criterion_confirmed'],H_criterion_url=h['criterion_url'],H_criterion_locator=h['criterion_locator'],H_independent_edition=h['independent_publication_criterion'],H_reconstructed_criterion_confirmed=h['criterion_confirmed'],limitations=[raw['L_metadata']['increment_over_B'],raw['counterexample'],con['time_intent']],raw_case_file='collection/journals/cases.json',raw_case_id=cid))

assert len(cases)==8
orders=[['B','BLX','BL','BX'],['BL','BX','B','BLX'],['BX','BL','B','BLX'],['BLX','B','BX','BL']]
configs={'B':['B'],'BL':['B','L'],'BX':['B','X'],'BLX':['B','L','X']}
components=[];cards=[];key=[];versions=[]
for i,c in enumerate(cases,1):
    c['case_index']=i
    components.append({k:c[k] for k in ['case_id','B','L','X','X_available']})
    k={a:v for a,v in c.items() if a not in ['B','L','X']}; k['component_hashes']={a:sha(c[a]) for a in ['B','L','X']};key.append(k)
    for pos,config in enumerate(orders[(i-1)%4],1):
        body='\n\n'.join(c[e] for e in configs[config])
        cards.append(dict(card_id=f"{c['case_id']}-{config}",case_id=c['case_id'],case_index=i,stratum=c['stratum'],config=config,elements=configs[config],body=body,sha256=sha(body),component_hashes={e:sha(c[e]) for e in configs[config]},presentation_index=(i-1)*4+pos,within_case_order=pos,task_order=['C','H'] if i%2 else ['H','C'],tasks={'C':c['C_question'],'H':c['H_question']},factor_complete=c['X_available'] and c['L_kind']!='replacement_locator_only'))
    versions.append({k:v for k,v in c.items() if k not in ['B','L','X','C_question','H_question']})

jl(P/'components.jsonl',components);jl(P/'cards.jsonl',cards);jl(P/'key.jsonl',key);write_csv(P/'versions.csv',versions)

sources=[]
for p in sorted((P/'collection').glob('*/sources.jsonl')):
    for l in p.read_text().splitlines():
        r=json.loads(l);r['collection_file']=str(p.relative_to(P))
        if r.get('counted') and not r.get('count_group'):
            kind=r['source_kind']
            r['count_group']='consumer' if kind.startswith('consumer') else 'notice' if ('notice' in kind) else 'target'
        r.setdefault('count_group','excluded_or_additional')
        sources.append(r)
assert len({r['source_id'] for r in sources})==len(sources)
jl(P/'sources.jsonl',sources)

# The collection CSVs remain exact original ledgers. This union provides a
# single task-level entry point without silently harmonizing their meanings.
frame=[]
for name in ['natural','statistics','journals']:
    p=P/'collection'/name/'frame.csv'
    with p.open() as f:
        for ix,r in enumerate(csv.DictReader(f),1):
            frame.append({'collection':name,'collection_row':ix,'source_file':str(p.relative_to(P)),**r})
write_csv(P/'frame.csv',frame)

seal={'phase':2,'scope_remote_commit':'a6cc61d4c2b6baf7cae47569c1454b371986ce47','cases':8,'cards':32,'planned_judgments':64,'planned_pairs':64,'cards_sha256':sha((P/'cards.jsonl').read_text()),'key_sha256':sha((P/'key.jsonl').read_text()),'components_sha256':sha((P/'components.jsonl').read_text()),'source_counted_groups':{g:sum(r.get('counted',False) and r.get('count_group')==g for r in sources) for g in ['consumer','target','notice','rule']},'complete_four_factor_cases':sum(c['X_available'] and c['L_kind']!='replacement_locator_only' for c in cases),'strict_historical_criteria':sum(c['H_criterion_confirmed'] for c in cases),'current_criteria':sum(c['C_criterion_confirmed'] for c in cases),'blind_readers_receive':['cards.jsonl filtered to assigned cases','READER_PROTOCOL.md'],'blind_readers_do_not_receive':['key.jsonl','versions.csv','components.jsonl','collection/','sources.jsonl'],'limitations':['Missing UCLA historical X is an explicit missing-factor stimulus, not a recovered quotation.','Four natural consumers do not establish their actual external target edition. Reconstructed-edition attainment is reported separately.','PLOS direct work URLs add access/section information; immutable-version-only effects are not isolated.','The original fixed crossover order is retained; it is not fully position-balanced.']}
(P/'evidence'/'input-seal.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(seal,ensure_ascii=False,indent=2))
