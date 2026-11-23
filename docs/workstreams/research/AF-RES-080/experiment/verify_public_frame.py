"""Read-only GitHub public issue-list verification without closing or answers."""
import concurrent.futures
import csv
import datetime
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

EMBEDDED = re.compile(r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>', re.S)

def fetch_page(repo, page, closed):
    terms = ['is:issue', 'created:2022-01-01..2024-12-31', 'sort:created-asc']
    if closed:
        terms.insert(1,'is:closed')
    url = 'https://github.com/' + repo + '/issues?' + urllib.parse.urlencode({'q':' '.join(terms),'page':page})
    at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(url,timeout=15) as response:
        source=response.read()
        arrival=response.geturl()
        status=response.status
    route=json.loads(EMBEDDED.search(source.decode('utf-8')).group(1))['payload']['issuesIndexContentRoute']
    assert route['pageInfo']['currentPage']==page
    details=[item['issue'] for item in route['results']]
    # Select only search ordinal metadata, deliberately omit issue statuses/title/body.
    return {
        'utc':at,'url':url,'arrival_url':arrival,'http':status,'page':page,'repo':repo,'closed_query':closed,
        'result_total_reported':route['pageInfo']['totalCount'],'page_sha256':hashlib.sha256(source).hexdigest(),'bytes':len(source),
        'records':[dict(number=r['number'],created_at=r.get('createdAt')) for r in details],
    }

def main():
    csv_in=Path(sys.argv[1])
    closed=sys.argv[2]=='calibration' if len(sys.argv)>2 else False
    count=100 if closed else 60
    pages=(count+24)//25
    repos=['pallets/click','python-attrs/attrs']
    with csv_in.open(newline='',encoding='utf-8') as stream:
        expected=list(csv.DictReader(stream))
    works=[(repo,n,closed) for repo in repos for n in range(1,pages+1)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(lambda row:fetch_page(*row), works))
    for page in results:
        print(json.dumps(page,ensure_ascii=False))
    for repo in repos:
        actual=[r['number'] for p in results if p['repo']==repo for r in p['records']][:count]
        listed=sorted((r for r in expected if r['repo']==repo and r['number']), key=lambda r:int(r['ordinal']))
        want=[int(r['number']) for r in listed]
        if len(want)!=count or actual!=want:
            raise SystemExit(f'{repo}: actual {actual}, expected {want}')
        dates=[r['created_at'] for p in results if p['repo']==repo for r in p['records']][:count]
        assert dates == [r['created_at'] for r in listed]
        print(f'{repo}: {len(want)} exact dates, numbers and sort positions equal',file=sys.stderr)

if __name__=='__main__':
    main()
