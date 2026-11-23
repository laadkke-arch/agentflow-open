"""Restore exact, losslessly compressed ranking/inventory ledgers before replay.

Run from any directory. No network, source execution, or judgment changes.
"""
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def main():
    manifest = json.loads((ROOT / 'evidence/compressed-ledgers.json').read_text())
    for row in manifest['files']:
        compressed = (ROOT / row['compressed_path']).read_bytes()
        if hashlib.sha256(compressed).hexdigest() != row['compressed_sha256']:
            raise ValueError('compressed ledger changed: ' + row['compressed_path'])
        raw = gzip.decompress(compressed)
        if hashlib.sha256(raw).hexdigest() != row['logical_sha256']:
            raise ValueError('logical ledger changed: ' + row['logical_path'])
        target = ROOT / row['logical_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != raw:
            raise ValueError('refusing to overwrite different ledger: ' + str(target))
        target.write_bytes(raw)
    print(json.dumps({'restored_or_verified': len(manifest['files']), 'network': False}))

if __name__ == '__main__':
    main()
