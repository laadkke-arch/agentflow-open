# Pandoc 후속 판독과 반례

A 봉인 `a6e2f47e6cfa52e249f4d648016cf9d324eccae9` 이후 2026-11-23 08:41:19 UTC에 댓글을 공개했다. raw GitHub REST의 UTC와 numeric author ID로 시간·작성자를 대조했다. 세 스레드는 각각 10·7·1개 댓글이며 한 페이지 100개 한도보다 작고 초기 REST의 comment count와 일치한다. 현재 조회 종료까지의 공개 댓글이다.

## 필드를 잘못 고르면 실제 새 조건도 B가 되지 않는다

[#7003의 첫 목적](https://github.com/jgm/pandoc/issues/7003)은 두 코드 리스팅 보존이었다. A에서 이 목적을 되묻지 않기로 한 판단과, 변환 앞 단계의 제약을 다 알았다는 주장은 다르다. [753672131](https://github.com/jgm/pandoc/issues/7003#issuecomment-753672131)에서 OP는 filecontents 제거가 용도상 불가능하다고 밝혔고, [753859056](https://github.com/jgm/pandoc/issues/7003#issuecomment-753859056)에서는 약 천 개 파일의 앞 단계에 정상 정의가 필요하다고 설명했다. 이 정보는 제거/no-op 우회안의 적합성·비용을 바꿀 수 있다. 그러나 봉인한 필드는 `preservation_target`이므로 이 금지조건과 인접 단계 정보를 사후 B로 치환하지 않았다. 또한 이 행은 댓글 구절 선노출로 사전판독층이 아니다.

## 질문 응답이 있어도 선택 필드의 답은 아닐 수 있다

[#7013](https://github.com/jgm/pandoc/issues/7013#issuecomment-757285247)의 실제 유지보수자 질문은 최소 입력과 명령이었다. [OP 답변757339567](https://github.com/jgm/pandoc/issues/7013#issuecomment-757339567)은 그것이 최초글에 이미 있고 URL 입력임을 지적한다. 이는 실제 중복 질문의 사례지만 연구자의 봉인 질문(fetch 성공/오류)과 다른 질문이므로 실제 A/B 분모를 섞지 않는다. 이후 OP의 [버전 회귀시험757355329](https://github.com/jgm/pandoc/issues/7013#issuecomment-757355329), [bisect757374825](https://github.com/jgm/pandoc/issues/7013#issuecomment-757374825)는 다른 필드다. 유지보수자 [루프 설명757427502](https://github.com/jgm/pandoc/issues/7013#issuecomment-757427502)은 타인의 코드 판단이지 같은 작성자의 fetch 응답값이 아니다. 마지막 감사는 독립 출력이 아니다.

## 최초글이 이미 두 조건을 제공하는 경우

[#7006](https://github.com/jgm/pandoc/issues/7006)은 이미지 뒤 블록 유무·출력을 A에 모두 담았다. [유지보수자 설명754856781](https://github.com/jgm/pandoc/issues/7006#issuecomment-754856781)은 backlink가 단독 이미지 조건을 깨는 메커니즘을 확인한다. 같은 작성자 후속은 없다. A의 observed pair를 새 B나 연구자 반사실로 재계상하지 않는다. 이 행 역시 편집문구 선노출층이며 사용판은 조건부다.

## 현재 분모와 실제 짝

선정된 세 자리의 선택 필드 B는 모두 자료 없음이다. 따라서 엄격 개선/동일/악화의 비교 가능한 분모는 0이며, 세 행은 관측 불가다. 질문 제안은 #7013 한 건이다. 고정 코드의 성공/오류 분기가 다르다는 독립 근거는 질문 필드의 판별성을 설명하지만, 전체 EPUB 실사용 성공이나 질문 비용을 입증하지 않는다. 질문 생략 두 행을 실제 질문제안 오탐 분모에 넣지 않는다.

현재 실제 B 사례가 없으므로 같은 동작의 B-무응답/정보무효 짝은 구성할 수 없다. 처음8의 미선정 #7039·#7057, 다음 규칙큐9–16은 진단 A를 별도 봉인한 뒤에만 댓글을 읽을 수 있다. 이미 열린 댓글로 유리한 진단 사례를 골라 주 표본을 대체하지 않는다.
