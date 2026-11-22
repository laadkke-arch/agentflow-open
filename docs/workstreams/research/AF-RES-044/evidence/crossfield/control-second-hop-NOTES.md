# C1·C2 실제 두 번째 도착 원장

기준 풀은 묶음 2의 원격 `b36cc513ccbc1616168401ec9564866038e880a3`다. 원풀·요구·그룹을 변경하지 않았다. 이 보조 작업은 원 후보의 허용 창 안에 있는 실제 outgoing href를 수집하고, 두 번째 목적지의 접속·fragment·읽은 범위·구현별 원자 조건을 판독했다.

## 수집과 판독 단위

| 단위 | 수 |
| --- | ---: |
| 실제 outgoing href 노출 | 313 |
| 고유 목적지 URL(fragment/쿼리 유지) | 236 |
| 고유 문서 HTTP 요청 | 144 |
| HTTP 접속에 성공한 목적지 URL | 219 |
| 실제 HTML 도착 범위가 확인된 URL | 212 |
| HTML은 받았지만 target fragment가 없는 URL | 5 |
| HTTP 접근 실패 URL | 17 |
| HTTP 성공했으나 HTML 문서 판독 대상이 아닌 URL | 2 |

반복 href도 노출 단위에서 보존했다. 같은 문서의 여러 fragment는 네트워크 응답을 재사용하되 목적지 판독은 분리했다. `trials.json`은 시작 후보마다 초기 상태를 다시 만드는 **의미 상태표**이며, 실제 독립 네트워크 시행 횟수나 사람의 클릭 횟수가 아니다. 첫 원문에 성공적으로 도착했다는 전제도 명시했다. 최종 화면별 경로의 독립 opener·빈 CookieJar·href·fragment 검사는 부모 작업의 실행 원장과 결합해야 한다.

`coding.json`의 `per_case[].alternative_atom_support`는 각 **구현 ID별** A1/A2를 둔다. 서로 다른 라이브러리의 이름 근거와 기능 근거를 합치지 않는다. `semantic_complete_alternative_ids`와 `reachable_complete_alternative_ids`도 분리했다. 예를 들어 Requests의 웹 의미 판독은 raw HTTP403의 접속 성공으로 바꾸지 않았다.

## C2의 중요한 경로

`C-H2-TRIAL-0259`는 `C2-1`에서 실제 raw href `user_guide/visualization.html#visualization`(원 HTML DOM 44)을 여는 경로다. 대상 문서의 HTTP200과 실제 fragment를 확인했다. 도착 h1 창 안의 **Plotting directly with Matplotlib** 절은 Series/DataFrame을 Matplotlib 함수에 직접 전달하는 설명과 `plt.plot` 예제를 포함한다. 출발 카드의 10개 완전 ID와 이 목적지의 추가 Matplotlib 근거를 같은 시행에서 합치면 원풀 11개가 확보된다. 다른 시행의 판독을 가져오지 않는다.

두 별도 경로는 원풀의 미확인을 해소한다. `C-H2-TRIAL-0061/0062`는 qtpandas 저장소, `C-H2-TRIAL-0103/0104`는 ipyvega 저장소로 간다. 각 저장소는 Python 패키지/요구/설치 또는 Python 사용 예제를 명시한다. 첫 ecosystem 카드에 있던 해당 시각화 설명과 결합해 **각 시행에서 하나씩** 추가 확인한다. 원풀 분모 11을 13으로 고치지 않았으며, 이 두 시행을 합쳐 한 사용자에게 두 추가 대안이 모두 확인됐다고 말하지 않는다.

Altair 홈페이지의 이미지 gallery 링크도 h1 뒤 실제 허용 창 안의 href다. 여러 예제와 `Specifying Data`가 DataFrame 또는 표 필드를 Chart에 연결한다. 반면 Bokeh·Plotly·Seaborn의 일반 홈페이지, 설치·공동체·갤러리 목록은 실제 읽은 범위의 강도만 기록했다. 링크 제목이나 일반 시각화 소개만으로 표 입력 조건까지 자동 통과시키지 않았다.

## C1의 실패와 의미 판독

HTTPX `#client-instances` 및 `#merging-of-parameters`는 받은 현재 문서에 target이 없었다. GitHub 토론의 `#top`도 target이 없었다. 같은 문서의 다른 절이 읽힌다는 이유로 그 fragment 도착을 성공으로 바꾸지 않았다.

Requests 원 후보는 raw HTTP 실패였지만 부모 작업은 새 브라우저 탭에서 `#prepared-requests`를 확인했다. `evidence/browser-observations.json`의 2026-11-22 20:35 UTC 관측에서 얻은 **7개 raw href(고유 6개)**를 추가했다. 원래 raw 실패·빈 링크 관측은 `pre-browser-*`와 source receipt에 보존했다. 두 번째 Requests 문서의 별도 raw 시도는 403이었다. 웹 도구에서는 Prepared Requests 및 API 정의를 읽어 구성·prepare·Session.send의 의미를 판독했다. PreparedRequest/Session의 사용 예제와 달리 `Request.prepare`/`Session.prepare_request` 자체는 전송 호출이 아니며, Response 정의는 수신 객체 설명이다.

GitHub 댓글 fragment와 옛 Matplotlib HTML의 `div.section`은 공통 helper가 가장 가까운 main/body까지 넓히는 문제가 있었다. **출발 C1-1의 봉인된 첫 800단어와 outgoing 목록은 유지**했다. 목적지 의미 판독만 실제 target subtree로 제한했고, 그 tag·id·HTML 위치·해시를 `manual-scopes.json`에 남겼다. 다른 댓글의 코드를 가져와 해당 댓글의 근거로 세지 않았다.

## W 반증 시도

`W-audit.json`은 C1 첫 세 원문을 그대로 두고 판독 범위만 각 원문 전체 본문으로 넓힌 조사다. 요청을 보내는 HTTPX 예제와 Requests라는 이름/리다이렉트 비교를 구별하기 위해, 전체 본문의 Requests 언급 문맥과 Requests import·Request/Session/get/post/request/send 호출 여부를 함께 확인했다. **세 원문 어디에서도 Requests 패키지의 구성·전송 경로는 확인되지 않았다.** 같은 원문 전체 읽기만으로 별개 Requests 대안의 근거가 생긴다는 가설은 지지되지 않는다. 외부 Compatibility 링크나 Requests 원문을 추가로 열어 이 W 판정에 섞지 않았다.

C1-3의 Mounting transports 창은 outgoing routing을 명시하고 Client/transport 설정을 보여 준다. 그러나 그 창에서 독립적인 Request 구성 후 get/send 호출을 실행하는 예제는 보이지 않는다. 이름층의 일반 기능 진술을 허용하는 판정과 구체 호출 예제가 있다는 판정을 구별해야 한다. 어느 문서의 요청 코드도 이 연구가 실제로 실행한 것은 아니다.

## 파일과 재개

`targets.json`·`source-receipts.json`·`access.json`·`arrivals.json`은 실제 주소·순서·도착 메타데이터다. `coding.json`·`manual-judgments.json`·`trials.json`은 수동 의미 판독과 단일 시행 상태다. `sources.jsonl`의 이 추가 행들은 최소 독립 원문 수를 부풀리는 데 사용하지 않도록 모두 미산입으로 두었다. `W-audit.json`은 범위 민감도다. `summary.json`은 위 분모를 재계산한다. 모두 `control-second-hop-` 접두어를 갖는다.

원문 전체를 담은 `.tmp.json` 읽기 파일은 제출 전 제거했다. 다시 읽으려면 작업 브랜치에서 `python -B docs/workstreams/research/AF-RES-044/evidence/crossfield/control-second-hop-harness.py`를 실행한다. 그 후 `control-second-hop-code.py`는 URL 및 허용 창 해시가 일치하는 고정 수동 판정만 재사용하며, 내용이 바뀐 창은 미확인으로 돌린다. 새로 생성되는 임시 본문은 다시 읽은 뒤 공개 커밋에서 제거해야 한다.

| 남은 약점 | 영향 | 다음 최소 행동 |
| --- | --- | --- |
| Requests의 raw HTTP와 브라우저 접근성이 다름 | 모든 HTTP 실패 시행을 브라우저 성공으로 바꿀 수 없음 | 최종 독립 시행 원장에서 실제 사용한 접근 채널과 최초 도착 성공을 적용 |
| 큰 API/문서 창은 관련 정의·입력·호출 문맥을 읽음 | 모든 옵션·숨은 기능·신규 구현을 빠짐없이 판독했다는 주장은 불가 | 반례가 제시된 특정 함수/절의 입력 계약부터 추가 읽기 |
| 문서 기능은 확인했으나 실제 사용자 행동과 코드 실행은 미관측 | 채택률·실사용 성공·현행 판 조합의 실행 호환성을 추정할 수 없음 | 선택된 한 구현의 실제 요구 입력을 고정한 실행 또는 사용자 관측 |
