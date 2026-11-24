# 원전 대조: 네트워크 척도와 STFT

## 수용 범위

사전 판정 커밋 `0b6287e5359257004900ef4b8e30f7abb7306024` 뒤에 원방법 저작 3개를 본문까지 직접 읽었다. 이 묶음은 **사후 검증**이며 원래 12자리의 링크·도달·새 선택 수를 늘리지 않는다. 전체 읽은 범위, 실제 도착 주소, 판, 해시, 확인 시각과 실패는 이 폴더의 `sources.jsonl`·`fetch-receipts.jsonl`에 있다. 원문 복사본과 렌더는 임시 캐시에만 두었다.

| 근거 ID | 실제 읽은 원저작 | 확인 범위와 제약 |
| --- | --- | --- |
| NET-METHOD-SELF | [Zelnik-Manor·Perona, Self-Tuning Spectral Clustering](https://proceedings.neurips.cc/paper_files/paper/2004/file/40173ea48d9567f1f393b20c855bb40b-Paper.pdf) | 8쪽 전체·부록. 3쪽 Fig2·식1–2를 렌더로 다시 확인. |
| NET-METHOD-STFT | [Allen·Rabiner, A Unified Approach to Short-Time Fourier Analysis and Synthesis](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/122_unified_approach_to_STFT.pdf) | 7쪽 전체. 1560쪽 Fig3·OLA 식과 1563쪽 표본화 식을 렌더로 확인. |
| NET-METHOD-SNF | [Wang 등, Similarity Network Fusion](https://mghassem.mit.edu/wp-content/uploads/2015/06/nmeth.2810.pdf) | 기관에 있는 원 논문의 웹 PDF 텍스트로 Online Methods를 직접 읽음. 원 PDF 다운로드·그림 렌더는 실패. 정확한 식1 분모 표기는 시각 확인하지 못했으므로 단정하지 않음. |

SNF의 성공한 본문 열람은 검색 서비스가 제공한 원 PDF 본문이다. 원 DOI의 초록, 기관 미러, 저자 목록 페이지를 별도 저작으로 더하지 않는다. MIT 다운로드 503, UCSD 공개 원경로 404, Nature PDF 요청의 HTML 이동, 저자 페이지의 publisher 이동 실패를 보존했다. 본문을 읽은 SNF 원저작 하나만 고유 산입하며, 원래 R3-B의 `abstract_only`는 유지한다.

## R3: 원전이 보장하지 않는 책임을 옮기지 않기

공통 문서에 이미 등장한 국소 척도의 방법 계보는 확인된다. 그러나 원전의 정의와 대상 API의 예외 계약은 다른 주장이다. 원전으로부터 시간 제외·상호이웃 필터 뒤의 공석을 전역 스칼라에서만 허용해야 한다는 결론은 나오지 않는다. 결측 측정값 대치와 그래프의 빈 이웃 행을 같은 실패로 합치면 이 구분이 사라진다. `NET-TEST-LOCAL-EMPTY`는 바로 그 차이를 보존한다.

처음에는 국소 척도를 원전의 주된 장점으로 읽었지만, 중복점에서 척도가 0이 되는 `NET-TEST-ZERO-SCALE`과 다중 뷰의 표본 ID 순서가 다른 `NET-TEST-VIEW-IDENTITY`를 추가해 보편적 적용을 보류했다. 이는 작업자의 구성 반례이며 논문이 그런 입력에서 실제 실패했다고 보고한 결과가 아니다.

SNF가 유전체를 다룬다는 이유만으로 원리가 유전체에서 시작됐다고 분류하면 안 된다. Online Methods는 컴퓨터 비전의 앞선 다중 뷰 학습을 계보로 명시한다. 이 파일에서는 실제 원문이 말하는 계보와 적용 분야를 분리했으며, 앞선 2012년 논문 자체의 우선권까지 검증했다고 주장하지 않는다. [SNF Online Methods, 본문 근거](https://mghassem.mit.edu/wp-content/uploads/2015/06/nmeth.2810.pdf)

## R1: 경계 패딩만으로 해결되지 않는 경우

구성 시험은 창 정렬, 변환 길이, 실제 시각이라는 서로 다른 책임을 분리한다. `NET-TEST-CIRCULAR`는 길이 4 FFT와 길이 5 선형 컨볼루션의 출력을 비교한다. `NET-TEST-IRREGULAR`는 `[0,1,3,4]`초의 관측을 배열 위치 `[0,1,2,3]`초로 오인하는 경우다. 두 사례의 숫자는 NumPy 산술로 확인했지만 원 논문 실험, librosa API, MKV 디코딩을 실행한 결과는 아니다. 정확한 명령·버전·입력·출력은 `arithmetic-result.json`에 있다.

`NET-TEST-WINDOW-EDGE`는 중심 패딩을 제거해도 첫 경계의 합성 가능성이 자동으로 확보되지 않는 조건부 반례다. 이 안은 원 요청의 tokenizer가 역변환을 요구한다는 근거를 제공하지 않는다. 따라서 R1에 반환할 보편 수리법으로 올리지 않는다.

## 기존 판정에 미치는 영향

원전의 목적·전제에 대한 이해는 늘었지만, 제한된 두 번째 열람의 새 선택 0이라는 사전 판정은 바뀌지 않는다. 반박 가능성을 검사하기 위해 만든 여섯 시험은 모두 사후 구성 자료다. 실제 실행은 그중 산술 두 건이고, 나머지는 예상값이다. 고정 프로젝트 소스가 이미 요청을 처리하는지는 부모 작업자의 별도 구현 원장으로 대조해야 한다.

## 검산

`acquisition-census.json`은 검색 3회·질의 8개와 원문/반복/실패를 포함하는 출처 행 18개를 구별한다. 서로 다른 원방법 저작은 3개다. 논문 전체의 임상·클러스터링 결과를 재현한 시행은 0개이고, 목표 라이브러리 실행도 0개다. 이 폴더는 Git 커밋을 만들거나 공통 원장을 수정하지 않았다.
