# Bioconductor B 봉인 준비

6개 참조·6개 출판 HTML·5프로젝트를 선택했다. DESeq2 1.28.0, GenomicRanges 1.40.0, SummarizedExperiment 1.18.0, SingleCellExperiment 1.10.0(devel/intro 두 문서), scater 1.16.0이다. 모두 Bioconductor 3.11의 초기 안정판이며 릴리스 공표일은 2020-04-28이다. DESCRIPTION의 Date/Publication 2020-04-27은 별도 날짜로 보존했고 특정 HTML 최초 업로드 UTC는 미확인이다.

## 문서·목적

| 참조 | 소비자 문서 | 첫 적격 href | 문장에 근거한 최소 목적 | 층 |
| --- | --- | --- | --- | --- |
| R01 | DESeq2 / Analyzing RNA-seq data | http://www.bioconductor.org/help/workflows/rnaseqGene/ | FASTQ에서 count matrix 생성까지 더 천천히 설명하는 workflow 읽기 | 현재 실용 |
| R02 | GenomicRanges Introduction | https://bioconductor.org/packages/3.11/IRanges | 기반 infrastructure 패키지 확인 | 애매함 |
| R03 | Extending SummarizedExperiment | https://bioconductor.org/packages/S4Vectors | setValidity2를 사용하는 validity method 정의 방법 | 현재 실용 |
| R04 | Developing around SingleCellExperiment | https://bioconductor.org/packages/3.11/DESeq2 | rowRanges를 갖는 DESeqDataSet 클래스 설계 예 | 애매함 |
| R05 | scater Overview | https://bioconductor.org/packages/3.11/SingleCellExperiment | 상호운용 기반 데이터 클래스 확인 | 현재 실용 |
| R06 | Introduction to SingleCellExperiment | https://bioconductor.org/packages/3.11/scater | 중심 데이터 구조의 적용 패키지 예 확인 | 애매함 |

특정 판 재현을 명시한 층은 0이다. 3.11이 href에 있다는 사실만으로 역사 재현 의도를 추정하지 않았다. 이후 목적지 결과를 보고 다른 참조로 바꾸지 않는다.

## 표집·탈락

프로젝트 우선순서는 SCOPE대로 적용했다. edgeR/limma에는 PDF 안내용 index HTML만 있고 외부 기술 href가 없다. Biostrings/S4Vectors/BiocParallel/Biobase/AnnotationDbi는 3.11 초기 안정판의 inst/doc HTML이 없었다. 이 일곱 프로젝트에서 다음 Bioconductor 안정 릴리스 3.12와 3.13의 초기 안정판도 조사해 같은 부재를 확인했다. '다음 안정판'은 R 경로가 명시한 Bioconductor 릴리스 순서를 적용했으며 모든 중간 패치판을 전수 검사한 것은 아니다. frame.csv가 34개 실제 archive 요청의 판·상태·멤버 수를 보존한다.

첫 순회에서 적격 문서는 다섯 개였다. 두 번째 순회의 SummarizedExperiment 일반 vignette는 외부 HTTP href가 0이어서 탈락했고, 다음 SingleCellExperiment intro를 여섯째로 택했다. split HTML 장을 독립 출판물로 세지 않았다. 자기 패키지 landing href는 자기 탐색, GitHub contact 요청은 연락 목적으로 제외했으며 link-selection.jsonl에 선택 전 앞선 href를 모두 남겼다.

## 중요한 사전 노출·한계

1. 최초 frozen PACKAGES가 끝 패치판을 가리켜, 초기 안정판 Archive 목록 응답을 기다리며 끝 패치판 tarball 12개를 원배포 후보로 취득했다. 그 뒤 Archive에서 .0을 찾아 원판으로 삼았다. 끝 패치판의 선택 대상 본문은 읽지 않았지만 member 목록/hash를 확인했다. edgeR/limma의 작은 index HTML은 읽었고 초기 안정판과 bytes가 같다. 이러한 선행 취득은 비용·시도에서 지우지 않았다. 동일 작성자의 이후 판독을 미노출이라고 부르지 않는다.
2. R-L02는 DESeq2의 원 배포 metadata를 찾기 위해 https://bioconductor.org/packages/3.11/bioc/html/DESeq2.html 을 먼저 열었다. 이것은 R04의 목적지와 canonical overlap 가능성이 있다. 원 href를 아직 직접 요청하지 않았어도 현재 도착 본문 사전 노출일 수 있으므로 R04의 pre_exposed_current_target=true를 미리 고정한다. 봉인 후 redirect를 대조해야 한다.
3. R01↔R04, R05↔R06 및 소비자/목적지 사이 프로젝트 단서가 겹친다. 새 판독 문맥도 간접 노출을 완전히 없애지는 못한다. N/H의 독립성·정답은 이 단계에서 판단하지 않는다.

## 보존·재현

references.jsonl에 archive URL/hash, member/hash, exact cleaned-text offset/hash, 실제 href·link text·HTML line, 목적과 층을 넣었다. evidence/*-B-context.txt는 B에 넣을 원문 exact bytes이고 *-B-html-excerpt.txt는 실제 href가 있는 원 HTML 구간이다. html_extract.py와 reconstruct_base.py로 공개 archive에서 같은 member와 발췌를 다시 얻을 수 있다. 큰 tarball과 이미지가 포함된 전체 HTML은 이 작업공간에서 취득했으나 커밋 대상에서 제외한다. 그 바이트를 원격에 영구 보존했다고 주장하지 않는다. 커밋 대상은 commit-files.json에 제시한다.

네 보기 결정과 기준판정은 아직 만들지 않았다. 목적지 GET과 H 원문 읽기는 루트의 12참조 B 원격 봉인 이후에만 시작한다. R04 metadata 사전 노출 예외는 위에 그대로 보존한다.
