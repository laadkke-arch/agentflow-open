"""Join immutable collection ledgers; retain versions without double-counting works.

This does not fetch sources, change eligibility, or infer positive judgments.
Run after recipient collection is frozen. LF CSV is repository policy.
"""
import argparse
import csv
import json
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def first(d, *keys, default=None):
    for key in keys:
        if d.get(key) is not None:
            return d[key]
    return default


def jl(path, data):
    path.write_text(''.join(json.dumps(d, ensure_ascii=False, sort_keys=True) + '\n' for d in data))


def normalize_source(d, category, origin):
    out = dict(d)
    out['source_id'] = d['source_id']
    out['kind'] = first(d, 'kind', 'source_type', default=category)
    out['publisher'] = first(d, 'publisher', 'issuer', 'repository', default='unverified')
    out['original_url'] = first(d, 'original_url', 'url')
    out['fixed_url'] = first(d, 'fixed_url', 'immutable_url', 'blob_url')
    if not out['fixed_url'] and d.get('url_fixity') not in {'current_mutable_url'}:
        out['fixed_url_status'] = 'No stronger immutability asserted; version/hash fields identify the capture.'
    out['publication_date'] = first(d, 'publication_date', 'publication_or_version_date', 'created_at')
    out['version'] = first(d, 'version', 'version_note', 'version_provenance', default='See captured source metadata and hashes.')
    out['checked_utc'] = first(d, 'checked_utc', 'read_at_utc', 'retrieved_at', 'retrieved_at_utc', 'checked_at_utc')
    out['read_location'] = first(d, 'read_location', 'read_locations', 'read_notes', 'read_line_range', default='See original collection record.')
    out['observed'] = first(d, 'observed', 'verified_content', 'neutral_procedural_summary', 'neutral_summary', 'source_observation', 'read_notes', default='See original collection record.')
    out['limitations'] = first(d, 'limitations', 'limit', 'initiality_limits', default=['No stronger inference than the cited read scope.'])
    out['supports'] = first(d, 'supports', 'question_ids', default={'candidate':['Q2','Q3','Q4','Q5'], 'recipient':['Q1','Q3','Q4'], 'field':['Q6','Q7']}[category])
    out['duplicate_group'] = first(d, 'duplicate_group', default=d['source_id'])
    out['counted_minimum'] = bool(d.get('counted_minimum', False))
    out['minimum_category'] = category if out['counted_minimum'] else None
    out['read_status'] = first(d, 'read_status', default='content_verified' if out['counted_minimum'] else 'opened_excluded_or_auxiliary')
    out['collection_record'] = origin
    out['aliases'] = list(d.get('aliases', []))
    return out


def sources():
    donor = rows(ROOT/'donor/donor_sources.jsonl')
    by_id = {}
    for i, d in enumerate(donor, 1):
        if d.get('same_work_selected_source_id'):
            continue
        r = normalize_source(d, 'candidate', f'donor/donor_sources.jsonl:{i}')
        by_id[r['source_id']] = r
    for i, d in enumerate(donor, 1):
        parent = d.get('same_work_selected_source_id')
        if parent:
            assert parent in by_id
            by_id[parent]['aliases'].append(d['source_id'])
            by_id[parent].setdefault('linked_version_records', []).append({'collection_record':f'donor/donor_sources.jsonl:{i}', **d})
    for name, category in [('field/field_sources.jsonl','field'), ('recipient/recipient_sources.jsonl','recipient')]:
        for i,d in enumerate(rows(ROOT/name), 1):
            r = normalize_source(d, category, f'{name}:{i}')
            assert r['source_id'] not in by_id, r['source_id']
            by_id[r['source_id']] = r
    targets={d['recipient_id']:d for d in rows(ROOT/'recipient/recipient_targets.jsonl')}
    for r in by_id.values():
        if r.get('recipient_id') in targets:
            t=targets[r['recipient_id']]
            r['title']=t['title_from_original']
            r['kind']='initial_recipient_proposal'
            r['version']='PR opening snapshot at '+t['original_source']['snapshot_commit_sha']
        if r.get('read_status')=='restored_not_read':
            r['supports']=['Q1-provenance-only']
            r['observed']='Original bytes restored and hashed; no substantive body reading or semantic claim.'
            r['read_location']='No substantive section read; restoration metadata only.'
    data = sorted(by_id.values(), key=lambda r:r['source_id'])
    assert len({r['duplicate_group'] for r in data if r['counted_minimum']}) == sum(r['counted_minimum'] for r in data)
    jl(ROOT/'sources.jsonl',data)
    print(json.dumps({'source_rows':len(data),'counted':dict(Counter(r['minimum_category'] for r in data if r['counted_minimum']))}))


def attempts():
    files = [
        ('donor/donor_attempts.jsonl','D'),
        ('recipient/recipient_attempts.jsonl','R'),
        ('field/field_fetch_attempts.jsonl','FD'),
        ('field/field_web_attempts.jsonl','FW'),
        ('evidence/root_attempts.jsonl','ROOT'),
        ('evidence/opening-archive-attempts.jsonl','AR0'),
        ('evidence/archive-recovery-attempts.jsonl','AR1'),
        ('evidence/prefix-archive-attempts.jsonl','AR2'),
        ('recipient/outcome_attempts.jsonl','OUT'),
    ]
    result=[]
    for name,prefix in files:
        path=ROOT/name
        if not path.exists():
            continue
        for i,d in enumerate(rows(path),1):
            result.append({'attempt_id':f'{prefix}-{i:04d}', 'collection_record':f'{name}:{i}',
                           'original_attempt_id':d.get('attempt_id'),
                           'event_kind':first(d,'kind','stage','event','method',default='see_record'),
                           'checked_utc':first(d,'checked_utc','retrieved_at_utc','retrieved_at','started_utc','recorded_utc','recorded_at'),
                           'record':d})
    jl(ROOT/'attempts.jsonl',result)
    print(json.dumps({'attempt_records':len(result),'note':'Records include metadata screening/dispositions; this is not a network-request count.'}))


def frame():
    result=[]
    with (ROOT/'recipient/recipient_frame.csv').open() as f:
        for i,d in enumerate(csv.DictReader(f),1):
            result.append({'frame_id':f'RF-{i:04d}','record_type':'recipient_pr',
                           'source_ledger':'recipient/recipient_frame.csv',**d})
    with (ROOT/'donor/donor_frame.csv').open() as f:
        for i,d in enumerate(csv.DictReader(f),1):
            result.append({'frame_id':f'DI-{i:03d}','record_type':'provider_issuer',
                           'source_ledger':'donor/donor_frame.csv',**d})
    known={}
    for d in rows(ROOT/'donor/donor_sources.jsonl'):
        for key in ['url','final_url']:
            if d.get(key):known[d[key]]=d
    attempt_by_url={}
    for a in rows(ROOT/'donor/donor_attempts.jsonl'):
        for k in ['url','candidate_url','requested_url']:
            if a.get(k):attempt_by_url[a[k]]=a
    manifests=['libraries_1_candidate_manifest.jsonl','libraries_2_stats_1_candidate_manifest.jsonl',
               'library_directory_manifest.jsonl','statistics_2_candidate_manifest.jsonl','transit_candidate_manifest.jsonl']
    n=0
    for name in manifests:
        for j,d in enumerate(rows(ROOT/'donor'/name),1):
            candidates=d.get('candidates',[])
            ordered=sorted(candidates,key=lambda c:(' '.join(unicodedata.normalize('NFKC',c.get('title','')).split()).lower(),c.get('url','')))
            for order,c in enumerate(ordered,1):
                n+=1;url=c.get('url','');s=known.get(url,{});a=attempt_by_url.get(url,{})
                result.append({'frame_id':f'DC-{n:04d}','record_type':'provider_discovery_candidate',
                    'source_ledger':f'donor/{name}:{j}', 'issuer':d.get('issuer',''),
                    'field':d.get('field',{'LIB':'library','STAT':'statistics'}.get(d.get('document_slot','').split('-')[0],'')),
                    'stage':first(d,'stage','search_stage',default='initial'),
                    'selection_order':c.get('selection_order',order),'title':c.get('title',''),
                    'original_url':url,'source_id':s.get('same_work_selected_source_id',s.get('source_id','')),
                    'alias_source_id':s.get('source_id','') if s.get('same_work_selected_source_id') else '',
                    'status':first(s,'selection_status',default=('selected' if s.get('counted_minimum') else a.get('status','discovered_only_no_individual_disposition'))),
                    'exclusion_reason':first(s,'exclusion_reason',default=first(a,'exclusion_reason','reason',default='')),
                    'evidence_note':json.dumps({'candidate':c,'disposition':a},ensure_ascii=False,sort_keys=True)})
    fields=['frame_id','record_type','source_ledger']+sorted({k for d in result for k in d}-{'frame_id','record_type','source_ledger'})
    with (ROOT/'frame.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(result)
    print(json.dumps({'frame_rows':len(result),'record_types':dict(Counter(r['record_type'] for r in result))}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',action='store_true');p.add_argument('--attempts',action='store_true');p.add_argument('--frame',action='store_true');a=p.parse_args()
    if a.sources:sources()
    if a.attempts:attempts()
    if a.frame:frame()
