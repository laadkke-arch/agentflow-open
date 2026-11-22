"""Normalize the frozen collectors; no network calls or writes outside owned_path."""
from pathlib import Path
import csv
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
CORE = ['MB01','MB02','MB03','MB04','MB05','MB06','ROR01','ROR02','ROR05','ROR06','ROR07','ROR08','SW01','SW02','SW03','SW05','SW06','WD01']
EVENT_SOURCES = {'MB-S37','MB-S10','MB-S12','MB-S17','MB-S21','MB-S22','ROR-S03','ROR-S09','ROR-S17','ROR-S23','ROR-S30','ROR-S38','SW-S01','SW-S04','SW-S07','SW-S11','SW-S14','WD-S05'}
POLICY_SOURCES = {'MB-S01','MB-S02','MB-S03','MB-S04','ROR-S01','ROR-S02','SW-S17','SW-S18','SW-S19','WD-S01','WD-S02','WD-S03'}
CONSUMER_SOURCES = {'MB-S23','ROR-S08','ROR-S20','ROR-S33','ROR-S34','SW-S20','SW-S21','WD-S07'}
INDEPENDENT_EXTERNAL_CONSUMERS = {'MB-C01','ROR-C01','ROR-C02','ROR-C03','ROR-C04','SW-D01','SW-D02'}

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def string(x):
    return x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)

def first(x, keys, default='미확인'):
    return next((x[k] for k in keys if k in x), default)

sources, events, citations = [], [], []
for collector in ['musicbrainz','ror','software','wikidata']:
    p = ROOT/'collectors'/collector
    for s in json.loads((p/'sources.json').read_text()):
        s['collector'] = collector
        s['collector_counted'] = s.get('counted', False)
        s['minimum_counted'] = s['id'] in EVENT_SOURCES | POLICY_SOURCES | CONSUMER_SOURCES
        s['minimum_category'] = ('event' if s['id'] in EVENT_SOURCES else 'policy' if s['id'] in POLICY_SOURCES else 'downstream' if s['id'] in CONSUMER_SOURCES else None)
        s['counted'] = s['minimum_counted']
        s['counting_rule'] = '최소수 보수산입: 사건은 대표 원문 1건, 정책은 고유 저작, 소비자는 별도 인용 원장 1건. 나머지 전후판·댓글은 같은 주장 계보를 보강하되 수를 늘리지 않는다.'
        s.setdefault('assertion_type', '확인 내용은 기록 관측/저자 진술의 자기말 요약; 연구 해석은 사건 및 RESULT에 별도 표기')
        s.setdefault('directly_opened', s.get('collector_counted',False) or collector in ['ror','software','wikidata'])
        if s['id'] in {'MB-S34','MB-S35','MB-S36','MB-S42','MB-S43','MB-S44','MB-S45'}:
            s['directly_opened'] = False
        if s['id'] == 'SW-S22':
            s['limits'] += ' root 재열람: issue33은 분리 후 이름을 추측한 사례이며 분리 전 저장한 옛 링크의 불변판은 아니다. 엄격한 옛 인용 최소수에서는 제외한다.'
        if s['id'] == 'WD-S07':
            s['independence_note'] = '별도 소비자 항목이나 같은 Wikidata 생산자. 외부기관 독립 소비자 수에서는 제외.'
        sources.append(s)
    for line in (p/'events.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        e['collector'] = collector
        e['primary_sample'] = e['event_id'] in CORE
        e['counted'] = e['primary_sample']
        e['automatic_restoration_execution_verified'] = False
        e['restoration_reading_rule'] = 'AUTO/auto는 표시된 기록에서 기계적으로 추출할 수 있다는 수집자 해석이다. 자동 복원 실행·전체 인용 이관 성공이 아니다. 접근 실패와 실제 손실은 구별한다.'
        events.append(e)
    for c in json.loads((p/'citations.json').read_text()):
        c['collector'] = collector
        citations.append(c)

for s in json.loads((ROOT/'collectors/ror/supplement-sources.json').read_text()):
    s.update(collector='ror', minimum_counted=False, minimum_category=None, counted=False)
    sources.append(s)
fork = json.loads((ROOT/'collectors/software/fork-supplement.json').read_text())
for s in fork['sources']:
    s.update(collector='software', minimum_counted=False, minimum_category=None, counted=False, directly_opened=True)
    sources.append(s)

events.sort(key=lambda e: (e['event_id'] not in CORE, CORE.index(e['event_id']) if e['event_id'] in CORE else e['event_id']))
dump(ROOT/'sources.json', sources)
(ROOT/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
dump(ROOT/'evidence/citations-normalized.json', citations)

fields = ['downstream_id','event_id','primary_case','independent_external_original','url','source_ids','source_version_or_date','contemporaneous_context','old_destination','changed_or_current_destination','followup_date','followup_record','required_function_version','observed_effect','actual_user_misrecommendation','limits','lineage']
rows=[]
for c in citations:
    cid=c['downstream_id']
    follow=first(c,['consumer_followups','consumer_correction','actual_consumer_correction','followup_url'])
    row={
        'downstream_id':cid,'event_id':c.get('event_id') or 'supplement',
        'primary_case':c.get('event_id') in CORE,
        'independent_external_original':cid in INDEPENDENT_EXTERNAL_CONSUMERS,
        'url':first(c,['url','consumer_url']),
        'source_ids':c.get('source_ids',[c.get('source_id')]),
        'source_version_or_date':first(c,['source_version','citation_date','written_or_corrected_at','written_at','first_citation_date']),
        'contemporaneous_context':first(c,['citation_context','original_context','contemporaneous_context']),
        'old_destination':c.get('old_destination','미확인'),
        'changed_or_current_destination':first(c,['corrected_destination','new_destination','then_new_destination','current_destination','changed_destination']),
        'followup_date':first(c,['followup_date','written_or_corrected_at','actual_consumer_followup_date','consumer_followups']),
        'followup_record':follow,
        'required_function_version':first(c,['required_function_version','required_function_or_version']),
        'observed_effect':first(c,['observed_effect','observed_result','observed_impact_kind','actual_consumer_effect']),
        'actual_user_misrecommendation':'미확인',
        'limits':first(c,['limits','inference_limit','observed_limit','user_harm','real_user_misrecommendation']),
        'lineage':first(c,['lineage','relationship_to_original_publisher','independence'])
    }
    if cid == 'SW-D03':
        row['limits'] = '분리 뒤 CLI 누락/판 불일치 보고. 분리 전에 저장한 링크의 불변판은 미확보. 실제 보고와 이번 재현을 구별.'
    if cid == 'WD-C01':
        row['required_function_version'] = '건물 Q314104의 topic main category(P910)를 찾는다. 정정판1048159950의 대상은 category Q55296215이다.'
    rows.append({k:string(v) for k,v in row.items()})
with (ROOT/'citations.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

counts={
    'primary_events':sum(e['primary_sample'] for e in events),
    'events_by_system':dict(Counter(e['collector'] for e in events if e['primary_sample'])),
    'events_by_class':dict(Counter(e['event_class'] for e in events if e['primary_sample'])),
    'source_ledger_rows':len(sources),
    'conservative_unique_originals':sum(s.get('minimum_counted',False) for s in sources),
    'minimum_by_category':dict(Counter(s['minimum_category'] for s in sources if s.get('minimum_counted'))),
    'independent_external_consumer_records':len(INDEPENDENT_EXTERNAL_CONSUMERS),
    'consumer_rows_all_including_supplements':len(rows),
    'consumer_dated_followup_chains':['MB-C01','SW-D01','SW-D02','WD-C01'],
    'unknowns_remain_in_denominator':True,
    'limits':'18는 실제 사건/기각 에피소드 수이며 완전한 전후 ID·정정판 18건을 뜻하지 않는다. ROR 현재 소비자의 작성 시점과 일부 MB 과거 ID가 미확인이다.'
}
dump(ROOT/'evidence/counts.json', counts)
print(json.dumps(counts,ensure_ascii=False,indent=2))
