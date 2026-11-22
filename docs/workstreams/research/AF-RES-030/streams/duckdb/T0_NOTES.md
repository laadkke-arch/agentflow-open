# DuckDB T0 판독과 봉인 메모

현재 단계: root/첫 실질 응답만 판독. 작성자 후속의 의도적 열람 전. A8, B screening26. 전역 B선정은 root가 interleave 순서로 결정한다.

## A 선정

2023Q1 최초순 #5816, #5818, #5821, #5826. #5817 ODBC build warning 제외. 2024Q3 #12784, #12789, #12796, #12804. #12798 debug build, #12800 sanitizer unit-test infrastructure 제외. 유지관리자 목적이 있는 CHECK/메모리경쟁/DST/array 요청은 포함하고 후속 독립성 민감도에서 나눈다. 레이블·종료·인기·답수를 선택에 쓰지 않았다.

API가 A 각15, B80개를 반환했다. 선정에 쓰인 실제 root 심사는 A11(선정8/제외3), B30(적격26/제외4). API 초과반환은 frame의 screened_for_selection=false. 편의상 출력한 root 중 A 일부 및 B#7047/#7049는 상한 뒤 직접 본문을 보았지만 첫 응답은 열지 않았고 후보선정에 재진입하지 않았다. frame이 이 차이를 보존한다.

## 실제 첫 질문과 보조 적격

- D02: 실제 장애였는지 코드 이론분석인지 물음. 예제 interleaving만으로 실측 사실을 채우지 않는다.
- D05: connection time zone. literal +05:30는 같은 값이 아니다.
- DB04: 실제 CSV null 토큰이 quoted인지 물음. current title은 quoted, root예제는 unquoted라 원판/실자료 동일성 보류. 첫 답이 예제를 인용하므로 그 예제만 Q부분 보강.
- DB07: 원하는 결과 순서. dplyr에 재정렬이 undesired라는 목적은 root에 이미 있음. 첫 답은 복합join/parallel 입력의 물리순서까지 확장해 묻는다. 질문에 인용된 root 문자열만 Q부분 보강.
- DB17: PostgreSQL dialect 오류 종류. 첨부2개 직접 보았다: getTimestamp/FAB9A2C5 및 trunc 함수 부재. current root의 dialect 취소선/교정 때문에 어느 시점에 어느 오류가 있었는지 최초판은 미확인.
- DB13/DB19의 patch PR 재시험은 action_request이고 Q4의 환경/목표/입력에 관한 질문 적격에서 제외했다. DB06 구현PR 확인형, DB12 진단 의문형은 수사/지원자 추론으로 분리했다.
- DB02 외부메일로 연락하라는 말, DB23 자기commit 농담은 실질 기술응답에서 제외했다. 연락을 취하지 않았다.

## 원판·인용·노출

공개 HTML root 객체에서 bodyVersion은 읽었으나 root lastEditedAt/userContentEdits 자체가 없었다. updated_at만으로 O(원판확정)라고 하지 않는다. /issues/5818/edits, /12784/edits, /7013/edits는404. A8 전체원판 U; DB04/DB07는 첫 답 인용한 부분에만 Q. 답의 lastEditedAt는 별도 JSON에서 확인하며 root시계와 섞지 않는다. 원판 복원 불능은 종료상태나 성공이 아니라 증거의 한계다.

사전노출은 숨기지 않았다. D01 HTML 메타데이터 정규식이 첫 답 이후 공급자댓글 세 문장 일부를 출력했다. D04 current root에는 ICU패치라는 결론이 있고 원작성/후대편집 시점이 불명이라 보수적으로 노출 표시. DB17 root dialect 교정은 후대정보 가능성. DB26 connector shape 검사가 작성자 자기해결 댓글을 출력했다. 이 네 행은 exposure=true이며 원본을 다른 사례로 교체하지 않는다. 질문분기 코딩 때 D02/D05/DB04/DB07 작성자 후속은 보지 않았다.

## 공개 증거와 임시 수집

source-ledger는 A스레드8개를 최소수에 산입, B screening26개는 산입하지 않는다. 실제 root/첫 응답을 읽었고 다운로드만 한 자료를 직접읽기로 세지 않았다. 원문은 permalink·body hash·UTC와 한국어 요약/짧은질문을 남긴다. evidence/unread_cache는 프로그램이 받은 원문/HTML/첨부의 임시 데이터로 gitignored이며 출처 최소수나 봉인 결과 파일이 아니다. 공개 first-*.json에는 전체 본문을 제거했다.

## 결과를 보기 전 대조짝

pairs-frozen.csv: D02↔D01, D05↔D07. 같은 원장/분기/bug유형/정보점수 차1이하에서 생성시각 최근접이다. 서로 기술적목적이 다르고 D01은 공급자/사전노출이어서 인과 비교에 사용할 수 없다. 매칭 후 그 차이를 지우거나 더 좋은 결말 대조로 교체하지 않는다.
