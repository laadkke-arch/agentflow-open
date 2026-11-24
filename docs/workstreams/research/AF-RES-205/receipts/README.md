# 원영수증과 재현

`runtime.json`의 Linux x86_64 CPython 3.11.15로 하류 wheel과 독립 venv를 검사했다. venv의 pip는 24.0이었다. `verify-wheels.json`은 게시자 JSON·wheel·태그·ZIP RECORD·구간 지문 대조 명령의 종료코드와 원출력이다. `setup.jsonl`은 venv 생성, pip 판, 정상 설치/resolver, freeze, check, import를 실제 명령 순으로 보존한다. 성공 시 `install-hashes.json`은 pip report의 해시와 받은 wheel URL·해시·해결판을 보존한 추출본이고, `requirements.lock`은 그 설치를 다시 실행하는 입력이다. 긴 pip report 원본은 당시 임시 환경에 저장됐고 저장소에는 resolver의 원 stdout/stderr와 추출본을 보존했다. `runs.jsonl`에는 별도 프로세스의 명령, 종료코드, stdout, stderr가 그대로 들어 있다. 중첩된 stdout은 원문 JSON 한 줄이다.

```sh
AF205_DIR="$(git rev-parse --show-toplevel)/docs/workstreams/research/AF-RES-205"
AF205_TMP="$(mktemp -d)"
AF205_PY="$(command -v python3.11)"
"$AF205_PY" -VV
"$AF205_PY" "$AF205_DIR/probe.py" run \
  --work "$AF205_TMP/work" --output "$AF205_TMP/receipts" \
  --locks "$AF205_DIR/receipts" --jobs 4
```

`--locks`를 빼면 원시험처럼 하류 wheel 파일과 NumPy/PyArrow 정확 핀을 주고 pip가 보조 의존성을 해결한다. A02는 lock이 없으므로 동일한 정확 핀을 정상 resolver에 다시 주고 충돌을 기록한다. 모든 다운로드·설치는 `--work` 아래에서 이뤄진다. `inputs.json`의 JSON 키는 환경과 합성 입력의 기준이며 A1/A2/A4는 `arange(10.0)`과 같은 값을 명시한 배열에서 시작한다. 본 NumPy·하류판과 함께 각 venv의 보조 의존성도 lock으로 고정할 수 있다.

각 프로세스는 설치된 패키지의 공개 호출을 한 번 실행한다. 결과가 반환되면 exit 0, 그 호출이 예외를 던지면 traceback과 함께 exit 10이다. 환경 차단 상태는 `state.json`과 해당 setup 행을 연결한다. 반복은 PID가 다르고 원본 값과 관측 필드가 같은지 확인한다. Arrow null의 NaN은 유효 JSON을 위해 `{"nonfinite":"NaN"}`으로 기록한다. H1의 원버퍼 reference는 단일 Arrow chunk의 zero-copy ndarray이고 H2–H4의 물리 buffer 검사는 구성 요소 수준이다. 관측하지 않은 공유나 전파는 JSON `null`이다.

잠금 재생을 마친 뒤 같은 작업 경로에서 보강 시험을 실행한다.

```sh
"$AF205_PY" "$AF205_DIR/controls.py" collect \
  --work "$AF205_TMP/work" --output "$AF205_TMP/controls.jsonl"
```

`controls.jsonl` 56행에는 독립 사본·가변/읽기전용 view 대조, 직접 NumPy/Arrow, Linux 매핑, Datasets 중간 list trace, Astropy implicit dtype 대조의 원출력이 있다. `replay-check.json`은 별도 디렉터리의 잠금 재생에서 확인한 전체 설치 파일 해시, 원출력 및 stderr 일치 검사 요약이다. PID와 두 임시 경로를 표준화해 비교했다. 기본 주표본에 해당하는 원출력 자체는 각 환경의 `runs.jsonl`이고 이 요약에는 반복 원출력의 지문과 상태를 보관했다. `tag-refs.json`은 GitHub 태그 이름과 고정 커밋의 대응을 다시 읽은 기록이다.

작업 환경에서 3.11.15는 uv 0.13.6의 `uv python install 3.11.15 --no-bin`으로 확보했다. `UV_CACHE_DIR`와 `UV_PYTHON_INSTALL_DIR`에는 각각 임시 경로를 쓸 수 있다. 메인 버전, 각 subprocess의 명령, pip 및 코드/입력 지문은 영수증에 있다.
