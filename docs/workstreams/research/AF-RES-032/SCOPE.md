# AF-RES-032 사전 조사 계약

## 시작과 책임
- 시작 기준: chore/workspace-foundation@172c6bc37bdf91b91c86b9b3be29cb5b44fa4971; 작업 branch work/research-af-res-032.
- 의존: AF-RES-027@42dadeeb632301108e1fc83ba393db971ec28b15의 HANDOFF, references, intervals, RESULT Q4–Q8.
- 배정 worker_kind web-pro. 실제 환경: ChatGPT Work의 공유 Linux 셸·GitHub connector·웹 검색. 세션 지시에서 표시된 모델 GPT-6 Astra Pro; 계정 UI 모델을 별도로 확인한 것은 아님.
- 조사 개시 2026-11-22T07:05Z, UTC로 원문별 확인시각 기록. 역사 표집창 2020-01-01–2024-12-31, 관측 종료는 실제 마지막 수집시각. 365일 이상 후속창.
- root가 봉인·통합·커밋·인계를 맡고 보조 판독자는 서로 다른 수집 파일만 작성. 내부 병렬 조사이며 외부 사람의 독립 검토가 아님.

## A: 결말을 열기 전 소비자 배포물부터 선택
두 유통 경로를 고정한다. 경로 D는 발행자가 직접 배포한 버전별 오프라인 HTML 문서 archive, 경로 R은 CRAN의 버전별 package archive 속 이미 빌드된 HTML vignette/도움말이다. 각 경로 6참조, 서로 다른 HTML 문서 12개, 총6프로젝트 이상, 프로젝트당2개 이하. 현재 편집 가능한 web만으로는 대체하지 않는다.

D의 원장 우선순위: Python 공식 docs/ftp, PostgreSQL 공식 ftp/pub/doc, SQLite 공식 연도별 sqlite-doc 다운로드. 각 프로젝트에서 2020년에 출판한 가장 이른 접근 가능한 안정판(2020판 없음은 2021→2024), HTML member 경로 사전순·문서 DOM 순으로 적격 외부 href를 찾는다. 기준 날짜/배포처/문서 경로를 frame에 남긴다. 프로젝트당 서로 다른 문서2개. 부족·archive 형식 불일치·접근불가이면 같은 유형의 GNU Octave 공식 doc archive → GNU GSL 공식 HTML archive → R 공식 HTML manual archive 순서로 이동. 이름만으로 HTML 보존을 인정하지 않는다.

R의 공개 원장은 CRAN Archive; 후보 프로젝트 순서는 DBI, curl, data.table, httr, jsonlite, knitr, rmarkdown, xml2, readr, dplyr다. 각 프로젝트의 2020년 첫 공개 archive를 날짜순으로 시도하고, 없으면 2021→2024. HTML은 inst/doc 또는 배포 도움말 member를 실제로 열며, 각 프로젝트 첫 두 적격 HTML 문서까지 선발한다. 6참조가 차면 멈춘다. 공식 CRAN 접속 실패 시 cloud.r-project.org → cran.rstudio.com → cran.ma.imperial.ac.uk 순으로 같은 원장의 미러를 시도한다. 미러는 독립 원문이 아니고 원주소·미러 주소·해시를 모두 기록한다.

공통 적격성: 본문이 왜 링크를 클릭할지 읽을 수 있어야 한다. nav/footer/theme/license boilerplate, 그림/css/js, 예시 가상 URI, 패키지명만 있고 URL 없는 항목, 같은 문서의 다른 링크는 제외한다. 처음 만난 적격 본문 링크를 택하되 링크 문자열 자체가 이전 AF-RES-027의 package/catalog 사건을 재추적하면 제외한다. 소프트웨어 공식 일반 설명/표준/판별 API/원 논문 모두 허용한다. 동일 manuscript가 다른 이름으로 있으면 중복 제외. 선택·제외·시도 실패를 frame과 attempts에 보존한다. 후속 변화가 없는 참조도 교체하지 않는다.

A 전체12개(부족시 실제 확보수와 거짓 수용조건)를 references.jsonl로 원격 커밋하고 재독하기 전에는 해당 목적지의 현재 내용·후속 소비자판·변경 결과를 열지 않는다. archive 목록·원 배포물 자체만 허용. 원 raw_href, base_url, resolved_url, fragment, link_text, 앞뒤 문장, 클릭 목적, 최소 성공조건, 모르는 의도, archive/member SHA256을 보존한다. 모든 상대경로 해소는 urllib.parse.urljoin의 문서 기준 URL이며 archive 내 상대 파일이 외부 링크로 오인되지 않게 한다. 사후 보강은 원봉인을 바꾸지 않고 amendments로 남긴다.

## B: 상류 사건 우선 보조6
A 봉인 뒤 공식 문서 이관/정정 공지에서 2020–2024 사건6개를 고른다. 미리 정한 탐색 쿼리 묶음은 official documentation moved new domain announcement 2020, 2021, 2022, 2023, 2024 및 official documentation broken links migration announcement다. 검색 결과 중 공식 발행자 원 공지·변경 시행을 직접 확인한 사건을 날짜 오름차순, 같은 날짜는 발행자·URL순으로 목록화한 뒤 첫6개를 고정한다. 후보/부적격도 남긴다. A 선택 결과를 B 성공 선별에 사용하지 않는다. 소비자 검색 시작 전에 B 목록을 별도 봉인한다.
사건마다 소비자 탐색은 질의 최대3개, 후보 출판 문서 최대5개. 쿼리·열람·실패를 실제로 기록한다. 동일 consumer+purpose+upstream_event_key로 A 중복을 표시한다. 미발견·이미 새 URI·옛판 유지·다른 목적 대체도 결과다. B를 A 분자에 합치지 않는다.

## 시계와 판정
upstream_effective, consumer_source_edit, merge, build, consumer_publication, reader_report, observed_at을 별도 필드로 둔다. 날짜 정밀도 day는 [그날00:00Z, 다음날00:00Z)이며 시차 미상은 UTC로 가장하지 않는다. mtime/현재 미러수집/현재 HTTP 상태를 역사 사건일로 쓰지 않는다.
source diff만은 배포 증거가 아니다. 같은 문서·같은 목적을 추적하고 실제 후속 archive member를 읽는다. 마지막 관측 옛판과 처음 관측 새판을 구별하고 그 사이 전체 원장과 모든 판의 bytes를 읽은 경우만 ‘최초’라 쓴다. 완전 목록과 미검사판 수를 같이 기록한다. 태그 source와 실제 빌드 HTML을 섞지 않는다.
엄격 지연은 동일 목적·동일 노출 매체의 상류 시행과 소비자 공개 수정이 근거로 고정된 쌍만. source→release 별도 보조량. 정확한 쌍 또는 출처 있는 상하한만 산술. 시작 미상은 미확인이지 우측검열이 아니다. 관측창 끝까지 같은 사건을 추적했을 때만 우측검열. reader가 읽었다는 당사자 원문 없는 경우 출판 접근 가능만 주장.
판정: 유지(목적에 맞는 원판/현 링크), 교체(동일 목적에 맞는 대체의 근거), 보류(목적/시간/내용 불명). HTTP status / final URL / fragment 존재 / 내용의 목적 충족을 분리한다. 원문을 보존하면서 현 경로를 병기할 수 있으며 역사적 인용을 지우지 않는다.

## 다른 분야와 세 보기
공공 통계의 고정 연도표·개정 공표, 박물관/기록관의 전시 당시 카탈로그·현재 개체 기록에서 각1쌍. 실제 인용 목적을 공개 본문에서 읽고 최소4개 고유 원문. AF-RES-023 카탈로그/ROR 및027의 PLOS·LC 사례 재사용 제외. 소프트웨어 전파분모에 합치지 않음.
L1 원URL만, L2 URL+링크텍스트/용도/소비자판, L3 배포물/앵커/이력을 추가한다. 가능한 경우 원문을 수집하지 않은 별도 내부 판독자에게 각 입력을 순차 제공해 가림판정을 보존하고 그 뒤 대조한다. 이력이 먼저 알려진 동일 작업자의 사후 ablation은 맹검으로 부르지 않고 retrospective로 표시한다. 정답/오교체/잘못유지/보류는 원문 대조 기준판정과 비교하며 보류를 정답으로 부풀리지 않는다. B 소비자 미발견은 평가불가로 분리한다. page read·빈 날짜·query 횟수는 실제 기록량이며 사람 시간/비용을 추정하지 않는다.

## 원문/수용/종료
고유 직접 원문 최소30 = A문서12 + 상류8 + 소비자후속6 + 타분야4. 동일 원고의 API/HTML/미러/동일본문 판은 duplicate_group로 묶어 한 번만. 페이지 수·원문 수·사건 수·행 수는 별도. 접근 실패/검색 snippet은 attempts만이고 최소수 제외.
SCOPE→A봉인→상류/B→소비자/타분야→결과·검산→원격 재독→HANDOFF 순서로 별도 커밋. 결과 수용조건의 거짓은 숨기지 않는다. 양성0은 실패한 연구가 아니며 부족한 표본/검사는 REVIEW_READY_WITH_GAPS로 인계. 최종 RESULT와 HANDOFF 끝 약점표 정확히3행. 코드 구현·실제 소프트웨어 실행 성공·독자 피해는 추측하지 않는다.

