| 소비자·호출 위치 | 원 입력·목적 | 부모판 동작 | 자식판 동작 | 근거 URL·절 | 미확인 |
|---|---|---|---|---|---|
| scikit-learn-extra C01 conftest.py:16–18 #141→#167 | numpy.__version__ <1.14, sklearn.__version__ <0.23.0; doctest gate | LooseVersion, 조건 만족 시 skip; ImportError catch | Version; 임계값/분기 동일, InvalidVersion은 해당 catch 밖; packaging 의존성 추가 | [#141](https://github.com/scikit-learn-contrib/scikit-learn-extra/pull/141), [부모](https://github.com/scikit-learn-contrib/scikit-learn-extra/blob/627f97b011cb267828e89cdf9257e35f59b328e7/conftest.py#L9-L38), [자식](https://github.com/scikit-learn-contrib/scikit-learn-extra/blob/0f95d8dda4c69f9de4fb002366041adcb1302f3b/conftest.py#L9-L38), S07/S08/S22/S23 | 실제 설치값과 후속 tag |
| scikit-learn-extra C02/C03 _commonnn.py:18–24,320–336 | sklearn 최소판; import, validation, sample-weight API | LooseVersion, old API vs new API | Version; API 분기 동일, 허용 문자열 및 순서 다름 | [#167 diff](https://github.com/scikit-learn-contrib/scikit-learn-extra/pull/167/files), [v0.3.0 old](https://github.com/scikit-learn-contrib/scikit-learn-extra/blob/v0.3.0/sklearn_extra/cluster/_commonnn.py), [merge file](https://github.com/scikit-learn-contrib/scikit-learn-extra/blob/0f95d8dda4c69f9de4fb002366041adcb1302f3b/sklearn_extra/cluster/_commonnn.py), S08/S24/S25 | v0.3.0은 변경 전; first tag 미확인 |
| Yellowbrick C04/C05 colors/rcmod #1323 | mpl.__version__ >=1.5.0; cycle/palette API gate | LooseVersion; 문자열 RHS 지원 | 제안은 parse, 선행 별도 #1319 패치는 Version 양쪽; 실제 병합 아님 | [#1323](https://github.com/DistrictDataLabs/yellowbrick/issues/1323), [#1319 fixed commit](https://github.com/DistrictDataLabs/yellowbrick/commit/5e493f212aca0efc845c63dadc4736c0bfcfa96f), [v1.5](https://github.com/DistrictDataLabs/yellowbrick/blob/v1.5/yellowbrick/style/colors.py#L32-L56), S09/S10/S27/S28 | #1323 직접 수정 및 tag 없음 확인이 아니라 미확인; #1319 인과 링크 없음 |
| Elpy C06 #1938 | installed < PyPI latest; config JSON | LooseVersion, warning 출력 문제 | 경고 필터 추가; LooseVersion 유지; #1951 추가 억제 | [#1938](https://github.com/jorgenschaefer/elpy/issues/1938), [#1939](https://github.com/jorgenschaefer/elpy/issues/1939), [#1951](https://github.com/jorgenschaefer/elpy/pull/1951), [자식 파일](https://github.com/jorgenschaefer/elpy/blob/2718cd5e815d9c15a5fb08e0bcf9f8ce552a6ae8/elpy.el#L632-L710), S12–S14/S30 | exact MELPA build, 비교 쌍 |
| Elpy C07 #2051→#2055 | 동일 latest; Python>=3.12에서 import 실패 | LooseVersion, 모듈 부재 오류 | setuptools 의존성 추가, 비교 유지; Emacs version<로 RPC 의존성 분기 | [#2051](https://github.com/jorgenschaefer/elpy/issues/2051), [#2055](https://github.com/jorgenschaefer/elpy/pull/2055), [merge file](https://github.com/jorgenschaefer/elpy/blob/bcfd5e8c25e5efbcb26cfcf389f1bf01c2e2f44f/elpy.el#L635-L710), S15/S16/S31/S32 | 실제 배포 build; 같은 환경 비교; 20241227.2255 후속 실패는 원인 혼재 |
| Elpy C08/C09 #2051 linked forks | installed < latest, None/exception 처리 | LooseVersion | [직접 호출 parse 교체](https://github.com/jorgenschaefer/elpy/commit/213a26a5af3de7a3474e9188f6d07e8e75195841) 또는 [ModuleNotFoundError fallback alias](https://github.com/jorgenschaefer/elpy/commit/208e5f09f61aa998cc6d9b61965cbec67e9134d2); parse 판별 시대 의존 | S17/S18; fixed diffs 640/663 | upstream 채택/first tag 미확인; broad except가 invalid와 network를 모두 None으로 |
| 보강 MNE C10 #10404→#10406 | library.__version__ >= min, 개발판 허용 | strict _compare_version; min gate 회귀 | strip=True default로 특정 접미사 제거; strict comparator 유지 | [#10404](https://github.com/mne-tools/mne-python/issues/10404), [#10406](https://github.com/mne-tools/mne-python/pull/10406), S19–S21 | 지명 표본 아님; 실제 설치 replay/태그 미확인 |

| 원문에 실제 나온 문자열 | 옛 판정 | 대안별 판정·증거 종류 | 예외·경쟁 설명 | 반례 URL |
|---|---|---|---|---|
| 1.0.dev0 >= 1.0 (V01) | True 보고 | packaging False 보고; MNE strip gate True 기대 | 둘 다 규격 문자열; 최소값 보존과 규격 순서 충돌; 동일 계보 1관측 | [MNE #10404](https://github.com/mne-tools/mne-python/issues/10404), [packaging #514](https://github.com/pypa/packaging/issues/514) |
| 1.0.dev0 == / <= 1.0 (V02,V03) | 둘 다 False 보고 | strip으로 같게 만드는 경우 둘 다 True 추론; strict == False, <= True | gate용 suffix 제거를 전체 정렬/동등성에 적용 금지 | [MNE #10404](https://github.com/mne-tools/mne-python/issues/10404) |
| 5.15.12-1-MANJARO < 5.10 (V04) | False (setuptools shim) 보고 | 당시 parse True 보고; 23.0 parse/Version은 InvalidVersion 규칙 추론 | kernel/vendor 문자열; 패키지 정확 판 미확인; 실제 named consumer 입력 아님 | [packaging #501](https://github.com/pypa/packaging/issues/501), [23.0 source](https://github.com/pypa/packaging/blob/23.0/src/packaging/version.py#L43-L62) |
| 3.4.1 >= 1.5.0 (V05) | True 추론 | Version True 추론 | release에 나온 matplotlib 값과 gate 상수 결합; 같은 환경 실측 아님; 좁은 단일 권고 | [Yellowbrick releases](https://github.com/DistrictDataLabs/yellowbrick/releases), [gate](https://github.com/DistrictDataLabs/yellowbrick/blob/v1.5/yellowbrick/style/colors.py#L32-L56) |
| 1.19.4, 1.26.1 < 1.14 (V06,V07) | 둘 다 False 추론 | 둘 다 Version False 추론 | CI의 * branch는 해당 핀 실제 설치 아님; 3.11 명칭/3.10 실행 차이 | [CI](https://github.com/scikit-learn-contrib/scikit-learn-extra/blob/0f95d8dda4c69f9de4fb002366041adcb1302f3b/azure-pipelines.yml) |
| 21.9b0, 0.18.0, 1.5.7, 0.31.0 (V08–V11) | latest 미확인, 비교 불가 | Version은 각 입력 수용 예상; 결과 미확인 | 실제 Elpy JSON PyPI false, latest null; 21.9b0는 PEP440 beta이지 vendor 예 아님 | [#1939](https://github.com/jorgenschaefer/elpy/issues/1939) |
| 3.5.0,3.6.0,3.12.0 (V12–V14) | 다른 함수 | RPC dependency 목록 기대; ERT 새 테스트 통과 저자 보고 | version<는 Emacs 함수, Python 비교로 환산 금지 | [ERT test](https://github.com/jorgenschaefer/elpy/blob/bcfd5e8c25e5efbcb26cfcf389f1bf01c2e2f44f/test/elpy-rpc--get-pip-dependencies-test.el) |
| 3.4j,3.2.pl0 (V15,V16) | CPython 문서 허용 | Version InvalidVersion 추론 | 문서 예시, 현업 문자열 아님 | [old source](https://github.com/python/cpython/blob/v3.11.0/Lib/distutils/version.py#L270-L344) |
| 1.23.0.dev0+782.g1168868df6, 1.9.0.dev0+1485.b06254e, 3.6.0.dev1651+g30d6161406, 1.1.dev0, 0.56.0dev0+39.gef1ba4c10, 9.1.0.rc1, 0.3dev0, 0.2.2.dev0 (V17–V24; 각 min values.csv) | LooseVersion 시험 안 함 | strict gate False; strip gate True: 시험 기대 | monkeypatch fixture, actual runtime/installed 값 아님 | [MNE #10406 diff](https://github.com/mne-tools/mne-python/pull/10406/files) |
| 3.2.2+150.g1e93bd5d, 1.2.3, 1.2, 1 (V25–V28; 각 min values.csv) | LooseVersion 시험 안 함 | strict/strip 모두 True: 시험 기대 | strip 반환 문자열 변경 가능; local 순서의 일반적 동치 아님 | [MNE #10406 diff](https://github.com/mne-tools/mne-python/pull/10406/files) |

| 사용자 목적 | 보존할 조건 | 반환할 원전 | 허용 문장 | 추가 질문 또는 보류 | 뒤집을 관측 |
|---|---|---|---|---|---|
| 과거 호출을 읽는 사람 (A01) | 해당 원판의 token 비교 및 연산 | [CPython v3.11 LooseVersion](https://github.com/python/cpython/blob/v3.11.0/Lib/distutils/version.py#L270-L344) | 옛 호출은 규격 버전 정렬과 다른 토큰 순서를 사용했다. | 당시 Python/셋업툴 판과 연산은? | 실제 호출 심볼/판이 다름 |
| 현재 표준판만 처리 (A02) | PEP440 보장 + 규격 순서 의도 | [PyPA Version spec](https://packaging.python.org/en/latest/specifications/version-specifiers/) | 규격 버전의 규격 정렬이 목적이면 Version을 쓰되 invalid 정책을 정하라. | 개발판도 해당 최소 기능을 만족해야 하는가? | 실제 gate 계약이 1.0.dev0을 1.0 이상으로 보존 |
| 벤더 문자열도 처리 (A03) | 허용 영역과 실제 연산별 결과 또는 벤더 순서 | [looseversion](https://pypi.org/project/looseversion/) | 옛 토큰 비교를 유지할 후보를 검증하되, 벤더 순서가 목표면 그 도메인 비교기를 별도 선택하라. | 실제 문자열 두 개와 <, >=, == 중 보존할 결과는? | 실제 입력이 모두 규격이고 표준 순서를 의도하거나, vendor 순서가 옛 비교와 다름 |
| 개발판 최소 기능 gate (A04) | 연산별 정책; strict 전체 정렬 별도 | [MNE #10406](https://github.com/mne-tools/mne-python/pull/10406) | 개발판 허용은 gate의 정책으로 제한할 수 있다. | 동등성/정렬에도 strip 필요? | dev가 실제 요구 기능 미구현 |
| obsolete gate (A05) | dependency floor와 도달 불가 | [Yellowbrick #1334](https://github.com/DistrictDataLabs/yellowbrick/pull/1334) | 지원 범위에서 도달 불가인 분기는 삭제도 검토한다. | 지원 제약 우회 환경도 포함? | 실제 1.5.0 미만 지원 계약 |

## 판정: PARTIAL

표의 제안/병합/릴리스/실행은 서로 다른 관측이다. 지명 3소비자에서 실제 same-call 교체 병합 1곳(scikit), 정확 patch 전후 3곳(그중 Yellowbrick proposal 및 Elpy fork), named first post-change tag 확인 0곳(미확인 또는 미병합, 전수 부재 아님). 실제 값에서 구/신 차이는 보강 MNE와 Manjaro 2개 독립 당사자 신고 계보로 확인했고, 좁은 안정판 동일 판정은 원문 값을 대입한 규칙 추론으로 확인했다. 이 작업 자체 실행은 없음. 필수 자료 수는 충족하나 named 소비자 배포·동일 입력 실행 연결과 실제 채택 2곳의 엄격 조건이 부족. PARTIAL로 인계.

### Q1–Q7
**Q1.** C01은 doctest skip, C02/03은 API gate, C04/05는 Matplotlib rc API gate, C06–09는 PyPI 새 버전 알림. 분류하면 min gate와 current<latest(신규판 판단)이며 전순서 sort 자체를 하는 것으로 코딩하지 않는다. 원 입력은 __version__ 혹은 PyPI JSON info.version. Elpy warning/output 및 connection 처리가 비교와 별개.

**Q2.** [PEP632](https://peps.python.org/pep-0632/)는 3.12 stdlib 제거와 packaging 방향을 제시하지만 의미 동일성을 약속하지 않는다. S02 LooseVersion은 숫자·문자 토큰 비교; S03 packaging 21.3 parse는 invalid에서 LegacyVersion, S04 23.0 parse는 Version으로만 진행. S06 PEP440 순서와 거부 규칙, S05 분리 호환 패키지의 동작 보존 주장(독립 검증 아님). S43 댓글은 PyPA 도구의 PEP440 목적을 명시하고 generic parser/vendoring을 구별한다. 입력 허용과 정렬은 다른 축이다.

**Q3.** C01–03 #167은 정확 same-call 변경 및 명시 의존성 추가. #141 자체는 open. C04/05 #1319 정확 패치는 #1323의 후속이 아니라 선행 미병합 대조. C06 2021 warning 억제, C07 2024 setuptools로 import 지원은 서로 다른 해결이고 비교 심볼 유지. C08 fork는 실제 parse 교체, C09는 ModuleNotFoundError fallback만. 동일 호출의 결과도 fallback이 활성화되는 환경과 packaging 버전에 따라 달라질 수 있다. 두 fork upstream 채택은 미확인.

**Q4.** S19/S20의 1.0.dev0은 정상 규격이지만 gate 판단 갈림. S43의 실제 vendor kernel release는 당시 parse와 LooseVersion 순서 차이, 최신 strict의 거부는 S04에 근거한 추론. S34/S27 안정판은 좁은 동일 판정. S26 CI 선언과 actual install을 분리, S21 fixture와 현업 입력을 분리, S13 Elpy의 installed 값은 latest 쌍 없음. 실제 named vendor 입력 및 exact before/after 판정은 미확인. 수용 정책과 조작 둘 다 알아야 한다.

**Q5.** #167 병합 2023-12-14, 확인 release v0.3.0 2023-03-27이고 태그 old 코드. Yellowbrick v1.5 2022-08-21 old 코드, #1323 open, #1319 open. Elpy #1951 warning fix 2021-12-11 이후 MELPA 표시 성공 보고, 정확판·RPC 경로·latest 값 같지 않음. #2055 2024-12-27 merged, 20241227.2255 후속 실패 보고, import 및 pkg_resources 문제 섞임. #2055 저자 신규 ERT 통과 및 기존 실패 보고는 별개. S45–47 태그 전체 목록 접근 차단. 첫 실제 교체 포함 tag를 추정하지 않는다.

**Q6.** S36 Debian EVR 유사 분리(정확 Debian epoch/upstream/revision), tilde 앞 정렬; S37 RPM EVR 1.0-1 <1.0-5 <1.0.1, ~와 ^; S38/39 청구기호 class 숫자와 Cutter 소수 및 연도. A55가 A6보다 앞이라 숫자 토큰 55<6으로는 맞지 않는다. 공통 원리는 도메인·연산·필드 해석을 먼저 확인하는 것뿐. Python Version/LooseVersion을 이식하지 않는다.

**Q7.** A01–03은 같은 old symbol에 서로 다른 목적을 조건으로 적용. 역사 링크는 원판, 표준 순서 링크는 규격 및 구현, vendor 호환 링크는 후보 및 실제 문자열 확인. A04는 minimum gate 한정, A05는 삭제 가능성. 선택은 제품 최종 설계가 아님.

## 경쟁 설명과 조합 조건
COUNTEREXAMPLES.md의 세 관점 및 다른 분야 비교 참조. 경고 소실/모듈 import/테스트 pass/업데이트 올바름은 서로 독립 관측. PEP440만 보장한다고 동작이 같지는 않으며, 비규격을 파싱한다고 옛 비교가 보존되는 것도 아니다. 조건부 링크를 반환하는 최소 구조는 입력 도메인 + 연산 + 허용/거부 정책 + 원전판 + 예외 증거. 단일 권고는 표준 순서 의도 또는 narrow invariant가 확인될 때만. 역사 원판은 별도 유지. 비용은 실제 문자열과 한 개의 원하는 결과를 묻는 작은 추가 마찰, 또는 원전+실행 검증 비용; 제품 DB/수집기/최종 검색 형식은 선택지로 남김.

## 자기 점검에서 가장 중요한 3개 약점
| 약점 | 영향을 받는 주장 | 다음 조사와 원자료 | 판단이 뒤집히는 관측 |
|---|---|---|---|
| 첫 post-change tag 및 실제 upstream 변경 연결 부족 | 지명 소비자 2곳 이상의 배포된 same-call 후계 | clone 각 원 저장소, git tag --contains exact merge/commit, tag 파일/릴리스 및 PyPI wheel과 연결; S45–47 | Yellowbrick/Elpy에서 동일 호출 변경을 실제 포함한 첫 tag와 upstream merge 확인 |
| named 소비자의 동일 실제 입력·환경 결과 쌍 미확인 | 실제 사용자 문자열에서 후계가 갈리거나 유지되는 주장 | S13 actual installed+PyPI latest 로그, S09 mpl raw value, S26 CI 실제 installed logs; fixed replay 및 실제 결과 비교 | 두 named 소비자에서 같은 값/환경으로 old/new 판정·예외가 확인되고 반례 범위가 좁혀짐 |
| fallback/호환 후보의 정확판·비규격 동작 미검증 | vendor 및 역사 입력에 대한 호환 단일 권고 | S05 pinned looseversion, CPython3.11, packaging21.3/23.0; S43 exact reporter environment; compare <,>=,== and errors | looseversion에서 실제 옛 결과가 불일치하거나 vendor 도메인 comparator와 다르므로 다른 후보가 필요 |
