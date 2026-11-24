# 비교 원자료 및 중간 판정

- C1 4.1.0 릴리스 태그에서 의존성 부재와 changelog #1977 확인(F09–10, F17). merge 버전은 4.0.0(A08–09). npm 게시 시각/실제 앱 소비 미확인.
- C2 beta3 = PR base, beta4 태그 generator에서 pin/register 부재(F03/F11), RubyGems 2023-01-31 게시(F12), 동일 작성자 version bump(F18). 이미 생성한 앱은 자동 갱신되지 않는다. C4는 downstream Blacklight beta7 lock(F08)과 같은 작성자/등록 구조, 하지만 복사 행위·공통 의사결정 증언 없음.
- C3 policy changelog 8.19.0 May5, 제거 전 코드 동시 존재(A07); 8.19.1 제거 후 코드(F14), May12 문서 날짜와 May13 UTC tag commit 구별. 사용자 업그레이드·접속은 미확인.
- D1 링크 제시 이후 원 제거 작성자가 문서 누락을 인식한 리뷰(A01). 문서 수정 PR은 리뷰 전부터 존재. D2 타입 이동은 upstream 0.5.2 root declaration(F16), 별도 타입 런타임 제거가 아님. 두 대조는 4개 runtime 분모 밖.

판정 초안: 기존 대안의 코드 수준 인지는 4/4(base 기준); 지원 환경 이유 직접 진술 4/4, 정책/버전 전환 corroboration DIM 1/4, HDS 매트릭스 본문 당시판 미확인. 첫 알림→선택 변경→동일인 행동 완전 사슬 0/4 관측(효과가 없다는 뜻 아님). PR base는 당시 API base, C2는 proposal 최초일보다 나중인 beta3. 노출: brief가 표본과 결과 방향을 이미 알려주고 diff 열람 후 body, 정책 고정본은 일부 body 후 읽음. 독립 블라인드 아님.
