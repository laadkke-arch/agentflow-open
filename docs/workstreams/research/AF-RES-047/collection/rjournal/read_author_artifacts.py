"""Fetch fixed author artifacts, without running their R code."""
import concurrent.futures,datetime,hashlib,json,urllib.request
from pathlib import Path
P=Path(__file__).resolve().parent
BASE='https://raw.githubusercontent.com/chainsawriot/rstyle/07a60457c88dbb20858441047f248d61ce2955c7/'
paths=['README.md','config.R','extract_metadata.R','helpers.R','syntax03_vis.R','target_meta.RDS','data/syntax_feature_yr1998.RDS','rjournal_submission/figures.R','rjournal_submission/yenetal.tex']
def read(path):
    r={'path':path,'source_url':BASE+path,'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(r['source_url'],timeout=40) as q:
            b=q.read();r.update(final_url=q.url,status=q.status)
        r.update(size=len(b),sha256=hashlib.sha256(b).hexdigest(),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        target=P/'author' / path
        target.parent.mkdir(exist_ok=True,parents=True);target.write_bytes(b)
        r['stored_path']=str(target.relative_to(P))
    except Exception as e:r['error']=repr(e)
    return r
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as x:rs=list(x.map(read,paths))
(P/'author_artifact_receipts.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n')
for r in rs:print(json.dumps(r))
