# AF-RES-107 재현

## 입력과 도구

작업 경로에서 `inputs.json`의 Git pin과 SHA-256을 확인한다. T2의 원본은 PGFPlots 1.18.1 공개 시험과 AF-RES-103 고정 입력의 동일 바이트다. S 원본은 WPT HTML, D는 Graphviz Heawood 원 DOT다. 후보 모집 목록과 사전 기대는 별도 파일이다. [원본](inputs.json) · [선정](SCOPE.md) · [판정 기준](protocol.json) · [판·폰트 SHA](environment.json)

당시 환경은 Debian 13, Python 3.12, pdfLaTeX/pdfTeX 1.40.26, PGFPlots 1.18.1/PGF 3.1.10의 설치 패키지와 Computer Modern Type 1, Graphviz 2.42.4와 Liberation Sans, Chromium 156.0.8078.79이다. Python 의존성은 [환경 원장](environment.json)의 PyMuPDF·Pillow·NumPy·Playwright 네 판을 사용한다. Graphviz 출력 모듈은 `-Tsvg`·`-Tjson` 둘 다 필요하다. `gs` 10.05.1은 상류 PS를 그려볼 때 쓴다. `pdflatex`의 포맷 위치를 확인할 때 `kpsewhich -engine=pdftex -format=fmt pdflatex.fmt`를 쓴다.

이 코드를 받은 새 checkout에서 다음을 실행한다. WPT 보조 스크립트는 고정 원격에서 가져와 동작 전에 지문을 비교한다. 이후 렌더에는 Playwright의 오프라인 HTTP 라우트로 그 파일의 바이트만 공급한다. 각 ID마다 새 임시 디렉터리의 사본에만 patch를 적용한다. WPT timestamp는 브라우저에서 2.000s로 정해 화면을 찍는다. PDF는 현재 UTC 메타데이터를 쓴다.

```sh
cd docs/workstreams/research/AF-RES-107
af107_run=$(mktemp -d /tmp/af107-replay.XXXXXXXX)
mkdir -p "$af107_run/wpt"
python -B - "$af107_run/wpt" <<'PY'
from hashlib import sha256
import json, pathlib, sys, urllib.request
out = pathlib.Path(sys.argv[1]); case = json.loads(pathlib.Path('inputs.json').read_bytes())['cases']['S']
for name, spec in case['support'].items():
    with urllib.request.urlopen(spec['raw'], timeout=30) as response:
        data = response.read()
    assert sha256(data).hexdigest() == spec['sha256'], name
    (out / name).write_bytes(data)
PY
python -B run.py environment --output "$af107_run/environment.json"
python -B run.py baseline --wpt-support "$af107_run/wpt" --output "$af107_run/baseline"
python -B run.py matrix --wpt-support "$af107_run/wpt" --output "$af107_run/matrix"
python -B run.py controls --wpt-support "$af107_run/wpt" --output "$af107_run/controls"
python -B verify.py --evidence "$af107_run"
python -B verify.py
```

1회씩 다시 보려면 `--slot T-one-B-1`, `--slot S-base-1` 또는 `--slot D-chain-B`를 해당 `matrix`, `baseline`, `controls` 명령에 붙이고 빈 출력 폴더를 준다. 도구 경로는 `--pdflatex`, `--dot`, `--chromium`으로 넘긴다. `git apply --whitespace=nowarn`은 원 TeX의 기존 주석 공백을 보존한다. `pdflatex`는 `-no-shell-escape`와 `-halt-on-error`로 실행한다. DOT는 `dot -v -Tsvg -ooutput.svg -Tjson -ooutput.dot.json input.gv` 한 프로세스의 SVG/JSON을 사용한다.

`verify.py`는 각 영수증의 사본·patch·파일 SHA를 확인하고, PDF 그리기 명령과 글자·PNG를 원 PDF에서 다시 읽는다. SVG 마커의 DOM 참조·paint는 저장 XML에서 찾고 픽셀을 다시 샘플한다. DOT에서는 원 SVG endpoint와 JSON 객체, 색과 화면 샘플을 다시 대조한다. 새 실행의 raw PDF 생성·수정 날짜와 ID는 달라질 수 있다. 두 영역의 정확한 색·보존, 644 관측 행, 15/15 의미 쌍이 당시 실행에서 검산됐다. [영수증 원장](runs.jsonl) · [요소별 값](elements.csv) · [검산 결과](evidence/verification.json)

## 별도 상류 회귀 6건과 PS 보기

```sh
mkdir -p "$af107_run/source-cases"
python -B - "$af107_run/source-cases" <<'PY'
from hashlib import sha256
import json, pathlib, sys, urllib.request
out = pathlib.Path(sys.argv[1]); specs = json.loads(pathlib.Path('evidence/upstream/support-inputs.json').read_bytes())
for spec in specs.values():
    for k in ('input','expected'):
        if k in spec:
            item = spec[k]
            with urllib.request.urlopen(item['url'], timeout=30) as response:
                data = response.read()
            assert sha256(data).hexdigest() == item['sha256'], item['file']
            (out / item['file']).write_bytes(data)
PY
python -B support_replay.py --inputs "$af107_run/source-cases" --output "$af107_run/supporting"
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r96 \
  -sOutputFile="$af107_run/Heawood-expected.png" evidence/upstream/Heawood.ps
```

GitLab raw의 HTTP가 제한된 곳에서는 [상류 Graphviz Git](https://gitlab.com/graphviz/graphviz)에서 정확한 `00d9fb4479c21b021e510dfb2633f1058d695db7`과 [기록된 tests 경로](evidence/upstream/support-inputs.json)를 `git show SHA:경로`로 같은 이름에 저장한다. WPT도 같은 방식으로 `03d41fe0fe3338c66cb56644b8a1705fe2e7247b:resources/파일명`을 가져올 수 있다. 공식 WPT 전체 실행기와 공식 Graphviz 전체 suite는 미실시다. [실행 범위](evidence/CONTROLS.md)

## 저장판 검사

원격 결과 SHA의 깨끗한 Git checkout 루트에서 실행한다. 실제 영수증과 활성 세션 수는 마지막 [HANDOFF](HANDOFF.md)에 있다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-107/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B docs/workstreams/research/AF-RES-107/verify.py
```
