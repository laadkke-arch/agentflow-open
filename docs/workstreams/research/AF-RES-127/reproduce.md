# AF-RES-127 재현

GitHub의 과제 브랜치에서 확인할 SHA를 checkout하고 저장소 루트에서 아래 명령을 실행한다. Python 3.12, Node 24, npm 11과 Chromium 156.0.8078.79를 사용했다. 패키지 설치에는 npm registry 접근이 필요하고, fixture 페이지는 번들을 inline으로 실행하며 네트워크 요청을 막는다.

```sh
cd docs/workstreams/research/AF-RES-127
af127_cache=$(mktemp -d /tmp/af127-npm.XXXXXX)
af127_run=$(mktemp -d /tmp/af127-run.XXXXXX)
npm --cache "$af127_cache" --prefix fixture ci --no-audit --no-fund
node replay/drive.mjs --mode all --out "$af127_run" --chromium /usr/bin/chromium
```

`--mode all`은 본행·대조·보충을 순서대로 새 브라우저 컨텍스트에서 실행한다. `--mode pilot`은 두 동작이 꺼진 3자리만 보낸다. 단계별로 `main`, `controls`, `supplement`도 지정할 수 있다. 각 mode의 개별 JSON·environment.json과 공통 PNG를 출력 폴더에 쓴다. 출력은 새 경로를 사용한다. 1차 원장의 경로와 분석·재생 비교는 같은 폴더의 증거와 연결한다. [입력](plan.json) · [지문](fixture/fingerprints.json)
