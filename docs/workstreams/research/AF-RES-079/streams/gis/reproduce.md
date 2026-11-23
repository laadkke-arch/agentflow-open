# GIS 미실시 검사의 재개 입력과 명령

이 파일의 양판 명령은 **미실행**이다. `runtime-probe.json`만 기존 환경 GDAL 3.10.3의 ARG 실패를 기록한다. `replay_gis.py`의 환경 조회·구조 검사 성공도 해당 양판의 출력 성공으로 세지 않는다. 아래 Python 경로는 정확한 GDAL과 연결된 실행 환경을 확보한 뒤 실제 경로로 대응해야 한다. GDAL version 문자열을 코드가 검사하므로 다른 판이 조용히 통과하지 않는다.

모든 명령의 작업 디렉터리는 `docs/workstreams/research/AF-RES-079/streams/gis/`다. `runs/`의 JSON 결과와 프로세스 종료값을 함께 보존한다. probe 종료 0은 요청한 관측이 수행됐다는 뜻이며 P1/P2의 모든 기대값이 맞았다는 뜻이 아니다. 종료 3도 예상된 잘못된 입력의 명시적 거절인지, driver 또는 환경 부재인지 JSON의 원인으로 구별한다. 이미 있는 출력 파일은 덮어쓰지 않는다.

## 정확한 판과 공통 입력

| 환경 | 소스 고정 위치 | 최소 필요 기능 |
| --- | --- | --- |
| GDAL 3.6.0 | `b77481ccf9f84a708fd37a13a7e0a3384fdf1622` | RASDAMAN + 호환 raslib, 기존 시험 서버 |
| GDAL 3.7.0 | `ab9cb1a1d4928cdcf2877d8e0c6ad9fc2c79fbc9` | ARG, Parquet + Arrow/Parquet |
| GDAL 3.8.0 | `c46fe7e20e33925735ae4b785752795af72823bc` | ARG, Parquet + Arrow/Parquet |
| GDAL 3.9.0 | `bb5ea618e23e498e79e8b8e6bd7215ad94bb2103` | Parquet + Arrow/Parquet |
| 수신 RASDAMAN | `OSGeo/gdal-extra-drivers@ffe0c44714a491eb90ba82d8df74f621ac6003e7` | `not_integrated_in_build/rasdaman`의 실제 통합 및 빌드 |

GDAL3.7/3.8/3.9에 Parquet가 있다는 것은 이 환경에서 확인하지 못했다. 실제 설치·의존성 버전·build 옵션도 새 결과와 함께 적어야 한다. 현재 설치된 3.10.3에는 이 driver가 없다. 수신 RASDAMAN은 빌드에 통합되지 않은 소스이므로, 작동이 확인되지 않은 범용 CMake 한 줄을 성공 명령으로 제시하지 않는다. 최소 첫 행동은 이 소스의 CMakeLists 및 raslib 요구를 담당 환경에서 확인하여 명시적인 빌드 조합을 정하는 것이다.

`inputs/vector.json`은 봉인한 두 Point, 정수 id, UTF-8 label, EPSG:4326의 구체 serialization이다. `inputs/point-boundary.json`은 읽은 공급자 시험의 정상/null/EMPTY/정상 Point 순서를 옮긴 재현 입력이며 별도 자연 사건으로 세지 않는다. 입력 해시는 `validation.json`에 있다. 공급자 `test.parquet` 경로는 판별로 바이트가 달라 이 고정 입력의 대체물로 삼지 않는다.

## G03: beta1 → 1.0, 같은 전후 쌍으로 P1과 P2

먼저 3.7 writer로 과거 파일을 **한 번만** 만든다. 이후 P1은 구·신 reader에 그 파일의 같은 해시를 전달한다.

```bash
mkdir -p runs
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 env > runs/g37-env.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 env > runs/g38-env.json
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 write-vector --fixture inputs/vector.json --output runs/g03-old.parquet > runs/g03-old-write.json
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 inspect-vector --input runs/g03-old.parquet --driver Parquet > runs/g03-p1-old.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 inspect-vector --input runs/g03-old.parquet --driver Parquet > runs/g03-p1-new.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 write-vector --fixture inputs/vector.json --output runs/g03-new.parquet > runs/g03-new-write.json
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 inspect-vector --input runs/g03-new.parquet --driver Parquet > runs/g03-p2-old-consumer.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 write-vector --fixture inputs/vector.json --output runs/g03-invalid-compression.parquet --compression invalid > runs/g03-invalid-compression.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 write-vector --fixture inputs/vector.json --output runs/g03-invalid-point-m.parquet --point-m > runs/g03-invalid-point-m.json
```

비교할 필드는 `fields`, `ordered_rows`, `srs_wkt`, `geo_metadata.version`, reader의 성공/오류다. WKT 문자열 차이만으로 CRS 의미 차이를 단정하지 말고 authority와 좌표축 순서를 함께 판독한다. `--point-m`은 공급자 시험과 같이 measured geometry **layer 선언**에 대한 거절을 조사하며 실제 M ordinate serialization 성공 시험이 아니다. 위 두 잘못된 입력을 3.7에도 각각 실행하여 같은 단계·오류 종류에서 거절되는지 확인해야 한다. 새 writer의 성공만으로 이전 consumer 적합성을 선언하지 않는다.

## G04: 이름 변경과 같은 이름의 의미 변경

P1은 위 G03의 방식으로 3.8 WKB 파일 하나를 만들고 3.8 및 3.9에서 읽는다. P2는 동일 `point-boundary.json`을 세 선택에 넣는다. `GEOARROW_INTERLEAVED`로 고친 이름은 P2에서 허용되지만, 이를 P1의 기존 호출 유지로 세지 않는다.

```bash
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 write-vector --fixture inputs/point-boundary.json --output runs/g04-old.parquet --encoding GEOARROW > runs/g04-old-write.json
/opt/gdal-3.9.0/bin/python3 replay_gis.py --expected-version 3.9.0 write-vector --fixture inputs/point-boundary.json --output runs/g04-new-same-name.parquet --encoding GEOARROW > runs/g04-new-same-name-write.json
/opt/gdal-3.9.0/bin/python3 replay_gis.py --expected-version 3.9.0 write-vector --fixture inputs/point-boundary.json --output runs/g04-new-alias.parquet --encoding GEOARROW_INTERLEAVED > runs/g04-new-alias-write.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 inspect-vector --input runs/g04-old.parquet --driver Parquet > runs/g04-old-read.json
/opt/gdal-3.9.0/bin/python3 replay_gis.py --expected-version 3.9.0 inspect-vector --input runs/g04-old.parquet --driver Parquet > runs/g04-new-reads-old.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 inspect-vector --input runs/g04-new-same-name.parquet --driver Parquet > runs/g04-old-reads-new-name.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 inspect-vector --input runs/g04-new-alias.parquet --driver Parquet > runs/g04-old-reads-alias.json
```

필수 판독은 Point column의 struct/FixedSizeList Arrow type, 두 번째 행의 null, 세 번째 행의 EMPTY, 정수 id·문자·순서·CRS다. `pyarrow`가 없으면 Arrow schema는 미관측으로 남는다. 공급자 정적 기대와 반대 결과가 나오면 공급자 시험과 동일한 Arrow/Parquet 의존성 판 및 NaN/null 처리 설정을 먼저 비교한다. 구 consumer를 GeoParquet1.0 규격만 구현한 별도 구현으로 확장하려면 그 구현의 정확한 판과 입력해시를 새 행에 추가해야 하며 GDAL3.8 결과로 모든 1.0 consumer를 대신하지 않는다.

## G02: 기존 ARG 기본값, opt-in, nodata와 쓰기

ARG는 저장된 Int16 값 -9999를 본래 nodata로 선언할 수 있다고 가정하면 안 된다. 읽은 3.8 구현은 Int16 nodata를 -32767로 고정한다. 따라서 봉인 입력의 -9999는 그대로 보존하고, reader가 이를 일반 값으로 읽으면 P1 nodata 요구는 실패로 남긴다. 다음 입력 생성은 관측값을 만들지 않는 serialization 단계다.

```bash
python3 - <<'PY'
from pathlib import Path
import json, struct
p = Path('runs/arg-input')
p.mkdir(parents=True, exist_ok=True)
(p/'sealed.arg').write_bytes(struct.pack('>4h', 1, 2, 3, -9999))
(p/'sealed.json').write_text(json.dumps({'layer':'sealed','type':'arg','datatype':'int16','xmin':0,'ymin':0,'xmax':2,'ymax':2,'cellwidth':1,'cellheight':1,'rows':2,'cols':2,'epsg':4326}))
(p/'supplier-int16.arg').write_bytes(struct.pack('>4h', -32768, 2, -3, -4))
(p/'supplier-int16.json').write_text(json.dumps({'layer':'supplier-int16','type':'arg','datatype':'int16','xmin':0,'ymin':0,'xmax':2,'ymax':2,'cellwidth':1,'cellheight':1,'rows':2,'cols':2}))
PY
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 inspect-raster --input runs/arg-input/sealed.arg --driver ARG > runs/g02-old-default.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 inspect-raster --input runs/arg-input/sealed.arg --driver ARG > runs/g02-new-default.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 --arg-opt-in inspect-raster --input runs/arg-input/sealed.arg --driver ARG > runs/g02-new-opt-in.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 --arg-opt-in inspect-raster --input runs/arg-input/supplier-int16.arg --driver ARG > runs/g02-sentinel-disagreement.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 --arg-opt-in write-raster --output runs/g02-new.arg > runs/g02-p2-write.json
/opt/gdal-3.7.0/bin/python3 replay_gis.py --expected-version 3.7.0 inspect-raster --input runs/g02-new.arg --driver ARG > runs/g02-p2-old-consumer.json
/opt/gdal-3.8.0/bin/python3 replay_gis.py --expected-version 3.8.0 --arg-opt-in write-raster --output runs/g02-invalid-bands.arg --bands 2 > runs/g02-p2-invalid.json
/opt/gdal-3.9.0/bin/python3 replay_gis.py --expected-version 3.9.0 inspect-raster --input runs/arg-input/sealed.arg --driver ARG > runs/g02-removed.json
```

기대: 기본3.8은 gate 때문에 거절한다는 **정적 예측**이며 이 연구에서 위 명령으로 실행한 결과가 아니다. opt-in 읽기는 값, Int16, nodata, 순서, CRS와 geotransform을 실제로 대조한다. supplier fixture의 -32768과 구현의 -32767 차이를 특히 남긴다. 잘못된 JSON의 `type`이나 `datatype`도 원본을 복사해 하나씩 바꾸고 명시적 오류가 발생하는지 추가 실행한다. 해당 파일은 정상 fixture를 덮어쓰지 않는다.

## G01: RASDAMAN의 source 이동을 실행 적합성과 분리

먼저 3.6 core driver 및 수신 source의 실제 build를 확보한다. 공급자 입력은 `rgb` collection이고 원 시험은 demo data와 checksum61774를 지정한다. 본 연구는 database를 만들거나 demo data를 적재하지 않았다. 준비된 시험 서버가 있다면 아래 쿼리를 두 환경에서 동일하게 사용한다. 쉘의 `$x_lo` 등을 치환하지 않도록 아래의 역슬래시를 유지한다.

```bash
/opt/gdal-3.6.0/bin/python3 replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select a[\$x_lo:\$x_hi,\$y_lo:\$y_hi] from rgb as a'" > runs/g01-core-rgb.json
/opt/gdal-3.6.0/bin/python3 replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select a[\$x_lo:\$x_hi,\$y_lo:\$y_hi] from notexisting as a'" > runs/g01-core-missing.json
/opt/gdal-3.6.0/bin/python3 replay_gis.py --expected-version 3.6.0 inspect-raster --driver RASDAMAN --input "rasdaman:query='select'" > runs/g01-core-syntax.json
```

수신 build에 연결된 Python의 실제 GDAL 판을 먼저 `VersionInfo`로 기록한 뒤 동일 명령의 실행기와 `--expected-version`만 그 판으로 지정한다. 수신 소스 자체에 GDAL runtime 판이 붙어 있다고 가정하지 않는다. 서버 rasdaman/raslib 판·demo input 해시를 함께 기록한다. 공급자 시험은 예외 비활성의 `None`을 기대하고 본 probe는 예외 활성으로 RuntimeError를 기록하므로, 거절 여부와 Python 오류 표현 정책을 별도 비교한다. P1의 전체 CRS 요구와 P2 write 기능은 이전·이후 모두 원래부터 제공하지 않아 적용 외다. 이관으로 인한 실패 분자에 넣지 않으며, pixel checksum 성공으로 전체 요구를 충족했다고 바꾸지 않는다.
