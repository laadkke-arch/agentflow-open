# G04 후속판 대조 결과

상태: **PARTIAL — 원래 세 자리 중 두 자리만 실제 소비 안내로 모집됐다.** 후속판은 ② 원격 봉인 `35d7e18024cced8cc81f9397b65e90e0e74bb907` 이후에 처음 취득했다. 첫 취득 UTC는 `2026-11-23T13:35:21.896212+00:00`이다. 원래 `records.jsonl`, `proposals.csv`, `frame.csv`는 봉인 당시 내용으로 보존한다.

## 분모와 관측

| 점검 | G04 결과 | 뜻과 한계 |
|---|---:|---|
| 원 모집 자리 | 3 | G04-1, G04-2, G04-3 |
| 적격 원 안내 | 2/3 | 두 안내 모두 GeoPandas 한 가이드의 서로 다른 행동; 독립 안내 저작은 1 |
| 공석 | 1/3 | G04-3. Arrow의 일반 Parquet 표 예제를 공간 안내로 바꾸어 세지 않음 |
| 옛판·첫후속·최신판 원문 확보 | 2/2 실제 안내 | 0.14.4 → 1.0.0 → 1.2.0 |
| 해당 원문 범위의 실제 발행자 편집 | 2/2 | G04-1은 최신판의 메서드 참조 qualification, G04-2는 첫후속판의 사양판 문구 변경 |
| 독립적으로 확정한 필수 동작 정정 | 0 | 발행자의 편집 사실이 곧 동작 오류의 확정은 아님 |
| A/B 정오 비교 가능 행 | 0 | 불필요한 변경·놓친 변경의 비율은 모두 **0/0, 산출 불가** |
| A 제안 분포 | 보류 2/2 | 두 안내 모두 옛 GDAL `GEOARROW` 옵션을 직접 호출하지 않음 |
| B 제안 분포 | 유지 1/2, 예방적 범위 명시 1/2 | 정오 평가 결과가 아닌 봉인 제안의 종류 |
| 정적 유지 근거가 있는 행 | 1 | G04-1의 이름·WKB 기본값·시험의 관측 기준; 모든 입력의 실행 성공을 뜻하지 않음 |
| 이 조사에서 수행한 소비자 기능 실행 | 0 | 고정판 원문·시험 선언·릴리스·실제 병합 변경을 읽었음 |

`postseal/record-fingerprints.json`에서 G04-1은 옛판과 첫후속판의 네 행 해시가 같고 최신판은 다르다. G04-2는 옛판과 첫후속판이 다르고 첫후속판과 최신판의 일곱 행 해시는 같다. 두 레코드를 모두 “그대로 발행”으로 묶거나, 같은 문단을 세 판에서 읽었다는 이유로 세 정정 사건으로 세면 안 된다.

검색 분모는 QGIS 110개, GeoPandas 60개, Arrow 231개 파일이다. 봉인 `frame.csv`의 G04-C01 설명에 적힌 111은 단순 전사 오류다. G083-S10의 제한 설명에 남은 “third slot fills”도 초안 잔여 문구로, 실제 봉인 원장 전반의 G04-3 공석과 충돌한다. 해당 Arrow 안내의 제외 이유는 공간 정보 계약이 없는 일반 Parquet 예제이기 때문이며 자리 초과가 아니다. 두 수정의 근거와 영향을 `postseal/corrections.jsonl`에 남겼다. 봉인본을 고쳐 사전 관측을 소급 변경하지 않았다.

## G04-1 — 공간 정보 보존 왕복 안내

옛 [GeoPandas 0.14.4 안내 L272–275](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275)는 `read_parquet`와 `GeoDataFrame.to_parquet`로 공간 정보를 보존하는 왕복을 권한다. 그 문단에는 구체 입력, geometry 인코딩 선택, CRS 번호, 메타데이터 바이트 동일성의 약속이 없다. 구현의 기본 WKB와 지원 사양판은 별도 원문 근거다. Fiona/GDAL이 패키지 의존성에 들어 있다는 사실은 이 Parquet 함수가 GDAL `GEOARROW` 옵션을 호출한다는 증거가 아니다. 이 경로는 PyArrow를 호출한다. 근거: G083-S01–S06.

[1.0.0의 같은 문단 L269–272](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/doc/source/docs/user_guide/io.rst#L269-L272)은 그대로다. [1.2.0 L308–311](https://github.com/geopandas/geopandas/blob/199fc53c8a1b87fe4f11d7a8f69f0d1408d9ef71/doc/source/docs/user_guide/io.rst#L308-L311)은 `GeoDataFrame` 메서드 교차참조를 `geopandas.GeoDataFrame`으로 명확히 한다. 주변 도입문에는 GeoParquet 웹사이트 링크가 추가됐다. 실제 변경 ID는 **PUBLISHER-GEO-3391**, [병합 커밋 6286f13f](https://github.com/geopandas/geopandas/commit/6286f13f8de8748edfa1ed9bc7deb4d05b83a300)이다. [원 요청 3386](https://github.com/geopandas/geopandas/issues/3386)은 `read_file`/`to_file`의 `use_arrow=True` 안내를 찾지 못한 독자를 위한 설명을 요구했다. 이것은 Pyogrio의 Arrow 전송 기능이며 GeoParquet native geometry 인코딩과 구분해야 한다. 공간 왕복 안내가 GDAL 3.9 때문에 틀렸다는 당사자 설명은 발견하지 못했다. 근거: G083-S11, S12, P1, P3, S16.

따라서 A는 일괄 치환할 동일 옛 대상을 찾지 못해 보류한다. B의 옛 WKB 지원 범위 유지에는 정적 근거가 있다. 079의 GN04 성공은 다른 호출자와 입력에서의 관측이고, GN05의 조용한 geometry/CRS 손실은 GeoPandas 관측이 아니다. 이를 이 안내의 성공 또는 실패로 옮겨 적지 않았다.

## G04-2 — 사양판 선택과 읽기 범위

옛 [0.14.4 L279–285](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285)는 당시 1.0.0 사양을 맥락으로 `schema_version`에 의한 옛판 선택과 여러 판의 읽기를 설명한다. 이를 아직 나오지 않은 모든 geometry 인코딩까지 읽겠다는 명시적 약속으로 해석하지 않았다. 옛 구현은 WKB 이외의 인코딩을 거부한다. GN05의 옛 GDAL처럼 정상 종료하면서 geometry를 빠뜨리는 동일 실패라고 단정할 수 없다. 근거: G083-S01, S02, S03.

[1.0.0 L276–282](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/doc/source/docs/user_guide/io.rst#L276-L282)에서는 1.0.0을 지칭하던 문장이 사라지고 사양 저장소 중심으로 일반화된다. `schema_version`과 여러 GeoParquet 판을 읽는다는 안내는 남았다. 이 일곱 행은 [1.2.0 L315–321](https://github.com/geopandas/geopandas/blob/199fc53c8a1b87fe4f11d7a8f69f0d1408d9ef71/doc/source/docs/user_guide/io.rst#L315-L321)에서도 동일하다. 실제 변경 ID **PUBLISHER-GEO-3348**의 [병합 커밋 7c621fe8](https://github.com/geopandas/geopandas/commit/7c621fe8434d148a77738a0fc37edcd16dd0ab38)과 [PR 3348](https://github.com/geopandas/geopandas/pull/3348)에서 작성자는 오래되기 쉬운 문구를 피하려 했다고 설명한다. GDAL 3.9에서 발생한 구체적 동작 손실을 수정 이유로 적지는 않았다. 병합 댓글의 되돌릴 수 있다는 표현은 실제 되돌림의 증거가 아니다. 근거: G083-P0, P2, S17.

후속 구현은 native GeoArrow 인코딩을 지원하지만 기본 쓰기는 WKB로 유지한다. [읽기 PR 3278](https://github.com/geopandas/geopandas/pull/3278), [쓰기 PR 3275](https://github.com/geopandas/geopandas/pull/3275), [이슈 3253](https://github.com/geopandas/geopandas/issues/3253)은 하나의 native 인코딩 사건으로 묶었다. 1.0.0의 비-WKB 쓰기는 사양 1.1.0과 `interleaved=False`를 사용한다. 따라서 옛 소비자의 WKB 한정을 미래 판에 계속 적용하는 수선도 틀릴 수 있다. 최신 1.2.0의 2.0 지원은 릴리스 원문에서 향후 사양으로 설명된다. 이를 이유로 예전 또는 현재 기본값 안내가 자동으로 틀렸다고 판단하지 않았다. 근거: G083-S15, S18–S25.

B의 범위 명시는 역사적 인용을 오늘 재사용할 때 유용한 예방적 제안이다. 원 안내가 당시 틀렸다는 판정은 미확정이다. 발행자가 판 문구를 줄여 유지 비용을 낮추는 목적과 연구 레코드가 판별 가능한 과거 범위를 보존하는 목적은 함께 충족할 수 있다. 현재 안내문과 역사적 provenance를 별도 필드에 두면 된다.

## 실제로 반대한 근거와 일반화 경계

1. **같은 생태계라도 호출자가 다르다.** QGIS의 옛 공식 태그에는 대상 안내가 없었고, Arrow는 GeoArrow를 설명하는 대목과 비공간 Parquet 예제만 제공했다. Arrow 자체는 공급자 연관성도 있다. 빈자리를 일반 표 예제로 채우면 “파일을 연다”와 “geometry/CRS를 복원한다”가 합쳐진다. 근거: G083-S07–S10, 고정 검색 원장.
2. **공간 보존이 CRS 표기 동일성을 뜻하지 않는다.** [1.0.0 소비자 시험 L930–958](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/tests/test_arrow.py#L930-L958)은 GDAL 3.9의 기본 Parquet 변환 명령을 남기고, EPSG:4326 입력의 읽기 기대값을 OGC:CRS84로 바꿔 대조한다. 이 시험은 고유 입력과 default encoding의 정적 선언이며, 079의 native 경계 입력을 대신하지 않는다. 근거: G083-S28.
3. **이미 바뀐 문구를 다시 수선한 것으로 세지 않는다.** G04-2의 첫후속판과 최신판 문구는 같다. 최신판에서 새로 발견했어도 독립 정정이 아니다. 반대로 G04-1의 qualification 변경은 작더라도 실제 원문 편집으로 기록한다. 단어 변경의 존재와 필수 동작 정정 여부는 다른 열이다.

원래 외부 링크의 현재 목적지는 직접 열었으며, 주소가 사양 저장소나 프로젝트 홈에 연결된다는 현재 관측만 남겼다. 당시 HTTP 리디렉션 흐름을 복원하지 못했으므로 **역사적 도착 미확인**은 그대로다. 이는 URL 생존율 재조사가 아니다. 근거: `postseal/current-link-targets.json`.

## Q6에 넘길 연구용 수선

`postseal/research-repair-plan.json`의 지시대로 봉인 원 레코드를 복사하고 판·호출자·인코딩에 대한 주석만 추가한다. 원 URL, 원문 위치, 짧은 원 인용과 원 레코드 해시는 보존한다. G04-1은 유지 조건, G04-2는 예방적 판 범위를 부가한다. G04-3에는 존재하지 않는 원 안내의 diff를 만들지 않는다. 연구용 정·역방향 diff에는 `RESEARCH-` ID를 사용하고, 위의 `PUBLISHER-GEO-3348`/`3391`과 섞지 않는다. 역적용으로 원 레코드가 바이트 단위 복원되는지는 확인할 수 있지만 소비자 기능이 작동한다는 증명이 되지는 않는다.

## 미실시 실행과 최소 재개 입력

기능 실행은 이번 하류 원문 조사에서 하지 않았다. 079 역사 실행을 반복하지 않았고 GeoPandas의 자체 시험을 통과했다고 주장하지 않는다. 필요한 최소 후속 검사는 아래와 같다.

| 목적 | 고정 대상·입력 | 기대해서 구분할 관측 |
|---|---|---|
| 옛 왕복·사양 선택 검증 | GeoPandas `60c9773e44fff8a35344c2a74431e00c5546a4ee`; 자체 `test_roundtrip`, `test_write_spec_version` | 입력 변화 없음, GeoDataFrame/geometry/CRS 대조, 요청 metadata 판. 후자는 box(0,0,10,10), EPSG:4326 |
| native 지원 전후의 조건 분리 | 첫판 `d8e14e1be3ecbef6f75a1142f85561ff652ed3d1`의 `geopandas/io/tests/data/arrow/geoparquet/1.1.0/data-point-encoding_native.parquet`와 같은 경로의 WKB 짝을 두 소비자에 동일하게 입력 | 옛판 non-WKB 거부와 첫판 geometry/CRS 복원. 종료값만으로 성공 판정하지 않음 |
| 첫판 native 자체 계약 | 첫판 `test_read_parquet_geoarrow`, `test_geoarrow_roundtrip`의 여섯 geometry 계열 fixture | native/WKB 결과와 CRS 대조, 명시적 `geometry_encoding="geoarrow"` 왕복 |

첫 행동은 위 두 SHA의 소비자 체크아웃을 소유 경로의 `.workbench/resume/`에 준비하고, 각 판의 CI 환경 명세와 해결된 설치 환경을 구분해 기록하는 것이다. 옛 `ci/envs/39-minimal.yaml`은 PyArrow 8.0.0을 **요청**하지만 옛날 실제 설치를 증명하지 않는다. 새로 해결한 환경도 역사적 설치 증거라고 이름 붙이면 안 된다. 아래 명령의 두 Python 실행 파일은 그 해결 결과를 가리키는 입력이다.

```bash
AF_G04_OLD=/absolute/owned/.workbench/resume/geopandas-0.14.4
AF_G04_FIRST=/absolute/owned/.workbench/resume/geopandas-1.0.0
AF_G04_OLD_PY=/absolute/resolved-old-env/bin/python
AF_G04_FIRST_PY=/absolute/resolved-first-env/bin/python
git -C "$AF_G04_OLD" rev-parse HEAD
git -C "$AF_G04_FIRST" rev-parse HEAD
"$AF_G04_OLD_PY" -m pip freeze
"$AF_G04_FIRST_PY" -m pip freeze
cd "$AF_G04_OLD"
"$AF_G04_OLD_PY" -m pytest -q geopandas/io/tests/test_arrow.py::test_write_spec_version geopandas/io/tests/test_arrow.py::test_roundtrip
cd "$AF_G04_FIRST"
"$AF_G04_FIRST_PY" -m pytest -q geopandas/io/tests/test_arrow.py::test_read_parquet_geoarrow geopandas/io/tests/test_arrow.py::test_geoarrow_roundtrip
```

각 명령의 종료값, Python/NumPy/PyArrow/GeoPandas 판, fixture SHA256, 실패·skip 이유, geometry·CRS·schema 관측을 함께 저장한다. native/WKB 파일을 옛판에 직접 넣는 추가 실행은 파일 해시와 metadata를 먼저 고정한다. 현재 시험 정의를 읽었다는 사실만으로 이 실행을 완료 처리하지 않는다.

## 통합 담당자에게

`revisions.csv`, `postseal/sources.jsonl`, 실제 발행자 변경 receipt, record fingerprint와 repair plan을 ③ 묶음에 포함할 수 있다. 사전 파일은 바뀌지 않았다. 이 GIS 묶음의 직접 분석 source 행은 31개지만 판·시험·토론 중복을 접으면 14 계보이며, 이를 전체 독립 저작 최소량으로 곧바로 더하지 말아야 한다. 핵심 안내 모집은 2개, 한 독립 가이드뿐이다. 공급자 관련성, 문서와 코드 보조층, 동일 사건 PR·이슈의 중복을 통합 원장에서 다시 보존한다. 전체 20개 독립 사건 및 6개 하류 저작 요건은 통합 원장이 최종 판단한다.
