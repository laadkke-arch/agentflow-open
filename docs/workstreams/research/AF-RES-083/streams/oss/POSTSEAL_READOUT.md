# O02 후속판 대조 — 핵심 모집은 0/3, 보조층은 7개 레코드

## 분모와 판 고정

등록한 세 저장소의 옛 배포 문서·예제 검색에서 핵심 모집 기준에 맞는 지시는 검출하지 못했다. **O02-1, O02-2, O02-3은 모두 공석이며, 아래 보조 사례로 채우지 않는다.** 이는 등록한 검색 범위에서의 미검출이며 세 프로젝트에 관련 안내가 전혀 없다는 증명은 아니다. 핵심 A/B 평가의 판정 가능 분모는 0이다. 운영 레코드도 0개이므로 운영 오류율은 산출 불가(0/0)다.

| 저장소 | 옛 판 | 변경 후 첫 정식 태그 | 조사 시점 마지막 정식 태그 | 해석상 주의 |
|---|---|---|---|---|
| statsmodels | v0.12.1 | v0.12.2 | v0.15.0 | 첫 후속판과 실제 내부 이관을 포함한 나중 판을 구별한다. |
| Astropy | v4.2 | v4.0.5 | v8.0.3 | v4.0.5는 시간순으로 처음 나온 유지보수 태그다. v4.2의 직계 후속으로 가정하지 않는다. |
| scikit-learn | 0.24.0 | 0.24.1 | 1.9.1 | 옛 AUC 구현은 NumPy, 최신 구현은 SciPy다. 최신 namespace를 과거에 소급하지 않는다. |

태그→커밋·시각·메타데이터 출처는 [versions.json](versions.json)에 있다. upstream 기준은 SciPy v1.6.0의 2020-12-31 명칭 이관이며 1.14 제거와 다르다. 옛 원문과 동일 레코드의 A/B 제안은 `35d7e18024cced8cc81f9397b65e90e0e74bb907`에서 봉인했다. 후속판 첫 취득은 2026-11-23T13:35:42.690296Z이고 취득 요청도 봉인 신호 이후였다. [postseal-acquisition.jsonl](postseal-acquisition.jsonl)에 각 취득 시각과 해시가 있다. 다운로드만 한 파일은 직접 읽은 독립 자료로 세지 않았다.

## 원 레코드별 후속 관측

| 보조 레코드 | 원 독자의 지시 | 첫 후속판 / 마지막 판 | 실제 수정과 그 범위 | A/B 판정의 한계 |
|---|---|---|---|---|
| O-AUX-SM-GAM | `BSplines`로 자동차 자료의 평활항을 만들고 Gaussian/Poisson `GLMGam.fit()` 및 부분 효과를 구한다. | 첫 판의 가이드 파일 전체 동일. 최신판의 주요 `BSplines`·fit 예제 문단도 동일. | 내부 적분은 `simps`→`simpson` 및 `x=x`로 바뀌었다. 가이드 후반의 k-fold RNG 추가는 별도 재현성 수정이다. | A가 원 가이드에서 바꿀 옛 적분 심벌은 없다. B의 원 지시 보존은 텍스트와 맞지만 원 예제의 수치 결과까지 검증한 것은 아니다. O-S01–03, O-P01–02, O-P05–06, O-P21–22. |
| O-AUX-SM-GEE | 간질 자료의 Poisson GEE를 적합하고 요약표를 읽는다. | 첫 가이드 파일 전체 동일. 최신판의 fit/summary 문단 동일. | 다른 메서드 `qic()` 내부의 `trapz`는 바뀌었다. 원 지시는 `qic()`를 호출하지 않는다. | 그 내부 수정으로 원 fit/summary 안내의 정정 필요성을 증명할 수 없다. O-S04–05, O-P03–04, O-P07–08. |
| O-AUX-AST-KERNEL | 정확도가 우선일 때 `Gaussian1DKernel(..., mode='integrate')`를 선택한다. | 세 판의 Discretization 문단 동일(뒤에 추가된 절 anchor 제외). | 원 설명의 연산은 `scipy.integrate.quad`/`dblquad`다. O02 적분 이름과 다르다. | O02를 이유로 바꾸지 않는 판단을 지지한다. 정확도 주장의 실제 실행 검사는 별개다. O-S07, O-P09–10. |
| O-AUX-AST-FITTING | 잡음이 있는 200개 점에 `Trapezoid1D`와 `Gaussian1D`를 적합한다. | 첫 가이드 파일 동일. 최신판은 `TRFLSQFitter`, `default_rng`, `maxiter=200`을 쓴다. | 실제 안내 수정은 있으나 모델의 `Trapezoid1D`가 적분 함수로 바뀐 것이 아니다. 최신 설명은 경계가 있는 모형에서 옛 fitter의 한계도 설명한다. | 단어 trapezoid만으로 SciPy 적분 이관 대상에 묶을 수 없다. O-S08, O-P11–12. |
| O-AUX-AST-BLACKBODY | 10,000 K `BlackBody`를 파장 1,000–30,000 Å의 1,000점에서 그리고 단위·복사휘도를 해석한다. | 첫 판의 BlackBody 절 동일. 최신판도 같은 모델 목적이며 plotting 표현과 deprecated 안내가 바뀐다. | 예전 별도 함수의 deprecation 안내 삭제는 아래 제거 사건과 연결된다. 원 가이드는 `trapz`를 권하지 않는다. | 100 K 적분 시험을 이 안내의 수치 검증으로 옮겨 붙이지 않는다. O-S09–10, O-P13–15. |
| O-AUX-AST-TRAPZ | 공개 가이드가 아닌 `test_blackbody_scipy`의 내부 적분 시험. | 첫 판에 `trapz` 시험 유지. 최신판에서 그 파일 삭제. | 삭제의 실제 원인은 4.0부터 deprecated였던 blackbody 모듈 제거다. PR 병합 결정은 2020-11-02로 SciPy 1.6 발행보다 앞선다. | A의 무조건 `trapezoid` 치환은 옛 SciPy >=1.1 지원 선언과 정적으로 충돌한다. 보조 시험의 판정이며 핵심 오류율에 더하지 않는다. O-S10–13, O-P15, O-E05, O-PR-10972, O-P24. |
| O-AUX-SKL-AUC | AP와 선형 보간의 trapezoidal AUC가 다르며 AUC가 낙관적일 수 있음을 이해한다. | 첫 가이드·예제 파일 동일. 최신판에서도 AP 대 AUC 구별 문단 유지. | 옛 `np.trapz`→SciPy fallback helper→직접 `scipy.integrate.trapezoid` 순으로 내부 구현이 바뀌었다. | 최신 namespace로 옛 대상을 재분류하지 않는다. 새로운 이름으로 AP와 AUC의 의미를 합치지도 않는다. O-S14–16, O-P16–20. |

세부 판정과 실제 diff ID는 [revisions.csv](revisions.csv)에 있다. 세 공석 행과 일곱 보조 행 모두 `denominator_eligible=false`다.

## 실제 발행자가 고친 것과 고치지 않은 것

### statsmodels: 지원판에 맞춘 fallback과 인자 수선

발행자의 [2023년 이관 diff](https://github.com/statsmodels/statsmodels/commit/410bf74b3edd169e83d3a816dc9ab8a8c65fe301)는 새 `simpson`/`trapezoid` import를 먼저 시도하고, 없으면 옛 이름을 새 지역 변수 이름으로 가져오는 fallback을 넣었다. 이는 호출 이름 일괄 교체만으로는 옛 지원판을 보존하기 어렵다는 실제 대응이다. [0.14.1 릴리스 원문](https://github.com/statsmodels/statsmodels/blob/7767ecdcd616c368ad3e1a4a79fe8997ca8e45ec/docs/source/release/version0.14.1.rst#L89-L98)은 그 PR 8940을 기록한다. 이후 [인자 수정](https://github.com/statsmodels/statsmodels/commit/defa30ace744de5c9248975643b3e3667c30cf4b)에서 `x`를 키워드로 전달했다. [2026년 fallback 제거](https://github.com/statsmodels/statsmodels/commit/ab01f9664bb3b7b425443625a015bfd853f05765)는 최소 지원 SciPy 1.8이 새 이름 도입판 1.6보다 높아졌음을 당사자가 이유로 든다. 세 diff는 한 이관 계보로 묶었다. O-E01–03, O-PR-8940/9046/10015, O-P23.

주요 GAM 안내 예제는 유지되었지만 내부 `get_covder2` docstring에는 최신판에도 `scipy.integrate simps`가 남는다. 따라서 “코드 이관 완료”에서 “모든 설명 정정 완료”가 따라오지 않는다. 다만 그 내부 docstring은 이번에 봉인한 핵심 안내 모집 범위에 속하지 않는다. [GAM 문서의 RNG 변경](https://github.com/statsmodels/statsmodels/commit/bd11a8744e02951692b5450561267997dbee26a7)은 별도 사건으로, 당사자 commit 메시지는 경고에 따른 문서 실패 수정을 말한다. 이 수정이 관측되었다는 사실만으로 SciPy 적분 이관이 수정 이유라고 추론하지 않았다. O-P06, O-E04.

### Astropy: 없어졌다는 관측만으로 이관 수선을 단정하지 않기

`test_blackbody.py` 최신 경로의 404는 시도 원장에만 먼저 기록했다. 삭제 자체와 이유는 [실제 diff](https://github.com/astropy/astropy/commit/d5abb1fd5742fe87cd9710b7cd438fe3027c1076), [PR 10972](https://github.com/astropy/astropy/pull/10972), [v4.3 변경 기록](https://github.com/astropy/astropy/blob/9f2c27e49b22f35fba04725fc4cd54b0300838cb/CHANGES.rst#L309-L316)을 통해 별도로 확인했다. 모듈·시험·deprecated 안내를 함께 제거한 사건이며 SciPy 1.6 발행 전에 병합됐다. 최신 시험으로 대체 계보를 만들지 않았다. 첫 후속 태그 v4.0.5의 유지보수 계보에는 옛 시험이 남아 있다는 사실과도 모순되지 않는다. O-E05, O-PR-10972, O-P24.

### scikit-learn: 같은 계산 이름도 원 namespace는 별도로 남기기

옛 `auc()`는 `np.trapz(y, x)`를 호출한다. [PR 27140](https://github.com/scikit-learn/scikit-learn/pull/27140)의 실제 diff는 SciPy integrate import와 구판 fallback으로 옮겼고, [후속 제거 diff](https://github.com/scikit-learn/scikit-learn/commit/b0f86e797190d1fd62331eac8b88a5b0dfa522b9)는 SciPy <1.6 지원 코드를 없앴다. PR 본문에는 `scipy.interpolate.trapezoid`라고 적힌 namespace 오타가 있지만 실행 코드는 `scipy.integrate.trapezoid`다. 당사자 글의 주장과 실제 수정 원문을 분리해 남겼다. AP와 선형 보간 AUC를 구별하는 안내는 세 판에 걸쳐 유지됐다. O-E06–07, O-PR-27140, O-P16–20.

## Q3: 079와 무엇을 조인할 수 있는가

| 소비자 관측 | 입력·출력 요구 | 079와의 조인 | 아직 없는 근거 |
|---|---|---|---|
| GAM 원 가이드 | `df_autos`의 weight/hp, spline df=[12,10], degree=[3,3], alpha=[21833888.8,6460.38479], fit·부분 효과 | 내부 `simps` 호출까지 정적 경로 연결. 079의 일부 `simps`/`cumtrapz`는 소스 별칭 확인뿐이다. | 원 가이드와 같은 환경·자료·alpha의 실행 결과. downstream `TestGAMMPGBS`도 `constraints='center'`, `include_intercept=True`, 다른 alpha를 써서 원 입력과 같지 않다. |
| GEE 원 가이드 | epil Poisson fit/summary | `qic()`의 10,000점 내부 적분과 다른 관측이다. | 원 가이드가 QIC를 요구한다는 근거. |
| Astropy test | 100 K, `np.logspace(0,8,100000)*u.AA`, W/(m²·µm) 단위, `trapz(flux.value,x=lum.value)`, `sigma_sb*T**4/pi`, rtol=0.01 | 같은 적분 심벌 계보까지만 연결한다. 079의 실행 입력과 다르다. | 이 소비자 입력으로 수행한 옛/새 심벌 수치 비교, 실제 설치 SciPy freeze. 정확한 함수명은 **test_blackbody_scipy**(old L62, first L61). |
| scikit-learn AUC | 단조 x, 최소 2점, 순서에 따른 direction, `np.trapz` | NumPy backend 계통과 SciPy public namespace는 구별한다. | 원 예제의 실제 배포 빌드 환경과 그 버전에서의 출력 재실행. |

이 조사에서 새 native 실행은 하지 않았다. dependency floor, tox matrix, PR의 체크박스, CI 업그레이드 명령은 설치된 판의 증명이 아니다. 과거 HTTP redirect 흐름도 복원되지 않았으므로 옛 목적지의 역사적 도착은 미확인이다.

## 자료량, 검증, 재개 입력

옛 원장 17행과 후속 원장 36행을 직접 읽은 자료 행으로 보존했다. 관련 판·테스트·PR·릴리스 노트는 `lineage_id`로 접는다. 이 부분에서 보수적으로 센 독립 하류 안내 저작은 6계보(GAM, GEE, kernel discretization, model fitting, BlackBody, AP/AUC)이고, 새 공개 변경 사건은 4계보(statsmodels 적분 이관, GAM RNG, Astropy 모듈 제거, scikit-learn 이관)다. 동일 AP/AUC 목적의 가이드와 예제는 둘로 세지 않았다. dependency/build 파일은 별도의 독립 저작 수를 늘리지 않는다.

텍스트 차이는 [paragraph-comparison.json](paragraph-comparison.json)으로 확인했다. GAM 주요 예제, GEE fit/summary, Astropy Discretization, scikit-learn AP/AUC 구별 문단은 각 원문 절을 지정해 세 판의 해시를 비교했다. 이 검사는 문서 보존 관측이며 프로그램 동작 검사가 아니다. [postseal-audit.json](postseal-audit.json)은 봉인 파일과의 동일성, 원장 참조, 행 수를 기록한다.

최소 다음 확인은 다음과 같다. (1) 핵심 모집을 더 넓힐지 결정할 경우 별도 회차에서 검색 범위를 먼저 봉인하고 GAM 같은 간접 호출 가이드를 포함할 조건을 명시한다. 기존 공석을 사후 교체하지 않는다. (2) GAM 원 가이드의 정확한 자료·alpha와 시험의 centered spline 입력을 각각 고정한 뒤 SciPy 지원판별 출력 및 실패 지점을 검사한다. (3) Astropy의 옛 `test_blackbody_scipy`를 지원 가능한 격리 환경에서 그대로 읽고 실행한다면 freeze와 단위 변환·적분·기대값을 모두 남긴다. 삭제된 시험을 최신 BlackBody 데모로 대신하지 않는다. 이들은 미실시이며 전체 인계의 실행 명령 문서에서 이어받는다.
