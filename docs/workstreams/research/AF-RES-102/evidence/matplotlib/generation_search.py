import json,concurrent.futures,urllib.parse,datetime
from fetch import get,ROOT
from audit_main import cached
T=[('old-source','matplotlib/matplotlib','c23ccdde6f0f8c071b09a88770e24452f2859e99'),('old-doc','matplotlib/matplotlib','655f616e86e2c0f7724d7c88717d4ac4eb438c57'),('old-pub','matplotlib/matplotlib.github.com','f3ac5407f8ffc861cae1ea87eddd06c63b222e4b'),('new-source','matplotlib/matplotlib','d6dd1b79142e4e2483244c25ff1e3ddb664722d3'),('new-doc','matplotlib/matplotlib','235131a6bc2527aee7eea370fd5f94564a48c20d'),('new-pub','matplotlib/matplotlib.github.com','410d8388303fab638bbedbd1d2eace0e5efb0de9')]
J=[]
for label,repo,sha in T:
 for kind,tail in [('actions','actions/runs?head_sha='+sha+'&per_page=100&page=1'),('status','commits/'+sha+'/status'),('checks','commits/'+sha+'/check-runs?per_page=100&page=1')]:J.append((f'gen-{label}-{kind}',f'https://api.github.com/repos/{repo}/{tail}',label,kind,sha))
for label,repo,dates in [('old-source-window','matplotlib/matplotlib','2023-01-11..2023-01-14'),('old-pub-window','matplotlib/matplotlib.github.com','2023-01-11..2023-01-14'),('new-source-window','matplotlib/matplotlib','2023-02-13..2023-02-16'),('new-pub-window','matplotlib/matplotlib.github.com','2023-02-13..2023-02-16')]:J.append(('gen-'+label,f'https://api.github.com/repos/{repo}/actions/runs?created={dates}&per_page=100&page=1',label,'window',dates))
def run(j):
 key,url,label,kind,target=j;b,r=cached(key,url,'Q5 bounded exact SHA or created-date-window run/status/check lookup; outputs require separate direct link')
 try:d=json.loads(b)
 except:d={}
 out={'id':key,'url':url,'utc':r['utc'],'http_status':r['status'],'sha256':r['sha256'],'target':target,'kind':kind,'receipt':'evidence/matplotlib/receipts/'+key+'.json'}
 if r['status']!=200:out['failure']=d.get('message',str(b[:150]));out['assessment']='Access failure, not no-build evidence'
 elif kind in ['actions','window']:
  runs=d.get('workflow_runs',[]);out['total_count']=d.get('total_count');out['returned_count']=len(runs);out['runs']=[{k:x.get(k) for k in ['id','name','path','head_branch','head_sha','event','status','conclusion','created_at','updated_at','html_url','artifacts_url','jobs_url']} for x in runs];out['assessment']='Retained listing only; empty means no visible retained run in queried scope, not proof no historic job'
 elif kind=='status':
  out['state']=d.get('state');out['total_count']=d.get('total_count');out['statuses']=[{k:x.get(k) for k in ['context','state','target_url','created_at','updated_at','description']} for x in d.get('statuses',[])];out['assessment']='Commit status provenance only; does not identify payload digest unless linked job supplies it'
 else:
  checks=d.get('check_runs',[]);out['total_count']=d.get('total_count');out['returned_count']=len(checks);out['checks']=[{k:x.get(k) for k in ['id','name','head_sha','details_url','html_url','status','conclusion','started_at','completed_at']} for x in checks];out['assessment']='Check records only; output artifacts/manifests need direct examination'
 print(key,out['http_status'],out.get('total_count'),out.get('state'),flush=True)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:A=list(ex.map(run,J))
(ROOT/'generation-search.json').write_text(json.dumps({'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'six exact commits (source tag/docs revision/publication for each edition), plus four explicit Jan/Feb2023 created windows; API first page100; pagination must be expanded if total>returned','queries':A,'limitation':'GitHub Actions may not be release-doc build host; CircleCI devdocs and manual release copies distinguished by rules. Missing/403/retention cannot prove G=NO.'},ensure_ascii=False,indent=2)+'\n')
