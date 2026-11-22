# SELF_CHECK 초안 — AF-RES-044

최종 보완 기준: **2026-11-22 21:20:17 UTC**의 로컬 작업 파일. 이 초안은 루트의 정식 `SELF_CHECK.md`·수용 원장 통합을 위한 내부 검토다. **연구 전체 완료 조건은 미충족**이며, 결과·수용 원장의 고정 원격 SHA 재열람과 session check를 완료했다고 주장하지 않는다. 본문·키·풀·결과 파일은 수정하지 않았다.

같은 연구 모델의 재독과 내부 보조 에이전트 교차 검토이며 **사람의 독립 평가·맹검·실제 사용자 실험이 아니다**. **관측**(원응답·DOM·도착), **저자 진술**(공식 문서·유지보수자의 설명), **연구자 해석**(원자 적격·동일성·대체 방향)을 구분한다. 문서상 지원을 프로그램 실행 성공이나 사용자 채택으로 승격하지 않는다.

## 최신 관측과 분모

선언된 자연 요구8건·보강4건,72슬롯과36보기는 그대로다. **Pandoc P1–P4의 원풀4개는 미확인**이며, 빈 후보 풀로 처리하지 않는다. **V1–V4의 봉인된 관측 풀에서 확인된 완전 대안은0**이다. V3의 원규칙 fallback 풀은 별도로 미확인이다. 같은 A/C 표시와 U 무변화는 **관측한8풀**에 한해 확인했으며, P4개의 U 효과는 미확인이다.

주 실험은 **1,924개 계획·1,924개 관측**으로 완료되었고 두 ID 집합의 일치와 각 ID의 유일성을 읽기 전용으로 재확인했다. 이는 접속 성공1,924건 또는 사람 클릭1,924건이라는 뜻이 아니다. 별도 Requests 브라우저 시행1건과 C2 외부 목적지 재검증2건은 독립 모집단으로 보존한다. 현재 `clicks.csv`의1,927개 고유 시행은 이 세 모집단을 합친 기록 수이며, 방법마다 복제한 시행 수가 아니다.

아래 수치는 모두 원풀 적격 ID를 분모로 한다. `직접`은 첫 세 대표가 제공하는 문서 근거 inventory다. `두 클릭 도달`은 **각 ID가 한 시행 안에서 완결된 경우만** 모은 도달 가능 ID 합집합이며, `한 시행 최대`와 구분한다. A/B/C 순으로 쓴다.

| 보강 요구 | 원풀 적격 ID 수 | 직접 A/B/C | 두 클릭 도달 A/B/C | 한 시행 최대 A/B/C | 해석 한계 |
| --- | --- | --- | --- | --- | --- |
| C1 | 2 | 1/2/1 | 1/2/1 | 1/1/1 | B의 Requests는 별도 브라우저 시행으로 확인. 도달 ID 합집합2를 한 시행2로 해석하지 않는다. |
| C2 | 11 | 11/10/11 | 11/11/11 | 11/11/11 | B의 직접 Matplotlib 근거는 대표 밖이지만 실제 outgoing href 두 클릭으로 원풀11을 한 시행에서 확인. 외부2대안은 아래 별도 기록. |
| C3 | 1 | 0/0/0 | 1/0/1 | 1/0/1 | B의 기본 두 클릭 완전0. W에서 B도1로 바뀜. |
| C4 | 0 | 0/0/0 | 0/0/0 | 0/0/0 | 확인된 완전 입증0이며 남은 조건은 미확인. 양성 미충족. |

C2의 `C2-ipyvega`·`C2-qtpandas`는 새 목적지에서 빠진 Python 조건을 채운 **원풀 밖 추가 근거**다. 원풀 분모11은 바뀌지 않았다. 각 별도 시행은 외부 대안1개와 원풀 대안10개를 확인하며, 두 시행의 외부 대안2개를 한 사용자의 두 클릭 결과로 합치지 않는다. A/B/C에 같은 첫 카드·경로가 있어 공유 witness로 적용했지만 실제 시행은2건이며6건이 아니다(`clicks.csv`1927–1928행; `changes.csv`158–159행).

## Q1~Q7 주장·반증·잔여 불확실성

경로는 모두 `docs/workstreams/research/AF-RES-044/` 기준이다. 아래 행 번호는 이 초안의 버전 표에 적힌 파일의 물리적 행 번호이며, JSON/CSV의 case·candidate·trial ID를 함께 사용한다. 원문 web 행은 직접 연 문서의 텍스트 렌더 위치로서 raw HTML 행과 다르다.

| 질문 | 주장·현재 판단 | 현재 파일·행 | 실제 원문 URL·정확한 위치 | 반증 시도·결과 | 미확인 | 결론을 뒤집을 조건 | 다음 최소 조사·첫 자료 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Q1. 이름 요청과 계약 요청을 미리 구별했는가?** | **연구자 판정:** 최초 작성자 본문에 명시된 필요 행동으로 N/K를 구분했다. 일반 도구·기능 이름 확인도 실제 지원 근거가 있어야 완전이다. 판·구체 입력 보존·호출·오류 해결을 요구하면 K다. 이 표본의 경계 판정은 사전 코드북에 따른 것이며 보편적 자동 분류기를 검증한 결과가 아니다. | `SCOPE.md`11–15·19행; `requirements.csv`2–16행; `evidence/pandoc/requirements-P.json`38–98행(P2/P3); `evidence/vega/requirements-V.json`77–104행(V3); `evidence/vega/input-audit.md`40–50행; `evidence/pandoc/sources-P.jsonl`2–3행과 `evidence/vega/sources-V.jsonl`3행. | [Pandoc #6126 API](https://api.github.com/repos/jgm/pandoc/issues/6126) `title`·`body` 전체: 추가 XML/HTML+CSS→PDF 엔진 일반 지원 요청. [#6095 API](https://api.github.com/repos/jgm/pandoc/issues/6095) `body` 첫 의미 문장 및 tagpdf `alttext`/accessibility `alt` 두 입력 예: 대체 내용 보존 계약. [Vega-Lite #6135 API](https://api.github.com/repos/vega/vega-lite/issues/6135) `title`·`body` 전체: word cloud 일반 지원 요청. | 단순 기능 추가 희망은 전부 이름층이라는 가정을 P2의 구체 입력 보존 요구로 반박했다. 반대로 PDF 엔진 요청의 변환 방향이 있다는 사실만으로 구체 호출 계약이라고 승격하지 않았다. V3/V4는 다른 최초 요청이지만 같은 상위 #1872 결정을 공유하므로 통계적으로 독립인 소비자 반응으로 일반화하지 않았다. | 현재 API 최초 작성자 본문이 최초 게시 당시 수정 전 revision과 동일한지는 미확인이다. P4 DITA의 N/K 경계와 사전 pilot·우연 노출은 해석·노출 원장에 남는다. 사람 간 분류 일치도는 미확인이다. | 역사적 원요구가 추가 호출·판 제약을 포함했거나 별도 독립 판독에서 경계 사례가 K로 바뀌면 층별 분석이 달라진다. 이름층 기능지원 자체가 확인되지 않으면 이름만으로 적격 처리할 수 없다. | 각 issue의 최초 작성자 revision 이력과 `frame.csv`의 노출·선정 이유를 대조한다. 첫 자료는 P4 [#6166](https://github.com/jgm/pandoc/issues/6166) 원문과 `requirement-interpretation-note.json`; 기존 층과 원자는 사후 교체하지 않는다. |
| **Q2. 후보 수집의 부족과 관측 실패를 구별했는가?** | **관측:**72자리 선언 순서와 동일 입력은 재구성되지만 P24슬롯은 raw HTML 미관측이다. 후기 DOM 획득을 원 발행 바이트·원순서 성공으로 바꾸지 않았다. V3의 `text` 연상 토큰은 원규칙 이탈이므로 현재 수치는 봉인 풀에만 유효하다. | `pool.csv`2–25행(P 결측),26–49행(V); `SCOPE.md`19–23행; `evidence/browser-observations.json`6–16·42–43행; `evidence/vega/discovery-plan.json`41–45행 및 `discovery-selections.json`26–28행; `evidence/vega/input-audit.md`40–44행; `evidence/pandoc/sources-P.jsonl`5–8행. | [Pandoc MANUAL](https://pandoc.org/MANUAL.html)의 원 HTTP 취득 실패 원장 및 후기 `documentElement.outerHTML` 진단. [V3 원요구 API](https://api.github.com/repos/vega/vega-lite/issues/6135)의 전체 `title`·`body`에는 `text`가 없다. [Vega-Lite 목차](https://vega.github.io/vega-lite/docs/) Table of Contents의 Text 범주와 [View Configuration](https://vega.github.io/vega-lite/docs/spec.html#config) 실제 h2 창을 구별한다. | 후기 성공 DOM으로 결측을 메우거나 토큰을 답에 맞춰 보정하면 되는지 검사했다. 렌더 DOM 해시가 원응답 바이트 해시와 같지 않으므로 P를 교체하지 않았다. V1의 일반 `config` 선택은 subtitle 해결 근거를 보장하지 않는다. V3의 `text`가 실제 최초 요청에 없음을 새 API 재열람에서도 확인했다. | P1–P4의 실제 원풀 및 완전 대안 수는 미확인이다. V3에서 원규칙의 무일치 fallback을 사용했을 풀도 미확인이다. V1의 과거 v4 요구와 현행 문서판 정렬은 미확인이다. | 공식 발행 원응답과 원순서를 새로 봉인했을 때 완전 경로가 생기거나, V3의 원규칙 fallback이 다른 근거를 제공하면 수집 단계와 이름/계약층의 판단이 달라진다. | 첫 자료는 위 MANUAL의 승인된 실제 원응답 바이트와 SHA·href 목록이다. V3는 원문 명사·fallback을 먼저 고정하는 별도 amendment로 재개한다. 기존 결측·성공 슬롯과 원규칙 수치는 보존한다. |
| **Q3. 양성 대조와 근접 오답이 실제로 성립하는가?** | **저자 진술+연구자 판정:** 원풀 적격은 C1=2,C2=11,C3=1,C4=확인0+미확인이다. C1 복원과 C3 보완 손실은 관측했다. C2는 첫 대표가 여러 대안을 이미 입증해 두 번째 복원 양성으로 부족하고, C4는 봉인 A2 전체를 원풀에서 입증하지 못해 양성 미충족이다. | `requirements.csv`17–24행; `gold-paths.csv`56–59·66–79·86–87행; `evidence/candidate-evidence.jsonl`49–72행; `evidence/control/freeze-C4.json`8–13행; `evidence/vega/computation-audit.md`§4–6. 현재 분모는 `evidence/pool-gold-summary.json`의 C1–C4 객체. | [Requests Prepared Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests) web72–132의 Request 구성·Session.send. [pandas ecosystem](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization) web40–113의 h2 전체. [직접 Matplotlib](https://pandas.pydata.org/pandas-docs/version/2.0/user_guide/visualization.html#visualization) 같은 h1 안 web972–994. [Python Data model](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers) web1401–1425와 [async-with expansion](https://docs.python.org/3.11/reference/compound_stmts.html#async-with) web816–847. | “뒤 별개 URL이 표시되면 새 완전 대안이 살아난다”는 가정을 C2 첫 h2가 이미 제공하는 Altair/Bokeh 등의 지원으로 반박했다. Data model의 awaitable 반환 의무를 caller의 두 await·예외 전달 전체로 읽는 근접 오답을 expansion의 실제 await 구문과 대조해 배제했다. C1-3 Mounting transports의 routing 근거만으로 construct-and-send 전체를 입증하지 않는다. | C4는 확인된 원풀 완전 입증0이고 남은 계약은 미확인이다. 현재 환경에서 라이브러리 예제가 실제 실행되는지는 검사하지 않았다. 보강은 해법 노출 후 선택한 메커니즘 대조이며 자연 발견 성공률이 아니다. | 봉인된 조건을 완화하지 않은 C4 완전 경로가 실제 허용 범위에 있거나, 앞 대표가 입증하지 못하는 별개 완전 대안이 복원되는 두 번째 대조를 확보하면 양성 충족 범위가 달라진다. | 새 독립 유지보수/이관 사례에서 요구·자연6순서·근접 오답을 그룹 계산 전에 봉인한다. 첫 비교 자료는 위 Data model/async-with와 pandas Visualization이다. C4를 사후 완화하거나 C2 외부 대안을 원풀로 옮기지 않는다. |
| **Q4. 같은 대상을 가리킨다는 판정은 어느 범위인가?** | **관측+계산:** A/B/C는 같은 후보 순서에 주소·상류·표시 metadata 키를 적용했다. gold를 키로 사용하지 않는다. 관측8풀에서 C=A이며 C의 실제 의미 병합 효과를 식별하지 못했다. 상류·문서판·대상 구현판·호출·대체 방향을 서로 바꾸어 쓰지 않는다. | `SCOPE.md`33–35행; `groups.jsonl`13–36행과 `views.jsonl`13–36행; `evidence/build_study.py`의 그룹 키 및 카드 생성; `evidence/metadata-audit-corrections.json`2–7행; `evidence/arithmetic-corrections.json`의 version_alignment 정정; `evidence/calculate_results.py`17–18·34–36·46–62행. | [pandas의 Altair 소개](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#altair) web43–45는 발행 문서판과 대상 구현이 다름을 보여준다. [Vega-Lite Overview](https://vega.github.io/vega-lite/docs/) web11–12는 Vega-Lite→Vega 컴파일 방향이다. [Aggregate](https://vega.github.io/vega-lite/docs/aggregate.html#encoding)의 encoding/transform 절은 같은 목적의 다른 JSON 호출 위치다. [Python constructors](https://docs.python.org/3.11/library/exceptions.html#ExceptionGroup)의 두 dt가 공유하는 exception-groups 절. | 같은 exceptions 원문이 component 키에 따라 다른 카드가 되는 예, 같은 aggregate 기능이 다른 호출 계약인 예, Vega transform 지원을 Vega-Lite 지원으로 역전할 수 없는 예를 확인했다. 감사에서 과도하게 특정한 C1-1 role/C1-2 component/C4-6 role을 미확인으로 정정했고 이미 unique였으므로 대표 결과는 그대로다. /3 현재판 및 제안 단계 메일을 final3.11 계약에 합치는 오류도 버전 gate로 제외했다. | Python3.11 branch 수준과 Vega exact semver 미확인 사이의 판 정밀도 차이, 일반 자료에서 C 키를 추출하는 재현성은 미확인이다. C=A라는 결과는 C가 안전하거나 우월하다는 증명이 아니다. | 표시 metadata만으로 같은 C 키가 실제 반복되는 독립 풀이 생기면 C가 완전 경로를 살리거나 가리는지 식별할 수 있다. 공급자가 다른 판·역방향 변환·다른 호출의 계약 동등성을 명시적으로 입증하면 방향/판 판정이 달라진다. | 첫 자료는 원 `display-metadata-freeze.json`과 위 metadata 정정 이력이다. 새로운 C 병합 표본은 코드북·판 정밀도를 먼저 고정한다. 현재 gold에 맞춰 기존 키를 재설계하지 않는다. |
| **Q5. 같은 세 자리와 실제 두 클릭에서 무엇까지 도달했는가?** | **관측:**1,924개 주 계획과 실제 관측이 일치한다. 카드 라벨은 `원문 보기`5자, 설명0자다. C1 B의 도달 합집합은2지만 한 시행 최대는1. C2는 실제 한 시행에서 원풀11을 확인. C3 A/C는 PEP→Specification으로1, B는 기본0이다. 통제 HTTP/DOM 도달과 의미 판독을 실제 사용자 행동과 분리했다. | `evidence/trial-plan.jsonl`·`trial-observations.jsonl`1–1924행; `clicks.csv`710·730·1118·1449·1604·1926행; `evidence/trial-observations.jsonl`709·729·1117·1448행; `evidence/browser-observations.json`45–63행; `views.jsonl`1–36행. `results-data.json`의 case/method와 witnesses를 교차 확인했다. | [HTTPX Timeouts](https://www.python-httpx.org/quickstart/#timeouts) web445–458, [Requests Prepared Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests) web72–132. [PEP654](https://peps.python.org/pep-0654/) 첫800의 실제 TOC `#specification`→[Specification](https://peps.python.org/pep-0654/#specification)의 constructor 경계·except*·Unmatched Exceptions(web87–91,342–345,394–415). C2는 ecosystem의 실제 `user_guide/visualization.html#visualization` href→Chart visualization. | 세 대표의 제공 범위를 한 사용자의 두 클릭 기록으로 합치는 오답을 C1의2대안 합집합/한 시행1로 반박했다. 형제 목록만 열면 원문 근거0이다. C3의 같은 PEP가 두 역할을 입증하는 반례를 실제 두 단계 도착으로 확인했다. 각주·TOC backlink·댓글을 전체 chapter로 확장한 추출 오류는 구조 block으로 정정했다. Requests HTTP 실패를 별도 브라우저 성공으로 소급 덮어쓰지 않았다. | 사람의 클릭·이해·확신·채택, 프로그램 실행 결과는 미확인이다. 원답변 바이트가 다른 dynamic GitHub 응답은 이전 의미 판독을 자동 승계하지 않으며, 별도 재검증한 응답만 해당 시행의 근거다. | 동일 href라도 출발 바이트·resolve URL·도착 fragment가 달라지면 경로 승인은 달라진다. 실제 독자가 긴 절이나 형제 목록을 다르게 이용하면 문서상 두 클릭 도달과 행동 결과가 달라진다. | 첫 자료는 해당 trial의 `actions`·`arrivals`·`locators`·같은 시행 complete IDs다. 이미 관측한 ID를 늘려 세지 말고 현재 views fixture로 사람의 과업별 탐색을 별도 실험한다. |
| **Q6. 병합 손실과 원풀 부재를 구별했는가?** | **계산 해석:** P4풀 미확인과 V4풀의 확인된 완전0을 구분했다. C1 B는 원풀 Requests를 직접 대표와 도달 합집합에 복원한다. C2 B의 직접 완전11→10은 Matplotlib 근거가 가려진 차이지만 두 클릭에서 원풀11이 회수된다. C3은 원풀1이 A/C 두 클릭1→B0으로 줄어 실제 병합 손실이 남는다. C4의 확인0을 무손실 양성으로 세지 않는다. | `changes.csv`98–99행(C1),110–111행(C2),122–123행(C3),134–135행(C4); `gold-paths.csv`의 최소 경로; `evidence/candidate-evidence.jsonl`31–34·51–57·61–72행. 원풀 밖은 `changes.csv`158–159행 및 `clicks.csv`1927–1928행에 별도 표시. | [Projection](https://vega.github.io/vega-lite/docs/projection.html)의 첫800과 [Types](https://vega.github.io/vega-lite/docs/projection.html#projection-types) web37–56(특히52)은 identity/reflectY 하위사실을 반복 제공한다. 완전 graticule-label 요구와는 다르다. 보강 근거는 Q3/Q5의 Requests·pandas·PEP 정확 절. 추가 근거는 [qtpandas](https://github.com/draperjames/qtpandas) README 첫 h1 뒤171어절과 [ipyvega](https://github.com/vega/ipyvega) 같은 규칙448어절의 Python 설치·사용 문구. | “숨은 URL=완전 근거 손실”을 V2의 기존 대표 하위사실 반복과 C2의 실제 회수로 반박했다. 반대로 C3은 풀에 완전 경로가 있는데 B의 클릭 비용 때문에 도달하지 못해 수집 부재와 다르다. C2의 외부2대안은 원풀에서 빠졌던 Python 조건을 새로 채운 경우로 확인했고, 원풀 대안을 되살린 이득으로 세지 않았다. | 자연 표본에서 실제 완전 대안의 복원/손실이 발생하는 빈도는 미확인이다. P의 분모 자체와 V3 원규칙 풀, 엄격한 실행판·구체 입출력 계약을 요구했을 때 C2 외부 지원은 미확인이다. | 새 자연 풀에서 완전 대안이 존재하고 그룹·순위·허용 경로에 따라 숨거나 돌아오면 그 요구의 병합 효과를 계산할 수 있다. 후보의 판·방향·필수 원자나 실제 도착 판정이 바뀌면 분모/분자가 달라진다. | 첫 자료는 해당 요구의 원6슬롯과 최소 완전 경로, 이어 witness의 두 도착 창이다. IPyvega의 A2는 공식 ecosystem 문맥 해석임을 유지하고 호출 계약으로 확대하지 않는다. 확인된 분모0 비율은 **해당 없음**, P처럼 분모 결측은 **미확인**으로 유지한다. |
| **Q7. 다른 분야와 한 요소 민감도는 어떤 반례를 보이는가?** | **관측+해석:** 작품명/노선명 대표는 특정 소장품 필드·정차 방향의 대표와 요구 범위가 다르다. 같은 문서가 여러 필요를 함께 담을 수도 있다. 소프트웨어 W에서 C3 B는0→1로 뒤집히지만 C4 양성은 해결되지 않는다. U는 관측8풀에서 대표·멤버·화면 밖 그룹을 바꾸지 않았고 P4풀은 미확인이다. | `evidence/crossfield/sources.jsonl`1–8행; `evidence/crossfield/NOTES.md`20–48행; `changes.csv`130–131행(C3 W),142–143행(C4 W),146–157행(U); `clicks.csv`1561·1567행의 C3 B strict/W; `evidence/views-U.jsonl` 및 `views.jsonl`의 같은 case 전체 카드·offscreen_groups. | [Met36491](https://www.metmuseum.org/art/collection/search/36491) Object Information web61–72(JP10), [Met56353](https://www.metmuseum.org/art/collection/search/56353) web62–73(JP2972), [Met API](https://metmuseum.github.io/) Object response web176–207. [A 시간표](https://www.mta.info/schedules/subway/a-train) p1 안내·p2 Manhattan·p8 Queens의 Inwood/Lefferts 행; [A line map](https://www.mta.info/maps/subway-line-maps/a-line) web14–20·51–69. W는 [PEP654](https://peps.python.org/pep-0654/) 같은 원문 안 Specification·except*·Unmatched Exceptions. | 같은 Great Wave 제목의 서로 다른 번호·치수·취득 기록을 확인하여 JP2972의 필드를 JP10에서 전용하는 오답을 배제했다. A 시간표에 역이 없으면 무정차라는 추론은 timepoint 한정과 공식 역 목록으로 반박했다. CF-T-SCOPE는 같은 PDF p2만 읽을 때 미확인, p8 허용 시 예로 바뀌는 사후 보조 진단이다. C3의 W에서는 키·카드·전이·비용을 고정하고 같은 PEP의 추가 절만 허용해 B 손실이 사라졌다. | 실제 판화 인상·상태 감정, 관리자 merge/split 재구성 시험, 일부 지도 개정일, 해당 날짜 실시간 운행, 실제 사람의 해당 쪽 탐색은 미확인이다. U 무변화는 unknown 병합의 일반 안전성을 입증하지 않는다. | 기관이 레코드를 동일 실물의 중복으로 정정하거나 운행 날짜·방향의 정차가 바뀌면 분야 판단이 달라진다. C 키가 실제 합쳐지는 표본 또는 같은 문서의 다른 절을 찾지 못하는 실제 이용자가 있으면 표시/행동 결론이 달라진다. | 첫 자료는 Met objectID별 필드·curatorial 기록과 날짜가 맞는 MTA 공식 운행 변경이다. 관리자 재분리 시험 및 사람의 탐색은 별도 수행한다. C3 W의 실제 witness부터 재현하고, W를 새 링크·추가 클릭·실패 fragment 수리로 확대하지 않는다. |

## 개별 시행과 한 시행 합산의 교차 확인

| 확인할 해석 | 실제 witness·기록 위치 | 허용된 도착과 결과 | 배제한 오해 |
| --- | --- | --- | --- |
| C1 B의 Requests 복원 | `BROWSER-C1-B-DIRECT-REQUESTS`, `clicks.csv`1926행; `browser-observations.json`45–63행 | 표시된 Requests 대표를 새 탭에서1회 열어 Prepared Requests 절의 두 원자 확인 | HTTP harness의 실패들을 성공으로 교체하지 않음. HTTPX를 확인한 다른 시행과 합쳐 한 시행2대안으로 만들지 않음 |
| C2 B의 원풀11 회수 | `C2-B-T0043`, `clicks.csv`1118행; `trial-observations.jsonl`1117행 | ecosystem h2→실제 `user_guide/visualization.html#visualization` href; 같은 두 클릭에서 첫 문서10대안과 두 번째 문서 직접 Matplotlib 근거를 합쳐 원풀11 | 형제 목록→Chart visualization 경로 `C2-B-T0006` 자체는2대안만 확인한다. 이 witness를11대안 경로로 잘못 붙이지 않음 |
| C3 A/C의 보완 계약 도달 | `C3-A-T0031`/`C3-C-T0031`, `clicks.csv`1449·1604행 | 첫 PEP800단어의 판·실제 TOC→`#specification`; 같은 시행에서 constructor 경계와 except* 계약 완결 | 다른 시행의 constructor/except* 판독을 합치지 않음 |
| C3 B에서 W만 바뀐 결과 | `C3-B-T0005`와 `C3-B-T0011`, `clicks.csv`1561·1567행 | 형제 목록→PEP 또는 release→PEP. 기본 first800에는 완전 근거가 없지만 W의 같은 PEP 확인된 추가 절에서 완결 | 원풀·카드·키·href 그래프·비용을 바꾸지 않음. first800에서 직접 읽었다고 소급하지 않음 |
| C2 원풀 밖 추가2대안 | `C2-REVALIDATED-QTPANDAS-20261122` / `C2-REVALIDATED-IPYVEGA-20261122`, `clicks.csv`1927–1928행 | 각 시행에서 같은 첫 ecosystem h2와 실제 외부 README를 열어 해당 대안의 A1/A2 완결. 현재 재검증 원장의 exact response hash·창·원자 위치를 확인 | 원풀 분모11 유지. 각 시행은 외부1대안만 추가. 공유 witness를 A/B/C별3번 복제하거나 두 목적지를 같은 시행으로 합치지 않음 |

C1의 한 시행 최대1은 **이번 실행 환경과 실제 수행한 시행의 최대**다. HTTP/브라우저 경로의 접근 차이를 포함한 관측이며, 두 대표를 두 클릭으로 확인하는 것이 논리적으로 언제나 불가능하다는 뜻이 아니다. Requests를 포함한 별도 브라우저 시행은 대표1개를 연 기록이므로 다른 시행의 HTTPX 근거와 사용자 기억을 합쳐 쓰지 않았다.

## 최종 재열람과 정정 확인

2026-11-22 21:13–21:17 UTC에 Q1~Q7의 핵심 원문을 다시 직접 열었다. GitHub issue HTML 웹 opener의 DisabledError는 성공으로 세지 않았고, 같은 공개 issue의 공식 API `title`·`body`를 직접 읽어 대조했다. 이 재독은 기존 원문의 확인이며 신규 원문 최소수에 추가하지 않는다. 새 네트워크 접속을 본 실험의 새 클릭 시행으로 추가하지도 않았다.

| 대응 Q | 다시 직접 읽은 URL·범위 | 이번 재대조에서 확인한 내용·한계 |
| --- | --- | --- |
| Q1 | [#6126 API](https://api.github.com/repos/jgm/pandoc/issues/6126)·[#6095 API](https://api.github.com/repos/jgm/pandoc/issues/6095)의 현재 작성자 body | 엔진 일반 지원과 두 LaTeX 표기 보존 요구를 구분. 과거 수정 전 body 동일성은 미확인 |
| Q2 | [#6135 API](https://api.github.com/repos/vega/vega-lite/issues/6135) title/body 전체·[Vega-Lite TOC](https://vega.github.io/vega-lite/docs/) Text 항목 | 원 요청에는 `text`가 없고 실제 목차에는 Text가 있음. 별도 fallback 풀은 만들지 않음 |
| Q3 | [Data model](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers) web1401–1425·[async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with) web816–847 | 반환 awaitable 의무와 호출자의 두 await·예외 전달 expansion의 위치 차이를 재확인. C4 기준·결과는 유지 |
| Q4 | [Vega-Lite Overview](https://vega.github.io/vega-lite/docs/) web11–12·[pandas Altair](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#altair) web43–45 | 컴파일 방향과 발행자/대상 구현 구별을 확인. 역방향 호환성이나 Altair 구현판을 추정하지 않음 |
| Q5 | [PEP654 Specification](https://peps.python.org/pep-0654/#specification) constructor 정의·except* web342–345·Unmatched Exceptions web394–415; [Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests) web72–132 | 같은 PEP의 두 역할과 Requests의 구성/send 문서 근거 확인. PEP 새 HTTP raw SHA는 `9f5a64abb1ae93b8892d5165a86c5de480156a77ebfe7875e515b6311d48b249`로 기존 receipt와 같음. 코드 실행·사용자 행동 미검증 |
| Q6 | [Projection Types](https://vega.github.io/vega-lite/docs/projection.html#projection-types) web37–56·[Chart visualization](https://pandas.pydata.org/pandas-docs/version/2.0/user_guide/visualization.html#plotting-directly-with-matplotlib) web972–994 | identity/reflectY 하위조건과 직접 Matplotlib 기능 근거를 확인. graticule-label 해결이나 환경별 실행까지 입증하지 않음 |
| Q7 | [Met36491](https://www.metmuseum.org/art/collection/search/36491) web61–72·[Met56353](https://www.metmuseum.org/art/collection/search/56353) web62–73·[A line map](https://www.mta.info/maps/subway-line-maps/a-line) web14–20 및 지선 역 목록 | 제목 공유와 소장품 필드 차이, 노선 지선·방향 범위를 확인. 시간표 p2/p8의 도표 배치 자체는 기존 crossfield 시각 판독 원장으로 대조했으며 이번 재독에서 새 시각 검사를 했다고 주장하지 않음 |

추가로 약점 표의 [NumPy compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html) web65–81을 다시 열어 같은 이름·seed만으로 호출·환경·판의 결과가 같다고 볼 수 없다는 저자 조건을 확인했다. 이것은 새 자연 표본이나 C 키 성능시험이 아니다.

이전 초안에서 집계 대기로 두었던 부분은 위 witness와 현재 결과로 갱신했다. `evidence/arithmetic-corrections.json`의 W 근거 소실·Python 판 정렬·출발 창 SHA/resolve gate 정정은 현재 코드46–62·88–100행과 대조했다. strict complete ID가 W의 부분집합임을 현재 `clicks.csv`의 모든 시행에서 다시 확인했다. 실제 `/3` 현재판·제안 메일의 사실은 원장에 남아도 3.11 계약 합침에는 들어가지 않는다. W 비판독 빈 배열은 부정이 아니며 기존 strict 사실을 유지한다. 이 gate는 이 봉인 입력의 보수적 처리이고 일반 호환성 판정기가 아니다.

`metadata-audit-corrections.json`은 추출 위치가 불명확했던 표시 필드3개를 미확인으로 낮췄다. `evidence/vega/source-scope-correction.md`의 활성 원장도 확인했다. Overview의 링크 목록에 다른 절의 identity 근거를 복제했던 설명을 철회하고 실제 해당 절 또는 별도 W 행에만 남겼다. 정정 전 원장과 키는 이력으로 보존되며 최종 근거로 중복 산입하지 않는다.

## 아직 충족으로 승인할 수 없는 항목

| 수용 항목 | 상태 | 남은 이유·최소 재개 |
| --- | --- | --- |
| Pandoc 원 발행 HTML·원순서 | **미충족** | 후기 DOM과 원응답 byte를 동치로 증명하지 못했다. 위 MANUAL 원응답 확보부터 새 관측을 봉인하고 P4개 원풀은 계속 미확인으로 둔다 |
| V3 원문 명사 기반 발견 | **미충족** | `text` 연상 토큰을 사용한 기존 풀은 보존한다. 원요구 명사와 원규칙 fallback으로 별도 amendment를 사전 고정한다 |
| C4 완전 양성 | **미충족** | 원풀의 확인된 완전 대안0이며 봉인 A2가 남는다. 외부 expansion의 존재로 원풀 양성을 충족 처리하지 않는다 |
| 두 번째 복원 양성 C2 | **미충족** | 첫 대표가 뒤 대안들을 이미 입증한다. 외부2대안은 새 근거 획득이며 원풀 복원 대조의 대체물이 아니다 |
| 사용자 결과·독립 사람 평가 | **미관측** | 통제 HTTP/DOM 및 내부 의미 재독만 수행했다. 과업별 사람 클릭·확신·채택은 별도 관측 대상이다 |
| 최종 고정 SHA·수용 원장·session check | **이 초안에서 미승인** | 루트의 결과·수용 원장 커밋, 고정 SHA 재열람과 실제 check 로그를 확인한 뒤 정식 인계서에서 확정한다. 이 초안의 로컬 검산이 그 절차를 대신하지 않는다 |

## 검토한 파일 버전

다음 해시는 최종 초안 작성 때 읽은 작업 파일의 SHA256이다. 이후 루트가 결과 형식이나 수용 원장을 갱신하면 case·trial ID를 기준으로 재대조해야 하며, 이 표의 해시를 고정 Git 결과 SHA라고 부르지 않는다.

| 파일 | SHA256 |
| --- | --- |
| `groups.jsonl` | `17605ae42f40ce39140acb9bb1939c72e8f352287310efa92c08c89540450fa4` |
| `views.jsonl` | `64d0571cf523be33af06c656e77176874c9c82e6dd65e13e2b67cffa0699f943` |
| `evidence/candidate-evidence.jsonl` | `b00d7e049f8ed261d9192ceea947334e60aa0572fde9f00b3c45b925ff58d492` |
| `evidence/results-data.json` | `dd845db57eef42512ed2e0c9960459c8d8d30ccc6e049d1537770477fd6d4e27` |
| `evidence/trial-plan.jsonl` | `16fbf84c0ac0b0cdc4162a021fb65519560c1eb2b91bf5e4de14fff493c11b66` |
| `evidence/trial-observations.jsonl` | `5094c7d4fb492d46dce83f81b848f92ba95716e95910da1e588194d592973f23` |
| `clicks.csv` | `0a82ad6b5c629f5aa8fa6cbf8553ec2bd4c5909ae65dd63d811b640c90401d91` |
| `changes.csv` | `1a81509d4d396f579901589060486c1235d83028681769d2f14d5d2b13e695df` |
| `gold-paths.csv` | `424f454e38a660d47b6f542a6067fb36e5e74d934c6c9165172289bcc3e95efb` |
| `evidence/arithmetic-corrections.json` | `a0611720dbc9a0ad04afe22473e479a2321f873ceae8792f3c071b380fda3c2f` |
| `evidence/metadata-audit-corrections.json` | `5e4c4b70ff31ccf10bd87d15a1d6ca240742ea43e840dae555bdc5964f0823f1` |
| `evidence/vega/source-scope-correction.md` | `8cc811facf3ce99519a39dd8837cdb42deecf5197bbd7d855d65c33960d5b4a3` |
| `evidence/crossfield/control-second-hop-revalidated-trials.json` | `01fe86bfc8553790068ef630f79720642df8186243b9fb8eae11b39e11279344` |
| `evidence/crossfield/NOTES.md` | `fe012e4d86b2fa97bad04afe883077b0befbe2b74646276bd03a56be40c19177` |
| `evidence/weaknesses.json` | `39c6be7c46f6749dbd9b206edf5b8335cbe6e5608c3eded7e9a4aa5a703711f6` |

## 마지막 약점 세 건

아래 세 건은 `evidence/weaknesses.json`2–19행과 동일한 약점·후속 조사다. Q별 미확인과 이 표를 실제 완료로 바꾸어 읽지 않는다.

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| 자연 표본의 획득 결측과 사전규칙 이탈 | P1–P4 raw HTML·원순서 및 V3 토큰; [MANUAL](https://pandoc.org/MANUAL.html), [V3 원요구](https://github.com/vega/vega-lite/issues/6135); pool.csv2–25행, source-scope/input audit | 같은 MANUAL 원응답 byte를 승인된 수집에서 확보해 SHA/href를 먼저 봉인. V3는 최초요구 명사만으로 새 amendment를 사전 고정; 기존 수치 유지. | 새 자연 풀에 실제 완전 경로가 생기거나 원규칙 V3 fallback이 다른 근거를 포함하면 이름/계약층의 회수·손실 판단이 달라짐. |
| 보강 양성의 부족과 해법 선정 편중 | C4 A2 및 C2 복원 양성의 해석; [Data model](https://docs.python.org/3.11/reference/datamodel.html#async-context-managers), [async-with](https://docs.python.org/3.11/reference/compound_stmts.html#async-with), [ecosystem](https://pandas.pydata.org/pandas-docs/version/2.0/ecosystem.html#visualization); requirements.csv C4행·gold-paths.csv | 새 독립 유지보수/이관 사례의 요구·자연6순서·근접오답을 그룹 계산 전에 봉인. C4를 사후 완화해 채우지 말고 완전 경로와 첫대표에 없는 별개 대안을 실제 확인. | 두 번째 복원 양성과 두 번째 보완 양성이 확보되거나, C4의 의미상 참조를 허용하는 별도 기준이 사전에 채택되면 대조 범위가 확대됨. |
| 키의 구별력과 통제 클릭의 외적 한계 | C=A인 관측8풀·U무변화·Requests HTTP/브라우저 차이; [Requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests), [PEP](https://peps.python.org/pep-0654/#specification), [NumPy](https://numpy.org/doc/stable/reference/random/compatibility.html); groups.jsonl·clicks.csv | 표시 metadata가 실제 같은 C key로 합쳐지는 독립 풀 하나부터 봉인하고 같은3카드로 사람의 과업별 클릭/확신/채택을 별도로 관측. 첫 자료는 현재 views fixture와 원멤버/절 지도. | C가 실제 병합하면서 다른 구현을 살리거나 필수조건을 가리거나, 실제 독자가 긴 문서·형제 목록을 다르게 이용하면 표시·행동 결론이 달라짐. |
