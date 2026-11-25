# AF-RES-267 재현

원 실행기는 [AF-RES-249 고정 소스](receipts/original/verify_vectors.py)이다. [원 입력의 SHA256](receipts/original/SHA256SUMS)은 249 인계 커밋 `a61cee2b8882e79226f383217440ab71f2637f8c`에서 가져온 Git blob bytes를 대상으로 한다. [snapshots.csv](snapshots.csv)의 `source_url`, `case_url`, `checkpoint_url`이 각 원 행을 가리킨다. `source_utf8` 필드만 UTF-8로 다시 인코딩해 해당 프로세스의 `submission.py`를 만들었다. 같은 bytes인 스냅샷도 별도 파일과 프로세스였다.

## 정확판

이 실행은 Linux x86_64의 GitHub CPython 태그 `v3.12.0`, 태그 객체 `0fb6e700c2f94ae0717ee1be7d4e50b2dd480d14`, peeled commit `0fb18b02c8ad56299d6a2910be0bab8ad601ef24`에서 직접 빌드했다. `--version`은 `Python 3.12.0`, `sys.version_info=(3,12,0,'final',0)`, `sys.implementation.name=cpython`, 실행파일 SHA256은 `823adc445e057c565f905df18a7fa19dad1a21ec084f9be6a43ab4c79fdf6c23`. `bisect_right`는 `_bisect`의 C 함수였다. [환경 원행](receipts/r1/environment.json) · [빌드 명령·로그](receipts/build/commands.txt).

같은 패치판을 빌드하는 명령이다. 아래에서 `af_build`와 실행 폴더는 각각 새로 만든다.

```bash
set -eu
af_build=$(mktemp -d)
git clone --depth 1 --branch v3.12.0 --single-branch https://github.com/python/cpython.git "$af_build/cpython"
test "$(git -C "$af_build/cpython" rev-parse HEAD)" = 0fb18b02c8ad56299d6a2910be0bab8ad601ef24
(cd "$af_build/cpython" && ./configure --quiet --without-ensurepip && make -s -j5)
af_python="$af_build/cpython/python"
"$af_python" --version
"$af_python" -VV
sha256sum "$af_python"
```

동일 태그를 새로 컴파일하면 빌드 시각·경로·컴파일러 때문에 실행파일 지문이 달라질 수 있다. 이 보고서의 고정 바이너리를 사용할 때는 `--expected-python-sha256 823adc445e057c565f905df18a7fa19dad1a21ec084f9be6a43ab4c79fdf6c23`를 넘긴다. 새 바이너리는 자체 지문을 영수증에 남긴다. 실행 스크립트는 항상 CPython 구현·micro·final·serial까지 검사한다.

## 고정 결과에서 실행

이 저장소의 작업 브랜치를 받아 [HANDOFF.md](HANDOFF.md)에 기록된 **고정 결과 SHA**를 `af_pin`에 넣고 저장소 루트에서 실행한다. 아래 세 호출의 결과는 각각 새로운 디렉터리에 남는다.

```bash
set -eu
af_scope=docs/workstreams/research/AF-RES-267
af_archive=$(mktemp -d)
git archive "$af_pin" "$af_scope" | tar -xf - -C "$af_archive"
af_source="$af_archive/$af_scope"
(cd "$af_source/receipts/original" && sha256sum -c SHA256SUMS)
af_one=$(mktemp -d)
af_two=$(mktemp -d)
af_controls=$(mktemp -d)
"$af_python" -B -X utf8 "$af_source/replay.py" snapshots --out "$af_one" --work "$(mktemp -d)"
"$af_python" -B -X utf8 "$af_source/replay.py" snapshots --out "$af_two" --work "$(mktemp -d)" --compare-to "$af_one"
"$af_python" -B -X utf8 "$af_source/replay.py" controls --out "$af_controls" --work "$(mktemp -d)"
cmp "$af_one/snapshots.csv" "$af_two/snapshots.csv"
cmp "$af_one/vectors.csv" "$af_two/vectors.csv"
```

스냅샷 회차마다 실행기 12회/90벡터와 독립 판독 12회/90벡터를 호출한다. 통제 회차는 고장 하나씩 넣은 4개와 함수 예외 대조 1개이며 실행기 5회/39벡터, 판독 5회/39벡터다. 첫 번째 실행이 분석 대상이다. 두 번째는 첫 회차 고정 커밋의 Git archive를 읽어서 별도 빈 폴더로 재생했다. [r1 요약](receipts/r1/summary.json) · [r2 요약](receipts/r2/summary.json) · [r2 24쌍 비교](receipts/r2/replay-comparison.json) · [통제 요약](receipts/controls/summary.json).

- 개별 `runs/<slot>/<engine>/`에 원 byte `stdout.jsonl`·`stderr.txt`와 `receipt.json`이 있다. receipt에 argv, 시각, 시작 시 빈 폴더, 실행판·원·복사 뒤 지문, stdout/stderr SHA256, 프로세스 상태·exit가 있다. 부모 실행은 각 `launcher.*`와 `summary.json`, 실행판은 `environment.json`에서 읽는다.
- 실행기와 참조판은 별도 하위 프로세스에서 각기 빈 작업 폴더를 받았다. 실제 호출은 <code>python -I -B -X utf8 verify_vectors.py A|B submission.py</code>이고 환경은 `LC_ALL=C.UTF-8`, `TZ=UTC`, timeout 10초였다. `-I`와 작업 폴더는 경로·캐시 격리다. 여기에서 실행한 코드는 249 소스와 이 작업의 공개 합성 통제다.
- [reference.py](reference.py)는 실행기를 import하지 않는다. 자극 수기 정답을 옮겨 두고 A는 인접 key 경계와 slice, B는 첫 (key>x) 위치 또는 길이를 각각 계산했다. 함수 파일은 독립적으로 읽어 compile/exec했다. 입력·got·정확 타입·반환 뒤 상태·판정 및 예외 종류/메시지를 비교했다. 원 실행기의 `got`은 repr이므로 실제 반환형의 이름은 참조판 직접 호출을 출처로 표기했다.
- 변경 후 복원 통제에서 현재 Python 함수 frame의 line/return/exception 이벤트마다 같은 plain list의 투영을 읽었다. `append` 뒤와 `pop` 뒤가 서로 다른 소스 줄에서 기록된다. 같은 한 줄의 여러 연산이나 네이티브 코드 내부의 모든 중간 상태를 포괄하는 측정은 아니다.
- 상세 `vectors.csv`는 90행에 두 회차의 실행기·참조판 원행을 연결한다. 통제는 [별도 39행](receipts/controls/vectors.csv)이다. 참조판 일반 종료 0은 원행 생성 성공이고 개별 정답 여부는 `endpoint_pass`다. 테스트 실행기는 전체 벡터 통과 0, 하나 이상 실패 1이다. 예외 trace에는 임시 경로가 포함되어 raw SHA256이 새 폴더에서 바뀔 수 있다. 통제 예외의 비교 기준은 유형과 메시지다.
- 본 재생은 고정 CPython·합성 과제의 관측이다. 스냅샷 원장과 판정이 같은지 확인하는 데 쓰며, 운영 인수·참가자 작업시간·열람 자료는 이 실행에서 생성되지 않는다.
