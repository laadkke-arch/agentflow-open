# 공통 작업환경 시작 안내

목표는 웹 대화에서 실제 개발 환경을 사용하고 조사·판단·검증 결과를 다음 프로젝트에 남기는 것이다. 이 브랜치에는 실제 커뮤니티 MCP 런타임의 설치 구성과 기록·검증 보조 도구가 함께 있다. 탐색기 제품은 아직 없다.

## 웹 개발 환경을 연결할 때

먼저 [커뮤니티 런타임 설치 안내](../integrations/web-runtime/README.md)를 따른다. 실제 서버·파일 편집·명령 세션·recall은 WebJjonku/SpaceDock 원본을 사용한다. 기본 설치에는 Git, Python, Docker Linux 엔진과 Compose가 필요하다.

```sh
git clone --branch chore/workspace-foundation https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
python integrations/web-runtime/manage.py setup
```

setup 명령은 내부 검증 후 종료되지만 시작한 컨테이너는 stop할 때까지 유지된다. 기본 설정은 인터넷에서 접속할 수 있는 터널을 만들지 않는다. 실제 웹 연결은 사용자 승인과 계정 등록이 필요하며, CI 성공으로 그 연결을 대신하지 않는다. Docker나 OS 관리자 설정을 자동 변경하지 않는다.

긴 대화의 Goal·Loop·Compact는 별도 브라우저 계층이다. CoS와 via Agents의 비교는 [커뮤니티 비교](research/community-web-runtime-2026-11-15.md)에 있다. 런타임, 브라우저 자동 진행, Git 저장을 같은 기능으로 혼동하지 않는다.

## 기존 기록·검증 보조 도구

보조 도구 자체는 Python 3.12 이상과 Git으로 실행하며 추가 Python 패키지를 요구하지 않는다.

```sh
python -m workbench doctor
python scripts/check.py --require-git
python -m workbench context repo-intake --query "manual review"
python -m workbench run repo-intake test
python -m workbench run repo-intake demo
python -m workbench context reference-audit --query contract
python -m workbench run reference-audit test
```

receipt 경로를 확인한 뒤 `python -m workbench verify-receipt 프로젝트 receipt경로`로 검사하고 stdout.txt와 stderr.txt를 읽는다. 해시는 변경 검출 근거이지 서명이나 완전한 품질 인증이 아니다. context는 BRIEF와 STATE를 우선 포함하는 문자열 검색이다. --budget은 토큰 수가 아니라 본문 문자 수다.

## 소규모 프로젝트를 독립 폴더로 내보내기

```sh
python -m workbench export repo-intake ../repo-intake-independent
cd ../repo-intake-independent
python -m workbench doctor
python -m workbench run repo-intake test
```

기존 목적지에는 덮어쓰지 않고 다른 프로젝트·Git 이력·.env는 자동 복사하지 않는다. 선언한 파일의 비밀값까지 자동 검사하지는 않으므로 공개 가능한 자료만 사용한다.

새 소규모 작업은 별도 폴더에 BRIEF, STATE, DECISIONS, RESEARCH, sources.json, 실행 코드와 테스트를 두고 workbench/catalog.json에 새 id를 등록한다. inputs에는 실제 읽는 파일을 포함하고 tasks에는 검토한 Python argv와 최대 120초 제한을 기록한다. 프로젝트 등록만으로 공통 acceptance 실행 범위가 확대되지는 않는다. 제품의 완료 조건은 그 제품의 실제 테스트로 별도 검증한다.

## 다음 대화 시작

저장소·계정·작업 브랜치의 최신 커밋을 확인하고 AGENTS.md, STATE.md, 이 파일을 읽는다. 실제 실행 기록과 검사 커밋을 대조한 뒤 필요한 프로젝트의 문서만 읽는다. 현재 MCP가 연결돼 있지 않다면 연결된 것처럼 도구를 호출했다고 쓰지 않는다. 이미 완료된 연결 시험을 계속 반복하지 않고 남은 실제 연결 조건부터 확인한다.

## CI와 백업

workbench.yml은 이전 Python 보조 환경과 두 실습을 검사한다. community-runtime.yml은 실제 원본 컨테이너와 MCP 통합을 검사한다. main 자동 병합·배포는 없다. 기존 workbench 아티팩트는 7일, 커뮤니티 런타임 증거는 14일 보관한다. Git bundle은 Git 객체·참조용으로 DB, 이슈, 비밀값, LFS 내용, 미커밋 파일의 완전한 백업이 아니다.

## 자동 실행의 경계

보조 도구는 검토된 작업 한 번을 실행한다. MCP 엔진은 명령 세션을 제공한다. CoS 같은 별도 브라우저 도구는 후속 메시지와 대화 교체를 관리할 수 있다. 현재 대화에 마지막 계층을 연결하지 않았으므로 무인 모델 작업을 시작했다고 보고하지 않는다. 새 연결·권한·비밀정보·유료 자원 사용은 승인 경계를 유지한다.
