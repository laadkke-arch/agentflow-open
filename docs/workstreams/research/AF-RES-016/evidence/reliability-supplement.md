# Q3 보강: Hooper(1965)·Markey(1984) 원문 재탐색

확인일: 2026-11-20 UTC. 기계 판독 기록: [reliability-supplement.json](reliability-supplement.json).

## 1. 결과와 완료 범위

추가 조사에서도 **지정 원문 본문을 확보한 수는 0/2편**이다. Hooper(1965)의 원 보고서·학회 발표문과 Markey(1984)의 학술지 논문 본문을 직접 읽었다고 표시할 수 없다. 후속 문헌의 인용, 서지정보, 검색 결과, 원문 요청 버튼을 해당 원문으로 대신 세지 않았다. 기존 `reliability-sources.json`과 `reliability-notes.md`는 수정하지 않았고, 이번 보강으로 최소 자료 개수에 더한 자료는 0개다.

정확한 제목, 보고서 번호, 저자·기관, 공식 학술지, 기관 저장소, 공개 스캔을 대상으로 **32개 질의**를 실행했다. 강한 검색 엔진(system1) 28개, 보조 검색 엔진(system2) 4개이며, 공개 URL **10곳**을 실제로 열었다. 같은 URL을 다시 확인한 요청은 URL 수에 중복 계산하지 않았다. 검색어 32개와 각 묶음의 결과는 JSON `search_log`에 보존했다.

이 결과는 지정한 두 고전 원문의 직접 열람 요건을 충족했다는 뜻이 아니다. 다른 직접 열람 문헌이 충분하더라도 이 두 자료의 원문 확인 여부는 별도 미확인으로 남겨야 한다.

## 2. 확인한 경로

| 대상·경로 | 실제 관측 | 본문 요건에 대한 처리 |
| --- | --- | --- |
| [Scholar Archive 정확한 제목 검색](https://scholar.archive.org/search?q=%22Interindexer+consistency+tests%22) | 도구가 URL에 접근하지 못함 | 원문 미열람; 아카이브에 원문이 없다고 추론하지 않음 |
| [Internet Archive Hooper 제목 검색](https://archive.org/search?query=%22Indexer+consistency+tests%22) | 도구가 URL에 접근하지 못함 | 원문 미열람; 공개 item URL은 확보하지 못함 |
| [공식 학술지 issue 목록](https://www.sciencedirect.com/journal/library-and-information-science-research/issues) | HTTP 403 | Markey의 1984년 issue·본문 미열람 |
| [공식 기관의 저자 링크 경로](https://www.si.umich.edu/people/karen-markey) | 공개 개인 사이트 연결만 확인 | 논문 본문 아님; 프로필 본문·연락처는 저장하지 않음 |
| [ERIC EJ303179](https://eric.ed.gov/?id=EJ303179) | 도구가 URL에 접근하지 못함 | 서지 레코드도 직접 읽지 못함; 레코드만 있어도 원문 기준에는 불충분 |
| [GovInfo의 NIST 서지자료 PDF](https://www.govinfo.gov/content/pkg/GOVPUB-C13-8797ec1300fb7a8449078ba434bc3f00/pdf/GOVPUB-C13-8797ec1300fb7a8449078ba434bc3f00.pdf) | 12,731,003바이트로 도구의 본문 길이 한도 초과, HTTP 400 | 다른 문헌의 서지자료이며, 이번 시도에서 본문을 읽지 못함 |
| [NASA CENDI 워크숍 1994](https://ntrs.nasa.gov/api/citations/19950005945/downloads/19950005945.pdf) | 본문과 일치도 측정 절 직접 열람 | MS01. Hooper 인용·후속 적용일 뿐 원문 재수록 아님 |
| [OSTI 1970년 색인자 훈련 보고서](https://www.osti.gov/servlets/purl/4091850) | 본문 직접 열람. 이후 참고문헌 검색 요청은 HTTP 502 | MS02. 요청한 두 원문 중 어느 것도 아님 |
| [기관이 연결한 저자 사이트](https://ylime.people.si.umich.edu/) | index 페이지, 추출된 본문 0줄 | 논문 목록·공개 원문 링크를 확보하지 못함 |
| [Markey 논문의 ResearchGate 공개 레코드](https://www.researchgate.net/publication/292401952_Interindexer_consistency_tests_A_literature_review_and_report_of_a_test_of_consistency_in_indexing_visual_materials) | 원문이 제공되지 않는다는 표시 확인. 나머지는 서지정보·후속 인용 문헌 | 원문 미열람. 저자에게 요청하거나 로그인하지 않음 |

## 3. 새로 읽은 후속 자료에서 확인한 것

### MS01: Hooper의 인용을 찾는 것과 원 보고서를 읽는 것은 다르다

NASA의 *CENDI Indexing Workshop*, NASA Conference Publication 10160(1994), 인쇄본 78–88쪽의 평가·색인자 일치도 절을 읽었다. 88쪽은 공통 색인어 수를 배정된 고유 색인어 수로 나눈 쌍별 계수와 그 평균인 집단 계수를 설명하며 Rodgers(1961), Hooper(1965)를 선행으로 인용한다. 이 내용은 **후속 현장에서 term-set overlap을 적용한 방식**을 확인한다. Hooper가 원 보고서에서 어떤 실험 단위·조건·수치를 제시했는지까지 검증하지는 않는다. [MS01 본문](https://ntrs.nasa.gov/api/citations/19950005945/downloads/19950005945.pdf)

따라서 후속 자료의 색인어 겹침 비율을 AF-RES-011의 149개 단위 중 역할 라벨이 같은 75개라는 비율과 수치만으로 비교해서는 안 된다. 공통 색인어와 합집합 색인어를 세는 문제, 이미 고정된 단위마다 하나의 라벨을 비교하는 문제는 분모가 다르다. 이 구분은 이번 보강에서도 유지된다.

### MS02: 일치도를 높이는 중재는 독립 코딩의 증거가 아니다

1970년 보고서 *Use of Data-Base Access for Interindexer Communication and for Indexer Training*(UCRL-19862)의 도입·방법·색인자 일치 시험·결과를 읽었다. 6명, 10개 논문씩 두 세트, 205개 항목·470개 기술어가 든 참조 파일을 사용하는 실험이다. 다른 색인 결과를 참조하는 소통·훈련 조건을 다루므로, 참조 이후 일치가 높아져도 블라인드 독립 코딩의 재현성이 높다는 것과 같은 의미는 아니다. [MS02 본문](https://www.osti.gov/servlets/purl/4091850)

이 보고서는 요청한 두 고전의 대체물이 아니다. 뒤이어 Hooper 참고문헌을 찾는 요청은 502로 실패했으므로, 해당 참고문헌의 정확한 문구를 직접 확인했다고 기록하지 않았다.

## 4. 대상별 남은 불확실성과 최소 다음 행동

| 대상 | 남은 불확실성 | 답을 바꿀 최소 추가 확인 |
| --- | --- | --- |
| Hooper(1965) | 원문 표지·실험·계수 정의·결과표를 읽지 못함. 서지 경로에 나타난 TR95-56과 TR-95-96의 차이도 원문 없이 확정할 수 없음 | 공개 IBM 또는 FID 1965 스캔의 실제 URL 하나를 확보한다. 첫 행동은 표지의 제목·번호·판을 확인하는 것이며, 다음으로 정의·실험 단위·결과표를 읽는다. 새 공개 URL이나 확인된 식별자가 없는 상태에서 같은 후속 인용만 다시 모으는 것은 충족 증거가 아님 |
| Markey(1984), *Library & Information Science Research* 6(2):155–177 | 원문의 방법·결과를 읽지 못함. 2차 설명의 참여자 수 차이도 해소되지 않음 | 공개 저자판·기관판 또는 정상 접근 가능한 발행사 원문 URL 하나를 확보해 155–177쪽을 읽는다. 참여자 수, 이미지 수, term/concept 구분, 비교쌍 선택을 원문 방법·결과에서 확인한 뒤에만 수치 인용 |

재개에 쓸 공개 검색 입력은 JSON에 모두 남겼다. 새 원문 주소가 제공되면 두 대상의 `original_body_read` 상태와 원문별 근거 위치부터 갱신한다. 이 작업을 위해 계정 생성·로그인·유료 구입·저자 메시지·접근 제한 우회를 할 필요는 없으며, 이번 조사에서는 그런 행동을 하지 않았다.

## 5. 한계

이 경로들에서 원문을 확보하지 못한 것은 공개 원문이 존재하지 않는다는 증명이 아니다. 웹 도구가 읽을 수 없는 레코드·사이트와 실제 원문 부재도 구별했다. `supporting_reads`의 두 자료는 본문 열람 기록이지만 이번 보강의 최소 자료 개수에는 더하지 않았다. 고전 원문 미확인 상태가 내부 별도 코딩의 수치 계산을 무효로 만들지는 않지만, 사용자가 지정한 고전 원문 직접 열람 요건은 여전히 충족하지 못한 상태다.

이 문서는 코딩 원 응답이나 다른 동시 작업의 결과를 열지 않고 작성했다. 내부 별도 코딩은 사람 간 또는 서로 다른 모델 집단 간 재현성의 직접 증거가 아니라는 기존 해석 제한도 그대로 적용한다.
