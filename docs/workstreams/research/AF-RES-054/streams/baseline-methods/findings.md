# B01·B02 및 방법·복제 근거

이 분담은 고정 AF-RES-050 결과판 `5797f9a9f1a1f0281d54c1922c6698a53093b67a`를 읽고, 두 기준 원논문의 분모·종점과 추론 규칙을 직접 대조했다. 새 여섯 자리의 선정자는 아니다. 배정 단위 원자료 결합은 두 기준 모두 **미실시**이며, 원자료 행 수를 0으로 바꾸지 않았다.

## 핵심 판정

| 자리 | 원래 분모·종점 | 이번 판정 | 바뀌지 않는 한계 |
| --- | --- | --- | --- |
| B01 Blueprint directed | 독립군10/10, URLLoader 과제10분; 완료9/8. 최종 품질은 외부 엔지니어의 순위 | 완료 여부만 저자 집계. **원래 이진 품질 통과선이 없어 요청한 공동 종점은 정의·식별 불가** | 순위로 q를 만들 수 없고, 서로 다른 정렬 그림을 person key로 쓸 수 없다 |
| B02 eXoaDocs 네 과제 묶음 | Java 경험층별 무작위 동수 배정,12/12.40분 안에 네 과제 모두 정확한 사람3/1을 저자가 명시 | **저자 공동 집계로3/12 대1/12, 차이1/6=+16.67pp**. raw 직접 계산과 별도 분류 | 정확한 제출시각·독립 시간 주변 t·개인별 task 패턴·원배정 키가 없다. 표본 불확실성·설명 단독 효과는 점식별되지 않는다 |

근거: [Blueprint 원문 printed518, Method/Results](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), [eXoaDocs §5.1–5.3.2, Tables X/XII, printed1:19–1:21](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf). `sources.jsonl` BM-B01/B02 행을 참조한다.

## Q1. 배정과 개입

Blueprint는 편집기 통합·코드 미리보기·검색 맥락·브라우저 제한을 함께 비교한다. Control은 Firefox/Adobe Community Help, Blueprint군은 브라우저 사용 금지다. Tutorial→directed→exploratory 순서이며 tutorial 안내도 동일하지 않다. 무작위 배정 절차는 읽은 Method에서 확인되지 않는다. eXoaDocs는 기본 JavaDocs에 채굴한 예제를 붙이는 중재이며, 원래 JavaDocs의 수동 예제도 두 군이 볼 수 있다. 같은 후보 링크에 설명만 붙인 독립 비교가 아니다.

## Q2. 시간과 최종 품질

Blueprint 첫 paste 평균57/121초와 완료자 평균346/479초는 서로 다른 종점·분모다. 완료자9/8만의 평균을 배정10/10의 평균으로 부르지 않는다. Engineer rank에는 사양·오류 처리·불필요 문장·style이 함께 들어가지만 이진 pass 기준이 없다. 10분 미완료1/2는 완료시간600초인 사람이 아니다.

eXoaDocs Table X는 성공적으로 끝낸 대상만 포함하며, 다음 과제 관련 문서를30초 넘게 본 로그에서 과제 전환을 추정한다. Task3·4는 같은 문서를 보므로 같은 시각을 대입한다. 제출 후 기능검사의 독립 타임스탬프가 아니다. §5.1.2의 검사 기준은 제출 코드로 테이블 생성·두 tuple 삽입·출력을 실행해 기대 tuple과 맞는지다. §5.3.2는 네 과제 모두 정확한 완료와40분을 한 문장으로 묶고3/1명을 명시하므로, 이 특정 공동 집계는 시간 평균에서 역산한 값이 아니다.

## Q3. 실제 결합 가능성

필요한 왼쪽 원장은 `cohort × participant × task × condition × period`다. B01 directed의 예정20 person-task, B02의 배정24 bundle/예정96 person-task는 프로토콜상 대상 수다. 공개 원행·집계 이벤트·join 전후·중복·미연결 수는 모두 미확인이다. `joins.json`의 null은 관측0이 아니다. 원자료가 없어 직접 join은 미실시이며, 저자 집계가 있다는 사실로 가상의 참가자 원장을 만들지 않는다.

### 원문 위치 정정: Blueprint 그림

2026-11-23 직접 받은 CHI PDF(SHA256 `f120690f776cc77b097054516f1e68e0b23c9e0450f63322f873d6b46e5922a5`)의 printed518은 Figure4를 참조하지만, 해당 hosted10쪽 PDF에 Figure4 그림·caption은 없다. printed518–520의 렌더를 확인했고 `pdfimages -list`에서도 그림 자산이 있는 쪽은1,3,4,9뿐이었다. 본문은10분·9/8·완료자 평균을 확인하기에 충분하다.

연결된 [Brandt2010 dissertation printed64–65, Fig5.4](https://hci.stanford.edu/publications/2010/brandt-dissertation/brandt-dissertation.pdf)를 직접 받아 PDF81쪽을 렌더했다. 네 그래프는 첫 paste·완료시간·코드품질·차트품질의 **각각 정렬된 조건 표시20칸**이다. 초 단위 축이나600초 표시, 공통 참가자 ID는 없다. 따라서 AF-RES-050의 해당 분담에 있던 “그림 위치20/20을 통한 paste–completion 연결”과 CHI Fig4 위치를 이번 결과의 직접 증거로 재사용하지 않는다. 이 정정은 표본·종점 규칙의 변경이 아니며, 같은 코호트 재수록을 새 저작 최소 수에 더하지 않는다.

## Q4. 범위와 정수 극단표

행렬 순서는 `[both, quality_only, time_only, neither]`다. 정확한 동일 모집단 주변 N,q,t가 있을 때만 `max(0,q+t−N) ≤ x ≤ min(q,t)`를 적용한다. 각 칸의 비음수가 경계를 주고, 경계 값을 넣으면 실제 정수표가 되므로 날카로운 경계다.

B01에서는 q의 값만 누락된 것이 아니라 원래 이진 품질 사건이 없다. 따라서 `primary_endpoint_bound=null`이다. 추후 독립적으로 이진 기준을 정할 때 가능한 논리 외피 `[0,9]`/`[0,8]`은 설명할 수 있지만, 이를 원 연구 종점의 경험적 식별 구간으로 보고하지 않는다. 순위 상위 절반을 통과로 자르거나 완료자 전원을 독립 품질 통과자로 바꾸는 표는 무효다.

B02에서는 저자가 x를 직접 집계했다. 별도 t를 몰라도 x는3/1이다. q를 “이 프로토콜에서 관측된 네 과제 전부 통과”로 두면 pass⊆within40min이므로, q=x만 적용한 약한 조건부 외피의 끝에서 아래 표가 성립한다. 이는 **같은 관측 t를 고정한 x의 양 끝이 아니라, 미보고 t의 허용 값이 달라지는 표**다.

| 군 | N,q,x | x=q만 쓴 조건부 t 끝 | 2×2표 | 해석 |
| --- | --- | --- | --- | --- |
| eXoa |12,3,3|3|[3,0,0,9]|통과자만 시간 내 제출했다고 놓은 구성 예 |
| eXoa |12,3,3|12|[3,0,9,0]|나머지도 시간 내 제출했으나 통과하지 못했다고 놓은 구성 예 |
| JavaDocs |12,1,1|1|[1,0,0,11]|동일 |
| JavaDocs |12,1,1|12|[1,0,11,0]|동일 |

어느 표도 개별 관측 기록을 복원한 것이 아니다. 최종 교차검토에서 Table XII의 과제별 correct submissions가 같은40분 내 부분 제출을 함의한다는 해석을 추가하면 t하한11/10과 (3,0,8,1)/(1,0,9,2)가 필요함을 확인했다. 원문의 최종 제출 정의·개별 시각이 미확인이므로 위3/1하단은 모든 출판 제약을 반영한 확정 t범위가 아니다. x3/1은 변하지 않는다. “나머지9/11”은 공동 성공으로 보고되지 않은 사람이며, 실패·미제출·철회의 세부 분해는 미확인이다.

## Q5. 비교 차이의 부호

같은 네 과제·40분·12명 분모에서 `(3−1)/12=1/6`이다. 이는 이 소표본의 저자 집계 기술 차이이며 모집단 효과의 신뢰구간이 아니다. 처치군·대조군의 실제 미관측 성공수 범위가 생기면 각 군의 식별 구간을 먼저 만들고 극단 조합으로 차이를 계산한다. 새로운 독립 표본을 가정하거나 원자료 없는 회귀·짝 효과를 실행하지 않았다.

## Q6. 결론을 뒤집어 보려는 구성

eXoaDocs Table XII 주변은 eXoa `[11,11,3,3]`, JavaDocs `[10,8,4,1]`이다. 네 과제 pass 패턴의 비트 순서는 T1,T2,T3,T4다.

| 구성 | eXoa 패턴:수 | JavaDocs 패턴:수 | Table XII와 §5.3.2 제약과의 관계 |
| --- | --- | --- | --- |
| 호환 예A |1111:3,1100:8,0000:1|1111:1,1110:3,1100:4,1000:2,0000:2|모든 과제 주변과 전체3/1에 맞음 |
| 호환 예B |1111:3,1100:7,1000:1,0100:1|1111:1,1110:3,1100:2,1000:4,0100:2|같은 전체 결과라도 미완성 과제들의 결합은 달라짐 |
| 주변만 맞춘 반례 |1110:3,1101:3,1100:4,1000:1,0100:1|1110:4,1100:4,1001:1,1000:1,0000:2|각 주변은 맞지만 all1111=0/0이므로 §5.3.2의3/1과 모순 |

전체 교집합 문장을 버리면 네 주변만의 범위는 eXoa0–3, JavaDocs0–1, 차이−1/12~+3/12여서 양 부호가 가능하다. 그러나 저자의3/1 제약을 읽은 뒤에도 이 넓은 구간을 최종 답으로 쓰면 이용 가능한 정보를 버리는 오류다. 반대로 Task3만 떼면3/12−4/12=−1/12이므로, 전체 묶음의 방향과 다른 하위 종점이 실제로 있다.

완료자 선택이 평균의 의미를 바꾸는지는 별도 **가상 반례**로 보였다. 두 군10명, 한 군1명만100초에 완료하고9명이600초 제한에서 미완료, 다른 군10명이200초에 완료했다고 하자. 완료자 평균100 대200은 앞 군이 빠르지만, 완료율10% 대100%와 명시적 cap 벌점 평균550 대200은 반대다. 이 숫자는 Blueprint 관측이 아니며, cap 벌점 역시 실제 완료시간으로 이름 붙이지 않는다.

## Q7. 설계자에게 허용할 문장

- Blueprint: “이 복합 도구 비교에서는 첫 paste가 빨랐고 완료자 평균도 짧았다. 원래 품질 판정은 순위여서, 제한시간 내 독립 품질 통과율은 계산할 수 없다.”
- eXoaDocs: “이 과제·초보 java.sql 코호트에서40분 내 네 과제를 모두 정확히 마친 사람은 eXoa3/12, JavaDocs1/12였다. 공개된 개인 결합행에서 재계산한 결과는 아니다.”
- 설명만의 효과, 동등 품질 총시간, 훈련·대기까지 포함한 총 노동, 후속 재작업에 대한 문장은 이 두 기준으로 뒷받침되지 않는다. 각각 동일후보 조건, 독립 품질 기준과 전원 시계, 훈련·idle 기록, 같은 산출물의 추적 수정 원장이 더 필요하다.

## 방법 원전4편의 역할과 적용 한계

| 저작·직접 확인 위치 | 여기서 쓰는 원칙 | 적용하지 않은 확대 |
| --- | --- | --- |
| [Imbens–Manski CWP09/03](https://cemmap.ac.uk/wp-content/uploads/2020/08/CWP0903.pdf), §2–3 pp2–4 | 관측 분포가 허용하는 식별 구간과 표본 변동을 반영한 신뢰구간은 다르다. 미관측 bounded outcome의 분포를 모르면 그 지지를 통해 범위를 둔다 | 이번 유한 표본의 셀 범위를95% CI로 부르지 않음; workingpaper와2004판 중복 산입 안 함 |
| [Lee author manuscript2008](https://www.princeton.edu/~davidlee/wp/resrevision8.pdf), §3.1 pp13–17 | 무작위 배정 뒤의 완료자 선택도 비교 가능성을 깨뜨릴 수 있다. 제시된 trimming bounds에는 independence·monotone selection이 필요하고 항상 관측될 잠재 집단을 겨냥한다 | 미확인 단조성·완료시간 분포로 Lee bounds 계산하지 않음; 완료자 평균을 배정 전원 효과로 확대 안 함 |
| [Rubin1976](https://people.csail.mit.edu/jrennie/trg/papers/rubin-missing-76.pdf), pp581–584 §§2,5 | missing pattern과 observed/missing 값을 구별하고, 결측기제를 무시할 조건을 명시해야 한다 | 공개 파일에서 빠졌다는 이유만으로 MAR를 가정하거나 미확인을 실패로 덮지 않음 |
| [Balke–Pearl1997](https://ftp.cs.ucla.edu/pub/stat_ser/r199-jasa.pdf), pp1171–1172 §§2–3 | assignment Z, 실제 받은 처치 D, outcome Y를 분리한다. 제한된 관측분포에 맞는 극단 분포를 구성해 sharp bound를 점검한다 | 그 논문의 exclusion·independence 가정이 필요한 인과효과 공식을 단순 완료×품질 교집합으로 오인하지 않음 |

## 다른 코호트·분모와 등록 기록

[Urry et al2021 직접복제](https://static1.squarespace.com/static/587ea259197aea1c1d66ec5b/t/601f2ac8268c6a7b9735c877/1612655305004/Urryetal_PSCI_2021.pdf) pp2–4는 원 연구65명과 복제145명 모집→142명 quiz 분석→140명 notes 분석을 구별한다. 두 무응답자와 조건 불명확1명이 제외되며 notes2명도 추가 누락이다. 같은 강의·점수 비교라도 정보 인코딩 직후의 시험과1주 뒤 복습 시험은 별도 종점이다. Abstract와 Method가 laptop/longhand의74/68 배치를 서로 바꿔 쓰므로 조건별 N은 독립 원장 확인 전 선택하지 않았다. 이 사례는 여덟 자리에 추가된 연구가 아니라 분모 감사용 별도 직접복제다.

[Bichler2020 저자 원고](https://www.researchgate.net/publication/337692670_How_working_memory_capacity_and_shifting_matter_for_learning_with_worked_examples-A_replication_study) pp13–21과 [2026 self-explanation 복제](https://bpspsychub.onlinelibrary.wiley.com/doi/pdf/10.1111/bjep.70098) pp1506–1508/Fig1을 대조했다. 2020의231명 중 비시간압력115명이2026에 재사용된다. 2026은2016/2022 원 코호트와는 다른 코호트의 복제 분석이지만2020과 독립된 모집은 아니다. 2020 논문이 E01로 채택되면 이 분담의 같은 DOI는 새로 산입하지 않는다. 2026은 표본 모집 기간2018–2025 밖의 보조 복제 문헌이며, 여덟 자리를 채우지 않는다.

같은 계보의 [Bichler2022 원 코호트 분석](https://link.springer.com/article/10.1007/s11251-022-09579-4), Method의 Sample and design은 self-explanation 자료77명에서 미완료1명과 다른 파일에 연결할 수 없는 worksheet2명을 제외해74명(36/38)을 분석했다고 적는다. 개인코드를 썼다는 Procedure 문장만으로 성공적인 전원 결합을 보장할 수 없다는 실제 반례다. 이는2020/2026의115명과 합칠 분모가 아니다.

별도 [dx6qv author preregistration DOCX v1](https://osf.io/download/gfawy/)는 OSF API 파일 날짜2016-04-29를 갖고, Sampling Plan 자체는 연구가4월 중순에 시작했다고 적는다. 따라서 이 공개판만으로 **자료 수집 전 등록이었다고 인증할 수 없다**. 계획136명·최소80명 뒤 순차 BF·가능 최대180–300은 실제 배정 분모가 아니다. 원본 preregistrant 사망 후 만든2018 fork라는2020 원고 주석과 OSF `forked_from=368fz`가 맞는다. 현재 fork는 registration=false이고 등록 목록이 비어 있다. 계획은 pairwise deletion·구성개념별 충분한 측정 시 포함을 명시하지만 실제 논문의 결측 제외와 일치하는지는 배정 원장·제외 이유가 필요하다. 별도 저자 계획 문서로 읽은 사실과 사전 시점 인증을 구분한다.

## 재현

`python -B docs/workstreams/research/AF-RES-054/streams/baseline-methods/calculate_baseline.py`는 N,q,t,x의 네 셀 합, 여섯 pass-pattern 표의 주변, 출판 제약과의 모순, 정확한 분수 대비를 검사하고 `calculation-output.json`을 만든다. 실제 실행 영수증은 `calculation-execution.json`이다. raw 참가자 행을 만들거나 저자 코드를 실행하지 않는다.

| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |
| --- | --- | --- | --- | --- |
| Blueprint 원래 pass cutoff 없음·그림 정렬을 공통키로 잘못 읽을 위험 | 제한시간 내 정확한 완료율·동등품질 시간 | 원논문 printed518; dissertation printed65 Fig5.4; BM-B01/B01-TH | 같은 코호트의 사전 binary rubric과 participant별 독립채점·시계 파일 | 원래 기준과 키가 확인되면 공동 종점 직접계산 가능 |
| eXoaDocs 명시된 전체3/1와 미보고 개인별 기록의 차이 | author aggregate를 raw join으로 잘못 승격; 미완료를 모두 오답으로 분류 | §5.3.1–5.3.2, Tables X/XII; BM-B02 |24명 배정대장과 task별 제출시각·teststatus·철회코드 | 같은 분모에 제출·채점이 연결되고3/1 집계와 일치할 때 직접계산으로 승격 |
| 계획·출판·재분석의 분모와 시점이 다름 | prereg를 사전등록 인증으로, reused cohort를 독립 복제로 오인 | dx6qv/gfawy Sampling Plan; Bichler2020 pp13–21; Bichler2026 Fig1; Urry2021 p3 | 원래368fz 등록snapshot·수집시작/배정/제외 대장; Urry 조건원장 | 등록 선후·실제배정분모·독립코호트·조건별N이 확인될 때 해당 주장 재판정 |
