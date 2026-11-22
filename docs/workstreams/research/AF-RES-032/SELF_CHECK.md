# AF-RES-032 자체 점검

**결과 수용 상태: REVIEW_READY_WITH_GAPS.** 엄격한 상류 시행→같은 목적의 소비자 공개판 날짜쌍은 A에서0/12, B에서0/6이다. 계산 적격 조건부 분모가0이므로 지연 결과는 **해당 없음**이며0일, 전파율0%, 우측 검열 또는 조사 종료 실패를 뜻하지 않는다. 확인한 실제 href 수정, 유지, 추천 폐기, 목적 불일치와 다음 최소 자료를 제출한다.

## 점검 기준과 실측 분모

| 항목 | 확인한 값과 한계 |
|---|---|
| 원문 최소수 | `evidence/counts.json`: 보수적으로 선택한 고유 원문75개, source 원장395행. A원문12·상류34·소비자후속8·타분야8·기타원문1·B소비자5·B보조7. 75는 모든 의미상태의 완전한 총수가 아니다. |
| A 표집 | 서로 다른 출판 HTML12문서, 두 유통 경로 각6참조,6프로젝트 각2참조. 원 A12 접두 바이트 SHA256 `b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562` 유지. |
| A 후속 관측 | actual archive123개, 문서 상태246개, 실제 존재 HTML211개, 내려받은 archive에서 확인한 멤버 부재35개. 부재35와 읽지 않은 SQLite46판을 구별한다. |
| A 변화와 현재 판단 | 같은 목적의 href 변경5/12참조, 독립 소비자 소스 수정4사건. 현재 최소 읽기 목적 판단은 유지9·교체2·보류1이다. 배포자 주소 수정과 연구자의 현재 목적 판정을 동일 분자로 합치지 않는다. |
| B 시도 | 6사건,18질의,17후보 문서 계열. 실제 archive HTML3·버전 웹 HTML2·역사적 배포 HTML 미확인1. B05는 A-D04 중복이며 추가 독립 HTML 소비자는4개다. |
| B 변화와 현재 판단 | 같은 목적 href 수정은 중복 포함2건, A중복 제외1건. 현재 판단은 유지4·교체1·보류1. B04는 HTML 기준 판정 불가이며 보류를 정답으로 세지 않는다. |
| 서로 다른 시계 | source committer→실제 CRAN Date/Publication 보조쌍은 A3참조/2소스사건, B1참조. 이 수치를 상류 시행→소비자 공개판 지연으로 전환하지 않는다. |
| 독자와 검열 | 같은 노출 매체로 연결된 독자 실패 사슬0, 별도 live-web 독자 보고1, 우측 검열0. 시작을 모르는 것은 미확인이다. |
| 남은 표본 공백 | SQLite는 열거51판 중5판만 읽었고46판 미열람. B04는 원 sdist/README만 있고 당시 렌더링 HTML이 미확인이다. |

집계 근거는 [counts](evidence/counts.json), [chains](chains.csv), [intervals](intervals.csv), [sources](sources.jsonl), [통합 감사](collectors/cran/integration-audit.json)다. 통합 감사의 대상은 HEAD `ffbce62e4c01459ebbfb006a5d6c67e425ed7c17` 및 그 영수증에 적힌 작업 트리 입력 해시이며, 이후 결과·인계 커밋을 미리 검사한 것은 아니다.

## 작성자와 판독자의 지식 범위

이 초안은 `/root/offline_a`가 기존 원장과 감사 영수증을 읽고 작성했다. 작성자는 D03–D06과 B05를 수집했고, 이후 Python/root B 자료를 별도 내부 재판독했다. 그러므로 D03–D06/B05에는 동일 수집자 자기 점검, Python/httr에는 별도 내부 재판독이라는 다른 성격이 있다. Python19판과 httr8판의 원 archive 재독은 [audit-root.json](collectors/offline/audit-root.json)에 기록되어 있다.

CRAN R 수집·78 archive 검산은 R 수집자의 영수증을, 타 분야는 다른 수집자의 직접 열람 기록을, A/B 세 보기 판단은 각각 별도 내부 판독자의 봉인 입력/결정 파일을 이용했다. 이 SELF_CHECK 작성 중에는 새 외부 검색이나 외부 원문 열람을 추가하지 않았다. 모든395개 원문을 작성자가 다시 열었다고 주장하지 않는다. 별도 내부 판독은 **외부 사람의 독립 검토나 실제 이용자 실험이 아니다**.

## Q1–Q8 주장·반증·미확인 점검

| 주장 | 근거 주소·위치 또는 탐색 실패 영수증 | 자기 결론을 뒤집을 조건 | 실제 반증을 찾은 경로와 결과 | 남은 미확인 |
|---|---|---|---|---|
| **Q1-1. A12는 실제 배포 파일 속 서로 다른 HTML12문서에서 출발한다.** 공식 오프라인 문서와 CRAN archive 속 이미 빌드된 vignette의 두 경로다. | [A 봉인 영수증](evidence/a-seal-remote.json), `references.jsonl` 첫12행; [PostgreSQL12.2 archive](https://ftp.postgresql.org/pub/source/v12.2/postgresql-12.2.tar.bz2), [SQLite3.31.0 문서zip](https://www.sqlite.org/2020/sqlite-doc-3310000.zip), [knitr1.27 archive](https://cran.r-project.org/src/contrib/Archive/knitr/knitr_1.27.tar.gz); member와 SHA는 각 참조행. 통합 감사 IA07/08. | 실제 멤버가 HTML이 아니거나, 같은 원고를 이름만 바꾸어 두 문서로 셌거나, 원 A가 봉인 뒤 바뀐 증거가 발견되는 경우. | 발행처 이름만으로 판정하지 않고 archive/member를 열었다. PostgreSQL 전용 doc 경로404 뒤 source tar 안의 prebuilt HTML을 확인했다. root의 fresh GET와 별도 Python/httr raw 재독, R18/18 검산이 해당 바이트를 대조했다. | 버전 파일의 첫 공개 순간과 최초 생성 바이트의 불변성은 모두 증명된 것이 아니다. 현재 서버 metadata·mtime은 그 증거로 쓰지 않는다. |
| **Q1-2. 날짜 우선 표집은 A 봉인 전에 정정됐지만 최초 초안은 요구 순서를 어겼다.** | [preseal-order-correction](evidence/preseal-order-correction.md), [scope-deviations](evidence/scope-deviations.md), `collectors/cran/provisional-project-order/`, 최종 `collectors/cran/final/`; 정정2026-11-22T07:17Z, A원격 봉인168d90b… 재독07:18:08Z. | 목적지나 소비자 후속 결과를 본 뒤 유리한 표본으로 바꾸었음이 나타나면 사전 표집의 주장은 성립하지 않는다. | 초기 프로젝트 순 provisional R6을 보존하고 최종 분모에서 제외했다. 최종 frame은 날짜→배포처→멤버 순이다. D는 사전 프로젝트별2 strata여서 구성원은 같고 순서만 정정했다. 실제 병렬 접근 순서를 표집 순서와 같았던 것으로 고치지 않았다. | 초안의 절차 오류는 남는다. 봉인 전 정정이라는 완화와 완벽한 최초 사전등록은 다르다. |
| **Q2-1. 원 href·문맥·목적과 최소 성공 조건을 상류/후속 열람 전에 고정했다.** | `references.jsonl` A접두, [a-sealed.jsonl](evidence/a-sealed.jsonl), [봉인검사 IA07](collectors/cran/integration-audit.json); 각 archive/member SHA, raw href/base/resolved/fragment, anchor/link text, 앞뒤 문장. | raw href가 연구자 정규화 주소로 대체됐거나 후대 목적 판단이 원 봉인에 삽입된 경우. | IA07에서50,326바이트 접두 전체가 원격 봉인과 같음을 대조했다. [postseal-amendments](evidence/postseal-amendments.jsonl)에 reader/시각 역할 보강을 따로 남겼고 A접두는 수정하지 않았다. | 문장은 클릭 목적의 근거이며 실제 독자의 클릭·정확한 심리·실행 의도를 직접 관찰한 자료는 아니다. |
| **Q2-2. 원 URL의 세부 경로가 독자 의도를 완전히 규정하지는 않는다.** R04의 preview 주소가 preview판 재현 의도를 입증하지 않는다. | [rmarkdown2.1](https://cran.r-project.org/src/contrib/Archive/rmarkdown/rmarkdown_2.1.tar.gz), `rmarkdown/inst/doc/pandoc.html` R-S04; [fresh reread](evidence/primary-reread.json) A-R04. A-R05 R-S05는 dbplyr 루트와 별도 backend NEWS 절을 구별. | 편집자의 원 설명이나 해당2020 IDE 배포물이 반드시 preview판을 요구했다고 입증하면 목적 분류와 보류 판단을 고쳐야 한다. | R04 원 본문과 Pandoc1.12.3 조건, href preview, 일반 IDE 링크텍스트를 함께 읽었다. R05에서 선택된 package-root를 다른 NEWS fragment 요구와 합치지 않았다. | 왜 preview를 골랐는지, 현 IDE payload/Pandoc이 rmarkdown2.1에 주는 실제 실행 호환성은 미확인이다. |
| **Q3-1. HTTP200·같은 도메인만으로 목적 충족을 판정하지 않았다.** A-R06과 B02는 대상/절이 달라진 반례다. | A-R06 [옛 BTS URI](http://www.transtats.bts.gov/DatabaseInfo.asp?DB_ID=120&Link=0), R-U06의 BorderCrossing 응답·onload payload; R-U09/10/11. B02 `collectors/b/root-current-observations.json`, [옛 GitHub rate-limit URI](https://developer.github.com/v3/#rate-limiting), [현재 목적별 절](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api). | 옛 BTS URI가 실제로 같은2013항공 데이터 출처를 제공하거나, GitHub 최종 본문에 원 fragment와 필요한 대기/reset 절이 있는 재현 가능한 관측이 나오면 현재 교체 판단을 재검한다. | 같은 정부 domain인데 국경통과 내용으로 도착하는지,200인 GitHub 개요에 목표 절이 없는지를 원문에서 확인했다. 별도 항공2013월별 카탈로그와 rate-limit guide를 읽었다. BTS script 목적지 GET503을 브라우저 실행 성공으로 해석하지 않았다. | 마지막 정상 HTTP 상태·개별 redirect/fragment 소실 시행일·2013ZIP과 nycflights13의 정확한 데이터 동일성·실제 독자 피해는 미확인이다. |
| **Q3-2. 주소가 바뀌어도 같은 읽기 목적이 유지되는 사례를 보존했다.** A-D01·A-D04·B03 등에서 현재 원 주소 반환을 유지할 수 있다. | A-D01 [Docutils 원 주소](http://docutils.sourceforge.net/rst.html)와 fresh reread; A-D04 [RFC4180 원 주소](https://tools.ietf.org/html/rfc4180) PG-U02; B03 [curl_easy_setopt 원 주소](https://curl.haxx.se/libcurl/c/curl_easy_setopt.html) B03-old. | 현재 최종 본문이 지정 문서/기능을 제공하지 않거나 목적이 특정 옛 API·실행판 재현이었다는 문장이 발견되는 경우. | RFC4180 최종 info 페이지에 실제 Section2 본문이 있는지 읽었고, 새 번호 RFC7111은 CSV fragment를 다루므로 quoting 원문 대체가 아님을 비교했다. Docutils와 curl은 주제/함수 절을 확인했다. | 현재 유지가 과거 모든 날짜의 정상 작동을 뜻하지 않는다. 과거 redirect 시행 시각과 구 런타임의 모든 최신 옵션 지원은 미확인이다. |
| **Q4-1. 최초 새 배포판은 완전하게 읽은 계열에만 한정했다.** Python3.8.15, PostgreSQL12.19, knitr1.30, dplyr1.0.2가 해당 경계다. | [Python3.8.14](https://docs.python.org/ftp/python/doc/3.8.14/python-3.8.14-docs-html.tar.bz2)/[3.8.15](https://docs.python.org/ftp/python/doc/3.8.15/python-3.8.15-docs-html.tar.bz2); [PG12.18](https://ftp.postgresql.org/pub/source/v12.18/postgresql-12.18.tar.bz2)/[12.19](https://ftp.postgresql.org/pub/source/v12.19/postgresql-12.19.tar.bz2); R-F023/024 [knitr1.30](https://cran.r-project.org/src/contrib/Archive/knitr/knitr_1.30.tar.gz), R-F021 [dplyr1.0.2](https://cran.r-project.org/src/contrib/Archive/dplyr/dplyr_1.0.2.tar.gz); `editions.csv`·각collector inventory. | 빠진 중간 판에 더 이른 변경 또는 되돌림이 있거나 같은 제목의 다른 문서를 잘못 연결한 경우. | Python19판·PG21판·R78 archive를 열거 원장과 대조했다. 별도 감사에서 Python19판/38HTML과 httr8판을 raw tar로 재독했고 PG12.18→19 해당 문단은 href만 다름을 검산했다. | 모든 major의 최초, 웹사이트의 최초 deploy, 독자 설치판 갱신 시각이라는 확대는 불가하다. SQLite는5/51판만 관측했다. |
| **Q4-2. 문서 부재·예제 변경·추천 폐기를 같은 목적 링크 정정에 넣지 않았다.** | R04 `pandoc` 문서 retirement, R06 flights→Star Wars 변경, R01 simple-datatables로 변경된 후속 상태; [httr1.4.7](https://cran.r-project.org/src/contrib/Archive/httr/httr_1.4.7.tar.gz) `api-packages.html`; 통합 IA26 및 `collectors/offline/AUDIT_ROOT.md`. | 원래 목적을 유지하는 직접 대체 문단이 실제 배포물에서 확인되면 retirement/대체 분류를 재검한다. | httr1.4.3–6의 rate-limit 문단을1.4.7의 httr2 권고와 비교했다. R06에서 항공 예제와 Star Wars 예제의 목적을 분리했다. 내려받은 archive에서35멤버 부재를 확인했으나 이를 미열람46판과 합치지 않았다. | 삭제 뒤 동일 목적 자료가 다른 문서로 별도 출판됐을 가능성은 완전히 소진하지 않았다. 부재만으로 독자 실패를 주장하지 않는다. |
| **Q5-1. 사건 우선 B6은 실패·중복·다른 매체를 포함하는 별도 분모다.** | [B 봉인](collectors/b/b-sealed.jsonl), [remote seal](collectors/b/remote-seal-receipt.json), `collectors/b/root-consumer-attempts.jsonl`, `collectors/cross/b/attempts.jsonl`, `collectors/offline/b05/screening.jsonl`; 통합 IA13–15. | 기록되지 않은 질의/후보, 성공을 본 후 사건 교체, B05를 새 독립 성공으로 세는 집계가 발견되는 경우. | 사건별3질의 상한, 전체18질의/17후보를 기록했다. gh는 HTML부재·이미 새 링크, B03은 옛 href 유지, B05는 알려진 A-D04 재사용임을 남겼다. B수집자의 사전 노출과 마스크 판독자의 지식을 구별했다. | B01/B06은 버전 웹만 읽었고 불변 archive/정확한 공개 시각이 미확인. 검색 색인의 완전성과 웹 전체의 최초6사건은 주장하지 않는다. |
| **Q5-2. B04를 HTML 양성으로 승격하지 않았으며 B01 범위 위반도 실패 영수증으로 보존했다.** | B04 CB-S15/16 PyPI sdists의 `README.rst`, HTML0개; CB-S10 현재 웹·CB-S20 새 Google 본문·CB-S24원장; `collectors/cross/b/attempts.jsonl`의 B01-C4, CB-GET30/33/34; [scope-deviations](evidence/scope-deviations.md). | 실제 날짜 있는 SphinxSitemap2.2.0/2.2.1 렌더링 HTML이 나오면 B04 매체/판정을 재개한다. 범위 밖 후보가 허용됐다는 근거가 없다면 그 위반을 취소할 수 없다. | B04 역사 HTMLzip404, sdist HTML0개, 옛 URI429와 별도 새 URI200을 분리했다. 제외 대상 JupyterLab을 B01후보로 요청한 것은 범위 위반이며3개 추정zip GET 모두404였다. 원문0·최소수0·수정분자0, 비용에는 포함한다. | B04의 역사 HTML은 미확인. JupyterLab을 허용 후보로 소급 정당화하지 않는다. 이 절차 조건은 false로 남겨 WITH_GAPS에 반영한다. |
| **Q6-1. 엄격한 시행→같은 목적 공개판 쌍은0이며 시작 미상을 검열로 바꾸지 않았다.** | `intervals.csv` strict18행, [counts](evidence/counts.json), 통합 IA17/23/24; [Python 상태 로그](https://discuss.python.org/t/github-issues-migration-status-update/14573), P-U06 live-web 독자 기록. | 같은 사건·같은 목적·같은 노출 매체에 대해 실제 시행과 해당 archive 공개 시각의 정확한 값/근거 있는 상하한이 함께 확보되는 경우. | source commit, merge, build, 제품 release day, CRAN Date/Publication, HTTP metadata와 독자 보고를 분리했다. Python 독자는 live `/3/`를 읽었으며 sealed docs-query나 offline판 클릭은 미확인임을 보강했다. | strict 적격 분모0, 우측 검열0. 공개판에 접근할 수 있었다는 사실과 실제 클릭/실패는 다르다. |
| **Q6-2. source committer→CRAN 배포 보조량은 A3참조/2사건, B1참조다. Python156일은 보고값→committer의 명목 차이뿐이다.** | R-C01 [knitr commit](https://github.com/yihui/knitr/commit/6c4388737598d3411abde548bac0107fbf54c790)와 R-F023/024; R-C02 [dplyr commit](https://github.com/tidyverse/dplyr/commit/a28d481259e23f1a7c739e0ebdf873144c446524)와 R-F021; B02-SOURCE/httr1.4.3 DESCRIPTION; `intervals.csv` 보조7행·IA18–20. | committer를 author/merge로 혼동했거나 DESCRIPTION이 다른 archive의 값이거나 원래 목적이 바뀐 판을 보조 수정쌍에 넣은 경우. | R01/R02의 같은 commit을 한 사건으로 합쳤다. 52,600초 두 참조, R05 510,146초, B02 14,044초를 재계산했다. httr author와 committer 차이, Packaged 별도 역할을 확인했다. Python13,480,547초는 공식 분 표시 상태 보고→source committer이며 실제 서버 시행 bound를 제거했다. | merge/build/독자 시각은 다수 미확인. Python의156일00:35:47을 실측 시행 지연이나 공개판 지연으로 쓰지 않는다. PG29일은 날짜 차이뿐이다. |
| **Q7-1. 새 판·새 번호로 바꾸면 원 목적이 나빠질 수 있으며 보류도 실측 결과다.** | PG-U05 [RFC7111](https://www.rfc-editor.org/rfc/rfc7111.txt), PG-U06 errata; R-S03의 `page-break-after` 원 호환성 설명, R-S04 Pandoc/preview 조건; `comparisons.csv` A-D04/A-R03/A-R04. | 인용 문장이 실제 최신 규범을 요구하거나 옛 속성/판이 더 이상 최소 목적을 충족하지 못한다는 같은 목적의 근거가 나오면 유지/보류를 바꾼다. | RFC4180 quoting과7111 fragment를 비교했고, R03 원문이 이미 새 `break-after`와 옛 호환 속성을 구분함을 확인했다. R04는 역사판 유지 의도를 단정하지 않고 원문을 fresh GET해 조건을 다시 읽어도 보류로 남겼다. | 같은 판 재현, 오늘의 사용법, 연구 결과와 errata의 역할을 항상 자동 결정할 수 없다. 후대 errata 상태를2020독자의 정보에 넣지 않는다. |
| **Q7-2. 통계 vintage와 역사 카탈로그의 인용 목적을 새 분야 두 쌍에서 시험했다. 소프트웨어 전파 분모에는 합치지 않았다.** | X-S01–05: [ONS2022연차판](https://www.ons.gov.uk/economy/grossdomesticproductgdp/compendium/unitedkingdomnationalaccountsthebluebook/2022/nationalaccountsataglance), [2023개정 공표](https://www.ons.gov.uk/economy/grossdomesticproductgdp/articles/impactofbluebook2023changesongrossdomesticproduct/2023-09-01), [실제 인용 BoE Box C](https://www.bankofengland.co.uk/monetary-policy-report/2023/november-2023). X-S06–08: [1936카탈로그](https://www.moma.org/documents/moma_catalogue_2748_300086869.pdf) Fig114/목록152, [현재 작품 기록](https://www.moma.org/collection/works/79269), `collectors/cross/citations.json`의 실제 역사 논증 인용. | 당시 보고서/전시사의 인용이 아니라 오늘의 최선 추정을 요구했다는 문맥, 또는 작품 식별이 서로 다르다는 자료가 발견되는 경우. | 통계2021성장률7.5(2022판),7.6(개정 직전 QNA),8.7(2023개정)을 분리했다. 카탈로그1914와 현재 작품1915(뒷면1914표기)를 이미지·치수·소장처 및 역사 논증과 대조했다. 오래됐다는 이유만으로 역사 목적을 부여하지 않았다. | 2022당일 원 bytes, 개체 재연대 결정일·웹 수정일,1936스캔 최초 게시일·1941편지 원본 직접 열람은 미확인. 두 쌍은 소프트웨어 전파율을 대표하지 않는다. |
| **Q8-1. 세 보기의 관측은 판단 보조 자료의 효용을 보여 주지만 배포이력만의 인과효과를 분리하지 못한다.** | `comparisons.csv`, [comparison-counts](evidence/comparison-counts.json), [protocol note](evidence/comparison-protocol-note.md), A `collectors/cross/L1–L3-receipt.json`, B `collectors/cran/B-L1–L3-receipt.json`. | 동일 현재 근거를 통제하고 이력만 달리한 입력, 독립 원문 대조, 사전노출 없는 판독에서 다른 결과가 나오면 효과 해석을 바꾼다. | L1/L2는 A12·B6 모두 보류였다. L3는 현재 상태·본문과 이력·일부 수집자 해석을 동시에 추가해 A11정답/1보류, B5정답/1보류로 대조됐다. 보류를 정답에 넣지 않았고 B04평가불가/B05중복을 분리했다. | 이력 단독효과, 실제 이용자 정확도, 설치/클릭 성공은 측정하지 않았다. L3가 수집자의 사실 요약을 입력받았다는 의존성이 남는다. |
| **Q8-2. 사전노출·비용·빈 시계를 실측 가능한 단위로 남겼다.** | A-D04 사전 B05요약 노출: `collectors/cross/L3-receipt.json`; B03 잠정curl배경: `collectors/cran/B-L3-receipt.json`; `comparisons.csv` 및 `scripts/compare_views.py`. | 판독자가 미제공 원문/결론을 더 보았다는 영수증, 또는 숨긴 추가 웹 조회가 발견되는 경우. | 별도판독자의 추가 외부 page 조회0, A카드50회/B카드23회를 별도로 기록했다. A-D04/B03 제외 민감도를 계산하고, A판독자의 L3 전 노출과 B05수집자의 기존 A지식을 혼합하지 않았다. | 카드 수는 새 외부 원문/페이지 수가 아니다. 소비자 merge/build/reader_report 세 칸 중 비어 있는 칸은18행 합53이며 모든 날짜 필드의 총누락수가 아니다. 사람 시간/금전 비용은 측정하지 않았다. |

## 세 보기 집계의 분모와 반례

| 표본·보기 | 시도 분모 | 수집 근거 대조상 정답 행동 | 오교체 | 잘못 유지 | 보류 | 별도 제한 |
|---|---:|---:|---:|---:|---:|---|
| A L1 | 12 | 0 | 0 | 0 | 12 | URL만으로 현 응답/본문을 제공하지 않음 |
| A L2 | 12 | 0 | 0 | 0 | 12 | 용도·판을 추가했으나 현재 관측 없음 |
| A L3 | 12 | 11 | 0 | 0 | 1 | A-D04 사전노출; 카드50회 |
| B L1 | 6 | 0 | 0 | 0 | 6 | HTML기준 불가 B04, A중복 B05를 별도 표시 |
| B L2 | 6 | 0 | 0 | 0 | 6 | 같은 제한 유지 |
| B L3 | 6 | 5 | 0 | 0 | 1 | B03 사전배경, B04평가불가, B05중복; 카드23회 |

정답은 수집자의 전체 문맥 기준판정과 내부 카드 판독 결과의 일치이며 외부 정답집·실제 사용자 성과가 아니다. A-D04를 뺀 A11행은 유지8·교체2·보류1, 즉 대조상 행동 일치10과 보류1이다. B03을 뺀 B5행은 유지3·교체1·보류1이다. **B04평가불가와 B05중복을 제외한 독립 평가 가능 B소비자는4개이며, 여기에 사전배경 B03까지 제외하면3개(B01/B02/B06)**다. 서로 다른 제외 축을 같은 분모로 표현하지 않는다.

단순한 정보로 충분했던 경우도 과장하지 않는다. A-R04/B04는 적은 정보에서 보류할 수 있었지만 보류를 정답 분자로 올리지 않았다. A-D01/03/05·R01/02의 의미상 유지에는 목적과 현재 본문만으로 충분할 수 있다는 사후 분석이 가능하나, 실제 L1/L2는 모두 보류였으므로 이를 그 보기의 성공으로 다시 쓰지 않는다. 이력을 더해도 A-R04의 실제 IDE/Pandoc 조건, B04의 역사 HTML, 공통 build/reader 시계는 해결되지 않았다.

## 완료된 검사와 원격 영수증의 범위

| 실제 영수증 | 대상·입력·결과 | 검사의 한계 |
|---|---|---|
| [A 원격 봉인 재독](evidence/a-seal-remote.json) | commit168d90b8519bcb4f673acc659bbaae895f79fca5, references blob e38024668d0b0321056831dad761f421c28bd792; 이후 IA07에서 A접두 동일성 재검 | 당시 A입력 봉인 영수증이며 최종 RESULT/HANDOFF의 원격 재독은 아니다. |
| [B 원격 봉인 재독](collectors/b/remote-seal-receipt.json) | commitffbce62e4c01459ebbfb006a5d6c67e425ed7c17, B6 봉인 | 소비자 질의 이전 사건 봉인 범위다. |
| [R followup verification](collectors/cran/followup/verification.json) | 실제 로컬 `verify_followup.py`,2026-11-22T07:40:31Z, HEADffbce62e…+입력해시,18/18·exit0; archive78, 존재멤버121/부재35,DESCRIPTION78, excerpt95 대조 | R 수집자의 자기 검산. package 설치·렌더링·사용자 실행 검사가 아니다. |
| [offline self-check](collectors/offline/followup/self-check-receipt.json) | 실제 로컬 `check_followup.py`, A봉인168d90b…+followup 입력해시,exit0; PG관련 fragment40·SQLite8,12.18→19 href만 변경, 중복·29일 날짜 산술 | 동일 수집자 검사. SQLite 미열람46판이나 실제 클릭을 검증하지 않는다. |
| [별도 root raw 감사](collectors/offline/audit-root.json)·[설명](collectors/offline/AUDIT_ROOT.md) | Python19+httr8 archive,HTML46,DESCRIPTION8; 입력13파일 SHA와 대상 HEAD; 바이트/해시/산술 오류0, 시계·reader 해상도 보강3 | 별도 내부 비맹검 판독. B03 `.deb`는 이 감사에서 독립 재독하지 않았다. |
| [root fresh primary reread](evidence/primary-reread.json) | 실제 public GET4건: Python3.8.14/15 경계, R04조건부 원문, D01 유지 목적;07:58:20Z 완료,all_pass·exit0. 대상HEAD와 working-tree data SHA 기록 | root 자신의 재검이다. 4건으로 전 원문이나 최종 커밋을 검증했다고 주장하지 않는다. |
| [통합 감사](collectors/cran/integration-audit.json) |2026-11-22T08:03:38Z, HEADffbce62e…+6입력해시;395 metadata/75선택 원문·A접두·분모·보조산술·조인27/27·exit0 | R 수집자/B 카드 판독자가 root 집계를 재검한 내부 감사. 새 외부 원문0. 첫 실행은 schema KeyError로exit1,표준필드에 맞춘 재실행이exit0임을 보존했다. |

통합 감사는 최소수 선택 그룹과 실제 동일본문 그룹의 혼합, 보조7행 source/event 조인, B6 최소 목적 필드, B02출판 시계 누락을 발견한 뒤 수정된 입력을 다시 검사했다. 결과가 처음부터 완전했던 것으로 설명하지 않는다. [postseal-amendments](evidence/postseal-amendments.jsonl)는 Python 독자 목적과 분 단위 nominal 시계 보강을 기록하며 strict 분자와 원 A바이트는 변하지 않았다.

## 미실시·미확인 검사와 WITH_GAPS 사유

아래는 결과 파일을 커밋하기 전의 상태다. root가 실제 실행한 pre-result 검사와 아직 뒤 단계인 fixed-result 원격 재독을 구분했다. 추가 실행은 마지막 HANDOFF에 대상 SHA·입력·종료 코드로 기록한다.

| 남은 항목 | 현재 상태 | 다음 첫 행동 또는 자료 |
|---|---|---|
| 작업 세션 `check --fetch`, 공통 gate | [pre-result session](evidence/checks/session-pre-result-execution.json)은6ac3d4d HEAD+작업트리에서 exit0; [공통 gate](evidence/checks/common-retry-execution.json)는 같은 고정SHA의 공식원격 freshclone에서5/5 exit0. 첫 localclone은 누락Gitobject로backup실패했고 첫영수증도보존 | 후기RESULT commit은아직이검사의대상이아님. 결과고정뒤 session check와문서검산·원격재독을HANDOFF에추가 |
| 결과·자체점검·수용판정의 원격 고정 SHA 재독과 마지막 HANDOFF 커밋 | A/B봉인 및④6ac3d4d counts/comparisons 고정재독은완료. RESULT·SELF_CHECK·수용을먼저커밋한뒤실행할원격재독은아직완료범위아님 | root가 결과 커밋을 원격에서 재독하고 그 뒤 별도 HANDOFF 커밋 작성 |
| SQLite 사이46판 | archive 내용 미열람이며 멤버 부재로 세지 않음 | 첫 미열람 `sqlite-doc-3310100.zip`의 about/aff_short 멤버부터 같은 범위로 재개 |
| B04 역사 HTML | sdist/README는 읽었으나2.2.0/2.2.1 렌더링 배포 HTML 없음 | 날짜 있는 SphinxSitemap2.2.0 또는2.2.1 HTML artifact1개 확보 |
| 실제 설치·부팅·Pandoc/IDE 호환·브라우저 클릭 | 실행하지 않음. 링크 문서의 존재·목적 적합성만 조사 | A-R04의 고정 IDE/Pandoc 배포판과 rmarkdown2.1 입력을 먼저 정하고 별도 실행 증거 확보 |
| 실제 시행/첫 공개 시계·같은 매체 독자 관측 | 다수 미확인; nominal/제품 release day/metadata로 채우지 않음 | 사건별 chains의 `next_material`; 예: RFC4180 개별 redirect 배포 영수증, exact Python doc archive 공개 기록, 해당 offline판을 명시한 독자 보고 |
| 절차·보기의 한계 | R의 봉인 전 순서 정정, B01 범위 밖 실패 후보, A-D04/B03 판독 노출, L3현재 증거와 이력 동시 추가 | 편차를 유지해 수용조건의 false를 보존. 다음 실험에서는 현재 증거를 고정한 뒤 이력만 달리하고 사전노출을 배제 |

원문 최소수와 A 표본 목표는 충족했지만 위 연구·절차 공백은 남아 있다. 따라서 WITH_GAPS로 인계한다. 엄격 적격 양성0은 이 표본에서 확인한 결과이며, 양성 수를 늘리기 위한 표본 교체나 후대 정보의 소급 삽입을 종료 조건으로 삼지 않는다.

## 결과 편집 후 추가 정정

별도 내부 RESULT 감사에서 MDN 경로변경 인용(R-U17), redirect가 추가한 Posit 도착anchor, 과거·현재 박물관 작품명 표기, B04 독립 canonical GET과 원 요청의 final URL 혼합을 바로잡았다. B04 원 요청은302→오류429이며 canonical200은별도요청이다. 현재원장에는 final_url=null과별도canonical필드를둔다. A봉인·가림카드·최종판정·분모는변하지않았다. 이전통합감사의입력hash와후기정정원장hash를구분하고새 deliverable검사에서고정한다.

## 결과 문서 기계 검산 영수증

[deliverable-check.json](evidence/deliverable-check.json)은 후기정정뒤의원장·표·로컬링크·Git허용경로를실제로검사한입력hash와exit를보존한다. 첫실행은자기영수증파일이아직없어서해당링크1건이실패했으며 [첫실행](evidence/deliverable-check-first-run.json)도남겼다. 초안검사기자체의가정오류와수정은 [draft](evidence/deliverable-check-draft.json)의 earlier_attempts에구분한다. 이검사는원문을새로읽은의미검증이아니며,원문판독·통합검산과별도로보고한다.
