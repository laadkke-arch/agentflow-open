# Cargo 후속 결정·역사 가용성 감사

## 상태와 고정 경계

요청된 **4개 결정 행과 원래 반환된 고유 후보 24개 행을 모두 작성했다.** 발견 단계와 가린 판정은 수정하지 않았다. 이 디렉터리는 primary seal `d1f506b1dde91e706360846f4c2eac5baabe492e`가 원격에서 확인된 **2026-11-22 05:50:22 UTC 이후**에 시작한 별도 조사다.

현재 원문에서 기능을 읽었다는 사실, 2021년에 제품이 있었다는 사실, 당시 그 사용에 필요한 기능 전체가 있었다는 사실은 분리했다. 역사 가용성은 **supported 1 / not_available 8 / unknown 15**다. supported는 GCC의 제한된 compiler filename mapping 사용 경계 1건이며, 원 반환 당시 부족했던 인용을 완전한 것으로 고치지 않는다. 이 분류는 검색 경로의 새 적중이나 독립 성능 지표가 아니다.

| 파일 | 기록 범위 |
| --- | --- |
| `decisions.jsonl` | Q05–Q08 각 1행. 상태, 선택 경계, 실제 후속 댓글, 고정 head, 변경 diff, 최초/후속 명시 구분 |
| `candidate-history.jsonl` | 원 반환 고유 후보 24개. 제품 존재와 필요한 기능의 역사, 실제 확인한 자료, 보류 사유와 다음 최소 확인 |
| `sources.json` | 계보별 원문 37행. 이 단계에서 새 고유 원문으로 표시한 18행 중 후속 결정 원장은 4행 |
| `receipts/` | 실제 요청 91건의 UTC, 입력, 받은 응답 해시, 실패, 개별 elapsed ms |
| `exploration.jsonl` | 원문 행에 묶이지 않은 검색/접근 실패/메타데이터 요청 22건. 최소 원문 수에서 제외 |
| `final-inputs/`, `diffs/` | 네 고정 최종 초안과 봉인된 최초 입력 대비 unified diff |
| `cost-summary.json`, `verify.py`, `verification.json` | 이 단계 비용 분리와 행·분모·참조·해시 검산 |

최종 초안은 rust-lang/rfcs의 공개 Apache-2.0/MIT 계보 원문이다. 원래 저작권·라이선스는 해당 저장소에 남아 있으며 출처와 full commit은 `sources.json`에 적었다. 댓글 전체나 검색 snippet을 재게시하지 않고 필요한 관측을 요약했다. 동일 초안의 다른 판과 동일 페이지의 재조회는 새 원문으로 추가하지 않았다. 다른 stream과의 마지막 계보 중복 제거는 root의 통합 단계가 맡는다.

## 결정과 조건 변화

| 질문 | 실제 결정 | 최초 입력 이후에 확인한 차이 | 주된 원문 |
| --- | --- | --- | --- |
| Q05 / RFC3074 | 2022-11-11 postpone, 병합되지 않음 | 문제의 가치는 인정하되 추진 필요가 달라졌고 추가 논의가 필요하다고 판단. symlink 이름은 최초판부터 있으며 후속은 Windows 사용 비용과 직접 복사 갱신 문제를 더 명시 | [보류 근거](https://github.com/rust-lang/rfcs/pull/3074#issuecomment-1298893844), [FCP 완료](https://github.com/rust-lang/rfcs/pull/3074#issuecomment-1312004870) |
| Q06 / RFC3127 | 2023-05-13 compiler/Cargo 수용 | private split-debug 정보 보존, remapping scope, build-script 전달이 추가됨. 모든 scope의 안정화를 약속한 것은 아님 | [초기 분리 요구](https://github.com/rust-lang/rfcs/pull/3127#issuecomment-850491441), [수용](https://github.com/rust-lang/rfcs/pull/3127#issuecomment-1546718539) |
| Q07 / RFC3139 | 2022-03-11 Cargo 수용 | 최초 HTTPS/localhost 필수 경계와 수용판이 다름. 2022-01-24 diff에서 HTTPS 전용 거부 문단이 삭제되고 index URL 조회 등이 추가됨 | [실제 변경](https://github.com/rust-lang/rfcs/commit/8a993d3d9f581d25fc94d3eb0fc246377edfbd1c), [수용](https://github.com/rust-lang/rfcs/pull/3139#issuecomment-1065671331) |
| Q08 / RFC3146 | 2022-10-10 작성자가 닫음 | compatible version requirement의 하한을 높이는 편집만으로 migration된 feature를 잃을 수 있다는 반례를 인정 | [반례](https://github.com/rust-lang/rfcs/pull/3146#issuecomment-1273473456), [인정](https://github.com/rust-lang/rfcs/pull/3146#issuecomment-1273520056), [닫음](https://github.com/rust-lang/rfcs/pull/3146#issuecomment-1273520941) |

Q07의 삭제는 **최종 설계 문서의 변화**다. 여기서 실제 Cargo 릴리스의 모든 HTTP 허용 동작을 증명한 것으로 넓히지 않았다. 최종 수용을 최초 질문의 정답으로 삼으면 요구가 바뀐 부분을 잘못 채점하게 된다.

Q08은 표집 때 허용된 공개 전 최초 실질 완성 초안 `40fda48412b511eee61644125cabfff993f7c39f`를 입력으로 썼다. 최종판과의 전체 diff에는 PR 공개 전 변화도 들어 있다. 예를 들어 `join -> meet`라는 commit subject는 2021-07-06이며 PR 생성은 2021-07-07이다. 이 변화를 공개 이후의 새 발견으로 세지 않았다.

## 후속에서 처음 명시된 것과 이미 명시된 것

Q06의 GCC, Clang, Reproducible Builds build-path 링크는 검사한 issue-comment 집합에서 **2021-06-27**에 처음 나타난다. [해당 댓글](https://github.com/rust-lang/rfcs/pull/3127#issuecomment-869199458)은 macro와 debug의 별도 prefix-map을 비교한다. [2021-08-31 commit](https://github.com/rust-lang/rfcs/commit/408dc507c55103a7174146df2d68ede5cb727888)이 이를 draft의 Prior art와 scope 설명에 반영한다. 문서 반영일과 토론에서 처음 명시된 날을 구별했다.

cc-rs라는 라이브러리를 build-script 전달 대상으로 언급한 것은 [2022-07-12 댓글](https://github.com/rust-lang/rfcs/pull/3127#issuecomment-1182020811)이다. 반환된 정확한 `cc::Build::remap_source_path` API는 [공급자 PR2071](https://github.com/rust-lang/cc-rs/pull/2071)이 **2026-10-30**에 추가한다. 라이브러리의 이름을 안다는 것과 후대의 구체 API가 존재한다는 것을 합치지 않았다.

Q07의 NPM과 GitHub Artifacts는 최초 원문에 있다. URI별 credential mapping이나 내부 redirect handler는 더 좁은 부품이다. 후속에 나오는 Swift라는 단어는 Biscuit 언어 구현을 가리키므로 SwiftPM registry authentication 후보의 명시로 세지 않았다. Q08의 `semver` crate1.0.3과 반환된 `semver.org` 표준도 별개 자료다.

검사한 범위에서 이름을 찾지 못했다는 것은 **해당 문서·댓글에 명시되지 않았다는 관측**이다. 작성자가 몰랐다고 판정하지 않는다.

## 당시 판과 현재 판의 차이

| 질문 | 후보 수 | 당시 전체 기능 supported | 후대의 정확한 반환 경로/원문 not_available | 전체 기능 unknown |
| --- | ---: | ---: | ---: | ---: |
| Q05 | 6 | 0 | 2 | 4 |
| Q06 | 6 | 1 | 1 | 4 |
| Q07 | 6 | 0 | 3 | 3 |
| Q08 | 6 | 0 | 2 | 4 |
| 합계 | 24 | 1 | 8 | 15 |

주요 시점 검증은 다음과 같다.

- Gradle3.1의 composite builds와 CLI include-build, Bazel3.7의 local_repository 및 override_repository, SCons4.0.1의 source repository는 2021년 전의 판으로 확인했다. 제품이 오래됐어도 named-base 오류 처리 등 전체 계약은 남는다.
- GCC10.3은 2021-04-08 출시됐다. 고정 source에서 map을 앞에 넣고 첫 일치를 택하는 순서, macro/debug별 map, builtin filename 분기를 읽었다. 이를 **자동 map 다음에 user map을 주는 조건**에서 사용할 수 있다. provider 테스트는 읽었으며 이 환경에서 실행하지 않았다.
- LLVM2019 지침에는 상대 입력 경로와 debug directory 제어뿐 아니라 split-DWARF와 기록된 명령의 한계도 있다.
- Zig의 공식 package manager 도입은0.11/2023, Bzlmod release는5.0/2022, Swift token registry authentication은5.8/2023이다. 이전 prototype이나 일반 build option 전체가 없었다는 주장은 하지 않는다.
- Shipyard의 modern 경로는 Rust1.74/2023 기능에 의존한다. 오래된 User-Agent 우회법의 2021 가용성과 같은 안전 경계는 미확인이다.
- npm-registry-fetch11.0.0의 URI lookup은 2021-06-02 tag와 root `auth.js`에서 확인했다. 2026 findings의20.0.1/make-fetch-happen16을 옛11/9계열에 소급하지 않았다.
- 다중 버전 TGG 논문은2024, OpenSSF 지침은2025다. trace-based 논문은2020, Go wrapper 문서는2020, SemVer 고정판은2019에 있었지만 Cargo feature-set 알고리즘을 모두 구현하지 않는다.
- IBM handbook은 실제 본문을 다시 열었지만 2021 이전 고정판이나 날짜를 확보하지 못했다.

`not_available`는 정확히 반환된 기능·릴리스·문서 경계의 후발을 뜻한다. 기반 원리나 동일 회사 전체의 부재가 아니다. `unknown` 행은 실제 탐색과 남은 기능을 적었으며, 검색 결과가 없다는 이유만으로 부재를 단정하지 않는다.

## 반례와 한계

SCons의 `Repository`는 존재하지 않는 디렉터리를 목록에서 조용히 제외한다. 기본 variable expansion도 없는 변수를 빈 문자열로 처리할 수 있다. 이는 unknown required base를 진단해야 하는 최초 Q05와 다른 계약이다. 2017 BUILD_PATH_PREFIX_MAP draft의 producer가 기존 사용자 map 뒤에 자동 map을 붙이면 오른쪽 우선 규칙 때문에 원래 원하는 사용자 우선이 뒤집힐 수 있다. draft라는 상태 자체를 거절 이유로 삼지는 않았다.

issue-comment corpus는 Q05 21개, Q06 74개, Q07 40개, Q08 14개로 **149개**다. 이 전체의 후보 별칭을 검색하고 결정·경계 관련 본문을 직접 읽었다. 모든 댓글을 동일 깊이로 정독했다고 주장하지 않는다. 별도 inline review **126개**는 읽지 않았다. 따라서 “검사한 후속에서 처음 명시”는 모든 커뮤니케이션에서 최초라는 뜻이 아니다. 각 final draft와 initial→final diff는 보존했지만 모든 중간판의 전문을 별도로 열지 않았다.

이 단계는 같은 모델의 후속 판독이며 새로운 독립 사람 검증이 아니다. 공급자 사실, 작성자/팀 결정, 연구자의 조건부 적용을 별도 필드에 두었다.

## 비용과 접근 실패

2026-11-22 **05:51:27.895–06:05:02.057 UTC** 사이의 실제 조회 영수증은91개다. 검색12개와 read/navigation/API79개를 분리했다. 이 중10개 요청이 실패했고, 추가로 시작 시 연결 인자가 빠진 connector schema 오류1건은 정확 시각/해시가 없어 별도 공개했다. 원문 읽기나 연구 시간으로 위 오류를 숨겨 합치지 않았다.

개별 tool elapsed 합은49,114ms다. 병렬 요청을 포함하므로 이 값은 총 작업 벽시간이나 인시가 아니다. 조회 창814.162초도 파일 정리·판독을 포함하는 전체 노동시간이 아니다. token 수와 실제 인시는 도구가 제공하지 않아 미확인이다. 원 검색 단계의 예산/비용과 합산하지 않았다.

접근 실패 대체는 다음과 같다.

- GitHub PR web open4건 실패 후 공식 repository API의 PR, comments, commits 및 고정 파일을 읽었다.
- GCC tag/10.3 웹 매뉴얼 일부 접근 실패 후 공식 gcc-mirror의10.3 코드·테스트와 release history를 읽었다.
- cc-rs commit-search endpoint가 connector에서 거절되어 공개 검색으로 supplier PR2071을 찾고 API 원문과 merge patch를 읽었다.
- SCons release API와 npm release API가 반환되지 않은 경우 tag object/commit과 고정 버전 원문으로 날짜·기능 일부를 대체했다.
- npm의 `lib/auth.js`는 옛판에 해당 경로로 없어서 실패했고, 동일 tag의 root `auth.js`를 읽었다.

## 재집계와 재개 명령

저장소 루트에서 다음을 실행하면 4개 질문, 24개 고유 반환 후보, 상태 분모, sources 참조, 영수증 및 공개 파일의 연결 ID 부재를 재검산한다.

```bash
python docs/workstreams/research/AF-RES-025/followups/cargo/verify.py
```

GitHub CLI가 연결된 환경에서 다음 read-only 입력으로 결정 corpus와 주요 diff를 다시 조회할 수 있다. 반환 JSON의 원문과 시각을 읽고, 기존 판정 파일을 덮어쓰지 않는 별도 감사 파일에 기록한다.

```bash
gh api 'repos/rust-lang/rfcs/issues/3127/comments?per_page=100&page=1'
gh api repos/rust-lang/rfcs/commits/408dc507c55103a7174146df2d68ede5cb727888
gh api repos/rust-lang/rfcs/commits/8a993d3d9f581d25fc94d3eb0fc246377edfbd1c
gh api repos/rust-lang/cc-rs/pulls/2071
gh api 'repos/npm/npm-registry-fetch/contents/auth.js?ref=v11.0.0'
```

GCC의 선택적 실행 검증에는 **GCC10.3.0**이 필요하다. `AF025_GCC103`을 해당 바이너리로 정한 뒤, 동일 임시 source root에 main.c와 header.h를 둔다. header는 `__FILE__`을 문자열 변수에 저장하고 main은 main/header의 `__FILE__` 및 동일 root를 포함한 하드코딩 문자열을 출력하게 한다. 다음 입력을 적용한다.

```bash
"$AF025_GCC103" --version
"$AF025_GCC103" -g -ffile-prefix-map="$AF025_SOURCE_ROOT"=/AUTO -ffile-prefix-map="$AF025_SOURCE_ROOT"=/USER "$AF025_SOURCE_ROOT/main.c" -o "$AF025_SOURCE_ROOT/out"
"$AF025_SOURCE_ROOT/out"
readelf --debug-dump=info "$AF025_SOURCE_ROOT/out"
readelf --debug-dump=decodedline "$AF025_SOURCE_ROOT/out"
```

예상 확인은 macro 경로의 `/USER/` 우선, 포함된 header의 동일 치환, 하드코딩 문자열의 원래 값 보존, DWARF source 경로의 해당 치환이다. 이 실행은 아직 수행하지 않았고 정적 코드 근거와 별도로 기록해야 한다. 재현 fixture의 원문/정확 compiler checksum까지 추가한 뒤 실행 증거를 갱신할 수 있다.

## 영향이 큰 약점과 다음 조사

1. **후속 요구의 변화**: Q07 HTTPS 문단 삭제 및 Q06 split-debug scope는 최초 요구와 최종 수용의 일치를 깨뜨린다. 다음 한 조사는 Cargo1.74 고정 구현의 transport/redirect tests를 최초 M1–M5와 최종 문서 양쪽으로 대조하는 것이다.
2. **과거의 전체 기능 가용성 15건 보류**: 오래된 제품의 일부 기능만으로 당시 적합성을 채울 수 없다. 다음 한 조사는 Bazel3.7 repository override tests에서 Q05-M4의 unknown-name 진단과 ordinary-path 보존을 확인하는 것이다.
3. **검사하지 않은 inline review126개와 중간판**: 최초 후속 명시 날짜는 제한된 corpus의 관측이다. 다음 한 조사는 RFC3127의101개 inline review를 시간순으로 읽고 GCC/Clang/guide의2021-06-27보다 이른 명시가 있는지 검사하는 것이다.
