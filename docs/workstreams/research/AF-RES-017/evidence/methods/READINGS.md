# AF-RES-017 방법·비교 문헌 열람 기록

## 인정 수와 읽기 기준

본문 확인 저작은 28건이다. 이 가운데 M27은 사건 반례 후보로 별도 보존하여 방법 문헌 최소치에서 제외했다. 인정되는 방법·비교 저작은 **27건 / 24개 사이트**이며 사이트별 최대 3건 규칙을 충족한다. 동일 저작의 다른 복사본은 중복 계산하지 않는다. 열람 실패·초록·검색 결과만 본 자료는 sources.json의 excluded 34건에 분리했다.

각 문헌의 실제 읽은 절은 아래에 적었다. 읽지 않은 절까지 완독했다고 주장하지 않는다. D1은 지정 절의 본문 확인을 뜻하며, 모든 원문을 파일에 복사해 보관한 것이 아니다. URL·서지·짧은 요약·한계만 저장했다.

| 요구 범주 | 최소 | 인정 | 자료 ID |
|---|---:|---:|---|
| 소프트웨어 재사용 실증 | 5 | 5 | M04, M05, M10, M11, M19 |
| 의학 연구 낭비·누적 시험 | 3 | 3 | M01, M02, M12 |
| 특허 선행기술·유효성 | 3 | 3 | M13, M14, M15 |
| 다중 발견·재발견 | 2 | 2 | M16, M25 |
| 사후 판단 편향 | 2 | 2 | M03, M18 |
| 원리 도입의 실제 구조를 가진 1차 기록 | 5 | 7 | M06, M07, M17, M20, M21, M22, M23 |

사이트별 인정 수는 ResearchGate 3건(M02·M10·M25), stafforini.com 2건(M16·M18), 나머지 인정 사이트는 각 1건이다. 대학 저자 사본도 원 저작으로 읽었으며 단순 메타데이터는 수에 넣지 않았다. 전체 집계와 분류별 ID는 [counts.json](counts.json)에 있다.

## 문헌별 기록

표의 판정과 한계 요약은 내부 수집 작업자의 분석이다. 원문의 저자 진술·측정치는 [sources.json](sources.json)의 confirmed와 limits에서 더 구체적으로 구분한다.

| ID | 문헌·판 | 실제 읽은 범위 | 확인한 내용 | 한계 |
|---|---|---|---|---|
| M01 | [Randomized controlled trials of aprotinin in cardiac surgery: could clinical equipoise have stopped the bleeding?](https://blogs.ubc.ca/googlescholar/files/2009/02/chalmers_etc.pdf) — Fergusson, Glass, Hutton & Shapiro; Clinical Trials 2005; 2:218–232; DOI 10.1191/1740774505cn085oa | pp.218–226: Methods, Results, Discussion, figures1–6 captions (commentary pp.229–232 not counted). | 효능 근거가 축적된 시점과 후속 시험·인용·검색 회수율을 함께 확인했다. | 안전성 시험까지 불필요했다고 할 수 없다. |
| M02 | [Avoidable waste in the production and reporting of research evidence](https://www.researchgate.net/publication/40028343_Avoidable_Waste_in_the_Production_and_Reporting_of_Research_Evidence) — Chalmers & Glasziou; Lancet 374:86–89; online 2009-06-15; issue 2009-07-04; DOI 10.1016/S0140-6736(09)60329-9 | Uploaded original Lancet body: pp.86–88 intro, four-stage figure, unnecessary/poorly designed studies, reporting, conclusions. | 연구 낭비는 질문·설계·출판·보고의 여러 손실을 합성한 개념이다. | 85%를 선행 해법 무지율로 읽을 수 없다. |
| M03 | [Hindsight Bias](https://carlsonschool.umn.edu/sites/carlsonschool.umn.edu/files/2026-01/vohs-et-al-2012-hindsight-bias.pdf) — Roese & Vohs 2012; Perspectives on Psychological Science 7(5):411–426; DOI 10.1177/1745691612454303 | pp.411–413; three-level framework; Debiasing Hindsight Bias; discussion. | 기억 왜곡·불가피성·예견 가능성은 서로 다른 후견 효과다. | 회고 사례를 전부 기각할 근거는 아니다. |
| M04 | [How Reuse Influences Productivity in Object-Oriented Systems](https://www.cs.umd.edu/~basili/publications/journals/J61.pdf) — Basili, Briand & Melo 1996; CACM 39(10):104–116; empirical observation Sep–Dec1994 | pp.104–105 participants; p.109Validity; pp.112–114 reuse/error density and rework. | 재작업을 오류 이해·수정·회귀검사 등 실제 노력으로 측정했다. | 도서관처럼 제공된 재사용 자원을 처음 발견하는 문제와 다르다. |
| M05 | [License Risks from Ad Hoc Reuse of Code from the Internet](https://www.ie.mgt.tum.de/fileadmin/w00cem/tim/Research/Publications/Henkel/Sojer_Henkel_2011_License_risks_Internet_code_reuse_CACM.pdf) — Sojer & Henkel 2011; CACM 54(12):74–81; DOI 10.1145/2043174.2043193; survey 2009 | pp.76–79 survey, reuse extent, regression, information sources; p.81 validity/conclusion. | 인터넷·동료 경로와 라이선스 지식의 부족을 분리했다. | 학습 경로와 해법 최초 발견 경로는 같지 않다. |
| M06 | [Managing Incidents](https://sre.google/sre-book/managing-incidents/) — Andrew Stribblehill; edited Kavita Guliani; Site Reliability Engineering 2016; live chapter | chapter14 opening, Elements of Incident Management Process, The Role of Incident Commander, A Recognized Command Post, Clear Live Incident State Document, Explicit Handoff. | 사고 지휘 체계가 실제 역할·권한·인계 규칙으로 옮겨졌다. | 가상 사고 장면을 실제 사건으로 세지 않는다. |
| M07 | [Innovation at Mettle – Double-Entry and Event-Sourcing](https://www.mettle.co.uk/blog/innovation-at-mettle-double-entry-and-event-sourcing/) — Mettle 2022-06-23 | body: accounting experience; event sourcing relation; WODE schema and balances; immutable ledger. | 회계 균형이 이벤트 구조의 제약으로 구현됐다. | 은행 업무와 회계의 분야 거리는 작다. |
| M08 | [Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html) — Martin Fowler2014-03-06 | body and Ruby example; self-reset/half-open; synchronous/asynchronous discussion. | 차단기는 실패·열림·복구 시험을 가진 구체적 코드 패턴이다. | 2014년 설명으로 최초 발명자를 확정하지 않는다. |
| M09 | [Reactive Streams](https://www.reactive-streams.org/) — Live official specification overview; JVM 1.0.4 release 2022-05-26 | complete 69-line page: problem statement, goals, JVM standard andJava 9 Flow relation. | 비차단 backpressure의 실제 규격 목적을 확인했다. | 유체역학에서 가져온 최초 경로는 적혀 있지 않다. |
| M10 | [Success and Failure Factors in Software Reuse](https://www.researchgate.net/publication/3188233_Success_and_failure_factors_in_software_reuse) — Morisio, Ezran & Tully 2002; IEEE TSE 28(4):340–357; DOI 10.1109/TSE.2002.995420; author manuscript | §2 Research approach; §5.1 success/failure and setup for failure analysis; original author manuscript. | 도입 프로젝트의 관리·과정·인적 조건을 다뤘다. | 저장소 접근성만의 효과 또는 전 산업 실패율이 아니다. |
| M11 | [Code Reuse in Open Source Software Development: Quantitative Evidence, Drivers, and Impediments](https://www.academia.edu/127623324/Code_Reuse_in_Open_Source_Software_Development_Quantitative_Evidence_Drivers_and_Impediments) — Sojer & Henkel 2010; JAIS 11(12):868–901; DOI 10.17705/1jais.00248 | Original text§4 data; §5.1 importance; §5.2 benefits/issues; §5.3 regression; §5.4 validity. | 재사용의 이득과 통제·의존성·업데이트 부담을 함께 조사했다. | 자기 보고 상관관계이며 인과 절약액이 아니다. |
| M12 | [Accumulating Research: A Systematic Account of How Cumulative Meta-Analyses Would Have Provided Knowledge, Improved Health, Reduced Harm and Saved Resources](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0102670) — Clarke, Brice & Chalmers 2014-07-28; PLOS ONE 9(7):e102670 | Methods/inclusion/search/assessment; Results four trajectory types; Discussion. | 누적 근거가 안정되는 경우뿐 아니라 초반 결론이 뒤집히는 경우도 포함한다. | Lau 1992의 요약을 Lau 원문 열람으로 세지 않는다. |
| M13 | [Empirical Evidence on the Validity of Litigated Patents](https://mail.ipmall.info/sites/default/files/BAYHDOLE/3_DIV_SCAN/3068_001_OCR_DBL_ZIP_0.pdf) — Allison & Lemley 1998; AIPLA QJ 26:185–275; original issue scan | pp.194–205 population, coding, limitations; pp.205–207 validity; pp.231–234 cited versus uncited prior art and footnotes. | 판결 표집·중복 판단 단위·선행기술 구분을 확인했다. | 미인용 선행기술과의 차이 p=.057을 유의한 차이로 단정하지 않는다. |
| M14 | [Ex Parte Reexamination Filing Data](https://www.uspto.gov/sites/default/files/documents/ex_parte_historical_stats_.pdf) — USPTO; first report through 2025-09-30;18-page historical bundle | First 2 pages: request counts, pendency, certificate outcomes and footnotes. | 재심사 요청·증서·청구항 단위와 처리기간을 구분했다. | 선택된 재심사 절차이며 전체 특허의 낭비율이 아니다. |
| M15 | [Applicant and Examiner Citations in US Patents: An Overview and Analysis](https://www.hbs.edu/ris/Publication%20Files/09-016_154955ba-d4bf-4c81-ac15-38a2b95ad2ef.pdf) — Alcácer, Gittelman & Sampat; July 2008 working paper09-016 (not later 2009 journal version) | §1 citation interpretation; §4 data/variables; Table 1 and accompanying interpretation (not all regression sections). | 심사관/출원인 인용과 특허별/인용쌍별 분모를 구분했다. | 심사관이 인용했다고 발명자가 몰랐다는 뜻은 아니다. |
| M16 | [Singletons and Multiples in Scientific Discovery: A Chapter in the Sociology of Science](https://pdf.stafforini.com/merton-1961-singletons-multiples-scientific.pdf) — Robert K. Merton 1961-10-13; Proc. APS 105(5):470–486; presented 1961-01-23 | pp.474–481 adumbrationism, rediscovery/unpublished prior work and priority; pp.483–486 264 multiples and qualifications. | 독립·동시·재발견·미발표 선행 작업을 분리했다. | 264건은 전체 발견의 분모가 아닌 선별된 다중 발견이다. |
| M17 | [A Brief History of Kanban for Knowledge Work](https://djaa.com/brief-history-kanban-knowledge-work/) — David J. Anderson; live retrospective article (publication date not shown); internal events October 2004, winter 2005, September 2006, January 2007 | timeline October 2004 through2007; origin distinction DBR→kanban; board introduction. | DBR에서 kanban으로 가는 당사자의 단계별 설명을 읽었다. | 최초 날짜와 인지 변화는 M27의 원저와도 대조해야 한다. |
| M18 | [The Hindsight Bias: A Meta-analysis](https://pdf.stafforini.com/christensen-szalanski-1991-hindsight-bias-metaanalysis.pdf) — Christensen-Szalanski & Willham 1991; OBHDP 48:147–168; DOI 10.1016/0749-5978(91)90010-Q | pp.149–150 selection; Table 1 p.155; pp.158–160 practical decision effects. | 실험 평균 효과와 실제 의사결정 문턱의 차이를 확인했다. | 과거 실험의 r을 현대 소프트웨어 작성자의 오류율로 쓰지 않는다. |
| M19 | [Large-scale Code Reuse in Open Source Software](https://mockus.org/papers/ossreuse.pdf) — Audris Mockus; ICSE'07 FLOSS workshop 2007-05-21; author PDF | §3 sampling/directorymatching; §4 results; §5 threats; §6 discussion. | 대규모 코드 복제가 재사용 추적 지표임을 확인했다. | 복제량을 독립 재발명의 비용으로 계산하면 방향이 뒤집힌다. |
| M20 | [Self-Nonself Discrimination in a Computer](https://profsforrest.github.io/homepage/data/publications/1994-self-nonself.pdf) — Forrest, Perelson, Allen & Cherukuri 1994; IEEE Symposium on Research in Security and Privacy:202–212 | §1 intro/systemoverview; §3 experiments; §4 discussion. | 면역학의 음성 선택이 탐지 절차로 옮겨졌다. | 원문은 실제 배치를 미해결 문제로 남긴다. |
| M21 | [Epidemic Algorithms for Replicated Database Maintenance](https://www.cis.upenn.edu/~bcpierce/courses/dd/papers/demers-epidemic.pdf) — PODC 1987; DOI 10.1145/41840.41841; 1987 ACM copyright and /87/0008 code directly visible in Cornell copy. | Introduction; §0.1 Motivation; anti-entropy and rumor-mongering mechanisms; spatial distribution counterexamples; conclusion. Cornell copy cover/date and pp.1–2 rechecked. | 역학 대응과 Xerox 설치, 과도한 remailing 조사 경위를 확인했다. | 새로 발견한 것은 문제적 구성일 수 있으며 원리 무지와 같지 않다. |
| M22 | [The Operational Analysis of Queueing Network Models](https://www.columbia.edu/~ww2040/8100S12/DenningBuzen1978.pdf) — Denning & Buzen 1978-09; ACM Computing Surveys 10(3):225–261 | Introduction; operationalvariables/laws; Little's Law p.235; response-time formulas pp.237–238. | 컴퓨터 성능을 측정 가능한 운영량·관측 창으로 관계화했다. | Scherr 1965에 대한 역사 서술은 원저 추가 확인이 필요하다. |
| M23 | [Optimization by Simulated Annealing](https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TemperAnneal/KirkpatrickAnnealScience1983.pdf) — Kirkpatrick, Gelatt & Vecchi; Science 220(4598):671–680; 1983-05-13; DOI 10.1126/science.220.4598.671 | pp.671–672 statistical-mechanics mapping; p.679 summary and conclusions; examples of placement and routing inspected. | 물리적 에너지·온도·수용 확률의 알고리즘 대응을 확인했다. | 스케줄·목적함수·이웃 정의의 품질을 대신하지 않는다. |
| M24 | [A Proof for the Queuing Formula: L = λW](https://fisherp.scripts.mit.edu/wordpress/wp-content/uploads/2015/11/ContentServer.pdf) — John D. C. Little 1961; Operations Research 9(3):383–387; received 1960-11-09; DOI 10.1287/opre.9.3.383 | Complete original pp.383–387: definitions, Theorems 1–2, proof, discussion. | 원 증명의 경계·평균·정류성 조건과 반례를 읽었다. | 항등식 자체는 개입의 인과 효과가 아니다. |
| M25 | [Bridging Academia and Industry: How Geographic Hubs Connect University Science and Corporate Technology](https://www.researchgate.net/publication/336002925_Bridging_Academia_and_Industry_How_Geographic_Hubs_Connect_University_Science_and_Corporate_Technology) — Bikard & Marx; online 2019-09-23; Management Science 66(8):3425–3443(2020); DOI 10.1287/mnsc.2019.3385 | §3 twin-identification and patent-citation analysis; discussion and limitations; original author-licensed full text. | 같은 발견을 담은 논문 사이 산업적 주목을 비교하는 방법을 확인했다. | 인용은 주목의 대리변수이며 회피 가능한 중복 노동량이 아니다. |
| M26 | [Little’s Law as Viewed on Its 50th Anniversary](https://projectproduction.org/journal/reprint-littles-law-as-viewed-on-its-50th-anniversary/) — John D. C. Little 2011; Operations Research 59(3):536–549; DOI 10.1287/opre.1110.0940; authorized reprint 2016-12-18 | §1–2 finite-window formulation; §4.1 computerarchitecture; §5 first-person history. | 원 저자가 설명한 유한 관측 창과 컴퓨터 적용을 확인했다. | 역사 회고로 특정 팀의 늦은 발견을 만들지 않는다. |
| M27 (비인정 보조) | [Kanban: Successful Evolutionary Change for Your Technology Business](https://img1.wsimg.com/blobby/go/b7728943-bef2-4e66-8058-ebe0b3999a7c/downloads/Blue%20Book%20Kanban-eng.pdf?ver=1730882190712) — David J. Anderson; Blue Hole Press 2010; ISBN 978-0-9845214-1-8 (PDF) | Copyright p.iv; Reinertsen foreword pp.xiii–xiv; chapter 1 pp.4–6; chapter 2 pp.11–12. Other chapters not counted. | 기제는 이미 알았으며 Microsoft 최종 결과는 같았을 것이라는 직접 반례다. | 사건 후보이므로 방법 문헌 최소치에서 제외; 여러 인지 날짜를 합치지 않는다. |
| M28 | [Notes on Backpressure Routing](https://ee.usc.edu/stochastic-nets/docs/backpressure.pdf) — Michael J. Neely; EE 649 Stochastic Network Optimization; Spring 2011 | §I history and pressure-gradient analogy; §II model assumptions; §III Lyapunov drift and B delay caveat; §IV extensions; references. | 서로 다른 backpressure 용어와 처리량/지연 차이를 원 저자 노트로 확인했다. | Reactive Streams와 같은 알고리즘·계보라고 추론하지 않는다. |

## 검색·접근 기록

검색 23묶음·질의 84개를 [SEARCH_LOG.json](SEARCH_LOG.json)에 그대로 남겼다. 마지막 MS022·MS023은 쉽게 찾히는 선행 자료, 정당한 미채택, 초기 결론의 반전, 미발표 선행 작업, 이름과 구조의 불일치를 일부러 찾은 재검색이다. 검색 결과 자체는 D0이며, 기존 원문 또는 새로 연 M27·M28에 연결된 것만 근거로 사용했다.

익명 GET 응답은 [NETWORK.json](NETWORK.json)에 호스트·UTC·코드를 남겼다. executor에서 403 또는 시간초과가 나고 허용된 웹 열람에서 본문이 반환된 경로는 별도로 기록했다. 계정·로그인·결제·네트워크 제한 우회를 사용하지 않았다.

## 한계

지정된 대표 원저 중 Lau 1992는 NEJM 403으로 직접 읽지 못했다. Fischhoff 1975와 Katz·Allen의 초기 NIH 원저도 공개 경로에서 본문 접근이 실패했다. 이 자료는 minimum에 넣지 않았고, 실제 읽은 다른 원저들로 각 하위 최소 수를 충족했다. 재개 URL과 명령은 CROSSFIELD-DRAFT.md §5에 있다.

M27 원저의 서문·제1장·제2장이 제시하는 사건과 인지 날짜를 동일한 발견으로 합치지 않았다. 이름이 달라졌다는 사실과 실제 구조가 바뀐 사실을 구분하는 직접 반례로만 보존했다.

이 자료군은 Q7·Q8의 방법·비교용 목적 표집이다. AF-RES-017 사건 40건의 빈도나 제품 효과를 이 문헌 수로 계산해서는 안 된다.
