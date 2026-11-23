# 새 경로에서 AF-RES-095 재현

## 입력과 환경

[HANDOFF](HANDOFF.md)의 결과 SHA를 clean checkout하고 루트에서 실행한다. 본 실험은 Debian 13.6 x86_64, Python 3.12.14에서 실행했다. 준비된 XeTeX, LaTeX2e 2024-11-01 PL2, booktabs 1.61803398, strace 6.13, `/usr/bin/pdftoppm` 25.03.0, PyMuPDF 1.26.6 / MuPDF 1.26.11, Pillow 13.0.0의 지문을 사용한다. [정확 패키지·바이너리·포맷 해시](environment.json)

```bash
AF095_SRC="$PWD/docs/workstreams/research/AF-RES-095"
AF095_LAB="$(mktemp -d /tmp/af-res-095-reproduce-XXXXXXXX)"
AF095_DIST="$AF095_LAB/quarto-1.4.553-linux-amd64.tar.gz"
AF095_RELEASE=https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.553
curl -fLsS "$AF095_RELEASE/quarto-1.4.553-linux-amd64.tar.gz" -o "$AF095_DIST"
curl -fLsS "$AF095_RELEASE/quarto-1.4.553-checksums.txt" -o "$AF095_LAB/checksums.txt"
(cd "$AF095_LAB" && awk '/quarto-1.4.553-linux-amd64.tar.gz$/' checksums.txt | sha256sum -c -)
tar -xzf "$AF095_DIST" -C "$AF095_LAB"
AF095_QUARTO="$AF095_LAB/quarto-1.4.553/bin/quarto"
"$AF095_QUARTO" --version
xelatex --version
/usr/bin/pdftoppm -v
kpsewhich --engine=xetex --format=fmt xelatex.fmt
sha256sum "$(kpsewhich booktabs.sty)"
python -c 'import pymupdf, PIL; print(pymupdf.version, PIL.__version__)'
python -B "$AF095_SRC/fixtures/prepare.py" --check
```

기대 아카이브 SHA-256은 `22b7541b1e1be9746657a447383796ba420e6f0cbc5e7b31c8229ddebc258c90`이다. bundle은 Pandoc 3.1.11을 포함한다. 렌더 중 TeX 패키지 자동 설치를 껐다. 렌더·쿼리에서 쓸 XDG·TEXMF 쓰기 경로와 per-run TMPDIR는 스크립트가 준비한다.

## 양성·음성 교정 및 12자리 실행

```bash
python -B "$AF095_SRC/experiment.py" calibrate --quarto "$AF095_QUARTO" \
  --work "$AF095_LAB/cal-work" --evidence "$AF095_LAB/cal"
python -B "$AF095_SRC/fingerprint.py" --quarto "$AF095_QUARTO" \
  --archive "$AF095_DIST" --checksums "$AF095_LAB/checksums.txt" \
  --calibration "$AF095_LAB/cal" --work "$AF095_LAB/fingerprint" \
  --output "$AF095_LAB/environment.json"
python -B "$AF095_SRC/experiment.py" matrix --quarto "$AF095_QUARTO" \
  --work "$AF095_LAB/matrix-work" --evidence "$AF095_LAB/matrix"
python -B "$AF095_SRC/audit.py" --reread-pdfs
```

교정 원본은 대상 1/0/1, 대조 1/1/1. ruler는 다크 밴드 1개와 x≈72–144pt, y≈143.598pt, 폭 0.8pt다. 행렬은 원본 대상 1/0/1, 수정 대상 0/0/0, 두 표 원본의 대조 1/1/1, 두 표 수정의 대조 0/1/0을 기대한다. 순서는 위·내부·아래다. 모든 표의 셀 기대값은 [plan](fixtures/plan.json)에 있다. PDF 날짜·ID·임시 템플릿 파일명은 재생성 때 달라질 수 있다. 원 PDF [벡터·셀·래스터](evidence/matrix/) 및 [반복 등가 기준](metrics.json)과 비교한다. `audit.py`는 커밋된 원장을 대조한다. 방금 렌더한 쪽의 원장과 증거는 새 디렉터리에 있다.

주 렌더의 실제 명령은 각 새 디렉터리에서 입력을 document.qmd로 복사한 후 다음과 같다. wrapper가 execve·파일 열기와 TeX 기록을 수집한다.

```bash
"$AF095_QUARTO" render document.qmd --to pdf -M keep-tex:true \
  -M latex-clean:false -M latex-auto-install:false --pdf-engine-opt=-recorder --log-level debug
```

## 본문·헤더·TeX 반례와 다른 출력 분야

```bash
python -B "$AF095_SRC/probes.py" --quarto "$AF095_QUARTO" \
  --work "$AF095_LAB/probe-work" --evidence "$AF095_LAB/probes"
AF095_WPT=https://raw.githubusercontent.com/web-platform-tests/wpt/0ba12e737fd832416b9a29dae9f200b311147517/css/css-tables
mkdir "$AF095_LAB/wpt"
curl -fLsS "$AF095_WPT/border-conflict-resolution.html" -o "$AF095_LAB/wpt/wpt-html"
curl -fLsS "$AF095_WPT/border-conflict-resolution-ref.html" -o "$AF095_LAB/wpt/wpt-reference"
python -B "$AF095_SRC/cross_domain.py" --sources "$AF095_LAB/wpt" \
  --work "$AF095_LAB/cross-work" --output "$AF095_LAB/cross"
```

보조 범위의 CSS는 Chromium 156.0.8078.79, Playwright 1.62.0이고 Calc는 `soffice --version`이 LibreOfficeDev 26.8.0.0.alpha0 `2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`를 반환했다. [TeX 반례와 출력](evidence/probes/README.md) · [CSS·Calc 기대값과 출력](evidence/cross/README.md)

엔진 1차 경고만 재생할 때는 새 작업 경로에 `evidence/matrix/{S,D}-{O,Z,T}-1/document.tex`를 조건별로 복사한다. `xelatex -interaction=batchmode -halt-on-error -recorder document.tex`를 두 번 실행하고 패스마다 `document.log`를 별도 파일로 복사한다. 1차에서 rerun 경고가 있고 2차에 없어지는지 본다. [실제 발췌와 입력 SHA](evidence/probes/engine-replay.jsonl)

## 저장소 검사

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-095/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python -B scripts/check.py --require-git
```

개별 검사는 저장소 상대 경로로 manifest를 받는다. 지정 의존의 원격 헤드가 이동한 동안에는 정확 SHA 핀과 원격 검사 결과가 갈린다. [조건과 인수](evidence/intake/contract.md)
