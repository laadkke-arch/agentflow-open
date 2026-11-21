#!/usr/bin/env python3
"""Audit frozen Git blobs and working content, accepting only Git's LF normalization."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def main(write):
    manifest=json.loads((ROOT/'runs/INPUT_MANIFEST.json').read_text())
    rows=[];errors=[]
    for path,expected in manifest['hashes'].items():
        f=ROOT/path;relative=f.relative_to(REPO).as_posix();working=f.read_bytes()
        frozen=subprocess.check_output(['git','show',manifest['gold_commit']+':'+relative],cwd=REPO)
        head=subprocess.check_output(['git','show','HEAD:'+relative],cwd=REPO)
        exact=sha(working)==expected;lf_only=not exact and sha(working.replace(b'\r\n',b'\n'))==expected
        passed=sha(frozen)==expected and sha(head)==expected and (exact or lf_only)
        rows.append({'path':path,'expected_sha256':expected,'frozen_blob_sha256':sha(frozen),
                     'head_blob_sha256':sha(head),'working_bytes_sha256':sha(working),
                     'working_LF_only_difference':lf_only,'passed':passed})
        if not passed:errors.append(path)
    result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'gold_commit':manifest['gold_commit'],'rows':rows,'errors':errors,
            'interpretation':'Git stores LF for these text artifacts. A CRLF-only working-copy difference does not change frozen questions, answers or rules; all other differences fail.'}
    if write:(ROOT/'analysis/input-integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'files':len(rows),'passed':not errors,'errors':errors,
                      'working_LF_only_differences':[r['path'] for r in rows if r['working_LF_only_difference']]}))
    if errors:raise SystemExit(1)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();main(a.write)
