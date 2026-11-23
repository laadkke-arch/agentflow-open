# Python 목록 봉인 v1 — 목적지 미열람

이 판은 최초 SCOPE의 '본문 제목 범위'를 그대로 적용하여 조직 범주도 스캔한 **잠정 메타데이터판**이다. 부모의 사전 검토가 조직 범주와 기능 절을 구분할 것을 제안했으나, 현재 파일을 먼저 커밋한 뒤 정정해 두 판을 복원 가능하게 할 예정이다. 아직 후보 목적지 본문·릴리스·시험은 읽지 않았다.

## 공식 출발과 고정

공식 index의 숨은 목차 19행과 Reference 92행이 `key_projects`를 가리킨다. 앞의 overview/flow/tutorials는 목적/과정 설명이며, index에서 명시적으로 프로젝트 목록이라고 표시된 첫 대상은 key_projects다. `overview.rst`는 역할 확인을 위한 맥락으로 읽었고 주목록으로 교체하지 않았다.

- 주목록: https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst
- 저장소 commit: `5ecbc0db967843e64d55da165b72e773888860c5`, 시각 `2026-11-18T11:35:18Z`.
- 목록 blob: `f6e282f771705daf519195ead425bfb2a4d7374a`.
- 선언한 범위: Python 설치와 패키징의 주요 프로젝트를 소개하는 목록(8–9행). exhaustive 순위·현재 사용자 적합도 순위라고 하지 않는다.
- 적용한 순서: 파일의 실제 제목과 본문 링크 출현 순서. 대체로 프로젝트 이름이 알파벳순이지만 정렬 규칙으로 재정렬하지 않았다.
- 별도 공식 편집 규칙: https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/contribute.rst . 프로젝트 문서를 대체하지 않는 범위, 목적별 문서 역할, 독자 검색어를 고려한 제목, 교차링크 원칙을 확인했다.
- 이 목록판은 두 자연 요청보다 뒤다. 모두 **현재 재탐색**이며 2022년 당시 목록으로 부르지 않는다.

## 링크를 복원하는 고정 입력

`source/conf.py`의 intersphinx_mapping은 build·distlib·packaging·pipenv의 base를 선언하지만 각 `index`의 정확 URI는 선언하지 않는다. 네 objects.inv를 각각 직접 GET했으나 HTTP403이어서 `inventory-resolution.json`에 실패를 남겼다. 목적지 페이지를 열거나 index.html을 추정하지 않았다. 목록 `build:index`는 원순서 6위에 그대로 남기고 exact URL을 비웠다.

PyPI 역할은 목록의 requirements.txt가 sphinx-issues6.0.0을 고정한다. 해당 공급자 코드 `src/sphinx_issues/__init__.py` 134–151행의 URL 생성식을 직접 읽어 패키지명 뒤 trailing slash가 없는 정확 URL을 복원했다. 이것은 목록 렌더러 확인이며 후보 문서 열람이 아니다. renderer 버전은 후보의 제품판 필드에 넣지 않았다.

AWS S3는 목록 마지막의 named target 선언을 사용한다. 링크 출현은 31행이며 선언 위치가 뒤라는 이유로 순서를 뒤로 옮기지 않는다. Issues라는 이름으로 본문에 등재된 프로젝트 이슈 목록은 정보 링크로 보존한다. 실제 계정/후원/초대 UI는 link-exclusions.csv에 따로 둔다.

## 자연층

P-N1/P-N2 모두 동결한 기능명과 같은 제목 또는 명시적 별칭이 없다. `natural-match.csv`에 무매치를 기록했다. readme_renderer라는 제품명을 description/readme.md의 별칭이라고 만들지 않는다. 본문에 원하는 기능이 있다는 이유로 제목 매칭을 사후 확대하지 않는다. 관측된 후보 수는 두 풀 모두 **관측 0**이며, 도구 전반에 해결책이 없다는 뜻은 아니다.

## 보강층 잠정 v1

첫20 본문 제목의 parent 범위를 포함했다. `section-scan.csv` PY-H01은 조직 범주 PyPA Projects, PY-H02 이후는 프로젝트 절이다. PY-H01의 첫6 출현을 보존했다.

| 원순번·원장 ID | 원문 행 | 정보 링크 | 상류 | 결측 |
| --- | --- | --- | --- | --- |
| 1 · P-S1-U1 | 21 | https://bandersnatch.readthedocs.io | bandersnatch | 제품판·문서역할 미기재 |
| 2 · P-S1-U2 | 22 | https://github.com/pypa/bandersnatch/issues | bandersnatch | 제품판·문서역할 미기재 |
| 3 · P-S1-U3 | 23 | https://github.com/pypa/bandersnatch | bandersnatch | 제품판·문서역할 미기재 |
| 4 · P-S1-U4 | 24 | https://pypi.org/project/bandersnatch | bandersnatch | 제품판·문서역할 미기재 |
| 5 · P-S1-U5 | 31 | https://aws.amazon.com/s3/ | AWS S3 | 제품판·문서역할 미기재 |
| 6 · P-S1-U6 | 39 | `build:index` | build | exact URL 및 제품판·문서역할 미확인 |

A는 1/2/3, B는 1/5/6(숨은 형제2/3/4), C는 1/2/3이다. 정확하게 풀린 URL은 5개이고 나머지 하나는 결측이다. 4위는 같은 bandersnatch의 다른 정보 주소다. B로 앞으로 온 5위는 cloud storage, 6위는 빌드 frontend 문서 선언이다. 공급자/라벨 차이는 관측했으나 **선정된 사용자 목적을 충족하는 독립 구현이라는 판정은 미확인**이다.

미리 고정한 P-N1/P-N2 및 PP-575/576/577/583/588/1020/605/609 가운데 PyPI 미러·클라우드 파일 제공을 요구한 요청이 없다. 이 풀에 목적을 새로 붙이지 않는다. 주목록의 조직 제목이 broad하다는 이유로 editable/README 요구를 자동 연결하지 않는다. 목적 불일치인 메타데이터 기회를 완결 대안 양성으로 세지 않는다.

P-S2는 첫20 스캔에서 제품판이 없는 C 키를 합칠 수 없어 채우지 못했다. `latest`나 목록 SHA를 제품판으로 간주하지 않았다. 미선정은 C 기회 관측 0이며 후보 읽기에 실패한 결과와 구분한다.

## 사전 정정 예정과 감도

조직 범주를 기능 절에서 제외하면 첫 적격은 bandersnatch 절(18–35행)이다. 그 절은 정확 URL5개에서 소진되고 A/C=1/2/3, B=1/5이다. AWS S3 승격과 사용자 목적 미연결은 남고 build:index 6위는 풀 밖으로 사라진다. 변경은 목적지 열람 전에 별도 정정 커밋으로 보존해야 하며 잠정 v1을 덮어 결과를 먼저 본 것처럼 만들지 않는다.

설명 텍스트 자체는 재배포하지 않는다. pools.csv에는 출처 행, 글자 수, SHA256을 두고 A/B/C에서 같은 설명을 유지하는 계약을 고정했다. C의 다섯 필드 중 모르는 값은 빈칸이며, 목적지 내용으로 채우지 않는다.

## v2 사전 정정 — 기능 절 확정, 목적지 미열람

잠정 v1은 원격 `cd940aa340a5396611d028002ffc7150981f853a`에 보존되어 있다. 조직 범주가 기능 절인지에 대한 독립 검토를 반영하여 **표제 또는 절의 도입문이 독립적으로 판정할 처리 목적을 제시하는 절**을 기능 절로 정했다. 소유 조직 범주와 자기 안내 항목을 제외했다. 이 변경은 목적지를 열기 전에 이루어졌고 양성 결과에 따라 목록을 고른 것이 아니다.

- 원 제목순위1 PyPA Projects, 13 Python Packaging User Guide, 21 Non-PyPA Projects를 제외 사유와 함께 `functional-scan.csv`에 보존했다.
- 첫20 기능 절은 bandersnatch에서 conda까지다. 원 제목 순위와 기능 모집 순위를 각각 저장했다. 기존 제목을 합치거나 새 제목을 만들지 않았다.
- 주분석 P-S1은 bandersnatch 18–35행이며 첫5 정보 URL에서 **실제 소진**했다. 주소는 위 잠정 표의1–5와 정확히 같다. A/C 대표1/2/3, B 대표1/5 및 숨은 형제2/3/4다. B의 세 번째 자리는 없으며 invent하지 않는다.
- P-S2는 이20개 기능 절에서도 엄격 C 충돌이 없어 빈 자리로 유지했다. bare Docs/GitHub/Issues/PyPI 라벨만으로 문서 역할을 overview/reference 등으로 단정하지 않았다.
- 두 자연 슬롯은 같은 주목록의 제목·공식 별칭 무매치라 변하지 않는다.
- 목적 연결은 여전히 미확인이다. 모든 원문을 읽어도 미러 요구를 연구자가 만들면 사전 사용자 목적과 독립적이지 않다.
- 기존 부모6 링크는 `diagnostic-pools.csv`/`diagnostic-groups.csv`의 **D-P1 진단 확장**으로 따로 보존했다. 그 확장의 build:index URI 결측을 주분석5 URL의 접근 결측으로 전이하지 않는다.

`correct_catalog_v2.py`는 봉인된 v1 파일에서 v2 주분석/진단 파일을 만드는 재현 코드다. 원자료 캐시가 필요하며 네트워크·후보 실행을 하지 않는다. `build_catalog.py`는 v1 생성기이므로 v2 결과 위에서 재실행하지 않는다.
