from pathlib import Path
import urllib.request,concurrent.futures,datetime,hashlib,json,re,io,zipfile
P=Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
items=[('3.35.0','3350000','2021'),('3.37.2','3370200','2022'),('3.41.0','3410000','2023'),('3.47.2','3470200','2024')]
def run(x):
 v,num,year=x;u=f'https://www.sqlite.org/{year}/sqlite-doc-{num}.zip';d={'version':v,'archive_url':u,'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sampling':'additional fixed annual follow-up checkpoints; no first-change claim'}
 try:
  c=P/'cache'/('sqlite-'+v)
  if c.exists():b=c.read_bytes();d['cache_reuse']=True
  else:r=urllib.request.urlopen(u,timeout=40);b=r.read();c.write_bytes(b);d.update(http_status=r.status,final_url=r.url,cache_reuse=False)
  d.update(archive_sha256=h(b),archive_size_bytes=len(b));z=zipfile.ZipFile(io.BytesIO(b));prefix='sqlite-doc-'+num+'/'
  m=[]
  for name,needle in [('about.html','Endianness'),('aff_short.html','darwinsys')]:
   path=prefix+name;b=z.read(path);s=b.decode();i=s.index(needle);left=s.rfind('<p',0,i);right=s.index('</p>',i)+4;para=s[left:right];fn=f'excerpts/sqlite-{v}-{name}.fragment.html';(P/fn).write_text(para)
   m.append({'member_path':path,'member_sha256':h(b),'member_size_bytes':len(b),'target_href':re.findall(r'href=[\"\x27]([^\"\x27]*'+needle+'[^\"\x27]*)',s),'relevant_bytes_sha256':h(para.encode()),'relevant_copy':fn,'read_lines':[s[:left].count('\n')+1,s[:right].count('\n')+1]})
  n='releaselog/'+v.replace('.','_')+'.html';rb=z.read(prefix+n);rs=rb.decode();date=re.search(r'Release[^<]+?(\d{4}-\d{2}-\d{2})',rs).group(1);(P/f'excerpts/sqlite-{v}-release.html').write_bytes(rb)
  d.update(release_date=date,release_date_role='official product release day; exact first HTML public-access timestamp unverified',release_member=prefix+n,release_member_sha256=h(rb),members=m)
 except Exception as e:d['error']=str(e)
 return d
with concurrent.futures.ThreadPoolExecutor(4) as pool:
 for d in pool.map(run,items):
  with (P/'sqlite-editions.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
  print(d['version'],d.get('release_date'),[x['target_href'] for x in d.get('members',[])],d.get('error',''),flush=True)
