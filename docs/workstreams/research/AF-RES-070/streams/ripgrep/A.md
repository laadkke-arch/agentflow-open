# ripgrep A 봉인 패킷

준비 UTC: 2026-11-23T08:37:59.309108+00:00. 댓글 아직 미열람. 원 모집슬롯3개와 별도 진단3개.

원래 본문8/8을 GH Archive IssuesEvent/opened에서 복구했다. 1808·1778·1792는 현재본문이 바뀌었다. 특히1778의 works→fails 수정 때문에 현재본문을 최초판으로 쓰면 관측 방향이 뒤집힌다. 이미 현재본문을 읽은 세 행은 재구성층이며 순수 사전판독 수에 넣지 않는다.

9–16은 원본문복구 전 최초판미확인 상태에서 순서대로 연 확장조회다. 첫3 원본문이 복구되어 선정 대체에 사용하지 않는다.

## 봉인 행

|행|층|한 필드|질문/생략|A 권고|
|---|---|---|---|---|
|RG-1808|reconstructed_exposed|preserve_negative_glob_priority|skip|RG1808-C2; 알려진 금지조건에 바로 답한다. --type가 --glob와 동일 우선순위라는 원글의 일반화는 코드 순서와 맞지 않는다.|
|RG-1778|reconstructed_exposed|working_directory|ask|조건부 C1/C2; 누락 cwd 하나가 패턴 해석을 가를 수 있으나 정확한 실패 원인을 확정하지 않는다.|
|RG-1814|prospective_packet|preserve_alphabetical_default|skip|RG1814-C2 방향으로 바로 답하기; 어떤 옵션이 어느 단계인지 별도 정확성 검토는 필요|
|RG-1792|diagnostic_reconstructed_exposed|no_config_must_disable|skip|C2 조건부; 질문 생략|
|RG-1812|diagnostic_prospective|workaround_allowed|skip|C2 조건부; 이미 허용한 우회 여부를 다시 묻지 않음|
|RG-1840|diagnostic_prospective|exclusion_reason|ask|원인이 확인되기 전 C1/C2 조건부|

## 노출·판별 범위

모든 A/B 후보는 pre.json과 pins.json에 고정한다. 데이터 수신 과정의 GitHub HTML에는 댓글이 포함되어 있었지만 JSON 최초 객체 키만 출력했고 댓글 내용은 보지 않았다. REST 댓글 endpoint는 아직 호출하지 않았다.

1808/1778은 사후 편집본문 선행노출과 부가문서절 판독으로 엄격 사전 노출통제 분석에서 제외한다. 이들의 원 최초판과 A 재구성은 별도로 유용하지만 사전예측 정확도라고 부르지 않는다. 1814의 도구판은 OP가 밝히지 않아 당시 공개12.1.1에 대한 조건부 판정이다.

본 스트림의 공식 원저작은 GUIDE.md, crates/core/app.rs, crates/ignore/src/walk.rs, crates/ignore/src/gitignore.rs의4계보이다. 같은 파일의 절·버전·API별 응답을 추가원작으로 세지 않는다. GUIDE/소스의 다운로드 전체와 실제판독절은 구분하며 실제판독절은 sources-pre.jsonl에 보존한다.

원작성자 발언은 의도 근거이고 도구 동작 판별은 고정판 코드·문서 근거이다. 새 필드 값이 없으면 B=자료없음, 질문이 쓸모없었다는 의미가 아니다.
