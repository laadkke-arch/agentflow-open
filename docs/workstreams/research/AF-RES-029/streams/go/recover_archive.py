#!/usr/bin/env python3
"""Recover only the original GitHub IssuesEvent(action=opened) from GHArchive.

Unrelated events, comments, state changes and outcomes are streamed past without
model display or persistence. GHArchive is a third-party capture of GitHub's
public event feed, not native GitHub edit-history proof.
"""
import gzip
import csv
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class HashReader:
    def __init__(self, stream):
        self.stream = stream
        self.sha = hashlib.sha256()
        self.bytes = 0
    def read(self, size=-1):
        chunk = self.stream.read(size)
        self.sha.update(chunk)
        self.bytes += len(chunk)
        return chunk

def recover(number, verbose=True, hour_offset=0):
    rows = list(csv.DictReader((ROOT / 'frame.csv').open()))
    row = next(x for x in rows if int(x['number']) == number)
    stamp = datetime.fromisoformat(row['first_public_date'].replace('Z', '+00:00')) + timedelta(hours=hour_offset)
    url = f'https://data.gharchive.org/{stamp:%Y-%m-%d}-{stamp.hour}.json.gz'
    receipt = {
        'canonical_id': row['canonical_id'], 'issue_url': row['url'],
        'archive_url': url, 'checked_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'actual shell urllib HTTPS GET; gzip stream; exact repository/type/action/issue-number filter',
        'source_role': 'third-party capture of original public GitHub IssuesEvent, not native edit history',
        'expected_issue_created_at': row['first_public_date'],
        'archive_hour_offset': hour_offset,
        'unrelated_event_bodies_displayed_or_retained': False,
    }
    (ROOT / 'receipts').mkdir(exist_ok=True)
    (ROOT / 'bodies').mkdir(exist_ok=True)
    try:
        request = urllib.request.Request(url, headers={
            'User-Agent': 'AF-RES-029 public initial-issue archival research',
            'Range': 'bytes=0-',
        })
        with urllib.request.urlopen(request, timeout=45) as response:
            receipt['http_status'] = response.status
            receipt['archive_headers'] = {key: response.headers.get(key) for key in [
                'Content-Length', 'Content-Range', 'Last-Modified', 'ETag',
                'x-goog-generation', 'x-goog-hash', 'x-goog-stored-content-length']}
            reader = HashReader(response)
            count = 0
            found = None
            with gzip.GzipFile(fileobj=reader) as archive:
                for raw_line in archive:
                    count += 1
                    if b'"golang/go"' not in raw_line or b'"IssuesEvent"' not in raw_line:
                        continue
                    event = json.loads(raw_line)
                    issue = event.get('payload', {}).get('issue', {})
                    if (event.get('type') == 'IssuesEvent'
                            and event.get('repo', {}).get('name') == 'golang/go'
                            and event.get('payload', {}).get('action') == 'opened'
                            and issue.get('number') == number):
                        found = event
                        receipt['event_line_ordinal'] = count
                        receipt['event_raw_line_sha256'] = hashlib.sha256(raw_line).hexdigest()
                        break
            receipt['compressed_prefix_bytes_read'] = reader.bytes
            receipt['compressed_prefix_sha256'] = reader.sha.hexdigest()
            receipt['archive_fully_read'] = found is None
            receipt['event_lines_examined'] = count
            if found:
                issue = found['payload']['issue']
                body = issue.get('body') or ''
                receipt.update({
                    'result': 'initial_opened_event_recovered',
                    'event_id': found['id'], 'event_created_at': found['created_at'],
                    'issue_created_at': issue['created_at'], 'issue_updated_at_at_capture': issue['updated_at'],
                    'title_at_open': issue['title'], 'author_login': issue['user']['login'],
                    'initial_body_sha256': hashlib.sha256(body.encode()).hexdigest(),
                    'initial_body_length': len(body), 'initial_body_file': f'bodies/{number}-initial.md',
                    'event_capture_file': f'receipts/{number}-opened-event.json',
                })
                (ROOT / receipt['initial_body_file']).write_text(body)
                # The matched original event alone is retained. It contains no later comments.
                (ROOT / receipt['event_capture_file']).write_text(json.dumps(found, indent=2) + '\n')
            else:
                receipt['result'] = 'no_matching_opened_event'
    except Exception as exc:
        receipt['result'] = 'retrieval_failed'
        receipt['error'] = f'{type(exc).__name__}: {exc}'
    suffix = '' if hour_offset == 0 else f'-{hour_offset:+d}h'
    (ROOT / f'receipts/{number}-archive-recovery{suffix}.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if verbose:
        print(json.dumps(receipt), flush=True)
    return receipt

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        recover(int(arg))
