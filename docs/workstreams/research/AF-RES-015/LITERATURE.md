# 링크 부패 실증 연구와 본 조사 비교

| 원문 | 자료·관측 창 | 분모와 기준 | 보고한 수치 | 이번 연구에서 대응되는 값 |
| --- | --- | --- | --- | --- |
| Liu 등, Broken External Links on Stack Overflow | 2019년 6월 덤프, 두 검사 라운드 2019년 12월·2020년 1월 | 고유 외부 URL 11,926,354개. 두 번 모두 2xx 없음. URL 출현 빈도를 따로 집계 | 1,687,995 URL(14.2%). 출현 빈도 기준 2,493,328건(10.8%) | 011 단회 HTTP 원값과만 같은 주소 차원. 반복 회수, 실패 코드, 모집단이 달라 비율을 합치지 않는다. [저자의 본문·방법](https://meta.stackexchange.com/questions/353998/characterizing-broken-external-links-on-stack-overflow), [논문 서지](https://smusg.elsevierpure.com/en/publications/broken-external-links-on-stack-overflow/) |
| Klein 등, Scholarly Context Not Found | 2014년 분석, STM 논문 350만 편 이상과 웹 URI 인용 100만 개 이상 | 논문별 한 건 이상 부패한 참조. 현재 도달성 및 출판 시점에 가까운 보존 사본을 사용 | 전체 논문 약 1/5. 웹 인용이 있는 논문 약 7/10 | 015의 답 단위는 여러 이유로 분해된다. 가까운 보존 사본 부족은 015에서는 과거 미확인으로 남긴다. [본문](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253) |
| Jones 등, Scholarly Context Adrift | 여러 논문 코퍼스의 인용 URI 약 106만 개. 초기·후기 보존본과 현재 텍스트 비교 | 보존 쌍과 현재 텍스트 241,091건의 텍스트 유사도 | 184,065/241,091(76.35%)에 drift | 작은 수정부터 기능 제거까지 텍스트 유사도는 구분하지 않는다. 015는 진술의 조건을 항목별 대조했다. [본문 §Assessment, Fig. 11](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0167475) |
| Zittrain·Albert·Lessig, Perma | 2014, 미국 연방대법원 1996년부터 2011년 개정기 및 3개 법률 학술지 | 공개 URL이 처음 인용한 자료를 내놓는지 원문 일부 수동 점검 | 대법원 URL 약 50%, 3개 학술지 전체 70% 이상에서 원 내용 재현 어려움 | 열리는 페이지에서 인용과 관련된 조건을 찾는다는 점이 015와 유사하다. 법률 쟁점 효력이나 추천 기능의 현재 평가와는 분모·판정 단위가 다르다. [본문](https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/) |
| Pew, When Online Content Disappears | Common Crawl 2013–2023 각 연도에서 추출한 약 100만 페이지의 총표본, 2023년 10월 검사 | URL과 DNS의 도달성, 네 차례 재시험. 모호한 실패는 사망에 미산입 | 전체 25%, 2013년분 38%, 2023년분 8% 접근 불가 | 일시적 차단과 명시 404를 분리하는 Q4 규칙의 근거다. 원래 추천 속성의 변경 비율로 환산할 수 없다. [보고서](https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/), [방법 원문](https://www.pewresearch.org/data-labs/2024/05/17/methodology-link-rot/) |
| 18 Million Links in Commit Messages | GitHub 23,110개 저장소의 링크 출현 18,201,165건. 2023년 공개 | 변경 위험이 있는 URL의 접근성, 저장소 이관과 반복 URL 분석 | 변경 위험군 14%가 접근 불가 | 역사적으로 옮겨진 코드 식별자는 실패의 중요한 원인이다. 015의 저장소 이동 양성에는 재명이 유지되는 반례도 있다. [논문 공개판](https://arxiv.org/pdf/2305.16591) |
| Escamilla 등, Cited But Not Archived | arXiv·PMC 260만 편에서 인용한 4개 Git 호스팅 플랫폼. 2024년 공개 | 전체 고유 호스팅 URL의 live·웹 보존, SWH는 저장소 URL에 한정 | live 93.98%, 웹 사본 81.43%, SWH 저장소 사본 68.39% | 보존 사본 하나와 추천 당시 사본을 구분해야 한다. 이 연구에서 과거 판이 확인된 이유의 비율로 옮길 수 없다. [논문 §4, Fig. 1](https://arxiv.org/pdf/2401.04887) |

한 페이지의 상태는 주소 응답, 원래 내용의 재현, 추천에 사용한 조건의 현재 성립으로 나뉜다. 동일한 링크를 따라가는 연구라도 위 세 값을 서로 대신 쓸 수 없다. 015의 고정 창에서 주소와 이유 모두 관측된 경우는 혼동표의 교차 셀에 있다. 신호 재현율은 그런 교차 표본으로만 계산했다. [confusion.json](results/confusion.json)

## 한계

원문에서 발표한 정의와 수치를 옮겼다. 각 연구의 원래 수집을 다시 실행하거나 URL 집합 사이의 중복을 확인하지 않았다. Liu 등의 전체 절차는 동일 연구자들의 공개 본문에 근거하며 IEEE 초록을 같은 연구의 서지로만 썼다. [열람 원장](sources.json)
