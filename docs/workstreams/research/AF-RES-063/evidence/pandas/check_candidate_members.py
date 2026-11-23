"""Read two new historical pytz public archives; do not execute conversions."""
import urllib.request,json,concurrent.futures,pathlib,datetime,hashlib,zipfile,io
P=pathlib.Path(__file__).parent

def get(u):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'AF-RES-063-public-research'}),timeout=40);d=r.read()
 return d,{'url':u,'opened_utc':t,'status':r.status,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def f(v):
 result={'package':'pytz','version':v,'purpose':'Q4 exact region member versus whole edition; not a historical process or transform replay','transform_execution':'미실시','requests':[]}
 try:
  d,r=get(f'https://pypi.org/pypi/pytz/{v}/json');result['requests'].append(r);j=json.loads(d)
  wh=next(x for x in j['urls'] if x['packagetype']=='bdist_wheel')
  result['publication_utc']=wh['upload_time_iso_8601'];result['url']=wh['url'];result['registry_sha256']=wh['digests']['sha256'];result['filename']=wh['filename']
  d,r=get(wh['url']);result['requests'].append(r);result['archive_sha256']=r['sha256'];result['registry_match']=result['archive_sha256']==result['registry_sha256']
  with zipfile.ZipFile(io.BytesIO(d)) as z:
   b=z.read('pytz/zoneinfo/Europe/Berlin');source=z.read('pytz/__init__.py').decode()
   result['berlin_member']={'path':'pytz/zoneinfo/Europe/Berlin','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'header':b[:5].hex()}
   result['labels']=[line for line in source.splitlines() if line.startswith(('OLSON_VERSION','VERSION','__version__'))]
 except Exception as e:result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: rows=list(ex.map(f,['2020.1','2020.5']))
result={'rows':rows,'same_berlin_bytes':len(rows)==2 and rows[0].get('berlin_member',{}).get('sha256')==rows[1].get('berlin_member',{}).get('sha256'),'same_archive':rows[0].get('archive_sha256')==rows[1].get('archive_sha256')}
(P/'candidate-member-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
