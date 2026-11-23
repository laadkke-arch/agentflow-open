# 다른 분야의 지정 반례: 수직 raster 값과 Python 상속도

| 지정 사례·목표 | 주 설명만으로 충분한 범위 | 인접 발행자 자료가 필요한 범위 | 원 시험과 확인 한계 |
|---|---|---|---|
| **XD-GDAL-VSHIFT** — GDAL 3.10.0의 수직 값 보정이 언제 작동하고 값이 왜 달라지는가 | `gdalwarp`의 Vertical transformation 절에 자동 적용 조건인 명시적 수직 CRS·단일 밴드, 강제/금지 옵션, 단위 우선순위가 있다. 이 규칙을 묻는 데 필요한 설명은 주 매뉴얼 안에 있다. | 실제 geoid grid가 없거나 찾지 못할 때는 PROJ resource-files의 탐색 순서·`PROJ_DATA`·배포/설치 절이 추가 조건을 준다. 저수준 연산을 직접 구성할 때는 `vgridshift`의 grid 형식·단위·방향을 따로 확인해야 한다. | GDAL 원 fixture는 100→120, 100→80, 두 grid에서 100→115, 동일 grid에서 100→100을 기대한다. 실제 실행은 하지 않았다. 상수 grid는 상류가 만든 시험 입력이다. 실제 DEM·실세계 grid가 제공된 것으로 대체하지 않았다. |
| **XD-SPHINX-INHERITANCE** — `top-classes`를 줬는데 상위 클래스 A가 남는가 | Sphinx inheritance 문서는 모듈 전체를 입력하면 A가 먼저 포함될 수 있다는 알려진 문제와, 필요한 하위 클래스를 직접 열거하는 해결 입력을 설명한다. 이는 Python 클래스 선택 문제다. Sphinx의 Graphviz 설정 문서에도 실행 파일 경로와 전달 인자가 이미 있다. | 특정 Graphviz 렌더러/formatter까지 요구하면 Sphinx의 `png`/`svg` 선택만으로 가용성을 보장하지 못한다. Graphviz 공식 `-Tformat:`·`-v` 절이 실제 빌드의 출력 조합을 확인할 방법을 준다. 이 경우 인접 실행기 문서와 실제 조회 결과가 필요하다. | 원 fixture는 같은 B/C 경계에서 명시적 F,D,E와 모듈 전체를 나눈다. 원 시험의 허용 목록은 각각 5개·6개지만 실제 목록에 대한 membership 반복 검사라 완전한 집합·개수 보장은 아니다. 실행기 가용성 fixture로 건너뛸 수도 있다. 실제 빌드·이미지 생성은 하지 않았다. |

## 범위와 계수

이 조사는 사전 판정의 원격 봉인 `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673` 뒤에 수행했다. 지정 사례군은 **2개**, 신규 모집 적중은 **0개**, 상류 시험 실행은 **0회**, 봉인한 32개 판정 수정은 **0개**다. F/S 및 A/B 패킷을 새로 구성한 실험이 아니므로 이 표에서 이득률·손실률이나 발견률을 계산하지 않는다.

`sources.jsonl`에는 직접 읽은 자료 14개를 기록했다. 그중 고정 원문 **10개**를 보수적인 자료 하한에 산입한다: 공식 문서 5개와 원 시험/fixture 5개다. GDAL·PROJ·Sphinx·Graphviz의 파일 수이며 독립 사건 10개라는 뜻이 아니다. 동일 파일의 여러 절·여러 시험 함수·웹 렌더링은 다시 세지 않았다. 보조 입력 XS3, 구현 XS4, 096과 문서 계보를 공유하는 설정 XS8, 비고정 현재 SVG 문서 XV2는 읽은 기록을 남기되 하한에는 넣지 않았다. `counts.json`은 원장에서 다시 계산된다.

고정판은 GDAL 3.10.0 `35a44cc570cdf4dbd55611e4bd61da76e56bc221`, PROJ 9.5.1 `41f79ccfe107d3951dac6826f289b55d17cc3b81`, Sphinx 8.1.3 `a1510de4777eaa2e569435f95b05f6f3293d7035`이다. Graphviz 문서는 사이트 원본 커밋 `51d048c433e5a80ab51915876b695c971544fe54`에 고정했지만, 이것을 Graphviz 실행기 버전으로 취급하지 않았다.

## 1. GDAL/PROJ: 외부 데이터가 있어도 추가 링크가 항상 필요한 것은 아니다

주 매뉴얼 [XG1, 623–654행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/programs/gdalwarp.rst#L623-L654)은 수직 변환의 자동 적용 조건과 단위 환산을 함께 설명한다. 단일 밴드 조건을 만족하지 않거나 보정이 금지된 상황을 이해하려는 독자에게는 이 절 자체가 판단 단위다. 이 파일은 외부 grid가 필요할 수 있다는 경고도 이미 포함한다. 따라서 외부 의존이 있다는 사실만으로 주 도구 설명이 불충분하다고 판정하면 틀린다. 다만 선택한 원 시험은 단일 밴드이므로, 다중 밴드의 부정 대조를 실행했다고 쓰지 않는다.

원 시험 [XG2, 1865–2046행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L1865-L2046)은 같은 값 100과 상류 정의 grid 20/5를 방향별로 조합한다. 기대값은 한 방향에서 120, 역방향에서 80, 두 grid 사이에서 115, 동일 grid를 양쪽에 쓸 때 100이다. 이는 “grid가 있으면 값에 한 번 더한다”는 설명에 대한 명확한 반례다. 값을 유지하는 100도 자동으로 실패라 부를 수 없다. 이 수치는 시험 소스의 기대값이며 이번 연구의 측정값이 아니다.

자원 누락을 해결하는 목표라면 필요한 근거가 달라진다. [XG4, 17–82행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/resource_files.rst#L17-L82)은 명시적 파일 경로, callback/context 경로, 사용자 경로, 환경 변수, 설치 경로의 우선순위와 일부 단계가 나머지를 중단시키는 조건을 설명한다. [XG4, 138–149행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/resource_files.rst#L138-L149)은 발행자의 `PROJ-data`, CDN, `projsync` 또는 `PROJ_DATA`에 압축을 푸는 경로를 제시한다. 선택한 `gdalwarp` 절에는 이 실행 조건의 세부 내용이 없다. 따라서 “이 실제 설치에서 grid를 찾아 수직 보정을 실행할 수 있게 하라”는 목표에는 인접 자원 문서와 실제 설치 상태가 더 필요하다. 자료 위치를 안다고 해당 grid의 지리적 범위·정밀도·설치 완료까지 확인된 것은 아니다.

[XG3, 102–133행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/operations/transformations/vgridshift.rst#L102-L133)의 저수준 부호·단위 식도 GDAL wrapper의 입출력 방향과 함께 읽어야 한다. 기본 multiplier가 -1이라는 문구만 가져와 GDAL의 120 기대값이 틀렸다고 결론내릴 수 없다. 정확한 GDAL 선택 pipeline은 이번에 추적하지 않았다.

### 원 시험 자체가 의도한 입력을 확인하지 못하는 경우

[XG2, 2222–2249행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L2222-L2249)의 `test_gdalwarp_lib_135s`는 임시 grid를 생성한 뒤 빈 보정 값의 오류 경로를 시험하려 한다. 그러나 2247행의 문자열에는 f-string 접두사가 없고 `{empty_grid_gtx}`가 그대로 들어 있다. **의도한 임시 grid 경로와 소스가 실제 전달하는 문자열을 구별해야 한다.** PROJ≥8에서 일반 `Exception`만 기대하므로, 이 시험만으로 “생성한 grid의 빈 값이 원인이었다”는 주장은 성립하지 않는다. 구체적인 런타임 예외 원인은 실행하지 않아 미확인이다. 이것은 본문의 실세계 데이터가 누락됐을 때 연구자 예시로 채워 넣으면 안 된다는 점과도 연결된다.

## 2. Sphinx/Graphviz: 실행기보다 앞에서 결정되는 실패

[XS1, 51–98행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/inheritance.rst#L51-L98)은 `top-classes`로 조상 탐색을 멈춰도 모듈 안의 A가 독립 노드로 남는 경우를 직접 다룬다. 원 클래스 fixture [XS5](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-inheritance/dummy/test.py)는 A를 상속하는 B/C와 그 아래 D/E/F를 정의한다. [XS6](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-inheritance/diagram_w_2_top_classes.rst)는 F,D,E를 열거하고, [XS7](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-inheritance/diagram_module_w_2_top_classes.rst)는 모듈 전체를 넣는다. 두 입력 모두 B/C를 경계로 삼는다.

주 구현의 [모듈 입력 처리](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/inheritance_diagram.py#L100-L130)와 [클래스 추가·탐색 종료](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/inheritance_diagram.py#L143-L222)도 이 설명과 맞는다. 모듈에서 먼저 선택된 A를 renderer 문서가 제거해 주지는 않는다. 독자에게 돌려줄 절은 Graphviz 설치 안내가 아니라 Sphinx의 이 입력 범위 설명이다.

단, 원 시험 [XS2, 90–130행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_inheritance_diagram.py#L90-L130)은 “실제 항목 각각이 기대 목록에 있는지”를 검사한다. 기대 목록 전체와의 동등성이나 길이를 검사하지 않는다. 그 목록의 5/6을 실제 실행에서 확인된 출력 개수로 쓰면 과장이다. 문서·입력·구현은 동작의 이유를 지지하지만, 엄격한 출력 집합 확인은 여전히 남는다.

외부 실행기 문제에서도 주 문서의 범위를 먼저 보아야 한다. [XS8, 203–229행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/graphviz.rst#L203-L229)은 `graphviz_dot`의 전체 경로, 명령행 `-D` 설정, 전달 인자, `png`/`svg` 선택을 설명한다. 단순 경로 설정에는 이 설명이 충분할 수 있다. 반면 [XV1, 85–107행](https://gitlab.com/graphviz/graphviz.gitlab.io/-/blob/51d048c433e5a80ab51915876b695c971544fe54/content/en/docs/cli/_index.md#L85-107)은 실행기 빌드에 따라 renderer/formatter가 달라지고, 어떤 명령으로 실제 조합을 확인하는지 설명한다. 특정 조합을 요구하는 목표라면 이 인접 문서와 실행 결과가 빠져서는 가용성을 완결로 세기 어렵다. 이번 조사에는 그 실행 결과가 없다.

## 3. 반환 제안과 AF-RES-100 결론에 주는 제약

| 관점 | 수직 raster 사례 | 상속도 사례 |
|---|---|---|
| 독자 | 규칙 질문에는 XG1 Vertical transformation, 실제 자원 설치에는 XG4 Resource files를 최대 두 링크로 준다. 실패 조건: 사용자 DEM/CRS·단위·grid 실물이 확인되지 않으면 수치 결과는 미확인이다. | 노드가 남는 문제에는 XS1 top-classes와 XS6 명시 입력을 준다. 실행기 조합 문제로 목표가 바뀌면 XS8 설정과 XV1의 `-T` 절로 바꾼다. 하나의 요청에 네 링크를 쌓지 않는다. |
| 도구 유지관리자 | 135s의 실제 파일명과 예외 원인을 우선 확인한다. 생성 fixture의 존재만으로 그 fixture가 시험에 들어갔다고 보지 않는다. | membership 검사와 실제 집합 동등성 검사를 구별한다. 테스트가 skip되면 빌드 성공의 증거로 세지 않는다. |
| 검색 결과 편집자 | 전체 파일보다 자동 조건·단위·자원 설치 중 목표에 해당하는 절을 지명한다. 인접 링크는 추가 조건이 빠졌을 때 선택한다. | 상속 입력 선택과 외부 렌더러 능력을 구별해 절을 지정한다. 외부 실행기 어휘가 등장한다고 인접 링크를 우선하지 않는다. |

이 지정 사례는 “인접 링크가 유리하다”는 일반 결론을 강화하기보다 조건을 붙인다. 주 도구 문서에 외부 의존과 해결 조건이 이미 포함될 수 있고, 인접 문서가 있어도 실제 데이터·실행기 상태가 확인되지 않을 수 있다. 또한 원 시험의 존재가 입력 계보와 출력 보장을 대신하지 못한다. 32개 패킷의 이득·손실은 그 패킷 원장에서 판단해야 하며, 여기서 읽은 사후 자료를 넣어 사전 완결을 올리지 않는다.

## 재현·미실시

`collect.py`는 고정 13개 파일의 원문을 무시되는 `_cache/`에만 가져오고 원 hash를 비교한다. 현재 SVG 탐색 자료 XV2는 비고정 보조 자료이므로 자동 재수집 대상에서 제외한다. `build_records.py`는 원 바이트에서 각 직접 읽은 절의 Unicode/UTF-8 범위와 SHA-256을 계산하고 `sources.jsonl`·`counts.json`을 만든다. 전체 외부 본문은 커밋하지 않는다.

상류 실행 명령, 정확한 원 fixture 입력과 필요한 의존성, 각 미실시 사유는 [unrun.md](unrun.md)에 있다. 이 보고서의 검토는 별도 하위 작업자가 수행한 원문 검토이며, 독립 런타임 재현이나 사람의 외부 심사로 표현하지 않는다.

`validation.json`에는 14개 원문 지문, 32개 직접 읽은 절의 문자/바이트 대응, 고유 산입 파일 10개, 원문 캐시 15개가 git 무시 대상임을 대조한 결과가 있다. 오류는 0개이며 이는 출처 원장 구조 검사다. 상류 프로그램의 동작 검사는 아니다. API tree의 403 접근 실패와 고정 connector tree로 우회한 범위는 `access-failures.jsonl`에 별도로 남겼으며 자료 수에 넣지 않았다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| GDAL 135s의 의도한 grid와 실제 문자열이 다르며 예외 원인은 미확인이다. | 고정판의 원 `test_gdalwarp_lib_135s`를 PROJ 진단 로그와 함께 실행해 열린 파일명을 확인한다. | 원래 코드가 실제 임시 grid를 읽고 그 grid의 빈 값 때문에 실패했다는 trace가 있으면 이 소스 수준 우려를 수정한다. |
| Sphinx 원 시험의 membership 목록은 실제 전체 집합과 개수를 보장하지 않는다. | 고정 XS5/XS6/XS7와 `test_inheritance_diagram`에서 얻은 `class_info` 전체를 보존한다. | 명시 입력에서 A가 남거나 모듈 입력에서 A가 사라지는 실제 결과가 나오면 문서·구현에서 한 조건부 판단을 수정한다. |
| 실제 DEM/grid·Graphviz 실행기/plugin 상태를 실행하지 않았고 이 사례들은 F/S 패킷 실험이 아니다. | 원 GDAL fixture, 원 Sphinx fixture, `dot -Tsvg:` 및 실제 사용자 DEM/CRS·grid 지문을 확보한다. | 동일 버전·실제 입력에서 주 설명만으로 설치까지 완결되거나, 인접 조건을 모두 충족해도 실패하면 링크 필요성의 적용 범위를 다시 정한다. |
