# AF-RES-255 재생

원형 진입점은 고정 WPT의 Chromium `./wpt run chrome`과 `webkitgtk_minibrowser` 제품의 정규 `wptrunner.wptrunner:main`이다. `_venv3/bin/python -c`는 저장소의 로컬 모듈 경로를 초기화하고 등록된 runner main을 호출한다. `.html`·참조·폰트 및 추적된 runner 코드는 WPT 체크아웃에서 그대로 읽는다. `config.json`은 무추적 서버 설정으로, localhost 및 충돌하지 않는 포트를 정한다. 두 표본은 HTTP와 같은 출처의 Ahem을 사용한다. `--reftest-screenshot always`로 성공한 비교의 캡처도 남긴다. [WPT runner 캡처 코드](https://github.com/web-platform-tests/wpt/blob/5ad65d6ea6c649696be2d0cf5188dfdb43f8d801/tools/wptrunner/wptrunner/executors/base.py#L532-L598).

`reftest.py`는 시험 하나마다 별도의 runner·WebDriver 및 프로필을 사용한다. 포트 중복을 피하기 위해 원형을 순차 실행한다. 각 `receipts/primary/{run_id}`의 `command.json`, `stdout.txt`, `stderr.txt`, `wptreport.json`과 `raw.jsonl.gz`가 원 실행 기록이다. `summary.json`은 raw의 `test_end` 1개와 report를 교차 확인하고, 같은 이벤트의 Base64를 `input.png`와 `reference.png`로 복원한 뒤 RGBA 채널의 정확 차이와 SHA-256을 저장한다. `diff.png`의 자홍 픽셀은 차이 위치다. `bbox_xyxy_exclusive`의 오른쪽·아래 끝은 제외한다. WPT 판정은 runner가 기록한 상태이며 재계산 픽셀 수는 보조 근거다.

## 고정 설치 및 호출

다음은 작업 checkout에서의 기준 절차다. `env.json`과 `receipts/setup/versions.json`에 실제 패키지 Version·Architecture, 도구판, 실행 파일 SHA-256이 있다. ChromeDriver는 Debian `chromium-driver_156.0.8078.79-1~deb13u1_amd64.deb`에서, MiniBrowser와 GTK WebCore는 WebKitGTK Debian security `libwebkit2gtk-4.1-0_2.54.3-1~deb13u1_amd64.deb`에서 가져왔다. WebKitWebDriver와 JavaScriptCore도 `2.54.3-1~deb13u1`이다. 같은 판의 Chromium 실행 파일이 `/usr/bin/chromium`에 있다. 수집에 사용한 Debian [Chromium pool](https://deb.debian.org/debian/pool/main/c/chromium/) 및 [WebKitGTK security pool](https://deb.debian.org/debian-security/pool/updates/main/w/webkit2gtk/).

```bash
# Bash. AF255_OUT을 매번 새 경로에 둔다.
AF255_OWNED="$PWD/docs/workstreams/research/AF-RES-255"
AF255_WPT=/tmp/afres255-wpt
AF255_PIN=5ad65d6ea6c649696be2d0cf5188dfdb43f8d801
AF255_OUT=$(mktemp -d /tmp/af255-replay.XXXXXX)
export PYTHONDONTWRITEBYTECODE=1

# 기존 고정 checkout이 없는 경우의 WPT 준비
git init "$AF255_WPT"
git -C "$AF255_WPT" remote add origin https://github.com/web-platform-tests/wpt.git
git -C "$AF255_WPT" fetch --depth=1 origin "$AF255_PIN"
git -C "$AF255_WPT" checkout --detach "$AF255_PIN"
cp "$AF255_OWNED/wpt-config.json" "$AF255_WPT/config.json"
cd "$AF255_WPT"
./wpt run --no-pause-after-test --list-tests --test-type reftest -y \
  --binary /usr/bin/chromium --webdriver-binary /tmp/afres255-net/chromium/usr/bin/chromedriver \
  chrome css/css-text/white-space/text-wrap-balance-002.html css/css-text/white-space/text-wrap-balance-003.html
git rev-parse HEAD HEAD:css/css-text HEAD:fonts
git diff --exit-code HEAD
git ls-tree -r --name-only HEAD css/css-text | LC_ALL=C sort | sha256sum
git grep -ilE '(text-wrap(-style)?[[:space:]]*:[^;{}]*balance|valdef-text-wrap-balance)' HEAD -- css/css-text \
  ':(exclude,glob)**/reference/**' ':(exclude,glob)**/*-ref.*' ':(exclude,glob)**/*-notref.*' ':(exclude,glob)**/support/**'
```

패키지는 Debian 인덱스에서 `apt-get download` 또는 pool의 `.deb`를 받아 `dpkg-deb -x`로 `/tmp`에 펼친다. `env.json.packages`의 Version·해시를 대조한다. Chromium driver의 추출 루트는 `/tmp/afres255-net/chromium`, WebKitGTK 세 패키지와 Xvfb·보조 라이브러리의 추출 루트는 `/tmp/afres255-net/gtk`다. Xvfb를 `:87 -screen 0 1280x1024x24 -nolisten tcp -noreset`로 시작한 뒤 `DISPLAY=:87 xrandr --current`를 실행한다. 기존 두 경로를 사용할 경우 SHA와 실행판을 대조한 뒤 다음을 수행한다. `libexec` C 코드는 Debian 패키지에 들어 있는 네 파일의 절대 경로만 추출 위치로 연결한다. 빌드된 브라우저·드라이버·WebCore 파일은 패키지의 바이트 그대로다. 재생은 Chromium의 `--no-sandbox`와 GTK의 브라우저 샌드박스 해제 및 소프트웨어 렌더링을 포함한 해당 환경에서 고정 공개 입력을 localhost로 연다.

```bash
AF255_CHROME_DRIVER=/tmp/afres255-net/chromium/usr/bin/chromedriver
export AF255_WEBKIT_ROOT=/tmp/afres255-net/gtk DISPLAY=:87
export AF255_WEBKIT_SHIM="$AF255_OUT/af255-libexec.so"
AF255_MINIBROWSER="$AF255_WEBKIT_ROOT/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser"
gcc -Wall -Wextra -Werror -fPIC -shared -o "$AF255_WEBKIT_SHIM" "$AF255_OWNED/webkit-libexec.c" -ldl
python "$AF255_OWNED/reftest.py" --wpt "$AF255_WPT" --engine chromium --engine webkitgtk \
  --chromium-driver "$AF255_CHROME_DRIVER" --webkit-binary "$AF255_MINIBROWSER" \
  --webkit-driver "$AF255_OWNED/webkit-driver.sh" --output "$AF255_OUT/primary" --profiles "$AF255_OUT/runner-profiles"
```

픽셀 검산의 입구는 출력의 원 report, 두 PNG 및 diff다. 동일 장면이라도 엔진 사이 PNG SHA가 달라질 수 있다. 비교는 같은 엔진의 입력·참조이며, `runs.csv`에서 로컬·공개 제출을 구별한다. 기존 도구의 `/etc/hosts` 사전 검사와 브라우저 기동 실패는 `receipts/setup/`에 있다. 원형 종료 값과 사전 준비 실패는 독립적으로 다룬다.

## 단어, 합성 통제, cue

`geometry.py`는 원형과 다른 프로세스·프로필에서 로컬 HTTP 서버로 정확히 같은 bytes를 읽는다. `measure.js`는 글자를 분리해 감싸거나 CSS를 주입하는 대신 텍스트 노드 내 DOM Range의 좌표를 읽는다. CSS px와 폰트 advance를 기록하며 `br`는 단어 식별용 텍스트 경계로 표현한다. 수평 LTR, 동일 폰트의 이 입력에서 같은 블록 y의 허용 오차는 0.5 CSS px다. 데이터에는 `fontEvents`, `fontResources`, `faces`, HTTP status·font payload SHA와 `documentWidth`가 포함된다. 로드 이벤트 수집을 위해 별도 계측 서버에서 폰트 응답을 350ms 늦춘다. Chromedriver는 eager, WebKitGTK는 normal navigation이다.

합성 C1·W7는 각기 width 8ch·7ch에 Ahem 20px와 normal gaps를 둔다. `-forced`는 word 2 뒤에 `br`를 삽입하고 나머지 CSS를 유지한다. 별도 002 변형은 word 2 또는 3 뒤에 `br`를 두며 원 입력 경로에서 실행하지 않는다. `missing-font`는 다른 HTTP 포트에서 해당 TTF 요청만 404로 응답한다. CSS 선언과 HTML byte는 보존한다. 002/003의 진단 결과는 별도 픽셀 비교이며 WPT 공식 PASS 모집에 산입하지 않는다.

`controls`의 W7 후속 시험은 명시 cut 1;3과 동일 텍스트의 `calc(7ch + 0.015625px)` 및 `calc(7ch + 1px)` auto/balance다. `font-audit`는 포트의 별도 calibration 문서 및 원문을 담은 same-origin iframe에서 FontFaceSet 이벤트를 시도한다. WebKitGTK 이벤트가 수신되지 않았던 영수증과 실제 TTF HTTP 응답을 같이 남겼다.

cue 원본은 `manifest.json`의 고정 `cue_fixture.url`을 다운로드한다. 두 cue의 raw line과 시각을 정적 추출한 뒤 브라우저가 `<track>`을 `hidden`으로 읽은 `VTTCue`에서 검산한다. 42ch·20ch 컨테이너에서 `pre-line`으로 두 cue 텍스트를 재배치한다. 이 높이와 줄은 일반 DOM 통제이며 비디오 오버레이나 읽기 선호 실험의 범위 밖이다.

```bash
AF255_VTT="$AF255_OUT/sintel-en.vtt"
curl -fSL 'https://raw.githubusercontent.com/mdn/shared-assets/f160bcf2db52b60820a7728aa9b3fa88568cfc38/misc/sintel-en.vtt' -o "$AF255_VTT"
sha256sum "$AF255_VTT"
for af255_mode in original controls missing-font captions; do
  python "$AF255_OWNED/geometry.py" --wpt "$AF255_WPT" --engine chromium \
    --binary /usr/bin/chromium --driver "$AF255_CHROME_DRIVER" --mode "$af255_mode" \
    --output "$AF255_OUT/measured" --profiles "$AF255_OUT/measure-profiles" --vtt "$AF255_VTT"
  python "$AF255_OWNED/geometry.py" --wpt "$AF255_WPT" --engine webkitgtk \
    --binary "$AF255_MINIBROWSER" --driver "$AF255_OWNED/webkit-driver.sh" --mode "$af255_mode" \
    --output "$AF255_OUT/measured" --profiles "$AF255_OUT/measure-profiles" --vtt "$AF255_VTT"
done
```

## 대표 재생과 비교

작업 결과 SHA를 별도 checkout에 놓고 `AF255_OWNED`를 그 경로로 바꾼다. 같은 WPT 핀과 바이너리에서 `reftest.py --engine chromium --test 003 --repeat 3 …`과 `geometry.py --engine chromium --mode original --test 003 --repeat 3 …`을 새 출력·프로필 폴더로 실행한다. 이어 `--mode controls`로 C1 강제 경계를 다시 검사한다. `--repeat 3`은 기본 8회와 구분하는 이름이다. 비교는 PNG SHA·diff 픽셀, `blocks[].words[].fragments`·`rows`, 폰트 SHA와 HTTP 상태다. 시각, WebDriver session id, 포트는 매 실행 바뀐다.

마지막에 `python -m workbench.session check docs/workstreams/research/AF-RES-255/session.json --fetch`와 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`을 고정 checkout에서 실행한다. 일반 `cloud_check.py`는 저장소의 기존 검사이며 이 폴더의 WPT 증거를 재생하지 않는다. `collect.py`는 체크인한 `receipts/primary/`와 `receipts/geometry/`를 읽어 `runs.csv`와 `words.csv`를 생성한다.
