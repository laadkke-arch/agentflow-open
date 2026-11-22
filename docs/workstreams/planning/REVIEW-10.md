# PLAN 10 · 설계자가 링크 하나를 믿고 무엇을 결정할 수 있는가

이 탐색기의 목적은 만들고 있는 소프트웨어의 전체 또는 일부와 그 용도를 받아, 쓸 만한 완성품·부품·다른 분야의 원리를 원문 링크로 알려주는 것이다. 줄이고 싶은 비용은 나중에 더 나은 해법을 알아 설계를 다시 하는 노동이다. 지금 가장 분명한 관측은 **필요한 근거를 보여 주거나 가릴 수 있다**는 점이다. 새 조사에서 프로젝트별로 링크를 묶자 두 요구의 부분 근거가 사라졌다. 옛 발췌를 저장해 두면 과거 문구를 다시 읽을 수 있었지만 현재 용도의 판정이 나아진 사례는 확인되지 않았다. 설계자의 실제 재작업 절감량은 여전히 미확인이다. [제품 브리프][product] · [040 손실 원장][40loss] · [039 짝별 실측][39pair] · [038 사람 측정 범위][38measure]

**H1**은 요구·용도와 원문 근거를 연결하면 더 나은 후보 판단을 돕는다는 가설이다. **H2**는 저장한 추천 이유를 나중에 다시 확인하면 오래된 오판을 줄일 수 있다는 가설이다. 새로 검색하기(C0), 링크·판·문맥을 조건부로 보관하고 재방문하기(C1), 주장·근거·판정 이력까지 보관하기(C2)는 서로 조합할 수 있다. 어떤 용도에서 추가 정보가 제값을 하는지가 선택 기준이다. 입력 계약, 검색기, DB, 크롤링 주기는 미결정이다. [REVIEW-9][r9] · [연구 운영 규칙][workflow]

## 검토한 범위

2026-11-22 UTC에 계획 브랜치 `0667c32`의 최신 파일 REVIEW-9를 먼저 읽었다. 당시 **DONE 32·BLOCKED 2**에서 통합 브랜치 `785880f`의 **등록 38·DONE 36·BLOCKED 2**로 바뀌었다. 추가된 DONE은 037~040이다. 네 작업 모두 원격 브랜치 끝과 진행표의 `result_commit`이 일치했다. 아래 첫 SHA는 인계가 포함된 브랜치 끝, 둘째 SHA는 인계서가 고정한 결과 본문이다. 이전 32건의 판단은 REVIEW-9에서 이어받았다. 이번 네 건은 각자의 경로에서 인계·결과·자체 점검·수용 파일과 세부 원장을 읽었다. 아래의 재집계는 저장된 원관측에 관한 것이며 당시 외부 열람과 프로그램 실행의 증거는 작업자의 영수증이다. [이전 검토][r9] · [고정 진행표][control]

| 새 DONE | 인계 SHA / 본문 SHA | 작업자가 직접 읽은 고유 외부 원문 | 이번에 대조한 단위 | 수용 조건 |
| --- | --- | ---: | --- | --- |
| 037 · 분야 간 원리의 설계 변경 | [68c45d2][37h] / [c92ad2c][37r] | 49 | 12사건, 판정 25행 중 원안 기준 12행·회고 허용 12행·기준 변경 1행 | 19/24. 결말 노출, 초기 수신 원문·제공 원전 공백, 두 종류 반례의 미확정. [수용 원장][37a] |
| 038 · 링크 제공과 설명을 비교할 과제 | [5a1699b][38h] / [964ecdc][38r] | 33 | 4과제×5파일, 작성 예시 12개·요구 36셀 | 내용 23/24. N08의 절대 최초 공개판 미확인. 마지막 인계 커밋은 선행 수용 파일의 절차 항목 A27을 따로 입증한다. [수용 원장][38a] |
| 039 · 같은 참조의 실제 재조회 | [cf3e62e][39h] / [7e7773c][39r] | 33 | 12참조×2보관 구성×2과업, 48실행·24짝 | 15/18. 현재 기준 4/12, R01의 옛 목적지 접근과 소비자 HTML 원판 4건 미확인. [수용 원장][39a] |
| 040 · 중복 제거와 근거 손실 | [9bff557][40h] / [b99b5e2][40r] | 64 | 8요구·후보 48슬롯·24보기, 손실 원장 72행 중 기본 조건 24행 | 필수 23/26. 자연 href 순서, 두 분야의 방향 판정 범위, 실제 설명 길이 통제가 미충족. [수용 원장][40a] |

원문 수는 각 작업 내부에서 같은 저작의 중복을 제거한 수다. 네 수를 합쳐 연구 전체의 고유 원문 수로 쓸 수 없다. 중앙의 DONE 36건은 모두 `acceptance_evidence`가 비어 있고 신규 네 건의 `source_commit`·`actual_model`도 비어 있다. 완료 표시는 인계 등록을 뜻한다. 근거 수준은 위 원장에 남은 실제 충족 항목을 따른다. 018은 세 번째 시도에서 대화 길이 한도, 035는 첫 시도에서 사이버 보안 위험 가능성 표시로 종료되어 두 건 모두 공식 인계와 결과 SHA가 없다. 035에 배정됐던 Go 값 추출과 외부 배열 소비자 전달의 검증도 미확인이다. [진행표][control]

## REVIEW-9까지 쌓인 근거

| 작업·판단 대상 | 분모가 있는 관측 | 다음 설계에서 지켜야 할 경계 |
| --- | --- | --- |
| DOT-001·002, RES-001~004·020 · 입력과 후보 단위 | 작업 인계·복원 경로를 확인했다. 합성 입력 6건의 분해에서 부정이 빠졌고 2문제·17질의에서 동명 도구와 부품이 섞였다. 003은 주소·대상·목적상 대체를 구분했고 004는 합성 18행을 판독했다. 020은 73개 주장 중 72개의 전달을 확인했다. | 문제·후보·제안 용도·설정·근거를 함께 보아야 한다. 020의 충돌 16개 중 완전 해소 2, 부분 8, 미해소 6이다. |
| 009~014 · 탐색과 부분 질문 | 비교 시스템 35개와 기능이 겹쳤다. 분야 힌트를 준 010은 24개 본문에서 원리 7군을 찾았다. 011의 실제 61스레드·635답에서 부분 질문 33개 중 10개가 진전했다. 013은 설계 문서 31개의 역사적 선례 176개 중 웹 검색 16개, 목록 5개를 회수했다. 정답 밖 178후보 중 문서상 유용한 170개 가운데 146개는 같은 분야였다. | 011의 전이 답 14개에는 질문자 반응이 없었다. 012의 합성 질의에서 본문 안의 한계 문구가 늘린 근접 오답은 014의 485자료에서 재현되지 않았다. 별도 필터의 오답은 610슬롯에서 5→3이었으나 새 후보 329개 중 한계 근거 보강은 15개였다. |
| 015~017·019·022 · 추천의 붕괴와 늦은 발견 | 015의 500추천 중 현재 판정 가능 195개에서 붕괴 14개, 과거 복원 83개에서 후발 붕괴 5·최초 오류 4였다. 016의 내부 일치는 후보 형태 78.3%, 기여 70.8%였다. 017의 늦은 발견 40건 중 두 날짜를 연결할 수 있던 사례는 18건이었다. 022는 결정 우선 24건 중 이미 알던 해법의 조건 정정 뒤 시행 2건을 찾았다. | 017에서 당시 검색 가능성을 확인한 사건은 0건, 주 표본의 타 분야 주 관계는 0/40, 별도 기원 추적은 7경로였다. 022의 미인지·당시 가용·결정 변경·시행은 주 표본 0/24와 발견 진술 우선 보조군 1/9다. 33건 모두 절감 노동 미확인이다. 019에서는 사건과 대조 7쌍에 각각 경보 3건, 알려진 공지 URL의 직접 확인 35/35와 신호 뒤 확인 13/35였다. |
| 021·023 · 요구와 근거를 연결하는 가치 | 같은 후보와 두 절 열람에서 주소만/근거 절 목록/요구와 절 연결의 인용 완결은 6/23·9/23·13/23이었다. 카탈로그 사건 18건에서 목적지를 고른 수는 주소와 이유 3, 식별자·판·근거 추가 5, 변경 관계·시점 추가 15였다. | 잘못된 연결이면 021은 8/23으로 내려갔다. 023의 풍부한 보기에 사후 정정이 들어갔으며 실제 자동 복원은 0/18이었다. |
| 024·028 · 링크가 살아 있어도 추천 이유가 무효가 되는가 | 64이유×16분기의 1,024셀은 유지 897·무효 95·최초 오류 16·보류 16이었다. 분기당 20회 방문에서 정기 직접 확인은 무효 이유 11/11, 신호 뒤 확인은 8/11을 찾았다. 10회에서는 7/11·0/11, 40회에서는 모두 11/11이었다. | 20회 조건의 신호 방식은 본문을 108개 덜 읽고 약 5.67 MB를 더 받았다. 028이 고정 Linux 용도를 실행한 유지층은 26이유의 32셀이다. 남은 유지 865셀의 동작은 미확인이다. |
| 025·029·031 · 검색에 나온 링크와 실제 소비 동작 | 025의 72슬롯은 지지 2·충돌 14·보류 53·빈칸 3이었다. 029의 새 설계 12건에서 부분 요구 인용 완결은 공통 검색 2, 추가 웹 검색 4, 제공자 내부 탐색 3이었다. 031은 이미 알려진 추천 3개를 36개 계약 입력으로 재생했다. | 029의 추가 성공은 원래 언급된 후보에서 나왔고 전체 요구 완결은 세 경로 모두 0/12였다. 031의 양성 11·대조 21·경계 4는 특정 Arrow·DataFusion·Jupyter 경로의 근거다. 기대를 정정한 행이 6개이며 대용량 종단 전달과 실제 프런트엔드 자동 전달은 미확인이다. |
| 026·030 · 되묻기가 선택을 바꾸는가 | 026은 24요청에 세 전략을 만들었고 실제 발송은 0회였다. 030은 최초 요청 표본 24건에서 같은 변수에 대한 직접 답 3건, 실제 질문을 보고 고른 보강 8건에서 직접 답 6건을 찾았다. | 같은 답변자의 기존 권고 변경과 요청자의 같은 목적 신규 실행까지 이어진 사례는 0/3·0/6이다. 사후에 알게 된 요청을 당시의 입력으로 쓰면 평가가 달라진다. |
| 027·032 · 공급자와 소비자의 변경 시점 | 027의 소비자 우선 12참조는 유지 5·실패 보고 2·보류 5였다. 032의 실제 HTML 12참조는 모두 HTTP 200이었다. 같은 목적의 href 수정 5건은 유지 4·교체 1, 그대로인 7건은 유지 5·교체 1·보류 1이었다. | 상류의 시행→소비자 배포를 엄격한 두 날짜로 확인한 사례는 0/12·0/6이었다. 풍부한 보기에는 현재 내용·판독자의 해석·이력이 함께 들어갔다. |
| 033·034·036 · 반환 근거, 사람의 노동, 과거 이력 | 033의 8설계×18후보에서 엄격 지지는 넓게 1/144였고 그 선택은 원안에 이미 있었다. 두 검색 방식 모두 실제 상위 3개 반환창에서 인용 완결 0/8이었다. 034의 사람 연구 22군·26실험에는 더 빨리 올바른 설명을 찾은 과제가 있다. 036에서는 현재 근거만 준 보기와 이력을 더한 보기 모두 유지 11·교체 1이었다. | 033의 당시판 엄격 지지는 0건이다. 034의 NCQ에서 선택 시간 중앙값은 380→57초, 총 과제 시간은 849→847초였다. 링크만 달리한 비교나 첫 채택 후 수정 노동을 대조한 연구군은 0이었다. 036의 옛 근거까지 복원하는 29→17 GET은 주소를 아는 상태에서 계산한 모의값이다. |

앞선 수치의 사건·근거 위치와 표본선정 조건은 이전 누적 검토에 연결돼 있다. 특히 검색기의 반환창, 사람 연구의 군별 종점, 과거 이력의 모의 비용은 측정 단위가 다르다. [REVIEW-9][r9] · [033 실제 반환창][33win] · [034 군별 효과][34effects] · [036 재조회 가정][36replay]

## 이번 네 건에서 확인한 것과 남은 공백

### 037 · 저자가 원리를 언급한 뒤 실제 선택이 바뀌었는가

결정부터 고른 CSSWG·GDAL 8건(A)과 인쇄·지도·음악 출처가 드러난 4건(B)을 분리했다. 판정 원장 25행을 사건과 기준선별로 다시 세면, **최초 설계안의 동일 선택에 대한 완결 인과는 A 0/8·B 0/4**다. 같은 목적의 후속 명세·코드·시험 정의는 A 7/8·B 3/4에서 확인됐다. 제안과 코드가 둘 다 존재해도 그 선택을 바꾼 외부 원전의 식별·당대 이용 가능성·저자의 연결·변경 전후가 한 사슬로 이어져야 한다. 당시 검색색인과 저자의 첫 노출은 12건 모두 미확인이다. [판정 25행][37j] · [시간순 원장][37chain]

B02에서 GDAL의 GMLJP2 축 순서가 바뀐 패치는 실재한다. 최초 RFC20이 이미 그 정책을 제안했으므로 ‘최초안이 바뀌었다’고 세면 기준선이 이동한다. 표준을 제공 분야에 넣고 **기존 코드→패치**를 묻는 감도에서만 B 1/4다. pdfTeX(B01) 저자는 hz의 영감과 알고리즘을 독자적으로 만든 일을 함께 기술했다. LilyPond(B03) 초기 소스는 기존 글꼴에 대한 불만·새 Feta 글꼴·출판사 악보를 연결한다. 핵심 hz 원전, 정확한 악보 판과 변경 전 글꼴은 미확인이다. B04는 원 발행본을 열지 못했고 A 한 사례는 선정 뒤 결의 스니펫이 노출됐다. 고유 원문 49개 중 제공 분야 규칙 10개를 모두 당대에 읽은 직접 원전으로 취급할 수 없다. 명시적 연결이 확인된 선행 저작은 2개다. 반환 카드의 제한적 선례 2·유사 오답 8·보류 2와 역사적 인과를 구별해야 한다. [본문과 반례][37r] · [출처 재집계][37count] · [카드 12개][37cards]

### 038 · 채점할 자료는 생겼지만 사람의 노동은 아직 측정하지 않았다

pandas·NumPy의 네 결정에서 각 과제의 최초 요구(t0), 자유 검색 A, 중립 링크 B, 같은 링크에 요구별 절·한계를 더한 C, 동일 요구 재검(t1)을 만들었다. B/C 원문 링크 11/11의 URL·판·순서가 같았다. 작성 예시 12행을 다시 대조하면 첫 별도 AI 문맥의 전체 판정은 12/12, 요구별 일치는 **35/36**이다. N08-E3의 R2는 기대 ‘부분’, 자체 판독 ‘실패’, 첫 가림 판독 ‘통과’였다. 키별 완성 출력까지 확인하도록 채점 기준을 명료화한 뒤 같은 판독자가 ‘실패’로 바꿨다. 최초 불일치는 그대로 남는다. [작성 예시][38ex] · [첫 판독과 사후 정정][38grade]

네 과제 중 최초 공개판을 엄격히 확인한 것은 3건이다. N08은 더 이른 동일 제안이 있었는지 열려 있다. P04에는 한 번 정한 날짜 형식을 끝까지 지켜 의도적으로 거부하는 정답이 있고, P06에는 dtype을 유지한 채 1.5를 1로 바꾸는 오답이 있다. 역사 버전 API를 실행한 것은 0/4이고 사람 참여는 0명이다. A/B의 차이에는 선정·제공 시점·제목·순서가, B/C의 차이에는 설명 내용과 늘어난 읽기 부담이 함께 들어 있다. 채점 준비도, 실제 API 출력, 사람의 수정 시간은 각각 검증을 필요로 한다. [과제와 루브릭][38r] · [미실행 드라이버와 환경][38exec] · [사람 측정 계획][38measure]

### 039 · 저장한 인용을 다시 보는 일과 발행 원문을 다시 찾는 일

C1은 주소·문맥·판·목적을, C2는 과거 근거와 출처까지 보관했다. 48실행·24짝을 두 과업별로 다시 세면, **현재 판단은 양쪽 모두 유지 1·보류 11**, 정확한 현재 발췌(N)와 과거 발췌(H)를 함께 복원한 수는 **C1 0/12·C2 1/12**다. C2가 보관 파일에서 H를 표시한 수는 12/12다. 완전 복원 한 건(G02)도 독립 발행처 H 두 조각 중 논리 예산에서 다시 연 것은 1개, 두 번째 문서 교환까지로 제한하면 0개였다. 같은 조회창에서 행동 기준을 확인한 참조는 4/12뿐이다. [실행 48행][39run] · [짝 24행][39pair] · [당시점 기준][39crit]

C1과 C2는 각각 논리 GET 47회, 발행 문서 HTTP 교환 7·8회, 클라이언트가 받은 본문 956,276·724,028바이트였다. 논리 GET 94회 중 실패 88회, 그중 80회는 HTTPS CONNECT 단계에서 거부됐다. 발행처까지 도달하지 못한 요청은 해당 서버의 문서 소멸을 입증하지 않는다. C2는 25,992바이트를 더 보관했다. 받은 내용과 완성한 과업이 다르고 성공쌍에서 저장 비용을 상쇄하는 회차당 이득을 입증하지 못했으므로 손익분기 횟수는 미확인이다. 036의 모의값은 경로를 찾는 비용과 이 접근 실패를 포함하지 않았다. [실측 영수증][39cost] · [두 예산·모의와 실측][39r] · [036 모의 단위][36replay]

### 040 · 같은 프로젝트라는 이유로 합쳤을 때 실제로 사라진 근거

두 원장의 요구 8건×6자리 중 링크가 있는 곳은 39곳이었다. 필수조건 25개 중 원래 풀에서 8개만 입증됐다. 원장 기본 조건(추가 클릭 0) 24행을 집계하면 **정확 URL(A) 8·상류 프로젝트(B) 6·부품/용도/판/근거 역할(C) 8**개가 남는다. B에서 G2는 MapInfo 읽기와 Java 호출의 보완 근거를, S1은 POT 생성과 위치 설정을 연결하는 근거를 각각 일부 잃었다. G4에서는 HDF5 원문 자체에 gdalinfo 예가 있어 대표 뒤로 다른 문서를 숨겨도 해당 근거가 남았다. B의 이질 병합은 쌍 단위로 48개였고, 필수조건 손실은 요구 단위로 2/8이었다. [원풀][40pool] · [24보기][40views] · [손실 원장][40loss]

완전 대안이 들어 있는 요구는 원래부터 0/8이었다. 모든 방식에서 완전 답변 0/8, 적격 대안의 조건부 회수는 **해당 없음**이다. 이름만 필요한 요청도 0건이었다. C가 A보다 완전 대안을 되살렸다고 말할 근거가 없다. Sphinx 후보 일부는 연구자가 만든 행 앵커였고, 실제 목차 순서가 사전 고정되지 않은 구간도 있었다. 두 분야에서 ‘대체 가능’의 판정 범위가 달랐다. 카드 설명은 80자 상한만 같았고 형제 확장은 모든 형제 원문까지 열 수 있다는 상한이었다. 두 클릭의 실제 도달 범위는 미측정이다. [기본·감도 재집계][40count] · [절차 정정][40method] · [결과와 예외][40r]

## 엇갈린 근거를 가를 다음 작업

| 앞선 관측 사이의 불일치 | 판정을 바꿀 근거 | 독립 작업 |
| --- | --- | --- |
| 010·017의 기원 사례와 037의 초기 저자 발언에는 전이 단서가 있지만 033의 반환창과 037의 최초안 기준에는 새 선택의 엄격한 양성이 없다. | 정확한 제공 원전과 저자가 바꾸기 전의 같은 선택을 연결하는 증언·반영. 빠진 고리를 특정하면 조건부 참고 카드도 남길 수 있다. | **041 · web-pro**. pdfTeX·Feta 두 사례의 원전 판과 변경 전후를 추적한다. |
| 021·034에서는 좁은 과제의 질이나 속도가 좋아진 경우가 있고 038의 예시 채점도 대체로 일치했다. 실제 동작·사람 노동에는 각각 별도의 근거가 필요하다. | P04의 정당한 오류, P06의 dtype 보존과 값 손실을 지정 릴리스에서 직접 관측해 틀린 정답표를 먼저 검출한다. | **042 · codex-cloud**. 두 pandas 판에서 원 드라이버와 반례를 실행하고 빈 환경에서 재생한다. |
| 023·032의 풍부한 자료에서는 목적지 판단이 늘었고, 036은 현재 내용을 같게 주자 이력 추가 변화 0/12, 039는 옛 발췌만 12/12 보였다. | 판 전용 주소와 인용 본문을 한 요소씩만 더하고, 현재 용도와 과거 문구의 발행판 확인을 각각 판독한다. | **043 · web-pro**. 자연 참조와 정정 우선 참조를 나눠 8건×4자료 구성에서 무엇이 충분한지 비교한다. |
| 003의 주소·대상·용도 구분에 관해 040은 상류별 합침의 부분 근거 손실을 보였으나 더 세밀한 구분의 완전 대안 이득은 판정할 분모가 없었다. | 원풀에 정답이 있었는지, 실제 세 자리·한 시행 두 클릭으로 무엇이 보이는지를 양성 대조와 자연 표본에서 따로 확인한다. | **044 · web-pro**. 실제 요구 8건·대조 4건에서 세 방식의 누락과 회복을 양방향으로 센다. |

041은 과거 결정의 인과, 042는 기존 과제의 API 동작, 043은 보관물의 증거 가치, 044는 반환 화면이 보존하는 대안을 다룬다. 네 지시문은 완료된 입력의 SHA, 직접 읽을 원문과 기록 형식, 필수 결과표, 중간 커밋, 반증·종료 조건을 각각 포함한다. 같은 차수의 산출물을 기다릴 작업은 없다. [다음 작업 네 건](NEXT_TASKS-10.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/785880f7b7c380dd49e0e4e6e6d90715a9b27838/docs/product/RESEARCH_BRIEF.md
[40loss]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/losses.csv
[39pair]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/pairs.csv
[38measure]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/measurement.md
[r9]: https://github.com/laadkke-arch/agentflow-open/blob/0667c32e7de4522275ad014d201f03638c771f05/docs/workstreams/planning/REVIEW-9.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/785880f7b7c380dd49e0e4e6e6d90715a9b27838/docs/RESEARCH_WORKFLOW.md
[control]: https://github.com/laadkke-arch/agentflow-open/blob/785880f7b7c380dd49e0e4e6e6d90715a9b27838/docs/automation/dot-control.json
[37h]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/HANDOFF.md
[37r]: https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/RESULT.md
[37a]: https://github.com/laadkke-arch/agentflow-open/blob/c92ad2c0c7dfc36e4614c62560a65621f8f0fd5b/docs/workstreams/research/AF-RES-037/evidence/acceptance-evidence.json
[38h]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/HANDOFF.md
[38r]: https://github.com/laadkke-arch/agentflow-open/blob/964ecdc0da2be2e8a864194c99741cabbe30e8e0/docs/workstreams/research/AF-RES-038/RESULT.md
[38a]: https://github.com/laadkke-arch/agentflow-open/blob/964ecdc0da2be2e8a864194c99741cabbe30e8e0/docs/workstreams/research/AF-RES-038/evidence/acceptance-evidence.json
[39h]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/HANDOFF.md
[39r]: https://github.com/laadkke-arch/agentflow-open/blob/7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8/docs/workstreams/research/AF-RES-039/RESULT.md
[39a]: https://github.com/laadkke-arch/agentflow-open/blob/7e7773cdec4c2213d2e81e0094fa5b6e742ec0e8/docs/workstreams/research/AF-RES-039/evidence/acceptance-evidence.json
[40h]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/HANDOFF.md
[40r]: https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/RESULT.md
[40a]: https://github.com/laadkke-arch/agentflow-open/blob/b99b5e2743e9cf0131a11d409707531f15a92f13/docs/workstreams/research/AF-RES-040/evidence/acceptance-evidence.json
[33win]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/returned-window-audit.jsonl
[34effects]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/effects.csv
[36replay]: https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/evidence/replay-summary.json
[37j]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/judgments.csv
[37chain]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/chains.csv
[37count]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/evidence/recount.json
[37cards]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/cards.md
[38ex]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/examples.jsonl
[38grade]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/evidence/grading-comparison.json
[38exec]: https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/streams/pandas/execution-next.md
[39run]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/runs.csv
[39crit]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/evidence/current-criteria.jsonl
[39cost]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/evidence/receipts.json
[40pool]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/pool.csv
[40views]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/views.jsonl
[40count]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/evidence/recount-summary.json
[40method]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/evidence/method-clarifications.md
