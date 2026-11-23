"""Prepare already-committed owned changes for GitHub git-data publication.

Does not perform network writes. Root uses authorized GitHub connector with a
lease, verifies the returned tree equals local_tree, then fetches that commit.
The payload is transient and not research evidence.
"""
from pathlib import Path
import json, subprocess, sys
task=Path(__file__).resolve().parents[1]
repo=task.parents[3]
parent=sys.argv[1]
tag=sys.argv[2]
if not tag.replace('-','').isalnum(): raise ValueError('invalid tag')
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
paths=git('diff','--name-only',parent,'HEAD','--').decode().splitlines()
prefix='docs/workstreams/research/AF-RES-056/'
assert all(x.startswith(prefix) for x in paths)
entries=[]
for path in paths:
    entries.append({'path':path,'mode':'100644','type':'blob','content':git('show','HEAD:'+path).decode()})
payload=json.dumps(entries,ensure_ascii=False)
out=task/'evidence/transient';out.mkdir(exist_ok=True)
f=out/('publish-'+tag+'.json');f.write_text(payload)
print(json.dumps({'parent':parent,'tag':tag,'chars':len(payload),'files':len(entries),'local_tree':git('rev-parse','HEAD^{tree}').decode().strip(),'payload':str(f.relative_to(repo))}))
