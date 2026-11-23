| 연구군·층 | 과제·배정 단위 | 링크·설명의 차이 | 배정 인원·시행 | 시간 시작·종료·단위 | 품질 기준 | 원자료 URL·파일·키 | 연결된 행/대상 행 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 NCQ · software-primary · J-NA-01/02/03 | 다섯 Node.js 과제 중 사람마다 서로 다른 두 과제. 두 별도 코호트 모두 baseline 먼저, NCQ 나중. 과제 조합을 균형 배치했지만 조건 순서는 고정 | 실험1은 같은 REPL의 검색 off/on. 실험2는 VSCode+웹 대 NCQ 전체(검색·후보·순위·수정·실행 환경). 같은 링크의 설명만 바꾸지 않음 | 분석 대상 각 실험 10명×2시행=20시행. 실험2 모집 계보에는 예약14명, 성공 세션10명, 세션 중 철회4명; 철회자의 과제·조건은 미확인 | 시작→첫/최종 package install, 시작→명세 충족까지 경과 초. 훈련 약10분·각 과제20분은 계획값이며 강제 제한은 미확인 | 실행되고 과제 명세를 충족하는 JS 결과물. snippet `Runs?` 및 lint는 최종 과제 점수와 다름 | [고정 repo](https://github.com/Brittany-Reid/node_code_query/tree/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study), `codesnippets1.csv`/`2.csv`, `P,T,Package,Snippet,Used?,Runs?,Error` | 관측 snippet 142/156행→각20개 `(P,T)` 그룹; 배정×시간×최종품질 join은 **미확인**/대상 각20시행 | T→조건·문제·period 코드북, 시각 로그, 최종 제출/검사표, 철회자 ledger. 공개 두 CSV는 총시간 원행이 아님 |
| S02 eXoaDocs · software-primary · J-NA-04 | Java SQL 네 순차 과제, Java 숙련도 네 층 안 독립군 무작위 배정 | JavaDocs 대 채굴 예제·요약·선정·인기도 표시를 추가한 문서. 대조문서에도 일부 수작업 예제 존재 | 24명, 조건별12명. 설계상96개 사람×과제 슬롯이며 원행96개를 관측한 것은 아님 | 다음 관련 문서를 30초 초과 열람한 시각으로 과제 전환 추론; 누적 분:초. 과제3/4는 문서가 같아 시간 분리 불가. 전체40분 제한 | 제출 코드의 테이블·두 tuple·출력 검사 pass/fail. Table X 시간과 XII 통과 수 사이 개인키 없음 | [원논문](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §5, Tables X/XII; 저자 사이트·DOI·프로젝트·GitHub/Zenodo/OSF·보관본까지 추적했으나 keyed data 미발견 | 시간×품질 join **미확인**/설계상96슬롯. Table X의 완료자 분모도 미확인 | 사람·배정층·시간포함·정답·오답·미제출·timeout 구분키, 정확한 제출 시각, 활동시간, 추적 재작업 |

| 연구·비교 조건 | 비교 가능 단위·분모 | 선택시간 | 총 과제시간 | 활동시간 | 품질·실패·제한시간 | 추정치·불확실성 또는 미산출 이유 | 반증·근거 주소 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O-NA-01 · NCQ 실험2 VSCode+웹→NCQ · 저자 집계 | 분석10명/조건, 같은 사람의 서로 다른 과제 | 최종 package 선택 중앙값380→57초 | 이 행의 종점 아님 | 미확인 | 분석10명은 둘 다 명세 충족; 철회4명의 해당 시행 미확인 | 034 배경 집계. marginal median 차이는 paired median 차이가 아니며 raw task/period 시각이 없어 짝 CI 미산출 | [§10.2, Fig20/21](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf); J-NA-02/03 |
| O-NA-02 · 같은 조건 · 저자 집계 | 분석10명/조건 | 이 행의 종점 아님 | 중앙값849→847초 | 미확인 | 강제20분 cap 미확인, 실제 노동/후속 수정 미계측 | 선택 종점의 큰 차이를 전체시간에 적용할 수 없음. 시간×최종품질 원행 없음 | [§10.2, Fig20/21](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) |
| O-NA-03 · NCQ 실험1 NCQBasic→NCQRetrieval · 저자 집계 | 분석10명/조건, 다른 과제·고정 순서 | 별도 종점 | 중앙값936→748초 | 미확인 | 분석10명 명세 충족. task5의 의미적 검색 불일치 사례 존재 | 기존034 배경. 참가자·과제/순서 보존한 재산출 불가 | [§7.2, Fig10](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) |
| O-NA-04/05/06 · JavaDocs→eXoaDocs · 저자 집계 | 완료자 조건부; 각 시간 셀의 n 미확인 | 미확인 | 문서로 추론한 누적 평균: T1 14:40→8:53, T2 25:03→23:34, T3/4 32:03→30:32 | 미확인 | 전체40분, 시간 포함자와 검사 통과자의 동일성 미확인 | Task1 저자90% CI: eXoaDocs[4:29,13:16], JavaDocs[10:44,18:37]. 독립군 marginal CI이며 차이/짝/시간×품질 CI 아님. 최종 제출시간·전체 배정자 효과·동등 품질 시간으로 해석 불가 | [§5.2, Table X](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-07 · 같은 조건 · 저자 집계 | 배정12명/조건 | 미확인 | 개인별 시간 미확인 | 미확인 | 40분 안 네 과제 모두 올바름: JavaDocs1/12, eXoaDocs3/12 | 허용식 `3/12 − 1/12`; 원 층별 배정·결과와 시간키 없음. 기존034 집계의 반복을 새 원행 효과로 세지 않음 | [§5.3.2, Table XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-08 · 같은 조건, 과제3 · 저자 집계 | 배정12명/조건 | 미확인 | T3/4 시간 분리 불가 | 미확인 | 실행 검사 통과 JavaDocs4/12, eXoaDocs3/12로 방향 반대 | 허용식 `3/12 − 4/12`. 대조군의 ResultSet 수작업 예제도 사용됨 | [§5.3.2, Table XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-SNIPPET1/2 · NCQ 공개행 기술통계 | 142/156개 snippet; 각10가명×2 T-label | 시각 없음 | 시각 없음 | 미확인 | `Used?`와 `Runs?` 조합만 관측. 최종 과제 검사와 다름 | 행·키·flag 빈도만 계산 가능. T 조건 코드북이 없어 T1/T2의 치료 효과로 계산하지 않음 | [CSV1](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets1.csv), [CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv); ncq-row-audit.json |

## 범위와 현재 판정

이 분담은 S01·S02만 조사했다. 새 성과는 논문 숫자의 반복 계산이 아니라, 실제 공개 snippet 대장의 키·기수·결측, eXoaDocs의 문서 기반 시간 정의와40분 제한, NCQ 모집 철회 계보, 공개 구현과 실제 실험 과제의 판 차이를 확인한 것이다. **배정×시간×최종품질을 연결한 원행 비교는 두 군 모두 미확인**이다. 원자료가 없다는 전 세계적 부재를 증명하지 않는다.

`sources.jsonl`에는 기준선19행, `sources-addendum.jsonl`에는 추가19행이 있다. 엄격 배당에 들어가는 독립 저작은5개(원논문2, 별도 연구자료1, 구현1, 방법 보고서1)다. eXoaDocs의2009·2010 논문은 각각 별도 발행된 1차 자료로 직접 읽었지만, 전자는 도구 계보이고 후자는2013과 같은 실험이어서 배당과 연구군 수를 늘리지 않았다. 보관 루트·검색·DOI metadata·repo 하위파일도 배당0이다. 따라서 직접 읽은 별도 연구 발행물7개와 엄격 배당5개를 구별한다.

## Q1 · 무엇이 배정되었는가

NCQ 두 실험의 조건은 순서가 무작위 교차된 설계가 아니다. 같은 사람이 baseline을 먼저, 서로 다른 문제를 NCQ로 나중에 수행한다. 다섯 문제의 배치 균형은 순서/학습효과를 제거하지 않는다. 실험1은 공통 REPL에 검색을 켠 차이에 더 가깝지만, 검색을 켜면 얻는 후보·탐색 과정도 함께 바뀐다. 실험2는 VSCode와 NCQ 전체를 비교하여 편집/실행 환경, 검색, 순위, 코드 수정과 corpus 차이를 분리할 수 없다. NA-001 §7.1, §10.1, §13.

eXoaDocs는 네 숙련도 층에서 두 독립군으로 나눈다. mined example의 유무·선정·요약·인기도 표시가 함께 달라진다. JavaDocs도 일부 수작업 예제를 갖고 있었다. 따라서 두 군 모두 '동일 후보 링크에 근거 설명만 추가했을 때' 효과는 식별되지 않는다. 실제 본문/화면 설명은 NA-002 §5.1–5.3 및 NA-010/011의 Figure2/3 계보로 확인했다.

## Q2 · 키와 행 수

NCQ 고정판 `ce14f193f7014c120f04619826cb251818d99b0e`의 CSV1은142행, CSV2는156행이다. 둘 다 사람 가명10개, `(P,T)`20개이며 null P/T와 완전 동일 중복 행은 각각 **관측0**이다. `(P,T)`는 snippet에 대해 일대다이므로 unique key라고 쓰면 틀린다. 같은 키의 추가행은 각각122·136개다. CSV1에는 snippet·Package·두 flag가 빈 한 행이 있으며 그 행을 조용히 버리지 않았다. 멀티라인 CSV이므로 논리 행번호와 물리 줄번호를 따로 남겼다. `joins.json` J-NA-01/02와 `ncq-row-audit.json` 참조.

T에는1/2만 있고 논문의 다섯 문제와 연결할 공개 코드북을 찾지 못했다. 숫자1을 baseline,2를 NCQ라고 추정하여 시간 효과를 계산하지 않았다. CSV2 T-label2는68행인데 본문은 NCQ가 본 snippet81개를 보고한다. **T2=NCQ와 파일/집계 정의가 같다는 것이 입증될 때만** 불일치가 된다. 현재는 판·포함기준·코드북을 확인할 신호다. CSV2 경로 history의 유일 반환 commit은2022-04-07이고 읽은 논문판은2023-01-02이다. 원행 대장과 논문 최신표의 완전 일치를 전제할 수 없다.

eXoaDocs에서는 논문→저자 출판목록/프로젝트→DOI/Crossref→GitHub/Zenodo/OSF exact-title search→Wayback을 추적했다. 현재 프로젝트 HTTP/HTTPS503, ACM403, 보관 `/exoa/`404를 기록했다. Wayback의 실제2010 루트는 프레임만 있고, `/exoa/*` index는 논문1건만 반환했다. 공개 keyed ledger는 발견하지 못했다. 목표96슬롯은24×4라는 설계 분모이며 관측96행이라는 뜻이 아니다. J-NA-04.

## Q3 · 시간 계약

NCQ 선택은 링크 클릭이 아니라 package installation 이벤트다. 최종 package는 최종 결과에 쓰인 package이다. 코드 시각·화면·브라우저 기록은 수집했지만 공개 repo에는 도구 logger 구현만 있고 실제 세션 usage log는 찾지 못했다. 총시간과 활동시간은 다르다. 영상·강사 demo·훈련이 있었고,20분/문제는 연구자가 예상한 budget이다. 분석 그래프를 근거 없이1200초에서 자르면 안 된다. NA-001 §7.1–7.2, §10.2; NA-003-LOGGER.

eXoaDocs의 시간은 문서 행동으로 추론했다. 다음 과제의 관련 문서를30초 초과 읽은 것을 이전 과제 완료의 proxy로 삼으므로 실제 제출/테스트 완료 시각과 다르다. 과제3/4가 같은 문서를 보아 시간이 같게 보고된다. Table X는 완료자만 포함한다. 전체 네 과제에는40분 제한이 있었으며 첫 발췌에서 누락했던 이 사실은 `REVISIONS.md` NA-R01에 정정했다. 문서 dwell은 활동시간 계측이 아니다. NA-002 §5.2–5.3.2.

## Q4 · 품질·실패와 모집 철회

NCQ 논문의 분석 대상은 각각10명이며 모두 명세 충족 결과를 냈다고 보고한다. 별도 모집 보고서가 본문의 실험2 모집 절에서 직접 인용되고, 그 보고서에는14명 예약·10명 성공 세션·4명 세션 중 철회가 있다. 이는 '모든 예약자가 완료'라는 확대 해석을 막는다. 어느 과제/조건까지 했는지는 공개되지 않아 네 명을 임의로 각 조건의 실패나20분 시간에 배치할 수 없다. 분석10명의 서로 다른 과제가 이진 성공 기준을 통과했다는 사실도 장기 품질 동등성이나 재작업 감소를 입증하지 않는다. NA-004 §3와 J-NA-03.

eXoaDocs는 테이블 생성, 두 tuple 삽입, 출력/내용 대조로 기능을 검사한다. 시간표의 완료자와 테스트 통과자가 같은 사람인지 식별하는 키가 없다. 네 과제 모두 통과한3명/1명은40분 제한 내 결과지만, 나머지를 오답·미제출·timeout으로 나눌 수 없다. Task3의 eXoaDocs3명/JavaDocs4명은 품질 우위가 모든 과제에 일관되지 않음을 보인다. NA-002 §5.3.2.

## Q5 · 가능한 산술과 금지되는 합성

새 공개행 계산은 NCQ snippet key·flag의 기술통계다. 실제 프로그램은 인터넷에서 고정 CSV 두 개를 메모리로 읽고, Python 표준 `csv`로 파싱하여 합계만 저장했다. CSV1의 UTF-8 decode 실패 후 cp1252를 명시적으로 썼으며 바이트를 버리지 않았다. 원 참가자 가명·snippet·코드는 파일로 저장하지 않았다. 자체 ID 예시는 실제 같은 원 가명이 선택된 두 T-label 행에만 같은 자체 ID를 배정하도록 확인했다.

논문 집계에서는 NCQ의 조건별 중앙값과 eXoaDocs의 각12명 분모 통과 수를 그대로 보고할 수 있다. eXoaDocs 독립군의 기술적 비율차 식은 `(3−1)/12`다. 기존034 숫자의 재계산은 새 핵심 성과로 제시하지 않는다. NCQ의 `median(E)−median(C)`를 `median(E−C)`라고 바꾸거나, eXoaDocs의 서로 다른 사람을 가짜 짝으로 연결하면 안 된다. 시간표의 누락된 포함지시자·n·개인 결과 때문에 동등품질 시간쌍과 전체 배정자 평균은 계산할 수 없다. 독립군의 층별 배정/결과가 없어 층을 보존한 추정의 불확실성도 재현하지 못했다. O-NA-01~08.

## Q6 · 반례를 찾아본 결과

선택 중앙값380→57초와 총849→847초가 같은 연구에 공존한다. 서로 다른 marginal median이므로 둘을 빼서 '선택 후 처리시간이 늘었다'고 개인별 메커니즘을 새로 만들지 않는다. 더 오래 걸려도 명세를 만족한 일부 NCQ 시행은 본문 요약으로만 확인되며 정확한 사람·과제별 raw time은 없다.

공개 CSV에는 `Used?=0, Runs?=1`과 `Used?=1, Runs?=0` 모두 있다. 예컨대 CSV2 논리17행/물리126–127줄의 자체 예시 `NA-C2-trial-label-2`는 후자이다. 이는 사용 flag와 snippet 단독 실행이 일치하지 않을 수 있다는 자료 수준 반례이며 최종 과제 실패라는 뜻은 아니다. 원자료의 '봤다'도 완전 가시성·수집 방식이 다르고, 실제 이해·열독을 직접 입증하는 gaze/dwell field는 없다. eXoaDocs의10/12 대4/12 예제 사용은 설문 집계이며 읽기→채택→통과의 person-key chain이 아니다. 자세한 제한은 `counterexamples.md`에 둔다.

## Q7 · 제품에 옮길 수 있는 관측 범위

두 소프트웨어 군으로 판단 가능한 것은 단기 과제에서의 도구 묶음·문서 묶음 비교다. '후보를 빨리 골랐다'에는 동일한 선택 이벤트·대상 후보, '제한시간 안 정확히 끝냈다'에는 배정분모·과제별 제출/검사·cap, '나중 재작업이 줄었다'에는 첫 채택 baseline·추적 기간·후속 수정과 활동시간이 각각 필요하다. 마지막 관측은 두 군에서 확인되지 않았다. 분야 대조 연구는 이 분담 밖이므로 root의 X01/X02와 연결해야 한다.

## 실행과 재개

실행한 명령은 `python -B docs/workstreams/research/AF-RES-050/streams/ncq-exoa/audit_ncq.py`이며 출력은 `ncq-row-audit.json`, 실제 종료코드는0이다. 고정 CSV download와 파싱만 수행했고 NCQ 도구, 저자 검사기, 참가자 결과 프로그램은 실행하지 않았다. `capture_retrievals.py`도 read-only URL/hash 확인으로 종료0이었다. 저자 환경 설치나 사용자 모집은 필요하지 않았다.

추가 파일을 얻으면 첫 행동은 NCQ의 `(experiment,P,T)` 코드북과 시각/제출/검사표를 연결하여20개 대상 시행의 unmatched·period를 다시 검사하는 것이다. eXoaDocs는24명 배정표와 사람×과제 event/test export를 먼저 확보해야 한다. 연락은 이 작업에서 하지 않았다.

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 두 군의 배정×시간×최종품질 원행 join 불가; NCQ 공개 CSV는 snippet 단위 | 동등 품질 총시간·활동시간의 개선 크기 | [NCQ CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) 열 P/T/Used?/Runs?; [eXoaDocs Tables X/XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf); J-NA-01/02/04 | person×task×condition×period×time×score 코드북/대장 | 키와 시행분모·완료/실패 이유가 연결되고 동일 종점으로 분석 가능할 때 |
| NCQ 모집 철회4명은 분석10명에 포함되지 않지만 task/condition 진행 위치 미확인 | 모든 예약·배정자에서의 완료율과 시간효과 | [모집 보고서 §3](https://brittany-reid.github.io/publication/reid-2022-software/reid-2022-software.pdf); J-NA-03 | 예약14명의 세션 흐름·탈락 단계 ledger | 철회자의 배정/훈련/시행/결과가 확인되어 전체 분모 분석 가능할 때 |
| 여러 도구 기능/후보가 함께 다르고 추적 재작업·활동시간 없음 | 같은 링크 설명만의 효과 및 장기 재작업 절감 | [NCQ §7.1/10.1/13](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf); [eXoaDocs §5](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) | 동일 후보의 설명 배정과 adoption→test→후속 수정 기록 | 설명 개입이 분리되고 추적 수정/활동시간이 배정 단위에 연결될 때 |
