"""Normalize research observations; raw stream files preserve original wording."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sources = {row['source_id']: row for row in map(json.loads, (ROOT/'sources.jsonl').read_text().splitlines())}

def read(rel):
    path = ROOT/rel
    return json.loads(path.read_text()) if path.suffix == '.json' else list(csv.DictReader(path.open()))

def value(row, *keys, default='미확인'):
    for key in keys:
        if key in row and row[key] not in ('', None, []):
            v = row[key]
            return ';'.join(map(str, v)) if isinstance(v, list) else str(v)
    return default

def refs(row):
    explicit = value(row, 'source_ids', 'evidence_ids', default='')
    text = json.dumps(row, ensure_ascii=False)
    found = set(re.findall(r'(?:B0[13]-[PL]\d{3}|ROOT-R\d{3}|ED\d{3})', explicit + ' ' + text))
    if 'ED001–ED026' in text:
        found.update('ED%03d' % i for i in range(1, 27))
    for sid, source in sources.items():
        if source['original_url'] in text:
            found.add(sid)
    return sorted(sid for sid in found if sid in sources)

def source_links(ids):
    return ';'.join(dict.fromkeys(sources[s]['original_url'] for s in ids)) or '미확인'

tables = {}
frame = []
for stream, name in [('root','frame.csv'), ('pdftex','frame.csv'), ('lilypond','frame.json'), ('editions','frame.csv')]:
    rel = f'streams/{stream}/{name}'
    for i, row in enumerate(read(rel), 2):
        ids = refs(row)
        frame.append(dict(frame_id=value(row,'frame_id'), case_id=value(row,'case_id',default='B01'),
            feature=value(row,'feature','function'), baseline=value(row,'baseline'),
            donor_candidate=value(row,'candidate','original_candidate'), query_or_route=value(row,'query_or_route','query','search_or_url','query_or_entry'),
            catalogue=value(row,'catalogue_or_service','catalog','catalog_or_publisher'), search_utc_or_date=value(row,'search_date','search_utc'),
            opened_url=value(row,'opened_url','url',default=source_links(ids)), observed_result=value(row,'observed_result','result','status','access_result'),
            exclusion_or_failure=value(row,'exclusion_or_failure','excluded','exclusion_or_limit','decision_or_exclusion'),
            next_first_source=value(row,'next_first_source',default='해당 없음: 이 경로의 후속은 원장 limitation과 SELF_CHECK.md 참조'),
            source_ids=';'.join(ids) or '미확인', raw_record=f'{rel}:{i}'))
tables['frame'] = frame

chronology = []
for stream,name in [('pdftex','chronology.csv'),('lilypond','chronology.json'),('editions','chronology.csv')]:
    rel=f'streams/{stream}/{name}'
    for i,row in enumerate(read(rel),2):
        ids=refs(row)
        dates=[sources[s]['checked_utc'] for s in ids]
        chronology.append(dict(event_id=value(row,'event_id'),case_id=value(row,'case_id'),
            work=value(row,'work','work_edition'),edition=value(row,'edition','version',default=value(row,'work_edition')),
            date_start=value(row,'date_start'),date_end=value(row,'date_end'),
            date_precision=value(row,'date_precision',default='원문 표기 정밀도; 최초 공개와 mtime 구분'),
            actor=value(row,'actor'),event_type=value(row,'event_type'),
            verified_event=value(row,'verified_event','event','fact'),source_ids=';'.join(ids),
            locator=value(row,'locator',default=';'.join(sources[s]['locator'] for s in ids)),
            source_urls=source_links(ids),alternative_explanation=value(row,'alternative_explanation'),
            author_exposure_date=value(row,'author_exposure_date'),
            researcher_checked_utc=';'.join(dict.fromkeys(dates)) or '미확인',
            ordering_rule='같은 날짜 행의 순서는 인과 순서가 아님; 원문이 제시한 버전 선후만 사용',raw_record=f'{rel}:{i}'))
tables['chronology']=chronology

mechanisms=[]
for stream,name in [('pdftex','mechanisms.csv'),('lilypond','mechanisms.json'),('editions','mechanisms.csv')]:
    rel=f'streams/{stream}/{name}'
    for i,row in enumerate(read(rel),2):
        ids=refs(row)
        mechanisms.append(dict(mechanism_id=value(row,'mechanism_id'),case_id=value(row,'case_id',default='B01'),
            feature=value(row,'feature','function','donor_candidate'),baseline=value(row,'baseline',default='원문·수신 위치에 명시한 기능별 비교'),
            donor_locator=value(row,'donor_locator','original_source_locator'),recipient_locator=value(row,'recipient_locator','recipient_source_locator'),
            input=value(row,'input',default='기능 및 보존값에 명시; 추가 입력은 미확인'),
            preserved_values=value(row,'preserved_values','preserved_value'),changed_values=value(row,'changed_values','changed_value'),
            match=value(row,'match','agreement'),difference=value(row,'difference','difference_or_failure'),
            verification_scope=value(row,'verification_scope'),failure_condition=value(row,'failure_condition','difference_or_failure'),
            source_ids=';'.join(ids),source_urls=source_links(ids),
            interpretation_level=value(row,'interpretation_level',default='직접 코드/문헌 관측과 연구자 해석; verification_scope 참조'),raw_record=f'{rel}:{i}'))
tables['mechanisms']=mechanisms

existing=ROOT/'evidence/table-data.json'
if existing.exists():
    old=json.loads(existing.read_text())
    if 'judgments' in old: tables['judgments']=old['judgments']
existing.write_text(json.dumps(tables,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({name:len(rows) for name,rows in tables.items()}))
