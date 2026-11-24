| 원질문·판 | 동률·NULL 계약 | 경로 A·도착 답 | 경로 B·도착 답 | 두 답의 실제 지지 절 | 판정·미확인 |
|---|---|---|---|---|---|
| 예정 사건 1 — 미배정 | 미확인 | 미확인 (질의 미봉인) | 미확인 (raw duplicate 미확보) | 미확인 | PARTIAL; 비교 불가 |
| 예정 사건 2 — 미배정 | 미확인 | 미확인 (질의 미봉인) | 미확인 (raw duplicate 미확보) | 미확인 | PARTIAL; 비교 불가 |
| 예정 사건 3 — 미배정 | 미확인 | 미확인 (질의 미봉인) | 미확인 (raw duplicate 미확보) | 미확인 | PARTIAL; 비교 불가 |
| 예정 사건 4 — 미배정 | 미확인 | 미확인 (질의 미봉인) | 미확인 (raw duplicate 미확보) | 미확인 | PARTIAL; 비교 불가 |

단위: 예정 원질문 1건 × 양 경로. 원표본 미확보로 4건 모두 미배정. #138641은 보정용이며 본표에 넣지 않는다.

| 사건·경로 | 공개 응답·UTC | 원위치·제외 이유 | 질문·답 열람 수 | 충족·누락·공석 |
|---|---|---|---|---|
| 1-A | 미확인; frame 접근 실패 F03 | 원질문 미배정; 검색 미실행 | 0·0 (미실시) | 공석; 미확인 |
| 1-B | 미확인; frame 접근 실패 F03 | 원질문 미배정; 대상 배열 미확보 | 0·0 (미실시) | 공석; 미확인 |
| 2-A | 미확인; frame 접근 실패 F03 | 원질문 미배정; 검색 미실행 | 0·0 (미실시) | 공석; 미확인 |
| 2-B | 미확인; frame 접근 실패 F03 | 원질문 미배정; 대상 배열 미확보 | 0·0 (미실시) | 공석; 미확인 |
| 3-A | 미확인; frame 접근 실패 F03 | 원질문 미배정; 검색 미실행 | 0·0 (미실시) | 공석; 미확인 |
| 3-B | 미확인; frame 접근 실패 F03 | 원질문 미배정; 대상 배열 미확보 | 0·0 (미실시) | 공석; 미확인 |
| 4-A | 미확인; frame 접근 실패 F03 | 원질문 미배정; 검색 미실행 | 0·0 (미실시) | 공석; 미확인 |
| 4-B | 미확인; frame 접근 실패 F03 | 원질문 미배정; 대상 배열 미확보 | 0·0 (미실시) | 공석; 미확인 |

단위: 예정 사건×경로 1회. 8자리 중 실제 방문 0, 결측 8; 두 경로 관측 가능한 쌍 0/4. 이 값은 접근/실시 수이며 관련성 점수나 정상 빈 응답 수가 아니다. 수렴 수·개선 수는 미확인.

## Q1. 모집과 판 구분 — 미확인
[S06 /questions](https://api.stackexchange.com/docs/questions)의 Discussion은 다중 tagged AND, creation 정렬을 설명한다. [S01 /search/advanced](https://api.stackexchange.com/docs/advanced-search)는 다중 태그 OR다. 초기 SCOPE의 advanced 모집은 이 반증으로 폐기했고 실제 원질문·답을 열기 전 8d068e444012d4e6adb6ba5052c8f30cfdcb8af4에서 정정했다. [S08 paging](https://api.stackexchange.com/docs/paging)에 따라 page 1=100, page 2의 처음 20까지, 동률 경계는 같은 시각 전체를 읽고 ID 오름차순. 고정 site=dba, tagged=postgresql;greatest-n-per-group, UTC 1325376000–1735689599 inclusive, sort=creation, order=asc. raw와 정규화 위치 분리. 그러나 F01–F04 실패: 실제 items/has_more/creation_date/closed_reason 없음. 실제 분모, 적격/제외 수 모두 미확인. 표본 네 자리 공석은 적격 질문 0이라는 의미가 아니다. frame.csv는 표집 슬롯 및 접근 보정 기록만 보존.

O00 [#138641 현재](https://dba.stackexchange.com/questions/138641/efficiently-get-records-with-latest-timestamp-per-group?noredirect=1)와 O00R [revisions](https://dba.stackexchange.com/posts/138641/revisions)에서 2016-05-16 15:10 최초 게시, 이후 body 수정들, 17:49 duplicate closure, 2020 tag edit의 표시 이력을 확인했다. UTC 여부 및 초기 body 전문은 미확인(F09), current body의 UPDATE는 최초 요구로 소급하지 않는다. [S03 revision API](https://api.stackexchange.com/docs/revisions-by-ids), [S12 revision type](https://api.stackexchange.com/docs/types/revision)으로 원문을 재확보할 수 있는 입력을 제시하되 성공 주장하지 않는다. 이 보정 질문의 표본 내 위치/중복 여부도 미확인.

## Q2. 원계약과 질의 — 본표 미확인
원표본 4건이 없으므로 각 그룹 키·날짜·NULL·보조키·필요 열과 A의 2–4 단어를 봉인하지 못했다. 임의 질의 또는 보조 질문으로 채우지 않았다. #138641 current body만 보면 id 그룹, last_updated timestamp, uuid unique, data payload, 지정된 두 id의 최신 버전. timestamp 동률과 all-NULL 그룹 계약 미명시, uuid가 고유하다는 사실은 선택 기준이 아님. current UPDATE의 ORDER BY id,last_updated DESC NULLS LAST는 작성자 후편집의 접근 방식이지 최초 동률 의도 증거가 아님. 유일 결정 승자, 공동 최고 전체, 임의 1행 중 가능한 계약을 남겨야 한다. 보정 질문 및 C01–C07 열람이 이미 있었으므로 이후 표본과 겹치면 비가림 노출을 기록하고 별도 독립 판독자가 원문만으로 질의를 봉인하는 것이 필요하다.

## Q3. A/B 동등한 출발과 예산 — 설계만
[S01](https://api.stackexchange.com/docs/advanced-search), [S02 closed_details](https://api.stackexchange.com/docs/types/closed-details), [S09 original_question](https://api.stackexchange.com/docs/types/original-question), [S04 create-filter](https://api.stackexchange.com/docs/create-filter), [S07 filters](https://api.stackexchange.com/docs/filters). original_questions는 복수 필드, 원소 type은 original_question. withbody만으로 필요한 closed_details가 제공된다고 가정하지 않는다. 명시 필터 생성 및 included_fields 영수증 필요. 시도는 웹 접근 불가/컨테이너 DNS code6(HTTP000). 필터 token 미확보, 실제 API wrapper/array 없음. A는 원표현 동결 이후 relevance top5에서 자기 제외 첫 질문. advanced OR이므로 원 raw top5와 두 태그를 동시에 충족하는 부분수열의 첫 5를 별도로 보존하는 보정은 SCOPE에 선등록했다. 이는 서버 AND relevance가 아니며 페이지 추가 비용/랭킹 변화 민감도 및 strict 비교 미충족을 별도 표시한다. B는 closed_details.original_questions 배열의 첫 원소; 보정 사례 HTML duplicate label은 원배열 순서·당시 경로의 증거가 아니다. [S13 DBA duplicate 도움말](https://dba.stackexchange.com/help/duplicates)과 S14 유사 사이트 템플릿은 편집자의 정책 목적이 사용자 실제 이동과 다름을 보여준다. A/B 질문 1+답 1의 동일 본문 예산 및 AB/BA 교대는 예정; 관측 0. 실제 네트워크 메타데이터 호출도 추후 따로 집계.

## Q4. 도착 답 선택 — 미확인
[S05 question](https://api.stackexchange.com/docs/types/question), [S10 answers on questions](https://api.stackexchange.com/docs/answers-on-questions), [S11 answer](https://api.stackexchange.com/docs/types/answer): accepted_answer_id 우선, 없으면 score DESC, creation_date ASC, answer_id ASC로 메타데이터에서 정렬 후 한 답 본문만 읽는다. API가 동일 득표 2차 순서를 보장하지 않으므로 로컬 정렬과 raw 위치를 모두 기록. 답 선택/SQL 절은 본표 0/8 관측. 정상 빈 응답은 하나도 입증되지 않았고, 자기 제외·동일 재게재·수렴 발생 횟수는 모두 미확인. #138641에 보이는 duplicate 제목을 B 답으로 간주하지 않았다. 보조 C01–C07은 별도 방문, score 표에서 제외한다.

## Q5. 동률·NULL·결정성 — 원문 기반 예측; 실행 및 본표 답 미확인
[P01 SELECT](https://www.postgresql.org/docs/16/sql-select.html) DISTINCT Clause/ORDER BY Clause, [P02 window](https://www.postgresql.org/docs/16/functions-window.html) 9.22 ranking functions, [P03 sorting](https://www.postgresql.org/docs/16/queries-order.html) 7.5, [P04 tutorial](https://www.postgresql.org/docs/16/tutorial-window.html) 3.5 예제, [P05 aggregate](https://www.postgresql.org/docs/16/functions-aggregate.html) max. DISTINCT ON은 group 내 첫 행을 선택하며 정렬키가 동률이면 내용 결정성 미보장. row_number는 행별 번호, rank는 ORDER BY 키 전부가 동일한 peers; unique id를 rank 키에 추가하면 공동 승자 의미가 달라진다. DESC 기본 NULLS FIRST. MAX는 NULL 무시, 원행 전체 아님. control_predictions.csv와 controls.sql에 2그룹 6행, 동일 최대 timestamp 두 행, NULL 및 all-NULL 그룹의 13개 통제를 분리했다. A의 ts 최신 동률 id1/2, B의 ts 모두 NULL id5/6. NULLS LAST + id ASC는 A1/B5, DESC는 A2/B6; rank(ts DESC NULLS LAST)는 A1/A2/B5/B6; NULL 제외 시 B 소멸. MAX equality join과 null-safe join도 다르다. payload의 min과 ts의 max 독립 결합은 실제 원행이 아닐 수 있다. 이는 문서상 예측이며 실행 관측 없음.

실제 게시물에서는 [C01](https://dba.stackexchange.com/questions/266559/select-distinct-on-ordered-by-another-column) 6행/3그룹 출력 및 내부 DISTINCT ON, 외부 sort, col3 NOT NULL 조건; [C03](https://dba.stackexchange.com/questions/123065/get-max-url-from-postgresql-statement/123085) 게시자 min(url)/max(date) 결합 문제 인정과 LIMIT 1 변경, 동률 임의 댓글; [C06](https://dba.stackexchange.com/questions/139115/count-rows-with-max-per-group-and-additional-condition/139164) expected count1과 rank/max join, NOT NULL 전제; C02/C04/C05/C07의 날짜 cutoff, earliest, scalar timestamp, left join 보존 사례. 실제 작성자가 제시한 입력/기대/SELECT와 연구자 통제 예측을 COUNTEREXAMPLES.md에서 구별했다. 어느 것도 이번 본표 답의 결과가 아니다. PG 16.0 실행은 미실시, 실제 판 확인과 정상 진입점은 HANDOFF에 남긴다.

## Q6. 공동 우승과 jump-off — 독립 경기 두 건
[W01 Tokyo 공식 결과](https://worldathletics.org/competitions/olympic-games/the-xxxii-olympic-games-7132391/results/men/high-jump/final/result) men high jump final: Barshim/Tamberi 공동 1위 2.37m, Nedasekau 3위 역시 2.37m. [W02 공식 보고](https://worldathletics.org/news/preview/tokyo-olympic-games-men-high-jump-report): 공동 1위 선수들은 2.37까지 무실패, 2.39에서 각각 세 번 실패, jump-off 포기. raw height만 비교하면 3명이 공동 최고로 잘못 포함될 수 있다. [W03 Paris 공식 보고](https://worldathletics.org/competitions/olympic-games/the-xxxiv-olympic-games-7173263/news/article/paris-2024-olympics-report-men-high-jump): Kerr/McEwen 2.36m와 동일 기록, 2.38 실패 후 jump-off, Kerr 2.34 성공/McEwen 실패. 추가 관측이지 arbitrary secondary id가 아니다. Paris raw 결과표는 403(F06/F07), W03 공식 보고만 직접 성공. [W04 TR26.8/26.9 PDF](https://worldathletics.org/download/download?filename=9b6dd391-ea84-4bc5-b7d1-4cec3587cb05.pdf&urlslug=C1.1+%26+C2.1+-+Competition+Rules+%26+Technical+Rules) printed 59–60의 countback 및 jump-off 규칙 텍스트는 확인했으나 screenshot 403과 판·시행일 미확인으로 성공 저작 수에서 제외. 공식 결과/보고 3편, 독립 경기 2개, 규칙 텍스트 별도. 과거 각 경기의 동일 규칙 판 적용은 추가 검증 필요. 공동 순위의 의미를 DB 원질문에서 먼저 확정해야 하며 스포츠 규칙을 기계적으로 대입하지 않는다.

## Q7. 어떤 링크를 남길까 — 조건부 설계; 효과 미판정
comparison.md는 자기 제외·동일 목적지/동일 답·재게재·채택 표시·동률 계약 누락·NULL 정책·원격 실패를 서로 다른 필드로 제안한다. 원작성자의 요구, 중복 표시에 대한 편집자 판단, DB 사용자의 실행 요구는 독립이다. 동일 도착은 두 경로를 보존하되 근거 중복 산입하지 않는다. 개선 판단은 본표 4쌍 중 실제 관측 0쌍이므로 비교 분모 0; 개선/동률/악화/수렴은 미확인(0으로 채우지 않음). 자기 제외 효과 AF-RES-220의 관측을 이번 연구 결과로 옮기지 않는다. 보조키 방향 반전으로 순위(각 그룹 단독 1행) 적합성 유지와 내용(id/payload) 적합성 변화가 발생하는 통제는 Q5와 COUNTEREXAMPLES.md의 D2/D3; 공동 1위 전체 계약에서는 둘 다 불일치. 사용자가 보조키를 요구하지 않았다면 조건부 표시. tie 미지정일 때 허용 결과와 계약별 민감도 병기.

## 자료 수·비용·대안
- sources.jsonl 41행: 직접 열람 별도 페이지/스레드 기준 산입 29 work_id, 13 계보(동일 저작 다른 형식 제외). 성공 산입 구성은 SE 공식 13, PostgreSQL 16 제작자 문서 5, 보정 질문 1, 보조 공개 스레드 7, 공식 스포츠 결과/보고 3. 매뉴얼/API reference 전체를 각각 하나의 저작으로 보는 더 엄격한 기준에서는 13 계보만을 별도로 제시하며 최소 22 독립 저작 충족을 주장하지 않는다. 미산입 12행: 동일 도움말 1, 수정이력 동일 질문 1, 스포츠 규칙 PDF 보수적 제외 1, 접근/판독 실패 9. 각 출처 개별 UTC는 재구성하지 못해 실제 시간창을 기록.
- 독립 사건: 본표 0/4, 보정 1, 보조 DBA 7, 스포츠 2 (본표 외 10). 관측 모집 분모 미확인/상한120; 예정 답 경로8/관측0/결측8. 보강 질문 4건의 필수 분류는 미충족. 보조 DBA 7건 및 스포츠 3문서는 해당 범주의 보강일 뿐. PG manual 5절의 근거는 확인했으나 공식 회귀 실행/판 고정 관측 아님. 자료 수로 핵심 측정의 결손을 가리지 않는다.
- 현재 표집 API 원응답과 선택 filter 미확보로 PARTIAL. 웹 실패를 정상 빈 목록으로 대체하지 않았다. 향후 실제 frame API와 원문 동결을 먼저 하고 A/B 원배열 및 선택 답을 확보. metadata pagination 비용은 별도 기록. A의 OR 후처리는 사용자 지정 동일 태그 서버 relevance를 대체하지 못하므로 엄격 판정은 별도 유지.
- 자체 문서/분모 대조는 수행; 독립 재검토와 PostgreSQL 실행은 미실시. 보강에서 본 결론이 틀릴 수 있는 조건은 C03/C04/C06, W01/W03 및 SQL D2/D3에 명시했다.

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 구체적 자료·검사 | 판정이 바뀌는 관측 |
|---|---|---|---|
| 필터 생성 및 /questions frame DNS/웹 실패, 원표본 미배정 | Q1–Q4, Q7 모든 A/B 효과와 실제 분모 | 지정 API v2.3 필터 생성/포함 필드 원응답 및 AND /questions page1–2, 동률 경계와 revision; 본문만으로 선봉인 | 실제 적격 4자리와 원응답 확보; 이후 양쪽 답 관측 쌍에 한해 개선/동률/악화 분모 생김 |
| advanced tagged OR; 현재 duplicate 표시와 과거 이동/원배열 불일치 가능; 보조 노출 | Q3 동등한 출발, Q7 수렴/선택의 해석 | raw relevance 5와 AND 부분수열·추가 페이지 비용, closed_details 배열 원순서 및 revision; 별도 독립 판독자 | 동일 조건에서 첫 비자기 후보가 바뀌거나 duplicate target이 다른 계약/자기/같은 목적지인 관측이 B 우위 가설을 뒤집음 |
| 동률·NULL 미명시, 답의 정렬/원행과 경기 규칙 판 미검증; SQL 미실행 | Q5–Q7 직접 충족 vs 조건부/불일치, 단독/공동 승자 의미 | PostgreSQL 16.0 controls.sql 실행과 각 실측 도착 SELECT 동일 fixture; Paris 공식 raw 결과 및 해당 당시 TR26 판 | 보조키 변경시 payload가 달라짐, all-NULL 그룹 유지/소멸, 공동 최고 반환 또는 단독 승자 요구 위배가 실제 계약별 점수를 바꿈 |
