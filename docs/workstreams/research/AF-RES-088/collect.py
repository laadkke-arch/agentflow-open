"""Bounded public Stack Exchange collection; no auth, answers withheld in frame/R0.

All paths are relative to this research bundle. Raw revision responses may contain
R1, but r0_packet emits only earliest body plus metadata. Fetch != semantic read.
"""
import argparse
import csv
import gzip
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

P = Path(__file__).resolve().parent
API = 'https://api.stackexchange.com/2.3/'
START, END = 1711929600, 1719791999
REV_FILTER = '!6X_1Q338)I5q6Nn_'


def utc(t=None):
    return datetime.fromtimestamp(t, timezone.utc).isoformat().replace('+00:00', 'Z') if t is not None else datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def digest(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def append(name, obj):
    with (P / name).open('a') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def read_json(path):
    path = Path(path)
    if path.exists():
        return json.loads(path.read_text())
    return json.loads(gzip.decompress(Path(str(path)+'.gz').read_bytes()))


def get(path, params, dest):
    dest = P / dest
    url = API + path + '?' + urllib.parse.urlencode(params)
    if dest.exists() or Path(str(dest)+'.gz').exists():
        return read_json(dest)
    stamp = utc()
    try:
        with urllib.request.urlopen(url, timeout=50) as r:
            b = r.read()
            status = r.status
        obj = json.loads(b)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b)
        append('access.jsonl', dict(url=url, fetched_utc=stamp, status=status, path=str(dest.relative_to(P)), sha256=digest(b), bytes=len(b), semantic_read=False))
        if obj.get('error_id'):
            raise RuntimeError(str({k: v for k, v in obj.items() if k.startswith('error')}))
        if obj.get('backoff'):
            if obj['backoff'] > 55:
                raise RuntimeError('API backoff exceeds one bounded wait; resume after ' + str(obj['backoff']) + ' seconds')
            time.sleep(obj['backoff'])
        return obj
    except Exception as e:
        append('attempts.jsonl', dict(url=url, attempted_utc=stamp, error=type(e).__name__ + ': ' + str(e), affected=str(dest.relative_to(P)), counted_as_source=False))
        raise


def frame():
    inc = '.items;.has_more;.backoff;.quota_remaining;.error_id;.error_message;question.question_id;question.creation_date;question.title;question.tags;question.link;question.owner;shallow_user.user_id;shallow_user.display_name;shallow_user.link;shallow_user.user_type'
    filt = get('filters/create', dict(base='none', include=inc), 'raw/question_filter.json')['items'][0]['filter']
    allrows = []
    for tag in ['jq', 'pandoc']:
        data = get('questions', dict(site='stackoverflow', tagged=tag, sort='creation', order='asc', fromdate=START, todate=END, pagesize=30, page=1, filter=filt), f'raw/frame_{tag}_page1.json')
        items = list(data.get('items', []))
        # A boundary tie must not silently drop a lower question_id on page 2.
        if len(items) == 30 and data.get('has_more'):
            second = get('questions', dict(site='stackoverflow', tagged=tag, sort='creation', order='asc', fromdate=START, todate=END, pagesize=30, page=2, filter=filt), f'raw/frame_{tag}_page2_boundary.json')
            edge = items[-1]['creation_date']
            items += [x for x in second.get('items', []) if x['creation_date'] == edge]
        items = sorted(items, key=lambda x: (x['creation_date'], x['question_id']))[:30]
        for n, x in enumerate(items, 1):
            allrows.append(dict(tag=tag, original_rank=n, **x))
        print(tag, 'items', len(items), 'page1_has_more', data.get('has_more'), 'first/last_id', [items[0]['question_id'], items[-1]['question_id']] if items else [])
    (P / 'frame_metadata.json').write_text(json.dumps(allrows, ensure_ascii=False, indent=2) + '\n')


def revisions():
    rows = json.loads((P / 'frame_metadata.json').read_text())
    for tag in ['jq', 'pandoc']:
        qs = [x for x in rows if x['tag'] == tag]
        ids = ';'.join(str(x['question_id']) for x in qs)
        if not ids:
            continue
        page = 1
        while True:
            obj = get(f'posts/{ids}/revisions', dict(site='stackoverflow', pagesize=100, page=page, filter=REV_FILTER), f'sealed/revisions_{tag}_page{page}.json')
            print(tag, 'revision_page', page, 'items', len(obj.get('items', [])), 'has_more', obj.get('has_more'), flush=True)
            if not obj.get('has_more'):
                break
            page += 1
            if page > 20:
                raise RuntimeError('Unexpected history size; preserve partial and inspect pagination')


def load_revisions():
    allitems = []
    for f in sorted((P / 'sealed').glob('revisions_*_page*.json*')):
        data=json.loads(gzip.decompress(f.read_bytes())) if f.suffix=='.gz' else json.loads(f.read_text())
        allitems += data.get('items', [])
    grouped = {}
    for r in allitems:
        key = (r['post_id'], r['revision_guid'], r.get('revision_number'), r.get('creation_date'), digest(json.dumps(r, sort_keys=True)))
        grouped[key] = r
    return list(grouped.values())


def r0_packet():
    rows = json.loads((P / 'frame_metadata.json').read_text())
    revs = load_revisions()
    packets = []
    for q in rows:
        rr = sorted([r for r in revs if r['post_id'] == q['question_id']], key=lambda r: (r['creation_date'], r.get('revision_number', 0), r['revision_guid']))
        bodies = [r for r in rr if 'body' in r]
        r0 = bodies[0] if bodies else None
        meta = [{k: v for k, v in r.items() if k not in ('body', 'last_body', 'title', 'last_title', 'tags', 'last_tags', 'comment')} | {'has_body': 'body' in r, 'has_last_body': 'last_body' in r, 'has_title': 'title' in r, 'has_tags': 'tags' in r} for r in rr]
        edits = [r for r in bodies[1:] if r['creation_date'] <= q['creation_date'] + 30 * 86400]
        packet = dict(tag=q['tag'], original_rank=q['original_rank'], question_id=q['question_id'], created_utc=utc(q['creation_date']), owner=q.get('owner'), current_tags=q.get('tags'), r0=r0, history_metadata=meta, separate_body_edits_30d=len(edits), history_records=len(rr), r0_missing=not bool(r0), current_title_withheld=True, answers_withheld=True)
        packets.append(packet)
    (P / 'r0_packet.json').write_text(json.dumps(packets, ensure_ascii=False, indent=2) + '\n')
    print('R0 packet count', len(packets), 'R1/answers not printed')


if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    arg.add_argument('stage', choices=['frame', 'revisions', 'r0'])
    a = arg.parse_args()
    {'frame': frame, 'revisions': revisions, 'r0': r0_packet}[a.stage]()
