# 고정 결과판 수용 확인

GitHub에서 새로 clone한 `0a4acb5368e2f064e9b3eb21b52d219de262440f`를 검사했다. clean 상태, 시작판과 비교한 변경 177개, 모두 AF-RES-123 소유 경로 안임을 확인했다. `git diff --check`도 종료 0이다. GitHub branch head 및 결과·자가 점검·검산 blob과 고정판 기능 절 3곳을 다시 열었다. [GitHub 확인](github.json) · [입력 SHA](input-commit.txt) · [변경된 경로](changed-paths.txt) · [원장 지문](ledger-sha256.txt) · 공통 검사 stdout의 마지막 빈 줄 한 줄을 정리했다.

| 단계 | 종료 | 명령과 출력 |
| --- | --- | --- |
| 계약 수용 | 0 | [명령](manifest.command.txt) · [stdout](manifest.stdout.txt) · [stderr](manifest.stderr.txt) |
| 공통 클라우드 검사 | 0 | [명령](cloud.command.txt) · [stdout](cloud.stdout.txt) · [stderr](cloud.stderr.txt) |
| 공통 검사 | 0 | [명령](base-check.command.txt) · [stdout](base-check.stdout.txt) · [stderr](base-check.stderr.txt) |
| 고정 npm 설치 | 0 | [명령](npm-ci.command.txt) · [stdout](npm-ci.stdout.txt) · [stderr](npm-ci.stderr.txt) |
| matrix | 0 | [명령](matrix.command.txt) · [환경·입력](matrix.environment.json) · [stdout](matrix.stdout.txt) · [stderr](matrix.stderr.txt) |
| controls | 0 | [명령](controls.command.txt) · [환경·입력](controls.environment.json) · [stdout](controls.stdout.txt) · [stderr](controls.stderr.txt) |
| 독립 계산 코드 | 0 | [명령](audit.command.txt) · [stdout](audit.stdout.txt) · [stderr](audit.stderr.txt) · [비교](verification.json) |

직접 manifest check는 원격 통합 head `a47cbbeb432dcaddf3431ac3388add5ab0a65845`와 의존을 대조해 `remote_checked`로 통과했다. 공통 검사에 포함된 자동 탐색은 `no_active_sessions`이므로 이 과제의 계약은 명시적인 manifest 명령의 결과로 판단한다. 여기의 제품 동작 관측은 하나의 Codex Cloud 작업자와 두 종류 렌더러의 실제 mouse IO다. 같은 작업자가 로그 검산을 수행했다.

고정 결과판에서 install부터 다시 실행한 본 48/48과 대조 36/36은 1차 원장에 있는 84/84와 동일했다. time 필드와 rAF 시각을 제외한 event·scenegraph·투영·색과 표면 fingerprint를 대조했다. 제3자의 검토·저자 도구 채택·키보드/터치 및 원 GIF는 이 검사 범위에 포함되지 않았다.
