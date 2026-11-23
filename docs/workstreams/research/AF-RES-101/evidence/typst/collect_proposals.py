"""Stage2: request-author material and outcome markers are never printed.
Creates a 30-day, third-party-only proposal projection from answer revisions and
public comments. Current comment bodies have no accessible edit history.
"""
import datetime as dt, hashlib, json, pathlib, time, urllib.request
BASE=pathlib.Path(__file__).resolve().parents[2]; OUT=BASE/'evidence/typst'; CACHE=BASE/'.cache/typst'
initial=json.loads((OUT/'initial-part.json').read_text()); byq={x['question_id']:x for x in initial}; bypost={q:q for q in byq}; receipts=[]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def fetch(url,name):
 t=now()
 try:
  with urllib.request.urlopen(url,timeout=45) as r: raw=r.read();status=r.status
  d=json.loads(raw); (CACHE/(name+'.json')).write_bytes(raw)
 except Exception as e:
  with (OUT/'proposals-failures.jsonl').open('a') as f:f.write(json.dumps({'url':url,'utc':t,'error':repr(e)})+'\n')
  raise
 rec={'url':url,'utc':t,'status':status,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'items':len(d.get('items',[])),'has_more':d.get('has_more'),'quota_remaining':d.get('quota_remaining'),'backoff':d.get('backoff'),'cache_name':name+'.json'}
 receipts.append(rec);(OUT/'proposals-acquisition.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
 if d.get('backoff'):
  if d['backoff']>60:raise RuntimeError('backoff greater than 60 seconds; resume separately')
  time.sleep(d['backoff'])
 if d.get('error_id'):raise RuntimeError(d)
 return d

def pages(url,name):
 ans=[]
 for page in range(1,11):
  d=fetch(url+'&page='+str(page),name+'-'+str(page));ans.extend(d['items'])
  if not d.get('has_more'):return ans
 raise RuntimeError('uncompleted pagination; cannot claim complete')
lo=min(x['creation_date'] for x in initial);hi=max(x['creation_date']+30*86400 for x in initial)
ids=';'.join(map(str,byq))
answers=pages(f'https://api.stackexchange.com/2.3/questions/{ids}/answers?site=stackoverflow&filter=withbody&sort=creation&order=asc&pagesize=100&fromdate={lo}&todate={hi}','proposals-answers')
for a in answers:bypost[a['answer_id']]=a['question_id']
# We can use all answer IDs for the comment endpoint; author and per-case windows
# are filtered BEFORE any body can reach the analyst. No accepted marker printed.
postids=';'.join(map(str,bypost))
comments=pages(f'https://api.stackexchange.com/2.3/posts/{postids}/comments?site=stackoverflow&filter=withbody&sort=creation&order=asc&pagesize=100&fromdate={lo}&todate={hi}','proposals-comments')
third_answers=[a for a in answers if a['creation_date']<=byq[a['question_id']]['creation_date']+30*86400 and a.get('owner',{}).get('user_id')!=byq[a['question_id']]['owner_user_id']]
aids=';'.join(str(a['answer_id']) for a in third_answers)
revs=pages(f'https://api.stackexchange.com/2.3/posts/{aids}/revisions?site=stackoverflow&filter=withbody&pagesize=100','proposals-answer-revisions') if aids else []
pro=[]
for a in third_answers:
 q=byq[a['question_id']];aid=a['answer_id'];end=q['creation_date']+30*86400
 rr=sorted([r for r in revs if r.get('post_id')==aid and r.get('body') is not None and q['creation_date']<=r['creation_date']<=end and r.get('user',{}).get('user_id')!=q['owner_user_id']],key=lambda r:(r['creation_date'],r.get('revision_number',0),r.get('revision_guid','')))
 for r in rr:
  pro.append({'case_id':q['case_id'],'question_id':q['question_id'],'kind':'answer_revision','post_id':aid,'created':r['creation_date'],'answer_created':a['creation_date'],'owner':a.get('owner',{}),'revision_author':r.get('user',{}),'body':r['body'],'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'url':f'https://stackoverflow.com/a/{aid}','fixed_url':f"https://stackoverflow.com/revisions/{r['revision_guid']}/view-source",'historical_scope':'body directly from a public revision within the 30-day window'})
for c in comments:
 q=byq[bypost[c['post_id']]]
 if q['creation_date']<=c['creation_date']<=q['creation_date']+30*86400 and c.get('owner',{}).get('user_id')!=q['owner_user_id']:
  pro.append({'case_id':q['case_id'],'question_id':q['question_id'],'kind':'comment','post_id':c['post_id'],'comment_id':c['comment_id'],'created':c['creation_date'],'owner':c.get('owner',{}),'body':c['body'],'body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),'url':f"https://stackoverflow.com/questions/{q['question_id']}#comment{c['comment_id']}_{c['post_id']}",'historical_scope':'current publicly returned comment body; creation within window; comment edit history unavailable'})
pro.sort(key=lambda x:(x['created'],x.get('comment_id',x['post_id']),x.get('revision_number',0)))
(CACHE/'proposals-third-party-only.json').write_text(json.dumps(pro,ensure_ascii=False,indent=2))
summary={'utc':now(),'answers_received_machine':len(answers),'comments_received_machine':len(comments),'answer_revisions_received_machine':len(revs),'third_party_answer_revision_projection_rows':sum(x['kind']=='answer_revision' for x in pro),'third_party_comment_projection_rows':sum(x['kind']=='comment' for x in pro),'question_author_material_model_exposed':False,'accepted_answer_markers_model_exposed':False,'current_answer_bodies_model_exposed':False,'outside_30day_bodies_model_exposed':False,'projected_file':str(CACHE/'proposals-third-party-only.json'),'pagination_complete':True,'last_quota_remaining':receipts[-1]['quota_remaining']}
(OUT/'proposals-exposure.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
