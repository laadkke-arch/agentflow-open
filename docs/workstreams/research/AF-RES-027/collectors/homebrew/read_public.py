"""Bounded read-only public GitHub retrieval; preserves URLs/hashes, not whole sources."""
import concurrent.futures,datetime,hashlib,json,re,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).parent
def read(url):
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-027-public-research'}),timeout=30) as r:
            data=r.read(); status=r.status
        rec={'url':url,'checked_utc':t,'http_status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        result=data.decode()
    except Exception as e:
        rec={'url':url,'checked_utc':t,'error':str(e)};result=None
    with (ROOT/'retrieval-receipts.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
    return result
def snapshot(repo,until):
    u=f'https://api.github.com/repos/{repo}/commits?until={until}&per_page=1'
    raw=read(u)
    if not raw:return {'repo':repo,'error':'snapshot access failed'}
    commits=json.loads(raw)
    if not commits:return {'repo':repo,'error':'no earlier commit'}
    c=commits[0];sha=c['sha'];tree=c['commit']['tree']['sha']
    raw=read(f'https://api.github.com/repos/{repo}/git/trees/{tree}?recursive=1')
    if not raw:return {'repo':repo,'sha':sha,'error':'tree access failed'}
    data=json.loads(raw)
    paths=[x['path'] for x in data['tree'] if x['type']=='blob' and re.search(r'Brewfile|INSTALL|install|build|contribut|environment.*ya?ml|conda.*ya?ml|workflow',x['path'],re.I)]
    result={'repo':repo,'sha':sha,'date':c['commit']['committer']['date'],'tree_sha':tree,'tree_truncated':data.get('truncated'), 'paths':sorted(paths)}
    return result
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='snapshots':
        repos=sys.argv[3:]
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            for r in ex.map(lambda repo:snapshot(repo,sys.argv[2]),repos):print(json.dumps(r,ensure_ascii=False))
    elif mode=='file':
        repo,sha,path=sys.argv[2:5]
        text=read(f'https://raw.githubusercontent.com/{repo}/{sha}/{path}')
        print('\n'.join(f'{i+1}: {line}' for i,line in enumerate(text.splitlines())) if text is not None else 'ACCESS FAILED')
