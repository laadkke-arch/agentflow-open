# AF-RES-154 재생

`run.py`는 최신 이미지를 가져오지 않는다. 아래 두 OCI 지문을 내려받고 GitHub 결과판의 동일 PDF를 쓴다. 통제 루트는 시스템 인증서 저장소에 추가할 필요가 없다. Docker는 각 데이터베이스·Redis·감시 폴더를 새로 만들고 Paperless HTTP를 호스트 루프백에만 연다. 재생은 그 실행에서 만든 이름 있는 Docker 자원만 정리한다.

```sh
task=docs/workstreams/research/AF-RES-154
export PYTHONDONTWRITEBYTECODE=1
export UV_CACHE_DIR=/tmp/af154-uv-cache
uv venv --python 3.12 /tmp/af154-replay-venv
uv pip install --python /tmp/af154-replay-venv/bin/python -r "$task/replay/requirements.txt"
docker pull --platform linux/amd64 ghcr.io/paperless-ngx/paperless-ngx@sha256:096719d7f44e5f8538ca4cf8c717d3a10d8fec699c85f494cdf94ded91bed666
docker pull --platform linux/amd64 redis@sha256:090276da2603db19b154602c374f505d94c10ea57e9749fc3e68e955284bf0fd
work=$(mktemp -d /tmp/af154-replay.XXXXXX)
/tmp/af154-replay-venv/bin/python "$task/replay/fixtures.py" --fixtures "$task/replay/fixtures" --ledger "$work/fixtures.jsonl"
/tmp/af154-replay-venv/bin/python "$task/replay/run.py" --out "$work/runs"
```

호스트에는 Python 3.12, Docker와 `pdfsig`, `pdftotext`, `pdftoppm`, OpenSSL이 필요하다. 마지막 두 도구는 각각 시각 대조와 재발급에 쓴다. 제품판과 OCR 의존은 이미지 digest로 고정하고, 로컬 검증·생성 Python 패키지는 requirements.txt에서 고정한다. 실제 실행한 호스트 도구 판은 증거에 있다. wrapper의 `probe`는 버전/언어 조회, `orientation`은 osd, `recognition`은 hOCR·PDF·텍스트 인식이다.

공급자 사본으로 시험을 재생하려면 위에 커밋된 고정 PDF와 validation-time.txt를 함께 사용한다. 새 시험 인증서를 쓰려면 `fixtures.py --generate --fixtures "$work/fresh-fixtures" --ledger "$work/fresh.jsonl"`을 실행한다. 새 키·시각이 들어간 서명 입력에는 새로운 SHA-256이 부여된다. 검사값의 문자열 경로, 작업 ID·시각, HTTP 헤더 파일명, PDF/A 생성 바이트는 검산에서 구분할 값이다.

재생 중 원본과 기본 응답, 작업 결과, SQLite 읽기 증거, 서비스 로그가 `$work/runs`에 생긴다. 정상 업로드 UI 대신 공식 소비 감시 경로를 쓰며, API 인증과 파일 서버는 제품 그대로다. 환경 오류가 있으면 `harness-errors.json`과 각 인스턴스의 stdout/stderr를 먼저 읽는다. fixture에는 개인 자료와 개인 키가 들어 있지 않다.
