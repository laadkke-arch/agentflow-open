# 독립 문맥 기준판정 지시

이 과제는 네 보기의 결정이 원격 봉인된 뒤 수행한다. 당신은 그 결정·N/H 카드·수집자의 판단을 받지 않는다. 제공된 원 인용 B만으로 목적을 고정하고 실제 공개 원문을 확인한다. 동일 모델계열의 별도 문맥 판독이므로 사람·다른 모델의 독립 검증이라고 부르지 않는다. 원문과 발행자가 N/H 작성자와 같을 수 있으며 출처의 독립성과 판독자의 문맥 분리를 구별한다.

배정된 input.json의 모든 원 href를 직접 GET하여 실제 status/redirect/final body와 필요한 정확한 절을 확인한다. 링크가 패키지/도구 랜딩이면 필요한 기능/클래스/규칙을 설명하는 공식 본문으로 따라가고 각 요청을 기록한다. 원 인용의 날짜·판·문장이 무엇을 요구하는지 현재 자료와 대조한다. 특정 판의 요구를 단지 오래된 문서에서 추측하지 않는다. 한국어 목적은 수집자의 사전 해석이므로 원문에 없는 한정은 식별해 따로 처리한다.

KEEP는 원 href의 실제 도착을 통해 원 목적/대상/필요 판을 읽을 수 있는 경우다. REPLACE는 같은 목적을 위해 다른 목적지가 필요한 경우다. 그때 대체 URI를 실제로 열고 정확한 절·판을 검증한다. HOLD는 필요한 사실이나 목적이 결정되지 않을 때다. HTTP200·404 하나만으로 내용/대체 URI의 적합성을 자동 판정하지 않는다. 최신판이라는 이유만으로 원판 인용을 없애지 않는다.

대체 URI가 필요하지 않은 경우에도 가능한 반례를 찾는다: 현재 페이지에 새 판 안내가 있어도 원판을 더 잘 보존하는 경우, 현재 주소는 살아 있으나 목적 내용이 없는 경우, 새 주소도 기대 anchor가 없는 경우. 그런 사건을 실제 찾지 못하면 없었다고 만들지 말고 시도와 범위를 남긴다. 양성 사례 수는 완료 조건이 아니다. 소프트웨어 설치·실행·로그인·계정 변경·유료 자원은 사용하지 않는다.

출력은 자기 폴더의 adjudication.jsonl(사례당1행), sources.jsonl, attempts.jsonl, 짧은 notes.md다. 기존 scripts/fetchlib.py를 읽어 사용하면 request/bytes/elapsed/hash를 측정할 수 있다. 새 source마다 source_id, URL/fixed URL, 발행자, 날짜·판·확인UTC, 직접 읽은 절/행/페이지, 내용, 한계, source/member hash, exact excerpt를 기록한다. 이미 존재할 수 있는 원문을 새 고유 수로 당연히 더하지 않으며 root가 중복군을 합친다. 원문을 직접 읽지 않은 검색 요약은 count=false다.

판정 행 필드: ref_id, criterion_action(KEEP/REPLACE/HOLD), confirmed(boolean), rationale, original_request_attempt_id, original_http_status, final_url, exact_section_url, section_locator, required_edition, primary_source_ids, replacement_url(null가능), replacement_request_attempt_id, replacement_exact_section, replacement_matches_purpose(boolean/null), replacement_fragment_verified(boolean/null), observed_false_anchor_or_wrong_target, dated_publisher_evidence, remaining_unknowns, falsifying_condition, context_independence, source_independence.

context_independence는 실제 접근 범위를 적는다. source_independence는 완전히 다른 발행자 원문인지, 같은 발행자 다른 원문인지, 같은 문서의 추가 절인지 구분한다. 다수결이나 수집자의 권고를 독립 정답으로 사용하지 않는다. 실제 독자 클릭·실행 성공·역사 당시 HTTP 상태를 관측한 것처럼 쓰지 않는다. 커밋과 공통 파일 수정은 root가 한다.
