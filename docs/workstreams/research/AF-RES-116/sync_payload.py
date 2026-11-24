"""Print one authorized staged blob for the GitHub connector; no credentials."""
from pathlib import Path
import base64,json,subprocess,sys
OWNED='docs/workstreams/research/AF-RES-116/'
def git(*args):return subprocess.check_output(['git',*args])
if len(sys.argv)==1:
    paths=git('diff','--cached','--name-only','--diff-filter=ACM').decode().splitlines()
    if any(not p.startswith(OWNED) for p in paths):raise SystemExit('outside ownership')
    print(json.dumps({'parent':git('rev-parse','HEAD').decode().strip(),'base_tree':git('rev-parse','HEAD^{tree}').decode().strip(),'paths':paths}))
else:
    p=sys.argv[1]
    if not p.startswith(OWNED) or '..' in Path(p).parts:raise SystemExit('outside ownership')
    b=git('show',':'+p)
    try:content=b.decode();encoding='utf-8'
    except UnicodeDecodeError:content=base64.b64encode(b).decode();encoding='base64'
    print(json.dumps({'path':p,'content':content,'encoding':encoding}))
