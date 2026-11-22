"""Repair two omitted III fields; preserve earlier records and carry forward unchanged cards."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
P=Path(__file__).resolve().parents[1]
manifest=P/'evidence/frozen-manifest-v4.json';assert not manifest.exists()
ts=datetime.now(timezone.utc).isoformat();paths=[];carry=[]
def cardhash(c):return hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
for i in [1,2,3]:
    x=json.loads((P/f'reconstruction/views/v3-view-{i}.json').read_text())
    previous={c['event_id']:cardhash(c) for c in x['cards']}
    x['protocol_version']='v4 final: two III fields explicitly supplied from already-read sources; sixteen cases carried forward only on identical card hashes'
    if i==3:
        for c in x['cards']:
            if c['event_id']=='MB05':
                c['saved_relationship_and_effective_history']+=' 48447069의 병합 방향은 release da729585-32c9-4261-8a30-322d7d414653 → 생존 target633a31aa-ed97-49fc-ab70-27f8e97fc5be이다(공식 target release history의 merge 행).'
            elif c['event_id']=='SW03':
                c['saved_relationship_and_effective_history']+=' 정정 commit8c2998215320942b1329f5b073fad7bfa33e9976의Formula/readline.rb도version6.2.4를기록한다(직접읽은revert후recipe). 현재최신formula의판을뜻하지않는다.'
    full=f'reconstruction/views/v4-view-{i}.json';paths.append(full)
    (P/full).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    repair=dict(x);repair['cards']=[c for c in x['cards'] if c['event_id'] in ['MB05','SW03']]
    sub=f'reconstruction/views/v4-repair-view-{i}.json';paths.append(sub)
    (P/sub).write_text(json.dumps(repair,ensure_ascii=False,indent=2)+'\n')
    for c in x['cards']:
        if c['event_id'] not in ['MB05','SW03']:
            assert previous[c['event_id']]==cardhash(c)
            carry.append({'event_id':c['event_id'],'representation':i,'card_sha256':cardhash(c),'answer_file':f'reconstruction/answers/v3-reader-{i}.json','unchanged_from_v3':True})
key='reconstruction/key/answer-key.json';paths.append(key)
m={'created_at_utc':ts,'version':'v4 final','primary_comparison':True,'reason':'MB05 merge target and SW03 post-revert version present in source but omitted by card writer; correct input defect, not source information loss','key_unchanged':True,'repair_cases':['MB05','SW03'],'new_reader_plan':'three fresh contexts, one representation, two repair cards only; no earlier answers/key/web','carried_forward_rows':carry,'sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in paths},'root_is_source_exposed':True}
manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/exposure-log.jsonl').open('a') as f:f.write(json.dumps({'at_utc':ts,'actor':'/root','action':'freeze v4 repair cards before new reader assignment; 48 unchanged rows carried forward by hash','files':paths,'sha256':m['sha256']},ensure_ascii=False)+'\n')
print(json.dumps({'v4_frozen':ts,'carry_forward_rows':len(carry),'repair_cases':m['repair_cases']},ensure_ascii=False))
