import urllib.request,urllib.parse,json,pathlib,datetime,hashlib,time,subprocess
P=pathlib.Path(__file__).parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts=[]
def fetch(url):
 start=now()
 try:
  r=urllib.request.urlopen(url,timeout=45);raw=r.read();d=json.loads(raw)
  receipts.append({'url':url,'started_utc':start,'finished_utc':now(),'status':r.status,'sha256':hashlib.sha256(raw).hexdigest(),'items':len(d.get('items',[])),'has_more':d.get('has_more')})
  if d.get('backoff'):time.sleep(d['backoff'])
  return d
 except Exception as e:
  receipts.append({'url':url,'started_utc':start,'finished_utc':now(),'error':repr(e)})
  P.joinpath('retrieval-receipts.json').write_text(json.dumps(receipts,indent=2));raise
base='https://api.stackexchange.com/2.3/'
qfields='.items;.has_more;.quota_remaining;.backoff;question.question_id;question.tags;question.creation_date'
rf='.items;.has_more;.quota_remaining;.backoff;revision.body;revision.creation_date;revision.is_rollback;revision.post_id;revision.revision_guid;revision.revision_number;revision.revision_type;revision.tags;revision.title'
fq=fetch(base+'filters/create?'+urllib.parse.urlencode({'include':qfields,'base':'none','unsafe':'false'}))['items'][0]['filter']
fr=fetch(base+'filters/create?'+urllib.parse.urlencode({'include':rf,'base':'none','unsafe':'false'}))['items'][0]['filter']
P.joinpath('filters.json').write_text(json.dumps({'question':{'filter':fq,'fields':qfields},'revision':{'filter':fr,'fields':rf}},indent=2))
params={'site':'stackoverflow','tagged':'pandoc','sort':'creation','order':'asc','fromdate':int(datetime.datetime(2025,7,1,tzinfo=datetime.timezone.utc).timestamp()),'todate':int(datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc).timestamp())-1,'pagesize':60,'filter':fq}
frame=fetch(base+'questions?'+urllib.parse.urlencode(params))
P.joinpath('frame-api-masked.json').write_text(json.dumps({'request':params,'response':frame},indent=2))
items=[];page=1;ids=';'.join(str(x['question_id']) for x in frame['items'])
while True:
 d=fetch(base+'posts/'+ids+'/revisions?'+urllib.parse.urlencode({'site':'stackoverflow','pagesize':100,'page':page,'filter':fr}))
 items.extend(d.get('items',[]))
 if not d.get('has_more'):break
 page+=1
out=[]
for row in sorted(frame['items'],key=lambda x:(x['creation_date'],x['question_id'])):
 matches=sorted([x for x in items if x.get('post_id')==row['question_id'] and x.get('body')],key=lambda x:(x.get('creation_date',10**15),x.get('revision_number',10**9),x.get('revision_guid','')))
 if matches:
  x=dict(matches[0]);body=x.pop('body');P.joinpath('_cache',str(row['question_id'])+'.html').write_text(body)
  out.append(dict(row,earliest_body_revision=x,body_sha256=hashlib.sha256(body.encode()).hexdigest(),body_characters=len(body),initial_creation_confirmed=x.get('creation_date')==row['creation_date'] and x.get('revision_number')==1,body_retrieved_utc=receipts[-1]['finished_utc']))
 else:out.append(dict(row,error='No preserved body returned in revisions'))
P.joinpath('r0-metadata.json').write_text(json.dumps(out,indent=2))
P.joinpath('retrieval-receipts.json').write_text(json.dumps(receipts,indent=2))
print(json.dumps({'rows':len(out),'has_more':frame.get('has_more'),'r0_bodies':sum('body_sha256'in x for x in out),'metadata':out},ensure_ascii=False,indent=2))
