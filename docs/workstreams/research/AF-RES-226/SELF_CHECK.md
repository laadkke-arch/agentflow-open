# AF-RES-226 자체 점검 — PARTIAL

## 고정판·범위
- ① SCOPE a51afdd54112c88b50dde037f4cfd6beb492fc45; ② 원장 82781923e03e556ea331e9bc7c5d8d086f9d49a4; ③ 표 4a2fc3df6c5638b023ca6637bc45a5c827990f51; ④ 반례 931526981500b6f2a32c3e97f974b6f472b438a0.
- 계획판 fc095c323d0177401d34f1daa7b4d1c529e2351f / 착수 f3895893e32e2c055cefde446d34f1467fa27b4c. 중앙표 초기 실패 후 fetch_blob으로 복구. [scope-recheck.md](scope-recheck.md). 계획에는 226 없음, 최신 226 RUNNING attempt1; depends_on 207 및 SHA ded4731e82fd2e9efd1e10cec6c60f2dd55f7259 일치. 통합판 수정 금지 준수. 195/207의 96/24행은 이전 인계만; PET/DivEMT 재감사 및 216–218 제외.
- 원표 모드 P/PA/PM 각각 4자리, 세션 문자열 정렬 P01/P02 각 2, 원순서 segId 1/2. 12자리 모두 실제 .tgt 원행 확인; raw artifact revision bytes hash 미확인. 참가자 2명이 반복되므로 12 independent people 아님.
- source D01과 slot D01의 문자열 충돌: 파일/열 namespace 명시; 자동 매핑에서 단일 전역키로 취급 금지.

## 질문별 확인/반증
| Q | 확인 근거 ID 및 위치 | 반례·오판 방지 | 현재 상태/해제 |
|---|---|---|---|
| Q1 | R01/R12 목록, D01 §3–4, R13 파일명 | P와 PI/PA/PM 동일 의미 아님; DG21 전부 PE, HT 없음 | 모드 연구 수준 확인; LS14 개별 도구 로그 결측 |
| Q2 | R03–04 manifest 108/111, R06–11 .tgt W id/cur, R05 후보 목록 | R08/R11 첫 분절 동일 문자열, R13 basename 충돌 | 12 출력 확인/12 후보/0 exact 성공; error XML+판 해시 필요 |
| Q3 | D01 §4.3/5.5, T02–05, F01–04 | 300ms vs 다른 도구 pause; cur 위치; actor 없는 로그 | 12 생산 시간 결측, 12 review 시간 결측; 원행/단위/actor |
| Q4 | D01 §4.8/Table10, D02/D03, D04 | 152 issue 중 48 이견, 40 비일관; UI 저장≠수용 | 연구 별도 주석자 있음; 12행 actor/가림/인수 미확인 |
| Q5 | R04/05, F01–06/F10, T03, I02 Tables17–21 | optional 로그 존재 가능; I02 2단계 합산 가능 반례 | DG21 sum 0/author-only 0/unknown12; 확인성공 수이지 노동 0 아님 |
| Q6 | I01 §3/Table1/2/Fig1/Table5/Table11, I04 | EN→SV 및 EN→DA 방향 반전; 서로 다른 분모·outlier | 집계 4/4, job join/acceptance 0/4 확인; 원행/단어 가중 미확인 |
| Q7 | S01 p.25, S02 §2.2/2.4/Fig8, S03 Table3, S04 §3 | 결함수/속도는 시간 아님; 계획률·실제/elapsed·인시 구별 | 3 원연구 + 1 규정; 개별 log→repair→acceptance 행 미확인 |

## 자료/독립 계보/분모
- 44 원장 기록 / 27 산입 / 17 미산입. 미산입: 중복/소개/목록 4 (R02/R05/R14/T01), 실패 10(F01–F10), 제목만 2(F11–F12), 동일 저작 서지 1(I05). 각 직접 파일의 2분절을 2자료로 세지 않음. Terribile 출판본/저자판 1건. Temizöz 동일 학위논문 여러 표 1건. 산입 work_id 27, lineage_id 15; 도구 문서와 공식 목록 계보를 별도 실험으로 부풀리지 않음.
- 유형별 22 필수 배정(중복 배정 없음): 원출력 6/6 R06–11, 주석/정의/방법 5/5 R01,D01,D02,D03,D04, 시간/도구 4/4 T02–05, 산업/독립노동 4/4 I01–04, SW 원연구 3/3 S01–03. 추가 5 R03/R04/R12/R13/S04. 단, SW 원개별 기록은 미열람; 문헌/양식/집계 관측만. DG21error 및 LS14 핵심 원행 미열람은 이 수치로 대체 불가.
- 연구 사건 계보 9(DG21/LS14/Terribile/Temizöz/Daems/DGT-Macken/JPL/Porter/Fagan). 연구별 분모는 보고 단위가 달라 합쳐 독립 관측 수를 만들지 않음. DG21 6/6 선정 세션 실제 출력, 12/12 예정 분절 출력, error 연결 원행 0/12 확인·12/12 미확인; producer/reviewer/acceptance 각각 0/12 확인·12/12 미확인. Terribile 네 역할 4/4 집계·0/4 개별 짝/acceptance 확인. I02 pilot 두 개 사례 짝(별도, main 아님). JPL 203, Porter 88 검사 집계 및 기록 구조(원개별 연결 미확인).
- 주표본 F01–F06/F08/F10 및 ZIP/XML 접근 제한: 웹 도구 MIME/400/접근 오류, 실제 자료의 부재 증거 아님. 문서 판 SHA/개별 확인 UTC는 원장에 가능한 판과 열람 묶음 기록 시각 명기; 개별 HTTP 완료 시각은 미계측. Temizöz PDF 화면 timeout, 표 parsed text 읽음. 개인 이름 비수집(저자 공개 이름 제외), participant 익명 키 사용.
- 오판 조건 검토: exact join 없는 문자열 동일성, annotation count를 시간으로, 구판/현행 시간 기준 혼용, 연구 QA를 acceptance로, 산업 job 평균 역수 합, 다른 언어쌍·모집단 합산, missing→0 모두 차단. P19 추가 행 역할 추정하지 않음.
- 자체 점검 수행; 외부 독립 검토 미실시. 웹 Pro 역할로 신규 소프트웨어 실행/설치/자동 검사·코드 구현 미실시. GitHub 커밋 재열람과 경로 점검은 HANDOFF 전 별도 확인. 핵심 Q2/Q3/Q4/Q5/Q7의 실제 원행 결손 때문에 PARTIAL. 완료 조건을 자료 수로 대체하지 않음.
