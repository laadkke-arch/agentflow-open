import urllib.request,urllib.parse,urllib.error,json,hashlib,time,datetime,pathlib,re,calendar
P=pathlib.Path(__file__).parent
rx=re.compile(r'timezone|time[\s_-]+zone|tzdata|\bDST\b|offset|daylight',re.I)
log=P/'search-log.jsonl'
def get(url,role='metadata'):
 for attempt in range(3):
  t=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:
   r=urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'AF-RES-063-public-research'}),timeout=40)
   data=r.read(); entry={'url':url,'opened_utc':t,'status':r.status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'role':role,'attempt':attempt+1}
   with log.open('a') as f:f.write(json.dumps(entry)+'\n')
   return json.loads(data)
  except Exception as e:
   with log.open('a') as f:f.write(json.dumps({'url':url,'opened_utc':t,'error':str(e),'role':role,'attempt':attempt+1})+'\n')
   if attempt==2:raise
   time.sleep(12)
def query(q,page=1):
 return get('https://api.github.com/search/issues?'+urllib.parse.urlencode({'q':q,'sort':'created','order':'asc','per_page':100,'page':page}))
def meta(x):return {k:x.get(k) for k in ['number','title','created_at','updated_at','html_url','state']}
if __name__=='__main__':
 union={}; queries=[]
 for term in ['timezone','"time zone"','tzdata','DST','offset','daylight']:
  q=f'repo:pandas-dev/pandas is:issue {term} in:title created:2021-01-01..2025-12-31'
  data=query(q);queries.append({'q':q,'total_count':data['total_count'],'incomplete_results':data.get('incomplete_results'),'returned':len(data['items'])})
  for x in data['items']:
   if rx.search(x['title']):union[x['number']]=meta(x)
  print('keyword',term,data['total_count'],flush=True)
 (P/'keyword-titles.json').write_text(json.dumps({'queries':queries,'titles':sorted(union.values(),key=lambda x:(x['created_at'],x['number']))},ensure_ascii=False,indent=2))
 titles=[]; matched={}; checks=[]
 for year in range(2021,2026):
  for month in range(1,13):
   q=f'repo:pandas-dev/pandas is:issue created:{year}-{month:02d}-01..{year}-{month:02d}-{calendar.monthrange(year,month)[1]}'
   for page in range(1,11):
    data=query(q,page);checks.append({'q':q,'page':page,'total_count':data['total_count'],'incomplete_results':data.get('incomplete_results'),'returned':len(data['items'])})
    for x in data['items']:
     row=meta(x);titles.append(row)
     if rx.search(row['title']):matched[row['number']]=row
    print('census',year,month,page,'matches',len(matched),flush=True)
    if len(data['items'])<100:break
   if len(matched)>=30:break
  if len(matched)>=30:break
 ordered=sorted(matched.values(),key=lambda x:(x['created_at'],x['number']))
 frame=ordered[:30]
 correction=[x for x in frame if x['number'] not in union]
 sealed={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'body_read_before_seal':False,'regex':rx.pattern,'census_rows':len(titles),'checks':checks,'first30':frame,'keyword_query_missing_before_correction':correction,'correction':'Keywordless chronological title census is authoritative. No body content read during metadata collection.'}
 (P/'title-census.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2))
 (P/'frame-seal.json').write_text(json.dumps(sealed,ensure_ascii=False,indent=2))
 print(json.dumps(sealed,ensure_ascii=False,indent=2))
