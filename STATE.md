# 현재 작업 상태

## 2026-11-19 신규 기록 — 제품 문서화와 병렬 협업 준비

- 기존 2026-11-15 환경 시험 결과는 아래에 보존한다. **2026-11-19에 새 런타임/새 PC 연결 실험을 통과했다고 주장하지 않는다.**
- 오픈소스·웹사이트·무료 서비스 탐색기 목표, 근거 중심 조사 방식, 5개 관계형 테이블 초안, AgentFlow Studio 선택형 미래 연동, 단계별 완료 기준을 `docs/product/`에 문서화했다. 현재까지는 **명세 초안**이며 제품 구현/실제 자료 수집/DB 배포가 아니다.
- 웹 ChatGPT 3개 병렬 대화용 `docs/collaboration/`, 작업별 `docs/workstreams/{discovery,data,experience}/` 상태 파일, 이슈 [#2](https://github.com/laadkke-arch/agentflow-open/issues/2)·[#3](https://github.com/laadkke-arch/agentflow-open/issues/3)·[#4](https://github.com/laadkke-arch/agentflow-open/issues/4)를 준비했다. **별도 채팅에서 실제 실행·인수인계 검증은 아직 없다.**
- 전용 브랜치 `work/discovery`, `work/data-model`, `work/experience`를 실제 생성했고, 각각 동일한 시작 커밋 `63de300926d26d3c86bc05ec831aee015639b7bb`과 담당 상태 문서·GitHub 이슈를 조회해 확인했다. **독립된 AI 웹 대화의 실행은 미검증**이다.
- 다음 단계: 사용자가 세 웹 대화를 A/B/C 시작 지시문으로 각각 시작하면, 자기 브랜치의 조사·설계 근거·실제 테스트를 커밋하고 PR로 인계한다. 통합 PR을 자동 병합하지 않으며 `main`은 그대로 둔다.
- 기술 환경의 미완료 항목인 사용자 PC Docker 설치, 웹 MCP 연결, CoS Goal/Loop, Render·DB 서비스 생성은 그대로 미완료다.

기술 환경 검증 기록 기준일: 2026-11-15
브랜치: `chore/workspace-foundation`
단계: 커뮤니티의 실제 WebJjonku/SpaceDock 런타임을 설치 가능한 형태로 구성하고 독립 컨테이너에서 검증. 실제 사용자 PC와 웹 계정 연결은 아직 안 됨.

## 이번에 달라진 것

기존 Python workbench는 기록·검증 보조 도구다. 그것만으로 웹 개발 환경이 완성됐다고 취급하지 않는다. 이번에는 커뮤니티에서 공개한 실제 MCP 서버를 재사용해 직접 파일 편집, 명령 실행·관찰, worktree, 프로젝트별 recall을 연결했다.

- 엔진: starlove7/spacedock 0.1.6, 원본 커밋 41df6ed1519242e742079c84989cd15b5a4e441b.
- 컨테이너 기반: repairer5812/webjjonku, 커밋 e0cef9118f612ed148c6db2806f1f8b6ea2661ad.
- 우리 변경: root 단위 기억 분리, shared 루트의 명령 권한 제거, Python 3.12 호환, 설치·연결 단계 분리, 실제 프로젝트 통합 검사.
- 구현 위치: integrations/web-runtime/. 서버·OAuth·명령 세션을 새로 직접 만든 것이 아니다.

## 실제 검증 근거

- 검증 코드: `2f7451afa7de81d1c5583090c9cd413fdef5f932`.
- 실행: https://github.com/laadkke-arch/agentflow-open/actions/runs/43707046397
- 설치 설정 검사 8개, 원본 HTTP OAuth 검사 18개, 실제 MCP 프로젝트 검사 23개, Python·Git 기록 검사 5개 통과.
- 설치한 Compose 프로필 HTTP 검사 11개, 컨테이너 재생성 후 같은 11개 재통과. 반복 항목을 고유 검사 수처럼 더하지 않는다.
- 두 프로젝트를 실제 MCP로 읽고 수정한 뒤 test/demo를 실행했다. 긴 명령은 같은 세션을 관찰했다.
- 프로젝트별 recall, 서버 재시작 후 기억·파일, worktree 분리, named volume 보존을 확인했다.
- 실제 doctor, MCP 수정 후 Git 커밋, 새 로컬 clone 복원도 통과했다. 런타임의 원격 push는 시험하지 않았다.
- 아티팩트 ZIP을 내려받아 SHA256을 대조하고 실제 요약·프로젝트 출력·호환 검사·설치 프로필 로그를 읽었다.
- 상세: docs/sessions/2026-11-15-community-runtime.json.

초기 CI 설정은 작업 시작 전 실패해 수정했다. 원본 컨테이너 Python 3.11과 기존 workbench의 3.12 계약 차이도 찾아 이미지와 실제 doctor 검사로 보완했다. 이전 검사 성공을 이 계약 확인으로 오인하지 않았다.

## 조사와 선택

디시의 효율·자동 세팅·연결 글, Reddit의 개발자 소개, SpaceDock 작성자 설명을 출발점으로 실제 저장소를 확인했다. CoS, DevSpace, 웹쫀쿠 via Agents, GPT Repo MCP 등을 비교했다.

특히 CoS의 Goal·Loop·Compact & Resume는 실제 구현된 별도 브라우저 계층이다. 모든 웹쫀쿠가 수동 인수인계뿐이라는 설명을 하지 않는다. 그러나 이 저장소에 CoS를 설치하거나 현재 웹 대화와 연결한 것은 아니다. 상세 비교: docs/research/community-web-runtime-2026-11-15.md.

## 실제로 남은 연결

사용자의 PC 또는 승인된 지속 실행 호스트가 필요하다. 현재 이 대화에 그 PC를 실행할 도구가 연결돼 있지 않다. 설치 파일은 준비됐지만 사용자 PC에서 실행했다고 보고하지 않는다.

1. integrations/web-runtime/README.md의 setup으로 전용 Docker 볼륨과 런타임을 준비한다.
2. setup은 공개 터널을 열지 않는다. connect --approve-public-endpoint는 별도의 공개 연결 승인이다.
3. 사용자 웹 계정에서 MCP 등록·OAuth 승인 후 실제 도구 호출을 확인한다. 키를 채팅에 붙이지 않는다.
4. 긴 대화의 자동 진행을 원하면 CoS 또는 via Agents의 브라우저 계층 연결을 별도로 확인한다. 중복 실행기와 개인 브라우저 기록 수집을 자동 설치하지 않는다.

## 유지한 것과 경계

이전 workbench의 두 소규모 프로젝트, Windows/Linux 검사와 Git 백업 증거는 docs/sessions/2026-11-15-runtime-acceptance.json에 유지한다. 새 Docker 통합은 Linux에서 확인한 것이며 Windows Docker Desktop 실사용까지 검증한 것이 아니다.

새 AI 대화 인계, 비공개 공통 저장소 분리, 원격 Git 인증, Render·DB·제품 구현은 아직 없다. main과 기존 AgentFlow Studio, 계정 권한, 공개 범위, 유료 자원은 바꾸지 않았다. 공개 저장소에 개인 대화 원문이나 인증정보를 넣지 않는다.

추가 문서는 위 검사 이후의 기록이다. CI 아티팩트는 14일 보존으로 2026-11-29 UTC에 만료되며 영구 백업이 아니다. 응답이 끝난 뒤 이 채팅의 모델이 계속 동작하는 상주 에이전트는 설정하지 않았다.
