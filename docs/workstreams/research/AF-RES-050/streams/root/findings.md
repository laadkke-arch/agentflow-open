# 분야 대조·측정 방법·선별 결과

## X01 Chan2011: 시간 고정 설계에서의 품질·독창성

RT-P01 §3/Table1/Table2를 원 PDF와 렌더 화면으로 읽었다. 본문153명과 Table1의9개 셀합151명이 다르므로 실제 배정 인원을 확정하지 않았다. 사람이 앉기 전에 배정한 종이 묶음은 near/far·commonness·picture/text를 달리한다. 각각3단계10분이므로 30분은 주어진 예산이지 관측된 완료시간이나 시간 절감량이 아니다. 그림 대신 문장으로 표현한 조건도 후보 특성과 분리해야 하며, 같은 링크에 설명만 붙인 처치로 부를 수 없다.

1321개 아이디어에서 최소 기능 요건을 통과한1066개를 분석했다. 제외255는 아이디어 수이며 사람 탈락 수가 아니다. 품질은0–4 차원 점수를 신뢰도로 가중한0–1 합성값, novelty는 드문 해결 방식의 빈도 기반 값이다. 예상 제작/설치 시간 항목은 평가자가 추정한 제품 속성이라 참가자 노동시간이 아니다. RT-M04 원 측정 논문 역시 quality·novelty·quantity·variety의 구별을 뒷받침하지만 이 실험의 누락 채점표를 대신하지 않는다.

저자는 far-field에서 novelty가 높아질 수 있는 동시에 생성한 아이디어 수가 줄었다고 보고한다. 마지막10분 단계만 보면 distance의 quantity 차이가 검출되지 않아 초기 해석 부담이라는 해석을 제시한다. 이는 그럴듯한 처리비용 기제이나 사람별 읽기시간이 계측된 증거는 아니다. RT-P01 §5.2/§6.1. 완성 설계나 추후 수정까지 조사하지 않아 downstream rework는 미확인이다(§6.3).

직접 원 특허 RT-T01/02를 열어 near-field 전기 발생 장치와 far-field 진동 방지 장치가 실제로 다른 후보임을 확인했다. 정확한 수업용 발췌문/보강 본문 묶음은 얻지 못했으므로 특허2개를 과제지 배당으로 인정하지 않는다. 참가자→phase→concept→coder 연결표·배정표는 저자 색인, DOI관계, OSF제목, Zenodo정확제목 경로에서 회수하지 못했다. 좁은 제목 검색의 관측0을 전세계 자료 부재로 확대하지 않는다.

## X02 Schwonke2009: 데이터 존재와 공개 연결 가능성의 차이

RT-P02에는 독립 무작위 두 실험50명(25/25),30명(15/15)이 있다. 같은7개 원기하 문제에서 수치 풀이 단계를 미리 채운 뒤 점차 없애는 조건과 모두 직접 푸는 조건을 비교하며 양쪽 모두 원리 설명과 tutor feedback을 받는다. 학습시간은 tutor 작업분, 전체 세션 약90분에는 교육·검사 등이 더 있다. E2는 guided exploration·연습·생각 말하기 교육을 바꾸므로 E1과 합쳐 한 효과로 계산하지 않는다. 각각 즉시 사후 개념·절차 전이를 검사했다. E1의 비유의 점수 차이는 동등성 검정이 아니다(RT-M03).

RT-A01 저자 프로젝트 보고서 Study1/2는 Data in Datashop Yes를 명시한다. Study1은2006년3월50명, Study2는4월30명이며 종료일 April31 오기가 있다. 현재 공개 목록 HTML에서215개 고유 dataset 링크를 읽었으나 지정 이름과 정확히 일치하는 두 실험을 식별하지 못했다. Other Datasets의4382개 링크 중 PI Renkl의 private Project94와 dataset77 Spring2006/78 Summer2006을 후보로 찾았다. 이들은 날짜 범위가 넓고 논문 실험ID 연결이 없어서 확정 대응으로 쓰지 않았다. 공개 DatasetInfo HTML에서 보이는 Students/Transactions 문구는 공통 도움말이며 실제 원행이나 값이 아니다. RT-D03/04 및 datashop-metadata-fields.json.

RT-M01 공식 export 문서에는 Transaction Id, Anon Student Id, Session Id, Time/Time Zone, Condition Name/Type, Outcome 등이 있다. 이는 가능한 자료 구조를 알려 줄 뿐 해당2006코호트 export를 열었다는 뜻이 아니다. sample 중복을 제거하지 않거나 event 간격을 활동시간으로 부르는 것도 부적절하다. duration의 긴 간격/세션 경계 결측 규칙은 실제판과 확인해야 한다. 독립군을 사람별로 임의 짝짓지 않는다.

RT-A01의 별도 Study3(CMU45명)는 학습시간이나 검사점수의 유의한 이득을 보고하지 않는다. 이는 고정 X02의 두 코호트 분모에 넣지 않은 맥락 반례다. 같은 페이지의 뒤 코호트 지연검사를 X02의 추적기간으로 가져오지 않는다. 재개에 필요한 최소 입력은 두 실험→dataset ID 대응표, 공개 비식별 transaction export, 동일 가명을 쓰는 posttest item scores, 당시 코드북이다.

## 방법과 보강 선별

RT-M02 crossover 보고 지침의 period·sequence·withdrawal·paired analysis 원칙을 적용하고, RT-M03 equivalence 원칙에 따라 비유의 검정을 동등성으로 읽지 않는다. RT-M05는 시간의 평균/중앙값/기하평균이 다른 목표라는 점과 성공자 표본 조건을 확인하는 자료다. 어떤 방법 논문도 누락 참가자 원행을 복원하지 못한다. 사전에 고정한 분석 규칙을 이 자료에 맞추어 사후 바꾸지 않았다.

두 고정 검색식의34개 결과를 기록했다. 공식 원문으로 자세히 확인한 ALICE(2019), NBSearch(2021), SURF(2024)는 검색/패턴/만족도 연구이며 실제 코드 수정의 시간과 기능 품질 비교라는 보강 조건을 충족하지 않았다. Rahman ICSE-Companion2019는 박사연구 개요이며 새 적격 실험을 확인하지 못했다. 선택0은 이 검색 프레임 안의 판정이며 포괄적 학회 전수조사 결과가 아니다. 원래6군을 대체하거나 잘 공개된 연구를 소프트웨어 효과 분모에 추가하지 않았다.

## 최소 연결식

- X01: `person(condition,site)` 1:N `phase` 1:N `concept(id,kept_reason)` 1:N `coder(score_dimension)`; 원행·키 없음. 정해진30분 안 품질·개수와 완료시간 효과는 다르다.
- X02: `cohort+anon_person` 1:N `problem/session/transaction` → 사람별 tutor-time; 같은 사람의 `posttest_item/score`와 결합. 독립군 평균 차이는 가능하나 짝 차이는 불가. 현재 cohort crosswalk·원시 clock·정답·누락지시자가 빠졌다.
- 모든 군: 후속 재작업은 초기 산출물ID·검사판·추적 종료일·실제 수정 활동을 연결해야 한다. 이 추가 관측은 공개 고정 실험에서 미확인이다.
