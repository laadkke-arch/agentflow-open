# AgentFlow용 커뮤니티 웹 개발 런타임

직접 MCP 서버를 다시 만들지 않고 WebJjonku와 SpaceDock의 실제 구현을 사용한다. 이 폴더는 고정한 원본, 프로젝트별 기억 분리, Python 호환 설정, 설치 명령과 실제 통합 검사를 묶는다. 제품 탐색기는 아직 구현하지 않는다.

## 실행 구조

웹 대화 → 사용자 승인 MCP 연결 → 전용 컨테이너의 파일 편집·명령·작업 세션·기억 → Git 기록. GitHub Actions는 독립 검사에 사용하며, 모든 작은 편집마다 Actions를 거칠 필요는 없다. Render는 제품 배포용으로 유지한다.

이 런타임만으로 웹 대화가 끝난 뒤 자동으로 다음 프롬프트가 전송되지는 않는다. Goal·Loop·Compact를 제공하는 CoS 같은 브라우저 측 구성은 별도 계층이며 이 설치에 몰래 포함하지 않는다.

## PC 또는 승인된 Linux 서버에서 설치

Git, Python, Docker의 Linux 컨테이너 엔진과 Docker Compose가 필요하다. OS 권한 변경이나 Docker 설치는 이 스크립트가 자동 수행하지 않는다. Windows에서도 아래 Python 명령을 사용한다.

```sh
git clone --branch chore/workspace-foundation https://github.com/laadkke-arch/agentflow-open.git
cd agentflow-open
python integrations/web-runtime/manage.py setup
```

이미 복제한 작업 폴더가 있으면 덮어쓰거나 reset하지 말고 해당 브랜치와 미커밋 변경부터 확인한다. setup은 원본을 사용자 홈의 별도 캐시에 준비하고 Docker 이미지를 빌드한다. 기존 PC 프로젝트나 홈 폴더를 컨테이너에 마운트하지 않는다. 공개 저장소의 작업 브랜치만 전용 볼륨에 복제한다. 이미지 다운로드와 빌드에는 인터넷·디스크·CPU가 필요하다.

기본 setup은 공개 터널을 열지 않는다. 내부 연결·OAuth·파일 작업·명령 실행을 확인한 뒤 종료한다. 성공해도 ChatGPT 연결 완료를 뜻하지 않는다.

## 웹 연결 승인

작업 실행 서버를 HTTPS로 노출하는 데 동의한 뒤에만 다음 명령을 실행한다.

```sh
python integrations/web-runtime/manage.py connect --approve-public-endpoint
```

출력된 /mcp 주소를 사용 중인 웹 클라이언트의 사용자 지정 MCP 연결에 등록하고 OAuth 승인을 진행한다. 소유자 인증키는 본인 터미널에서만 다음 명령으로 확인하고 그 인스턴스 승인 화면에만 입력한다. 채팅·스크린샷·Git·CI 로그에 붙이지 않는다.

```sh
python integrations/web-runtime/manage.py owner-key
```

이 설치는 원본의 임시 Cloudflare 터널을 사용한다. 재시작 때 주소가 바뀔 수 있으며, 고정 주소나 사설 터널은 별도 연결 검토 대상이다. 웹 계정 로그인·앱 등록·권한 승인은 자동 수행하지 않는다.

## 연결 직후 실제 대화에서 확인

연결한 앱으로 다음 요청을 수행한다. 이 대화 시험은 설치 스크립트가 대신했다고 주장하지 않는다.

> agentflow-open 루트를 checkout 모드로 열고 AGENTS.md, STATE.md, docs/START_HERE.md를 읽어라. python3 -m workbench doctor와 repo-intake의 test를 실행하고 실제 종료 코드와 파일 변경을 보고하라. main 변경·원격 push·배포는 하지 마라. 완료한 사실과 아직 확인하지 않은 항목을 분리해라.

## 기억과 프로젝트 분리

SpaceDock 0.1.6 recall은 workspace_id가 아니라 root_id를 기준으로 보관한다. 기본 원본처럼 여러 프로젝트를 한 루트에 넣으면 그 프로젝트들의 recall이 공유된다. 여기서는 demo, agentflow-open, shared를 각각 별도 루트로 둔다. shared에는 명령 실행 권한을 부여하지 않는다. 새 프로젝트는 기존 루트 아래 폴더만 추가하지 말고 별도 허용 루트로 등록해야 한다.

이것은 자료의 논리적 구분이지 서로 적대적인 사용자 사이의 보안 격리가 아니다. 허용된 셸은 같은 컨테이너 사용자 권한으로 다른 볼륨 경로에도 접근할 수 있다. 서로 신뢰하지 않는 작업은 컨테이너 자체를 분리해야 한다.

Git에 남긴 상태·결정·출처가 장기 기록의 기준이다. recall에는 그 기록의 요약과 위치를 두고, 로컬 기억을 저장했다는 이유만으로 Git 백업이 완료됐다고 보지 않는다. /state 전체에는 인증 상태가 있으므로 공개 저장소에 복사하지 않는다.

## GitHub에 변경 반영

초기 런타임에는 GitHub 쓰기 인증정보를 넣지 않는다. 공개 브랜치를 읽어오는 clone과 컨테이너 내부 커밋은 가능하지만 원격 push 권한은 별도다. 현재 대화의 GitHub 연결로 검토한 변경을 반영하거나, 나중에 최소 권한의 Git 인증을 사용자 로컬에서 설정한다. MCP와 기존 GitHub 연결이 자동으로 같은 작업 폴더를 공유하는 것으로 가정하지 않는다. 기준 커밋과 실제 diff를 대조하고, 원격이 변했으면 먼저 차이를 확인한다.

## 사용 명령

```sh
python integrations/web-runtime/manage.py status
python integrations/web-runtime/manage.py verify
python integrations/web-runtime/manage.py stop
python integrations/web-runtime/manage.py start
```

stop과 컨테이너 재생성은 전용 named volume을 지우지 않는다. down -v 또는 volume prune은 사용하지 않는다. prepare는 수정된 원본 캐시를 덮어쓰지 않는다. 소스 커밋은 고정하지만 원본의 기본 이미지 태그와 apt 저장소까지 바이트 단위로 고정한 빌드는 아니다.

## 검증 범위

CI에서는 외부 네트워크 없는 컨테이너에서 실제 HTTP OAuth와 stdio MCP를 시험한다. 사용자 PC 설치, 공개 HTTPS 연결, 실제 웹 대화, 무인 모델 루프는 별도다. 원본 고지와 라이선스는 THIRD_PARTY.md 및 이미지 내부 고지를 따른다.
