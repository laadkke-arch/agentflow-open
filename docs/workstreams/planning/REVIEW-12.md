# REVIEW 12 · 원문 링크가 실제 선택과 결과를 어디까지 설명하는가

이 탐색기는 설계 중인 소프트웨어의 전체나 일부, 그리고 그 목적을 입력받아 설계자가 참고할 제품·부품·다른 분야의 원리를 원문 링크와 함께 돌려주려는 연구다. 지금까지 근거가 가장 분명한 용도는 **어느 요구를 어느 절에서 확인할 수 있고, 적용하면 무엇이 달라지는지 알려 주는 것**이다. 설계자가 링크 덕분에 더 나은 안을 처음 발견했는지, 결과 품질을 유지하며 재작업을 줄였는지는 여전히 미확인이다. [제품 브리프][product] · [누적 검토 11][r11]

H1은 요구와 근거 절을 연결한 설명이 후보 판단을 돕는다는 가설이다. H2는 추천 이유를 기록하고 다시 확인하면 옛 판단을 바로잡을 수 있다는 가설이다. 이번 네 작업에서 조언 뒤 실제 코드 수정, 과거 실행에 투입된 외부 파일, 표시 방식 때문에 가려진 두 번째 원문을 각각 확인했다. 셋은 서로 다른 질문에 답한다. C0(필요할 때 새로 탐색), C1(주소·판·용도 보관), C2(발췌·판정 이력까지 보관)는 계속 비교할 대안이다. 입력 계약, 검색기, 제품 DB, 수집 주기와 반환 형식은 열려 있다. [046 사건][cases46] · [047 구성별 판독][read47] · [048 경로별 변화][change48] · [연구 운영 규칙][workflow]

## 이번 검토에서 인수한 범위

`work/planning@dbb279d`의 최신 REVIEW-11을 먼저 읽고, 당시 통합 진행표 `1f722bf`와 이번 `d8c8d02`를 작업 ID별로 대조했다. **등록 42→46, DONE 40→44, BLOCKED 2→2. 새 DONE은 045·046·047·048뿐이다.** 네 작업의 진행표 결과 SHA는 각각 작업 브랜치 끝과 같았다. 네 끝 커밋 모두 HANDOFF 한 파일만 담았고, 각 인계의 고정 본문 SHA에서 다시 읽은 RESULT는 끝 커밋의 RESULT와 일치했다. 이전 작업의 결과 파일을 다시 연 예외는 034의 `effects.csv` 한 건이다. REVIEW-11에는 050이 이어받을 사람 실험의 개별 연구 ID와 시간·품질 표 연결 한계가 없어 그 행만 식별했다. [이전 진행표][oldreg] · [현재 진행표][reg] · [034 비교 원장][old34]

| 새 DONE | 인계 커밋 / 고정 본문 | 작업자가 직접 읽어 산입한 고유 원문 | 수용 파일을 다시 센 상태 |
| --- | --- | ---: | --- |
| 045 · 분야 간 원리의 예측 | [7649739][h45] / [29c5da5][r45] | 30저작 | 28항목 중 충족 22, 미충족 6. 인계서는 연구 근거 부분을 BLOCKED로 표기했다. [수용 원장][a45] |
| 046 · 공개 리뷰 링크와 작성자 수정 | [4003022][h46] / [d8a2c69][r46] | 54저작 | 30항목 중 충족 18, 공개 미러 기준 충족 1, 부분 3, 미충족 8. [수용 원장][a46] |
| 047 · 발행판·실행 입력·보고값 | [a6ef2b0][h47] / [235724a][r47] | 31저작, 필수 역할에 27 배당 | 고정 시점 55항목 중 충족 31, 관측 15, 부분 2, 미충족 4, 해당 없음 1, 후속 절차 대기 2. 두 대기는 이후 원격 재열람 영수증과 단독 인계 커밋에서 확인했다. [수용 원장][a47] · [후속 영수증][receipt47] |
| 048 · 링크를 묶은 뒤의 도착 절 | [132e010][h48] / [a690049][r48] | 33저작 | 38항목 중 충족 28, 미충족 10. 9개 후보 풀 중 2개에 원래 순서와 게시 바이트가 있다. [수용 원장][a48] |

중앙 진행표에서 DONE 44건의 `acceptance_evidence`는 모두 빈 배열이고 새 네 건의 `source_commit`·`actual_model`은 비어 있다. 위 표의 충족 범위는 각 작업의 파일에서 확인했다. 018은 세 번째 시도의 대화 길이 한도, 035는 첫 시도의 사이버 보안 위험 가능성 표시로 차단됐으며 두 건 모두 공식 인계·결과 SHA가 없다. 아래 수치는 보관된 행과 영수증을 대조한 것이다. 과거의 외부 자료 열람·실험 실행은 각 작업자가 기록한 범위까지 인용한다. [현재 진행표][reg]

## 044까지 이어받는 판단

| 질문과 작업 | 실제 확인된 범위 | 어긋난 결과와 적용 한계 |
| --- | --- | --- |
| 부분 설계를 어떻게 받고 전달하는가 · DOT-001·002, RES-001~004·016·020 | 전달·복원을 시험했다. 합성 입력 6건에서 부정 조건이 빠졌고, 2문제·17질의에서는 같은 이름의 제품과 부분 기능이 뒤섞였다. 003·004는 주소·대상·목적의 식별을 나누고 합성 18행을 판독했다. 020은 73개 주장 중 72개의 전달을 확인했다. | 실제 사용자의 원뜻 보존율은 미확인이다. 016 내부 판독의 일치는 후보 형태 78.3%, 기여 70.8%였다. 020은 충돌 16건 중 2건만 완전히 해소했다. [이전 검토][r11] |
| 검색이 다른 분야의 쓸 만한 부분까지 찾는가 · 009~014·025·029·033 | 35개 비교 시스템에서 기능이 겹쳤다. 분야 단서를 준 010은 24원문에서 원리 7군을 찾았다. 011은 실제 61스레드·635답을 읽었고 부분 질문 33건 중 10건에서 진전을 찾았다. 013의 역사적 선례 176건에서 웹 검색이 회수한 것은 16건, 목록은 5건이었다. | 011의 전이 답 14개에는 질문자 반응이 없었다. 012의 합성 질의에서 증가한 근접 오답은 014의 485자료에서 재현되지 않았다. 025의 72칸은 지지 2·충돌 14·보류 53·빈칸 3. 029에서 공통 검색·추가 웹 검색·제공자 내부 탐색의 부분 요구 인용 완결은 2/12·4/12·3/12였고 전체 요구는 모두 0/12였다. 033에서 8설계×18후보의 엄격 지지는 넓게 봐도 1/144, 당시판 기준은 0, 실제 상위 세 자리 완결은 두 검색 모두 0/8이었다. [누적 검토][r11] · [033 반환창][old33] |
| 뒤늦은 발견이 설계를 바꿨는가 · 017·022·037·041 | 017은 40사건 중 18건에서 두 날짜를 연결했다. 022에서는 이미 알던 대안의 조건을 바로잡아 시행한 사례가 결정 우선 24건 중 2건이었다. 037은 같은 목적의 후속 명세·코드·시험을 7/8과 출처 노출층 3/4에서 확인했다. 041의 pdfTeX·LilyPond 두 사례에서 저자의 포괄적 출처 명명과 같은 기능 반영을 확인했다. | 017의 당시 탐색 가능성 확인은 0건. 022의 미인지→당시 가용→변경→시행은 주표본 0/24, 발견 진술 우선층 1/9였고 33건 모두 노동 절감은 미확인이었다. 037의 최초안 변경 인과는 두 층 모두 0건이다. 041은 037과 겹치는 두 사례다. 활자 폭·줄바꿈 생각이 초기안에 있었고, 악보 본보기 주석과 기호 함수의 변경에는 읽은 악보 판·쪽이 빠졌다. 엄격 인과는 최초안·기존 코드 기준 모두 0/2였다. [037 사건 판정][old37] · [041 원전 판정][old41] |
| 링크 설명이 사람의 작업을 얼마나 돕는가 · 021·026·030·034·038·042 | 021에서 두 절을 열었을 때 주소만 6/23, 절 목록 9/23, 요구와 절 연결 13/23이 완결됐다. 030의 같은 변수 질문에 직접 답한 수는 최초 표본 3/24와 보강 6/8이었다. 038은 네 과제의 링크·루브릭을 통제했다. 042는 pandas 1.4.4 날짜 18행·1.5.2 정수 25행을 재실행해 43/43 일치를 확인했고, 이 중 의도한 근접 오답 5개를 구별했다. | 잘못 연결한 021은 8/23이었다. 026의 실제 질문 전송은 0, 030의 같은 답변자 권고 변경과 요청자 신규 시행까지 간 사례는 0/3·0/6이었다. 034의 사람 연구 22군·26실험 중 NCQ에서 패키지 선택은 중앙값 380→57초, 같은 실험의 전체 과제는 849→847초였다. 038 사람 참가자는 0명이다. 042의 값·형·예외 재현은 해당 두 과제·판의 근거다. [이전 검토][r11] · [034 종점][old34] · [042 실행][old42] |
| 추천 이유는 언제 낡고 재확인은 어느 정도 필요한가 · 015·019·024·028 | 015에서 500추천 중 현재 판정 가능한 195개에 붕괴 14개, 과거 복원 83개에 후발 붕괴 5·최초 오류 4가 있었다. 024는 64이유×16분기에서 유지 897·무효 95·최초 오류 16·보류 16을 분류했다. 분기 20회 방문 예산에서 정기 확인은 무효 이유 11/11, 신호 뒤 확인은 8/11을 찾았다. | 019의 사건/대조 7쌍에서 경보는 양쪽 3건씩이었다. 024의 10회 예산은 7/11 대 0/11, 40회는 모두 11/11이다. 028이 실행 검증한 유지층은 32셀로 나머지 865셀의 동작은 미확인이다. 비용과 탐지 범위는 이유·예산에 따라 달랐다. [누적 검토][r11] |
| 옛 추천을 되찾아 지금 다시 쓸 수 있는가 · 023·027·032·036·039·043 | 023에서 주소·이유만으로 목적지를 찾은 사건은 3/18, 판·근거 추가 5/18, 변경 관계·시점까지 추가 15/18이었다. 032의 12참조가 모두 HTTP 200이어도 교체할 근거가 있었다. 039에서 옛 발췌는 12/12 재표시됐다. 043 정정 우선 4건의 옛 발행판 대조는 기본/판 주소 추가/발췌 추가/둘 다의 순서로 2/4·4/4·2/4·4/4였다. | 023의 자동 복원은 0/18이고 027·032의 상류 시행과 소비 배포 두 날짜 연결도 0/12·0/6이었다. 036은 이력이 있거나 없어도 유지 11·교체 1, GET 29→17은 모의값이었다. 039의 두 시점 발췌 복원은 C1 0/12, C2 1/12, 요청 실패 88/94 중 80회가 CONNECT였다. 043 자연 소비자의 실제 과거 사용판 기준은 0/4였다. 정정 우선층의 현재 판정은 3/4·4/4·2/4·3/4로, 발췌 추가의 이득은 과업에 따라 달랐다. [039 짝 비교][old39] · [043 판독][old43] |
| 같은 프로젝트의 링크를 묶으면 무엇을 잃는가 · 031·040·044 | 031은 알려진 추천 3개를 36개 계약 입력에 재생했고 기대표 6행을 고쳤다. 040에서 URL·상류·부품별 표시가 보존한 필수조건은 8·6·8개였다. 044 보강 4건의 완전 대안은 2·11·1·0개였다. 세 방식 모두 직접 12/14, 대안별 두 클릭 경로 존재 13/14였으나 상류 묶음이 Requests를 올린 경우와 보완 절을 밀어낸 경우가 따로 있었다. | 031의 대형 입력 종단·실제 프런트엔드 자동 전달, 040의 완전 대안 복원은 미확인이었다. 044 자연층은 Pandoc 원응답 4건 결측, Vega-Lite의 4개 관측 풀에는 완전 대안 0개, 최초 토큰 규칙까지 준수한 자연 요구는 3/8이었다. A(정확 URL)와 C(다섯 표시 필드)가 만든 그룹은 관측 8풀에서 같았다. 13/14는 대안별로 가능한 경로의 합집합이다. 한 독자가 두 번 열어 본 대안 수나 채택률은 미측정이다. [040 손실][old40] · [044 요구별 차이][old44] |

## 새 DONE 네 건의 근거와 남은 구멍

### 045 · 두 원리가 다른 말을 한 것과 실제 출력이 둘을 가른 것

6요구×2후보의 예측과 후속 원장 12행을 맞췄다. 봉인 때 두 후보의 관계는 다름 3, 같음 2, 판별불가 1이었다. 후속 12행의 판정은 미확인 7, 판별불가 5였다. 최초 본문의 불변판은 0/6이었다. 결과를 본 뒤 더 엄격하게 만든 ‘정상·경계 모두에서 두 조작을 완결 비교’의 적격 분모는 **0**으로 성공률은 해당 없음이다. 사전 문구를 관대하게 읽으면 M01 한 건이 적격이고, 입력 일치까지 완화하면 M01·M03 두 건이다. 어느 기준에서도 한 원리만 지지하는 사례는 없었다. [후속 12행][out45] · [분모 수정 이력][amend45]

M03에서 페이지 가운데를 고정하는 조작은 작성자가 수락했다. factor .01과 .001에서 실제 colorbar 범위·글자 좌표가 어땠는지는 기록되지 않았고, 인접 PR 시험은 별도의 None 예외를 다뤘다. M02는 두 원리가 모두 범례를 배치 계산에서 빼는 쪽을 허용했다. Audacity AUD01에서 실제로 반영된 구현은 사전 두 안 밖의 세 번째 getter였다. AUD03에서는 당시 코드가 해당 기능을 비활성화한 줄을 봉인 전에 놓쳤다. 5-bin 산술값으로 실제 오디오 출력을 입증할 수 없다. 이 자료로 반환할 수 있는 것은 “어느 양을 고정하려는가”를 묻는 진단 링크와 조건이다. [045 결과][r45] · [미실행 Matplotlib 절차][probe45]

### 046 · 링크 뒤의 코드 수정과 링크 때문에 한 코드 수정

두 저장소·기간의 생성순 160개에서 자연 8자리, 링크 우선 4자리를 보존했다. 자연층에 적격 리뷰어 링크는 0/8이었다. 링크 우선층에서 내용에 관여한 답은 2/4, 제안에 응답한 답은 3/4, 명시적 읽음·최초 발견은 각각 0/4였다. 같은 작성자·같은 목적의 수정은 **2/4**이고, 다른 작성자까지 허용하면 4/4였다. 첫 링크→그 자료를 변경 이유로 든 작성자→같은 사람의 패치→해당 시험/반영을 모두 이은 사례는 **0/4**다. 12자리 모두 직접 노동 로그, 주 관측 기간 안의 원 작성자 소요시간 진술, 동등 품질 시간쌍이 없었다. [사례 원장][cases46] · [노동 원장][labor46]

L-S2는 링크 전부터 실패가 있었고 작성자가 별도로 호출부 타입 계약을 이유로 들었다. 두 번째 링크에는 더 강한 부분 연결이 있었다. L-P2는 앞서 작성된 로직을 링크 뒤에 통합한 경우다. 첫 부모 대비 실제 변경을 확인해 최종 2/4에 넣었다. 기존 로직의 통합을 양성에서 빼면 1/4이고 선행 착수한 해당 슬롯을 분모에서도 빼면 1/3이다. 지도의 편집자는 필드를 고친 **26초 뒤**에 규칙 링크를 남겼다. 음악 사례는 포럼 보고만 열리고 개별 편집·적용판은 열리지 않았다. 최초 PR판 복원은 공개 미러 기준 12/12였고 원 이벤트 파일과의 독립 대조는 0/12였다. [판정 정정][rev46] · [시간·행위자 감도와 분야 대조][r46]

### 047 · 발행자가 보존한 판, 실행이 읽은 파일, 분석이 보고한 값

8사례×3구성의 판독 24행을 다시 셌다. 소비자 우선 6건에서 **구별되는 발행판 4, 특정판·파일 사용 선언 1, 원 실행의 외부 입력 연결 0, 선정 필드 독립 확인 0**이었다. 실행 기록 우선 2건은 같은 순서로 **2·1·1·0**, 보관된 로컬 입력까지의 실행 연결은 2/2였다. 외부 입력이 확인된 사례에서 필드 확인은 보강층 0/1이고 자연층은 해당 없음이다. 기본 주소에 발행 증거를 더하자 6개 판이 구별됐고 실행·소비 기록까지 더하자 저자의 선언 2건과 원 실행의 외부 입력 1건이 보였다. 이 비교는 각 기록 묶음이 담은 정보에 대한 감사다. [구성별 판독 24행][read47] · [실행 기록][runs47]

RUN02에서 전체 파일의 체크섬과 해제된 내용을 대조한 후 입력 판정이 0→1로 바뀌었다. 보고 필드는 기존 파생 출력에서 다시 읽었으므로 독립 검증은 미확인이다. RJ02에서는 저자가 남긴 16파일 명세가 대상 판을 좁혔다. R의 두 연속판은 동일한 iris 자료와 자유도 2를 주어 그 값으로 사용판을 식별할 수 없었다. 40개 정보 제거 행 중 17개에서 근거로 서술할 수 있는 상태가 바뀌었다. 이미 결측이던 6행에는 새 손실이 없었다. 선정한 주 결과의 정확값 두 건, 정정 전후 메타데이터만 달랐음을 입증할 원본 쌍, 같은 바이트를 보관했지만 특정 실행에서 안 썼다는 직접 음성례는 남았다. 일부 선정 해석은 사후 수정됐으므로 최초 6+2의 보존율로 일반화하기 어렵다. [047 결과][r47] · [정보 제거 40행][sensitivity47] · [반례 원장][counter47]

### 048 · 그룹이 줄어도 새 구현이 보이지 않은 이유

9풀×6자리에서 관측 6, 실제 목록 소진 6, 접근 결측 42자리였다. 다섯 자연 요구와 PyPA 보강 두 곳의 원응답은 확보하지 못했다. 공식 발행 저장소에서 고정한 Matplotlib 3.11.2 두 풀에 각각 후보가 세 개 있었다. 정확 URL A는 풀마다 3그룹, 상류 B는 1그룹, 다섯 필드 C는 2그룹이었다. **C가 서로 다른 URL을 합친 풀은 2/2**, 배열이 바뀐 풀도 2/2였지만 새 대표 URL은 0/2였다. 원래 네 번째 후보가 없었으므로 다른 구현을 앞자리로 올리는 효과는 이 두 풀에서 판단할 수 없다. [048 결과][r48] · [풀·표시 방식별 27행][change48]

M1의 원풀에서 완결된 구현 하나는 A/B/C 모두 직접 읽거나 두 동작으로 확인할 수 있었다. A의 T011에서만 두 번째 원문을 통해 풀 밖의 TightLayoutEngine까지 같은 시행에서 확인했다. B/C의 대표에서 같은 문서로 가는 경로는 동작 예산을 넘었다. M2는 원풀에 완결 구현이 0개였고 standalone 설명은 형제 목록을 열어야 보였다. 저장 재생은 **고유 경로 40개 중 완결 37·부분 3**, 방식별 적용 70회였다. 원 게시 주소에서 별도로 시도한 라이브 경로 2건의 도착은 0건이다. 사후에 더 읽은 40문서·372절에서는 새 URL이 앞에 온 절 6곳, 다른 상류의 완전 구현 회복을 확인한 절 0곳이었다. 새 URL, 두 번의 저장 재생, 사람이 실제로 선택한 링크는 각각 다른 관측 단위다. [경로별 원장][trials48] · [사후 40문서][diag48]

## 어긋나는 결론을 가를 다음 작업

| 남은 판단 | 독립 작업과 새로 얻을 증거 | 이 자료로 바꿀 수 있는 결정 |
| --- | --- | --- |
| 010·041은 영감의 출처, 045는 사전 예측을 보여줬다. M03의 같은 입력에 대한 실측이 비었다. M02처럼 두 원리가 같은 조작을 권하는 경우도 있다. | **049 · codex-cloud** — 3.0.2에서 M03의 두 factor와 M02의 10·30 범례를 실제 렌더링하고 빈 환경에서 반복한다. 판·목적을 바꾼 감도도 별도로 둔다. | 추천 카드가 특정 조작의 출력을 예측할 수 있는지, 목적을 명시한 원문 참고까지만 허용할지 판단한다. 새 실행이 채울 수 있는 것은 조작의 결과다. |
| 021의 절 연결은 판독을 도왔지만, 034의 선택·전체 시간은 다른 방향의 해석을 낳았고 046의 수정에는 사람 시간이 없었다. | **050 · web-pro** — 공개 실험 6군과 다른 분야 2군의 원자료에서 연구 배정·사람·과제·시간·품질 키를 잇는다. 두 조건의 비교가 불가능한 이유도 결과다. | 동등 품질의 완료, 부분 과제 시간, 결과물 재작업 중 어떤 문장을 사용 근거로 제시할 수 있는지 정한다. |
| 043은 옛 발행판으로 가는 주소의 이득을, 047은 실제 외부 입력 한 건을 확인했다. 사용할 수 있었던 파일과 결과값에 기여한 필드 사이가 비어 있다. | **051 · codex-cloud** — 공식 통계·정적 교통 표로 실행 16자리를 만든다. 같은 바이트의 미사용 파일, 헤더만 읽은 파일, 읽어도 최종값이 같은 조건을 비교한다. | 주소·판·해시 또는 행·변환 영수증이 필요한 질문을 골라낸다. 통제 실행 결과로 역사적 사용자 행동을 소급하지 않는다. |
| 044의 요구별 득실은 반대 방향이었고 048은 실제 병합을 찾았지만 세 자리를 다 채운 뒤에 남은 독립 후보가 없었다. | **052 · web-pro** — 공개 패키징·문서 변환 목록에서 자연 요구 4자리와 네 번째 후보가 있는 보강 4자리를 나누어, 세 대표·두 번 열람으로 읽히는 원문과 구현을 비교한다. | 독립 구현이 올라온 경우, 필요한 절을 숨긴 경우, 대표만으로 충분한 경우의 반환 조건을 구별한다. |

네 작업의 표본과 입력은 과거의 고정 커밋만 참조한다. 각 작업자는 필수 표·원문 기록·반례를 자기 경로에 남긴다. 사람의 장기 노동 절감, 실제 검색 회수율, 제품 전체의 최적 저장·표시 방식은 이 차수의 개별 관측만으로 정하기 어렵다. [다음 작업 네 건](NEXT_TASKS-12.json)

[product]: https://github.com/laadkke-arch/agentflow-open/blob/d8c8d029bfb6107520ae74d2a172b2b18840e764/docs/product/RESEARCH_BRIEF.md
[r11]: https://github.com/laadkke-arch/agentflow-open/blob/dbb279dd8e298fdfc2ca822eeddad7a17a78f281/docs/workstreams/planning/REVIEW-11.md
[cases46]: https://github.com/laadkke-arch/agentflow-open/blob/d8a2c696046e28adb68cdfb75d4104454e48dd52/docs/workstreams/research/AF-RES-046/cases.json
[read47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/readings.csv
[change48]: https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/changes.csv
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/d8c8d029bfb6107520ae74d2a172b2b18840e764/docs/RESEARCH_WORKFLOW.md
[oldreg]: https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/automation/dot-control.json
[reg]: https://github.com/laadkke-arch/agentflow-open/blob/d8c8d029bfb6107520ae74d2a172b2b18840e764/docs/automation/dot-control.json
[old34]: https://github.com/laadkke-arch/agentflow-open/blob/f6dc9b8873b049f1eb4f8977ce3408ed057df1f7/docs/workstreams/research/AF-RES-034/effects.csv
[h45]: https://github.com/laadkke-arch/agentflow-open/blob/7649739855299e7c054286d5d5126a76c701fd01/docs/workstreams/research/AF-RES-045/HANDOFF.md
[r45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/RESULT.md
[a45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/evidence/acceptance-evidence.json
[h46]: https://github.com/laadkke-arch/agentflow-open/blob/40030229bfa87f92f9875cdf5937fe382af8cb57/docs/workstreams/research/AF-RES-046/HANDOFF.md
[r46]: https://github.com/laadkke-arch/agentflow-open/blob/d8a2c696046e28adb68cdfb75d4104454e48dd52/docs/workstreams/research/AF-RES-046/RESULT.md
[a46]: https://github.com/laadkke-arch/agentflow-open/blob/d8a2c696046e28adb68cdfb75d4104454e48dd52/docs/workstreams/research/AF-RES-046/evidence/acceptance-evidence.json
[h47]: https://github.com/laadkke-arch/agentflow-open/blob/a6ef2b0bcb6412d9e6fa7a9eb59b5e863c621ff0/docs/workstreams/research/AF-RES-047/HANDOFF.md
[r47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/RESULT.md
[a47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/evidence/acceptance-evidence.json
[receipt47]: https://github.com/laadkke-arch/agentflow-open/blob/bbf9fad206acfcb45be4e65a5996c59a1eb8371c/docs/workstreams/research/AF-RES-047/evidence/finalization-evidence.json
[h48]: https://github.com/laadkke-arch/agentflow-open/blob/132e0108e652bdd2413edb71dfd6531507ea63e8/docs/workstreams/research/AF-RES-048/HANDOFF.md
[r48]: https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/RESULT.md
[a48]: https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/evidence/acceptance-evidence.json
[old33]: https://github.com/laadkke-arch/agentflow-open/blob/03ff2eb1264b85016266de1f36ddebe45f5fface/docs/workstreams/research/AF-RES-033/evidence/returned-window-audit.jsonl
[old37]: https://github.com/laadkke-arch/agentflow-open/blob/68c45d2fb4482850d6a3c29826c43a45ea1dc407/docs/workstreams/research/AF-RES-037/judgments.csv
[old41]: https://github.com/laadkke-arch/agentflow-open/blob/d610d7b16836c2cadff60edcd46cd394dc220ed6/docs/workstreams/research/AF-RES-041/judgments.csv
[old42]: https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/probe-results.csv
[old39]: https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/pairs.csv
[old43]: https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/judgments.csv
[old40]: https://github.com/laadkke-arch/agentflow-open/blob/9bff55706d5b1a939e39185bda9cf6f22bea246b/docs/workstreams/research/AF-RES-040/losses.csv
[old44]: https://github.com/laadkke-arch/agentflow-open/blob/176e2eee3c00257d7dcc64665c74b12bf4399913/docs/workstreams/research/AF-RES-044/changes.csv
[out45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/outcomes.csv
[amend45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/amendments.md
[probe45]: https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/evidence/reproduction/REPRODUCE.md
[labor46]: https://github.com/laadkke-arch/agentflow-open/blob/d8a2c696046e28adb68cdfb75d4104454e48dd52/docs/workstreams/research/AF-RES-046/labor.csv
[rev46]: https://github.com/laadkke-arch/agentflow-open/blob/d8a2c696046e28adb68cdfb75d4104454e48dd52/docs/workstreams/research/AF-RES-046/REVISIONS.md
[runs47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/runs.csv
[sensitivity47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/sensitivity.csv
[counter47]: https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/contradictions.md
[trials48]: https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/trials.csv
[diag48]: https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/evidence/post-seal-matplotlib-screen-40.json
