#!/usr/bin/env python3
"""Re-fetch one recorded GNU evidence source and verify its exact excerpt slices.
Usage: python verify-evidence.py GNU-P-SHELL
No files are written, and no downloaded program is installed or executed.
An unversioned or dynamic HTML response may legitimately change; that is a
verification failure against this recorded response, never silently accepted.
"""
import gzip
import hashlib
import io
import json
import sys
import tarfile
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def deb_data(data):
    pos = 8
    while pos + 60 <= len(data):
        header = data[pos:pos + 60]
        name = header[:16].decode().strip().rstrip('/')
        size = int(header[48:58])
        value = data[pos + 60:pos + 60 + size]
        pos += 60 + size + (size % 2)
        if name.startswith('data.tar'):
            return value
    raise ValueError('Debian data.tar member not found')


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == 'id' or (tag == 'a' and key == 'name'):
                self.values.append(value)


def main(source_id):
    root = Path(__file__).resolve().parent
    records = [json.loads(line) for line in (root / 'sources.jsonl').read_text().splitlines()]
    source = next(row for row in records if row['source_id'] == source_id)
    if not source.get('directly_read') or not source.get('url'):
        raise ValueError('Select a directly read primary source, not an error or search summary')
    request_url = urllib.parse.urldefrag(source['url'])[0]
    request = urllib.request.Request(request_url, headers={
        'User-Agent': 'Mozilla/5.0 AF-RES-036 evidence reproduction',
        'Accept-Encoding': 'identity',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
        result = {'source_id': source_id, 'http_status': response.status,
                  'final_url': response.url, 'retrieved_body_sha256': digest(data)}
    checks = {}
    if source.get('member'):
        checks['archive_sha256_matches'] = digest(data) == source['archive_sha256']
        archive = deb_data(data) if data.startswith(b'!<arch>\n') else data
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:*') as tar:
            data = tar.extractfile(source['member']).read()
        checks['member_sha256_matches'] = digest(data) == source['member_sha256']
        if source.get('member_transform') == 'gzip.decompress':
            data = gzip.decompress(data)
    checks['source_sha256_matches'] = digest(data) == source['source_sha256']
    checks['exact_excerpt_slices_match'] = all(
        data[e['byte_start_0_based']:e['byte_end_exclusive']] == e['text'].encode('utf-8')
        and digest(data[e['byte_start_0_based']:e['byte_end_exclusive']]) == e['sha256']
        for e in source['exact_excerpts']
    )
    if source.get('fragment_checks'):
        parser = Anchors()
        parser.feed(data.decode('utf-8'))
        checks['fragment_counts_match'] = all(
            parser.values.count(check['fragment']) == check['id_or_anchor_name_match_count']
            for check in source['fragment_checks']
        )
    result['checks'] = checks
    result['verified_recorded_response'] = all(checks.values())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['verified_recorded_response'] else 2


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python verify-evidence.py SOURCE_ID')
    raise SystemExit(main(sys.argv[1]))
