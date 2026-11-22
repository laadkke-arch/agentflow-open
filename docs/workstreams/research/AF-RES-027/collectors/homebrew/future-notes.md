# Homebrew A · 봉인 뒤 추적 결과

## 실행·분모·완료 범위

A 봉인 `1714a55a529c7da42596ac0779d398f3aacf97c3` 원격 확인 뒤, 2026-11-22T05:06:15Z부터 상류/후속 이력을 열었다. 수집 마감은 2026-11-22T05:34 UTC다. frozen `historical.json`, `frame.json`, `sources.json`, `search-log.jsonl`의 SHA256 네 개는 `future-self-check.json`에서 모두 일치했다. 수집자 자신은 git commit/push를 하지 않았다.

Homebrew A는 6참조/6소비자 프로젝트다. 확인된 상류 관계 사건 4개(규칙 기능 제거, pkg-config 구현 교체, SDL2 호환 구현 교체, Qt5 alias 정리), 관련 사건 미관측 2행(Ninja/CMake)이다. 이는 완전 독립 작성자 6명이나 대표 표본의 변경률이 아니다. Homebrew라는 공통 발급자와 반복된 상류 작성자가 있다. 개별 공개 commit 작성자 비교는 `author-lineages.json`과 `verdicts.json`에 있다. 비교한 각 쌍은 다른 공개 로그인이나 전체 작성 이력의 완전 독립은 단정하지 않는다.

`future-sources.json`은 101행이며 자료/lookup/현재 API 관측을 구분한다. 보수적으로 최소수에 산입하는 후속 원문은 상류 8개, 소비자 후속 6개다. 봉인된 과거 소비자 6개까지 이 수집자의 최소 원문 기여는 20개다. 같은 commit의 여러 파일, release tag/메타데이터/아카이브, 동일 PR의 source/bottle/merge 기록은 중복 편집 계보로 묶었다. A-H02/B-H01, A-H06/B-H03의 공통 상류 사건도 전체 집계에서 중복 제외해야 한다. 현재 API나 공개 path history 조회를 원문 최소수에 더하지 않았다.

## 여섯 참조에서 실제 확인한 결과

| A행 | 확인된 사슬/반례 | 엄격한 판정·범위 | 마지막 고정판/핵심 근거 |
| --- | --- | --- | --- |
| H01 fish/cppcheck | 2019 `lint.fish`는 `--rule-file=.cppcheck.rules`; Homebrew는 2026 규칙 엔진 OFF. fish는 2024 Rust 전환 때 이미 C++/cppcheck 목적 제거 | 옛 호출과 현재 recipe의 정적 불일치는 확인. 고정 2019문서가 원래 틀렸거나 실제 사람이 실패했다는 뜻은 아니다. 현재 소비자의 수정 필요는 보류 | H-F02(봉인 뒤 동일 과거 SHA 추가 판독), H-U15/H-U22/H-U23, H-U18, H-C02 |
| H02 kitty/pkg-config | 다른 구현 pkgconf가 같은 CLI alias 제공. 2024-11-23 Brewfile 직접줄 삭제 뒤 0.38.0 실제 source archive에도 반영. setup.py는 계속 pkg-config 호출 | source 수정·동일 공개 archive 내용은 확인, CI 효과/실제 피해 미확인. source asset upload metadata와 최초 실제 공개 시각을 구별 | H-C01, H-F05/H-F11, H-R01/H-R02 및 release-archive-receipt.json |
| H03 Neovim/ninja | 2023→2026 fixed BUILD.md에서 Ninja 설치/빠른 CMake 빌드 역할 유지. 새 Zig 절도 공존 | 관련 identity/출력 분리 사건 미관측. 모든 Ninja 버전의 실제 빌드 성공을 보장하지 않는다 | H-U03/H-U09, H-F03 `bd5435324628c22d9b5e32597613e086c08afe6f` |
| H04 OBS/cmake | Brewfile이 두 번 이동. 이전 경로 삭제 뒤에도 같은판 새 .Brewfile과 cmake 호출 유지 | 관측 source 범위 2023-07-17까지 역할 유지. 2026 CMake4.x와 2021판의 모든 하위 빌드 호환은 미검증 | H-F04, H-C09, H-F10/H-F13 `099314795458ad249d3c7d7c6d6972ef5af4df07` |
| H05 scrcpy/sdl2 | 2026-01 source API migration 및 2026-05 v4.0 배포가 Homebrew의 2026-06 sdl2→sdl2-compat보다 앞선다 | 하류의 SDL3 목적 변화. 같은 상류 정정이 먼저 전파된 음수 지연으로 계산하면 틀린다. 옛 SDL2 API의 호환층 실행 성공은 미확인 | H-C04, H-F09/H-R03; H-U16/H-U17/H-U24 |
| H06 qutebrowser/qt5 | qt5→qt@5 alias는 같은 Qt5 recipe 보존. 소비자는 2020 qt로 바꾸고 2023 main에서 pyqt@5, 나중 pyqt@6로 이동 | 2023-01 pyqt@5 정정은 뒤 v2.5.3/v2.5.4 source에 없고 v3.0.0에는 다른 pyqt@6. 같은 수정의 배포 시각 미확인 | H-U19/H-U20, H-C05/H-C06, H-F07/H-F12/H-F08 |

H01의 `--rule-file` 호출은 **봉인 뒤 같은 과거 SHA를 추가로 읽어 Q2를 보강한 세부**다. 최초 봉인의 cppcheck.sh 호출 기록을 소급해서 바꾸지 않았다. 문서가 `.cppcheck.rule`이라고 쓴 부분과 실제 `.cppcheck.rules` 파일명을 구별한다. H01의 현재 Cppcheck parser는 HAVE_RULES가 없으면 해당 옵션을 Fail로 처리함을 H-U18 L1338–1441에서 확인했다. 설치나 동작 실험을 수행한 것은 아니다.

사전 enum에 없는 기능 삭제/다른 구현 교체는 `relation=UNRESOLVED`, `relation_detail=FEATURE_REMOVAL` 또는 `IMPLEMENTATION_REPLACEMENT...`로 보존했다. 여기서 UNRESOLVED는 diff가 불명이라는 뜻이 아니라 사전 관계 어휘에 맞는 코드가 없다는 뜻이며, 별도 `event_observed=true`와 `relation_uncertainty`로 구별한다.

## 날짜·배포·검열

네 사건 모두 `Tu`(실제 사용자에게 처음 시행된 시각)는 미확인이다. 제안/source commit/merge/bottle metadata/current API 조회를 각각 저장했고 그 중 하나를 Tu로 치환하지 않았다. 따라서 네 행의 정식 365일 창 시작/끝과 좌·우 검열은 확정하지 않았다. 사건 미관측 두 행은 Tu/수정 지연이 **해당 없음**이다. 시작일 미확인을 우측 검열로 세지 않는다. 현재 source 조회를 사건 뒤 365일 창말 원문이라고 부르지 않는다. 정확한 5시점 완전 사슬은 이 수집 범위에서 0개다.

H02는 source commit `2024-11-23T14:18:05Z`, release page published `2024-12-16T01:40:10Z`, source asset created `01:41:05Z`, updated `01:41:07Z`, state=uploaded를 각각 읽었다. release page는 해당 source asset metadata보다 55–57초 앞서므로 page 게시 시각을 Brewfile archive 배포시각으로 쓸 수 없다. 2026-11-22 직접 HTTP200으로 받은 8,927,688-byte archive의 SHA256은 `96fe79a645ec57a378295cdf16204265768091338d77efb058977b60209bb8ff`; `kitty-0.38.0/Brewfile` 멤버에 pkg-config 줄이 없음을 확인했다. 아카이브 코드는 실행하지 않았다.

Tc→asset created/updated **메타데이터 차이**는 22.4743055556–22.4743287037일(22일 11시간 23분 00–02초)이다. 별도 내부 판독과 root의 GitHub 공식 문서 재열람 후, 이 값을 최초 실제 공개 접근 가능 시각의 구간으로 수용하지 않았다. updated_at은 최초 upload 완료 시각으로 보장되지 않으므로 `eligible_for_same_reference_source_release_delay=false`로 수정했다. `chains.json`은 endpoint를 source asset upload metadata라고 표시하며, 실제 사용자 다운로드/CI 개선/피해 정정 시간으로 일반화하지 않는다. 확정된 Tu→Tc 시간쌍은 없다. H05의 선행 source/release 날짜 차이를 상류 정정 전파 시간으로 계산하지 않았다.

## 반증·무결과·재열람 비용

첫 인상은 안정적인 패키지 이름이면 기능이 유지될 것이라는 것이었다. H01의 user-rule 기능 제거와 H05의 다른 구현 교체가 이를 깨뜨렸다. 반대로 옛 경로 삭제를 정정으로 보는 해석은 H04의 이동된 Brewfile 때문에 틀렸고, 최신 successor를 무조건 고르는 해석은 H06의 Qt5 목적 보존과 bindings 구분 때문에 틀렸다. H03의 새 Zig 절은 기존 Ninja 폐기가 아니었다. H02의 CI fix 제목 후보 `8183e9d3...`은 실제로 simde 추가뿐이어서 탈락시켰고, H06의 `9308d124...`는 cask 문법만 고쳐 탈락시켰다.

H02의 수정 SHA Actions 공개조회는 retained run 0이었다. 당시 CI가 없었거나 성공했다는 뜻이 아니며 실행 효과 확인은 실패했다. Homebrew의 pkg-config/sdl2/qt5 JSON API 주소 조회는 404였으나 소비자가 붙인 것은 URL이 아니라 brew 이름이다. alias와 현재 recipe를 별도 확인하므로 API404를 설치 실패로 바꾸지 않는다. 재현 가능한 lookup 목록과 실패/제외 이유는 `future-search-log.jsonl`에 있다.

`read-metrics.json`의 사례별 직접 원문 조회 URL/서로 다른 repository 판 수는 H01 12/10, H02 11/6, H03 5/4, H04 8/5, H05 12/10, H06 13/11이다. 같은 commit의 여러 파일은 URL 수에서 각각, 판 수에서 하나로 센다. 이는 출처 원장의 재열람 경로 수이며 실제 UI 클릭 수나 사람의 해석시간 측정이 아니다. API 탐색/실패를 포함한 URL 수도 별도 열에 있다. 기록 비용·전파율·사람 시간은 추정하지 않았다. 같은 자료를 본 연구자의 필드 가림 비교이며 독립 맹검 성능 실험도 아니다.

## 재개할 최소 입력

1. **H02의 의미와 실제 배포 시각**: e625f0aa 및 parent의 당시 macOS CI 로그, pkgconf 버전/환경, source asset213583777의 최초 공개 접근 가능 시각을 확인할 기록. 업로드 metadata의 해석을 독립 판독하고, source 내용 확인과 기능 효과를 분리한다.
2. **H01/H05의 옛판 실제 재현**: 고정 fish2019+정확한 Cppcheck bottle에서 --rule-file 실행 로그, 고정 scrcpy2019+정확한 SDL2-compat bottle의 빌드/렌더링 로그. 현재 upstream의 호환/불호환 의도를 실제 사람 피해로 바꾸지 않는다.
3. **H06의 사라진 배포 연결**: 7b53f648의 docs/nightly 배포 artifact·로그, qutebrowser2.5 계열의 실제 PyQtWebEngine 설치 보고와 Qt@5 WebEngine 제외 최초 diff. v3.0.0 pyqt@6를 pyqt@5 수정의 배포로 대체하지 않는다.

## 실행을 다른 환경에서 해야 할 때

이 조사에서는 brew 설치/패키지 빌드를 실행하지 않았다. 필요한 최소 실행은 아래처럼 고정 환경과 입력을 먼저 지정해야 한다. 이는 현행 도구를 옛 소스에 섞어 테스트했다는 보고가 아니다.

- H01: fish `efa9d5dd6a1a4f90e5a6d9372cddf539634be27e`, 비교 대상 Homebrew recipe `00c8278face7ab08d37330a3c0a7a6877d3b8acb`(1.90)와 rules-OFF bottle의 정확한 SHA/OS를 고정. 그 환경에서 `cppcheck --version`, `cppcheck --rule-file=.cppcheck.rules --enable=warning,performance,portability,information --std=c++11 --std=posix --language=c++ src/*.cpp`의 stdout/stderr/exit code를 저장. 전체 `build_tools/lint.fish`의 같은 flag·include 조건도 함께 기록한다.
- H05: scrcpy `83d48267a734e999fac0eccd93173b93019bf006`, SDL2 원본/SDL2-compat의 정확한 bottle 및 당시 FFmpeg/Meson/Ninja 환경을 각각 고정. 그 판 BUILD.md의 client build 명령과 `pkg-config --modversion sdl2`, `sdl2-config --version`, 실제 렌더링 smoke-test를 같은 OS/device 입력으로 저장한다. 새 SDL3 API용 v4.0을 옛 SDL2 의도와 섞지 않는다.
- H02: `https://api.github.com/repos/kovidgoyal/kitty/actions/runs?head_sha=e625f0aa024d7277287edac0c5c04c0239c5da0e&per_page=100` 재조회 및 당시 유지관리자가 보존한 CI 링크를 찾는다. 현재 run 0 결과를 역사 실행 0으로 바꾸지 않는다.

공통 진행표/색인에는 위 여섯 A행과 중복 B 연결, Tu 미확인 네 행, 무사건 두 행, source archive 내용 확인 사례 하나를 제안한다. 공통 파일은 수집자가 수정하지 않았다.
