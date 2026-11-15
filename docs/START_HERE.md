# 공통 작업환경 시작 안내

이 브랜치에는 작업환경과 두 개의 검증용 소규모 프로젝트가 있습니다. 탐색기 제품은 아직 없습니다. 작업환경 자체는 의존성 설치 없이 Python 3.12 이상에서 실행합니다.

## 첫 실행

```sh
git clone --branch chore/workspace-foundation https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
python -m workbench doctor
python scripts/check.py --require-git
```

네트워크는 최초 Git 복제와 CI 도구 준비에 필요하며, 실습 작업과 테스트는 외부 API에 접속하지 않습니다. 기본 실행에 계정 토큰을 넣지 않습니다.

## 조사부터 결과까지

```sh
python -m workbench context repo-intake --query "manual review"
python -m workbench run repo-intake test
python -m workbench run repo-intake demo
python -m workbench context reference-audit --query contract
python -m workbench run reference-audit test
```

run 결과의 receipt 경로를 확인한 뒤 `python -m workbench verify-receipt 프로젝트 receipt경로`로 검사합니다. 실제 내용은 같은 폴더의 stdout.txt와 stderr.txt를 읽습니다. receipts는 검증한 파일의 해시를 포함하지만 서명이나 완전한 품질 인증은 아닙니다.

context는 BRIEF와 STATE를 우선 포함하고 나머지 선언된 문서에서 문자열을 검색합니다. --budget은 토큰 수가 아닌 본문 문자 수입니다. 맞는 자료가 없다는 것이 세상에 해당 정보가 없다는 뜻은 아닙니다. 비밀값이나 미등록 파일을 재귀 검색하지 않습니다.

## 별도 작업 폴더로 가져가기

```sh
python -m workbench export repo-intake ../repo-intake-independent
cd ../repo-intake-independent
python -m workbench doctor
python -m workbench run repo-intake test
```

기존 목적지에는 덮어쓰지 않습니다. 다른 프로젝트·Git 이력·계정·.env는 자동 복사하지 않고, 명시된 파일과 공통 절차만 복사합니다. 단, 선언된 문서에 비밀값이 들어 있으면 자동 감지하지 못하므로 공개 가능한 자료만 사용합니다.

## 새로운 소규모 프로젝트 등록

기존 project.json을 참고하여 별도 폴더에 BRIEF.md, STATE.md, DECISIONS.md, RESEARCH.md, sources.json과 실행 코드·테스트를 둡니다. 기존 프로젝트의 상태를 그대로 현재 사실로 복사하지 않습니다. 새 id와 경로를 workbench/catalog.json에 등록하고 inputs에 실제 읽는 모든 파일을 포함합니다. tasks에는 검토한 Python argv와 최대 120초 제한을 기록합니다. --shell 문자열을 받는 기능은 없습니다.

환경 자체의 두 실습 acceptance는 고정된 회귀 시험입니다. 새 제품의 완료 판정은 그 제품에 맞는 별도 테스트로 추가해야 하며 기존 실습 두 개의 성공으로 대체하지 않습니다. 복잡한 의존성이 필요해지면 uv/Nox 등 기존 도구를 도입하고 잠금 파일로 버전을 관리합니다.

## 다음 AI 대화에 전달할 시작문

`laadkke-arch/agentflow-open`의 `chore/workspace-foundation` 브랜치 최신 커밋을 확인하고 AGENTS.md, STATE.md, docs/START_HERE.md를 읽는다. 실제 실행 기록에 연결된 코드 버전을 확인한 후 선택한 프로젝트의 context를 읽고 미완료 항목부터 이어간다. 이미 완료된 선택을 다시 묻지 않고, 미실행 항목을 완료로 가정하지 않는다.

이 시작문을 파일에 넣었다는 이유로 새 대화 인수인계를 검증한 것은 아닙니다.

## CI와 백업

현재 CI는 이 환경 브랜치와 work/** 브랜치의 코드·실습·공통 절차 변경에 반응합니다. main에 자동 배포하거나 병합하지 않습니다. Linux·Windows에서 같은 검사 명령을 실행하며 Git bundle로 현재 소스 이력을 내보내고 새 디렉터리에 복원한 뒤 demo를 실행합니다.

아티팩트 보존 기간은 7일입니다. 영구 백업이 필요하면 별도의 승인된 보관 위치로 내려받아야 합니다. Git bundle은 DB·GitHub 이슈·비밀값·미커밋 파일·외부 링크 파일이나 LFS 내용을 모두 보관하는 완전한 서비스 백업이 아닙니다.

## 자동 실행의 범위

이 도구는 작업 큐를 무한히 소비하거나 AI 모델을 자동 호출하지 않습니다. 검토된 작업 한 번을 실행하고 결과를 남깁니다. Python 작업은 OS 계정 권한을 가지므로 프로세스/폴더 분리만으로 보안 격리를 주장하지 않습니다. 새 연결·유료 자원·운영 데이터 접근은 별도 승인 대상으로 남깁니다.
