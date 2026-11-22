# AF-RES-026 · 즉답·조건부 답·한 변수 질문·보류의 실제 예시

아래 인용은 공개 질문을 입력으로 연구자가 작성한 **가상 I/C/Q**다. 실제 게시자에게 전송하지 않았다. 후속을 읽기 전에 봉인한 [`frozen-responses.jsonl`](https://github.com/laadkke-arch/agentflow-open/blob/68fc97fadceb46f9945a71fcc53730e29f6c62bf/docs/workstreams/research/AF-RES-026/frozen-responses.jsonl)의 문자열을 수정 없이 옮겼다. 원래 잘못 가른 조건도 보존했으며 개선 문구로 교체하지 않았다.

각 문구는 공백과 URL을 포함한 Unicode 문자 수로 300자 이하다. 한 사례의 세 전략은 같은 최초판·같은 후보 집합·같은 당시 원문 최대 두 곳을 공유한다. I는 그중 한 사용 또는 보류를 말하고, C는 한 갈림 조건으로 두 사용 또는 보류를 말하며, Q는 변수 하나를 묻는다. 이 문서는 해당 예시에 필요한 전략 1~2개만 인용한다. 문구의 태그 URL과 원장에 고정된 exact SHA는 같은 비교판을 가리킨다. 저자가 사용한 판이 미상인 경우 비교판을 실제 설치판으로 간주하지 않는다.

**기술적으로 맞는 제한적 설명, 조건부 사용 설명, 원 목표의 사용 승인, 작성자의 실제 행동은 서로 다른 관측이다.** 안전하게 보류한 답을 사용 승인으로 세지 않는다. 실제 대화의 질문 수·지연을 이 가상 문구의 비용이나 효과로 대입하지 않는다. 전체 24건의 분모와 판정은 `strategy.csv`, `judgments.csv`, `followups.csv` 및 `RESULT.md`에서 확인한다.

| 예시 | 고정 문구 | 보여 주는 경계 |
| --- | --- | --- |
| C03 | I | 이미 적힌 버전·현상만으로 제한된 동작 설명 가능 |
| C04 | C | 두 입력 처리의 차이는 설명 가능하나 추가 문자 진단은 미완 |
| S05 | C·I | 공식 원문 하나로 두 mutex 조건 설명 가능; 전체 안전성·성능은 보류 |
| S04 | Q·C | 필요한 변수라도 저자의 주장과 코드·로그가 충돌하면 값 확정 불가 |
| C08 | I | 후보가 없는 질문도 원 분모에 남기고 원인 승인 보류 |
| P04 | C | 접속 가능성으로만 분기하면 기존 덤프의 입력 경계를 바꿀 수 있음 |
| C01 | Q | 최초판에 적힌 관측 주체를 다시 묻는 판독 오류 |
| C05 | 실제 대화 대조 | 추가 질문 없는 조건부 설명 뒤 결정 수용; 새 구현 성공과 구별 |

## 1. C03 — 즉답으로 동작의 뜻을 설명할 수 있었던 경우

원 작성자는 **curl 7.55.1**을 명시하고, POST 완료까지의 시간과 첫 업로드 바이트부터 마지막 바이트까지의 시간을 이미 구별했다. 요청은 이 현상이 버그인지 다른 계산 논리인지 이해하려는 것이었다. 새 속도 출력 기능을 반드시 구현하라는 요구로 넓히지 않는다. 근거: **C-R03**, [최초 요청](https://curl.se/mail/archive-2022-01/0024.html) L33–43.

**미전송 봉인 문구 — C03/I, 공백·URL 포함 130자**

> 7.55.1의 평균 업로드 속도는 업로드 바이트/시작 이후 경과시간입니다. 서버처리 대기를 뺀 속도라고 해석하면 안 됩니다. https://github.com/curl/curl/blob/curl-7_55_1/lib/progress.c

**동일 후보와 당시 근거.** A는 기본 meter의 평균 분모를 설명하는 사용으로, **C-D09** [7.55.1 `progress.c`](https://github.com/curl/curl/blob/8839c05fba1f8415eec17eff8ac60cc3a50eb51e/lib/progress.c)의 `Curl_pgrsUpdate` L375–394 및 표시부 L560–570을 연결했다. B는 진행량을 보이는 bar이며 **C-D10** [같은 판 `progress-bar.d`](https://github.com/curl/curl/blob/8839c05fba1f8415eec17eff8ac60cc3a50eb51e/docs/cmdline-opts/progress-bar.d) L5–11이다. B를 순수 업로드 구간의 평균속도 대체로 승인한 것은 아니다. 인용한 I는 A의 계산 의미만 설명한다.

**실제 후속과 한계.** **C-F010026**, [유지관리자 첫 답](https://curl.se/mail/archive-2022-01/0026.html)의 새 본문은 업로드/다운로드별 타이머가 없고 서버 작업 대기가 평균에 영향을 준다고 확인한다. 추가 조건을 먼저 묻지 않았다. 30일 창에 원 작성자의 수정·실행 결과는 연결되지 않았다. 이 예시는 최초판으로 설명할 수 있었다는 근거이며, 가상 I가 실행 성공이나 시간 절약을 만들었다는 근거가 아니다.

## 2. C04 — 한 조건으로 두 사용을 설명해도 진단이 끝나지 않는 경우

명령줄 `-d`로 보낼 때는 되지만 같은 데이터를 임시파일에 복사해 `-d @tmp.dat`로 보내면 추가 문자가 생긴다는 요청이다. 실제 파일과 전송 바이트는 제공되지 않았다. 근거: **C-R04**, [최초 요청](https://curl.se/mail/archive-2022-01/0027.html) L35–44. PHP `trim` 관련 정확한 위치는 L43–44이며, 봉인 원장에 있던 위치 오류는 `streams/curl/field-corrections.json`에서 별도 보정했다.

**미전송 봉인 문구 — C04/C, 공백·URL 포함 248자**

> 줄바꿈을 제거할 파일 입력이면 -d @file, 바이트를 그대로 보낼 입력이면 --data-binary @file입니다. 어느 쪽이든 추가 문자의 원인은 별도 확인이 필요합니다. https://github.com/curl/curl/blob/curl-7_81_0/docs/cmdline-opts/data.d https://github.com/curl/curl/blob/curl-7_81_0/docs/cmdline-opts/data-binary.d

**동일 후보와 당시 근거.** A와 B는 각각 **C-D04** [7.81.0 `data.d`](https://github.com/curl/curl/blob/801bd5138ce31aa0d906fa4e2eabfc599d74e793/docs/cmdline-opts/data.d) L14–34의 파일 CR/LF 제거와 **C-D05** [같은 판 `data-binary.d`](https://github.com/curl/curl/blob/801bd5138ce31aa0d906fa4e2eabfc599d74e793/docs/cmdline-opts/data-binary.d) L10–23의 바이트 보존이다. 이는 당시 비교판의 입력 처리 차이에 대한 조건부 설명이다. 원 작성자의 실제 curl 버전은 미상이다.

**실제 후속과 한계.** **C-F010028**, [실제 첫 답](https://curl.se/mail/archive-2022-01/0028.html)의 새 본문은 `od` 등으로 추가 문자의 정체를 확인할 수 있는지 물었다. 봉인한 Q의 변수인 “CR/LF를 보존해야 하는가”와 다른 질문이다. 작성자 재응답은 30일 창에서 연결되지 않았다. CR/LF 보존 여부가 밝혀져도 문자의 발생 원인과 전체 요청의 동등성은 남으므로, 이 C가 설명한 분기와 원인 해결을 같은 수로 세지 않는다.

## 3. S05 — 공식 링크 하나로 두 조건을 설명하되 전체 안전성은 보류하는 경우

원 작성자는 같은 연결에서 main thread가 다른 작업을 하는 동안 별도 thread가 statement의 reset/clear를 수행해도 안전한지 물었다. 성능 개선은 바람이고 실효 threading mode는 미기재였다. 근거: **S-S05**, [최초 artifact](https://sqlite.org/forum/artifact/a57b1695d49a70c88481c41cc46392a98be29a30a8d32fef693dc813b90b7051)의 W 본문, 처음 두 단락 및 마지막 질문.

**미전송 봉인 문구 — S05/C, 공백·URL 포함 182자**

> serialized이면 연결·statement 접근을 SQLite가 직렬화합니다. multi-thread/no-mutex이면 같은 연결을 앱이 직렬화해야 합니다. 어느 쪽도 성능 향상의 증거는 아닙니다. https://github.com/sqlite/sqlite/blob/version-3.37.1/src/sqlite.h.in

**미전송 봉인 문구 — S05/I, 공백·URL 포함 164자**

> 현재 설정만으로 안전 승인은 보류합니다. 같은 연결을 동시에 쓰므로 실제 threading mode를 확인해야 하며, mutex 안전성이 성능 향상을 보장하지는 않습니다. https://github.com/sqlite/sqlite/blob/version-3.37.1/src/sqlite.h.in

**동일 후보와 당시 근거.** A는 SQLite의 serialized mode 아래 API 접근, B는 multi-thread/no-mutex 환경에서 앱이 같은 연결 접근을 직렬화하는 사용이다. 둘 다 **S-D01**, [3.37.1 `sqlite.h.in`](https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/src/sqlite.h.in)의 `SQLITE_CONFIG_MULTITHREAD` L1761–1773와 `SQLITE_CONFIG_SERIALIZED` L1775–1789에 있다. 두 갈래가 한 원문에 있으므로 C의 링크도 하나다. 최초판에 실제 사용 버전이 없어 3.37.1은 비교판이다.

**승인하지 않은 범위.** 문서는 연결·statement 접근의 mutex 계약을 설명한다. 이 사실만으로 여러 호출의 논리적 작업 순서·statement 수명·전체 재사용 안전성이나 성능 향상이 입증되지는 않는다. 원 작성자가 single-thread 빌드나 다른 설정을 썼는지도 확인되지 않았으며, 해당 문서 L1749–1759의 single-thread 제약을 위 두 갈래가 없앤다고 읽으면 안 된다. C는 mode별 계약 설명으로 성립하고 원 목표의 전체 안전성은 I처럼 보류한다.

**실제 후속과 한계.** 같은 **S-S05**의 [답 artifact `ad1beab8…`](https://sqlite.org/forum/artifact/ad1beab8b38eeef8c10c8d0c27ae7c75549dafd1e0c71c804b89bc87fe66da0c) W-body L1–3은 serialized 또는 non-null `sqlite3_db_mutex` 조건을 제시했다. 이는 제3자의 조건 설명이며 작성자의 실제 mode 값이 아니다. 작성자 재응답·사용 결과는 30일 창에서 관측되지 않았다. 따라서 “공식 링크 하나로 조건 두 가지를 설명할 수 있음”과 “링크 하나로 실제 안전한 구현이 완성됨”을 구분한다.

## 4. S04 — 한 변수를 물을 이유가 있어도 공개 답의 충돌이 남는 경우

강제 재시작 전 출력한 rowid보다 재부팅 뒤 rowid가 작다는 요청이다. SQLite3.37.0, iPhone6S/iOS12.3, DELETE journal, FULL synchronous 설정은 적혀 있지만 손실 행의 COMMIT 성공 반환은 적혀 있지 않았다. 근거: **S-S04**, [최초 artifact `feed150c…`](https://sqlite.org/forum/artifact/feed150c20f8acd84f4b7ce548a8a2b990a2f1bd8f6e4793c8a0b49673d7e87f) W-body L1–6 및 L14–21.

**미전송 봉인 문구 — S04/Q, 공백·URL 포함 45자**

> 사라진 행을 포함한 트랜잭션의 COMMIT가 강제 재시작 전에 성공을 반환했나요?

**미전송 봉인 문구 — S04/C, 공백·URL 포함 213자**

> COMMIT 전이면 rowid 출력만으로 보존을 기대할 수 없습니다. 성공 COMMIT 뒤라면 장치·sync 경계 원인을 더 확인해야 합니다. https://github.com/sqlite/sqlite/blob/version-3.37.0/src/sqlite.h.in https://github.com/sqlite/sqlite/blob/version-3.37.0/src/pager.c

**동일 후보와 당시 근거.** A는 COMMIT 이전 INSERT/rowid를 미확정 상태로 해석하는 사용, B는 성공 COMMIT 뒤 손실이면 sync/OS 경계를 더 조사하는 보류다. **S-D06** [3.37.0 `sqlite.h.in`](https://github.com/sqlite/sqlite/blob/315e3122c37b2dbe0fb7b3a4c3b9b6961e3bda96/src/sqlite.h.in) `Last Insert Rowid`, 특히 L2476–2477은 rowid의 INSERT 성공 의미가 후속 rollback과 별개임을 설명한다. **S-D07** [같은 판 `pager.c`](https://github.com/sqlite/sqlite/blob/315e3122c37b2dbe0fb7b3a4c3b9b6961e3bda96/src/pager.c) L3503–3549는 sync 설정의 의미를 뒷받침하며 실제 장치의 성공 COMMIT를 증명하지 않는다.

**실제 후속의 값과 충돌.** 작성자는 [artifact `2070eae6…`](https://sqlite.org/forum/artifact/2070eae6fd0fa53a44a8ac87b946dd31facab9d181d29f4a304c74c5846246a4) W-body L1–2에서 행마다 다른 트랜잭션을 쓰며 commit된 데이터도 사라진다고 말했다. 하지만 [후속 재현 편집판 `8a24d27a…`](https://sqlite.org/forum/artifact/8a24d27a64786c26fcee69222d94ce3e0d88c58126bec7aedcd22bff513139d6) W-body L7–23에는 BEGIN·INSERT·close가 있고 COMMIT는 보이지 않으며 L35에는 commit 실패 로그가 있다. 이 자료들이 앞서 설명한 FMDB 원앱과 같은 완전 실행인지도 확인되지 않았다.

이 충돌은 작성자의 말이 거짓이라고 판정할 근거가 아니다. 다만 **성공을 반환한 COMMIT라는 봉인 변수는 엄격히 채워지지 않았다.** 실제 질문→답 3쌍은 언어/wrapper/재시작 방식, transaction 단위, 재현 세부를 묻고 답한 것으로, 가상 Q를 실제 전송한 기록이 아니다. 후속 답을 얻었다는 사실과 갈림 조건을 확정했다는 사실을 분리해야 한다. 원인·장치 결함·해결 여부도 여전히 미확인이다.

## 5. C08 — 후보가 없을 때 원 질문을 유지하고 보류하는 경우

명령줄 curl POST는 성공하고 Chrome97/Windows64bit 확장 Fetch는404를 반환한다는 요청이다. 실제 URL·headers·body·서버 응답은 없다. 보안 비활성 재시작도 실패했다고 적혀 있지만 그것이 원인이라는 증거는 아니다. 근거: **C-R08**, [최초 요청](https://curl.se/mail/archive-2022-01/0066.html) L33–45.

**미전송 봉인 문구 — C08/I, 공백·URL 포함 79자**

> curl 성공과 Chrome의 404만으로 원인을 정할 수 없습니다. 두 요청의 URL·헤더·본문과 서버응답이 없어 해결책 승인을 보류합니다.

**동일 후보와 한계.** 봉인 후보 집합은 빈 배열이다. 따라서 이 I에는 해결책을 뒷받침하는 링크가 없고, 원인이나 특정 수정을 승인하지 않는다. Q의 최종 URL 일치 여부를 알아도 다른 요청 조건이 남는다. 후보가 없다고 질문을 빼거나 다른 성공 사례로 교체하지 않았다.

**실제 후속.** root+30일인 2022-02-24 22:24:49 UTC까지 연결된 첫 답은 관측되지 않아 우측 검열했다. 같은 표시 작성자의 [2월25일 DOM 질문](https://curl.se/mail/archive-2022-02/0048.html), **C-F020048**은 범위 밖 시점이고 원 Fetch404와 동일 구현이라는 명시 연결이 없어 해결 후속으로 쓰지 않았다. 무응답을 거절·실패로 코딩하지 않는다.

## 6. P04/C — 분기 변수만으로 기존 입력을 바꿀 수 있다고 오인한 경우

원 작성자는 pg_dumpall14.1로 구버전 클러스터에서 만든 **기존 다중 DB·roles 덤프 파일**에서 DB 하나를 복원할 방법을 물었다. 근거: **P-S04**, [최초 Message-ID 원문](https://www.postgresql.org/message-id/YdQFiQrF/2GXgxTI%40pureos) p2–3, web L21–26.

**미전송 봉인 문구 — P04/C, 공백·URL 포함 259자**

> 원본에 접속할 수 있으면 단일 DB pg_dump를, 파일만 남았다면 분리 환경에 전체 복원 후 해당 DB의 pg_dump를 검토하세요. https://github.com/postgres/postgres/blob/REL_14_1/doc/src/sgml/ref/pg_dump.sgml#L36-L86 https://github.com/postgres/postgres/blob/REL_14_1/doc/src/sgml/ref/pg_dumpall.sgml#L780-L801

**동일 후보와 당시 근거.** A는 원본에서 단일 DB를 다시 덤프하는 경로로 **P-D06**, [REL_14_1 `pg_dump.sgml`](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/pg_dump.sgml) L36–87을 사용했다. B는 기존 전체 SQL을 별도 환경에 복원한 뒤 대상 DB를 덤프하는 경로로 **P-D05**, [같은 판 `pg_dumpall.sgml`](https://github.com/postgres/postgres/blob/0a455b8d61d8fc5a7d1fdc152667f9ba1fd27fda/doc/src/sgml/ref/pg_dumpall.sgml) L30–68 및 L780–801을 사용했다.

**잘못 가른 조건.** 원본에 다시 접속할 수 있다는 사실만으로 새 덤프가 기존 파일의 시점·내용을 대체해도 된다는 조건은 충족되지 않는다. 원 목표는 이미 만들어진 파일을 입력으로 정했다. A를 원 요청의 대안으로 허용하려면 새 덤프로 바꿔도 되는지와 필요한 동등성 근거가 더 필요하다. B도 역할·종속성·복원환경의 완전성을 별도로 확인해야 한다. 문서가 각 명령의 기능을 설명한다는 사실만으로 이 요청에서 대체 경로의 모든 조건을 인용한 것은 아니다.

현재 이 C는 **조건이 부족한 대안 제시**로 기록한다. 실제 손상·실패가 확인된 오승인으로 올려 세지 않는다. 이 발견은 후속 작성자 정보의 이득이 아니라 최초판 재독 보정 **P-COR04**다.

**실제 후속과 한계.** **P-S04**의 [Tom Lane 답](https://www.postgresql.org/message-id/4024278.1641308516%40sss.pgh.pa.us) p3–5, web L28–34는 flat SQL이라는 형식을 설명하고 앞으로 개별 DB를 덤프하는 방법과 이미 남은 파일을 편집하는 방법을 구별한다. 작성자의 재접속 값·채택·실행 결과는 30일 창에 없었다. 실제 답변의 존재가 봉인 C의 누락 조건을 채워 주지는 않는다.

## 7. C01/Q — 이미 적힌 관측 주체를 다시 묻는 경우

원문은 브라우저에 표시된 Request cookies를 얻고 싶다고 했고, extension→XHR/Fetch→browser/network/headers라는 시험 순서도 적었다. 근거: **C-R01**, [최초 요청](https://curl.se/mail/archive-2022-01/0002.html) L33–42.

**미전송 봉인 문구 — C01/Q, 공백·URL 포함 54자**

> 확인하려는 쿠키는 브라우저가 실제 보낸 요청의 것인가요, curl이 재현해 보낸 요청의 것인가요?

**왜 재질문인가.** 브라우저의 실제 요청이라는 주체가 원문에 있다. 다른 도구로 값을 얻고 싶다는 말에서 curl 재현 요청을 별도의 목적 후보로 만든 것은 연구자의 판독 문제다. 실제로 부족했던 것은 당시 브라우저 쿠키 획득법을 확인할 후보·증거였으며 관측 주체가 아니었다. 이 Q가 새 대체 목표를 만들 위험을 별도 보정에 남겼다. 공개 작성자가 이 가상 질문을 받아 목표를 바꿨다고 주장하지 않는다.

**동일 후보와 당시 근거.** A는 curl 자신의 송신 헤더 관측으로 **C-D02**, [7.80.0 `verbose.d`](https://github.com/curl/curl/blob/9e560d11aad028de74addc0d1edfefa5667884f4/docs/cmdline-opts/verbose.d) L10–23이다. B는 브라우저 JS 실행을 curl로 대체하는 경로를 보류하며 **C-D12**, [같은 판 FAQ](https://github.com/curl/curl/blob/9e560d11aad028de74addc0d1edfefa5667884f4/docs/FAQ) §3.14 L602–624를 연결한다. A가 기술적으로 존재한다는 것과 원 목적에 적합하다는 것은 다르다.

**실제 후속과 한계.** **C-F010005**, [첫 답](https://curl.se/mail/archive-2022-01/0005.html)은 브라우저 도구·쿠키 export 등의 대안을 제시했고 frozen 변수를 묻지는 않았다. **C-F010006**, [작성자 후속](https://curl.se/mail/archive-2022-01/0006.html)은 `curl -c`에서 빈 cookiejar를 얻었다는 시도와 브라우저 XHR/Fetch 쿠키 목적을 말한다. 이는 frozen A의 `-v` 실패도, 새 주체값 회수도, 성공 보고도 아니다. 보정은 `streams/curl/t0-corrections.json`과 통합 `evidence/T0-review.md`에 있고 봉인 Q는 그대로다.

## 8. C05 — 실제 조건부 설명 뒤 결정 수용을 관측한 대조 사례

이 절은 가상 I/C/Q의 효과 사례가 아니라 **실제로 오간 공개 대화**의 대조다. 원 작성자는 Content-Disposition의 절대경로가 저장위치를 바꿀 수 있는지와 `-OJ`의 이름 처리 대안을 물었다. 근거: **C-R05**, [최초 요청](https://curl.se/mail/archive-2022-01/0032.html) L39–45.

**C-F010033**, [유지관리자의 첫 답](https://curl.se/mail/archive-2022-01/0033.html)은 서버 경로를 제거한다고 설명하고, Content-Disposition이 없으면 `-O`가 URL 기반 이름을 사용한다는 조건을 알려 줬다. 이 답에는 기술 근거로 연결하는 문서 링크가 없었으며 추가 질문도 없었다. **C-F010037**, [작성자의 다음 답](https://curl.se/mail/archive-2022-01/0037.html)은 설명을 충분하다고 수용하고, 빈 임시 디렉터리에서 받은 뒤 필요시 move/rename하는 기존 workflow를 밝혔다. 새 명령을 실행해 성공했다는 보고는 아니다.

문서 링크는 그 다음 **C-F010038**, [문서 수정 보고](https://curl.se/mail/archive-2022-01/0038.html)에 나왔다. **C-IM02**, [정정 commit a6f2272](https://github.com/curl/curl/commit/a6f227252cfc80c7c44be395f5a6952221313b74)의 `remote-header-name.d` diff는 root를 참조하며 경로제거·저장위치 설명을 보완한다. 기술 동작은 원래 후보 **C-D13**, [7.81.0 `tool_cb_hdr.c`](https://github.com/curl/curl/blob/801bd5138ce31aa0d906fa4e2eabfc599d74e793/src/tool_cb_hdr.c)의 `parse_filename` L219–289와 대응한다. 문서 수정은 새 기능 구현이나 질문자 실행 성공과 다르다.

따라서 이 사례는 “추가 질문 없는 조건부 설명 뒤 결정 수용”으로 사용한다. **이 조사에서 ‘조건부 링크 하나로 실제 구현이 성공했다’는 관측은 없다.** 가상 C는 전송되지 않았고, 실제 C05 첫 답에는 문서 링크가 없었으며 새 구현 성공도 확인되지 않았다. S05의 한 링크 조건 설명 역시 작성자 mode·실행 결과가 없다.

## 후보가 유지되어도 질문의 모든 가치가 0은 아니다

위 예시는 후보 선택·필수 조건·사용 승인·작성자 행동을 분리한다. 그렇다고 후보가 안 바뀌면 질문의 가치가 반드시 없다는 규칙을 도출할 수는 없다. **X-L2**, [Pellegrino의 공개 도서관 상담 관측](https://ils.unc.edu/MSpapers/2957.pdf), 인쇄 pp.40–41 / PDF 인덱스41–42 / 추출 L954–976의 Mexico 사례에서는 자료 형식을 묻는 질문이 형식별 후보를 좁히지 못했지만 이용자의 검색 숙련도 정보를 얻었다. 사서는 주제어와 검색 방법을 안내했다.

이 반례가 허용하는 전이는 **설명 수준·접근 안내·다음 행동에 정보가 쓰일 수 있음**까지다. 공개된 것은 연구 보고서의 상담 발췌이며, 추가 질문의 인과적 편익·시간 절약·소프트웨어 채택 효과는 입증하지 않는다. C04처럼 원인 진단이 남는 조건부 설명이나 S04처럼 wrapper 사실이 A/B 판정을 바꾸지 않는 대화에서도, 정보의 활용 범위를 후보 변경 하나로 축소하지 않아야 한다. 이는 관측 범위를 구분하는 해석이며 새 개선 문구 제안이 아니다.

## 확인 범위와 재현

원문 인용의 정본은 전역 봉인 SHA `68fc97fadceb46f9945a71fcc53730e29f6c62bf`의 `frozen-responses.jsonl`이다. 예시별 input SHA, 비교판, 후보 ID는 같은 사례 행에서 재현할 수 있다. 후속 사실은 `followups.csv` 및 각 stream의 `case-analysis.jsonl`, 판독 보정은 별도 corrections 파일에 있다. 이번 예시 편집에서 원판·후속 URL과 고정 코드 절을 다시 대조했고, SQLite artifact의 web-reader 접근 실패는 같은 artifact의 공식 `/forum/raw/<ID>`로 확인했다. 원문·사건 최소수는 늘리지 않았다.

아래 검산은 편집상의 동일성 확인이며 전략의 추가 실행 시험이 아니다.

| 사례·전략 | 봉인 문자열 문자 수 | 동일성 |
| --- | --- | --- |
| C03/I | 130 | 봉인 문자열 그대로 |
| C04/C | 248 | 봉인 문자열 그대로 |
| S05/C | 182 | 봉인 문자열 그대로 |
| S05/I | 164 | 봉인 문자열 그대로 |
| S04/Q | 45 | 봉인 문자열 그대로 |
| S04/C | 213 | 봉인 문자열 그대로 |
| C08/I | 79 | 봉인 문자열 그대로 |
| P04/C | 259 | 봉인 문자열 그대로 |
| C01/Q | 54 | 봉인 문자열 그대로 |
