# 별도 AI 검토 — ① 모집·선정과 ② 목록 예측

검토자: `/root/cross_domain`. **사람 검토가 아닌 별도 AI 에이전트의 실제 교차검토**다. 본인이 작성한 Q6 EPUB·Data Citation Corpus 부분은 독립 검토 범위에서 제외했다. 이 기록은 단계 ③·④ 결과판의 최종 승인을 뜻하지 않는다.

검토 고정판은 ① `c0d31ca194e47fe69bc51dc0ef85d6e346b50774`, ② `0df9ea9edbcee995d631eef54b65fd43f73c245f`다. 원본 파일은 수정하지 않았다. 작업 트리의 미완성 단계 ③ 원장은 잠정 중복 점검에만 사용했고, 봉인된 ② 결과와 구별했다.

## 먼저 수정·확인할 사항

| ID·수준 | 실제 관측·근거 | 영향 | 요청한 처리 |
|---|---|---|---|
| R1 · 작은 사실 오기 | ① `evidence/cpython/stage1.md` 22행은 PY2 그림을 500×322라 한다. 직접 다시 받은 [3.12.0 PNG](https://docs.python.org/release/3.12.0/_images/hashlib-blake2-tree.png)의 IHDR은 **500×320**, 11,070B, SHA256 `382828d64e88644e47e695d717ea8432ec1ef79a17f2d209b11aef4fdbfa4bf5`다. 기존 `PY2-old-excerpt.json`·sources도 320이다. | 판 선택·그림 동일성·예측 값에는 영향 없음. 사실 표시는 불일치한다. | 봉인된 기록을 없던 일로 바꾸지 말고 결과판에서 정정 사실·근거를 명시한다. |
| R2 · 원장 필드 누락 | ①·② root `sources.jsonl`의 `GG-OLD-DEPLOYS`, `GG-OLD-TAG`, `GG-OLD-PKGDOWN`은 `claim`이 빈 문자열이다. `observed`·URL·한계는 있다. | 사용자 요구인 자료별 지지/반박 주장이 비어 있다. | 최종 병합 원장에서 배포↔소스 연결, 태그 식별, 빌드 도구/시각 표시가 각각 어느 축을 지지하고 생성 귀속은 왜 증명하지 못하는지 적는다. |
| R3 · 단계 ③ 잠정 집계 위험 | 점검 시점 GG2 OLD/NEW SOURCE는 SHA `e28cc59f…`가 같고, OLD/NEW WORKFLOW는 `7a02cdb8…`가 같다. 두 ACTIONS 응답도 36B·SHA `a2790a38…`로 같다. 모두 잠정 `counted=true`였으며 최종 병합에서 중복 제거한다고 명시돼 있다. | 작업 중 원장을 그대로 합산하면 동일 저작·동일 바이트를 판별로 중복 센다. 빈 run 목록은 생성 job이 아니다. | 동일 source/workflow는 각각 한 자료로 집계한다. 빈 Actions 응답은 해당 조회 범위의 반환 0건만 지지하며 생성 job의 부재나 특정 생성 실행을 뜻하지 않음을 적는다. 최종 원장·수치에서 재검사한다. |
| R4 · 표기 개선, 예측 결함 아님 | root `predictions.csv`의 `same_basename_candidates`는 MPL은 0, CPython은 정확 경로까지 포함한 문자열, ggplot2는 정확 경로 외 후보 JSON이다. | 이 열만 직접 비교하면 CPython과 ggplot2의 ‘중복 수’가 같은 정의처럼 보일 수 있다. | 봉인값을 유지하고 결과 비교에서는 `exact_path_count`와 `other_same_basename_paths/count`를 구분한다. |

R1·R2는 실제 확인된 불일치이며 부모 작업자에게 전달했다. R3는 최종 병합 전의 잠정 위험으로, 최종 결과의 오류라고 미리 판정하지 않았다.

## 봉인과 노출 경계

[GitHub 커밋 API](https://api.github.com/repos/laadkke-arch/agentflow-open/commits/0df9ea9edbcee995d631eef54b65fd43f73c245f)를 직접 열었다. ②의 부모가 정확히 ①이고 커밋 시각은 **2026-11-23T19:45:38Z**다. 이 원격 응답의 SHA256은 `c083da642affe34a2e543313dd963c1791776898b338370383242efa2b4f5ea4`이며, 짧은 속성은 [independent-reads.json](independent-reads.json)의 `SEALED-COMMIT2`에 있다.

`git show`로 두 고정판을 비교한 결과 `SCOPE.md`, `freeze.json`, 통합 `frame.csv`는 **바이트 동일**하다. ② root `predictions.csv`는 여섯 행 모두 YES다. 작업 트리와 봉인판의 raw SHA 차이는 일곱 줄의 CRLF/LF 차이뿐이고 줄바꿈 정규화 후 내용이 같다. 따라서 이 차이를 예측 수정이라고 판정하지 않았다. 파일별 SHA와 검산 결과는 [selection-review.json](selection-review.json)에 있다.

단계 ② CPython 스크립트는 새 ZIP을 불투명하게 받아 저장한 뒤 `ZipFile.namelist()`만 사용한다. `ZipFile.read`·extract·새 HTML 분석은 없다. ggplot2 스크립트는 태그 SHA, 배포 날짜/SHA 투영, `tree[].path/type` 목록을 읽어 정확 경로 수를 계산한다. 응답에 동봉된 blob SHA/size·배포 커밋 message는 예측에 사용하지 않는다고 명시한다. Matplotlib 단계 ②도 root/image 목록·배포 SHA/date에 한정된다. 이는 `SCOPE.md` 23행에 봉인된 취급과 일치한다.

다음 판 ZIP 바이트를 전송받은 사실 자체를 숨기지 않으며, 그 의미를 ‘파일을 읽었다’로 바꾸지 않는다. 반대로 스크립트와 영수증만으로 작업자의 모든 잠재적 사전 지식을 증명할 수도 없다. 이번 검토는 공개된 노출 로그·실제 실행 코드·커밋 순서에서 금지된 다음 판 본문 선열람의 모순을 찾지 못했다는 범위다. 릴리스 목록/노트·현행 release-guide 미리보기의 선노출은 SCOPE 48–50행에 명시돼 있다.

## Q1 릴리스·정렬 선택

| 프로젝트 | 봉인된 두 판·공개일 | 후보 수·선택 순위 | 독립 점검 결과 |
|---|---|---|---|
| Matplotlib | 3.7.0 2023-02-13T22:22:08Z → 3.7.1 2023-03-04T07:19:11Z | 612 고유 경로; 3 `animation_demo`, 10 `pause_resume` | 612 경로의 사전식 순서를 검산. 기존 공식 릴리스 원장·선행 7페이지의 제외 영수증·옛 원발행판과 현행판 대조를 읽었다. 독립 릴리스 API 재조회는 403, HTML 재조회는 도구 DisabledError였으므로 이번 재조회로 날짜를 새로 확증했다는 주장은 하지 않는다. |
| CPython | 3.12.0 2023-10-02 → 3.12.1 2023-12-08 | 515 고유 HTML; 132 `howto/logging.html`, 264 `library/hashlib.html` | 공식 전체 릴리스 목록과 두 발행 페이지를 직접 다시 읽음. .0 후보 3.11.0은 2022-10-24로 기간 밖, 3.13.0은 2024-10-07, 3.14.0은 2025-10-07. 3.12.1 페이지는 첫 maintenance라고 명시. 515 경로 정렬과 적격 첫 둘을 검산. |
| ggplot2 | 3.5.0 2024-02-23T09:33:36Z → 3.5.1 2024-04-23T10:21:20Z | 208 고유 reference HTML; 3 `aes.html`, 7 `aes_colour_fill_alpha.html` | 208 경로 정렬을 검산하고 이전판 첫 7페이지를 직접 재열람. API 재조회 403; 3.5.0 GitHub 발행 페이지는 별도 웹 경로로 읽었지만 3.5.1 재조회는 실패. 3.4.0/패치 선후 관계는 봉인 원장·release-selection.json 범위로 검토했다. |

세 모집틀 합계는 **1,335 후보 경로**다. 이 숫자는 읽은 본문 수가 아니다. CPython의 자동 스캔 515 HTML 중 실제 두 본문을 원장에 산입하고 나머지를 읽은 자료로 늘리지 않는 처리도 확인했다. Matplotlib·ggplot2는 첫 두 적격 후 본문 미열람인 경로를 부적격으로 단정하지 않는다.

공식 릴리스 목록의 공개일을 사용하고 같은 `x.y`의 첫 패치를 택한 해석은 SCOPE 13행에 사전 고정돼 있다. Git 태그의 author date·CRAN date·GitHub release published_at을 하나의 시각으로 합치지 않는 처리도 일관한다. 다만 이 검토의 API 재조회 실패는 원래 성공 영수증을 무효화하지도, 그것을 독립 재현했다고 바꾸지도 않는다.

### 설명 그림 포함과 ggplot2 selector 반례 탐색

SCOPE 15행은 설명 그림과 실행 결과를 모두 포함한다. CPython stage1 15행도 설명 그림을 실행 결과로 부르지 않는다. 따라서 PY1/PY2가 도식이라는 이유만으로 사후 탈락시키는 것은 봉인 기준을 바꾸는 행위다. 사용자 표현을 ‘실행 산출물’로 더 좁게 읽을 경우 선택이 달라질 수 있다는 해석상 한계는 보존돼 있다.

ggplot2 수집기는 명시적 Examples 구간을 우선 찾으므로, SCOPE의 넓은 주 본문 정의에 비해 설명 그림을 놓쳤을 가능성을 직접 조사했다. 고정판 `392175bbb00b04025aa5d17a0c18b3896adeb40f`의 첫 7페이지 **문서 전체**에서 `img/src/srcset`, `source`, 이미지·데이터 확장자 링크를 재확인했다. 결과는 [selection-rereads.json](selection-rereads.json)의 각 `GG-OLD-*`에 URI·행과 함께 있다.

- `absoluteGrob`·`add_theme`·`aes_all`: 공통 logo와 외부 Posit 로고뿐이다.
- `aes_`·`aes_auto`: 위 로고 외에 `figures/lifecycle-deprecated.svg` 상태 배지가 있다. 이는 주 예제의 설명/실행 그림으로 분류하지 않는다는 stage1의 제외와 일치한다.
- `aes.html` 195행의 첫 적격 그림은 `aes-1.png`다.
- `aes_colour_fill_alpha.html` 165행의 첫 적격 그림은 `aes_colour_fill_alpha-1.png`다.

이 앞부분에서 ‘Examples 바깥의 적격 설명 그림 때문에 first-two가 바뀐다’는 반례는 발견하지 못했다. 후순위 201페이지에 관한 전수 의미 판독을 했다는 주장은 하지 않는다. PY2 본문도 직접 다시 열어 705행의 그림 앞 가장 가까운 절이 `creating-hash-objects`임을 확인했다. 추측했던 anchor 오류는 실제 결함이 아니었다.

## Q2 exact-path와 basename 중복

SCOPE 24–26행은 정확 경로 한 번이면 YES, 정확 경로가 없고 다른 basename 후보가 있거나 정규화 경로가 중복되면 HOLD라고 봉인한다. `dev/reference/aes-1.png`와 `dev/reference/aes_colour_fill_alpha-1.png`가 존재해도 `reference/…`의 정확 경로가 각각 한 번이면 YES라는 규칙이다. 따라서 ggplot2 두 YES는 동명 중복을 숨기거나 사후 완화한 결과가 아니다.

다음 판 스냅샷은 release 시각 이후 첫 gh-pages 커밋이라는 날짜 규칙으로 택했고, 해당 스냅샷이 실제 3.5.1 source/deploy라는 확정은 봉인 뒤 남겼다. 이 유보는 단계 ② receipt에 명시돼 있다. 최종 판별에서 source-tag/deploy 연결을 실제로 확보하는지 확인해야 하며, 날짜 근접성만으로 새 생성 G=YES를 만들면 안 된다.

## 자료 수 사전 감사

| 고정판 | 원장 행 | `counted=true` | 예제 본문 | payload | 같은 계보·같은 SHA 중복 | 필수 구체 필드 누락 |
|---|---:|---:|---:|---:|---:|---|
| ① | 34 | 34 | 14 | 2 | 0 | claim 3행이 빈 문자열 |
| ② | 41 | 40 | 14 | 2 | 0 | 같은 claim 3행 |

여기서 본문 14에는 실제 읽은 선행 제외 본문도 있다. 이 수를 주 6사례×2판 12자리의 완료 수로 바꾸면 안 된다. 원장에 선언된 count/category·SHA의 산술 검토이며 최종 연구의 최소 개수 충족 판정은 아니다. ③에서 실제 payload·새 본문·발행 계보가 추가된 뒤 동일 저작·동일 바이트, 실패 응답, 읽지 않은 자동 수집물을 다시 제거해야 한다. 이번 재열람은 동일 자료의 별도 검토이므로 원문 자료 수를 추가하지 않는다.

## 재현·제한

`python -B docs/workstreams/research/AF-RES-098/evidence/cross-review/verify-selection.py`는 두 git 고정판·정렬·원장을 검산하고 공식 원문을 재조회한다. 최초 로컬 검토 스크립트는 열 이름 `prediction`/`prediction_U` 차이로 종료 1이었고, 이를 수정한 실행은 종료 0이다. 종료 0은 모든 HTTP 접근 성공을 뜻하지 않는다. 실제 실패와 범위는 [review-execution.json](review-execution.json)에 분리했다. 예제 프로그램·빌드는 실행하지 않았다. 원래 연구 파일이나 봉인 예측은 수정하지 않았다.

후속 결과 검토에서는 다음을 우선 확인한다: R1·R2 정정, R3 중복 제거, 12행 세 축과 6예측의 분모, 본문 부재와 접근 실패 구별, 생성 provenance 유보, 실제 비용의 문서/내부 파일 단위, RESULT 최종 3약점 및 check/cloud_check 대상 SHA. 현재 단계 ③·④와 HANDOFF는 이 검토의 승인 대상이 아니다.
