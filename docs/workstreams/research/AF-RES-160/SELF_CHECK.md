# AF-RES-160 SELF_CHECK — 자체 검산 (독립 검토 아님)
검사 입력 고정: e27b55e6809be66231ab06055c4b9e065e36a1a2. 원격 connector fetch 응답을 JS로 파싱했다. 외부 API 원장/실행기 검사는 별개이며 미수행. UTF-8 원격 대표 파일 exact equality를 커밋마다 확인했다.

## 구조·분모 검사
| 파일 | 데이터행 | 열 | 열수 오류 | 빈 셀 | 중복 ID |
|---|---:|---:|---:|---:|---:|
| frame.csv | 28 | 11 | 0 | 0 | 0 |
| frame-extra.csv | 8 | 11 | 0 | 0 | 0 |
| time-entries.csv | 166 | 16 | 0 | 0 | 0 |
| deliveries.csv | 16 | 12 | 0 | 0 | 0 |
| comparisons.csv | 12 | 12 | 0 | 0 | 0 |
sources 58행 / ID 58 / counted 22 / counted work ID 22; 상태 {"success":28,"success text":3,"failure":19,"pending":8}. CSV source_id 역참조 누락 0: 없음; time-entry duplicate_key 중복 0. 중복 의미(서로 다른 분해)와 ID 중복은 구분한다. 후보 36행=10 실패 조회+26 보조(A10/B16), 순서가 검증된 정식 후보 0; 적격/탈락/공개 여부의 전체 분모 미확인. 실패 10은 모집 조회 단위, source failure는 별도 열람 단위. 빈칸 대신 미확인 및 사유. 12 비교 행에서 matched software 0, 기술통계 1. 미확인 비율 계산 없음.
원장 6개 요건 미달: S09/S10 동일 SEL 관측군과 S30 별도 이식; S29/S31 같은 프로젝트 제외. 결정/후속 7저작 후보 중 독립 배포 완결 6 미달. 방법 7, 교통/기록 각2. counted 원문 22를 시간 원장 개수로 확대하지 않는다. sources는 독립 논리 열람 단위로 묶었으며 동일 자료의 연속 화면 열기마다 별도 row가 아니고 정확한 시·분·초도 미기록. 이것은 요청 형식의 미달이다.

## 원장 값 검산
| 사건 | T2-7 4항 합 | 인쇄총계 | 차 | T2-5 3항 합 | 인쇄총계 | 차 |
|---|---:|---:|---:|---:|---:|---:|
| GROSS | 15164 | 15165 | -1 | 15165 | 15165 | 0 |
| GRODY | 19133 | 19133 | 0 | 19133 | 19133 | 0 |
| GOADA | 25886 | 25886 | 0 | 25886 | 25886 | 0 |
| GOFOR | 12233 | 12233 | 0 | 12233 | 12233 | 0 |
| GOESIM | 13040 | 13039 | 1 | 13040 | 13039 | 1 |
| UARSTELS | 11168 | 11167 | 1 | 11167 | 11167 | 0 |
| EUVETELS | 4237 | 4235 | 2 | 4236 | 4235 | 1 |
| EUVEDSIM | 17805 | 17805 | 0 | 17805 | 17805 | 0 |
| SAMPEXTS | 2039 | 2038 | 1 | 2039 | 2038 | 1 |
| POWITS | 11677 | 11677 | 0 | 11678 | 11677 | 1 |
1–2h 차는 반올림 가능성, 원카드 없으므로 확정 못함. 원본 수치 유지. T2-7 합산 include yes는 40행, 총계·대체 분해·지원은 no. 단순 ID 고유성으로 의미적 중복 없음을 보장하지 않는다. S29 p.65 weekly/component forms 차이 확인, S09 두 표 동일 기간 노동으로 별도 컷. S29 GRODY 1989 실제 7항 합 22863h, 인쇄 22,863h; T2-5 19,133h와 범위 차(교육/요구사항 등). S30 REHOST phase 합 1061.9h 및 activity 합 1061.9h, 각각 1,061.9h, 합산 금지. S09 support 10행은 별도 역할, 원자료/보정 여부 확인 전 프로젝트 전체 합산 금지. EUVEDSIM 20,775h/121주 G 보정, 원래 T2-5 17,805h 유지. 원장 원시 담당자별 합계 대조는 불가(원카드 없음). C10 69/40*10-13=4.25; FAC 50+35+70+128.25+342.75=626, audit 비중 54.75%; 두 값은 부분 통계이지 순절감 아님.

## Q ↔ 근거 ↔ 원장 양방향 대조
| Q | 결론·미확인 | 출처 URL·정확한 위치 | 원장/영수증 | 한계 및 반증 |
|---|---|---|---|---|
| Q1 | 정식 분모 미확인; 시간 규약만 확인 | [S12](https://docs.gitlab.com/user/project/time_tracking/) time tracking; [S26](https://github.com/gitlabhq/gitlabhq/blob/v16.5.0/doc/user/project/time_tracking.md) [S27](https://github.com/gitlabhq/gitlabhq/blob/v17.0.0/doc/user/project/time_tracking.md) [S28](https://github.com/gitlabhq/gitlabhq/blob/v18.0.0/doc/user/project/time_tracking.md) spent/estimate/delete; [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5 | F1–F10,F12–14; frame F-G/F-N; N6,N7,N15 | 정식 정렬/실제 원장 성공 시 변경 |
| Q2 | 실제 I와 E/G, R/C 분리 | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section 2 pp.9–14; [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) p.65; [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) T4-1; [S21](https://gitlab.com/gitlab-org/gitlab/-/issues/439782) [S22](https://gitlab.com/gitlab-org/gitlab/-/issues/396376) | deliveries G1/G3,GROSS…POWITS,GOESIM-REHOST; C1–6,C12 | 초기 명세 같아도 인수·기능 다름; 원결정/같은 기능 구현이 반증 |
| Q3 | 활동/단계/지원/교육/견적 분리 | [S05](https://ntrs.nasa.gov/api/citations/19820016122/downloads/19820016122.pdf) forms; [S08](https://ntrs.nasa.gov/api/citations/19930006390/downloads/19930006390.pdf?attachment=true) PRF/SPF/WMEF; [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) pp.65,68; [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-4/5/7 | *-ACTTOTAL,*-phase-*,*-SUPPORT,GRODY89-*,S10 EMS | 개별 원카드/정정/누락 없음 확인 불가 |
| Q4 | 프로젝트 코드→보고 납품, 독립 인수 0 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-1/5; [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section 2; [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) pp.3-5–7 | deliveries 16, REHOST-P-*; SCOPE_CORRECTION | 인수서/실제 release SHA/날짜 발견 시 승격 |
| Q5 | matched pair 0 | [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) p.65,68–70; [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) T4-1; [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) pp.81–82 | C1–12, 위 합계검사 | 양쪽 같은 기간·기능·검수·역할 확보 시 차이 계산 |
| Q6 | 90일 노동 미관측, 순절감 부호 미확인 | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section2/3; [S21](https://gitlab.com/gitlab-org/gitlab/-/issues/439782) implementation issue; [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) pp.4-2–3; [S08](https://ntrs.nasa.gov/api/citations/19930006390/downloads/19930006390.pdf?attachment=true) WMEF | all delivery followup fields, EMS, C5,C6,C12 | 지연/교육 pre-release와 post-release 분리; 실제 90일 ledger 필요 |
| Q7 | 타분야 범위/주체 규칙 | [S15](https://docs.nlr.gov/docs/fy17osti/68413.pdf) PM/maintenance transition; [S16](https://docs.nlr.gov/docs/fy21osti/80022.pdf) pp.28–29; [S17](https://docs.nlr.gov/docs/fy11osti/49342-1.pdf) p.13; [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) pp.81–82; [S19](https://www.randtke.com/portfolio/2013_Randtke_preprintFor_64SerialsLibr267.pdf) Cost Benefit Analysis | C8–11, AC/Foothill/OSUL/FAC rows | 실제/추정/청구/downtime, 작업물/차량 차이 |
| Q8 | 작업 제거/부분 실측/순절감 문장 분리 | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) SAMPEXTS/POWITS; [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) T3-1/4-1; [S01](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/150540) [S03](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/168783) MR description | RESULT 표3 ↔ deliveries/comparisons | 비용으로 최종 선택 불가; 양쪽 원장 확보 시 변경 |

반례를 실제로 찾은 곳: S29 p.65 동일 초기 명세 병행 실험이 다른 기능/인수/교육을 가짐; S10 POWITS 부적합 아키텍처와 성능 미달, EUVEDSIM 인수 생략; S30 4-2/4-3 언어 표준에도 compiler/입출력·math 노동과 추정 비교; S15 교육 PM; S18 다른 작업물 그룹; S19 audit. 반증할 자료는 동일 범위의 양쪽 실측 및 납품 후 원장. 자동 이관 잘못된 수정 및 유지가 실제로 더 저렴한 matched 사례는 찾지 못함. 미관측이지 부재가 입증된 것 아님. ④ 보정은 별도 e27b55e...; 원판 보존. 독립 검토 없음, 원격 구조·산술 검사만 수행.
