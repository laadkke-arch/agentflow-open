# ④ 반례 및 정정
직접 원행 재판독: 초기 전체 246, 110/136; 초기 합 9999/16257.5분; 후기 기록 합 1000/1898 (n103/127), 관측 0 53/56. 초기 zero 0, noAI 예측 nonpositive 0. 그룹 평균 대체는 1000/103=9.708738, 1898/127=14.944882분. 후기 결측 7+9=16(6.50%) vs 논문 C.3.4 27 및 코드 주석 ~12%: 공개 판이 동일한 수집 상태라는 가정 기각; 변환 이력 미확인. 원자료의 raw blank를 보존하고 모형 입력용 값 별도. 독립 preprint M04는 동일 SHA, Table2 230 recorded; 기하비 +18.8%, 산술 보정 +24.0%, CI jackknife 0 포함. 동일 연구 재분석이지 두 번째 개발 실험 아님.
후속 원행 상태:
| 상태 | 0 N / 초기빈 / 후기빈 / 초기0 / 후기0 | 1 N / 초기빈 / 후기빈 / 초기0 / 후기0 |
|---|---|---|
| complete | 368/0/0/3/238 | 460/0/0/1/289 |
| incomplete | 124/82/106/0/11 | 120/91/117/0/2 |
| ditched | 29/26/26/1/2 | 28/20/24/0/1 |
| cheating | 2/0/0/0/1 | 0/0/0/0/0 |
| corrupted | 0/0/0/0/0 | 3/0/0/0/3 |
완료 828; 전체 1134. L03 조건을 JS로 직접 원행 필터 판독(회귀 미실행): complete-valid 367+460=827; started 365+459 complete, 42+29 incomplete, 2 cheating+3 corrupted=900. ditched 0 (제외), started의 예측/초기 유효 조건을 통과하는 이상 상태 5건. README 3상태 및 cheating 제외 설명과 실제 불일치. started도 종속변수 총합, 이름만 초기 시작. L01 L3 incomplete allowed 24+blank; L196 ditched allowed 200+200=400분 보고, 완료만 남기면 누락. 이 값의 실제 작업/오입력은 미확인, 상태를 0으로 바꾸지 않음.
독립 품질의 반례: T03 En2→Tr2 47.45+18.91=66.36분, QA66.39 Fail, En1→Tr1 79.17분 QA93.36 Pass. 더 빠른 둘의 합이 인수되지 않을 수 있고 revision이 오히려 품질 68.46→66.39 악화. Tr1→En1 69.71분 QA95.02 Pass. 동일 번역 사건 역할연결은 가능하지만 연구 QA Pass≠고객 수락, 평가자의 labor unknown. T04 빠른 단일언어 검수는 오류 탐지 열세. S05 median 4h 미만은 elapsed, S06 14.7~20.8h도 review interval, S04 22 person-hours/KNCSL는 labor; 섞지 않음. S01 별도 독립성 증거지만 시간 하한 산입하지 않음. M01 실제 사용 조건 제한은 ITT 깨짐, M02 completion selection monotonicity 불확실, M03 diary 단계 생략 가능.
가상 통제(실측 아님): A control author80+review10+rework10+accept5=105, allowed author40+review60+rework15+accept5=120 → 작성 50% 절감에도 총 14.29% 증가. 노출 but no use 사례 원배정 유지; 같은 artifact hash review; 회피 과제도 status/time. 10 assigned per arm, 8 complete×50 min+2 fail×200 vs 10 complete×80 = 800 each/assigned, accepted per arm 100 vs 80 min; 성공자 평균 50 vs80과 방향 반대. 가상 2 review rounds/acceptance 키·시간이 빠지면 총노동 unknown.
원장 31행, counted 23, group {"early":4,"late":6,"software":5,"translation":4,"methods":4}, counted unique lineage 16 (Rigby 재사용 사건 포함 가능; 사건 수와 동일하지 않음). E05/E06 duplicate excluded; T03 재접속 성공; F01 initial timeout 유지. 원자료를 더 못 찾은 early 5th 독립 artifact 미충족. 초록 D02/T04의 증거 깊이 낮음 명시.