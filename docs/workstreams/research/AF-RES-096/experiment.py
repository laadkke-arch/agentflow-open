"""Deterministic file ranking, four-slot exposure, and charged source opening.

rank must be run only after the first remote seal. open/section never consult
unexposed files. Judgments are written by researchers, not generated here.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, re, unicodedata

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def tokens(s):
    return set(re.findall(r'[a-z0-9_]+', unicodedata.normalize('NFKC', s).casefold()))

def read_jsonl(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]

def append(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')

def write_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def rank():
    marker = ROOT / 'evidence/seal1-receipt.json'
    seal = json.loads(marker.read_text())
    assert re.fullmatch('[0-9a-f]{40}', seal['remote_sha'])
    protocol = json.loads((ROOT / 'protocol.json').read_text())
    inventory = read_jsonl(ROOT / 'corpus-files.jsonl')
    # Reusable machine index; contents never printed during construction.
    bodies = {r['file_id']: (ROOT / r['cached_body']).read_text() for r in inventory}
    index = {k: tokens(v) for k, v in bodies.items()}
    log = ROOT / 'evidence/search-events.jsonl'
    if log.exists():
        raise ValueError('Refusing to replace an existing experiment log')
    for case in protocol['cases']:
        for route in case['route_order']:
            allowed = [case['main_label']]
            if route == 'B' and case['adjacent_label']:
                allowed.append(case['adjacent_label'])
            files = [r for r in inventory if r['label'] in allowed]
            merged_tokens = set()
            for qnum, query in enumerate(case['queries'], 1):
                start = now()
                ts = tokens(' '.join(query)); merged_tokens |= ts
                ranked = sorted(files, key=lambda r: (-len(ts & index[r['file_id']]), r['repo']+'/'+r['path']))
                rows = [{'rank': i, 'file_id': r['file_id'],
                         'score': len(ts & index[r['file_id']]),
                         'matched_tokens': sorted(ts & index[r['file_id']])}
                        for i, r in enumerate(ranked, 1)]
                target = ROOT / f'evidence/ranking/{case["case_id"]}-{route}-q{qnum}.jsonl'
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(''.join(json.dumps(r, separators=(',', ':'))+'\n' for r in rows))
                append(log, {'event': 'search', 'case_id': case['case_id'], 'route': route,
                             'query_number': qnum, 'query_tokens': sorted(ts), 'allowed_labels': allowed,
                             'started_utc': start, 'finished_utc': now(), 'charged_searches': 1,
                             'ranked_files': len(rows), 'positive_files': sum(r['score'] > 0 for r in rows),
                             'full_ranking_file': str(target.relative_to(ROOT)),
                             'full_ranking_sha256': digest(target.read_bytes())})
            ranked = sorted(files, key=lambda r: (-len(merged_tokens & index[r['file_id']]), r['repo']+'/'+r['path']))
            all_rows = [{'rank': i, 'file_id': r['file_id'],
                         'score': len(merged_tokens & index[r['file_id']]),
                         'matched_tokens': sorted(merged_tokens & index[r['file_id']])}
                        for i, r in enumerate(ranked, 1)]
            target = ROOT / f'evidence/ranking/{case["case_id"]}-{route}-merged.jsonl'
            target.write_text(''.join(json.dumps(r, separators=(',', ':'))+'\n' for r in all_rows))
            positive = [r for r in ranked if merged_tokens & index[r['file_id']]]
            primary = [r for r in positive if r['label'] == case['main_label']]
            adjacent = [r for r in positive if r['label'] == case['adjacent_label']]
            if route == 'A' or case['stratum'] == 'control':
                chosen = (primary[:4] + [None]*4)[:4]
            else:
                chosen = (primary[:2]+[None]*2)[:2] + (adjacent[:2]+[None]*2)[:2]
            global_ranks = {r['file_id']: r['rank'] for r in all_rows}
            slots = []
            for slot, row in enumerate(chosen, 1):
                if row is None:
                    slots.append({'slot': slot, 'file_id': None, 'empty': True})
                    continue
                body = bodies[row['file_id']]
                mt = sorted(merged_tokens & index[row['file_id']])
                pattern = r'(?<![a-z0-9_])(?:'+'|'.join(re.escape(t) for t in mt)+r')(?![a-z0-9_])'
                m = re.search(pattern, body, flags=re.I)
                offset = max(0, (m.start() if m else 0)-100)
                raw_excerpt = body[offset:offset+600]
                slots.append({'slot': slot, 'file_id': row['file_id'], 'empty': False,
                              'repo': row['repo'], 'path': row['path'], 'url': row['url'],
                              'role': 'main' if row['label'] == case['main_label'] else 'adjacent',
                              'merged_global_rank': global_ranks[row['file_id']],
                              'within_role_rank': (primary if row['label'] == case['main_label'] else adjacent).index(row)+1,
                              'score': len(mt), 'matched_tokens': mt,
                              'excerpt': raw_excerpt.ljust(600), 'excerpt_offset': offset,
                              'anchor_fallback': m is None,
                              'excerpt_source_chars': len(raw_excerpt), 'excerpt_sha256': digest(raw_excerpt.encode()),
                              'body_sha256': row['sha256']})
            exposure = {'event': 'exposure', 'case_id': case['case_id'], 'route': route,
                        'created_utc': now(), 'full_merged_ranking': str(target.relative_to(ROOT)),
                        'full_merged_sha256': digest(target.read_bytes()), 'slots': slots,
                        'route_order': case['route_order'], 'seal1_remote_sha': seal['remote_sha']}
            write_json(ROOT / f'evidence/routes/{case["case_id"]}-{route}/exposure.json', exposure)
            append(log, exposure)
            print(json.dumps({'case_id':case['case_id'],'route':route,'slots':[
                {'slot':r['slot'],'file_id':r['file_id'],'path':r.get('path'),'role':r.get('role')}
                for r in slots]}), flush=True)

def open_next(case_id, route):
    folder = ROOT / f'evidence/routes/{case_id}-{route}'
    exposure = json.loads((folder / 'exposure.json').read_text())
    log = folder / 'access.jsonl'
    prior = read_jsonl(log) if log.exists() else []
    attempts = [r for r in prior if r['event'] == 'body_attempt']
    if len(attempts) >= 4:
        raise ValueError('Body attempt budget exhausted')
    attempted_slots = {r['slot'] for r in attempts}
    slots = [s for s in exposure['slots'] if not s['empty'] and s['slot'] not in attempted_slots]
    if not slots:
        raise ValueError('All exposed files already attempted')
    slot = slots[0]
    row = next(r for r in read_jsonl(ROOT/'corpus-files.jsonl') if r['file_id'] == slot['file_id'])
    event = {'event':'body_attempt','case_id':case_id,'route':route,'slot':slot['slot'],
             'attempt_number':len(attempts)+1,'file_id':row['file_id'],'url':row['url'],
             'role':slot['role'],'started_utc':now(),'charged_attempts':1,
             'source':'frozen local official-source corpus; separate construction cost'}
    try:
        raw = (ROOT/row['cached_body']).read_bytes()
        assert digest(raw) == row['sha256'], 'corpus body changed'
        text = raw.decode('utf-8')
        if not text.strip():
            raise ValueError('empty file')
        target = folder / '_cache' / (row['file_id']+'.txt')
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
        event.update({'status':'success','bytes':len(raw),'body_sha256':digest(raw),
                      'opened_body':str(target.relative_to(ROOT)),'line_count':len(text.splitlines())})
    except Exception as exc:
        event.update({'status':'failed','error':f'{type(exc).__name__}: {exc}'})
    event['finished_utc'] = now()
    append(log,event)
    print(json.dumps(event,ensure_ascii=False,indent=2))

def section(case_id, route, file_id, start, end):
    folder = ROOT / f'evidence/routes/{case_id}-{route}'
    prior = read_jsonl(folder/'access.jsonl')
    ev = next((r for r in prior if r['event']=='body_attempt' and r['file_id']==file_id and r['status']=='success'),None)
    if ev is None:
        raise ValueError('File not opened in this route')
    lines = (ROOT/ev['opened_body']).read_text().splitlines()
    selected = lines[max(0,start-1):min(len(lines),end)]
    event = {'event':'section_navigation','case_id':case_id,'route':route,'file_id':file_id,
             'utc':now(),'start_line':start,'end_line':min(len(lines),end),
             'charged_attempts':0,'already_opened_file':True,
             'section_sha256':digest('\n'.join(selected).encode())}
    append(folder/'access.jsonl',event)
    print('\n'.join(f'{start+i}: {line}' for i,line in enumerate(selected)))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); subs=parser.add_subparsers(dest='cmd',required=True)
    subs.add_parser('rank')
    p=subs.add_parser('open');p.add_argument('case');p.add_argument('route',choices=['A','B'])
    p=subs.add_parser('section');p.add_argument('case');p.add_argument('route',choices=['A','B']);p.add_argument('file_id');p.add_argument('start',type=int);p.add_argument('end',type=int)
    a=parser.parse_args()
    if a.cmd=='rank':rank()
    elif a.cmd=='open':open_next(a.case,a.route)
    else:section(a.case,a.route,a.file_id,a.start,a.end)
