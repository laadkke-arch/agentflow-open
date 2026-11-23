# 원 자극에서 실제 기사와 독립 원전까지 따라간 대조

이 두 사례는 **Panizza의 접근 효과 주 선정 자료가 아니다**. 모든 군이 같은 링크에 접근할 수 있어 pop-up/보상 개입의 자극·참값 점검에만 쓴다. 원 [실험2 자극 파일](https://osf.io/download/xsr43/)의 `Stimuli` 시트에서 `Name=MaleC`, `Name=NaturalB`의 `ArticleURL`, `Sources`, `Scientific Validity` 열을 직접 읽었다. 파일 SHA256은 `1dcdc7f06ab835659b3d9bed3ea0ecefee71a86a332f798078feca820cb830c5`다. 두 행 모두 저자 키는 `High`이며 이를 임의로 바꾸지 않았다.

## 1. MaleC: 중심 방향 지지와 통계 표현의 범위

| 연결 | URL·판·직접 읽은 위치 | 판정 |
|---|---|---|
| 실제 자극 기사 | [France24 원 URL](https://www.france24.com/en/live-news/20201209-men-with-covid-19-3-times-more-likely-to-need-intensive-care-study); [2020-12-30 보관판](https://web.archive.org/web/20201230195400/https://www.france24.com/en/live-news/20201209-men-with-covid-19-3-times-more-likely-to-need-intensive-care-study), 제목·본문1–4문단·동반질환 한계 문단 | 실험 이전 기사 본문 회수. 현재 원 URL 웹 도구 접근 실패를 보관판으로 보완했다. |
| 저자가 키에 연결한 독립 원전 | [Peckham et al. 2020](https://www.nature.com/articles/s41467-020-19741-6), Results의 최종 포함 보고서·meta-analysis, Figure3, Methods의 data extraction/analysis | 집중치료 입원에 대한 남성의 **오즈비 2.84**, 95%CI 2.06–3.92. 8개 보고서, 341,571사례가 해당 분석 분모다. 전체 감염사례 3,111,714를 이 결과의 분모로 옮기지 않는다. |
| 독해 판정 | 원 기사와 독립 원전은 중심 방향에서 일치 | **지지**: 해당 초기 유행 자료에서 남성의 입원 오즈가 더 높음. “모든 남성 개인의 입원확률이 정확히 3배” 또는 인과 효과까지는 지지하지 않음. |

기사의 “more likely”를 정밀한 확률비로 읽는다면 원전의 OR와 다른 양이다. 이는 본 조사자의 통계적 범위 판정이다. 원전 자체도 집계 자료여서 생활양식, 동반질환, 검사 방식, 병원/지역사회 사례 차이를 통제하지 못했다고 설명한다. 기사 후반도 동반질환 자료 부족을 언급한다. 기사 링크가 존재했다는 사실만으로 독자가 그 한계 절을 읽었다고 판정하지 않는다.

원전 본문은 2026-11-23의 현재 발행자 판에서 직접 읽었으며, 논문 본문의 실험 당시 정확한 화면은 별도로 보장하지 못한다. DOI+correction/erratum 검색과 Crossref `relation`/`update-to`에서 이 DOI의 정정을 찾지 못했다. 이는 검색 범위 내 미발견이며 정정이 전혀 없다는 증명이 아니다.

## 2. NaturalB: 올바른 중심 키와 기사 세부 불일치

| 연결 | URL·판·직접 읽은 위치 | 판정 |
|---|---|---|
| 실제 자극 기사 | [ZME Science 원 URL](https://www.zmescience.com/science/many-plants-have-been-naturally-gmod-by-bacteria/); [2021-05-08 보관판](https://web.archive.org/web/20210508064022/https://www.zmescience.com/science/many-plants-have-been-naturally-gmod-by-bacteria/), 본문 전체와 말미 원논문 링크 | 실험 이전 기사 회수. 기사 발행일은 2021-04-21. 현재 원 URL은 웹 도구에서402였다. 보관판은 공개 접근200으로 읽었다. |
| 키의 독립 원전 | [Matveeva & Otten 2019](https://link.springer.com/article/10.1007/s11103-019-00913-y), 공개 초록·첫 페이지 | 본문 구독벽. 초록은 275종의 유전체에서 23종, 356종의 전사체에서 추가16종을 보고한다. 이는 완전한 방법·결과 독해가 아니다. |
| 저자 기관 설명 | [IBMP/CNRS 2019-10-12 발표](https://www.ibmp.cnrs.fr/naturally-transgenic-plant-species-occur-on-an-unexpectedly-large-scale/?lang=en), 본문 전체 | 자연적 전달과 41종을 설명하고 일부 유전자의 기능은 미상이라고 한다. 원 논문 전체를 대체하지 않는다. |
| 독해 판정 | 자극 키 `High`를 유지하고 기사 세부를 별도 표기 | **중심 주제의 부분 지지 / 원전 전체 검증 미확인**. 당시 기사에는 “356종의 유전체, 15종”이라고 되어 있어 원 초록의 데이터 유형과 수가 다르다. 자연적 전달의 존재를 식품 안전이나 모든 규제 판단의 정답으로 넓히지 않는다. |

이 사례는 참값키가 제목·자막의 중심 과학 주장에 붙고 기사 전체의 모든 숫자에 붙는 것이 아님을 보여 준다. 키를 보존하면서 오류 위치를 따로 표시해야 한다. “원문을 열었다”만으로 원문 안의 모든 세부가 검증되지는 않는다.

본문 결손을 위해 발행자 페이지, ResearchGate의 발행자 preview, OpenAlex의 판본 위치, [HAL hal-02354867v1](https://hal.science/hal-02354867v1)와 공개 HAL API, 저자 기관 페이지를 확인했다. HAL API는 정확히1개 서지 레코드를 반환했으나 `fileMain_s`/`files_s`는 제공하지 않았다. OpenAlex도 해당 위치에 공개 PDF를 표시하지 않았다. 정정 검색은 이 DOI의 명시적 정정을 찾지 못했고 다른 논문의 정정/철회 템플릿은 이 논문의 사건으로 연결하지 않았다.

**최소 재개 입력**은 저자가 공개한 전문 또는 정상 공개 접근이 되는 원논문 판본이다. 그 판본의 표·보충자료와 15/16종 차이, 유전체/전사체 구분을 다시 확인하면 현재 “부분 지지” 판정이 바뀔 수 있다. 초록과 기관 요약은 직접 독해 최소20개 산입에서 제외했다. 보관 기사 두 건도 수량을 늘리는 용도로 세지 않고 이 원 자극 검증에만 연결했다.

## 재현 위치

`retrieval-log.jsonl`의 `truth/male.html`, `truth/male_news_archive.html`, `truth/natural_news_archive.html`, `truth/matveeva_cnrs.html`, `truth/matveeva_openalex.json`, `truth/hal_record.json`에 URL·UTC·상태·해시를 남겼다. 보관판 응답의 HTTP200은 직접 본문을 읽은 뒤에만 성공으로 판정했다. 원 참가자의 해당 페이지 열람·스크롤·이해는 두 사례 모두 **미확인**이다.
