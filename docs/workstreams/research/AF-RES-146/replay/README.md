# AF-RES-146 재생

Python 3.12, Git, SQLite FTS5를 사용한다. 소스 파일은 Git의 고정 객체 또는 GitHub raw의 고정 커밋에서 가져온다. 별도 Python 패키지는 필요하지 않다. 기관 절에 대해서는 공개 원전을 직접 확인한 기록의 바이트를 재생에 사용한다. `inputs.py`가 기관 PDF를 가져오거나 원문의 의미를 새로 평가하지 않는다.

새 저장소 checkout에서 아래처럼 실행한다. `NAME`마다 처음 쓰는 경로를 사용한다. 양쪽 결과 파일에서 절 읽기 시각과 CPU는 반복 측정이고 결정적 비교 대상은 아니다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-142 work/research-af-res-138 work/design-gallim
p=docs/workstreams/research/AF-RES-146
export PYTHONDONTWRITEBYTECODE=1
python "$p/replay/run.py" "$p/replay/.runs/check-one"
python "$p/replay/run.py" "$p/replay/.runs/check-two"
python "$p/replay/compare.py" "$p/replay/.runs/check-one" "$p/replay/.runs/check-two" "$p/replay/.runs/check-join"
cmp "$p/stages.csv" "$p/replay/.runs/check-one/stages.csv"
cmp "$p/transitions.csv" "$p/replay/.runs/check-one/transitions.csv"
cmp "$p/evidence/prototype.json" "$p/replay/.runs/check-one/prototype.json"
python -m unittest discover -s "$p/replay/.runs/check-one/prototype-src" -p test_roundtrip.py
python -m workbench.session check "$p/session.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
python scripts/check.py --require-git
```

다섯 개의 원본 SQLite(연구 `stages.sqlite`와 원본 조건 네 파일)는 각 실행 폴더에 생긴다. [작업 시작 SHA](../session.json), 142 원장 `6c379fe049e8e8416c4a42df8dcb9f76de36b684`, 138 교정 입력 `198e74358fe2d124c31e16f8bbb93dbbf7ee561d` 및 gallim 원본 코드 `fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c`가 필요하다. 의존 브랜치 이력이 바뀌었다면 위의 SHA도 명시적으로 fetch한 뒤 git object의 존재를 확인한다.

```sh
python "$p/replay/check_legacy_bodies.py" "$p/replay/.runs/legacy-body-recheck.json"
python "$p/replay/capture_frame.py" /tmp/af146-fresh-first-bodies.json
```

두 명령은 현재 공개 최초 본문을 확인한다. 새 프레임 JSON에는 저자 첫 글 전문이 있으므로 외부 저장 경로에 커밋하지 않는다. 결과 비교의 입력은 이미 동결한 [요청 원장](../requests.jsonl)이며 웹 본문이 수정되면 별도 시점 관측으로 남긴다.

OCR·Paperless 공급자 시험 코드는 판독만 했다. 해당 릴리스의 제품 실행환경을 준비할 경우 OCRmyPDF `v16.0.2`에서 `python -m pytest tests/test_acroform.py tests/test_metadata.py -k 'digital_signature or acroform_and_redo or bookmarks_preserved'`는 `acroform.pdf`, 서명 플래그 fixture, `toc.pdf`를 확인한다. Paperless `v2.2.1`의 테스트 환경에서는 `python manage.py test documents.tests.test_api_documents paperless_tesseract.tests.test_parser`로 기본/명시 원본 응답 및 텍스트/이미지 fixture 분기를 확인한다. 이 검사는 사용자 첨부의 서명 유효성이나 ZIP 로테이션 결과까지 입증하지 않는다.
