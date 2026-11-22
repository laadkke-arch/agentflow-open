"""AF-RES-036 measured public-source reads; all writes remain in owned_path."""
import hashlib
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def append(path, record):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n')

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({'url':req.full_url, 'status':code, 'location':newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(url, directory, attempt_id, role, case_ids=(), save_name=None, timeout=30):
    directory = Path(directory).resolve()
    directory.relative_to(BASE)
    directory.mkdir(parents=True, exist_ok=True)
    handler = Redirects()
    opener = urllib.request.build_opener(handler)
    record = {'attempt_id':attempt_id, 'operation':'GET', 'url':url, 'role':role,
              'case_ids':list(case_ids), 'started_utc':utc(), 'timeout_seconds':timeout,
              'status':None, 'error':None, 'received_body_bytes':0,
              'stored_bytes':0, 'wire_bytes':None, 'measurement':'actual'}
    start = time.monotonic()
    data = b''
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 AF-RES-036 public-document research', 'Accept-Encoding':'identity'})
        with opener.open(req, timeout=timeout) as r:
            data = r.read()
            record.update(status=r.status, final_url=r.url,
                          content_type=r.headers.get('Content-Type'),
                          last_modified=r.headers.get('Last-Modified'),
                          content_encoding=r.headers.get('Content-Encoding'))
    except urllib.error.HTTPError as e:
        data = e.read()
        record.update(status=e.code, final_url=e.url, error=str(e))
    except Exception as e:
        record['error'] = type(e).__name__ + ': ' + str(e)
    record.update(finished_utc=utc(), elapsed_seconds=round(time.monotonic()-start,6),
                  redirect_chain=handler.chain, received_body_bytes=len(data), sha256=sha(data))
    if data and save_name:
        path=directory/save_name
        path.resolve().relative_to(BASE)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        record.update(stored_path=str(path.relative_to(BASE)), stored_bytes=len(data))
    append(directory/'attempts.jsonl',record)
    return data,record
