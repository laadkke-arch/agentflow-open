"""Bounded public-source retrieval; records access, not proof of source truth."""
import datetime
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / '.cache'

def retrieve(url, key, maximum=100_000_000):
    CACHE.mkdir(exist_ok=True)
    (CACHE / '.gitignore').write_text('*\n!.gitignore\n', encoding='utf-8')
    out = {'url': url, 'key': key, 'opened_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'kind': 'retrieval'}
    body = b''
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-063 public historical evidence research', 'Accept': '*/*'})
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read(maximum + 1)
            final = urllib.parse.urlsplit(response.url)
            signed = 'X-Amz-' in final.query or 'Signature=' in final.query
            safe_final = urllib.parse.urlunsplit((final.scheme, final.netloc, final.path, '' if signed else final.query, ''))
            out.update(status=response.status, final_url=safe_final, signed_redirect_query_omitted=signed, content_type=response.headers.get('Content-Type'))
            if len(body) > maximum:
                raise ValueError('response exceeds declared retrieval cap')
        out.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        (CACHE / key).write_bytes(body)
    except urllib.error.HTTPError as exc:
        body = exc.read(8000)
        out.update(status=exc.code, error=str(exc), error_body=body.decode('utf-8', 'replace')[:2000])
    except Exception as exc:
        out.update(status=None, error=type(exc).__name__ + ': ' + str(exc))
    with (ROOT / 'root-access.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(out, ensure_ascii=False) + '\n')
    return out, body

if __name__ == '__main__':
    out, _ = retrieve(sys.argv[1], sys.argv[2])
    print(json.dumps(out, ensure_ascii=False))
