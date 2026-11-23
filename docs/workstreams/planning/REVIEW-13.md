# REVIEW 13 · 설계자가 링크에서 확인할 수 있는 것

이 연구의 목표는 설계 중인 소프트웨어의 전체나 일부와 그 목적을 받아, 바로 쓸 제품·부품이나 다른 분야에서 빌려올 원리를 찾아 주는 것이다. 지금까지 가장 잘 입증된 반환 단위는 **어떤 판의 어느 절이 사용자의 어느 조건을 뒷받침하는가**다. 이번에는 같은 조작도 소프트웨어 판에 따라 출력이 달라지고, 서로 다른 자료판도 같은 숫자를 낼 수 있음을 확인했다. 사람이 링크를 받고 동등한 품질의 설계를 더 빨리 마쳤는지, 검색 결과를 묶으면 실제 선택 가능한 구현이 늘어나는지는 여전히 미확인이다. [제품 연구 브리프][product] · [연구 운영 규칙][workflow]

### 인수 범위

계획 브랜치 `ef8ecd3`에서 가장 최근 번호인 REVIEW-12를 먼저 읽었다. 그 검토의 통합판 `d8c8d02`와 이번 `d7e60da`의 진행표를 ID별로 비교했다. **등록 46→50, DONE 44→48, BLOCKED 2→2. 새 DONE은 AF-RES-049~052 네 건**이다. 예전 작업은 REVIEW-12의 누적 검토를 사용했다. 새 네 작업만 각 소유 경로의 인계·결과와 판정 원장까지 열었다. 네 진행표 결과 SHA는 작업 브랜치 끝과 같고, 끝 커밋에서 바뀐 파일은 각각 HANDOFF.md 하나다. 인계서가 지정한 본문 SHA에서도 RESULT.md의 Git blob이 같았다. 아래에서 재검산한 것은 저장된 행과 검사 기록이다. 외부 원문 열람·실행·사람 실험의 관측 주체는 해당 작업자와 원 연구자다. [직전 검토][prev] · [직전 진행표][oldreg] · [이번 진행표][reg]

| 작업 | 인계 / 본문 고정판 | 원문과 수용 원장에서 확인한 범위 |
| --- | --- | --- |
| 049 · 그림 좌표·범례 | [ae40dc2][h49] / [ab50b40][r49] | 고유 1차 저작 34개. 24조건 중 충족 20, 미충족 2, 미확인 1, 범위 밖·미확인 1. 인계 상태는 부분이다. [수용 원장][a49] |
| 050 · 사람의 시간과 최종 품질 | [a3e1307][h50] / [5797f9a][r50] | 고유 1차 저작 25개 중 지정 범주에 적격 19, 실제 배당 충족 17/24. 27조건 중 통과 20, 부분 6, 마지막 인계 대기 1이었다. 단독 인계는 후속 커밋에서 확인했다. [수용 원장][a50] · [자료 배당][sources50] |
| 051 · 파일·필드·산출값의 관계 | [537712e][h51] / [4e1a76c][r51] | 원문 배당 26개(최소 22). 23조건 중 충족 20, 운영 교통 개정판 미확인 1, 사후 검증 대기 2였다. 대기 2건은 고정판 재열람과 계약 검사 영수증에서 확인했다. 인계 상태는 검토 가능이다. [수용 원장][a51] · [사후 검사][ver51] |
| 052 · 세 자리의 대표 링크 | [6e6818e][h52] / [3da61ff][r52] | 지정 24저작 충족. 15조건 중 충족 6, 제한부 충족 5, 부분 2, 추정 불가 1, 미관측 1. 자연 요구와 연결된 후보 풀이 없어 부분 인계다. [수용 원장][a52] · [자료 배당][s52] |

중앙 DONE 48건의 `acceptance_evidence`는 모두 빈 배열이다. 새 네 건의 `source_commit`과 `actual_model`도 비어 있다. 018은 세 번째 시도에서 대화 길이 한도에 도달했고, 035는 첫 시도에서 사이버 보안 위험 가능성 표시로 종료됐다. 두 작업 모두 진행표에 결과 SHA가 없고 정식 인계가 확인되지 않았다. [이번 진행표][reg]

### 048까지의 결론을 어떻게 이어 쓰는가

| 설계 판단 | 그동안 확인된 근거 | 결정을 제한하는 반례와 미확인 |
| --- | --- | --- |
| 부분 입력·식별 · DOT-001~002, RES-001~004·016·020·026·030 | 인계를 다른 세션에서 복원했다. 합성 입력 6건에서 부정 조건이 빠졌고, 2문제·17질의에서 같은 이름의 제품과 부분 기능이 섞였다. 주소·가리킨 대상·사용 목적을 구별할 필요가 있었다. 020의 주장 전달은 72/73이었다. | 016의 내부 판독 일치는 후보 형태 78.3%, 기여 70.8%였다. 020의 충돌 16건 중 완전 해소는 2건이다. 026에서 질문을 실제 보낸 사례는 0, 030의 자연 24건 중 같은 변수에 직접 답한 경우는 3건이며 그 뒤 같은 답변자의 권고 변경과 요청자의 신규 시행까지 이어진 경우는 0/3이었다. 입력 계약과 되묻기 기본값은 열려 있다. [누적 근거][prev] |
| 같은 목적의 부품과 타 분야 선례 검색 · 009~014·025·029·033 | 비교 시스템 35개의 기능이 겹쳤다. 010은 분야 단서를 받은 24원문에서 원리 7군을 찾았다. 011은 실제 61스레드·635답에서 부분 질문 33건 중 10건의 진전을 찾았다. 다른 분야로 옮겨온 답 14개에는 질문자 반응이 없었다. 013의 역사적 선례 176개 중 웹 검색 회수는 16, 목록은 5였다. | 012의 합성 질의에서 늘었던 근접 오답은 014의 실제 자료 485개에서 재현되지 않았다. 025는 72칸 중 지지 2·충돌 14·보류 53·빈칸 3이었다. 029에서 공통 검색·추가 웹 검색·제공자 내부 탐색의 부분 요구 완결은 2/12·4/12·3/12, 전체는 모두 0/12였다. 분야 힌트를 뺀 033은 8요구×18후보에서 엄격 지지가 넓게 봐도 1/144, 당시판 기준은 0이었다. 상위 세 자리 완결도 두 방식 모두 0/8이었다. [누적 근거][prev] |
| 선례가 실제 결정을 바꾸었는가 · 017·022·037·041·045·046 | 017은 40사건 중 18건에서 두 날짜를 이었다. 022 결정 우선층에서 이미 알던 대안의 조건을 바로잡아 시행한 사례가 2/24 있었다. 037의 같은 목적 반영은 결정 우선 7/8, 출처 노출층 3/4였다. 041의 pdfTeX·LilyPond 두 저자는 출처를 넓게 명명했다. 046의 링크 우선 리뷰 4건 중 같은 작성자·같은 목적 수정은 2건이었다. | 022에서 미인지→당시 가용→변경→시행은 결정 우선 0/24, 발견 진술 우선 1/9였다. 037·041에선 최초안 변경의 엄격 인과가 확인되지 않았다. 045는 6요구 중 두 원리의 예측이 3건에서 갈렸지만 정상·경계 양쪽을 판정할 엄격 적격 사례는 0건이었다. 046의 자연층은 적격 링크 0/8, 보강층은 첫 링크를 명시적 이유로 든 작성자의 패치·시험까지 0/4였다. [누적 근거][prev] |
| 근거 설명과 사람 과제 · 021·034·038·042 | 021에서 두 절을 열어 요구가 완결된 수는 주소만 6/23, 절 목록 9/23, 요구–절 대응 13/23이었다. 잘못 연결하면 8/23이었다. 038은 네 과제의 자료·루브릭을 고정했고 042는 pandas의 두 고정판에서 43/43 출력과 근접 오답 5개를 구별했다. | 038의 사람 참가자는 0명이다. 034의 22연구군·26실험 중 NCQ에서 패키지 선택 중앙값은 380→57초, 같은 실험의 전체 과제는 849→847초였다. 046의 12자리에도 동등 품질 노동시간 쌍이 없었다. [누적 근거][prev] |
| 추천 이유의 수명·점검 예산 · 015·019·024·028 | 015의 판정 가능한 현재 추천 195개 중 이유가 무너진 것은 14개였다. 과거 복원 83개에서는 후발 붕괴 5·최초 오류 4였다. 024의 64이유×16분기에서 유지 897·무효 95·최초 오류 16·보류 16이 나왔다. | 019의 사건과 대조 7쌍에서 경보는 각각 3건이었다. 024의 분기 방문 10·20·40회 예산에서 정기/신호 후 발견은 7/11 대 0/11, 11/11 대 8/11, 11/11 대 11/11이었다. 028의 유지층 실행 확인은 32셀이다. 최적 재확인 주기는 정해지지 않았다. [누적 근거][prev] |
| 옛 링크·사용판 복원 · 023·027·032·036·039·043·047 | 023은 주소·이유에서 출발할 때 3/18, 판·근거 추가 5/18, 변경 관계와 시점까지 추가 15/18의 목적지를 찾았다. 032는 12참조가 모두 HTTP 200이어도 교체 사유를 찾았다. 039에서 옛 발췌는 12/12 재표시됐다. 043의 정정 우선 4건에서 옛 판 대조는 기본 2/4에서 판 주소 추가 4/4로 늘었다. | 027·032에서 상류 시행일과 소비 배포일의 연결은 0/12·0/6이다. 036은 이력 유무 모두 유지 11·교체 1이었고 요청 절약은 모의값이었다. 039의 두 시점 복원은 C1 0/12·C2 1/12였다. 043 자연 소비자의 과거 사용판은 0/4, 047의 외부 입력 연결은 소비자 우선 0/6·실행 기록 우선 1/2, 선정 필드 독립 확인은 두 층 모두 0건이었다. [누적 근거][prev] |
| 대표 링크와 보완 절 · 031·040·044·048 | 031은 3추천을 36입력에서 재생해 기대표 6행을 고쳤다. 040의 URL·상류·부품별 표시가 보존한 필수조건은 8·6·8개였다. 044 보강 4건의 완전 대안 수는 각각 2·11·1·0개였다. 048의 Matplotlib 두 목록에서는 주소가 달라도 다섯 표시 필드가 같은 링크가 실제로 묶였다. | 044의 두 클릭 13/14는 대안별 가능한 경로를 합한 수다. 048은 원목록과 게시 바이트를 확보한 풀이 2/9였고 두 풀 모두 후보가 3개뿐이었다. 한 요구에서는 URL별 표시만 두 번째 원문에서 추가 구현에 닿았다. 후순위 구현 승격과 실제 독자의 선택 효과는 남았다. [누적 근거][prev] |

### 새 증거가 바꾼 판단

**049 · “가운데”가 어떤 좌표의 가운데인지가 출력 차이를 설명한다.** M03에서 Linux/Agg Matplotlib 3.0.2로 색 막대 축 좌표에 글자를 두면 두 배율 모두 (0.5, 0.5)였다. 데이터 좌표를 쓰면 배율 .01에서 (0.505051, 0.505051), .001에서 (5.050505, 5.050505)가 되고 레이아웃 예외가 반복됐다. 2.2.2에서는 두 조작 모두 가운데이고 배율별 A/B PNG가 같았다. 주실행 20행은 PNG 18·예외 2, 판 감도 4행은 PNG 4, 목적 감도 4행은 PNG 3·예외 1이다. 같은 호스트의 두 설치에서 주실행 9쌍의 PNG 바이트와 RGB, 나머지 한 쌍의 예외가 일치했다. 지난 045에서 없던 **수신 프로그램의 예측 검증**이 생겼다. [실행 28행][runs49] · [재실행 10쌍][pairs49]

M02에서 범례 10개는 두 조작 모두 읽혔다. 30개일 때 범례를 배치 계산에서 빼면 데이터 축 크기는 유지됐지만 읽힌 이름은 12개였고, 포함하면 11개였다. 축 크기를 보존하려는 사람과 모든 계열을 식별하려는 독자는 다른 조작을 고를 수 있다. 인쇄와 지도 원리가 같은 조작을 권한 사례이며 당시 API 설명만으로도 그 조작을 찾을 수 있었다. 원작성자의 첨부 둘·Windows/TkAgg 당시 결과·Adobe CS6 지정 두 쪽·예외 후 픽셀은 미확인이다. 049로 인쇄·지도 링크의 독자적 효용이나 역사적 채택을 단정할 근거는 생기지 않았다. [PNG 판독][pix49] · [조건별 반환 카드][cards49]

**050 · 공개 표가 충분한 분모를 갖췄는지부터 판정해야 한다.** 고정 소프트웨어 6군과 다른 분야 2군의 연결 계약 16행·종점 26행에서 배정·시간·최종품질을 같은 시행의 원자료로 잇고 새 비교가 가능한 군은 소프트웨어 0/6, 전체 0/8이었다. NCQ 두 실험의 코드 조각 142·156행은 각각 사람×시행 표지 20그룹까지 묶이지만 조건 대응표·시각·최종검사가 없다. CodeMend 361행은 검색 질의 평가표였고, Strata의 6/6 연결은 조건×과제 집계다. 사람 원자료의 부분 대장을 얻은 연구는 NCQ 한 군이다. 저자 자료 4건과 별도 과제·구현 3건이 부족해 25저작을 읽고도 지정 배당은 17/24에 머물렀다. [연결 원장][join50] · [종점 원장][end50] · [자료 배당][sources50]

eXoaDocs의 네 과제 전체 통과는 개입 3/12·대조 1/12, 과제 3만 보면 3/12·4/12였다. Blueprint에서 20명 모두 붙여넣었지만 3명은 제한시간 안에 완료하지 못했다. 시간표와 품질표의 순위를 맞춰 같은 사람으로 만들면 이 차이를 숨긴다. Strata의 precision은 표 90.1%·그림 91.0%, Chan은 본문 153명·표 합 151명으로 이견이 남았다. 021의 판독 향상이나 NCQ의 선택시간 단축은 여전히 각 종점에서 쓸 근거다. 동등 품질의 총시간·후속 재작업에 대해서는 효과의 방향도 미확인이다. [반례 원장][cross50] · [050 결과][r50]

**051 · 어떤 파일이 있었다는 증거로 어느 필드를 썼는지 판정하면 오판이 생긴다.** 통계와 정적 교통 자료에서 사전 정답 16실행×3기록×4사실을 대조했다. 네 사실은 대상 경로 열기, 특정 행·필드 조회, 지정한 변경에 따른 보고값 변화, 발행 파일과의 바이트 일치다. 주소·목적(P0)은 64/64 보류, 판·해시를 더한 P1은 바이트 일치 여부 16/64 판정·48보류, 경로·필드·변환을 기록한 P2는 64/64 정답과 일치했다. 주소만으로 모두 긍정하면 거짓 양성 28, 해시를 사용의 증거로 삼으면 거짓 양성 16·거짓 음성 4였다. P2도 사용 목록을 누락하고 수집 범위를 완전하다고 표시하자 거짓 음성 3건이 나왔다. 주실행·짝 변형·감도를 합한 재실행은 시각을 제외해 59/59, 파생 원장 5개는 바이트가 일치했다. [192판정][dec51] · [누락 대조][sens51] · [재실행][repeat51]

NYC 두 공식판에서 같은 3월 19일의 두 필드 합은 1300→1331이었지만 이 과제의 반올림 보고값은 모두 1300이었다. 교통 예제도 방향을 바꾸면 trip ID 두 개가 모두 달라지면서 개수는 2로 같았다. 반면 2016·2026 저장소판에는 같은 예제 ZIP이 재수록돼 있었다. 같은 서비스일에 적용되는 운영자의 서로 다른 원 배포판, 제3자의 실제 사용판, 캐시·다른 프로세스의 읽기는 관측 밖이다. P2의 추가 기록 비용도 직렬화 바이트까지 측정됐다. 이 실행은 047의 역사적 소비자가 어느 필드를 썼는지 소급해 주지 않는다. [판·집합 대조][contrast51] · [051 결과][r51]

**052 · 이번에 먼저 막힌 단계는 사용자의 표현을 후보 목록에 연결하는 일이었다.** 두 생태계에서 80개 이슈 본문을 선별해 Python 2·Markdown 2요구를 고정했다. 기능 명사와 발행 제목·공식 별칭이 맞은 자연 풀은 0/4였다. 보강 네 자리 중 bandersnatch 목록만 확보했고 독립적으로 고정된 사용자 목적 연결은 0/1이었다. 따라서 보강층의 목적별 완결률은 분모 0으로 해당 없음이다. 그 목록에서 URL별 A와 알려진 다섯 필드 기준 C는 원래 1·2·3번, 상류 프로젝트별 B는 1·5번을 대표로 보였다. 5번은 미러를 보완하는 S3였다. “다른 상류 URL이 노출됐다”는 주장은 지지되지만 “대체 구현을 찾았다”는 주장은 미확인이다. [8자리][slot52] · [요구별 변화][change52]

별도 Markdown 진단 50경로에서 B의 원래 6번은 명세였고 그룹→원래 4번 경로 하나는 첫 번째 필수조건(C1)만 새로 드러냈다. A/B/C 모두 두 조건을 한 경로에서 완결한 구현은 0이었다. 네 번째 직접 자리를 주면 A/C도 C1을 드러냈다. 엄격 C에 필요한 판·문서 역할이 없어 병합 기회는 미관측이다. 목록을 본 뒤 기능 절과 소속 범주의 정의를 고쳤고, 라우팅에 쓴 README는 진단의 첫 목적지로 먼저 노출됐다. 후기의 다른 PyPI 스냅샷으로 최초 창을 보충할 수도 없었다. 원장 177행에는 빈 상태 21행이 있다. 이것은 열람 가능한 경로의 재구성이며 사람의 채택·설치 시험은 미실시다. [경로 원장][path52] · [정정 이력][cor52] · [052 결과][r52]

### 다음 네 작업으로 가를 결정

| 독립 작업 | 이번에 새로 요구하는 증거 | 탐색기에서 달라질 판단 |
| --- | --- | --- |
| 053 · 다른 분야 원전의 추가 설명력 · web-pro | 새 그림·자막 요구에서 같은 API 절에 분야 안 예제 또는 타 분야 원전을 붙인다. 읽는 분량을 맞추고 후속 출력 전에 예측을 고정한다. | 원리 링크를 특정 조작의 근거로 돌려줄 경우와, 보존할 목표를 묻는 참고 자료로 둘 경우를 가른다. |
| 054 · 사람 과제의 시간·품질 공동 판정 · web-pro | 050의 두 고정 사례와 새 공개 실험 자료에서 제한시간 내 정확한 완료의 실제 결합행, 또는 같은 배정군의 주변 개수로 가능한 최솟값·최댓값을 구한다. | 직접 계산·구간만 식별·판정 불가 중 어디까지 제품 효과 설명에 허용할지 정한다. |
| 055 · 운영 자료 개정 후에도 유효한 이유 · codex-cloud | 실제 교통 시간표와 IANA 시간대의 연속 발행판에서 같은 기준일·질문으로 재계산한다. 운영자 원본 미확보, 같은 숫자·다른 구성도 표에 남긴다. | 오늘 다시 답하는 데 필요한 기록과 예전 판을 재현하는 데 필요한 기록의 취득 비용을 비교한다. |
| 056 · 사용자 용어와 목록의 기능명 · web-pro | JSON Schema와 JSON-LD의 공개 요구를 원문 제목 매칭·사전에 고정한 표준 용어 대응으로 각각 같은 목록에서 찾아, 같은 판의 두 필수조건이 실제 구현에서 확인되는지 비교한다. | 세 자리를 어떻게 묶을지 결정하기 전에 어느 입력 표현으로 유용한 부품이 후보 집합에 들어오는지 가른다. |

H1(요구와 근거 절의 연결이 판단을 돕는가)과 H2(추천 이유를 보관·재확인하면 옛 판단을 바로잡는가)는 계속 별도로 판단한다. 새로 찾기(C0), 주소·판·용도 보관(C1), 발췌·판정 이력 추가(C2)는 나중 설계자가 비교할 대안이다. 네 작업의 입력은 각각 이미 끝난 작업 한 건에 고정했다. 이 차수는 특정 DB·크롤러·표시 방식이나 사용자 노동 절감 수치를 확정하지 않는다. [작업별 전체 지시문][next]

[product]: https://github.com/laadkke-arch/agentflow-open/blob/d7e60daf1b5b2c918502c407982566369b7149e3/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/d7e60daf1b5b2c918502c407982566369b7149e3/docs/RESEARCH_WORKFLOW.md
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/ef8ecd3eb6ae1b7718a288c13721c06b231f2a96/docs/workstreams/planning/REVIEW-12.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/d8c8d029bfb6107520ae74d2a172b2b18840e764/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/d7e60daf1b5b2c918502c407982566369b7149e3/docs/automation/dot-control.json
[next]: NEXT_TASKS-13.json
[h49]: https://github.com/laadkke-arch/agentflow-open/blob/ae40dc268bca0774ee8e5d8326cfb8aa8101b87b/docs/workstreams/research/AF-RES-049/HANDOFF.md
[r49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/RESULT.md
[a49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/evidence/acceptance-evidence.json
[runs49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/runs.csv
[pairs49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/evidence/replay-pairs.json
[pix49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/evidence/png-readback.csv
[cards49]: https://github.com/laadkke-arch/agentflow-open/blob/ab50b40bd12109fb13c29f2f0256e6654ae81c47/docs/workstreams/research/AF-RES-049/cards.md
[h50]: https://github.com/laadkke-arch/agentflow-open/blob/a3e13076e889dd49bfa7b7aa2fad6d149d874452/docs/workstreams/research/AF-RES-050/HANDOFF.md
[r50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/RESULT.md
[a50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/evidence/acceptance-evidence.json
[join50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/joins.csv
[end50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/outcomes.csv
[sources50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/evidence/source-counts.json
[cross50]: https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/counterexamples.md
[h51]: https://github.com/laadkke-arch/agentflow-open/blob/537712e2f716a0ff9b517b23ac7c4ec2fb37435d/docs/workstreams/research/AF-RES-051/HANDOFF.md
[r51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/RESULT.md
[a51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/evidence/acceptance-evidence.json
[dec51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/decisions.csv
[contrast51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/evidence/contrasts.md
[sens51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/evidence/receipt-sensitivity.json
[repeat51]: https://github.com/laadkke-arch/agentflow-open/blob/4e1a76cd0ca25bfe616797b623f9ecb435261fcb/docs/workstreams/research/AF-RES-051/evidence/repeat-check.json
[h52]: https://github.com/laadkke-arch/agentflow-open/blob/6e6818e345ff8ab9beffd0ea0e1cee9fd6f4ae01/docs/workstreams/research/AF-RES-052/HANDOFF.md
[r52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/RESULT.md
[a52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/evidence/acceptance-evidence.json
[slot52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/slots.csv
[change52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/changes.csv
[path52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/paths.csv
[cor52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/CORRECTIONS.md
[s52]: https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/evidence/source-counts.json
[ver51]: https://github.com/laadkke-arch/agentflow-open/blob/9ba0e376838cb9b505cc5d31d912d462cbfc5e11/docs/workstreams/research/AF-RES-051/evidence/final-check.json
