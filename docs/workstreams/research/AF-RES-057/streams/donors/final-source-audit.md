# 최종 출처 계보·배당 감사

기록 UTC: 2026-11-23T03:46:06.875472+00:00. 검토자는 root와 같은 모델의 donor 분담 조사자이며 **분담 원장을 독립적으로 읽어 재계수**했다. 독립 사람 검토나 전체 외부 원문 재취득은 아니다. 실제 읽은 파일은 세 stream의 sources.jsonl, ProseMirror와 donor의 source-counts.json이다. 제품 원장의 봉인 후 기대값·실행 요약을 읽었고 별도의 observations·raw replay 파일은 열지 않았다. 정확 입력 해시·행·전체 alias·정규화 계보별 source_id는 [final-source-audit.json](final-source-audit.json)에 있다.

## 결론과 계수 단위

세 원장의 합계는130행, source_id130개로 고유하다. 적격 취득 행112개와 제외 행18개다. 원래 work_id를 그대로 세면72개지만 아래 보수적 alias를 적용하면 **고유 외부 저작66개**가 남는다. 자료군은 **요청4/API·예제4/서로 다른 수정6/지도·회계 사례4/원논문2**, 총20개를 같은 계보 중복 없이 배당할 수 있다.

| Stream | 취득 행 | 원래 적격 work_id | 보수적 alias 뒤 고유 저작 |
| --- | --- | --- | --- |
| Yjs | 54 | 34 | 33 |
| ProseMirror | 50 | 27 | 22 |
| Donor | 26 | 11 | 11 |
| 합계 | 130 | 72 | 66 |

66개는 출처 원장의 고유 저작 수다. 여섯 자리에서 원요구와 동일판 A/B 출력이 모두 확인됐다는 뜻은 아니다. ② 봉인 감사 당시 시험군 결손을 봉인 후 실제 읽은 수정 계보로 보완한 것이며, 과거 원장의 시각이나 예측을 바꾸는 것이 아니다.

## 제안하는 보수적 alias

| 기존 work_id | 정규화 work_id | 근거와 영향 |
| --- | --- | --- |
| yjs-doc-implementation | yjs-undo-implementation | 같은 Yjs 구현의 Doc.js/UndoManager.js 파일 분할을 저작 두 개로 세지 않음. 34→33 |
| P-W-TEST-BASIC-UNDO; P-W-TEST-EXCLUDED-CHANGES; P-W-TEST-MULTILEVEL | P-W-HISTORY-TEST-SUITE | 일반 시험 파일의 서로 다른 선언군·판을 한 suite 저작으로 보수 병합. 27→25 |
| P-W-PATCH-892 | P-W-ISSUE-892 | 요청·댓글·축약 재현·패치가 같은 crash 정정 사건. 해당 CI metadata도 이 계보에 연결하되 계수 제외 |
| P-W-PATCH-984 | P-W-ISSUE-984 | 최초 수정 ab0951c와 후속 정정 c8f47ad는 같은 closeHistory 회귀 사건. 댓글·CI와 함께 한 계보 |
| P-W-PATCH-1311 | P-W-ISSUE-1311 | IME 보고·댓글·composition 패치는 같은 정정 사건. 위 세 병합으로 PM25→22 |

기존 Yjs 원장은 #390/#392 이슈와 수정, forum454와9e98fec, YT1 시험과7395229를 이미 같은 work_id로 묶었다. 이 처리와 PM에도 같은 계보 기준을 적용했다. 같은 매뉴얼의 역사판·그림, 지도 사건의 게시글·변경집합·객체 버전은 donor 원장에서도 이미 병합되어 있다.

CI 빈 조회는 별도 저작이 아니다. `P-CI-9bdb377`은892, `P-CI-c8f47ad`는984, `P-CI-f70697e`는1311, `P-CI-554d6ee`는 history test suite의 출처 관계로만 연결한다. Y-CI-PROBES는 여러 SHA의 metadata 묶음이므로 어느 하나의 새 저작으로 세지 않는다. 연구자 재생은 모든 경우 외부 최소 수에서 제외한다.

## 중복 없는 20저작 배당

아래 대표 source_id는 모두 실제 적격 취득 행이다. 같은 줄의 여러 ID는 계보를 설명하는 참조이며 저작 수를 더하지 않는다.

| 자료군 | 정규화 저작/사건 | 대표 source_id | 배당 수 |
| --- | --- | --- | --- |
| 선정 요청 | yjs-issue-157 | Y-I157; 후속 Y-O157 | 1 |
| 선정 요청 | yjs-issue-204 | Y-I204; 후속 Y-O204 | 1 |
| 선정 요청 | P-W-ISSUE-892 | P-I892; P-O892-C; P-FIX892; P-REPRO892 | 1 |
| 선정 요청 | P-W-ISSUE-1341 | P-I1341; P-O1341-C | 1 |
| 제품 API·예제 | yjs-readme-undo-docs | Y-DOC-ALPHA; Y-DOC-1308; Y-DOC-DIAG | 1 |
| 제품 API·예제 | yjs-forum-drawing-789 | Y-X789: 제품 저자가 작성한 yLine/yLines 작업 예제 | 1 |
| 제품 API·예제 | P-W-HISTORY-API | P-API103; P-API104; P-API130; P-API150 | 1 |
| 제품 API·예제 | P-W-INPUTRULES-API | P-IR120; P-IR120-RULE | 1 |
| 시험·수정 | yjs-test-infinite-capture | Y-F431; Y-T-DIAG-OUT | 1 |
| 시험·수정 | yjs-issue-390 | Y-F390; 원요청 Y-I390 | 1 |
| 시험·수정 | yjs-issue-392 | Y-F392; 원요청 Y-I392 | 1 |
| 시험·수정 | yjs-forum-454 | Y-F454; Y-X454 | 1 |
| 시험·수정 | P-W-ISSUE-984 | P-FIX984; P-FIX984-PREV; P-O984-C; P-I984 | 1 |
| 시험·수정 | P-W-ISSUE-1311 | P-FIX1311; P-O1311-C; P-I1311 | 1 |
| 지도 직접 사례 | W-D-OSM-casablanca | D04; D05; D05A; D05B | 1 |
| 지도 직접 사례 | W-D-OSM-payap | D12; D12H | 1 |
| 회계 직접 사례 | W-D-GNC-guide | D03; D03V1; D03V2 | 1 |
| 회계 직접 사례 | W-D-GNC-reconciliation2017 | D14 | 1 |
| 원연구 | W-D-Prakash1992 | D07 | 1 |
| 원연구 | W-D-Yu2015 | D08 | 1 |

API·예제 배당은 코드 파일을 여러 저작으로 나누는 데 기대지 않도록 Yjs README와 별도 저자 작업 예제를 골랐다. Y-X789는 봉인 후 읽은 보강 자료이며, 고정 E 카드에 사후 대입한 것이 아니다. 네 선정 요청 외의 모집 이슈는 전체66개에는 포함될 수 있으나 선정 요청 배당을 대신하지 않는다.

## 여섯 수정 사건의 직접 식별자

| 배당 source_id | 수정 커밋 | 원장이 확인한 변경 | 한계 |
| --- | --- | --- | --- |
| Y-F431 | [7395229086d9d4db06ebd5936bdd326dbe346834](https://github.com/yjs/yjs/commit/7395229086d9d4db06ebd5936bdd326dbe346834) | MAX_VALUE에서도 stopCapturing 경계가 작동하도록 lastChange guard를 추가하고 관련 시험을 추가 | YT1 시험·helper·PR432를 더하지 않음 |
| Y-F390 | [a22b3cdbc1ee975c023d78725f521f250b7020c2](https://github.com/yjs/yjs/commit/a22b3cdbc1ee975c023d78725f521f250b7020c2) | 원격 map 변경을 덮어쓰는 선택 정책과 시험 | 원문 시험 주석의392 연결은 오기라고 분담 원장이 설명. #390과 #392를 같은 사건으로 합치지 않음 |
| Y-F392 | [abf3fab1b6a479d01d688bb0d5dd7678aec695c6](https://github.com/yjs/yjs/commit/abf3fab1b6a479d01d688bb0d5dd7678aec695c6) | 텍스트 서식 marker 정리와 delta 복원 시험 | 한 패치의 시험 두 개는 한 사건 |
| Y-F454 | [9e98fec5042fd348304fd70b12172cc84409ec37](https://github.com/yjs/yjs/commit/9e98fec5042fd348304fd70b12172cc84409ec37) | 효과 없는 stack item을 건너뛰어 실제 변경이 일어날 때까지 진행 | 원격 복원의 소유권 문제와 stack 순회 결함을 혼동하지 않음 |
| P-FIX984 | [c8f47adf3db77f2fe8756fb28451f8fa1c984958](https://github.com/ProseMirror/prosemirror-history/commit/c8f47adf3db77f2fe8756fb28451f8fa1c984958) | appended transaction과 명시 closeHistory 경계의 회귀 정정 | 이전 ab0951c와 한 사건. 이 패치에는 새 assertion 없음 |
| P-FIX1311 | [f70697ef0cb6f06f0f9e0b719865d115f8c5f1c6](https://github.com/ProseMirror/prosemirror-history/commit/f70697ef0cb6f06f0f9e0b719865d115f8c5f1c6) | composition identity를 추적하여 동일 composition을 한 사건으로 취급 | 새 assertion 없음. ellipsis command 결과 증거로 쓰지 않음 |

그 밖에 [P-FIX892의9bdb377](https://github.com/ProseMirror/prosemirror-history/commit/9bdb3774203d21e3ec14e621eb444524c629b7a3)도 별도의 정정 사건으로 읽혔다. 따라서 읽은 수정 사건 자체는7개다. 다만892는 이미 선정 요청 계보에 배당했으므로 여섯 수정 목표에 다시 배당하지 않았다. 이 구분을 적용하면20개 배당에 중복이 없다.

## 검증 범위와 남는 제한

- 모든 source_id130개와 반대 근거 참조를 재계수했고, 참조 누락은0개다.
- Y-T-DIAG 입력 전용 행은 봉인 후 메타데이터 정정으로 비적격이며, 실제 기대값 취득은 별도 시각의 Y-T-DIAG-OUT으로 남아 있다. PM 입력 전용 행도 비적격이고 P-T150-OUT이 후속 취득이다. 앞선 감사의 양 제품 적격성 불일치는 해소됐다.
- PM source-counts의25개는 suite만 병합한 값이다. 이번22개는 추가로 세 issue/patch 쌍을 합친 값이며, 다른 자료를 버리거나 읽기 기록을 없앤 것이 아니다.
- 여섯 수정 배당 가운데 일부는 구현 패치이며 그 패치에 새 assertion이 없다. 사용자 목표의 '시험·수정 기록' 배당에는 해당하지만, 여섯 개의 실행 확인된 시험이나 기대 문자열로 설명하면 안 된다.
- 지도·회계 직접 사례4개 중 수치 원장/같은 객체 상태 대조는3개, 나머지는 비수치 작성자 실행 보고다. CI 검색의0개 조회 결과는 실행 미실시의 증거가 아니다.
- 이 감사는 외부 최소 수와 계보 배당을 확인한다. 봉인 예측의 적중, 동일판 재현, 첫 두 결과표의 관측 분모는 RESULT 준비 뒤 별도의 주장 검토가 필요하다.
