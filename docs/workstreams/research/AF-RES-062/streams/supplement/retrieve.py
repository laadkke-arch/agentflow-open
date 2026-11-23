"""Public, unauthenticated source retrieval; cache bytes are excluded from git."""
import argparse, hashlib, json, urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
def retrieve(key, url):
    when = datetime.now(timezone.utc).isoformat()
    out = BASE / 'cache' / key
    out.parent.mkdir(parents=True, exist_ok=True)
    row = {'retrieval_id':key, 'url':url, 'started_utc':when, 'actor':'supplement AI via cloud Python urllib', 'read_status':'retrieved_not_yet_read'}
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            b = r.read()
            row.update(status=r.status, final_url=r.url, content_type=r.headers.get('Content-Type'), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
        out.write_bytes(b)
    except Exception as e:
        row.update(status='failed', error=type(e).__name__+': '+str(e))
    row['finished_utc']=datetime.now(timezone.utc).isoformat()
    with (BASE/'retrieval-log.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return row

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('key');p.add_argument('url');a=p.parse_args()
    print(json.dumps(retrieve(a.key,a.url),ensure_ascii=False))
