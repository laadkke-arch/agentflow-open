# AF-RES-009 — 실패·중단·전환과 반례

## 판정 범위

종료·부분 중단·전환의 핵심 사건 7건을 운영자·창업자·승계 당사자의 원문으로 확인했다. Sourcegraph의 부분 중단을 빼도 6개 별도 시스템 사건이 남는다. 접속 실패나 오래된 README만으로 쇠퇴·폐업을 판정하지 않았다. 아래 공식 이유와 연구자 추론 **H**를 구분한다. 기계 판독용 사건과 원인 축은 sources.json의 failure_cases에 있다.

## 1. 핵심 사건 7건

### F01. Google Code Search (classic public web service)

- **사건·날짜:** 공개 웹 코드검색과 API 종료. 2012-01-15 (2011-10-14 공지의 종료일).
- **범위:** 당시 외부 웹 OSS 코드 검색 제품과 API.
- **공식 이유:** Google은 여러 제품을 줄이고 집중한다는 포트폴리오 이유만 밝혔다. 짧은 원문: “To succeed you need real focus and thought”. [S-F03]
- **H: 큰 공급자도 별도 서비스의 우선순위를 바꾸므로 검색 공급자를 바꿀 수 있는 경계가 필요하다.**
- **경고:** 후속 Google Code Search나 내부 코드검색이 계속 존재하는 것과 옛 전역 제품의 종료를 구별한다.

### F02. Microsoft Academic Services / MAG

- **사건·날짜:** 웹·API 접근과 그래프 갱신/구판 배포 종료. 2021-12-31.
- **범위:** MAS 서비스와 MAG 갱신; 기존 사본 사용권은 라이선스대로 지속.
- **공식 이유:** 다른 조직·산업과 Microsoft 365로 기술을 옮기는 기회비용 판단이며 운영비가 이유는 아니라고 명시했다. 짧은 원문: “not based on the operational but on the opportunity cost”. [S-F01] [S-F02]
- **H: 풍부한 개체·인용 그래프와 의미검색이 있어도 소유 조직의 기회비용 판단으로 갱신이 끝날 수 있다.**
- **경고:** 풍부한 구조를 만드는 것과 그 구조를 계속 제공할 운영 약속은 별개다; 원 데이터 사본과 교체 경로를 알아야 한다.

### F03. Kite

- **사건·날짜:** 개발·지원 중단과 코드 공개. 2022-11-16 (창업자 회고 발행; 개발 활동은 글에서 2014–2021로 설명).
- **범위:** AI 코딩 보조 제품.
- **공식 이유:** 창업자는 당시 모델의 코드 구조/비지역 문맥 한계, 수익화가 늦어져 실패한 순서, code search 전환을 추진하기 어려운 팀 피로를 들었다. 짧은 원문: “our product did not monetize”. [S-F09]
- **H: 코드 문맥을 더 잘 이해하는 것만으로 구매할 새 가치를 설명할 수 있는 것은 아니다.**
- **경고:** 2022년의 '기술이 아직 준비되지 않았다' 판단을 오늘의 LLM 검색 한계로 복제하지 않는다.

### F04. Openbase (open-source package discovery)

- **사건·날짜:** 패키지 탐색 서비스 종료. 2023-04-24.
- **범위:** openbase.com의 OSS 부품 선택/비교 서비스.
- **공식 이유:** 창업자는 개발자에게 널리 쓰였지만 규모 있는 수익성 회사를 만들지 못했다고 밝혔다. 짧은 원문: “unable to build a large profitable company”. [S-F11]
- **H: '개발자가 좋은 부품을 모르는 비용'을 줄이는 가치가 있어도 회사가 원하는 수익 규모에 도달하지 못할 수 있다.**
- **경고:** 사용량·투자자 명성·개발자 호응을 유지 가능한 수익 구조의 대용으로 쓰지 않는다.

### F05. searchcode

- **사건·날짜:** 기존 대규모 전역 색인 중단 뒤 LLM용 저장소 도구로 재출발. 2025-08-28 중단 공지; 2026-03-03 재출발 회고.
- **범위:** 옛 전역 코드색인/광고형 서비스; 현재 이름을 쓴 새 도구 전체 폐업 아님.
- **공식 이유:** 운영자는 큰 색인/메모리 자원·환율과 광고매출 감소, API 이용자의 지불 의사 부족으로 비용을 감당하지 못했다고 설명했다. 짧은 원문: “approximate 10x drop in advertising revenue”. [S-F05] [S-F06] [S-F07]
- **H: 광범위한 상시 색인의 비용을 먼저 떠안기보다 이미 찾은 저장소를 요청에 맞게 조사하는 도구가 다른 운영 모델이 될 수 있다.**
- **경고:** 동일 도메인의 살아 있음만 검사하면 제품 범위가 전역 발견에서 저장소 분석으로 바뀐 사실을 놓친다.

### F06. Sourcegraph.com (personal sync / team beta)

- **사건·날짜:** 개인 저장소(공개·비공개) 동기화·team beta 중단 및 유료 고객 전용 Cloud 이전 계획. 2022-08-01.
- **범위:** Sourcegraph.com의 일부 multi-tenant 기능; 공개 OSS 검색은 유지.
- **공식 이유:** 보안·확장성·고객별 기능 제공과 개발 집중을 위해 single-tenant Cloud를 선택했다. 짧은 원문: “provide optimal security and scalability”. [S-F04]
- **H: 하나의 공개 서비스가 개인용/팀용/전역색인 요구를 모두 감당하는 운영 모델은 다시 나뉠 수 있다.**
- **경고:** 부분 중단 공지를 제품 전체 종료로 저장하면 후보 유효성 판단을 잘못한다.

### F07. Papers with Code (Meta original)

- **사건·날짜:** 원 포털 종료·Hugging Face 승계, 후속 재구현. 2025-07-24 (2025-07-25 당사자 글의 yesterday); 2026-11-20 재구현 README 확인.
- **범위:** 원 paperswithcode.com; 데이터 공개와 승계/재구현은 별도.
- **공식 이유:** 승계 당사자는 종료와 Meta 파트너십을 확인했으나 원 종료 이유는 공개하지 않았다. 짧은 원문: “which was sunsetted yesterday”. [S-F12] [S-F13] [S-F14]
- **H: URL 이전 또는 데이터를 넘겨주는 것만으로 분류·leaderboard·추천과 기존 workflow의 같은 기능이 보존되지는 않는다.**
- **경고:** 공식 승계 이름과 실제 기능 집합을 따로 확인하고, 최신 재구현이 있으면 영구 공백이라는 결론을 수정한다.

F07의 날짜는 공개 공지 HTML의 datePublished와 본문의 상대 날짜를 연결한 D1 확인이다. Kite는 당시 공식 창업자 글의 Wayback 보존본을 읽었으며 현재 주차 도메인을 종료 근거로 쓰지 않았다. [S-F09] [S-F14]

## 2. 어떤 원인이 제시됐는가

| 사건 | 유지·비용 | 수익 | 자료/모델 품질 | LLM 대체·유통 | 스팸·SEO | 다른 명시 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | 미공개 | 미공개 | 미공개 | 언급 없음 | 미공개 | 포트폴리오 집중 |
| F02 | 운영비 원인 부정 | 직접 이유 아님 | 미공개 | 직접 이유 아님 | 미공개 | 기회비용·다른 적용처 |
| F03 | 개발 부담 | 명시 | 당시 모델 문맥 한계 | 대체되어 종료라는 설명 아님 | 미공개 | 팀 피로 |
| F04 | 세부 미공개 | 명시 | 미공개 | 미공개 | 미공개 | 원하는 회사 규모 |
| F05 | 색인·RAM·환율 | 광고/API 명시 | 직접 원인 미공개 | 운영자의 zero-click·LLM 영향 주장 | 스팸 원인 미공개 | 새 제품 경계로 재출발 |
| F06 | 보안·확장성 | 고객 이전 계획; 부족 원인 미공개 | 미공개 | 직접 이유 아님 | 미공개 | single-tenant 집중 |
| F07 | 미공개 | 미공개 | 미공개 | 미공개 | 미공개 | 승계 사실만 확인 |

이 표는 원인 빈도를 추정하는 표본 통계가 아니다. 공개 회고에는 선택 편향이 있다. 수익화 실패와 크롤링 유지비 때문에 종료했다는 설명을 합칠 수 없다. [S-F01] [S-F03] [S-F04] [S-F05] [S-F09] [S-F11] [S-F14]

## 3. 추가 사례 — 최소 6건에 산입하지 않음

### F08. Hyperlint (adjacent evidence-maintenance tool)

2025-09-20: 상업적 GitHub 문서 검토·유지 도구 종료; OSS 도구 전환 의사. 창업자는 예산·설치/보안 마찰·알림 소음·구현 유지 부담과 범용 coding 도구/MCP의 대체 압박을 들었다. 원문: “that last 20 units needs to be valuable to justify your existence”. [S-F10]

**H: 범용 도구가 이미 제공하는 대부분의 가치 위에 얹는 유지/근거 기능의 추가 가치를 실제 구매나 반복 사용으로 확인해야 한다.** 핵심 지형 바깥의 인접 유지 도구; 최소 6건 요건은 F01–F07로 충족. 근거 유지 기능을 추가하는 것 자체가 제품 차별성과 지속성을 보장하지 않는다.

### F09. Neeva

2023 (인수 완료 전; 읽은 창업자 회고는 2025-03-27): 소비자 검색 종료 후 기업 검색으로 기술 이동. 창업자는 RAG 검색에 필요한 기술이 시작 당시 없었고 구현 시점에는 팀이 지쳐 기존 기술을 새 분야에서 쓰는 편이 낫다고 판단했다고 회고했다. 원문: “My team was tired”. [S-F15]

**H: 뛰어난 검색 기술과 인용 기능이 있어도 시장 시기·팀 지속성·유통은 별도 문제다.** 1차 인터뷰는 읽었지만 최초 공지/정확한 종료일 보강 전; 핵심6건에 의존하지 않음. 기술이 기업 내 검색으로 살아남은 사례를 소비자 검색 사업의 성공으로 바꾸지 않는다.

### F10. Sourcegraph Cody

2027-01-31 예정 (2026-11-09 발표): 미래 종료 예고. coding agent로 발전시키지 않은 선택과 시장 변화 뒤 code intelligence/retrieval 기반에 집중한다는 설명이다. 원문: “not to evolve Cody into a coding agent”. [S-F08]

**H: 같은 검색 자산이라도 사람용 assistant와 다른 agent가 쓰는 retrieval 도구 중 어디에 제품 경계를 둘지 바뀔 수 있다.** 조사 시점보다 미래의 예정 사건. 종료 예정일·실제 종료·대체 기능의 일대일 호환을 별도 상태로 저장한다.

Hyperlint의 80/20 가치 설명은 창업자의 가정적 가격 논증이다. 실제 대체율 80%라는 측정값이 아니다. Cody는 조사일보다 미래인 2027-01-31 종료 예정이며 현재 완료된 종료가 아니다. [S-F10] [S-F08]

## 4. 반대 방향 사례와 우리에게 주는 경고

- **풍부한 구조가 있어도 중단:** Microsoft Academic은 개체·관계 그래프와 의미검색을 갖췄지만 기회비용으로 종료됐다. **H:** 새 스키마의 풍부함은 지속 제공의 증거가 아니다. [S-F01] [S-F02]
- **단순한 링크 목록도 지속:** awesome의 2014 생성·2026 push와 비보관 상태는 장수의 반례다. PR 검토 밀림과 상호 검토 의무는 사람이 하는 유지 비용도 보여 준다. [S-AC05] [S-AC07] [S-AC37]
- **비용 부담이 곧 폐쇄는 아님:** Connected Papers의 2022 운영자는 서버·개인 자금/시간 부담에 Premium과 무료 한도로 대응했다. 이는 수익 모델 전환 사례이며 2026 가용성까지 증명하지는 않는다. [S-DE18] [S-DE19]
- **문서상 기능과 현재 경로의 차이:** OSSInsight About에 남은 Explorer가 직접 경로에는 유지보수 공지를 표시한다. 전체 서비스 종료나 원인을 추정하지 않는다. [S-AC16] [S-AC18]
- **H: 기존 조합을 먼저 비교:** searchcode는 LLM이 소비하는 저장소 도구로 재출발했고 Hyperlint는 범용 도구 위의 잔여 가치를 가격으로 설명하지 못했다. 별도 추천 UI보다 기존 도구를 연결하는 얇은 절차가 충분할 수 있다. [S-F06] [S-F07] [S-F10]
- **H: 유지 상태의 단위를 작게 둔다:** endpoint·기능·데이터 갱신·권리·권고 범위는 따로 변한다. Sourcegraph 부분 중단, searchcode의 범위 전환, PWC 원 포털과 재구현을 한 상태로 압축하지 않는다. [S-F04] [S-F06] [S-F12]

## 한계

공식 이유는 당사자의 진술이며 독립 손익·트래픽 감사가 아니다. 미공개 원인을 LLM·SEO·스팸으로 채우지 않았다. Koders/Ohloh/Open Hub·Slant는 적절한 1차 실패 본문을 얻지 못해 최소 사례에 넣지 않았다. 이 연구는 문서 확인 D1이며 계정·유료 호출·제품 가용성 시험을 하지 않았다. 새 형태의 완전성·갱신 SLA·수익성은 별도 확인 대상이다.

## 출처 링크

[S-F03]: https://googleblog.blogspot.com/2011/10/fall-sweep.html?hl=en_GB
[S-F01]: https://www.microsoft.com/en-us/research/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/
[S-F02]: https://www.microsoft.com/en-us/research/project/academic/
[S-F09]: https://web.archive.org/web/20221122101021/https://www.kite.com/blog/product/kite-is-saying-farewell/
[S-F11]: https://www.linkedin.com/posts/liorgrossman_today-i-am-writing-to-share-that-weve-made-activity-7051208392559771648-etA3
[S-F05]: https://boyter.org/posts/searchcode-is-being-rebooted/
[S-F06]: https://searchcode.com/
[S-F07]: https://boyter.org/posts/searchcode-has-been-rebooted/
[S-F04]: https://sourcegraph.com/blog/single-tenant-cloud
[S-F12]: https://github.com/huggingface/paperswithcode
[S-F13]: https://github.com/paperswithcode/paperswithcode-data
[S-F14]: https://www.linkedin.com/feed/update/urn:li:activity:7354483119762153472/
[S-F10]: https://billchambers.me/articles/hyperlint-post-mortem/
[S-F15]: https://stratechery.com/2025/an-interview-with-snowflake-ceo-sridhar-ramaswamy-about-data-and-ai/
[S-F08]: https://sourcegraph.com/blog/sunsetting-cody-future-of-code-intelligence
[S-AC05]: https://github.com/sindresorhus/awesome
[S-AC07]: https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md
[S-AC37]: https://api.github.com/repos/sindresorhus/awesome
[S-DE18]: https://medium.com/connectedpapers/announcing-connected-papers-a-visual-tool-for-researchers-to-find-and-explore-academic-papers-89146a54c7d4
[S-DE19]: https://medium.com/connectedpapers/announcing-premium-accounts-multi-origin-graphs-and-more-92e8dbd66848
[S-AC16]: https://ossinsight.io/docs/about
[S-AC18]: https://ossinsight.io/explore
