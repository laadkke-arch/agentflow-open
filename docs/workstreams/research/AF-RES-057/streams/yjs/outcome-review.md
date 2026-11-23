# Yjs 결과와 반증 검토

봉인 SHA는 `74dc9f887bc47bc0a92b9a75ea327ffa30aca70b`이고 원래 가린 assertion은 2026-11-23T03:32:32.205236+00:00에 처음 읽었다. 연구 재실행14개는 모두 완료했다. 공개 원시험 runner 실행은0, 선택 사례의 공개 A/B+redo 전체 기대 fixture 확보는0이다. 이를 섞어 3/3 역사적 사례 검증이라고 쓰지 않는다. 자연 두 자리의 원래 실행판/완전 입력 또는 비노출 조건은 불충분하고, 시험 자리에서는 고정판의 A undo 기대값만 직접 선언되어 있다.

## Q1 — 사람, origin, 사건 단위는 서로 다르다

[요청157](https://github.com/yjs/yjs/issues/157)은 보호할 문장을 정확히 제시하지만 초기 문서와 일반 편집의 주체·순서는 주지 않는다. 연구자가 추가한 ordinary/protected 두 사건을 원래 요청으로 소급하지 않았다. [뒤의 유지관리자 제안](https://github.com/yjs/yjs/issues/157#issuecomment-505416645)은 별도 origin으로 감싸는 것이다. YN1 재실행에서 순서를 바꾸면 첫 undo의 보이는 텍스트는 같아도 undo 깊이와 두 번째 undo 결과가 달랐다. 동일 사람이 null origin으로 두 사건을 만들면 보호 문장이 자동으로 보호되지 않았다. 따라서 이름이 같은 사용자라는 정보 대신 추적 원점과 사건 경계가 필요하다.

## Q2 — 실제 호출과 판의 제한

2019년 호환 프리릴리스는 tracked origin Set을 두 번째 위치 인자로 받는다. 현대 options 객체를 소급하면 다른 조작이다. [그 판의 실제 constructor/filter](https://github.com/yjs/yjs/blob/dd2b8bc6c79d98e2fb8d773339d9de7532114eba/src/utils/UndoManager.js)는 호출 가능한 비교를 제공하지만 작성자의 실제 판까지 증명하지 않는다. [13.0.8의 gc 설명](https://github.com/yjs/yjs/blob/772bb87d5cfcc4d9e87ba970731c6aa58f6809bf/README.md)은 삭제 payload 보존 가능성을 주며 private stack 이동의 계약은 주지 않는다. YN2 A/B는 두 문서에 적용하는 공통 gc 값 하나만 바꾼다.

## Q3 — 수신 분야 자료로 이미 갈리는 것과 멈추는 것

YN1 A와 A+E는 origin membership의 같은 결론을 냈고, YT1 A와 A+E는 stopCapturing의 같은 그룹 경계를 예측했다. 전체 implementation/README를 읽은 창 밖 지식은 기록되어 있으므로 짧은 카드만 읽은 사람의 효과라고 주장하지 않는다. YN2는 A/E 모두 판별 불가로 봉인했다. 후속 gc=false 성공은 그 보류를 새 정답으로 바꾸지 않는다. [독립적인 저자 작업 예제](https://discuss.yjs.dev/t/infinite-drawing-app/789/4)는 연결되지 않은 yLine의 set과 문서에 삽입하는 push를 구별한다. 문법상 transaction 두 개라는 수만으로 undo 그룹이나 효과 두 개를 예측해서는 안 된다. 이 예제는 결과 후 읽었으며 E를 대체하지 않았다.

## Q4 — 지도/회계 대응의 적용 지점과 경계

외부 원전과 대응표는 부모 조사에서 합친다. Yjs 쪽에서 요구하는 추가 변수는 원래 삽입 ID/현재 효과/상대 편집/undo 가능한 항목/redo 후 순서다. 화면 텍스트가 없어지는 것, payload가 GC되지 않는 것, 정정의 감사 기록이 남는 것은 서로 다른 조건이다. YN2의 gc=false는 삭제된 payload를 남겨 복원을 가능하게 했으나 감사 원장·지원되는 history 직렬화를 보장하지 않는다. [유지관리자 답변](https://github.com/yjs/yjs/issues/204#issuecomment-637678031)은 keep 표시 자체가 DB나 동료에게 전파되지 않는다고 설명한다. 회계의 원기록 존속을 곧바로 Yjs 객체 ID나 history 이동 성공으로 대입할 수 없다.

## Q5 — 원래 보류와 노출을 유지

YN1 A/E의 조건부 연구 입력 예측과 YT1의 고정판 예측은 실제 연구 출력과 일치했다. YN2는 원문에서 삭제 실패 및 삽입 control의 기대123을 보았다. 후속 출력은 삭제 A=`123 World`, B=`Hello123 World`이고, 원문의 대략적인 기대 `~"Hello 123 World"`와 동일한 정확 공백 명세가 아니다. 카드 A/E의 판별 불가를 유지하며 새 적중으로 세지 않는다. D의 봉인 예측은 중앙 predictions.csv에 그대로 둔다.

## Q6 — 원본 assertion, 수정, 실행을 분리한 반례

[선택 시험](https://github.com/yjs/yjs/blob/0a09ff854b2ecd942b3c0f0e741253a214cee1bf/tests/undo-redo.tests.js)은 A undo=[1,2,3]만 선언한다. [그 시험을 추가한2022 수정](https://github.com/yjs/yjs/commit/7395229086d9d4db06ebd5936bdd326dbe346834)은 lastChange>0 조건을 넣는다. 결과를 읽은 뒤 같은 입력을13.0.8에 적용하니 stopCapturing이 있어도 A/B 모두[]였다. 따라서 API 문장과 일반 예제만으로 모든 판·극단 timeout에서 구현 성공을 보증하지 못한다.

[원격 map 변경 정책](https://github.com/yjs/yjs/commit/a22b3cdbc1ee975c023d78725f521f250b7020c2)은 설정에 따라 후행 상대 값4를 덮어쓰고 값2로 돌아가는 시험을 담는다. 추적 원점과 이후 원격 값 보호는 같은 옵션이 아니다. [텍스트 formatting 수정](https://github.com/yjs/yjs/commit/abf3fab1b6a479d01d688bb0d5dd7678aec695c6)은 같은 문자열을 유지해도 두 동료의 bold delta가 달라질 수 있음을 다룬다. [외부 변경 후 복원 사례](https://discuss.yjs.dev/t/undomanager-with-external-updates/454)는 원격 복원이 새 삽입으로 보이므로 동일한 화면 내용이 원래 편집 이력의 소유를 보존하지 않을 수 있음을 설명한다. 그 뒤의 실제 [stack 순회 수정](https://github.com/yjs/yjs/commit/9e98fec5042fd348304fd70b12172cc84409ec37)은 유효한 변화가 생길 때까지 항목을 넘겨야 한다는 별도 오류를 고친다. 토론과 같은 fix/test는 한 사건 계보다.

네 fix 계보의 출처는 읽었지만 CI 통과를 관측하지 못했다. 조사한 tag와 세 수정 SHA에 retained statuses/check-runs가0개이고 tag의 actions run도0개다. API aggregate pending+0records를 실행 중인 시험이라고 해석하지 않는다. 이 결과의 한계는 `ci-probes.json`에 있다.

## Q7 — 마지막 링크와 뒤집힐 조건

YN1의 구현 선택에는 당시 origin API, YT1에는 해당 판의 stopCapturing test/fix가 직접적인 링크다. YN2에는 gc 설명과 저자 후속 답변을 반환하되 private stack 전달의 지원 여부·항목 ID·정확한 입력을 더 확인해야 한다. 지도·회계 원리는 보존 목표를 명시하는 질문을 보완할 수 있으나 Yjs의 호출 규약이나 불충분한 GC/history 계약을 대신 확정하지 못한다.

판정을 뒤집을 최소 자료는 YN1 작성자의 실제 버전과 완전 사건열, YN2 같은 입력 A/B+redo를 선언하고 실행한 지원 API 시험, YT1 고정 SHA의 공식 runner/CI 결과다. 단, YT1의 B/redo가 공식 fixture에 없다는 사실은 CI 통과만으로 보완되지 않는다. [origin 설명의 저자 정정 사례](https://discuss.yjs.dev/t/detecting-a-transaction-made-by-undo-redo-in-y-prosemirror/1393)는 유지관리자 해석도 버전·실행 근거 앞에서 바뀔 수 있음을 보여 준다.

## 자체 검토 범위

Yjs 연구 에이전트가 원문 입력·metadata·사전 봉인·후속 assertions·연구 출력·출처 계보를 검토했다. 부모 에이전트는157/204 원문과 마스킹 선택 교정, 중앙 카드/예측 및 출력 통합을 검토한다. 별도 감사 에이전트가 지적한 Y-T-DIAG input-only eligibility와 YN1-A code-line metadata는 사후 오류 정정으로 남겼다. 재검토는 사람 독자의 수행 실험이나 역사적 채택 이유의 증거가 아니다.
