# Q7 · 다음 조작에 따라 달라지는 대체 가능성

## 읽은 판과 판독의 성격

LibreOffice는 `libreoffice-24.2.7.2`의 core `ee3885777aa7032db5a9b65deec9457448a91162`, help `79e75f7a043646862051e6e0621f336b24d3aa04`를 고정했다. 두 태그 시각은 2024-10-29 11:14:39 UTC다. Arrow는 `apache-arrow-18.1.0`의 commit `6a0414bd9a91e890ec6a45369bf61f405180628c`다. 18.1.0 태그는 2024-11-24 18:48:14 UTC에 rc2 태그를 가리키며, rc2는 2024-11-13 21:34:10 UTC에 이 commit을 가리킨다. 태그 시각은 각 파일의 최초 발행일이 아니다.

아래에서 **원 시험**은 유지관리자 저장소에 있는 입력·assertion을 직접 읽었다는 뜻이다. 이 연구에서 Calc·Arrow를 빌드하거나 원 시험을 실행하지 않았다. **추론**과 **제안 입력**은 실제 실행 결과와 구별했다. 새 Inkscape·Pillow 여섯 건의 정답 분모에는 전혀 넣지 않는다.

## 대조표

| 분야·목적 | 두 선택과 다음 소비자 | 원 자료의 입력·기대값 | 판정 및 조건 | 틀리는 입력·미확인 |
|---|---|---|---|---|
| Calc: 지금 표시할 숫자만 복사 | `.uno:PasteOnlyValue` / `.uno:PasteOnlyFormula`; 소비자는 `getString()`·`getValue()` | **원 시험 CD-C03:** A1=`=SUM(A2:A3)`, 다른 셀은 빈 상태. D1에 값 붙여넣기와 E1에 수식 붙여넣기 모두 문자열 `0`, 숫자 0. E1의 수식은 `=SUM(E2:E3)`로 이동. | **조건부 묶음(연구자 판정):** 이 입력에서 지금 표시된 숫자만 읽고 후속 변경·수식 노출을 요구하지 않을 때 두 선택 모두 충분. | 상대 참조의 목적지가 달라지면 이후 값은 달라질 수 있다. D1의 `getFormula()` assertion과 후속 입력 변경은 이 원 시험에 없다. 화면 출력이 같았다는 결과를 수식 보존까지 넓힐 수 없다. |
| Calc: 다음 재계산에도 의존 관계 유지 | 위 두 선택; 다음 소비자는 참조 셀 변경 뒤 계산된 값 또는 수식 문자열 | **공식 도움말 CD-C01/C02:** 값 전용과 수식 선택을 별개로 제공하고 CalculateHard는 모든 수식 셀을 재계산한다. **원 회귀 CD-C04:** A1=100, A2=1, A3=`=A2`에 산술 추가 붙여넣기 뒤 101·`=(A2)+100`; A2=2로 바꾸면 102를 기대. 버그가 있던 경로는 101에 머물렀다고 시험 주석에 명시. 범위 대조에서 상수 셀은 1100 유지, 참조 셀은 101→102. | **분리(설계 제안):** 숫자 스냅샷 보존과 이후 계산 관계 보존은 다른 목적이다. 수식이 필요하면 수식 경로와 참조 이동 조건을 함께 반환. | C03의 값/수식 두 가지 붙여넣기를 동일 참조값 변경까지 잇는 단일 원 시험은 찾지 못했다. C04는 산술 추가 회귀이며 C03의 양쪽 후속 정답을 직접 주지 않는다. 동작 원리는 지지하지만 여섯 건의 독립 정답으로 재활용하지 않는다. |
| Arrow: 재배열 뒤 표시할 논리값 | 원 dictionary array / `DictionaryArray::Transpose`; 소비자는 dictionary를 통해 해석한 논리 문자열 | **원 시험 CD-A02 TransposeBasic:** dictionary `[A,B,C]`, indices `[1,2,0,0]` → 새 dictionary `[Z,A,C,B]`, map `[1,3,2]`, 기대 indices `[3,2,1,1]`. 두 표현의 문자열은 모두 `[B,C,A,A]`라는 **명세를 적용한 계산**. | **조건부 묶음(연구자 판정):** 매번 해당 dictionary를 참조해 논리값만 읽는 소비자. index 정수 또는 buffer 동일성을 요구하지 않는 경우. | 원 시험은 transposed 배열과 기대 dictionary-array의 동등성을 검사한다. 원 배열과 새 배열의 논리 문자열을 별도 decode해서 직접 비교한 assertion은 이 함수에 없다. 명세와 입력으로 산출한 해석임을 표시했다. |
| Arrow: 원 index로 후속 선택 | 위 동일 두 표현; 소비자는 `indices()` 또는 `GetValueIndex(i)` | **원 시험 CD-A02:** 전 indices `[1,2,0,0]`, 후 `[3,2,1,1]`. `GetValueIndex` 시험은 index 숫자 자체와 비교하며 slice offset도 검사. **구현 CD-A03:** `GetValueIndex`는 index buffer에서 읽는다. | **분리:** 소비자가 예전 index=0인 행을 고르는 계약이라면 앞에서는 행 2·3, 뒤에서는 없음이다. 행 번호는 0부터 세며 이 선택 집합은 원 벡터에 연구자가 적용한 술어다. | index를 외부 영구 ID로 약속했는지는 Arrow 명세만으로 알 수 없다. 실제 사용자 의도에 없으면 임의로 그 보존 요구를 추가하면 안 된다. |
| Arrow: 기존 index를 유지하는 확장 | 원 배열 / identity map의 `Transpose`; 다음 소비자는 논리값과 index 숫자 | **원 시험 CD-A02 TransposeTrivial:** `[A,B,C]`에 D만 덧붙인 dictionary, map `[0,1,2]`, indices `[1,2,0,0]` 유지. 같은 index type이면 **구현 CD-A03**은 기존 buffer를 재사용하는 경로. | **묶음 가능한 반례:** 다음 조작 필드를 채웠어도 기존 원소의 값·index가 모두 같은 입력에서는 분리할 이유가 늘지 않는다. | index type을 int16→int8로 바꾸는 시험에서는 숫자는 같아도 raw bytes 계약은 다르다. 전체 dictionary 목록까지 소비하면 D 추가 자체가 관찰된다. |
| Arrow: 원 index가 사라진 뒤 복원 | decoded 논리값 / 원 표현 복구; 소비자는 과거 index 또는 원 dictionary 위치 | **명세 CD-A01:** dictionary의 중복값·null을 허용한다. 예시에서 `foo`가 서로 다른 dictionary slot에 놓일 수 있다. | **유보/복구 불가(연구자 추론):** decode된 값만 남고 원 dictionary와 map·index를 버렸다면 동일한 `foo`에서 원 slot을 일반적으로 복원할 수 없다. 추가 설명 필드는 이미 잃은 데이터를 생성하지 못한다. | 원 dictionary, provenance map, 별도 ID가 남아 있으면 복원 가능성이 달라진다. 영구 정보 소실을 주장하려면 무엇이 실제로 삭제됐는지 관측해야 한다. |

## 실제로 반환할 링크

| 사용자 목적 | 링크와 한 줄 이유 | 한 번만 물을 질문 또는 바로 답하는 근거 |
|---|---|---|
| Calc 숫자를 현재 값으로 고정 | [CD-C01 Paste Special · Values Only](https://github.com/LibreOffice/help/blob/79e75f7a043646862051e6e0621f336b24d3aa04/source/text/shared/01/02070000.xhp#L64-L97), [CD-C03 실제 값/수식 대조](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/uitest/calc_tests/CalcPasteOnly.py#L17-L39) · 현재 수치와 수식 보존을 구분하는 공식 명령과 원 기대값. | 목적이 ‘값으로 고정’이라고 주어지면 다시 묻지 않는다. ‘복사’만 있으면 “붙여넣은 셀이 참조하는 값을 바꾸면 결과도 다시 계산되어야 하나요?” 예→수식, 아니오→값 전용. |
| Calc 수식을 유지하고 계속 편집 | [CD-C01 Formulas](https://github.com/LibreOffice/help/blob/79e75f7a043646862051e6e0621f336b24d3aa04/source/text/shared/01/02070000.xhp#L95-L97), [CD-C04 다음 계산 회귀](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/unit/ucalc_copypaste.cxx#L10467-L10574) · 수식 문자열이 남았다는 것과 참조 변경 뒤 값이 갱신된다는 것을 따로 검사. | 수식 보존이 명시되어 있으면 그대로 답한다. 상대 참조 이동을 원본 셀 연결과 혼동하지 않는다. |
| Arrow 논리값을 읽거나 dictionary 통합 | [CD-A01 명세](https://arrow.apache.org/docs/18.1/format/Columnar.html#dictionary-encoded-layout), [CD-A02 TransposeBasic/Trivial](https://github.com/apache/arrow/blob/6a0414bd9a91e890ec6a45369bf61f405180628c/cpp/src/arrow/array/array_dict_test.cc#L1177-L1276) · 같은 문자열이 새 index로 표현될 수 있고 identity map에서는 기존 index도 유지됨. | 값만 필요하다고 명시되면 원 index 요구를 새로 만들지 않는다. |
| Arrow index 숫자로 행을 고르거나 외부 label과 조인 | [CD-A03 `GetValueIndex`/`TransposeDictIndices`](https://github.com/apache/arrow/blob/6a0414bd9a91e890ec6a45369bf61f405180628c/cpp/src/arrow/array/array_dict.cc#L54-L76), [CD-A02 기대 index](https://github.com/apache/arrow/blob/6a0414bd9a91e890ec6a45369bf61f405180628c/cpp/src/arrow/array/array_dict_test.cc#L1192-L1322) · raw index를 읽는 API와 index 변경 기대값을 같이 반환. | 소비값이 불명확할 때만 “문자열 값이 같으면 충분한가요, 아니면 이전 index 숫자도 그대로 필요하나요?” 값→명세+Transpose, index→원 index/map 보존 조건과 두 링크. |

## 세 관점의 차이

| 관점 | Calc | Arrow |
|---|---|---|
| 생산자 | 현재 표시 숫자가 같다는 사실을 전달할 수 있지만, 수식·참조 관계 보존까지 보장하려면 별도 확인. | 논리값이 동일한 새 dictionary 표현을 생산할 수 있다. index 안정성은 별도 계약. |
| 편집을 이어갈 사용자 | 참조 셀 변경/재계산 결과가 목적에 맞는지 중요. ‘수식을 보존했다’만으로 stale-cache 회귀를 배제하지 못한다(C04). | dictionary-aware 값 읽기와 raw index 선택이 다른 작업. index type·offset·null도 실제 소비 경로에 따라 중요. |
| 링크 목록 관리자 | ‘붙여넣기’라는 기능명만으로 대표 하나를 남기면 값 고정 또는 수식 보존 목적 하나를 놓칠 수 있다. | Transpose의 이름만 보고 늘 분리하면 identity map 대조의 불필요한 분리를 만든다. 링크 선택은 요구된 관측값에 조건부. |

## 옮길 수 있는 원리와 옮길 수 없는 보장

**연구자 추론:** 링크 병합 단위는 현재 출력이 아니라, 명시된 다음 조작이 읽는 대상과 유지해야 할 값에 조건부다. 같은 값을 서로 다른 표현으로 만들 수 있고, 같은 표현의 원 계보를 역으로 유일하게 복원할 수 없는 경우도 있다.

**적용 한계:** Calc는 의존 관계가 바뀌며 재계산되는 편집 모델이다. Arrow 명세는 in-memory 표현과 전송을 정의하며 일반적인 변경 동기화 의미를 대신하지 않는다. 따라서 Calc의 ‘원본 수정이 복사본에 반영’ 약속을 Arrow dictionary map이나 Inkscape 객체 연결에 그대로 옮기지 않는다. Arrow의 표현 변환에서 논리값이 보존된다는 추론도 UI 선택·Undo·object identity 보존을 증명하지 않는다.

**다음 최소 확인:** Calc C03 원 시험을 같은 버전에 고정해 D2=7, E2=7을 추가하고 CalculateHard 후 D1·E1의 수치와 수식 문자열을 각각 기록한다. 문서·기존 회귀를 결합한 예상은 D1=0, E1=7이지만 이는 이번에 실행한 관측이 아니다. Arrow C++ `TestDictionary.TransposeBasic`·`TransposeTrivial`·`GetValueIndex` 원 시험을 실행하고, 같은 배열에 논리값 판독과 `indices == 0` 선택을 각각 추가하면 이 원리의 두 소비 경로를 직접 대조할 수 있다.

## 계보·산입

핵심 자료는 8개 원문 파일/명세다(CD-C01–C05, CD-A01–A03). 저작 계보 ID는 6개이며, 행위 기대값이 있는 시험 사건군은 3개(CalcPasteOnly, tdf116413, Arrow dictionary fixtures)다. 이 가운데 이슈 번호가 식별되는 회귀는 tdf116413 한 건이고 원 사용자 글은 이번에 열지 않았다. Calc 도움말 3파일은 같은 도움말 저작군, 두 시험은 공식 유지관리자 시험이므로 독립 사용자 재현으로 세지 않는다. Arrow 명세·구현·시험도 같은 프로젝트이며 동작 설계의 완전히 독립된 확인자 3명으로 취급하지 않는다. 내용이 같은 웹 문서/원 소스, tag/commit 재열람은 한 자료로만 센다. 탐색용 추가 시험과 접근 실패·버전 메타데이터는 별도 원장에 남기고 핵심 자료 최소량에서 제외한다. 후보와 판단 근거가 같은 저작이라는 중복을 공개하며 신규 여섯 건의 독립 사후 확인 수는 0이다.
