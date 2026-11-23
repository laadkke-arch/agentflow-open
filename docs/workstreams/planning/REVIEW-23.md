# REVIEW-23 · 같은 결과처럼 보일 때 어느 링크까지 권할 수 있는가

탐색기가 링크 하나로 무엇을 약속할 수 있는지는 사용자가 그다음에 할 일에 달려 있다. MuseScore에서는 복제본의 표시가 다른 두 구현이 실제 편집에서는 같은 두 음을 바꿨다. GeoParquet에서는 정반대로 **파일 바이트가 같은데도 ‘원래 Point였던 행’의 정답이 달랐다.** 두 링크를 대체품으로 묶을 때 보존해야 할 값과 후속 조작을 함께 보는 이유다. 문서에 외부 자원이 필요하거나 검색 결과에 다른 처리 단계가 끼는 경우에는 그 자원을 실제로 열 수 있는지도 아직 가려야 한다. [MuseScore 대응 실행][v89] · [GeoParquet 동일 파일 대조][alias91] · [문서 경로][trav90] · [검색 노출][search92]

## 범위와 판정 근거

2026-11-23 UTC, work/planning의 최신 [REVIEW-22][prev]를 먼저 읽고 그 검토가 사용한 진행표 62a80b9와 이번 e2a80af를 ID별로 비교했다. 등록 **86→90**, DONE **84→88**, BLOCKED **2→2**다. 기존 86행의 값은 모두 같았다. AF-RES-018(범용 LLM 검색과의 비교)과 035(Go·DLPack 실행)가 계속 BLOCKED다. 새 DONE은 089–092 네 건뿐이며, DONE 88행 중 acceptance_evidence에 항목이 있는 행은 0이다. 088까지의 결론은 REVIEW-22에서 이어받았고, 이번에는 새 네 작업의 고정 인계·결과·원장을 열었다. 실행 횟수와 출력은 작업자가 남긴 기록을 재집계했다. [이전 진행표][old] · [현재 진행표][reg]

| 새 DONE · 담당 | 인계판 · 검사한 결과판 | 직접 대조한 결과 | 이 검토에서 수용한 범위 |
| --- | --- | --- | --- |
| 089 · codex-cloud | [dad9574][h89] · [4f7ace7][r89] | 정식 메뉴 8회와 양성·음성 대조 4회, 변경 객체·Undo·재열기, Voice 1 필터 원 로그 | **REVIEW_READY**. 두 입력·두 복제 구현에서 작동한 명령의 실제 대상 |
| 090 · web-pro | [e5f6cf5][h90] · [03c6102][r90] | 고정 16경로, 실제 22열람의 상태·본문·후속 자료·판 관계와 목적별 반환 카드 | **PARTIAL**. 정한 두 번의 열람에서 실제 얻은 내용과 막힌 위치 |
| 091 · codex-cloud | [f74a55d][h91] · [952c813][r91] | 8회 쓰기, 16개 읽기 자리, writer 예외와 별도 동일 바이트 대조, 실제 소비 코드 | **REVIEW_READY**. 고정 스택의 쓰기 가능 여부와 관측 가능한 행 선택 |
| 092 · web-pro | [e0d7ecd][h92] · [707216d][r92] | 신규 6질문·12경로의 사전 판정, 검색·접근 원장, 현재 채택과 질문자 후속 | **PARTIAL**. 주어진 탐색 절차의 결과와 실패. 여섯 쌍 전체의 효과는 미확인 |

각 등록 result_commit은 해당 작업 브랜치 끝과 같고 네 마지막 커밋은 각각 HANDOFF.md 한 파일만 추가했다. 090은 검사한 결과판과 최종 인계 사이에 검사 영수증 커밋이 하나 더 있다. 아래의 원 출력은 각 결과판에 연결했다. [089 인계 커밋][c89] · [090 영수증][rec90] · [091 인계 커밋][c91] · [092 인계 커밋][c92]

## 앞선 검토에서 이어받은 제품 판단

사용자는 만들려는 소프트웨어의 전체나 일부 구조와 목적을 건넨다. 돌려줄 대상에는 바로 쓸 제품, 연결할 기능·부품, 실패를 발견하는 데 옮겨 쓸 다른 분야의 원리가 있다. 최종 설계자는 근거가 있는 묶음을 골라 재조합한다. 입력 JSON, 링크에 저장할 필드, 크롤러, DB, 검색 엔진, 화면 구성은 열린 선택이다. [제품 브리프][product] · [연구 운영 규칙][workflow]

| 설계 질문 | 누적 조사에서 얻은 근거 | 지금 설계자가 사용할 범위 |
| --- | --- | --- |
| 부분 요청에 무엇을 더 물을까 | 020은 주장 72/73을 전달했으나 충돌을 완전히 해소한 경우는 2/16이었다. 070의 자연 요청 24건에는 답변 하나가 정오를 바꿨다고 독립 판정할 분모가 없었다. 074의 구성 대조에서는 조건을 주자 8/8에서 답이 하나로 좁혀졌다. 082의 옛 Python 요구는 이미 명시돼 있었고, 088 JN1은 전체 JSON 추가 뒤에도 map 링크가 같고 다음에 물을 것은 Bash 소비 방식으로 바뀌었다. | 사용자가 이미 준 조건, 빠진 조건, 그 답을 들으면 바뀔 링크를 따로 적을 수 있다. 092 J2의 새 값과 선택 기준은 여전히 공석이다. 연구자가 넣은 예시 값을 사용자 요구로 채우면 원뜻을 바꾼다. [누적 검토][prev] · [092 최초 요구와 후속][r92] |
| 다른 분야의 원리는 어디에 도움이 되나 | 010은 분야 단서로 원리군 7개를 얻었다. 033의 단서 없는 144쌍은 넓은 의미 지지 1, 당시판 지지 0이었다. 069·073은 요청 접수와 실제 적용, 저장소 이전과 유지 책임 인수를 구별했다. 077 보조 3건에서 핵심 구현 선택 변화는 0이었다. 081은 두 복제안의 차이를 드러낼 입력을 찾았고 085는 숨은 자식의 선택색을 관측했다. | 다른 분야에서 가져온 질문으로 시험 입력과 실패 조건을 제시할 수 있다. 089의 화면색·선택 목록, 091의 팔레트 색·원 인덱스처럼 다음 연산을 정해야 전이 범위가 보인다. 원 개발자가 그 선례 때문에 결정을 바꿨는지는 미확인이다. [누적 검토][prev] · [089 비교 사례][r89] · [091 팔레트·행 선택][r91] |
| 링크 설명을 늘리면 검증이나 작업시간이 나아지나 | 021의 같은 두 절 열람에서 공식 근거 회수는 주소만 6/23, 절 목록 9/23, 조건과 절을 맞추면 14/23, 잘못 맞추면 8/23이었다. 066에서는 같은 주소가 반대 권고에도 붙었다. 022의 결정 우선 표본에서 미인지→결정 변경→실행이 모두 확인된 수는 0/24였다. 034의 부분 시간은 380→57초였으나 전체는 849→847초였다. 078에서는 두 기능이 각각 작동해도 합성에서 갈렸다. | 볼 절과 쓰임을 구체화할 근거는 있다. 사람이 실제로 덜 고쳤거나 빨리 끝냈다고 주장하려면 사람의 전체 작업·결과 관측이 필요하다. 090의 열람 횟수와 바이트, 092의 채택 표지는 각각 다른 측정값이다. [누적 검토][prev] · [090 열람 집계][count90] · [092 공개 후속][out92] |
| 어떤 판과 자료를 같은 것으로 보며 무엇을 보관할까 | 032의 배포 참조 12건은 유지 9·교체 2·보류 1이었다. 055는 과거 답 4/4를 다시 얻었지만 다음 판은 0/4였다. 071의 통제 22/22, 075의 양성 존재 15/15를 복구해도 유일·공동 1위 판단은 각각 16/16 보류였다. 079의 옛 GDAL 경로에서는 geometry·CRS가 사라졌고, 083의 실제 안내는 PyArrow를 사용했다. 087의 GeoPandas에서는 같은 1.1.0이라도 WKB와 native의 reader 호환이 갈렸다. 086의 과거 제공 주 관측창은 0/9 확인이었다. | 파일·판·호출자를 고정하면 과거에 내린 좁은 결론을 재현할 수 있다. 090의 동일 HTML은 후속 파일판까지 보장하지 않았고 091의 동일 native 바이트는 원 행 타입을 지목할 수 없었다. 어떤 질문에 쓸 기록인지부터 정해야 한다. [누적 검토][prev] · [090 자원 대조][asset90] · [091 원 타입][alias91] |
| 기능 목록과 검색 범위를 넓힐 때 무엇이 늘어나는가 | 060·064·068에서 이름과 첫 절을 개선해도 두 필수조건의 공동 근거가 자주 비었다. 076의 자연 6요구×20후보 직접 양성은 0이었다. 080의 범위 확장으로 양성이 된 비율은 비교 가능한 자연 1/5, 교정 3/5였다. 084의 선택된 4요구는 확보본에서 양성 3·기본 조합 반박 1을 얻었고 개설 본문은 0/4였다. 088의 비교 가능 26쌍은 개정 전후 판정 변화 0, 채택 주해법 3건은 모두 좁은 후보 밖이었다. | 기능 목록에서 빠짐, 주 도구 전체에서 빠짐, 검색 결과에 노출되지 않음은 따로 추적할 수 있다. 092의 P3 해법은 두 경로에서 모두 열 수 있었던 주 도구 안에 있었고 둘 다 놓쳤다. [누적 검토][prev] · [092 사전 쌍][pairs92] · [사후 해결 보고][out92] |

## 새 근거와 결론이 어긋난 자리

### 089 · 선택색, 실제 편집 대상, Undo

085에서는 복제 직후 선택 비트가 다른 G/L 쌍이 6/8이었지만 주 키로 문서값이 바뀐 것은 0/24였다. 선택 목록이 비었거나 그 키가 단일 음을 요구했다. 089에서는 Explode 뒤 범위에 적용되는 가시성 명령 V를 보냈다. 기본 필터의 두 악보×두 빌드×두 반복에서 8/8회 값이 바뀌었다. G는 공통 복사에서 선택 비트를 지우는 병합안, L은 새 파트 요소 순회에서 지우는 안이다. 4/4 대응쌍에서 두 구현은 같은 두 음을 바꿨다. V 하나를 Undo하면 8/8에서 Explode 결과는 남고 가시성은 복구됐다. 별도 양성 2/2에서는 값이 바뀌고 음성 2/2에서는 빈 선택이 그대로였다. 정식 저장본 재열기 22/22가 객체값 판정과 맞았다. [정식 12회][run89] · [짝별 검산][v89]

결론이 갈리는 입력은 Voice 1을 제외한 X1이다. 수동 선택에서는 V가 작동했다. 메뉴가 E4를 필터 밖 성부로 옮긴 뒤에는 두 구현 모두 대상이 0개였고 Undo 인덱스는 1→1이었다. L에서만 E4가 선택색을 띠면서 실제 목록 밖에 남았다. **잘못된 표시를 없애려는 질문에는 G, 실제 명령 대상을 알고 싶은 질문에는 범위 재선택·목록 순회 코드**가 근거가 된다. 주 실험은 두 단순 악보의 master 탭에서 한 V다. 기존 Violin 피어의 보존이나 별도 G4 가시성 시험으로 다른 속성의 파트 전파, 부분 마디·tie, 사용자의 재클릭 절감까지 결론 내릴 수 없다. [필터 원 로그][filter89] · [목적별 구현과 대조][r89]

### 090 · 본문, 외부 자원, 독자가 원하는 판

네 프로젝트에서 두 목적과 두 입구를 교차한 16경로를 다시 세면 22문서 열람, HTTP 200 17회·404 2회·503 3회다. 지정판 본문 목적은 3/8 충족했다(cibuildwheel 두 입구, asciicast 현재 안내). 지정 본문·봉인한 후속 자원·필요한 판 관계를 모두 채운 후속 목적은 0/8이다. 그중 archive의 현재 예제에서 system.file 도움말 자체는 1/8 읽혔지만 1.1.12 생성 당시 R판과 연결할 근거가 비었다. cibuildwheel에서 stable 입구도 두 번째 열람에 3.3.0 본문을 찾았다. 같은 메뉴로 간 1.x/options의 식별자 목록은 지정한 1.x 루트 지원 표와 달랐다. [16경로 원장][trav90] · [목적별 분모][count90]

086은 현재 HTTP 200이 8/9, 목표판 내용 식별이 4/9였으나 주 관측창의 당시 제공은 9/9 미확인이었다. 고정 생성 HTML에서 archive의 옛 본문을 읽을 수 있어 네 권고 중 한 건을 바꿨다. 090에서 그 GitHub 입구의 HTTP 503과 별도 UI의 소스 열람은 서로 다른 시점·수단이었다. 직접 적격 자료 45건이 18개 저작·사건 계보에 걸쳐 있어도 두 주소·세 경로의 503이 얼마나 지속됐는지는 미확인이다. asciicast의 현재·고정 HTML은 15,974바이트 모두 같았지만 Source가 가리킨 HEAD의 Rmd는 고정 Rmd와 달랐다. 해당 절의 정적 출력은 읽혔고 SVG/cast 재생 데이터는 명시된 경로에서 찾지 못했다. 090은 회수와 판 귀속을 분리했지만 **두 번째 링크를 실제로 제공했을 때 추가로 성공하는 독자 경로**를 시험하지 않았다. R·Python·재생 실행과 사람의 소요시간도 미측정이다. [090 카드][cards90] · [파일별 관측][asset90] · [인계의 접근 경계][h90]

### 091 · 파일이 생기는 조건과 같은 파일에서 되찾을 수 있는 행

고정 GeoPandas 1.0.0 스택에서 4입력×2인코딩의 쓰기를 시도해 WKB 4파일과 동종 2D native 1파일이 생겼다. 혼형에 빈 단수 Point가 함께 든 S1–S3 native는 writer의 ArrowInvalid로 거절됐다. 따라서 예정한 16읽기 중 **실제 10회, 파일 미생성 6자리**다. 실제 판독 10/10에서는 원 타입으로 고르는 T와 XY 사각형과 교차하는 P가 각각 자기 기대 ID·score와 일치했다. 인코딩 간 8대응쌍 중 양쪽을 읽은 것은 동종 S0의 2쌍뿐이다. 거절을 reader 실패로 세거나 ‘혼형도 10/10 보존’이라고 쓰면 분모를 잘못 읽는다. [쓰기 원장][files91] · [S1 예외][err91] · [읽기 원장][run91] · [대응쌍][sum91]

빈 Point를 뺀 보조 입력에서는 A가 MultiPoint로 승격돼 T에서 빠지고 P에는 남았다. A와 B 중 어느 쪽이 원래 단수인지 맞바꾼 두 입력의 native 파일 SHA-256은 8174134afb03…로 완전히 같았다. 원 T 정답은 한쪽 A/101, 다른 쪽 B/NA였다. 이 파일과 타입 목록만으로 두 정답을 복원할 수 없다. 별도 S3의 B는 물리 Z에 NaN이 있는데 고정 reader에서 2D였고, S2의 두 유한 Z는 살아 있었다. 087의 WKB는 두 reader에서 12/12 보존됐다. 같은 1.1.0의 동종 native는 옛 reader에서 2/2 명시 거절, 새 reader에서 2/2 보존이었다. 이번의 쓰기 거절·원 타입 소실까지 구별하려면 **입력, writer, 소비 술어**가 필요하다. 공개 .cx 호출은 연구 입력에 실행했으며 실제 옛 안내 때문에 피해를 본 사용자의 파일·판·기대값 연결은 여전히 미확인이다. [동일 바이트의 두 원입력][alias91] · [Z 출력][z91] · [소비자 호출의 범위][cons91]

### 092 · 인접 자료를 허용하는 것, 노출하는 것, 답을 완결하는 것

A는 주 도구의 자료만, B는 질문에 근거가 있는 인접 도구의 자료까지 허용했다. jq·Pandoc 신규 6질문×2경로에서 엄격 비교 가능한 5쌍은 **A만 완결 0, B만 0, 양쪽 2(J1·J3), 어느 쪽도 완결 아님 3**이다. jq 세 건은 실제 허용 집합이 같았다. 집합이 다른 유효 P1·P3에서 B 단독 완결은 0/2였다. P2-B는 부분 코퍼스 검색 1회·전면 실패 1회와 실패 포함 본문 접근 5회로 예산 4를 넘겼다. 이 쌍은 비교불가다. 검색 원장의 검색 24·본문 33·실패 접근 1·경로 탐색 9를 다시 셌다. 순위에 노출된 인접 원문은 0이고, 인접 파일 6개는 경로를 따로 찾아 열었다. 직접 원자료 40건(저작·사건 29그룹)을 확보했어도 A만 또는 B만 완결한 쌍이 없어 그 안의 승률은 산출할 수 없다. **인접 자료를 실제로 노출했을 때의 효과는 이 0/5로 판정할 수 없다.** [검색 원장][search92] · [엄격 쌍][pairs92] · [노출·비용 집계][metrics92]

현재 채택은 5/6이고 P3에는 질문자의 해결 보고가 1건 있다. 사후 해법은 Pandoc reader의 example_lists를 끄는 것이었다. 두 경로 모두 이를 놓쳤다. P3 원문이 실제로 어떤 구문 트리(AST)로 읽혔는지는 미확인이다. 정확판·입력·명령·출력이 모두 갖춰진 질문자 실행은 0/6이다. P2에서 Pandoc 소스만 읽은 사전 ‘완결’을 원 Quarto 사슬의 ‘부분’으로 낮춘 이유도 여기에 있다. 질문의 Qmd와 두 매크로는 보존됐고 해당 Quarto에서 생성한 tex·PDF는 없었다. 088의 ‘좁은 후보 밖에 채택 답 3개’와 이번 ‘넓혀도 추가 완결 0’은 비교 대상이 다르다. 공정한 검색 실험과 알려진 해법의 정확판 실행에는 서로 다른 입력이 필요하다. [공개 후속][out92] · [보존된 P2 입력][input92] · [후속 검증의 범위][next92]

## 다음 배정

| ID · 담당 | 독립적으로 인수할 완료 작업 | 이번에 가를 판단과 필수 산출 |
| --- | --- | --- |
| 093 · web-pro | [089][h89], [091][h91] | 두 결과는 교정용으로 두고 Inkscape·Pillow의 새 부분 요청 6건에서 ‘다음 조작과 보존할 값’을 기록하기 전후의 오병합·불필요한 분리·유보를 비교한다. 묶어도 되는 링크와 따로 돌려줄 링크를 남긴다. |
| 094 · codex-cloud | [090][h90] | 같은 본문에서 시작해 후속 URL만 더한 카드의 효과를 6목적×2카드×2접근 수단에서 실행한다. 소스 보기, 실제 자원, 목적판 귀속을 분리해 두 번 안에 얻는 것을 보고한다. |
| 095 · codex-cloud | [092][h92]의 P2 고정 입력 | Quarto 1.4.553의 실제 번들로 원본과 두 매크로를 단일 표·두 표 문서에서 두 번씩 변환한다. 12자리의 생성 tex, PDF의 두 선·셀 값·다른 표에 미친 영향으로 권고 범위를 정한다. |
| 096 · web-pro | [092][h92]의 검색·예산 원장 | P2를 포함한 알려진 질문을 제외하고 새 8건을 모집한다. 주 도구 파일만 노출한 방식과 인접 파일에도 자리를 배정한 방식을 같은 4접근 예산으로 대조한다. 어느 쪽만 완결했는지와 밀려난 후보를 함께 남긴다. |

095와 096은 같은 완료 인계에서 각각 재현 입력과 검색 절차만 가져간다. 어느 신규 작업도 다른 신규 작업의 결과를 기다리지 않는다. MuseScore의 다른 편집 명령, GeoPandas의 다른 reader, P3의 원 서지 파일은 계속 열린 질문이다. 이번 배정은 이미 관측한 두 국소 차이를 새 편집·이미지 요구에 적용하고, 비교가 성립하지 않았던 문서 접근과 검색 노출을 직접 가르는 데 우선순위를 뒀다. 각 작업의 원문 최소량, 필수 표의 열, 결원 처리와 마지막 인계 조건은 독립 배정문에 들어 있다. [다음 작업 네 건](NEXT_TASKS-23.json)

[prev]: https://github.com/laadkke-arch/agentflow-open/blob/cf011015e6e21d8b3c58b237cb445e8f2a3322c6/docs/workstreams/planning/REVIEW-22.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/62a80b9f111c695527a8ca87bcb867796d2e96bb/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/e2a80afec762b10ee7979136c6332473c70905bb/docs/automation/dot-control.json
[product]: https://github.com/laadkke-arch/agentflow-open/blob/e2a80afec762b10ee7979136c6332473c70905bb/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/e2a80afec762b10ee7979136c6332473c70905bb/docs/RESEARCH_WORKFLOW.md
[h89]: https://github.com/laadkke-arch/agentflow-open/blob/dad9574f3ef1831e50071a019e5e80b6e8dc8983/docs/workstreams/research/AF-RES-089/HANDOFF.md
[r89]: https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/RESULT.md
[h90]: https://github.com/laadkke-arch/agentflow-open/blob/e5f6cf5b1cb27b926ebc2356f9a8b763cebfcc87/docs/workstreams/research/AF-RES-090/HANDOFF.md
[r90]: https://github.com/laadkke-arch/agentflow-open/blob/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090/RESULT.md
[h91]: https://github.com/laadkke-arch/agentflow-open/blob/f74a55d70b38d8585ff3512fe478442917444441/docs/workstreams/research/AF-RES-091/HANDOFF.md
[r91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/RESULT.md
[h92]: https://github.com/laadkke-arch/agentflow-open/blob/e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf/docs/workstreams/research/AF-RES-092/HANDOFF.md
[r92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/RESULT.md
[c89]: https://github.com/laadkke-arch/agentflow-open/commit/dad9574f3ef1831e50071a019e5e80b6e8dc8983
[c91]: https://github.com/laadkke-arch/agentflow-open/commit/f74a55d70b38d8585ff3512fe478442917444441
[c92]: https://github.com/laadkke-arch/agentflow-open/commit/e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf
[rec90]: https://github.com/laadkke-arch/agentflow-open/commit/870ac87f09225cbc346fa09fe4fe35dfa5b6a131
[v89]: https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/evidence/verify.json
[run89]: https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/runs.jsonl
[filter89]: https://github.com/laadkke-arch/agentflow-open/blob/4f7ace747bfc5313679b8023ce85b4e7cc3217f2/docs/workstreams/research/AF-RES-089/evidence/aux/F-X-L/app.jsonl
[cards90]: https://github.com/laadkke-arch/agentflow-open/blob/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090/cards.md
[trav90]: https://github.com/laadkke-arch/agentflow-open/blob/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090/traversals.csv
[count90]: https://github.com/laadkke-arch/agentflow-open/blob/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090/evidence/counts.json
[asset90]: https://github.com/laadkke-arch/agentflow-open/blob/03c6102d6c0d90f6722550d5e2cb1c7219e49b5f/docs/workstreams/research/AF-RES-090/assets.jsonl
[alias91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/evidence/auxiliary/type-alias.json
[run91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/runs.jsonl
[cons91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/consumers.csv
[sum91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/evidence/read/summary.json
[err91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/evidence/build/S1-native-writer.json
[z91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/evidence/auxiliary/S3-drop-E.json
[files91]: https://github.com/laadkke-arch/agentflow-open/blob/952c81311dc7b5917fa04af6e4513dc5fd7020b0/docs/workstreams/research/AF-RES-091/files.csv
[search92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/searches.jsonl
[metrics92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/metrics.json
[pairs92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/pairs.csv
[out92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/outcomes.csv
[input92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/evidence/next-inputs/README.md
[next92]: https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/NEXT_ACTIONS.md
