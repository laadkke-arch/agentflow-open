# AF-RES-101 재현 절차

이 문서는 **커밋된 판정의 재계산**, **현재 공개 원자료의 재취득**, **연구자 합성 실행**, **추가로 필요한 원 환경 실행**을 구별한다. 현재 API가 반환하는 상태는 2024년의 댓글 수정 전 상태나 삭제 자료를 복원하지 않는다. 분석 규칙은 [SCOPE.md](SCOPE.md), 결과와 결손은 [RESULT.md](RESULT.md), 마지막으로 검사한 판은 `HANDOFF.md`의 `checked_result_sha`가 기준이다.

## 1. 검사 대상과 재생 공간 고정

원 작업 checkout에서 모집·코딩·실행 스크립트를 다시 돌리면 영수증과 일부 표를 덮어쓴다. 아래처럼 이 작업의 무시된 `.cache/` 안에 **깨끗한 검사 checkout**과 **자료 재생 checkout**을 별도로 만든다. 기존 원문·최초판·후보 봉인과 원 검사 영수증을 바꾸지 않는다. 연구용 원 다운로드는 커밋에 포함하지 않는다.

먼저 최신 인계의 `checked_result_sha` 40자리를 읽어 `AF101_TARGET`에 넣는다. `HANDOFF.md`가 나중 단독 커밋이면 그 커밋 자체와 검사된 결과 커밋은 다르다. 변수의 설명 문자열을 실제 SHA로 바꾸기 전에는 아래 명령을 실행하지 않는다.

```sh
AF101_REPO="$(git rev-parse --show-toplevel)"
AF101_TASK=docs/workstreams/research/AF-RES-101
AF101_TARGET='<HANDOFF.md의 checked_result_sha 40자리>'
AF101_RUN="$AF101_REPO/$AF101_TASK/.cache/replay-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$AF101_RUN"
git -C "$AF101_REPO" cat-file -e "$AF101_TARGET^{commit}"
git clone --no-hardlinks --no-checkout "$AF101_REPO" "$AF101_RUN/clean"
git -C "$AF101_RUN/clean" remote set-url origin https://github.com/laadkke-arch/agentflow-open.git
git -C "$AF101_RUN/clean" checkout --detach "$AF101_TARGET"
git -C "$AF101_RUN/clean" rev-parse HEAD
git -C "$AF101_RUN/clean" status --porcelain
```

HEAD 출력이 인계의 SHA와 같고 `status --porcelain`이 비어 있는지 확인한다. 오래된 얕은 clone에 대상 커밋이 없으면 먼저 공개 `origin`에서 작업 브랜치와 대상 커밋을 받아야 한다. 기존 작업 파일을 `reset --hard`로 지우는 방식으로 재현 공간을 만들지 않는다.

이 작업의 선행 봉인은 ① `9d646592613ba2fd9c52bc9bbf3dbc28bac68693`, ② `4e7539906eb03abd46e6910643ed5317f97ddb45`이다. 이후 묶음과 실제 원격 검증 시각·변경 경로는 [commits.jsonl](evidence/seals/commits.jsonl)에 있다. 시작 통합판·의존 SHA·사용 blob의 대조는 [contract-read.json](evidence/start/contract-read.json)과 [manifest.json](manifest.json)을 읽는다. 역사적 재현을 위해 `session start`로 기존 manifest를 새 원격 끝에 맞춰 다시 쓰지 않는다.

## 2. 깨끗한 결과 SHA에서 계약·공통 검사

`clean` checkout의 저장소 루트에서 사용자가 요구한 명령을 그대로 실행한다. 실제 도움말과 인자 정의는 `workbench/session.py`, `scripts/cloud_check.py`에서 확인했다. 재취득·재생으로 파일이 바뀐 checkout에서 `--require-clean`을 생략하는 방식으로 통과시키지 않는다.

```sh
cd "$AF101_RUN/clean"
git rev-parse HEAD
python -B -m workbench.session check docs/workstreams/research/AF-RES-101/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
git rev-parse HEAD
git status --porcelain
```

각 명령의 UTC·종료값·stdout·stderr를 `AF101_RUN` 아래 별도 영수증에 남긴다. 공통 검사 자체의 상세 영수증은 `clean/.workbench/cloud-check.json`, 단계 로그는 `clean/.workbench/cloud-check-logs/`다. 다음 필드를 읽어야 한다.

- 개별 검사: `checked_out_commit`, `integration_commit`, `freshness`, `outside_paths`, `unmerged_paths`, `errors`.
- 공통 검사: `source_start.commit`, `source_end.commit`, 양쪽 `clean`, 각 단계의 `status/exit_code`, `session_validation.count`와 상태.
- `session_validation.count=0`이면 공통 검사가 실제 과제 세션을 검증하지 않은 것이다. 별도 manifest의 개별 검사 결과를 대신했다고 쓰지 않는다. `no_active_sessions`·`already_integrated`와 실패를 구별한다.
- `--fetch`가 확인한 현재 통합 계약이나 의존 브랜치가 옛 pin과 달라 실패하면 그 차이를 기록한다. 역사적 결과를 통과시키려고 manifest·검사기·의존 SHA를 교체하지 않는다. `--integration-ref`는 과거 로컬 비교에 쓸 수 있지만 최신 원격 확인을 대체하지 않는다.

실행 수단이 없으면 해당 SHA에서 저장소의 승인된 검사 실행 경로를 사용하고 생성된 영수증을 읽는다. 실행 요청만 보냈거나 명령을 문서에 쓴 것은 검사 통과가 아니다. `codex-cloud`라는 문자열은 실행자가 붙인 환경 이름이며 계정·브라우저 연결 증거가 아니다.

## 3. 공개 자료 재생 checkout

검사 공간을 보존하고 별도의 재생 공간을 만든다. 이후 모든 상대 경로 명령은 `replay` 저장소 루트에서 실행한다. 아래 Python 스크립트들은 경로를 자기 파일 위치에서 계산하므로 원본 스크립트의 절대 경로로 실행하면 원본에 쓸 수 있다. 반드시 재생 checkout의 복사본을 실행한다.

```sh
git clone --no-hardlinks --no-checkout "$AF101_RUN/clean" "$AF101_RUN/replay"
git -C "$AF101_RUN/replay" remote set-url origin https://github.com/laadkke-arch/agentflow-open.git
git -C "$AF101_RUN/replay" checkout --detach "$AF101_TARGET"
cd "$AF101_RUN/replay"
git rev-parse HEAD
mkdir -p docs/workstreams/research/AF-RES-101/.cache/imagemagick
mkdir -p docs/workstreams/research/AF-RES-101/.cache/typst
```

원자료 응답은 복사본의 `docs/workstreams/research/AF-RES-101/.cache/`에, 재생된 영수증은 복사본의 `evidence/`에 생긴다. 원 결과와의 차이는 `clean` checkout 또는 `git show "$AF101_TARGET:<path>"`에서 읽은 고정 blob에 대조한다. `seal_initial.py`, `code_initial.py`, `seal_proposals.py`, `code_proposals.py`, `assemble_initial.py`, `assemble_candidates.py`에는 연구자가 이미 코딩한 판단과 출력 갱신이 포함되어 있다. 이를 실행하는 것은 **같은 코딩의 재물질화**이며 새로운 독립 맹검 선정이 아니다. 새 분석자는 projection만 읽고 자기 판정을 별도 파일에 남긴 뒤 봉인판과 대조한다.

### 3.1 모집창과 최초 공개 revision

질문목록 API는 다음 값으로 호출한다. H1에서 각 층 두 자리를 채우면 H2로 연장하지 않는다. 이번 실제 모집은 ImageMagick60건·Typst27건, 합계87건이다. 이 수와 선정8건은 [frame.csv](frame.csv)에서 확인한다. 현재 태그로 뽑힌 질문을 최초 tags/title/body와 비교한 차이를 보존한다.

| 구분 | fromdate | todate | 공통 인자 |
| --- | --- | --- | --- |
| H1 | 1704067200 | 1719791999 | `site=stackoverflow&tagged=imagemagick` 또는 `typst`, `sort=creation&order=asc&pagesize=60` |
| H2, 층 결원일 때만 | 1719792000 | 1735689599 | 같은 규칙·첫60건 |

ImageMagick의 `acquire_initial.py`는 질문목록을 새로 가져오지 않고 `questions-h1-masked.json`을 입력으로 읽는다. H1 모집부터 재취득하려면 아래 코드를 **재생 checkout에서만** 실행한다. 질문의 답 개수·채택·score·현재 body를 화면이나 분석용 projection으로 출력하지 않는다.

```sh
python -B - <<'PY'
from pathlib import Path
import datetime, hashlib, json, time, urllib.error, urllib.request
base = Path('docs/workstreams/research/AF-RES-101')
cache = base / '.cache/imagemagick'
cache.mkdir(parents=True, exist_ok=True)
url = ('https://api.stackexchange.com/2.3/questions?site=stackoverflow'
       '&tagged=imagemagick&fromdate=1704067200&todate=1719791999'
       '&sort=creation&order=asc&pagesize=60&filter=default')
at = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    with urllib.request.urlopen(url, timeout=45) as response:
        raw = response.read()
except Exception as error:
    (cache / 'questions-h1-failure.json').write_text(json.dumps(
        {'url': url, 'utc': at, 'error': repr(error)}, indent=2))
    raise
(cache / 'questions-h1.json').write_bytes(raw)
data = json.loads(raw)
if data.get('error_id'):
    raise RuntimeError('API error; inspect the saved response separately')
keys = ('question_id', 'creation_date', 'tags', 'title', 'link')
items = sorted(data['items'], key=lambda x: (x['creation_date'], x['question_id']))[:60]
masked = [{key: row.get(key) for key in keys} for row in items]
result = dict(source_url=url, fetched_at=at,
              raw_sha256=hashlib.sha256(raw).hexdigest(),
              has_more=data.get('has_more'), items=masked)
(base / 'evidence/imagemagick/questions-h1-masked.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2))
delay = data.get('backoff', 0)
if delay > 60:
    raise SystemExit('backoff exceeds60s: stop and resume only after the full delay')
if delay:
    time.sleep(delay)
print(json.dumps({'masked_questions': len(masked), 'has_more': data.get('has_more')}))
PY
python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/acquire_initial.py
python -B docs/workstreams/research/AF-RES-101/evidence/typst/recruit.py h1
```

최초판용 허용 projection은 IM의 `.cache/imagemagick/initial-h1.json`·`initial-h1-readable.md`, Typst의 `.cache/typst/initial-only-h1.json`이다. revision 원응답은 `/posts/{ids}/revisions?site=stackoverflow&filter=withbody&pagesize=100&page=N`을 `has_more=false`까지 읽고 `revision_number=1`만 노출한다. 최신부터 오는 첫 페이지를 최초판이라고 가정하지 않는다. 같은 시각이면 숫자 질문 ID 순으로 정렬한다.

질문목록·API pagination·quota/backoff·실패는 영수증을 읽는다. 기존 초기 스크립트는 backoff를60초로 제한한 부분이 있으므로, 원응답이60초보다 큰 값을 지시하면 다음 API 호출을 하지 않고 전 지연을 충족한 후 별도 재개한다. 인증 계정 전환이나 무한 재시도로 quota를 우회하지 않는다.

현재 태그 변경 등으로 새 모집 ID가 달라지면 새 frame과 원 frame의 차이를 남기고 원8자리·봉인 코드의 ID를 자동 교체하지 않는다. 기존8사건 검증은 `initial.csv`의 고정 question ID·revision GUID로 개별 revision을 다시 확인한다. H2를 새로 조사할 때 Typst 수집기는 `recruit.py h2`를 지원하지만 기존 acquisition 파일을 갱신하므로 H1 재생 영수증을 별도 보존한다. IM 수집기는 H1 파일명을 고정 사용하므로 H2는 같은 endpoint의 날짜만 바꿔 별도 cache/receipt로 수집해야 한다. 이번 H2 실행은 미실시이며 필요하지 않았다.

### 3.2 첫 봉인 뒤 30일 제안·A/B

8개 최초 이력과 후보 채택 규칙을 먼저 고정한다. 그 전에는 답·댓글·질문자 수정·수락표시를 읽지 않는다. 그 뒤 다음 무인자 스크립트를 실행한다.

```sh
python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/acquire_proposals.py
python -B docs/workstreams/research/AF-RES-101/evidence/typst/collect_proposals.py
```

각 질문의 `t0 <= creation <= t0+30*86400`인 질문자 외 작성자만 사용한다. `/questions/{ids}/answers`에서 answer IDs를 얻고 질문+답 ID의 `/posts/{ids}/comments`, 답의 `/posts/{answer_ids}/revisions`를 페이지 끝까지 읽는다. 공개 답 revision에서 창 안에 존재한 조작을 확인한다. 댓글은 현재 본문만 보이므로 과거 동일성을 확정하지 않는다.

분석용 파일은 IM `.cache/imagemagick/stage2/non-op-30day-projection.json`, Typst `.cache/typst/proposals-third-party-only.json`이다. 원 API payload의 질문자 댓글·자기 답·수락·score·창 밖 내용은 분석자에게 노출하지 않는다. 타인 본문이 질문자의 후속을 인용하면 그 간접 노출을 기록한다. 실제 연구의 예외는 두 태그의 `proposals-exposure.json`과 [root-proposals-exposure.json](evidence/seals/root-proposals-exposure.json)에 있다.

조작의 첫 공개 시각→숫자 post/comment ID→본문 위치 순으로 최대3개를 뽑는다. 같은 조작 반복만 합치고 서로 다른 인수·단계를 구별한다. A/B는 동일 세 후보에서 각각 앞의 두 생존 후보를 반환하며 외부 검색으로 빈자리를 채우지 않는다. 실제 판정과 빈자리는 [candidates.csv](candidates.csv), 최초 조작 원위치는 태그별 `candidate-part.json`에 있다. 후보·제외·반환을 두 번째로 봉인하기 전 공식 동작 평가나90일 작성자 후속을 읽지 않는다.

### 3.3 두 번째 봉인 뒤 90일 후속

```sh
python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/stage3/fetch_followup.py
python -B docs/workstreams/research/AF-RES-101/evidence/typst/stage3/collect_followup.py
```

창은 각 질문의 `t0`부터 `t0+90*86400`까지 양 끝 포함이다. 최초 모집 때 기계가 받은 질문 revision cache를 재사용하므로 3.1 단계가 먼저 필요하다. 자기 답이 있으면 해당 답의 revision도 읽는다. IM의 `.cache/imagemagick/stage3/followup/author-90day-projection.json`, Typst의 `.cache/typst/followup-author-only.json`을 시간순으로 읽고 고정 [followup.csv](followup.csv)와 대조한다.

`already_knew_before_proposal`, 명시 신규인지, 실행 보고, 입력·판·출력 연결 실행, 거절, 이전 방식 유지, 공개 응답 없음, 미확인을 독립적으로 판단한다. 감사·현재 채택·좋다는 평가는 신규인지나 실행의 대용이 아니다. 현재판의 시도 이력으로 최초판을 갱신하지 않는다. 동일 실행의 revision과 댓글은 관측2개여도 실행1에피소드일 수 있다.

## 4. 공식 고정 자료와 연구자 합성 실행

다음 스크립트의 인자와 출력 경로를 실제 코드에서 확인했다. 표의 명령은 모두 재생 checkout에서 실행한다. 필요한 실행 파일·패키지가 없으면 그 검사를 미실시로 기록하고 다른 판을 같은 판이라고 사용하지 않는다.

| 범위 | 실행 명령·입력 의존성 | 영수증·의미 |
| --- | --- | --- |
| IM 고정 문서/구현/상류 시험 재취득 | `python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/stage3/fetch_official.py` | 고정 commit `eeb41d70c9baf418a3aa75c424fb305362a1b280`; cache의 `imagemagick/stage3/official/`와 `official-acquisition.json` |
| IM 합성 연산·상류 colorspace shell 시험 | 위 재취득 뒤 `python -B docs/workstreams/research/AF-RES-101/evidence/imagemagick/stage3/run_core_probes.py` | PATH의 `magick`, `sh` 필요. `probes/results.json`은 바이너리판·모든 명령·해시를 기록. 원7.0.10-61 실행과 구별 |
| wrapper 공식 source 재취득 | `python -B docs/workstreams/research/AF-RES-101/evidence/root-supplement/acquire.py` | 이미 기록한 URL과 SHA를 읽어 `.cache/root-supplement/acquisition-replay.json`에 결과 저장. mutable RubyGems metadata와 고정 파일 불일치 구별 |
| IM mask·A2 literal 제어 | 3.2 IM projection 생성 후 `python -B docs/workstreams/research/AF-RES-101/evidence/root-supplement/probe.py` | `magick`, `bash`, `python` 필요. `probe-receipt.json`; A2-C1은 argv만 포착하며 실제 convert 실행 아님 |
| Typst17개 입력 | 아래 고정 바이너리 준비 후 `python -B docs/workstreams/research/AF-RES-101/evidence/typst-official/run.py` | Python의 `fitz`(PyMuPDF), `PIL`(Pillow) 필요. `inputs/`, `outputs/`, `run-receipt.json`을 재생 공간에 생성 |
| Git·FFmpeg 교정 | `python -B docs/workstreams/research/AF-RES-101/evidence/cross-domain/reproduce.py` | `git`, `ffmpeg`, `ffprobe` 필요. 합성 저장소/1초 미디어, `receipt.json`·`commands.jsonl`. 상류 suite 실행 아님 |

Typst 준비는 아래처럼 고정 릴리스 archive와 바이너리의 해시를 검증한다. 전역 설치는 필요하지 않다. Python3.12+의 안전한 tar 추출 필터를 사용한다.

```sh
python -B - <<'PY'
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
binary = base / 'typst-x86_64-unknown-linux-musl/typst'
assert hashlib.sha256(binary.read_bytes()).hexdigest() == '717ee1ec236d32076e39137d4f38b65e9073a4d02aca3247528ff868965f92bc'
PY
python -B docs/workstreams/research/AF-RES-101/evidence/typst-official/run.py
```

Typst 고정 source/expected PNG는 [source-receipts.json](evidence/typst-official/source-receipts.json)의 `url`·`name`·`sha256`으로 받는다. 고정 `raw.githubusercontent.com/typst/typst/70ca0d257bb4ba927f63260e20443f244e0bb58c/` URL만 역사판 재생에 사용하고 `.cache/typst-official/sources-replay/<name>`에 저장한다. 현재 typst.app reference는 별도 비교 자료다. Git·FFmpeg의4개 고정 파일은 [cross-domain-sources.jsonl](evidence/cross-domain-sources.jsonl)의 `fixed_url`·Git blob SHA로 대조한다. `github.com/<owner>/<repo>/blob/<sha>/<path>`를 원 바이트로 받을 때는 `raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>`를 사용하며 URL 앵커를 파일 경로에 붙이지 않는다.

비교 기준은 종료값뿐 아니라 실제 출력이다. Typst는 PDF의 내용·도형·페이지와 PNG 렌더를 대조한다. IM의 합성 gradient/checker와 root의5픽셀 PPM은 질문자 입력이 아니다. FFmpeg Matroska 파일은 생성 metadata 때문에 전체 파일 SHA가 달라질 수 있으므로 stream 목록·codec·packet data hash의 관계를 비교한다. 원 상류 시험 입력/expected output을 읽은 것, 상류 시험을 실행한 것, 연구자 fixture를 실행한 것은 각각 별도로 센다.

## 5. 고정 표와 분모 재계산

네트워크가 없어도 결과 checkout의 봉인된 CSV·평가 JSON·source 원장으로 집계를 재계산할 수 있다. root의 무인자 재계산기는 다음 경로에서 `evidence/reconciliation.json`을 출력한다. 이 명령 역시 원 결과가 아닌 재생 checkout에서 실행한다.

```sh
python -B docs/workstreams/research/AF-RES-101/recalculate.py
git diff -- docs/workstreams/research/AF-RES-101/evidence/reconciliation.json
```

대조할 단위는 요청8자리, 후보24자리와 실재/빈자리, 동일 세 후보에서 A/B 앞2자리 반환, 각 지표의 후보별 분모 자격이다. 재추천 제거·다른 유효 조작 손실·이미 아는 방법의 실제 반환은 독립 분모다. 전체 후보와 이미 인용된 core CLI만의 민감도, 필터 생존과 실제 반환, 알려진 반박과 근거 결측을 섞지 않는다. 분모0이면 비율은 산출 불가다. 재계산은 코딩된 근거를 집계하는 것이므로 유효성·인지 판단 자체를 자동 재검증하지 않는다.

모집·후보 봉인 재료를 다시 읽을 때 후속 판정을 알고 있던 분석자가 최초 맹검을 재현했다고 쓰지 않는다. 새로운 독립 검토자가 있었다면 사람/다른 작업자/자기 검토의 주체와 실제 읽은 범위를 기록한다.

## 6. 바이트 지문과 CRLF/LF 교정

[transport-normalization.json](evidence/seals/transport-normalization.json)은 다섯 CSV의 로컬 CRLF와 GitHub의 LF 바이트 차이를 기록한다. 역사적 봉인 해시를 지우지 않았고 의미상 행·정렬 변화는0으로 확인했다. GitHub/`git show`의 원 바이트에는 `committed_sha256`, 옛 로컬 업로드 전 바이트에는 `preupload_sha256`을 사용한다. 단순히 현재 파일의 해시가 이전 봉인 해시와 다르다는 이유로 내용 교체라고 판정하거나, 모든 차이를 줄바꿈 탓으로 무시하지 않는다.

```sh
python -B - <<'PY'
from pathlib import Path
import hashlib, json, subprocess
task = Path('docs/workstreams/research/AF-RES-101')
rows = json.loads((task / 'evidence/seals/transport-normalization.json').read_text())['rows']
for row in rows:
    path = task / row['path']
    raw = subprocess.check_output(['git', 'show', row['commit'] + ':' + path.as_posix()])
    current = path.read_bytes()
    recorded_match = hashlib.sha256(raw).hexdigest() == row['committed_sha256']
    normalized_match = current.replace(b'\r\n', b'\n') == raw
    print(json.dumps({'path': path.as_posix(), 'recorded_commit_bytes_match': recorded_match,
                      'current_after_CRLF_to_LF_match': normalized_match}))
    assert recorded_match and normalized_match
PY
```

이 정규화 예외는 기록된 CSV에만 적용한다. 원 API response는 받은 raw bytes, 본문 SHA는 API가 돌려준 HTML 문자열의 UTF-8 bytes, 공식 소스는 받은 파일 bytes가 기준이다. 코드 인용 위치의 C 파일 행 번호는 LF로 센다. Python `splitlines()`는 폼피드도 행 경계로 처리할 수 있으므로 이 자료의 LF 행 번호를 만들 때는 `split('\n')`를 사용한다. 재취득 시 quota 같은 응답 필드는 달라질 수 있어 response SHA 불일치와 고정 revision body SHA 불일치를 따로 확인한다.

## 7. 실패·미실시의 정확한 다음 실행

### 7.1 원 ImageMagick7.0.10-61/Cygwin

현재 실행한 IM은7.1.1-43 Q16이다. 원판 바이너리·Cygwin 환경·원 image/coords/폰트를 확보하지 못했다. 고정 source를 Linux에서 빌드해도 Cygwin 원 환경 실행과는 다르다. 소스 수준 동작을 확인할 다음 명령은 아래와 같다. compiler·라이브러리·빌드 도구가 갖춰진 별도 재생 환경을 전제로 하며 이번에 실행한 명령은 아니다.

```sh
git clone https://github.com/ImageMagick/ImageMagick.git "$AF101_RUN/ImageMagick-7010"
git -C "$AF101_RUN/ImageMagick-7010" checkout --detach eeb41d70c9baf418a3aa75c424fb305362a1b280
cd "$AF101_RUN/ImageMagick-7010"
./configure --prefix="$AF101_RUN/im7010-prefix"
make -j2
make check TESTS=tests/validate-convert.tap
make check
```

고정 `Makefile.am`의 `TESTS`·`check_PROGRAMS`와 `tests/Makefile.am`의 `tests/validate`, `tests/validate-convert.tap` 항목을 직접 확인했다. 첫 `make check`는 convert 그룹, 둘째는 구성된 전체 suite다. source가 제공하는 예상 종료값과 실제 실행 수를 읽고 준비 실패/컴파일 실패/테스트 실패/미실시를 구별한다. 현재 연구에서 전체 C suite를 돌렸다고 쓰지 않는다. [명령 확인용 두 source 행](evidence/reproduction-sources.jsonl)

원 A2 재현에 필요한 입력은 원 이미지 bytes·SHA, `num`, `coords[0]` 제목·`coords[1]`/`coords[2]` crop geometry, Calibri-Bold의 실제 사용 판, Cygwin/Bash판, ImageMagick7.0.10-61 빌드/quantum 정보다.3.2와 root `probe.py` 실행 후 원 answer revision1 블록은 복사본의 `.cache/root-supplement/probes/answer-77797032-rev1.sh`와 `answer-77797051-rev1.sh`에 있다. 실제 입력을 확보한 Cygwin Bash에서 먼저 아래 구문 검사를 수행한다.

```sh
bash --version
convert -version
bash -n docs/workstreams/research/AF-RES-101/.cache/root-supplement/probes/answer-77797032-rev1.sh
bash -n docs/workstreams/research/AF-RES-101/.cache/root-supplement/probes/answer-77797051-rev1.sh
```

그다음 원 입력값을 셸 변수로 설정한 별도 스크립트에 원literal을 그대로 연결해 실행한다. 원literal에는 `val=300`이 있으므로 이를301로 바꿔 다른 분기를 시험하는 것은 별도 연구자 대조다. 잔여`fi`, `dims`의`d`, 고정30×40 patch, 문자열 안 escape를 먼저 고쳐서 원 제안이 통과했다고 쓰지 않는다. 실제 호출·입력 해시·stdout/stderr·출력 이미지·예상 두 patch geometry를 함께 기록한다.

### 7.2 Ruby/QuickMagick/RMagick/Open3

Ruby/gem 실행기가 없어서 wrapper 후보의 런타임 실행은 미실시다. 고정 QuickMagick0.8.0과 RMagick5.3.0 소스 검토는 실행을 대신하지 않는다. Ruby·해당 gem·native ImageMagick 의존성이 있는 격리 환경에서 아래처럼 원 코드 블록을 추출한다. 이 코드는 원snippet을 수정하지 않고 입력 경로/출력 파일 변수와 gem 판 선택만 연구 harness로 앞에 둔다.

```sh
python -B - <<'PY'
from pathlib import Path
import html, json, re
base = Path('docs/workstreams/research/AF-RES-101')
events = json.loads((base / '.cache/imagemagick/stage2/non-op-30day-projection.json').read_text())
event = next(e for e in events if e.get('post_id') == 77774667 and e.get('revision_number') == 2)
blocks = [html.unescape(s) for s in re.findall(r'<pre\b[^>]*><code\b[^>]*>(.*?)</code></pre>', event['body'], re.S)]
assert len(blocks) == 3
out = base / '.cache/ruby-replay'
out.mkdir(parents=True, exist_ok=True)
gems = ["gem 'quick_magick', '0.8.0'\n", "gem 'rmagick', '5.3.0'\n", '']
for i, body in enumerate(blocks, 1):
    (out / f'c{i}-literal.rb').write_text(body)
    prefix = gems[i-1] + 'remote_image = Struct.new(:path).new(ARGV.fetch(0))\noutfile = ARGV.fetch(1)\n'
    (out / f'c{i}-harness.rb').write_text(prefix + body)
print(json.dumps({'revision_guid': event['revision_guid'], 'body_sha256': event['body_sha256'], 'blocks': 3}))
PY
ruby --version
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c1-harness.rb /absolute/path/to/input.png /absolute/path/to/c1-output.png
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c2-harness.rb /absolute/path/to/input.png /absolute/path/to/c2-output.png
ruby docs/workstreams/research/AF-RES-101/.cache/ruby-replay/c3-harness.rb /absolute/path/to/input.png /absolute/path/to/c3-output.png
```

`/absolute/path/to/...`는 확보한 원 입력과 cache 안 새 출력 경로로 교체해야 한다. 원 입력이 없으면 root의 합성5픽셀 PPM을 쓸 수 있으나 원 사용자 실행이 아닌 연구자 대조로 표시한다. C3에 `ruby -rshellwords .../c3-harness.rb ...`를 적용한 별도 대조는 누락된 loading 조건을 보완한 **수정형**이다. RMagick 구판을 추가로 쓸 때는 그 판·ImageMagick 연결 정보를 기록하고5.3.0 반례와 섞지 않는다.

### 7.3 Typst·Git·FFmpeg 상류 suite

합성 실행은 수행했지만 아래 고정 상류 suite 자체는 미실시다. 빌드 의존성과 고정 source checkout을 준비한 뒤 다음 명령으로 재개한다. Typst 테스트는 ref를 갱신하는 `--update` 없이 실행한다.

| 고정 upstream checkout | 다음 명령 | 추가 입력 |
| --- | --- | --- |
| Typst `70ca0d257bb4ba927f63260e20443f244e0bb58c` | `cargo test --workspace --test tests -- layout/container.typ` / `cargo test --workspace --test tests -- math/content.typ` / `cargo test --workspace --test tests -- layout/align.typ` | Cargo·해당 판 빌드 의존성·upstream test assets/fonts. 실제 필터가 고른 시험 수 확인. [Typst 재현](evidence/typst-official/reproduce.md) |
| Git `bea9ecd24b0c3bf06cab4a851694fe09e7e51408` | 빌드 후 `make -C t T=t2070-restore.sh` | 그 판 Git 테스트 빌드와 test-lib. 설치된 Git2.56.1 합성 fixture와 구별 |
| FFmpeg `af25a4bfd2503caf3ee485b27b99b620302f5718` | 빌드 후 `make fate-copy-psp fate-copy-trac3074 fate-copy-trac236 SAMPLES=/absolute/path/to/fate-suite` | 공식 sample corpus의 `h264/wwwq_cut.mp4`, `eac3/csi_miami_stereo_128_spx.eac3`, `mov/fcp_export8-236.mov`; configure·sample SHA·ref diff 기록 |

### 7.4 접근 실패한 원 이미지·원 링크

QR 입력 `https://i.sstatic.net/iyzQE.png`, 답변 그림 `HUbgd.png`, `gDvdB.png`, `2dmoc.gif`는 당시403, 두 gyazo 사진은503, `https://imagemagick.org/Usage/distorts/`는404였다. 원주소·UTC는 [image-acquisition.json](evidence/imagemagick/stage3/image-acquisition.json)과 [original-link-acquisition.json](evidence/imagemagick/stage3/original-link-acquisition.json)을 읽는다. 접근이 회복되면 새 bytes와 SHA를 `.cache/`에 저장하고 과거 실패 영수증을 유지한다. QR에는 reader 이름/판·payload·성공 판정이, 사진에는 source corners·목표 크기/aspect·viewport와 자동 검출 단계가 추가로 필요하다. 접근 가능한 다른 그림을 원 입력이라고 대체하지 않는다.

## 8. 고정 GitHub 판 재열람과 실행 영수증 해석

검사한 결과 SHA에서 GitHub의 `RESULT.md` 첫 세 표, `initial.csv`, `candidates.csv`, 대표 원자료 영수증, 대표 출력·재현 절차를 다시 연다. 주소는 `https://github.com/laadkke-arch/agentflow-open/blob/<checked_result_sha>/docs/workstreams/research/AF-RES-101/<path>` 형태다. 움직이는 branch URL만 읽고 고정 결과를 검증했다고 쓰지 않는다. API 또는 raw bytes로 읽었다면 실제 열린 URL·blob/본문 해시·UTC를 남긴다.

이 문서의 기존 스크립트 인자·입출력 경로와 두 검사 CLI 도움말은 작성 시 읽어 확인했다. **문서 전체의 깨끗한 새 환경 순차 재실행**, 원7.0.10-61/Cygwin, Ruby wrapper 실행, 전체 상류 suite는 이번 추가 문서 작성에서 실행하지 않았다. 실행된 연구 결과의 근거는 각 기존 receipt이고, 여기 적은 준비·추가 명령은 미래 재현 절차다. 성공 종료, 의도한 실패, 예상치 못한 실패, 환경 부족으로 시작하지 못한 작업을 각각 보존한다.
