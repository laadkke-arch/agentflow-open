# 고정 실행 판정표

세 실행은 문서 창 밖의 보조 진단이다. 두 정상, 하나 근접음성, 하나 금지 동작/손실을 그룹별로 실행하고 전후 입력을 비교한다. 원 요청자가 성공했는지는 미확인이다. 지지의 단위는 fixture와 실제 고정판이다.

| 고정 후보판 | 정상 P1·P2 | 근접 N1 | 금지 동작 G1·판정 |
| --- | --- | --- | --- |
| JS-6/SC-005 Ajv `9050ba1359fb87cd7c143f3c79513ea7624ea443` | 인수한 draft-07 schema, type=article/id="1" 및 "2" 허용 | id 숫자 1 거부, id 제약 진단 | 빈 객체 허용, required 임의 추가 금지. allErrors=true, coerceTypes/useDefaults/removeAdditional=false. 네 입력 모두 같은 입력 바이트(직렬화) 유지. |
| JS-3/SC-027 jschon `eb0782c98e16d9b562e48fbf9dce2c936b2c7512` | Person 남/여 허용, 외부 types.json→gender enum 참조 사용 | 나머지 필드를 갖춘 채 enum 밖 값 거부 | name/surname/sex/email을 각각 하나씩 제거한 네 변형 모두 거부, 입력 유지. 원 draft-04 + $id와 코드의 문제 있는 추출 경로를 유지하는 실행을 우선하고 실행되지 않으면 오류를 그대로 남긴다. 별도 명시적 2020-12 재구성은 같은 네 입력에 대한 능력 진단이다. Node/TypeScript/Ajv 충족 집계에서 제외한다. |
| LD-3/LD-008 Ruby JSON-LD `652730747e70f44f71ab7331f111c4308fe25b5c` | 원래 a=1 행 또는 순서가 바뀐 a=1 행만 선택. 각 행의 b/c와 credential subject·issuer·날짜·type 등 구조/값 보존 | a=1을 포함하지 않는 입력, 일치 값 목록이 비거나 선택 없이 실패해야 한다. 엔진 오류는 필터 지지로 세지 않는다. | 선택 행의 b/c 및 credential 날짜를 고정된 새 값으로 바꿔서 값 손실·다른 행과 결합·임의 정규화 여부 검사. 원문 @nest와 원 frame의 문서형을 우선한다. 별도 명시적 노드 관계는 능력 진단이고 원래 context 재현 성공으로 보고하지 않는다. |

JS-3은 [요구 본문 rev1](https://stackoverflow.com/revisions/65726164/1)의 두 스키마 및 TS의 `properties` / `definitions.person` 추출 위치를 기록했다. 예제 이메일은 공개 예시 도메인의 합성 값이다. LD-3은 [요구 본문 rev1](https://stackoverflow.com/revisions/65917156/1)의 코드 블록 세 개를 토대로 필요한 데이터와 frame을 고정한다. 원 @context 배열에서 작성자가 가정한 URL은 원문이 제시한 JSON을 로컬 loader에 제공한다. 나머지 원 URL에 대한 공개 응답을 식별하고 고정하되 응답 결손을 다른 @context로 자동 치환하지 않는다.
