# GDAL 경로 조사·판독 원장

이 파일은 AF-RES-040의 G 경로만 설명한다. 최종 A/B/C 보기, 짝 집계, 수용 판정의 권위 파일은 상위 `RESULT.md`, `views.jsonl`, `losses.csv`, `evidence/acceptance-evidence.json`이다. 이 조사는 단일 조사자의 문서 판독이며 실제 사용자의 클릭·채택·성공은 관측하지 않았다.

## 1. 요구와 표본을 먼저 봉인한 범위

- 사전 규칙: `SCOPE.md`, 원격 규칙 커밋 `2ccbf7ab660d6e16dab637eea40867cbc4f83499`.
- 원장: OSGeo/gdal 공개 GitHub issues. 검색은 `repo:OSGeo/gdal is:issue format in:title,body created:2020-01-01..2025-12-31`, created 오름차순 최초30, 동률은 번호 오름차순이다. PR은 포함하지 않았다.
- 선정: #2150, #2169, #2172, #2193. 최초6노출 중 #2158과 #2173을 제외하고 최초 적격4를 고정했다. 정원 뒤24건은 노출만 보존하고 요구를 다시 분류하거나 더 나은 사례로 교체하지 않았다.
- 최초4 원 요청의 본문을 모두 직접 읽고 `requirements-G.json`을 공급자 문서 열람 전에 봉인했다. 봉인시각 `2026-11-22T18:35:20.654Z`, SHA256 `1b903826db971b731b4bb2281747c547eebbdd8c0ed5509371b469e9d35581e2`.
- 30행은 `frame-G.csv`와 `frame-receipt-G.json`에 보존했다. `direct_issue_body_opened`가 붙은 정원 뒤 행은 원문 요청이 반환됐다는 뜻이며, 전체를 세밀하게 판독해 적격 판단했다는 뜻이 아니다. 최소 원문수에서도 제외했다.

| 요구 | 원문·목적·고정판 | 원문만으로 남긴 불확실성 |
|---|---|---|
| G1 | [#2150](https://github.com/OSGeo/gdal/issues/2150): HFA 압축 내부 overview, 64 이외 블록, GDAL3.0.1/Python3.7.2/Windows10 | NoData 경계 제거는 보고된 회피 조건이며 허용 대안으로 승인되지 않았다. 첨부 zip·이미지 미실행. |
| G2 | [#2169](https://github.com/OSGeo/gdal/issues/2169): MapInfo→Java GetNextFeature, 주판3.0.1 | 2.4.0 성공은 비교 관측이며 롤백 승인 아님. 입력 파일과 전체 Java 재현 코드 없음. |
| G3 | [#2172](https://github.com/OSGeo/gdal/issues/2172): alpine-small에서 FlatGeoBuf 시험, dev SHA `6d5d00851c24c25b4d814305cc5d4122ce72b4bc` | 원문은 빌드 없이 해당 포맷을 쓰고 싶다는 기능·배포 가용성 요청이다. 설치 과정의 일반 실패가 아니므로 포함. 다른 이미지로의 교체 승인은 미확인. |
| G4 | [#2193](https://github.com/OSGeo/gdal/issues/2193): COSMO-SkyMED HDF5→gdalinfo, GDAL3.0.3/Windows10/HDF5 1.10.4 | 3.0.1 성공 출력은 보고자 관측이며3.0.3 해결 증거 아님. 원 데이터 없음. |

#2172의 포함 경계는 Expected behavior의 포맷 시험 목적과 `ogrinfo --formats`의 출력 부재에 있다. #2158은 NumPy extras/pip 설치 순서의 패키징 개선, #2173은 libxml2 빌드 연동 유지보수이므로 정해진 파일 입출력 소비자 행동 범위에서 제외했다. 이 구분은 공급자 문서를 본 뒤 바꾸지 않았다.

## 2. 발견 순서와 판 고정, 절차상의 약점

후보 순서는 고정판 공식 목차·드라이버/API 색인의 원 노출 순서, 요청에 명시된 다른 공급자, 관련 패키지 레지스트리, 공식 tutorial/통합 예제 순서다. 서로 같은 URL이 두 원장에서 자연스럽게 노출되면 원 풀에 두 행을 두었고 A가 제거하게 했다. 조건이 맞지 않는 이름 검색 결과를 더 좋은 후보로 교체하지 않았다.

역사판 `https://gdal.org/en/3.0.1/` 및 `/3.0.3/`는 웹 열람 도구에서 접근 불가였다. 예상한 `gdal/doc/source/index.rst`도 두 tag에서404였다. 발행자 소스 디렉터리를 열어 Doxygen `.dox`/`.html` 체계임을 확인한 뒤 tag 원문을 썼다. dev SHA는 Sphinx `doc/source` 체계를 쓴다. 각 source에는 blob SHA도 남겼다. 접근 실패8건은 G-F01..G-F08이며 최소수에 포함하지 않았다.

실제 조회 순서는 완전히 전향적 목차 순회만으로 이뤄지지 않았다. HFA 원문은 실패한 역사판 index 조회와 함께 알려진 소스 경로를 탐색해 먼저 열었고, 이후 `formats_list.html`의 HFA 행·href로 순위를 확인했다. Java 역시 현행 package index에서 Layer를 찾아 역사판 `javadoc.java`로 역추적했다. 따라서 후보 내용까지 보기 전 모든 href를 봉인한 엄격한 탐색 실험이라고 주장하지 않는다. 요구4는 그 이전에 봉인됐고, 후보의 표시 방식별 계산·분류 결과를 본 후 URL을 고르거나 갈아끼우지는 않았다. 이 탐색 경로 한계는 수용 판정에 남겨야 한다.

| 요구 | 6위 내 자연 노출 | 빈 슬롯의 이유 |
|---|---|---|
| G1 | HFA, gdaladdo, gdal_fillnodata, gdal_edit, PyPI3.0.1, Raster tutorial | 6칸 채움. NoData 단어 때문에 별도 행동2개가 먼저 잡힌 결과를 유지. |
| G2 | MapInfo main index, 같은 MapInfo driver index, Java GetNextFeature, C/C++ OGR tutorial | Java 요구에 적합한 고정판 공식 추가 패키지/예제를 선언한 경로에서 확보하지 못해5·6위 빈칸. |
| G3 | ogrinfo, 고정 Docker README, alpine-small Dockerfile | dev vector index와 전체 트리 경로에서 flatgeo 이름이 없었고 추가 적합 경로를 확보하지 못해4~6위 빈칸. 파일명 부재를 구현 부재로 단정하지 않음. |
| G4 | HDF5 driver, gdalinfo | 고정판 원장에 COSMO 전용 문서/요청 조합을 해결하는 통합 예제를 찾지 못해3~6위 빈칸. 구현 소스는 관계·반증 보조 원문으로만 사용. |

`pool-G.csv`는24슬롯, 실URL15행, 서로 다른 URL14개다. G2-1/G2-2는 완전히 같은 URL이다. version URL만 다르고 blob이 같은 utilities 문서(D02/D11)를 한 원문으로 계산하면 후보의 고유 원문은13개다. 후보15행 모두 명시한 본문/절을 실제로 열어 읽었다. 빈칸은 열람하지 않은 후보로 위장하지 않았다. 풀 봉인시각 `2026-11-22T18:41:13.890Z`, SHA256 `3ea0ba21f1b24ea1bb93f178931c596632648ad9ccd9896d895f7eeeb1bf492b`이며 URL과 순서를 유지했다.

## 3. 최종 atom 코딩과 관계 판정

`coding-G.json`에는 required_atoms, strict/relaxed eligible_paths, partial_paths, 후보별 atoms, document_group, 수작업 관계25쌍이 있다. `relation_pairs`의 방향 값은 원 목적·판에서 확인된 행동과 증거 역할을 보존하는 문서 대체 범위다. 프로그램 전체나 바이너리 호환성을 증명하는 yes/no가 아니다. 같은 URL2개만 좁은 범위에서 양방향 yes이고, Java/C++ 쌍은 wrapper 동등성을 확인하지 못해 양방향 unknown이다.

각 요구의 완전 경로는0이다. G1은 아티팩트 없는 실제 생성, G2는 조기 null 해결, G3는 당시 고정 이미지의 FlatGeoBuf 포함, G4는 해당 Windows/HDF5 조합의 원 파일 성공이 입증되지 않았다. 단지 일반 지원 문서가 존재한다는 이유로 이 필수 조건을 삭제하지 않았다. 버전 조건만 완화해도 같은 실패/포함 증거가 부족하므로 네 건 모두 complete eligible_paths_relaxed 역시0이다. 적격 없는 조건부 회수율은 ‘해당 없음’이고, 완전 답변 가능 여부의 전체 요구 분모4는 별도로 남는다.

부분 근거는 G1의 HFA 생성·압축·블록 설정, G2의 MapInfo 지원+Java 호출, G3의 --formats 호출, G4의 gdalinfo 일반 호출이다. G2는 서로 다른 원문이 결합돼야 형식과 Java 호출 두 조건을 함께 뒷받침한다. 원 보고의 실제 실패 해결은 이 쌍으로도 입증되지 않는다. `partial_paths`는 전체 대안 회수 분모에 합치면 안 된다.

대표 URL의 fragment 밖이라도 동일한 고정 원문 전체를 읽을 수 있으면 추가 클릭0으로 접근 가능하다. `document_group`은 판 고정 URL에서 fragment를 제거한 값이다. 한 Doxygen 파일에 여러 명령이 들어 있을 수 있으므로 카드의 표시 부품과 원문에서 접근 가능한 다른 절을 분리한다. 동일 원문 반복 슬롯과 동일 기능 중복 슬롯도 같은 지표가 아니다.

### 원 라벨 정정: 풀은 보존하고 최종 코딩을 권위값으로 사용

| 후보 | 원 라벨→최종 라벨 | 재확인 근거·사유 | 분모 영향 |
|---|---|---|---|
| G1-2 | `[G1.A1]`→`[]` | [gdaladdo 원문](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/apps/gdal_utilities.dox#L574-L649): 내부 예제는 GeoTIFF, .img 예제는 외부 GeoTIFF라 HFA 내부 생성 atom의 단독 증거로 과대계상했음. | 전체 풀의 G1.A1은 G1-1에 남음. 완전 적격0→0. 표시별 변화는 root 재집계 참조. |
| G4-1 | `[]`→`[G4.A2]` | [HDF5 원문](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html#L21-L44): gdalinfo와 subdataset metadata 호출, L121–123의 크기 출력을 전체 문서에서 확인. 일반 호출만 인정. | 원래도 G4-2에 A2가 있어 전체 풀 분모 불변. G4-1 대표에서도 A2가 남으므로 B의 손실 과대계상을 정정. 완전 적격0→0. |

이 수정은 `coding-G.json.correction_log`에 시각, 이전 값, 새 값, 이유, 분모를 보존했다. `pool-G.csv` 안의 잠정 atoms 필드는 봉인상태 그대로다. 분석에서는 최종 coding candidates.atoms가 우선한다. 기능/URL/요구를 사후로 바꾼 정정이 아니다.

## 4. 자기 결론에 반하는 자료를 찾은 결과

첫째, 같은 저장소의 모든 링크를 한 대표로 묶으면 언제나 필수 호출을 잃는다고 말할 수 없다. G4의 첫 HDF5 문서 자체에 gdalinfo 호출이 있어서 일반 호출 atom은 남는다. G1의 HFA 첫 문서도 압축과 블록 설정을 함께 제공한다. 한 원문의 실제 범위를 보지 않고 링크 제목만으로 손실을 세면 과장된다.

둘째, [HDF5 매뉴얼](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/frmt_hdf5.html#L176-L197)은 지리참조 목록을 OMI/Aura로 적고 Metadata 절에서 미지원을 말하지만, [고정 구현 소스](https://github.com/OSGeo/gdal/blob/v3.0.3/gdal/frmts/hdf5/hdf5imagedataset.cpp#L950-L999)는 Mission_ID와 Product_Type으로 CSK/KMPS를 처리한다. 예제의 SUBDATASET metadata, 제품 메타데이터 처리, 지리참조 지원, 특정 파일 열기 성공은 서로 다른 범위다. 문서의 빠진 이름을 즉시 구현 부재로 읽는 것도, 소스 분기를 성공 보장으로 읽는 것도 피했다.

셋째, [MapInfo 고정 문서](https://github.com/OSGeo/gdal/blob/v3.0.1/gdal/ogr/ogrsf_frmts/mitab/drv_mitab.html)는 TAB과 MIF/MID의 읽기/쓰기 지원을 같이 적지만 기존 파일 update에서는 다르게 제한한다. 같은 제품/포맷 이름에서 읽기·새 생성·갱신을 대칭 동등성으로 옮길 수 없다. 이것은 자연 후보를 바꾸지 않은 보조 방향성 사례다.

넷째, 원 요청에 명시된 [FlatGeobuf 주소](https://gdal.org/drivers/vector/flatgeobuf.html)를 풀 봉인 후 반증 검토용으로 열었다. 현재 stable 페이지는3.1 도입과3.9 layer metadata를 구분한다. [v3.1.0 원문](https://github.com/OSGeo/gdal/blob/v3.1.0/gdal/doc/source/drivers/vector/flatgeobuf.rst)도 기본 내장 read/write 드라이버라고 적지만, 앞선 dev SHA와 당시 이미지 digest를 대신하지 않는다. 이를 주 후보에 사후 삽입하지 않았다. 판 완화 실험은 같은 풀의 판 조건만 바꾸므로 이 새로운 보조 원문을 슬쩍 유입시키지 않는다.

## 5. 직접 열람 집계와 보관 조건

`sources-G.jsonl` 최종77행 중 고유 직접 원문19개를 counted=true로 계산한다: 원 소비자 요청4, 독립 공급자 문서11(보조 FlatGeobuf1 포함), 배포 레코드2, 소스 기록2. 같은 utilities blob의 다른 tag, 같은 문서의 현행 URL·별칭, 탐색용 목차/디렉터리, 정원 뒤 노출 요청, 실패 URL은 최소수에서 제외한다. 공급자 본문은 필요한 절/멤버를 직접 읽었으며 긴 파일 전체를 정독했다는 주장은 하지 않았다. 필수14키와 다시 찾을 수 있는 절·행, 확인 시각, 한계를 모두 남겼다.

되돌리기에는 원 URL 순서와 원 멤버, component/purpose/version, evidence_roles, source_id와 locator가 필요하다. 단순 URL 목록만으로는 같은 기능을 가리키는지 또는 문서와 배포 레코드가 상호보완인지 다시 알아낼 수 없다. 같은 정확 URL 중복만 제거한 경우에는 원 URL과 노출 순서로 복원이 가능하다. 이것은 저장 설계 조건이며 실제 편집자의 해제 비용을 관측한 결과가 아니다.

## 6. 실행하지 않은 검사와 재개 입력

문서 판독 외에 GDAL·Docker·Java·Windows 재현을 실행하지 않았다. 다음 명령은 재개용이며 성공 증거로 세지 않는다.

- G1 첫 자료: [원 첨부 zip](https://github.com/OSGeo/gdal/files/4027388/test_hfa_block_size.zip). `python -m zipfile -l test_hfa_block_size.zip`으로 먼저 멤버/실행 스크립트를 확인한다. 입력은 원 zip, 환경은 Windows10/Python3.7.2/GDAL3.0.1. 실제 스크립트명은 미열람이므로 임의로 만들어 쓰지 않는다.
- G2 첫 자료: [원 이슈의 재현 절](https://github.com/OSGeo/gdal/issues/2169). MapInfo 입력과 전체 Java 호출, native library 경로가 필요하나 본문에 없어 미확인이다. 먼저 그 입력을 찾거나 확보한 뒤 같은 입력으로2.4.0과3.0.1의 GetNextFeature 반환을 비교한다.
- G3 첫 자료: [고정 Dockerfile](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/alpine-small/Dockerfile#L90-L119). 당시 이미지 digest와 빌드 인자 확보가 첫 행동이다. 확보 뒤 `docker run --rm <검증된_당시_image_digest> ogrinfo --version`, `docker run --rm <검증된_당시_image_digest> ogrinfo --formats`를 실행한다. 꺾쇠 값은 미확인 입력이며 지금의 latest를 대신 쓰지 않는다.
- G4 첫 자료: 원 파일 `CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5`와 당시 Windows binary/dependency 조합. `gdalinfo --version` 후 `gdalinfo CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5`를 실행한다. 실제 파일과 GDAL3.0.3/HDF5 1.10.4 환경이 없어 여기서는 미실행이다.

## 7. 우선순위 약점 세 건

| 중요한 약점 | 영향받는 판단 | 다음 최소 조사·첫 자료 | 결과가 바뀌는 조건 |
|---|---|---|---|
| 1. 완전 경로0, 오류·배포 포함을 문서만으로 해결하지 못함 | 대안 회수율·실제 효용으로 일반화할 수 없음 | #2150 첨부 zip의 재현 입력과 수정 commit/검사 결과부터 확인 | 고정 요구를 만족하는 자연 풀 원문/조합이 실제 성공까지 입증할 때 완전 분모가 생김 |
| 2. 역사판 목차 대체와 일부 경로 역추적 | 전향적 후보 발견 절차의 재현성 | v3.0.1 배포 문서 archive의 완전한 링크 목차를 첫 자료로 독립 조사자가 재순회 | 원 순서가 달라지거나 누락된 허용 후보가 확인되면 별도 반복실험으로 비교, 이번 풀은 보존 |
| 3. 단일 조사자·문서와 구현 불일치 | 오병합/부분 조건 라벨의 외적 타당성 | HDF5 Metadata 절과 hdf5imagedataset.cpp IdentifyProductType를 독립 판독하고 원 COSMO 입력 확인 | 제품별 metadata 범위나 허용 대안에 대한 독립 근거가 달라지면 해당 atom/관계만 정정 |
