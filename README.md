# AgentFlow Open 공통 작업환경

## 새 세션·탐색기 제품 시작점 (2026-11-19)

이 공통 작업환경은 **오픈소스·웹사이트·무료/유료 서비스 발견 및 프로젝트 적합성 비교**를 위한 기반이다. 작업환경 코드와 실제 탐색기 제품은 별개이며, 제품 DB·웹서비스·배포는 아직 구현하지 않았다.

- **제품 목적과 결정:** [docs/product/README.md](docs/product/README.md)
- **조사 기준:** [docs/product/RESEARCH_PROTOCOL.md](docs/product/RESEARCH_PROTOCOL.md)
- **DB 초안·범위:** [docs/product/DATA_MODEL_DRAFT.md](docs/product/DATA_MODEL_DRAFT.md), [ROADMAP.md](docs/product/ROADMAP.md)
- **3개 ChatGPT 웹 세션의 시작 지시문:** [docs/collaboration/SESSION_STARTS.md](docs/collaboration/SESSION_STARTS.md)
- **이슈/브랜치/인수인계:** [docs/collaboration/README.md](docs/collaboration/README.md), [STATUS_BOARD.md](docs/collaboration/STATUS_BOARD.md)

실제 기준은 `chore/workspace-foundation` 브랜치의 최신 파일이다. 다른 웹 채팅은 GitHub 기록을 **직접 읽고** 시작한다. 브랜치 생성은 자동 AI 실행이 아니며, 공개 저장소에 개인/비공개 자료를 넣지 않는다.

탐색기 제품을 만들기 전에, 조사·작은 구현·검증·기록 검색·다른 프로젝트 재사용을 실제로 실행하는 작업환경입니다. 제품 UI, DB, Render 서비스는 아직 만들지 않습니다. 기존 AgentFlow Studio와 main은 변경하지 않습니다.

현재 작업 브랜치는 `chore/workspace-foundation`입니다. 최종 실행 결과는 [STATE.md](STATE.md), 시작 안내는 [docs/START_HERE.md](docs/START_HERE.md)를 읽으세요.

## 바로 실행

Python 3.12 이상과 Git을 사용합니다. 기본 실행에 pip 설치, API 키, 외부 네트워크는 필요하지 않습니다. Windows에서는 `python` 대신 설치된 `py -3.12`를 사용할 수 있습니다.

```sh
python -m workbench doctor
python -m workbench list
python -m workbench context repo-intake --query contract
python -m workbench run repo-intake test
python -m workbench run repo-intake demo
python -m workbench run reference-audit test
python scripts/check.py
```

Git으로 받은 작업 폴더에서 전체 백업 복원 시험까지 강제하려면 `python scripts/check.py --require-git`를 사용합니다. Actions도 같은 명령을 실행합니다.

## 실제로 들어 있는 기능

| 기능 | 실행 또는 저장 위치 |
| --- | --- |
| 프로젝트 선택과 상태·결정 검색 | `python -m workbench context PROJECT --query WORDS` |
| 검토된 작업 실행, 시간 제한, 실패 로그 | `python -m workbench run PROJECT TASK` |
| 실행 시 입력 파일 해시와 코드 버전 보관 | `.workbench/runs/PROJECT/RUN/receipt.json` |
| 오래된 입력·수정된 로그·다른 프로젝트 결과 거부 | `python -m workbench verify-receipt PROJECT PATH` |
| 다른 프로젝트를 제외한 독립 실행 묶음 내보내기 | `python -m workbench export PROJECT ../new-workspace` |
| 전체 검사와 Git 백업 복원 시험 | `python scripts/check.py --require-git` |

실행 결과 폴더는 Git에서 제외하고, CI는 지정된 결과 파일만 7일 보존 아티팩트로 올립니다. 영구적으로 필요한 판단과 검증 요약은 `docs/sessions/`에 따로 남깁니다.

## 두 개의 작업으로 검증

`lab/repo-intake`는 여러 형태의 GitHub 저장소 주소를 정리하되 파일·이슈 주소를 잘못 합치지 않는 실습입니다. `lab/reference-audit`는 조사 문서의 출처 연결과 중복 저장소 참조를 확인합니다. 두 번째 실습은 첫 번째의 공통 함수를 재사용하지만 상태·자료는 분리합니다. 둘 다 완성된 탐색기 제품은 아닙니다.

## 참고하고 채택한 것

Python의 URL 파서와 unittest, Git bundle, 공식 GitHub Actions를 사용합니다. w3lib, yarl, Nox, uv와 urllib3의 실제 Nox 설정을 비교한 이유는 [도구 선택 기록](docs/research/tool-decisions.md)에 있습니다. 후보를 전부 설치하지 않았으며 문서 확인과 직접 실행을 구분합니다.

## 권한과 한계

이 저장소는 공개입니다. 비밀키, 사용자 대화 원문, 고객 자료, 비공개 프로젝트를 넣지 마세요. 실행 명령은 검토된 project.json에서만 선택하지만 Python은 실행 계정의 권한을 가지므로 보안 샌드박스가 아닙니다. 이 환경은 모델을 자동 호출하거나 무기한 반복하지 않습니다. 새 AI 대화에서의 인수인계는 새 프로세스 시험과 별도입니다.

main 병합, 비공개 공통 저장소 생성, PC 원격 연결, 유료 서비스와 권한 변경은 별도 승인 대상입니다. Render는 나중에 제품을 배포할 때 사용합니다.

## 라이선스

이 프로젝트 자체의 공개 라이선스는 아직 결정하지 않았습니다. 외부 자료는 링크와 자체 요약으로 기록하며, 외부 프로젝트의 라이선스는 각 원 출처를 따릅니다.
