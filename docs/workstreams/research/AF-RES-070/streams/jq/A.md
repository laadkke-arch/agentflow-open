# jq A 봉인

댓글을 열지 않고 생성 당시 IssuesEvent로 원본문을 복구했다. 원 저장소명 stedolan/jq와 현재 jqlang/jq는 repository ID 5101141로 연결했고, LolHens→lhns 같은 계정명 변경은 사용자 ID로 대조했다.

|행|최초표현 최소발췌|선택필드|질문/생략|A 판단|가림|
|---|---|---|---|---|---|
|jq-2259|jq keeps strings as it is.|읽을 수 있는 원본 파일이 있는가|생략|파일 대조가 이미 제공되어 입력 출처를 재질문할 필요 없음. 차이는 버퍼/디코딩 경로 검토 대상으로 제한하며 두 경로의 완전한 바이트 동등성은 미확인.|main_blind|
|jq-2267|try in a map|숫자 변환 실패 항목의 처리|생략|A의 목적은 C1이며 C2는 기대 배열과 다르다. 이미 명시한 오류 정책을 묻지 말고 해당 개발판 문제로 한정한다.|main_reconstructed_exposed|
|jq-2349|2 elements|병합키 anidb_id가 없는 원소의 보존|생략|C2 방향을 조건부 제안. missing key가 null로 평가되고 같은 값은 함께 묶이는 판별 근거는 있으나 원 두 파일의 당시 전체내용·실행판·전체 파이프 출력은 미확인.|main_blind_conditional_version|

원문 전체는 비공개 분석용 private 사본에만 보존한다. 공개 고정 아카이브 주소·이벤트ID·행·해시는 enrollment.json과 pre.json으로 연결한다. 독립 판별 절은 pre.json의 후보별 목록 그대로 B에도 사용한다. 세 행 모두 A에 목표/값이 이미 있어 질문을 만들지 않았다. 이는 실제 질문 효과 0이 아니라 질문 미제안이다.
