"""Reproduce only the original YT1 test with upstream source, helper, runner and lock."""
import hashlib
import io
import json
import pathlib
import re
import subprocess
import tarfile
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OWNED = HERE.parents[2]
SHA = '0a09ff854b2ecd942b3c0f0e741253a214cee1bf'
CACHE = OWNED / '.cache' / 'yjs' / 'upstream-reproduce'
CACHE.mkdir(parents=True, exist_ok=True)
URL = 'https://codeload.github.com/yjs/yjs/tar.gz/' + SHA
data = urllib.request.urlopen(URL, timeout=60).read()
with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
    archive.extractall(CACHE, filter='data')
project = CACHE / ('yjs-' + SHA)
for item in json.loads((HERE / 'upstream-file-pins.json').read_text())['files']:
    blob = (project / item['path']).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(blob)).encode() + b'\0' + blob).hexdigest()
    if actual != item['git_blob_sha']:
        raise SystemExit('Source mismatch: ' + item['path'])
if (project / 'package-lock.json').read_bytes() != (HERE / 'upstream-package-lock.json').read_bytes():
    raise SystemExit('Original lock differs from committed acquisition')
subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=project, check=True)
command = ['npm', 'test', '--', '--filter', 'undoredo: infinite capture timeout$', '--seed', '57']
run = subprocess.run(command, cwd=project, capture_output=True, text=True)
(CACHE / 'run.stdout.txt').write_text(run.stdout)
(CACHE / 'run.stderr.txt').write_text(run.stderr)
headers = re.findall(r'^\[\d+/\d+\] (.+)$', run.stdout, re.M)
passed = re.findall(r'^Success: infinite capture timeout in ', run.stdout, re.M)
print(json.dumps({'exit_code': run.returncode, 'tests_selected': len(headers), 'tests_passed': len(passed),
                  'execution_kind': 'local_original_source_test', 'public_CI': False,
                  'stdout': str(CACHE / 'run.stdout.txt'), 'stderr': str(CACHE / 'run.stderr.txt')}))
if run.returncode or len(headers) != 1 or len(passed) != 1:
    raise SystemExit(1)
