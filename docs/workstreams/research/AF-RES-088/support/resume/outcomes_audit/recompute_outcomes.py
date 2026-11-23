"""Resume Q6 metadata/chronology audit. Does not write shared files or change judgments."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import json, hashlib
P=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
checks=[]; hashes={}
def read(base,name):
 b=(base/name).read_bytes(); hashes[str((base/name).relative_to(P))]=hashlib.sha256(b).hexdigest();return json.loads(b)
def req(ok,label,detail=None):
 checks.append({'check':label,'pass':bool(ok),'detail':detail})
def utc(t):return datetime.fromtimestamp(t,timezone.utc).isoformat().replace('+00:00','Z')
packet=read(P,'outcome_packet.json')
outcomes=[json.loads(l) for l in (P/'outcomes.jsonl').read_text().splitlines()]
revisions=[json.loads(l) for l in (P/'revisions.jsonl').read_text().splitlines()]
case={r['question_id']:r for r in revisions}
q={x['question_id']:x for x in read(OUT,'questions_reopened.json')['items']}
a={x['answer_id']:x for x in read(OUT,'answers_reopened.json')['items']}
rs=read(OUT,'answer_revisions_full_filter_reopened.json')['items']
cs=read(OUT,'comments_reopened.json')['items']
for name,key,new,fields in [('questions','question_id',list(q.values()),['creation_date','accepted_answer_id','answer_count']),('answers','answer_id',list(a.values()),['question_id','creation_date','body','is_accepted']),('answer_revisions','revision_guid',rs,['post_id','creation_date','revision_number','body','last_body','is_rollback']),('comments','comment_id',cs,['post_id','creation_date','body','edited'])]:
 old={x[key]:x for x in packet[name]};fresh={x[key]:x for x in new}
 req(set(old)==set(fresh),name+' same identities',{'before':len(old),'after':len(fresh)})
 differences=[]
 for ident in old.keys() & fresh.keys():
  for f in fields:
   if old[ident].get(f)!=fresh[ident].get(f):differences.append({'id':ident,'field':f})
 req(not differences,name+' same material fields',differences)
qa=[];answer_rows=[]
for qid,x in q.items():
 aa=sorted([v for v in a.values() if v['question_id']==qid],key=lambda v:(v['creation_date'],v['answer_id']))
 authored=next(y for y in outcomes if y['question_id']==qid)
 own=x['owner'].get('user_id');start=x['creation_date'];end=start+2592000
 children={qid}|{v['answer_id'] for v in aa};cm=[v for v in cs if v['post_id'] in children]
 ac=[v['answer_id'] for v in aa if v.get('is_accepted')]
 req(ac==([] if x.get('accepted_answer_id') is None else [x['accepted_answer_id']]),str(qid)+' accepted-id flag join')
 req(len(aa)==x['answer_count']==authored['answer_records'],str(qid)+' answer count join')
 ownc=[v for v in cm if own is not None and v.get('owner',{}).get('user_id')==own]
 req(len(ownc)==authored['author_followup_comments'],str(qid)+' comment actor join')
 post_answer=[]
 for rev in case[qid]['history_metadata']:
  if rev['has_body'] and rev.get('revision_number',0)>1 and start<=rev['creation_date']<=end and aa and rev['creation_date']>aa[0]['creation_date']:
   post_answer.append({'guid':rev['revision_guid'],'utc':utc(rev['creation_date']),'editor_user_id':rev.get('user',{}).get('user_id'),'questioner':own is not None and rev.get('user',{}).get('user_id')==own,'first_answerer':rev.get('user',{}).get('user_id')==aa[0].get('owner',{}).get('user_id')})
 for ans in aa:
  rr=sorted([r for r in rs if r['post_id']==ans['answer_id'] and 'body' in r],key=lambda r:(r['creation_date'],r['revision_number']))
  orig=next(t for t in authored['answers'] if t['answer_id']==ans['answer_id'])
  req(rr[0]['revision_guid']==orig['first_body_guid'],str(ans['answer_id'])+' earliest preserved GUID')
  req(rr[0]['creation_date']==ans['creation_date'],str(ans['answer_id'])+' creation vs first revision timestamp')
  req(hashlib.sha256(rr[0]['body'].encode()).hexdigest()==orig['first_body_sha256'],str(ans['answer_id'])+' earliest body digest')
  for prev,nxt in zip(rr,rr[1:]):req(nxt.get('last_body')==prev['body'],str(ans['answer_id'])+' last_body chain')
  answer_rows.append({'answer_id':ans['answer_id'],'first_guid':rr[0]['revision_guid'],'first_utc':utc(rr[0]['creation_date']),'same_creation_timestamp':True,'strict_initial_bytes':'unknown (grace edits possible)','current_accepted':ans.get('is_accepted',False),'acceptance_time':'unknown'})
 qa.append({'case_id':case[qid]['case_id'],'question_id':qid,'current_answers':len(aa),'answers_within30d':sum(start<=v['creation_date']<=end for v in aa),'comments':len(cm),'comments_within30d':sum(start<=v['creation_date']<=end for v in cm),'questioner_comments':len(ownc),'accepted_answer_id':x.get('accepted_answer_id'),'body_edits_after_answer_within30d':post_answer})
sol=read(OUT,'solution_control_revisions_reopened.json');sar=read(OUT,'solution_control_answer_revisions_reopened.json')
rmap={r['revision_number']:r for r in sol['items']};a0=min([r for r in sar['items'] if r['post_id']==60178790 and 'body' in r],key=lambda r:r['revision_number'])
req(rmap[6]['body'].startswith(rmap[5]['body']),'SC1 old requirements are exact prefix of solution-added body')
req(rmap[6]['user']['user_id']==rmap[5]['user']['user_id']==667049,'SC1 questioner edits')
req(rmap[6]['creation_date']-a0['creation_date']==100013,'SC1 answer precedes insertion 100013 seconds')
req(all(t in rmap[6]['body'] and t not in rmap[5]['body'] for t in ['while','reverse','join','tostring','-r']),'SC1 five new solution tokens')
req('Thanks for @peak' in rmap[6]['body'],'SC1 self-attributed answer use statement')
for name in ['no_response_control_answers_reopened.json','no_response_control_comments_reopened.json']:
 d=read(OUT,name);req(d.get('has_more') is False and len(d['items'])==0,name+' currently visible empty endpoint')
nr=read(OUT,'no_response_control_revisions_reopened.json');req(nr.get('has_more') is False and len(nr['items'])==1,'no-response control exactly one preserved revision')
res={'audit_id':'AF-RES-088-RESUME-Q6','utc':datetime.now(timezone.utc).isoformat(),'metadata_status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','scope':'Fresh API reacquisition comparison + authored metadata reconciliation; semantic report corrections recorded separately; no independent blinded judgment','checks':checks,'question_rows':sorted(qa,key=lambda v:v['case_id']),'answer_rows':answer_rows,'summary':{'questions':len(q),'answers':len(a),'answer_revisions':len(rs),'comments':len(cs),'questioner_comments':sum(x['questioner_comments'] for x in qa),'questioner_comment_cases':sum(x['questioner_comments']>0 for x in qa),'currently_accepted_questions':sum(x['accepted_answer_id'] is not None for x in qa),'body_edits_after_first_answer_in_30d_cases':sum(bool(x['body_edits_after_answer_within30d']) for x in qa),'author_body_edits_after_first_answer_in_30d':sum(sum(t['questioner'] for t in x['body_edits_after_answer_within30d']) for x in qa)},'input_sha256':hashes}
(OUT/'resume_outcome_audit.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'metadata_status':res['metadata_status'],'summary':res['summary'],'failed_checks':[x for x in checks if not x['pass']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(x['pass'] for x in checks) else 1)
