# Typst Q5 재현

1. 이 작업의 결과 SHA를 checkout한다. `assessment.json`의 12개 candidate ID를 단계② `evidence/typst/candidate-part.json`과 대조한다. CSS는 root의 별도 검증을 결합하며 TY-U2 빈 자리는 그대로 둔다.
2. 아래 공식 바이너리를 **작업 소유 경로 안의 cache**에 내려받는다. 계정·전역 설치를 바꾸지 않는다.

```sh
python - <<'PY'
from pathlib import Path
import hashlib, tarfile, urllib.request
base = Path('docs/workstreams/research/AF-RES-101/.cache/typst-official')
base.mkdir(parents=True, exist_ok=True)
url = 'https://github.com/typst/typst/releases/download/v0.10.0/typst-x86_64-unknown-linux-musl.tar.xz'
data = urllib.request.urlopen(url, timeout=60).read()
assert hashlib.sha256(data).hexdigest() == 'd3e1f266186f9a130762283bc8907abebc63267f08bd03a3366f79527ba95ad9'
archive = base / 'typst-v0.10.0.tar.xz'
archive.write_bytes(data)
with tarfile.open(archive) as package:
    package.extractall(base, filter='data')
PY
python -B docs/workstreams/research/AF-RES-101/evidence/typst-official/run.py
```

`run.py`에는 PyMuPDF(`fitz`)와 Pillow가 필요하다. 이 작업에서는 이미 설치되어 있었으며 새 패키지를 설치하지 않았다. 바이너리 `--version`은 `typst 0.10.0 (70ca0d25)`여야 한다. `environment.json`의 바이너리 SHA와 함께 확인한다. script는 17개의 `.typ` 입력과 synthetic-image.png, 결과 PDF/PNG, run-receipt.json을 생성한다. 생성물에는 공개 작성자의 실제 이름·이메일이 없다. 새 재생은 원 영수증과 구분해서 수행·보존해야 한다.

3. `run-receipt.json`에서 compiler exit 15개 0·2개 1을 읽되, 이것을 목적 충족률로 쓰지 않는다. `a2-initial-fail`의 unknown red, `u1-direct-p-rejected`의 type 오류가 의도한 음성 대조다. `u1-c1-literal-pagebreak`는 exit0이어도 한 페이지에 함수 이름을 출력한다.
4. PDF의 내용·도형·페이지 수와 PNG를 대조한다. A1 stroke 1→4, 동일 텍스트; A2 C1/C2 원 수식 적용의 렌더 동일성; U1 literal1page vs 호출/page/helper3pages를 재계산한다. PNG image 입력은 C2/C3의 page2에 caption과 함께 나타나야 한다. 색 metadata 추출은 일부 standalone 문서에서 부정확하여 실제 렌더를 함께 본다.
5. 원 source 바이트는 `sources.jsonl`의 고정 URL에서 받아 SHA-256/blob SHA를 확인한다. 현재 reference 페이지는 역사판 근거로 대체하지 않는다. 원 upstream expected PNG와 입력은 묶음으로 세고, 서로 다른 댓글을 새 독립 사건으로 늘리지 않는다.

## 미실시 upstream test harness

공식 [고정 tests/README.md](https://github.com/typst/typst/blob/70ca0d257bb4ba927f63260e20443f244e0bb58c/tests/README.md)의 명령을 따른다. Cargo와 빌드 의존성이 있는 별도 작업환경에서 고정 commit을 checkout하고 다음을 실행한다.

```sh
cargo test --workspace --test tests -- --exact container.typ content.typ align.typ
```

파일명 필터의 합집합이 원하는 세 경로인지 실제 출력에서 확인한다. 혼동을 피하려면 다음처럼 파일 경로 문자열로 나눠 실행한다.

```sh
cargo test --workspace --test tests -- layout/container.typ
cargo test --workspace --test tests -- math/content.typ
cargo test --workspace --test tests -- layout/align.typ
```

이 전체 harness 실행은 이번에 하지 않았다. 원 ref 파일을 갱신하는 `--update`는 재검증 명령에 넣지 않는다. 실행한 시험 수·실패·ref diff를 별도 영수증으로 보존한다. 이 확인이 끝나기 전 이번 합성 입력 실행을 upstream suite 통과로 부르지 않는다.
