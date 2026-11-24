# AF-RES-128 SELF_CHECK — PARTIAL

| 질문 | 주장 | 고정 근거 주소·위치 | 반례·관측 | 판정을 뒤집을 조건 | 미확인·최소 다음 확인 |
|---|---|---|---|---|---|
| Q1 | 18답 허용필드, 13 실제 면, 5 stop 제외, 56 archive 무결성 | 99746d7da62c5bac396fa1cd6a1b6ac046df6f40 SCOPE; 62f09763ccb6d8b55ba93f7dc1258a884f81b885 projection/blind-packets.jsonl; 120 de99023970ca060e8227594c41448e6938efed23 | 12 반복 인지, B13 타사건 단서, 면 수로 시점 추정 | 금지 필드/실제 면 조인 오류 발견 시 해당 행 폐기 | 독립 평가자/단일 사건 시야 미실시 |
| Q2 | 72 원자 주장, 18답, H15/O3 | 418cf8865711c96c2b3a045f5a94a266fba417d4 blind-claims.csv 72행 | B01/B15/B17 확정적 보존 vs 조건부 문맥 해석 | 독립 판독에서 모두 명시 유보로 판단 | 별도 평가자 없음; 원판 실행하지 않음 |
| Q3 | 18/18 대응, 일치9 불일치9; 정의 차이 6·표현 차이 3 | f1c957a302812f28360a7defd01469211a6ae1ae concordance.csv; 124 7dd19f7fdac69b9dad4d6170ea247580b857f9b4 scores.csv | 후단 12/12 좁은 지지에도 H 우선, 124 P6 | 공통 정의 독립 평가에서 판정 유지/변경 | 기존 독자 효과 vs 평가 차이 분리; 사후 실행은 별도 |
| Q4 | 6개 N의 결정 조건을 찾아 기록 | d03a34bc6d56ad86d490c44244405682608cd1b3 candidates.jsonl; ad610cc4f8a2672387c8d857cdaa7dbcae78f4b1 selected-slices | P3 첨부 failed, J3 PR failed, 댓글 batch 상한 위반 | 원본 확보 및 단건 경로 재탐색에서 다른 N 선택 | exact 댓글 UTC, 적용판 미확인, source ordering 엄격 준수 실패 |
| Q5 | 6×3 18자리, N 공석0, F 9000/F+O 17397/F+N 12924자 | c9dbe949e8543763a321567f707e75ffe72530a6 bundles.csv; selected-slices | F+N 실제 길이 더 짧음, N도 필수 예외 미확인 | 각 N에서 동일판 입력·보존·예외 직접 지지 | 새 독자 효과 0 관측; 편집 이벤트 정확한 횟수 미계측 |
| Q6 | 음성 대조 3개, 경계 민감도 1개 | bundles NEG-WRITE, NEG-JSON, NEG-DUPLICATE, SENS-HEADER-ONLY; py39 Lib/csv.py L93–127, jq1.6 src/builtin.jq L297–303 | wrong direction, wrong syntax, duplicate id; 좁은 경계에서 dict(zip) 빠짐 | 더 좁은 같은 구간에 동일 메커니즘 존재 또는 실제 판 반례 | 동일 작업자 분석, 독립 동료 없음; 124 probe 재실행 금지 |
| Q7 | 판별 ISBN/매체·총보/파트 이조 일반 규칙과 개별 레코드 분리 | 9ef3061cfdaf72e2c6e7bfa0bab52f9c491b31ff sources.jsonl loc-bib020, loc-auth020, bm-print/ebook, argue-score, boosey-adiemus, nsm-massenet | 인쇄 레코드 자체에 두 판 묶임; octave 예외; A/Bb 개별 파트 | 판별 실제 인쇄/전자 원문 및 동일 마디 음표를 대조해 확인 | 악보 음표/도서 본문 직접 비교 미실시; ISBN과 매체 및 파트 안내까지만 증명 |

원장 보수 집계 24 고유 read work_id(최소 22 이상), 6 원 요청/6 정의·구현/6 별도 시험·예제/서지3/악보3. 실패 5행은 제외. 댓글 같은 issue는 별도 저작 아님. 작업 CLI checkout DNS 실패로 manifest.json 미생성, workbench.session start/check 미실행; 원격 readback은 별도 증거. 직접 새 실행/신규 독자 모집 없음. 해당 범위 전체 완료로 표기하지 않는다.

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
|---|---|---|
| 동일 사건 반복·답에서 단계 단서가 보이고 등급 우선순위에 따라 9건 불일치 | 제3 평가자에게 사건별 1답만, H 우선/부분 우선 두 축 사전 고정 후 교차표 작성 | 반복 없는 독립 판독에서도 같은 3건 확정 서술 지적 및 6건 유보 우선 차이 재현 |
| 새 면은 입력/구현을 보강하나 원판 실행 및 P1 EOF/P3 첨부 없음 | 원 파일 확보, jq1.6 및 실제 Python판에서 보존·예외별 고정 기대값 검증; J3 다중 cd/SEP 정상 header 음성 시험 | 동일 판·동일 입력에서 조작/보존/예외 모두 직접 지지 또는 명시 반박 |
| 전체 댓글 반환으로 경로당 3개 후보 상한 엄격 위반, 선택 댓글 시점·악보 실음·정식 세션 검사 미완 | 후보별 단건 열람 UI/타임스탬프, 악보 총보·파트 실제 음표 대응 확인 및 고정 시작판 workbench 검사 | 상한 준수 독립 재탐색에서도 N 선택이 유지되고 계약 검사 통과, 실제 판별 일치 |
