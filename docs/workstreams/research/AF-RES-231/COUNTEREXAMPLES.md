# 반례 및 정정 — 본표 외, SQL 미실행

## #138641 접근 보정
O00 [현재 질문](https://dba.stackexchange.com/questions/138641/efficiently-get-records-with-latest-timestamp-per-group?noredirect=1), O00R [수정 이력](https://dba.stackexchange.com/posts/138641/revisions). 최초 표시 2016-05-16 15:10, closure 17:49; 그 사이 body 수정 4건, 2020 태그 수정. 표시 시간의 UTC 여부 미확인. 초기 revision source 본문 판독 미확인(F09). 현재 글은 id별 최근 버전의 uuid/data/last_updated를 원하며 UPDATE에는 DISTINCT ON(id), ORDER BY id,last_updated DESC NULLS LAST. uuid는 unique이나 동률 보조키로 사용하라는 계약은 아니다. NULL 배치와 all-NULL 그룹 유지 여부는 별개. UPDATE는 후편집이지 첫 계약의 증거가 아니다. 현재 HTML의 duplicate 대상 제목은 Select ONE most recent post for each author. 현재 표시가 과거 사용자 방문이나 closed_details.original_questions 배열 원순서의 증거는 아니다. 대상 답을 경로 B로 산입하지 않았다. 모집 내 순번/중복 여부 미확인. 이후 이 질문 또는 C01–C07이 표본에 들어오면 이번 사전 노출을 기록하고 새 독립 판독자가 원질문만 읽고 질의를 봉인하도록 권고한다.

## SQL 통제 (P01–P05, PG16 문서 기반, controls.sql)
A=(1,2 같은 최대 timestamp; 3 더 이른 행; 4 NULL), B=(5,6 둘 다 NULL). id는 명시된 고유키. payload는 id마다 다르다. 아래는 **예측**이며 게시자/실행 결과가 아니다.
| 조작 | A의 id 집합 | B의 id 집합 | 반증 조건/해석 |
|---|---|---|---|
| DISTINCT ON(g) ORDER BY g,ts DESC | {4} | {5} 또는 {6} | DESC NULLS FIRST 기본값; 최신 non-NULL 의도와 불일치 |
| DISTINCT ON(g) ... ts DESC NULLS LAST | {1} 또는 {2} | {5} 또는 {6} | 단독 임의 선택; 공동 전체 아님 |
| DISTINCT ON ... ts DESC NULLS LAST,id ASC | {1} | {5} | id 방향은 비즈니스 계약이어야 함 |
| 같은 쿼리 id DESC | {2} | {6} | 순위(단독 한 행) 유지, 내용 변화 |
| ROW_NUMBER() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST) = 1 | {1} 또는 {2} | {5} 또는 {6} | 동률 id 미지정 |
| ROW_NUMBER() ... ,id ASC = 1 | {1} | {5} | deterministic selection; tie contract 미지정이면 조건부 |
| RANK() ... ORDER BY ts DESC NULLS LAST = 1 | {1,2} | {5,6} | B의 all-NULL도 peer; NULL 배제 요구이면 불일치 |
| RANK() ... ORDER BY ts DESC = 1 | {4} | {5,6} | default NULLS FIRST |
| RANK() ... ORDER BY ts DESC NULLS LAST,id ASC = 1 | {1} | {5} | unique id를 peer 정의에 넣으면 공동 1위 사라짐 |
| WHERE ts IS NOT NULL 후 RANK() = 1 | {1,2} | {} | B 그룹 소멸; null-last와 null-exclude의 차이 |
| MAX(ts) join on equality | {1,2} | {} | NULL=NULL은 true 아님 |
| MAX(ts) join on IS NOT DISTINCT FROM | {1,2} | {5,6} | null-safe equality로 B 보존 |
| GROUP BY g, MAX(ts), MIN(payload) | 원행 아닌 조합 가능 | 원행 증명 없음 | A max=2024-02-01, min(payload)=aardvark(id3 과거); 조합이 존재하지 않음 |

id ASC/DESC 통제는 단독 승자 요건만 주어진 경우 두 답 모두 순위 적합, payload 지정된 경우 하나만 내용 적합이다. 계약에 공동 전체가 있으면 둘 다 불일치. outer ORDER BY는 이미 뽑은 행의 표시 순서이지 tie winner 해결이 아니다. PostgreSQL 16 [SELECT](https://www.postgresql.org/docs/16/sql-select.html), [window](https://www.postgresql.org/docs/16/functions-window.html), [sorting](https://www.postgresql.org/docs/16/queries-order.html), [aggregate](https://www.postgresql.org/docs/16/functions-aggregate.html). row_number의 출력이 반복 실행에서 우연히 동일해도 계약상 결정성 증명 아님.

## 실제 게시물의 주장/출력과 한계
- C01 [#266559](https://dba.stackexchange.com/questions/266559/select-distinct-on-ordered-by-another-column): 6행 예의 원하는 출력 2 xyz,1 abc,3 tcs; Erwin 내부 DISTINCT ON(col1) ORDER BY col1,col3 DESC + outer col3 DESC,col2. col3 NOT NULL 전제. 내림차순 전체 출력과 group별 tie 선택을 혼동하면 잘못된 직접 충족이다. 본 예에 동일 timestamp/NULL 검증 없음.
- C02 [#207894](https://dba.stackexchange.com/questions/207894/how-can-i-order-the-results-from-a-distinct-on-query?noredirect=1): cutoff <로 NULL 제외; outer sort_order. NULL 제거는 단순 표시 순서와 다름. 현재 두 태그 조건 미충족.
- C03 [#123065](https://dba.stackexchange.com/questions/123065/get-max-url-from-postgresql-statement/123085): 게시자가 독립 min(url)/max(date)의 문제를 인정하고 ORDER BY date DESC LIMIT 1로 변경. 동일 날짜 임의 선택 댓글. 닫힘 사유 duplicate 아님. max 값과 payload의 원행 결합 오류를 보여 준다.
- C04 [#106795](https://dba.stackexchange.com/questions/106795/remove-duplicate-values-from-query-result/106809): 원하는 first 3 (week에 3/33); DISTINCT ON without ORDER로 둘 중 하나가 가능하다는 답, LATERAL ORDER BY date LIMIT 1 대안. 최신이 아닌 최초라는 반대 방향도 계약 핵심.
- C05 [#51895](https://dba.stackexchange.com/questions/51895/efficient-query-to-get-greatest-value-per-group-from-big-table/330285): 20M행/57그룹 맥락. timestamp scalar/index 최적화가 payload까지 보장하지 않는다. 실제 성능 미검사.
- C06 [#139115](https://dba.stackexchange.com/questions/139115/count-rows-with-max-per-group-and-additional-condition/139164): 게시자 기대 count1, max join과 rank=1 비교, non-NULL 전제. 공동 top이 2개이면 행수와 그룹수 다르며 all-NULL에서도 차이. 원행 요청이 아닌 count 사례.
- C07 [#295760](https://dba.stackexchange.com/questions/295760/joining-only-one-row-of-a-table): 두 child 테이블 최신 derived DISTINCT ON, LEFT JOIN으로 child 없는 parent 보존. ts 동률 id 미지정; full source row와 parent 보존은 서로 다른 계약.

위 보조 7사건 모두 순위/채택 답 선택 규칙의 실험 결과로 사용하지 않는다. 현재 source_tag와 closure만으로 과거 표본 적격성을 보증하지 않는다.

## 공동 순위의 다른 분야
W01 공식 [Tokyo 2021 결과](https://worldathletics.org/competitions/olympic-games/the-xxxii-olympic-games-7132391/results/men/high-jump/final/result): Barshim/Tamberi rank1 2.37m, Nedasekau rank3 역시 2.37m. W02 [공식 보고](https://worldathletics.org/news/preview/tokyo-olympic-games-men-high-jump-report): 둘 모두 2.37까지 무실패, 2.39에서 각각 세 번 실패; jump-off 없이 공동 금. 높이만 MAX/RANK라면 세 사람을 공동 1위로 잘못 포함한다. 규칙의 countback 키는 실제 의미가 있는 비교 키이고 선수 ID는 아니다.
W03 [Paris 2024 공식 보고](https://worldathletics.org/competitions/olympic-games/the-xxxiv-olympic-games-7173263/news/article/paris-2024-olympics-report-men-high-jump): Kerr/McEwen 동일 2.36, 2.38 실패 후 jump-off 진행, Kerr 2.34 성공/McEwen 실패. 이는 기존 키의 임의적인 2차 정렬이 아니라 **새 관측**으로 승자를 선택한 사건이다. Paris 공식 결과표 두 URL 403, 보고만 직접 확인.
W04 공식 TR26.8–26.9 PDF 본문(printed 59–60): 마지막 높이 시도수→총 실패수→공동 순위; 첫 순위 jump-off 또는 포기 결정시 공동. PDF screenshot 실패, 판/시행일 미확인으로 직접 저작 수에서 보수적으로 제외한다. 결론은 스포츠 규칙과 DBA 계약의 형식 차이를 보여주는 반례이지 SQL 사용자에게 공동 1위를 강요하는 근거가 아니다.
