# SELF_CHECK — 작성자 자체 검토

상태 PARTIAL. 독립 검토 미실시. 제품/DB/CLI/외부 데이터 재현 미실시. 이 파일은 결과판에서 재열람할 대조표이며 최종 확인 사실은 별도 마지막 HANDOFF에 기록한다.

| 질문 | 근거 ID/파일 | 반증·결손 | 확인 |
|---|---|---|---|
| Q1 | O01–04, C01/C04, SCOPE | 11411 보존 해석 반대; 초기 revision 미확인 | 현재 body 확인 |
| Q2 | SCOPE, queries.csv 사전판 ac14b425 | A 자체 목적/넓은 A, 비가림 | 4×2; 단서 하나 |
| Q3 | receipts/INDEX, 8 JSON, G01 | API 버전 header 미확인; 당시 인덱스 아님 | 8/8 ordered |
| Q4 | paths.csv, G04, DUPLICATE_SCREEN | 16 고유 timeline, 하위 본문 전수 아님; 명시 duplicate 없음 관측 | 21/40 item,19 정상 없음 |
| Q5 | X01–03, O03/O04, C03–10 | exact reproduction vs solution, 11583 self rank2/5 미도착 | 7 고유 첫 도착 본문/댓글 |
| Q6 | M01–06,P01–05,C11–17 | 발행자 식별자, quote ≠ type, 2048 가설, C08 행 충돌, 후속 판 | 원문 비교; 실제 실행 미실시 |
| Q7 | pairs.csv, RESULT, COUNTEREXAMPLES | strict/partial 민감도, self-only 공집합 | 각 4/4 관측 |

자료 원장 42행, counted 39 unique works/18 lineages. 원요구4, Github 공식4, 소비자/응답/패치20, 제작자/규격6, 발행기관5. P05 parsed PDF 이미지 실패 비산입 가정: 38 works, publisher4. 메타데이터 P06 동일 work와 실패 F01/F02 제외. 영수증 별도. 사건 계보 10, 그 중 지명 4. 처음 10개 exact checked_utc가 첫 search 시각 복제였던 오류를 stage4에서 읽기 시간창으로 정정; P01 claim 축소. 자료별 확인 위치, 한계 및 산입 사유 명시. 
손계수 raw A,B by case (1,1),(0,0),(1,1),(0,1); ext (0,0)×4. 주척도 raw 개선1 tie3; ext tie4. Strict solution 2 없음; raw/ext tie4. 좁은 partial 정의에서 12856 U→raw tie3 U1. 정상 빈 외부4/8과 실제 무관련4/8을 별도 구분; incomplete=0, raw 요청 실패=0, 미열람 first=0. Original edit history와 exact API version 미관측은 rank/position 결측과 별개.
사전판·원응답 파일·40 paths·4 pairs의 대조 및 결과 SHA 재열람을 마지막 HANDOFF 전 수행. 공통 파일 변경/병합/배포 금지. 
