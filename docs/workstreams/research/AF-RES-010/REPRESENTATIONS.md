# AF-RES-010 — 표현 체계와 검색 시스템

## 결론과 읽는 법

문제의 **보존해야 할 조건**과 검색할 **기능·관계 투영**을 함께 적어야 한다. 전자는 P1/P2 원문에 고정하고, 후자는 기능 동사, 모순, 생물 용어 등으로 여러 개 만든다. 이 조사에서 확인한 체계는 같은 일을 하지 않는다. Functional Basis·분류표·용어 사전은 검색 어휘를 만들고, SAPPhIRE·FBS·SBF는 원인이 어떻게 결과를 만드는지 설명하며, TRIZ는 상충하는 요구를 드러낸다. 하나를 완전한 소프트웨어 요구 언어로 사용하는 것은 이 자료들이 입증한 범위를 넘는다. [R01](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821676), [R02](https://dm.iisc.ac.in/cpdm/ideaslab050320/paper_scans/UID_61.pdf), [R03](https://www.academia.edu/1064816/The_situated_function_behaviour_structure_framework), [R04](https://aitriz.org/documents/articles/40p_triz.pdf)

고정 입력은 AF-RES-002 `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`의 PROTOCOL §2·§3, 판정 틀은 AF-RES-004 `2b798c7d2b7355b649691c18de196104ceabb0f0`의 T축이다. 아래 소프트웨어 예시는 **연구자 작성 H**이며 원저자가 P1/P2를 검증한 결과가 아니다. 원문·필수 조건은 [SCOPE.md](SCOPE.md)에 있고, 아래는 일부 조건을 표현하는 시험이다. SOLVENT와 focused abstraction은 AF-RES-002 METHODS의 기존 검토를 인용하며 이 문서에서 다시 요약하지 않는다.

## Q1. 원문으로 비교한 7개 체계

| 체계 | 표현 단위·어휘 크기 | 누가 어떻게 주석하는가 | 검색에 주는 것 |
| --- | --- | --- | --- |
| Functional Basis | 기능 동사＋흐름; 8개 기능 대분류, 전체 기능 53개; material/signal/energy의 3단계 흐름 분류. Correspondents는 4번째 계층이 아니다. | 설계자가 요구에서 기능을 분해하고 표준 동사·흐름·상세 수준을 선택한다. | 제품명 없이 기능을 찾는 질의; 정밀한 조건은 별도. [R01](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821676) |
| SAPPhIRE | State, Action, Parts, Phenomenon, Input, oRgan, Effect의 7종; activation/creation/interpretation의 3관계. 도메인별 값의 폐쇄 어휘는 없다. | 연구자가 문헌·그림·영상에서 행동의 인과 사슬을 만들고 VNA(동사·명사·형용사)로 기술한다. | 높은 수준 행동과 실제 효과·조건 사이를 이동. [R02](https://dm.iisc.ac.in/cpdm/ideaslab050320/paper_scans/UID_61.pdf) |
| FBS | Function/Behaviour/Structure의 3변수 종류, 기대 Be와 구조에서 도출한 Bs 구별; 기본 FBS 8과정, situated 확장 20과정. 단어 수가 고정된 사전이 아니다. | 설계자가 요구를 해석해 목적, 기대 행동, 구조를 쓰고 분석·평가·재정식화한다. | 목적이 같다는 것과 실제 행동이 맞는다는 것을 구별. [R03](https://www.academia.edu/1064816/The_situated_function_behaviour_structure_framework) |
| TRIZ | 개선/악화 매개변수 쌍, 39×39 전통 행렬, 40원리; 물리적 모순은 동일 요소의 반대 요구. | 설계자·TRIZ 실무자가 특수 문제를 일반 모순으로 재서술하고 원리를 구체화한다. | 무엇을 개선하다 어떤 필수 조건을 해치는지 묻는 질의. [R04](https://aitriz.org/documents/articles/40p_triz.pdf), [R05](https://www.triz.co.uk/glossary) |
| Biomimicry Taxonomy | 8그룹·30하위그룹·160개 넘는 기능; 기능–생물 전략 분류. | 과학 저술·편집·생체모방 검토자가 전략에 기능을 붙인다. 사용자도 기능·동의어·상위/반대 질문으로 탐색한다. | 목적이 비슷한 생물 전략을 발견하는 입구. [R06](https://ask-nature.sfo3.digitaloceanspaces.com/wp-content/uploads/2021/06/31121252/Taxonomy_Explainer_2021.pdf), [R17](https://asknature.org/about/) |
| Engineering-to-Biology thesaurus | Functional Basis 기능·흐름과 생물 대응어의 다대다 연결; 원논문 기반 계층은 기능 8/21/24, 흐름 3/20/22. 현재 공개 대응표는 10쪽이며 생물 동의어 총수는 명시하지 않는다. | 연구자가 교과서 동시출현·사전·기존 어휘를 종합하고 동물학 교수1명이 배치·모호성을 검토했다. | 익숙한 동사를 생물 문헌 용어로 바꾸기. [R07](https://www.academia.edu/20640079/An_Engineering_to_Biology_Thesaurus_for_Engineering_Design), [R08](https://jacquelynnagel.com/wp-content/uploads/2020/10/E2BThesaurusv2.pdf) |
| 특허 기능 벡터(Murphy/Fu 등) | 특허에서 추출한 1,700기능 동사, 계층·동의어로 확장한 질의 벡터와 문서 벡터. | 전처리·품사/어휘 추출로 대량 주석; 설계자는 기능을 골라 검색하고 원문을 판단한다. | 명칭·산업 분류가 다른 특허의 기능적 유사성. [R09](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/murphy_2014_function-based_design-by-analogy-jmd.pdf) |

### 소프트웨어 개념 수용성

다음은 각 정의를 소프트웨어에 대입한 **H 평가**다. “표현 가능”은 그 표현을 받아 실행하거나 검색 결과를 검증하는 소프트웨어가 있다는 뜻이 아니다.

| 체계 | 재시도 | 상태 | 충돌 | 흐름 제어 | 멱등성 |
| --- | --- | --- | --- | --- | --- |
| Functional Basis | 반복 횟수·중단 후 재개는 보조 조건 | status signal은 가능 | 분기·결합 동사만으로 상충 의도는 불충분 | Regulate/Stop/Prevent＋control signal이 직접적 | 같은 입력·동일 결과 관계는 별도 |
| SAPPhIRE | 상태 전이·입력 반복으로 서술 | 명시 구성요소 | 복수 상태·조건을 추가해 서술 | Input–oRgan–Effect 사슬로 연결 | 논리 법칙을 Effect로 쓰면 물리 중심 원형의 확장 |
| FBS | Be에 실패 후 행동 명시 | B의 변수로 명시 | Be에 보존·해결 절차 명시 | B와 S의 대응으로 기술 | Be의 반복 적용 불변식으로 기술; Bs 검증은 별도 |
| TRIZ | 신뢰성 개선 수단으로 넣음 | 고유 상태 기계 없음 | 기술 모순은 편집 충돌과 다른 개념 | 개선/악화 모순을 통해 접근 | 중복 결과를 악화 항목으로 넣을 수 있으나 보장식은 없음 |
| AskNature taxonomy | 복구·반응 등의 탐색 질문 | modify state 등의 넓은 기능 | cooperate/coordinate가 충돌 보존까지 의미하지 않음 | process/respond/send signals 경로 | 특정 동일성·한 번 공개 조건은 범주 밖 |
| E2B thesaurus | 대응 동사로 우회 | status signal 대응어 | 생물학적 경쟁·재조합을 편집 충돌과 혼동할 위험 | Regulate→gate 등 | 중복/동일성 정의와 원리 검증은 제공하지 않음 |
| 특허 기능 벡터 | retry 관련 동사가 있어도 순서 관계는 약함 | 동사 집합은 전이 순서·버전을 소실 | resolve/combine은 덮어쓰기와 병합을 구별하지 못함 | regulate/control 기능 후보 검색 | 부정·횟수·동일 입력 조건이 벡터에 보존된다는 증거 없음 |

특히 NIST Appendix B의 **Provision은 물질·에너지 흐름으로 제한**된다. `Store information`을 원형의 엄격한 기능식이라고 쓸 수 없다. 반면 Separate/Export/Regulate는 signal 흐름을 허용한다. 이 차이는 R1이 “Functional Basis식 질의”일 때 소프트웨어 확장 부분을 표시해야 하는 실제 이유다. [R01](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821676)

### P1/P2 필수 조건을 실제로 써 본 결과 — 모두 H

| 체계 | P1의 조건 하나를 표현 | P2의 조건 하나를 표현 | 표현 뒤에 반드시 남길 조건 |
| --- | --- | --- | --- |
| Functional Basis | **실패 항목 확인**: `Detect(status signal: item_failed) → Indicate(status signal: failed_item_id)` | **사용자 파일 내보내기**: `Export(signal: record_content, boundary: user's file)` | 동사·signal은 원형 어휘; item ID·파일 경계는 목표 문제 주석이다. 실패 표시만으로 성공 보존이나 재시도는 증명되지 않는다. |
| SAPPhIRE | **중복 공개 방지**: Action=publish once; State=공개0→1; Input=동일 항목의 반복 요청; Parts=처리기·공개 기록; oRgan=동일 입력 식별＋원자적 공개 판정; Phenomenon=반복 공개 억제; Effect=멱등 전이. | **상충 수정 보존**: Action=retain competing edits; State=기준판→{수정a, 수정b}; Input=재연결; Parts=복제본·해결 화면; oRgan=수정 식별·내구 저장; Phenomenon=두 수정 합집합과 충돌 표시; Effect=해결 전 비삭제. | 마지막 Effect 두 개는 물리 법칙을 논리 불변식으로 바꾼 연구자 확장이다. 실제 구현의 원자성·내구성은 별도 입증해야 한다. |
| FBS | **성공 결과 보존**: F=완료 작업의 효용 보존; Be=`fail(i) ⇒ successful_result(j≠i) retained`; S 후보=항목별 결과 경계; Bs=장애 실행 후 관측할 행동. | **상충 수정 확인·해결**: F=수정 의도 보존; Be=동시 수정a,b를 사용자 해결 전 모두 확인 가능; S 후보=분기 기록＋해결 화면; Bs=재접속 시험으로 확인할 행동. | Be는 요구이고 Bs는 결과다. 후보 S를 썼다는 이유로 충족 판정하지 않는다. |
| TRIZ | **재시도＋중복 공개 금지**: 재실행은 복구 가능성을 높이지만 동일 결과의 중복 노출을 늘린다. 질문: 실행과 공개를 서로 다른 시간·조건으로 분리할 수 있는가? | **오프라인 쓰기＋충돌 보존**: 독립 수정을 허용하면 가용성이 높아지지만 공동 상태 해석은 어려워진다. 질문: 병렬 수정의 보존과 최종 선택을 단계로 분리할 수 있는가? | 일반 모순 서술이며 검증된 행렬 셀 조회 결과가 아니다. “최종 일치”만 얻어 사용자 수정을 버리는 해결은 P2 탈락이다. |
| AskNature taxonomy | **항목별 실패 격리**: `Process information → Process signals → Respond to signals`에서 “생물은 결함 부위 신호에 반응하면서 다른 부분의 기능을 어떻게 지속하는가?” | **재연결 후 충돌 확인**: `Maintain community → Coordinate → Coordinate by self-organization`에서 “분리된 개체가 정보를 다시 교환할 때 다른 신호를 어떻게 감지하는가?” | 생물 신호 제거·다수결·세포 사멸은 P1 성공 보존/P2 수정 보존과 충돌할 수 있다. 실제 후보는 이 부정 조건으로 다시 걸러야 한다. |
| E2B thesaurus | **실패 확인**: `Measure → monitor/observe`로 “monitor abnormal local process, signal without disabling others”라는 생물 질의를 작성. | **수정 보존**: `Store → conserve/hold`로 “conserve competing local states until reconciliation”이라는 질의를 작성. | P2의 conserve는 생물 용어로 옮긴 확장 질의이며 정보를 저장하는 원형 FB 식이 아니다. 의미 보존을 필수 조건 표와 다시 비교한다. |
| 특허 기능 벡터 | **항목별 실패 격리**: `separate + detect + prevent`를 각각 단독 및 짧은 조합으로 검색; 대상은 처리 항목. | **충돌 확인·해결**: `detect + indicate + couple`를 분리 검색; 대상은 독립 수정들. | 검색 뒤 두 수정이 남는지 원문 확인이 필요하다. 동의어를 모두 합친 긴 벡터는 더 좋은 명세가 아니다. |

이 표는 “어떤 소프트웨어 부품을 채택할지”를 정하지 않는다. 예컨대 P1의 입력 동일성을 바이트 해시·경로·사용자 작업 ID 중 무엇으로 정의할지는 원문이 정하지 않았으므로 열어 둔다. P2도 집합 합집합을 적었다고 실제 기록 의미의 충돌 해결이 끝나는 것은 아니다.

## Q2. 실제 시스템, 규모, 평가와 운영 상태

규모는 **논문 발행 당시**와 **2026-11-20 공개 관측**을 구별했다. 정확도 대신 아이디어 수나 모델 완성도를 측정한 연구에 검색 정확도 숫자를 만들어 붙이지 않았다.

| 시스템 | 표현·당시 규모 | 구축/주석과 보고된 평가 | 현재 공개 운영 증거 |
| --- | --- | --- | --- |
| AskNature | 기능 taxonomy로 색인한 생물 전략·응용. 기관 소개는1,700+프로필. | 편집·과학 저술·검토 역할 공개; 이번에 읽은 공식 문서에는 검색 정밀도 벤치마크나 항목당 원가 없음. | native 검색 UI에서 Biological Strategies facet1,839와 `cell cycle` 결과3개 관측. 프로필/검색facet은 단위가 다르다. [R17](https://asknature.org/about/), [R18](https://biomimicry.org/inspiration/asknature/), [O01](https://asknature.org/?s=cell%20cycle&page=0&hFR%5Bpost_type_label%5D%5B0%5D=Biological%20Strategies&is_v=1) |
| IDEA-INSPIRE | SAPPhIRE/VNA; 2005 자연 DB 약100항목＋인공 시스템 DB. | 설계자3명×2문제; 전체 아이디어의 평균 약47%가 시스템 기여. 비교 순서는 항상 단독→도구 사용. 검색 가중치를 정밀도로 해석하지 않는다. | 기관 설명 페이지 가용; 현재 공개 검색 런타임의 실행 증거는 확보되지 않았다. [R02](https://dm.iisc.ac.in/cpdm/ideaslab050320/paper_scans/UID_61.pdf), [R10](https://dm.iisc.ac.in/cpdm/ideaslab050320/ideainspire.php) |
| DANE | **SBF** 모델 약40개(부분 모델 포함); Gero의 FBS와 동일 체계로 부르지 않는다. | 40–100h/완성 모델; 수업40명에서 학생 신규9모델 모두 불완전. 검색 정밀도 실험이 아니라 현장 관찰. | 읽은 자료는 당시 배포·연구 도구를 증명한다. 기관 페이지 접근 실패는 서비스 폐쇄의 증거가 아니다. [R11](https://web.cs.wpi.edu/Research/aidg/CS540/papers/Goel-four-characteristics-of-KB-CAD.pdf) |
| BioTRIZ | 약500현상·270+기능·약2,500모순/해결을6분야 행렬에 대응. | 전문가 분류; 기존 TRIZ와 행렬 유사도.12는 성능 지표가 아니다. | 공식 교육 과정이 공개돼 있으나 원논문 DB의 현재 공개 검색 서비스와는 별개다. [R12](https://pmc.ncbi.nlm.nih.gov/articles/PMC1664643/), [R19](https://www.biotriz.com/programs/online-classes-9xemw) |
| InnoGPS | 500만+특허의 인용 기반 기술 공간,121영역. 기능·메커니즘의 정답 표가 아닌 탐색 지도. | 54명(24/30), 아이디어126→165와149→216; p=.0560/.0023. 품질 미측정·고정순서. | 개발 연구실 페이지·계정 생성 링크 가용; 로그인 없이 검색 실행은 관측하지 않았다. [R13](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/C25D8D2979FF65EEA2F1D855C179B7F3/S0890060418000094a.pdf/design_opportunity_conception_using_the_total_technology_space_map.pdf), [R14](https://www.aidilab.ai/innogps) |
| Hope et al. 2017 | 8,500제품의 목적/메커니즘 주석, 학습 약5,500·시험2,500. | 문서당4작업자 주석. 상위5% 쌍 precision .612 대 TF-IDF .537; top-5 결과 정확도가 아니다. 38명 ideation 실험 별도. | 연구 프로토타입/원논문이 증거이며 현재 일반 공개 서비스 운영 증거는 아니다. [R15](https://joelchan.me/assets/pdf/2017-kdd-analogy-purpose.pdf) |
| Kittur et al. 2019 | 크라우드+AI 연구 프로그램의 종합. 단일 새 검색 DB나 별도 표본이 아니다. | 표현의 비용–정교함 절충, 복수 조건의 문제를 종합; 인용된 동일 실험을 독립 재현으로 세지 않는다. | 논문 접근 가능. 단일 운영 서비스에 해당하지 않아 “현재 DB 몇 항목”을 배정하지 않는다. [R16](https://pmc.ncbi.nlm.nih.gov/articles/PMC6369801/) |
| Murphy et al. 특허 기능 검색 | 65,000특허에서 어휘, 약275,000특허 검색. | 2설계 사례; 와인더의 기존 상위 유사제품5개 중3개 회수. 일반적인 precision60%가 아니다. | 논문 내 프로토타입이 확인 범위; 현재 상용·공개 서비스와 동일하다고 볼 근거 없음. [R09](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/murphy_2014_function-based_design-by-analogy-jmd.pdf) |

### 표현이 더 정교하면 항상 더 낫다는 결론에 대한 반증

| 반증 시도 | 실제로 확인한 내용 | 이 연구의 판단 변화 |
| --- | --- | --- |
| 원형 어휘만 쓰면 의미가 보존되는가? | Functional Basis의 Store는 signal을 허용하지 않는다. E2B의 Bind는 여러 공학 기능에 대응한다. [R01](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=821676), [R08](https://jacquelynnagel.com/wp-content/uploads/2020/10/E2BThesaurusv2.pdf) | 표준어를 사용한 것과 P1/P2 의미 보존을 따로 검사한다. |
| 기능을 더 많이 넣으면 더 정확한가? | Murphy의 약120용어 확장 질의는 코사인 판별력을 악화시켜 적은 기능의 복수 검색을 권했다. [R09](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/murphy_2014_function-based_design-by-analogy-jmd.pdf) | 전체 요구를 한 기능 벡터로 압축하지 않고 부분별 질의를 만든다. |
| 완전한 관계 모델이면 자발적 큐레이션이 늘어나는가? | DANE 신규9모델이 모두 불완전했고 기존 DB가 작아 기여 동기도 약했다. [R11](https://web.cs.wpi.edu/Research/aidg/CS540/papers/Goel-four-characteristics-of-KB-CAD.pdf) | 후보를 좁히기 전 전량 깊은 주석을 요구하는 안을 지지하지 않는다. |
| 기존 taxonomy를 그대로 기계 추론용 ontology로 쓰면 되는가? | 2025년9자원×9기준 평가가 용어·관계·가용성 문제를 발견했다. 유용성 자체는 평가 대상에서 제외했다. [R20](https://pmc.ncbi.nlm.nih.gov/articles/PMC11762366/) | 검색용 어휘와 형식 추론 계약을 구분한다. 그 비판을 인간 탐색의 무효 판정으로 확대하지 않는다. |

반증 질의 문자열과 열람 경로는 [evidence/representation-searches.json](evidence/representation-searches.json), 원문별 확인 내용·절·한계는 [evidence/representation-sources.json](evidence/representation-sources.json)에 있다.

## 한계

서로 다른 시스템의 모집단·정답·목표가 달라 정밀도 순위를 만들 수 없다. FBS와 Kittur 논문은 각각 개념 틀과 종합 연구이며 새 통제 실험으로 세지 않았다. 구형 도구의 설명 페이지, 현재 교육 판매, 로그인 링크를 현재 검색 성능으로 대체하지 않았다. AskNature 현재 동작은 O01의 직접 관측 범위로 제한한다. 소프트웨어 예시의 실제 실행 검증은 수행하지 않았으며, 이는 Q5 후보 판정과도 별개다.
