"""Print one authorized staged blob for the GitHub connector; no credentials."""
from pathlib import Path
import base64,json,subprocess,sys
OWNED='docs/workstreams/research/AF-RES-116/'
def git(*args):return subprocess.check_output(['git',*args])
if len(sys.argv)==1:
    paths=git('diff','--cached','--name-only','--diff-filter=ACM').decode().splitlines()
    if any(not p.startswith(OWNED) for p in paths):raise SystemExit('outside ownership')
    items=[{'path':p,'sha':git('rev-parse',':'+p).decode().strip(),'bytes':int(git('cat-file','-s',':'+p))} for p in paths]
    print(json.dumps({'parent':git('rev-parse','HEAD').decode().strip(),'base_tree':git('rev-parse','HEAD^{tree}').decode().strip(),'paths':paths,'items':items}))
elif sys.argv[1]=='--chunk':
    p=sys.argv[2];offset=int(sys.argv[3]);size=48000
    if not p.startswith(OWNED) or '..' in Path(p).parts:raise SystemExit('outside ownership')
    b=git('show',':'+p)
    print(json.dumps({'path':p,'offset':offset,'total':len(b),'content':base64.b64encode(b[offset:offset+size]).decode()}))
else:
    p=sys.argv[1]
    if not p.startswith(OWNED) or '..' in Path(p).parts:raise SystemExit('outside ownership')
    b=git('show',':'+p)
    try:content=b.decode();encoding='utf-8'
    except UnicodeDecodeError:content=base64.b64encode(b).decode();encoding='base64'
    print(json.dumps({'path':p,'content':content,'encoding':encoding}))
