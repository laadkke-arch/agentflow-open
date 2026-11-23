# Q1 · 고정판의 후보를 찾은 순서

1. momepy v0.9.1 `86b342fdf18b37b651be3ffdd40d8d1a2adcd26b`: [rg 원 출력](momepy.txt).
2. libpysal v4.13.0 `bcbe4302b1a9c63c44f027572b265154e83251a9`: [rg 원 출력](libpysal.txt).
3. Dask-GeoPandas v0.5.0 `90c0734199e1c678318d66b2e7ee69a5edb4895c`: [rg 원 출력](dask-geopandas.txt).

[검색 명령](scan.sh)은 package → 문서 순으로 Python, RST, Markdown과 notebook 원 JSON의 타입 이름·타입 ID·spatial predicate를 모집한다. 각 경로 그룹 안에서 파일 경로, 행 순으로 읽었다. 타입 결과의 코드/문서 문맥은 직접 열어 확인했다. 후보별 호출, 원 입력·assert 또는 작성자 예와 채택 범위는 [consumers.csv](../../consumers.csv)에 있다.

- **T 적격 기준.** 행을 정확히 `Point`로 선택하는 마스크나 동등한 필터다. momepy 0/5, libpysal 0/5, Dask-GeoPandas 0/5로 검색 출력 끝까지 결원이다. momepy는 Polygon/Line 계열 분기와 타입 변경 검사였다. libpysal은 Point 전용 컬렉션 gate와 시험의 좌표 개수 assert였다. Dask는 `geom_type` API 위임 및 타입 관련 테스트였다. 동적으로 만든 마스크와 명명하지 않은 타입 상수 전체까지의 부재는 미확인이다. 다음 관측은 세 고정판에서 GeoDataFrame 행을 실제로 타입별 선택한 호출과 결과 ID다.
- **P 적격 기준.** GeoSeries/STRtree/공간 조인의 실제 intersects로 행·짝·입력 매칭 위치를 선택하는 코드 단계 또는 그 호출의 원 시험. 선택 뒤 거리·각도·가공이 있는 경우 그 단계에만 채택한다. 하나의 호환성 분기(`query`/`query_bulk`)는 한 호출로 센다. momepy의 앞 5개는 StreetProfile, SharedWalls, NeighboringStreetOrientationDeviation, enclosure tessellation, enclosures다. 두 Blocks 조인은 `within`이어서 제외했다.
- libpysal P 적격은 4/5다. Voronoi 매핑, Graph fuzzy contiguity, nonplanar neighbors, weights fuzzy contiguity 순이다. Alpha shape는 전체에 대한 bool, shapely_ext는 단일 쌍 bool, Graph `intersects` 테스트는 그래프 집합 연산이라 제외했다. Tabular wrapper는 기본 intersects에 위임하는 구현을 읽었지만 자체 join 시험이 `pass`이고 결과를 갖춘 사용 예를 찾지 못해 보류했다. Buffer를 적용한 nonplanar fallback은 같은 호출의 추가 단계다. 다섯째 실제 원 시험 또는 사용 예는 미확인이다.
- Dask-GeoPandas P 앞 5개는 GeoDataFrame 기본 sjoin(모듈의 행 조인과 한 계통), `_cx_part`의 직접 행 선택, 모듈 sjoin의 partition 후보 쌍, 기본 sjoin 회귀 호출, 공간 분할 `.cx` 회귀 호출이다. 그중 partition 선택은 실제 행 필터의 전 단계다. `within`만 호출한 시험은 별도 반례로 적었다. 사용 가이드의 `usa.cx` 셀은 저장 출력이 즉시 GeoPandas DataFrame이어서 Dask 호출 증거에서 제외했다.
- 세 저장소에서 T가 비어 있어 공개 검색을 넓혔다. Spatial Thoughts의 OSM 주차 notebook에서 원 입력 조회, exact Point 행 선택, 선택 결과의 GeoPackage 저장을 읽었다. 원 notebook에 호출 출력은 비어 있다. 이 근거는 행 타입을 실제 목적에 쓰는 공개 코드이며 GeoParquet 장애 보고나 연구의 유효성 마스크까지 포함한 재현은 아니다. [고정 notebook](https://github.com/spatialthoughts/python-dataviz-web/blob/dd68ad89f88d28bee301e235a4af3bb95fe225ad/supplement_leafmap_osm.ipynb#L138-L198).
