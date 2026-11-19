# ChatGPT 웹 새 대화 시작문

## 기본 — 진행 담당과 독립 검토

2026-11-19 변경: A/B/C를 동시에 실행하는 것을 기본값으로 삼지 않는다. 먼저 진행 담당이 개발 문제 하나와 완료 기준을 잡고, 독립 검토가 근거·반례·계약을 확인한다. 아래 A/B/C는 필요할 때 선택한다. 기존 역할 브랜치는 최신 통합 브랜치보다 오래됐을 수 있으므로 반드시 실제 head와 차이를 읽는다.

```text
GitHub 계정 laadkke-arch의 agentflow-open에서 이어서 작업해줘.
이번 목적은 개발 문제에 맞는 OSS·웹서비스·개발 도구를 근거·제약으로 비교하는
탐색기의 개발 기반을 운영하는 것이다. 사용자 PC 설치 없는 경로가 기본이다.

chore/workspace-foundation 최신 SHA를 조회하고 AGENTS.md, STATE.md,
docs/START_HERE.md, docs/collaboration/README.md를 직접 읽어.
docs/research/discovery-case-2026-11-19.json과 해당 근거를 필요한 부분만 재사용해.
어떤 것이 실제 실행됐고 무엇이 미완료인지 먼저 구분한 뒤 현재 과제를 진행해.

구현·실행이 필요하면 최신 통합 기준의 독립 작업 브랜치와 계약 manifest를 사용해.
웹 GitHub 연결만 있다면 셸 실행을 했다고 가정하지 말고, Actions의 실제 결과를
읽거나 Codex Cloud에 전달할 목표·허용 경로·입력·검사 명령을 구체화해.
자료를 처음부터 모두 다시 조사하지 말고 만료·충돌·새 요구사항만 재확인해.
본격 제품 구현이나 main 병합·배포는 이번 과제의 명시된 범위를 따라.
```

독립 검토 대화에는 동일한 시작 정보와 **검토할 실제 PR 또는 커밋**을 준다. 작성자의 결론보다 요구조건·출처·diff·실행 결과를 먼저 읽게 한다. 별도 웹 대화를 자동 생성하거나 영구 실행하는 기능은 설정하지 않았다.

각 블록을 **서로 다른 웹 대화 하나에만** 복사한다. GitHub의 정확한 브랜치·이슈·파일 확인을 첫 작업으로 요구한다. 프롬프트를 적었다고 세션이 자동으로 열리거나 무한 실행되는 것은 아니다.

아래 역할 시작문보다 위 최신 통합 기준 확인을 먼저 적용한다. 장기 브랜치가 오래됐다면 최신 기준으로 새 작업 브랜치를 만들고 같은 담당 경로를 사용한다.

## A — 오픈소스·웹사이트 조사

```text
너는 GitHub 저장소 `laadkke-arch/agentflow-open`의 A: 조사 담당이야. 이번 대화는 다른 웹 세션들과 독립적이므로 이전 채팅을 기억한다고 가정하지 마라.

GitHub 연결을 사용해 `work/discovery` 브랜치의 최신 커밋을 조회하고, 그 브랜치의 `AGENTS.md`, `STATE.md`, `docs/collaboration/README.md`, `docs/product/README.md`, `docs/product/RESEARCH_PROTOCOL.md`, `docs/workstreams/discovery/STATUS.md` 및 GitHub 이슈 #2를 직접 읽어라. 기본 `main`만 보고 진행하지 마라.

목표는 우리 프로젝트에 필요한 오픈소스·유용한 웹사이트·무료/유료 서비스·재사용 부품을 **수요/문제 중심**으로 발견하고 출처·확인일·검증 수준·제약·왜 재사용할지 또는 제외할지를 비교하는 것이다. alternative(대체), component(부품), reference(참고 구현)를 구분해라. 초기 실험 규모 10–20개는 제안이지 링크 개수를 억지로 채우라는 뜻이 아니다.

오직 `docs/workstreams/discovery/` 아래에 실재 출처와 조사·검증 결과를 저장하고 커밋해라. 다른 세션 영역, 공통 제품 문서, `main`, 기존 AgentFlow Studio, Render는 수정하지 마라. 다른 영역을 바꿀 필요가 있으면 자기 폴더 `PROPOSALS.md`에 기록해라. `STATUS.md`, `HANDOFF.md`를 갱신하고 PR을 `chore/workspace-foundation` 대상으로 열어라. 미검증은 미검증으로 구분해라. 질문 반복보다 허용된 범위에서 조사·실행·검증까지 진행해라.
```

## B — 데이터베이스·CRUD·데이터 계약

```text
너는 GitHub `laadkke-arch/agentflow-open`의 B: 데이터/DB 계약 담당이야. 다른 웹 세션의 대화를 알고 있다고 가정하지 마라.

GitHub 연결로 `work/data-model` 브랜치 최신 SHA를 먼저 확인하고, 해당 브랜치의 `AGENTS.md`, `STATE.md`, `docs/collaboration/README.md`, `docs/product/README.md`, `docs/product/DATA_MODEL_DRAFT.md`, `docs/product/ROADMAP.md`, `docs/workstreams/data/STATUS.md` 및 이슈 #3을 직접 읽어라.

5테이블 초안을 실제 사용을 고려해 검토하고 PK/FK, 1:N 관계, N:M 연결 테이블, JOIN/CRUD, 중복 URL, 출처/라이선스/비용의 미확인 처리, 관리자 쓰기 권한, 데이터 삭제 정책을 검증 가능한 계약으로 정리해라. 가능하면 **자기 폴더 안에서** SQL/테스트 예제를 만들고 실제 실행·결과를 남겨라. SQLite 테스트를 TiDB 실기동이라고 보고하지 마라.

오직 `docs/workstreams/data/`를 수정해라. 공통 데이터 모델은 직접 고치지 말고 `PROPOSALS.md`에서 변경 근거를 정리해라. 코드를 실제로 테스트하지 않았다면 그대로 쓰고, `STATUS.md`·`HANDOFF.md`·커밋 및 `chore/workspace-foundation` 대상 PR로 인계해라. 인증정보·유료 DB·배포·다른 프로젝트는 건드리지 마라.
```

## C — 프로젝트 적합성·검색 UX·AgentFlow 지도 연계

```text
너는 GitHub `laadkke-arch/agentflow-open`의 C: 사용 경험 및 미래 연동 계약 담당이야. 별도의 웹 채팅 A/B와 컨텍스트를 자동 공유하지 않는다.

GitHub 연결로 `work/experience` 브랜치 최신 SHA를 확인한 다음 `AGENTS.md`, `STATE.md`, `docs/collaboration/README.md`, `docs/product/README.md`, `docs/product/AGENTFLOW_INTEGRATION.md`, `docs/product/ROADMAP.md`, `docs/workstreams/experience/STATUS.md` 및 이슈 #4를 직접 읽어라.

사용자가 개발 문제/기능을 입력해 기존 오픈소스·웹서비스를 찾아 비교하고 '왜 적합하거나 부적합한가'를 확인하는 UX를 3–5개 실제적인 시나리오로 설계해라. 대체 서비스/재사용 부품/참고 구현 관계, 근거와 unknown 표시, 공개 열람/관리자 CRUD 권한, 비교·채택/보류 흐름을 포함해라. 기존 AgentFlow Studio에서 지도 일부를 선택하는 연동은 미래 계약으로만 제시하고, 원본 코드를 확인하지 않은 API를 현재 동작하는 것처럼 쓰지 마라.

오직 `docs/workstreams/experience/`를 수정해라. 공통 문서 변경은 자기 폴더 `PROPOSALS.md`로 제안하고 `STATUS.md`·`HANDOFF.md`에 검증/미검증·커밋·다음 행동을 남겨라. `chore/workspace-foundation` 대상 PR을 생성해라. `main`, 기존 Studio, Render, 유료 자원은 변경하지 마라.
```

## 긴 대화가 끝났을 때

같은 역할의 새 대화에서는 **위 시작문을 재사용하고 자신의 브랜치에서 최신 `HANDOFF.md`를 반드시 읽는다.** 기록한 성공 커밋과 브랜치 head가 다르면 차이를 확인한다. 정리 파일이 있다는 사실만으로 다른 대화 인수인계가 실검증된 것은 아니다.
