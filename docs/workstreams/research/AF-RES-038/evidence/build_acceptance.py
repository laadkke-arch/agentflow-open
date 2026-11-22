"""Record acceptance with explicit research gaps and phase-specific closure receipts."""
from pathlib import Path
import json
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1]
PREFIX='docs/workstreams/research/AF-RES-038/'
def j(p):return json.loads((B/p).read_text())
def evidence(p,needle=None):
    lines=(B/p).read_text().splitlines()
    hits=[n for n,l in enumerate(lines,1) if needle is not None and needle in l]
    return {'file':PREFIX+p,'start_line':hits[0] if hits else 1,'end_line':hits[-1] if hits else len(lines),'locator':needle or 'whole bounded artifact'}
v=j('evidence/verification.json');s=j('evidence/source-summary.json');g=j('evidence/grading-comparison.json')
criteria=j('evidence/criteria-before-grading.json')['criteria']
rows=[]
def add(i,met,n,d,paths,reason='',scope='',phase='research'):
    requirement=next(x['requirement'] for x in criteria if x['id']==i)
    rows.append({'id':i,'requirement':requirement,'met':bool(met),'numerator':n,'denominator':d,'phase':phase,
      'evidence':[evidence(*p) if isinstance(p,tuple) else evidence(p) for p in paths],
      'shortfall_reason':reason if not met else '', 'qualification':scope})
add('A01',True,2,2,['manifest.json',('PROGRESS.md','①')],scope='계획/실제배정 SHA 구분. branch/owned path는 verification에서 확인.')
add('A02',True,1,1,['SCOPE.md',('PROGRESS.md','①')],scope='사전 원격7b977101…; 수정은 REVISIONS 보존.')
add('A03',True,40,40,['frame.csv',('SCOPE.md','2. 후보 원장')],scope='각20번호. metadata만 본/미심사를 완전 적격심사로 세지 않음; 현행 상태노출 기록.')
add('A04',True,4,4,[('RESULT.md','준비도 판정'),('frame.csv','selected_document_task_conditional')],scope='전체2/부분2는 사전 조작적 정의. N08은 작은 흐름이며 장기 설계가 아니다. 무조건 최초성 적격은 A05 별도.')
add('A05',False,3,4,[('sources.jsonl','"source_id": "N-S01"'),('sources.jsonl','"source_id": "N-M01"'),'streams/numpy/selection-freeze.md',('SELF_CHECK.md','## Q1')],
 reason='formal/첫 복구 본문4개는 읽었지만 SCOPE §2.4의 최초공개 완전 확인 조건에서 N08 미확인. 4/10 사전논의와4/27 문서/4/29 git추가판의 관계만 확인.',
 scope='원문 수 역할의 초기문서4와 절대첫공개 확인3을 구별. 첫 재개: 공식2010-04 archive의 formal 구매문서 게시판/원작성 이력.')
add('A06',True,4,4,['rubric.csv',('RESULT.md','3. 네 과제')],scope='당대 기전·설계 수준의 두 방어 가능한 대안. P06 guard는 작성자 구성, P02 POC closure/실제 build는 미확인. 공식 완성 recipe·실행보증을 요구하면 분자 재평가.')
add('A07',True,33,24,['sources.jsonl','evidence/source-summary.json'],scope='107행 중33고유 산입. 실패/미러/부분판독/중복 제외. P-S14는 보수적 제외.')
add('A08',True,24,24,['evidence/source-summary.json',('streams/numpy/source-audit.json','disjoint_24_source_witness')],scope='서로 다른24원문 증인. 실제 역할 초기4/대안9/기준5/후속4/방법6; 첫 공개 완전성은 A05.')
add('A09',True,20,20,['distribution.json','evidence/material-check.json'],scope='4폴더에 t0,A,B,C,t1. 실행 config 숫자는 미합의.')
add('A10',True,4,4,['evidence/material-check.json',('RESULT.md','B 본문 문자')],scope='B/C URL11개·순서·판 동일; 각3/2/3/3개; 설명 문단 외 동일; Unicode 문자수.')
add('A11',True,4,4,['evidence/semantic-review.json','streams/pandas/packet-audit.json','evidence/public-access.json'],scope='작성자 의미 재독·동일 연구문맥 재독. 공개 링크 접근11/11. 새요구/완성답 없음은 사람 합의가 아니며 지속접근 미확인.')
add('A12',True,12,12,['rubric.csv',('SELF_CHECK.md','## Q3')],scope='원요구→t0→t1 연결. 후대/범위밖 입력 제외. P04 inferred 적용·N08 원키별 수치 경계 정정 보존.')
add('A13',True,4,4,['rubric.csv','evidence/source-summary.json',('streams/pandas/read-notes.md','출처와 기준의 독립성')],scope='카드와 기준 파일/기관의 겹침·판/날짜 기록. 독립 기관/사람 재현을 확보했다는 뜻 아님. 댓글 편집가능성,ME03 hash 한계 유지.')
add('A14',True,4,4,['distribution.json','evidence/material-check.json'],scope='whitelist만 전달. t0/t1 답안 URL 없음, B/C 근거 URL 유지. 공개repo 전체 공유는 가림 파괴.')
add('A15',True,12,12,['evidence/grade-seal.json','evidence/blind-observed.json','evidence/transport-normalization.json'],scope='a9589…에서 기대/익명 입력 고정 후 첫 별도 판독. JSON해시일치. 최초CSV 로컬CRLF→원격LF 차이13개와 필드동일성 별도 검증; 접근 지시 격리, OS 격리 아님.')
add('A16',True,12,12,['examples.jsonl','evidence/grading-comparison.json'],scope='허용8의 오탈락0/8, 오류4의 오통과0/4. 첫 요구셀35/36; 다른/비주류 해법을 이름으로 탈락시키지 않음. 유명도/오류빈도의 사람 측정 아님.')
add('A17',True,1,1,['evidence/blind-observed.json','evidence/blind-clarification-observed.json','evidence/post-review-rubric-change.json',('REVISIONS.md','R10')],scope='예상partial/자기fail/첫가림pass 이견1셀 보존. 원문기반 조정+같은AI 재독fail. 외부사람0. 사후정정으로 첫35/36을 덮지 않음.')
add('A18',True,12,12,['evidence/measurement-fixtures.jsonl','evidence/measurement-check.json','evidence/measurement-comparison.json'],scope='포기·결측·오답유지·정답유지·새요구·원요구수리·오류카드·무변화·노동결측·혼합·품질미확인·늦은최초완성. 의미 판독은 이전 설계 기억/품질표식이 있어 완전독립 가림검증 아님.')
add('A19',True,11,11,['measurement.md','forms/run-config.json','evidence/verification.json'],scope='빈 원자료CSV11종. 전원품질/총노동 우선, 채택자/완료자 분모 별도. 시간null, 사람시뮬레이션0.')
add('A20',True,6,4,['streams/methods/methods.md',('RESULT.md','6. 두 분야')],scope='디자인3/교육3의 실제 자극/채점 원문. 초보/숙련/인지자/작성자/유지자/가림채점 관점. 시간효과 전용 없음.')
add('A21',True,7,7,['measurement.md',('SELF_CHECK.md','## Q7')],scope='배정단위·사전인지·공유·가림/불일치·중단/결측·분모/가설. 숫자/추정법 합의는 별도.')
add('A22',True,1,1,['forms/run-config.json',('RESULT.md','사람 시험 개시')],scope='내용검토와 사람시험개시를 구별했음. human_trial_ready=false; budget/gap/margins/sample 등 미합의 자체는 해소하지 않았다.')
add('A23',True,3,3,['RESULT.md',('evidence/verification.json','result_table_locations')],scope='제목 바로 뒤 표12행/12행, 마지막 정확3행. 헤더·구분선 제외.')
add('A24',True,7,7,['SELF_CHECK.md'],scope='Q1~Q7 직접URL/위치·지지·반증 경로·잔여미확인·뒤집힐 조건.')

receipt_path=B/'evidence/finalization-receipt.json'
receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else None
reads=receipt.get('fixed_commit_reread',[]) if receipt else []
read_ok=len(reads)==2 and all(x.get('exact_bytes_match_local') for x in reads)
check=receipt.get('session_check',{}) if receipt else {}
check_ok=check.get('exit_code')==0
add('A25',read_ok,2 if read_ok else 0,2,['evidence/finalization-receipt.json'] if receipt else ['PROGRESS.md'],
 reason='이 수용 파일의 첫 결과 커밋 뒤 고정 SHA에서 RESULT/acceptance를 재독하는 종료 단계가 아직 남음.',
 scope='met 시점은 receipt의 검증 대상commit이다. 최종판의 재독은 마지막 HANDOFF에 추가 기록.',phase='closure')
add('A26',check_ok,1 if check_ok else 0,1,['evidence/finalization-receipt.json'] if receipt else ['manifest.json'],
 reason='결과/수용 커밋 뒤 요청된 session check --fetch를 실행할 종료 단계가 남음.',
 scope='exit0은 세션 계약/경로/의존 검사이며 연구의 미확인 조건을 해소하지 않는다.',phase='closure')
add('A27',False,0,1,['PROGRESS.md'],reason='절차상 이 파일을 고정·재독·점검한 뒤에만 HANDOFF 단독 최종 커밋을 만들 수 있다. 따라서 이 선행 snapshot에서 미래 완료를 true로 쓰지 않는다.',
 scope='최종 HANDOFF와 그 단독 commit diff가 이 종료항목의 후속 증거다. 연구내용 미충족 목록과 별도이며 위 snapshot을 소급 수정하지 않는다.',phase='deferred_final_handoff')
payload={'schema':1,'task_id':'AF-RES-038','recorded_utc':datetime.now(timezone.utc).isoformat(),
 'phase':'result_ready_for_final_reread_and_handoff' if receipt else 'result_checkpoint_before_remote_reread',
 'research_scope':'문서/예시 판별 준비. 사람 모집·실험·시간·제품효과 없음.',
 'counts':{'content_kits':4,'strict_first_public_gate_passed_kits':3,'first_public_gate_unmet_kits':1,'participant_files':20,'source_rows':107,'counted_unique_sources':33,'sealed_examples':12,'first_overall_matches':12,'first_requirement_matches':35,'requirement_cells':36,'state_fixtures':12,'humans':0},
 'research_criteria_met':sum(r['met'] for r in rows if r['phase']=='research'),'research_criteria_denominator':24,
 'substantive_unmet_ids':[r['id'] for r in rows if r['phase']=='research' and not r['met']],
 'closure_pending_at_this_snapshot':[r['id'] for r in rows if r['phase']!='research' and not r['met']],
 'human_trial_ready':False,'historical_runtime_verified':False,'criterion_rows':rows,
 'first_resume_material':'https://mail.python.org/pipermail/numpy-discussion/2010-April/049846.html',
 'closure_note':'A27의 false는 선행 acceptance snapshot의 시점 상태다. 이를 미리 완료로 쓰지 않고 검증 후 HANDOFF만 별도 마지막 커밋한다. 최종 HANDOFF와 remote branch head로 완료 여부를 판독한다.'}
(B/'evidence/acceptance-evidence.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:payload[k] for k in ['research_criteria_met','research_criteria_denominator','substantive_unmet_ids','closure_pending_at_this_snapshot']},ensure_ascii=False))
