"""Capture prespecified public issue frames; do not read comments or solutions."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import gzip
import json
import re
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent

def utc():
    return datetime.now(timezone.utc).isoformat()

def request_job(job):
    project, repo, word = job
    q = f'repo:{repo} is:issue created:2023-01-01..2025-12-31 in:body {word}'
    url = 'https://api.github.com/search/issues?' + urllib.parse.urlencode(dict(q=q, sort='created', order='asc', per_page=100, page=1))
    start = utc()
    req = urllib.request.Request(url, headers={'Accept':'application/vnd.github+json','User-Agent':'AF-RES-116-public-research'})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw=r.read(); arrival=r.url; status=r.status
    end=utc()
    d=json.loads(raw)
    path=BASE/'recruitment'/project/f'search-{word}.json.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(raw,mtime=0))
    receipt=dict(project=project,repo=repo,word=word,query=q,url=url,arrived_url=arrival,status=status,started_utc=start,finished_utc=end,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),total_count=d.get('total_count'),incomplete_results=d.get('incomplete_results'),returned=len(d.get('items',[])),last_created_at=d.get('items',[{}])[-1].get('created_at'))
    return receipt,d

def main():
    jobs=[('pandoc','jgm/pandoc',w) for w in ['table','image']]+[('imagemagick','ImageMagick/ImageMagick',w) for w in ['profile','alpha']]
    outcomes=list(ThreadPoolExecutor(max_workers=4).map(request_job,jobs))
    (BASE/'recruitment/receipts.json').write_text(json.dumps([r for r,d in outcomes],ensure_ascii=False,indent=2)+'\n')
    allrows=[]
    for project,repo,words,start in [('pandoc','jgm/pandoc',['table','image'],'https://pandoc.org/MANUAL.html'),('imagemagick','ImageMagick/ImageMagick',['profile','alpha'],'https://imagemagick.org/script/command-line-processing.php')]:
        union={}
        rx=re.compile(r'\b(?:'+ '|'.join(words)+r')\b',re.I)
        for r,d in outcomes:
            if r['project']!=project: continue
            for it in d.get('items',[]):
                if 'pull_request' not in it and rx.search(it.get('body') or ''):
                    union[it['number']]=it
        selected=sorted(union.values(),key=lambda x:(x['created_at'],x['number']))[:50]
        if len(selected)!=50: raise RuntimeError(f'{project}: insufficient frame {len(selected)}')
        threshold=selected[-1]['created_at']
        for r,d in outcomes:
            if r['project']==project:
                if r['incomplete_results']: raise RuntimeError('incomplete search result')
                if r['returned']<r['total_count'] and r['last_created_at'] <= threshold: raise RuntimeError('need another search page for '+project)
        docs=[]
        for rank,it in enumerate(selected,1):
            keep={k:it.get(k) for k in ['number','title','body','created_at','updated_at','html_url']}
            keep['author']=it['user']['login']; keep['rank']=rank;keep['project']=project
            keep['body_sha256']=hashlib.sha256((it.get('body') or '').encode()).hexdigest()
            docs.append(keep)
            allrows.append(dict(project=project,rank=rank,number=it['number'],created_at=it['created_at'],original_url=it['html_url'],title=it['title'],body_sha256=keep['body_sha256'],start_url=start,screening='not_yet_read',case_id='',reason=''))
        (BASE/'recruitment'/project/'first50.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n')
        print(project, len(selected), selected[0]['number'], selected[-1]['number'], threshold)
    with (BASE/'frame.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)

if __name__=='__main__':main()
