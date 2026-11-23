# AF-RES-096 Q7 · 호출 경계와 별도 자원 경계

상태: **고정판 원문·상류 시험의 대조 완료 / 이 환경에서 원 시험 실행은 미실시.** 이 묶음은 배정문이 이미 지정한 Sphinx/Graphviz·GDAL/PROJ의 교정 사례다. 신규 jq/Pandoc 요청, 두 경로의 노출·열람·판정, 답·채택·댓글에는 접근하지 않았다. 이 사례를 설명할 수 있다는 사실은 새 요청에서 네 번의 접근 안에 해당 자료를 찾아낼 수 있다는 관측이 아니다.

## Q7의 답

**앞뒤 단계를 판별할 수 있지만 제품 이름만으로 나누면 틀린다.** Sphinx가 목표한 출력이 문장·텍스트인지 새 그래프 이미지인지에 따라 외부 `dot` 실행의 필요가 달라진다. GDAL의 좌표변환 API가 호출된다는 사실만으로 별도 PROJ 격자가 필요해지는 것도 아니다. 같은 데이텀의 투영변환과 특정 격자를 요구하는 데이텀 변환을 나누고, 축 순서·좌표 범위·허용 정확도·대체 연산 허용 여부를 확인해야 한다. 아래는 읽은 원문 사실이며, 성공률이나 인과효과 추정은 아니다.

|교정 요청과 목표|고정 원문에서 직접 확인한 입출력·경계|내부에서 끝나는 대조|외부 자원이 없을 때의 대조|틀리는 전제|
|---|---|---|---|---|
|Sphinx의 텍스트 문서를 만들고 줄 블록 뒤 문단을 유지|[Q7-S6](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_builders/test_build_text.py#L42-L55)의 `text` 빌더 원 시험이 문자열 결과를 비교한다.|텍스트 빌더와 writer의 해당 출력 경로는 Graphviz 이미지 연산을 요청하지 않는다. Graphviz 노드 자체도 [Q7-S2](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/graphviz.py#L434-L447)의 text/man 방문자는 `[graph]` 또는 alt 문자열을 직접 쓴다.|여기서 외부 `dot` 링크를 추가해도 줄 블록·문단 조건의 직접 근거는 늘지 않는다.|“문서에 Graphviz 관련 노드가 있으면 어떤 출력에서도 dot가 필요하다.” 텍스트 대체 출력은 실제 그림 생성과 다른 목표다.|
|Sphinx RST의 DOT 내용을 새 HTML 그래프 이미지로 만들기|[Q7-S1](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/graphviz.rst#L16-L39)에서 DOT→PNG/SVG, LaTeX 대상이면 PDF를 명시한다. [Q7-S2](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/ext/graphviz.py#L260-L319)는 `dot -T... -o...`에 DOT 바이트를 stdin으로 넘긴다.|기존 출력 파일이 정확한 해시 경로에 있으면 소스의 277–278행에서 외부 호출 전에 반환한다. 캐시된 그림 재사용과 새 그림 생성은 구별한다.|실행 파일 부재/OSError면 경고 후 `(None,None)`를 돌려주고 HTML 경로는 원 DOT를 escape해 넣는다(302–308,339–340행). “문서 파일 생성”은 계속될 수 있지만 “그래프 이미지 생성”은 만족하지 않는다.|“Sphinx가 빌드 성공하면 Graphviz 조건도 완결”, “확장을 conf.py에 넣으면 실행 파일도 설치”, “dot 미설치면 모든 빌더가 중단”이 모두 과장이다.|
|GDAL에서 WGS84 좌표를 UTM으로 투영|[Q7-G2](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L58-L90)는 위도·경도 `(32,-117.5,0)`→UTM11 `(452772.06,3540544.89,0)`을 0.01 허용차로 기대한다. [Q7-G3](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct_proj.py#L30-L57)의 단순 UTM_WGS84 행은 `grid_req=None`이다.|별도 데이텀 이동 격자를 요구하지 않는 GDAL API 경로다. 그러나 내부 PROJ 라이브러리와 CRS 처리 의존까지 없는 순수 GDAL 계산이라는 뜻은 아니다.|좌표축 순서가 바뀌면 결과 의미가 달라진다. 이 입력은 `OAMS_AUTHORITY_COMPLIANT` 설정의 위도 우선이며, 일반 경도 우선 입력으로 그대로 복사하면 안 된다.|“좌표변환에는 항상 추가 grid 다운로드가 필요하다”, 또는 반대로 “GDAL API 하나이므로 외부 의존이 전혀 없다.”|
|GDAL에서 PD/83→WGS84의 최선 연산만 허용|[Q7-G2](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L573-L597)는 EPSG4746→4326, `(50.5,10,0)`에 `SetOnlyBest(True)`를 두고 `de_adv_BETA2007.tif` 부재 예외를 기대한다.|같은 시험에서 `SetOnlyBest(False)`는 `(50.498804120408145,9.99880336687919,0)`을 기대한다. 출력 수치는 생겨도 “최선만”이라는 원 조건을 바꾼 것이다.|최선 연산을 유지하려면 그 연산의 grid 가용성이 필요하다. PROJ의 [Q7-G6](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/gie/gridshift.gie#L268-L292)는 grid 인수 누락·유효하지 않은 grid·없는 파일을 서로 다른 오류 조건으로 고정한다.|“숫자를 반환하면 원 요청을 해결했다.” 명시된 정확도나 최선 연산 조건이 있으면 낮은 정확도의 대체 출력은 성공으로 승격할 수 없다.|
|격자를 네트워크에서 가져올 수 있으니 변환 가능한가|[Q7-G4](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/usage/network.rst#L28-L56)는 네트워크 구현과 명시적 활성화, 로컬 탐색 후 원격 로드 조건을 정한다.|[Q7-G7](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/unit/test_network.cpp#L1850-L1900)의 별도 원 시험은 격자를 먼저 저장한 다음 network를 끄고 수직변환을 수행해 높이 `36.5909996032715`를 기대한다. 원격 연결이 매 변환의 필수는 아니다.|같은 파일의 [도달 불가 endpoint 시험](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/unit/test_network.cpp#L1237-L1291)은 객체 생성 성공 후 첫 변환·재시도·역변환 모두 `HUGE_VAL`과 `PROJ_ERR_OTHER_NETWORK_ERROR`를 기대한다.|“연산 목록에 후보가 보이면 격자도 읽었다.” [2246–2281행](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/unit/test_network.cpp#L2246-L2281)은 후보10개 이상을 얻어도 네트워크 활동이 없음을 검사한다.|

## 설정과 원 시험을 연결해 읽은 범위

### Sphinx / Graphviz

기준은 Sphinx **v8.1.3**, 커밋 `a1510de4777eaa2e569435f95b05f6f3293d7035`, 커미터 시각 `2024-10-13T20:23:48Z`다. 이는 해당 고정판이 2025년 이전에 존재했다는 증거이며 각 절의 최초 작성일은 아니다. Graphviz 실행 파일의 정확한 판은 이 문서·시험만으로 고정되지 않아 **미확인**이다.

[실제 conf.py(Q7-S4)](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-ext-graphviz/conf.py)는 `sphinx.ext.graphviz`를 등록한다. [입력 fixture(Q7-S5)](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/roots/test-ext-graphviz/index.rst)는 inline DOT, 외부 DOT 파일, `neato`, 상대 이미지와 URL을 포함한다. [원 시험(Q7-S3)](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_extensions/test_ext_graphviz.py#L11-L119)은 PNG의 `img`, SVG의 `object`, SVG 안 이미지·링크의 상대경로 변경을 검사한다. “이미지가 있다”를 넘어 최종 소비자인 HTML에서 자원 경로가 붙는지도 시험한다.

중요한 반증 한계는 [Q7-S8](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/sphinx/testing/fixtures.py#L224-L239)이다. 이 fixture는 `dot -V`를 호출할 수 없으면 테스트를 **skip**한다. 따라서 원 시험 코드가 있다는 사실이나 전체 검사 녹색 표시만으로 Graphviz 실제 동작을 검증했다고 쓸 수 없다. 이번 연구에서는 실행·skip 여부를 관측하지 않았으며, 원 시험의 **기대값과 조건**만 읽었다.

이 계열에서 “외부 도구가 필요하다”는 주장은 **캐시되지 않은 새 그래프를 이미지로 생성한다**는 조건에 한정한다. 일반 텍스트 렌더링, Graphviz alt 출력, 이미 생성된 캐시 파일 재사용으로 범위를 넓히면 성립하지 않는다. 그래프 그림이 목표일 때 원 DOT의 HTML fallback은 완결이 아니다.

### GDAL / PROJ

GDAL **v3.10.0**, `35a44cc570cdf4dbd55611e4bd61da76e56bc221`(`2024-11-01T15:42:59Z`), PROJ **9.5.1**, `41f79ccfe107d3951dac6826f289b55d17cc3b81`(`2024-12-01T11:34:42Z`)를 고정했다. 각 원 시험의 실제 CI 이미지·PROJ-data 배포판은 이 연구에서 확보하지 않았으며 **미확인**이다. GDAL의 `SetOnlyBest` 원 시험은 PROJ 9.2 이상을 요구한다.

[GDAL 공식 튜토리얼(Q7-G1)](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/doc/source/tutorials/osr_api_tut.rst#L339-L469)은 변환 객체 생성 실패와 실제 좌표 변환 실패를 구분한다. 특정 연산을 지정하는 예에는 축 교환, degree↔radian, 두 horizontal grid shift를 포함한다. 이 중간 단계를 빼고 “두 CRS 이름을 입력한다”만 연결 근거로 쓰면 단위·축 경계가 사라진다.

[PROJ 명세(Q7-G5)](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/usage/transformation.rst#L328-L368)는 `@`로 표시한 grid는 선택 사항이며, `null`은 전 세계에 0 이동을 적용하는 특수 grid라고 설명한다. 누락을 무시하거나 0 이동으로 떨어지는 경로는 오류 회피와 정밀한 원 요구 달성을 구별해야 하는 반례다. [원 grid 시험(Q7-G6)](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/test/gie/gridshift.gie#L10-L44)도 유효 grid 안의 두 좌표는 수치 기대값을 두지만 영역 밖 좌표에는 별도 오류를 기대한다. 파일을 확보했어도 **좌표가 격자 영역 안인가**라는 조건이 남는다.

GDAL을 주 도구로 부르는 사용자 요청에서 PROJ는 이미 필수 런타임 구성일 수 있다. 이 교정의 인접성은 “이름이 다른 라이브러리”가 아니라 **선택된 연산이 요구하는 추가 격자·설정·입력 범위**의 가용성이다. 별도 파일 자원은 앞뒤 실행 단계가 아니라 처리 단계의 입력이 될 수도 있다. 따라서 Q1의 생산자/소비자 명명 규칙을 데이터 의존성 전체에 일반화하면 놓치는 경계가 있다. 이것은 연구자의 범위 해석이며 신규 표본의 선정 규칙을 바꾼 것이 아니다.

## 세 관점에서 반환할 자료

|관점|한 링크가 충분한 경우|연결된 두 링크가 필요한 경우|한 가지 되물을 조건|
|---|---|---|---|
|질문자|문장·표 텍스트 출력은 [Sphinx text 원 시험](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/tests/test_builders/test_build_text.py#L42-L55); 동일 데이텀 투영은 [GDAL 원 시험](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L58-L90).|그래프면 [DOT 입력·출력 설명](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/graphviz.rst#L16-L39)과 [실행 파일 설정](https://github.com/sphinx-doc/sphinx/blob/a1510de4777eaa2e569435f95b05f6f3293d7035/doc/usage/extensions/graphviz.rst#L201-L239). 두 절이 같은 파일이므로 검색 파일 수는 1이다.|최종 산출물은 텍스트 대체 설명인가 실제 그래프 그림인가?|
|도구 유지관리자|정확한 실패가 grid 부재라면 [GDAL only-best 회귀시험](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L573-L597).|[선택된 연산의 grid 조건](https://github.com/OSGeo/gdal/blob/35a44cc570cdf4dbd55611e4bd61da76e56bc221/autotest/osr/osr_ct.py#L573-L597)과 [로컬/원격 로드 규칙](https://github.com/OSGeo/PROJ/blob/41f79ccfe107d3951dac6826f289b55d17cc3b81/docs/source/usage/network.rst#L28-L56).|최선 연산이나 특정 정확도가 필수인가, 낮은 정확도의 대체 연산을 허용하는가?|
|검색 결과 편집자|주 도구 원문이 이미 입력·처리·출력·실패 조건을 모두 지지하면 그 파일만 반환한다.|별도 자원 없이는 명시 조건이 깨지는 경우에만 소비 경계 원문과 자원 확보·가용성 원문을 함께 반환한다.|이미지/좌표의 존재만 확인했는가, 요구한 형식·축·단위·정확도까지 확인했는가?|

## 반례 탐색·분모·귀속

- 직접 연 고유 파일 후보 **15**. 그중 상응 주장에 사용한 1차 자료 **14**(Sphinx계열7: S1·S2·S3·S4·S5·S6·S8, GDAL/PROJ계열7: G1–G7). `tests/conftest.py`(S7)는 fixture 위치 탐색용이고 핵심 근거가 없어 하한 산입에서 제외했다. 커밋·tree API6회, 상류 라이선스 고지3회, 검색 미리보기와 같은 파일 반복 열람도 산입0이다. 실제 HTTP 취득24회 중 실패0; 보존된14개 근거 파일의 SHA-256은 취득 영수증과 모두 일치한다. 이 검산은 파일 확인이며 소프트웨어 동작 시험이 아니다.
- 독립 프로젝트 저작 계보 **3**: Sphinx, GDAL, PROJ. 표의 구체적 교정 목표 **5**. 실제 사용자 공개 사건이나 이 연구자의 실행 사건 **0**. 파일14개를 독립 사용자 사건14건으로 세지 않는다. `event_id`는 문서/시험 묶음을 추적하기 위한 계보 식별자다.
- 외부 의존이 항상 필요하다는 주장을 깨기 위해 Sphinx text/man 방문자·일반 text 원 시험·캐시 단축 경로, GDAL의 grid_req=None 투영, PROJ의 선택 grid·null grid·로컬 다운로드 후 network off를 확인했다.
- 외부 자원이 보이면 완결이라는 주장을 깨기 위해 Graphviz 시험 skip 조건과 실제 이미지 경로 검사, GDAL only-best 대체 연산, PROJ 영역 밖 오류·도달 불가 endpoint·목록 생성만으로는 network를 읽지 않는 원 시험을 확인했다.
- **사실:** 위 고정 파일에 적힌 처리, 기대값, skip·오류 조건. **연구자 추론:** 링크 적합 판정은 목표 출력·정확도·연산의 필수 입력에 따라 달라진다. **설계 제안:** 반환 카드에서 “후보 목록·원문 열람·실제 실행·조건 달성”을 서로 다른 필드로 유지한다. 제안은 신규 A/B 우열의 관측이 아니다.
- 신규 실험 기여: 모집0, 경로0, A만/B만/양쪽 분자0. **발견 능력 승률은 산출 불가(새 표본 탐색 분모0)**. 이 교정 결과를 본 실험의 사전 완결 판정에 넣지 않는다.

## 미실시·다음 최소 확인

판 고정 Sphinx/Graphviz·GDAL/PROJ 프로그램 실행은 미실시다. 본 과제는 문서와 **상류 원 시험에 기록된 기대값**을 대조했으며, 그 시험을 실행한 것으로 보고하지 않는다. 실제 배포자 실행 receipt, Graphviz 판, PROJ-data 배포판·격자 해시가 없다. 아래 명령은 **실행할 대상과 입력을 특정하는 후속 명령**이며 이번 결과가 아니다.

1. Sphinx 위 SHA를 checkout한 별도 환경에서 `dot -V`, `python -m pytest tests/test_builders/test_build_text.py tests/test_extensions/test_ext_graphviz.py -rA`를 실행한다. `tests/roots/test-ext-graphviz/` 원 fixture를 입력으로 쓰고 skip 수·Sphinx/Graphviz판·생성 파일을 보존한다. missing-dot 경로는 `sphinx-build -b html -D graphviz_dot=/nonexistent/af096-dot tests/roots/test-ext-graphviz output-missing`와 정상 dot 경로를 각각 깨끗한 출력 디렉터리에서 실행해 비교한다. 캐시를 공유하지 않는다. 그래프 생성 여부와 프로세스 종료값을 따로 판정한다.
2. GDAL 위 SHA+PROJ9.5.1+정확한 PROJ-data manifest를 준비해 `python -m pytest autotest/osr/osr_ct.py -k 'test_osr_ct_2 or only_best_enabled' -rA`를 실행한다. 상류 시험이 가정하는 missing-grid 환경과 격자 제공 환경을 섞지 않는다. `SetOnlyBest=True/False`의 `(50.5,10,0)` 입력에 대해 실제 선택 연산·grid 경로/해시·출력·오류를 기록한다.
3. PROJ 위 SHA의 빌드·시험 환경에서 `gie test/gie/gridshift.gie`와 `ctest --test-dir build -R proj_test_cpp --output-on-failure`를 실행하되 정확한 테스트 이름은 `ctest --test-dir build -N`에서 먼저 확인한다. 네트워크 시험은 프로젝트 설정이 활성화한 경우에만 실제 실시로 기록하고, network off/로컬 grid 유무/endpoint 도달 여부를 각각 남긴다. **최소 판정 변경 관측**은 같은 고정 입력에서 “있다고 가정했던 grid가 없어도 동일한 명시 정확도를 만족함” 또는 “가용 grid가 있어도 영역·축·형식 때문에 실패함”이다.

Q7 다음 첫 행동은 Graphviz 없는 깨끗한 출력 디렉터리에서 HTML이 원 DOT로 fallback하는지를 정확판으로 확인하는 것이다. 원문 해석은 강하지만 실제 실행으로 관측하지 않은 한계를 먼저 줄인다.
