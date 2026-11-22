# AF-RES-038 · 링크 제공과 설명 추가를 분리하는 과제·가림 판독 결과

| 과제 ID·전체/부분 | 최초 요구·버전 | A·B·C의 차이 | 두 대안·근거 URL | t0 제출 | t1 동일 요구·검사 URL | 뒤집힐 선택 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P02·전체 / P02-R1 | 컴파일 대상과 의존관계를 legacy setup.py monolith에 묶인 상태에서 분리할 수 있는 native build 구조를 제안한다.; [formal2022-08-06 / aad11f69](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md); P-S01 L12-20 | [A 자유검색](packets/P02/arm-A.md) / [B 링크](packets/P02/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P02/arm-C.md) | [graph+packaging 위임](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py) / [다른 graph+전용 backend](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md) + [backend 규격](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md) | 컴파일 graph의 책임 위치와 Python package metadata/wheel 조립 책임의 경계를 그리거나 적으세요. | 새 C/C++/Cython extension target과 dependency를 넣을 때 어느 선언을 바꾸며, source install도 그 graph를 호출하는지 추적하세요.; [동일 요구 기준](https://github.com/lithomas1/pandas/blob/7e401dc31ca155fcc7b3128ee7a7b43989c71da3/meson.build) | 단일 compile monolith 유지안을 graph 경계로 변경 | 두 historical POC 실행·@main 의존 잠금·플랫폼 성공 미확인 |
| P02·전체 / P02-R2 | 개발 시에만 되는 병렬 컴파일 경계를 end-user source-distribution build까지 해결한다.; [formal2022-08-06 / aad11f69](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md); P-S01 L16-20 | [A 자유검색](packets/P02/arm-A.md) / [B 링크](packets/P02/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P02/arm-C.md) | [graph+packaging 위임](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py) / [다른 graph+전용 backend](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md) + [backend 규격](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md) | developer build와 unpacked source-distribution install 양쪽의 compile 호출/worker 전달 경로를 적으세요. | clean unpacked sdist에서 frontend→backend→compiler로 worker 설정이 전달되는지 살피고, 개발에서만 -j가 붙는지 확인하세요.; [동일 요구 기준](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md) | 개발에서만 병렬인 경로라면 source 설치도 연결. 고정 오답E3는 이 요구 통과. | 두 historical POC 실행·@main 의존 잠금·플랫폼 성공 미확인 |
| P02·전체 / P02-R3 | 표준 frontend/backend 경계를 통해 native artifact와 Python wheel/sdist를 일관되게 연결한다.; [formal2022-08-06 / aad11f69](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md); P-S01 L18-20 + 인용된 PEP517 P-S10 L206-284 | [A 자유검색](packets/P02/arm-A.md) / [B 링크](packets/P02/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P02/arm-C.md) | [graph+packaging 위임](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py) / [다른 graph+전용 backend](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md) + [backend 규격](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md) | pyproject/backend 및 build_wheel/build_sdist의 연결, 필요한 입력 파일, wheel 산출을 설명하세요. | sdist를 풀고 wheel hook을 실행하는 경로가 필요한 graph/source/metadata를 포함하고 wheel 위치/이름 계약을 지키는지 확인하세요.; [동일 요구 기준](https://github.com/python/peps/blob/19f2582774070b86cc4f8866d5c751f8cb7c56ee/pep-0517.txt) | sdist 입력/표준 hook 누락이면 경계 보완. 고정 예시3개는 이 요구 통과. | 두 historical POC 실행·@main 의존 잠금·플랫폼 성공 미확인 |
| P04·부분 / P04-R1 | 각 batch에서 선언된 explicit 형식 또는 첫 non-NaN으로 결정한 형식 하나를 전체 입력에 적용.; [formal2022-09-18 / e59b6ffd](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md); P-S02 Abstract and Detailed Description | [A 자유검색](packets/P04/arm-A.md) / [B 링크](packets/P04/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P04/arm-C.md) | [배열 explicit format](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py) / [행별 고정 format](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) | declared_mode, declared_format 또는 inference rule, 실제 format_used, errors 정책을 제출하세요. | 새 batch에서도 첫 채택의 같은 알고리즘을 사용하며 형식을 언제 확정했고 뒤 행에서 바꿨는지 적으세요.; [동일 요구 기준](https://github.com/pandas-dev/pandas/blob/v2.0.0/pandas/tests/tools/test_to_datetime.py) | 행별 fallback을 batch 고정 형식·raise로 변경 | 현재 날짜 literal 밖 API/시간대·성능·실행 미확인 |
| P04·부분 / P04-R2 | 서로 다른 날짜 순서로 조용히 전환하지 않고 불일치는 사전 errors 정책대로 처리.; [formal2022-09-18 / e59b6ffd](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md); P-S02 Motivation examples and Detailed Description | [A 자유검색](packets/P04/arm-A.md) / [B 링크](packets/P04/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P04/arm-C.md) | [배열 explicit format](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py) / [행별 고정 format](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) | errors='raise'로 둔 상태에서 입력 해석과 오류 조건을 설명하세요. | ['12-01-2000 00:00:00','13-01-2000 00:00:00']를 검토하세요. DMY이면 Jan12/Jan13, MDY를 처음에 고정했다면 두 번째에서 오류가 올바릅니다.; [동일 요구 기준](https://github.com/pandas-dev/pandas/blob/v2.0.0/pandas/tests/tools/test_to_datetime.py) | 선언한 raise 대신 silent fallback하는 결정을 수정; R1과 같은 원인. | 현재 날짜 literal 밖 API/시간대·성능·실행 미확인 |
| P04·부분 / P04-R3 | 부적합 문자열을 정상 날짜로 조용히 바꾸지 않음.; [formal2022-09-18 / e59b6ffd](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md); P-S02 Detailed Description errors/no silent switching; P-S06 L703-706 | [A 자유검색](packets/P04/arm-A.md) / [B 링크](packets/P04/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P04/arm-C.md) | [배열 explicit format](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py) / [행별 고정 format](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) | 선언한 형식에서 불가능한 날짜를 받으면 어떻게 종료하는지 적으세요. | explicit/inferred 모두 각 batch에서 실제 확정한 format_used에 두 공통 probe를 적용한다. DMY이면 01-13의 month13, MDY이면 13-01의 month13에서 raise가 올바르다. inferred 모드는 batch마다 같은 추론 알고리즘으로 한 번 확정한다.; [동일 요구 기준](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) | 불가능한 형식을 다른 날짜로 바꾸는 fallback을 거부; R1과 같은 원인. | 현재 날짜 literal 밖 API/시간대·성능·실행 미확인 |
| P06·부분 / P06-R1 | setitem-like 작업은 기존 Series의 dtype을 바꾸지 않음.; [formal2022-12-23 / 1fb0adb5](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md); P-S03 Abstract; Detailed description first two bullets | [A 자유검색](packets/P06/arm-A.md) / [B 링크](packets/P06/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P06/arm-C.md) | [native+선검증 guard](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py) / [생성 때 nullable+strict setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | 생성 때 정수 dtype을 명시하고 성공/오류 후 dtype이 그대로인지 설명하세요. | 각 독립 대입 전에 [1,2,3] 새 인스턴스를 같은 dtype으로 만들고, 이후 dtype을 기록하세요.; [동일 요구 기준](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | 사후 dtype 승격/재생성은 수정. 고정 오답E3는 dtype 자체를 유지. | native guard는 근거 기반 구성 설계; 완성 public recipe/역사 실행 미확인 |
| P06·부분 / P06-R2 | 정수 dtype에 손실 없이 호환되는 값은 정수값 그대로 저장.; [formal2022-12-23 / 1fb0adb5](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md); P-S03 Detailed description np_can_hold_element snippet; P-S08 L1959-1966; P-S09 L216-218 | [A 자유검색](packets/P06/arm-A.md) / [B 링크](packets/P06/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P06/arm-C.md) | [native+선검증 guard](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py) / [생성 때 nullable+strict setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | 4와 2.0 같은 호환 scalar를 넣는 동작을 보여주세요. | index1에 3.0을 넣으면 [1,3,3]이며 original dtype인가?; [동일 요구 기준](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | whole-valued float까지 거부하면 손실 없는 저장으로 수정. 고정 예시3개는 이 요구 통과. | native guard는 근거 기반 구성 설계; 완성 public recipe/역사 실행 미확인 |
| P06·부분 / P06-R3 | 비호환 fractional/text 값은 조용히 변환/승격하지 않고 오류.; [formal2022-12-23 / 1fb0adb5](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md); P-S03 fractional options and selected option1; potage example | [A 자유검색](packets/P06/arm-A.md) / [B 링크](packets/P06/arm-B.md) / [C 같은 링크+요구→절·한계](packets/P06/arm-C.md) | [native+선검증 guard](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py) / [생성 때 nullable+strict setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | 1.5와 'potage'가 들어오면 오류/변경 전후 값을 설명하세요. | 독립 reset 상태에서 index1=1.5와 index1='potage'를 시도해 오류와 unchanged data/dtype을 기록하세요.; [동일 요구 기준](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/tests/arrays/masked/test_indexing.py) | fractional 정수절삭을 쓰기 전 호환성 검증으로 변경 | native guard는 근거 기반 구성 설계; 완성 public recipe/역사 실행 미확인 |
| N08·전체(작은 흐름) / N08-R1 | SKU별·월별·점포별 집계를 각각 제공하고 원래 필드를 다른 의미로 대체하지 않는다.; [doc2010-04-27·git04-29 / bceb9c20; 첫 공개 미확인](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L21-L38); L23-L32 | [A 자유검색](packets/N08/arm-A.md) / [B 링크](packets/N08/arm-B.md) / [C 같은 링크+요구→절·한계](packets/N08/arm-C.md) | [키·값 같은 정렬순열+감소](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py) / [고유키 역색인+원행 선택](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py) | 세 grouping의 키 정의와 전체 처리 흐름을 제출한다. | 같은 6개 구매행의 재배열에서 동일한 세 grouping을 다시 산출한다.; [동일 요구 기준](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py#L95-L181) | grouping 누락/키 의미 변경이면 복구. 고정 오답E3는 키 목록은 충족. | 정식 본문 최초 공개; 장기 API 정책 대표성; 역사 NumPy 실행 미확인 |
| N08·전체(작은 흐름) / N08-R2 | 각 관측 그룹의 number에 대해 max/min/mean/sum 네 통계를 모두 낸다. 행 수는 수량 합계를 대신할 수 없다.; [doc2010-04-27·git04-29 / bceb9c20; 첫 공개 미확인](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L30-L38); L30-L36 | [A 자유검색](packets/N08/arm-A.md) / [B 링크](packets/N08/arm-B.md) / [C 같은 링크+요구→절·한계](packets/N08/arm-C.md) | [키·값 같은 정렬순열+감소](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py) / [고유키 역색인+원행 선택](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py) | 네 통계와 계산 방법을 제출한다. | 같은 네 통계를 다시 계산하고 불일치가 있으면 원 결정을 지목한다.; [sum](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py#L1314-L1396) / [max/min](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py#L1708-L1832) / [mean](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py#L2235-L2311) | 원키별 틀린 완성 수치는 R3의 대응 수리로 함께 수정; 별도 독립 사건 아님. | 정식 본문 최초 공개; 장기 API 정책 대표성; 역사 NumPy 실행 미확인 |
| N08·전체(작은 흐름) / N08-R3 | 같은 키를 가진 원래 행의 수량만 함께 집계한다. 행 순서가 달라져도 키별 의미와 결과는 유지한다.; [doc2010-04-27·git04-29 / bceb9c20; 첫 공개 미확인](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L79-L95); L23-L38 and L79-L95; 원문에 정렬된 입력 제약 없음 | [A 자유검색](packets/N08/arm-A.md) / [B 링크](packets/N08/arm-B.md) / [C 같은 링크+요구→절·한계](packets/N08/arm-C.md) | [키·값 같은 정렬순열+감소](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py) / [고유키 역색인+원행 선택](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py) | 행과 키의 대응을 유지하는 방법을 설명하고 결과 라벨을 붙인다. | 동일 행 재배열에서 키별 결과를 비교한다. 값의 대응이 바뀐 결정만 같은 원요구 수정으로 분류한다.; [inverse 시험](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/tests/test_arraysetops.py#L11-L35) / [reduce 시험](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/tests/test_ufunc.py#L7-L12) / [정렬 규격](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py#L579-L666) | 키만 정렬한 결정을 키·값 대응 보존으로 변경 | 정식 본문 최초 공개; 장기 API 정책 대표성; 역사 NumPy 실행 미확인 |

| 과제·예시 제출 ID | 군·도구명을 가린 판독 | 기대 판정·근거 URL | 실제 판정 | 불일치·수정 | 외부 사람 검증 여부 |
| --- | --- | --- | --- | --- | --- |
| P02-E1 / S117 | 별도 graph를 두 경로가 호출하고 metadata/wheel 조립만 위임 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/Kitware/CMake/blob/d566bd962df5b1bf0ec5d16e9e7affe592b8b3eb/Help/manual/cmake.1.rst) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P02-E2 / S152 | target/dependency 선언과 native backend·배포 경로 연결 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P02-E3 / S138 | 병렬·배포는 연결하지만 compile monolith를 명시적으로 유지 | fail; R1/R2/R3 fail/pass/pass; [근거](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md) | fail; R1/R2/R3 fail/pass/pass; 중대오류 True | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P04-E1 / S145 | 같은 explicit DMY를 배열 전체에 적용; 불일치는 raise | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P04-E2 / S124 | 각 문자열에 같은 상수 format; 다른 반환타입도 허용 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P04-E3 / S110 | MDY로 시작해 13-01을 DMY로 조용히 바꿈 | fail; R1/R2/R3 fail/fail/fail; [근거](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md) | fail; R1/R2/R3 fail/fail/fail; 중대오류 True | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P06-E1 / S173 | native 생성 schema+lossless 선검사 뒤 실제 쓰기 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P06-E2 / S159 | nullable 생성 schema+기존 strict scalar setter | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| P06-E3 / S187 | dtype은 보존하지만 1.5를1로 절삭해 저장 | fail; R1/R2/R3 pass/pass/fail; [근거](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md) | fail; R1/R2/R3 pass/pass/fail; 중대오류 True | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| N08-E1 / S166 | 같은 순열로 키·값을 정렬한 뒤 그룹 감소 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/add_newdocs.py) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| N08-E2 / S131 | 역색인으로 같은 키의 원행을 선택해 네 통계 | pass; R1/R2/R3 pass/pass/pass; [근거](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py) | pass; R1/R2/R3 pass/pass/pass; 중대오류 False | 없음; 실제 실행 성공/수정 수행은 별도 미확인 | 없음. AI 작성·별도 문맥 AI 판독 |
| N08-E3 / S180 | 키만 정렬하고 원순서 수량의 구간을 감소 | fail; R1/R2/R3 pass/partial/fail; [근거](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py) | fail; R1/R2/R3 pass/pass/fail; 중대오류 True | R2 예상partial / 자기fail / 첫 가림pass. 원키별 완성 출력으로 기준 명료화 후 같은 AI 재독fail. 전체fail 유지; 주 원인1개. | 없음. AI 작성·별도 문맥 AI 판독 |

## 준비도 판정과 관측 범위

**네 과제의 내용 묶음과 판독 장치는 조건부로 준비했다. 최초 공개판의 완전 확인은 N08 한 건이 미충족이며, 사람 시험은 시작하지 않았다.** 첫 표는12개 원요구의 t0/t1 대응, 둘째 표는12개 작성 제출의 최초 가림 판독이다. 표의 pass는 설명·의사코드·작성된 응답의 요구 합치성이다. 사람12명, 실제 재작업12건, 역사적 소프트웨어 실행 성공12건을 뜻하지 않는다.

관측한 것은 파일의 처치 차이, 원요구와 재검의 연결, 작성 예시의 판별과 실제 이견이다. 원격 사전계약 뒤 후보를 선정하고 별도 문맥 판독 전에 기대·입력 해시를 봉인했다. 첫 전체 판정은12/12 기대와 일치했으며, 허용8개 오탈락0/8, 오류4개 오통과0/4였다. 요구별로는35/36이 일치했다. N08의 한 셀은 예상partial·자기fail·별도pass로 갈렸고 원문을 다시 읽어 기준을 명확히 했다. 같은 AI의 대상3개 재독은 새 독립검증이나 사람 합의가 아니다. 최초35/36을36/36으로 소급 고치지 않았다.

| 준비 항목 | 실제 분자/분모 | 판정 범위 |
| --- | --- | --- |
| 내용 과제와 세 보기·두 시점 | 4/4과제·20/20파일 | 전체2(그중 N08은 작은 흐름), 부분2. 형식/내용 검토 가능 |
| 당대 문서 기전으로 방어할 수 있는 두 대안 | 4/4과제 | P06 한 대안은 private helper 기반 작성자 구성; 완성 공식 recipe 두 개라는 더 강한 기준은 충족 주장 안 함 |
| formal 첫판 또는 첫 복구판 직접 열람 | 4/4 | 정식 문서의 최초 공개 이력 완전 확인은3/4; N08 미확인 |
| 고유 외부 원문 최소수 | 33/24 | 접근 실패·미러·재인용·중복 제외. 원장107행과 고유원문33개를 구분 |
| 첫 가림 판독 | 전체12/12·요구35/36 | 같은 모델 계열의 별도 AI 문맥. 외부 사람 검증0 |
| 상태 분류 예시 | 규칙12/12·별도 의미 판독12/12 | 측정 초안 작성 문맥이 남은 AI의 의미 검토; 사람 신뢰도 아님 |
| 실제 역사 환경 실행 | 0/4과제 | N08 유한 산술/의사코드 점검만 수행. P04/P06 재현 driver는 구문 점검만 |
| 사람 시험 개시 | 0회·사람0명 | run-config 미합의; 모집/연락/배정/시간/효과 추정 미실시 |

`evidence/acceptance-evidence.json`은 내용 수용과 마지막 원격 재독·세션 검사·별도 인계 커밋 절차를 나누어 기록한다. 종료 절차의 고정 SHA와 재개 행동은 마지막 `HANDOFF.md`에서 확인한다.

## 1. 표집·원판·출처 집계

SCOPE는 계획 SHA922bf317…와 실제 배정 de544231…를 분리하고, PDEP1~20 뒤 NEP1~20의 번호순, 생성일2007~2025, 최대각20, NumPy 최소1자리, 전체2/부분2를 사전 고정했다. 후보40행은40개를 모두 정독했다는 뜻이 아니다. PDEP8~18 등 할당 뒤 후보는 미심사로 남겼고 결번/접근 실패도 삭제하지 않았다. 현행 상태·후속 제목이 보인 점을 남겼으므로 완전한 후대결과 가림 표집이라고 하지 않는다. 실제 후속 수정 발견을 선정 점수로 쓰지 않았다. 선택하지 않은 PDEP3/5는 두 번째 정답으로 보이는 관행을 넣으면 원 목적을 잃었고, PDEP7은 이관 전 첫 본문 복구가 부족했다. 근거는 `frame.csv`와 각 stream의 최초 봉인·read-notes다.

모든 산입 자료는 원문 본문/관련 절을 직접 열었다. 검색 결과나 다운로드만 한 자료는 최소수에서 뺐다. 필수14키에 URL·판·작성/사건일·확인UTC·위치·검증내용·한계·Q/과제·중복군을 남겼다. 원격 자료③b 전에 P-S14를 보수적으로 제외해 최초 합계34에서 최종33으로 고쳤다. PDEP/날짜 시험 개정이 담긴 merge를 별도 원문으로 다시 세지 않기 위해서이며 그 후속 내용 판독은 남아 있다. `REVISIONS.md` R09와 `evidence/source-summary.json`이 변경 분모를 보존한다.

| 역할 | 최소 | 최종 산입 | 확인 범위·한계 |
| --- | --- | --- | --- |
| 최초 formal 제안/첫 복구 문서 | 4 | 4 | P-S01~03, N-S01; N08 최초 공개시각은 미확인 |
| 당시 대안별 공식 명세/기전 | 8 | 9 | P-S04~09, N-S02~04; 내부 helper와 완성 recipe 구별 |
| 상세 기준/공개 시험 | 4 | 5 | P-S10~12, N-S05~06; 구성요소 시험을 종단간 구매 시험으로 부르지 않음 |
| 후속 결정/재검 기록 | 4 | 4 | P-S13, P-S15, N-S07~08; 안정 댓글앵커지만 본문은 편집 가능 |
| 디자인·교육 사람 방법 원문 | 4 | 6 | 디자인3·교육3. 기존034의5개는 해당 쪽 재독 |
| 추가 공개 POC·backend·생성/병렬 근거 | — | 5 | P-X01~05. 핵심 최소24 증인에 없어도 각 역할 충족 |

역할에 서로 다른 원문을 배정한24개 목록은 `streams/numpy/source-audit.json`의 `disjoint_24_source_witness`에 있다. 이 감사는 원 stream101행/34개 시점이며 최종 통합107행/33개 집계는 `evidence/source-summary.json`이다. 댓글3개의 내용 불변 snapshot, ME03의 바이트 해시는 미확인이다. 출처 위치의 안정성과 내용 불변성·기관 독립성은 같은 속성이 아니다.

## 2. 실제 배포 자료와 처치 차이

배포자는 `distribution.json` 목록에 따라 t0+배정된 arm 하나만 전달하고 공통 시점에 t1을 전달한다. 공개 저장소 전체를 주면 정답·루브릭이 노출된다. 참가자 t0/t1에는 답안·후속 결정 링크가 없으며 B/C의 본래 근거 링크는 유지했다. 모든 arm의 검색·도구·교육·지원·예산 규칙은 공통이다. 숫자 예산과 재검 간격은 임의로 넣지 않고 후속 실행 설정에서 결정할 항목으로 남겼다.

| 과제 | B/C 링크 개수 | B 본문 문자 | C 본문 문자 | 추가 문자 | 검사 |
| --- | --- | --- | --- | --- | --- |
| P02 | 3 | 482 | 946 | 464 | URL·순서·판 동일; 설명 문단 외 동일 |
| P04 | 2 | 387 | 759 | 372 | URL·순서·판 동일; 설명 문단 외 동일 |
| P06 | 3 | 544 | 989 | 445 | URL·순서·판 동일; 설명 문단 외 동일 |
| N08 | 3 | 465 | 767 | 302 | URL·순서·판 동일; 설명 문단 외 동일 |

문자수는 UTF-8로 저장한 전체 Markdown을 Unicode 문자 기준으로 센 값이며 끝 줄바꿈을 포함한다. C의 추가 길이를 B에 filler로 맞추지 않았다. 원문 링크11개는 같은 URL을 인증·쿠키 없이 열어HTTP200을 확인했다. 이는 해당 시점 접근 증거이며 이후 가용성이나 이해를 보증하지 않는다.

A↔B는 선별·제공시점·제목·순서가 묶인 비교다. B↔C는 같은 URL·판·순위 위의 설명 추가이며 의미·읽기 부담·추천으로 받아들이는 정도가 함께 달라진다. A↔C는 전체 제공이다. 이 세 보기만으로 링크 선정 알고리즘의 순수 효과, 설명 의미와 글자 수의 각각 효과, 두 요소의 상호작용을 분리하지 못한다. P02의 세 번째 backend 링크가 한쪽 대안에 더 직접 연결되는 것도 B/C 공통 선별 특성이다.

## 3. 네 과제의 방어 가능한 대안과 원요구 재검

### P02 — native build·배포 경계 전체

[첫 formal PDEP](https://github.com/pandas-dev/pandas/blob/aad11f695cacd7a07a35f4e31b8e0d1fc9a2767f/web/pandas/pdeps/0002-build-system-overhaul.md) L10–32는 compile monolith, 개발/일반 source 설치의 병렬화, 두 native build 후보를 함께 제시한다. [CMake POC](https://github.com/pandas-dev/pandas/blob/d62f894c3ec08b721de0499cabe2c58a6e322496/build_support/build_backend.py)는 별도 graph로 컴파일한 뒤 metadata/wheel 조립을 기존 도구에 위임한다. [Meson Python module](https://github.com/mesonbuild/meson/blob/9c6dab2cfd310ef2d840a2a7a479ce6b9e563b1d/docs/markdown/Python-module.md)과 [당대 backend](https://github.com/mesonbuild/meson-python/blob/2f9acf25e23de95b0ceead72770cad4acf19a449/README.md)도 다른 연결 설계를 지지한다. 패키징 위임에 특정 이름이 남았다는 이유로 탈락시키지 않는다.

첫 제출은 graph·개발명령·frontend/backend·wheel/sdist 입력의 경계와 worker 전달을 보여준다. 재검은 같은 구조를 clean source archive 경로까지 추적한다. target 하나 추가 가정은 기존 표현 경계의 질문이며 실제 새 기능 구현이 아니다. 파일 이름/개수로 구조 분리를 대신 채점하던 위험을 공통 문구에서 고쳤다. 잘못된 예시는 병렬과 패키징 계약은 갖추지만 compile graph를 분리하지 않는다.

두 설계의 문서 합치성과 실제 historical pandas 빌드 성공을 구분한다. Meson POC의 @main 전이 의존을 실제 당시 commit으로 닫지 못했다. 후대 editable 자동 rebuild는 원요구가 아니다. 실제 실행 명령을 서둘러 성공으로 표시하지 않고 `streams/pandas/execution-next.md`에 의존 잠금 확인을 첫 행동으로 남겼다.

### P04 — batch 날짜 파싱 부분 선택

[원 PDEP](https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md) Abstract·Detailed Description은 explicit format 또는 첫 non-NaN에서 한 번 정한 format을 batch 전체에 유지하도록 한다. [당대 배열 파서](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py)의 format/exact와 [당대 표준 datetime](https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst)의 strptime은 서로 다른 구현·반환타입으로 같은 계약을 충족할 수 있다.

고정 예시 두 정답은 explicit DMY지만 이 형식을 모든 참가자에게 정답으로 강요하지 않는다. t1 입력1은12-01/13-01, 입력2는12-01/01-13이다. DMY는 첫 batch를 정상 파싱하고 두 번째의 month13에서 오류를 낸다. first-row MDY를 고정한 대안은 첫 batch의13-01에서 오류를 내도 옳다. 첫 batch의12-01을12월1일,13-01을1월13일로 조용히 반환하는 fallback이 잘못된 예시다. 성공 날짜 개수 대신 선언 모드·format_used·오류 정책을 본다.

후대 mixed/ISO8601 지원을 재검의 필수조건으로 더하지 않았다. 입력은year2000 naive datetime으로 한정했고 시간대·locale·범위·성능은 비교하지 않았다. infer-once strict 대안은 허용 기준에 있으나 봉인12개에는 별도 네 번째 예시로 넣지 않았다. 향후 API 재현 driver에는 해당 반례를 포함했으며 아직 실행하지 않았다.

### P06 — 생성 때 정한 dtype을 지키는 scalar 편집

[formal 첫 PDEP](https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md)의 dtype 불변·호환성·fractional 선택과 [lossless helper](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py) L1931–2009, [nullable scalar setter](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py) L198–235를 연결했다. 2021의 앞선 아이디어에서 fractional 처리까지 이미 합의됐다고 소급하지 않았다.

처음 만들 때 native int64 또는 nullable Int64를 선택할 수 있고, 그 뒤에는 선언 dtype이 계약이다. 기존 native 컨테이너를 사후에 nullable로 갈아 끼우는 답은 다르다. native setter 앞의 lossless guard는 내부 공식 기전을 근거로 작성자가 구성한 소비자 설계다. nullable 대안은 생성 schema를 선언하고 기존 strict scalar setter를 쓴다. 공개된 완성 consumer recipe 두 개를 실증한 것으로 확대하지 않는다.

t0의4/2.0과 t1의3.0/1.5/text는 같은 scalar 호환성 요구다. 각 t1 probe는[1,2,3]의 독립 초기 상태에서 시작한다. 3.0은 손실 없이 저장하고1.5/text는 쓰기 전 오류와 원값/dtype 보존을 보여야 한다. 잘못된 예시는1.5를1로 잘라 dtype은 보존하지만 값을 잃는다. NaN·overflow·bool·vector를 새 필수조건으로 넣지 않았다. JSON이 whole float를 정수처럼 표시할 위험 때문에 literal과 type을 따로 보존했다.

### N08 — 작은 구매집계 흐름 전체

[첫 복구 formal NEP](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst) L23–38의 구매 필드와 SKU·월·점포별 max/min/mean/sum을 과제로 삼았다. [unique 역색인](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/lib/arraysetops.py) L95–181, [reduction 계약](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/add_newdocs.py), [정렬/통계 함수](https://github.com/numpy/numpy/blob/4b42c8f6b81d87f35ed8dcf4430224992cf2d296/numpy/core/fromnumeric.py)가 두 기전의 당시 근거다. 전체는 이 작은 흐름을 뜻하며 새 ufunc/API 정책 전체나 장기 아키텍처를 뜻하지 않는다.

t1은t0의 같은6행 순서만 바꾼다. by month의 연도경계가 원문에 명시되지 않아 단일년으로 고정하고 month와(year,month)를 모두 허용했다. 키와 수량에 같은 정렬 순열을 쓰는 흐름과 역색인으로 원행을 고르는 흐름은 둘 다 원키별 숫자를 보존한다. SKU AA는수량[2,4,10]의sum16·mean16/3, BB는sum14·mean7, CC는3이며 월/점포까지7그룹×4통계=28셀이다.

작성자 산술 점검에서 두 적격 절차는 각 시점28/28셀 일치했고, 키만 정렬한 오류 절차는t0 17/28·t1 24/28셀이 달랐다. 별도 문맥 판독자도 입력으로 원키별 숫자를 다시 계산했다. 이것은 역사적 NumPy 실행이나 사람 성과가 아니다. 오류의 주 원인은 키-값 대응 파괴 하나이고, 여러 통계/요구의 실패를 여러 수정사건으로 늘리지 않는다.

N08-R2의 옛 pass 문구인 선택된 값에 대한 산술은 잘못 고른 slice에도 성립했다. 최초 판독은 이를R2 pass/R3 fail로 읽었다. 원문이 요구하는 원키별 완성 출력을 명시한 뒤 같은 판독자는R2 fail로 바꿨다. 자료·의사코드·전체fail은 그대로이며 점수 적용 범위의 사후 명료화다. 원본 입력·루브릭·기대/자기/첫 가림 판독·명료화 입력·재독을 각각 저장했다.

## 4. 채점·가림의 한계와 실제 정정

과제별 필수조건은pass/partial/fail/unverified, 중대오류는 별도다. 모든 필수조건pass와 중대오류 없음이어야 전체pass다. 다른 제품 이름·표현·반환타입·추정 속도는 기준이 아니다. 등록하지 않은 대안도 원요구와 근거를 충족하면 받아들인다. 중복된 요구 셀은 독립 사례나 독립 오류 수가 아니다.

예시 작성자 기대와 root의 자기 판독은 공개된 source/key를 알고 있다. 첫 별도 AI 문맥은 프로토콜v1만 미리 알고 익명 입력 하나를 읽었다. 정책·제품·군·예상 분포는 주지 않았다. 가림은 지시와 입력 분리이며 OS 접근권한으로 강제한 격리가 아니다. 별도 판독자는 실제 역사 소프트웨어나 외부 원문을 직접 재검하지 않았다. 같은 모델 계열·작은 고정 예시의 일치를 사람 간 신뢰도나 오류율로 계산하지 않았다.

원격 봉인에서 최초CSV의 로컬CRLF가 전송 중LF가 된 점도 확인했다.13개 줄바꿈뿐이고12행의 모든 필드는 같았다. 가림 입력JSON과 기대JSON은 원래 바이트 해시와 일치한다. 원 해시를 지우지 않고 `evidence/transport-normalization.json`에 로컬/원격 해시와 비교를 남겼으며 이후CSV는LF로 저장했다.

## 5. 조기 종료·결측·새 요구를 구별하는 원자료

`forms/`에는 배정·노출·활동·제출·결정·품질·수정·제공자비용·조정·일탈·시각사건의 빈CSV11개와 미합의 run-config를 둔다. t0는 첫 채택 선언과 제출판 해시이며 품질 통과와 다르다. 첫 기록된 성공은 보존된 제출이 공통 루브릭을 통과한 최초 제출시각이고 채점시각은 별도다. 머릿속 해법 획득시각이나 미관측된 더 이른 성공을 만들지 않는다.

원요구 수정은 첫t0선언 이후부터 센다. 최초 프로토콜이t1뒤만으로 좁게 읽힐 위험을 별도 문맥 검토에서 발견했고, t0와t1 사이 작업도 기록하게 고쳤다. t1은 모든 배정자에게t0과제 표시부터 같은 사전 간격으로 제공한다. 초기 미채택자도 동의를 유지하면 재검을 받으며 그때의 최초 완성은 초기작업 계속이지 채택 후 재작업이 아니다.

상태 fixture12개는 작성 예시다. 원본10개와 정정 이유를 보존했고 모든 실제 노동·시각은null이다. 기대 코드와 규칙 출력12/12, 기대를 보지 않은 다른 작업 문맥의 의미 판독12/12를 확인했다. 그 판독자는 측정 초안을 작성한 기억이 있고 입력 품질 표식도 보였으므로 새로운 독립 가림 품질검증이 아니다.

| 작성 상태 | 예시 | 판정 | 분모·계산 한계 |
| --- | --- | --- | --- |
| FX01 | 채택 없이 탐색을 중단한 작성 예시. 최종 제출/정답 증거 없음. 최초 채택 후 사건을 만들 수 없음. | pre_adoption_abandonment | 해당 없음; 실제 노동null |
| FX02 | t0에 explicit DMY 설계를 선언했으나 t1 제출·활동이 없음. 알 수 없는 재검을 무수정0으로 대체하지 않음. | followup_missing | 미확인; 실제 노동null |
| FX03 | E3의 t0 inference를 그대로 유지. t1 12-01→Dec1,13-01→Jan13으로 조용히 형식을 바꾼 채 성공이라고 제출. | retained_incorrect | 0사건; 품질실패; 실제 노동null |
| FX04 | E2 생성 schema 유지. t1 3.0은 저장,1.5/text는 쓰기 전 오류. 변경 없이 같은 요구 통과. | retained_correct | 0사건; 수정불필요; 실제 노동null |
| FX05 | t0 E2의 finite scalar 계약은 맞음. t0 뒤 새로 요청됐다고 가정한 NA 저장 기능만 추가. 기존 오류를 수리한 사건이 아님. | new_requirement_excluded | 예방가능 재작업 제외; 실제 노동null |
| FX06 | t0 E3 키만 정렬을 채택. t0 선언 뒤 t1 제공 전에 키와 수량에 같은 순열을 적용하는 E1으로 바꿈. 같은 원행 소속 요구를 고침. | original_requirement_repair | 원요구 수정사건; 실제 노동null |
| FX07 | 의도적으로 틀린 카드 문구를 작성: 이 판의 infer_datetime_format=True만 켜면 batch의 모든 행에 한 형식이 엄격히 유지된다. E3의 Dec1/Jan13 반례로 카드가 틀림을 확인한 뒤 E1처럼 explicit format으로 바꾸었다고 가정. 실제 참가자 유도 관측은 아님. | card_error_repair | 원요구 수정+제공자오류; 실제 노동null |
| FX08 | 두 개의 허용 설계 E1/E2를 각각 같은 행 재배열로 재검. 둘 다 원키별 동일 숫자이고 설계 변경 없음. 0수정은 노동0이 아님. | retained_correct | 두 허용대안 모두 0사건; 차이없음; 실제 노동null |
| FX09 | E3에서 E1으로 바뀐 두 제출판과 동일 원행 소속 위반은 확인. 수정 활동 구간은 누락되어 사건만 확인 가능. | original_requirement_repair | 사건 확인; 노동 미확인; 실제 노동null |
| FX10 | fractional 절삭 오류 E3를 guard로 고치면서 새로 요청된 NA 기능을 함께 구현했다는 작성 예시. 두 변경의 실제 노동구간 분리 근거 없음. | mixed_unseparable | 사건은 원요구+새요구; 노동분해 미확인; 실제 노동null |
| FX11 | t0 설계 채택 후 t1 제출은 있고 변경 없음. 제출에 source archive의 필수 graph/source 포함 여부가 없어 최종 요구통과를 판독할 수 없다. 실제 실패를 확인한 증거도 없다. | retained_unverified | 전원 포함; 품질 미확인, 실패로 채우지 않음; 실제 노동null |
| FX12 | t0 상한까지 최초 채택을 선언하지 않았다. 공통 t1을 제공받은 뒤 처음으로 explicit 형식의 맞는 제출을 완성했다. 되돌릴 t0 채택 결정은 없다. | initial_work_continuation | 전원 최종품질/총노동 포함; t0채택자 재작업 해당없음; 실제 노동null |

전원 최종품질은 통과수/배정수, 중대오류/배정수, 품질미확인/배정수를 함께 보고한다. 결측을 성공·실패로 임의 채우지 않고 가능한 통과율 경계를 제시한다. 전원 총 소비 노동은 실제 활동초의 배정 단위 평균이며 팀이면 구성원 노동을 합친다. 경과시간·CPU·build시간·commit 간격은 사람 노동이 아니다. 완료자 시간과t0채택자 수정 노동은 별도 조건부 분모이며 전원 인과효과로 읽지 않는다.

원요구를 고치며 버린 초기 구현 노동은 이미t0노동이므로 수리시간에 다시 더하지 않는다. 새 요구 기능추가는 예방 가능 재작업에서 제외해도 전체 소비 노동에는 남긴다. 오연결 카드는 처치 오류와 원요구 수리를 함께 태그하되 사건/노동을 이중 합산하지 않는다. 노동 누락은0이 아니며 사전 유한 상한을 못 만들면 전원 노동 감소 판정을 보류한다. 제공자 준비·판확인·검수·정정·유지는 별도 기록하고 실제 사용 횟수가 없으면 비용을 상각하지 않는다.

## 6. 두 분야의 원 실험에서 가져온 반례

아래는 실험의 자극·과제·채점법을 직접 읽고 설계에 옮긴 범위다. 사람 효과 크기·표본수 계산을 재수행하거나 AF038의 시간으로 바꾸지 않았다.

| 분야/원문 | 직접 위치 | 확인한 자극·채점 | 현재 과제의 반증/한계 |
| --- | --- | --- | --- |
| MD01·디자인 | [Chan2011](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) §§3–4·Table2 | 발전기 발상에 특허의 거리/흔함/그림·글; 기능 적합성·특징 전이·참신성·품질 분리 | 카드와 닮은 선택이 정답이라는 보장 없음. 근거 채택과 원요구 통과를 따로 기록 |
| MD02·디자인 | [Fu2013](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/md_135_2_021007.pdf) §§3–4 | 특허 공간 거리와 발상 단계, 최선 아이디어 품질; 신뢰도 낮은 평가차원 제외 | 최선 아이디어만으로 전원 결과를 대신하지 않음. 실제 채점 경계 이견을 보존 |
| MD05·디자인 | [Vasconcelos2016](https://api.repository.cam.ac.uk/server/api/core/bitstreams/6cd62cf5-a602-48f2-95ed-38a9f61f5644/content) pp5–8 | 같은 자전거 그림의 사용지시 변경, 다른 해법도 코딩, 공동 논의 후 분담채점 | 한 줄 설명도 추천·주의를 바꿀 수 있음. 공동 논의와 독립 일치도는 다름 |
| ME01·교육 | [McLaren2016](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf) §2·Table2 | 화학량론의 완성/오류 예제·도움/독립풀이와 공통검사 | 완성답 제공 효과는 근거 절 한 줄과 다름. 학습·읽기·도움 부담을 포함 |
| ME02·교육 | [Wesenberg2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1032003/full) Methods·Results | 맞고 틀린 수학 예제 순서·문제 일치 조작, 개념 오류와 단계별 채점 | 체감 용이성과 정답은 다름. 같은 세션 지연검사는 소프트웨어 유지보수 아님 |
| ME03·교육 | [Reisslein2006](https://faculty.engineering.asu.edu/sites/g/files/litvpz5806/files//2020/02/Exp_Rev_LI06.pdf) pp94–97/99–102 | 사전 내용지식 층, near/far 구조의 단계점수; 지식×순서 양상이 전이범위마다 다름 | 경력 연수만으로 사전지식을 대신하지 않음. 단순 구현의 결과를 장기 설계에 옮기지 않음 |

초보는 근거 위치로 도움을 받을 수도 있지만 권위 있는 잘못된 문구를 그대로 따를 수 있다. 숙련자나 이미 해법을 아는 사람에게 설명은 추가 읽기일 수 있다. 카드 작성자는 검색·선정·판 잠금·상충 근거 검수, 유지자는 변경 확인·정정을 맡는다. 조건을 모르는 채점자는 익숙하지 않은 대안을 읽는 비용을 부담한다. 이들은 관측된 사람 효과가 아니라 별도로 측정할 가설이다. 과제별로 P02의 이름만 보고 경로 누락, P04의 silent fallback, P06의 dtype만 보고 값 손실 누락, N08의 함수 이름만 복사하고 원행 대응 누락을 오류 관측항목으로 정했다.

## 7. 후속 사람 시험에서 지지·기각할 결과

한 사람 한 과제 한 보기의 병렬 배정이 기본이며 공동작업은 팀을 단위로 한다. 과제·사전 내용지식·동일 해법 인지를 처치 전에 기록하고 사전 지정 층에서 무작위 배정한다. 사전문항이 답을 가르치지 않도록 별도 검토해야 한다. 공유가 생기면 일탈/오염으로 남기고 사후 제외로 유리한 군을 만들지 않는다. 참가자/제공자는 보기 차이를 알 수 있고 품질 채점자만 가린다. 사람 두 명이 먼저 독립 판정한 뒤 제3조정자가 원문으로 불일치를 다룬다는 계획이며 이번에는 실시하지 않았다.

| 가설/대비 | 지지에 필요한 관측 | 반대·판별불충분 결과 | 현재 필요한 원자료/미확인 |
| --- | --- | --- | --- |
| 선별·제공 B–A | 사전 품질 기준을 지키면서 전원 총 소비 노동이 사전 실질 차이를 만족 | 찾기만 빨라지고 총노동 동일/증가, 품질 악화, 넓은 불확실성 | 배정·노출·최종품질·전체 활동; 경계/표본/사람 자료 없음 |
| 설명 추가 C–B | 같은 URL·판·순위에서 설명과 읽기 부담을 합친 결과가 기준 만족 | 추가 읽기 비용, 권고 고착, 오연결·비주류 불이익 | 설명노출/읽기·원요구별 결과·결측; 의미와 길이의 개별 효과 불가 |
| 채택 뒤 원요구 수정 | 전원 품질·총노동을 지키며 원결정 되돌림/수리 노동 감소 | 틀린 선택 유지로0수정, 채택자만 선택, 새 기능 노동 차이뿐 | t0해시·원요구·변경판·실제 구간; 채택자 조건부 인과효과 미확인 |
| 전체 제공 C–A | 소비자뿐 아니라 준비·검수·유지까지 합친 사전 기준 만족 | 독자 이득보다 제공자 비용 큼 | 실제 제공자 노동·사용자 수 없음; 상각/손익분기 불가 |

두 올바른 대안이t1에서 전부 그대로이면 원요구 검사를 통과한 유효한 결과다. 그 표본에서는 수정 차이를 식별할 사건이 없고 예방 효과를 주장할 수 없다. 이를 이유로 사후에 새 조건/난도를 더하지 않는다. 카드가 틀린 FX07도 원래 배정 결과와 제공자 정정 노동에 남는다. 결측 범위에 따라 결론이 뒤집히면 노동 절약/동등 품질을 확정하지 않는다.

`forms/run-config.json`에는 예산·간격·훈련·도구·지원·모집·동의/보상·할당은폐·표본수·중단·품질 허용열화·중대오류 허용경계·최소 노동차이·추정법·다중비교가 미합의로 남았다. 034의7일·90/60분을 채택하지 않았다. 이 값을 사전에 고정하기 전에는 실제 사람 시험을 시작할 수 없다. 현재 사람 배정N=0이므로 사람 품질률/수정효과는 해당 없음, 실제 노동은 미확인이다.

## 8. 검증 파일과 실행 경계

직접 원문 판독, 실제20파일 대조, 익명12개 판독, N08 유한 산술, 상태12개 규칙/의미 판독을 수행했다. `evidence/check_materials.py`, `evidence/check_measurement.py`의 실행 출력은 해당JSON에 남았다. 별도 원문 감사와 참가자 문구 감사도 출처·조건 누출·반례의 제한을 남겼다. Python driver는AST 구문만 확인했으며 pandas/NumPy historical 환경을 설치·실행하지 않았다. `streams/pandas/execution-next.md`는 재현 환경·typed 입력·expected-failure 대조·실제 잠금 필요사항을 명시한다.

최종 Q별 지지·반증·뒤집힐 조건은 `SELF_CHECK.md`에, 수용 조건별 파일·행/분자·분모는 `evidence/acceptance-evidence.json`에 있다. 결과/수용 파일의 원격 고정판 재독과 요청된 session check 출력은 종료 단계에서 추가하고, 그 뒤 마지막 별도커밋으로 HANDOFF를 작성한다.

## 우선순위를 유지할 약점 세 가지

| 중요한 불일치·약점 | 영향받는 결론 | 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 1. N08 정식 본문의 절대 최초 공개 미확인 | 최초판 완전 확인3/4;4과제 무조건 적격이라는 결론 불가 | [4/10 사전논의](https://mail.python.org/pipermail/numpy-discussion/2010-April/049846.html) 본문 first proposal 이전 의견수집; [formal 본문](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst) L23–38 | 공식4월 archive와 git추가 직전 제출 맥락에서 구매 schema를 포함한 최초 게시판을 찾고 현재판과 대조. 첫 자료는4/10 원 저자 메일과4/27~30 mbox 검색 기록. | 더 이른 같은 문서에서 요구/대안이 다르거나 이관 내용이 바뀌면 N08 적격·t1 기준을 다시 정함 |
| 2. 작성 예시의 한 요구가 실제로 갈렸고 외부 사람 채점 없음 | 전체 판별12/12는 사람 채점 신뢰도 증명 아님; 요구셀 첫 일치35/36 | [원키별 통계 원문](https://github.com/numpy/numpy/blob/bceb9c20700514db5667831ce2878f1660fb071f/doc/neps/groupby_additions.rst#L23-L38); evidence/blind-observed.json S180 R2; rubric-before-adjudication.csv N08-R2 | 명료화한 rubric와 익명12개를 서로 판정을 보지 않는 사람 두 명에게 후속 검토. 첫 자료는 blind-input.json과 명료화 기준; 첫 이견은 그대로 제공자 기록에 유지. | 유효한 대안 오탈락/오답 오통과 또는 원요구를 바꿨다는 판독이 남으면 채점 준비도 철회 |
| 3. 사람·역사 실행·장기 설계/제공 비용의 관측 부재 | 링크/설명 효과, 노동 절약, 장기 재작업 예방은 현재 계산 불가 | [지식/전이 방법](https://faculty.engineering.asu.edu/sites/g/files/litvpz5806/files//2020/02/Exp_Rev_LI06.pdf) pp94–97/99–102; measurement.md §§4–8; forms/run-config.json | 먼저 P02 의존 잠금·P04/P06 typed 계약 재현과 사람 시험 설정을 고정. 첫 자료는 execution-next.md 및 run-config의 null 항목. 제공자 활동도 함께 기록. | 실행이 두 대안의 원계약을 깨거나 전원 품질·총노동/제공비용 기준을 못 지키면 효율 가설 기각·범위 축소 |

