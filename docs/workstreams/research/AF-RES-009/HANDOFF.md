# AF-RES-009#1 — HANDOFF

## 1. 식별

- 작업 ID/시도: **AF-RES-009#1**.
- 작업 종류: codex-cloud의 공개 문헌 연구 및 GitHub 커밋.
- 실행 위치/모델: 공유 Linux workspace, 세션에 표시된 GPT-6 Astra Pro. 내부 분담은 같은 작업의 별도 조사·검토이며 사람/외부 모델 검토로 부르지 않는다.
- 공개 작업자 참조: AF-RES-009#1 / work/research-af-res-009. 별도 비공개 작업 조회 ID는 제공되지 않았다.
- 역할: 선행 시스템 지형·실패·재사용·반증 조사. 제품 구현·배포·최종 검색 스택 결정 아님.
- 저장소: laadkke-arch/agentflow-open.
- 브랜치: **work/research-af-res-009**.
- source_commit: **50ebddbc28a756a4c886184d0f56a0f648e19145**.
- 인계 작성 직전 마지막 확인/원격 저장 SHA: **7f90451417e99b38160fce1b5412b200da70afd6**. 원격 SELF_CHECK.md를 다시 읽어 로컬 본문과 같음을 확인했다.
- 최종 결과 커밋: **이 HANDOFF.md만 담은 마지막 커밋**. 본문 안에 자신의 커밋 SHA를 만들지 않고 Git 기록으로 식별한다.
- 마지막 실제 검사 증거: 2026-11-20T05:02:02.017056Z, audit.py pre-handoff **PASS, 종료 코드 0, 886개 형식·참조·범위 검사**. 검사 당시 HEAD 08523204e9cb28fed275dd4dbfaeda197ada27f5; 당시 작업 파일의 SHA-256은 VERIFICATION.json에 있고 이후 자기점검 커밋에 포함됐다.
- 인계 작성 확인 시각 UTC: 2026-11-20T05:04:13Z.
- PR: 만들지 않았다. 요청된 작업 브랜치의 묶음별 원격 커밋까지 수행했다.
- 상태: **REVIEW_READY**. 문서 연구 완료이며 새 제품의 성능·지불 가치 확인 상태는 아니다.

### 읽은 기준 SHA와 범위

| 역할 | 고정 SHA | 직접 읽은 파일 |
| --- | --- | --- |
| 시작 규칙·배정 | 50ebddbc28a756a4c886184d0f56a0f648e19145 | AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, docs/automation/dot-control.json의 AF-RES-009, docs/product/RESEARCH_BRIEF.md 및 시작/인계 규칙 |
| AF-DOT-001 | ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea | HANDOFF.md, REVIEW.md §2 |
| AF-RES-002 | 62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1 | HANDOFF.md, METHODS.md, PROTOCOL.md §2·3 |
| AF-RES-004 | 2b798c7d2b7355b649691c18de196104ceabb0f0 | HANDOFF.md, CASES.json의 P03 |

앞선 고정 입력은 통합 브랜치의 현재 파일로 대체하지 않고 지정 result_commit에서 읽었다. 기존 네 후보의 역할과 방법 문헌 제외 범위를 유지했다. [I-DOT] [I-METHODS] [I-PROTOCOL] [I-CASES]

### 묶음별 원격 커밋

| 묶음 | SHA |
| --- | --- |
| 1. 조사 전 SCOPE | 53e612b596a009ddb49d61fe7e9e713a5a6ced55 |
| 2. a–c 시스템·원장·질의 | fa01814fc6bfbb1d6504f3652a5f9b46a13f8647 |
| 3. d–g 시스템·원장·질의 | 9c29d9dc0d8f57c69f8ec1669ab8c012886fa386 |
| 4. 실패·중단·전환 | 64e0503930b42b2c54b37a4b43ba2ea30e9739f0 |
| 5. LANDSCAPE·GAP 및 판정 | 08523204e9cb28fed275dd4dbfaeda197ada27f5 |
| 6. SELF_CHECK·검증 | 7f90451417e99b38160fce1b5412b200da70afd6 |
| 7. HANDOFF 단독 | 이 파일을 추가한 최종 커밋; 원격 재열람과 final audit로 확인 |

각 묶음 직후 GitHub tree/commit/ref 갱신으로 원격에 저장했다. 마지막에 한 번에 올린 작업이 아니다.

## 2. 사용자 요구와 작업 범위

목표는 설계의 전체/일부와 목적에서 유용한 오픈소스·서비스·부품·참고 원리로 가는 기존 시스템을 비교하고, 다시 만들지 않을 부분과 남은 가설을 분리하는 것이다. 제품 기준은 시작 SHA의 [RESEARCH_BRIEF.md](https://github.com/laadkke-arch/agentflow-open/blob/50ebddbc28a756a4c886184d0f56a0f648e19145/docs/product/RESEARCH_BRIEF.md)다.

쓰기 경로는 **docs/workstreams/research/AF-RES-009/**만 사용했다. dot-control.json·공통 색인/계약·제품 코드·기존 Studio·main을 수정하지 않았다. AF-RES-010~012의 결과는 읽거나 기다리지 않았다. 계정·로그인·유료 API·권한 변경·배포·상시 수집·비공개 자료 수집은 수행하지 않았다.

## 3. 실제 산출물

| 파일 | 변경 내용 | 확인 |
| --- | --- | --- |
| SCOPE.md | 조사 전 질문·범주·후보·제외·판정·질의 원칙 고정 | 첫 커밋으로 선행 보존 |
| sources.json | 외부 원문108 + 고정 내부 입력4, 출처별 확인/한계·D1·used_in, 제외51기록, 실패 사건 원장 | ID·URL·필수필드·상한·참조 검사 |
| SYSTEMS.json | 시스템35, 범주 a4/b6/c4/d4/e6/f5/g6, 필수 필드와 5요소 판정 | 행마다 직접 읽은 1차 출처 |
| SEARCH_LOG.json | 정확한 탐색 질의101, UTC·도구·본 결과·열람 source 연결 | 중복·누락·참조 검사 |
| LANDSCAPE.md | Q1–Q5/Q7 비교, 수집/권리/표현/설명/전문분야·재사용 조건 | 내부 별도 검토·주요 원문 재열람 |
| FAILURES.md | 종료·부분 중단·전환7건, 추가3건·반대 사례, 공식 이유와 H | 1차 본문·날짜·사건 범위·짧은 인용 |
| GAP.md | 35시스템×5요소, 두 반대 가설, 재구축 불필요 후보, 기각 조건 | 강한 기존 조합 인정; 완전검색 요구 제거 |
| SELF_CHECK.md / SELF_CHECK.json | Q1–Q8의 답·출처 종류·반증·불확실성·최소 추가 확인 | 모든 행 출처2종류 이상 |
| REVIEW.md | 내부 별도 검토 지적과 수정 | 효과 시험·외부/사람 검토로 오표기하지 않음 |
| audit.py / VERIFICATION.json | 문서/참조/개수/경로/커밋 검사와 내용 hash | pre-handoff PASS; final은 인계 커밋 후 읽기 전용 실행 |
| HANDOFF.md | 이 인계와 다음 첫 행동 | 자기점검 통과 후 마지막 단독 커밋 |

## 4. Q1–Q8 결론과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계 |
| --- | --- | --- |
| Q1 | 넓은 가치는 7범주와 기존 조합이 상당 부분 제공한다. [S-AC31] [S-DE04] [S-FG03] | 지형 선정은 전수 시장 조사나 사용자 성공률이 아님 |
| Q2 | 부분 파일·자유문·역할/분류·카탈로그 대조 등 여러 입력이 있고 완전 양식은 일반적 필수조건이 아니다. [S-DE04] [S-FG14] [S-FG11] | 입력을 받음과 정확히 이해함은 별개; 분자 구조 검색을 일반 설계 해석으로 확대하지 않음 |
| Q3 | 수집/갱신·코드/데이터/본문/API 조건을 분리해야 한다. [S-AC12] [S-AC15] [S-DE16] [S-DE17] | 구판 라이선스·공개 열람으로 현재 전체 DB 권리를 확정하지 않음 |
| Q4 | 그래프·색인·분류·패턴은 다른 관계를 보존한다. [S-AC25] [S-DE15] [S-FG03] | 역사 모델을 현행 전체 구현과 동일시하지 않음 |
| Q5 | 링크 존재·문장 지지·부분 도움 이유·후속 변화는 다른 검증 대상이다. [S-DE22] [S-DE27] [S-DE28] [S-DE29] | 2023/2025 수치를 2026 개발 추천 오류율로 쓰지 않음 |
| Q6 | 7건의 중단·전환은 수익·기회비용·비용·기술/팀 등 원인이 다르다. [S-F01] [S-F05] [S-F09] [S-F11] | 공식 원인 진술은 독립 손익/인과 감사가 아님; PWC 이유 미공개 |
| Q7 | 부품·패턴·구현 연결은 이미 있으며 EIP의 기술 간 대응도 일부 존재한다. [S-AC31] [S-F06] [S-FG03] [S-FG04] | 더 넓은 원리 전이의 시장 부재는 입증하지 못함; AskNature는 위치만 확인 |
| Q8 | 일반 목록·식별·검색·문맥 UI의 재구축보다 기존 조합 대비 추가 검토/유지 가치부터 시험해야 한다. [S-DE04] [S-AC31] [S-F10] | 신규성·성능 우위·지불 가치는 여전히 H이며 제품화 결정 아님 |

### 가장 강한 근거 3개

1. **grep.app의 공식 MCP 예제 [S-AC31].** 부분 오류 처리 문제를 코드 검색에 옮기고 파일·행과 설명으로 답하는 실제 제작자 예제다. 부품 연결·링크 설명의 일반적 부재를 직접 반박한다. 이 연구의 D3 실행은 아니다.
2. **AWS architecture reviews [S-FG24].** IaC·목표·일부 pillar/item 범위를 받는 구체적 인터페이스가 있다. 구조·목표·부분 범위 결합 자체의 신규성을 반박한다. preview·AWS 환경 안의 기능이며 외부 OSS의 범용 발견과 구별한다.
3. **Microsoft Academic 공식 종료 FAQ [S-F01].** 풍부한 개체·관계·의미검색에도 종료할 수 있고, 운영비가 아닌 기회비용이라는 이유가 명시된다. “구조가 풍부하면 지속”과 “모든 중단은 유지비”를 함께 반박한다.

### 다시 만들 필요가 없는 부분

일반 제품 목록, 패키지/버전/의존 식별, 범용 코드 색인, 지정 repo의 구조 설명, 파일 문맥 조사 UI, 논문 추천/구현 연결, 기본 패턴 카탈로그, 원문/버전 식별의 기본 원리는 기존 자료·도구가 제공한다. 가져올 조건은 LANDSCAPE §7/GAP §4에 분리했다. 최종 DB/API/검색 스택을 지정하지 않았다.

## 5. 실제 검증·미실시·약점

### 완료한 검사

- 외부 원문108개를 직접 열어 관련 본문을 읽었다. 시스템당 전체 사이트를 합쳐 최대3개로 보수적으로 제한하여 **95개**를 최소 수에 산입했다.
- 공식 문서 태그77개, 명확한 공학 글/원논문 지정9개, 서로 다른 시스템의 1차 실패 원문 지정6개, 생성형 평가 원문3개를 확보했다.
- 범주별 최소3개·전체35개·모든 시스템의 1차 출처·질문별2종류와 반증 기록·출처/검색 참조·판정표·owned_path와 control 불변 검사를 통과했다.
- 초기 검사기의 Git 상태 앞 공백 처리 오류를 고치고 재실행했다. 내용 진실성·효과와 문서 무결성 검사를 구별했다.
- SELF_CHECK.md 원격 본문은 자기점검 커밋에서 로컬과 일치했다. 이 HANDOFF의 원격 본문 재열람은 단독 커밋 뒤 수행하며, 그 확인을 위해 인계 파일을 다시 수정하지 않는다.

재현 명령 — 저장소 루트에서, 기본 입력은 이 브랜치의 JSON/Markdown과 source_commit이다:

```bash
python docs/workstreams/research/AF-RES-009/audit.py --stage final
git diff --name-only 50ebddbc28a756a4c886184d0f56a0f648e19145 HEAD
git status --porcelain
```

실제 pre-handoff 검사와 출력은 VERIFICATION.json에 보존했다. 최종 검사는 HANDOFF 단독 커밋·로컬/원격 일치·clean worktree와 원장 hash 불변까지 추가로 확인한다.

### 미실시와 그 의미

외부 자료는 모두 D1이다. D2 고정 실행 코드 검증, 선택적 Q7의 P1/P2/P03 공개 제품 질의, D3 결과 순위, D4 목표 과제 성공률은 만들지 않았다. 계정·유료 호출 없이 가능한 문헌 조사 필수 검사는 수행했으므로 직접 못한 필수 실행 때문에 막힌 작업은 없다. 제품 빌드·런타임 검사는 이번 문서 연구의 효과 증거가 아니어서 수행하지 않았다.

선택적 Q7을 후속으로 추가한다면 입력을 재구성하지 말고 다음 고정 파일의 원문을 읽는다:

```bash
git show 62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1:docs/workstreams/research/AF-RES-002/PROTOCOL.md
git show 2b798c7d2b7355b649691c18de196104ceabb0f0:docs/workstreams/research/AF-RES-004/CASES.json
```

PROTOCOL §2/3의 P1/P2와 CASES P03 문장을 그대로 입력한다. 로그인 없는 공개 시스템에만 시스템당 최대3질의, 실제 UTC·화면의 상위 항목/URL·설명 여부를 D3로 기록한다. 이 명령은 입력 확인이며 이미 서비스 질의를 실행했다는 뜻이 아니다.

### 우리 결론이 틀릴 수 있는 지점 3개

1. 기존 LLM+목록+코드 도구 조합이 사전 고정한 실제 과제·허용 오류·검토시간에서 새 절차와 동등하거나 더 나으면 **H1 추가 탐색 가치**를 기각한다. 장기 유지가 없다는 이유로 그 탐색 성공을 취소하지 않는다.
2. 유추 전문 시스템을 깊게 조사하지 않았고 보강 질의4개도 공식 기능을 확증하지 못했다. 타 분야 원리의 미확인 칸을 신규 시장의 증거로 쓰면 결론이 틀릴 수 있다.
3. 문서상 갱신·권리·운영 모델은 실제 SLA·손익·효용을 대신하지 못한다. 의미 있는 유지 가치는 **H2 변경 후 재검토 과제**로 별도 확인해야 하며, 기존 방법이 동등 이상이면 그 가설도 기각한다.

## 6. 색인 변경 제안 — 적용하지 않음

| 작업 | 제안 상태·결과 위치 | 요약·다음 연결 |
| --- | --- | --- |
| AF-RES-009#1 | REVIEW_READY; work/research-af-res-009의 HANDOFF 단독 최종 커밋; docs/workstreams/research/AF-RES-009/ | 35시스템·95산입 원문·종료/부분중단/전환7건. PLAN#1 scope/maintenance는 기존 조합 기준선과 별도 탐색/유지 가치 검증에서 시작 |

dot-control.json과 공통 색인은 담당자만 위 제안을 반영하도록 남겼으며 이 작업에서 고치지 않았다.

## 7. 다음 첫 행동

1. 작업 브랜치 최신 SHA와 HANDOFF를 다시 읽고, final audit를 읽기 전용으로 실행한다.
2. **실제 공개 프로젝트의 설계 결정 자료로 작은 사례 집합을 고정하는 비교 프로토콜**을 먼저 작성한다. 기존 합성 문제 결과를 다시 늘리는 대신, 후보를 미리 알고 선택하지 않은 실제 목적 문장을 사용한다.
3. 기준선 A는 범용 LLM+기존 코드/목록 도구 조합, 기준선 B는 목록/패턴+개발자 검토다. 같은 공개 자료·시간 조건에서 제약 누락·적합 후보·원문 지지·검토 시간으로 H1을 비교한다. H2는 근거가 바뀐 뒤 재검토 과제로 분리한다.
4. 이 작업의 미해결 차단·추가 승인 요청은 없다. 다음 실험의 새 과제/접근 범위는 후속 작업에서 정하며, 현재 결과가 새 유료 API·로그인·배포·상시 수집을 승인하는 문서는 아니다.

새 세션이 이 파일과 고정 SHA를 자동으로 기억하는 것으로 가정하지 않는다.

## 출처 링크

[I-DOT]: https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/REVIEW.md
[I-METHODS]: https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/METHODS.md
[I-PROTOCOL]: https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/PROTOCOL.md
[I-CASES]: https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/CASES.json
[S-AC31]: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp
[S-DE04]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/copilot-spaces/create-copilot-spaces
[S-FG03]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html
[S-FG14]: https://assets.wiley.com/image/upload/v1786361551/how-to-use-pico-search-updated-2023.pdf?_s=public-apps
[S-FG11]: https://www.epo.org/en/learning/learning-resources-profile/business-and-ip-managers/inventors-handbook/novelty-and-prior-art
[S-AC12]: https://zenodo.org/records/1196312
[S-AC15]: https://docs.deps.dev/api/v3/
[S-DE16]: https://webflow.semanticscholar.org/product/api/license
[S-DE17]: https://api.semanticscholar.org/license/
[S-AC25]: https://github.blog/engineering/the-technology-behind-githubs-new-code-search/
[S-DE15]: https://aclanthology.org/2020.acl-main.207.pdf
[S-DE22]: https://elicit.com/solutions/reports
[S-DE27]: https://aclanthology.org/2023.findings-emnlp.467.pdf
[S-DE28]: https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
[S-DE29]: https://aclanthology.org/2023.emnlp-main.398.pdf
[S-F01]: https://www.microsoft.com/en-us/research/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/
[S-F05]: https://boyter.org/posts/searchcode-is-being-rebooted/
[S-F09]: https://web.archive.org/web/20221122101021/https://www.kite.com/blog/product/kite-is-saying-farewell/
[S-F11]: https://www.linkedin.com/posts/liorgrossman_today-i-am-writing-to-share-that-weve-made-activity-7051208392559771648-etA3
[S-F06]: https://searchcode.com/
[S-FG04]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/
[S-F10]: https://billchambers.me/articles/hyperlint-post-mortem/
[S-FG24]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-architecture-reviews.html

