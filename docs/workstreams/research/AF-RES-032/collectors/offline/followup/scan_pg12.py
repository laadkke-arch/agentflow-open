from pathlib import Path
import concurrent.futures, datetime, hashlib, html, io, json, re, tarfile, bz2, urllib.request
P=Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
index=(P/'cache/pg-index').read_text()
versions=sorted(set(re.findall(r'href="v(12\.\d+)/',index)),key=lambda x:int(x.split('.')[1]))
assert versions==['12.'+str(i) for i in range(23)],versions
versions=[v for v in versions if int(v.split('.')[1])>=3]
def run(v):
 u=f'https://ftp.postgresql.org/pub/source/v{v}/postgresql-{v}.tar.bz2'
 d={'version':v,'archive_url':u,'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_complete_for_lineage':'official index lists 12.0 through 12.22; this scan covers 12.3 through 12.22 after sealed 12.2'}
 try:
  cached=P/'cache'/('pg-'+v)
  if cached.exists():b=cached.read_bytes();d['cache_reuse']=True
  else:
   r=urllib.request.urlopen(u,timeout=45);b=r.read();cached.write_bytes(b);d.update(http_status=r.status,final_url=r.url,cache_reuse=False)
  d.update(archive_sha256=h(b),archive_size_bytes=len(b))
  t=tarfile.open(fileobj=io.BytesIO(bz2.decompress(b)),mode='r:');prefix=f'postgresql-{v}/doc/src/sgml/html/'
  m=[]
  for name,needle in [('acronyms.html','American_National_Standards_Institute'),('app-psql.html','rfc4180')]:
   path=prefix+name;content=t.extractfile(path).read();s=content.decode();ix=s.index(needle);left=s.rfind('<p',0,ix);right=s.index('</p>',ix)+4;para=s[left:right]
   hrefs=re.findall(r'href="([^"]*'+needle+'[^"]*)"',s)
   fn=f'excerpts/pg-{v}-{name}.fragment.html';(P/fn).write_text(para)
   if v in ['12.18','12.19']:(P/f'excerpts/pg-{v}-{name}').write_bytes(content)
   m.append({'member_path':path,'member_sha256':h(content),'member_size_bytes':len(content),'target_href':hrefs,'relevant_bytes_sha256':h(para.encode()),'relevant_copy':fn,'read_lines':[s[:left].count('\n')+1,s[:right].count('\n')+1]})
  n='release-'+v.replace('.','-')+'.html';rb=t.extractfile(prefix+n).read();rs=rb.decode();date=re.search(r'Release date:.*?(\d{4}-\d{2}-\d{2})',rs,re.S).group(1)
  (P/f'excerpts/pg-{v}-{n}').write_bytes(rb)
  d.update(release_date=date,release_date_role='stated release day; timezone not stated; first HTML public-access time not observed',release_member=prefix+n,release_member_sha256=h(rb),members=m)
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(4) as pool:
 for d in pool.map(run,versions):
  with (P/'pg-editions.jsonl').open('a') as f:f.write(json.dumps(d,ensure_ascii=False)+'\n')
  print(d['version'],d.get('release_date'),[x['target_href'] for x in d.get('members',[])],d.get('error',''),flush=True)
