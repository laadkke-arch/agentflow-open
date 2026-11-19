# 공통 작업환경 시작 안내

갱신: 2026-11-19. 기본 경로는 **사용자 PC 설치 없이 웹 ChatGPT Pro + GitHub + GitHub Actions**다. 코드를 여러 번 실행하며 수정할 때는 **Codex Cloud**를 보조 실행환경으로 사용한다.

**Dot이 있는 경우:** [연결·진행 설정](DOT_AUTOMATION.md)을 사용한다. 웹 Pro의 조사·설계·검토 역할은 유지하고, Dot이 자기 클라우드 컴퓨터에서 상태를 확인해 작업과 세션을 연결한다. GitHub 인계와 두 작업 연결 시험은 준비했으며, 실제 사용자 Dot의 세션 생성·교체와 지속 실행은 아직 연결하지 않았다.

## 무엇을 위한 환경인가

최종 제품은 사용자의 개발 문제에서 출발해 오픈소스·웹서비스·라이브러리·MCP를 찾고, **요구조건별 적합성·출처·제약·미확인 사항**을 비교하는 탐색기다. 지금은 그 제품을 조사·설계·검증할 공통 기반을 준비한다. 제품의 웹앱·DB·추천 엔진은 아직 구현하지 않았다.

처음에는 다음 다섯 곳만 읽는다. 나머지는 과제에 필요한 때 읽는다.

1. [현재 상태](../STATE.md): 실제 검사와 미실시 범위.
2. [제품 목적](product/README.md), [조사 기준](product/RESEARCH_PROTOCOL.md).
3. [이번에 확인한 선택과 이유](research/no-local-discovery-workflow-2026-11-19.md).
4. [클라우드 실행 절차](CLOUD_WORKFLOW.md).
5. [협업 규칙](collaboration/README.md), [새 대화 시작문](collaboration/SESSION_STARTS.md).

## 기본 작업 순서

1. GitHub 연결로 `laadkke-arch/agentflow-open`의 **`chore/workspace-foundation` 최신 SHA**를 확인한다. 기본 `main`의 옛 파일을 기준으로 작업하지 않는다.
2. 개발 문제 하나를 정하고 필요한 기존 도구·자료부터 조사한다. 출처는 링크·확인일·근거 수준과 함께 저장한다. [실제 조사 사례](research/discovery-case-2026-11-19.json)를 재사용할 수 있다.
3. 통합 담당이 목표·완료 조건·허용 경로·공통 계약·의존 커밋을 정한다. 기존 A/B/C 역할은 선택지다. 현재 기본은 **진행 담당 1개 + 독립 검토 1개**, 독립적인 조사에만 추가 세션을 사용한다.
4. 변경은 작업 브랜치에 저장한다. 구현이 필요한 작업은 Codex Cloud 등 클라우드 checkout에서 작업 manifest를 생성하고 검사한다. 웹 GitHub 연결만 있는 대화는 파일 읽기·편집·PR·Actions 결과 검토를 담당할 수 있지만, 셸 명령을 실행했다고 보고하지 않는다.
5. Actions가 실제 checkout을 검사한다. 완료 후 실행한 SHA·종료 코드·로그·미실시 항목을 읽어 변경과 연결한다. 테스트는 제품의 추천 품질을 대신하지 않는다.
6. 짧은 인수인계에 현재 결론, 결정이 달라질 조건, 근거 파일, 검사 SHA, 다음 행동을 남긴다. 새 대화는 이를 직접 읽는다.

## 클라우드에서 실행할 공통 명령

현재 필요한 것은 Python 3.12 이상과 Git이다. 기본 검사는 외부 Python 패키지나 모델 API 키 없이 실행한다. 아래 명령을 **사용자 PC에 설치하라는 의미가 아니다.**

```sh
python scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

CI처럼 커밋된 파일만 검사하려면 `--require-clean`을 추가한다. `.workbench/cloud-check.json`에 검사한 SHA, 작업 폴더 수정 여부, 플랫폼, 명령별 종료 코드와 로그 경로가 남는다. `--environment`는 호출자가 붙인 이름이며 Codex 계정 연결 증명이 아니다.

Actions가 사용할 수 없는 때에도 같은 명령을 다른 허용된 클라우드 환경에서 실행할 수 있다. Ubuntu 실행을 Windows 통과로 보고하지 않는다. 현재 세션에서 실제로 실행한 결과와 GitHub hosted 실행은 [검사 기록](../STATE.md)에서 구분한다.

## 자료 재사용 확인

`lab/reference-audit`는 출처 연결을 검사하는 기존 실습이다. 실제 탐색기 조사에 사용한 자료도 다음 명령으로 연결 무결성을 확인한다.

```sh
python -m workbench run reference-audit discovery
```

이 검사는 출처 ID 누락과 중복을 찾는다. 외부 주장 자체의 진실성·현재 서비스 상태·우리 제품의 추천 정확도를 자동 인증하지 않는다. 실제 자료의 판단은 고정 출처와 확인 시점까지 읽어 검토한다.

## 선택형 경로

- **Codex Cloud 준비 환경**: [CLOUD_WORKFLOW.md](CLOUD_WORKFLOW.md)의 설정 대화를 사용한다. 이번 공유 브라우저는 로그인 화면까지만 확인되어 사용자 계정의 환경 발행은 미완료다.
- **WebJjonku/SpaceDock**: 직접 파일·명령 MCP가 필요한 때 [기존 설치 안내](../integrations/web-runtime/README.md)를 참고한다. Docker·지속 호스트·웹 계정 연결을 요하는 별도 경로이며 기본 작업의 선행조건이 아니다.
- **CoS Goal/Loop/Compact**: 별도 브라우저 계층이다. 현재 연결하지 않았다. GitHub에 저장한 근거·결정이 장기 기록이다.
- **Render**: 제품 시연·배포가 필요해질 때 검토한다. 현재 작업환경 검사에는 서버 생성이 필요하지 않다.

공개 저장소에는 공개 가능한 요약과 시험 자료만 보관한다. 기존 AgentFlow Studio, `main`, 계정 권한과 유료 자원의 변경은 현재 작업 범위에 포함하지 않는다.
