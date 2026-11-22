"""Correct three common-input defects without changing the frozen v1 experiment."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
P=Path(__file__).resolve().parents[1]
manifest=P/'evidence/frozen-manifest-v2.json'
assert not manifest.exists(), 'v2 already frozen'
ts=datetime.now(timezone.utc).isoformat();paths=[]
for i in [1,2,3]:
    x=json.loads((P/f'reconstruction/views/view-{i}.json').read_text())
    x['protocol_version']='v2: common-observation identifier/path repair, same source pool and key'
    for c in x['cards']:
        if c['event_id']=='SW02':
            c['saved_url']='https://github.com/Homebrew/homebrew-core/blob/main/Formula/lib/libxml%2B%2B3.rb'
            c['current_lookup']='이 saved_url과 정확히 같은 URL에서 2026-11-22T03:15:16.399960Z anonymous GET HTTP404를 관측했다. 고정판본문은 별도 경로로 확보했다는 사실만 공통제공하며 내용/후계는 이 필드에 넣지 않는다.'
        elif c['event_id']=='MB04':
            c['current_lookup']='saved_url과 같은 recording7a3eb993-0b45-4ee3-971a-b385e9e92e11의 현재본문을 직접 읽었다: Back Again/Reamonn7:34, ISRC2개, 여러 Beautiful Sky release 연결. raw HTTP 미확인.'
        elif c['event_id']=='MB06':
            c['current_lookup']='2026현재 AcoustID track이 표시하는 target은 fd416d42-3d40-4a4f-9673-ca1a51fdedab 하나다. 2024 Fingerprints URL도 https://musicbrainz.org/recording/fd416d42-3d40-4a4f-9673-ca1a51fdedab/fingerprints 로 도착한다(웹 도구 관측; HTTP코드 아님).'
    path=f'reconstruction/views/v2-view-{i}.json';paths.append(path)
    (P/path).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
key='reconstruction/key/answer-key.json';paths.append(key)
m={'created_at_utc':ts,'version':'v2','reason':'three common-input defects found by audit after v1 answers; v1 retained and excluded from primary comparison','key_unchanged':True,'reader_plan':'three new fork_turns=none readers, one v2 view each, no v1 answers/key/web','sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in paths},'root_is_source_exposed':True}
manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/exposure-log.jsonl').open('a') as f:f.write(json.dumps({'at_utc':ts,'actor':'/root','action':'freeze v2 after audit common-input corrections; v1 kept immutable','files':paths,'key_unchanged':True,'sha256':m['sha256']},ensure_ascii=False)+'\n')
print(json.dumps(m,ensure_ascii=False))
