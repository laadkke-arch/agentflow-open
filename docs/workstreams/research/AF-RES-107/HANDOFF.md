# AF-RES-107 최종 인계

**COMPLETE · 자가점검 완료.** 기준 6/6, 주 출력 24/24, 약속 충족 18/24, 종료 0인 목적 실패 6/24다. 단일 A 0/6, B 6/6, 전체 A·B 각 6/6이다. 단일 A가 목표와 함께 칠한 형제는 T g21, S m-end, D e02–e21이다. 전체에서 A와 B는 세 원본 모두 의미상 같다. 두 반복은 가용 15/15쌍에서 의미 일치다. T PDF 원시 지문 일치는 0/5쌍이며 S XML·D SVG는 각각 5/5다. 대조 11회와 상류 재생 6회는 별도다. 고유 1차 자료 25개 중 원저작 3, 언어·구현 10, 회귀 6, 측정 6이다. [결과](RESULT.md) · [원장](runs.jsonl) · [요소](elements.csv) · [검산](evidence/verification.json) · [출처](sources.jsonl)

T에서는 PITCH g12(6쪽)와 g21(11쪽)을 각각 확인했다. 같은 각도의 B 대조는 두 개를 칠했고 첫 회차만 펼친 로컬 대조는 하나를 칠했다. 역패치는 원 TeX 지문과 27개 청색을 복원했다. S는 같은 정의에 연결된 두 마커의 실제 paint 발생을 사용했다. 상류 `<use>` 2건 및 구성 쌍 5개에서는 explicit fill·상속·복사를 별도로 확인했다. D는 연쇄 전체를 칠하는 B 대조, 뒤의 default, strict 재지정과 한 간선만 소비하는 local default를 실행했다. [단일 원 화면](evidence/plates/) · [대조](evidence/CONTROLS.md)

## 저장과 검증

브랜치는 `work/research-af-res-107`다. 계획 `49f603a98188fbf2009c4c490b0539f32d124e38` 이후 최초 통합 `e601fa1aed009106be983ae9b24e4778e793276f`에서 만들었고, 작업 시작 전 다음 원격 통합 `32b6bb32989730df78d521c29a50dbebd3289b46`을 fast-forward하여 계약을 생성했다. 관련 파일 차이는 중앙 진행표뿐이다. 운영 의존 AF-RES-103의 등록 인계와 실제 끝은 `09503ac5452bbfb329aa0d5ff4bad9499924f277`, 연구 입력은 `41f5fbb3d6db39532e7aa9d9dca6c2f4012678fd`이다. 두 판 사이 변경은 인계 추가이며 사용 blob이 같다. [시작·의존 지문](inputs.json) · [manifest](manifest.json)

| 묶음 | 원격에서 확인한 커밋 | 커밋·원격 확인 UTC와 경로 |
| --- | --- | --- |
| ① | [79ac12bf676a0fc6d45a940572e18f0460716e1a](https://github.com/laadkke-arch/agentflow-open/commit/79ac12bf676a0fc6d45a940572e18f0460716e1a) | 23:27:36·23:27:50.997. `SCOPE.md`, manifest·입력·protocol·기대표, 선택 원장과 원 입력 11파일 |
| ② | [3fc3c9abc317ec0556c2457056c53ac3a2a4cec6](https://github.com/laadkke-arch/agentflow-open/commit/3fc3c9abc317ec0556c2457056c53ac3a2a4cec6) | 23:35:24·23:35:26.185. baseline·upstream, 도구와 patch 12개, 대조 입력·실행기 포함 78파일 |
| ③ | [3bcb979a49097a51e42eae80a41b2ef43c2bb079](https://github.com/laadkke-arch/agentflow-open/commit/3bcb979a49097a51e42eae80a41b2ef43c2bb079) | 23:40:07·23:40:09.268. `evidence/matrix`, `controls`, `plates`, CSV/JSONL·검산 코드, 334파일 |
| **④ 검사 결과판** | [8ae7aad97c7a4e958cdfe078ff49262b3717874e](https://github.com/laadkke-arch/agentflow-open/commit/8ae7aad97c7a4e958cdfe078ff49262b3717874e) | 23:52:32·23:52:34.267. RESULT·SELF_CHECK·출처·재현·검산 보강·상류 영수증·라이선스·색인, 41파일 |
| 인계 | 이 파일만 추가한 최종 커밋 | ④ 검사 및 원격 재열람 뒤 작성 |

시각은 2026-11-23 UTC다. ①~③의 경로별 기록은 [묶음 영수증](evidence/commit-files.json)에 있다. ④까지 통합판 대비 460파일은 모두 허용 경로 안이다.

검사 전후 현재 SHA가 ④이고 Git status가 clean인 새 GitHub 사본에서 다음을 실행했다. 통합 원격과 의존 원격은 위의 계약 SHA와 같았다. 공통 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`이다.

| 실제 명령 | UTC · 종료값 · 범위 | stdout SHA-256 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-107/manifest.json --fetch` | 23:53:07.250–23:53:08.297, 0. 한 작업을 직접 확인, `remote_checked`. 자체 manifest 제외 변경 459, 범위 밖·미병합·오류 각 0. | `475db96ba0b6bd26c881025495a4431c522c2ce0849a8bdbabf675358ba0a26b` |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 23:53:08.345–23:53:15.301, 0. doctor·acceptance·research-case·original-smoke 통과. 공통 `check-all` 자동 발견 실제 0. `not-executed/no_active_sessions`, `freshness=not_checked`. 공통 및 lab 테스트 55+7+9; Git 객체 복원·export 확인. | `f039121d6bcec984c53fdc84bcbefe688dbc45b15f199811f3c5d2e9fbe3d054` |
| `python -B docs/workstreams/research/AF-RES-107/verify.py` | 23:53:15.305–23:53:17.695, 0. 기준 6, 주 24, 대조 11의 파일·원 PDF/DOM/PNG 판독과 644 요소 행, 의미 15쌍 재계산. | `9c06fde67fb6c6b17ff20aba9481fc3e0ddad126f7cc40cfdc9c8110b38bdf09` |

세 명령의 외부 stderr는 0바이트다. 23:53:33.984에 새 bare Git 저장소로 ④를 받아 **64/64 파일 바이트 일치**를 대조했다. 필수 표 6/24/6행과 마지막 약점 3행, 대표 원 TeX/HTML/DOT, patch, T PDF·두 쪽 PNG, S SVG/PNG와 D SVG/PNG, `reproduce.md`를 다시 열었다. GitHub 커넥터로도 해당 SHA의 텍스트 7개를 직접 재열람했다. RESULT blob은 `2e107dc049e8570c219ee2e603b91134c7a9f4c5`, SELF_CHECK는 `2722dc70c5bd53da8e8b7f1911c2867460ca08b1`, reproduce는 `dfe6d0a9677e7063872d648942b7412eb2b9ce72`다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/8ae7aad97c7a4e958cdfe078ff49262b3717874e/docs/workstreams/research/AF-RES-107)

## 미확인과 다음 첫 행동

원본 결원·도구 준비 실패·출력 없음·주 미실시는 각 0이다. S 첫 100개에 리터럴 `<use>`가 없어서 기존 marker의 서로 다른 paint 사용을 원본으로 정했다. D의 기준에서 단색 픽셀만 읽으면 e01/e02를 놓쳤으며, 주 실행 전에 같은 원 화면에서 안티앨리어싱 검사를 보완했다. 공식 상류 WPT CLI와 Graphviz 전체 하네스, 별도 사람 검토, 엔진·폰트가 다른 재생, 독자의 시간·자연 문서 일반화는 미확인이다. [자가점검](SELF_CHECK.md) · [측정 교정](evidence/baseline/dot-raster-calibration.json)

재개 첫 행동은 ④의 [T 단일 원 화면](evidence/plates/T-one.png)과 [원 PITCH L45–49](https://github.com/pgf-tikz/pgfplots/blob/d8e70d407d4f40a02cfdcc4783e7ff3028d8c5c6/source/latex/pgfplots/pgfplotstest/regressiontests/unittest_3d_0.tex#L45-L49)를 열고 새 반복 원소를 삽입했을 때의 ID 이행을 실험하는 것이다. 즉시 재현할 때는 ④ checkout의 `python -B docs/workstreams/research/AF-RES-107/verify.py`와 [실행 입력·명령](reproduce.md)을 사용한다.

**색인 제안** — AF-RES-107 · COMPLETE · 공유 정의와 사용 발생의 편집 범위 · 단일 A 0/6 B 6/6, 전체 A·B 각 6/6 · 직접 1차 자료 25개 · 결과 `8ae7aad97c7a4e958cdfe078ff49262b3717874e` · [RESULT](RESULT.md)

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| T의 g12·g21은 두 인자가 같고 호출 줄도 공유한다. 순번도 다음 판에서 움직인다. | [원 PITCH](https://github.com/pgf-tikz/pgfplots/blob/d8e70d407d4f40a02cfdcc4783e7ff3028d8c5c6/source/latex/pgfplots/pgfplotstest/regressiontests/unittest_3d_0.tex#L45-L49)에 새 회차를 앞에 삽입해 source와 발생 ID 매핑 수명을 측정. | 두 과거 발생을 구별하고 삽입 후에도 과거 목표 한 곳만 수정된다. |
| 주 S는 마커 paint이고 `<use>`는 별도 비교다. 외부 참조·타 엔진은 미확인. | [WPT use inheritance](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/svg/struct/reftests/use-inheritance-001.svg)를 외부 참조와 Firefox까지 재생. | 속성 우선순위와 보존 집합이 엔진·문서 경계를 넘어 재현된다. |
| 같은 endpoint 다중 간선과 독자 재편집 시간은 미확인. | [DOT 원 연쇄](https://gitlab.com/graphviz/graphviz/-/blob/00d9fb4479c21b021e510dfb2633f1058d695db7/tests/graphs/Heawood.gv#L18-30)와 다중 간선 입력을 주고 링크 순서 두 가지로 독립 과제를 실행. | 두 링크로 보기·원본 재생·한 발생 변경을 정해진 시간 안에 구별해서 완수한다. |
