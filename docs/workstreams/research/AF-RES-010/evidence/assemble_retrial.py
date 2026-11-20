"""Assemble recorded observations; never performs searches or changes judgments.

Run from any cwd: python <this-file> --phase p1|all.
The p1 phase publishes only P1 observations in the main log/source ledger.
"""
import argparse
import copy
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]
E = P / 'evidence'


def read(name):
    return json.loads((E / name).read_text())


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


parser = argparse.ArgumentParser()
parser.add_argument('--phase', choices=['p1', 'all'], default='all')
args = parser.parse_args()
problems = {'P1'} if args.phase == 'p1' else {'P1', 'P2'}

sources = []
excluded = []
for filename in ['retrial-root-sources.json', 'retrial-extra-sources.json', 'retrial-p2-extra-sources.json']:
    d = read(filename)
    sources += d['sources']
    excluded += d.get('excluded', [])

judgments = []
for filename in ['retrial-root-judgments.json', 'retrial-extra-judgments.json', 'retrial-p2-extra-judgments.json']:
    for original in read(filename)['judgments']:
        j = copy.deepcopy(original)
        j['source_ids'] = j.get('source_ids', [j.get('source_id')])
        j['family'] = j.get('family', j.get('candidate_family'))
        j['representations'] = sorted({q[3:5] for q in j['query_ids']})
        if j['candidate_id'] in ['D02', 'RP2-C06']:
            j['origin_family_before_conservative_grouping'] = j['family']
            j['family'] = 'source_variant_and_editorial_decision'
            j['grouping_note'] = 'TEI/구술사/FEMA의 원자료와 선택된 해석 분리를 하나의 넓은 family로 보수 집계; 서로 다른 새 알고리즘이라고 하지 않는다.'
        judgments.append(j)

gao = next(j for j in judgments if j['candidate_id'] == 'RP2-C05')
bad = copy.deepcopy(gao)
bad.update(candidate_id='RP2-C05-M', proposed_use='허용오차 이하의 작은 상충 수정은 표시·검토 없이 실사값 우선으로 덮어쓰는 적용', label='SURFACE_OR_CONSTRAINT_MISMATCH', bucket='near_miss')
bad['candidate_name'] = '허용오차 이내 차이의 무조사 조정을 상충 수정의 무음 덮어쓰기로 옮기는 오용'
bad['explicit_setting'] = '같은 기록ID의 두 오프라인 수정이 모두 정당한 입력인데, 차이가 작다는 임계값 판정만으로 한 값을 우선하고 다른 수정·출처·충돌 표시를 남기지 않는 설정.'
bad['mapping'] = [
    {'source_relation': '일부 실사 절차는 허용오차 이내 수량 차이를 추가 조사 없이 장부에 반영한다.',
     'target_relation': '작다고 분류한 상충 수정은 사용자 검토 없이 한 값으로 덮어쓰고 다른 대안을 버린다.',
     'status': 'H_misuse_mapping_with_constraint_violation'}
]
bad['bridge'] = ['H: P2는 작은 수정도 상충하면 확인·해결 가능해야 한다. 무음 덮어쓰기 규칙을 제거하고 원 대안을 보존해야 한다.']
bad['requirement_scope_notes'] = {
    'offline_read_write': 'not_in_scope',
    'preserve_conflicting_changes': 'violated_by_proposed_use: 작은 차이라는 이유로 정당한 수정이 소리 없이 소실됨',
    'inspect_and_resolve_conflicts': 'violated_by_proposed_use: 차이와 원 대안이 표시되지 않아 확인·해결할 수 없음',
    'export': 'not_in_scope'
}
bad['minimum_next_check'] = {
    'input': '같은 기준판 r7에 대해 A는 note의 한 글자를 수정하고 B는 다른 유효한 한 글자를 수정한다. 작은 차이 임계값에 둘 다 포함되도록 하고 A→B 및 B→A 도착 순서를 바꾼다.',
    'observe': '원 대안·출처·충돌 표시가 없이 한 값만 남으면 제안된 오용의 필수 조건 위반을 관측한다. 원 대안과 검토 경로가 남으면 이 오용 설정과 다른 구현이다.',
    'executed': False,
    'if_pass': '두 대안 보존·충돌 표시를 확인해도 이 무음 덮어쓰기 설정의 채택 성공으로 세지 않는다. 올바른 사용 방식으로 별도 판정한다.',
    'if_fail': '수정 소실 또는 충돌 은폐가 있으면 근접 오답 판정을 유지한다.'
}
bad['counting_note'] = '같은 family의 다른 사용 방식; (a)와(c)에 각각 한 번 나타나지만 전체 고유 family를 늘리지 않는다.'
judgments.append(bad)

all_source_map = {s['id']: s for s in sources}
for j in judgments:
    j['novelty_baseline'] = 'AF-RES-002@62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1; evidence/baseline-comparison.json'
    if j['bucket'] == 'new_candidate':
        j['novelty_scope'] = '기존 조사에 없던 출발 분야 관계·조건의 후보. 새로운 소프트웨어 알고리즘/이론의 발명은 입증하지 않음.'
    if j['candidate_id'] == 'D01':
        j['alternate_result_urls'] = ['https://shop.process-tech.com/Documentation/Document/ynrzqZ/174868.pdf', 'https://www.turckbanner.my/attachment/174868_en.pdf']

for problem in ['P1', 'P2']:
    js = [j for j in judgments if j['problem'] == problem]
    ids = {s for j in js for s in j['source_ids']}
    save(E / (problem.lower() + '-judgments.json'), {'problem': problem, 'T_protocol_commit': '2b798c7d2b7355b649691c18de196104ceabb0f0', 'judgments': js})
    save(E / ('retrial-' + problem.lower() + '-sources.json'), {'count_group': 'q5_candidate_only', 'sources': [s for s in sources if s['id'] in ids], 'excluded': [x for x in excluded if any(q.startswith(problem) for q in x.get('query_ids', []))]})

constraints = {
 'P1': {'A':'항목별 실패 격리','B':'성공 결과 보존','C':'중단 후 재시도','D':'같은 입력의 중복 공개 방지','E':'실패 확인','F':'자체 운영 가능성'},
 'P2': {'A':'오프라인 읽기·쓰기','B':'복구 후 병합/충돌 보존','C':'상충 수정 확인·해결','D':'사용자 데이터 내보내기'}
}
# Letters are the intended constraint projections, not a claim that analogy terms
# retain the full original semantics. The full fixed text remains in SCOPE.md.
mentions = {
 'P1-R0':['ABCDEF','','AB','CDE','F','AB','ABCDE','CDEF'],
 'P1-R1':['ABCD','AE','CD','BC','ABE','','ABC','BD'],
 'P1-R2':['CD','AB','BCE','CD','CD','D','AB','AB'],
 'P1-R3':['D','ABCE','CD','BE','C','AB','ACE','ACD'],
 'P2-R0':['ABCD','A','BC','D','','ABC','BCD','BCD'],
 'P2-R1':['BCD','BC','AB','BC','BCD','','BC','ACD'],
 'P2-R2':['AB','A','BC','ABC','AB','B','BC','BC'],
 'P2-R3':['BC','BC','BC','BC','BC','BC','BC','BC']
}
notes = {
 'R0':'원문 전체 또는 정확한 연속 구절. 부분 인용에서 빠진 조건은 전체 요구에서 제거된 것이 아니다.',
 'R1':'Functional Basis식 기능 투영 H; Store information은 NIST 원형 Provision의 signal 허용을 뜻하지 않는다. 흐름·불변식은 별도 대조한다.',
 'R2':'모순의 개선/악화 쌍을 적은 질의이며 TRIZ 행렬 셀을 실제 조회한 실험은 아니다.',
 'R3':'분야 용어로 옮긴 H 투영. 분야의 동의어와 P1/P2 불변식이 같은 의미인지 열린 원문에서 판정한다.'
}
special = {
 'P1-R1-06':'의도적으로 너무 넓은 동사·흐름 질의. Signal Routing이 나왔고 B07 본문에서 내구성 관계가 없는 오탐으로 판정.',
 'P2-R1-06':'의도적으로 너무 넓은 기능어 질의. 현재 store combine API가 나왔고 D03 본문에서 분기 병합과 다른 관계로 확인.',
 'P1-R1-08':'without central service는 검색의 추가 제한이며 P1 필수 조건이 아니다. 자체 운영 가능한 중앙 서비스를 잘못 배제할 위험을 기록한다.',
 'P1-R2-01':'repeating/reliability가 과학적 replicability로 이동했다. 반복 성공의 정의와 중복 공개 금지의 대상이 사라진 실제 오탐 B14.',
 'P1-R3-01':'once per cell cycle을 once per same input으로 옮길 때 주기/재시작 경계가 달라진다. RP1-B09-M은 잘못된 적용의 근접 오답.',
 'P2-R3-04':'repair는 한 가닥을 제거할 수 있다. 같은 기록의 두 정당한 수정 보존 속성이 사라졌으며 C08 근접 오답으로 확인.',
 'P2-R3-06':'동일 환자 판별로 문제가 바뀌었다. 같은 기록ID의 상충 내용 판정과 달라 C07 표면 오탐으로 확인.',
 'P2-R3-07':'물리 수량의 참값·허용오차는 정당한 복수 수정 의도와 다르다. RP2-C05-M을 별도 적용 반례로 기록.'
}

plan = {q['id']:q for q in read('query-plan.json')['queries']}
web = read('web-search-runs.json')['queries']
native = read('native-search-runs.json')['runs']
metadata = {q['query_id']:q for q in read('web-returned-metadata.json')['queries']}
all_rows = []
for raw in web + [r for r in native if r['parent_query']]:
    q = copy.deepcopy(raw)
    parent = q.get('parent_query', q['id'])
    spec = plan[parent]
    p, r = spec['problem'], spec['representation']
    q['problem'], q['representation'] = p, r
    q['verbatim_or_transformed'] = spec['verbatim_or_transformed']
    letters = mentions[parent[:5]][int(parent[-2:])-1]
    q['preserved_constraints'] = [constraints[p][x] for x in letters]
    q['lost_or_unqueried_constraints'] = [v for k,v in constraints[p].items() if k not in letters]
    q['preservation_semantics'] = '의도된 부분 투영이며 원분야 단어가 제약을 실제 보장한다는 뜻은 아님'
    q['projection_note'] = notes[r] + ' ' + special.get(parent, '')
    if r == 'R3':
        q['lost_or_unqueried_constraints'] += ['동일성·시간·실패 단위의 소프트웨어 의미를 원문 대조로 복구해야 함']
    q['execution_status'] = q.get('execution_status', 'results_observed')
    q['opened'] = []
    q['judgments'] = []
    for j in judgments:
        if q['id'] not in j['query_ids']:
            continue
        for sid in j['source_ids']:
            s = all_source_map[sid]
            if not any(o['source_id'] == sid for o in q['opened']):
                q['opened'].append({'source_id':sid,'url':s['url'],'outcome':'body_read','level':s['level'],'read_location':s['sections_read']})
        q['judgments'].append({k:j[k] for k in ['candidate_id','family','T','label','bucket','far_domain']})
    for x in excluded:
        if q['id'] in x.get('query_ids', []):
            q['opened'].append({'source_id':x['id'],'url':x['url'],'outcome':'excluded_no_body','reason':x['reason']})
    for hit in q['results']:
        matched = [s['id'] for s in sources if s['url'] == hit['url']]
        hit['body_source_ids'] = matched
        hit['read_status'] = 'D1_body_read' if matched else 'D0_only_in_this_url_window'
    if q['id'] in metadata:
        opened_urls = {o['url'] for o in q['opened']}
        q['followed_outside_top3'] = [hit for hit in metadata[q['id']]['results'][3:] if hit['url'] in opened_urls]
    if q['execution_status'] in ['result_not_validated', 'site_error_stale_results']:
        q['screening_decision'] = '질의 결과 검증 실패로 분석 제외. 빈 결과·오탐·근접 오답·후보 부재로 세지 않는다.'
    elif not q['results'] and not q['opened']:
        q['screening_decision'] = '해당 제출에서 빈 결과를 관측했다. 전체 검색 공간의 후보 부재나 오탐으로 세지 않는다.'
    elif any(o['outcome'] == 'body_read' for o in q['opened']):
        q['screening_decision'] = '선택한 원리 후보/반례의 본문을 판정; 나머지 상위 결과는 D0로 남김.'
    elif q['opened']:
        q['screening_decision'] = '원문 열람을 시도했으나 본문을 확인하지 못한 자료는 excluded로 기록. 오탐·근접 오답으로 세지 않는다.'
    else:
        q['screening_decision'] = '반환 결과를 기록했으나 원문 판정은 미선택. 오탐/근접 오답/부재로 세지 않는다.'
    if parent in ['P2-R1-01','P2-R1-07','P2-R2-06','P2-R2-07'] and q['system'].startswith('general_web'):
        q['existing_candidate_note'] = 'TreeDB/PaPoC2022 기존 재발견. 고정 입력에서 이미 확인한 자료이므로 다시 열어 재분석하지 않고 새 후보에서 제외.'
    if parent == 'P2-R2-01' and q['system'].startswith('general_web'):
        q['existing_candidate_note'] = 'Git merge 기존 재발견; 새 원거리 후보에서 제외.'
    all_rows.append(q)

selected = [r for r in all_rows if r['problem'] in problems]
log = {'schema':'AF-RES-010 search observations v1','scope_commit':'ebcca564df68377cc116634dcdab1695be69c0e8','phase':args.phase,
       'ranking_note':'일반 웹은 각 단일 질의 도구 반환의 첫3개 관측 창. 엔진 전체 절대 순위·전수 검토·정밀도가 아님.',
       'native_note':'16개 사전 질의 제출; P1 전체문은 한 번 재확인해도 이전 결과가 남아 1개 query의 결과 미검증. 나머지15개는 결과 또는 빈 결과 관측. control1회/재확인1회는64개에 추가하지 않음.',
       'queries':selected,'control_runs':[r for r in native if not r['parent_query']],
       'supplemental':'evidence/retrial-supplemental-searches.json',
       'preflight_excluded':[{'system':'Google Patents native','observation':'public endpoint 503; not a successfully searched second system'},{'system':'Semantic Scholar API','observation':'429; no account/API-key bypass; not counted'}]}
save(P/'SEARCH_LOG.json',log)
for problem in problems:
    save(E/(problem.lower()+'-search-runs.json'),{'problem':problem,'queries':[r for r in all_rows if r['problem']==problem]})

count_rows=[]
for p in ['P1','P2']:
    for r in ['R0','R1','R2','R3']:
        relevant=[j for j in judgments if j['problem']==p and r in j['representations']]
        row={'problem':p,'representation':r,'unique_web_queries':8,'planned_native_queries':2}
        for bucket in ['new_candidate','surface_false_positive','near_miss','insufficient','rediscovery','technical_support']:
            row[bucket]=len({j['family'] for j in relevant if j['bucket']==bucket})
            row[bucket+'_ids']=[j['candidate_id'] for j in relevant if j['bucket']==bucket]
        row['new_far_families']=len({j['family'] for j in relevant if j['bucket']=='new_candidate' and j['far_domain']})
        row['distinct_opened_sources']=len({s for j in relevant for s in j['source_ids']})
        count_rows.append(row)
counts={'unit':'problem × representation × family × use-specific bucket; category columns can overlap for different uses of one family',
        'not_generalized':'Counts of judged material, not comparative precision/recall or controlled performance.',
        'overall_new_problem_families':len({(j['problem'],j['family']) for j in judgments if j['bucket']=='new_candidate'}),
        'opened_distinct_candidate_sources':len(sources),'judgments':len(judgments),'rows':count_rows,
        'new_family_groups':[{ 'problem':p,'family':f,'candidate_ids':[j['candidate_id'] for j in judgments if j['problem']==p and j['family']==f and j['bucket']=='new_candidate']} for p,f in sorted({(j['problem'],j['family']) for j in judgments if j['bucket']=='new_candidate'})]}
save(E/'comparison-counts.json',counts)

background=[]
background_excluded=[]
for filename in ['representation-sources.json','empirical-sources.json','transfer-sources.json','observation-sources.json']:
    d=read(filename);background+=d['sources'];background_excluded+=d.get('excluded',[])
for s in background:
    if s['id'].startswith('E'):
        s['methods_results_read'] = s['id'] in {f'E{i:02d}' for i in list(range(1, 14)) + [16]}
        s['methods_results_count_note'] = 'EVIDENCE와 sections_read에 근거한 정규화. E14는 데이터 설명, E15는 검토논문이므로 방법·결과 실증 논문 수에서 제외. E13/E16 표본 중복은 독립 재현 수로 세지 않음.'
selected_sids={s for j in judgments if j['problem'] in problems for s in j['source_ids']}
d0=[]
seen=set()
read_urls={s['url'] for s in sources+background}
for r in selected:
    for hit in r['results']:
        if hit['url'] not in read_urls and hit['url'] not in seen:
            d0.append({'id':'Q5-D0-'+str(len(d0)+1).zfill(3),'url':hit['url'],'title':hit['title'],'level':'D0','reason':'상위 관측 창 제목/snippet만 확인; 본문 근거 수·오탐 수에서 제외','first_query_id':r['id']})
            seen.add(hit['url'])
ledger={'schema':'AF-RES-010 unified sources v1','scope_commit':'ebcca564df68377cc116634dcdab1695be69c0e8',
        'counting_rule':'Background 본문 자료와 Q5 retrial_sources 별도. 동일 저작물 미러/재열람 중복 제외; O01은32개 본문 기준 제외.',
        'sources':background,'retrial_sources':[s for s in sources if s['id'] in selected_sids],
        'excluded':background_excluded+[x for x in excluded if any(q[:2] in problems for q in x.get('query_ids',[]))]+d0,
        'unselected_returned_metadata':'evidence/web-returned-metadata.json: top3 밖의 제목/URL 반환 메타데이터는 별도; 본문 확인 표시가 없는 항목은 모두 D0이며 근거 수 제외'}
save(P/'sources.json',ledger)
print(json.dumps({'phase':args.phase,'web_queries':sum(r['system'].startswith('general_web') for r in selected),'native_attempts':sum(r['system'].startswith('AskNature') for r in selected),'background_including_observation':len(background),'candidate_sources_published':len(ledger['retrial_sources']),'new_families_all':counts['overall_new_problem_families']},ensure_ascii=False))
