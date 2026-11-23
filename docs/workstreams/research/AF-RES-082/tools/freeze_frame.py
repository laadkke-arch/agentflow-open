import urllib.request,json,datetime,hashlib,csv,concurrent.futures,pathlib
D=pathlib.Path(__file__).resolve().parents[1]
def get_org(org):
 rows=[]; receipts=[]
 for page in range(1,10):
  url=f'https://api.github.com/orgs/{org}/repos?type=public&per_page=100&page={page}'
  now=datetime.datetime.now(datetime.timezone.utc).isoformat()
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-082-public-research','Accept':'application/vnd.github+json'})
  with urllib.request.urlopen(req,timeout=45) as r:
   raw=r.read(); data=json.loads(raw); receipt={'url':url,'opened_at_utc':now,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'http_status':r.status,'sha256':hashlib.sha256(raw).hexdigest(),'entries':len(data),'etag':r.headers.get('ETag'),'link':r.headers.get('Link')}
  receipts.append(receipt)
  for x in data:
   if not x['fork'] and not x['private']: rows.append({k:x.get(k) for k in ['id','name','full_name','language','fork','private','archived','created_at','pushed_at','default_branch','html_url']})
  if len(data)<100: break
 rows=sorted(rows,key=lambda r:(r['name'].casefold(),r['name']))
 for i,row in enumerate(rows,1): row['org']=org;row['original_rank']=i;row['status']='not_yet_screened';row['last_2024_2025_formal_tag']='';row['case_id']='';row['exclusion_reason']=''
 (D/'evidence'/f'{org}-frame.json').write_text(json.dumps({'org':org,'receipts':receipts,'ordering':'casefold(name), then name','selection':'public and non-fork','repositories':rows},ensure_ascii=False,indent=2)+'\n')
 return rows
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex: groups=list(ex.map(get_org,['pypa','r-lib']))
 fields=['org','original_rank','id','name','full_name','language','fork','private','archived','created_at','pushed_at','default_branch','html_url','last_2024_2025_formal_tag','case_id','status','exclusion_reason']
 with (D/'FRAME.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(sum(groups,[]))
 for rows in groups: print(rows[0]['org'],len(rows),[r['name'] for r in rows[:20]])
