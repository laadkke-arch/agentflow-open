#!/usr/bin/env python3
"""Restore committed input/reference/actual3.10.3 outputs without network access."""
import argparse,base64,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--output',default='evidence/runtime/restored-gdal3103');a=ap.parse_args()
target=(P/a.output).resolve();assert target.is_relative_to(P),'Output must stay in owned path'
m=json.loads((P/'evidence/gdal3103-artifacts.json').read_text())
for r in m['files']:
    data=base64.b64decode(r['content'],validate=True)
    assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
    out=(target/r['name']).resolve();assert out.is_relative_to(target)
    if out.exists():assert out.read_bytes()==data,'Refuse to overwrite different bytes: '+str(out)
    else:out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
print(json.dumps({'restored_files':len(m['files']),'bytes':sum(r['bytes'] for r in m['files']),'output':str(target)}))
