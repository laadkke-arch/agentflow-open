# GDAL A 네 사건: 후속 결정과 반영

단계2 최초판 동결은 `7a33c17be2d25b2c1936038205187e8108bf4482`다. 그 뒤에 투표, PR, 고정 코드와 반례를 읽었다. 네 사건 모두 추적했으며 **새 타 분야 원문이 작성자의 기존 선택을 바꾼 C3 사슬은 확인하지 못했다.** 이는 해당 역사가 존재하지 않았다는 증명이 아니다. 최초 번호 RFC가 이미 구현을 정리하는 문서인 경우가 있어, 원안 이전의 인과가 공개 기록 밖에 남을 수 있다.

## 판단과 적용 범위

| 사건 | 확인한 변화·유지 | 반영의 가장 강한 직접 근거 | 사슬의 약한 접점 |
|---|---|---|---|
| A-G01 / RFC71 | SVN/Trac에서 GitHub 소스·신규 이슈로 이동. 기존 티켓·위키·백업의 범위는 분리 | [2018-03-23 완료 공지](https://lists.osgeo.org/pipermail/gdal-dev/2018-March/048296.html): 새 이슈 경로와 기존 Trac 수정권한, PR 재기반 비용 | 비소프트웨어 제공 원문 및 저자의 유입 연결 없음 |
| A-G02 / RFC72 | pytest 포팅, 통상 단일 프로세스. CI sugar는 제외하고 ASAN은 파일별 프로세스 유지 | [합병 코드](https://github.com/OSGeo/gdal/blob/59d0840b1980d1a1a84701b6dae5fc5c78e999f5/gdal/ci/travis/gcc52_stdcpp14_sanitize/script.sh#L49-L66) | pytest는 소프트웨어 도구이며 타 분야 원리 유입과 구별해야 함 |
| A-G03 / RFC73 | CRS 권위 정의와 데이터 축 매핑 분리는 최초안과 동일. CLI WKT 기본값은 후속 조정 | [합병 매핑 코드](https://github.com/OSGeo/gdal/blob/ab9e80368ef662712c963191fd86fde2c5b75600/gdal/ogr/ogrspatialreference.cpp#L286-L394), 같은 커밋의 osr_ct.py | 원안 이전 노출·바뀐 기존 선택·특정 제공 원리 인과가 연결되지 않음 |
| A-G04 / RFC74 | 이미 진행된 Sphinx 문서 이관을 공식화하고 배포. 기존 번역은 원래 제외 | [고정 conf.py](https://github.com/OSGeo/gdal/blob/3a9f10aaca02876a01e090ef8437e513a4877fdf/gdal/doc/source/conf.py), [배포 완료](https://lists.osgeo.org/pipermail/gdal-dev/2019-May/050273.html) | 다른 소프트웨어 사이트 모방을 인쇄분야 원리로 바꾸어 부를 근거 없음 |

따라서 네 사건을 모두 실패한 설계로 해석해서도 안 된다. 전환과 반영은 관측했지만, 이번에 묻는 **타 분야 출처가 선택을 바꾼 인과**는 별도 요건이다. 최초 원안의 규범 설명, 이후의 구현, 나중의 상세 인용을 이어 붙인다고 그 요건이 자동으로 충족되지는 않는다.

## RFC73은 한 가지 결정이 아니다

축 매핑에서는 동일한 CRS의 이름과 권위를 보존한 채 데이터 저장 순서를 별도 상태로 둔다. 공식 EPSG 정의의 축 순서를 바꾸면서 같은 EPSG 코드를 남기면 CRS 정체성을 잘못 표현하게 된다. 최초 실질 v2는 이미 이 대안을 거절하고 매핑을 택했다. 합병 코드의 새 SRS 기본값은 `OAMS_AUTHORITY_COMPLIANT`이고, [시험](https://github.com/OSGeo/gdal/blob/ab9e80368ef662712c963191fd86fde2c5b75600/autotest/osr/osr_ct.py#L73-L140)은 기본 순서 `(32,-117.5)`와 전통 GIS 매핑의 `(-117.5,32)`를 같은 UTM 결과로 연결한다. 이는 선택의 반영 증거이며, 저자가 언제 그 발상을 처음 얻었는지에 대한 증거는 아니다.

반면 WKT 출력 기본값은 후속 논의에서 달라졌다. [2019-01-14](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049587.html)에 저자는 CLI를 WKT2:2015로 바꾸면 사용 영역을 보여 주어 위치를 이해하기 좋다고 제안했다. [GRASS 개발자의 권고](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049635.html)는 더 넓은 WKT2 전환을 지지했다. [2019-01-25](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049658.html)에 저자는 기존 VRT/aux.xml 호환성을 이유로 전역 API 기본 변경은 하지 않기로 했고 CLI만 WKT2로 전환한다고 분명히 밝혔다. 고정 v5와 합병 코드가 이 구분을 반영한다. 이를 “아무 선택도 변하지 않았다”로 요약하면 틀리지만, “새 타 분야 원리가 축 설계를 바꿨다”로 합치면 역시 틀리다.

[Extent 논의](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049649.html)는 유용한 오답 교정이다. 같은 BBOX라는 이름이라도 CRS의 적용 권고 범위는 수치 안정성에 따라 넘어갈 수 있으나, grid 좌표변환의 자료 영역은 엄격한 제약이다. 권한·대상 객체가 달라 같은 단어만으로 행위를 옮길 수 없다. [2019-01-28의 OGC08-015r2 인용](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049665.html)은 Geographic3D와 PostGIS geography를 혼동한 질문에 대한 설명이다. 원안 뒤의 인용이며, 새 개정판은 아직 공개 예정이라고 말한다. 2019년에 나온 표준 판을 2019-01 원안의 이미 공개된 정확 원문으로 바꾸어 넣지 않는다.

## 반증으로 범위를 고친 곳

| 넓게 읽으면 생기는 주장 | 직접 반증 | 수정된 범위 |
|---|---|---|
| pytest 포팅은 모든 환경을 단일 프로세스로 통일했다 | ASAN script는 메모리와 진단의 관련성을 위해 파일별 프로세스. PR은 xfail이 실행되어 무관 시험을 깨뜨렸다고 보고 | 환경별 예외와 실행/미실행의 차이를 보존한다 |
| RFC73 원안 뒤에는 설계 변화가 없었다 | v5와 저자의 Jan25 메일은 CLI 기본값과 API 유지의 선택을 구별 | 축 매핑 유지와 출력 기본값 조정을 별도 하위 결정으로 둔다 |
| 문서화 플랫폼을 바꾸면 모든 기존 내용과 링크가 이관됐다 | RFC74는 번역을 처음부터 제외하고 완료 메일은 대부분의 redirect와 누락 제보를 말함 | 주요 내용 배포만 확인한다 |
| GitHub 전환은 기존 협업 관계를 그대로 유지했다 | SHA 재작성 때문에 약20개 열린 PR이 닫혀 재제출이 필요했다고 완료 메일이 보고 | 소스 역사 보존과 PR 관계 보존을 분리한다 |

이 정정은 최초 C3 양성을 나중에 음성으로 바꾼 사건 수가 아니다. 이 stream에서는 C3를 먼저 부여한 사건이 없으므로 **양성 판정의 반증 뒤집힘은 0**이다. 세부 범위를 좁힌 근거는 별도 보존한다. 비슷하지만 독립 발명이라는 네 번째 설명을 적극 입증한 원문은 찾지 못했다. 인용 부재만으로 독립 발명을 확정하지 않는다.

## 경계와 원문 집계

frame은76행이다: 선택4, RFC73 제목-only 자리표시자1, 기간 전 본문 경계6, 기간 전 metadata65. 마지막65에는 RFC59의 두 파일 변형이 포함된다. 초기15개의HTTP500을 낮은번호만으로 제외하지 않았다. 단계2에 동일 URL을 한 번 재시도한 결과15개 모두200과2018이전 v1 생성시각을 확인했다. `boundary-reconciliation.json`에 이전 미확인값과 새 근거를 함께 둔다. A 표본은4→4, 기간 내 후보 상한 변화0, 남은 경계 미확인15→0이다.

`sources.jsonl`은69행이며 이 중 최소수에 세는 보수적 고유 저작은11개다: 최초 수신4, 후속 결정/반영6, 독립 비판1. 같은 RFC의 개정판, 같은 코드 합병의 여러 파일, 같은 메일 스레드의 보조 발언은 중복 계산하지 않았다. 독립 비판1은 pytest의 검증 구조에 관한 소프트웨어 내부 비판이므로 비소프트웨어 제공 원리를 확인한 숫자로 재사용하면 안 된다. 코드/시험을 읽은 것과 당시 시험을 직접 실행한 것을 구별한다.

## 실행하지 않은 검사와 재개 입력

이 stream의 필수 검사는 자료·행·카운트 대조이며 과거 GDAL 빌드의 실행은 하지 않았다. 런타임까지 재개하려면 다음 입력을 먼저 마련해야 한다.

- RFC72: GDAL 합병 `59d0840b1980d1a1a84701b6dae5fc5c78e999f5`; 그 버전의 autotest requirements와 CI script, 당시 Python/driver/ASAN 환경. 첫 자료는 고정 `gdal/ci/travis/gcc52_stdcpp14_sanitize/script.sh`다. 현재 pytest를 임의로 설치해 당시 성공을 대신하지 않는다.
- RFC73: GDAL 합병 `ab9e80368ef662712c963191fd86fde2c5b75600`; 호환 PROJ6 개발판·데이터베이스·GDAL Python 바인딩. 당시 정확한 PROJ SHA는 미확인이다. 첫 자료는 PR1185의 당시 CI dependency 설정과 공식 [병합 공지](https://lists.osgeo.org/pipermail/gdal-dev/2019-January/049681.html)다.
- RFC74: 문서 구성 `3a9f10aaca02876a01e090ef8437e513a4877fdf`; 당시 Sphinx/Breathe/LaTeX 버전과 링크 목록. 첫 자료는 고정 conf.py 및 Azure 배포 설정이다. 당시 DNS/권한 상태는 현재 빌드만으로 복원할 수 없다.

환경을 별도 격리하고 정확한 옛 의존성을 고정한 뒤, RFC73의 위도/경도 순서 사례는 다음 명령으로 좁혀 확인할 수 있다. 현재 연구 저장소에서 바로 실행하는 명령이 아니다. 입력 좌표와 기대값은 앞서 읽은 고정 시험 정의를 그대로 사용한다.

```sh
# GDAL ab9e80368ef662712c963191fd86fde2c5b75600 checkout에서,
# 호환 PROJ와 해당 GDAL Python 바인딩이 먼저 빌드·설치된 환경
cd autotest
python -m pytest osr/osr_ct.py::test_osr_ct_2 osr/osr_ct.py::test_osr_ct_4 osr/osr_ct.py::test_osr_ct_6 -q
```

API/CLI의 출력 차이는 같은 환경에서 아래 입력을 대조한다. 기존 API EPSG:4326은 WKT1, `gdalsrsinfo` 기본 WKT 부분은 WKT2:2018, 명시 WKT1 선택은 계속 지원되어야 한다. 실제 출력은 아직 미확인이다.

```sh
gdalsrsinfo EPSG:4326
gdalsrsinfo -o wkt1 EPSG:4326
python -c 'from osgeo import osr; s=osr.SpatialReference(); s.ImportFromEPSG(4326); print(s.ExportToWkt())'
```

엄격 C3 적격은0이므로 조건부 회수율은 **해당 없음**이다. 검색 실험을 실행하지 않았고, 이 연구가 새 원리를 검색해 냈다는 성능 수치로 전환하지 않는다.


### RFC72와 RFC74의 별도 재개 명령

RFC72의 합병본에는 `test_osr_ct_1`이 전역 상태를 마련하고 다음 시험이 이를 사용하는 구조가 남아 있다. 그래서 RFC73에서 제시한 선택 함수 실행 명령을 옛 RFC72에 그대로 적용하지 않는다. GDAL `59d0840b1980d1a1a84701b6dae5fc5c78e999f5`, 그 버전의 Python 바인딩과 호환 PROJ4, 당시 pytest를 준비한 격리 환경에서 **모듈 전체**를 입력으로 사용한다. 입력 좌표는 옛 코드의 `(-117.5,32,0)`이다.

```sh
cd autotest
python -m pytest -vv -p no:sugar --color=no -o console_output_style=classic osr/osr_ct.py
```

ASAN 방식까지 확인하려면 해당 고정 CI script의 GCC5.2/ASAN2·UBSAN0 및 suppression 파일을 먼저 마련해야 한다. 원 script는 작업 트리 일부를 지우고 pip를 제한 없이 갱신하므로, 현재 환경에서 그것을 통째로 실행해 역사적 성공을 주장하지 않는다. 당시 의존성의 정확한 해결 버전은 미확인이다. 위 명령은 pytest 모듈 포팅의 실행 확인이며 ASAN·모든 CI 통과를 대신하지 않는다.

RFC74의 구성 커밋 `3a9f10aaca02876a01e090ef8437e513a4877fdf`에서는 Sphinx source가 `gdal/doc/source`, Breathe XML 입력이 `gdal/doc/build/xml`이다. 그 커밋의 custom theme·extensions와 당시 호환 Sphinx/Breathe, 미리 생성한 Doxygen XML을 준비한 격리 환경에서 다음처럼 HTML 생성을 확인할 수 있다. 출력 경로는 연구 owned_path 아래 별도 reproduction 디렉터리로 지정한다. 이 명령은 당시 DNS 배포·전체 redirect·번역 보존의 재현은 아니다.

```sh
# RESEARCH_OUTPUT은 docs/workstreams/research/AF-RES-037/reproduction 아래의 절대경로
cd gdal/doc
sphinx-build -b html source "$RESEARCH_OUTPUT/rfc74-html"
```
