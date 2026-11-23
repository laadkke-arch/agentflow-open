"""Stage 3: release the 90-day author evidence after the second remote seal."""
import datetime
import hashlib
import json
from pathlib import Path
import time
import urllib.request

BASE=Path(__file__).resolve().parents[3]
OUT=BASE/'evidence/imagemagick/stage3'
CACHE=BASE/'.cache/imagemagick/stage3/followup'
CACHE.mkdir(parents=True,exist_ok=True)
cs={x['question_id']:x for x in json.loads((BASE/'evidence/imagemagick/initial-part.json').read_text())}
t0={q:int(datetime.datetime.fromisoformat(c['created_at']).timestamp()) for q,c in cs.items()}
limit={q:t+90*86400 for q,t in t0.items()}
receipts=[]
def pages(stem,path,query):
    acc=[]
    for page in range(1,21):
        url=f'https://api.stackexchange.com/2.3/{path}?site=stackoverflow&pagesize=100&page={page}&{query}'
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            response=urllib.request.urlopen(url,timeout=45);raw=response.read();data=json.loads(raw)
        except Exception as error:
            (OUT/f'failure-{stem}-{page}.json').write_text(json.dumps({'url':url,'utc':utc,'error':str(error)},ensure_ascii=False,indent=2));raise
        (CACHE/f'{stem}-{page}.json').write_bytes(raw)
        receipts.append({'stem':stem,'page':page,'url':url,'utc':utc,'status':response.status,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'has_more':data.get('has_more'),'items':len(data.get('items',[])),'quota_remaining':data.get('quota_remaining')})
        acc.extend(data.get('items',[]))
        if data.get('backoff'):
            if data['backoff']>60:raise RuntimeError('backoff >60; pause')
            time.sleep(data['backoff'])
        if not data.get('has_more'):break
    else:raise RuntimeError('paging incomplete')
    return acc
date=f'fromdate={min(t0.values())}&todate={max(limit.values())}'
answers=pages('answers90','questions/'+';'.join(map(str,cs))+'/answers',date+'&sort=creation&order=asc&filter=withbody')
post_q={**{q:q for q in cs},**{a['answer_id']:a['question_id'] for a in answers}}
comments=pages('comments90','posts/'+';'.join(map(str,post_q))+'/comments',date+'&sort=creation&order=asc&filter=withbody')
self_answers=[a for a in answers if a['creation_date']<=limit[a['question_id']] and a.get('owner',{}).get('user_id')==cs[a['question_id']]['first_revision_author']['user_id']]
self_revs=pages('selfanswer-revisions','posts/'+';'.join(str(a['answer_id']) for a in self_answers)+'/revisions','filter=withbody') if self_answers else []
question_revs=[]
for p in (BASE/'.cache/imagemagick').glob('revisions-h1-*.json'):
    question_revs.extend(json.loads(p.read_text())['items'])
events=[]
for c in comments:
    q=post_q[c['post_id']]
    if c['creation_date']>limit[q] or c.get('owner',{}).get('user_id')!=cs[q]['first_revision_author']['user_id']:continue
    events.append({'kind':'author_comment','case_id':cs[q]['case_id'],'question_id':q,'post_id':c['post_id'],'comment_id':c['comment_id'],'time':c['creation_date'],'author':{k:v for k,v in c['owner'].items() if k in ['user_id','display_name']},'body':c['body'],'body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),'url':f'https://stackoverflow.com/questions/{q}#comment{c["comment_id"]}_{c["post_id"]}'})
for r in question_revs:
    q=r.get('post_id')
    if q not in cs or r.get('revision_number',1)==1 or r.get('creation_date',0)>limit[q] or 'body' not in r:continue
    events.append({'kind':'question_revision','case_id':cs[q]['case_id'],'question_id':q,'post_id':q,'time':r['creation_date'],'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'is_requester_editor':r.get('user',{}).get('user_id')==cs[q]['first_revision_author']['user_id'],'author':{k:v for k,v in r.get('user',{}).items() if k in ['user_id','display_name']},'body':r['body'],'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'url':f'https://stackoverflow.com/revisions/{q}/{r.get("revision_number",1)}'})
for r in self_revs:
    if 'body' not in r:continue
    q=post_q[r['post_id']]
    if r['creation_date']>limit[q]:continue
    events.append({'kind':'selfanswer_revision','case_id':cs[q]['case_id'],'question_id':q,'post_id':r['post_id'],'time':r['creation_date'],'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'body':r['body'],'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'url':f'https://stackoverflow.com/revisions/{r["post_id"]}/{r.get("revision_number",1)}'})
events.sort(key=lambda e:(e['time'],e.get('comment_id',e['post_id']),e.get('revision_number',0)))
(CACHE/'author-90day-projection.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
current=[]
for q,c in cs.items():
    rs=[r for r in question_revs if r.get('post_id')==q and 'body' in r]
    r=max(rs,key=lambda r:(r.get('revision_number',0),r.get('creation_date',0)))
    current.append({'case_id':c['case_id'],'question_id':q,'revision_number':r.get('revision_number'),'revision_guid':r.get('revision_guid'),'time':r.get('creation_date'),'body':r['body'],'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'initial_body_sha256':c['initial_body_sha256'],'body_changed':hashlib.sha256(r['body'].encode()).hexdigest()!=c['initial_body_sha256'],'url':f'https://stackoverflow.com/revisions/{q}/{r.get("revision_number",1)}'})
(CACHE/'current-question-projection.json').write_text(json.dumps(current,ensure_ascii=False,indent=2))
(OUT/'followup-acquisition.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
inventory=[]
for q,c in cs.items():
    inventory.append({'case_id':c['case_id'],'question_id':q,'t0_utc':c['created_at'],'cutoff_utc':datetime.datetime.fromtimestamp(limit[q],datetime.timezone.utc).isoformat(),'author_comment_ids':[e['comment_id'] for e in events if e['question_id']==q and e['kind']=='author_comment'],'question_revision_numbers':[e['revision_number'] for e in events if e['question_id']==q and e['kind']=='question_revision'],'self_answer_ids':[a['answer_id'] for a in self_answers if a['question_id']==q],'current_acceptance':{a['answer_id']:a.get('is_accepted') for a in answers if a['question_id']==q},'current_acceptance_limitation':'current API state; no acceptance timestamp and no awareness inference','raw_pagination_complete':all(not r['has_more'] for r in receipts),'deleted_content_limit':True})
(OUT/'followup-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps({'events':len(events),'current_body_changes':[x['case_id'] for x in current if x['body_changed']],'inventory':inventory,'quota':[r['quota_remaining'] for r in receipts]},ensure_ascii=False,indent=2))
