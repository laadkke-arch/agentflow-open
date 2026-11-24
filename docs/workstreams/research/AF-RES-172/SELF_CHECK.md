# SELF_CHECK — 작업자 자기점검 (독립 검토 아님)
상태 PARTIAL. 고정 통합/의존/시작 SHA SCOPE. 현재 주 결과의 입력 커밋 ad5bd94776de126c5c46b7b1c1d0cb9b9c4a44e5. 검증한 원장 57행, direct-read 40(의존 1), 실패 16, abstract-only 1. 신규 직접 읽은 행 39, 고유 work_id 24 (보충 포함); 각 URL/읽은 구간/한계 기록. 독립 관측 lineage 후보 17 (Screen2016/2017 중복 미확인 및 일부 보고 보충; 원행 실제 SW 5 계보 별도). 전체 검색 클릭/재시도 로그를 완전히 보존하지 못했으며 sources의 57은 실제 총 클릭수가 아니다. 문서 간 재열람/같은 DOI 패키지 중복 제외, 하한 후보 18; 완전한 적격 판독 수는 이보다 적을 수 있다. S12/S13 경로 오류 S40/S41 복구.
 
| 층 | 예정 | 실제 보수적 후보 | 부족 | 산입 ID |
|---|---:|---:|---:|---|
| SW 원보고 | 6 | 5 | 1 | S01, S05, S28, S35, S36 |
| 별도 author artifact | 6 | 3 | 3 | S03, S06, S38 |
| 시간/탈락/검수 protocol | 4 | 4 | 0 | S19, S26, S27, S29 |
| TM 비교 | 3 | 3 | 0 | S21, S22, S23 |
| 기록물 | 3 | 3 | 0 | S24, S45, S46 |
| 합 | 22 | 18 | 4 | 후보 count, 하한 불충족 |
 
주의: S36 도메인 모델 제작, 코드 구현만이면 4 SW 원보고. S22/S23 최종 품질표, S24/S45/S46 역할별 노동+최종 품질쌍 미확인; Q6 엄격 판독 3+3 미달. S25 명세는 보충. S42–43 CITR 원과제+원표는 직접 판독했으나 파일 찾기 평가와 실제 구현 다르고 파일 최초 공개일 독립 확인 못 해 하한 제외. O1 과제지·검수/기록 양식·원자료 자체는 별도 문서로 모두 직접 읽었으나 같은 패키지 DOI를 늘려 산입하지 않음. S16–18 Echoes 고정 2025 패키지 파일 일치 미확인. 2012/2013 자료는 SW 기간창 외, 별도 분야 보충층.
 
| 질문 | 근거 행/결과 행 | 반증 시도 | 판정 및 미확인 |
|---|---|---|---|
| Q1 | S01/03/04/05/06/07/09/10/40/41/35/36/42; PROTOCOL ASSIGNMENT/STOP | 완료원장≠배정, 숙련·도구 미사용·시간제한 | 부분 충족; 최초 목록·METR prereg·개별 탈락+과제지 추가 |
| Q2 | S08/22/26/29, W10; E01–03 | silent log editor, 두 사람 합 vs 한 사람 overlap | 정의·예시 충족; actual simultaneous interval 원행 미확인 |
| Q3 | S25/34/40/41/42, X/Y | ragged CSV B impossible; simple comma count fails quoted comma | 설계 fixture 충족, pinned runtime 확인/기존 실제 과제 input의 직접 이식 미충족 |
| Q4 | S07/19/27/28/35/37/43, W11/14/15/16 | timed out≠pass, survival reversal, quality local≠global | 설계 충족; 실제 각 route success rate/margin/power 미확인 |
| Q5 | S01/15/24/30/45/46, W12 | 1회 적자→반복 흑자; upstream not free | 식/역할 충족, empirical F/I/V/R/M 원행 미확인 |
| Q6 | S21/22/23/24/45/46, W18–19 | 입력수/문자 정확도 vs 실제 시간/최종 품질; S47 abstract만 제외 | 부분; TM/기록물 paired labor+final quality 부족 |
| Q7 | D01, W01–09/15–19; S04/11/17/18/39/43 | raw unknown/scale, valid≠correct, same A, blank≠0 | 5 원행 계보 적용, 3 물리 단위, 실제 A/B/C 활동+검수+전분모 0 |
 
## 분모 대조
- frame.csv header + 76행: natural Z/O/A 각 8=24 unresolved, S01–S52 52 supplemental source rows. 원 목록 0자리 복원; 25–48 확장 실행 안 함. F01–04/D01 sources에만 있고 natural rows와 의존으로 별도. original_position 빈 보충행을 original rank라 부르지 않음. 
- sources 57=52 S +4 F +1 D. 40 read+16 failed+1 abstract. 18 counted candidate. Work ID와 lineage를 분리; 클릭 수와 신규 문서 수 동일 취급하지 않음. 검색 스니펫 결과 노출 및 실제 query 반환 목록 불완전 SCOPE에 명시.
- worked-cases.csv header +19행, W01–09,W15–19=14 관측/전사/보고 요약; W10–14=5 가상; 혼합 산식 없음. W07 2610/60=43.5, W05 232+10=242, W11 (60+60)/2=60 vs (20+120)/2=70; W12 30N−90; W14 [30/2,(30+180)/2]=[15,105]. 동일 A 원척도 차 방향만. 손계산, 실험 코드/일괄 검사 하지 않음.
- effort-form.csv blank template/assignment/review/stop/producer 및 별도 DESIGN_EXAMPLE. Protocol primary union+all assigned N, p/unknown, missing L; 지원·후속 cap 미정. X/Y exact outputs·마감·역할/phase 명시. actual route 분류 및 pre-assignment Y-B sentinel 보정. 검수자 블라인드 실제 source audit로 깨질 수 있음.
- 공개 소스 PDF screenshot 실제 성공: S21 p131/p136, S22 p8, S24 p1, S30 p1, S35 p17, S37 p30, S42 p1, S43 p1, S46 p156/p158. 실패 S23/S28/S29/S45는 text 기반 읽음, 시각 판독 불가 명시. 
- 자료 원값은 필요한 구간만, 개인 식별 데이터 재공개 없음. 과제지 일부 문서 시각 자료 미확인. 모집·처치 배정·실제 코드 실행·신규 절감률 없음. 
- 대표 커밋 재열람: scope ded04def7d2ed25e4f45552df9c0e3e96290c874; first sources e4e1dde47f8768352e10075d52af2f49814990d8; W01–09 0acb885debc9e7390d24369aef9afda8e7d69615; sources 마지막 S52 및 행 분모 ad5bd94776de126c5c46b7b1c1d0cb9b9c4a44e5. RESULT/HANDOFF는 커밋 후 다시 열어야 함.
 
## 미충족 및 재개
1) first 24 natural slots 원순서; 22 후보 4 이상 부족, 엄격 적격은 추가 부족. 원 메타 목록 복구 후 결과를 가린 상태로 DOI/date/실제 raw availability 판독. 2) METR prereg URL·OC article 정식판·Echoes v1 and v6 package match·Frattini raw 경로·Piantadosi figshare access. 3) TM/기록물 비교 원 시간/최종 품질표와 역할별 창. 4) fixed runtime fixture 검산(후속 허용 시), actual trial 승인 전 설계 파라미터와 자료권한. 현재 참가자 효과·실측 절감 미확인. 
