# AF-RES-265 범위와 사전 합격표

## 입력판과 노출 순서

- `work/research-af-res-265`는 GitHub에 해당 ref가 없음을 확인하고 새 checkout의 통합 head `c64c54d2aae4045b0e2a28a1fdfca9f9313de765`에서 만들었다. 작업 종류는 Codex Cloud 실행·검사, attempt 1이다. 소유 경로는 `docs/workstreams/research/AF-RES-265/` 하나다. [착수 통합판 진행표](https://github.com/laadkke-arch/agentflow-open/blob/c64c54d2aae4045b0e2a28a1fdfca9f9313de765/docs/automation/dot-control.json)
- 요청 기준판 `933a0f7d534314470c083b0aa284044a9ad45443`의 control blob은 `c047d0da888ed4fa993cc97d749fdcd7d2c4da67`. 253행에서 본인 행은 미등록, AF-RES-247은 DONE과 합의 SHA를 확인했다. 착수판 blob `b33c62aab6f9db2ce3b2d5305633acba0fb7faf7`에서는 본인 RUNNING, `af-res-265`, attempt 1, branch·owned_path 일치, `depends_on=[AF-RES-247]`, source/result null을 확인했다. [요청 기준 진행표](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/automation/dot-control.json)
- 2026-11-25 00:57–00:59 UTC에 GitHub의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 클라우드·협업 절차를 읽고, 직접 의존 결과 `72657241644860b35c01c5ab7a68ff2e9b7db6b5`의 HANDOFF 및 RESULT·bundles의 관련 부분을 읽었다. 중앙 DONE과 작성자 PARTIAL을 구분한다. 이 과정에서 Box/BoxTextured의 기존 GLB chunk·PNG 바이트, Lamp GLB 크기/예상 blob과 분리판 참조, PNG/KTX2 필수 확장 가설, EPUB 후보, 기존 렌더·오프라인 실행 0/9를 이미 보았다. 아래 예측은 이 노출을 포함한다. 이번 표본 원바이트, 새 파서 출력과 브라우저 결과를 열기 전에 본 판을 고정한다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/72657241644860b35c01c5ab7a68ff2e9b7db6b5/docs/workstreams/research/AF-RES-247/HANDOFF.md)
- `workbench.session start`에서 원격으로 계약 v2와 정확한 의존 SHA를 확인했다. [계약 핀](session.json) · [시작 영수증](receipts/session-start.json)
- 기준 [RESEARCH_BRIEF](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/product/RESEARCH_BRIEF.md)와 [RESEARCH_WORKFLOW](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/RESEARCH_WORKFLOW.md)를 적용한다. 242, 251, 254, 255를 의존·대기·정답 판정에 쓰지 않는다. 지도·SVG·LOD와 EPUB 일반 조사도 표본 밖이다.

## 단위와 실행 설정

고정 표본은 Khronos glTF-Sample-Assets `e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea`의 Box, BoxTextured, AnisotropyBarnLamp다. 주검사 단위는 (모델, 목적, 회차) 18개다. G는 원본 GLB 로더의 primitive 속성 배열과 두 바이트 판독기의 일치, R은 공식 외부 `glTF/` 구성의 정상 재질 장면, O는 해당 원본 GLB 하나와 로컬 런타임만 제공하는 오프라인 렌더다. G의 이미지 요청·콜백도 기록한다. G에는 표시 판정이 적용되지 않는다. 공식 외부 glTF의 POSITION/indices 판독과 이미지 없는 최소 기하 구성의 로더 실행을 별도 대조한다. 각 관측은 새 브라우저 컨텍스트에서 반복한다. 추가 회차의 통제와 두 번째 빈 폴더 재생을 18개 실적에서 제외한다. [고정 자산 트리](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/e124e8d8d7330a5372bc2b4d00d39a4a9d7997ea/Models)

실행 선택은 Debian 13 x86-64, Python 3.12.14, Node 24.22.1, Chromium 156.0.8078.79 headless WebGL2 ANGLE SwiftShader, Playwright Core 1.56.1, Three.js 원판 `084ec06444244980752a420f0e1af5cd8f112aa1`의 GLTFLoader와 동판 KTX2Loader 및 Basis JS/WASM이다. Khronos validator는 npm `gltf-validator@2.0.0-dev.3.10` 고정 후보이며 독립 참고로 실행한다. Python struct/JSON와 JavaScript DataView/JSON은 서로의 결과를 입력으로 쓰지 않는다. 실제 GPU 문자열, 번들 해시, 실행 옵션과 달라진 선택은 영수증과 변경 이력에서 확인한다.

장면은 384×384, 배경 #171b22, sRGB 출력, NoToneMapping, 카메라 (3, 2, 4)에서 원점 주시, FOV 35°, near 0.1/far 100이다. 모델의 월드 AABB 중심을 원점에 맞추고 최장축을 2로 균일 조정한다. 원좌표 판독과 해시는 변환 전 배열을 사용한다. 고정 방향광·환경 조명은 재현 코드에 수치로 남긴다. 빈 프레임 대비 채널 최대차 ≥3인 픽셀 수·평균색, 전체 RGBA8 SHA-256, draw callback과 삼각형 수를 같이 기록한다. 이 설정은 작가 스크린샷과 픽셀을 맞추는 시험이 아니다.

loopback HTTP의 회차별 allowlist로 모델·런타임 제공 파일을 분리한다. 런타임·모델·합성 대조 외 파일 요청은 파일이 없도록 하고, 페이지/워커의 외부 HTTP를 차단한다. 브라우저의 새 격리 컨텍스트, 비활성 캐시와 서비스 워커 차단을 사용한다. 자체 차단 probe를 따로 실행한다. 요청, 응답 상태, 실패 이벤트, loader callback, 텍스처 연결, 프레임을 독립 열에 보존한다.

자료 단위는 실제 열람한 서로 다른 원저작 또는 핵심 자원이다. 지원 문서/트리/재게시·동일 바이트 운반판·정해진 회차를 고유 자료 수에 섞지 않는다. 지명 표본 원바이트/핵심 자원 7, 규범·공식 원자료 4, 실행판 구현·디코더·검증기/시험 6, 소비 사례·EPUB 4 이상이 목표다. Box 계열의 공유 기하, Lamp의 반복 BIN·재인코딩, EPUB 한 권의 여러 요소는 원장에 계보로 연결한다. 실패와 인용 위치도 남긴다.

## 경쟁 예측과 판정 기준

| 질문 | 첫 예측 | 뒤집을 관측과 통과 조건 |
|---|---|---|
| Q1 원본과 컨테이너 | 두 작은 모델의 선행 관측을 재현할 수 있다. Lamp는 크기만 알려져 있고, GLB의 PNG 또는 KTX2 및 URI 구성은 열어봐야 한다. | 동일 경로의 고정 tree blob·길이와 원바이트 Git blob·SHA-256 확인. 두 파서의 magic/version/length, 각 오프셋·길이·pad 바이트 일치. 불일치면 해당 변형/판 분리. |
| Q2 실제 기하 | 분리판·내장판이 대표 POSITION/indices를 공유한다. 기하 전용 조합에서는 이미지가 없어도 값이 나온다. | 두 정적 경로와 실제 loader 배열에서 count, 첫/끝, min/max, bounds와 논리 배열 바이트 지문 일치. 재직렬화·좌표값·인덱스가 다르면 정확한 수준의 일치만 남김. |
| Q3 재질 | Box의 이미지 공석은 정상, BoxTextured와 Lamp는 그림 소비 후 draw. 같은 기하라도 텍스처 조건에 따라 픽셀이 바뀔 수 있다. | callback·material 슬롯과 실제 draw·비배경 픽셀을 독립 검증. callback 성공과 배경뿐인 프레임, 기하 일치와 이미지 탈락을 성공과 분리. |
| Q4 오프라인 | Box 두 모델은 모델 파일 추가 요청 0 예상. Lamp의 닫힘과 실제 표시를 모두 측정해야 한다. | 브라우저/서버 양측에서 GLB 외 model request 0이고, 지정 모델 200, callback 성공, draw와 비배경 프레임이 있어야 해당 회차 성공. 추가 요청을 회피해 배경만 그리는 경우 탈락. |
| Q5 PNG/KTX2 | 같은 Lamp JSON에서 decoder 설정만 바꾸면 required BasisU 경로는 성공/실패로 나뉜다. 별도 PNG는 같은 파일의 자동 대체가 아니다. | required와 core source, 실제 요청, decode 완료/실패, 연결된 texture/image, frame 비교. 조건부 core source 합성 입력으로 같은 JSON에서 capability에 따른 선택 반례를 따로 검사. |
| Q6 합성 반례 | URI 선언·실제 요청·선택은 서로 다를 수 있다. 외부 URI가 합법인 GLB가 한 파일만으로 기하를 회복하지 못할 수 있다. | 그림 선언을 유지하되 material edge만 제거하고 PNG 제공 여부 비교. 외부 buffer GLB에서 같은 GLB + buffer 제공/미제공을 비교. 원형·합성과 validator/loader 판단 구분. |
| Q7 출판물 | Creative Commons Shared Culture 고정판에서 OPF 항목과 XHTML의 사용 간선을 둘 다 확인할 수 있다. 컨테이너 포함, 선언, 선택은 다른 관측이다. | 샘플 고정판 `7651e2002b631e6577fadf7e9e0692fa6efb8746`의 OPF→spine→XHTML→영상/텍스트트랙을 두 로컬 추출 경로로 비교. 동일 해시의 archive 입력을 쓰고, 빈 폴더에서 Lamp 및 BoxTextured와 함께 재생. EPUB 플레이어의 코덱·픽셀 선택은 표본 밖. |

예정, 관측, 정상 공석, 미수신, 미실행, 적용 대상 밖과 단순 미확인을 구분한다. 주요 원바이트·디코더·결과가 미달이면 해당 목적 또는 작업 상태를 PARTIAL로 기록한다. 통합 담당의 상태와 구분한다.
