import urllib.request,json,concurrent.futures,datetime,pathlib
B=pathlib.Path(__file__).resolve().parent
specs=[('statsmodels/statsmodels','old','v0.12.1','2020-10-29T14:58:16Z','release.published_at'),('statsmodels/statsmodels','first','v0.12.2','2021-02-02T01:56:04Z','release.published_at'),('statsmodels/statsmodels','latest','v0.15.0','2026-08-27T06:44:51Z','release.published_at'),('astropy/astropy','old','v4.2','2020-11-25T07:20:49Z','annotated tagger date fallback; no GitHub Release'),('astropy/astropy','first','v4.0.5','2021-03-26T19:57:09Z','annotated tagger date fallback; maintenance line, no GitHub Release'),('astropy/astropy','latest','v8.0.3','2026-11-18T11:38:39Z','release.published_at'),('scikit-learn/scikit-learn','old','0.24.0','2020-12-22T16:55:16Z','release.published_at'),('scikit-learn/scikit-learn','first','0.24.1','2021-01-19T18:10:37Z','release.published_at'),('scikit-learn/scikit-learn','latest','1.9.1','2026-09-11T09:38:12Z','release.published_at')]
def run(t):
 repo,role,tag,date,basis=t; u=f'https://api.github.com/repos/{repo}/git/ref/tags/{tag}'
 d=json.load(urllib.request.urlopen(u,timeout=45)); obj=d['object']; tag_sha=obj['sha']; urls=[u]
 if obj['type']=='tag':
  urls.append(obj['url']); d=json.load(urllib.request.urlopen(obj['url'],timeout=45)); obj=d['object']
 return {'repository':repo,'role':role,'tag':tag,'commit':obj['sha'],'tag_object':tag_sha,'date':date,'date_basis':basis,'metadata_urls':urls,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'body_read':role=='old'}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: rows=list(ex.map(run,specs))
(B/'versions.json').write_text(json.dumps({'cutoff':'2026-11-23T13:30:00Z','upstream_boundary':{'release':'SciPy v1.6.0','published_at':'2020-12-31T15:02:43Z','url':'https://api.github.com/repos/scipy/scipy/releases/tags/v1.6.0','basis':'directly read release metadata; upstream source evidence supplied by root'},'rows':rows,'limit':'Astropy first followup is v4.0.5 maintenance line by chronological official-tag rule; it is not assumed descended from v4.2. Post-cutoff tag metadata inspected, contents not opened before proposal seal.'},indent=2)+'\n')
for r in rows:print(r['repository'],r['role'],r['tag'],r['commit'])
# Preserve full recruitment metadata in reproducible local scratch; publication uses concise selectors.
D=B/'.workbench'/'metadata';D.mkdir(exist_ok=True)
for name in ['statsmodels-releases.json','astropy-releases.json','scikit-learn-releases.json','astropy-v4-tag-metadata.json']:
 p=B/name
 if p.exists(): p.rename(D/name)
