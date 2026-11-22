"""Read publisher objects without executing any publisher/consumer code.

Keeps tiny extracted data members and audit receipts, not whole R archives.
"""
import concurrent.futures, datetime, hashlib, io, json, tarfile, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(item):
    label, url, kind = item
    out = dict(label=label, source_url=url, opened_utc=now(), kind=kind)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-047 public research'})
        with urllib.request.urlopen(req, timeout=50) as r:
            body=r.read()
            out.update(final_url=r.url, http_status=r.status, response_headers=dict(r.headers))
        out.update(completed_utc=now(), size=len(body), sha256=hashlib.sha256(body).hexdigest())
        if kind == 'r_tar':
            with tarfile.open(fileobj=io.BytesIO(body), mode='r:gz') as t:
                names=[n for n in t.getnames() if '/datasets/' in n and ('iris' in n.lower())]
                out['members']=[]
                for n in names:
                    content=t.extractfile(n).read()
                    path=ROOT/'objects'/(label+'-'+n.rsplit('/',1)[-1])
                    path.parent.mkdir(exist_ok=True)
                    path.write_bytes(content)
                    out['members'].append(dict(path=n, size=len(content), sha256=hashlib.sha256(content).hexdigest(), stored_path=str(path.relative_to(ROOT))))
        elif kind == 'iris_zip':
            with zipfile.ZipFile(io.BytesIO(body)) as z:
                out['members']=[]
                for n in z.namelist():
                    b=z.read(n)
                    path=ROOT/'objects'/('uci-'+n.rsplit('/',1)[-1])
                    path.parent.mkdir(exist_ok=True)
                    path.write_bytes(b)
                    m=dict(path=n,size=len(b),sha256=hashlib.sha256(b).hexdigest(),stored_path=str(path.relative_to(ROOT)))
                    if n.endswith('.data'):
                        lines=[x for x in b.decode().splitlines() if x.strip()]
                        groups={x.rsplit(',',1)[-1] for x in lines}
                        m.update(row_count=len(lines), groups=sorted(groups), one_way_species_df=len(groups)-1, row35=lines[34], row38=lines[37])
                    out['members'].append(m)
        else:
            path=ROOT/'objects'/(label+'.json')
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(body)
            out['stored_path']=str(path.relative_to(ROOT))
        return out
    except Exception as e:
        out.update(completed_utc=now(),error=repr(e))
        return out

items=[
 ('R-4.2.0','https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz','r_tar'),
 ('R-4.2.1','https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz','r_tar'),
 ('uci-iris','https://archive.ics.uci.edu/static/public/53/iris.zip','iris_zip'),
 ('rstyle-1.0-tree','https://api.github.com/repos/chainsawriot/rstyle/git/trees/07a60457c88dbb20858441047f248d61ce2955c7?recursive=1','json'),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    result=list(pool.map(read,items))
(ROOT/'object_comparison_receipts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for r in result:
    print(json.dumps({k:v for k,v in r.items() if k not in ('response_headers',)},ensure_ascii=False))
