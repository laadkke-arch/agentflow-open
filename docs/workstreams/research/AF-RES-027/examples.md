# AF-RES-027 · 확인된 인용 사슬과 끊긴 사슬 8개

이 문서는 현재 source·사례 원장에 있는 연결을 다시 읽기 쉽게 풀어 쓴 것이다. 새 표본, 새 원문 조회, 새 계산, 외부 소프트웨어 실행은 추가하지 않았다. 근거 ID는 [sources.json](sources.json), 상세 단계는 각 수집자의 사례·chain 원장에 대응한다.

**source의 명령·설정, 당사자의 실패 보고, 이번 실행의 아카이브 판독은 서로 다른 증거다.** 파일이나 패키지에 수정 내용이 있다는 사실을 실제 CI·GUI·문서 서버의 정상화로 바꾸지 않는다. B 사례와 타 분야 사례는 A의 분모·성공률에 더하지 않는다. 아래에서 시행일이 미확인이면 commit·merge·현재 조회일로 대신하지 않았다.

| 사례 | 읽을 때 확인할 차이 | 사슬이 끊긴 곳 |
| --- | --- | --- |
| A-H01 | 같은 이름의 도구라도 필요한 옵션이 사라질 수 있고, 기여 문서는 해당 안내를 먼저 지울 수 있음 | 실제 upstream 첫 시행과 옛 소비자 실행 결과 |
| A-H02 | 수정 source archive의 내용 확인과 그 archive의 최초 공개 시각 확인 | asset metadata를 실제 Tr로 해석할 근거, CI 개선 효과 |
| A-H06 | main의 중간 수정과 나중 release의 최종 참조 | pyqt@5 변경 자체의 첫 배포 |
| A-C04 | 원래 문서 빌드 목적, 제안일·배포 후보·실제 선택 artifact | 실패 CI가 선택한 정확한 NumPy build |
| A-C06 | 기존 실패의 수정과 새 배포 때문에 생긴 실패 | 실패 환경·첫 정상 solve/GUI 실행 |
| B-C02 | mamba CLI 소비자와 libmambapy API 소비자 | 실제 CLI 실행, API 소비자의 이전 참조 |
| B-C03 | 원래 Qt 5.12 시험과 나중 Python 3.11/Qt 5.15 시험 | 원래 목적의 부적합 여부, 우회/복귀가 적용된 실제 CI |
| X-LIB01 | 현재 국가의 식별과 과거 전체 영역의 역사 주제 | 동일 소장 record의 전후 수정판·첫 공개 |

## 1. A-H01 · cppcheck 이름은 남지만 user-rule 기능은 사라진다

**옛 참조의 목적.** fish의 고정 소비자 판은 `efa9d5dd6a1a4f90e5a6d9372cddf539634be27e`, 2019-12-31T22:16:20Z다. [CONTRIBUTING.md](https://github.com/fish-shell/fish-shell/blob/efa9d5dd6a1a4f90e5a6d9372cddf539634be27e/CONTRIBUTING.md)는 Homebrew cppcheck 설치와 C++ lint 목적을 함께 제시한다(H-S01). 봉인 뒤 같은 과거 SHA의 [build_tools/lint.fish L81–107](https://github.com/fish-shell/fish-shell/blob/efa9d5dd6a1a4f90e5a6d9372cddf539634be27e/build_tools/lint.fish#L81-L107)을 추가로 읽어 `--rule-file=.cppcheck.rules` 전달까지 확인했다(H-F02). 이 세부는 Q2의 **봉인 뒤 보강**이며 최초 표집 원장을 소급 변경하지 않았다.

확인된 순서는 기여 문서의 안내 삭제가 먼저다.

1. **당시 공급자 recipe**: [`00c8278face7ab08d37330a3c0a7a6877d3b8acb`](https://github.com/Homebrew/homebrew-core/blob/00c8278face7ab08d37330a3c0a7a6877d3b8acb/Formula/cppcheck.rb)는 Cppcheck 1.90과 `HAVE_RULES=yes`를 명시한다(H-U01). recipe 판독이며 설치 성공 기록은 아니다.
2. **기여 문서의 안내 삭제**: 2024-04-12T09:27:55Z의 [`59922d0859781ea9202f8312da8f43c7c15cd192`](https://github.com/fish-shell/fish-shell/commit/59922d0859781ea9202f8312da8f43c7c15cd192)는 기여 문서에서 C++/cppcheck 설명을 지운다(H-C02). Rust 전환 맥락이 보이지만 저장소 전체의 C++ 코드나 모든 현재 도구 사용이 없어졌다는 전수 확인은 아니다. 2026년 공급자 변경에 반응한 정정으로도 볼 수 없다.
3. **나중 공급자 기능 제거**: 2026-01-11T02:18:45Z의 [`7ed0b0b9765d948cc6ebf62772c1073f1e17fe86`](https://github.com/Homebrew/homebrew-core/commit/7ed0b0b9765d948cc6ebf62772c1073f1e17fe86)는 pcre 의존성을 없애고 `HAVE_RULES=OFF`로 바꾼다(H-U15). [bottle rebuild 1 기록](https://github.com/Homebrew/homebrew-core/commit/8eda88f5198ed8c1ae74df5f6e7c1da7060d7e29)은 03:07:28Z, [PR 262253 merge](https://github.com/Homebrew/homebrew-core/pull/262253)는 03:16:31Z다(H-U22–23). 실제 사용자 첫 시행일 Tu는 미확인이다.
4. **이번 정적 대조**: [Cppcheck 2.22.0 고정 parser `a436ca35ed1887bee789765122b65ed2d7a7e045`, L1338–1441](https://github.com/cppcheck-opensource/cppcheck/blob/a436ca35ed1887bee789765122b65ed2d7a7e045/cli/cmdlineparser.cpp#L1338-L1441)는 rules 지원 없이 해당 옵션을 받으면 실패를 반환한다(H-U18). 이는 옛 호출과 현재 recipe의 **정적 불일치**다.

**끊긴 곳.** 옛 명령을 실제 macOS binary로 실행한 결과와 사람의 오추천 피해는 미확인이다. 2019 문서가 당시 잘못됐다고도, 현재 fish 유지관리자가 그 문서를 정정해야 한다고도 바로 결론낼 수 없다. 현재 기여 문서의 안내와 과거판 재현자의 요구가 다를 수 있으며, 전체 현재 기능이 폐기됐다고 전수 확인하지 않았다.

**다음 불변판.** fish 2019 SHA와 정확한 rules-OFF bottle SHA·OS·명령 입력을 짝지은 실행 로그, 그리고 그 bottle/API의 최초 공개 기록이 필요하다. 옛 1.90 recipe로 재현하려는 명시적 의도도 확보해야 “보존”과 “현재용 정정”을 가를 수 있다.

## 2. A-H02 · kitty 수정은 실제 source archive에 있지만 최초 Tr는 미확인이다

**옛 참조.** kitty `003f77b25733aee73981423e3464c59812558d2b`, 2019-12-29T16:33:08Z의 [Brewfile](https://github.com/kovidgoyal/kitty/blob/003f77b25733aee73981423e3464c59812558d2b/Brewfile)은 `pkg-config`를 설치한다(H-S03). [같은 판 setup.py](https://github.com/kovidgoyal/kitty/blob/003f77b25733aee73981423e3464c59812558d2b/setup.py)는 이 명령으로 harfbuzz/libpng 등의 compiler flags를 조회한다(H-S05).

- **공급자 구현 교체 source**: 2024-11-12T03:24:54Z의 [`48b5788c062ba492c34890e1b2a7cb26c8a1505f`](https://github.com/Homebrew/homebrew-core/commit/48b5788c062ba492c34890e1b2a7cb26c8a1505f)는 pkg-config 이름을 pkgconf에 연결하고 같은 CLI 이름의 symlink를 추가한다(H-U14; B-H01과 같은 상류 사건). 이 commit 날짜는 실제 Tu가 아니다.
- **소비자 수정 Tc**: 2024-11-23T14:18:05Z의 [`e625f0aa024d7277287edac0c5c04c0239c5da0e`](https://github.com/kovidgoyal/kitty/commit/e625f0aa024d7277287edac0c5c04c0239c5da0e)는 Brewfile의 직접 설치 줄을 지운다(H-C01). 제목은 pkgconf를 빼면 CI가 개선되는지 보려는 시도다. 성공 보고로 읽지 않는다.
- **공개 source 판의 내용**: v0.38.0의 고정 source `d3f93cb0cb84b7b61c4a41f0dbfa2d816ba5908e` [Brewfile](https://github.com/kovidgoyal/kitty/blob/d3f93cb0cb84b7b61c4a41f0dbfa2d816ba5908e/Brewfile)에는 해당 줄이 없고, [setup.py](https://github.com/kovidgoyal/kitty/blob/d3f93cb0cb84b7b61c4a41f0dbfa2d816ba5908e/setup.py)는 여전히 pkg-config를 호출한다(H-F05,H-F11).
- **이번 아카이브 판독**: [실제 v0.38.0 source archive](https://github.com/kovidgoyal/kitty/releases/download/v0.38.0/kitty-0.38.0.tar.xz)를 HTTP 200으로 받아 `kitty-0.38.0/Brewfile`을 읽었고 같은 삭제를 확인했다(H-R02). SHA256은 `96fe79a645ec57a378295cdf16204265768091338d77efb058977b60209bb8ff`다. 아카이브 코드는 실행하지 않았다.

**시각의 역할.** [release metadata](https://api.github.com/repos/kovidgoyal/kitty/releases/tags/v0.38.0)의 page published는 2024-12-16T01:40:10Z, source asset created/updated는 01:41:05Z/01:41:07Z다(H-R01). 그러나 `updated_at`이 최초 업로드 완료나 최초 공개 접근 시각이라는 보장은 확인하지 못했다. 별도 판독을 반영한 원장은 이 metadata 차이를 **Tr 지연 부적격**으로 두며, 실제 최초 공개 시각은 미확인으로 남긴다. 내용이 공개 archive에 존재함을 확인한 것과 최초 배포 날짜를 고정한 것은 다르다.

**끊긴 곳.** Homebrew Tu, source asset의 최초 공개 시각, CI 개선 효과가 끊겨 있다. 현재 Actions 조회의 retained run 0은 당시 실행이 없었거나 성공했다는 뜻이 아니다. 직접 설치 줄 삭제를 실행명이나 compiler-flags 목적의 폐기로 읽는 것도 틀리다.

**다음 불변판.** e625f0aa와 parent의 당시 macOS CI 로그·정확한 pkgconf 환경, source asset 213583777의 첫 공개 기록, 공급자 API 첫 발행 기록이 필요하다. [release-archive-receipt.json](collectors/homebrew/release-archive-receipt.json)은 현재 확인한 내용의 영수증으로 남는다.

## 3. A-H06 · pyqt@5 수정 commit을 나중 release에 그대로 대입할 수 없다

**옛 목적.** qutebrowser `d38ade9ee9791bf01c7466458f3efbb4e298e93d`, 2019-12-31T15:55:22Z의 [설치 문서](https://github.com/qutebrowser/qutebrowser/blob/d38ade9ee9791bf01c7466458f3efbb4e298e93d/doc/install.asciidoc)는 `brew install qt5`를 안내한다(H-S12). [같은 판 호출부](https://github.com/qutebrowser/qutebrowser/blob/d38ade9ee9791bf01c7466458f3efbb4e298e93d/qutebrowser/browser/webengine/webenginetab.py)는 PyQt5.QtWebEngineWidgets를 사용한다(H-S13). Qt C++ toolkit, Python bindings, WebEngine 요구를 이름 하나로 합칠 수 없다.

1. **소비자의 먼저 바뀐 지시**: 2020-09-29T13:45:19Z [`59ac5b6b690963e514220886a60a1c5b47aa1188`](https://github.com/qutebrowser/qutebrowser/commit/59ac5b6b690963e514220886a60a1c5b47aa1188)는 qt5를 qt로 바꾸고 PyQt/PyQtWebEngine 수동 빌드를 추가한다(H-C05).
2. **공급자의 목적별 관계**: 2021-01-04T21:44:55Z [`562c37360f8133eda5870ab801d1a7710fe9abdc`](https://github.com/Homebrew/homebrew-core/commit/562c37360f8133eda5870ab801d1a7710fe9abdc)는 qt5→qt@5 관계를 같은 Qt 5 recipe에 연결한다(H-U19). 뒤 [`ab9d906d072fb2c5ba6ca30b23cb3136e42de6c1`](https://github.com/Homebrew/homebrew-core/commit/ab9d906d072fb2c5ba6ca30b23cb3136e42de6c1), committer 2021-03-02T15:55:25Z에서 기본 qt recipe는 Qt 6.0.1로 바뀐다(H-U20). 같은 Qt 5 목적에는 옛 계열 관계 보존이 의미가 있다.
3. **중간 수정 commit**: 2023-01-27T08:27:52Z [`7b53f648141dd9b604fc01a8603faa55021576e7`](https://github.com/qutebrowser/qutebrowser/commit/7b53f648141dd9b604fc01a8603faa55021576e7)가 `qt + 수동 bindings` 안내를 `pyqt@5`로 바꾼다(H-C06).
4. **후속 release 원문의 반례**: [v2.5.3 고정판 `2fe78b7644605c1e6622573935e7a2404922cbcd`](https://github.com/qutebrowser/qutebrowser/blob/2fe78b7644605c1e6622573935e7a2404922cbcd/doc/install.asciidoc)과 [v2.5.4 `c5919da4c410e706aacf348b76748a80a17b58ce`](https://github.com/qutebrowser/qutebrowser/blob/c5919da4c410e706aacf348b76748a80a17b58ce/doc/install.asciidoc)에는 여전히 qt와 수동 빌드 안내가 있다(H-F07,H-F12). [v3.0.0 `b11ead8f424e6bc901009a4b13dfcfd7516bae59`](https://github.com/qutebrowser/qutebrowser/blob/b11ead8f424e6bc901009a4b13dfcfd7516bae59/doc/install.asciidoc)는 이미 pyqt@6다(H-F08). [2023-08-18T10:29:03Z 수정 `adc2e1af7bef3af8ad55e5e41dc6489d284571a8`](https://github.com/qutebrowser/qutebrowser/commit/adc2e1af7bef3af8ad55e5e41dc6489d284571a8)가 이 마지막 변경을 보여 준다(H-C07).

**끊긴 곳.** pyqt@5 수정 자체가 처음 배포된 docs/nightly/release artifact가 미확인이다. 다음 release의 날짜나 v3.0.0의 다른 pyqt@6 내용을 중간 수정의 Tr로 채울 수 없다. 실제 설치 실패·해결 효과도 이 사슬에서 확정하지 않았다.

**다음 불변판.** 7b53f648 head를 실제로 배포한 docs/nightly artifact와 배포 로그, 당시 Qt/PyQt/PyQtWebEngine의 정확한 조합이 필요하다. 같은 이름을 계속 썼는지보다 같은 API 세대와 binding 목적이 유지됐는지를 먼저 확인한다.

## 4. A-C04 · NumPy 제안일과 문서 빌드에 도달한 공급 후보는 다르다

**원래 문서 목적.** Pandas `35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276`, 2019-12-31T21:05:41Z의 [environment.yml](https://github.com/pandas-dev/pandas/blob/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/environment.yml)은 NumPy >=1.15와 Python 3.7을 명시한다(C-S04). 같은 판 [CI L99–121](https://github.com/pandas-dev/pandas/blob/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/.github/workflows/ci.yml#L99-L121)와 [setup_env.sh L94–104](https://github.com/pandas-dev/pandas/blob/35ba6b0dc0d49dbe5abe44eee62ea6276a1f7276/ci/setup_env.sh#L94-L104)는 이 파일로 환경을 만들고 Ubuntu에서 warnings-as-errors 문서를 빌드하는 연결을 보여 준다(C-F53). 이는 봉인 뒤 같은 과거판에서 보강한 Q2 근거다.

- **상류 source·제안**: [`daf397a4a759356a94ff5945f1b84119993f88b8`](https://github.com/conda-forge/numpy-feedstock/commit/daf397a4a759356a94ff5945f1b84119993f88b8)의 source 시각은 2020-06-20T23:25:06Z다(C-F33). [PR 195](https://api.github.com/repos/conda-forge/numpy-feedstock/pulls/195)는 같은 날 23:26:08Z 제안됐지만 2020-07-16T17:13:54Z에 merge됐다(C-F34).
- **공급 후보의 업로드**: [NumPy 1.19.0 배포 원장](https://api.anaconda.org/release/conda-forge/numpy/1.19.0)의 선택 Linux CPython 3.6/3.7/3.8 파일은 2020-07-16T17:23:43.986Z–17:26:43.103Z로 기록된다(C-F50). 6월 제안일을 이 공급 후보의 배포 시각으로 대체하면 안 된다.
- **당사자의 실패 보고**: 2020-07-16T21:32:11Z [Pandas PR 35312](https://api.github.com/repos/pandas-dev/pandas/pulls/35312)는 NumPy 경고가 Matplotlib를 거쳐 master 문서 빌드를 실패시켰다고 설명하고, Matplotlib 3.3.0을 기다리는 임시 pin임을 밝힌다(C-F16). 연구자가 실행해 재현한 실패가 아니라 직접 당사자의 공개 보고다.
- **소비자 correction source**: 22:43:07Z [`cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda`](https://github.com/pandas-dev/pandas/commit/cd5e17c1a537a8ce8e786d308cebc64e1a2c6bda)는 같은 환경의 NumPy에 <1.19.0을 더한다(C-F15). v1.1.0rc0의 [`bfac13628394ac7317bb94833319bd6bf87603af`](https://github.com/pandas-dev/pandas/blob/bfac13628394ac7317bb94833319bd6bf87603af/environment.yml)에도 pin이 들어 있으며, 해당 source-release 후보의 공개 기록은 2020-07-17T19:50:14Z다(C-F18,C-F56).

**끊긴 곳.** [2020 수정 직전 parent `5e45f4f6dd253fa585076ea3149ef4e07fed5d0f`](https://github.com/pandas-dev/pandas/blob/5e45f4f6dd253fa585076ea3149ef4e07fed5d0f/environment.yml)의 Python 조건은 `python=3`이다(C-F54). 2019의 3.7 조건으로 2020 실패 artifact를 py37로 확정할 수 없다. 실제 conda explicit list와 CI 로그가 없으므로 Tu→Tc를 확정 지연으로 계산하지 않는다. 공개 source에 pin이 실렸다는 사실도 첫 성공 CI나 dev-docs 서버 배포를 뜻하지 않는다. 이 사례의 판정 범위는 **보고된 특정 문서 빌드 실패**이며 모든 NumPy 용도나 실제 오추천 피해로 확대하지 않는다.

**다음 불변판.** 2020-07-16 web_and_docs job의 conda explicit list, 실패·첫 성공 로그, 그 head의 dev-docs 게시 receipt가 필요하다. 원장의 조건부 artifact 산술과 실제 노출 지연은 계속 분리한다.

## 5. A-C06 · Spyder의 기존 실패는 upstream 수정 전에 보고됐다

**옛 참조와 목적.** Spyder `569b4cf8d93969163412cfc2b3f36b02bfaff0d5`, 2021-12-31T00:39:16Z의 [requirements/conda.txt](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/requirements/conda.txt)는 applaunchservices >=0.1.7을 허용한다(C-S06). [같은 판 qthelpers.py](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/spyder/utils/qthelpers.py)는 macOS 파일 열기 등록 목적을 연결한다(C-F32; 봉인 뒤 Q2 보강).

1. **상류 수정 전 직접 보고**: 2022-04-29T01:24:04Z [issue 1](https://api.github.com/repos/impact27/applaunchservices/issues/1)은 Python 3.10 conda 환경의 editable Spyder가 pyobjc 의존성 오류로 시작하지 못한다고 보고한다(C-F28). 이는 나중 0.3.0 배포가 새로 일으킨 실패라는 순서가 아니다.
2. **공급자 metadata 수정**: 2022-05-20T14:32:15Z [`2fe4aca7b4ecf33b233425d7606ca842f092b517`](https://github.com/conda-forge/applaunchservices-feedstock/commit/2fe4aca7b4ecf33b233425d7606ca842f092b517)는 0.3.0의 Pyobjc 의존성을 고친다(C-F38). 뒤 [`39fb2d76a908d840161db78bd8c86e97d77a0530`](https://github.com/conda-forge/applaunchservices-feedstock/commit/39fb2d76a908d840161db78bd8c86e97d77a0530)는 noarch로 돌아가도 `__osx` 조건을 명시한다(C-F40). noarch라는 표기만으로 모든 OS용이라고 판단할 수 없다.
3. **공급 후보 업로드**: [0.3.0 원장](https://api.anaconda.org/release/conda-forge/applaunchservices/0.3.0)은 2022-05-24~05-29의 OS/Python/build별 rollout을 기록한다(C-F52). 보고된 실패 환경의 정확한 architecture/build는 미확인이다.
4. **소비자 하한 변경**: 2022-07-03T19:56:02Z [`c1853843ace0f7b9347d74b9c8636f48d12c2537`](https://github.com/spyder-ide/spyder/commit/c1853843ace0f7b9347d74b9c8636f48d12c2537)는 macos.yml·setup.py·dependency 선언의 하한을 0.3.0으로 올린다(C-F25). [PR 18530](https://api.github.com/repos/spyder-ide/spyder/pulls/18530)의 merge는 2022-07-04T18:52:59Z로 별개다(C-F26). v5.3.2 [고정 source `1172bb4678970250c8e8f46a70a151c00d32d69f`](https://github.com/spyder-ide/spyder/blob/1172bb4678970250c8e8f46a70a151c00d32d69f/requirements/macos.yml)에 새 하한이 있고, source-release 공개 기록은 2022-07-13T19:55:59Z다(C-F29,C-F57).

**끊긴 곳.** 옛 >=0.1.7도 0.3.0을 허용한다. 하한 변경은 0.3.0 미만을 배제하지만 모든 사용자의 최초 정상화 날짜나 실제 설치된 metadata를 보장하지 않는다. 실제 GUI installer·conda package의 첫 수정 배포와 첫 정상 실행은 미확인이다. 직접 launch 실패 보고, 별도 plugin 검사 보고, macOS 파일 등록 목적의 source 호출은 각각 범위를 유지한다. 겹치는 유지관리자 계보를 독립 소비자의 반복 검증으로 세지 않는다.

**다음 불변판.** 실패한 Python 3.10 환경의 CPU·conda explicit list, 정확한 0.3.0 build를 사용한 첫 성공 로그, 새 하한을 포함하고 실제로 사용한 Spyder 5.3.2 배포 artifact가 필요하다.

## 6. B-C02 · mamba 분리 뒤에도 CLI 소비자는 옛 이름을 쓴다

이 사례는 사전 지정 공식 원장으로 시작한 **보조 B 시도**다. 발견한 유지나 API 차이를 A의 정정률에 더하지 않는다.

**상류 전후.** [이전 recipe `f6f010fa71fa2a2f93d486cc76897c08e38cab93`](https://github.com/conda-forge/mamba-feedstock/blob/f6f010fa71fa2a2f93d486cc76897c08e38cab93/recipe/meta.yaml)에서 [분리 뒤 `364da0d5190fa659c927183e938a7264a71fba95`](https://github.com/conda-forge/mamba-feedstock/commit/364da0d5190fa659c927183e938a7264a71fba95)로 바뀌면서 libmamba/libmambapy 출력이 나뉘지만 mamba CLI entry point는 남는다(BC-S10). [PR 134](https://github.com/conda-forge/mamba-feedstock/pull/134)는 2021-11-06T09:29:28Z 제안, 11-18T16:11:50Z merge다. 선택한 [Linux CPython 3.8 mamba 0.18.0 아카이브](https://conda.anaconda.org/conda-forge/linux-64/mamba-0.18.0-py38h1abaa86_0.tar.bz2)의 업로드 기록은 11-18T16:30:03.576Z이고, 실제 파일 목록에 bin/mamba가 있다(BC-S11). 이 시각을 모든 플랫폼 최초 공급으로 합치지 않는다.

**CLI 소비자의 유지.** Snakemake의 2021-11-17T14:05:26Z [`d0a7bf243c5df204136fa1f14706aab793793c68` 설치 문서](https://github.com/snakemake/snakemake/blob/d0a7bf243c5df204136fa1f14706aab793793c68/docs/getting_started/installation.rst)는 conda-forge mamba를 설치하고 CLI로 환경을 만든다(BC-S12). [첫 후속 source `cd968cd03437ad6db1d791f5d7ae5295b9754137`](https://github.com/snakemake/snakemake/blob/cd968cd03437ad6db1d791f5d7ae5295b9754137/docs/getting_started/installation.rst)에도 이 목적이 남고(BC-S13), 창 말에 해당하는 v7.18.2 [source `a5c3523992656ec8230d59ee12f9652313c6dd96`](https://github.com/snakemake/snakemake/blob/a5c3523992656ec8230d59ee12f9652313c6dd96/docs/getting_started/installation.rst)와 [2022-11-10T19:37:07Z release 기록](https://github.com/snakemake/snakemake/releases/tag/v7.18.2)도 같은 CLI 지시를 보존한다(BC-S14).

**반대 역할.** conda-libmamba-solver의 [`f93d38a190d912902ec90729304ea2936dd0976b` solver.py](https://github.com/conda/conda-libmamba-solver/blob/f93d38a190d912902ec90729304ea2936dd0976b/conda_libmamba_solver/solver.py)는 libmambapy를 import하며 mamba 자체를 import하지 않도록 설명한다(BC-S16). 이 API 역할에 맞는 후계명을 Snakemake의 CLI 참조에도 일괄 대입하면 필요한 실행파일과 다른 답이 된다.

**끊긴 곳.** source와 archive의 인터페이스 대응은 확인됐지만 Snakemake의 실제 solver 선택·환경 생성 성공은 미확인이다. API 소비자는 처음 확보한 코드부터 libmambapy를 사용하므로, 앞선 mamba 참조나 전환 자체를 가정할 수 없다. 이를 통계적 좌측 검열 정정으로 세지 않는다.

**다음 불변판.** Snakemake v7.18.2의 lock/CI 환경 영수증, 그리고 f93d38a190 이전 conda/conda의 poc-libsolv 코드에서 마지막 이전 참조와 첫 후계 import를 찾아야 한다.

## 7. B-C03 · Qt 구성요소로 우회했다가 qt로 돌아온다

**처음 고정한 목적 R1.** QtPy `b784f035bb9aad24f37614327d9f2c0d44166c19`, 2022-05-31T16:49:07Z의 [test.sh](https://github.com/spyder-ide/qtpy/blob/b784f035bb9aad24f37614327d9f2c0d44166c19/.github/workflows/test.sh)는 기본 Qt 5.12를 포함한 compatibility matrix를 시험한다(BC-S20). 이후 Python 3.11/Qt 5.15 행의 실패를 이 옛 5.12 용도가 잘못됐다는 증거로 옮기지 않는다.

공급자 [`d4afcdfece6e225bf7e316dc66e0936f50d2d8c0`](https://github.com/conda-forge/qt-feedstock/commit/d4afcdfece6e225bf7e316dc66e0936f50d2d8c0)는 qt를 qt-main과 qt-webengine에 의존하는 메타패키지로 바꾼다(BC-S17). [2022-04-23 공지](https://conda-forge.org/news/2022/04/23/packages-for-qtpyqt-5152-are-now-available/)의 구성요소 공개와, 선택 Linux qt wrapper의 2022-06-02T18:41:45.800Z [업로드 기록](https://api.anaconda.org/release/conda-forge/qt/5.15.2)은 다르다(BC-S18–19).

**나중의 다른 목적 R2.** 같은 B 원장 안의 보조 참조는 Python 3.11/PyQt 5.15 조건이다.

1. **직접 실패·우회 보고**: [2022-12-17T08:48:05Z 댓글](https://github.com/spyder-ide/qtpy/pull/392#issuecomment-1356123618)은 해당 조합의 의존성 충돌과 구성요소별 고정 설치가 해결된다는 당사자의 보고다(BC-S22). [`3cb24d0de241613615b9aa90dcdb25a8d7b19e3a`](https://github.com/spyder-ide/qtpy/commit/3cb24d0de241613615b9aa90dcdb25a8d7b19e3a), 10:02:30Z에 우회 source를 쓰고, 12-19T18:02:37Z [`7bd9ea7f70cb947f2d45d4398acf6245d57b14a0`](https://github.com/spyder-ide/qtpy/blob/7bd9ea7f70cb947f2d45d4398acf6245d57b14a0/.github/workflows/test.sh)에 merge됐다(BC-S21).
2. **같은 보조 목적에 대한 상류 수리**: [`275058548203f5d3bdb563930d6ad8bee7c475e0`](https://github.com/conda-forge/qt-feedstock/commit/275058548203f5d3bdb563930d6ad8bee7c475e0)는 qt 5.15.6 wrapper의 WebEngine 판 제약을 완화한다(BC-S24). 선택 Linux 수정 artifact의 [업로드 기록](https://api.anaconda.org/release/conda-forge/qt/5.15.6)은 2023-01-12T15:27:37.161Z다(BC-S25).
3. **후계를 알고 옛 이름으로 복귀**: [`0c8108b09af3e45d2e939f00c612e56eed6ba6e5`](https://github.com/spyder-ide/qtpy/commit/0c8108b09af3e45d2e939f00c612e56eed6ba6e5), 2023-01-12T20:55:58Z는 구성요소 우회를 없애고 qt로 돌아온다. [PR 397](https://github.com/spyder-ide/qtpy/pull/397)은 상류 문제가 해결됐음을 이유로 든다(BC-S26). 원장에 있는 19,700.839초 간격은 이 **보조 R2의 선택 Linux 업로드→소비자 source 수정**에만 적용한다. 실제 CI 정상화나 전체 전파율이 아니다.
4. **source release의 최종 상태**: [v2.3.1](https://github.com/spyder-ide/qtpy/releases/tag/v2.3.1), 2023-03-28T23:06:05Z의 [고정판 `f809bbe44321968bb4319605ed2aac7a27af2947`](https://github.com/spyder-ide/qtpy/blob/f809bbe44321968bb4319605ed2aac7a27af2947/.github/workflows/test.sh)에는 이미 복귀한 qt가 있다(BC-S27). 우회 commit이 ancestry에 있다는 사실만으로 중간 우회 지시가 별도 release에 실렸다고 하지 않는다.

**끊긴 곳.** 원래 R1의 같은 목적에서 부적합이 생겼다는 증거는 미확인이다. R2의 실제 CI run/job은 조회 실패이고, 현재 retained run 0을 당시 실행 0으로 해석하지 않는다(BC-S30). 당사자의 solver 보고를 연구자의 새 재현 실행이나 실제 사용자 오추천 피해로 바꾸지 않는다. 이 보조 사슬을 A의 분모에도 더하지 않는다.

**다음 불변판.** [run 3718737526/job 6307127310](https://github.com/spyder-ide/qtpy/actions/runs/3718737526/jobs/6307127310)의 보존 로그와 우회/복귀 head의 첫 성공 CI, 당시 OS·Python·Qt pin에 맞는 2022–2023 불변 repodata가 필요하다. 현재 채널로 다시 실행하는 것은 당시 조건의 검사가 아니다.

## 8. X-LIB01 · 역사적 전체 영역의 옛 ID를 보존하는 편이 정확하다

이 사례는 소프트웨어 A/B와 별개의 Q7 대조다. Git repository 판이 아니므로 Git SHA를 붙이지 않고, 아래 record 식별자·고정 dump 위치·실제 record SHA256을 보존한다.

**상류가 정한 범위.** [LC Cataloging Service Bulletin 60, Spring 1993](https://www.loc.gov/aba/publications/FreeCSB/CSB_060.pdf)의 인쇄 pp.2–4는 Czech Republic `n90718759`와 Slovakia `n50075233`의 적용, 옛 전체 국가에 Czechoslovakia와 `e-cs`를 계속 쓸 조건을 구별한다(X-S04). 국가 분리 기준일은 1993-01-01, 새 지리 코드 시행일은 1993-05-24다. 이 코드 시행일을 모든 주제 표목의 정확한 시행일로 쓰지 않는다.

**실제 소비자 고정판.** [Harvard MARC record](https://openlibrary.org/show-records/harvard_bibliographic_metadata/20220215_017.bib.mrc:295257330:2338)는 `20220215_017.bib.mrc`의 offset 295257330, length 2338, 001=`990068819680203941`로 특정된다(X-S05). 1968년 책 *The agony of Czechoslovakia ’38/’68*의 제목·목차는 과거 사건을 다룬다. 043의 `e-cs---`, 651의 역사 주제 URI `http://id.loc.gov/authorities/subjects/sh85035319`, 852/876의 WID·Slav7340.95 소장 정보가 함께 있다. 현재 국가 안내가 아니라 과거 역사 주제의 소장 자료를 찾는 목적이다.

e-cs/e-xr/e-xo는 **지리 코드**, n90718759/n50075233은 **국가명 전거**, 소비자에 나타난 sh85035319는 **역사 주제 전거**다. 서로 다른 역할의 식별자이므로 sh85035319가 두 n 식별자로 직접 분리됐다고 기록하지 않는다. 이 sh URI가 1993년 이전부터 존재했는지도 미확인이다. 확인된 보존 판단은 역사 범위에 맞는 옛 표목과 e-cs에 관한 것이다.

**이번 원 바이트 확인.** [원 dump](https://archive.org/download/harvard_bibliographic_metadata/20220215_017.bib.mrc)에서 해당 2338바이트 구간을 HTTP 206으로 확보한 기록이 있다(X-S12). record SHA256은 `6ce2142a32f7fe98f815cc62de767efdf6312571da20814c65a1fb6170d5e4e6`다. 전체 dump의 manifest 해시를 읽은 것과 전체 파일을 내려받아 재계산한 것은 구별한다. 렌더링·mirror·원 record는 소비자 세 곳이 아니다.

**왜 단일 후계로 바꾸지 않는가.** 현재 체코 한 나라로 일괄 치환하면 이 책이 다루는 과거 전체 영역과 주제 범위를 좁힐 수 있다. 다만 모든 역사 자료에 옛 이름을 고정한다는 일반 규칙도 아니다. 같은 당대 결정은 descriptive 접근점, subject 표목, 지리 세목의 역할을 나눈다. [후속 H710 §3.a·§4](https://www.loc.gov/aba/publications/FreeSHM/H0710.pdf)는 그 역할 구별을 보강하지만, Harvard가 언제 이 규칙을 적용했는지를 증명하지는 않는다(X-S07).

**끊긴 곳.** MARC005=`20020606163548.3`, 파일명의 20220215, mirror mtime 2026-03-12T03:48:10Z는 서로 다른 시계다. 어느 값도 이 record의 651이 처음 수정된 날짜나 Harvard의 명시적 보존 결정일이 아니다. 옛 표목이 자료의 범위에 맞는다는 판정은 가능하지만, 소비자 정정 전파 지연과 실제 피해는 미확인이다.

**다음 불변판.** Harvard 2022 export의 원 발행 receipt와 **같은 001**의 이전 snapshot이 필요하다. 651·852와 변경 provenance를 비교하기 전에는 다른 책의 record, MARC005, 현재 화면으로 전후 수정 사슬을 채우지 않는다.

