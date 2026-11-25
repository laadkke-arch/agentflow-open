"""Verify downloaded npm distributions and the installed JS executed by Playwright."""
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parent


def curl(url):
    return subprocess.check_output(['curl', '-fsSL', '--max-time', '25', url])


def check(deps):
    inputs = json.loads((ROOT / 'inputs.json').read_text())
    lock = json.loads((deps / 'package-lock.json').read_text())['packages']
    for build in inputs['builds']:
        version = build['version']
        registry = f'https://registry.npmjs.org/axe-core/{version}'
        metadata = json.loads(curl(registry))
        alias = 'axe' + version.replace('.', '')
        assert metadata['name'] == 'axe-core' and metadata['version'] == version
        assert metadata['gitHead'] == build['gitHead']
        entry = lock['node_modules/' + alias]
        distribution = metadata['dist']
        assert distribution['tarball'] == entry['resolved']
        payload = curl(entry['resolved'])
        sha1 = hashlib.sha1(payload).hexdigest()
        integrity = 'sha512-' + base64.b64encode(hashlib.sha512(payload).digest()).decode()
        assert sha1 == distribution['shasum']
        assert integrity == entry['integrity'] == distribution['integrity']
        with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
            member = archive.extractfile('package/axe.min.js')
            assert member is not None
            js = member.read()
        installed = deps / 'node_modules' / alias / 'axe.min.js'
        assert js == installed.read_bytes()
        yield {
            'version': version,
            'registryUrl': registry,
            'gitHead': metadata['gitHead'],
            'tarballUrl': entry['resolved'],
            'tarballBytes': len(payload),
            'tarballSha1': sha1,
            'tarballSha256': hashlib.sha256(payload).hexdigest(),
            'tarballIntegrity': integrity,
            'axeFile': f'{alias}/axe.min.js',
            'axeBytes': len(js),
            'axeSha256': hashlib.sha256(js).hexdigest(),
            'installedBytesEqual': True,
        }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python verify-builds.py DEPS_DIR')
    print(json.dumps(list(check(Path(sys.argv[1]))), indent=2))
