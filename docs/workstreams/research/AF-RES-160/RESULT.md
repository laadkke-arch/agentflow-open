# AF-RES-160 — 노동 원장과 기존 부품 선택의 비용 문장 (PARTIAL)

## 표 1. 프로젝트·사건·모집층과 납품 연결
단위: 사건/원문/인시. 예정 A·B 각 최초 12, 연결 2 미만 시 추가 12(최대 48 후보); 실제 순서가 확정된 후보 **0**, 반환 분모 미확인(검색 실패, 관측된 0건 아님). 보조 프레임 A 10(외부 프로젝트 포함), B 16, 조회실패 행 10. SEL 단계 집계 프로젝트 10 + 별도 이식 실험 1; 독립 승인 원문까지 연결된 실제 납품 0. GitLab 실제 시간 0건 확인(값이 0이라는 의미 아님). 기록관·교통은 별도 보조층 각 2 사례. 결과는 비확률 탐색이다.

| 프로젝트·사건·모집층 | 납품 목표·부품과 대안 | 원장 주소·기록 주체 | 시간 단위·실측/견적 | 실제 납품 증거 | 결측 |
|---|---|---|---|---|---|
| G1 GitLab A 보조 | CycloneDX 보고서로 교체; 옛 dependency_files artifact 선언 제거 | [S01](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/150540) sidebar; [S21](https://gitlab.com/gitlab-org/gitlab/-/issues/439782) [S22](https://gitlab.com/gitlab-org/gitlab/-/issues/396376) 결정; 기여자 | spent/estimate 미확인, F12 API 실패 | MR 설명·후속 이슈(옛 CI 템플릿 제거 누락); 17.0 목표는 실제 발행 아님 | timelog, merge SHA, release/90일 |
| G2 GitLab A 보조 | 죽은 의존성 목록 경고 제거; 실패 pipeline 데이터 수집 유지 | [S02](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/161512) sidebar, F13 | 미확인 | MR 설명 | 부품 선택에 해당하는지, merge/release/시간 |
| G3 GitLab A 보조 | 쓰는 Bootstrap JS vendoring, GitLab UI SCSS 소비; 외부 dependency 유지 가능 | [S03](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/168783) [S23](https://gitlab.com/gitlab-org/gitlab-ui/-/merge_requests/4333) upstream; F14 | 미확인 | MR 및 upstream import 안내 | 배포·검토·이관·지원 인시 |
| GROSS/GRODY B 보조 | 동일 초기 명세, 운영 FORTRAN vs 실험 Ada(다른 UI/범위/교육/인수) | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5, T2-7; [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) pp.65,68–70; [S31](https://ntrs.nasa.gov/api/citations/19910006459/downloads/19910006459.pdf?attachment=true) | 인시 A; GRODY 별도 22,863h incl 교육(3,346h); 계획 30,800h E | 운영/실험 보고 [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) pp.9–14 | 실제 인수·동등 기능·원카드 |
| GOADA/GOFOR B 보조 | UI 재사용 Ada 운영화 vs FORTRAN 경로 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-1/5/7; SEL | 인시 A, 단계표 아래 | GOADA 통합 문제·지연 보고 [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) | 비교 목표·팀·납품 날짜 |
| GOESIM B 보조 | 늦은 Ada 채택, FORTRAN 설계 유지 및 인터페이스 구현 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5/7; SEL | 인시 A | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 개발사례 | 원래 자체/유지안 인시 |
| UARSTELS/EUVETELS B 보조 | 전자: 부적합 부품 대신 generic 작성; 후자: 공유 소스 소비 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5/7; SEL | 인시 A | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 병행 라이브러리 변경 설명 | 생산자/소비자 귀속, 동등 납품 |
| EUVEDSIM B 보조 | 설계 개선 대신 재사용 극대화 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5/7; SEL | 실제 17,805h; 20,775h/121주 모델 보정 G | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 필요 소멸/정식 인수 없음 | 실제 인수 노동·비교안 |
| SAMPEXTS B 보조 | 안정된 소스·기존 문서·검토 통합 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5/7; SEL | 실제 2,038h(3단계 인쇄 총계); 자체 구현 추정은 E/G | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 시험 오류와 납품 경과 보고 | 독립 인수·동일 비교·90일 |
| POWITS B 보조 | 다른 자세제어 계열 구조 재사용; 경험 부족 | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5/7; SEL | 실제 11,677h | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 7개월 지연·성능 미달 | 같은 품질/기능의 유지·자체안 |
| TOMSTELS/FASTELS B 보조 | 자세제어 방식에 맞춘 선택·prototype/benchmark | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section 2, SEL | 총계 A 3,839/6,039h; 단계 미확인 | 일정에 맞춰 운영계통 공급했다는 저자 보고 | 정확한 배포·비교 원장 |
| GOESIM-REHOST B 보조 | 작동하던 Ada 시뮬레이터 VAX→NAS, 누락 math routines 구현, I/O 교체 | [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) pp.3-5–7 T3-1, rehost team | 1,061.9 staff-hours A; FORTRAN 198–220 staff-days E | 이식 실험 및 시험, 입력 파일 4/5 성공 보고 | 실제 운영 인수/성능·대안·지원 |
| AC Transit, Foothill Q7 | 제조사→운영 정비 및 전기버스/CNG 다른 차량군 | [S15](https://docs.nlr.gov/docs/fy17osti/68413.pdf) [S16](https://docs.nlr.gov/docs/fy21osti/80022.pdf) 작업지시 집계 | labor-hours A/E 분리 | 현장 운영 보고 | 동일 작업/차량·기간·정비 주체 |
| OSUL, FAC Q7 | 기록물 촬영 배치 변경/자동 메타데이터와 수동 보완 | [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) pp.81–82; [S19](https://www.randtke.com/portfolio/2013_Randtke_preprintFor_64SerialsLibr267.pdf) 비용분석 | staff-hours A, 실제 부분작업 | 기록관/프로젝트 작성자 보고 | 산출물 질/건수·제외 단계·동일 대안 |

## 표 2. 비용 차이의 허용 범위
단위: person-hours/staff-hours/staff-days(서로 자동 환산하지 않음). 계획 비교 가능한 모든 적격 대조; 실제 대조 후보 12, 동등 소프트웨어 0, 기술 집계 10 프로젝트와 이식 1건, 부분 기술통계 1(기록관). 원장 행 166, 실제 관측·견적·합계·대체 집계·미확인 혼재. 아래 총계는 인쇄값, 행 합계 차이는 SELF_CHECK에 공개한다.

| 사건·단계·역할 | 도입안 시간·위치 | 비교안 시간·위치 | 기간·품질·중복·누락 | 계산 가능한 차이와 단위 | 귀속 한계 |
|---|---|---|---|---|---|
| C1 GRODY/GROSS 기술·관리 | 19,133h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) | 15,165h 동표 | 실험/운영, 기능·교육·인수 불일치; [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) p.65 | 미확인 | 병행 구현이어도 matched 아님 |
| C2 GOADA/GOFOR | 28,056h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-1 | 12,804h 동표 | 기간·팀·목표 상이 가능 | 미확인 | UI 재사용 인과 불명 |
| C3 EUVETELS/UARSTELS | 4,235h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5 | 11,167h 동표 | 소비/생산 프로젝트 다름 | 미확인 | 라이브러리 생산 비용 이동 |
| C4 SAMPEXTS/EUVETELS | 2,038h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5 | 4,235h 동표 | 다른 임무·안정/동시변경 라이브러리·프로세스 | 미확인 | 20% 자체구현은 추정 |
| C5 POWITS/SAMPEXTS | 11,677h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5 | 2,038h 동표 | 다른 자세제어, 경험/성능 기준 상이 | 미확인 | 지연/성능 미달은 반례, 차액은 절감 아님 |
| C6 EUVEDSIM 시험 | 4,701h [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5 | 6,679h rev 보정 | 생략된 인수시험 가정 | 미확인 | 보정 차액은 실제 투입 아님 |
| C7 GitLab G1–3 | 미확인 F12–14 | 미확인 | merge/release, time_stats 차단 | 미확인 | access failure ≠ 0 |
| C8 AC Transit 정비/훈련 | 23 labor-hours [S15](https://docs.nlr.gov/docs/fy17osti/68413.pdf) | minor 3 / major 8h 견적 | PM 종류·여러 직원 교육 | 미확인 | 청구/실제/표준 구분 |
| C9 Foothill BEB35FC/CNG | 8,127.5 labor-hours [S16](https://docs.nlr.gov/docs/fy21osti/80022.pdf) | 8,212.1 labor-hours 동표 | 12/8대, 주행·기간·보증 다름 | 미확인 | 총계 차이의 인과 비교 금지 |
| C10 OSUL 촬영·편집 | 13h/10점 [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) | 69h/40점 동보고, 17.25h/10점 환산 | 서로 다른 작업물 조합, clock vs calendar, 보존·설치 제외 | 69/40×10−13=4.25h/10점 **기술통계만** | 품질·추가 작업 동등 아님; 순절감 아님 |
| C11 FAC 메타데이터 | 70h 자동 [S19](https://www.randtke.com/portfolio/2013_Randtke_preprintFor_64SerialsLibr267.pdf) | 128.25h 수동 | 별개 보완 필드; audit 공통 | 미확인 | 자동/수동 전체 대안 아님 |
| C12 GOESIM-REHOST | 125 staff-days A 보고서 제외 [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) T4-1 | 198–220 staff-days E | 유사 시스템 FORTRAN 저자 추정; 환경/성능 대조 없음 | 미확인 | 실측 vs 추정 |

## 표 3. 조건별 비용 문장 및 남겨야 할 선택지
단위: 작업 종류/관측 범위/인시(있을 때만). 예정 실제 소프트웨어 사건 2 이상(비용 문장), 실제 기술집계+당사자 납품 보고에서 4개 사례 문장, 독립 원장·납품 결합 0, matched 순절감 0. 비용으로 결정할 수 없는 대안과 반대 조건을 보존한다.

| 설계자가 고를 조건 | 줄어든 작업·새 후속 작업 | 확인한 기간·반례 | 원문 링크와 쓸 수 있는 비용 문장 | 순절감·미확인 | 다음 최소 확인 |
|---|---|---|---|---|---|
| SAMPEXTS: 안정된 기존 소스·같은 문제 계열이면 채택, 아니면 독립 작은 구현/부분 재사용 | 문서/검토 일부 통합; 적합성 검증·통합·시험은 잔존 | 프로젝트 월 경계는 deliveries; POWITS 반례 | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section 2 + [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) T2-5: 해당 프로젝트 설계·코드·시험 2,038h 인쇄 총계(팀 전체 아님) | 자체 구현/유지 실제 노동 미확인 | 동일 시험·인수조건 비교와 상류 생산원장 |
| POWITS: 자세제어 계열이 다르면 맞는 라이브러리/검증된 prototype vs 필요한 부분 직접 구현 | 부적합한 구조 수정·학습, 성능/통합 시험 증가 가능 | 지연 7개월, 성능 미달 보고, 첫 발행+90일 미확인 | [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf): 채택 경로에 11,677h 기록, 성능 조건 못 맞춤. 더 싼 대안이라는 주장은 불가 | 미확인 | 실제 대체 경로와 인수 기준, 적합성 검토 노동 |
| GOESIM-REHOST: 이식성 검증 가능한 부품 vs 유지/재구현 | 기존 계산 로직 활용; 누락 수학함수, 입출력, compiler 수정과 시험 필요 | 1989–90 실험 10개월; 4/5 입력파일 테스트 | [S30](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf) T3-1: 이식 준비·컴파일·링크·실행·시험·보고 1,061.9 staff-hours, 405.7 컴파일, 307.9 시험; FORTRAN 추정은 비교 실측 아님 | 미확인 | 실제 FORTRAN 이식/원래 환경 유지 및 같은 입력·성능·지원 |
| GitLab G1/G3: 기존 보고서·패키지 소비 vs 새 제공자/내부 vendoring | 기존 artifact 선언 제거·dependency 제거; CI/하류 소비자·import 변경 | 2024 MR 설명; 누락된 템플릿 후속 수정·upstream 주의 | [S01](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/150540) [S21](https://gitlab.com/gitlab-org/gitlab/-/issues/439782) [S22](https://gitlab.com/gitlab-org/gitlab/-/issues/396376) [S03](https://gitlab.com/gitlab-org/gitlab/-/merge_requests/168783) [S23](https://gitlab.com/gitlab-org/gitlab-ui/-/merge_requests/4333): 명시된 작업이 없어지거나 옮겨짐; 인시 불명 | 비용으로 고를 수 없음 | public time_stats/timelogs, merge/release 및 첫 90일 |
| 기록관·정비의 비교 조건 | 배치작업·자동 메타데이터; 별도 audit/교육/보증 비용 | OSUL 부분률, FAC audit, AC 정비훈련 | [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) [S19](https://www.randtke.com/portfolio/2013_Randtke_preprintFor_64SerialsLibr267.pdf) [S15](https://docs.nlr.gov/docs/fy17osti/68413.pdf): 같은 단위라도 범위 및 작업 주체가 다르면 순절감 보류 | 4.25h/10점은 기술통계; 나머지 미확인 | 양쪽 작업 지시·검수·교육·후속 작업의 동일 창 |

## Q별 해석

### Q1. 시간 정의와 모집
SCOPE ①의 정렬/분모 규칙을 유지했다. A: GitLab issue/MR 검색 6개 API가 DisabledError(F1–F6), 프로젝트 색인 F7 실패, 전역 F8 로그인 화면. 3개 공개 MR 설명은 열렸으나 시간 부분 Loading, time_stats F12–F14 실패. 비공개인지, 단순 도구 접근 실패인지까지 단정하지 않는다. 공식 2023–25 문서 버전 [S26](https://github.com/gitlabhq/gitlabhq/blob/v16.5.0/doc/user/project/time_tracking.md) [S27](https://github.com/gitlabhq/gitlabhq/blob/v17.0.0/doc/user/project/time_tracking.md) [S28](https://github.com/gitlabhq/gitlabhq/blob/v18.0.0/doc/user/project/time_tracking.md)의 spent/estimate/negative/delete/100-entry 제한을 직접 확인했다. estimate는 덮어쓰기, spent는 누적, 0 미만 차감은 무시, 삭제 허용, d/w/mo는 제품 내 8/40/160h 규약이다. 17.0 미지정 날짜 기본 현재; 18.0 역할 변경. 원장 응답의 기본0과 명시적 기록0은 별개다. B: NTRS 검색/GET 접근 실패(F9–10). 외부 검색으로 보고서 직접 열람했으나 처음 12·다음 12를 주장하지 않는다. 보조 B 16 후보 중 방법/동저작/미열람/원본 프로젝트 미위치 모두 frame에 보존. 엄격 모집 미달 PARTIAL.

### Q2. 실제 대안과 목표
[S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) section 2의 프로젝트별 설명에서 기존 FORTRAN 경로, Ada 전환, 이전 라이브러리 재사용, generic 직접 작성, 목표에 맞춘 선택을 구분했다. GROSS/GRODY는 병행 구현이지만 초기 명세가 같다는 사실만으로 실제 목표가 같지 않다: [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) p.65, [S31](https://ntrs.nasa.gov/api/citations/19910006459/downloads/19910006459.pdf?attachment=true) 실험 결과. UARSTELS는 적합하지 않은 GOESIM 부품을 대부분 쓰지 않고 새 generic을 만든 선택, EUVETELS는 그 소스를 병행 소비. SAMPEXTS는 안정된 소스 활용과 검토 통합. POWITS는 부적합한 자세제어 아키텍처와 경험 문제. TOMSTELS/FASTELS는 선택적으로 사용. 자체 작성에 드는 20% 등 저자 추정은 실제 대안 I가 아니라 E/G. S30은 이식 실제와 FORTRAN 추정 비교. G2는 alert 삭제이며 부품 채택의 직접 사례에서 제외. G1/G3는 명시된 의존관계 변경으로만 사용.

### Q3. 시간의 의미와 귀속
SEL [S05](https://ntrs.nasa.gov/api/citations/19820016122/downloads/19820016122.pdf) [S08](https://ntrs.nasa.gov/api/citations/19930006390/downloads/19930006390.pdf?attachment=true) weekly project effort/지원/유지 양식 및 종료 요약, 인시와 CPU 구별. [S29](https://ntrs.nasa.gov/api/citations/19900012222/downloads/19900012222.pdf) p.65 weekly phase vs component activity는 별도 기록폼이고 합계가 반드시 동일하지 않다. S09 p.2-8 T2-5는 생애주기 설계/코드/시험 단계, p.2-10 T2-7은 작업 종류 설계/코드/시험/기타. 두 표의 값은 같은 기간의 대체 분해, 합산 금지. p.2-7 T2-4 지원 직원은 별도 집계; 배포 후 지원과 동일하지 않다. S29 p.68 실제 교육 3,346h는 일부 요구사항 다시 작성이 포함될 수 있다. 표의 수치를 재분류하거나 반올림 차이를 임의 배분하지 않는다. 기록자 집계와 실제 근무 기록 원카드의 차이는 미확인. 근무월을 일률적으로 160h로 환산하지 않는다(SEL S29 계획 환산은 22일×8h=176h, GitLab 규약과 다름).

### Q4. 산출물 연결
S09/S10 프로젝트 코드는 집계와 납품 서술을 연결한다. 독립 커밋/승인서/발행물은 미열람. 운영/실험 구분과 실제 수락 여부는 저자 보고 범위까지만. EUVEDSIM 인수시험 없음 및 모델 보정(별도 SCOPE_CORRECTION). S30은 표 3-1의 이식 단계 인시와 시험 실험 보고를 직접 연결하지만 production 승인 아님. GitLab 이슈와 MR 연결은 가능한 범위에서 G1/G3의 원인 및 소비자 수정 작업을 특정한다. 실제 commit→release 미확인. 최초 배포 정확한 날짜를 개발 종료 월이나 목표판으로 대체하지 않는다.

### Q5. 대조와 검산
아래는 같은 인쇄 원장 내부의 단계 분해이지 대안 차액이 아니다. 단위 person-hours, 설계/코드/시험/인쇄총계. S09 T2-5. 10개 실제 프로젝트 집계; 원카드 0, 독립 matched pair 0.

| 사건 | 단계 3개/총계 | 위치 | 제한 |
|---|---|---|---|
| GROSS · B 보조 | 3679 / 5397 / 6089 / **15165** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; GROSS-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| GRODY · B 보조 | 2987 / 11174 / 4972 / **19133** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; GRODY-phase-* | 실험판/운영 인수 불동등 |
| GOADA · B 보조 | 7170 / 10815 / 7901 / **25886** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; GOADA-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| GOFOR · B 보조 | 1898 / 3853 / 6482 / **12233** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; GOFOR-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| GOESIM · B 보조 | 3712 / 5763 / 3565 / **13039** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; GOESIM-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| UARSTELS · B 보조 | 2751 / 4402 / 4014 / **11167** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; UARSTELS-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| EUVETELS · B 보조 | 1107 / 1718 / 1411 / **4235** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; EUVETELS-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| EUVEDSIM · B 보조 | 4258 / 8846 / 4701 / **17805** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; EUVEDSIM-phase-* | 인수시험 없음; 보정치 제외 |
| SAMPEXTS · B 보조 | 981 / 368 / 690 / **2038** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; SAMPEXTS-phase-* | 기술·기술관리 집계; 원카드/정확한 납품일 없음 |
| POWITS · B 보조 | 1588 / 5493 / 4597 / **11677** | [S09](https://ntrs.nasa.gov/api/citations/19940030750/downloads/19940030750.pdf) p.2-8 T2-5; POWITS-phase-* | 성능 미충족/지연; 품질 불동등 |

S30 별도 이식 1,061.9h. 단계별 124.7+405.7+15.7+142.4+307.9+65.5=1,061.9; 활동별 65.5+251.8+180+93.5+96.6+374.5=1,061.9. 같은 노동의 분해이므로 더하지 않는다. S30 T4-1 actual 125 staff-days excluding report vs estimated 198–220, 절감량/비율 금지. S29 p.68 22,863h(7 항목 합 동일), estimate 30,800h는 예상 대비 실제일 뿐 독립 대안 아님. C1–12의 첫 탈락 조건을 comparisons.csv에 남겼다. C10만 부분 단위율 산술을 허용했으며 품질·시간기록법이 달라 효과 추정은 하지 않는다.

### Q6. 후속 비용과 역전
소프트웨어 16 deliveries 행 모두 정확한 첫 release와 90일/완결 3개월 원장 미관측. 0건 확인 사례 없음. 개발 중 추가 작업과 배포 후 업무 구분: GOADA 통합/성능, POWITS 지연·요구 미충족, GOESIM 이식 compiler/math/I/O, UARSTELS 부적합 후보 기각, GitLab G1 후속 CI 누락 및 G3 upstream 교체 안내. SEL [S10](https://ntrs.nasa.gov/api/citations/19950022386/downloads/19950022386.pdf) 교육 사례 EMS practice 1,336 staff-hours, 영상/세미나 40/24h는 코스 길이, 사람 수를 곱할 자료 없음. 교육 반복에 대한 일반 위험을 뒷받침하나 90일 반복 실제 인시 미확인. 자동 이관이 잘못된 수정을 생성한 소프트웨어 원장 사례, 실제로 유지가 더 저렴한 동등 품질 비교는 미확인. 이 미달을 문서의 계획 문장으로 대체하지 않는다. 
D_partial=H_old,matched−H_new,matched; D_net=D_partial−(H_new,missing−H_old,missing). 미측정 순증가가 양의 D_partial을 초과하면 역전. 이번 소프트웨어에는 수치 D_partial 자체 없음. C10 4.25h/10점의 경우, 동등한 10점과 품질이라는 가정 아래 다른 단계 순증가가 4.25h를 넘으면 부분률 우세가 사라짐; 보존 담당 4h를 곧바로 순증가로 대입하지 않는다(옛 보존 시간 결측).

### Q7. 분야 전이(방법만)
- AC Transit [S15](https://docs.nlr.gov/docs/fy17osti/68413.pdf) 정비 직원 훈련으로 한 PM의 기록 23 mechanic-hours, 통상 minor 3h/major 8h는 견적; 작업 종류 미확인. 한 차량의 운영 중단과 참여 정비사 합계가 다르고, 제조사 지원/교육과 기관 자체 노동도 다르다.
- Foothill [S16](https://docs.nlr.gov/docs/fy21osti/80022.pdf) pp.28–29, 정비 작업지시에서 차량군별 8,127.5/1,029.5/8,212.1 labor-hours. 차량 수 12/2/8 및 주행거리·기간·보증범위 다름. 보고서 $50/h는 비용 산출 가정이지 실제 지급 임금이 아니다. [S17](https://docs.nlr.gov/docs/fy11osti/49342-1.pdf) p.13 수집계획은 maintenance, downtime, warranties, payer 분리를 요구한다. 서로 다른 기관 요율을 이식하지 않는다.
- OSUL [S18](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/archiving/15/1/art00017) 40점 69h vs 10점 13h 촬영/편집; 기존은 calendar 조정, pilot clock-in/out. 설치 제외, 보존 담당 별도 4h, 유리/반사/품질 및 작업물 선택 차이. 카메라 교체 보류 조건도 기록. 단위당 부분률은 총 노동이 아니다.
- FAC [S19](https://www.randtke.com/portfolio/2013_Randtke_preprintFor_64SerialsLibr267.pdf) 50h DB+35h digitization+70h 자동 metadata+128.25h 수동+342.75h audit=626h(표 범위의 작업합계, 다른 작업 전체 여부 불명). audit가 이 다섯 작업합계에서 342.75/626≈54.8%. 자동·수동은 보완 필드, 완전대안 아님. [S20](https://wiki.diglib.org/Data_Collection_and_Contribution,_Digitization_Cost_Calculator)는 수집 방법과 제외 overhead의 공개 필요를 보강한다.

### Q8. 탐색기 전달 규칙
비용 문장의 허용 수준을 세 가지로 유지: (1) 원문이 말하는 제거/이동 작업, 시간 미확인; (2) 관측 단계·단위·창·품질·비교 상대가 맞은 경우만 차이, 아니면 기술통계; (3) 전체 순절감은 모든 관련 노동 범위 맞기 전 미확인. 표3의 SAMPEXTS/POWITS/REHOST/G1·G3는 서로 조건이 다른 선택지다. 재사용률, 코드 크기, 프로젝트 달력 경과, 예산, 런타임, 모델 추정을 인시로 변환하지 않는다. 비용으로 고를 수 없을 때 기능·품질·호환성으로 선택할 수 있지만 비용 랭킹은 비워 둔다.

## 추가 분석 및 증거 하한
- sources.jsonl 58행, counted 22 고유 work_id. 중복 원장 재인용을 별도 시간으로 세지 않음. 22는 전체 원문 하한(서로 다른 결정·규약·사례 포함)이지 소프트웨어 원장 22개가 아니다. 독립 소프트웨어 원장 요건 6: S09/S10 공동 SEL 프로젝트군 1계보 + S30 별도 이식 1계보(원보고서 3개, 독립 관측 묶음 보수적으로 2), **미달**. 결정/변경 기록 S01–03/S07/S21–23(7 저작) 중 실제 납품/후속까지 독립 입증한 6개는 미달. 방법 S05/S08/S12/S13/S14/S17/S20(7, 4 이상); 교통 S15/16, 기록관 S18/19(각 2). 정확한 열람 UTC는 일자까지만 보존.
- frame의 순서 고정 실패와 10개 실패 조회를 음성 관측으로 분류하지 않음. 원장 접근 실패, 범위 밖/형식중복 및 미열람을 분리. 추가 자료의 후보 행은 frame-extra.csv에 보존. 원판 ①과 ④ 유지, 이후 데이터 보정만 별도 커밋.
- 독립 검토자 없음. 커넥터로 원격 파일을 다시 읽고 구조/합계를 자체 검산. 실제 원자료/CLI 실행이나 CI를 했다고 주장하지 않는다. 최종 상태 PARTIAL.
| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |
|---|---|---|---|
| GitLab 6개 검색 API와 원장/색인 접근 실패; NTRS 원순서 미확인 | 모집 대표성, 0시간/기본값의 빈도, 12+12 모집 완료 불가 | 허용된 공개 API/브라우저에서 6+4 질의를 페이지 끝까지 재현, ID/생성일/보고서번호 및 상태 저장 | 원장 접근 및 정렬된 최초 12/추가12의 실제 기록·명시0·기본0·접근불가 분모 |
| SEL 보고서 10개 프로젝트의 단계집계와 별도 이식 1건은 있지만 원카드·동등 인수시험·정확한 배포일 부족; 독립 원장 6개 미달 | 독립 검증된 납품 사건 2건, 맞춘 대안의 순절감 부호 모두 미확인 | FDD-552-91/007, FDD/552-90/045 등 개발 이력·승인 산출물, 실제 대안 팀의 동일 기능·기간 기록 | 2개 사건의 인수증거 및 같은 목표/품질/기간/역할의 양쪽 비중복 인시 |
| 첫 배포+90일의 원장 미관측; 교육/지원·하류·보정의 귀속 불완전 | 팀 전체 순절감 및 후속 노동에 의한 역전 미확인 | 날짜 있는 release/maintenance WMEF 및 upstream/downstream 원장·정정 이력 | 양쪽 동일 관측창에서 지원 포함 총계와 역전 여부, 또는 단계 차이를 초과하는 추가 순노동 |
