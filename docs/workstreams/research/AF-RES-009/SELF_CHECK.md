# AF-RES-009 — 자기 점검

## 완료 판정과 검사 범위

문서 연구의 필수 기준을 점검했다. 자동 검사의 실제 결과는 VERIFICATION.json, 다시 실행할 코드는 audit.py, 질문별 기계 판독 기록은 SELF_CHECK.json에 있다. **개수·참조 무결성과 문서상의 결론은 검증했으며 현재 제품 성능 우위나 D4 유용성을 검증한 것은 아니다.** 내부 별도 검토에서 발견한 과도한 완전성 기준·측정 분모·기능 범위 표현을 고쳤다.

| 필수 기준 | 결과 |
| --- | --- |
| 시스템 25개 이상, 범주별 3개 이상 | 35개: a4 / b6 / c4 / d4 / e6 / f5 / g6 |
| 직접 읽은 외부 원문 | 108개, 보수적 시스템당 최대3개 상한 후 **95개** 산입 |
| 공식 문서/About/약관 | 산입 자료 중 공식 문서 태그 **77개** |
| 공학 글·원논문 6개 이상 | 애매한 기술 도움말을 빼도 지정 집합 **9개**; 아래 별도 검증 |
| 1차 실패 자료·사건 | 서로 다른 6개 시스템의 지정 1차 원문6개 확보; 종료·부분중단·전환 핵심7건 |
| 생성형 결과 평가 | 원문3편: Liu2023·Tow2025·ALCE2023 |
| 검색·제외 기록 | 정확한 질의101개, 실패·차단·D0 제외51기록 |
| Q1–Q8 출처 다양성·반증 | 아래 전행에 외부 자료 2종류 이상과 실제 탐색/결과 있음 |
| 쓰기·커밋 | owned_path만 수정. dot-control·제품·공통 문서·main은 변경하지 않음 |
| 실행 등급 | 외부 문헌 D1. 선택적 Q7 질의 D3와 목표 유용성 D4는 미실시 |

공학/원논문의 보수적인 지정 집합: [S-AC24] [S-AC25] [S-AC31] [S-DE11] [S-DE12] [S-DE15] [S-DE18] [S-FG02] [S-FG03]. 실패 최소 자료의 지정 집합: [S-F03] [S-F01] [S-F09] [S-F11] [S-F05] [S-F14]. 보조 source를 더 읽었어도 상한을 넘겨 최소 개수에 넣지 않았다.

## Q1–Q8 자기 점검표

| 질문 · 답 한 줄 | 출처 ID와 종류 수 | 반증 질의·자료와 결과 | 남은 불확실성 · 답을 바꿀 최소 추가 확인 |
| --- | --- | --- | --- |
| Q1 — 35개 시스템의 분업과 기존 조합이 넓은 가치를 이미 제공한다. | **3종류**. 공식 기능 문서: [S-AC02] [S-DE04]; 제작자 원논문: [S-DE15]; 공학 설계 글: [S-FG03] | L-AC19, L-AC20, L-DE25, L-FG13. [S-AC37] [S-AC31] [S-FG24] — 장수 목록과 부분 문제→코드 설명, 구조+목표 도구가 있어 ‘단일 신규 가치’ 주장을 축소했다. | 선택한 지형의 문서 연구다. 현재 조합의 실제 과제 충분성은 비교하지 않았다. **최소 다음 확인:** 실제 공개 설계 결정 과제를 사전 고정하여 기존 조합 기준선과 비교. |
| Q2 — 자유문·부분 파일·패턴 대조·PICO/CPC 등 여러 시작점이 있으며 완전 양식을 일률 강제하지 않는다. | **3종류**. 공식 입력 문서: [S-DE04] [S-FG07] [S-FG14]; 전문가 조사 지침: [S-FG11]; 공학 설계 글: [S-FG03] | L-DE02, L-AC21, L-FG09, L-FG13. [S-FG14] [S-FG24] [S-AC30] [S-FG07] — PICO 단일 용어+역할, scope+자연어, 선택 항목, SMILES/부분구조를 확인하여 ‘전체 구조와 모든 필드 필수’를 기각했다. | 입력 수용과 구조 해석/제약 보존 정확성은 다르다. **최소 다음 확인:** 동일 부분 입력을 기준선에 주고 빠뜨린 제약과 추가 질문을 기록. |
| Q3 — 수집·갱신과 코드/데이터/본문/API의 권리를 분리해야 하며 공개 열람을 재배포 허가로 읽을 수 없다. | **4종류**. 약관·라이선스: [S-AC01] [S-AC20] [S-DE16] [S-DE17]; 제작자 데이터 배포: [S-AC12]; 제작자 원논문: [S-AC24]; 운영자 회고: [S-F05] | L-AC01, L-AC07, L-AC09, L-DE20. [S-AC12] [S-AC15] [S-DE16] [S-DE17] — 허용된 CC-BY/CC-BY-SA 데이터도 찾았으나 구판/원천/계약 경계와 S2 약관 문안 차이를 남겼다. 전부 사용불가 또는 전부 자유 사용이라는 양쪽 단정을 기각. | 선택할 endpoint·release별 적용 계약과 현재 갱신 SLA는 일부 미확정. **최소 다음 확인:** 실제 재사용 후보 하나의 릴리스·권리·갱신 조건만 우선 확인; DB 복제 전 판단. |
| Q4 — 대안·의존·인용·내용해시·코드색인·패턴·PICO는 다른 관계를 보존하므로 한 검색 표현으로 같게 볼 수 없다. | **3종류**. 공학 설계 글: [S-AC25] [S-FG03]; 제작자 원논문: [S-DE15] [S-AC24]; 공식 검색 문서: [S-AC30] [S-FG14] | L-AC11, L-AC21, L-DE12, L-FG02. [S-AC30] [S-DE15] [S-DE18] [S-DE23] — 자연어를 받는 코드 검색, 인용 없이 추론 가능한 SPECTER, 인용 트리와 다른 유사성 그래프를 확인하여 단순 키워드/그래프 이분법을 수정. | 과거 설계가 현행 엔진 전체와 같은지, 표현이 목표 적합성을 얼마나 보존하는지는 미측정. **최소 다음 확인:** 하나의 실제 부분 과제에서 기존 표현별로 누락/오연결된 제약을 비교. |
| Q5 — 링크·문장 지지·도움 이유·후속 유효성은 다르며 설명 기능과 실제 인용 품질을 구별한다. | **4종류**. 공식 기능 문서: [S-DE22] [S-FG16]; 공학 제작자 예제: [S-AC31]; 동료심사 평가 논문: [S-DE27] [S-DE29]; 기관 원평가: [S-DE28] | L-DE13, L-DE14, L-DE16, L-AC13, L-AC22. [S-DE27] [S-DE28] [S-DE29] [S-AC09] — 세 다른 과제의 무근거 문장/후첨 인용 불일치/잘못된 원기사·URL과 유료 노출 위치를 확인. 이를 2026 제품 오류율이나 비밀 순위 조작으로 확대하지 않음. | 현재 설계 추천의 인용 지지율·사용자 판단 비용은 미측정. **최소 다음 확인:** 기준선 결과에서 원문 구절과 특정 도움 주장 사이의 지지를 현재 자료로 판정. |
| Q6 — 종료·부분 중단·전환 7건은 이유가 다르며 유지비·수익·기회비용·기술/팀 문제를 분리한다. | **3종류**. 공식 종료/전환 공지: [S-F01] [S-F03] [S-F04] [S-F14]; 운영자·창업자 회고: [S-F05] [S-F09]; 창업자 종료 공지: [S-F11] | L-F03, L-F04, L-F13, L-F19, L-F23. [S-F01] [S-F06] [S-F12] [S-F11] — MAS는 운영비 이유를 부정했고 searchcode/PWC는 후속 형태가 있다. 전체 폐업·부분 중단·재출발·미래 Cody 예고를 분리. | 공식 이유는 독립 인과/손익 감사가 아니며 PWC 원 종료 이유는 미공개. **최소 다음 확인:** 경제성 가설이 필요해질 때만 선택 사례의 공개 손익/트래픽 또는 운영자 추가 자료 확보. |
| Q7 — 부품·구현·패턴 연결은 이미 있고 EIP의 기술 간 대응도 일부 존재한다. 더 넓은 원리 전이 부재는 입증하지 못했다. | **3종류**. 공학 글·제작자 예제: [S-AC31] [S-DE12] [S-FG03]; 공식 기능 문서: [S-F06] [S-FG04] [S-FG24]; 운영자 전환 회고: [S-F07] | L-AC13, L-AC15, L-AC21, L-FG17, L-X01, L-X02, L-X03, L-X04. [S-AC31] [S-F06] [S-FG03] [S-FG24] [S-X01] — 부분문제→코드 근거와 기술 간 용어/구성 대응을 인정. 추가 공식 질의4개는 엄격 전이 기능을 새 본문으로 확증하지 못했고 AskNature는 위치만 확인하여 시장공백으로 쓰지 않음. | P1/P2/P03 공개 실행은 선택 사항으로 미실시; 유추 전문 시스템의 방법론은 범위 밖. **최소 다음 확인:** 다음 범위에서 실제 결정 과제 또는 허용된 공개 Q7 질의로 부품/원리 연결을 관측. |
| Q8 — 일반 목록·식별·코드검색·문맥UI를 재구축할 필요성은 낮고, 목표 대응·변경 후 재검토의 추가 가치는 H로 남는다. | **4종류**. 공식 기능/데이터 문서: [S-DE04] [S-FG24] [S-AC15]; 공학 제작자 예제: [S-AC31]; 운영자 회고: [S-F10] [S-F07]; 평가 논문: [S-DE27] | L-DE25, L-DE27, L-AC19, L-AC20, L-AC21, L-FG17, L-X01. [S-AC05] [S-AC31] [S-DE04] [S-FG24] [S-F10] — LLM 조합 충분/목록 충분 양쪽을 조건부로 수용. 무누락 기준을 빼고 동일 과제·허용오류·검토시간에서 동등 이상이면 H1을 기각; H2 유지는 별도 판단. | 제품 필요성·지불 가치·성능 우위는 아직 검증되지 않았다. **최소 다음 확인:** 실제 공개 결정 과제의 강한 두 기준선 프로토콜부터 고정; 합성 문제만 재사용하지 않음. |

질의의 정확한 원문·실제 UTC·도구·본 결과와 열린 source ID는 SEARCH_LOG.json에서 위 ID로 연결된다. “2종류”는 도움말/About의 이름만 다르게 세는 방식이 아니라 기능 문서, 공학 글/원논문, 데이터 배포·약관, 운영자 공지/회고, 전문가 지침, 외부 원평가의 역할 차이를 구분한 것이다. 모든 근거·반증 source ID가 존재하고 외부 본문인지 자동으로 점검한다.

## 내부 별도 검토와 반영

- a–c 조사자, d–e/평가 조사자, 실패 조사자가 서로 다른 원장·종합 초안을 검토했다. **사람 또는 다른 모델의 검토라고 부르지 않는다.**
- ALCE의 모호한 “절반” 대신 문장별 citation recall의 설정·분모를 기록했다. Liu의 1450은 각 엔진의 질의 수임을 명시했다. [S-DE27] [S-DE29]
- AWS preview·내부 자원 링크, citator의 일부 법률 논점, Cochrane의 역사 주석과 현재 갱신 계약을 분리했다. [S-FG22] [S-FG26] [S-FG16] [S-FG14]
- grep.app/Sourcegraph/searchcode의 기존 부분 연결을 적극 인정하고, deps.dev의 버전·출처·갱신은 해당 범위의 충족으로 올렸다. [S-AC31] [S-AC30] [S-F06] [S-AC15]
- 분야 사이의 거리를 새 조건으로 넣지 않고 EIP의 기술 간 대응을 부분 충족으로 인정했다. 카탈로그 입력은 사람이 문제를 대조·선택하는 과정임을 밝혔다. [S-FG03] [S-FG04]
- 기준선에 완전검색을 요구하는 문구를 제거했다. 탐색 H1과 변경 후 유지 H2를 별도 비교하며, 사전 고정한 허용 오류·검토시간에서 기존 방법이 동등하거나 더 나으면 해당 추가 가치 가설을 기각한다.

더 자세한 검토 범위와 수정은 REVIEW.md에 남겼다.

## 실행한 검사와 재현

저장소 루트에서:

```bash
python docs/workstreams/research/AF-RES-009/audit.py --stage pre-handoff --write-report docs/workstreams/research/AF-RES-009/VERIFICATION.json
```

인계 커밋과 원격 재열람 후에는 쓰기를 만들지 않는 최종 검사:

```bash
python docs/workstreams/research/AF-RES-009/audit.py --stage final
git diff --name-only 50ebddbc28a756a4c886184d0f56a0f648e19145 HEAD
git status --porcelain
```

제품 코드를 바꾸지 않은 문서 연구이므로 제품 빌드·성능 테스트로 유효성을 꾸미지 않았다. 무결성 검사는 참조·개수·필수필드·질의 연결·경로·커밋 범위의 게이트다.

## 한계

각 원문은 관련 절을 읽은 D1이며 문서 전체를 한 글자씩 읽었다는 주장이 아니다. source counts는 독립 실험 횟수가 아니다. 공개 계정 기능·실제 추천 순위·운영 손익·자동 인용 정확도·P1/P2/P03 결과는 관측하지 않았다. 기능·권리·시점의 불확실성은 원장에 남겼고, 전행의 최소 다음 확인을 적었으므로 미확정 영역을 완료된 성능 증명으로 인계하지 않는다.

## 출처 링크

[S-AC24]: https://upsilon.cc/~zack/research/publications/ipres-2017-software-heritage.pdf
[S-AC25]: https://github.blog/engineering/the-technology-behind-githubs-new-code-search/
[S-AC31]: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp
[S-DE11]: https://exa.ai/blog/building-web-scale-vector-db
[S-DE12]: https://exa.ai/blog/exa-code
[S-DE15]: https://aclanthology.org/2020.acl-main.207.pdf
[S-DE18]: https://medium.com/connectedpapers/announcing-connected-papers-a-visual-tool-for-researchers-to-find-and-explore-academic-papers-89146a54c7d4
[S-FG02]: https://microservices.io/post/architecture/2023/03/13/better-decision-making-with-patterns.html
[S-FG03]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html
[S-F03]: https://googleblog.blogspot.com/2011/10/fall-sweep.html?hl=en_GB
[S-F01]: https://www.microsoft.com/en-us/research/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/
[S-F09]: https://web.archive.org/web/20221122101021/https://www.kite.com/blog/product/kite-is-saying-farewell/
[S-F11]: https://www.linkedin.com/posts/liorgrossman_today-i-am-writing-to-share-that-weve-made-activity-7051208392559771648-etA3
[S-F05]: https://boyter.org/posts/searchcode-is-being-rebooted/
[S-F14]: https://www.linkedin.com/feed/update/urn:li:activity:7354483119762153472/
[S-AC02]: https://alternativeto.net/faq/
[S-DE04]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/copilot-spaces/create-copilot-spaces
[S-AC37]: https://api.github.com/repos/sindresorhus/awesome
[S-FG24]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-architecture-reviews.html
[S-FG07]: https://support.google.com/faqs/answer/7049475?hl=en
[S-FG14]: https://assets.wiley.com/image/upload/v1786361551/how-to-use-pico-search-updated-2023.pdf?_s=public-apps
[S-FG11]: https://www.epo.org/en/learning/learning-resources-profile/business-and-ip-managers/inventors-handbook/novelty-and-prior-art
[S-AC30]: https://sourcegraph.com/docs/code-search/query-assist
[S-AC01]: https://alternativeto.net/about/terms/
[S-AC20]: https://docs.ecosyste.ms/docs/usage/licences/
[S-DE16]: https://webflow.semanticscholar.org/product/api/license
[S-DE17]: https://api.semanticscholar.org/license/
[S-AC12]: https://zenodo.org/records/1196312
[S-AC15]: https://docs.deps.dev/api/v3/
[S-DE23]: https://learn.researchrabbit.ai/en/articles/12454660-how-researchrabbit-builds-and-ranks-your-map
[S-DE22]: https://elicit.com/solutions/reports
[S-FG16]: https://www.thomsonreuters.com/en-us/help/drafting-assistant/westcheck/keycite-status-flags
[S-DE27]: https://aclanthology.org/2023.findings-emnlp.467.pdf
[S-DE29]: https://aclanthology.org/2023.emnlp-main.398.pdf
[S-DE28]: https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
[S-AC09]: https://www.saashub.com/featured-products
[S-F04]: https://sourcegraph.com/blog/single-tenant-cloud
[S-F06]: https://searchcode.com/
[S-F12]: https://github.com/huggingface/paperswithcode
[S-FG04]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/
[S-F07]: https://boyter.org/posts/searchcode-has-been-rebooted/
[S-X01]: https://asknature.org/about/
[S-F10]: https://billchambers.me/articles/hyperlint-post-mortem/
[S-AC05]: https://github.com/sindresorhus/awesome
[S-FG22]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent.html
[S-FG26]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-view-rec.html

