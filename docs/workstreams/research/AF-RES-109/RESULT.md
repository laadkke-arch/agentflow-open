| 요청 | 층·원문판 | 주소 | 선택 부분 | 두 조건 | 이미 해본 안 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 · Flow menu entry "Rename" should be named "Edit" as the opened dialog already displays | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/node-red/node-red/issues/4505](https://github.com/node-red/node-red/issues/4505) | flow menu label / localization · 환경변수 등을 편집하는 dialog를 메뉴에서 찾기 / Current Behavior; Expected Behavior; final sentence | ① 메뉴 이름이 실제 Edit flow dialog의 동작을 가리킴<br>② 번역판에도 같은 명칭 변경을 반영 | 이미 Rename 메뉴로 Edit flow를 열어 환경변수 설정을 찾음; Edit로 바꾸기와 번역 수정도 요청자가 제시 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |
| R2 · Flow Properties tab missing (3.13) Can't rename a flow | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/node-red/node-red/issues/4507](https://github.com/node-red/node-red/issues/4507) | flow properties pane · flow 이름을 바꿀 수 있게 속성 UI 복구 / Current Behavior; Expected Behavior; Steps To Reproduce | ① flow 이중클릭 경로에서 properties pane을 볼 수 있음<br>② 그 pane에서 flow 이름을 바꿀 수 있음 | flow를 이중클릭해 pane을 열었으나 properties pane과 rename이 없음 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |
| R3 · 3.1.3 Global environment credentials are lost | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/node-red/node-red/issues/4508](https://github.com/node-red/node-red/issues/4508) | global environment credential persistence · 기존 credential을 plaintext 변수 추가 뒤에도 보존 / Current Behavior; Steps To Reproduce; Expected Behavior | ① 처음 global credential 값이 inject 경로로 실제 값으로 읽힘<br>② plaintext global 변수 추가 뒤 같은 credential 조회가 __PWRD__로 바뀌지 않음 | global credential 설정→inject 확인 성공→plaintext 추가→flow에 새 변수 추가→기존 credential이 __PWRD__; #4396과 flow credential fix3.1.0을 이미 비교 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |
| R4 · selectHandle | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/xyflow/xyflow/issues/3757](https://github.com/xyflow/xyflow/issues/3757) | node selection hit region · 겹친 node를 통과해 클릭하면서 필요한 node 삭제도 가능 / Please describe... paragraphs1–2 | ① 일부 node 영역 클릭은 뒤 node로 통과<br>② drag handle을 통한 이동을 유지하면서 선택/삭제가 가능 | dragHandle과 selectable=false로 click-through와 dragging은 달성; selection이 없어 delete 불가 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |
| R5 · Example to have multiple edges on the same node with auto spacing between edges. | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/xyflow/xyflow/issues/3758](https://github.com/xyflow/xyflow/issues/3758) | multiple edge routing · 동일 node의 여러 edge 자동 간격 예시/참고 찾기 / title; body final sentence; image URL only | ① 같은 node에 여러 edge 연결<br>② edge 사이 간격을 자동으로 조정 | multiple edges 시도만 명시; 알려진 layout 도구/수치 없음 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |
| R6 · Zoom on pinch not working on Windows | 공개 현재본문·탐색층 / 원문 최초판 미확인 | [https://github.com/xyflow/xyflow/issues/3759](https://github.com/xyflow/xyflow/issues/3759) | viewport gesture routing · Windows pinch가 scroll 대신 zoom하도록 복구 / Describe the Bug; Steps; Expected; Additional context | ① Windows Chrome/Edge에서 pinch로 zoom<br>② panOnScroll=true 구성 유지 | Figma-like viewport예제; zoomOnPinch=true도 효과없음; Mac에서는 작동한다고 보고 | 최초판·편집이력·원첨부/환경; 목록 외 사전인지 미확인 |

| 요청·방식·순위 | 실제 반환 URL·판·절 | 새 조작·타 분야 원리 | 선택을 가를 입력 | 반례·한계 | 비용 |
| --- | --- | --- | --- | --- | --- |
| R1 · 방식 A · 원래 1위 | [https://nodered.org/docs/user-guide/editor/workspace/flows](https://nodered.org/docs/user-guide/editor/workspace/flows)<br>현행 무판본; Editing flow properties / core:edit-flow | 기지 Edit 변경은 제외; 메뉴·double-click 경로 동등성 시험<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 같은 flow의 환경변수만 바꿔 두 경로로 재개봉 | 번역 조건 미지원; 문서의 Rename 표기도 남음<br>현재 적합성: 근접 실패; 실제 실행 없음 | R1-A 전체 검색2·명시열람4·116.189초; 자동열람·토큰·금액 미확인 |
| R1 · 방식 A · 원래 2위 | [https://www.i18next.com/principles/fallback](https://www.i18next.com/principles/fallback)<br>현행; Fallback / translation resolution | 해당 언어 키가 빠져도 fallback이 가리는지 검사<br>형태: 동종 부품; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 선택 locale의 항목을 하나 없애고 완전성 검사 비교 | 검색 때 응답은 rewritten summary; 사후 원전 재독과 분리<br>현재 적합성: 조건부; 실제 실행 없음 | R1-A 전체 검색2·명시열람4·116.189초; 자동열람·토큰·금액 미확인 |
| R1 · 방식 A · 원래 3위 | 공석 | 반환 후보 없음; 타 분야 원리 없음 | — | [{"rank": 3, "reason": "The Node-RED node-authoring i18n guide supplied background but did not verify the core flow-menu binding. It overlaps the translation test and is not promoted as a third independent contribution. The design-wiki fetch failed."}] | R1-A 전체 검색2·명시열람4·116.189초; 자동열람·토큰·금액 미확인 |
| R1 · 방식 B · 원래 1위 | [https://nodered.org/docs/user-guide/editor/workspace/flows](https://nodered.org/docs/user-guide/editor/workspace/flows)<br>현행 무판본; Editing flow properties / core:edit-flow | A와 같은 경로 동등성 시험; 새 구현0<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 환경변수 수정 뒤 이름·flow ID가 그대로인지 확인 | A와 같은 기능·같은 시험 계보<br>현재 적합성: 근접 실패; 실제 실행 없음 | R1-B 전체 검색3·명시열람3·354.117초; 자동열람·토큰·금액 미확인 |
| R1 · 방식 B · 원래 2위 | [https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus?source=recommendations](https://learn.microsoft.com/en-us/windows/win32/uxguide/cmd-menus?source=recommendations)<br>2022-02-08 표기; Command menus / Properties | Edit·Properties 표현을 가르는 첫 클릭 시험<br>형태: 동종 부품; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 동일 편집 과제에 표현만 달리해 목적지 선택 관측 | Properties가 더 낫다는 근거 없음; 번역 조건 미지원<br>현재 적합성: 조건부; 실제 실행 없음 | R1-B 전체 검색3·명시열람3·354.117초; 자동열람·토큰·금액 미확인 |
| R1 · 방식 B · 원래 3위 | 공석 | 반환 후보 없음; 타 분야 원리 없음 | — | [{"rank": 3, "reason": "The opened i18n guide covers node-author templates, not the core flow menu. It repeats the translation baseline and would require an unverified surface assumption for a new test; no third sufficiently grounded candidate selected."}] | R1-B 전체 검색3·명시열람3·354.117초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 A · 원래 1위 | [https://nodered.org/docs/user-guide/editor/workspace/flows](https://nodered.org/docs/user-guide/editor/workspace/flows)<br>현행; Editing flow properties | 메뉴와 double-click 경로의 상태 비교<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 같은 flow를 두 경로로 열고 pane·저장 결과 비교 | double-click만 반복하면 기지 재현; 수리 실행 아님<br>현재 적합성: 조건부; 실제 실행 없음 | R2-A 전체 검색3·명시열람3·360.024초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 A · 원래 2위 | [https://nodered.org/docs/api/admin/methods/put/flow/](https://nodered.org/docs/api/admin/methods/put/flow/)<br>현행; PUT /flow/:id / Arguments / Responses | UI와 설정 저장을 분리하는 API 대조시험<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 폐기 가능한 빈 flow의 label만 갱신 후 다시 읽기 | pane를 우회하므로 두 UI 조건 불충족; 빈 배열은 실제 flow에 쓰지 않음<br>현재 적합성: 근접 실패; 실제 실행 없음 | R2-A 전체 검색3·명시열람3·360.024초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 A · 원래 3위 | [https://developer.chrome.com/docs/devtools/css/issues](https://developer.chrome.com/docs/devtools/css/issues)<br>2022-11-15 표기; Inspect and debug CSS | DOM 생성과 계산된 CSS/상위 요소 상태를 분리<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 문제 control의 존재·computed 값·선언 출처 비교 | 관찰 도구이며 실제 pane 원인·수리 미확인<br>현재 적합성: 조건부; 실제 실행 없음 | R2-A 전체 검색3·명시열람3·360.024초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 B · 원래 1위 | [https://nodered.org/docs/user-guide/editor/workspace/flows](https://nodered.org/docs/user-guide/editor/workspace/flows)<br>현행; Editing flow properties | A와 같은 대체 진입 경로 시험<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 메뉴와 double-click 후 Properties·이름 저장 비교 | 같은 기능·시험 중복 제거<br>현재 적합성: 조건부; 실제 실행 없음 | R2-B 전체 검색3·명시열람6·423.892초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 B · 원래 2위 | [https://www.w3.org/TR/2015/WD-wai-aria-practices-1.1-20150514/](https://www.w3.org/TR/2015/WD-wai-aria-practices-1.1-20150514/)<br>W3C WD2015-05-14; Tab Panel | 탭 등록·선택·연결 panel 표시를 분리한 진단<br>형태: 동종 부품; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 탭 선택 상태와 대응 panel 표시를 각각 관측 | 초안의 일반 계약; Node-RED 수리나 이름 저장 보장 아님<br>현재 적합성: 조건부; 실제 실행 없음 | R2-B 전체 검색3·명시열람6·423.892초; 자동열람·토큰·금액 미확인 |
| R2 · 방식 B · 원래 3위 | [https://github.com/node-red/node-red/blob/main/packages/node_modules/@node-red/nodes/core/function/10-function.html](https://github.com/node-red/node-red/blob/main/packages/node_modules/@node-red/nodes/core/function/10-function.html)<br>main 가변판; Function editor / RED.tabs | 동일 프로젝트 tabs 구현 비교를 시도했으나 보류<br>형태: 동종 부품; 새 구현0·새 시험0; 먼 타 분야 원리 없음 | 등록·초기 선택·change callback 구간을 비교하려 함 | 별도 판독자의 본문503/raw차단; 새 구현·시험 산입0<br>현재 적합성: 근접 실패; 실제 실행 없음 | R2-B 전체 검색3·명시열람6·423.892초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 A · 원래 1위 | [https://nodered.org/docs/creating-nodes/credentials](https://nodered.org/docs/creating-nodes/credentials)<br>현행; Runtime / Credentials within Editor | 존재·편집 의도와 비밀값 표현을 분리<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | Inject 고정 후 plaintext만 변경 / flow만 변경 / 명시 교체 | 일반 node와 global 경로는 다를 수 있음; runtime까지 미실행<br>현재 적합성: 조건부; 실제 실행 없음 | R3-A 전체 검색2·명시열람2·311.342초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 A · 원래 2위 | [https://developer.hashicorp.com/vault/docs/commands/kv/patch](https://developer.hashicorp.com/vault/docs/commands/kv/patch)<br>현행 및 조건부 v1.15.x; kv patch / method / CAS | 전체 대체와 부재 필드 보존 갱신을 구분<br>형태: 단일 기능; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | SECRET 생략 / mask 전송 / 실제 새 값 전송 | 명시 mask는 patch에도 저장될 수 있음; 과거판 navigation 모순<br>현재 적합성: 조건부; 실제 실행 없음 | R3-A 전체 검색2·명시열람2·311.342초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 A · 원래 3위 | 공석 | 반환 후보 없음; 타 분야 원리 없음 | — | [{"rank": 3, "reason": "No third independently useful mechanism was verified. Related search hits mostly repeat credential handling or partial-update semantics; a vacant slot avoids padding."}] | R3-A 전체 검색2·명시열람2·311.342초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 B · 원래 1위 | [https://auxx.ai/blog/connections-part-2-secret-lifecycle](https://auxx.ai/blog/connections-part-2-secret-lifecycle)<br>2026-08-18; sentinel filtering / merge | mask 제거 뒤 같은 깊이의 기존 형제 값을 보존<br>형태: 단일 기능; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | A·B mask와 새 P를 보내 delta·저장·runtime 비교 | 2024 이후 글; 얕은 merge·불안정 ID·실제 marker 값이 반례<br>현재 적합성: 조건부; 실제 실행 없음 | R3-B 전체 검색2·명시열람4·342.655초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 B · 원래 2위 | [https://docs.vendure.io/current/framework/developer-guide/secret-fields](https://docs.vendure.io/current/framework/developer-guide/secret-fields)<br>v3.8.2 현행; Secret fields, 2026-07-31 편집 | 기존 값 없는 retain 의도를 거절하는 정책<br>형태: 단일 기능; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 기존 A와 새 B에 같은 placeholder를 각각 제출 | 생성 정책은 원 요청에 없음; 빈 값 정책이 Auxx와 상충<br>현재 적합성: 조건부; 실제 실행 없음 | R3-B 전체 검색2·명시열람4·342.655초; 자동열람·토큰·금액 미확인 |
| R3 · 방식 B · 원래 3위 | [https://nodered.org/docs/creating-nodes/credentials](https://nodered.org/docs/creating-nodes/credentials)<br>현행; Node credentials / has_password | 일반 node와 global 경로를 대조하는 시험만 추가<br>형태: 동종 부품; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 초기 두 값의 runtime 소비 확인 후 plaintext global 추가 | 동일 프로젝트라도 serializer·저장 계약이 같다는 보장 없음<br>현재 적합성: 조건부; 실제 실행 없음 | R3-B 전체 검색2·명시열람4·342.655초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 A · 원래 1위 | [https://www.w3.org/TR/css-ui-4/](https://www.w3.org/TR/css-ui-4/)<br>CSS UI4 WD2026-01-20 §6.2 | wrapper 제외·자식 handle만 hit target 허용<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 겹친 두 노드의 body/handle 클릭·drag·선택 ID 비교 | 선택·삭제 통합은 앱 책임; 2024판 문구 미확인<br>현재 적합성: 조건부; 실제 실행 없음 | R4-A 전체 검색3·명시열람6·484.296초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 A · 원래 2위 | [https://reactflow.dev/api-reference/types/delete-elements](https://reactflow.dev/api-reference/types/delete-elements)<br>현행; DeleteElements / nodes / edges | 선택 대신 명시 ID로 삭제하는 별도 제어<br>형태: 단일 기능; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 미선택 노드 ID 삭제 후 노드·연결 edge 목록 확인 | 선택 핸들은 구현하지 않으므로 근접 오답<br>현재 적합성: 조건부; 실제 실행 없음 | R4-A 전체 검색3·명시열람6·484.296초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 A · 원래 3위 | [https://app.unpkg.com/@xyflow/react@12.4.2/files/dist/esm/index.mjs](https://app.unpkg.com/@xyflow/react@12.4.2/files/dist/esm/index.mjs)<br>@xyflow/react12.4.2 배포 미러; NodeWrapper | 안쪽 요소와 wrapper의 제외 위치를 가르는 실패 시험<br>형태: 동종 부품; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 안쪽만 none / wrapper none 후 실제 event target 비교 | 미러 중복 산입0; v12는2024-07 이후이며 handle/선택 보존 미흡<br>현재 적합성: 조건부; 실제 실행 없음 | R4-A 전체 검색3·명시열람6·484.296초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 B · 원래 1위 | [https://www.w3.org/TR/css-ui-4/](https://www.w3.org/TR/css-ui-4/)<br>CSS UI4 WD2026-01-20 §6.2 | A와 같은 공간별 hit target 설계<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | wrapper none·자식 auto와 전체 none을 비교 | 같은 규칙·시험 중복 제거; 부모 bubbling과 선택은 별개<br>현재 적합성: 조건부; 실제 실행 없음 | R4-B 전체 검색2·명시열람6·340.982초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 B · 원래 2위 | [https://reactflow.dev/learn/customization/utility-classes](https://reactflow.dev/learn/customization/utility-classes)<br>현행; Utility classes / nodrag | 동작 억제와 아래 노드로의 전달을 가르는 음성 대조<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | nodrag와 공간 제외를 적용해 target·선택 ID 비교 | nodrag만으로 click-through가 되지 않으며 drag handle을 망칠 수 있음<br>현재 적합성: 근접 실패; 실제 실행 없음 | R4-B 전체 검색2·명시열람6·340.982초; 자동열람·토큰·금액 미확인 |
| R4 · 방식 B · 원래 3위 | [https://reactflow.dev/api-reference/react-flow](https://reactflow.dev/api-reference/react-flow)<br>현행; Interaction props / selectNodesOnDrag / elevation | drag 선택·선택 후 쌓임 순서 대조시험<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | selectable 조건 고정 후 drag 정책과 겹침 재검사 | 영역별 선택 구현 아님; selectable=false면 여전히 선택 안 됨<br>현재 적합성: 조건부; 실제 실행 없음 | R4-B 전체 검색2·명시열람6·340.982초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 A · 원래 1위 | [https://next.reactflow.dev/learn/customization/handles](https://next.reactflow.dev/learn/customization/handles)<br>next 현행; Handles / Dynamic handles | 고정 handle ID와 개수별 좌표·측정 갱신 책임<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | handle 수를 늘린 뒤 좌표·edge 연결·refresh 전후 비교 | 좌표 산술은 제안 코드; 끝점 간격이 전체 경로 분리를 보장하지 않음<br>현재 적합성: 조건부; 실제 실행 없음 | R5-A 전체 검색2·명시열람5·393.758초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 A · 원래 2위 | [https://eclipse.dev/elk/reference/options/org-eclipse-elk-nodeSize-options.html](https://eclipse.dev/elk/reference/options/org-eclipse-elk-nodeSize-options.html)<br>현행; ELK Node Size Options | 균등 port 간격과 node 밖 overhang 정책 선택<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | label 크기 차이·좁은 node에서 두 옵션 조합 비교 | 지원 layout·sizing 조건 필요; edge 내부 경로 겹침 가능<br>현재 적합성: 조건부; 실제 실행 없음 | R5-A 전체 검색2·명시열람5·393.758초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 A · 원래 3위 | [https://reactflow.dev/api-reference/utils/add-edge](https://reactflow.dev/api-reference/utils/add-edge)<br>현행; addEdge / Notes | 자료 누락과 겹쳐 그려짐을 분리하는 시험<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | 같은 source/target/handles·다른 ID를 넣고 edge 수 확인 | 삽입 규칙이며 자동 spacing이 아님; 원 topology 미확인<br>현재 적합성: 조건부; 실제 실행 없음 | R5-A 전체 검색2·명시열람5·393.758초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 B · 원래 1위 | [https://next.reactflow.dev/learn/customization/handles](https://next.reactflow.dev/learn/customization/handles)<br>next 현행; Handles / Dynamic handles | A와 같은 개수별 handle 배치 정책<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 한 노드→서로 다른 목적지에서 좌표·refresh 비교 | 고유 ID만으로 간격은 생기지 않음; 같은 선택·시험 중복<br>현재 적합성: 조건부; 실제 실행 없음 | R5-B 전체 검색3·명시열람4·353.149초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 B · 원래 2위 | [https://docs.yworks.com/yfiles/doc/api/y/layout/ParallelEdgeLayouter.html](https://docs.yworks.com/yfiles/doc/api/y/layout/ParallelEdgeLayouter.html)<br>yFiles Java2.19; Concept / Features / line distance | master 경로 재사용과 고정 간격·node 맞춤 간격 선택<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 같은 두 끝점의 다중 간선에 고정/가변 gap 비교 | 동일 끝점 해석에서만 적합; 원 이미지·fan-out은 미확인<br>현재 적합성: 동일 노드쌍 해석에 한정; 실제 실행 없음 | R5-B 전체 검색3·명시열람4·353.149초; 자동열람·토큰·금액 미확인 |
| R5 · 방식 B · 원래 3위 | [https://kb.yworks.com/article/313/Routing-multiple-edges-between-two-nodes-in-a-parallel-fashion](https://kb.yworks.com/article/313/Routing-multiple-edges-between-two-nodes-in-a-parallel-fashion)<br>현행; yWorks KB313 / edge-created handler | 새 간선 추가 시 영향받는 peer group만 다시 배치<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 정·역방향 peer를 추가하고 해당 group 경로 재계산 | 앞 URL과 같은 router; 삭제·임의 fan-out·실제 adapter 미검증<br>현재 적합성: 동일 노드쌍 해석에 한정; 실제 실행 없음 | R5-B 전체 검색3·명시열람4·353.149초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 A · 원래 1위 | [https://chromium.googlesource.com/chromium/src/%2B/297980d7a0e33b44dce6c727d7016345a80e33fa/content/browser/renderer_host/input/touchpad_pinch_event_queue.cc](https://chromium.googlesource.com/chromium/src/%2B/297980d7a0e33b44dce6c727d7016345a80e33fa/content/browser/renderer_host/input/touchpad_pinch_event_queue.cc)<br>Chromium297980d7, 2018-06-04; pinch queue | Ctrl 표시 wheel을 pan 전에 별도 경로로 분기<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | modifier만 다른 입력과 실제 pinch의 첫 이벤트 비교 | B1과 같은 encoder 계보; 해당 Windows 장치 경로는 미확인<br>현재 적합성: 조건부; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-A 전체 검색3·명시열람3·268.461초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 A · 원래 2위 | [https://d3js.org/d3-zoom](https://d3js.org/d3-zoom)<br>D3 현행; zoom.filter / wheelDelta / scaleExtent | wheel listener를 남기고 시작 이벤트를 선택적으로 거름<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | listener 제거 / 선택 filter와 scale·translation 비교 | 의존 버전·override·scale 경계 미확인; R6 판독 후속노출<br>현재 적합성: 조건부; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-A 전체 검색3·명시열람3·268.461초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 A · 원래 3위 | [https://developer.chrome.com/blog/scrolling-intervention-2/](https://developer.chrome.com/blog/scrolling-intervention-2/)<br>2019-02-07 표기; Chrome73 passive intervention | 기본 passivity와 취소 가능성을 분리한 진단<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | root listener 옵션과 defaultPrevented를 대조 | 이미 nonpassive인 element listener면 빗나감; pan→zoom 수리 아님<br>현재 적합성: 조건부; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-A 전체 검색3·명시열람3·268.461초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 B · 원래 1위 | [https://chromium.googlesource.com/chromium/src/%2B/3b54b6aa8be4525318436d271397fc7d90c21da4/content/browser/renderer_host/input/touchpad_pinch_event_queue.cc](https://chromium.googlesource.com/chromium/src/%2B/3b54b6aa8be4525318436d271397fc7d90c21da4/content/browser/renderer_host/input/touchpad_pinch_event_queue.cc)<br>Chromium3b54b6aa; pinch queue / first ACK | A1과 같은 modifier 분기, 첫 update 취소 관측<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | Ctrl wheel / 일반 wheel 및 첫 ACK 상태 비교 | 원 검색 tree2018-10-12 확인(시간대 없음); 독립 재조회 실패·실제 Chrome120 배포 미확인<br>현재 적합성: 조건부; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-B 전체 검색2·명시열람6·420.144초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 B · 원래 2위 | [https://chromium.googlesource.com/chromium/src/%2B/36321190fa6fb1f7b2e2ebd5ee1d635b91f060bb/chrome/browser/resources/pdf/gesture_detector.ts](https://chromium.googlesource.com/chromium/src/%2B/36321190fa6fb1f7b2e2ebd5ee1d635b91f060bb/chrome/browser/resources/pdf/gesture_detector.ts)<br>Chromium36321190; PDF GestureDetector | wheel을 pinch 시작·누적·종료 생명주기로 바꾸는 어댑터<br>형태: 동종 부품; 새 구현1·새 시험1; 먼 타 분야 원리 없음 | 시간 간격을 둔 두 wheel의 누적 scale과 종료 비교 | PDF와 원앱의 handler가 다름; Mac 주석·Ctrl wheel 혼동·판 날짜 결손<br>현재 적합성: 조건부; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-B 전체 검색2·명시열람6·420.144초; 자동열람·토큰·금액 미확인 |
| R6 · 방식 B · 원래 3위 | [https://reactflow.dev/api-reference/react-flow](https://reactflow.dev/api-reference/react-flow)<br>현행; ReactFlow Keyboard props | activation key 기본값/null의 통제 비교<br>형태: 단일 기능; 새 구현0·새 시험1; 먼 타 분야 원리 없음 | panOnScroll 유지, activation만 바꿔 실제 이벤트 관측 | zoomOnPinch=true는 기지 안; 두 설정이 함께 실패할 수 있음<br>현재 적합성: 원문 계약 범위; 실제 실행 없음<br>R6 사후 논의 노출 독해자: 잠정 판정 | R6-B 전체 검색2·명시열람6·420.144초; 자동열람·토큰·금액 미확인 |

| 고유 요청 | 비교 분류 | 새 구현·새 시험 | 실제 후속 | 비교 가능 분모 |
| --- | --- | --- | --- | --- |
| R1 · 고유 요청 1 | 비교 불가 | 구현0·시험3 (요청 내 키 합집합; A 0/2, B 0/2) | PR4506 2024-01-05 병합, 3.1.4 02-06 게시; 원 요청자 재실행 확인 없음<br>[공개 후속 기록](https://github.com/node-red/node-red/issues/4505) | 0/1 |
| R2 · 고유 요청 1 | 비교 불가 | 구현0·시험4 (요청 내 키 합집합; A 0/3, B 0/2) | goldriver2 2024-01-02 Node.js 업그레이드 뒤 회복 보고; 인과는 본인도 불확실<br>[공개 후속 기록](https://github.com/node-red/node-red/issues/4507) | 0/1 |
| R3 · 고유 요청 1 | 비교 불가 | 구현3·시험5 (요청 내 키 합집합; A 2/2, B 2/3) | PR4526 2024-01-16 병합, 3.1.4 포함; 원 요청자 재시험 확인 없음<br>[공개 후속 기록](https://github.com/node-red/node-red/issues/4508) | 0/1 |
| R4 · 고유 요청 1 | 비교 불가 | 구현2·시험5 (요청 내 키 합집합; A 2/3, B 1/3) | 2024-08-26 유지보수자 updateNode 제안·닫힘; 실제 selected:false; 실행 확인 없음<br>[공개 후속 기록](https://github.com/xyflow/xyflow/issues/3757) | 0/1 |
| R5 · 고유 요청 1 | 비교 불가 | 구현4·시험5 (요청 내 키 합집합; A 2/3, B 3/3) | 2024-01-03 custom-edge 경로 예시 제안·닫힘; 실행 확인 없음; 제목26초 뒤 편집<br>[공개 후속 기록](https://github.com/xyflow/xyflow/issues/3758) | 0/1 |
| R6 · 고유 요청 1 | 비교 불가 | 잠정 · 구현3·시험5 (요청 내 키 합집합; A 2/3, B 2/3) | 2024-04-30 PR4229/4230·11.11.3; 이후 느린 pinch 보고; aleib 재시험 확인 없음<br>[공개 후속 기록](https://github.com/xyflow/xyflow/issues/3759) | 0/1 |

## 수용 판정과 이 결과의 의미

**AF-RES-109의 수용 상태는 PARTIAL이다.** 공개 요청의 현재 opening post 6건에 대해 A/B 검색 12회를 실제 수행했고, 원격 봉인 후 분리 판독·반례 검토·공개 후속 조사를 마쳤다. 그러나 최초 작성판 6건을 확보하지 못했고 정확한 백엔드 모델 ID와 검색엔진의 자동 개봉 수를 관측하지 못했다. 일부 검색과 판독에는 후속 정보가 노출되었다. 따라서 엄격한 방법 비교의 분모는 **0/6**이며 A 우세, B 우세, 동률, 성공률을 추정하지 않는다. 표3의 여섯 행은 모두 비교불가다. 이는 여섯 요청이 모두 해결 불가능했다는 뜻도 아니다.

현재판을 입력으로 한 탐색 기록에서는 중복을 합친 **조건부 선택안 12개와 제안된 판별시험 27개**가 남는다. 이 수에는 요청의 전체 조건을 충족하지 못한 근접 오답을 가르는 선택도 포함된다. R6의 선택3·시험5는 판독자의 후속 노출 뒤 작성되어 잠정치로 분리한다. R1–R5만의 기술적 목록은 선택9·시험22다. 원 프로젝트에 적용하거나 제안된 시험을 실행한 수는 **0**이다. 두 필수조건을 무조건 함께 만족하는 해결책12개, 원 개발자가 처음 안 기능12개, 채택12건이라는 해석은 모두 성립하지 않는다. 먼 분야의 원리를 검색 단계에서 발견했다는 적격 후보는 **0**이다. [판정 원장](choices.csv), [가림과 노출 감사](evidence/audit/execution-audit.md), [판독 예외](evidence/blind/r4-r6/review.md).

자료 하한은 현재 접근 가능한 원자료를 기준으로 보수적으로 대사했다. 직접 읽은 검색 원자료52행의 작업자 자체 고유표시37개를 그대로 더하지 않고, 같은 원전·제품 기능·원천 코드 계보를 합쳐 검색 원저작·기능 계보17개만 인정했다. 최초판이라는 별도 자격은 여전히 결손이다.

| 배당 | 목표 | 독해·중복 제거 후 산입 | 남은 자격 결손 |
| --- | ---: | ---: | --- |
| 모집 원 요청 | 6 | 현재 opening post 6 | 최초 작성판 확인0/6; 현재판을 최초판으로 대체하지 않음 |
| 검색 반환 원 설계·구현 | 8 | 보수적 원저작·기능 계보17 | 17개의 독립 구현·새 원리·2024년 가용성을 뜻하지 않음 |
| 다른 계보의 판별시험·반례 원전 | 6 | 6 | 원전 계약 비교; 제안된 실제 프로젝트 시험0 |
| 발굴 뒤 외부 분야 원전 | 4 | 4 | 전부 사후 보조층; 발견 실적0 |
| 합계 | 24 | 33 | 자료 수 충족과 핵심 비교 충족은 별도; 최종 PARTIAL |

독해 행, 원저작 계보, 고유 요청 사건, 검색 실행, 실제 제품 실행을 서로 다른 단위로 유지한다. 같은 사건의 PR·패치·릴리스·재열람은 원저작 수를 늘리지 않는다. 33은 보수적인 출처 재고의 수이며 도달 가능한 전체 웹의 분모나 재현율이 아니다. [전역 출처 원장](sources.jsonl), [52행 처리와17개 계보의 근거](evidence/audit/source-genealogy-audit.json), [산입 규칙](evidence/source-accounting.json).

## Q1. 바꾸려는 부분과 보존 조건은 무엇이었나

2024년 공개 issue를 GitHub에서 생성시각 오름차순, 동시각에는 번호순으로 읽었다. PR을 제외한 현재 검색 결과는 Node-RED187건, xyflow531건이었다. 각 첫80개를 고정한160행에서 제목과 opening post만으로 부분·목적·구별되는 조건 둘을 읽을 수 있는 첫3건씩을 취했다. 실제 선별은 각 저장소의 첫3건에서 끝났으며 그 앞의 탈락행은0개다. 나머지154행은 탈락이 아니라 `not_screened_after_third`다. 현재 검색에서 사라진 issue까지 복원한 역사적 전체 모집틀은 아니다. [frame.csv](frame.csv), [모집 규칙](SCOPE.md).

R2의 pane 표시와 이름변경은 인과적으로 가까운 약한 조건쌍이다. R5의 자동 간격 요구는 제목에 있으며 본문 그림의 실제 연결 구조는 읽지 못했다. 처음에는 이 두 요청을 더 풍부한 뒤쪽 요청으로 바꾸려 했지만, 별도 프로토콜 판독이 원순위 규칙 위반을 지적하여 검색 전에 첫3건을 유지했다. 이 약점을 결과가 좋은 다른 사례로 메우지 않았다. 사후에 R5 제목이 생성26초 뒤 수정된 사건을 발견했으므로, 현재 입력을 최초 요청과 동일하다고 가정하는 것은 실제로 깨질 수 있다. 이는 원문 본문판 복구가 아니며 기존 입력과 검색 결과를 고치지 않았다. [입력·위치](requests.jsonl), [R5 편집 사건](https://api.github.com/repos/xyflow/xyflow/issues/events/11365940209), [후속 원장](aftermath.csv).

Studio 층은 **0건**이다. 첫 묶음 봉인 시 공개된 `docs/product/RESEARCH_BRIEF.md`의 미래 제품 설명과 예시를 두 보존조건이 붙은 실제 사용자 요청으로 간주하지 않았다. 비공개 저장소·대화, 다른 PLAN#27 작업, 다른 작업자의 중간 산출물을 모집에 넣지 않았다. 공개 예시가 실제 요청으로 승격되었다는 근거가 없다는 제한된 판단이며 저장소 어디에도 실제 요청이 없다는 전수조사 결론은 아니다.

## Q2. 당사자의 기지 안과 미정 선택

baseline은 검색 전에 봉인했다. R1은 이미 Rename→Edit와 번역 반영을 제안했다. 따라서 이를 다시 제안하는 것은 새 구현이 아니다. R3은 기존 credential 실패와 이전 flow 수준 수정, 추가 환경변수와 Inject 편집 순서를 제시했다. R4는 `dragHandle`과 `selectable=false`를 이미 시도했고 선택 불가가 삭제 불가로 이어지는 문제를 설명했다. R6은 `panOnScroll=true`, `zoomOnPinch=true`, Windows와 macOS의 차이 및 Figma 예시를 이미 알고 있었다. R2의 원문 Node-RED 버전 문자열 `3.13`을 임의로 `3.1.3`으로 고치지 않았다. R5의 알려진 선택은 예시 요청이며 이미 특정 레이아웃 알고리즘을 시도했다는 증거는 없다. [baseline.csv](baseline.csv), 각 행의 `exact_location`과 [원 요청](requests.jsonl).

이후 후보가 baseline에 없으면 **사전 목록에 없음**으로만 기록한다. 최초 인지, 학습, 채택은 별도 근거가 필요하다. 생략된 값이나 그림의 연결 구조를 채워 자연 요청으로 만들지 않았다. 제안된 최소 입력·예상 출력은 검색 뒤 작성한 연구자의 시험 설계이며 자연 표본6건에 섞지 않았다.

봉인 때 원 API 본문의 CRLF를 포함한 지문과 실제 프롬프트의 LF 정규화 지문이 달랐다. 원 hash를 보존하고 실험 지문을 추가했으며12개 arm의 실제 입력 지문은 모두 일치했다. 내용·숫자·조건은 변경하지 않았고 재검색도 하지 않았다. 이 정정은 최초판 결손을 해소하지 않는다. [줄바꿈 대사 영수증](evidence/start/input-newline-reconciliation.json), [프롬프트 지문](evidence/start/prompt-fingerprints.json).

## Q3. 실제 검색 전략·노출·소비량

A는 일반적인 숙련 모델의 자유 검색이며 다른 분야와 재질의도 허용했다. B는 부분·보존조건·입력→처리→관측을 분해하고 동종 후보와 공여 분야 이름 없는 관계형 질의를 시도했다. 두 방식 모두 영어 입력·영어 질의와 같은 `system2_search_query` 도구를 사용했다. 모든 arm은 별도 `fork_turns=none` 문맥에 해당 요청과 해당 방식 지시만 받았다. 요청쌍 내 실행 순서는 R1/R3/R5 A→B, R2/R4/R6 B→A로 교대했고 앞 arm 종료 후 뒤 arm을 시작했다. 부모의 표시 모델은 GPT-6 Astra Pro지만 immutable backend ID·seed 일치를 확인할 수 없었다. 독립 인간 판독이나 별도 native web-pro 세션을 수행했다고 쓰지 않는다. [실제 지시](evidence/start/search-instructions.md), [실행 감사](evidence/audit/execution-audit.md).

실제 실행은 질의30개, 명시적 페이지 동작52개, 최종 반환33개와 공석3개다. 6×2×3의36자리를 모두 유지했다. 공석은 R1-A3, R1-B3, R3-A3다. query 결과에 노출된523행을 기록했으며 상위5위는 실제 반환 또는 명시적 공석으로 대사했다. R2-B의 event5는 rank1만 있고2–5는 공석이다. 실패3동작과 반복 원전 작업12동작도 개봉 예산에 포함했다. 자동 개봉 수·토큰·금액은 미확인이고0으로 환산하지 않는다. 원장108이벤트에는 검색·페이지 동작과 실행 상태 기록이 함께 있으므로108을 검색 횟수로 세지 않는다. [search.jsonl](search.jsonl), [12개 원 실행](evidence/search/), [costs.csv](costs.csv).

| 방식 | 질의 | 명시 개봉 | 최종 링크 | 각 arm 경과시간의 합 |
| --- | ---: | ---: | ---: | ---: |
| A | 15 | 23 | 16 | 1,934.069433초 |
| B | 15 | 29 | 17 | 2,234.938809초 |

경과시간에는 모델의 판단과 도구 대기 시간이 포함되며 요청 간 병렬 작업이 있어 합계는 벽시계 전체 소요시간이 아니다. 같은 질의 상한이 같은 실제 비용을 뜻하지 않는다. B가6회 더 개봉했다는 관측만으로 비용 대비 효율이나 시간 절감 효과를 추정할 수 없다.

| 요청 | 공통 상한 q/open | A의 공통 소비량 안에서 읽은 최종 순위 | B의 공통 소비량 안에서 읽은 최종 순위 | 주의 |
| --- | --- | --- | --- | --- |
| R1 | 2/3 | 1,2 | 1,2 | 원문 취득 가능성만 확인 |
| R2 | 3/3 | 1,2,3 | 1 | A는 검색요약으로 같은 요청 후속 노출 |
| R3 | 2/2 | 1,2 | 확정 없음;1 또는3 순서 불명확 | 동시 개봉의 event index와 UTC 순서 불일치 |
| R4 | 2/6 | 없음 | 1,2,3 | A의 최종 근거는3번째 질의 이후 |
| R5 | 2/4 | 1,3 | 없음 | B의 yFiles 검색은3번째 질의 |
| R6 | 2/3 | 1,2 | 2 | B 검색 및 최종 판독에 후속 노출 |

| 방식 | 전체 실행의 고유 선택안 / 시험 | 공통 소비량 안에서 원전 취득이 확인된 선택키 / 시험키 |
| --- | ---: | ---: |
| A | 8 / 16 | 5 / 11 |
| B | 8 / 16 | 2 / 7 |

두 방식 사이의 같은 선택·시험을 합치면 전체12/27이며 위 방법별 수를 단순 합산하지 않는다. R6 잠정치가 포함되어 있고 근접 오답의 판별안도 포함한다. 오른쪽 열의 차이를 방법의 성능 차이라고 해석하지 않는다.

공통 소비량 결과는 최종 후보의 **원전 취득이 해당 prefix 안에 있었는가**를 뜻한다. 그 시점에 제안이 이미 완성되었거나 짧은 예산으로 재실행해 같은 결과를 얻었다는 뜻은 아니다. R3-B는 index순과 UTC순의 두 prefix를 보존하고 확정 공통 실적은0으로 보수적으로 처리했다. 전체 실행의 후보는 그대로 남겼다.

B의 관계형 질의가 항상 유용한 다른 분야를 찾아주지는 않았다. R5의 관계형 질의는 네트워크 분야의 단어 유사 결과로 흘렀고 이후 평행 edge 질의에서 yFiles에 도달했다. A도 기능·원리 재검색을 수행했다. R2-A의 같은 issue 포럼 요약과 R6-B의 같은 issue 댓글 요약 노출은 의도적 열람이 아니어도 실제 정보다. root의 검색 전 R4 댓글 일부 노출과 R6 판독자의 사후 노출도 기록했다. 노출된 후보를 인용에서 빼는 것만으로 문맥이 다시 깨끗해지지는 않는다.

## Q4. URL·기능·원전 계보를 어떻게 분리했나

33개 반환행을 요청·URL 기준28개 묶음으로 가리고 두 판독 문맥에 나누었다. 서로 다른 요청까지 합친 주소는26개다. 판독자는 방법·순위·root 해석·사후 결정을 받지 않았고 원전과 요청을 읽었다. 다만 R6 판독 중 우연한 원 issue 요약이2026-11-24 02:29:49 UTC에 노출되었고 R6 최종 판정은 그 뒤였으므로 결과 가림은 성립하지 않는다. 방법·순위 가림과 별도로 기록했다. 패킷과 판독 파일은 검색 봉인 `628e337...` 뒤 생성되었으며 그 검색 커밋에 이미 있었다고 주장하지 않는다. [패킷](evidence/blind/packet.json), [R1–R3 판독](evidence/blind/r1-r3/review.md), [R4–R6 판독](evidence/blind/r4-r6/review.md).

원저작 산입은 제목이나 주소 수로 하지 않았다. Node-RED flow guide 반복과 PUT flow 문서는 보수적으로 같은 flow 편집 계보로 묶었다. yFiles API와 데모는 같은 parallel router, Chromium 입력 인코더의 두 revision은 같은 기능 계보로 묶었다. React Flow의 같은 클래스·API 반복도 기능 계보로 합쳤다. 동일 계보 안에서 실제 조작이 달라 선택안이 둘일 수는 있지만 원저작 수가 둘로 늘지는 않는다. 17개 계보에 붙인 대표 산입행은 장부의 대표일 뿐 먼저 발견한 arm의 독점 승점이 아니다. [계보 감사](evidence/audit/source-genealogy-audit.md).

검색 단계의 i18next 개봉은 도구 재작성 요약이어서 독립 원문 산입을 제외했다. Function-node 소스의 실제 작동 절은 독립 재개봉이 실패하여 비교 근거를 보류했다. unpkg 미러도 원저작을 늘리지 않았다. 반대로 W3C tabs, Vendure, CSS에서 처음 메타데이터만 본 행의 산입을 실제 본문을 읽은 같은 검색 안의 후속행으로 옮겼다. 판독자의 나중 재열람을 옛 발견 실적으로 이전하지 않았다. 탈락·보류 후보의 가장 강한 반대 근거는 [candidates.csv](candidates.csv)의 판정과 [choices.csv](choices.csv)의 `broken_source_assumption`에 남겼다.

## Q5. 어떤 선택과 실패 시험이 추가되었나

R1의 새 내용은 명칭 변경 자체가 아니라 같은 대화상자로 가는 진입경로, 번역 fallback, 명칭에 따른 첫 클릭을 가르는 시험3개다. R2 역시 실제 pane 고장 원인을 찾은 것이 아니라 진입경로, DOM/CSS, tab 상태, UI와 설정 API의 차이를 나누는 시험4개다. 화면을 우회해 이름을 저장하는 API는 pane을 복구하지 않으므로 전체 조건의 해법이 아니다. [Node-RED flow 편집 절](https://nodered.org/docs/user-guide/editor/workspace/flows), [R1·R2 선택행](choices.csv).

R3에서는 비밀값 존재와 편집 의도를 따로 표현하기, 변경된 키만 적용하며 형제 키를 보존하기, 기존 값 없는 새 항목에 유지 표식이 들어왔을 때 거부하기라는 선택3개를 구별했다. Node-RED의 password credential 표시, Vault PATCH, Auxx의 형제 필드 보존, Vendure의 생성·변경 구분은 비슷한 단어가 아니라 서로 다른 입력 계약을 제공한다. 그러나 node credential 계약을 global environment 전체에 곧바로 적용하거나 생략을 항상 보존으로 해석하면 안 된다. 선택을 가르는 입력은 기존 secret A/B, A 생략, A 명시 교체, 새 키의 표식, 비밀 아닌 환경변수 추가 후 Inject 편집 등이다. 모두 제안된 입력이고 실행하지 않았다. [Node-RED credentials](https://nodered.org/docs/creating-nodes/credentials), [Vault PATCH](https://developer.hashicorp.com/vault/docs/commands/kv/patch), [반례 원장](counterchecks.csv).

R4에서는 wrapper hit 영역을 제외하고 자식 handle을 다시 활성화하는 선택과 선택 상태를 거치지 않는 ID 기반 삭제를 구별했다. 후자는 삭제를 가능하게 할 수 있어도 요청의 선택 동작을 보존하지 못하는 근접 오답이다. `nodrag`가 클릭을 아래 요소로 재지정한다는 추론도 거부했다. R5에서는 handle 수와 ID에 따른 위치 갱신, ELK의 균일 port gap·overhang 정책, yFiles의 master 경로·간격 정책, peer group 변화 시 재라우팅 책임을 구별했다. yFiles의 두 안은 **같은 두 끝점 사이의 평행 edge**라는 해석에서만 적합하다. 원 그림이 여러 목적지로 뻗는 fan-out이라면 필수조건을 그대로 지지하지 않는다. [CSS UI §6.2](https://www.w3.org/TR/css-ui-4/#pointer-events-control), [yFiles ParallelEdgeLayouter](https://docs.yworks.com/yfiles/doc/api/y/layout/ParallelEdgeLayouter.html), [판정 교정 기록](evidence/adjudication-changes.jsonl).

R6은 Ctrl+wheel을 pan보다 앞서 분기하는 책임, wheel listener를 유지하면서 조건부 filter를 적용하는 책임, wheel을 pinch 생명주기로 바꾸는 adapter 책임을 구별했다. passive listener 진단과 활성화 키 비교는 시험이며 전체 Windows pinch 해법이 아니다. 실제 touchpad·브라우저·deltaMode·cancelability를 읽지 않은 synthetic wheel은 물리 pinch 성공을 입증하지 못한다. 이 요청의 세 선택과 다섯 시험은 판독 노출 때문에 잠정적으로만 보고한다. [D3 zoom filter·wheelDelta](https://d3js.org/d3-zoom), [Chrome wheel intervention](https://developer.chrome.com/blog/scrolling-intervention-2), [UI Events 2019](https://www.w3.org/TR/2019/WD-uievents-20190530/).

반환33행의 원 판정 종류는 새 구현결정15행, 새 판별시험만12행, 근접 오답5행, 근거 부족1행이다. 행 수와 중복 제거된 선택·시험 수는 다르다. 근접 오답에도 판별 가능한 대안이나 시험이 있을 수 있어 `novelty_class`만으로 새 선택 수를 합하지 않는다. 원문 작성자가 이미 제시한 Rename→Edit, `zoomOnPinch=true` 재제안에는 새 구현 실적을 주지 않았다. 동일 주장 말바꾸기와 같은 선택·시험은 `choice_key`와 `test_key`로 합쳤다.

## Q6. 당시 이용 가능성과 가까운 오답

현재의 공식 문서·소스라는 사실은2024년1월의 문구·버전 가용성을 보장하지 않는다. Auxx 자료는2026년, 읽은 Vendure 판은2026년 편집, CSS UI4 판은2026년1월20일 초안이다. 2021년 CSS 판에서 해당 pointer-events 문구를 찾지 못한 것을 당시 브라우저가 기능을 지원하지 않았다는 증거로 해석하지 않는다. React Flow12.4.2 자료를2024년1월 요청 당시의 v12로 소급하지 않는다. 현재 API, package 판, 원 소스 commit 날짜, 문서 편집일을 각각 남겼다. Chromium 인코더297980d7의2018년6월4일 metadata는 독립 판독에서 읽었다. 3b54b6aa는 원 검색의 R6-B-S6에서2018년10월12일 tree 날짜를 읽었지만 나중 독립 재열람은 실패했다. 검색 중 날짜 확인과 재열람 실패를 함께 보존하며 시간대·최초 도입·신고자의 Chrome120 배포 경로는 여전히 미확인이다. [각 후보 역사 판정](candidates.csv), [R4–R6 시점 판독](evidence/blind/r4-r6/sources.jsonl).

Vault의 versioned1.15 경로는 PATCH/CAS 본문을 반환했지만 내비게이션에는1.16 이전 문서를 제공하지 않는다는 상충 문구가 있었다. GA 발표는 PATCH 절을 직접 입증하지 않는다. 따라서 당시 동일 문구의 고정 원문을 확보한 것으로 세지 않는다. 현재 적합성과 역사적 이용 가능성을 분리하는 이유가 실제로 드러난 사례다. 모든 후보에서 같은 구성의 입력과 실패 전제를 남겼으며 원전의 조건을 충족하지 못하면 보류했다.

| 요청 | 별도 계보에서 찾은 가장 강한 반례 | 이 반례가 막는 성급한 결론 |
| --- | --- | --- |
| R1 | GNU `msgcmp`는 msgid 집합 일치를 검사하지만 번역의 의미 적합성을 보장하지 않음 | 번역 키가 모두 있다는 이유로 Edit 의미가 전달된다고 채택 |
| R2 | Playwright actionability에서 opacity0은 visible일 수 있고 editable·hit target은 별도 | DOM 존재 또는 visible 판정 하나로 pane 사용 가능성을 확정 |
| R3 | Kubernetes SSA에서 유일 소유자가 빠뜨린 필드는 삭제·기본화될 수 있음 | partial update의 생략은 제품·소유권 계약에 상관없이 항상 보존 |
| R4 | Qt NoButton은 아래 item으로 전달하지만 해당 item의 press/grab·drag 경로를 바꿈 | click-through를 켜도 선택·drag·삭제가 자동으로 보존 |
| R5 | Cytoscape의 자동 parallel bezier와 수동 제어점은 다른 계약 | 동일 끝점 평행 edge 해법을 미확인 fan-out 그림에 그대로 적용 |
| R6 | W3C UI Events의 trusted·cancelability·deltaMode 구분 | 합성 wheel 한 번이 실제 Windows touchpad pinch 성공을 입증 |

이 표의 원전6개는 모두 발굴 종료 뒤 읽었으며 원 검색의 발견 실적에 넣지 않았다. 각 정확한 절·실패 입력·예상 출력·미실행 상태는 [counterchecks.csv](counterchecks.csv)와 [사후 원전](evidence/postsearch/sources.jsonl)에 있다. 소스의 규격 반례를 읽은 것과 원 프로젝트에서 실패를 실행 관측한 것은 별도다.

## Q7. 실제 후속 선택과 추천의 효과

두 검색의 원격 봉인 뒤 같은6개 issue의 댓글·timeline·관련 PR·릴리스를 읽었다. 읽은 댓글24개와 timeline event76개, 성공 응답42개에는 빈 collection9개도 포함된다. 접근 실패4개를 숨기지 않았다. 사건 내부의 여러 URL은 새 원자료 수를 늘리지 않았다. [aftermath.csv](aftermath.csv), [원 후속 독해](evidence/aftermath/sources.jsonl).

R1은 GogoVega의 PR4506을 knolleary가2024년1월5일 병합했고3.1.4 릴리스에 들어갔다. 실제 변경은 기존 `menu.label.edit`를 재사용하고 `core:edit-flow`를 유지하며 쓰지 않는 rename 키를9개 locale에서 제거한 것이다. 이는 원 요청자가 이미 제안한 방향이다. PR 작성자의 `npm run test` 통과 표시는 작성자 진술이며 독립 실행로그나 camueller의 재시험이 아니다. R3은 changed-only credentials를 완전 map처럼 처리한다는 기여자 진단, commit58e2fcbe 및 PR4526, 같은3.1.4 릴리스까지 연결된다. 원 요청자 kanunnikau의 재시험이나 회귀시험 실행로그는 읽지 못했다. [PR4506](https://github.com/node-red/node-red/pull/4506), [PR4526](https://github.com/node-red/node-red/pull/4526), [3.1.4](https://github.com/node-red/node-red/releases/tag/3.1.4).

R2만 원 요청자 goldriver2의 명시적 복구 진술이 있다. Node.js를 올린 뒤 동작했지만 본인도 원인을 의심했다. opening post의18.16.1과 후속의18.6이라는 문자열 불일치를 유지했다. 콘솔 기록이나 통제된 before/after가 없어 업그레이드의 인과효과도 확정하지 않는다. R4는 maintainer의 helper 제안과 닫힘이며 실제 snippet의 `selected:false`를 편의상 true로 고치지 않았다. R5 역시 custom edge 예시와 닫힘이며 자동 간격 구현·당사자 실행 증거는 없다. [R2 진술](https://github.com/node-red/node-red/issues/4507#issuecomment-1874067118), [R4 제안](https://github.com/xyflow/xyflow/issues/3757#issuecomment-2310479396), [R5 제안](https://github.com/xyflow/xyflow/issues/3758#issuecomment-1875259548).

R6은 maintainer의 제한된 Windows11/Parallels 시험 진술, macOS 전용 gate를 제거하는 PR4229/4230과11.11.3 릴리스가 있다. 그러나 원 요청자의 수정 뒤 재시험은 없고 다른 사용자의 초기 긍정 진술 철회, 실제 Windows touchpad 실패, 이후 느린 zoom 보고도 있다. `12.0.0-next.17`은 편집된 maintainer 댓글 진술만 확인했으며 해당 릴리스 개봉 실패를 공개했다. 닫힘·릴리스·한 환경의 성공만으로 전체 원 조건이 해결됐다고 판단하지 않는다. [PR4230](https://github.com/xyflow/xyflow/pull/4230), [11.11.3](https://github.com/xyflow/xyflow/releases/tag/11.11.3), [느린 zoom 후속](https://github.com/xyflow/xyflow/issues/3759#issuecomment-2202581188).

공개 패치와 릴리스로 연결된 요청은3/6, 원 요청자의 명시적 복구 진술은1/6이다. **이번 추천을 전달받아 같은 제안을 배워 실행한 사건의 판정 가능한 분모는0**이다. 이번 결과는2026년11월에 생성되었고 후속 행동은2024년 사건이므로 시간 순서만으로도 이번 추천의 원인 효과가 될 수 없다. 직접 메시지나 외부 연락을 하지 않았다. 원 개발자의 작업시간·절약시간도 미확인이다. 운영 선행105의 좁은 기능 최초인지2건과 동일 제안 학습→실행 분모0을 이번6건의 양성 결과로 상속하지 않는다.

## 추가 분석: 외부 분야의 전이는 어디서 깨지는가

사후 보조층은 기록보존에서 OCFL1.1과 Library of Congress PREMIS3.0 공식 XSD, 제조 품질검사에서 NIST LASP와 MIL-STD-1916 원문을 읽었다. 추가로 W3C PROV-DM의 revision 정의를 확인했지만 배당 수를 늘리지 않았다. PREMIS PDF는429/403으로 읽지 못했으므로 읽었다고 쓰지 않고 공식 저장소의 고정 XSD를 대체 원전으로 명시했다. MIL-STD-1916은 공식 DLA에서 받은33쪽 PDF의 해당 본문과 도표를 직접 읽었다. 웹 도구의 재작성 요약을 그 PDF 독해 대신 산입하지 않았다. [전이 원장](external-transfer.csv), [실제 도착 주소와 실패 경로](evidence/postsearch/sources.jsonl).

OCFL의 version state와 digest는 어느 바이트가 어느 버전에 속하는지 고정하는 데 유용하다. 하지만 언제 새 버전을 만들지, credential 생략이 삭제인지 유지인지, 기능이 성공했는지는 정하지 않는다. PREMIS는 event·outcome·agent·object를 구별하게 하지만 공식 XSD에서 outcome·연결 agent/object는 선택적이다. schema-valid 파일이 있다는 이유만으로 실행·검증 주체가 완비되었다고 간주하면 실패한다. 이 두 원전은 이번 원장에서도 판·주체·실행 결과를 서로 다른 열로 유지해야 할 이유를 제공한다. [OCFL §3.6–3.7](https://ocfl.io/1.1/spec/), [PREMIS 고정 XSD](https://github.com/LibraryOfCongress/premis-v3-0/blob/3b79c30136c0f6ed673dd6ec9c9830d55730d889/xsd).

NIST의 acceptance sampling은 표본에서 accept/reject/resample을 결정하고 생산자·소비자 위험을 구별한다. MIL-STD-1916의 무작위 표본과 무결점 인수 규칙, 부적합 lot의 시정 책임도 확인했다. 하지만 순위가 매겨진 동적인 웹 검색 결과는 정의된 제조 lot의 무작위 표본이 아니다. 검색 결과6개 중 적합 후보가 없었다고 웹 전체에 후보가 없다고 결론 내리거나, 발견 수로 웹 재현율을 계산하는 전이는 거부한다. [NIST §6.2.2](https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc22.htm), [MIL-STD-1916 공식 원문 경로](https://quicksearch.dla.mil/WMX/Default.aspx?token=41416), 정확한 PDF 절은 sources의 `EXTERNAL-MIL1916` 행을 따른다.

이 네 원전은 유용한 보조 점검을 제공했지만 A/B가 그 분야를 스스로 발견했다는 실적은0이다. 검색전략의 결과, 연구자가 뒤에 읽은 타 분야 원전, 제안된 실패시험, 실제 원 개발자 행동을 한 성공 점수로 합치지 않았다.

## 검산·재개 경계

필수 세 표는 [recalculate.py](recalculate.py)가 requests·baseline·candidates·choices·costs·aftermath 원장에서 재생성한다. [SELF_CHECK.md](SELF_CHECK.md)는 Q별 답과 반례 경로, 판독 주체·시각·본 정보, 뒤집힌 행, 중복과 결손을 확인한다. [수용 근거](evidence/acceptance-evidence.json)는 각 체크의 파일·판·주체·관측·미달을 기록한다. 검산은 raw 검색48파일과 검색 봉인 SHA, baseline의 최초 열과 모집 봉인 SHA,36자리·33반환·3공석·출처 산입·독립성 상태를 대사한다. 입력·원장 검산 통과는 실제 설계 제안의 실행 성공을 뜻하지 않는다.

검사 대상 결과판을 먼저 원격 고정하고 그 SHA에서 manifest·공통 검사·작업별 검산을 실행한다. 실제 명령·환경·종료값·자동 발견 세션 수는 이후 영수증과 마지막 [HANDOFF.md](HANDOFF.md)에 기록한다. 이 결과 본문 작성 시점의 예정 명령을 실행 근거로 사용하지 않는다. 미실행 제품 시험의 입력과 실행 절차는 [EXECUTION_PLAN.md](EXECUTION_PLAN.md), 전체 재현은 [reproduce.md](reproduce.md)를 따른다. 재개 첫 행동은 최초 작성판과 관측 가능한 동일 실행 환경을 확보할 수 있는지 확인하는 것이다. 새 조건이 마련되면 새 봉인으로 재실행하며 현재 기록을 성공으로 소급 변경하지 않는다.

| 불일치·약점 | 다음 조사·직접 열 자료 | 어느 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 최초 본문판0/6, R2 약한 조건쌍, R5 제목 편집·그림 topology 미확인으로 역사적 입력이 고정되지 않음 | 여섯 issue의 공개 최초 편집판과 R5 event11365940209·원 첨부를 직접 대조하고 baseline을 새 봉인 | 생성시점 원문에서 두 조건·기지 안이 확인되고 특히 R5가 같은 끝점 평행 edge인지 판명되면 해당 요청의 입력·적합 자격을 재판정 |
| immutable 모델·자동 개봉 미관측, R2/R6 후속 노출, R3-B prefix 순서 불일치로 엄격 비교분모0 | 동일 모델 ID·완전 노출 영수증을 제공하는 환경에서 동일6문장과 교대순서를 새 문맥으로 재실행하고 사건 순서를 원 로그로 확인 | 실제 모델·노출·순서가 검증되고 후속 가림이 유지된 쌍만 엄격분모에 포함; 원전 취득 prefix를 성공으로 소급하지 않음 |
| 선택12·시험27은 조건부·미실행이고 R6은 잠정; 당시판·원 요청자 실행·추천 인과효과가 미확인 | EXECUTION_PLAN의 원 버전·최소 입력으로 UI/credential/edge 시험과 실제 Windows touchpad 기록을 수행하고 고정 릴리스·CI·기존 당사자 진술을 직접 읽기 | 두 필수조건을 같은 실행에서 보존한 결과와 실패 대조가 나오면 기술 적합성을 갱신; 추천 노출 뒤 동일 주체 실행·시간 자료가 있어야 채택·절감 판단을 갱신 |
