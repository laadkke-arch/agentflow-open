# PostgreSQL T1: 봉인 후 대조와 반증

전체 24건/72문구 봉인 `68fc97fadceb46f9945a71fcc53730e29f6c62bf`의 exact-SHA 원격 검증을 root가 알린 뒤 열람을 시작했다. 최초 후속 GET 시작은 `2026-11-22T05:08:42.062264Z`이며 `t1-receipt.json`과 개별 capture의 UTC/hash를 남겼다. 주 코딩은 같은 작성자의 순차 자기 점검이다. 이후 P03에는 curl 담당의 T0-only→T1 표적 재검과 root의 원문 재검에서 이견이 제기되어 수용했다(`p03-review-disagreement.json`). 이는 전체8건의 독립 가림 중복 코딩이 아니다. 가상의 I/C/Q를 원 작성자에게 보낸 적은 없다. T0 `initial.jsonl`, `frozen-responses.jsonl`은 변경하지 않았다.

## 핵심 집계와 분모

8개 질문을 유지했다. 공식 아카이브의 개별 Message-ID 본문 전문은 8/8 확보했고, 원형 RFC822 Received 헤더는 0/8이다. P04의 실질 질문 전문과 P05의 본문 전체가 첫 답의 인용과 공백 정규화 SHA256로 일치한다. P04에서는 인사·감사·서명이 인용에서 생략되었다. 이 보강은 회신 시점 이전의 요청 내용에 관한 교차 근거이며, 암호학적으로 제출 시각을 인증하지 않는다. `initial-quote-crosschecks.json`에서 두 범위를 분리했다.

후속 공개 메시지는 36개 읽었다. 여기에는 동일 사건 재게시의 첫 글 2개가 포함된다. 이를 36개의 독립 원문이나 36개의 독립 사건으로 세지 않는다. 대화 최소수는 P01–P08의 8건, 당시 제공자 문서는 서로 다른 파일 13건, 이 계열 고유 산입 원문은 총 21건이다. 8개 질문의 공개 발신자 표시는 6개다. P03/P05, P07/P08은 각각 같은 발신자다. P07/P08은 Oracle 이식 맥락을 공유하지만 정확히 같은 프로젝트인지는 미확인이다.

| 항목 | 관측값 | 제한 |
| --- | ---: | --- |
| 이미 T0에 봉인 변수 값이 있음 | 1/8, P01 | 부모에 저장한 행임이 최초 SQL/결과에 있음 |
| 응답자가 같은 변수를 묻고 작성자가 직접 답함 | 0/8 | 직접 답 분모는 0; 이 분모의 비율은 정의되지 않음 |
| 새 작성자 사실로 정확한 봉인 변수 값을 회수 | 0/8 | P03 local 발화는 실제 물리 원천과 예시 결과집합이 모호해 strict 집계에서 제외 |
| 넓은 실행경계 해석의 회수 민감도 | 1/8, P03 | local 발화를 실제 ID 원천까지 가리킨다고 해석할 때만1; 주 집계에 더하지 않음 |
| 아직 정확한 작성자 값 없음 | 7/8 | P01만 이미 T0에 있음. 30일 검열; 거절·실패로 코딩하지 않음 |
| 새 저자 사실 때문에 후보 판정 변화 | 0/8 | 실제 ID 질의의 B는 unknown 유지. 넓은 해석에서만1 민감도 |
| 그 변화에 작성자의 채택·구현 진전 보고가 동반 | 0/8 | 이해했다/좋아 보인다는 표현과 실행을 구분 |
| 실제 잘못된 승인·피해가 관측됨 | 0/8 | 가상 C의 부족한 분기조건은 P04 1건; 실제 실행은 관측되지 않음 |
| 원 요청 전체를 T0 사실로 판정 가능 | 2/8, P01/P05 | P05는 명시한 비교판14.1의 음성 구문 답. 실사용판 가정까지 제거하면 P01 1/8 |
| 명시된 기능 존재/구문 하위질문에 답할 수 있음 | 3/8, P01/P05/P07 | 전체 복구·이식·성능 해결로 확대하지 않음 |
| 가상 I의 한정된 문구가 문서로 지원됨 / 보류 | 5/8 / 3/8 | supported_limited는 전체 목표 해결을 뜻하지 않음 |
| 가상 C의 한정 문구 지원 / 보류 / 부족한 조건 | 5/8 / 2/8 / 1/8 | P04는 기존 파일 경계를 보존하는 조건 누락 |

실제 같은 변수 확인의 완료 왕복은 0회다. 더 넓은 의미의 응답자 메시지→작성자 직접 회신 쌍은 9회(P01 1, P03 2, P07 1, P08 5)다. 작성자의 자기 회신과 재게시는 왕복 수에서 제외했다. 가상 Q는 답이 온다면 추가 요청/응답 한 쌍이 필요하다는 구조만 기록했다. 실제 대기 시간과 가상 질문 비용을 같다고 놓지 않았다.

## 사례별 대조

| 사례 | 후속에서 확인한 것 | 봉인 변수와 판정 | 남은 한계 |
| --- | --- | --- | --- |
| P01 | 작성자가 data entry 목적도 언급. 응답자가 updatable view와 목적별 대안을 제시 | 부모 저장 여부는 이미 T0. 질문 없이 조회 방향 설명 가능 | data entry 목적이 시간 지나 새로 생겼는지, 처음부터 있었는지 불명. 새 목적을 T0 필수로 소급하지 않음 |
| P02 | Tom Lane이 실제 SELECT 오류 여부를 묻고 old transaction 가설 제시 | 작성자 답 없음. 응답자의 가설은 Q 값을 채우지 않음 | 문서상 EXPLAIN/실행 차이와 손상 원인·안전한 복구는 별개 |
| P03 | 원 스레드는 무응답. 1월6일 재게시에서 작성자가 local 쪽 table/result 설명 | 실제 ID 원천의 B는 unknown 유지. 상수 UNION 예시는 T0부터 remote join 조건 불충족. 진단 A 유지 | local 표현이 실제 물리 원천인지 결과집합 실행경계인지 모호. 넓은 해석의 변화1은 민감도만 |
| P04 | 첫 답은 flat SQL이라고 설명하고 기존 파일 편집과 다음 덤프 구성을 구별 | 원본 접근 여부 답 없음. 원판 재독으로 새 덤프 제안의 입력 경계 부족 확인 | 새로운 dump는 기존 dump와 데이터 시점이 달라질 수 있음. C의 접속 가능 조건만으로 원 목표를 승인하면 안 됨 |
| P05 | 응답자는 사용판 확인과 해당 문서를 요구하고 개별 이름 refresh는 안 된다고 답함 | ONE 분기는 처음부터 요청됨. 금지 강도 확인은 음성 구문 답에 불필요 | T0의 preference 코딩을 정정하는 민감도는 새 후속 정보의 효과가 아님. 실제 PG판 미상 |
| P06 | SQL·기대값·실제값·PG판을 요구하고 PostGIS 목록 안내 | geography/SRID 일치 값 없음. I/C 모두 원인 보류 | 같은 입력이라는 답 하나를 받아도 PROJ/실제 SQL/수치가 더 필요 |
| P07 | 작성자가 DO block에서 Oracle SQL 전체를 쓰려는 것인지 추가 질문 | 원 Oracle 스크립트의 loop/branch는 여전히 미공개 | SQL 함수가 있다는 yes가 Oracle 호환 yes로 확대될 수 있는 반례. 봉인 I의 한계 문구는 유효 |
| P08 | PostGIS 재게시에서 추가·순회·pop·위치 접근, 이후 단순성 선호를 질문 | numeric→text 허용은 답하지 않음. basic map 후보와 전체 collection 목표는 분리 | 새 목적 표현은 확인했지만 발생 시점과 필수 강도는 불명. 가능해 보인다는 말만 있고 채택/실행 보고 없음 |

## 재게시의 계보와 시간

P03의 원 요청은 `2022-01-03T16:26:33Z`이다. 재게시 첫 글은 `2022-01-06T07:43:46Z`이며 동일 SQL, 2.5GB/122행/70MB 설명, 빠른16.251ms·느린46827.945ms 수치가 일치한다. 이는 강한 내용 계보지만 실인물 동일성 인증은 아니다. 작성자의 local 표현은 `2022-01-06T10:20:49Z`, 원 요청에서 65.904444시간 후다. 앞선 실제 질문은 use_remote_estimate/fetch_size였으며, ID 원천 위치를 직접 묻지 않았다. 발화 자체는 `author_existing_fact`이고 `direct_answer`가 아니다. 그러나 같은 상수 UNION 예시를 다시 사용했으므로, 그 local table이 예시 결과집합인지 실제 ID 질의의 물리적 테이블인지 확정되지 않는다. 정확한 frozenQ의 값으로는 사용하지 않고 `locked_variable_value_used=false`로 두었다.

- 원 요청: <https://www.postgresql.org/message-id/DB9PR07MB7180EDC1ACD3222532399E1CCB499%40DB9PR07MB7180.eurprd07.prod.outlook.com> p2–8.
- 재게시: <https://www.postgresql.org/message-id/DB9PR07MB7180C5E73400BB58F649843FCB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com> p2–8.
- 작성자 사실: <https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com> p3–5.
- 뒤의 DELETE 실행: <https://www.postgresql.org/message-id/DB9PR07MB7180C7235B334F3D8D6EED1FCB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com> p2–4. 최초 SELECT INTO의 개선 결과가 아니다.
- 응답자의 별도14beta1 재현: <https://www.postgresql.org/message-id/CAM%2B6J96i4Wad41fLvcJB_anBGQgAxyg-RcBirtAH0%3DQcVYTEmw%40mail.gmail.com> p3–18. 질문자 채택 및14.1 공식 보증과 구별한다.

P08의 PostGIS 재게시는 같은 공개 발신자·제목·Oracle 선언을 가진다. 첫 글은 원 요청보다 약6.32시간 뒤다. 1월8일 요구 확대는 그 재게시의 첫 답 이후 약5시간이 지나 공개되었으나, 요구가 그 사이에 새로 생겼다는 증거는 없다. P07 같은 발신자의 Oracle 스크립트에 실제 루프가 있었다는 증거로 P08의 loop 가능성 언급을 전이하지 않는다.

- 재게시 원문: <https://lists.osgeo.org/pipermail/postgis-users/2022-January/045146.html> p1–3.
- 추가 처리 조건: <https://lists.osgeo.org/pipermail/postgis-users/2022-January/045171.html> p3–7.
- 순서 제약과 순회 예: <https://lists.osgeo.org/pipermail/postgis-users/2022-January/045172.html> p2–30.
- 작성자 가능성 평가: <https://lists.osgeo.org/pipermail/postgis-users/2022-January/045174.html> p2–4.
- 단순성 추가 질문: <https://lists.osgeo.org/pipermail/postgis-users/2022-January/045192.html> p2–3.

## 반례를 찾은 결과

**질문 없이 충분한 경우:** P01은 이미 행의 저장 위치가 본문에 있었다. P05는 요청된 ONE 분기가 알려져 있으며14.1의 구문이 이름을 받지 않는다는 사실에는 선호 강도 답이 필요하지 않다. 다만 실제 사용판을 확인하지 않은 무제한 판정은 피한다.

**관련 발화를 정확한 조건 값으로 오인하는 경우:** P03의 local 표현을 실제 ID 물리 원천의 값으로 읽으면 B가 탈락한다고 보인다. 표적 재검은 이것이 상수 UNION 예시의 실행경계일 수도 있음을 지적했다. 원 글은 그 예시와 실제 SELECT를 명시적으로 구별했다. 따라서 주 비교는 변수 미회수/판정 변화0, 넓은 실행경계 해석의 민감도는1로 고쳤다. I의 EXPLAIN VERBOSE 제안은 최초 글만으로 가능했고 C도 local 분기를 이미 제시했다. 이 사건은 가상 Q의 해결 속도 효과를 입증하지 않는다.

**조건을 하나 골랐지만 입력 경계를 잘못 잡은 경우:** P04는 복원할 원 파일이 주어진다. 원본 접속 가능성은 같은 스냅샷이나 재덤프 허용을 뜻하지 않는다. `coding-corrections.json`에 frozen coding과 original reread 판단을 따로 보존했다. 이것은 저자 후속 답의 공로가 아니다.

**맞는 기술 사실을 목표 전체에 확대하는 경우:** P07의 SQL 함수 존재와 Oracle 스크립트 호환은 다르다. P08의 문자열 키·숫자값 표현과 처리 순서/queue 동작도 다르다. jsonb object key 순서와 hstore pair 순서는 보존 보장이 없다(P-D12 L46–60, P-D11 L39–49). 그러나 후속에서 순서가 엄격한 필수라고 확정된 것도 아니므로, 그 해석은 주 비교가 아닌 소급 민감도에만 넣었다.

**조건부 답이 실제로 해결했다는 증거 탐색:** P01/P04/P08에서 실제 조건부 응답을 찾았지만, 그 답만으로 작성자가 목표를 실행·해결했다고 보고한 사례는 없었다. 이 계열에서 그러한 해결 관측은 0/8이며, 효과가 없다는 뜻은 아니다. 동일하게 봉인 변수의 확정된 새 값이 두 후보 모두에 무관했던 실측 예는 확보하지 못했다. P03의 관련 local 발화를 넓게 해석할 때만 B 전제에 관계하는 민감도가 있다.

**시간 지연과 요구 자체 변화:** P01/P03/P07/P08에서 나중에 다른 목적·동작·선호가 표현되었다. 그것이 새로 생긴 요구인지 기존 목적을 뒤늦게 설명한 것인지는 모두 미확인이다. Q4의 `new_requirement` 행에 `temporal_origin`을 함께 두었고, 새 요구가 실제로 탄생했다고 주장하지 않는다.

## 30일·90일 범위와 원판 보강

원 스레드의 모든 공개 후속 링크를 열었다. 발견한 두 재게시의 연결된 메시지도 모두 열었다. 31–90일에 해당하는 구현/채택 보고는 찾지 못했다. 추가로 정확 제목/작성자 검색과 PostGIS 2022년1–4월 공개 date 원장을 살폈다. 1월78개, 2월118개, 3월74개, 4월59개 제목·작성자 행 범위에서 Sameer Twayana의 연결된 geography/ST_Length/ST_Distance 사례는 찾지 못했다. 2월의 다른 작성자 ST_DWithin 스레드는 동일 사건으로 연결하지 않았다. 4월 전체 목록은 검색상 열렸으나 사례별90일 끝 이후는 결과 창에 포함하지 않는다. 인덱스 열람을 각 메시지 전문 열람으로 세지 않는다.

P04/P05 공식 페이지의 Raw/mbox는 href="#"와 별도 data-ref를 가진 POST폼 동작이었다. 공식 main.js를 읽고 공개 Raw 요청 두 건을 폼과 같은 방식으로 재시도했지만 List archives 로그인 페이지로 이동했다(`initial-raw-attempts.json`). 원형 메일/Received는 확보하지 못했고 인증은 진행하지 않았다. 대체 공개 mail-archive 검색 두 건도403이었다(`initial-mirror-attempts.json`). P08의 OSGeo 월별 `.txt` 원형 mbox 시도는404였으며, 개별 Pipermail 원문과 mailto 회신 대상의 Message-ID로 보강했다. 원본 `In-Reply-To` 또는 Received 헤더라고 오인하지 않는다. 실패 자료와 검색 결과만 읽은 자료는 최소수에서 제외한다.

## 파일과 재현

- `followups.csv`: 36개 공개 메시지와 8개 검열/무응답 요약. `record_type`으로 구별한다. 정확한 Q 값에 쓸 새 저자 발화는 없어 `locked_variable_value_used`는 모두false이며 P03 넓은 해석을 별도열에 둔다.
- `judgments.csv`: 후보·조건별 T0/T1 쌍. `adjudication_basis`가 원판 재독/새 저자 사실/새 요구 소급을 구별. 기술 근거와 작성자 행동 근거 별도.
- `case-analysis.jsonl`: 8건의 전략 제한·분모·변수값·시간·왕복·행동·반례.
- `sources-t1.json`: 기존 P-S01–08/P-D11–12를 보강하고 신규 P-D13 추가. 같은 자료 ID를 새 원문 수에 다시 더하지 않는다.
- `field-locations.jsonl`: T0의 목표/입력/출력/버전/플랫폼/주체 각6필드에 위치와 명시·연구자 해석·미상 표시. 후속 사실 사용 없음.
- `coding-corrections.json`: P04 입력 경계와 P05 ONE 분기 강도의 원판 재독 보정.
- `initial-quote-crosschecks.json`: P04/P05 최초판과 첫 회신 인용의 정규화 hash 및 범위.
- `t1-summary.json`, `t1-validation.json`: 집계 및 T0 불변 확인.

재현 명령은 저장소 루트에서 다음과 같다. 네트워크 재열람은 공개 원문이 유지되어야 한다.

```bash
python docs/workstreams/research/AF-RES-026/streams/postgres/verify_initial_quotes.py
python docs/workstreams/research/AF-RES-026/streams/postgres/build_t1.py
```

후자는 저장된 메타데이터와 명시 코딩에서 결과 표만 재생성한다. PostgreSQL 실행·성능 재현·사용자 실험을 수행하는 명령이 아니다. 원본 SQL 및 누락된 환경을 받지 못했으므로 안전한 복구나 실제 성능 검사는 실행하지 않았다.

## 남은 중요한 약점과 다음 한 건

1. **최초판의 서버 수신시각:** P04/P05 회신 인용 보강은 실질 내용의 선행성을 강하게 지지하지만 raw Received를 대체하지 않는다. 다음 조사는 공식 pgarchives의 해당 Message-ID 원형 RFC822 또는 당시 별도 공개 보존본 두 개에서 본문과 Received를 대조하는 것이다.
2. **질문 변수의 선택 실패/목표 축소:** P04의 기존 파일 경계, P07의 Oracle 호환, P08의 처리 순서 때문에 기본 기능 사실만 맞아도 전체 목표는 미확인이다. 다음 조사는 봉인된 P04/C를 최초 글만 읽은 독립 판독자가 재분류해, 접속 가능 조건으로 새 덤프를 원 요청 해법으로 승인하는지 확인하는 것이다.
3. **정확한 변수값·행동·인과 효과 부재:** 같은 변수 직접 답0건, 정확한 새 변수값0건, 채택/구현 진전0건이다. P03의 관련 local 표현만으로 실제 원천을 확정하면 예시/실제 경계를 혼합한다. 다음 조사는 P03의 실제 ID SELECT/EXPLAIN VERBOSE와 작성자의 후속 구현·지연 보고가90일 안에 별도 공개 장소에 있는지 원 Message-ID 계보로 확인하는 것이다. 없으면 미확인으로 유지한다.
