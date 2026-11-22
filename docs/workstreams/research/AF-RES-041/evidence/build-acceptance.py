"""Freeze observed acceptance evidence; post-commit actions close in HANDOFF."""
from datetime import datetime, timezone
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
validation=json.loads((ROOT/'evidence/validation.json').read_text())
assert validation['passed'], 'required validation has not passed'
sources=[json.loads(line) for line in (ROOT/'sources.jsonl').read_text().splitlines()]
by_id={row['source_id']:(line,row) for line,row in enumerate(sources,1)}
judgments=list(csv.DictReader((ROOT/'judgments.csv').open()))
conditions=[]

def location(path,needle=None):
    if needle is None:return {'file':path,'line':1}
    for n,line in enumerate((ROOT/path).read_text().splitlines(),1):
        if needle in line:return {'file':path,'line':n}
    raise ValueError((path,needle))

def evidence(ids):
    return [dict(source_id=sid,file='sources.jsonl',line=by_id[sid][0],url=by_id[sid][1]['original_url'],locator=by_id[sid][1]['locator']) for sid in ids]

def condition(cid,met,unit,numerator,denominator,files,ids=(),reason='해당 없음',resume='해당 없음',status=None):
    conditions.append(dict(condition_id=cid,met=bool(met),unit=unit,numerator=numerator,denominator=denominator,
        comparison='observed/required or explicit eligible denominator; not an adoption rate',files=files,evidence=evidence(ids),
        status=status or ('observed' if met else '미확인'),unmet_reason=reason,minimum_resume_source=resume))

condition('contract_scope_inputs',True,'범위·입력·환경 기록',1,1,[location('manifest.json'),location('SCOPE.md','실제 시작 통합 SHA')])
condition('pre_registration_before_new_reading',True,'사전 규칙 고정',1,1,[location('SCOPE.md','고정 시각'),location('evidence/validation.json','registration_before_counted_readings')])
condition('unique_primary_works',True,'서로 다른 고유 외부 1차 저작/최소 필요수',29,22,[location('sources.jsonl'),location('evidence/source-audit.json')])
for cat,required in [('printing_background',4),('music_background',4),('recipient',8),('bibliography',3),('counter',3)]:
    selected=[s['source_id'] for s in sources if s['counted'] and s['quota_category']==cat]
    condition('quota_'+cat,len(selected)>=required,'단일 배당 고유 저작/필수 하한',len(selected),required,[location('evidence/source-audit.json',cat)],selected)
for case in ['B01','B03']:
    selected=[s['source_id'] for s in sources if s['counted'] and s['quota_category']=='recipient' and case in s['case_ids']]
    condition('recipient_'+case,len(selected)>=3,'프로젝트 수신 원저작/필수 하한',len(selected),3,[location('sources.jsonl')],selected)
condition('ledger_fields_and_duplicates',True,'열람 범위의 필수14키·고유ID·중복검산',validation['reading_ranges'],validation['reading_ranges'],[location('evidence/validation.json','required_source_fields')])
condition('fixed_two_cases_four_judgments',True,'사전 판독 행',4,4,[location('judgments.csv')])
condition('five_contacts_recorded',True,'참/거짓/미확인을 명시한 접점',20,20,[location('judgments.csv')])
condition('paired_denominators_preserved',True,'최초안/코드 분모를 분리한 기준',2,2,[location('RESULT.md','기준·민감도'),location('evidence/validation.json','paired_denominators')])
condition('decisive_original_access_attempts',True,'결정적 원전 경로를 직접 시도한 사건',2,2,[location('frame.csv'),location('sources.jsonl')],['B01-P090','B01-P091','ED013','ED014','B01-P006','ED007'])
condition('B01_inspiration_and_independent_implementation_counter',True,'한 사건의 지지·반증 원문 대조',1,1,[location('RESULT.md','독자 구현')],['B01-P001','B01-P004','B01-P006'])
condition('B03_general_feature_nonadoption_counter',True,'당대 소스의 의도적 미채택 진술',1,1,[location('RESULT.md','sharp 가로 획 끝')],['B03-L001'])
condition('B03_exact_exemplar_nonadoption_pair',False,'정확 저자 사용판의 특정 glyph와 미채택 특징의 쌍',0,1,[location('SELF_CHECK.md','정확한 특정 본보기')],['B03-L001','ED001','ED007','ED020'],
 '미채택 특징 자체는 sharp 획 끝의 수평성이지만, 그것을 관찰한 정확 악보판·쪽과 Wanske 원책의 언급부재는 확인하지 못함.',
 '1997 이전 저자 사용 Schubert/Müller 판면과 Wanske ISBN3-7957-2886-X accidentals 장; 해당 코드 주석의 작성자 설명')
condition('same_function_reflection',True,'같은 목적·대상의 기능 변경과 반영을 확인한 사건',2,2,[location('mechanisms.csv'),location('RESULT.md','확인한 수는 별도로')],['B01-P013','B01-P001','B01-P003','B03-L011','B03-L012','B03-L031','B03-L032'])
condition('two_required_result_tables',True,'지정 열·지정 행수의 앞부분 표',2,2,[{'file':'RESULT.md','line':3,'end_line':8},{'file':'RESULT.md','line':10,'end_line':13}])
condition('two_cards_two_links',True,'실패조건·누락 접점과 두 링크를 가진 카드',2,2,[location('cards.md','## B01'),location('cards.md','## B03')])
condition('Q1_Q7_self_review',True,'정확 위치·반증·미확인·뒤집을 조건을 대조한 질문',7,7,[location('SELF_CHECK.md','Q1–Q7'),location('evidence/root-recheck.md')])
condition('core_URL_reopen',True,'RESULT 초안 후 본문 재개봉',9,9,[location('evidence/final-recheck-downloads.json')])
condition('csv_and_reference_integrity',True,'원문 문자열 보존·참조 검산 CSV',4,4,[location('evidence/artifact-table-check.json'),location('evidence/validation.json')])
condition('final_three_weaknesses',True,'마지막 약점·다음 조사 행',3,3,[{'file':'RESULT.md','line':validation['result_tables']['weaknesses'][0],'end_line':validation['result_tables']['weaknesses'][1]}])
condition('three_prior_remote_bundles',True,'결과 묶음 앞의 원격 중간 커밋',3,3,[location('evidence/commit-log.jsonl')])
condition('only_owned_path_modified',True,'수정 범위 준수',1,1,[location('evidence/validation.json','only_owned_paths')])

for index,row in enumerate(judgments,2):
    for contact in ['exact_donor','available_then','author_link','change_same_baseline','same_purpose_reflection']:
        state=row[contact]
        suffix={'exact_donor':'exact_donor_missing','author_link':'author_link_missing'}.get(contact)
        reason='해당 없음' if state=='참' else (row[suffix] if suffix else row.get(contact+'_evidence','정확한 관측 미확인'))
        condition(row['judgment_id']+'_'+contact,state=='참','동일 기준선의 개별 접점',int(state=='참'),1,
            [{'file':'judgments.csv','line':index}],row['source_ids'].split(';'),reason,row['next_minimum_source'] if state!='참' else '해당 없음',status=state)

for baseline in ['I','C']:
    condition('strict_complete_chain_'+baseline,False,'다섯 접점 모두 참인 사례/고정 대상 사례',0,2,
        [location('RESULT.md','엄격 최초안 기준의 완결'),location('judgments.csv')],
        reason='관측된 완결 양성이0건. 인과가 거짓임을 증명한 것이 아니라 정확 원판·독서 연결 등에 미확인이 남음.',
        resume='RESULT 마지막 W1/W2의 정확 원판·간기·해당 쪽 및 날짜 있는 독서→같은 선택 변경 기록',status='미확인')

post=[]
for cid,action in [
 ('result_bundle4_remote_commit','결과와 이 수용 원장을 함께 원격 커밋하고 SHA를 기록'),
 ('fixed_SHA_readback','그 SHA에서 RESULT.md와 evidence/acceptance-evidence.json을 GitHub로 다시 열고 내용 해시 대조'),
 ('session_check_after_freeze','python -B -m workbench.session check docs/workstreams/research/AF-RES-041/manifest.json --fetch'),
 ('last_HANDOFF_only_commit','위 실제 결과를 확인한 뒤 HANDOFF.md만 마지막 별도 원격 커밋'),
]:
    post.append(dict(condition_id=cid,met=False,status='not_yet_run_at_result_freeze',unit='결과고정 뒤 절차',numerator=0,denominator=1,
        files=[{'file':'HANDOFF.md','line':'최종 커밋 뒤 확인'}],unmet_reason='요구된 순서상 이 수용 스냅샷의 커밋 이후에만 수행 가능. 완료 여부는 마지막 HANDOFF의 실제 SHA·명령 결과를 따른다.',minimum_resume_source=action))
output=dict(task_id='AF-RES-041',attempt=1,checked_utc=datetime.now(timezone.utc).isoformat(),
 phase='research evidence immediately before result freeze; post-commit closure is recorded only in final HANDOFF',
 outcome='완결 인과 양성: 최초안0/2·코드0/2. 같은 기능 반영2/2. 조사기록과 반증 완료; 결정적 원판·독서 연결 관측은 미충족.',
 format_validation_passed=True,unknown_is_not_false=True,strict_contact_states=validation['contact_state_counts'],
 corpus=dict(unique_works=29,reading_ranges=validation['reading_ranges'],categories=validation['categories'],recipient_by_case=validation['recipient_by_case'],
             conservative_release_family_merge=dict(unique_works=28,recipient_works=9,B01=6,B03=3)),
 conditions=conditions,post_commit_conditions=post,
 interpretation='met=false의 역사 접점은 자료 미확인이다. post_commit_conditions의false는 결과고정 시점의 미실시 상태이며 최종HANDOFF가 후속 완료 증거다. 0건 결과를 일반 채택률이나 인과 부재 증명으로 해석하지 않는다.')
(ROOT/'evidence/acceptance-evidence.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'conditions':len(conditions),'observed_met':sum(c['met'] for c in conditions),'historical_unmet':sum(not c['met'] for c in conditions),'post_commit_conditions':len(post),'reading_ranges':validation['reading_ranges']},ensure_ascii=False))
