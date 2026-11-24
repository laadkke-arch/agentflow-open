# AF-RES-105 재현 안내

이 문서는 고정된 조사 기록의 재계산, 공개 자료의 별도 재취득, 현재 실행 환경의 작은 비교 시험을 구분한다. **검사할 결과 commit은 [HANDOFF.md](HANDOFF.md)에 적힌 결과 SHA다. `work/research-af-res-105`의 현재 tip으로 대체하지 않는다.** HANDOFF가 마지막 별도 commit이면 그 commit과 검사 대상 결과 commit은 다르다.

이 문서를 작성하면서 네트워크 요청이나 시험을 실행하지 않았다. 실행 완료 여부는 기존 acquisition/execution 영수증과 최종 HANDOFF를 따른다. 아래 재시도 명령을 그 자체로 실행 증거로 읽지 않는다. 이미 결과를 읽은 사람이 전 과정을 다시 실행하는 것은 새 맹검 실험이 아니며, 원 작성자의 환경이나 AF-RES-101 A/B를 복원하는 절차도 아니다.

## 1. 시작판, 의존, 입력 핀

| 역할 | 고정 값 | 확인 기록 |
|---|---|---|
| 실제 시작 통합판 | `32b6bb32989730df78d521c29a50dbebd3289b46` | [manifest.json](manifest.json) |
| 통합 브랜치 | `chore/workspace-foundation`, remote `origin` | manifest의 `integration` |
| 작업 브랜치 | `work/research-af-res-105` | [SCOPE.md](SCOPE.md), 원격 봉인 영수증 |
| 계획 시점 통합판 | `49f603a98188fbf2009c4c490b0539f32d124e38` | [contract-read.json](evidence/start/contract-read.json) |
| 운영 의존 AF-RES-101 | `work/research-af-res-101=b29c25fe6d7375dc28c4c700da2240c1a205093d` | manifest의 `dependencies` |
| 연구 입력 AF-RES-101 결과판 | `392ff3d651577ab6aacd65f4ed86884586b960d1` | contract-read의 입력 파일별 blob |
| 허용 경로 | `docs/workstreams/research/AF-RES-105/` | manifest의 `allowed_paths` |
| 계약 snapshot | version `2`, SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc` | manifest의 파일별 계약 해시 |

계획판에서 실제 시작판까지 바뀐 경로는 `docs/automation/dot-control.json`이었다. 계약·연구 규칙 등 비교한 파일의 blob은 동일했고, 별도 시작 영수증이 이 차이를 보존한다. AF-RES-101 연구 입력판과 운영 인계판 사이의 해당 작업 변화는 HANDOFF 추가였다. 이전 연구의 결과와 인계 문서를 읽은 사실을 그 연구의 사용자 세션 재실행으로 부르지 않는다.

### 최초 계약 생성 명령

다음은 새 작업 브랜치가 실제 시작판을 가리키고, manifest 출력 파일이 아직 없는 최초 계약 생성에 해당하는 명령이다. **결과 checkout에서 다시 실행하여 기존 manifest를 덮어쓰지 않는다.** 현재 원격 통합판이나 의존 브랜치가 이동했다면 이 명령은 옛 시작 상태를 재현하지 않으며, 새로운 작업 계약으로 별도 기록해야 한다.

```bash
python -B -m workbench.session start af-res-105 \
  --allow docs/workstreams/research/AF-RES-105/ \
  --dependency work/research-af-res-101=b29c25fe6d7375dc28c4c700da2240c1a205093d \
  --output docs/workstreams/research/AF-RES-105/manifest.json \
  --fetch
```

`--fetch`와 `--integration-ref`는 함께 쓸 수 없다. `--integration-ref`는 로컬 기준을 지정하는 옵션이지 원격 최신성 확인을 대신하는 옵션이 아니다. 실제 CLI 정의는 `workbench/session.py`, 공통 절차는 `docs/CLOUD_WORKFLOW.md`에 있다.

## 2. HANDOFF 결과 SHA의 깨끗한 checkout에서 검사

먼저 최종 전달된 HANDOFF의 고정 링크를 열고 **결과 SHA**와 **HANDOFF SHA**를 구분한다. 아래 `AF105_RESULT_SHA`에는 HANDOFF에서 확인한 40자리 결과 SHA를 설정한다. 아직 결과 SHA를 확인하지 않았다면 브랜치 tip을 넣어 진행하지 않는다.

```bash
: "${AF105_RESULT_SHA:?Set the exact 40-character result commit recorded in HANDOFF.md}"
python -B - <<'PY'
import os, re
assert re.fullmatch(r'[0-9a-f]{40}', os.environ['AF105_RESULT_SHA'])
PY
git fetch origin "$AF105_RESULT_SHA"
export AF105_CHECKOUT="${TMPDIR:-/tmp}/af105-result-$AF105_RESULT_SHA"
git worktree add --detach "$AF105_CHECKOUT" "$AF105_RESULT_SHA"
cd "$AF105_CHECKOUT"
test "$(git rev-parse HEAD)" = "$AF105_RESULT_SHA"
test -z "$(git status --porcelain)"
```

`AF105_CHECKOUT`은 새 경로여야 한다. 이미 같은 경로에 작업물이 있으면 덮어쓰거나 삭제하지 말고 다른 새 경로를 쓴다. Git 이력이 없는 파일 압축본만으로는 봉인 SHA와 `git show`를 쓰는 재계산 검사를 수행할 수 없다.

요청된 개별 계약 검사, 조사 원장 검사, 공통 검사는 다음과 같다. 실제 실행자는 각 종료값과 출력을 보존한다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-105/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-105/recalculate.py --check
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

공통 기본 명령은 `python scripts/cloud_check.py --environment codex-cloud --fetch-contract`이며, 결과판의 깨끗한 사본 검사에서는 위와 같이 `--require-clean`을 추가한다. 기존 저장소 검사만 직접 재실행해야 한다면 `python -B scripts/check.py --require-git`가 해당 명령이다. 이 안내서 작성자는 이 명령들을 추가 실행하지 않았다. 최종 실행 여부와 검사 SHA는 HANDOFF와 최종 검사 영수증에서 확인한다.

`cloud_check.py`는 `.workbench/cloud-check.json`과 `.workbench/cloud-check-logs/<run-id>/`에 새 영수증·출력을 쓴다. `environment=codex-cloud`는 호출자가 지정한 이름이며 계정 연결 증거가 아니다. `session_validation.count`, `reason`, 직접 지정한 manifest 검사 결과를 따로 읽는다. 자동 발견은 `docs/tasks/*.json`의 활성 세션을 대상으로 하므로, 소유 경로 안의 이 manifest를 직접 검사했다고 자동 발견 수를 1로 바꾸지 않는다.

나중에 원격 계약이나 의존 브랜치가 이동해 `--fetch` 검사가 실패하면 그 변경을 남긴다. 과거 PASS를 재현하려고 manifest를 갱신하거나 검사를 약화하지 않는다. 네트워크 없는 구조 진단이 필요할 때 아래 명령은 가능하지만 결과는 **local_only**다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-105/manifest.json \
  --integration-ref 32b6bb32989730df78d521c29a50dbebd3289b46
```

## 3. 봉인과 자료 노출 순서

실제 원격 확인 기록은 [evidence/seals/commits.jsonl](evidence/seals/commits.jsonl)에 있다.

| 단계 | 원격 확인 SHA | 확인 UTC | 다음에 허용된 판독 |
|---|---|---|---|
| 0 — 범위·초기 규칙 | `15ad66b68f974073d2a0ab880314a3130145c2c2` | 2026-11-23 23:32:25.474872 | 최초판 모집·판독 계속 |
| 1 — 초기 8자리·보조 검색 규칙 | `de11fb2b05c0e65cc1451826c720eebcbc3e52cd` | 2026-11-23 23:43:05.543932 | 첫 타인 제안과 보조 후보 모집 |
| 2 — 첫 제안·보조 4자리 | `4a4aae107be25f71318dbb0c7b7cfa73506c5030` | 2026-11-24 00:04:06 | 작성자 후속·공식 동작·원 첨부·반례 |
| 3 — 후속·공식·교차 분야 | `242ccb21a00fb769b0bd40e54afc52f0a2f30fad` | 2026-11-24 00:38:37 | 결과·분모·재현·자가검토 |
| 4 — 결과판과 마지막 HANDOFF | HANDOFF의 결과 SHA 사용 | 최종 HANDOFF 참조 | 고정 결과판 검사·인계 |

현재 원격 브랜치가 과거 봉인 SHA와 같을 필요는 없다. 과거 확인 시점은 위 영수증으로 확인하고, 결과 checkout에서는 각 봉인 commit이 결과의 조상인지 별도로 확인할 수 있다.

```bash
git merge-base --is-ancestor de11fb2b05c0e65cc1451826c720eebcbc3e52cd "$AF105_RESULT_SHA"
git merge-base --is-ancestor 4a4aae107be25f71318dbb0c7b7cfa73506c5030 "$AF105_RESULT_SHA"
git merge-base --is-ancestor 242ccb21a00fb769b0bd40e54afc52f0a2f30fad "$AF105_RESULT_SHA"
```

연결 확인 중 통합 담당자는 질문 309037의 현재 채택·답변 수·점수 metadata 일부를 먼저 보았다. [exposure-log.jsonl](evidence/start/exposure-log.jsonl)이 이를 기록한다. 초기 선택은 그 출력을 받지 않은 두 새 문맥 판독자가 맡았고 SCOPE 7절을 제외해 읽었다. 통합 담당자가 완전 맹검이었다는 주장은 하지 않는다. 새로 초기 맹검 판독을 반복하려면 결과·선정 ID·후속을 읽지 않은 판독자에게 초기 규칙과 마스킹한 자료만 제공해야 한다. 이 완성된 재현 안내서를 읽은 판독자를 새 맹검 판독자로 간주하지 않는다.

## 4. 시간순 모집 API와 최초판 투영

### 고정 query

Stack Exchange API v2.3의 `questions`를 다음 인수로 요청한다. 필터 문자열을 `default`나 `withbody`로 바꾸지 않는다.

```json
{
  "fromdate": 1704067200,
  "todate": 1719791999,
  "sort": "creation",
  "order": "asc",
  "pagesize": 80,
  "page": 1,
  "filter": "7W-GLRnw_MC-oFjiXW2Yp.*Kixtw9X1Cp_B-Jb"
}
```

| 모집 | 추가 인수 | 고정 기본 기간 |
|---|---|---|
| Blender | `site=blender`, `tagged=geometry-nodes` | 2024-01-01 00:00:00–2024-06-30 23:59:59 UTC |
| QGIS | `site=gis`, `tagged=qgis` | 같은 기간 |

질문은 `(creation_date, numeric question_id)` 오름차순 첫 80개다. `has_more=true`여도 이 80개 프레임을 반년 전체 전수라고 부르지 않는다. 현재 태그로 검색했으므로 현재 태그가 제거된 과거 관련 질문은 찾지 못한다. 최초판 태그와 현재 태그는 각각 저장한다. 최초 태그에 검색 태그가 없어도 최초 내용이 관련 처리이면 내용으로 판정한다.

각 80개를 실제 읽고도 적격 4개 미만일 때만 `fromdate=1719792000`, `todate=1735689599`인 2024년 7–12월 첫 80개로 한 번 연장한다. 이번에는 두 사이트 모두 연장하지 않았다.

### 경계 동률

최종 helper는 마지막 항목 시각의 `boundary-1`부터 `boundary+1`까지 같은 마스킹 필터, `pagesize=100`으로 조회한다. 정확히 같은 생성시각의 ID를 합쳐 숫자 ID로 재정렬한 뒤 첫 80개를 유지한다. `has_more`가 남거나 알려진 마지막 ID가 응답에 없으면 경계 확인 완료로 처리하지 않는다.

실제 최초 실행의 별도 경계 기록은 다음과 같다.

| 사이트 | 80번째 질문/시각 | 실제 경계 확인 |
|---|---|---|
| Blender | 310379 / `1705962876` / 2024-01-22 22:34:36 UTC | 같은 초 조회는 빈 응답. 이를 근거로 쓰지 않고 `1705962875..1705962877` 조회로 해당 초의 310379만 확인; 첫 80개 불변 |
| GIS | 474078 / `1704966405` / 2024-01-11 09:46:45 UTC | 같은 초 조회는 빈 응답. 동일 기본 query의 `page=2,pagesize=80` metadata에서 첫 항목 474083, `1704970184`를 확인; 추가 본문은 읽지 않았고 첫 80개 불변 |

근거는 [Blender 초기 판독 기록](evidence/blender-initial/reading-notes.md)과 [QGIS 경계 기록](evidence/qgis-initial/boundary-check.json)이다. 현재 helper의 좁은 시간 bracket은 과거 QGIS의 page-2 확인과 구분한다.

### 최초 revision만 노출

`research_io.initial_revisions`는 `posts/{semicolon-separated-ids}/revisions`에 `site`, `pagesize=100`, 증가하는 `page`, 위 초기 필터를 요청한다. 모든 응답은 캐시에 보존하되 **`revision_number==1` 투영만 판독자에게 출력**한다. 같은 post의 충돌하는 revision-1 GUID는 오류로 남긴다. 최초판 본문·그림을 실제 읽은 뒤 대상, 관측 가능한 목표, 구체적인 이미 수행한 조작을 확인한다. 이름 언급이나 코드 자리표시자만으로 T/O를 채우지 않는다.

다음은 새 공개 스냅샷을 별도 캐시에 취득하는 명령이다. 이 명령은 사람의 적격 판독이나 과거 80개의 불변성을 자동으로 증명하지 않는다. 저장된 연구 결과와 섞지 않는다.

```bash
export AF105_ROOT="$AF105_CHECKOUT/docs/workstreams/research/AF-RES-105"
export AF105_ACQUIRE="$AF105_ROOT/.cache/acquisition-replay"
mkdir -p "$AF105_ACQUIRE"
cp "$AF105_ROOT/research_io.py" "$AF105_ACQUIRE/research_io.py"
python -B - <<'PY'
from pathlib import Path
import os, sys
sys.path.insert(0, os.environ['AF105_ACQUIRE'])
from research_io import initial_frame, initial_revisions
for site, tag, reader in [('blender','geometry-nodes','blender-initial'),
                          ('gis','qgis','qgis-initial')]:
    frame, _ = initial_frame(site, tag, reader, half=1)
    ids = [q['question_id'] for q in frame]
    first, _ = initial_revisions(ids, site, reader, 'h1')
    assert len(ids) == len(set(ids)) == 80
    assert set(first) == set(map(str, ids))
    assert all(first[str(i)].get('body') for i in ids)
    assert len({first[str(i)]['revision_guid'] for i in ids}) == 80
    print(site, 'first80', len(ids), 'initial_body_count', len(first))
PY
```

원 응답 전체나 현재 질문 페이지를 초기 판독자에게 보여 주지 않는다. 캐시의 `h1-initial-only.json`만 초기 판독 대상으로 전달한다. 원 이미지 URL을 직접 열어 읽고, 성공/실패·UTC·바이트 해시·실제 읽은 영역을 기록한다. 링크 존재만으로 노드·매개변수를 추측하지 않는다. 이미지가 없어도 텍스트에 충분한 시도 증거가 있으면 그 결측을 남긴 채 적격일 수 있다.

이번 판독은 각 사이트 80개 전부였다. Blender는 적격 70/제외 10, 선정 순위 1·2·3·4였다. GIS는 적격 47/제외 33, 선정 순위 1·3·4·7이었다. 이 수치는 새 재조회에서 동일할 것을 가정하지 않고, 봉인된 `frame.csv`와 초기 영수증에서 재계산한다.

## 5. 첫 제안 고정과 후속 분리

단계 1 원격 확인 후에만 선택 질문의 타인 답변과 **질문 댓글**을 `(creation_date, numeric event ID, body order)`로 정렬한다. 질문 생성 후 30일 안에 입력에 적용할 연산/단계를 지목한 첫 제안 한 개를 고정한다. 명확화 질문만의 댓글은 제외하며, 한 답에 방법 두 개가 있으면 첫 방법을 주 단위로 둔다. 답변 댓글은 첫 제안 모집 단위에 넣지 않는다.

공개 corpus 취득은 [acquire_episodes.py](acquire_episodes.py)의 `collect`와 `pages`를 따른다.

```text
GET https://api.stackexchange.com/2.3/questions/{question_ids}/answers
GET https://api.stackexchange.com/2.3/posts/{question_and_answer_ids}/comments

site=blender 또는 gis
fromdate=1704067200&todate=1735689599
sort=creation&order=asc&page=1부터 증가&pagesize=100
filter=RXBclA_iTvr1Vkp7e4w7BNj)RNrc4avJuy-XQ*WKgptGK(hfFWaiTNFAhTF)br7Q*arP
```

ID는 100개씩 묶고 마지막 `has_more=false`까지 받는다. API backoff/error나 예외적인 페이지 수는 실패/미완료로 기록한다. `acquire_episodes.py <site> --seal-sha <SHA>`의 인수는 그 자체로 원격 확인을 수행하지 않으므로, 호출자가 별도로 봉인 영수증을 확인해야 한다. 재취득에는 별도 복사본과 새 기록 경로를 쓴다. 완료된 결과판에서 수집·조립 스크립트를 실행해 봉인 원장을 덮어쓰지 않는다.

수집 당시 현재 답변 본문이 raw cache에 들어왔더라도 바로 읽지 않는다. 답변 ID의 revision 응답을 먼저 최초판으로 투영하여 당시 첫 방법·그림·링크를 확인한다. 나중에 추가된 조작을 답변 생성시각으로 소급하지 않는다. 댓글은 생성시각은 알려져도 공개 편집 이력이 없어 현재 문구의 정확한 최초 출현 시각은 미확인일 수 있다. 원래 연결한 예제와 연구자가 나중에 찾은 공식 문서는 다른 열에 둔다.

첫 제안 시각보다 앞선 **원 질문 작성자**의 수정·댓글만 초기 보충으로 따로 보존한다. 최초판을 덮어쓰지 않는다. 원 작성자의 제안 이후 댓글·수정·자기 답은 단계 2 원격 확인 뒤에 연다. 이후 관측 창은 각 고정 제안 시각부터 정확히 180일이며, 같은 주체·같은 조작·제안 이후 실행 여부를 각각 확인한다. 공개 ID가 없는 경우 이름만으로 동일인 판정을 보충하지 않는다.

## 6. 보조 모집: 고정 26개 query JSON과 닫힌 범위

실행할 문자열의 기준은 [auxiliary-search-plan.json](evidence/start/auxiliary-search-plan.json)의 26개 `queries`다. 각 사이트에 대해 아래 13개 문구를 이 순서로 검색했다. 사이트 순서는 `blender.stackexchange.com`, `gis.stackexchange.com`이다.

```json
[
  "already tried", "already knew", "already know", "i tried that", "i knew that",
  "didn't know", "didn’t know", "did not know", "wasn't aware", "wasn’t aware",
  "was not aware", "never knew", "was unaware"
]
```

각 query는 `site:HOST "PHRASE" "2024"`이다. 검색 도구는 **`system1_search_query`**, query마다 1회 응답, `response_length=long`, 추가 페이지 없음이다. 곡선/ASCII 아포스트로피 query를 모두 유지한다. `had already tried`와 `have already tried`는 본문 사전에 있으며 `already tried` query/정규화 범위 안에서 검사한다. 검색 결과의 문구나 날짜 표시는 적격 증거가 아니다.

다음 로컬 명령은 고정 계획을 그대로 읽어 **26개 도구 요청 JSON을 출력할 뿐**, 검색하지 않는다. 실제 재검색을 한다면 각 `tool_arguments`를 `mcp__codex_apps__search_service_web_run`에 한 번씩 전달하고, 새 UTC·응답 경계·반환 순위·URL·실패를 별도 실행 기록에 남긴다.

```bash
python -B - <<'PY'
from pathlib import Path
import json
p = Path('docs/workstreams/research/AF-RES-105/evidence/start/auxiliary-search-plan.json')
plan = json.loads(p.read_text())
assert len(plan['queries']) == 26
assert plan['engine'] == 'system1_search_query'
assert plan['calls_per_query'] == 1 and plan['extra_pages'] is False
for q in plan['queries']:
    print(json.dumps({'query_id': q['query_id'],
        'tool_arguments': {'system1_search_query': [{'q': q['q']}],
                           'response_length': 'long'}}, ensure_ascii=False))
PY
```

실제 검색은 2026-11-23T23:46:42.479Z에 26개 응답을 끝냈다. 반환 URL 출현은 152개, 문자열 기준 서로 다른 URL은 145개였고 도구 오류 기록은 0개였다. 같은 질문의 다른 URL과 검색 노출 횟수는 고유 사건·자료 수가 아니다. [search-results.json](evidence/auxiliary/search-results.json)은 query별 실제 반환 URL과 판독 노출 경계를 보존한다.

### 본문 정규화와 자격 판정

실제 `acquire_episodes.py` 구현은 아래 순서다. HTML 태그를 공백으로 바꾸고 entity를 decode한 visible text에 NFKC, 소문자, 곡선 아포스트로피 변환을 적용한다. frozen 사전의 각 문구는 `(?<!\w)`와 `(?!\w)` 경계로 찾고 본문 위치순으로 정렬한다.

```python
visible = html.unescape(re.sub(r'<[^>]*>', ' ', text))
value = unicodedata.normalize('NFKC', visible).lower()
value = value.replace('\u2019', "'").replace('\u2018', "'")
```

HTML entity 보정은 보조 후보 본문 판독·선정 **이전**에 기록되었다. query나 지식 사전을 늘린 것이 아니며, 옛 raw-HTML 적중 투영과 corrected visible-text 투영을 따로 보존했다. 보정 시점·parser 해시·전후 수는 [pool-close.json](evidence/auxiliary/pool-close.json)에 있다.

닫힌 범위는 다음 두 집합의 공개 2024년 답·질문 댓글·답변 댓글이다.

1. 사이트별 시간순 최초 80개 현재 태그 질문과 그 공개 답/댓글.
2. 위 26개 query가 실제 반환한 URL에서 확인한, 2024년 말까지 생성된 현재 관련 태그 부모 질문과 그 공개 2024년 사건.

검색색인 밖의 전체 2024년 댓글을 전수 조사한 것이 아니다. 부모 질문은 2024년보다 앞설 수 있지만 적격 진술은 실제 사건 시각/첫 출현 범위로 검사한다. API 페이지를 소진하거나 실패를 기록한 뒤, **2026-11-23T23:49:08.391264Z**에 후보 풀을 닫았다. 이후 발견한 반례는 고정 4자리를 교체하지 않고 별도 반례 묶음에 둔다.

| corpus | 질문 | 답 | 댓글 | 사건 레코드 |
|---|---:|---:|---:|---:|
| Blender 최초 프레임 | 80 | 75 | 316 | 391 |
| Blender 검색 추가 부모 | 11 | 11 | 56 | 67 |
| GIS 최초 프레임 | 80 | 58 | 245 | 303 |
| GIS 검색 추가 부모 | 22 | 14 | 60 | 74 |

visible-text 사전 적중은 Blender 9개, GIS 13개로 총 22개 사건이었다. 원 작성자 공개 ID가 일치한 적중은 각각 8개와 9개였지만, 이것도 자동 자격 판정은 아니다. 구체적인 제안 지시 대상과 진술 의미를 읽고 시간순 `(발언 시각, 숫자 ID, 본문 순서)`으로 판정했다. 같은 사건이 두 계열에 해당하면 먼저 나온 적격 발언/본문 부분에 배정하고 다른 계열은 다음 독립 사건으로 진행한다. 시간순 8자리와 같은 사건은 재사용하지 않는다. 최종 4자리는 BL-K1, BL-N1, QG-K1, QG-N1이며, 빈자리 0은 **이 닫힌 검색 가능 범위에서**의 결과다. 이 목적 표본으로 사전인지/신규인지 발생률을 추정하지 않는다.

## 7. 원장·출처·보고서 재계산

검증의 기준은 [recalculate.py](recalculate.py)의 `--check`다. `--write`는 산출물을 생성하는 모드이므로 검증 실패를 해소하려고 자동 실행하지 않는다.

```bash
python -B docs/workstreams/research/AF-RES-105/recalculate.py --check
```

이 명령은 다음 연결을 확인하고 저장된 [evidence/reconciliation.json](evidence/reconciliation.json)과 재계산 결과를 비교한다.

- `frame.csv`: 시간순 160개 최초 요청과 보조 적중 22개 사건, rank/생성시각/숫자 ID, 적격 순서의 첫 4개.
- `initial.csv` ↔ `proposals.csv` ↔ `followup.csv` ↔ `returns.csv`: 각각 12개의 유일 `case_id`, 일치하는 질문·candidate·episode·원제안 URL.
- 단계 1 `initial.csv`의 시간순 8개 값과 단계 2 `proposals.csv`의 12개 값: 봉인 SHA에서 `git show`로 읽어 현재 원장과 대조. 후속 결론으로 초기판을 바꾸지 않았는지 확인.
- 작성자 사건 수, 공개 주체 ID, 제안 전후 관계, 정확한 180일 창, 최초 30일 창, 판정 가능/미확인 분모, 반환 선택지.
- JSON 배열 형태의 `source_refs`와 `sources.jsonl`의 유일 `source_id`; 고유 저작 계보, 필수 범주별 서로 다른 자료, 실패 응답의 비산입.

저장된 재계산은 PASS, 원장 `frame` 182행, 선택 episode/candidate 각각 12개, 필수 자료 24개, 보수적으로 산입한 고유 1차자료 32개다. 필수 할당은 요청 8 + Blender 공식 4/상류 2 + QGIS 공식 4/상류 2 + Calc 2 + Audacity 2다. 같은 사건의 수정·댓글·첨부, 같은 문서의 앵커·미러·판, 실패 응답을 별도 필수 자료로 늘리지 않는다. 세부 기준 ID는 [source-counts.json](evidence/source-counts.json)에 있다.

`--check`에서 말하는 보고서 대조 대상은 **reconciliation JSON**이다. 산문 `RESULT.md`를 자동으로 사실 검증하는 코드는 아니다. 산문 숫자와 사례 해석은 [result-tables.md](evidence/result-tables.md), [return-perspectives.json](evidence/return-perspectives.json), 각 원장·원자료 locators에 대조한다. 생성 스크립트 `build_result.py`, `assemble_stage2.py`, `assemble_stage3.py`, `merge_sources.py`는 출력 파일을 쓰므로 결과판의 읽기 전용 검증 명령에 넣지 않는다.

현재 전 조작 신규성 판정 가능 분모는 시간순 0/8, 보조 0/4다. `0/0`은 0%가 아니라 산출 불가다. 부분 능력의 명시 신규 진술, 전체 제안 인지, 같은 제안 실행, 성공, 학습 후 같은 조작 실행은 다른 열이다. 감사·투표·채택 또는 문서 동작을 실행/인지 증거로 승격하지 않는다. 공개 작성자 ID가 없는 슬롯도 결측으로 유지한다.

## 8. 실제 현재판 실행과 읽기만 한 상류 자료

| 묶음 | 실제 수행 | 재현 안내와 한계 |
|---|---|---|
| Blender 원 첨부 4개 | 바이트/헤더 확인, scripts 비활성, Blender 4.3.2 구조 판독·평가 | [Blender 상세 재현](evidence/blender-official/reproduce.md) 1–3절; 원 입력 해시와 script 해시 포함 |
| Blender 합성 probe 3개 | 섬별 edge 선택, modifier copy/convert, Compare/Pivot 대비; 전부 통과 | 같은 안내; 원 사용자 환경 복원 아님 |
| QGIS 합성 probe 2개 | 3.40.6-Bratislava / GDAL 3.10.3 / Python 3.13.5; 반복 라벨·그룹별 라벨 | [QGIS 상세 재현](evidence/qgis-official/reproduce.md) 1절; 첫 enum 오류와 수정 후 성공을 모두 보존 |
| 보조 QGIS/GDAL semantics | 길이/보간/centroid 식, 단위 설정, 데이터셋 with/Close 후 reopen 비교 | 아래 9절; label 렌더링과 별개 |
| Blender C++ 2개 상류 저작 | v4.0.2 회전·벡터 시험의 입력/기대 단언 직접 판독 | 컴파일·시험 실행 **미실시**; 상세 재현 4절의 명령도 미실행 recipe |
| QGIS 상류 2개 저작 | 3.34.0 표현식과 GDAL 명령 생성 시험 입력/기대값 판독 | 빌드/상류 suite 실행 **미실시**; QGIS 상세 재현 2절 |
| Calc / Audacity | 고정 공식 자료와 별개 원 예제 판독 | [교차 분야 재현](evidence/crossdomain/reproduce.md); LibreOffice C++ 시험·Audacity 앱 실행 **미실시** |

QGIS native script도 `Path(__file__).parents[2]`를 작업 루트로 사용하므로, 봉인 결과를 보존하려면 디렉터리 모양을 유지한 별도 복사본에서 실행한다.

```bash
export AF105_QGIS_REPLAY="$AF105_ROOT/.cache/qgis-native-replay"
mkdir -p "$AF105_QGIS_REPLAY/evidence/qgis-official"
cp "$AF105_ROOT/evidence/qgis-official/native_probe.py" "$AF105_QGIS_REPLAY/evidence/qgis-official/native_probe.py"
/usr/bin/python3 -B "$AF105_QGIS_REPLAY/evidence/qgis-official/native_probe.py"
```

이 명령을 이번 문서 작성 중에 실행한 것은 아니다. 실행하려면 상세 문서에 기록된 Python bindings, Qt offscreen, GDAL, 폰트 조건이 필요하다. 다른 버전의 실행은 새로운 실행 기록으로 남긴다. 원본 결과와 새 결과를 섞지 않는다.

## 9. `probe_semantics.py`의 독립 복사본 재실행

이 보조 script는 원 입력 파일을 요구하지 않으며 합성 선과 점을 만든다. 다만 GDAL v3.8.4 공식 예제의 문자 그대로의 parse를 확인하기 위해 다음 고정 문서 바이트가 필요하다.

- 원시 URL: https://raw.githubusercontent.com/OSGeo/gdal/c2d2a61739ca770bae5a26be3eeb25a045dd3458/doc/source/api/python_gotchas.rst
- SHA-256: `94c2d8080ab3c0c434deff265464414752e5ad7e13c1ee896a972d6292e89128`
- 실행 script SHA-256: `64969aa706b9c373df886bd6ab413068034c2a61355897b81e26257e19c20dac`
- 기록된 runtime: QGIS `3.40.6-Bratislava`, GDAL `3.10.3`; 실제 명령은 `QT_QPA_PLATFORM=offscreen /usr/bin/python3 -B .../probe_semantics.py`.

다음 recipe는 문서를 재취득하고 해시가 맞을 때만 독립 복사본을 실행하며 새 stdout/stderr와 종료값을 보존한다. 이 문서를 작성하면서 수행하지 않았다.

```bash
export AF105_AUX_REPLAY="$AF105_ROOT/.cache/auxiliary-semantics-replay"
mkdir -p "$AF105_AUX_REPLAY/evidence/auxiliary-official"
mkdir -p "$AF105_AUX_REPLAY/.cache/auxiliary-official"
cp "$AF105_ROOT/evidence/auxiliary-official/probe_semantics.py" "$AF105_AUX_REPLAY/evidence/auxiliary-official/probe_semantics.py"
python -B - <<'PY'
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import hashlib, json, os, subprocess

root = Path(os.environ['AF105_AUX_REPLAY'])
script = root / 'evidence/auxiliary-official/probe_semantics.py'
assert hashlib.sha256(script.read_bytes()).hexdigest() == '64969aa706b9c373df886bd6ab413068034c2a61355897b81e26257e19c20dac'
url = 'https://raw.githubusercontent.com/OSGeo/gdal/c2d2a61739ca770bae5a26be3eeb25a045dd3458/doc/source/api/python_gotchas.rst'
opened = datetime.now(timezone.utc).isoformat()
with urlopen(Request(url, headers={'User-Agent':'AF-RES-105-public-reproduction'}), timeout=60) as response:
    data = response.read()
assert hashlib.sha256(data).hexdigest() == '94c2d8080ab3c0c434deff265464414752e5ad7e13c1ee896a972d6292e89128'
(root / '.cache/auxiliary-official/gdal-v3.8.4-gotchas.bin').write_bytes(data)
command = ['/usr/bin/python3', '-B', str(script)]
environment = os.environ.copy()
environment['QT_QPA_PLATFORM'] = 'offscreen'
started = datetime.now(timezone.utc).isoformat()
run = subprocess.run(command, env=environment, capture_output=True, timeout=120)
(root / 'stdout.log').write_bytes(run.stdout)
(root / 'stderr.log').write_bytes(run.stderr)
receipt = {'document_url':url, 'document_opened_utc':opened,
           'document_sha256':hashlib.sha256(data).hexdigest(),
           'command':command, 'QT_QPA_PLATFORM':'offscreen',
           'started_utc':started, 'ended_utc':datetime.now(timezone.utc).isoformat(),
           'exit_code':run.returncode,
           'stdout_sha256':hashlib.sha256(run.stdout).hexdigest(),
           'stderr_sha256':hashlib.sha256(run.stderr).hexdigest()}
(root / 'replay-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
raise SystemExit(run.returncode)
PY
```

결과 `evidence/auxiliary-official/probe-results.json`는 새 복사본 안에 생긴다. 원래 기록과 비교할 대상은 식 출력·단위 차이·reopen한 피처 내용과 실제 버전이다. 선 `(0,0)–(10,0)`의 거리 0.5와 절반 길이는 다르고, 꺾인 선의 중간점과 centroid도 다른 조작이다. GPKG with/Close 두 경로는 점 `(3,4)` 하나를 다시 읽었으며, 파일 바이트가 항상 같다는 주장은 하지 않는다.

공식 v3.8.4 예제에는 닫는 괄호가 빠져 문자 그대로의 `ast.parse`가 실패했다. 그 실패는 `gdal_manual_literal_parse`에 보존되고, 별도 합성 populate 코드는 독립 실행으로 기록되었다. 원문 예제를 수정하여 원 코드가 실행됐다고 만들지 않는다. 전체 process exit 0과 그 문자 예제의 parse 실패는 함께 성립한다. Qt/AF_NETLINK 경고도 삭제하지 않는다.

## 10. 접근 실패·미실행을 다시 시작할 정확한 위치

| 미완료 대상 | 재개 입력/명령 위치 | 이번 조사에서 하지 않은 일 |
|---|---|---|
| Blender GN `accumulate_field_column_grid.blend` | [Blender 상세 재현 5절](evidence/blender-official/reproduce.md), test-data commit `221f67d71e370f251d39ea7d863b9e08a18094ed`의 utilities 경로 | 403 이후 파일 내용/기대 geometry 판독·node fixture 실행 |
| Blender GN `sample_curves.blend` | 같은 안내, 같은 commit의 curves 경로 | 같은 결측; 현재 native probe로 대체하지 않음 |
| Blender 저수준 C++ tests | 상세 재현 4절의 v4.0.2 source/blob·GTest filter·입력/기대값 | dependency bundle 구성, configure/build, 실제 suite 실행 |
| QGIS 역사판 upstream tests | QGIS 상세 재현 2절, commit `ffbdd678812eec460ff02ff73bd36ee7955ac8a5` | 해당 판의 개발 build/Python 환경·fixture 구성과 실제 시험 실행 |
| R/spdep queen–rook | QGIS 상세 재현 3절, spdep1.3-2 commit `46c90789e61affa495e1b9139442f4416dc7e7af` | R/Rscript가 없어 설치·4사각형 합성 비교 **미실시**; 문서의 예상 간선 6/4는 관측값 아님 |
| Calc upstream formula test | 교차 분야 재현, LibreOffice24.2.0.3 core `da48488a73ddd66ea24cf16bbc4f7b9c08e9bea1` | `testFormulaRefUpdate` 실제 C++ 실행 |
| Audacity 원 보고 재실행 | 교차 분야 재현의 issue2371/5099 입력과 결측 | 원 음원·정확한 envelope 등 미확인; 앱 실행·raw sample 측정 **미실시** |
| 원 사용자 환경 | 사례별 `author_version`, 입력/매개변수 결측 | 12사건의 원 환경·동일 입력을 복원하지 않음 |

403 fixture의 재시도는 해당 상세 문서에 보존된 공개 URL을 사용하고 새로운 HTTP 상태를 남긴다. 성공해도 파일 헤더와 실제 입력/기대 객체를 먼저 읽는다. 2025 test-data와 2023 v4.0.2 harness의 matching build가 자동으로 성립하지 않으므로, 현재4.3.2 시험은 명시한 cross-version trial일 뿐이다. 상류 low-level test 두 개를 읽은 사실, node fixture 두 개의 접근 실패, 연구자 합성 probe 성공을 서로 바꾸어 세지 않는다.

## 11. 바뀔 수 있는 자료와 재현의 한계

공개 API는 현재 살아 있는 자료만 반환한다. 삭제된 댓글·답·계정은 복원하지 않았고, 댓글에는 공개 revision 이력이 없다. 답/질문 revision GUID는 읽은 본문 판을 고정하지만, 그 본문이 가리키는 이미지나 `.blend` URL의 현재 바이트가 당시 바이트와 같다는 보장은 별도로 확인하지 못했다. 현재 채택·투표는 관측 시점 metadata이며 채택 날짜나 실행 증거가 아니다.

이미지·첨부·manual HTML·공개 이슈 응답·검색 순위가 바뀌면 새 취득 UTC와 해시로 기록한다. 해시가 달라졌다고 과거 판독을 현재 내용으로 덮어쓰지 않는다. 새 search/API 프레임이 달라지면 기존 선택의 잘못으로 자동 처리하지도 않는다. 기존 선택은 봉인된 시점과 범위에서 감사하고, 새 모집은 별도 실행으로 닫는다.

원문 전체·바이너리는 무시되는 캐시에만 두고, 공개 URL·판/GUID/commit·UTC·위치·fingerprint·관측·한계를 영수증과 source ledger에 보존한다. source 전체 복사본이 없는 clean checkout에서 과거 bytes를 재취득할 수 없으면 그 부분은 정확한 locator를 가진 미확인으로 남는다. 수집 성공, 실제 판독, source-level 기대값, native 실행, 원 작성자의 말은 서로 다른 증거 수준이다.

마지막으로 결과 SHA에서 검사한 산출물과 마지막 HANDOFF 단독 commit을 구분한다. HANDOFF나 이후 브랜치 변화가 과거 결과판의 검사 범위에 포함된 것처럼 보고하지 않는다. 새 검사자는 실제 checkout SHA, 입력/script 해시, 명령, UTC, 종료값, stdout/stderr, 자동 발견 세션 수, 남은 실패·미실시를 새 기록으로 남긴다.
