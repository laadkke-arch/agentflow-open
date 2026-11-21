# 외부 문헌 직접 읽기 기록

## 열람 방식과 집계 규칙

- 열람 일자: 2026-11-21 UTC. 기록의 시각 정밀도는 날짜이며 개별 요청의 초를 추정하지 않는다. 본문 열람 구간은 04:59:35–05:12:26 UTC 세션 안이다.
- D0 검색 결과·초록은 후보 탐색에만 사용했다. 열람 실패·판독 불가·서지만 읽은 주소는 sources-external.json의 excluded에 분리했다.
- 웹 open/find의 본문을 직접 읽었다. 스캔인 X09는 익명 urllib GET200 후 PyMuPDF와 Tesseract를 메모리에서 사용해 PDF pp.3–9를 읽었다. 원문·OCR 전문은 파일로 저장하지 않았다. pdf 스킬의 추출·판독 점검 지침을 적용했다.
- X08은 셸 GET403과 달리 웹 open의 본문 전사가 반환되었다. 실제 본문 L123–825의 지정 범위를 읽었으며 검색 snippet만 읽은 것으로 세지 않았다.
- 최소수의 단위는 고유 문헌이다. X12의 PDF 합본은 Part 1 한 건, X07의 같은 원문 대체 주소는 한 건으로 센다. X21은 저자의 회고 원문이며 X05·X07과 독립적인 검증 횟수로는 세지 않는다.

## 원문별 확인 위치

| ID | 실제 연 주소 | 읽은 본문 위치 | 수준 | 근거로 쓴 질문 |
| --- | --- | --- | --- | --- |
| X01 | [Sobek, Ward & Liker — Toyota’s Principles of Set-Based Concurrent Engineering](https://www.gapimprove.org/_files/ugd/cd8b34_2d04bd540ca04019986c3ba54ae8631e.pdf?index=true) | 본문 Introduction; Principles 1–3; PDF pp.1–6,16–20 / 열람 L25–157,440–550 | D1 | Q1, Q3, Q5, Q6, Q8 |
| X02 | [Ford & Sobek — Adapting Real Options to New Product Development by Modeling the Second Toyota Paradox](https://www.researchgate.net/publication/3076866_Adapting_Real_Options_to_New_Product_Development_by_Modeling_the_Second_Toyota_Paradox) | 원 논문 모델·결과·Discussion; HTML L1689–1759 | D1 | Q3, Q5, Q6, Q8 |
| X03 | [Dow et al. — Parallel Prototyping Leads to Better Design Results, More Divergence, and Increased Self-Efficacy](https://hci.stanford.edu/publications/2010/parallel-prototyping/ParallelPrototyping2010-final.pdf) | 실험 설계·결과; PDF pp.1–11 / L0–322 | D1 | Q5, Q6, Q8 |
| X04 | [Parnas — On the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html) | KWIC 두 분해안; General comments; Conclusions / HTML L86–113 | D1 | Q1, Q3, Q5, Q7, Q8 |
| X05 | [Baldwin & Clark — Modularity in the Design of Complex Engineering Systems](https://homepages.cwi.nl/~storm/teaching/reader/BaldwinClark06.pdf) | §4–6, §11; PDF pp.5–10,25–26 / L215–384,898–929 | D1 | Q1, Q3, Q5, Q7, Q8 |
| X06 | [Sullivan, Griswold, Cai & Hallen — The Structure and Value of Modularity in Software Design](https://www.researchgate.net/publication/2366338_The_structure_and_value_of_modularity_in_software_design) | Introduction; KWIC 모델; §7 Discussion / HTML L2375–2414 | D1 | Q1, Q3, Q5, Q6, Q8 |
| X07 | [Baldwin & Clark — The Option Value of Modularity in Design: An Example from Design Rules](https://www.academia.edu/23867694/The_Option_Value_of_Modularity_in_Design_An_Example_from_Design_Rules_Volume_1_The_Power_of_Modularity) | §2, §2.1–2.3, §3; HTML L13,19–56; 원문 pp.4–11 | D1 | Q1, Q3, Q5, Q6, Q8 |
| X08 | [MacLean, Young, Bellotti & Moran — Questions, Options, and Criteria: Elements of Design Space Analysis](https://www.researchgate.net/profile/Victoria_Bellotti/publication/233367028_Questions_Options_and_Criteria_Elements_of_Design_Space_Analysis/links/00b7d53211940ad48e000000/Questions-Options-and-Criteria-Elements-of-Design-Space-Analysis.pdf) | §2–4 및 휴리스틱; 열람 L123–164,242–254,365–417,594–644,787–825 | D1 | Q1, Q2, Q3, Q4, Q6, Q7, Q8 |
| X09 | [Kunz & Rittel — Issues as Elements of Information Systems](https://www.escholarship.org/content/qt5cj786v8/qt5cj786v8.pdf) | PDF pp.3–9(본문 §1–12), 메모리 내 OCR 직접 열람; 원본 PDF 첫 장 메타데이터 | D1 | Q1, Q3, Q4, Q6, Q7, Q8 |
| X10 | [Nygard — Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 본문 전체; HTML L7–61 | D1 | Q1, Q4, Q5, Q6, Q7, Q8 |
| X11 | [Buckingham Shum et al. — Graphical Argumentation and Design Cognition](https://kmi.open.ac.uk/publications/pdf/kmi-97-5.pdf) | §2–4; PDF pp.9–21; L316–438,505–620,842–886 | D1 | Q1, Q5, Q6, Q8 |
| X12 | [Alonso-Coello et al. — GRADE Evidence to Decision frameworks 1: Introduction](https://ilcor.org/uploads/Tools-GRADE-guidelines-Evidence-to-Decision-Tables.pdf) | Part 1 질문·평가·결론; PDF pp.1–9 / L19–35,101–160 | D1 | Q1, Q2, Q4, Q6, Q7, Q8 |
| X13 | [Elliott et al. — Living systematic review: 1. Introduction—the why, what, when, and how](https://discovery.ucl.ac.uk/10025041/1/Thomas_LSR%20overview%20paper%20final%20-%20revised.pdf) | Introduction; When; How; PDF pp.3–8 / L46–159 | D1 | Q2, Q5, Q6, Q7, Q8 |
| X14 | [Snilstveit et al. — 3ie evidence gap maps: a starting point for strategic evidence production and use](https://www.3ieimpact.org/sites/default/files/2019-01/wp28-egm.pdf) | §1–2; PDF pp.7–10 / L126–190 | D1 | Q1, Q2, Q4, Q6, Q7, Q8 |
| X15 | [White et al. — Guidance for producing a Campbell evidence and gap map](https://journals.sagepub.com/doi/full/10.1002/cl2.1125) | 본문 지도 범위·틀·자료 검색/코딩·갱신; HTML L28–90 | D1 | Q1, Q2, Q3, Q6, Q7, Q8 |
| X16 | [Neumann et al. — The GRADE evidence-to-decision framework: testing in 15 international guideline panels](https://link.springer.com/article/10.1186/s13012-016-0462-y) | Methods, Results, Discussion; HTML L100–158 | D1 | Q2, Q4, Q6, Q7, Q8 |
| X17 | [Elliott et al. — Living Systematic Reviews: An Emerging Opportunity to Narrow the Evidence-Practice Gap](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001603) | Living Systematic Reviews; Production; Publication; HTML L165–194 | D1 | Q2, Q5, Q6, Q7, Q8 |
| X18 | [Shin & Ariely — Keeping Doors Open: The Effect of Unavailability on Incentives to Keep Options Viable](https://web.mit.edu/ariely/www/MIT/Papers/doors.pdf) | Experiment 1; Experiment 3; PDF pp.3,7–8 / L193–236,578–650 | D1 | Q5, Q6, Q8 |
| X19 | [Gilbert & Ebert — Decisions and revisions: The affective forecasting of changeable outcomes](https://gwern.net/doc/psychology/2002-gilbert.pdf) | Studies 1,2 및 Discussion; PDF pp.3–9 / L175–229,682–725 | D1 | Q5, Q6, Q8 |
| X20 | [Amazon — 2016 Letter to Shareholders](https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders) | High-Velocity Decision Making; HTML L43–55 | D1 | Q5, Q6, Q8 |
| X21 | [Lenfle & Baldwin — From Manufacturing to Design: An Essay on the Work of Kim B. Clark](https://www.hbs.edu/ris/Publication%20Files/07-057.pdf) | §5.1–5.3; PDF pp.31–36 / L965–1128 | D1 | Q1, Q3, Q5, Q8 |
| X22 | [NASA — Systems Engineering Handbook §6.8 Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/) | §6.8.1–6.8.1.3; HTML L258–346 | D1 | Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 |
| X23 | [Amazon — 2015 Letter to Shareholders](https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF) | Invention Machine; PDF p.5 / L188–219 | D1 | Q5, Q6, Q7, Q8 |
| X24 | [HM Treasury — The Green Book: UK government guidance on appraisal](https://assets.publishing.service.gov.uk/media/6ae0ba897b7111c482d80a3b/The_Green_Book_2026.pdf) | §1.8; §5.1–5.4,5.35; §6.101–6.104; PDF pp.8,29,36,54 / 열람 L184–188,1064–1093,1477–1494,2275–2294 | D1 | Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 |

## 새 호스트 익명 접근 기록

첫 단계의 기존 호스트 점검은 PROGRESS.md에 있다. 이후 발견한 호스트는 공개 웹 open으로 문서의 본문 또는 실패 응답을 확인했고, 아래에는 추가 익명 루트 GET 1회의 **실제 코드**를 남긴다. 루트 URL의 코드는 문서 URL·웹 열람 도구의 코드와 같지 않다. HTTP 코드가 노출되지 않는 웹 성공을 임의로 200이라고 적지 않는다. 자세한 시각과 최종 URL은 external-network-check.json이다.

| 호스트 | 익명 루트 GET 코드 | 본문 확인 |
| --- | --- | --- |
| www.gapimprove.org | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| homepages.cwi.nl | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| www.cs.lafayette.edu | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| www.cognitect.com | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| ilcor.org | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| discovery.ucl.ac.uk | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| journals.sagepub.com | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| gwern.net | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| hci.stanford.edu | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| kmi.open.ac.uk | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| link.springer.com | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| journals.plos.org | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| www.hbs.edu | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| www.academia.edu | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| www.nasa.gov | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| s2.q4cdn.com | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| assets.publishing.service.gov.uk | 404 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| scholarsarchive.byu.edu | 403 | 원문별 성공/실패는 sources-external.json에 별도 기록 |
| mitpress.mit.edu | 200 | 원문별 성공/실패는 sources-external.json에 별도 기록 |

기존 시도에서 코드가 직접 확인된 문서 요청: www.escholarship.org PDF200, www.researchgate.net PDF403(웹 본문은 성공), www-personal.umich.edu PDF403, public.websites.umich.edu PDF403, www.usmcu.edu PDF403, papers.ssrn.com403, www.cs.drexel.edu502/503, www.cc.gatech.edu 지정 PDF404. 제한을 변경하거나 우회하지 않았다. 차단 시 재개는 같은 URL에 대해 접근이 허용된 환경에서 `curl -I '<url>'`로 확인하고 원문을 읽는 것이다. 이미 성공한 별도의 공개 원문이 있으면 그 주소를 쓴다.

## 탐색과 반증 질의

| 목적 | 실행한 질의·열람 | 결과 |
| --- | --- | --- |
| 대안 보존의 조건과 비용 | ‘The Second Toyota Paradox’ PDF; Sobek1999 find ‘Principle 3’; Ford/Sobek 모델 Discussion | Ward1995 스캔 제외; X01의 극단 사례 정정과 X02의 이른/늦은 확정 비용 확인 |
| 모듈화의 무조건 우월성 반증 | ‘The Option Value of Modularity in Design’ PDF; Baldwin/Clark2006 find ‘Costs’; Parnas General comments | X04·X05·X07: 공유 규칙, 인터페이스 손실, 비용 가정 때문에 무조건 우월성 기각 |
| 논증 기록의 부담 | ‘Questions Options and Criteria pdf Maclean Bellotti’; ‘Graphical Argumentation and Design Cognition’ PDF | X08·X11: QOC와 IBIS의 차이, 잘 정의된 문제에서 기록 부담 확인 |
| 보존 충동과 복구 가능성의 비용 | ‘Keeping Doors Open Shin Ariely’ PDF; Gilbert/Ebert Studies·Discussion | X18·X19: 소멸 위협과 만족 비용. 가역성의 이점도 함께 남김 |
| 근거와 결정이 달라지는 이유 | ‘GRADE evidence-to-decision 15 international’ 및 EtD 본문 | X12·X16: 관점·기준·응답 축이 다르면 결론 비교가 달라짐 |
| 무조건 living 운영 반증 | Elliott2017 When/How; Elliott2014 Publication | X13·X17: 적용·종료 조건, 갱신 강도와 거짓 양성 문제 |
| 빈칸의 다른 의미 | 3ie wp28 및 Campbell 본문 | X14·X15: 자료 부재와 종합 부재, 과도한 세분화의 비용 |
| 결정 전환 조건과 규모 | NASA 6.8; ‘Green Book real options 2022’ 후 실제 PDF 판 확인 | X22·X24: 추가 정보 가치, 전환 가정, 2022 URL의 2026 redirect 관측 |

## 재현 입력

문헌 다시 읽기의 입력은 sources-external.json의 url, version_or_date, sections_read이다. 네트워크 접근 검사:

```sh
curl --max-time 20 -I 'https://www.nasa.gov/reference/6-8-decision-analysis/'
curl --max-time 20 -I 'https://www.escholarship.org/content/qt5cj786v8/qt5cj786v8.pdf'
```

PDF 본문 확인이 필요한 경우 공개 원문을 허용된 환경에서 열고 지정한 PDF 쪽을 읽는다. X09의 추출은 PyMuPDF의 `fitz.open(stream=pdf_bytes, filetype='pdf')`, 쪽 이미지의 메모리 변환, `tesseract stdin stdout`을 사용했다. 스캔 문서의 정밀 인용이 필요하면 OCR을 그대로 복사하지 말고 해당 쪽과 대조해야 한다.

## 최소수와 사이트 상한 계산

고유 원문 24개이며 excluded 22개는 포함하지 않는다. 카테고리는 겹칠 수 있지만 고유 문헌 총수에는 한 번만 센다. 비용·실패 최소수는 모형 X02를 빼고도 직접 연구 보고 X11·X18·X19 세 개로 충족한다. 아래 숫자는 이번 작업자의 자료 분류 집계이며 문헌의 연구 결과 수치가 아니다.

| 조건 | 최소 | 집계 | ID | 충족 |
| --- | --- | --- | --- | --- |
| alternative_preservation_set_based | 3 | 5 | X01, X02, X03, X22, X24 | 예 |
| real_options_modularity | 3 | 6 | X02, X04, X05, X06, X07, X21 | 예 |
| rationale_QOC_IBIS_ADR | 3 | 4 | X08, X09, X10, X11 | 예 |
| evidence_decision_living_EGM | 4 | 6 | X12, X13, X14, X15, X16, X17 | 예 |
| cost_failure_primary_reports | 2 | 3 | X11, X18, X19 | 예 |

보수적 사이트 집계(Amazon 회사 사이트와 IR CDN을 합침):

| 사이트 | 집계 | 상한 3 이내 |
| --- | --- | --- |
| www.gapimprove.org | 1 | 예 |
| ResearchGate | 3 | 예 |
| hci.stanford.edu | 1 | 예 |
| www.cs.lafayette.edu | 1 | 예 |
| homepages.cwi.nl | 1 | 예 |
| www.academia.edu | 1 | 예 |
| www.escholarship.org | 1 | 예 |
| www.cognitect.com | 1 | 예 |
| kmi.open.ac.uk | 1 | 예 |
| ilcor.org | 1 | 예 |
| discovery.ucl.ac.uk | 1 | 예 |
| www.3ieimpact.org | 1 | 예 |
| journals.sagepub.com | 1 | 예 |
| link.springer.com | 1 | 예 |
| journals.plos.org | 1 | 예 |
| web.mit.edu | 1 | 예 |
| gwern.net | 1 | 예 |
| Amazon (including IR CDN) | 2 | 예 |
| www.hbs.edu | 1 | 예 |
| www.nasa.gov | 1 | 예 |
| assets.publishing.service.gov.uk | 1 | 예 |

## 한계

완료자·표본·관측 창이 필요한 수치는 원문 위치를 함께 기록했다. 비율을 이용한 설계 우월성 판정은 하지 않았다. 24개는 서로 다른 문헌이지 24개의 독립 재현이 아니다. 전이 효과 검증은 CROSSFIELD.md §7의 후속 입력으로 남긴다.
