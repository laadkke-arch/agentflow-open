from pathlib import Path
import urllib.request,tarfile,io,hashlib,json,gzip
from datetime import datetime,timezone
from lxml import html
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parents[1]/'collectors/b'
def run(x):
 base,v=x;u=base+f'python-pycurl-doc_{v}_all.deb';o={'event_id':'B03','candidate_document':'PycURL Quickstart','version':v,'url':u,'observed_at_utc':datetime.now(timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(u,timeout=30);b=r.read();(P/'cache'/f'python-pycurl-doc_{v}.deb').write_bytes(b);o.update(status=r.status,archive_sha256=hashlib.sha256(b).hexdigest(),last_modified=r.headers.get('Last-Modified'),last_modified_role='file metadata only')
  assert b[:8]==b'!<arch>\n';pos=8;members={}
  while pos<len(b):
   head=b[pos:pos+60];size=int(head[48:58]);members[head[:16].decode().strip().rstrip('/')]=b[pos+60:pos+60+size];pos+=60+size+(size%2)
  t=tarfile.open(fileobj=io.BytesIO(next(value for key,value in members.items() if key.startswith('data.tar'))));ns=[n for n in t.getnames() if n.endswith('/quickstart.html')];o['found_members']=ns;o['documents']=[]
  for n in ns:
   raw=t.extractfile(n).read();doc=html.fromstring(raw);aa=[]
   for a in doc.xpath('//a[@href]'):
    if 'curl.haxx.se' in a.get('href') or 'curl.se' in a.get('href'):
     q=a
     while q.getparent() is not None and q.tag not in ['p','dd','li']:q=q.getparent()
     aa.append({'href':a.get('href'),'text':a.text_content(),'paragraph':q.text_content()})
   o['documents'].append({'member':n,'sha256':hashlib.sha256(raw).hexdigest(),'links':aa})
  logs=[n for n in t.getnames() if n.endswith('/changelog.Debian.gz')]
  if logs:o['changelog_first']=gzip.decompress(t.extractfile(logs[0]).read()).decode().split('\n\n')[:4]
 except Exception as e:o['error']=repr(e)
 return o
jobs=[('https://archive.debian.org/debian/pool/main/p/pycurl/','7.43.0.2-0.1'),('https://deb.debian.org/debian/pool/main/p/pycurl/','7.43.0.6-5'),('https://deb.debian.org/debian/pool/main/p/pycurl/','7.45.2-3')]
rows=list(ThreadPoolExecutor(3).map(run,jobs));(P/'debian-archives.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
