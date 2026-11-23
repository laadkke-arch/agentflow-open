import pathlib,json,urllib.request,urllib.parse,datetime,hashlib,concurrent.futures,time
P=pathlib.Path(__file__).parent
QIDS=[79692729,79701174,79703916,79714790]
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
receipts=[]
def fetch(path,params,label):
 url='https://api.stackexchange.com/2.3/'+path+'?'+urllib.parse.urlencode({'site':'stackoverflow',**params});start=now()
 try:
  r=urllib.request.urlopen(url,timeout=50);raw=r.read();d=json.loads(raw)
  receipt={'label':label,'url':url,'started_utc':start,'finished_utc':now(),'status':r.status,'response_sha256':hashlib.sha256(raw).hexdigest(),'response_bytes':len(raw),'item_count':len(d.get('items',[])),'has_more':d.get('has_more'),'backoff':d.get('backoff')}
  receipts.append(receipt);P.joinpath('_cache',label+'.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
  if d.get('backoff'):time.sleep(d['backoff'])
  return d,receipt
 except Exception as e:
  receipt={'label':label,'url':url,'started_utc':start,'finished_utc':now(),'error':repr(e)};receipts.append(receipt);raise
ids=';'.join(map(str,QIDS))
requests=[('questions/'+ids,{'filter':'withbody','pagesize':100},'questions-current'),('questions/'+ids+'/answers',{'filter':'withbody','sort':'creation','order':'asc','pagesize':100},'answers-current'),('posts/'+ids+'/revisions',{'filter':'withbody','pagesize':100},'questions-revisions')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as e:results=list(e.map(lambda x:fetch(*x),requests))
questions,answers,qrev=[x[0]for x in results]
aids=[x['answer_id']for x in answers['items']]
allposts=QIDS+aids;allids=';'.join(map(str,allposts));requests=[('posts/'+allids+'/comments',{'filter':'withbody','sort':'creation','order':'asc','pagesize':100},'comments')]
if aids:requests.append(('posts/'+';'.join(map(str,aids))+'/revisions',{'filter':'withbody','pagesize':100},'answers-revisions'))
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as e:results2=list(e.map(lambda x:fetch(*x),requests))
# Pagination is explicit for every collection.
for path,params,label in requests:
 if not P.joinpath('_cache',label+'.json').exists():continue
 d=json.loads(P.joinpath('_cache',label+'.json').read_text());page=1
 while d.get('has_more'):
  page+=1;d,_=fetch(path,{**params,'page':page},label+'-page'+str(page))
# Initial collections also retain any additional pages.
for path,params,label in [('questions/'+ids,{'filter':'withbody','pagesize':100},'questions-current'),('questions/'+ids+'/answers',{'filter':'withbody','sort':'creation','order':'asc','pagesize':100},'answers-current'),('posts/'+ids+'/revisions',{'filter':'withbody','pagesize':100},'questions-revisions')]:
 d=json.loads(P.joinpath('_cache',label+'.json').read_text());page=1
 while d.get('has_more'):
  page+=1;d,_=fetch(path,{**params,'page':page},label+'-page'+str(page))
P.joinpath('retrieval-receipts.json').write_text(json.dumps(receipts,indent=2))
summary={'retrieved_utc':now(),'after_remote_seal2':'5d81bcbeb5f1248fc1dd2ce2d825cf6467353673','questions':[{k:x.get(k)for k in ['question_id','title','creation_date','last_edit_date','accepted_answer_id','answer_count','owner']}for x in questions['items']],'answers':[{k:x.get(k)for k in ['answer_id','question_id','creation_date','last_edit_date','is_accepted','owner']}for x in answers['items']],'collection_counts':{x['label']:x.get('item_count')for x in receipts},'cache_bodies_ignored_by_git':True}
P.joinpath('retrieval-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
