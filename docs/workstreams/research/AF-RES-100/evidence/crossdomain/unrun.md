# 실행하지 않은 원 시험과 재개 입력

이 문서의 명령은 **실행하지 않았다**. 종료값은 모두 미실시이며 성공·실패·skip으로 집계하지 않는다. 현재 확보한 것은 고정 원문과 일부 원 fixture의 바이트다. 전체 상류 checkout, 해당 빌드, Python binding, 실행기/plugin을 갖춘 실행 환경은 만들지 않았다. 원 시험이 스스로 만드는 상수 grid는 그대로 둘 수 있지만, 결손 실제 DEM이나 geoid를 연구자 입력으로 대신하지 않는다.

## A. GDAL 수직 raster 원 시험

준비할 checkout은 `OSGeo/gdal@35a44cc570cdf4dbd55611e4bd61da76e56bc221`이다. 이 checkout의 `autotest/`를 작업 디렉터리로 삼는다. Python에서 가져오는 GDAL binding과 GDAL library가 모두 3.10.0이어야 한다. 시험 환경에는 `pytest`, 상류 `conftest.py`/`pymod`, `MEM`·`GTX` 드라이버, 단위/VRT 시험에는 `VRT`·`GTiff`, 연결된 PROJ와 일치하는 `proj.db`가 필요하다. 실제 PROJ 버전, `PROJ_DATA`, context search path, 네트워크 설정을 결과와 함께 기록한다. 이 목록은 이번 환경에 설치되어 있다는 주장이 아니다.

원 파일: `autotest/utilities/test_gdalwarp_lib.py` (XG2). 실행할 최소 원 시험:

```sh
python -m pytest -q utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135 utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135b utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135d utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135f
python -m pytest -q utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135h utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135n
PROJ_DEBUG=3 python -m pytest -q -s utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135s
```

정확한 원 입력은 XG2의 1865–1920행이다. GTX는 3×3×1 Float32, WGS84, geotransform `[-270,180,0,135,0,-90]`, 첫 grid의 모든 값 20, 둘째 grid의 모든 값 5다. 기본 MEM source는 1×1, geotransform `[500000,1,0,4000000,0,-1]`, 값 100이다. 원 pytest fixture가 임시 경로에 이 파일을 생성하도록 한다. 첫 명령의 원 기대값은 순서대로 120, 80, 115, 100이다. `135h`는 Float32 US survey feet에서 `115/(1200/3937)`, `135n`은 원 band 단위 feet의 값을 환산한 120을 기대한다. 이번 조사에서 관찰한 값은 없다.

`135s`는 별도로 격리한다. 원 소스는 -88.8888로 채운 임시 GTX를 만들지만 `srcSRS`에는 변수 보간이 없는 `{empty_grid_gtx}`를 전달한다. 먼저 원 코드를 고치지 않고 trace에서 실제로 시도한 파일명과 예외 메시지를 보존해야 한다. 단순 PASS는 의도한 grid 값 오류가 재현됐다는 뜻이 아니다. 원 test 수정·패치 제안은 이 연구 결과 밖의 별도 작업이다.

실세계 DEM을 다루려면 원 사용자 파일의 SHA-256, 단일/다중 밴드, source/target 수직 CRS, band unit, nodata, 실제 grid 이름·버전·SHA와 위치/네트워크 상태가 먼저 필요하다. XG1의 `in_dem.tif` 문서 예제는 실물이 없는 명령 템플릿이므로 실행하지 않는다. XG3가 지명한 `egm96_15.gtx`의 실물도 이번 조사에서 가져오지 않았다. 이 결손은 상수 시험 grid로 메우지 않는다.

## B. Sphinx 상속도 원 시험

준비할 checkout은 `sphinx-doc/sphinx@a1510de4777eaa2e569435f95b05f6f3293d7035`이다. 이 checkout을 작업 디렉터리로 삼고, 프로젝트가 지정하는 Python/test 의존성을 갖춘 환경을 사용한다. `pytest`와 Sphinx app fixture, 해당 checkout을 import하는 Sphinx 8.1.3, 원 `tests/roots` 전체가 필요하다. build 시험에는 실제 Graphviz `dot`과 출력 renderer가 필요하며, 없어서 skip되면 성공으로 세지 않는다.

```sh
python -m pytest -q tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram
python -m pytest -q tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_svg_html
dot -Tsvg:
```

첫 시험의 정확한 원 입력은 `tests/roots/test-inheritance/` 전체와 XS5/XS6/XS7다. XS5는 `A`, `B(A)`, `C(A)`, `D(B,C)`, `E(B)`, `F(C)`를 정의한다. XS6는 F,D,E를 각각 지정하고 XS7은 `dummy.test` 모듈을 지정한다. 두 RST의 `top-classes`는 B,C다. 원 시험이 캡처한 `class_info`의 전체 목록을 별도로 보존하면, membership 검사만으로 빠지는 전체 집합/개수 질문에 답할 수 있다. 이번 연구는 새 assertion을 원 시험에 넣거나 runtime instrument를 작성하지 않았다.

둘째 시험의 원 testroot는 `ext-inheritance_diagram`이며, 원 `conf.py`, Python 클래스 모듈, `index.rst`, 하위 페이지와 상류 시험 내부의 압축 intersphinx inventory가 필요하다. 그 inventory와 URI는 상류 정의 입력을 그대로 쓰고 실제 외부 사용자 사이트라고 해석하지 않는다. 이 시험은 렌더러 경계의 보조 확인이며 AF-RES-096의 기존 일반 Graphviz 경로 사례를 새로운 모집 적중으로 다시 세는 것이 아니다.

`dot -Tsvg:`는 XV1에 있는 실제 렌더러 조회 문법이다. 이 명령은 사용 가능한 조합을 출력하는 진단이며 비영 종료값 자체를 build 실패로 오인하지 않는다. 선택된 renderer/formatter와 실행기 버전을 기록하고 원 Sphinx 시험의 skip/경고/출력 파일을 확인해야 한다. 실행기 버전은 현재 고정되어 있지 않다. P4 렌더링은 이 작업에 포함되지 않는다.

## 원장 재계산

저장소 root에서 다음 두 명령은 원문 취득·hash 확인 및 출처 원장 재계산만 수행한다. 상류 시험은 실행하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-100/evidence/crossdomain/collect.py
python -B docs/workstreams/research/AF-RES-100/evidence/crossdomain/build_records.py
```

비고정 SVG 보조 자료 XV2의 원 캐시가 있으면 hash를 다시 검증한다. 새 checkout에서 캐시가 없으면 커밋된 `sources.jsonl`의 과거 취득 기록을 그대로 유지하고 `counts.json`에 바이트 재검증을 못 한 항목으로 표시한다. 이 자료는 계속 하한에서 제외한다. 현재 페이지를 다시 취득하려면 새 시점·새 지문으로 별도 기록해야 한다. 바뀐 자료를 옛 지문으로 간주하면 안 된다.
