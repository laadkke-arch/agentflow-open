# AF-RES-010 — 자기 점검

## 상태와 점검 범위

이 문서는 Q1–Q8의 답·근거 종류·반증 시도·남은 확인을 대조한 내용 점검이다. **내용 기준과 기록 일관성·허용 경로 검사를 통과했다.** 아래 §7의 실제 검사 결과를 확인한 뒤 HANDOFF를 작성한다. 통과 범위는 연구 산출물이며 대상 소프트웨어 구현의 성공을 뜻하지 않는다.

원문과 판정의 기준은 [SCOPE.md](SCOPE.md)다. 시작 SHA는 `1eca580bf9ddc153f7c9691e30bd727eb7d0ce06`, P1/P2 고정 입력은 AF-RES-002 `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`, T축은 AF-RES-004 `2b798c7d2b7355b649691c18de196104ceabb0f0`다. 검색 전에 고정한 SCOPE 커밋은 `ebcca564df68377cc116634dcdab1695be69c0e8`다.

출처 ID와 종류는 [sources.json](sources.json)의 실제 `source_type` 문자열을 사용한다. 종류 수는 독립성·신뢰도의 점수가 아니다. 예컨대 원저자 저널 논문과 같은 실험의 공개 데이터 설명은 서로 다른 자료 종류지만 독립 재현은 아니다. Q5/Q6에는 사용자 규칙의 실험 예외인 **수치표 1개와 구체 사례 1개 이상**을 적용한다.

## 1. 질문별 내용 점검

| 질문 | 답 한 줄 | 붙은 출처 ID와 실제 종류 수 | 반증을 찾은 질의·자료와 관측 결과 | 남은 불확실성·답을 바꿀 최소 추가 확인 |
| --- | --- | --- | --- | --- |
| Q1 표현 | 원문 조건을 유지하면서 기능·흐름, 인과 관계, 모순, 분야 대응어로 부분 질의를 만들고, 어느 표현도 소프트웨어 불변식을 자동 보장한다고 보지 않는다. | **8종**: `institutional_technical_report` (R01); `peer_reviewed_article` (R02, R03, R09, R20); `primary_method_document` (R04); `practitioner_primary_documentation` (R05); `official_taxonomy_document` (R06); `peer_reviewed_conference_paper` (R07); `author_primary_vocabulary` (R08); `official_editorial_documentation` (R17). | RQ02 `"Function Based Design-by-Analogy" "poor resolution"` → R09의 약 120용어 확장은 판별력을 낮췄다. RQ03의 ambiguity/validation 질의 → R07·R08은 대응어를 인과 동일성으로 보증하지 않는다. R01 Appendix B의 Provision은 물질·에너지로 한정되어 `Store information`을 원형 문법으로 쓸 수 없다. RQ04 → R20의 ontology 재사용 문제도 확인했다. | 7체계의 P1/P2 예시는 H이며 실제 검색 성능이 아니다. 같은 필수 조건·후보 자료에 표현만 교차 적용하여 누락 조건과 대응 일치도를 확인해야 표현 우열로 답을 바꿀 수 있다. |
| Q2 시스템 | 표현을 검색 시스템으로 만든 사례는 여럿 있으나 규모·검색 정밀도·아이디어 증가·현재 공개 동작은 서로 다른 지표다. | **7종**: `peer_reviewed_article` (R02, R09, R11, R12, R13); `official_system_documentation` (R10, R14, R18); `peer_reviewed_conference_paper` (R15); `peer_reviewed_synthesis_article` (R16); `official_editorial_documentation` (R17); `official_training_documentation` (R19); `primary_system_observation` (O01). | RQ01 `"DANE" "40–100" "knowledge"` → R11의 깊은 모델 비용과 불완전한 신규 9모델을 확인했다. RQ02 → 특허 기능 벡터의 긴 질의 역효과. O01 및 native 검색 로그 → AskNature의 동작을 직접 관측했지만 전체문 1개는 결과 갱신 실패로 제외했다. R10/R14의 설명·계정 링크가 있다는 것을 검색 실행 성공으로 세지 않았다. | IDEA-INSPIRE·DANE·InnoGPS 등의 현재 검색 런타임과 공통 정답셋 성능을 확보하지 못했다. 로그인·계정 생성 없이 접근 가능한 동일 질의의 결과와 버전 기록이 최소 추가 확인이다. Hope의 상위 5% 쌍 precision을 top-5 정확도로 바꾸지 않는다. |
| Q3 실증 | 먼 유추는 일부 조건에서 새로움을 높였지만 다른 거리 조작·인지 상태에서는 성과를 낮췄고, 추상화·예시가 항상 고착을 풀지는 않았다. | **3종**: `peer_reviewed_empirical_paper` (E01, E02, E03, E04, E05, E06, E07, E08, E09, E10, E11, E12, E13, E16); `primary_dataset_documentation` (E14); `peer_reviewed_methodological_review` (E15). | EQ02 `"The Meaning of Near and Far" Fu pdf` → E02의 far 최대 새로움이 near보다 낮음(d=−.82, p=.02). 지지 E01의 far>near 새로움 d=.56과 함께 기록했다. EQ11 → E13·E15의 상세도/작성시간 대체 설명; E01 마지막 단계의 수량 효과도 p=.47. EQ16 → E16 혼합 자극의 다양성 저하와 내용/추상수준 혼재. EQ06 → E12는 개발자의 생물·항공 원리 검색 빈도를 입증하지 않는다. | E13 일부 표본과 E16은 중복이며 독립 재현이 아니다. E14는 공개 데이터 설명만 읽었다. 최소 추가 확인은 E14 평가표의 수치 재계산, 동일 메커니즘의 내용·추상수준을 분리한 교차 처치, 전문 개발자의 고정 P1/P2 판단 실험이다. 현재 자료로 순수한 추상화 깊이 효과나 원거리 검색 수요를 확정하지 않는다. |
| Q4 실제 전이 | 9개 원저자 저작물에서 10개 전이를 확인했으며, 성공하는 것은 분야 명칭이 아니라 조건에 맞게 바꾼 관계와 작동 경계다. | **8종**: `peer_reviewed_conference_paper` (T01, T02); `peer_reviewed_journal_paper_author_copy` (T03); `original_author_technical_book` (T04); `original_practitioner_operations_book` (T05, T11); `peer_reviewed_journal_paper` (T06, T07); `implementing_organization_technical_report` (T08); `original_implementer_conference_transcript` (T09); `original_practitioner_technical_report` (T10). | TQ01 `"circuit breakers" "modal behavior" recovery` → T10은 모드 전환과 회복 지연 위험을 설명한다. TQ02 → T02의 race-condition 누락. TQ03 → T03의 NSFNET UP 부하에서 BF/SPF throughput이 약 10% 높음. TQ04 → T09의 Andon 사용이 약 두 달 뒤 끊긴 행동 반례. 성공 사례 수만으로 보편 효과를 주장하지 않는다. | 원저자의 D1 구현·운영 보고를 이번 연구의 D3 재실행으로 세지 않는다. 다음 확인은 선택한 한 전이에 대해 원저자의 실패 조건을 포함한 부하·장애·행동 시나리오를 실행하는 것이다. T04의 두 패턴을 서로 다른 저작물로 세지 않는다. |
| Q5 재탐색 | 일반 웹 64개와 AskNature 16개 계획 질의를 실행하여 별도 후보 본문 24개를 읽고 25개 사용 방식으로 판정했으며, 두 문제의 새 출발 분야 관계는 7가족으로 묶였다. | **실험 예외 기준**: §3의 8행 수치표 및 §4의 실제 질의·사례를 사용한다. [SEARCH_LOG.json](SEARCH_LOG.json), [Q5 별도 원장](sources.json), [P1 판정](evidence/p1-judgments.json), [P2 판정](evidence/p2-judgments.json). 구체 출처: B07, B09, B14, C05, C07, C08, D01, D03. O01은 검색 관측이며 후보 본문 수에 넣지 않는다. | P1-R1-06 `separate control store signal flow` → B07은 신호 라우팅 단어만 맞는 오탐. P2-R1-06 `combine store information flow` → D03의 현재값 결합은 분기 보존이 아니다. P2-R3-06 → C07의 동일인 판별로 문제가 바뀌었다. P1-R3-01의 B09-M과 P2-R3-07의 C05-M은 관계가 있어도 필수 조건을 위반하는 사용 방식이다. | 64개는 고유 일반 웹 문자열이고 native 재확인·control은 더하지 않는다. AskNature는 계획 16개 중 15개에서 결과 또는 빈 결과를 확인했고 1개는 검증 실패했다. 후보 판정은 선택적으로 연 본문에 한정된다. 동일 언어·읽기 예산·독립 질의 작성으로 재실행해야 현재 발견 차이를 표현 효과로 바꿔 말할 수 있다. |
| Q6 표현 비교 | R1은 제어/복구, R2는 모순·판정, R3는 보존·조정 관계를 끌어왔지만 오탐과 근접 오답도 함께 나와 새 표현의 일반적 우위를 주장할 수 없다. | **실험 예외 기준**: §3의 표현별 새 후보/오탐/근접 오답 수치표와 §4의 B07·D03·B09-M·C05-M·C08·C07 사례. 집계 원본은 [comparison-counts.json](evidence/comparison-counts.json); 출처·용도 연결은 두 문제의 판정 파일이다. | R1의 B07/D03은 너무 넓은 추상화의 실제 반례이고, P1-R2-01의 B14는 reliability/repeating이 과학적 replicability로 이동한 오탐이다. R3의 B09-M·C05-M·C08은 관계 대응이 있어도 공개 중복/수정 소실을 낳는 근접 오답이다. P2-R0 본문 판정 0개는 후보 부재나 낮은 정밀도의 증거가 아니다. | 같은 가족이 여러 표현에서 나오거나 양성/근접 오답 용도를 함께 가지므로 행·열을 더해 고유 원리 수로 읽을 수 없다. R0의 한국어와 R1–R3의 영어, 연구자의 분야 선택·본문 선택이 교란된다. 사전 고정한 동등 읽기 예산과 독립적으로 만든 질의 집합에서 재검증해야 우열 판단을 바꿀 수 있다. |
| Q7 최소 설명 | 후보 옆에는 관계 대응, 연결 조건, 실패 입력, 원 분야의 입증 수준과 목표 적용 범위를 함께 적고, 시간·규모·사람 가정은 T축을 바꾸지 않고 덧붙여야 한다. | **7종**: `manufacturer_primary_product_manual` (D01); `primary_regulatory_manual` (B03); `peer_reviewed_primary_experiment` (B09); `primary_healthcare_process_protocol` (C01); `primary_healthcare_process_toolkit` (C02); `primary_editorial_encoding_standard` (C04); `government_primary_field_study_and_practice_guide` (C05). | P1-R3-01/B09-M: 세포의 다음 주기 재허가를 프로세스 재시작으로 옮기면 동일 입력을 다시 공개한다. P2-R3-07/C05-M: 허용오차 이하 차이를 숨기는 관행은 P2의 수정 보존·확인 조건을 위반한다. D01의 Automatic Power-Up 조건은 reset/start 단어만 보고 자동 공개를 허용할 수 없다는 반례다. §5의 6후보 설명 시험은 이 차이를 실제 필드로 드러낸다. | 설명 카드를 실제 설계자에게 주어 판단 정확도나 시간을 측정하지 않았다. 최소 추가 확인은 동일 후보의 제목·요약만 준 조건과 관계/실패 조건을 준 조건에서 채택·기각 이유, 핵심 조건 회상, 근접 오답 거부를 비교하는 것이다. 판정 단위는 AF-RES-004 그대로다. |
| Q8 비용·운영 | 작은 프로젝트에는 수요가 있는 부분 문제에서 유망 후보만 깊게 설명하는 방식이 타당한 H이며, 전량 인과 모델·대규모 자체 코퍼스 재구축의 경제성은 입증되지 않았다. | **7종**: `peer_reviewed_article` (R09, R11, R12, R13, R20); `official_system_documentation` (R14, R18); `peer_reviewed_conference_paper` (R15); `peer_reviewed_synthesis_article` (R16); `official_editorial_documentation` (R17); `official_training_documentation` (R19); `primary_system_observation` (O01). | RQ01/R11: 완성 SBF 모델 40–100시간, 학생의 신규 9모델 모두 불완전하여 자발적 완전 주석 가정에 반대한다. RQ02/R09: 더 긴 기능 확장은 판별력을 낮췄다. RQ04/R20: 9자원 중 6개만 가용하고 용어·관계 문제를 확인했다. R15의 비용·precision, R17/R18의 규모·역할, R19의 교육 가격을 같은 단위로 환산하지 않았다. | 항목당 유지 원가·FTE와 이 프로젝트의 작업 시간은 계측하지 않았다. [COST.md](COST.md) §5처럼 찾기/읽기/매핑/반증/수정 시간을 기록하고, 전량 주석과 선택적 주석을 동일 예산으로 비교해야 경제성 가설을 바꿀 수 있다. 선별로 좋은 후보를 놓치는 비용도 포함한다. |

Q1/Q2/Q8의 반증 질의 RQ01–RQ04는 [representation-searches.json](evidence/representation-searches.json), Q3의 EQ01–EQ19는 [empirical-searches.json](evidence/empirical-searches.json), Q4의 TQ01–TQ04는 [transfer-searches.json](evidence/transfer-searches.json)에 있다. 이 문헌 조사 질의는 Q5의 64개에 더하지 않는다. Q1·Q2는 [REPRESENTATIONS.md](REPRESENTATIONS.md), Q3는 [EVIDENCE.md](EVIDENCE.md), Q4는 [TRANSFER_CASES.md](TRANSFER_CASES.md), Q8은 [COST.md](COST.md)에 상세 설명이 있다.

## 2. 원장 수와 계수 경계

아래 원장 집계를 §7의 검사에서 재계산했다. 자료 수는 실험의 독립성이나 목표 적용 성공 수를 나타내지 않는다.

| 집계 대상 | 현재 수 | 무엇을 세지 않았는가 |
| --- | ---: | --- |
| background 본문 자료 | 47 | Q5 후보 24개, 검색 snippet, 차단/열람 실패, 동일 저작물 미러 |
| 별도 직접 시스템 관측 | 1 (O01) | 본문 47개 또는 Q5 후보 본문으로 중복 계수하지 않음 |
| background 동료심사 논문 | 30 | 자료 수를 독립 표본·독립 재현 수로 해석하지 않음 |
| 방법·결과까지 확인한 동료심사 자료 | 27 | 개념 틀 R03, 종합 R16, 방법론 검토 E15를 실험 방법·결과 확인 수에서 제외; E13/E16의 겹치는 표본은 독립성 없음 |
| 표현·시스템의 1차 문서 | 18 | 원저자의 논문과 공식·전문가 문서를 포함; 같은 원리/시스템 수와는 다름 |
| 표현 체계 비교 | 7 | FBS와 DANE의 SBF를 같은 체계로 합치지 않음 |
| 원저자가 밝힌 전이 | 9개 저작물, 10개 사례 | T04의 circuit breaker/bulkhead는 2사례·1저작물; T10/T11의 반증·후속 자료를 새 전이 원저자로 더하지 않음 |
| Q5에서 별도로 읽은 후보 본문 | 24 | background 47+1과 별도; 같은 문서를 여러 질의·용도에서 열어도 1개 |
| Q5 사용 방식 판정 | 25 | 본문 수와 다름; C01 판정은 C01/C02 두 자료를 쓰고 B09/C05는 서로 다른 두 용도를 판정 |
| 새 출발 분야 관계 가족 | 문제별 고유 7 (P1 4, P2 3) | 새 소프트웨어 알고리즘 7개라는 뜻이 아님; 양성 판정 10개·표현별 가족 수와 구별 |
| 일반 웹 실행 | 64개 고유 문자열 | 문헌 조사, supplemental, native 반복을 더하지 않음 |
| AskNature 계획 질의 | 16개: 15개 결과/빈 결과 확인, 1개 검증 실패 | 실패를 빈 결과 또는 부재로 바꾸지 않음 |
| AskNature 전체 시도 | 18회 = 계획 16 + 재확인 1 + control 1 | 18회를 서로 다른 질의 수로 쓰지 않음 |

## 3. Q5/Q6 수치표

집계 원본은 [comparison-counts.json](evidence/comparison-counts.json)이다. 단위는 **문제 × 표현 × 가족 × 사용 방식별 bucket**이다. 각 bucket 안에서는 같은 가족을 한 번 세지만, 같은 가족의 다른 용도가 새 후보와 근접 오답에 각각 들어갈 수 있다. 읽지 않은 결과는 오탐·근접 오답·부재 중 어느 쪽에도 넣지 않는다.

| 문제 | 표현 | 일반 웹 고유 질의 | native 계획 질의 | 새 후보 가족 (a) | 본문 확인 오탐 가족 (b) | 필수 조건 충돌 가족 (c) | 직접 연 서로 다른 후보 자료 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | R0 | 8 | 2 | 0 | 1 | 0 | 1 |
| P1 | R1 | 8 | 2 | 1 | 2 | 0 | 3 |
| P1 | R2 | 8 | 2 | 1 | 1 | 0 | 3 |
| P1 | R3 | 8 | 2 | 3 | 1 | 1 | 6 |
| P2 | R0 | 8 | 2 | 0 | 0 | 0 | 0 |
| P2 | R1 | 8 | 2 | 0 | 2 | 0 | 2 |
| P2 | R2 | 8 | 2 | 1 | 0 | 0 | 1 |
| P2 | R3 | 8 | 2 | 3 | 1 | 2 | 8 |

부족 판정은 P1-R3의 B13과 P2-R3의 C03에 각각 1가족이며, P1-R3의 B12는 기존 원리 재발견, P1-R2의 B11은 소프트웨어 내부 검증 참고다. 이들은 (a)–(c)에 억지로 배치하지 않는다. P1-R3의 B09와 P2-R3의 C05는 (a)/(c)에 각각 등장해도 전체 고유 가족은 늘지 않는다. P1의 B02/B10, P2의 C04/D02/C06은 출처·표현이 달라도 각각 한 가족으로 묶었다. P2-R3 새 후보의 ID는 4개지만 가족은 3개다.

이 표는 반환 모집단 전수의 정밀도/재현율 표가 아니다. 선택한 본문의 수와 종류, 언어, 분야 어휘, 선행 지식이 달라 비율로 표현 우열을 일반화하지 않는다.

## 4. Q5/Q6의 구체 반례 대조

| 실제 질의 | 본문·판정 | 무엇이 틀렸는가 | 결론에 주는 제약 |
| --- | --- | --- | --- |
| P1-R1-06 `separate control store signal flow` | B07 / RP1-B07: surface_false_positive | signal routing 블록 목록은 공개 이력·입력 동일성·내구 상태의 관계를 제공하지 않았다. | 기능 추상화가 너무 넓으면 이름이 맞는 내부 소프트웨어 문서로 돌아올 수 있다. |
| P2-R1-06 `combine store information flow` | D03: surface_false_positive | 현재 store 값의 결합은 독립 수정의 계보·충돌 보존과 다르다. | combine이라는 공통 동사로 병합의 의미를 대체하지 않는다. |
| P1-R2-01 `increase reliability by repeating interrupted work without duplicating released results` | B14 / RP1-B14: surface_false_positive | 과학적 결과의 재현은 한 입력의 중복 공개를 금지하는 처리 계약이 아니다. | 모순 표현도 reliability/repeating의 다의성에서 벗어나지 못한다. |
| P1-R3-01 `cell cycle DNA replication once and only once licensing prevent rereplication after checkpoint` | B09 / RP1-B09-M: near_miss | 다음 주기의 재허가를 프로세스 재시작으로 옮기면 A 공개→중단→재허가→A 재공개의 구조가 생긴다. | 관계가 있어도 동일성·시간 경계를 잘못 옮기면 P1을 위반한다. 실행 관측이 아닌 명시적 사용 방식의 논리 반례다. |
| P2-R3-04 `biology homologous recombination mismatch repair conflicting genetic information loss of heterozygosity` | C08 / RP2-C08: near_miss | 기존 가닥을 참값으로 놓고 다른 것을 오류로 제거하는 적용은 유효한 사용자 수정까지 없앤다. | 원 분야의 오류 제거 목적을 P2의 복수 의도 보존 목적과 맞바꾸지 않는다. |
| P2-R3-06 `epidemiology duplicate case records retain source reports reconcile discrepancies offline` | C07 / RP2-C07: surface_false_positive | 환자 동일인 판별·중복 record merge의 대상은 이미 같은 기록 ID에 속한 두 수정의 버전 충돌과 다르다. | 다른 분야 어휘로 바꾼 뒤 핵심 문제 자체가 달라진 실제 사례다. |
| P2-R3-07 `logistics disconnected inventory counts reconcile discrepancies preserve original counts audit trail` | C05 / RP2-C05-M: near_miss | GAO의 허용오차 이하 무조사 조정 관행을 작은 상충 수정 숨김으로 옮기면 보존·확인 조건을 위반한다. | C05를 독립 관측·차이 검토의 참고로 쓰는 양성 판정과 덮어쓰기 오용 판정을 분리한다. |

P1-R1-08의 `without central service`는 원문 P1이 요구하지 않은 질의 조건이다. [SEARCH_LOG.json](SEARCH_LOG.json)에 추가 제약임을 남겼으며 후보의 필수 탈락 기준으로 올리지 않는다. P2의 자체 운영 역시 선호를 필수 조건으로 바꾸지 않는다. 파일 내보내기는 내용에 관한 원문 요구이고, 모든 이력의 특정 형식 내보내기를 새 필수 조건으로 추가하지 않는다.

## 5. Q7 최소 설명의 6후보 교차 점검

RETRIAL §5에는 7개 원리군 설명을 완성했다. 여기서는 그중 6개의 정규화된 판정과 설명 요소를 교차 대조한다. 실제 설계자가 카드를 사용한 실험 결과가 아니다. 원 자료의 입증은 D1이며, P1/P2로 잇는 설계는 H다. 관계·연결·실패 조건은 기존 T축 안에 두고, 시간·규모·사람 가정은 설명 보충으로만 적었다.

| 원거리 후보·판정 | 관계와 소프트웨어 대응 | 필요한 연결과 실패 입력 | 원 분야 입증 수준·T축 밖 설명 |
| --- | --- | --- | --- |
| D01 제조 안전 interlock | reset/준비와 별도 start를 구분 → 복구 완료와 결과 공개 허가를 구분 | 입력 ID·영속 공개 상태·원자적 판정이 필요; 공개 직후 응답 전에 중단하고 같은 입력을 재전송 | 제조사 상태 계약; 자동 power-up 설정에 따라 다름. 인간 reset 확인을 자동 판정으로 바꾸는 근거를 별도 설명 |
| B03 / RP1-B03 의료 검사 결과 수정 | 원 결과와 수정 결과를 연결 → 원 공개본과 의도된 수정 버전을 구분 | retry와 의도된 새 버전의 동일성 경계 필요; 중단 후 같은 결과를 수정본으로 새로 공개하는지 확인 | 규정의 기록·수정 의무; 처리량이나 crash 내구성 실험이 아님. 법정 보존·사람 통지 가정을 그대로 제품 의무로 이식하지 않음 |
| B09 / RP1-B09 생물학적 복제 허가 | 복제 허가와 소비·재허가 감시 → 준비 상태와 한 번의 공개 허가를 구분 | 세포 주기가 아니라 입력/변환 버전 단위에 허가를 연결; process restart 때 초기화하면 반례 | 세포 실험의 관측·조작; 세포 주기 시간 척도와 소프트웨어 crash/retry 경계가 다름 |
| C01 / RP2-C01 약물 조정 | 여러 출처의 차이 발견과 의도 확인을 구분 → 충돌 탐지와 의미 해결을 구분 | 기준판·수정 ID·출처를 보존; 모르는 차이를 자동 LWW로 처리하면 수정 소실 | WHO의 절차 및 C02의 도구킷; 임상 담당자의 전문 판단·책임을 일반 팀의 자동 알고리즘으로 대체하지 않음 |
| C04 / RP2-C04 비평 판본 | 대안 읽기와 편집자 선택을 분리 → 두 수정과 현재 선택을 다른 객체로 표현 | 범위·기준판·수정 계보·저장 연결 필요; 선택 텍스트만 남겨 대안을 잃으면 반례 | TEI 인코딩 표준; 표기 구조가 동기화 구현을 입증하지 않음. 편집 권한과 다중 사용자 권한의 차이를 명시 |
| C05 / RP2-C05 물류 실사 | 독립 관측과 거래 이력으로 차이를 조정 → 독립 수정·기준판을 대조하고 해결을 새 결정으로 연결 | 양쪽 값·출처 보존, 물리수량의 참값 우선과 허용오차 삭제를 제외; 작은 차이를 숨기는 입력으로 확인 | 7개 선도기업 12곳의 관행 조사; 10/12곳 blind count. 물리수량의 단일 참값과 두 유효한 사용자 의도의 차이를 설명 |

Q7의 6후보에는 보조 근거 C02까지 총 7개 자료·7종류가 연결된다. 종류 수가 늘어도 설계자 실험의 부재를 메우지는 않는다.

## 6. 한계와 승인 전에 보존할 구분

모든 후보를 본문까지 읽은 것은 아니므로 미선택 결과의 적합성을 추정하지 않는다. 검색으로 관측한 D3와 후보 원문의 D1, P1/P2의 설계 연결 H를 구분하며, 대상 구현의 D4 성공은 주장하지 않는다. 방법·결과 확인 27개를 27개의 독립 재현으로 읽지 않는다. 순수한 추상화 수준의 효과, 전문 개발자의 원거리 원리 검색 수요, 설명 카드의 판단 개선, 선택적 주석의 경제성은 위 표의 최소 추가 확인으로 남는다.

내부 검토는 **내부 별도 검토**다. 사람 검토·원 분야 전문가 검증·독립적인 다른 모델 검증을 받았다고 부르지 않는다. 내용 검토에서 제기한 C05-M 양성/오용 설정 혼재와 빈 결과 screening 문구는 수정했고 최종 기계 점검에서도 확인했다. 검토 발견·수정 내역은 [internal-review.json](evidence/internal-review.json)에 보존했다.

## 7. 최종 기계 점검

**통과.** Q1–Q4·Q7·Q8의 각 행에 서로 다른 출처 종류가 2종 이상 연결돼 있고 반증 시도·관측 결과·남은 확인이 비어 있지 않다. Q5/Q6은 위 수치표와 실제 질의·반례로 실험 작업의 기준을 충족한다. 내용 판단은 문헌 대조와 내부 별도 검토이며, 아래 33개 기계 점검이 논문의 진위를 자동 입증한다는 뜻은 아니다.

| 검사 | 결과와 범위 | 실행 기록 |
| --- | --- | --- |
| 원문·필수 조건·사전 SCOPE | AF-RES-002 원문 2개와 필수 조건 등의 6개 원문 행이 정확히 같다. 사전 커밋 이후 SCOPE 내용 변경 없음. | verification-report의 P1_P2_verbatim / fixed_constraints_verbatim / SCOPE 검사 |
| 자료 최소조건·근거 경계 | 배경 본문47, 관측1, 동료심사30, 방법·결과27, 표현/시스템 1차18, 전이 원저자9·사례10. Q5 별도 본문24. ID/URL 중복·공통 필드 누락 없음. | source/count 검사 |
| 검색·판정·집계 | 웹64개 고유 문자열·조합당8개, native16계획/15유효·전체18시도. 24개 후보 자료가25판정에 연결되고 기존 T enum·필수 항목을 유지. 새7/표면8/근접3 원리군 재계산 일치. | query / T / comparison 검사 |
| 내부 검토 수정 | C05-M 오용 설정·위반 조건 일치, 미검증 결과가 빈 결과와 구별됨. 최초 날짜만 남은 E01–E16은 실제 재열람 시각을 추가하고 최초 날짜를 보존. | internal-review 및 source timestamp 검사 |
| 허용 경로·문서 링크 | 과제 경로 밖 변경0, 문서의 로컬 링크 누락0, git diff --check 종료0. | owned_path_only / local_document_links_exist / git_diff_check |
| 계약·의존·원격 신선도 | workbench.session check --fetch 종료0, status=passed, freshness=remote_checked. 시작 이후 통합 브랜치는 020c8d002cf782079053441368ed3e4a95b3289f로 이동했으나 계약 해시는 그대로이며 작업 source_commit을 바꾸지 않았다. | [session-check.json](evidence/session-check.json) |

기록 일관성 검사의 종료 코드는 **0**, 결과는 **33/33 passed**다. 검사 당시 Git HEAD는 `99c4698ef031eab80b5ba97afcafd385b397c415`이고, 그 위 작업 트리의 날짜·분류 flag·문장 설정 수정까지 검사 입력에 포함했다. 입력 파일별 SHA-256은 [verification-report.json](evidence/verification-report.json)에 있다. 자기 참조를 피하려고 SELF_CHECK/HANDOFF/검사 영수증 자체는 입력 해시에서 제외했다. 검사한 파일 집합의 집계 SHA-256은 `da78e4cf260fa64c9d1e73ef7fd67b974452b1000dc1c4738d982ebdf938fb7e`다. 이 수정들과 검사 코드는 자기 점검 묶음으로 커밋한다.

실행한 명령은 저장소 루트 기준이다.

```bash
python docs/workstreams/research/AF-RES-010/evidence/assemble_retrial.py --phase all
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-010/evidence/verify_research.py --output docs/workstreams/research/AF-RES-010/evidence/verification-report.json
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-010/manifest.json --fetch
```

`verify_research.py`는 외부 검색·제품 실행 없이 이미 남긴 원장의 관계와 경로를 검사한다. 논문 재현, 후보 설치, P1/P2 목표 적용(D4), 설계자의 설명 카드 사용 시험, 실제 유지 비용 계측은 수행하지 않았다.

### 공통 전체 검사 명령의 실행 범위

AGENTS.md의 아래 두 명령은 실행하지 않았다. `scripts/check.py`는 저장소 루트 `.workbench/`에 로그를 쓰고 acceptance 작업을 호출하며, `scripts/cloud_check.py`도 같은 경로에 실행 디렉터리와 영수증을 만든다. 이는 이번 사용자가 허용한 `docs/workstreams/research/AF-RES-010/` 밖 쓰기다. 검사기를 바꾸거나 범위 제한을 우회하지 않았고, 연구 자료 검사와 계약 검사는 위 명령으로 수행했다.

공통 경로 쓰기가 허용된 통합 작업에서 실행할 정확한 명령과 입력은 다음과 같다. 입력은 이 작업의 최종 브랜치 체크아웃과 `manifest.json`이며, 제품/공통 실행 검사를 이 연구의 완료 근거로 소급하지 않는다.

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/check.py --require-git
PYTHONDONTWRITEBYTECODE=1 python scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

SELF_CHECK를 커밋한 뒤 HANDOFF를 단독 커밋한다. 최종 원격 HANDOFF 본문 일치와 커밋되지 않은 파일이 없는지는 그 마지막 커밋 뒤에 확인한다.
