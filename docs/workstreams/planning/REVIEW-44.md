# REVIEW-44 · 같은 이름의 링크로 실제 어디까지 약속할 수 있는가

개발자가 만들 소프트웨어의 전체 또는 일부와 그 목적을 주면, 탐색기는 재사용할 부품·서비스나 다른 분야의 원리를 찾아 **어느 부분에 왜 쓸 수 있는지** 원문 링크와 함께 돌려준다. 이번 결과에서 첫 링크를 실제로 가른 것은 기능명이 아니라 사용자가 끝까지 보존할 대상이었다. 자동완성에서는 창에 남을 문자열과 추가 검색 발행이 갈렸고, 메일에서는 큐 접수와 같은 호스트의 사서함 배달이 갈렸다. 이용자가 이미 쓸 수 있던 기능을 안다는 사실도 새 인터페이스의 필요성이나 절약한 노동까지 설명하지는 못했다. [제품 브리프][product] · [운영 규칙][workflow] · [자동완성 원요구][req189] · [메일 선택 조건][choice193] · [PEP 당시 대안][alt194]

**43차 이후 신규 DONE은 186~194 아홉 건이다.** 작업자 자체 판정은 186·191이 DONE, 나머지 일곱이 PARTIAL이다. 186은 같은 시험에서 두 엔진의 실제 반환 차이를 남겼다. 191은 특정 편집 결정과 판본을 잇는 문헌 조사를 마쳤다. 이번 배정은 **즉시 착수 가능한 웹 조사·설계 8건, 즉시 가능한 Codex 검사 2건, 195와 196의 실제 인계를 모두 기다리는 Codex 검사 1건**이다. [진행표][control] · [독립적으로 전달할 지시문 11건](NEXT_TASKS-44.json)

## 어느 변경을 검토했는가

계획 브랜치의 가장 최근 누적 검토는 `work/planning@b7c9bb5`의 REVIEW-43이었다. 그 문서를 먼저 읽고, 43차 기준 진행표와 요청 시점 통합판을 ID·전체 필드로 비교했다. 기존 184행 중 186만 RUNNING에서 DONE으로 바뀌었고 다른 변경 필드는 결과 SHA와 최근 진척 시각뿐이다. 187~196 열 행이 추가됐으며 삭제는 없다. 아래 아홉 건만 중앙 결과 SHA와 작업 브랜치 끝이 일치함을 확인하고 소유 경로의 HANDOFF·RESULT·자체점검·원장을 읽었다. 이전의 세부 결론은 REVIEW-43에서 이어받았다. 195·196은 중앙 행과 배정문으로 범위를 확인했다. [이전 누적 검토][r43] · [이전 진행표][prevctl] · [통합판 차이][delta]

| 진행표 기준 | 전체 행 | DONE | RUNNING | BLOCKED | 새로 검토한 범위 |
| --- | ---: | ---: | ---: | ---: | --- |
| 43차 · 0f6765d | 184 | 179 | 1 | 4 | 비교 기준 |
| 44차 · 0502786 · 2026-11-24 20:20:41 UTC 커밋 | 194 | 188 | 2 | 4 | 기존 행 186과 새 행 187~194의 완료 |

DONE 188건에는 연구 186건과 연결 시험 2건이 있다. 이들 모두 중앙 `acceptance_evidence`는 빈 배열이다. 각 작업의 구체적인 증빙은 고정된 파일로 찾아가야 한다. 018은 대화 한도 후 인계 미커밋, 035는 실행 종료 후 인계 미확인이다. 149는 조사한 7주 중 세 유입 경로 각각 6건을 복원한 주가 없었고, 151은 최초 N0 응답·독립 가림 검토·원사용자 비용이 비었다. 네 중앙 차단은 계속된다. 196은 43차 **계획**에서 186 대기로 BLOCKED였으나 186 인계 후 이번 **중앙 상태**는 RUNNING이다. 195·196의 `result_commit`은 계획 시점에 모두 null이다. [기준 진행표][control]

| AF-RES | 자기판정 | 중앙에 기록된 인계 SHA | 작업자가 지정한 결과·자체점검 SHA | 출처 원장 행 / 작업자 산입 단위 |
| --- | --- | --- | --- | --- |
| 186 · JSON-LD | DONE | [7042060][h186] | [7182108][r186] | [63 / 열어 지문을 남긴 파일 48, 다른 SHA-256 값 42][s186] |
| 187 · NumPy 복사 | PARTIAL | [4dd004b][h187] | [1c1ebce][r187] | [52 / 고유 자료 32][s187] |
| 188 · 영국 좌표 | PARTIAL | [a0fcb2d][h188] | [4f7f76d][r188] | [50 / 적격 31, 엄격한 주표본의 사건 문서 1][s188] |
| 189 · 자동완성 | PARTIAL | [6fa4492][h189] | [328d1c6][r189] | [51 / 고유 44, 자연 표본의 독립 원사건 4][s189] |
| 190 · 디지털 도서 | PARTIAL | [0449e0d][h190] | [a9c1200][r190] | [75 / 산입 50, 직접 읽은 고유 원면 17][s190] |
| 191 · CSS 색역 | DONE | [19ae6c6][h191] | [e89749e][r191] | [33 / 적격 22판, 21개 저작·14계보][s191] |
| 192 · 논문과 배포 | PARTIAL | [60704a5][h192] | [5486399][r192] | [50 / 직접 고유 자료 36, 배포 사건 4][s192] |
| 193 · 메일 제공자 | PARTIAL | [2beb6cb][h193] | [8a52106][r193] | [46 / 편의 표본 포함 33, 엄격 기준 25][s193] |
| 194 · 기존 API | PARTIAL | [5e46fcf][h194] | [6b685b8][r194] | [51 / 고유 URL 39, 목적표본 PEP 4][s194] |

471개 JSONL 행을 파싱해 작업별 source_id 수를 대조하고 CSV의 행 수·열 너비를 검산했다. 186의 T04 양 엔진·두 반복 원로그와 감사 요약, 188의 점과 실효 연산, 190의 24개 대상 판정, 191의 결의·편집 시점, 192~194의 목적별 원행도 대조했다. 파일 단위·저작 단위·사건 단위는 표에 구분했다. 이 검토에는 외부 시험 재실행, 과거 사용자 인터뷰, 독립 독자 실험이 포함되지 않았다. [실행 감사][audit186] · [점 원장][pt188] · [도서 24행][rt190] · [편집 연표][dec191] · [제안 연표][time194]

**작성 중 확인한 상태 변경.** 새 ID의 충돌을 마지막으로 확인한 통합 커밋(`ca4f683`, 20:40:26 UTC)에는 195·196이 모두 중앙 DONE으로 기록됐다. 이번 결과 검토의 마감은 위 `0502786`이다. 다음 누적 검토자는 그 SHA부터 비교해 두 신규 인계를 읽을 수 있다. 207 담당자는 두 고정 SHA에서 실제 입력 요건을 확인하는 즉시 착수 상태를 다시 판정할 수 있다. [마감 뒤 진행표](https://github.com/laadkke-arch/agentflow-open/blob/ca4f683e612c404035e2d80d49b6707f390d3985/docs/automation/dot-control.json)

## 43차까지 이어받은 제품 판단

| 설계 질문 | 앞선 검토에서 남은 근거 | 지금 유지할 선택 조건 |
| --- | --- | --- |
| 전체 설계 없이 일부 구조와 목적을 받을 수 있나 | 020은 전달 주장 72/73이지만 모든 충돌이 풀린 묶음은 2/16이었다. 103은 외관 10/10과 텍스트 선택을 별개로 보였고, 107은 개별 발생 위치로 편집 6/6, 공유 정의만으로 0/6이었다. 159에서 위치만으로 기능을 가른 자리는 46/48, 소비자 역할로 가른 자리는 48/48이었다. | 선택한 객체, 다음 조작, 그때 보존할 값이 다르게 해석되면 최소 예나 한 질문이 유용하다. 구분 가능한 설계와 실제 작성자의 대답은 따로 센다. |
| 기능명 밖에서 원리를 찾아올 가치가 있나 | 010은 원분야 단서로 7군을 찾았다. 033의 단서 없는 144쌍에서 당시판 지지 0, 145의 독립 초안 0/16이었다. 166·174의 대기열·지도 레이블 예측과 183의 금액 분배 24예측은 남았지만, 183의 같은 입력·SHA 공개 실행은 0/16이었다. 가까운 반올림 규칙도 몇 입력에서 같은 예측을 냈다. | 원리의 설명력, 힌트 없이 발견한 경로, 가까운 대안에 더한 판별력, 실제 설계 선택 변화는 각기 다른 결과다. |
| 여러 링크는 언제 같이 또는 따로 보여 줄까 | 040의 완전 적격 0/8, 044의 고정 풀에서는 두 묶음 방법이 같았다. 114의 ‘충돌’ 138건은 118에서 명시 충돌 7·미확인 131로 갈렸다. 146의 48후보는 직접 충족 0·부분 15·충돌 14·미확인 19였다. 177의 요청은 검색과 단일 페이지 중 하나로 충족 가능했다. | 같은 판단을 지지하는 출처 둘, 대체 가능한 후보 둘, 같은 환경에서 함께 작동해야 하는 부품 둘을 따로 표현한다. 보편적인 최적 링크 수는 열려 있다. |
| 옛 추천 이유와 현재 후계는 같은 기록으로 찾나 | 055는 옛 답 4/4·다음 판 0/4, 147은 과거 답 112/112 복원이었다. 150의 세 보관안은 동일성 값과 근거가 함께 맞은 쌍이 7·9·15/16이었다. 161에서는 병합 취소 뒤 하류 P910에 별도 복구가 필요했다. 169는 분할된 코드마다 후보 둘과 기본값 하나를 찾았으나 실제 개별 레코드 치환쌍은 0이었다. | 당시 상태의 인용, 오늘의 대상 선택, 특정 부분의 재사용은 요구하는 식별 정보가 다르다. 178의 유효한 개발판 문자열도 비교 정책에 따라 결과가 갈렸다. |
| 언제 새 정보와 변경을 확인할까 | 024의 무효화 11건 중 주기는 11, 신호는 8을 찾았다. 신호는 열람이 108회 적고 전송량은 5,672,462바이트 많았다. 152의 새 자료 15건 중 신호/희소 공급원 방식은 14, 주기는 13이었다. 162·170은 공지·설정·사용자의 실제 접근 시점이 다를 수 있음을 보였다. | 신규 발견, 기존 이유의 무효화, 해당 이용자의 실사용 가능성을 따로 평가한다. 날짜·예산·놓친 신호를 함께 남긴다. |
| 작성자가 받아들이고 실제로 해결했나 | 158의 제출 28건은 수신 증거가 아니었고 163은 발신 35건 중 특정 통지 뒤 원제출자가 재개한 보강 사례가 1건이었다. 180은 자연 8건의 지정 창에 원제보자 텍스트 후속 0, 보강 #197268에는 특정 명령 재시험이 있었으나 동일 빌드·fixture 확인은 비었다. 022의 미인지→선택 변경→시행은 0/24였다. | 제출·마감·배포·회신·같은 조건의 당사자 재시험을 구분한다. 표본에서 관측하지 못한 행동을 거절로 바꾸지 않는다. |
| 재사용이 노동이나 재작업을 줄였나 | 034의 한 단계는 380→57초, 전체는 849→847초였다. 160에는 1,061.9인시와 추정 비교값이 섞였고 164는 한 직접작성 집단을 두 비교가 공유했다. 172에서 전원·동일 기능·시간·독립 검수가 맞은 비교는 0. 181의 터키어 번역 다섯 분절은 2,061,853ms·원문 111단어였고 여덟 문서의 24예정 배정에서 처리행이 보인 것은 1배정이었다. | 역할별 시간창·예정 분모·검수 품질을 갖춰야 절감을 말할 수 있다. 한 처리행을 같은 사람의 세 조건 비교로 쓰지 않는다. |
| 설치·호환·보존 근거가 사용자가 원하는 동작까지 가나 | 154는 명시적 원본 회수 10/10, 기본 다운로드 같은 바이트 6/10이었다. 176은 보고서→표시 55/55 일치, 당시 독립 실행 여부 미확인이었다. 179의 고정 18자리 중 17개는 미확인이고 별도 커서의 오류는 다른 JSON 함수였다. 182에는 악보 그림 차이, 184에는 로그 하나를 가리킨 바이너리 표시 셋, 185에는 같은 lock의 소비자 둘이 있었으나 실제 공동 출력은 비었다. | 선택한 소스·실효판·실제 같은 입력·마지막 출력까지 특정한 범위로 링크의 약속을 좁힌다. 한 계보에서 나온 여러 표시는 독립 결과로 더하지 않는다. |

이 표는 43차에서 채택·보류한 판단의 요약이다. 상세 계보와 이전 정정은 해당 누적표에 남아 있다. 제품 DB·AgentFlow 입력 계약·AI 전처리·상시 크롤러·최종 순위는 계속 비교할 대안이다. [43차 누적표][r43] · [178~185의 관측과 반례][r43facts] · [제품의 열린 질문][product]

## 신규 아홉 작업에서 확인한 것과 결론을 멈춰야 하는 곳

**186 · 같은 시험에서 다른 두 반환을 직접 읽을 수 있다.** W3C 고정판 열 입력을 Gold v0.3.0과 JS v3.1.0에 별도 프로세스로 두 번씩 넣었다. 40회 중 Gold 18/20, JS 20/20 합격이다. 반복끼리 20/20 일치했고 엔진끼리는 9/10이었다. Expansion t0123의 동일 입력에서 Gold는 두 번 모두 공백이 든 datatype IRI를 JSON에 넣어 돌려줬고, JS의 두 stderr에는 `invalid typed value`가 있다. 실패 두 번은 같은 엔진·시험의 반복이다. 2020년 제출자의 판정과 이번 판정 20/20이 일치하지만 당시 옵션·suite SHA·런타임·원로그·운영자 독립성은 복원되지 않았다. 전체 시험군이나 다른 환경으로의 일반화도 미확인이다. [40회 실행][runs186] · [Gold 원출력][gold186] · [JS 원오류][js186] · [50행 비교][cmp186]

**187 · 같은 값을 얻는 변경과 원본을 함께 수정할 수 있는 변경이 다르다.** Datasets 2.20.0→2.21.0, Astropy 6.0.1→6.1.0의 실제 태그에서 호출·호환 코드 변화를 확인했다. NumPy 2에서 필요할 때 사본을 허용하는 호출과 명시적 `copy=False`는 입력 변환이 필요할 때 갈린다. Astropy는 단위 변환·dtype 변환이 추가 경계를 만든다. HF 원제보에는 실행 스택이 있지만 설치판·Arrow schema·입력값·같은 데이터 재시험이 빠진다. Astropy 출발점은 실제 입력이 없는 설계 이슈다. 완전한 원요구→실제 객체 연결 0/2, wheel/sdist 내부 대조 0/2, 동일 입력 재시험 0/2, 직접 쓰기 전파 실측 0이다. 태그 두 쌍은 확실하지만 원사용자의 문제가 해결됐다는 근거는 약하다. [호출 원장][call187] · [18개 동작 판독][beh187] · [HF 원제보](https://discuss.huggingface.co/t/valueerror-unable-to-avoid-copy-while-creating-an-array-as-requested/93584) · [Astropy의 실제 분기](https://github.com/astropy/astropy/blob/35d18ce8bd682a36e30a8f7ee86a8d5fac89e2bf/astropy/units/quantity.py#L430-L575)

**188 · 모형 파일을 열었다는 로그와 선택된 연산은 다를 수 있다.** 영국 본토 수평 변환과 ODN 높이, Scilly·맨섬의 높이 기준은 서로 다른 자료/조건을 요구한다. 보강 #2173의 로그에는 수직 격자 열람이 있는데 실제 경로에는 근사 수직 연산(ballpark)이 선택됐다. #1534의 원제보자에게 어느 격자가 실효였는지는 미확인이다. 여섯 요구 자리는 TP01·02·03·21 네 고유점이며, 두 재게재본이 선택한 행에서 일치했다. 발행처 ZIP에서 직접 확인한 점은 0/6, 명시적인 공식 점별 공차도 0/6이다. 별도 대조 TP31의 E/N은 두 저장소 원행에서 9,587.909/899,448.996 m, X05 게시표에서는 9,587.906/899,449.000 m다. 이 mm 차이가 생긴 이유는 기관 원본을 확인할 때까지 열려 있다. TP31/32는 선택한 네 점의 불일치율에 넣지 않는다. 사건 원문은 보강을 넣어 3/4, 지정 모집틀 안에서 1/4였다. [여섯 자리의 원값·단위][pt188] · [발견된 연산과 실효 연산][op188] · [제보와 디버그 로그](https://github.com/OSGeo/PROJ/issues/2173)

**189 · ‘검색어를 유지해 달라’는 말로 서로 다른 기능을 요구했다.** #36085는 선택 뒤 입력창의 검색어를 보존하려 했다. #18784 작성자는 선택 라벨로 인한 추가 검색을 막고 사용자 입력에만 반응하려는 뜻을 직접 확인했다. 후자에게 문자열 자체의 보존까지 필수라고 단정할 수 없다. 두 목적이 이미 쓰여 있으면 각각 다른 첫 링크로 즉답할 수 있다. 목적이 생략됐을 때만 ‘화면 문자열이 남아야 하나, 추가 검색이 없어야 하나’가 답을 가른다. 자연 여섯 자리에는 같은 계보의 후속이 들어 있고 독립 원사건은 네 건이다. 제시한 질문을 사용자에게 실제로 물어 얻은 효용은 측정하지 않았다. 표시가 계속 유지된 상태에서 정확히 두 요청을 본 동일 사건도 없다. 두 제보와 다른 프로젝트의 사례를 접합하면 존재하지 않았던 로그가 생긴다. [원요구 원장][req189] · [실제·가상 답 구분][q189] · [작성자 회신](https://github.com/mui/material-ui/issues/18784#issuecomment-564681486)

**190 · 판과 면만으로 페이지는 정해져도 그 안의 대상이 남는다.** 1866년 Tenniel 소장본의 첫 문장은 스캔 21–22면, 1916년 Rackham 인쇄본에서는 21면이다. 면 번호가 같은 두 첫 면도 서로 다른 인쇄·삽화다. 두 판 여덟 대상에서 작품+인쇄 숫자는 유일 1·공석 7, 판+파일+면은 유일 4·복수 4, 부분 단서까지 넣으면 유일 8이다. 이는 고정된 대상을 아는 연구자의 대조다. 독립 재탐색은 0/24이고 실제 클릭 시간도 없다. 삽화 파생본이 보인 원면과 구성이 같아도 바이트·변환 출전 연결은 0/2다. 파일/소장 자료 네 개 중 하나는 PDF 컨테이너여서 독립 서지 기준은 3/4이고 B 소장본의 출처 표기도 충돌한다. [원면과 전사 위치][loc190] · [세 안의 24행][rt190] · [출처·파생 관계][map190]

**191 · 문헌에서 실제 편집과 원리의 설명력을 구분했다.** 2025-04-24 초안은 Local MINDE를 설명한다. 2025-08-19 CSSWG 결의, 2026-01-22 편집, 06-23 Ray 수치 교정, 08-25 초안에서 세 방법을 허용하게 된 경로가 이어진다. 위원 발언은 비용·정확도·구현 환경의 절충을 지지한다. Oklab 원저자 인용과 별도 예제의 직접 링크는 있어도 특정 관찰자 연구 때문에 #10579의 선택이 바뀌었다는 발언은 찾지 못했다. 별도 IPT 실험의 9명·30세션을 CSS 후보 세 개의 지각 실측으로 옮길 수 없다. 같은 관찰 조건에서 세 후보를 비교한 실측은 원장에 0건이다. 작업자의 DONE은 질문에 맞는 문헌 판정을 마쳤다는 뜻이다. [결정 9행][dec191] · [응용 조건 6행][tr191] · [위원회 결의](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200859856) · [반영된 초안](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/)

**192 · 인용과 설치가 실제로 다른 객체를 가리킨다.** seaborn v0.13.1/0.13.2의 CITATION.cff는 같은 blob이고 PyPI 파일은 달랐다. JOSS가 가리키는 보관 DOI는 v0.11.1이었다. MAPIE v1.1.0/v1.2.0의 선호 PMLR 논문은 과거 arXiv 저작과 다르고, 두 태그 소스에서 Romano Algorithm 2를 지목하는 것은 `agg_scores="crossval"` 조건이다. 네 판의 배포 목록과 파일 여덟 개의 게시자 해시는 읽었지만 배포 바이트를 독립 확인하지 않았다. 정확한 네 선택판 archive DOI는 0/4 확인, 두 계보 concept DOI의 조회일 실제 이동도 0/2 확인이다. DOI 미발견과 DOI 부재를 구분해야 한다. 사용자 목적을 네 가지로 나눈 16행은 링크 제안이며 실제 사용자 클릭 기록은 없다. [버전별 객체][obj192] · [변화 10행][chg192] · [목적별 16행][rt192] · [MAPIE 조건이 있는 원소스](https://github.com/scikit-learn-contrib/MAPIE/blob/v1.2.0/mapie/classification.py#L477-L522)

**193 · 설치 관리자의 택일로 최종 이용자에게 택일을 보장할 수 없다.** Debian trixie에서 bsd-mailx의 Depends와 cron의 Recommends가 다르며, Exim과 nullmailer는 같은 가상 제공자 자리를 채울 수 있다. nullmailer의 큐 접수는 릴레이 전달의 시작이다. 같은 호스트 mbox에 새 메일을 받으려면 Exim 모드·스풀 형식·읽기 단계까지 맞아야 한다. 외부 릴레이가 목적이면 두 제공자가 각각 조건부 대안이 되고, cron 메일이 필요 없으면 `MAILTO=""`라는 다른 답이 생긴다. 모집틀의 네 패키지×최초 두 BTS 자리 8개는 순서 검증이 안 됐다. 읽은 편의 사건 8건은 엄격 모집틀의 사건 문서 하한 4건을 채우지 못한다(적격 0). 같은 정확판 실행의 끝단 수신 증빙 0건이므로 전달 실패율도 계산할 수 없다. [관계 원장][rel193] · [정적 호출 4·제보 8행][evt193] · [목적별 선택][choice193]

**194 · 먼저 알던 대안이 있어도 새 API가 채택될 수 있다.** PEP 559의 저자는 초안부터 지역 helper를 알았고 결정권자의 기각 이유에도 그 충분성이 나온다. 3142는 takewhile에 기능 대응이 있지만 기각 메일에 그 대안이 원인이라는 설명이나 저자 직접 회신이 없다. 616·618은 기존 조합으로 남는 공통 인터페이스·오류 처리·발견성 같은 요구가 있었고 채택·출시됐다. 618의 외부 `zip_equal` 안정판은 최초 제안 뒤, 결정 전 비교 자료였다. 네 PEP 모두에서 ‘처음 몰랐음→링크로 선택 변경→실행’의 적격 사례는 0/4이다. 41개 연표 행과 12개 링크 카드는 독립 결정 41건이나 절약 12건을 뜻하지 않는다. 분야 대조는 교통·도서관 요구 원문 4개 중 2개만 적격이었다. [당시 대안 16행][alt194] · [제안 연표][time194] · [목적별 카드][card194] · [559의 당시 결정 메일](https://mail.python.org/pipermail/python-dev/2017-September/149438.html)

## 충돌하는 주장에서 무엇을 돌려줄 것인가

| 겉으로 충돌하는 결과 | 증거가 갈리는 지점 | 개발자에게 허용되는 답과 이를 바꿀 관측 |
| --- | --- | --- |
| 176에서는 합격 표시가 원보고와 맞았고 186에서는 같은 시험에서 두 엔진이 달랐다. | 전자는 보고서 재표시, 후자는 같은 입력으로 남긴 새 원출력이다. 역사 판정 20/20 일치와 현 엔진 값 9/10 일치도 비교 대상이 다르다. | 186 고정판의 t0123에는 구현·입력·옵션을 붙여 해당 오류 또는 반환을 안내한다. 과거 실행값을 인용하려면 당시 원로그와 suite 판이 필요하다. [직전 누적 검토][r43] · [현·과거 비교 원장][cmp186] |
| 187의 패치 태그, 188의 열린 격자, 193의 패키지 제공자 모두 기능이 있는 것처럼 보이는데 끝단은 확인되지 않았다. | 배포 소스, 후보 연산, 설치 관계가 각각 증명하는 시점이 다르다. 188에는 실제 다른 수직 연산을 선택한 양성 반례가 있다. | 실행 근거를 요구하는 입력에는 배포 artifact·실효 선택·최종 목적을 붙인다. 205는 같은 fixture에서 값·공유·쓰기, 206은 기관 대조점 원값만 판정한다. 해당 검사로 과거 사용자 해결을 소급하지 않는다. [187][beh187] · [188][op188] · [193][evt193] |
| 상세 단서가 늘수록 좋아 보이지만 189의 두 제보는 이미 목적을 밝혔고 190에서는 일부에만 부분 단서가 필요했다. | 조건이 문장에 이미 있는지, 대상이 면 전체인지 면의 한 구성요소인지가 다르다. 192에서는 같은 프로젝트라도 원리 인용과 설치의 첫 주소가 달랐다. | 목적이 명시되면 바로 해당 절을 주고, 두 해석이 실제로 다른 링크를 필요로 할 때만 한 번 묻는 안을 보존한다. 이용자의 답·시간·행동을 측정해야 상호작용 우위를 말할 수 있다. [189][q189] · [190][rt190] · [192][rt192] |
| 191에는 외부 원리 인용이 있고 194에는 기성 대안이 있지만, 결정 원인은 확인되기도 하고 비어 있기도 하다. | 559에는 결정권자가 충분성을 말했다. 3142에는 그 이유가 없고 191의 편집 결의는 특정 외부 실험을 채택 사유로 지목하지 않는다. | 가까운 구현 설명, 타 분야 원리, 당사자 결정 기록을 각기 어떤 질문에 쓸지 명시한다. 사용자가 새로 알게 됐다는 주장은 같은 사람의 발언·행동이 있을 때만 더한다. [CSS 결정][dec191] · [PEP 연표][time194] |

## 다음 배정과 착수 조건

새 웹 작업은 앞선 결과가 비운 **서로 다른 제품 결정**을 다룬다. 예컨대 무손실 컷의 필수 조건을 찾는 작업(198)과 공개 지명 검색 서버의 이용 방식을 고르는 작업(204)은 근거도, 답을 바꾸는 관측도 다르다. 205·206은 웹 문헌을 더 늘려도 얻을 수 없는 배포 바이트와 공식 ZIP의 원행을 검사한다. 아래 ‘즉시’는 데이터 의존이 풀렸다는 뜻이며 실제 동시 실행 수는 진행 담당자의 배정에 따른다. [전체 지시문](NEXT_TASKS-44.json)

| ID · 담당 | 선행 · 착수 | 자료·고정 단위 | 완성하면 결정할 수 있는 것 |
| --- | --- | --- | --- |
| 197 · 웹 | 189 · 즉시 | MUI X·TanStack Table의 행 선택 원요구 여섯 자리, 페이지·필터·ID·수신 측 | ‘전체’가 현재 면인지 서버의 전체인지 밝히기 위해 한 번 물어야 하는 경우 |
| 198 · 웹 | 187 · 즉시 | LosslessCut 지명 요청 여섯 건, 두 문서 탐색 경로, FFmpeg·MKVToolNix 경계 | 원본 압축을 유지하는 링크와 프레임 경계를 맞추는 링크가 갈라지는 요청 |
| 199 · 웹 | 191 · 즉시 | Reinhard 2002/2005 원논문, pfstmo/OpenCV 두 구현의 여섯 조작 자리 | 사진 인화 원리가 실제 조작 선택에 더하는 것과 이름만 비슷한 잘못된 원전 |
| 200 · 웹 | 192 · 즉시 | matplotlib 3.9.1·pytest 8.1.0 철회와 인접판, 핀·범위·기설치 목적 | 링크가 열려도 특정 사용자에게만 경고하거나 다른 판을 보여줄 조건 |
| 201 · 웹 | 192 · 즉시 | 네 소비자 출판판의 실제 seaborn 언급 및 논문→저자 코드→그림 | 비교문헌, 실제 구현 예, 출력 생성 기록 가운데 어느 것을 추천 근거로 쓸지 |
| 202 · 웹 | 188·193 · 즉시 | Tesseract의 세 모델 모음×두 언어×두 모드, 경로·구성 오류 원제보 | 오프라인 인식에서 엔진과 함께 어느 언어 자료를 반드시 안내할지 |
| 203 · 웹 | 194 · 즉시 | Clippy 가독성 규칙 자연 제안 여섯 자리와 별도 보강, 당대 규칙·후속 행동 | 중복 마감과 구별해 기존 기능의 발견이 실제로 바꾼 제안자의 선택 |
| 204 · 웹 | 193 · 즉시 | Nominatim·Photon의 공용/자체 운영 네 형태×세 지명 검색 패턴 | 같은 OSS의 기능·공용 서비스 조건·자가 호스팅용 데이터 중 어느 링크가 맞는지 |
| 205 · Codex | 187 · 즉시 | 정확한 wheel 네 개, Python·NumPy 고정 8환경×4 fixture | 같은 값이 돌아와도 쓰기 전파와 원본 공유를 실제로 보장할 수 있는지 |
| 206 · Codex | 188 · 즉시 | OS 원 아카이브·두 저장소 사본·별도 게시표, 주점 4개·충돌점 2개 | 기관이 실제로 발행한 점별 원값과 재게재본 차이·공차 미기재를 어디까지 인용할지 |
| 207 · Codex | **195·196 · BLOCKED** | 196에서 단건 원출전 확인에 통과한 기록을 195의 단일행·복수행 집계·유보 문장에 적용 | 숫자가 같지만 분모나 구성 행은 틀린 추천 근거를 가려내려면 어떤 기록이 더 필요한지 |

웹 진입점으로는 MUI의 지명 제보, LosslessCut의 원논의, 두 톤매핑 구현의 제작자 문서, 실제 PyPI 철회 기록, 후속 저자의 JOSS 출판판, Tesseract 모델 안내, Clippy의 공식 규칙 색인, OSMF의 해당 호스트 운영 방침이 있다. 이 주소는 작업자가 판·본문·당사자를 확인할 출발점이다. 열람 가능성을 결과 적중으로 세지 않는다. [행 선택 제보](https://github.com/mui/mui-x/issues/14070) · [컷 경계 제안](https://github.com/mifi/lossless-cut/issues/126) · [pfstmo 구현](https://resources.mpi-inf.mpg.de/tmo/reinhard02/index.html) · [OpenCV 구현](https://docs.opencv.org/4.x/d0/dec/classcv_1_1TonemapReinhard.html) · [pytest 철회 기록](https://pypi.org/project/pytest/8.1.0/) · [소비자 출판판](https://joss.theoj.org/papers/10.21105/joss.07120) · [언어 자료](https://tesseract-ocr.github.io/tessdoc/Data-Files) · [규칙 색인](https://clippy.rust-lang.org/stable/index.html) · [공용 지오코딩 서비스 방침](https://operations.osmfoundation.org/policies/nominatim/)

**진행 중인 두 작업의 경계.** 195는 고정한 DivEMT 이탈리아어·터키어 ZIP에서 여덟 문서와 24개 예정 배정의 작업 사건·시간·출력을 대조한다. 196은 186의 확정 인용을 세 저장안×두 가용 조건에 놓고 당시 원출전 회수·해시·비용을 검사한다. 197~204의 어느 표집에도 이 ZIP·분절·JSON-LD 영수증·오프라인 복원이나 보관비 비교가 없다. 205·206도 187·188만 사용한다. **207의 선행은 두 가지가 모두 필요하다.** 각각 중앙 DONE·확정 SHA·해당 SHA의 HANDOFF를 확인하고, 195에 익명 행키·집계 입력이, 196에 실제 통과한 단건 표현·판정행이 있어야 한다. 하나라도 없으면 착수 보류를 유지한다. 207은 기존 두 실험의 재실행 대신 다른 자료형에서 행집합·단위·분모가 보존되는지를 별도 대조한다. [195·196의 고정 요청문][p43] · [요청 시점 중앙 상태][control]

## 다음 판단에 가장 중요한 약점 세 건

| 약점 | 현재 말할 수 있는 범위 | 판단을 바꿀 다음 자료 |
| --- | --- | --- |
| 동작을 권할 때 실효 입력과 마지막 결과가 빠진다. | 태그 소스, 격자 열람, 큐 접수는 확인했다. 각각 배포된 동일 버퍼·선택된 수직 연산·수신자의 메일함과는 거리가 있다. | 205의 실제 wheel 경로·공유·쓰기 원로그와 206의 기관 점 원행을 확보한다. 메일의 최종 배달을 주장하려면 같은 호출→큐 ID→목적 사서함의 기록이 별도로 필요하다. |
| 출처를 찾았다는 말이 실제 사용·재발견·설득 효과로 바뀌기 쉽다. | 190의 조건부 유일 대상 8개, 191의 결의·참고문헌, 194의 실제 처분은 확인됐다. 독립 독자의 재탐색과 대안 발견 뒤 행동은 비어 있다. | 199에서 원리와 구현 조작, 201에서 인용과 실제 함수/그림, 203에서 제안자의 전후 행동을 따로 추적한다. 이용자가 말하지 않은 의도는 미확인으로 남긴다. |
| 자료 수가 늘어도 비교할 분모·역할·기관 원본은 빠질 수 있다. | 188의 여섯 자리에는 네 점, 193의 사건 여덟 개에는 엄격한 최초 표집 0건, 181의 기록시간에는 다른 역할의 검수시간이 없다. | 195의 실제 행과 196의 실제 표현이 공개된 뒤에만 207로 행 선택이 다른데 합계가 일치하는 음성 대조를 검사한다. 그 전에는 절감률이나 최소 저장량을 일반화하지 않는다. |

[product]: https://github.com/laadkke-arch/agentflow-open/blob/050278651b11a2a3a49d45baebf41c707c06b700/docs/product/RESEARCH_BRIEF.md
[workflow]: https://github.com/laadkke-arch/agentflow-open/blob/050278651b11a2a3a49d45baebf41c707c06b700/docs/RESEARCH_WORKFLOW.md
[control]: https://github.com/laadkke-arch/agentflow-open/blob/050278651b11a2a3a49d45baebf41c707c06b700/docs/automation/dot-control.json
[prevctl]: https://github.com/laadkke-arch/agentflow-open/blob/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6/docs/automation/dot-control.json
[delta]: https://github.com/laadkke-arch/agentflow-open/compare/0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6...050278651b11a2a3a49d45baebf41c707c06b700
[r43]: https://github.com/laadkke-arch/agentflow-open/blob/b7c9bb5941539d187118d81c5dbf6f3b5af4ce05/docs/workstreams/planning/REVIEW-43.md
[r43facts]: https://github.com/laadkke-arch/agentflow-open/blob/b7c9bb5941539d187118d81c5dbf6f3b5af4ce05/docs/workstreams/planning/REVIEW-43.md#여덟-작업에서-확인된-것과-빈-고리
[p43]: https://github.com/laadkke-arch/agentflow-open/blob/b7c9bb5941539d187118d81c5dbf6f3b5af4ce05/docs/workstreams/planning/NEXT_TASKS-43.json
[h186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/HANDOFF.md
[r186]: https://github.com/laadkke-arch/agentflow-open/blob/7182108b635189f6b866d99e2eaadc210d59d9f9/docs/workstreams/research/AF-RES-186/RESULT.md
[s186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/sources.jsonl
[audit186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/execution/audit.stdout.log
[runs186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/runs.csv
[gold186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/gold-T04-r1/stdout.log
[js186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/receipts/js-T04-r1/stderr.log
[cmp186]: https://github.com/laadkke-arch/agentflow-open/blob/7042060cd73aad96f70ff290ec6d5f6adf22570b/docs/workstreams/research/AF-RES-186/comparison.csv
[h187]: https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/HANDOFF.md
[r187]: https://github.com/laadkke-arch/agentflow-open/blob/1c1ebcecc3b2d0e5881818e5b619b67a42d44452/docs/workstreams/research/AF-RES-187/RESULT.md
[s187]: https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/sources.jsonl
[call187]: https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/calls.csv
[beh187]: https://github.com/laadkke-arch/agentflow-open/blob/4dd004ba7bebb19ebc03f2539bf5716a14bd1787/docs/workstreams/research/AF-RES-187/behaviors.csv
[h188]: https://github.com/laadkke-arch/agentflow-open/blob/a0fcb2d1229e01639b27d34f8cb336fca7cf3cfc/docs/workstreams/research/AF-RES-188/HANDOFF.md
[r188]: https://github.com/laadkke-arch/agentflow-open/blob/4f7f76d981f10b6d6efbfe396751a1180b8dbd85/docs/workstreams/research/AF-RES-188/RESULT.md
[s188]: https://github.com/laadkke-arch/agentflow-open/blob/a0fcb2d1229e01639b27d34f8cb336fca7cf3cfc/docs/workstreams/research/AF-RES-188/sources.jsonl
[pt188]: https://github.com/laadkke-arch/agentflow-open/blob/a0fcb2d1229e01639b27d34f8cb336fca7cf3cfc/docs/workstreams/research/AF-RES-188/points.csv
[op188]: https://github.com/laadkke-arch/agentflow-open/blob/a0fcb2d1229e01639b27d34f8cb336fca7cf3cfc/docs/workstreams/research/AF-RES-188/operations.csv
[h189]: https://github.com/laadkke-arch/agentflow-open/blob/6fa4492e0e1a8c0510f573e914b4288786e0e694/docs/workstreams/research/AF-RES-189/HANDOFF.md
[r189]: https://github.com/laadkke-arch/agentflow-open/blob/328d1c6988ccaf89e7beddf34017bd7f80f68cff/docs/workstreams/research/AF-RES-189/RESULT.md
[s189]: https://github.com/laadkke-arch/agentflow-open/blob/6fa4492e0e1a8c0510f573e914b4288786e0e694/docs/workstreams/research/AF-RES-189/sources.jsonl
[req189]: https://github.com/laadkke-arch/agentflow-open/blob/6fa4492e0e1a8c0510f573e914b4288786e0e694/docs/workstreams/research/AF-RES-189/requests.csv
[q189]: https://github.com/laadkke-arch/agentflow-open/blob/6fa4492e0e1a8c0510f573e914b4288786e0e694/docs/workstreams/research/AF-RES-189/questions.csv
[h190]: https://github.com/laadkke-arch/agentflow-open/blob/0449e0d7e30477e31e868ca4dc9167ebd3f074eb/docs/workstreams/research/AF-RES-190/HANDOFF.md
[r190]: https://github.com/laadkke-arch/agentflow-open/blob/a9c1200b2e3eee705f0453c7cb73c0457dfc12b2/docs/workstreams/research/AF-RES-190/RESULT.md
[s190]: https://github.com/laadkke-arch/agentflow-open/blob/0449e0d7e30477e31e868ca4dc9167ebd3f074eb/docs/workstreams/research/AF-RES-190/sources.jsonl
[loc190]: https://github.com/laadkke-arch/agentflow-open/blob/0449e0d7e30477e31e868ca4dc9167ebd3f074eb/docs/workstreams/research/AF-RES-190/locators.csv
[rt190]: https://github.com/laadkke-arch/agentflow-open/blob/0449e0d7e30477e31e868ca4dc9167ebd3f074eb/docs/workstreams/research/AF-RES-190/routes.csv
[map190]: https://github.com/laadkke-arch/agentflow-open/blob/0449e0d7e30477e31e868ca4dc9167ebd3f074eb/docs/workstreams/research/AF-RES-190/sources-map.csv
[h191]: https://github.com/laadkke-arch/agentflow-open/blob/19ae6c6d17cc8adecec948d7103b7d3e81e428b6/docs/workstreams/research/AF-RES-191/HANDOFF.md
[r191]: https://github.com/laadkke-arch/agentflow-open/blob/e89749e4f61897626c29c7e99760e7e19521460c/docs/workstreams/research/AF-RES-191/RESULT.md
[s191]: https://github.com/laadkke-arch/agentflow-open/blob/19ae6c6d17cc8adecec948d7103b7d3e81e428b6/docs/workstreams/research/AF-RES-191/sources.jsonl
[dec191]: https://github.com/laadkke-arch/agentflow-open/blob/19ae6c6d17cc8adecec948d7103b7d3e81e428b6/docs/workstreams/research/AF-RES-191/decisions.csv
[tr191]: https://github.com/laadkke-arch/agentflow-open/blob/19ae6c6d17cc8adecec948d7103b7d3e81e428b6/docs/workstreams/research/AF-RES-191/transfer.csv
[h192]: https://github.com/laadkke-arch/agentflow-open/blob/60704a5701d1ac1608954d339b5ef8e9e25bcbd2/docs/workstreams/research/AF-RES-192/HANDOFF.md
[r192]: https://github.com/laadkke-arch/agentflow-open/blob/54863994cbf6ddee1aacc385679bf3fad2326306/docs/workstreams/research/AF-RES-192/RESULT.md
[s192]: https://github.com/laadkke-arch/agentflow-open/blob/60704a5701d1ac1608954d339b5ef8e9e25bcbd2/docs/workstreams/research/AF-RES-192/sources.jsonl
[obj192]: https://github.com/laadkke-arch/agentflow-open/blob/60704a5701d1ac1608954d339b5ef8e9e25bcbd2/docs/workstreams/research/AF-RES-192/objects.csv
[chg192]: https://github.com/laadkke-arch/agentflow-open/blob/60704a5701d1ac1608954d339b5ef8e9e25bcbd2/docs/workstreams/research/AF-RES-192/changes.csv
[rt192]: https://github.com/laadkke-arch/agentflow-open/blob/60704a5701d1ac1608954d339b5ef8e9e25bcbd2/docs/workstreams/research/AF-RES-192/routes.csv
[h193]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/HANDOFF.md
[r193]: https://github.com/laadkke-arch/agentflow-open/blob/8a52106de2dee1c5c07d7cfab5d0664667a8908b/docs/workstreams/research/AF-RES-193/RESULT.md
[s193]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/sources.jsonl
[rel193]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/relations.csv
[evt193]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/events.csv
[choice193]: https://github.com/laadkke-arch/agentflow-open/blob/2beb6cb6a1857942c41670458ae32f4895777366/docs/workstreams/research/AF-RES-193/choices.csv
[h194]: https://github.com/laadkke-arch/agentflow-open/blob/5e46fcf801c6857b8b2f574be3be4d9e95c5195e/docs/workstreams/research/AF-RES-194/HANDOFF.md
[r194]: https://github.com/laadkke-arch/agentflow-open/blob/6b685b8f6b4eebf4b2aa9d11f58c21b844a74e74/docs/workstreams/research/AF-RES-194/RESULT.md
[s194]: https://github.com/laadkke-arch/agentflow-open/blob/5e46fcf801c6857b8b2f574be3be4d9e95c5195e/docs/workstreams/research/AF-RES-194/sources.jsonl
[alt194]: https://github.com/laadkke-arch/agentflow-open/blob/5e46fcf801c6857b8b2f574be3be4d9e95c5195e/docs/workstreams/research/AF-RES-194/alternatives.csv
[time194]: https://github.com/laadkke-arch/agentflow-open/blob/5e46fcf801c6857b8b2f574be3be4d9e95c5195e/docs/workstreams/research/AF-RES-194/timeline.csv
[card194]: https://github.com/laadkke-arch/agentflow-open/blob/5e46fcf801c6857b8b2f574be3be4d9e95c5195e/docs/workstreams/research/AF-RES-194/cards.csv
