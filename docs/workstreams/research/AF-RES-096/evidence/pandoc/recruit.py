import urllib.request,urllib.parse,json,pathlib,datetime,hashlib,time
P=pathlib.Path(__file__).parent
P.joinpath('_cache').mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
frame=json.loads(P.joinpath('frame-api-masked-h1.json').read_text())['response']['items']
f=json.loads(P.joinpath('filter-revision.json').read_text())['response']['items'][0]['filter']
items=[]; receipts=[];ids=';'.join(str(x['question_id']) for x in frame)
page=1
while True:
 u='https://api.stackexchange.com/2.3/posts/'+ids+'/revisions?'+urllib.parse.urlencode({'site':'stackoverflow','pagesize':100,'page':page,'filter':f})
 start=now()
 try:
  r=urllib.request.urlopen(u,timeout=50);raw=r.read();d=json.loads(raw)
  receipts.append({'url':u,'started_utc':start,'finished_utc':now(),'status':r.status,'sha256':hashlib.sha256(raw).hexdigest(),'item_count':len(d.get('items',[])),'has_more':d.get('has_more'),'quota_remaining':d.get('quota_remaining'),'fields':['body','creation_date','is_rollback','post_id','revision_guid','revision_number','revision_type','tags','title'],'selection':'Only earliest body is emitted or retained; later bodies discarded inside adapter.'})
  items.extend(d.get('items',[]))
  if d.get('backoff'):time.sleep(d['backoff'])
  if not d.get('has_more'):break
  page+=1
 except Exception as e:
  receipts.append({'url':u,'started_utc':start,'finished_utc':now(),'error':repr(e)});break
out=[]
for row in frame:
 matches=[x for x in items if x.get('post_id')==row['question_id'] and x.get('body')]
 matches.sort(key=lambda x:(x.get('creation_date',10**15),x.get('revision_number',10**9),x.get('revision_guid','')))
 chosen=matches[0] if matches else None
 if chosen:
  b=chosen.pop('body');h=hashlib.sha256(b.encode()).hexdigest();P.joinpath('_cache',str(row['question_id'])+'.html').write_text(b)
  out.append(dict(row,earliest_body_revision=chosen,body_sha256=h,body_characters=len(b),initial_creation_confirmed=chosen.get('creation_date')==row['creation_date'] and chosen.get('revision_number')==1,body_retrieved_utc=receipts[-1]['finished_utc']))
 else:out.append(dict(row,error='No preserved body returned in revisions'))
P.joinpath('revision-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
P.joinpath('r0-metadata.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'metadata_rows':len(frame),'revision_items':len(items),'r0_bodies':len([x for x in out if 'body_sha256'in x]),'receipts':receipts},ensure_ascii=False,indent=2))
