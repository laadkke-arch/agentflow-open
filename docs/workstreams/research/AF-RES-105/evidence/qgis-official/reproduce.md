# QGIS / spdep 독립 재현 명령

이 문서는 이미 읽은 소스와 저장된 실행 영수증에서 재현 절차를 정리한다. 이 문서를 작성하면서 추가 연구, 네트워크 취득, 설치, 빌드 또는 시험을 실행하지 않았다. 아래 상류 시험과 R 비교 명령은 **미실행**이다. 원 사용자의 데이터나 2024년 작업 환경을 복원하는 절차가 아니다.

| 대상 | 이 조사에서 실제 수행한 일 | 재현 상태 |
|---|---|---|
| `native_probe.py` | QGIS 3.40.6에서 두 합성 기능 probe를 실행. 첫 시도는 enum 오류, 수정한 두 번째 시도는 exit 0. | 저장된 결과와 실행 영수증 있음 |
| QGIS C++ 표현식 시험 | 3.34.0 고정 소스의 입력·기대값 및 `evaluation()` 실행 경로 판독 | 상류 시험 실행 안 함; 빌드 target/실행 파일 경로 미확인 |
| QGIS GDAL Python 시험 | 같은 고정 소스의 `testWarp`와 `testBuildVrt` 입력·기대 명령 판독 | 상류 시험 실행 안 함; 해당 판의 시험용 Python 환경 미구축 |
| spdep queen/rook 비교 | spdep 1.3-2 문서·구현 판독 | 아래 합성 비교 미실행; 이 작업공간에는 R/Rscript 없음 |

## 1. 이미 실행한 작은 native probe

저장소 루트에서 실행한다. 재현은 별도 복사본에서 수행한다. 스크립트가 `native-probe-results.json` 및 합성 이미지 캐시를 갱신하므로 봉인된 산출물과 새 실행 결과를 구분해야 한다.

```bash
cd /workspace/scratch/fb980e912f69/agentflow-open
/usr/bin/python3 -B docs/workstreams/research/AF-RES-105/evidence/qgis-official/native_probe.py
```

실제 성공한 환경의 확인된 전제는 다음과 같다.

- `/usr/bin/python3`: Python 3.13.5.
- 이 Python에서 import 가능한 `qgis.core`, `qgis.PyQt.QtCore`, `qgis.PyQt.QtGui`: QGIS **3.40.6-Bratislava**.
- `osgeo.gdal`: **GDAL 3.10.3**, release 2025/04/01.
- Qt의 offscreen 렌더링이 가능했다. 스크립트가 `QT_QPA_PLATFORM=offscreen` 및 작업 전용 profile/config/runtime 경로를 설정한다.
- 폰트 설정은 `DejaVu Sans`, 10이다. 배포판 패키지 이름, Qt 세부 버전, 폰트 대체 여부를 별도로 열거·검증한 것은 아니다. 추가 Python 패키지 설치 없이 저장된 시스템 Python으로 실행했다.

입력과 기대 기능 검사는 스크립트 및 `native-probe-results.json`에 완전히 들어 있다.

| Probe | 입력 | 저장된 관측과 검사 |
|---|---|---|
| QG-T2 반복 라벨 | EPSG:3857, `LINESTRING(0 0,1000 0)`, 라벨 `ROAD`, 반복 거리 200 Map Units | 라벨 5개가 모두 `ROAD`; 원 피처 수 1 유지 |
| QG-T3 그룹 라벨 | A(0,0), A(0,0), A(500,0), B(0,500); 필드 `Location_Names` | 배치만 적용하면 A 두 개/B 한 개. Show label에 `$id = array_first(array_agg($id,"Location_Names"))`를 적용하면 A/B 각 하나; 피처·속성·지오메트리 유지 |

저장된 성공 실행은 `native-probe-attempts.jsonl`의 attempt 2이며 exit 0, 렌더 오류 목록은 빈 배열이다. AF_NETLINK 권한 경고 5개를 삭제하지 않았다. attempt 1의 `OffsetFromPoint` 속성 오류는 성공에서 제외했다. 현재판 합성 실행은 역사판 구현 시험이나 원 사용자 성공 증거가 아니다.

## 2. QGIS 상류 시험을 실행할 준비

읽은 두 시험 파일 및 관련 구현의 고정 commit은 다음이다.

```text
ffbdd678812eec460ff02ff73bd36ee7955ac8a5
```

`final-3_34_0` annotated tag에서 확인한 QGIS 3.34.0 commit이다. 다음 명령은 **준비된 별도의 소스·빌드 경로를 검사하기 위한 미실행 명령**이다. 예시 절대 경로를 실제 경로로 바꾼다.

```bash
export AF105_QGIS_SOURCE=/absolute/path/to/qgis-3.34.0-source
export AF105_QGIS_BUILD=/absolute/path/to/qgis-3.34.0-build
git -C "$AF105_QGIS_SOURCE" rev-parse HEAD
test "$(git -C "$AF105_QGIS_SOURCE" rev-parse HEAD)" = ffbdd678812eec460ff02ff73bd36ee7955ac8a5
ctest --test-dir "$AF105_QGIS_BUILD" -N
```

필요한 전제는 위 commit의 소스, 그 판에 맞는 QGIS 개발 라이브러리·Python bindings, Qt 및 QtTest, GDAL, C++ 도구 체인, CMake/CTest, QGIS 시험 fixture와 시험 실행 환경이다. **전체 의존 패키지 목록·버전, configure 옵션, CMake target 이름, CTest 등록 이름, 생성된 실행 파일 경로는 이 조사에서 읽지 않아 미확인이다.** 따라서 `qgis_expressiontest` 같은 추정 target을 검증된 이름으로 쓰지 않는다. 해당 판의 공식 빌드 절차에 따라 시험을 활성화한 개발 빌드를 먼저 준비하고, 실제 생성된 target/CTest 목록에서 실행 파일을 확인해야 한다. 현재 설치된 QGIS 3.40.6을 역사판 시험 환경으로 대체하지 않는다.

### 2.1 C++ 표현식 시험

자료: `QG-T-U-EXPRESSION`, [고정 시험 소스](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/tests/src/core/testqgsexpression.cpp).

직접 읽은 QtTest 슬롯 이름은 **`evaluation`**(L2323–L2337)이다. 이 슬롯은 식을 평가한 뒤 dump, 원 식, 복사한 식에도 같은 검사를 적용한다. 리터럴 입력/기대값 행은 L2050–L2054에 있다. 생성된 이 소스의 QtTest 실행 파일을 확인한 다음 아래처럼 실행한다. 환경 변수 값은 검증된 빌드 산출물의 실제 경로로 지정해야 한다.

```bash
export AF105_EXPRESSION_TEST_BIN=/absolute/path/to/the/verified/expression-test-executable
QT_QPA_PLATFORM=offscreen "$AF105_EXPRESSION_TEST_BIN" evaluation
```

이는 전체 `evaluation` 슬롯을 실행하는 명령이다. 그 안에서 이 조사가 읽은 핵심 행은 다음이다. 나머지 행까지 별도 자료로 세지 않았다.

| 입력 | 상류의 기대값 |
|---|---|
| `array_first(array('a', 'b', 'c'))` | `QVariant("a")` |
| `array_first(array())` | `QVariant()` — 무효/NULL 값 |

`layerAggregates()`라는 다른 슬롯 이름도 L2959에서 확인했으나 전체 aggregate fixture를 판독하지 않았으므로 이 최소 재현 명령에는 추가하지 않는다. 이 조사에는 C++ 시험 실행 로그나 통과 주장이 없다.

### 2.2 GDAL Python 처리 시험

자료: `QG-T-U-GDAL`, [고정 시험 소스](https://github.com/qgis/QGIS/blob/ffbdd678812eec460ff02ff73bd36ee7955ac8a5/python/plugins/processing/tests/GdalAlgorithmsRasterTest.py).

검증된 함수 이름은 **`testWarp`**(L1948 시작), **`testBuildVrt`**(L2740 시작)이다. 시험 class 이름 및 해당 판의 CTest 등록 이름을 검증하지 않았으므로 아래 runner는 소스 module의 `unittest.TestCase` subclass에서 이 두 메서드만 찾아 실행한다. 이 runner 자체도 **미실행**이다.

전제는 위 commit으로 준비한 QGIS 시험용 Python 환경이다. 그 환경에서 QGIS bindings, GDAL, Processing 모듈, 시험 helper 및 fixture가 import/접근 가능해야 한다. 완전한 `PYTHONPATH`, library path, provider/plugin bootstrap 설정은 이 조사에서 확정하지 않았다. 아래 코드는 시험 파일의 디렉터리만 import 경로에 추가하며, 누락된 개발 환경을 자동으로 구성하지 않는다.

```bash
export AF105_QGIS_PYTHON=/absolute/path/to/python-for-the-qgis-3.34.0-test-build
QT_QPA_PLATFORM=offscreen "$AF105_QGIS_PYTHON" - <<'PY'
import importlib.util
import os
from pathlib import Path
import sys
import unittest

from qgis.core import Qgis
assert Qgis.QGIS_VERSION_INT == 33400, Qgis.QGIS_VERSION

source_root = Path(os.environ['AF105_QGIS_SOURCE']).resolve()
test_path = source_root / 'python/plugins/processing/tests/GdalAlgorithmsRasterTest.py'
sys.path.insert(0, str(test_path.parent))
spec = importlib.util.spec_from_file_location('af105_gdal_raster_upstream', test_path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

suite = unittest.TestSuite()
selected = []
seen_classes = set()
for value in vars(module).values():
    if not isinstance(value, type) or not issubclass(value, unittest.TestCase):
        continue
    if value in seen_classes:
        continue
    seen_classes.add(value)
    for method in ('testWarp', 'testBuildVrt'):
        if callable(getattr(value, method, None)):
            selected.append(f'{value.__name__}.{method}')
            suite.addTest(value(method))
assert len(selected) == 2, selected
print('Selected upstream methods:', selected)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
PY
```

실행되는 두 함수에는 추가 단언도 있다. 본 조사에서 입력과 기대 출력을 직접 읽은 핵심 비교는 아래와 같다.

| 함수·위치 | 입력 인수 | 기대 명령의 해당 부분 |
|---|---|---|
| `testBuildVrt`, L2747–L2757 | fixture `dem.tif`, `INPUT=[source]`, `OUTPUT=check.vrt`, `SEPARATE` 생략 | `gdalbuildvrt`; `-resolution average -separate -r nearest` |
| `testBuildVrt`, L2769–L2779 | 위 입력에 `SEPARATE=False` | 같은 명령에서 `-separate` 없음 |
| `testWarp`, L2078–L2087 | fixture `dem.tif`, `SOURCE_CRS=EPSG:3111`, `TARGET_RESOLUTION=10.0`, `OUTPUT=check.jpg` | `gdalwarp`; `-s_srs EPSG:3111 -tr 10.0 10.0 -r near -of JPEG` |
| `testWarp`, 읽은 해상도 구간 L2059–L2107 | 목표 해상도 `None` 또는 `0.0` | `-tr` 생략 |

이 시험의 입출력 단위는 **매개변수 사전 → 생성된 명령 문자열**이다. TIFF 픽셀을 읽어 워핑 결과를 검증했다는 뜻이 아니다. 입력 fixture의 실제 픽셀 내용은 이 조사에서 판독하지 않았다.

## 3. 미실행 R / spdep queen 대 rook 비교

자료: `QG-T-O-POLY2NB`, [spdep 1.3-2 문서](https://github.com/r-spatial/spdep/blob/46c90789e61affa495e1b9139442f4416dc7e7af/man/poly2nb.Rd), 고정 commit `46c90789e61affa495e1b9139442f4416dc7e7af`.

**이 작업공간에는 R/Rscript가 없어서 아래 비교를 실행하지 않았다.** 요구 전제는 R, `sf`, spdep DESCRIPTION이 요구하는 의존 패키지, 그리고 고정 소스에서 설치한 spdep **1.3-2**이다. R/sf/GEOS 세부 버전이나 역사적 의존 환경은 여기서 확정하지 않았다. 아래 예제는 CRS 없는 평면 단위 사각형을 쓰며, 원 사용자의 입력 복원이 아니다.

별도 환경에 해당 소스를 준비한 뒤 설치판을 고정하는 미실행 명령은 다음과 같다. 라이브러리 경로는 연구 전용 경로로 지정한다. 의존 패키지 설치 명령은 검증하지 않아 제공하지 않는다.

```bash
export AF105_SPDEP_SOURCE=/absolute/path/to/spdep-source
export AF105_R_LIBRARY=/absolute/path/to/dedicated-r-library
test "$(git -C "$AF105_SPDEP_SOURCE" rev-parse HEAD)" = 46c90789e61affa495e1b9139442f4416dc7e7af
mkdir -p "$AF105_R_LIBRARY"
R CMD INSTALL --library="$AF105_R_LIBRARY" "$AF105_SPDEP_SOURCE"
```

그다음 다음 입력/예상 결과를 독립 실행할 수 있다. `snap=1e-9`는 두 비교에 동일하게 명시한 합성 시험 매개변수이며, 원 제안자의 값으로 주장하지 않는다.

```bash
Rscript --vanilla - <<'RS'
.libPaths(c(Sys.getenv("AF105_R_LIBRARY"), .libPaths()))
stopifnot(utils::packageDescription("spdep")$Version == "1.3-2")

square <- function(x, y) {
  xy <- matrix(c(x, y,
                 x + 1, y,
                 x + 1, y + 1,
                 x, y + 1,
                 x, y), ncol = 2, byrow = TRUE)
  sf::st_polygon(list(xy))
}

# Order: 1=A lower left; 2=B lower right;
#        3=C upper left; 4=D upper right.
geometry <- sf::st_sfc(square(0, 0), square(1, 0),
                       square(0, 1), square(1, 1))
polygons <- sf::st_sf(id = c("A", "B", "C", "D"), geometry = geometry)

queen_nb <- spdep::poly2nb(polygons, queen = TRUE, snap = 1e-9)
rook_nb  <- spdep::poly2nb(polygons, queen = FALSE, snap = 1e-9)

edges <- function(nb) {
  parts <- lapply(seq_along(nb), function(i) {
    j <- nb[[i]]
    j <- j[j > i]
    if (length(j)) paste(i, j, sep = "-") else character(0)
  })
  sort(unique(unlist(parts, use.names = FALSE)))
}

queen_edges <- edges(queen_nb)
rook_edges <- edges(rook_nb)
print(list(queen = queen_edges, rook = rook_edges))
stopifnot(identical(queen_edges,
                   c("1-2", "1-3", "1-4", "2-3", "2-4", "3-4")))
stopifnot(identical(rook_edges,
                   c("1-2", "1-3", "2-4", "3-4")))
print(utils::sessionInfo())
print(sf::sf_extSoftVersion())
RS
```

문서에서 도출한 **기대값**은 queen의 무방향 간선 6개와 rook의 4개다. 대각선 A–D와 B–C는 한 꼭짓점에서만 만나므로 queen에서만 포함될 것으로 예상한다. 이 예제의 예상 출력은 관측 결과가 아니다. 또한 spdep 문서상 `queen=FALSE`는 공유 점 두 개 이상 조건이지 모든 복잡한 입력에서 공유 선분을 증명하는 일반 명세가 아니다.

## 4. 새 실행 기록에 남길 항목

독립 실행자는 실제 소스 commit, 실행 명령, 사용한 binary/Python/R 경로, 전체 버전, UTC, exit code, stdout/stderr, 필요한 fixture와 출력 해시를 새 기록에 남긴다. 환경 준비 실패와 실제 시험 실패를 구분하고, 이 문서의 미실행 명령을 실행 완료로 바꾸어 읽지 않는다. 이 안내서는 기존 Stage 1/2 파일이나 저장된 D3 결과를 수정하지 않는다.
