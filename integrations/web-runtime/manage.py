"""Install/run the reviewed community runtime without touching host projects.

No elevated installation, credentials, public tunnel or browser login is automatic.
Docker named volumes are preserved; this tool never removes volumes.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
LOCK = json.loads((HERE/'upstreams.json').read_text(encoding='utf-8'))
SHA = LOCK['wrapper']['commit']
BASE = 'agentflow-community-runtime:'+SHA[:12]
IMAGE = 'agentflow-web-runtime:'+SHA[:12]
CACHE = Path(os.environ.get('AGENTFLOW_WEB_HOME', str(Path.home()/'.agentflow-web-runtime'))).resolve()
PROJECT = 'agentflow-web-runtime'


def run(args, *, cwd=None, capture=False, timeout=900):
    return subprocess.run(args, cwd=cwd, check=True, text=True, encoding='utf-8',
                          capture_output=capture, timeout=timeout)


def prerequisites():
    for name in ('git','docker'):
        if not shutil.which(name):
            raise RuntimeError(name+' is missing. Install/enable it locally; no admin changes were attempted.')
    system=run(['docker','info','--format','{{.OSType}}'], capture=True, timeout=30).stdout.strip()
    if system != 'linux':
        raise RuntimeError('Select the Docker Linux container engine; no host setting was changed.')
    run(['docker','compose','version'], capture=True, timeout=30)


def compose(*args, capture=False):
    path = CACHE/'compose.json'
    if not path.is_file():
        raise RuntimeError('Run setup or start first.')
    return run(['docker','compose','--project-name',PROJECT,'-f',str(path),*args],capture=capture)


def prepare():
    prerequisites()
    CACHE.mkdir(parents=True,exist_ok=True)
    target = CACHE/('upstream-'+SHA[:12])
    if not target.exists():
        run(['git','init',str(target)])
        run(['git','-C',str(target),'remote','add','origin','https://github.com/'+LOCK['wrapper']['repository']+'.git'])
        run(['git','-C',str(target),'fetch','--depth','1','origin',SHA])
        run(['git','-C',str(target),'checkout','--detach','FETCH_HEAD'])
    actual=run(['git','-C',str(target),'rev-parse','HEAD'],capture=True).stdout.strip()
    dirty=run(['git','-C',str(target),'status','--porcelain'],capture=True).stdout.strip()
    if actual != SHA or dirty:
        raise RuntimeError('Cached upstream differs from reviewed commit; not overwriting it.')
    run(['docker','build','--progress=plain','-t',BASE,str(target)])
    run(['docker','build','--progress=plain','--build-arg','BASE='+BASE,'-t',IMAGE,str(HERE)])
    identity=run(['docker','image','inspect',IMAGE,'--format','{{.Id}}'],capture=True).stdout.strip()
    (CACHE/'build-receipt.json').write_text(json.dumps({'wrapper_commit':SHA,'image':IMAGE,'image_id':identity,
         'note':'Source pinned. Upstream base image tags and apt repositories are not a bit-reproducible lock.'},indent=2),encoding='utf-8')
    print('PREPARED '+IMAGE)


def configuration(public=False, offline=False):
    if public and offline:
        raise ValueError('Public tunnel and offline test mode are mutually exclusive.')
    service = {'image':IMAGE,'init':False,'restart':'unless-stopped','read_only':True,
        'cap_drop':['ALL'],'security_opt':['no-new-privileges:true'],'pids_limit':256,
        'mem_limit':'1g','cpus':'2',
        'environment':{'PUBLIC_BASE_URL':'' if public else 'http://127.0.0.1:8766'},
        'volumes':['state:/state','workspace:/workspace'],
        'tmpfs':['/tmp:uid=1000,gid=1000,mode=1777,size=512m'],
        'healthcheck':{'test':['CMD','python3','-c',"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8766/healthz',timeout=5)"],
                       'interval':'10s','timeout':'8s','retries':3,'start_period':'120s'},
        'logging':{'driver':'json-file','options':{'max-size':'10m','max-file':'3'}}}
    if offline:
        service['network_mode']='none'
    return {'name':PROJECT,'services':{'runtime':service},'volumes':{'state':{},'workspace':{}}}


def start(public=False, offline=False):
    prerequisites()
    CACHE.mkdir(parents=True,exist_ok=True)
    run(['docker','image','inspect',IMAGE],capture=True)
    config=configuration(public,offline)
    (CACHE/'compose.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    compose('up','-d')
    for _ in range(90):
        try:
            compose('exec','-T','runtime','python3','-c',
                    "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8766/healthz',timeout=3)",capture=True)
            print('RUNNING '+('public endpoint requested' if public else 'internal only; no public endpoint'))
            return
        except subprocess.CalledProcessError:
            time.sleep(1)
    raise RuntimeError('Runtime did not become healthy. Existing volumes were preserved.')


def verify():
    compose('exec','-T','runtime','python3','/opt/kc-mcp/scripts/check_live.py')


def seed():
    script = "from pathlib import Path; import subprocess; p=Path('/workspace/agentflow-open'); " \
             "exists=(p/'.git').is_dir(); " \
             "assert exists or not any(p.iterdir()), 'Nonempty workspace preserved; manual review required'; " \
             "print('Existing checkout preserved' if exists else 'Cloning approved public work branch'); " \
             "subprocess.run(['git','clone','--single-branch','--branch','chore/workspace-foundation'," \
             "'https://github.com/laadkke-arch/agentflow-open.git',str(p)],check=True,timeout=120) if not exists else None"
    compose('exec','-T','runtime','python3','-c',script)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','setup','start','seed','verify','status','stop','connect','owner-key'])
    parser.add_argument('--approve-public-endpoint',action='store_true')
    parser.add_argument('--offline',action='store_true',help='Disable all container external networking for tests.')
    args=parser.parse_args()
    if args.action=='prepare': prepare()
    elif args.action=='setup':
        prepare(); start(offline=args.offline); verify()
        if not args.offline: seed()
        print('Local runtime ready. ChatGPT is NOT connected. Public exposure requires connect --approve-public-endpoint.')
    elif args.action=='start': start(offline=args.offline)
    elif args.action=='seed': seed()
    elif args.action=='verify': verify()
    elif args.action=='stop': compose('stop')
    elif args.action=='status':
        compose('ps')
        compose('exec','-T','runtime','cat','/state/connection-url.txt')
    elif args.action=='connect':
        if not args.approve_public_endpoint:
            raise RuntimeError('Public HTTPS exposure requires --approve-public-endpoint. No change was made.')
        start(public=True,offline=args.offline); verify()
        compose('exec','-T','runtime','cat','/state/connection-url.txt')
        print('Authorize this endpoint yourself. Do not paste the owner key into any chat.')
    elif args.action=='owner-key':
        if not sys.stdout.isatty():
            raise RuntimeError('Owner key is shown only in your interactive terminal, never CI or redirected logs.')
        compose('exec','-T','runtime','cat','/state/oauth-owner.token')

if __name__=='__main__':
    try:
        main()
    except (RuntimeError,ValueError,subprocess.CalledProcessError,subprocess.TimeoutExpired,OSError) as exc:
        print('SETUP_STOPPED: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
