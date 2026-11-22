#!/usr/bin/env python3
"""Narrow fallback: event captured at the exact issue creation/update timestamp.

This does not accept later IssueEvent snapshots, and does not display outcomes.
The timestamp test is weaker than an opened-event and is reported explicitly.
"""
import csv
import gzip
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from recover_archive import HashReader

ROOT = Path(__file__).resolve().parent

def recover(number):
    row = next(r for r in csv.DictReader((ROOT/'frame.csv').open()) if int(r['number']) == number)
    initial = row['first_public_date']
    stamp = datetime.fromisoformat(initial.replace('Z','+00:00'))
    url = f'https://data.gharchive.org/{stamp:%Y-%m-%d}-{stamp.hour}.json.gz'
    receipt = {'canonical_id': row['canonical_id'], 'archive_url':url,
        'checked_utc':datetime.now(timezone.utc).isoformat(),
        'method':'actual shell gzip scan; exact event.created_at == issue.created_at == issue.updated_at timestamp test',
        'native_edit_history_recovered':False,
        'limitation':'Second-resolution timestamps do not prove absence of a same-second edit; no later-time snapshot accepted.'}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-029 public initial-issue archival research','Range':'bytes=0-'})
        with urllib.request.urlopen(req,timeout=45) as response:
            reader=HashReader(response)
            receipt['http_status']=response.status
            receipt['etag']=response.headers.get('ETag')
            receipt['generation']=response.headers.get('x-goog-generation')
            found=None
            with gzip.GzipFile(fileobj=reader) as archive:
                for ordinal,line in enumerate(archive,1):
                    if b'"golang/go"' not in line or b'"IssuesEvent"' not in line: continue
                    event=json.loads(line)
                    issue=event.get('payload',{}).get('issue',{})
                    if issue.get('number') != number or event.get('repo',{}).get('name') != 'golang/go': continue
                    if (event.get('created_at') == initial == issue.get('created_at') == issue.get('updated_at')
                            and event.get('payload',{}).get('action') in ['opened','labeled','assigned','milestoned']):
                        found=event
                        receipt['event_line_ordinal']=ordinal
                        receipt['event_raw_line_sha256']=hashlib.sha256(line).hexdigest()
                        break
            receipt['compressed_prefix_bytes_read']=reader.bytes
            receipt['compressed_prefix_sha256']=reader.sha.hexdigest()
            receipt['archive_fully_read']=found is None
        if found:
            issue=found['payload']['issue'];body=issue.get('body') or ''
            receipt.update({'result':'coincident_initial_snapshot_recovered','event_id':found['id'],
                'action':found['payload']['action'],'event_created_at':found['created_at'],
                'issue_created_at':issue['created_at'],'issue_updated_at_at_capture':issue['updated_at'],
                'title_at_open':issue['title'],'author_login':issue['user']['login'],
                'initial_body_sha256':hashlib.sha256(body.encode()).hexdigest(),
                'initial_body_length':len(body),'initial_body_file':f'bodies/{number}-initial-snapshot.md',
                'event_capture_file':f'receipts/{number}-initial-snapshot-event.json'})
            (ROOT/receipt['initial_body_file']).write_text(body)
            (ROOT/receipt['event_capture_file']).write_text(json.dumps(found,indent=2)+'\n')
        else: receipt['result']='no_coincident_initial_snapshot'
    except Exception as exc:
        receipt.update({'result':'retrieval_failed','error':f'{type(exc).__name__}: {exc}'})
    (ROOT/f'receipts/{number}-initial-snapshot-recovery.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt

if __name__=='__main__':
    for value in sys.argv[1:]: print(json.dumps(recover(int(value))),flush=True)
