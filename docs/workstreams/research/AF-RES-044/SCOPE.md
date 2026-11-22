# AF-RES-044 사전 범위·표집·표시·판독 규칙 v1

## 0. 고정 입력과 노출

시작 통합 SHA `333e83c9a46b0c005d22efcccbb5a055b27e904e`; 계획 SHA `785880f7b7c380dd49e0e4e6e6d90715a9b27838`; 의존 AF-RES-040 `9bff55706d5b1a939e39185bda9cf6f22bea246b`. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF, START_HERE, CLOUD_WORKFLOW와 040 HANDOFF/RESULT/pool/losses/method-clarifications를 직접 읽었다. 기존 GDAL/Sphinx 8요구, 도서관/음악, 수동 #L 후보를 다시 판정하지 않는다. 040의 완전경로 분모0·G2/S1 부분손실·G4 무손실은 출발점이다.

규칙 커밋 전 접근성 점검에서 현행 Pandoc MANUAL의 서두~Creating a PDF, Vega-Lite docs 목차~Error Bar가 웹 도구 출력으로 보였다. 이를 숨기지 않는다. 어떤 소비자 사례도 아직 선정하지 않았고 후보 풀/해법을 계산하지 않았다. shell Pandoc MANUAL 403, Vega docs HTTP200. 초기 노출은 파일 evidence/pilot-exposure.json에 보존한다. 이 파일의 커밋 전 완전 무노출을 주장하지 않는다. 이하 실제 원요구·후보 순서는 규칙 커밋 이후 봉인한다. 원문 전체를 저장하지 않고 해시·href와 자체 요약을 보존한다.

## 1. 자연 원요구 표집 (Q1)

두 공개 원장 P=`jgm/pandoc` GitHub issues, V=`vega/vega-lite` GitHub issues. 기간 UTC 2020-01-01..2025-12-31. 각 고정 질의 `repo:REPO is:issue created:2020-01-01..2025-12-31 support in:body`; GitHub search sort=created, order=asc, per_page=40. 검색순서를 만든 뒤 생성시각·번호 오름차순 동률 정렬. 최초 40노출 모두 frame에 남긴다. 검색 API metadata와 최초 본문만 읽고 댓글은 선정·요구 봉인 뒤 읽는다. 검색결과에 댓글/결말 문구가 노출되면 outcome_exposure에 적는다. 제목만 본 노출을 직접 읽은 소비자 원문 최소수에 넣지 않는다.

원장별 N(이름/기능 지원 확인) 최초 적격2, K(계약) 최초 적격2; 합계8. N은 어떤 도구/이름이 해당 일반 기능을 지원하는가로 응답 가능한 요청이며 정해진 실행판·구체 입력/출력 보존·호출 방식·버그 해결을 필수로 요구하지 않는다. K는 판·정확한 입출력/표현·호출·조건부 오류 해결 중 하나 이상을 필수로 한다. 기능 추가 희망도 실제 소비자 행동이 명시된 경우 포함하되, 구현 내부 리팩터·유지보수자 할일·동일 요청 재서술·스레드 중복은 제외. 복합/애매한 사례는 K 또는 미확인, N으로 억지 축소하지 않는다. 정원 후에도 최초40의 제목/번호/탈락 이유(정원후 미판독)를 남긴다.

예비 원장 R=`matplotlib/matplotlib`, 같은 기간·질의·순서·최초40. 주 원장 한 곳이 정원을 채우지 못한 경우에만 사용; 결핍한 층에 필요한 최초 적격을 택하고 원래 빈자리·대체 이유 보존. 예비로도 부족하면 빈 요구 슬롯과 수용 미충족. 관측 후 검색어를 바꾸거나 성공 사례로 교체하지 않는다.

## 2. 후보 원풀 6자리 (Q2)

각 원요구를 봉인하고 최초 문장·요구 원자·필요 행동·N/K·명시 판을 기록한 뒤, 본문 판단 이전 case-specific discovery plan을 evidence/<route>/discovery-plan.json에 쓴다. 이 계획에는 원요구 명사에서 가져온 검색 토큰(최대3), 시작 공식 HTML 목차, 메뉴 범위, 대상 기능 범주, 판, 첫6 슬롯 규칙이 있다. 계획 수정 전/후를 따로 보존한다.

P 시작 `https://pandoc.org/MANUAL.html`, 공식 게시 소스 `jgm/pandoc` gh-pages의 실제 HTML을 접근 대체로 허용. V 시작 `https://vega.github.io/vega-lite/docs/`, 게시 소스 `vega/vega-lite` gh-pages 또는 공식 웹 HTTP. 명시한 과거판이 있으면 공식 당시 버전 HTML URL을 **그대로 실제 발견한 경우만** 사용; 현재 링크를 과거 URL로 고쳐 쓰지 않는다. 과거 HTML을 확보 못 하면 현행 snapshot은 별도 진단이며 원판 적격은 미확인. 버전 미지정 요구는 읽은 현행 게시판/hash 기준 지원 여부만 판정하고 과거 해법으로 소급하지 않는다.

목차에서 원요구 토큰이 가장 구체적으로 일치하는 제목의 범주를 택한다(긴 정확 문자열 우선, 동률 DOM 최초). 전체 부모 기능 범주 내 실제 a[href]의 DOM 순서를 사용하고 제목 자체에 링크가 있으면 그것부터 포함한다. 텍스트의 임의 단어를 새 fragment로 만들지 않는다. 동일 문서 fragment·반복 href도 그대로 한 슬롯. 관련 범주가 목차에 없으면 본문에서 같은 제목 범주(상위 h2/h3까지) 내 href; 그래도 없으면 전체 본문 첫6 href. 최대 시작 목차1 + 최초 범주 페이지1, 두 페이지. 외부 링크도 본문 범주에 실제 있으면 유지한다. 사이트 전역 nav/로그인/공유/광고/footer는 제외; 기능 목차/본문 메뉴는 포함. 첫6 다음은 읽지 않고 부족하면 빈칸. 원 href, resolve URL, DOM 전체순번, 범주순번, 노출 HTML URL·판·SHA256·수집시각을 모두 남긴다. 검색 순위가 아니라 이 고정 목차 범주 순회에서 나온 풀이다.

원 HTML은 작업 중 보관하되 공개 결과에는 짧은 href 추출·해시·재취득 명령·자체 요약을 남긴다. 초기 파일·본문 확인만으로 full text 읽음으로 세지 않는다. 모든 비빈 후보를 열어 실제 목적지·fragment 존재·관련 범위·접속 실패를 기록한다.

## 3. 양성 대조4 (Q3)

별도 C1..C4. C1/C2 목표: 공식 비교/이관/유지보수자 결정 페이지의 자연 순서에 같은 용도 여러 URL 다음 별개 구현의 완전 대안. C3/C4 목표: 한 상류의 보완 문서 또는 다른 판이 필요한 요구. 탐색 출발 계열은 Python 포장/호환성(Pillow↔PIL, psycopg2↔3), 시각화(Vega/Vega-Lite/Altair), 문서(Pandoc PDF engines/filters), HTTP(Requests/HTTPX) 순으로 탐색하되 사후 발견 표본이라는 사실을 유지한다. 원 결정·요구·6 URL·DOM 순서·완전 경로/근접 오답을 그룹 계산 전 별도 봉인한다. 원래 HTML에 연속하는 기능 범주의 첫6 href를 쓰며 반복을 삭제하지 않는다. 부족한 URL·양성 근거가 있으면 빈슬롯 또는 실패 대조이며, 구성 순서를 인위적으로 만들면 별도 진단 D로만 저장한다. 대조 해법을 발견 성능으로 집계하지 않는다.

## 4. 메타데이터와 그룹 (Q4)

A key=resolve한 실제 URL 완전 일치(쿼리/fragment 보존). B key=공식 publisher/repository identity로 확인된 상류 프로젝트. C key=(상류 구현, 명명 부품, 요구와 독립인 기능/용도, 공개 판, 문서 근거 역할). 제목·TOC 라벨·URL·발행 metadata에서 알 수 있는 값만 쓴다. 역할=overview/capability/reference/configuration/example/migration/test/release 중 표시시점에 명시한 것. 다기능 문서의 역할은 정렬 집합. gold의 완전/부분 여부·미래 댓글·숨은 해법·원자 적격값을 key로 사용하지 않는다. 필드 하나라도 미확인이면 singleton. 같은 상류가 같은 기능 또는 호환이라는 의미는 아니다. 각 key의 근거 위치와 미확인 이유를 원장에 남긴다.

각 방식은 첫 등장 그룹을 원순서로 정렬하고 첫3 그룹의 최초 멤버를 대표로 쓴다. 부족하면 빈자리. 원멤버 전체를 유지한다. 카드 라벨은 비빈 전부 정확히 `원문 보기`(5 Unicode code points, 공백 포함), 설명은 빈 문자열 0자. 형제 목록 버튼은 동일 `관련 링크`(5자). 연구 ID는 분석 metadata이며 사용자 카드 설명에 넣지 않는다. 대표 선택에 gold를 사용하지 않는다.

## 5. 판독과 실제 2동작 (Q5)

첫 표 direct는 첫3 대표의 각 문서 근거를 모은 **제공 범위 inventory**이며 한 사용자가 3개 문서를 읽은 두 클릭 시행과 구별한다. 기본 판독 창: fragment가 있으면 실제 해당 element로 도착한 뒤 그 절(다음 동급 이상 heading 전까지); fragment가 없으면 main/article/body에서 첫 h1 뒤 첫800 단어. 무제한 전체문서 보기는 기본에 포함하지 않는다. 전체문서 접근 허용만 단독으로 완화한 민감도를 별도 계산한다.

각 시행은 카드를 초기 상태로 새로 시작. 허용 전이는 (i) 대표 열기 1회 후 다른 표시 대표 열기 1회, (ii) 형제 목록 열기 1회 후 그 멤버 원문 열기 1회, (iii) 대표 원문 1회 후 그 도착절에 실제 있는 href 열기1회. 뒤로/연구자 기억/다른 시행 내용 합산 금지. 형제 목록만 열기는 원문 근거0. 같은 화면 대표 두개는 각각1회. 첫 클릭 원문 후 형제목록을 열면 2회 예산 소진, 멤버는 못 읽음. 가능한 유효 경로를 열거하고 실제 네트워크 목적지/도착절을 확인한다. HTTP/DOM navigation harness는 연구자의 통제 도달 관측이며 실제 사람의 사용/채택은 미확인. 실패·누락 fragment를 성공 클릭으로 바꾸지 않는다. 경로마다 접속성공, 보고서 의미판독, 실제 사용자반응을 별도 필드로 둔다.

## 6. 적격·손실·수치 (Q6)

모든 요구는 필수조건 atom으로 분해. 후보별 같은 요구·판·방향 평가=예/아니오/조건부/미확인. 문서 진술(D1), 구현 관측(D2), 실행(D3)을 구별한다. 완전 대안은 하나의 실제 구현/허용 조합이 모든 필수 atom을 입증하는 최소 문서 경로다. 같은 구현의 여러 URL/예제를 독립 대안 수로 늘리지 않는다. 여러 구현의 부분 atom을 섞어 가상 완전 대안을 만들지 않는다. 이름층도 기능지원 진술이 있어야 적격. 과거 버그를 현행 일반문서만으로 해결 처리하지 않는다.

48 natural+24 control slots, unique exact URLs, independent documents(같은 저작/fragment/미러 중복제외), eligible alternative IDs를 각각 센다. 원풀 완전 대안은 풀 URL들의 허용 범위의 조합으로 입증되며 클릭 제한 이전 분모다. 대표 direct와 한 시행 2회로 확인한 경로의 complete IDs를 따로 센다. 자연 N/K, 보강 C를 따로 집계. 원풀 absent, ranking truncate, grouping hidden, duplicate original document slots 구별. 0 eligible denominator ratio는 `해당 없음`, unknown은 `미확인`. same upstream different call, repeated function URLs, one document multiple roles, one-way substitution을 반례로 실제 확인한다.

## 7. 분야 간·민감도·검토 (Q7)

박물관2+·운수기관2+ 독립 원문. 이름 소비자/구성품·정차 검증 소비자/관리자별 필요를 분리. U는 C의 알려진 필드가 같은 unknown끼리만 병합; 다른 key나 gold는 불변. W는 같은 열린 원문 전체 확인된 절을 허용; key/대표/클릭 비용은 불변. 한 번에 한 요소만 바꾸고 변경된 요구ID·원 수치를 같이 기록. 변경이0이면 효과 없음이라는 관측이지 안전성 보증 아님.

같은 연구 모델의 재판독은 자체 점검. 별도 보조 에이전트의 근거 검토는 내부 병렬 검토이며 사람/블라인드 독립판독이 아니다. 원문 최소28과 범주별 최소, 필수 표12/36행, 72슬롯 원순서, 동일입력/라벨, completeID 이득/손실 양방향, 약점3행, 네 묶음커밋을 검사한다. 예측: B가 이름층에서 충분할 수 있고 계약층에서는 보완근거를 가릴 수 있음; C도 역할을 과하게 나누면 별개 대안을 가릴 수 있음; W가 B 손실을 지울 수 있음; 원풀 부재는 어떤 병합으로도 해소 안 됨. 예측의 반례를 먼저 찾는다.

## 8. 커밋·완료

① 이 규칙·manifest, ② 요구·frame·원href·보강·gold기준 봉인, ③ 후보판독·36보기·경로, ④ 짝집계·반례·자체점검·수용. 각 remote SHA를 다음 커밋의 COMMIT_LOG.md에 기록. RESULT/acceptance를 고정 원격 SHA로 다시 열고 `python -B -m workbench.session check docs/workstreams/research/AF-RES-044/manifest.json --fetch` 실제 결과 기록 뒤 HANDOFF 단독 마지막 커밋. 미달은 구체 condition=false와 최소 재개자료로 표시한다. dot-control 및 owned_path 밖 내용은 변경하지 않는다.
