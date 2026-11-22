# AF-RES-038 · pandas API 재현과 POC 재개 명령 — 미실시

## 현재 상태와 증명 범위

**이 파일의 명령과 replay_api_contracts.py는 이번 작업에서 실행하지 않았다. 패키지를 설치하지 않았다.** 아래는 후속 실행자가 결과·오류를 그대로 남길 수 있도록 만든 입력과 명령이다. 드라이버의 문법 검사, import 검사, unittest 실행도 아직 하지 않았다.

두 종류의 주장을 구분한다.

|주장|필요한 증거|현재 상태|
|---|---|---|
|선택한 버전의 API가 이 과제의 고정 입력에서 어떤 동작을 하는가|명시 버전 환경에서 driver JSON, stderr, wheel hash, 전체 freeze, 종료코드|미실시|
|그 환경이 실제 2022년 제안자·유지보수자의 환경과 같은가|당시 OS/architecture/compiler, Python patch, 전체 dependency closure, wheel/build 입력과 당시 실행 기록|복원 미확인|
|두 POC가 실제 pandas 전체 build/install을 통과했는가|각 source SHA, 당시 dependency closure, 개발·sdist 설치 양 경로의 실제 로그|미확인|
|사람의 품질·시간·재작업 효과|별도 사전 배정과 사람 시험 원자료|미실시; 이 driver가 계산하지 않음|

P04는 CPython **3.10.6**, pandas **1.4.4**를 고정한다. P06는 pandas **1.5.2**를 고정하고, 재현 명령의 interpreter도 비교를 쉽게 하도록 CPython **3.10.6**으로 선택한다. **P06의 실제 최초 제안자 Python patch가 3.10.6이었다는 자료는 없다.**

명령에서 NumPy **1.23.5**, python-dateutil **2.8.2**, pytz **2022.2.1**, six **1.16.0**은 *API 재현용으로 지금 선택하는 고정 의존판*이다. 당시 pandas 실행 환경의 lock으로 복구한 값이 아니다. 특히 P04의 historical dependency로 NumPy1.23.5를 소급하지 않는다. 읽은 [NumPy1.23.5 can_cast 원문](https://github.com/numpy/numpy/blob/v1.23.5/numpy/core/multiarray.py)은 API 설명일 뿐 당시 pandas environment 증거가 아니다. 이 조합의 설치 가능성과 결과도 실제 실행 전에는 미확인이다. 설치가 실패하면 버전을 조용히 바꾸지 말고 실패 로그와 제안할 새 lock을 별도 판으로 남긴다.

## 드라이버가 검사할 내용

드라이버는 표준 라이브러리 unittest를 사용한다. 테스트 대상 pandas/NumPy 외의 테스트 프레임워크는 필요 없다. --case로 두 환경을 분리하고 Python/pandas/NumPy의 실제 버전이 명령의 고정값과 다르면 테스트 전에 종료한다.

|사건|정상 계약 검사|알려진 잘못된 선택의 대조|
|---|---|---|
|P04|pandas explicit vector와 stdlib datetime.strptime loop가 같은 DMY 결과/오류; 첫 non-missing 한 번만 추론한 뒤 explicit format으로 고정하는 wrapper; MDY를 고정한 경우의 정당한 오류|pandas1.4.4 infer_datetime_format=True의 조용한 MDY→DMY 전환을 characterization과 expectedFailure로 구별|
|P06|native int64 앞단 lossless guard; 생성 때 명시한 nullable Int64 setter; 정수/whole float 수용, fractional/text 거부와 값·dtype 보존|guard 없는 기존 Series의 float/object 승격, NumPy의 1.5→1 truncation을 characterization과 expectedFailure로 구별|

strict-infer wrapper는 pinned private guess_datetime_format으로 format을 한 번 구한 뒤 public to_datetime에 explicit format으로 넘기는 **작성자 구성 구현**이다. pandas1.4.4 자체의 default가 이미 strict했다는 주장이 아니다. native guard도 pinned private np_can_hold_element 앞단을 작성자가 소비자 경계로 조합한 것이다. private helper가 사라지거나 import가 달라지면 무심코 대체하지 않는다.

P04의 모든 batch는 독립 입력이다.

- t0: ['01-01-2000 00:00:00', '02-01-2000 00:00:00']
- t1 batch1: ['12-01-2000 00:00:00', '13-01-2000 00:00:00']
- t1 batch2: ['12-01-2000 00:00:00', '01-13-2000 00:00:00']

P06는 Python 소스 literal로 int 4, float 2.0, float 3.0, float 1.5, str 'potage'를 보존한다. 각 t1 검사는 선언된 dtype의 [1,2,3] 독립 reset에서 시작한다. JSON에는 value_literal과 value_type을 쓴다. NA, overflow, bool, vector/slice, timezone, locale, 전체 추론 정확도는 검사하지 않는다.

근거 절:

- [P04 최초판](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md), Abstract·Motivation·Detailed Description.
- [pandas1.4.4 datetime source](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py), L31–35 guess helper import, L703–773 errors/format/inference.
- [CPython3.10.6 datetime docs](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst), L1035–1047 strptime.
- [P06 최초판](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md), Detailed description·fractional options.
- [pandas1.5.2 native guard](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py), L1931–2009.
- [pandas1.5.2 nullable setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py), L198–235; [원 테스트](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/tests/arrays/masked/test_indexing.py), L9–55.

## 정확한 API 재현 명령

전제: 저장소 root의 shell, 작동하는 Docker CLI/daemon, 공개 image·PyPI wheel에 접근 가능한 네트워크. 이 전제는 이번 작업에서 시험하지 않았다. Python image tag가 없거나 architecture가 실행되지 않으면 그 단계의 실패를 기록하고 멈춘다. 움직일 수 있는 image tag를 역사적 image라고 부르지 않는다. 아래 절차는 **이번에 내려받은 실제 image digest**를 고정하고 inspect 결과를 저장한다.

### 1. 출력 경로와 interpreter image 고정

```sh
AF038_ROOT="$(pwd)/docs/workstreams/research/AF-RES-038"
AF038_RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
AF038_OUT="$AF038_ROOT/evidence/api-replay-$AF038_RUN_ID"
AF038_DRIVER="$AF038_ROOT/streams/pandas"
mkdir -p "$AF038_OUT"

docker pull --platform linux/amd64 python:3.10.6-slim
docker image inspect python:3.10.6-slim > "$AF038_OUT/python-image-inspect.json"
AF038_IMAGE="$(docker image inspect --format '{{index .RepoDigests 0}}' python:3.10.6-slim)"
printf '%s\n' "$AF038_IMAGE" > "$AF038_OUT/python-image-digest.txt"
```

복구된 historical image digest가 아니다. digest가 비어 있으면 다음 명령을 실행하지 않는다. 드라이버는 Python patch가 정확히 3.10.6인지도 별도로 확인한다. 새 run directory를 사용하므로 이전 report를 덮어쓰지 않는다.

### 2. P04 — pandas1.4.4 / Python3.10.6

```sh
if docker run --rm --platform linux/amd64 \
  --mount type=bind,source="$AF038_DRIVER",target=/driver,readonly \
  --mount type=bind,source="$AF038_OUT",target=/out \
  "$AF038_IMAGE" sh -eu -c '
    mkdir -p /out/P04/wheels
    python -m pip download --only-binary=:all: --no-deps \
      --dest /out/P04/wheels \
      numpy==1.23.5 pandas==1.4.4 python-dateutil==2.8.2 pytz==2022.2.1 six==1.16.0
    sha256sum /out/P04/wheels/* > /out/P04/wheels.sha256
    python -m pip install --no-index --no-deps --find-links /out/P04/wheels \
      numpy==1.23.5 pandas==1.4.4 python-dateutil==2.8.2 pytz==2022.2.1 six==1.16.0
    python -m pip check > /out/P04/pip-check.txt
    python -m pip freeze --all > /out/P04/freeze.txt
    python -B /driver/replay_api_contracts.py \
      --case P04 --expected-numpy 1.23.5 --report /out/P04/report.json
  ' > "$AF038_OUT/P04-container.log" 2>&1
then
  printf '0\n' > "$AF038_OUT/P04-container.exitcode"
else
  AF038_P04_EXIT=$?
  printf '%s\n' "$AF038_P04_EXIT" > "$AF038_OUT/P04-container.exitcode"
fi
```

### 3. P06 — pandas1.5.2 / 동일하게 선택한 interpreter

```sh
if docker run --rm --platform linux/amd64 \
  --mount type=bind,source="$AF038_DRIVER",target=/driver,readonly \
  --mount type=bind,source="$AF038_OUT",target=/out \
  "$AF038_IMAGE" sh -eu -c '
    mkdir -p /out/P06/wheels
    python -m pip download --only-binary=:all: --no-deps \
      --dest /out/P06/wheels \
      numpy==1.23.5 pandas==1.5.2 python-dateutil==2.8.2 pytz==2022.2.1 six==1.16.0
    sha256sum /out/P06/wheels/* > /out/P06/wheels.sha256
    python -m pip install --no-index --no-deps --find-links /out/P06/wheels \
      numpy==1.23.5 pandas==1.5.2 python-dateutil==2.8.2 pytz==2022.2.1 six==1.16.0
    python -m pip check > /out/P06/pip-check.txt
    python -m pip freeze --all > /out/P06/freeze.txt
    python -B /driver/replay_api_contracts.py \
      --case P06 --expected-numpy 1.23.5 --report /out/P06/report.json
  ' > "$AF038_OUT/P06-container.log" 2>&1
then
  printf '0\n' > "$AF038_OUT/P06-container.exitcode"
else
  AF038_P06_EXIT=$?
  printf '%s\n' "$AF038_P06_EXIT" > "$AF038_OUT/P06-container.exitcode"
fi
```

--only-binary는 현재 선택 환경에서 이용 가능한 wheel을 요구한다. wheel이 없다고 source build나 다른 판으로 자동 fallback하지 않는다. 다운로드된 wheel은 SHA-256과 함께 보존하고 해당 실제 바이트를 다음 재현의 입력으로 사용한다. 설치·import가 실패했으면 테스트를 실행한 것으로 세지 않는다.

### 4. 결과 해석과 종료코드

|드라이버 종료|뜻|후속 기록|
|---|---|---|
|0|정상 대안 검사와 characterization이 맞고 정해 둔 expectedFailure가 재현됨|API replay 관측으로 추가. historical equivalence·사람 효과는 계속 미확인|
|1|정상 검사 실패, 오류, expectedFailure 수 불일치 또는 unexpectedSuccess|원 결과를 보존하고 차이·버전·입력을 조사. 기대를 성공하도록 소급 수정하지 않음|
|2|버전 불일치, import/환경 차단, CLI/기존 report 경로 오류|환경 차단으로 기록. tests_executed=false 또는 report 미생성|

Docker의 image/download/install 단계 실패는 드라이버 종료와 다를 수 있다. container.exitcode와 container.log를 함께 읽어 어느 단계까지 실행됐는지 판정한다. report가 없다는 이유만으로 API 실패라고 코딩하지 않는다.

P04에서 요구한 expectedFailure는 1건, P06은 3건이다. 이는 **잘못된 선택이 계약에 실패한다는 대조**다. 성공 대안 수에 합산하지 않는다. 드라이버는 그 실제 잘못된 출력도 별도의 ordinary characterization test에서 확인하므로 아무 예외나 발생했다는 이유만으로 expectedFailure 재현 성공이라고 부르지 않는다.

## P02 — POC의 움직이는 의존부터 확인하기

아래 역시 **미실시 명령**이다. pandas 전체 빌드를 시작하기 전에 source와 dependency closure를 구분한다. 원문에서 확인한 고정 입력:

|입력|고정 SHA|읽을 위치|복원 한계|
|---|---|---|---|
|CMake pandas POC|d62f894c3ec08b721de0499cabe2c58a6e322496|build_support/build_backend.py, pyproject.toml, CMakeLists.txt|cmake/setuptools/wheel/Cython/numpy 의존은 완전 lock이 아님|
|Meson pandas POC|7e401dc31ca155fcc7b3128ee7a7b43989c71da3|meson.build, pyproject.toml|meson-python을 git+...@main으로 참조; 그때 resolved commit 미확인|
|당시 공개된 meson-python0.7.0|2f9acf25e23de95b0ceead72770cad4acf19a449|README.md, mesonpy/__init__.py|당시 사용 가능했던 released 후보이지 POC @main이 실제 가리킨 commit이라는 증거 아님|

[CMake POC wrapper](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py)는 compile 후 packaging을 위임한다. [Meson POC pyproject](https://github.com/lithomas1/pandas/blob/7e401dc31ca155fcc7b3128ee7a7b43989c71da3/pyproject.toml)는 움직이는 VCS 요구를 실제 포함한다. [0.7.0 README](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md)의 platform 한계도 유지한다.

### source 읽기와 의존 확인 명령

위 공통 경로 변수를 사용한다. fetch 이후에도 이 단계에서는 build/install을 하지 않는다.

```sh
mkdir -p "$AF038_OUT/P02"

git init "$AF038_OUT/P02/cmake-poc"
git -C "$AF038_OUT/P02/cmake-poc" remote add origin https://github.com/pandas-dev/pandas.git
git -C "$AF038_OUT/P02/cmake-poc" fetch --depth=1 origin d62f894c3ec08b721de0499cabe2c58a6e322496
git -C "$AF038_OUT/P02/cmake-poc" rev-parse FETCH_HEAD
git -C "$AF038_OUT/P02/cmake-poc" show d62f894c3ec08b721de0499cabe2c58a6e322496:pyproject.toml
git -C "$AF038_OUT/P02/cmake-poc" show d62f894c3ec08b721de0499cabe2c58a6e322496:build_support/build_backend.py

git init "$AF038_OUT/P02/meson-poc"
git -C "$AF038_OUT/P02/meson-poc" remote add origin https://github.com/lithomas1/pandas.git
git -C "$AF038_OUT/P02/meson-poc" fetch --depth=1 origin 7e401dc31ca155fcc7b3128ee7a7b43989c71da3
git -C "$AF038_OUT/P02/meson-poc" rev-parse FETCH_HEAD
git -C "$AF038_OUT/P02/meson-poc" show 7e401dc31ca155fcc7b3128ee7a7b43989c71da3:pyproject.toml
git -C "$AF038_OUT/P02/meson-poc" show 7e401dc31ca155fcc7b3128ee7a7b43989c71da3:meson.build

git init "$AF038_OUT/P02/backend-candidate"
git -C "$AF038_OUT/P02/backend-candidate" remote add origin https://github.com/mesonbuild/meson-python.git
git -C "$AF038_OUT/P02/backend-candidate" fetch --depth=1 origin 2f9acf25e23de95b0ceead72770cad4acf19a449
git -C "$AF038_OUT/P02/backend-candidate" rev-parse FETCH_HEAD
git -C "$AF038_OUT/P02/backend-candidate" show 2f9acf25e23de95b0ceead72770cad4acf19a449:README.md
```

### 실제 @main resolution을 찾을 첫 공개 기록

```sh
curl --fail --silent --show-error \
  'https://api.github.com/repos/lithomas1/pandas/commits/7e401dc31ca155fcc7b3128ee7a7b43989c71da3/check-runs' \
  > "$AF038_OUT/P02/meson-poc-check-runs.json"

curl --fail --silent --show-error \
  'https://api.github.com/repos/lithomas1/pandas/issues/19/comments?per_page=100' \
  > "$AF038_OUT/P02/meson-poc-discussion-page1.json"

curl --fail --silent --show-error \
  'https://api.github.com/repos/lithomas1/pandas/pulls/19/comments?per_page=100' \
  > "$AF038_OUT/P02/meson-poc-review-comments-page1.json"
```

먼저 해당 commit의 당시 CI 로그·pip freeze·VCS resolved commit·lockfile이 남아 있는지 확인한다. API 페이지에 next가 있으면 후속 페이지도 저장하고 조회 범위를 적는다. 오래된 로그가 소실되었거나 resolved SHA를 찾을 수 없으면 **당시 @main dependency 복원 미확인**으로 종료한다. 현재 main의 SHA, 과거 날짜로 필터한 commit, 0.7.0 release SHA 가운데 하나를 원래 resolution이라고 자동 채택하면 안 된다. 후속 연구자가 released backend를 새로 고르면 별도 API/build replay 조건이며 원래 환경의 재현 성공이 아니다.

CMake 쪽도 같은 원칙으로 당시 compiler, Python patch, CMake, setuptools, wheel, Cython, NumPy의 전체 resolved 버전을 찾는다. ranges만 있는 pyproject로 원래 환경을 복구했다고 하지 않는다.

잠금이 확인된 뒤 검사할 입력과 종점은 다음과 같다.

- 입력: 위 source commit, 확인한 전체 dependency lock와 wheel/source hashes, OS/architecture/compiler, 동일 native target/dependency graph, 동일 worker 설정.
- 개발 경로: graph의 configure/compile 호출과 worker 전달을 실제 로그로 확인.
- source-install 경로: source archive를 clean directory에 풀고 표준 frontend→backend→동일 native graph로 연결되는지 확인.
- 산출: native artifact, wheel의 파일명/metadata, sdist 필수 graph·source·backend 입력 및 import 결과.
- 판정: P02-R1/R2/R3별 동일 원래 요구의 합치성. 파일 수/이름, packaging 위임 또는 후대 Meson 채택만으로 합격/탈락시키지 않는다.
- 시간: software 로그가 있더라도 사람 노동이나 링크/설명 처치 효과로 환산하지 않는다.

## HANDOFF용 현재 한 줄

P04/P06의 재현 driver와 입력·명령을 작성했으나 설치·문법검사·API 실행은 미실시다. P02는 고정 POC source와 움직이는 dependency 확인 경로만 제공하며, 당시 closure와 전체 build 성공은 미확인이다.

