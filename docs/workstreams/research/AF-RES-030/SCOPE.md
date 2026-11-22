# AF-RES-030 사전 범위·표집·봉인 규칙

## 고정 입력과 실행

- 시작 통합 SHA: 172c6bc37bdf91b91c86b9b3be29cb5b44fa4971. 계획 입력 478c539b0fccbb7949ed7d7fbb6bf8810a2ca998와 구분한다.
- AF-RES-026 의존: c6eff012a74451e9882d8d43b6a6e510b4d15225. HANDOFF, ANALYSIS_RULES, strategy-summary, analysis, actual-roundtrips를 읽었다. 과거 24건 재판독·가상 I/C/Q 생성은 하지 않는다.
- 실행 환경: ChatGPT의 Linux cloud workspace, 세션 지시상 GPT-6 Astra Pro. 실제 UI 모델 선택/추론 강도는 미관측. 세 프로젝트의 독립 조사 에이전트는 같은 세션 모델을 상속한다. 로컬 셸 실행과 GitHub 읽기 영수증을 구별한다.
- 소유 경로: docs/workstreams/research/AF-RES-030/만. 공통 진행표는 변경하지 않는다. manifest.json은 실제 workbench.session start --fetch의 출력이다.

## A: 사전 고정 두 분기

2023Q1(2023-01-01T00:00:00Z–2023-04-01T00:00:00Z 미만) 및 2024Q3(2024-07-01T00:00:00Z–2024-10-01T00:00:00Z 미만).
세 원장 matplotlib/matplotlib, pydata/xarray, duckdb/duckdb의 GitHub Issues에서 각각 분기별 최초 적격 요청 4개, 총24개. issue created_at 오름차순, 동률 issue number 오름차순. PR 제외. 상태·댓글 수·인기·수락 표시는 선별에 사용하지 않는다.
적격: 특정 작성자의 사용/설계 목적(그림·출력/자료형·차원/질의·API 등), 그 목적에서 기대와 현실 또는 선택할 일이 드러남. bug/feature/question 레이블은 선정 기준이 아니며 실제 본문으로 판단한다. 설치/빌드만·프로젝트 관리/공지·보안 신고·독립 목적 없는 중복·식별 불능/삭제는 이유와 함께 제외한다. 작성자가 유지관리자여도 제외하지 않고 감도분석에서 분리한다.
각 분기의 earliest candidates를 순서대로 모두 심사하며 네 번째 적격에서 중지한다. 검색 API의 정렬·페이지·전체수·범위를 기록한다. 검색 결과가 빈 경우 같은 범위를 공식 이슈 목록으로 재확인한다. 원장 접근 실패시 (1) 같은 프로젝트 GitHub Discussions (2) matplotlib Discourse / xarray 공식 연결 지원 게시판 / DuckDB GitHub Discussions 순, 기간은 2023Q2→2024Q4→2025Q1. 대체 전 실패 URL/UTC/원인을 남기며 같은 원장 분모로 섞지 않는다.

## B: 질문부터 찾는 보조 표본

A와 겹치지 않는 다른 월 2023-04부터 시작한다. 부족하면 2023-05,06,07 순으로 진행한다. 세 원장의 적격 root를 각각 최초시각 순으로 읽되 전역 순서는 M1,X1,D1,M2,X2,D2,…,M27,X27(총80)으로 고정한다. 각 프로젝트는 최대 M27/X27/D26개의 적격 root와 그 첫 실질 응답만 심사한다. 부적격 root는 이80 적격 상한에서 제외하되 원장에 남긴다.
전역 순서상 첫 실질 응답이 환경·목표·입력을 직접 묻는 첫8건이 B다. 작성자 답·성공·수락/닫힘을 보지 않는다. 초과 스크리닝은 B 후보 시도로 보존하되 분모8에 넣지 않는다. 80 이내 질문적격이8개 미만이면 관측 수만 보고한다. A를 B로 보충하지 않는다.

## T0 / 첫 응답 봉인

1. API 원 요청과 댓글을 프로그램이 받을 수는 있으나 모델에는 root와 첫 타인 실질 응답까지만 표시한다. 후속 원문은 별도 미열람 영역이며 봉인 전 읽지 않는다. API가 반환한 current body는 원판으로 단정하지 않는다.
2. root author 자기보충·봇·단순 인사/관리만인 댓글은 별도 메타데이터로 보존한다. 첫 실질 응답: 질문, 실제 설명/진단/사용제안 또는 기술적 판정. 첫 답이 요청자 본인이면 별도 self-followup이다.
3. 본문/댓글의 편집 시각·본문 수정 이력·첫 답 인용·첨부 버전/URL을 직접 확인한다. 원판 복원 불가=U(미확인); 시점 이전 문자열만 첫 답 인용으로 확인=Q(부분 보강); 본문 편집 없음/공개 원판 이력 확보=O(확인). API updated_at은 본문 편집만의 시계가 아니므로 O의 충분조건이 아니다. 호환 등급을 원판 등급과 별도로 둔다.
4. 최초 목적·시도·판/설정/데이터·출력·필수/선호/금지를 위치에 매핑한다. 현재 원문에 미리 해결 내용이 있거나 검색 결과가 후속 내용을 노출하면 case-level exposure를 true로 기록한다. 후속에서 배운 값을 initial 칸에 넣지 않는다.
5. first_strategy: information_request / conditional_action / directive / mixed / no_substantive_response. 질문 변수마다 최초 값 already_present / absent / unclear, 가능한 두 값과 달라질 후보·용도·행동을 실제 작성자 답 전에 적는다. 질문 없는 사례에는 가상 질문을 만들지 않는다.
6. stage2 커밋은 A initial, questions, B first-response screening, 결과 미열람 짝선정 파일을 봉인한다. 봉인 후 정정은 원본을 덮지 않고 별도 correction 파일에 남긴다.

## 후속 관측과 판정

질문 후30일(해당 질문 시각 기준)의 작성자 답과 권고, root 후90일의 동일 사건 후속을 별도 기록한다. root 후30일 전체창도 함께 제공하여 기준 차이를 보존한다. 삭제·페이지 누락은 관측불능이며 온전히 읽은 창에서 답 없음과 구별한다. 모든 2023/2024 표본의 달력창은 조사시점 종료되어 있다.
같은 변수·주체·판·대상의 직접답/부분답/재진술/제3자/후발 새요구/중단·미확인 분리. 예제 데이터와 실제 데이터, 가정과 선언을 합치지 않는다. 복합 질문은 변수 행을 나누되 (question_comment_id,answer_comment_id) 왕복키를 하나로 센다.
권고 변화: candidate_switch / same_candidate_option_or_explanation / next_action_change / no_change / no_prior_proposal / unconfirmed. 같은 지원자의 명시적 연결과 연구자 사후추론을 구별한다. 설명만 좋아짐과 실제 실행 성공은 별개다. 실행 성공/실패는 요청자의 구체적인 새 실행·출력 보고만 센다. 감사·close/accepted·공급자 PR은 실행 성공이 아니다.
클릭·읽기 시간·대신할 수 있었던 노동은 미확인. 대기는 질문→작성자 답의 경과시간과 답 없는 관측상한을 기록하며 중첩 합산하지 않는다.

## A 내부 대조와 분모

결과 열람 전 질문 포함 사례를 같은 원장·분기·요청 종류(usage/bug/feature/design)·최초 정보충족 점수로 매칭한다. 점수=목적/시도/판/입력 예제/출력 다섯 필드의 명시수(0–5). 같은 요청종류, 점수차1 이하인 실제 directive/conditional_action 우선, created_at 거리 최소, 동률 issue number. 비복원 root로 만든 점수는 current-body proxy임을 표시한다. 적격 대조가 없으면 해당 없음. 비교전 목표·복잡도·원판 등급 차이를 남기며 효과 추정은 하지 않는다.
분모는 A24, 실제 질문 있음, 같은 변수 직접답, 동일목적 새 실행, B8/실제확보를 나눈다. variable 수·roundtrip 수·사례 수·고유 발신자 수를 따로 센다. 반복발신자 제외(각 공개 handle 최초1건), 유지관리자 겸 질문자 제외, 미래노출 제외, 미확인 극단(모두0/모두1)을 보고한다. 0분모는 해당 없음.

## 외부 자료와 종료

A24 threads + 당시 공식 매뉴얼/테스트/결정8 + 도서관 참고상담2 및 공공 통계 인지면접2 = 최소36 고유 원문. B는 별도. 같은 스레드 여러 댓글·같은 문서 HTML/PDF/미러는 하나. 검색 요약·실패는 최소수 제외. 출처마다 source_id/type/publisher/url/version/checked_utc/sections/observed/limitations/linked_Q_cases/duplicate_group/count_minimum을 보존한다. 짧은 인용과 정확한 permalink를 우선하고 대화 원문을 자료 수 늘리기에 쓰지 않는다.
결과·자체검사·수용조건을 커밋하고 원격 SHA에서 재독한 뒤 별도 HANDOFF 커밋. 미충족을 false로 남기고 REVIEW_READY_WITH_GAPS. 양성0 자체는 실패가 아니다.
