# ChatGPT 웹 새 대화 3개 시작문

각 블록을 **서로 다른 웹 대화 하나에만** 복사한다. GitHub의 정확한 브랜치·이슈·파일 확인을 첫 작업으로 요구한다. 프롬프트를 적었다고 세션이 자동으로 열리거나 무한 실행되는 것은 아니다.

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
