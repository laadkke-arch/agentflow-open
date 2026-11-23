# AF-RES-079 GIS 원문 판독

## 범위와 분모

봉인된 GDAL 정식 minor 공지 5개를 읽었다. 모집은 3.7.0 → 3.8.0 → 3.9.0 → 3.10.0 → 3.11.0 발행 순서이고, 각 NEWS에서 해당 릴리스의 첫 절만 검사했다. 자연 자리는 **4/4**, 양판의 문서·등록부·구현 자료는 **4/4**, 선택한 양판을 같은 입력으로 직접 실행한 자리는 **0/4**다. 현재 환경의 GDAL 3.10.3 ARG 접근 실패를 별도 1회 실행했으며 자연 양판 실행의 분자에 넣지 않았다.

`recruitment.csv`는 어휘/포맷판으로 검사한 115행의 원순위와 제외·중복·quota 이후 사유다. 구현/매개변수 변경, GRIB 해석표 판, tile-matrix resource URI를 driver 또는 file-format identity 변경으로 세지 않았다. `sources.jsonl`은 성공·실패·metadata 조회를 모두 보존한다. **GDAL driver manual의 여러 페이지/판은 1계보**, NEWS 1, 공급자 시험 1, 구현 1로 합쳤다. 전체 독립 원저작은 **9계보**이며 개별 파일 수를 저작 수로 쓰지 않는다. `recruitment-summary.json`에 목록과 실제 수가 있다.

| 사건 | 모집 원순위 | 선정된 변경 | 양판 및 추가 확인 |
| --- | --- | --- | --- |
| G01 | 1 | RASDAMAN core source → extra-drivers의 미빌드 source | GDAL3.6 원본과 등록 호출 존재, 3.7 부재; 2023-03-12 수신 commit ffe0c447 |
| G02 | 23 | ARG 3.8 폐기 예고·기본 비활성, 3.9 제거 | 3.7 Open, 3.8 deprecation gate, 3.9 등록부 부재 |
| G03 | 39 | Parquet writer의 GeoParquet beta1 → 1.0 출력판 | 3.7/3.8 문서·writer·공급자 시험; 같은판 문서 불일치 |
| G04 | 60 | GeoParquet1.1 도입과 GEOARROW 의미 변경 | 3.8/3.9 문서; 3.9 두 encoding 시험; 표준1.0/1.1 |

JP2Lura 제거는 quota 이후 보충 사례다. 이 자료가 더 편리하다고 선정된 사건을 교체하지 않았다. 릴리스 날짜는 GitHub 공식 releases API에서 확인했다: 3.7.0 2023-05-10, 3.8.0 2023-11-13, 3.9.0 2024-05-10, 3.10.0 2024-11-06, 3.11.0 2025-05-09 UTC.

## 모집 확정 중의 반대 근거

Rasdaman은 3.7 NEWS에서 처음 적격으로 나타났다. 수신 README의 Other drivers 절에 ‘3.5에서 제거’라는 일괄 문구가 있어 한때 과거 사건의 재공지일 가능성을 검토했다. 하지만 원본 3.6의 `rasdamandataset.cpp`와 `GDALRegister_RASDAMAN()` 호출이 실제 존재하고, 3.7에서는 둘 다 사라졌다. 유지관리자의 2023-03-12 댓글과 같은 날 수신 commit은 이관을 쌍방 연결한다. 따라서 Rasdaman을 제외하는 해석은 기각하고 첫 적격으로 확정했다. 최종 선정 시각은 **2026-11-23 11:35:48 UTC**다. 사전 모집 규칙은 바꾸지 않았다.

이것은 단순한 사후 취향 변경이 아니다. 포괄적인 README 표제보다 사건별 전후 원판·commit을 우선해야 한다는 실재 반례다. 자료: `G-extra-readme`, `G-ras-dest-readme`, `G-issue4808-comments`, `G-ras-reg3.6`, `G-ras-reg3.7`, `G-ras-move-commit`.

## 사건별 기능·판정 범위

### G01 · 소스가 옮겨간 것과 작동하는 교체 부품

RASDAMAN 등록 이름과 query-template 역할은 이어지고, 전후 설명 문서의 SHA-256도 같다. 그러나 이전 소스와 수신 소스의 바이트는 다르며, 수신 경로는 `not_integrated_in_build`다. README는 미유지와 제한된 판 호환을 밝힌다. 원 이슈는 기존 driver의 빌드 문제를 보고한다. 따라서 소스 존재를 작동하는 plugin 배포물로 바꾸어 말할 수 없다.

논리적인 adapter ID는 **① 보존**하고, core source와 archived source 배포물 사이에는 **④ 이동 관계**를 둔다. rasdaman 서버 제품과 GDAL adapter도 구분한다. P1의 필수 CRS/geotransform은 이전·이후 모두 원래부터 지원하지 않으므로 전체 요구는 적용 외다. 픽셀만 읽는 부분 P1의 실제 양판 동작은 보류한다. P2의 쓰기 기능도 양쪽 등록 callback에 원래부터 없으므로 적용 외이며, 이관 때문에 기능을 잃은 실패 분자에 넣지 않는다. 픽셀 읽기의 최소 재개에는 공급자 시험의 `rgb` 조회·checksum 61774와 missing-collection/syntax 오류를 입력으로 쓴다. 시험 정의를 읽었고 실행하지 않았다.

### G02 · 삭제판 전에도 기존 기본값은 달라졌다

ARG는 3.9에 제거됐지만, 3.8의 Open/CreateCopy는 `GDALIsDriverDeprecatedForGDAL39StillEnabled`를 통과해야 한다. 해당 helper는 `GDAL_ENABLE_DEPRECATED_DRIVER_ARG`를 기본 **NO**로 읽고 실패를 반환한다. 공급자 시험은 명시적으로 YES를 설정한다. 따라서 3.8에서 시험이 정의되어 있다는 이유로 옛 기본 호출이 계속 된다고 판단하면 안 된다.

기존 ARG ID를 **① 퇴역 상태로 보존**한다. 안내의 ‘다른 일반 형식으로 변환’은 특정 driver의 별칭 선언이 아니다. P1은 기본값 유지 조건에서 정적 근거상 실패하고, P2는 3.8의 opt-in writer와 3.9의 부재를 구별해야 한다. 2×2 ARG fixture의 nodata는 format/driver가 고정하는 값을 확인해야 하며 봉인한 -9999를 몰래 다른 값으로 바꾸어 성공으로 처리하지 않았다. 공급자 int16 fixture는 -32768 sentinel을 생성하는데 driver는 -32767을 NoData로 놓는 정적 불일치도 있어 별도 실행 확인이 필요하다.

### G03 · 같은 발행판의 문서가 구현보다 뒤처진다

3.8 NEWS와 writer/test는 `1.0.0`을 나타내지만, 3.8 driver 문서는 여전히 beta1과 experimental을 적는다. 이때 페이지가 200을 반환하는지는 어떤 판의 출력인지 결정하지 못한다. Parquet driver ID는 **① 유지**하고 beta와 정식 format edition은 구분하여 **④ 판 관계**를 연결한다.

공급자 시험의 writer 입력 경로 `test.parquet`도 판마다 실제 바이트가 달랐다. 3.7은 57,756B, 3.8은 72,316B, 3.9는 72,995B이며 지문도 다르다. 같은 시험 이름·경로를 동일 입력이라고 세지 않았다. P1의 완전 호환은 보류다. P2에서는 같은 WKB 기본과 PointM/invalid compression 예외 기대가 정의되지만, 옛 consumer가 새 format을 받아들이는지는 미실행이다.

### G04 · 이름 하나가 다른 표현을 가리킨다

3.9 이전 `GEOARROW`는 interleaved fixed-size-list 표현이었다. 3.9 이후 그 표현은 `GEOARROW_INTERLEAVED`로 이름이 바뀌고, `GEOARROW`는 struct 표현을 뜻한다. 기존 unversioned GEOARROW record가 두 의미를 섞으면 **③ 분리**한다. 옛 표현에는 판을 한정한 **② 별칭**을 붙이고, 구·신 encoding 사이에는 **④ 관계**를 둔다.

공급자 3.9 시험의 입력은 `POINT (1 2)`, null, EMPTY, 정상 Point 순서다. struct 시험은 null을 `None`으로 기대하지만, interleaved Point 시험은 null 위치를 EMPTY로 기대한다. 따라서 이름을 같다고 병합하면 Arrow type이나 null/empty 계약을 잃는다. 반대로 이름이 새롭다는 이유로 옛 interleaved 기능을 새 기능으로 세면 중복 작업을 할 수 있다. 후자는 별도의 이름 분리 정책 반례이며 URL-only 규칙의 false-split으로 계산하지 않는다.

P1의 기본 WKB reader는 계속 쓸 수 있을 가능성이 있지만 정확한 고정 입력 실행은 보류다. P2에서 옛 FixedSizeList 소비자에 이름만 같은 새 `GEOARROW` writer를 연결하는 것은 거절한다. GeoParquet1.1의 forward-compatibility 규정도 옛 reader가 새 encoding을 ‘해석할 수 없다고 인식’하는 것을 허용한다. 이를 모든 파일의 구 consumer 처리 성공으로 해석할 수 없다.

## URL-only 비교에서 셀 수 있는 것

RASDAMAN·ARG 옛 문서 주소는 현재 301 이후 404다. URL-only U는 보류한다. Parquet 옛 주소는 301 이후 stable 문서 200으로 도착하므로 U는 주소를 고치고 같은 record를 유지한다. 현재 관측을 과거 redirect 이력으로 확대하지 않는다.

G03은 driver ID 단위라면 U가 유지한 것이 맞고, format edition 정보 부족을 곧바로 false product merge로 세지 않는다. G04의 **encoding feature** 단위에서는 같은 이름에 서로 다른 표현이 있어 U의 무조건 record 유지가 의미를 섞는다. G01·G02의 U 보류는 오답으로 세지 않는다. U 자체에 분리 행동이 없으므로 U false-split을 만들어내지 않는다. 발행자 선언·정적 구현과 별도 판독으로 단위를 고정한 뒤 통합표의 분모를 계산해야 한다.

## 실제 실행 및 미실시

- `runtime-probe.json`: 클라우드 `/usr/bin/python3`, GDAL3.10.3, ARG·Parquet·JP2Lura driver 부재를 관측했다. 2×2 ARG bytes를 `/vsimem`에 넣고 `allowed_drivers=['ARG']`로 열자 `RuntimeError`가 발생했다. 관측 runner 종료값0. 양판 재현 성공으로 세지 않는다.
- 양판 native 실행은0/4다. raslib/server, Parquet가 포함된 정확한 GDAL3.7/3.8/3.9 환경이 없다. JP2Lura는 보충 사례이며 SDK·라이선스가 필요하다. 계정/권한/유료 자원을 만들지 않았다.
- `reproduce.md`에 필요한 판·입력과 후속 명령을 기록한다. 공급자 test 정의와 실제 실행 결과를 분리한다.
- 소스 원문은 직접 열어 해당 절을 판독했다. HTTP 응답·chain·원문 지문·원 주소·고정 가능한 commit 주소는 원장에 보존했다. 작업용 전체 응답 캐시는 Git 산출물에서 제외한다. 캐시는 증거 수에 추가하지 않는다.

## 통합 담당에게 넘길 가장 중요한 세 약점

1. **동일 입력 양판 실행 부재.** 같은 파일명도 bytes가 달랐다. 최소 재개는 이 연구의 고정 fixture 하나를 정확한 구·신 GDAL에 전달해 type/순서/CRS/예외까지 대조하는 것이다.
2. **발행자의 선언 안에서도 범위가 충돌한다.** Rasdaman README의 포괄적3.5, Parquet3.8 beta1 문구는 세부 원판·구현과 맞지 않는다. 사건별 commit과 해당 기능 절을 함께 남겨야 한다.
3. **driver·배포물·encoding·format edition을 섞으면 오류 수가 바뀐다.** G03의 driver 유지와 G04의 encoding 분리는 서로 다른 단위다. URL-only 비교에서는 평가 단위를 먼저 정하고 source-level lineage를 runtime acceptance로 승격하지 않는다.
