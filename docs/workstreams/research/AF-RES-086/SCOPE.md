# AF-RES-086 — 사전 범위·판정 규칙

## 기준

- 계획 기준 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`; 실제 시작 통합판 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`.
- 계획 기준의 dot-control에는 AF-RES-086 행이 없었다. 실제 시작 통합판에서 RUNNING, 의존 AF-RES-082, 본 요청과 같은 brief를 확인했다. 계획 SHA를 실제 시작 SHA로 바꾸어 보고하지 않는다.
- 유일 선행 결과 `work/research-af-res-082@1f8bf039ad4f9a38b99764a11f72b515facef39c`. HANDOFF, requirements.csv, deployments.jsonl, cards.md, streams/python·r의 관련 행을 읽는다. 같은 회차 결과는 사용하지 않는다.
- 브랜치 `work/research-af-res-086`; 유일 쓰기 범위 `docs/workstreams/research/AF-RES-086/`. 중앙 상태와 다른 브랜치는 변경하지 않는다.
- `python -B -m workbench.session start af-res-086 --allow docs/workstreams/research/AF-RES-086/ --dependency work/research-af-res-082=1f8bf039ad4f9a38b99764a11f72b515facef39c --output docs/workstreams/research/AF-RES-086/manifest.json --fetch` exit 0, remote_checked.
- 실제 환경은 셸·공개 HTTP·GitHub connector가 제공된 현재 작업공간이다. 배정 worker_kind=web-pro와 별도의 웹 UI Pro 실행 확인을 혼동하지 않는다.

## 고정 네 자리와 관측창 (UTC)

| 자리 | 소스 / 생성·게시 입력 | 주 관측창 |
|---|---|---|
| P3 cibuildwheel v3.3.0 | source `63fd63b352a9a8bdcc24791c9dbee952ee9a8abc`; RTD 30298914,30298916; 1.x 14073318 | [2025-11-11T00:00:00Z,2025-11-14T00:00:00Z) |
| R1 archive v1.1.12 | source `a4c6ec37fc8737a189ca7ec7095ec0161888f9e8`; HTML `45e0d9ebc168cf3632bc2d737c9db2318668a826`; Pages 2328795124 | [2025-03-24T00:00:00Z,2025-03-27T00:00:00Z) |
| P1 bandersnatch 7.0.1 | source `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74`; latest 30720077 | [2025-12-16T17:51:34.578405Z,2025-12-19T17:51:34.578405Z) |
| R2 asciicast 2.3.1 | source `f992b26f3cb30c799fbb95f6148852d8ae8a7f18`; HTML `92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1` | [2024-01-21T20:53:46Z,2024-01-24T20:53:46Z) |

P1의 생성시각은 선행 원장의 build finished(생성 완료), R2는 output commit 시각으로 사전에 선택한다. 시작시각과 완료시각을 섞지 않는다. 주 사례의 자료 공석에는 시작 -30일 / 종료 +30일까지만 보조 검색하며 main/supplemental/current를 별도 기록한다. 과거 1.x 생성은 ancestry 증거이며 2025년 응답으로 승격하지 않는다. 고정 네 자리는 교체하지 않는다.

## 결합 규칙과 사전 후보

1. 소유자의 원문 약속과 연구 가정을 별도 claims 행으로 둔다. stable, 1.x, options/#enable, root, named tag는 서로 다른 경로다. 공개 URL 하나는 영구 보존·불변 바이트·구판 유지기간의 약속이 아니다.
2. source → build → artifact → deployment → route response를 각각 별도 사건으로 기록한다. SHA가 같아도 두 run 중 하나를 임의 선택하지 않는다. build-success가 별도 publish-success나 과거 HTTP 응답을 대체하지 않는다.
3. 직접 받은 바이트의 SHA-256, git blob ID, 발행자 제공 checksum/commit/version metadata는 필드와 관측 주체를 분리한다. 현재 Last-Modified는 현재 서버의 진술이며 과거 관측 영수증이 아니다.
4. 동시 제공 양성은 동일 시점의 두 경로 응답, 또는 경로별 내용 식별이 있는 두 게시 유효구간의 교집합으로 판정한다. 서로 다른 날짜의 200 두 개, 오래된 build와 현재 응답만으로 양성을 만들지 않는다. 반증에는 해당 조건을 직접 어긴 원행이 필요하다.
5. 과거 최종 상태는 해당 창의 상태 순서로 읽는다. 나중의 inactive·재게시·삭제·현재 실패는 과거 성공과 별도다. 빈 배열·403 quota·404 삭제 로그는 기록 부재/접근 실패이며 배포 실패로 집계하지 않는다.
6. 비교 후보는 이동 별칭 / 고정판 / 생성물 / 유보로 고정한다. 현재 URL과 서비스 도움말에 제한된 사전 권고를 먼저 커밋한 뒤 역사 조사 권고를 작성한다. 의존 보고서의 결과를 이미 안다는 한계가 있으므로 독립 맹검 실험·성능 우월성으로 부르지 않는다.
7. 사건 표본은 네 자리와 분리한다. 2024–2025의 mike/MkDocs/RTD/GitHub Pages 공개 사건에 사전 검색식을 고정하고, 회수 후보를 생성 UTC→이슈 번호 순서로 읽어 첫 12고유 사건과 제외 이유를 남긴다. 사건당 이슈·댓글·PR·로그는 한 계보로 센다. strong=성공한 생성+성공한 게시+동일 ref의 틀린 독자 응답+회복 뒤 올바른 판 연결. 공석은 0으로 남긴다.
8. 외부분야는 두 제도의 실제 판 쌍 최소4기록과 양쪽 파일/manifest를 직접 읽는다. 정책은 실제 기록과 별도 역할이다. 같은 저작의 여러 판은 한 계보다.

## 분모·완료·검산

- 고정 자리 4, 소유자 두 조건 원 분모 1/6(082 원 모집), 이번 고정 표본 1/4. 새 원문으로 바뀌면 원문과 사후 변경을 표시한다.
- 제공자 성공 보고 배포, 당시 판을 식별한 경로, 두 조건 공동 확인의 분모를 따로 둔다. 경로 기본 슬롯=P3 stable/options/#enable·1.x·v3.3.0/options/#enable, P1 latest·7.0.1, R1 root·reference/archive_read.html, R2 root·articles/asciicast-demo.html: 9슬롯. 루트 부가 확인은 별도 행으로 두되 분모를 임의 늘리지 않는다.
- 고유 원자료≥24, 같은 저작/사건을 합쳐≥20계보. 검색 요약·실패·미러·제목만 확인은 불산입. 직접 원문 확인 여부와 source_id를 검산한다.
- R1 당시 최종 상태와 P3 두 경로를 판단할 수 있고 최소자료량 충족하면 REVIEW_READY(양성/반증 무관). 공석이 남으면 대체 공개근거와 대조를 끝낸 뒤 원분모를 유지한 PARTIAL.
- 순서: ① 범위·창·결합 규칙 ② 원 요구·현재 근거 사전 권고 ③ 역사·사건·타분야 원장 ④ 비교·카드·표·자가검산·원격 재열람 ⑤ HANDOFF 단독.
- 인계 전 `workbench.session check manifest.json --fetch`, 범위·원장 참조·분모·사전 권고 불변을 검사한다. 현재 서비스 신규 빌드/배포, 계정·권한·유료 API 변경은 하지 않는다.
