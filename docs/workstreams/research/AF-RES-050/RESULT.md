| 연구군·층 | 과제·배정 단위 | 링크·설명의 차이 | 배정 인원·시행 | 시간 시작·종료·단위 | 품질 기준 | 원자료 URL·파일·키 | 연결된 행/대상 행 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S01 NCQ · 주표본 · J-NA-01/02/03 | 두 별도 실험; 동일인이 서로 다른 두 Node.js 과제; baseline 먼저 | 실험1 공통 REPL 검색 off/on; 실험2 VSCode+웹 대 NCQ 전체. 후보·순위·편집·실행도 다름 | 실험별 분석10명×2=20시행. 실험2 모집 계보 예약14·성공 세션10·중도 철회4 | 시작→첫/최종 package 설치; 시작→명세 충족, 초. 과제20분은 계획값 | 실행 가능한 명세 충족 JS; snippet Runs?는 최종 검사 아님 | [고정 repo](https://github.com/Brittany-Reid/node_code_query/tree/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study), codesnippets1/2.csv의 P,T,Used?,Runs? | snippet142/156→각20 P×T그룹; 시간×배정×최종품질 join 미확인/각20 대상시행 | T→조건·문제·순서 코드북, 시간·제출·최종점수, 철회 단계, 강제 cap |
| S02 eXoaDocs · 주표본 · J-NA-04 | Java SQL 네 순차 과제; 숙련도4층 안 독립 무작위 배정 | JavaDocs 대 채굴·선정·요약 예제와 인기도. 대조에도 일부 수작업 예제 | 24명,12/12; 예정 사람×과제96슬롯 | 다음 관련 문서를30초 초과 본 전환으로 추론한 누적 분:초. 전체40분 | 제출 코드의 기능 검사 pass/fail | [논문](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) §5 Tables X/XII; keyed export 미발견 | 시간×통과 join 미확인/예정96; 시간 셀 포함자 n도 미확인 | 개인·과제 키, 시간 포함 지시자, 오답/미제출/timeout 구분, 실제 제출 시각 |
| S03 Blueprint · 주표본 · BC-J01/02 | 독립군 directed URLLoader 과제와 exploratory chart 과제; 무작위 방식 미확인 | Blueprint군 browser 금지; 대조 Firefox+Adobe Community Help. 검색·미리보기·복사와 허용 자원 차이 | 20명,10/10; 각 과제20시행 | 시작→첫 paste/완료, 초. directed600초; exploratory 고정900초 | 독립 엔지니어 코드 순위; 별도 디자이너 차트 순위 | [논문 p518/Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), [학위논문 Fig5.4](https://hci.stanford.edu/publications/2010/brandt-dissertation/brandt-dissertation.pdf); 안정적 개인키 없음 | 그림20/20 위치의 paste↔완료상태; 최종품질까지 joint join 미확인/20 directed | endpoint별 정렬 그림의 개인 대응, exact time, 코드/채점 원행, 판정자 가림·신뢰도 |
| S04 CodeMend · 주표본 · BC-J03/04 | 동일20명, bar/pie에 조건 하나씩; 각3부분과제 | 동일 환경 Google-only 대 CodeMend+Google; 자연어 질의·API 추천·수정 묶음 | 20명×2과제=40; 예정 부분과제120,조건별60 | 부분과제 초; 정확한 시작·종료·cap 미확인 | 부분과제 기능 충족 수; 전체 수정품질과 분리 | [논문](https://cond.org/codemend.pdf), [고정 repo](https://github.com/ronxin/codemend/tree/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d); eval-gt-2.csv는 case_study_no,answer,query,query_source | IR361행→완전행키360; 사람 join 미확인/예정120부분과제 | 실제 세션 로그·순서·미도달/실패 구분·시간 포함 n; IR표는 참가자표 아님 |
| S05 Unakite · 주표본 · J-US-01/02/04 | E1 독립 무작위20명×2공통과제; E2 별도16명 교차·순서 균형 | E1 같은 페이지에서 Unakite 대 Docs; E2 사전 비교표·snippet 대 동일 출처 페이지 묶음 | E1대상40,군별 n미확인; E2대상32. 전원 Unakite 자가과제는 비교 제외 | E1상호작용/총시간 비율; E2세 번째 타당한 이유까지 초 | E1표 완성; E2연구자 gold 중 이유3개 | [논문](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf), [공식 구현](https://unakite-v2.firebaseapp.com/static/js/main.bb8e5ba3.js.map) taskId,eventAuthorId,timestamp | 참가자 join 미확인/40·32; 구현 스키마만 열람 | 실제 배정·영상코딩·gold·시간행, 당시 배포판, 총 활동시간; E1훈련 비대칭 |
| S06 Strata · 주표본 · J-US-03/AGG | 독립 무작위20명; Python/Deep/Cloud3과제 순서 무작위 | 같은 Unakite 표·링크에 문맥·신뢰·이력·대안 기능 묶음 on/off | 대상60; 군별 n미확인 | 이유 평가→완료/진행불가,정확 계측 원점 미확인;600초 cap; 양군10분 훈련+연습 | gold 기반 고품질 이유와 조건 가림 유효성 판정 | [논문](https://lxieyang.github.io/assets/files/pubs/strata-cscw-2021/strata-cscw-2021.pdf), [arXiv 제작자료](https://arxiv.org/src/2102.06231v2); chart1.xml의 조건×과제 | 발표용 집계6/6 연결; 참가자 join 미확인/60 | 외부 참조 CSCW 2020 Participants Tracking.xlsx 누락; 시간·배정·채점 원행; 품질 표/그림 불일치 |
| X01 Chan2011 · 분야 대조 · J-RT-01 | 설계 유추 거리×흔함×그림/텍스트와 무예제; 좌석 폴더 배정 | 예제의 원리·내용·표현이 바뀜; 동일 링크 설명만 비교 아님 | 본문153명 대 Table1합151 불일치; 개념1321→기능조건1066 | 고정10분×3단계; 가변 완료시간 아님 | 두 채점자의 품질·독창성·수량 등; 제품 완성 검사 아님 | [논문](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) Tables1/2; 실제 자극 특허2건 별도 확인 | 사람/개념/채점 join 미확인; 사람분모151/153 미해결 | 원 과제 packet, 참가자 배정과 탈락,255제외 개념의 키, 후속 구현·재작업 |
| X02 Schwonke2009 · 분야 대조 · J-RT-02/03 | 독립 무작위 E1 25/25,E2 15/15; 기하 tutor7문제 | 풀이 단계 제시 후 점차 제거 대 모든 단계 직접 풀기; 양군 원리 설명·힌트·피드백 | E1예정350·E2예정210 사람×문제; 별도 코호트 | 학습단계 분; 약90분 세션과 다름 | 즉시 절차·개념 사후검사 | [논문 저자본](https://www.academia.edu/17358375/The_worked_example_effect_Not_an_artefact_of_lousy_control_conditions), [프로젝트](https://learnlab.org/mediawiki-1.44.2/index.php?title=Does_learning_from_worked-out_examples_improve_tutored_problem_solving%3F), DataShop후보77/78 | 실제 transaction/score join 미확인/예정350·210 | 77/78의 코호트 대응·공개 export·2006코드북·사후점수 키; 고정 코호트 지연검사 |

| 연구·비교 조건 | 비교 가능 단위·분모 | 선택시간 | 총 과제시간 | 활동시간 | 품질·실패·제한시간 | 추정치·불확실성 또는 미산출 이유 | 반증·근거 주소 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O-NA-01 NCQ E2 VSCode+웹→NCQ · 저자 집계 | 같은 분석10명,다른 과제·고정 순서 | 최종 설치 중앙값380→57초 | 별도 종점 | 미확인 | 분석자 명세 충족; 철회4명 위치 미확인 | 034배경; 주변 중앙값 차이를 개인별 짝 차이로 바꿀 수 없음 | [NA-001 §10.2](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf), J-NA-02/03 |
| O-NA-02 같은 E2 · 저자 집계 | 같은 분석10명 | 별도 종점 | 중앙값849→847초 | 미확인 | 20분 강제 cap 미확인 | 선택 이득을 총시간에 적용 불가; raw 시각/과제키 없어 짝 CI 미산출 | [NA-001 Fig20/21](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) |
| O-NA-03 NCQ E1 Basic→Retrieval · 저자 집계 | 같은 분석10명,다른 과제·고정 순서 | 별도 종점 | 중앙값936→748초 | 미확인 | 분석자 명세 충족 | 034배경; 순서·문제 보존 재추정 불가 | [NA-001 §7.2](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) |
| O-NA-04 JavaDocs→eXoaDocs T1 · 저자 집계 | 완료자 조건부; 시간 셀 n미확인 | 미확인 | 문서 전환 누적평균14:40→8:53 | 미확인 | 전체4과제40분; 통과행과 미연결 | 저자90% CI: 대조[10:44,18:37],개입[4:29,13:16]. 군별 구간이며 차이 CI 아님 | [NA-002 TableX/p21](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf), NA-002-CI |
| O-NA-05 같은 조건 T2 · 저자 집계 | 완료자 조건부;n미확인 | 미확인 | 누적평균25:03→23:34 | 미확인 | 전체40분 | 실제 제출시간·전체 배정자 평균 미산출; 과제2단독 소요도 아님 | [NA-002 TableX](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-06 같은 조건 T3/4 · 저자 집계 | 완료자 조건부;n미확인 | 미확인 | 누적평균32:03→30:32 | 미확인 | 두 과제 시간 분리 불가;전체40분 | 공통 문서 때문에 같은 완료 proxy; 사람별 품질/시간키 없음 | [NA-002 TableX](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-07 같은 조건 네 과제 모두 통과 · 저자 집계 | 독립 배정12/12 | 미확인 | 개인시간 미확인 | 미확인 | 대조1/12→개입3/12;비통과11/12→9/12;40분 | 허용식3/12−1/12; 틀림/미제출/timeout 분리와 층별 불확실성 미산출 | [NA-002 §5.3.2/TableXII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-08 같은 조건 T3 통과 · 저자 집계 | 독립 배정12/12 | 미확인 | T3/4분리 불가 | 미확인 | 대조4/12→개입3/12 | 반대 방향; 허용식3/12−4/12. 예제 사용과 정답은 다름 | [NA-002 TableXII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) |
| O-NA-SNIPPET1 NCQ공개 CSV1 · 공개행 기술통계 | 142snippet,20 P×T그룹 | 시각 없음 | 시각 없음 | 미확인 | Used?/Runs?;최종점수 아님 | 정확 중복0·키 null0; 조건 코드북 없으므로 조건 효과 미산출 | [NA-003-CSV1](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets1.csv), J-NA-01 |
| O-NA-SNIPPET2 NCQ공개 CSV2 · 공개행 기술통계 | 156snippet,20 P×T그룹 | 시각 없음 | 시각 없음 | 미확인 | 사용했지만 Runs?=0인 행 등 관측 | 정확 중복0·키 null0; T2를 NCQ로 가정하면 안 됨 | [NA-003-CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv), J-NA-02 |
| BC-O01 Control→Blueprint directed 첫 paste · 저자 집계 | 독립 배정10/10,모두 paste | 평균121→57초 | 별도 종점 | 미확인 | 이후3명 미완료 포함 | 첫 paste는 후보 채택/정답/완료 보장 아님; 안정적 품질키 없음 | [BC-01 Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), BC-J02 |
| BC-O02 같은 조건 directed 완료시간 · 저자 집계 | 완료자 대조8·개입9;원배정10/10 | 별도 종점 | 완료자 평균479→346초 | 미확인 | 600초;미완료2→1명 | 전원 순위검정p=.14를 완료자 평균차 CI로 쓰지 않음 | [BC-01 p518 Directed Results](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| BC-O03 같은 조건 directed 제한 내 완료 · 저자 집계/그림 판독 | 원배정10/10 | 모두 paste | 개별정확값 미복원 | 미확인 | 600초 내8/10→9/10 | 그림20위치와 완료상태 연결; 실패 포함 평균은 미산출 | [BC-01 Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), BC-J02 |
| BC-O04A 같은 조건 directed 코드 품질 · 저자 집계 | 독립군 과제별 순위;개인키 없음 | 별도 종점 | 품질과 미연결 | 미확인 | 엔지니어 코드 순위,600초 | 저자p=.02; 점수/시간 joint 효과나 동등성 아님 | [BC-01 p518 Directed Results](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| BC-O04B Control→Blueprint exploratory 차트 품질 · 저자 집계 | 독립군10/10 | 미확인 | 고정900초 예산 | 미확인 | 디자이너 순위합116→94 | 저자p=.21; 비유의가 동등품질 증거 아님; 완료시간 종점 없음 | [BC-01 p518 Exploratory Results](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| BC-O05 Control→CodeMend 부분과제 시간 · 저자 집계 | 같은20명;실제 시간 포함 시행 n미확인 | 미확인 | 부분 평균134.12→108.70초;전체 아님 | 미확인 | cap/미도달·실패 시간 포함 미확인 | 예정60/조건을 시간표 n으로 쓰지 않음; 과제/순서 짝 재구성 불가 | [BC-02 Evaluation](https://cond.org/codemend.pdf), BC-J03 |
| BC-O06 같은 조건 부분과제 완료 · 저자 집계 | 예정60기회/조건;실제 시도 n미확인 | 미확인 | 부분시간과 미연결 | 미확인 | 완료41→46;잔여19→14는 미도달/미완료 혼합 | 예정기회 기준 완료만 기술 가능; 미시도 전부 오답으로 처리 금지 | [BC-02 Evaluation](https://cond.org/codemend.pdf), BC-J04 |
| BC-O07 Blueprint/CodeMend 활동·재작업 · 식별 불가 | 각 독립군/동일인 설계별 추적 필요 | 미확인 | 전체 수정시간 미확인 | 미확인 | 후속수정·재검사 미확인 | 공개 IR표와 구현 score는 사람 노동/품질 측정치 아님 | [BC-05 repo](https://github.com/ronxin/codemend/tree/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d) |
| O-US-01 GoogleDocs→Unakite E1 · 저자 집계 | 독립20명,40공통시행;군별 n미확인 | 별도 측정 없음 | 절대초 미확인 | 전체 노동 미확인 | 표 완성;독립 품질루브릭 미확인 | 상호작용/총시간44%→25%;분율 감소를 절감초로 환산 불가 | [US-01 p8](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf), J-US-01 |
| O-US-02 동일 출처 페이지→Unakite표 E2 · 저자 집계 | 별도16명 교차,32시행;과제/순서 보존 필요 | 별도 측정 없음 | 세 번째 타당한 이유 평균332.56→114.63초 | 미확인 | gold 중3이유 문턱;cap미확인 | 공통 제한 품질문턱은 있으나 코드 수정·전면 품질 동등성 아님 | [US-01 p9](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf), J-US-02 |
| O-US-03 Unakite→Strata · 저자 집계 | 독립20명,60시행;군별 n미확인 | 별도 측정 없음 | 이유 평가 평균432.7→292.1초 | 미확인 | 전원3과제600초 내 완료 진술;전원 정답 아님 | 무효 이유 생략≠0; 참가자별 품질/시간키 없음 | [US-02 §6](https://lxieyang.github.io/assets/files/pubs/strata-cscw-2021/strata-cscw-2021.pdf), J-US-03 |
| O-US-04 Strata recall 제작자료↔본문 · 공개 집계 연결 | 조건×과제6집계,개인 아님 | 해당 없음 | 해당 없음 | 미확인 | XML캐시6개↔TeX6개 | join6/6,유일키6,미연결0; 새 실험효과 아님 | [US-11 chart1.xml/main.tex](https://arxiv.org/src/2102.06231v2), J-US-AGG |
| O-US-05 Strata 품질 값 감사 · 불일치 판정 | 같은 출판 집계의 판 대조 | 해당 없음 | 시간과 미연결 | 미확인 | Python/Strata precision 표90.1%·그림91.0%;Deep recall 관계 불일치 | workbook/이유별 원점수 없으므로 어느 값을 참으로 정정할지 미확인 | [US-11](https://arxiv.org/src/2102.06231v2), main.tex802/848/850·precision-chart.svg |
| O-RT-01 Chan 먼/가까운 유추 등 · 저자 집계 | 사람분모153/151불일치;개념1321/1066 구별 | 미확인 | 고정30분 단계 | 미확인 | 먼 유추 독창성↑·수량↓;최종 제작검사 없음 | 시간절감 미산출;255제외는 개념이지 참가자 아님 | [RT-P01 Tables1–2/결과](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf) |
| O-RT-02 Schwonke E1 직접풀이→예제 · 저자 집계 | 독립25/25,예정350문제 | 미확인 | 학습 평균35.4→30분 | 미확인 | 즉시 절차·개념 검사;비유의≠동등성 | 약90분 세션·지연 전이와 분리;score/transaction join 미확인 | [RT-P02 Experiment1](https://www.academia.edu/17358375/The_worked_example_effect_Not_an_artefact_of_lousy_control_conditions), J-RT-02 |
| O-RT-03 Schwonke E2 직접풀이→예제 · 저자 집계 | 별도 독립15/15,예정210문제 | 미확인 | 학습 평균39.2→30분 | 미확인 | 즉시 검사;E1과 다른 도입·카드·think-aloud | 코호트/훈련 합쳐 평균 금지;고정 코호트 지연검사 미확인 | [RT-P02 Experiment2](https://www.academia.edu/17358375/The_worked_example_effect_Not_an_artefact_of_lousy_control_conditions), J-RT-03 |

## 판정과 읽는 방법

**부분 인계.** 고정8군을 모두 유지하고 논문→공개자료 경로→실제 필드 또는 실패 위치를 판정했다. 그러나 배정·시간·최종 품질을 같은 사람×과제 단위에 연결하여 새 시간–품질 효과를 계산할 수 있는 고정 연구군은 **관측0/8**, 소프트웨어 주표본만은 **관측0/6**이다. 이는 효과가0이거나 원자료가 전 세계 어디에도 없다는 뜻이 아니다. 미확인 join의 행수를0으로 대체하지 않았다. 원문과 독립 공식 자료25개를 실질적으로 읽었지만 요구된 층별 배당은 **17/24**라서 완전 충족을 선언하지 않는다.

표의 화살표는 대조→개입이며 인과 효과의 새 추정치라는 뜻이 아니다. 저자 집계 수치는 034의 고정 배경과 원문 정의를 연결하기 위해 제시했다. 034의22군 숫자 재계산,046의PR시각 추정,038의합성답 재채점은 하지 않았다. 분야 대조 X01/X02와 선정되지 않은 후보는 소프트웨어6군 분모에 합치지 않았다. 보강 연구군은0개다.

ID는 연구 S/X, 출처 NA/BC/US/RT, 연결 J/BC-J, 결과 O/BC-O로 유지한다. [sources.jsonl](sources.jsonl)은143개 직접 열람·중복·탐색·실패 기록을 분리한다. [evidence/line-index.json](evidence/line-index.json)은 모든 ID의 파일·논리행·물리줄 대응이다. `관측0`은 실제 센 수가0일 때, `미확인`은 필요한 관측을 얻지 못했을 때 사용한다. 분모0의 조건부 비율은 산출하지 않고 `해당 없음`으로 남기는 규칙을 적용한다.

## Q1 · 무엇이 실제로 바뀌었는가

**확인된 사실:** 여섯 소프트웨어군 어디에서도 동일 후보 링크에 설명 문구 하나만 더한 인과 효과를 분리할 수 없었다. NCQ는 검색을 켜거나 전체 작업환경을 바꾸고, eXoaDocs는 예제 채굴·선정·요약·인기도를 함께 바꿨다. Blueprint는 browser 허용 자체가 달랐다. CodeMend는 추천과 코드 수정 흐름이 함께 바뀐다. Unakite는 자료의 표현·구조화·클리핑 기능, Strata는 문맥·신뢰·이력·추가 대안 기능 묶음을 바꿨다. 같은 출처를 통제한 Unakite/Strata도 설명 한 요소만의 비교는 아니다. [NA-001 §7.1/10.1; NA-002 §5; BC-01 p518; BC-02 Evaluation; US-01 pp8–9; US-02 §5.4/6.1]

설계도 구별했다. NCQ는 사람 내 비교지만 baseline→NCQ 고정 순서여서 학습/기간과 조건이 분리되지 않는다. Unakite E2와 CodeMend는 사람 내 조건 비교여도 서로 다른 과제이며 과제·순서를 보존해야 한다. eXoaDocs·Blueprint·Unakite E1·Strata는 독립군이므로 조건별 사람을 임의로 짝지을 수 없다. NCQ의 과제 조합 균형은 순서 균형을 뜻하지 않는다. Strata의 과제 순서 무작위도 처치 교차를 뜻하지 않는다. [J-NA-01~04; BC-J01/03; J-US-01~03; RT-M02]

훈련은 분석 밖의 공짜 시간이 아니다. Unakite E1은 개입군이 비교 전에10분 소개와5분 연습을 받지만 대조군은 공통과제 후에 받는다. Strata는 양군10분 훈련+연습이며 NCQ10분은 계획값이다. Schwonke E1/E2의 도입·예비활동도 다르다. 실제 열람·채택량은 배정 후 참가자 선택이므로 많이 읽은 사람만 비교하면 원 배정 효과와 다른 질문이 된다. 현재 공개행으로 이런 선택을 보정하지 않았다. [US-01 pp8–9; US-02 §6.1; NA-001 §7.1; RT-P02 방법]

## Q2 · 어떤 키가 실제로 연결되었는가

**NCQ:** 고정 SHA `ce14f193f7014c120f04619826cb251818d99b0e`에서 실제 CSV 두 개를 파싱했다.142/156행, 각각10가명·20개 P×T그룹, P/T null과 완전행 중복은 각각 관측0이다. P×T는 snippet에1:N이므로122/136추가행을 오류 중복으로 삭제하면 안 된다. CSV1의 빈 snippet/flag 한 행도 유지했다. 멀티라인 CSV의 논리행과 물리줄을 나눠 기록했다. T값1/2를 조건이나 논문의5개 문제로 매핑하는 코드북이 없다. `T2=NCQ`를 가정할 때 CSV2의68행과 논문의81snippet이 달라지는 점은 그 가정을 검증할 이유이며 확정된 논문 오류는 아니다. [J-NA-01/02; NA-003-CSV1/2; streams/ncq-exoa/ncq-row-audit.json]

원 참가자 가명·코드·행 전문을 제출물에 복사하지 않았다. 자체 예시 `NA-C2-trial-label-2`는 CSV2 논리17행/물리126–127줄의 `Used?=1,Runs?=0`을 가리킨다. 선택한 두 T-label의 같은 원 가명에만 같은 자체 ID를 부여했지만, T-label의 조건 의미는 여전히 미확인이다. 양 조건의 시간–품질 관측 예시는 이 파일로 만들 수 없다. [J-NA-02의 examples; O-NA-SNIPPET2]

**CodeMend:** 고정 SHA `445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d`의206트리 항목·3커밋 트리·1브랜치와 릴리스 경로를 확인했다. `eval-gt-2.csv`는361데이터행/360완전행키, 물리163–164줄에 정확중복1쌍이다. 네 열은 검색 질의 평가용이다. XLS는 질의×모델 순위, SQLite는 함수ID·코드·SVG 예제이며 eval2.py의 score는 모델값이다. 이를 사람·과제 성과로 재해석하지 않았다. logging 비활성·log-* 제외와 누락 입력파일, 공개 준비 노트의 hatch와 논문 shadow 과제 차이 때문에 release=실험판이라는 가정도 보류했다. [BC-J03/04; BC-05 및 구현 출처; artifact-inspection.json]

**Blueprint/Strata:** Blueprint 그림20위치에서 첫 paste와 완료상태를 연결해3미완료도 남겼다. 독립 정렬된 완료시간·품질 그림의 같은 순위를 같은 사람으로 이어 붙이지 않았고 정확한 초를 디지털화하지 않았다. Strata에서는 XML캐시와 TeX표의 `(condition,task)`6키를1:1 연결했으며 미연결·중복·결측은 관측0이다. 이는 참가자6명이 아니다. 차트 관계파일의 외부 workbook 이름은 `CSCW 2020 Participants Tracking.xlsx`; recall값은 `together!G54:I55`, 과제명G53:I53, 조건F54/F55, 오차G56:I57이다. 압축 안 CSV/TSV/XLS/XLSX/R/Python은 관측0이었다. [BC-J02; J-US-AGG; US-11; aggregate-join-audit.json]

**나머지 경로:** eXoaDocs는 저자 페이지·DOI·프로젝트·GitHub/Zenodo/OSF 정확명 검색·Wayback까지 추적했다.503/403/404와 성공한 보관 frame/논문은 실패·계보 행으로 분리했다. Unakite는 공개 bundle/source map의 `taskId,eventAuthorId,timestamp,pieceId`를 열었지만 당시 배포판과 실제 참가자 export를 확인·확보하지 못했다. Chan은 원 과제에 사용된 특허2개를 직접 열었으나 배포 과제 packet/사람×개념 점수표는 찾지 못했다. Schwonke의 별도 프로젝트는 DataShop 보유를 명시하지만 후보 dataset77/78과 두 실험의 대응은 미입증이다. 공통 도움말의 Students/Transactions 문자열은 실제 값이 아니었다. [J-NA-04; US-12; RT-T01/02; RT-A01; RT-D계열; datashop-metadata-fields.json]

8군의 원자료 탐색 경로와 버전·실패는 [studies.csv](studies.csv)에 남겼다. 두 군 이상에서 참가자 대장을 찾기 위한 실제 파일 수준 탐색을 수행했다. 확보한 부분 참가자행은 NCQ1군이며, CodeMend의 IR표는 사람 대장에 포함하지 않는다. 공개 인체 실험 대장2군을 확보한 것으로 주장하지 않는다. Strata의 집계 및 DataShop 후보 metadata도 그 수를 부풀리는 데 쓰지 않았다.

## Q3 · 선택·열람·총시간·활동시간의 경계

NCQ 선택은 링크 클릭이 아니라 package installation이다. 총시간은 명세를 충족하는 결과까지의 경과시간이며 선택 중앙값을 빼서 개인의 선택 후 처리시간을 만들 수 없다. Blueprint 첫 paste도 최종 채택/검증과 다르다. CodeMend는 부분과제 시간이어서 이를3배 하거나 완료자 평균에 곱해 전체 작업시간을 만들지 않았다. [O-NA-01~03; BC-O01/02/05]

eXoaDocs는 관련 문서 체류30초를 이용한 전환 proxy다. TableX는 완료자 조건부 누적시간이고 T3/4는 동일 문서를 보므로 시간 분리가 불가능하다.40분은 네 과제 전체의 상한이다. TableX의 시간 포함자 분모를 TableXII에서 가져오거나, 차례로 누적평균을 빼서 같은 사람의 과제별 시간을 추정할 수 없다. [NA-002 §5.2–5.3.2; O-NA-04~08]

Unakite의44%/25%는 비디오로 코딩한 도구 상호작용 비중이다. 총초와 기능 정의가 없으면 사람 전체의 활성 노동초가 아니다. 공개 구현의 start/end 함수 존재만으로 실제 계측을 확정할 수도 없다. Strata의 웹 체류·scroll 비율은 작성자의 맥락 신호이지 소비자 실험 노동시간과 같은 것이 아니다. DataShop codebook의 transaction 간격도10분 초과/세션 경계 처리에 따라 누락될 수 있고,2006실험의 실제 열/규칙을 대신하지 않는다. [US-01 pp8–9; US-02 §5.4.1; US-12; RT-M01]

**판정:** 전체 활동시간을 수치로 채울 수 있는 행은 이 자료집에서 관측0이다. 실제 경과시간·부분 상호작용 비율을 활동시간 칸으로 옮기지 않았다. 대기·중단·훈련·도구 소개를 제거하거나 포함했을 때의 새 효과는 해당 이벤트 원행이 없어서 미산출이다.

## Q4 · 같은 품질과 실패자를 어떻게 다뤘는가

명세 충족, 첫 paste, 표 완성, 타당한 설명3개, 코드 순위, 개념 독창성은 서로 다른 품질이다. NCQ 분석10명 전원 성공은 모집14명 전원 성공과 다르고,4명의 철회 단계를 임의로 각 조건 실패에 배정할 수 없다. Blueprint 완료자9/8의 시간평균에는 미완료1/2가 빠진다. CodeMend60기회에서 남은14/19는 미도달·미완료 혼합이므로 모두 잘못된 제출이라는 뜻이 아니다. [NA-004 §3; BC-01; BC-02; J-NA-03]

eXoaDocs의 네 과제 모두 pass는 개입3/12·대조1/12, 비통과는9/12·11/12이다. 실패 원인을 오답·미제출·시간초과로 분할할 공개키는 없다. Task3만은3/12 대4/12로 방향이 반대다. 따라서 전체 pass 수와 더 짧은 완료자 평균을 연결해 "같은 품질로 더 빨라졌다"고 쓰지 않는다. [NA-002 TableX/XII]

Strata는 전원이600초 안 끝냈다는 진술과 각 이유가 유효/고품질이라는 판정을 분리한다. 생략된 무효 이유는0으로 채우지 않는다. 품질 값 자체도 Python/Strata precision 표90.1% 대 그림91.0%, Deep/Strata의 gold11·고품질 평균6.90·recall64.5%가 같은 고정분모 정의 아래 맞지 않는 문제가 있다. 제작 캐시가64.5%를 반복한다고 어느 값이 맞는지는 결정되지 않는다. [US-02 §6; US-11; O-US-05]

동등 품질에는 사전 허용차와 그 차이의 불확실성, 같은 과제/루브릭·실패 분모가 필요하다. Blueprint p=.21이나 Schwonke의 비유의 점수 차이만으로 동등성을 선언하지 않았다. Unakite E2의 공통3이유 문턱은 제한 과제의 품질 통제로 볼 수 있지만 실제 코드 품질·장기 재사용까지 확장하지 않는다. [RT-M03; BC-O04B; O-RT-02; O-US-02]

## Q5 · 허용 계산과 빠진 항

새로 실행한 계산은 NCQ행/키/flag 감사, CodeMendIR행·중복 감사, Blueprint그림 위치·완료상태 판독, Strata집계6키 연결이다. [joins.csv](joins.csv)의16개 연결 계약과 [outcomes.csv](outcomes.csv)의26개 종점 행은 입력·대상·연결·미연결 수, 설계, 필요한 파일, 계산식, 불확실성·누락 분모를 보존한다. 원자료가 없는 조인의 unmatched 수는 미확인이다.

| 계산 대상 | 허용 형식 | 지금 빠진 최소 항 |
| --- | --- | --- |
| 동일인 교차/반복 비교 | 사람 식별키를 보존하고 조건·과제·period·sequence를 구분한 시간/원점수 차이; 같은 과제를 가장하지 않음 | NCQ의 T코드북·시각·최종검사, CodeMend/Unakite의 순서·실제시간 포함행 |
| 독립군 시간/품질 | 군별 배정자 분포와 완료자 조건부 분포를 별도 보고; 사람끼리 임의 짝짓기 없음 | eXoaDocs의 각 시간 셀 n·포함 지시자·숙련층; Blueprint의 개인별 그림 대응; Strata군별 n |
| 제한시간 안 정확히 완료 | 각 군의 ΣI(최종검사 통과 AND 제출시간≤cap)/배정 대상수 | 시간·검사 공동키, cap 적용·중단·제출없음 사유. eXoaDocs는 저자 all-pass집계만 사용 가능 |
| 실패 포함 시간 | 미완료를 삭제한 시간과 별도 종점; cap/censor 정의를 먼저 고정 | 각 미완료자의 중단·관측종료 시각과 제한 적용. 실패를 cap초의 실제 완료시간으로 쓰지 않음 |
| 동등 품질에서 시간 | 사전 품질 허용차·구간 또는 동일 기능문턱, 전체 배정 분모/선택 과정 명시 | 품질 원점수·time joint row·허용차. 사후 성공자 제한은 배정 효과와 구별 |

eXoaDocs `3/12−1/12` 같은 공개 집계식은 쓸 수 있지만 새 원자료 효과로 재포장하지 않았다. NCQ `median(E)−median(C)`는 `median(E−C)`가 아니다. Blueprint 전원 순위검정p값은 완료자 평균차의 구간이 아니다. 평균·중앙값·기하평균과 성공자 조건부 분포는 서로 다른 추정대상이며 단위를 맞췄다고 합칠 수 없다. [RT-M02/03/05; analysis-procedure.md]

## Q6 · 처음 결론을 뒤집을 반례와 감도

[counterexamples.md](counterexamples.md)에12개 사례와 최소 추가 기록을 두었다. 직접 확인한 주요 반례는 다음과 같다.

- **선택 대 총시간:** NCQ E2의380→57초와849→847초는 큰 선택 차이가 전체에 그대로 옮겨가지 않는 집계 반례다. 개인의 후처리 지연 원인까지 증명하지는 않는다. [O-NA-01/02]
- **사용 대 실행:** NCQ의 Used?=1/Runs?=0,Used?=0/Runs?=1은 채택/단독 실행이 다를 수 있음을 보여준다. snippet의 실행 실패를 최종 제출 실패로 바꾸지 않는다. [O-NA-SNIPPET1/2]
- **검색 후 미완료:** Blueprint는20명 모두 paste했지만3명이600초 안 완료하지 않았다. 완료자 평균만 보면 이3명이 사라진다. 그림 정렬 때문에 이들을 품질 순위에 안정적으로 연결할 수는 없다. [BC-J02; BC-O01~03]
- **시간과 품질 방향 분리:** eXoaDocs의 T3통과3 대4는 문서 평균시간만으로 전 과제 품질 향상을 일반화할 수 없게 한다. [O-NA-06/08]
- **읽기·저장·채택 분리:** Unakite에는 수집한 자료를 즉시 비교표에 쓰지 않는 질적 패턴과 긍정 표지 수가 좋은 대안을 뜻하지 않는다는 사용자의 지적이 있다. 구현도 highlight/save/tableinsert를 구분한다. 실제 event 빈도·노출→거절 개인행은 미확인이다. [US-01 p10; US-12]
- **다른 분야의 비용:** Chan에서는 먼 유추의 독창성과 수량이 갈라지고, Schwonke 별도 프로젝트의 후속Study3에는 시간/전이 우위가 보고되지 않는다. 후속45명을 고정2009코호트나 소프트웨어 분모에 더하지 않는다. [RT-P01; RT-A01]

성공자만/실패 포함은 Blueprint·eXoaDocs에서 분모가 달라짐을 확인했으나 원행 감도 추정은 불가능하다. 초보/숙련은 eXoaDocs의 배정층 존재까지만 확인되며 층별 시간–품질효과가 없다. 훈련 포함/제외, 같은 링크/다른 후보, 부분/전체 시간은 설계 차이를 식별했으나 없는 활동초를 넣어 순이득을 계산하지 않았다. "설명을 읽고 채택하지 않은 기록"을 못 찾았을 때는 관측0이라 하지 않고 살핀 event 필드·미공개 score/log를 명시했다. [SELF_CHECK.md Q6; counterexamples.md]

## Q7 · 설계자의 작업에 옮길 수 있는 범위

**확인된 사실:** Chan의 과제는 에너지 수확 장치 아이디어이고 예제 탐색·해석 뒤 아이디어를 내는 고정30분이다. 직접 열어 본 특허는 가까운 발전 장치와 먼 지진 격리 원리처럼 내용이 다르다.1321개 개념 중1066개를 품질 분석에 남긴 과정은 실제 제작·검증·나중 수정까지 관측한 것이 아니다. 품질의 예상 제작/설치 용이성은 실제 사람의 제작시간이 아니다. 본문153명과 표151명을 해결하기 전에는 정확한 군별 배정분모를 확정할 수 없다. [RT-P01; RT-T01/02; RT-M04]

Schwonke는 학습중 일부 풀이 단계를 제공하는 비교다. 즉시 절차·개념 점수와 학습단계 시간은 관련 있지만 특정 소프트웨어 설계의 완료·유지보수와 같은 결과가 아니다. 다른 코호트의 지연검사나 프로젝트 후속결과를 고정 실험의 추적값으로 가져오지 않았다. DataShop보유 표시는 파일 접근·2006코호트 대응·사후점수 연결을 대신하지 않는다. [RT-P02; RT-A01; J-RT-02/03]

| 주장 | 설계자에게 필요한 관측 | 참가자 관점에서 필요한 관측 | 채점자 관점에서 필요한 관측 | 현재 판정 |
| --- | --- | --- | --- | --- |
| 자료를 빨리 골랐다 | 같은 선택 대상과 첫/최종 선택·채택 정의 | 과제 시작,검색,열람,선택 시각과 순서 | 선택된 자료가 과제에 맞는지 | 일부 선택/이유작성 종점만 확인; 전체 완료와 분리 |
| 제한시간 안 정확히 끝냈다 | 공통 명세와 제출·검증 완료 | 배정군·과제·훈련·timeout·중단을 포함한 분모 | 기능검사/루브릭과 실패 사유,판정 가림 | 일부 저자 집계 가능; 새 joint raw 분석은 미확인 |
| 나중의 재작업이 줄었다 | 최초 결과 기준선·추적 기간·후속 변경량 | 재열람·재구현·대기·활동시간 | 후속 수정의 필요성과 최종 품질 | 고정8군에서 이 효과를 검증할 공동 추적 자료 미확인 |

**조건부 제안:** 제품은 선택·채택·구현·검사·재수정 단계를 분리한 기록을 우선 설계할 수 있다. 그러나 이 연구 묶음으로 제품의 절감 시간 숫자를 정하지는 않는다. Unakite의 일주일 후 도구 채택 질적 확인 사례는 존재하지만 대조군·동일 명세·노동·수정 기록이 없어 재작업 절감 관측으로 계산할 수 없다. 따라서 "후속 관찰이 전혀 없다"는 과장도 피한다. [US-01 p9; US-QC-02; counterexamples.md]

## 직접 열람·선정·수용 조건

| 요구 자료층 | 요구 | 중복 제외 배당 인정 | 충족 슬롯 | 부족 |
| --- | --- | --- | --- | --- |
| 고정8군 원논문 | 8 | 8 | 8 | 0 |
| 저자 별도 부록·연구자료·복제 패키지 | 6 | 2 | 2 | 4 |
| 독립 과제지·채점 기준·도구 구현 | 6 | 3 | 3 | 3 |
| 원 측정·비교방법 또는 추가 공개 자료 | 4 | 6 | 4 | 0 |
| 합계 | 24 | 19 | 17 | 7 |

실질적으로 읽은 고유1차저작25개 중 배당 인정19개와 배당 밖6개를 분리한다. 배당 밖은 적격성 판단을 위해 읽은 SURF/ALICE/NBSearch 원논문·SURF독립repo와 Chan자극 관련 특허2개다. 특허원문을 열었다고 실제 실험 과제 packet을 열었다고 세지 않았다. 같은 논문의 저자판/출판판/TeX·그림, 동일repo구성파일, 겹치는 학위논문, eXoa계보 반복, 설명서·정책, DOI metadata, 검색 결과·실패는 수를 채우지 않는다. 특히 방법자료 초과2개로 다른 층 부족7개를 메우지 않았다. [evidence/source-counts.json; sources.jsonl]

보강은 사전 범위에 따라2019–2025 ICSE/CHI, 두 검색식(API example 또는 code search와 user study), 날짜·제목 정렬, 실제 소프트웨어 수정과 시간·품질 모두 요구했다.34개 **반환 기록**은34개 고유 연구가 아니다. 검색/패턴/이해 과제 중심의 가까운 후보는 제외했고 원 논문/공개 artifact 존재만으로 적격으로 올리지 않았다. 공식 목록 전수조사가 아니므로 미해결 metadata 후보와 검색 범위의 한계도 남겼다. 앞선6군을 공개성이 좋은 후보로 교체하지 않았다. [SCOPE.md; evidence/supplement-search-frame.json]

요구사항별 분자·분모·단위·행과 미충족 이유는 [evidence/acceptance-evidence.json](evidence/acceptance-evidence.json), Q별 반대증거·재개행동은 [SELF_CHECK.md](SELF_CHECK.md)다. 사전 규칙은①커밋에서 고정했고 원문으로 알게 된 제한시간·자원허용·분모·표 불일치는 [CORRECTIONS.md](CORRECTIONS.md)에 남겼다. 규칙을 바꿔 결측 자료를 적격으로 만들지 않았다.

## 실행·재현·다음 첫 행동

실행한 것은 공개 URL/고정SHA의 읽기, 문서·정적코드 판독, 메모리 내 CSV/제작자료 감사와 원장 정합성 검사다. 참가자 프로그램·저자 도구·비공개 DB를 실행하거나 사람을 모집하지 않았다. 명령·입력·원문 줄 범위·실제 출력은 [analysis-procedure.md](analysis-procedure.md), 각 stream 실행 receipt, 원장 evidence_pointer에 있다.

```bash
python -B docs/workstreams/research/AF-RES-050/streams/ncq-exoa/audit_ncq.py
"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/audit_public_release.py
python -B docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py strata
python -B docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py unakite
python -B docs/workstreams/research/AF-RES-050/build_ledgers.py
python -B docs/workstreams/research/AF-RES-050/verify_ledgers.py --documents
python -B -m workbench.session check docs/workstreams/research/AF-RES-050/manifest.json --fetch
```

위 목록은 재현 명령이다. 각 명령의 실제 실행/미실행 상태는 receipt를 우선한다. RESULT 커밋5a86c940 이후 session check는 exit0/passed였고, 두 표와 수용 원장은 원격 전체 내용이 일치했다(evidence/session-check.json, remote-reread.json). 검증 커밋의 최종 재열람/check도 HANDOFF에 실제 결과와 함께 기록한다. 원자료 부재 때문에 사람별 시간–품질 통합분석·작성자 분석 스크립트 재실행은 미실시다. 이를 실행했다고 표시하지 않는다.

**다음 첫 행동은 NCQ의 공개 코드북과 시간·제출·최종검사 파일 존재를 정확한 파일/저작 경로에서 다시 확인하는 것이다.** `(experiment,P,T)→condition,problem,period` 대응과 각20대상시행의 timestamp·최종score·중단사유가 최소 입력이다. 확보 전에는 T1/T2조건 효과를 계산하지 않는다. 이어 Strata workbook의 공개 비식별판과 이유별 점수/gold를 확인하고, Schwonke는 후보77/78의 코호트 crosswalk와 export/사후점수 키부터 확인한다. 새 자료가 공개되면 동일 사전 종점으로 조인 전후 행수·탈락 분모를 먼저 감사한 뒤 분석한다. 저자에게 연락하거나 접근 권한을 요청한 작업은 없다.

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 1. 배정×시간×최종품질·실패 원행 미연결; Strata 품질/Chan 사람분모도 불일치 | 동등 품질 총시간,실패 포함 효과,정확한 불확실성 | [NCQ CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) P/T와논리17행; [Strata 제작자료](https://arxiv.org/src/2102.06231v2) main.tex802/848/850; [Chan Table1](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf); J-NA-01/02,J-US-03/AGG,J-RT-01 | NCQ코드북·timestamp·최종검사와 철회 ledger;Strata workbook/이유별score;Chan배정표 | 자연키·관측분모·제외 규칙이 연결되고 출판 불일치가 같은 원행으로 해소될 때 |
| 2. 도구·후보·훈련 묶음과 부분 종점; 추적 노동/재작업 계측 미확인 | 동일 링크 설명만의 효과 및 설계자의 전체 재작업 절감 | [Blueprint p518/Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); [Unakite pp8–10](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf); O-NA-01/02,BC-O01~07,O-US-01~03 | 같은 후보 설명 배정과 교육·열람·구현·검사·후속수정 event 계약 | 개입이 분리되고 같은 품질 기준의 전체 활동/추적 시간이 배정 단위에 연결될 때 |
| 3. 직접 자료 배당17/24; 별도 연구자료4·과제/구현3 부족 | 요구된 조사 완결성·공개성 탐색 범위의 확신 | [sources.jsonl](sources.jsonl), [source-counts](evidence/source-counts.json), [검색틀](evidence/supplement-search-frame.json); eXoa실패·DataShop후보행 | 부족한 두 층의 독립 공개 packet/루브릭/복제자료를 정확명·DOI·artifact경로에서 확인 | 중복·검색·실패를 빼고8/6/6/4 각 층을 채우거나 접근불가 범위를 명시한 부분 인계로 수용될 때 |
