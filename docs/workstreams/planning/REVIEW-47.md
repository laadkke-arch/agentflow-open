# REVIEW-47 · 새 링크가 알려 주는 것과 실제로 바뀐 것

개발자가 일부 기능과 목적만 설명해도 적절한 부품·서비스·다른 분야의 원리와 읽을 절을 돌려주는 것이 제품 목표다. 이번 결과에서 DuckDB의 원질문이 검색 1위로 올라온 일은 새 해법 발견으로 이어지지 않았다. pandas에서는 리뷰 뒤 같은 작성자가 실제 시험 코드를 바꿨지만 리뷰어가 건넨 외부 링크는 없었다. 반면 FreshRSS에서는 입력에 없던 읽음 값이 수신 설정에 따라 실제 DB에서 0 또는 1이 되는 단계까지 확인했다. 추천 문구의 동사는 이런 마지막 관측에 맞춰야 한다. [제품 브리프][product] · [검색 쌍][220pairs] · [리뷰 사건][225timeline] · [수신 DB][228obs]

**요청 당시 새 중앙 DONE은 219~226 여덟 건이고, 여덟 인계 모두 자체 PARTIAL이다.** 작성 중 중앙 DONE이 된 227~229도 각 소유 경로에서 따로 검토했다. 최종 신규 검토는 **11건**이며 자체 판정은 PARTIAL 8, REVIEW_READY 1, DONE 2다. 후속 제안 13건 가운데 웹 조사·설계 8건과 Codex 실행 4건은 요청 당시 근거만으로 시작할 수 있다. 별도 웹 판독 1건은 새 작업 238이 기관 원행과 가린 카드·정답표를 제출해야 시작한다. [요청 시 진행표][req] · [최종 진행표][end] · [작업자용 전체 지시문](NEXT_TASKS-47.json)

## 검토 범위와 시점

계획 브랜치 `cd60e68`에서 가장 최근인 REVIEW-46을 먼저 읽었다. 그 문서가 216~218의 결과까지 반영한 기준점은 `2a32cb8`이다. 이 판과 요청판의 전체 작업을 ID 및 행의 모든 필드로 대조했다. 기존 216행의 변경·삭제는 없었고 219~229 열한 행이 추가됐다. 이전 작업의 결과는 46차의 누적 판단을 이어 썼다. 요청 시점 RUNNING 세 건의 주제·판별 목표는 **중앙 배정문**에서 읽고, 완료로 기록된 뒤에 인계와 결과를 열었다. [직전 누적 검토][prev] · [직전 마감][old] · [요청 시 진행표][req] · [연구·인계 규칙][workflow]

| 통합판·UTC | 행 | 중앙 DONE | RUNNING | BLOCKED | 결과 검토 경계 |
| --- | ---: | ---: | ---: | ---: | --- |
| 46차 결과 마감 · 22:00:55 · 2a32cb8 | 216 | 212 | 0 | 4 | 218까지 결과 반영 |
| 47차 요청 · 22:30:41 · 914dbfa | 227 | 220 | 3 | 4 | 219~226 신규, 227~229 Codex 진행 중·결과 SHA 없음 |
| 작성 중 · 22:40:34 · de683d7 | 227 | 222 | 1 | 4 | 228·229 추가 확인, 227 진행 중 |
| 47차 결과 마감 · 22:47:37 · 3057e4e | 227 | 223 | 0 | 4 | 227 인계까지 반영. 다음 차수의 비교 기준 |

네 시각은 모두 2026-11-24 UTC의 Git 커밋 시각이다. 최종 223개 DONE에는 연구 221건과 연결 시험 2건이 들어 있다. 중앙 DONE 223행의 `acceptance_evidence`는 모두 빈 배열이다. 개별 산출물의 근거·자체 판정·독립 검토 여부는 아래와 같다. 유지된 BLOCKED는 018(인계 전 대화 한도), 035(실행 세션 종료·인계 미확인), 149(세 유입 경로의 동일 주간 분모 미확보), 151(최초 N0 응답·독립 가림·원사용자 비용 미확인)이다. [이전 진행표][old] · [중간 진행표][mid] · [최종 진행표][end]

| AF-RES · 대상 | 자체 판정 | 배정 브랜치의 인계 / 그 직전 결과 SHA | 원장 행 / 산입 고유 저작 | 실제 판단 단위 |
| --- | --- | --- | ---: | --- |
| 219 · 알림 설정 | PARTIAL | [a2fdcb7][h219] / [b6ee9d2][r219] | 49 / 35 | 지명 4자리 중 직접 중단 문제 1, 별도 합성 3 |
| 220 · 검색 첫 답 | PARTIAL | [5df1c48][h220] / [7364e52][r220] | 42 / 39 | 원요구 4쌍, 요청 8개, 예정 위치 40 |
| 221 · 등고선 연결 | PARTIAL | [78a561e][h221] / [eefc1be][r221] | 33 / 24 | 실재 입력 2·통제 5, 단계 표 28행 |
| 222 · 정정 이름 | PARTIAL | [fe41449][h222] / [e6ed02b][r222] | 55 / 25 | 산입 32기록·25저작, 고정판 18행·소비자 방향 36자리 |
| 223 · Change 링크 | PARTIAL | [27518e8][h223] / [c3895c3][r223] | 174 / 76 | 후보 경로 197, 엄격 앵커 12자리 중 8개 소스 연결 |
| 224 · 카운티 결합률 | PARTIAL | [c9897ac][h224] / [0cfc6fc][r224] | 37 / 22 | 목표 원행 4·48셀, 오류 4×보관안 3 |
| 225 · 리뷰 제안 채택 | PARTIAL | [d1d8595][h225] / [d00f774][r225] | 151 / 44 | 본 모집에서 1사건, 별도 보강 2사건 |
| 226 · 검수 노동 | PARTIAL | [d166817][h226] / [8b9445c][r226] | 44 / 27 | 번역 6세션·12분절, 별도 산업 역할 집계 4셀 |
| 227 · diff | REVIEW_READY | [075c66a][h227] / [70b89c4][r227] | 55 / 29 | 원형 입력 8×방법 4×반복 2, 별도 표시·진단 |
| 228 · RSS 이관 | DONE | [a2e9d82][h228] / [e0d151c][r228] | 52 / 48 | 원파일 2개, 수신 8회·항목 상태 20자리 |
| 229 · 철회판 선택 | DONE | [10a7d1c][h229] / [a10e044][r229] | 58 / 34 | pip 원형 16회·보조 2회, 별도 환경 재생 |

11건 모두 중앙 `result_commit`과 배정 브랜치 끝이 같았다. 모든 인계가 가리킨 결과 SHA는 바로 앞 부모였고 두 SHA의 RESULT blob이 일치했다. 요청 때 완료된 여덟 건은 고정 인계·결과·자체점검 외에 원장 585행을 파싱하고, 작업별 source_id 고유성과 최상위 CSV 29개·자료행 632개의 열 수를 확인했다. 작업별 산입 고유 저작 합은 292건이다. 같은 출전·사건의 반복을 포함할 수 있다. 220은 8개 원응답의 실제 항목 순서, 227은 내부 계측과 재생 요약, 228은 두 수신 설정의 원영수증, 229는 선택/거절의 실제 stderr까지 표와 대조했다. 각 실행은 해당 작업자의 고정 환경 관측이며, 이 검토가 새 독립 재실험이나 독자 평가를 한 것은 아니다. [220 원응답][220raw] · [227 계측][227diag] · [228 수신 설정 꺼짐][228off] · [켜짐][228on] · [229 경고][229warn] · [229 후보 부재][229absent]

## 지금까지의 제품 판단

| 설계자가 정할 문제 | 누적한 근거와 아직 남은 선택 |
| --- | --- |
| 전체 프로젝트 없이 무엇을 물을까 | 020은 전달 주장 72/73을 추적했지만 모든 충돌이 풀린 묶음은 2/16이었다. 107은 편집할 발생 위치에서 6/6, 공유 정의만으로 0/6이었고 159의 소비자 역할은 48/48을 갈랐다. 197의 현재 면/방문 면, 208의 원회차/이동 시각에 이어 219는 멈출 이벤트와 남길 채널을 갈랐다. 첫 원문 절이 달라지는 한 축만 되묻는 안을 보존한다. 실제 질문 전후의 효율은 미확인이다. [누적 근거][prev] · [219 분기][219routes] |
| 관련 원리와 다른 분야 선례를 얼마나 보여줄까 | 010의 힌트로 7군을 찾았으나 033의 무힌트 144쌍에서 당시판 지지는 0, 145의 독립 초안은 0/16이었다. 191·199는 색지각·인화 원전에서 다른 조작을 추적했다. 210에서 LIS 길이는 후보를 제한했고 227은 같은 길이에서 두 구현이 다른 줄을 보존한 사실을 확인했다. 221의 이진 연결·연속장·라이브러리 정책도 다른 질문이다. 설명, 독립 추가 적중, 사람의 선호는 각각 측정한다. [누적 근거][prev] · [221 입력][221inputs] · [227 앵커][227anchors] |
| 원어를 어떻게 검색어로 바꿀까 | 209의 JPEG 사례는 단서 추가로 도구 순위가 개선 0·악화 1·동률 1·판정불가 2쌍이었고 제공자 순위는 없었다. 220은 제공자 순서를 복원하고 원질문 제외·실제 조작 충족으로 다시 매겼다. 지금은 원 표현과 해석을 함께 보관하고 원사건 재방문과 새 대안 도착에 다른 점수를 줄 근거가 있다. AI 전처리·항상 두 질의의 실익은 열려 있다. [46차의 209][prev] · [220 질의][220queries] · [220 판정][220pairs] |
| 하나의 링크, 택일, 필수 조합 중 무엇을 줄까 | 040의 완전 적격은 0/8, 044 고정 풀의 두 묶음 방식은 동률이었다. 114의 충돌 후보 138건은 118에서 명시 7·미확인 131로 갈렸다. 193 메일 큐와 사서함, 202 OCR 모델·모드, 204 엔진·운영자, 213 저널 별칭·부모·로캘은 서로 다른 역할이다. 222는 같은 코드의 검색명과 표시명을, 223은 링크가 여는 필드를 갈랐다. 목적과 마지막 조작을 기준으로 원문 절·대안·함께 필요한 자원을 제시한다. [누적 근거][prev] · [222 방향표][222cons] · [223 앵커][223anchors] |
| 저장을 어디까지 늘려야 재현 가능한가 | 055는 옛 답 4/4·다음 판 0/4, 147은 옛 답 112/112를 복원했다. 150은 동일성과 근거가 함께 맞은 수가 보관안별 7·9·15/16이었다. 196은 표시 문장이 세 안 모두 4/4, 사본 없이 원바이트까지 확인된 것은 C 4/4였다. 207은 같은 648,615ms가 다른 분절에서도 나와 단건 인용으로 틀린 교체를 허용했다. 224가 제시한 분모·지리 키의 추가 비용과 효용은 실제 네 원행·독립 판독 전까지 설계 가설이다. [누적 근거][prev] · [224 셀][224rows] · [224 통제][224controls] |
| 갱신과 재확인은 언제 할까 | 024의 무효화 11건을 주기 방식은 11, 신호 방식은 8건 찾았다. 후자는 열람 108회가 적고 전송량은 5,672,462바이트 많았다. 152는 새 자료 15건 중 신호/희소 공급원 14, 주기 방식 13이었다. 211의 당시 fragment는 0/6이었고 216은 현존 파일 88개의 철회 표시를 연결했다. 229에서 경고는 선택한 파일과 요청 범위에 달렸다. 현재 응답, 옛 링크의 당시 도착점, 현재 사용자에게 줄 경고의 기록을 구분한다. [누적 근거][prev] · [229 행렬][229matrix] |
| 누가 실제로 선택을 바꿨나 | 022의 미인지→선택 변경→실행은 0/24, 180의 자연 8건에는 정한 시간창 안 원제보자 후속 글이 없었다. 194·203의 대안 및 214의 제거 패치도 최초 발견 인과를 확정하지 못했다. 225는 본 모집 한 건에서 동일인의 직계 패치와 회신을 복구했다. 그 사람이 이미 알았거나 새 조건 때문에 바꾼 가능성은 남는다. 무회신은 무효, 병합은 링크 효과로 바꿔 세지 않는다. [누적 근거][prev] · [225 단계별 주장][225claims] |
| 재작업·사람 노동이 줄었나 | 034의 한 단계는 380→57초, 전체는 849→847초였다. 172에는 전원·동일 기능·시간·독립 검수를 모두 연결한 비교가 없었다. 195는 번역 배정 24/24를 복원해도 독립 검수 키·시간이 0/96이었다. 207은 두 총노동 주장을 보류했다. 226의 두 단계 시간 실례는 존재하지만 직접 작성/재사용 대조와 최종 인수는 빠졌다. 현재 인용 가능한 값은 역할별·자료별 측정에 한정한다. [누적 근거][prev] · [226 시간표][226labour] · [별도 짝 실례][226pair] |
| 실제로 검사한 마지막 동작은 무엇인가 | 176의 합격 표시 55개는 한 보고서의 재표시였다. 205는 Astropy의 메모리 원값 0→99, 218은 새 reader에서 update 8회만 99·readonly/copyonwrite 16회는 0임을 보였다. 217의 OCR은 지정 12조합 두 반복에서 초기화 성공 14회/실패 10회였고 정확도는 측정하지 않았다. 이번 227의 hunk, 228의 SQLite 값, 229의 선택 report·경고도 각각 그 조작까지만 추천 문장을 뒷받침한다. [46차까지의 실행][prev] · [227 재생][227replay] · [228 수신표][228obs] · [229 재생][229replay] |

이 판단은 최종 검색 엔진, 제품 DB, 상시 수집, AI 호출 횟수 또는 AgentFlow 입력 계약을 확정하지 않는다. 개발자에게 줄 기본 단위는 목적·해당 부품·왜 쓸 만한지·판별 절이며, 근거가 더 필요한 질문에서만 판·행 선택·상태 정보를 더하는 안을 비교할 수 있다. [제품이 열어 둔 설계 질문][product]

## 요청 시점에 새로 끝난 여덟 건

**219 · 알림 중단 요구를 실제로 한 사람은 지명 네 자리 중 한 명이었다.** Discourse #229919에서 관리자는 기본 mute를 걸었는데 일부 주제 메일이 왔다고 했다. 자기 글의 메일을 남기고 싶다는 조건은 후속 #8에 나왔다. 고정 v3.3.0 소스에서 주제 mute와 unwatch→tracking은 다르고, 관리자 기본을 소급 변경하는 경로는 이전 값 일치 여부를 보므로 같은 값을 명시한 사람의 의도까지 식별할 수 없다. 나머지는 사용 가이드 1, 라벨 개선 요청 1, 원문 미열람 1이었다. 최초 revision 0/4, 해당 수신자의 변경과 다음 알림이 모두 연결된 경우 0/1이다. 세 통제는 합성이고 답글 선노출로 질문의 사전 적중은 평가할 수 없다. [요구별 원행][219requests] · [첫 설정이 바뀌는 분기][219routes] · [인계][h219]

**220 · 검색 순위가 오른 것과 외부 첫 해법이 좋아진 것을 구분할 수 있게 됐다.** DuckDB 네 원요구의 A/B 8회는 같은 제공자의 실제 배열을 반환했다. 40자리 중 반환 항목 21, 정상적으로 비어 있는 자리 19였다. 자기 이슈가 원 1위인 요청은 5/8, 자기만 있는 응답은 4/8이다. #12856에서 단서 DOUBLE이 자기 이슈를 1위로 올렸지만 그 도착점은 정확 재현까지였다. 부분 관련성을 포함하면 자기 포함 개선 1·동률 3, 자기 제외 첫 답은 개선 0·동률 4, 구체 해법만 보아도 두 방식 모두 성공 0이었다. #11583의 자기 위치가 5→2여도 첫 링크는 여전히 날짜 변환 문제를 풀지 못했다. 실제 API 버전 헤더·최초 편집판·옛 실행 환경은 미확인이다. 현재 제한된 공개 색인의 네 쌍으로 전체 웹 검색을 평가할 수 없다. [원응답 8개 색인][220raw] · [40자리][220paths] · [쌍별 판정][220pairs]

**221 · 원전과 제품 설명이 서로 반대인 구체 입력이 있다.** C3의 모서리를 시계 방향으로 (8, −4, 1, −3)으로 놓으면 중앙 평균은 +0.5, 쌍선형 안장값은 −0.25다. ContourPy의 중앙 기준과 연속장 원리가 다른 변 쌍을 예측한다. C4의 정확한 교차도 강제로 두 선분을 이어야 하는 정책과 구분된다. 첫 논문 스캔의 분자 부호와 행렬식 유도·후속 논문이 어긋나므로 원판 정오 여부를 보류한다. 통제 5개와 실재 2개에서 각 4단계로 만든 28행 중, 실재 R1은 기대 동시 노출, R2는 상대 비교 시험이었다. 정답을 보지 않은 독립 정확도 분모와 같은 입력에서의 실행 관측은 모두 0이다. 239의 실제 꼭짓점이 필요한 이유다. [입력][221inputs] · [노출·예측][221pred] · [결과와 식의 한계][r221]

**222 · 검색에 쓰는 올바른 이름이 화면에 반환할 공식 이름과 같을 필요는 없다.** 네 correction은 코드 포인트를 유지하고 별도 공식 별칭을 가진다. 예컨대 FE18은 공식 철자의 BRAKCET과 correction BRACKET을 구분해야 한다. 6코드×3판 18행은 원자료 판독이다. 2소비자×3방향 36자리에는 N/A 2개가 포함되고 실행은 0이다. 13별칭에 대해 CPython은 수용할 것으로, ICU의 ALIAS choice는 correction 4개를 수용하고 나머지 9개를 거절할 것으로 고정 코드에서 추론했다. ICU 헤더의 U_INVALID_CHAR_FOUND와 구현의 U_ILLEGAL_CHAR_FOUND·0xFFFF도 불일치한다. 도서관 n79090096은 교육 문서의 역사 전사만 있고 Kate Davis 두 사람의 현행 기관 LCCN은 확보하지 못했다. 233은 레코드, 240은 바이너리 오류값을 각각 맡는다. [고정판 원행][222names] · [소비자 방향][222cons] · [교육 전사와 한계][r222]

**223 · 실제 서비스의 편집 경로를 찾았지만 아직 클릭해 본 자료는 없다.** 영국 Apply 6앵커, Register 2앵커를 템플릿→라우트→대상 필드까지 조건부 연결했다. Apply의 같은 ‘Change’가 추천인 유형 라디오와 이름 텍스트 입력으로 각각 이어진다. 보강 사례에서는 다른 계산 이름이 같은 전체 폼을 가리켰다. 모집 경로 197개는 이름으로 골라낸 목록이며 모두 열어 본 화면 수가 아니다. 정규 6화면 중 4개, 12앵커 중 8개이고 나머지 Register 4자리는 공석이다. 클릭·복귀를 동일 화면에서 기대한 시험은 2/8, 실제 DOM·AX·발화·사용자 선택 관측은 0이었다. 도서관의 서로 다른 서지 ID 두 개에서도 실제 소장·예약 동작은 0/2다. 이름과 목표 역할까지 안내할 수 있고 실제 포커스·복귀·발화는 별도다. [앵커 원표][223anchors] · [복귀 근거][223returns] · [모집 경로][223frame]

**224 · 계산식은 근거가 있고 목표 지역 수치는 비어 있다.** 2019–2023 ACS5 B23025에서 005E는 실업자, 003E는 민간 노동력, 001E는 16세 이상 전체다. 목표 두 지역을 합한 실업률은 분자 합/민간 노동력 합으로 계산해야 한다. 기관 핸드북에는 *다른 지역·판*의 1,196/13,734 실례가 있다. Alameda·Alpine·Harris·Loving은 웹 리더의 벌크 크기 제한 등으로 4원행·48셀 중 확보 0, 두 결합률·MOE도 0/2다. 실패 응답은 기관에 자료가 없다는 근거가 아니다. 합성 12자리에서 A는 네 오류를 보류, B는 분모·단순평균 둘을 거부, C는 지리 중복까지 넷을 거부하도록 수동 판독했다. 작성자가 만든 카드의 기대이며 실제 네 지역 값에서의 검출은 0/12다. 238에서 값·주석·불확실성을 회수하고 242에서 오승인과 정당한 보류를 별도 판독한다. [비어 있는 48셀][224rows] · [대상 합집합][224ratios] · [합성 통제][224controls]

**225 · 채택된 코드는 보였고 최초 발견을 입증한 링크는 없었다.** 시간 순서로 모집한 60개 PR 중 시험 파일 적격으로 읽은 대화 20건에서 해당 사건은 #57697 하나였다. 리뷰의 도우미 이름·코드 제안 뒤 같은 작성자의 직계 커밋과 긍정 회신, 병합본을 연결했다. 제안 전에는 원시 Excel 헤더 일부를, 이후에는 파싱한 전체 프레임을 검사하므로 두 시험의 보장 범위도 다르다. 보강 #57957에서는 전체 Series 비교 후 이름 검사 조건을 완화했다. #57974에서는 재작성된 이력과 선행 리뷰어의 오기로 직계 다음 패치를 확정할 수 없다. 본 1/1·보강 1/2에서 같은 작성자의 직계 수정이 보였지만 세 댓글의 외부 URL 제시는 0, 완전 발견 인과는 본 0/1·보강 0/2다. JOSS에서도 ‘고쳤다’는 회신 뒤 추가 정정이 필요했다. 인계는 이전 커밋에 연결 계정 메타데이터가 남고 현행 결과 파일에서는 일반 문장으로 치환됐다고 기록한다. 이 검토는 그 값을 전재하지 않았다. [작성자·시점][225timeline] · [검사 조건][225assert] · [주장 단계][225claims] · [인계의 기록 범위][h225]

**226 · 두 역할의 시간표가 있다고 해서 동일 품질의 총노동이 계산되지는 않는다.** DG21의 실제 .tgt 6세션에서 12분절과 위치를 찾았다. 세 조건은 모두 사후 편집이다. 이름이 같은 주석 파일 후보가 12개여도 같은 판의 주석 원행 결합은 0/12였고 생산 시간·독립 검수 시간·인수 키도 각 자리에서 미확인이었다. Terribile의 별도 산업 자료는 역할별 처리속도 4셀을 제공한다. 평균 PE 제작·검수 속도는 더 높았지만 직무별 수용품질과 두 사람의 시간 연결은 없다. 다른 Temizöz 파일럿에서는 순서가 바뀐 두 작업의 단계 합계 79.17분과 69.71분이 실제로 짝지어졌다. 직접 작성 대 PE 및 최종 인수 시간 비교로는 쓸 수 없다. 평균 WPH를 뒤집거나 다른 연구 사람의 시간을 보태 전체 절감률을 만들 근거가 없다. [분절 키][226joins] · [역할별 시간][226labour] · [단계 합계 실례][226pair]

## 요청 후 완료된 세 Codex 인계

| 작업 | 원영수증이 허용하는 결론 | 판정을 넘어서려면 필요한 근거 |
| --- | --- | --- |
| 227 · Git/Breezy | 8입력×4방법×2회=64/64 기본 실행, 동일 조건 재생 일치. C1에서 Git patience의 후퇴와 histogram의 직접 선택은 같은 stdout을 냈다. C2에서 Git은 B(2,1), Breezy는 A(1,2)를 보존해 편집 수·범위가 같아도 내용이 달랐다. R4의 중간 c(5,4)는 정리 뒤 c(5,5)였다. [중간 앵커][227anchors] · [계측 원행][227diag] · [재생][227replay] | 공개 기대 선노출, 한 OS와 고정판이다. 내부 분기 확인과 원전의 추가 적중·읽기 쉬움은 다른 질문이다. 후자는 원래 기대를 안 본 판독자나 사용자 자료를 요한다. 작업자는 REVIEW_READY로 인계했다. |
| 228 · FreshRSS | 1.29.1 SQLite, 원파일 2개·초회/재수입 8회·20/20자리. 명시 read 3항목은 두 설정 모두 1, read 누락 2항목은 reception=false에서 0, true에서 1이었다. 원형 재수입에서 ID·별표·태그는 유지됐지만 lastSeen은 0으로 바뀌었다. 다른 피드에서 같은 GUID를 한 파일로 준 통제는 3피드·2행과 오연결, 둘로 나눈 경우 3행이었다. [원형][228obs] · [GUID 통제][228collision] · [별도 재생][228replay] | 가공한 read:false는 형식상 지원되지 않았고 UI 표시와 구독 갱신은 검사 범위 밖이다. 같은 원서비스 계정 사용자의 역사적 이관 성공·실제 보존 선호는 미확인이다. |
| 229 · pip | pip 24.0의 세 wheel 고정 HTML 인덱스에서 정확 ==8.1.0은 같은 파일을 고르고 stderr에 #12069 사유를 냈다. 범위 >=8.0.2,<8.1.1은 8.0.2, 철회 속성만 뺀 통제는 8.1.0을 택했다. 대상 링크 부재는 종료 1, 빈 철회 표시는 같은 대상과 사유 미제공 경고였다. 기본 16·보조 2회 모두 새 환경 재생에서 일치했다. [16회 선택][229matrix] · [두 통제][229controls] · [원경고][229warn] · [재생][229replay] | dry-run의 선택·경고까지다. 그 판 실제 설치·pytest 실행, 모든 인덱스 형식, 2024년 소비자 캐시·그때의 최초 경고는 미확인이다. |

### 결론이 부딪힌 지점

| 겉으로 어긋나는 결론 | 관측 대상을 맞춰 내린 판단 | 제품의 안내를 바꿀 근거 |
| --- | --- | --- |
| 219에서는 조건 하나가 첫 설정을 바꾸지만 220에서는 조건어를 추가해도 외부 첫 답이 나아지지 않았다. | **링크를 고르는 데 필요한 사용자 의도**와 **그 단어가 특정 제공자의 순위를 바꾸는 효과**는 독립이다. 220의 자기 이슈가 재현을 확인한 경우와 다른 해법을 찾은 경우도 다르다. | 230의 답글 이전 첫 경로·원작성자 후속과 231의 자기 제외 텍스트/중복 링크가 각각의 질문을 판별한다. [219 경로][219routes] · [220 순위][220paths] |
| 221의 기하 원리는 한 예측을 좁혔고 227에서는 원리와 양립하는 여러 줄 중 서로 다른 줄을 택했다. | 연속장 연결·이진 연결·정책 구현은 다른 목표다. 최장 길이가 옳더라도 실제 보존한 증인과 최종 hunk를 알 수 없다. | 수식·구현·공개 기대의 순서를 보존하고 239에서 동일 입력의 실제 반환 좌표를 확인한다. 232의 조판 원리에도 별도 봉인과 반증을 요구한다. [221 단계별 표][221pred] · [227 예측 대조][227pred] |
| 222의 다른 문자열은 같은 문자를 가리키지만 223의 같은 ‘Change’는 다른 필드를 연다. | 표시 문자열, 검색 입력, 안정 식별자, 행을 눌렀을 때의 동작은 다른 관계다. 감춘 접미사가 다르더라도 실제 한 폼일 수 있다. | 233에서 이름→기관 레코드→저작을, 240에서 별칭 입력→실제 반환을, 241에서 이름→입력·저장·복귀를 확인한다. [222 원행][222names] · [223 목적][223anchors] |
| 224에서는 분모만 고쳐도 잘못된 비율을 거부했고 226에서는 두 속도나 두 시간이 있어도 총노동을 알 수 없다. | 집계 산식이 옳다는 것과 그 행들이 같은 지리·사람·산출물 판·인수 조건에 속한다는 것은 별개다. 한 값이 비어 있는 경우에도 0을 대입할 수 없다. | 238의 공개 원행과 242의 가린 판독, 237의 역할별 시간·결측을 서로 다른 산출물로 남긴다. [224 통제][224controls] · [226 연결키][226joins] |
| 225에서 실제 코드가 바뀌고 228·229에서 실제 기계 상태도 변했지만, 원사용자의 발견 효과는 미확인이다. | 리뷰 반영에는 당사자의 직계 변경이 있다. 수신기나 resolver 실험은 조건 하나와 관측 상태의 관계를 입증한다. 어느 쪽도 당사자가 몰랐던 링크를 발견해 재작업을 줄였다는 전 과정을 증명하지 않는다. | 236은 실제로 제시한 URL·동일 작성자의 행동·다른 이유를 시간순으로 찾는다. 사용자 근거가 비면 ‘이 조건에서 동작함’ 또는 ‘리뷰 뒤 반영함’까지만 쓴다. [225 단계][225claims] · [228 수신][228obs] · [229 선택][229matrix] |

## 다음 배정과 착수 경계

웹 여덟 건은 **각각 단독으로 시작**할 수 있다. 원요구를 확인하는 데 필요한 최소 질문, 다른 해결책으로 가는 경로, 전이할 수 있는 원리, 자료의 동일성, 반드시 함께 줘야 하는 부품, 오래된 근거의 갱신, 실제 선택 변경, 노동 비교라는 서로 다른 제품 결정을 맡는다. 아래의 자료 입구는 신규 조사 결과가 아니다. 표본·실패 경로·필수 표 열·파일·직접 자료 유형별 하한·중간 커밋·마지막 인계 조건은 각 작업의 `brief` 안에 독립적으로 들어 있다. [전체 배정 JSON](NEXT_TASKS-47.json)

230의 단건 이슈 응답 네 개에는 본문과 정수형 댓글 수가 있고, 댓글 내용은 별도 경로에서 읽는다. 219에서 실패한 순차 판독을 이번에는 이 경계에서 봉인할 수 있다. 231은 중복 표시가 가리키는 대상 필드에서, 234는 스타일 제작자의 자원 명세에서, 237은 공개 연구의 두 작성자 시간 열에서 출발한다. [Audacity 단건 이슈 예](https://api.github.com/repos/audacity/audacity/issues/3402) · [Stack Exchange 중복 대상](https://api.stackexchange.com/docs/types/closed-details) · [MapLibre 스프라이트](https://maplibre.org/maplibre-style-spec/sprite/) · [METR 데이터·변수 정의](https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs)

| 작업·담당 | 선행·착수 | 자료·판정 목표 | 완료를 확인할 산출물 |
| --- | --- | --- | --- |
| 230 · web-pro | 219 · 즉시 | Audacity #3402·4811·5302·5797의 단건 이슈 본문에서 파일 단위/시간 원점을 먼저 고정한 뒤 별도 댓글을 읽는다. | 네 첫 안내와 두 갈래 원문 절, 원작성자 후속/다른 사람·미확인 분리 |
| 231 · web-pro | 220 · 즉시 | DBA Stack Exchange에서 PostgreSQL 그룹별 최신 행 질문의 검색 첫 후보와 실제 duplicate 대상 링크를 같은 예산으로 비교한다. | 본표 4건×2경로. 동률·NULL 요구와 각 도착 답의 근거, 빈 경로와 동일 도착을 포함 |
| 232 · web-pro | 221 · 즉시 | 웹 제목의 줄 균형·인쇄 조판 원리·자막의 구문 단위가 다른 줄 선택을 하는지 판독한다. | 게시된 WPT 2건·폭 통제 4건의 단계별 예측, 실제 시험이 단언한 범위 |
| 233 · web-pro | 222 · 즉시 | LOC 전거의 400/500과 저작 연결. Williams의 역사 전사, Kate Davis 교육용 두 자리, 별도 Dumas 부자 실레코드를 구분한다. | 동일·별개·보류 판정. 보강된 Dumas 사례로 지명 미확인을 메우지 않은 전거/저작 원표 |
| 234 · web-pro | 223 · 즉시 | MapLibre demotiles와 Protomaps의 배경·아이콘·글자 레이어에 필요한 스타일, 타일, 스프라이트, 글리프를 따라간다. | 두 스타일×세 역할, 읽기·부분 재사용·오프라인 목적별 필수·대체·보조 자료 |
| 235 · web-pro | 222 · 즉시 | W3C의 날짜 있는 WCAG 세 판·정오표·axe의 실제 규칙에서 Parsing과 Non-text Content의 상태를 비교한다. | 여섯 기준/판 자리, 과거 인용과 현행 개발자 안내에 필요한 절·갱신 조건 |
| 236 · web-pro | 225 · 즉시 | Godot 제안 40건을 먼저 모집하고 기존 기능의 실제 외부 URL을 받은 사람의 후속을 본다. | 최대 여섯 본 사건의 URL·당시 가용성·같은 사람의 시도·산출물·거절·사전 지식. 보강과 무응답 별도 |
| 237 · web-pro | 226 · 즉시 | METR의 공개 개발 과제에서 AI 사용 허용, 작성자의 구현/리뷰 후 수정시간, 외부 검수·인수의 연결 가능성을 판독한다. | 배정별 6원행, 역할과 누락 규칙·인수 범위. 추천 링크 평가에 옮길 최소 측정 설계 |
| 238 · codex-cloud | 224 · 즉시 | 2023 ACS5 기관 원파일의 네 카운티·48셀과 두 결합률을 실제 추출한다. | 원토큰/공식 부재·지문·정밀 계산·다른 경로 재생, 별도 정답과 가린 카드 세 벌 |
| 239 · codex-cloud | 221 · 즉시 | scikit-image 0.25.2·ContourPy 1.3.3의 일곱 배열에서 실제 꼭짓점과 연결 변을 측정한다. | 28회 원좌표, C3·C4 독립 변 쌍 복원 및 별도 축·부호·동률 통제 |
| 240 · codex-cloud | 222 · 즉시 | CPython 3.13.0·ICU 76.1의 이름 검색과 반환값·오류 상태를 공개 API로 확인한다. | 36방향 자리와 13별칭의 하위 호출, 오류상수·sentinel·N/A 원로그 |
| 241 · codex-cloud | 223 · 즉시 | 고정 Apply·Register의 소스 연결 8앵커를 로컬 정상 화면에서 실제 편집한다. | 저장/무수정 16여정의 DOM·접근성 트리·필드 전후·복귀. 실제 발화는 따로 표시 |
| 242 · web-pro | **238 · BLOCKED** | 공개 원행으로 만든 같은 열 명제의 A/B/C 카드를 다른 판독자가 각 단계에서 정답 공개 전에 채점한다. | 30개 판정과 사전 커밋 세 개, 키 공개 뒤 오승인·오기각·보류·표시 비용 |

**238이 중앙 DONE이 되는 것만으로 242가 열리지는 않는다.** 배정자는 고정 인계의 네 지역 원행, 두 유효 합집합률, 10개 명제의 별도 정답 키, 각각 10행인 카드 A/B/C 및 지문을 확인한다. 판독자에게는 그 SHA와 키를 포함하지 않는 manifest만 먼저 준다. 카드 한 벌씩 판정을 커밋한 뒤 정답·원기관 자료를 연다. 참값을 못 얻거나 키가 노출되면 해당 조건은 미달이다. 서로 다른 저작·역할을 분리하는 것 자체가 연구 결과이므로 웹 판독을 배정하고, 기계적 추출·계산은 238에서 마친다. [224 원셀][224rows] · [후속 두 브리프](NEXT_TASKS-47.json)

### 227~229와의 분리

| 요청 때 진행 중이던 작업 | 그 작업이 이미 차지한 대상과 끝점 | 47차에서 지킨 선 |
| --- | --- | --- |
| 227 · Git/Breezy | 210의 여덟 diff 입력에서 내부 앵커·후퇴와 최종 hunk를 비교한다. | 232는 조판 문단과 줄바꿈 선택, 239는 수치 격자의 실제 경계 좌표다. 227의 앵커·원로그가 없어도 두 과제를 시작할 수 있다. hunk의 인간 가독성 효과까지 말하려면 이 출력 고정 후 별도 독자 증거가 필요하다. |
| 228 · FreshRSS | 비식별 송신 파일 2개와 수신 설정 2개에서 원형 가져오기/재수입 뒤 동일 항목의 DB 상태를 본다. | 234는 지도 스타일 레이어가 참조한 그림·글리프 파일의 필수성이다. 피드 GUID·읽음 상태·수신기의 행은 쓰지 않는다. 역사 이관 성공을 주장하려면 228의 재생 외에 같은 이용자의 전후 자료가 필요하다. |
| 229 · pip | 고정 인덱스와 pytest 세 wheel로 정확판/범위의 선택·stderr 경고를 본다. | 235는 W3C 규범 문구·정오표의 적용 시점과 소비자 규칙이고, 240은 Unicode 이름 호출의 반환/오류다. 패키지 resolver 선택·철회판의 파일을 쓰지 않는다. 당시 실제 설치를 주장하려면 그 시점의 설치 기록과 파일이 필요하다. |

세 작업의 요청 당시 상태와 나중의 인계는 각각 위의 시간표와 신규 검토에 반영했다. 이번 즉시 배정은 그 결과를 선행으로 요구하지 않는다. 계획 파일의 READY는 독립 착수 요건을 가리킨다. 중앙 배정·실제 작업 세션 생성은 Dot 진행 절차에 속한다. [당시 세 배정문][req] · [최종 통합판][end]

## 다음 결정을 가장 크게 바꿀 세 가지 약점

| 불일치·약점 | 지금 잘못 쓸 수 있는 문장 | 다음 조사와 판정 전환 조건 |
| --- | --- | --- |
| 최초 노출·원작성자 선택·새 외부 해법이 한 사건에 함께 있는 표본이 드물다. | ‘질문을 하나 더 하면 올바른 답을 찾는다’, ‘새 링크가 패치를 일으켰다’. | 230은 답글 이전 본문만 봉인하고, 231은 두 첫 도착의 실제 해법 절을, 236은 댓글에 실제 포함된 URL과 원제안자의 이후 산출물을 잇는다. 다른 사용자의 반응·원질문 재발견·사전 지식 미확인인 경우를 별도 분모에 둔다. |
| 문서와 소스가 예측한 값이 실제 사용자의 마지막 동작과 다를 수 있다. | ‘논문에서 이 연결을 쓰므로 내 라이브러리도 쓴다’, ‘두 별칭이 같으니 같은 값을 반환한다’, ‘이 Change는 원하는 필드로 돌아온다’. | 239의 원좌표, 240의 동일 빌드 오류 상태, 241의 실제 필드·포커스·복귀가 필요한 증거다. 227의 같은 stdout/다른 분기처럼 표시가 같아도 내부 동작이 다른 반례를 유지한다. |
| 분모·겹치는 구성원·같은 산출물의 인수가 없으면 정확한 숫자로도 잘못된 합계를 만들 수 있다. | ‘실업률을 평균해 결합했다’, ‘검수 속도가 높아 전체 개발 노동이 줄었다’. | 238의 기관 원행과 242의 가린 판정으로 필드 추가의 판단 이득을 확인한다. 237에서 구현자·검수자·인수 판정이 같은 과제에 연결되는 범위를 확인할 때만 노동 주장을 확대한다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/914dbfa789ebec97063ed97130ea2a71c2e9f503/docs/product/RESEARCH_BRIEF.md
[220pairs]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/pairs.csv
[225timeline]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/timeline.csv
[228obs]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/observed.csv
[req]: https://github.com/laadkke-arch/agentflow-open/blob/914dbfa789ebec97063ed97130ea2a71c2e9f503/docs/automation/dot-control.json
[end]: https://github.com/laadkke-arch/agentflow-open/blob/3057e4ede5762f3f7352420085f74016e939c27c/docs/automation/dot-control.json
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/cd60e68d89490a6ad3b6de0b15492eded25de518/docs/workstreams/planning/REVIEW-46.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/2a32cb8a661539308320cf985fc5584588203d52/docs/automation/dot-control.json
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/914dbfa789ebec97063ed97130ea2a71c2e9f503/docs/RESEARCH_WORKFLOW.md
[mid]: https://github.com/laadkke-arch/agentflow-open/blob/de683d7e8319974618062d191a7cc2dace103cae/docs/automation/dot-control.json
[h219]: https://github.com/laadkke-arch/agentflow-open/blob/a2fdcb7da07d9d278fb038dd54d3699d05f946a8/docs/workstreams/research/AF-RES-219/HANDOFF.md
[r219]: https://github.com/laadkke-arch/agentflow-open/blob/b6ee9d2ed8592c2ef1fb10790616c60628c2a64b/docs/workstreams/research/AF-RES-219/RESULT.md
[h220]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/HANDOFF.md
[r220]: https://github.com/laadkke-arch/agentflow-open/blob/7364e529addc20042f45ca68b7012e6ffa1b1988/docs/workstreams/research/AF-RES-220/RESULT.md
[h221]: https://github.com/laadkke-arch/agentflow-open/blob/78a561e00cb9130430bdee7b5c053f740122e973/docs/workstreams/research/AF-RES-221/HANDOFF.md
[r221]: https://github.com/laadkke-arch/agentflow-open/blob/eefc1be2a41ab96a6ce024d86ca9d39394fc545e/docs/workstreams/research/AF-RES-221/RESULT.md
[h222]: https://github.com/laadkke-arch/agentflow-open/blob/fe41449d156eb5e723c254a0530863468c084480/docs/workstreams/research/AF-RES-222/HANDOFF.md
[r222]: https://github.com/laadkke-arch/agentflow-open/blob/e6ed02b1ed41eee07a8c81c6728bd434f95fffc8/docs/workstreams/research/AF-RES-222/RESULT.md
[h223]: https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/HANDOFF.md
[r223]: https://github.com/laadkke-arch/agentflow-open/blob/c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6/docs/workstreams/research/AF-RES-223/RESULT.md
[h224]: https://github.com/laadkke-arch/agentflow-open/blob/c9897ac1ac8a9445e261fd350385a727f9a5d4b2/docs/workstreams/research/AF-RES-224/HANDOFF.md
[r224]: https://github.com/laadkke-arch/agentflow-open/blob/0cfc6fc18747ab78d4dcae2c0d1850ef6914c33f/docs/workstreams/research/AF-RES-224/RESULT.md
[h225]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/HANDOFF.md
[r225]: https://github.com/laadkke-arch/agentflow-open/blob/d00f774245da1c10b6174270da62db84ae38db7c/docs/workstreams/research/AF-RES-225/RESULT.md
[h226]: https://github.com/laadkke-arch/agentflow-open/blob/d166817bc25f79650f2d02835b0f5f42617cdbdd/docs/workstreams/research/AF-RES-226/HANDOFF.md
[r226]: https://github.com/laadkke-arch/agentflow-open/blob/8b9445c89969db89f1cc02e8e504b8b1bf02e18d/docs/workstreams/research/AF-RES-226/RESULT.md
[h227]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/HANDOFF.md
[r227]: https://github.com/laadkke-arch/agentflow-open/blob/70b89c4f71c7638fe75ed0b17a42e2a9f7c702c1/docs/workstreams/research/AF-RES-227/RESULT.md
[h228]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/HANDOFF.md
[r228]: https://github.com/laadkke-arch/agentflow-open/blob/e0d151c1d0565631c31196e2c3067fa79643947a/docs/workstreams/research/AF-RES-228/RESULT.md
[h229]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/HANDOFF.md
[r229]: https://github.com/laadkke-arch/agentflow-open/blob/a10e044150195e0c3d7219c5314b54d35dee6f66/docs/workstreams/research/AF-RES-229/RESULT.md
[220raw]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/receipts/INDEX.json
[227diag]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/receipts/diagnostic-base.jsonl
[228off]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/receipts/S02-r0.json
[228on]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/receipts/S02-r1.json
[229warn]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/receipts/main/pin-target-baseline-r1/stderr.txt
[229absent]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/receipts/controls/pin-target-missing-r1/stderr.txt
[219routes]: https://github.com/laadkke-arch/agentflow-open/blob/a2fdcb7da07d9d278fb038dd54d3699d05f946a8/docs/workstreams/research/AF-RES-219/routes.csv
[221inputs]: https://github.com/laadkke-arch/agentflow-open/blob/78a561e00cb9130430bdee7b5c053f740122e973/docs/workstreams/research/AF-RES-221/inputs.csv
[227anchors]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/anchors.csv
[220queries]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/queries.csv
[222cons]: https://github.com/laadkke-arch/agentflow-open/blob/fe41449d156eb5e723c254a0530863468c084480/docs/workstreams/research/AF-RES-222/consumers.csv
[223anchors]: https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/anchors.csv
[224rows]: https://github.com/laadkke-arch/agentflow-open/blob/c9897ac1ac8a9445e261fd350385a727f9a5d4b2/docs/workstreams/research/AF-RES-224/rows.csv
[224controls]: https://github.com/laadkke-arch/agentflow-open/blob/c9897ac1ac8a9445e261fd350385a727f9a5d4b2/docs/workstreams/research/AF-RES-224/controls.csv
[229matrix]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/matrix.csv
[225claims]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/claims.csv
[226labour]: https://github.com/laadkke-arch/agentflow-open/blob/d166817bc25f79650f2d02835b0f5f42617cdbdd/docs/workstreams/research/AF-RES-226/labour.csv
[226pair]: https://github.com/laadkke-arch/agentflow-open/blob/d166817bc25f79650f2d02835b0f5f42617cdbdd/docs/workstreams/research/AF-RES-226/review-pair-witness.csv
[227replay]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/receipts/replay-summary.json
[229replay]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/receipts/replay-audit.json
[219requests]: https://github.com/laadkke-arch/agentflow-open/blob/a2fdcb7da07d9d278fb038dd54d3699d05f946a8/docs/workstreams/research/AF-RES-219/requests.csv
[220paths]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/paths.csv
[221pred]: https://github.com/laadkke-arch/agentflow-open/blob/78a561e00cb9130430bdee7b5c053f740122e973/docs/workstreams/research/AF-RES-221/predictions.csv
[222names]: https://github.com/laadkke-arch/agentflow-open/blob/fe41449d156eb5e723c254a0530863468c084480/docs/workstreams/research/AF-RES-222/names.csv
[223returns]: https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/returns.csv
[223frame]: https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/frame.csv
[224ratios]: https://github.com/laadkke-arch/agentflow-open/blob/c9897ac1ac8a9445e261fd350385a727f9a5d4b2/docs/workstreams/research/AF-RES-224/ratios.csv
[225assert]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/assertions.csv
[226joins]: https://github.com/laadkke-arch/agentflow-open/blob/d166817bc25f79650f2d02835b0f5f42617cdbdd/docs/workstreams/research/AF-RES-226/joins.csv
[228collision]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/receipts/C1-collision.json
[228replay]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/receipts/container-replay.json
[229controls]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/matrix-controls.csv
[227pred]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/predictions-comparison.csv
