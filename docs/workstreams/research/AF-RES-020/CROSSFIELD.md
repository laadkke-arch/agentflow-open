# AF-RES-020 — 다른 분야의 대안 보존과 조립 방법

## 1. 확인 범위와 핵심 답

**대안을 보존한다는 것은 모든 대안을 계속 개발한다는 뜻이 아니다.** 이 비교가 제안하는 것은 버린 대안의 근거를 복원할 수 있게 남기고, 현재 돈과 시간을 쓰는 대안의 수에는 조건과 종료 시점을 붙이는 방식이다. 또한 독립적으로 판단 가능한 연구 묶음과 독립적으로 실행 가능한 제품 모듈을 구분해야 한다. 이 구분을 하지 않으면 짧은 파일을 만든 것만으로 교체 가능성을 얻었다고 오인한다. [X01](https://www.gapimprove.org/_files/ugd/cd8b34_2d04bd540ca04019986c3ba54ae8631e.pdf?index=true), [X05](https://homepages.cwi.nl/~storm/teaching/reader/BaldwinClark06.pdf), [X11](https://kmi.open.ac.uk/publications/pdf/kmi-97-5.pdf), [X18](https://web.mit.edu/ariely/www/MIT/Papers/doors.pdf)

직접 열어 읽은 외부 방법·비교 원문은 **24개**다. 연구 논문·저자 원문·공식 지침을 사용했다. 자동차 제조, 소프트웨어 설계, HCI, 공공 계획, 보건 근거 종합, 국제 개발·사회 정책, 행동 의사결정, 항공우주, 조직 운영의 관점을 비교했다. 정확한 URL·판·읽은 위치·확인 내용·한계는 [sources-external.json](evidence/sources-external.json), 접근 실패와 읽기 절차는 [external-readlog.md](evidence/external-readlog.md)에 있다. 직접 인용은 사용하지 않았다.

| 문헌 조건 | 본문 확인 ID | 개수 | 판정 |
| --- | --- | --- | --- |
| 대안 보존·set-based 설계 3개 이상 | X01, X02, X03; 보강 X22, X24 | 5 | 충족. X01·X02는 Toyota 계열, X03은 같은 예산의 병렬 설계 실험 |
| real options·모듈화 3개 이상 | X02, X04, X05, X06, X07, X21 | 6 | 충족 |
| QOC·IBIS·ADR 3개 이상 | X08, X09, X10, X11 | 4 | 충족 |
| EtD·living review·근거 격차 지도 4개 이상 | X12, X13, X14, X15, X16, X17 | 6 | 충족 |
| 대안 유지의 비용·실패 원보고 2개 이상 | X11, X18, X19; 모형 X02; 틀 부담 X16 | 5 | 충족. X11·X18·X19는 직접 연구 보고이며 X02의 모형과 구분 |
| 가역·비가역 결정의 구분 | X20, X23 | 2 | 2015·2016 원 주주 서한 |
| 같은 사이트 최대 3개 | ResearchGate X02·X06·X08; Amazon X20·X23을 CDN까지 같은 기관으로 묶음 | 최다 3 | 충족 |

문헌의 근거 수준은 모두 **D1(원문 읽기)**이다. 논문 안의 실험이 있다고 해서 이번 작업이 D3-run 또는 D4를 수행한 것은 아니다. 아래의 연구 묶음 적용안은 **H(분야 간 전이 가설)**이며, 제품 구조를 확정하지 않는다. 판정자는 GPT-6 Astra Pro의 내부 별도 작업자이며 외부 독립 검토 또는 사람의 판정이 아니다.

## 2. 방법별 대응표

기록 구조·관측 비용·한계는 원문 요약이다. 원문에 명시적 시간·종료 규칙이 없는 방법의 보존·축소 조건은 **H 전이**로 표시했다. 특히 X18·X19는 비용을 관측한 실험이며 여기 적은 중단 규칙은 연구자의 제안이다. ‘묶음에 반영’은 모두 H다. 최신 제품 성능이나 AF-RES 관측 수치의 근거로 외부 방법 문헌을 사용하지 않는다.

| 원문·분야 | 언제까지 대안을 열어 두나 | 무엇을 기록하나 | 언제 좁히나 | 유지 비용 | 묶음에 반영(H) | 전이 한계 |
| --- | --- | --- | --- | --- | --- | --- |
| [X01](https://www.gapimprove.org/_files/ugd/cd8b34_2d04bd540ca04019986c3ba54ae8631e.pdf?index=true) Sobek, Ward & Liker — Toyota’s Principles of Set-Based Concurrent Engineering / 제조·자동차 | 호환 가능한 집합을 유지할 동안 | 설계 범위·제약·불가능 영역·교집합 | 새 지식으로 불가능한 대안을 제거; 남은 집합 안에서 확정 | 병렬 개발과 조정·시제품 비용 | 묶음별 적용·실패 조건, 관계의 조건 필드 | Toyota의 관찰·방법 해석이다. 시제품 수나 최종 확정일을 다른 제품에 그대로 적용할 근거가 아니다. |
| [X02](https://www.researchgate.net/publication/3076866_Adapting_Real_Options_to_New_Product_Development_by_Modeling_the_Second_Toyota_Paradox) Ford & Sobek — Adapting Real Options to New Product Development by Modeling the Second Toyota Paradox / 제조·프로젝트 경제 | 학습 이득이 지연 비용을 상쇄할 동안 | 진행 단계·학습·결정 시점 가정 | 추가 학습 가치가 지연 비용보다 작아지는 때 | 지연과 중복 개발 | 보류 기한·재검토 신호·대안 유지 비용 | 시뮬레이션 조건부 결과이며 AF-RES의 금전 가치나 최적 시점을 측정하지 않았다. |
| [X03](https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-final.pdf) Dow et al. — Parallel Prototyping Leads to Better Design Results, More Divergence, and Increased Self-Efficacy / HCI·시각 설계 | 정해진 피드백 주기까지 | 대안별 시제품·동일 평가 기준·시간 | 비교 피드백 후 수정·축소 | 정교화에 쓸 시간을 병렬 탐색에 배분 | 같은 질문·예산에서 시작 구성 비교 | 초보 광고 설계 과제와 15일 온라인 평가에 한정된다. 첫 5일 이후 광고 노출 배분 변화가 있으며 장기 소프트웨어 설계로 일반화할 수 없다. |
| [X04](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) Parnas — On the Criteria To Be Used in Decomposing Systems into Modules / 소프트웨어 설계 | H: 변경 가능 결정을 인터페이스 뒤에 둘 동안 | 각 모듈의 숨길 결정·공개 계약 | H: 공개 계약으로 호환성 판단 가능할 때 | 인터페이스 설계·효율 손실 가능성 | 결정 하나·교체 경계 하나; 정의 계약은 공개 | 분해 기준의 논증·예시다. 모든 연구 주장 또는 데이터 의존을 감춰도 된다는 뜻은 아니다. |
| [X05](https://homepages.cwi.nl/~storm/teaching/reader/BaldwinClark06.pdf) Baldwin & Clark — Modularity in the Design of Complex Engineering Systems / 공학 설계·산업 조직 | 공유 규칙을 지키는 대체물을 유지할 동안 | 의존 행렬·공유 규칙·시험 | 대체물의 호환성과 순가치 확인 | 공유 규칙·실험·통합 시험 | 판단 독립과 실행 독립을 구분; 숨은 의존 등록 | 25배 가치 예시는 비용을 뺀 사고실험이다. 파일을 나누었다는 사실만으로 독립 채택 또는 성능 향상을 입증하지 않는다. |
| [X06](https://www.researchgate.net/publication/2366338_The_structure_and_value_of_modularity_in_software_design) Sullivan, Griswold, Cai & Hallen — The Structure and Value of Modularity in Software Design / 소프트웨어 경제 | 교체 가능성과 유의미한 불확실성이 있을 동안 | 변경 가정·실험 비용·모듈 의존 | 대체 가치와 계약을 확인한 뒤 | 추정 모형·독립성 가정 검증 | 수익 수치 대신 결정을 바꿀 증거를 기록 | 논문 자체가 수치 모형의 즉시 실무 적용을 권하지 않는다. AF-RES 묶음별 수익 점수를 만들어 내는 근거로 쓰지 않는다. |
| [X07](https://www.academia.edu/23867694/The_Option_Value_of_Modularity_in_Design_An_Example_from_Design_Rules_Volume_1_The_Power_of_Modularity) Baldwin & Clark — The Option Value of Modularity in Design: An Example from Design Rules / 설계 경제 | 기존 대안으로 돌아갈 권리가 실제 있을 동안 | 현행 기준·대체물·규칙 소유·비용 | 대체물의 개선이 전환 비용을 넘을 때 | 구조·실험·시험·거래 비용 | 구성별 복구 자료와 전환 비용을 필수화 | 책 전체를 읽은 기록이 아니다. 가치 분포 보존 등 모형 가정과 비용 제외 명제를 현실의 무조건 우월성으로 읽지 않는다. |
| [X08](https://www.researchgate.net/profile/Victoria_Bellotti/publication/233367028_Questions_Options_and_Criteria_Elements_of_Design_Space_Analysis/links/00b7d53211940ad48e000000/Questions-Options-and-Criteria-Elements-of-Design-Space-Analysis.pdf) MacLean, Young, Bellotti & Moran — Questions, Options, and Criteria: Elements of Design Space Analysis / 설계 논증·HCI | H: 주요 질문과 대안의 장단점이 드러날 때까지 | 질문·대안·기준·평가·의존 | H: 기준 간 절충과 후속 질문을 설명 가능할 때 | 구조화와 편집 노력 | 결정별 선택지·반증·근거 위치; 찬성 개수로 고르지 않음 | 관찰한 설계 발화 분류는 맥락에 의존한다. QOC는 연대기 기록 전체를 대체하지 않는다. |
| [X09](https://www.escholarship.org/content/qt5cj786v8/qt5cj786v8.pdf) Kunz & Rittel — Issues as Elements of Information Systems / 공공 계획·논증 | 쟁점이 해결·포기되거나 잠재 상태가 될 때까지 | 쟁점·사실 질문·입장·논거·상태·관계 | 증거·설득·정식 결정; 필요시 쟁점을 교체 | 논거 편집·관계 지도 유지 | 경험적 질문과 가치·정의 다툼 분리 | 스캔 OCR의 일부 글자 오류가 있어 짧은 용어·구조만 확인했다. 세 실험적 운영 사례는 통제된 효과 검증이 아니다. |
| [X10](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) Nygard — Documenting Architecture Decisions / 소프트웨어 아키텍처 | 결정 전에는 proposed, 변경 뒤에도 이력을 보존 | 맥락·결정·상태·좋고 나쁜 결과·대체 링크 | 중요 결정을 내릴 때 accepted 또는 superseded | 짧은 기록과 추적 유지 | 판정 규칙 버전·대체 이력·결정 상태를 분리 | ADR의 채택 상태는 연구 근거의 확실성이나 작업 완료를 뜻하지 않는다. 인과적 생산성 검증이 아니다. |
| [X11](https://kmi.open.ac.uk/publications/pdf/kmi-97-5.pdf) Buckingham Shum et al. — Graphical Argumentation and Design Cognition / HCI·협업 인지 | H: 아직 불명확한 설계 공간을 설명하는 동안 | 거친 탐색 메모와 정리된 논거를 연결 | H: 탐색이 끝나면 결정 기록으로 전환 | 기록 지연·기록자 소외·허수 대안 | 가벼운 결정에는 선택지 증식 대신 변경 근거 보존 | 세 질적 연구이며 모든 상황에 대한 효과 크기는 없다. 표기법 사용 자체가 좋은 판단을 보장하지 않는다. |
| [X12](https://ilcor.org/uploads/Tools-GRADE-guidelines-Evidence-to-Decision-Tables.pdf) Alonso-Coello et al. — GRADE Evidence to Decision frameworks 1: Introduction / 보건 근거 종합 | H: 관점과 판단 기준을 명시할 때까지 | 질문·관점·근거·판단·결론·연구 우선순위 | H: 기준별 판단과 절충을 설명한 뒤 | 근거 수집·기준별 토론 | 주장 대조와 구성 채택을 분리 | 보건 의사결정 틀을 빌린 것이다. D0–D4를 GRADE 확실성 등급으로 치환하지 않는다. |
| [X13](https://discovery.ucl.ac.uk/10025041/1/Thomas_LSR%20overview%20paper%20final%20-%20revised.pdf) Elliott et al. — Living systematic review: 1. Introduction—the why, what, when, and how / 보건 근거 유지 | 중요·불확실·새 근거 유입 조건이 유지될 동안 | 검토 판·검색 시점·갱신/종료 규칙 | 결론을 바꿀 새 근거 또는 living 종료 조건 | 지속 인력·편집·방법 유지 | 재검토 트리거와 보류/종료 상태 | 지속 갱신의 총비용 절감은 확정 효과가 아니라 가설로 제시된다. 모든 묶음에 상시 확인을 강제하지 않는다. |
| [X14](https://www.3ieimpact.org/sites/default/files/2019-01/wp28-egm.pdf) Snilstveit et al. — 3ie evidence gap maps: a starting point for strategic evidence production and use / 국제 개발·근거 정책 | H: 빈칸의 종류와 결정상 필요가 정해질 때까지 | 개입×결과·연구 위치·종합 여부·검토 신뢰도 | H: 자료 생성이 필요한지 종합이 필요한지 구분 | 검색·분류·검토 품질 평가 | 빈칸 묶음에 자료 부재/종합 부재를 표시 | 포함 기준과 검색 범위 안의 빈칸이다. 실제 효과 없음 또는 세계 전체의 자료 없음으로 읽을 수 없다. |
| [X15](https://journals.sagepub.com/doi/full/10.1002/cl2.1125) White et al. — Guidance for producing a Campbell evidence and gap map / 사회 정책·근거 지도 | H: 질문 범위와 분류 틀이 쓸모 있는 동안 | 프로토콜·포함 기준·분류 사전·연구 링크 | H: 사용자에게 의미 없는 세분류를 통합 | 코딩·검색·사용자 협의 | 8개 질문 색인과 기계 판독 목록을 함께 유지 | 지도 셀의 연구 수는 효과 추정치가 아니다. 문서의 기간·인원 예시는 AF-RES 비용 예측으로 옮기지 않는다. |
| [X16](https://link.springer.com/article/10.1186/s13012-016-0462-y) Neumann et al. — The GRADE evidence-to-decision framework: testing in 15 international guideline panels / 보건 패널·도구 평가 | H: 질문과 응답 선택지가 판단을 구분할 때까지 | 근거·추가 맥락·기준별 판단·피드백 | H: 실제 사용자 혼동이 나타나면 틀 개정 | 길이·훈련·회의 부담 | 어휘 충돌의 원인을 실측 실패와 분리 | 틀 개발자가 포함된 자기 보고이고 독립 평가가 없었다. 투명성 개선의 객관적 효과 크기로 읽지 않는다. |
| [X17](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001603) Elliott et al. — Living Systematic Reviews: An Emerging Opportunity to Narrow the Evidence-Practice Gap / 보건 출판·근거 유지 | 새 자료가 실제 결론을 바꾸는지 평가하는 동안 | 판 번호·확인 날짜·기여·변경 범위 | 무변경/추정 변화/결론 변화에 따라 검토 수준 조절 | 지속 작업·중복 분석·검토 부담 | 수집 성공과 판단 변경을 다른 사건으로 기록 | 방법 제안이지 AF-RES 갱신 정책의 실험 결과가 아니다. 논문이 인용한 효과 수치는 이 과제에서 재검증하지 않았다. |
| [X18](https://web.mit.edu/ariely/www/MIT/Papers/doors.pdf) Shin & Ariely — Keeping Doors Open: The Effect of Unavailability on Incentives to Keep Options Viable / 행동 의사결정 | H: 유지 목적이 실제 미래 가치에 연결될 동안 | 보존 이유·지불 시간·기회 비용 | H: 보존 자체가 목적이면 중단 또는 잠재 보관 | 저가치 대안에 시간·돈 낭비 | 활성 연구와 비용 낮은 보관을 구분 | 실험 게임의 행동이며 실제 연구 옵션의 경제적 가치가 항상 낮다는 증거는 아니다. |
| [X19](https://gwern.net/doc/psychology/2002-gilbert.pdf) Gilbert & Ebert — Decisions and revisions: The affective forecasting of changeable outcomes / 심리·의사결정 | H: 정서적 재심 비용과 정보 이득을 비교하는 동안 | 평가 대상·관측 시점·수정 가능 기간 | H: 유용한 새 정보 없이 재심만 반복하면 점검 | 만족·주의 자원 비용 | 실패 신호에 반복 재심의 부담 포함 | 정서적 만족과 기술적 정답은 다르다. 되돌릴 수 없게 만들라는 설계 권고로 전이하지 않는다. |
| [X20](https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders) Amazon — 2016 Letter to Shareholders / 조직 의사결정 | 복구 가능성과 수정 관측이 확보될 동안 | 복구 경로·오류 신호·결정 맥락 | 가역적이면 시도 후 빠르게 재검토 | 늦은 결정의 기회 비용 | 되돌릴 수 있는 경로를 실제 명령·자료로 적음 | 기업 리더의 실무 원칙이다. 70%를 AF-RES의 수용 임계치나 통계 신뢰도로 쓰지 않는다. |
| [X21](https://www.hbs.edu/ris/Publication%20Files/07-057.pdf) Lenfle & Baldwin — From Manufacturing to Design: An Essay on the Work of Kim B. Clark / 산업 조직·설계사 | H: 상호작용을 충분히 알 때까지 경계를 잠정으로 둠 | 분해 근거·규칙·통합 시험 | H: 억제해도 되는 상호작용을 이해한 뒤 | 조직 변화·통합 실패 위험 | 순환 의존 묶음은 공통 계약 또는 합친 판단 단위 | 원 저자 회고의 방법 논증이다. 역사적 성과를 독립 재현한 사례나 AF-RES의 검증으로 세지 않는다. |
| [X22](https://www.nasa.gov/reference/6-8-decision-analysis/) NASA — Systems Engineering Handbook §6.8 Decision Analysis / 항공우주·시스템 공학 | 불확실성 감소가 순위를 바꿀 여지가 있을 동안 | 기준·범위·가정·불확실성·민감도·탈락 이유 | 필수 조건 실패 또는 순위가 견고해질 때 | 분석 시간·일정 지연 | 결정을 바꿀 최소 증거와 보류 이유 | NASA의 공식 방법 지침이며 이 과제의 제품 성능 실험은 아니다. 여기서 최종 구성 추천을 맡기지 않는다. |
| [X23](https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF) Amazon — 2015 Letter to Shareholders / 조직 의사결정 | 비가역적 효과를 내기 전까지 | 가역성·남는 손실·결정권자 | 비가역적이면 충분한 심의; 가역적이면 작은 시험 | 과잉 절차 또는 잘못 분류한 비가역 손실 | 데이터 손실 여부를 코드 크기와 별도로 평가 | 기업 자체 설명이며 양방향성의 정량 판별법은 제공하지 않는다. 작은 구현이라는 이유만으로 가역적이라고 판정하지 않는다. |
| [X24](https://assets.publishing.service.gov.uk/media/6ae0ba897b7111c482d80a3b/The_Green_Book_2026.pdf) HM Treasury — The Green Book: UK government guidance on appraisal / 공공 정책·투자 평가 | 목표·필수 성공 조건으로 좁힐 때까지 | 대안 축·포함/탈락 이유·전환 가정 | 목표 실패 또는 민감도 기준의 변화 | 분석·검토 비용; 규모에 비례시킴 | 독립 선택지 조립과 결정 전환 증거 기록 | 공공 지출의 가치 판단 기준은 AF-RES 사용자 가치와 같지 않다. 실제 열린 판은 2026이며 2022판으로 인용하지 않는다. |

## 3. 나누기와 다시 합치기에 적용할 규칙 — H

### 3.1 분리 기준은 파일 수가 아니라 바뀔 결정이다

묶음의 ‘식별·질문’에는 이 묶음만 채택·보류·교체할 때 바뀌는 결정을 쓴다. ‘관계’에는 공개해야 할 정의·단위·판정 기준을 명시한다. 다른 묶음의 기준이 바뀌면 자신의 수치 의미도 바뀌는 경우는 독립 실행을 주장하지 않는다. 공통 정의를 관계로 드러내도 판단 자체가 불가능하면 합친 단위로 제시한다. 이는 Parnas의 경계 원리와 Baldwin·Clark의 공유 규칙을 연구 문서에 전이한 제안이다. [X04](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html), [X07](https://www.academia.edu/23867694/The_Option_Value_of_Modularity_in_Design_An_Example_from_Design_Rules_Volume_1_The_Power_of_Modularity)

H 적용 예: ‘역할별 recall’과 ‘역할의 뜻’을 별개의 결정으로 유지할 수는 있어도, 전자의 수치를 읽는 순간 후자의 판정 규칙 버전이 필요하다. 계약을 붙이지 않고 독립이라고 부르면 의미가 변한다. AF-RES의 구체 수치·일치 여부는 내부 CLAIM_CHECK에서 판단하며 여기서는 재조사하지 않는다.

### 3.2 보류에는 살려 둘 조건과 비용을 함께 쓴다

‘대안·조합’에는 경쟁 대안과 함께 보류가 유지되는 조건을, ‘다음 확인’에는 선택을 바꿀 최소 증거를 쓴다. ‘반례·한계’에는 보류 비용과 중단 신호를 둔다. 문헌 링크와 이전 판정을 보관하는 일, 유료·인력 투입을 계속하는 일, 실제로 구현해 운영하는 일을 다른 강도의 약속으로 취급한다. NASA의 추가 정보 가치와 Ford·Sobek의 확정 시점 모형에서 빌린 구분이다. [X02](https://www.researchgate.net/publication/3076866_Adapting_Real_Options_to_New_Product_Development_by_Modeling_the_Second_Toyota_Paradox), [X22](https://www.nasa.gov/reference/6-8-decision-analysis/)

### 3.3 사실·근거·판단·결정의 경계를 보존한다

‘근거’에는 원 주장과 분모·관측 창·작성자·위치를 유지한다. ‘검토’에는 이번 작업자의 재대조 판정과 이유를 별도로 둔다. ‘다음 확인’에서 무엇을 관측하면 어떤 선택을 다시 열지 연결한다. QOC의 기준, IBIS의 논거, EtD의 확실성, ADR의 상태는 같은 칸에 넣지 않는다. [X08](https://www.researchgate.net/profile/Victoria_Bellotti/publication/233367028_Questions_Options_and_Criteria_Elements_of_Design_Space_Analysis/links/00b7d53211940ad48e000000/Questions-Options-and-Criteria-Elements-of-Design-Space-Analysis.pdf), [X09](https://www.escholarship.org/content/qt5cj786v8/qt5cj786v8.pdf), [X12](https://ilcor.org/uploads/Tools-GRADE-guidelines-Evidence-to-Decision-Tables.pdf)

### 3.4 수정 이력은 작은 구성도 첫날부터 갖는다

‘짧은 핵심’은 읽기 편하게 고치더라도 원 주장·원 판정·이전 규칙을 덮어쓰지 않는다. 구성 전환에 필요한 최소 이력은 원 질문, 원문 위치와 확인 시점, 평가 단위, 원 판정과 이유, 판정 규칙의 판이다. 구현이 작다는 사실은 되돌릴 수 있다는 증거가 아니다. 이 정보가 유실되면 나중에 더 풍부한 구성으로 옮기며 과거 판단을 복원할 수 없다. ADR의 대체 이력과 가역성 구분을 적용한 H이다. [X10](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), [X23](https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF)

### 3.5 비어 있는 칸을 조사 우선순위와 동일시하지 않는다

빈칸 묶음에는 자료 미발견, 비교 종합 부재, 정의 미정, 접근 차단을 구분하고, 채워지면 바뀔 결정을 적는다. 모든 빈칸을 같은 비용으로 채우지 않는다. 후속 연구자가 먼저 할 일은 빈칸의 종류와 결정상 가치를 확인하는 것이다. 지속 확인도 새 자료가 결론을 바꾸는 영역에 한정하고, 중요성이 줄거나 확실성이 충분하면 종료할 수 있게 한다. [X13](https://discovery.ucl.ac.uk/10025041/1/Thomas_LSR%20overview%20paper%20final%20-%20revised.pdf), [X14](https://www.3ieimpact.org/sites/default/files/2019-01/wp28-egm.pdf), [X15](https://journals.sagepub.com/doi/full/10.1002/cl2.1125)

## 4. 처음 결론을 반증한 기록

첫 가설은 ‘많이 나누고 대안을 오래 남기면 재조합이 쉬워진다’였다. 다음 원문들은 이 가설의 조건을 바꾼다. 이 표의 사례는 외부 방법의 반례이며 AF-RES 원 결과의 불일치 건수에 더하지 않는다.

| 반증하려 한 명제 | 실제 질의·열람 | 관측한 반례 | 바뀐 적용안 |
| --- | --- | --- | --- |
| Toyota는 가능한 오래 미루고 시제품을 늘리면 좋다는 뜻이다 | Sobek/Ward/Liker1999 Introduction·Principle 3; find ‘Principle 3’ | 이전 사례의 극단성을 정정하고 학습에 따라 더 일찍 좁힐 수 있다고 설명 | 달력 지연 대신 적용 조건과 제거 근거를 보존 |
| 경계만 나누면 독립적 교체가 된다 | Parnas General comments; Baldwin·Clark2006 §4–6,11 | 노출한 순서·공유 규칙·통합 비용이 독립성을 제한 | 모든 쌍의 관계와 공유 정의를 남김 |
| 모든 결정에 대안 논증을 상세히 기록하면 도움이 된다 | ‘Graphical Argumentation and Design Cognition’ 원문 Study C | 잘 규정된 문제에서는 QOC가 늦은 기록 작업과 허수 대안을 유발 | 결정의 불확실성에 맞게 기록 강도 조절 |
| 선택지가 사라지지 않게 하는 지출은 정보 가치를 반영한다 | ‘Keeping Doors Open’ 원문 Experiment 3 | 명시적 비용에도 소멸 위협이 추가 유지 행동을 유발 | 보류 이유와 비용의 상한을 따로 검토 |
| 가역성은 모든 결과 지표를 개선한다 | ‘Decisions and revisions’ Studies·Discussion | 변경 가능성의 만족 비용, 반대로 높은 불확실성에서의 이점 인정 | 성능·만족·전환 비용을 하나의 점수로 섞지 않음 |
| 근거를 투명하게 적으면 어휘 충돌도 사라진다 | EtD 15개 패널 연구 Results | 가치의 변이와 불확실성을 한 응답 축으로 묶어 혼동 | 축 분리와 실제 판정자 시험 필요 |
| ‘2022’라는 URL이면 2022판이다 | Green_Book_2022.pdf open→find | 실제 응답은 표지 2026 및 2026 URL로 redirect | URL 외에 실제 판·절·확인 시점 보존 |

## 5. 네 관점에서 산출물을 읽는 법 — H

| 관점 | 조립 시 필요한 정보 | 이번 형식이 제공해야 하는 것 | 남겨 둔 결정 |
| --- | --- | --- | --- |
| 최상위 설계자 | 어떤 선택을 버리면 어떤 근거·조건을 잃는가 | 선택지·충돌·선행·전환 증거; 순위가 불명확한 구성은 함께 표시 | 가중치·목표·초기 구성 선택은 설계자가 결정 |
| 편집 담당 | 제목이 바뀌어도 원문과 이전 선택을 찾을 수 있는가 | 안정된 ID·원 SHA·대체 이력·색인 행 제안 | 공통 색인 반영과 버전 정책 |
| 후속 연구자 | 빈칸을 채우면 어떤 결정이 바뀌는가 | 질문·자료·최소 규모·재개 입력; 자료 부재와 종합 부재 구별 | 어떤 빈칸부터 조사할지 |
| 앞선 작업자 | 수치와 제한이 그대로 전해졌는가 | 원 주장과 이번 재대조를 분리; 분모·시점·정답 작성자·위치 유지 | 원 결과의 수정은 이 과제 범위 밖 |

이 네 읽기 목적은 QOC의 비교 구조, ADR의 대체 이력, 근거 지도의 빈칸 구분, EtD의 근거와 판단 분리에서 가져왔다. 구체 업무 효과는 아직 H다. [X08](https://www.researchgate.net/profile/Victoria_Bellotti/publication/233367028_Questions_Options_and_Criteria_Elements_of_Design_Space_Analysis/links/00b7d53211940ad48e000000/Questions-Options-and-Criteria-Elements-of-Design-Space-Analysis.pdf), [X10](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), [X12](https://ilcor.org/uploads/Tools-GRADE-guidelines-Evidence-to-Decision-Tables.pdf), [X14](https://www.3ieimpact.org/sites/default/files/2019-01/wp28-egm.pdf)

## 6. Q1–Q8에 붙일 외부 방법 출처

내부 원 결과의 근거는 각 묶음과 CLAIM_CHECK에 따로 연결한다. 이 표는 외부 문헌이 무엇을 보조하는지 지정하며, 외부 방법을 내부 관측의 증명으로 대신하지 않는다.

| 세부 질문 | 외부 ID | 보조하는 판단 |
| --- | --- | --- |
| Q1 묶음 나누기 | X04, X05, X08, X14 | 변경 결정·공개 정의·비교 질문·빈칸 종류 |
| Q2 주장 재대조 | X12, X16, X22, X24 | 근거와 판단 분리·축 혼동 탐지·가정/판의 추적 |
| Q3 관계 | X05, X07, X09, X22 | 의존 행렬·공유 규칙·쟁점 관계·상호작용 |
| Q4 충돌 | X08, X09, X12, X16 | 사실·정의·가치·관점의 구별 |
| Q5 시작 구성 | X01, X02, X03, X07, X18, X23 | 대안 보존의 조건·고정 예산 비교·비가역 자료 |
| Q6 남은 결정 | X10, X13, X22, X24 | 재개/종료·수정 이력·전환 증거 |
| Q7 어휘·근거 수준 | X08, X09, X12, X15, X16 | 비슷한 이름의 다른 역할·코딩 사전·정의의 시험 |
| Q8 분야 비교 | X01–X24 | 서로 다른 목적·기록·종료·비용·전이 한계 |

## 7. 한계와 다음 확인

본문 확인 24개는 목적 표집이며 체계적 문헌 고찰의 망라성을 주장하지 않는다. 같은 사이트 최대 3개를 지켰지만 저자 계보의 의존은 남는다. Baldwin·Clark 관련 여러 문헌은 독립 검증 횟수가 아니다. X05·X07·X21, X13·X17, X20·X23을 각각 한 계보로 보수적으로 묶어도20문헌군이다. 이20 역시 통계적으로 독립인 효과 검증20회라는 뜻이 아니다. Toyota 원문 X01에는 Ward가 공동저자로 참여하며, 별도의 1995 논문 스캔은 읽지 못해 제외했다. Design Rules는 원 저자의 허가 재인쇄 발췌 X07과 후속 장 X05를 읽었고 전권 독서를 주장하지 않는다.

학술 저장소·출판사 본문과 저자 공개 원문을 우선했다. 일부 셸 요청은 403이어도 사용자가 허용한 웹 열람 도구에서는 본문이 제공됐다. 공개 원문 전문·사용자 프로필·로그인 자료는 저장하지 않았다. IBIS는 메모리 내 OCR로 본문을 읽었으며, 원 파일과 전체 OCR을 저장하지 않고 구조와 한계만 기록했다.

**다음 확인(H):** 최상위 설계자·편집 담당·후속 연구자·앞선 작업자 역할을 맡은 검토자가 동일한 세 구성을 조립해 보도록 한다. 최소 입력은 정의 선행 관계가 있는 묶음 2쌍, 충돌 2건, 빈칸 1건, 원 판정이 다른 사례 2건이다. 측정할 것은 선택의 일치율 하나가 아니라 원 근거 복원 여부, 조건 누락, 잘못된 무관 판정, 보류 이유의 재현이다. 이 작은 점검으로 비용 추정을 확정하지 않고 형식의 이해 가능성과 실패 조건을 먼저 시험한다. 실제 검토는 이번 외부 방법 읽기에서 수행하지 않았다.
