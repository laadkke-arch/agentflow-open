import urllib.request,urllib.parse,json,pathlib,datetime,time,hashlib,html,re
P=pathlib.Path(__file__).resolve().parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url):
 t=now()
 with urllib.request.urlopen(url,timeout=45) as r:
  b=r.read();d=json.loads(b)
 if d.get('backoff'):time.sleep(d['backoff'])
 return d,{'url':url,'checked_utc':t,'finished_utc':now(),'status':200,'transport_sha256':hashlib.sha256(b).hexdigest(),'backoff':d.get('backoff'),'has_more':d.get('has_more'),'quota_remaining':d.get('quota_remaining')}
fields=['.items','.has_more','.quota_remaining','.backoff','revision.body','revision.creation_date','revision.revision_guid','revision.revision_number','revision.revision_type','revision.post_id','revision.title']
u='https://api.stackexchange.com/2.3/filters/create?'+urllib.parse.urlencode({'include':';'.join(fields),'base':'none','unsafe':'true'})
d,rc=get(u);f=d['items'][0]['filter'];rc.update(filter=f,included_fields=d['items'][0]['included_fields']);(P/'revision-filter.json').write_text(json.dumps(rc,indent=2))
rows=json.loads((P/'recruitment-h1.json').read_text())['items'];allrev=[];receipts=[]
for i in range(0,len(rows),10):
 ids=';'.join(str(x['question_id']) for x in rows[i:i+10]);page=1
 while True:
  u='https://api.stackexchange.com/2.3/posts/'+ids+'/revisions?'+urllib.parse.urlencode({'site':'stackoverflow','pagesize':100,'page':page,'filter':f})
  d,rc=get(u);receipts.append(rc);allrev.extend(d.get('items',[]))
  print('batch',i,'page',page,'items',len(d.get('items',[])),'more',d.get('has_more'),flush=True)
  if not d.get('has_more'):break
  page+=1
out=[]
for n,q in enumerate(rows,1):
 r=[x for x in allrev if x.get('post_id')==q['question_id'] and 'body' in x]
 r.sort(key=lambda x:(x.get('creation_date',0),x.get('revision_number',999999),x.get('revision_guid','')))
 z=dict(q,original_rank=n)
 if r:
  t=r[0];z.update(t);z['question_creation_date']=q['creation_date'];z['earliest_is_creation_timestamp']=t.get('creation_date')==q['creation_date'];z['body_sha256']=hashlib.sha256(t['body'].encode()).hexdigest();z['body_text']=html.unescape(re.sub('<[^>]+>',' ',t['body']));z['r0_url']='https://stackoverflow.com/revisions/'+t['revision_guid']+'/view-source';z['all_body_revision_count']=len(r)
 else:z['missing']='No body-bearing revision returned'
 out.append(z)
(P/'r0-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
(P/'_cache'/'r0-bodies.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('stored',len(out),'questions')
