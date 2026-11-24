# AF-RES-122 재현

## 고정 입력으로 네 조건 재생

Python 3.12의 표준 라이브러리로 실행한다. `--data`의 catalog·aliases와 두 증거 투영만 검색에 입력한다. [판독 원장](truth.csv), [질문의 설명/가림 이유](requests.jsonl), 댓글과 공식 시험 결과는 순위 생성에서 빠진다. [SCOPE](SCOPE.md)의 가중치와 상한을 적용한 네 원장을 쓴다.

```bash
af122_path=docs/workstreams/research/AF-RES-122
python -B "$af122_path/replay.py" --out /tmp/af122-replay-check
cmp "$af122_path/ranks.csv" /tmp/af122-replay-check/ranks.csv
cmp "$af122_path/evidence/slots.csv" /tmp/af122-replay-check/slots.csv
cmp "$af122_path/evidence/comparisons.csv" /tmp/af122-replay-check/comparisons.csv
cmp "$af122_path/evidence/replay-costs.csv" /tmp/af122-replay-check/replay-costs.csv
python -B -m workbench.session check "$af122_path/manifest.json" --fetch
```

두 독립 디렉터리에 필요한 파일만 복사하는 실험은 [재생 영수증](evidence/replay-receipt.json)을 따른다. 출력에는 조사 8·표시 3 각각의 빈자리, 별칭 전환·심벌 가림을 별도로 비교한 순위 이동 및 실제 어절 비교 수가 있다. 세 채점표를 만들 때에만 이 결과를 고정 기준과 합친다.

## 원문에서 투영 재구축

`prepare.py`는 `{"request_id":"O5952","body":"..."}` 형식 JSONL을 읽는다. 각 인용 URL에서 [requests.jsonl](requests.jsonl)의 opening 1·웹 텍스트 줄 범위와 위치를 확인한다. 도구 발췌의 줄 번호 접두사를 제거한 LF 문자열을 `body`에 넣고 실제 사용한 해시부터 대조한다. 도구나 배포 후 편집에 따라 발췌·앵커 문자열·행 번호가 바뀔 수 있다. 현재 공개 원문 모두의 재구축에는 그 발췌판을 다시 읽을 수 있어야 한다. 저장소의 투영은 고정 영어 어절과 별칭 검사에 필요한 최소 어절·위치만 보존한다. 정답 및 응답 글은 입력하지 않는다. 같은 사례의 구성 query를 [controls.jsonl](evidence/controls.jsonl)의 `request_id`, `body`에서 읽을 수 있다.

```bash
python -B "$af122_path/prepare.py" --input /tmp/af122-opening-views.jsonl \
  --views /tmp/af122-projection.jsonl --audit /tmp/af122-masks.jsonl
python -B "$af122_path/prepare.py" --input "$af122_path/evidence/controls.jsonl" \
  --views /tmp/af122-controls-projection.jsonl --audit /tmp/af122-controls-masks.jsonl
cmp "$af122_path/evidence/controls-query-inputs.jsonl" /tmp/af122-controls-projection.jsonl
```

## 발행판 판독과 CPU 대조

PyTorch 2.5.1+cpu wheel과 NumPy 2.1.3을 쓴다. CPU 시험은 wheel의 Git SHA와 고정 태그를 직접 대조한다. 재작성한 작은 배열과 모델 shape만 실행한다. 포럼 코드, Core ML 변환, CUDA, DDP나 PyG 실동작은 실행하지 않았다. 설치는 임시 분리 경로를 사용했다. [시험 스크립트](probe_torch.py) · [stdout](evidence/torch-probe.stdout.json) · [stderr](evidence/torch-probe.stderr.txt) · [종료코드](evidence/torch-probe.exit)

```bash
python3.12 -m venv /tmp/af122-torch
/tmp/af122-torch/bin/pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu'
/tmp/af122-torch/bin/pip install 'numpy==2.1.3'
/tmp/af122-torch/bin/python -B "$af122_path/probe_torch.py" > /tmp/af122-torch-observations.json
```

## 정규 모집 복구 입력

정규 시간창은 보존했다. 현재 환경은 패키지 호스트만 허용하고 `discuss.pytorch.kr`의 익명 JSON GET이 CONNECT 403이다. 웹 발췌의 활동 목록에는 서로 다른 캐시 시점과 4페이지 공백이 있었다. [시도 원장](frame.csv)

해당 공개 호스트에 정상 접속할 수 있는 환경에서 아래 메타데이터 읽기부터 시작한다. 응답의 `category_list.categories`에서 qna/5와 subcategory IDs를 확인하고 `topic_list.more_topic_url`을 쫓는다. `created_at,id,category_id,pinned`만 추리고, 두 UTC 창 각각의 앞·뒤 페이지를 검증한다. 핀이 페이지마다 반복되면 ID로 합치되 생성 시각에 둔다. `created_at`의 순서를 여러 페이지에서 확인해 240건 안에서 첫 4건씩 읽는다. `created_at`을 제공하지 않는 활동 페이지와 검색 snippet은 모집에 쓰지 않는다.

```bash
curl -fsS 'https://discuss.pytorch.kr/categories.json?include_subcategories=true' -o /tmp/af122-categories.json
curl -fsS 'https://discuss.pytorch.kr/c/qna/5/l/latest.json?order=created&ascending=true' -o /tmp/af122-category-page0.json
curl -fsS 'https://discuss.pytorch.kr/t/5952/1.json?include_raw=true' -o /tmp/af122-example-opening.json
python -B - <<'PY'
import json
from pathlib import Path
for topic in json.loads(Path('/tmp/af122-category-page0.json').read_text())['topic_list']['topics']:
    print(topic['created_at'], topic['id'], topic['category_id'])
PY
```

`5952`는 요청 경로 확인 예시이며 미래 표본은 시간순으로 결정한다. `post_stream.posts`에서 `post_number == 1` 하나만 선택해 본문과 공개 편집 표시를 읽는다. 문제가 된 예외 입력은 [requests.jsonl](requests.jsonl)의 판·shape·작성자 관측을 먼저 확인한다. 공식 미응답이나 편집이 가려진 경우 unknown으로 남긴다.
