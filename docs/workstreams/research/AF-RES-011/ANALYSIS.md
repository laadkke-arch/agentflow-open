# AF-RES-011 — 공개 추천 질문·답변 실증 분석

## 핵심 결론

공개 스레드61개를 읽은 결과, 목적과 선택 대상만으로도 답은 시작되지만 **필수조건의 대상·강제성·드러난 시점**이 실제 탈락 판단을 크게 가른다. AF-RES-001의 정보 후보는 보존할 항목으로 대체로 유용하다. 그러나8개를 모두 채우게 하는 보편 입력 양식의 효과는 이 표본에서 입증되지 않았다. 부분 질문33개 중6개에는 질문자의 선택·구현 중·사용 보고가 있었고, 모호한 요청에 조건부 답이 먼저 나온 사례도 있다.

L/E/H는 서로 다른 오류·반박을 구별하는 데 도움이 됐다. 반면 **엄격한 타분야 전이 실패 T의 실제 거절은0개**다. 유지보수·생태계·가격·라이선스·신뢰·운영 부담·경험 등4축 밖 이유만 붙은 비판 응답은102개/32스레드였다. 이는4축의 정의를 다시 설계할 근거가 아니라, 적용 가능성 판정과 사람의 선택 이유를 분리해 보존할 근거다.

되묻기 뒤 변화는6사건이지만 질문 수정·설명 변경·새 후보 제시가 섞여 있다. 무응답을 실패로 바꾸지 않았다. 내부 별도 재코딩은 정보99/105칸, 답 형식129/149쌍이 일치한 반면 역할은75/149쌍만 일치했다. 따라서 세부 역할의 빈도나 일치율을 추천 품질의 검증으로 쓰지 않는다. 모든 수치의 분모와 반례는 아래에 있다.

## 1. 자료·단위·출처의 연결

| 플랫폼 | 스레드 | 전체 | 부분 | 코딩한 실질 답 단위 |
| --- | --- | --- | --- | --- |
| Software Recommendations SE | 30 | 15 | 15 | 89 |
| Ask HN | 10 | 5 | 5 | 169 |
| Reddit | 11 | 5 | 6 | 255 |
| GitHub Issues/Discussions | 5 | 0 | 5 | 12 |
| Lobsters·OKKY·GeekNews | 5 | 3 | 2 | 110 |
| 합계 | 61 | 28 | 33 | 635 |

본표본의 질문·현재 공개 답·댓글을 직접 열었다. 기타5개는 Lobsters3개와 한국어 OKKY·GeekNews 각1개다. 비스레드 자료는 **30개: 문헌8, 참고서비스 지침1, 커뮤니티 실증연구5, 플랫폼 규칙·메타16**이며 서로 다른 URL30개·호스트18개다. 스레드와 문헌 수는 합산하지 않았다. 연구진이 읽은 원문 위치·확인 내용·한계는 [CASES.json](CASES.json), [sources.json](sources.json), [SAMPLING.md](SAMPLING.md)에 있다.

635는 후보 제품의 수가 아니라 **코딩한 실질 답 단위**다. 한 답이 여러 후보를 비교할 수 있고 같은 후보에 대한 독립 후속 설명도 있다. 원판609개에서 재코딩의 누락 단위 감사로26개를 추가했다. 상세 대응은 [RELIABILITY.md](RELIABILITY.md), 집계는 [metrics.json](evidence/metrics.json), 재생성은 `python docs/workstreams/research/AF-RES-011/audit.py --write`다. 원판·블라인드 코딩은 보정 전 그대로 남아 있다.

표본은2014–2026 공개 기록의 검색 순서에 따른 층화 편의표본이다. 모집단 비율·인과 효과·검증된 제품 성능을 추정하지 않는다. D1은 문서/발언 내용, D3은 단회 URL 접근, 제품 적용 제안은 H로 구분한다. 직접 실행·통합 실험(D4)은 없다. 각 사례 ID는 최초 데이터 ID로 고정했고 문헌 ID는 sources의 항목으로 연결한다.

## Q1. 질문에 무엇이 있고 무엇이 빠지는가

| 항목 | present | absent | 그 밖의 상태 | 대표 관측 |
| --- | --- | --- | --- | --- |
| I1 원문·다시 찾을 위치 | 11 | 0 | captured=50 | T061 이전 논의 연결; 연구자가 URL을 저장한 captured와 구별 |
| I2 바라는 결과·불편 | 61 | 0 | — | T013 텍스트 추출, T040 작업 분배 |
| I3 선택 범위 | 61 | 0 | — | T033 설치할 블로그와 호스팅의 차이 |
| I4 명시 조건 | 57 | 4 | — | T001 서버/클라이언트 공개성; T017 필수/선호 구별 |
| I5 주변 입출력·경계 | 45 | 16 | — | T049 업로드→검증/재작성; T045 여러 앱을 올릴 기반 |
| I6 현재·계획·예시·보고 지위 | 48 | 13 | — | T050 첫 후보와 후일 사용 보고의 차이 |
| I7 적용 환경·설정·자료형 | 44 | 17 | — | T022 .NET8 DLL; T019 후속 Windows/GPU 설정 |
| I8 원문과 재해석의 관계 | 8 | 0 | not_applicable=53 | T061 앞선 논의와 현재 비교; 독립 질문은 해당 없음 |

I2와 I3가61/61인 것은 ‘무엇을 하려는 추천 질문인가’라는 포함 기준의 영향도 받는다. 이 결과로 모든 실제 입력에 목적과 범위가 충분히 들어 있다고 추론할 수 없다. I1의 captured50은 연구자가 위치를 보존했다는 뜻이며 질문자의 정보 충실성 점수가 아니다. I8의 not_applicable53도 누락률이 아니다.

가장 자주 비어 있는 적용 정보는 I7 17개, I5 16개, I6 13개였다. I7의 present44는 OS·언어·형식·설정 중 무엇인가가 있다는 뜻이며 **정확한 버전44개**를 뜻하지 않는다. [T014](https://softwarerecs.stackexchange.com/questions/87508/please-suggest-a-free-good-video-editing-tool) · [T036](https://news.ycombinator.com/item?id=16882140) · [T039](https://news.ycombinator.com/item?id=41072631)의 일반 플랫폼 범위·위험 비유·SQLite 비유는 실제 적용 설정과 구별해 재코딩 뒤 수정했다. [T053](https://github.com/rlemaigre/vue3-promise-dialog/issues/15)은 본문에는 버전이 없지만 저장소 문맥으로 Vue3가 알려져 있으므로, 실서비스가 이미 가진 정보를 다시 묻게 할 이유는 없다.

조건은 대부분 보였지만 강제성·대상이 같지 않았다. 구조화한 조건 묶음118행에서 must68, prefer44, unclear6, positive107, negative11이었다. 이유가 기록된 행은18이다. 여러 조건을 한 행으로 묶은 곳이 있으므로 이를118개의 독립 요구나100건의 확정 이유 누락으로 환산하지 않는다. [T001](https://softwarerecs.stackexchange.com/questions/75118/alternative-to-slack)의 ‘서버와 클라이언트’를 구별하지 않으면 Discord가 비슷한 채팅 제품이라는 이유로 통과한다. [T017](https://softwarerecs.stackexchange.com/questions/30347/a-modernish-c-graph-representation-and-manipulation-library)의 C++ 선호를 필수로 바꾸면 래핑 비용 때문에 피한 후보를 H로 과대 판정하게 된다.

이 관측은 SR의 목적·필수/선호·대체 이유 규범과 맞지만, 그 규범이 적용된 사이트의 생존 표본이라는 점도 중요하다([P01](https://softwarerecs.stackexchange.com/help/on-topic) · [P02](https://softwarerecs.meta.stackexchange.com/questions/336/what-is-required-for-a-question-to-contain-enough-information) · [P04](https://softwarerecs.meta.stackexchange.com/questions/48/how-to-ask-for-an-alternative-to-some-software)). 요구 도출 연구의 질문 누락·성급한 기술 결정 사례([C06](https://openportal.isti.cnr.it/data/2019/411068/2019_411068.postprint.pdf))는 이 항목을 확인할 이유를 보태며, 모든 빈칸을 반드시 질문해야 한다는 근거를 주지는 않는다.

## Q2. 무엇을 되묻고 실제로 무엇이 바뀌는가

전체 명료화80사건은 원질문 대상38, 추천 설명 대상28, 곁가지 대화14로 나뉜다. 원질문38사건 중1개는 봇의 보강 요청이므로, **사람의 원질문 되묻기는37사건/23스레드**다. 추천을 받은 질문자가 기능을 다시 묻는 경우는 원질문자에게 부족 정보를 받는 사건과 합치지 않았다.

| 되묻기 종류 | 사람의 원질문 대상 사건 수 /37 | 그 답이 바꾸는 판단 예 |
| --- | --- | --- |
| 언어·OS·설정 | 11 | 로컬 모델인가 API인가(T019), 기존 AWS인가 범용 큐인가(T040) |
| 예산·금지·강제성 | 7 | 예산 내 후보인가(T021), 외부 호스팅이 가능한가(T042) |
| 입출력·규모·연결 | 6 | 필요한 처리량·전달 의미를 감당하는가(T047) |
| 어느 부분을 고르는지 | 5 | 대체 SaaS가 무엇인가(T041); 이미 준 예시를 반복하는지도 점검 |
| 시도·배제 이유 | 3 | cdist가 탈락한 이유 때문에 pyinfra를 검토해야 하는가(T056) |
| 목적·왜 | 3 | 코드·위키·Markdown 중 실제 편집 목적에 따라 후보를 고르는가(T020) |
| 용어 의미 | 2 | 같은 용어가 데이터 구조와 실행 제품 중 무엇을 뜻하는가 |

### 응답 뒤 변화가 보인6사건

| 사례 | 되묻기→질문자 정보 | 관측된 변화 | 바꾸는 판단 한 문장 |
|---|---|---|---|
| [T009](https://softwarerecs.stackexchange.com/questions/84965/a-framework-to-build-an-interactive-website) | 쓰는 언어·재학습 의향 | 질문 수정 | 기존 환경 유지와 새 프레임워크 학습 중 어느 경로를 비교할지 달라진다. |
| [T019](https://softwarerecs.stackexchange.com/questions/95480/looking-for-a-free-open-source-vs-code-ai-coding-assistant-similar-to-github-cop) | GPU·메모리·OS | 설명과 새 답 | 로컬 대형 모델 실행 대신 API 경로를 검토할지 달라진다. |
| [T021](https://softwarerecs.stackexchange.com/questions/86879/is-there-a-decent-open-source-or-low-cost-net-sdk-that-has-functions-for-parsin) | 예산 범위 | 질문에 가격 범위 추가 | 개인 예산 안에 있는 라이선스 후보인지 판정할 수 있다. |
| [T040](https://news.ycombinator.com/item?id=18542227) | Java/AWS와 기존 SQS·DB | 새 후보·구성 설명 | 범용 큐보다 기존 AWS 실행·중복 처리 설정을 먼저 볼지 달라진다. |
| [T042](https://www.reddit.com/r/selfhosted/comments/1gxw9z9/selfhosted_kahoot_alternative/) | 추가 기능 초대→자체 도메인·운영 이유 | 호스팅 설명의 한정 | 무료 외부 호스팅으로 충분한지 자체 호스팅 경로가 필요한지 달라진다. |
| [T056](https://lobste.rs/s/bgsuwg/how_do_you_find_your_software_tools) | 시도한 대안→수동 셸 금지 | pyinfra 추가 | 셸 기반 후보를 남길지 다른 구성 관리 후보를 찾을지 달라진다. |

질문 수정2건을 새 후보 선택2건과 같은 성공으로 세지 않는다. T042는 의문문이 아닌 넓은 추가 기능 초대다. 이를 제외하면 변화5건이고, 모호한 SQLite 적합성 질문 T039도 제외하면 사람 되묻기35사건/21스레드다. 원질문38사건 중 나머지32개는 unknown, 명시적 동일 추천 유지가 확인된 no는0개다. 따라서6/38은 인과 성공률이 아니다.

‘무엇이 바뀔지’를 말할 수 있다는 AF-RES-001 §6 기준은 [T019](https://softwarerecs.stackexchange.com/questions/95480/looking-for-a-free-open-source-vs-code-ai-coding-assistant-similar-to-github-cop) · [T040](https://news.ycombinator.com/item?id=18542227) · [T056](https://lobste.rs/s/bgsuwg/how_do_you_find_your_software_tools)에서 직접적인 설명력을 가진다. 그러나 [T041](https://www.reddit.com/r/selfhosted/comments/1p80fui/is_there_a_good_uptodate_site_for_finding/)의 어떤 SaaS냐는 질문은 원문에 이미 예시가 있어 추가 가치가 낮다. [T054](https://github.com/mixelpixx/KiCAD-MCP-Server/issues/546)의 버전 질문 뒤 응답이 보이지 않는 것도 필요 없는 질문 또는 대화 단절의 증거가 되지 않는다. “되묻기가 대화를 끊었다”는 강한 반례는 공개 종점만으로 확인되지 않았다.

이 구별은 질문·댓글·편집·답의 순서를 나눈 [M01](https://sailresearch.github.io/sail-website/data/pdfs/2022_An_empirical_study_of_question_discussions_on_Stack_Overflow.pdf), 이용자가 결과를 본 뒤 자발적으로 요구를 보완한 [C08](https://journals.ala.org/index.php/rusq/article/download/3946/4432), 비동기 비응답을 다룬 [C07](https://www.dlib.org/dlib/february03/janes/02janes.html)과 연결된다. [C09](https://crl.acrl.org/index.php/crl/article/view/23611/30924)에서는 명료화와 불만·중립의 양의 관련이 있어 ‘더 물으면 항상 좋다’는 가정을 경계하게 하지만, 어려운 질문·표집·설문 비응답 때문에 인과 방향은 확정되지 않는다. 상세 방법·분모는 [CROSSFIELD.md](CROSSFIELD.md)에 있다.

## Q3. 답은 어떤 형태이고 무엇을 추천하는가

| 주 형식 | 답 단위 /635 | 비율 | 그 형식이 있는 스레드 /61 |
| --- | --- | --- | --- |
| 최소 후보 제시 | 79 | 12.4% | 26 |
| 링크+조건/기능 설명 | 115 | 18.1% | 50 |
| 직접 사용 경험이 주 설명 | 242 | 38.1% | 35 |
| 링크 없는 설명·원리 | 199 | 31.3% | 39 |
| 실제 비교표 | 0 | 0.0% | 0 |

최소 후보 제시79개 중 실제 URL이 있는 것은48개, 이름만 제시한 것은31개다. 특정 조건과의 명시 연결 FIT는 **356/635개**, 그런 답이 하나 이상 있는 스레드는60/61개다. 실제 비교표는0개이며 [T024](https://softwarerecs.stackexchange.com/questions/91466/a-cross-platform-c-library-for-parsing-command-line-arguments)의 요구별 체크리스트는 표와 구별했다. 기능 설명 없이 이름만 놓인 답과, 짧아도 PHP·공개 소스 조건을 말한 [T023](https://softwarerecs.stackexchange.com/questions/91936/looking-for-a-form-generator)의 답은 다르게 코딩했다.

| 답 역할 | 단위 /635 | 존재 스레드 /61 |
| --- | --- | --- |
| 전체 목적을 수행할 앱·서비스 | 204 | 28 |
| 시스템에 넣을 부품 | 202 | 35 |
| 재사용 원리·방법 | 157 | 31 |
| 복수 역할 | 72 | 30 |

역할 표는 기술통계다. 원판 재코딩의 product/component 경계가 특히 약해4역할 일치가50.34%였다. 제품·부품을 합친3범주로는87.92%, 구체 대상 포함/원리만이라는2범주로는93.96%였지만, 사후 합산이 상세 판정 오류를 없앤 것은 아니다. 가장 긴 [T047](https://www.reddit.com/r/golang/comments/1rzhrze/what_message_broker_would_you_choose_today_and_why/) 하나가66답이므로 답 수 비율과 스레드 존재 수를 함께 제시했다.

### 설명과 전이에 대한 반례

[T026](https://softwarerecs.stackexchange.com/questions/90462/library-that-lets-you-write-tests-in-almost-english-like-manner)은 **이름과 URL만 있는 자기 답으로 찾던 라이브러리를 식별했다고 보고한 사례**다. 이는 후보 식별에 긴 설명이 언제나 필요한 것은 아니라는 좁은 반례다. 타인의 링크 추천이 공식 체크표로 채택되거나 통합에 성공한 사례로 확대하지 않는다. [T050](https://sr.reddit.com/r/rails/comments/1t7u9iv/migrating_off_heroku_what_deployment_setups_are/)의 짧은 Kamal 링크에는 읽어보겠다는 반응만 있고 실제 선택은 다른 조합이다. [P03](https://softwarerecs.meta.stackexchange.com/questions/356/what-is-required-for-an-answer-to-be-high-quality)도 링크가 단순 조건을 입증할 수 있으며 직접 사용 경험이 모든 답의 절대 요건은 아니라고 설명한다. [M03](https://ricerca.uniba.it/retrieve/dd9e0c6b-cb83-1e9c-e053-3a05fe0a45ef/1710.04692.pdf)의 미채택 질문 재검토는 공식 채택과 실제 유용성을 같은 변수로 놓지 말아야 할 외부 근거다.

최종 반례 탐색은 더 직접적인 반례를 확보했다. [SXR08](https://softwarerecs.stackexchange.com/questions/90362/is-there-a-file-uploader-like-dreamweavers/90455)은 WinSCP 이름/URL과 일반 권유만 있는 코드북상 **link_only 답이 공식 채택되고 보너스도 받은 사례**다. 정식 답1개라 본표본에는 넣지 않았지만, 공개API의 accepted_answer_id=90455와 해당 답의 is_accepted=true를 본문에 대조했다. 질문자는 모든 기능이 되는 것 같지는 않다고도 말했다. 따라서 설명이 항상 필수라는 가정의 실제 반례인 동시에, 채택이 완전한 요구 충족을 보증하지 않는 사례다.

[SXR09](https://softwarerecs.stackexchange.com/questions/36607/android-app-for-generating-pdf-from-images/36609)에서는 설치해 작동했다는 질문자 발언과 공식 채택을 둘 다 확인했다. 다른 댓글은 link-only라고 불렀으나 답에 짧은 사용 경험과 정렬 기능 설명이 있어 엄격 코드북에서는 experience다. 공동체의 표현과 분석 정의를 맞바꾸지 않았다. [추가 질의](evidence/minimal-answer-counter-search.json)·[공식 메타데이터](evidence/accepted-metadata-attempt.json)·[답 본문 대응](evidence/accepted-answer-mapping.json)에 각각 검색, 현재 선택표, 본문 판정을 남겼다.

다른 제품 기능/분야의 관계를 옮기는 답은 **14개/5스레드**다. [T021](https://softwarerecs.stackexchange.com/questions/86879/is-there-a-decent-open-source-or-low-cost-net-sdk-that-has-functions-for-parsin)의 Word 기능→PDF 라이브러리 작업, [T039](https://news.ycombinator.com/item?id=41072631)의 SQLite/DB→큐, [T047](https://www.reddit.com/r/golang/comments/1rzhrze/what_message_broker_would_you_choose_today_and_why/)의 DB·파일→메시지 전달은 소프트웨어 안의 제품 기능 전용이다. [T035](https://news.ycombinator.com/item?id=29604618)의 Last.fm→자료 추천, [T040](https://news.ycombinator.com/item?id=18542227)의 시각효과 렌더팜→일반 작업 분배는 분야가 다른 비교다. 이14개에는 원질문자의 adopt/reject 반응이 없다. 원리 제시의 존재를 전이 성공률로 바꾸지 않는다.

동일 지식 그래프 대체([T025](https://softwarerecs.stackexchange.com/questions/91241/how-to-access-high-quality-and-accurate-company-logo)), 심장 모니터라는 위험 비유([T036](https://news.ycombinator.com/item?id=16882140)), 책이라는 탐색 채널 변경([T057](https://lobste.rs/s/v7r423/where_can_i_find_old_internet))은 엄격 전이 계수에서 제외했다. [T058](https://lobste.rs/s/0zdh32/does_it_make_sense_switch_github)의 P2P 보관에는 실제 추가 호스트가 있어야 한다는 반박이 있지만 같은 기능 계열의 조건 문제여서 넓은 T 민감도1건으로만 남겼다. PICO 검색 구조 비교([C04](https://jmla.pitt.edu/ojs/jmla/article/download/345/726) · [C05](https://link.springer.com/article/10.1186/s12913-014-0579-0))도 원리를 가져올 때 목적·대상·누락 위험을 그대로 옮길 수 없다는 비교 기준을 제공한다.

## Q4. 채택·추천점수·거절의 이유

### 결과 신호를 먼저 나눈다

| 신호 | 답 단위 | 스레드/구성 | 의미 |
|---|---:|---|---|
| 질문자의 선택·식별·사용 보고 adopt | 10 | 10스레드; 자기 답7개 | 단계가 다르므로 설치 성공10건이 아님 |
| 시험·열람·검토 try | 19 | 13스레드 | 실제 시험과 향후 읽기/검토를 단계로 분리 |
| 질문자의 거절·일부 방안 반박 reject | 14 | 12스레드 | 게시물 전체 채택과 일부 방안 거절은 공존 가능 |
| 감사 thanks | 11 | 답 단위 | 채택 아님 |
| 질문자 반응 없음 none | 577 | 답 단위 | 실패·거절 아님 |
| 질문자 신원/반응 불명 unknown | 4 | 답 단위 | 추정하지 않음 |
| 현재 최대 점수 답 표시 | 53 | 41스레드; 동점·0점 포함 | 투표자의 동기는 관측되지 않음 |
| 공식 accepted 표식 | 7 true /78 false | SR30질문의 정식답85;댓글4는해당없음 | 익명 공개API의 현재값;다른플랫폼은미노출null |

본문 도구에서 표식이 빠졌으나 최종 익명 공개API 조회가 성공해 SR30질문의 정식 답85개를 보완했다. 현재 채택은7개, 나머지78개는 현재 미채택이며, 같은30개 질문의 API 답 수와 코딩한 정식 답 수가 모두 일치했다. 댓글 추천4개에는 게시물 채택표가 적용되지 않는다. 이것은 응답 형식이나 명시 사용 보고를 바꾸는 새 코딩이 아니라 결과 신호의 보강이다.

| 공식 채택 사례·답ID | 채택된 답의 적합 근거 | 질문자의 채택 이유를 어디까지 알 수 있는가 |
|---|---|---|
| T004 ·39981 | BiblioteQ 무료·오프라인·단일 운영 | 자기 답이 요구 충족과 작은 단점을 직접 설명 |
| T005 ·42908 | LAMP/LAPP·Laravel·Angular 조합의 보안·반응형·학습 근거 | 답변자의 근거다. 질문자는 다른 Vaadin 답에도 검토 의향을 보임 |
| T010 ·39104 | 익숙한 언어·주변 공동체, 시각 디자인과 프레임워크의 분리 | 특정 제품명보다 선택 원리를 채택; 직접 채택 동기는 별도 발언 없음 |
| T016 ·91604 | filer.dev의 오프라인·OS·무료 일괄 변환 주장 | 현재 채택표가 있지만 후속502댓글도 있어 유효성 보증은 아님 |
| T022 ·94873 | LanguageDetection 포크의 .NET8 빌드·통합 | 질문자가 자기 실행 경험을 보고 |
| T023 ·93493 | Form Tools의 PHP/MySQL·양식·모듈 구성 | 사용을 시도하겠다는 자기 답이 채택; 실제 통합 성공은 아님 |
| T027 ·87705 | 위치DB 조회와 국가 직접 입력을 함께 제시 | 국가 직접 입력 방안은 질문자가 반박했지만 DB 대안도 있는 답 게시물은 채택 |

이 표의 근거는 [공식 답 대응 원장](evidence/accepted-answer-mapping.json)이다. 채택을 한 사람의 동기를 답변자의 설명으로 대신하지 않는다. 특히 T027은 **게시물 단위 채택과 그 안의 한 방안 거절이 공존**하므로 rejection_targets를 사용자 직접 입력에 한정했다.

선택·사용 보고10개의 이유와 단계는 다음과 같다. 선택이 특정 타인의 답 때문에 일어났다고 가정하지 않는다.

| 사례 | 선택·사용 대상 | 확인된 이유/단계 |
|---|---|---|
| [T002](https://softwarerecs.stackexchange.com/questions/37143/open-source-gui-program-for-producing-plots-graphs) | Veusz | 장기 사용·요구 충족 보고; 자기 답에서 QtiPlot 삭제와 별개 |
| [T004](https://softwarerecs.stackexchange.com/questions/39255/simple-and-free-book-library-management-system-ils-for-a-small-library) | BiblioteQ | 가장 맞는 해결책 식별; 불필요한 입력칸도 인정 |
| [T013](https://softwarerecs.stackexchange.com/questions/52849/read-powerpoint-ppt-file) | PPT→PDF→텍스트 | 느려도 자기 용도에 작동한다는 방법 사용 보고 |
| [T018](https://softwarerecs.stackexchange.com/questions/76875/translation-tool-for-desktop-with-glossary) | OmegaT | 완벽하지 않아도 Word 문서에 실제 사용 |
| [T022](https://softwarerecs.stackexchange.com/questions/94872/human-language-detection-library-for-c) | LanguageDetection 포크 | .NET8 빌드·DLL 통합 성공을 질문자가 보고 |
| [T026](https://softwarerecs.stackexchange.com/questions/90462/library-that-lets-you-write-tests-in-almost-english-like-manner) | SpecFlow | 찾던 라이브러리 식별; 설치 보고 아님 |
| [T038](https://news.ycombinator.com/item?id=41756808) | Playwright | 이미 익숙하므로 시작하겠다는 계획 |
| [T049](https://th.reddit.com/r/golang/comments/1uktfq6/any_good_image_validation_libs_for_go/?sort=confidence) | OWASP 방어 절차 | 구현 중 보고; 업로드 안전성 검증 결과 아님 |
| [T050](https://sr.reddit.com/r/rails/comments/1t7u9iv/migrating_off_heroku_what_deployment_setups_are/) | Hetzner+Hatchbox | 후일 사용·만족 보고; 첫 질문에도 있던 후보 |
| [T061](https://ru.reddit.com/r/selfhosted/comments/1q7jbx1/anyone_using_mediamanager_over_the_arr_apps/?sort=random) | 선택적 수동 작업 | 세밀한 선택은 수동, 덜 중요한 것은 자동화한다는 자기 사용 보고 |

[T050](https://sr.reddit.com/r/rails/comments/1t7u9iv/migrating_off_heroku_what_deployment_setups_are/)에서는 최다 추천 답이 Render 경험담인 반면 질문자의 보고는 Hetzner+Hatchbox다. 최다 추천·질문자 선택을 합치면 이 차이가 사라진다. [M02](https://www.mdpi.com/2306-5729/11/3/58)의 ‘성공 답변’ 범주는 닫힌 질문까지 포함하므로 채택률로 가져오지 않았고, [M03](https://ricerca.uniba.it/retrieve/dd9e0c6b-cb83-1e9c-e053-3a05fe0a45ef/1710.04692.pdf)의 미채택100개 중38개에 유용/해결 답이 있었다는 결과도 지표 구별을 지지한다.

### L/E/H/T와 추가 이유

| 코드·이유 | 비판 포함 답 단위 | 스레드 | 대표 사례 |
| --- | --- | --- | --- |
| L 주소·출처를 찾을 수 없음 | 2 | 2 | T002 AlphaPlot 링크 요청; T016 filer.dev 502 보고 |
| E 사실 주장에 대한 반박 | 13 | 12 | T039 삽입형/별도 서버 구별; T061 개발 의도 주장 반박 |
| H 명시 필수조건 위반 | 15 | 12 | T001 Discord, T004 Librarika; 후속 명료화는 별도 |
| T 엄격한 타분야 전이 조건 실패 | 0 | 0 | 0; T058 같은 계열 보관 조건은 넓은 T 경계로만 보존 |
| M 유지보수·프로젝트 수명 | 14 | 9 | T048 업데이트 지연, T052 대안 라이브러리의 유지 불확실성·오래 열린 PR |
| C 생태계·공동체·지원 | 12 | 9 | T058 네트워크 효과, T061 지원·지속성 우려 |
| P 가격·운영비 | 9 | 8 | T040 실행 비용, T050 배포 비용 |
| LIC 공개성·사용권 | 8 | 8 | T017 LEDA, T048 폐쇄 OS에 대한 우려 |
| TRUST 보안·개인정보·벤더 신뢰 | 16 | 12 | T027 사용자 자기신고 불신, T048 데이터 보관 위험 |
| UX 학습·운영 부담·편의 | 55 | 17 | T058 자가호스팅 관리 부담, T061 여러 UI |
| EXP 써 본 경험·기존 투자 | 33 | 12 | T035 빈 화면 시험, T061 설치·업데이트 경험 |
| OTHER 설명/예제 부족·범주/논리 이견 등 | 22 | 19 | T023 설명 요구, T006 Q&A/포럼 범주 이견 |

다중 코딩이므로 행을 합산하지 않는다. 이는 **비판·배제·우려가 붙은 답**의 수이며 모두 원질문자가 실제 거절한 제품 수가 아니다. 뒤늦게 드러난 조건에 대한 H, 다른 독자의 H, 원질문자의 H도 [근접 오답 원장](evidence/near-misses.json)에서 구별한다. [T024](https://softwarerecs.stackexchange.com/questions/91466/a-cross-platform-c-library-for-parsing-command-line-arguments)처럼 자기 답에 미지원만 표시한 경우는 condition_failures에 남기고 rejection_codes에서는 뺐다.

L/E/H/T 밖 코드만 있는 답102개/32스레드가 있었다. 특히 [T048](https://es.reddit.com/r/DataHoarder/comments/iqzq44/alternative_to_storage_spaces/?sort=old)의 Xpenology는 업데이트 지연·폐쇄 OS에 데이터 맡기기·과거 사용 경험 때문에 거절됐지만, 그 항목들이 처음부터 명시 필수였던 것은 아니다. [T058](https://lobste.rs/s/0zdh32/does_it_make_sense_switch_github)에서는 기능이 충분해도 공동체, CI, 운영 시간 때문에 다른 선택을 유지한다. 가격·라이선스도 명시 must이면 H와 함께 기록하고, 후속 선호·위험평가이면 별도 이유로 둔다. 모든 선택 이유를 사후 H로 바꾸면 처음 입력이 무엇이었는지를 잃는다.

L 감사도 경계를 바꿨다. [T023](https://softwarerecs.stackexchange.com/questions/91936/looking-for-a-form-generator) · [T026](https://softwarerecs.stackexchange.com/questions/90462/library-that-lets-you-write-tests-in-almost-english-like-manner) · [T028](https://softwarerecs.stackexchange.com/questions/85007/is-there-a-whatsapp-library-like-sulla-but-for-python) · [T029](https://softwarerecs.stackexchange.com/questions/84968/seeking-c-logging-software-to-record-exceptions-possible-errors-etc)의 링크가 있는 답에 요구 대응이나 예제를 보강하라는 요청은 OTHER다. [T016](https://softwarerecs.stackexchange.com/questions/80653/offline-batch-conversion-of-heic-to-jpg-while-preserving-metadata-exif)의 봇 보강 요청까지 넓게 L로 합치면 L은3개가 되지만, 주 표에서는 실제 출처·주소 문제2개만 셌다. 사실 반박 E도 참여자의 반박이 존재했다는 뜻이며 연구자가 제품의 해당 버전을 실행해 진위를 확정했다는 뜻은 아니다. SR 답변 규범([P03](https://softwarerecs.meta.stackexchange.com/questions/356/what-is-required-for-an-answer-to-be-high-quality))과 낡은 답의 실증 연구([M04](https://arxiv.org/pdf/1903.12282))를 이 구별에 함께 사용했다.

## Q5. 표면상 비슷하지만 핵심 조건에 어긋난 실제 후보

검토한 후보–조건 쌍은19개/12스레드다. 추천 시점에 이미 알려진 조건과 실제 반박을 엄격히 연결한 것은 **16쌍/11스레드**다. 이 중 본표본10쌍/8스레드, 보완 관측6쌍/3스레드다. 보완 자료는 일부 접힌 댓글 때문에61개 빈도에 넣지 않았지만, 표에 쓴 질문 조건과 반박 본문은 직접 읽었다. 같은 스레드에서 여러 후보가 탈락한 것과 서로 다른 스레드 수를 구별한다.

| 쌍 ID | 스레드 | 후보 | 어긋난 핵심 조건 | 분모 | 반박자 |
| --- | --- | --- | --- | --- | --- |
| NM01 | [T001](https://softwarerecs.stackexchange.com/questions/75118/alternative-to-slack) | Discord | 서버와 클라이언트 모두 공개 소스 | 본표본 | 질문자/자기 답 |
| NM02 | [T002](https://softwarerecs.stackexchange.com/questions/37143/open-source-gui-program-for-producing-plots-graphs) | QtiPlot | 공개 소스 그래프 GUI | 본표본 | 질문자/자기 답 |
| NM03 | [T004](https://softwarerecs.stackexchange.com/questions/39255/simple-and-free-book-library-management-system-ils-for-a-small-library) | Librarika | 무료로 한 컴퓨터에서 오프라인 운영 | 본표본 | 질문자/자기 답 |
| NM04 | [T017](https://softwarerecs.stackexchange.com/questions/30347/a-modernish-c-graph-representation-and-manipulation-library) | LEDA | 공개 소스 그래프 라이브러리 | 본표본 | 질문자/자기 답 |
| NM05 | [T033](https://news.ycombinator.com/item?id=41608459) | GitHub Pages | 설치·운영할 공개 소스 블로그 소프트웨어 | 본표본 | 질문자/자기 답 |
| NM06 | [T040](https://news.ycombinator.com/item?id=18542227) | S3 이벤트 + Lambda | 한 작업이 최대 약1시간 실행 | 본표본 | 질문자/자기 답 |
| NM07 | [T043](https://www.reddit.com/r/selfhosted/comments/opgyga/any_self_hosted_alexas_or_similar/) | Mycroft | 이미 쓰는 Mycroft 외의 대안 | 본표본 | 삭제 계정·신원 미확정 |
| NM08 | [T044](https://www.reddit.com/r/selfhosted/comments/5ge434/lf_selfhosted_alternative_to_teamviewer_or_logmein/) | Guacamole | 대상 Windows 방화벽을 개별 설정하지 않는 중앙 원격접속 | 본표본 | 다른 독자 |
| NM09 | [T044](https://www.reddit.com/r/selfhosted/comments/5ge434/lf_selfhosted_alternative_to_teamviewer_or_logmein/) | TeamViewer 우회 사용 | 자가 호스팅 원격접속 | 본표본 | 다른 독자 |
| NM10 | [T044](https://www.reddit.com/r/selfhosted/comments/5ge434/lf_selfhosted_alternative_to_teamviewer_or_logmein/) | mRemoteNG | 연결 설정·도달성을 제공할 원격접속 방식 | 본표본 | 다른 독자 |
| NM12 | [SX01](https://softwarerecs.stackexchange.com/questions/35392/an-open-alternative-for-evernote?noredirect=1) | NixNote/NeverNote | Evernote 서버 생태계를 떠날 수 있어야 함 | 보완·부분 열람 | 질문자/자기 답 |
| NM13 | [SX01](https://softwarerecs.stackexchange.com/questions/35392/an-open-alternative-for-evernote?noredirect=1) | Dropbox Paper | 자기 파일로 보유·외부 처리할 수 있어야 함 | 보완·부분 열람 | 질문자/자기 답 |
| NM14 | [SX01](https://softwarerecs.stackexchange.com/questions/35392/an-open-alternative-for-evernote?noredirect=1) | Turtl | 데이터의 공개 형식과 특정 앱에서의 독립성 | 보완·부분 열람 | 질문자/자기 답 |
| NM15 | [SX08](https://softwarerecs.stackexchange.com/questions/84072/transform-text-into-gibberish-while-maintains-the-look-of-the-original-text) | Markov-chain text generation | 기존 텍스트 단어 길이 대응 보존 | 보완·부분 열람 | 질문자/자기 답 |
| NM18 | [SXR05](https://softwarerecs.stackexchange.com/questions/26907/command-line-option-parser-for-java) | picocli, 2017 응답 당시 | 사전에 옵션을 정의하지 않고 임의 옵션 수용 | 보완·부분 열람 | 질문자/자기 답 |
| NM19 | [SXR05](https://softwarerecs.stackexchange.com/questions/26907/command-line-option-parser-for-java) | args4j | 옵션 이름을 미리 정의하지 않고 String/String[]에서 임의 옵션과 값을 추출 | 보완·부분 열람 | 질문자/자기 답 |

대상 범주만 맞추면 서버 공개성, 오프라인 운영, 이미 사용한 제품 제외, 설치 제품과 호스팅의 차이, 실행시간, 임의 옵션이라는 핵심을 놓친다. 이 사례는 AF-RES-004의 **SURFACE_OR_CONSTRAINT_MISMATCH** 경계를 지지한다. 상용이라는 표현만으로 비공개 소스가 논리적으로 증명되는 것은 아니므로 QtiPlot의 기록은 참여자가 당시 공개성 위반으로 판단해 제거한 사건으로 한정했다.

반대로 세 종류를 제외했다. 첫째, [T006](https://softwarerecs.stackexchange.com/questions/1841/a-framework-for-question-answers-forum)의 Discourse는 Q&A와 포럼의 범주 해석에 대한 의문형 이견이므로 엄격 H가 아니다. 둘째, [T035](https://news.ycombinator.com/item?id=29604618) TinyGem의 빈 화면은 실제 시험의 문제지만 선택 철회·구조적 기능 부재가 확인되지 않았다. 셋째, [SXR05](https://softwarerecs.stackexchange.com/questions/26907/command-line-option-parser-for-java)의 GetOpt와 [SXR07](https://softwarerecs.stackexchange.com/questions/34740/open-source-speech-to-text-software-for-audio-files-in-english)의 YouTube는 조건이 답 뒤 명료화됐으므로 과거 답을 처음부터 틀렸다고 하지 않았다. SXR05의 args4j/picocli에는 그 조건이 이미 알려져 있었지만, Map 반환은 비필수 선호다.

[SX08](https://softwarerecs.stackexchange.com/questions/84072/transform-text-into-gibberish-while-maintains-the-look-of-the-original-text)의 Markov 제안은 최초 수정판의 길이 보존 조건으로 확인했다. Fillerama/Smodin은 ‘기존 텍스트 변환’ 표현이 뒤에 보강된 경계이며 같은 반박을 두 번 세지 않으려고 엄격16쌍에서는 제외했다. [T061](https://ru.reddit.com/r/selfhosted/comments/1q7jbx1/anyone_using_mediamanager_over_the_arr_apps/?sort=random)의 다른 독자 자막 필수성도 별도 보완 반응으로 남겼다. 수정 이력과 재열람 범위는 [timing audit](evidence/near-miss-timing-audit.json)에 있다. 요구를 명시하라는 규칙([P04](https://softwarerecs.meta.stackexchange.com/questions/48/how-to-ask-for-an-alternative-to-some-software))과 질문·답 갱신을 구별한 연구([M01](https://sailresearch.github.io/sail-website/data/pdfs/2022_An_empirical_study_of_question_discussions_on_Stack_Overflow.pdf) · [M04](https://arxiv.org/pdf/1903.12282))는 왜 이 시간 경계가 필요한지 설명한다.

## Q6. 오래된 답과 추천 링크의 현재 상태

추천 관련 주소 **281회/고유 URL279개**를 단회 관측했다. fragment만 다른 주소는 같은 문서로 합쳤다. 원문에 하이퍼링크가 없는 이름 제시는 D1 not_linked이며 아래 접속 분모에서 제외했다. 추가 IP2Location 도메인1건은 원문 도메인에 HTTPS 스킴을 붙여 관측한 것으로, 원문 하이퍼링크와 구별해 저장했다.

| 단회 상태 | 관측 행 | 고유 URL | 해석 |
| --- | --- | --- | --- |
| 접속 가능 | 202 | 200 | 기능·유지·정확성 보증 아님 |
| 이동 | 36 | 36 | 옛 주소와 현재 목적지 구별 |
| 보관 표면 | 2 | 2 | Archive 위치1 + 소유자 보관 배너1 |
| 접속 실패 | 21 | 21 | 명시404 4개 + 다른/미상 오류17개 |
| 도구 접근 차단 | 20 | 20 | 원격 사이트의 소실로 세지 않음 |

명시404는4개 URL/3스레드([T035](https://news.ycombinator.com/item?id=29604618) · [T043](https://www.reddit.com/r/selfhosted/comments/opgyga/any_self_hosted_alexas_or_similar/) · [T051](https://github.com/perses/perses/discussions/3862))이고410은0개다. 나머지 실패17개와 차단20개를 죽은 링크37개로 바꾸지 않았다. T016은 현재 공식 채택을 유지하면서502댓글과접속실패가있어,채택표와현재근거접근성도별개임을보인다. T043의 두404는 Mycroft 시작 문서와 음성 인식 하드웨어 범주 주소이므로, Mycroft 제품과 모든 관련 기능이 죽었다는 결론도 아니다.

역사 발언 중 특정 추천·회피 대상의 명시 관리/유지지원 중단은3스레드였다: [T011](https://softwarerecs.stackexchange.com/questions/16368/get-alerts-with-diffs-of-web-page-changes) Specto, [T049](https://th.reddit.com/r/golang/comments/1uktfq6/any_good_image_validation_libs_for_go/?sort=confidence) nfnt/resize, [T061](https://ru.reddit.com/r/selfhosted/comments/1q7jbx1/anyone_using_mediamanager_over_the_arr_apps/?sort=random) Huntarr. 긍정/조건부 추천만 남기면2개이고, 처음 대체하려던 원본 [T022](https://softwarerecs.stackexchange.com/questions/94872/human-language-detection-library-for-c) · [T052](https://github.com/knolleary/pubsubclient/issues/1095)까지 포함하면5개다. PHP IMAP 확장 폐기([T055](https://github.com/osTicket/osTicket/issues/7002))는 전체 프로젝트 관리 중단과 분리했다.

| 오래됨의 관측 정의 | 스레드 수 /61 |
|---|---:|
| 특정 추천·회피 대상의 명시 유지중단 발언 또는 현재 보관/404 | 7 |
| 기본7 + Codepundit 개발 중지 요약1 | 8 |
| 기본7 + 기존 교체 대상2 | 9 |
| 기본7 + 기존 교체 대상2 + 구성요소 폐기1 | 10 |
| 특정 대상의 넓은 노후화 신호까지 포함한 별도 합집합 | 16 |

[T058](https://lobste.rs/s/0zdh32/does_it_make_sense_switch_github)의 soft-serve는 스레드 시작 뒤인2026-10-26 소유자 보관 배너가 있었다. [T011](https://softwarerecs.stackexchange.com/questions/16368/get-alerts-with-diffs-of-web-page-changes)은 Google Code Archive 위치라 배너와 다른 상태다. [T034](https://news.ycombinator.com/item?id=7798545)의 Codepundit는 도메인 판매 페이지로 이동했으므로 HTTP200만으로 원래 추천 내용이 보존됐다고 할 수 없다. 또 [T011](https://softwarerecs.stackexchange.com/questions/16368/get-alerts-with-diffs-of-web-page-changes)에서는 관리가 멈춘 도구를 계속 사용하는 경험이 있었고, [T036](https://news.ycombinator.com/item?id=16882140)에서는 성숙해 커밋이 드문 프로젝트와 실제 미처리 문제를 구별하라고 했다.

이 집계는 [aging-observations.json](evidence/aging-observations.json)의 역사27행·현재44행 감사와 연결된다. [M04](https://arxiv.org/pdf/1903.12282)는 채택 답도 낡을 수 있음을, [M05](https://sail.cs.queensu.ca/data/pdfs/2021_Broken_External_Links_on_Stack_Overflow.pdf)는 여러 시점·위치의 링크 확인이 필요함을 보여준다. 현재 단면만 있는 이 연구는 추천의 생존율이나 시간에 따른 악화율을 산출하지 않았다.

## Q7. 전체 구조 없이 일부만 물어도 쓸 만한 답을 받는가

부분 질문은33개다. 그중 선택·식별·구현 중·사용 보고가 있는6개는 [T013](https://softwarerecs.stackexchange.com/questions/52849/read-powerpoint-ppt-file) · [T022](https://softwarerecs.stackexchange.com/questions/94872/human-language-detection-library-for-c) · [T026](https://softwarerecs.stackexchange.com/questions/90462/library-that-lets-you-write-tests-in-almost-english-like-manner) · [T038](https://news.ycombinator.com/item?id=41756808) · [T049](https://th.reddit.com/r/golang/comments/1uktfq6/any_good_image_validation_libs_for_go/?sort=confidence) · [T050](https://sr.reddit.com/r/rails/comments/1t7u9iv/migrating_off_heroku_what_deployment_setups_are/)다. T013·T022는 자신에게 작동했다는 보고, T050은 사용·만족, T049는 구현 중, T038은 계획, T026은 후보 식별이다. 이를 모두 실제 통합 성공으로 부르지 않는다.

현재 공식 채택이 있는 부분 질문은 T005/T010/T022/T023/T027의5개다. 명시 선택·사용 보고6개와는 T022만 겹쳐 합집합은10/33이지만, 이를10개의 검증된 사용 성공으로 부르지 않는다. 특히 T010은 원리 답, T023은 시험 계획, T027은 일부 방안 반박을 포함한 답의 채택이다.

| 부분 질문 사례 | 주어진 좁은 범위 | 답이 진전시킨 부분 |
|---|---|---|
| [T013](https://softwarerecs.stackexchange.com/questions/52849/read-powerpoint-ppt-file) | PowerPoint 파일에서 텍스트 추출 | PDF 경유 방법이 자기 용도에 작동한다는 보고 |
| [T022](https://softwarerecs.stackexchange.com/questions/94872/human-language-detection-library-for-c) | .NET 언어 판별 부품 | 직접 빌드한 포크와 DLL 통합 보고 |
| [T049](https://th.reddit.com/r/golang/comments/1uktfq6/any_good_image_validation_libs_for_go/?sort=confidence) | 이미지 검증·크기 조정 부품 | 처리 절차와 특정 함수를 나누어 구현 중·수정 의향 보고 |
| [T047](https://www.reddit.com/r/golang/comments/1rzhrze/what_message_broker_would_you_choose_today_and_why/) | 메시지 브로커 | 필요한 보장·규모에 따른 조건부 후보; 질문자의 선택은 없음 |
| [T053](https://github.com/rlemaigre/vue3-promise-dialog/issues/15) | Vue3에서 쓸 구성요소 | 저장소 맥락이 일부 정보를 제공; 질문 본문만의 빈칸과 구별 |

반대 사례도 있다. [T009](https://softwarerecs.stackexchange.com/questions/84965/a-framework-to-build-an-interactive-website)의 MongoDB, [T015](https://softwarerecs.stackexchange.com/questions/90398/simple-and-open-source-or-free-tool-to-add-captions-to-gif-images)의 macOS, [T040](https://news.ycombinator.com/item?id=18542227)의 Java는 나중에 드러나 먼저 제시된 후보의 적용 범위를 바꿨다. 필요한 것은 전체 설계서가 아니라 **그 부분의 후보를 가르는 주변 환경**이었다. [T048](https://es.reddit.com/r/DataHoarder/comments/iqzq44/alternative_to_storage_spaces/?sort=old)에서도 같은 저장 계층 안에서 무결성 복구와 패리티 갱신의 의미를 물어야 했다.

[SXR02](https://www.reddit.com/r/devops/comments/1i5sk7r/what_do_you_recommend_i_should_use_for_making_my/)는 모호한 CI/CD 요청에서도 이미 GitHub에 코드를 둔 맥락과 연결해 Actions를 선택하겠다는 반응이 나온 보완 반례다. 현재 조건을 완벽히 쓰지 못했다는 이유만으로 답 전체를 중지할 필요가 있다는 가정과 맞지 않는다. [SXR06](https://softwarerecs.stackexchange.com/questions/36505/self-hosted-open-source-alternative-for-packagecloud-io)은 꽤 좁은 부분 요청이면서도 닫혀 정식 답을 못 받았고 댓글에는 후보가 있었다.

AF-RES-001의 **부분 질문을 막을 필요는 없다**는 판단은 이 범위에서 지지된다. 참고 면담의 사용 목적 확인([C01](https://crl.acrl.org/index.php/crl/article/download/12027/13473) · [C02](https://c3s.weebly.com/uploads/4/7/3/5/4735750/neutral_questions.pdf) · [C03](https://www.ala.org/sites/default/files/rusa/content/Guidelines%20for%20Behavioral%20Performance%20of%20Reference%20and%20Information%20Service%20Providers%202023.pdf))과 PICO 필터의 누락 위험([C04](https://jmla.pitt.edu/ojs/jmla/article/download/345/726) · [C05](https://link.springer.com/article/10.1186/s12913-014-0579-0))은 주변 정보만 선택적으로 확인하는 비교 근거다. 현재 관측은 어떤 부분 질문이든 유용한 답을 보장한다거나, 질문자 응답 없이 자동 통합까지 가능하다는 주장은 지지하지 않는다.

## Q8. 플랫폼 규칙은 품질을 높이는가, 질문을 막는가

| 플랫폼·규칙 | 규칙이 요구하거나 금지하는 것 | 스레드에서 보인 경로 |
|---|---|---|
| SR [P01](https://softwarerecs.stackexchange.com/help/on-topic) · [P02](https://softwarerecs.meta.stackexchange.com/questions/336/what-is-required-for-a-question-to-contain-enough-information) · [P04](https://softwarerecs.meta.stackexchange.com/questions/48/how-to-ask-for-an-alternative-to-some-software) | 과업·객관적 조건·바꿀 이유; 기술 선택 일반론과 특정 소프트웨어 요청 구별 | T021 예산 보완, T027 목적/환경 질문; SX07·SXR06 폐쇄 |
| SR 답변 [P03](https://softwarerecs.meta.stackexchange.com/questions/356/what-is-required-for-an-answer-to-be-high-quality) | 요구 대응·설정·단점; 무설명 홍보/링크 답 제재 | T023 질문자가 설명 보강 요구, T028 삭제 가능성 안내 |
| SO [P05](https://stackoverflow.com/help/on-topic) · [P06](https://stackoverflow.com/help/dont-ask) · [P07](https://meta.stackoverflow.com/questions/417476/question-close-reasons-definitions-and-guidance/417482) · [P08](https://meta.stackoverflow.com/questions/254393/what-exactly-is-a-recommendation-question) | 외부 자원 추천을 의견·스팸·노후화 이유로 제한; 구체 문제 풀이에 라이브러리를 답하는 것은 허용 | T034는 추천을 물을 장소의 제약을 언급; SR/다른 커뮤니티로 이동하는 맥락 |
| selfhosted·devops [P09](https://www.reddit.com/r/selfhosted/) · [P10](https://www.reddit.com/r/devops/) | 이미 시도한 것·막힌 곳·자체 맥락·링크 설명·이해관계 | T041–T045의 요구 확인과 조건부 답; SXR01의 스팸 잠금 |
| softwarearchitecture·ExperiencedDevs [P11](https://www.reddit.com/r/softwarearchitecture/) · [P12](https://www.reddit.com/r/ExperiencedDevs/) | 아키텍처 주제/홍보 제한; 현재 경험7년·단순 검색형 도구 질문 제한 | 같은 Reddit이라도 추천 질문의 진입 조건이 다름 |
| golang·DataHoarder [P13](https://www.reddit.com/r/golang/) · [P14](https://www.reddit.com/r/DataHoarder/) | 관련성·건설적 답; 사전 검색·보관 맥락과 전문 기술 질문 | T047–T049의 전달 보장·저장 무결성·업로드 처리 대화 |
| rails·nextjs [P15](https://www.reddit.com/r/rails/) · [P16](https://www.reddit.com/r/nextjs/) | 경청·건설적 반론 또는 노력·관련성·홍보 경로 | T050과 보완 SUP-R18-07; 통일된8칸 입력 양식은 아님 |

품질 보완과 차단은 둘 다 직접 보였다. [T021](https://softwarerecs.stackexchange.com/questions/86879/is-there-a-decent-open-source-or-low-cost-net-sdk-that-has-functions-for-parsin)은 예산을 추가했고 [T023](https://softwarerecs.stackexchange.com/questions/91936/looking-for-a-form-generator)은 짧은 답을 비판한 질문자가 뒤에 조건 설명을 붙인 자기 답을 썼다. 반대로 [SX07](https://softwarerecs.stackexchange.com/questions/84859/leaflet-vs-maplibre)은 안정성·유지·문서·커뮤니티·WebGL 축을 이미 제시했지만 제품 간 비교 방식이라는 이유로 닫혔다. 질문자는 GIS에서 SR로 보내졌다고 말했고 정식 답은0개다. [SXR06](https://softwarerecs.stackexchange.com/questions/36505/self-hosted-open-source-alternative-for-packagecloud-io)은 공개 소스·자가 호스팅·deb/rpm·배포판 버전을 적었는데도 더 구체적 요구가 필요하다는 사유로 닫혔으며, 댓글에는 Pulp 후보가 있다.

[SXR01](https://www.reddit.com/r/selfhosted/comments/1jvc3b8/selfhosted_alternative_to_markupio/)의 잠금은 정보 양식보다 반복 홍보·스팸 때문이라고 명시돼 있어 ‘너무 엄격한 질문 양식’의 사례에 합치지 않았다. [P02](https://softwarerecs.meta.stackexchange.com/questions/336/what-is-required-for-a-question-to-contain-enough-information)와 [P08](https://meta.stackoverflow.com/questions/254393/what-exactly-is-a-recommendation-question)의 메타 토론에는 품질 기준을 지지하는 의견과 유용한 질문까지 막는다는 반론이 함께 있다. [M02](https://www.mdpi.com/2306-5729/11/3/58)가 폐쇄를 성공 범주에 포함한 점은 운영 지표와 질문자의 목표가 다를 수 있음을 보여준다.

따라서 **품질을 높이려는 규범과 실제 정보 보완은 관측됐고, 규칙에 의한 질문 폐쇄도 관측됐다. 순효과는 관측되지 않았다.** 답2개 이상을 고른 본표본만으로 규칙의 성공률을 계산하면 닫히거나 무응답인 질문을 미리 제외하는 오류가 된다. 2026년 현재 읽은 Reddit 규칙을 과거 게시물 당시 규칙으로 소급하지 않았다.

## 9. 고정 입력에 대한 항목별 판정

### AF-RES-001 정보 후보8개

판정은 정보의 **보존·확인 가치**에 관한 것이며8칸 필수화의 효과가 아니다. 선행 연구를 재요약하거나 새로운 정보표로 교체하지 않았다.

| 후보 | 판정 | 이번 관측이 보탠 것 | 사례·비교 근거 |
|---|---|---|---|
| I1 원문/고정 위치 | 관측 없음 | 연구자가 모든 URL을 수집했으므로 사용자 입력의 필수성 효과는 시험하지 못함. 수정판·관측 시각은 비교 재현에 필요 | T061, SX08 revision; M01 |
| I2 목적/불편 | 지지 | 기능 명칭과 실제 용도의 차이를 설명하지만 존재61/61은 포함 기준 영향 | T027, T049; C01·C02 |
| I3 선택 범위 | 지지·보완 | 설치 소프트웨어·호스팅·일부 계층을 나누고 이미 쓰는 대상 재추천을 막아야 함 | T033, T043; P04 |
| I4 명시 조건 | 지지·보완 | 대상·부정·강제성·누가 언제 말했는지를 함께 보존해야 H 과대판정을 피함 | T001, T017, SXR05; P02 |
| I5 주변 입출력 | 지지 | 전체 구조 대신 해당 부품의 경계·보장·연동을 물을 가치 | T047–T049; C06 |
| I6 지위/시점 | 지지·보완 | 계획·실제 사용·현재 코드 상태와 과거 추천을 구별 | T038, T050, SXR05; M01·M04 |
| I7 버전/설정/자료형 | 지지·보완 | 후보를 바꾸는 실제 환경은 유용하지만 일반 예시·저장소 문맥·정확한 버전을 혼합하지 않음 | T019, T022, T039, T053; C06 |
| I8 해석–원문 관계 | 관측 없음 | 독립 질문53개에 해당 없음; 필수성·효과를 검증할 자료가 부족. 원문/추론 분리 원칙은 유지 | T061, T036 재코딩; C02 |

§6의 ‘답이 바꾸는 판단을 쓸 수 있어야 한다’는 기준은 T019/T040/T056이 지지한다. 하지만 조건부 잠정 답을 먼저 줄 수 있다는 T047/SXR02 때문에 ‘정보가 없으면 무조건 대기’라는 확장은 지지하지 않는다. §7 추측 정지는 무응답→실패, 링크 접근→유지, 계획→적용 성공, 나중 조건→과거 오답으로 넘어가지 않는 데 적용했다.

### AF-RES-004 판정 축4개

| 축 | 판정 | 실제 구별과 적용 경계 | 사례·추가 근거 |
|---|---|---|---|
| L 출처·링크 | 지지·보완 | 실제 주소/출처 문제와 설명 보강을 구별; 현재 fetch 실패와 역사 반박도 별도 | T002/T016 대 T023/T026; P03·M05 |
| E 사실 주장 | 지지·보완 | 주장에 대한 실제 반박이 있고 조건·시점이 중요. 반박 존재가 곧 사실 판정 승리는 아님 | T039, T061; M04 |
| H 필수조건 | 지지 | 추천 전 핵심조건이 실제 후보 탈락을 가름. 선호·나중 조건·부분 미지원은 별도 | 엄격16쌍/11스레드; P02·P04 |
| T 타분야 전이 조건 | 관측 없음 | 제안14개는 있지만 해당 원질문자의 실제 수용/거절 없음. 같은 계열 P2P 조건을 넓게 T로 볼 때1경계 사례 | T021/T035/T039/T040/T047; T058 경계; C04·C05 |

DIRECT_DOCUMENTED를 질문자의 채택만으로 부여하지 않았고, 무반응을 INSUFFICIENT나 SURFACE 실패로 일괄 바꾸지 않았다. CONDITIONAL_TRANSFER의 후보가 있다는 것과 전이 성공의 실증은 다르다. ‘4축이면 사람의 모든 채택·거절 이유를 설명한다’는 확대 가정은 추가 이유102답 때문에 반박된다. 이는 고정 입력 AF-RES-004가 그 확대 가정을 이미 했다는 주장이 아니다.

## 10. 민감도와 내부 별도 재코딩의 영향

| 민감도 표본 | n | 전체/부분 | 답 단위 | 부분 질문의 선택·사용 보고 스레드 | 4축 밖 이유만 있는 답 단위 |
| --- | --- | --- | --- | --- | --- |
| 주 분석 | 61 | 28/33 | 635 | 6 | 102 |
| 헤더 수 차이3개 제외 | 58 | 28/30 | 557 | 4 | 89 |
| 복구 URL T061 제외 | 60 | 27/33 | 608 | 6 | 89 |
| 범위 경계 T057 제외 | 60 | 27/33 | 605 | 6 | 98 |
| 위5개 모두 제외 | 56 | 26/30 | 500 | 4 | 72 |

이 표는 재선별한 새 표본이 아니라 관측 경계를 제외했을 때 결론의 방향을 확인한 것이다. 모두 제외한56개를 사용자 요구의61개 대신 제출하는 것이 아니다. 가장 보수적인 제외에도 부분 질문의 선택/사용 보고4개와4축 밖 이유72답이 남는다. T048의 scope만 whole로 바꾸면29/32이며 최소20씩 조건은 유지된다.

재코딩15개에서 I2–I8은99/105(94.29%), 전체/부분은6/15(40.00%), 같은 실제 답의 형식은129/149(86.58%), 역할은75/149(50.34%)였다. 코드북에 scope 정의가 빠진 준비 결함을 고친 별도 추가 패스는14/15였지만 최초40%를 대체하지 않는다. 원질문자 응답 뒤 변화·엄격 근접오답은 양쪽 양성이0이어서 그 사건의 높은 음성 일치를 검증 성공으로 부르지 않았다.

15개 스레드의 최종 답176개를 블라인드 원응답192단위로 치환하면 전체는635−176+192=651단위가 된다. 이 민감도는 코드뿐 아니라 단위 분리 차이까지 포함한다. 원635와635개 동일 단위에서의 오차율처럼 비교하지 않는다. 불일치를 반영해 역할의 지배적 비중, 설명의 필수성,4축의 포괄성에 대한 강한 결론을 낮췄다. [RELIABILITY.md](RELIABILITY.md)에 모든 대응·불일치·보정 이유가 있다.

## 11. 다음에 시험할 적용 가설(H)

1. 요청의 원문·선택 범위·알려진 필수조건을 먼저 보존하고, 후보를 가르는 부족 정보만 묻는다. 질문마다 어떤 판정이 달라지는지 한 문장을 남긴다.
2. 짧은 되묻기와 현재 조건에서 가능한 잠정 답을 함께 제시한다. 응답 없이도 유지되는 설명과 응답에 따라 바뀌는 후보를 구별한다. 이것이 이탈을 줄인다는 결론은 아직 내리지 않는다.
3. 후보 카드에 근거의 시점과 조건 대응을 붙이고 L/E/H/T와 선택 이유를 별도 기록한다. 링크만·높은 점수·관리 상태 하나로 채택이나 탈락을 자동 결정하지 않는다.

다음 첫 검증은 실제 부분 요청을 받아 ‘질문만’과 ‘조건부 답+그 판단을 바꾸는 질문’의 대화 과정을 비교하는 것이다. 질문자 응답 여부, 후보/설명/질문 수정, 실제 선택과 이후 사용을 분리해 기록해야 한다. 이번 연구에서 그런 개입이나 사람 모집은 하지 않았다.

## 한계

- 검색 관련도·쿼터·공개 접근성과2답 이상·80답 이하 기준으로 선택했다. 삭제·폐쇄·0답·매우 긴 토론이 덜 보이며 개발자 신원도 추론하지 않았다. 비교 비율은 모집단·플랫폼 우열이 아니다.
- 현재 편집본이 중심이다. 일부 핵심 시점은 공개 revision/댓글로 보강했지만 모든 최초판과 편집을 복원하지 않았다. 보완 부분열람 사례는 존재 사례에만 쓰고 본표본 분모와 구분했다.
- 공식 채택은 SR30질문에 대해 최종 공개API로 보완했으나 현재값이며 과거 채택 이력은 아니다. 다른 플랫폼의 미노출 표식은null이다. 공개 반응 없는 실제 사용·실패·만족·이탈 원인은 여전히 알 수 없다. 자기 답·계획·일부방안 반박·선택 보고를 구별했다.
- 모든 현재 공개 댓글을 읽었다는 것과 모든 실질 행위를 동일 단위로 빠짐없이 코딩했다는 것은 다르다. 재코딩은26개 누락을 드러냈고 product/component 일치가 낮았다. 다른46개에도 같은 단위 경계가 남을 수 있어 역할 비율로 강한 제품 결정을 내리지 않는다.
- 문헌의 모집단·결과 변수는 서로 다르며 C05는 C04에 포함된다. 정책·메타 여러 페이지를 독립된 실험 여러 편으로 세지 않았다. 전문직 지침과 개념 논문도 효과 시험과 구분했다.
- D3는 도구·캐시를 통한 단회 URL 관측이다. 현재 기능·라이선스·성능·보안의 실행 검증이 아니며 실제 적용(D4)은 없다. API/DB/검색 스택 확정이나 배포 제안은 하지 않는다.
