"""Recover an issue's original opened event from public GH Archive.

Never emits comments or other issues. Writes selected raw issue body only into
the task's ignored private directory. No authentication or target execution.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request


def recover(repo, number, created, target):
    hour = dt.datetime.fromisoformat(created.replace('Z', '+00:00'))
    url = f'https://data.gharchive.org/{hour:%Y-%m-%d}-{hour.hour}.json.gz'
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    receipt = dict(repo=repo, issue_number=number, created_at=created,
                   archive_url=url, accessed_utc=started, status='unknown')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-070-public-research'})
        with urllib.request.urlopen(req, timeout=55) as r:
            receipt['http_status'] = r.status
            with gzip.GzipFile(fileobj=r) as stream:
                for lineno, raw in enumerate(stream, 1):
                    # Full JSON parse only after narrow lexical filtering.
                    if b'IssuesEvent' not in raw or repo.lower().encode() not in raw.lower():
                        continue
                    event = json.loads(raw)
                    payload = event.get('payload', {})
                    issue = payload.get('issue', {})
                    if (event.get('type') == 'IssuesEvent'
                            and event.get('repo', {}).get('name', '').lower() == repo.lower()
                            and payload.get('action') == 'opened'
                            and issue.get('number') == number):
                        body = issue.get('body') or ''
                        receipt.update(status='original_recovered', archive_line=lineno,
                                       event_id=event.get('id'), event_created_at=event.get('created_at'),
                                       body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                                       event_sha256=hashlib.sha256(raw).hexdigest(),
                                       issue_created_at=issue.get('created_at'),
                                       author=issue.get('user', {}).get('login'),
                                       body=body, event=event)
                        break
                else:
                    receipt['status'] = 'opened_event_not_found'
    except Exception as exc:
        receipt.update(status='access_failed', error=f'{type(exc).__name__}: {exc}')
    receipt['completed_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return {k: v for k, v in receipt.items() if k not in ('body', 'event')}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('repo')
    p.add_argument('number', type=int)
    p.add_argument('created')
    p.add_argument('output', type=Path)
    a = p.parse_args()
    print(json.dumps(recover(a.repo, a.number, a.created, a.output), ensure_ascii=False))
