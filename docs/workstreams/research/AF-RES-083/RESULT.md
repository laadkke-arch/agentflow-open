# AF-RES-083 — 배포된 안내의 판·조건별 수선 판정

## 표1. 옛 배포 지시와 아직 비어 있는 근거

| 원 레코드ID·모집 순번 | 소비자·배포판·URL#절 | 독자에게 권한 행동 | 필수 출력·설정 | 상류 ID·판과 확인 수준 | 빈 근거 |
|---|---|---|---|---|---|
| G04-1 · G04의 1번 | GeoPandas 0.14.4, [I/O 안내 L272–275](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L272-L275) | `read_parquet`·`GeoDataFrame.to_parquet`로 공간 정보를 보존하며 왕복한다. | geometry·CRS를 포함하는 공간 정보. 정확한 원 fixture·CRS 번호는 문단에 없음. 고정 구현의 기본 encoding은 WKB. | G04/GDAL 3.9와 같은 포맷 생태계지만 **직접 GDAL GEOARROW 호출은 아님**. GeoPandas→PyArrow 경로·WKB 기본값·소비자 시험을 정적으로 확인. G083-S01–06. | 실제 설치 PyArrow/GEOS/PROJ, 원 예제 입력·출력, 해당 소비자 실행. GN04 성공·GN05 실패를 전용할 수 없음. |
| G04-2 · G04의 2번 | GeoPandas 0.14.4, [같은 안내 L279–285](https://github.com/geopandas/geopandas/blob/60c9773e44fff8a35344c2a74431e00c5546a4ee/doc/source/docs/user_guide/io.rst#L279-L285) | `schema_version`으로 옛 사양판을 선택하고 지원되는 파일을 읽는다. | 쓰기 지원판 0.1.0/0.4.0/1.0.0-beta.1/1.0.0. 옛 reader는 WKB 범위. 당시 1.0.0 문맥의 “files of any version”. | 같은 GeoParquet 저장소 링크이나 **사양판·encoding·reader 판은 별개**. 옛 validator의 non-WKB 거부, 1.0.0의 native 지원을 정적으로 확인. G083-S02, S20–22. | 원 문장이 미래 native 인코딩까지 약속했다는 근거, 그 조건으로 재사용된 실제 안내 레코드, 실제 소비자 실행. |
| G04-3 · G04의 3번 | **공석**. QGIS `manual_1.8_en`, GeoPandas 0.14.4, Arrow 16.0.0까지 등록 순서로 검색. [검색·제외 원장](frame.csv) | 적격 공간 안내 미검출. Arrow의 일반 Parquet 표 읽기는 보조층 AUX-G04-A1. | a/b/c 표를 여는 것과 geometry·CRS 복원은 다른 요구. | GeoArrow 정의·일반 Parquet 예제는 읽었으나 G04의 동일 호출 지시로 연결되지 않음. G083-S07–10. | 원 사용 지시가 없어 수선·후속 정오 판정 적용 불가. |
| O02-1 · O02의 1번 | **공석**. statsmodels 0.12.1→Astropy 4.2→scikit-learn 0.24.0의 고정 범위 검색. [검색 원장](streams/oss/old-search.json) | 등록 검색에서 대상 SciPy 심벌을 권하는 안내 미검출. | 내부 적분 호출과 독자에게 권한 행동을 구별. | O02/SciPy 1.6.0 명칭 이관은 확인. 이 자리에 연결할 원 안내 없음. | 원 지시·실제 설치판·소비자 수용 기준. |
| O02-2 · O02의 2번 | **공석**. 같은 고정 후보틀의 두 번째 예약 자리. | 보조층의 `quad`/`dblquad`·`Trapezoid1D` 안내로 채우지 않음. | 같은 이름이나 namespace만으로 동일 함수가 되지 않음. | 서로 다른 심벌이라는 정적 반대 근거만 확보. O-S07–08. | 해당 원 지시가 없어 A/B 적용 불가. |
| O02-3 · O02의 3번 | **공석**. 같은 고정 후보틀의 세 번째 예약 자리. | 옛 BlackBody 내부 시험·NumPy AUC를 SciPy 원 안내로 승격하지 않음. | 적분값·인자 허용·모형 적합은 별개 관측. | 보조 시험과 다른 namespace를 확인. O-S09–17. | 해당 원 지시가 없어 A/B 적용 불가. |

## 표2. 실제 후속판과 봉인한 두 수선안

| 레코드ID | 실제 후속판·diff URL | 관측된 수정·유지 | A의 수선 | B의 수선 | 독립 판단 근거·분모 | 불일치·미확인 |
|---|---|---|---|---|---|---|
| G04-1 | 첫 1.0.0·최신 1.2.0. [PUBLISHER-GEO-3391](https://github.com/geopandas/geopandas/commit/6286f13f8de8748edfa1ed9bc7deb4d05b83a300) | 첫 판의 네 행은 동일. 최신판은 메서드 참조에 `geopandas.`를 붙임. 공간 왕복 목적은 유지. | **보류**. 동일한 옛 GDAL 이름/주소와 공식 단일 수신 대상이 없음. | **유지**. 0.14.4의 WKB 지원 범위를 보존. | 실제 문서 편집 1행. 심벌·기본값 유지의 정적 지지 1행. **A/B 정오 비교 분모 0**. | 문서 편집은 관측했지만 필수 동작 정정은 미확정. 079는 다른 caller·입력. |
| G04-2 | 첫 1.0.0·최신 1.2.0. [PUBLISHER-GEO-3348](https://github.com/geopandas/geopandas/commit/7c621fe8434d148a77738a0fc37edcd16dd0ab38) | 첫 판에서 명시적 1.0.0 설명을 일반화. `schema_version`·원 사양 저장소 링크는 유지. 최신판의 같은 일곱 행은 첫 판과 동일. | **보류**. 발행자가 이 원 레코드의 유일한 대체 위치/심벌을 지정하지 않음. | **예방적 조건 명시**. 원 인용을 남기고 0.14.4·WKB 범위를 붙임. 필수 정정이라는 판정은 하지 않음. | 실제 문서 편집 1행. 옛 WKB 제한·새 native 지원은 정적 확인. **독립적으로 확정한 필수 정정 0행**. | 발행자 이유는 오래되기 쉬운 문구 정리. GN05 실패 수선이라는 설명은 없음. B와 발행자의 편집 목적도 다름. |
| G04-3 | Arrow 16.1.0·26.0.1은 판 선택 metadata만 확인. QGIS 정식 후속 태그는 미확보. | 공석. 보조 일반 표 예제의 후속 성공을 채워 넣지 않음. | 적용 불가 | 공석 유지 | 원 안내 0, 정오 분모 0 | 후속 문단 쌍이 없는 자리를 실제 유지 사례로 세지 않음. |
| O02-1 | statsmodels 0.12.2·0.15.0 등은 보조층에서 읽음. [후속 원장](streams/oss/POSTSEAL_READOUT.md) | 핵심 자리에는 원 지시 없음. 보조 GAM/GEE 안내와 내부 이관은 따로 비교. | 적용 불가 | 공석 유지 | 원 안내 0, 정오 분모 0 | 내부 수정으로 핵심 원 안내를 사후 생성하지 않음. |
| O02-2 | Astropy 4.0.5·8.0.3은 보조층에서 읽음. | 핵심 자리에는 원 지시 없음. 첫 후속 4.0.5는 시간순 유지보수 태그이며 4.2의 직계 후속으로 간주하지 않음. | 적용 불가 | 공석 유지 | 원 안내 0, 정오 분모 0 | 태그 계보·함수 종류·삭제 사유를 구별. |
| O02-3 | scikit-learn 0.24.1·1.9.1은 보조층에서 읽음. | 핵심 자리에는 원 지시 없음. AP/AUC 구별은 유지되고 내부 namespace는 변경. | 적용 불가 | 공석 유지 | 원 안내 0, 정오 분모 0 | 옛 `numpy.trapz`를 최신 SciPy 호출로 소급 재분류하지 않음. |

## 표3. 이력 보존과 역적용

| 원 레코드ID | 유지·별칭·분리·조건 변경·보류 | 근거가 적용되는 판 | 보존할 옛 인용 | 역적용 결과 | 다음 확인 |
|---|---|---|---|---|---|
| G04-1 | 유지. `RESEARCH-G04-1`에 판·호출자 주석만 부가. | 옛 0.14.4 WKB 범위. 1.0.0·1.2.0 view는 별도 위치로 연결. | 옛 L272–275 URL·짧은 인용·원 레코드·사전 A/B 전부. | 정방향·역방향 모두 종료 0. 원 JSON bytes·옛 판정 **완전 복구**. | 정확한 옛 `test_roundtrip`/`test_write_spec_version`의 설치 환경·geometry·CRS 관측. |
| G04-2 | 예방적 조건 변경. `RESEARCH-G04-2`에 지원판/encoding 범위 부가. | 옛 0.14.4 WKB. 새 1.0.0 native 지원을 별도 연결하여 옛 제한을 새 판에 반복 적용하지 않음. | 옛 L279–285와 “files of any version”의 당시 문맥·사전 A/B. | 정방향·역방향 모두 종료 0. 원 JSON bytes·옛 판정 **완전 복구**. | 미래 native 파일을 대상으로 사용한 실제 재사용 레코드와 old/first reader의 같은 입력 비교. |
| G04-3 | 보류·공석 보존 | 해당 없음 | 검색 범위·제외 이유·빈자리 | 적용 불가. 가짜 원문이나 patch를 만들지 않음. | 직접 공간 지시를 포함할 별도 모집 기준과 원 배포 안내. |
| O02-1 | 보류·공석 보존 | 해당 없음 | 원 검색과 보조 GAM/GEE의 구별 | 적용 불가 | 간접 호출 안내의 모집 포함 조건을 먼저 고정한 새 회차. |
| O02-2 | 보류·공석 보존 | 해당 없음 | 다른 심벌·다른 입력의 제외 기록 | 적용 불가 | 원 지시와 내부 시험 사이의 정확한 호출·입력 연결. |
| O02-3 | 보류·공석 보존 | 해당 없음 | 옛 NumPy namespace와 안내 목적 | 적용 불가 | 실제 원 안내가 권한 함수·판을 확인한 뒤 후속판 가림 재설정. |

## 분모와 완료 상태

| 검산 항목 | 결과 | 산입과 해석 |
|---|---:|---|
| 등록한 핵심 자리 | **6** | G04 3 + O02 3. 원 분모 유지. |
| 실제 주제 적격 원 안내 / 공석 | **2/6 · 4/6** | 두 안내는 같은 GeoPandas I/O 가이드의 서로 다른 지시. |
| 핵심 안내의 독립 하류 저작 | **1** | 두 행을 독립 발견 두 건으로 세지 않음. |
| 핵심 안내 중 정확한 GDAL GEOARROW 호출 노출 | **0/2** | 포맷 생태계 연관성과 동일 상류 심벌 노출을 분리. O02 핵심 원 안내는 0. |
| 실제 원 안내의 옛판·첫후속·최신판 확보 | **2/2** | 여섯 자리 전체 기준으로는 2/6. |
| 실제 문서 원문 수정 | **2/2, 같은 가이드 1개** | 참조 qualification 1건, 판 문구 일반화 1건. 필요 정정의 정답으로 대용하지 않음. |
| 연구용 정·역방향 수선 가능 | **2/2, 전체 2/6** | 두 복사본만 검사. 원문 의미의 참·거짓 또는 기능 호환을 증명하지 않음. |
| 직접 읽은 원자료 행 | **124** | 접근 실패·검색 스니펫 등 시도 원장 33행은 제외. |
| 원 계보 / 코드·시험·CI·의존 단독 제외 | **39 / 35** | 같은 안내의 판, 같은 사건의 PR·이슈·릴리스는 중복 처리. |
| 더 보수적으로 후속 변경까지 원 저작에 통합 | **25** | 가까운 안내까지 추가 통합하면 **23**. 최소 20은 두 계수법에서도 충족. |
| 서로 다른 하류 가이드 저작 | **11** | 핵심 1개 + 제외/보조 저작. 이 중 O02 보조 안내는 6계보. 핵심 노출 11개라는 뜻이 아님. |
| 다른 분야 실제 사건 / 제도 | **5 / 2** | 전거 분할·병합 2, 출판 정정 3. 정책 4계보는 사건 수에서 제외. |
| 외부 옛 항목·수신 항목 양쪽 열람 | **5/5** | 역사적 전후 bytes 직접 비교는 PLOS **1/5**만. |
| 소비자 실제 설치/build·새 기능 실행 | **0 / 0** | 선언·matrix·시험 소스와 실제 설치/실행을 분리. |
| 독립 기준으로 A/B 정오 비교 가능한 핵심 행 | **0** | 불필요한 변경·놓친 변경·유효 유지 비율 모두 **0/0, 산출 불가**. |
| 실제 운영 추천 레코드 / 운영 오류율 | **0 / 산출 불가** | 0/0을 0%로 적지 않음. |

**상태는 PARTIAL이다.** 자료량·외부 사건·연구 복사본의 가역성은 확보했지만 여섯 실제 안내와 두 상류 변경에 대한 동일 대상 노출 표본은 확보하지 못했다. 그러므로 이 결과는 A/B의 우열이나 운영 오류율을 추정하지 않는다. A는 실제 두 행에서 모두 보류했고, B는 유지 1개와 예방적 범위 명시 1개를 제안했다. 이 **제안 분포**를 맞힌 비율로 표현하지 않는다. 정오가 확정되지 않았다는 사실도 “수정이 필요 없다”는 판정으로 바꾸지 않는다.

산출 근거는 [source-counts](evidence/source-counts.json), [보수적 계수 민감도](streams/review/source-count-sensitivity.json), [외부 자체 검산](streams/external/evidence/counts-and-self-check.json), [정역 검사 영수증](evidence/rollback-receipt.json), [전체 분모](evidence/denominators.json)에 있다.

## Q1. 원 독자가 요구받은 행동을 어떻게 분리했는가

G04-1은 파일을 여는 것보다 강한 공간 왕복 지시다. 그러나 geometry·CRS를 보존한다는 목적에서 모든 메타데이터 bytes나 CRS 식별자 문자열의 동일성까지 도출할 수는 없다. 실제 첫 후속판의 [GDAL 3.9 fixture 시험](https://github.com/geopandas/geopandas/blob/d8e14e1be3ecbef6f75a1142f85561ff652ed3d1/geopandas/io/tests/test_arrow.py#L930-L958)은 EPSG:4326 입력을 OGC:CRS84로 바꾼 기대값과 비교한다. 시험 소스를 직접 읽은 관측이며 실행 통과는 아니다. G083-S28은 이 추가 반례를 같은 시험 계보에 넣어 자료 수를 늘리지 않는다.

G04-2의 옛 문구 바로 앞에는 GeoParquet 1.0.0과 이전 판이라는 문맥이 있다. 그 문맥을 지운 채 “any version”만 인용하면 미래 encoding 지원 약속처럼 보이게 된다. 원 지시의 설정 축 `schema_version`, 실제 구현의 encoding 축, 독자가 설치한 reader 판을 각각 남겼다. 옛 구현의 비-WKB 거부는 079 GN05의 정상 종료와 공간 정보 소실과도 다르다. 원문과 validator를 함께 읽은 이유다. G083-S01–03.

반대로 Arrow 예제는 10행 a/b/c 표를 두 Parquet 파일로 나누어 쓰고 directory dataset으로 읽는다. 그 예제는 유효한 독자 지시지만 공간 정보 계약이 없다. AP/AUC 안내도 적분 이름이 나오는 문서이지만 독자가 구별해야 하는 것은 평균 정밀도와 선형 보간 면적이다. 이러한 보조 저작을 읽되 핵심 빈자리를 채우지 않았다. G083-S09–10, O-S14–16; [원 안내 보존 원장](records.jsonl).

## Q2. 같은 상류 대상이라는 연결의 확인 수준

이 조사에서 가장 먼저 실패한 가정은 **같은 포맷 이름·사양 저장소 링크가 같은 호출자를 뜻한다**는 것이다. GeoPandas 0.14.4의 Parquet 경로는 PyArrow를 부른다. 패키지 차원의 Fiona/GDAL 의존은 그 경로가 `GEOMETRY_ENCODING=GEOARROW`를 선택한다는 증거가 아니다. 두 핵심 행의 원 링크는 Apache Parquet·Arrow·GeoParquet 프로젝트를 가리키며, 079의 GDAL 옵션 주소를 직접 인용하지 않는다. 공급자가 같거나 연결된 Arrow 자체 가이드는 독립 소비자 공급망으로 과장하지 않았다. G083-S01–06, S09.

원문 링크와 조사 시점 목적지는 [현재 목적지 기록](streams/gis/postseal/current-link-targets.json)에 분리했다. 당시 HTTP 흐름은 복원하지 못했으므로 모든 관련 행의 상태는 **역사적 도착 미확인**이다. 이는 URL 생존율 표본을 새로 모집한 것이 아니다. 최신 목적지가 존재한다는 관측은 옛 문서 작성 시 목적지·판·의미의 증명이 아니다.

의존성 선언도 실제 설치 증거와 구별했다. 예를 들어 GeoPandas의 최소 CI 명세는 PyArrow 8.0.0을 요청하지만 그 명세를 실행한 당시 해결 결과나 문서 build lock을 확보하지 못했다. statsmodels의 SciPy >=1.2, Astropy의 >=1.1, scikit-learn의 구 최소판 역시 허용 범위다. 실제 설치판 0이라는 분모를 유지했다. G083-S04–06, O-S06, O-S11–13, O-S17.

## Q3. 079와 소비자 요구가 조인되는가

| 관측 축 | 079 또는 상류에서 확인한 것 | 이번 원 안내·시험 | 조인 판정 |
|---|---|---|---|
| G04 WKB | GN04는 GDAL 3.8/3.9의 고정 WKB 입력에서 공간 정보를 읽음. | GeoPandas 두 안내의 기본 encoding은 WKB지만 caller·원 입력이 다름. | 같은 표현 범위라는 정적 참고. 소비자 실행 성공으로 전용 불가. |
| G04 struct | GN05는 새 struct 파일을 옛 GDAL로 읽을 때 정상 종료하나 geometry·CRS가 사라짐. | GeoPandas 0.14.4 validator는 비-WKB를 거부하는 코드. | 실패 양상이 다름. GN05를 GeoPandas의 침묵 오류로 붙이지 않음. |
| G04 interleaved | GN06은 geometry·CRS 복구와 bbox 속성 증가를 함께 관측. GN07은 null/EMPTY 표현 차이. | 원 안내에 그 옵션·fixture가 없음. | 함수 성공만으로 계약 동일성을 주장하지 않음. 환경·Arrow C++ 차이도 남김. |
| O02 trapz | 079 지정 입력의 일부 alias 결과를 실행. | Astropy 시험은 100 K, 100,000점, 단위 변환, rtol=0.01. | 심벌 계보는 연결되지만 입력·소비판은 불일치. |
| O02 simps/cumtrapz | 079는 일부를 소스 별칭으로만 확인. | GAM 원 예제와 소비자 자체 시험은 spline 제약·alpha도 다름. | 실행된 다른 함수·다른 시험의 결과를 이 행에 옮기지 않음. |

인수 원행과 실행·정적 수준은 [dependency-observations.json](streams/root/dependency-observations.json), 상류 고정 소스·시험·호환 문장은 [UPSTREAM_NOTES.md](streams/root/UPSTREAM_NOTES.md), 정확한 재개 입력은 [REPRODUCE.md](REPRODUCE.md)에 연결된다. AF-RES-079의 고정 결과는 [cc527e2의 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/cc527e2c4f827afaaaa63f75c897d863c3adcc80/docs/workstreams/research/AF-RES-079/RESULT.md)에서 인수했으며 역사 실행을 반복하지 않았다.

상류만 보아도 단순 별칭 이상의 시간 조건이 있다. SciPy 1.6.0은 옛 이름을 호환 목적으로 남겼다. 하지만 [PR 18209](https://github.com/scipy/scipy/pull/18209)의 1.11 기본 알고리즘 변경은 짝수 표본의 수치가 달라질 가능성을 명시했고, [PR 20554](https://github.com/scipy/scipy/pull/20554)와 1.14 기록은 옛 이름·`even` 인자·일부 위치 인자 허용의 제거를 보여 준다. 1.6의 소스 별칭 관계가 모든 후속판의 수치·인자 계약 동등성을 뜻하지 않는다. UP-S160REL, UP-S111REL, UP-S114REL, UP-PR18209, UP-PR20554.

## Q4. 실제 발행자의 수정과 수정 이유

GeoPandas 두 행은 모두 실제 원문 편집을 겪었다. G04-1의 최신 qualification 변경과 G04-2의 첫 후속판 일반화를 각각 PUBLISHER-GEO-3391·3348로 기록했다. [PR 3348](https://github.com/geopandas/geopandas/pull/3348)의 당사자 이유는 시간이 지나 낡는 문구를 줄이려는 것이었다. [사용자 요청 3386](https://github.com/geopandas/geopandas/issues/3386)은 `use_arrow=True` 안내를 찾기 어렵다는 문제였다. 후자는 Pyogrio의 Arrow 전송과 관련되며 GeoParquet native encoding과 구별해야 한다. 단지 GDAL 3.9 뒤에 병합되었다는 이유로 GN05의 수선이라 분류하지 않았다. 병합 댓글의 되돌릴 수 있다는 말도 실제 revert 관측으로 세지 않았다. G083-P0–P3, S16–19.

O02 보조층에서는 코드 수정과 안내 목적의 유지가 함께 나타났다. [statsmodels 이관](https://github.com/statsmodels/statsmodels/commit/410bf74b3edd169e83d3a816dc9ab8a8c65fe301)은 새 import를 시도하고 옛판에서는 fallback을 쓰며, [후속 인자 수정](https://github.com/statsmodels/statsmodels/commit/defa30ace744de5c9248975643b3e3667c30cf4b)은 `x=x`를 명시한다. 그러나 첫 후속판의 GAM/GEE 가이드 파일은 옛판과 같고 최신 주요 예제도 유지된다. GEE의 원 지시는 `fit`/`summary`이며 `qic()` 적분을 요구하지 않는다. 최신 GAM 내부 docstring에 남은 옛 `simps` 표기도 따로 적었다. 코드가 이관됐다고 모든 설명까지 정정됐다고 할 수 없다. O-P01–08, O-E01–04.

시간적 반례도 찾았다. Astropy 옛 trapz 시험의 삭제는 [PR 10972](https://github.com/astropy/astropy/pull/10972)에서 deprecated blackbody 모듈 제거로 결정됐고, 병합일은 **2020-11-02**, SciPy 1.6 발행 전이다. 최신 경로의 404만 보고 이관 때문에 삭제했다고 판단하지 않았다. scikit-learn의 [PR 27140](https://github.com/scikit-learn/scikit-learn/pull/27140)은 옛 NumPy backend에서 SciPy로 옮긴 별도 소비자 변경이다. PR 본문의 `interpolate` 오타보다 실제 diff의 `integrate`를 우선해 namespace를 기록했다. O-E05–07, O-PR-10972, O-PR-27140. 상세 전후 문단·실제 diff·릴리스는 [O02 후속 보고서](streams/oss/POSTSEAL_READOUT.md)에 있다.

## Q5. 봉인과 사후 평가가 허용하는 결론

프로토콜을 `7b108414`에서, 옛 지시·두 제안·원 분모를 `35d7e180`에서 게시했다. [preseal.json](evidence/preseal.json)의 네 파일 해시는 그대로 유지했다. 첫 소비자 후속 본문 취득은 GIS 13:35:21 UTC, O02 13:35:42 UTC로 원격 봉인 뒤다. 태그의 날짜·SHA metadata 열람은 그보다 먼저 수행한 판 선택 작업이다. 각 취득·분석 시각, 일부 외부 웹 시각의 상한 정밀도, 사전 파일 byte 대조는 원장과 [감사 기록](streams/review/audit.md)에서 구별된다.

A의 정의에는 공식 단일 수신자가 없으면 보류한다는 조건이 있다. 두 핵심 행에 임의의 이름 일괄 치환을 만들어 A의 오류로 세지 않았다. Astropy 내부 시험의 무조건 새 이름 치환이 옛 SciPy >=1.1 지원 범위와 충돌하는 보조 반례는 있지만, 핵심 표본의 A 오류 수에는 넣지 않았다. B 역시 G04-2가 반드시 잘못됐다는 주장을 하지 않는다. 원 문맥과 정확한 재사용 조건이 없기 때문이다.

따라서 핵심의 불필요한 변경·놓친 변경·유효 유지·보류를 같은 성공률 표에 넣지 않는다. 확정 정오 행 0에서 앞의 세 비율은 산출 불가이고, 실제 원 안내 두 행에 대한 A 보류 2/2·B 제안 분포만 관측된다. B의 G04-1 정적 유지 지지는 독립 판정 기준의 일부를 제공하지만 모든 입력이나 실제 설치판을 통과시킨 정답으로 격상하지 않았다.

## Q6. 옛 답과 새 조건을 양방향으로 읽기

[patches/locations.json](patches/locations.json)은 각 실제 배포본의 URL#행과 세 판 문단 해시를 연구용 diff에 연결한다. `RESEARCH-G04-1`·`RESEARCH-G04-2`는 연구 복사본의 주석 추가이며, 발행자가 병합한 PUBLISHER-GEO-3391·3348과 다른 ID다. `evidence/repairs/before/`와 `after/`의 객체에는 원 지시·짧은 인용·옛 A/B가 모두 남아 있다. 새 필드에는 옛 0.14.4 view와 1.0.0·1.2.0 view를 별도로 넣었다.

실제 `patch --batch --forward -p1`로 정방향 diff를 적용해 after SHA256과 대조한 뒤, 역방향 diff를 적용해 before SHA256과 대조했다. 두 레코드 모두 종료 0, 바이트 일치, 옛 판정 불변을 확인했다. 실행 명령·cwd·시각·기대/실제 해시는 [rollback-receipt.json](evidence/rollback-receipt.json)에 있다. 옛 태그를 선택하면 원 지시와 당시 WKB 범위를, 새 태그를 선택하면 새 native 지원과 해당 문단을 찾을 수 있다. 이 view는 프로그램이 아니라 판별 가능한 연구 JSON이다. 소비자 사이트를 고치거나 실제 publisher revert를 수행한 것은 아니다.

## Q7. 그대로 둘 것, 범위를 나눌 것, 아직 정정이라 할 수 없는 것

**그대로 둘 근거가 있는 안내**는 먼저 독자 행동을 확인한다. GeoPandas의 WKB 기본 왕복, GEE의 fit/summary, Astropy의 quad/dblquad kernel 적분, scikit-learn의 AP/AUC 의미 구별은 각각 다른 계약이다. 옛 함수 이름이 사라지는 상류 사건만으로 이들 문장을 모두 바꾸는 이유가 생기지 않는다. 반대로 옛 GeoPandas의 WKB 제한을 1.0.0 이후에 반복 적용하면 이미 추가된 native 지원을 가리게 된다. G083-S20–22, O-P01–20.

**링크가 살아 있어도 판별해야 할 조건**은 남는다. GeoParquet 사양 저장소 주소가 유지되어도 reader 판·encoding·지원 schema 범위는 다를 수 있다. 079 GN05는 링크가 아니라 실제 출력 차이를 관측했다. 그러나 이번 핵심 두 안내 중 링크가 살아 있으면서 독립 기준상 반드시 고쳐야 한다고 확정된 행은 **0**이다. G04-2의 범위 주석은 예방적 제안이며, 이 빈 결과를 강한 정정 사례로 꾸미지 않는다.

**새 이름 하나로 합치면 안 되는 의미**도 실제 원문에 있다. AP와 trapezoidal AUC는 평가 정의가 다르며, GeoArrow의 struct와 interleaved는 좌표 배치와 호환 범위가 다르다. 정확한 함수·인자 허용과 어떤 입력의 적분값 보존도 별개다. 원 독자는 사용 지시와 결과를, 상류 유지관리자는 지원·제거·알고리즘 조건을, 하류 편집자는 읽기 쉬운 현재 문구와 유지 비용을 다룬다. 세 관점의 근거를 합쳐도 서로 다른 목적을 하나의 정오 척도로 만들지 않았다. UP-G38, UP-G39, UP-S160QUAD, UP-PR18209; O-S14–16; G083-P0–P3.

## Q8. 전거·출판 정정에서 옮길 수 있는 규칙

| 실제 사건 | 옛 항목과 수신 항목의 직접 확인 | 옮길 규칙 | 반대 근거·전이 한계 |
|---|---|---|---|
| EXT-L01 · LC 분할 | [Idaho ground squirrel](https://id.loc.gov/authorities/subjects/sh2005001761.madsrdf.json) → [Northern](https://id.loc.gov/authorities/subjects/sh2020006293.madsrdf.json)·[Southern](https://id.loc.gov/authorities/subjects/sh2020006294.madsrdf.json). 취소·양 수신과 [발행 목록](https://classweb.org/approved-subjects/2008.html)을 읽음. | 한 옛 이름이 복수 수신에 연결되면 원 자료의 범위를 판별하기 전 단일 치환을 보류. | receiver에 옛 이름이 공통으로 남아도 둘이 동의어는 아님. 당시 전체 export와 개별 도서 갱신은 미확인. |
| EXT-L02 · LC 병합 | [Actiniopteridaceae](https://id.loc.gov/authorities/subjects/sh85000704.madsrdf.json)·[Parkeriaceae](https://id.loc.gov/authorities/subjects/sh85098104.madsrdf.json)와 옛 Adiantaceae → [Pteridaceae](https://id.loc.gov/authorities/subjects/sh85000871.madsrdf.json). [발행 목록](https://classweb.org/approved-subjects/2402.html)도 대조. | 여러 옛 관계를 현재 수신 ID로 모으면서 이전 인용을 보존하고 현재 관계의 중복을 제거. | receiver ID가 재사용된 이름 변경도 있음. 개별 소비자에서 실제 중복 갱신한 관측은 없음. |
| EXT-P01 · Nature 형식 한정 정정 | [원 논문](https://www.nature.com/articles/s41598-018-31246-3) ↔ [정정](https://www.nature.com/articles/s41598-018-35361-z). 발행자는 PDF Fig.4만 잘렸고 HTML은 올바랐다고 명시. | 같은 DOI라도 PDF/HTML이라는 표현물에 따라 적용 대상이 다름. | 역사적 잘린 PDF bytes는 미확보. 형식별 영향은 당사자 설명 수준. |
| EXT-P02 · PLOS 정정의 재정정 | [첫 정정 e1002284](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002284)와 [재발행 공지 e1002301의 S1·S2](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002301)를 직접 대조. | 같은 DOI·인쇄 날짜여도 첨부판 해시가 다르면 받은 버전을 따로 식별. 이미 S2라면 다시 교체할 조건이 없음. | p.2 그림·해시 차이는 직접 확인. 이미 고친 소비자의 실제 중복 적용은 미관측. |
| EXT-P03 · JNCI 중복 공지 철회 | [철회된 중복 정정](https://academic.oup.com/jnci/article/114/1/e1/5943179) → [확정 정정](https://academic.oup.com/jnci/article/113/2/217/5943178)·[공식 PMC 게재본](https://pmc.ncbi.nlm.nih.gov/articles/PMC7850513/). | 정정 DOI 두 개를 내용 패치 두 번으로 보지 말고 대표 공지와 중복 관계를 보존. | 실제 중복 **공지 발행**은 확인. 소비자 DB에 중복 항목이 추가됐다는 관측은 아님. |

PLOS 두 PDF는 내부 DOI와 2017-03-24 표시가 같지만 해시는 각각 `add0a689…`와 `191de5a5…`이며 p.2 아래 패널이 달랐다. 정확한 공개 첨부 URL·전체 해시·시각 판독은 [pdf-comparison.json](streams/external/evidence/pdf-comparison.json)에 있다. 서로 다른 URL이 같은 정정 사건인 JNCI와, 같은 내부 식별자라도 다른 표현물인 PLOS를 함께 보면 이름·주소 단독 매칭의 두 방향 한계를 알 수 있다.

[LC H193](https://www.loc.gov/aba/publications/FreeSHM/H0193.pdf)는 기존 인용 보존과 유지관리 필드의 중복 방지를 구별하고, [ICMJE](https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html)는 이전판 보존과 현행 인용의 최신판 사용을 함께 요구한다. 이것은 역사적 provenance와 현재 안내를 별도 필드로 둘 근거다. 최신판만 남기거나 모든 옛 인용을 덮어써야 한다는 결론은 따르지 않는다. 현재 정책을 사건 당시 정책으로 소급하지도 않는다. X-POL-LC193/225, X-POL-ICMJE.

이식 가능한 것은 대상 동일성·적용 조건·이력·중복 방지의 규칙이다. 전거 분할은 geometry 보존을, 출판 정정은 수치 적분 동등성을 증명하지 않는다. 외부 사례로 비어 있는 소비자 실행 셀이나 운영 오류율을 채우지 않았다. 전체 양방향 기록·한계는 [CROSS_DOMAIN.md](streams/external/CROSS_DOMAIN.md)에 있다.

## 선택·검산 기록과 색인 반영 제안

GDAL 경계는 3.9.0의 2024-05-10, SciPy 경계는 1.6.0의 2020-12-31이다. Arrow 16.1의 tagger date는 경계 전이지만 정식 공개일은 2024-05-14여서 옛 판은 16.0.0으로 남겼다. Astropy 첫 후속 4.0.5는 날짜순 선택이며 별도 유지보수 계보다. 정식 태그가 부족한 QGIS에서 버전 브랜치를 임의 태그로 바꾸지 않았다. 실제 시작 통합 SHA, 선언한 검색식·누락·후계명 회고 검색은 [SCOPE.md](SCOPE.md), [protocol-deviations.md](protocol-deviations.md), 각 versions/release 파일에 있다.

검색 파일 수는 QGIS 110, GeoPandas 60, Arrow 주 검색 231와 별도 Rmd 20, statsmodels 237, Astropy 263, scikit-learn 455다. 봉인 frame의 QGIS 111 오기와 G083-S10의 자리 초과 설명 잔재는 [postseal 정정 2건](streams/gis/postseal/corrections.jsonl)으로 바로잡았고 사전 파일은 덮어쓰지 않았다. 시각의 의미도 최초 취득·직접 분석·시각 판독·상한값을 원장에 분리했다.

후속 감사에서 단수 `c_glib/example/` 경로의 README 세 개를 추가 누락 후보로 찾았다. 같은 Arrow 16.0.0 SHA에서 세 본문을 모두 직접 읽었고, C/Lua/Vala의 Arrow array file/stream 예제와 실행 준비 지시일 뿐 등록 검색식·공간 계약은 없었다. [추가 점검 영수증](streams/root/supplemental-readme-check.json)의 적격 지시는 0이다. 후속 결과를 본 뒤의 점검임을 표시하고 원 frame·A/B·공석은 유지했다. 자료 행은 121에서124로 늘지만 이 세 README를 독립 원저작 최소량에 추가 산입하지 않았다.

중앙 색인에는 **PARTIAL, 핵심 2/6·노출 0/2·독립 핵심 저작 1·정오 분모 0·자료 최소량 충족**을 함께 반영할 것을 제안한다. 형식적 자료량 충족만 보고 완료로 올리지 않는다. 운영 레코드 수선 제안은 0개다. 중앙 상태·dot-control은 수정하지 않았다. 계약 check·파일 참조·반대 근거·공석·최소 재개 입력의 검산은 [SELF_CHECK.md](SELF_CHECK.md), 최종 결과 SHA·원격 재열람·명령 종료값은 마지막 단독 커밋의 [HANDOFF.md](HANDOFF.md)에 남긴다.

## 결론을 바꿀 중요한 불일치·약점 — 정확히 3건

1. **모집한 두 안내는 한 저작이며, 같은 GDAL GEOARROW 변경에 직접 노출된 두 안내가 아니다.** O02 세 자리도 비어 있어 정책 비교의 대상 분모가 없다. **다음 조사:** 별도 회차의 포함 기준을 먼저 봉인하고, GDAL `GEOMETRY_ENCODING=GEOARROW`를 실제로 권하는 옛 배포 가이드와 간접 `BSplines` 호출 안내의 포함 여부를 고정한다. 입력은 태그·원 문단·호출 경로이며, 관측할 것은 같은 대상에 서로 다른 소비 조건을 요구하는 독립 안내 쌍이다. 발견해도 현재 공석을 사후 채우지 않는다.
2. **실제 소비자의 설치판·원 입력 실행과 정적 근거 사이가 비어 있다.** 079의 다른 입력 성공·실패나 공급자 시험 선언으로 이를 메울 수 없다. **다음 조사:** GeoPandas 두 고정 SHA의 `test_write_spec_version` 및 native/WKB 짝 fixture와 Astropy 옛 `test_blackbody_scipy`의 100 K·100,000점·rtol=0.01을 사용한다. resolved 환경·파일 해시·종료값·geometry/CRS/schema 또는 적분값·허용 인자를 함께 관측한다. 그 결과가 있어야 유지·필수 조건 변경 판정을 강화할 수 있다.
3. **예방적 명시와 실제 필요한 정정, 중복 공지와 중복 적용을 아직 동일시할 수 없다.** G04-2의 당시 문맥은 미래 encoding 보증이 아니며, 외부 전후 bytes는 1/5만 확보했다. **다음 조사:** 옛 “any version” 문구를 새 native 파일에 실제 적용한 독자 레코드, LC 역사 export, Nature 옛 PDF, JNCI 정정 전후 Box2와 소비자 적용 로그를 입력으로 확보한다. 지원 범위를 벗어난 실제 실패 또는 이미 반영된 내용의 중복 추가가 관측될 때만 필수 정정·중복 적용 판정을 바꾼다.
