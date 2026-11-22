# AF-RES-026 · 근거와 반증의 사후 자체 점검

점검 기준 시각: 2026-11-22 05:51:33 UTC. 전체 T0 봉인은 `68fc97fadceb46f9945a71fcc53730e29f6c62bf`, 이 문서가 대조한 통합 결과 판은 `a9dd0998e8428c74cd7722c19a06223ac5c7df20`이다. 원문별 근거와 한계는 [sources.json](sources.json), 사례별 원판 필드의 명시·연구자 해석·미상 구분은 [field-locations.jsonl](field-locations.jsonl)에 있다. 이 자체 점검을 작성하면서 새 외부 원문을 추가하지 않았다.

**판독 방법:** 계열 담당자가 같은 사례의 T0와 T1을 순서대로 읽었고, 통합자가 원판과 일부 후속을 다시 대조했다. P03, 타 분야 자료, S03·S08에는 표적 동료 검토와 정의 조정이 있었다. 이는 사후 자기 점검 및 표적 교차검토이며, 전체 24건을 가린 독립 판독자에 의한 이중 코딩이 아니다. 원판 재독으로 찾은 오류는 작성자가 새로 제공한 사실과 분리한다.

## 먼저 고정한 분모와 용어

| 점검 대상 | 이 문서에서 사용하는 수 | 재현 위치와 제한 |
| --- | --- | --- |
| 모집 원장 | 149행 = root 심사 40건(포함 24·제외 16) + 답장 metadata 87행 + 상한 뒤 미심사 22행 | [frame.csv](frame.csv), [SCOPE.md](SCOPE.md)의 실행 종료 전 범위 확정. 149개의 적격 최초 질문을 읽었다는 뜻이 아니다. curl의 제외 root 3건은 제목·원장 기준 제외이며 본문 완독을 주장하지 않는다. |
| 주 표본과 메시지 | 3계열 × 8건 = 24건, 사례별 I/C/Q = 72문구 | [initial.jsonl](initial.jsonl), [frozen-responses.jsonl](frozen-responses.jsonl), [t0-seal.json](evidence/t0-seal.json). 답·수락·진전 유무로 표본을 교체하지 않았다. |
| 원판 증거와 노출 | 원문 전문·원판 식별 연결 24건 / 추가 교차 보강 18건 / 답 요약 미노출 23건 | 추가 보강은 SQLite 8 + curl 8 + PostgreSQL P04/P05이다. 24건 모두의 제출 시각을 암호학적으로 인증했다는 뜻이 아니다. S01은 봉인 전 답 한 문장 노출이다. |
| 최소수 산입 외부 원문 | 61저작 = 대화 24 + 당시 제공자 문서·테스트 32 + 타 분야 5 | [source-counts.json](evidence/source-counts.json). 날짜 불명 X-S1을 제외하면 60저작·타 분야 4가 남는다. `sources.json`의 159행은 탐색·재독·계보를 포함한다. 댓글·개정·재게시·같은 파일의 여러 판을 독립 저작으로 늘리지 않는다. |
| 후속 기록과 조건 판정 | 후속 137행 = 공개 발화 114 + 개정 4 + 검열 요약 11 + 원 사례와 미연결 인접 기록 8; 조건 판정 294행 = T0/T1 147쌍 | [followups.csv](followups.csv), [window-audit.json](evidence/window-audit.json), [judgments.csv](judgments.csv). 137명을 뜻하지 않으며 인접 기록 8행은 주 사례의 새 요구나 진전으로 합산하지 않는다. |
| 정확한 봉인 변수 | 이미 T0에 있음 8/24, 엄격 신규 작성자 값 0/24, 정확히 같은 변수의 완료 직접 답 0/24, 여전히 미확인 16/24 | [analysis.csv](analysis.csv), [metrics.json](evidence/metrics.json). 직접 답만의 분모는 0이므로 비율은 **해당 없음**이다. |
| 약한 값·판정 변화 민감도 | 넓은 값 해석 최대 3건(P03·S04·C05); 엄격 새 사실에 따른 후보 변화 0건, P03의 넓은 해석에서만 변화 1건 | [adjudication-overrides.json](adjudication-overrides.json). 이 상한은 해석 규칙을 바꾼 민감도이며 통계적 신뢰구간이 아니다. |
| 설명 범위와 전체 사용 승인 | 제한된 문구 성립 I 13·C 14; 전체 사용 승인 I 4(S01·S03·S08·P01), C 2(S01·P01) | [strategy.csv](strategy.csv), [strategy-summary.csv](strategy-summary.csv). 엄격 미노출 분모에서는 I 3·C 1. 보류·부적합 설명·미출시 제안은 전체 사용 승인이 아니다. |
| T0 원 목표의 사실 충분성 | 6건(S01·S03·S07·S08·P01·C03); 선언한 비교판 가정하에서 P05를 더하면 7건 | [analysis.csv](analysis.csv)의 두 `T0_original_goal...` 열. 사실이 충분해도 실제 봉인 문구가 필요한 조건을 모두 포함했는지는 별도 판정이다. |
| 행동 관측 | S01의 자기 실행 성공, C05의 기존 workflow에 대한 결정 수용, C06의 공급자 신규 개발 | 같은 종류의 채택 3건으로 합치지 않는다. 아래 Q5의 각각 다른 당사자 기록을 사용한다. |
| 실제 추가 질문 비용 | 주 대화 7쌍(S01 3·S04 3·C07 1) + 별도 구현 1쌍(C06) | [actual-roundtrips.json](evidence/actual-roundtrips.json). 같은 실제 쌍을 I/C/Q마다 세 번 더하지 않는다. |

`0건`은 정의한 범위에서 산입 조건을 충족한 관측이 없다는 뜻이다. `미확인`은 필요한 사실·계보·판·행동 근거가 부족하다는 뜻이다. `해당 없음`은 분모 0 또는 적용할 수 없는 항목에 사용한다. `관측 실패`는 차단·삭제·원형 미확보 같은 자료 접근 문제다. 무응답은 30일 창의 검열로 기록하며 거절이나 실패로 바꾸지 않는다.

## Q1 · 후속보다 앞선 최초 요청을 얼마나 고정했는가

**점검한 주장.** 각 계열의 월별 공식 원장을 최초 제출 시각으로 심사하고, 같은 프로젝트에서 8건에 도달하면 멈췄다. 기본 기간은 2022–2024였으나 실제 표본은 모두 2022년 1월에 모였다. SQLite는 1월 1–6일, PostgreSQL은 1월 2–5일, curl은 1월 1–25일이다. 뒤의 연도나 일반 소프트웨어 질문 전체의 대표 표본으로 해석하지 않는다.

**근거 ID·URL·위치.** 표집 규칙의 사전 판은 `cecbfb981b9a7ccfd59f7bc40a23445a19d020fa`의 [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/cecbfb981b9a7ccfd59f7bc40a23445a19d020fa/docs/workstreams/research/AF-RES-026/SCOPE.md), 원장 전체는 `frame.csv`의 `frame_id/decision/reason`이다. SQLite의 예인 [S-S03 원판 artifact](https://sqlite.org/forum/artifact/c9ec666ab91f0454a91fa4374d971ea44e0af0859665f70b7c8722f4fbf66ea7)는 W body와 artifact 식별자, curl의 [C-R03 개별 메일](https://curl.se/mail/archive-2022-01/0024.html)은 body L32–45 및 HTML `id/isoreceived/isosent`가 근거다. P04는 [P-S04 최초 메일](https://www.postgresql.org/message-id/YdQFiQrF/2GXgxTI%40pureos) p2–3과 [첫 답](https://www.postgresql.org/message-id/4024278.1641308516%40sss.pgh.pa.us) p1–2의 실질 질문 인용이 일치한다. P05는 [P-S05 최초 메일](https://www.postgresql.org/message-id/DB9PR07MB718011344D6E231910D42BFBCB4A9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p1–2와 [첫 답](https://www.postgresql.org/message-id/0b7219fe-2bfe-f01d-ce1b-025bfb07e24f%40matrix.gatewaynet.com) p2·p7의 인용이 일치한다. 정규화 방법·SHA256·일치 범위는 [initial-quote-crosschecks.json](streams/postgres/initial-quote-crosschecks.json) P04/P05 행에 있다.

**반증을 찾은 모집틀과 관측 결과.** 선택 24건과 제외·metadata·상한 뒤 행을 모두 남겼고, 무응답 P03을 답 있는 사례로 바꾸지 않았다. P03 재게시도 새 표본으로 추가하지 않았다. PostgreSQL raw/mbox와 공개 미러를 추가 시도했으나 공식 경로는 로그인으로 이동했고 미러는 403이었다. P08의 OSGeo 월별 mbox 시도는 404였다. URL·시도 결과는 [initial-raw-attempts.json](streams/postgres/initial-raw-attempts.json), [initial-mirror-attempts.json](streams/postgres/initial-mirror-attempts.json), [notes-t1.md](streams/postgres/notes-t1.md)의 원판 보강 단락에 남았다. P04의 회신 인용은 인사·서명을 포함한 원 본문 전체가 아니라 **실질 질문 전문**의 일치다.

**미확인과 판단을 바꿀 최소 자료.** PostgreSQL 8건의 원형 RFC822 `Received`는 확보하지 못했다. 따라서 원판 연결 24, 추가 보강 18, 미노출 23을 하나의 확정 수로 합치지 않는다. 추가 교차 자료가 약한 P01·P02·P03·P06·P07·P08 중 한 건이라도 당시 원형 메일 또는 별도 보존본의 본문·수신 헤더가 나오면 그 건의 증거 수준을 올릴 수 있다. 완전한 24건 사전 미노출 조건은 S01의 이미 발생한 노출 때문에 **met=false**이며, 자료 보강으로 그 노출 이력을 지울 수 없다.

## Q2 · 최초판만으로 조건과 발화 주체를 구분했는가

**점검한 주장.** 목표·입출력·판·플랫폼·행위 주체, 필수·금지·선호·불필요·미상·상충을 T0에 코딩하고 근거 위치를 남겼다. 후속을 읽은 뒤 추가한 위치 보강은 원판 값의 소급 수정이 아니다. 최초판에 없던 실제 설치판·비동기 주체를 당시 문서의 이름이나 최신판으로 채우지 않는다.

**근거 ID·URL·위치.** [C-R01](https://curl.se/mail/archive-2022-01/0002.html) L33–42에는 브라우저 Request cookies와 XHR/Fetch 주체가 이미 있다. L39–40의 쿠키 제거는 테스트 상태이며 쿠키 사용 금지가 아니다. [C-R03](https://curl.se/mail/archive-2022-01/0024.html) L33–39에는 curl 업로드 뒤 서버 처리 순서가 있지만 클라이언트의 `await`나 서버 내부 비동기성을 확정할 내용은 없다. [S-S03](https://sqlite.org/forum/artifact/c9ec666ab91f0454a91fa4374d971ea44e0af0859665f70b7c8722f4fbf66ea7)의 steps 1·10·12는 이 예에서 외래키 단계가 불필요하다는 뜻이고, OFF는 당시 설정이지 반드시 유지할 금지 조건이라고 확정하지 않는다. [S-S06](https://sqlite.org/forum/artifact/aaa53d0db4c1f9528ffdb3c076295a72e90161af0e66d88b016b866e5f9e1957)의 `Dont ask why` 문장은 빌드 시스템을 여럿 쓰는 이유를 다시 묻지 말라는 실제 경계다. 여섯 필드의 명시/해석/미상 위치는 `field-locations.jsonl`의 해당 사례 행에 있다.

**반증을 찾은 모집틀과 관측 결과.** 24건의 요구 분류를 원판 위치와 다시 대조했다. P05의 [원판 P-S05](https://www.postgresql.org/message-id/DB9PR07MB718011344D6E231910D42BFBCB4A9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p1은 처음부터 하나의 publication을 요구한다. `do not want`를 언제나 약한 선호로 낮춰서는 안 되지만, 모든 상황에서 전체 refresh가 절대 금지라는 강한 주장 역시 미확인이다. 이 교정과 C01·P04 재독은 [postseal-original-review.json](evidence/postseal-original-review.json), [coding-corrections.json](streams/postgres/coding-corrections.json)에 보존했다. 이는 Q의 새 정보 이득이 아니다. S03의 `n/a`와 C01의 테스트 상태를 금지로 읽는 경우도 명시적으로 배제했다.

**미확인과 판단을 바꿀 최소 자료.** 이미 T0에 정확한 봉인 변수 값이 있는 8건은 S01·S02·S07·S08·P01·C01·C03·C07이다. P05의 강한 금지 여부는 이 8건에 억지로 넣지 않는다. 독립 판독자가 후속을 가린 최초판과 같은 코드북만으로 필수/선호·주체를 재코딩한 자료가 생기면 판독 안정성을 별도로 평가할 수 있다. 현재 자료는 해석이 일치한다는 독립 신뢰도 추정치를 제공하지 않는다.

## Q3 · 세 메시지의 입력·길이·판정 수준이 같은가

**점검한 주장.** 사례마다 같은 최초 입력 해시와 후보 최대 두 곳을 사용한 I/C/Q를 먼저 저장하고, 전체 24건·72문구를 봉인했다. 반환 길이는 링크를 포함해 각 300자 이하이며 가상 메시지는 실제 전송하지 않았다. 근거가 있는 보류문을 사용 승인으로 세지 않는다.

**근거 ID·URL·위치.** [봉인된 frozen-responses.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/68fc97fadceb46f9945a71fcc53730e29f6c62bf/docs/workstreams/research/AF-RES-026/frozen-responses.jsonl)의 각 사례 `input_sha256/I/C/Q/candidate_ids`와 [t0-seal.json](evidence/t0-seal.json)의 파일 해시가 입력 경계다. [C-D04](https://github.com/curl/curl/blob/801bd5138ce31aa0d906fa4e2eabfc599d74e793/docs/cmdline-opts/data.d) L14–34와 [C-D05](https://github.com/curl/curl/blob/801bd5138ce31aa0d906fa4e2eabfc599d74e793/docs/cmdline-opts/data-binary.d) L10–23은 C04의 줄바꿈 제거/바이트 보존 분기를 뒷받침하지만 원인의 해결까지 보증하지 않는다. [P-D07](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/alter_subscription.sgml) L22–35·L98–164는 P05의 14.1 구문 답을 한정한다.

**반증을 찾은 모집틀과 관측 결과.** 72문구 모두에서 이미 적힌 값의 재질문, 답을 알아도 남는 조건, 후보 없는 보류를 유지했다. C08은 후보가 없어도 원 질문과 세 문구를 남겼다. S08 C는 바인딩 설명은 지지되지만 I에 있던 나머지 NOT NULL 열 조건을 포함하지 않아 전체 사용 승인에서 제외했다. S03 C는 OFF 유지 분기값이 정해지지 않았고 다른 분기는 참조 의미 확인을 남기므로 전체 승인에서 제외했다. S03 C의 사용 가능한 첫 갈래만 넓게 세면 C 전체 승인 3건이라는 민감도를 따로 남겼다. [adjudication-overrides.json](adjudication-overrides.json)의 S03·S08은 후속 사실 효과가 아닌 사후 정의·집계 보정이다.

**미확인과 판단을 바꿀 최소 자료.** I 제한 성립 13·보류 11, C 제한 성립 14·보류 9·근거 부족 1이라는 문구 판정과 전체 사용 승인 I 4·C 2를 구분한다. S01을 제외한 23건은 미노출 비교가 가능하지만, 전체 24건의 완전한 사전 통제는 성립하지 않는다. 실제 I/C/Q가 무작위 또는 비교 가능한 조건으로 사용자에게 전달되고 행동이 관측되기 전에는 질문의 인과효과나 시간 절감은 미확인이다.

## Q4 · 누가 어떤 값을 언제 밝혔는가

**점검한 주장.** 직접 답, 작성자가 자발적으로 밝힌 기존 사실, 제3자 해석, 후발 요구, 답 없음·자료 미확보를 발화 행마다 구분했다. 발화가 있다는 것과 정확한 봉인 변수의 값을 채웠다는 것은 별도다. 후속 공개 대화의 주 창은 최초 요청 기준 30일이고 별도 구현은 90일 열에 둔다.

**근거 ID·URL·위치.** P03의 [P-S03 최초판](https://www.postgresql.org/message-id/DB9PR07MB7180EDC1ACD3222532399E1CCB499%40DB9PR07MB7180.eurprd07.prod.outlook.com) p2·p7–8은 상수 UNION을 실제 ID SELECT의 예로 구분한다. [작성자의 local 발화](https://www.postgresql.org/message-id/DB9PR07MB718015C40BC021957A7165F5CB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p3–5, 2022-01-06 10:20:49 UTC는 같은 예시를 반복한다. 앞선 질문은 `use_remote_estimate/fetch_size`에 관한 것이므로 동일 봉인 변수의 직접 답으로 세지 않는다. 같은 대화 ID의 `postseal_observations/followup_read_events`와 [p03-review-disagreement.json](streams/postgres/p03-review-disagreement.json)에 이 한계가 있다. S04는 [S-S04-T1의 committed 주장](https://sqlite.org/forum/artifact/2070eae6fd0fa53a44a8ac87b946dd31facab9d181d29f4a304c74c5846246a4) body L1–2와 [재현·로그](https://sqlite.org/forum/artifact/8a24d27a64786c26fcee69222d94ce3e0d88c58126bec7aedcd22bff513139d6) body L7–23·L28–35가 충돌을 남긴다. C05의 [C-F010037](https://curl.se/mail/archive-2022-01/0037.html)은 기존 empty temp directory·move/rename 문장에서 부분 사실을 제공한다.

**반증을 찾은 모집틀과 관측 결과.** 24개 원 스레드와 연결 근거가 있는 재게시·후속 구현을 대조했다. 엄격한 신규 값 회수와 같은 변수의 완료 직접 답은 각각 0건이다. P03의 `local`을 실제 물리적 원천으로, S04의 `committed`를 성공 반환으로, C05의 기존 rename을 basename 보존의 완전한 답으로 넓게 읽으면 최대 3건이지만 주 집계에 합치지 않는다. P03의 뒤 [DELETE 실행](https://www.postgresql.org/message-id/DB9PR07MB7180C7235B334F3D8D6EED1FCB4C9%40DB9PR07MB7180.eurprd07.prod.outlook.com) p2–4는 원 SELECT INTO 해법의 결과가 아니다. P08의 [추가 처리 요청](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045171.html) p3–7과 [단순성 요청](https://lists.osgeo.org/pipermail/postgis-users/2022-January/045192.html) p2–3은 늦게 말한 요구이지만 그때 새로 생겼는지는 미확인이다.

**미확인과 판단을 바꿀 최소 자료.** P03에는 실제 ID SELECT와 foreign-table 매핑 또는 물리 원천 서버를 명시한 작성자 발화, S04에는 원앱과 같은 실행의 성공 COMMIT 반환·재시작 로그, C05에는 최초 시점의 basename 보존 강도를 명시한 발화가 필요하다. P03/P08 재게시의 내용·공개 발신자 계보를 기록했지만 실인물 인증은 없다. P07/P08은 공개 발신자와 Oracle 이식 맥락을 공유하며 독립 사용자 두 명으로 해석하지 않는다. `window-audit.json`의 C03·C04·C08 경계 차이 3행은 검열 요약이며 실제 발화의 30일 포함 여부를 바꾸지 않는다.

## Q5 · 조건 판정과 당사자 행동을 서로 다른 근거로 보았는가

**점검한 주장.** 같은 후보·같은 비교판·같은 조건의 T0/T1 147쌍을 유지하고, 기술적 지지는 제공자의 당시 문서·테스트에, 진전은 당사자 발화·diff에 연결했다. 새 작성자 사실로 후보 적합성이 바뀐 엄격 사례는 0건이다. 실제 요청자의 설치판이 미상이면 비교 문서판을 그 설치판이라고 대입하지 않는다.

**근거 ID·URL·위치.** [P-D04](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/postgres-fdw.sgml) L800–840의 원격 join 조건은 P03의 실제 ID 원천을 밝혀주지 않는다. [P-D05](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/pg_dumpall.sgml) L30–68·L780–801과 [P-D06](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/pg_dump.sgml) L36–87은 기존 dump와 새로운 dump가 같은 데이터 시점을 갖는다는 보증이 아니다. [S-TD02](https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/test/notnull.test) L25–51·L75–81은 S08의 생략한 NOT NULL 열과 DEFAULT 있는 열을 구분한다. 이는 읽은 테스트 기대값이며 이번 실행에서 구판 바이너리로 실행한 결과가 아니다.

| 당사자 행동 | 근거 ID·URL·정확한 위치 | 산입한 것과 제한 |
| --- | --- | --- |
| S01 자기 실행 | [S-S01-T1의 작성자 보고](https://sqlite.org/forum/artifact/76963f0026b6b12a2ccec60eff052ad870a1fe4e597334cf19d287ffcc2f18cb), body L3·L16–18·L35–59 | 자기 test app과 대조 결과의 성공 보고. 연구자가 재실행한 성공은 아니며 S01 노출 때문에 엄격 미노출 분모에서 제외한다. |
| C05 결정 수용 | [C-F010037](https://curl.se/mail/archive-2022-01/0037.html), 기존 temp directory·move/rename 문장 | 설명 수용과 기존 workflow 공개. 새 기능 사용이나 새 실행 성공으로 세지 않는다. |
| C06 공급자 개발 | [C-F010060](https://curl.se/mail/archive-2022-01/0060.html), `To get a feel` 단락·PR8314 링크; [C-IM01 diff](https://github.com/curl/curl/commit/32160cae847b4e42d52edb033615f88b12ce5c05), `json.d`, `getparameter`, `get_args`, tests383–386 | T0 이후 `--json` 개발 행동. T0에 배포된 후보나 외부 이용자의 신규 채택으로 소급하지 않는다. 빌드·테스트를 이번 실행에서 돌린 것은 아니다. |

**반증을 찾은 모집틀과 관측 결과.** 294개 조건 행의 예시·민감도 행을 본 비교와 구분했다. P03의 상수 예시는 T0부터 원격 join 조건에 맞지 않으며 실제 질의는 T0/T1 모두 미확인이다. 넓은 local 해석을 채택한 경우만 후보 변화 1건이다. P04 C는 원본 접속 가능성만으로 새 덤프를 권해 입력 시점·데이터의 동등성을 빠뜨린 **근거 부족 승인 1건**이다. 실제 불일치·피해 발생이나 확정 충돌형 오승인으로 올리지 않는다. 가상 문구에서 확인된 충돌형 오승인은 0건이며, 미전송이므로 실제 승인 실험의 오류율은 없다. S03·S08 C의 전체 승인 제외는 문구 재검 결과이지 새 사용자 정보의 효과가 아니다.

**미확인과 판단을 바꿀 최소 자료.** P04는 기존 dump와 재덤프의 동일 시점·데이터 또는 대체 입력 허용 사실이 필요하다. P08에 늦게 나타난 순회·위치 접근 등을 T0 필수로 넣는 변화는 `N1_retroactive` 보조 조건에만 둔다. 실제 선택 변화와 기술 판정 변화를 연결하려면 같은 후보·판을 채택한 작성자 실행 기록이 더 필요하다. 수락·감사 또는 제공자 문서 한 개로 기술과 행동을 동시에 채점하지 않았다.

## Q6 · 질문의 비용을 실제 관측과 가상 비용으로 나눴는가

**점검한 주장.** 주 대화의 추가 사실·목적 요청→작성자 응답 7쌍과 별도 구현 1쌍을 계산했다. 첫 답까지의 시간, 추가 질문 뒤 답까지의 시간, 전체 대화 경과시간은 다른 관측이다. 가상 I/C의 추가 요청은 0, Q는 답이 온다는 조건에서 최소 1왕복이라는 구조만 비교한다. 예상 대기 시간과 실제 절감 시간은 미확인이다.

**근거 ID·URL·위치.** [actual-roundtrips.json](evidence/actual-roundtrips.json)은 S01·S04 각 3쌍의 두 URL과 시각차를 담는다. C07의 [C-F010058](https://curl.se/mail/archive-2022-01/0058.html) 새 본문의 대상 사용자 질문과 [C-F010061](https://curl.se/mail/archive-2022-01/0061.html) 새 본문의 개발자 사용자 답은 10.973333시간 차다. 기술 입력만 세는 좁은 민감도에서는 이 목적 질문 1쌍을 제외한다. C06의 [C-F020009](https://curl.se/mail/archive-2022-02/0009.html) JSON 연결 이유 질문과 [C-F020010](https://curl.se/mail/archive-2022-02/0010.html) 개발 판단 답은 0.033611시간 차이며 별도 구현 열에 둔다. 이 쌍은 달력으로 30일 안에도 있지만 주 대화와 중복 산입하지 않는다.

**반증을 찾은 모집틀과 관측 결과.** PostgreSQL의 응답자→작성자 직접 회신 9쌍을 [clarification-cost-audit.json](streams/postgres/clarification-cost-audit.json)에서 재검했다. 감사·설명 뒤 자발 고지를 완료된 추가 사실 질문으로 세지 않아 전역 정의에서 산입 0쌍이다. 후보 선택에 관계없는 정보의 가능성은 P01의 data entry 고지, P08의 추가 목표에서 찾았으나 그 발생 시점과 원 목표 동일성은 미확인이다. 이미 충분한 예는 P01, 조건부로 안전한 범위만 설명하는 예는 C04, 시간이 지난 뒤 요구 표현이 넓어진 예는 P08이다. C04는 바이트 분기 설명이 가능해도 추가 문자 원인의 해결·사용 보고는 없다. 이 표본에서 **조건부 답만이 실제 해결을 만들었다는 인과 사례는 확인하지 못했다**. 무응답을 실패로 바꾸어 비용을 과장하지 않는다.

**미확인과 판단을 바꿀 최소 자료.** 61은 중복 제거한 외부 원문 저작 수이며 도구의 총 HTTP 요청·재시도·캐시 접근 수도, 사용자의 원문 클릭 수도 아니다. 링크 수는 `strategy.csv`의 문구 대리량이다. 이 값으로 읽기 시간이나 추천의 경제효과를 추정하지 않는다. 실제 질문 비용과 이득을 비교하려면 질문을 받은 시각·읽은 시각·작성자 답·다음 행동을 같은 사용자 경로에서 관측한 자료가 필요하다. 현재는 각 메시지 쌍의 달력 간격만 확인한다.

## Q7 · 다른 직종의 규칙과 반례를 제한된 범위에서 옮겼는가

**점검한 주장.** 도서관과 공공 통계기관에서 각각 규칙과 실제 관측을 짝지었다. 질문을 좁히면 도움이 될 수 있지만 질문이 해석·회상·응답 주의를 바꿀 수도 있다. 어느 관점의 편익인지 구분하고 이를 소프트웨어 채택 효과로 환산하지 않는다.

| 분야·관점 | 근거 ID·URL·정확한 위치 | 반증에서 확인한 것과 적용 한계 |
| --- | --- | --- |
| 도서관의 목적 확인·자료 안내 | [X-L1 RUSA 지침](https://www.ala.org/sites/default/files/rusa/content/Guidelines%20for%20Behavioral%20Performance%20of%20Reference%20and%20Information%20Service%20Providers%202023.pdf), §3.3–3.5·§4.1–4.9·§6.1–6.5; [X-L2 실제 chat 관측](https://ils.unc.edu/MSpapers/2957.pdf), pp.27–35 방법·pp.39–44 사례·pp.45–47 논의 | Mexico 자료형식 질문은 후보를 좁히지 못했으나 검색 숙련도 정보를 얻었다. 따라서 후보가 안 바뀌었다는 이유만으로 질문의 모든 편익을 0으로 만들지 않는다. Ingenta는 기존 특정 논문 접근 목적의 명확화다. |
| 도서관의 비용·성공 판독 | X-L2 pp.41–42의 Long Island 안내, p.32의 성공 정의 수정 | 약 50분은 전체 상담 경과시간이며 연결 끊김·질문 난도 등이 함께 있었다. 질문 한 번의 지연 효과로 쓰지 않는다. 감사 뒤 다음 행동이 남은 사례는 감사=성공 분류의 반례다. |
| 통계기관의 해석·회상 점검 | [X-S1 Census Appendix A2](https://www.census.gov/about/policies/quality/standards/appendixa2.html), Cognitive Interviews·Debriefing; [X-S3 면접자 교육](https://www.census.gov/content/dam/Census/newsroom/press-kits/2022/aapor/20220511-aapor-presentation-training-the-researchers-cognitive-interviewer-training.pdf), slides3–4·7 | 일부 문항도 문맥을 유지하고 이 문항에서 용어가 무엇을 뜻했는지 확인한다. 면접은 주의·협조 자체를 바꿀 수 있다. X-S1의 최초 발행일은 미확인이므로 제외 민감도를 함께 둔다. |
| 통계기관의 실제 변화와 반응성 | [X-S2 CPS 보고서](https://www2.census.gov/library/working-papers/2025/adrm/cbsm/rsm2025-03.pdf), §2.3.1–2.3.2·§3.2.1–3.2.5·§3.3.2 인쇄 p.3-18/PDF p.34·Appendix B1/B2 | 기간 이해 뒤 1개월→2개월 응답 변화가 있고, 기준기간 회상 probe가 여러 기간을 섞어 혼란을 만들어 2차에서 수정된 반례가 있다. P636은 가정형 취업 가능을 실제 제안 부재로 해석했다. 측정 정의를 사용자의 자연어 목적보다 무조건 우선하는 규칙으로 옮기지 않는다. |

**반증을 찾은 모집틀과 관측 결과.** X-L2의 공개 대화 발췌, X-S2의 관측·부록, X-S3의 반응성 논의를 함께 읽었다. X-L3의 당사자 회고, X-E2의 익명 회고는 핵심 최소수 밖에 두었다. X-E1의 Pig War는 원문이 가상 사례라고 표시해 실제 관측에서 제외했다. [crossdomain-review.json](streams/sqlite/crossdomain-review.json) CR1–CR7을 통해 Mexico의 검색 숙련도 편익과 모집/면접 날짜·정확한 절을 보정했다. X-S2는 공식 발행 2025-03-07, 내부 표지 2024-10, 실제 면접 2023–2024를 구분하며 소프트웨어의 2022 T0 후보 자료로 쓰지 않는다.

**미확인과 판단을 바꿀 최소 자료.** 공개 발췌만으로 도서관 전체 익명 원장을 다시 코딩할 수 없고, 두 분야의 질문은 무작위 배정 비교가 아니다. 목적 자체를 질문이 새로 만들었다는 직접 관측은 **미확인**이다. 현재 관측은 기존 목적 명확화와 해석·회상·주의 변화다. 목적 생성 주장을 하려면 질문 전 목적, 면접자의 새 목적 제안, 당사자가 그것을 새로 채택했다는 시간순 발화를 같은 사건에서 확보해야 한다. 이 구분은 다음 조사의 조건이며 이미 발견한 효과라는 주장이 아니다.

## Q8 · 어떤 규칙을 설계자에게 넘기며 어디서 멈추는가

**점검한 주장.** 24개 사례를 유지한 기술 통계와 코딩 민감도를 넘긴다. 이미 적힌 사실 8건을 Q의 성공으로 세지 않고, 엄격 신규 값 0건·판정 변화 0건과 16건의 미확인을 함께 제시한다. 원판 미확인으로 코딩된 사례가 0이라 그 코드의 성립/불성립 양극단 수는 같지만, Q1의 증거 수준 차이는 여전히 남는다. 추가 교차 보강 18건과 미노출 23건 분모를 별도로 둔다.

**근거 ID·URL·위치.** [metrics.json](evidence/metrics.json)의 `subsets`, `unknown_original_extremes`, `weak_author_value_sensitivity`와 [strategy-summary.csv](strategy-summary.csv)가 분모를 재현한다. 질문 없이 설명 가능한 P01은 [P-S01](https://www.postgresql.org/message-id/-YOusR_95io8hzFnscly6yFVD7ssgOhG0dnTRskP2hU2TaCDS29X2XIxNaYAKjZjYdYYYVF87qlFcmzDHIgw-9ooalVT6DkLDnd6cLqHCko%3D%40protonmail.com) p1–13의 SQL·결과와 [P-D01](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ddl.sgml) L3178–3335의 상속 조회 방향을 연결한다. 조건부 링크의 범위는 Q3의 C-D04/C-D05, 원판에 이미 값이 있는 재질문은 Q2의 C-R01/C-R03, 한 변수만 알아도 해결되지 않는 한계는 Q4의 P03와 Q5의 P04에서 추적할 수 있다.

**반증을 찾은 모집틀과 관측 결과.** 전체 24, 원판 연결 24, 엄격 미노출 23, 추가 교차 보강 18, 직접 답만 0, 공급자 겸 질문자 C06/C07 제외 22의 하위분모를 비교했다. I/C의 제한 성립을 전체 승인으로 올리지 않았고, S03 C를 넓게 허용할 때 C 승인 3이라는 별도 민감도를 보존했다. 엄격 신규 값 0이라는 결과를 ‘질문은 쓸모없다’로 해석하지 않는다. 공개 자료에 답이 남지 않았거나, 봉인 질문이 이미 적힌 사실을 되묻거나, 필요한 변수보다 좁았을 수 있다. 같은 발신자·프로젝트·재게시를 독립 사용자나 채택으로 늘리지 않았다.

**설계 제안과 그 적용 조건.** 다음 네 선택지는 관측에 근거한 연구자의 규칙 제안이며 배정된 사용자 실험의 우월성 결론이 아니다.

1. 최초판이 필요한 조건을 이미 말하고 후보의 같은 판 근거가 그 사용을 지지하면, 그 범위를 밝히고 근거 링크를 바로 준다. P01의 조회 방향 설명이 해당한다.
2. 한 변수로 나뉘는 두 사용 또는 사용/보류가 짧고 각 분기의 근거가 확보되면, 조건부 링크를 준다. C04는 전송 바이트 분기를 설명할 수 있으나 추가 문자 원인 해결은 남긴다.
3. 그 한 값이 실제 판정이나 다음 행동을 바꾸고 최초판에 없다면, 변수 하나를 요청하는 안을 남긴다. 이 표본에서 정확한 봉인 질문의 신규 값 회수 이득은 관측하지 못했으므로 비용 대비 이득의 크기를 붙이지 않는다.
4. 후보가 없거나 한 답을 얻어도 다른 필수 조건·판·입력 경계가 남으면, 남은 조건을 표시하고 보류한다. C08의 후보 부재와 P04의 입력 경계가 이 한계를 보여준다.

**미확인과 판단을 바꿀 최소 자료.** 실제 I/C/Q의 전달·응답·동일 후보 실행을 추적한 비교 자료가 생기기 전에는 실제 인과효과·시간 절감·추천의 경제효과를 추정하지 않는다. 독립 가림 재판독은 코딩 안정성을, 동일 원판의 실제 전략 비교는 사용자 효과를 확인하는 서로 다른 후속 조사다. 직접 답 분모 0의 비율은 0%가 아니라 해당 없음으로 유지한다.

## 수용 근거에 넘길 통제 이탈과 재현 경로

| 조건 | 자체 점검 판단 | 인계할 근거와 남은 행동 |
| --- | --- | --- |
| 전체 24건 모두 후속·답 요약을 전혀 보지 않은 사전 판정 | **met=false** | S01의 검색 답 문장 노출을 `t0-seal.json.exposure_exclusions`에 보존했다. 전체 24와 엄격 23을 함께 보고한다. 이미 발생한 노출을 사후 보강으로 충족 처리하지 않는다. |
| PostgreSQL 8건 모두 원형 RFC822·서버 Received 확보 | 미확보를 명시 | 공식 raw/미러 시도는 실패했다. P04의 실질 전문과 P05 전체 인용의 해시 일치, SQLite/curl 원장 증거로 추가 교차 18건을 따로 제시한다. 이를 24개 암호학적 제출 인증으로 쓰지 않는다. |
| 독립 가림 중복 판독 | 수행하지 않음 | 같은 작성자의 순차 판독과 사후 표적 동료 검토를 구분한다. P03 이견·Q7 날짜 및 편익 교정·S03/S08 승인 정의 조정을 삭제하지 않는다. |
| 자료 최소수·입력 불변·분모 일관성 | 기계 검산으로 재현할 항목 | `verify.py`는 입력 해시·행·출처 참조·분모·표 형식을 검사한다. 원문 완독·역사적 진실·인과효과를 기계적으로 보증하지 않는다. 최종 실행 결과는 실행 영수증에서 확인한다. |

재현 명령은 저장소 루트에서 다음과 같다. 집계 프로그램은 파생 파일을 재생성하므로 고정 결과 커밋의 별도 작업 트리에서 실행하고 diff를 검토한다. 원문 추가 판독 없이 동일 코딩을 재집계하는 명령이다.

```bash
python docs/workstreams/research/AF-RES-026/assemble_results.py
python docs/workstreams/research/AF-RES-026/summarize.py
python docs/workstreams/research/AF-RES-026/verify.py --require-report --record evidence/verification.json
```

이 문서의 작성 자체를 위 명령의 최종 성공 영수증으로 사용하지 않는다. `evidence/acceptance-evidence.json`은 조건별 충족 여부와 남은 입력을, 최종 실행 영수증은 실행 시각·명령·로컬 HEAD·입력 해시·검사 결과를 기록한다. 원격 고정 SHA 파일 재읽기는 별도 커밋 영수증으로 확인한다. 최종 HANDOFF 작성과 상태 판정은 이 자체 점검 및 수용 근거가 커밋되고 원격에서 확인된 뒤 진행한다.

## 추가 인용·표현 점검

S03의 최초 missing_variable 요약은 legacy를 끌 수 없다는 방향이어서 OFF 유지 필수를 묻는 봉인 Q/R3와 반대였다. 원본을 보존하고 RESULT/행렬의 표시만 교정했다. OFF가 선택 가능하다고 단정하지 않고 필수 여부 미확인으로 쓴다. [교정 근거](adjudication-overrides.json)의 S03과 [봉인 Q](frozen-responses.jsonl)를 대조한다.

[SQLite 인용 감사](streams/sqlite/citation-coverage.json)는 기술 지지와 짧은 문구 실제 링크를 분리해16문구 중6인용 누락을 기록했다. [curl 명제 감사](streams/curl/citation-coverage.json)는 C01/C의 JS 비실행→일반 대체 불가능, C02/I·C의 외부서비스/비교 필수성이라는 범위 확대를 발견했다. 세 문구 모두 원래 보류이며 승인/진전 수치를 사후 바꾸는 새 사실이 아니다. 두 감사는 축이 달라 하나의 인용 완결률로 합산하지 않는다.

## 실제 검산 영수증

고정 결과 `ed14e806a5a7bf4e6195fd12024c482d31768449`에서 보고서 포함 자체 검산은18 PASS/0 FAIL/1 SKIP, 종료코드0이었다. SKIP은 수정 주석을 허용한 현재 SCOPE 해시이며, 봉인9파일은 모두 일치했다. [verification](evidence/verification.json)은 실제 입력해시와 검사HEAD를 포함한다. 별도 [session check --fetch](evidence/session-check-receipt.json)는 PASS/remote_checked, 통합 `21c517691e8d8882f0e66ef262b32fe3ad39b630`의 계약과 동일, 소유밖변경0·오류0을 확인했다. 통합SHA는검사시점의계약확인이며이번차수다른연구결과를분석입력으로추가한것이아니다. 후속수용근거/인계문서는이전실행에포함됐다고하지않는다.

공통 검사는 [두 시도와 원문 영수증](evidence/required-checks/README.md)에 보존했다. 첫 partial clone의 과거 객체 누락으로 Git bundle 단계가 실패했고, 공개 저장소를 필터 없이 다시 복제한 같은 ed14에서55개 단위검사·test/demo·export·Git bundle 복원과 공통5명령이 통과했다. 공통코드는 수정하지 않았다. common check-all은 활성 세션0으로 원격 세션을 검사하지 않았으므로, 이를 앞의 explicit manifest --fetch와 혼합하지 않는다. [검증 범위 요약](evidence/verification-summary.json).
