import urllib.request,urllib.error,json,datetime,pathlib,hashlib,concurrent.futures
B=pathlib.Path(__file__).resolve().parent
v=json.loads((B/'versions.json').read_text()); cache=B/'.workbench'/'postseal';cache.mkdir(exist_ok=True)
paths={'statsmodels/statsmodels':['docs/source/gam.rst','docs/source/gee.rst','statsmodels/gam/smooth_basis.py','statsmodels/genmod/generalized_estimating_equations.py','requirements.txt'],'astropy/astropy':['docs/convolution/kernels.rst','docs/modeling/fitting.rst','docs/modeling/physical_models.rst','astropy/modeling/tests/test_blackbody.py','astropy/modeling/physical_models.py','setup.cfg'],'scikit-learn/scikit-learn':['doc/modules/model_evaluation.rst','examples/model_selection/plot_precision_recall.py','sklearn/metrics/_ranking.py','sklearn/_min_dependencies.py']}
items=[(row,path) for row in v['rows'] if row['role']!='old' for path in paths[row['repository']]]
def fetch(it):
 row,path=it; url=f'https://raw.githubusercontent.com/{row["repository"]}/{row["commit"]}/{path}'
 out={'repository':row['repository'],'tag':row['tag'],'commit':row['commit'],'role':row['role'],'path':path,'url':url,'requested_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seal_commit':'35d7e18024cced8cc81f9397b65e90e0e74bb907'}
 try:
  with urllib.request.urlopen(url,timeout=45) as resp:raw=resp.read();out['status']=resp.status
  dst=cache/row['repository'].split('/')[0]/row['role']/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
  out.update({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'cache_path':str(dst.relative_to(B)),'acquired_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'countable_source':False,'note':'Acquired bytes; source ledger records actual section reading separately.'})
 except Exception as e:out.update({'status':getattr(e,'code',None),'error':str(e),'countable_source':False})
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:rows=list(ex.map(fetch,items))
(B/'postseal-acquisition.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
for r in rows:print(r['repository'],r['role'],r['path'],r.get('status'))
