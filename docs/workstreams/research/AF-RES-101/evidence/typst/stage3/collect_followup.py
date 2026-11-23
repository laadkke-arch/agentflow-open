"""Stage3 author follow-up acquisition after proposal/filter seal."""
import datetime as dt,hashlib,json,pathlib,time,urllib.request
BASE=pathlib.Path(__file__).resolve().parents[3];OUT=BASE/'evidence/typst/stage3';CACHE=BASE/'.cache/typst'
initial=json.loads((BASE/'evidence/typst/initial-part.json').read_text());byq={x['question_id']:x for x in initial};bypost={q:q for q in byq};receipts=[]
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def fetch(url,name):
 t=now()
 try:
  with urllib.request.urlopen(url,timeout=45) as r: raw=r.read();status=r.status
  d=json.loads(raw);(CACHE/(name+'.json')).write_bytes(raw)
 except Exception as e:
  with (OUT/'failures.jsonl').open('a') as f:f.write(json.dumps({'url':url,'utc':t,'error':repr(e)})+'\n')
  raise
 receipts.append({'url':url,'utc':t,'status':status,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'items':len(d.get('items',[])),'has_more':d.get('has_more'),'quota_remaining':d.get('quota_remaining'),'backoff':d.get('backoff'),'cache_name':name+'.json'})
 (OUT/'acquisition.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
 if d.get('backoff'):
  if d['backoff']>60:raise RuntimeError('backoff over60: resume separately')
  time.sleep(d['backoff'])
 if d.get('error_id'):raise RuntimeError(d)
 return d

def pages(url,name):
 out=[]
 for p in range(1,11):
  d=fetch(url+'&page='+str(p),name+'-'+str(p));out.extend(d['items'])
  if not d.get('has_more'):return out
 raise RuntimeError('pagination incomplete')
lo=min(x['creation_date'] for x in initial);hi=max(x['creation_date']+90*86400 for x in initial);ids=';'.join(map(str,byq))
answers=pages(f'https://api.stackexchange.com/2.3/questions/{ids}/answers?site=stackoverflow&filter=withbody&sort=creation&order=asc&pagesize=100&fromdate={lo}&todate={hi}','followup-answers')
for a in answers:bypost[a['answer_id']]=a['question_id']
postids=';'.join(map(str,bypost))
comments=pages(f'https://api.stackexchange.com/2.3/posts/{postids}/comments?site=stackoverflow&filter=withbody&sort=creation&order=asc&pagesize=100&fromdate={lo}&todate={hi}','followup-comments')
current=pages(f'https://api.stackexchange.com/2.3/questions/{ids}?site=stackoverflow&filter=withbody&pagesize=100','followup-current')
selfanswers=[a for a in answers if a.get('owner',{}).get('user_id')==byq[a['question_id']]['owner_user_id'] and byq[a['question_id']]['creation_date']<=a['creation_date']<=byq[a['question_id']]['creation_date']+90*86400]
aids=';'.join(str(a['answer_id']) for a in selfanswers)
selfrevs=pages(f'https://api.stackexchange.com/2.3/posts/{aids}/revisions?site=stackoverflow&filter=withbody&pagesize=100','followup-selfanswer-revisions') if aids else []
qrevs=[]
for f in sorted(CACHE.glob('revisions-h1-*.json')):qrevs.extend(json.loads(f.read_text())['items'])
events=[]
for c in comments:
 q=byq[bypost[c['post_id']]]
 if c.get('owner',{}).get('user_id')==q['owner_user_id'] and q['creation_date']<=c['creation_date']<=q['creation_date']+90*86400:
  events.append({'case_id':q['case_id'],'question_id':q['question_id'],'kind':'author_comment','created':c['creation_date'],'post_id':c['post_id'],'comment_id':c['comment_id'],'body':c['body'],'body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),'url':f"https://stackoverflow.com/questions/{q['question_id']}#comment{c['comment_id']}_{c['post_id']}",'historical_limit':'current comment text; creation within90days, edit history not available'})
for r in qrevs:
 if r.get('post_id') not in byq:continue
 q=byq[r['post_id']]
 if r.get('revision_number',0)>1 and r.get('user',{}).get('user_id')==q['owner_user_id'] and q['creation_date']<=r['creation_date']<=q['creation_date']+90*86400:
  events.append({'case_id':q['case_id'],'question_id':q['question_id'],'kind':'author_question_revision','created':r['creation_date'],'post_id':r['post_id'],'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'body':r.get('body'),'body_sha256':hashlib.sha256(r.get('body','').encode()).hexdigest(),'revision_comment':r.get('comment'),'url':f"https://stackoverflow.com/revisions/{r['revision_guid']}/view-source",'historical_limit':'explicit revision record inside90daywindow; body may be absent on tag-only edit'})
for r in selfrevs:
 aq=next((a for a in selfanswers if a['answer_id']==r.get('post_id')),None)
 if not aq:continue
 q=byq[aq['question_id']]
 if q['creation_date']<=r['creation_date']<=q['creation_date']+90*86400:
  events.append({'case_id':q['case_id'],'question_id':q['question_id'],'kind':'author_self_answer_revision','created':r['creation_date'],'post_id':r['post_id'],'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'body':r.get('body'),'body_sha256':hashlib.sha256(r.get('body','').encode()).hexdigest(),'revision_author':r.get('user',{}),'url':f"https://stackoverflow.com/revisions/{r['revision_guid']}/view-source",'answer_url':f"https://stackoverflow.com/a/{r['post_id']}",'historical_limit':'self-answer revision inside90days; verify edit author before assigning behavior'})
events.sort(key=lambda x:(x['created'],x.get('comment_id',x['post_id']),x.get('revision_number',0)))
(CACHE/'followup-author-only.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
(CACHE/'followup-current-questions.json').write_text(json.dumps(current,ensure_ascii=False,indent=2))
summary={'utc':now(),'phase':'after_stage2_remote_seal_4e7539906eb03abd46e6910643ed5317f97ddb45','answers_received':len(answers),'comments_received':len(comments),'selfanswers_received':len(selfanswers),'selfanswer_revisions_received':len(selfrevs),'author_events_projected':len(events),'question_revisions_reused':{'cache_file':'revisions-h1-1.json','initial_acquisition_receipt':'../acquisition.json','new_fetch':False},'pagination_complete':True,'current_status_available_after_seal':True,'last_quota':receipts[-1]['quota_remaining']}
(OUT/'exposure.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
