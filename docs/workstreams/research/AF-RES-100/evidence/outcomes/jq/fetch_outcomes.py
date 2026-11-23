"""Post-seal Stack Overflow attribution, authorized after seal2 5d81bcb.
Full external bodies are temporary cache only. No user commands are executed.
"""
import datetime, hashlib, json, pathlib, time, urllib.parse, urllib.request
P = pathlib.Path(__file__).resolve().parent
C = P / '_cache'
C.mkdir(parents=True, exist_ok=True)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts = []

def get(label, url):
    started = now()
    try:
        with urllib.request.urlopen(url, timeout=45) as response:
            raw = response.read()
            status = response.status
        data = json.loads(raw)
        (C / (label + '.json')).write_bytes(raw)
        receipts.append({'label': label, 'url': url, 'checked_utc': started,
                         'finished_utc': now(), 'status': status,
                         'transport_sha256': hashlib.sha256(raw).hexdigest(),
                         'bytes': len(raw), 'has_more': data.get('has_more'),
                         'quota_remaining': data.get('quota_remaining'), 'backoff': data.get('backoff')})
    except Exception as exc:
        receipts.append({'label': label, 'url': url, 'checked_utc': started, 'error': str(exc)})
        (P / 'fetch-receipts.json').write_text(json.dumps(receipts, indent=2))
        raise
    (P / 'fetch-receipts.json').write_text(json.dumps(receipts, indent=2))
    delay = data.get('backoff', 0)
    while delay:
        amount = min(delay, 45)
        time.sleep(amount)
        delay -= amount
    return data

def pages(label, endpoint, flt, **extra):
    items = []
    page = 1
    while True:
        query = dict(site='stackoverflow', pagesize=100, page=page, filter=flt, **extra)
        url = 'https://api.stackexchange.com/2.3/' + endpoint + '?' + urllib.parse.urlencode(query)
        data = get(label + '-' + str(page), url)
        items.extend(data.get('items', []))
        if not data.get('has_more'):
            break
        page += 1
    (C / (label + '-items.json')).write_text(json.dumps(items, ensure_ascii=False, indent=2))
    return items

fields = ['.items', '.has_more', '.quota_remaining', '.backoff',
          'question.question_id', 'question.creation_date', 'question.last_edit_date',
          'question.last_activity_date', 'question.title', 'question.body', 'question.link',
          'question.owner', 'question.accepted_answer_id',
          'answer.answer_id', 'answer.question_id', 'answer.creation_date', 'answer.last_edit_date',
          'answer.last_activity_date', 'answer.body', 'answer.owner', 'answer.is_accepted',
          'comment.comment_id', 'comment.post_id', 'comment.creation_date', 'comment.body',
          'comment.link', 'comment.owner', 'comment.reply_to_user',
          'revision.body', 'revision.creation_date', 'revision.revision_guid',
          'revision.revision_number', 'revision.revision_type', 'revision.post_id',
          'revision.title', 'revision.user',
          'shallow_user.user_id', 'shallow_user.display_name', 'shallow_user.user_type']
created = get('filter', 'https://api.stackexchange.com/2.3/filters/create?' +
              urllib.parse.urlencode({'include': ';'.join(fields), 'base': 'none', 'unsafe': 'true'}))
flt = created['items'][0]['filter']
(P / 'filter.json').write_text(json.dumps(created['items'][0], indent=2))
qids = [79694539, 79699191, 79711268, 79727040]
qidstr = ';'.join(map(str, qids))
questions = pages('questions', 'questions/' + qidstr, flt)
answers = pages('answers', 'questions/' + qidstr + '/answers', flt, order='asc', sort='creation')
posts = qids + [a['answer_id'] for a in answers]
revisions = pages('revisions', 'posts/' + ';'.join(map(str, posts)) + '/revisions', flt)
comments = pages('comments', 'posts/' + ';'.join(map(str, posts)) + '/comments', flt, order='asc', sort='creation')
print(json.dumps({'seal2_sha': '5d81bcbeb5f1248fc1dd2ce2d825cf6467353673',
    'questions': len(questions), 'answers': len(answers), 'revisions': len(revisions),
    'comments': len(comments), 'first_outcome_access_utc': receipts[1]['checked_utc']}, indent=2))
