# AF-RES-036 사전 범위·표집·판독 규칙

## 고정 입력과 권한

- 계획 기준: chore/workspace-foundation@d3fbd08d44fd0e2915d1f766721a81845bacc213.
- 실제 시작 및 원격 확인: 9668632e915d508e93ddfdc5e8fe4b88bcbfec56, 2026-11-22 15:40–15:44 UTC (한국 2026-11-23).
- 의존: AF-RES-023@a9178ca95979564fd8801559d90d15db4ddac91b, AF-RES-032@b4dcf0a1ca3f2066629869ac1a9347ad2f5717df. 최종 판정은 교정 자료이며 새 실험의 정답이 아니다.
- 실제 환경: ChatGPT Work의 공유 Linux shell, GitHub 연결 도구, 웹 검색. 세션에 선언된 모델 GPT-6 Astra Pro; 별도 계정 UI의 모델/추론 강도는 관측하지 않았다.
- 허용: 이 폴더 아래의 연구·원장·작은 수집/검산 스크립트, 지정 작업 브랜치 커밋·push. 공통 문서·dot-control.json·제품 코드·main은 수정하지 않는다.

## 표집 봉인

현재 목적지의 상태 또는 후속 정정 결과를 조회하기 전에 이 규칙을 커밋한다. 새 표본은 GNU 유통 G 6참조와 Bioconductor 유통 R 6참조, 서로 다른 출판 HTML 문서 12개, 전체 최소 6프로젝트, 프로젝트당 최대 2문서다. 분할 HTML의 장·절을 다른 출판 문서로 중복 산입하지 않는다. 원 소비자의 최소 목적은 실제 문장으로만 기록한다.

원 배포 후보 기간은 2020-01-01–2022-12-31이다. 각 프로젝트에서 이 기간의 가장 이른 안정판을 먼저 취득한다. 빌드 HTML이 없으면 같은 프로젝트의 다음 날짜 안정판을 최대 2개 더 조사한다. 날짜는 배포 목록/릴리스 문서의 날짜이며 archive member mtime으로 출판일을 추정하지 않는다. 실패·HTML 없음은 frame/attempts에 기록한다. 과거 HTML을 얻지 못하면 아래 고정 순서의 다음 공식 유통으로 옮긴다. 결과에 맞춰 빠진 목적 층을 채우지 않는다.

### G 경로

GNU 공식 버전 tarball의 빌드 HTML을 우선한다. 프로젝트 순서: bash, coreutils, findutils, gawk, make, tar, grep, sed, gettext, gcc, binutils, gdb. 프로젝트마다 독립 매뉴얼 최대 2개를 HTML 제목/멤버 경로 사전순으로 본다. 현재 웹 매뉴얼에서 옛 배포를 추정하지 않는다. tarball에 빌드 HTML이 없으면 해당 도구의 Debian 공식 배포 doc 패키지(archive.debian.org → deb.debian.org의 버전이 붙은 .deb 순), 이어 발행자가 보존하는 버전 경로의 HTML 매뉴얼을 시도한다. 이때 원 배포가 GNU 직접인지 Debian 재배포인지 구분한다. 위 후보의 여섯 문서가 채워지면 멈춘다. 소스 texi를 새로 빌드한 결과는 과거 배포 HTML에 산입하지 않는다.

### R 경로

Bioconductor의 3.11(2020), 3.12(2020), 3.13(2021), 3.14(2021), 3.15(2022), 3.16(2022) 순서로 실제 package tarball의 inst/doc/*.html 또는 릴리스별 배포 vignette HTML을 취득한다. 프로젝트 우선 순서: DESeq2, edgeR, limma, Biostrings, GenomicRanges, SummarizedExperiment, S4Vectors, BiocParallel, Biobase, AnnotationDbi, SingleCellExperiment, scater. 패키지당 제목/멤버 경로 사전순의 서로 다른 vignette 최대 2개. 최소 3프로젝트를 보장하기 위해 첫 순회는 프로젝트당 첫 문서 1개만 취하고, 여섯 개가 부족하면 같은 프로젝트 순서의 두 번째 문서를 취한다. 과거 HTML이 없는 프로젝트는 다음으로 이동한다. 모두 불충분하면 같은 기간 CRAN 공식 Archive의 실제 inst/doc HTML을 data.table, ggplot2, tidyr, purrr 순서로 시도한다. 의존032에 등장한 knitr/dplyr/rmarkdown/httr/PycURL/SphinxSitemap/StarlingX는 제외한다.

### 문서 안 링크 선정

내부 nav·목차·저작권/라이선스·mail·추적 링크·단순 기관/저자 홈페이지·일반 citation DOI만 있는 서지는 제외한다. 본문이 외부 기술 문서·도구·데이터·특정 규칙을 읽도록 설명하는 첫 적격 href를 DOM 순서로 택한다. 같은 목적 링크 중복은 첫 것으로 합친다. 아직 목적지를 열지 않고 href 원문, anchor text, 주변 문단, 문서/배포판/멤버, SHA256, 원문 위치를 고정한다. 읽을 수 있는 목적 문장이 없으면 제외한다. 선택 당시 발견한 판/대상을 그대로 기록하고 현재 실용/특정 판 재현/애매함으로 층화한다. 오래됐다는 사실만으로 역사 재현층으로 바꾸지 않는다. 032 전체 A/B 소비자-목적 및 기존 통계/박물관·023 사건은 review/exclusions.json의 교정 제외군이다. 새 후보가 같으면 상태 열람 전 제외한다.

## 카드와 누출 방지

B는 인용문서 제목·판·원 href·link text·문맥(최대 1200 Unicode 문자)·명시 근거가 있는 최소 목적을 담는다. N은 한 확인창의 실제 GET 상태·redirect·최종 URL·anchor 존재와 목적에 필요한 현 본문 발췌(최대 1600문자)다. HTTP200만으로 적격이라고 하지 않는다. H는 그 확인창 이전의 발행자가 식별한 판·원판/후속판의 관련 문장·공식 이전/정정 공지에서 최대 1600문자다. 사건일과 fetch UTC는 따로 적는다. H에는 오늘 GET 상태·수집자 권고·정답·결정 결과를 넣지 않는다. N에 별도 옛판을 인위적으로 보태지 않는다. 현 본문 자체가 이력을 말하면 overlap_history=true로 기록하고 별도 민감도에서 뺀다.

절단 규칙: 해당 anchor가 있으면 그 heading에서 목적 문장까지(앞뒤 문장 포함); 없으면 일치하는 본문 용어의 최초 절; 그래도 없으면 title+본문 첫 절과 부재 범위. 임의 유리한 발췌 교체 금지. HTML script/style/nav를 제거한 UTF-8 텍스트의 시작/끝 offset과 원 member hash, 카드 bytes SHA256을 보존한다. 길이 초과는 문장 끝에서 자르고 truncated=true. 빈 증거도 빈 문자열과 실패 사유를 보존한다. 재구성 도구와 정확한 발췌 bytes를 둔다.

## 판독과 기준판정

보기 B, BN, BH, BNH의 네 입력에서 B/N/H 문자열을 단 한 번 만들고 그대로 조합한다. BN과 BNH의 N bytes·순서·길이, BH와 BNH의 H bytes가 같아야 한다. 순서 seed=360032, 12사례의 case order를 shuffle하고 각 사례 view order는 Latin rotation [B,BN,BH,BNH], [BN,BH,BNH,B], [BH,BNH,B,BN], [BNH,B,BN,BH]를 순환한다. 48칸 전체를 보존한다.

사전 판독 규칙: (1) 목적/대상/필수 판이 명확하지 않으면 보류; (2) 제공 증거가 현재 원 href의 필요한 본문 접근과 목적 적합을 보여주면 유지; (3) 제공 증거가 같은 목적에 어긋남을 보여주고 같은 목적의 대체 필요를 입증하면 교체(대체 URI 확인 여부는 별도); (4) H만으로 현재 접근을 보증하지 않으며 상태 단서가 없는 B/BH는 보류할 수 있음; (5) 과거 판과 다른 새 내용이라고 무조건 교체하지 않음. 판단 이유와 근거절을 먼저 기록하고 정답으로 맞추어 수정하지 않는다.

이번 수집자가 판독하는 48칸은 동일 작성자의 사전 규칙 적용 민감도다. 본문을 수집한 노출을 숨기지 않으며 엄격 미노출 분모=0을 허용한다. 별도 문맥 판독자가 들어오더라도 받은 자료/선행 노출을 공개하고 사람 시험이라고 부르지 않는다. 독립 자료 검토와 독립 미노출 의사결정을 구분한다. 네 보기 결정의 커밋 이후에만 별도 기준판정(adjudication)을 작성한다. 실제 도착 절·발행자 날짜 문서·보존 배포물과 대조하되 같은 발췌만 있으면 dependent_same_source로 표시한다. 판정 불가를 맞음에 넣지 않는다.

## 비용·재조회와 보조 분야

각 요청 시 UTC·실제 경과 seconds·HTTP chain·response body bytes·저장 bytes·실패·재시도를 기록한다. body bytes는 HTTP 압축을 해제한 응답 바이트이며 network wire bytes로 부르지 않는다. archive bytes/추출 member bytes/카드 bytes를 구분한다. 파일 공유의 물리 fetch수와 논리 참조수를 따로 센다. 카드 판독 token/사람 노동/실서비스 운영비는 측정하지 않는다.

2차 재조회 예산은 참조당 현재 본문 1 GET + 필요 시 과거 배포 1 GET, 최대 2 GET, 순차 timeout 각 30초다. C1은 B만 보관하고 C2는 B+H+provenance를 보관한다고 두되 현재 확인 의무는 같다. 실제 재생이 가능하면 구분 기록하고, 다른 URI 복구/사람 판독 비용은 모의 가정으로만 적는다. C0의 발견 검색비는 미측정이다.

Q7의 지리·서지 조사는 소프트웨어 표본에서 분리한다. 지리 후보 순서: ONS 2021→2023 local-authority boundary/code changes와 그 코드/판을 명시한 공식 통계 보고서; 안 되면 US Census Connecticut planning regions와 county 기반 원 통계. 서지 후보 순서: Library of Congress/국립도서관의 edition/translation 식별·정정 기록과 해당 판·번역을 명시한 공개 참고문헌; 안 되면 BnF 또는 DNB. 실제 정정 사슬이 없으면 원판 구별의 사례와 정정의 미확인을 분리한다. 각 쌍은 발행자+실제 소비자 원문을 직접 읽는다.

## 원문 최소수와 종료

고유 직접 원문 최소30, 원 배포 소비자12, 현 목적지 적격본문≥8, 독립 과거/공식 정정/보존 원자료≥6, 보조 두 분야 각2. 동일 원고/미러/과거현재 동일bytes는 한 duplicate_group. 검색요약·목록 발견만·자체 표는 산입하지 않는다. 모든12 목적지를 시도한다. 총수와 범주수를 각각 재계산한다. 결과가 음성 또는 엄격 미노출 분모0이어도 그대로 남기고 부족한 최소수를 성공으로 꾸미지 않는다.

묶음 순서: 1 이 규칙·manifest, 2 목적지 열람 전 12개의 B 봉인, 3 N/H 관측·sources 및 결정 봉인(기준판정 전), 4 기준/집계/RESULT/SELF_CHECK/수용 근거, 5 고정 결과의 원격 재독·계약 검사 뒤 HANDOFF. 중간 실패와 규칙 편차는 이전커밋을 보존한 errata에 적는다.
