# Bioconductor N/H 수집 인계

B 원격 봉인 `bd3c17ef2f989b3d9e0566405d82357fc17f47bb` 이후 현재 조회를 시작했다. evidence-components.jsonl에 R01–R06 각각 N/H의 정확한 문자열, SHA256, byte/문자 길이, 원문 위치·절·판·조회 UTC를 기록했다. 12개 component는 모두 1600문자 이내다. components/*.txt가 판독 입력의 정확한 bytes이며 원장 metadata는 그와 분리했다. 판정·정답·교체 권고는 작성하지 않았다.

## 직접 관측

| 참조 | 원 href 관측 | 필요 절을 읽은 경로 | H |
| --- | --- | --- | --- |
| R01 | HTTP→HTTPS301 뒤404, Page Not Found 본문 | 원 href의 오류 본문. 대체 목적지는 아직 판정/검증하지 않음 | rnaseqGene1.12.0의 실제 배포 HTML, Abstract 및 FASTQ→Salmon→gene count 절을 읽음. 카드에는 Abstract |
| R02 | 302→Bioconductor3.11 IRanges package page200 | integer ranges/S4 class 본문 | IRanges2.22.0의 IRanges-class.Rd 설명 |
| R03 | 302→현재release3.23 S4Vectors page200 | 공식 PDF index가 setValidity2를 internals70쪽으로 연결하지만 그 절은 포괄적 helper 설명뿐. package page가 연결한 현재0.50.3 source tar의 R/S4-utils.R 함수 정의를 추가 확인 | 0.26.0 R/S4-utils.R의 같은 함수 정의 |
| R04 | 302→3.11 DESeq2 page200 | 연결된1.28.1 PDF9쪽 subclass 설명과10쪽 rowRanges 인자. 두 쪽을 렌더링해 직접 대조 | 1.28.0 배포의 DESeqDataSet.Rd 설명 |
| R05 | 302→3.11 SCE page200 | 현재 제공된1.10.1 intro vignette의 Motivation 실제 본문 | 1.10.0의 SCE class Rd 설명 |
| R06 | 302→3.11 scater page200 | 도구 설명과 Depends SingleCellExperiment 절 | 1.16.0 plotColData.Rd에서 SCE object를 받는 설명 |

현재 열리는 3.11 본문을 최신판이라고 부르지 않는다. 목적지 page의 package 이름만으로 R03/R04 필요 기능을 확인했다고 보고하지 않았으며 위 추가 요청/정확 절을 분리했다. R01의 실패는 실제404이며 fallback 검색 요약으로 채우지 않았다. Q4의 대체 URI 검증은 48판정 봉인 이후에 가능하다.

## 중복·노출·분리의 한계

- R04 finalURL와 HTML bytes는 원 배포 찾기에 먼저 읽은 R-L02와 정확히 같다. pre_exposed_current_target=true를 유지했다.
- N3와 H3의 setValidity2 함수 발췌는 bytes가 완전히 같다. 두 파일 전체의 hash는 다르지만 이번 기능 근거는 같은 원문군으로 보수적으로 합쳤다. H3를 새 독립 이력 원문 최소수에 더하지 않는다.
- N4 PDF와 H4 Rd는 동일 DESeqDataSet reference entry의 다른 판/표현이다. 같은 주장과 정의가 반복되므로 H4는 새 고유 원문 수에서 빼고 동일 원고군으로 묶었다.
- N5의 현재 SCE intro Motivation은 B6의 해당 문단과 bytes가 같다. 전체 HTML은1.10.0/1.10.1 등으로 달라져도 같은 vignette 원고군으로 보수적으로 합쳤다. N5 current landing 자체의 별도 클래스 설명은 다른 원문이다.
- R02/R04/R05/R06의 현 도착 page에는3.11와stable current판 구분이 이미 있다. N4에는Bioconductor3.1 rowRanges 주석까지 포함된다. 원문 자체의 판/이력 정보가 있는 사례로 표시해 해당 민감도에서 뺄 수 있다.
- H 원문은 공식 과거 package Date/Publication 및 판으로 식별했다. 그 파일을 오늘 취득했다는 조회 UTC는 원장에 따로 있고 H 카드에는 오늘 상태·권고·정답이 없다. R03–R06 H의 archive는 표집 때 취득한 파일을 재사용했으며 해당 H member 읽기는 B 봉인 뒤에 수행했다.
- R03의 source function을 읽은 것은 실행·API 안정성 보증이 아니다. R4의 class 문서를 읽은 것은 새 데이터 처리 결과 검증이 아니다.

## 비용과 재현

costs.csv는 실제 기록한 GET 단위, final body bytes, 저장 bytes, 측정 elapsed, redirect를 포함한다. body bytes에는 redirect 중간 response body와 HTTP header/transport 비용이 포함되지 않는다. requests는 원 요청 단위이고 http_exchanges는 기록한 redirect+final 응답 수다. H의 네 물리 재사용은 별도0-request 행으로 기록한다. 읽기 노동·모델 비용·실서비스 비용은 미계측이다. 두번째 조회 구성 비교는 아직 실행하지 않았으며 root가 사전예산 안에서 실제 재생 또는 명시한 모의 계산으로 다루어야 한다.

sources.jsonl의 기존 B 접두 행은 유지하고 새 관측을 덧붙였다. 원문별 확인 내용·한계·duplicate group·최소수 산입은 각 행에 있다. 동일 원고와 조사 실패는 source 총 행수와 고유 원문 최소수로 혼동하지 않는다. N/H 카드의 원문 span은 exact excerpt 파일로 커밋하고 큰 PDF/HTML/tarball은 URL/hash/member/offset으로 재취득할 수 있게 기록한다. PDF 해당 쪽은 실제 렌더링해 text extraction과 대조했다.

다음 행동은 root의 카드·48판정 봉인이다. 이 파일은 기준판정이나 결과율을 제시하지 않는다.
