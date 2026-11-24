# SELF_CHECK — AF-RES-208

상태 PARTIAL. 자체 검토자: 이 작업을 작성한 동일 모델 (독립 검토 0). 원장 및 body_freeze와 현재 분석을 대조. 사용자 연구 브리프, 197 HANDOFF/answers에 사전 노출됨. 네 issue 본문 동결 commit 32d47b4f338d9027ecb0f718fa12e7125b4e6d47 뒤 댓글 조회. GitHub 공개 이슈 제목·현재 본문은 최초 작성 revision을 확정하지 않으며 검색어/대안은 이미 지시로 노출. 독립 blind 평가 아님.

| Q | 직접 근거 ID | 판정 및 반례 | 미확인/다음 |
|---|---|---|---|
| Q1 | N1–N4, F5,F6,F12,F13 | 4 원본문 vs 댓글 구분. N1 RID 추론; N2 상대시간; N3 scope 미정; N4 원래 날짜 | X1, 최초 revision 및 정확 날짜 |
| Q2 | K1,K2,K3,K4,K5,E1 | 원시각과 표시 시각, C1 양방향 경계 | 원작성자 raw UID/RID 0/4 |
| Q3 | K1,E2,F11,E3,F9,E4 | uniform shift, C3b 선택적 요일 반례; C2 취소/ C4 DST | 런타임 미실행, 정확 deployed range support |
| Q4 | K3–K7,H1,K2 | split design, ETag/old/new keys, tombstone; K3 L219 주의 확인 | 최신 official split/reset 원예 미확인, 2 API 실행 0 |
| Q5 | N1,N2,F1–F7,F9–F11,E4 | readback·reported client differences vs static tests | 직접 fix chain, X1/X2/X3; 수신 raw 0 |
| Q6 | T1–T5 | 1/2 service date add/remove; T3/T4 기관별 차이, identity 불전이 | 실제 feed 및 운행 실측 0 |
| Q7 | N1–N4,K1–K7,methods/routes | 3 명시적 scope/1 모호, 질문의 답을 바꾸는 조건; C0 equivalence | 실제 질문/답/검색 ranking 실험 0 |

| 유형 | 목표 | 산입 | 비고 |
|---|---:|---:|---|
| 사건 본문 | 4 | 4 | 고정 4/4, 교체 0 |
| 변경·시험·후속 | 6 | 10 | F1–7,F9–11; F8 같은 파일 다른 버전 제외 |
| 표준·제공자 | 5 | 7 | K1–7; RFC 절별 중복 없음 |
| 공개 ICS·제작자 예 | 4 | 4 | E1–4, fixture/test 기대값만. X1 raw 사건 첨부 미확인 |
| 교통 표준·기관 | 3 | 5 | T1–5 |
| 합계 | 22 | 30 | sources.jsonl 43행, noncounted 13; 같은 계보 독립 실측 취급 금지 |

고유 URL work_id 30/30; 유형별 하한 달성. 원자료 종류와 사건 분모 별도. planned primary slots N1–N4 4, controls C1–C4 4 (C0/C3b 보조), no original ICS 0, end-to-end recipient source 0/4. 결과 셀 중 규칙을 저자 결과로 표기한 셀 0 (수동 표 검토); "작성자 보고" 라벨은 당사자 관측 서술. 신규 코드·벤치마크·CI 실행 0. Q5 incident-specific patch-chain 미달, Q4 공식 두 요청 원예/reset 미달. 정정 내역 counterexamples.md. 
체크: RESULT 제목 다음 표1/2/3, Q1~7 및 마지막 3건 표; SCOPE/frame/sources/events/methods/routes 존재, counterexamples 별도 commit. 모든 쓰기 owned_path. 실제 GitHub reread/compare는 최종 RESULT+SELF_CHECK SHA에 대해 HANDOFF 전 별도 수행 예정(현재 파일 작성 시 미수행); HANDOFF에 실제 수행 내역을 기록한다. 
