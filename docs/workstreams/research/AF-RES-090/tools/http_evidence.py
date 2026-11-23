"""Bounded public HTTP evidence; not a browser execution or a source counter."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch(url, source_id, directory, timeout=40):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    start = now()
    redirects = []
    class TrackingRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            redirects.append({'status': code, 'from': req.full_url, 'to': newurl})
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    opener = urllib.request.build_opener(TrackingRedirect)
    error = None
    body = b''
    headers = {}
    final_url = url
    status = None
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-090 public documentation research', 'Accept-Encoding': 'identity'})
        try:
            response = opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            response = e
        with response:
            body = response.read(20_000_001)
            if len(body) > 20_000_000:
                raise ValueError('Response exceeds 20 MB evidence bound')
            headers = dict(response.headers.items())
            final_url = response.geturl()
            status = response.status
    except Exception as e:
        error = f'{type(e).__name__}: {e}'
    redacted_headers = [k for k in headers if k.lower() in {'set-cookie', 'authorization', 'proxy-authorization', 'cookie'}]
    for k in redacted_headers:
        headers[k] = '[omitted: response credential/cookie not research evidence]'
    receipt = {
        'source_id': source_id, 'requested_url': url, 'final_url': final_url,
        'started_utc': start, 'retrieved_utc': now(), 'status': status,
        'content_type': next((v for k,v in headers.items() if k.lower() == 'content-type'), None),
        'body_bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
        'git_blob_sha1': hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(),
        'redirects': redirects, 'headers': headers, 'redacted_headers': redacted_headers, 'error': error,
        'measurement': 'decoded HTTP response entity bytes; excludes headers/TLS; no JS execution',
    }
    (directory / (source_id + '.receipt.json')).write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    cache = directory / 'raw'
    cache.mkdir(exist_ok=True)
    (cache / (source_id + '.bin')).write_bytes(body)
    return receipt, body

def save_excerpt(directory, source_id, observations, excerpts=None):
    """Store only short quoted spans plus analyst observations, not whole webpages."""
    payload = {'source_id': source_id, 'recorded_utc': now(), 'observations': observations, 'short_excerpts': excerpts or []}
    Path(directory, source_id+'.excerpt.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
