## 표 1 · 네 파일과 footer

| 파일 ID | 원 안내·요구 URL | writer·사양판·인코딩 | 입력·footer·file SHA | 바꾸려던 축·실제 함께 바뀐 값 | 미확인 |
|---|---|---|---|---|---|
| F1 | [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) | O · 1.0.0 · WKB/WKB | [입력 `cba3544746ad`](fixtures/input.json) · [footer `ecf238473752`](evidence/build/F1-footer.stdout.json) · [file `ec572faef2c8`](fixtures/F1.parquet) | 기준 O writer. 두 geometry는 Arrow binary, Parquet BYTE_ARRAY. 전체 bbox 두 개. | 2024년 실제 배포자 lock |
| F2 | [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) | N · 1.0.0 · WKB/WKB | [입력 `cba3544746ad`](fixtures/input.json) · [footer `8c47a0ceba5a`](evidence/build/F2-footer.stdout.json) · [file `ea937b96d5bc`](fixtures/F2.parquet) | F1 대비 writer만 교체. 본문 SHA 동일. creator, geometry 2열에 geoarrow.wkb 확장 이름·CRS metadata, pandas geometry 표시 bytes→empty. | 다른 Arrow extension 소비자 |
| F3 | [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) · [1.1.0 규격](https://geoparquet.org/releases/v1.1.0/) | N · 1.1.0 · WKB/WKB | [입력 `cba3544746ad`](fixtures/input.json) · [footer `af285bd58050`](evidence/build/F3-footer.stdout.json) · [file `975bdce7a75d`](fixtures/F3.parquet) | F2 대비 geo.version만 1.0.0→1.1.0. 본문 SHA 동일. geo 및 직렬 ARROW:schema 해시가 연동. | O의 1.1.0 기능 전체 |
| F4 | [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) · [1.1.0 규격](https://geoparquet.org/releases/v1.1.0/) | N · 1.1.0 · polygon/point | [입력 `cba3544746ad`](fixtures/input.json) · [footer `cb02036faded`](evidence/build/F4-footer.stdout.json) · [file `c8eddc72bf70`](fixtures/F4.parquet) | F3 대비 인코딩 교체. polygon list/list/struct 및 point struct, x/y DOUBLE. Arrow 확장 이름과 Parquet 필드, 파일 본문도 변경. 두 bbox 및 CRS 동일. | 혼형의 전체 범위, 다른 차원/CRS·reader |

## 표 2 · 파일별 두 reader와 두 반복

| 파일·reader·반복 | 실제 환경 지문 | 종료·거절 또는 성공 | geometry·좌표·CRS·축 | 속성·열 순서 | 의미 보존·엄격 스키마 판정 | 원 출력 URL |
|---|---|---|---|---|---|---|
| F1 · O · 1 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L1](runs.jsonl#L1) |
| F1 · O · 2 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L2](runs.jsonl#L2) |
| F1 · N · 1 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L3](runs.jsonl#L3) |
| F1 · N · 2 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L4](runs.jsonl#L4) |
| F2 · O · 1 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L5](runs.jsonl#L5) |
| F2 · O · 2 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L6](runs.jsonl#L6) |
| F2 · N · 1 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L7](runs.jsonl#L7) |
| F2 · N · 2 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L8](runs.jsonl#L8) |
| F3 · O · 1 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L9](runs.jsonl#L9) |
| F3 · O · 2 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L10](runs.jsonl#L10) |
| F3 · N · 1 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L11](runs.jsonl#L11) |
| F3 · N · 2 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L12](runs.jsonl#L12) |
| F4 · O · 1 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 20 · ValueError `Only WKB geometry encoding is supported` | GeoDataFrame 미반환 | reader 출력 없음 | 평가 불가 · 평가 불가 | [출력 L13](runs.jsonl#L13) · [stderr](evidence/reads/F4-O-1.stderr.txt) |
| F4 · O · 2 | [0.14.4@60c9773 · Python 3.12.14 · Arrow 16.1.0](environments.json#L2) | 20 · ValueError `Only WKB geometry encoding is supported` | GeoDataFrame 미반환 | reader 출력 없음 | 평가 불가 · 평가 불가 | [출력 L14](runs.jsonl#L14) · [stderr](evidence/reads/F4-O-2.stderr.txt) |
| F4 · N · 1 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L15](runs.jsonl#L15) |
| F4 · N · 2 | [1.0.0@d8e14e1 · Python 3.12.14 · Arrow 16.1.0](environments.json#L140) | 0 · 성공 | geometry Polygon×2, box(0,0,10,10)/box(115,20,119,26). probe Point (2,7)/(117,23). 두 CRS EPSG:4326, 공식 북/동·저장 x/y. | 2행 A-01/B-07, score 7/null, label 제주/delta, enabled 참/거짓. feature_id, geometry, score, label, probe, enabled 순. | 통과 · 통과 | [출력 L16](runs.jsonl#L16) |

## 표 3 · 독자 목적별 반환

| 독자 목적과 판 | 유지·판 한정·되묻기·보류 | 지지하는 동일 파일의 두 실행 | 반대 입력 | 반환할 안내·시험 링크 | 미확인 |
|---|---|---|---|---|---|
| 생산자 · O/N 혼용 배포 | **유지** · 양쪽이 필요한 새 파일은 WKB 1.0.0을 명시한다. | F2 O/N 각 2회 보존 [L5–8](runs.jsonl#L5-L8) | F4는 O 거절. F2는 reader 변경을 금지해도 유지. | 두 원 절 [G04-1·2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L285) · [F2 writer](evidence/build/F2-writer.stdout.json) | 새로운 도구나 사용자 실제 설치판 |
| 생산자 · N 전용이며 각 geometry 열에 동종 타입 | **판 한정** · native 1.1.0을 명시하고 목적에 맞는 geometry 타입을 검증한다. | F4 O 2회 거절/N 2회 보존 [L13–16](runs.jsonl#L13-L16) | [G-native](evidence/auxiliary/G-native.json)는 N에서도 Point→MultiPoint | [N의 I/O 절](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/doc/source/docs/user_guide/io.rst#L269-L282) · [N native 원 시험](evidence/upstream/pytest-N.txt) | 처리량·다른 지오메트리 계열 |
| WKB 전용 소비자 · O 고정, 새 파일의 인코딩/판 미제공 | **되묻기** · 파일 SHA와 footer의 version 및 geometry별 encoding을 확인한다. F3 유형은 확인 후 판 한정으로 읽는다. | F3 O/N 각 2회 보존 [L9–12](runs.jsonl#L9-L12) | F3와 사양판이 같은 F4의 O 거절 [L13–14](runs.jsonl#L13-L14) | [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) · [O validator](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/geopandas/io/arrow.py#L205-L238) | 제공되지 않은 파일의 encoding, epoch/edges |
| WKB 전용 소비자 · O 고정, 제공 파일이 F4 | **보류** · O에서 쓸 수 있는 WKB 파일이 필요하다. | F4 O/N 동일 SHA [L13–16](runs.jsonl#L13-L16) | 인코딩 협의 없이 사양판만 낮추면 [N 쓰기 validator](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/arrow.py#L326-L350)의 native 제약에 걸린다. 기존 F1은 [L1–4](runs.jsonl#L1-L4) 보존. | [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) · [F4 거절](evidence/reads/F4-O-1.stderr.txt) | 원 생산자가 WKB 재발행 가능한지 |
| 정확한 속성 스키마 소비자 · O/N 및 검증한 입력 | **유지** · 순서·ID·값·dtype·물리 타입 대조를 통과한 F1–F3와 N의 F4에서만 확정한다. E의 새 열은 계약을 완화할 때만 수용한다. | F2 O/N [L5–8](runs.jsonl#L5-L8), F4 N [L15–16](runs.jsonl#L15-L16) | [B 값 1칸](evidence/auxiliary/B-cell.json)·[F dtype](evidence/auxiliary/F-no-pandas-meta.json)은 새 열 허용 후에도 엄격 기준 미달. | [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [검증과 재현](reproduce.md) · [E](evidence/auxiliary/E-added.json) | 생산자의 pandas metadata/타입 정책 |

### 분모와 판정

| 항목 | 실측 / 계획 |
|---|---|
| 네 생성 파일과 제3 footer | 4/4 생성, 4/4 판독. F1/F2·F2/F3·F3/F4 비교 3/3. 생성 실패 0. |
| 동일 파일 bytes의 대응쌍 | 4/4 SHA에서 O/N 양쪽에 입력. 파일×reader 셀 8/8 판독. |
| 서로 다른 Python 프로세스 | 16/16 실행. 두 반복 분류 8/8 일치. 보존 14, 명시적 거절 2, 조용한 손실 0, skip 0, 장비 실패 0. |
| 두 계약 | API 성공 14/14에서 공간·엄격 모두 통과. 전체 16자리 중 양쪽 계약 통과 14, 계약 거절 때문에 평가 불가 2. |
| 원 pytest | 48/48 선택 케이스 통과, 실패·스킵 0. O 17, N 31. Parquet·Feather 포함, 역사 GDAL 쓰기 재실행 0. |
| 보조 시험 | A–G 7군, 성공적인 계기 판독 20/20 자리. GeoPandas 호출 18(반환 16, 거절 2)과 일반표/축 계산 2. 첫 F 계기 실패 2회는 별도. |
| 직접 자료 | 55 산입 행, URL 문서 51, 독립 원저작·사건 35. 상속 연구 5행 별도. 독립 GIS 소비 8사건·반대 근거 9사건·이미지 2사건·접근성 2사건. |
| 원 안내의 하류 재사용 또는 정정 필요성을 확정할 실제 사례 | 0개. 정정 적중률은 0/0 산출 불가. |

**REVIEW_READY**. 옛 안내를 두 판 모두에서 쓸 때는 검증한 WKB 범위로 반환한다. 1.1.0이라는 판만으로 O의 결과를 예측할 수 없었다. F3의 WKB는 보존됐고 F4의 native는 명시적으로 거절됐다. N의 native 반환에는 geometry 타입과 독자 계약의 확인이 추가된다.

표 1의 해시는 접두사다. 전체 SHA-256과 writer/footer 종료값은 [files.csv](files.csv)에 있으며 입력 SHA·판정 기준은 [manifest.json](manifest.json)으로 고정했다. 표 2의 실제 사용 라이브러리 전체와 import 경로는 [environments.json](environments.json)에 있다. 원 출력의 geometry 좌표열 및 속성 검정은 반복별로 열어 볼 수 있다.

## Q1 · 원 안내와 테스트의 계약

G04-1의 약속은 GeoPandas API로 왕복할 때 공간 정보가 유지된다는 것이다. 구체적인 geometry·CRS 기대는 배포 시험에서 확인한다. G04-2에서 “files of any version”을 해석할 때 직전 문장의 GeoParquet **1.0.0 추적**과 이전 판 지원을 함께 본다. 1.0.0의 후속 I/O 절은 특정판 언급을 빼고 문구를 일반화했다. **두 원 안내 절에 정확한 열 순서, dtype 또는 물리 스키마를 요구한 문장은 없다.** [O 원 안내](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L285) · [N 원 안내](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/doc/source/docs/user_guide/io.rst#L269-L282).

O writer의 기본은 WKB와 사양 1.0.0이다. 쓸 수 있는 값은 0.1.0, 0.4.0, 1.0.0-beta.1, 1.0.0이다. N은 1.1.0을 추가했으며 기본 WKB의 사양은 그대로 1.0.0이다. native를 선택하면 사양 미지정에서 1.1.0을 택하고, 명시했다면 이 판의 구현에서 1.1.0이어야 한다. 두 reader의 validator는 판 값 및 필요한 키가 있는지 확인한 뒤 geometry별 encoding에 따라 분기한다. O는 WKB만, N은 WKB와 point/linestring/polygon 및 각 multi를 받는다. 따라서 N 안내의 “latest”도 이 고정판에서는 **인코딩별 기본값**으로 풀어야 한다. [O 작성·읽기](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/geopandas/io/arrow.py#L88-L130) · [O validator](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/geopandas/io/arrow.py#L205-L248) · [N 작성·읽기](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/arrow.py#L134-L194) · [N validator](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/arrow.py#L270-L315).

원 `test_write_spec_version`은 box(0,0,10,10) 한 행, EPSG:4326, WKT 또는 PROJJSON과 Polygon의 표기를 검증한다. `test_roundtrip` 및 GDAL fixture 시험은 속성이 있는 frame과 기본 열 순서도 비교한다. `test_geoarrow_roundtrip`·`test_read_parquet_geoarrow`에서는 공식 파일의 정수 열과 geometry/CRS를 비교한다. 원 비교기에는 순서와 dtype 검사가 있지만 topology 위주의 geometry 비교이며 exact 링 직렬 순서나 Parquet 물리 dtype을 지정하지 않는다. 이 연구는 원 좌표열을 기록하고 geometry의 정규화 좌표와 속성의 Parquet 물리 dtype을 별도로 검증했다. 3.5.0 GDAL의 Parquet footer가 **0.3.0/WKB**라는 실측은 writer 목록과 reader 행동이 별개라는 독립 반례다. N의 3.9.0 fixture는 CRS 키가 없는 **1.0.0/WKB**이며, 원 시험은 CRS84와 bbox 필터 1행을 확인한다. [원 assert·skip·실행 메모](evidence/upstream/notes.md) · [fixture footer](evidence/upstream/fixture-fingerprints.json).

GeoParquet 1.1의 호환성 절은 구 구현이 새 입력을 올바르게 해석하거나 해석할 수 없음을 알아차리는 두 경우를 둔다. F4의 O 거절과 F3의 O 보존은 이 관찰 범위에서 양립한다. [1.1.0 Version Compatibility](https://geoparquet.org/releases/v1.1.0/#version-compatibility).

## Q2 · 실제 import와 의존판

|항목|O|N|
|---|---|---|
|태그·코드|v0.14.4 · `60c9773e44fff8a35344c2a74431e00c5546a4ee`|v1.0.0 · `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1`|
|실제 package import| `/tmp/af087/src-O/geopandas/__init__.py` | `/tmp/af087/src-N/geopandas/__init__.py` |
|실제 Arrow I/O import| `/tmp/af087/src-O/geopandas/io/arrow.py` | `/tmp/af087/src-N/geopandas/io/arrow.py` |
|실행 파일| `/tmp/af087/venv-O/bin/python` | `/tmp/af087/venv-N/bin/python` |
|동일 CPython·플랫폼|3.12.14, Linux 6.18.57 x86_64, glibc 2.41|동일|
|동일 패키지·라이브러리|pandas 2.2.2, NumPy 1.26.4, PyArrow/C++ Arrow 16.1.0, Shapely 2.0.4 / GEOS 3.11.3, pyproj 3.6.1 / PROJ 9.3.0|동일|
|벡터 I/O|Fiona 1.9.6 (GDAL 3.6.4)와 Pyogrio 0.9.0 (GDAL 3.8.5) 모두 설치, 기본 `read_file`은 Fiona|패키지는 동일, 기본 `read_file`은 Pyogrio|

두 venv는 같은 휠 파일 집합을 사용했다. package/배포판 이름뿐 아니라 import 경로와 Git HEAD를 매 프로세스 검증했다. 서로 다른 것은 GeoPandas 자체·checkout·venv 경로와 upstream 벡터 입력의 기본 engine이다. F1–F4의 호출 대상은 PyArrow 경로다. 같은 F4 bytes에서 갈라진 결과와 예외는 이 스택의 두 고정 구현에 귀속할 수 있다. 벡터 upstream 시험에서 엔진 효과만 비교하려면 같은 태그·같은 벡터 bytes에서 engine을 명시해 Fiona/Pyogrio 한 축을 바꾼다. PyArrow 또는 Shapely 효과만 분리하려면 한 번에 그 휠만 교체하여 동일 파일·태그를 읽고, 변환 생성 문제에는 동일 입력을 그 writer로 다시 쓴 짝을 추가한다. [환경과 휠](environments.json) · [설치 증거](evidence/build/installation.json) · [O CI 요청](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/ci/envs/39-minimal.yaml#L5-L26) · [N CI 요청](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/ci/envs/39-minimal.yaml#L5-L28).

원 발행자의 resolved lock과 실제 하류 런타임 지문은 확보하지 못했다. 이번 환경은 재구성이다. 최소 CI 요청의 PyArrow 8.0.0과 10.0 및 Shapely 1.8.0과 2.0.0은 교차 왕복 실측값과 구별한다. [v1.0.0 릴리스 기록](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/CHANGELOG.md#L3-L11).

## Q3 · 실제로 바뀐 값

공통 입력은 역사 box에 비대칭 polygon, 두 번째 geometry인 Point probe, ID와 타입이 정해진 속성을 보탰다. N writer의 native 옵션은 각 geometry 열에 다른 native encoding을 적용한다. N의 `write_covering_bbox=False`를 명시했다. 네 footer 모두 열 전체 bounds `bbox` 두 개를 갖고, covering이나 bbox 열은 없다. EPSG:4326 PROJJSON과 primary geometry, geometry type 목록, row count, Parquet `version=2.6` 및 Snappy 정책은 동일했다. footer 검사 경로는 GeoPandas reader 밖의 PyArrow 16.1.0과 CRS 객체를 해석하는 pyproj다. [files.csv](files.csv) · [footer 원 출력과 diff](evidence/build/footer-differences.json).

- **F1/F2, writer 교체.** 헤더를 포함해 footer 이전의 바이트는 완전 동일하다. N은 두 WKB field에 GeoArrow extension name/CRS metadata를 붙인다. pandas의 두 geometry 표기는 bytes에서 empty로 바뀌며 실제 geometry 저장은 binary로 같다. creator 판과 관련 metadata 해시도 따라 바뀐다. 이 비교에서 달라진 것은 writer가 만든 여러 metadata이며, 각 필드의 개별 인과는 이 쌍에서 분리되지 않는다. [data section](evidence/build/data-sections.json) · [footer diff](evidence/build/footer-differences.json).
- **F2/F3, 사양판 교체.** data section SHA가 같고, 구조상 달라진 값은 `geo.version`뿐이다. 같은 JSON을 포함하는 `geo`와 `ARROW:schema` SHA는 같이 변했다. 이 쌍에서 O의 WKB 처리 결과가 바뀌지 않았다. [F2/F3 footer diff](evidence/build/footer-differences.json) · [L5–12](runs.jsonl#L5-L12).
- **F3/F4, 인코딩 옵션 교체.** writer 인자 한 개를 바꿨는데 결과에는 geo encoding, nested Arrow/Parquet storage 타입 및 extension 필드, data section SHA가 함께 바뀌었다. 이를 **인코딩과 storage의 복합 변화**로 취급한다. O 거절의 직접 조건은 읽기 validator가 보고한 non-WKB encoding이다. field를 하나씩 무시하는 다른 reader의 결과는 이 대조에서 분리하지 않았다. [F4 실제 인자](evidence/build/F4-writer.stdout.json) · [F4 footer](evidence/build/F4-footer.stdout.json) · [O traceback](evidence/reads/F4-O-1.stderr.txt).

## Q4 · 반환값과 엄격 스키마

14개 정상 반환 모두 2행의 A-01/B-07 대응이 같았다. Polygon의 위상과 정규화 좌표가 같고, 비대칭 `probe=(117,23)`은 순서가 유지됐다. 두 geometry 열의 CRS는 모두 명시 EPSG:4326이고 CRS 축 포함 비교도 통과했다. 파일 좌표는 x/y 경도/위도 순이며 EPSG:4326의 authority 축은 북/동이다. 비공간 열은 `feature_id`, `label`의 pandas `string[python]`/Arrow string/Parquet BYTE_ARRAY, `score`의 pandas Int16/Arrow int16/Parquet INT32 (signed 16-bit 논리), `enabled`의 pandas boolean/Arrow bool/Parquet BOOLEAN이었다. null, 값, 전체 열과 행 순서, RangeIndex가 유지됐다. 16자리에서 생성 SHA와 호출 bytes SHA가 일치했다. [16개 원 실행](runs.jsonl) · [고정 계약](SCOPE.md).

CRS 보조 D는 동일 숫자가 맥락에 따라 어떤 좌표가 되는지 보인다. 두 reader가 CRS **키 생략**을 CRS84로 읽었다. CRS84와 EPSG:4326은 축을 포함한 `equals`에서 False, 축 무시에서는 True다. `always_xy`로 (117,23)을 3857로 보내면 둘 다 (13024380.422813008, 2632018.6375864246)이다. authority 순서로 같은 tuple을 넘기면 EPSG:4326 쪽은 위도 117°로 해석되어 무한대 응답이었다. CRS를 **명시 null**로 두면 양쪽 모두 geometry와 속성을 반환하지만 CRS는 None, 공간 계약은 실패했다. [CRS axis 실행](evidence/auxiliary/D-axis-comparison.json) · [생략](evidence/auxiliary/D-missing-crs.json) · [명시 null](evidence/auxiliary/D-null-crs.json) · [GeoParquet CRS 규격](https://geoparquet.org/releases/v1.1.0/#crs).

## Q5 · 반례와 유지 사례

|대조|실제 관측과 독자의 손익|
|---|---|
|옛·새 WKB, F1–F3|세 파일 모두 O/N 12자리에서 독립 계약이 유지됐다. F3는 1.1.0 번호 자체만으로 O가 거절한다는 가정을 반박한다. [L1–12](runs.jsonl#L1-L12)|
|같은 1.1.0의 F4|O 두 실행은 exact ValueError와 harness 종료 20으로 명시 거절했다. N 두 실행은 두 계약을 통과했다. [L13–16](runs.jsonl#L13-L16)|
|A 일반 표 경로|F4의 같은 bytes를 PyArrow가 Table로 열었고 `geo` metadata도 남았다. pandas 변환은 object형 geometry와 활성 geometry 없는 DataFrame을 반환했다. 공급한 metadata의 존재와 공간 변환은 따로 판정한다. [A 원 출력](evidence/auxiliary/A-pyarrow.json)|
|B 동일 geometry, 속성 1칸|F3 입력의 A-01 score만 7→8로 바꾼 통제 파일이다. O/N의 공간 계약은 True, 엄격은 False이며 다른 속성과 물리 타입이 같다. 이는 검사의 민감도 확인이다. [B 원 출력](evidence/auxiliary/B-cell.json)|
|C null과 EMPTY|WKB 성공 2/2, native N 성공 1/1에서 `POINT (117 23)`, None, `POINT EMPTY` 구분이 유지됐다. native storage는 유효 mask [true,false,true]와 EMPTY의 두 NaN으로 확인했다. O의 native는 거절했다. 우려했던 EMPTY/None 합쳐짐은 이 환경에서 발생하지 않았다. [C-WKB](evidence/auxiliary/C-WKB.json) · [C-native](evidence/auxiliary/C-native.json) · [Shapely 2.0.4 전후 원 이슈](https://github.com/shapely/shapely/pull/2034)|
|D CRS 메타데이터|같은 F1 좌표를 써도 생략은 CRS84, 명시 null은 CRS 불명이다. 대칭 box만으로는 축 문제를 확인하기 어려워 별도 probe를 썼다. [D 축 실행](evidence/auxiliary/D-axis-comparison.json)|
|E 열 추가|동일 공간·기존 스키마에 `new_flag` 추가는 O/N 모두 엄격 판정 실패, 추가 비공간 열 허용 계약에서는 양쪽 통과였다. [E 원 출력](evidence/auxiliary/E-added.json)|
|F pandas metadata 제거|F3의 `pandas` metadata를 제거해 재기록했다. O/N은 geometry·CRS를 복원했다. `score`는 물리 INT32·논리 int16이지만 pandas Int16의 7/NA에서 float64의 7.0/NaN으로 바뀌었다. 문자열은 object, nullable boolean은 bool이 됐다. [F 원 출력](evidence/auxiliary/F-no-pandas-meta.json) · [Arrow Pandas Integration](https://arrow.apache.org/docs/16.1/python/pandas.html#nullable-types)|
|G 혼형 추가 탐색|한 열의 Point와 MultiPoint를 함께 쓰면 WKB에서 O/N 모두 타입이 유지됐다. N의 native 출력은 양쪽 행의 위상 동등성이 True지만 Point를 MultiPoint로 읽었다. geo metadata 유형 목록에는 원래 Point도 있었고, 개별 행 타입을 되돌리는 정보는 기록되지 않았다. [G-WKB](evidence/auxiliary/G-WKB.json) · [G-native](evidence/auxiliary/G-native.json) · [Shapely 동작 설명](https://shapely.readthedocs.io/en/2.0.4/reference/shapely.to_ragged_array.html)|

독립 자료의 관측을 붙이면 양성과 실패의 원인이 더 명확하다. GDAL 3.5.0의 WKB와 공식 GeoParquet→N fixture는 실제 읽기에 성공했다. Dask 소비자는 같은 SGP 파일에 대해 GeoPandas의 polygon 표를 보고했지만 dask-geopandas의 CRS 키 접근은 실패했다. Polars 소비자는 처음 geoarrow.wkb Arrow extension을 거절했고 후기 1.39.3은 binary로 받아들였다. Sedona 보고에서는 writer의 frame CRS가 파일에서 null이 됐다. DuckDB Python은 Overture geometry의 CRS 타입을 표시하더라도 실제 값을 반환하지 못했고, 별도의 PUDL dbt는 주입한 CRS 메타데이터에서 실패했다. Arrow extension이 있지만 파일 수준 geo가 빠진 파일을 직접 읽은 #3475의 ValueError도 별개다. 이 사건들은 버전·output 목적을 명시할 이유를 주며 이 연구의 고정 8셀을 대체하지 않는다. [원장 S11–S12·S22·S36–S41](sources.jsonl) · [Dask 270](https://github.com/geopandas/dask-geopandas/issues/270) · [Polars 20978](https://github.com/pola-rs/polars/issues/20978) · [Sedona 3375](https://github.com/apache/sedona/issues/3375) · [DuckDB 766](https://github.com/duckdb/duckdb-spatial/issues/766) · [PUDL 5074](https://github.com/catalyst-cooperative/pudl/issues/5074) · [GeoPandas 3475](https://github.com/geopandas/geopandas/issues/3475).

## Q6 · 한 조건만 바꾼 답

1. **reader 판을 바꿀 수 없다.** 파일 F4, 생산자 및 보존 기준이 그대로라면 N에서의 판 한정 사용이 O 고정에서 보류로 바뀐다. 기존 F2는 똑같은 제약을 줘도 보존된다. 새 쓰기를 통제하는 생산자는 F2 조합으로 돌아갈 수 있다. 공간 객체가 필요한 WKB 소비자가 파일의 실제 encoding을 모르면 먼저 footer를 확인한다. [G04-2](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) · [F4 동일 bytes 실행](runs.jsonl#L13-L16) · [F2 동일 bytes 실행](runs.jsonl#L5-L8).
2. **새 속성 열만 허용한다.** 동일 E 파일과 reader, 공간·기존 값·dtype 요구를 유지한 채 열 추가만 허용하면 보류에서 수용으로 바뀐다. B 파일은 기존 score가 다르며, F 파일은 기존 dtype이 달라서 답이 그대로다. 이는 열 확장 권한과 기존 계약 완화를 구별하는 경우다. [G04-1](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) · [E](evidence/auxiliary/E-added.json) · [B](evidence/auxiliary/B-cell.json) · [F](evidence/auxiliary/F-no-pandas-meta.json).

이력에서 3348의 발행자 목적은 낡기 쉬운 표기의 정리였고, 3391은 벡터 I/O의 `use_arrow=True` 안내를 고치면서 공간 왕복의 취지를 유지했다. 실제 하류가 이 두 원 절을 그대로 적용해 실패했다는 공개 기록은 확보하지 못했다. 이번에 제시한 조건은 독자에게 원 안내를 반환하는 판단이다. 발행자가 반드시 정정해야 했는지는 보류한다. [3348 작성자](https://github.com/geopandas/geopandas/pull/3348) · [3348 diff](https://github.com/geopandas/geopandas/commit/7c621fe8434d148a77738a0fc37edcd16dd0ab38) · [3391 diff](https://github.com/geopandas/geopandas/commit/6286f13f8de8748edfa1ed9bc7deb4d05b83a300).

## Q7 · 색 표현과 논리 읽기 순서

|분야|원 규격과 읽는 기능|실제 적용/실패 기록|적용할 조건과 한계|
|---|---|---|---|
|색 프로파일|PNG 2판 iCCP는 샘플을 ICC 색공간에 연결한다. CSS Color 4 §3.4는 유효한 tagged 이미지의 지정 색공간 적용을 요구한다. [PNG §11.3.3.3](https://www.w3.org/TR/2003/REC-PNG-20031110/#11iCCP) · [CSS Color 4](https://www.w3.org/TR/css-color-4/#tagged-images)|① Firefox 1.5.0.3/Minefield에서 iCCP 비교 색이 다르다는 보고 및 별도 확인. ② Lilley의 2022년 Chrome/Edge/Firefox/Safari 결과에서 ICC v2/v4 패치가 각각 참조색과 일치. [Mozilla 338277](https://bugzilla.mozilla.org/show_bug.cgi?id=338277#c0) · [Lilley 결과](https://svgees.us/PNG/iCCP/results.html)|PNG 판과 프로파일·디스플레이 조건을 함께 기록한다. 바이트/샘플이 같아도 색공간을 대체하면 색이 달라질 수 있다. 실제 색상 비교는 gamut·렌더링 인텐트에 의존한다.|
|PDF 접근성|WCAG 2.2 1.3.2와 PDF3은 의미에 맞는 읽기 순서의 프로그램적 확인을 요구하거나 시험한다. PDF/UA-1의 Matterhorn 09-001은 사람이 확인하며 veraPDF는 PDF/UA에서 기계 확인만 실행한다고 설명한다. [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#meaningful-sequence) · [PDF3](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3) · [Matterhorn](https://pdfa.org/wp-content/uploads/2021/04/Matterhorn-Protocol-1-1.pdf) · [veraPDF](https://docs.verapdf.org/validation/)|① PDF Association의 PASS/FAIL 두 파일은 모두 PDF 1.7·Tagged=yes였다. 이번 Poppler에서 레이아웃 텍스트는 둘 다 H1→1→2→3이나 실패본 태그는 2→H1→3→1이었다. ② 사용자의 이어지는 표는 Acrobat/NVDA에서 서로 달랐으며 둘 다 의도한 페이지별 순서를 지키지 못했다. Adobe는 실제 태그 위치를 확인했다. [PASS](https://pdfa.org/techniques-for-accessible-pdf/content-order-correctly-set/UA1_Tpdf-G4_01/) · [FAIL](https://pdfa.org/techniques-for-accessible-pdf/content-order-incorrectly-set/UA1_Tpdf-G4_F01/) · [Poppler 실행](evidence/other/pdf-tag-order.json) · [Adobe 사례](https://community.adobe.com/questions-9/tagged-pdf-x-reading-order-issue-1627355)|같은 판·같은 표시 성공이라도 기능별 반환을 따로 잰다. Poppler 출력은 태그/레이아웃 추출이며 화면 낭독 실행은 Adobe 사례의 보고에 근거한다.|

형식판 지원표에 의존할 때도, 판·feature·reader·입력 SHA별로 **open 결과와 사용자가 기대한 값의 비교**를 두 칸에 기록할 수 있다. 이 조사의 WKB split, iCCP 적용 여부, PDF 태그 순서 모두 이 방식으로 검토할 수 있다. 이미지의 색 변환은 올바른 색을 보이려 샘플 수치를 바꿀 수 있다. GeoParquet의 고정 x/y 계약에서 y/x를 바꾸는 것은 같은 행·같은 위치의 보존이 아니며, 원 CRS가 투영좌표라면 파일의 CRS 키를 지운 뒤 CRS84로 읽어도 같은 좌표 해석이 아니다. 문서는 문맥상 둘 이상의 읽기 순서를 허용할 수 있지만 Point 타입과 정확한 속성 열 순서를 요구한 소비자에게는 허용 범위를 바꾸면 답도 달라진다. [CRS 축/누락 대조](evidence/auxiliary/D-axis-comparison.json) · [혼형 geometry](evidence/auxiliary/G-native.json) · [열 추가](evidence/auxiliary/E-added.json).

## 주요 약점과 판단을 바꿀 조사 3건

1. **F4 양성은 동종 2D의 짝에서 성립한다.** G에서 타입이 바뀌므로 native를 공간 정보 전체에 일반화할 수 없다. 다음 대상은 N writer의 native와 WKB, 입력은 같은 열에 2D/3D Point 및 MultiPoint가 있는 고정 소표본, 바꿀 관측은 per-row 타입·Z 좌표·null/EMPTY 및 footer geometry_types의 보존이다.
2. **동일 재구성 스택 한 조합에서만 두 release를 격리했다.** 다음 대상은 동일 O/N과 한 패키지의 두 판이며, 입력은 F3/F4와 C의 해시가 고정된 파일이다. Shapely 한 판 또는 PyArrow 한 판만 차례로 바꿔 읽고 C의 새 생성도 따로 확인한다. 설치/호출/geometry/CRS/dtype 차이가 재현되면 권고에 해당 의존판을 붙인다.
3. **원 문장 때문에 실제 독자가 실패했는지 미확인이다.** 다음 대상은 G04-2의 “any version”을 실제 인용한 하류 설정 또는 장애 보고다. 인용 문단, 실제 import SHA, 실패 파일 bytes와 의도한 출력이 입력이다. 그 조합에서 거절 또는 조용한 손실이 확인되고 범위 주석이 독자의 선택을 바꾸면 발행자의 필수 정정 여부를 재평가한다.
