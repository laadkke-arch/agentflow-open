# AF-RES-040 — 같은 세 자리에서 보존되는 용도와 가려지는 근거

| 요구 ID·목적·판 | 후보 URL 쌍 | 주소·프로젝트·부품 관계 | 필요한 근거 역할 | 방향별 대체 가능 | 원문 URL·절 | 판정 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G1 — HFA 압축 내부 overview·NoData 보존 / GDAL 3.0.1 | [G1-1: HFA 압축 overview 설정](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/hfa/frmt_hfa.html) ↔ [G1-2: gdaladdo overview 생성](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/apps/gdal_utilities.dox#L510-L668) | 다른 주소·동일 상류·HFA와 일반 overview 호출 | 형식별 설정·제약 + 일반 invocation | 좌→우 partial; 우→좌 no (문서 역할 치환 범위) | [G-D01](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/hfa/frmt_hfa.html) — L10–17 read/write; L37–53 Creation Options; L67–83 Configuration Options; [G-D02](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/apps/gdal_utilities.dox) — L1–44 프로그램 색인; L510–668 gdaladdo; L127–155 일반 --formats 출력 의미 | 상호 보완 증거; 일반 호출만으로 HFA 조건 치환 불가 | 공통 overview 목적만으로 역할/제약을 동일화하지 않는다. 어느 쪽도 원 오류 수정 증거가 아니다. |
| G2 — MapInfo→Java GetNextFeature / GDAL 3.0.1 | [G2-1: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) ↔ [G2-2: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) | 정확히 같은 주소·같은 원문·같은 MapInfo 부품 | 읽기 capability·constraint | 좌→우 yes; 우→좌 yes (문서 역할 치환 범위) | [G-D03](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) — L1–39 MapInfo TAB/MIF/MID; Creation Issues; dataset/layer creation options | 같은 구현·용도; A/B/C 모두 하나로 묶음 | 이 yes는 같은 문서의 대체 가능성이다. Java 입력 버그 성공을 의미하지 않는다. |
| G2 — MapInfo→Java GetNextFeature / GDAL 3.0.1 | [G2-1: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) ↔ [G2-3: Java Layer.GetNextFeature](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878) | 다른 주소·동일 상류·드라이버와 Java 호출 | 형식 capability + Java invocation | 좌→우 no; 우→좌 no (문서 역할 치환 범위) | [G-D03](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html) — L1–39 MapInfo TAB/MIF/MID; Creation Issues; dataset/layer creation options; [G-D10](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java) — Layer.GetNextFeature L6863–6878; ResetReading L6903–6907 | 상호 보완 증거; B에서 Java 근거 숨김 | 원 요구의 서로 다른 atom을 보완하며 완전 동작 성공은 입증하지 않는다. |
| G2 — MapInfo→Java GetNextFeature / GDAL 3.0.1 | [G2-3: Java Layer.GetNextFeature](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878) ↔ [G2-4: OGR feature 읽기 예제](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox) | 다른 주소·동일 상류·Java wrapper와 C/C++ API | wrapper 호출·메모리 계약·예제 | 좌→우 unknown; 우→좌 unknown (문서 역할 치환 범위) | [G-D09](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox) — Reading From OGR; L108–129 GetNextFeature/ResetReading; C/C++ 반복 예제; [G-D10](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java) — Layer.GetNextFeature L6863–6878; ResetReading L6903–6907 | 미확인; C/C++ 예제를 Java 대안으로 승인하지 않음 | 동일 하위 GDAL 구현을 활용해도 wrapper 계약·버전별 버그 동등성은 확인되지 않았다. 현재 Java 요구의 직접 대체로 승인하지 않는다. |
| G3 — alpine-small FlatGeoBuf / dev 6d5d008 | [G3-1: ogrinfo 가용 드라이버 조회](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/doc/source/programs/ogrinfo.rst) ↔ [G3-2: 공식 Docker 이미지 구성](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/README.md) | 다른 주소·동일 상류·조회 프로그램과 배포 구성 | invocation + distribution | 좌→우 no; 우→좌 no (문서 역할 치환 범위) | [G-D05](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/doc/source/programs/ogrinfo.rst) — --formats 옵션; Synopsis/Description; 명령 예제; [G-R01](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/README.md) — L24–34 Small 이미지; L36–47 Normal; L79–84 Usage | 상호 보완 증거; 조회법은 배포 포함 결과가 아님 | 조회 방법과 포함 설명은 서로 다른 근거 역할이며 결과가 실제로 나왔는지는 미확인. |
| G4 — COSMO-SkyMED HDF5→gdalinfo / GDAL 3.0.3 | [G4-1: HDF5 드라이버와 subdataset](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html) ↔ [G4-2: gdalinfo 정보 조회](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/apps/gdal_utilities.dox#L187-L301) | 다른 주소·동일 상류·HDF5와 일반 정보 조회 | 형식 범위·제약 + invocation·example | 좌→우 partial; 우→좌 no (문서 역할 치환 범위) | [G-D04](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html) — L1–30 범위; Dataset/Subdataset 예제; L176–197 Georeference/Metadata/Driver building; [G-D11](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/apps/gdal_utilities.dox) — gdalinfo L187–301 | 상호 보완 증거이지만 일반 호출 atom은 둘 다 지지 | 일반 호출 atom G4.A2는 둘 다 지원한다. HDF5/COSMO 인식 및 원 환경 성공의 완전한 대체는 미확인이다. |
| S1 — gettext 위치의 상대경로 / Sphinx 2.3.0·2.3.1 | [S1-1: MessageCatalogBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387) ↔ [S1-4: gettext_location](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L761) | 다른 주소·동일 상류·gettext builder와 location 설정 | POT capability + 위치정보 설정 | 좌→우 unknown; 우→좌 unknown (완전 원 요구 범위) | [S-DOC-BUILDERS-23](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst) — L18–113 first six class entries; L386–401 MessageCatalogBuilder; [S-DOC-CONFIG-23](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst) — L734–797 gettext_compact/uuid/location/auto_build/additional_targets; L911 html_context; L1354 html_scaled_image_link | 상호 보완 증거; 두 고정 문서가 함께 있어야 부분 atom 지지 | 같은 config 문서 안에서 다른 설정도 읽을 수 있음. 상대경로 회귀 해결은 여전히 미확인. |
| S2 — 개별 이미지 링크 해제·전역 유지 / 원문 cad1f86, semver 미지정 | [S2-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71) ↔ [S2-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L85) | 같은 고정 원문·다른 앵커·같은 상류·다른 출력 부품 | HTML 출력 배치 capability·constraint | 좌→우 unknown; 우→좌 unknown (완전 원 요구 범위) | [S-DOC-BUILDERS-92](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst) — L71–187 first six named class entries; L245+ LaTeXBuilder | 같은 프로젝트의 다른 기능; 개별 이미지 계약과는 별개 | 출력 계약 차이는 문서로 확인하지만 고정 원 요청의 완전 대체는 미확인. 같은 도메인/문서 호스팅은 동일 상류 근거가 아님. |
| S3 — 늦게 만든 이미지→HTML·LaTeX / 판 미지정 | [S3-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71) ↔ [S3-4: HTMLHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L118) | 같은 문서 호스트·다른 앵커·확인된 별도 상류 | HTML과 HTMLHelp의 출력 계약·패키지 귀속 | 좌→우 unknown; 우→좌 unknown (완전 원 요구 범위) | [S-DOC-BUILDERS-92](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst) — L71–187 first six named class entries; L245+ LaTeXBuilder; [S-META-HTMLHELP](https://pypi.org/project/sphinxcontrib-htmlhelp/) — Description; Project links / Code; Release files | 원 요구의 대체는 미확인; 도메인만으로 B 키를 정하지 않음 | 출력 계약 차이는 문서로 확인하지만 고정 원 요청의 완전 대체는 미확인. 같은 도메인/문서 호스팅은 동일 상류 근거가 아님. |
| S4 — 함수값 테마의 재빌드 캐시 / Sphinx 2.2.2·2.3.1 | [S4-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L18) ↔ [S4-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L50) | 같은 고정 원문·다른 앵커·동일 상류·다른 출력 부품 | 여러 HTML 파일과 단일 HTML의 출력 계약 | 좌→우 unknown; 우→좌 unknown (완전 원 요구 범위) | [S-DOC-BUILDERS-23](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst) — L18–113 first six class entries; L386–401 MessageCatalogBuilder | 같은 프로젝트의 다른 기능; 캐시 성공은 미확인 | 출력 계약 차이는 문서로 확인하지만 고정 원 요청의 완전 대체는 미확인. 같은 도메인/문서 호스팅은 동일 상류 근거가 아님. |

| 요구 ID | 방식 | 첫 세 자리의 실제 대표 URL | 보존한 적격 용도·판 | 숨긴 필수 용도 | 중복 슬롯 | 되살아난 대안 | 적격 분모 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | A | 1: [G1-1: HFA 압축 overview 설정](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/hfa/frmt_hfa.html); 2: [G1-2: gdaladdo overview 생성](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/apps/gdal_utilities.dox#L510-L668); 3: [G1-3: gdal_fillnodata 보간](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/python/scripts/gdal_fillnodata.dox) | G1.A1, G1.A2, G1.A3 — 부분 3/3 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 3 | NoData 경계·압축·비64 블록 동시 성공 미확인 |
| G1 | B | 1: [G1-1: HFA 압축 overview 설정](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/hfa/frmt_hfa.html); 2: 빈칸; 3: 빈칸 | G1.A1, G1.A2, G1.A3 — 부분 3/3 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 3 | NoData 경계·압축·비64 블록 동시 성공 미확인 |
| G1 | C | 1: [G1-1: HFA 압축 overview 설정](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/frmts/hfa/frmt_hfa.html); 2: [G1-2: gdaladdo overview 생성](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/apps/gdal_utilities.dox#L510-L668); 3: [G1-3: gdal_fillnodata 보간](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/python/scripts/gdal_fillnodata.dox) | G1.A1, G1.A2, G1.A3 — 부분 3/3 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 3 | NoData 경계·압축·비64 블록 동시 성공 미확인 |
| G2 | A | 1: [G2-1: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html); 2: [G2-3: Java Layer.GetNextFeature](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878); 3: [G2-4: OGR feature 읽기 예제](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox) | G2.A1, G2.A2 — 부분 2/2 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 2 | 해당 입력의 조기 null 해결·Java/C++ 대체 미확인 |
| G2 | B | 1: [G2-1: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html); 2: 빈칸; 3: 빈칸 | G2.A1 — 부분 1/2 | G2.A2 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 2 | 해당 입력의 조기 null 해결·Java/C++ 대체 미확인 |
| G2 | C | 1: [G2-1: MapInfo TAB/MIF 드라이버](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html); 2: [G2-3: Java Layer.GetNextFeature](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878); 3: [G2-4: OGR feature 읽기 예제](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox) | G2.A1, G2.A2 — 부분 2/2 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 2 | 해당 입력의 조기 null 해결·Java/C++ 대체 미확인 |
| G3 | A | 1: [G3-1: ogrinfo 가용 드라이버 조회](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/doc/source/programs/ogrinfo.rst); 2: [G3-2: 공식 Docker 이미지 구성](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/README.md); 3: [G3-3: alpine-small 빌드 설정](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/alpine-small/Dockerfile) | G3.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | 고정 이미지 digest·FlatGeoBuf 포함·실행 출력 미확인 |
| G3 | B | 1: [G3-1: ogrinfo 가용 드라이버 조회](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/doc/source/programs/ogrinfo.rst); 2: 빈칸; 3: 빈칸 | G3.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | 고정 이미지 digest·FlatGeoBuf 포함·실행 출력 미확인 |
| G3 | C | 1: [G3-1: ogrinfo 가용 드라이버 조회](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/doc/source/programs/ogrinfo.rst); 2: [G3-2: 공식 Docker 이미지 구성](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/README.md); 3: [G3-3: alpine-small 빌드 설정](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/alpine-small/Dockerfile) | G3.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | 고정 이미지 digest·FlatGeoBuf 포함·실행 출력 미확인 |
| G4 | A | 1: [G4-1: HDF5 드라이버와 subdataset](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html); 2: [G4-2: gdalinfo 정보 조회](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/apps/gdal_utilities.dox#L187-L301); 3: 빈칸 | G4.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | COSMO 범위·요청 Windows/HDF5 조합의 성공 미확인 |
| G4 | B | 1: [G4-1: HDF5 드라이버와 subdataset](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html); 2: 빈칸; 3: 빈칸 | G4.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | COSMO 범위·요청 Windows/HDF5 조합의 성공 미확인 |
| G4 | C | 1: [G4-1: HDF5 드라이버와 subdataset](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html); 2: [G4-2: gdalinfo 정보 조회](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/apps/gdal_utilities.dox#L187-L301); 3: 빈칸 | G4.A2 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | COSMO 범위·요청 Windows/HDF5 조합의 성공 미확인 |
| S1 | A | 1: [S1-1: MessageCatalogBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387); 2: [S1-2: gettext_compact](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L734); 3: [S1-3: gettext_uuid](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L744) | S1-A1 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 1 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | Windows 상대경로 회귀·2.3.0/2.3.1 결과 미확인 |
| S1 | B | 1: [S1-1: MessageCatalogBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387); 2: 빈칸; 3: 빈칸 | 입증된 부분 atom 없음 | S1-A1 | 기능 0; 같은 원문 0 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | Windows 상대경로 회귀·2.3.0/2.3.1 결과 미확인 |
| S1 | C | 1: [S1-1: MessageCatalogBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387); 2: [S1-2: gettext_compact](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L734); 3: [S1-3: gettext_uuid](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L744) | S1-A1 — 부분 1/1 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 1 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 1 | Windows 상대경로 회귀·2.3.0/2.3.1 결과 미확인 |
| S2 | A | 1: [S2-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S2-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L85); 3: [S2-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L103) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 원 핀의 개별 이미지 호출 계약 미입증; 전역 off는 거부됨 |
| S2 | B | 1: [S2-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S2-4: HTMLHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L118); 3: [S2-5: QtHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L131) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 원 핀의 개별 이미지 호출 계약 미입증; 전역 off는 거부됨 |
| S2 | C | 1: [S2-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S2-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L85); 3: [S2-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L103) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 원 핀의 개별 이미지 호출 계약 미입증; 전역 off는 거부됨 |
| S3 | A | 1: [S3-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S3-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L85); 3: [S3-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L103) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 늦은 이미지 등록·복사·URI 양쪽 충족 미입증 |
| S3 | B | 1: [S3-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S3-4: HTMLHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L118); 3: [S3-5: QtHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L131) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 늦은 이미지 등록·복사·URI 양쪽 충족 미입증 |
| S3 | C | 1: [S3-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71); 2: [S3-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L85); 3: [S3-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L103) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 늦은 이미지 등록·복사·URI 양쪽 충족 미입증 |
| S4 | A | 1: [S4-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L18); 2: [S4-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L32); 3: [S4-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L50) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 함수값 html_context의 두 번째 빌드 0 outdated 미입증 |
| S4 | B | 1: [S4-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L18); 2: [S4-4: HTMLHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L65); 3: [S4-5: QtHelpBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L78) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 함수값 html_context의 두 번째 빌드 0 outdated 미입증 |
| S4 | C | 1: [S4-1: StandaloneHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L18); 2: [S4-2: DirectoryHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L32); 3: [S4-3: SingleFileHTMLBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L50) | 입증된 부분 atom 없음 | 풀 안의 입증된 필수 atom 가림 없음 | 기능 0; 같은 원문 2 | 완전 적격 대안 0 | 완전 경로 0: 해당 없음; 부분 atom 0 | 함수값 html_context의 두 번째 빌드 0 outdated 미입증 |

## 판정과 표의 읽는 범위

**상태: REVIEW_READY_WITH_GAPS.** 위 두 표가 각각 필수 표 1(10개 핵심 쌍)과 필수 표 2(8×3=24개 보기)다. 원 URL·원 순서·실제 카드·숨은 멤버는 [pool.csv](pool.csv), [views.jsonl](views.jsonl), 사람이 읽을 수 있는 [카드 24개](evidence/CARDS.md)에 있다. 전체 쌍 120행은 [relations.csv](relations.csv), 기본·민감도 72행은 [losses.csv](losses.csv)다. 링크 라벨의 후보 ID를 누르면 표에 사용한 실제 원 URL로 간다.

**이 고정 풀에서는 A와 C가 같은 부분 근거를 보존했고, B는 두 요구에서 각각 하나의 부분 근거를 가렸다.** 전체 25개 필수 atom 중 원 풀에서 입증된 것은 8개다. A/C는 그 8개, B는 6개를 보존한다. 하지만 어느 요구에도 필수 조건 전부를 입증하는 완전 적격 경로가 없으므로 완전 답변은 모두 **0/8**, 조건부 완전 경로 회수는 **해당 없음(적격 요구·경로 분모 모두 0)**이다. 이를 0% 회수율, 일반적인 검색 성능, C의 사용자 효용 우위로 바꾸지 않는다. 계산 근거는 [재집계 요약](evidence/recount-summary.json)의 per_arm·paired_details와 [정규화된 수동 입력](evidence/analysis-input.json)이다.

표 2의 ‘보존’은 **요구의 일부를 입증하는 문서 근거의 접근 가능성**이다. 원 요청의 버그가 해결됐다는 뜻이 아니다. ‘가림 없음’도 풀 밖에 필요한 근거가 없다는 뜻이 아니다. 전체 풀에서도 미입증인 필수 atom 17개는 별도 `unsupported_required_atoms`에 남겼다. 기능 중복은 같은 구현·부품·용도·판·역할의 반복이고, ‘같은 원문’은 서로 다른 앵커가 같은 고정 문서를 다시 가리킨 횟수다. 두 수를 더해 낭비량으로 쓰지 않는다.

방향 판정 역시 범위를 보존한다. G 경로는 해당 문서의 행동·근거 역할 치환을, S 경로는 완전 원 요구의 대체를 판독했다. G의 `partial`은 일부 역할만 겹친다는 원 판정이며 `yes`로 승격하지 않았다. 이는 사전 코드북의 yes/no/conditional/unknown에 더해진 비균질 어휘·범위다. 따라서 **방향별 yes/no 빈도나 두 경로의 대체율을 합산하지 않는다.** 이 절차 편차와 원 규칙은 [정정 원장 M07](evidence/amendments.jsonl)에 남겼다.

## 1. 여덟 요구의 짝 비교와 실제 변화 — Q4·Q5

| 요구 | 풀에서 입증된 필수 부분 atom / 전체 필수 atom | A | B | C | A↔B·A↔C에서 실제 달라진 근거 |
| --- | --- | --- | --- | --- | --- |
| G1 | 3/4 | 3 | 3 | 3 | HFA 첫 원문에 내부 overview·압축·블록 설정이 함께 있어 B에서도 세 atom을 보존한다. |
| G2 | 2/3 | 2 | 1 | 2 | B가 Java GetNextFeature 문서를 MapInfo 대표 뒤에 숨겨 G2.A2를 잃는다. A/C는 정확 URL 중복 한 개를 없애고 Java 호출을 둘째 자리에 둔다. |
| G3 | 1/3 | 1 | 1 | 1 | ogrinfo 조회 계약은 첫 대표에 남는다. Docker 문서가 보여도 특정 배포 포함은 입증하지 못한다. |
| G4 | 1/3 | 1 | 1 | 1 | HDF5 첫 원문에도 gdalinfo·크기·subdataset metadata 예제가 있어 일반 호출 G4.A2는 보존된다. |
| S1 | 1/3 | 1 | 0 | 1 | POT builder와 위치 설정의 두 문서가 필요하다. B는 config 문서를 숨긴다. A/C의 config 다른 앵커를 열어도 location 절에 접근 가능하다. |
| S2 | 0/3 | 0 | 0 | 0 | B의 셋째 전후 새 도움말 빌더 카드는 개별 이미지 계약을 입증하지 않는다. |
| S3 | 0/3 | 0 | 0 | 0 | HTML/LaTeX를 소개하는 전체 builders 원문도 늦게 만든 이미지의 등록·복사·URI를 충족하지 않는다. |
| S4 | 0/3 | 0 | 0 | 0 | 일반 HTML 출력 설명은 함수값 테마의 캐시 성공 증거가 아니다. |

각 숫자는 서로 다른 요구의 부분 atom을 세는 설명적 합계이며 동일 난이도 가중 점수나 사용자 효용 단위가 아니다. G1은 네 atom, 나머지는 세 atom이다. [입력의 required_atoms·partial_paths·atom_support_sets](evidence/analysis-input.json)와 [G 원 판독](evidence/gdal/coding-G.json), [S 원 판독](evidence/sphinx/coding-S.json)을 연결해 재확인할 수 있다.

| 같은 8건의 짝 | 양쪽이 보존한 부분 atom | 왼쪽만 | 오른쪽만 | 양쪽 모두 가린 풀 내 atom | 요구별 더 많이/동률 | 완전 답변 양쪽 성공 / 양쪽 미성공 |
| --- | --- | --- | --- | --- | --- | --- |
| A 대 B | 6/8 | A만 2/8 | B만 0/8 | 0/8 | A 2건, 동률 6건 | 0/8 / 8/8 |
| A 대 C | 8/8 | A만 0/8 | C만 0/8 | 0/8 | 동률 8건, 실제 atom 집합도 동일 | 0/8 / 8/8 |
| B 대 C | 6/8 | B만 0/8 | C만 2/8 | 0/8 | C 2건, 동률 6건 | 0/8 / 8/8 |

| 지표와 분모 | A | B | C |
| --- | --- | --- | --- |
| 완전 답변 / 전체 요구 | 0/8 | 0/8 | 0/8 |
| 부분 근거가 하나 이상 남은 요구 / 전체 요구 | 5/8 | 4/8 | 5/8 |
| 필요한 atom을 하나도 입증하지 못한 요구 / 전체 요구 | 3/8 | 4/8 | 3/8 |
| 조건부 완전 대안 회수 / 풀에 적격 경로가 있는 요구 | 해당 없음 / 0 | 해당 없음 / 0 | 해당 없음 / 0 |
| 보존한 부분 atom / 풀에서 입증된 부분 atom | 8/8 | 6/8 | 8/8 |
| 필수 부분 atom의 병합 가림 / 풀에서 입증된 부분 atom | 0/8 | 2/8 | 0/8 |
| 기능·용도·판·역할이 같은 반복 표시 슬롯 | 0 | 0 | 0 |
| 같은 고정 원문을 다시 가리키는 표시 슬롯 | 7 | 6 | 7 |
| 서로 다른 의미 signature를 합친 후보 쌍 | 0 | 48 | 0 |
| 보존한 여러 원문 보완 근거 묶음 / 전체 2묶음 | 2/2 | 0/2 | 2/2 |
| A 대비 되살아난 완전 적격 대안 | 0 | 0 | 0 |

48개 이질 병합 쌍은 기계적 구조 지표다. 실제 필수 atom 손실이 없는 쌍과 화면 밖 그룹도 포함하므로 **48건의 해로운 오병합**이라고 부를 수 없다. 요구 손실이 확인된 것은 G2·S1의 2건/8건, 부분 atom 2개/8개다. 보완 근거 2묶음도 G2의 형식+Java 부분 경로, S1의 POT+위치 부분 atom으로서 완전 대안 두 개가 아니다. [losses.csv](losses.csv)의 `heterogeneous_merged_pairs`, `merge_hidden_required_atoms`, `complementary_sets_n`을 서로 구분한다.

### 가려진 근거와 가려지지 않은 반례

**G2는 같은 프로젝트의 문서 역할을 하나로 덮으면 손실이 생기는 관측이다.** [MapInfo 고정 문서](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html)의 읽기 기능과 [Java GetNextFeature](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/swig/java/javadoc.java#L6863-L6878)의 호출·null·GC 계약은 서로를 대체하지 않는다. 정확 URL 중복 제거로 셋째 자리에 들어온 [C/C++ 예제](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogr_apitut.dox#L108-L129)는 새로운 참고 문서지만 Java의 조기 null 문제를 해결한 별도 적격 구현은 아니다. 2.4.0으로 롤백해도 된다는 승인도 [원 요청 #2169](https://github.com/OSGeo/gdal/issues/2169)에서 확인되지 않았다.

**S1은 두 원문이 합쳐져야 하나의 부분 주장을 지지한다.** [MessageCatalogBuilder](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/builders/index.rst#L387)와 [gettext_location](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/usage/configuration.rst#L761)을 함께 읽으면 POT와 위치 출력의 계약을 알 수 있다. A/C의 둘째·셋째 카드는 다른 config 설정 앵커지만 같은 config 원문이므로 location 절에 접근할 수 있다. 이를 첫 앵커에 없다는 이유로 가렸다고 세지 않았다. 그러나 그 문서도 [Windows 상대경로 회귀 요청 #7019](https://github.com/sphinx-doc/sphinx/issues/7019)의 해결을 입증하지는 않는다.

**G4는 “다른 부품이 숨었으니 필요한 근거도 사라졌다”라는 첫 추론을 뒤집는다.** [HDF5 v3.0.3 원문](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html) L21–44·L121–123에는 gdalinfo와 크기·subdataset metadata 예제가 있다. 그래서 [일반 gdalinfo 문서](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/apps/gdal_utilities.dox#L187-L301)가 B에서 숨더라도 일반 호출 atom은 남는다. Metadata 절 L189의 제한은 COSMO 제품 메타데이터 전체와 별도로 읽어야 한다. [원 요청 #2193](https://github.com/OSGeo/gdal/issues/2193)의 특정 환경 성공은 여전히 미확인이다. G4-1 지원 atom을 빈 집합에서 G4.A2로 정정한 이유와 원 기록은 [G coding correction_log](evidence/gdal/coding-G.json)에 있다.

**과도하게 나눈 표시의 비용도 확인했지만 효용 손실로 확정하지 않았다.** S2/S3/S4의 A/C 첫 세 링크는 같은 builders 문서의 다른 출력 부품이다. 다른 호출·출력 계약이므로 기능 중복 0이지만, 같은 원문을 세 번 가리켜 각 보기에서 원문 반복 슬롯 2개가 생긴다. B도 같은 문서에 기술된 별도 상류 도움말 확장 두 개를 대표로 보이므로 각 2개 반복이다. 어느 경우도 이번 정확한 이미지·캐시 요구를 해결하지 못한다. 원문 수 기준 낭비와 목적별 정보 가치가 같지 않다는 음성 관측이다. [S 고정 빌더 문서](https://github.com/sphinx-doc/sphinx/blob/v9.2.0/doc/usage/builders/index.rst#L71-L187), [S 판독](evidence/sphinx/NOTES.md).

## 2. 누구의 어떤 선택을 고정했는가 — Q1

소비자 요청 본문을 먼저 읽고 공급자 자료를 읽기 전에 경로별 네 요구를 봉인했다. 두 원장·검색어·2020–2025 기간·생성시각/번호 오름차순·최초30·프로젝트별4 상한·대체 원장은 [SCOPE §1](SCOPE.md)에 사전 등록했다. 원격 사전 등록 커밋은 `2ccbf7ab660d6e16dab637eea40867cbc4f83499`, 요구·풀 고정 커밋은 `b406236564be8dc6435912912ba67e5d16c98102`다. 대체 원장은 사용하지 않았다. [frame.csv](frame.csv)는 60노출을 보존한다. 정원 후 노출은 정독·분류한 소비자 원문 수에 더하지 않았다.

| 요구·원 요청 | 최초 행동·방향 | 원문 판·조건 | 허용 대안과 제외 경계 |
| --- | --- | --- | --- |
| G1 [#2150](https://github.com/OSGeo/gdal/issues/2150) | HFA .img→압축 내부 overview, NoData 경계 보존 | GDAL3.0.1·Python3.7.2·Windows10, 블록64 이외 | NoData 경계 제거는 보고된 회피 조건이지 허용된 대안이 아님. |
| G2 [#2169](https://github.com/OSGeo/gdal/issues/2169) | MapInfo→Java feature 순회, 조기 null 방지 | 주판3.0.1, 비교2.4.0, 추가 실패3.0.0·3.0.2 | C++ 전환·구판 롤백 승인은 미확인. |
| G3 [#2172](https://github.com/OSGeo/gdal/issues/2172) | 빌드 없이 alpine-small에서 FlatGeoBuf 시험 | 3.1.0dev `6d5d00851c24c25b4d814305cc5d4122ce72b4bc` | 해당 배포의 포맷 포함 요청이므로 일반 설치 실패와 구별해 포함. 다른 이미지 교체 승인은 미확인. |
| G4 [#2193](https://github.com/OSGeo/gdal/issues/2193) | COSMO-SkyMED HDF5→인식·크기·metadata 조회 | GDAL3.0.3·Windows10·HDF5 1.10.4, 비교3.0.1 | 구판 성공은 보고자 관측이며 현재판 해결이 아님. |
| S1 [#7019](https://github.com/sphinx-doc/sphinx/issues/7019) | RST→POT/PO 위치 주석에 상대경로 유지 | Windows·Sphinx2.3.0/2.3.1, 비교2.2.2 | 위치정보를 꺼 버리는 것은 같은 요구가 아님. |
| S2 [#7032](https://github.com/sphinx-doc/sphinx/issues/7032) | 개별 이미지 버튼의 자동 원본 링크만 해제 | semver 미지정, 원문 소스 핀 `cad1f86dd895836e36e6a57407a5d82c990dfaa8` | 소비자가 전역 off를 명시적으로 거부. semver 미지정을 판 제약 없음으로 해석하지 않음. |
| S3 [#7054](https://github.com/sphinx-doc/sphinx/issues/7054) | doctree-resolved 이후 이미지→HTML와 LaTeX 모두의 파일·URI | 판 미지정 | 한 빌더에서만 성공하는 경우는 전체 요구 미충족. |
| S4 [#7093](https://github.com/sphinx-doc/sphinx/issues/7093) | 같은 소스의 둘째 HTML 빌드→0 outdated | Sphinx2.2.2/2.3.1, 테마 핀 `aebde13c30dd4bc63159482d5b6a87fc3f211556` | 일반 HTML 출력이나 함수값 제거를 승인된 해결로 바꾸지 않음. |

G는 최초6노출 중 [#2158](https://github.com/OSGeo/gdal/issues/2158)의 NumPy 패키징과 [#2173](https://github.com/OSGeo/gdal/issues/2173)의 libxml2 연동을 제외하고 최초 적격4를 택했다. S는 최초4가 적격이었다. 이번 표본은 모두 contract_required 8건이며 name_only는 0건이다. 따라서 ‘이름만 필요한 소비자에게 B가 충분한가’는 주 표본의 실증 결과가 아니다. [G 요구 봉인](evidence/gdal/requirements-G.json), [S 요구 봉인](evidence/sphinx/requirements-S.json), [pool-freeze.json](evidence/pool-freeze.json)에 원 해시와 시각을 남겼다.

## 3. 후보 풀과 근거 원장의 범위 — Q2·Q3

공식 버전 목차·패키지 설명·공식 예제 순서를 선언하고 6칸씩 고정했다. 48칸 중 실제 링크39, 빈칸9다. 중복을 포함한 후보 행과 고유 URL32개, 판별 접근 키로서 고정 문서17개(고유 원문15개), 전체 조사 고유 원문64개를 서로 다른 수로 보고한다. G2의 MapInfo 동일 URL이 두 원장에서 노출된 한 중복은 그대로 두고 A에서 제거했다. G2의 빈칸2, G3의 빈칸3, G4의 빈칸4를 이후 반례나 더 좋은 후보로 채우지 않았다. [pool.csv](pool.csv), [source-counts.json](evidence/source-counts.json).

| 고유 직접 원문 범주 | 직접 확인·중복 제거 수 | 요구 최소수 | 산입 경계 |
| --- | --- | --- | --- |
| 최초 소비자 원 요청 | 8 | 8 | 선택8의 본문. 정원 뒤 제목·노출은 제외. |
| 공급자 부품·호출·판 공식 문서 | 22 | 8 | 관련 절 직접 판독. 같은 문서의 별칭·다른 페이지 형식·보수적 판 중복은 제외. |
| 배포·소스·동일성·비호환 기록 | 18 | 4 | 공급자 문서 범주와 중복 산입하지 않음. |
| 도서관 운영 원문·구체 레코드 | 5 | 2 | IFLA·LoC 가이드3, 실제 기관 레코드2. |
| 음악 운영 원문·구체 레코드 | 11 | 2 | 가이드5, 레코드4, 실제 편집자 토론2. |
| 합계 | 64 | 24 | 전체 원장176행 중112행은 중복·검색·노출·접근 실패·범위 밖으로 제외. |

원문 수 정정 M08에서는 현행 gdaladdo/gdal_translate를 역사판 통합 utilities.dox의 후속 표현으로 보수적으로 중복 제외해 66→64개로 바꿨다. 원 관측과 종전 산입값은 보존했고 주 분석 결과는 변하지 않았다.

모든 39개 비어 있지 않은 후보를 직접 열람했고, 각 후보의 확인 범위와 문서 위치를 남겼다. 이는 긴 소스 파일의 모든 줄을 정독했다는 뜻이 아니다. `sources.jsonl`의 14개 필수 키, `locator`와 `limitation`이 해당 주장에 사용한 범위를 한정한다. 가령 Java 12,094행 파일에서는 GetNextFeature·ResetReading 멤버를, GDAL utilities에서는 해당 명령 절을 읽었다. 기준판 blob·source ID·접근 실패 주소와 대체 경로도 원 관측자 원장에 있다. [G notes](evidence/gdal/NOTES-G.md), [S notes](evidence/sphinx/NOTES.md), [crossfield access log](evidence/crossfield/access-log.jsonl).

**엄격한 자연 링크 실험으로 충족하지 못한 부분이 있다.** S 후보는 공식 소스의 명명 항목을 발견한 뒤 연구자가 만든 `#L` 링크다. 원 HTML href를 그대로 취득한 것은 아니다. S1의 builders→configuration 순서도 세부 seed 순회까지 사전에 등록되지 않았으며 실제 [v2.3.1 doc/contents.rst](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst)의 순서와 다르다. G의 HFA는 실패한 역사판 색인 탐색 중 원문을 먼저 열고 나중에 목차 href를 확인했고, Java는 현행 목차에서 과거판으로 역추적했다. 요구 봉인과 이후 3방식의 입력 동일성은 유지했지만, **후보 내용 노출 전의 완전한 자연 href 순회**는 미충족으로 처리했다. [method-clarifications.md](evidence/method-clarifications.md), [S receipts](evidence/sphinx/receipts-S.json).

같은 한 문서 호스트를 공유해도 상류가 같은 것은 아니다. Sphinx의 HTML/dirhtml/singlehtml은 core, htmlhelp/qthelp/applehelp는 각각 패키지 Code 링크로 확인한 별도 상류다. 그래서 B는 S2/S3/S4에서 첫 대표1·4·5를 보인다. [htmlhelp](https://pypi.org/project/sphinxcontrib-htmlhelp/), [qthelp](https://pypi.org/project/sphinxcontrib-qthelp/), [applehelp](https://pypi.org/project/sphinxcontrib-applehelp/)의 Project links/Code를 대조했다. 현재 패키지 metadata는 과거 소비자의 설치 버전이나 실행 성공을 보증하지 않는다.

## 4. 표시 예산과 한 번에 하나씩 바꾼 민감도 — Q4·Q7

A는 원 URL 완전 일치, B는 확인된 상류, C는 확인된 구현·부품·용도·판·근거 역할 집합·범위로 묶는다. 원문 URL은 보존하며 fragment를 임의 제거하지 않는다. 상류 불명·동일성 미확인은 기본 singleton이다. 모든 그룹 대표와 순서는 최초 출현이며 적격 문서를 골라 대표로 바꾸지 않았다. 각 보기는 빈칸을 포함해3행, 행당 원문 링크1개, 추가 클릭0이다. **설명은 동일한 80자 상한과 동일 후보 문구를 보존했으나 서로 다른 대표의 실제 글자수를 같게 만들지 않았다.** 따라서 사용자의 ‘같은 설명 길이’를 문자수 완전 일치로 해석한 조건은 미충족이다. 실제 길이는 `views.jsonl`과 [카드](evidence/CARDS.md)에 있다.

대표 링크의 fragment는 위치 안내이지 문서의 다른 절에 대한 접근 제한이 아니다. 기본 판독은 열린 **고정 문서 전체에서 이미 확인한 관련 절**에 접근 가능하다고 본다. 검색·스크롤 비용이나 사용자가 그 절을 발견했는지는 측정하지 않았다. 이 경계가 없으면 S1 config의 숨김과 G4 일반 호출 손실을 과대 계산한다. 반대로 다른 문서의 숨은 형제 내용은 기본 화면에 보태지 않는다.

U는 같은 확인 상류 안에서 미확인 후보의 기록된 긍정 속성이 모두 같은 경우에만 합치도록 바꾼다. Vg는 묶음 key에서 판만 제거하고, Vr는 적격 판 조건만 완화하며 묶음 key를 유지한다. K는 표시된 각 그룹의 형제 목록을 펼친 뒤 모든 멤버 원문까지 읽는 **상한**이다. 처음 코딩의 U가 목적/역할까지 버렸던 오류, V가 묶음/적격을 동시에 바꿨던 오류는 최초 최종집계 전에 고쳤고 원 규칙·이유·64→72행 변화는 [M01–M06](evidence/amendments.jsonl)에 남겼다.

| 한 요소 변화 | 대상·분모 | 대표 URL 변화 | 부분 atom 변화 | 완전 적격 분모·회수 | 해석 |
| --- | --- | --- | --- | --- | --- |
| U: 미확인 합침 | 8요구, 미확인 동일성 후보0/39 | 바뀐 요구0/8 | C 8→8 | 0→0, 해당 없음 | 변화 대상 없음. 미확인 합침의 안전성 증거가 아님. |
| Vg: 묶음의 판만 제거 | 8요구, 요구 안에 복수 후보판이 있는 경우0/8 | 바뀐 요구0/8 | C 8→8 | 0→0, 해당 없음 | 판을 합칠 위험을 관측하지 못함. |
| Vr: 적격 판만 완화 | 8요구, 완전 경로0 | 바뀐 요구0/8 | C 8→8 | 0→0, 해당 없음 | 버전만 완화해도 빠진 기능·수정·성공 근거는 생기지 않음. |
| K-list: 형제 URL 목록만 추가 | A/B/C 각8요구 | 최초 대표 전부 동일 | A8, B6, C8 그대로 | 각0, 해당 없음 | 링크 목록을 봤다는 사실은 숨은 원문 내용을 읽은 증거가 아님. |
| K-source-upper-bound: 멤버 원문 전부 접근 가정 | A/B/C 각8요구 | 최초 대표 전부 동일 | B6→8: G2.A2·S1-A1 회복; A/C8 유지 | 각0, 해당 없음 | B에서 추가로11개 문서를 읽는 접근을 가정한다. 실제 두 번째 클릭 효과가 아님. |

아래 K 표는 사용자가 실제로 총 두 번만 클릭한 결과가 아니다. 첫3그룹을 유지하고 각 그룹을 펼친 뒤 멤버 원문까지 열 수 있다고 가정했을 때의 범위다. 화면 밖 네 번째 그룹은 여전히 보이지 않는다. 각 행의 상세는 `losses.csv`에서 `additional_clicks=1`과 `click_model`, `sibling_list_only_preserved_atoms`, `additional_source_documents_assumed`로 구별한다.

| 요구 | K 원문 상한의 부분 atom A/B/C | B에서 회복한 부분 근거 | 추가로 읽는다고 가정한 고정 문서 A/B/C | 완전 적격 경로 |
| --- | --- | --- | --- | --- |
| G1 | 3/3/3 | 없음 | 0/5/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| G2 | 2/2/2 | G2.A2 | 0/2/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| G3 | 1/1/1 | 없음 | 0/2/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| G4 | 1/1/1 | 없음 | 0/1/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| S1 | 1/1/1 | S1-A1 | 0/1/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| S2 | 0/0/0 | 없음 | 0/0/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| S3 | 0/0/0 | 없음 | 0/0/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |
| S4 | 0/0/0 | 없음 | 0/0/0 | A/B/C 모두 0; 조건부 회수 해당 없음 |

## 5. 다른 분야의 규칙을 옮길 때 보존할 구분 — Q6

도서관·음악의 원칙은 보조 원장으로만 비교했다. 주 표본의 후보나 분모에 추가하지 않았다. 상세 원문·관측·한계는 [CROSSFIELD.md](evidence/crossfield/CROSSFIELD.md), 구체 보조 묶음은 [stress.jsonl](evidence/crossfield/stress.jsonl)에 있다.

| 직접 관측한 운영 원문·레코드 | 제공자·소비자·편집자의 관점 | 소프트웨어 적용 추론과 깨지는 조건 |
| --- | --- | --- |
| [IFLA LRM 2017-12](https://www.ifla.org/wp-content/uploads/2019/05/assets/cataloguing/frbr-lrm/ifla-lrm-august-2017_rev201712.pdf), E3 pp.23–25·§5.2 p.87; [LoC BIBFRAME2](https://www.loc.gov/bibframe/docs/bibframe2-model.html), Work/Instance/Item | 제공자는 관계 층을 관리하고 소비자는 원하는 표현·판을 구별한다. BIBFRAME의 Work가 언어 등을 포함해 LRM과 이름이 같은 필드도 범위가 같지 않다. | project→work, version→edition의 고정 대응은 부적절하다. 소프트웨어에는 입력/출력 방향, wrapper, ABI, 빌드 설정, 호출·근거 역할을 더해야 한다. |
| [LoC 2019 운영 교재](https://www.loc.gov/catworkshop/bibframe/Training/Bf2.0/2019/bf-2019-3.html), Unit6/8; [Illinois 1813년판](https://exhibits.library.illinois.edu/s/rbml/item/1104), Description; [Yale 1813·1832년판 쌍](https://onlineexhibits.library.yale.edu/s/publication-and-prejudice/item/13314), Identifier/Source | 기존 Work·Instance 존재 여부에 따라 연결과 새 기술을 구분한다. 한 Yale URL에 두 판·발행처·식별자가 있다. | URL 하나가 판 하나가 아니다. 작품만 찾는 목적과 특정 판·소장본 목적이 다르다. 두 판의 전체 본문 동일성까지 판독한 것은 아니다. |
| [MusicBrainz Recording](https://musicbrainz.org/doc/Recording), Definition/Examples; [Beatmasters remix](https://musicbrainz.org/recording/023b1e14-0e7e-4dc1-9ab4-9ef4f0e70ce0), Appears on releases L75–93 | Beatmaster mix·Beatmasters mix 등 표기가 같은 MBID로 이어진다. 제공자는 중복 참조를 줄일 수 있지만 소비자의 발매 선택에는 발매·track 정보가 필요하다. | 같은 기능의 주소·표기 차이를 무조건 분리하면 중복 표시가 된다. 다만 관측은 카탈로그 연결이며 독립 음향 동일성 검증이 아니다. |
| [Into the Blue work](https://musicbrainz.org/work/adfdfa6c-fa04-3571-aa2c-a13a99e64e96), Recordings; [원녹음](https://musicbrainz.org/recording/9ce76fe1-769f-481a-afbb-3b9b81c6f433); [발매](https://musicbrainz.org/release/0e99c968-f511-4d74-9650-1c1a06de79b2), Tracklist L70–105 | 같은 작품의 원녹음·remix는 다른 녹음이고 한 발매에도 다른 mix가 있다. 작곡자만 원하는 소비자와 특정 mix를 원하는 소비자는 필요한 층이 다르다. | 같은 상류에서 다른 기능을 최초 대표 하나로 숨기는 상황의 유사 사례다. ‘기능적 대안’과 ‘동일 구현’ 관계를 분리해야 한다. |
| [Merge](https://musicbrainz.org/doc/Merge)·[How To Merge Recordings](https://musicbrainz.org/doc/How_To_Merge_Recordings), target/identifier/reference 설명; [오귀속 정정 사건](https://community.metabrainz.org/t/unmerging-recording/713181), posts1–4; [잘못 붙은 track 토론](https://community.metabrainz.org/t/best-way-to-handle-a-recording-that-should-be-merged-but-contains-wrong-tracks-as-well/683297), posts6–9 | 편집자는 표시명 외에 track·ISRC·AcoustID·관계 귀속을 복원해야 한다. 충돌 필드는 target 쪽으로 유지될 수 있다. | 원자료 속성을 덮는 병합과 표시만 묶는 것을 구분해야 한다. 문서팀 미검토 안내·편집자 사례 한계를 유지하며 전체 unmerge 성공률이나 비용을 추정하지 않는다. |

MusicBrainz edit115752742는 운영 검색에서 이름 교정과 종료를 확인했지만 개별 편집 원문 접근이 실패했다. 전체 분리·관계 복원 성공은 미확인이다. 실패 주소·대체 탐색·다음 확인은 `sources.jsonl` X-M12·X-F 행과 [access-log](evidence/crossfield/access-log.jsonl)에 남겼다. root의 재열람도 일부 429였으며 이를 새 직접 원문으로 세지 않았다.

## 6. 최초 결론을 깨는 소프트웨어 반례와 단순 묶음의 충분 조건 — Q7

| 보조 사례·직접 원문 위치 | 처음의 단순한 결론을 깨는 관측 | 현재 허용되는 판단·남은 미확인 |
| --- | --- | --- |
| [Cairo1.12.4 PNG Support](https://www.cairographics.org/manual-1.12.4/cairo-PNG-Support.html), Synopsis·create_from_png/write_to_png; [PDF Surfaces](https://www.cairographics.org/manual-1.12.4/cairo-PDF-Surfaces.html), Description | 한 URL에 PNG 읽기·쓰기가 있고 같은 프로젝트의 PDF 출력은 다른 행동이다. | 원문 전체가 필요한 양 방향을 함께 입증하면 한 링크로 충분할 수 있다. PDF 출력 문서를 PDF 읽기의 근거로 옮기면 틀린다. 실제 backend 포함은 미확인. |
| [libjpeg-turbo3.1.3 고정 README](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/af9c1c268520a29adf98cad5138dafe612b3d318/README.md), Using/Mathematical Compatibility/Colorspace Extensions; [공식 binary 안내](https://libjpeg-turbo.org/Documentation/OfficialBinaries), Included Features | 별도 구현이어도 공통 v6b API/ABI에 대한 호환 선언이 있다. 하지만 확장 색공간·in-memory 호출의 역방향은 달라지고 floating DCT·4:4:0 예외가 있다. | 다른 공급자라는 이유만으로 대체 불가로 분류할 수 없다. 고정 소비 계약에서 조건부 대안이며 무조건 완전 대체는 미입증. IJG v6b 원판·소비 바이너리 실행이 다음 자료다. |
| [zlib-ng2.2.4 PORTING](https://github.com/zlib-ng/zlib-ng/blob/860e4cff7917d93f54f5d7f0bc1d0e8b1a3cb988/PORTING.md), native/compat·Changes from zlib | fork 뒤 native/compat 헤더·symbol·링크 방식이 갈리고 할당 메모리·압축 스트림도 달라질 수 있다. | 동일 압축 목적만으로 정확 출력 길이·allocator 계약까지 동등하게 묶지 않는다. 현행 [zlib1.4 매뉴얼](https://zlib.net/manual.html)을 해당 fork판의 검증된 호환 상대라고 추정하지 않았다. |
| [GDAL v3.10.0 COG 등록 소스](https://github.com/OSGeo/gdal/blob/v3.10.0/frmts/gtiff/cogdriver.cpp#L1614-L1640), pfnCreateCopy; [현행 COG 문서](https://gdal.org/en/stable/drivers/raster/cog.html), Driver capabilities/Create; [GTiff](https://gdal.org/en/stable/drivers/raster/gtiff.html), capabilities | 같은 저장소여도 COG/GTiff와 Create/CreateCopy가 다르고 문서가 설명하는 판에 따라 호출 능력도 달라진다. | 현행 문서의 Create 추가판 표기를 과거판에 역전이하지 않는다. 3.13이 실제 배포됐다고 이 문서만으로 주장하지 않는다. [root stress](evidence/root/stress-R.jsonl). |
| [gdal_translate](https://gdal.org/en/stable/programs/gdal_translate.html), option synopsis; [gdaladdo](https://gdal.org/en/stable/programs/gdaladdo.html), overview options | 하나의 gdal_translate URL은 여러 변환 행동을 설명하고 gdaladdo는 overview 생성·삭제에 한정된다. | URL 수와 부품 수는 다르다. 같은 저장소 대표 하나가 충분한지는 요청과 대표 원문의 실제 범위에 달렸다. |

반례 탐색의 결과는 양쪽이다. G4·Cairo PNG처럼 한 원문이 필요한 여러 역할을 갖고 있으면 단순 URL 보존이나 B의 대표도 부분 요구를 지킬 수 있다. 반대로 G2·S1은 상류가 같아도 다른 원문에 분산된 필수 역할을 보존해야 한다. 별도 구현의 제한적 호환은 오히려 별도 대안으로 남기되 방향·조건을 붙여야 한다. **주 표본에서 C가 A보다 중복을 더 없애 적격 대안을 되살린 사례는 없었다.** 정교한 그룹 키를 택한다는 이유만으로 첫3자리 결과가 개선된다는 결론은 이번 자료가 지지하지 않는다.

## 7. 합침 해제와 보관 선택

| 보관 대안 | 충분한 조건 | 부족해지는 조건·이번 근거 |
| --- | --- | --- |
| 원 URL·원 순서 | 같은 고정 원문을 다시 확인할 수 있고 표시만 묶으며 이전 의미 판정을 그대로 재현할 필요가 없는 경우 | 한 URL의 여러 부품·판, 문서 역할, 방향 조건을 다시 추론해야 한다. Cairo PNG·Yale 한 URL 두 판이 반례다. |
| 원 member·고정 문서·구현/부품/용도/판/역할·대표 선택·숨김 이유·규칙판 | 이번처럼 표시 그룹을 해제하고 어느 문서가 어느 atom을 지지했는지 복원할 경우 | URL 목록만으로는 G2 Java와 S1 config를 숨긴 판정 이유를 재현할 수 없다. 정정 전후 기록과 근거 위치도 필요하다. |
| 위 항목과 방향·조건·필드/관계의 이전 귀속 | fork·호환 레이어·원자료 병합까지 다루는 경우 | MusicBrainz처럼 target 속성 변경·참조 이동까지 발생하면 링크 목록만으로 옛 귀속을 복구한다는 보장이 없다. 실제 복원 비용은 이번 범위 밖이다. |

24보기는 모든 그룹과 원 member ID, 잘린 그룹, 빈 슬롯을 보존한다. 이를 `analysis-input.json`·`pool.csv`·`relations.csv`와 결합하면 원6슬롯의 순서·URL·카드 문구·부품·용도·판·역할을 복원할 수 있다. S의 최초 pool 의미 필드는 빈칸이고 후속 coding에서 판독했으므로 원풀 행과 검증된 의미 행을 ID로 각각 복원한다. 둘을 처음부터 같은 문자열로 기대한 검사의 첫 실패와 수정은 M09·실패 영수증에 남겼다. 원본을 파괴하지 않는 표시 묶음이므로 이 복원은 데이터 검산으로 확인할 수 있다. 그러나 근거 원문이 바뀌거나 수동 판독을 재실시하면 같은 의미 판단이 나오는지는 별도 문제다. 새 설계의 저장 비용·유지 부담·사용자 클릭 비용은 측정하지 않았다.

## 8. 검산·재현·수용 경계

원본 요구·풀 해시와 실제 원격 커밋은 [manifest](manifest.json), [pool-freeze](evidence/pool-freeze.json), [commits](evidence/commits.jsonl)에 있다. 시작 세션 명령은 성공했고, 실제 배정 SHA는 `de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62`, 계획 SHA는 `922bf3171cab62f30469720ac80327ad3f24fbf9`로 구분했다. 고정 선행003·020은 코드북 출발점으로만 사용했고 과거 사례를 이관하지 않았다. 확인 가능한 제공 모델 표시는 GPT-6 Astra Pro이며 native web-pro 선택 화면·실제 사용자 효용·외부 독립 판독은 미확인이다.

문서·계산 검산의 재현 명령은 아래와 같다. 제품 실행을 뜻하지 않는다. 첫 실행의 관계 스키마 KeyError와 수정 후 성공, 입력/출력 해시는 [execution-log](evidence/execution-log.jsonl)에 보존했다. [내부 정적 검토](evidence/crossfield/FINAL_METHOD_REVIEW.md)는 같은 세션의 검토이며 독립 사용자 실험이 아니다. 최종 고정 SHA 재열람과 세션 check의 실제 영수증은 수용 파일과 HANDOFF에서 연결한다. 이 문서의 상태를 확인 전 성공으로 바꾸지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-040/evidence/compile_inputs.py
python -B docs/workstreams/research/AF-RES-040/evidence/recount.py --check-only
python -B docs/workstreams/research/AF-RES-040/evidence/verify_delivery.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-040/manifest.json --fetch
```

GDAL·Docker·Java·Windows·Sphinx 빌드, 음원 비교, 실제 두 클릭, 채택은 실행하지 않았다. 입력 파일·고정 이미지 digest·역사판 의존 환경·독립 소비자 판독이 필요한 부분은 [재현 대기 명령](evidence/RUNBOOK.md)에 명령과 입력, 무엇을 입증할지 기록했다. 기계적 원장 검사가 통과해도 자연 href 전향 순회, 완전 동일 설명 길이, 방향 판정 범위 통일의 미충족은 사라지지 않는다. Q1–Q7별 지지·반증·미확인은 [SELF_CHECK.md](SELF_CHECK.md), 수용 조건별 met·분자/분모·파일/행은 [acceptance-evidence.json](evidence/acceptance-evidence.json)에서 분리한다.

## 9. 중요한 불일치·약점과 다음 최소 조사

| 중요한 불일치·약점 | 영향받는 결론 | 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| W1. 완전 적격 경로0/8, 이름만 요청0/8, U 후보0/39·Vg 노출0/8인 두 프로젝트 표본 | 적격 대안 귀환·C의 A 대비 우위·미확인/판 병합 안전성은 판정할 수 없다. 부분 근거2건 손실만 관측했다. | [G2 원 요청](https://github.com/OSGeo/gdal/issues/2169) Expected behavior; [S2 원 요청](https://github.com/sphinx-doc/sphinx/issues/7032) 개별/전역 구분; [losses.csv](losses.csv) strict·eligible_paths_n; [source-counts](evidence/source-counts.json) | 먼저 이 두 원 요청과 고정 풀의 부족 atom을 재확인하고, 별도 전향 등록 원장에서 실제 대안·판 차이·미확인 후보가 자연 노출되는 새 표본을 봉인한다. 기존8건을 교체하지 않는다. | 고정 원 풀에 모든 필수 atom을 입증하는 경로가 확인되거나 새 사전 표본에서 C가 A와 다른 적격 경로를 보존하면 효과 판정 범위가 달라진다. |
| W2. 자연 href·세부 seed 순서의 완전 전향 고정 미충족, 80자 상한만 동일, K는 원문 접근 상한 | 후보 순서가 완전히 자연스럽다는 주장과 엄격히 동일한 노출/두 클릭 비용의 인과 비교를 지지하지 못한다. | [Sphinx v2.3.1 contents](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst) toctree; [S receipts](evidence/sphinx/receipts-S.json); [G notes](evidence/gdal/NOTES-G.md) §2; [views](views.jsonl) budget·description_length | 첫 자료인 contents와 GDAL formats_list의 raw href·목차 순서를 후보 본문 전에 봉인한다. 실제 같은 문자수 카드와 총 클릭 예산을 따로 사전 고정해 재구성한다. | 사전 등록된 raw href 순서와 엄격한 카드·클릭 조건에서도 G2/S1 손실이 반복되거나 반대로 사라지면 처치의 영향 판단이 바뀐다. |
| W3. 단일 내부 판독, G/S 방향 범위 비균질, 별도 구현의 무조건 대체·음향 동일성·병합 전체 복원 미확인 | 방향 대체율·실제 소비자 효용·보관만으로 오병합 복구가 충분하다는 일반 주장은 할 수 없다. | [libjpeg-turbo README](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/af9c1c268520a29adf98cad5138dafe612b3d318/README.md) compatibility; [MusicBrainz edit115752742](https://musicbrainz.org/edit/115752742) 접근 미확인; [M07](evidence/amendments.jsonl) | 공통 목적·판·판정 범위로 핵심 G2/S1/G4 쌍을 독립 재판독한다. IJG v6b 원판·소비 호출을 먼저 확보하고 edit115752742 및 뒤따른 split의 old/new 관계를 다시 연다. | 독립 판독이 핵심 atom을 바꾸거나 제한 계약에서 완전 대체가 입증되거나 원 멤버/관계의 전체 복원이 확인되면 보존·호환·복원 결론을 수정한다. |
