# AF-RES-020 — 충돌 등록부

## 1. 읽는 법

REVIEW-4 §3의 원11행을 CF01–CF11로 전부 보존하고, 이번 재대조에서 CF12–CF16을 추가했다. 계획 검토는 목록의 출발점이며 사실 근거는 각 행 아래에 연결한 **고정 SHA의 원 결과**다. 계획 검토 위치는 `work/planning@b373862baf009f3f8d37ac01b5437530434f7d31`의 `docs/workstreams/planning/REVIEW-4.md` L173–189이다.

- **경험적:** 같은 고정 대상·정의 또는 같은 순위파일을 두고 실제 판정/결과가 다르다. 원인의 일부가 정의·근거 범위 차이일 수 있으므로 인과 원인까지 단정하지 않는다.
- **정의상:** 같은 이름이 다른 질문·단위·상태를 가리킨다. 수치가 다르거나 같다는 사실만으로 경험적 오류로 바꾸지 않는다.
- **범위 차이:** 문제·표본·처치·관측 창·측정 대상이 다르다. 조건을 맞추기 전에는 승패로 합치지 않는다.
- **해소:** 현재 전달상의 충돌을 원 정의·집계로 설명했다. 제품 효과가 검증됐다는 뜻이 아니다. **부분 해소:** 정의/단위를 나눴지만 선택을 가를 관측 또는 원 기록 정정이 남았다. **미해소:** 현재 자료로 설계 선택을 가를 수 없다.

최소 규모는 별도 표기가 없는 한 **H: 다음 결정을 바꿀 진단용 입력 제안**이다. 검정력 계산·모집단 발생률 추정에 충분한 규모라는 뜻이 아니다. 원 작업의 작성자·내부 별도 코더가 만든 판정을 이번 감사가 외부 정답으로 승격하지 않았다. AF-RES-017~019의 결과는 읽지 않았으며 해당 이름은 대기 입력 자리만 표시한다.

## 2. 충돌 등록부

| 충돌 ID | 관련 묶음 | 어긋나는 내용(수치 포함) | 성격(경험적·정의상·범위 차이) | 현재 상태 | 해소에 필요한 최소 증거 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| CF01 | B04 · B07 · B12 · B14 · B15 | 011의 원 역할 재코딩은 75/149=50.34%였다. 016의 같은 120개 부분표본은 원 66/120, 새 S1 형태 94/120, S2 기여 85/120이며, 다른 012 표본의 S1은 59/60이다. 후보 형태와 문제 상대 기여, 013의 기능·분야·관계 역할축을 같은 변수로 합칠 수 없다(동결된 같은 모델 내부 코딩 창). | 정의상 | 부분 해소 | 질문: 형태와 기여를 분리하면 새 실제 문맥에서도 경계 판정이 재현되는가? 자료: 선택 범위·proposed_use를 포함한 새 사례와 코드북 버전. 규모: H 60단위(형태 경계30·기여 경계30), 코더3명; 원198개를 재훈련 평가에 재사용하지 않는다. | 미확인(사람 간 재현성·새 표본의 코더 및 요약 효과를 분리해야 함) |
| CF02 | B01 · B02 · B11 · B13 · B23 | 011 부분33질문의 진전 신호는 명시 선택/사용6 + 현재 accepted5 − 중복1 = 10/33이며 통합 성공이 아니다. 012 합성 발췌는 whole12/part24의 nDCG .343/.238, 014 실제 질문 유형은 whole28/part33(양성28/31)의 nDCG .4073/.3792·recall .3623/.4306이다. 014 I5 없는 부분은4/33이고 nDCG .25다. | 범위 차이 | 부분 해소 | 질문: 같은 질문에서 주변 입출력 I5를 보존하면 부분 입력의 판정이 개선되는가? 자료: 최초 원문·부분 발췌·I5만 추가한 입력·동일 qrel. 규모: H 실제12질문×3입력; I5 결핍6개 이상과 선택 반응/통합 후속 기록을 별도로 수집. | 미확인(현재4개 I5 결핍 및 다른 질문 유형 비교로 문맥 추가의 인과 효과를 정할 수 없음; 대기 중인 입력: AF-RES-018) |
| CF03 | B06 · B13 · B14 · B23 · B24 | 012 D-b→D-c는 N 85→163/216질의·조건(6셀×36; 슬롯2160), 평균 .3935→.7546이다. 014는 N17→11/183질의·조건(3방식×61; 슬롯1830), 평균 .0929→.0601이다. 012 문서156/합성36질의와014 문서485/고정 요약61질의·추가 한계 신규15문서는 다른 처치다. 필터의 GGL 제거는 답 등급과 제약의 차이이고 Word 제거 반례는 ‘불필요→금지’ 오독이다. | 범위 차이 | 미해소 | 질문: 같은 한계·질의·qrel에서 인라인/별도 필터의 N 방향이 유지되는가? 자료: 동일 문서의 한계 원문·범위·판, 실제 조건별 양성 및 알려진 N, 고정 검색 코드. 규모: H 실제30질문·N30쌍 이상·관련60쌍 이상에 동일 비율로 한계를 넣고 세 처리 조건을 재생. | 미확인(014의 N9쌍과 신규 한계15문서만으로 보편 방향 판단 불가; 학습 임베딩 미실행) |
| CF04 | B03 · B08 · B12 · B15 · B21 | 010은 분야 힌트가 포함된2문제·64고유 웹 질의에서 조건부 새 family7개를 찾았다. 011은 전이 표현14답/5스레드의 질문자 반응0/14, 012는 원리 양성32질의의 개선15·하락11·동일6, 013은 결정일2000–2023의 gold176 중 구조 차용1·외부 다른 분야 인용0이다. 발견·반응·회수·인용은 수요와 같은 측정이 아니다. | 범위 차이 | 미해소 | 질문: 늦게 알게 된 다른 분야 원리가 실제 선택·재작업을 바꿨는가? 자료: 결정 전후 기록, 발견 시각, 후보의 관계·bridge·실패 조건, 가까운 분야 대안. 규모: H 실제12결정(원거리6·가까운 대안6), 각 후보를 실제 적용 맥락에서 비교할 판정2개. | 미확인(무인용·무반응을 무가치로 해석할 수 없음; 대기 중인 입력: AF-RES-017) |
| CF05 | B09 · B10 · B14 · B15 · B20 | 009 H1은 같은 예산의 기존 LLM+코드 검색+목록+원문 확인 조합보다 대응 기록이 검토를 줄이는지, H2는 변경 뒤 재검토 가치다. 013의2026-11-20 검색에서 역사 gold 적중 A16/176·B5/176과 좁은 문서상 정답 밖 참고 A170/178·B109/120은 함께 성립한다. 새 절차와의 쌍대 비교 및 더 나은 실제 설계 확인은0건이고 H2는 미평가다. | 범위 차이 | 미해소 | 질문: 같은 입력·예산에서 구조화 기록이 초기 검증 또는 변경 후 재검토를 개선하는가? 자료: 접두부·기존 조합·새 절차·원문 근거·검토 시간, 알려진 변경. 규모: H 실제12결정과 변경12건을 두 성과 창으로 분리 비교하고 결정적 제약 오류를 사전 고정. | 미확인(낮은 역사 recall·높은 조건부 참고 수만으로 기존 조합의 충분성이나 제품 우위를 결정할 수 없음; 대기 중인 입력: AF-RES-018) |
| CF06 | B05 · B10 · B16 · B17 | 011의 단회 URL관측281회 중 명시404는4URL/3스레드다. 015는 답 날짜2014-05-05~2026-11-16에서2026-11-20까지 당시 성립·현재 알려진 이유83개 중 후발 변화5행(4사건)이다. 015 HTTP판정92행에서404/410은 적중0·놓침3·오경보2였고 archived124행은 적중0·놓침5·오경보10이었다. 주소 생존과 이유 성립은 다른 상태다. | 범위 차이 | 부분 해소 | 질문: 사건 전에 얻은 값싼 신호가 이유 재검토의 우선순위를 개선하는가? 자료: 사건 전후 시점·원 이유·후보 중복을 제거한 신호 시계열·같은 유형의 안정 대조. 규모: H 고유 후발 사건20건과 안정 대조40건, 최소2관측 시점 및 사건 유형3종. | 미확인(현재/상속 신호뿐이고 사건3–5행으로 선행 예측·운영 점검 주기 판단 불가; 대기 중인 입력: AF-RES-019) |
| CF07 | B03 · B07 · B08 · B18 · B20 | 초기 결과의 D3는 주로 제품 직접 실행을 뜻했고 002의 실제 검색 기록·003의 maintenance 페이지 관측은 D1/D2와 함께 기술됐다. 013~016은 D3-search(검색 반환), D3-fetch(페이지/API 응답), D3-run(직접 실행·집계)을 분리한다. 외부 저자 실행을 읽은 것은 이번 관측 D1이며 D4 적용과 다르다. | 정의상 | 해소 | 질문: 같은 관측을 새 어휘로 바꿔도 수행 사실과 미실시가 보존되는가? 자료: 원 관측 기록·실행 영수증·코드 위치. 규모: H 주요 주장 중 검색·응답·실행 각3건을 원 기록과 이중 점검; 현재 조립의 분류표와 원 표기를 나란히 보존. | 미확인(원 작업의 모든 세부 주장을 재분류한 것은 아님; 개별 실행 주장 채택 시 영수증 대조 필요) |
| CF08 | B03 · B08 · B11 · B13 · B14 · B15 · B17 · B18 | 010의64는 고유 웹 질의, 012의156은 색인 자료, 011의635는 답/독립 후속 응답, 013의176은 gold항목(외부 실체30), 014의485는 자료(한계 변경171=기존156+신규15), 015의500은 이유(현재 판단195), 016의198은 코딩 단위(011120+01260+합성00418)다. 같은 연구량·독립 표본 수로 합산할 수 없다. | 범위 차이 | 부분 해소 | 질문: 숫자를 옮길 때 단위·중복·판정자·관측 창을 재구성할 수 있는가? 자료: 각 원 JSON/CSV, 필터·join 규칙과 고정 SHA. 규모: H 이7개 headline 집계 전부와 중복 제거 경계2개(010 family7/행합9,013 두146)를 산술 재검사. | 미확인(각 표본은 편의·합성·사건 단위가 혼합되어 대표성이나 교차 연구 효과량을 추정하지 못함) |
| CF09 | B07 · B11 · B12 · B14 · B15 · B24 | 011의 엄격 근접오답16쌍/11스레드는 본표본10쌍과 보완6쌍이다. 014의 실제 답 초기299쌍에는 자료집 내 N9쌍, 013의 좁은 참고 사용 판정342후보에는 확정 제약 위반0/342가 있다. 016 product-only 가정 필터는004의 문서상 DIRECT7개 중3개를 버린다. 네 숫자는 실제 반박·매핑된 N·작성자 참고 판정·필터 누락으로 서로 다른 사건이다. | 범위 차이 | 미해소 | 질문: 알려진 나쁜 후보와 유용한 좁은 참고가 같은 규칙에서 구별되는가? 자료: 추천 전 필수조건·실제 반박·후보 proposed_use·충분한 원문·qrel 출처. 규모: H 실제30질문에 알려진 N30쌍·조건부 참고30쌍을 섞고 맹검 판정2개 이상을 비교. | 미확인(013의0/342는 나쁜 후보 발생률0이나 완전한 변별력을 뜻하지 않음; 대기 중인 입력: AF-RES-018) |
| CF10 | B06 · B07 · B16 · B17 | 015에서 현재 판단 가능한 이유195/500 중 무너짐14개에는 초기 오류가 섞여 있다. 당시 성립·현재 확인 가능한83개 중 후발 변화5행(4사건; 긍정 속성만4행)과 답 이전부터 틀린4개 이유는 별개다. 4와5를 같은 위험률로 비교하거나14/195·5/83을 연간 사망률로 쓰면 안 된다(확인일2026-11-20). | 정의상 | 부분 해소 | 질문: 추천 시점 검증과 후발 유지 중 어느 확인이 결정적 오류를 더 줄이는가? 자료: 날짜가 있는 추천 원문, 당시 및 현재의 독립 근거, 고유 사건ID·변화 방향. 규모: H 날짜가 있는 이유100개 중 초기오류10·후발변화10 이상을 진단 표집하고 두 종류 비용을 별도 보고. | 미확인(현재4초기오류·5후발행으로 두 위험의 모집단 크기 또는 비용 우위를 판단할 수 없음; 대기 중인 입력: AF-RES-018·AF-RES-019) |
| CF11 | B07 · B12 · B14 · B15 · B18 | 같은012의15질의에서 풀링 qrel은 nDCG M2 .335327>M3 .334482, 내부 별도는 M3 .308483>M2 .307296다. 같은014의10질의도 실제 답 RRF .4035>LSA .3313에서 내부 별도 LSA .4449>RRF .4357로 바뀌며, 관련 양성 합집합12쌍 중 공통3쌍(전체279/290 일치)이다. 013의 낮은 역사 적중과 높은 조건부 참고도 다른 판정 질문이다. 주성격 ‘경험적’은012의 같은 평가 목적에서의 판정자 민감도에 한정하며,014의 실제 답 grade와 내부 must 판단은 정의·범위 차이 성분이다. | 경험적 | 미해소 | 질문: 관련성 정의와 근거 범위를 고정한 독립 판정에서도 방식 순위가 유지되는가? 자료: 같은 순위파일·질의·원 조건·두 qrel의 판단 근거. 규모: H 공통15질문과 양성/근접경계60쌍 이상, 판정원3종; 순위와 effect 차이·양성 교집합을 함께 보고. | 미확인(판정 근거 범위·기준이 달라 어느 qrel이 참인지 또는 어느 검색 방식이 우월한지 결정 못 함) |
| CF12 | B07 · B12 · B14 | 016의 동일 코드북·동일011표본120개에서 S2 comparison을 코더A는0/120, B는14/120 사용했다. S2 전체 일치는85/120이다. 두 코더의 S3 contribution은 각자 S2와198/198 같아 이 차이는 독립 반복이 아니다. Q7의0/30은 공통 수기 판정 재사용이며 역할 표시의 인과 효과가 아니다. | 경험적 | 미해소 | 질문: comparison/reference 우선 규칙을 고정하면 새 문맥에서 비대칭이 줄어드는가? 자료: 새 코드북·훈련 예·원 선택 범위와 명시 사용. 규모: 원016 제안에 맞춘 H 새60단위(비용/기준30+실행/정보원30), 독립 사람 코더3명; 원120개는 보존하고 새 평가에서 제외. | 미확인(같은 모델·A의 선행 라벨 노출을 제거한 재현성; 0/30에서 표시 효과를 추정할 수 없음) |
| CF13 | B06 · B07 · B12 | 004 HANDOFF L80의 단위는 문제×후보×역할×설정×근거이나 같은SHA PROTOCOL L24는 문제×후보×제안한 사용 방식×명시 설정×제공 근거이며 역할은 별개다. C-B07-04의 실제 전달 불일치다. 역할만 저장하면 같은 component의 다른 사용을 복원하지 못한다. | 정의상 | 부분 해소 | 질문: role만 같은 서로 다른 사용에서 판정이 갈리는가? 자료: 동일 후보·역할·다른 proposed_use와 근거. 규모: H 실제3쌍을 두 독자가 복원하고 축약 정의로 합쳐지는지 검사; 원004 문서는 편집 담당이 별도 정정할지 결정. | 미확인(조립본은 PROTOCOL을 우선했으나 원 HANDOFF 정정 여부는 편집 담당 결정) |
| CF14 | B12 · B14 · B15 | 013의 역할 ‘같은 분야의 다른 설계’146/176과 종류 structural_design146/176은 교집합142, 각 차집합4다. 역사A 적중이 역할표7/146과 종류표8/146인 것은 수치 오류가 아니다. 결정일2000–2023·2026-11-20 실행의 같은176gold라도 분류 축이 다르다. | 정의상 | 해소 | 질문: 두 축의 서로 다른 원ID 집합과 적중이 재구성되는가? 자료: cases/CASES.json의 role·match_kind와 역사 집계. 규모: 현재176gold 전수 join과 차집합8개를 직접 대조 완료; 향후 H 새 집계마다 두 축 교차표를 유지. | 미확인(분류 축을 바꾼 새 표본의 효과는 별도 평가 필요; 현재 두146 집합 차이는 확인 완료) |
| CF15 | B18 · B20 · B22 | 고정 foundation 진행표는013·016을 DONE으로 기록한다. 그러나 고정013 HANDOFF L6은 BLOCKED—SITE_CAP_CASES, 016은 core_artifacts_complete_with_blocked_named_original_reading(지정 고전2편 미열람)이다. 이 원 상태는 020의 정규화 REVIEW_READY_WITH_GAPS 제안이나 제품안 채택과 동일하지 않다. | 정의상 | 부분 해소 | 질문: 진행표의 인수 판단과 원문 공백을 동시에 추적할 수 있는가? 자료: 두 작업의 원 HANDOFF·SELF_CHECK·인수 근거와 진행표 상태 변경 기록. 규모: 해당2작업에 원 상태/정규화 상태/인수 상태를 별도 칼럼으로 기록하고 편집 담당이 인수 이유1건씩 확인. | 미확인(원 상태를 달리 인수한 판단 근거의 확정은 진행·편집 담당 몫; dot-control은 수정하지 않음) |
| CF16 | B01 · B04 · B05 · B06 · B07 · B12 · B20 | H: 작게 시작해도 원 질문·원 라벨·proposed_use·근거 구간·확인 시각을 버리면 이행이 어려워진다. 후보 role 단일값만 남기면 형태/기여 분리에 필요한 원 판단을 잃고, live URL+날짜만 남기면 바뀐 원문을 복원하지 못한다. 단일 필드 자체의 실패를 실측한 것은 아니며 원 문맥을 따로 보존하면 이행 가능하다. | 범위 차이 | 부분 해소 | 질문: 작은 구성의 기록만으로 다른 구성의 의미를 복원할 수 있는가? 자료: 역할 경계·부정 범위·live 변경이 있는 기록, 원 질문/라벨 보존판과 삭제판. 규모: H6기록(유형별2)에서 두 이행 경로를 두 독자가 재구성하고 손실 필드·재수집 비용을 표시. | 미확인(실제 이행 비용·사용자 복원 정확도는 미측정; 설계 가설이며 특정 DB/필드 수를 강제하지 않음) |

## 3. 분류 이유와 원 근거 위치

### CF01 — REVIEW-4 §3 #1, L179

‘역할’이 가리키는 질문이 다르다. 50.34%와78.33%는 분모도149와120이므로 직접 차이가 아니며, S1/S2 분리는 정의 충돌을 줄여도 사람 재현성을 증명하지 않는다. 남는 같은 정의의 코더 차이는 CF12로 분리한다.

- [AF-RES-011 · HANDOFF.md · 원 절: 한계·미실시와 결론이 틀릴 수 있는 지점; 행: L147](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-016 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 분류안별 일치도; §2 세부 질문별 답 / Q6. 어느 안이 더 일치하고 왜 갈리는가; 행: L9–17, L160–164](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · CODEBOOK.md · 원 절: 1. 공통 규칙과 입력; 3. S2 문제 상대형 — 선택 범위에 대한 기여; 4. S3 두 축 — form × contribution; 행: L9–11, L25–41](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/CODEBOOK.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표 2 — 역할별 집계; §2 세부 질문별 답 / Q3. 정답 항목은 외부 실체보다 내부 설계 대안에 치우쳤다; 행: L43–50, L97–99](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.

방법 대응(조립 가설 H): X04, X08. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF02 — REVIEW-4 §3 #2, L180

질문자 반응, 검색 순위, 같은 문장 발췌, 서로 다른 질문 유형은 다른 결과다. 관측된 반응을 실제 통합 성공으로 승격하지 않고 효과 크기는 동등 입력에서 따로 묻는다.

- [AF-RES-011 · HANDOFF.md · 원 절: 5. 판단·근거 / Q1–Q8 결론과 적용 범위; 5. 판단·근거 / 고정 입력 판정; 5. 판단·근거 / 가장 강한 근거 세 가지; 행: L116–128](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-011 · CODEBOOK.md · 원 절: 1. 단위와 누락 / 1.1. 전체·부분 질문의 정의 — v1.2 명료화; 4. 답의 형태·역할·반응; 행: L16, L44](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CODEBOOK.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-012 · RESULTS.md · 원 절: Q5. 전체 질의와 부분 질의; 행: L80–89](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-014 · RESULT.md · 원 절: §2 세부 질문별 답 / Q5 전체·부분과 I5; 행: L90–99](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.

방법 대응(조립 가설 H): X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF03 — REVIEW-4 §3 #3, L181

방향은 반대지만 같은 것을 같은 조건에서 반복 측정한 충돌이 아니다. 평균 N/질의와 N/슬롯을 구별한다. T017은 relevance 정의 차이, T021은 의도적인 오독 시험이므로 둘을 같은 필터 오류로 합치지 않는다.

- [AF-RES-012 · RESULTS.md · 원 절: 서두(제목 아래); Q3. 한계 문장이 근접 오답을 줄이는가; 행: L5–9, L45–53](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-012 · metrics.csv · D-b L47,77,182,212,317,347; D-c L92,122,227,257,362,392](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/results/metrics.csv) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-014 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 조건별 지표; §1 필수 결과 표 / 표 2 — 012 결론 재현 여부; §2 세부 질문별 답 / Q2 자료집; §2 세부 질문별 답 / Q3 인라인·필터·감점; 행: L23–32, L61, L67–84](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.
- [AF-RES-014 · metrics.csv · D-b/D-c actual-answer all-query 조건 행](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/results/metrics.csv) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.

방법 대응(조립 가설 H): X08, X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF04 — REVIEW-4 §3 #4, L182

상이한 관측의 희소성을 같은 ‘수요0’으로 합치지 않는다. 010의 목표 mapping H와013의 실제 저자 인용도 증거 유형이 달라 방향 반박으로 사용할 수 없다.

- [AF-RES-010 · HANDOFF.md · 원 절: 상태; 2. 세부 질문별 결론과 적용 한계; 행: L5–7, L31–38](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/HANDOFF.md) — SHA `0603f0d2990c7a501dbdfc45fbbba79155f505fc`.
- [AF-RES-010 · comparison-counts.json · L1–6; new_family_groups L211–264](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/comparison-counts.json) — SHA `0603f0d2990c7a501dbdfc45fbbba79155f505fc`.
- [AF-RES-011 · HANDOFF.md · 원 절: 5. 판단·근거 / Q1–Q8 결론과 적용 범위; 행: L112](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-012 · RESULTS.md · 원 절: Q2. 목적과 메커니즘이 다른 분야 원리 발견을 늘리는가; 행: L41–43](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표 3 — 주장 표; §2 세부 질문별 답 / Q4. 다른 분야의 실제 인용: 구조 차용1건, 외부 자료 인용0건; §2 세부 질문별 답 / Q8. AF009의 반대 가설 A/B는 이번 결과만으로 기각되지 않는다; 행: L56, L103–116, L146](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.

방법 대응(조립 가설 H): X08, X12, X22. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF05 — REVIEW-4 §3 #5, L183

역사적 대안 복원, 현재 문서상 참고, 실제 설계 효용, 유지 효용은 다른 목표다. 동일한 강한 기준선을 유지하고 새 절차가 없는 결과를 비교 승리로 바꾸지 않는다.

- [AF-RES-009 · GAP.md · 원 절: 2. 반대 가설 A — “범용 LLM 검색이 이미 충분히 한다” / 지지하는 자료를 의도적으로 찾은 결과; 5. 남은 가설과 반증 가능한 다음 연구 / H1. 목적·부분·제약과 후보의 대응 기록; 5. 남은 가설과 반증 가능한 다음 연구 / H2. 제공자가 바뀌어도 이어지는 근거의 재검토; 5. 남은 가설과 반증 가능한 다음 연구 / H3. 별도 제품보다 기존 작업 도구의 작은 절차가 적절할 수 있음; 행: L73–79, L113–125](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md) — SHA `7f627a81199f06da7f7b15f979e7fef25dd17602`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표의 단위와 판정 책임; §2 세부 질문별 답 / Q5. 기준선 A: 전31사례의 실제 실행, 역사 적중16/176; §2 세부 질문별 답 / Q7. 채점: 적중·부분 참고·미해결 조건·링크를 분리했다; §2 세부 질문별 답 / Q8. AF009의 반대 가설 A/B는 이번 결과만으로 기각되지 않는다; 행: L65–73, L122, L134–146](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.

방법 대응(조립 가설 H): X08, X12, X22. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF06 — REVIEW-4 §3 #6, L184

404의 URL분모와 이유 변화의83개 분모는 직접 비교할 수 없다. 이유가 무너졌는데 주소가 살아 있는 반례는 차이를 입증하지만 신호의 장기 무용성을 입증하지 않는다.

- [AF-RES-011 · HANDOFF.md · 원 절: 5. 판단·근거 / Q1–Q8 결론과 적용 범위; 행: L115](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-015 · RESULT.md · 원 절: §1 필수 결과 표 / 표 2 — 신호 예측력; §2 세부 질문별 답 / Q3 답 시점 복원; §2 세부 질문별 답 / Q4 값싼 신호; §3 추가 분석; 행: L20–33, L65–71, L94–95](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) — SHA `e39d23c9a7307ba83c974580f60115d90e221084`.
- [AF-RES-015 · confusion.json · HTTP 404/410 및 GitHub archived의 strict 혼동표](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/results/confusion.json) — SHA `e39d23c9a7307ba83c974580f60115d90e221084`.

방법 대응(조립 가설 H): X12, X22. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF07 — REVIEW-4 §3 #7, L185

어휘를 관측 모달리티로 통일하면 충돌은 해소된다. 더 높은 숫자를 진실성 점수로 해석하거나 fetch/search를 제품 run으로 승격하는 것은 금지한다. 원 결과 파일은 덮어쓰지 않는다.

- [AF-RES-002 · RESEARCH.md · 원 절: 2. 조사 설계와 실제 읽은 범위; 행: L30–39](https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/RESEARCH.md) — SHA `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`.
- [AF-RES-002 · p1.json · queries L231–1088](https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/evidence/p1.json) — SHA `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1`.
- [AF-RES-003 · RESEARCH.md · 원 절: 5. 무엇을 더 저장할지: 필드보다 막아야 할 실패; 행: L101](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md) — SHA `b13db3931b4021ff9e1ac6e404590c09526c3087`.
- [AF-RES-004 · PROTOCOL.md · 원 절: 판정 단위와 증거 경계; v1.1 명확화 — 독립 v1 판정 이후; 행: L26, L81–85](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md) — SHA `2b798c7d2b7355b649691c18de196104ceabb0f0`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표의 단위와 판정 책임; 행: L73](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-014 · HANDOFF.md · 원 절: 서두(제목 아래); 행: L3](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/HANDOFF.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.
- [AF-RES-016 · RESULT.md · 원 절: §1 필수 결과 표 / 표 4 — 주장 표; §2 세부 질문별 답 / Q7. 불일치가 실제 판정을 바꾸는가; 행: L120, L170–174](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF08 — REVIEW-4 §3 #8, L186

숫자는 대체로 재집계와 일치하며 충돌은 전달 시 분모가 생략될 때 생긴다. 012/014의 N 평균은 질의·조건당 개수이고 상위10 슬롯 비율과10배 차이난다는 점을 CF03에 명시했다.

- [AF-RES-010 · comparison-counts.json · L1–6; rows와new_family_groups](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/comparison-counts.json) — SHA `0603f0d2990c7a501dbdfc45fbbba79155f505fc`.
- [AF-RES-012 · RESULTS.md · 원 절: 서두(제목 아래); 행: L5–9](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-011 · HANDOFF.md · 원 절: 3. 실제 변경과 자료 규모; 행: L34–37](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표의 단위와 판정 책임; §2 세부 질문별 답 / Q3. 정답 항목은 외부 실체보다 내부 설계 대안에 치우쳤다; 행: L65–71, L97–99](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-014 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 조건별 지표; §2 세부 질문별 답 / Q2 자료집; 행: L23, L61](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.
- [AF-RES-015 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 이유 유형별 노후화; §2 세부 질문별 답 / Q1 추천 이유 추출; §2 세부 질문별 답 / Q2 현재 유효성; §2 세부 질문별 답 / Q3 답 시점 복원; 행: L16, L59–67](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) — SHA `e39d23c9a7307ba83c974580f60115d90e221084`.
- [AF-RES-016 · RESULT.md · 원 절: §1 필수 결과 표 / 표 4 — 주장 표; §2 세부 질문별 답 / Q5. 이중 코딩은 어떻게 수행했는가; 행: L120, L156](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF09 — REVIEW-4 §3 #9, L187

정답원·필수조건·용도 범위가 다르고 필터의 적합 후보 누락은 근접오답 발생 빈도가 아니다. 정의상 차이를 포함하지만 핵심 비교는 서로 다른 표본·발생 과정의 범위 차이다.

- [AF-RES-011 · HANDOFF.md · 원 절: 3. 실제 변경과 자료 규모; 5. 판단·근거 / Q1–Q8 결론과 적용 범위; 5. 판단·근거 / 가장 강한 근거 세 가지; 행: L37, L114, L127](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-011 · CODEBOOK.md · 원 절: 5. L/E/H/T 대응과 추가 이유; 행: L64–66](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CODEBOOK.md) — SHA `478c301b693896e2c6d777f46ac441f071bfdfe8`.
- [AF-RES-014 · RESULT.md · 원 절: §2 세부 질문별 답 / Q1 실제 질문과 답; 행: L57](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표 3 — 주장 표; §2 세부 질문별 답 / Q7. 채점: 적중·부분 참고·미해결 조건·링크를 분리했다; 행: L60, L134–136](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-016 · RESULT.md · 원 절: §2 세부 질문별 답 / Q7. 불일치가 실제 판정을 바꾸는가; §3 추가 분석 / 3.2 요구된 반례 다섯 가지; 행: L174, L202](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X08, X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF10 — REVIEW-4 §3 #10, L188

처음부터 거짓과 나중에 변함은 시간 상태의 정의가 다르다. 정의와 행 중복은 분리했지만 상대 중요성은 측정하지 않았으므로 부분 해소다. OpenZFS 제약 해소를 부정적 서비스 붕괴로 바꾸지 않는다.

- [AF-RES-015 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 이유 유형별 노후화; §2 세부 질문별 답 / Q2 현재 유효성; §2 세부 질문별 답 / Q3 답 시점 복원; §3 추가 분석; 행: L16, L63–67, L93–95](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) — SHA `e39d23c9a7307ba83c974580f60115d90e221084`.
- [AF-RES-015 · REASONS.jsonl · then/current 판정 및 초기오류·후발변화 행; OpenZFS·Almond](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/REASONS.jsonl) — SHA `e39d23c9a7307ba83c974580f60115d90e221084`.
- [AF-RES-009 · GAP.md · 원 절: 5. 남은 가설과 반증 가능한 다음 연구 / H2. 제공자가 바뀌어도 이어지는 근거의 재검토; 행: L117–119](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md) — SHA `7f627a81199f06da7f7b15f979e7fef25dd17602`.

방법 대응(조립 가설 H): X10, X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF11 — REVIEW-4 §3 #11, L189

주성격을 경험적으로 둔 근거는012의 동일15질의·고정 검색 순위·문서 관련성이라는 평가 목적 아래 판정자에 따라 방식 순서가 실제 바뀌었다는 점이다. 다만012도 일부 근거 열람·조건 해석 범위가 달라 엄밀히 동일 조건의 수치 오류라고 부르지 않는다. 014의 실제 답 grade는 관측된 추천·사용 신호를, 내부 must 판정은 문서상 조건 충족을 묻는 성분이 있으므로 두 qrel의 차이에는 정의상·범위 차이가 있다. 이를012와 합쳐 한 종류의 경험적 불일치율로 계산하지 않는다. 013의 역사 적중과 조건부 참고도 다른 평가 질문이다. 전체0 일치에 가려진 양성 불일치를 함께 보존한다.

- [AF-RES-012 · RESULTS.md · 원 절: Q8. 판정과 자료집이 바뀌면 결론도 바뀌는가; 행: L137–145](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md) — SHA `cb602858378db90adb1f085953016267f9afbd6d`.
- [AF-RES-014 · RESULT.md · 원 절: §1 필수 결과 표 / 표 3 — 판정 출처 민감도; §2 세부 질문별 답 / Q7 실제 답과 판정 편향; 행: L34–41, L107–109](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) — SHA `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`.
- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표의 단위와 판정 책임; §2 세부 질문별 답 / Q7. 채점: 적중·부분 참고·미해결 조건·링크를 분리했다; §2 세부 질문별 답 / Q8. AF009의 반대 가설 A/B는 이번 결과만으로 기각되지 않는다; 행: L65–69, L134–146](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.

방법 대응(조립 가설 H): X08, X12, X22. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF12 — 추가: AF-RES-020 원 결과 재대조

같은 정의·패킷을 읽고 서로 다른 값을 실제로 부여했으므로 단순 용어 대응표로 해소되지 않는 경험적 재현성 차이다. 원 단위ID로 직접 조인해 A0/B14를 다시 셌다.

- [AF-RES-016 · RESULT.md · 원 절: §1 필수 결과 표 / 표 1 — 분류안별 일치도; §2 세부 질문별 답 / Q7. 불일치가 실제 판정을 바꾸는가; §4 가장 중요한 불일치·약점 3건과 다음 조사 제안 / 1. S2의 낮은 점수에는 코드북 적용 비대칭과 과제 차이가 섞여 있다; 행: L12, L170, L216–224](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · CODEBOOK.md · 원 절: 3. S2 문제 상대형 — 선택 범위에 대한 기여; 4. S3 두 축 — form × contribution; 행: L25–36, L39–41](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/CODEBOOK.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · units.json · units[*].unit_id/sample; 011 표본120개](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/sample/units.json) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · coder-a.json · rows[*].S2; T036-005 L532 이후](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/coding/coder-a.json) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · coder-b.json · rows[*].S2; T036-005 L528 이후](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/coding/coder-b.json) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X08, X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF13 — 추가: AF-RES-020 원 결과 재대조

숫자 오류가 아니라 proposed_use를 role로 바꾼 정의 축 생략이다. 공통 해석은 PROTOCOL로 정했으나 원 파일은 이 작업의 수정 범위 밖이므로 부분 해소로 남긴다.

- [AF-RES-004 · HANDOFF.md · 원 절: 5. 판단과 근거; 행: L80](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/HANDOFF.md) — SHA `2b798c7d2b7355b649691c18de196104ceabb0f0`.
- [AF-RES-004 · PROTOCOL.md · 원 절: 판정 단위와 증거 경계; 행: L22–26](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md) — SHA `2b798c7d2b7355b649691c18de196104ceabb0f0`.
- [AF-RES-016 · RESULT.md · 원 절: §3 추가 분석 / 3.1 세 안의 적합 조건과 실패 조건; §3 추가 분석 / 3.4 판정 상태를 보존하는 조립 원칙(H); 행: L192, L210–212](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X04, X08, X10. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF14 — 추가: AF-RES-020 원 결과 재대조

같은 숫자146이 같은 집합을 보장하지 않는 정의 차이다. 직접 원JSON에서146/146/142 및4+4를 재계산했으며 7과8을 재현 실패로 만들지 않았다. 실제 오분류의 정정 이력도 있다: 013 RESULT L101과 cases/CASES.json coding_revisions[0]에서 C05는 외부 참고문헌 없음과 구조 전이 없음의 혼동을 바로잡았다. 이 과거 정정을 현재 고정판의 수치 불일치로 다시 세지 않는다.

- [AF-RES-013 · RESULT.md · 원 절: §1 필수 결과 표 / 표 2 — 역할별 집계; §2 세부 질문별 답 / Q3. 정답 항목은 외부 실체보다 내부 설계 대안에 치우쳤다; §3 추가 분석 / 3.1 계열·정답 종류·시간·노출을 나눈 관측; 행: L43–50, L97–101, L161–166](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-013 · CASES.json · gold_items[*].role/match_kind; 차집합 L601,1527,1792,1808,1827,2743,4929,4945](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/cases/CASES.json) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-013 · AGGREGATES.json · roles L938 이후(같은 분야의 다른 설계 A.strict_historical=7); gold_types L2122 이후(structural_design A.strict_historical=8)](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/evidence/AGGREGATES.json) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.

방법 대응(조립 가설 H): X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF15 — 추가: AF-RES-020 원 결과 재대조

작업 진행 상태·원 인계의 조건 충족 상태·연구 내용의 채택은 별개다. DONE을 허위 완료라고 자동 단정하지 않고 인수 이유를 남길 별도 기록을 요청한다. 원016이 표준 REVIEW_READY_WITH_GAPS 문구를 실제 썼다고 꾸미지 않는다.

- [workspace-foundation · dot-control.json · AF-RES-013 L264–282; AF-RES-016 L337–355](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/automation/dot-control.json) — SHA `7b4334e55a0563225295618eaf3ad299b415d9f7`.
- [workspace-foundation · DOT_AUTOMATION.md · 원 절: 한 작업을 연결하는 순서; 행: L59–64](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/DOT_AUTOMATION.md) — SHA `7b4334e55a0563225295618eaf3ad299b415d9f7`.
- [AF-RES-013 · HANDOFF.md · 원 절: 서두(제목 아래); 1. 인계 상태와 차단 이유; 행: L6, L12](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/HANDOFF.md) — SHA `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- [AF-RES-016 · HANDOFF.md · 원 절: 0. 인계 상태; 행: L3–12](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/HANDOFF.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · RESULT.md · 원 절: §5 한계; 행: L252](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X10, X12. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

### CF16 — 추가: AF-RES-020 원 결과 재대조

‘가볍게 시작 가능’은 정보 보존 조건이 다른 구성 간의 범위 차이다. 파괴적 압축이 없으면 단일 메모도 가능하므로 가벼운 저장 자체와 충돌한다고 일반화하지 않는다.

- [AF-RES-001 · RESEARCH.md · 원 절: 9. 독립 검토가 바꾼 판단; 행: L147–152](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/RESEARCH.md) — SHA `4d6208c08f6f2657865ba000d6768f6537e832b6`.
- [AF-RES-003 · RESEARCH.md · 원 절: 5. 무엇을 더 저장할지: 필드보다 막아야 할 실패 / 원문을 보존하지 않는 최소안의 정확한 한계; 7. 병합·분리·대체에서 보존할 연결; 행: L107–111, L146–159](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md) — SHA `b13db3931b4021ff9e1ac6e404590c09526c3087`.
- [AF-RES-004 · PROTOCOL.md · 원 절: 판정 단위와 증거 경계; 행: L24](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md) — SHA `2b798c7d2b7355b649691c18de196104ceabb0f0`.
- [AF-RES-016 · RESULT.md · 원 절: §3 추가 분석 / 3.1 세 안의 적합 조건과 실패 조건; §3 추가 분석 / 3.4 판정 상태를 보존하는 조립 원칙(H); 행: L192, L210–212](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.
- [AF-RES-016 · CODEBOOK.md · 원 절: 4. S3 두 축 — form × contribution; 행: L39–41](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/CODEBOOK.md) — SHA `3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc`.

방법 대응(조립 가설 H): X04, X10, X22. 원 사실의 증거를 추가한 것이 아니라, 질문·대안·기준·상태·추가 확인을 분리하는 기록 방식으로 사용한다.

## 4. 방법 문헌과 조립에서의 사용

방법 출처는 `sources.json`의 X04·X08·X10·X12·X22 및 `CROSSFIELD.md`를 함께 읽는다. 이 등록부는 해당 문헌의 효용을 새로 실험한 결과가 아니다.

| 방법 출처 | 이 등록부에 적용한 원리 | 적용의 한계 |
| --- | --- | --- |
| X04 Parnas | 바꿀 수 있는 결정을 분리하되 숨기면 안 되는 의미 계약은 의존으로 남김 | 연구의 근거·정의를 감추라는 뜻이 아님 |
| X08 QOC | 충돌을 질문·대안·기준으로 전개하고 기준 찬성 수로 자동 선택하지 않음 | 같은 단어의 다른 기준을 하나의 경험적 효과로 합치지 않음 |
| X10 ADR | 원 판정·상태·정정 이유를 보존하고 대체 기록으로 연결 | ADR 채택 상태는 연구 근거 확실성·진행 DONE과 다름 |
| X12 GRADE EtD | 근거와 기준별 판단·선택을 분리하고 관점·자원·실행 가능성을 함께 기록 | D0–D4를 GRADE 등급으로 치환하지 않음 |
| X22 NASA 의사결정 분석 | 다음 증거가 선택을 바꿀 가능성과 수집 비용을 비교하며 가까운 대안을 함께 유지 | 이번 최소 표본은 정밀한 정보 가치·검정력 계산이 아님 |

## 5. 재대조와 반례 기록

- 계획 원11행은 L179–189에서 직접 읽었고 CF01–CF11과 일대일 대응한다. 계획의 ‘부분10/33 진전’을 통합 성공으로, ‘다른 분야 인용0’을 가치0으로 옮기지 않았다.
- 013 원 `cases/CASES.json`의176gold를 role×match_kind로 직접 조인했다. 두146의 교집합142와 차집합4+4, 해당 원ID 위치8개를 확인했다. 숫자7/146·8/146은 원 표에서 각기 다른 축이다.
- 016 원 coder-a/b를 원 sample/units의ID로 조인해 같은011표본120에서 comparison A0/B14를 직접 재계산했다. S3의 contribution 복사는 코드북에 명시돼 독립 반복으로 세지 않는다.
- 015 결과의 후발5행에 동일 Almond 사건2행과 OpenZFS 제약 해소1행이 있음을 원문에서 확인했다. 초기오류4개를 후발 분자에 더하지 않았고 연간 사건률도 만들지 않았다.
- 014 GGL은 답 기반 등급과 제약 충족의 차이이고 Word는 의도적 오독 반례다. 둘 다 실제 관련성 등급이 제거되었지만 해소할 원인은 다르다.
- 004의 HANDOFF→PROTOCOL 사용 단위 누락은 실제 원 전달 불일치다. 나쁜 문장을 새로 만들어 원 결과 오류 수를 채우지 않았다.

모든16행의 필수 필드·허용 성격/상태·고정 SHA 참조 경로를 확인했고 오류0건이었다. 현재 분류는 정의상6·범위 차이8·경험적2, 상태는 해소2·부분 해소8·미해소6이다. 경로·구조 검사는 내용의 진위를 자동 판정한 것이 아니다.

## 6. 한계

이 표는 조립을 위한 충돌 지도이며 새로운 제품 성능 비교가 아니다. 고정 원 결과와 하위 기록을 대조했고 이전 외부 원 스레드·논문 전체를 재조사하지 않았다. 같은 모델 계열의 내부 별도 검토(GPT-6 Astra Pro)다. 경험적 충돌의 판정자 독립성·근거 범위·표본 편향은 해소되지 않았다. 같은 숫자가 반복돼도 같은 집합인지 확인해야 하며, 단위를 맞춘 것만으로 남은 대안 중 하나를 최종 선택하지 않는다.
