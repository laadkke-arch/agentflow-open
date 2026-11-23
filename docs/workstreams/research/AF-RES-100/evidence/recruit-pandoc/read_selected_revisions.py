import urllib.request,urllib.parse,json,pathlib,datetime,hashlib,concurrent.futures
P=pathlib.Path(__file__).parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
ids=[79692729,79701174,79703916,79714790]
rows=json.loads(P.joinpath('r0-metadata.json').read_text())
f=json.loads(P.joinpath('filters.json').read_text())['revision']['filter']
def read(x):
 g=x['earliest_body_revision']['revision_guid'];u='https://api.stackexchange.com/2.3/revisions/'+g+'?'+urllib.parse.urlencode({'site':'stackoverflow','filter':f});start=now()
 try:
  r=urllib.request.urlopen(u,timeout=45);raw=r.read();d=json.loads(raw);items=[a for a in d.get('items',[]) if a.get('revision_guid')==g and a.get('body')]
  assert len(items)==1
  body=items[0]['body'];P.joinpath('_cache',str(x['question_id'])+'.html').write_text(body)
  return {'question_id':x['question_id'],'revision_guid':g,'url':u,'started_utc':start,'finished_utc':now(),'status':r.status,'payload_sha256':hashlib.sha256(raw).hexdigest(),'body_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_chars':len(body),'body_bytes':len(body.encode()),'initial_revision_unchanged':hashlib.sha256(body.encode()).hexdigest()==x['body_sha256']}
 except Exception as e:return {'question_id':x['question_id'],'url':u,'started_utc':start,'finished_utc':now(),'error':repr(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:res=list(e.map(read,[x for x in rows if x['question_id'] in ids]))
P.joinpath('selected-revision-receipts.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
