# AF-RES-009 — 빈자리와 반증

## 판정

**“설계 일부와 목적을 받아 도움이 될 링크를 설명한다”는 넓은 가치만으로 신규성은 성립하지 않는다.** 부분 입력은 Copilot Spaces와 Sourcegraph, 부품 연결·설명은 grep.app/LLM와 searchcode·Exa, 패턴에서 구현으로의 연결은 EIP에 이미 있다. 다른 분야에서는 Elicit·Cochrane·citator가 구조화 질문·근거 구절·후속 취급의 구체적 선행 기능을 제공한다. [S-DE04] [S-AC30] [S-AC31] [S-F06] [S-DE12] [S-FG04] [S-DE21] [S-FG14] [S-FG16]

남은 것은 **H: 외부의 여러 제공자를 가로질러, 사용자의 원래 부분·목적·제약과 후보 해법·근거·변경을 함께 검토하는 절차가 반복 비용을 줄이는가**이다. 이것은 문서 지형에서 추린 검증할 가설이며, 아직 비어 있는 시장이나 별도 제품의 지불 가치를 입증한 결론이 아니다.

## 1. 다섯 요소 × 시스템 판정

SCOPE의 기준을 유지한다. **이미 충족**은 그 시스템의 명시된 분야와 입력 범위 안에서 해당 기능이 문서화됐다는 뜻이다. 목표 소프트웨어 과제에 대한 D4 성공이나 모든 다섯 요소의 동시 충족이 아니다. **부분 충족**은 일부 경로·인접 단위 또는 사람의 번역이 필요함을 뜻한다. **비어 있음**은 이번에 읽은 공식 범위에서 해당 기능의 근거를 확인하지 못했다는 뜻이며 시스템/시장 전체의 기능 부재 선언이 아니다.

- 구조·부분 입력: 부분 범위/구성/관계와 목적을 함께 줄 수 있는 경로. 구조 해석의 정확도는 별도.
- 부품 단위 연결: 전체 제품보다 작은 패키지·코드·패턴·방법 단위. 임상/법률 근거 단위는 인접 능력으로 부분 판정.
- 타 분야 원리: 다른 영역의 메커니즘과 목표 구조의 대응·전이 전제를 설명. 제품·기술 간 전이도 후보이며 분야의 거리는 필수조건이 아니다. EIP의 제품 간 용어/구성 대응은 부분 충족으로 인정하고, 단순 다분야 색인은 그 자체로 충족하지 않는다.
- 링크 중심 설명: 검토할 원문/코드/지침 위치와 도움·관계의 이유 연결. 대상 자원 링크인지 외부 해법의 출처인지 구별.
- 근거 유지: 출처/버전/갱신 또는 후속 무효화 관계의 명시된 관리. SWH 보존·revision context·S2 diff·citator는 서로 다른 방식의 충족이며, 모두 주장 진실성을 보증한다는 뜻은 아님.

| 시스템 | 구조·부분 입력 | 부품 연결 | 타 분야 원리 | 링크 설명 | 근거 유지 | 판정 범위·근거 |
| --- | --- | --- | --- | --- | --- | --- |
| AlternativeTo | 부분 충족 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 주목적·부분 대안 문제/개선 경로는 있으나 설계 관계는 사용자가 번역. [S-AC02] |
| OpenAlternative | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 제품·부품 목록과 활동 점수; 목적별 부분 적합성은 별도. [S-AC03] [S-AC04] |
| sindresorhus/awesome | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 분야별 부품 링크는 이미 충분할 수 있음; 사람이 선정·유지. [S-AC05] [S-AC07] [S-AC37] |
| SaaSHub | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 제품 비교·재검증; 유료 삽입을 적합도 순위로 읽지 않음. [S-AC08] [S-AC09] [S-AC10] |
| Libraries.io | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 패키지/의존 링크는 제공; 수집 정확도·목적 적합성은 다른 계약. [S-AC11] [S-AC12] |
| deps.dev / Open Source Insights | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 이미 충족 | 패키지 버전·출처·해시와 피드/스캔 갱신은 충족; 목적 적합성은 별도. [S-AC14] [S-AC15] |
| ecosyste.ms | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 패키지·repo·패치·목록 관계의 메타데이터 기반. [S-AC19] [S-AC20] [S-AC35] |
| OSSInsight | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 활동 증거 보조; 자연어 Explorer는 부분 유지보수 공지. [S-AC16] [S-AC17] [S-AC18] |
| Software Heritage | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 이미 충족 | 해시·origin·visit의 원문 보존은 충족; 현재 본체 상태 불명. [S-AC23] [S-AC24] |
| npms.io / npms analyzer and queries | 비어 있음 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 부품 발견·연속 점수 루프는 있으나 근거 버전 보존 계약과 현재 가동은 불명. [S-AC33] [S-AC34] [S-AC36] |
| GitHub Code Search / Blackbird | 부분 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 부분 코드를 검색식으로 번역; 코드/정의 링크·색인 갱신. [S-AC25] [S-AC26] [S-AC27] |
| Sourcegraph Code Search / Zoekt / Query Assist | 이미 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 이미 충족 | scope+자연어·부분 코드; revision context로 근거 재현의 한 형태 지원. [S-AC28] [S-AC29] [S-AC30] |
| grep.app + MCP | 이미 충족 | 이미 충족 | 비어 있음 | 이미 충족 | 비어 있음 | LLM 조합의 공식 부분문제→코드→파일/행 설명 예제; 갱신 계약 미확인. [S-AC31] [S-AC32] |
| searchcode (current repository intelligence service) | 부분 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 지정 repo의 구조·구간·구현 비교; 외부 후보의 최초 발견과 구별. [S-F06] |
| Perplexity Search / Deep Research / Projects | 이미 충족 | 부분 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 부분 문맥+목적·검색 합성·인용이 존재; 전용 전이/무효화는 미확인. [S-DE01] [S-DE02] [S-DE03] |
| GitHub Copilot Spaces / repository semantic search | 이미 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 선택 파일+지시·관련 코드 검색은 기존 기능; moving main과 고정 인계 근거는 다름. [S-DE04] [S-DE05] [S-DE06] |
| DeepWiki / Ask Devin | 부분 충족 | 이미 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 선택 repo의 부분 구조·소스 링크 설명; 새 후보 전역 발견과 구별. [S-DE07] [S-DE08] [S-DE09] |
| Exa Search API / exa-code | 부분 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | API/SDK 코드 예제와 URL 문맥; 최종 적합성 설명은 호출자. [S-DE10] [S-DE11] [S-DE12] |
| Semantic Scholar / S2AG / Recommendations / SPECTER | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 이미 충족 | 논문 추천과 릴리스/update-delete 유지; 소프트웨어 적용 판단은 별도. [S-DE14] [S-DE15] [S-DE16] |
| Connected Papers | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 비어 있음 | 논문 유사성/선행·후속 연결; 2026 갱신·운영 상태 불명. [S-DE18] [S-DE19] |
| Elicit | 이미 충족 | 부분 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 학술 질문+PICO/조건+구절 인용; 원문변경의 과거 주장 무효화는 미확인. [S-DE20] [S-DE21] [S-DE22] |
| ResearchRabbit / RR+ Signals | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 이미 충족 | 논문 관계 추천; 기존 collection의 위험/철회 표식 유지. [S-DE23] [S-DE24] [S-DE25] [S-DE26] |
| Microsoft Academic Services (역사 시스템) | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 비어 있음 | 과거 의미검색/추천 기능의 기록; 현재 서비스·갱신 종료. [S-F01] [S-F02] |
| Papers with Code (Meta 원 서비스와 Hugging Face 재구현) | 부분 충족 | 이미 충족 | 비어 있음 | 부분 충족 | 부분 충족 | task/method/구현·평가 링크; 원 포털 종료와 재구현의 현재성 구별. [S-F12] [S-F13] [S-F14] |
| microservices.io | 부분 충족 | 이미 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 사람이 부분 문제를 패턴으로 찾음; forces·대가 설명. [S-FG01] [S-FG02] |
| Enterprise Integration Patterns | 부분 충족 | 이미 충족 | 부분 충족 | 이미 충족 | 부분 충족 | 서로 다른 메시징 제품의 용어·구성 대응과 구현 링크; 다른 영역의 적용 전제 판정은 사람. [S-FG03] [S-FG04] |
| Azure Architecture Center — Cloud design patterns | 부분 충족 | 이미 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 제약별 패턴·구현 예; 자동 사용자 구조 해석은 별도. [S-FG05] |
| Thoughtworks Technology Radar | 비어 있음 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 경험 기반 권고·발행 시점; 옛 blip을 갱신하지 않음. [S-FG06] |
| AWS Well-Architected Tool / Agent | 이미 충족 | 부분 충족 | 비어 있음 | 이미 충족 | 부분 충족 | AWS의 부분 구조/목표·지침/자원 링크·why; Agent preview, 외부 OSS 발견과 구별. [S-FG19] [S-FG22] [S-FG24] [S-FG26] |
| Google Patents | 부분 충족 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 문단·CPC·SMILES/화학 부분구조 입력; 일반 설계의 목적 해석·원리 전이와 구별. [S-FG07] [S-FG08] [S-FG09] |
| EPO Espacenet / CPC | 부분 충족 | 부분 충족 | 비어 있음 | 부분 충족 | 부분 충족 | 분류/청구항·인용으로 신규성 반증; 전체 구조를 요구하지 않음. [S-FG10] [S-FG11] |
| PubMed Clinical Queries | 부분 충족 | 부분 충족 | 비어 있음 | 부분 충족 | 이미 충족 | 임상 질문 필터와 수정/철회 연결·일별 데이터 변경. [S-FG12] |
| Cochrane Library PICO Search | 이미 충족 | 부분 충족 | 비어 있음 | 이미 충족 | 부분 충족 | 임상 역할별 부분 입력·PICO 대응; 네 칸 필수 아님, 현재 주석 SLA 별도. [S-FG13] [S-FG14] [S-FG15] |
| Westlaw KeyCite | 비어 있음 | 부분 충족 | 비어 있음 | 이미 충족 | 이미 충족 | 특정 법률 논점의 후속 취급·의존 위험을 표시. [S-FG16] |
| LexisNexis Shepard's | 비어 있음 | 부분 충족 | 비어 있음 | 이미 충족 | 이미 충족 | 인용 이력의 여러 단계에서 온 신호; 판례 전체 진실 보증 아님. [S-FG17] |

**타 분야 열이 대부분 비어 있다는 이유로 이를 제품의 독점 영역으로 삼지 않는다.** EIP의 기술 간 대응은 부분 충족으로 인정한다. 범용 LLM의 요청 가능성과 전용 기능의 문서화는 다르고, AskNature 같은 직접 인접 시스템의 깊은 방법론 조사는 사전 제외했다. 보강 질의 L-X01–04에서도 지정 공식 도메인 밖 연구·2차 자료가 주로 반환되어 엄격한 기능을 새 공식 본문으로 확증하지 못했다. 이 검색 실패는 부재 증명이 아니다. AskNature는 자연의 형태·과정·생태계에서 설계 영감을 얻는 인접 프로그램이라는 위치만 확인했다. [S-X01]

역사적 MAS 행의 부분 능력은 과거 기능 기록이며 현재 선택지로 권고하지 않는다. Software Heritage·npms·Connected Papers의 현재 운영 불명도 기능 설계 문서의 존재와 구분한다. AWS Agent는 preview이고 자원 링크/지침은 범용 외부 OSS 추천과 동일하지 않다. [S-F01] [S-AC23] [S-AC33] [S-DE19] [S-FG22] [S-FG26]

## 2. 반대 가설 A — “범용 LLM 검색이 이미 충분히 한다”

### 지지하는 자료를 의도적으로 찾은 결과

| 탐색 기록 | 찾으려 한 반증 | 확보한 자료와 결과 |
| --- | --- | --- |
| L-DE01·02·25·27 | 문맥/파일·부분 목표·원문 인용·코드 부품이 이미 가능한가 | Perplexity의 문맥·검색 합성, Copilot 선택 파일+지시, Exa 코드 예제를 확인. 넓은 가치의 신규성 주장을 축소 [S-DE01] [S-DE03] [S-DE04] [S-DE12] |
| L-AC13·15·21과 직접 연결 문서 | 코드 검색은 단지 키워드만 받는가 | 자연어+repo scope 및 부분문제→검색→파일/행 설명의 제작자 예제가 있어 부재 가설 기각 [S-AC30] [S-AC31] |
| L-F13·L-F23 및 회고 연결 | 기존 제공자가 같은 가치/잔여 가치를 먼저 경험했는가 | searchcode의 LLM 도구 전환과 Hyperlint의 범용 도구 대체 경험을 확인. Openbase는 수익성 반례이며 LLM 충분성의 직접 증거는 아님 [S-F07] [S-F11] [S-F10] |
| L-FG13·17 | 구조·목표·부분 범위·왜/대가를 함께 제공하는가 | AWS에서 분야가 제한된 구체 기능 확인. 입력/설명 부재 명제를 기각 [S-FG24] [S-FG26] |
| L-X01–04 | 다른 분야 메커니즘을 옮기는 기능도 공식적으로 문서화됐는가 | 새 공식 본문 확보 실패. D0/범위 밖 연구로 확증하지 않았으며 전체 부재를 주장하지 않음 |

정확한 질의 문자열·UTC·반환 결과·열람 ID는 SEARCH_LOG.json에 있다. 이 표의 묶음은 검색 기록을 요약한 것이며 새로 실행한 질의가 아니다.

**판정:** 한 번의 조사, 알려진 기술 범주, 선택 저장소의 일부 구현 이해와 후보 링크 수집에는 이 반대 가설을 배제할 근거가 없다. 오히려 공식 기능이 이를 적극 지지한다. 기준선은 LLM 단독만이 아니라 **LLM + grep.app/Sourcegraph/searchcode + 기존 목록 + 원문 확인**의 조합이어야 한다. “단일 시스템이 다섯 칸을 모두 충족하지 않는다”는 표만으로 조합을 이겼다고 말할 수 없다. [S-AC31] [S-F06] [S-DE04]

충분성의 경계는 현재 과제에서 아직 재지 않은 부분이다. 과거 인용 평가가 무근거 문장·허위 링크·후첨 인용의 위험을 보여 주지만, 현재의 설계 추천이 반드시 실패한다는 실험은 아니다. 반대로 링크를 붙인 제품 소개도 제약 보존·채택 적합성의 증거는 아니다. [S-DE27] [S-DE28] [S-DE29]

**우리 결론이 틀리는 조건 A:** 사전 고정한 실제 과제·허용 오류·검토시간에서 기존 LLM 조합이 새 절차와 동등하거나 더 나으면 H1의 추가 탐색 가치와 별도 조사 UI 필요성은 기각한다. H2의 지속 유지 가치는 변경 후 재검토 과제를 별도로 비교한다. 장기 유지 기능이 없다는 이유로 한 번의 탐색에서 충분한 기준선의 성공을 취소하지 않는다.

## 3. 반대 가설 B — “기존 디렉터리와 awesome 목록이 이미 충분하다”

| 탐색 기록 | 반증 자료 | 판정에 반영한 것 |
| --- | --- | --- |
| L-AC19·20과 기여/metadata 직접 열람 | CC0 분야별 링크, 선정·제외 규칙, 2014 생성→2026 push [S-AC05] [S-AC07] [S-AC37] | 단순 링크 목록도 오래 유지되며, 부품 범주를 아는 사용자에게 탐색 가치가 있음 |
| L-AC01 및 FAQ 직접 열람 | 주목적 중심 대안과 부분 기능 문제·App Type 개선 경로 [S-AC01] [S-AC02] | 목록이 부분 추천을 전혀 못 한다는 명제는 기각. 동시에 자동 구조 매핑을 한다고 확대하지 않음 |
| L-AC03·22와 연결 FAQ | 유료 노출 삽입과 공급자 재검증 [S-AC08] [S-AC09] [S-AC10] | 화면 순서와 적합도 순서를 분리. 목록 전체가 쓸모없다는 근거는 아님 |
| L-FG01·02·19 | 패턴 목록의 상황·대가·구현 링크 [S-FG02] [S-FG03] [S-FG04] | 원리/부분 설명도 카탈로그가 이미 제공할 수 있음 |

**판정:** 범주나 부품명으로 질문을 바꿀 수 있고, 비교 후보 수가 작고, 원문의 대가를 개발자가 읽을 수 있는 경우에는 기존 목록이 충분할 가능성이 높다는 **H**를 채택한다. 링크 수·태그 수만 늘리는 재구축은 우선 검증할 차별성이 아니다. 다만 AlternativeTo의 운영자도 부분 대안의 어려움을 인정하고, awesome의 검토 제한은 사람이 수행하는 비용을 보여 준다. [S-AC02] [S-AC05] [S-AC07]

**권리와 효용을 혼동하지 않는다.** 경쟁 DB 수집 금지는 우리가 데이터를 복제하는 제약이지, 사용자가 직접 그 디렉터리를 써서 충분한 답을 얻는다는 가설의 반증이 아니다. 오래된 항목을 빼는 규칙도 현재 채택 후보에는 합리적일 수 있다. **H:** 종료한 구현에서 참고 원리를 얻으려는 과제에는 과거 자료가 더 필요할 수 있지만, 이것만으로 새 제품의 필요성이 증명되지는 않는다. [S-AC01] [S-AC07] [S-AC24]

**우리 결론이 틀리는 조건 B:** 사전 고정한 실제 목적 문장과 허용 오류·검토시간에서 목록/패턴+개발자의 짧은 번역이 새 절차와 동등하거나 더 나으면 H1의 구조 입력 UI/자동 매핑 가치 가설을 기각한다. 전체 시장의 후보를 빠짐없이 찾을 것을 요구하지 않는다. H2의 변경 후 유지 가치는 별도 과제로 판단하고, 링크 개수만으로 승리를 정하지 않는다.

## 4. 다시 만들 필요가 없는 부분과 재사용 조건

| 재구축을 기본값으로 삼지 않을 부분 | 이미 있는 것 | 가져올 때 남는 일 |
| --- | --- | --- |
| 제품·프로젝트 이름의 일반 목록 | 디렉터리·CC0 목록 [S-AC04] [S-AC05] | 적법한 목록만 사용; 새 설계의 관련 부분과 대응 검증 |
| 패키지·버전·의존성·repo 식별 | deps.dev·ecosyste.ms·Libraries.io [S-AC12] [S-AC15] [S-AC35] | 원천/버전/환경·권리·갱신 조건, 기존 defer 유지 |
| 범용 코드 전역 색인 | GitHub Blackbird·Zoekt·grep.app [S-AC25] [S-AC28] [S-AC31] | 필요한 범위/리비전·누락·접근 조건을 선택 |
| 지정 repo의 구조 설명 | DeepWiki·searchcode [S-DE07] [S-F06] | 최초 후보 발견과 목표 적합성 판단 |
| 파일 문맥+자연어 조사 UI | Copilot Spaces·Perplexity [S-DE04] [S-DE03] | 기존 조합보다 줄어드는 실제 검토 비용 측정 |
| 학술 논문 추천·구현/벤치마크 연결 | S2 추천 API·PWC [S-DE14] [S-F12] [S-F13] | 약관/데이터 라이선스와 현재 재구현 상태 |
| 부분 설계 패턴 설명 | EIP·microservices·Azure [S-FG02] [S-FG04] [S-FG05] | 허용된 항목의 출처 표시·적용 맥락 검증 |
| 원문/버전 식별·후속 위험 표시의 기본 원리 | SWH·S2 diff·PubMed·citator [S-AC24] [S-DE14] [S-FG12] [S-FG16] | 우리 근거 단위에 어떤 변경이 재검토를 유발하는지 실험 |

이는 스택·API 채택 확정이 아니다. 공개 코드·API 존재는 사용 권한, 전체 데이터 수출 허가, 우리가 원하는 유지 약속의 증거가 아니다. 필요한 최소 범위부터 조건을 확인하는 재사용 우선순위다.

## 5. 남은 가설과 반증 가능한 다음 연구

### H1. 목적·부분·제약과 후보의 대응 기록

새 후보가 어느 부분을 대신하거나 참고하게 하는지, 어떤 필수 제약을 만족/위반하는지, 근거가 어디인지 한 결정 단위로 기록하면 검토가 빨라질 수 있다. 그러나 Elicit·AWS·grep.app 조합이 이미 이를 충분히 제공할 수 있으므로 새 기능 자체가 독자적이라는 주장은 하지 않는다. [S-DE22] [S-FG24] [S-AC31]

### H2. 제공자가 바뀌어도 이어지는 근거의 재검토

원문 버전·인용 위치·권리·후속 변경과 “이 추천 이유가 아직 성립하는가”를 연결하는 절차에 잔여 가치가 있을 수 있다. SWH·S2·citator·ResearchRabbit는 이 중 여러 부분을 이미 해결한다. 남은 것은 서로 다른 제공자의 특정 목표 판단을 연결하는 비용 차이다. [S-AC24] [S-DE14] [S-FG16] [S-DE25]

### H3. 별도 제품보다 기존 작업 도구의 작은 절차가 적절할 수 있음

Hyperlint는 추가 UI·설치·알림 비용을 직접 설명하고, searchcode의 재출발은 도구의 소비자·배포 경로·수익 모델 전환을 보여 준다. **H:** 동일한 근거 장부를 기존 에이전트/문서/PR 작업에 얹는 것이 별도 검색 서비스보다 충분할 수 있다. 이 문서는 구현·배포나 수익 모델을 결정하지 않는다. [S-F10] [S-F07]

**다음 첫 행동:** 합성 문제가 아닌 실제 공개 프로젝트의 설계 결정 자료에서 작은 사례 집합을 먼저 고정하고, 정답을 미리 알고 고르지 않은 채 두 기준선(A: 범용 LLM+기존 도구, B: 목록/패턴+개발자 검토)을 같은 시간·같은 공개 자료 조건으로 비교할 프로토콜을 작성한다. 측정은 링크 개수보다 필수 제약 누락, 적합 후보, 특정 근거의 지지, 판정 수정 횟수, 검토 시간으로 나눈다. 아직 이런 D4 비교를 실행한 것처럼 보고하지 않는다.

## 6. 가장 강한 약점 3개

1. **문서상 기능과 실제 충분성 사이가 비어 있다.** 현재 조합이 실제 설계 과제에서 잘하는지 못하는지 이 연구만으로 확정할 수 없다. 그러므로 기능 목록의 공백을 성능 우위로 바꾸지 않는다.
2. **타 분야 원리 열은 조사 범위의 영향을 크게 받는다.** 유추 전문 시스템의 깊은 조사를 제외했고 추가 공식 질의도 확증을 못 했다. 따라서 가장 신규적으로 보이는 칸을 제품의 독점 근거로 쓰지 않는다.
3. **운영·권리·유지의 안정성을 제작자 문서로만 본다.** 겉으로 같아 보이는 API나 소유자가 바뀔 수 있고 일부 조건은 모순되거나 불명이다. 확인 가능한 선택 범위로 줄이거나 후속 계약/실행 확인이 필요하다.

## 한계

“비어 있음”은 이번 D1 문서에서 확인한 기능 범위의 빈칸이다. 존재하지 않음을 실험한 결과가 아니다. 계정·유료 호출·공개 제품의 P1/P2/P03 질의는 실행하지 않았고, 과거 평가 수치를 현재 성능으로 쓰지 않았다. 유지 요소를 충족한 시스템도 모든 주장 진실성·전수 링크 생존을 보증하지 않는다. 반증 조건은 다음 연구에서 판단할 기준이며 이번에 달성한 수치가 아니다.

## 출처 링크

[S-DE04]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/copilot-spaces/create-copilot-spaces
[S-AC30]: https://sourcegraph.com/docs/code-search/query-assist
[S-AC31]: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp
[S-F06]: https://searchcode.com/
[S-DE12]: https://exa.ai/blog/exa-code
[S-FG04]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/
[S-DE21]: https://support.elicit.com/en/articles/14759154-systematic-reviews-in-elicit
[S-FG14]: https://assets.wiley.com/image/upload/v1786361551/how-to-use-pico-search-updated-2023.pdf?_s=public-apps
[S-FG16]: https://www.thomsonreuters.com/en-us/help/drafting-assistant/westcheck/keycite-status-flags
[S-AC02]: https://alternativeto.net/faq/
[S-AC03]: https://openalternative.co/about
[S-AC04]: https://github.com/piotrkulpinski/open-source-alternatives
[S-AC05]: https://github.com/sindresorhus/awesome
[S-AC07]: https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md
[S-AC37]: https://api.github.com/repos/sindresorhus/awesome
[S-AC08]: https://www.saashub.com/about
[S-AC09]: https://www.saashub.com/featured-products
[S-AC10]: https://www.saashub.com/faq.html
[S-AC11]: https://support.tidelift.com/for-subscribers/references/understanding-the-difference-between-data-from-libraries-io-and-the-tidelift-subscription/
[S-AC12]: https://zenodo.org/records/1196312
[S-AC14]: https://docs.deps.dev/faq/
[S-AC15]: https://docs.deps.dev/api/v3/
[S-AC19]: https://docs.ecosyste.ms/docs/usage/
[S-AC20]: https://docs.ecosyste.ms/docs/usage/licences/
[S-AC35]: https://docs.ecosyste.ms/docs/services/data-services/repositories/
[S-AC16]: https://ossinsight.io/docs/about
[S-AC17]: https://ossinsight.io/docs/faq
[S-AC18]: https://ossinsight.io/explore
[S-AC23]: https://github.com/SoftwareHeritage/swh-model
[S-AC24]: https://upsilon.cc/~zack/research/publications/ipres-2017-software-heritage.pdf
[S-AC33]: https://github.com/npms-io/npms-analyzer
[S-AC34]: https://github.com/npms-io/queries
[S-AC36]: https://github.com/npms-io/npms-analyzer/blob/master/docs/architecture.md
[S-AC25]: https://github.blog/engineering/the-technology-behind-githubs-new-code-search/
[S-AC26]: https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax
[S-AC27]: https://docs.github.com/en/search-github/github-code-search/about-github-code-search
[S-AC28]: https://sourcegraph.com/docs/admin/search
[S-AC29]: https://sourcegraph.com/docs/code-search
[S-AC32]: https://grep.app/
[S-DE01]: https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search
[S-DE02]: https://www.perplexity.ai/changelog/shared-workspaces-personal-computer-for-windows-and-model-council
[S-DE03]: https://www.perplexity.ai/en-GB/hub/products/deep-research
[S-DE05]: https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing
[S-DE06]: https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/use-copilot-spaces
[S-DE07]: https://docs.devin.ai/work-with-devin/deepwiki
[S-DE08]: https://github.com/CognitionAI/deepwiki
[S-DE09]: https://docs.devin.ai/work-with-devin/ask-devin
[S-DE10]: https://exa.ai/docs/reference/search
[S-DE11]: https://exa.ai/blog/building-web-scale-vector-db
[S-DE14]: https://webflow.semanticscholar.org/product/api/tutorial
[S-DE15]: https://aclanthology.org/2020.acl-main.207.pdf
[S-DE16]: https://webflow.semanticscholar.org/product/api/license
[S-DE18]: https://medium.com/connectedpapers/announcing-connected-papers-a-visual-tool-for-researchers-to-find-and-explore-academic-papers-89146a54c7d4
[S-DE19]: https://medium.com/connectedpapers/announcing-premium-accounts-multi-origin-graphs-and-more-92e8dbd66848
[S-DE20]: https://elicit.com/solutions/search
[S-DE22]: https://elicit.com/solutions/reports
[S-DE23]: https://learn.researchrabbit.ai/en/articles/12454660-how-researchrabbit-builds-and-ranks-your-map
[S-DE24]: https://learn.researchrabbit.ai/en/articles/12454605-the-researchrabbit-database
[S-DE25]: https://learn.researchrabbit.ai/en/articles/15888747-exploring-article-risk-with-signals-indicators
[S-DE26]: https://learn.researchrabbit.ai/en/articles/12454495-what-is-researchrabbit
[S-F01]: https://www.microsoft.com/en-us/research/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/
[S-F02]: https://www.microsoft.com/en-us/research/project/academic/
[S-F12]: https://github.com/huggingface/paperswithcode
[S-F13]: https://github.com/paperswithcode/paperswithcode-data
[S-F14]: https://www.linkedin.com/feed/update/urn:li:activity:7354483119762153472/
[S-FG01]: https://microservices.io/patterns/
[S-FG02]: https://microservices.io/post/architecture/2023/03/13/better-decision-making-with-patterns.html
[S-FG03]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html
[S-FG05]: https://learn.microsoft.com/en-us/azure/architecture/patterns/
[S-FG06]: https://www.thoughtworks.com/radar/faq
[S-FG19]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/tutorial.html
[S-FG22]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent.html
[S-FG24]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-architecture-reviews.html
[S-FG26]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-view-rec.html
[S-FG07]: https://support.google.com/faqs/answer/7049475?hl=en
[S-FG08]: https://support.google.com/faqs/answer/7049724?hl=en
[S-FG09]: https://support.google.com/faqs/answer/7049585?hl=en
[S-FG10]: https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/classification/cpc
[S-FG11]: https://www.epo.org/en/learning/learning-resources-profile/business-and-ip-managers/inventors-handbook/novelty-and-prior-art
[S-FG12]: https://pubmed.ncbi.nlm.nih.gov/help/
[S-FG13]: https://www.cochrane.org/about-us/news/try-new-cochrane-pico-search-beta-cochrane-library
[S-FG15]: https://help.cochrane.org/kb/article/27-how-can-i-access-cochrane-evidence/
[S-FG17]: https://www.lexisnexis.com/en-us/support/lexis/faqs/shepards-signal-indicators.page
[S-X01]: https://asknature.org/about/
[S-F07]: https://boyter.org/posts/searchcode-has-been-rebooted/
[S-F11]: https://www.linkedin.com/posts/liorgrossman_today-i-am-writing-to-share-that-weve-made-activity-7051208392559771648-etA3
[S-F10]: https://billchambers.me/articles/hyperlint-post-mortem/
[S-DE27]: https://aclanthology.org/2023.findings-emnlp.467.pdf
[S-DE28]: https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
[S-DE29]: https://aclanthology.org/2023.emnlp-main.398.pdf
[S-AC01]: https://alternativeto.net/about/terms/
