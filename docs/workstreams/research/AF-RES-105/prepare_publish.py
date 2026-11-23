"""Prepare bounded inline GitHub tree payloads from the staged owned-path diff.

Does not publish, push, commit or mutate refs. The caller publishes each tree,
creates one commit with the recorded parent, and updates the ref with a lease.
"""
from pathlib import Path
import subprocess
import json
import hashlib
import datetime

ROOT=Path(__file__).resolve().parent
PREFIX='docs/workstreams/research/AF-RES-105/'

def git(*args):return subprocess.check_output(['git',*args],text=True).strip()

def main():
    head=git('rev-parse','HEAD')
    changes=[line.split('\t') for line in git('diff','--cached','--name-status').splitlines() if line]
    if not changes:raise SystemExit('No staged changes')
    if any(len(row)!=2 or not row[1].startswith(PREFIX) for row in changes):
        raise SystemExit('Unexpected rename or path outside task scope')
    batches=[];batch=[];size=0
    for status,path in changes:
        entry={'path':path,'mode':'100644','type':'blob'}
        if status=='D':entry['sha']=None
        else:
            entry['content']=subprocess.check_output(['git','show',':'+path],text=True)
        n=len(json.dumps(entry,ensure_ascii=False).encode())
        if batch and n+size>85000:batches.append(batch);batch=[];size=0
        batch.append(entry);size+=n
    if batch:batches.append(batch)
    cache=ROOT/'.cache'/'publish';cache.mkdir(parents=True,exist_ok=True)
    for i,b in enumerate(batches):
        (cache/f'batch-{i}.json').write_text(json.dumps(b,ensure_ascii=False))
    meta={'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_sha':head,
          'base_tree_sha':git('rev-parse','HEAD^{tree}'),'expected_tree_sha':git('write-tree'),
          'batch_count':len(batches),'changed_paths':[p for s,p in changes],
          'batch_sizes':[len(json.dumps(b,ensure_ascii=False).encode()) for b in batches]}
    (cache/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print(json.dumps(meta,ensure_ascii=False))

if __name__=='__main__':main()
