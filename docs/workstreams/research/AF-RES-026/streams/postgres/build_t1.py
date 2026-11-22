"""Rebuild post-seal research tables from read receipts and explicit human/model coding.

Does not fetch sources, modify T0 files, or run PostgreSQL. All textual notes are
short paraphrases; source bodies remain at their public original URLs.
"""
import csv, hashlib, json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

P = Path(__file__).resolve().parent
SEAL = '68fc97fadceb46f9945a71fcc53730e29f6c62bf'
NOW = datetime.now(timezone.utc).isoformat()
initial = [json.loads(s) for s in (P/'initial.jsonl').read_text().splitlines()]
bycase = {x['case_id']: x for x in initial}
frozen = {x['case_id']: x for x in map(json.loads, (P/'frozen-responses.jsonl').read_text().splitlines())}
sources0 = json.loads((P/'sources.json').read_text())
src = {x['id']: x for x in sources0}

def dump(name, value):
    (P/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def csvout(name, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with (P/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

def dt(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def iso(s):
    return s.replace(' ', 'T')+'Z'

def hours(a, b):
    return round((dt(b)-dt(a)).total_seconds()/3600, 6)

captures=[]
for name in ['t1-captures-P01-P02-P04-P05-P06.json', 't1-captures-P07-P08.json',
             't1-captures-P03-crosspost-a.json', 't1-captures-P03-crosspost-b.json']:
    captures += json.loads((P/name).read_text())

# Match within already-read messages, never an inference from the author's name alone.
codes = {
 'CAKFQuwa': ('third_party','p2','상속 가시성은 반대 방향이며 문서를 읽으라고 답함','explanation'),
 'CA%2BbJJbws': ('third_party','p2–5','자식 조회는 부모 행을 포함하지 않음; 구조 상속과 행 복사를 구별','explanation'),
 'TYXOG': ('new_requirement','p2–4','문서는 이미 읽었으며 data entry 목적도 있다고 새로 명시; 목적이 실제로 지금 생겼는지는 미확인','newly_stated_scope'),
 '830db': ('third_party','p2–6','일부 view는 data entry 가능하다고 답하고 Updatable Views 절 연결','conditional_technical_answer'),
 'CA%2BbJJby': ('third_party','p2–5','목적을 묻고 행 복사/양쪽 행 조회에 따라 대안을 나눔; 작성자 후속 없음','conditional_technical_answer'),
 '6962fa': ('third_party','p1–2','객체 상속 비유로 부모/자식 조회 방향 설명','explanation'),
 '3561426': ('third_party','p2–3','실제 SELECT가 오류 없는지 묻고 dead row/old transaction 가설을 조건부로 제시; 작성자 답 없음','question_unanswered'),
 '4024278': ('third_party','p3–5','flat SQL이라 직접 선택 복원은 없다고 답함; 다음 덤프 구성과 기존 파일 편집 경로를 구별','conditional_technical_answer'),
 '0b7219fe': ('third_party','p3–6','PG 버전을 확인하고 해당 매뉴얼을 읽으라고 한 뒤 개별 publication refresh 불가라고 답함','negative_answer'),
 '6515271a': ('third_party','p2–5','SQL·기대값·실제값·PG 판이 필요하며 PostGIS 목록에 문의하도록 안내','additional_inputs_requested'),
 '3716cb3b': ('third_party','p2–4','LANGUAGE SQL 예와 의도 확인 질문; 봉인 변수인 원본 루프 여부는 묻지 않음','existence_answer'),
 'ef205ba5': ('third_party','p2–3','server programming 문서 링크 보충','documentation_link'),
 '20220105111258': ('third_party','p2–3','상수 반환 LANGUAGE SQL 함수 예','existence_answer'),
 'CA%2Bi5JwY_': ('new_requirement','p1–2','Oracle 스크립트를 DO block에서 실행하고 모든 Oracle SQL이 호환되는지 추가 질문; 기존 포팅 목적의 명료화 가능','newly_stated_scope'),
 'CA%2Bi5JwbQ': ('new_requirement','p1','Oracle SQL 사용 문서/예 요청; 구체 원본이나 루프 여부는 공개하지 않음','newly_stated_scope'),
 '20220105113426': ('third_party','p2','구체 SQL 없이는 호환 여부를 판단할 수 없으므로 실행해 보고 오류를 제시하라고 답함','additional_inputs_requested'),
 'CAHyXU0w': ('third_party','p2','호환 제품 및 구체 포팅 도움 언급; 작성자의 사용 결과가 아님','third_party_suggestion'),
 '41274': ('third_party','p2–3','jsonb/hstore를 키-값 구조 후보로 제시; Oracle 문법 동등성을 보증하지 않음','candidate_suggestion'),
 'CA%2Bi5JwZRM': ('author_existing_fact','p1–2','2010년 key/value 타입/함수 글을 찾아 의견 요청; 사용 보고 없음','candidate_exploration'),
 '299857': ('third_party','p2','옛 블로그보다 새 방식이 있다고 지적','candidate_age_correction'),
 'CA%2Bi5JwZEV': ('author_existing_fact','p1–3','kv-pair 저장소를 제시하고 문서 사용법이 부족하다고 말함; 설치/채택 보고 아님','candidate_exploration'),
 'eca47936': ('third_party','p2–5','그 저장소를 쓸 이유를 묻고 jsonb/hstore 문서 제시','candidate_suggestion'),
 'DB9PR07MB7180C5E': ('author_existing_fact','p2–8','동일 SQL·테이블 크기·실행 수치로 pgsql-performance에 재게시; 원 글 명시 링크 없음','crosspost'),
 'CAM%2B6J96xK': ('third_party','p3–6','use_remote_estimate/fetch_size 질문 및 EXPLAIN VERBOSE 제안; ID 원천 위치를 직접 묻지 않음','different_variable_question'),
 '20220106.183908': ('third_party','p2–4','예시 inner subquery가 foreign scan이 아니어서 remote join 대상이 아니라고 해석','technical_explanation'),
 'DB9PR07MB718015C': ('author_existing_fact','p3–5','local 쪽 table/result가 원격보다 백만 배 작다고 명시. 같은 UNION 예시가 반복돼 실제 ID SELECT의 물리적 원천 위치를 확정하지 못함','related_local_execution_fact'),
 'CAM%2B6J975q': ('third_party','p3–5','통계/비용 가설과 소스 읽기를 제안하며 전문적 확신의 한계를 명시','third_party_hypothesis'),
 'DB9PR07MB7180C723': ('new_requirement','p2–4','새 DELETE anti-join SQL과 약62초 실행계획을 제시; 최초 SELECT INTO 해법 채택/실패 보고는 아님','new_query_execution_report'),
 'CAM%2B6J96i4': ('third_party','p3–18','응답자가 별도14beta1 테스트를 수행; parameterized scan도 자기 예에서 더 느렸음. 원 작성자 사용 결과가 아님','third_party_reproduction'),
}

followups=[]
for c in captures:
    tail=c['url'].rsplit('/',1)[-1]
    key=next(k for k in codes if tail.startswith(k))
    classification, locator, value, action = codes[key]
    case=c['case_id']; occurred=iso(c['headers']['Date'])
    author=classification in ['author_existing_fact','new_requirement']
    cross=case=='P03'
    followups.append({
      'case_id':case,'message_id':c['headers']['Message-ID'],'url':c['url'],
      'occurred_utc':occurred,'actor':c['headers']['From'],'role':'original_author' if author else 'respondent',
      'reply_to':c['reply_to_url'] or '', 'classification':classification,
      'variable':bycase[case]['missing_variable'], 'value':value,
      'within_30_days':0 <= hours(bycase[case]['submitted_utc'],occurred) <= 720,
      'action':action,'locator':locator,'censoring':'',
      'record_type':'public_message','lineage_id':'P-S'+case[1:],
      'locked_variable_value_used':False,
      'locked_variable_value_used_under_broad_interpretation':key=='DB9PR07MB718015C',
      'thread':'pgsql-performance crosspost' if cross else 'original pgsql-general thread',
      'temporal_origin':'newly stated; actual time requirement arose unknown' if classification=='new_requirement' else 'existing fact' if author else 'not author fact',
      'relation_evidence':'same public sender, identical SQL and performance numbers; no explicit original-thread link' if cross else 'official archive reply navigation',
      'read_utc':c['checked_utc'],'body_sha256':c['body_sha256'],
    })

pipe_meta=[]
for n in ['t1-captures-P08-postgis-a.json','t1-captures-P08-postgis-b.json']:
    pipe_meta+=json.loads((P/n).read_text())
pipe_ids={x['url']:x for x in json.loads((P/'p08-postgis-identifiers.json').read_text())}
pipe_codes={
 '045146':('2022-01-05T18:30:07Z','Shaozhong SHI','author_existing_fact','p1–3','동일 Oracle 선언과 동일 목표를 PostGIS 목록에 재게시','crosspost',''),
 '045168':('2022-01-07T21:19:10Z','Regina Obe','third_party','p1–17','jsonb 저장·수정·조회 예; PG14 subscripting과 구판용 함수 경로를 조건부로 나눔','conditional_technical_answer','045146'),
 '045171':('2022-01-08T02:24:41Z','Shaozhong SHI','new_requirement','p3–7','새 항목 추가·쌍의 순차 처리·pop·위치 접근을 추가 질문; 숫자 text 변환 허용은 답하지 않음','newly_stated_scope','045168'),
 '045172':('2022-01-08T04:17:37Z','Regina Obe','third_party','p2–30','object key 순서는 보존되지 않으며 each/concat로 수정·순회하는 예를 제시','conditional_technical_answer','045171'),
 '045173':('2022-01-08T04:20:23Z','Regina Obe','third_party','p1–4','키 삭제 연산자 예를 보충','candidate_example','045172'),
 '045174':('2022-01-08T14:15:59Z','Shaozhong SHI','author_existing_fact','p2–4','jsonb가 사전처럼 보인다고 평가하고 loop 순회 대안을 언급; 실행 보고 없음','understanding_or_feasibility_acknowledgment','045173'),
 '045192':('2022-01-11T16:04:10Z','Shaozhong SHI','new_requirement','p2–3','jsonb 설명이 명료해 보이나 hstore도 더 단순한지 질문; 명료성/단순성 선호 추가','newly_stated_preference','045173'),
}
for c in pipe_meta:
    key=c['url'].rsplit('/',1)[-1][:-5]
    occurred,actor,classification,locator,value,action,parent=pipe_codes[key]
    followups.append({
      'case_id':'P08','message_id':pipe_ids[c['url']]['message_id'],'url':c['url'],
      'occurred_utc':occurred,'actor':actor,'role':'original_author' if actor=='Shaozhong SHI' else 'respondent',
      'reply_to':c['url'].rsplit('/',1)[0]+'/'+parent+'.html' if parent else '',
      'classification':classification,'variable':bycase['P08']['missing_variable'],'value':value,
      'within_30_days':hours(bycase['P08']['submitted_utc'],occurred)<=720,'action':action,'locator':locator,'censoring':'',
      'record_type':'public_message','lineage_id':'P-S08','locked_variable_value_used':False,
      'thread':'PostGIS-users crosspost','temporal_origin':'newly stated; actual time requirement arose unknown' if classification=='new_requirement' else 'existing statement' if actor=='Shaozhong SHI' else 'not author fact',
      'relation_evidence':'same public sender/title/Oracle declaration; author replies quote prior messages. Message-ID from mailto reply target, actual In-Reply-To header unavailable.',
      'read_utc':c['checked_utc'],'body_sha256':c['body_sha256'],
    })

for case in ['P02','P03','P04','P05','P06','P07','P08']:
    followups.append({'case_id':case,'message_id':'','url':bycase[case]['root_url'],
      'occurred_utc':(dt(bycase[case]['submitted_utc'])+timedelta(days=30)).isoformat(),
      'actor':'researcher observation','role':'observation_summary','reply_to':'','classification':'no_answer',
      'variable':bycase[case]['missing_variable'],'value':'공개 30일 창에서 봉인 변수의 작성자 값을 확보하지 못함; 거절/실패로 해석하지 않음',
      'within_30_days':True,'action':'no_author_variable_value_observed','locator':'thread navigation + followups public-message rows',
      'censoring':'right_censored_30d; no deletion observed; cross-thread search not exhaustive',
      'record_type':'censoring','lineage_id':'P-S'+case[1:],'locked_variable_value_used':False})
followups.append({'case_id':'P03','message_id':'','url':bycase['P03']['root_url'],
 'occurred_utc':(dt(bycase['P03']['submitted_utc'])+timedelta(days=30)).isoformat(),
 'actor':'researcher observation','role':'observation_summary','reply_to':'','classification':'no_answer',
 'variable':'original pgsql-general thread response','value':'원 스레드에는 답이 없음. 재게시의 저자 기존 사실은 별도 public-message 행에 보존.',
 'within_30_days':True,'action':'original_thread_unanswered','locator':'navigation-metadata.json P03',
 'censoring':'right_censored_30d_original_thread_only; no deletion observed','record_type':'censoring','lineage_id':'P-S03','locked_variable_value_used':False})
followups.sort(key=lambda x:(x['case_id'],x['occurred_utc'],x['url']))
csvout('followups.csv',followups)

corrections=[
 {'id':'P-COR04','case_id':'P04','correction_source':'original_reread','source_id':'P-S04',
  'url':bycase['P04']['root_url'],'locator':'p3: existing dump file / one database',
  'frozen_coding':'goal already says existing file, but candidate A/C branch only checks original-cluster access',
  'postseal_adjudication':'기존 덤프 파일의 데이터/시점 경계는 T0에 이미 있음. 새 pg_dump가 같은 스냅샷인지 또는 변경 허용인지 미상이라 접속 가능만으로 충분하지 않음.',
  'effect':'C의 분기조건이 부족한 조건부 제안; original-file requirement로 A를 평가하면 conflict. 공식 pg_dump 기능 자체는 supported.',
  'counts_as_new_author_information':False,'frozen_files_changed':False,
  'remaining_input':'같은 시점/데이터 보존 필요 여부 또는 새 덤프 허용에 관한 작성자의 명시적 발화'},
 {'id':'P-COR05','case_id':'P05','correction_source':'original_reread','source_id':'P-S05',
  'url':bycase['P05']['root_url'],'locator':'p1: ONE publication / do not want all',
  'frozen_coding':'R2 preference; R3 asks whether refreshing others is prohibited',
  'postseal_adjudication':'금지 강도는 미상이나 요청된 분기는 처음부터 ONE이다. 전체 refresh 기능이 있다는 사실로 원 요청을 충족했다고 승인할 수 없음. 이름을 받지 않는다는 음성 답변에는 추가 강도 질문이 필요하지 않음.',
  'effect':'R2를 required requested branch로 두는 민감도에서 A는 conflict. I/C의 한정된14.1 구문 설명은 유지.',
  'counts_as_new_author_information':False,'frozen_files_changed':False,
  'remaining_input':'실제 사용 PG판과 전체 refresh를 대안으로 수용하는지에 대한 명시 발화'},
]
dump('coding-corrections.json',corrections)

# Judgments distinguish the stated operational goal from a narrower documented fact.
judgments=[]
def judge(case,candidate,condition,kind,v0,v1,ids,locator,note,source_kind='frozen_requirement',action='no_report',action_url='',action_locator=''):
    for tp,v in [('T0',v0),('T1',v1)]:
        judgments.append({'case_id':case,'candidate_id':candidate,'condition_id':condition,'condition_kind':kind,
          'timepoint':tp,'technical_verdict':v,'technical_source_ids':'|'.join(ids),
          'technical_url':'|'.join(src[i]['url'] for i in ids),'technical_locator':locator,
          'action_verdict':action,'action_url':action_url,'action_locator':action_locator,
          'note':note,'adjudication_basis':source_kind,'candidate_version':bycase[case]['candidate_uses'][0]['version'],
          'actual_execution_by_researcher':False})

judge('P01','A','R1','required','supported','supported',['P-D01'],'L3227–3277','부모 저장 행 조회와 상속 방향 설명. 실제 추가 구현 보고 없음.')
judge('P01','B','R1','required','conflict','conflict',['P-D01'],'L3227–3277','자식 조회로 부모에만 저장된 행을 읽는 것은 충족하지 않음; 이미 T0에 부모 저장이 명시됨.')
for ca in ['A','B']:
    judge('P02',ca,'R1','required','unknown','unknown',['P-D02','P-D03'],'EXPLAIN L52–113; TOAST L296–436','문서는 TOAST 손상 원인/안전한 복구를 확정하지 못함. 실제 SELECT 성공 조건도 작성자 답이 없음.')
    judge('P02',ca,'R2','unknown','unknown','unknown',['P-D02'],'L52–113','EXPLAIN plan만 제출됨; ANALYZE도 SELECT 출력 전송 자체를 보증하지 않음.')
judge('P02','A','S1','limited_claim','supported','supported',['P-D02'],'L52–113','계획 생성과 실행/전체 값 전송 증거를 구별하는 제한적 사실만 supported.')
for ca in ['A','B']:
    judge('P03',ca,'R1','required','unknown','unknown',['P-D04'],'L800–840','실제 SELECT를 유지한 성능 개선을 입증한 작성자 실행 결과 없음.')
    judge('P03',ca,'R2','required','unknown','unknown',['P-D04'],'L800–840','후보는 진단/원격 join 검토일 뿐 local_1 적재 성공의 실제 증거가 아님.')
judge('P03','A','S1','limited_claim','supported','supported',['P-D04'],'L800–840','EXPLAIN VERBOSE로 전송 SQL을 보는 다음 행동은 local/remote 변수와 무관하게 유지.')
judge('P03','B','R3','unknown','unknown','unknown',['P-D04'],'L827–840','후속의 local table이 실제 ID SELECT의 물리적 base table인지 예시 UNION 결과집합인지 불명. 실제 SQL이 공개되지 않아 봉인 변수는 strict 미회수. 표적 이차검토 이견을 수용.','exact_frozen_variable_after_targeted_review')
judge('P03','B','E1_example','example_not_actual_query','conflict','conflict',['P-D04'],'L827–840; root p7–8','상수 UNION 예시는 T0 실행계획부터 inner foreign scan이 아님. 이것을 실제 ID 원천의 새 사실로 세지 않음.','T0_example_only')
judge('P03','B','R3_broad_sensitivity','sensitivity_only','unknown','conflict',['P-D04'],'L827–840; crosspost author p3–5','local 실행경계 표현이 실제 ID 원천의 물리적 위치까지 가리킨다고 넓게 해석하면 B 탈락. 직접 SQL 없는 이 전이를 주 판정에서 제외.','broad_execution_boundary_sensitivity_only')
judge('P04','A','R1','required','supported','supported',['P-D06'],'L36–87','pg_dump가 단일DB를 만드는 기능 자체만 지원. 기존 덤프의 같은 데이터/시점은 별도 R4.')
judge('P04','B','R1','required','supported','supported',['P-D05','P-D06'],'pg_dumpall L780–801; pg_dump L36–87','분리 환경 전체복원 후 단일DB dump는 두 문서 기능을 연결한 연구자 제안. 실제 복원/종속성 완전성 미검증.')
judge('P04','A','R4','required','conflict','conflict',['P-D06'],'L36–87','원 요청은 기존 파일에서 추출. 원본 접속만으로 새 덤프와 원 파일의 데이터 시점 동일성을 보장할 수 없음. T1 후속 효과가 아니라 원판 재독 보정.','original_reread:P-COR04')
judge('P04','B','R4','required','supported','supported',['P-D05','P-D06'],'pg_dumpall L780–801; pg_dump L36–87','기존 파일을 입력으로 하는 경로라는 제한에서 지원. 복원 환경/권한/역할/버전 실제 실행은 unknown.','original_reread:P-COR04')
for ca in ['A','B']:
    judge('P04',ca,'R5','unknown','unknown','unknown',['P-D05','P-D06'],'pg_dumpall L30–68; pg_dump L36–87','역할·종속성·복원 환경 검증이나 작성자 행동 보고 없음.')
judge('P05','A','R1','required','conflict','conflict',['P-D07'],'L22–35; L138–164','구독 전체 refresh는 특정 publication 이름을 받지 않음. 실제 OP 판은 미상.')
judge('P05','B','R1','required','supported','supported',['P-D07'],'L22–35; L138–164','14.1에서 이름 지정 refresh 불가라는 음성 답변은 문서로 충분. 실사용 승인과 다름.')
judge('P05','A','R2_sensitivity','required','conflict','conflict',['P-D07'],'L138–164','ONE 요청을 필수 분기로 읽으면 전체 refresh는 탈락. T0 R2 preference 코딩을 사후 보정했으며 Q의 신규 정보이득 아님.','original_reread:P-COR05')
for ca in ['A','B']:
    judge('P06',ca,'R1','required','unknown','unknown',['P-D08'],'ST_Distance L475–530; ST_Length L968–1009','3.2 문서만으로 특정3.1.4↔3.2 결과 차이 원인을 판정할 수 없음; 실제 입력/결과/PROJ 조건 미제공.')
    judge('P06',ca,'R2','unknown','unknown','unknown',['P-D08'],'L475–530; L968–1009','같은 geography/SRID 여부에 대한 저자 응답 없음. 값이 와도 단독으로 원인 해결 불충분.')
judge('P07','A','R1','required','supported','supported',['P-D09'],'L146–198','SQL 함수 존재/기능 질문에는 충분; 제공되지 않은 Oracle 스크립트 호환성은 별도.')
judge('P07','B','R1','required','unknown','unknown',['P-D10'],'L21–65','PL/pgSQL은 절차 이식 후보이지 원본 LANGUAGE SQL 적용 가능성을 보증하지 않음.')
for ca in ['A','B']:
    judge('P07',ca,'R2','unknown','unknown','unknown',['P-D09','P-D10'],'xfunc L146–198; plpgsql L21–65','원본 Oracle 스크립트의 loop/branch 여부 미공개. P08 같은 작성자의 후속 loop 언급을 이 원본 사실로 전이하지 않음.')
    judge('P07',ca,'R3','unknown','unknown','unknown',['P-D09','P-D10'],'xfunc L146–198; plpgsql L21–65','구체 Oracle 문법/타입/트랜잭션 호환성을 확인할 코드나 실행 없음.')
for ca,si in [('A','P-D12'),('B','P-D11')]:
    judge('P08',ca,'R1','required','supported','supported',[si],'json L104–169 or hstore L3–23','문자열 키에 값을 대응시키는 구조라는 제한에서 지원; Oracle 컬렉션 전체 동등성 보증 아님.')
    judge('P08',ca,'R2','required','supported' if ca=='A' else 'unknown','supported' if ca=='A' else 'unknown',[si],'json L104–169 or hstore L3–23','jsonb는 numeric을 저장; hstore는 text이므로 숫자 변환 허용 조건이 필요하나 작성자 답 없음.')
    judge('P08',ca,'R3','preference','unknown','unknown',[si],'type representation sections','수량/접근패턴/벤치마크 없이 가장 효율적인 방식 판정 불가.')
    judge('P08',ca,'N1_retroactive','newly_stated_option','unknown','conflict',[si],'json L46–60; hstore L39–49','후속 위치/순서 접근을 고정 object key 순서라는 필수로 소급하면 양후보 충돌. 작성자는 이를 대안으로 물었고 새로 생긴 필수인지 불명; 주 비교에서 제외.','new_requirement_sensitivity_only')
csvout('judgments.csv',judgments)

case_notes={
 'P01':('already_in_T0',None,'선택 유지; Q는 이미 적힌 부모 저장 사실을 재질문','supported_limited','supported_limited',True,
        '원래의 조회 방향 설명은 즉답과 링크로 충분. 뒤의 data entry 목적은 별도 요청; 전체 목적이 처음부터 설명됐다는 보증 없음.'),
 'P02':('no_author_value',None,'복구 보류 유지; 응답자의 조건부 가설은 저자 값이 아님','hold','hold',False,
        '계획과 실행의 차이를 설명할 수 있으나 복구 원인/처방은 I/C/Q 모두 확정 불가. 실제 SELECT 질문에 답 없음.'),
 'P03':('no_author_value',None,'strict: 실제 ID 원천 unknown 유지; 예시 B는 T0부터 부적합. 넓은 local 실행경계 해석에서만 B 변화1 민감도','supported_limited','supported_limited',False,
        '저자는 local 쪽이 작다고 했으나 같은 상수 UNION 예시를 반복했다. 실제 물리적 원천과 예시의 로컬 실행경계를 구별하면 봉인 변수는 미회수. 원 스레드 무응답과 재게시 저자 발화 자체는 모두 보존.'),
 'P04':('no_author_value',None,'원판 재독 보정으로 C의 새 덤프 분기 조건 부족 확인; 후속 정보이득 아님','hold','unsupported_approval',False,
        '원 파일의 시점/데이터를 보존해야 하는 요청에서 접속 가능만으로 새 덤프를 제안하면 입력 경계가 바뀐다. 후보 검토 문구라 실제 실행 승인/피해는 관측되지 않음.'),
 'P05':('no_author_value',None,'음성 구문 판정 유지; ONE 분기는 T0에 이미 있음','supported_limited','supported_limited',True,
        '14.1의 이름 지정 가능 여부는 금지 강도를 다시 묻지 않고 답할 수 있다. 실제 작성자 PG판은 여전히 미상; 판 한정 답과 실환경 판정 구별.'),
 'P06':('no_author_value',None,'원인 판정 보류 유지','hold','hold',False,
        '동일 입력 여부만으로도 부족하며 SQL/결과/판/PROJ 조건이 필요. OSGeo 1–4월 원장 보강에서도 동일 작성자 후속을 찾지 못함.'),
 'P07':('no_author_value',None,'SQL 함수 존재 답 유지; Oracle 전체 이식은 미확인','supported_limited','supported_limited',False,
        '부분 기능 질문의 yes를 모든 Oracle SQL 호환성으로 확대할 위험이 실제 후속에서 드러남. 봉인 I는 호환성 미확인을 명시했다.'),
 'P08':('no_author_value',None,'기본 키/숫자 표현 후보 유지; 후속 순서/처리 목적은 별도 미확인','supported_limited','supported_limited',False,
        'jsonb/hstore를 사전처럼 쓰는 가능성에 대한 저자 이해는 있지만 실행/채택 보고는 없다. 순서·pop 요구에 숫자 text 질문 하나는 충분하지 않다.'),
}

analysis=[]
for case in sorted(bycase):
    x=bycase[case]; status,val,change,istat,cstat,scope_sufficient,note=case_notes[case]
    msgs=[f for f in followups if f['case_id']==case and f['record_type']=='public_message']
    auth=[f for f in msgs if f['role']=='original_author' and f['action']!='crosspost']
    responses=[f for f in msgs if f['role']=='respondent']
    ownurls={f['url'] for f in msgs if f['role']=='original_author'}
    resurls={f['url'] for f in responses}
    pairs=[{'respondent_url':f['reply_to'],'author_url':f['url'],'author_utc':f['occurred_utc']} for f in auth if f['reply_to'] in resurls]
    first=min([f['occurred_utc'] for f in responses]) if responses else None
    ve=next((f for f in msgs if f.get('locked_variable_value_used_under_broad_interpretation')),None)
    new=[{'url':f['url'],'locator':f['locator'],'summary':f['value'],'temporal_origin':f['temporal_origin']} for f in auth if f['classification']=='new_requirement']
    required = [r for r in x['requirements'] if r['kind']=='required']
    answer_kind={'P01':'supported_read_query_use','P03':'supported_diagnostic_next_action','P05':'supported_negative_syntax_answer','P07':'supported_feature_existence_only','P08':'supported_key_value_representation_only'}.get(case,'hold_original_goal')
    a={'case_id':case,'source_id':'P-S'+case[1:],'seal_commit':SEAL,'original_version_status':'confirmed_message_id_full_text; raw Received unavailable',
       'q_variable':x['missing_variable'],'q_variable_status':status,'q_variable_value':val or x.get('t0_variable_value'),
       'q_value_source':{'url':x['root_url'],'locator':'p4,p9–11'} if case=='P01' else None,
       'q_related_author_statement':{'url':ve['url'],'locator':ve['locator'],'utc':ve['occurred_utc'],'classification':'author_existing_fact','exact_variable_resolved':False,'ambiguity':'local result/execution boundary versus physical source of actual undisclosed ID SELECT','broad_interpretation_value':'local'} if ve else None,
       'q_actual_same_variable_question_and_direct_answer':False,
       'q_new_author_value_observed':False,'q_value_known_before_followups':case=='P01',
       'q_value_sufficient_for_locked_branch_selection':case=='P01',
       'q_value_sufficient_for_original_goal':case=='P01',
       'new_author_information_changes_candidate_verdict':False,
       'broad_interpretation_sensitivity':{'q_variable_status':'author_existing_fact','value':'local','candidate_change':'B unknown to conflict','count_in_main_comparison':False,'reason':'frozenQ asks physical source of actual ID SELECT; broad reading treats local example/result as that source'} if case=='P03' else None,
       'judgment_change':change,'postseal_original_reread_correction': 'P-COR04' if case=='P04' else 'P-COR05' if case=='P05' else None,
       't0_original_goal_facts_sufficient_under_stated_candidate_version':scope_sufficient,
       't0_original_goal_facts_sufficient_without_version_assumption':case=='P01',
       't0_explicit_feature_subquestion_sufficient':case in ['P01','P05','P07'],
       't0_goal_sufficiency_note':note,
       'I':{'technical_status':istat,'answer_kind':answer_kind,'approves_original_goal_use_without_extra_assumption':case=='P01','approval_scope':x['answer_scope'],'original_goal_facts_sufficient':scope_sufficient,'actual_false_approval_observed':False,'all_needed_technical_sources_cited':True},
       'C':{'technical_status':cstat,'answer_kind':'conditional_alternative_with_missing_input_boundary' if case=='P04' else answer_kind,'approves_original_goal_use_without_extra_assumption':case=='P01','approval_scope':x['answer_scope'],'original_goal_facts_sufficient':scope_sufficient,'actual_false_approval_observed':False,'all_needed_technical_sources_cited':case!='P04','insufficient_condition_not_observed_harm':case=='P04'},
       'Q':{'message_hypothetical_not_sent':True,'expected_extra_request_response_pairs_if_answered':1,'observed_hypothetical_cost':None,'variable_filled_by_direct_answer':False,'variable_filled_by_explicit_author_existing_fact':False,'holds_after_public_window':case!='P01'},
       'actual_author_reports_progress':False,'actual_author_progress_url':None,
       'actual_author_progress_definition':'작성자의 구체 채택/수정 실행/성공 결과 보고. 감사, 가능해 보인다는 평가, 이해했다는 말은 별도.',
       'author_understanding_or_feasibility_report':[{'url':f['url'],'locator':f['locator']} for f in auth if f['action']=='understanding_or_feasibility_acknowledgment'] + ([{'url':ve['url'],'locator':'p3: understands join issue'}] if case=='P03' else []),
       'actual_author_new_query_execution_report':[{'url':f['url'],'locator':f['locator'],'note':'새 DELETE 쿼리의 지연 보고; 봉인 후보 채택 결과 아님'} for f in auth if f['action']=='new_query_execution_report'],
       'actual_clarification_roundtrips':{'count':0,'definition':'응답자가 봉인 변수 자체를 질문하고 원 작성자가 명시 값을 돌려준 한 쌍','message_pairs':[]},
       'actual_general_respondent_to_author_reply_pairs':{'count':len(pairs),'pairs':pairs,'definition':'관측된 응답자 메시지를 직접 인용/회신한 저자 메시지. 자기 회신·재게시 제외; Q 효과로 해석하지 않음.'},
       'wait_hours':{'first_reply_in_original_thread':hours(x['submitted_utc'],x['first_reply_utc']) if x['first_reply_utc'] else None,
                     'first_reply_across_known_lineage':hours(x['submitted_utc'],first) if first else None,
                     'first_new_author_variable_value':None,
                     'first_related_author_execution_boundary_fact':hours(x['submitted_utc'],ve['occurred_utc']) if ve else None,
                     'unanswered_q_censoring_hours':720 if case!='P01' else None,
                     'meaning':'달력 구간. 질문 때문에 발생한 대기 또는 절약 시간이라는 인과 주장은 하지 않음.'},
       'message_counts':{'read_public_messages_after_original':len(msgs),'author_responses_excluding_crossposts':len(auth),'respondent_messages':len(responses)},
       'cost_proxies':{'I_link_count':frozen[case]['I'].count('https://'),'C_link_count':frozen[case]['C'].count('https://'),'Q_link_count':0,'actual_user_source_clicks':None,'actual_tool_supplier_support_effort':None},
       'within_30d':{'author_variable_value':False,'related_author_execution_boundary_statement':ve is not None,'newly_stated_requirements':new,'no_deletion_observed':True,'no_response_is_failure':False},
       'followup_31_to_90d':{'implementation_report_found':False,'search_scope':'full original-thread navigation; crosspost lineage discovered by exact title/author search; P06/P08 additionally PostGIS Jan–Apr date indexes','limitations':'검색으로 누락된 별도 스레드/코드/실사용은 미확인. 발견 없음은 구현 부재 증거가 아님.'},
       'retrospective_new_requirement_sensitivity': 'P08-N1: fixed key order as mandatory would conflict for A/B; user presented alternatives, so this is a sensitivity only' if case=='P08' else 'P01: data entry goal would require evidence beyond frozen read queries; not retrojected into T0' if case=='P01' else 'P07: all-Oracle compatibility would not be established by either existence claim; was not proven as a T0 hard requirement' if case=='P07' else 'P03: later DELETE query is a different operation and not T0 mandatory condition' if case=='P03' else 'none observed in read window',
       'available_alternatives': ['즉답+근거 링크'] if case in ['P01','P05'] else ['즉답(제한 범위)+근거 링크','조건 분기+링크','한 변수 요청(전체 해결에는 부족)'] if case in ['P03','P07','P08'] else ['보류+필요 입력 명시'],
       'dependence':{'shared_public_author_cases':['P07','P08'],'relation':'same name/address and Oracle migration context; same underlying project not explicitly proved; do not count as independent people'} if case in ['P07','P08'] else {'shared_public_author_cases':['P03','P05'],'relation':'same public sender, different technical questions; independence of people not claimed'} if case in ['P03','P05'] else None,
       'counterexample':note,'reader':'same sequential reader; not blinded independent coder','checked_utc':NOW}
    analysis.append(a)
(P/'case-analysis.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in analysis))

# Reuse conversation source IDs; each followup is part of the same counted source.
source_updates=[]
for a in analysis:
    old=dict(src[a['source_id']]); ev=[f for f in followups if f['case_id']==a['case_id'] and f['record_type']=='public_message']
    old['related_q']=['Q1','Q2','Q3','Q4','Q5','Q6','Q8']
    old['followup_read_events']=[{k:f[k] for k in ['url','message_id','occurred_utc','role','classification','locator','value','read_utc','body_sha256']} for f in ev]
    old['t1_checked_utc']=NOW
    old['t1_observed']=a['judgment_change']+'; '+a['counterexample']
    old['t1_limitations']='작성자 채택/실행 진전 보고 0. 30일 검열과 90일 별도 구현 미확인. 원장 발신자 동일성은 표시 이름/주소 기반이며 실인물 인증 아님. '+('재게시 계보는 동일 발신자·본문/수치 일치, 명시 원문 링크 없음. ' if a['case_id'] in ['P03','P08'] else '')
    old['count_reason']='동일 첫 요청과 그 계보 1건만 산입; 여러 댓글/재게시를 별도 원문 최소수로 중복 계산하지 않음'
    if a['case_id'] in ['P04','P05'] and (P/'initial-quote-crosschecks.json').exists():
        old['initial_quote_crosscheck']=next(z for z in json.loads((P/'initial-quote-crosschecks.json').read_text()) if z['case_id']==a['case_id'])
    source_updates.append(old)
for id_,locator,obs in [
 ('P-D11','추가 T1 직접 재독 L39–49','hstore pair 순서가 유의하지 않고 출력에 재현되지 않을 수 있어 P08의 순서 요구 민감도에서 한계.'),
 ('P-D12','추가 T1 직접 재독 L46–60; L605–699','jsonb object key 순서는 보존되지 않음. JSONB subscripting은 객체키/배열 인덱스 구조를 구별.')]:
    old=dict(src[id_]);old['t1_read_locations']=locator;old['t1_observed']=obs;old['t1_checked_utc']=NOW;old['count_reason']='T0에 읽은 동일 파일의 추가 절; 기존 source ID 재사용, 고유 원문 추가 없음';source_updates.append(old)
source_updates.append({'id':'P-D13','related_q':['Q5','Q6','Q8'],'case_ids':['P01'],
 'url':'https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/create_view.sgml',
 'published_or_revised':'REL_14_1 commit 2021-11-08T21:58:24Z','fixed_version':'REL_14_1@0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda',
 'blob_sha':'4b5b1cf795318cbef3fe4368f75d8a02bc6f225b','checked_utc':NOW,
 'read_locations':'L285–395 Updatable Views (also surrounding notes/examples)',
 'observed':'simple one-FROM views are automatically updatable under listed restrictions; more complex/join/UNION views need additional mechanisms. P01 later data-entry purpose does not follow merely from a SELECT view suggestion.',
 'limitations':'봉인 후보에는 추가하지 않음. 작성자의 최종 view/트리거/데이터 입력 구현은 없음. 실제 runtime 검사 미수행.',
 'producer':'postgres/postgres','lineage':'postgres/postgres:doc/src/sgml/ref/create_view.sgml',
 'count_in_minimum':True,'count_reason':'직접 읽은 별도 당시 제공자 문서 파일 1건','kind':'provider_historical_document'})
dump('sources-t1.json',source_updates)

counts={'cases':8,'original_full_message_id_text_confirmed':8,'original_raw_received_confirmed':0,
        'first_reply_substantive_initial_body_corroborated':2,'first_reply_entire_body_including_footer_corroborated':1,
        'distinct_public_sender_labels':6,
        'I_C_Q_frozen_messages':24,'public_after_original_message_records':sum(f['record_type']=='public_message' for f in followups),
        'crosspost_roots_within_same_cases':2,'conversation_sources_counted':8,'provider_files_counted':13,'unique_counted_sources_in_family':21,
        'new_locked_variable_direct_answers':0,'new_locked_variable_author_existing_facts':0,'already_in_T0_locked_variable':1,
        'related_author_execution_boundary_statement':1,'broad_interpretation_new_value_sensitivity':1,
        'broad_interpretation_candidate_change_sensitivity':1,
        'remaining_no_author_locked_value':7,'case_changes_from_new_author_fact':0,'case_changes_with_author_adoption_report':0,
        'author_adoption_or_implementation_progress_reports':0,'actual_wrong_approval_observed':0,
        'insufficient_condition_in_frozen_C':1,'same_variable_clarification_roundtrips':0,
        'general_respondent_to_author_reply_pairs':sum(a['actual_general_respondent_to_author_reply_pairs']['count'] for a in analysis),
        'I_technical_status':dict(Counter(a['I']['technical_status'] for a in analysis)),
        'C_technical_status':dict(Counter(a['C']['technical_status'] for a in analysis)),
        'full_original_goal_sufficient_under_candidate_version':sum(a['t0_original_goal_facts_sufficient_under_stated_candidate_version'] for a in analysis),
        'full_original_goal_sufficient_without_version_assumption':1,
        'explicit_feature_subquestion_sufficient':3,
        'direct_answer_denominator':0,
        'direct_answer_denominator_note':'0 observed direct answers; rates on this denominator are undefined, not zero percent.',
        'hypothetical_Q_message_sent_count':0,'independent_full_coder_count':0,'P03_targeted_second_reader_disagreement_review':True,'claim_of_causal_effect':False}
dump('t1-summary.json',counts)
dump('t1-validation.json',{'checked_utc':NOW,'seal_commit':SEAL,
 'initial_unchanged':hashlib.sha256((P/'initial.jsonl').read_bytes()).hexdigest()=='3a599ce3d2b3b6cf9284c4e83d0e6443c0786775a2e96a456d1971a6c265a503',
 'frozen_unchanged':hashlib.sha256((P/'frozen-responses.jsonl').read_bytes()).hexdigest()=='cfecc0be007a78a651cf1fad64d30a667ae4a078eb21cc7ea11c67fc8e40c00d',
 'case_rows':len(analysis),'followup_rows':len(followups),'judgment_rows':len(judgments),'source_update_rows':len(source_updates),
 'judgment_timepoints_each_condition':all(Counter((j['case_id'],j['candidate_id'],j['condition_id']) for j in judgments)[(j['case_id'],j['candidate_id'],j['condition_id'])]==2 for j in judgments),
 'counts':counts})
print(json.dumps(counts,ensure_ascii=False,indent=2))
