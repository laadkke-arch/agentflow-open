"""Small, read-only HTTP receipt helper. Full payloads stay outside the repository."""
import hashlib
import json
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = pathlib.Path('/tmp/af098-root')

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.history = []
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.history.append({'from': req.full_url, 'status': code, 'to': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(sid, url, group='matplotlib', timeout=45):
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = ROOT / 'evidence' / group / 'receipts'
    dest.mkdir(parents=True, exist_ok=True)
    handler = Redirects()
    record = {'id': sid, 'requested_url': url, 'utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-098 research/1.0'})
        with urllib.request.build_opener(handler).open(request, timeout=timeout) as response:
            data = response.read()
            record.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type'),
                          bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                          redirects=handler.history)
            (CACHE / sid).write_bytes(data)
    except Exception as error:
        data = None
        record.update(error=type(error).__name__ + ': ' + str(error), redirects=handler.history)
    (dest / (sid + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    return data, record

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('id')
    parser.add_argument('url')
    parser.add_argument('--group', default='matplotlib')
    args = parser.parse_args()
    _, receipt = fetch(args.id, args.url, args.group)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
