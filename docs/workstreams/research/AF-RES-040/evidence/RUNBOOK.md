# AF-RES-040 — 재현 명령·입력과 미실행 범위

이 파일은 **실행 계획**이다. 아래 제품 실행·사용자 시험을 수행했다고 주장하지 않는다. 실제 수행한 것은 외부 원문의 지정 절 열람, 원장 계산, 파일 검산 및 별도 영수증에 기록된 세션 검사다. 미확인 입력을 현행 latest·임의 데이터로 대신 넣으면 원 요구 재현이 아니다. 이후 결과를 저장할 때에도 AF-RES-040 경로 안의 새 evidence/runtime 디렉터리를 사용하고 고정 풀을 덮어쓰지 않는다.

## 1. 지금 재실행 가능한 원장 검산

입력은 결과 커밋의 전체 AF-RES-040 디렉터리다. Python3.12.14에서 실행했다. 컴파일 명령은 정규화 파일을 다시 만들며, check-only와 검산 명령은 읽기 전용이다.

```sh
python -B docs/workstreams/research/AF-RES-040/evidence/compile_inputs.py
python -B docs/workstreams/research/AF-RES-040/evidence/recount.py --check-only
python -B docs/workstreams/research/AF-RES-040/evidence/verify_delivery.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-040/manifest.json --fetch
```

기대 구조는 frame60, pool48(실제39/빈9), sources176(고유64), relations120(수동85/빈35), views24, losses72다. 필수 atom25 중 풀 지원8, 완전 경로0이며 A/C8·B6 부분 atom을 보존한다. 이 숫자를 얻는 것이 원자료의 진실성이나 실제 사용자 효용 검증을 대신하지 않는다. 현재 입력에 complete path가 없으므로 미래의 새 적격 경로가 모든 필수 atom과 판·구현 조합을 만족하는지도 별도로 검사해야 한다.

## 2. GDAL 요청의 미실행 제품 재현

| 요구 | 먼저 확보할 실제 입력·환경 | 실행할 명령·관측값 | 막힌 이유·첫 행동 |
| --- | --- | --- | --- |
| G1 | [원 첨부 test_hfa_block_size.zip](https://github.com/OSGeo/gdal/files/4027388/test_hfa_block_size.zip), Windows10/Python3.7.2/GDAL3.0.1 | `python -m zipfile -l test_hfa_block_size.zip`으로 멤버부터 확인한 뒤 저자의 실제 재현 스크립트를 그 환경에서 실행한다. 64/비64·압축·NoData 경계 조건과 출력 픽셀/overview를 비교한다. | zip 멤버·실행파일명은 미열람이다. 임의 스크립트를 지어내지 않는다. 첫 행동은 zip 목록 확인, 그 다음 원 스크립트와 입력 검토다. |
| G2 | [#2169](https://github.com/OSGeo/gdal/issues/2169)의 MapInfo 파일·전체 Java 재현, native library·GDAL jar, Ubuntu16.04의2.4.0 및3.0.1 환경 | 원 재현 main과 인자 계약을 확보한 뒤 아래 Java 호출 틀을 각 환경에서 실행한다. 반환 feature 수와 null이 나온 순서를 기록한다. | 실제 입력·전체 재현 코드·main 이름이 없어 지금 실행할 완성 명령은 미확인이다. 첫 행동은 원 이슈 및 공개 첨부/연결 수정의 입력 확보다. |
| G3 | dev SHA `6d5d00851c24c25b4d814305cc5d4122ce72b4bc`와 연결된 당시 `alpine-small` 이미지의 검증된 digest·빌드 인자 | `docker run --rm "$AF040_IMAGE_DIGEST" ogrinfo --version` 및 `docker run --rm "$AF040_IMAGE_DIGEST" ogrinfo --formats`에서 FlatGeobuf 포함을 확인한다. | 현재 latest는 해당 이미지가 아니다. [고정 Dockerfile L90–119](https://github.com/OSGeo/gdal/blob/6d5d00851c24c25b4d814305cc5d4122ce72b4bc/gdal/docker/alpine-small/Dockerfile#L90-L119)과 당시 배포 digest 연결이 첫 자료다. |
| G4 | `CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5`, Windows10/GDAL3.0.3/HDF5 1.10.4 | `gdalinfo --version` 후 `gdalinfo CSKS1_DGM_B_HI_24_HH_RA_SF_20091113111415_20091113111422.h5`의 인식·크기·subdataset/product metadata·종료 코드를 기록한다. | 원 파일과 정확한 binary/dependency 환경이 없다. 첫 행동은 [#2193](https://github.com/OSGeo/gdal/issues/2193)의 공개 입력/빌드 출처 확인이다. |

Java 호출 틀은 입력이 확인된 뒤에만 쓴다. 아래 AF040 변수들은 아직 값이 없는 재개 입력이다. classpath·main 인자는 저자의 재현을 검토한 뒤 맞춰야 하며 그대로 실행 가능한 완성 재현이라고 주장하지 않는다.

```sh
java -Djava.library.path="$AF040_GDAL_NATIVE_DIR" \
  -cp "$AF040_GDAL_JAR:$AF040_REPRO_CLASSES" \
  "$AF040_REPRO_MAIN" "$AF040_MAPINFO_INPUT"
```

## 3. Sphinx 요청의 미실행 제품 재현

각 환경은 고정판·의존성·OS를 별도 식별하고, 원 요청의 source tree와 conf.py/extension/theme를 보존해야 한다. 현재 조사에서는 설치·빌드하지 않았다. 아래 `AF040_*` 경로는 원문에서 확보해야 할 입력이고 실행 결과가 아니다.

| 요구 | 입력·고정 환경 | 명령과 비교할 출력 | 첫 자료·남은 한계 |
| --- | --- | --- | --- |
| S1 | 원 RST/source tree와 conf.py, Windows, Sphinx2.2.2·2.3.0·2.3.1 각각의 Python 실행기 | 각 고정 환경에서 `python -m sphinx -b gettext -d "$AF040_DOCTREES" "$AF040_S1_SOURCE" "$AF040_POT_OUT"`. POT의 source-location 주석이 상대경로인지 비교한다. | [#7019 재현](https://github.com/sphinx-doc/sphinx/issues/7019). POSIX에서 나온 결과를 Windows 회귀 해결로 쓰지 않는다. 원문 환경을 확보한 뒤 Windows에 맞는 경로/쉘 표기로 실행한다. |
| S2 | 원 소스 핀 cad1f86·해당 extension의 이미지 버튼 생성 코드와 최소 두 이미지(개별 off/기존 전역 동작 유지) | 해당 환경에서 `python -m sphinx -b html "$AF040_S2_SOURCE" "$AF040_HTML_OUT"`. 개별 버튼의 원본 링크 유무와 다른 이미지 동작을 함께 검사한다. | [#7032](https://github.com/sphinx-doc/sphinx/issues/7032). 현행 no-scaled-link를 과거 핀에 적용할 수 있는지 먼저 확인한다. global off만으로 성공 처리하지 않는다. |
| S3 | doctree-resolved에서 파일·노드를 추가하는 원 확장 코드·샘플 이미지·원 conf.py | `python -m sphinx -b html "$AF040_S3_SOURCE" "$AF040_HTML_OUT"` 및 `python -m sphinx -b latex "$AF040_S3_SOURCE" "$AF040_LATEX_OUT"`. 두 출력의 파일 복사·URI·등록 시점을 함께 비교한다. | [#7054](https://github.com/sphinx-doc/sphinx/issues/7054). 원 사용판은 미지정이며 이후 tag 결과를 당시 해결로 옮기지 않는다. |
| S4 | 원 source tree, 함수값 html_context를 생성하는 sphinx-material 핀 aebde13, Sphinx2.2.2·2.3.1 | 같은 source·같은 outdir에서 `python -m sphinx -b html "$AF040_S4_SOURCE" "$AF040_HTML_OUT"`를 두 번 실행하고 둘째의 outdated 수를 기록한다. 두 실행 사이 source/config를 바꾸지 않는다. | [#7093](https://github.com/sphinx-doc/sphinx/issues/7093). 버전만 설치하고 테마·함수값을 누락하면 원 요구를 시험하지 못한다. |

## 4. 엄격한 표시·판독 반복조사

지금 존재하는 views.jsonl을 사람에게 보였다거나 실제 두 번 클릭을 관측하지 않았다. 다음 최소 입력은 새로 봉인한 raw href 풀, 같은 실제 문자수의 설명, 동일 원문 단위, 총 클릭의 정확한 정의다. 먼저 Sphinx [v2.3.1 contents](https://github.com/sphinx-doc/sphinx/blob/v2.3.1/doc/contents.rst)의 toctree와 GDAL 역사판 형식 목차를 후보 본문 전에 저장해 원 href·원순서·판·시각을 봉인한다. 이번 풀의 #L 링크를 raw href였던 것처럼 바꾸지 않는다.

기존 핵심 G2/S1/G4를 공통 판정 범위로 재코딩할 때는 원 요청을 먼저 읽고, 수동 쌍의 방향을 ‘같은 문서 역할 대체’ 또는 ‘모든 필수 조건 대체’ 중 하나로 고정한다. 둘을 같은 yes/no 분모에 넣지 않는다. 독립 판독·실제 사용자 시험을 하려면 그 설계와 관측 로그를 새로 남겨야 한다. 이 조사자가 만든 카드와 자체 검토만으로 독립성이 생기지 않는다.

## 5. 타 분야와 호환 구현의 첫 재개 자료

- **제한 계약의 구현 대체:** libjpeg-turbo 고정 README의 API/ABI·Mathematical Compatibility·확장 절과 IJG v6b 원판/소비자의 실제 호출·빌드 조건을 먼저 대조한다. 출력 bit 동일성·메모리 예산까지 필요한지 봉인한다. IJG 원판·소비 binary가 없으므로 실행할 호환 harness와 입력은 아직 미확인이다. 조건을 고정하지 않은 ‘무조건 대체’ 명령은 만들지 않는다.
- **MusicBrainz 전체 복원:** [edit115752742](https://musicbrainz.org/edit/115752742)와 [원 편집 토론](https://community.metabrainz.org/t/unmerging-recording/713181)에 연결된 후속 split 편집의 old/new track·ISRC·AcoustID·관계 귀속을 다시 연다. 현재는 개별 edit 접근 실패로 전체 복원을 확인하지 못했다. 편집을 직접 실행하거나 타인에게 메시지를 보내는 요청은 이 작업에 포함되지 않는다.
- **같은 녹음의 음향 동일성:** [remix MBID](https://musicbrainz.org/recording/023b1e14-0e7e-4dc1-9ab4-9ef4f0e70ce0)의 표기가 다른 동일 연결 두 track에 대해 이용 가능한 원 음원 또는 운영자의 동일성 근거를 대조한다. 카탈로그 연결 외의 실제 음원 입력은 미확인이다.

## 6. 재개 때 바꾸면 안 되는 것

이 작업의 frame·요구 봉인·pool·결과 숫자를 사후 성공 사례로 채우지 않는다. 새 근거가 고정 후보의 atom 판독을 수정한다면 원 라벨·수정 이유·판·분모 차이를 amendments에 남기고 별도 커밋한다. 새 표본과 새 UI 예산은 별도 반복조사로 기록한다. 현재 원장 검사 통과와 위 미실행 검사의 성공을 혼동하지 않는다.
