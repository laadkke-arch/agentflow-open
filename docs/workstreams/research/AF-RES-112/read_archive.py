"""Explicit URL ZIP view; no crawl, extraction, installation, or code execution."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
MAX_ARCHIVE = 15_000_000
MAX_FILE = 2_000_000


def main():
    p = argparse.ArgumentParser()
    p.add_argument('session')
    p.add_argument('url')
    p.add_argument('--entry')
    a = p.parse_args()
    if not (len(a.session) == 3 and a.session[0] == 'r' and a.session[1:].isdigit()):
        raise ValueError('invalid reader id')
    parsed = urllib.parse.urlsplit(a.url)
    if parsed.scheme != 'https' or parsed.netloc != 'github.com' or not parsed.path.endswith('.zip'):
        raise ValueError('only the original HTTPS GitHub ZIP URL is supported')
    directory = ROOT / 'cache' / 'reader-zips' / a.session
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory / 'source.zip'
    metadata = directory / 'metadata.json'
    if not archive.exists():
        hops = []

        class Redirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                hops.append({'from': req.full_url, 'to': newurl, 'status': code})
                return super().redirect_request(req, fp, code, msg, headers, newurl)

        opener = urllib.request.build_opener(Redirect())
        with opener.open(a.url, timeout=15) as r:
            data = r.read(MAX_ARCHIVE + 1)
            if len(data) > MAX_ARCHIVE:
                raise ValueError('archive exceeds bounded download size')
            meta = {'original_url': a.url, 'arrival_url': r.url,
                    'status': r.status, 'redirects': hops,
                    'downloaded_bytes': len(data),
                    'sha256': hashlib.sha256(data).hexdigest(),
                    'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        archive.write_bytes(data)
        metadata.write_text(json.dumps(meta, ensure_ascii=False), encoding='utf-8')
    meta = json.loads(metadata.read_text())
    if meta['original_url'] != a.url:
        raise ValueError('cached URL mismatch')
    with zipfile.ZipFile(archive) as z:
        files = [x for x in z.infolist() if not x.is_dir()]
        if a.entry is None:
            result = {'metadata': meta, 'kind': 'archive_directory',
                      'entries': [{'name': x.filename, 'bytes': x.file_size} for x in files[:200]],
                      'listing_truncated': len(files) > 200}
        else:
            info = z.getinfo(a.entry)
            if info.file_size > MAX_FILE:
                raise ValueError('entry exceeds bounded text size')
            data = z.read(info)
            text = data.decode('utf-8')
            result = {'metadata': meta, 'kind': 'archive_entry', 'entry': a.entry,
                      'source_sha256': hashlib.sha256(data).hexdigest(), 'text': text[:10000],
                      'source_truncated_after_codepoints': 10000 if len(text) > 10000 else None}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'error': type(error).__name__ + ': ' + str(error)}))
