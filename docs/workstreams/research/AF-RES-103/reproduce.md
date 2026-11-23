# AF-RES-103 재현

연구 폴더에서 `run.py`를 실행한다. 고정 입력과 선언 원 행은 [inputs.json](inputs.json)과 [definitions.json](evidence/definitions.json)에 있다. T0는 공개 질문 revision의 코드, T1은 099 연구자가 기록한 동일 파생, T2는 PGFPlots 버전 태그의 전체 원문이다. T3/T4는 [계약](SCOPE.md)의 파생이다. 원 PGFPlots fixture의 저작권 표시를 사본에 보존했다. [공개 질문](https://stackoverflow.com/revisions/79393445/1) · [099 재현](https://github.com/laadkke-arch/agentflow-open/blob/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099/reproduce.md) · [PGFPlots 배포 정보](https://ctan.org/ctan-ann/id/mailman.2869.1621410113.4615.ctan-ann%40ctan.org)

## 도구 준비

실행판은 Debian 13 amd64, Python 3.12.14, TeX Live의 pdfLaTeX 및 texlive-latex-base/extra/recommended/pictures, Chromium이다. Python에는 playwright 1.62.0, PyMuPDF 1.26.6와 Pillow 13.0.0을 사용했다. `dot`은 별도 영역 대조에 사용한다. 실제 경로와 의존 라이브러리는 [환경 지문](environment.json)에 있다. 다음은 연구용 도구를 임시 경로에 준비하는 명령이다.

```bash
af103_tools="$(mktemp -d /tmp/af103-tools.XXXXXXXX)"
curl -fL -o "$af103_tools/pandoc.tar.gz" \
  https://github.com/jgm/pandoc/releases/download/3.6/pandoc-3.6-linux-amd64.tar.gz
printf '%s  %s\n' 8e3702b195f75412e425df46f8f3f08241b66a2b33abbd9e04eda501bfde860c "$af103_tools/pandoc.tar.gz" | sha256sum -c -
tar -xzf "$af103_tools/pandoc.tar.gz" -C "$af103_tools" pandoc-3.6/bin/pandoc
mkdir -p "$af103_tools"/{debs,debian,apt/lists/partial,apt/cache/archives/partial}
printf '%s\n' 'deb https://deb.debian.org/debian trixie main' > "$af103_tools/apt/sources.list"
af103_apt=(-o "Dir::Etc::sourcelist=$af103_tools/apt/sources.list" -o Dir::Etc::sourceparts=-   -o "Dir::State::lists=$af103_tools/apt/lists" -o "Dir::Cache=$af103_tools/apt/cache")
apt-get "${af103_apt[@]}" update
(
  cd "$af103_tools/debs"
  apt-get "${af103_apt[@]}" download pdf2svg=0.2.4-1 mupdf-tools=1.25.1+ds1-6+deb13u1     libmupdf25.1=1.25.1+ds1-6+deb13u1 libgumbo3=0.13.0+dfsg-2 libmujs3=1.3.6-1
  for pkg in *.deb; do dpkg-deb -x "$pkg" ../debian; done
)
kpsewhich -engine=pdftex -format=fmt pdflatex.fmt
```

다른 미러 시점에서 지정판을 내려받을 수 있는지는 확인이 필요하다. `run.py`는 세 바이너리 지문과 각 TeX 원 입력을 검증한다. 099 지문을 대조하려면 099 결과 SHA를 Git으로 읽어 `--af099-environment`에 전달한다.

## 세 경로와 별도 대조

```bash
af103_out="$(mktemp -d /tmp/af103-output.XXXXXXXX)"
python -B run.py environment --tools "$af103_tools" --output "$af103_out/environment.json"
python -B run.py reference --tools "$af103_tools" --output "$af103_out/reference"
python -B run.py calibration --tools "$af103_tools" --output "$af103_out/calibration"
python -B run.py matrix --tools "$af103_tools" --output "$af103_out/matrix"
python -B run.py controls --tools "$af103_tools" --output "$af103_out/controls"
```

- K의 Lua는 [원 파일](evidence/inputs/p4-raw-tikz.lua)이다. 실제 자식 인자·전달 TeX·종료값은 각 `children/`에 있다. `reader.json`은 동일 reader 인자로 별도 관측한 읽기 결과다.
- M은 [run.py](run.py)의 `m`이 선언을 원행 목록에서 꺼내 새 `g1.tex`, `g2.tex`를 만든다. 컴파일된 SVG를 동일 reader에서 나온 호스트 AST에 삽입한다. M의 동적 미지원 목록은 원행과 토큰을 남긴다.
- P는 `mutool draw -oout.svg aff2748b-266e-48f5-b2f7-7547936bb6aa.pdf`를 호출하며 앞의 pdfLaTeX와 뒤의 `make_preview`는 연구자 단계다. 번호순의 `outN.svg`를 이미지로 넣는다. [공개 답의 명령](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source)
- 각 슬롯은 새 폴더와 새 임시 TeX/XDG 경로를 쓴다. Chromium 탐색과 HTML만 복사한 이동은 별도 오프라인 컨텍스트다. 루프백 URL에는 해당 폴더의 파일 바이트만 공급한다. 이는 실제 인터넷 요청이 아니다. `browser.json`, `moved.json` 및 image 별 PNG가 판독 범위다.

`runs.jsonl`과 각 `receipt.json`에는 실제 인자·시각·종료값·출력 해시가 있다. 절대 실행 경로와 PDF 생성 시간이 바뀔 수 있다. 의미와 주 산출물 바이트는 별도 기준으로 검산한다.
