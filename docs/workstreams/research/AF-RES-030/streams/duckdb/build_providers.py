"""Ledger for contemporary provider material actually read after T0 seal."""
from pathlib import Path
import json,datetime,hashlib
P=Path(__file__).resolve().parent; C=P/'evidence/unread_cache'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=[]
def add(sid,kind,url,version,sections,observed,limitations,cases,cache,minimum=True):
 rows.append({'source_id':sid,'type':kind,'publisher':'DuckDB project / public maintainers','url':url,'version':version,'checked_utc':now,
  'sections':sections,'observed':observed,'limitations':limitations,'linked_Q_cases':{'questions':['Q6','Q7','Q8'],'cases':cases},
  'duplicate_group':sid,'count_minimum':minimum,'minimum_category':'contemporary_official_provider' if minimum else 'additional_decision_record',
  'artifact_sha256':hashlib.sha256((C/cache).read_bytes()).hexdigest(),'reader':'DuckDB child, source and listed sections directly read; not execution',
  'relation_to_cases':'provider technical support or supplier work, never independent user execution'})
add('DP01','official contemporaneous manual',
 'https://github.com/duckdb/duckdb-web/blob/b0d70dc34c4bbd2685d89ad22b10287f0c217a80/docs/sql/window_functions.md',
 'b0d70dc34c4bbd2685d89ad22b10287f0c217a80; immediately preceding July 2 2024 PR3223',
 ['lines60–74 function table','lines118–134 last/last_value descriptions and aliases','lines195–203 aggregate window shadowing','lines298–311 ordering/frame'],
 '당시 문서는 last와 last_value를 alias로 표시하며 결과가 frame의 마지막 값임을 설명. 기본 frame 종료는 current row. 전체 partition 마지막을 원하면 frame 범위를 명시해야 한다는 제한 기술 명제를 지지.',
 '당시 문서가 오류 없음을 보장하지 않는다. 특정 데이터/peer ties에서 실제 출력을 실행하지 않았다. D08 지원자의 처음 alias 부정 설명과 후속 정정이 상충하며, 문서 PR의 병합 자체는 정답 증명이 아니다.', ['D08'],'v1-windowdoc.txt')
add('DP02','official fix and regression test',
 'https://github.com/duckdb/duckdb/commit/3098c5a5e1c810294bb5b1407420f08ca1a87a94',
 '2024-07-01 commit3098c5; PR12794 merged2024-07-02T09:04:23Z',
 ['extension/icu/icu-dateadd.cpp patch around101','test/sql/function/timestamp/test_icu_dateadd.test added months-before-days cases after503'],
 'months를 days보다 먼저 적용하도록 수정. Kolkata 설정과 양/음 month/day 조합 기대값을 추가. D05 root의 불일치를 공급자가 수정 대상으로 연결했다.',
 'Kolkata는 지원자가 선택한 재현 설정이며 작성자의 직접 답이 아니다. 회귀시험 소스/기대값 열람만 했고 테스트/실사용 실행은 하지 않았다. 질문 필요성이나 질문 효과를 증명하지 않는다.', ['D05'],'p12794-files.json')
add('DP03','official regression test and fixture',
 'https://github.com/duckdb/duckdb/blob/bd98353fbf2356853ad5603c9a9b51f0ea870cb8/test/sql/copy/csv/parallel/test_parallel_csv.test',
 'PR7379 head bd98353fbf2356853ad5603c9a9b51f0ea870cb8; merged2023-05-08T14:22:39Z',
 ['PR7379 files data/csv/null_string.csv full3rows','test_parallel_csv.test null_string tests for parallel true/false and nullstr'],
 '따옴표 속 null 토큰 fixture에 nullstr를 지정하면 SQL NULL을 기대하는 테스트가 있음. 지정하지 않은 테스트는 문자값을 남김. PR 본문은 #6943을 수정 대상으로 명시.',
 '보고 당시0.7.1이 아닌 한 달 뒤 공급자 소스다. 테스트 코드와 기대값이 존재한다는 확인이며 CI 실행/작성자 사용 성공은 미확인. 응답 후 같은 지원자의 권고 변경은 원 스레드에 없다.', ['DB04'],'p7379-files.json')
add('DP04','official implementation at requester exact revision',
 'https://github.com/duckdb/duckdb/blob/3dcba6d0b59d50a5cb23a9878ed2847f654712d4/src/execution/physical_plan/plan_window.cpp',
 'exact requester revision3dcba6d0b59d50a5cb23a9878ed2847f654712d4; 2023-04 root',
 ['lines13–32 streaming eligibility','lines52–107 blocking before streaming scheduling','lines109–123 output column projection'],
 'partition/order가 없는 row_number는 streaming에 들어가고 blocking window가 먼저 계획된다. 따라서 같은 window 연산 묶음 안에 row_number를 덧붙이는 안이 이미 바뀐 행 순서에 번호를 붙일 수 있다는 지원자 우려의 구현 근거다.',
 '코드 판독은 정적 추론이다. 임의 relation 전체에서 원순서 보존/인덱스 접근을 보장하지 않으며 실제 client 변경 실행을 확인하지 않았다. COLUMN 출력 정렬 복원과 ROW 순서 복원을 혼동하면 안 된다.', ['DB07'],'db07-exact-planwindow.txt')
add('DP05','official implementation at requester exact revision',
 'https://github.com/duckdb/duckdb/blob/662041e2b43283bfcfeed984af7c3eaa85fb4996/src/storage/buffer_manager.cpp',
 'requester-linked exact revision662041e2b43283bfcfeed984af7c3eaa85fb4996; Jan2023',
 ['RegisterMemory lines226–235','Pin lines270–299','EvictBlocks lines318–353','SetLimit lines376–395'],
 '메모리 사용량을 먼저 늘린 뒤 한도를 검사하고 eviction queue가 비면 되돌려 실패하는 흐름을 확인. 호출자가 실패를 메모리 예외로 바꾸는 위치도 확인했다.',
 '이 파일 하나로 실제 동시 실행 schedule, 메모리 모델 전체, 모든 query 중단 정책을 증명할 수 없다. 요청자의 장애 회상과 코드 반례를 분리해야 한다. 별도 workload 재현 없음.', ['D02'],'buffer662041.txt')
add('DP06','official scoped fix and tests',
 'https://github.com/duckdb/duckdb/commit/88e217dc5a4ec937cea98779559b6684c150a526',
 '2023-02-09T11:30:18Z commit88e217dc5a4ec937cea98779559b6684c150a526',
 ['column_definition.cpp generated-column exception','check_binder.cpp lambda exception','test/sql/function/list/lambdas/incorrect.test added constraint/generated cases'],
 'lambda를 CHECK/생성열에서 지원하는 대신 명시적 미지원 예외를 던지고 그 오류를 기대하는 회귀시험을 추가했다. 이슈 종료와 최초 기능 목적 달성은 다름.',
 '기능의 훗날 지원 여부 미조사. 작성자의 새 실행/전체 사용 수락 없음. root30 밖 root90 안 공급자 작업이다.', ['D01'],'c88e217.json')
add('DP07','official fix and regression tests',
 'https://github.com/duckdb/duckdb/pull/6039',
 'head43a521fda5269284f7547359496f4dae6bde35b0; merged2023-02-06T11:29:53Z',
 ['PR description','table_function_binder.cpp BindColumnReference patch','test/sql/function/list/lambdas/table_functions.test including issue5821 case'],
 'table function에서 lambda parameter를 상수 이름으로 오해하지 않도록 binding 경로를 추가. 원 이슈를 명시한 로컬 parquet 경로 생성 테스트가 기대 count10을 둔다.',
 '원 예제의 httpfs는 테스트에서 빠져 있어 원 remote URL 전체 경로 검증이 아니다. 공급자 추가 테스트의 소스 읽기이며 작성자 실행이 아니다.', ['D03'],'p6039-files.json')
add('DP08','official contemporaneous decision record',
 'https://github.com/duckdb/duckdb/pull/5869',
 'head492646b9b1ab82c5d677897b214555141847ca92; merged2023-01-12T11:39:52Z',
 ['PR title/body linking5826','head/merge metadata'],
 'ICU의 역방향 필드 연산 패치, 기존 subtraction hack 제거, 양수 interval 적응, 테스트 갱신을 명시. D04와 수정 PR의 같은 사건 연결 확인.',
 '이 PR은 본문/메타데이터만 읽었고 상세 코드와 테스트 출력은 읽거나 실행하지 않았다. 산술 적합성 전부나 원 작성자의 새 실행을 주장하지 않는다.', ['D04'],'p5869.json')
add('DP09','official contemporaneous decision record',
 'https://github.com/duckdb/duckdb/pull/12859',
 'heade6fc5978dfffecc7d1c48937d958225afcf99e6d; merged2024-07-07T11:55:01Z',
 ['PR title/body linking12789','head/merge metadata'],
 'list_zip에 fixed array 자료형을 허용하려는 변경임을 직접 명시하며 D06에 연결됨.',
 '상세 패치/시험 출력은 미열람. 특정 array 조합의 실제 적합이나 작성자의 사용은 확인하지 못함. PR 병합은 공급자의 결과다.', ['D06'],'p12859.json')
add('DP10','official documentation-change decision',
 'https://github.com/duckdb/duckdb-web/pull/3223',
 'head88823a94e07f83c6a50a369254c7cf5480da9325; merged2024-07-02T12:56:13Z',
 ['docs/sql/window_functions.md diff removing first/last rows and alias text','PR timestamps'],
 'D08 첫 지원자 설명을 받은 뒤 first/last alias 항목을 삭제한 실제 문서 변경. 이후 같은 지원자가 기능의 frame 동등성을 인정함.',
 '최초 기술 안내가 틀릴 수 있다는 반례용. 문서 변경이 정확한 최종 정답이라고 사용할 수 없다. DP01과 같은 문서 사건이므로 보수적으로 최소 자료수에는 추가하지 않는다.', ['D08'],'p3223-files.json',False)
add('DP11','official parser implementation inspected as corroboration',
 'https://github.com/duckdb/duckdb/blob/v1.0.0/src/parser/transform/expression/transform_function.cpp',
 'v1.0.0', ['lines33–85 TransformWindowFrame','lines222–235 copied window frame checks'],
 'frame start/end 옵션을 실행 표현 경계에 대응시키는 코드를 읽음. 옵션 해석 경로의 보조 확인이다.',
 '이 파일의 읽은 절만으로 기본 frame mode, alias 동등성 또는 D08 실제 결과 전체를 증명하지 않는다. 최소자료수를 늘리는 근거로 쓰지 않는다.', ['D08'],'v1-transform.txt',False)
add('DP12','official implementation alternative revision',
 'https://github.com/duckdb/duckdb/blob/v0.7.1/src/execution/physical_plan/plan_window.cpp',
 'v0.7.1', ['streaming eligibility and blocking/streaming scheduling sections'],
 '빈 partition/order의 streaming window와 blocking 우선 계획을 읽은 뒤 DB07 exact requester revision을 추가 확인했다.',
 'DP04와 같은 파일의 다른 판이며 별개 최소 원문으로 합산하지 않는다. 최종 기술판정은 exact requester revision DP04를 사용한다.', ['DB07'],'v071-planwindow.txt',False)
rows[-1]['duplicate_group']='DP04'
for row in rows:
 if row['source_id']=='DP02':row['supporting_urls']=['https://github.com/duckdb/duckdb/pull/12794','https://api.github.com/repos/duckdb/duckdb/pulls/12794/files']
 if row['source_id']=='DP03':row['supporting_urls']=['https://github.com/duckdb/duckdb/pull/7379','https://api.github.com/repos/duckdb/duckdb/pulls/7379/files']
(P/'providers.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
print(json.dumps({'read_provider_originals':len(rows),'minimum_contemporary_count':sum(x['count_minimum'] for x in rows)}))
