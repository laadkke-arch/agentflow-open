import urllib.request,urllib.parse,re,html,json,csv,datetime,concurrent.futures,hashlib,pathlib
P=pathlib.Path(__file__).parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
 t=now()
 with urllib.request.urlopen(url,timeout=40) as r:
  data=r.read();return data.decode('utf-8'),{'opened_utc':t,'completed_utc':now(),'url':url,'final_url':r.geturl(),'http_status':r.status,'sha256_current_response':hashlib.sha256(data).hexdigest()}
items=[];indexes=[]
for issue in ['2022-1','2022-2']:
 url='https://journal.r-project.org/issues/'+issue+'/'
 raw,receipt=fetch(url);indexes.append(receipt)
 for i,(rel,title) in enumerate(re.findall(r'<a[^>]+href="([^" ]*/articles/[^" ]+)"[^>]*>(.*?)</a>',raw,re.S),1):
  items.append({'issue':issue,'toc_order':i,'url':urllib.parse.urljoin(url,rel).rstrip('/')+'/','title':html.unescape(re.sub('<[^>]+>',' ',title)).strip()})
def meta(row):
 try:
  raw,receipt=fetch(row['url'])
  doi=re.search(r'<meta name="citation_doi" content="([^"]+)"',raw)
  date=re.search(r'<meta name="citation_publication_date" content="([^"]+)"',raw)
  row.update(receipt);row['publication_date']=date.group(1).replace('/','-') if date else '미확인';row['doi']=doi.group(1) if doi else row['url'].strip('/').split('/')[-1]
 except Exception as e:row.update({'opened_utc':now(),'publication_date':'미확인','doi':row['url'].strip('/').split('/')[-1],'error':str(e)})
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:rows=list(ex.map(meta,items))
rows.sort(key=lambda r:(r['issue'],r['publication_date'],r['doi']))
for i,r in enumerate(rows,1):r['exposure_order']=i;r['within_first30']=i<=30;r['semantic_read']=False;r['selection']='not_screened_after_first3' if i>3 else 'pending_body_screen';r['outcome_exposure']='metadata_only; earlier accidental body exposure of RJ-2022-006/007/008 recorded separately'
(P/'frame_all_metadata.json').write_text(json.dumps({'index_receipts':indexes,'ordering':'issue chronological then article publication date then DOI; issue1 dates all must be confirmed','rows':rows},ensure_ascii=False,indent=2)+'\n')
with (P/'frame.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows[:30])
print(json.dumps([{k:r.get(k) for k in ['exposure_order','issue','doi','publication_date','title','error']} for r in rows],ensure_ascii=False,indent=2))
