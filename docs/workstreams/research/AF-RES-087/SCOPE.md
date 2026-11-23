# AF-RES-087 실행 전 계획

계획 기준은 `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd`다. 그 판의 중앙 진행표에는 087 행이 아직 없다. 배정 기록 `a940d79`과 작업 브랜치 부재를 확인한 원격 최신 통합판 `9dcae48a47b05d7ba2a1320444be28f5d0fcd739`의 087 행은 같은 브리프를 담고 있다. 실제 시작은 9dcae48이다. 두 판의 AGENTS, STATE, 연구 운영·제품 브리프, 최신 DOT_AUTOMATION과 배정·의존 행을 읽었다. 허용 출력 경로는 이 디렉터리 하나다. [계획판](https://github.com/laadkke-arch/agentflow-open/tree/184137d2f257f5d1a7ef584e0f3a6b35f3d280cd), [시작판 진행표](https://github.com/laadkke-arch/agentflow-open/blob/9dcae48a47b05d7ba2a1320444be28f5d0fcd739/docs/automation/dot-control.json).

직접 의존은 AF-RES-083@f9be0dacdb51603c72f30abd452ce9d349d0ca3b 하나다. HANDOFF, RESULT의 G04-1·G04-2, records 첫 두 행, revisions 첫 두 레코드, REPRODUCE의 GeoPandas 입력을 읽었다. 핵심 안내 두 절은 같은 0.14.4 I/O 가이드 저작에서 나왔고 실제 Parquet 경로는 PyArrow다. 선행판에서 GeoPandas 소비자 실행은 0건이다. 이미 다룬 GDAL 드라이버의 역사 격자, SciPy·Astropy 이관, 하류 안내 재모집 및 patch 역적용은 범위 밖이다. [선행 인계 및 원장](https://github.com/laadkke-arch/agentflow-open/tree/f9be0dacdb51603c72f30abd452ce9d349d0ca3b/docs/workstreams/research/AF-RES-083).

## 고정판과 쓰기 규칙

|역할|Git 태그의 실제 commit|코드에서 확인한 조건|
|---|---|---|
|O|v0.14.4 @ 60c9773e44fff8a35344c2a74431e00c5546a4ee|기본 사양 1.0.0, writer 지원 0.1.0·0.4.0·1.0.0-beta.1·1.0.0. WKB 고정. 읽기 validator는 빈 판 값과 비-WKB를 거절하며 판 허용목록을 조회하는 분기는 없다.|
|N|v1.0.0 @ d8e14e1be3ecbef6f75a1142f85561ff652ed3d1|WKB 기본, WKB 사양 기본 1.0.0, 이전 목록에 1.1.0 추가. 명시 native는 1.1.0, 옵션 미지정 시 native 결과로부터 1.1.0 선택. validator는 WKB와 여섯 가지 단일 geometry 계열 native 인코딩 허용.|

[O 코드](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/geopandas/io/arrow.py), [N 코드](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/arrow.py). 두 writer에서 동일한 PyArrow Parquet 인자 `compression="snappy", index=False, version="2.6"`을 적용한다. 마지막 인자는 Parquet 파일 형식 판이며 표의 사양판 `schema_version`과 독립이다. N의 `write_covering_bbox=False`를 명시한다. 전체 열 bounds인 footer `bbox`는 남을 수 있다. F1의 WKB는 O 구현으로 고정한다.

|파일|writer|schema_version|실제 writer geometry_encoding 인자|기대 footer encoding|사전 기대 O / N|
|---|---|---|---|---|---|
|F1|O|1.0.0|인자 없음|WKB / WKB|둘 다 공간·엄격 통과|
|F2|N|1.0.0|WKB|WKB / WKB|둘 다 공간·엄격 통과|
|F3|N|1.1.0|WKB|WKB / WKB|둘 다 공간·엄격 통과. O 성공은 선언된 1.1.0 전체 지원으로 해석하지 않는다.|
|F4|N|1.1.0|geoarrow|polygon / point, x·y 분리|O ValueError 거절, N 공간·엄격 통과|

공통 입력 [fixtures/input.json](fixtures/input.json)은 역사 테스트의 첫 box와 두 열에 명시한 EPSG:4326을 사용한다. 역사의 원 시험은 별개다. 비대칭 box와 비대칭 Point 열을 함께 두되 각 geometry 열 안의 유형을 고정한다. Point(117,23)는 교차하지 않는 경도·위도 범위의 검증점이다. 한 파일의 bytes를 한 번 읽어 해시한 뒤 메모리 파일로 그대로 전달한다. 생성 실패 파일은 다른 파일로 채우지 않는다. 각 파일·reader의 서로 다른 Python 프로세스 두 번을 실행해 8셀·16자리를 고정한다. 파일 없는 경우 `generation_failed`와 `reader_skip`을 분리한다. 정상 계약 거절에는 reader API의 고유 예외와 종료값을 남긴다. 미설치·import/입력 해시 불일치·비정상 종료 같은 장비 실패는 reader의 계약 거절과 구별한다.

## 독립 판정 두 가지

- **공간 의미:** GeoDataFrame, 활성 열 `geometry`, ID의 유일성과 정확한 대응, 두 geometry dtype과 종류·차원, 각 ID의 좌표값을 확인한다. Polygon은 동일 topology와 정규화 후 좌표 완전 일치를 모두 요구하고 원래 좌표열도 별도 기록한다. Point는 x/y 값 정확 일치를 요구한다. 두 열 모두 명시 CRS가 있어야 한다. CRS는 pyproj의 축 포함/축 무시 동등성을 각각 기록하며, 공간 의미는 축 무시 동등성과 고정 xy 계약에서 `always_xy` 대조 통과를 요구한다. EPSG:4326의 공식 축과 WKB/native에서 사용하는 x/y는 별개로 기록한다. 축에 민감한 소비자는 별도의 축 일치 관측을 적용한다.
- **엄격 속성·스키마:** ID 및 행의 정확한 순서, RangeIndex(0,2), 열 이름과 순서 전부, 비공간 값과 null, pandas dtype과 string 저장 backend, footer Arrow 타입 및 Parquet 물리·논리 타입 일치를 요구한다. geometry 저장 형태는 이번 교차 비교의 독립변수라 엄격 속성 기준에서 제외한다. 공간 판정과 별도로 비교하며, 두 계약의 동시 만족 여부도 보고한다. reader가 거절한 경우 두 계약은 평가 불가이며 파일의 footer 물리 타입은 별도 관측 가능하다.

검증 순서에서 native 인코딩은 하나의 geometry 열 안에서 동종이어야 한다. footer는 제3 경로인 PyArrow와 pyproj로 조사한다. F1/F2의 creator와 Arrow field metadata, F2/F3의 version 외 동반 값, F3/F4의 물리/논리 형태와 확장 이름·metadata, 모든 쌍의 bbox/covering을 대조한다. 바이트가 달라야 할 이유와 메타데이터 차이를 파일 해시 비교와 구별한다.

## 보조 대조와 원 시험

같은 설정으로 맞춘 O/N 의존 환경을 우선하며 별도 venv의 정확 소스 checkout을 가져온다. 원 배포 lock은 제공되지 않았으므로 재구성 환경이다. 원 시험 표본은 O/N `test_write_spec_version`, O/N `test_roundtrip`, N의 `test_read_parquet_geoarrow`·`test_geoarrow_roundtrip`로 고정한다. 원 시험 assert와 스킵 조건을 먼저 읽고 원 프로세스의 실제 수집/통과/실패/스킵을 집계한다. GDAL 제공 fixture와 GeoPandas 소비 시험의 byte·발생 근거를 연결한다.

보조 대조는 (A) plain PyArrow에서 같은 F4의 표와 geometry 저장값 읽기, (B) F3의 공간값과 스키마가 같고 속성 한 칸이 다른 복사본, (C) 같은 Point 입력에 유효 점·null·POINT EMPTY를 두고 N의 WKB/native 1.1.0을 양쪽 reader와 Arrow로 비교, (D) EPSG:4326과 CRS84의 축·transform 교차 확인이다. 보조 입력·실행은 8셀에 산입하지 않는다. C의 native에서 EMPTY가 NaN 좌표로 별도 복구되는지와 null mask가 유지되는지 관측하며 실패를 가정하지 않는다. 이미지와 접근성은 규격과 별도 실제 사례를 연결한다. 자료를 독립 사건 단위로 접고 실패 시도를 분리한다.
