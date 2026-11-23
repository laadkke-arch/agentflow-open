# AF-RES-103 최종 인계

**COMPLETE · 자가검토 완료.** K/M/P 30자리를 실행했다. 약속 충족 20, 실패 10, 미실시 0이다. K 2/10, M 8/10, P 10/10이다. 자연 T2는 P의 2/6, 원 교정 T0/T1은 10/12, 구성 T3/T4는 8/12다. 의미 반복은 15/15쌍이다. 출력이 있는 10쌍의 HTML·SVG가 바이트 일치했고 PDF는 0/10쌍이다. 14개 보조 실행과 두 다른 분야 비교는 별도다. 직접 읽어 산입한 고유 1차 자료는 33개다. [결과의 필수 표](RESULT.md) · [원장](runs.jsonl) · [검산](evidence/verification.json) · [출처 원장](sources.jsonl)

K는 원 그림을 격리해 표시했으나 T1의 AFControl, T3/T4의 AFTrack을 읽지 못했다. M은 각 그림 위치의 선언 목록으로 T1/T3/T4의 그림과 검색 가능한 본문을 보존했다. 둘째 재정의를 빼거나 닫힌 그룹 정의를 넘기면 종료 0·정상 HTML에서도 뒤 그림이 오색이었다. T2는 자연 문서의 27개 투영을 P로 보존했고, K는 첫 axis 컴파일에서 실패했다. M은 T2의 매개변수·반복을 발견해 자식 컴파일 전에 멈췄다. P의 페이지 이미지는 오프라인 단일 파일 이동 후 보였으며 호스트 본문 선택은 0이었다. [원소별 비교](evidence/ELEMENTS.md) · [T2 판정](evidence/matrix/T2-M-1/admission.json) · [T4 범위 대조](evidence/controls/T4-M-leak-inner/browser.png) · [SVG와 DOT](evidence/CROSS_DOMAIN.md)

## 저장판과 계약

저장소 laadkke-arch/agentflow-open, 브랜치 work/research-af-res-103, 허용 경로 docs/workstreams/research/AF-RES-103/. 시작 통합 커밋은 ac7abc85e12b3a5b5f87b694d00e9511332fe272이다. 계획판 ace1a06a13ea435f5cb6a3e340ad24f03f68ecae 이후 관련 변경은 중앙 진행표 하나다. 운영 의존 099 원격 끝과 등록 인계는 8426e3511114fd36a00fc57bc270cfe3f5d573c8, 연구 자료는 099 결과 01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7와 096 봉인 Lua의 1d399f630930d2763459e16509c5224b0cded9a0이다. 099 결과와 인계 차이는 HANDOFF.md 추가 한 건이고, 사용 blob은 양쪽에서 일치했다. [시작 계약](manifest.json) · [비교 원장](inputs.json)

| 묶음 | 푸시 후 원격에서 확인한 SHA | 봉인 UTC / 변경 경로 |
| --- | --- | --- |
| ① | [cddcd7fa51f8a64afbf671ca9e1fe5958429d8c9](https://github.com/laadkke-arch/agentflow-open/commit/cddcd7fa51f8a64afbf671ca9e1fe5958429d8c9) | 21:59:05 커밋. 입력·기대 좌표·정의 목록·사전 계획 14개 |
| ② | [398492443e6cd0fd73a2dc46eb1b1cf7ef7d2a6a](https://github.com/laadkke-arch/agentflow-open/commit/398492443e6cd0fd73a2dc46eb1b1cf7ef7d2a6a) | 22:07:08 커밋, 원격 22:07:11. 기준 PDF·도구·교정·실행기 178개 |
| ③ | [5d89eeddcba539bb4ff88838d845aa190982640c](https://github.com/laadkke-arch/agentflow-open/commit/5d89eeddcba539bb4ff88838d845aa190982640c) | 22:09:51 커밋, 원격 22:09:55. 30자리·14개 대조·교차 분야 1,138개 |
| **④ 결과** | [41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd](https://github.com/laadkke-arch/agentflow-open/commit/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd) | 22:30:38 커밋, 원격 22:30:41. 표·출처·재현·반복·자가검토 17개 |
| 인계 | 이 파일의 단독 커밋 | ④ 검사 및 원격 재열람 뒤 작성 |

모든 시각은 2026-11-23 UTC다. ①–③의 개별 경로와 입력 봉인은 [묶음 원장](evidence/commit-files.json)에 있다. ④까지 범위 변경은 허용 폴더의 1,344개뿐이다.

## 결과 SHA의 실제 검사

검사 대상은 ④ 41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd다. 처음과 끝 모두 동일 SHA의 clean checkout을 확인했다. 검사 시 통합 원격 끝 e01dd119d08dcb6aa744ffbdf3c56c9640cd4efd까지의 추가 차이는 중앙 진행표였으며 계약 지문 19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc는 일치했다. 099 원격 끝은 운영 핀과 일치했다.

| 실제 명령 | UTC · 종료값 · 범위 | stdout SHA-256 |
| --- | --- | --- |
| python -B -m workbench.session check docs/workstreams/research/AF-RES-103/manifest.json --fetch | 22:31:26.718–22:31:27.999, 0. remote_checked. 자체 manifest 제외 변경 1,343, 범위 밖·미병합·오류 각각 0 | cffe05cdf98a9ad5dcd47ef425be7709f7bc0959360dbfa28c28ab4a47bd615e |
| python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean | 22:31:28.001–22:31:42.117, 0. doctor·acceptance·research-case·original-smoke가 통과했다. 공통 check-all의 활성 세션 자동 검사는 not-executed/no_active_sessions, 실제 0, freshness not_checked | 9536f6920088929120d7fad6d8d54eeda9f7e41e157c78ecb4563e166b041af1 |
| python -B docs/workstreams/research/AF-RES-103/verify.py | 22:31:42.119–22:31:45.077, 0. 주 30·보조 14개 원장의 1,049 파일 지문, PDF·화면 명제와 반복 쌍 검산 | 4eba959638b4d8888f50f62b98cea8c0e97b70b9591d8e612dd756141116559f |

세 명령 stderr는 비어 있었다. 22:31:28.562에 GitHub에서 ④를 새 bare 저장소로 가져온 뒤 38개를 다시 열어 **38/38 바이트 일치**를 확인했다. 필수 표 5/30/5행, 마지막 약점 3행, 재현 명령과 T2 원 TeX·14쪽 PDF, 대표 SVG/HTML·화면·DOM 및 대조를 대조했다. RESULT blob은 fcf617698e6d7d4815587408d1bdf1e1146aeb6d, reproduce는 37f4d2a86ad1d94a4739f8abd6677e295791599b, 원장은 752181666f59d52c222ccf8aae9eddd3a12ff545다. GitHub 커넥터의 고정 파일 읽기에서도 대표 문서와 원 입력·DOM·미지원 판정을 재열람했다. [GitHub ④ 결과 디렉터리](https://github.com/laadkke-arch/agentflow-open/tree/41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd/docs/workstreams/research/AF-RES-103)

## 미실시와 재개

Chromium file URL은 정책에서 차단됐다. Chromium 오프라인 로컬 바이트 라우팅과 HTML 단독 파일 이동을 확인했다. 099와 네 주요 도구 바이너리 지문은 동일하며 시스템 pdflatex.fmt 지문은 다르다. 밝은 선과 이중원 경계에서 보조 픽셀 판정이 한 번 틀렸고 원 화면·확대·원 좌표를 대조해 고쳤다. 스크린 리더, 실제 타인 독립 검토, WPT 공식 하네스와 Graphviz 상류 C++ 하네스는 미실시다. [환경 교정](evidence/CALIBRATION.md) · [픽셀 검산 수정](evidence/visual-probe-recheck.json) · [자가검토](SELF_CHECK.md)

재개 첫 행동은 ④의 [T2 L21–69](evidence/inputs/T2.tex#L21-L69)와 [독립 페이지 첫 쪽](evidence/reference/T2/pdf-page-01.png)을 열어 g01 view=(0,50)만 재편집하는 시나리오에 필요한 호출원과 패키지를 고르는 것이다. 기존 비교를 재생하려면 [재현](reproduce.md)의 도구 지문과 새 출력 폴더를 사용한다.

**색인 제안** — AF-RES-103 · COMPLETE · 부분 그림의 위치별 TeX 선언과 페이지 외관·본문의 분리 · 30자리 중 K 2/10, M 8/10, P 10/10 · 자연 T2 27 그림/14쪽 · 고유 1차 자료 33 · 결과 41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd · [RESULT](RESULT.md)

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| 자연 입력이 T2 하나이며 27개 그림이 동적으로 전개된다 | 다음 순서의 unittest_3d_1과 T2 g01의 펼친 호출을 각각 식별해 그림 장면과 XML을 대조 | 원 조각과 구체적 호출값으로 크기·색·촉·제목의 대응을 재현해 T2를 편집 가능한 반환 대상으로 분류 |
| M의 행 선택은 수동이며 단순 명시 범위에서 확인했다 | 동일 스타일명을 삼중 그룹에서 가리고 종료 후 다시 쓰는 원문과 그림별 사용자 목록 | 올바른 위치별 목록이 세 단계 모두 색·방향을 보존하고, 선언 없는 경로의 그릇된 상속을 구별 |
| P의 페이지 외관과 검색 가능한 본문·접근성 사이에 간격이 있다 | P 페이지 img와 실제 텍스트/그림 대체 설명을 담은 단일 HTML을 오프라인 Chromium과 Orca에서 평가 | 원 그림·본문 순서·키보드 선택·스크린 리더 대체 설명이 모두 확인되면 접근성 목적 반환에 포함 |
