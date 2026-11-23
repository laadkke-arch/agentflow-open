"""Stage 2 public acquisition; author followups and outcome fields are hidden."""
import datetime
import hashlib
import json
from pathlib import Path
import time
import urllib.request

BASE=Path(__file__).resolve().parents[2]
OUT=BASE/'evidence/imagemagick'
CACHE=BASE/'.cache/imagemagick/stage2'
CACHE.mkdir(parents=True,exist_ok=True)
initial=json.loads((OUT/'initial-part.json').read_text())
cases={x['question_id']:x for x in initial}
t0={qid:int(datetime.datetime.fromisoformat(c['created_at']).timestamp()) for qid,c in cases.items()}
cutoff={qid:t+30*86400 for qid,t in t0.items()}
receipt=[]

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pages(stem,path,query):
    acc=[]
    for page in range(1,21):
        url=f'https://api.stackexchange.com/2.3/{path}?site=stackoverflow&pagesize=100&page={page}&{query}'
        fetched=now()
        try:
            response=urllib.request.urlopen(url,timeout=45); raw=response.read();data=json.loads(raw)
        except Exception as error:
            (OUT/f'stage2-failure-{stem}-{page}.json').write_text(json.dumps({'url':url,'utc':fetched,'error':str(error)},ensure_ascii=False,indent=2));raise
        (CACHE/f'{stem}-{page}.json').write_bytes(raw)
        receipt.append({'stem':stem,'page':page,'url':url,'utc':fetched,'status':response.status,'response_sha256':hashlib.sha256(raw).hexdigest(),'items':len(data.get('items',[])),'has_more':data.get('has_more'),'quota_remaining':data.get('quota_remaining'),'backoff':data.get('backoff')})
        acc.extend(data.get('items',[]))
        if data.get('backoff'):
            if data['backoff']>60:raise RuntimeError('backoff >60, resume later')
            time.sleep(data['backoff'])
        if not data.get('has_more'):break
    else:raise RuntimeError('pagination incomplete')
    return acc

ids=';'.join(str(q) for q in cases)
datequery=f'fromdate={min(t0.values())}&todate={max(cutoff.values())}'
answers=pages('answers',f'questions/{ids}/answers',datequery+'&sort=creation&order=asc&filter=withbody')
answer_q={a['answer_id']:a['question_id'] for a in answers}
post_q={**{q:q for q in cases},**answer_q}
answer_nonop=[a for a in answers if a['creation_date']<=cutoff[a['question_id']] and a.get('owner',{}).get('user_id') is not None and a['owner']['user_id']!=cases[a['question_id']]['first_revision_author']['user_id']]
comments=pages('comments','posts/'+';'.join(str(p) for p in post_q)+'/comments',datequery+'&sort=creation&order=asc&filter=withbody')
revisions=[]
if answer_nonop:
    revisions=pages('answer-revisions','posts/'+';'.join(str(a['answer_id']) for a in answer_nonop)+'/revisions','filter=withbody')
projections=[]
for a in answer_nonop:
    qid=a['question_id']
    revs=[r for r in revisions if r.get('post_id')==a['answer_id'] and r.get('creation_date',0)<=cutoff[qid] and 'body' in r and r.get('user',{}).get('user_id')!=cases[qid]['first_revision_author']['user_id']]
    revs.sort(key=lambda r:(r['creation_date'],r.get('revision_number',0),r.get('revision_guid','')))
    for r in revs:
        projections.append({'kind':'answer_revision','case_id':cases[qid]['case_id'],'question_id':qid,'post_id':a['answer_id'],'time':r['creation_date'],'revision_number':r.get('revision_number'),'revision_guid':r['revision_guid'],'body':r['body'],'body_sha256':hashlib.sha256(r['body'].encode()).hexdigest(),'author':{k:v for k,v in a['owner'].items() if k in ['user_id','display_name']},'url':f'https://stackoverflow.com/a/{a["answer_id"]}','revision_url':f'https://stackoverflow.com/revisions/{a["answer_id"]}/{r.get("revision_number",1)}'})
for c in comments:
    qid=post_q[c['post_id']]
    if c['creation_date']>cutoff[qid]:continue
    uid=c.get('owner',{}).get('user_id')
    if uid is None or uid==cases[qid]['first_revision_author']['user_id']:continue
    projections.append({'kind':'comment','case_id':cases[qid]['case_id'],'question_id':qid,'post_id':c['post_id'],'comment_id':c['comment_id'],'time':c['creation_date'],'body':c['body'],'body_sha256':hashlib.sha256(c['body'].encode()).hexdigest(),'author':{k:v for k,v in c['owner'].items() if k in ['user_id','display_name']},'url':f'https://stackoverflow.com/questions/{qid}#comment{c["comment_id"]}_{c["post_id"]}','history_limit':'API exposes current comment body; edit history unavailable'})
projections.sort(key=lambda r:(r['time'],r.get('comment_id',r['post_id']),r.get('revision_number',0)))
(CACHE/'non-op-30day-projection.json').write_text(json.dumps(projections,ensure_ascii=False,indent=2))
(OUT/'stage2-acquisition.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
inventory=[]
for qid,c in cases.items():
    aa=[a for a in answers if a['question_id']==qid]
    cc=[co for co in comments if post_q[co['post_id']]==qid]
    inventory.append({'case_id':c['case_id'],'question_id':qid,'t0_utc':c['created_at'],'cutoff_utc':datetime.datetime.fromtimestamp(cutoff[qid],datetime.timezone.utc).isoformat(),'nonop_answer_ids':[a['answer_id'] for a in answer_nonop if a['question_id']==qid],'nonop_answer_first_revision_available':all(any(r.get('post_id')==a['answer_id'] and r.get('revision_number')==1 and 'body' in r for r in revisions) for a in answer_nonop if a['question_id']==qid),'nonop_comment_ids':[r['comment_id'] for r in projections if r['question_id']==qid and r['kind']=='comment'],'author_outcomes_or_acceptance_displayed':False,'note':'All current raw answer/comment objects retained in ignored cache; owner self posts/current statuses/late revisions suppressed before projection. Counts of suppressed author material are intentionally not exposed before seal.'})
(OUT/'stage2-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print(json.dumps({'cases':len(inventory),'nonop_projection_events':len(projections),'pages':len(receipt),'quotas':[x['quota_remaining'] for x in receipt]},ensure_ascii=False))
