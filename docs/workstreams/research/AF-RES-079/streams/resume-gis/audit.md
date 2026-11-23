# AF-RES-079#2 · GIS 복구 근거 비가림 감사

검토자: `/root/gis_resume_audit` 별도 도구 에이전트. 최초 판정·수선안을 읽은 뒤의 **비가림 검토**다. 이전 가림 재판독과 별개이며 독립 정확도·일치율을 계산하지 않는다. 검토 시각과 실제 명령·종료값은 [audit.json](audit.json) 및 [7개 재실행 영수증](runs/)에 기록했다.

## 수용 가능한 범위

**GIS 자연 4사건 중 3사건(G02·G03·G04)에 과거 판의 네이티브 관측이 있다.** 이 수는 모든 기능·입력의 호환 성공 수가 아니다. G01에는 실행 가능한 rasdaman 서버·원 adapter build가 없고, 전체 georeferencing 및 쓰기 요구는 원래 adapter의 역할 밖이었다. 자연 모집 4/4와 양판 원문 4/4를 실행 3/4와 분리해야 한다.

복구된 command receipt **65개**에 대해 참조한 출력 파일의 존재와 SHA-256 일치를 검사했고 모두 일치했다. 이는 설치 실패와 예상 거절도 포함한 로그 무결성 검사이지 65개 기능 성공이라는 뜻이 아니다. 이전 작업 공간의 작은 생성 입력·출력 **11개, 13,266B**를 새 `artifacts/`에 복사했으며 원본을 바꾸지 않았다. 여섯 writer의 출력 해시와 실제 bytes도 일치했다. 이들은 연구용 fixture와 출력으로 독립 원저작·자연 사건 수에 **0개**를 더한다.

기존 환경을 설치·복사하지 않고, `-B` 및 `PYTHONDONTWRITEBYTECODE=1`로 실행기를 읽기만 재사용했다. 출력·캐시는 이 검토 경로 안으로 한정했다. 대표 **7개 읽기 호출**을 재실행해 원 입력 해시와 명시한 의미 필드를 대조했다. 7개 모두 이전 관측과 일치했다. 실제 프로세스 종료는 정상 읽기 6개가 0, 예상한 ARG 기본 설정 거절 1개가 3이다. 검토 스크립트는 종료 **0**이다. 원래 모집·시험 입력·이전 로그를 수정하지 않았다.

## 사건별 판독

| 사건·질문 | 확인한 입력과 결과 | 수용 범위·한계 | 근거 |
| --- | --- | --- | --- |
| G01 P1/P2 | 과거 서버 또는 adapter build를 실행하지 않았다. georeferencing·writer는 원래 미지원이다. | full CRS/write 요구 적용 외. pixel-only 읽기는 계속 미확인이다. 이관 후 새 손실로 세지 않는다. | 기존 `streams/gis/GIS_NOTES.md` G01 및 `G-O01/02` |
| G02 P1 | 동일 `sealed.arg` 해시 `d3ae3ecf…`와 JSON sidecar를 3.7 기본값에서 읽고, 3.8 기본값에서는 폐기 gate로 거절하며, 3.9에서는 driver가 없다. 3.8 YES opt-in은 값을 복원한다. | 기본 호출 지속성은 기각된다. 다만 -9999를 NoData로 보고해야 한다는 전체 요구는 3.7부터 이미 불충족이었다. 3.7과 3.8 YES는 -32767을 NoData로 보고하고 -9999를 보통 pixel로 유지한다. | `arg-default-3.7.0.log`, `arg-default-3.8.0.log`, `arg-default-3.9.0.log`, `arg-opt-in-3.8.0.log`; 새 `runs/arg-default.receipt.json`, `runs/arg-optin.receipt.json` |
| G02 P2 | 3.8 opt-in CreateCopy의 2×2 Int16 출력은 구 3.7에서 값·형·EPSG4326·geotransform이 유지되지만 NoData는 -32767이다. 2 band 입력은 명시적 오류로 거절된다. | 전체 nodata 보존 요구는 기각된다. 원래의 고정 sentinel 한계를 새 이관 손실로 세지 않는다. 새 successor driver는 확인하지 못했으므로 임의 별칭을 만들지 않는다. | `arg-write-3.8.0.log`, `arg-old-consumer.log`, `arg-invalid-bands.log`; 보존 `artifacts/new.arg`, `artifacts/new.json` |
| G03 P1 | 3.7 writer가 만든 동일 Parquet 파일 `83163259…`을 3.7/3.8에서 읽었다. id Integer, label String, UTF-8 값, 순서, 두 Point, EPSG4326 및 data-axis mapping `[2,1]`가 같다. | 기록한 정상 입력에서 수용. 대각선 좌표 두 개와 null 없는 입력은 모든 축 변환·null 동작을 입증하지 않는다. | `g03-p1-old/new.log`, `contract-g03-p1-old/new.log`; 새 `runs/g03-read-old/new.receipt.json` |
| G03 P2 | 같은 JSON writer 입력으로 metadata beta.1과 1.0.0 출력이 생긴다. 3.7 consumer는 3.8의 새 WKB 파일을 요구한 값·형·순서·CRS로 읽는다. invalid compression과 PointM 선언은 양판 모두 RuntimeError·종료3이다. | 지정 정상 입력과 두 오류에서 조건부 수용. format판 변경 자체가 모든 구 consumer 실패라는 반례는 성립하지 않는다. beta 문자열 자체를 요구하는 소비자·다른 입력은 별도다. | `g03-old/new-write.log`, `g03-p2-old-consumer.log`, `contract-g03-p2-old-consumer.log`, `g03-invalid-*.log` |
| G04 P1 | 같은 구 WKB 파일 `96279956…`을 3.8/3.9에서 읽었으며 필수 필드·값·순서·Point·CRS·data-axis mapping이 같다. | 기록한 기본 WKB 입력 범위에서 수용. GEOARROW 교체의 결과로 확대하지 않는다. | `g04-p1-wkb-3.8.0/3.9.0.log`, `contract-g04-p1-old/new.log` |
| G04 P2 같은 이름 | 동일 Point/null/EMPTY 입력으로 3.9 `GEOARROW`가 struct를 쓴다. 구 3.8 consumer는 프로세스 종료0이나 geometry field가 0이고 CRS도 없으며 x/y를 일반 속성으로 노출한다. 3.9는 geometry field 1과 null/EMPTY 구분을 유지한다. | 같은 이름만 바꿔 연결하는 교체를 기각한다. 성공한 open과 종료0을 요구 기능의 성공으로 세면 안 된다. | `g04-old-reads-new-name.log`, `contract-g04-new-name-old-consumer.log`; 새 `runs/g04-old-reads-struct.receipt.json`, `runs/g04-new-reads-struct.receipt.json` |
| G04 P2 범위 있는 별칭 | 3.9 `GEOARROW_INTERLEAVED`는 FixedSizeList 표현을 유지하여 구 consumer의 geometry·CRS를 복원한다. 구 consumer에는 bbox 속성 4개가 추가되지만 필수 id/label과 순서는 유지된다. 기존 3.8 interleaved도 이미 null을 EMPTY로 바꾸었다. | 옛 표현의 판 한정 별칭을 지지한다. exact-schema 소비자는 추가 속성 때문에 별도 조건이 필요하며, required-field subset 소비자는 추가 속성만으로 실패라 할 수 없다. strict null 보존은 이미 이전 표현에서 실패한 요구다. | `g04-old-read.log`, `g04-old-reads-alias.log`, `contract-g04-alias-old-consumer.log`; 새 `runs/g04-old-reads-alias.receipt.json` |

위 표의 기존 `.log` 경로는 `streams/gis/historical/` 아래다. 새 재실행 결과는 각 receipt의 `result` 및 stdout 원본을 읽는다. 원 native supplement의 GN01–GN11은 이 관측들을 질문별로 묶은 행이며, 11행을 독립 사건 11개로 세면 안 된다.

## 확인한 반례와 고쳐야 할 서술

1. **미커밋 자료 복구 시점의 RESULT·원장 불일치.** 첫 감사 시 RESULT와 GIS_NOTES는 GIS native 0/4와 G02–G04 미실행을 적고 있었지만 복구 로그에는 3사건 관측이 있었다. 최종 통합판의 RESULT, SELF_CHECK, observations, relations, acceptance 분자와 보류 조건을 함께 갱신해야 한다. 원 GIS_NOTES를 초기 시점 기록으로 유지한다면 머리에 후속 native supplement를 가리켜야 한다.

2. **ignored 출력 때문에 실행 입력 bytes가 Git 산출물에서 빠짐.** `historical/.gitignore`가 `runs/*.parquet`와 `runs/*.arg`를 제외했다. 새로운 `artifacts/`에는 다섯 Parquet, ARG writer 출력·sidecar, 두 ARG 입력·sidecar를 보존했다. [audit.json](audit.json)의 `artifact_manifest`는 원 `streams/gis/historical/runs/...` 상대경로, 새 보존 경로, 길이·해시를 대응한다. 최종 통합 담당자는 이 동일 bytes를 원래 상대경로에 복구하거나 이 매핑으로 참조를 해소할 수 있다. 이관·복구 중 bytes가 달라졌다는 증거는 없었다.

3. **일치한 Python 패키지 버전과 writer에 연결된 라이브러리를 구별해야 함.** G04 양쪽 `pyarrow.__version__`는 14.0.2지만 `parquet_created_by`의 C++ writer 표기는 구 3.8에서 14.0.1, 새 3.9에서 14.0.2다. Python 빌드, PROJ와 다른 의존성도 다르다. 따라서 이 실행은 주어진 배포 환경의 결과이며 GDAL 버전만 바꾼 인과 실험이 아니다. 같은 3.9 환경에서 struct와 interleaved를 비교한 GN07은 그 환경 안에서 표현·null 의미가 다르다는 더 직접적인 구별 근거다. G03 두 writer의 C++ 표기는 둘 다 10.0.1이지만 다른 의존성 한계는 여전히 남는다.

## 원문 재열람

고정 commit의 [GDAL3.9 Parquet 문서](https://raw.githubusercontent.com/OSGeo/gdal/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/doc/source/drivers/vector/parquet.rst) L68–83, L125–133에서 이름·표현 변경과 `WRITE_COVERING_BBOX` 기본 YES를 다시 직접 읽었다. bbox 추가는 이 기본 옵션과 일치한다. 이것만으로 `WRITE_COVERING_BBOX=NO`가 모든 exact-schema 교체를 해결했다고 주장하지 않는다. 그 조합은 이번 감사에서 실행하지 않았다. 3.9 문서 자체도 interleaved를 정식 GeoParquet 규격 밖의 확장으로 구분한다. 관측 metadata의 `1.0.0` 또는 `1.1.0` 문자열을 전체 규격 적합성 인증으로 읽지 않는다.

고정 commit의 [GDAL3.8 gate 구현](https://raw.githubusercontent.com/OSGeo/gdal/c46fe7e20e33925735ae4b785752795af72823bc/gcore/gdaldrivermanager.cpp) L1187–1207도 직접 읽어 기본 NO 및 YES opt-in을 확인했다. 두 재열람의 HTTP200, 실제 도착 URL, UTC, 원문 해시는 [source-reread.jsonl](source-reread.jsonl)에 있고 이전 source 행의 해시와 같다. 이미 센 저작의 재열람이므로 추가 저작은 0이다. 앞선 web-open 도구는 DisabledError로 원문을 반환하지 않았고 HTTP 상태도 관측하지 못했다. 이후 직접 HTTPS 취득으로 원문을 읽었다.

## 최소 재개와 종료 기준

- G01을 바꿀 최소 확인은 정확한 옛·수신 adapter build와 rasdaman 서버의 `rgb` 및 invalid query 입력이다. source 이동만으로 runtime 승인을 만들지 않는다.
- G04 exact-schema 별칭을 바꿀 최소 확인은 같은 경계 fixture에 3.9 `GEOARROW_INTERLEAVED`와 `WRITE_COVERING_BBOX=NO`를 함께 적용하여 구 3.8 consumer의 필드·geometry·CRS·null/EMPTY를 대조하는 것이다. 이 가설은 미실행으로 남긴다.
- 모든 환경의 완전한 동작을 더 시험하는 대신, 이번 감사의 구체적 위험인 복구 로그 무결성·입력 bytes 소실·핵심 소비자 실패를 해소한 후 종료한다. 최초 조사자의 판정과 이번 별도 검토가 같은 출처 선택을 공유하므로 독립 일치율을 만들지 않는다.

실행 명령은 `python -B docs/workstreams/research/AF-RES-079/streams/resume-gis/audit_recovery.py`다. 이전 환경 경로가 사라진 새 실행기에서는 `audit.json`의 기록을 우선 읽고, exact historical package manifest로 환경을 복원한 뒤 지정 입력을 사용해야 한다. 이 감사의 종료0을 모든 새 실행기의 재현 보장으로 확대하지 않는다.
