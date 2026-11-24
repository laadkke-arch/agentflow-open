# 결과 고정판 수용 검사

검사한 SHA는 [de62ead16f71041f0a1c3cc37c651a0de3d760a5](https://github.com/laadkke-arch/agentflow-open/blob/de62ead16f71041f0a1c3cc37c651a0de3d760a5/docs/workstreams/research/AF-RES-131/RESULT.md)다. 동일 작업자가 새 저장소·npm cache·Chromium 컨텍스트에서 자기검사했다. [재현 진입점](../../reproduce.md) · [변경 경로 170개](changed-paths.txt)

| 경로 | checkout과 실제 UTC | 기준 원 로그와 비교 | 실행·환경 |
| --- | --- | --- | --- |
| A | GitHub 과제 브랜치 clone 뒤 결과 SHA detach. 2026-11-24 10:44:52.107–10:46:19.830 UTC | 본 48/48, 대조 16/16, 보충 12/12, 정착 전용 8/8 일치. 경고 횟수 차이 7/84. | [실행 명령](route-a/commands.log) · [stdout/stderr/exit](route-a/steps.json) · [경로 비교](route-a/compare.json) · [지문](route-a/environment-all.json) |
| B | 빈 Git 저장소에서 결과 SHA만 shallow fetch 뒤 detach. 2026-11-24 10:47:06.934–10:48:35.524 UTC | 본 48/48, 대조 16/16, 보충 12/12, 정착 전용 8/8 일치. 경고 횟수 차이 10/84. | [실행 명령](route-b/commands.log) · [stdout/stderr/exit](route-b/steps.json) · [경로 비교](route-b/compare.json) · [지문](route-b/environment-all.json) |

A와 B 사이에서도 84/84행의 입력·hit·결과·렌더러·bundle과 기록의 순서가 같았다. 이 중 76행은 콜백 인자·반환·순서·횟수까지, 8행은 래퍼 없는 정착만 대조했다. raw 시각은 따로 놓았다. 관측한 76개 down→settled의 B−A 차이 범위는 −17.1~+33.3ms, 중앙값 0.0ms다. Canvas2D readback 경고의 횟수는 9/84행에서 달랐다. 비교 종료값은 0이다. QGIS·Audacity 원 파일과 PNG는 양쪽 checkout에서 감사했으며 두 분야의 GUI 입력은 별도 4행과 3행을 사용했다. [A↔B 정규화 SHA·시각 차이](cross.json) · [비교 stdout](cross.stdout) · [비교 종료값](cross.exit) · [A 재집계](route-a/recount.json) · [B 재집계](route-b/recount.json)

명시 세션 검사는 위 결과 SHA, base `adafe971a088300e3a5319f95c5341db4c27e334`, 검사 시 통합 `7b3eb10bb1c2581dc5d5d8258dbed44b675d5aad`에서 통과했다. 원격 최신성과 AF-RES-127 의존성을 확인했으며, manifest를 뺀 169개 변경 경로를 판정해 소유 범위 밖 0개를 기록했다. 저장소 공통 검사도 같은 깨끗한 SHA에서 시작해 doctor, acceptance, research-case, original-smoke 및 sessions의 각 종료값 0을 저장했다. 공통 검사의 자동 작업 목록은 `no_active_sessions`이고, 이 과제의 소유·의존 계약은 별도 명시 검사로 검증했다. [세션·저장소 공통 stdout/stderr와 종료값](route-a/steps.json) · [공통 검사 영수증](route-a/cloud-check.json)

결과 SHA에 저장한 모집·아카이브·분기 코드로 당시 packument 및 검증한 64개 tarball을 다시 읽었다. 공개판 CSV와 사전판 CSV는 원장과 바이트가 일치했다. 다른 분야 매뉴얼은 웹에서 본문을 재확인했다. 셸 경로의 QGIS 편집·Audacity 클립·동기화 문서는 HTTP 403이므로 웹에서 성공한 열람만 원장 수에 포함했다. [배포 재검산 stdout](release-recount/stdout.log) · [stderr](release-recount/stderr.log) · [종료값](release-recount/exit.txt)
