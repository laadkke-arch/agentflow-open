| 원요구 | 보존할 값 | 동결 A·B | 단서의 본문 주소 | 미확인 |
|---|---|---|---|---|
| #11411 v0.9.2 Python: 자동 정수 추론 | 숫자 01→1,12→12; 원문 fips 식별자 폭 보존은 초기 요구 아님 | ignore leading zeros / ignore leading zeros Integer | [O01](https://github.com/duckdb/duckdb/issues/11411) What happens: detect Integer instead | 원본 다운로드 판·행수·원 revision; C01/C04 후속 목적 완화 |
| #11583 v0.10.2-dev504 CLI: 명시한 format에서 자동 DATE | 8개 날짜의 의미, 예 Dec 8, 2022→2022-12-08; 문자 그대로가 아님 | date strings / date strings convert | [O02](https://github.com/duckdb/duckdb/issues/11583) What happens: detect and convert date strings | 동일 환경 독립 실행; 안정판 고정 |
| #15376 1.1.3: 인용된 TSV 식별자 | quoted numeric prefix 및 D1000263 그대로 VARCHAR, 탭 구조 유지; nightly quote 오류 별도 | tab-delimited text file / tab-delimited text file strings | [O03](https://github.com/duckdb/duckdb/issues/15376) What happens: consider them strings | 파일 해시, 실제 schema, 행번호 불일치 |
| #12856 v1.0.1-dev2164: pipe CSV decimal comma | 123,000→123.0 DOUBLE, 2047/2048 data rows 같은 값·형 | number field / number field DOUBLE | [O04](https://github.com/duckdb/duckdb/issues/12856) reproduction §1: number field gets recognized correctly as DOUBLE | 패치/출시판, 독립 실행 |

표 1 단위: 지명 원요구 하나.

| 사건·조건 | 제공자 응답 주소·시각 | 원 1위 | 자기 제외 첫 링크 | 실제 지지 절 | 판정·미확인 |
|---|---|---|---|---|---|
| #11411 A (1) | [GET](https://api.github.com/search/issues?q=ignore%20leading%20zeros%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:29.146Z; [raw](receipts/01-11411-A.json); total=1, incomplete=false | [#11411](https://github.com/duckdb/duckdb/issues/11411) (자기) | 없음 (정상 배열의 자기만) | C03 수동 타입·C04 수용, 자동 해결 없음 | raw 1, external 0; 외부 관측 0 |
| #11411 B (2) | [GET](https://api.github.com/search/issues?q=ignore%20leading%20zeros%20Integer%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:29.582Z; [raw](receipts/02-11411-B.json); total=1, incomplete=false | [#11411](https://github.com/duckdb/duckdb/issues/11411) (자기) | 없음 (정상 배열의 자기만) | 동일 C03/C04 | raw 1, external 0; 외부 관측 0 |
| #11583 B (3) | [GET](https://api.github.com/search/issues?q=date%20strings%20convert%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:30.171Z; [raw](receipts/03-11583-B.json); total=4, incomplete=false | [#15376](https://github.com/duckdb/duckdb/issues/15376) | [#15376](https://github.com/duckdb/duckdb/issues/15376) raw 1 | O03/C08 TSV BIGINT→VARCHAR, 날짜 변환과 반대 | raw 0, external 0; 본문 판독 무관련 |
| #11583 A (4) | [GET](https://api.github.com/search/issues?q=date%20strings%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:30.689Z; [raw](receipts/04-11583-A.json); total=16, incomplete=false | [#14004](https://github.com/duckdb/duckdb/issues/14004) | [#14004](https://github.com/duckdb/duckdb/issues/14004) raw 1 | X01/C10 JSON timestamp format, 다른 형/입력 | raw 0, external 0; 본문 판독 무관련 |
| #15376 A (5) | [GET](https://api.github.com/search/issues?q=tab-delimited%20text%20file%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:31.139Z; [raw](receipts/05-15376-A.json); total=1, incomplete=false | [#15376](https://github.com/duckdb/duckdb/issues/15376) (자기) | 없음 (정상 배열의 자기만) | O03/C07/C08 full sample 성공 보고·문서 의도; schema 미인쇄 | raw 1, external 0; 전체 schema 미확인 |
| #15376 B (6) | [GET](https://api.github.com/search/issues?q=tab-delimited%20text%20file%20strings%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:31.566Z; [raw](receipts/06-15376-B.json); total=1, incomplete=false | [#15376](https://github.com/duckdb/duckdb/issues/15376) (자기) | 없음 (정상 배열의 자기만) | 동일 O03/C07/C08 | raw 1, external 0; 전체 schema 미확인 |
| #12856 B (7) | [GET](https://api.github.com/search/issues?q=number%20field%20DOUBLE%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:32.171Z; [raw](receipts/07-12856-B.json); total=3, incomplete=false | [#12856](https://github.com/duckdb/duckdb/issues/12856) (자기) | [#12384](https://github.com/duckdb/duckdb/issues/12384) raw 2 | O04/C09 정확 재현 보고만; X02 Arrow view filter unrelated | raw 1, external 0; 정확 재현만, 해법 미확인 |
| #12856 A (8) | [GET](https://api.github.com/search/issues?q=number%20field%20repo%3Aduckdb%2Fduckdb%20is%3Aissue%20in%3Atitle%2Cbody%20created%3A%3C2025-01-01&per_page=5&page=1) 2026-11-24T22:11:32.719Z; [raw](receipts/08-12856-A.json); total=24, incomplete=false | [#14487](https://github.com/duckdb/duckdb/issues/14487) | [#14487](https://github.com/duckdb/duckdb/issues/14487) raw 1 | X03 JSON profiling key, 무관련 | raw 0, external 0; 본문 판독 무관련 |


표 2 단위: 개별 GET 한 건. 8개 정상 응답, 실제 위치 21, 정상적으로 비어 있는 위치 19, 미관측 0. 위 표의 raw=0/1/2는 첫 링크의 목적 적합성 등급이고 external은 자기 제외 동일 척도; 순위와 혼동하지 않는다. 0은 읽어서 무관련으로 확인했거나 정상적인 후보 부재인 경우이며 경로 상태는 paths.csv에 구별했다.

## Q1–Q7 — 답, 원자료 위치, 오판 가능성

**Q1.** O01–04 body와 판·fixture를 검색 전에 SCOPE에 동결했다. #11411과 #12856은 정수/실수 변환, #11583은 DATE 변환, #15376은 문자열 유지. #11411의 0 보존 추측은 원뜻과 충돌한다. C01/C04 후속 발언은 명시 타입 수용까지 보여주나 원래 자동 추론 목적을 소급 변경하지 않는다. O03의 원본 파일 SHA와 초기 편집 revision, O01 전체 행수는 미확인. G02 REST current body와 timeline은 revision의 전체 이력은 아니다.

**Q2.** queries.csv 8행, 사전 동결 ac14b425d6bda727bdc24606321b1798f0a0a56c. A 2–4 토큰, B=A+본문 목적 1단어(Integer, convert, strings, DOUBLE). 제목 전체, 이슈 ID, 링크, 해법 옵션명을 넣지 않았다. AB/BA/AB/BA. 네 모두 적격으로 두되 #11411 A 자체에 ignore라는 방향이 있어 추가 정보량이 작은 사례, #12856 A가 매우 넓은 사례라는 한계가 있다. 발표자/판독자는 지명 ID와 현재 body에 노출; 댓글·결과는 사전 동결 후 열었다. 가림 없는 표본.

**Q3.** receipts/INDEX.json 및 8개 원응답 JSON. 실제 GitHub REST /search/issues, 동일 공개 대상·연결, repo:duckdb/duckdb is:issue in:title,body created:<2025-01-01, per_page=5, page=1, sort/order 생략. 2026-11-24 UTC 22:11:28.591–22:11:32.719, 개별 8회. total_count 순서 1,1,4,16,1,1,3,24; incomplete_results 8건 false. score 모두 1이지만 배열 순서를 그대로 보존했다. 제공자 원응답은 확인했으나 connector가 HTTP 버전 헤더/API version 선택값을 내주지 않아 같은 버전이라는 요구는 검증 불가. 209의 웹 도구 배열을 대신 사용하지 않았다. API 검색의 현재 인덱스·수정된 이슈 본문이므로 2024년 당시 검색을 재현한 것은 아니다.

**Q4.** paths.csv 40 예정 행. 21 observed_item, 19 observed_no_item, 미관측 0. 자기 번호 포함 7/8, 자기 원1위 5/8, 외부 첫 후보 있음 4/8, 자기만 있는 정상 배열 4/8, raw 빈 배열 0/8. #11583 B 자기 raw2, A raw5. #12856 B 외부 첫 raw2. 나머지 외부 후보 있는 조건은 raw1. G04와 DUPLICATE_SCREEN: 반환된 서로 다른 16 이슈의 timeline을 확인해 대상과 동일 사건이라고 명시된 유지자 duplicate를 발견하지 못했다. #5782는 반대 목적의 선행 사건이며 중복 아님. 단순 유사 표현은 배제 근거가 아니다. 하위 순위 본문 전수 판독이나 모든 시점의 삭제된 댓글까지 증명하지 않는다.

**Q5.** 7개 서로 다른 첫 도착 이슈(자기 포함/제외 합집합) 본문·댓글 확인; 추가 링크 사용 0/허용 최대1, 양 조건 동일. #11411 C03 명시 타입 조언, C04 수용은 실제 자동 탐지 해법이 아니다. #15376 O03/C08 full sample 권고·신고자 성공은 부분 근거이며 동일 TSV의 최종 VARCHAR schema가 미인쇄, C07 LIMIT100과 CTAS 다름. #12856 O04/C09 정확한 재현 보고만으로 관련성 점수1, 실제 해법 점수0; 외부 X02/X03은 Arrow와 JSON profile 문제. #11583 A X01/C10 JSON timestamp/혼재 fraction, B O03/C08 TSV ID 보존은 요구와 다르다. C06의 같은 작성자 v1.0.1-dev4803 성공은 원이슈의 후속 근거지만 두 조건 첫 답이 아니라 점수에 반영하지 않았다. C16 commit 자체도 날짜 수정의 패치는 아니었다. 보조 자료와 실제 도착을 구별한다.

**Q6.** COUNTEREXAMPLES.md. C12/C13의 #5782·PR5850은 09001→9001 손실 방지와 명시 cast 9001 허용이라는 경쟁 목표를 같은 구현에서 확인한다. P02/P03의 FIPS 2자리 표현, P04의 특허 prefix/폭 및 P05의 patent_id varchar(20) vs patent_date date/num_claims int(11)에서는 문자 보존·수치 변환을 열마다 결정해야 한다. M01의 인용 문법은 타입 규약이 아니다. M02/M06의 20480 표본, -1 전체 및 2048 chunk는 각기 다른 단위다. #12856의 2047/2048 경계 원인을 chunk라고 단정 못한다. M03 현재 delim·decimal_separator·thousands·types, C17 이후 천 단위 사례가 보여주는 서로 다른 수치 문법; M04 dateformat과 M05 cast 정밀도. 현재 2.0 문서는 과거판 수정 증명이 아니고 P05의 snapshot도 원래 TSV와 같다는 보장 없다. C08 첫 비수치 행 주장과 O03 두 오류 행 불일치도 보존했다.

**Q7.** 손계수: #11411 [1,1]→[0,0], #11583 [0,0]→[0,0], #15376 [1,1]→[0,0], #12856 [0,1]→[0,0] (괄호 안은 A,B; 화살표는 자기 포함→제외). 부분 관련성까지 허용한 원1위에서 개선1/동률3/악화0/판정불가0, 외부 첫 링크에서는 개선0/동률4/악화0/판정불가0. 양쪽 각각 예정/관측 4쌍/4쌍. #12856의 1은 정확 재현에 한정한 부분 관련성이다. 사전 규칙의 'concrete workaround'를 좁게 적용하여 재현만 U로 판단하면 자기 포함 개선0/동률3/악화0/판정불가1; 재현을 무해법 0으로 보면 동률4. 해법만 요구한 이진 지표(등급2만 성공)에서 양쪽 모두 성공 0, 개선0/동률4/악화0/판정불가0. 성공 없음은 실행 실패라는 뜻이 아니라 읽은 첫 답이 입증하지 못했다는 뜻이다. #15376 출력 schema가 입증되면 A/B 양쪽이 동시에 2가 될 수 있어 쌍 차이는 여전히 0. #11583 자기 위치 변화는 별도 지표이지 첫 링크 개선이 아니다. pairs.csv의 주판정과 민감도를 함께 사용한다.

## 조건부 추천과 비용

결론: **이 표본에서는 목적 한 단어를 추가해도 외부 첫 답의 개선은 관찰되지 않았다.** 단, 목적을 무시해도 된다는 증거는 아니다. 오히려 발행자 식별자 보존과 소비자 정수 변환의 양극이 있어 의미론적 구분은 필요하다. 이 실험은 단일 제공자의 제한된 repo/날짜/5자리/한 토큰 추가에 관한 것이고, 넓은 웹 순위나 다른 쿼리 형식으로 일반화하지 않는다.

- 입력 계약 후보: 원값(lexeme), 원하는 결과형, 입력 문법(delim, quote, decimal, date format), 목적(preserve/convert), 적용 버전, 표본 범위를 분리. 보존할 것은 데이터 값인지 표현인지 코드폭인지 먼저 확인. 미기재 목적은 추정이라고 표시.
- retrieval 후보 A 단독(1 요청), B 단독(1 요청), A/B 둘 다(2 요청)와 자기 제외를 별도 탭으로 보여주는 방법; union은 새 실험 없이 품질 향상 단정 금지. A/B union·rerank는 별도 비용/검증 필요. 첫 답이 자기일 때는 '원사건 해결 추적'과 '새 사례'를 분리. 양쪽 빈 결과는 확대 검색을 요청하거나 부족하다고 표시.
- 출력 후보: 원문 증상·조작·적용판·결과형·제약 근거를 각각 링크. #11411의 prior art는 검색 첫 결과에 없었으나 방향 충돌 설명에 유용한 수동 발견이다. 자동 추론, 명시 스키마, 후처리 cast를 같은 '해결'로 병합하지 않는다.
- 근거 수: 원장 42행 중 직접 산입 39 독립 work_id, 18 계보, 미산입 3(메타데이터 중복 1, 실패2). O4/G4/소비자·패치·댓글 C17+X3=20/M6/P5. 동일 사건 댓글/패치는 독립 사건 수 아님. 지명 사건4, 첫 도착 고유 이슈7(지명4와 외부3의 합집합), 보조 사건까지 원장 event 계보 10. P05 PDF는 본문 추출 직접 읽음, 페이지 이미지 실패; 보수적으로 제외해도 38, P4로 하한 충족. 모든 8 GET 영수증은 자료 수 제외. 원문 22 하한 및 분류별 충족. 새 프로그램 실행/설치, 데이터셋 전체 다운로드, 독립 재현·검토 없음.
- 상태 PARTIAL: 원응답 및 순위/두 분모 비교는 완수, 자료 하한 충족. API 버전 헤더 및 공개 편집 revision 전수 복구 미확인, 정확한 데이터 파일/역사판 실행 미확인, #12856 실제 fix 미확인. 현재 지명 원문 기준 관련성 관측은 유효하나 엄격한 API 버전 및 완전한 원요구 동결/해법 판정 보증은 못 한다. 별도 실험과 원자료 재확인에 넘긴다.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 특정 자료·검사 | 판정이 뒤집힐 관측 |
|---|---|---|---|
| 자기 이슈 exact reproduction만 점수1; #12856 C09 수정/조작 없음 | 포함 개선1은 해법 개선 아님 | #12856 closed timeline 및 연결 fix commit, 원판 fixture 2047/2048; C17은 별도 문법 | 원판에 맞는 실제 DOUBLE 자동 처리 조작/패치가 당시 첫 답 안에서 확인되면 strict 개선, 재현만 제외하면 동률 또는 U |
| O03 8,123,649행 D1000263 vs C08 2,156,093행 주장/nightly 인용 오류, full scan schema 없음 | #15376 partial, 전체 표본과 명시 VARCHAR 추천 조건 | 동일 파일 SHA·판 확보, CTAS와 DESCRIBE, quoted-only numeric 대조; P05 historical dictionary | -1 결과도 BIGINT/오류이면 전체 표본 권고 취소, 실제 VARCHAR와 보존 확인이면 양쪽 2 |
| 공개 revision/API 버전 미관측, 비가림 4사건·all score1; #11583 A/B 첫 답 모두 오답 | 목적 토큰 효과의 범위·재현성 | GitHub API version/header 영수증 별도 재실험, issue edit history, 고정 queries.csv 순서, C06 날짜 고정판 확인 | 명시 버전 반복에서 첫 외부 적합 답 또는 원요구 revision 변화가 관찰되면 효과/적격성 재평가; 과거 원순위 대체 금지 |
