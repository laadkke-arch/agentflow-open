#!/usr/bin/env python3
"""Print explicitly selected owned files as a GitHub tree payload. Does not commit."""
import argparse
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[5]
OWNED = pathlib.Path('docs/workstreams/research/AF-RES-025')
parser = argparse.ArgumentParser()
parser.add_argument('paths', nargs='+')
args = parser.parse_args()
files = []
for item in args.paths:
    rel = pathlib.Path(item)
    if rel.is_absolute() or '..' in rel.parts or not (rel == OWNED or OWNED in rel.parents):
        raise SystemExit('outside owned path: ' + item)
    path = REPO / rel
    candidates = sorted(path.rglob('*')) if path.is_dir() else [path]
    for f in candidates:
        if not f.is_file() or '.git' in f.parts or '__pycache__' in f.parts:
            continue
        if subprocess.run(['git','check-ignore','-q','--',f.relative_to(REPO).as_posix()],cwd=REPO).returncode==0:
            continue
        files.append(f)
entries = []
for f in sorted(set(files)):
    data = f.read_bytes()
    content = data.decode('utf-8')
    entries.append({'path': f.relative_to(REPO).as_posix(), 'mode': '100644', 'type': 'blob', 'content': content})
print(json.dumps(entries, ensure_ascii=False))
