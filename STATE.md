# 현재 작업 상태

기준일: 2026-11-15
브랜치: `chore/workspace-foundation`
단계: 공통 작업환경 v0.1 구현 및 Linux·Windows 실행 검증 완료. 증거 출력과 CI 도구 정리 변경은 새 실행으로 재확인한다.

## 실제 완료

프로젝트별 기록 검색, 검토된 작업 실행, 입력·로그 해시가 포함된 결과 기록, 오래된 결과 거부, 프로젝트 하나만 독립 폴더로 내보내기가 구현됐다. Python 표준 라이브러리와 기존 Git/Actions를 사용하며 기본 실행에 별도 패키지나 비밀키가 필요하지 않다.

저장소 주소 정리(repo-intake)와 문서 출처 연결 검사(reference-audit)를 각각 구현하고 같은 공통 함수를 재사용했다. 각 프로젝트의 상태·결정·출처는 분리되어 있고, 새 프로세스의 context와 단독 export 시험에서 서로의 자료가 섞이지 않았다. Git bundle을 생성하고 검증한 뒤 새 폴더에서 같은 커밋으로 복원하여 demo를 실행했다.

## 확인한 코드와 실행

- 검증한 코드: `c48190a335228788c9ce41969259efce08c9913d`
- 실행: https://github.com/laadkke-arch/agentflow-open/actions/runs/43703974464
- Windows 3.12.10 및 Ubuntu 3.12.16에서 공통 검사 39개 통과, 건너뛴 검사 0개.
- 두 프로젝트 test·demo와 독립 export 후 test, Git 백업 복원 후 demo 모두 성공.
- 양쪽 실제 job 로그를 읽어 위 결과와 검사 커밋을 대조했다.
- 상세: docs/sessions/2026-11-15-path-recovery.json

최초 Windows 실행에서는 경로 별칭 문제로 14개 오류가 발생했다. 경로 기준을 통일하고 회귀 검사를 추가해 복구했으며, 기존 검사 기준은 유지했다. 빈 URL 인증 필드와 실행 중 입력 삭제 오류도 로컬에서 수정·검증했다.

## 이번 정리 변경과 다음 확인

프로젝트 상태 문서를 실제 검증 결과로 갱신하고, 두 프로젝트의 test/demo 원문 출력을 CI 로그에서도 볼 수 있도록 했다. 폐기 예정 Node 런타임 경고를 내던 upload-artifact v4 대신 공식 v7.0.2(Node 24)를 전체 커밋 SHA로 고정했다. 새 변경 커밋의 Actions에서 두 OS의 검사·백업·아티팩트 업로드가 다시 성공하는지 확인해야 한다. 이전 실행 결과를 새 커밋 전체가 검증됐다는 뜻으로 확장하지 않는다.

## 시작 위치

AGENTS.md, docs/START_HERE.md를 읽고 `python -m workbench context PROJECT --query 관련단어`로 해당 프로젝트만 탐색한다. 전체 확인 명령은 `python scripts/check.py --require-git`이다. 실행된 code SHA와 run URL을 확인한 뒤 미완료 항목을 선택한다.

## 아직 하지 않은 것

새 AI 대화의 실제 인수인계, 비공개 공통 저장소 분리, PC 원격 연결, Render·DB·탐색기 제품 구현은 미실시다. 현재 지원하는 실행기는 검토된 Python 작업용이며 OS 샌드박스나 비밀정보 검사기가 아니다. 자동 모델 호출·무기한 에이전트·정기 실행은 설정하지 않았다.

원문은 사용자가 제공한 텍스트를 참고했으며 최신 댓글을 열람한 것으로 표현하지 않는다. main, 기존 AgentFlow Studio, 계정 권한, 공개 범위, 유료 자원은 변경하지 않았다.
