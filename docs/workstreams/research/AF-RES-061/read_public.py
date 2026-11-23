"""Fetch public primary materials into ignored cache; record acquisition, not reading.

Usage: python -B read_public.py ID URL [--pdf]
This does not promote a fetched document to sources.jsonl direct-read evidence.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source_id')
    ap.add_argument('url')
    ap.add_argument('--pdf', action='store_true')
    args = ap.parse_args()
    if not args.url.startswith('https://') or not args.source_id.replace('-', '').replace('_', '').isalnum():
        raise SystemExit('Public HTTPS and safe source ID required')
    cache = ROOT / '.cache' / 'root'
    cache.mkdir(parents=True, exist_ok=True)
    start = datetime.now(timezone.utc).isoformat()
    record = dict(source_id=args.source_id, url=args.url, acquisition_start_utc=start,
                  reader='root', direct_read=False)
    try:
        request = urllib.request.Request(args.url, headers={'User-Agent': 'AF-RES-061 public research'})
        with urllib.request.urlopen(request, timeout=45) as response:
            content = response.read()
            record.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type'))
        suffix = '.pdf' if args.pdf else '.txt'
        path = cache / (args.source_id + suffix)
        path.write_bytes(content)
        record.update(bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                      cache_path=str(path.relative_to(ROOT)))
        if args.pdf:
            text = cache / (args.source_id + '.txt')
            run = subprocess.run(['pdftotext', '-layout', str(path), str(text)], capture_output=True)
            record.update(extract_exit=run.returncode, extracted_path=str(text.relative_to(ROOT)))
    except Exception as exc:
        record.update(status='failed', reason=str(exc))
    record['acquisition_end_utc'] = datetime.now(timezone.utc).isoformat()
    with (ROOT / 'evidence' / 'root-acquisitions.jsonl').open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
