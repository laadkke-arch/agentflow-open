#!/usr/bin/env python3
from report_tables import *
g=read('evidence/agreement.json');d=read('coding/adjudication.json');imp=read('evidence/impact.json')
text='''# AF-RES-016 — 일치도와 불일치 진단

## 1. 관측 결론

동결한 198단위 × 3안 × 2코딩에서 단순 일치가 가장 높은 안은 **011·012에서는 S1, 004에서는 S2**다. 모든 상황의 우승안을 뜻하지 않는다. S3의 결합 일치는 두 축을 모두 맞혀야 하므로 S2와 같은 난도의 지표가 아니며, 형태·기여 분리의 정보 가치는 별도로 판단한다.

코딩은 작업자 GPT-6 Astra Pro와 새 문맥의 같은 모델 내부 별도 코딩이다. 사람 사이 재현성이나 타 모델 재현성 실험은 아니다. 작업자는 선행 라벨을 읽었고, 별도 코더에는 동결 CODEBOOK·label-blind 표본만 주었다. 이 정보 비대칭도 결과의 일부다.

'''+t1()+'''

주 불일치 유형의 분모는 해당 안·표본의 불일치 수다. 여러 축이 다른 단위에도 지배 진단 하나를 붙였으므로 표의 유형은 축별 인지 원인 검증이 아니다. 모든 수치의 원자료·주변분포·혼동행렬은 [agreement.json](evidence/agreement.json), 원 코딩은 [A](coding/coder-a.json)와 [B](coding/coder-b.json)에 있다.

## 2. 동결·표본·통계 방법

### 2.1 순서와 단위

| 단계 | 고정 커밋 | 확인한 내용 |
| --- | --- | --- |
| 코드북 | `68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0` | SCOPE/CODEBOOK을 표본 코딩 전에 동결 |
| 표본 | `019f0fcc6ee07946cd337aa43fb708784dd67e5a` | 011 120 + 012 60 + 004 18 = 198; 원 역할·판정 제거 |
| 작업자 A | `0981732949cdea358c4ffa27aafd4ae50d310bbe` | 198행 원 TSV·JSON 동결 |
| 내부 별도 B | `674f1c8eb99e531acee7531c8f1495f721c4dffd` | A 동결 뒤 새 문맥에서 198행; 원 TSV·JSON 보존 |

011은 대응 가능한149개에서 T047 66개 중37개를 시드2026112016으로 고르고 나머지83개는 전부 유지했다. T047은37/120=30.83%로 줄었지만 T036 28개와 합하면65/120=54.17%다. 012는 자료집156개 중60개를 고정 시드로 선택하고 기존 qrel 연결이 있으면 해당 질의, 없으면 시드2026112028로 질의를 붙였다. 이 중 **24개만 기존 qrel 연결이고 36개는 무작위 질의 연결**이다. 004는 합성18행 전부이며 R18의 바뀐 요구와 given을 반영했다. 선택 과정은 [sample/README.md](sample/README.md), [design-audit.md](evidence/design-audit.md)에 있다.

### 2.2 계수와 구간

`Po=같은 라벨 행 수/n`, `Pe=Σ pA(k)pB(k)`, `κ=(Po−Pe)/(1−Pe)`를 사용했다. S3는 `(form, contribution)`의 정확한 결합을 한 범주로 센다. 결측은 없고 `unknown`, `mixed`도 정식 범주로 포함한다. S3 contribution은 코드북상 S2와 동일하므로 3안은 서로 독립된 실험 처치가 아니다.

원 행의 두 코딩을 함께 유지하며 **011은 스레드15개, 012는 선택 질의31개, 004는 기본 문제4개**를 복원추출했다. 5,000회, 시드2026112616, 매 회 주변분포·Pe를 다시 계산하고 선형 보간 percentile 2.5/97.5%를 보고한다. 같은 재표본을 안끼리와 011 원/새 코딩 비교에 공유했다. 행 가중 점 추정이며 thread-macro 평균이 아니다. cluster 내 행들은 모두 함께 재표집한다. [M07](https://link.springer.com/article/10.1186/s12874-016-0200-9), [M08](https://journals.sagepub.com/doi/pdf/10.1177/0962280218794733)

'''
text+=table(['표본','안/축','일치/단위','Po','Po 95% 구간','κ 95% 구간','κ 미정의 복제/5000'],[metrics_row(r) for r in g['main']])
text+='''

Pe=1인 재표본의 κ는 1로 채우지 않고 미정의로 뺐으며 그 수를 보고했다. 004 S2에서301/5000, S3와 형태축에서각21/5000이 미정의다. 특히 18/18의 [1,1] 구간은 같은 관측을 재표집해 얻은 퇴화 결과이며 새 문제에서도 완전 일치한다는 보장이 아니다. cluster4/15개의 불균형 편의표본에서 95% 모집단 coverage를 검증하지 않았다. 사례 구성 변동만 다루며 코더 모집단의 변동은 포함하지 않는다.

012는 상위 문제를 공유하는 질의들을 다시 묶어 **12개 문제 cluster**로도 계산했다. 점수는 같지만 S2 κ 구간은 [0.642, 0.969], S3는 [0.679, 0.916]으로 넓어졌다. 원 주분석을 바꾸지 않고 민감도로 보존했다. [query-parent-map.json](evidence/query-parent-map.json)

## 3. 기존 011의 재계산과 같은 표본 비교

원149의 값은 **75/149=50.34%, κ=0.382**였다. 원 코딩 A의 component77/product18과 B의 component12/product76이 크게 다르며, A component→B product가56/149였다. 이번120에 해당하는 원 코딩은 **66/120=55.00%, κ=0.427**, 같은 방향 혼동은38/120이다. 기존 코딩은 다시 하지 않았고 대응 ID와 원값만 재계산했다. [sample/baseline.json](sample/baseline.json), 고정011 RELIABILITY·reliability-original/blind/selection

'''
rows=[]
for r in g['paired_011_differences']:
 if r['scheme']=='S3_form':continue
 rows.append([r['scheme'],f"{100*r['po_difference']:+.2f}pp",interval([100*x for x in r['po_difference_ci95']],2)+'pp',f"{r['kappa_difference']:+.3f}",interval(r['kappa_difference_ci95'])])
text+=table(['새 안 − 원120','Po 차이','같은 cluster 재표집 95% 구간','κ 차이','κ 차이 95% 구간'],rows)
text+='''

세 안 모두 점 추정은 올랐지만 **차이 구간은 모두 0을 포함한다.** 동일120을 쓰더라도 새 코드북·코더 문맥·기존 연구 요약·범주가 함께 바뀌었으므로 상승을 분류안 하나의 인과 효과로 분리할 수 없다. 특히 S2/S3는 원래 답 역할과 질문 자체가 달라 원 κ와 동질한 척도라는 보장이 없다.

## 4. 높은 일치의 반례와 낮은 일치의 반례

### 4.1 S1이 충분할 수 있는 자료

012의 registry-origin URL(npm/PyPI)27개에서는 S1이 **27/27**, 양쪽 component26/product1로 일치했다. 문맥 없이 관측 가능한 배포물 형태가 선명할 때 후보 속성형 색인이 유용할 수 있다는 반례다. 다만 실제로 문맥을 가린 별도 실험을 한 것은 아니며 두 코더에게 문제는 보였다. κ=1의 bootstrap에서1812/5000개가 단일범주라 미정의였으므로 남은 [1,1]을 확실성의 근거로 쓰지 않는다. 이 층은 URL 규칙으로 나눴고 결과를 보고 쉬운 라벨만 골라낸 것이 아니다.

다른 분야에서도 M09의 main-entry 일치는99/106=93.4%지만 subject field는44/106≈41.5%, 전체 record는5/106≈4.7%였다. 고정 필드의 높은 재현성과 의미 분류의 낮은 재현성이 공존한다. [M09](https://files.eric.ed.gov/fulltext/ED413903.pdf)

### 4.2 문맥을 붙여도 낮은 일치

T036 28개는 S1 27/28=96.43%인 반면 S2 17/28=60.71%(κ=0), S3 16/28=57.14%(κ=−0.034)다. A는 comparison을011 전체에서0개, B는14개 사용했다. 그중 T036의 비교 기준/설계 참고 경계가 반복된다. 코드북은 명시적 **기준**도 comparison에 포함하므로 A가 실명 비교 대상이 없다는 이유로 reference에 둔 것은 더 좁은 적용이었다. 사후에 이를 고치지 않았다. 이는 S2의 본질적 불가능성보다 규칙 적용의 비대칭을 지지하는 대안 설명이다.

T041의 S3는5/11=45.45%다. 목록을 document/data로 나누는 규칙과 주 후보를 어디에 두는지가 걸린다. T054는1/3이지만 작은 n=3이라 일반화하지 않는다. S3가 형태와 기여를 분리해도 입력의 실제 복수 대상·사용 문맥 부족은 자동 해소되지 않는다.

### 4.3 012의 높은 Po를 깨뜨리는 층별 검사

'''
text+=table(['012 연결 방식','안','일치/단위','Po','Po 95% 구간','κ 95% 구간','κ 미정의 복제/5000'],[metrics_row(r) for r in g['strata_012'] if r['scheme']!='S3_form'])
text+='''

무작위 연결36개에서 S2는34/36=94.44%지만 κ=0.321이다. A의 none34개, B의 none35개로 우연 기대 일치가0.918까지 높아졌기 때문이다. 실제 qrel 연결24개만 보면 S2는20/24=83.33%, κ=0.751이다. 따라서 전체60의90%를 실제 추천 상황의 역할 재현성으로 제시하면 과장이다. registry 층에서도 S2는25/27이지만 B가전부none이라 κ=0이다. 이 결과는 role과 retrieval relevance를 구별하되 문제 연결 자체가 없는 표본의 영향을 별도로 보라는 경고다.

## 5. S3의 축별 분해

'''
text+=table(['표본','n','두 축 모두 일치','기여만 일치·형태 다름','형태만 일치·기여 다름','두 축 모두 다름'],[[x['sample'],x['n'],x['both_axes_agree'],x['contribution_agrees_form_differs'],x['form_agrees_contribution_differs'],x['both_axes_differ']] for x in g['S3_decomposition']])
text+='''

011 형태축 자체는94/120=78.33%, κ=0.728이고 결합은75/120이다. S2 κ=0.538보다 S3 κ=0.561이 조금 높아도 Po는70.83%에서62.50%로 낮아진다. 범주가 달라 Pe가0.369에서0.146으로 내려갔기 때문이다. **κ만으로 S3가 더 잘 재현된다고 읽으면 안 된다.** 두 축을 묶었을 때 Po가 각 축을 넘을 수 없다는 것은 정의상의 성질이며 S3의 정보 가치에 대한 실험 결과는 아니다.

`unknown/mixed`를 어느 쪽이든 사용한 행을 사후 빼면011의 S1은82/92=89.13%, S2는83/106=78.30%, S3는64/87=73.56%가 된다. 이는 난해한 행을 제거한 선택 효과이므로 주 결과는198개 전부를 유지한다. 상세 규칙별 결과는 agreement.json의 sensitivities에 있다.

## 6. 불일치 59개 진단

전체198개 중 적어도 한 축이 다른 고유 단위는59개(011 47, 012 10, 004 2)다. 내부 별도 진단자가 전체 패킷·A/B 이유를 읽어 제안하고 작업자가59행 모두 검토했다. 유형은 **경계 정의 부족35/59, 문맥 부족18/59, 실제 다의성6/59**다. 원 제안은 [diagnostic-proposal.json](evidence/diagnostic-proposal.json), 채택·유보 메모는 [adjudication.json](coding/adjudication.json)에 별도 보존했다. 원 A/B 라벨과 일치도는 수정하지 않았다.

| 유형 | 구체 사례 | 진단 근거 | 해결해도 남는 점 |
| --- | --- | --- | --- |
| 경계 정의 부족 | 004-R07, 011-T047-032, 012-bazel-cache | 하위 기능을 component로 볼지 독립 service가 제공하는 product로 볼지 | '후보'가 배포물인지 기능인지 먼저 고정해야 한다 |
| 경계 정의 부족 | 011-T036-005·014·022 | 비용 방법 reference와 명시적 평가기준 comparison 중첩; A/B 우선 규칙 상이 | A의 규칙 오적용 가능성과 코드북 중첩을 분리할 새 표본 필요 |
| 문맥 부족 | 011-T011-005, 011-T053-002 | 이름·기능 요약만으로 app/service/library를 보충하는 정도가 다름 | unknown도 합법 값이지만 배경지식 사용 여부를 통제해야 한다 |
| 문맥 부족 | 012-otel-wal | broker 금지라는 부정 조건만 있고 양의 목표가 없다 | 상위 문맥을 추가하는 것은 새 입력 실험이다 |
| 실제 다의성 | 011-T036-008, 011-T054-003 | 평가 기준·구현 조언 또는 모델·설정이 실제 함께 존재 | 하나의 대표 역할인지 복수 동급인지 원 의도 확인 필요 |

경계 정의 부족에는 경계 중첩과 이미 있는 규칙의 상이한 적용이 함께 포함된다. 진단자가 실제 인지 원인을 관찰한 것이 아니므로 이 비율을 보편적 원인 분포로 쓰지 않는다.

## 7. 50%를 해석할 비교 기준

고정 역할의 안정적 재현을 전제로 후속 측정을 한다는 주장에는 원50.34%와 κ0.382가 약한 근거다. 그러나 색인어 집합의 Hooper overlap과 단일 역할의 정확 일치는 분모가 달라, 색인 연구의20–40%를 들어50%가 보통이라고 정당화할 수도 없다. M01은63명×초록3개의 조건별 overlap이27.7–39.5%, M10은이미지20개×8명에서평균27.1%, M14는기관레코드82쌍에서정확16%·부분36%였다. 어느 것도 이번 명목 라벨 정확 일치의 합격선이 아니다. [M01](https://informationr.net/ir/16-4/paper502.html), [M10](https://www.researchgate.net/publication/235290123_Inter-indexer_consistency_in_graphic_materials_indexing_at_the_National_Library_of_Wales), [M14](https://yunus.hacettepe.edu.tr/~tonta/yayinlar/indxcons.htm)

소프트웨어 topic3,000개의 application-domain 필터도3명 alpha0.68, 쌍별0.79/0.68/0.52였다. 주변 양성496/370/238의 차이가 판단 기준 차이를 드러낸다. [M02](https://arxiv.org/pdf/2205.09379) 내용 분석의0.667/0.8은 목적 의존적 관례로 다루고 자동 합격선으로 사용하지 않았다. 높은 일치도 타당성·후속 판정의 무오류를 뜻하지 않는다. [M04](https://aclanthology.org/J08-4004.pdf), [M11](https://aclanthology.org/J96-2004.pdf), [M13](https://aclanthology.org/J08-3001.pdf)

## 8. 한계와 재현

같은 모델·같은 요약 입력, 작업자의 선행 라벨 노출, 이름 지식의 비대칭 사용, 비교 기준의 규칙 적용 차이, 012 무작위 연결, 작은 cluster가 핵심 한계다. 같은 후보를 여러 실제 문제에서 반복한 통제 표본도 부족하다. exact candidate 문자열196종/198행이며 정확 반복은2그룹뿐이다. 보조 확인에서 Form Tools는같은문제의whole 유지, AlternativeTo는서로다른문제에서whole→none, SQS는요구변형에도whole 유지였다. AlternativeTo의 두 번째는 무작위 연결이므로 이를 실제 추천 성공 사례라고 하지 않는다.

Hooper1965·Markey1984 지정 원문은 추가32검색 질의와10개 URL 시도 뒤에도 원문 본문을 확보하지 못했다. 후속 문헌으로 대신 읽었다고 계산하지 않는다. [reliability-supplement.md](evidence/reliability-supplement.md)에 실패·다음 접근 경로를 기록했다. Cohen1960 원논문도 미열람이며 동일 저자의1986 회고 M06과 다른 지표 원문들을 사용했다.

재현: 저장소 루트에서 `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/analyze.py`, 이어서 `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/render_agreement_impact.py`. analyze.py는 동결 입력을 읽고 수치 파일만 생성한다. 원 코딩이나 코드북을 수정하지 않는다. 분석 함수의5개 의미 검사는 [analysis-method-checks.json](evidence/analysis-method-checks.json)에 있다.
'''
(BASE/'AGREEMENT.md').write_text(text)
text='''# AF-RES-016 — 역할 불일치가 판정을 바꾸는가

## 1. 결과와 해석 범위

59개 불일치 단위를 정렬하고 균등 간격으로 고른 **고유30개**를 검토했다. 같은 문제·후보·제안 사용·설정·근거를 고정한 작업자 문서 재판정에서는 **역할명만 달라서 H/T 또는 근접 오답 여부가 바뀐 경우는0/30**이다. 구성은 알려진 실패1개, 근거 부족14개, 전체 판정 라벨 미부여15개(조언·비교10개, 필수 판정 기준이 부족한 실제 대안 제안5개)다. 이는 사람에게 역할 표지를 보여 주었을 때의 인과 실험이 아니다. 많은 unknown이 그대로라는 결과를 충분한 근거 아래 무영향이 입증된 것으로 세지 않는다.

A/B 때의 H/T 판단은 원 A/B 코더가 별도로 제출한 값이 아니다. 사례별로 양쪽 역할의 의미와 같은 요구·근거를 대조한 뒤 수기 판단 하나를 양쪽 표시에 재사용했다. 따라서0/30은 두 H/T를 독립적으로 재코딩한 실험에서 얻은 변화율이 아니다. **작업자 GPT-6 Astra Pro가 동결한 두 역할을 조건으로 작성한 사후 문서 판단(H)**이다. 004-R03의 고정 연구자 기대판정과 I01–I03 후속 공식 본문을 참조했다. 실행한 것은두 toy 반례와 잘못된 역할 필터의 계산뿐이며 실제 후보 설치·통합 성공을 주장하지 않는다.

## 2. 비교 방법

004의 단위 `문제 × 후보 × 제안한 사용 × 설정 × 제공 근거`를 유지했다. `part/reference`라는 라벨만으로 원 must를 `not_in_scope`로 지우지 않았다. `prefer`를 must로 올리지 않았고, `force=unclear`이면 정확한 요구를 만들어 넣지 않았다. 원 proposal이 비어 있는012 후보에는 '이것만으로 전체 충족'이라는 주장을 추가하지 않았다. [고정004 PROTOCOL](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md)

선택 ID는 [impact-selection.json](evidence/impact-selection.json)에 동결 후 규칙대로 보존했다. 59개 중 순서통계 인덱스 `round(i×58/29), i=0..29`로30개를 골랐다. 영향이 큰 행만 고른 표본은 아니나 모집단 무작위 추출도 아니다. 각 행의 이유·반박 검토·최소 다음 확인은 [impact.json](evidence/impact.json), 수기 판단을 직렬화한 원 스크립트는 [build_impact.py](evidence/build_impact.py)에 있다.

`H: must 미제공/unclear`는 pass가 아니다. `전체 판정 라벨 미부여`도004의 새로운 상태값이 아니다. 조언·비교10개와 필수 판정 기준이 부족한 실제 대안 제안5개에 전체 적합 라벨을 붙이지 않았다는 설명이다. `N 미입증`은 관련성0이나 적합 판정과 다르다.

## 3. 30개 고정 사용 비교

'''+t2()+'''

### 3.1 대표 사례의 실질 검사

**R03:** 표준인지 패턴인지 다르지만 같은 도착 순서 구성을 평가한다. local 수정은pass, log에서 본문 복원은unknown, 순서 무관 수렴은fail이다. 동일 초기문서에 A/B replace를 역순 적용해 실제 toy trace가 서로 다른 최종값을 냈다. 표준/원리라는 형태가 기능 보증을 대신할 수 없다. [I03](https://www.rfc-editor.org/rfc/rfc6902.html), [toy-counterexamples.json](evidence/toy-counterexamples.json)

**T036 비교 기준6행:** 비용·선택법을 reference로 볼지 comparison으로 볼지 다르지만, 보안·총비용은prefer이고 구체 구현 승인 주장은 없다. 기준을 제시했다는 것과 기준에 합격했다는 것은 다른 사실이다. 이 범위의 역할 불일치는 H/T 판정을 바꾸지 않는 명명 차이에 가깝다.

**T027과 T010:** 부분 기여라는 라벨로 원래의 판매 제한·안전한 결제 조건을 삭제하지 않았다. 구현 연결이 없는 것은 두 역할 모두unknown이다. 별도 좁은 데이터층/UI층의 평가를 하려면 새 사용 행을 만들어야 한다.

**Briefpanel·Iggy·ZFS:** 내부망 사용, 복제, 한 디스크씩 증설을 원 입력의 새로운 must로 추가하지 않았다. 당시 댓글의 기능 한계가 현재 버전의 사실이라는 주장도 하지 않았다. 역할 변경보다 요구·관측 창을 바꾸는 오류가 더 결정적이었다.

**aiolimiter:** part와none 중 어디에 놓든 빈 proposal은 전체 상한 보장 주장이 아니다. 다만 '시간 기반 limiter만으로 처리중≤4를 보장한다'는 별도 가정은 반례가 있다. 1초마다 하나를 들이고 각 작업이10초 지속되면4.5초 시점에5개가 처리 중이다. 이 toy는 허용 스케줄의 계산이며 실제 라이브러리를 실행한 것은 아니다. [I02](https://aiolimiter.readthedocs.io/en/stable/)

**OTLP exporter:** 후속 공식 문서 I01은 Python SDK의 전송과 Collector pipeline의 후단 exporter 구성을 구별한다. 같은 exporter라는 이름이나 component라는 역할로 Collector 내구 queue 설정을 입증할 수 없다. 원 패킷만으로 방향을 확정했던 B의 배경지식도 동결 결과에 그대로 남겼다. [I01](https://opentelemetry.io/docs/languages/python/exporters/)

## 4. 역할 해석이 사용 단위를 바꾸는 조건부 대비

SQLite 테이블 큐와 기존 Postgres 테이블/확장 큐2개는 A의 실행 부품/whole 해석과 B의 방법/reference 해석이 다른 사용 단위를 가리킬 수 있다. 다음 대비는 **연구자가 새 가정을 붙인 H 예시**이고 주0/30의 분자에 넣지 않았다.

| 원 ID | 추가 가정 A | 추가 가정 B | 조건부 T 차이 | 보존할 H | 확인이 필요한 것 |
| --- | --- | --- | --- | --- | --- |
| 011-T039-009 | 이미 실행 가능한 큐 부품과 인터페이스를 직접 사용 | DB의 행을 메시지처럼 쓰자는 참고만 있고 claim/ack·중단 복구 대응 없음 | not_needed → analogy_only | OSS·ZooKeeper 금지는 유지; 실제 큐 보장 미확인 | 원 제안이 구현체인지 원리인지, 구체 연결·실패 조건 |
| 011-T047-018 | 실제 제공된 큐 확장을 기존 인터페이스로 직접 사용 | 기존 DB 관계를 새 큐 설계로 옮기자는 거친 비유 | not_needed → analogy_only | 필요한 신뢰성 값을 먼저 명시; pass 자동 부여 금지 | 기존 Postgres 전제와 확장 구현, 메시지 상태 대응 |

원 패킷에는 이 추가 가정이 없어 T는unknown으로 남았다. 상세 대응·연결·실패 조건까지 새로 주면 다른 `reference_design`의 mapped 후보가 될 수 있지만 그때도 구현 성공은 별개다. 이는 역할명 변경의 효과가 아니라 **proposed_use와 근거가 달라졌을 때 다른 판정 질문이 된다는 사례**다. 따라서 문제 상대 역할을 저장할 때 사용 범위와 구체 제안을 함께 남겨야 한다는 권고는 유지하지만, 실제 판정 변화율2/30이라고 보고하지 않는다.

## 5. 역할 표시가 잘못된 필터가 되는 반례

'선택 범위 전체를 대체할 후보는 S1=product만 남긴다'는 잘못된 규칙을 실제18행에 적용했다. 이 규칙은 의도적으로 만든 연구자 가정(H)이며 적용 계산만D3-run이다. 정답 참조도004의 연구자 문서 EXPECTED이지 외부 금표준이 아니다.

두 코더 모두 DIRECT_DOCUMENTED7개 중 **R01·R02·R10의3/7을 탈락**시킨다. 세 후보는 component이지만 선택된 부품 범위에서는 whole이다. 반대로 product 통과 후보는A에서7개 중알려진 mismatch2개(R16·R18), B에서8개 중3개(R07·R16·R18)를 포함한다. 형태는 필수 요구 충족을 대신하지 않는다. [role-filter-counterexample.json](evidence/role-filter-counterexample.json)

S2=whole만 통과시키는 규칙도 R03 등실패 후보를 남긴다. 이번18행에서 S2 whole15개 중 DIRECT7·INSUFFICIENT2·MISMATCH6이다. 따라서 S2가004에서18/18로 재현되어도 판정 정확성의 대리 지표가 되지 않는다. 검증된 효용은 L/E/H/T와 구체 근거로 판단해야 한다.

## 6. 한계와 다음 확인

이 분석은 통제한 문서 판단의 일관성을 검사했으며, 역할 표지가 실제 사용자나 자동 판정기에 주는 영향은 시험하지 않았다.30개 중14개는INSUFFICIENT이고15개는전체 라벨 미부여다. 후자는 조언·비교10개와 필수 판정 기준이 부족한 실제 대안 제안5개로 구분된다. 이 구성에서0변화는 역할 무영향의 상한 추정도 아니다. 원인별 영향 비율이나 인과 효과를 계산하지 않는다. 내부 별도 검토 [impact-independent-review.md](evidence/impact-independent-review.md)는 이런 오판 위험을 확인한 검토이며 새로운 사람/모델 실험이 아니다.

최소 후속 확인은 실제 proposed_use가 명시된 불일치30개를 새로 모아 역할 표시 없음/A/B를 무작위 배정하고, 원 코딩을 보지 않은 평가자가 같은 H/T를 판정하는 것이다. 현재 가정2개는 원 제안의 사용 문장부터 정상 공개 원문에서 확인해야 한다. 이 작업은 수행하지 않았으므로 실행 입력·절차는 HANDOFF에 남긴다.

재현: `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/build_impact.py`; `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/toy_counterexamples.py`. 이 명령들은 수기 판정을 직렬화하거나 toy 계산을 재현할 뿐 원 추천의 실효성을 시험하지 않는다.
'''
(BASE/'IMPACT.md').write_text(text)
print('wrote AGREEMENT.md and IMPACT.md')
