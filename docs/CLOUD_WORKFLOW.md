# 로컬 설치 없는 개발·검증 경로

확인일: 2026-11-19. 사용자의 기본 조건은 **PC에 개발환경을 설치하지 않는 것**이며, GPT-6.2 Sol Max를 사용하는 Codex Cloud는 보조 수단으로 허용됐다.

## 역할 배분

| 작업 | 기본 위치 | 남겨야 할 결과 |
| --- | --- | --- |
| 문제 정의·검색·대안 비교·설계 검토 | 웹 ChatGPT Pro | 근거·제약·결정·다음 질문 |
| 작업 연결·진행 확인·세션 교체 | Dot와 Dot의 클라우드 컴퓨터 | 작업 ID·실행 상태·저장 커밋·다음 행동 |
| 파일·브랜치·PR·결정 이력 | GitHub | 정확한 커밋과 연결된 문서 |
| 커밋 검사·OS별 실행·실패 로그 | GitHub Actions 표준 러너 | 검사 SHA·결과·bounded artifact |
| 반복 편집·디버깅·작은 독립 실험 | Codex Cloud 또는 현재 제공된 클라우드 작업공간 | 실제 실행 로그·변경 diff·handoff |
| 제품 시연용 웹 서비스 | 추후 Render 등 | 별도 배포 검증 |

GitHub Actions가 모델을 제공하는 것은 아니다. 검토한 코드의 실행을 맡긴다. 웹 Pro와 Codex 사용량은 실제 계정의 현재 표시를 따른다. API 키로 실행하는 모델은 ChatGPT 구독과 별도 과금이므로 이 구성에는 넣지 않았다.

사용자의 Dot은 가벼운 진행 담당으로 배치한다. 자기 클라우드 컴퓨터에서 Git·diff·검사 결과를 읽고, 실제 작업은 웹 Pro와 Codex Cloud에 묶음으로 전달한다. [Dot 연결 절차와 시작문](DOT_AUTOMATION.md), [진행 상태](automation/dot-control.json)를 따른다. 새 세션은 GitHub에 저장된 handoff를 직접 읽는다. 실제 native 웹 Pro 세션 생성·모델 선택은 Codex 위임과 별도로 확인하며, 현재 연결 상태는 준비 단계다.

## 1. GitHub 왕복

통합 브랜치는 `chore/workspace-foundation`이다. 작업 브랜치는 최신 통합 기준에서 `work/<task>` 또는 `codex/<task>`로 만든다. 기존 `work/discovery`, `work/data-model`, `work/experience`에는 과거 시작 지점이 남을 수 있으므로 재사용 전에 차이를 확인한다. 다른 작업자의 미반영 변경을 덮어쓰지 않는다.

코드·lab·검사 스크립트가 바뀌면 `Workbench acceptance`가 Ubuntu/Windows에서 실행된다. 제품·협업·작업 문서 변경에는 `Collaboration contract`가 실행된다. PR은 통합 브랜치 또는 `main` 대상에서도 검사하지만 자동 병합·배포는 없다.

작업 manifest가 없는 실행은 `no_active_sessions`, 모두 이미 통합되고 후속 변경도 없는 실행은 `already_integrated`로 표시한다. 이것은 새 세션 협업 시험의 통과가 아니다. 수동 실행 버튼은 기본 브랜치의 workflow 등록에 영향을 받으므로 지금은 push/PR 경로를 사용한다.

```sh
python scripts/cloud_check.py --environment github-actions --fetch-contract --require-clean
```

이 명령은 doctor, 기존 전체 검사·export·Git bundle 복원, 원본 smoke, 활성 작업 계약 검사를 실행한다. 모델·서버를 계속 켜 두거나 임의 입력 명령을 실행하지 않는다. 실패·timeout도 receipt에 남는다.

## 2. Codex Cloud 설정 대화

현재 공식 경로는 **Work in → Cloud → Select environment → Create environment** 또는 **Settings → Codex Cloud → Environments**다. GitHub 저장소를 선택하고 준비 대화에서 아래 지시문을 사용한다. 모델 선택은 계정 UI에서 **GPT-6.2 Sol / Max**, 속도는 기본 Standard부터 사용한다. 추론 강도와 속도 옵션은 별개다.

```text
laadkke-arch/agentflow-open을 위한 재사용 Codex Cloud 환경을 준비해줘.
저장소의 chore/workspace-foundation 최신 브랜치를 확인하고 AGENTS.md,
STATE.md, docs/START_HERE.md, docs/CLOUD_WORKFLOW.md를 직접 읽어.

목적은 개발 문제에 맞는 OSS·웹서비스·개발 도구를 근거와 제약으로
비교하는 탐색기를 조사·개발할 공통 환경이다. 이번에는 환경 준비만 한다.

현재 요구사항은 Python 3.12 이상과 Git이다. 기존 체크아웃을 재사용하고,
필요한 도구가 빠졌을 때만 설치해. 지금은 추가 Python 패키지·모델 API 키·
Docker·DB·상시 서버가 필요하지 않다. 기존 개인 작업을 덮어쓰지 마.

python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
을 실제 실행하고 .workbench/cloud-check.json과 실패 로그를 읽어줘.
작업 중 파일 수정이 있으면 먼저 diff를 검토하고 커밋/검사 범위를 분명히 해.
환경 설정 보고서에 코드 SHA, Python, 실제 명령, 종료 코드,
검사 미실시 항목을 남겨. 기본 main 변경과 제품 배포는 하지 마.

실제 확인된 설치 내용을 환경 설정에 저장하고 Publish 전에 준비 결과를 보여줘.
앞으로 새 작업은 AGENTS.md와 통합 브랜치 최신 상태를 읽고,
독립 작업 브랜치와 docs/tasks의 계약 핀으로 시작하도록 해.
```

공식 문서의 Save는 설정 저장, Publish는 준비된 파일시스템을 새 작업에 제공하는 단계다. 발행된 환경의 새 작업은 준비 상태를 사용하고, 기존 작업은 자기 파일 상태를 유지한다. 환경 수정 후에도 기존 작업이 자동으로 최신 공통 계약을 적용한 것으로 취급하지 않는다. 중요한 변경은 Git에 커밋한다.

**실제 계정 설정 상태:** 이번 공유 브라우저에서는 `chatgpt.com/codex` 로그인 화면을 확인했다. 로그인·GitHub 계정 연결·환경 생성/발행은 실행하지 못했다. 위 설정은 준비된 실행안이며 계정 설정 완료 보고가 아니다. 일반 웹 Pro의 GitHub 연결과 Actions 경로는 이것에 의존하지 않는다.

## 3. 작업 계약 생성과 검사

아래는 **클라우드 checkout에서** 진행한다. 브랜치 생성과 최신 통합 문서 읽기가 먼저다.

```sh
python -m workbench.session start discovery-case \
  --allow docs/workstreams/discovery/ \
  --output docs/tasks/discovery-case.json --fetch
```

manifest는 시작 SHA, 계약 버전·파일별 해시, 허용 경로, 의존 커밋을 고정한다. 다른 작업의 결과를 전제로 할 때는 `--dependency work/data-model=실제_40자리_SHA`를 추가한다. 문자열 예시를 그대로 실행하지 않는다.

```sh
python -m workbench.session check docs/tasks/discovery-case.json --fetch
```

`--fetch` 성공만 원격 최신성 확인으로 표시한다. 원격 접근 없이 로컬 ref로 검사할 수 있지만 결과는 `local_only`다. 계약이 바뀌면 변경을 읽고 자신의 영향 분석을 남긴 뒤 새 과제로 핀을 다시 만든다. 기존 manifest를 덮어쓰며 과거 전제를 없애지 않는다. 이 검사는 동시 편집 잠금이나 자동 알림, 자동 의미 충돌 해결이 아니다.

## 4. 한도를 아끼는 실행 단위

작은 오타·문서 정리는 웹에서 처리하고, 실행·실패 수정이 필요한 묶음만 Codex에 맡긴다. 매 대화에 저장소 전체를 넣는 대신 현재 목표·계약·관련 근거·검사 명령을 전달한다. 세 세션 모두 같은 자료를 다시 조사하게 하지 않는다. 구현 담당과 검토 담당을 분리해 이미 만든 가정을 검토한다.

11월 이후에도 남는 것은 GitHub의 코드·근거·결정·재현 명령이다. 구독의 특정 시점 혜택이나 무한 브라우저 루프를 지속성의 전제로 삼지 않는다.

## 공식 출처

- [Codex Cloud 환경과 발행](https://learn.chatgpt.com/docs/environments/cloud-environments)
- [현재 모델·추론 설정](https://learn.chatgpt.com/docs/models)
- [Work/Codex 사용량과 API 구분](https://learn.chatgpt.com/docs/pricing)
- [GitHub Actions 요금 구조](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [GitHub Actions 제한](https://docs.github.com/en/actions/reference/limits)
