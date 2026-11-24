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

## 원장과 고정판을 검산

앞에서 만든 `af127_run`에 파일럿을 추가하면 3+16+12+10자리를 비교할 수 있다. `compare.py`는 timeOrigin·clock·eventTime과 브라우저 notices를 비교에서 따로 둔다. 이벤트 순서, handler 반환, 좌표, 선택, Canvas 표면 PNG, 버전 및 입력 SHA를 대조한다. Canvas readback 경고 횟수는 보고서에 보존한다.

```sh
node replay/drive.mjs --mode pilot --out "$af127_run" --chromium /usr/bin/chromium
python -B replay/analyze.py --evidence "$af127_run" --output "$af127_run/runs.jsonl"
python -B replay/compare.py --reference evidence --candidate "$af127_run" --report "$af127_run/compare.json"
python -B replay/audit.py --report "$af127_run/recount.json"
```

GitHub에서 고정 결과 SHA를 받아 두 새 checkout에서 검사하는 진입점이다. `full`을 넘긴 경로에서 명시 세션 체크와 저장소 공통 검사도 실행한다. `RESULT_SHA`는 [수용 영수증](evidence/acceptance/RECEIPT.md)의 실제 검사 결과 SHA를 넣는다. 아래는 이 폴더에서 실행한다.

```sh
af127_verify=$(mktemp -d /tmp/af127-verify.XXXXXX)
bash replay/accept.sh "$RESULT_SHA" "$af127_verify/route-1" full
bash replay/accept.sh "$RESULT_SHA" "$af127_verify/route-2"
python -B replay/compare.py --reference "$af127_verify/route-1/run" --candidate "$af127_verify/route-2/run" --commit "$RESULT_SHA" --report "$af127_verify/cross.json"
```

고정 소스 바이트는 아래 비교를 반복할 수 있다. 파일명은 [지문 목록](fixture/fingerprints.json)의 하나로 두고, lock과 동일한 tarball integrity/sha256 및 바이너리 입력을 확인한다.

```sh
af127_module=interaction/Translate.js
af127_pin=88fc44564552176b761dbb9531f9977386d041c0
curl -fsSL "https://raw.githubusercontent.com/openlayers/openlayers/$af127_pin/src/ol/$af127_module" -o "$af127_run/source.js"
curl -fsSL 'https://registry.npmjs.org/ol/-/ol-10.11.0.tgz' -o "$af127_run/ol.tgz"
tar -xOf "$af127_run/ol.tgz" "package/$af127_module" > "$af127_run/distribution.js"
sha256sum "$af127_run/source.js" "$af127_run/distribution.js" "fixture/node_modules/ol/$af127_module" "$af127_run/ol.tgz"
```
