# AF-RES-027 · 표집·관측 계약 v1

## 실행과 고정 입력

- 작업: AF-RES-027#1; 배정 종류 web-pro. 실제 실행은 ChatGPT 공유 Linux workspace `/workspace/scratch/0b2e37f3b4f7/agentflow-open`, 세션 표시 GPT-6 Astra Pro. 별도 웹 모델 선택 화면/사용자 PC/개별 Codex Cloud 환경은 확인하지 않았다.
- 브랜치: `work/research-af-res-027`; 소유 경로: `docs/workstreams/research/AF-RES-027/`만. 공통 진행표·계약·색인 수정 없음.
- 계획 기준: `e2d0917ccd0e0010e14627a2f919265c332cec53`; 배정 후 최초 원격 확인 및 실제 시작 foundation: `b420fb7e1e01f4a366512fa71c0f507051aa6a19`.
- 고정 의존: AF-RES-023 `a9178ca95979564fd8801559d90d15db4ddac91b`의 HANDOFF, RESULT Q3–Q6, citations.csv, reconstruction.csv, evidence/counts.json. 원문·계산의 교정용이며 신규 표본 수에 넣지 않는다. 다른 동시 작업은 입력으로 쓰지 않는다.
- `manifest.json`은 `workbench.session start af-res-027 --allow docs/workstreams/research/AF-RES-027/ --output docs/workstreams/research/AF-RES-027/manifest.json --dependency work/research-af-res-023=a9178ca95979564fd8801559d90d15db4ddac91b --fetch`로 생성했다. 계약 v2, remote_checked.
- 조사 시작 2026-11-22T04:46 UTC (한국 13:46). 끝 시각과 중간 원문 열람 시각은 sources.json 및 최종 인계에서 확정한다.
- 선행 18사건과 SW-D01/SW-D02/MB-C01/WD-C01, ROR 현재 소비자 4개는 제외. 소프트웨어 제외 사건: tinyfugue/tiny-fugue, libxml++3→libxml++@3, gnu-readline 되돌림, postgresql→postgresql@14, tree-sitter CLI 분리. 같은 사건의 다른 소비자로 최소수를 채우지 않는다.

## ① 결과 열람 전 고정하는 주 표본 A

단위는 **소비자 프로젝트가 한 공개 용도에 붙인 패키지 참조 하나**다. 이 표집은 확률표집이 아니라 사전에 한정한 공개 개발환경 모집틀의 목적표집이다. 변경·성공·실패를 검색어에 넣지 않는다. 표집 완료 전 상류 변경 이력, 소비자의 기준시점 이후 파일/커밋/이슈를 열지 않는다. 연구자의 일반 사전 지식까지 차단한 맹검은 아니다.

호스트는 공개 GitHub 저장소, 소비자 문서의 당시 외부 공식 링크만 보조 허용한다. 각 프로젝트의 기준판은 2019-12-31T23:59:59Z, 없거나 적격 파일이 없으면 2021-12-31T23:59:59Z, 이어 2023-12-31T23:59:59Z **순서**로 `commits?until=...&per_page=1` 또는 동등한 Git 이력에서 고정한다. 해당 기준판에서 작성·수정일이 2019–2023년인 실제 환경 파일/설치 지시와 같은 판의 호출/목적을 확보한다. 기준판 이전에 작성된 줄도 그 기준판이 계속 공개한 지시라는 범위에서 포함하며, 최초 삽입일과 혼동하지 않는다.

소비자 목록은 알려진 공개 개발 프로젝트를 목적별로 분산해 **아래 순서로 미리 선택**했다. 인기·대표성·무작위성을 주장하지 않는다. 목표는 계열당 6참조/6소비자, 전체 12소비자다. 프로젝트당 최대 2이며 기본 1개; 6곳 확보가 안 될 때만 적격 프로젝트의 두 번째 다른 파일을 쓰고 전체 8프로젝트 하한을 지킨다. 제외/실패도 frame.csv에 남기며 뒤에서 성공 사례로 교체하지 않는다.

| 계열 | 순서대로 볼 1차 후보 | 순서대로 볼 예비 후보 |
| --- | --- | --- |
| Homebrew | alacritty/alacritty; fish-shell/fish-shell; kovidgoyal/kitty; mpv-player/mpv; neovim/neovim; obsproject/obs-studio | wez/wezterm; tmux/tmux; Genymobile/scrcpy; qutebrowser/qutebrowser |
| conda-forge | dask/dask; jupyterlab/jupyterlab; napari/napari; pandas-dev/pandas; scikit-image/scikit-image; spyder-ide/spyder | holoviz/panel; bokeh/bokeh; astropy/astropy; scikit-learn/scikit-learn |

검색식/경로 순서: 기준판 tree에서 `Brewfile|INSTALL|install|build|contribut|environment.*ya?ml|conda.*ya?ml|workflow`를 대소문자 무시 검색한다. 목적을 설명하는 설치/개발 문서를 우선하고 그 안의 실제 환경파일 경로를 따른다. 같은 우선순위는 POSIX 경로 오름차순. 본문은 `brew (install|bundle)|conda-forge|channels:|dependencies:`로 찾는다. 웹 검색은 발견용 `site:github.com/OWNER/REPO "brew install" before:2024-01-01` 또는 `"conda-forge" "environment"`로 제한하며 검색 요약은 원문 수에서 제외한다.

각 소비자에서 해당 목적에 설치·호출되는 **본문 순서의 첫 적격 패키지**를 선택한다. 이미 그 계열에서 선택한 패키지명이면 다음 이름으로 넘어가 기능/판 다양성을 확보한다. 후보가 모두 중복이면 첫 이름을 포함하고 독립 상류 사건으로 중복 산입하지 않는다. 023 제외 사건, 자기 제품 자체 설치, cask, pip 하위 목록, 공식 카탈로그가 아닌 개인 tap는 제외. conda-forge는 첫 채널 또는 `conda-forge::` 명시를 요구한다. 채널 나열은 실제 solver가 그 채널의 binary를 선택했다는 증명이 아니므로 별도 미확인이다.

기준판 파일 12개와 소비자 목적·버전·호출 위치를 `references.jsonl`과 수집자 `historical.json`에 기록하고 해시·GitHub 커밋으로 봉인한 다음에만 미래 이력을 연다. 설치명만 있고 원래 용도가 불명인 행도 보류 상태로 남기며 정정 필요성을 채워 넣지 않는다.

## ③ 이후 이력과 사전 판정

각 참조에서 최초 확인 가능한 관련 상류 사건을 추적한다. 관계는 `NAME_ONLY`, `SAME_ARTIFACT_RENAME`, `VERSION_SUCCESSOR`, `CLI_LIBRARY_SPLIT`, `MULTIPLE_SUCCESSORS`, `REVERT`, `NO_RELEVANT_EVENT_OBSERVED`, `UNRESOLVED`로 구별한다. 버전 증가만으로 기능 소실 또는 소비자 정정 필요라고 하지 않는다.

다섯 시점은 T0 과거 인용 불변판, Tu 상류 사용자 시행, To 최초 관측 적합/부적합, Tc 소비자 수정 커밋, Tr 첫 수정 배포다. 제안·merge·source commit·배포·현재 조회는 각각 다른 열이다. Tu가 없으면 commit 날짜를 시행일로 바꾸지 않는다. 해당 배포를 본 1차 기록이 없으면 미확인이다. 소스가 바로 배포되는 문서인지, 릴리스 포함 여부인지도 명시한다.

주 관측 창은 Tu 이후 365일이며 Tu가 구간이면 창도 구간이다. 창 말 불변판, 그 뒤 첫 알려진 수정은 별도 기록한다. 무사건에는 Tu와 지연이 해당 없음이다. 창 말에 파일이 같다는 관측은 구간 중 수정·되돌림이 없었다는 증명이 아니다. 경로 변경/rename을 포함한 공개 이력, parent/blame, 릴리스/CI를 확인한다.

판정: `MAINTAINED_FOR_PURPOSE`, `INTENTIONAL_PIN`, `INCOMPATIBLE_FOR_STATED_PURPOSE`, `COMMIT_ONLY_RELEASE_UNKNOWN`, `NO_FIX_OBSERVED_IN_WINDOW`, `HISTORY_UNAVAILABLE`, `UNDECIDABLE`. 마지막 세 항목을 실제 실패/미정정률로 합산하지 않는다. 고의 고정은 명시적 의도 근거가 필요하다. 명시된 당시 stable을 지금 최신 요구로 바꾸지 않는다. 실제 사용자 피해는 직접 소비자 보고/맞는 릴리스·CI가 없으면 미확인이다.

날짜 쌍은 동일 참조·기능·목적이고 Tu/Tc 또는 Tc/Tr 양 끝이 확인될 때만 계산한다. 범위 날짜는 하한/상한. 우측 검열은 시작 시행과 관측 끝이 확인되며 그 사이 수정이 관측되지 않았을 때; 좌측 검열은 최초 관측 전 이미 바뀐 경우. 이벤트/시작일 자체 미확인은 검열 관측으로 위장하지 않는다. 무사건·고의 고정·복수 후계·결정 불가는 분모에 유지한다.

## ④ 보조 B와 타 분야

B는 아래 **공식 원장 6개**를 지금 고정하고, 각 원장에서 2019–2023년 첫 관련 이름/출력/분리 변경을 찾는 6회 역추적이다. 그 기간에 없으면 2024년 이후 최초 관련 사건을 보조로 표시하고, 없거나 확인 불가도 시도 1개로 보존한다. 소비자 탐색은 사건의 옛 이름+brew/conda-forge+설치 목적; 당시/현재 소비자 고정판을 찾는다. 이미 알려진 성공으로 발견한 경우는 B에만 들어간다. A와 중복되면 연결 ID를 남기며 A의 비율에 더하지 않는다.

- B-H01: Homebrew/homebrew-core `formula_renames.json`의 `pkg-config` 관계 및 관련 recipe 이력.
- B-H02: 같은 공식 원장의 `python` 관계 및 관련 recipe 이력.
- B-H03: 같은 공식 원장의 `qt` 관계 및 관련 recipe 이력.
- B-C01: conda-forge/matplotlib-feedstock `recipe/meta.yaml` outputs/이름 이력.
- B-C02: conda-forge/mamba-feedstock `recipe/meta.yaml` outputs/이름 이력.
- B-C03: conda-forge/qt-feedstock `recipe/meta.yaml` outputs/이름 이력.

Q7은 학술 정정/재발행+실제 후속 인용, 도서관 전거 분리/신규 표목+실제 소장목록 고정판을 각각 한 쌍 이상 찾는다. 정책 설명 또는 현재 레코드만으로 날짜 있는 소비자 사슬을 대신하지 않는다. 타 분야 조사자는 A/B와 분리해 병행한다.

## Q8 · 가벼운 기록 비교

A 각 행의 같은 원자료를 세 단계로 가려 읽는다: L1 주소/패키지명, L2 +기대 기능/판/목적, L3 +당시 원문·소비자 인용시점·상류 관계. 질문은 당시 무엇을 쓰려 했나, 현재 목적을 충족하나, 언제 수정/배포됐나의 세 가지다. 가려진 단계의 답과 결정불가를 verdicts.csv에 남긴다. 이미 원문에 노출된 연구자의 구조적 점검이며 외부 독립 맹검 성능 실험이 아니다. 숫자는 재열람 URL·서로 다른 고정판 수만 실제 기록에서 세고 사람의 해석시간·전체 전파율·운영 비용은 추정하지 않는다.

## 자료 수·저장·종료

고유 외부 원문 최소 32: 소비자 과거 12, 상류 recipe/릴리스/diff 8, 소비자 후속 8, 두 타 분야 4. 같은 편집/commit의 여러 렌더링·미러·복수 줄은 중복 제외. 서로 다른 판은 판 수에는 따로 기록하되 동일 작업의 중복 최소수 부풀림 금지. 내부 023 보고/검색 요약/초록/차단은 탐색 기록만. 출처마다 직접 본 절·시각·근거·한계·생산계보와 산입 이유를 남긴다.

① 본 계약 ② A 봉인 ③ 계열별 3–6행 사슬 ④ B/타 분야/검열/기록비교 ⑤ 집계·수용근거·자체점검 ⑥ HANDOFF를 따로 커밋하고 원격 고정 SHA로 재열람한다. ⑤ 원격 확인 전 HANDOFF를 작성하지 않는다. 날짜 완전 사슬 6개는 보강 목표이며 양성 사례를 위해 A를 바꾸지 않는다. 미충족은 false 및 재개 불변판/명령을 남겨 REVIEW_READY_WITH_GAPS 또는 BLOCKED로 인계한다.
