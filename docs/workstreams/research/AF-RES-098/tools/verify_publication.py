#!/usr/bin/env python3
"""Reopen committed GitHub deliverables and compare them with exact Git blobs.

No source or publication is mutated. The optional receipt path must not exist.
This checks publication availability and byte identity, not scientific truth.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.request import HTTPRedirectHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
REL = ROOT.relative_to(REPO).as_posix()
FILES = [
    'RESULT.md', 'SELF_CHECK.md', 'reproduce.md', 'SCOPE.md', 'freeze.json',
    'frame.csv', 'predictions.csv', 'lineage.csv', 'sources.jsonl',
    'evidence/counts.json', 'evidence/input-contract.json',
    'evidence/prediction-seal.json', 'evidence/matplotlib/audit.json',
    'evidence/cpython/audit.json', 'evidence/ggplot2/audit.json',
    'evidence/calibration/audit.json', 'evidence/cross-domain/audit.json',
    'evidence/cross-review/final-review.json',
    'evidence/cross-review/source-count-review.json',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


class Redirects(HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.steps = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.steps.append({'from': req.full_url, 'status': code, 'to': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_one(commit, name):
    path = REL + '/' + name
    wanted = subprocess.check_output(['git', '-C', str(REPO), 'show', commit + ':' + path])
    url = 'https://raw.githubusercontent.com/laadkke-arch/agentflow-open/' + commit + '/' + path
    record = {'file': name, 'commit': commit, 'url': url,
              'utc': datetime.now(timezone.utc).isoformat(),
              'git_blob_bytes': len(wanted), 'git_blob_sha256': sha(wanted)}
    handler = Redirects()
    try:
        with build_opener(handler).open(url, timeout=40) as response:
            actual = response.read()
            record.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type'),
                          bytes=len(actual), sha256=sha(actual),
                          same_as_git_blob=(actual == wanted))
        record['passed'] = record['status'] == 200 and record['same_as_git_blob']
        if name == 'RESULT.md':
            text = actual.decode('utf-8')
            # The structural validator performs detailed table parsing; this is
            # a remote-content presence check after exact-byte comparison.
            record['required_sections_present'] = all(x in text for x in
                ('## 1. 모집·사전 예측 표', '## 2. 판별 표', '## 3. 목적별 반환 표'))
            record['passed'] &= record['required_sections_present']
    except Exception as error:
        record.update(passed=False, error=type(error).__name__ + ': ' + str(error))
    record['redirects'] = handler.steps
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.commit):
        parser.error('--commit must be a complete Git SHA')
    if args.output and args.output.exists():
        parser.error('Receipt output already exists; choose a new path')
    with ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(lambda name: read_one(args.commit, name), FILES))
    result = {'checked_commit': args.commit, 'utc': datetime.now(timezone.utc).isoformat(),
              'status': 'passed' if all(r['passed'] for r in rows) else 'failed',
              'checked_files': len(rows), 'passed_files': sum(bool(r['passed']) for r in rows),
              'scope': 'GitHub fixed-commit tables, evidence, and reproduction instructions; exact Git blob equality.',
              'not_claimed': 'A rendering/browser run, revalidation of every cited external source, or build generation attestation.',
              'rows': rows}
    out = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(out)
    print(out)
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
