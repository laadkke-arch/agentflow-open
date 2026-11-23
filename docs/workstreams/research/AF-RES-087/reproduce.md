# AF-RES-087 재현

## 입력 고정 및 재구성 환경

저장소 루트에서 시작한다. 두 venv가 동일 CPython 3.12.14와 휠을 썼다. Python과 OS가 다르면 먼저 새 지문을 적는다. 원 배포자의 과거 설치판은 미확인이다. 검증된 패키지 hash와 import 파일은 [installation](evidence/build/installation.json) 및 [environments](environments.json)에 있다. 패키지 설치와 업스트림 checkout은 연구 디렉터리 외 임시 공간에 두었다.

```sh
af_work="$PWD/docs/workstreams/research/AF-RES-087"
af_replay_root="$(mktemp -d /tmp/af087-replay.XXXXXX)"
af_lab="$af_replay_root/lab"
af_out="$af_replay_root/result"
mkdir -p "$af_lab/wheels" "$af_out"
git init "$af_lab/geopandas"
git -C "$af_lab/geopandas" fetch --depth=1 https://github.com/geopandas/geopandas.git \
  refs/tags/v0.14.4:refs/tags/v0.14.4 refs/tags/v1.0.0:refs/tags/v1.0.0
git -C "$af_lab/geopandas" worktree add --detach "$af_lab/src-O" v0.14.4
git -C "$af_lab/geopandas" worktree add --detach "$af_lab/src-N" v1.0.0
git -C "$af_lab/src-O" rev-parse HEAD
git -C "$af_lab/src-N" rev-parse HEAD

python -m pip download --only-binary=:all: --dest "$af_lab/wheels" \
  --requirement "$af_work/requirements.txt" pip==24.1.2 setuptools==70.1.1 wheel==0.43.0
for af_role in O N; do
  python -m venv "$af_lab/venv-$af_role"
  af_py="$af_lab/venv-$af_role/bin/python"
  "$af_py" -m pip install --no-index --find-links "$af_lab/wheels" pip==24.1.2 setuptools==70.1.1 wheel==0.43.0
  "$af_py" -m pip install --no-index --find-links "$af_lab/wheels" --requirement "$af_work/requirements.txt"
  "$af_py" -m pip install --no-index --no-build-isolation --no-deps -e "$af_lab/src-$af_role"
  "$af_py" -m pip check
done
```

O HEAD `60c9773e44fff8a35344c2a74431e00c5546a4ee` 및 N HEAD `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1`을 고정한다. 코드가 import한 파일·Git SHA·깨끗한 tracked source를 확인한다. [공통 논리 입력](fixtures/input.json), 두 판정과 예측은 [봉인 계획](SCOPE.md)에 있다. `version=2.6`은 Parquet 인수이고 GeoParquet 판은 `schema_version`이다.

## 네 파일과 16자리

```sh
python -B "$af_work/build_matrix.py" "$af_lab" "$af_out"
python -B "$af_work/read_matrix.py" "$af_lab" "$af_out" "$af_out"
```

첫 명령은 새 경로에서 네 writer 호출과 PyArrow footer를 기록한다. 저장된 원래 bytes에 대해 독립 실행하려면 두 번째 명령의 입력을 `"$af_work"`로 바꾼다. [files.csv](files.csv)는 입력·출력 SHA, [footer diff](evidence/build/footer-differences.json)는 바뀐 메타데이터를 담고 있다. 동일 환경에서는 각각의 파일 SHA가 일치해야 한다. 다른 환경에서 새로 쓰면 새 SHA로 두 reader를 묶어서 비교한다.

한 셀의 복원은 아래와 같다. 나머지는 파일 ID·SHA·reader·반복만 바꾼다. [runs.jsonl](runs.jsonl)에 16개 실제 명령, 각 프로세스 ID, SHA, 종료값과 fail 이유, 값, dtype, 양 판정이 들어 있다.

```sh
"$af_lab/venv-O/bin/python" -B "$af_work/observe.py" O "$af_lab/src-O" \
  F4 "$af_work/fixtures/F4.parquet" c8eddc72bf703a19d6e8ac452de58c7f28a804048f91d202630a28e5d419be7e 1
```

관측기는 바로 읽은 SHA와 같은 메모리 bytes를 `read_parquet`에 넘긴다. 종료 0은 GeoPandas가 객체를 반환한 경우다. `semantic_spatial`, `strict_attribute_schema`를 별도로 읽는다. 종료 20은 고정 ValueError 거절, 21은 다른 reader 예외다. 호출 전 harness/import/hash 실패와 파일 미생성 skip도 별도 기록한다. 축 포함/무시 동등성과 `always_xy` 변환을 원 좌표 및 dtype과 함께 읽는다.

## 원 시험

```sh
(
  cd "$af_lab/src-O"
  "$af_lab/venv-O/bin/python" -B -m pytest geopandas/io/tests/test_arrow.py \
    -o "cache_dir=$af_out/pytest-O" -vv -ra -k 'test_write_spec_version or test_roundtrip'
  "$af_lab/venv-O/bin/python" -B -m pytest geopandas/io/tests/test_arrow.py \
    -o "cache_dir=$af_out/pytest-O" -vv -ra -k 'test_read_gdal_files'
)
(
  cd "$af_lab/src-N"
  "$af_lab/venv-N/bin/python" -B -m pytest geopandas/io/tests/test_arrow.py \
    -o "cache_dir=$af_out/pytest-N" -vv -ra \
    -k 'test_write_spec_version or test_roundtrip or test_read_parquet_geoarrow or test_geoarrow_roundtrip'
  "$af_lab/venv-N/bin/python" -B -m pytest geopandas/io/tests/test_arrow.py \
    -o "cache_dir=$af_out/pytest-N" -vv -ra -k 'test_read_gdal_files'
)
```

원 시험은 수정 없이 실행했다. 원 명령에는 `--junitxml`도 포함되며 경로·케이스별 상태는 [시험 영수증](evidence/upstream/receipts.json)에 있다. 원 assert·skip과 파일 SHA는 [원 시험 메모](evidence/upstream/notes.md)에서 확인한다. 48 케이스에는 Feather가 포함된다.

## 보조 입력

```sh
python -B "$af_work/auxiliary.py" run "$af_lab" "$af_work" "$af_out"
"$af_lab/venv-N/bin/python" -B "$af_work/mixed_types.py" write "$af_lab/src-N" "$af_out/fixtures/auxiliary"
```

[outcomes A–F](evidence/auxiliary)는 plain PyArrow, A-01의 score 변경, Point/결측/EMPTY, CRS 생략/명시 null, 새 열, pandas metadata 제거의 실제 호출과 stdout을 담는다. G는 `Point(117,23)`와 `MultiPoint([(2,7),(3,8)])`를 같은 열에 두고 N writer로 재생성한다. 원 [G-WKB](evidence/auxiliary/G-WKB.json) 및 [G-native](evidence/auxiliary/G-native.json) 각 두 명령에 새 output·SHA를 지정한다. [G-writer](evidence/auxiliary/G-write.json)에서 경로와 기대 geometry를 확인한다. F 최초 시도는 footer 도구가 pandas key를 필수로 가정해 API 호출 전 종료 1이었다. [초기 stderr](evidence/attempts/F-no-pandas-meta-O-1.stderr.txt), [같은 bytes로 재실행](evidence/auxiliary/F-no-pandas-meta.json).

## 작업 계약

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-087/manifest.json --fetch
```

시작 명령·최종 결과 SHA의 종료·검사 범위는 [HANDOFF.md](HANDOFF.md)에 있다. 결과판 고정 SHA에서 조회한다.
