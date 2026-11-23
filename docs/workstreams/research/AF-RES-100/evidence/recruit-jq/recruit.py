"""AF-RES-100 blinded jq recruitment. Never request answer/comment/vote fields."""
import datetime, hashlib, html, json, pathlib, re, subprocess, time
import urllib.parse, urllib.request

P = pathlib.Path(__file__).resolve().parent
C = P / '_cache'
C.mkdir(exist_ok=True)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts = []

def get(url):
    started = now()
    try:
        with urllib.request.urlopen(url, timeout=45) as response:
            raw = response.read()
            status = response.status
        data = json.loads(raw)
    except Exception as exc:
        receipts.append({'url': url, 'checked_utc': started, 'error': str(exc), 'counted': False})
        (P / 'fetch-receipts.json').write_text(json.dumps(receipts, indent=2), encoding='utf-8')
        raise
    receipt = {'url': url, 'checked_utc': started, 'finished_utc': now(), 'status': status,
               'sha256': hashlib.sha256(raw).hexdigest(), 'has_more': data.get('has_more'),
               'quota_remaining': data.get('quota_remaining'), 'backoff': data.get('backoff')}
    receipts.append(receipt)
    (P / 'fetch-receipts.json').write_text(json.dumps(receipts, indent=2), encoding='utf-8')
    if data.get('backoff'):
        time.sleep(min(data['backoff'], 60))
    return data

def make_filter(fields):
    params = {'include': ';'.join(fields), 'base': 'none', 'unsafe': 'true'}
    data = get('https://api.stackexchange.com/2.3/filters/create?' + urllib.parse.urlencode(params))
    return data['items'][0]['filter'], data['items'][0]['included_fields']

def run(phase):
    # Initial run also requested current question.title; that exposure is retained
    # in metadata-exposure-audit.json. A replay uses ID/origin metadata only.
    qfields = ['.items', '.has_more', '.quota_remaining', '.backoff', 'question.question_id',
               'question.creation_date', 'question.tags', 'question.link']
    qfilter, qincluded = make_filter(qfields)
    rfields = ['.items', '.has_more', '.quota_remaining', '.backoff', 'revision.body',
               'revision.creation_date', 'revision.revision_guid', 'revision.revision_number',
               'revision.revision_type', 'revision.post_id', 'revision.title']
    rfilter, rincluded = make_filter(rfields)
    (P / ('filters-' + phase + '.json')).write_text(json.dumps({'question_filter': qfilter,
       'question_fields': qincluded, 'revision_filter': rfilter, 'revision_fields': rincluded}, indent=2))
    period = ('2025-07-01', '2026-01-01', 60) if phase == 'h2' else ('2026-01-01', '2026-04-01', 30)
    begin, end, limit = period
    epoch = lambda x: int(datetime.datetime.fromisoformat(x).replace(tzinfo=datetime.timezone.utc).timestamp())
    params = {'site': 'stackoverflow', 'tagged': 'jq', 'sort': 'creation', 'order': 'asc',
              'fromdate': epoch(begin), 'todate': epoch(end)-1, 'pagesize': limit, 'filter': qfilter}
    url = 'https://api.stackexchange.com/2.3/questions?' + urllib.parse.urlencode(params)
    data = get(url)
    rows = sorted(data.get('items', []), key=lambda x: (x['creation_date'], x['question_id']))
    (P / ('metadata-' + phase + '.json')).write_text(json.dumps({'url': url, 'items': rows,
         'has_more': data.get('has_more'), 'metadata_fields': qincluded}, ensure_ascii=False, indent=2))
    # All revision bodies are held in memory only. Only the earliest body-bearing
    # revision is saved/displayed; modified question bodies remain blinded.
    revisions = []
    for start in range(0, len(rows), 10):
        ids = ';'.join(str(q['question_id']) for q in rows[start:start+10])
        page = 1
        while True:
            u = 'https://api.stackexchange.com/2.3/posts/' + ids + '/revisions?' + urllib.parse.urlencode(
                {'site': 'stackoverflow', 'pagesize': 100, 'page': page, 'filter': rfilter})
            d = get(u)
            revisions.extend(d.get('items', []))
            if not d.get('has_more'):
                break
            page += 1
    outputs = []
    for rank, q in enumerate(rows, 1):
        candidates = [r for r in revisions if r.get('post_id') == q['question_id'] and 'body' in r]
        candidates.sort(key=lambda r: (r.get('creation_date', 0), r.get('revision_number', 99999), r.get('revision_guid', '')))
        item = dict(q, rank=rank, phase=phase)
        if candidates:
            r = candidates[0]
            item.update(r)
            item['question_creation_date'] = q['creation_date']
            item['r0_is_creation_timestamp'] = r['creation_date'] == q['creation_date']
            item['r0_url'] = 'https://stackoverflow.com/revisions/' + r['revision_guid'] + '/view-source'
            item['body_sha256'] = hashlib.sha256(r['body'].encode()).hexdigest()
            item['body_text'] = html.unescape(re.sub('<[^>]+>', ' ', r['body']))
        else:
            item['missing'] = 'No earliest body-bearing revision returned'
        outputs.append(item)
    (C / ('r0-' + phase + '.json')).write_text(json.dumps(outputs, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'phase': phase, 'count': len(outputs), 'has_more': data.get('has_more'),
        'questions': [{'rank': r['rank'], 'question_id': r['question_id'], 'title': r.get('title'),
                       'r0_url': r.get('r0_url')} for r in outputs]}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else 'h2')
