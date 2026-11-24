# AF-RES-164 자기검산 (독립 검토 아님)

검산 대상 결과 초판: 90e2e43bfd3a81de5f82521dff66a44842c9fc83. 이 고정판에서 원격 재열람한 sources.jsonl 38행, frame.csv 41행, studies.csv 18행, arms.csv 23행, contrasts.csv 20행, lattanzi-raw.csv 24행(헤더 제외). 동일 작업자의 재판독이며 독립 복제나 연구 실행은 아님.

| 질문·주장 또는 미확인 | 원문 URL·정확한 위치 | 원장 행·분모 | 반증 조건·낮춘 판정 |
|---|---|---|---|
| Q1 같은 후위표기 과제·개인 배정 확인, 자연 모집 미복원 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) §5.1–5.4, App D pp165–167; [S24](https://www.mi.fu-berlin.de/inf/research/publications/techreports/tr2007/B-07-03/tr-b-07-03.pdf) §1.2 p4; [DBLP](https://dblp.org/db/journals/tse/) | ST06 A08–10 R1–24, 8/8/8; ST10; F01–41, 자연 순위 0/예정16, 반환수 미확인 | 서로 다른 배정 과제지/검수 요건이면 ST06 동등성 철회. 플랫폼 혼입 ST10 제외. 정식 순위를 확보할 때만 대표성 검토 |
| Q2 제공 스택 호출·파생 수정·직접 구현 구별 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) App D, §5.4; [S01](https://eprints.cs.vt.edu/archive/00000294/01/TR-92-14.pdf) §§2–4; [S05](https://le-an.gitlab.io/publications/library_reuse.pdf) figs2–3 | ST06 24 저자보고, ST01 21명·42 과제관측 풀링, ST05 코드 사례 | 실제 제출 코드가 지시와 다르거나 양팔 공통 기반이면 처치 재분류. 권장만으로 실제 채택 주장하지 않음 |
| Q3 노동의 물리 단위 미확인 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) p78 표5.3 Hours, App E p169, App G p173; [S25](https://link.springer.com/article/10.1007/s10664-023-10408-6) RQ3 | R1–24, C02/03; C19 12 projects | G.1 단위가 원기록과 일치한다는 증거 또는 정정 필요. 기계시간, churn, 팀 경과와 합산 금지 |
| Q4 동일 품질은 저자 확인 수준, 탈락·재작업 독립검증 미확인 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) §5.4/G.1; [S04](https://link.springer.com/article/10.1186/2195-1721-1-4) §5.2.5–5.3.3; [S18](https://link.springer.com/article/10.1186/s13104-024-06749-0) 평가자료 | ST06 24/24 저자 보고, ST04 배정16·사전제외1, ST18 14/19 평가, 5 미평가 | 개별 채점 및 배정 원장에 실패/중단 발견하면 분모·판정 변경; 완료자만 효과 일반화 금지 |
| Q5 원척도 차이 +33.125, −17.5, 엄격 인시 미확인 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) G.1 p173, 표5.3–5.5; [S07](https://users.uowm.gr/sbibi/download/C24.pdf) 표III | C02/C03, 공유 A 8명+B8+C8; C06 1실측 팔. 전체 C01–20 | 단위/역할/관측창이 달랐거나 기록 누락 발견 시 차이 철회. 양쪽 실제 원장 전까지 S07 59h 견적을 실측으로 바꾸지 않음 |
| Q6 단계 제거와 이동·신규 노동, 조건부 역전 | [S06](https://vtechworks.lib.vt.edu/server/api/core/bitstreams/dc01f3c9-a892-4b64-b213-d8785198755b/content) G.1; [S19](https://www.cs.otago.ac.nz/cosc345/resources/COCOMO-II-2000.pdf) §2.4.2 eq4/Table5–6; [S29](https://www.nature.com/articles/s41598-024-74643-7) 현장 관찰 | C02/03, R1–24, S19 모델, C20 관찰20개 회사 | 동일 척도 B−A 추가 순노동 >33.125면 B 이점 역전; C−A 기존 표본 불리 방향은 A−C 누락 >17.5면 역전. 원척도 확정 전 시간 단위 아님. |
| Q7 타 분야 동일 품질의 노동 비교 미확인 | [S11](https://www.jmir.org/2015/11/e247) 표3; [S17](https://onlinelibrary.wiley.com/doi/full/10.1002/icd.70007) §4 표1; [S14](https://www.mdpi.com/2220-9964/10/1/10) 비교 결과표; [S20](https://www.mdpi.com/2079-9292/15/7/1373) 기하/텍스처 결과 | C09 30/30, C15/16 2 녹음, C14 데이터셋, C18 1원물; C17 19/14 | 오류·검수·실패 복구 및 공통 품질 합격을 만족하는 인시 쌍이 발견되면 해당 단계만 판정 상향. 표40/본문42 차이 보존. |

## 재계산
원격 lattanzi-raw.csv를 JS로 읽어 네 단계 합과 printed_total 및 computed_total 비교: 24/24 일치. 집단별 합과 평균:
| 군 | n | 설계 합 | 라이브러리 합 | 코드 합 | 디버그 합 | 총합 | 평균 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 8 | 133 | 0 | 312 | 340 | 785 | 98.125 |
| B | 8 | 115 | 82 | 156 | 167 | 520 | 65 |
| C | 8 | 149 | 146 | 278 | 352 | 925 | 115.625 |

단위 미확정 원척도. A−B=33.125, A−C=−17.5. 독립 비교 2건으로 세지 않음. 인쇄된 반올림 평균과 일치. 저자 Tukey cutoff 32.45, AB 33.13, AC 17.50: C 평균이 더 커도 A/C 유의차로 쓰지 않음. 원자료 프로그램 실행/재통계 및 독립 연구 복제는 미실시.

## 가장 강한 경쟁 설명
재사용 절감이 아니라 과제·부품 적합성, 배우는 비용과 검수/수정 방식의 차이가 관측을 만든다. 실제 반례 C03의 수정 상속군은 동일 과제에서 직접군보다 큰 평균이며 라이브러리 활동 합146, 디버그352로 A의 0,340보다 큼. 단순 재사용 여부로 모든 경우 방향 예측 불가; 유의한 손해도 단정 안 함. S04 P16 역방향은 기존 프레임워크 내 도구 선택이며, S07 Dialog 견적60/실측180은 기대와 실제의 차이이지 실제 양팔 반례가 아니다. S20 기하와 텍스처 우위가 달라 시간만 비교 불가. 이 때문에 일반적 비용 절감/손해 부호, 인시 차이, 모집 빈도 모두 미확인.

## 산입·기록 자기검산
sources.jsonl 38열람 행, 실질 원문 구간 21고유(교정 S02 제외 20), 12/22 범주 충족 후보: 5/8 비교,1/5 별도 저자자료,2/5 후속/비용,2/2 전사 보고서,2/2 디지털화 보고서. 나머지 10(3+4+3), Q7 엄격 동등조건도 추가 검증 필요. S06b/c 중복 제외; S16/S28 자료 랜딩, S03/S13 초록·차단, F* 서지/색인 미산입. 원문 확인 UTC 날짜까지만. 정식 원순위 미복원, 자연 표본 분모 불명, 보충층의 원 검색 결과 순위도 미확보. 18 study rows 및 20 contrast rows를 연구 수와 혼동하지 않음. 동일 저자/관측계보 분리, SEL/OSUL 재산입 없음. PARTIAL 유지. 제품 실행·독립 리뷰 없음.
