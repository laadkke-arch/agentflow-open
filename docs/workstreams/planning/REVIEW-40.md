# REVIEW-40 · 어떤 근거로 어디까지 링크를 권할 수 있는가

탐색기가 주는 링크는 사용자가 하려는 일에 따라 달라진다. 고정된 규격 절을 다시 읽을 때는 주소 하나로 충분했다. 같은 주소를 다른 판과 합쳐도 되는지 묻거나, 접수된 파일이 실제로 보관됐는지 묻는 순간에는 다른 근거가 필요했다. 기존 부품을 쓰면서 절약한 인시, 선례를 본 사람이 처음 바꾼 설계 선택에는 여전히 비교할 양쪽 기록이 없다. 제품은 전체 또는 선택한 구조와 그 목적을 받아 기존 완성품·기능·부품·타 분야 원리의 출전과 적용 이유를 돌려주는 탐색기다. 수집기·DB·Studio 입력 형식과 최종 검색 방식은 열려 있다. [제품 브리프][product] · [운영 규칙][workflow] · [주소 실험][r150] · [접수 사건][r158] · [노동 원장][r160] · [설계 전후 원자료][r157]

## 두 시점의 진행표

`work/planning@a61743a`에서 가장 최근 파일인 REVIEW-39를 먼저 읽었다. 그 검토가 사용한 통합판 `ff5a037`과 이번 시작판 `ded3420`의 진행표를 ID·상태·결과 SHA로 대조했다. 이전 154행 중 150행은 모든 필드가 같았다. 149·151은 RUNNING에서 BLOCKED, 150·152는 RUNNING에서 DONE으로 바뀌었다. 새 행은 157~160 네 개였다. 계획 시작 당시 새 DONE은 **150·152·158·160**이었다. 이 네 건의 원장을 읽고 웹 과제 여덟 개의 대상·질문·선행을 정했다. [직전 검토][r39] · [직전 진행표][c39] · [시작 진행표][start40]

| 2026-11-24 UTC 기준판 | 전체 | DONE | RUNNING | BLOCKED | 39차 이후 새 DONE |
| --- | ---: | ---: | ---: | ---: | --- |
| 직전 검토 `ff5a037` | 154 | 148 | 4 | 2 | 기준 |
| 기획 시작 17:10:37 · `ded3420` | 158 | 152 | 2 | 4 | 150·152·158·160 |
| 마감 재조회 17:37:45 · `82c3f51` | 158 | 154 | 0 | 4 | 위 네 건에 159·157 추가 |

두 번째 조회까지 바뀐 파일은 진행표 하나다. 159는 17:34, 157은 17:37에 DONE으로 기록돼 이 두 건의 인계·결과·원장도 추가로 읽었다. 마감판의 DONE 154건은 연구 152건과 연결 시험 2건이다. 중앙 `acceptance_evidence`는 154건 모두 빈 배열이다. 아래 표의 상태는 각 작업자가 인계한 판정이다. 018은 대화 한도 이후 인계 미커밋, 035는 기존 실행 종료, 149는 조사한 7주 중 세 경로를 모두 6항목씩 복원한 주가 0, 151은 최초 N0 응답·독립 가림 판독·원사용자 비용 증빙 미확보로 BLOCKED다. 149·151의 상태 변경은 진행표의 차단 사유로만 확인했다. [두 시점 차이][move] · [마감 진행표][end40]

| 새 DONE | 실제 인계 상태·고정 커밋 | 인계가 가리킨 결과판 | 출처 원장 행 / 작업자 기준 산입 고유 저작 |
| --- | --- | --- | --- |
| 150 · 참조 정정 | [REVIEW_READY · ff2c1fc][h150] | [e4086f5][r150] | [75 / 49][s150] |
| 152 · 발견과 재점검 예산 | [REVIEW_READY · ba038a0][h152] | [1334ae6][r152] | [97 / 66][s152] |
| 158 · 제출자에게 보이는 상태 | [PARTIAL · 53450ff][h158] | [981a82d][r158] | [113 / 66][s158] |
| 160 · 부품 도입의 노동 | [PARTIAL · 3e93d6c][h160] | [43a4c2f][r160] | [58 / 22][s160] |
| 159 · UI 문구의 실제 기능 | [PARTIAL · fd703cf][h159] | [dfd6feb · 검증 영수증 포함][r159] | [136 / 29][s159] |
| 157 · 선례 개봉과 개인 작품 | [PARTIAL · 82e0154][h157] | [b82bafd][r157] | [82 / 20][s157] |

여섯 작업의 등록 SHA는 각각 조회한 작업 브랜치의 끝과 일치했다. 이번 검토에서 GitHub 원장의 고유 저작·비교행·결측을 다시 셌다. 실행 수치는 각 작업자가 보관한 결과와 재생 영수증에 근거한다. 158·160이 한 원격 문서 검산과 150·152·157·159가 한 체크아웃 재생은 확인 범위가 다르다. 39차까지의 관측은 직전 REVIEW의 누적 검토를 이어받았다. [39차 검토][r39] · [152 검증][v152] · [159 검증][v159]

## 1~39차에서 이어지는 여섯 가지 판단

| 탐색기가 답할 질문 | 지금까지 확인된 근거 | 아직 결정할 수 없는 것 |
| --- | --- | --- |
| 모르던 원리가 실제 선택을 바꿨는가 | 002는 발견 경로와 빌린 부분을 남겼다. 010은 분야 단서로 원리 7군을 찾았으나 033은 단서 없이 본 144쌍에서 당시판 지지 0이었다. 022의 미인지→결정 변경→시행은 0/24, 141의 Matplotlib 작성자는 링크 전에 외부 타입 스텁을 알았다. 145는 독립 초안 0/16·유효 검색 짝 0/8이었다. 153의 전후 후보 11행에도 엄격쌍은 없었다. | 원리를 설명하는 링크, 독자가 그것을 처음 알았다는 증거, 저자 자신이 고친 선택과 구현 결과는 따로 필요하다. |
| 부분 구조에 문맥을 얼마나 붙여야 하는가 | 020은 주장 72/73을 전달했으나 충돌을 모두 푼 묶음은 2/16이었다. 119의 도표 6건에서 요구만으로 정확 0, 이웃 또는 직접 참조를 준 보기에서 각각 3이었다. 103은 외관 10/10을 지키고도 텍스트 선택을 잃었다. 107의 단일 발생 편집은 공유 정의 0/6·위치 지정 6/6. 144에서는 성공 종료 뒤에도 날짜 열이 Text였다. 148의 유효 비교는 0/6이었다. | 선택 위치, 보존할 값, 다음 소비자 중 무엇이 답을 가르는지 요청별로 확인해야 한다. |
| 자료를 더 찾거나 묶으면 무엇이 표시되는가 | 040은 8요구에서 완전 적격 0/8, 묶기별 부분 근거 8 대 6이었다. 044의 8풀에서는 두 방법이 같았다. 118은 충돌과 일부 지지를 함께 숨겼고 142는 잠정 신규층 72자리가 비었다. 146의 4요구×12후보는 직접 0·일부 15·충돌 14·미확인 19. 검토 폭 3→8의 추가 표시 세 건은 모두 한 요구의 5·7·8위였다. | 발견 실패, 낮은 순위, 적용 근거 부족과 표시 보류를 구별해야 한다. 여러 단계의 서로 다른 부분 지지가 완전한 답 한 건인지도 별도다. |
| 가벼운 저장으로 어떤 답을 복원하는가 | 003은 짧은 메모가 충분한 경우와 정정이 필요한 경우를 찾았다. 023의 18사건은 허용 병합 5·정정 등 9(실제 오병합 수정 3)·기타 4였다. 055는 과거 4/4·다음 판 0/4, 071은 절·설정으로 과거 22/22를 복원했다. 075는 전체 후보 없이 단독·공동 1위 주장을 각각 16/16 보류했고 147은 당시 증빙이 있는 안에서 과거 질의 112/112에 답했다. | 북마크를 여는 데 드는 정보와 현시점 적합성·후보 간 우선순위를 설명할 정보가 다르다. |
| 언제 링크를 다시 읽을 것인가 | 019의 같은 신호는 엄격 7쌍 중 사건 3·대조 3건에 울렸다. 024에서 정기 확인은 무효화 11/11, 신호 확인은 8/11. 후자는 원문 108개를 덜 읽고도 5,672,462바이트를 더 받았다. 135는 같은 README 아래의 기본 출력 변화를, 143은 수치 변화 양성 없이 공개 진입의 실패·회복을 봤다. 147의 마지막 주소 답 대조는 현 요청 96건 중 오승인 40·오거절 32·정답 24였다. | 열람 횟수 외에 요청 시점·판·전송량·대기·재검사 비용이 필요하다. 상시 크롤러나 고정 주기는 미결정이다. |
| 사용자나 팀 노동이 얼마나 줄었는가 | 021의 두 절 예산에서 충분한 근거는 주소만 6/23·맞춘 절 14/23. 034의 한 단계는 380→57초, 전체는 849→847초였다. 140이 더한 둘째 절 7개로 새로 해결한 핵심 조건은 0. 156은 Django 호환 어댑터 일부 제거와 하류 수정, pandas의 수정 패치를 확인했으나 시간 원장 12행 모두 실제 인시 미확인이었다. | 더 빨리 읽기, 실제 구현·납품, 후속 지원까지 포함한 순노동 각각에 별도 비교가 필요하다. |

39차의 직접 실행 두 건도 경계를 정한다. 154의 Paperless-ngx v2.2.1은 주 실험 입고 성공 10/16, 성공 뒤 명시 원본은 10/10, 기본 다운로드의 동일 바이트는 6/10이었다. OCR을 생략한 서명 텍스트와 입고에 실패한 서명 이미지는 다른 입력이다. 155는 20경로×2회 중 실제 실행 38행에서 출력 문자열이 같아도 AST 속성이 다를 수 있음을 보였다. 자연 대조 0/4, 한 X05에서 파생된 구성 대조로는 사용자에게 어떤 문맥을 일률적으로 요구할지 정하지 못했다. 153의 ‘먼 예시’도 연구별로 독창성·품질 평정과 유용성 평정의 방향이 달랐다. 156의 pandas 후속 귀속은 P5/P8이며 보고된 실행시간·13시간 시차를 노동량으로 옮길 수 없다. [153 결과][r153] · [154 결과][r154] · [155 결과][r155] · [156 결과][r156]

이전 수치의 정정도 유지한다. 114가 충돌로 분류한 138/144쌍은 118의 명시적 반박 기준으로 충돌 7·미확인 131이고 나머지 6은 일부 지지다. 119의 M3994 원형 MG 좌표 y는 11.71875, 공유 변경 뒤는 275다. 136의 고유 면 9개, 열람 10회, 답–면 연결 16쌍은 서로 다른 분모다. [39차 누적 근거][r39]

## 새 결과가 지지하는 주장과 결론이 갈리는 곳

### 150 · 같은 링크를 기억하는 일과 같은 대상임을 증명하는 일

자연 사건 12와 안정 대조 4에서 주소별 메모(A), 공통 키·고정판(B), 범위·방향·정정 이력(C)을 비교했다. 16쌍에서 동일성의 **값과 근거가 함께 맞은 수는 7·9·15**였다. A는 실제 동치 6쌍을 분리했고, B는 Frankenstein·Darwin의 다른 판 등을 포함해 6쌍을 잘못 합쳤다. C도 Atom/Pulsar가 별개라는 값은 맞추고 원 발행자의 보관 근거를 반환하지 못했다. 안정 절 네 건에서는 주소 하나만으로 두 시점·네 조회 32/32에 답했지만 두 주소의 동일성을 증명하라는 네 질문에서는 모두 근거를 잃었다. 사용자가 원문을 읽으려는지, 동일 판임을 입증하려는지에 따라 필요한 기록이 갈린다. [사건 원장][ca150] · [응답 원장][a150] · [결과][r150]

정상 A/B/C의 성공 쓰기 38/52/60회와 논리 바이트 10,156/13,987/16,652는 작은 SQLite 재생값이다. C의 오답 네 건을 취소해 돌려놓은 시험은 의도적으로 잘못 넣은 관계 두 개에 대한 결과다. Open Library #6371의 피해 보고와 운영자 설명은 읽었으나 거래 42049802가 OL14863262W의 판 24→26을 건드렸는지, 뒤에 추가한 별개 필드가 실제로 어디서 사라졌는지는 원 revision을 읽지 못해 비었다. 동시 편집·실제 편집 시간도 추론할 수 없다. 161은 바로 이 거래 조인과 다른 실제 수정 이력을 조사한다. [쓰기 비용][cost150] · [150 인계][h150] · [Open Library 당사자 보고](https://github.com/internetarchive/openlibrary/issues/6371)

### 152 · 새 항목을 더 많이 발견하는 정책과 더 빨리 발견하는 정책

Cloudflare·Mozilla·curl에서 신규 26건 중 25건이 지정 채널에 창 안에 들어왔다. 기존 상태 전이 13건, 안정 대조 8건은 다른 분모다. 182일 유보 구간의 신규 15건에서 신호 중심(S)·희소 공급원 순번 보장(F)은 14건, 정기 확인(P)은 13건, 요청 시 확인(O)은 10~14건을 발견했다. 높은 예산·주류 수요에서 발견 지연 중앙값은 P 27시간, S 57시간이었다. 둘 다 찾은 13건만 놓아도 27 대 51시간이다. 반면 낮은 예산·희소 수요의 같은 13건은 92.1 대 27시간이었다. 희소층을 제거하면 낮은 예산·주류 수요의 낡은 추천 시간도 P/S 136/70에서 22/109로 역전했다. [사건][e152] · [정책별 원장][m152] · [민감도][sen152]

높은 예산·희소 수요에서 O의 기본 결과는 **309/364**다. 알려진 과거 목록 전체를 같은 1회 비용으로 열 수 있게 바꿨을 때 나온 **350/364**를 현장 기본 성적으로 읽으면 안 된다. 통지 시각과 실제 이용 시각에도 차이가 있다. 11월 3일자가 붙은 Wrangler 항목의 production 편입은 다음 해 4월 1일이었다. 과거 공개 웹에서 실제로 보이기 시작한 시각과 고객 집단별 첫 사용은 미확인이다. 유보 회복 2건도 모든 재생에서 직접 포착 0/2였다. S/F가 사후 보고 2/2를 읽은 사실은 그와 양립한다. HTTP 표본 9시도 중 원래 호스트 3건은 터널 단계에서 막혔다. 10만·100만 건의 병목과 사람 판독 시간은 모형에 남는다. 162는 고객 집단의 당시 관측을 조사한다. [기본·변경 예산][r152] · [전송 표본][http152] · [Wrangler 편입 PR](https://github.com/cloudflare/cloudflare-docs/pull/26259)

### 158 · 접수와 원본 보관, 통지 수신이 갈린 실제 사건

검색 표시 104행·고유 후보 99개 중 Paperless 첫 12개에 적격 10, Dataverse는 첫 12개에 2여서 24개로 넓혀 적격 4였다. 후자에는 큐레이터 집합 보고가 한 건 있다. 두 제품을 합친 자연 모집 자리는 36개, QA·보충 등을 포함해 단계별로 판독한 사건은 28개다. Paperless 구판의 API 설명은 OK, 당시 구현은 작업 ID를 반환했다. #2435는 HTTP 200과 UUID 뒤에 처리 실패를 보고했고, #2667은 오류가 뜬 뒤에도 문서가 보였다고 했다. #11004에서는 이전 문서 ID 5와 중복 거절이 연결됐지만 다른 사건에서는 휴지통·삭제 뒤에도 중복 신호가 나왔다. Dataverse #9425에서도 ZIP을 그대로 저장한다는 응답 뒤 목록에 없었다는 보고가 남았다. 접수가 성공했다는 응답만으로 최종 레코드를 안내하기 어렵다. [모집 원장][fr158] · [사건 연결][tr158] · [Paperless #2435](https://github.com/paperless-ngx/paperless-ngx/issues/2435) · [Dataverse #9425](https://github.com/IQSS/dataverse/issues/9425)

154의 성공 입력에서 원본이 회수됐다는 실행과 158의 공개 제출 사건은 모순되지 않는다. 158에서 별도 알림의 실제 수신, 원본 동일 바이트, 최종 공개판은 **세 열 각각 28/28 미확인**이었다. #2573에는 당사자의 재제출 성공 보고가 있으나 원본 지문·단일 레코드까지 이어지지 않는다. 다섯 사건의 A/B/C 보기 15행에서 A·C는 각각 한 절, B는 두 절이다. 추가 절이 답할 수 있는 내용은 보였지만 설명 자체의 효과와 더 읽은 효과, 사용자의 이해시간은 분리해 측정하지 않았다. 163은 실제 통지와 제출자 답장이 같은 공개 사건으로 남는 자료에서 ‘인지했다’는 문장의 근거를 찾는다. [상태 28행][st158] · [답 비교 15행][ans158] · [154 실행][r154]

### 160 · 실제 인시 집계와 재사용으로 절약한 인시

SEL 보고서에서 기술·기술관리 단계 집계 10개 프로젝트를 확인했다. GOESIM 이식은 **1,061.9인시**이며 컴파일 405.7, 시험 307.9가 그 안에 든다. 단계별·활동별 두 분해의 합이 각각 같은 1,061.9다. 따로 제시된 FORTRAN 경로 198~220인일은 추정이다. SAMPEXTS 2,038시간과 POWITS 11,677시간도 임무·성능 및 숙련 조건이 달라 차이를 재사용 효과로 계산할 수 없다. EUVEDSIM의 20,775시간·121주는 생략된 인수시험을 보정한 값이며 원래 단계표 17,805시간과 구분했다. [시간 원장][tm160] · [보정 기록][corr160] · [이식 원보고서](https://ntrs.nasa.gov/api/citations/19910006458/downloads/19910006458.pdf)

**인계문의 ‘소프트웨어 12 비교 후보’는 원장 기준으로 정정한다.** C1~C7과 C12가 소프트웨어 8행, C8~C9는 교통 2행, C10~C11은 기록관 2행이다. 이 8행도 서로 독립된 여덟 실험을 뜻하지 않는다. 동등한 소프트웨어 양측 실측쌍은 0이다. 유일한 차이 4.25시간/10점은 OSUL 촬영·편집의 기술통계이며 표본 및 시간기록 방식이 달랐다. 소프트웨어 납품 원장 16행 모두 최초 배포 뒤 90일치 노동이 미관측이다. GitLab·NTRS의 정식 모집 순서를 복원하지 못했고 원보고서 3개에서 확인된 독립 노동 관측 계보는 2개다. 164는 같은 과제의 실제 구현 경로가 두 개 있는 연구부터 모집한다. [인계 문구][h160] · [열두 비교행][co160] · [납품·후속 관측][de160]

### 마감 중 추가된 159 · 같은 문자열이 같은 기능인지

GIMP 3.0.6·Inkscape 1.4.3에서 자연 문구 12쌍과 단일 대조 4건을 골랐다. 자연 24호출×2언어 48자리에서 문구와 목적만 준 보기 및 무관한 이웃을 더한 보기는 유일한 기능 0/48이었다. 실제 원문 위치를 주면 46/48, 코드에서 읽은 소비 역할을 주면 48/48, 직접 번역 키로는 42/48이었다. 단일 대조는 문구만으로 8/8이었다. 같은 ‘All visible layers’가 캔버스 크기 조정 대상 또는 선화 감지의 입력을 뜻했고, 독일어 표기는 같았다. 실제로 존재하는 잘못된 문맥 키로 조회해도 48자리 중 38개는 올바른 문맥과 같은 문자열을 돌려줬다. 기능이 필요한 사용자에게 번역 문자열의 일치만 제시하면 이 차이가 사라진다. [실제 호출][call159] · [사전 판정][pred159] · [반례][cx159]

역할 한 필드가 48자리를 가른 결과는 고정판을 이미 판독한 한 작성자의 기술적 역참조다. 같은 GIMP enum의 두 소비자에서는 위치만으로 부족했고, 교환한 무관 이웃을 쓴 보조 비교에서는 예산 안 17번 중 9번 잘못된 유일 판정이 나왔다. 두 번의 주 재생은 각 328조회였다. 56개 문맥 조회 중 54는 활성 번역, 한국어 2개는 fuzzy 표기로 원문이 반환됐다. 공식 GIMP 배포 tar·원배포 MO의 취득, 실제 GUI의 표시, 추가 질문 횟수·사용자 이해는 미확인이다. Inkscape는 서명 소스 tar와 Debian MO까지 확인했다. 이 후속 실행은 해당 파일이나 실제 사용 증거가 확보된 뒤에 가치가 있다. [검증 영수증][v159] · [결과와 미확인][r159]

### 마감 중 추가된 157 · 받은 파일에서 확인할 수 없었던 사람의 변화

153에서 크기만 확인했던 Sketchy 파일럿 CSV의 **15,062,721바이트, 196행**을 이번에는 두 새 체크아웃에서 같은 지문으로 읽었다. 참가자×완료 참조 57개, 같은 완료 참조의 추가 행 139개, 서로 다른 역할의 두 배열이 같은 행 62개가 있었다. 파일에는 과제 키, 실제 개봉 시각, 직전·직후의 별도 저장판이 없다. 같은 배열 62개를 사람의 ‘무변경 62회’로 바꿀 수 없다. 판독 원장 34행은 계획 자리 24·파일럿 진단 4·저자 선정 6이다. 두 핵심 연구에서 목표로 둔 **8자리 중 엄격 연결 0**, 실제 개인 변화율의 분모는 0이다. [전후 원장][pa157] · [파일럿 계수][snap157] · [결과][r157]

Sketchy 저자 DB, Delft ZIP, VIS OSF 파일의 내용은 여전히 미취득이다. Fig. 7 네 예에서 판독한 부분은 저자의 레이블·캡션으로, 원행·픽셀이나 작동하는 인터랙션으로 이어지지 않았다. B09는 중간 그림이 어떤 자극을 고를지 먼저 결정했고 VIS에는 이미 비슷한 안을 그렸다는 진술도 있다. 닮은 결과에서 영향의 방향을 추론하기 어려운 구체적 이유다. 원자료 20저작 중 애니메이션 두 건은 편집 타임라인의 제작 변경이며 스토리보드 그림 원판으로 한정하면 18저작이다. 책·제작판의 실제 변화와 개인의 동기를 분리해 인용할 수 있다. 개인 효과에 대한 다음 검사는 공개 비식별 사건·영속판과 시계가 확보될 때 별도로 성립한다. [취득과 실패][ar157] · [대조 원장][ct157] · [157 인계][h157]

## 바로 시작할 웹 조사 8건

아래 ID의 선행은 모두 기획 시작판에서 이미 DONE이었다. 같은 회차끼리 자료·판독자·실행 결과를 주고받을 필요가 없다. 특히 166은 작업 배정 순서를 예측하는 공개 규칙, 167은 두 구현 사이에서 보존된 파일 속성을 본다. 두 과제의 질문과 단위는 157의 참여자·작품이나 159의 UI 호출과 별개다. 각 작업의 고유 브랜치·소유 경로, 세부 질문 7개, 원전 22~24개 하한, 필수 결과표 세 개, 반례·커밋·인계 절차는 개별 brief에 들어 있다. [배정용 JSON](NEXT_TASKS-40.json)

| 작업과 고정 선행 | 모집할 자료와 판정 단위 | 이번 답이 바꿀 추천 |
| --- | --- | --- |
| 161 · 정정된 참조 / 150 | Open Library·Wikidata의 실제 편집 거래. 같은 객체에서 병합 전·중간 편집·복구 후의 대상 필드와 무관한 필드를 대조한다. | 옛 주소 한 개를 주는 경우와 관계가 복구된 특정 판을 함께 줘야 하는 경우. 42049802와 작품판의 연결이 확인되지 않으면 따로 남긴다. |
| 162 · 단계적 제공 / 152 | Workspace와 GitHub의 두 출시 창. 공지와 대상 집단별 마지막 부재·첫 사용의 시각 구간을 비교한다. | ‘이날 발표됨’과 ‘이 집단에서 쓸 수 있음’에 각각 어느 링크가 필요한지. |
| 163 · 제출자 통지 / 158 | Debian·GNU의 공개 티켓. 종료 메시지와 원 제출자가 인용한 회신을 같은 통지에 연결한다. | ‘종료 시 통지를 생성한다’, ‘이 건에서 발송했다’, ‘제출자가 내용을 확인했다’ 중 자료가 지지하는 문장. |
| 164 · 비교 가능한 노동 / 160 | 같은 소프트웨어 작업을 다른 구현 경로로 수행한 연구. 과제·배정·인수 수준·노동 단위·탈락 분모를 맞춘다. | 어느 단계의 인시 차이를 알려줄 수 있는지, 비용 문장을 보류해야 하는지. |
| 165 · 예제의 파일별 배포 / 150 | Debian·Fedora의 패키지 심사와 실제 배포 목록. 코드·그림·글꼴 각각의 출전과 포함·교체 이유를 추적한다. | 작동 원리를 읽는 링크와 특정 자산을 배포한 근거 링크가 갈리는 조건. |
| 166 · 타 분야 대기열 / 145 | Kueue·Slurm 요청의 작업 두 개를 고정한다. 선착순·당시 정책·도서관 예약·관측시설 배정의 예측을 봉인하고 공개 후속 결과와 대조한다. | 다른 분야 원전이 실제로 다른 다음 선택이나 깨지는 경계 조건을 드러내는 경우. |
| 167 · 두 구현 사이의 교환 / 155 | MusicXML·IFC의 공개 교환 사건. 송신판·수신판과 같은 파일의 음표·관계·속성값을 단방향과 왕복으로 추적한다. | 사양 링크만으로 답할 수 있는 질문과 두 구현·교환물 링크가 필요한 질문. |
| 168 · 겹치는 근거의 출전 / 160 | CSS 레이아웃·타이포그래피의 브라우저판별 주장 16자리. MDN·Can I use의 셀과 실제 공개 관측을 거슬러 올라간다. | 여러 사이트가 같은 원자료를 전할 때 대표 원전 하나로 충분한지, 별개 관측이나 반례를 덧붙여야 하는지. |

웹 작업자가 이미 공개된 사건·규약·실행 기록을 읽고 판단한다. 대량 원장 대조나 소프트웨어 실행은 입력이 갖춰진 뒤의 Codex 작업이다. 예를 들어 157은 동일 참여자·과제의 공개 비식별 사건과 전후 판, 159는 당시 공식 배포물과 지문, 167의 왕복 검사는 동일 교환 파일·양쪽 버전·판독할 속성값이 선행한다. 162의 과거 고객 활성 시각이나 164의 누락 인시는 현재 제품 실행으로 복원할 수 없어 당시 기록이 필요하다. 이들 후속 검사는 위 여덟 건의 시작 조건에 포함되지 않는다. [157 재개 입력][h157] · [159 재개 입력][h159] · [배정용 JSON](NEXT_TASKS-40.json)

## 결정을 가장 크게 바꿀 세 가지 불일치

| 불일치·약점 | 현재 근거로 내릴 수 있는 판단 | 다음 조사와 판정을 바꿀 관측 |
| --- | --- | --- |
| 원문들이 같은 대상을 가리키거나 말이 같아도, 필요한 파일·동작·근거 계보는 다를 수 있다. | 150의 주소 하나는 안정 절의 32개 조회에 충분했다. 같은 판을 증명하는 데는 실패했다. 159에서는 틀린 문맥으로도 38/48에서 같은 문자열이 나왔다. | **161·165·167·168**에서 각각 실제 복구 필드, 포함된 파일, 같은 교환물의 값, 독립 관측의 출전을 건넨다. 추가 근거를 줘도 답이 같거나 강한 한 원문으로 끝나는 대조를 같이 확인한다. |
| 제공자가 발표·처리한 시점과 당사자에게 실제로 일어난 일이 이어지지 않는다. | 152의 사후 회복 보고와 158의 접수 ID는 각각 서비스 회복의 직접 관찰, 사용자 통지 수신까지 입증하지 않는다. 157도 파일 전체를 받았지만 개봉과 직전 저장을 잇는 키가 비었다. | **162**의 같은 배포 집단에서 마지막 부재와 첫 사용, **163**의 같은 통지에 대한 원 제출자 회신이 확인되면 해당 사례의 문장을 높인다. 개인 설계 효과는 별도로 157에 명시한 시계·작품판이 확보돼야 한다. |
| 흥미로운 선례·줄어든 한 단계와 더 나은 선택·전체 절감 사이의 비교가 비었다. | 145의 유효 검색 짝은 0/8, 160의 동등 소프트웨어 노동쌍은 0이었다. 반면 조건과 값이 명시된 일부 기능 링크는 해당 조작의 차이를 설명한다. | **166**에서 사전에 서로 다른 예측을 낸 규칙이 같은 사건의 결과로 갈리면 그 조건을 추천할 수 있다. **164**에서는 같은 품질·기간의 양쪽 실측과 제외 노동의 범위가 확인될 때만 그 범위의 차이를 계산한다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/ded3420249a3d60ebbb578a8432cf262d3ffa7d7/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/ded3420249a3d60ebbb578a8432cf262d3ffa7d7/docs/RESEARCH_WORKFLOW.md
[r150]: https://github.com/laadkke-arch/agentflow-open/blob/e4086f5b8f58b1b8494ed6474547e34cd7bff567/docs/workstreams/research/AF-RES-150/RESULT.md
[r158]: https://github.com/laadkke-arch/agentflow-open/blob/981a82d6f15b15c213931c29e55d0e8e3d2c1b25/docs/workstreams/research/AF-RES-158/RESULT.md
[r160]: https://github.com/laadkke-arch/agentflow-open/blob/43a4c2fee6b48fa19f3bca026ef0a4dfd23805a2/docs/workstreams/research/AF-RES-160/RESULT.md
[r157]: https://github.com/laadkke-arch/agentflow-open/blob/b82bafda1355a6e5160b58db70019e5a8c6fa4d4/docs/workstreams/research/AF-RES-157/RESULT.md
[r39]: https://github.com/laadkke-arch/agentflow-open/blob/a61743ae3c5a8bdcccd4596b543684b0a3ba5d8c/docs/workstreams/planning/REVIEW-39.md
[c39]: https://github.com/laadkke-arch/agentflow-open/blob/ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8/docs/automation/dot-control.json
[start40]: https://github.com/laadkke-arch/agentflow-open/blob/ded3420249a3d60ebbb578a8432cf262d3ffa7d7/docs/automation/dot-control.json
[move]: https://github.com/laadkke-arch/agentflow-open/compare/ded3420249a3d60ebbb578a8432cf262d3ffa7d7...82c3f5133debf2b8c333ce542750db6b4340ce99
[end40]: https://github.com/laadkke-arch/agentflow-open/blob/82c3f5133debf2b8c333ce542750db6b4340ce99/docs/automation/dot-control.json
[h150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/HANDOFF.md
[s150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/sources.jsonl
[h152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/HANDOFF.md
[r152]: https://github.com/laadkke-arch/agentflow-open/blob/1334ae6cb6bf615664efcc17e54f9c95b69ea5d4/docs/workstreams/research/AF-RES-152/RESULT.md
[s152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/sources.jsonl
[h158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/HANDOFF.md
[s158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/sources.jsonl
[h160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/HANDOFF.md
[s160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/sources.jsonl
[h159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/HANDOFF.md
[r159]: https://github.com/laadkke-arch/agentflow-open/blob/dfd6feb005aabf0818d12cdf4e0e6a27345ab7f9/docs/workstreams/research/AF-RES-159/RESULT.md
[s159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/sources.jsonl
[h157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/HANDOFF.md
[s157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/sources.jsonl
[v152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/verification.json
[v159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/evidence/fresh-verification.json
[r153]: https://github.com/laadkke-arch/agentflow-open/blob/f92048ad779897a10fafaf2ca2ca84c975cd42c9/docs/workstreams/research/AF-RES-153/RESULT.md
[r154]: https://github.com/laadkke-arch/agentflow-open/blob/b19c8f966e3f5ae95c0f8714ebcd09122dabdc35/docs/workstreams/research/AF-RES-154/RESULT.md
[r155]: https://github.com/laadkke-arch/agentflow-open/blob/1c1e68c33507139561abe5160f6f29600ecb81ca/docs/workstreams/research/AF-RES-155/RESULT.md
[r156]: https://github.com/laadkke-arch/agentflow-open/blob/ef71cee3114731142a50b06eb63efb9d250b5934/docs/workstreams/research/AF-RES-156/RESULT.md
[ca150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/cases.jsonl
[a150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/answers.csv
[cost150]: https://github.com/laadkke-arch/agentflow-open/blob/ff2c1fc8786ba70a1432f1089f8f81288e43a61d/docs/workstreams/research/AF-RES-150/costs.csv
[e152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/events.jsonl
[m152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/metrics.csv
[sen152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/sensitivity.csv
[http152]: https://github.com/laadkke-arch/agentflow-open/blob/ba038a0aa589985d5f14549fa55f628f02fa151d/docs/workstreams/research/AF-RES-152/http-sample.csv
[fr158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/frame.csv
[tr158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/traces.csv
[st158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/state_checks.csv
[ans158]: https://github.com/laadkke-arch/agentflow-open/blob/53450ff704bb33a95090093f81c5762d4483d127/docs/workstreams/research/AF-RES-158/answers.csv
[tm160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/time-entries.csv
[corr160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/SCOPE_CORRECTION.md
[co160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/comparisons.csv
[de160]: https://github.com/laadkke-arch/agentflow-open/blob/3e93d6cdaaaa6213682da9d2588677c35b3f2517/docs/workstreams/research/AF-RES-160/deliveries.csv
[call159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/calls.csv
[pred159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/predictions.csv
[cx159]: https://github.com/laadkke-arch/agentflow-open/blob/fd703cfc31dcdf424c5302f33d841d2d8e00f9be/docs/workstreams/research/AF-RES-159/evidence/counterexamples.md
[pa157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/pairs.csv
[snap157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/evidence/pilot-snapshots.json
[ar157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/archive.csv
[ct157]: https://github.com/laadkke-arch/agentflow-open/blob/82e015434f375de7ca236611abbd848576261714/docs/workstreams/research/AF-RES-157/contrasts.csv
