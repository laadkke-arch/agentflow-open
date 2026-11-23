"""Small local transport for GitHub connector commits; never holds credentials."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
OWNED = ROOT.relative_to(REPO).as_posix() + '/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def files():
    changed = git('diff', '--name-only', 'HEAD', '--', OWNED).decode().splitlines()
    untracked = git('ls-files', '--others', '--exclude-standard', '--', OWNED).decode().splitlines()
    rows = []
    for path in sorted(set(changed + untracked)):
        p = REPO / path
        if not p.is_file():
            raise ValueError('deletion requires a separate explicit implementation: ' + path)
        raw = p.read_bytes()
        sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        try:
            content = raw.decode('utf-8')
            if '\x00' in content:
                raise UnicodeError('binary NUL')
            encoding = 'utf-8'
        except UnicodeError:
            content = base64.b64encode(raw).decode('ascii')
            encoding = 'base64'
        rows.append({'path': path, 'bytes': len(raw), 'chars': len(content),
                     'git_blob_sha': sha, 'sha256': hashlib.sha256(raw).hexdigest(),
                     'encoding': encoding})
    return rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('command', choices=['list', 'chunk'])
    ap.add_argument('--path'); ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--size', type=int, default=16000); ap.add_argument('--encoding', default='utf-8')
    a = ap.parse_args()
    if a.command == 'list':
        print(json.dumps({'head': git('rev-parse', 'HEAD').decode().strip(),
                          'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(), 'files': files()}))
    else:
        if not a.path or not a.path.startswith(OWNED) or '..' in Path(a.path).parts:
            raise ValueError('outside owned path')
        raw = (REPO / a.path).read_bytes()
        s = raw.decode('utf-8') if a.encoding == 'utf-8' else base64.b64encode(raw).decode('ascii')
        print(json.dumps({'content': s[a.start:a.start+a.size]}, ensure_ascii=False))

if __name__ == '__main__':
    main()
