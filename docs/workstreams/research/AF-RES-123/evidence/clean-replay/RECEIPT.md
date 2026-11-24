# 별도 checkout 재생 영수증

GitHub 작업 브랜치를 새 경로에 clone하고 `c8d5eed811b03c796efa25cc65924f94aa5dbe56`와 clean status를 확인했다. 잠금 파일로 새 prefix에 npm ci 후 Chromium을 따로 시작했다. 본 48과 대조 36을 동일 plan에서 다시 실행했다. [입력 커밋](input-commit.txt) · [설치 명령](npm-ci.command.txt) · [본행 명령](matrix.command.txt) · [대조 명령](controls.command.txt) · [분석 명령](analyze.command.txt)

| 단계 | 종료 | 환경·출력 |
| --- | --- | --- |
| 설치 | 0 | [stdout](npm-ci.stdout.txt) · [stderr](npm-ci.stderr.txt) |
| matrix | 0 | [환경](matrix.environment.json) · [stdout](matrix.stdout.txt) · [stderr](matrix.stderr.txt) |
| controls | 0 | [환경](controls.environment.json) · [stdout](controls.stdout.txt) · [stderr](controls.stderr.txt) |
| 분석 | 0 | [stdout](analyze.stdout.txt) · [stderr](analyze.stderr.txt) |

두 실행의 84개 원파일과 이벤트·첫 frame·다음 frame·색·결과 표면을 별도 계산으로 비교했다. 시스템 시각, event timestamp, driver 호출 시점 및 rAF 시각은 비교에서 제외했다. 다른 필드의 불일치는 없었다. raw SHA-256는 실행 시각 때문에 구분하며 두 번째의 84개 SHA는 검산 영수증에 있다. 같은 작업자의 별도 실행과 검산이다. [비교 영수증](../verification.json)
