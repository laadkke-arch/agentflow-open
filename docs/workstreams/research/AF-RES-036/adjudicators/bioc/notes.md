# AF-RES-036 Bioconductor 별도 문맥 기준판정

완료 UTC: 2026-11-22T16:29:17.544636+00:00

## 범위와 판정

배정된 원 인용 B 6개를 고정하여 **R01 REPLACE, R02–R06 KEEP**으로 판정했다. HOLD는 없다. 원 링크 6개를 모두 직접 GET했다. R01은 HTTP→HTTPS 301 뒤 404 및 Page Not Found 본문, 나머지 5개는 각각의 패키지 랜딩으로 302 뒤 200을 관측했다. HTTP 코드만으로 판정하지 않고 실제 목적 본문·배포 소스까지 읽었다.

제공된 adjudicator-instructions.md, bioc/input.json, 허용된 fetchlib.py, PDF 읽기 지침, 자기 폴더 생성물과 직접 취득한 공개 원문만 사용했다. 다른 카드·수집결과·판독결정·요약·기준 파일은 열지 않았다. 동일 모델계열의 별도 문맥이며 인간·다른 모델의 독립검증은 아니다.

봉인 SHA 5fbde38a04613fbd6f057fd562bd173b7193f2c9는 작업 배정에서 받은 문맥이다. 그 봉인에 담긴 판독결정 파일을 읽거나 독립 확인한 것은 아니다. input.json의 base citation commit과 배포 URL·해시를 사용했다. 다른 표본으로 바꾸지 않았다.

## 판단의 핵심

- R01: 대체는 `https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2`다. 직접 받은 HTML에서 정확한 id와 FASTQ/Salmon/tximeta/summarizeToGene 절을 확인했다. 현재 release workflow도 읽었지만 원 문맥을 보존하는 3.11판을 택했다. 원 인용이 특정 target 판을 요구한다고 꾸미지는 않았다.
- R02·R04·R05·R06: 원 URL은 3.11판을 명시한다. 오래됐다는 이유로 최신판으로 교체하지 않았다. 랜딩의 patch 버전은 각각 IRanges 2.22.2, DESeq2 1.28.1, SingleCellExperiment 1.10.1, scater 1.16.2이다. 원 소비 문서의 버전을 링크 대상 버전으로 혼동하지 않았다. 연결된 공식 본문에서 infrastructure, DESeqDataSet/ranges, SCE/scater 관계를 확인했다.
- R03: 원 인용은 setValidity2의 제공 패키지를 연결하고 원 소비 문서 안에 예제를 이미 제공한다. 한국어 목적을 별도 standalone tutorial이 필수라는 한정으로 확대하지 않았다. 현재 landing이 연결하는 source tarball에서 함수와 export를 읽었고 3.11 source도 대조했다. 확인한 함수 정의 블록은 두 버전에서 SHA-256 `64d66cc12bca0968bb5307d11e54a6b466a18c6f0e5f142885d4e204b2d16af1`로 동일하다. 전체 패키지 실행 호환성을 확인한 것은 아니다.

## 실제 찾은 한계와 반례

- 현재 S4Vectors PDF는 200이지만 setValidity2를 p.70의 generic internal-helpers 항목으로 보내고 전용 signature/usage를 제공하지 않는다. quick overview도 setValidity 예제이며 setValidity2 문자열은 없다. 이 두 응답만으로 기능을 확인했다고 하지 않았고 소스 구현을 추가 확인했다.
- rnaseqGene 3.11 standalone HTML의 해시 `fcca99d06b540a81c4f8584232d482d9e55b29efcc1783d98e6ac63d08ff9814`와 1.12.0 tar member의 해시 `8f8cb5f18bce644aca30118247202157a6dbd3c429e8a93f450ec8031527e5a8`는 다르다. 필요한 문장·명령·앵커는 양쪽에 있으나 전체 바이트 동일성을 주장하지 않는다.
- S4Vectors 0.50.3 tar DESCRIPTION의 Date/Publication은 2026-09-16, PDF metadata는 2026-11-11이고 cover는 2026-11-12다. 차이를 숨기거나 임의로 하나의 발행일로 합치지 않았다.
- 요구 anchor가 새 후보에서 사라지는 사건은 이번 확인 범위에서 찾지 못했다. 원 6개 href에는 fragment가 없고, 실제 사용하는 추가 HTML anchors는 반환 본문에서 id를 확인했다. 임의의 없는 anchor를 만들어 반례로 세지 않았다.

## 출처와 측정의 제한

모두 Bioconductor 발행자 계열이다. 원 소비 문서, 대상 패키지 본문, 배포 소스와 릴리스 공지는 서로 다른 원문/표현이지만 독립 발행자 출처가 아니다. 같은 문서의 HTML·tar 멤버와 추가 절은 별도 독립 근거로 세지 않는다.

직접 GET 25회, 수신 body 합계 28,200,415 bytes를 기록했다. 이는 애플리케이션이 받은 body 크기이며 wire bytes/네트워크 전체 비용은 미확인이다. 검색 2회는 별도 discovery 기록이고 source count=false이다. 초기 허용 측정유틸 경로 조회 실패와 bs4 미설치에 따른 로컬 파서 import 실패 2건도 별도 기록했다. 올바른 허용 경로와 표준 라이브러리로 해결했으며 설치는 하지 않았다. 직접 읽은 source record 25개는 오류 응답·동일 문서의 표현·중복 배포원을 포함하므로 새 고유 출처 수나 독립 근거 수가 아니다. root가 URL·source/member hash와 문서 가족별로 중복군을 합쳐야 한다.

원 소비 tarball 5개의 hash와 HTML member 6개의 hash가 input.json과 전부 일치했다. 날짜는 문서 표시일, 수정/컴파일일, package Date/Publication, 릴리스 공지일, HTTP Last-Modified, 실제 조회 UTC를 구분했다. landing의 확인되지 않은 발행일은 빈 published_dates로 남겼다. DESeq2의 숫자 표시일 05/12/2020은 월/일 순서를 확정하지 않았다. 현재 HTTP 관측을 2020년 당시 상태로 소급하지 않았다.

R/Bioconductor 소프트웨어 설치·실행, 로그인, 계정 변경, 유료 자원, 실제 독자 클릭/사용성 검사는 하지 않았다. PDF는 pdftotext 추출과 관련 페이지 시각 확인을 병행했다. S4Vectors p.70 및 IRanges pp.1–2를 시각적으로 확인했다.

## 재현과 원격 보존

`sources.jsonl`의 exact_excerpt는 원 수신 body 또는 명시된 tar member / `pdftotext -layout` UTF-8 결과의 정확한 부분이다. 각각 source hash, member/derived hash, 0-based byte_start와 exclusive byte_end, 1-based line 범위, excerpt hash를 기록했다. tar 파일은 source URL로 취득해 SHA-256을 먼저 확인하고 명시된 member를 추출한다. PDF 발췌는 명시된 pdftotext 명령을 사용하고 derived hash가 다른 경우 발췌를 원 PDF 페이지와 다시 대조한다. HTTP fragment의 검증은 반환 HTML의 정확한 id 확인이며 서버 fragment 요청이나 브라우저 클릭 결과가 아니다.

원문 전체·tarball·PDF·PNG·임시 생성 스크립트는 commit whitelist에서 제외했다. 커밋 대상은 판정·출처 발췌·시도 로그·이 메모·whitelist 5개뿐이다. 커밋과 공통 파일 수정은 root가 수행한다.
