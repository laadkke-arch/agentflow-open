"""Read public originals; log transport only, never equate fetching with reading."""
import argparse, hashlib, json, pathlib, subprocess, urllib.request
from datetime import datetime, timezone

BASE = pathlib.Path(__file__).resolve().parents[1]
def main():
    p = argparse.ArgumentParser()
    p.add_argument('source_id')
    p.add_argument('url')
    p.add_argument('--filename')
    args = p.parse_args()
    target = BASE / 'streams/root/tmp' / (args.filename or args.source_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    rec = {'attempt_id': args.source_id, 'url': args.url, 'started_utc': datetime.now(timezone.utc).isoformat(), 'method': 'ordinary public HTTP GET', 'read_status': 'download_only'}
    try:
        request = urllib.request.Request(args.url, headers={'User-Agent': 'Mozilla/5.0 (research document retrieval)'})
        with urllib.request.urlopen(request, timeout=25) as r:
            content = r.read(30_000_000)
            rec.update(status=r.status, final_url=r.url, content_type=r.headers.get('Content-Type'), bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        target.write_bytes(content)
        if content.startswith(b'%PDF'):
            result = subprocess.run(['pdftotext', '-layout', str(target), str(target.with_suffix('.txt'))],capture_output=True,text=True)
            rec['text_extraction_exit'] = result.returncode
        rec['local_temporary_path'] = target.relative_to(BASE).as_posix()
    except Exception as e:
        rec.update(status='failed', error=type(e).__name__+': '+str(e))
    rec['finished_utc'] = datetime.now(timezone.utc).isoformat()
    log = BASE / 'streams/root/attempts-http.jsonl'
    with log.open('a',encoding='utf-8') as f:
        f.write(json.dumps(rec,ensure_ascii=False)+'\n')
    print(json.dumps(rec,ensure_ascii=False))
if __name__ == '__main__':
    main()
