# AF-RES-010 — 인계

## 상태

**연구 완료. SELF_CHECK 통과 후 이 파일을 마지막 단독 커밋으로 작성한다.** 배경 본문 47개와 Q5 후보 본문 24개를 별도로 읽고 기록했으며, 일반 웹 64개 고유 질의와 AskNature 공개 검색을 실행했다. 후보 본문 24개는 사용 방식별 25개 T 판정으로 연결했다. 새 출발 분야 관계는 보수적으로 **7개 원리군(P1 4, P2 3)**이며, 표면 오탐 8개와 필수 조건을 깨는 근접 오답 3개도 남겼다.

이 완료는 연구·검색 기록·설명 작성의 완료다. 새 소프트웨어 알고리즘 7개의 발명, 표현별 정밀도 우위, P1/P2 구현 성공을 뜻하지 않는다. AskNature의 계획 질의 16개 중 15개는 결과 또는 빈 결과를 확인했고, 전체 원문 1개는 결과 갱신 실패로 판정에서 제외했다. 재확인 1회와 control 1회를 포함한 native 기록은 18개다.

- 저장소/브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-010`
- 작성일: 2026-11-20. 실행 원장의 시각은 UTC.
- 쓰기 경로: `docs/workstreams/research/AF-RES-010/`만.
- dot-control, 공통 색인·계약, 제품 코드, 기존 AgentFlow Studio, main을 수정하지 않았다. AF-RES-009·011·012 결과를 읽거나 기다리지 않았다.

## 1. 읽은 SHA와 고정 입력

| 용도 | SHA / 실제로 읽은 범위 |
| --- | --- |
| source_commit | `1eca580bf9ddc153f7c9691e30bd727eb7d0ce06` — 시작 시 `chore/workspace-foundation` 최신 SHA. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF, START_HERE, CLOUD_WORKFLOW, dot-control의 AF-RES-010 항목. 작업 브랜치 부재를 확인하고 여기서 생성. |
| AF-RES-002 | `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` — HANDOFF; PROTOCOL §2·§3; RESEARCH §3·§5; METHODS; evidence/p1.json·p2.json·methods.json의 queries. |
| AF-RES-004 | `2b798c7d2b7355b649691c18de196104ceabb0f0` — HANDOFF; PROTOCOL의 T축; RESEARCH §5; EXPECTED R11·R12·R17. |
| 재탐색 전 고정 | `ebcca564df68377cc116634dcdab1695be69c0e8` — SCOPE의 원문·조건·질의 작성 규칙·수·검색/판정 절차. 정확한 64문자열이 이 커밋에 있었다고 주장하지 않는다. |
| SELF_CHECK 커밋 | `8fc5fff6057cfa9133881ac038f6646883416d93` — 문헌/검색/판정·내부 검토·검사 기록을 포함한 인계 직전 커밋. 이 SHA에서도 33개 검사를 재실행해 통과했고 작업 트리는 깨끗했다. |
| 최종 계약 검사에서 관측된 통합 SHA | `020c8d002cf782079053441368ed3e4a95b3289f` — `workbench.session check --fetch`가 계약·경로 검사용으로 참조. 시작 source_commit을 바꾸거나 다른 신규 작업 결과를 읽은 것이 아니다. 계약 SHA-256은 시작과 같은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`. |

P1/P2 원문과 필수 조건은 [SCOPE.md](SCOPE.md)에 글자 단위로 보존했다. T축의 `not_needed / mapped / analogy_only / unknown`과 판정 단위는 변경하지 않았다. 기존 SOLVENT/focused abstraction은 인용만 했고, 기존 Reflow·SQLite·TreeDB·NASA 전이 표 및 Reactive Streams·Toyota JIT·CT Merkle 판정을 새 사례로 세거나 재분석하지 않았다.

## 2. 세부 질문별 결론과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계·근거 위치 |
| --- | --- | --- |
| Q1 표현 | 원문 조건을 보존하고 기능·흐름, 인과 관계, 모순, 분야 대응어를 검색용 부분 표현으로 병기해야 한다. | 7체계를 원문 비교하고 각각 P1/P2 조건을 부호화했다. FB의 Store는 원형에서 signal 저장을 허용하지 않으므로 R1은 소프트웨어 확장 H다. 어떤 체계도 멱등성·수정 보존을 자동 보증하지 않는다. [REPRESENTATIONS](REPRESENTATIONS.md), R01–R09. |
| Q2 시스템 | AskNature, IDEA-INSPIRE, DANE, BioTRIZ, InnoGPS, 목적/메커니즘 검색과 특허 기능 검색은 서로 다른 표현·평가 단위를 사용한다. | 규모·정밀도·아이디어 수·현재 공개 동작을 분리했다. AskNature만 이번 분야 검색에서 직접 실행했고, 다른 도구의 설명 페이지·로그인 링크를 운영 성공으로 세지 않았다. [REPRESENTATIONS](REPRESENTATIONS.md), R10–R20·O01. |
| Q3 실증 | 먼 유추는 일부 조건에서 새로움을 높였지만, 다른 거리 조작·인지 상태에서는 성과를 낮췄고 고착도 유발했다. | E01의 far>near 새로움 d=.56과 E02의 far<near 최대 새로움 d=−.82를 함께 보고한다. 조작·측정이 달라 단순 합성하지 않는다. E13/E16은 일부 표본이 겹치며 독립 재현이 아니다. 개발자 정보 탐색 E12는 원거리 원리 검색의 수요를 직접 입증하지 않는다. [EVIDENCE](EVIDENCE.md). |
| Q4 실제 전이 | 9개 원저자 저작물에서 10개 소프트웨어 전이를 확인했고 관계·연결·실패 조건을 T 형식으로 적었다. | 생물·역학, 제조, 금융·회계 등과 안전·비상 대응·물리를 포함한다. T04의 두 패턴은 2사례·1저작물이다. 저자의 실험·운영 보고 D1을 이번 연구의 재실행으로 올리지 않았다. [TRANSFER_CASES](TRANSFER_CASES.md). |
| Q5 재탐색 | 64개 고유 웹 질의와 실제 AskNature 제출에서 후보 본문24개·사용 방식25개를 판정했다. | AskNature 15/16만 유효 관측이고 P2 R0의 본문 열람은 0이다. 열지 않은 결과는 오탐·후보 부재로 세지 않는다. [SEARCH_LOG](SEARCH_LOG.json), [sources](sources.json), 두 문제의 판정 JSON. |
| Q6 표현 비교 | 새 후보는 P1 4개/P2 3개 원리군이지만 기능·모순·분야 표현 모두 오탐 또는 근접 오답을 만들었다. | 표현별 (a)합9는 전체 고유7과 다르다. 언어·길이·메커니즘 힌트·읽기 예산이 달라 표현 우열/정밀도/recall로 일반화하지 않는다. [RETRIAL §2–4](RETRIAL.md), [comparison-counts](evidence/comparison-counts.json). |
| Q7 최소 설명 | 원 관계와 대상 관계, 연결 조건, 깨지는 입력, 원 분야 입증 수준을 결과 옆에 함께 적어야 한다. | 실제 원리군 7개의 설명을 작성했다. 시간·규모·사람·참값 가정을 보충했지만 T축은 다시 설계하지 않았다. 설명의 판단 개선 효과를 설계자 실험으로 측정하지 않았다. [RETRIAL §5–6](RETRIAL.md). |
| Q8 비용 | 수요가 있는 부분 문제에서 유망 후보만 깊게 설명하는 작은 운영 방식이 타당한 H다. | DANE의 40–100시간/깊은 모델·불완전 기여는 전량 인과 주석의 반례다. 교육 가격·무료 열람·크라우드 중앙값을 전체 구축 원가로 바꾸지 않았다. 이 프로젝트의 시간·FTE·유지비는 계측하지 않았다. [COST](COST.md). |

## 3. 남긴 원거리 원리군과 좁은 참고 부분

| 문제 | 원리군 / 원 분야 | 참고할 소프트웨어 부분 | 결정적인 연결·실패 조건 |
| --- | --- | --- | --- |
| P1 | 실패품의 처분·공개 판정 / 제조 품질 B02·B10 | 실패 확인·보류·재처리·공개 상태 구분 | 독립 문서의 경계를 물리 batch와 혼동하면 다른 성공 결과까지 철회할 수 있다. |
| P1 | 원 보고와 수정 보고의 계보 / 검사실 B03 | 내부 결과 이력과 현재 공개본 선택 | retry를 의도된 개정으로 취급해 매번 발행하면 중복 공개를 막지 못한다. |
| P1 | 복제 허가의 소비와 재허가 감시 / 세포 B09 | 처리 준비와 이미 소비한 공개 허가 구분 | 세포 주기를 프로세스 실행 주기로 바꿔 재시작 때 허가를 초기화하면 실패한다. |
| P1 | reset과 실제 시작의 분리 / 제조 안전 D01 | 복구 완료와 외부 공개 허가의 경계 | 입력 동일성·영속 상태·공개 원자성을 별도로 구현해야 한다. 자동 power-up 설정도 확인해야 한다. |
| P2 | 차이 발견과 의도 확인의 분리 / 약물 조정 C01·C02 | 충돌 검토·해결 근거 | 모든 차이를 오류로 자동 정규화하면 유효한 사용자 수정이 사라진다. |
| P2 | 원자료·대안과 편집 선택의 분리 / 문헌·구술사·재난 C04·D02·C06 | 원 수정/현재뷰/해결 결정을 나누는 표현 | 선택된 본문만 남기면 충돌 근거를 잃는다. 내구 저장·인과관계·내보내기 계약은 별도다. |
| P2 | 독립 관측과 차이 조사 후 조정 / 물류 실사 C05 | base/A/B 대조와 조정 이력 | 물리 수량의 참값 우선·허용오차를 복사해 작은 수정을 숨기면 P2를 위반한다. |

모두 `mapped + CONDITIONAL_TRANSFER`인 좁은 reference 후보다. 새 알고리즘 신규성은 입증하지 않았으며, 특히 P2의 원자료/현재뷰 분리는 기존 변경 보존 기법과 넓은 생각이 겹친다. 이번에 새로 얻은 것은 원 분야 출처와 관계·조건·반례의 설명이다.

## 4. 가장 강한 근거 세 가지

1. **표현의 명칭만으로 의미가 보존되지 않는 직접 근거.** R01의 원형 흐름 제약과 R09의 약120용어 확장 시 판별력 저하를 함께 확인했다. 표준 동사 선택과 소프트웨어의 동일성·시간·보존 조건은 별도 검사가 필요하다. [REPRESENTATIONS](REPRESENTATIONS.md), R01·R09.
2. **먼 유추의 이익과 손해가 모두 나타난 실증.** E01(N=153)의 새로움 이점과 E02(72명 모집/70명 분석)의 먼 자극 최대 새로움 저하를 설계·표본·측정·효과 크기와 함께 읽었다. E01의 수량 감소는 마지막 단계만 분석하면 p=.47이어서 처리시간 설명도 남는다. “먼 것이 항상 낫다”는 무조건 명제는 지지되지 않는다. [EVIDENCE](EVIDENCE.md), E01·E02.
3. **같은 원리의 올바른 좁은 참고와 잘못된 사용을 갈라낸 실제 재탐색 기록.** B09의 복제 허가와 C05의 차이 조정은 관계가 대응하지만, 재시작 시 재허가와 허용오차에 따른 무음 덮어쓰기는 각각 고정 조건을 위반한다. 별도 25개 판정과 입력을 남겨 후보 수만 늘리는 결론을 반박했다. [P1 판정](evidence/p1-judgments.json), [P2 판정](evidence/p2-judgments.json). 이것은 D1 근거에 기초한 H 구조적 반례이며 대상 실행 실패 관측은 아니다.

## 5. 이 결론이 틀릴 수 있는 지점

- **선택적 독해:** P2 R0는 본문 판정이 없다. 현재 0은 낮은 성과의 증거가 아니며, 동일 검토 예산에서는 원문 표현의 후보가 더 많을 수 있다.
- **질의 작성자의 선행 지식:** licensing, critical apparatus, testimony 같은 힌트를 이미 넣었다. 원거리 후보의 자동 발견 능력이나 순수 표현 효과를 측정한 것이 아니다.
- **언어·길이·검색 시스템 차이:** 한국어 R0와 주로 영어 R1–R3, 문장/부분 인용/기능어의 차이가 크다. 전문 DB의 결과도 일반 웹보다 자동으로 적합하지 않았다.
- **신규성의 입도:** FDA 문서 두 개와 문헌/구술사/FEMA 관계를 보수적으로 합쳤지만, 다른 원리군 분류에서는 숫자가 달라질 수 있다. 7은 새로운 소프트웨어 이론 수가 아니다.
- **원 분야의 전제:** 생물의 오류 가닥, 실사의 물리적 참값, 임상/편집 담당자의 의미 판단은 복수의 정당한 사용자 수정과 다르다. 연결 조건을 빼면 후보가 근접 오답으로 바뀐다.
- **입증 범위:** 원 분야의 실험·운영 지침·형식 표준과 대상 코드의 실제 보장은 다르다. 설명 카드의 사용자 효과와 작은 큐레이션 방식의 경제성은 여전히 H다.

구체 반박 관측으로 B07·D03의 지나치게 넓은 기능어, B14의 과학적 재현성으로의 의미 이동, C07의 동일 환자 판별로의 문제 변경, C08의 유효한 수정 삭제를 남겼다. [RETRIAL §3–4·7](RETRIAL.md).

## 6. 검증한 것과 미실시

### 실행 결과

- `8fc5fff6057cfa9133881ac038f6646883416d93` 체크아웃에서 연구 검사 **33/33 passed, 종료 코드0**. 집계 입력 SHA-256: `da78e4cf260fa64c9d1e73ef7fd67b974452b1000dc1c4738d982ebdf938fb7e`.
- 같은 SHA에서 `workbench.session check --fetch` **passed, remote_checked, 종료 코드0**; 2026-11-20T05:46:34.705087+00:00. 허용 경로 밖 변경0, 계약 오류0.
- HANDOFF 작성 직전 `git status --porcelain` 출력은 비어 있었다. 마지막 커밋에는 이 HANDOFF만 넣는다.
- P1/P2 원문·필수 조건·SCOPE 고정, 64문자열과 실행 연결, 자료 중복/분리, 24자료→25판정, T 필수 요소, 표현별 가족 집계, 로컬 링크, 변경 경로를 확인했다.
- 내부 별도 검토의 두 내용 오류(C05-M 설정 혼재, 빈/미검증 결과 문구)를 수정했다. 날짜만 있던 E01–E16은 실제 본문 접근을 다시 확인하고 최초 UTC 날짜와 재확인 시각을 구별했다. [내부 검토](evidence/internal-review.json).

[verification-report.json](evidence/verification-report.json)은 bundle8 이전의 같은 입력 파일 집합을 해시로 보존한다. 그 파일의 `checked_git_head`는 bundle7이고, 위 bundle8의 재실행은 출력 파일을 다시 쓰지 않고 동일 입력 해시·33개 통과를 확인한 결과다. 이전 검사 영수증을 나중 커밋의 실행 영수증으로 바꿔 쓰지 않았다.

재확인 명령(저장소 루트에서 실행):

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-010/evidence/verify_research.py
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-010/manifest.json --fetch
git diff --check 1eca580bf9ddc153f7c9691e30bd727eb7d0ce06 -- docs/workstreams/research/AF-RES-010/
```

### 수행하지 않은 검사와 이유·입력

원논문 실험 재현, E14 원자료 재계산, 후보 설치, P1/P2 대상 구현의 D4 시험, 실제 설계자 카드 평가, 분 단위 비용 계측은 하지 않았다. 다음 후보 검증의 입력과 관측은 각 판정의 `minimum_next_check` 및 RETRIAL의 7개 설명에 남겼다. 대상 구현이 정해지지 않아 작동하지 않는 가상 실행 명령을 만들지 않았다. 이는 완료된 문헌/재탐색 작업과 구분된 다음 적용 작업이다.

AGENTS.md의 공통 전체 검사 두 개는 **허용 경로 밖 `.workbench/` 쓰기**가 있으므로 이번 범위에서 실행하지 않았다. `scripts/check.py`와 호출되는 `scripts/acceptance.py`, `scripts/cloud_check.py`의 쓰기 경로를 확인했고 검사기를 수정하거나 제한을 우회하지 않았다. 공통 경로 쓰기가 허용되는 통합 작업에서 이 브랜치 최종 체크아웃과 작업 manifest를 입력으로 다음 명령을 실행하면 된다.

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/check.py --require-git
PYTHONDONTWRITEBYTECODE=1 python scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

Google Patents native 503, Semantic Scholar API 429, 일부 후보 PDF 차단은 excluded로 보존했고 계정 생성·유료 API·우회 로그인을 하지 않았다. AskNature 결과 갱신 실패 1개를 빈 결과로 바꾸지 않았다. 이러한 미실시·접근 실패를 성공한 구현 검사로 보고하지 않는다.

## 7. 산출물과 커밋 묶음

| 묶음 | 커밋 | 내용 |
| --- | --- | --- |
| 1 | `ebcca564df68377cc116634dcdab1695be69c0e8` | SCOPE·manifest 고정 |
| 2 | `13f7ed57090fe563a7bd136b655c6444764b8df0` | Q1/Q2·REPRESENTATIONS·원문 원장 |
| 3 | `c0dd5b0bf8fdc03e2b085122e63ce394e2093c12` | EVIDENCE·실증 및 반증 질의 |
| 4 | `f46dcf9c6e573693905f6aec0dccb3e244a32f0a` | TRANSFER_CASES·원저자 자료 |
| 5 | `eca8eb0d44728bffb755c3748194de86797ac23a` | P1 재탐색 로그·판정 |
| 6 | `f9dc276f2a17dffb094969a0d8c5963d2b03627f` | P2 로그·판정·전체 검색 기록 |
| 7 | `99c4698ef031eab80b5ba97afcafd385b397c415` | RETRIAL·COST·비교 수치 |
| 8 | `8fc5fff6057cfa9133881ac038f6646883416d93` | SELF_CHECK·검사 증거·검토 수정·열람 시각 보완 |

묶음9는 이 HANDOFF의 단독 커밋이며 SHA는 Git 이력에서 확인한다. 각 묶음은 생성 즉시 원격 브랜치에 반영했다. Git HTTPS push 인증 대신 허용된 GitHub tree/commit/ref의 expected SHA를 사용한 fast-forward로 저장했다.

읽는 순서: [SCOPE](SCOPE.md) → [REPRESENTATIONS](REPRESENTATIONS.md) → [EVIDENCE](EVIDENCE.md) → [TRANSFER_CASES](TRANSFER_CASES.md) → [RETRIAL](RETRIAL.md) → [COST](COST.md) → [SELF_CHECK](SELF_CHECK.md). 상세 추적은 [sources.json](sources.json)과 [SEARCH_LOG.json](SEARCH_LOG.json)에 있다.

## 8. 색인 변경 제안 한 행

공통 색인은 수정하지 않았다. 통합 담당에게 제안할 한 행:

| AF-RES-010 | 유추 설계 7표현·실증 반례·원저자 전이10사례, P1/P2 64질의 재탐색과 조건부 원리군7 | docs/workstreams/research/AF-RES-010/HANDOFF.md | AF-RES-002/004 고정 입력; D1＋D3-search, 대상 적용 H |

## 9. 다음 첫 행동

**후속 비교의 SCOPE를 별도 작업으로 먼저 고정한다.** P1/P2 원문은 그대로 두고 R0–R3의 언어, 질의 길이 범위, 분야/메커니즘 힌트, 본문 검토 예산을 같게 정한다. 이번에 비어 있던 P2 R0 본문 검토도 동일 예산으로 포함한다. 이 조건을 고정하기 전에 새 표현의 우위나 전체 검색 스택을 채택하지 않는다.

후속 구현 참고를 먼저 시험한다면 P1의 입력 A를 공개한 직후 응답 전에 중단하고 같은 A를 두 번 다시 보내는 입력부터 사용한다. 후보별로 어디까지 원 분야 관계가 도움이 되고 입력 동일성·영속 상태·원자성은 어디서 별도로 필요한지 관측한다. 현재 자료는 이 선택과 기각의 근거를 제공하며 실제 구현 통과를 대신하지 않는다.
