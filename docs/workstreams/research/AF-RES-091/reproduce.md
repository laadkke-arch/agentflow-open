# AF-RES-091 재현

## 087 N과 같은 환경 잠금

저장소 루트와 Python 3.12.14/Linux x86-64에서 실행한다. 원 087 requirements와 휠 bytes 23개, GeoPandas source SHA와 import의 실제 코드 지문이 일치해야 writer가 실행된다. [AF-RES-087 원 설치 영수증](https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/evidence/build/installation.json) · [091 실제 환경](environments.json).

```sh
af091_work="$PWD/docs/workstreams/research/AF-RES-091"
af091_lab="$(mktemp -d /tmp/af091-replay.XXXXXX)"
af091_src="$af091_lab/geopandas"
af091_build="$af091_lab/build"
af091_read="$af091_lab/read"
af091_prev="263fe7581cf45eadd1f05139aacaadb27290b86e"
af091_prevpath="docs/workstreams/research/AF-RES-087"
mkdir -p "$af091_lab/wheels"

git fetch origin refs/heads/work/research-af-res-087
git show "$af091_prev:$af091_prevpath/requirements.txt" > "$af091_lab/requirements.txt"
git show "$af091_prev:$af091_prevpath/environments.json" > "$af091_lab/environments-087.json"
git show "$af091_prev:$af091_prevpath/evidence/build/installation.json" > "$af091_lab/installation-087.json"
git clone --depth=1 --branch v1.0.0 https://github.com/geopandas/geopandas.git "$af091_src"
test "$(git -C "$af091_src" rev-parse HEAD)" = d8e14e1be3ecbef6f75a1142f85561ff652ed3d1

python -m pip download --only-binary=:all: --dest "$af091_lab/wheels" \
  --requirement "$af091_lab/requirements.txt" pip==24.1.2 setuptools==70.1.1 wheel==0.43.0
python -m venv "$af091_lab/venv"
af091_py="$af091_lab/venv/bin/python"
"$af091_py" -m pip install --no-index --find-links "$af091_lab/wheels" pip==24.1.2 setuptools==70.1.1 wheel==0.43.0
"$af091_py" -m pip install --no-index --find-links "$af091_lab/wheels" --requirement "$af091_lab/requirements.txt"
"$af091_py" -m pip install --no-index --no-build-isolation --no-deps -e "$af091_src"
"$af091_py" -m pip check
```

## 쓰기, footer, 읽기

```sh
"$af091_py" -B "$af091_work/fixtures/build.py" "$af091_build" "$af091_src" "$af091_lab/wheels" \
  "$af091_lab/installation-087.json" "$af091_lab/environments-087.json"

# The committed bytes and writer receipts are the read inputs.
"$af091_py" -B "$af091_work/fixtures/read_matrix.py" matrix "$af091_work" "$af091_read" "$af091_src"

# To compare fresh writer output rather than committed bytes, use a separate output folder.
"$af091_py" -B "$af091_work/fixtures/read_matrix.py" matrix "$af091_build" "$af091_lab/read-generated" "$af091_src"
```

고정 입력은 [inputs.json](fixtures/inputs.json)이다. writer 전 기록과 [files.csv](files.csv)의 file·footer 해시를 새 실행과 대조한다. GeoParquet의 `schema_version=1.1.0`과 Parquet의 `version=2.6`은 다른 인수다. 입출력은 서로 다른 경로에 두고 새 디렉터리를 사용한다. [inspect_parquet.py](fixtures/inspect_parquet.py)는 별도 PyArrow 프로세스다. reader는 각 회차마다 동일 SHA를 확인한 메모리 bytes를 `gpd.read_parquet`에 전달한다. 별도 bbox/filters 지정 없이 전체를 읽은 뒤 정렬한 T/P ID·score를 계산한다. [원 reader와 실패 자리](runs.jsonl) · [reader 병합 집계](evidence/read/summary.json).

단일 자리의 같은 bytes 재열람 예다.

```sh
af091_original_sha="$(sha256sum "$af091_work/fixtures/S0-original.json" | cut -d' ' -f1)"
"$af091_py" -B "$af091_work/fixtures/read_matrix.py" read "$af091_src" \
  "$af091_work/fixtures/S0-native.parquet" 9dcc45e8fe3313265336484882ad64e5762eedbd267cfb7a86d69a177fc39911 \
  "$af091_work/fixtures/S0-original.json" "$af091_original_sha" 1
```

실제 프로세스 exit 0은 읽기와 비교 관측까지 완료한 경우다. 19는 파일 확인 또는 reader 호출 전 harness 오류, 20은 read 예외, 21은 read 성공 뒤 observer 오류에 배정했다. writer가 거절한 자리에는 파일 SHA·PID·종료코드가 없고 원 writer traceback에 연결된다. 첫 환경 검사는 Pyogrio의 tuple accessor를 087의 문자열과 비교해서 실패했다. 동일 accessor를 적용한 뒤 입력·휠 해시 변경 없이 처음 writer를 실행했다. [환경 preflight](evidence/build/preflight.json) · [GeoSeries.notna 경고](evidence/build/original-query-warning.txt) · [writer 예외](evidence/build/S1-native-writer.json).

## 통제 밖 대조와 원 시험

```sh
"$af091_py" -B "$af091_work/fixtures/auxiliary.py" "$af091_lab/auxiliary" "$af091_src"
"$af091_py" -B "$af091_work/fixtures/type_alias.py" \
  "$af091_work/evidence/auxiliary/S1-drop-E.parquet" "$af091_lab/type-alias.json" "$af091_src"
```

S1의 N 제거, E 제거, E 교체 및 S2/S3의 E 제거는 주 파일과 다른 입력이다. 원 4입력의 Shapely ragged 배열 관측에는 추가 Parquet 쓰기가 없다. `type_alias`는 보조 S1-drop-E의 원 타입을 두 유효 행에서 맞바꾼 뒤 동일 파일이 생기나 확인한다. [옆 대조와 bytes](evidence/auxiliary) · [동일 bytes 원 출력](evidence/auxiliary/type-alias.json).

다음은 087 N과 독립인 추가 venv다. Dask 호출에 사용하는 v0.5.0 wheel에서 `expr.py`가 고정 Git source와 같은 bytes인지도 확인한다. Q7의 Pillow 및 Arrow 원 시험은 아래 버전에서 실시했다.

```sh
python -m venv "$af091_lab/external"
af091_ext="$af091_lab/external/bin/python"
"$af091_ext" -m pip install --no-index --find-links "$af091_lab/wheels" pip==24.1.2 setuptools==70.1.1 wheel==0.43.0
"$af091_ext" -m pip install --no-index --find-links "$af091_lab/wheels" --requirement "$af091_lab/requirements.txt"
"$af091_ext" -m pip install --no-index --no-build-isolation --no-deps -e "$af091_src"
"$af091_ext" -m pip install --only-binary=:all: --constraint "$af091_lab/requirements.txt" \
  'dask[dataframe]==2025.5.1' dask-geopandas==0.5.0 pillow==11.3.0 \
  cloudpickle==3.1.3 fsspec==2026.9.0 locket==1.0.0 partd==1.4.2 pyyaml==6.0.4 toolz==1.2.0 \
  hypothesis==6.103.1 sortedcontainers==2.4.0
"$af091_ext" -m pip check
git clone --depth=1 --branch v0.5.0 https://github.com/geopandas/dask-geopandas.git "$af091_lab/dask-geopandas"
git clone --depth=1 --branch apache-arrow-16.1.0 https://github.com/apache/arrow.git "$af091_lab/arrow"
git clone --depth=1 --branch 11.3.0 https://github.com/python-pillow/Pillow.git "$af091_lab/pillow"

"$af091_ext" -B "$af091_work/fixtures/consumer_controls.py" "$af091_work" \
  "$af091_lab/consumer-controls.json" "$af091_lab/dask-geopandas"
"$af091_ext" -B "$af091_work/fixtures/representation_controls.py" "$af091_lab/representation-controls.json"

af091_arrowtest="$af091_lab/external/lib/python3.12/site-packages/pyarrow/tests/test_pandas.py"
cmp "$af091_arrowtest" "$af091_lab/arrow/python/pyarrow/tests/test_pandas.py"
"$af091_ext" -B -m pytest -c /dev/null -p no:cacheprovider -q \
  "${af091_arrowtest}::test_array_protocol" "${af091_arrowtest}::test_convert_to_extension_array"
(
  cd "$af091_lab/pillow"
  "$af091_ext" -B -m pytest -c /dev/null -p no:cacheprovider -q \
    Tests/test_image.py::TestImage::test_remap_palette \
    Tests/test_image.py::TestImage::test_remap_palette_transparency \
    Tests/test_file_png.py::TestFilePng::test_save_p_single_transparency
)
(
  cd "$af091_lab/dask-geopandas"
  "$af091_ext" -B -m pytest -c /dev/null -p no:cacheprovider -q --noconftest \
    dask_geopandas/tests/test_sjoin.py::test_no_value_error
)
```

출처는 [원장](sources.jsonl)과 [원문 증빙](evidence/source-reads.jsonl)을 함께 읽는다. Git 원문의 line spans와 SHA-256은 `git show SHA:path`의 bytes에서 계산한다. 공식 PDF/HTML의 원 bytes 다운로드가 제한된 경우에는 원문 페이지·절과 식별 값을 남겼다. [별도 하류 호출](evidence/external/consumer-execution.json) · [Q7 원 출력](evidence/external/representation-controls.json) · [원 pytest 및 첫 Arrow conftest 오류](evidence/external/upstream-tests.json). AF-RES-087의 사례/원 시험과 이번 격자는 따로 둔다.

## 계약과 결과 검사

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-091/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B docs/workstreams/research/AF-RES-091/audit.py
```

원격에서 결과 커밋을 별도로 가져와 체크아웃한 뒤 명령을 적용한다. 실제 검사 SHA와 종료값은 마지막 인계에 있다.
