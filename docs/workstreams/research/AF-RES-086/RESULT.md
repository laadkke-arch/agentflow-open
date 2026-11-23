## 표 1 — 원 독자와 원 약속

| 사례·원 독자 | 원 약속과 주소 | 필요한 판·관측창 | 당시 소스·생성물 | 주장 근거 URL | 빠진 약속 |
|---|---|---|---|---|---|
| P3 cibuildwheel — 당시 지원 Python 독자와 지원 종료 Python 독자 | README는 [stable](https://cibuildwheel.pypa.io/en/stable/)·[options/#enable](https://cibuildwheel.pypa.io/en/stable/options/#enable), 지원 종료 Python에는 [1.x](https://cibuildwheel.pypa.io/en/1.x/)를 안내한다. | v3.3.0의 enable 내용과 실제 구계열 내용. 주창 2025-11-11~13 UTC, 양 끝 날짜 포함. | source `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc`; tag runs 30298914·30298916. 1.x run 14073318은 2021년 별도 소스다. | [고정 README L44·53·140](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/README.md#L44), [고정 changelog](https://github.com/pypa/cibuildwheel/blob/63fd63b352a9a8bdcc24791c9dbee952ee9a8abc/docs/changelog.md) | 구판 유지 기간, 고정 patch의 영구 보존, 두 경로의 가동 보장 기간은 명시하지 않았다. 고정 v3.3.0을 지금 재현하려는 목적은 연구 가정이다. |
| R1 archive — 패키지 1.1.12 문서를 찾는 독자 | DESCRIPTION의 프로젝트 URL은 [문서 root](https://archive.r-lib.org/). README·NEWS·릴리스 체크리스트를 함께 읽었다. | 1.1.12 root와 archive_read. 주창 2025-03-24~26 UTC. | source `a4c6ec37fc8737a189ca7ec7095ec0161888f9e8`; 생성 `45e0d9ebc168cf3632bc2d737c9db2318668a826`; Pages 2328795124. | [DESCRIPTION L18](https://github.com/r-lib/archive/blob/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION#L18), [릴리스 #113](https://github.com/r-lib/archive/issues/113) | root를 계속 1.1.12로 유지한다는 약속, 구판 전용 URL·동시 제공·유지 기간은 찾지 못했다. |
| P1 bandersnatch — 문서 진입점을 찾는 독자 | README가 [latest](https://bandersnatch.readthedocs.io/en/latest/)와 root를 안내한다. | 7.0.1을 지금 읽는 목적은 연구 가정. 대조창 `[2025-12-16T17:51:34.578405Z, 2025-12-19T17:51:34.578405Z)`. | source `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74`; latest run 30720077. | [고정 README L18·99](https://github.com/pypa/bandersnatch/blob/7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74/README.md#L18), [7.0.1 릴리스](https://github.com/pypa/bandersnatch/releases/tag/7.0.1) | named 7.0.1 경로의 게시·영구 유지 및 구판 동시 제공 약속은 확인하지 못했다. |
| R2 asciicast — 패키지 2.3.1 사용 예제를 읽는 독자 | DESCRIPTION이 [문서 root](https://asciicast.r-lib.org/)를 안내한다. 대표 예제는 articles/asciicast-demo.html이다. | 2.3.1. 대조창 `[2024-01-21T20:53:46Z, 2024-01-24T20:53:46Z)`. | source `f992b26f3cb30c799fbb95f6148852d8ae8a7f18`; 생성 `92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1`. | [DESCRIPTION L19](https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/DESCRIPTION#L19), [고정 NEWS](https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/NEWS.md) | 특정 옛판을 계속 제공하거나 구판을 따로 유지한다는 두 번째 약속은 확인하지 못했다. |

## 표 2 — 소스·실행·게시·독자 응답의 연결

| 사례·경로 | source SHA | build·artifact | deployment·최종 상태 | 응답 UTC·최종 URL·파일/절 지문 | 같은 시점의 두 조건 | 미확인 |
|---|---|---|---|---|---|---|
| P3 stable/options/#enable | `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc` | 동일 소스 조회에서 stable 30298915 추가 확인. 실제 MkDocs exit 0. 파일 manifest 미확보. | RTD build success; 별도 게시 승인·유효구간은 미확인. | **보조** 2025-11-14T02:26:28Z [보관 options](https://web.archive.org/web/20251114022628id_/https://cibuildwheel.pypa.io/en/stable/options/): v3.3.0 nav, id=enable, CPython 3.13 free-threading opt-in/3.14+ 기본 포함; decoded SHA256 `05b8fe8e…`. **현재** 2026-11-23T14:50:43Z의 [같은 경로](https://cibuildwheel.pypa.io/en/stable/options/#enable)는 옵션 내용이 달라졌고 stable changelog 첫 판은 4.3.5다. | P3 원 약속 쌍 전체 **0/1 확인, 1 미확인**. | 주창 응답, 두 게시 구간 교집합, 파일→run 지문. 보조 응답을 주창으로 소급하지 않는다. |
| P3 1.x/ | `da84127892e79fab70b0ca4a4d22a23c1db53116` | 14073318, 2021-06-22 MkDocs exit 0. 당시 소스 식별용 ancestry. | 2025년 게시 상태 전이는 미확인. | **보조** 2025-11-14T11:28:00Z [보관 root](https://web.archive.org/web/20251114112800id_/https://cibuildwheel.pypa.io/en/1.x/): CPython 2.7·PyPy 2.7 표. decoded SHA256 `5fae3b9e…`; **현재** 2026-11-23T14:50:48Z [1.x](https://cibuildwheel.pypa.io/en/1.x/)와 바이트 전체 일치. | 위 P3 쌍의 두 번째 경로. 다른 시각의 응답이다. | 주창 제공 여부와 두 응답 사이의 연속성. |
| P3 v3.3.0/options/#enable | `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc` | 30298914·30298916 모두 같은 소스·생성 성공. 특정 파일을 어느 run이 만들었는지는 확정하지 않음. | 현재 version active/built; 과거 독립 publish 거래 미확인. | **현재** 2026-11-23T14:50:48Z [고정판 options](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable), SHA256 `4576ddf7…`. 보조 stable/options와 RTD slug 메타데이터 한 값만 달라, stable→v3.3.0 치환 뒤 정확히 일치한다. | 원문에 없는 별도 고정판 약속을 추가하지 않음. | 당시 tag 경로 응답, 파일별 run 귀속. |
| P1 latest/ | `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74` | 30720077, Sphinx HTML 2025-12-16T17:51:07.787761Z~17:51:12.494739Z exit 0. | RTD build success; 별도 당시 publish 거래 미확인. | **현재** 2026-11-23T14:50:47Z [latest](https://bandersnatch.readthedocs.io/en/latest/)는 8.2.0; SHA256 `c00b3dcc…`. | 0/0, 두 번째 원 조건 없음. | 대조창의 7.0.1 응답과 artifact checksum. |
| P1 7.0.1/ | `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74` | 현재 named version identifier는 같은 소스. active=false, built=false. 같은 소스의 latest 성공과 구별. | named의 과거 게시 미확인. | **현재** 2026-11-23T14:50:47Z [named 경로](https://bandersnatch.readthedocs.io/en/7.0.1/) 404; 오류 본문 SHA256 `09fd43d0…`. | 0/0, 산출 불가. | 404를 과거 생성·게시의 부재로 확대하지 않는다. |
| R1 root | `a4c6ec37fc8737a189ca7ec7095ec0161888f9e8` | 생성 `45e0d9eb…` @2025-03-24T12:34:38Z. 발행자 메시지는 소스 접두 a4c6ec3을 지목. index SHA256 `409a0d3b…`. | 2328795124 입력=생성 SHA, 생성 12:35:07Z. 남은 status 6150834411은 **inactive @12:38:03Z**. env URL 공백, log run 14035386117/job39292155301 현재 404. | **현재** 2026-11-23T14:49:25Z [root](https://archive.r-lib.org/)는 1.1.14, SHA256 `54645ed3…`; 생성 1.1.12 파일과 다름. **보조** 2025-02-27 보관 root는 1.1.11. | 0/0, 두 번째 원 조건 없음. | 주창의 root 응답과 앞선 status 순서. inactive는 성공·실패·내용 소실 중 어느 것도 단독 입증하지 않음. |
| R1 reference/archive_read.html | 위 R1 source | [고정 생성 HTML](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html), SHA256 `0c0efbe4…`; 발행자 git blob과 직접 계산 일치. | 위와 같은 선택 Pages 객체. | **현재** 2026-11-23T14:49:24Z [archive_read](https://archive.r-lib.org/reference/archive_read.html)는 1.1.14, SHA256 `6f173ffa…`. 두 후속 생성 스냅샷에서도 1.1.12 root·leaf는 유지됐지만 당시 HTTP는 아님. | 0/0, 산출 불가. | 생성 HTML의 실제 제공 구간. |
| R2 root | `f992b26f3cb30c799fbb95f6148852d8ae8a7f18` | 생성 `92fecbc0…` @2024-01-21T20:53:46Z. index SHA256 `cd5bab13…`. | 발견한 Pages 1283145596 입력=생성 SHA, 생성 20:55:45Z. 남은 status 3093912083 **inactive @20:58:36Z**; env URL 공백, run7603761786 현재404. | **현재** 2026-11-23T14:49:29Z [root](https://asciicast.r-lib.org/) 2.3.1, 선택 생성물과 바이트 전체 일치. | 0/0, 두 번째 원 조건 없음. | 대조창 실제 제공 응답·상태 순서. |
| R2 articles/asciicast-demo.html | 위 R2 source | [고정 생성 HTML](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html), SHA256 `c812426f…`. | 위와 같은 선택 Pages 객체. | **현재** 2026-11-23T14:49:29Z [예제](https://asciicast.r-lib.org/articles/asciicast-demo.html) 2.3.1, 생성물과 바이트 전체 일치. | 0/0, 산출 불가. | 바이트 일치만으로 2024년 제공·무중단 유지까지 입증할 수 없음. |

## 표 3 — 현재 정보의 선택과 역사 근거를 더한 선택

| 독자 목적 | 현재 정보로 선택한 링크 | 역사 근거를 더한 선택 | 바뀐 근거·반례 | 추가 확인 비용 | 보류 조건 |
|---|---|---|---|---|---|
| P3: v3.3.0 enable 판단과 구계열 안내 | **고정판** [v3.3.0/options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable) + [1.x](https://cibuildwheel.pypa.io/en/1.x/). 당시 공동 제공은 이미 유보. | 기본 선택 유지. 두 보조 capture와 각각의 UTC를 추가한다. 현재 지원판을 원하는 다른 목적에는 stable을 안내한다. | 별칭 이름이 달라도 options 내용이 같은 대조를 확보. 동일 SHA·내용만으로 두 tag run 중 하나를 고를 수 없다는 한계는 유지. | P3/P1 합계로 사전 이후 49 논리 GET·1,182,485 body bytes. 개별 귀속/게시 구간은 아직 필요. | 주창 두 경로 응답 또는 내용 식별을 포함한 게시 구간 교집합 전에는 당시 공동 제공을 주장하지 않음. |
| P1: 7.0.1 문서 읽기 | **유보**. 현재 latest는 8.2.0, named 7.0.1은404. | 유보 유지. [30720077 원 빌드](https://readthedocs.org/api/v3/projects/bandersnatch/builds/30720077/)를 생성 증거로만 첨부한다. | 현재 named404에서 “그 소스 문서가 생성되지 않았다”로 가는 추론은 같은 SHA latest의 HTML 성공이 반박한다. 이 잘못된 추론을 실제 사전 권고가 했다고 꾸미지 않는다. | 위 Python 공동 비용에 포함. 남은 최소 입력은 30720077 파일 manifest·당시 latest HTML. | 7.0.1 내용을 식별한 생성물 또는 보관 응답이 없으면 8.2.0을 7.0.1 대용으로 반환하지 않음. |
| R1: 1.1.12 archive_read의 내용을 확인 | **유보**. 현재 root·leaf는1.1.14. | **생성물** [1.1.12 HTML 원문/다운로드](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html). 렌더링된 옛 사이트는 아니다. | 선택 생성 파일의 판과 바이트를 확인해 반환 가능한 자료가 생김. inactive 전후의 두 생성 스냅샷은 같은 정식판 파일을 보존. 공개 제공 구간은 여전히 공석. | R1/R2 합계로 사전 이후 62 논리 GET·1,374,800 body bytes. R1 상태/로그 공석을 대체할 당시 정적 기록 필요. | 당시 웹 공개 성공·과거 root 제공을 말하려면 상태 전이와 경로별 응답 지문을 더 확보해야 함. |
| R2: 현재 2.3.1 예제 읽기 | **이동 별칭** [현재 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html). 당시 제공은 유보. | 같은 링크 유지. 역사 자료 인용용 [고정 HTML 원문](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)을 보조로 제공한다. | 현재 root·leaf 2/2가 선택 생성물과 정확히 같음. 현재 내용의 신뢰는 강화되지만 당시 제공 주장은 바뀌지 않음. | 위 R 공동 비용에 포함. 대조창 경로 응답·원 Pages 로그는 남음. | 목적을 “2024년 제공을 입증”으로 바꾸면 현재 링크만으로 승인할 수 없음. |

### 분모와 산출할 수 없는 값

| 계산 단위 | 확인/분모 | 해석 |
|---|---:|---|
| 고정 소비자 자리·같은 목적의 권고 비교 가능 | 4/4 | P3·R1·P1·R2를 교체하지 않았다. |
| 두 원 독자 조건을 약속한 프로젝트 | **1/6 원 분모**, 이번 선택 **1/4** | AF-RES-082 원 모집 분모를 보존. P3만 해당. 연구자가 붙인 고정판 목적을 원 약속으로 세지 않음. |
| 원 로그까지 분석한 선택 RTD 생성 run | **4/4 success** | tag14·tag16·추가 stable15·P1latest. 별도로 메타데이터에서 latest30298913도 읽었으나 이 4run 분모에는 넣지 않음. 2021 legacy1/1은 ancestry로 분리. |
| RTD 선택 run의 별도 게시 거래 식별 | **0/4, 미확인4** | build success를 별도 publish success로 승격하지 않음. |
| 제공자가 success를 보고한 Pages 배포를 직접 읽음 | **0/2, 이전 순서 미확인2** | 선택 Pages 객체2/2와 남은 inactive2/2는 읽음. 실패율0/2 또는2/2라는 뜻이 아님. RTD run과 단위를 합쳐 성공률을 만들지 않음. |
| 주 관측창의 목표판을 실제 경로 응답으로 식별 | **0/9, 미확인9** | 고정9슬롯. 생성 파일이나 현재 응답은 이 분자에 넣지 않음. P3 root 부가 확인도 분모를 늘리지 않음. |
| P3 두 원 조건의 당시 공동 확인 | **0/1, 미확인1, 직접 반증0** | 서로 다른 보조 응답의 시각을 합치지 않음. 나머지3자리의 공동 확인은 **0/0, 산출 불가**: 두 번째 원 조건이 확인되지 않음. |
| 현재9경로의 HTTP200 / 목표판 내용 식별 | **8/9 / 4/9** | 404는P1 named. 목표판은P3 tag·1.x, R2두경로. HTTP200과 목표판은 별도 값. |
| 현재 R 응답과 선택 생성물의 바이트 일치 | **2/4** | R2두파일. R1의 NEXT/LAST 생성 스냅샷은별도 **4/4** 동일하며 웹 요청수가 아님. |
| 기본 링크 후보 변경 / 유지 | **1/4 / 3/4** | R1만 유보→생성물. 사전의 당시 공개 제공 주장 반전은 **0/4**: 이미 유보했기 때문. R2의 현재 바이트 일치 유보는 새로 해소됐다. 실제 A/B 서비스 효과는 실험하지 않아 **0/0 산출 불가**. |
| 강한 사건 사슬 완결 | **0/12 최초 층화 표본**, **0/4 추가 사건** | 관련 사건은8/12+4/4. 회복 지문까지 갖춘 사례가 없다는 표본 결과이지 그런 사건이 세상에 없다는 증명이 아님. |
| 타 분야 실제 판 관계 | **2기관, 3쌍, 6판 기록** | 양쪽 파일 또는 manifest를 읽음. 여러 판은 같은 저작 계보로 묶음. |
| 직접 읽은 원문·계보 | **201원장행; 적격126 URL·판; 같은 바이트 중복까지 뺀 최소123자료; 25계보** | 정책4계보를 모두 빼도 실제 저작·사건21계보. 검색·실패·빈 색인·중복 미러는 원자료 최소수에서 제외. [검산](evidence/source-audit.json). |

# AF-RES-086 결과 — PARTIAL

**지금 반환할 내용은 식별했지만, “이 주소에서 당시 지원판과 구판 안내를 함께 읽을 수 있었다”는 핵심 역사 주장은 확정하지 못했다.** P3는 주창 다음 날의 개별 두 판 응답을 찾았고, R1은 남은 inactive 상태와 동일 정식판 파일을 보존한 후속 생성물을 찾았다. 어느 결과도 빠진 당시 게시 구간을 대신하지 않는다. 자료 최소량과 독립 검산을 통과해도 이 공석 때문에 REVIEW_READY로 올리지 않는다.

본 연구는 계획 SHA `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`, 실제 시작 SHA `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`, 유일 선행 `AF-RES-082@1f8bf039ad4f9a38b99764a11f72b515facef39c`를 구별한다. 작업 계약과 창은 [manifest](manifest.json)·[SCOPE](SCOPE.md), 사전 권고는 원격 커밋 `586b33488f6338ee8309a671d270656d837df636`, 역사 원장은 `a8852cc15640429f9faf5ee487f83c0fd0d8dfdc`에 고정했다. 같은 회차 과제의 결과는 사용하지 않았다. 222개 저장소 모집, 12개 서비스의 재평가, 가격·현재 홈페이지 전수 조사는 수행하지 않았다.

표의 현재 응답 UTC는 수신 완료 시각을 초 단위로 표시했다. 요청 시작·수신 완료의 소수점 UTC는 중앙 원장의 retrieval 필드에 따로 두고, 보관 capture·발행자 사건 UTC와 구별했다. stream의 기존 read_utc가 요청 시작인 경우 그 의미를 보존했다. 표의 짧은 지문은 SHA256 접두다. 전체 값, 원문 URL·판·절, 직접 조회 UTC, 발행자 제공 지문, 관측 주체와 한계는 [sources.jsonl](sources.jsonl)·[routes.jsonl](routes.jsonl)에 있다. 전체 다운로드는 재생 가능한 임시 자료이며 커밋에는 짧은 원문 추출·manifest·조회 영수증을 남겼다. 직접 받은 파일의 지문과 발행자가 적은 source SHA·ETag·CDX digest·Git blob ID를 한 값으로 합치지 않았다.

## Q1 — 주소를 안내한 범위와 연구자가 추가한 목적

P3의 고정 README는 현재 지원판의 문서 진입점과 enable 옵션을 안내하면서, 지원이 끝난 Python을 쓰는 독자에게 별도로 1.x를 가리킨다. 따라서 두 독자 조건을 같은 프로젝트의 원 약속으로 센다. 그러나 1.x는 구계열 경로다. 특정 patch의 불변 바이트, 영구 제공, 명시적인 유지 기간까지 약속한 문장은 찾지 못했다. 고정 v3.3.0 경로를 지금 반환하는 것은 반복 가능한 판 인용을 돕기 위한 이번 연구의 선택이다. [PY-P3-README, PY-P3-CHANGELOG-SOURCE, claims.csv의 C-P3-SUPPORTED·C-P3-LEGACY·A-P3-FIXED]

P1의 원 진입점은 latest다. named 7.0.1을 지금 읽고 싶다는 목적과 그 경로를 소유자가 영구 보존하겠다는 약속은 다르다. R1·R2의 DESCRIPTION은 판 번호와 root URL을 적지만 구판 전용 경로나 유지기간을 적지 않는다. 현재 root가 새 판을 주는 결과만으로 원 계약 위반이라고 결론 내릴 수 없다. [PY-P1-README; R1/R2-REQ-DESCRIPTION·README·NEWS]

R1의 동시대 릴리스 #113은 URL 검사, GitHub 릴리스, 개발판 전환을 완료했다고 표시한다. 이것은 발행자의 작업 기록이며 실행된 Pages success 로그는 아니다. P3의 보조창 공개 이슈/PR 검색에서 읽은6개 후보에는 문서 구판 유지기간의 발화가 없었다. R1의 같은 방식 검색은 #111·#112·#113 세 후보였다. 이 검색은 별도 GitHub Discussions 전체나 모든 키워드의 완전 탐색이 아니다. 누락된 원 약속을 연구 가정으로 채우지 않았다. [PY-P3-DISCUSSION-SEARCH; R1-DISCUSSIONS-WINDOW; R1-RELEASE-ISSUE]

## Q2 — 같은 SHA의 두 실행은 같은 파일의 증명이 아니다

RTD 소스별 조회는 같은 SHA의 실행4개를 반환했다. 지정된 tag30298914·30298916 이외에 latest30298913과 stable30298915가 있었다. 지정한 두 tag를 새 실행으로 교체하지 않고, stable의 경로 연결을 조사하기 위해15의 원 로그를 더 읽었다. [PY-P3-SOURCEBUILDS, PY-P3-LOG14·LOG16·LOGSTABLE]

| 실행 | APIv3 요약 created~finished, 2025-11-12 UTC | 원 생성 명령의 시작~종료 UTC | 해석 |
|---|---|---|---|
| tag30298914 | 19:28:06.450081~19:28:17.450081 | 19:28:11.247855~19:28:15.993088 | MkDocs exit0. |
| tag30298916 | 19:28:06.585063~19:28:22.585063 | 19:33:12.804589~19:33:20.236085 | v2 task_executed_at은19:33:07.043447. 요약 finished와 실제 명령 시각이 다름. |
| stable30298915 | 19:28:06.545031~19:28:22.545031 | 19:33:12.542235~19:33:20.287693 | stable 생성의 별도 실행. tag16과 생성 구간이 겹침. |

run16의 API 요약 시각을 삭제하거나 원 명령 시각과 같은 값으로 바꾸지 않았다. 현재 tag index의 BuildDate는19:33:19.984472로 tag16 구간과 맞는다. 반대로 현재 tag options의 서버 mtime은19:28:15.896559606로 tag14 구간과 맞는다. 보관 stable options의 mtime은19:33:20.100373631이다. 이는 후보를 좁히는 시간 정합성이며, 파일을 어느 실행이 생성·게시했다는 최종 귀속은 아니다. 동일 바이트가 재생성되거나 복사되고 과거 mtime이 남을 가능성을 배제할 자료가 없다. [PY-P3-TAG-INDEX, PY-P3-TAG-NOW, PY-CAP-STABLE-OPTIONS-20251114]

공개 build JSON, UI의 원 로그 링크, version downloads, 공식 API 계약과 현재 URL/serializer 구현, sitemap을 읽었지만 대상 run의 파일별 checksum·artifact ID를 연결한 공개 manifest는 확보하지 못했다. APIv2의 `is_uploaded=false`를 게시 실패로 판단하지 않은 이유는 현재 공식 모델에서 이 필드가 upload API 유형을 설명하기 때문이다. 이 현재 코드가 2025년 배포의 실제 코드였다고 확장하지 않는다. 내부 manifest가 존재하지 않는다는 주장도 하지 않는다. [PY-RTD-BUILD-MODEL, PY-RTD-API-HELP, PY-RTD-API2-HELP 등 해당 service 계보]

P1은 같은 SHA로 latest HTML 생성이 성공했다. PDF 단계의 뒤쪽 오류를 HTML 실패로 읽지 않았다. 현재 named 경로가 비활성·미생성으로 표시되고404를 주더라도, 같은 소스의 문서 생성 자체가 없었다고 말하면 이 원 로그와 충돌한다. 다만 최신 경로의 과거 HTML 파일과 당시 요청 응답은 여전히 없다. [PY-P1-BUILD, PY-P1-LOG, PY-P1-VERSION]

## Q3 — R1 상태의 보존 한계와 재게시 시각

[선택 statuses 원문](https://api.github.com/repos/r-lib/archive/deployments/2328795124/statuses)은 이 세션에서 HTTP200으로 읽혔다. 반환 배열에는 inactive 한 행만 남아 있었다. deployment 입력 SHA는 선택 생성 SHA와 같고, 상태 시각·env URL 공백·run/job URL도 읽었다. 링크된 run API, job API와 웹 실행 페이지는 현재404였다. 주창 Actions 목록이 비거나 combined status가 pending/0건인 결과는 과거 실패로 채점하지 않았다. 모든 실패 URL·조회 UTC·영향받는 연결은 R 원장과 영수증에 남아 있다. [R1-DEPLOYMENT·DEPLOYMENT-STATUSES·PAGES-RUN·PAGES-JOB·PAGES-WEB-RUN·PAGES-RUNS-WINDOW·COMBINED-STATUS]

현재 [GitHub 공식 상태 API 설명](https://docs.github.com/en/rest/deployments/statuses?apiVersion=2022-11-28)은 이전 상태의90일 보존과 현재 상태의 유지를 구별한다. 이것은 과거 순서가 현재 응답에 다 없을 수 있음을 설명하는 현재 정책이다. 선택 배포에 실제 success가 있었거나 특정 행이 삭제됐음을 입증하지 않는다. `auto_inactive`일 가능성도 직접 기록이 없으므로 추론으로만 남겼다. [R-SERVICE-STATUS]

선택 객체만 읽고 끝내지 않고 주창에 만들어진11개 배포와 각각의 현재 statuses를 읽었다. 그중10개 status 시각은 주창, 마지막 하나의 inactive는2025-10-21로 주창과 보조창 밖이다. 나중 inactive 시각을3월의 게시 종료 시각으로 대체하지 않았다. 별도 failure→success 전이도 확보하지 못했다. [R1-DEPLOYMENTS-ALL·R1-DEPLOYMENTS-ALL-P2; R1-STATUS-*; streams/r/evidence/R1-republish-timeline.json]

발행자가 남긴 생성 커밋도 대조했다. NEXT `64824c63…`는12:37:22Z로 선택 inactive12:38:03Z 직전이다. LAST `3f2c1d51…`는16:07:18Z로 이후다. 두 스냅샷의 root·archive_read 네 파일이 선택1.1.12 파일과 모두 같았다. 개발판 파일의 갱신과 정식 root 내용의 교체는 다른 사건이었다. 따라서 inactive를 “저장된 정식판 내용의 소실”과 같다고 읽을 수 없다. 그러나 두 스냅샷 사이 모든 트리나 실제 사이트의 무중단 제공을 증명한 것은 아니다. [R1-NEXT-COMMIT·ROOT·LEAF, R1-LAST-COMMIT·ROOT·LEAF]

## Q4 — 보조 기간의 두 응답을 주창의 동시 제공으로 바꾸지 않음

초기 `statuscode:200` CDX 검색은1.x의 `warc/revisit` 기록을 놓쳤다. 후속 all-status prefix 조회로 찾아 실제 replay payload를 읽었다. 주창 stable/1.x의 all-status 조회는 여전히 비어 있었다. 빈 색인은 실제 제공 실패의 증거가 아니며, 보조 조회의 collapse=urlkey도 모든 capture나 제공 구간을 보존하는 조회가 아니다. 이 방법 변경과 한계는 [method-adjustments.json](evidence/method-adjustments.json)에 기록했다.

2025-11-14 stable/options에서 enable anchor와 내용을 직접 읽었고, 1.x에서는 Python2 계열 표를 직접 읽었다. URL 뒤 fragment는 HTTP 요청에 전달되지 않으므로 HTML의 id와 해당 절을 판독했다. 브라우저 스크롤·JavaScript 상호작용을 실행한 검사는 아니다. stable의 응답 시각은02:26:28Z, 1.x는11:28:00Z다. 같은 달력 날짜라도 같은 순간은 아니며 두 시각 사이의 제공 구간을 보장하지 못한다. 무엇보다 둘 다 고정 주창 밖이다.

보관 전송물은 gzip이었다. CDX의 base32 SHA1은 전송 gzip 바이트와 대조해 일치했고, 해제 HTML의 SHA256은 따로 계산했다. stable/options와 현재 tag/options는 RTD version-slug 한 필드만 다르다. 그 값을 stable→v3.3.0으로 치환하면 현재 tag의 원바이트 SHA256 `4576ddf7…`와 같아진다. 독립 검토자는 양쪽 slug를 같은 공통 표식으로 치환해 동일성도 재계산했다. 이 비교는 options 한 파일에 한정한다. root는 BuildDate도 다르므로 같은 정규화 결과라고 일반화하지 않았다. [streams/python/evidence/html-comparison.json; streams/review/python-audit.md]

이 결과는 “다른 별칭이면 다른 판”이라는 추론의 반대 근거다. 동시에 같은 본문을 여러 실행이 만들 수 있으므로 “같은 내용이면 같은 run”이라는 추론도 막는다. 10월16일 stable/options에는3.2.1의 nav와 같은 enable 절이 있었다. 절 하나의 공통 문구만으로3.3.0을 식별하면 틀릴 수 있다. 판 식별에는 nav·changelog·메타데이터·파일 지문을 함께 사용했다.

## Q5 — 사전 권고의 변화와 유지

사전 권고를 먼저 커밋했지만 선행082의 결과를 이미 알고 있었다. 따라서 맹검 실험이나 빠른 검사가 실전에서 얼마나 실패하는지 측정한 비교로 부르지 않는다. 같은 후보 네 가지와 같은 독자 목적을 유지한 비교에서 변경은 R1 한 건뿐이었다. 나머지 세 건은 근거의 깊이가 바뀌었으며 선택은 유지됐다. R2의 목적을 사후에 역사 증명으로 바꾸어 변경 건수를 늘리지 않았다. [prerecommendations.json; comparison.json; cards.md]

새 증거가 직접 막은 싼 추론은 세 가지다. P1의 named404가 소스 전체의 생성 실패를 뜻한다는 추론은 latest 성공 로그와 충돌한다. R1 inactive가 정식판 생성 파일의 소실을 뜻한다는 추론은 후속 파일 보존과 충돌한다. P3 별칭 이름이 다르면 본문 판도 다르다는 추론은 한 메타데이터 값만 다른 options 파일과 충돌한다. 반대로 현재 응답이 선택 생성물과 같아도 당시 제공은 미확인이라는 R2의 유보는 그대로 남았다.

반환 카드의 후보는 사용 목적에 따라 달라질 수 있다. 현재 지원 환경을 설정하려면 stable의 현재 내용이 알맞다. 과거 v3.3.0의 결정 근거를 인용하려면 고정판 또는 시각이 붙은 보관본이 더 구체적이다. 생성물 원문은 내용을 복구하는 데 유용하지만 브라우저에서 그때 서비스되던 사이트를 복원하지는 않는다. 이것은 링크 후보의 단일 우열이 아니라 입증할 주장에 맞춘 선택이다.

## Q6 — 사건 표본과 반대 방향의 대조

검색 기간은 이슈 생성2024–2025년이며 저장소는 jimporter/mike, mkdocs/mkdocs, readthedocs/readthedocs.org, actions/deploy-pages다. 검색식은 `is:issue created:2024-01-01..2025-12-31 (alias OR redirect OR 404 OR "wrong version")`. 각 저장소에서 생성순 첫3개를 선택한 뒤12개를 생성 UTC·번호 순서로 판독했다. 이는 전역 검색 결과의 최초12개라는 뜻이 아니다. 전송은 병렬이었고 판독·코딩을 시간순으로 정렬했다. 검색 원응답, 선별 규칙, 처음12개와 탈락 이유, 추가4개의 분리는 [PROTOCOL](streams/incidents/PROTOCOL.md)·[incidents.csv](incidents.csv)에 있다.

| 처음12개 시간순 | 사건 | 남는 증거와 강한 반례에서 빠진 부분 |
|---|---|---|
| 1 | RTD10990 | 내부 logging 예외. 독자 경로 사건이 아니므로 최소자료 수 제외. |
| 2 | RTD11001 | 프로젝트 삭제와 접근 손실. 성공한 생성·게시 후 경로만 틀린 사례는 아님. |
| 3 | RTD11042 | 폼·대시보드 논의. 독자 판 증거 없음, 제외. |
| 4 | mike199 | YAML 생성 실패. 생성 성공 조건을 만족하지 않는 대조. |
| 5 | mike202 | forge 기능 요청. 고정 배포 사건이 아니므로 제외. |
| 6 | MkDocs3579 | 테마 안내 논쟁. 판·게시 사건이 아니므로 제외. |
| 7 | MkDocs3583 | 생성 성공 제보와404. publish/ref/회복 지문 부족. |
| 8 | MkDocs3593 | 절대 CSS 경로 문제. site_url 진단과 반대 설명이 있으나 두 단계 성공 사슬 없음. |
| 9 | mike223 | 옛 deep link404·새 latest 내용의 당시 제보. 같은 ref의 성공 로그·회복 지문 부족. |
| 10 | Pages365 | 산출물 누락. 원 run 현재404, 게시 성공 없음. |
| 11 | Pages373 | 게시 success와404 제보. 생성·회복의 공개 원문 부족; 비공개 원 run 접근 불가. |
| 12 | Pages377 | 게시 도구 버전으로 인한 실패. 성공 뒤 경로 오류 조건 아님. |

추가4개는 RTD11531, mike229, Pages383, mike248이다. RTD11531은 stable과 release-r24.03.1의 footer Git hash가 같은데 경고 표시가 다르다는 기록이다. 전체 HTML의 바이트 동일성까지 확인한 사건은 아니다. mike229도1.0/stable이1.0.0을 가리키며 이름 표시가 다르다는 대조다. mike248은 Cloudflare의 SPA 처리와 root404 부재가 재귀 경로를 만드는 사례이며, 정상404 복구를 과거판 내용 복구로 바꾸지 않았다. [각 사건 BODY·COMMENTS 원문]

가장 가까운 반례는 [Pages383](https://github.com/actions/deploy-pages/issues/383)에서 이어진 [typst-community/dev-builds #1](https://github.com/typst-community/dev-builds/issues/1)이다. 발행자가 남긴 로그에는 같은 source `7d14b2f45ed78db82f976e5cd2dec5c7ffac2f9f`, run19385417200, artifact4575825543, 생성/업로드와 publish success가 있다. artifact의 catalog에는11월14일 릴리스가 있는데 공개 curl catalog에는9월19일 항목만 있다는 차이를 원문에서 읽었다. 발행자는 같은 commit의 dispatch로 회복했다고 보고했다. [I-TYPST-SUPPLEMENT-0 및 I-TYPST-CHAIN-2·3·4]

그러나 회복 직후 artifact ID·응답 바이트 지문을 확보하지 못했다. 현재 catalog에11월 항목이 있다는 관측도 그때의 회복 영수증이 아니다. 따라서 발행자의 상세한 성공·오래된 응답 연결은 인정하되 요구한 강한 사슬의 완결은0으로 유지한다. 같은 SHA를 재사용한 것이 단독 원인이라고도 결론 내리지 않는다. 같은 SHA의 dispatch로 달라졌다는 사실은 release 목록 같은 동적 입력이 source SHA 밖에 있음을 보여준다. 발행자 digest와 연구자가 받은 현재 catalog 지문은 별도 필드다.

## Q7 — 독자·릴리스 담당자·서비스 제공자의 증명 비용

| 관점과 이번에 실제 한 확인 | 계측한 요청·원문·바이트 | 남는 확인 |
|---|---|---|
| 지금 링크를 읽는 독자 | 고정9경로9 논리 GET, 응답본문458,565 bytes. 8개200, 1개404. 판과 절을 읽어 목표판4/9 식별. | 현재 페이지 하나로 과거 게시 구간을 알 수 없음. 고정판·생성물·보관 시각을 골라 주장 범위를 줄여야 함. |
| 현재 정보로 사전 권고를 만든 조사자 | 고정 소유자 원문·현재 URL·도움말20 GET,765,122 bytes. Python9+R11. | 이 비용에는 과거 run·게시·보관 조회가 없음. 선행 결과를 알고 있다는 비맹검 한계가 있음. |
| 과거 판을 입증하려는 릴리스 담당자에 대응한 추가 조사 | 네 자리에서 사전 이후111 GET,2,557,285 bytes. 원문·로그·상태·생성물·보관 index·실제 capture를 연결. | P3 파일별 run manifest·게시 구간, R1 당시 상태 전이·경로 응답이 남음. 모두 더 읽어도 공석이 해소되지는 않았음. |
| 공개 사건을 비교한 조사자 | GitHub connector46호출, 별도 HTTP6 GET·277,631 bytes. 원문12+추가4사건. | connector의 실제 HTTP 교환 수·전송 바이트는 미측정. 회복 직후 지문은 남음. |
| 보존기관의 판 관계를 읽은 조사자 | 계측35 GET·3,777,598 bytes. 그중 실제 tar.gz2개3,542,168 bytes. 별도 사전 탐색3 GET은 계측 밖. | matplotlib ZIP2개는 manifest만 읽음. 보존기관의 방문·파일 해시가 웹사이트 배포 이력을 대신하지 못함. |
| 서비스 제공자 | 공개 API·정책에서 무엇을 노출하고 무엇이 보존되지 않을 수 있는지 확인. 내부 운영 요청·저장·계산 비용은 **미측정**. | source/run/artifact/file digest, 게시 시작·종료, alias 목적지, 응답 판 지문을 보존해 공개해야 역사 주장을 적은 요청으로 재확인할 수 있음. 이는 제안이며 이번 서비스의 실제 내부 비용 측정이 아님. |

합계는 계측172 논리 HTTP GET·7,377,636 응답본문 bytes이며, 별도 connector46호출·계측 전 탐색3 GET·웹 검색 도구 비용을 포함한 전체 전송량이라고 부르지 않는다. redirect 내부 hop·헤더·TLS·독해 시간·금전도 측정하지 않았다. HTTP200이라도 빈 색인은 판 내용 확인 점수를 받지 않는다. 원자료 최소량과 네트워크 요청 수는 다른 분모다. [costs.json]

### 실제 판 쌍과 제도 간 적용 범위

| 제도·실제 저작 | 읽은 판 관계와 양쪽 파일/manifest | 웹 배포에 가져올 수 있는 판별법 | 그대로 가져올 수 없는 부분 |
|---|---|---|---|
| Zenodo Umap/Bismap | [60943](https://zenodo.org/api/records/60943) 1.0.0과 [800648](https://zenodo.org/api/records/800648) 1.1.0; concept705645는 현재800648을 가리킴. tar.gz 두개를 받아 MD5를 발행자값과 대조, setup.py의 판과245/263개 파일 manifest를 읽음. | 판 DOI와 이동 concept DOI를 구별하고, 판 record→파일명·크기·checksum→실제 bytes를 잇는다. | concept의 현재 목적지에서 과거 어느 때의 목적지였는지 복원할 수 없음. 소프트웨어 문서 서비스의 게시 기간도 알 수 없음. |
| Zenodo matplotlib | [2893252](https://zenodo.org/api/records/2893252) v3.1.0과 [3695547](https://zenodo.org/api/records/3695547) v3.2.0; concept592536의 현재 판은22700776/v3.11.2. 양쪽 ZIP명·크기·MD5 manifest를 읽음. ZIP은 미다운로드. | 발행자 파일 목록과 직접 파일 검증을 구별한다. | manifest의 checksum을 직접 받은 ZIP의 검산으로 세지 않음. |
| Software Heritage GNU hello | snapshot `a5e90783…`의2.9 revision `55c14d05…`와2.10 `dbdaa32b…`; 내부 디렉터리29/30항목, 양쪽 configure.ac와2.10 NEWS를 직접 읽고 hash 대조. 보존 방문은2015-08-28T11:13:26Z. | origin→방문→snapshot→revision→디렉터리→내용 지문으로 판을 식별한다. | tarball에서 만든 synthetic revision 시각은 원 CI·게시 시각이 아니다. 원 사이트의 URL·anchor·redirect·제공 기간은 별도다. |

반대 상황도 실제 기록으로 확인했다. [Zenodo DOI22705920](https://doi.org/10.5281/zenodo.22705920)은 철회 tombstone으로 HTTP410을 반환하고 기록에는 파일이 없다. 식별자가 계속 해결된다는 사실이 다운로드 가능한 내용의 보존을 보장하지 않는 실제 사례다. 의도적인 철회를 서비스 장애로 분류하지 않았다. 반대로 [Gitorious 보존 참여자의 고정 기록](https://wiki.archiveteam.org/index.php?title=Gitorious&oldid=59702)은 mirror 종료일을2024-09-30으로 적으며, Software Heritage에서는 해당 origin의 snapshot·33항목 manifest·Home.markdown 내용과 지문을 읽을 수 있었다. 옛 주소의 직접 요청은 이 환경의 proxy503이어서 영구404로 판정하지 않았다. 참여자의 종료 보고와 보존된 내용이 확인되는 수준의 사례다. [PR07·PR11·PR19·PR21·PR27·PR31·PR34]

현재 Zenodo 파일 관리 정책은 일정 기간의 사소한 파일 수정과 재게시를 설명한다. 그러므로 판 DOI가 같다는 이유만으로 모든 시점의 bytes 불변을 전제할 수 없다. 그렇다고 이번 두 Umap 파일이 실제로 교체됐다고 주장하지 않는다. 정책상 가능성과 특정 판의 관측을 분리한다. [PR16]

## 재사용 조건과 대안

반환 계약을 세 층으로 나누면 이 결과를 활용할 수 있다. 첫째, “현재 이 판의 내용을 읽을 수 있음”은 현재 경로의 판·절 확인으로 답한다. 둘째, “이 고정 생성 파일에 내용이 있음”은 소스 지목·파일 manifest·직접 지문으로 답한다. 셋째, “그때 이 주소에서 제공했음”은 당시 응답 또는 내용이 묶인 게시 구간이 있어야 답한다. 소스 보존은 둘째에 크게 도움이 되지만 셋째를 자동으로 채우지 못한다.

운영 측면에서 선택할 수 있는 대안은 고정판 URL, 시각이 붙은 보관 응답, 생성물 원문, 유보다. 고정판 URL은 읽기 편하지만 run 귀속·영구성은 별도다. 보관 응답은 관측 시각을 붙일 수 있지만 색인 공석·revisit·압축 지문을 처리해야 한다. 생성물 원문은 정확한 파일을 인용할 수 있지만 과거 렌더링 서비스라고 안내하면 안 된다. 유보는 자료가 없다는 정직한 결과이며 생성 실패라는 뜻이 아니다. 네 카드에는 이 조건에 따라 지금 실제로 반환할 주소와 볼 절을 적었다.

## 결론의 핵심 불일치·약점 — 정확히 3건

1. **P3의 주창 공동 제공과 파일별 run 귀속이 비어 있다.** 보조 capture는 모두11월14일이고, 두 tag run의 source는 같지만 요약 시각과 실제 생성 시각은 다르다. **다음 대상·입력:** RTD30298914·30298916·30298915의 당시 공개 artifact/file manifest와 stable/options·1.x의2025-11-11~13 보관 응답 또는 게시 유효구간. **판단을 바꿀 관측값:** 파일 digest가 특정run에 연결되고, 판별된 두 경로 응답이 같은 시점이거나 유효구간이 겹침; 또는 같은 시점의 잘못된 판/응답이 직접 반증으로 남음.
2. **R1은 inactive 한 행만 남아 역사적 최종 성공·실패 순서를 복원할 수 없다.** 후속 생성 스냅샷의 내용 보존은 확인했지만 당시 웹 제공과 같지 않다. **다음 대상·입력:** deployment2328795124/status6150834411와 run14035386117/job39292155301에 대해 발행자가 당시 공개한 Pages 로그·상태 배열·배포 산출물 지시자. **판단을 바꿀 관측값:** 입력45e0d9eb…의 게시 success/failure와UTC·environment_url이 실제 root/leaf 응답 지문으로 이어짐. 현재90일 정책이나 다른 프로젝트의 성공은 대체 근거가 아님.
3. **반례와 보존기관 대조는 경로의 역사까지 완결하지 못한다.** Pages383/typst는 회복 직후 지문이 없고, Gitorious의 옛 주소는 직접 영구 소실 판정이 아니라 참여자의 종료 보고와 proxy503 수준이다. **다음 대상·입력:** typst 같은 source의 회복 dispatch run·artifact·catalog 원문, Gitorious 종료 당시 공개 HTTP/redirect 보관본과 대응 SWH 파일. **판단을 바꿀 관측값:** 회복 직후 expected catalog의 판·digest가 원 실패 사슬과 연결되거나, 옛 경로 소실 시각과 보존 내용이 같은 판으로 결합됨. 그 전에는 강한 사건0/12·0/4와 역사 경로 미확인을 유지한다.
