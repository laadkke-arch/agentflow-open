# Calc의 정확한 다음 재계산 대조 탐색

## 고정 범위와 결과

대상은 `LibreOffice/core@ee3885777aa7032db5a9b65deec9457448a91162`(24.2.7.2)다. **값 붙여넣기와 수식 붙여넣기를 같은 원 입력에서 수행하고, 참조 입력을 바꾼 다음 양쪽 결과를 직접 assertion하는 원 시험은 아래 조사 범위에서 0개 발견했다.** 저장소 전체에 없다고 주장하지 않는다. 함수명/키워드를 쓰지 않는 간접 helper, 다른 시험 디렉터리와 다른 판은 아직 미확인이다.

| 직접 연 범위 | 검색·판독 방법 | 발견한 것 | 결손 |
|---|---|---|---|
| [ucalc_copypaste.cxx](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/unit/ucalc_copypaste.cxx) 10,772행 | 전체 파일에서 `InsertDeleteFlags::VALUE`를 찾고 앞의 `CPPUNIT_TEST_FIXTURE`/`void TestCopyPaste::`에 위치를 대응. signatures L39–105, 추가 fixture L10467–10638 직접 판독. | VALUE 13위치는 네 MultiRange*AsLinkTranspose 함수의 comment/flag다. 기본 executeCopyPasteSpecial는 CONTENTS·ATTRIB와 NoCalc/AutoCalc/RecalcAtEnd/HardRecalcAtEnd 선택을 가진다. tdf116413에는 산술 추가 뒤 참조 변경의 101→102 assertion이 있다. | 같은 원 입력의 값전용/수식보존 양 후보를 다음 변경까지 잇는 시험 없음. AsLink는 값전용이 아니며 다른 후보로 대체하지 않았다. |
| [CalcPasteOnly.py](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/uitest/calc_tests/CalcPasteOnly.py) 41행 | 전체 원 파일 직접 판독. | 정확한 두 UNO command, 첫 출력 0/0, 수식 E1의 상대 참조 이동. | 다음 참조 입력 변경·재계산 assertion 없음. |
| `sc/qa/uitest/pasteSpecial/`의 tag tree 13개 Python 파일 | tree API로 파일 수 확인, 13/13 파일에서 함수명·enter_text_to_cell/getFormula/Calculate/Recalc/assertEqual 위치 직접 탐색. 각 파일의 관측은 sources의 CD-X01–08 및 CD-X10–14. | shift-right/서식 없는 붙여넣기/주석/선택조건/절대 참조 등 주변 반례. tdf65856의 상대참조 결과, tdf57274의 절대식과 값0 assertion. | 정확한 두 후보의 다음 재계산 대조 0개. |
| [ucalc.cxx](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/unit/ucalc.cxx) 6,925행 | testFormulaToValue/InsertDeleteFlags::VALUE/testCopyPaste/testPaste 전체 파일 검색 후 L5802–6010 직접 판독. | ConvertFormulaToValue 전후 숫자 보존과 ISFORMULA TRUE→FALSE, Undo로 TRUE 복구. Undo 후 B5/B6=10/11 때 C5/C6=20/22 기대. | 붙여넣기 두 후보가 아니라 수식→상수→Undo 작업. exact 대조의 빈칸을 대신 채우지 않았다. |
| [ucalc_formula.cxx](https://github.com/LibreOffice/core/blob/ee3885777aa7032db5a9b65deec9457448a91162/sc/qa/unit/ucalc_formula.cxx) 5,043행 | 위 네 키워드 전체 파일 검색. | 목표 일치 0. | 간접 helper·별도 함수명은 놓칠 수 있다. |

GitHub code search의 `PasteOnlyValue`는 CalcPasteOnly.py를 찾았고, `PasteOnlyFormula Calculate`는 메뉴/명령 레지스트리를, `InsertDeleteFlags::VALUE pasteFromClip`은 구현 파일을 반환했다. 이 검색 결과만으로 원 시험 수를 늘리지 않았다. 검색의 현재 기본판과 위 고정 24.2.7.2 원 파일을 구별했다.

## 최소 추가 관측

공식 C03의 입력을 바꾸지 않고 첫 양 후보 assertion 뒤에 D2=7·E2=7을 입력하고 `.uno:CalculateHard`를 실행한다. D1/E1의 숫자·문자열·수식 문자열을 함께 읽는다. 예상 D1=0/E1=7은 공식 명령 의미와 C03의 수식에서 유도한 연구자 예측이며 이번 실행 결과가 아니다. 원 제작자가 만든 같은 비교 시험 또는 그 고정판 실행이 확보되면 ‘문서+분리 회귀의 결합’ 한계를 직접 양 후보 관측으로 낮출 수 있다.

원본 셀과 이동된 참조 셀은 다르다. A1의 수식을 E1로 붙일 때 C03은 참조가 A2:A3→E2:E3로 바뀌는 것을 기대한다. 원본 A2만 바꾸고 E1이 따라야 한다고 기대하면 다른 계약을 시험하게 된다. 원본 연결 요구에는 CD-C01의 Link 옵션이라는 별도 선택이 있으며 여기의 두 후보에 몰래 추가하지 않았다.
