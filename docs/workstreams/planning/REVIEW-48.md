# REVIEW-48 · 어느 링크가 무엇을 입증하는가

부분 설계와 목적을 받은 탐색기는 개발자가 바로 읽을 절과 참고할 부품·원리를 돌려줘야 한다. 이번에 그 차이가 잘 드러난 두 사례가 있다. Godot 제안자는 가져오기 문서를 읽었다고 답했지만 여전히 원하는 저장 동작을 설명해 달라고 했다. 반면 같은 네 모서리 값을 받은 두 등고선 엔진은 실제로 서로 다른 변을 이었다. 앞 사례로는 **링크 열람 진술**, 뒤 사례로는 **특정 판과 입력에서의 반환 기하**까지 안내할 수 있다. 어느 쪽도 개발자의 총노동 절감을 측정하지 않았다. [제품 연구 브리프][product] · [Godot 사건][236chain] · [두 엔진 원표][239obs]

**요청 때 새 중앙 DONE은 AF-RES-230~237 여덟 건이며, 여덟 인계 모두 자체 PARTIAL이다.** 작성 중 중앙 DONE이 된 238~241도 별도로 검토했다. 총 12건의 자체 상태는 PARTIAL 9, DONE 2, REVIEW_READY 1이다. 238의 실제 카드가 비어 242는 계속 BLOCKED다. 다음 배정은 13건이다. 웹 조사·설계 8건은 서로 독립적으로 즉시 시작할 수 있고 재현·검산 4건도 자료가 준비됐다. 별도 웹 판독 1건은 새 작업 252의 실응답을 기다린다. [작업자별 지시문](NEXT_TASKS-48.json)

## 검토 범위와 비교 기준

계획 브랜치 `685311e`의 디렉터리에서 최신 파일이 REVIEW-47임을 확인해 먼저 읽었다. 그 문서가 인계한 결과 마감 `3057e4e`와 이번 요청판 `7369707`의 모든 작업 행을 ID와 필드값으로 대조했다. 기존 227행의 수정·삭제는 없고 230~242가 추가됐다. 완료된 229까지는 직전 검토의 판정·한계·근거 링크를 이어 썼다. 진행 중인 작업의 조사 대상은 중앙 배정문에서 확인했고, 결과는 중앙 DONE과 result_commit이 생긴 뒤 해당 브랜치의 owned_path에서 열었다. [직전 누적 검토][prev] · [47차 마감][old] · [48차 요청판][req] · [운영 규칙][workflow]

| 통합판 · 2026-11-24 UTC | 전체 행 | 중앙 DONE | RUNNING | BLOCKED | 이번 검토에서 원결과를 연 범위 |
| --- | ---: | ---: | ---: | ---: | --- |
| 22:47:37 · 3057e4e | 227 | 223 | 0 | 4 | 229까지 직전 검토 |
| 23:20:37 · 7369707 | 240 | 231 | 4 | 5 | 230~237의 인계와 결과. 238~241 진행 중, 242 대기 |
| 23:30:54 · 02ff9f0 | 240 | 234 | 1 | 5 | 238~240의 완료 인계를 추가로 읽음. 241 진행 중, 242 대기 |
| 23:43:17 · c02486b | 240 | 235 | 0 | 5 | 241 추가. 230~241까지 결과 반영, 다음 검토의 비교 기준 |

마감의 DONE 235건은 연구 233건과 연결 시험 2건이다. 235행 모두 중앙 acceptance_evidence는 빈 배열이며 개별 인계·결과가 관측의 출처다. 이전부터 보류인 018은 인계 전 대화 한도, 035는 실행 세션 종료 후 인계 미확인, 149는 같은 주간 세 경로의 모집 분모 결손, 151은 최초 응답·독립 판독·원사용자 비용 결손이다. 이번 242에는 별도의 자료 조건이 있다. 아래의 자체 상태와 집계는 중앙 상태의 의미를 좁혀 준다. [요청판][req] · [마감판][end] · [242에 필요한 카드 목록][238manifest]

| AF-RES · 대상 | 인계 자체 상태 | 고정 인계 / 직전 결과 | 원장 행 / 작업 내 산입 고유 저작 | 관측 또는 결측 단위 |
| --- | --- | --- | ---: | --- |
| 230 · 오디오 내보내기 | PARTIAL | [896b13e][230h] / [cb0cb98][230r] | 66 / 36 | 지명 4건·현행 본문 4, 최초 revision 0, 같은 작성자 후속 2 |
| 231 · 중복 표시와 첫 답 | PARTIAL | [e55fd8c][231h] / [b9a13af][231r] | 41 / 29 | 4개 본사건 미배정, 8경로·4쌍 실측 0 |
| 232 · 문단 조판 | PARTIAL | [430a1a5][232h] / [a88485d][232r] | 41 / 26 | 실재 WPT 2·추상 통제 4·분할 303행 |
| 233 · 도서관 저자 전거 | PARTIAL | [08685fe][233h] / [157d115][233r] | 52 / 25 | 교육 두 자리의 현행 전거 0/2, Dumas는 BnF·NDL 부분 확인 |
| 234 · 지도 스타일 자원 | PARTIAL | [6513921][234h] / [273d94f][234r] | 70 / 45 | 정식 6자리 중 확정 공석 3·원파일 미확보 3 |
| 235 · 표준 정오 | PARTIAL | [5dce1f8][235h] / [9d698c3][235r] | 71 / 46 | 날짜판 본문 6/6·실제 HTML target 0/6 |
| 236 · 제안자의 링크 사용 | PARTIAL | [538cb1f][236h] / [f8d76bc][236r] | 100 / 54 | 본 모집 40, 공식 링크 넓게 3·엄격 1, 교체 산출물 관측 0 |
| 237 · 개발 시간 | PARTIAL | [0cd0389][237h] / [23c2bd5][237r] | 31 / 23 | 조건별 6행씩 한 작성자, 독립 검수/인수 키 0/12 |
| 238 · 카운티 원자료 | PARTIAL | [b79bb92][238h] / [1f1221c][238r] | 102 / 29 | 원셀 0/48·실제 카드 0/30 |
| 239 · 등고선 반환 | DONE | [7a48538][239h] / [64b2d5a][239r] | 44 / 29 | 원형 입력–엔진 14조건×2회, 별도 통제 23회 |
| 240 · 문자 이름 소비자 | REVIEW_READY | [fbd1b0b][240h] / [cfabee8][240r] | 62 / 29 | 36방향 자리·실험 204호출·반례 182호출 |
| 241 · 교육 서비스 Change | DONE | [49e2c47][241h] / [bdc7c52][241r] | 109 / 78 | 여덟 앵커·16여정·목표 의미값 저장 8/8 |

요청 때 완료된 여덟 건은 sources.jsonl **472행**을 직접 파싱했다. 작업 내 source_id 중복은 없고 산입한 work_id의 작업별 합은 **284**다. 한 매뉴얼의 여러 절이 같은 계보에 있거나 같은 사건이 여러 자료에 실릴 수 있다. 예컨대 231의 29개 페이지·스레드는 13개 계보이며, 237의 23개 가운데 2개는 원저자 초록까지만 읽었다. 여덟 소유 경로의 최상위 CSV 25개, 자료행 653개를 헤더와 대조했다. **234의 layers.csv 12번째 줄 W-I만 20열 헤더에 19개 값**이다. 위치대로 읽으면 M13이 feature_evidence에, ‘not strict’가 source_ids에 놓이고 unknown이 비게 된다. 원문과 앞뒤 행을 확인해 ‘추가 World 스타일의 아이콘 공석’으로만 읽었다. 정식 6자리 분모에는 들어가지 않는다. [문제 행][234bad] · [234의 구분 기준][234r] · [231 자체 점검][231self] · [237 자체 점검][237self]

12건 모두 중앙 result_commit과 조회한 작업 브랜치 끝이 같았고 인계에 적힌 결과 SHA는 바로 앞 부모였다. 두 판의 RESULT blob도 12/12 동일했다. 236은 네 댓글 파일의 40개 배열에서 228개를 읽어 원제안부터 60일 이내 174개·빈 창 8개를 다시 셌다. 237은 12개 원표행의 역할·시간·0값 분포를 다시 집계했다. 238은 세 카드가 헤더만 있고 키가 빈 배열인 것을 확인했다. 239는 C3/C4의 원좌표, 240은 ICU 상태값을 해당 결과표와 맞췄다. 241에서는 R1-1 저장 후 복귀 및 이름이 중복된 참조 객체의 원영수증을 열어 여정표와 대조했다. 이 검토가 직접 확인한 것은 저장된 원표와 실행 영수증이다. 사용자 실험과 독립적인 바이너리 재실험은 미실시다. [236 모집][236frame] · [원댓글 묶음][236comments] · [237 시간 원행][237cohort] · [238 패킷][238manifest] · [239 C3의 첫 엔진][239sk] · [둘째 엔진][239cp] · [240 오류 원표][240err] · [241 복귀 원영수증][241raw]

## 누적 판단과 여전히 열려 있는 선택

| 최종 설계자가 결정할 일 | 지금까지 확인한 근거와 선택이 갈리는 조건 |
| --- | --- |
| 부분 입력에서 무엇을 되물을까 | 020은 전달 주장 72/73을 추적했지만 충돌이 모두 풀린 묶음은 2/16이었다. 107은 편집할 발생 위치를 알 때 6/6, 공유 정의만 줄 때 0/6이었고 159는 소비자 역할이 48/48을 갈랐다. 197의 현재 면/방문 면, 208의 원회차/이동 시각, 219의 중단 이벤트/남길 채널, 230의 파일 단위/시간 원점은 서로 다른 축이다. 목적이 쓰여 있거나 두 값의 첫 절이 같다면 조건을 설명할 수 있다. 질문에 실제 답한 뒤 효과가 달라진 분모는 230에서 0/4다. [47차 누적][prev] · [230 첫 안내][230routes] |
| 어떤 검색 결과를 새 대안으로 셀까 | 209 JPEG 질의의 단서 추가는 도구 순위 개선 0·악화 1·동률 1·불가 2쌍이었다. 220의 DuckDB 원요구 네 쌍은 제공자 원순서를 회수했다. 40자리 중 반환 21, 원문 자기 이슈가 1위인 요청 5/8, 자기 제외 외부 첫 해법 개선 0·동률 4였다. 231은 정상 응답 자체가 없어 이 결과를 다른 제공자에서 재현하지 못했다. 원문 재발견, 대안 발견, 요구 충족을 별도 집계해야 한다. [220 쌍별 판정][220pairs] · [231 수신 기록][231receipt] |
| 다른 분야 원리를 어디까지 권할까 | 010은 힌트로 7군을 찾았으나 033의 무힌트 144쌍 당시판 지지 0, 145의 독립 초안 변화 0/16이었다. 191·199는 색지각/인화 원전과 실제 조작의 관계를 좁혔다. 210·227에서 최장 길이가 같아도 Git과 Breezy의 보존 줄은 달랐다. 221→239에서 한 수식과 같은 변 쌍이 나와도 다른 입력에서 일반화가 깨졌다. 232의 조판·자막은 목적함수가 달랐다. 설명에 도움을 준 예, 추가로 맞힌 예, 사람이 읽기 쉬워진 예의 분모를 각기 유지한다. [227 앵커][227anchors] · [232 단계별 예측][232pred] · [239 대조][239control] |
| 하나, 대안 둘, 필수 조합 중 무엇을 줄까 | 040의 완전 적격은 0/8, 044의 두 묶음 방식은 동률이었다. 114가 같은 대상으로 의심한 138건은 118에서 명시 근거 7·미확인 131로 갈렸다. 193의 메일 큐/사서함, 202의 OCR 모델/모드, 204의 엔진/운영자, 213의 스타일/부모/로캘은 역할이 달랐다. 222·240의 검색 별칭/표시 이름, 233의 저자/관련 인물, 234의 그림 이름/그림 파일도 그 목적에서만 묶을 수 있다. [47차 누적][prev] · [233 역할 원표][233works] · [234 자원][234res] · [240 방향][240dir] |
| 얼마나 저장하면 과거와 현재의 주장을 되살릴까 | 055는 과거 답 4/4·다음 판 0/4, 147은 옛 답 112/112 복원, 150은 동일성과 근거 동시 복원 7·9·15/16이었다. 196은 표시 문장 4/4이나 사본 없이 원바이트 입증은 확장안 4/4였고 207의 같은 648,615ms는 다른 분절에서도 나왔다. 이번 238은 산식·코드가 있어도 기관 원행과 가린 카드가 없었고, 237은 같은 사람의 시간을 독립 검수 키로 쓸 수 없었다. 원문 링크·설명에 판/행·대상·분모를 더할 조건을 보존한다. [47차 누적][prev] · [238 원셀][238rows] · [237 단계][237stages] |
| 무엇을 보고 링크를 갱신할까 | 024에서 무효화 11건을 주기 방식 11, 신호 방식 8건 발견했다. 신호 방식은 열람 108회가 적지만 전송량이 5,672,462바이트 많았다. 152는 새 자료 15건 중 신호/희소 공급원 14, 주기 13이었다. 211의 당시 절 위치는 0/6, 216은 현존 파일 88개의 철회 표시를 대조했다. 229는 고정 인덱스의 정확판/범위에 따라 선택과 경고가 달랐다. 235는 문서가 남아도 적용 근거·소비 규칙이 서로 다른 날 바뀌는 실제 사례다. 과거 인용과 현행 첫 링크의 갱신 시점을 따로 기록한다. [229 선택][229matrix] · [235 변경 시간표][235timeline] |
| 링크 때문에 선택이 달라졌나 | 022의 미인지→선택 변경→실행은 0/24, 180의 원제보자 후속은 모집된 여덟 사건의 정한 창 안에 없었다. 194·203의 대안과 214의 제거 패치도 최초 발견의 인과를 결정하지 못했다. 225 pandas 본 모집에는 같은 작성자의 직계 수정이 1건 있으나 외부 URL은 없었다. 236은 명시 URL을 복원했어도 같은 작성자의 교체가 관측되지 않았다. 서로 다른 사람·사건의 빈 단계를 이어 붙여 인과 사슬을 만들 수 없다. [225 주장 단계][225claims] · [236 경쟁 설명][236rivals] |
| 시간을 얼마나 아꼈나 | 034는 한 단계가 380→57초인데 전체는 849→847초였다. 172는 전원·같은 기능·시간·독립 검수를 동시에 연결하지 못했다. 195는 번역 배정 24/24를 복원했지만 검수 키/시간은 0/96, 226의 역할별 처리속도와 별도의 두 단계 시간에도 직접 작성 대조·최종 인수가 빠졌다. 237의 개발 시간은 작성자 안의 두 단계다. 과제·산출물 판·외부 검수 시간·인수 기준이 같은 사건에 붙기 전까지 사람 전체 노동과 수락률은 미확인이다. [226 역할별 표][226labour] · [237 원행][237cohort] |
| 어떤 동사로 동작을 설명할까 | 176의 합격 표시 55개는 한 보고서의 재표시였다. 205 메모리 값 0→99 중 218에서 새 reader의 파일값 99는 update 8회였고 readonly/copyonwrite 16회는 0이었다. 217의 OCR 24회는 초기화 성공 14·실패 10이며 정확도는 측정하지 않았다. 227은 hunk, 228은 같은 RSS 항목의 수신 SQLite read 값 0/1, 229는 dry-run 선택·경고까지 확인했다. 239는 반환 좌표, 240은 반환 수와 오류 상태, 241은 저장 뒤 같은 URL에서 접힌 화면 섹션까지 확인했다. 공개 기대·실제 반환·사용자 목적 달성에는 각각 다른 근거가 필요하다. [47차 누적][prev] · [228 수신 원표][228obs] · [239 원영수증][239sk] · [240 ICU 원로그][240raw] |

최종 DB, 상시 수집, 검색 알고리즘과 AI 호출 수는 열려 있다. 지금 설계자가 비교할 두 가지는 **목적·해당 부품·첫 원문 절과 짧은 이유만 주는 답**, 그리고 **반환값·적용판·함께 필요한 자료가 적합성을 바꿀 때 그 근거를 펼치는 답**이다. 250은 어느 근거가 없어지면 어떤 결정을 다시 열어야 하는지 실제 묶음으로 작성한다. [제품 브리프][product] · [작업 250의 배정문](NEXT_TASKS-48.json)

## 요청 당시 새로 끝난 여덟 작업

**230 · Audacity.** #4811은 첫 라벨 이전 오디오의 포함 여부, #5302는 각 트랙을 섞지 않은 파일을 명시했다. 네 단건의 현행 본문을 먼저 읽고 두 건에는 즉답, 두 건에는 조건부 두 경로를 골랐다. 늦게 본 같은 작성자의 재시험 진술은 앞 두 건의 안내와 양립했다. #3402·#5797에는 같은 사람의 후속이 없었다. 첫 공개 revision 0/4, 실제 질문 응답 0/4, 실제 PCM 0/4다. 3.4.2의 코드에서는 상단 라벨이 경계를 정해도 아래 오디오가 믹스 대상이 될 수 있어 매뉴얼의 범위 설명과 충돌한다. 251이 파일 길이와 두 주파수를 별도로 측정하는 이유다. [첫 안내 봉인][230routes] · [원작성자 후속][230follow] · [정적 대조][230r]

**231 · DBA 검색.** 필터 생성과 모집에서 정상 API 페이지 수신이 0회였다. 원질문 0/4, 경로 0/8, 유효 비교쌍 0/4다. 검색의 정상 빈 배열, 순위 동률, 중복 경로의 실패율 어느 것도 셀 수 없다. 대신 /questions 두 태그는 AND, /search/advanced의 tagged는 OR라는 차이를 찾아 표집을 정정했고, 동률·NULL·원행 내용의 차이를 13개 SQL 통제로 명시했다. 이 13개는 문서상 예측이며 실행은 0이었다. 보정 #138641, 별도 DBA 스레드 일곱, 높이뛰기 두 경기로 본표를 대신할 수 없다. 252는 수신을, 254는 답의 의미를 맡는다. [수신 실패 원장][231receipt] · [8개 경로][231routes] · [SQL 예측][231control]

**232 · 제목 줄바꿈.** 폭 8, 단어 폭 [4,3,3,2,2]에서 줄 길이 [4,7,5]는 [8,6,2]보다 분산이 작았다. 마지막 줄을 자유롭게 두는 조판 설정은 허용 신축량에 따라 후자만 남기거나 해가 없었다. 같은 목표를 두 방법으로 푼 셈으로 합산할 수 없다. 여섯 입력의 분할 303행·단계별 예측 24행 중 WPT 002는 참조 이미지와 달라야 한다는 제약까지다. 003에는 단어 4 뒤 명시적 줄바꿈과의 일치 기대가 있었지만 그 기대가 입력에도 보였다. 두 시험×두 엔진의 실측 0/4, 독립 예측 분모 0이다. 자막의 구문을 지키는 26/14자 분할은 시각적으로 더 고른 16/24자와도 다르다. [분할표][232breaks] · [단계별 예측][232pred] · [원조건과 한계][232r]

**233 · 도서 저자 식별.** 2008년 교재가 전사한 2004년 레코드에서는 Tennessee Williams의 선호 표목과 Thomas Lanier Williams의 이형 표목을 연결했다. 현행 LC 원필드 0/6이다. Kate Davis 교육 자리 두 개는 읽었지만 기관 전거 0/2, 지명 저작에서 돌아온 실제 전거 0/3이다. Dumas 부자는 BnF·NDL 각각의 두 원레코드에서 별개로 확인됐고 한 서지에 두 사람이 함께 저자로 나타날 수도 있었다. 다섯 서지 표시는 네 작품이며 표제면 영상·원 MARC 0/5, 지명 대조 GNIS 실재 ID/이형 행 0/3이다. 책·서지판·저자 역할·전거 식별자의 단계가 남는다. 246은 세 책의 출판 책임표시에서 거꾸로 출발한다. [전거 원표][233auth] · [책별 역할][233works] · [후보와 미확인][233un]

**234 · 지도 스타일.** 사전 순서로 선택한 MapLibre Debug의 두 레이어는 raster와 hillshade라 세 역할이 실제 공석이었다. Protomaps의 공식 완성 JSON을 받지 못한 세 자리는 미확인이다. 생성 코드의 세 후보와 OSM Bright의 보강 레이어는 정식 0/6을 채우지 않는다. 보강에서는 school 피처→school_11 목록 좌표→PNG, Inn의 문자→PBF 글리프까지 이어졌다. 같은 sprite 색인과 다른 PNG 바이트의 짝도 있었다. 네 렌더 통제 0/4, 오프라인 실행 영수증 0이다. 정적 자원 존재와 사용자 화면에서의 선택을 분리해야 한다. 추가 World 대조 W-I의 한 열 결손도 원표 재사용 시 주의할 부분이다. [레이어 원표][234layers] · [실제 자원][234res] · [목적별 조합][234bundles]

**235 · 표준과 정오표.** WCAG 4.1.1 Parsing은 2.0 원문과 편집 정정, 2.1 원문과 HTML/XML의 충족 간주 노트, 2.2의 제거 표시로 갈렸다. 1.1.1은 핵심 요구가 유지되며 과거의 상호참조가 정정됐다. axe-core 4.8.0은 2.2 최종 권고안보다 먼저 나왔다. generic/active 중복 ID 규칙 비활성과 ARIA 규칙의 4.1.2·검토 분류는 같은 변경이 아니다. 세 날짜판 본문 6/6과 두 태그 규칙 8/8은 정적으로 관측됐지만 실제 HTML id/name 0/6, axe runtime 0이었다. 2.0 정정 #13의 개별 적용일도 미확인이다. 과거 감사 인용과 오늘 수정할 조건에 다른 링크를 줄 근거는 있으며, 실제 어느 요소로 스크롤하거나 도구가 실패를 냈는지는 253의 대상이다. [시간표][235timeline] · [도구 원표][235consumer] · [인용 시나리오][235cit]

**236 · Godot 제안.** 40개 모집, 60일 안 댓글 174개에서 공식 링크가 나온 사건은 넓은 정의 3/40, 원래 요구의 직접 대체 방향만 잡으면 1/40이었다. #8785에서 정점 색인의 쓸모를 인정한 뒤에도 strip 요구가 남았다. #8793의 원작성자는 문서를 읽었다고 했지만 원본 저장에 대한 설명을 더 원했다. #8803의 기능 태그 링크는 이후의 export 질문에 대한 답이었고 타인이 제안을 닫았다. 세 사건 중 열람 자기보고 1/3, 확인된 교체 산출물 0/3, 보강 #8903은 이미 문서를 읽고 시도했으나 실패했다는 진술이다. 작업자는 before 추출에서 ‘worked around’를 놓쳐 사후 정정했고 OSM 원사건 0/2였다. 진행표 본문도 당시 작업자에게 보이지 않았지만 이번 검토에서는 중앙 236의 의존이 225인 것을 확인했다. 현재 배정의 가시성은 당시 개인의 지식 결손을 해소해 주지 않는다. [사건별 링크][236chain] · [무효/경쟁 설명][236rivals] · [중앙 배정][req]

**237 · METR 개발 시간.** 초기판의 두 조건에서 issue 번호순 여섯 개씩 읽은 12건은 모두 개발자 655의 행이다. 초기 작업과 리뷰 후 수정 모두 같은 작성자의 분이며 후기시간 0이 7개다. 원표를 다시 더한 산술평균은 불허 146.50분·허용 226.67분이고 독립 검수/인수 키는 0/12다. 전체 완료 246건에서 후기 원값 결측이 16건인 데 비해 논문은 27건이라고 했고 외부 자료 요구도의 척도 방향도 README와 조사 지침이 반대다. 발표의 보정 로그 시간비 +18.8%와 12행의 단순평균비는 대상과 계산이 다르다. 후속 자료 1,134건은 complete 828·incomplete 244·ditched 57·cheating 2·corrupted 3이며 원저자 조건으로 유효 완료는 827이다. 독립 회귀·최종 인수 관측은 없다. 번역 파일럿에서도 66.36분 실패와 79.17분 합격이 공존했다. 더 빨리 끝난 산출물의 품질은 별도로 판정해야 한다. [12개 원행][237cohort] · [원관측][237obs] · [측정 대상 차이][237estim]

## 요청 이후 중앙 DONE이 된 실행 작업

| 작업·자체 판정 | 원자료에서 확인한 결과 | 남은 판단 |
| --- | --- | --- |
| 238 · PARTIAL | 2023 ACS5의 카운티 B23025 분산재현 자료가 공식 목록에 있다는 점과 기관 worked example의 산술을 확인했다. 실행 영수증 37건 모두 프록시 CONNECT 403·exit 56으로 기관 본문 수신에 실패했다. 네 카운티·48셀, 두 결합률/오차, 실제 10명제와 카드 30장이 모두 비어 있다. A/B/C는 같은 헤더만 있는 파일 3개, 키는 0행이다. [실제 요청][238http] · [원셀][238rows] · [manifest][238manifest] | 계산기와 자료목록을 확보해도 특정 지역의 공표값이나 독립 판독 결과를 줄 수 없다. 정상적으로 확보한 동판 기관 원행 및 지문, 유효 두 결합률, 정답 키, 각각 10행인 세 벌과 올바른 지문이 242의 선행이다. |
| 239 · DONE | 두 고정 엔진의 일곱 입력·두 반복 28/28, 추가 통제 23/23. C3에서 scikit-image는 북–서·동–남, ContourPy는 북–동·남–서였다. 보간 끝점이 같아도 연결이 달랐다. C4의 정확 동률에서 둘 다 두 선을 냈고, 연속 쌍선형 모델은 중앙을 공유하는 X를 낸다. [C3 원반환 1][239sk] · [원반환 2][239cp] · [통제][239control] | scikit-image의 C3가 연속장과 같은 쌍을 골라도 C2에서는 다르다. 14개 입력–엔진 판정 가운데 사전 10, 기대 동시 노출 뒤 재구성 4, 독립 가림 분모 0이다. 해당 빌드의 반환 기하까지만 입증됐다. |
| 240 · REVIEW_READY | CPython 3.13.0/UCD 15.1은 별칭 13/13을 받아들였고 ICU4C 76.1/UCD 16.0의 ALIAS는 correction 4개를 받아들였다. ICU 헤더의 miss 상수 10과 실제 12가 달랐다. 실제 miss는 65535·status 12, EXTENDED의 유효한 U+FFFF도 65535이지만 status 0이었다. 36방향 중 적용 34, N/A 2, 본 호출 204/204·반례 182/182다. [실제 방향][240dir] · [오류 원표][240err] · [ICU 원로그][240raw] | 표시할 공식명, 입력 별칭, API choice와 실패 상태를 보존해야 한다. 시간대 대조도 입력 ID·CLDR canonical·IANA preferred가 달랐다. 다른 빌드, 로캘 UI에서의 표시는 미확인이다. |
| 241 · DONE | 두 교육 서비스의 네 화면·여덟 Change 앵커를 변경 저장/무저장 복귀로 나눈 16/16 여정이 원 URL로 돌아왔다. 저장 8/8에서 목표 의미값이 바뀌었고 모델의 목표 속성만 바뀐 경우는 3/8이었다. R1-1은 같은 URL에서도 course 섹션이 접혔다. 중복 참조 두 개는 AX 이름이 같고 실제 객체 ID가 달랐다. [16여정][241js] · [복귀 원영수증][241raw] · [중복 이름][241dup] | 브라우저의 접근성 트리에서 계산한 이름까지 확인했다. 실제 화면낭독기 발화·사용자 선택률, 다른 브라우저, 도서관 예약 거래는 미확인이다. |

## 서로 어긋난 결론과 판정 기준

| 어긋난 관측 | 같은 사건·대상에 맞춰 내릴 수 있는 판단 | 답을 바꿀 확인 |
| --- | --- | --- |
| 230은 첫 글만 보고 두 번 즉답했고 231은 첫 답 8개 전부가 결측이다. | 무엇을 알아야 첫 절을 고를지 정하는 문제와 제공자가 그 절을 노출하는 문제는 별개다. 230의 두 재시험 진술은 첫 링크가 원인이었다는 증거로 쓸 수 없다. | 243은 원글 봉인 뒤 본문 목차·탐색책갈피를 가른다. 252/254는 다른 공급자의 실제 도착을 원계약으로 판독한다. [230 후속][230follow] · [231 수신][231receipt] |
| 232에서 가장 고른 폭은 조판의 최적안과 달랐고 239에서는 같은 끝점도 다른 선이 됐다. | 목표 함수·경계 조건·동률 처리까지 주어져야 구현 예측이 특정된다. 002의 참조 불일치 통과도 어느 단어 뒤에 줄을 나눴는지 결정하지 않는다. | 245는 음성 정렬의 제약이 음악의 어느 대응점을 실제 제한하는지, 255는 두 WPT의 픽셀 단언과 단어 줄 위치를 따로 확인한다. [232 분할][232breaks] · [239 좌표][239obs] |
| 233에서 두 이름/작품을 연결하고 240에서 별칭을 받아들여도 반환할 이름은 달랐다. 234에서는 그림 이름을 알아도 다른 atlas 바이트가 나왔다. | 레코드의 지시 대상, 역할, 검색 문자열, 소비 API가 반환하는 값, 화면에 쓰인 바이트는 독립적으로 확인할 관계다. | 246은 표제면→서지→전거의 양방향을, 247은 모델 재질→그림/바이트의 실제 참조를 짚는다. [233 저작][233works] · [234 자원][234res] · [240 방향][240dir] |
| 235는 제거된 기준의 본문 자리가 남았지만 도구의 처리 시점은 더 빨랐다. | 특정 절의 존재, 그때의 규범력, 사용자가 실제 받을 도구 결과는 서로 다른 시간축이다. | 253은 여섯 실제 앵커와 두 axe 판의 결과 분류를, 248은 릴리스 지원 선언과 실제 wheel 발행 시점을 가른다. [235 변경 사건][235timeline] · [235 규칙][235consumer] |
| 225의 실제 패치, 236의 실제 URL, 237의 두 시간, 238의 가중 산식은 각각 참인 근거를 가질 수 있다. | 다른 작성자/사건을 조합해 발견 인과를 만들거나, 다른 역할의 값을 붙여 총노동을 만들거나, 만들어진 산식에 결측 지역을 넣어 통계를 만들 수 없다. | 249는 동일 세션의 사전 설계·노출·변경·인수를 연결한다. 250은 근거 한 묶음이 빠질 때 철회해야 할 문장을 표시한다. 242는 기관 수치 확보 뒤에만 연다. [236 사건][236chain] · [237 시간][237cohort] · [238 패킷][238manifest] |

## 다음 배정과 의존 관계

웹 조사·설계 8건은 각각 다른 판단을 맡는다. 같은 호스트를 쓰더라도 답해야 할 문제·표본·완료 산출물이 다르다. 예를 들어 245는 악보와 연주의 **박 시각**을, 246의 음악 대조는 **작품·녹음의 서지 관계**를 본다. 249는 사람에게 정보를 제공할 시점을 통제하는 연구안, 250은 최종 설계자에게 건넬 근거의 조합안이다. 각각의 brief에 고정 선행 SHA·제외 범위·일곱 세부 질문·직접 열 자료 유형별 하한·반례·표 열·파일·중간 커밋·자체 점검 후 인계 조건을 넣었다. [전체 JSON](NEXT_TASKS-48.json)

| AF-RES·담당 | 선행·착수 | 조사 대상과 판별 목표 | 완료를 판단할 결과 |
| --- | --- | --- | --- |
| 243 · web-pro | 230, 즉시 | Pandoc 네 최초 요청 자리에서 인쇄 목차·탐색 책갈피·제목 문자열을 구별한다. | 현행/최초 본문을 분리한 네 사전 안내, 후속 작성자 증거, 조건에 따라 바뀌는 절과 EPUB 대조 |
| 244 · web-pro | 231, 즉시 | scikit-learn 세 심볼에 실제 게시된 예제 목록에서 ‘언급’, ‘호출’, ‘원하는 반환값을 씀’을 가른다. | 여섯 자리의 원순서·호출 줄·소비 줄·두 면으로 판단 가능한 범위와 MeSH 색인 반례 |
| 245 · web-pro | 232, 즉시 | 말소리의 시간 변형 원리가 악보·연주의 내부 박을 얼마나 결정하는지 확인한다. | 실제 두 주석쌍의 14개 내부 박과 세 비용표의 경쟁 경로, 입력에 음향 특징이 없을 때의 보류 |
| 246 · web-pro | 233, 즉시 | 교육용 Kate Davis 두 자리의 실제 서지 관계를 세 책에서 역추적한다. | 판/책임표시→기관 서지→전거와 역방향 원필드. 기관 원레코드 부재·교육용 가공 가능성도 표기 |
| 247 · web-pro | 234, 즉시 | Khronos Box·BoxTextured·AnisotropyBarnLamp의 기하·재질·오프라인 전달에서 파일과 확장 의존을 구별한다. | 세 자산×세 목적의 실제 참조·대체 자원·미확인, 외부 URI 또는 내장 바이트의 원문 위치 |
| 248 · web-pro | 235, 즉시 | SciPy 세 릴리스×세 CPython에서 지원 문구·메타데이터·실제 업로드 파일이 맞는지 본다. | Linux x86_64의 9개 셀에 파일 태그·업로드 시각·조건. sdist/다른 플랫폼·실행 성공은 따로 판정 |
| 249 · web-pro | 236, 237, 즉시 | 발견 이전의 지식, 같은 작성자의 선택 변경, 독립 인수를 한 사건에서 식별할 연구를 설계한다. | 두 개발 과제·지연 공개 조건·사건 키·품질 기준·사람시간·합성 행동기록 네 건. 실제 참가자 효과는 미측정 |
| 250 · web-pro | 230, 233~237, 즉시 | 짧은 근거 하나를 제거해도 최종 설계자가 나머지 대안과 보류 이유를 추적할 수 있는지 설계한다. | 여섯 주장 묶음, 15쌍의 관계, 두 조합에서 하나씩 제외한 12자리. 과거 보고 재요약 대신 실제 인계 입력을 제공 |
| 251 · codex-cloud | 230, 즉시 | Audacity 두 정확판에서 라벨 위치가 정하는 파일 경계와 믹스된 오디오를 측정한다. | 16회 정상 내보내기의 WAV 프레임과 440/880Hz, 단일 변경·독립 디코더·재생 영수증 |
| 252 · codex-cloud | 231, 즉시 | DBA 공개 API의 정상 모집과 원순위를 받아 원질문·익명 답·경로 키를 만든다. | 최대 120개 모집, 첫 12 duplicate 하위집합, 제목식 질의를 미리 고정한 실제 A/B 배열·판독 파일 지문 |
| 253 · codex-cloud | 235, 즉시 | W3C 날짜판 앵커의 실제 도착 요소와 axe 판/옵션의 결과 종류를 검사한다. | 6개 target·두 도구판×네 입력×세 모드 24원결과·별도 재생 |
| 254 · web-pro | **252, BLOCKED** | 원요구와 익명 도착 답을 다른 사람이 순서대로 판독해 그룹별 최신 원행·동률·NULL 계약 충족을 채점한다. | 원요구 계약·익명 답·경로 공개 후 3단계 커밋, 가능한 최대 네 쌍의 근거·정상 공석·원래 미수신 분리 |
| 255 · codex-cloud | 232, 즉시 | 두 WPT 입력에 대해 Blink와 WebKit의 실제 픽셀 단언과 각 단어가 놓인 줄을 확인한다. | 8회 정상 reftest와 단어별 기하, Ahem 실로딩·폰트 반례·재생. 239의 등고선 좌표는 사용하지 않음 |

252의 제목식 질의는 최초 제목에서 고정 규칙으로 2~4단어를 가져온다. 231이 계획한 사람이 고른 질의와 모집 분모도 따로 표시한다. 254는 252가 실제 수신한 질문 배열·모집 경계·세 판독 파일의 지문을 확인한 경우에만 열린다. 원글만 받은 판독자가 계약을 커밋하고, 익명 답을 채점해 다시 커밋한 뒤 대응표를 연다. 네 쌍보다 적으면 모자란 이유와 분모를 보고한다. 정상 빈 배열과 실패 응답을 구분할 근거가 없으면 시작 조건 미달이다. [231 수신 인덱스][231receipt] · [두 후속 배정](NEXT_TASKS-48.json)

### 요청 당시 238~242와의 경계

| 이미 배정된 대상 | 해석에 필요한 선행 결과 | 이번 즉시 웹 과제와 구별한 점 |
| --- | --- | --- |
| 238 · ACS 네 카운티의 공표 셀·두 결합률·실제 카드 제작 | 224의 정의와 정상 수신한 동판 기관 원파일 | 243~250에는 카운티 원행·계산식·카드가 없다. 250의 근거 묶음도 230·233~237 중 여섯 사례로 한정했다. 기존 238의 재개는 정당하게 이용 가능한 발행기관 원파일·지리 키·판이 확보될 때 같은 기준을 쓴다. |
| 239 · 두 엔진의 7개 수치 격자·모서리 연결 | 221의 정적 예측과 해당 빌드 반환 좌표 | 245는 시간축의 구간 대응 및 연주 주석, 255는 문서의 줄바꿈이다. 239의 결과는 누적 검토에만 반영했다. |
| 240 · 두 Unicode 소비자의 이름 검색·반환/오류 | 222의 6문자·별칭과 실제 라이브러리 상태값 | 246은 출판물의 책임표시·서지와 기관 전거 연결이다. 정정 별칭이나 문자 API 호출을 재검사하지 않는다. |
| 241 · Apply/Register의 Change 앵커, 편집·저장·복귀 | 223의 소스 연결 8앵커와 같은 화면의 실행 증거 | 243은 문서 작성자의 출력 목적, 244는 API→예제의 코드 사용, 253은 날짜판 target과 별도 로컬 규칙 판정이다. 서비스 화면·필드·여정 로그를 선행으로 쓰지 않는다. |
| 242 · 238이 만든 카드 A/B/C의 별도 판독 | 238 중앙 DONE **및** 실제 48셀/공식 부재 확인, 두 유효 결합률, 10명제 정답과 10행씩 세 벌의 카드·검산 지문 | 현재 238의 파일은 이름만 존재하며 0/0/0행이다. 242는 BLOCKED로 둔다. 새 254는 SQL 답의 계약과 도착 경로를 읽으며 세 지역통계 카드를 다루지 않는다. |

자료가 준비됐다는 계획상의 READY는 실제 작업자 배정·착수와 구분된다. 조사 입구로 지명한 자료는 최종 설계 근거로 승격하려면 해당 작업에서 판·내용·한계를 다시 확인해야 한다. [Pandoc 단건 예](https://api.github.com/repos/jgm/pandoc/issues/449) · [예제 색인 규칙](https://sphinx-gallery.github.io/stable/configuration.html) · [ASAP 원자료](https://github.com/fosfrancesco/asap-dataset) · [Khronos 모델 목록](https://github.com/KhronosGroup/glTF-Sample-Assets/blob/main/Models/Models.md) · [SciPy 릴리스](https://docs.scipy.org/doc/scipy/release/1.14.1-notes.html)

## 다음 판정을 가장 크게 바꿀 세 가지 결손

| 불일치 또는 약점 | 지금 오해할 수 있는 판단 | 다음 조사·판정 전환 조건 |
| --- | --- | --- |
| 선택·만족·노동의 당사자와 시점이 끊겨 있다. | 230의 두 재시험이나 236의 링크 열람으로 발견을 입증하고, 237의 작성자 시간을 전체 노동으로 환산할 수 있다. | 249에서 사전 지식·봉인된 설계·노출·후속 산출물·독립 검수와 인수를 같은 키에 묶는다. 각 단계에서 경쟁 설명이 남을 때 허용할 문장을 따로 둔다. |
| 정상 공석과 원자료 미수신이 같은 빈칸처럼 보인다. | 231의 수신 실패를 검색 성능 0%, 234의 여섯 공석 전체를 자원 부재, 238의 헤더 파일을 242 착수 증빙으로 쓸 수 있다. | 252/254는 원배열과 의미 판정을 분리한다. 234는 다른 스타일을 끼워 넣기 전에 공식 완성 스타일과 같은 판의 실제 feature를 확보해야 한다. 238은 공개 원값과 실제 카드 수를 복구해야 242에 전달한다. |
| 규칙·표시·실제 작동을 같은 근거로 전파할 수 있다. | 232의 WPT 기대에서 줄 위치를, 235의 기준 문구에서 도구 결과를, ICU의 반환 숫자 하나에서 성공을 확정한다. | 251·253·255는 각각 원음, 실제 도구 분류, 실제 줄 기하를 검산한다. 240의 성공/실패 동일 숫자처럼 반대 판정을 만드는 추가 필드를 250의 인계 단위에 보존한다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/7369707441e2eb70e84004ca6cb3bfeefc8b4061/docs/product/RESEARCH_BRIEF.md
[236chain]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/chain.csv
[239obs]: https://github.com/laadkke-arch/agentflow-open/blob/7a48538c4dec868a3cb97e8834ddbaa71d28df84/docs/workstreams/research/AF-RES-239/observed.csv
[prev]: https://github.com/laadkke-arch/agentflow-open/blob/685311ef0589f021abd6f2aeb8928fd63fcb3351/docs/workstreams/planning/REVIEW-47.md
[old]: https://github.com/laadkke-arch/agentflow-open/blob/3057e4ede5762f3f7352420085f74016e939c27c/docs/automation/dot-control.json
[req]: https://github.com/laadkke-arch/agentflow-open/blob/7369707441e2eb70e84004ca6cb3bfeefc8b4061/docs/automation/dot-control.json
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/7369707441e2eb70e84004ca6cb3bfeefc8b4061/docs/RESEARCH_WORKFLOW.md
[end]: https://github.com/laadkke-arch/agentflow-open/blob/c02486b3d2f3db80f4672b5d9945e51b0e6853c7/docs/automation/dot-control.json
[238manifest]: https://github.com/laadkke-arch/agentflow-open/blob/b79bb92387ce8f4d70616486a9fcc5a355be9fc6/docs/workstreams/research/AF-RES-238/packet-manifest.json
[230h]: https://github.com/laadkke-arch/agentflow-open/blob/896b13e51f18738e60d63977e999c0aa25027057/docs/workstreams/research/AF-RES-230/HANDOFF.md
[230r]: https://github.com/laadkke-arch/agentflow-open/blob/cb0cb98c87060f10be7f890caa1a5c736540235c/docs/workstreams/research/AF-RES-230/RESULT.md
[231h]: https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/HANDOFF.md
[231r]: https://github.com/laadkke-arch/agentflow-open/blob/b9a13af90bab17cb640305d6d24ec52d62c71b89/docs/workstreams/research/AF-RES-231/RESULT.md
[232h]: https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/HANDOFF.md
[232r]: https://github.com/laadkke-arch/agentflow-open/blob/a88485d2471d69384d3bd72c16abfe2fd81a1bc0/docs/workstreams/research/AF-RES-232/RESULT.md
[233h]: https://github.com/laadkke-arch/agentflow-open/blob/08685fe6a837db69ffc5a34b0c1dd0eccbfa4918/docs/workstreams/research/AF-RES-233/HANDOFF.md
[233r]: https://github.com/laadkke-arch/agentflow-open/blob/157d1152dc4f6169d68addaecc149f3761c86e3a/docs/workstreams/research/AF-RES-233/RESULT.md
[234h]: https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/HANDOFF.md
[234r]: https://github.com/laadkke-arch/agentflow-open/blob/273d94fc4c65b25d4a0b3c7739d0000e801d28e7/docs/workstreams/research/AF-RES-234/RESULT.md
[235h]: https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/HANDOFF.md
[235r]: https://github.com/laadkke-arch/agentflow-open/blob/9d698c3e01b67fee6f189d0452efa4ccb3e2b572/docs/workstreams/research/AF-RES-235/RESULT.md
[236h]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/HANDOFF.md
[236r]: https://github.com/laadkke-arch/agentflow-open/blob/f8d76bcbfed2073733b377a84350a5a01e3cc3fa/docs/workstreams/research/AF-RES-236/RESULT.md
[237h]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/HANDOFF.md
[237r]: https://github.com/laadkke-arch/agentflow-open/blob/23c2bd58e9f08816231c81f796aaa75a8500cead/docs/workstreams/research/AF-RES-237/RESULT.md
[238h]: https://github.com/laadkke-arch/agentflow-open/blob/b79bb92387ce8f4d70616486a9fcc5a355be9fc6/docs/workstreams/research/AF-RES-238/HANDOFF.md
[238r]: https://github.com/laadkke-arch/agentflow-open/blob/1f1221c9b9dd9ad65938b0a3ea007ebc24e03841/docs/workstreams/research/AF-RES-238/RESULT.md
[239h]: https://github.com/laadkke-arch/agentflow-open/blob/7a48538c4dec868a3cb97e8834ddbaa71d28df84/docs/workstreams/research/AF-RES-239/HANDOFF.md
[239r]: https://github.com/laadkke-arch/agentflow-open/blob/64b2d5a90e3b73c7ff0c197ddfb75bbcc0b4aa93/docs/workstreams/research/AF-RES-239/RESULT.md
[240h]: https://github.com/laadkke-arch/agentflow-open/blob/fbd1b0b2f630ca7822e7d77094cb71cc5d9afe96/docs/workstreams/research/AF-RES-240/HANDOFF.md
[240r]: https://github.com/laadkke-arch/agentflow-open/blob/cfabee892503403b3900f9100d3a141d08475a71/docs/workstreams/research/AF-RES-240/RESULT.md
[241h]: https://github.com/laadkke-arch/agentflow-open/blob/49e2c4708f4830e3077eb1b96625926647316a5e/docs/workstreams/research/AF-RES-241/HANDOFF.md
[241r]: https://github.com/laadkke-arch/agentflow-open/blob/bdc7c52ba9364c29997bd70c89752a026bd732e2/docs/workstreams/research/AF-RES-241/RESULT.md
[234bad]: https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/layers.csv#L12
[231self]: https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/SELF_CHECK.md
[237self]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/SELF_CHECK.md
[236frame]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/frame.csv
[236comments]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/comments-01.jsonl
[237cohort]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/cohort.csv
[239sk]: https://github.com/laadkke-arch/agentflow-open/blob/7a48538c4dec868a3cb97e8834ddbaa71d28df84/docs/workstreams/research/AF-RES-239/receipts/primary/C3-skimage-1.json
[239cp]: https://github.com/laadkke-arch/agentflow-open/blob/7a48538c4dec868a3cb97e8834ddbaa71d28df84/docs/workstreams/research/AF-RES-239/receipts/primary/C3-contourpy-1.json
[240err]: https://github.com/laadkke-arch/agentflow-open/blob/fbd1b0b2f630ca7822e7d77094cb71cc5d9afe96/docs/workstreams/research/AF-RES-240/errors.csv
[241raw]: https://github.com/laadkke-arch/agentflow-open/blob/49e2c4708f4830e3077eb1b96625926647316a5e/docs/workstreams/research/AF-RES-241/receipts/journeys/R1-1-S.json
[230routes]: https://github.com/laadkke-arch/agentflow-open/blob/2dd710ad319633c68df5ff37d566c3468e4dfba9/docs/workstreams/research/AF-RES-230/first-routes.md
[220pairs]: https://github.com/laadkke-arch/agentflow-open/blob/5df1c4816f3401629d6a247d8f0ed8bb7c0cad37/docs/workstreams/research/AF-RES-220/pairs.csv
[231receipt]: https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/receipts/INDEX.json
[227anchors]: https://github.com/laadkke-arch/agentflow-open/blob/075c66a02f17b4fd466a12ba5c0b49cf1b6539b6/docs/workstreams/research/AF-RES-227/anchors.csv
[232pred]: https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/predictions.csv
[239control]: https://github.com/laadkke-arch/agentflow-open/blob/7a48538c4dec868a3cb97e8834ddbaa71d28df84/docs/workstreams/research/AF-RES-239/controls.csv
[233works]: https://github.com/laadkke-arch/agentflow-open/blob/08685fe6a837db69ffc5a34b0c1dd0eccbfa4918/docs/workstreams/research/AF-RES-233/works.csv
[234res]: https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/resources.csv
[240dir]: https://github.com/laadkke-arch/agentflow-open/blob/fbd1b0b2f630ca7822e7d77094cb71cc5d9afe96/docs/workstreams/research/AF-RES-240/directions.csv
[238rows]: https://github.com/laadkke-arch/agentflow-open/blob/b79bb92387ce8f4d70616486a9fcc5a355be9fc6/docs/workstreams/research/AF-RES-238/rows.csv
[237stages]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/stages.csv
[229matrix]: https://github.com/laadkke-arch/agentflow-open/blob/10a7d1ca8baf7cea5e3ccb5644b31281fe7db26d/docs/workstreams/research/AF-RES-229/matrix.csv
[235timeline]: https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/timeline.csv
[225claims]: https://github.com/laadkke-arch/agentflow-open/blob/d1d8595dd72dcfc809c1045e20d44366bbe30ae5/docs/workstreams/research/AF-RES-225/claims.csv
[236rivals]: https://github.com/laadkke-arch/agentflow-open/blob/538cb1f04c83ae2dbf79be7d4fc91b27f818baef/docs/workstreams/research/AF-RES-236/rivals.csv
[226labour]: https://github.com/laadkke-arch/agentflow-open/blob/d166817bc25f79650f2d02835b0f5f42617cdbdd/docs/workstreams/research/AF-RES-226/labour.csv
[228obs]: https://github.com/laadkke-arch/agentflow-open/blob/a2e9d82ec4aa2d75f36f4c008ada4d3e91cbe40e/docs/workstreams/research/AF-RES-228/observed.csv
[240raw]: https://github.com/laadkke-arch/agentflow-open/blob/fbd1b0b2f630ca7822e7d77094cb71cc5d9afe96/docs/workstreams/research/AF-RES-240/receipts/main/icu-1.stdout
[230follow]: https://github.com/laadkke-arch/agentflow-open/blob/896b13e51f18738e60d63977e999c0aa25027057/docs/workstreams/research/AF-RES-230/followup.csv
[231routes]: https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/routes.csv
[231control]: https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/control_predictions.csv
[232breaks]: https://github.com/laadkke-arch/agentflow-open/blob/430a1a5ec049f58878d963cb8ca539c9375f93d0/docs/workstreams/research/AF-RES-232/breaks.csv
[233auth]: https://github.com/laadkke-arch/agentflow-open/blob/08685fe6a837db69ffc5a34b0c1dd0eccbfa4918/docs/workstreams/research/AF-RES-233/authority.csv
[233un]: https://github.com/laadkke-arch/agentflow-open/blob/08685fe6a837db69ffc5a34b0c1dd0eccbfa4918/docs/workstreams/research/AF-RES-233/unresolved.md
[234layers]: https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/layers.csv
[234bundles]: https://github.com/laadkke-arch/agentflow-open/blob/6513921a9aa6f05b7424b4862700daea230d8f9c/docs/workstreams/research/AF-RES-234/bundles.csv
[235consumer]: https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/consumer.csv
[235cit]: https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/citations.csv
[237obs]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/primary-observations.md
[237estim]: https://github.com/laadkke-arch/agentflow-open/blob/0cd0389a47514c81d95ed2b2cd7e42e1efe84ba5/docs/workstreams/research/AF-RES-237/estimands.md
[238http]: https://github.com/laadkke-arch/agentflow-open/blob/b79bb92387ce8f4d70616486a9fcc5a355be9fc6/docs/workstreams/research/AF-RES-238/receipts/http-attempts.jsonl
[241js]: https://github.com/laadkke-arch/agentflow-open/blob/49e2c4708f4830e3077eb1b96625926647316a5e/docs/workstreams/research/AF-RES-241/journeys.csv
[241dup]: https://github.com/laadkke-arch/agentflow-open/blob/49e2c4708f4830e3077eb1b96625926647316a5e/docs/workstreams/research/AF-RES-241/receipts/controls/C-A1-DUP.json
