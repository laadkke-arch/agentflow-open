from pathlib import Path
import json,csv,datetime,hashlib,re
P=Path(__file__).parent; E=P/'evidence'; C=E/'unread_cache'; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sets={k:json.loads((C/f'{k}.json').read_text())['items'] for k in ['A2023','A2024','B2023']}
roots={x['number']:x for v in sets.values() for x in v};mapping={int(k):v for k,v in json.loads((C/'selected-mapping.json').read_text()).items()}
# Researcher paraphrases, based only on current root and first substantive external reply.
goals={
'D01':'CHECK 제약식에 중첩 lambda를 사용하고 내부 참조 오류의 원인을 찾음',
'D02':'BufferManager 메모리 예약/퇴거에서 동시에 두 스레드가 실패하는 경쟁상황을 설명하고 할당 가능성을 보존함',
'D03':'list comprehension/lambda로 만든 URL 문자열을 read_parquet/read_csv 인수로 사용함',
'D04':'DST 경계를 넘는 timestamp 뺄셈과 덧셈의 역연산 일관성을 기대함',
'D05':'같은 timestamptz와 복합 interval 덧셈이 PostgreSQL/DuckDB에서 하루 차이 나는 이유를 확인함',
'D06':'고정 길이 ARRAY를 list_zip에 전달해 LIST와 같은 zip 결과를 얻음',
'D07':'NumPy float 배열의 NaN을 DuckDB 왕복 뒤 유지하고 MaskedArray.fill_value 동작을 맞춤',
'D08':'client별 시간순 창에서 최신 status를 last로 반환하고 lag와 비교함',
'DB01':'20GB 이상 CSV를 로컬 DB로 읽고 Parquet로 내보내는 3시간 비용을 줄임',
'DB02':'WITH CTE 안에서 DESCRIBE 결과를 쿼리함',
'DB03':'소스 빌드 CLI 시작 화면의 실제 판 번호를 파악함',
'DB04':'CSV의 null 표시를 SQL NULL로 읽고 Mac/Ubuntu 결과 차이를 설명함',
'DB05':'Windows11 Go ODBC에서 CSV reader 옵션을 매개변수 쿼리로 전달함',
'DB06':'R relational API에서 lag와 partitioned window를 사용함',
'DB07':'dplyr 사용에서 window 연산 전 원래 행 순서를 결과에 보존함',
'DB08':'Windows Python에서 CSV를 Parquet로 바꾸다 생긴 상세 없는 IOException의 원인을 찾음',
'DB09':'따옴표 있는 CSV 헤더를 정확히 해석하고 sample_size에 따른 이름 변경을 막음',
'DB10':'CREATE TYPE 별칭에 UNION 전용 함수를 적용함',
'DB11':'CLI BLOB 문자열을 복사할 때 DEL 비인쇄문자를 이스케이프함',
'DB12':'첨부 Parquet 파일을 count 쿼리로 읽고 segfault 원인을 확인함',
'DB13':'CSV 앞줄을 skip하며 experimental parallel reader를 사용함',
'DB14':'Windows Python에서 지정한 절대 DB 경로를 열음',
'DB15':'date_sub week가 1초 짧은 주/연도에 반환하는 값을 해석함',
'DB16':'다른 자료형의 두 SELECT를 UNION할 때 암시적 캐스팅이 의도인지 확인함',
'DB17':'Tableau JDBC로 timestamp를 preview하고 시간 단위로 집계함',
'DB18':'중첩 STRUCT를 지정해 Zulip JSON을 읽음',
'DB19':'Pandas2 Arrow string null 배열을 DuckDB에 register함',
'DB20':'UUID와 primary key를 갖는 DB/Parquet의 저장크기 차이를 설명함',
'DB21':'빈 schema.sql을 가진 export를 import database로 읽음',
'DB22':'SHOW TABLES에서 index가 table처럼 나타나는 현상을 확인함',
'DB23':'대소문자를 섞은 column을 split_part macro에 전달함',
'DB24':'Parquet timestamp를 fetchmany로 읽을 때 Python 메모리 누수를 막음',
'DB25':'INT2 subquery 피연산자와 직접 literal 비교의 행 결과 차이를 설명함',
'DB26':'AVG/REAL 상수와 subquery 계산의 부동소수 결과 차이를 설명함'}
known={
'D01':{'tried':'CREATE TABLE CHECK와 INSERT SQL, list_apply/list_filter','version':'master, MacOS unittest; 정확한 SHA 미기재','input':'i/j BIGINT[] 실제 예제 두 배열','desired_output':'중첩 lambda의 내부 참조 오류 없이 제약 판정; 정확한 기대 INSERT 결과는 미기재','preference_required_forbidden':'명시적 금지/선호 없음'},
'D02':{'tried':'두 스레드의 EvictBlocks 접근 순서를 두 시나리오로 구성','version':'C++, Linux5.15; 662041e2b43283bfcfeed984af7c3eaa85fb4996','input':'current_memory/extra_memory/memory_limit 숫자와 스레드 순서; 실제 워크로드인지는 미기재','desired_output':'시나리오1 한 스레드, 시나리오2 Thread2가 메모리 할당 가능해야 함','preference_required_forbidden':'임시 예약 상태의 스레드별 소유권/신호 제안'},
'D03':{'tried':'독립 SELECT와 같은 식을 read_parquet/read_csv에 넣은 비교','version':'v0.6.1, MacOS, cli/wasm','input':'a=1,b=2,c=3 문자열을 lower/list_string_agg','desired_output':'s,s,s 또는 duck,duck,duck 대신 배열 값으로 URL 구성','preference_required_forbidden':'명시 없음'},
'D04':{'tried':'origin+(dst-origin), gregorian/Europe-London 설정','version':'v0.6.2-dev942, OSX CLI','input':'2000-10-29T03:00Z, 2000-01-03T00:00Z','desired_output':'03:00 대신04:00 나오는 차이 제거','preference_required_forbidden':'역연산 일관성; 본문에 ICU 패치 진단 있으나 작성 시점 미확인'},
'D05':{'tried':'동일 timestamptz+month/day/minute/hour/second interval 비교','version':'DuckDB1.0, Python, Ubuntu20.04.5; PostgreSQL판 미기재','input':'1920-12-12 01:02:02+05:30 literal; connection time zone 이름 미기재','desired_output':'PostgreSQL1921-12-26 대비 DuckDB1921-12-25 차이 설명','preference_required_forbidden':'일치 기대; 오프셋+05:30을 연결 zone 이름으로 대체하지 않음'},
'D06':{'tried':'int[] 성공/int[3] binder error 대조','version':'1.0.0, MacOS, CLI/Python; nightly 시험 표시','input':'[1,2,3] 두 배열의 int[3]/int[] cast','desired_output':'고정길이 ARRAY zip 허용','preference_required_forbidden':'LIST 우회 허용 여부 미기재'},
'D07':{'tried':'np.array→DuckDB SELECT→fetchnumpy→filled','version':'1.0.0 Python, MacOS14.1.1 arm64; NumPy판 미기재','input':'[3.2,np.nan,9.1] float ndarray','desired_output':'float 결과에 NaN 보존, fill_value를1e20 대신nan','preference_required_forbidden':'MaskedArray 불필요라는 주장; NaN/NULL 구별 목적'},
'D08':{'tried':'last/first, doc ASC/DESC, lag(status) 대조','version':'v1.0.0 Python, Ubuntu20.04 x86-64','input':'client fa4행, TP5→TP7 및 네 doc 시각','desired_output':'client창의 마지막 status','preference_required_forbidden':'frame 지정 없음; 전체 partition 마지막인지 표면 목적에 의해 추론'} }
strat={'D01':'directive','D02':'mixed','D03':'no_substantive_response','D04':'no_substantive_response','D05':'information_request','D06':'no_substantive_response','D07':'directive','D08':'directive',
'DB01':'directive','DB02':'no_substantive_response','DB03':'conditional_action','DB04':'mixed','DB05':'no_substantive_response','DB06':'directive','DB07':'mixed','DB08':'directive','DB09':'no_substantive_response','DB10':'no_substantive_response','DB11':'conditional_action','DB12':'directive','DB13':'mixed','DB14':'directive','DB15':'directive','DB16':'directive','DB17':'mixed','DB18':'directive','DB19':'mixed','DB20':'directive','DB21':'no_substantive_response','DB22':'directive','DB23':'no_substantive_response','DB24':'directive','DB25':'directive','DB26':'no_substantive_response'}
firstsum={
'D01':'지원자가 별도 nested lambda 재현과 undefined-behavior를 보태고 두 버그를 함께 수정할 계획을 밝힘; 사용자 정보 요청 아님',
'D02':'한 스레드라도 OOM이면 전체 query abort이므로 실제 문제가 있었는지 이론 분석인지 묻고 수정시험 난점을 설명함',
'D05':'time zone을 요청함',
'D07':'NumPy 처리 경로가 pandas 구현에서 파생된 점과 Polars numpy/pandas NaN 처리 차이를 설명함',
'D08':'LAST가 frame에 적용되어 현재값이 나온다고 설명하고 LAST_VALUE 링크를 제안함; 의문형은 추정/수사로 분류, 조건값 회수를 요청하지 않음',
'DB01':'CSV를 in-memory DB에 로드해 보라고 권고함; 댓글 수정은2024년이라2023년 원형 미확인',
'DB02':'첫 타인 댓글은 외부 이메일 연락요청뿐; 실질 기술 응답 없음',
'DB03':'자기 fork에서 build했다면 upstream git tags를 받으라고 제안함',
'DB04':'제시 CSV로 재현 안 됨을 출력으로 보여주고 실제 파일 null이 따옴표로 묶였는지 물음',
'DB06':'PR6757에서 구현한 것으로 생각한다고 확인형 언급; 특정 환경/입력값 요청은 아님',
'DB07':'결과의 원하는 순서를 직접 묻고 partition/hash/sort/parallel 동작과 빈 OVER의 예외를 설명함',
'DB08':'동일 계열 #6931과 Windows 원인 추정을 연결함',
'DB11':'최신 master 수정PR6654와 출력 제공, 다른 BLOB문자열 지원을 원하면 별도 discussion 제안',
'DB12':'파일 파서 assertion/pyarrow 실패 및 중첩·encoding 진단; 의문형은 지원자의 추론이며 작성자값 직접요청 아님',
'DB13':'PR6977에서 이미 해결됐을 수 있으므로 해당 patch로 재시험 여부를 확인함; 순수 patch verification은 B 적격에서 제외',
'DB14':'Windows 경로 구분자 문제를 추정하고 과거 수정PR5852 연결',
'DB15':'Gregorian년은52주+1일이므로 예상 동작이라고 설명',
'DB16':'UNION 입력형이 다르면 compatible type로 cast하는 의도된 동작과 공식 링크 안내',
'DB17':'PostgreSQL dialect에서 받은 오류를 요청하며 해당 호환성을 지향한다고 설명함',
'DB18':'중복으로 보이는 #6569로 연결함; 기술적 경로 제공',
'DB19':'PR7005로 재현하는지 재시험 요청; master에서 현재 예상이라는 설명. B 환경/목표/입력값 질문에서 제외',
'DB20':'PRIMARY KEY ART index의 추가 공간을 설명하고 UUID-only/문자열/PK 비교 출력 제시',
'DB22':'information_schema.tables 사용을 권고하며 index 물리적 성격 추측 제공',
'DB23':'첫 타인 댓글은 자기 commit이 원인이 아님을 농담한 인사성 발화; 실질 응답 없음',
'DB24':'PyDateTime 반환 reference ownership 오류와 수정코드를 제시함',
'DB25':'문자열→INT16 경계와 두 쿼리의 차이를 줄여 재현하고 남은 차이는 모른다고 설명함'}
exposure={'D01':'edit metadata 정규식이 첫 답 뒤 공급자3문장 일부를 우연 출력. 문구는 이후 분석 근거로 쓰지 않고 엄격 미노출 집합 제외.',
'D04':'current root 본문에 fix는 ICU 패치라는 결론 포함. 그것이 최초 진단인지 후대 편집인지 미확인; 보수적으로 노출표시.',
'DB17':'current root dialect 이름에 strikethrough/교정이 있어 후대 수정값을 노출했을 가능성. 원판 미복원.',
'DB26':'connector shape probe가 첫 댓글인 requester self-resolution을 필터 전 출력. 엄격 미노출 제외.'}
bs={'DB04','DB07','DB17'}
records=[]
for n,cid in mapping.items():
 r=roots[n];fpath=E/f'first-{n}.json';first=json.loads(fpath.read_text())
 if n==7045:first=json.loads((E/'first-7045-fallback.json').read_text())
 f=first.get('first_nonself_comment')
 if cid in ['DB02','DB23']:f=None
 rootmeta=json.loads((E/f'root-version-{n}.json').read_text()) if (E/f'root-version-{n}.json').exists() else {}
 info=known.get(cid,{'tried':'본래 To Reproduce 절의 시도','version':next(iter(re.findall(r'### DuckDB Version:\s*\n+([^\n]+)',r['body'])), '미기재'),'input':'To Reproduce 절의 코드/자료 또는 데이터 링크; 실제자료와 예제 동일성 별도 미확인','desired_output':goals[cid],'preference_required_forbidden':'원문에 명시한 범위 이외 필수조건 추가 없음'})
 score=4 if cid in ['D01','DB09','DB12'] else 5
 original='Q' if cid in ['DB04','DB07'] else 'U'
 # Quote corroborates only the quoted fragment, never the whole original.
 rec={'case_id':cid,'sample':'A' if cid.startswith('D0') else 'B_screen','project':'duckdb/duckdb','issue_number':n,'root_url':r['html_url'],'root_created_utc':r['created_at'],'root_updated_utc':r['updated_at'],'root_author':r['user']['login'],'author_association':r.get('author_association'),'supplier_also_requester': r.get('author_association') in ['MEMBER','OWNER','COLLABORATOR'] or cid=='D06','title':r['title'],'quarter':'2023Q1' if r['created_at'].startswith('2023-01') else ('2024Q3' if r['created_at'].startswith('2024-07') else '2023-04'),'request_type':'usage' if cid in ['DB01','DB06','DB07','DB16'] else 'bug','information_score':score,'information_score_basis':'current-body proxy; original not restored','goal':goals[cid],'root_conditions':info,'root_condition_locations':{'goal':'What happens? / title','tried':'To Reproduce','version':'OS / DuckDB Version / DuckDB Client','input':'To Reproduce code or attachment','desired_output':'What happens? / To Reproduce contrast','preference_required_forbidden':'What happens? (explicit only)'},'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'body_version':rootmeta.get('root_meta',{}).get('bodyVersion'),'original_grade':original,'original_limit':'whole first-version body unrecovered; current API updated_at is not a body-edit timestamp','compatibility_grade':'partial_quote_support' if original=='Q' else ('same_thread_partial_context' if f else 'no_first_reply_to_compare'),'first_strategy':strat[cid],'first_response_url':f.get('html_url') if f else None,'first_response_id':f.get('id') if f else None,'first_response_created_utc':f.get('created_at') if f else None,'first_response_updated_utc':f.get('updated_at') if f else None,'first_responder':f.get('login') if f else None,'first_response_summary':firstsum.get(cid,'공개 반환 댓글에서 타인의 실질 응답 없음'),'first_response_body_sha256':hashlib.sha256(f['body'].encode()).hexdigest() if f else None,'prior_self_comment_metadata':first.get('self_comments_before_first',[]),'has_information_question':cid in ['D02','D05','DB04','DB07','DB17'],'b_question_eligible':cid in bs,'b_action_only_request':cid in ['DB13','DB19'],'b_eligibility_note':'environment/goal/input를 직접 묻는 문장' if cid in bs else ('patch verification action; existing fact clarification과 구분' if cid in ['DB13','DB19'] else '첫 실질 응답에 직접 환경/목표/입력 질문 없음'),'exposure':cid in exposure,'exposure_note':exposure.get(cid,'후속 본문 미열람; current root 편집시점 불확실성은 별도 원판 등급으로 남김'),'checked_utc':now,'reader':'duckdb child agent; sequential self-coding, not independent blind duplication','future_outcome_opened_intentionally':False}
 if cid=='DB04':rec['root_conditions']['input']='current title은 quoted NULL, 본문 예제는 unquoted null; 첫 답이 예제3줄 인용. 실제 CSV와 예제 구별 필요'
 if cid=='DB07':rec['root_conditions']['preference_required_forbidden']='root에서 window 재정렬은 dplyr에 undesired라고 명시; 첫 답은 physical order/parallel joins까지 뜻을 확장해 물음'
 if cid=='DB17':rec['root_conditions']['input']='Tableau2023.1 MacOS13.3.1 DuckDB0.7.1; root첨부1 getTimestamp/FAB9A2C5, 첨부2 trunc 함수 부재; 어느 dialect 대응인지는 current strikethrough 편집과 구분 필요'
 records.append(rec)
with (P/'initial.jsonl').open('w') as f:
 for r in records:f.write(json.dumps(r,ensure_ascii=False)+'\n')
qs=[
('D02','observed_workload_vs_theoretical','Did you run into any problems caused by the current implementation','absent','실제 워크로드 장애','재현 워크로드와 올바른 스레드별 메모리 동작을 요구하고 수정 타당성을 검토','이론 분석만','현 시스템 abort 정책 설명과 시험 가능성 확인; 아직 실행성공/변경을 예측하지 않음','root는 두 schedule을 기술하지만 실제 실행인지 선언하지 않음'),
('D05','connection_time_zone','Please include your time zone when reporting issues like this.','absent','역사적 zone offset/전환이 관련된 설정','같은 zone으로 재현해 timezone-aware interval/DST 동작을 확인','해당 전환이 없는 zone','DuckDB/PostgreSQL interval 또는 ICU의 판/계산 차이 조사','literal +05:30는 connection zone 이름과 다른 변수'),
('DB04','actual_csv_null_is_quoted','is the null value perhaps quoted in the original CSV file?','unclear','실제 null 토큰이 인용됨','quoted-null 해석 옵션/입력처리 분기','실제 null 토큰이 비인용됨','제시 예제와 환경/판 재현 차이를 조사','current title에는 quoted라 쓰였으나 예제는 unquoted; 원형 title/본문 편집 복원 안 됨'),
('DB07','desired_result_order_contract','What do you mean by "may reorder the result"?','already_present','최초 입력 물리순서를 보존','명시 row-order 키/최종 ORDER BY 또는 API보장 우회 검토','window partition/order 결과순서를 수용','현재 window 재정렬 설명으로 제한 답 가능','root의 undesired 재정렬은 이미 선언. 복합 join/parallel까지의 보장 요구는 아직 없음'),
('DB17','postgres_dialect_error','Are you able to provide the error you get when you use the postgres dialect?','unclear','생성 SQL의 함수 부재 오류','PostgreSQL 호환 함수/SQL 변환 또는 dialect 지원 조사','JDBC getTimestamp 변환 오류','JDBC 타입/driver 반환 변환 조사','root 첨부 오류2개 직접 확인했으나 current dialect 취소선 교정과 원판 시점 대응 미복원')]
rows=[]
for cid,var,quote,present,v1,a1,v2,a2,note in qs:
 r=next(z for z in records if z['case_id']==cid)
 rows.append({'question_id':cid+'-Q1','case_id':cid,'sample':r['sample'],'question_url':r['first_response_url'],'question_comment_id':r['first_response_id'],'question_created_utc':r['first_response_created_utc'],'questioner':r['first_responder'],'variable':var,'actual_question_excerpt':quote,'value_in_current_root':present,'value_in_first_version':'미확인' if r['original_grade']=='U' else '인용으로 일부만 보강; 전체원판 미확인','value_a':v1,'predicted_branch_a':a1,'value_b':v2,'predicted_branch_b':a2,'predicted_difference':'yes','note':note,'frozen_before_author_answer':True,'exposure':r['exposure'],'coded_utc':now})
with (P/'questions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Preserve every retrieved candidate but distinguish screening from over-fetched metadata.
fr=[]
exclude={5817:'build warnings only',12798:'debug build failure only',12800:'unit-test sanitizer/build infrastructure; no user query/output goal',6954:'announcement: author states fix already made and issue for affected users',6964:'compilation only',7002:'extension installation/loading only; no query/use objective',7009:'package build/link/load only'}
limits={'A2023':5826,'A2024':12804,'B2023':7045}
for group,xs in sets.items():
 for rank,r in enumerate(xs,1):
  cid=mapping.get(r['number'],'');selected=bool(cid);within=r['number']<=limits[group]
  rec={'frame_id':group+'-'+str(rank),'project':'duckdb/duckdb','sample':'A' if group.startswith('A') else 'B_screen','quarter':group,'candidate_rank':rank,'issue_number':r['number'],'root_url':r['html_url'],'created_utc':r['created_at'],'title':r['title'],'case_id':cid,'screened_for_selection':within,'root_directly_read':within or (group.startswith('A') and rank<=10) or (group=='B2023' and rank<=32),'root_eligible':selected if within else 'not_assessed_after_cap','included_A':selected and group.startswith('A'),'b_screen_rank':int(cid[2:]) if cid.startswith('DB') else '','b_question_eligible':cid in bs,'reason':('included_by_root_creation_order' if selected else exclude.get(r['number'],'not_assessed_after_fixed_cap')),'selection_uses_status_comments_popularity':False,'first_strategy':strat.get(cid,''),'request_type':next((z['request_type'] for z in records if z['case_id']==cid),''),'information_score':next((z['information_score'] for z in records if z['case_id']==cid),''),'original_grade':next((z['original_grade'] for z in records if z['case_id']==cid),''),'exposure':cid in exposure}
  fr.append(rec)
with (P/'frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(fr[0]));w.writeheader();w.writerows(fr)
sources=[]
for r in records:
 sources.append({'source_id':'D-THREAD-'+r['case_id'],'type':'public GitHub issue thread','publisher':'duckdb/duckdb public participants','url':r['root_url'],'version':r['root_created_utc']+' root; current body snapshot '+now,'checked_utc':now,'sections':'root What happens?/To Reproduce/OS/Version/Client; first substantive external reply only at T0','observed':r['goal']+'; '+r['first_response_summary'],'limitations':'원판U/부분Q; 뒤 답과30/90일은 봉인후 열람. 스레드 여러 댓글은1원문. '+r['exposure_note'],'linked_Q_cases':['Q1','Q2','Q3','Q4',r['case_id']],'duplicate_group':'duckdb-issue-'+str(r['issue_number']),'count_minimum':r['sample']=='A','count_group':'A_thread' if r['sample']=='A' else 'B_screen_not_in_minimum','evidence_files':['initial.jsonl#'+r['case_id'],'evidence/first-'+str(r['issue_number'])+'.json']})
with (P/'source-ledger.jsonl').open('w') as f:
 for r in sources:f.write(json.dumps(r,ensure_ascii=False)+'\n')
# Store only bounded first-message excerpts with hashes in commit-ready evidence. Raw remains ignored cache.
for n,cid in mapping.items():
 fp=E/f'first-{n}.json';d=json.loads(fp.read_text())
 if d.get('first_nonself_comment') and 'body' in d['first_nonself_comment']:
  ff=d['first_nonself_comment'];(C/f'first-original-{n}.json').write_text(json.dumps(d,ensure_ascii=False))
  ff['body_sha256']=hashlib.sha256(ff['body'].encode()).hexdigest();ff['body_summary']=firstsum.get(cid,'실질 응답 없음');del ff['body'];d['full_body_storage']='ignored unread_cache, not counted as published evidence';fp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
(P/'.gitignore').write_text('evidence/unread_cache/\n')
print(json.dumps({'A':8,'B_screen':26,'B_question_eligible':[r['case_id'] for r in records if r['b_question_eligible']],'T0_variables':len(rows),'exposure':[r['case_id'] for r in records if r['exposure']],'timestamp':now},ensure_ascii=False))
