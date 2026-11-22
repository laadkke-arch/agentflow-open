# AF-RES-034 · 주장·반례·분모 자체 점검

상태: 통합 결과에 대한 내용 점검과 현재 원장 재계수. **최종 결과 커밋의 기계 검증, `session check --fetch`, 고정 원격 RESULT·수용 파일 재독 영수증은 아직 이 문서에 확정하지 않았다.** 아래 마지막 절의 예정 경로를 통합 담당자가 실제 대상 SHA·종료 코드·확인 범위로 갱신해야 한다. 중간 원장 커밋의 검사나 분담 작성자의 산술 확인을 최종 결과판의 검사로 대신하지 않는다.

이 문서는 조사 갈래가 직접 읽은 원문과 보존한 위치, 통합 결과, 추가 검토 기록을 연결한다. SELF_CHECK 작성자가 모든 소프트웨어 원문을 새로 독립 판독했다는 뜻은 아니다. 실제 사람 모집·연락·새 사용자 시험은 수행하지 않았다.

## Q1~Q8: 주장과 실제로 찾아본 반례

| 질문 | 주장 | 직접 읽은 근거 주소·위치 | 결론이 틀리는 조건 | 실제로 찾아본 반례·확인 결과 | 남은 미확인·다음 자료 |
| --- | --- | --- | --- | --- | --- |
| Q1 | 2005~2025년 문헌에서 핵심 일차 원문22편과 독립 내용 원산출물8개를 심사했다. 최소수30과 검색 반환 행수는 다른 분모다. 검색 종료일은2026-11-23 KST이며 실제 최종 조회 UTC는 최종 영수증에서 확정한다. 네이티브 색인의 전수 검색·완전 인용망은 주장하지 않는다. | [봉인 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/9a7d461ed8fd3fe57c2b4d29d8249b7c64e93eae/docs/workstreams/research/AF-RES-034/SCOPE.md) Q1/선정·중복 규칙;[초기 선정 봉인](https://github.com/laadkke-arch/agentflow-open/blob/5873c4b42d4a0fb362f024b3d1d76eb4a2ba5b1a/docs/workstreams/research/AF-RES-034/initial-selection.json);[Leahy2018 저자본](https://www.academia.edu/37014386/Overcoming_Design_Fixation_in_Idea_Generation) Methods36–50/Results51–70행(Xd-D01);검색·실패 원장은 attempts.jsonl과 screening.csv의 실제 반환 순서·판정 행. | 같은 참가자·실험을 독립 연구로 더했거나, 검색요약·부분열람·미러·일반 문서 파일을 적격 원문으로 올렸다면 최소수와 범위 판단이 틀린다. 미심사 후보에 적격 재작업 비교가 있으면 관측0의 범위도 바뀐다. | Leahy2018/2020의 N185·성별·연령·과제 일치와 절차 차이를 확인하고 중복 의심으로 보수적 제외. McLaren 선행판·EO/Bing 동반판을 새 사람 표본으로 세지 않았다. Seahawk는 사람 수행 부재로 제외. CHI2024 격자는 인접 자료로 보존하고 디자인3편에 넣지 않았다. | ACM DL/IEEE 네이티브 질의별 처음30개 전체는 확보하지 못했다. 초기 SW-B 보조7질의 순위 손실과, root 전방검색2건의 exact query/event UTC 미보존은 별개 약점이다. 다음은 보존된 정확 질의를 네이티브 export와 대조하고, 후기사건은 원 호출 인자 영수증이 있는지 확인하는 것이다. 접근 실패한 Prospector 저자본·선택 인용경로의 미심사 원문을 이어 읽되 URL 수를 논문 수로 바꾸지 않는다. |
| Q2 | 링크 표시, 목적·한계 설명, 실행 예제, 완전 풀이 및 도구 묶음을 분리했다. 비교 연구 대부분은 UI·코퍼스·훈련·입력 지원을 함께 바꾸므로 제품의 링크 단독 효과를 추출할 수 없다. 표시·열기·채택도 다른 사건이다. | [Strata](https://lxieyang.github.io/assets/files/pubs/strata-cscw-2021/strata-cscw-2021.pdf) pp23–26/Table2(Rt-S03);[Codelets](https://from.so/assets/pdfs/oney-codelets-chi2012.pdf) Evaluation pp4–6/Table1(Swa-09);[NCQ](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) §§7.1.5/10.4(Swb-P07);[McLaren](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf) pp90–93/Table2(Xl-02). | 동일 원문·동일 화면·동일 훈련에서 링크의 목적/근거 문구만 바꾼 비교가 확인되거나, 실제 열람·채택 로그가 노출과 같음을 입증하면 현재의 개입 분리 한계가 줄어든다. | Codelets는 대조군에도 직접 예제 링크가 있었지만 자동 삽입·builder·훈련 차이가 남았다. Strata는 같은 표/URL에서 추가 신호 묶음을 비교했다. NCQ의 Used/Run은 snippet 단위이고, 인접 CHI2024 Dropdown에서는37/61명이 추가 예시를 열지 않았다(Xd-04). 화면 표시만으로 사용을 추정하는 가정이 깨진다. | NCQ 지시문의 실제 참가자 제공판과 CodeMend 준비 notebook의 실제 사용판은 미확인이다. 첫 자료는 [NCQ 고정 instructions.md](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md)(Swb-A01)와 실험 당시 배포 기록, 그리고 원자료의 shown/opened/adopted 사건 정의다. |
| Q3 | 사람·과제·세션·배정군 행을 분리했다. 설계상 직접 비교16연구군, 간접/배정불명4, 대조 부재2이며 이를 제품 인과효과16개라고 부르지 않는다. 사전 경력과 특정 해법을 이미 아는지는 다르다. | [Acar](https://userlab.utk.edu/files/papers/kim/2016/acar2016you.pdf) §§IV–V/TablesII–IV(Swb-P03);[NCQ](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) §§7/10(Swb-P07);[Chan2011](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) p3 §3.2/Table1(Xd-01);[McLaren](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf) pp90/94–96(Xl-02). | 반복 과제를 독립 사람으로 세거나, 제외된 사람과 군별 탈락을 복원 없이 포함했다고 주장하거나, 균형 교차를 무조건 기억 오염 없는 비교로 취급하면 판단이 틀린다. | NCQ는20사람/40시행·baseline 항상 선행으로 Q. Acar는56참여→54분석/216시행이며 round-robin/random 서술 충돌로 Q. Chan 본문153 대 군표151, McLaren E1 ErrEx/TPS43·36 역전을 원문 렌더로 확인했다. Mica/Strathcona는 대조 부재를 유지했다. | Chan 실제 배정·완료 총수, McLaren 최초배정/군별 중단, 다수 연구의 특정 해법 사전 인지가 미확인이다. 다음 첫 자료는 해당 표의 정오표 또는 비식별 배정·제외 원장이다. McLaren은 열람 조판본과 최종 출판판 대조가 먼저이며 다른 CTAT 자료를 같은 코호트로 가정하지 않는다. |
| Q4 | 같은 종점의 시간 비교와 시간·공통 품질검사를 함께 보고한 연구는 있다. 완료자 조건부 시간, 고정 예산 품질, 전체 배정 효과, 품질 동등성은 구분한다. 공개 요약값으로 가능한 대비만 계산했다. | [Unakite](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf) pp8–10/Fig6(Rt-S01);[eXoaDocs](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) TablesX–XII pp19–22(Swb-P01);[Schwonke](https://www.academia.edu/17358375/The_worked_example_effect_Not_an_artefact_of_lousy_control_conditions) Table1 p261/Table3 p263(Xl-01);[McLaren](https://www.cs.cmu.edu/~bmclaren/pubs/McLarenVanGogEtAl-Efficiency%20of%20WE-CHB016.pdf) Tables3–4 pp94–96(Xl-02). | 미완료자의 소비 노동·오류·훈련·자료 작성비를 넣으면 시간차가 줄거나 뒤집힐 수 있다. 비유의 품질차를 사전 허용범위 없는 동등성으로 바꾸거나, 반복측정 공분산 없이 독립군 CI를 붙이면 과장이다. | Unakite2는 정답설명3개를 모든 조건에서 달성한 종점. eXoaDocs는 완료자 시간의 정확n 미공개. McLaren WE−PS 품질 CI는 E1[−5.76,+9.96]/101점,E2[−11.28,+7.88]로 손상 가능성을 배제하지 못한다. Schwonke E2 개념전이는 단측유의지만 자체 양측 CI가0을 포함하고 절차전이는−5.30pp[−22.95,+12.35]다. | 사람별 시작·종료·idle·중단 원자료가 없어 완전 재분석은 못 했다. 다음 첫 자료는 각 실험의 참가자×군×과제 event log와 채점표다. Unakite paired 공분산, eXoaDocs 시간표 사람 조인, McLaren 누락자/정확군n이 각각 어떤 CI·전체배정 효과를 바꾸는지 effects.csv에 명시한다. |
| Q5 | 첫 설계/해법 채택 뒤 실제 결정 철회와 수정 사람 노동을 대조군·관측창과 함께 측정한 비교는 핵심22연구군에서0이다. 절감량은0분이 아니라 미확인이고, 조건부 절감 계산은 해당 없음이다. | [Unakite](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf) p10 P3 사용 사례(Rt-S01);[Blueprint](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) printed519–521 배포로그(Swa-02);[Leahy](https://www.academia.edu/103094924/Design_Fixation_From_Initial_Examples_Provided_Versus_Self_Generated_Ideas) Methods/Results pp3–9(Xd-03);[Wesenberg](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1032003/full) Methods/Results의 immediate/delayed 검사(Xl-04). | 별도 후속 버전·작업 일지에 최초 채택 시점, 되돌린 결정, 같은 창의 대조군 수정 노동이 존재한다면 관측0은 바뀐다. 본 심사밖 연구의 부재까지 증명한 것으로 읽으면 틀리다. | Unakite1주 인터뷰는 사용 확인이지만 비교 수정시간 없음. REST 게시물 수정·CodeMend 연속 그래프 변경·Codelets 자기코드 재사용은 최초 과제. Leahy 고착은 유사성이고, McLaren 다회 수업/후검사와 Wesenberg 같은세션 말 delayed는 원해법을 다시 만드는 노동이 아니다. | 다음 첫 자료는 최초 채택 SHA와 후속 독립 품질 재검·수정 로그를 연결하는 자료다. 공개 연구에서는 해당 artifact의 버전 이력·보존 후속 제출 여부를 확인한다. 새 시험은 future-study.md의 submission/rework 표로 계획만 했으며 실행하지 않았다. |
| Q6 | 긍정 효과만 모으지 않고 시간 이득 소멸, 품질 반대 방향, 조건부 분모 역전, 고착과 전문성 상호작용을 찾았다. 서로 다른 조건의 반대 결과를 동일 처치의 재현 실패로 합치지 않는다. | [NCQ](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) §10(Swb-P07);[ExampleOverflow](https://alexeyza.com/pdf/Zagalsky.Alexey-MSc.pdf) Tables5.1–5.4(Swa-04);[Acar](https://userlab.utk.edu/files/papers/kim/2016/acar2016you.pdf) §V(Swb-P03);[Fu2013](https://edrl.engr.wisc.edu/wp-content/uploads/sites/142/2022/02/md_135_2_021007.pdf) pp6–9(Xd-02);[Reisslein](https://www.academia.edu/1126010/Encountering_the_expertise_reversal_effect_with_a_computer_based_environment_on_electrical_circuit_analysis) Tables1–2 pp99–100(Xl-03). | 순서·난도·자극거리·조건부 성공자의 차이를 통제하면 일부 반대 방향이 달라질 수 있다. 작은 표본의 넓은 CI를 효과 없음 또는 확정 악화로 읽으면 틀리다. | NCQ2 선택중앙−323초가 총중앙−2초로 축소. EO 평균총점차−1/4점이지만 CI[−2.56,+.56]. Acar 기능35/52 대21/52와 조건부 보안18/35 대18/21이 충돌하나 전체 안전기능은 양쪽18/52. Chan/Fu far의 방향은 반대지만 거리척도가 다르다. Reisslein 상호작용은 근접전이이며 시간·원거리까지 확장하지 않았다. | 긴 근거 때문에 느려졌지만 정확해진 제품 링크 직접 비교는 미확인이다. 첫 자료는 같은 내용·UI에서 설명 길이를 바꾼 참가자별 읽기/총시간/공통 품질의 원표다. 거리 반례는 같은 특허집합/거리 정의로 재분석해야 하며 현재 d값을 합치지 않는다. |
| Q7 | 산업·제품 디자인3원문과 학습과학4원문은 측정법을 옮길 근거다. 스케치 참신성·고착·교과 학습 시간의 효과크기를 제품의 링크·장기 노동효과로 옮길 수는 없다. | [Chan2011](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) pp3–10(Xd-01);[Leahy](https://www.academia.edu/103094924/Design_Fixation_From_Initial_Examples_Provided_Versus_Self_Generated_Ideas) 측정/결과/한계 pp5–9(Xd-03);[Schwonke](https://www.academia.edu/17358375/The_worked_example_effect_Not_an_artefact_of_lousy_control_conditions) pp259–264(Xl-01);[Reisslein](https://www.academia.edu/1126010/Encountering_the_expertise_reversal_effect_with_a_computer_based_environment_on_electrical_circuit_analysis) Methods/Table1–2(Xl-03);[Wesenberg](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1032003/full) Results/Limitations(Xl-04). | 여러 타당한 해법·통합 비용·보안·장기 유지보수를 가진 업무에서도 같은 종점과 조작이 성립함을 보인 전이 연구가 있다면 적용 범위가 넓어진다. 유사성=실패·초기 풀이학습=재작업이라는 전제가 필요하면 현재 전이는 성립하지 않는다. | 디자인에서는 제공 예시뿐 아니라 자기 최초 개념 고착을 확인했다. 먼 예시는 참신성을 높이거나 낮췄고 예상 build time은 실제 노동이 아니었다. 학습에서는 Reisslein의 작은 시간차·넓은 CI, Wesenberg의 부담/확신/학습점수 불일치를 확인했다. | 옮길 방법은 초기 개념ID·후속 산출물 관계의 독립 코딩, 사전지식 검사·단계별 시간·공통 채점이다. 옮기지 않을 것은 참신성 d나15~63% 학습시간 차이다. 다음 첫 자료는 실제 다단계 설계의 동일 요구 루브릭·초기제출/수정 이력이며, Design Heuristics 일반 교육폼을 실험 제공판으로 간주하지 않는다. |
| Q8 | 자유검색 대 목적·근거·한계가 붙은 링크를 동일 환경·과제·예산에서 비교하는 두 군 무작위 병렬 계획을 썼다. 사전지식·전체배정 분모·공통 품질·첫채택 후 재검·제공자 비용을 포함한 미시행 가설이다. | future-study.md §§1–6의 계획/수집표;[Strata](https://lxieyang.github.io/assets/files/pubs/strata-cscw-2021/strata-cscw-2021.pdf) pp23–26의 공통 기본표 비교(Rt-S03);[NCQ](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) §§7/10의 고정 순서·단계/총시간(Swb-P07);[Reisslein](https://www.academia.edu/1126010/Encountering_the_expertise_reversal_effect_with_a_computer_based_environment_on_electrical_circuit_analysis) pp94–100의 사전지식 층화(Xl-03). | 과제·검사 난도나 지원이 군별로 다르거나 기억이 다른 군에 전달되면 효과 해석이 깨진다. 첫채택자만의 수정시간, 빠른 포기의 검열, 숨은 요구를 늦게 추가한 수정, 자료 작성비 누락으로 전체 노동 가치를 과대평가할 수 있다. | 기존 연구의 완료자 선택·NCQ 순서혼입·Codelets 훈련 차이·교육 개입시간만 측정한 경계가 이 위험을 구체화했다. 계획에서 미채택자의 재작업을0분 성공으로 두지 않고 전원 최종품질/소비노동을 공동 판정했다. | 90/60분·7일·10분 사업차이·−5%p 비열등 경계·60명 탐색·가정상 약63명/군은 관측값이 아니다. 실제 과제 분산·통과율·오판비용·사전 합의가 필요하다. 첫 입력은 배정표·동일 루브릭·카드 고정본·중단 사건 코드북이며, 행정 상한과 조기 포기/실패의 분석 구분도 시행 전에 봉인해야 한다. |

## 현재 원장 분자·분모와 검증 방법

아래는 SELF_CHECK 작성 시 작업트리와 evidence/counts.json에서 확인한 집계다. **최종 고정 SHA에 대한 검산 영수증은 아니다.** 작성 도중 root의 기존 전방검색2건을 지연 기록한 `streams/root/attempts-forward-final.jsonl`이 추가되어 attempts/screening/고유 URL은 재집계 대상이다. 아래 초안201/1040/879를 고정 최종수로 인용하지 않으며, 통합 담당자가 최신 evidence/counts.json과 실제 최종 판에 맞춰 교체해야 한다. 원문30·연구군22·실험26에는 변화가 없다.

| 집계 | 현재 값 | 재계수·해석 규칙 |
| --- | --- | --- |
| sources.jsonl 전체 행 / 고유 source_id | 48 / 48 | 원장 행수다. D0·부분 열람·동반판·범위 밖/인접 원문도 있어 ‘전문48편’이라는 뜻이 아니다. access_level·count_minimum·minimum_decision을 함께 읽는다. |
| 최소수 적격 고유 외부 원문 | 30 | count_minimum=true만 합산: software_primary15 + design_primary3 + learning_primary4 + artifact8. 검색요약·미러·작성자 표는 더하지 않는다. |
| 핵심 일차 연구군 / 독립 실험 | 22 / 26 | 적격 일차 원문에서 study_family를 중복 제거하고, studies의 included_core=true 중 study_id를 다시 중복 제거한다. Unakite·NCQ·Schwonke·McLaren의 각2실험을 보존한다. |
| 설계상 직접 / 간접·배정불명 / 대조 부재 | 16 / 4 / 2 연구군 | 각 family 안에서 확인된 가장 강한 설계로 분류. R은 비교 설계이며 제품 링크 단독효과나 동등품질 인과절감의 보증이 아니다. |
| 실험 단위 설계 등급 | R19 / Q3 / U2 / O2 = 26 | 무작위·균형교차, 비무작위, 배정불명, 대조 부재를 분리한다. 가족 수와 실험 수를 혼용하지 않는다. |
| studies.csv 배정군 행 | 74 | 군별 전사 행수다. 사람 수를74로 세거나 people_enrolled 등 반복된 연구전체 수를 군행마다 더하지 않는다. |
| effects.csv 행 | 53 | 효과·계산불가·비시간 비교를 포함한다. 여러 대비/결과가 같은 사람을 공유하므로53독립 실험으로 세지 않는다. |
| attempts.jsonl 행 | 203 | 검색·본문 요청·실패·대체 경로·실행·인용 확인 기록이다. 최종값은 evidence/counts.json의 attempt_rows를 따른다. 요청횟수를 고유원문 수로 바꾸지 않는다. |
| screening.csv 행 / 비어 있지 않은 고유 URL | 1066 / 901 | 검색 반환과 전문 판정 행을 함께 포함한다. 최종값은 evidence/counts.json의 screening_rows와 screening_unique_nonempty_urls를 따른다. 반복 질의/URL/미러와 같은 연구의 별판을 제거하기 전 수이며 고유 연구 수가 아니다. |
| 링크만 바꾼 제품 직접 비교 | 0 | studies의 product_directness와 cochanges를 같이 판정한다. B/X를 L로 임의 변경하지 않는다. |
| 첫채택 뒤 재작업 노동 대조 비교 | 0 | 최초채택·같은 관측창·되돌린 결정·실제 사람 노동·대조군이 모두 필요한 기준이다. 절감량은 미확인, 조건부 산식은 해당 없음이다. |

통합 검증에서 source_id 중복과 source_ids→sources, study_id→studies, study_family→적격 연구군, 비교 ID→effects, 주장→원문 위치의 연결을 확인했다. evidence/validation.json에 실제 입력 해시와 검사 결과를 남긴다. 빈 study_id·claim_ids가 통과했다는 이유로 연결 완전성을 선언하지 않는다. SW-B 추가 검토에서 지적한 NCQ 코호트 매핑, 대표 시간·시행 열, 원보고 계수의 전사 누락을 수정했고 대표 열과 detail_json을 함께 검사했다. cross-domain 비시간6행과 Chan 충돌 분모도 대표 열에 올렸다(REVISIONS.md). 모든 효과는 원단위·사람/시행 분모·종점·시점·반올림 입력·공분산 부재를 확인하고 계산 불가의 이유를 보존한다.

## 원 산출물 8개, 엄격 하위집합 7개, 사람 시간 원자료 0개

공개 독립 내용의 기준으로 산입한8개는 CodeMend4(Rt-A01~04)와 NCQ4(Swb-A01~04)다. 과제/자극 준비 notebook2, 별개 자료집3, 원 분석/채점 절차2, 도구 조작 지시문1이다. 두 연구군의 자료이며8개 독립 사람 실험이 아니다. 같은 CSV의 포맷이나 notebook의 그림·cell을 쪼개 수를 늘리지 않았다. 별도 에이전트의 내용 재독은 streams/software-a/artifact-review.md에 있다.

가장 약한 연결은 [NCQ instructions.md](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md)다. 논문 §7.1.5의 제공 조작문서와 내용상 연결되지만 이 고정 commit의 문구가 당시 참가자 제공판인지는 미확인이다. 일반 조작문서를 제외하고 실험 전용 자료만 인정하는 민감도 기준에서는 **7개**다. 따라서 ‘공개 독립 원산출물8개’와 ‘정확한 실험 제공판8개’를 같은 수용 조건으로 쓰면 안 된다.

[CodeMend lab 준비본](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/user-study-prepare-0405.ipynb)은 bar의 마지막 변경이 hatch이나 논문은 shadow다. [crowd 준비본](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/mturk_data_prepare_0302.ipynb)은10후보 변경쌍이지만 논문은5쌍을 보고한다. 실제 제공판을 확인한 것으로 처리하지 않는다. CodeMend의 IR 관련3개는20명 lab의 시간자료가 아니다.

NCQ의 두 CSV는 실제 snippet 관측 자료이지만 참가자별 총시간·중단·최종정답 로그가 아니다. 연구1/2의 P1~P10 번호 재사용을 같은 사람으로 조인하지 않는다. 이8개 중 사람별 시작·종료·중단을 연결해 시간효과를 다시 계산할 공개 raw 자료는 **0개**다. Design Heuristics 공식 교육자료2개는 Leahy 실험과의 판·절차 연결이 확인되지 않아 최소수에서 제외했다.

## 실제로 확인한 불일치와 해석의 제한

| 원문/판 | 확인한 문제 | 보존한 처리와 다음 최소 확인 |
| --- | --- | --- |
| Xd-01 Chan2011 p3 | 본문153명과 Table1 아홉 군 합151명 불일치. 최초 자체검산 뒤 PDF 렌더로 확인 | 군 값을 임의 증보하지 않고 확정 총배정/완료를 null로 둠. 원보고153과 표합151 모두 보존. 정오표/원배정표가 다음 자료다. |
| Xl-02 McLaren 열람 조판본 pp90/94–96 | E1 ErrEx/TPS n이43/36 대36/43로 뒤바뀜. E2 설문N135 대 본문115도 충돌. 첫쪽 Available online xxx | WE/PS 일치 분모만 CI 계산, 충돌 군이 든5대비 CI 보류. 최종 출판판 접근 실패를 남기고 저자판 내부의 충돌로 한정. 최종판·선행 학회판·정오표 대조가 먼저다. |
| Xd-03/Xd-D01 Leahy2020/2018 | 표본 세부는 일치하나85/95분·생성25/30분·자기평가/독립코딩 설명이 다름.2020 안에도 개념 총수/pooled 고착값 불일치 | 같은 코호트 의심으로 중복 제외하되 동일성을 확정하지 않음. 군별 n 없는 효과의 CI와 모순된 후반 집계는 만들지 않음. 실험일·원자료ID·실제 프로토콜이 다음 자료다. |
| Rt-S03 Strata Table2 | Deep 고품질 이유6.9와 정답목록11을 나누면62.73%이나 recall64.5%로 기재 | 해당 품질셀의 정확 효과는 미확인. 원 PDF 렌더 확인과 원보고값을 보존하며 개인별 채점표/정오표가 필요하다. |
| Swb-P03 Acar 배정·조건부 분모 | Methods의 round-robin과 Results의 random 서술 충돌. 기능성공에 조건부인 보안 분모 | Q로 분류. 전체 안전기능18/52 동률과 조건부 차이를 분리하고 동률을 등가성 증명으로 쓰지 않음. 원배정/제외 기록이 다음 자료다. |

검색 범위의 약점도 원문 오류와 별개다. ACM DL/IEEE 접근 실패를 저자본·기관본·공개 웹 venue/site 질의로 보완했지만 네이티브 색인의 정렬된 전건을 확보했다고 쓰지 않는다. 주요 일반/반대 질의는 각각 다시 실행해 실제 반환을 기록했으나 초기 보조 검색 순위 손실은 소급 재구성하지 않았다. 후방·전방은 연구군별 **선택한 한 단계 경로**이며 완전 인용망이 아니다. 한 경로가 확인되지 않았으면 인용 간선을 철회하거나 미확인으로 남겼고, 접근 실패를 무효 효과로 세지 않았다.

후기 기록의 약점은 따로 남긴다. `ROOT-FORWARD-CODEMEND-LATE-RECORD`와 `ROOT-FORWARD-STRATA-LATE-RECORD`는 이미 실행되고 Rt-C01/Rt-C02로 이어진 전방검색의 보존된 출력에서16개/10개 반환 메타데이터를 뒤늦게 저장한 것이다. 로그 시각은2026-11-22T16:25:48Z이지만 **원래 정확한 질의 문자열과 실행 UTC는 보존되지 않았다**(`queries=null`, `event_utc=null`). 새 검색·새 고유원문으로 세지 않으며, 로그 시각을 실행 시각으로 대신하지 않는다. 이는 네이티브 색인 포괄성 부족이나 초기7질의 순위 누락과 다른 출처 추적 한계다. 다음 최소 확인은 원 tool 호출 인자/실행 영수증의 잔존 여부이며, 없으면 추정해 채우지 않는다.

## 검토의 독립성과 실제 수행 범위

| 검토 종류 | 수행 범위 | 주장하지 않는 것 |
| --- | --- | --- |
| 조사 갈래별 직접 원문 판독 | 소프트웨어A/B,교차 분야,통합 담당의 원문·표·프로토콜 판독과 출처 원장. 접근 단계와 위치를 source별 보존 | 모든 source48행이 동일 깊이의 전문 심사를 통과했다는 주장 |
| 작성자와 다른 AI 에이전트의 추가 재독 | SW-A가 통합자가 선정한 원산출물8개의 실제 내용·모 논문 연결·행수/해시를 추가 확인. 각 final-review는 지정 분야의 통합표와 원장을 대조 | 독립 인간2명의 맹검 코딩, 전 분야 모든 연구의 독립 이중 추출, 원 사용자 시험 재현 |
| 동일 작성자의 자체 재검·계산 | 분담별 산술 확인, 교차 분야17대비 계산·ID/분모 재계수, Chan/McLaren PDF 렌더 재확인. 교차 분야 원장과 통합 숫자17대비의 전사 일치도 점검 | 동일 자료를 다시 계산한 것을 새로운 사람 관측이나 독립 효과 재현으로 부르는 것 |
| 독립 사람 판독/새 사람 시험 | **수행하지 않음** | 사람의 독립 판정 합의도·참여자 반응·현장 재작업 효과를 만들어 보고하는 것 |

중간 검토에서 Codelets PartB의 선택된10+4명·동일도구 조건, Blueprint의 URLLoader/차트 과제 분리, Schwonke E2의 Table3 위치, 학습시간 경계, SW-B 통합 대표 열 누락을 지적했다. 수정안과 당시 작업트리 해시는 각 streams의 final-review.md에 있다. 이 사실을 최종 원격판에서 모든 수정이 완료됐다는 영수증으로 바꾸지 않는다. 최종판 재독은 아래 별도 단계다.

## 통합 검산과 결과 고정 뒤의 영수증

| 단계 | 작성 시 상태 | 예정 영수증/확인 대상 |
| --- | --- | --- |
| 통합 원장 ID·중복·분모·산식·필수 표 구조 검증 | 통합 검사91개·수치 검사64개, 별도 비시간3대비·EO CI 재계산 포함, exit0. 고정 전 입력판 검증 | evidence/validation.json. 입력 파일 해시·실제 명령·종료 코드·검사 범위와 한계. 검산 당시 HEAD는 관측 묶음이며 통합 입력 해시를 별도로 기록한다. |
| 조건별 수용 판정 | 조건별 수용 파일 작성·현재판 조인과 산식 확인; 출판 후 단계는 별도 완료 영수증에서 확정 | evidence/acceptance-evidence.json. 조건별 met, 파일/행, 8대7 민감도·검색 포괄성·시간raw 부재·다음 최소 확인을 분리한다. |
| 소유 경로·의존 SHA 검사 | **최종 인계 전 실행 예정** | `python -B -m workbench.session check docs/workstreams/research/AF-RES-034/manifest.json --fetch`; 실제 영수증은 evidence/session-check.json 및 HANDOFF에 연결한다. 명령을 적었다는 사실은 실행 성공이 아니다. |
| 고정 결과의 원격 재독 | 중간 원장 `f31b498c56dc9f06f76a163d0601280df0704f7a`는 결과판과 다름. **최종 결과 원격 재독 예정** | 최종 결과 SHA의 RESULT.md·수용 파일을 GitHub에서 다시 읽은 실제 URL·UTC·파일 해시/확인 범위를 evidence/remote-reread.json과 HANDOFF에 남긴다. |
| 최종 HANDOFF | 위 단계의 실제 상태를 반영한 뒤 마지막 커밋 예정 | 결과 SHA·경로·확인 범위·미충족·색인 한 줄·재개 첫 자료·검사 영수증·중요 약점3개를 기록한다. 미완료 검사를 완료했다고 쓰지 않는다. |

이 SELF_CHECK는 결과 고정 전 내용 검증판이다. 이후 출판 단계의 완료는 evidence/acceptance-finalization.json과 HANDOFF가 보완하며, 이 판의 미래 단계 문구를 수행 완료로 소급 해석하지 않는다.

현재 의미 판단은 **REVIEW_READY_WITH_GAPS**다. 공개 원문 최소수는 정해진 독립 내용 기준에서 충족하지만, 엄격 산출물 하위집합7·네이티브 검색 포괄성·정확 실험판·개인별 시간 원자료·제품의 후속 재작업 효과는 별도로 남는다. 양성 연구 수가 많아졌다는 이유로 이 빈칸을 채우거나 검색 종료를 정당화하지 않는다.
