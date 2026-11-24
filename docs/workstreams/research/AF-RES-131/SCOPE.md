# AF-RES-131 조사 범위와 입력

어느 공개 `ol` 배포에서 Translate의 `features`가 피처 조건 `filter`와 레이어 조건 `layers`보다 우선하며, 같은 Canvas hit의 첫 마우스 조작에서 geometry와 view center가 어떻게 갈리는지 확인한다. 탐색기가 설치판에 맞는 기능 절을 반환하려면 버전·목록 유무·보존 상태 중 무엇을 알아야 하는지도 비교한다.

- 계획판 `f5279cabf578ae93dd2374adb4f6fb525ce06b9d`. 배정 확인에서 읽은 통합 head `eb74eadc59e5b22239684615db0a9e8241aabd39` 이후 Dot 표만 변경됐다. GitHub에 과제 브랜치를 생성한 기준판과 manifest base는 `adafe971a088300e3a5319f95c5341db4c27e334`다. 작업 범위는 이 폴더다. [배정표](https://github.com/laadkke-arch/agentflow-open/blob/adafe971a088300e3a5319f95c5341db4c27e334/docs/automation/dot-control.json) · [manifest](manifest.json)
- 선행 인계 `50eb2d582e8e70cf9ee5af072c606662d74a8c85`, 검산판 `cee582b227357f5935fd87eaa5e3a0e415d65cc9`. 10.11.0의 filter 우회 실측과 6.0.0의 조합 소스는 사전 정보다. 이 시점에 131의 브라우저 입력을 실행한 횟수는 0이다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/HANDOFF.md) · [선행 검산](https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/RESULT.md)
- 같은 SHA의 지도 원장·fixture 지문·plan·reproduce·driver를 읽었다. Toggle 두 개를 같은 후보에 제공하는 6셀과 경계판을 추가한다. 기존 시험의 8셀·차트 예측·#9625 앱은 이전 자료를 참조한다. [원장](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/evidence/map-sources.md) · [지문](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/fixture/fingerprints.json) · [입력](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/plan.json) · [재현](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/reproduce.md) · [driver](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/replay/drive.mjs)

## 배포와 원전 단위

2026-11-24 10:04:35 UTC의 npm packument 표본이다. `6.0.0 ≤ x.y.z ≤ 10.11.0`과 안정판 형식에 맞는 공개판 64개를 모집했다. semver 순위와 실제 publish 순위를 서로 다른 열로 기록한다. 숫자 기준 세 부분이 범위 안인 사전판 3,941개는 별도 표에 있다. 조사 단위는 안정판 1개와 옵션 1개의 조합이다. gitHead, tag 객체·대상 커밋, release 날짜, tarball integrity와 실제 Translate 모듈을 각각 확인한다. 동일 바이트는 SHA-256 단위로 묶고 다르면 분기를 읽는다. 유지보수 줄·늦은 공개·이전 tarball을 다시 쓴 정황은 별도로 표시한다. 등록소에서 사라진 판이나 이전에 바뀐 바이트의 역사는 현재 스냅샷 한 건으로 알 수 없다. [안정판](releases.csv) · [사전판](evidence/prereleases.csv) · [모집 영수증](evidence/roster.json)

직접 읽은 고유 1차 저작의 목표는 구현/API ≥6, 테스트/예제 ≥4, PR/원 보고 ≥4, 배포/환경/입력 ≥4, QGIS ≥3, Audacity ≥3이다. 같은 웹 본문에서 버전·태그·미러만 다르면 하나로 센다. 검색 결과·메타데이터 전용·접근 실패는 수량에서 뺀다. 지도 실행은 QGIS·Audacity 문서·실연과 분모를 공유하지 않는다.

## 브라우저 셀

| 셀 | Translate에 공급하는 목록 | 피처 filter | 레이어 predicate |
| --- | --- | --- | --- |
| ① | 속성 생략 | 허용 | 허용 |
| ② | 속성 생략 | 거부 | 허용 |
| ③ | 속성 생략 | 허용 | 거부 |
| ④ | parcel-01을 넣은 Collection | 거부 | 허용 |
| ⑤ | parcel-01을 넣은 Collection | 허용 | 거부 |
| ⑥ | 빈 Collection | 허용 | 허용 |

앵커 6.0.0·10.11.0, 각 옵션의 인접 경계 양쪽을 합집합으로 선택한다. 경계가 여러 곳이면 각 옵션의 최초 변화와 되돌림 한 곳을 우선한다. 판당 본 6셀 × 깨끗한 컨텍스트 2개다. 배경 드래그와 무이동 클릭은 판당 2회씩 추가한다. 양성 2회는 본 ①을 참조한다. 같은 점의 문턱 이하 이동과 Translate 등록 제외는 최초 경계의 두 판에서 보충한다. 경계에서 ④·⑤는 라이브 관측을 끄고 각 2회 다시 보내며, 공급한 predicate를 유지하고 콜백/핸들러 래퍼를 제거한다. 옵션 부재는 공급 의도 및 실제 기본동작과 함께 기록한다. [고정 입력](fixture/input.json)

같은 720×460 CSS 뷰포트, 지도 rect (24,20,640,400), DPR 1, EPSG:3857, center (0,0), 해상도 2·회전 0이다. hit `parcel-01/owned`는 (-128,80), 시작 client (280,180)이고 배경은 (280,280)이다. 드래그 상대 이동은 (1,0),(4,2),(12,7),(24,13),(36,20) CSS px, 각 단계에 자연 rAF 2회, up 뒤 330ms 대기한다. `Select({style:null})`을 사용하고 선택 포함은 hover 전에 seed 127과 선행 fixture의 `getFeatures().push(feature)`로 준비한다. 등록 `[Select,DragPan,Translate]`에서 Translate가 먼저 down을 처리한다. 양쪽의 primary/no-modifier 의미와 kinetic이 없는 배열을 확인한다.

관측 단위는 판 × 셀 × 반복 × 단계다. raw hit와 실제 callback 후보·인자·반환을 따로 잡는다. down, 첫 pointermove, 최초 상태 변경, up, 정착에서 ID·geometry·center·해상도·회전을 비교한다. 세계 좌표의 성분별 절대차 > 10⁻⁶ EPSG:3857 단위가 변화다. CSS 픽셀 10⁻⁶ px, 해상도 10⁻⁹ 지도 단위/px, 회전 10⁻⁹ rad를 각각 쓴다. callback은 단계별 순서와 횟수를 남기고, 본 예측에는 down/전체 최소 횟수와 0회를 구분한다. 실제 누름과 첫 변경이 가려진 예측은 새 브라우저 입력 전에 커밋한다. 구현에 근거한 예측이며 문서·소스에 대한 가림 시험은 아니다.
