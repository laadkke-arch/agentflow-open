# ③ 핵심 표 사전 초안 — 원값과 수신 구분
- 표1의 여섯 자리: M1 P, M2 V 같은 필터, M3 P 토글/V 보존, T1 V(잠정), T2 ?(경계), T3 결측. 본문 동결 이전에 댓글이 노출된 TanStack에 대해서는 독립 사전예측으로 세지 않는다.
- 표2 ID 원값: C10/D02 test [0]→[0,3,4], filter change [0,1,2,3]→[1]. D04 [0]→[0,2,3]. C11 server page expected size2 of4. 실제 실행이나 reporter ID라고 부르지 않는다. T02의 4 true keys와 T01의 getRowId uuid는 같은 author이나 body literal ID는 없음. T05/T06 author index issue→getRowId 해결 보고. T13 fetchCategories read options에 selection 없음. T10 allIds server→client 보고일 뿐.
- 표3 초기 답: 현재 면만이면 page handler 직접, 누적이면 stable ID state+object model boundary, 미로드 filter 전체라면 scope/exclusions or ID enumeration contract candidate. F vs U 불명확시 질문 한 문장. M04/M05로 filter 변경 보존 정책은 따로 결정해야 한다.
- 증거: 본문/댓글 진술, 정적 코드, PR 테스트 기대, 문서 계약, 설계 추론을 별도. 수신/처리된 IDs는 0건 검증, 반드시 미확인 표시.
