# AF-RES-079 · 주소가 바뀐 뒤에도 같은 기능을 가리키는가

**인계 상태: PARTIAL — 식별·수선 원장은 수용 가능하며, 행동 적합성은 실제 확인한 입력·환경에 한정한다.** 자연 8자리와 대조 3자리를 다른 층으로 유지했다. 이전·이후 원판 근거는 자연 8/8, 대조 3/3이다. 독립 원저작은 보수적으로 합친 32계보다. 과거 native 실행 근거는 OSS 4/4, GIS 3/4로 자연 7/8이다. G01 서버·adapter 실행과 대조의 역사 양판 실행 0/3은 미확인으로 남긴다. 모집·원문 최소량·두 질문·근거 연결은 충족했으며 PARTIAL은 이 행동 검증 범위를 뜻한다.

실제 시작 통합판은 `d73c8ec85d375f37451795b575dd7d0e6b2f3594`, 계획 기준은 `0d2b08431067e8d87212a66ecb27657c65722a59`다. 이 결과의 최종 고정 SHA와 원격 재독 영수증은 마지막 단독 커밋의 `HANDOFF.md`에 있다. 조사·응답 시각은 UTC이며 모든 HTTP 표는 **2026-11-23의 실제 GET 관측**이다. 과거 리다이렉트 이력은 11/11 미확인이다.

아래의 source ID는 [sources.jsonl](sources.jsonl), 관측 ID는 [observations.csv](observations.csv), 관계 ID는 [relations.csv](relations.csv)의 행 식별자다. `H-` 관측은 과거 SciPy 양판 실행을 결합한 행, `GN01–GN11`은 후속 GDAL 실행 묶음, `PA-`는 원 PIL 보관본의 추가 판독이다. GN07·GN11은 같은 판의 보조 대조여서 전후 사건 수를 늘리지 않는다. 원절 URL·판·확인 UTC·한계는 해당 source 행에 있고, [EVIDENCE_MAP.md](EVIDENCE_MAP.md)에 산입한 32계보를 모았다.

## 필수 표1 — 사건ID·모집 원순위·대상의 전후와 실제 도착

| 사건ID | 모집 원순위 | 자연/대조 | 옛/새 ID와 판 | 이름/주소 | 실제 도착 | 발행자 선언 |
|---|---|---|---|---|---|---|
| G01 | GDAL 후보1; 3.7 NEWS L37 | 자연 GIS 1/4 | 논리 ID `gdal-driver:RASDAMAN`; core3.6의 source component → `gdal-extra-drivers`의 `ffe0c447…` 보관 component. driver와 rasdaman 서버 제품은 별개 | [옛 driver URL](https://gdal.org/drivers/raster/rasdaman.html) → [수신 원본](https://github.com/OSGeo/gdal-extra-drivers/tree/ffe0c44714a491eb90ba82d8df74f621ac6003e7/not_integrated_in_build/rasdaman) | 옛 URL 301→stable404; 고정 수신 원문200 | GDAL 유지관리자 2023-03-12 댓글과 수신 commit, 3.7 NEWS가 이동을 선언. 수신 README는 `not_integrated_in_build`, 비유지·호환 무보증. `G-issue4808-comments`, `G-ras-move-commit`, `G-NEWS-3.7.0`, `R037` |
| G02 | 후보23; 3.8 NEWS L25 | 자연 GIS 2/4 | `gdal-driver:ARG` 3.7→3.8 기본 비활성/폐기 예고→3.9 등록 제거. **새 ID 미지정** | [옛 ARG URL](https://gdal.org/drivers/raster/arg.html); [3.8 원절](https://github.com/OSGeo/gdal/blob/c46fe7e20e33925735ae4b785752795af72823bc/doc/source/drivers/raster/arg.rst) | 301→stable404; 3.8 원문200; 3.9 해당 source path404와 등록부 부재를 함께 확인 | issue7920, 3.8/3.9 NEWS. 일반 포맷으로 변환 권고는 특정 driver와의 동일성 선언이 아니다. `G-issue7920`, `G-arg-reg3.9` |
| G03 | 후보39; 3.8 NEWS L510 | 자연 GIS 3/4 | `gdal-driver:Parquet` 유지; `geoparquet-format:1.0.0-beta.1`→`1.0.0`; GDAL3.7→3.8 | [옛 Parquet URL](https://gdal.org/drivers/vector/parquet.html) → [현재 정식 위치](https://gdal.org/en/stable/drivers/vector/parquet.html) | 301→200. 현재 한 페이지에 도착해도 과거 두 출력판은 별도 | 3.8 NEWS와 writer/test는 1.0.0 출력. **같은 3.8 manual은 beta1**을 계속 설명. `G-parquet-writer3.7/3.8`, `G-parquet-doc-3.8` |
| G04 | 후보60; 3.9 NEWS L489–494 | 자연 GIS 4/4 | GDAL3.8 `GEOARROW`=interleaved. 3.9 `GEOARROW_INTERLEAVED`=옛 표현; 3.9 `GEOARROW`=struct. format1.1의 native geometry도 구별 | G03과 같은 URL이지만 **선택한 사건·기능·판이 다르다** | 301→200; 같은 이름의 옵션 의미 변경은 HTTP에서 보이지 않음 | [3.9 Parquet 문서](https://github.com/OSGeo/gdal/blob/bb5ea618e23e498e79e8b8e6bd7215ad94bb2103/doc/source/drivers/vector/parquet.rst)의 생성 옵션 절이 명시. `G-parquet-doc-3.9`, `G-parquet-test-3.9` |
| O01 | R02; 1.5.0 release L250 | 자연 OSS 1/4 | `scipy.stats.median_absolute_deviation` 1.4.1 → `median_abs_deviation` 1.5.0. 구 wrapper는 1.5.0에 공존 | [구판](https://docs.scipy.org/doc/scipy-1.4.1/reference/generated/scipy.stats.median_absolute_deviation.html) / [신판](https://docs.scipy.org/doc/scipy-1.5.0/reference/generated/scipy.stats.median_abs_deviation.html) | 양판200; unversioned 구 함수 문서는404 | SciPy PR11431·issue11090. 구 scale 곱셈과 새 scale 나눗셈, 기본값 변경을 문서·wrapper가 구별한다. `OS-PR-11431` |
| O02 | R10; 1.6.0 L52–57, stats L245–246를 같은 결정으로 묶음 | 자연 OSS 2/4 | 1.5.4→1.6.0: integrate의 `simps/trapz/cumtrapz`→`simpson/trapezoid/cumulative_trapezoid`; stats의 `trapz`→`trapezoid`. **4개 기능 ID, 모집 1사건** | [구 trapz](https://docs.scipy.org/doc/scipy-1.5.4/reference/generated/scipy.integrate.trapz.html) / [신 trapezoid](https://docs.scipy.org/doc/scipy-1.6.0/reference/generated/scipy.integrate.trapezoid.html) | 양판200; unversioned 구 integrate.trapz404 | 하나의 명명 결정 issue12924와 PR12927/12934. integrate 옛 3이름은 1.14.0에 제거; stats 별칭 종료판은 여기서 확정하지 않음. `OS-ISSUE-12924`, `OS-PR-12934` |
| O03 | R12; 1.6.0 L270–271 | 자연 OSS 3/4 | `KDTree.query#k=None` 1.5.4 → `KDTree.query_ball_point` 1.6.0. 메서드 전체와 특정 mode를 구별 | [옛 query](https://docs.scipy.org/doc/scipy-1.5.4/reference/generated/scipy.spatial.KDTree.query.html) / [새 메서드](https://docs.scipy.org/doc/scipy-1.6.0/reference/generated/scipy.spatial.KDTree.query_ball_point.html) | 양판200; live query도200. 현재1.17 실행에서는 k=None ValueError | PR12382·1.6 공지는 대체를 제안. 예정 제거1.8과 실제 문서의 제거1.9를 구별. `OS-PR-12382`, `OS-DOC-O03-live_old` |
| O04 | R17; 1.6.0 issue목록 L490/PR목록 L637 | 자연 OSS 4/4 | `scipy.ndimage.sum` 1.5.4 → `sum_labels` 1.6.0; 구 이름은 별칭으로 유지 | [구판](https://docs.scipy.org/doc/scipy-1.5.4/reference/generated/scipy.ndimage.sum.html) / [신판](https://docs.scipy.org/doc/scipy-1.6.0/reference/generated/scipy.ndimage.sum_labels.html) | 양판200; live 구 문서는404지만 설치1.17에서 구/신 함수 모두 실행됨 | PR12242의 alias와 공급자 test_sum_labels. 404를 기능 삭제나 거짓 분리로 간주하지 않음. `OS-PR-12242`, `O04-HTTP-COUNTER` |
| C01 | 사전 지정 A | 대조 1/3 | 프로젝트 `scikit-learn` 유지; import namespace `scikits.learn`0.8→`sklearn`0.9 | [현재 원경로](https://scikit-learn.org/0.9/whats_new.html) / [남아 있는 0.9 발행판](https://scikit-learn.sourceforge.net/0.9/whats_new.html) | 전자404, 후자200. 역사 redirect라고 주장하지 않음 | 같은 유지관리자의 0.9 공지·alias source. 0.11 제거 예고와 뒤의 실행 공지를 구별. `R002`, `R003`, `R005`, `R026` |
| C02 | 사전 지정 B | 대조 2/3 | 원 배포물 `PythonWare/Imaging` PIL1.1.7 → 별도 fork `pypi:pillow`; 양쪽 import `PIL.Image`는 배포 ID가 아님 | [옛 사이트](https://pythonware.com/products/pil/) / [fork 설명](https://pillow.readthedocs.io/en/stable/about.html); 원판은 [Debian orig archive](https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7.orig.tar.gz) | 옛 사이트301→www200이며 현재 페이지는2026 설명이다. 원 PIL 발행자와 저자 연속성은 미확인. 원 tarball·descriptor200, 해시 일치 | 2010-07-31 fork 작성자 공지와 08-01 원 저자 답변을 모두 읽음. 원 저자의 패치 선호는 배포물 병합 승인으로 과장하지 않음. 2020 PyPI 이름 소유권 이동은 별개. `R035/36`, `R014`, `PA001/2` |
| C03 | 사전 지정 C | 대조 3/3 | `cpython-api:imp.find_module`3.11 → 개별 대체 `importlib.util.find_spec`; imp는3.12 제거 | [옛 live fragment](https://docs.python.org/3/library/imp.html#imp.find_module) / [보존할3.11 원절](https://docs.python.org/3.11/library/imp.html#imp.find_module) | live200이지만 `imp.find_module` anchor/기능 절 없음. 3.11 원절200 | [3.12 이관표](https://docs.python.org/3.12/whatsnew/3.12.html#imp)와 issue98040. 모듈 전체 별칭이 아니라 API별 대체/미대체. `R016–R022`, `R032/33` |

## 필수 표2 — 같은 쌍에 두 요구를 적용한 입력·출력·경계

P1은 기존 호출·기본값·필수 형/순서/메타데이터 유지다. P2는 명시적 이름 변경을 허용하지만 출력 소비자와 오류 계약을 유지한다. 정적 공급자 시험은 **기대/예측**이며 실제 실행 행과 분리했다. `PASS`를 쓰는 경우도 적힌 입력의 수용이지 전 입력 동등성 증명이 아니다.

| 사건 | 질문 | 입력/환경 | 기대 | 실제 또는 미관측 | 증거절 | 규범/동작 불일치 | 판정 |
|---|---|---|---|---|---|---|---|
| G01 | P1 | core3.6/수신 source; rgb collection reader, checksum61774; 원래 reader의 역할 | pixel 값, 전체 요구라면 CRS/변환도 보존 | 양판 미실행. 문서는 원래부터 georeferencing 미지원 | `G-O01`; `G-ras-doc3.6`, `G-ras-dest-doc/test` | 같은 문서 바이트는 build·CRS 능력 증거가 아님 | 전체 CRS 요구 적용 외. pixel-only 부분 보류; 이관으로 잃은 기능 분자에서 제외 |
| G01 | P2 | 같은 adapter로 Create/CreateCopy 출력, invalid query | 기존 출력 기능 지속 | 양쪽 모두 Open 등록만 있음. 공급자 bad query→None 기대는 미실행 | `G-O02`; `G-ras-code3.6/dest-code` | source 보관을 writer 제공으로 오해할 수 있음 | **적용 외**: 원래 read-only. 새 이름 때문에 실패했다고 세지 않음 |
| G02 | P1 | 같은 ARG Int16 `[1,2;3,-9999]`·sidecar;3.7→3.8 default/YES,3.9 | 옛 호출·기본값·값/형/순서/nodata/CRS 유지 | **실제3.7 열림,3.8 default 종료3,YES 열림,3.9 부재**.3.7부터 nodata는-32767 | `GN08/09/11`; 원 예측 `G-O03/05` 유지 | 기본 호출 변화와 원래 nodata 불충족을 구별 | P1 전체 기각; opt-in은 필수 값/형/CRS에 한정한 복구이며 기본값 보존 아님 |
| G02 | P2 | 같은2×2 MEM Int16·nodata-9999를3.8 CreateCopy,3.7 read;2band 경계 | 구 소비자의 nodata 포함 계약,unsupported 거절 | **write/read 종료0**이나 nodata-32767.2band는 예상 RuntimeError/종료3.3.9 writer 없음 | `GN10`; `G-arg-code-3.8`, 시험 | 옛3.7도 같은 sentinel 한계; 신규 손실로 세지 않음 | 전체 nodata-preserving P2 기각;2band 오류는 일치 |
| G03 | P1 |3.7 생성 Parquet SHA `83163259…`를3.7/3.8에서 동일 reader로 읽음 | 필드·형·순서·Point·CRS/축 보존 | **동일 값·형·순서·EPSG4326·축[2,1]**, 같은 nullable 선언, 실제 null0 | `GN01`; 원 fixture 판별 불일치 `G-O06` 보존 | 다른 supplier fixture bytes 문제를 고정 새 입력으로 해소 | 지정 정상 입력 P1 수용; 비대각 좌표 변환·null 범위 일반화 금지 |
| G03 | P2 | 같은 vector 입력의3.8 WKB output SHA `96279956…`→3.7 consumer;invalid compression/PointM | 필수 data·CRS·지정 오류 보존 | **구 소비자 정상 계약 보존**, output beta.1→1.0.0. 양판 invalid4호출 모두 예상 RuntimeError/종료3 | `GN02/03`; writer/test/doc3.8 |3.8 manual beta1 대 **실제 출력1.0.0** | 지정 정상·오류 범위 수용; 정확 beta만 허용하는 소비자와 전규격 적합성 별도 |
| G04 | P1 | 같은3.8 WKB 파일 SHA `96279956…`를3.8/3.9 read | 필수 필드·형·순서·geometry·CRS/축 유지 | **양판 실제 일치**, nullable 선언/metadata도 관측 | `GN04`; `contract-g04-p1-old/new` | Python pyarrow와 C++ writer/build를 구별 | 지정 WKB 정상 입력 P1 수용; 전체 입력 인증 아님 |
| G04 | P2 | 같은 `GEOARROW` 옵션,Point/null/EMPTY;3.9 struct output SHA `f71606cd…`→3.8/3.9 | 구 consumer의 geometry·CRS·오류 계약 | **양쪽 종료0**; 구3.8 geometry field0·CRS없음, 신3.9 field1·EPSG4326 | `GN05`; 같은 file hash·contract logs | 같은 이름·URL·정상 종료에도 필수 geometry/CRS 손실 | 구3.8 consumer에 무수정 같은 이름 P2 기각 |
| G04 | P2 별칭·경계 | 동일 Point(1 2),null,EMPTY,Point(1 2);구/신 interleaved 및 같은3.9 struct 대조 | 필수 필드와 strict schema/null 요구 구별 | alias가 구consumer geometry/CRS 복구, **bbox4필드 추가**. old와alias 모두 null→EMPTY; 같은3.9 struct만 null보존 | `GN06/07`;3.9 옵션 절·공급자시험 | null→EMPTY는 구판부터 존재; GN07은 같은판 대조 | 판 한정 alias 수용. exact-schema는 보류, 필수 필드 subset은 유지. bboxNO 조합 미실행 |
| O01 | P1 정상 | Python3.8.20/NumPy1.19.5, SciPy1.4.1→1.5.0; `[1,3,2]`, 옛 이름 | float64 1.4826 | **양판 실제1.4826**, 신판 DeprecationWarning | `H-O01-P1-normal`; PR11431 wrapper | 값/형은 보존, 경고 정책은 변화 | 정상 값·형 부분 수용; strict warnings 별도 |
| O01 | P2 정상 | 같은 데이터, 새 이름 기본값 및 scale adapter | 옛 결과1.4826 | **기본1.0**; `scale=1/1.4826`은 실제1.4826 | `H-O01-P2-normal`, `…normal-adapter` | 공식 후속이라는 선언은 동일 기본값 선언이 아님 | 무수정 교체 기각; 해당 정상 입력의 adapter 수용 |
| O01 | P1/P2 경계 | shape(3,0), axis=1 | 옛 반환 형상 | **구 scalar NaN→신 shape[3] NaN 배열**, 구 wrapper도 변화 | `H-O01-P1-empty_2d`, `H-O01-P2-empty_2d` | scale adapter만으로 빈 배열 계약 복구 안 됨 | 전체 경계 동등성 기각 |
| O02 | P1 | trapz 옛 이름, 고정 NumPy; 정상/역순/빈/단일/2D/float32/complex·잘못된 축/길이 | 값·형/오류·순서 | 1.5.4/1.6.0 실제 일치. stats 분포 alias의 PDF도 일치 | `H-O02-P1-*` | 같은 NumPy를 고정한 조건; 새 배포물 전체의 동등성 아님 | 실행한 범위 별칭 수용 |
| O02 | P2 | integrate.trapezoid 및 stats.trapezoid의 각각 올바른 역할 | 지정 수치 결과 또는 해당 분포 PDF | P1/P2 총20대응: 반환 표현 일치16, 오류 일치4. **simps/cumtrapz 개별 native는 미실행** | `H-O02-P2-*`; `O02-NAMESPACE-COUNTER` | 잘못된 namespace의 stats 호출은 숫자 대신 frozen distribution; 현재 음성 시험 별도 | qualified 별칭만 수용. 짧은 이름 병합 기각 |
| O03 | P1 정상 | 점[[0],[1],[2]], query[0], k=None, bound1.1 | 거리/인덱스와 원소 형 | 실제 거리·인덱스 값은 [0,1]/[0,1]; **np.int64→Python int** | `H-O03-P1-normal` | JSON 숫자만 평탄화하면 형 변화를 놓침 | 값 부분 유지; 봉인한 엄밀 형 계약 전체는 기각 |
| O03 | P1 경계 | 같은 트리, bound1.0 | 구 strict 경계 | 실제 **구 [0]/[0]→신 [0,1]/[0,1]** | `H-O03-P1-exact_boundary` | 미확인으로 남겼던 경계가 실제 불일치로 바뀜 | 경계 동등성 기각 |
| O03 | P2 | query_ball_point, radius1.1/1.0 | 거리와 거리순 인덱스, 구 경계 | 실제 새 반환은 인덱스만. exact radius는 경계점도 포함. complex는 양판 같은 TypeError | `H-O03-P2-normal/exact_boundary/complex_query` | 후속 권고와 drop-in 출력 계약은 다름 | 거리/정렬/경계/형 adapter 필요; adapter 자체는 미검증 |
| O04 | P1 | 공급자 input[[1,2],[3,4]], labels[[1,2],[2,4]], index[4,8,2] | 순서[4,0,5], 없는 label은0 | 양판 실제 float64 shape[3], [4,0,5] | `H-O04-P1-provider`; PR12242 test | 없음: 실행 범위에서 원문 기대와 일치 | 부분 수용 |
| O04 | P2 | sum_labels; float32/빈/complex/labels shape 경계 | 원 값/형과 오류 | P1/P2 총10대응: 반환 일치6, 오류 일치4. complex TypeError, shape ValueError 메시지도 일치 | `H-O04-P2-*` | live 구 문서404지만 현재 구 함수도 동작 | 요구별 결론 불변; 별칭② 지지 |
| C01 | P1 | 0.8→0.9 `from scikits.learn.datasets import load_iris` | 옛 import·필드 | alias source가 sklearn.datasets를 전달. 배열 bytes/양판 native 미관측 | `C01-P1`; `R005`, `R024–26` | forwarding 구조와 모든 데이터 동등성은 별도 | 판 한정 alias, 행동 보류 |
| C01 | P2 | 0.9 estimator.fit에 model parameter 또는 default gamma | 옛 호출/기본값 계약 | 공지는 fit parameter 제거와 gamma 1/n_samples→1/n_features를 명시. native 미실행 | `C01-P2`; `R002/4` | 같은 프로젝트·namespace alias와 다른 estimator 기능의 변화 공존 | 무조건 교체 기각. load_iris 실패로 일반화하지 않음 |
| C02 | P1 | 원PIL1.1.7와 Pillow의 import layout, 같은 PNG를 load까지 | import와 decoded pixels | 원 selftest도 이미 `from PIL import Image`. 2010 installer별 차이 보고. 현재 top-level Image import 실패. 원PIL native 미실행 | `C02-P1`, `PA-O01/02`; `R015`, `PA006/7` | 같은 import 문자열은 배포물 ID가 아님; open은 lazy | 환경별 보류. 새 import를 fork가 처음 도입했다는 가설 기각 |
| C02 | P2 | 2×1 RGB 빨강/초록 PNG, invalid bytes; 현재 Pillow13.0 | 순서·mode·size, 오류 | 현재 roundtrip 성공/UnidentifiedImageError. 원PIL source는 단계별 IOError/ValueError 등을 정의; 원판 실행 미확인 | `C02-P2`, `PA-O03`; root runtime 원행 | 현재 성공을 역사판 equivalence로 승격하지 않음 | 현재 fixture 수용, 역사 교체 동등성 보류 |
| C03 | P1 | 3.11 imp 계약→3.12.14 `import imp` | 기존 함수 호출 | 현재 ModuleNotFoundError. live 문서는200이나 원절 없음 | `C03-P1`; `R016/17/32`, runtime | 문서 transport 생존과 API 생존 불일치 | 기존 호출 기각 |
| C03 | P2 | find_spec(json), 존재하지 않는 모듈 | 옛 3-tuple·ImportError | 현재 ModuleSpec와None. 옛 계약은 원문/source로 확인, 양판 native 아님 | `C03-P2`; `R016/19/33` | 개별 대체 경로에도 결과/예외 변환 필요 | drop-in 기각; 명시적 계약 변환 후 재검사 |

## 필수 표3 — 옛 근거를 보존하는 수선·보류 원장

관계의 시작/종료 범위와 복구 방식은 [relations.csv](relations.csv)에 있다. 모든 행은 옛 ID·판정·인용을 남긴다. 새 관계를 나중에 비활성화할 수 있으며 옛 레코드를 덮어쓰지 않는다. ① ID 유지, ② 범위 있는 별칭, ③ 이미 혼합된 레코드의 분리, ④ 별도 ID의 방향 관계, ⑤ 보류다.

| 구 ID | 새 ID | 관계/방향 | 적용판 | 원주소 수선 | 과거 인용 | 단순 수선과의 차이 | 오류 영향 | 재개 조건 |
|---|---|---|---|---|---|---|---|---|
| G01-R01 RASDAMAN driver | 같은 논리 driver | ① 유지 | core3.6까지,3.7 제거 | 고정 옛 문서 추가 | 3.6 원절 유지 | 소스 존재와 실행 부품을 구별 | 설치·쓰기 가능성 오인 방지 | 정확 build/server로 pixel reader 실행 |
| G01-R02 core source component | extra-drivers source component | ④ moved_to_source → | 2023-03-12/3.7 | 수신 commit 추가 | 이전 source/문서 유지 | 수신자가 비통합·미유지라고 밝힘 | README3.5로 실제 이관판을 잘못 정하는 것 방지 | 수신 build·지원판 선언 |
| G02-R01 ARG driver | 같은 퇴역 ID | ① 상태·유효판 유지 | 3.8 opt-in,3.9 제거 | 마지막 원판+제거 공지 | 옛 동작 보존 | 404 보류보다 구체적 퇴역 기록 | 마지막 유효 설정 손실 방지 | -9999를 보존하는 명시 후속/변환과 아직 미시험 자동감지·손상입력 |
| G02-R02 ARG driver | 미지정 | ⑤ 후속 보류 | 3.9 이후 | 임의 GTiff alias 금지 | 보존 | 변환 workflow와 동일 ID를 구별 | nodata/형/CRS 손실 가능 | 실제 변환품과 roundtrip |
| G03-R01 Parquet driver | 같은 driver ID | ① 위치 수선 |3.7→3.8 | current canonical URL+고정판 | 원 beta/final 인용 보존 | driver와 format판 구별 | 주소 수선만으로 출력판 보증 불가 | 정상·지정 오류는 GN01–03 확인; 실제 추가 입력/소비자만 재검사 |
| G03-R02 format beta.1 | format1.0.0 | ④ 후속판 → | writer3.8부터 | final 규격/source 추가 | beta 기대 유지 | URL 한 개로 두 출력판을 덮지 않음 | 새판을 모든 구consumer 실패로 추정하지 않음 | 구3.7 정상 읽기는 GN02 확인; exact beta 제한/외부consumer만 별도 |
| G04-R01 GEOARROW@3.8 interleaved | GEOARROW_INTERLEAVED@3.9 | ② 판 한정 별칭 → | 3.9 명시 | 이름·시작판 추가 | 옛 옵션 인용 유지 | 새 철자 때문에 별 기능으로 중복시키지 않음 | 중복 작업·잘못된 이관 안내 | 실제 소비자의 필수subset/exact schema/null 정책; bboxNO 조합은 미실행 |
| G04-R02 GEOARROW@3.8 interleaved | GEOARROW@3.9 struct | ④ 다른 encoding 관계 → | 3.9 | 두 옵션 의미 분리 | 보존 | 같은 이름·200이어도 같지 않음 | type/null 의미 불일치 | 실제 소비자 계약·bboxNO 조합; GN05–07의 schema/손실 관측은 완료 |
| G04-R03 판 없는 혼합 레코드 | 위 두 typed ID | **③ 조건부** | 실제 혼합 입력이 있을 때 | 원 revision 보존 후 참조 분리 | 보존 | U가 표현 못 하는 분리 | 실재 오류 수로는 미산입 | 원 추천 record+호출 옵션 확보 |
| O01-R01 median_absolute_deviation | median_abs_deviation | ④ scale adapter 필요 → | 1.4.1→1.5.0 | 대체 주소와 인자 변환 추가 | 1.4826·빈 배열 계약 유지 | 이름 변경과 계산 계약을 구별 | 정상 기본값·빈 형상 차이 | 실제 caller의 빈/NaN/경고 정책 |
| O02-R01 integrate.simps | integrate.simpson | ② qualified alias → | 1.6; 구명1.14 제거 | 새 이름 추가 | 보존 | 짧은 이름 하나로 합치지 않음 | 별도 native 미검증 범위 | simps 정상/경계 쌍 실행 |
| O02-R02 integrate.trapz | integrate.trapezoid | ② qualified alias → | 1.5.4→1.6; 구명1.14 제거 | 새 주소 추가 | 구판·NumPy pin 유지 | 실제 범위 일치 확인 | 전판 전체 호환으로 과장 금지 | 필요한 추가 입력만 검증 |
| O02-R03 integrate.cumtrapz | integrate.cumulative_trapezoid | ② qualified alias → | 1.6; 구명1.14 제거 | 새 이름 추가 | 보존 | 같은 결정이지만 다른 기능 ID | 누적 출력/initial 계약 별도 | cumtrapz 개별 양판 실행 |
| O02-R04 stats.trapz | stats.trapezoid | ② 분포 alias → | 1.6 도입; 종료 미확인 | stats namespace 보존 | 보존 | integrate와 합치지 않음 | 숫자 대신 분포 객체 호출 방지 | 실제 분포 parameter 계약 |
| O03-R01 query(k=None) | query_ball_point | ④ 기능 이동 → | 1.6 경고, 실제1.9 제거 | 구 mode 원절+새 메서드 | tuple/거리/경계 유지 | live query200에 숨은 mode 제거 판독 | 거리 유실·경계점 추가·scalar 형 변화 | 거리·정렬·strict경계·형 adapter 검사 |
| O04-R01 ndimage.sum | sum_labels | ② alias → | 1.5.4→1.6 | preferred URL 추가 | 옛 이름도 유지 | 404를 삭제/분리로 해석 안 함 | 같은 label 계산 중복 방지 | 요구되는 추가 dtype/error만 |
| C01-R01 scikit-learn project | 같은 project | ① 유지 | 0.8→0.9 | 살아 있는 고정판 위치 추가 | 옛 이름 유지 | project와 import ID 구별 | 프로젝트 분열 오인 방지 | 필요한 estimator판 확인 |
| C01-R02 scikits.learn | sklearn | ② namespace alias → | 0.9,0.11 제거 | 범위 있는 별칭 | 0.8 인용 유지 | 영구 alias로 만들지 않음 | fit/default 변화 누락 방지 | 역사 환경의 실제 caller |
| C02-R01 PythonWare/Imaging | Pillow | ④ fork → | 2010 선언;2.0 source;13.0 현재 별도 | 원 archive+fork 공지 | 원저자·1.1.7 근거 유지 | 같은 import/버전상수/도메인 불충분 | 별도 배포물 병합 방지 | 동일 이미지 load/오류 양판 |
| C02-R02 PyPI:PIL 이름 | 같은 registry 이름 | ① 소유권 속성 변경 | 2020-01-03 | 이전 완료 댓글 추가 | 옛 release provenance 유지 | 이름 소유권≠배포물 ID | 과거 PIL을 Pillow로 재라벨 방지 | exact installed artifact metadata |
| C02-R03 unqualified PIL record | distribution/import/registry ID | **③ 조건부** | 실제 혼합 입력이 있을 때 | namespace별 참조 분리 | 원 revision 유지 | 이 연구에 실제 mixed record 없음 | 오류 분자 미산입 | 원 추천과 설치 metadata |
| C03-R01 imp.find_module | 같은 퇴역 함수 | ① 유지 | 3.11까지,3.12 제거 | 3.11 anchor 추가 | 원 tuple/예외 근거 유지 | current200으로 원절 손실 안 덮음 | 옛 답 검증 가능성 보존 | 원 caller의 요구 기록 |
| C03-R02 imp.find_module | importlib.util.find_spec | ④ 개별 후속 → | 3.12 이관 | 메서드별 안내 추가 | 옛 호출계약 유지 | imp 전체 alias 금지 | ModuleSpec/None 변환 누락 방지 | result/예외 변환 시험 |
| EXT01-R01 IANA language:mo | IANA language:ro | ② Preferred-Value → | Deprecated2008-11-22 | registry/request 추가 | 원 tag+판 유지 | 정확 namespace/날짜 구별 | 이전 mo.txt의 다른 사건 혼동 방지 | 필요시 원 ISO 변경 승인 자료 |
| EXT02-R01 IANA language:bhk | fbl/lbl/rbl/ubl | ④ split successors → | 2010-03-11 | 4개 방향 관계 유지 | bhk 원자료 보존 | 한 목적지 수선 불가 | 세 대안 유실 방지 | legacy 내용/지역의 구별 근거 |
| EXT02-R02 bhk가 붙은 특정 자료 | 아직 미지정 | ⑤ 단일 매핑 보류 | 구별 전 | 자동 첫 값 선택 금지 | 보존 | 관계와 개별자료 재분류를 구별 | 잘못된 한 언어 선택 방지 | 어느 수신 언어인지 판별 자료 |

## 판단 요약과 분모

**수선의 기준 단위는 URL이 아니라 namespace가 있는 대상 ID와 판, 그리고 그때 추천한 기능 계약이다.** 계보상의 동일성과 행동상의 대체 가능성은 독립적으로 기록해야 한다. 같은 프로젝트가 이름을 바꿔도 특정 함수의 기본값은 달라질 수 있고, 다른 배포물이 같은 import namespace를 사용할 수 있다. 옛 문서가 살아 있어도 원 기능 절이 사라질 수 있다. 주소는 이 대상과 근거를 찾는 위치이며, 그 자체로 합병 지시가 아니다.

이번 제안은 옛 레코드를 지우지 않고 `original ID / namespace / kind / edition / configuration / source section / original behavior`를 남긴 뒤 새 위치와 방향 관계를 추가하는 방식이다. 각 관계에는 시작·종료 범위, 선언 근거와 행동 근거, 복구 방법, 보류를 바꿀 관측을 둔다. ③은 실제 혼합 레코드가 있을 때 적용한다. 실제 운영 레코드는 제공되지 않았으므로 G04/C02의 ③은 조건부 제안이고 완료한 분리나 운영 오병합으로 세지 않았다.

| 층 또는 증거 단위 | 확인/분모 | 해석 |
|---|---:|---|
| GIS 자연 모집·양판 원문 | 4/4 | 5개 공지 전체와 후보115행, quota 이후도 기록 |
| OSS 자연 모집·양판 원문 | 4/4 | 10개 공지와 후보25행. 반복 wminkowski 사건 제외 |
| 대조 모집·전후 원문 | 3/3 | C02 orig archive 추가 확보로 최초 원판 공백 보완 |
| 외부 실제 등록 이력 | 2/2 | IANA mo→ro, bhk→4개 수신자; 자연층에 미산입 |
| 독립 원저작 | 32/최소20 | GIS9+OSS6+대조10+외부7; 원PIL 미러·고정 source pin은0 추가 |
| 출처/접근 행 대 직접 본문 행 | 166 대121 | 실패·메타·기계 선별을 직접 본문 수에 섞지 않음 |
| 양판 native 기능 실행 | OSS4/4; GIS3/4; 대조0/3 | 자연 총7/8. 현재 단독 실행·같은판 GN07/GN11·HTTP는 이 분자에서 제외 |
| OSS 과거 원 호출/대응 | 200호출 /49대응 | 46 exact input hash,3 명시 인자 매핑. 독립 사건49개가 아님 |
| GIS 후속 실행 묶음 | GN11묶음: 양판9·같은판2 | 자연 사건3개만 산입. 원 실행/설치/환경 출력 영수증65개 해시 검증, 재개 때 핵심7개 read 재현 |
| 두 요구 적용 | GIS3/4에 P1·P2 모두; OSS4/4 모두 | G01 full CRS/write는 원래 역할 밖. 각 분야 최소1 같은 쌍 조건 충족 |
| 가림 재판독 | 자연4+대조2 / 지정6 | 별도 도구 에이전트. 첫 판정 가림, 출처 선정은 비가림 |
| 실제 기존 레코드 교정 | 제공0/11 | 본문 관계는 적용 가능한 연구 제안; 운영 오류율/정확도 없음 |

### Q1. 무엇이 변했고 무엇이 그대로인가?

**위치, 등록 ID, 배포물, 기능, 문서판은 한 필드로 합칠 수 없다.** G03은 driver ID가 그대로인 채 출력 format판이 변한다. G04는 같은 옵션 이름이 다른 encoding을 뜻하는 동시에 옛 encoding에 새 별칭이 생긴다. O02는 한 명명 결정 안의 네 qualified 기능이 각각 alias를 얻는다. C02는 import namespace와 일부 버전 상수가 같아도 배포물과 제공자가 다르다. C03은 live 문서 위치가 그대로인데 함수의 원절과 실행 가능성이 사라진다.

Q1의 독립 근거는 양판 등록/source, 판별 URL 응답과 원절이다. G01은 3.6 등록 호출/source와 3.7 부재, 수신 commit을 역으로 확인했다. G02는 3.9 source404만으로 삭제를 단정하지 않고 등록부 부재와 제거 공지를 함께 봤다. OSS의 모든 선택된 양판 API 문서는 현재200이지만 unversioned 구주소는3개404,1개200이다. HTTP 상태와 함수 사용 가능성이 서로 다른 축임을 O03/O04가 반대 방향으로 보여준다. [원문·도착 원장](sources.jsonl), `G01–O04-HTTP-U`, `O04-HTTP-COUNTER`, `C03-P1`을 함께 읽어야 한다.

### Q2. 누가 어떤 판에서 계보를 선언했고 수신자는 무엇을 확인했는가?

G01은 GDAL의 이관 공지와 수신 repository의 실제 원본을 함께 읽었다. 그러나 수신 README의 범용 “3.5 제거” 문구는 정확한 Rasdaman 이력과 맞지 않았다. 이 문구만 믿고 첫 후보를 역사적 재공지로 제외하려던 잠정 해석을 기각했다. 원판·정확 commit을 읽은 뒤 **봉인한 선정 규칙을 그대로 적용**해 G01을 첫 적격 사건으로 되돌렸다. 원순위와 이 경위는 모집 원장과 protocol-deviations에 남겼다.

O01–O04는 원/수신 기능의 발행자가 SciPy로 같으나, 이 사실은 행동 호환성을 보증하지 않는다. PR12382가 옛 mode를 undocumented로 부른 표현도 1.5.4 Returns 원절의 계약을 지우지 않는다. C01은 명시적 namespace rename과 shim이 있다. C02는 fork 작성자의 공지뿐 아니라 원 PIL 저자의 답변을 읽었고, 그 답변의 패치 선호를 포괄적 병합 승인으로 해석하지 않았다. PyPI 관리자의 2020 transfer 완료와 2024 보관 방침 댓글은 **registry 이름 소유권**에 관한 별도 증거다. [2010 fork 공지](https://mail.python.org/pipermail/image-sig/2010-July/006423.html), [원 저자 답변](https://mail.python.org/pipermail/image-sig/2010-August/006429.html), `R014`, `PA001/2`가 서로 다른 주장을 뒷받침한다.

### Q3. 동일 입력의 정상·경계 결과는 어디까지 선언과 맞았는가?

SciPy는 실제로 CPython3.8.20·NumPy1.19.5를 공통으로 둔 네 분리 환경에서 실행했다. **O01 정상 P1은 값·형이 같지만 빈 배열 형상은 다르고, O03은 정상 값이 같아도 scalar 형이 다르며 exact radius의 구성원도 다르다.** 반대로 O02의 실행된 trapz/분포 alias와 O04의 label 합산은 정상·지정 경계·오류에서 같은 결과를 냈다. 차이를 찾는 시험만 골라 결론을 만들지 않고 결론 불변 사례도 남겼다. 자세한 원행·동일 입력 해시·예외·경고는 [역사 실행 결과](streams/oss/historical/HISTORICAL_RESULTS.md)와 `H-` 관측에서 확인할 수 있다.

49대응 가운데3행은 같은 기록 인자가 아니다. MAD의 reciprocal scale과 KDTree의 `distance_upper_bound`→`r` 대응을 명시해 비교했다. 이를46개 exact input hash와 분리했다. 경고 후 예외가 나는 경우 원 probe는 경고를 보존하지 못하므로 null을 “경고 없음”으로 비교하지 않았다. O02의 simps/cumtrapz 개별 동작은 source alias만 읽었고 실행 범위에 넣지 않았다.

GIS의 후속 실행은 G02·G03·G04 세 사건이다. 최초 공급자 `test.parquet`는 판별 bytes가 달랐으므로, 후속에는 생성 입력과 생성 파일의 SHA-256을 고정해 양판에 같은 bytes를 넣었다. G03은3.7이 만든 파일을3.7/3.8에서 읽고,3.8이 만든1.0.0 파일을 구3.7 소비자에서도 읽었다. 필수 값·형·순서·geometry·EPSG4326·축 매핑이 보존되어 포맷판 변경이 모든 구 소비자를 깨뜨린다는 가설을 반박했다. invalid compression과 PointM 선언은 두 판에서 동일 단계의 RuntimeError/예상 종료3이었다. [GN01–GN03](streams/gis/historical/observations.jsonl), [불변 입력·출력](streams/resume-gis/audit.json).

G04는 동일 WKB 읽기 P1이 보존되지만, 새 같은 이름의 struct 파일을 구3.8 소비자가 열면 **종료0·geometry field0·CRS 없음**이었다. 정상 종료와 필수 기능 충족을 분리해야 한다. 판 한정 별칭 `GEOARROW_INTERLEAVED`는 geometry·CRS를 복구하나 구 소비자에 bbox4속성이 추가되므로 필수 필드 부분집합과 정확 schema 요구를 나눴다. 같은3.9 환경에서 struct와 interleaved를 대조한 GN07은 null1개 대0개/EMPTY 치환을 직접 보인다. 옛3.8 interleaved에도 null→EMPTY가 있어 새 이관 손실로 세지 않는다. [GN04–GN07](streams/gis/historical/observations.jsonl).

G02의 기본 호출은3.7 성공→3.8 gate 거절→3.9 driver 부재로 바뀐다. YES opt-in은 읽기를 복구하지만 봉인한-9999 NoData는3.7부터 이미-32767로 보고되어 전체 요구의 성공 기준이 아니었다. 쓰기 뒤 구 소비자에서도 같은 한계가 남는다. G01의 no-georeferencing/read-only도 이전부터의 한계다. 두 사건 모두 원래 없던 능력을 새 이관 손실로 세지 않았다. [GN08–GN11](streams/gis/historical/observations.jsonl).

GIS 실행환경은 conda-forge 재빌드이며 출시 당일 binary 또는 GDAL 판만 바꾼 인과 실험이 아니다. G03 두 writer의 C++ Arrow는10.0.1이다. G04의 Python pyarrow는 양쪽14.0.2지만 실제 파일은 구 writer C++ Arrow14.0.1, 신 writer14.0.2를 기록한다. PROJ와 다른 build도 다르다. 이 한계를 환경 원장과 각 GN 관측에 명시했다. [환경](streams/gis/historical/environment-packages.json) · [비가림 재검증](streams/resume-gis/audit.md).

### Q4. URL만 수선하면 어떤 오류를 낳는가? 기준이 없는 건수는?

봉인한 U를 그대로 적용하면 자연층은 **위치 수선+유지2/8, 같은 URL 유지1/8, 보류5/8**이다. 대조층은 **수선+유지1/3, 같은 URL 유지1/3, 보류1/3**이다. 301 다음404도 최종 실패이므로 보류다. [실제 입력·조치11행](evidence/url-policy-comparison.json)에 요청·도착·체인·시각을 남겼다.

서로 다른 오류를 한 오병합률로 합치지 않았다. G03은 driver ID 수준에서 U의 위치 수선이 맞다. 다만 beta/final 출력판 구별은 표현하지 못한다. G04는 기능 encoding 수준에서 같은 `GEOARROW` 이름/주소를 유지하면 두 의미를 구별하지 못하는 **규칙 적용상 구별 누락1/8**이다. O03은 live 메서드 문서가 남은 채 특정 mode가 제거된 **기능 지속성 누락1/8**이며, C03도 대조층에서 원 기능 절을 놓치는 **1/3**이다. C02는 현재 페이지와 원 PIL 발행자 사이의 저자 연속성을 확인할 수 없는 **인용 출처 검증 문제1/3**이다. 작성자나 소유자가 실제 바뀌었다고 단정하지 않는다. 이 네 분자는 서로 다른 단위여서 더하지 않는다.

**운영 오병합을 직접 관측한 분자는0이고 운영 레코드 검증 분모도0이다.** 실제 추천 레코드가 제공되지 않았기 때문이다. U는 분리 조치를 표현하지 못하므로 관측 거짓 분리를 만들지 않았다. U의 보류6/11을 오류로 바꾸지도 않았다. O04/C01에서 새 철자마다 별도 기능을 만드는 가상 정책은 중복 작업을 만들 수 있지만, 그것은 봉인한 U가 아니라 별도의 반례다.

발행자 선언·원절·구현에 의한 식별 기준은11/11에 연결했다. 행동 기준은 한층 좁다. 자연층의 같은 입력 과거 native가 있는 것은7/8, 없는 것은G01의1/8이며, 대조층은0/3이다. 현재 단독 실행은 후자의 결손을 자동으로 메우지 않는다. 이 연구로 전체 웹 링크의 정확도나 기능 호환 확률을 추정할 수 없다.

### Q5. 같은 쌍의 P1과 P2가 달라지는가? 불변 사례는?

O01의 정상 scalar 범위는 명확하다. 기존 이름의 P1은1.4826을 유지하고 새 이름 기본값 P2는1.0이 된다. 다만 P1 전체가 통과한 것은 아니다. 빈 배열을 포함하면 구 wrapper도 형상이 바뀐다. **부분 수용의 범위를 행에 남기지 않으면 이 사례 자체를 잘못 요약하게 된다.** O03도 정상 값 부분과 엄밀 형/경계 계약을 구별해야 한다. 새 ball 메서드를 단순 대입하는 P2는 거리 출력 자체를 잃는다.

G04에서는 같은 전후 쌍의 기존 default WKB 읽기 P1을 지정 정상 입력에서 수용하고, 같은 이름의 새 encoding을 쓰는 P2를 구 소비자의 geometry/CRS 실제 손실로 기각했다. 새 별칭은 geometry를 복구하지만 exact-schema 요구에는 bbox 추가 속성을 따져야 한다. G03은 같은 정상 입력과 지정 오류에서 P1/P2가 모두 맞아 결론 불변인 GIS 반례다. O02의 실행된 함수와 O04는 P1/P2 모두 지정 입력에서 일치해 결론 불변이다. G01은 처음부터 writer 역할이 없어 P2 적용 외이며, 이를 P1 성공/P2 실패라는 이관 효과로 포장하지 않았다.

### Q6. 외부 전거·표준에서 무엇을 옮길 수 있고 무엇은 별도 시험해야 하는가?

[IANA registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry)의 File-Date2026-11-18 판과 두 실제 등록 요청을 직접 읽었다. `mo`는 Deprecated2008-11-22와 단일 Preferred-Value `ro`를 갖는다. 원 요청은 upstream 표준 변경2008-11-03과 registry 반영을 구별하게 한다. 같은 이름의 `mo.txt`는 더 이른 설명 변경이라 이번 폐기 근거가 아니었다. `bhk`는2010-03-11 폐기되며 Comments의 수신자 fbl/lbl/rbl/ubl 네 개가 실제 등록되어 있으나 단일 Preferred-Value가 없다. 각 수신자의 Added와 Macrolanguage도 역확인했다. [EXT01/EXT02 원장](streams/standards/external-records.json), `STD-S01/06/07/08`에 기록했다.

가져올 수 있는 규칙은 namespace 명시, 원 ID 비삭제, 폐기/대체 날짜, 일대다 관계, 수신 레코드 역확인, 원문 출처 보존이다. `bhk`의 첫 수신자를 임의 선택할 수 없듯 함수 fork의 첫 도착 URL을 정답으로 선택해서는 안 된다. RFC5646의 tag canonicalization, RFC8141의 URN 식별·해석 분리, RFC3986의 URI equivalence 범위와 LC NACO의 이름/인용 정책은 이 설계를 보조한다. LC 정책 설명을 실제 인명 합병 사례라고 꾸미지는 않았다.

옮길 수 없는 것은 **소프트웨어 행동의 보증**이다. 언어 tag의 preferred value는 median 함수의 scale, KDTree의 경계 포함, encoding의 null/EMPTY를 시험해 주지 않는다. 이런 계약은 입력 bytes, 의존성, 호출 설정, 소비자 판, 결과 형/순서/예외로 별도 검사해야 한다. 같은 공급자의 규범 설명도 오래된 manual과 새로운 writer 사이에서 어긋날 수 있으므로 규범과 실행 열을 합치지 않는다.

### Q7. 무엇 하나가 보류를 바꾸며, 옛 답을 다시 읽을 때 무엇을 남겨야 하는가?

보류는 “더 조사”가 아니라 구별 입력과 다음 행동을 가진다. O03은 exact radius1.0 한 입력이 경계 보류를 실제 불일치로 바꿨다. O01은 빈(3,0) 입력이 정상값 adapter의 적용 한계를 바꿨다. C02는 .dsc에 적힌 orig archive 해시와 일치하는 원 tarball이 원소스 공백을 줄였지만 native 호환성을 증명하지는 않았다. 이런 상태 변화는 이전 행을 삭제하지 않고 추가 관측에 연결했다.

G03의 한 해시로 고정된 Parquet, G04의 Point/null/EMPTY, ARG의 같은 bytes에 대한 default/YES 구별은 후속 실행으로 이미 확인했다. 그때의 보류를 이 결과판에서 갱신하고 원 예측 행은 남겼다. 이제 G04 exact-schema 보류를 바꿀 최소 추가 입력은 같은 fixture에 `GEOARROW_INTERLEAVED`와 공식 옵션 `WRITE_COVERING_BBOX=NO`를 함께 적용해 구 소비자의 필드를 보는 것이다. 이 조합은 아직 실행하지 않았다. G03의 추가 범위에는 비대각 좌표·실제 null·특정 외부 소비자 계약이 필요하다. ARG는-9999 봉인 raster를 고정 nodata로 몰래 바꾸어 성공시킬 수 없고, 정한 nodata를 보존하는 이름 있는 변환 구현이 필요하다. Rasdaman은 정확한 raslib/server와 수신 source build가 첫 장애다. C03은 옛 caller가 tuple/ImportError 중 무엇을 실제 요구하는지 확인하면 명시적 변환의 수용 범위를 좁힐 수 있다. [REPRODUCE.md](REPRODUCE.md)와 stream별 재개 명령에 입력을 명시했다.

옛 답에는 원 ID·판·설정·문서 절·당시 기대·출처 지문·당시 판정을 남겨야 한다. 새 관계의 방향, 시작/종료판, 새 증거 수준, 변경 이유를 별도 revision으로 덧붙인다. 현재 답을 더 정확하게 만드는 일과 과거 답을 소급해서 다른 뜻으로 바꾸는 일을 분리하는 것이 수선 원장의 목적이다.

## 추가 분석 — 초기 판단을 뒤집은 근거와 가림 검토

첫 결론에서 멈추지 않기 위해 다음 반례를 실제로 추적했다. G01의 일반 README3.5 문구는 구 등록부·수신 commit으로 반박되어 모집에서 잘못 빼려던 잠정 해석을 취소했다. O02의 stats/integrate 이름 변경은 같은 명명 결정임을 issue로 확인해 여러 사건으로 늘리지 않았다. wminkowski는1.6에서 새 경고가 보이지만 원 PR이1.0 이관의 반복임을 밝혀 제외했다. C02 현재 PythonWare200은 원 저자 연속성의 증거가 되지 않았고, PIL의 원 selftest도 from-PIL import를 쓴다. O03의 문서/정적 분석 보류는 실제 경계·형 변화 관측으로 바뀌었다. 모두 [protocol-deviations.md](protocol-deviations.md)와 원순위·실행 원행에 남겼다.

별도 판독자는 첫 판정과 수선안을 가린 상태에서 G01/G02/O01/O02/C01/C02를 읽었다. 최초 snapshot은11:41:36 UTC, 가림 결과 완료는11:41:51 UTC, 첫 snapshot을 판독자에게 공개한 기록은11:46:41 UTC다. 처음의 잠정 GIS packet을 읽은 경위와 최종 packet 해시도 보존했다. 정규화한 코드 집합은 G02에서 최초 `{1}` 대 재판독 `{1,5}`로 달랐지만 최초 산문에도 후속 미지정⑤가 있어 의미상 충돌보다는 기록 범위 차이였다. 나머지 다섯의 요약 관계는 같다. **통계적 독립 일치율·정확도는 계산하지 않았다.** 같은 도구 계열이며 출처 선정이 가려지지 않았고, 뒤에 추가한 native 실행을 처음 가림판독에서 본 것도 아니다.

재판독 뒤 원장을 별도로 검사해 UTC 안내문, 실행 ID의 파일 경로, mutable 대표 source 위치를 보완했다. current HTTP11행을 native 기능 시험 수에 넣지 않도록 명시했다. 스크립트 종료0은 참조·범위·분모 검사가 끝났다는 뜻이며, 미실행 행동까지 승인했다는 뜻이 아니다. [가림 대조](streams/review/RECONCILIATION.md), [원장 검토](streams/review/ledger-audit.json), [수정 근거](evidence/ledger-audit-resolution.json)를 함께 보존했다.

재개 검토에서는 세 도구 에이전트가 비가림으로 출처·GIS·OSS를 나누어 감사했다. GIS 출력 영수증65개와 writer해시6개를 대조하고 생성 파일11개를 보존했으며, 핵심7개 read 재실행은6개 종료0·예상 거절1개 종료3이었다. OSS는 원200호출/49대응의 해시를 확인하고18개 핵심 호출을4개 기존 환경에서 다시 실행했다. 독립 원저작을 코드·시험 계보까지 더 합쳐 제외하는 보수적 민감도에서도27건으로 최소20을 충족한다. 원문 최소량 감사와 행동 수용은 구별했다. [GIS 감사](streams/resume-gis/audit.md) · [OSS 감사](streams/resume-oss/audit.md) · [모집·출처 감사](streams/resume-sources/audit.md).

## 가장 중요한 불일치·약점 3건과 다음 확인

1. **계보와 정상값이 맞아도 경계 계약은 달랐다.** O01은 normal scale adapter가 작동해도 빈 배열의 scalar/array가 달라지고, O03은 경계 포함과 인덱스 형까지 바뀌었다. 다음 확인은 실제 caller 계약을 적은 뒤 O01 빈 형상, O03 거리·정렬·strict 경계·형을 복구하는 adapter를 같은 원 입력에 넣는 것이다. 이번 연구는 adapter의 필요성을 입증했으며 완성된 호환 layer를 제공하지 않는다.

2. **같은 발행자·같은 판·같은 파일 이름도 원근거의 불일치를 숨겼다.** G01 README의 포괄적 제거판과 정확 commit이 다르고, G03의3.8 manual과 실제 writer format판도 달랐다. 고정 bytes 후속 실행에서는 G03 구 consumer가 새 출력에 성공한 반면 G04 구 consumer는 정상 종료에도 geometry·CRS를 잃었다. G04의 새 별칭은 geometry를 복구하되 bbox 속성을 추가한다. 다음 확인은 같은 입력의 `WRITE_COVERING_BBOX=NO` 조합과 실제 소비자 schema이며, rasdaman은 정확 server/build 없이는 여전히 보류다.

3. **현재 주소의 생존과 연구용 규칙 대조에는 적용 한계가 있다.** C02의 미확인 발행자 연속성, C03의 사라진 원절, G04의 재사용 옵션 이름을 HTTP만으로 알 수 없었다. 그러나 실제 운영 추천 레코드가 없어 생산 환경의 오병합/분리율을 산출할 수 없고, 별도 에이전트 검토도 독립 표본 평가가 아니다. 다음 첫 확인은 원 추천 레코드 한 개의 namespace·판·호출·소비자 요구를 확보해 이 원장 관계를 적용한 전후 diff를 검토하는 것이다. 옛 ID와 인용을 지우지 않는 조건은 계속 유지한다.
