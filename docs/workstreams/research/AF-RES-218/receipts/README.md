# AF-RES-218 재현과 영수증

실행은 Linux x86_64의 CPython 3.11.15, pip 24.0 및 [A01 해시 잠금](../requirements.lock)을 사용했다. 다른 Python ABI의 wheel 대신 선행 실측과 같은 W03을 설치한다. 아래 명령은 클라우드 checkout에서 실행한다.

```sh
AF218_DIR="$(git rev-parse --show-toplevel)/docs/workstreams/research/AF-RES-218"
AF218_TMP="$(mktemp -d /tmp/af-res-218.XXXXXXXX)"
export UV_CACHE_DIR="$AF218_TMP/uv-cache"
export UV_PYTHON_INSTALL_DIR="$AF218_TMP/uv-python"
uv python install 3.11.15 --no-bin
AF218_BASE_PY="$(uv python find --managed-python 3.11.15)"
"$AF218_BASE_PY" -m venv "$AF218_TMP/venv"
AF218_PY="$AF218_TMP/venv/bin/python"
"$AF218_PY" -m pip --isolated install --index-url https://pypi.org/simple \
  --require-hashes --only-binary=:all: --report "$AF218_TMP/install-report.json" \
  -r "$AF218_DIR/requirements.lock"
"$AF218_PY" -m pip check
"$AF218_PY" -E -s -B "$AF218_DIR/probe.py" run matrix --work "$AF218_TMP/matrix-work" \
  --output "$AF218_TMP/matrix-out" --jobs 4
cmp "$AF218_TMP/matrix-out/baseline.fits" "$AF218_DIR/receipts/baseline.fits"
"$AF218_PY" -E -s -B "$AF218_DIR/reopen.py" "$AF218_TMP/matrix-work/baseline.fits" --hdu 0 --pixel 0
```

원경로는 각 사례의 `original.fits`다. `before_flush_or_close`는 쓰기 직후 writer가 연 상태, `after_flush`는 명시 호출을 실행한 직후, `after_hdul_close`는 writer가 아직 살아 있는 상태, `after_writer_exit`는 상위 프로세스가 writer 종료코드를 받은 뒤다. 각 reader는 `memmap=False`와 읽기 전용 디스크 파일 핸들을 사용한다. Astropy에서 읽은 픽셀과 별도로 `struct.unpack(">d", …)`로 원바이트를 해석한다. 디렉터리 경로와 프로세스 ID는 새 실행마다 바뀐다.

| 기록 | 판독 위치 |
| --- | --- |
| [baseline.fits](baseline.fits), [baseline-reader.json](baseline-reader.json) | 매번 재생성해 고정 SHA를 확인하는 원본 사본과 독립 reader 출력 |
| [setup.jsonl](setup.jsonl), [wheel-check.json](wheel-check.json), [runtime.json](runtime.json) | 설치와 실행 명령, 설치된 배포물 지문, 모듈 위치·코드 지문 및 파일시스템 종류 |
| [preflight.json](preflight.json) | 네이티브 float64와 big-endian 힙, 별도 FITS 매핑 예비 양성 |
| [matrix.jsonl](matrix.jsonl) 및 [persistence.csv](../persistence.csv) | 사례별 합성 원파일, writer 원출력(각 경계의 reader 영수증을 포함), 종료 후 reader 원출력 및 그 집계 |
| [matrix-command.jsonl](matrix-command.jsonl) | 실제 suite 명령의 UTC·종료코드·stdout/stderr |
| [controls.jsonl](controls.jsonl), [controls.csv](controls.csv), [controls-command.jsonl](controls-command.jsonl) | 별도 FITS 사본 6건의 원출력·집계·명령 |
| [sqlite-command.jsonl](sqlite-command.jsonl), [signatures.jsonl](signatures.jsonl) | SQLite 공식 사례의 합성 재생과 로드된 Astropy API 서명 |

같은 영수증에서 별도 프로세스로 독립 reader 순서를 확인하고 CSV 분류를 재생한다.

```sh
"$AF218_PY" -E -s -B "$AF218_DIR/probe.py" replay matrix --receipts "$AF218_DIR/receipts" \
  --output "$AF218_TMP/persistence.replay.csv"
cmp "$AF218_DIR/persistence.csv" "$AF218_TMP/persistence.replay.csv"
```

FITS 통제와 SQLite 비교는 각자의 임시 폴더에서 실행한다.

```sh
"$AF218_PY" -E -s -B "$AF218_DIR/probe.py" run controls --work "$AF218_TMP/controls-work" \
  --output "$AF218_TMP/controls-out" --jobs 4
"$AF218_PY" -E -s -B "$AF218_DIR/probe.py" replay controls --receipts "$AF218_DIR/receipts" \
  --output "$AF218_TMP/controls.replay.csv"
cmp "$AF218_DIR/receipts/controls.csv" "$AF218_TMP/controls.replay.csv"
"$AF218_PY" -E -s -B "$AF218_DIR/receipts/sqlite_probe.py" --work "$AF218_TMP/sqlite-work"
```

205에서 받은 공개 자료 P01–P11은 [출처 원장](../sources.jsonl)에 고정 링크로 보존한다. 여기의 기준 FITS, writer/reader 원출력과 통제는 AF-RES-218에서 생성했다.
