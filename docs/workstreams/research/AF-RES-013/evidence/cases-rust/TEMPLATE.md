# Rust 계열: 템플릿 이력·정답원 경계

## 실제 확인

| 변화 | 직접 연 고정판/이력 | 확인 내용 |
|---|---|---|
| 최초 template, 2014-03-10 | [14ca6f65](https://raw.githubusercontent.com/rust-lang/rfcs/14ca6f655066058b886eac1dcc4017af0d22c2f5/0000-template.md) | Summary/Motivation과 Alternatives를 별도 절로 둔다. Prior art 절은 없다. |
| 대안 절의 이름 변경, 2017-07-19 | [4a3f5c55](https://raw.githubusercontent.com/rust-lang/rfcs/4a3f5c5570b4ae5940aa0c4d0d62b4e79aabeeb1/0000-template.md) | Alternatives가 Rationale and Alternatives로 바뀐다. 이는 Prior art 절 도입과 다른 사건이다. |
| Prior art 작성 commit, 2018-02-12 | [f08f8818](https://raw.githubusercontent.com/rust-lang/rfcs/f08f881847850d5d587e3504088a11fad766e51b/0000-template.md) | 다른 언어·다른 커뮤니티 경험과 논문을 명시적으로 돌아보도록 요구한다. |
| Prior art 통합, 2018-02-27 | [a488ca02](https://raw.githubusercontent.com/rust-lang/rfcs/a488ca0263dc4e8ee495ef9b6ca0d9d5d7fbc790/0000-template.md) | PR2333 merge. 다른 언어의 전례만으로 기능 도입이 정당화되는 것은 아니며 Rust의 의도적 차이도 고려하라는 단서가 포함된다. |

`template-history.json`은 공식 [path history API](https://api.github.com/repos/rust-lang/rfcs/commits?path=0000-template.md&per_page=100)의38개 항목을 역순으로 대조한 기록이다. 36개 역사판의 heading을 fetch하여 prior-art 존재 여부를 검사했다. 2개 경로 404는 제외했다. 전체 본문을 읽은 최초판/추가판/통합판3개와 heading 검사만 한 판을 구별한다. 작성 날짜와 통합 날짜를 섞지 않는다.

**선정 편향:** 번호 오름차순 절차의 Rust8개는 모두2014년이다. 명시 Prior art 유도절의2018년 도입보다 이르다. 따라서 이 표본의 다른 분야 인용 빈도는 현대 Rust RFC 템플릿 전체의 빈도가 아니다. Alternatives의 내부 설계와 외부 선행 제품은 처음부터 서로 다른 회수 대상이다. R0123의8개는 전부 명명 대안이며 이름만 검색된 것으로 적중 처리하면 안 된다.

## 리뷰 원문2건

- [PR8 comments](https://api.github.com/repos/rust-lang/rfcs/issues/8/comments?per_page=100): 반환된8개 댓글의 본문을 읽었다. 형변환 크기 제약, private trait 또는 macro 대안이 추가되었지만 작성자가 별도 이슈라고 명시한다. 이 내용은 intrinsics를 일반 함수로 노출하는 본문 gold에 소급 추가하지 않았다. 범위 밖의 리뷰 제안이 많다는 반례다.
- [PR123 comments](https://api.github.com/repos/rust-lang/rfcs/issues/123/comments?per_page=100): 반환된25개 댓글을 읽었다. Sync 제안([comment46233066](https://github.com/rust-lang/rfcs/pull/123#issuecomment-46233066))과 이름을 바꿨다는 후속 보고([comment49805271](https://github.com/rust-lang/rfcs/pull/123#issuecomment-49805271))가 연결된다. 원문 대안8개와 별도로5개 review pool 항목을 보존했다. Clojure atom과 Atom의 유사성([comment46475940](https://github.com/rust-lang/rfcs/pull/123#issuecomment-46475940))은 **용어 비유(term_only)**다. 상태 관리 원리를 Rust trait로 이식한 사례로 세지 않는다.

## 뒤집힌 결정

R0114는 초기 closure 설계에서 by-reference 기본값과 receiver inference를 각각 거절/유보했다. [후속 R0231의 수락 전 고정판](https://raw.githubusercontent.com/rust-lang/rfcs/2e7023d11a34f7718f248000edd6f1b8e7e189c1/active/0000-upvar-capture-inference.md)은 capture/receiver 추론을 도입하고 ref 명시를 제거한다. [PR231 metadata](https://api.github.com/repos/rust-lang/rfcs/pulls/231)의 merge 날짜는2014-09-18이다. 변경 범위는 기본 capture와 receiver 표시 방법이며 callable-trait 통합 전체의 철회가 아니다.

현재 보존본문의 escaping 형태는 move, 복구한 PR head에서는 proc여서 문법의 세부 수락시점까지 일치한다고 주장하지 않는다. 이 불일치는 최신판을 결정 전 입력에 쓰면 미래 정보가 섞일 수 있는 실제 예다. 현재 R0008에 있는 retired/never implemented 공지는 역사적 종료 날짜를 고정하지 못했으므로 대체5개 조건에 산입하지 않았다.

## 한계

PR8·42·85의 head/merge 원문 SHA256이 동일하다. 다른5개 PR의 API merge SHA는 commit.patch에서도404여서 정확한 병합 내용은 아직 미확인이다. 이5개 사례는 수락 전 head의 고정판, 공식 병합일, 현재 보존된 대안 절과의 항목 일치를 분리하여 기록했다. 수락이 구현·안정화나 실제 채택 성공을 뜻하지 않는다. 리뷰의 모든 후보가 처음 댓글에서 생겼다는 것은 입증하지 못하므로, 본문에 원래 있던 항목의 added_in_review는 unknown이다.
