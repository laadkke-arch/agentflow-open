# AF-RES-131 최종 인계

**DONE.** 두 옵션 계약의 경계는 공개 안정판 6.6.1 → 6.7.0이다. 같은 피처가 목록에 포함되어 있을 때 6.6.1의 거부 filter·layers는 geometry를 보존했고 6.7.0은 해당 callback을 호출하지 않고 geometry를 이동시켰다. 빈 Collection은 어느 판에서도 피처를 옮기지 못했다. 안정판 64/64의 배포 파일·소스 비교, 적격 고유 1차 저작 37개, 브라우저 본 48·대조 등 36, 두 경로에서 브라우저 84/84 일치를 기록했다. 더 오래된 5.3.3의 filter 부재, 원 앱의 미확인 판과 6.0.0의 DOM 차이는 결과에 구별했다. [결과](RESULT.md) · [출처 원장](sources.jsonl) · [공개판](releases.csv) · [실행 원장](runs.jsonl)

## 입력과 이번 구조

- 계획판 `f5279cabf578ae93dd2374adb4f6fb525ce06b9d`, 새 원격 브랜치 기준과 manifest base `adafe971a088300e3a5319f95c5341db4c27e334`. 배정 브랜치는 `work/research-af-res-131`, 소유 경로는 `docs/workstreams/research/AF-RES-131/`다. 작업환경의 기존 로컬 `work` ref와 충돌해 로컬 이름만 `codex/research-af-res-131`로 두고 지정 원격 ref에 커밋을 발행했다. [시작 범위](SCOPE.md) · [manifest](manifest.json)
- 의존 AF-RES-127 인계 `50eb2d582e8e70cf9ee5af072c606662d74a8c85`, 검산판 `cee582b227357f5935fd87eaa5e3a0e415d65cc9`. 지도 원장, Canvas 점·seed·궤적, npm 지문 구조, Playwright driver와 비교기를 재사용했다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/50eb2d582e8e70cf9ee5af072c606662d74a8c85/docs/workstreams/research/AF-RES-127/HANDOFF.md) · [선행 검산](https://github.com/laadkke-arch/agentflow-open/blob/cee582b227357f5935fd87eaa5e3a0e415d65cc9/docs/workstreams/research/AF-RES-127/RESULT.md)
- 이번 입력은 `fixture/input.json`과 예측 전에 고정한 cases·npm lock을 공유한다. 구판 Select 스타일과 제스처만 어댑터로 맞췄고, 네 판에서 같은 callback·포인터 수집기와 집계를 사용했다. 통합판과 비교한 변경 경로는 과제 폴더에 속한다. 6.0.0의 빈 overlay DOM target과 초기 PNG 차이는 로그에 남겼다. 당시 HTML API의 접근 실패는 고정 JSDoc으로 보완했다. QGIS 4행과 Audacity 3행은 별도 로컬 도구로 실행했다. [재현](reproduce.md) · [어댑터](evidence/browser/MAIN.md) · [분야 대조](evidence/cross-domain/README.md)

## 고정 검사와 GitHub 재열람

Codex Cloud의 동일 작업자가 [결과 SHA de62ead16f71041f0a1c3cc37c651a0de3d760a5](https://github.com/laadkke-arch/agentflow-open/blob/de62ead16f71041f0a1c3cc37c651a0de3d760a5/docs/workstreams/research/AF-RES-131/RESULT.md)에서 clone 경로와 SHA fetch 경로를 새로 실행했다. 상태·콜백·렌더러·bundle의 불일치는 0/84다. 76행은 전체 trace, 8행은 정착 전용이다. 시간과 Canvas readback 경고 수는 측정 차이를 따로 기록했다. 판별·배포 계보와 Q1–Q7의 반증은 같은 작업자의 자기검사다. [정규화 비교](evidence/acceptance/cross.json) · [자기검사](SELF_CHECK.md)

같은 검사의 명시 `workbench.session check … --fetch`와 `cloud_check.py --environment codex-cloud --fetch-contract --require-clean`은 각각 종료 0이다. 검사 시 통합은 `7b3eb10bb1c2581dc5d5d8258dbed44b675d5aad`다. 변경 파일 170개가 소유 범위였고 명시 검사는 manifest를 뺀 169개를 판정했다. 공통 검사의 자동 작업 목록은 `no_active_sessions`다. 함께 수행한 명시 검사가 이 과제의 계약과 의존을 확인했다. [명령·stdout·stderr·exit](evidence/acceptance/route-a/steps.json) · [공통 검사 영수증](evidence/acceptance/route-a/cloud-check.json) · [정리 영수증](evidence/acceptance/RECEIPT.md)

| 묶음 | GitHub에서 다시 연 고정판의 대표 파일 | 검사 주체 |
| --- | --- | --- |
| ① 범위·판 모집·셀 | [6c5dd2b08dfec7fd0888d3b73bce856739e17a6c · SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/6c5dd2b08dfec7fd0888d3b73bce856739e17a6c/docs/workstreams/research/AF-RES-131/SCOPE.md) | 동일 작업자, 배정·원격 파일 대조 |
| ② 배포 이력·예측 봉인 | [4aef99bcf8c6a59bf7436fc2aa32e822129fa179 · predictions](https://github.com/laadkke-arch/agentflow-open/blob/4aef99bcf8c6a59bf7436fc2aa32e822129fa179/docs/workstreams/research/AF-RES-131/predictions.csv) · [배포 이력](https://github.com/laadkke-arch/agentflow-open/blob/4aef99bcf8c6a59bf7436fc2aa32e822129fa179/docs/workstreams/research/AF-RES-131/evidence/release-history.md) | 동일 작업자, 포인터 최초 실행 전 원격 재열람 |
| ③ 브라우저 본 실측 | [dd05e22208eacb9e9362c9283f2e76bf249366fa · 본행 영수증](https://github.com/laadkke-arch/agentflow-open/blob/dd05e22208eacb9e9362c9283f2e76bf249366fa/docs/workstreams/research/AF-RES-131/evidence/browser/MAIN.md) | 동일 작업자, 패키지·브라우저 로그 검산 |
| ④ 대조·무래퍼·타 분야 | [9461d2a3a36c34c4ae102fe7bd94da95cf188dce · 대조](https://github.com/laadkke-arch/agentflow-open/blob/9461d2a3a36c34c4ae102fe7bd94da95cf188dce/docs/workstreams/research/AF-RES-131/evidence/browser/CONTROLS.md) · [타 분야 실측](https://github.com/laadkke-arch/agentflow-open/blob/9461d2a3a36c34c4ae102fe7bd94da95cf188dce/docs/workstreams/research/AF-RES-131/evidence/cross-domain/README.md) | 동일 작업자, 반례와 원격 원장 재열람 |
| ⑤ 결과 고정·두 경로·검사 | [de62ead16f71041f0a1c3cc37c651a0de3d760a5 · 결과](https://github.com/laadkke-arch/agentflow-open/blob/de62ead16f71041f0a1c3cc37c651a0de3d760a5/docs/workstreams/research/AF-RES-131/RESULT.md) · [2b41224f71bb9dab61b2f5957f8c1b6e4cfeabf8 · 수용](https://github.com/laadkke-arch/agentflow-open/blob/2b41224f71bb9dab61b2f5957f8c1b6e4cfeabf8/docs/workstreams/research/AF-RES-131/evidence/acceptance/RECEIPT.md) | 동일 작업자, 깨끗한 두 경로·공통 검사·원격 재열람 |
| ⑥ 최종 인계 | 이 파일만 추가한 별도 마지막 커밋 | 동일 작업자, 끝의 세 행·소유 경로·GitHub 재열람 |

## 첫 재개 행동

실제 프로젝트에 결과를 적용할 때는 lockfile의 정확한 ol 판과 Translate의 features 제공 여부부터 맞춘다. 그 뒤 같은 공개 결과의 ④·⑤ 원 로그에서 raw hit, predicate 인자·반환, 움직인 값을 읽는다. 원 앱 입력이나 더 넓은 비교가 필요하면 동일 두 경계판에 허용 hit와 Collection의 다른 거부 멤버를 함께 넣어 geometry 두 개를 추가 관측한다. 기준 명령과 판·입력은 [재현](reproduce.md)에 있다. [반환 조건](returns.csv) · [구형 ④](evidence/browser/main/main-6.6.1-04-r1.json) · [신형 ④](evidence/browser/main/main-6.7.0-04-r1.json)

색인 제안 — AF-RES-131 · OpenLayers Translate의 두 거부 조건·선택 목록 경계와 당시 기능 절 · DONE · [결과](RESULT.md) · AF-RES-127 고정 인계에 의존.

| 중요한 불일치·약점 | 다음에 열 자료 또는 수행할 검사 | 판단을 바꿀 관측 |
| --- | --- | --- |
| #9625 실제 앱 설치판, 목록과 전달 순서는 미확인이다. | [원 보고 후속](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656)과 해당 앱 lockfile을 읽고 같은 Canvas hit의 첫 down과 포인터 이동 한 건을 기록한다. | 설치된 판과 callback·geometry/center가 밝혀지면 원 앱의 기능 절과 보존 예측을 확정한다. |
| 본행은 한 피처다. 6.0.0 DOM 표면과 최신판의 RenderFeature 조건이 다르다. | [6.6.1 그룹 이동](https://github.com/openlayers/openlayers/blob/a8b949a802c4d79ce6fbdcbb2fe3828a83e375b3/src/ol/interaction/Translate.js#L288-L305)을 열고 허용 hit·거부 멤버, renderer와 입력 조건을 한 요인씩 바꿔 재생한다. | 다른 멤버나 다른 렌더러의 첫 hit에서 geometry·center의 범주가 달라지면 적용 조건을 좁힌다. |
| 반환 비용은 문서 절과 근거 실험 수이며 실제 채택은 미관측이다. | [세 입력과 반환 전략](returns.csv)을 실제 작성자·유지보수자에게 열고 판 확인 시간과 채택 절을 기록한다. | 추가 확인 한 번이나 변경 hunk 동봉으로 선택 절과 보호한 값이 달라지면 조건별 반환 방식을 조정한다. |
