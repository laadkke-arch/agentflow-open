# 웹 ChatGPT Pro 세션 3개 병렬 협업 규칙

작성: 2026-11-19. 상태: **협업 파일·이슈·브랜치 준비 단계**. 다른 AI 웹 세션에서의 실제 실행/인수인계 검증은 아직 없다.

## 시작

- 저장소: `laadkke-arch/agentflow-open`, 통합 기준 브랜치: `chore/workspace-foundation`. **`main`은 건드리지 않는다.**
- A **실제 오픈소스·웹사이트 자료 조사**: `work/discovery`, [이슈 #2](https://github.com/laadkke-arch/agentflow-open/issues/2), 수정할 경로 `docs/workstreams/discovery/`.
- B **데이터 모델·DB 검증 계약**: `work/data-model`, [이슈 #3](https://github.com/laadkke-arch/agentflow-open/issues/3), 수정할 경로 `docs/workstreams/data/`.
- C **검색·비교 UX 및 AgentFlow 지도 연동 설계**: `work/experience`, [이슈 #4](https://github.com/laadkke-arch/agentflow-open/issues/4), 수정할 경로 `docs/workstreams/experience/`.
- 새 대화 각각에 [`SESSION_STARTS.md`](SESSION_STARTS.md)의 A, B, C 시작 지시문을 **하나씩** 전달한다.
- 제품 기준문서는 `docs/product/README.md`, `RESEARCH_PROTOCOL.md`, `DATA_MODEL_DRAFT.md`, `AGENTFLOW_INTEGRATION.md`, `ROADMAP.md`이다. **수업 과제 조건과 제품 장기 목표, 확인된 사실과 설계 제안을 구분**한다.

## 세션마다 반드시 해야 하는 순서

1. 올바른 GitHub 계정이 연결됐는지 확인하고 **자기 브랜치의 최신 SHA**를 조회한다. GitHub의 기본 `main` 파일만 열지 않는다.
2. 자기 브랜치의 `AGENTS.md`, `STATE.md`, 위 제품 기준문서, 이슈 및 담당 `STATUS.md`를 **직접 읽는다**. 전혀 다른 채팅의 메모를 자동 공유한다고 가정하지 않는다.
3. 기존 해결책·커뮤니티 실제 사례를 비교하고 출처/확인 시점/검증 수준/채택·보류·제외 이유를 명시한다.
4. 자기 담당 폴더에서 문서·작은 재현 가능한 예제만 만들고, 가능하면 실제 검증한다. **기존 AgentFlow Studio 코드, `main`, 다른 세션 폴더, 운영 데이터는 변경하지 않는다.**
5. `STATUS.md`와 자기 폴더 `HANDOFF.md`에 작업 내용·커밋·검증·다음 행동을 적고 같은 브랜치에 커밋한다.
6. 리뷰 가능하면 **자기 브랜치 → `chore/workspace-foundation`** 대상 PR을 만든다. 자동으로 병합하지 않는다.

## 파일 충돌과 데이터 공유

- 공유 제품 기준문서(`docs/product/`), 루트 README·AGENTS·STATE, 협업 규칙(`docs/collaboration/`)은 **통합 담당만 수정한다**.
- A/B/C는 공통 설계의 변경 제안을 **자기 폴더의 `PROPOSALS.md`**에 기록한다. 같은 파일을 동시에 고치는 일은 피한다.
- 상호 의존 정보는 이슈/PR URL, **정확한 커밋 SHA**, 필요한 필드와 불확실성을 적는다. 다른 대화가 기록을 즉시 감지하지는 못한다.
- PR이 승인되면 통합 담당은 근거·중복·보안·데이터 계약 충돌을 검토하고 기준문서를 별도 커밋으로 갱신한다. 자동 병합·강제 push 금지.
- 새 대화에서 이어받을 때에는 과거 답변의 '완료'가 아니라 **GitHub의 최신 파일·PR·실제 테스트 기록**으로 상태를 재구성한다.

## 자동화의 실제 범위

세 개의 ChatGPT 웹 대화를 열면 **세 개의 독립 채팅**이 되는 것이지, 자동 조율되는 에이전트 팀이 되는 것은 아니다. GitHub에 브랜치/문서가 있어도 자동으로 프롬프트를 보내거나 무기한 작업하지 않는다.

현재 WebJjonku/SpaceDock의 Docker 실행 구성을 독립 Linux CI에서 확인했지만, **사용자 PC 및 이 웹 채팅의 MCP 연결은 미완료**다. CoS의 Goal·Loop·Compact는 별도 설치·브라우저 권한을 요하는 다른 계층이며 현재 켜져 있지 않다. 이번 3개 작업은 연결 없이도 GitHub로 조사·문서화를 할 수 있게 분리했다.

이 저장소는 공개다. 개인 대화 원문, API 키, 고객 자료, 로컬 비공개 경로, 비공개 코드, 사업상의 비공개 기록을 올리지 않는다. 배포·계정 권한·유료 자원·Render/DB 변경·기존 운영환경 변경은 별도 승인 대상이다.

- 작업 배정 및 실제 상태: [STATUS_BOARD.md](STATUS_BOARD.md)
- 새 세션 시작: [SESSION_STARTS.md](SESSION_STARTS.md)
- 인수인계 양식: [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md)
- 검토·통합: [REVIEW_AND_MERGE.md](REVIEW_AND_MERGE.md)
