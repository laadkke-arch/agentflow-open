# 재열람·검산·미실시 항목의 재개 입력

## 이번에 수행한 것

공개 저장소의 고정판 원문·원문 위치·소비자 release/tag 날짜·원 변경 이력을 읽고, 원자료/수선안/후속판정을 연결했다. 역사 실행은 AF-RES-079의 고정 결과만 인수했다. 이 연구에서 새로 하는 실행은 CSV/JSON 참조·모집 분모·커밋 범위·연구용 정역 diff 검산이다. 이는 소비 라이브러리의 기능 시험과 다르다.

동일 조건의 소비자 기능 실행을 완료하지 못한 이유는 원 안내의 실제 설치/build 기록과 정확한 원 입력·기대값을 확보하지 못했기 때문이다. 임의의 최신 환경에서 성공한 시연은 이 공백을 메우지 않는다. 아래 소비자 자체 시험은 재구성 환경에서 수행할 수 있는 명시적 다음 입력이며, 그 환경이 과거 실제 배포 환경이라는 증명과는 별도로 기록해야 한다.

## 공통 계약

실제 시작 명령은 저장소 루트에서 다음과 같았으며, manifest의 base는 f736bd557fa4c40aecb6833165823196cfa42af2다.

```sh
python -B -m workbench.session start af-res-083 --allow docs/workstreams/research/AF-RES-083/ --output docs/workstreams/research/AF-RES-083/manifest.json --dependency work/research-af-res-079=cc527e2c4f827afaaaa63f75c897d863c3adcc80 --fetch
```

인계 대상 결과판을 checkout한 다음 다음 명령으로 범위를 확인한다. 종료0은 Git 계약·소유 경로·의존 head 확인이지 제품 동작의 인증이 아니다. 중앙 integration이나 dependency가 바뀌었다면 과거 manifest를 덮어쓰지 말고 그 차이를 먼저 읽는다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-083/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-083/audit.py
```

## 가장 작은 재개 입력

|미확인|정확한 다음 대상·입력|관측과 판단 변화|
|---|---|---|
|G04 실제 소비자 실행|GeoPandas old60c9773e44fff8a35344c2a74431e00c5546a4ee, firstd8e14e1be3ecbef6f75a1142f85561ff652ed3d1의 io/tests/test_arrow.py::test_write_spec_version. 원 test의 box(0,0,10,10),EPSG4326, 지원 schema_version 값. 먼저 해당 빌드의 Python/NumPy/PyArrow/GEOS/PROJ 정보를 확보.|읽기 성공만 보지 않고 assert_geodataframe_equal, metadata.version, CRS와 encoding을 양쪽에서 기록한다. 각 판의 정확한 의존성 freeze가 없으면 재구성 환경임을 표시한다. GN05의 GDAL struct 실패를 GeoPandas 실패로 바꾸지 않는다.|
|G04 현재 encoding 조건|동일 소비자 원 레코드를 대상으로 first1.0.0의 geometry_encoding='WKB'/'geoarrow'를 명시한 파일을 old0.14.4에서 읽는다. 대상 file bytes·SHA256·schema/version·crs를 보존한다.|원 안내가 보장한 지원범위에서 읽기/거절/geometry·CRS를 구분한다. 정확 fixture 없이 임의 최신 demo를 원안내 성공으로 세지 않는다. 이는 아직 미실시이며079역사실행반복이 아니다.|
|O02 핵심 공석|old-search.json에 남은 후보 세 저장소·고정태그·등록 검색식/경로에서 누락을 재검토한다. 먼저 이전 태그의 실제 사용 지시가 지정 함수 또는 링크를 권하는 원문 한 항목을 확보한다.|발견 전에는 여섯 자리 분모를 유지한다. 추가 검색으로 찾은 항목은 기존 모집의 누락인지 새로운 모집인지 표시하고 사전 A/B와 후속판 가림을 새 회차에서 고정한다.|
|O02 부록 exact 입력|Astropy01369fb9d230480220dd81813f3fff906f88d52d의 test_blackbody.py::test_blackbody_scipy. 온도100K, logspace(0,8,100000)Angstrom, rtol0.01. 원 의존 최소SciPy1.1과 새명칭사용구간을 구별한다.|원 tester의 exact 적분과 기대값을 실행하기 전에는079의3점trapz 결과로 통과시키지 않는다. 시험 발견을 사용자 guide 발견으로 승격하지 않는다.|
|외부 역사판|LC 두 사건의 변경 직전 authority export와 실제 배포일; Nature 원잘린PDF; JNCI 원Box2 정정 전후와 소비자 적용 이력.|현재 tombstone/정정당사자 설명→역사bytes 비교로 근거 수준을 높인다. 중복공지와 소비자 중복적용의 분모를 분리한다.|

준비된 역사 환경의 역할 이름을 `$AF083_OLD_PYTHON`, `$AF083_NEW_PYTHON`으로 사용하면 소비자 시험 명령은 다음과 같다. 변수는 실제 환경 경로로 명시적으로 설정해야 하며, 이 경로들이 이번 세션에 설치되어 있다는 뜻이 아니다. 기존 사용자 환경에 패키지를 덮어쓰지 않는다.

```sh
"$AF083_OLD_PYTHON" -m pytest geopandas/io/tests/test_arrow.py -k test_write_spec_version -vv
"$AF083_NEW_PYTHON" -m pytest geopandas/io/tests/test_arrow.py -k test_write_spec_version -vv
"$AF083_OLD_PYTHON" -m pytest astropy/modeling/tests/test_blackbody.py -k test_blackbody_scipy -vv
```

각 명령은 해당 소비 저장소의 정확 고정 checkout에서 실행한다. fixture 다운로드·optional dependency·historical binary가 없으면 종료값과 그 입력을 남기고 통과로 바꾸지 않는다. 연구용 정역 diff 검사는 별도 patches manifest와 audit.py에서 수행하므로 이 라이브러리 실행 환경을 요구하지 않는다.

## 사전 봉인 재확인

프로토콜 커밋7b108414de50ff32f28d1fa3c03ef6f2492724e6, 옛 지시/A·B 커밋35d7e18024cced8cc81f9397b65e90e0e74bb907이다. `evidence/preseal.json`의 네 파일 SHA256은 이 두 번째 원격판과 대조할 수 있다. 이후 결과는 그 원판을 고치지 않고 revisions와 연구용 view로 덧붙인다. 실제 publisher diff와 연구 diff는 각각 PUBLISHER-, RESEARCH- ID를 사용한다.
