# 재생 절차

실험은 Debian 13 amd64, Python 3.12, Pandoc 3.6, TeX Live Debian 패키지, Chromium에서 수행했다. 명령을 다시 돌리면 새 작업 디렉터리에서 출력이 생긴다. [도구·포맷·패키지 지문](environment.json) · [실행 인자와 종료값](runs.jsonl)

## 1. 원 입력과 고정 파일

결과 checkout 루트에서 시작한다. 원문 첫 TeX 코드 블록을 UTF-8 및 LF로 저장한다. Markdown 코드 블록 바깥의 기본 들여쓰기는 제외하고, 블록 안 탭 들여쓰기는 각각 ASCII 공백 4개로 복원한다. 마지막 LF를 하나 둔다. [원문 첫 코드 블록](https://stackoverflow.com/revisions/5938869D-E61B-410C-97F5-035731293446/view-source)

```bash
AF099_REPO="$PWD"
AF099_STUDY="$AF099_REPO/docs/workstreams/research/AF-RES-099"
AF099_TOOLS="$(mktemp -d /tmp/af099-tools.XXXXXXXX)"
export AF099_TOOLS

# example.tex는 위 GUID 원문 또는 아래 API에서 저장한다.
sha256sum "$AF099_TOOLS/example.tex"
# 12b9969b2a0556c2a43933046a4a0b914a3911c7a97c22bb18425f4eb1aec9bc

git fetch --no-tags origin work/research-af-res-096
git show 1d399f630930d2763459e16509c5224b0cded9a0:docs/workstreams/research/AF-RES-096/evidence/pandoc/p4-raw-tikz.lua > "$AF099_TOOLS/p4-raw-tikz.lua"
sha256sum "$AF099_TOOLS/p4-raw-tikz.lua"
# a63d10a7ee391a518ddf6f646a5714ebb902b00a3d4f608333d1c1f25581176c

(
  cd "$AF099_TOOLS"
  curl -fL -o pandoc-3.6-linux-amd64.tar.gz https://github.com/jgm/pandoc/releases/download/3.6/pandoc-3.6-linux-amd64.tar.gz
  printf '%s\n' '8e3702b195f75412e425df46f8f3f08241b66a2b33abbd9e04eda501bfde860c  pandoc-3.6-linux-amd64.tar.gz' | sha256sum --check
  tar -xzf pandoc-3.6-linux-amd64.tar.gz pandoc-3.6/bin/pandoc
  sha256sum pandoc-3.6/bin/pandoc
  # 7f1ac56064cdc02cdf8bd913f9ea45ba07fbb74419e755328c4571e4470769b2

  git init diagram
  git -C diagram remote add origin https://github.com/pandoc-ext/diagram.git
  git -C diagram fetch --depth=1 origin 023b31752cb5b63cd8bab828b268fa60ebd16d0c
  git -C diagram switch --detach FETCH_HEAD
  readlink diagram/diagram.lua
)
```

AF-RES-096의 API 방식은 `https://api.stackexchange.com/2.3/revisions/5938869D-E61B-410C-97F5-035731293446?site=stackoverflow&filter=%21R1.Y5iw_Z1WCrEMwmtA2p`의 `items`에서 해당 GUID의 `body` HTML을 꺼낸 뒤 첫 `pre`의 문자 데이터를 추출한다. 해당 body SHA-256은 `ddb73cf5ed41e2931fdefc58a7e180391b3741ca3b18ed7d0b8243a3f1ff28bf`다. 이번 셸은 HTTP 403을 받았고 GUID 화면에서 전사한 TeX가 동일 지문을 통과했다. [선행 고정 추출 코드](https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/post-pandoc/run-probes.py#L45-L84)

## 2. 작업 도구 준비

기본 이미지에서 `pdflatex`, `xelatex`, `kpsewhich`, `fmtutil-user`, `inkscape`, `chromium`과 TeX Live의 latex-base, latex-extra, latex-recommended, pictures, xetex 패키지를 사용한다. Python의 `playwright`, `PyMuPDF` 및 교차검사의 `Pillow` 판은 환경 원장에 있다.

실행에 없던 프로그램은 signed APT index에서 받아 사용자 권한의 연구 경로에 풀었다. 현재 APT 미러에 판이 남아 있는지 `apt-cache policy`로 조회할 수 있고, 관측한 아카이브 이름·지문은 환경 원장에 있다.

```bash
mkdir -p "$AF099_TOOLS"/apt/lists/partial "$AF099_TOOLS"/apt/cache/archives/partial "$AF099_TOOLS"/{debs,debian}
printf '%s\n' 'deb https://deb.debian.org/debian trixie main' > "$AF099_TOOLS/apt/sources.list"
AF099_APT=(-o "Dir::Etc::sourcelist=$AF099_TOOLS/apt/sources.list" -o Dir::Etc::sourceparts=- -o "Dir::State::lists=$AF099_TOOLS/apt/lists" -o "Dir::Cache=$AF099_TOOLS/apt/cache")
apt-get "${AF099_APT[@]}" update
(
  cd "$AF099_TOOLS/debs"
  apt-get "${AF099_APT[@]}" download \
    pdf2svg=0.2.4-1 mupdf-tools=1.25.1+ds1-6+deb13u1 \
    libmupdf25.1=1.25.1+ds1-6+deb13u1 libgumbo3=0.13.0+dfsg-2 libmujs3=1.3.6-1
  for package in *.deb; do dpkg-deb -x "$package" ../debian; done
)
python -B "$AF099_STUDY/run.py" formats --tools "$AF099_TOOLS" --output "$AF099_TOOLS/format-evidence"
python -B "$AF099_STUDY/run.py" calibrate --tools "$AF099_TOOLS" --output "$AF099_TOOLS/calibration"
```

`formats`는 `fmtutil-user --byfmt pdflatex` 및 xelatex를 새 format 경로에서 실행한다. 그 뒤 `TEXFORMATS`와 `MKTEXFMT=0`을 슬롯에 지정한다. 긍정 Q2-POS의 format 위치는 `kpsewhich -engine=pdftex -format=fmt pdflatex.fmt`로 조회한다. 단일 format을 제거하는 음성 순서는 Q2-NOFMT가 실행한다. FIRST-B를 별도로 재현하려면 원 TeX와 실제 동작하는 시스템 format에서 converter가 없는 PATH를 사용한다. [실제 FIRST-B 인자](runs.jsonl) · [FIRST-B 프로세스 trace](evidence/calibration/FIRST-B/trace.txt)

## 3. 6자리와 추가실행

```bash
python -B "$AF099_STUDY/run.py" matrix --tools "$AF099_TOOLS" --output "$AF099_TOOLS/matrix"
python -B "$AF099_STUDY/run.py" counterexample --tools "$AF099_TOOLS" --output "$AF099_TOOLS/counterexample"
python -B "$AF099_STUDY/audit.py"
```

- A 명령은 Pandoc 3.6에서 `--standalone -N --lua-filter=diagram.lua -f latex -t html example.tex -o example.html`이다. 각 슬롯에서 같은 basename의 symlink를 upstream 파일로 연결한다. 별도 관측 파일의 추가 코드는 문서·CodeBlock 콜백 로그만 내보낸다.
- B 명령은 Pandoc 3.6에서 `--standalone -N --from=latex+raw_tex --to=html5 --lua-filter=<봉인파일> --embed-resources example.tex --output=example.html`이다. 외부 호출 출력과 종료값은 그대로 전달하면서 활동 로그와 삭제될 중간 PDF를 PATH 래퍼가 복사한다. 사용자 인수 파일은 SHA-256 검증을 거친다.
- C는 원 TeX를 답의 PDF basename으로 컴파일한다. MuPDF 호출은 `mutool draw -oout.svg aff2748b-266e-48f5-b2f7-7547936bb6aa.pdf`다. 관측한 파일명은 `out1.svg`다. C+ 생성과 파일 제거 대조는 독립 디렉터리다.
- 기본 환경의 Chromium 파일 URL은 정책으로 차단됐다. Playwright의 오프라인 Chromium으로 실제 슬롯 바이트를 루프백 URL에 응답하고, 요청한 슬롯에 파일이 없으면 404를 공급한다. 이 자원 공급에는 서버가 필요 없다. 개별 file URL의 동작을 확인하려면 로컬 파일 접근이 되는 브라우저에서 B HTML 한 파일 및 C+의 HTML·SVG 한 쌍을 열면 된다.
- 산출물 원장에 파일 지문과 저장 위치가 있다. 로그·PDF 메타데이터·계측 URL은 새 실행에서 변할 수 있다. [의미와 바이트 일치의 별도 기준](RESULT.md#반복과-근거)

## 4. 다른 분야 및 원 시험

```bash
git init "$AF099_TOOLS/graphviz"
git -C "$AF099_TOOLS/graphviz" remote add origin https://gitlab.com/graphviz/graphviz.git
git -C "$AF099_TOOLS/graphviz" fetch --depth=1 origin 00d9fb4479c21b021e510dfb2633f1058d695db7

python -m venv "$AF099_TOOLS/jupyter"
"$AF099_TOOLS/jupyter/bin/python" -m pip install -r "$AF099_STUDY/evidence/cross-domain/upstream-tests/python-packages.txt"
python -B "$AF099_STUDY/cross_domain.py" --tools "$AF099_TOOLS" --output "$AF099_TOOLS/cross-output"

git init "$AF099_TOOLS/nbconvert-src"
git -C "$AF099_TOOLS/nbconvert-src" remote add origin https://github.com/jupyter/nbconvert.git
git -C "$AF099_TOOLS/nbconvert-src" fetch --depth=1 origin 2ba58585f649c1a2024aadd58007ec138457cc58
git -C "$AF099_TOOLS/nbconvert-src" switch --detach FETCH_HEAD
(
  cd "$AF099_TOOLS/nbconvert-src"
  export PATH="$AF099_TOOLS/jupyter/bin:$PATH"
  python -B -m pytest -q --color=no -p no:cacheprovider tests/test_nbconvertapp.py -k embedding_images_htmlexporter
  python -B -m pytest -q --color=no -p no:cacheprovider tests/exporters/test_html.py -k png_metadata
)
```

WPT 하네스 및 Graphviz 전용 회귀 하네스는 실행 범위 밖이다. GitLab 고정 Graphviz fixture는 현재 dot에서 직접 변환해 기대 XML을 비교했다. nbconvert 선택 시험 3건을 직접 실행했다. [각 비교 명령·해시, 결과](evidence/cross-domain/cross-results.json) · [선택 시험 로그](evidence/cross-domain/upstream-tests/)
