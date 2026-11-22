# AF-RES-027 자체 점검 — 최종 내용 검산

## 상태와 검토 범위

이 문서는 Q1–Q8의 주장, 직접 읽은 근거, 반증 시도, 남은 최소 자료를 대응시킨 **최종 내용 검산본**이다. 통합 원장·분모·산술·보고서 구조의 내용 검산을 완료했다. `evidence/validation.json`은 2026-11-22T06:09:57.838831Z의 79/79 통과를, `evidence/independent-ledger-check.json`은 별도 구현의 전체 47/47 및 06:12:49.655527Z의 증분 7/7 통과를 기록한다. 최종 문장 감사에서 발견한 근거 ID·정보 범위 오류의 수정도 현재 RESULT에서 대조했다. 이는 역사적 패키지 실행이나 실제 정정 효과가 입증됐다는 뜻이 아니며, 수용 상태는 **REVIEW_READY_WITH_GAPS**다.

**내용 검산 완료; 이 문서를 포함한 ⑤ 커밋의 원격 확인 이후 HANDOFF를 작성하고, 해당 SHA·영수증은 HANDOFF에 기록한다.** 이 갱신 시점에는 ⑤ 커밋이 아직 생성되지 않았다. 따라서 이 문서는 ⑤ 원격 확인을 완료했다고 주장하지 않는다. 최종 갱신 입력은 2026-11-22T06:10 UTC 이후의 RESULT·통합 원장·검산 영수증이다.

여기서 “직접 근거”는 `sources.json`의 원문 판독 기록을 뜻한다. 모든 자료를 이 문서 작성자가 다시 열었다는 뜻은 아니다. 최초 수집자의 판독, root의 선택 원문 재열람, 같은 모델 계열의 별도 내부 판독을 아래에서 구분한다. 정적 파일·공식 메타데이터, 당사자의 보고, 이번 실행의 다운로드/해시 확인, 연구자의 해석·제품 제안을 섞지 않는다. 패키지·CI·GUI를 이번 세션에서 실행해 기능 성공을 검증한 것은 아니다.

### 고정과 원격 확인

| 단계 | 확인된 고정 커밋 | 확인 범위·영수증 |
| --- | --- | --- |
| 표집·판정 계약 | `188152a5f561f8b478c3a850b9dcbc1c19894a59` | SCOPE 원격 원문. `evidence/commit-log.json`의 `01-protocol` |
| conda 과거 참조 부분 봉인 | `965b431de6756d0ec5422a1a005e37744884356a` | 6참조의 부분 봉인. 전체 A 미래 이력 개방 전 |
| **전체 A 봉인** | **`1714a55a529c7da42596ac0779d398f3aacf97c3`** | `evidence/a-seal.json` 원격 확인 2026-11-22T05:05:37Z. 이후에만 상류·소비자 미래 이력 조사 |
| ③H | `885537f8849d9fff1ecba3adf0068e9d8c70cc2f` | Homebrew chains blob 원격 일치. 05:39:32Z |
| ③C | `5ef2a246f4a18ac1eb6adb65e47660e03f49cab8` | conda chains blob 원격 일치. 05:41:07Z |
| ④ | `17229e1bde153aaf29290dceae4dad9172fe987f` | conda B cases blob 원격 일치. 05:43:57Z |
| ⑤ 집계·수용·자체 점검 | **내용 검산 완료; 커밋 아직 미생성** | 이 문서를 포함한 ⑤ 커밋을 만들고 원격 고정판을 확인한 뒤 HANDOFF 작성. 해당 SHA·영수증은 HANDOFF에 기록 |

위 원격 확인은 특정 파일 blob에 대한 영수증이다. 커밋 안의 모든 원문과 모든 계산을 독립 재실행했다는 뜻은 아니다. 상세 경로·SHA·시각은 `PROGRESS.md`와 `evidence/commit-log.json`에 있다.

## 분모·원문 최소수 점검

| 항목 | 현재 원장/인계 값 | 검산한 범위와 해석의 제한 |
| --- | --- | --- |
| A | 12참조, Homebrew 6·conda-forge 6, 서로 다른 소비자 프로젝트 12 | 봉인 기록과 최종 frame/references/chains/verdicts의 대응을 검사했다. 79/79 영수증의 `A sealed rows unchanged`와 47/47 별도 원장 검산에 행 수·계열·프로젝트 수를 보존 |
| A 판정 | 용도 유지 5, 특정 용도의 당사자 실패 보고가 있는 부적합 2, 보류 5 | 유지: A-H03/H04/C01/C02/C03. 보고: A-C04/C06. 보류: A-H01/H02/H05/H06/C05. 실행 성공률·전체 오류율·실제 사람의 오추천 피해율로 해석하지 않음 |
| B | 사전 원장 6회, A와 연결 중복 2회 | B-H01↔A-H02, B-H03↔A-H06. 새 참고 참조4, A+B 서로 다른 프로젝트16을 별도 검산했다. B의 성공·지연·추가 소비자를 A 분자/분모에 합산하지 않음 |
| 엄격한 날짜 완전 사슬 | 0건 | 다섯 시점의 숫자가 있는 행과 동일 목적·실제 소비 artifact·배포 효과가 연결된 완전 사슬은 다름. “실패가 0건”이라는 뜻 아님. 보강 목표 6건은 미달 |
| 동일 참조의 source commit→공개 source release | A-C04 후보판·안정판, A-C06 안정판: **2참조·3쌍** | `intervals.csv`와 별도 원장 검산에서 76,027초·1,004,454초·863,997초를 대조했다. source edition 포함/게시의 날짜쌍이며 실제 문서 서버·conda binary·GUI installer·첫 정상 실행 지연으로 승격하지 않음 |
| 통합 출처 행 | 348행 | 출처 ID 행 수이며 고유 원문/독립 사건 수와 다름 |
| 보수적 고유 원문 최소수 산입 | 87: A 과거 12, 상류 37, 후속 30, B 추가 과거 4, 타 분야 4 | sources의 산입·중복 key와 retrieval metrics, 별도 원장 검산을 대조했다. 후속30은 raw category followup19+consumer_followup11, B과거4는 b_consumer_original1+consumer_historical3. 동일 편집·미러·같은 커밋 여러 파일 중복을 제외 |
| 자료 최소수 조건 | 총32, A과거12, 상류8, 후속8, 타분야4의 수량 하한 충족 | 별도 검산의 source_minimum_categories 및 수용근거와 일치. 수량 충족이 기능·날짜 적합성의 미확인을 해소하지 않음 |
| 상류 사건 key | A10, B6, A+B 중복 제거14 | 별도 원장 계산과 RESULT 표2를 대조했다. 일상 버전 후계를 포함한 선택 사건 key이며 오류 사건·통계적 독립 실험 수가 아님. 원문87과 별개의 분모 |
| 읽기 기록량 | 서로 다른 직접 판독 URL288, 고정 Git revision134, root 재열람 영수증16 | 최종 retrieval metrics와 RESULT Q8을 대조했다. HTTP 총 요청 수, 최소 읽기량, 독립 실험 수, 인간 소요 시간 아님. 추가 tag 재확인 URL2개는 원문 최소수·고정 Git판 수를 늘리지 않음 |
| 사람 시간·운영 비용·전체 전파율·실제 오추천 피해 | 미확인 | 사람 읽기 시간과 기록 운영 비용을 측정하지 않았고 모집단 전파율을 추정하지 않음. 보고된 빌드/시작 실패와 오추천 피해를 구분 |

`0건`은 정한 적격 조건으로 확인한 행이 없다는 뜻이다. `해당 없음`은 사건·수정 필요성 자체가 적용되지 않는 상태다. `관측 실패`는 요청 실패/삭제·retained log 부재다. `미확인`은 값이나 인과 판단이 아직 정해지지 않은 상태다. 이 네 값을 서로 대체하지 않는다. A의 무사건 참조와 보류도 분모에서 제거하지 않는다.

## Q1. 결말을 보기 전에 참조를 선정했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 공개 개발환경 모집틀의 사전 순서·날짜·중복 규칙으로 A를 봉인했다. 확률표집·전체 소프트웨어 대표성·완전 맹검은 주장하지 않는다 | `SCOPE.md`의 “① 결과 열람 전 고정하는 주 표본 A”, `evidence/a-seal.json`, `evidence/exposure-log.jsonl`; 대표 원문 [H-S01](https://github.com/fish-shell/fish-shell/blob/efa9d5dd6a1a4f90e5a6d9372cddf539634be27e/CONTRIBUTING.md) L20–27/L37–43/L259–267, [C-S01](https://github.com/dask/dask/blob/c69d10f97cadd06f147817f0084bddeadb8195e6/continuous_integration/appveyor/environment.yaml) L1–8 | `collectors/homebrew/frame.json`의 alacritty/mpv/wezterm/tmux 탈락과 neovim/OBS의 더 이른 기준판 탈락을 보존했다. `collectors/conda/frame.json`과 과거 검색 기록은 scikit-image의 2019/2021 명시 채널 미확인, Spyder 2019의 다른 채널을 남긴다. 결말이 좋은 행으로 교체하지 않음 | 봉인 전 미래 source 접근을 보여 주는 영수증, 후보/날짜 순서 위반, 제외 후보에서 당시 직접 적격 파일을 발견하면 표집 절차 판정을 수정해야 한다. 최종 frame↔seal 대응은 validation 및 별도 원장 검산에서 확인했다 |
| “일반 도구”는 공식 카탈로그의 재사용 가능한 패키지로 해석했고 역할 차이를 보존한다 | `evidence/protocol-clarifications.md` 05:05 절; `collectors/cross/preseal-review.md`의 “일반 도구 범위”; C-S01–C-S06의 역할·목적 원문 | 별도 판독에서 NumPy·SciPy·applaunchservices가 라이브러리임을 지적했다. conda 6건을 범용 CLI 6건으로 부르지 않는다. Homebrew SDL2·Qt에도 같은 해석을 적용 | 사용자가 독립 CLI만으로 모집단을 한정한다면 이 A는 그 조건의 6+6을 충족한다고 할 수 없다. 그 경우 새 사전 표집이 필요하며 이번 성공/실패를 보고 행을 교체하면 안 됨 |

## Q2. 참조의 원래 목적과 호출을 같은 판에서 확인했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 환경 파일의 이름만으로 목적을 채우지 않고 같은 판의 설치 지시·호출·산출물과 연결했다 | [H-S03](https://github.com/kovidgoyal/kitty/blob/003f77b25733aee73981423e3464c59812558d2b/Brewfile) L1–5 + [H-S05](https://github.com/kovidgoyal/kitty/blob/003f77b25733aee73981423e3464c59812558d2b/setup.py) L45/L60–68/L260–275. C-S05의 requirements L1–4 및 같은 SHA INSTALL.rst L263–291, 특히 L278 `-c conda-forge --file requirements/default.txt`; C-S06 + [C-S17](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/CONTRIBUTING.md) L58–84, 특히 L63 | 봉인 전 내부 판독이 “requirements 파일은 pip 전용일 수 있다”는 반대 설명을 두 설치 명령의 정확한 `--file` 입력과 대조했다. 실제 conda-forge 선택 binary·solver 성공은 명시 채널만으로 확정하지 않음 | 해당 명령이 다른 파일/다른 SHA를 실제 사용했음을 보이는 contemporaneous CI 로그, 환경 lock/explicit artifact가 나타나면 연결을 수정. 당시 “stable”을 지금도 최신판을 원한다는 의도로 확장하지 않음 |
| 일부 구체 호출은 봉인 뒤 같은 과거 SHA를 보강해 찾았다. 이를 봉인 전 알고 있던 목적처럼 서술하지 않는다 | [C-F53](https://github.com/pandas-dev/pandas/blob/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/.github/workflows/ci.yml) L9–10/L99–121 + 같은 SHA `ci/setup_env.sh` L94–104: environment→warnings-as-errors docs. [C-F32](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/spyder/utils/qthelpers.py) L43–44/L121–123/L759–802: macOS register 호출. [H-F02](https://github.com/fish-shell/fish-shell/blob/efa9d5dd6a1a4f90e5a6d9372cddf539634be27e/build_tools/lint.fish) L81–107: `--rule-file` | 최초 C06 원장에 구체 런타임 호출 미확인을 남겼고 후속 C-F32를 보강으로 표시했다. C04는 일반 개발환경과 실제 docs job을 연결해 import 가능성만으로 문서 빌드 호환을 단정하는 설명을 반박 | 동일 목적의 사후 보강을 표집 기준의 사후 변경으로 사용하지 않는다. 소비자 release 판 포함 여부와 실제 실행·배포는 별도 근거 필요 |

## Q3. 상류의 이름·출력·기능과 실제 배포 시계를 구분했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 이름/주소의 존속·변경만으로 기대 기능의 유지/소실을 판단할 수 없다 | [H-U15](https://github.com/Homebrew/homebrew-core/commit/7ed0b0b9765d948cc6ebf62772c1073f1e17fe86) `Formula/c/cppcheck.rb` install diff + [H-U18](https://github.com/cppcheck-opensource/cppcheck/blob/a436ca35ed1887bee789765122b65ed2d7a7e045/cli/cmdlineparser.cpp) L1338–1441. 대조 [H-U19](https://github.com/Homebrew/homebrew-core/commit/562c37360f8133eda5870ab801d1a7710fe9abdc) alias/formula_renames diff와 [H-U20](https://github.com/Homebrew/homebrew-core/commit/ab9d906d072fb2c5ba6ca30b23cb3136e42de6c1) Qt5→Qt6 version/source diff | cppcheck는 같은 이름인데 rules 기능이 빠지는 정적 반례다. 반대로 Qt5 alias 이름 이동은 같은 Qt5 산출물을 가리키며 뒤의 Qt6 기본값 전환과 다른 사건이다. H01은 현재 조합의 정적 부적합을 2019 당시 오류나 현재 fish 실패로 소급하지 않음 | 당시 실제 bottle/API 가용성·소비 binary 및 해당 옵션 실행 결과가 필요. HTTP404는 formula API 경로 상태일 뿐 brew alias 실패를 자동 의미하지 않음 |
| recipe의 내부 이름·복수 outputs는 소비자가 설치한 이름과 다를 수 있다 | [BC-S01](https://github.com/conda-forge/matplotlib-feedstock/commit/08bc9282bb815e646617b28a94c85b6bc9ac31d3) package.name/outputs/build.number diff; [BC-S10](https://github.com/conda-forge/mamba-feedstock/commit/364da0d5190fa659c927183e938a7264a71fba95) outputs/entry_points/tests; [BC-S11](https://api.anaconda.org/release/conda-forge/mamba/0.18.0) distribution과 실제 archive `info/files`의 `bin/mamba`; C-F06/C-F60의 scipy-split과 scipy/scipy-tests outputs | B-C01의 2019 recipe cleanup은 소비자 `matplotlib` 이름 교체가 아니며 2018 split 사건으로 원장을 바꾸지 않았다. B-C02는 native/Python library 분리 뒤에도 mamba CLI를 유지한다. “분리면 옛 참조를 전부 고쳐야 한다”는 초기 가설을 반박 | 서로 다른 output이 실제 기대 CLI/API를 제공하지 않는 일치 artifact·호출 자료가 나오면 용도별 판정 변경. recipe root name만으로 artifact URL을 합성하지 않음 |
| 제안·source commit·merge·artifact upload를 서로 다른 날짜로 기록했다 | C-F33 NumPy recipe source diff, [C-F34](https://api.github.com/repos/conda-forge/numpy-feedstock/pulls/195) created_at/merged_at, [C-F50](https://api.anaconda.org/release/conda-forge/numpy/1.19.0) `distributions[].basename/upload_time/attrs.depends` | NumPy source 제안은 6월, merge와 확인된 upload는 7월이다. B-C03의 공식 4월 Qt 구성요소 공지(BC-S18), 6월 qt metapackage recipe/아카이브(BC-S17/19)도 같은 날짜가 아니다 | 정확한 platform/build의 최초 가용성 또는 소비 solve 영수증. 배포 미확인을 source 날짜로 대체하지 않음 |

## Q4. 소비자의 실제 경로 이력과 수정 배포를 연결했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 옛 경로 삭제와 수정 부재를 동일시하지 않았으며, 창 말의 같은 파일 내용으로 중간 불변을 주장하지 않는다 | H-F04 `CI/include/Brewfile` L1–5, H-C09 삭제 diff, [H-F10](https://github.com/obsproject/obs-studio/blob/099314795458ad249d3c7d7c6d6972ef5af4df07/.github/scripts/.Brewfile) L1–5 + H-F13 build-macos L199–267. C-F23/24/25의 conda.txt→main.yml→macos.yml. [C-F58](https://api.github.com/repos/jupyterlab/jupyterlab/commits/e13a60c49a361216e5e908e6f6c89d1b5a21597d) docs env 추가/requirements 삭제 및 RTD diff | `homebrew/future-search-log.jsonl` H-T05/06/31이 옛·새 경로를 따라간다. `conda/future-search-log.jsonl`의 main.yml/macos.yml 후속과 `counterexample_review`는 Jupyter conda→pip→conda를 찾았다. Dask workflow 교체는 단순 Git rename이라고 부르지 않음 | 빠진 중간 path/branch 또는 실제 배포된 파일을 보여 주는 기록. 공개 API path log가 모든 미공개/삭제 이력을 보장하지는 않음 |
| 소스 수정이 공개 source release에 포함된 경우와 대응 배포가 미확인인 경우를 분리한다 | [H-C06](https://github.com/qutebrowser/qutebrowser/commit/7b53f648141dd9b604fc01a8603faa55021576e7) Homebrew 설치 diff; [H-F07](https://github.com/qutebrowser/qutebrowser/blob/2fe78b7644605c1e6622573935e7a2404922cbcd/doc/install.asciidoc)·H-F12 L374–390; H-F08 L367–372. 비교 C-F18/C-F20 environment L1–10, C-F29 macos.yml L1–6 + C-F56/57 release 목록 | H-T25/26/32–37에서 릴리스 태그·목록을 재검토했다. qutebrowser `pyqt@5` main 수정 뒤 v2.5.3/2.5.4에는 이전 안내가 남고 v3은 다른 Qt6 참조다. kitty의 H-R02 archive 내용 확인도 최초 공개 시각이나 CI 효과의 확인과 분리 | `pyqt@5`를 담은 당시 문서 사이트/nightly/릴리스 불변판, 정확한 배포 성공 로그. 소스 release date만으로 실제 CI·사용자 도달을 채우지 않음 |
| 실제 실패·첫 성공은 맞는 목적의 당사자 자료에 한정한다 | C-F16 Pandas PR35312 body, C-F28 applaunchservices issue1 traceback; C-F55 check-runs/status 조회, H-T27 kitty retained runs 조회 | Pandas와 Spyder에는 특정 작업의 직접 실패 보고가 있다. 현재 조회의 run/check 0은 당시 실행 0 또는 성공의 증거가 아니다. B-H02 BH-S08/BH-S09/BH-S12의 다른 기능 수정·기존 성능 보고를 Python 전파 사슬에서 제외 | 실패한 정확한 환경과 첫 성공을 잇는 공개 CI log·artifact·배포 영수증. 지금 없는 로그를 가정한 값으로 메우지 않음 |

## Q5. 바뀌지 않은 참조와 바뀐 목적을 오류와 구분했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 유지 5건은 관측한 source 목적 범위이며 실행 성공률이 아니다. 의도적인 역사 고정을 명시 근거 없이 추정하지 않는다 | H-S06/H-F03의 Ninja 빌드 안내, H-S08/H-F04/H-F10/H-F13의 CMake 구성 역할; C-S01/C-F02/C-F68의 Python3.6; C-S02/C-F03/C-F69의 Sphinx/Python3.5; C-S03/C-F04/C-F36/C-F49의 setuptools | “Zig 추가→Ninja 폐기”, “기본 Python 최신 recipe→3.6 요구 소실”, “setuptools의 Python2 지원 종료→Python3 CI 실패”를 대조해 적용 범위 밖 반례로 처리했다. C01/C02 경로 이행은 별도 내부 판독에서 일관성 점검 | 같은 버전·platform·명령의 실패/성공 자료와 유지 의도의 직접 기록. 고정 커밋 존재만으로 deliberate pin, 끝판 유지로 전 기간 성공을 부여하지 않음 |
| 같은 후계가 다른 목적에는 상반된 답을 줄 수 있다. 먼저 바뀐 소비자 목적을 지연으로 계산하지 않는다 | [H-U17](https://github.com/libsdl-org/sdl2-compat/blob/e4df8a55f20da762290a78c2bbe8f8d89d01486a/README.md) L9–31/L82–84/L127–148: SDL2 API 호환층·새 SDL3 개발 구분. H-C04의 소비자 API 변경, H-F09/H-R03의 SDL3 source release. C-F44/C-F46/[C-F59](https://api.github.com/repos/scikit-image/scikit-image/pulls/7576) sparse-array 전환 | scrcpy는 공급자 sdl2 replacement보다 먼저 SDL3 개발 목적으로 옮겼다. SciPy 1.11.2 하한은 새 sparse-array 사용에 연결되므로 옛 Gaussian 목적의 정정 지연으로 쓰지 않는다. conda `counterexample_review`가 해당 PR/issue를 따라갔다 | 과거 Gaussian 호출이 같은 결함에 실제로 실패했음을 보이는 고정판 재현, 또는 SDL2/SDL3 각각의 정확한 실행 결과. 먼저 바뀐 날짜를 음수 전파 지연으로 만들지 않음 |
| 실제 관측 부적합 2건은 특정 당사자 작업에 한정한다 | [C-F16](https://api.github.com/repos/pandas-dev/pandas/pulls/35312) body의 warnings-as-errors docs 실패; [C-F28](https://api.github.com/repos/impact27/applaunchservices/issues/1) Python3.10 conda Spyder 시작 실패; C-F25/26의 최소판 변경 | NumPy import가 가능하다는 사실로 문서 빌드 실패를 지울 수 없다. 반대로 Spyder 옛 `>=0.1.7` 범위도 0.3.0을 허용하므로 수정 전 모든 사용자가 실패했다고 할 수 없다. C06 metadata “보장” 문구를 축소한 내부 판독 권고 반영 | 정확한 failed artifact, 첫 성공 solve/GUI 실행과 사용자 범위. 빌드/시작 실패를 실제 사람의 오추천 피해로 동일시하지 않음 |

## Q6. 날짜 쌍·범위·검열의 적격성을 지켰는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 현재 A에서 엄격한 Tu→Tc 전파 지연이나 완전 사슬을 확정하지 않는다 | C-F50/C-F52 artifact별 upload metadata, C-F55 retained log 부재, C-F28의 상류 수정 이전 실패. Homebrew chains의 Tu=null/`START_UNRESOLVED`. `SCOPE.md`의 다섯 시점·365일·검열 정의 | Pandas의 Linux/Python 후보 artifact 차이는 조건부 범위다. Spyder는 보고가 0.3 배포보다 먼저이고 architecture/build가 불명이다. 상류 수정일을 실패 발생일로 대체하지 않는다. Homebrew Tu 미확인을 우측 검열로 합산하지 않음 | 같은 소비자가 사용한 platform/build/기능의 실제 노출 영수증. 사건·시작점 미확인은 “우측 검열”이라는 통계적 관측이 아님 |
| 적격 source commit→source release는 A 2참조·3쌍이다 | A-C04 C-F15→C-F18/C-F56(rc0), C-F20/C-F19(stable); A-C06 C-F25→C-F29/C-F57(stable). 수집자 `chains.json`의 `source_commit_to_release_intervals` | 수집자 값은 각각 76,027초, 1,004,454초, 863,997초다. rc를 stable로, source release를 설치 binary/서버 배포로 바꾸지 않는다. 통합 intervals·RESULT와 별도 산술 검산의 값이 일치한다 | release 시각/포함 source SHA가 정정되거나 그보다 앞선 대응 source 배포물이 발견되면 첫 관측 시각을 갱신. 실제 첫 효과는 별도 자료 |
| H02 및 B-C02의 과도한 시간 의미를 제거했다 | H-R01 `assets[id=213583777].created_at/updated_at/state`, H-R02 archive 영수증; `evidence/independent-read-review.md` IR-M01. [BC-S16](https://github.com/conda/conda-libmamba-solver/blob/f93d38a190d912902ec90729304ea2936dd0976b/conda_libmamba_solver/solver.py) L1–4/L36 및 pyproject 의존성 | H02의 약22.4743일은 asset record 필드와 Tc의 산술차만 남고 first-distribution 적격=false. BC-S16은 첫 읽힌 판이 libmambapy라는 사실만 확인하며 이전 mamba 참조/전환 자체가 미확인이므로 **좌측 검열 산입도 보류** | H02 당시 upload/publication 로그와 시각 필드의 의미; BC-S16의 실제 이전 참조 및 전환 시점을 묶는 불변 parent/이력. “첫 관측 때 이미 새 값”만으로 존재 미확인 전환의 좌측 검열을 만들지 않음 |
| B는 사전 원장 6회 역추적의 탐색 결과이며 A 지연 통계의 보충 분자가 아니다 | `SCOPE.md` B-H01~03/B-C01~03; `collectors/homebrew-b/search-log.jsonl`; `collectors/conda-b/ledger-scan.json`·`search-log.jsonl`·`cases.json` | B-C01의 2018 선행 split, B-C03의 Python3.11 신규 목적과 후속 복구, B-H01의 2019–2023 비적격 결과 후 2024 보조 사건을 명시했다. B-C02 CLI와 library 관점 차이를 보존하되 library 이전 전환은 미확인. B-H01/03의 A 중복2는 연결만 함 | 공식 원장에 더 이른 적격 관계 변경이 있음을 보이는 diff나 일치하는 소비자 predecessor. B의 선택 편향과 서로 겹치는 작성자 계보를 제거했다고 주장하지 않음 |

## Q7. 타 분야에서 옛 ID 보존의 정확성을 확인했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 연구 내용 인용과 정정 공지 인용의 대상은 다를 수 있어 정정 DOI로 기계적 치환하면 안 된다 | [X-S01](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0165166) “Notice of Republication”, S1/S2 설명·Reference1; [X-S03](https://jevinwest.org/papers/Piwowar2018peerj.pdf) p.1 출판 metadata, p.5 open-access citation advantage, p.22 Ottaviani reference | `collectors/cross/search-log.jsonl` SEARCH01–10 및 ACCESS02–05. 이후 PeerJ 논문의 실제 본문·참고문헌은 연구 DOI `.0159614`를 유지한다. 정정 공지 DOI `.0165166`를 연구 인용으로 바꾸지 않았다는 관측이다. 출판사 공지는 재발행을 설명하지만 S1/S2 원문은 직접 읽지 못함 | 정정 전·후 보충 PDF와 후속 저자의 날짜 있는 인용 수정 이력. 현재 자료는 후속 인용의 정확성 조건을 보일 뿐 실제 정정 전달 경로나 저자의 수정 지연을 증명하지 않음 |
| 역사 대상의 영토·시대·표목 역할을 보존해야 하는 소장목록에서는 옛 표목이 정확할 수 있다 | [X-S04](https://www.loc.gov/aba/publications/FreeCSB/CSB_060.pdf) printed pp.2–4 “Division of Czechoslovakia and Yugoslavia”, descriptive/subject practice; [X-S05](https://archive.org/download/harvard_bibliographic_metadata/20220215_017.bib.mrc)의 offset295257330, length2338, MARC001/005/040/043/245/260/505/651/852/876. [X-S12](https://archive.org/metadata/harvard_bibliographic_metadata) 파일 checksum 및 bounded record 영수증 | LC 사건 원문은 새 Czech Republic/Slovakia 표목과 과거 Czechoslovakia 사용을 구분한다. Harvard의 실제 소장 항목은 1937–1938·1968 역사 내용에 옛 국가 subject/지리코드를 사용한다. SEARCH05/06과 ACCESS07–10으로 현재 카탈로그 대신 고정 export의 실제 소장 기록을 확보 | 같은 소장 항목의 날짜 있는 이전판·전거 갱신 로그·사용 의도 설명. 2022라는 파일명은 당시 공개 시각의 단독 증거가 아니며 보존본의 현재 manifest 수정 시각과 분리한다. 명시 의도나 1993→2022의 연속 불변을 추정하지 않음 |

두 분야는 각 2개 고유 원문으로 최소수4를 충족하는 기록이 있으나, 날짜 있는 실제 소비자 **수정** 사슬 두 개를 확보한 것은 아니다. 현재 페이지만 있는 ID 조회·검색 요약·차단 자료는 그 증거로 쓰지 않았다. 보충 자료의 공개 대체는 어디까지 같은 내용을 대신하는지 `sources.json`과 cross 접근 실패 기록에 남겼다.

## Q8. 제품에 보존할 필드의 필요성과 대가를 반증했는가?

| 주장·적용 범위 | 직접 근거 ID·정확한 위치 | 반증을 찾은 범위·결과 | 주장을 바꿀 최소 자료·남은 점검 |
| --- | --- | --- | --- |
| 주소+기대 기능/판은 주소만보다 역할을 구별하지만, 모든 질문에 전체 이력이 필요한 것은 아니다 | `collectors/*/verdicts.json`의 A12 `record_ablation` 또는 `mask_L1/L2/L3`; C-S01/C-F02/C-F68의 Python3.6 역할, C-S02/C-F03/C-F69의 Sphinx entrypoints, C-S05/C-F06/C-F60의 scipy 출력 구별 | “이력은 항상 전부 저장해야 한다”는 가설에 반례: Python minor/platform과 해당 recipe로 기대 interpreter identity를, 기능/module+output으로 scipy와 scipy-tests를 구별할 수 있다. 다만 언제 경로가 바뀌고 실행됐는지는 추가 이력 필요 | 동일 질문에서 L1/L2만으로도 답을 재구성하는 새로운 반례 또는 정확한 실행 자료. 이 점검은 충분조건의 제품 제안이며 통제 실험의 정답률 아님 |
| 인용 시점·원문·관계를 더해야 복구되는 질문이 있고, L3에도 미확인이 남는다 | H-F02/H-U15/H-U18/H-C02의 rules 기능과 목적 변화; H-C06/H-F07/H-F12의 source/release 차이; C-F53/C-F54/C-F16/C-F50/C-F55의 docs 목적·artifact 미확인; C-F23/24/25의 경로 chain | H01은 “C++ lint” 정도의 기능 기록만으로 custom rule 필요를 놓친다. H04는 URL 삭제만 보면 새 path의 같은 역할을 놓친다. C04는 전체 source·PR·metadata를 보아도 실제 solve/첫 성공은 모른다. H02도 archive를 읽었다는 사실이 최초 공개 시각을 만들지 않음 | 소비자가 실제로 사용한 lock/explicit URL, 실행·배포 영수증. 기록 비용을 늘리면 모든 결론이 자동 확정된다는 제안을 하지 않음 |
| 비교는 같은 자료를 이미 본 연구자의 구조적 필드 가림 점검이고 기록량만 측정했다 | `SCOPE.md` Q8, 수집자 verdict의 `mask_method`, `evidence/retrieval-metrics.json`의 산식·URL/revision 목록 | A12 모두 동일 원자료를 L1 주소, L2 기능/판/목적, L3 원문/시점/관계로 나눴다. **외부 독립 맹검·사용자 효율 실험이 아니다.** URL288/Git134는 기록된 고유값이고 요청수·사람시간이 아님 | 별도 사람이 가려진 자료만 보고 답한 정확성·시간 실험, 실제 저장·유지 비용 기록. 현재 전체 비용 절감이나 재확인 시간 감소율은 미확인 |

## 자체 검토·별도 내부 판독·원장 검산의 구분

| 층위 | 수행자·기록 | 무엇을 확인했는가 | 독립성·범위 제한 및 반영 |
| --- | --- | --- | --- |
| 수집자 자기 검토 | 각 collector의 notes/verdicts/검색·접근 실패 기록; Homebrew future-self-check, conda future-check-receipt, conda B validation | 같은 자료의 반대 설명·날짜/역할 분리·행과 출처 대응 | 수집 결과에 이미 노출됨. 자체 검토를 독립 재현으로 부르지 않음 |
| root 통합 재열람 | `evidence/root-rechecks.json`, `review-sources.json`, `retrieval-metrics.json` | 선택 원문과 통합 판정·날짜 의미를 다시 확인. 현재 root 재열람 영수증16 | 전수 독립 판독 아님. 재열람 기록과 URL/Git판의 고유값은 서로 다른 측정 단위 |
| 봉인 전 별도 적격성 판독 | `/root/cross_domain`, `collectors/cross/preseal-review.md` | 당시 고정파일·설치 명령·정확한 --file·역할. C05/C06 연결과 library 범위를 대조 | 같은 모델 계열의 비맹검 내부 판독. 미래 이력은 미열람 상태. library 해석 명확화는 과거 수집 뒤 전체 A 봉인·미래 개방 전에 기록했으며 최초 후보 선정 전부터의 해석이라고 부르지 않음 |
| 봉인 후 별도 원문 판독1 — Homebrew/Borg | `/root/cross_domain`, `evidence/independent-read-review.md` | H02 시간 의미, H01 목적 소급, H06 source/release, B-H02 다른 기능 수정 전이. 핵심4원문+고정판1+API문서 재열람 | Homebrew 최초 수집자는 아니지만 같은 모델 계열이고 수집자의 설명을 읽은 비맹검. H02 first-distribution 부적격 처리 반영. 전체12행 실행 재현 아님 |
| 봉인 후 별도 원문 판독2 — conda 날짜·목적 | `/root/homebrew_a`, `evidence/independent-conda-review.md` | C04/C06 직접 실패·같은 목적·수정·배포 한계: 원문4묶음/7GET. C01/C02는 경로 이행의 원장 일관성 점검 | conda 최초 수집자는 아니지만 같은 모델 계열 내부 판독. C06 metadata 보장 문구 축소 반영. C01/C02를 직접 원문 재판독과 같은 범위로 부르지 않음 |
| 봉인 후 별도 원문 판독3 — B·타 분야 | `/root/homebrew_a`, `evidence/independent-b-cross-review.md` | B-C01~03/B-H02, X-BIB01/X-LIB01. 역할·보고자 계보·B R1/R2 분리·MARC/전거 ID/날짜와 bounded record 재열람 | 대상 자료의 최초 수집자는 아니지만 같은 모델 계열 내부 판독. BC-S16의 좌측 검열 추정 제거, 서로 다른 namespace의 직접 split과 snapshot 시각 오독 방지. 역사 소비자 수정 경로까지 확인한 것은 아님 |
| 최종 보고서 문장 감사 | `/root/cross_domain`, `evidence/final-report-review.md` | root가 작성한 RESULT의 네 표·Q7·마지막3행과 source ID의 의미 연결. C-F33/15 및 C-F36/65 연결, L1 범위·서지 DOI 역할·자체점검 갱신 지적 | 기존 Q7/B 수집에 참여했으므로 그 원자료의 독립·맹검 검증이 아님. 자신의 SELF_CHECK 문서 갱신은 별도 독립 판독으로 세지 않음. 해당 감사의 수정은 아래 해결 기록에 남김 |
| 동일 수집자의 최종 내용 QA | `/root/homebrew_a`, `evidence/final-homebrew-report-review.md` | Homebrew 날짜·목적·A/B 판정과 최신 RESULT를 대조. Borg 하한 변화의 표현과 OBS 첫 이동 원문 연결 보강 | Homebrew A를 수집한 동일 에이전트의 자기 결과 대조다. 새 외부 원문 수집·독립 실행 재현 아님. 다른 수집자가 작성한 Homebrew B 대조 범위를 별도 표시 |
| 별도 구현의 원장·산술 검산 | `/root/conda_a`, `evidence/independent-ledger-check.json` | 생성기 계산을 재사용하지 않은 전체 **47/47**, 이후 증분 **7/7** 확인. B-C01 마지막판 시각, C04 후보/안정 tag 연결, L1/L2/L3 키를 보존한 직렬화, 모든 시간쌍 재계산을 대조 | A-conda 수집자이므로 모든 자료에 독립인 검토자는 아니다. 계산 구현의 별도성이지 외부인 독립 검토·원문 전체 재현이 아님. 증분 검사에서 분모·수치·판정 변경 없음 |
| 통합 검증 실행 | root, `scripts/validate.py` → `evidence/validation.json` | 봉인 입력, 원장·산술·파일 구조·소유 경로 등 **79/79** 통과 | 기계적 정합성 검사. 올바른 URL을 틀린 주장에 붙인 의미 오류는 최종 문장 감사가 따로 찾아 수정했으며, 역사 runtime을 검증하는 시험은 아님 |

위 활동들은 같은 모델 계열의 협업·내용 QA이며 외부 연구자·외부 기관의 독립 검토가 아니다. SELF_CHECK 작성자는 Q7/B-C 수집과 일부 내부 판독에 참여했다. 자기 수집분에 대해 이 문서만으로 독립 판독을 주장하지 않으며, 작성자 수·판독 파일 수·원문 수를 서로 다른 분모로 유지한다.

## 최종 감사 지적의 적용 확인

2026-11-22T06:10 UTC 이후 현재 RESULT와 통합 입력을 다시 읽어 아래 수정의 적용을 대조했다. 앞선 판독 파일은 발견 당시 상태를 보존하며 이 절과 `evidence/review-resolutions.json`이 후속 적용 확인을 제공한다. SELF_CHECK의 검산 상태·기록량 갱신은 이 문서의 자기 점검이며 새 독립 판독으로 추가하지 않는다.

| 지적 | 적용 확인 | 남긴 한계 |
| --- | --- | --- |
| NumPy 상류 recipe와 소비자 pin의 ID 혼동 | 표1 A-C04의 2020-06-20 recipe는 C-F33, 07-16 소비자 pin은 C-F15로 분리 | 6월 source 작성·7월 merge/upload·실제 실패 artifact의 날짜 역할도 분리 |
| setuptools44 후계와45 지원범위의 ID 역전 | C-F65는42.0.2→44.0.0, C-F36은45 build1의 Python<3.5 제외로 표1·표3·표4에 대응 | napari의 Python3 목적에 Python2 지원 중단을 실패로 전이하지 않음 |
| SciPy 과거 안정판과1.12 후계 혼동 | A-C05의 옛 안정1.11.4 recipe C-F70, 1.12 후계 diff C-F60으로 수정 | Gaussian과 뒤 sparse-array 용도는 다른 요구이며 정확한 solve는 미확인 |
| Q8 L1에 이후 이력/실행 정보가 들어감 | H02 L1은 주소·이름만/실제 구현 미확인, C04 L1은 주소·패키지명/실제 import 실행 미확인으로 축소 | alias 관계와 source 역사 정보는 이후 단계로, 실행 결과는 별도 자료로 남김 |
| Q7 연구 DOI 유지와 정정 전 과거판 보존 의도 혼동 | 연구 DOI/정정 공지 DOI의 역할과 도서관의 역사 지리 범위를 구분 | PLOS 소비자의 정정 전 판 보존 의도, 공지 전달·인용 수정일은 미확인 |
| Q1 library 해석 명확화의 시점 | RESULT를 다시 읽어 “전체 봉인·미래 이력 개방 전 해석 명확화”로 바뀐 문장을 확인 | 과거 자료를 이미 수집한 뒤의 해석 보충을 최초 표집 전부터의 설명으로 소급하지 않음 |
| H02 자산 시각·C06 보장·BC-S16 좌측 검열 | first-distribution 적격=false, C06 최소판 요구 범위로 축소, BC-S16 predecessor 미확인으로 검열 산입 보류 | 원자료의 메타데이터·정적 기능·보고 사실은 보존하고 실제 효과/이전 전환을 추정하지 않음 |

## 최종 내용 검산 결과와 인계 순서

| 확인 항목 | 결과 | 영수증·남는 제한 |
| --- | --- | --- |
| RESULT 제목 바로 아래 네 필수 표 | 순서와 데이터 행 수 **18/6/14/8** 확인 | final-report-review 및 final-homebrew-report-review. 표1은 A12+B6, 표2는 계열/전체6행, 표3은 A12+보조2, 표4는 Q1~8 |
| A12/6+6/12프로젝트, B6/중복2, 유지5·보고2·보류5, 완전사슬0 | 통합 파일·RESULT와 별도 원장 값 일치 | independent-ledger-check 전체47/47+증분7/7, validation79/79. 실제 오류율·피해율로 바꾸지 않음 |
| 날짜쌍2참조3쌍·H02 부적격·C06 범위·BC-S16 검열 보류 | CSV와 보고서의 적격성·산술·문장 제한 확인 | source release와 실제 소비자 실행·운영 배포를 분리. B-C03-R2는 보조3쌍으로 A에 더하지 않음 |
| 출처348/보수적87, 범주 최소수·중복 | 통합 sources·counts·retrieval metrics·검산 영수증 일치 | URL288/Git134/root영수증16은 다른 측정량. 실제 요청 수·사람 시간·기록비용 미측정 |
| 무사건·고의 고정·복수 후계·결정 불가의 분모 | 무사건A2, 의도적 역사 재현 pin 확인0, 보류A5 등을 분리 | 관측 미확인을0일/오류0/우측·좌측 검열로 바꾸지 않음. 관계 key와 지원 기능을 별도 열로 유지 |
| 조건별 수용 근거 | `acceptance-evidence.json` **18조건 중15 true·3 false** 확인 | false는 완전사슬6개 보강 목표, 실제 artifact→실행·효과·운영 배포, 타 분야 날짜 있는 정정/ID 계보. 각각 재개 입력이 있으며 REVIEW_READY_WITH_GAPS 유지 |
| RESULT 마지막 약점 표 | 네 열, 정확히 **3데이터 행**, 문서 맨 끝 확인 | 영향순으로 공급 artifact·동일 수정의 첫 배포·도서관 전후 계보. 아래의 자체점검 마지막3행도 같은 순서 |
| ⑤ 커밋과 HANDOFF 순서 | **내용 검산 완료; ⑤ 커밋 아직 미생성** | 이 문서를 포함한 집계·수용·자체 점검을 먼저 커밋하고 GitHub 고정 SHA의 파일을 확인한 뒤 HANDOFF 작성. 해당 SHA·영수증은 HANDOFF에 기록 |

## 영향이 큰 남은 약점과 다음 조사

| 약점 | 영향을 받는 판단 | 다음 조사 한 건과 최소 확인 |
| --- | --- | --- |
| 공급 artifact와 실제 실패/성공 환경이 연결되지 않음 | Tu→Tc 전파 지연, 엄격한 완전 사슬, 같은 목적의 정정 효과 | Pandas2020-07-16 web_and_docs의 보존 로그 한 쌍에서 conda explicit URL/Python minor와 pin 전 실패·pin 후 첫 성공을 고정한다. C-F50/C-F54/C-F55/C-F16을 재개 입력으로 사용 |
| 동일 수정의 source commit·source판 존재와 최초 실제 배포가 다름 | commit→첫 배포 지연, 배포 성공률; H02 자산 시각과 H06 다른 Qt계열 릴리스의 잘못된 대체 | qutebrowser7b53f648의 첫 docs/nightly artifact 또는 배포 로그 한 건에서 pyqt@5 문구 자체와 공개 시각을 확인한다. H-C06/H-F07/H-F08 및 H-R02/R-S01을 구별하고 pyqt@6 판으로 대체하지 않음 |
| 도서관 subject ID의 전후 계보와 snapshot 최초 공개일이 미확인 | sh계열을 n계열로 직접 분리했다는 주장, 1993→2022 정정 지연 | 동일 Harvard001의 이전 불변 export 한 판과 원 배포 영수증을 확보해651/043/소장필드 변화·ID종류·실제 판 공개일을 구별한다. X-S04/X-S05/X-S12와 현재2338바이트 record/hash로 동일 항목을 고정 |
