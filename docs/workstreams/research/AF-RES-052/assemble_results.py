"""Assemble observed ledgers and required tables, preserving missingness and layers.

No network access. This does not alter the pre-observation inputs.
"""
from pathlib import Path
from collections import Counter
import csv
import json

ROOT = Path(__file__).resolve().parent
def read_csv(name):
    return list(csv.DictReader((ROOT / name).open()))
def read_json(name):
    return json.loads((ROOT / name).read_text())
def dump_csv(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})
def dump_json(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def sequence(s):
    if not s: return []
    if s.startswith('['): return json.loads(s)
    return s.split(';')

slots = read_csv('slots.csv')
groups = read_csv('groups.csv')
slot_by_id = {r['slot_id']: r for r in slots}
py_evidence = read_csv('evidence/python/evidence.csv')
md_evidence = read_csv('evidence/markdown/evidence.csv')
evidence = []
requirements = {
    'P-N1': [('P-N1-R1', 'editable 설치', 'PY-I564', 'body L70-L72'),
             ('P-N1-R2', '텍스트·문서 데이터 포함', 'PY-I564', 'body L61-L67')],
    'P-N2': [('P-N2-R1', 'readme.md 내용에서 long_description', 'PY-I574', 'body L19-L25'),
             ('P-N2-R2', 'Markdown content type 및 PyPI 설명', 'PY-I574', 'body L19,L24-L25,L43')],
    'M-N1': [('M-N1-C1', '언어 없는 code의 backtick fence', 'M-ISS-941', 'body L22,L30-L40,L55-L60'),
             ('M-N1-C2', 'javascript 언어·코드 내용 보존', 'M-ISS-941', 'body L30-L36,L42-L53')],
    'M-N2': [('M-N2-C1', 'inline code의 < 및 > entity 출력', 'M-ISS-955', 'body L22-L35'),
             ('M-N2-C2', 'pre/code entity 및 language-html 유지', 'M-ISS-955', 'body L22-L35,L47')],
}
for case, conditions in requirements.items():
    for cid, text, source, loc in conditions:
        evidence.append(dict(evidence_id='E-' + cid, case_id=case, layer='natural',
            purpose_id=case, pool_ranks=[], condition_id=cid, implementation_id=None,
            evidence_level='requirement D1; candidate none', same_version_status='미확인',
            condition_status='미확인: no matched candidate pool',
            scope='primary empty return; not ecosystem absence', source_ids=[source], arrival_ids=[],
            locator=loc, finding=text + '; 고정 기능명사-목록 제목 무매치',
            limitations='반환 구현 집합은 관측 0. 조건을 충족하는 도구의 존재 여부와 생성 당시 본문은 미확인.',
            executed=False, origin_file='frame.csv; domain requirements', origin_row=case))
for case in ('P-S2', 'M-S1', 'M-S2'):
    s = slot_by_id[case]
    evidence.append(dict(evidence_id='E-' + case + '-UNFILLED', case_id=case, layer='supplemental',
        purpose_id=None, pool_ranks=[], condition_id=None, implementation_id=None,
        evidence_level='catalog screening', same_version_status='미확인',
        condition_status='미확인: unfilled slot', scope='primary unfilled slot',
        source_ids=['PY-LIST' if case.startswith('P') else 'M-LIST-PRIMARY'], arrival_ids=[],
        locator='functional/section scan in domain evidence', finding=s['status'], limitations=s['missing'],
        executed=False, origin_file=s['origin_file'], origin_row=case))
for n, r in enumerate(py_evidence, 2):
    evidence.append(dict(evidence_id=r['evidence_id'], case_id=r['slot_id'],
        layer='supplemental' if r['slot_id']=='P-S1' else 'context', purpose_id=None,
        pool_ranks=[int(r['original_rank'])] if r['original_rank'] else [],
        condition_id=None, implementation_id=r['implementation_id'] or None,
        evidence_level=r['evidence_level'] or 'catalog metadata', same_version_status=r['version'] or '미확인',
        condition_status=r['condition_status'], scope=r['gold_vs_window'],
        source_ids=sequence(r['source_ids']), arrival_ids=sequence(r['arrival_id']),
        locator=r['locator'] or 'see source/arrival IDs', finding=r['reason'],
        limitations='사전 목적 미연결: 완결 구현 ID·증감 미확인. ' + r['user_window_status'],
        executed=False, origin_file='evidence/python/evidence.csv', origin_row=n))
for n, r in enumerate(md_evidence, 2):
    evidence.append(dict(evidence_id=r['evidence_id'], case_id=r['case_id'], layer='diagnostic',
        purpose_id=r['purpose_id'], pool_ranks=[int(r['pool_rank'])], condition_id=r['condition_id'],
        implementation_id=r['implementation_id'] or None, evidence_level=r['evidence_level'],
        same_version_status=r['historical_status'], condition_status=r['condition_status'], scope=r['scope'],
        source_ids=sequence(r['source_ids']), arrival_ids=['MA-R'+r['pool_rank']] if r['scope'].startswith('exact-arrival') else [],
        locator=r['locators'], finding=r['judgment'], limitations=r['limitations'], executed=False,
        origin_file='evidence/markdown/evidence.csv', origin_row=n))
dump_csv('evidence.csv', evidence)

paths = []
for g in groups:
    if g['case_id']=='P-S1': continue
    natural = slot_by_id[g['case_id']]['layer']=='natural'
    paths.append(dict(path_id=g['group_row_id']+'-EMPTY', case_id=g['case_id'],
        layer=slot_by_id[g['case_id']]['layer'], purpose_id=g['case_id'] if natural else None,
        method=g['method'], path_kind='empty_status_record', actions=0, steps=[], arrival_ids=[],
        arrival_statuses=[], path_instantiated=False, current_supported_atoms=[],
        complete_current_ids=[] if natural else None, complete_current_count=0 if natural else None,
        maximum_complete_this_trial=None, historical_status='미확인',
        outside_original_pool_urls=[], outside_original_pool_work_urls=[], outside_pool_complete_ids=None,
        judgment='관측 0: no heading match' if natural else '미확인: unfilled sample slot',
        limitations='시행이 없으므로 한 시행 최대·조건부 성공률은 해당 없음. 전체 생태계 실패로 해석하지 않는다.',
        mode='status record; no traversal', origin_file='groups.csv', origin_row=g['group_row_id']))
for n, r in enumerate(read_csv('evidence/python/paths.csv'), 2):
    paths.append(dict(path_id=r['path_id'], case_id=r['slot_id'],
        layer='supplemental' if r['slot_id']=='P-S1' else 'diagnostic', purpose_id=None,
        method=r['method'], path_kind=r['kind'], actions=int(r['actions']), steps=json.loads(r['steps']),
        arrival_ids=sequence(r['arrival_ids']), arrival_statuses=sequence(r['arrival_statuses']),
        path_instantiated=r['instantiated']=='True', current_supported_atoms=None,
        complete_current_ids=None, complete_current_count=None, maximum_complete_this_trial=None,
        historical_status='미확인: no linked purpose', outside_original_pool_urls=None,
        outside_original_pool_work_urls=None, outside_pool_complete_ids=None, judgment=r['result'],
        limitations=r['limits'], mode=r['mode'], origin_file='evidence/python/paths.csv', origin_row=n))
for n, r in enumerate(read_csv('evidence/markdown/paths.csv'), 2):
    paths.append(dict(path_id=r['path_id'], case_id=r['case_id'], layer='diagnostic',
        purpose_id=r['purpose_id'], method=r['method'], path_kind=r['path_kind'], actions=int(r['actions']),
        steps=json.loads(r['steps_json']), arrival_ids=sequence(r['arrival_ids']),
        arrival_statuses=['opened; fixed source projection'], path_instantiated=True,
        current_supported_atoms=sequence(r['current_supported_atoms']),
        complete_current_ids=sequence(r['complete_current_ids']), complete_current_count=int(r['complete_current_count']),
        maximum_complete_this_trial=int(r['maximum_complete_this_trial']), historical_status=r['historical_status'],
        outside_original_pool_urls=sequence(r['outside_original_pool_urls']),
        outside_original_pool_work_urls=sequence(r['outside_original_pool_work_urls']),
        outside_pool_complete_ids=sequence(r['outside_pool_complete_ids']), judgment=r['judgment'],
        limitations=r['reading_limit'], mode='paired reconstruction from same observed source windows; no human traversal',
        origin_file='evidence/markdown/paths.csv', origin_row=n))
dump_csv('paths.csv', paths)

changes = []
for g in groups:
    case=g['case_id']; s=slot_by_id[case]; natural=s['layer']=='natural'
    changes.append(dict(change_id=g['group_row_id'], case_id=case, layer=s['layer'], method=g['method'],
        representative_ranks=json.loads(g['representatives']), hidden_siblings=json.loads(g['hidden_siblings']),
        current_direct_complete_ids=[] if natural else None,
        current_two_action_union_ids=[] if natural else None, single_trial_max=None,
        gained_complete_ids=[] if natural else None, lost_complete_ids=[] if natural else None,
        gained_url_ranks=[5] if case=='P-S1' and g['method']=='B' else [],
        lost_direct_url_ranks=[2,3] if case=='P-S1' and g['method']=='B' else [],
        delta_status='관측 0 in empty return; conditional rate 해당 없음' if natural else '미확인: purpose missing or slot unfilled',
        supported_atom_gain=[], reason=g['status']))
for method, ranks in [('A',[1,2,3]),('B',[1,6]),('C',[1,2,3])]:
    changes.append(dict(change_id='D-M1-'+method, case_id='D-M1', layer='diagnostic', method=method,
        representative_ranks=ranks, hidden_siblings=[2,3,4,5] if method=='B' else [],
        current_direct_complete_ids=[], current_two_action_union_ids=[], single_trial_max=0,
        gained_complete_ids=[], lost_complete_ids=[], gained_url_ranks=[6] if method=='B' else [],
        lost_direct_url_ranks=[2,3] if method=='B' else [], delta_status='관측 0 current full completion; historical 미확인',
        supported_atom_gain=['M-N1-C1'] if method=='B' else [],
        reason='rank6 specification is not runtime; B-P08 exposes C1 only' if method=='B' else 'fixed first800 and first2hrefs do not expose both conditions'))
dump_csv('changes.csv', changes)

sensitivity=[]
for case in slot_by_id:
    if case=='P-S1':continue
    natural=slot_by_id[case]['layer']=='natural'
    for method in ('A','B','C'):
        sensitivity.append(dict(sensitivity_id=case+'-'+method+'-SLOTS', case_id=case,
            layer=slot_by_id[case]['layer'], method=method, change='slots3_to4', baseline_ranks=[], changed_ranks=[],
            new_visible_ranks=[], complete_delta=0 if natural else None, atom_delta=[],
            reason='빈 매치는 슬롯을 늘려도 빈 배열' if natural else '미충원 자리를 슬롯 수로 채우지 않음',
            exact_flip_condition='정확 기능명사/공식 별칭으로 매치되는 발행 절과 적격 풀 필요' if natural else '같은 사전 규칙에 적격인 기능 절·목적 필요'))
    sensitivity.append(dict(sensitivity_id=case+'-C-VERSION', case_id=case,
        layer=slot_by_id[case]['layer'], method='C', change='unknown_product_version_as_same_sentinel_only',
        baseline_ranks=[], changed_ranks=[], new_visible_ranks=[], complete_delta=0 if natural else None,
        atom_delta=[], reason='실제 후보 배열 없음', exact_flip_condition='후보가 생기고 나머지 네 필드가 모두 알려져 같아야 함'))
for r in read_csv('evidence/python/sensitivity.csv'):
    sensitivity.append(dict(sensitivity_id=r['sensitivity_id'],case_id=r['slot_id'],
        layer='supplemental' if r['slot_id']=='P-S1' else 'diagnostic' if r['slot_id']=='D-P1' else 'context',
        method=r['method'], change=r['changed_rule'] or 'slots3_to4',
        baseline_ranks=sequence(r['default_ranks']), changed_ranks=sequence(r['changed_ranks']),
        new_visible_ranks=sequence(r['visible_url_delta']), complete_delta=None, atom_delta=None,
        reason=r['reason'],exact_flip_condition=r['exact_flip_condition']))
for r in read_csv('evidence/markdown/sensitivity-observations.csv'):
    sensitivity.append(dict(sensitivity_id=r['sensitivity_id'],case_id='D-M1',layer='diagnostic',method=r['method'],
        change=r['change'],baseline_ranks=[int(x) for x in sequence(r['baseline_representatives'])],
        changed_ranks=[int(x) for x in sequence(r['sensitivity_representatives'])],
        new_visible_ranks=[int(r['first_changed_original_rank'])] if r['first_changed_original_rank'] else [],
        complete_delta=int(r['two_action_complete_delta']), atom_delta=sequence(r['direct_supported_atom_delta']),
        reason=r['interpretation'], exact_flip_condition='rank4 direct C1 at slot4; C2 remains absent; version-only relaxation leaves other unknown fields'))
dump_csv('sensitivity.csv', sensitivity)

counterexamples = [
 ('CE01','P-S1','4–6위 공급자 URL이 독립 완결 구현인가','PY-E05;PY-E06','rank5 AWS 승격 확인; 보완 저장 서비스·사전 목적 없음','미확인','일치하는 사전 목적과 대체 가능한 별도 실행 구현 및 동일판 조건 증거'),
 ('CE02','D-M1','4–6위 별도 상류가 독립 runtime인가','ME-R6-C1;ME-R6-C2','rank6 mdast는 명세; runtime 승격 관측 0','counterexample','첫6 안의 별개 실행 공급자와 두 조건의 창 근거'),
 ('CE03','D-M1','완결 차이0이면 모든 증거 차이도0인가','D-M1-B-P08;ME-R4-C1','B만 C1 원자 노출; 완결은 모든 방식0','counterexample','C2가 같은 시행·판 창에 추가되면 완결 양성 가능'),
 ('CE04','P-S1','상류 묶음이 보완 절의 접근을 늦추는가','PY-E08;PY-E10','Issues→#2059는 A/C2동작, B3동작; Compose 원도착은 실패','qualified','해당 보고/예제가 사전 목적의 필수조건임을 입증하고 정확 도착 복구'),
 ('CE05','P-S1;D-M1','C=A이면 표시키가 검증됐는가','groups.csv;diagnostic-groups.csv','제품판·역할 결측, 혹은 부품 차이로 충돌 없음','counterexample','목록에서 다섯 필드가 알려진 실제 충돌과 후순위 대안 필요'),
 ('CE06','context-first20','병합이 있으면 앞3 대표는 늘 달라지는가','PY-E11;PY-LIST L284-L294','trove의 원4·6 exact URL 병합은 앞3을 바꾸지 않음','counterexample','첫3 안에서 슬롯을 차지하는 중복과 그 뒤의 새 그룹 필요'),
 ('CE07','D-M1;context','원문 하나는 한 구현만 설명하는가','M-VENDOR-ROOT;PY-O14','root 네 패키지·build 비교 절은 여러 역할을 소개','counterexample','같은 도착 창이 별개 구현 각각의 모든 조건·판을 설명해야 둘로 셈'),
 ('CE08','D-M1','유효 Markdown이면 backtick 요구의 정답인가','M-HOP-COMMONMARK;M-CODE-INDENT;M-CODE-FENCE;M-TEST-UTILITY','indent/tilde는 유효해도 사용자 backtick 조건을 깨뜨림','counterexample','요구자가 fence marker 제약을 명시적으로 완화한 별도 요구'),
 ('CE09','D-M1','현재판·릴리스 설명은 역사판 동작을 보장하는가','M-RELEASE-15;ME-HISTORY','2023 기본값 변경; false 설명은 코드/시험과 충돌','counterexample','원2022 package identity/lockfile와 해당판 실행·시험'),
 ('CE10','P-S1','같은 URL을 연속 조회하면 같은 창인가','PY-E09;PY-A04;PY-A17','7.0.0 일부 뒤8.2.0 레이아웃으로 바뀜; 합성하지 않음','counterexample','동일 snapshot 원800단어를 보존하거나 새 통제 시행'),
 ('CE11','crossfield','같은 곡명은 같은 특정 연주인가','X01;X02','ARK·연주자·날짜가 다른 두 Beautiful Dreamer 레코드','counterexample','특정 연주가 아닌 작품 수준 탐색만 요구할 때 묶음 허용'),
 ('CE12','crossfield','같은 family/다른 이름은 같은/다른 축 계약인가','X03;X04','Inter 판·flavor에 따라 축 지원 다름; Inter/Inter V는 이름만 다른 반례','counterexample','판·flavor·축 계약을 문서/실파일에서 고정해야 기능 대표 선택 가능'),
]
dump_csv('counterexamples.csv',[dict(zip(['counterexample_id','case_id','challenge','ledger_refs','observation','status','minimum_flip_condition'],r)) for r in counterexamples])

P_URL='https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst'
M_URL='https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md'
t1_headers=['층·요구·최초판','목적·필수조건','목록 고정 URL·절·원순번','관측 후보/소진/결측','네 번째 후보·묶일 기회','원풀의 완결 구현 ID·근거','미확인']
t1_rows=[
 ['자연 P-N1 · #564 · 2022-01-03 · 최초 가용 현재본문','editable 설치 + 텍스트·문서 데이터 포함 (R1/R2)',f'[PY-LIST]({P_URL}) · 제목/별칭 무매치 · 원순번 없음','반환 후보 관측 0 · 목록 본문 확보','네 번째 없음 · 기회 관측 0','반환 ID 관측 0 · E-P-N1-R1/R2','생성판·역사 환경·생태계의 해결책 존재'],
 ['자연 P-N2 · #574 · 2022-02-17 · 최초 가용 현재본문','README 내용→long_description + Markdown content type (R1/R2)',f'[PY-LIST]({P_URL}) · 무매치 · 원순번 없음','반환 후보 관측 0 · 목록 본문 확보','네 번째 없음 · 기회 관측 0','반환 ID 관측 0 · E-P-N2-R1/R2','생성판; setup.py 부재는 금지 조건 아님'],
 ['자연 M-N1 · #941 · 2022-01-21 · 최초 가용 현재본문','AST→Markdown: 언어 없는 backtick + javascript 언어·내용 유지 (C1/C2)',f'[M-LIST]({M_URL}) · 무매치 · 원순번 없음','반환 후보 관측 0 · 목록 본문 확보','네 번째 없음 · 기회 관측 0','반환 ID 관측 0 · E-M-N1-C1/C2','생성판·첨부·literal react-stringify10.0.2 식별'],
 ['자연 M-N2 · #955 · 2022-02-18 · 최초 가용 현재본문','Markdown→HTML: inline와 pre/code의 <·> entity; language-html (C1/C2)',f'[M-LIST]({M_URL}) · 무매치 · 원순번 없음','반환 후보 관측 0 · 목록 본문 확보','네 번째 없음 · 기회 관측 0','반환 ID 관측 0 · E-M-N2-C1/C2','생성판·첨부·보고된 4패키지 역사판'],
 ['보강 P-S1 · 사전 목적 미연결','절의 미러링/클라우드 저장 목적과 맞는 사전 요구 없음',f'[PY-LIST]({P_URL}#L18-L35) · bandersnatch · 원1–5','정확 URL5 · 5에서 소진 · 도착5 중 온전한 창4/부분1','원4 PyPI 존재; B가1–4 묶어 원5 S3 승격','미확인 · PY-E01–10; URL 공급자2를 완결 구현2로 세지 않음','목적·완결 ID·증감; 원4 snapshot·-h·Compose 도착'],
 ['보강 P-S2 · 미충원','엄격 C 충돌 절을 사전 목적에 연결할 자리',f'[PY-LIST]({P_URL}) · 첫20 기능 절 · 적격 절 없음','선정 풀 없음 · 미충원','엄격 C 기회 관측 0 / 조사20절','미확인 · E-P-S2-UNFILLED','실제 C 충돌·목적·후순위 독립 구현'],
 ['보강 M-S1 · 미충원','같은 상류 반복이 있는 기능 절 자리',f'[M-LIST]({M_URL}#L34-L98) · 범주5개, 기능 절0','선정 풀 없음 · 기능 절 소진','적격 기능 절 없음; 기회 비율 해당 없음','미확인 · E-M-S1-UNFILLED','Official6은 D-M1 진단으로만 보존'],
 ['보강 M-S2 · 미충원','엄격 C 충돌이 있는 별도 기능 절 자리',f'[M-LIST]({M_URL}#L34-L98) · 기능 절0','선정 풀 없음 · 기능 절 소진','적격 기능 절 없음; 기회 비율 해당 없음','미확인 · E-M-S2-UNFILLED','기능 절·C 제품판/역할·목적'],
]
t2_headers=['요구·방식 A/B/C','세 대표·숨은 원순번','직접 완결 ID','두 번 안에 확인 가능한 ID','한 시행 최대·경로','A 대비 올라온/잃은 ID·이유','도착 원문·절','결측']
t2_rows=[]
for g in groups:
    case=g['case_id'];method=g['method'];natural=slot_by_id[case]['layer']=='natural'
    if natural:
        t2_rows.append([g['group_row_id'],'없음 · 형제 없음','관측 0','관측 0','해당 없음 · 시행 없음','관측 0 / 관측 0 · 빈 반환','도착 없음; '+g['group_row_id']+'-EMPTY','생성판·목록 매치; 생태계 존재 미판정'])
    elif case=='P-S1':
        b=method=='B'
        t2_rows.append([g['group_row_id'],'1,5 · 형제2,3,4' if b else '1,2,3 · 형제없음; 4,5 잘림',
            '미확인','미확인','미확인 · '+('13' if b else '18')+' 경로',
            '미확인 / 미확인; URL5 승격, URL2·3 형제화' if b else '미확인 / 미확인; 목적 미연결',
            'PY-A01 매뉴얼; PY-A05 S3' if b else 'PY-A01 매뉴얼; A02 Issues; A03 README',
            '목적; 원4 부분창·-h 정확fragment·Compose실패'])
    else:
        t2_rows.append([g['group_row_id'],'없음 · 미충원','미확인','미확인','해당 없음 · 시행 없음','미확인 / 미확인 · 적격 풀 없음',
            '도착 없음; '+g['group_row_id']+'-EMPTY',slot_by_id[case]['missing']])
dump_json('evidence/required-table-data.json',{'table1':{'headers':t1_headers,'rows':t1_rows},'table2':{'headers':t2_headers,'rows':t2_rows}})
def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(x).replace('|',' / ').replace('\n',' ') for x in r)+' |' for r in rows)+'\n'
(ROOT/'evidence/required-tables.md').write_text(table(t1_headers,t1_rows)+'\n'+table(t2_headers,t2_rows))

metrics={
 'primary_slots':8,'primary_groups':24,'natural_requested':4,'natural_selected':4,
 'natural_nonempty_pools':0,'natural_metadata_opportunities':0,
 'supplemental_requested':4,'supplemental_metadata_pools':1,'supplemental_unfilled':3,
 'supplemental_purpose_linked':0,'supplemental_complete_positive':None,
 'supplemental_complete_positive_rate':'해당 없음: linked-purpose denominator 0',
 'primary_pool_url_rows':5,'primary_pool_exact_urls':5,'primary_publisher_groups':2,
 'primary_complete_implementation_ids':None,'human_adoption':'미측정',
 'natural_return_complete_ids_observed':0,'natural_ecosystem_complete_ids':'미확인',
 'path_rows':len(paths),'empty_status_rows':sum(r['actions']==0 for r in paths),
 'observed_or_planned_path_rows':sum(r['actions']>0 for r in paths),
 'path_rows_by_case':dict(Counter(r['case_id'] for r in paths if r['actions']>0)),
 'diagnostic_markdown':read_json('evidence/markdown/diagnostic-metrics.json'),
 'source_counts':read_json('evidence/source-counts.json'),
 'physical_arrival_or_human_trial_claim':False,
 'evidence_rows':len(evidence),'sensitivity_rows':len(sensitivity),'counterexample_rows':len(counterexamples)
}
dump_json('evidence/result-metrics.json',metrics)

index={}
for name,id_field in [('slots.csv','slot_id'),('groups.csv','group_row_id'),('pools.csv','pool_row_id'),
    ('evidence.csv','evidence_id'),('paths.csv','path_id'),('changes.csv','change_id'),
    ('sensitivity.csv','sensitivity_id'),('counterexamples.csv','counterexample_id')]:
    entries=read_csv(name)
    if entries and id_field not in entries[0]:
        id_field='row_id' if 'row_id' in entries[0] else list(entries[0])[0]
    index[name]={r[id_field]:i for i,r in enumerate(entries,2)}
index['sources.jsonl']={json.loads(s)['source_id']:i for i,s in enumerate((ROOT/'sources.jsonl').read_text().splitlines(),1)}
dump_json('evidence/ledger-index.json',index)
print(json.dumps({k:metrics[k] for k in ['primary_slots','primary_groups','path_rows','empty_status_rows','evidence_rows','sensitivity_rows','counterexample_rows']},ensure_ascii=False))
