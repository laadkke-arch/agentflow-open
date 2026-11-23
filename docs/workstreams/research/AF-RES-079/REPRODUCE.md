# AF-RES-079 · 재현·미실시 검사·최소 재개

작업 기준 디렉터리는 저장소 root다. 아래 명령은 별도 표시가 없으면 repo root에서 실행한다. 산출물 경로는 계속 `docs/workstreams/research/AF-RES-079/` 안이다. 현재 결과의 SHA·실행 주체·시점·종료값은 `evidence/acceptance-evidence.json`과 마지막 `HANDOFF.md`를 먼저 읽는다. 기존 원관측을 덮어쓰지 않고 새 실행 디렉터리에 기록한다.

## 1. 원장과 Git 계약 검사

```bash
python -B docs/workstreams/research/AF-RES-079/audit.py --phase result --output evidence/reruns/audit-result-new.json
python -B -m workbench.session check docs/workstreams/research/AF-RES-079/manifest.json --fetch
```

첫 명령은 source/observation/relation ID 연결, 필드, 판독 분모, 실행 해시, prospective SCOPE 보존, 변경 경로를 검사한다. 두 번째 명령은 저장소의 workbench 계약·소유경로·원격 기준을 검사한다. 어느 것도 미실행 제품 동작을 증명하지 않는다. `audit.py --phase result`의 기본 출력은 `evidence/audit-result.json`이며, 위 명령은 `--output`으로 새 영수증 경로를 지정한다. 기존 원 결과판 영수증은 덮어쓰지 않는다. 중앙 원장은 수정하지 않는다.

통합 뷰 재생성은 다음과 같다. 최초 stream 원관측과 가림 snapshot은 입력으로 유지한다.

```bash
python -B docs/workstreams/research/AF-RES-079/assemble_ledgers.py
python -B docs/workstreams/research/AF-RES-079/adjudicate_relations.py
```

## 2. 실제 완료한 OSS 양판 실행을 새 위치에서 반복

실제 환경은 CPython3.8.20, NumPy1.19.5, SciPy1.4.1/1.5.0/1.5.4/1.6.0의 네 venv다. 원 호출200행과49대응은 `streams/oss/historical/`에 있다. 명시적 mapping3행과 exact input hash46행을 구별한다. 단일 probe의 `historical_pair_claim=false`는 의도된 값이다. 양판 결과를 join·검증한 파일만 pair 관측을 선언한다.

다음 예는 새 디렉터리 이름을 사용하므로 기존 기록을 덮어쓰지 않는다. 이미 그 이름이 있으면 다른 고유 이름을 지정한다. `uv`와 공개 PyPI wheel 접근이 필요하다. wheel만 허용하며 전역 설치를 하지 않는다.

```bash
export AF079_REPLAY=docs/workstreams/research/AF-RES-079/reruns/scipy-replay-001
mkdir -p "$AF079_REPLAY/oss/historical"
cp docs/workstreams/research/AF-RES-079/streams/oss/probe.py "$AF079_REPLAY/oss/probe.py"
cp docs/workstreams/research/AF-RES-079/streams/oss/historical/run_recorded.py "$AF079_REPLAY/oss/historical/"
cp docs/workstreams/research/AF-RES-079/streams/oss/historical/install_and_probe.py "$AF079_REPLAY/oss/historical/"
cp docs/workstreams/research/AF-RES-079/streams/oss/historical/compare_pairs.py "$AF079_REPLAY/oss/historical/"
cp docs/workstreams/research/AF-RES-079/streams/oss/historical/.gitignore "$AF079_REPLAY/oss/historical/"
python -B "$AF079_REPLAY/oss/historical/run_recorded.py" --label install-python38 --timeout 150 -- uv python install 3.8.20 --no-bin --system-certs --no-config
python -B "$AF079_REPLAY/oss/historical/install_and_probe.py"
python -B "$AF079_REPLAY/oss/historical/compare_pairs.py"
```

입력은 unchanged `probe.py`에 구체적으로 저장되어 있다. O01의 핵심은 `[1.,3.,2.]`, 빈 `(3,0)`와 `axis=1`, 정상 reciprocal-scale adapter다. O02는 적분 y/x의 정상·역순·빈·단일·2D·float32·complex와 axis9/길이 불일치, 별도 stats 분포 fixture다. O03은 점 `[[0],[1],[2]]`, query `[0]`, bound/radius `1.1`과 `1.0`이며 거리·순서·scalar 표현까지 비교한다. O04는 `input=[[1,2],[3,4]], labels=[[1,2],[2,4]], index=[4,8,2]`와 dtype/shape 오류다.

**아직 실행하지 않은 OSS 최소 추가 검사:** `simps→simpson`, `cumtrapz→cumulative_trapezoid` 두 개별 mapping의 정상/짝수·홀수 표본/initial·축 계약. 같은 명명 사건의 일부를 실행했다는 이유로 이 두 기능을 자동 승인하지 않았다. 또한 O01 빈 형상 adapter 및 O03 거리·정렬·strict 경계·원소 형 adapter는 구현하지 않았다. 다음 작성자는 이 contract를 먼저 명시하고 같은 원 fixture를 adapter에 통과시켜야 한다.

## 3. GIS의 정확 입력과 실행 조건

기본 재현 script·고정 입력·명령은 [streams/gis/reproduce.md](streams/gis/reproduce.md), `replay_gis.py`, `inputs/vector.json`, `inputs/point-boundary.json`에 있다. 그 문서는 단계2 시점의 미실행 상태를 보존한다. 후속 실행이 있으면 `streams/gis/historical/`의 영수증과 matrix가 해당 입력에 한해 상태를 갱신한다. 문서의 `/opt/gdal-<판>/bin/python3`는 **준비할 실행기의 역할 이름**이며 이 workspace에 존재한다고 주장한 경로가 아니다.

GIS에서 `pyarrow` 설치만으로 GDAL Parquet driver가 존재하지는 않는다. 실행 직전에 `GetDriverByName('Parquet')`를 확인한다. 실제로 G02·G03·G04에서 후속 환경을 실행했다. 환경은 conda-forge의 `libgdal-arrow-parquet`를 사용하며 Python/GDAL/plugin/Arrow/NumPy/PROJ/build ID를 모두 기록한다. `historical/environment-packages.json`과 네 `*-explicit.txt`는 재취득할 패키지·build를 고정한다. transient 환경 디렉터리 자체는 저장하지 않았다. 생성 파일11개는 `historical/runs/`와 `streams/resume-gis/audit.json`의 manifest로 보존했다. 재빌드 배포물을 원 release-day binary라고 부르지 않고, 의존성이 달라진 경우 GDAL 판만의 인과 효과라고 단정하지 않는다. G04에서 Python pyarrow는 양쪽14.0.2지만 파일의 실제 C++writer는3.8의14.0.1 대3.9의14.0.2이다. 같은3.9 encoding 대조GN07은 이 환경 차이와 구별되는 근거다.

### G03의 최소 구별 실행

3.7 writer가 `inputs/vector.json`에서 파일 하나를 만든 뒤 그 동일 해시를 3.7/3.8에 전달한다. P2는3.8 writer 결과를3.7 reader에도 전달한다. 핵심 명령 형태는 다음과 같다. 정확한 실행기 경로는 후속 영수증의 `command_argv`에서 취한다.

```bash
GDAL37_PYTHON=/opt/gdal-3.7.0/bin/python3
GDAL38_PYTHON=/opt/gdal-3.8.0/bin/python3
AF079_GIS=docs/workstreams/research/AF-RES-079/streams/gis
AF079_GIS_RUN=docs/workstreams/research/AF-RES-079/reruns/gis-replay-001
mkdir -p "$AF079_GIS_RUN"
"$GDAL37_PYTHON" "$AF079_GIS/replay_gis.py" --expected-version 3.7.0 write-vector --fixture "$AF079_GIS/inputs/vector.json" --output "$AF079_GIS_RUN/g03-old.parquet" > "$AF079_GIS_RUN/g03-old-write.json"
"$GDAL37_PYTHON" "$AF079_GIS/replay_gis.py" --expected-version 3.7.0 inspect-vector --input "$AF079_GIS_RUN/g03-old.parquet" --driver Parquet > "$AF079_GIS_RUN/g03-old-read.json"
"$GDAL38_PYTHON" "$AF079_GIS/replay_gis.py" --expected-version 3.8.0 inspect-vector --input "$AF079_GIS_RUN/g03-old.parquet" --driver Parquet > "$AF079_GIS_RUN/g03-new-read.json"
"$GDAL38_PYTHON" "$AF079_GIS/replay_gis.py" --expected-version 3.8.0 write-vector --fixture "$AF079_GIS/inputs/vector.json" --output "$AF079_GIS_RUN/g03-new.parquet" > "$AF079_GIS_RUN/g03-new-write.json"
"$GDAL37_PYTHON" "$AF079_GIS/replay_gis.py" --expected-version 3.7.0 inspect-vector --input "$AF079_GIS_RUN/g03-new.parquet" --driver Parquet > "$AF079_GIS_RUN/g03-old-consumer.json"
```

비교 대상은 값뿐 아니라 fields, ordered_rows, srs_wkt/authority/axis, geo metadata version, file hash와 오류 발생 단계다. WKT 문자열 차이만으로 CRS 의미가 달라졌다고 단정하지 않는다.

G04는 동일 Point/null/EMPTY 입력을3.8 `GEOARROW`,3.9 같은 문자열,3.9 `GEOARROW_INTERLEAVED`에 각각 쓰고3.8/3.9 reader에서 읽는다. Arrow column의 struct/FixedSizeList, null bitmap과 geometry EMPTY를 비교한다. GDAL reader 하나의 성공으로 모든 GeoParquet1.0 구현을 대신하지 않는다.

G02는 원 -9999 bytes를 그대로 두고3.7 default,3.8 default,3.8 opt-in을 비교한다. `--arg-opt-in`은 P1의 기존 기본 호출 유지가 아니다. 노데이터가 -32767로 고정되어 -9999가 일반값이 되면 원 요구를 보존하지 못했다고 적어야 한다. 봉인 입력을 지원 포맷에 맞춰 몰래 바꾸지 않는다. invalid multiband/type/header의 명시적 거절은 오류 코드·단계로 기록한다.

### G04 exact-schema 보류를 바꿀 최소 후속 — 아직 미실행

공식3.9 문서에서 `WRITE_COVERING_BBOX` 기본YES를 확인했다. 아래는 보존된 새 struct 파일을 같은3.9에서 legacy encoding으로 변환하면서 bbox 기록을 끄고,3.8 reader의 field 집합을 확인하는 구체 명령이다. 입력SHA는 `f71606cd995ad8b04533735d47abe8490bcc5faf75206f1e727610a6238b9f45`다. 새 입력이나 자연 사건을 추가하는 시험이 아니다. `GDAL39_PYTHON`/`GDAL38_PYTHON`은 앞 설명대로 준비한 정확 runtime이고 plugin/data 경로도 그 환경에 맞춘다.

```bash
GDAL39_PYTHON=/opt/gdal-3.9.0/bin/python3
GDAL38_PYTHON=/opt/gdal-3.8.0/bin/python3
AF079_EXACT=docs/workstreams/research/AF-RES-079/reruns/g04-bbox-no-001
mkdir -p "$AF079_EXACT"
"$GDAL39_PYTHON" -c 'from osgeo import gdal; import sys; gdal.UseExceptions(); d=gdal.VectorTranslate(sys.argv[2], sys.argv[1], format="Parquet", layerCreationOptions=["GEOMETRY_ENCODING=GEOARROW_INTERLEAVED","WRITE_COVERING_BBOX=NO"]); assert d is not None; d=None' docs/workstreams/research/AF-RES-079/streams/gis/historical/runs/g04-new-same-name.parquet "$AF079_EXACT/no-bbox.parquet"
"$GDAL38_PYTHON" docs/workstreams/research/AF-RES-079/streams/gis/replay_gis.py --expected-version 3.8.0 inspect-vector --input "$AF079_EXACT/no-bbox.parquet" --driver Parquet > "$AF079_EXACT/old-consumer.json"
```

필드가 id/label뿐인지,geometry·CRS·순서가 유지되는지,original interleaved와 같은 null→EMPTY 범위인지 판독한다. 이 명령은 실행 결과가 아니며 **bboxNO가 모든 계약을 복원한다고 예측만으로 승인하지 않는다.**

### G01에서 남는 실제 장애와 첫 행동

원 adapter는 `raslib`와 준비된 rasdaman server/collection에 의존한다. 수신 source는 빌드에 통합되어 있지 않다. 이 연구는 해당 서버를 만들거나 demo data를 적재하지 않았다. **첫 행동은 수신 commit `ffe0c44714a491eb90ba82d8df74f621ac6003e7`의 source와 담당 환경의 raslib/server 판을 함께 받아 실제 build 조합을 정하는 것**이다. 무조건 성공하는 CMake 한 줄을 제시하지 않는다.

build가 준비되면 같은 서버의 `rgb` collection과 supplier checksum61774를 양쪽 adapter에 사용한다. 다음 명령에서 실행기 경로와 GDAL 판은 실제 build와 맞춰야 한다. 변수 치환을 막기 위해 `$x_lo` 등의 역슬래시를 유지한다.

```bash
/opt/gdal-3.6.0/bin/python3 docs/workstreams/research/AF-RES-079/streams/gis/replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select a[\$x_lo:\$x_hi,\$y_lo:\$y_hi] from rgb as a'"
/opt/gdal-3.6.0/bin/python3 docs/workstreams/research/AF-RES-079/streams/gis/replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select a[\$x_lo:\$x_hi,\$y_lo:\$y_hi] from notexisting as a'"
/opt/gdal-3.6.0/bin/python3 docs/workstreams/research/AF-RES-079/streams/gis/replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select'"
```

수신 build에서도 같은 input/server hash를 쓰고 실제 Python 경로/`--expected-version`만 바꾼다. 원 공급자 시험은 exception-disabled `None`, probe는 exception-enabled RuntimeError를 기록하므로 거절 결과와 Python 표현 정책을 구별한다. 원래 지원하지 않은 georeferencing과 writer를 이관 때문에 사라졌다고 세지 않는다.

## 4. 대조의 미실시 검사

### C02: 원 PIL 확보는 완료, 원 native는 미실행

원 archive SHA256은 `895bc7c2498c8e1f9b99938f1a40dc86b3f149741f105cf7c7bd2e0725405211`이다. 공식 Debian `.dsc`의 크기·SHA256/SHA1/MD5와 일치하며 Debian diff를 원 archive에 적용하지 않았다. PGP 서명 trust chain은 검증하지 않았다. 아래는 획득/지문 검사이며 원 PIL 프로그램 실행이 아니다.

```bash
python -B docs/workstreams/research/AF-RES-079/streams/pil_archive/acquire.py
python -B docs/workstreams/research/AF-RES-079/streams/pil_archive/inspect_archive.py
```

옛 원판 실행에는 PIL1.1.7이 지원하는 Python2 환경과 해당 native codec build가 필요하다. 원 README·setup.py에 따라 이를 먼저 준비한 뒤 설치 방법을 고정한다. fixture는 현재 Pillow가 만든 2×1 RGB PNG와 같은 bytes이어야 하며, `Image.open` 성공만 보지 말고 `load()` 후 mode/size/ordered pixels를 확인한다. invalid header, truncated PNG, mode='w', verify 호출 순서를 별도로 검사한다. 현재 결과의 PNG 해시는 `78253200c249d4d84293b2a1e6fc803adedeba8645f38d6bc2f6734a2dfacec9`이다. 원 bytes를 재생성하면 먼저 이 해시가 같은지 확인하고 다르면 새 fixture로 표기한다.

```python
from PIL import Image
import io
raw = open('fixed-rgb.png', 'rb').read()
im = Image.open(io.BytesIO(raw))
im.load()
print(im.mode, im.size, list(im.getdata()))
try:
    Image.open(io.BytesIO(b'not an image')).load()
except Exception as exc:
    print(type(exc).__name__, str(exc))
```

이 코드는 양쪽 환경에 동일하게 넣을 재개 입력이며 원PIL에서 실행했다고 주장하지 않는다. 원 selftest도 `from PIL import Image`를 사용하므로 이 import 형태가 fork에서 새로 생겼다는 가정을 하지 않는다.

### C01과 C03

C01은 scikit-learn0.8 `f7c9f24511d9b32add23e75bbf0a2a6c223d932f`와0.9 `3f1ea662ee1b1b08cee63cc31e4e3e36ec532208`의 지원 Python/NumPy/SciPy 조합이 먼저 필요하다. 같은 `load_iris()`에서 필드·배열 bytes·순서를 비교하고, P2 estimator는 원 caller의 fit parameter와 명시적 gamma를 고정해야 한다. 프로젝트 rename으로 모든 estimator를 승인하지 않았다.

C03의 다음 입력은 CPython3.11/3.12에서 `imp.find_module('json')`, 존재하지 않는 모듈, `find_spec` 대응을 비교하는 것이다. 현재3.12.14 실행은 이미 root runtime 영수증에 있다. old return tuple/ImportError를 사용하는 실제 caller가 확인되면 명시적 변환을 작성하고 별도 검증한다. `load_module`의 reload 의미를 단순 import_module에 넘기지 않는다.

## 5. 원격 결과판 재독과 마지막 인계

결과 commit을 만든 뒤 해당 **정확 SHA의 raw 파일**을 다시 내려받아 로컬 canonical Git blob과 SHA256을 비교한다. RESULT, SELF_CHECK, 세 원장, SCOPE/frame, 수용 JSON 및 실제 실행/가림 근거를 포함한다. 다른 branch의 최신 파일과 비교하지 않는다. Git의 LF 정규화 때문에 작업 파일의 CRLF와 원격 LF를 혼동하지 말고 `git show <resultSHA>:<path>`를 기준으로 한다.

이 재독 완료를 마지막 HANDOFF에 기록하고, `HANDOFF.md` 하나만 별도 마지막 commit으로 만든다. 그 commit의 parent가 결과 고정 SHA이고 changed path가 HANDOFF 하나인지 확인한다. 이후 산출물을 고치면 새로운 결과판·재독·마지막 HANDOFF 절차가 필요하다.
