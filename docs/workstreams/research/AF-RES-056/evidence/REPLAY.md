# 재생 입력과 실제 실행의 경계

이 안내는 원격 고정판에서 같은 자료를 다시 계산할 때 필요한 입력을 구분한다. 원래 receipt를 보존하려면 별도 checkout에서 실행한다. 연구자 진단의 통과를 원 사용자 전체 요구의 통과로 바꾸지 않는다.

## 커밋된 파일만으로 가능한 검산

저장소의 stage1/stage2 Git 객체와 이 결과판을 가져온 checkout에서 다음을 실행한다. 첫 명령은 파일을 수정하지 않고 stdout으로 검산 결과를 출력한다. 나머지 두 감사기는 자신의 receipt를 쓰므로 별도 checkout을 사용한다.

```bash
python -B docs/workstreams/research/AF-RES-056/evidence/validate_report.py
python -B docs/workstreams/research/AF-RES-056/evidence/review/ranking_audit.py
python -B docs/workstreams/research/AF-RES-056/evidence/review/window_audit.py
```

순위 감사는 Git 고정 입력을, 창 감사는 저장한 경계/해시/판정 receipt를 재계산한다. 창 감사가 원 공급자 프로그램을 다시 실행하거나 현재 홈페이지를 원래 응답으로 다시 읽는 것은 아니다.

## 공개하지 않은 최초 질문 본문 캐시

원문 전문을 그대로 재배포하지 않기 위해 `evidence/schema-pre/revisions-p1.json`은 커밋하지 않았다. 최초 조사와 원문 감사에서는 이 실제 API 응답의 revision1 본문40개를 읽고 body hash를 재계산했다. 그 감사의 입력 hash와 결과는 `review/source-audit-receipt.json`에 남겼다. LD40개는 후속 감사에서 metadata 연결만 확인했다.

아래는 **미실시 재개용 명령**이다. 이번 조사에서 직접 사용한 같은 Stack Exchange posts/revisions endpoint와 frame의 같은40 ID를 사용하며, 내용·GUID가 고정 원장과 모두 일치할 때만 새 캐시를 쓴다. 새 응답의 HTTP/byte hash를 원래 응답과 같다고 주장하지 않는다. API 접근/백오프/개정 누락이 있으면 멈추고 같은 질문 ID의 공개 개정 이력 또는 덤프를 확보해야 한다. 다른 질문으로 바꾸지 않는다. 이 재조회로 역사적 tag/alias·삭제 모집단 결손이 해결되는 것은 아니다.

```bash
python -B - <<'PY'
from pathlib import Path
import csv, datetime, hashlib, json, urllib.request
p = Path('docs/workstreams/research/AF-RES-056')
with (p/'frame.csv').open(newline='') as f:
    rows = [r for r in csv.DictReader(f) if r['domain'] == 'JSON Schema']
ids = ';'.join(r['question_id'] for r in rows)
items, requests = [], []
for page in range(1, 101):
    url = f'https://api.stackexchange.com/2.3/posts/{ids}/revisions?site=stackoverflow&pagesize=100&page={page}&filter=withbody'
    with urllib.request.urlopen(url, timeout=45) as response:
        body = response.read()
        final = response.geturl()
    data = json.loads(body)
    requests.append({'url':url, 'final_url':final,
                     'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     'response_sha256':hashlib.sha256(body).hexdigest()})
    if data.get('backoff'):
        raise SystemExit(f"API backoff={data['backoff']}; stop and resume after that interval")
    items.extend(data.get('items', []))
    if not data.get('has_more'):
        break
else:
    raise SystemExit('Pagination exceeded the explicit replay cap')
first = {str(r['post_id']):r for r in items
         if r.get('revision_number') == 1 and 'body' in r}
for row in rows:
    original = first[row['question_id']]
    assert original['revision_guid'] == row['revision_guid'], row['question_id']
    assert hashlib.sha256(original['body'].encode()).hexdigest() == row['body_sha256'], row['question_id']
target = p/'evidence/schema-pre/revisions-p1.json'
assert not target.exists(), 'Do not overwrite an existing captured response'
target.write_text(json.dumps({'items':items,'replay_requests':requests,
                             'scope':'new acquisition of the fixed 40 IDs; not the original HTTP snapshot'},
                            ensure_ascii=False))
print('Recovered and checked', len(rows), 'fixed first-revision bodies')
PY
python -B docs/workstreams/research/AF-RES-056/evidence/review/source_audit.py
```

위 캐시는 source_audit의 재해시에만 사용하고 공개 커밋에 전문을 추가하지 않는다. 현재 홈페이지의 예전 응답은 바뀔 수 있으므로 `review/render_window_check.py`를 단순 live 재조회로 원래 관측처럼 재생할 수 없다. 그 계산에는 원래 `home-parsed-full.json`, v1 추출문과 고정 provider checkout이 필요하다. 공개 결과에는 각 응답/창 hash·단어 수·끝 위치·첫 링크와 v1/v2 판정이 남아 있다. 해당 캐시를 확보하지 못하면 원래 화면 내용의 독립 재생은 **미실시/미확인**으로 두어야 한다.

## 공급자 진단 재현

| 대상 | 정확한 입력·판·명령 | 결과를 해석할 범위 |
| --- | --- | --- |
| SC-032 C++ | [windows/FINDINGS.md](windows/FINDINGS.md)의 두 고정 SHA clone 및 `run_sc032_diagnostic.py`; 입력 `schema_fixture.cpp` | C2-only3입력. 잘못된 pii 수락은 그 schema의 C1 누락이며 라이브러리 전체의 불가능 아님 |
| python-jsonschema | [schema-diagnostics/FINDINGS.md](schema-diagnostics/FINDINGS.md)의 `run_diagnostics.py`; 입력 `selected-cases.json`와 고정 MIT snapshots | 실제 receipt는4.26.0의14호출. 문서판4.23.0 및 원 요구 전체 실행으로 소급하지 않음 |
| PyLD | [ld-suppliers/REPLAY_PLAN.md](ld-suppliers/REPLAY_PLAN.md)의 checkout·task-local dependency·runner; 입력 `minimal-fixtures.json`와 wheel hash lock | 최초 runner exit1이 관측된 예상 불일치. 후속 `trace_nest.py`의 exit0을 최초 통과로 합치지 않음 |
| 원 JS-4/LD-3 환경 | 원 Python/jsonld package lock, 전체 입력·schema/context 고정판, 옵션과 모호한 guard의 뜻이 먼저 필요 | 이 자료가 없어 원 프로그램 전체 공동시험은 미실시. 작은 fixture를 대신 넣어 완결을 만들지 않음 |

역사적 모집의 다음 첫 행동은 날짜가 명확한 Posts/PostHistory·당시 TagSynonyms와 삭제/태그 제거 범위를 확보하는 것이다. 2024cutoff 덤프 한 벌에 이미 삭제된 질문의 이력까지 들어 있다고 가정하지 않는다. 확보한 판의 URI·hash·범위를 먼저 고정하고 기존 frame을 보존한 별도 모집판에서 같은 생성일/ID·첫 적격4 규칙을 대조해야 한다.
