# SELF_CHECK — AF-RES-153 (self review, PARTIAL)

## 검산 범위와 방법
고정 원격 ④ ee78f61491bbea4c644f8844b4e32f81c2302019에서 GitHub fetch_file로 frame.csv, frame-extension.csv, exposures.csv, pairs.csv, contrasts.csv, sources.jsonl, SCOPE.md, COST_AND_ACCESS.md, SEARCH_LOG.md를 다시 읽었다. JSONL 실제 파싱, quoted CSV 줄/필드 파싱 및 참조 대조(도구 JS, 체크아웃 아님). 실제 계산: 원전 34행/고유 source_id 34, URL/위치/한계 등 필드 빈칸 0, access success26/partial3/failed5; counted 고유 work_id20, experiment10(ACM4/공학6), stimulus patent6, engineering field primary2, interaction field primary2. 특허 원문 발행 원면 6을 제3자 호스팅에서 읽음: 호스트를 엄격하게 제한하면 하한14; 공식호스트 직접열람 추가 필요. 중복 실험 A03 자료 3행, X11 2행 및 인접 분야 등 불산입. 38 반환행 A1=11 A2=8 B1=8 B2=11, 고유 candidate A01–04와 B01–05/B07–08(7), 보충8행. 15/30 최초 후보 완성 아님. 보충 3 target experiments + 외부 IEEE 별도. exposures12, pairs11, strict_pair=1 0, contrasts19. 3 CSV 참조 토큰 50개, 없는 source_id 0; 미참조 7개는 S08/S12/S13(모집 차단; frame/table1), S19/S22(자극 원전, Q6), S25/S26(자극 실패, Q6). 원전 역추적은 이 예외를 포함. 수치·분모를 독립 판정하거나 연구 데이터 재분석하지 못했다.

## 질문별 주장 ↔ 원전 ↔ 원장 ↔ 한계
| 질문/주장 | 원전 위치/링크 (sources.jsonl 해당 ID의 URL, fixed_address) | 원장 행/역추적 | 한계·반증 |
|---|---|---|---|
| Q1 후보 모집 불완전, 원파일 접근 실패 | S01–18, S04 README/pilot_data, S12 dataset item, S18 OSF | frame A1-1..11,A2-1..8,B1-1..8,B2-1..11; frame-extension 8; RESULT 표1; SEARCH_LOG | 네이티브 색인 순번과 30까지 채워야 함. 새 공개 부록이 두 연구 이상 적격이면 현재 연결수 수정 |
| Q2 배정과 실제 열람 분리 | S01 Fig5; S03 §3; S10 p533; S14 §3; S15 Fig2; S16 Fig4–6; S17 §6 | exposures 12행, C01–10, RESULT 표1 | 이벤트 행/시각 미접근, A02 초기 공통 예시. 배정과 개봉 대조가 되면 노출 판정 갱신 |
| Q3 엄격쌍 0/8, 연구0/2 | S03–05, S10, S14, S15, S16, S17–18 원문 위치 | pairs 11행 모두 strict_pair=0, 표2, 노출 행과 work_id 매칭 | 초기/후기 원면·ID·자극 타임스탬프 미조인. 누락은 무변경이 아님. 첫 4 ID 순서 다시 적용 |
| Q4 구체화/신규를 결정 못 함, 표현/구조/복사/실패 사례 | S03 §3; S15 Fig2; S16 Fig4–6; S17 Fig7/§6.3 | pairs A03 2, B09 2, A05 3, X11 4; C08–10 | 저자 선택 사례; 최초 인지 발언 P17도 원면 없음; 연구자 구현을 참가자 변경으로 세지 않음 |
| Q5 반대 결과 및 분모 분리 | S02 §3, S07–11 방법/결과, S14 Fig2, S15 Fig4–5, S16, S17 §6 | C02–10, 표3, exposures | 153명과 1321개 개념/1066 분석 혼동 금지, 66명-6 손상=60, 64 선택 57/7, 145 사례사건=89+56. 원대조군/개봉/누락 조인 재계수 불가 |
| Q6 자극 원전의 동작/제약과 현장 반례 | S14 Table2→S19–26 원면 및 claim/설명, S27 pp451–452,461, S28 xiv, S29–34 절 | C11–19; S19/S22/S25/S26 Q6 직접 링크, Q6 설명 | 특허가 소프트웨어 실행 증거 아님; 근거리 충분성 가설, 도로 감지/발전 출력 다름. 현장 권고/후속 시행 분리 |
| Q7 동일 링크 전달안 둘, 실제 비교 없음 | S29 절, S21 Fig2–3,9 | C15,C11 및 Q7; COST_AND_ACCESS | 작업자 추가 테스트 제안, 사용성/시간 절감 미측정. 원전 조건 실패/유지 결과 없으면 결론 보류 |

역방향 검사: 20 count된 고유 work_id와 모든 실패/부분 접근은 frame, exposure, pair, contrast 또는 RESULT Q6/표1로 연결. 원장 source_id 및 work_id는 연구 본문과 원자료 접근 행을 동일 저작으로 묶는다. C19의 F07/F08은 현장 시행 결과 아닌 지침/계획으로 별도. B06의 학회/저널 동일 실험 중복 제외; B04 자극 재사용 B09는 별도 참가자 실험으로만 세고 자극 원전 수를 늘리지 않았다. B04 prose/Table2 번호 불일치는 해결하지 않음. A04 인접 제작 연구와 IEEE X11 및 추가 F05–08 성공 본문은 최소량 산입하지 않았다. 실제 개별 열람 시각은 stage seal 기준, 시각 필드의 한계를 기록. 접근 로그와 본문을 분리. 원자료가 공개되지 않았다고 단정하지 않는다.

## 변경·무변경 및 검토의 한계
145의 8 자기 판정은 규칙 예시로만 사용했고 재검색/사람 데이터로 전환하지 않았다. 이번 작업자 단일 GPT-6.2 컨텍스트, 선행 원장 노출 있음, 독립 검토자/참여자 새 모집 0. 본문 보고 수치와 연구자 평가를 원실험 참여자의 변화·최초인지·시험 수행으로 바꾸지 않았다. 실제 반대 결과 C02/C03/C04/C06/C08/C09/C10, F02/F04/S32와 원전 S21/S23의 다른 출력에서 찾음. 새로운 원면과 비교군 동일 조건 자료가 효과를 약화/역전하면 현재 방향 제안을 철회. 변경 없음/기각은 실제 쌍이 있을 때만 센다.

## 실행·검사 및 커밋
① e8a00888ed5029b758a4a833335b817b23463299 SCOPE.md 재열람 일치; ② d74d80b7e87319140372a2a0a8193d981877ef48 frame.csv 재열람 일치; ③ 01a78c206c33d71ed166a5cff05b604054c50d18 pairs.csv 재열람 일치; ④ ee78f61491bbea4c644f8844b4e32f81c2302019 sources.jsonl 재열람 일치 및 ⑤ 봉인 전 위 JS 검산 완료. 기준 9e378ca91c399454466196617cf362d0cdb514f9; 계획 기준 f140af3179b7d9271710778104ccee5b4812e2ef 대비 ahead3/behind0 dot-control +92. 저장소 로컬 checkout 시도 실패(네트워크 DNS). git ls-remote exit128, python -m workbench.session --help exit1 ModuleNotFoundError; 체크아웃 검사/manifest 실행/공통 스크립트 미실시. 외부 소프트웨어/사람 시험 실행 없음. 실제 검사 범위는 원격 커밋과 파일 재열람 및 JS 원장 구조 검사. RESULT와 이 파일의 고정 결과판 원격 확인, 시작판 대비 범위 확인은 ⑤ 직후 HANDOFF에서 기록. 기준 하한 미달 및 검증 불충분으로 PARTIAL.
