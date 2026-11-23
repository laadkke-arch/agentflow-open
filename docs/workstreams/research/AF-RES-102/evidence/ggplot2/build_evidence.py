from pathlib import Path
import sys,json,concurrent.futures,tarfile,io,hashlib
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import collect
ed=json.loads((D/'editions.json').read_text());jobs=[]
for k in ['old','new']:
 for r in ['source_sha','publication_sha']:
  sha=ed[k][r];tag=f'{k}-{r}'
  jobs.extend([(f'{tag}-runs',collect.API+'actions/runs?head_sha='+sha+'&per_page=100'),(f'{tag}-checks',collect.API+'commits/'+sha+'/check-runs?per_page=100'),(f'{tag}-status',collect.API+'commits/'+sha+'/status')])
 jobs.append((k+'-pkgdown-workflow',collect.RAW+ed[k]['source_sha']+'/.github/workflows/pkgdown.yaml'))
 jobs.append((k+'-pkgdown-config',collect.RAW+ed[k]['source_sha']+'/_pkgdown.yml'))
 jobs.append((k+'-package-description',collect.RAW+ed[k]['source_sha']+'/DESCRIPTION'))
 jobs.append((k+'-distribution',f'https://cran.r-project.org/src/contrib/Archive/ggplot2/ggplot2_{ed[k]["version"]}.tar.gz'))
for k,win in [('old','2022-11-06..2022-11-10'),('new','2024-02-22..2024-02-25')]:jobs.append((k+'-created-window-runs',collect.API+'actions/runs?created='+win+'&per_page=100'))
def read(j):
 key,url=j
 try:
  b,r=collect.fetch(key,url)
  summary={'key':key,'receipt':f'evidence/ggplot2/receipts/{key}.json','url':url,'accessed_utc':r['accessed_utc'],'sha256':r['sha256'],'bytes':len(b),'status':r['status']}
  if key.endswith('-runs'):
   data=json.loads(b);summary.update(total_count=data.get('total_count'),runs=[{k:x.get(k) for k in ['id','name','head_sha','event','status','conclusion','created_at','updated_at','html_url','jobs_url','artifacts_url']} for x in data.get('workflow_runs',[])])
  elif key.endswith('-checks'):
   data=json.loads(b);summary.update(total_count=data.get('total_count'),checks=[{k:x.get(k) for k in ['id','name','head_sha','status','conclusion','started_at','completed_at','details_url','output','check_suite']} for x in data.get('check_runs',[])])
  elif key.endswith('-status'):
   data=json.loads(b);summary.update(state=data.get('state'),total_count=data.get('total_count'),statuses=[{k:x.get(k) for k in ['id','state','description','target_url','context','created_at','updated_at']} for x in data.get('statuses',[])])
  elif key.endswith('-distribution'):
   with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as tar:
    members=tar.getmembers();names=[x.name for x in members];summary.update(members=len(names),member_names=names)
    ins=[]
    for p in ['ggplot2/DESCRIPTION','ggplot2/man/expansion.Rd','ggplot2/man/geom_count.Rd','ggplot2/man/annotation_custom.Rd','ggplot2/man/geom_histogram.Rd']:
     d=tar.extractfile(p).read();ins.append({'path':p,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()})
    summary['read_members']=ins;summary['html_reference_members']=[x for x in names if '/reference/' in x and x.endswith('.html')]
  else:summary['text']=b.decode()
  return summary
 except Exception as e:return {'key':key,'url':url,'error':repr(e),'receipt':f'evidence/ggplot2/receipts/{key}.json'}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for r in ex.map(read,jobs):
  results.append(r);print(json.dumps({k:v for k,v in r.items() if k not in ['text','member_names','checks','statuses','runs']},ensure_ascii=False),flush=True)
(D/'cache/build-full.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
compact=[]
for r in results:
 q={k:v for k,v in r.items() if k not in ['text','member_names','checks']}
 if 'text' in r:q['line_count']=len(r['text'].splitlines())
 if 'checks' in r:q['checks']=[{k:v for k,v in x.items() if k!='output'} for x in r['checks']]
 compact.append(q)
(D/'build-search.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2))
