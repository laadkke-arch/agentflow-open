"""Acquire Typst recruitment frame; only revision 1 is exposed to the analyst.
Full API downloads are transient in .cache/typst; receipts and sanitized projections
are preserved. Never prints scores, accepted answers, or later revision bodies.
"""
import datetime as dt, hashlib, json, pathlib, sys, time, urllib.request, urllib.error
BASE=pathlib.Path(__file__).resolve().parents[2]
OUT=BASE/'evidence/typst'; CACHE=BASE/'.cache/typst'
OUT.mkdir(parents=True,exist_ok=True); CACHE.mkdir(parents=True,exist_ok=True)
receipts=[]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def fetch(url,name):
    path=CACHE/(name+'.json')
    start=now()
    try:
        with urllib.request.urlopen(url,timeout=45) as r:
            raw=r.read(); status=r.status
        path.write_bytes(raw); d=json.loads(raw)
    except Exception as e:
        rec={'url':url,'utc':start,'error':repr(e),'name':name}
        with (OUT/'failures.jsonl').open('a') as f: f.write(json.dumps(rec)+'\n')
        raise
    rec={'url':url,'utc':start,'status':status,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'items':len(d.get('items',[])),'has_more':d.get('has_more'),'quota_remaining':d.get('quota_remaining'),'backoff':d.get('backoff'),'cache_name':path.name}
    receipts.append(rec)
    (OUT/'acquisition.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
    if d.get('backoff'): time.sleep(min(d['backoff'],60))
    if d.get('error_id'): raise RuntimeError(d)
    return d
window=sys.argv[1] if len(sys.argv)>1 else 'h1'
a,b=(1704067200,1719791999) if window=='h1' else (1719792000,1735689599)
u=f'https://api.stackexchange.com/2.3/questions?site=stackoverflow&tagged=typst&fromdate={a}&todate={b}&sort=creation&order=asc&pagesize=60&filter=default'
d=fetch(u,'questions-'+window)
qs=sorted(d['items'],key=lambda q:(q['creation_date'],q['question_id']))[:60]
projections=[{k:q.get(k) for k in ['question_id','creation_date','tags','title','link','owner','content_license']} for q in qs]
(CACHE/('frame-meta-'+window+'.json')).write_text(json.dumps(projections,ensure_ascii=False,indent=2))
ids=';'.join(str(q['question_id']) for q in qs)
revs=[]
for page in range(1,11):
    u=f'https://api.stackexchange.com/2.3/posts/{ids}/revisions?site=stackoverflow&filter=withbody&pagesize=100&page={page}'
    r=fetch(u,'revisions-'+window+f'-{page}')
    revs.extend(r['items'])
    if not r.get('has_more'): break
else: raise RuntimeError('revision pagination exceeded declared cap; do not infer first revision')
first=[]
for i,q in enumerate(projections,1):
    rr=[r for r in revs if r.get('post_id')==q['question_id'] and r.get('revision_number')==1 and r.get('revision_type')=='single_user']
    rr.sort(key=lambda r:(r['creation_date'],r.get('revision_guid','')))
    x={**q,'frame_rank':i,'window':window,'first_revision_found':bool(rr)}
    if rr:
        z=rr[0]
        x.update({'first_revision':z,'body_sha256':hashlib.sha256(z.get('body','').encode()).hexdigest(),'revision_url':f"https://stackoverflow.com/revisions/{z['revision_guid']}/view-source",'all_revision_count':sum(r.get('post_id')==q['question_id'] for r in revs),'current_vs_initial_title_different':q['title']!=z.get('title',q['title']),'current_vs_initial_tags_different':q['tags']!=z.get('tags',q['tags'])})
    first.append(x)
(CACHE/('initial-only-'+window+'.json')).write_text(json.dumps(first,ensure_ascii=False,indent=2))
print(json.dumps({'window':window,'count':len(qs),'revisions_count':len(revs),'first_found':sum(x['first_revision_found'] for x in first),'quota':receipts[-1]['quota_remaining'],'projected_file':str(CACHE/('initial-only-'+window+'.json'))},ensure_ascii=False))
