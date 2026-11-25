# AF-RES-264 재생

GitHub에서 `HANDOFF.md`가 가리키는 고정 결과 SHA를 체크아웃한다. 실험 입력은 [document.md](fixtures/document.md), 정확판 지문은 [downloads.json](fixtures/downloads.json), EPUB 원출처와 해시는 [epub.json](fixtures/epub.json)에 있다.

## 공통 환경과 폴더

실측은 Debian 13 x86-64, Python 3.12와 pypdf 6.21.4, pdfTeX 1.40.26/LaTeX2e 2024-11-01, article v1.4n, hyperref v7.01l, Latin Modern v1.6.1, Poppler 25.03.0이다. `prepare_tools.py`는 두 Pandoc 공식 .deb와 Debian MuPDF 1.25.1·해당 라이브러리를 지정한 임시 폴더에만 추출한다. 실제 태그와 내장 템플릿 지문을 재확인한다. `git`, `curl`, `dpkg-deb`와 위 TeX/Poppler/pypdf 환경이 필요하다. 기존 도구 폴더를 재사용할 경우 아래 `--tools`를 그 폴더로 지정할 수 있다. [실측 설치·클래스·패키지](receipts/matrix/v23-on-unique-r1/latex-file-list.txt) · [도구 지문](receipts/environment/tool-setup/packages.json)

```bash
export PYTHONDONTWRITEBYTECODE=1
task=docs/workstreams/research/AF-RES-264
tmp=$(mktemp -d)
python "$task/fixtures/prepare_tools.py" --tools "$tmp/tools" --receipts "$tmp/tool-setup"
python "$task/fixtures/run.py" matrix --tools "$tmp/tools" --output "$tmp/matrix"
python "$task/fixtures/run.py" controls --tools "$tmp/tools" --output "$tmp/controls"
python "$task/fixtures/read_epub.py" --output "$tmp/epub"
python "$task/fixtures/compare.py" --matrix "$tmp/matrix" --controls "$tmp/controls" --output "$tmp/comparisons.json"
python "$task/fixtures/verify.py" --replay-root "$tmp"
```

`verify.py`는 체크아웃의 아카이브와 최종 PDF를 먼저 읽고 새 실행의 AST·TeX·공통 TeX 읽은 파일·페이지·책갈피·고정 길이 날짜/ID 마스킹 PDF를 비교한다. 원바이트 일치 개수도 따로 보고한다. 다른 TeX 설치나 바이너리 지문으로 바뀌었다면 차이를 해당 새 환경 관측으로 남긴다.

## 1회 생성과 원판독

실행기는 매 회차 빈 폴더에서 동일한 이름으로 작업한다. 아래는 2.3 toc on/고유값 한 회의 손 재생이다. `TEXMFHOME`과 Pandoc data-dir에는 비어 있는 경로를 전달한다. 다른 셀은 켤 때만 `--toc`를 넘기고 고유값을 줄 때만 `--metadata=...`를 추가한다. YAML의 문서 제목은 그대로 둔다.

```bash
task="$(pwd)/docs/workstreams/research/AF-RES-264"
tools="$tmp/tools"
build=$(mktemp -d)
cp "$task/fixtures/document.md" "$build/document.md"
cd "$build"
mkdir empty-data
export LC_ALL=C.UTF-8 LANG=C.UTF-8 TZ=UTC TEXMFHOME="$build/empty-data"
unset SOURCE_DATE_EPOCH FORCE_SOURCE_DATE
pandoc="$tools/bin/pandoc-2.3/usr/bin/pandoc"
args=(--data-dir=empty-data -f markdown --toc '--metadata=toc-title:Archive Contents 264')
"$pandoc" "${args[@]}" -t json document.md > ast.json
"$pandoc" "${args[@]}" -s -t latex document.md > case.tex
for pass in 1 2 3; do
  mkdir "pass-$pass"
  status=0
  pdflatex -interaction=nonstopmode -no-shell-escape -halt-on-error -file-line-error \
    -recorder -jobname=case '\listfiles\input{case.tex}' \
    > "pass-$pass/pdflatex.stdout" 2> "pass-$pass/pdflatex.stderr" || status=$?
  printf '%s\n' "$status" > "pass-$pass/pdflatex.exit"
  for file in case.log case.aux case.toc case.out case.fls case.pdf; do
    if test -f "$file"; then cp "$file" "pass-$pass/"; fi
  done
  if test "$status" != 0; then break; fi
done
export LD_LIBRARY_PATH="$tools/bin/mupdf/usr/lib/x86_64-linux-gnu"
mutool="$tools/bin/mupdf/usr/bin/mutool"
pdftotext -layout -enc UTF-8 case.pdf -
pdftotext -bbox-layout -enc UTF-8 case.pdf bbox.html
"$mutool" show case.pdf outline
"$mutool" show case.pdf trailer/Root/Outlines
"$mutool" run "$task/fixtures/observe_mupdf.js" case.pdf
python "$task/fixtures/observe_pdf.py" case.pdf
sha256sum ast.json case.tex case.pdf
```

MuPDF는 자체 resolver에서 0기반 페이지와 위쪽을 원점으로 한 y를 준다. pypdf는 name tree 해석으로 1기반 페이지와 아래쪽 원점 `/XYZ`를 원본 단위로 기록한다. 두 경로의 비교 허용치는 0.002 PDF pt다. 페이지 텍스트/좌표는 Poppler, 96 dpi 래스터 SHA는 MuPDF draw, PDF Info와 link annotation은 pypdf에서 얻었다. 정상 공석은 valid read, catalog/outline raw 부재, 적절한 종료 0을 함께 확인한다. 깨진 입력의 실제 exit와 stderr는 별도 영수증이다. [실패 통제](receipts/controls/invalid-pdf/)

## 교차 및 바이트 대조

`run.py controls`는 2.2.3.2 + 2.3 기본 템플릿, 2.3 + 2.2.3.2 기본 템플릿, 2.3의 첫 contentsname 블록만 제거한 사본을 아예 새 폴더에서 실행한다. `Contents` 값 명시, `bookmarks=false`, TOC 앞 명시적 `\pdfbookmark`, depth=1을 각각 한 변수만 바꾸어 돌린다. epoch A·A·B는 각각 1704067200, 1704067200, 1704153600이다. 원바이트는 두 날짜 literal·trailer ID의 고정 길이 치환과 별개로 비교한다. 해당 literal이 유일한지 확인한 뒤에만 byte-level 분류를 읽는다. [교차·반례 원시 결과](receipts/controls/) · [비교 영수증](receipts/comparisons.json)

## EPUB 대조와 Git 체크

`read_epub.py`는 지정 Git commit에서 두 OPF+nav를 받아 AF-RES-243의 4 blob과 맞춘다. 공개 ZIP도 고정 SHA로 받아 container.xml의 rootfile, manifest nav·spine link와 제목을 같은 ElementTree로 추출한다. 원본 ZIP과 Git 원파일은 고정 URL에서 다시 받을 수 있다. 각 XML 차이는 CRLF→LF의 exact 비교로 따로 기록한다. [EPUB 영수증](receipts/epub/)

```bash
python -m workbench.session check "$task/session.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

Bare/dirty checkout과 fetch 실패의 처리 내역은 원영수증의 실제 종료를 사용한다. nested 작업 manifest는 저장소의 `check-all` 기본 검색 위치와 다르므로 개별 `session check`를 같이 실행한다.

결과 폴더의 `run.json`은 실행 입력·환경 해시와 3패스 요약이다. `commands.jsonl`는 실제 argv, cwd, UTC, stdout/stderr SHA와 종료를 담는다. 각 `passes.tar.gz`에는 `pass-1`부터 `pass-3`의 원 PDF, TeX 로그·보조 파일, 판독 출력과 상태가 들어 있다. 파일은 아래처럼 풀기 전에 확인할 수 있다.

```bash
archive="$task/receipts/matrix/v23-on-unique-r1/passes.tar.gz"
tar -tzf "$archive"
tar -xOzf "$archive" pass-1/commands.jsonl
tar -xOzf "$archive" pass-3/case.out
```
