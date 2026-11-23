"""Follow-up only: preserve the original frame failure and inspect its cause."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

from pyld import jsonld
from pyld.__about__ import __version__

source_root = Path(jsonld.__file__).resolve().parents[2]
source_commit = subprocess.check_output(
    ['git', '-C', str(source_root), 'rev-parse', 'HEAD'], text=True
).strip()
assert __version__ == '3.3.0'
assert source_commit == '3ac1987d9be3648c09b7c7e34865ce82d637e742'
fixture_path = Path(__file__).with_name('minimal-fixtures.json')
raw = fixture_path.read_bytes()
case = next(c for c in json.loads(raw)['cases'] if c['case_id'] == 'PLAN-LD-NEST')
requests = []

def offline_loader(url, options=None):
    requests.append(url)
    raise RuntimeError('External document loading is forbidden: ' + url)

options = dict(case['options'], documentLoader=offline_loader)
receipt = {
    'diagnostic_id': 'DIAG-LD-NEST-CAUSE',
    'original_case_id': case['case_id'],
    'fixture_sha256': hashlib.sha256(raw).hexdigest(),
    'source_commit': source_commit,
    'version': __version__,
    'executed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'same negative input and frame; new diagnostic only; original expected values and exit 1 remain unchanged',
}
receipt['expanded_input'] = jsonld.expand(case['input'], options=options)
try:
    receipt['frame_output'] = jsonld.frame(case['input'], case['frame'], options=options)
except Exception as exc:
    causes = []
    while exc is not None:
        causes.append({
            'error_class': type(exc).__name__,
            'error_type': getattr(exc, 'type', None),
            'error_code': getattr(exc, 'code', None),
            'message': str(exc),
        })
        exc = exc.__cause__
    receipt['frame_error_chain'] = causes
receipt['external_document_requests'] = requests
print(json.dumps(receipt, ensure_ascii=False, indent=2))
