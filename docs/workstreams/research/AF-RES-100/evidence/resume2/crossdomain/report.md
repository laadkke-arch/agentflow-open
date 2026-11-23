# Q7 교차 도메인 맥락: GDAL 수직 이동과 Sphinx 상속도

작성일: 2026-11-23 UTC. 이 자료는 사전에 지정된 **두 개의 명명된 맥락 사례**를 조사한 것이다. recruited8, 32개 패킷의 주판정, 문서 접근 전략의 승리 횟수 또는 효과 크기에 포함하지 않는다. 기존 봉인입력과 reader 결과는 수정하지 않았다.

## 결과

두 사례 모두 기본 기능의 의미와 외부 의존 조건을 구별할 수 있다. GDAL의 주 문서는 자동 수직 이동의 단일 밴드 조건을 직접 설명한다. Sphinx의 상속도 문서는 클래스 인수와 캡션을 직접 설명한다. 반면 **정확한 PROJ 그리드 탐색·결손 처리**, **native Graphviz 실행 파일과 출력 형식 확인**까지 답하려면 각각의 인접 문서가 더 구체적인 근거를 제공한다. 여기서 ‘필요’는 아래의 좁은 운영 조건을 완성하기 위한 의미이며, 주 문서가 모든 관련 문제에 불충분하다는 보편 주장으로 사용하지 않는다.

| 고정 사례 | 주 문서만으로 충분한 조건 | 추가로 확인할 경계 | 인접 근거 |
|---|---|---|---|
| GDAL warp 수직 이동 | 단일 밴드에서 자동 적용되는 조건과 `-novshift` | 요구 그리드의 위치·가용성, `@`로 표시한 선택적 그리드의 의미 | PROJ `vgridshift.rst`, `resource_files.rst` |
| Sphinx inheritance-diagram | 클래스/기저 클래스 탐색, `caption` 지정 | DOT를 이미지로 만드는 실행 파일과 SVG/PNG 지원 | Graphviz CLI 문서 및 Sphinx 전용 fixture의 실행 파일 gate |

공식 문서 5개, 서로 다른 상류 테스트 프로그램 2개, Sphinx fixture 입력 전체 8개를 포함한 **18개 출처**를 `sources.jsonl`에 고정했다. 각 항목에는 원 URL, 고정 revision, 취득 UTC, SHA256, 저자 계보, 읽은 정확한 절/줄 범위와 원본 문자·UTF-8 바이트 범위, 해당 근거의 한계를 기록했다. `fixtures.json`은 문서상 기대와 실제 실행을 별도 필드로 보존한다.

통합 원장용 공통 필드도 기존 상세 필드와 함께 보존했다. 최소개수에는 `crossdomain_official_docs` 5개와 `crossdomain_fixtures` 2개를 산입한다. Sphinx의 입력 8개·공통 실행 gate는 이미 산입한 하나의 상속도 fixture를 뒷받침하는 파일이므로 `count_minimum=false`와 `duplicate_reason`을 기록했다. 구현 소스도 별도 fixture로 세지 않는다. 이 산입 구분은 문서/fixture 최소개수 충족을 위한 것이며 통계적 독립 표본 수가 아니다.

**재사용 공개:** 공통 gate 파일 `sphinx/testing/fixtures.py`는 AF-RES-096에서도 읽은 파일이다. 이번 조사에서는 새 상속도 fixture의 실행 조건을 연결하기 위해 같은 공통 인프라를 다시 읽었다. 이 사실은 coordinator가 후속 확인해 주었으며, 수리를 위해 AF-RES-096 자료를 다시 열지는 않았다. 해당 gate는 신규 자료 최소개수나 신규 예제로 세지 않았다. 새 예제라는 판단은 상속도 본 문서와 `test-ext-inheritance_diagram` fixture 쌍에 적용하며, 모든 보조 파일이 처음 사용된 자료라는 주장은 하지 않는다.

## 1. 과학 계산: GDAL의 단일 밴드와 그리드 의존

### 고정 문서와 상류 fixture

GDAL 3.10.0의 고정 revision은 `35a44cc570cdf4dbd55611e4bd61da76e56bc221`이다. `gdalwarp.rst`의 Vertical transformation 절은 수직/3D CRS 조건과 단일 밴드 조건을 함께 만족할 때 자동 수직 변환을 수행한다고 명시한다. `-vshift`와 `-novshift`의 강제·비활성화도 설명한다. 따라서 같은 CRS 설정에서 한 밴드와 여러 밴드의 값 변경이 다른 이유를 설명하는 데 주 문서가 충분하다. [GDAL 주 문서, 624–652행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/programs/gdalwarp.rst#L624-L652), [옵션, 181–196행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/programs/gdalwarp.rst#L181-L196).

이에 대응하는 상류 fixture는 `autotest/utilities/test_gdalwarp_lib.py`의 `gdalwarp_135_grid_gtx`와 `gdalwarp_135_src_ds`이다. 전자는 WGS84의 3×3 GTX 그리드를 상수 20으로 채우고, 후자는 지정된 geotransform을 가진 한 픽셀·한 밴드 래스터를 100으로 채운다. `test_gdalwarp_lib_135`는 이 그리드를 source CRS의 geoid 보정으로 사용하고 EPSG:4979로 변환한 값이 **120**이라고 assert한다. 이는 읽은 상류 코드의 기대값이다. [그리드 fixture, 1865–1879행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L1865-L1879), [입력 fixture 및 테스트, 1899–1935행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L1899-L1935).

여러 밴드 변형은 위 상류 테스트의 원래 assertion이라고 주장하지 않는다. 이 변형의 기대는 주 문서와 PROJ 기반 구현 분기의 밴드 수 조건으로부터 도출한 것이다. 구현은 한 밴드 또는 명시적 강제 옵션과 수직 축 여부를 검사한다. [GDAL 구현, 619–667행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/apps/gdalwarp_lib.cpp#L619-L667).

### 인접 문서가 완성하는 조건

GDAL 주 문서는 그리드 설치 또는 PROJ 네트워크 기능이 필요할 수 있음을 이미 알린다. 그러나 정확한 파일 탐색 순서와 선택적 결손 의미까지 그 페이지가 제공하는 것은 아니다. PROJ 9.5.1의 `41f79ccfe107d3951dac6826f289b55d17cc3b81`에서 `resource_files.rst`를 읽으면 명시적 경로, API 검색 경로, 사용자 디렉터리, `PROJ_DATA`, 설치 경로 등의 관계를 확인할 수 있다. API 및 빌드 설정에 따른 우선순위도 있어 `PROJ_DATA`가 언제나 첫 번째라는 식으로 단순화하면 안 된다. [PROJ 자원 탐색, 19–82행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/resource_files.rst#L19-L82).

`vgridshift.rst`는 그리드의 `@` 접두사가 파일 부재를 허용하고, 복수 그리드가 나열 순서로 우선한다고 명시한다. 이에 대응하는 GDAL `test_gdalwarp_lib_135j`와 `135k`는 존재하지 않는 선택적 그리드에서 값이 **100으로 유지**된다고 assert한다. 따라서 실행이 끝난 사실을 실제 높이 보정이 수행된 사실로 바꿔 말할 수 없다. [PROJ 그리드 의미, 23–45행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/operations/transformations/vgridshift.rst#L23-L45), [선택적 결손 상류 테스트, 2091–2114행](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/utilities/test_gdalwarp_lib.py#L2091-L2114).

### 실제 실행: 별도의 로컬 보조 실험

현재 환경의 `/usr/bin/python3`에는 **GDAL 3.10.3 / PROJ 9.6.0**이 이미 있었다. 고정 문서판과 동일하다고 가정하지 않았다. `run_gdal_fixture.py`는 위 fixture를 작게 재구성하고, `PROJ_NETWORK=OFF`, 명시적 로컬 그리드 경로를 사용했다. 결과는 `gdal-runtime.json`에 보존했다.

| 조건 | 기대의 출처 | 실제 값/결과 |
|---|---|---|
| 한 밴드, 존재하는 상수 20 그리드 | 상류 `135` assertion | 120 |
| 두 밴드, 같은 그리드 | 주 문서·구현에서 도출한 연구 변형 | 100, 100 |
| 한 밴드, `-novshift` | 주 문서에서 도출한 연구 변형 | 100 |
| 한 밴드, `@` 선택적 결손 그리드 | 상류 `135j`의 경로를 재구성 | 100 |
| 한 밴드, 필수 그리드 결손 | 연구의 대조 변형 | 예외 발생, 출력 데이터셋 없음 |

다섯 조건 모두 사전에 코드에 기록한 기대와 일치했다. 마지막 조건의 실제 예외에는 필요한 그리드를 찾지 못해 `vgridshift` 파이프라인 구성과 출력 범위 계산에 실패했다는 설명이 포함된다. 이는 해당 로컬 버전에서 관측한 사실이며, 고정 GDAL 3.10.0 상류 테스트를 실행했다는 주장이 아니다.

이 상수 그리드는 실제 geoid의 정확도, 지리적 적용 범위, datum 선택이나 실측 높이를 검증하지 않는다. 실제 과학 데이터에 대한 오차나 일반 성능을 이 결과에서 추정하지 않는다.

## 2. 문서 생성: Sphinx 상속도와 native Graphviz

### 고정 문서와 구체적인 입력

Sphinx 8.1.3의 고정 revision은 `a1510de4777eaa2e569435f95b05f6f3293d7035`이다. 상속도 문서는 클래스 또는 모듈을 인수로 받아 기저 클래스를 찾는 동작과 `caption` 옵션을 설명한다. 이것만으로 다음 입력을 지정하는 조건은 충족된다. [상속도 문서, 11–42행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/inheritance.rst#L11-L42).

```rst
.. inheritance-diagram:: test.Foo
   :caption: Test Foo!
```

이 입력은 `tests/roots/test-ext-inheritance_diagram/index.rst`에 실제 존재한다. `conf.py`는 상속도와 intersphinx extension을 활성화하며, Python 파일에는 `Foo → DocHere → DocSubDir1 → DocSubDir2`의 기저 클래스 관계가 정의되어 있다. fixture 루트의 세 파일과 하위 디렉터리 다섯 파일을 모두 고정했다. [입력 문서](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-ext-inheritance_diagram/index.rst#L1-L18), [설정](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-ext-inheritance_diagram/conf.py#L1-L6), [클래스](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-ext-inheritance_diagram/test.py#L1-L22).

### 문서상의 기대와 실행 파일 조건

상류 `test_inheritance_diagram_png_html`은 PNG 이미지 HTML, 캡션, 링크를 검사한다. `test_inheritance_diagram_svg_html`은 동일 fixture에 `graphviz_output_format='svg'`를 설정하고 SVG object HTML과 생성된 SVG의 링크를 검사한다. 이 기대는 테스트 소스에서 읽었으며 이 환경에서 실행한 결과가 아니다. [PNG 테스트, 156–203행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_inheritance_diagram.py#L156-L203), [SVG 테스트, 206–262행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_inheritance_diagram.py#L206-L262).

두 테스트에는 `if_graphviz_found` gate가 붙는다. 이 gate는 설정된 명령을 `-V`로 실행하고, 실행 파일을 시작할 수 없으면 테스트를 skip한다. 또한 `check=False`이므로 이 gate만 통과했다고 반환 코드 0 또는 SVG 렌더러 지원까지 증명되는 것은 아니다. 상속도 구현도 직접 DOT를 생성한 다음 Graphviz 렌더링 함수로 넘긴다. [실행 파일 gate, 224–239행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/testing/fixtures.py#L224-L239), [상속도 HTML 경계, 414–442행](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/inheritance_diagram.py#L414-L442).

인접 Graphviz CLI 문서는 `dot -V`와 `dot -Tsvg`, stdin·stdout 사용, 빌드에 따라 달라질 수 있는 renderer를 설명한다. 공식 웹사이트가 가리킨 revision `51d048c433e5a80ab51915876b695c971544fe54`의 원 Markdown을 다시 받아 고정했다. 이 revision은 2025-10-29의 문서 수정이며, Sphinx의 시점이나 로컬 Graphviz 바이너리판과 같다는 뜻은 아니다. [Graphviz CLI, 9–22행](https://gitlab.com/graphviz/graphviz.gitlab.io/-/blob/51d048c433e5a80ab51915876b695c971544fe54/content/en/docs/cli/_index.md#L9-22), [형식 및 버전 옵션, 85–116행](https://gitlab.com/graphviz/graphviz.gitlab.io/-/blob/51d048c433e5a80ab51915876b695c971544fe54/content/en/docs/cli/_index.md#L85-116).

### 실제 실행 범위

로컬 `dot -V`는 **Graphviz 2.42.4**를 보고했다. `run_graphviz_probe.py`는 읽은 fixture의 클래스 관계를 작은 DOT 입력으로 작성하여 `dot -Tsvg`에 전달했고, 반환 코드 0과 유효한 SVG root를 관측했다. 존재하지 않는 별도 실행 파일 경로를 시작하는 대조에서는 `FileNotFoundError`가 발생했다. `graphviz-runtime.json`에 명령, 버전, 결과, SVG SHA256을 기록했다.

이 실험은 **Graphviz 단독 probe**이다. Sphinx, docutils, pytest가 조사한 Python 환경에 없어 상류 Sphinx 테스트는 실행하지 않았다. 생성된 DOT는 연구자가 공급했으므로 Sphinx의 HTML, 캡션, 파일명, intersphinx inventory 또는 링크 검사가 성공했다고 주장하지 않는다. Python extension의 의미가 올바른 것과 native renderer까지 작동하는 것은 구분된 조건이다.

## 3. 출처 계보와 추론 한계

`lineage.json`은 고정 release commit과 주요 문서·테스트의 마지막 path 변경 commit을 기록한다. GDAL과 PROJ의 여러 항목은 Even Rouault라는 변경 저자를 공유한다. Sphinx 문서와 테스트의 마지막 변경에는 Adam Turner가 관여한다. Graphviz 문서 revision의 저자는 Matthew Fernandez로 기록되어 있다. 이는 마지막 변경 및 release 계보이며, 단독 원저자나 독립적인 재현 연구를 뜻하지 않는다.

따라서 공식 문서·구현·테스트 간의 연결은 추적할 수 있지만, 서로 독립인 표본 수로 셀 수는 없다. 이 조사에서 인접 문서를 선택하면 어느 비율로 해결률이 오른다는 효과를 산출하지 않았다. 두 사례는 주 문서의 명시적 계약과 데이터/실행 파일 경계를 구분하는 설명용 맥락이다.

지정된 이전 **본 문서·fixture 예제**인 OSR OnlyBest / EPSG:4746→4326 / BETA2007을 사용하지 않았다. `osr_ct.py`, `osr_api_tut.rst`, PROJ `usage/network.rst`·`usage/transformation.rst`, `test/gie/gridshift.gie`·`test_network.cpp`도 읽지 않았다. Sphinx 일반 `graphviz.rst`, `ext/graphviz.py`, `test_ext_graphviz.py`, `test-ext-graphviz` 입력 및 `test_build_text.py` 대신 상속도 전용 본 문서·fixture를 사용했다. 이 지정 경로 제외 확인은 공통 지원 파일까지 신규라는 의미가 아니다. `sphinx/testing/fixtures.py`의 gate는 AF-RES-096에서 사용한 공통 파일을 재열람한 것이며, 원장과 검증 기록에서 그 재사용과 비산입을 명시한다.

## 4. 재현과 산출물

아래 명령은 저장소 루트에서 실행한다. 첫 명령은 고정 body의 SHA256을 확인하고 인용한 절을 표시한다. `--refetch`를 붙이면 고정 URL에서 다시 취득하고, hash가 같은 경우에만 cache를 갱신한다. 패키지 설치나 Git 작업은 수행하지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/reproduce_sources.py
python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/reproduce_sources.py --refetch --source gdal-warp-doc
/usr/bin/python3 -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_gdal_fixture.py
python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_graphviz_probe.py
```

핵심 산출물은 다음과 같다.

- `sources.jsonl`: 18개 고정 출처와 정확한 근거 범위·한계.
- `fixtures.json`: 두 사례의 조건, 상류 assertion, 보조 실행과 구분된 재현 명령.
- `gdal-runtime.json`, `graphviz-runtime.json`: 실제 보조 실행 기록.
- `environment.json`, `version-probes.json`, `system-python-probe.json`: 실행 환경 조사.
- `lineage.json`: 공식 프로젝트와 저자/commit 계보.
- `validation.json`: 공통 원장 필드, 5+2 최소개수, 정확한 인용 payload hash, 지정된 본 문서·fixture 제외 경로 확인 및 AF-RES-096 공통 gate 재사용·비산입 공개.
- `run_gdal_fixture.py`, `run_graphviz_probe.py`, `reproduce_sources.py`, `assemble_evidence.py`: 재현 가능한 절차.

원 body와 생성된 GTX/SVG는 지정된 `evidence/_cache/resume2-crossdomain/`에 보존했다. 고정판의 전체 상류 테스트를 다시 실행할 경우 필요한 정확한 test node와 준비된 환경 조건은 `fixtures.json`에 명시했다. 그러한 준비나 실행이 이미 완료되었다고 가정하지 않는다.
