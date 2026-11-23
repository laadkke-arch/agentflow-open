import urllib.request,urllib.error,json,datetime,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def get(key,url,scope=''):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF-RES-102-public-research'}),timeout=60)
  b=r.read();status=r.status
 except urllib.error.HTTPError as e:
  r=e;b=e.read();status=e.code
 (ROOT/'cache'/f'{key}.bin').write_bytes(b)
 receipt={'id':key,'url':url,'final_url':r.url,'utc':now,'status':status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'headers':{x:r.headers.get(x) for x in ['Content-Type','ETag','Last-Modified']},'scope':scope}
 (ROOT/'receipts'/f'{key}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 return b,receipt

if __name__=='__main__':
 urls={
 'old-release':'https://api.github.com/repos/matplotlib/matplotlib/releases/tags/v3.6.3',
 'new-release':'https://api.github.com/repos/matplotlib/matplotlib/releases/tags/v3.7.0',
 'old-tag':'https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v3.6.3',
 'new-tag':'https://api.github.com/repos/matplotlib/matplotlib/git/ref/tags/v3.7.0',
 'old-pub-history':'https://api.github.com/repos/matplotlib/matplotlib.github.io/commits?path=3.6.3/index.html&per_page=100',
 'new-pub-metadata':'https://api.github.com/repos/matplotlib/matplotlib.github.io/git/commits/410d8388303fab638bbedbd1d2eace0e5efb0de9'
 }
 for k,u in urls.items():
  b,r=get(k,u,'release/tag/commit metadata only; no new body/resource/CI');print(k,r['status'])
  if r['status']==200:
   d=json.loads(b)
   if k.endswith('release'):print({x:d.get(x) for x in ['tag_name','target_commitish','published_at','html_url']},'assets',[(a['name'],a['browser_download_url']) for a in d.get('assets',[])])
   elif k.endswith('tag'):print(d.get('object'))
   elif k=='old-pub-history':print([{x:z.get(x) for x in ['sha','html_url']}|{'date':z.get('commit',{}).get('committer',{}).get('date'),'message':z.get('commit',{}).get('message','').splitlines()[0]} for z in d])
   else:print({x:d.get(x) for x in ['sha','tree','author','committer','message']})
