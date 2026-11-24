| 경로 | 원 실험 입구(2025-11-10~16 / 17~23) | 보충 입구(2025-11-03~09 / 24~30) | 확인한 경로 차이·근거 | 미확인 |
|---|---|---|---|---|
| A 일본어 일반 업데이트 | [원 목록 11/13](https://forest.watch.impress.co.jp/docs/digest/2063126.html), [11/20](https://forest.watch.impress.co.jp/docs/digest/2065122.html) | [11/6](https://forest.watch.impress.co.jp/docs/digest/2061271.html), [11/27](https://forest.watch.impress.co.jp/docs/digest/2066848.html) | 배포판/기능 업데이트를 먼저 노출. Electron/Zed 반복, GitHub Desktop 안정/베타 중복. S1 A-SW2-3 Telegram 기능 발견. | 개별 제보·편집 선정 사유·2025 클릭수 |
| B 영어 전문 색인 | [#625](https://this-week-in-rust.org/blog/2025/11/12/this-week-in-rust-625/), [#626](https://this-week-in-rust.org/blog/2025/11/19/this-week-in-rust-626/) | [#624](https://this-week-in-rust.org/blog/2025/11/05/this-week-in-rust-624/), [#627](https://this-week-in-rust.org/blog/2025/11/26/this-week-in-rust-627/) | Project/Tooling Updates가 특정 생태계에 집중. B-SW1 4행, B-SW2 3행 전부 모집; 5자리 구조적 없음. 기존 channels-console/Tokuin의 우위가 새 창에 재현되지 않음. | 생태계 전체 발견율·개별 제보 PR |
| C 영어 배포 편입 | [11/13](https://f-droid.org/en/2025/11/13/twif.html), [11/20](https://f-droid.org/en/2025/11/20/twif.html) | [11/6](https://f-droid.org/en/2025/11/06/twif.html), [11/27](https://f-droid.org/en/2025/11/27/twif.html) | Newly Added Apps부터 package/build/제작자까지. 첫 링크는 S1 6/12 열림 모두 중간, 6 실패. 두 번째 정규 URL로 ciphernotes 현재 설명을 회복, 역사적 제작자 증거는 별도. | 편입 제보·심사 과정 및 당시 실제 배포판의 전체 기능 |

표 1. 동결 원장과 사전등록 보충의 모집틀. 단위=경로×창, 각 예정 6자리. 개별 출처/원문은 [frame](frame.csv), [paths](paths.jsonl), [sources](sources.jsonl), 원 결과 [고정 SHA](https://github.com/laadkke-arch/agentflow-open/blob/fbd9a00b105da2666af5a158ee2678740572cf38/docs/workstreams/research/AF-RES-149/RESULT.md). 비교 대상은 원래 R1~R3 요구 그대로, 다른 차수 후보 사용 안 함.

| 연구/창·경로 | 실제/예정 자리 | 첫 링크 시도/성공 (제작자/중간)/실패 | 직접 R1/R2/R3; 조건부 쌍 | 적격 고유 및 추가 vs 같은 창 A | 원장 ID·결손 |
|---|---:|---|---|---|---|
| 원 W1 A | 6/6 | 6/5 (5/0)/1 | 0/0/0; 2 | 1, +0 | A-W1-1~6 |
| 원 W1 B | 6/6 | 6/6 (6/0)/0 | 0/0/0; 3 | 2, +2 | B-W1-1~6 |
| 원 W1 C | 6/6 | 6/6 (0/6)/0 | 0/0/0; 0 | 0, +0 | C-W1-1~6 |
| 원 W2 A | 6/6 | 6/6 (6/0)/0 | 0/0/0; 0 | 0, +0 | A-W2-1~6 |
| 원 W2 B | 2/6 | 2/1 (0/1)/1 | 0/0/0; 0 | 0, +0 | B-W2-3~6 없음 |
| 원 W2 C | 6/6 | 6/6 (0/6)/0 | 0/0/0; 0 | 0, +0 | C-W2-1~6 |
| S1 SW1 A | 6/6 | 6/3 (3/0)/3 | 0/0/0; 0 | 0, +0 | A-SW1-1~6 |
| S1 SW1 B | 4/6 | 4/4 (4/0)/0 | 0/0/0; 0 | 0, +0 | B-SW1-5~6 없음 |
| S1 SW1 C | 6/6 | 6/3 (0/3)/3 | 0/0/0; 0 | 0, +0 | C-SW1-1~6 |
| S1 SW2 A | 6/6 | 6/5 (5/0)/1 | 0/0/0; 0 | 0, +0 | A-SW2-1~6 |
| S1 SW2 B | 3/6 | 3/3 (2/1)/0 | 0/0/0; 0 | 0, +0 | B-SW2-4~6 없음 |
| S1 SW2 C | 6/6 | 6/3 (0/3)/3 | 0/0/0; 0 | 0, +0 | C-SW2-1~6 |
| 원 합 | 32/36 | 32/30 (17/13)/2 | 0/0/0; 5/96 | 3, +2 | 4 구조적 공백 |
| S1 합 | 31/36 | 31/21 (14/7)/10 | 0/0/0; 0/93 | 0, +0 | 5 구조적 공백 |
| 전체 첫 링크 | 63/72 | 63/51 (31/20)/12 | 0/0/0; 5/189 | 3, +2 | 9 구조적 공백 |

표 2. 비교 단위=모집 자리, 시도/성공은 첫 링크만, 요구 쌍은 실제 자리×3. 원 108/S1 108 예정 쌍에서 각 12/15 미관측 유지. 실패와 비적격 및 중간 도달 분리. S1 호출/대기 [calls.csv](calls.csv), [final_attempts](final_attempts.jsonl); 원 시간은 소급 불가. 추가 진단은 아래 별도.

| 대안 | 유리한 모집 조건 | 단독 기여를 뒤집은 반례·URL | 다른 분야에서 가져온 원리/한계 | 다음에 관측할 것 |
|---|---|---|---|---|
| A 먼저 | 범용 업데이트와 작은 일본어 프로그램·버전 기능 찾기 | [Electron](https://github.com/electron/electron/releases/tag/v39.2.3) 복수 릴리스, S1 첫 링크 적격 0. [Telegram](https://github.com/telegramdesktop/tdesktop/releases/tag/v6.3.4) 추가 판독 때만 조건부 | 기증 기록과 실제 입수물 분리; 판별 단위는 제품/기능 | 고정 날짜 링크·변경 로그·형식 검증 |
| B 병행 | 분야 특화된 메커니즘, 코드/저자 직결 | [#624](https://this-week-in-rust.org/blog/2025/11/05/this-week-in-rust-624/)·[#627](https://this-week-in-rust.org/blog/2025/11/26/this-week-in-rust-627/) 7행 모두 적격 0, CGP의 가상 예시는 실기록 아님 | 표본관/색인에서 공급원 편향과 결번을 기록; 소프트웨어 편입 수와 가치 불일치 | 사전등록한 더 긴 날짜 창에서 실제 유입 및 원문 비용 |
| C 병행·제작자까지 2단계 | 설치 가능한 소형 앱, 빌드/버전 | [ciphernotes](https://f-droid.org/en/packages/com.ciphernotes.twa/) 최초 링크 실패 및 현재 중간 설명만 회복; [Calisthenics v1.3](https://github.com/Gonbei774/CalisthenicsMemory/blob/v1.3.0/README.md) 과거 근거는 추가 조사에서만 | 입수 provenance·버전·검증 기록을 분리; 빌드 성공은 기능 시험 아님 | 실제 배포 SHA와 재연결 시험 |
| D 원어권 자천/현지 큐레이션·역추적 | 편집·배포 관문 밖 독립 웹 및 지역 어휘 | [CRAMA](https://news.hada.io/topic?id=37753) 작은 브라우저 도구지만 요구 적격 아님; [GeekNews 날짜별](https://news.hada.io/past?day=2025-11-25) 전체 목록은 Show만의 모집틀 아님 | zine/지역 컬렉션의 직접 제출과 이후 편입 구별; 웹은 저자/복제본/삭제의 불확실성 | 동일 종류 과거 목록, 교차 유입 경위 및 실제 기능 |

표 3. 조건부 대안이지 최종 설계 채택 아님. 기존 [OPTIONS](../OPTIONS.md)과 함께 해석.

# AF-RES-149#1 — 사전등록 보충 결과 S1

**보충 관측·비교·검산 실행 완료. 원 과제 엄격 판정 PARTIAL 유지.** 시작 기준 fbd9a00b105da2666af5a158ee2678740572cf38. 사전등록 [PROTOCOL](PROTOCOL.md) 커밋 f9438d8c45d0c02b3cde985c06897c534b552407. 원 SCOPE, frame, paths, sources, judgments, cost, OPTIONS, RESULT, SELF_CHECK는 바꾸지 않았다. 모집 부족 4자리의 **누적 수량**은 B의 독립 7자리로 초과 보완했다. 원래 B W2의 네 결번과 새 B의 다섯 결번을 채운 것으로 간주하지 않는다. 합계 63/72 실제 자리. 36이라는 전체 실제 표본 하한을 넘었지만 각 셀 실제 6개라는 엄격한 기준은 재현 실패. 날짜 선택 후 결과를 보고 창/경로 바꾸지 않았다.

## Q1. 실제 유입과 먼저 보인 곳
원 자료의 운영 규칙, 편집 노출, 제보 글, 편입판 표시와 최초 공개를 구분하는 원 Q1을 유지한다. 새 6개 목록을 실제 열고 첫 순서대로 31자리를 확보했다. A는 버전 업데이트를, B는 전문 분야의 소프트웨어·글을, C는 Newly Added Apps를 목록에서 실제 제공했다. SW1 B의 CGP 0.6 (10/26)와 esp-hal (10/30)이 11/5 목록에 들어온 것은 이 창의 신규 구현이라고 부를 수 없다. SW2 A의 Telegram 주제별 export는 11/25 코드 흔적→11/27 목록, C ciphernotes는 2024-12-26 및 2025-09-13 제작자 코드→11/27 편입 목록. 등재 이전 자료를 다시 발견한 경우다. C의 Calisthenics는 H04 빌드 기록 1.2(11/18), 1.3(11/19)→11/20 목록; 1.4(11/22), 1.5(11/24) 검증은 뒤다. 제보 메일/MR의 실제 송수신 시각 및 세계 최초 공개는 미확인. 각 행 날짜·URL·실패는 paths/sources와 history에 기록. 원 Q1의 운영자·원저자·현지 이용자·다른 분야 설계자 자료는 별개 관점으로 보존한다.

## Q2. 공급 경로, 반복, 새로 보인 것
선택 원리는 A 일반 편집 업데이트, B 전문 커뮤니티, C 배포 편입, D 지역 자천/큐레이션(별도 목록 감사), 외부 분야의 입수 사건 분리 및 소비자 이슈 역추적(가설). 새 원장의 A에서 Github Desktop의 안정/베타와 Electron 세 릴리스가 반복된다. 원과 S1의 겹침 라벨 Zed/Electron/SeaORM 3개; 같은 프로젝트의 버전 및 기능이 다르므로 이를 별개 구현의 증거로 합산하지 않는다. 원 29·S1 28·합 54 라벨 하한, 자리 상한 32/31/63. Athena 명칭 동일·package 상이, CGP 프레임워크와 serializer 관계 등 미결. 새로운 URI 발견과 새로운 구현 확인을 분리한다. 전문 색인 B의 원 2개 적격은 이번 7개에서 0개로 재현 실패. C 경로는 편입 메타만 읽어 실제 기능을 확인하지 못한 자리와 접근 실패가 많았다. 미지의 세계 자료·전체 recall은 산출 불가.

## Q3. 네 언어 최신·과거 목록 직접 확인
| 언어 | 최신 (조회 2026-11-24 UTC / 표시 일자) | 과거 직접 원문 | 같은 모집틀 여부·근거 |
|---|---|---|---|
| ja | [Impress 11/24 2026](https://forest.watch.impress.co.jp/docs/digest/2158894.html), 29건 | [2025-11-06](https://forest.watch.impress.co.jp/docs/digest/2061271.html), [11-27](https://forest.watch.impress.co.jp/docs/digest/2066848.html) | 동일 다이제스트. 531drop QR 및 ノコス 입력 유지 등 작은 독립 기능도 보임 |
| en | [TWIR #678 2026-11-18](https://this-week-in-rust.org/blog/2026/11/18/this-week-in-rust-678/) 홈페이지 최신 표시 호 | [#624](https://this-week-in-rust.org/blog/2025/11/05/this-week-in-rust-624/), [#627](https://this-week-in-rust.org/blog/2025/11/26/this-week-in-rust-627/) | 동일 전문 Project/Tooling 섹션; F-Droid는 별도 C |
| ko | [GeekNews 날짜별](https://news.hada.io/past) 당일 2026-11-24 목록, [Show](https://news.hada.io/show) 최신 | [2025-11-25 날짜별](https://news.hada.io/past?day=2025-11-25) | 동일 날짜별 전체 목록 쌍 직접 확인, Show 전용 2025 깊은 페이지는 미확인. 한국어 제작자 글 별도: [orca](https://news.hada.io/topic?id=37768), [CRAMA](https://news.hada.io/topic?id=37753) |
| fr | [Framablog](https://framablog.org/) 2026-11-24 글, 11/23 Khrys’presso 등 | [2025-11 월별](https://framablog.org/2025/11/), [11/24 Khrys’presso 본문](https://framablog.org/2025/11/24/khryspresso-du-lundi-24-novembre-2025/) | LinuxFr 과거 직접 본문 실패를 숨기지 않고 프랑스어 대안 모집틀 사용. 같은 발행처 목록 쌍, 주간 큐레이션 존재; 최신 주간 개별 글 본문 재확인 미실시. |

단위=언어×최신/과거 쌍, 4/4 날짜 목록 확보, 3/4 좁은 유형 유지(ko는 사전 관심 Show→전체 일자 목록). [languages.jsonl](languages.jsonl)과 [live_observations](live_observations.jsonl), [final_attempts](final_attempts.jsonl) 원문·실패. 과거 LinuxFr/Show 전용 직접 개봉 결손은 지속. 최신 관측 캐시/제공 시점 한계 있음. 원문 언어로 기록, 저자의 국적 추론 안 함. 이 네 언어 감사는 A/B/C 적격 비교 분모 밖이다. 독립 웹서비스 CRAMA가 브라우저 PDF/이미지 변환을 소개하지만 R1~R3 적격은 아님; AI ID 사진 도구 첫 링크 실패도 포함한다.

## Q4. 요구에 맞는 실제 동작과 역사적 재평가
S1 첫 링크는 0/93 요구 쌍, 직접 0, 조건부 0. 원 5/96 조건부 및 고유 3 유지. 두 번째 제한 층도 제작자 엄격 0, C의 현재 중간 설명만 허용하면 ciphernotes 1. 아래는 별도의 비균등 추가 조사(원장 덮어쓰기 없음).

| 대상·근거 | 날짜와 확인 동작 | 요구 판정 및 제한 |
|---|---|---|
| 원 A-W1-1 ii-svn-log H17 [저자 글](https://note.com/just_vole1456/n/ncea39628b332) | 2025-11-11 21:54, SVN 기록 Excel 출력 및 외부 파일 공유 | R2 부분/R3 전이; Excel, 보드/게임 아님 |
| 원 B-W1-1 channels-console H01 [2025-11-10 고정 README](https://github.com/pawurb/channels-console/blob/a260ba23c4ca7a69d1824e6178fe50d19a65e71e/README.md) | HTTP JSON metrics endpoint/TUI, opt-in 채널 proxy, 큐 근사·버퍼 세 층 | R3 전이, 당시 판 근거 복구; 전량 게임 기록/정확 큐 아님 |
| 원 B-W1-4 Tokuin H18 [2025-11-07 저자 글](https://noos.blog/posts/tokuin-token-tooling-for-llm-builders/) | 토큰/비용/부하 분석 JSON scripts 및 CSV | R2 부분/R3 전이; CLI 분석, 원 데이터 전량 아님 |
| 원 C-W2-2 Calisthenics H21 [v1.3.0](https://github.com/Gonbei774/CalisthenicsMemory/blob/v1.3.0/README.md), H04 [빌드 검증](https://verification.f-droid.org/packages/io.github.gonbei774.calisthenicsmemory/) | 11/19 v1.3 재빌드, v1.3 README 모든 운동/그룹/기록 JSON backup export; 11/15 v1.4 확장 CSV [H02/H22](https://github.com/Gonbei774/CalisthenicsMemory/blob/a0ce0a96ee94d0dcc348bae244aa940963d9c642/CHANGELOG.md) | R2 부분/R3 전이; v1.3 CSV 입력/템플릿과 changelog의 앞선 CSV 지원 불일치. 당시 빌드 가능 판의 JSON만 확정; 실제 APK 기능 시험·정확 편입 첫 판 미확인 |
| S1 A-SW2-3 Telegram H09 [11/25 코드](https://github.com/telegramdesktop/tdesktop/commit/57411b962f2192b288641dccdf842a3b1b59f5ef) / H10 / [H11 2018 공식](https://telegram.org/blog/export-and-more) | 주제별 기록·페이지 분할/경로·공통 writer, 공식 일반 chat export JSON/HTML | R2 부분/R3 전이 **추론**; 해당 기능 JSON 결과 실행/정확 writer 검증 안 함. 삭제 민감도 별도 |
| S1 C-SW2-3 ciphernotes [H12 2024-12-26](https://github.com/rapnuss/cipher-notes/blob/a0b3f9c08f3476721d64ffe2d5eafe9e3379a996/frontend/src/state/notes.ts), [H13 2025-09-13](https://github.com/rapnuss/cipher-notes/blob/a68441b7027427f54f7baf418f34a346a2f3ae8d/frontend/src/state/import.ts) | local Dexie dirty state 및 sync 전송; JSON notes 및 파일 ZIP export, H23 focus/visibility sync | R2 부분/R3 전이; R1 현재 패키지 설명은 오프라인/재연결 충족 주장이나 2025 foreground 자동 재연결, Android 배포판 SHA는 미확인. 직접 적격 아님 |

원 날짜 고정 후보 2→4(7 조건부 쌍), S1 별도 역사 진단 2(4 쌍), 합 6(11 쌍), 역사 진단 직접 0. 원 4는 동일 비용의 새 검색 결과가 아니라 기존 후보의 추가 원문 검증이다. Telegram 형식 추론을 제외하면 5, ciphernotes 배포판 불명까지 제외하면 4. 원래 엄격한 요구와 동일 도메인 구현은 확인되지 않았다. 기존 두 메커니즘 file_export/http_json 이외의 새 메커니즘 0. [historical_judgments.csv](historical_judgments.csv)과 [history](history.jsonl), [history_addendum](history_addendum.jsonl) 연결. CGP의 가상 암호화 아카이브 serializer 예시는 실제 누적 기록 내보내기가 아니므로 제외. Patina 펌웨어·ESP-HAL·SeaORM nested ActiveModel 역시 기록 export의 증거 아님. 별도 유명 대안 대조: [Notesnook 현재 공식 sync 안내 H15](https://notesnook.com/help/sync/how-sync-works)는 텍스트 로컬 저장/연결 검출 시 동기화·모바일 지원을 명시해 현재 R1 직접 요구에 대응(전체 첨부 오프라인은 유료 등 한계); H16 2025 모바일 설정 커밋은 당시 모든 절을 증명하지 않는다. 유명 하나로 충분할 수 있는 반례이지 2025 주 비교의 직접 적격으로 추가하지 않는다.

## Q5. 비용 및 누락 분모, 민감도
| 경로 | S1 절반 실제/예정·첫 열람·적격 | S1 전량 실제/예정·첫 열람·적격 | 2단계 누적 시도/열림·엄격/완화 적격 | 역사 진단 고유 (같은 예산 아님) |
|---|---|---|---|---|
| A | 6/6·4·0 | 12/12·8·0 | 12/8·0/0 | 1 |
| B | 6/6·6·0 | 7/12·7·0 | 8/8·0/0 | 0 |
| C | 6/6·4·0 | 12/12·6·0 | 19/12·0/1 | 1 |
| 합 | 18/18·14·0 | 31/36·21·0 | 39/28·0/1 | 2 |

[24행 cost](cost.csv)와 [recalculation.json](recalculation.json) 근거. 동일 첫 3/6자리 최대 예산에서 모든 경로 단독 기여와 A 대비 추가 적격 및 새 기제/100 성공=0. 새 표본 절반→전량 추가 시도 13, 성공 7, 추가 엄격 0. B 빈 5행을 결과 없음·접근 실패와 혼동하지 않는다. 2차는 실제 8회 추가·7 성공(제작자 6/중간 1), 합계 39회·28 성공·11 실패; 제작자 엄격 0. 완화 1개/28성공=3.57/100, 1/39시도=2.56/100; C 1/12=8.33, 1/19=5.26. 절반 24시도/19성공·완화 1=5.26/100성공. 진단 2개 모두 SW2 위치3에 있으나 별도 불균등 추가 호출에 의존, 비용률 산출 불가. 기제 신규성 0/추가 열람(분모 불균등). 원 비용표 576개 수치 독립 재계산 불일치 0. 원 첫 링크 B2>A1>C0; B 빼면 A1, A 빼면 B2, C 빼면 B2>A1. 새 S1에서는 어느 하나 빼도 엄격 0. 역사 진단 A2/B2/C2, 하나 빼면 4개; Telegram 추론 제외 A1/B2/C2; ciphernotes 배포판 불명도 제외 A1/B2/C1. 두 판정은 실제 순위 뒤집힘 가능성을 보여준다. 일본어 목록 제거 시 원 A1과 S1 진단 Telegram 제거, 영어 목록 제거 시 원 A1 및 S1 진단 Telegram만 남음; 제작자 언어와 목록 언어는 다르다. 네 언어 보조 모집 제거의 적격 영향은 분모 밖이어서 산출 불가. 반복 판을 개별 자리로 세면 63, 라벨 합치면 54; 적격 6은 서로 다른 라벨, 불확실 동일성 전역 확정 아님.

호출 실측: [calls.csv](calls.csv)와 [final_attempts](final_attempts.jsonl)에 연구 호출 웹 20회/148 subrequests, GitHub 검색·원문 조회 39회, 셸 네트워크 요청 3회(연구 원장 기준, 작업관리 커밋·재열람 제외). 웹 배치 단위 UTC 전후 bracket, 개별 도구 내부 대기는 미계측; GitHub 요청별 JS 경과, 실패/0건/스키마 오류도 남김. W20 bracket 83.019초는 컨텍스트 처리까지 포함한 상한, 네트워크 지연 아님. 원 실험 호출·대기 소급 불가. git ls-remote 두 번 DNS 실패 exit 128, curl DNS 실패 기록. 정확 동일 실제 시간 비용·계약 검사 성공 주장 불가.

## Q6. 당시 노출과 rediscovery
[exposure.csv](exposure.csv)에서 2025 목록의 당시 등재 순서는 직접 관측 가능한 보존본으로 기록하지만 당시 실이용/조회/별/댓글 수와 동일시하지 않는다. 두 주 비교 전체 63 실제 자리의 2025 당시 정확 audience 수치 복구 0/63. [final_attempts](final_attempts.jsonl) 5개 archive availability lookup 접근 실패(아카이브 부재라고 추론 금지). 현재 관측 note 좋아요 3, Calisthenics mirror stars 17, ciphernotes stars 12 등은 캐시 시각과 함께 구분, 원 Magika 과거 자체보고와 단위 다름. 새 실제 조사 시점의 독립 한국어 orca 4점, CRAMA 3점은 2026-11-24 목록에서 발견 당시 표시값이며 2025 값이 아니다. 둘 다 R1~R3 적격 없음. 당시 목록의 낮은 순위/현재 적은 stars로 저노출·효용 인과 추론하지 않는다. 기능 판정에는 exposure 수치 미사용, 독립 블라인드 판독은 아님. 널리 알려진 단일 후보 Notesnook 현재 R1 대응이라는 반례는 있으나 인기도의 동일시점 지표 미확보. 오래된 CGP/esp-hal·ciphernotes의 후기 등재와 SeaORM/Electron 재등재는 rediscovery/반복을 실제 관측한 사례. 현지어 암묵지의 인과는 네 언어 감사만으로는 입증되지 않았다.

## Q7. 설계로 넘길 조건/원전 감사
원 X01/X02/X06/X07(표본관 기증/지역 zine 수집)을 다시 집계에 넣지 않고 유지. 물리 표본·zine의 기증/입수·선별·등록과 소프트웨어의 제보/편입/원문 판독은 비슷한 증거 구분이 유용하지만, 실물 소유권·접수 날짜는 복제 가능한 URL의 세계 최초와 다르다. 원전 원 83 기록(71 성공, 41 산입), 유형 14 intake/14 maker/9 operation/4 outside, 5언어/발행자 표기 29. S1 주 원전 37 기록(27 성공, 17 산입=6 intake/11 maker). 합 산입행 58, 중복 work_id 합친 기록 기준 56, 다른 관계 미확인; 역사 및 언어 추가 원문은 별도 증거로 남기고 중복 산입하지 않음. 이 수는 전세계 고유 저작이 아니다. 원 경로의 실패·노출 편향은 보존. 다음 설계 선택은 쉬운 공개 날짜 목록 우선, 필요 시 전문/배포 입구 보완, 역사 확인 별도 비용 계층을 두는 안과 단일 유명 제품 검증 우선 안을 경쟁 대안으로 유지. 순위를 확정하거나 영구 동일성/보존 정책으로 확대하지 않는다.

## 최종 판정과 남은 한계
누적 모집 부족 4자리 보완, 네 언어 날짜 목록 직접 확보, 역사 원문·현지 노출 및 실패 기록, 호출/대기 범위·비용 재검산을 실제 수행했다. 원 과제의 모든 셀 6자리·실제 동일 비용 및 당시 정확 노출 지표 확보를 거짓 완료 처리하지 않는다. B는 추가 날짜 창에도 실제 목록 수가 적었다. 계약 CLI는 DNS 실패. 따라서 원 과제 PARTIAL은 유지하되 재개 내용은 이전 단순 인계가 아니라 비교와 증거가 저장된 결과다. 아래가 남은 가장 중요한 정확히 3개 약점이다.

| 불일치·약점 | 어떤 결정에 영향을 주는가 | 다음 조사와 구할 자료 | 판단이 뒤집힐 관측 |
|---|---|---|---|
| 원 B W2 4 및 S1 B 5 구조적 결번; ko Show 전용 과거 불가로 전체 일자 목록 사용 | 동일 실제 자원·언어 경로 우위 및 모든 셀 6자리 판정 | 새 독립 사전등록 창에서 B 실제 6개 이상 확보, 한국어 동일 종류 날짜 목록 접근 및 전수 표본 | 실제 각 6개 이상 및 동일 비용에서 B/A/C의 추가 적격 차이 재현 |
| 정확 2025 노출 0/63, archive 5 접근 실패; Telegram 형식 추론·ciphernotes Android 당시 재연결/배포 SHA, Calisthenics 정확 편입판 미확인 | 저노출 효용, 당시판 직접/조건부 판정과 역사 진단 4~6 | 당시 snapshot/API metric, 원 제작자 판·MR/build SHA, JSON export 및 mobile offline/reconnect 실제 테스트, 독립 판독 | 당시 노출 자료와 정확 배포판이 새로운 적격/부적격 판정을 뒷받침 |
| 개별 웹 지연 미계측, 원 비용 시간 소급 불가, GitHub DNS 실패로 계약 CLI 미실행 | 실제 시간 비용/검증 완료 주장 불가 | 네트워크 허용 실행 환경에서 고정 SHA checkout, 계약 명령 및 개별 호출 latency·wait 기록 | CLI 통과와 같은 실제 시간 예산에서 경로별 결과 차이 관측 |
