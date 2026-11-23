"""Read every committed owned artifact back from the exact GitHub result SHA.

Compare bytes with canonical Git blobs, not platform newline conversions. This
is delivery verification only. No branch mutation and no inference of behavior.
"""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE=Path(__file__).resolve().parent
REPO=BASE.parents[3]
OWNED='docs/workstreams/research/AF-RES-079/'
parser=argparse.ArgumentParser()
parser.add_argument('--commit',required=True)
parser.add_argument('--output')
parser.add_argument('--brief',action='store_true')
args=parser.parse_args()
if not re.fullmatch(r'[0-9a-f]{40}',args.commit):
    raise SystemExit('exact 40-character SHA required')
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',args.commit,'--',OWNED],cwd=REPO,text=True).splitlines()
assert paths and all(p.startswith(OWNED) for p in paths)
started=dt.datetime.now(dt.timezone.utc).isoformat()


def verify(path):
    canonical=subprocess.check_output(['git','show',args.commit+':'+path],cwd=REPO)
    digest=hashlib.sha256(canonical).hexdigest()
    url='https://raw.githubusercontent.com/laadkke-arch/agentflow-open/'+args.commit+'/'+path
    row={'path':path,'url':url,'git_blob_sha256':digest,'expected_bytes':len(canonical),'attempts':[]}
    for _ in range(2):
        attempt={'started_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-079 exact-result-verification'}),timeout=30) as response:
                data=response.read()
                attempt.update({'status':response.status,'arrived_url':response.url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matches_git_blob':data==canonical})
            row['attempts'].append(attempt)
            row['passed']=attempt['status']==200 and attempt['matches_git_blob']
            if row['passed']:break
        except Exception as exc:
            attempt.update({'status':getattr(exc,'code',None),'error_type':type(exc).__name__,'error':str(exc)})
            row['attempts'].append(attempt)
            row['passed']=False
    return row


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows=list(pool.map(verify,paths))
failed=[r['path'] for r in rows if not r['passed']]
manifest='\n'.join(r['path']+' '+r['git_blob_sha256'] for r in rows)+'\n'
report={'actor':'root via local Python urllib GET','location':str(REPO),'started_utc':started,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'repository':'laadkke-arch/agentflow-open','result_commit':args.commit,'owned_path':OWNED,'checked_files':len(rows),'matched_files':sum(r['passed'] for r in rows),'failed_paths':failed,'canonical_manifest_sha256':hashlib.sha256(manifest.encode()).hexdigest(),'exit_code':1 if failed else 0,'command_argv':sys.argv,'files':rows,'limit':'Exact remote bytes and committed scope only; not an additional software compatibility test.'}
if args.output:
    output=Path(args.output).resolve()
    if not output.is_relative_to(BASE):raise SystemExit('output must remain in owned path')
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if args.brief:
    selected={'RESULT.md','SELF_CHECK.md','SCOPE.md','frame.csv','sources.jsonl','observations.csv','relations.csv','evidence/acceptance-evidence.json','streams/oss/historical/paired-check.receipt.json','streams/gis/historical/native-summary.json','streams/review/blind-review.json','HANDOFF.md'}
    shown={k:v for k,v in report.items() if k!='files'}
    shown['selected_hashes']={r['path'][len(OWNED):]:r['git_blob_sha256'] for r in rows if r['path'][len(OWNED):] in selected}
    print(json.dumps(shown,ensure_ascii=False))
else:
    print(json.dumps(report,ensure_ascii=False))
sys.exit(report['exit_code'])
