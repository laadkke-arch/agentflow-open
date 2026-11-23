import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import threading
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
LOCK = threading.Lock()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def fetch(url, name):
    started = now()
    before = time.monotonic()
    receipt = {'url': url, 'started_at_utc': started, 'method': 'GET', 'local_file': name}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-077-public-research', 'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            receipt.update(status=response.status, headers=dict(response.headers), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        (ROOT / name).write_bytes(data)
        result = json.loads(data) if name.endswith('.json') else data.decode()
    except Exception as error:
        receipt.update(error=type(error).__name__ + ': ' + str(error))
        result = None
    receipt.update(completed_at_utc=now(), elapsed_seconds=round(time.monotonic()-before, 3))
    with LOCK:
        with (ROOT / 'http_calls.jsonl').open('a') as stream:
            stream.write(json.dumps(receipt) + '\n')
    return result

def main():
    queries = ['repo:mltframework/shotcut proxy created:2019-01-01..2025-12-31', 'repo:mltframework/shotcut relink created:2019-01-01..2025-12-31']
    receipts = []
    for name, query in zip(['proxy', 'relink'], queries):
        params = {'q': query, 'sort': 'created', 'order': 'asc', 'per_page': 10, 'page': 1}
        url = 'https://api.github.com/search/issues?' + urllib.parse.urlencode(params)
        result = fetch(url, 'raw_query_' + name + '.json')
        receipts.append({'query': query, 'parameters': params, 'url': url, 'original_order': [item['number'] for item in result['items']] if result else None, 'total_count': result.get('total_count') if result else None, 'incomplete_results': result.get('incomplete_results') if result else None})
    (ROOT / 'raw_query_receipt.json').write_text(json.dumps({'retrieved_at_utc': now(), 'queries': receipts}, indent=2)+'\n')
    numbers = sorted(set(number for row in receipts for number in (row['original_order'] or [])))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        values = list(executor.map(lambda number: fetch('https://api.github.com/repos/mltframework/shotcut/issues/' + str(number), 'issue_' + str(number) + '.json'), numbers))
    issues = [x for x in values if x]
    issues.sort(key=lambda x: (x['created_at'], x['number']))
    candidates = [{'union_rank': rank+1, 'number': item['number'], 'url': item['html_url'], 'type': 'pull_request' if item.get('pull_request') else 'issue', 'title': item['title'], 'author': item['user']['login'], 'created_at': item['created_at'], 'updated_at': item['updated_at'], 'body_file': 'issue_'+str(item['number'])+'.json'} for rank, item in enumerate(issues)]
    (ROOT / 'candidates.json').write_text(json.dumps(candidates, indent=2)+'\n')
    print(json.dumps({'query_receipt': receipts, 'candidates': candidates}, indent=2))
    for item in issues[:10]:
        body = item.get('body') or ''
        if item['number'] == 942:
            body = '\n'.join(body.splitlines()[:45]) + '\n[Crash-log body preserved in issue_942.json; later matching relationship terms below]\n' + '\n'.join(line for line in body.splitlines() if any(x in line.lower() for x in ['prox', 'relink', 'original', 'moved', 'folder']))
        print('\nISSUE '+str(item['number'])+' CURRENT BODY\n'+body)

if __name__ == '__main__':
    main()
