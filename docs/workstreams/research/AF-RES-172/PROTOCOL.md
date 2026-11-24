# AF-RES-172 실험 서식 v0.1 — 설계, 미실행
## 질문 및 배정
같은 외부 목표에 대한 탐색 결과 수락 이후 직접(A), 그대로(B), 수정(C)의 사람노동/합격/탈락을 비교한다. 검색 자체의 효과나 AI 효과를 식별하지 않는다. S01/S03/S04, S05, S06–11, S19/S27. 실제 참가 모집·배정 금지. 사전등록 초안이며 숫자 예시는 실측 아님.

단위: 1 개발자(확장 시 팀 인원 동일) × 1 과제 × 최초 배정. 개발자 간 독립 6개 cell(X/Y×A/B/C), 동일인 두 과제를 주지 않는 방안 우선. 숙련도(언어, CSV, 부품 경험, 도메인, 익숙한 도구, 직전 비슷한 과제 횟수) 블록화; 계획 표본수·seed·블록 크기·배정 관리자·사전 검정력은 실제 실행 승인 전 동결, 현재 미정. 공통 Python 3.12.10, 표준 환경/편집기·네트워크/AI 허용 정책·공통 하네스 동결. 외부 패키지/AI 금지, 동일 공식 언어/CSV 명세 제공; A에는 부품 구현/코드 제공 금지, B/C 같은 고정 csv.reader 버전과 문서 제공. 부품 존재를 아는 A 참가자와 선택 오염은 기록. 초기 상태·기기·환경 설치 공통; 공통 setup이라도 소비자 특이 교육/설치 시간 포함. 배정자, 개발자, 검수자 분리. 검수자는 경로 라벨 가림(소스에서 추측 가능성 기록). 배정 경로 ITT, 실제 route/as-treated 별도 탐색; 교차/혼용/미사용 이유 기록, 탈락시키지 않음.

## 과제지 X — 바로 쓰기 가능
공통 공개 API parse(text: str) -> list[list[str]]; UTF-8 텍스트 이미 문자열로 주어짐; 지원 범위: comma delimiter, double quote, doubled quote escape, CRLF/LF 행끝, LF 또는 CRLF inside quotes 보존, 헤더 특별 취급 없음, 빈 필드 보존; 빈 입력 [] (빈 줄 제외한 입력만 시험), 유효 CSV만. 외부 IO/정렬/타입 변환 없음. Python csv 문서 S25 https://docs.python.org/3.12/library/csv.html (reader, dialect) 근거로 공개 설계 fixture를 만들었다; 해당 release 실제 실행 및 docs 3.12.10 대조 미실시(S34). 공통 최소 하네스는 text를 newline=""인 StringIO에 전달/결과 materialize/직접 함수 호출만 허용, 변환이나 검증은 없음. A는 좁은 grammar 직접 구현, B는 stock reader+설정/최소 binding, C는 동일 reader 유지+자기 수정/adapter를 허용하되 실질 수정 없는 경우 actual B.

| ID | 입력 (\\n,\\r = 실제 문자) | 기대 결과 |
|---|---|---|
| X1 | a,b\\r\\nc,d\\r\\n | [["a","b"],["c","d"]] |
| X2 | a,"b,c"\\n | [["a","b,c"]] |
| X3 | "a""b",\\n | [["a\"b",""]] |
| X4 | "a\\nb",c\\n | [["a\\nb","c"]] |
| X5 | 빈 문자열 | [] |
| X6 | a,b,c\\n | [["a","b","c"]] |
| X7 | ,\\n | [["",""]] |
| X8 | "a\\r\\nb",c\\r\\n | [["a\\r\\nb","c"]] |

## 과제지 Y — 같은 API, 정책 adapter 필요
같은 문법 및 반환 타입. 단 모든 행의 필드 수가 정확히 2가 아니면 전체 결과 대신 ValueError("width")를 발생시키며 부분 출력 금지. X1–5, X7–8 동일 기대; Y6 X6 입력은 ValueError("width"); Y9 a,b\\nc\\n 역시 ValueError("width"); Y10 a,b\\nc,d,e\\n 역시 ValueError("width"); Y11 "a,b",c\\n 은 [["a,b","c"]] (단순 쉼표 세기로는 실패). 오류는 문법이 아닌 정책; malformed CSV 범위 밖. B는 stock reader가 행별 list를 반환하므로 너비 검사 없이는 계약 불충족(문서 기반 예상, 미실행); 이 cell을 불가능성 sentinel로 사전 지정하고 성공 경로와 평균 비교하지 않음. 요구 위반하지 않고 중단할 수 있으며 실패/노동 원분모에 둔다. C는 기존 reader 실호출 + 결과 행별 검증, A는 직접 파서+같은 검증. B에 검사 추가 시 C로 실제 분류, 원 배정 B 유지. C가 파서 핵심을 새로 구현하여 기존 parser를 실호출하지 않으면 actual A; 부분 호출/우회는 mixed, 코드 검토 근거 기록. X와 Y 입력·출력 차이는 과제 간만; 같은 과제 내 모두 동일. 구조적 불가능성은 사람 능력 효과와 구분.

## 마감/검수 (설계값)
t0 명세/환경/부품 제공·배정 공개, t0+120 wall min 첫 제출/중단 마감(1 개발자). 담당 검수자 1인은 동일 fixture 및 금지 도구/경로 위반 검사, 30분 내 초기 인수(제출 즉시 검수 가능; 결과·검수자 활동 시간 분리); 개발자에게 동일 형식 피드백 1회, t0+180분 최종 제출, 개발자 활성시간 총 150분 상한; 독립 검수자 활동 최대 30분 전체(초기+최종), 최종 판정 t0+210분. 인수 점검표: 과제별 모든 mandatory fixture pass, 반환형/예외 계약, 외부 의존 금지, 재현 가능한 버전 및 제출 hash, partial output 금지(Y), 미제출/기한초과/기능 fail/경로위반을 별도 코드. 기능 합격과 경로 준수 별도; ITT 성공은 기능 계약+공통 정책 합격, actual route 기록; 경로만 위반 시 기능 pass를 숨기지 않는다. 각 fixture observed expected status evidence; 독립 검수자가 실제 확인하고 익명 평가자 ID 기록. 공통 절차/정답 세트·검수 시간 상한 사전 동결; 이 문서의 수용테스트는 수작업 설계, 실행 결과 아님. 판정 부재는 unknown, failure로 대치하지 않음. 중단 이유/마지막 상태/elapsed/관측된 활동 보존. 사전 탈락 vs 배정 후 미시작 분리. 철회 데이터 허용 범위, 누락만 보고(동의/윤리 검토 후 실행). 
후속 7일 창: 최초 납품 뒤 동일 오류 발견/유지 요구에 발생한 소비자/유지자/검수자 활동 별도; 미응답/미관측=NA, 0 아님. follow-up 관측 기점 final decision/미납품은 마감, 실패를 제외하지 않음. 실제 후속 활동 상한 미정이므로 결측 시 상한 없음. 1회 창은 t0~최종판정까지의 개발·검수, 후속 포함 확장창 별도.

## 기록지 및 합계
effort-form.csv 첫 행은 header, BLANK_TEMPLATE 1행은 복제용 빈 행, DESIGN_EXAMPLE 행은 예시만. 실제 row_type=OBSERVATION, 각 event ID·assignment ID·person pseudonym·role·UTC timestamps (ISO8601)·primary activity·unit·source·confidence·window·overlap group·related submission/fixture·amendment link. source_id 참조. 별도의 ASSIGNMENT row 1개씩으로 분모 고정; REVIEW row fixture별, STOP row 이유, CHANGE row 교차와 근거, follow-up row, PRODUCER row. 원 단위 보존, active interval은 seconds→/60 person-min, 자기보고 합계만이면 reported_duration 별도. 누락 이유(unknown, declined, not collected, log failure, not applicable)와 0(명시 관측된 영) 구분. 
활동 분류: SEARCH(수락 후 자료), LEARN, SETUP, DESIGN, IMPLEMENT, ADAPT, DEBUG, TEST, REVIEW, REWORK, SUPPORT, MAINTAIN; IDLE_WAIT(machine/person/blocked), BREAK, OFF_TASK 별도. 사람이 기계 기다리며 문서를 읽으면 그 구간 LEARN; CPU 경과 독립 기록; 기다려야만 해서 묶인 available time은 별도. 한 사람의 동시에 열린 타이머는 union of half-open [start,end) 구간, primary activity 하나를 기록하거나 겹침 unresolved; 분류 총계 unresolved bucket 포함, 다중 태그 중복합 금지. 서로 다른 사람은 합산(30+30=60인분, 경과 30). 중복은 동일 person_id×동일 task에만 union; 동시에 서로 다른 과제는 allocation 합≤실제 시간, 미해결 플래그. 음수/역전/단위 모호/창 밖 reject/보정 로그, 원행 덮지 않음. 활동시간이 실제로 모두 관측되었는지 coverage flag. machine interval, wall elapsed, report duration, 원척도를 물리 인시로 합치지 않음. 독해·숙고 무입력 시간을 자동 제거하지 않는다(S08, S26, S29).
 
## 산식 (분모와 결측)
cell g의 N_g는 배정 전 동의 후 배정된 모든 assignment 수. p_g=known pass/N_g, u_g=unknown quality/N_g. 실제 합격률 범위 [p_g,p_g+u_g]. 실패·중단·미시작 남김; 확인된 미시작 0만 0. 모든 배정의 관측 기간 활성인분 L_i=Σ_person |union active|/60 (개발자+독립 검수자+해당 도입 지원, 지원 별도 role, 중복 없음). 1차 결과 벡터 (p_g, u_g, ΣL_i/N_g [전부 관측일 때만], missing L_i/N_g); 지원 인시 상한 미정이면 소비자+검수만 별도 cap 180 인분/배정, 지원 포함 총 상한 없음. 결측 노동은 관측 합/N 하한, 유한 상한이 사전 정의된 역할에 한해서만 (known sum+Σmissing caps)/N 상한; 부분관측은 관측 구간 하한. 결과 명시: 완료자 평균, time-to-pass/censored wall, 최초/최종 pass, 역할별 분해, 재작업·후속·기계경과, route adherence는 보조. 동일 품질/창/모집이 없으면 절감 주장 금지. A-B와 A-C는 shared A, 독립 효과 아님; 동일 설계에서 covariance/cluster 반영; 서로 다른 과제 X,Y를 한 평균으로 섞지 않음. 실패의 시간은 실제 소비된 값만, 마감시간 대치 금지. N=0 계산 금지. 누락이 0이라도 합격률 다르면 시간만으로 우열 금지. 동등성 마진/실제 표본수·추론 계획 미정(실행 전 사전등록).

## 비용 및 사용자 관점
F_g 선행 제작·유지준비(생산자), I_g 1회 교육/도입/공통 setup 중 경로 특이, U_gj 소비자 실행+디버그+시험, V_gj 독립 검수, R_gj 후속 수정(소비자/유지자 별도), M_g(N) 공유 유지/버전 전환, S_gj 지원. 모든 항은 같은 단위/창, 중복 없이: Total_g(N)=F_g+I_g+Σ_j(U_gj+V_gj+R_gj+S_gj)+M_g(N). 이미 존재하는 OSS F는 소비자 관점 sunk(0 추가 지출, 실제 노동 0 아님); 생태계 관점 실측 배분(증분 또는 전체), N과 귀속 기준 명시. 1회/반복 비용 차이 A−g, N회 평균 /N; 고정 차이 ΔF+ΔI, 매회 절감 d>0 일정 및 유지차 0 가정이면 임계 N> (F_g+I_g−F_A−I_A)/d. 미확인 F/M/R은 기호로 두고 조건부 경계만; 화폐 비용 계산은 역할별 요율 필요. 최종 사용자는 계약 품질+납기, 도입팀은 활성 노동+교육, 유지자는 재사용 부품 원가/지원/호환성, 독립검수자는 검수+수정, 관점 간 상쇄를 합쳐 지우지 않음. 탐색 전 검색비용은 별도 실험창으로만 추가.
