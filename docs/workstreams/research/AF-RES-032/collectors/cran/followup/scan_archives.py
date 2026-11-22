import pathlib,json,datetime,urllib.request,hashlib,tarfile,re,concurrent.futures,sys
from lxml import html
P=pathlib.Path(__file__).parent;R=P.parent
REFS=[json.loads(x) for x in (R/'final/references.jsonl').read_text().splitlines()]
INV=json.loads((P/'all-editions-inventory.json').read_text())
KEYS={'A-R01':['datatables','DT package'],'A-R02':['docco'],'A-R03':['page-break-after','break-after'],'A-R04':['RStudio','rstudio','Pandoc'],'A-R05':['dbplyr'],'A-R06':['transtats','Bureau of Transportation','nycflights13','2013']}
def clean(t):return ' '.join(t.split())
def scan(a):
 a=dict(a);start=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z');local=P/'cache'/a['archive_id'];cached_original=R/'cache'/a['archive_id']
 try:
  if local.exists():b=local.read_bytes();fetch='cached_followup'
  elif cached_original.exists():b=cached_original.read_bytes();fetch='cached_original'
  else:
   response=urllib.request.urlopen(a['url'],timeout=55);b=response.read();local.write_bytes(b);fetch='downloaded';a['status']=response.status;a['response_final_url']=response.url
  a.update(request_started_utc=start,response_completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),archive_sha256=hashlib.sha256(b).hexdigest(),archive_bytes=len(b),fetch_mode=fetch)
  import io
  with tarfile.open(fileobj=io.BytesIO(b)) as tf:
   members=sorted(x.name for x in tf.getmembers() if x.isfile() and x.name.endswith('.html') and '/inst/doc/' in x.name)
   desc=tf.extractfile(a['project']+'/DESCRIPTION').read().decode();a['version']=re.search(r'^Version:\s*(.+)',desc,re.M)[1];a['publication_raw']=re.search(r'^Date/Publication:\s*(.+)',desc,re.M)[1]
   a['publication_utc']=datetime.datetime.strptime(a['publication_raw'],'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=datetime.timezone.utc).isoformat().replace('+00:00','Z')
   a['publication_description_sha256']=hashlib.sha256(desc.encode()).hexdigest();a['html_members']=members;a['documents']=[]
   (P/'excerpts'/f"{a['project']}-{a['version']}-publication.txt").write_text('\n'.join(x for x in desc.splitlines() if x.startswith(('Package:','Version:','Date:','Packaged:','Date/Publication:','Repository:')))+'\n')
   for ref in [x for x in REFS if x['consumer_project']==a['project']]:
    name=ref['member_path'];d=dict(reference_id=ref['reference_id'],member_path=name,original_member_present=name in members)
    if name in members:
     raw=tf.extractfile(name).read();s=raw.decode();dom=html.fromstring(raw)
     for e in dom.xpath('//script|//style'):e.drop_tree()
     text=clean(dom.text_content());d.update(member_sha256=hashlib.sha256(raw).hexdigest(),member_bytes=len(raw),body_text_sha256=hashlib.sha256(text.encode()).hexdigest(),old_href_present=ref['raw_href'] in dom.xpath('//a/@href'),links=[],paragraphs=[])
     for x in dom.xpath('//body//a[@href]'):
      if any(k.lower() in (x.get('href')+' '+x.text_content()).lower() for k in KEYS[ref['reference_id']]):
       parent=x
       while parent.getparent() is not None and parent.tag not in ('p','li','dd','td'):parent=parent.getparent()
       line=x.sourceline;rawline=s.splitlines()[line-1]
       d['links'].append(dict(href=x.get('href'),text=clean(x.text_content()),line=line,paragraph=clean(parent.text_content()),raw_line=rawline if len(rawline)<20000 else rawline[:20000]))
     for x in dom.xpath('//p'):
      t=clean(x.text_content())
      if any(k.lower() in t.lower() for k in KEYS[ref['reference_id']]):d['paragraphs'].append(dict(line=x.sourceline,text=t))
     d['matching_html_other_members']=[]
    else:
     d['old_href_present']=False;d['matching_html_other_members']=[]
     # Search every available compiled HTML when path disappears; do not mistake filename removal for reference removal.
     for other in members:
      raw=tf.extractfile(other).read();dom=html.fromstring(raw)
      links=dom.xpath('//a/@href')
      matches=[u for u in links if any(k.lower() in u.lower() for k in KEYS[ref['reference_id']])]
      if matches:d['matching_html_other_members'].append({'member_path':other,'member_sha256':hashlib.sha256(raw).hexdigest(),'matching_hrefs':matches})
    a['documents'].append(d)
  return a
 except Exception as e:a.update(request_started_utc=start,error=repr(e));return a
names=sys.argv[1:]
selected=[a for a in INV if a['archive_id'] in names]
out=list(concurrent.futures.ThreadPoolExecutor(6).map(scan,selected))
for x in out:
 (P/'cache'/('scan-'+x['archive_id']+'.json')).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'archive':x['archive_id'],'publication_utc':x.get('publication_utc'),'error':x.get('error'),'documents':[{'id':d['reference_id'],'exists':d['original_member_present'],'old_href':d['old_href_present'],'links':[(l['href'],l['text']) for l in d.get('links',[])],'other':d.get('matching_html_other_members')} for d in x.get('documents',[])]},ensure_ascii=False))
