# AF-RES-024 진행 기록

- 묶음 ①. 배정판·의존 보고서와 인계, T0 색인·태그, 모집단·정책·분모를 고정했다. 이 파일을 처음 추가한 커밋이 기준 묶음이다.
- 현재 접근 범위. 공식 2021년 T0 자료만 열었다. 이후 분기 관측은 시작 전이다.
- 다음 첫 행동. T0 태그 두 개의 색인에서 프레임을 추출하고, 뽑힌 이유를 당시 절에서 대조한 뒤 `cohort.csv`와 해시를 별도 커밋한다.
- 접근 제한. 현재 Python 공식 홈페이지·문서와 GitHub API는 셸 CONNECT 403이다. 버전 고정 Git과 raw를 기본으로 사용한다. Python.org 공개일은 웹 도구에서 확인한다.

- 묶음 ②. ①의 원격 SHA는 `da455ddbefb5310de8a8ec3492dfe1fcad9c78a0`이다. T0 원문 대조로 이유 64개와 입력 해시를 고정했다. 63개는 성립하고 Linux에서의 winreg 1개는 초기 오류다. 추출 프레임 CPython 4,038행·Node 2,443행, 상위 기능은 각각 208/46개다. 표본 확률과 추출 경계는 cohort.csv와 frame-exclusions.csv에 있다.
- ② 재생 입력. CPython 3.10.1 및 Node 17.3.0의 위 고정 커밋 codeload tar에서 해당 폴더를 풀고 `python -B docs/workstreams/research/AF-RES-024/cohort.py --t0-root /tmp/af-res-024-t0 --out /tmp/af-res-024-t0/rebuild --claims docs/workstreams/research/AF-RES-024/claims.json`을 실행한다.
- 표식 경계. 3.10 이전에 이미 제거된 항목을 설명하는 RST 표식은 현행 폐기층에서 제외했다. 관련 없는 하위 API 표식이 다른 모듈 구성원으로 넘어가지 않도록 모듈 도입부를 경계로 삼았다.
- 다음 첫 행동. 이 표본 해시와 커밋을 원격 ref에서 확인한 후 분기 정식판과 공개 날짜를 열고 2022Q1–Q3의 관측을 먼저 저장한다.
