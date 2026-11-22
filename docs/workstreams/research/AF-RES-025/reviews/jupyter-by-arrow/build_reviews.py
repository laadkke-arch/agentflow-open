"""Rebuild this masked review from its manually authored judgments.

Reads only the assigned blind packet; never joins route/rank/return mappings.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PACKET = BASE / "blind/jupyter.jsonl"
EXPECTED = "60d0dcfafa3297f8e572aa5fc41617e302df3130b58412b105d61e948e6bc524"
assert hashlib.sha256(PACKET.read_bytes()).hexdigest() == EXPECTED

# Per condition: supported / unknown / conflict, followed by the actual reason.
# These judgments were written after reading the assigned initial inputs and
# packets; the important originals were reopened separately in audit receipts.
D = {
"B-06b02d84d2b9": {
 "p": [("unknown", "응답 전에 매칭을 시작한다는 관측은 등록 순서의 근거다. 그러나 별도 수신 경로의 준비를 클라이언트가 관측했다는 근거까지 제공하지 않는다."), ("unknown", "수신기를 먼저 준비하고 응답 뒤 실행한다는 순서는 연구자의 제안이다. 해당 전송 경로의 준비 완료가 응답 이전임을 보장하는 계약이 필요하다.")],
 "pick": [[1,2],[1,2]], "audit": ["RVJ-001"],
 "fact": "구독 ID, 활성 구독의 매칭 및 SubscribeResponse 이전 매칭 시작은 패킷의 원문 관측이다.",
 "counter": "제어 요청은 성공했지만 통지 목적지 연결이 아직 수립되지 않은 구현이면, 활성 매칭 뒤 첫 통지의 단회 전송이 실패할 수 있다.",
 "note": "초안·비규범 PDF라는 지위 때문에 탈락시키지 않았다. 독립 재열람 3회는 403/HTML 대체 응답으로 본문 확보에 실패했다. 전송 규약이 준비 보장을 제공한다면 판정이 달라진다."
},
"B-2ad4d1b4fe30": {
 "p": [("unknown", "발행자가 구독자의 수신 상태를 모른다는 패턴 설명은 준비 신호의 구현 근거가 아니다."), ("unknown", "request-reply를 추가할 수 있다는 권고만으로 출력 경로와 연결된 실행 gate가 성립하지 않는다.")],
 "fact": "문서는 비동기 분배의 손실 가능성과 응답이 필요한 경우의 별도 패턴을 설명한다.",
 "counter": "명령 처리기의 응답은 도착했으나 별도 출력 subscriber의 등록은 늦을 수 있다."
},
"B-2dc7ccbffe3c": {
 "p": [("unknown", "별도 request-reply 경로는 subscriber 상태를 알릴 가능성을 제공하지만 준비 완료 상태의 정의가 없다."), ("unknown", "제어 응답과 실제 출력 구독 사이의 선후 관계가 명시되지 않아 첫 출력 이전 gate를 검증할 수 없다.")],
 "fact": "일방향 pub/sub와 상태를 회신하는 별도 경로를 구별하는 설계 원리다.",
 "counter": "상태 응답을 낸 구성요소와 아직 등록되지 않은 출력 subscriber가 서로 다른 경우에는 양 경로가 독립적으로 진행한다."
},
"B-8072600fac36": {
 "p": [("unknown", "queue group의 수신자 분배는 subscription readiness의 관측 신호를 제시하지 않는다."), ("conflict", "여러 queue member 중 하나에게만 전달하는 사용은 특정 클라이언트가 최초 출력을 받는 보장을 깨뜨린다.")],
 "fact": "동일 queue group에서는 하나의 소비자로 분배하며 일반 fanout과 다르다.",
 "counter": "두 클라이언트가 같은 queue group에 있으면 첫 출력은 다른 member로 갈 수 있다."
},
"B-c5d0c525d551": {
 "p": [("unknown", "구독 생성 이후의 메시지를 보관한다는 사실과 생성 완료를 관측하는 신호의 계약은 다르다. 인용된 개요에는 후자가 없다."), ("unknown", "이미 생성된 구독의 보관은 손실 회피에 유용하지만, 그 생성 완료를 확인한 뒤 실행한다는 요청 순서의 근거가 부족하다.")],
 "audit": ["RVJ-011"],
 "fact": "subscription-overview는 구독 생성 이후 발행분의 제공과 전달 후 ACK를 구별한다.",
 "counter": "구독 생성 요청을 제출한 직후 완료 확인 없이 실행하면, 생성 완료보다 앞선 첫 발행분은 제공 대상에서 빠질 수 있다.",
 "note": "두 패키지는 다른 개요 URL을 인용하므로 합쳐서 보강하지 않았다. RVJ-011은 subscription-overview 패키지만 직접 재확인했다."
},
"B-cb7808ad0554": {
 "p": [("unknown", "durable subscription의 보관 성질은 최초 구독 준비를 클라이언트가 관측하는 절차가 아니다."), ("unknown", "이미 존재하는 구독에 대한 보관은 확인되지만 구독 생성과 첫 실행의 동기화는 인용 절에 없다.")],
 "fact": "topic 복제 및 durable subscription의 보관을 설명한다.",
 "counter": "최초 출력 뒤에 durable subscription을 처음 만들면 기존 보관 보장만으로 그 출력을 복구할 수 없다."
},
"B-e148d3383916": {
 "p": [("unknown", "challenge GET 수신은 callback의 접근 가능성을 보여 주지만 hub가 응답을 검증하고 구독을 활성화했다는 후속 신호는 아니다."), ("conflict", "subscriber가 challenge에 응답한 직후 실행하는 순서는 hub의 검증 완료보다 앞설 수 있어 최초 출력의 gate로 충분하지 않다.")],
 "pick": [[0,1,2],[0,1,2]], "audit": ["RVJ-002"],
 "fact": "202와 후속 검증은 분리되며, hub는 challenge 응답을 검증한 뒤 상태를 바꾼다.",
 "counter": "subscriber가 echo를 전송한 직후 실행 요청이 hub의 echo 수신·검증보다 먼저 처리되는 일정이 규약상 가능하다.",
 "note": "연구자 제안은 202를 readiness로 쓰지 않는다. 이 판정은 그보다 강한 callback-verification 제안에도 남는 경쟁을 대상으로 한다. 초안 지위는 탈락 사유가 아니다."
},
"B-eb88c394616d": {
 "p": [("unknown", "READY는 필요한 수의 ACK 연결을 publisher가 관측하는 신호다. 이것이 해당 출력 수신 경로의 준비와 같은 상태라는 대응이 추가로 필요하다."), ("unknown", "입력 발행을 READY 뒤로 미루는 규칙은 있으나, 실행 요청과 가변 개수 출력으로 옮기는 사용의 손실 회피는 확인되지 않았다.")],
 "audit": ["RVJ-010"],
 "fact": "READY 대기와 입력 블록 하나당 출력 블록 하나라는 보장 전제가 명시된다.",
 "counter": "한 실행이 출력 0개 또는 여러 블록을 내면 문서의 1입력:1출력 ACK 대응이 그대로 유지되지 않는다.",
 "note": "publisher라는 명칭만으로 주체 불일치라고 단정하지 않았다. 사용자가 입력 publisher와 출력 subscriber를 겸하는 대응은 가능하지만, 해당 연결과 블록 대응 근거가 원 패키지에 없다."
},
"B-511f8125b6a8": {
 "p": [("supported", "청취 중인 동적 포트를 다른 클라이언트에 재할당하지 않는 자원 소유 규칙을 확인한 패킷 관측을 사용한다."), ("unknown", "발견 수단의 열거가 실제 바인딩 완료 후 시작 주체에 회신하는 순서를 모두 규정하지는 않는다."), ("unknown", "다중 커널·채널 식별 및 후속 클라이언트용 정보 갱신 경계가 해당 절에서 확인되지 않았다.")],
 "fact": "동적 포트의 사용 중 재할당 금지와 구성파일·IPC·DNS 발견을 다룬다.",
 "counter": "이전 프로세스의 포트가 적힌 구성파일을 새 프로세스의 정보로 읽으면 포트 충돌을 피했어도 다른 커널에 접속할 수 있다.",
 "note": "구현이 없다는 이유로 배제하지 않았다. 2022 Release17 문서를 2021 입력의 당시판으로 취급하지 않는다."
},
"B-8dab70c937e3": {
 "p": [("supported", "BIND 첫 회신은 실제 소켓 생성·바인딩 뒤 이뤄진다."), ("supported", "첫 회신으로 실제 bound address/port를 받은 뒤 상대의 연결을 유도하는 관계가 성립한다."), ("unknown", "세션별 BIND 응답만으로 다중 커널·채널의 재사용 가능한 발견 정보를 제공하지 않는다.")],
 "fact": "첫 BIND 응답과 실제 인입 연결 결과를 알리는 두 번째 응답을 구별한다.",
 "counter": "첫 BIND 회신을 재사용용 주소 원장으로 저장해도 제어 세션 종료 뒤 같은 endpoint의 지속성을 보장하지 않는다.",
 "note": "SOCKS의 바인딩 주체와 요청 주체를 실행 주체·시작 주체에 대응한 설계 선례 범위에서 P1/P2를 인정한다."
},
"B-a130cf2b54b3": {
 "p": [("supported", "listen(0)는 실제 서버 바인딩을 유지하며 listening 이후 address().port를 읽을 수 있다."), ("supported", "자식이 실제 주소를 process.send로 보내고 부모의 message 이벤트 뒤 연결하는 조합은 인용된 API들로 구성된다."), ("unknown", "다중 프로세스·채널 이름과 후속 클라이언트가 읽는 manifest는 연구자가 추가해야 하며 인용된 API 계약 자체에는 없다.")],
 "pick": [[0,1,2],[1,3,4],[5,6]], "audit": ["RVJ-003","RVJ-004"],
 "fact": "OS 배정 포트 조회와 자식→부모 IPC를 제공하고 이미 열린 서버 핸들도 전달할 수 있다.",
 "counter": "자식이 보고 후 종료하거나 다른 자식의 포트와 연결정보를 섞어 저장하면 재접속 클라이언트가 올바른 채널을 찾지 못한다.",
 "note": "send callback을 부모의 수신 완료로 해석하지 않는다. 부분 handshake는 유효하나 전체 질문의 P3는 보류다."
},
"B-b086270464d1": {
 "p": [("supported", "서버가 동적 포트를 bind하는 관계가 정확한 원문에 있다."), ("supported", "그 포트를 구성파일·IPC 등 내부 수단으로 클라이언트에 알려 주는 관계가 있어 설계 선례로 성립한다."), ("unknown", "여러 커널·채널을 구별하는 정보 구조 및 후속 클라이언트의 갱신·재사용 규칙은 주어진 절에 없다.")],
 "audit": ["RVJ-005"],
 "fact": "호스트 내부의 bind→포트 전달이라는 관계를 명시하는 권고다.",
 "counter": "두 프로세스가 같은 파일의 한 포트 칸을 덮어쓰면 이 권고의 개별 bind/전달은 지키면서도 커널·채널 구별에는 실패한다.",
 "note": "원 패킷의 ‘§6 p9–10 L500–555’ 표제는 부정확하다. 재열람에서는 §7.1, 특히 L511–518와 L550–555에 해당한다. URL·쪽·행은 찾을 수 있으므로 P1/P2 인용을 무효화하지 않았다. 구현 부재 자체는 반증이 아니다."
},
"B-bc34353f2111": {
 "p": [("unknown", "원자적인 파일 registry 예약이 OS 소켓의 바인딩 보유와 동등하다는 근거는 없다."), ("unknown", "회신하는 번호가 실제 사용할 프로세스가 잡고 있는 endpoint라는 조건이 확인되지 않았다."), ("supported", "PID·tag와 복수 포트를 registry로 구별하고 조회하는 정보 구조는 제공한다.")],
 "pick": [[0,1,2],[1],[0,1]],
 "fact": "semaphore로 보호한 PID/tag 기반 할당 원장과 복수 포트 API다.",
 "counter": "원장을 사용하지 않는 프로세스가 그 번호를 OS에서 먼저 bind하면 원장의 원자성만으로 실제 포트 경쟁을 막지 못한다."
},
"B-e4a22ebb5c04": {
 "p": [("supported", "bind/listen/getsockname 이후 매핑을 요청하므로 로컬 endpoint를 먼저 확보한다."), ("supported", "실제 매핑 회신 이후 외부 발견 정보를 게시하는 관계가 설계 선례로 제시된다."), ("unknown", "주소 게시 방식이 범위 밖이며 여러 커널·채널과 후속 클라이언트의 정보 연결은 규정하지 않는다.")],
 "fact": "로컬 바인딩→매핑 회신→rendezvous 갱신 순서다.",
 "counter": "하나의 rendezvous 항목에 여러 커널의 매핑을 덮어쓰면 각각의 포트 확보는 성공해도 후속 클라이언트는 필요한 채널을 구별할 수 없다.",
 "note": "P2는 이 순서의 관계 대응을 인정한 것이다. Jupyter launcher 구현이 이미 제공된다는 뜻은 아니다."
},
"B-e53fa84614ac": {
 "p": [("supported", "해당 Windows 판·주소 조건에서 bind 전 독점 옵션을 설정하고 실제 바인딩을 유지하는 방식이다."), ("unknown", "독점 바인딩 옵션에는 시작 주체로 실제 주소를 회신하는 동작이 없다."), ("unknown", "여러 채널의 발견·재접속 정보를 공개하는 기능은 해당 옵션의 계약 범위 밖이다.")],
 "pick": [[1,2],[0,1,2],[0,1,2]],
 "fact": "SO_REUSEADDR와 SO_EXCLUSIVEADDRUSE의 소유·충돌 조건을 OS별로 구별한다.",
 "counter": "소켓을 안전하게 독점해도 부모에게 번호를 통지하지 않으면 부모는 어느 포트로 연결할지 알 수 없다."
},
"B-f254a168210a": {
 "p": [("supported", "bind 뒤 listen 전에도 포트 소유를 보호해야 한다는 규칙은 탐색과 사용 사이 공백을 줄이는 근거다."), ("unknown", "포트 배정의 소유 제약은 실제 주소를 시작 주체에 회신하는 절차를 포함하지 않는다."), ("unknown", "다중 채널 정보 원장과 후속 클라이언트의 재사용 계약은 없다.")],
 "fact": "LISTEN 상태만 보호하는 포트 배정의 허점을 지적한다.",
 "counter": "bind 소유를 지키는 서버라도 실제 주소를 폐기하면 다른 클라이언트는 포트를 발견할 수 없다."
},
"B-fdf46aebdd58": {
 "p": [("unknown", "Resolve가 반환한 후보 endpoint가 계속 바인딩되어 예약되는 자원이라는 보장은 확인되지 않는다."), ("unknown", "RendezvousDone의 연결 완료와 자식이 실제 확보 주소를 launcher에 회신하는 계약은 같지 않다."), ("unknown", "후보 교환의 외부 signaling 및 지속적인 다중 채널 정보 노출은 주어진 규약 밖이다.")],
 "fact": "endpoint 후보의 탐색과 실제 연결 준비 이벤트를 구별한다.",
 "counter": "탐색된 후보가 연결 전 만료되거나 바뀌면 Resolve 목록을 곧바로 바인딩 완료 manifest로 사용할 수 없다."
},
"B-47b9b46f13d0": {
 "p": [("unknown", "body와 params의 분리는 확인되지만 body의 셀 소스를 실행하는 요청이라는 연결은 확인되지 않는다."), ("supported", "설치된 서버 실행 handler는 요청별 params 객체를 받아 자신의 동작에 사용할 수 있다."), ("supported", "params와 불변 input 문서를 별도 인자로 받아 body에 magic을 주입하지 않고 추가 값을 전한다.")],
 "audit": ["RVJ-013"],
 "fact": "post/put(context, params, input)에서 클라이언트 인자와 요청 body를 분리한다.",
 "counter": "body에 ‘1+1’을 넣어도 저장·변환용 extension은 그것을 실행하지 않는다. 별도의 셀 실행 adapter가 필요하다.",
 "note": "P2/P3는 제안된 전송 부품의 API 경계에 한정한다. 이미 셀 실행기라는 주장으로 확대하지 않는다."
},
"B-47e08ed87846": {
 "p": [("conflict", "이 자료의 code는 GetMap 같은 operation 식별자이며 실행될 셀 소스 본문이 아니다."), ("unknown", "별도 namespace extension을 실제 실행 동작의 입력으로 소비하는 계약은 확인되지 않는다."), ("unknown", "실행 소스의 별도 전송 계약 자체가 없으므로 magic 없는 전달을 입증하지 않는다.")],
 "fact": "operation의 URL·method·payload 및 namespace extension을 기술한다.",
 "counter": "code=GetMap은 지도 작업의 이름을 정할 뿐 ‘1+1’ 같은 셀 코드와 metadata를 커널에 전달하지 않는다."
},
"B-4f391993bf95": {
 "p": [("supported", "같은 parent 메시지에서 content.code와 root metadata를 별도로 얻는다."), ("supported", "cell_meta를 받는 do_execute 서명일 때 그 값을 전달하므로 수신 하위클래스가 실행 입력으로 읽거나 무시할 수 있다."), ("supported", "code 인자는 그대로 두고 cell_meta를 별도 인자로 전달한다.")],
 "pick": [[0],[0,1],[0]], "audit": ["RVJ-006"],
 "novelty": "known_host_new_part_or_use",
 "fact": "현재 Kernel.execute_request의 metadata→cell_meta 전달 및 do_execute의 독립 인자다.",
 "counter": "최초 제안 예시대로 metadata를 content.metadata에만 넣으면 이 코드는 root metadata를 읽으므로 해당 값이 전달되지 않는다.",
 "note": "제안된 사용은 root metadata를 쓰는 클라이언트와 수신 하위클래스로 한정되어 현재 조건을 충족한다. 노트북 파일의 자동 복제·모든 kernel 지원·최초 날짜의 이용 가능성은 확인하지 않았다. ipykernel이라는 이름은 첫 문서에 없고 Jupyter host는 명시되어 있어 새 부품과 새 제품의 해석을 분리해야 한다."
},
"B-51c848af2a59": {
 "p": [("conflict", "descriptor 또는 result의 metadata를 per-cell 실행 요청의 입력 metadata로 바꾸어 세지 않는다."), ("unknown", "반환 결과의 metadata가 현재 실행을 선택하는 수신 입력이라는 근거는 없다."), ("unknown", "이 인용은 셀 소스와 별도 입력을 실행기에 전달하는 경계를 보이지 않는다.")],
 "fact": "tool descriptor, result 및 manifest의 metadata 역할을 구별한다.",
 "counter": "실행 뒤 결과에 붙인 상태 표지는 이미 수행된 호출의 실행 환경을 선택할 수 없다."
},
"B-67a1b02e55b6": {
 "p": [("conflict", "kernel 시작·선택 단위의 명세 metadata는 요청마다 달라지는 셀 metadata와 다른 경계다."), ("unknown", "인용된 metadata가 매 execute_request에서 수신 실행 주체에 전달되는 계약은 없다."), ("unknown", "시작 argv/env가 존재한다는 사실로 셀별 별도 metadata 전달을 입증하지 않는다.")],
 "novelty": "known_target_new_use_or_constraint",
 "fact": "kernelspec의 선택용 metadata 및 시작 argv/env를 설명한다.",
 "counter": "같은 kernel에서 연속 두 셀의 locale을 다르게 설정하려 해도 하나의 kernelspec metadata만으로 요청별 구별이 되지 않는다."
},
"B-73674e9635a1": {
 "p": [("unknown", "원문을 확보하지 못한 rewritten summary라 body·보조 필드 관계를 직접 확인하지 못했다."), ("unknown", "sidecar 보안 판단과 셀 코드 실행 수신자의 행동 입력이 같은 경계인지 확인되지 않았다."), ("unknown", "원문 및 실제 실행 요청 schema 없이 코드 비변경 전달을 검증하지 않는다.")],
 "fact": "패킷에는 요약 도구의 allow/block/flag 설명만 있고 원문 확보 실패가 기록되어 있다.",
 "counter": "요약의 sidecar가 tool 실행을 차단하더라도 셀 metadata는 실제 커널에 전혀 전달하지 않는 구현이 가능하다.",
 "note": "새 원문을 열어 원 검색 당시의 직접 원문 열람 실패를 소급 교정하지 않았다."
},
"B-832023c6d065": {
 "p": [("unknown", "현재 cell 객체를 callback에 주는 것은 확인되나 kernel 실행 요청에 metadata를 결합하는 wire 계약은 아니다."), ("unknown", "클라이언트의 hook과 수신 kernel을 같은 실행 주체로 간주할 수 없다."), ("supported", "local hook은 별도 callback 인자로 cell을 받으므로 code magic을 바꾸지 않고 부가자료를 읽는 부품으로 사용할 수 있다.")],
 "novelty": "known_host_new_part_or_use",
 "fact": "셀 실행 전후 hook에 NotebookNode와 cell_index를 제공한다.",
 "counter": "클라이언트 hook에서 metadata를 읽었어도 kernel로 code만 보내는 경로이면 수신자는 그 값을 볼 수 없다.",
 "note": "nbclient라는 부품 이름의 신규성과 Jupyter host의 기존 인지를 구별한다."
},
"B-c926c69dfd9e": {
 "p": [("conflict", "호출 trace에 사건을 연결하는 모델을 실행 입력 metadata 전송으로 바꾸어 해석하지 않는다."), ("unknown", "수신 executor가 trace 필드를 호출 선택에 사용하는 코드는 해당 인용에 없다."), ("unknown", "관측 자료형의 필드 분리는 셀 실행 전달 경계의 증거가 아니다.")],
 "fact": "ToolCall 원 payload와 실행 중 사건을 trace 모델에서 연결한다.",
 "counter": "실행이 끝난 뒤 trace에 붙인 필드는 같은 호출의 kernel 선택을 바꾸지 못한다."
},
"B-e3eb5dc23dcb": {
 "p": [("unknown", "cell.source와 cell.metadata의 저장 분리는 확인되지만 execute_request와의 연결은 없다."), ("unknown", "파일 metadata를 kernel이 실행 입력으로 받는 동작은 형식 규약에 포함되지 않는다."), ("unknown", "저장 형태를 코드 변경 없는 전송 절차로 간주할 수 없다.")],
 "novelty": "known_target_same_use",
 "fact": "노트북 저장 형식에서 source와 metadata가 별도 필드다.",
 "counter": "notebook에는 metadata가 있어도 client가 source만 execute에 넣으면 수신 kernel은 metadata를 잃는다."
},
"B-ede1018ca153": {
 "p": [("unknown", "notebook/cell 식별과 backend 연결은 있으나 셀의 구조화 부가자료를 같은 실행 요청에 싣는 schema는 제시하지 않는다."), ("unknown", "기존 notebook→backend 매핑과 startup 설정을 셀별 metadata 소비로 볼 근거가 없다."), ("unknown", "실행 경로 분리는 설명하지만 코드와 metadata를 독립 전달하는 API 필드가 해당 절에 없다.")],
 "audit": ["RVJ-012"],
 "fact": "문서·실행 backend, notebook 매핑, HTTP 실행과 callback 확장을 구별한다.",
 "counter": "셀의 localization metadata를 바꿔도 backend가 기존 notebook 연결을 그대로 사용하며 source만 kernel로 보내는 구현이 가능하다.",
 "note": "새 감사에서 본 startup config 및 identity를 임의의 per-cell metadata 전송으로 확대하지 않았다."
},
"B-1e62bee0c2fa": {
 "p": [("conflict", "환경별 kernel을 등록하는 방식은 선택별 실행 명세를 늘리지 않는다는 조건과 어긋난다."), ("unknown", "등록 절차는 사용자에게 선언된 parameter schema에 따라 입력을 요청하고 검증하는 실행기 계약이 아니다."), ("unknown", "환경 등록과 선택은 사용자값을 argv/env template에 대입하는 동일 실행 경계를 입증하지 않는다.")],
 "fact": "가상환경 생성 후 ipykernel 등록으로 Launcher에서 선택한다.",
 "counter": "환경을 하나 더 등록할 때 kernel 항목도 하나 늘어나므로 조합별 항목 증가를 그대로 재현한다."
},
"B-28640fb5042b": {
 "p": [("supported", "한 tool 정의에 schema와 동적 인자를 두어 여러 실행값을 같은 명령 template으로 표현한다."), ("unknown", "자동 schema 검증은 확인되지만 사용자에게 값을 요청하는 경계와 허용값 목록의 실제 검증은 주어진 절에서 확인되지 않는다."), ("supported", "실행 인자를 command args/env에 치환하고 executeWithArguments로 실행하는 계약이 있다.")],
 "pick": [[0,1,2,4],[1,4],[0,2,3,4,5]], "audit": ["RVJ-008","RVJ-009"],
 "fact": "typed/default/required schema와 명령·환경 변수 치환을 제공한다.",
 "counter": "LLM이 인자를 모두 채워 API를 호출하고 사용자에게는 묻지 않는 client도 문서를 만족한다. 이 경우 입력 요청 조건은 충족되지 않는다.",
 "note": "JSON Schema라는 명칭만으로 enum 전체 지원이나 form 제공을 추론하지 않았다. 사용자 입력기를 새로 붙인다는 제안을 이미 제공되는 전체 실행기로 확대하지 않는다."
},
"B-836354c77778": {
 "p": [("conflict", "공유 template은 있지만 선택 뒤 사용자별 kernel.json과 Launcher 항목을 생성하므로 명세·항목 증식 회피 조건을 충족하지 않는다."), ("supported", "동적 dialog와 type/oneof/default/limits 규칙으로 사용자 선택과 검증을 수행한다."), ("supported", "선택값으로 kernel template을 치환하고 provisioner의 script/environment template을 사용해 작업을 시작한다.")],
 "pick": [[0,1],[0,2],[1,3]], "audit": ["RVJ-007"],
 "fact": "입력 form과 실행 template이 연결되며 새 kernel.json이 생성된다.",
 "counter": "두 parameter 조합을 각각 만들어 두면 두 kernel 명세와 Launcher 항목이 남는다. template 공유만으로 이 증가가 제거되지 않는다.",
 "note": "생성 명세를 단순 임시 실행 인자로 재해석하지 않았다. P2/P3의 장점은 전체 질문 P1 위반과 함께 보존한다."
},
"B-8975538191e9": {
 "p": [("unknown", "console:create의 선택 인자는 조합별 실행 명세를 없애는 parameter template이라는 근거가 아니다."), ("unknown", "명령 인자 목록에는 선언 기반 사용자 입력 요청·허용값 검증 흐름이 없다."), ("unknown", "kernelPreference와 cwd만으로 임의 실행 argv/env에 사용자값을 치환하는 계약을 확인하지 못했다.")],
 "novelty": "known_host_new_part_or_use",
 "fact": "console 생성에 kernel 식별·언어·시작 선호값 등을 넘긴다.",
 "counter": "이미 등록된 C++11/14/17 kernel 중 name으로 하나를 고르는 구현은 이 API를 만족해도 원래의 세 명세를 그대로 요구한다."
},
"B-8add6c6d3c45": {
 "p": [("unknown", "값 검증 schema는 실행 template의 조합별 복제 방지를 그 자체로 규정하지 않는다."), ("supported", "제약 선언과 model-driven form 생성·검증을 결합하는 설계 관계는 제시한다."), ("unknown", "schema 검증과 실제 process의 argv/env 치환은 서로 다른 기능이며 후자는 없다.")],
 "pick": [[1,2],[0,1,2,3],[0,1,2,3]],
 "novelty": "known_target_same_use",
 "fact": "형식·필수 값·범위 제약 및 선언에서 UI를 생성하는 용도를 설명한다.",
 "counter": "사용자 입력이 검증된 JSON을 저장하기만 하는 form은 모든 인용된 schema 기능을 사용하지만 새 process를 실행하지 않는다.",
 "note": "추상 설계 선례로서 P2를 인정하되 처음부터 명시된 부품이며 전체 실행기는 아니라는 점을 유지한다."
},
"B-9086761a0421": {
 "p": [("conflict", "기존 kernel에 문서·console을 붙이는 사용은 새로운 parameter형 실행 명세의 조합 표현이 아니다."), ("unknown", "선택값 schema와 사용자 입력·검증을 제공하는 근거가 없다."), ("conflict", "이미 존재하는 kernel에 코드를 보내는 흐름은 선택값으로 새 process/job을 시작한다는 조건과 다르다.")],
 "novelty": "known_target_new_use_or_constraint",
 "fact": "문서와 실행 중 kernel/console 및 subshell을 연결한다.",
 "counter": "같은 kernel에 console 두 개를 붙여도 서로 다른 실행 인자를 갖는 새 process 두 개가 생기지 않는다."
},
"B-a8cdb86fd5e6": {
 "p": [("unknown", "YAML로 미리 정의한 Launcher 항목을 추가한다는 설명만으로 조합을 한 template에 표현하는지를 알 수 없다."), ("unknown", "사용자 parameter 입력 요청과 type/default/허용값 검증은 인용된 README 절에 없다."), ("unknown", "고정 명령 실행은 있지만 사용자 선택값을 args/env에 대입하는 경계가 확인되지 않는다.")],
 "fact": "YAML 항목으로 명령·서버·문서 등을 시작한다.",
 "counter": "parameter 조합마다 YAML command 항목을 추가하는 설정도 README 설명을 만족하지만 명세 증가 문제를 해결하지 않는다."
},
"B-f0752e922f0e": {
 "p": [("supported", "commandTemplate과 step 실행값을 분리하여 동일 template의 여러 인자 조합을 표현한다."), ("unknown", "오케스트레이션 문서의 schema 검증은 사용자에게 parameter를 요청하고 허용값을 검증하는 입력 계층까지 입증하지 않는다."), ("supported", "step args/env가 default를 덮어쓰고 실제 명령을 실행하는 예제가 있다.")],
 "pick": [[0,1],[0,1,2],[0,1,2,3]],
 "fact": "재사용 commandTemplate, step의 args/env 및 실제 run 예제다.",
 "counter": "개발자가 손으로 step YAML을 모두 작성해야 하는 시스템도 이 문서를 만족하므로 사용자 입력 dialog의 존재는 따라오지 않는다."
}
}

packets = [json.loads(x) for x in PACKET.read_text().splitlines()]
assert len(packets) == 35 and set(D) == {x['blind_key'] for x in packets}
audit_receipts = [json.loads(f.read_text()) for f in (OUT/'receipts').glob('RVJ-*.json')]
audit_urls = {r['source_id']: r['url'] for r in audit_receipts}
audit_success = {r['source_id'] for r in audit_receipts if not r['error_observed']}
reviews = []
for x in packets:
    d = D[x['blind_key']]
    predicates = x['question']['mandatory_predicates']
    assert len(d['p']) == len(predicates)
    packages = []
    for package in x['citation_packages']:
        per = []
        citations = package['returned_citations']
        for i, (condition, decision) in enumerate(zip(predicates, d['p'])):
            status, reason = decision
            indices = d.get('pick', [list(range(len(citations)))] * len(predicates))[i]
            cited = [citations[j] for j in indices]
            # All selected original citation locators are taken verbatim from
            # the blinded package; no audit URL is inserted into these fields.
            assert all(z in package['opened_evidence'] for z in cited)
            supported = status == 'supported'
            per.append({
                'condition_id': condition['id'], 'status': status,
                'source_ids': list(dict.fromkeys(z['source_id'] for z in cited)),
                'urls': list(dict.fromkeys(z['url'] for z in cited)),
                'sections': [z['section'] for z in cited],
                'original_evidence_locations': cited,
                'support_in_original_opened': supported,
                'support_in_original_citations': supported,
                'reason': reason,
            })
        required = package['required_bundle']
        def contained(r, evidence):
            return any(all(r.get(k) == z.get(k) for k in ('source_id','url','section')) for z in evidence)
        complete = all(p['status'] == 'supported' for p in per)
        packages.append({
            'package_key': package['package_key'],
            'predicate_reviews': per,
            'opened_complete': complete,
            'cited_complete': complete,
            'status': 'supported' if complete else ('near_miss' if any(p['status']=='conflict' for p in per) else 'hold'),
            'required_evidence': required,
            'missing_conditions': [p['condition_id'] for p in per if p['status'] != 'supported'],
            'bundle_open_coverage_complete': all(contained(r, package['opened_evidence']) for r in required),
            'bundle_citation_coverage_complete': all(contained(r, citations) for r in required),
            'returned_unique_url_count': len({z['url'] for z in citations}),
            'fresh_audit_source_ids': [s for s in d.get('audit',[]) if audit_urls.get(s) in {z['url'] for z in citations}],
            'fresh_success_source_ids': [s for s in d.get('audit',[]) if s in audit_success and audit_urls.get(s) in {z['url'] for z in citations}],
            'original_return_eligibility': 'not_exposed_in_packet; root must join sealed mapping',
        })
    reviews.append({
        'blind_key': x['blind_key'], 'question_id': x['question_id'],
        'reviewer': 'arrow_agent_same_model', 'package_reviews': packages,
        'novelty_category': d.get('novelty', 'new_target'),
        'proposed_boundary': x['proposed_uses'],
        'provider_facts': d['fact'],
        'counterexample': d['counter'],
        'review_basis': {
            'initial_input_sha256': x['question']['input_sha256'],
            'initial_input_path': x['question']['input_path'],
            'packet_source_ids': [z['source_id'] for z in x['sources']],
            'fresh_audit_source_ids': d.get('audit', []),
            'mode': 'fresh_open_plus_packet' if d.get('audit') and d.get('audit') != ['RVJ-001'] else 'packet_observations_only',
            'followup_or_unmasked_data_read': False,
        },
        'notes': d.get('note', '') + ' 판정은 현재 제안 경계에 한정한다. 당시판 이용 가능성·당사자 인지는 판정하지 않았으며, 반례는 별도 표시한 연구자의 논리적 반례다.',
    })
(OUT/'reviews.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in reviews))
summary = {'blind_keys':len(reviews),'packages':sum(len(x['package_reviews']) for x in reviews),'predicate_reviews':sum(len(p['predicate_reviews']) for x in reviews for p in x['package_reviews']),'supported_packages':sum(p['cited_complete'] for x in reviews for p in x['package_reviews'])}
print(json.dumps(summary,ensure_ascii=False))
