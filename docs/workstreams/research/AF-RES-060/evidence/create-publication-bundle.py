"""Prepare only AF-RES-060 changed text files for the authorized GitHub commit API.

This does not publish, move refs, or stage files. Raw retrieval caches remain ignored.
"""
from pathlib import Path
import argparse, json, subprocess

ap = argparse.ArgumentParser()
ap.add_argument('stage')
args = ap.parse_args()
root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip())
owned = 'docs/workstreams/research/AF-RES-060/'
paths = set()
for cmd in [
    ['git', 'diff', '--name-only', '-z', 'HEAD'],
    ['git', 'ls-files', '--others', '--exclude-standard', '-z'],
]:
    paths.update(x for x in subprocess.check_output(cmd, cwd=root).decode().split('\0') if x)
assert all(x.startswith(owned) for x in paths), 'A change outside the owned path must be investigated'
files = []
for name in sorted(paths):
    if name.endswith('-upload.json'):
        continue
    path = root / name
    if path.is_file():
        content = path.read_bytes().decode('utf-8')
        # Preserve byte identity and seed local object storage before the remote fetch.
        assert content.encode('utf-8') == path.read_bytes(), name
        subprocess.run(['git', 'hash-object', '-w', str(path)], cwd=root, check=True, capture_output=True)
        files.append({'path': name, 'mode': '100644', 'type': 'blob', 'content': content})
    else:
        files.append({'path': name, 'mode': '100644', 'type': 'blob', 'sha': None})
bundle = {
    'parent': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
    'base_tree': subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=root, text=True).strip(),
    'files': files,
}
target = root / owned / 'evidence' / (args.stage + '-upload.json')
text = json.dumps(bundle, ensure_ascii=False, separators=(',', ':'))
target.write_text(text, encoding='utf-8')
print(json.dumps({'file': str(target), 'entries': len(files), 'characters': len(text), 'chunks_12000': (len(text)+11999)//12000, 'parent': bundle['parent']}, ensure_ascii=False))
