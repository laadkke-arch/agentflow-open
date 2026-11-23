"""Read a public source into ignored local cache and record exact acquisition metadata.
No participant rows or publisher PDF text are included in committed outputs.
"""
import argparse, datetime, hashlib, json, pathlib, subprocess, urllib.request

P = pathlib.Path(__file__).parent

def fetch(source_id, url, suffix):
    out = P / '_cache' / (source_id + suffix)
    d = {'source_id': source_id, 'url': url, 'opened_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (public academic source audit)'})
        with urllib.request.urlopen(req, timeout=35) as r:
            raw = r.read()
            d.update(http_status=r.status, final_url=r.url, content_type=r.headers.get('content-type'), byte_count=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        out.write_bytes(raw)
        if suffix == '.pdf' and raw.startswith(b'%PDF'):
            t = subprocess.run(['pdftotext', '-layout', str(out), str(out.with_suffix('.txt'))], capture_output=True, text=True)
            d['extraction_exit_code'] = t.returncode
        d['cache_path'] = str(out)
        d['acquisition_status'] = 'downloaded; read-status requires explicit analyst locator/notes'
    except Exception as e:
        d.update(acquisition_status='failed', error=str(e))
    with (P / 'retrievals.jsonl').open('a') as f:
        f.write(json.dumps(d, ensure_ascii=False) + '\n')
    print(json.dumps(d, ensure_ascii=False))
    return d

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source_id');parser.add_argument('url');parser.add_argument('suffix')
    a=parser.parse_args();fetch(a.source_id,a.url,a.suffix)
