# AF-RES-027 · 정정이 실제 소비자의 인용에 도달하는 시점 — 인계

## 상태와 고정 결과

**상태: REVIEW_READY_WITH_GAPS.** 정한 모집틀의 A12·B6 조사, 원문 최소수, 전체 원장, Q1–Q8 반증, 결과표와 검산을 완료했다. 정확한 소비 artifact와 첫 실행/배포, 타 분야 소비자의 날짜 있는 정정 경로는 미확인이다. 날짜 있는 완전 사슬6건의 보강 목표는 충족하지 못했다. 양성 수를 늘리기 위한 표본 교체·조건부 날짜의 승격은 하지 않았다.

- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-027`.
- 소유 경로: `docs/workstreams/research/AF-RES-027/`. 공통 STATE·계약·색인·dot-control은 수정하지 않았다.
- **⑤ 고정 결과 커밋: `3d208baa81744c464360b5469a74a10d76c4bc7f`.** 이 인계보다 먼저 RESULT·SELF_CHECK·수용 근거를 커밋하고 원격에서 확인했다.
- [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/3d208baa81744c464360b5469a74a10d76c4bc7f/docs/workstreams/research/AF-RES-027/RESULT.md), [고정 SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/3d208baa81744c464360b5469a74a10d76c4bc7f/docs/workstreams/research/AF-RES-027/SELF_CHECK.md), [고정 수용 조건](https://github.com/laadkke-arch/agentflow-open/blob/3d208baa81744c464360b5469a74a10d76c4bc7f/docs/workstreams/research/AF-RES-027/evidence/acceptance-evidence.json).
- 원격 재열람 완료: **2026-11-22T06:16:42Z**. 아래 세 파일의 Git blob SHA가 스테이징한 파일과 모두 일치했다. 이후 fetch한 커밋 전체와 로컬 index도 `git diff --cached --exit-code`로 일치 확인했다.
- 이 HANDOFF는 그 gate 이후 2026-11-22T06:18 UTC부터 작성했다. 마지막 인계 커밋 자체의 SHA는 아래 명령으로 확인한다. 앞선 결과 SHA는 이 문서 안에 고정돼 있다.

| 원격에서 읽은 파일 | 확인한 blob SHA | 확인 범위 |
| --- | --- | --- |
| RESULT.md | `28a8058e358c9f9ffd3d1359bcb0fe2019a81e5d` | 제목 아래 네 표, Q별 해석, 마지막3행을 담은 결과판 |
| SELF_CHECK.md | `c46592273d1dced2f7c02e50540448c605a0ca16` | Q별 반증·분모·검토 범위·79개 자료검사와 별도 검산 |
| evidence/acceptance-evidence.json | `db13ed7ec7d43483812d60573a1102decf2c770b` | 조건18개, met=true15 / false3, 미충족 사유·재개 입력 |

## 검산한 분모와 관측 결과

| 항목 | 고정 값 | 해석 범위 |
| --- | --- | --- |
| 주 표본 A | 12참조 / 12프로젝트; Homebrew6·conda-forge6 | 2019–2023 소비자 고정판을 미래 이력 전에 봉인. 프로젝트당1참조, 상한2 이하 |
| 보조 B | 사전 공식 원장6회; A 중복2·새 참조4 | A와 합치면 서로 다른 프로젝트16곳. B의 성공·지연은 A의 분자에 더하지 않음 |
| 선택 상류 사건키 | A10, B6, 중복제거 합계14 | 일상 버전 후계 포함. 별도 후속 수리·모든 버전 변화의 총수가 아니며 통계적 독립성도 아님 |
| A 판정 | 용도 유지5 / 특정 용도의 당사자 실패 보고2 / 보류5 | 소스·목적 범위의 판정. 현재 실제 실행 성공률이나 생태계 오류율 아님 |
| 보수적 고유 원문 | **87** = A 과거12 + 상류37 + 소비자 후속30 + B 추가 과거4 + 타 분야4 | 요구 하한32 및 범주12/8/8/4 충족. 같은 편집·commit·미러를 중복 산입하지 않음 |
| 자료 기록량 | sources348행, 직접 판독 URL288개, 고정 Git판134개 | 원문87·사건14와 다른 수. 요청/클릭 수·최소 읽기량·사람 시간·운영 비용 아님 |
| 엄격한 완전 사슬 | A0/12, B 원사건0/6 | 정확한 같은 목적의 공급·관측·수정·배포/실행 연결이 미완성. 실패0건이라는 뜻 아님 |
| A의 적격 source commit→공개 source판 | 2참조에서3쌍 | Pandas RC·stable와 Spyder source판. 실제 문서 서버·installer·GUI 정상화 지연 아님 |
| 형식적 우측/좌측 검열 | 0 / 0 | 시작 사건/시행이 불명인 행과 이전 참조 존재가 불명인 행을 검열로 만들지 않음 |
| 명시적 역사 결과 재현 고정 | A에서 확인0 | 버전 constraint/불변 commit만으로 재현 의도를 추정하지 않음 |
| 실제 사람의 오추천 피해 | 확인0 / A12 모두 미확인 | 특정 빌드·시작 실패 보고와 추천 때문에 생긴 사람 피해는 다른 주장 |

유지5는 A-H03/H04/C01/C02/C03, 특정 활동의 부적합 보고2는 A-C04/C06, 보류5는 A-H01/H02/H05/H06/C05다. B 원래 목적의 판정은 유지3·보류3이며 보조 R2를 원래 참조에 합치지 않았다. 데이터의 빈 날짜 칸은 동반 status/한계로 읽으며 0일로 바꾸지 않는다. `0건`, `해당 없음`, `관측 실패`, `미확인`의 정의는 [DATA_DICTIONARY](DATA_DICTIONARY.md)에 있다.

## 판단에 남겨야 할 핵심 차이

**주소의 생존은 기대 기능을 보장하지 않는다.** A-H01에서는 같은 cppcheck 이름 아래 rules 기능이 빠졌지만, 옛 fish 호출은 `--rule-file`을 요구했다. 이는 현재 recipe와 옛 호출의 정적 불일치다. 2019 당시 오류·현재 fish 실행 실패로 소급하지 않는다. 반대로 Qt5의 alias 이동과 B의 mamba CLI 출력은 이름/구성이 바뀌어도 원래 역할을 보존하는 사례다. 근거: RESULT 표1/3, H-F02/H-U15/H-U18, BH-S03, BC-S10/11/12.

**소스 정정과 같은 내용의 배포는 다르다.** A-H06의 main은 `pyqt@5`로 고쳤지만 확인한 v2.5.3/2.5.4는 이전 안내였고 v3.0.0은 `pyqt@6`였다. 다음 release 날짜를 같은 수정의 배포일로 채우지 않았다. A-H02의 실제 source archive에서는 설치줄 삭제를 확인했지만 현재 asset `created_at`/`updated_at`이 최초 공개 시각의 하한·상한이라는 보장은 없다. 해당22.4743일은 metadata 산술이며 지연 적격성=false다. 근거: H-C06/H-F07/H-F12/H-F08, H-R02, R-S01.

**옛 참조의 요구와 나중에 생긴 요구를 나눠야 한다.** scrcpy의 SDL3 전환은 Homebrew sdl2-compat 교체보다 먼저였지만 같은 정정의 음수 지연이 아니다. SciPy의 뒤 sparse-array 목적은 옛 Gaussian 목적과 다르다. QtPy의 Python3.11/PyQt5.15 보조 R2는 옛 Qt5.12 R1과 다르므로 후속 수리의 약5.47시간을 원래 사건이나 A의 전파 지연에 더하지 않았다. 근거: H-C04/H-R03/H-U16, C-S16/C-F59, BC-S20–27.

**실패 보고가 있어도 실제 노출 시계는 더 필요하다.** Pandas에는 문서 작업 실패와 임시 상한의 당사자 설명이 있으나 실제 solve된 NumPy build가 미확인이다. Spyder의 시작 실패는 상류 metadata 수리보다 먼저 발생했으며, 옛 `>=0.1.7`도 이미0.3을 허용한다. 최소판 수정일을 모든 사용자의 첫 정상화일로 바꿀 수 없다. 근거: C-F16/C-F50/C-F53/C-F54, C-F28/C-F25/C-F52.

**타 분야의 옛 식별자는 대상 역할에 따라 정확할 수 있다.** PLOS 연구 DOI와 정정 공지 DOI는 서로 다른 역할이다. 후속 PeerJ 인용에서 연구 DOI가 남은 것을 미정정 오류로 단정하지 않는다. 정정 전 byte/과거판 자체를 보존하려는 의도는 미확인이다. 도서관 사례의 `e-cs`는 역사 지리 범위에 맞는다. 지리 코드, 국가명 전거 `n…`, 주제 URI `sh85035319`를 직접 split 관계로 합치지 않았다. 근거: X-S01/X-S03/X-S04/X-S05. 같은 소비자의 날짜 있는 수정 사슬은 두 분야 모두 미확인이다.

## 날짜 산술의 사용 가능 범위

| 날짜쌍 | 확인한 시간 차이 | 합산/해석 제한 |
| --- | --- | --- |
| A-C04 pin source→확인한 첫 RC source판 | 76,027초, 약0.879942일 | RC와 stable은 같은 참조이며 소비자2건으로 세지 않음 |
| A-C04 pin source→확인한 stable source판 | 1,004,454초, 11.625625일 | source판 공개 시간. 실제 문서 게시/수정 효과 미확인 |
| A-C06 최소판 source→확인한 stable source판 | 863,997초, 약9.999965일 | macOS installer·첫 GUI 성공 날짜 미확인 |
| B-C03-R2 선택 Linux 수리 artifact→source 복귀 | 19,700.839초, 약5.472455시간 | R2 후속 수리의 source응답만. 원래2022 사건의 지연 아님 |
| 같은 R2 artifact→default branch 병합 | 86,726.839초, 약24.090789시간 | 작성 시각/최초 CI 적용과 다름 |
| R2 복귀 source→확인한 source release | 6,487,807초, 약75.090359일 | 중간 우회 상태가 별도 release됐다는 증거 아님 |

C04의 초기 Linux CPython artifact를 실제 썼다고 가정한 약5.27–5.32시간과 H02 asset metadata 산술은 `eligible=false`로 남겼다. 산술이 맞는 것과 그 값이 정정 전파 지연으로 적격인 것은 다르다. 모든 시작·끝·정밀도·출처 ID는 [intervals.csv](intervals.csv)에 있다.

## 실행·검토 영수증과 한계

- [validation.json](evidence/validation.json): 봉인 A행·과거 수집파일 해시, 참조/출처 조인, 범주 최소수, 날짜 산술,365일 창, 네 표/마지막3행, 파일 링크와 소유 경로 **79/79 통과**.
- [independent-ledger-check.json](evidence/independent-ledger-check.json): 통합 생성기를 재사용하지 않은 별도 구현의 **47/47 및 증분7/7**. 입력8파일 해시 고정. 숫자가 채워진8행의 범위·초/일 산술, 분모·출처 ID, 보충 직렬화 대조. 여기서8은 A/B 보조·비적격 metadata까지 포함한 숫자행 수다.
- [session-check.json](evidence/session-check.json): 2026-11-22T06:11:56Z 계약/소유 경로 검사 통과, remote_checked, 범위 밖 변경0. 이때 최신 foundation은 `21c517691e8d8882f0e66ef262b32fe3ad39b630`, 계약 fingerprint는 시작 때와 같은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`였다. 새 통합 결과를 연구 입력으로 읽거나 봉인 기준을 바꾸지 않았다.
- 실제 파일 검사는 kitty source archive8,927,688바이트/SHA256 `96fe79a645ec57a378295cdf16204265768091338d77efb058977b60209bb8ff`의 Brewfile, 작은 conda archive의 출력/의존성, Harvard 소장 MARC2,338바이트/SHA256 `6ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6`에 한정된다. archive 내용 검사는 원래 소프트웨어의 실행 성공이 아니다.
- 수집자 자기 검토, root 재열람16개, 봉인 전 적격성 판독, 이후 Homebrew/conda/B·타 분야 판독, 최종 문장 감사와 별도 원장 산술을 구별했다. 같은 모델 계열의 내부 검토이며 외부 사람의 독립 검토·맹검 사용자 실험이 아니다. [SELF_CHECK](SELF_CHECK.md)와 [지적 해소 기록](evidence/review-resolutions.json)에서 역할과 수정 내용을 확인할 수 있다.
- 실제 실행 환경은 공유 Linux workspace와 세션 표시 GPT-6 Astra Pro다. 배정 종류 web-pro와 별도 UI 모델 검증을 혼동하지 않았다. 조사 시작은2026-11-22T04:46Z(한국13:46), 외부 원문 마지막 보강은06:08:12Z, 결과 원격 확인은06:16:42Z(한국15:16:42)다. 마지막 인계 커밋/재열람 시각은 Git 기록으로 확인한다.

## 커밋 순서와 다시 읽는 방법

| 묶음 | 커밋 | 해당 묶음 뒤의 원격 확인 |
| --- | --- | --- |
| ① 표집·관측·판정·manifest | `188152a5f561f8b478c3a850b9dcbc1c19894a59` | SCOPE 고정판 확인 |
| ②a conda 과거 부분 봉인 | `965b431de6756d0ec5422a1a005e37744884356a` | 부분 봉인 파일 확인 |
| ②b A 전체 미래 열람 전 봉인 | `1714a55a529c7da42596ac0779d398f3aacf97c3` | 05:05:37Z 원격 확인 뒤 미래 이력 개방 |
| ③H Homebrew6 사슬 | `885537f8849d9fff1ecba3adf0068e9d8c70cc2f` | chains blob 일치 |
| ③C conda6 사슬 | `5ef2a246f4a18ac1eb6adb65e47660e03f49cab8` | chains blob 일치 |
| ④ B6·타 분야·검열·대조 | `17229e1bde153aaf29290dceae4dad9172fe987f` | conda B cases blob 일치 |
| ⑤ 집계·자체 점검·수용 근거 | `3d208baa81744c464360b5469a74a10d76c4bc7f` | RESULT/SELF_CHECK/acceptance 원격 일치; 이 문서 상단 영수증 |
| ⑥ 인계 | 이 HANDOFF를 추가한 마지막 커밋 | 아래 git log로 확인. ⑤ 확인 뒤에만 작성 |

저장소 루트에서 고정판과 마지막 인계 커밋을 확인한다.

```bash
git fetch origin work/research-af-res-027
git log -1 --format='%H %s' origin/work/research-af-res-027 -- docs/workstreams/research/AF-RES-027/HANDOFF.md
git show 3d208baa81744c464360b5469a74a10d76c4bc7f:docs/workstreams/research/AF-RES-027/RESULT.md
git rev-parse 3d208baa81744c464360b5469a74a10d76c4bc7f:docs/workstreams/research/AF-RES-027/evidence/acceptance-evidence.json
git diff --name-only 3d208baa81744c464360b5469a74a10d76c4bc7f origin/work/research-af-res-027
git status --porcelain
```

이 인계 직후의⑤→⑥ 차이는 HANDOFF.md 하나여야 한다. 나중 후속 커밋이 생기면 branch tip 대신 위 첫 명령이 찾은 인계 SHA로 비교한다. 앞선 여섯 묶음의 상세 원격 영수증은 [commit-log.json](evidence/commit-log.json)에 있다.

원장 재생성/검산은 다음 순서다. 이미 고정한 collector 원문 관측을 읽는 명령이며 외부 software를 설치하지 않는다. 검산 영수증의 실행 시각은 새로 생성되므로 재실행 작업물과 고정 결과를 구분한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/append_b.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/consolidate_sources.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/build_ledgers.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/build_report.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-027/scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-027/manifest.json --fetch
```

## 미확인 자료를 재개할 입력과 명령

현재 공개 source·release·retained CI API만으로 실제 과거 실행을 복원할 수 없었다. 현재 API의0/404는 당시 실행 부재·성공의 증거가 아니다. 아래는 후속 조사자가 같은 입력을 재확인하거나 새 보존 로그를 확보할 때 사용할 명령이다. 이번 조사에서 실행하지 않은 역사 software 검사를 이미 통과한 것처럼 기록하지 않는다.

### 1. 첫 행동: Pandas의 같은 문서 작업에서 실제 artifact와 첫 성공 연결

재개 입력은 PR35312, pin source `cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda`, 직전판 `5e45f4f6dd253fa585076ea3149ef4e07fed5d0f`, Ubuntu `web_and_docs`, C-F50의2020-07-16 NumPy1.19.0 artifact 목록이다. 현재 보존 checks/status 조회 결과는0이었다(C-F55). **우선 필요한 새 자료는 해당 작업의 당시 로그 한 쌍**이며 Python minor·platform·conda explicit artifact와 pin 전 실패/후 첫 성공을 함께 보여야 한다. 새 일반 NumPy 설치 시험으로 이 과거 노출을 대체하지 않는다.

```bash
AF027_RESUME=docs/workstreams/research/AF-RES-027/resume
mkdir -p "$AF027_RESUME"
gh api 'repos/pandas-dev/pandas/commits/cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda/check-runs' > "$AF027_RESUME/pandas-pin-check-runs.json"
gh api 'repos/pandas-dev/pandas/actions/runs?head_sha=cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda&per_page=100' > "$AF027_RESUME/pandas-pin-runs.json"
git clone --filter=blob:none https://github.com/pandas-dev/pandas.git "$AF027_RESUME/pandas-source"
git -C "$AF027_RESUME/pandas-source" show 5e45f4f6dd253fa585076ea3149ef4e07fed5d0f:.github/workflows/ci.yml > "$AF027_RESUME/pandas-before-workflow.yml"
git -C "$AF027_RESUME/pandas-source" show cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda:ci/setup_env.sh > "$AF027_RESUME/pandas-pin-setup-env.sh"
```

이 API 재조회는 보존 상태를 확인하는 명령이며 이미 사라진 로그를 되살리지 않는다. PR의 외부 CI 링크/공공 동시대 보존본을 우선 따라가야 한다. 실제 재현에는 추가 입력 `pandas-before-explicit.txt`와 `pandas-after-explicit.txt`(그 작업에서 수집한 정확한 explicit URL 목록), 해당 패키지 archive 캐시, 당시 문서 호출을 보존한 shell 파일이 필요하다. 이 세 입력을 아직 확보하지 못했으므로 아래 실행은 하지 않았다.

```bash
test -s "$AF027_RESUME/pandas-before-explicit.txt"
test -s "$AF027_RESUME/pandas-after-explicit.txt"
test -s "$AF027_RESUME/pandas-web_and_docs-command.sh"
conda create --yes --offline -p "$AF027_RESUME/pandas-before-env" --file "$AF027_RESUME/pandas-before-explicit.txt"
conda create --yes --offline -p "$AF027_RESUME/pandas-after-env" --file "$AF027_RESUME/pandas-after-explicit.txt"
conda run -p "$AF027_RESUME/pandas-before-env" bash "$AF027_RESUME/pandas-web_and_docs-command.sh"
conda run -p "$AF027_RESUME/pandas-after-env" bash "$AF027_RESUME/pandas-web_and_docs-command.sh"
```

실행 위치·소스 SHA·환경변수·working directory는 보존된 workflow/로그와 일치시켜야 한다. 단순 import 성공이나 다른 Python minor의 현재 solve는 이 연구의 실패/정정 효과를 확인하지 못한다. macOS Spyder/kitty의 같은 목적 검사는 별도 해당 macOS 환경과 정확한 당시 artifact가 필요하며 이번 Linux 세션에서 수행하지 않았다.

### 2. qutebrowser의 같은 pyqt@5 수정이 공개된 첫 판

입력은 `7b53f648141dd9b604fc01a8603faa55021576e7`의 `doc/install.asciidoc`이며, 찾을 것은 그 문구가 들어 있는 당시 docs/nightly artifact와 공개 시각의 영수증1건이다. 뒤 `pyqt@6` release는 대체 자료가 아니다.

```bash
gh api 'repos/qutebrowser/qutebrowser/deployments?sha=7b53f648141dd9b604fc01a8603faa55021576e7&per_page=100' > "$AF027_RESUME/qute-pyqt5-deployments.json"
gh api 'repos/qutebrowser/qutebrowser/actions/runs?head_sha=7b53f648141dd9b604fc01a8603faa55021576e7&per_page=100' > "$AF027_RESUME/qute-pyqt5-runs.json"
git clone --filter=blob:none https://github.com/qutebrowser/qutebrowser.git "$AF027_RESUME/qute-source"
git -C "$AF027_RESUME/qute-source" show 7b53f648141dd9b604fc01a8603faa55021576e7:doc/install.asciidoc > "$AF027_RESUME/qute-pyqt5-source.asciidoc"
git -C "$AF027_RESUME/qute-source" log --all --follow --date=iso-strict --format='%H %cI %s' -- doc/install.asciidoc > "$AF027_RESUME/qute-install-path-history.txt"
```

반환된 deployment/run이 있다면 그 원문이 동일 문구를 배포했는지 다시 확인해야 한다. 단지 성공 상태나 ancestry 포함만으로는 부족하다. 예전 artifact가 없으면 최초 배포는 계속 미확인으로 둔다.

### 3. 도서관 같은 항목의 이전판과 공개일

입력: Harvard MARC001 `990068819680203941`; 현재 확보한 파일 `20220215_017.bib.mrc`, offset295257330·length2338. 후속의 첫 자료는 **동일001의 이전 불변 export와 그 원 배포 영수증**이다. 이전 파일에서 같은 offset을 사용할 수 있다고 가정하지 않는다. 아래 명령은 현재 고정 관측의 해시를 재확인할 뿐1993 이후 연속 이력을 증명하지 않는다.

```bash
curl --fail --location --range 295257330-295259667 'https://archive.org/download/harvard_bibliographic_metadata/20220215_017.bib.mrc' -o "$AF027_RESUME/harvard-record.mrc"
python - "$AF027_RESUME/harvard-record.mrc" <<'PY'
import hashlib, pathlib, sys
b = pathlib.Path(sys.argv[1]).read_bytes()
assert len(b) == 2338
assert hashlib.sha256(b).hexdigest() == '6ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6'
print('fixed record bytes verified; no first-publication inference')
PY
curl --fail --location 'https://archive.org/metadata/harvard_bibliographic_metadata' -o "$AF027_RESUME/harvard-mirror-metadata.json"
```

이후 이전 export에서043/651/852/876과 같은001을 대조하고, 원 공개일·MARC005·파일명 날짜·미러mtime을 따로 기록해야 한다. PLOS 쌍의 보강은 X-S01 notice에 링크된 정정 전/후 S1·S2 PDF의 동시대 공공 보존본이 첫 입력이다. 접근하지 못한 PDF의 정확한 title diff나 본문 동일성을 현재 초록으로 대체하지 않는다.

## 진행 담당에게 제안할 반영

공통 진행표/색인에는 **REVIEW_READY_WITH_GAPS, A12/B6, 고유 원문87, 엄격 전파 사슬0, source출판2참조3쌍, 실제 사람 피해 미확인**, 고정 결과 SHA `3d208baa81744c464360b5469a74a10d76c4bc7f`와 이 인계 커밋을 연결할 것을 제안한다. 진행 담당에게 메시지를 보내거나 공통 파일을 직접 수정하지 않았다.

제품 기록의 최소 제안은 주소에 소비자판·참조 문자열/채널·기대 명령/모듈/API세대·허용판/플랫폼·목적을 붙이고, 시간 판단이 필요할 때 원문 판·관계 종류·날짜 역할·배포 내용과 미확인 이유를 더하는 것이다. 모든 이력을 항상 복사해야 한다는 결론이나 기록비용 절감률은 제안하지 않는다. 후속 조사 우선순위는 아래3건이며, 첫 행동은 Pandas의 당시 문서 작업 로그를 찾는 것이다.

| 중요한 불일치·약점 | 근거 ID·URL | 영향을 받는 결정 | 다음 조사 질문·찾을 자료·최소 확인 |
| --- | --- | --- | --- |
| 공급 artifact와 실제 실패/첫 성공의 연결이 없어 A의 엄격 전파 지연은0건이다. | C-F50/C-F54/C-F16; [NumPy artifact](https://api.anaconda.org/release/conda-forge/numpy/1.19.0), [Pandas PR35312](https://github.com/pandas-dev/pandas/pull/35312) | 제안일부터 늦게 고쳤다는 주장, 약5.3시간 전파 주장, 실제 정정 효과 | Pandas2020-07-16 web_and_docs 보존 로그 한 쌍에서 실제 Python minor·conda explicit URL와 pin 전 실패/후 첫 성공을 같은 목적에서 고정한다. |
| 수정 source와 같은 수정의 최초 실제 배포가 이어지지 않는다. | H-C06/H-F07/H-F08/H-R02/R-S01; [pyqt@5 수정](https://github.com/qutebrowser/qutebrowser/commit/7b53f648141dd9b604fc01a8603faa55021576e7), [asset 날짜 필드](https://docs.github.com/en/rest/releases/assets?apiVersion=2022-11-28) | commit→첫 배포 지연, 배포 성공률, 다른Qt계열 release나 asset metadata의 대체 사용 | 같은 pyqt@5 문구가 들어간 첫 docs/nightly artifact 또는 배포 로그1건에서 실제 내용과 공개시각을 확인한다. |
| 옛 지리 역할의 적합성은 보이나 subject ID 전후 계보와 snapshot 최초 공개일은 미확인이다. | X-S04/X-S05/X-S12; [LC CSB60](https://www.loc.gov/aba/publications/FreeCSB/CSB_060.pdf), [소장 원본 export](https://archive.org/download/harvard_bibliographic_metadata/20220215_017.bib.mrc) | sh→n 직접 분리 주장,1993→2022 전파 지연, 소비자의 고의 보존/수정 의도 | 동일 Harvard001의 이전 불변 export1판과 원 배포 영수증을 확보해043/651·소장필드·ID종류·실제 판 공개일을 대조한다. |
