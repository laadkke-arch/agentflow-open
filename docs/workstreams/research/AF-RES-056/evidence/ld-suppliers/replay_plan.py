"""Narrow offline diagnostic; observation receipts are stored separately."""
from pathlib import Path
import datetime
import hashlib
import json
import importlib.metadata
import platform
import subprocess
import sys

from pyld import jsonld
from pyld.__about__ import __version__

if __version__ != '3.3.0':
    raise RuntimeError('This plan requires PyLD 3.3.0 and the pinned source commit.')

source_root = Path(jsonld.__file__).resolve().parents[2]
source_commit = subprocess.check_output(
    ['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True
).strip()
required_commit = '3ac1987d9be3648c09b7c7e34865ce82d637e742'
if source_commit != required_commit:
    raise RuntimeError('The loaded PyLD source commit is not the pinned commit.')

external_document_requests = []
def offline_loader(url, options=None):
    external_document_requests.append(url)
    raise RuntimeError('This diagnostic forbids external document loading: ' + url)

fixture_path = Path(__file__).with_name('minimal-fixtures.json')
raw = fixture_path.read_bytes()
plan = json.loads(raw)
records = []
for case in plan['cases']:
    record = {'case_id': case['case_id'], 'actual_version': __version__}
    try:
        options = dict(case['options'], documentLoader=offline_loader)
        output = jsonld.frame(case['input'], case['frame'], options=options)
        values = output.get('values', []) if isinstance(output, dict) else []
        values = values if isinstance(values, list) else [values]
        c1 = len(values) == 1 and isinstance(values[0], dict) and values[0].get('a') == 1
        c2 = (
            isinstance(output, dict)
            and output.get('issuer') == 'issuer-A'
            and len(values) == 1
            and isinstance(values[0], dict)
            and values[0].get('b') == 2
            and values[0].get('c') == 3
        )
        record.update(output=output, C1=c1, C2=c2)
        record['matches_planned_prediction'] = (
            c1 == case['C1_expected'] and c2 == case['C2_expected']
        )
    except Exception as exc:
        record.update(error_type=type(exc).__name__, error=str(exc))
        record['matches_planned_prediction'] = False
    records.append(record)
receipt = {
    'executed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'module_file': jsonld.__file__,
    'actual_version': __version__,
    'required_source_commit': required_commit,
    'actual_source_commit': source_commit,
    'source_commit_verified_by_script': True,
    'source_worktree_status': subprocess.check_output(
        ['git', '-C', str(source_root), 'status', '--short'], text=True
    ).strip(),
    'python': sys.version,
    'platform': platform.platform(),
    'dependency_versions': {
        name: importlib.metadata.version(name)
        for name in ('cachetools', 'frozendict', 'lxml')
    },
    'external_document_requests': external_document_requests,
    'external_document_loader': 'deny all requests',
    'fixture_sha256': hashlib.sha256(raw).hexdigest(),
    'scope': 'local researcher-authored mechanism fixture; not original LD-3; not a returned two-action window',
    'records': records,
}
print(json.dumps(receipt, ensure_ascii=False, indent=2))
sys.exit(0 if all(r['matches_planned_prediction'] for r in records) else 1)
