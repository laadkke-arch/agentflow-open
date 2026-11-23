# REVIEW-18 · 설계 중인 소프트웨어에 쓸 링크를 찾고, 그 링크가 선택을 뒷받침하는지 확인하기

**현재 근거로는 ‘참고할 링크를 찾았다’, ‘그 부분이 요구를 충족한다’, ‘개발자가 그 때문에 다른 선택을 했다’에 서로 다른 판정이 필요하다.** 새 검색 연구는 기존 기능의 수정 지점과 다른 분야에서 빌릴 시험 아이디어를 찾았다. 세 실제 문제 중 두 필수조건을 갖춘 새 해법으로 확인된 것은 없었다. 반면 이전 답을 다시 계산하는 일은 작은 통제 실험에서 재현됐다. 무엇을 보관해야 하는지는 사용자가 나중에 다시 묻는 질문에 달려 있다. 특히 ‘이 후보도 가능하다’와 ‘이 후보가 유일하거나 가장 낫다’는 증명의 범위가 다르다. [새 검색 결과][r69] · [재계산 결과][r71] · [제품 연구 브리프][product]

## 검토 기준과 새 인계

2026-11-23 UTC. 계획 브랜치의 최신 REVIEW-17을 먼저 읽었다. 그 파일이 사용한 통합판 `320424d`와 이번 통합판 `39cadb6`의 모든 작업을 ID로 대조했다. 등록 66→70건, DONE 64→68건, BLOCKED 2→2건이다. 이전 66개 행은 필드 단위로 같았다. 018·035는 계속 BLOCKED이고 이번 비교 대상이 아니다. 새 DONE은 069~072 네 건뿐이다. 중앙 DONE 68행의 `acceptance_evidence`는 모두 빈 배열이다. 연구 수용 여부는 각 작업의 인계·결과·원장에서 판정했다. 068까지의 결론은 이전 REVIEW에서 인수했다. [이전 누적 검토][previous] · [직전 원장][before] · [이번 원장][registry] · [운영 규칙][workflow]

| 작업·상태 | 인계 커밋 / 결과 커밋 | 실제 관측 | 이 자료에서 아직 답하지 못한 질문 |
| --- | --- | --- | --- |
| 069 · PARTIAL | [616a1da][h69] / [fb710fc][r69] | 문제 3·검색 18·반환 90자리. 일반 검색에서 수정 지점, 관계 검색에서 조건부 시험 관점이 나왔다. | 최초판이 확인된 엄격 비교 0쌍. 양쪽을 같은 실제 비용으로 비교하거나 원 개발자의 채택을 확인하지 못했다. |
| 070 · PARTIAL | [1a92715][h70] / [30266f9][r70] | 4개 프로젝트의 주 12·진단 12건. 사전에 고른 새 작성자 값은 진단 1건에서 조건부 후보를 좁혔다. | 정답의 개선·악화를 독립 판별할 수 있는 분모가 0이다. 새 질문 발송·그에 따른 사용자 비용은 관측하지 못했다. |
| 071 · REVIEW_READY | [f8b3fc8][h71] / [cb4931b][r71] | 8개 객체, 주 22·보조 4변경쌍. 발췌와 설정을 보관하면 실험 속 과거 자료 소실 후에도 주 22/22를 재계산했다. | 후보 전체를 알아야 하는 주장, 실제 발행사 과거 바이트와 운영 규모 비용에 적용되는지는 미확인이다. |
| 072 · REVIEW_READY | [f77d2d6][h72] / [330efd4][r72] | 20작품×보류 요청 6건. 색인으로 부분·원거리 후보가 각각 하나씩 상위 3에 진입했다. 비용과 순위는 추적 가능하다. | 직접 적격의 분모는 0. 최종 54자리 중 48자리는 개별 표시 판독 메모와 연결되지 않는다. |

네 작업의 브랜치 끝은 각각 중앙 결과 SHA와 같았고 각 인계 커밋은 HANDOFF.md 한 파일만 추가했다. 이번 검토에서는 해당 소유 경로의 결과·CSV·JSONL과 집계 코드를 고정판에서 열었다. 071의 준비·실행·감사와 072의 오프라인 재생 2회·감사를 별도 임시 경로에서 실행했다. 071의 짝·입력 지문·판정·점수 원장은 커밋본과 바이트 단위로 일치했다. 072의 순위 지문은 `c2b7aad3…`, 표시·접근 영수증 지문은 `311ef22d…`로 원 보고와 같았다. 069·070의 외부 저작 전부를 이번에 다시 판독하거나 072의 라이브 HTTP를 새로 측정한 것은 아니다. [071 재현 절차][rc71] · [072 재현 절차][rc72]

## 068까지 이어지는 제품 판단

제품의 출발점은 개발자가 만들고 있는 소프트웨어의 전체 또는 선택한 부분과 그 목적이다. 반환 후보에는 그대로 쓸 제품·사이트·서비스, 특정 기능·부품, 다른 분야에서 옮길 원리가 포함된다. 최종 설계자가 어떤 선택을 할 수 있게 되었는지가 평가 대상이다. Studio의 현 입력 형식, 상시 크롤링, 특정 DB는 모두 비교할 대안으로 남아 있다. [제품 브리프][product] · [선행 결과와 분모][previous]

| 설계 질문 | 앞선 표본에서 확인된 것 | 계속 열어 둘 판단 |
| --- | --- | --- |
| 부분 요청에서 무엇을 보존하고 언제 물을까? | 초기 합성 요청에서 부정 조건이 누락됐다. 020은 주장 72/73을 전달했지만 충돌 16건 중 완전 해소는 2건이었다. 026의 실제 질문 발송은 0건, 030의 직접 답변은 일반 선정 3건·답변 우선 6건에서 엄격 권고 변경이 각각 0건이었다. [030 근거][correct30] | 목적·금지조건은 보존할 이유가 있다. 매번 맥락을 더 요구할 이득과 비용은 미확인이다. |
| 다른 분야의 원리나 놓친 선택을 찾을 수 있나? | 010은 분야 단서와 원전 24개에서 원리 7군을 찾았고 011의 타 분야 답 14개에는 요청자 반응이 없었다. 013의 당시 선례 회수는 웹 16/176·목록 5/176, 033의 단서 없는 144쌍은 넓은 지지 1·당시판 지지 0이었다. 065에서 사진 레이아웃의 현재 설명이 인쇄 원리를 지목했다. 최초 선정 요건 충족 0/8, 역사적 인용 사건 0/4였다. [065 결과][base65] | 아이디어의 출처, 당시 발견 가능성, 새 문제의 실행 가능한 선택은 각각 근거가 필요하다. 012의 합성 근접 오답 증가도 014의 실제 485개에서는 재현되지 않았다. |
| 링크를 보자 실제 결정이나 노동이 달라졌나? | 022의 결정 우선 24건에선 미인지→변경→시행이 0건, 발견 진술 우선 9건에선 1건이었다. 046의 보강층에서 첫 링크를 수정 이유로 명시하고 시험까지 이은 것은 0/4였다. 061의 비교 가능 6행은 예측 차이 0/6이었다. 034의 패키지 선택은 380→57초, 전체 과제는 849→847초였다. [누적 검토][previous] | 짧게 찾은 시간·실행 성공·실제 재작업 절감은 별도 결과다. 모집을 성공 진술에서 시작하면 빈도가 달라진다. |
| 근거가 붙은 답은 언제 더 정확한가? | 021에서 두 절 예산의 공식 지지와 근거 동시 회수는 주소만 6/23, 절 목록 9/23, 요구–절 대응 14/23, 잘못 대응 8/23이었다. 054의 정확 완료는 전체 네 과제 3/12 대 1/12, 단일 과제 3/12 대 4/12였다. 058·062에서 옳은 채택과 오수락의 방향은 보기별로 달랐다. 066에서는 한 권고에만 제공된 출처가 상대 권고 결과행에도 들어갔고 세 출처를 전부 검증한 권고는 0/24였다. [021 근거][correct21] · [066 두 결과행][base66] | 표시한 URL·절, 그 절이 직접 지지한 요구, 당사자가 실제로 본 보기의 소속을 보존한다. |
| 옛 답을 설명하려면 무엇을 저장할까? | 015의 현재 판단 가능 이유 195개 중 14개가 무너졌다. 032의 배포 HTML 표본은 12참조 중 유지 9·교체 2·보류 1, 같은 목적의 배포 링크 자체 변경은 5/12였다. 023의 옛 이유 복원은 주소·이유 3/18→판·근거 추가 5/18→변경관계·시점 추가 15/18이었다. 055의 옛 답은 0/4→2/4→4/4로 재생했지만 다음 판 판단은 세 보기 모두 0/4였다. 059·063의 배포판과 보고만으로 실제 소비판은 대개 미확인, 067은 Debian·천문 원실행 0/8·유효한 보기 비교 0/24였다. [032 근거][correct32] · [067 모집 원장][base67] | 주소, 당시 문구, 실제 읽은 입력, 현재 재판정에 필요한 입력을 분리해 보관량을 비교한다. |
| 검색이나 첫 링크를 좁히면 충분한가? | 040의 세 묶기 방식이 보존한 조건 수는 8·6·8이었다. 060의 용어 확장은 후보 있는 요구를 기존층 0/8→4/8, 새 층 0/4→2/4로 늘렸지만 고유 28쌍에서 두 조건의 공동 완결은 0이었다. 064는 6/11 첫 주소와 표시량을 바꿨지만 공동 확인은 양쪽 0/11이었다. 068의 36경로는 적격 둘째 열람 0, 요구 12건의 공동 확인 0이었다. 고정 시험 기대 일치 9/16은 별도 실행군이다. [068 결과][base68] | 후보 발견, 첫 도착점, 그 창 안의 조건별 증거, 실제 동작을 서로 연결해 측정한다. |

## 새 결과의 근거와 과도하게 읽기 쉬운 부분

### 069 · 일반 검색과 관계 검색에서 실제로 바뀐 선택

일반 검색은 Inkscape의 기존 TreeView 제목과 바인딩이라는 구체적인 수정 위치를 찾았다. 관계 검색은 Chime 같은 말단 장치에서 중간 장치의 요청 수락과 실제 설정 변경을 분리해 확인할 관점을 얻었다. 같은 원장에는 결정 트리의 ‘leaf’를 물리 장치로 오독하기 쉬운 반례와, 원리 설명에 있어도 대상 장치의 제어 기능은 제공하지 않는 경우가 함께 있다. JupyterLab의 완료 표식은 개발자가 이미 검토한 대안이었고 후행 PR은 검색 적중에 넣을 수 없다. Chime 신고자가 장치를 이미 반품했다는 발언은 열린 이슈가 곧 지금 선택할 기회라는 가정을 깨뜨린다. [조건별 판독][j69] · [사후 당사자 기록][discussion69]

모집 75행에서 관측 문제 3쌍, 최초판 엄격층 0쌍이다. 반환 90자리에는 고유 URL 76·계보 52개가 있었지만 대표로 직접 읽은 반환 URL은 27·계보 18개였다. 최소량으로 센 최종 26원저작에는 문제 3·선별 6·반환 신규 16·사후 분야 1이 섞인다. 26을 검색이 찾은 새 원전 수로 쓰면 과대계상된다. 판정 90행은 모두 `confirmed_fit=false`면서 분류 64행이 ‘미확인’이다. 관측 3문제에서 확정 적합이 없었다는 것까지가 결론이다. 검색 18+최초 접근 30+추가 접근 10=58회이고 A 25·B 33회다. 같은 최초 열람 상한만으로 효율의 우열을 말할 수 없다. [모집][f69] · [원순위][ru69] · [직접 독해 분해][cnt69] · [비용][cost69]

### 070 · 한 질문이 후보를 좁히는 경우와 효과를 잴 수 있는 경우

64건에서 최초 본문 56건을 복원했다. 주 12·진단 12건의 원글과 댓글 103개, A/B 보기 48개가 연결된다. 진단 RG1840에서 ‘숨김 속성’과 ‘ignore 규칙’에 따라 살필 옵션이 달라졌다. A도 원래 두 후보를 조건부로 제시했다. 같은 댓글의 성공 표현은 새 값과 독립된 정답이 아니다. RG1808과 jq2349의 중복 값은 권고 방향을 그대로 뒀고 PAN7113에서는 연구자가 고르지 않은 필드의 작성자 반례가 설명을 바꿨다. [최초판 모집][en70] · [보기][v70] · [후속 사건][events70] · [결과행][out70]

원장의 35결과행 가운데 사례는 24개다. 별도 비교와 반사실 11행을 빼면 신규 1·중복 2·그 밖 21이고 엄격 정오 변화는 24행 모두 관측 불가다. 질문 제안 8·생략 16은 연구자의 선택이다. 기술적으로 오탐 판별이 가능했던 2건 모두 실제 열람 예산을 넘었다. 실제 PINS의 66개 근거 연결은 계획 예산 열이 모두 참인데 실제 준수 열은 38개 참·28개 거짓이다. 후대 정보 비노출과 실제 예산을 함께 지킨 것은 주 2·진단 5건이었다. ‘오탐 0/2’를 모든 질문에 적용하거나 응답 없는 사례를 효과 0으로 넣을 근거가 없다. [원래 근거와 실제 예산][pins70] · [분모 정의][scope70] · [집계][sum70]

### 071 · 과거 재계산에서 이득이 난 조건

전사 4개와 기후 관측소 자료 4개의 발췌에서 파생 입력을 만들었다. 주 변경 22쌍에서 답 변경 8, 추천 이유 변경 3, 근거 연결 변경 14였다. 항목이 나타내는 현상은 겹칠 수 있다. A0는 주소와 짧은 이유, A1은 판·파일 목록과 지문·옛 답 추가, A2는 실제 처리한 조각·선택 설정·출력 연결까지 저장했다. 주 22쌍의 옛 입력 재계산 정답은 원본 보존 시 4·20·22, 소실 시 0·0·22였다. 나머지 재계산 행은 보류였다. A1과 A2의 옛 문구 표시는 각각 44/44였다. A1은 설정이 남지 않은 두 건에서 문구를 내보이면서 재계산은 못 했다. A2에서 조각을 지운 LOSS01도 재계산을 보류했다. [짝과 조건][pairs71] · [판정 원장][jud71] · [실행 기록][runs71]

세 보기의 현재 계산은 각각 44/44였다. 코드가 모든 판독기에 다음 주소를 인자로 주고 그곳에서 현재 자료를 실제로 열었다. 이 수치는 다음 주소를 발견하거나 여러 후보 중 해당 원전이 가장 적합함을 입증하는 성능으로 쓸 수 없다. 자료 조사 28건 중 24건은 직접 열람, 기후 상세 4건은 발행사 본문의 색인 발췌다. 288개 비용 행에서 보기별 96개 저장 페이로드의 중앙값을 다시 계산하면 162.5·995.5·3,973.5 B다. 인계에는 각각 162·995·3,973 B로 정수 표기됐다. 실행 원장의 처리 비용은 작은 로컬 실험의 비용이고 실제 발행사 전송량은 미측정이다. [주소를 넘기는 비교 코드][code71] · [판독기][storage71] · [비용 원장][co71] · [수용·접근 범위][acc71]

### 072 · 상위에 든 문서와 보인 절의 증거

보류 6×20=120쌍을 다시 세면 동종 부분 적격 6, 원거리 전이 14, 반박 12, 무관 88이다. 직접 적격은 0이라 직접 후보 회수율은 산출할 수 없다. URL에서 시작해 원문을 여는 L은 상위 3에서 부분 0/6·원거리 0/14, 카드만 쓰는 I와 카드 뒤 원문을 여는 H는 각각 1/6·1/14였다. 두 방법이 찾은 것은 각각 O02/W02와 Z04/W06으로 동일하다. 짧은 이름·목적만 남긴 보조 P는 다른 Z03/A04를 찾았다. W06의 다른 절에는 날짜 표현이 있지만 H가 실제 보여 준 절은 우→좌 표 방향이었다. 반대로 H는 O03/W02의 순위를 올리면서 그 절에서 직접 쓸 수 없다는 근거를 보여 줬다. [120쌍 판정][q72] · [상위 원순위][rk72] · [표시 원장][fetch72]

**‘공동 충족 0, 반박 1, 기권 53’의 추적 범위는 고쳐 읽어야 한다.** L/I/H 18경로의 최종 54슬롯을 실제 표시·판독 ID로 결합하면 개별 메모가 있는 것은 H 5·L 1·I 0이다. 그 6개 메모는 부분 근거 1·직접 반박 1·보류 4개다. 나머지 48자리는 판독 메모에 대응되지 않는다. 생성 코드는 반박 이외를 기권으로 처리하고 잘못된 채택을 항상 거짓으로 넣는다. 출력 표의 충족 건수도 0으로 고정한다. 연구자가 모든 슬롯을 보았다고 보고했지만 54개의 독립 판독 또는 양성을 판별하는 채점 결과로 재검증할 수 없다. 본실험 뒤의 CLI 양성 대조 X01은 URL만으로도 필요한 절에 도착한 별도 1건이다. [개별 판독 6행][slot72] · [기본 판정 코드][report72] · [출력 표 생성][reportline72] · [별도 양성 대조][ctrl72]

카드 구축은 원문 20회·2,087,664 B였다. 보류 6건의 빈 캐시에서 건당 L은 28,260 B, I는 0 B, H는 485,044 B를 전송했다. L은 6요구 모두 동률에서 같은 A07로 시작했다. 관측 평균을 같은 빈 캐시 요청에 반복 적용하면 I와 L은 HTTP 횟수로 5회에서 동률, 누적 본문 바이트로 약 74회에서 순서가 바뀐다. 즉시 반복 조건에서 L의 추가 HTTP는 0이었다. 전체 수치 49회·완전 응답 48회는 연구자가 기록한 빈 캐시와 반복의 라이브 접근이다. 카드 제작자의 실제 활동시간·자연 요청량·개방 웹 검색비용은 관측하지 않았다. [구축·요청별 비용][cost72] · [재생 규칙][rc72]

## 결과가 어긋나는 지점과 PLAN#18

| 판정을 달리할 불일치 | 현재 설계에서 쓸 수 있는 결론 | 결론을 바꿀 다음 관측 |
| --- | --- | --- |
| 관계어는 다른 분야의 원리를 노출했지만 대상의 종류를 지우자 같은 단어의 다른 의미를 찾았다. 좁힌 절이 오히려 추천을 반박하기도 했다. | 사용자 목적과 보존 조건, 동작의 주체·대상, 원문이 실제 지지하는 범위를 함께 반환할 후보로 둔다. | 같은 예산에서 대상·역할을 복원한 질의만 추가한 적용 가능 선택이 있는지, 직접 적격이 있는 자료집에서 표시창이 이를 지지하는지 본다. |
| 후속 정보가 조건부 대안을 하나로 좁혔지만 틀린 단정이 옳아졌는지와 질문의 비용은 측정하지 못했다. | 처음부터 조건부 링크 두 개를 주는 안, 하나를 권하는 안, 한 가지를 묻는 안을 보존한다. | 한 필드의 두 값과 독립적인 결과가 있는 대조와 원 요청을 분리해 비교한다. 질문하지 않아도 같은 행동이 나오는 경우도 센다. |
| 055의 다음 판 판정 0/4와 071의 현재 계산 44/44는 서로 다른 입력에서 나왔다. 072에서도 긴 카드는 일부 회수를 늘리지만 요청량에 따라 비용 순서가 바뀐다. | 원본의 옛 상태와 현재 상태, 새 후보를 찾는 비용, 후보 집합을 충분히 살폈다는 증거를 구분한다. URL과 짧은 설명에 요청 시 원문을 여는 방식도 비교에 둔다. | 승자 인용은 그대로인데 경쟁 후보가 생긴 두 판에서 존재·유일·우선 판정을 따로 검산한다. 구체 기능이 있는 요구에서 발행자 한 문장의 이득을 측정한다. |

| 다음 작업 | 고정된 선행 작업 | 독립적으로 판단할 제품 선택 |
| --- | --- | --- |
| 073 · web-pro | [069][h69] | Git 최초판이 있는 세 설계 제안에서 일반어·관계어·대상/역할 보존어로 찾은 링크가 실제로 서로 다른 선택을 여는가. |
| 074 · web-pro | [070][h70] | 단일 링크, 조건부 링크 두 개, 한 필드 질문 중 무엇이 추가 왕복 없이 올바른 다음 행동을 고르게 하는가. |
| 075 · codex-cloud | [071][h71] | 두 유한 목록에서 승자 발췌·판별 후보 기록·전체 판 중 무엇이 존재·유일성·공동 1위를 다시 입증하는가. |
| 076 · codex-cloud | [072][h72] | URL, 발행자 한 문장, 용도·동작 카드에 같은 요청 시 열람을 허용할 때 직접 쓸 기능·표시 근거·비용이 어떻게 달라지는가. |

네 작업은 서로의 자료·결과나 새 참가자 응답을 기다리지 않는다. 첫 두 작업은 공개 기록·원문을 조사하고, 뒤 두 작업은 고정판에서 실행·검사한다. 성공 사례와 기각된 사례를 모두 남겨 최종 설계자가 입력 필드·검색·저장을 독립적으로 채택하거나 교체할 수 있게 한다. [작업별 지시문과 완료 조건][next]

[r69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/RESULT.md
[r71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/RESULT.md
[product]: https://github.com/laadkke-arch/agentflow-open/blob/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853/docs/product/RESEARCH_BRIEF.md
[previous]: https://github.com/laadkke-arch/agentflow-open/blob/59e584cbc8fa3b266c60d6ac49f60cc30d9ff6d5/docs/workstreams/planning/REVIEW-17.md
[before]: https://github.com/laadkke-arch/agentflow-open/blob/320424d87f99e70c42eeb8cb7211467de27f2c2e/docs/automation/dot-control.json
[registry]: https://github.com/laadkke-arch/agentflow-open/blob/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853/docs/automation/dot-control.json
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/39cadb6ecdf62d0b21c0cce67834f2aef3bf6853/docs/RESEARCH_WORKFLOW.md
[h69]: https://github.com/laadkke-arch/agentflow-open/blob/616a1dab1b7d3ff8ff14210316c251cd5e5727b7/docs/workstreams/research/AF-RES-069/HANDOFF.md
[h70]: https://github.com/laadkke-arch/agentflow-open/blob/1a92715786d444f57976082329470a24e2a291b6/docs/workstreams/research/AF-RES-070/HANDOFF.md
[r70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/RESULT.md
[h71]: https://github.com/laadkke-arch/agentflow-open/blob/f8b3fc86b8eb6ba71e02866b48551245b5dbd95f/docs/workstreams/research/AF-RES-071/HANDOFF.md
[h72]: https://github.com/laadkke-arch/agentflow-open/blob/f77d2d68b3361df5a0fd70d5ea10df79b08b0f09/docs/workstreams/research/AF-RES-072/HANDOFF.md
[r72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/RESULT.md
[rc71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/reproduce.md
[rc72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/reproduce.md
[correct30]: https://github.com/laadkke-arch/agentflow-open/blob/3f77073d6294b739bb340b23e3c4c10640c5b08c/docs/workstreams/research/AF-RES-030/HANDOFF.md#L3-L7
[base65]: https://github.com/laadkke-arch/agentflow-open/blob/796e7127babc7440fa3b1a0f2a400fee67b33326/docs/workstreams/research/AF-RES-065/RESULT.md
[correct21]: https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/HANDOFF.md#L9-L17
[base66]: https://github.com/laadkke-arch/agentflow-open/blob/d736df8b3108451ab183ab0a09656a2d719bae12/docs/workstreams/research/AF-RES-066/RESULT.md#L13-L16
[correct32]: https://github.com/laadkke-arch/agentflow-open/blob/b4dcf0a1ca3f2066629869ac1a9347ad2f5717df/docs/workstreams/research/AF-RES-032/HANDOFF.md#L7-L16
[base67]: https://github.com/laadkke-arch/agentflow-open/blob/a4b0c47959aa234719f13b3fa6ee76e019c187c6/docs/workstreams/research/AF-RES-067/frame.csv
[base68]: https://github.com/laadkke-arch/agentflow-open/blob/9d46186a67d6dc328ad2f66539c8d630ee1d08b5/docs/workstreams/research/AF-RES-068/RESULT.md
[j69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/judgments.csv
[discussion69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/postseal-discussion-metadata.json
[f69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/frame.csv
[ru69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/runs.jsonl
[cnt69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/final-counts.json
[cost69]: https://github.com/laadkke-arch/agentflow-open/blob/fb710fce01052a5b907398e2da6840b59d3cfa08/docs/workstreams/research/AF-RES-069/evidence/costs.jsonl
[en70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/ENROLLMENT.csv
[v70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/VIEWS.csv
[events70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/EVENTS.csv
[out70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/OUTCOMES.csv
[pins70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/PINS.csv
[scope70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/DATA_DICTIONARY.md
[sum70]: https://github.com/laadkke-arch/agentflow-open/blob/30266f9354134b7aad33596b0acb96209876ce7d/docs/workstreams/research/AF-RES-070/evidence/ledger-summary.json
[pairs71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/pairs.csv
[jud71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/judgments.csv
[runs71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/runs.jsonl
[code71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/experiment/run.py#L72-L97
[storage71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/experiment/storage.py#L234-L260
[co71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/costs.csv
[acc71]: https://github.com/laadkke-arch/agentflow-open/blob/cb4931b38b3d75e98da1291628ec66966507be29/docs/workstreams/research/AF-RES-071/evidence/acceptance-evidence.json
[q72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/qrels.csv
[rk72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/ranks.csv
[fetch72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/fetches.jsonl
[slot72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/evidence/route-reading.json
[report72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/report.py#L103-L118
[reportline72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/report.py#L149-L156
[ctrl72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/evidence/counterexample-control.jsonl
[cost72]: https://github.com/laadkke-arch/agentflow-open/blob/330efd4489a2bac012ff9be603020076a424ec6f/docs/workstreams/research/AF-RES-072/costs.csv
[next]: NEXT_TASKS-18.json
