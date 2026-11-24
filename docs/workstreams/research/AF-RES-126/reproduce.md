# AF-RES-126 재현

Python 3.12 표준 라이브러리와 Git으로 순위와 분모를 재현한다. 후보 16개, 활성 별칭 12개의 출전과 코드가 저장된 입력판은 AF-RES-122 결과 SHA다. 등록 의존 SHA에서 결과판이 선조인지 먼저 확인한다. 후보 설명과 한국어 사전을 이 브랜치에 복사해 유지하지 않는다. [범위](SCOPE.md) · [계약](manifest.json)

## 고정판과 두 경로

아래 명령은 결과 SHA가 체크아웃된 저장소 루트에서 실행한다. 각 디렉터리는 처음에 비어 있고 저장소에서 읽은 코드·명시적 입력으로 채운다. 검색 재생은 AF-RES-122의 심벌 가림 결과, catalog·aliases, 정확 심벌 및 영어 점수·정렬·공석 구현을 재사용한다. 별칭 판독과 적격표는 집계에서 결합한다.

```bash
af126=docs/workstreams/research/AF-RES-126
af122=docs/workstreams/research/AF-RES-122
af122_result=e69a3f837d400ba8a4820edb5bcd91223dc5f9cc
af122_handoff=1fe299790d14a6bd93a101c005ba0802368cba50
git fetch origin refs/heads/work/research-af-res-122
git merge-base --is-ancestor "$af122_result" "$af122_handoff"

af126_a=$(mktemp -d /tmp/af126-a.XXXXXX)
af126_b=$(mktemp -d /tmp/af126-b.XXXXXX)
for af126_run in "$af126_a" "$af126_b"; do
  mkdir -p "$af126_run/prior"
  git archive "$af122_result" "$af122" | tar -x -C "$af126_run/prior" --strip-components=4
  git archive HEAD "$af126" | tar -x -C "$af126_run"
done
(cd "$af126_a" && PYTHONHASHSEED=0 python -B "$af126/replay.py" --prior prior --out out)
(cd "$af126_b" && PYTHONHASHSEED=37 python -B "$af126/replay.py" --prior prior --out out)
diff -rq "$af126_a/out" "$af126_b/out"
cmp "$af126/ranks.csv" "$af126_a/out/ranks.csv"
for af126_name in slots.csv transitions.csv replay-costs.csv domain-cases.csv; do
  cmp "$af126/evidence/$af126_name" "$af126_a/out/$af126_name"
done
```

[재생 영수증](evidence/replay-runs.json)에는 분리한 경로, 입력 지문, 명령, stdout·stderr·종료값, 5개 출력의 지문이 있다. A/B는 원문과 가림의 투영·순위 모든 선행 필드를 C/D 실행 전에 비교한다. 추가 경계 확인 12개는 연구 질문의 분모에 들어가지 않는다. [전수 점수](ranks.csv) · [조사·표시 자리](evidence/slots.csv) · [유입·탈락](evidence/transitions.csv) · [검사량](evidence/replay-costs.csv)

## 공개 첫 게시물의 입력을 직접 다시 만들기

[openings.jsonl](openings.jsonl)의 링크에서 topic ID와 작성자의 opening #1을 확인한다. 저장소의 선행판에는 포럼 본문 전체가 없고, 원문 열람 경로는 [sources.jsonl](sources.jsonl)에 있다. 이번에는 웹 도구 공개 HTML 출력에서 지정한 L줄 접두사를 걷어 내어 빈 줄·코드 들여쓰기·링크 표지를 보존하고 LF로 합쳤다. 끝에 LF를 덧붙이지 않는다. 응답이나 제목을 포함하지 않는다. 원 작성자의 범위별 원문을 UTF-8 JSONL의 `request_id, body`에 넣고, 원문/가림 SHA를 비교한다. 게시물 편집 시점과 JSON 원문은 별도 증거가 필요하다.

```bash
python -B "$af126/capture.py" --prior "$af126_a/prior" \
  --forum-bodies /tmp/af126-openings-current.jsonl --out /tmp/af126-capture
for af126_group in forum controls; do
  cmp "$af126/evidence/$af126_group-inputs.jsonl" "/tmp/af126-capture/$af126_group-inputs.jsonl"
  cmp "$af126/evidence/$af126_group-audit.jsonl" "/tmp/af126-capture/$af126_group-audit.jsonl"
done
```

전체 포럼 본문은 읽는 환경에서 임시 입력으로만 사용했다. 커밋된 투영에 영어 어절 위치, 정확 심벌 판정, D에서 검사할 수 있는 한글 어절, 어절 사이의 비어 있는 위치, 원문·가림 해시가 있다. 이 입력으로 네 정책의 출력은 재생할 수 있다. 원문 전체의 독립 재검산은 공개 화면에서 같은 발췌판을 다시 취득해야 한다. 해시가 달라지면 현행판으로 분류해 요구 조작·보존과 전수 기준을 새로 봉인한다. [공개 입력](evidence/forum-inputs.jsonl) · [원문·가림 감사](evidence/forum-audit.jsonl) · [구성문](controls.jsonl)

## 결과 집계와 저장소 계약

```bash
python -B "$af126/summarize.py" --prior "$af126_a/prior" \
  --ranks "$af126_a/out" --out /tmp/af126-summary
cmp "$af126/evidence/metrics.json" /tmp/af126-summary/metrics.json
python -B -m workbench.session check "$af126/manifest.json" --fetch
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

분모·공석·판정 연결은 [집계 스크립트](summarize.py), 작업 경로·깨끗한 Git·공통 단위/lab/export 범위는 별도 검사 영수증에서 확인한다. 동일 코드의 두 실행은 출처의 독립 판독이나 사용자 시험과 구별한다.

## CPU 반례

PyTorch 2.5.1+cpu의 Git SHA와 NumPy 버전을 출력한다. 이 관측은 인덱스/표본 반환, 세 축 순열과 단순 shape 변경, 지정 입력의 공유, 독립 사본과 미분 경로, 개별 샘플 변환에 한정된다. [프로브](probe_torch.py) · [실행 영수증](evidence/cpu-probe.json)

```bash
python3.12 -m venv /tmp/af126-torch
/tmp/af126-torch/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu'
/tmp/af126-torch/bin/python -m pip install 'numpy==2.1.3'
/tmp/af126-torch/bin/python -B "$af126/probe_torch.py"
```
