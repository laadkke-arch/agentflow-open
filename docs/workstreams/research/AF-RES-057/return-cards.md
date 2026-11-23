# 사례별 반환 링크와 사용 조건

선택은 이번 증거 범위의 반환 제안이다. D의 더 높은 조작 선택 정확도를 입증한 결과가 아니다.

## YN1

[해당 판 원점 필터 API/구현 — 어느 변경을 추적할지 정할 때](https://github.com/yjs/yjs/blob/dd2b8bc6c79d98e2fb8d773339d9de7532114eba/src/utils/UndoManager.js#L101-L130). 보호 문구 `this text can not be undone` 유지; 일반 편집은 취소; 원점과 사람 식별 구별. 이번 사전 E/D 판정은 A만은 연구 정규화에 조건부; 원요구는 미확인로 같다. E↔D 변경 없음. 원점 집합과 실제 문구/남은 stack 대조는 보조 재생 근거. 중단 조건: 모든 변경이 null 원점이거나 실제 판의 인자 형식이 다르면 보호정책을 보장하지 못함; 사람 신원으로 origin을 해석하지 않음. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.

## YN2

[해당 판 Y.Doc.gc 절 — 삭제 데이터의 보존 가능성을 확인; #204 후속과 함께 한계 점검](https://github.com/yjs/yjs/blob/772bb87d5cfcc4d9e87ba970731c6aa58f6809bf/README.md#L466-L470). 복사한 문서에서 삭제한 Hello 복원, 새 작성자의 `123`·기존 World 유지; undo/redo와 삭제 데이터 존속. 이번 사전 E/D 판정은 판별 불가로 같다. E/D 모두 보류. gc=false 후속 설명·보조 출력은 사후 지식이며 사전 선택을 바꾸지 않음. 중단 조건: GC를 꺼도 private stack의 영속화·다른 문서로의 이동이 공개 계약이 되지 않음; 원자료가 이미 소실되면 단순 상쇄 원리로 복원 불가. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.

## YT1

[stopCapturing API — 묶음 경계를 구현할 때; 원시험은 첫 표의 별도 링크](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/src/utils/UndoManager.js#L321-L343). 첫 push `[1,2,3]` 유지, 다음 `[4,5,6]`만 취소; 순서·undo 그룹·redo 구별. 이번 사전 E/D 판정은 A만로 같다. E↔D 변경 없음. 후열람 원 assertion은 공통 API가 이미 준 그룹 예측과 일치. 중단 조건: 13.0.8 사후 감도에서는 같은 MAX_VALUE 입력의 경계 호출도 두 push를 합침; 판을 확인하지 않은 API 설명의 일반화 중단. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.

## PN1

[#892 선택 mapping 수정 — 원 RangeError를 조사할 때. 캡처 범위 질문이면 해당 판 addToHistory 절](https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3). U2 삭제의 undo에서 RangeError 없이 선택25..30 복원; U1 계속 입력의 보존은 별도 추론 조건. 이번 사전 E/D 판정은 원사건 판별 불가; 보조 정상 A만·역순 텍스트 동률로 같다. E↔D 변경 없음. #892 수정은 selection mapping 근거이며 metadata 개입의 원사건 효과를 증명하지 않음. 중단 조건: 원격 수신·rebase·selection·appendTransaction 순서가 다른 입력을 같은 사건으로 합치지 않음; 엄격한 명시적 남길 텍스트 기준에서는 PN1 제외. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.

## PN2

[undoInputRule의 마지막 동작 조건 — 자동변환만 즉시 취소할 때](https://github.com/ProseMirror/prosemirror-inputrules/blob/40ef4104e086517283081c713727a7f029b565c1/src/inputrules.ts#L105-L107). `...`→`…` 자동변환만 취소하고 입력한 세 점 유지; 후속 x·redo는 연구 경계. 이번 사전 E/D 판정은 즉시 B만; redo 일부·후속 편집 경계 보류로 같다. E↔D 변경 없음. API의 마지막 동작 조건이 선택을 이미 가름. 회계 원리로 redo를 보장하지 않음. 중단 조건: 다른 입력이 이어졌거나 원래 ellipsis로 redo할 것을 요구하면 같은 API 계약으로 해결됐다고 하지 않음. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.

## PT1

[closeHistory API — 사용자가 생각하는 한 번의 편집과 undo 그룹을 맞출 때](https://github.com/ProseMirror/prosemirror-history/blob/554d6eedb76704d1db62d85768611ce4b611abd2/src/history.ts#L363-L366). 연구 목표는 a를 남기고 b만 취소; 원시험 목표는 일반 undo 가능. 같은 작성자와 원격 b를 구별. 이번 사전 E/D 판정은 연구 목표 B만; 원격 b 변형 둘 다로 같다. E↔D 변경 없음. E의 의미적 선노출 때문에 기대 일치를 새로운 발견으로 세지 않음. 중단 조건: 원래 그룹 전체 취소가 목표이면 a까지 사라지는 것은 실패가 아님; 원격 제외 메타데이터와 그룹 경계를 혼동하지 않음. 지도·회계 원전은 내부 기록·현재 효과·뒤 변경·다음 이력 중 보존 목표를 묻는 참고로만 연결하고, 같은 입력판의 제품 출력 보증으로 바꾸지 않는다.
