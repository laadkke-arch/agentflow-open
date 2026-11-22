"""Final pre-reader refinement: keep historical values in II, changes/judgments in III."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
P=Path(__file__).resolve().parents[1]
manifest=P/'evidence/frozen-manifest-v3.json';assert not manifest.exists()
ts=datetime.now(timezone.utc).isoformat()
historical={
 'MB01':'저장에 함께 남긴 과거 근거는 edit131420900·137042427이다. release893fa571-0d95-4a89-a970-a408d1586755, 11-track CD, DiscID QnV3tLQLJjFu6sEFcbSYh5AstG4-, Worldwide/2025가 기록돼 있다. 유럽판 matrix와 원 source ID는 이 저장 표현에 확보하지 못했다.',
 'MB02':'2019-09-04 edit63656996 판의 recording132ded03-02d3-4dc6-b7d8-2d15ff97ec0f 이름은 Les Princes des villes이다. 저장 문맥은 medium3 track1, 5:27이다(공식 recording history).',
 'MB03':'2019-04 edit60587125에 recording2775d583-3c95-4f65-b856-76c5e1db732f는 07, 2:32로 표시된다. release5aeb8c8f-cd6a-4d43-97e5-fb86b9b35695의 B4 표시는 2:38이다. 이 근거에 원 source MBID는 미노출이다.',
 'MB04':'2020 edit68967621에 recording7a3eb993-0b45-4ee3-971a-b385e9e92e11은 Reamonn/Back Again7:34, ISRC DEC640300057 및 DEG120300914로 표시된다. 원 source MBID는 미노출이다.',
 'MB05':'2017년 공식 토론/편집 history에는 da729585-32c9-4261-8a30-322d7d414653 Neththara와633a31aa-ed97-49fc-ab70-27f8e97fc5be Neththara - Project4가 함께 있다. da729585에는 트랙3·8이 없고 artist 표기가 축약되어 있었다.',
 'MB06':'소비자 issue114가2024-12-31 인용한 recording MBID는fa9c940c-408b-41f0-b746-997e50e36d72, AcoustID는b847e16e-d9ed-4aeb-bc4d-cabe7f16a914이다. 당시 인용한 Fingerprints target은958820ff-ec99-4aec-8df3-737d699e796e였다.',
 'ROR02':'2024 issue13495 본문에는 National Center for PTSD 본부04xv0vq46와 Pacific Islands Division01dbbht76가 각각 표시된다. 저장한 소속 단위는division이다. 불변 전체dump의 해당 record는 확보하지 못했다.',
 'SW03':'parent e2f98568822c4f3f9b180b77a2ef10236189e2fa의Formula/gnu-readline.rb는GNU readline6.2.4와sourcearchive를기록한다. 이 고정 recipe 본문은 직접 읽었다.',
 'SW05':'2022 parent b354eba6f430f0da6b5f8e8d24c25c0411fab517의unversioned postgresql recipe는14.5이다. Rails의2024-05-23 Brewfile diff에서 이전 줄은brew postgresql이라는이름을사용했다. 이 표현에는 후속 선택과 사유를 포함하지 않는다.'
}
prepend={
 'MB01':'저장 시점 모델은2026-08병합이후다. ',
 'MB02':'2019 edit63656996은 원 La Groupie du pianiste(CD2/Rhythm mix/4:39) ID의 이름을 Les Princes로 바꾼 사건이다. ',
 'MB04':'서로 다른 Beautiful Sky 두 edition에 중복 recording이 있다는 제안이었다. ',
 'MB06':'merge92853437은2022-09-19 Applied지만 즉시 target MBID는 공개행에 없다. ',
 'ROR02':'본부와division을 같은 조직으로 묶자는 제안이었다. ',
 'SW03':'revert직전의readline은gnu-readline을가리키는alias였다. 원rename adee5315265cc46aa6a3057071527abb16e1cd94객체는접근불가였다. '
}
paths=[]
for i in [1,2,3]:
    x=json.loads((P/f'reconstruction/views/v2-view-{i}.json').read_text())
    x['protocol_version']='v3 final primary: v2 common-observation fixes + strict separation of historical values and change judgments'
    for c in x['cards']:
        eid=c['event_id']
        if i>=2 and eid in historical:c['saved_historical_id_version_and_locator']=historical[eid]
        if i>=3 and eid in prepend:c['saved_relationship_and_effective_history']=prepend[eid]+c['saved_relationship_and_effective_history']
    path=f'reconstruction/views/v3-view-{i}.json';paths.append(path)
    (P/path).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
key='reconstruction/key/answer-key.json';paths.append(key)
m={'created_at_utc':ts,'version':'v3','primary_comparison':True,'reason':'audit moved proposal/change/post-edit rationale from II to III before any new reader assignment','previous_versions':'v1 pilot answered; v2 intermediate fixed common inputs, no readers assigned','key_unchanged':True,'reader_plan':'three fresh fork_turns=none readers, one v3 view each; no prior views/answers/key/web','sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in paths},'root_is_source_exposed':True}
manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/exposure-log.jsonl').open('a') as f:f.write(json.dumps({'at_utc':ts,'actor':'/root','action':'freeze v3 before new reader assignment; v1/v2 and original key preserved','files':paths,'sha256':m['sha256']},ensure_ascii=False)+'\n')
print(json.dumps({'v3_frozen':ts,'files':paths},ensure_ascii=False))
