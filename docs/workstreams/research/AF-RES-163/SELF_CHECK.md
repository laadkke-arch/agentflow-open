# SELF_CHECK — AF-RES-163 자기검산 (독립 검토 아님)
## 주장 → 원문 위치 → 원장·분모 → 반증 조건
| 질문 | 주장 또는 미확인 | 원문 URL·정확 위치 | 원장·분모 | 반증·최소 보강 |
|---|---|---|---|---|
| Q1 | 대상 제출자·closer·구독자 구분; GNU code route 미확인 | https://www.debian.org/Bugs/Developer L12–48; https://www.debian.org/Bugs/server-control L12–15,56–100,114–117 | P1–P6 6 규약; GNU 직접 티켓 0 | 당시판에서 다른 수신 대상 규정 또는 실제 originator 변경·구독/병합 |
| Q2 | 원 제출자/closer 발신 로그 별개 | https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1074014 L2346–2352; https://lists.debian.org/debian-policy/2025/02/msg00040.html | T1074014,M1074014; 보충 8 원 제출자 +8 closer | 같은 event의 원 제출자 대상 송신 기록이 다른 시각·역할이면 조정 |
| Q3 | 특정 통지 내용 인지 1건(보강) | https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1020248;msg=97 L1211–1250; L1073–1074 | J04 X1020248B/C; 보강 원 제출자 11 중 승인 1; 자연 0 분모 | 원 제출자 동일성/시각이 틀리거나 인용이 다른 통지면 보류 |
| Q4 | 반복/다른 수신인 조인 거절 | https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1034732 L232–238,336–368,434–445; https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1095935 L1032–1033,1148–1175; https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=990667 L405–411,545–569 | J05–J08; 반례 4 독립 티켓(동일 Debian 운영) | 해당 원 제출자 별도 인용·정확 event ID 발견, 전달/병합 기록 |
| Q5 | J04 재개; 보충 후속 2는 인지 인과 미확인 | https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1020248 L1382–1386; https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1027832 L708–734; https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1075856 L605–609 | J01/J02/J04; 자연 행동 분모 0; 보충 2 후속, 0 인지 조인 | 정확 통지 인용/수신 진술, 이후 실제 상태; 수락/감사 별도 원전 |
| Q6 | 학술 리뷰 내용 응답, ED 수신 보류; 시민 한 강한 내용 연결·한 부분 대조 | https://egusphere.copernicus.org/preprints/2024/egusphere-2024-1354/egusphere-2024-1354-AR2.pdf p1 L3–26, https://egusphere.copernicus.org/preprints/2025/egusphere-2025-419/egusphere-2025-419-AR1.pdf p1 L0–44; https://democracy.medway.gov.uk/mgconvert2pdf.aspx?id=59254 §5.4–5.5 PDF p5; https://democracy.north-herts.gov.uk/ieListDocuments.aspx?CId=151&MID=3988 item62 L37–43 | J09–J12, E1/E1R/E2/E2R,C2/C3/C4; 학술 2·시민 2 중 완전 1 | 동일 ED 통지와 저자 응답 직접 조인; 시민 두 번째 원 제출자 회신 |
| Q7 | 약속 수준에 따른 최소 증거 | P1 URL 및 https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1020248;msg=91 / ;msg=97 | 표3 12 판단(승인6 보류6), advice 6 | 별도 독립 검토, 동일 통지의 직접 수신 자료, 원문과 반환문 불일치 |

## 원장 기계적 자기검산
GitHub ④의 고정 원장을 다시 읽어 동일 작업자 JS로 JSONL parse, 각 완전 인용 CSV의 열수·원장 ID 연결, 통지 역할별 집계. E1R/E2R 및 보정 joins는 이번 ⑤ 쓰기 직전 동일 방식 검사. 결과: sources 74 (47 opened / 27 failed), unique work 28 / 실질 24, 중복 source_id 0; 원장 참조 누락 0 (헤더명 기준 재검산). 행수/열수불일치 [["notifications",36,0],["frame",36,0],["tickets",34,0],["joins",13,0],["advice",6,0]]. G/S/A/R tally: supplement {"rows":17,"g":16,"s":16,"o":8,"closer":8,"a":0,"r":0}; counterexample/later {"rows":19,"g":19,"s":19,"o":11,"closer":8,"a":1,"r":1}; total {"rows":36,"g":35,"s":35,"o":19,"closer":16,"a":1,"r":1}. 20 예정 자연자리 전부 미배정, 미확인 상태를 음성으로 변환하지 않음; 확장 순서 미복원. 원 제출자 A/R는 J04 한 건만, closer-content-only 2행은 A에서 제외. D1034732 인용도 역할로 거절. 전달 수신증은 전건 unknown; 미수신으로 센 행 0. J13은 6 꼬리 묶음으로 전수 무응답 사례 아님. 학술 PDF에서 reviewer 인지는 확인, 정확 editor notice 인지는 유지 보류. 158 고정 state_checks/traces 각각 28 데이터 행 재조회. 계획판→실제 시작은 GitHub compare ahead4/behind0, dot-control만 +190/-6. 원문 JSON 전체는 대용량 실패, 배정 diff 확인만.

경쟁 설명을 찾은 범위: (1) 자기 종료/다른 UI/다른 연락을 통해 이미 상태 인지 — J01/J02의 판정을 낮춤; (2) 서로 다른 수신인/반복 종료 — J03/J05–J08 및 E2를 거절; (3) 공개 게시됐으나 이메일 미발송 — C2 실제 기록; (4) 회신은 했어도 요구 충족 실패 — E1 이후 리뷰와 D1034732/D1095935. 원 제출자가 응답하지 않았다는 전체 창이나 실제 배달 실패는 검증하지 못했다.

실행/독립 검사: 별도 checkout·빌드·제품 실행 없음. 이 JS 검산은 형식/자기 원장만 검증, 외부 원문 완전성이나 역사적 모집을 보증하지 않음. 최초 접근 단위 기록 일부 묶음·실제 순위 미복원·30일 연속 관찰창 0은 남은 결함. 소스 추가·정확 조인이 없으면 PARTIAL 유지.

### ⑤ 보정 커밋
첫 자기검산(a5d8367)은 notifications.csv의 location 열을 source_id로 잘못 지정하여 37개 미해결처럼 표시했다. 원판 보존. 헤더 기반 재검산(0-based notifications source_id=16, tickets source_id=10, joins source_ids=4, advice source_ids=4) 결과 실제 누락 0. 검사 대상: [["notifications","source_id",16,36],["tickets","source_id",10,34],["joins","source_ids",4,13],["advice","source_ids",4,6]]. 데이터 행/판정·분모는 바꾸지 않았다. 표1 발신 근거 괄호는 URL 중복 대신 location을 표시하도록 정정. 독립 검토 아님.
