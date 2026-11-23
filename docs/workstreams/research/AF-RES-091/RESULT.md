# AF-RES-091 · GeoParquet의 행 선택과 Z

## 표 1 · 입력과 쓰기

| 입력·행 ID | 원래 타입·XY·Z·None/EMPTY | 원 목적·근거 URL | writer·encoding·실제 footer | 파일 SHA 또는 생성 실패 |
|---|---|---|---|---|
| S0 · WKB · A/B/N/E | A Point (117,23), B Point (2,7) · N None · E Point EMPTY 2D | 동종 2D에서 각각의 술어 유지 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S0-original.json) | N · WKB → WKB · 1.1.0 · `Point` · [footer](evidence/build/S0-WKB-footer.json) | [`7dd2a078997039bb5cc97066446f93e21819d73d3f73191d8bee2ae055b7e30f`](fixtures/S0-WKB.parquet) |
| S0 · native · A/B/N/E | A Point (117,23), B Point (2,7) · N None · E Point EMPTY 2D | 동종 2D에서 각각의 술어 유지 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S0-original.json) | N · geoarrow → point · 1.1.0 · `Point` · [footer](evidence/build/S0-native-footer.json) | [`9dcc45e8fe3313265336484882ad64e5762eedbd267cfb7a86d69a177fc39911`](fixtures/S0-native.parquet) |
| S1 · WKB · A/B/N/E | A Point (117,23), B MultiPoint ((2,7)) · N None · E Point EMPTY 2D | 동일 XY의 정확 타입으로 행 선택 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S1-original.json) | N · WKB → WKB · 1.1.0 · `MultiPoint, Point` · [footer](evidence/build/S1-WKB-footer.json) | [`568ae9b904c6901fbb65816b479f3d47b0dd15150b34f3c5089d5ee420cb5d55`](fixtures/S1-WKB.parquet) |
| S1 · native · A/B/N/E | A Point (117,23), B MultiPoint ((2,7)) · N None · E Point EMPTY 2D | 동일 XY의 정확 타입으로 행 선택 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S1-original.json) | N · geoarrow · footer 미생성 | 생성 실패 [ArrowInvalid](evidence/build/S1-native-writer.json) · [fixture 영수증](fixtures/S1-native.refusal.json) |
| S2 · WKB · A/B/N/E | A Point Z (117,23,135.25), B MultiPoint Z ((2,7,−42.5)) · N None · E Point EMPTY 2D | 유효한 두 행의 유한 Z 보존 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S2-original.json) | N · WKB → WKB · 1.1.0 · `MultiPoint Z, Point, Point Z` · [footer](evidence/build/S2-WKB-footer.json) | [`f6fa29c0e8bfe0230311687d7c4a6e31d0eb1c1b26fd421b0bbfca2b79dbd090`](fixtures/S2-WKB.parquet) |
| S2 · native · A/B/N/E | A Point Z (117,23,135.25), B MultiPoint Z ((2,7,−42.5)) · N None · E Point EMPTY 2D | 유효한 두 행의 유한 Z 보존 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S2-original.json) | N · geoarrow · footer 미생성 | 생성 실패 [ArrowInvalid](evidence/build/S2-native-writer.json) · [fixture 영수증](fixtures/S2-native.refusal.json) |
| S3 · WKB · A/B/N/E | A Point Z (117,23,135.25), B MultiPoint ((2,7)) · N None · E Point EMPTY 2D | 유한 Z와 Z 없는 행 구분 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S3-original.json) | N · WKB → WKB · 1.1.0 · `MultiPoint, Point, Point Z` · [footer](evidence/build/S3-WKB-footer.json) | [`a22fbce676e02168952cec94035017c5823c9de436c5ba7dab7be056b04a1a5f`](fixtures/S3-WKB.parquet) |
| S3 · native · A/B/N/E | A Point Z (117,23,135.25), B MultiPoint ((2,7)) · N None · E Point EMPTY 2D | 유한 Z와 Z 없는 행 구분 · [수작업 기대](fixtures/inputs.json) · [원 행](fixtures/S3-original.json) | N · geoarrow · footer 미생성 | 생성 실패 [ArrowInvalid](evidence/build/S3-native-writer.json) · [fixture 영수증](fixtures/S3-native.refusal.json) |

## 표 2 · 16개 읽기 자리

| 입력·인코딩·반복 | 읽기·동일 SHA | 기대→관측 타입·Z·CRS | T 기대→실제 ID/score | P 기대→실제 ID/score | 값·오류 근거 URL | 미확인 |
|---|---|---|---|---|---|---|
| S0 · WKB · 1 | 성공 0 · `7dd2a0789970` 일치 | A/B Point 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 · B/NA → A/101 · B/NA | A/101 → A/101 | [값·PID·exit](evidence/read/S0-WKB-r1.json) | — |
| S0 · WKB · 2 | 성공 0 · `7dd2a0789970` 일치 | A/B Point 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 · B/NA → A/101 · B/NA | A/101 → A/101 | [값·PID·exit](evidence/read/S0-WKB-r2.json) | — |
| S0 · native · 1 | 성공 0 · `9dcc45e8fe33` 일치 | A/B Point 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 · B/NA → A/101 · B/NA | A/101 → A/101 | [값·PID·exit](evidence/read/S0-native-r1.json) | — |
| S0 · native · 2 | 성공 0 · `9dcc45e8fe33` 일치 | A/B Point 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 · B/NA → A/101 · B/NA | A/101 → A/101 | [값·PID·exit](evidence/read/S0-native-r2.json) | — |
| S1 · WKB · 1 | 성공 0 · `568ae9b904c6` 일치 | A Point 2D · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S1-WKB-r1.json) | — |
| S1 · WKB · 2 | 성공 0 · `568ae9b904c6` 일치 | A Point 2D · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S1-WKB-r2.json) | — |
| S1 · native · 1 | reader 미실시 · SHA 미생성 | A Point 2D · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S1-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |
| S1 · native · 2 | reader 미실시 · SHA 미생성 | A Point 2D · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S1-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |
| S2 · WKB · 1 | 성공 0 · `f6fa29c0e8bf` 일치 | A Point Z=135.25 · B MultiPoint Z=−42.5 · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S2-WKB-r1.json) | — |
| S2 · WKB · 2 | 성공 0 · `f6fa29c0e8bf` 일치 | A Point Z=135.25 · B MultiPoint Z=−42.5 · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S2-WKB-r2.json) | — |
| S2 · native · 1 | reader 미실시 · SHA 미생성 | A Point Z=135.25 · B MultiPoint Z=−42.5 · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S2-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |
| S2 · native · 2 | reader 미실시 · SHA 미생성 | A Point Z=135.25 · B MultiPoint Z=−42.5 · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S2-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |
| S3 · WKB · 1 | 성공 0 · `a22fbce676e0` 일치 | A Point Z=135.25 · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S3-WKB-r1.json) | — |
| S3 · WKB · 2 | 성공 0 · `a22fbce676e0` 일치 | A Point Z=135.25 · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 모두 일치 | A/101 → A/101 | A/101 → A/101 | [값·PID·exit](evidence/read/S3-WKB-r2.json) | — |
| S3 · native · 1 | reader 미실시 · SHA 미생성 | A Point Z=135.25 · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S3-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |
| S3 · native · 2 | reader 미실시 · SHA 미생성 | A Point Z=135.25 · B MultiPoint 2D · N None · E Point EMPTY 2D · EPSG:4326 → 미관측 | A/101 → 미관측 | A/101 → 미관측 | [writer 원 예외](evidence/build/S3-native-writer.json) | 파일·복원·T/P 미확인 (writer 거절) |

## 표 3 · 목적별로 돌려줄 링크

| 소비자 목적·호출 URL | WKB 또는 native 권고·볼 절 | 관측상 동등한 입력 | 반례·바뀐 행 | 확인할 한 조건 |
|---|---|---|---|---|
| 생산자가 기존 ID에 정확한 geometry를 연결해 배포 · [GeoDataFrame.to_parquet](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/geodataframe.py#L1322-L1352) | 고정 N의 WKB 1.1.0 · [사양 WKB 절](https://geoparquet.org/releases/v1.1.0/#wkb) | S0–S3 WKB, 각각 2회 보존 | S1–S3 native에는 파일이 없다. S1-drop-E native는 A 타입을 바꾼다. [영수증](evidence/auxiliary/S1-drop-E.json) | 원 열에 혼형과 빈 단수 Point가 함께 들어오는가 |
| 영역 교차로 행을 선택 · [Dask-GeoPandas .cx](https://github.com/geopandas/dask-geopandas/blob/90c0734199e1c678318d66b2e7ee69a5edb4895c/dask_geopandas/expr.py#L1062-L1117) | 이미 읽히는 파일에서 이 P만 필요하면 S0 WKB/native 모두 허용 · [intersects](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/base.py#L3008-L3033) | S0 2쌍, 외부 동일 .cx A/101. S1-drop-E native도 원 P와 동일. [호출](evidence/external/consumer-controls.json) | S1–S3 native는 생산에서 보류. Point만 받는 XY 거리 경로는 별도 gate가 있다. [libpysal kernel](https://github.com/pysal/libpysal/blob/bcbe4302b1a9c63c44f027572b265154e83251a9/libpysal/graph/_kernel.py#L126-L148) | 사용자 호출이 이 사각형과 같은 2D 위치 술어인가 |
| 정확히 Point인 행을 선택 · [공개 주차 분리 호출](https://github.com/spatialthoughts/python-dataviz-web/blob/dd68ad89f88d28bee301e235a4af3bb95fe225ad/supplement_leafmap_osm.ipynb#L161-L173) | 혼형의 원 타입이 필요하면 WKB · [ISO 코드와 writer 경로](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/_geoarrow.py#L176-L204) | S0 두 인코딩의 T=A/B와 Z 부재 유지 | S1-drop-E의 동일 native 파일에서 원 T=A 또는 B, 복원 T=∅. A와 B 모두 MultiPoint. [동일 bytes](evidence/auxiliary/type-alias.json) | singleton MultiPoint를 Point와 같은 부류로 받아도 되는가 |
| Z 수치와 차원에 따라 분류 · [Shapely 차원](https://github.com/shapely/shapely/blob/3853e1170173125b7e86cbb5cc8dab1c274c3999/shapely/_geometry.py#L123-L147) | 원 차원과 Z까지 요구하면 고정 WKB · [GeoParquet geometry types](https://geoparquet.org/releases/v1.1.0/#geometry_types) | S2/S3 WKB 원 Z와 유무. S2-drop-E native의 두 유한 Z도 N에서 유지. [실제 XYZ](evidence/auxiliary/S2-drop-E.json) | S3-drop-E의 B는 물리 Z=NaN, N에서 2D. S2/S3 주 native는 writer 거절. [실제 NaN](evidence/auxiliary/S3-drop-E.json) | NaN 채움과 물리 Z 부재를 동등하게 취급하는가 |
| 파일·reader 또는 보존 목적 미상 · [GeoParquet footer 절](https://geoparquet.org/releases/v1.1.0/#metadata) | 링크 판정 유보. 한 질문으로 목표를 확인한 뒤 위 셀의 읽기 결과를 대조 | S0 native의 현재 N 결과만 직접 확인 | 타입 목록이 같은 두 입력에서 T 정답이 달랐다. [동일 파일 대조](evidence/auxiliary/type-alias.json) | “XY로 고른 행이 같으면 되나요, 아니면 원래 타입이나 Z에 따라 골라야 하나요?” |

### 분모와 결원

| 모집·실행·비교 | 완료와 결원 |
|---|---|
| 논리 입력과 파일 | 4/4 수작업 입력 검산. 8/8 writer 호출, 5/8 파일 생성 및 5/5 PyArrow footer 판독. WKB 4/4, native 1/4. native 3건은 같은 ArrowInvalid. [쓰기 목록](files.csv) |
| 계획한 읽기와 대응쌍 | 16/16 자리의 상태를 기록했다. 실제 새 PID는 10개, 종료 0은 10/10, reader 오류 0/10. writer 거절로 6개 PID·종료값·파일 SHA 미관측. 8대응쌍 중 비교 2쌍, 비교 불가 6쌍. [실행 원장](runs.jsonl) · [집계](evidence/read/summary.json) |
| 반복 안정성 | 같은 bytes를 받은 5/5 파일의 두 반복에서 행·frame·T/P 대조가 동일했다. native S1–S3의 반복은 산출 불가. [파일별 반복](evidence/read/summary.json) |
| XY·정확 타입·Z | 좌표가 있는 A/B의 XY와 2D 위상 20/20. 빈 E까지 포함한 위상 30/30과 정확 타입 30/30. 비결측 행의 차원 및 Z 유무·수치 30/30이며 유한 Z 비교는 6/6. [행별 비교](runs.jsonl) |
| 결측·속성·CRS | N None 10/10, E Point EMPTY 10/10. score 값 및 행 순서 40/40과 10/10, Int64 및 CRS 축·WKT 10/10. [행별 비교](runs.jsonl) |
| T | 관측 10, ID/score 일치 10/10. 관측 자리의 누락·추가·값 불일치 ID 각각 0. A/B 포함 총 14개 기대·14개 반환. writer 거절 6자리에서 A 각 1개 미관측. [T 집계](evidence/read/summary.json) |
| P | 관측 10, ID/score 일치 10/10. 관측 자리의 누락·추가·값 불일치 ID 각각 0. A 총 10개 기대·10개 반환. writer 거절 6자리에서 A 각 1개 미관측. [P 집계](evidence/read/summary.json) |
| Q1 후보와 외부 자료 | 지정 순서로 고정판 3개를 검색했다. exact T는 0/5·0/5·0/5, P는 5/5·4/5·5/5. 외부 공개 T 호출 1건을 별도로 찾았다. 산입 고유 1차 자료 52건과 독립 저작·사건 계보 38개를 확인했다. 사양 5, 라이브러리 15, 하류 25, 표 3, 팔레트 4. 제외 22행을 포함한 원장 74행. [후보와 결원](evidence/consumer-search/README.md) · [원장](sources.jsonl) |

## Q1–Q2 · 호출과 원 입력

T와 P 모두 유효하고 존재하며 비어 있지 않은 행을 대상으로 한다. T는 정확한 단수 타입으로 A/B를 가르고, P는 주어진 XY 사각형에서 A만 선택한다. S0에서 T는 A/B이고 P는 A다. S1–S3의 원 입력은 T와 P 모두 A다. B의 score는 결측이며 T가 B를 반환할 때 그대로 남긴다. N은 결측 지오메트리인데 score는 −3이며 E는 빈 Point인데 score는 0이다. 이 둘은 조건의 다른 절에 걸린다. 원 좌표를 쓰기 전에 WKT, ISO WKB, Z, dimension, mask, CRS 축과 함께 기록했다. [수작업 정답](SCOPE.md#수작업-정답) · [원 예 S2](fixtures/S2-original.json) · [GeoPandas 결측 안내](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/doc/source/docs/user_guide/missing_empty.rst#L14-L33).

momepy·libpysal의 공개 코드에서는 폴리곤·선 등의 위치 교차 단계 및 Point 전용 입력 gate가 각각 확인됐다. 각 알고리즘의 후속 거리·버퍼·이웃 가중치까지 실험 결과를 확장하려면 해당 원 입력이 필요하다. Dask의 `.cx`는 먼저 공간 분할을 고르고 각 분할에서 원 행을 `intersects`로 선택한다. 고정 v0.5.0에서 S0 두 파일과 보조 S1-drop-E를 실제 호출했고 세 파일 모두 A였다. [하류 호출·assert](consumers.csv) · [외부 실행](evidence/external/consumer-controls.json).

Spatial Thoughts의 주차 예는 OSM 주차 형상에서 정확히 Point인 행만 별도 레이어로 보낸다. 해당 원 lambda는 주 격자의 N이 있으면 AttributeError를 내며 N만 제외한 S0에서는 빈 E까지 뽑는다. 유효·비결측·비어 있지 않음 조건을 적용한 재현은 S0 두 파일에서 A/B이고 S1-drop-E native에서 빈 목록이다. 이 세 경우의 측정은 연구 입력에서 이뤄졌다. 원 OSM 질의의 사용자 데이터와 당시 실행 환경은 미확인이다. [원 notebook](https://github.com/spatialthoughts/python-dataviz-web/blob/dd68ad89f88d28bee301e235a4af3bb95fe225ad/supplement_leafmap_osm.ipynb#L161-L198) · [원 오류 및 출력](evidence/external/consumer-execution.json).

공개 Dask 이슈 #303의 원 사용자 실행은 공간 shuffle 뒤 기본 sjoin에서 tuple이 전달된 별도 장애다. 그 최소 box 입력을 고정 v0.5.0의 원 회귀시험에서 통과시켰다. 087 안내 인용이나 GeoParquet bytes가 그 장애로 이어졌는지는 미확인이다. [원 이슈](https://github.com/geopandas/dask-geopandas/issues/303) · [고정 원 시험 실행](evidence/external/upstream-tests.json).

## Q3–Q5 · 형식과 행 동작

S0에서 writer의 한 옵션을 바꾸자 WKB `binary/BYTE_ARRAY`가 native `struct<x: double not null, y: double not null>`로 바뀌었다. WKB는 E에 type code 1과 NaN XY가 든 값을 쓴다. native는 validity가 `[true,true,false,true]`이고 E의 x/y는 NaN이다. Arrow에서 N의 마스크 아래에 보이는 child 0,0은 유효 위치가 아니다. `version`, 컬럼별 타입 목록과 CRS 및 bbox 값은 S0에서 같았다. S2 WKB는 A/B의 ISO type code 1001/1004, S3 WKB는 1001/4였다. WKB Z가 있어도 관측한 footer bbox는 4원소 XY였다. 3D bbox까지의 사양 적합성과 가속 효과는 미확인이다. 비용 비교 범위는 S0의 실제 크기 7,951 → 8,390 bytes (+439)다. [S0 WKB footer](evidence/build/S0-WKB-footer.json) · [S0 native footer](evidence/build/S0-native-footer.json) · [S2 WKB footer](evidence/build/S2-WKB-footer.json) · [S3 WKB footer](evidence/build/S3-WKB-footer.json) · [사양 bbox](https://geoparquet.org/releases/v1.1.0/#bbox).

S1–S3의 혼형은 Shapely가 MULTIPOINT 배열을 선택하는 경로로 들어간다. 실제 `get_parts`에는 A/B와 E의 빈 단수 Point가 들어가지만 `get_coordinates`에는 A/B만 들어간다. `[0,1,2,2,3]`의 마지막 offset 3이 좌표 2개를 넘어, PyArrow 검증에서 파일 bytes가 0이었다. S1은 두 유효 행이 모두 2D이므로 이 오류는 2D/3D 혼합 여부만으로 설명할 수 없다. [원 ragged 관측](evidence/auxiliary/original-ragged.json) · [Shapely 고정 구현](https://github.com/shapely/shapely/blob/3853e1170173125b7e86cbb5cc8dab1c274c3999/shapely/_ragged_array.py#L76-L85) · [Arrow 변환 호출](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/_geoarrow.py#L371-L385).

| 별도 변경 | 결과와 관측 |
|---|---|
| S1에서 N만 제거 | E가 남고 offset 3이 좌표 2개를 넘어 여전히 ArrowInvalid다. [원 출력](evidence/auxiliary/S1-drop-N.json) |
| S1에서 E만 제거 | N은 null로 유지됐다. A가 MultiPoint로 승격되고 B는 그대로다. 원/복원 A/B의 XY와 위상이 동일하며 T에서 A/101만 빠지고 P는 A/101이다. [원 출력](evidence/auxiliary/S1-drop-E.json) |
| S1에서 E만 MULTIPOINT EMPTY로 교체 | 4행 native 쓰기와 읽기가 됐다. E는 비어 있고 N은 None이다. A의 정확 타입과 T가 바뀌고 P는 A다. [원 출력](evidence/auxiliary/S1-empty-MultiPoint.json) |
| S2에서 E만 제거 | XYZ 열로 쓰였으며 A=135.25, B=−42.5를 N이 모두 복원했다. A의 타입과 T는 바뀌고 P는 유지됐다. [원 출력](evidence/auxiliary/S2-drop-E.json) |
| S3에서 E만 제거 | XYZ 열 B에 숫자 NaN이 들어갔고 N의 Shapely는 B를 원래와 같은 2D로 보고했다. A=135.25는 유지됐고 A 타입/T는 바뀌었다. B의 물리 Z 부재를 요구하면 이 파일은 조건과 다르다. 최신 GEOS의 B 판독은 미확인이다. [원 출력](evidence/auxiliary/S3-drop-E.json) · [GEOS 3.12 변화](https://github.com/shapely/shapely/blob/5fb639d1056888d135fe56bfaf750c9648addeec/docs/release/2.x.rst#L158-L168) |

지리적 위상 비교는 여기서 공간 선택의 설명 근거다. OGC 관계는 2D 수평 투영에 기반하고, 고정 Shapely의 `equals`와 Point EMPTY 처리에 관한 원 시험도 XY/구조/차원의 차이를 보여 준다. T와 P가 같아도 P의 A가 갖는 Z의 값과 B의 원 차원은 따로 검사했다. 087의 G는 빈 행이 없는 타입 승격 사례였고, 이번 동종 S0는 native의 유지 사례다. [OGC 2D 관계](https://docs.ogc.org/is/06-103r4/06-103r4.pdf#page=33) · [Shapely equals](https://github.com/shapely/shapely/blob/3853e1170173125b7e86cbb5cc8dab1c274c3999/shapely/predicates.py#L716-L744) · [087 G-native](https://github.com/laadkke-arch/agentflow-open/blob/263fe7581cf45eadd1f05139aacaadb27290b86e/docs/workstreams/research/AF-RES-087/evidence/auxiliary/G-native.json).

## Q6 · 같은 파일에서 요구가 바뀔 때

- **링크 유지.** 같은 S0-native 파일은 영역 P에 이어 정확 타입 T와 두 유효 행의 Z 부재 계약도 통과했다. S0-WKB에도 같은 관측이 있다. 높이값을 실제로 사용하는 경우의 직접 유지 사례는 S2-WKB의 두 유한 Z다. [S0 native](evidence/read/S0-native-r1.json) · [S2 WKB](evidence/read/S2-WKB-r1.json).
- **링크 변경.** 같은 보조 S1-drop-E native에서 요구를 영역 P에서 정확 원 타입으로 바꾸면 native/.cx 안내에서 원 생산자의 WKB 또는 원 타입을 따로 보존한 파일 요청으로 바뀐다. B만 단수 Point가 되도록 A/B의 단·복수 타입을 맞바꾼 보조 입력도 같은 옵션으로 썼다. 두 writer 입력의 T 정답은 A/101과 B/NA로 다르지만 파일 SHA가 `8174134afb03872bd4495a9fb4507c2ae3c92b1f52cd673c9e9298db31669aaa`로 같았다. 두 입력의 P는 계속 A/101이다. `geometry_types=[MultiPoint, Point]` 목록에 타입이 둘 다 있어도 이 파일로 원 행별 타입을 식별할 수 없다. [같은 bytes와 원 T/P](evidence/auxiliary/type-alias.json) · [종류 목록 계산](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/arrow.py#L97-L111).
- **높이와 거리.** S2-drop-E에서 위치 P와 유한 Z 두 값은 유지된다. S3-drop-E에서는 동일 파일의 평면 P가 충분하다는 결론이 물리적으로 Z 부재가 필요할 때 바뀐다. XY 거리라는 이름 아래에서도 libpysal Delaunay/kernel이 Point만 허용하는 사례가 있다. 거리 보존은 해당 호출의 ID·기대값을 확보하기 전 미확인이다. [S3 물리/복원값](evidence/auxiliary/S3-drop-E.json) · [Delaunay gate](https://github.com/pysal/libpysal/blob/bcbe4302b1a9c63c44f027572b265154e83251a9/libpysal/weights/gabriel.py#L117-L152).

같은 main reader의 일부 성공을 전체 사양·저장 조합으로 확대하면 S1–S3 생산 실패와 충돌한다. 반대로 native를 전부 제외하면 S0와 `S2-drop-E`의 실제 좌표 계약 유지 사례를 놓친다. 일반 링크에는 적용할 reader 판과 파일 인코딩, 확인한 입력과 소비 호출 및 예상 ID를 붙인다. [GeoPandas writer API](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/geodataframe.py#L1330-L1352) · [검사 명령](reproduce.md).

## Q7 · 다른 분야에서 같은 계약을 확인하는 검사

| 분야 | 표시나 수치는 같아도 바뀐 선택 | 둘 다 유지된 조건·동일 입력 원 근거 |
|---|---|---|
| nullable 정수 | Arrow int64의 `[1,2,null]`에서 pandas metadata만 제거하면 float64가 된다. 결측 mask와 수치 비교는 같고 `select_dtypes(include="integer")`에서 score가 빠진다. 큰 정수 A=2⁵³·B=2⁵³+1과 같은 결측의 대조에서는 float에서 A/B가 중복 ID로 오인된다. [pandas 공식 정의](https://github.com/pandas-dev/pandas/blob/d9cdd2ee5a58015ef6f4d15c7226110c9aab8140/doc/source/user_guide/integer_na.rst#L11-L46) · [실행](evidence/external/representation-controls.json) | 원 metadata 및 `types_mapper` 두 경로에서 dtype·값·결측 mask·선택이 모두 유지됐다. Arrow 원 코드는 [1,2,None]의 int64 변환과 Int64 roundtrip을 검사했고 실행한 두 원 시험이 통과했다. [Arrow 공식 설명](https://arrow.apache.org/docs/16.1/python/pandas.html#nullable-types) · [원 시험](https://github.com/apache/arrow/blob/7dd1d34074af176d9e861a360e135ae57b21cf96/python/pyarrow/tests/test_pandas.py#L4288-L4308) · [실행](evidence/external/upstream-tests.json) |
| 색인 팔레트 | 합성 PNG 두 픽셀에서 팔레트 순서와 인덱스를 함께 교환했다. 재개봉 RGBA는 같지만 label 1의 픽셀 위치가 x=1에서 x=0으로 옮겼다. [PNG PLTE 정의](https://www.w3.org/TR/2025/REC-png-3-20250624/#11PLTE) · [실행](evidence/external/representation-controls.json) | identity remap과 PNG 왕복에서 원 픽셀 index와 RGBA 둘 다 유지됐다. Pillow 원 시험은 같은 p_trns_single.png 재저장 뒤 (31,31)의 index 164와 RGBA를 검증한다. 같은 팔레트 교환의 원 시험에서 투명 index는 0→1이다. [PNG 유지 원 시험](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/Tests/test_file_png.py#L267-L285) · [교환 원 시험](https://github.com/python-pillow/Pillow/blob/89f1f4626a2aaf5f3d5ca6437f41def2998fbe09/Tests/test_image.py#L665-L701) · [실행](evidence/external/upstream-tests.json) |

표는 수치와 null mask를, 팔레트는 렌더링 전 RGBA와 index 위치를 각각 독립 비교한다. 실측은 실제 모니터 색이 아닌 decoded RGBA다. GeoParquet에서도 사용자 선택 연산의 결과와 입력 표현에 의존하는 연산을 함께 측정하면 변환을 받아들일 조건을 구분할 수 있다. [자가검산](SELF_CHECK.md).

## 핵심 약점과 판정을 바꿀 관측 3건

1. **혼형 native의 쓰기 조건은 고정 스택과 이 입력에서만 확인했다.** 최신 지원 스택의 첫 대조 입력은 원 S1, 이어서 같은 S3-drop-E SHA와 B다. 새 writer가 E를 유지해 원 파일을 만들거나 새 reader에서 NaN B를 3D로 분류하면 새 판에는 별도 권고가 필요하다. [거절](evidence/build/S1-native-writer.json) · [NaN](evidence/auxiliary/S3-drop-E.json) · [판 차이 근거](https://github.com/shapely/shapely/blob/5fb639d1056888d135fe56bfaf750c9648addeec/docs/release/2.x.rst#L158-L168).
2. **위치 질의의 동등성은 지정한 XY intersects에서 관측했다.** 다음 입력은 A/B 외에 경계점과 복수 좌표 MultiPoint가 있고 실제 소비자의 CRS 및 거리·공간 조인 호출이 있는 파일이다. 같은 위치·타입 완화에서도 다른 ID/score, Point 전용 입력 거절 또는 좌표 수에 따른 다중 매칭을 관측하면 영역용 native 적용 범위를 줄인다. [직접 영역 호출](evidence/external/consumer-controls.json) · [Point gate](https://github.com/pysal/libpysal/blob/bcbe4302b1a9c63c44f027572b265154e83251a9/libpysal/weights/gabriel.py#L139-L152).
3. **공개 소비 목적은 확인했으며 087 안내의 실제 장애 이력은 미확인이다.** 다음 대상은 그 문구를 인용한 한 공개 하류에서 원 파일 SHA·reader import 판·기대 ID와 Z를 함께 제공하는 보고다. 그 환경과 bytes에서 기대 T/P 또는 Z가 달라지고 안내 조건이 선택을 바꾼다는 관측이 있으면 문서 수정의 필요도를 다시 판정한다. [087 인계](https://github.com/laadkke-arch/agentflow-open/blob/36a76b384810730b7d819a5ed469e6e8ded92f8a/docs/workstreams/research/AF-RES-087/HANDOFF.md) · [찾은 공개 하류와 결원](evidence/consumer-search/README.md).
