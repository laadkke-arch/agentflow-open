from pathlib import Path
import json,csv,datetime,urllib.parse,hashlib
P=Path(__file__).parent

def canonical(u):
 p=urllib.parse.urlsplit(u); qs=urllib.parse.parse_qsl(p.query,keep_blank_values=True);qs=[(k,v) for k,v in qs if k not in ['hl','locale','curius','utm_source','utm_campaign','utm_medium']]
 return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path.rstrip('/'),urllib.parse.urlencode(qs),''))

def build():
 routes=[json.loads(f.read_text()) for f in sorted(P.joinpath('routes').glob('*.json'))]
 sdict={};cs=[];rets=[];logs=[]
 for rt in routes:
  q=rt['question_id'];route=rt['route'];source_by_id={s['source_id']:s for s in rt['sources']};chosen_urls={canonical(s['url']):s for s in rt['sources']};seen={}
  for s in rt['sources']:
   receipt=json.loads(P.joinpath('receipts',s['receipt_ids'][0]+'.json').read_text())
   current={'source_id':s['source_id'],'title':s['title'],'source_url':s['url'],'version':s['version'],'published_or_revised':s.get('published_or_revised',s['version']),'checked_utc':receipt['finished_utc'],'sections_read':s['sections'],'verified_content':s['observation'],'limitations':s['limitation'],'producer':s['producer'],'lineage_id':s.get('lineage_id',canonical(s['url'])),'count_in_minimum':s.get('count_in_minimum',True),'count_reason':s.get('count_reason','공식/작성자 후보 원문 직접 판독; 스니펫/metadata를 산입하지 않음'),'related_questions':[q,'Q3','Q4'],'source_category':'candidate_provider','receipt_ids':s['receipt_ids'],'observation_type':'provider_statement'}
   if s['source_id'] in sdict:
    old=sdict[s['source_id']];old['related_questions']=sorted(set(old['related_questions']+current['related_questions']));old['receipt_ids']=sorted(set(old['receipt_ids']+current['receipt_ids']))
   else:sdict[s['source_id']]=current
  query_map={}
  for rid in rt['queries']:
   rec=json.loads(P.joinpath('receipts',rid+'.json').read_text());qi=int(rid.rsplit('-',1)[1]);raw=rec['request']['system1_search_query'][0]['q'];query_map[qi]=raw
   common={'question_id':q,'route':route,'query_index':qi,'request_utc':rec['started_utc'],'finished_utc':rec['finished_utc'],'query':raw,'engine':'system1_search_query','response_length':'long','receipt_id':rid,'returned_count':rec['provided_result_count'],'engine_absolute_rank':'unknown','wall_seconds':rec['wall_seconds']}
   logs.append({**common,'event_type':'search_request','observed_rank':'','url':'','title':'','ref_id':'','selection':'observed','reason':'first min(10,provided) only eligible; no invented ranks','canonical_url':'','source_id':'','error':str(rec['isError'])})
   manual=rt.get('result_annotations',{})
   for res in rec['results']:
    u=res['url'];cu=canonical(u);rank=res['provided_rank'];key=f'{qi}:{rank}';sr=chosen_urls.get(cu)
    if rank>10:sel='out_of_budget_exposure';reason='provided rank beyond first10; not used'
    elif cu in seen:sel='duplicate';reason='same canonical source as '+seen[cu]
    elif key in manual:sel=manual[key]['selection'];reason=manual[key]['reason']
    elif sr:sel='opened';reason='first eligible original within5-document budget'
    else:sel='not_opened';reason='5-original budget exhausted or ineligible; see selection_note and manual annotations'
    seen.setdefault(cu,key)
    logs.append({**common,'event_type':'search_result','observed_rank':rank,'url':u,'title':res['title'],'ref_id':res['ref_id'],'selection':sel,'reason':reason,'canonical_url':cu,'source_id':sr['source_id'] if sr else'','error':''})
  for s in rt['sources']:
   for j,rid in enumerate(s['receipt_ids']):
    rec=json.loads(P.joinpath('receipts',rid+'.json').read_text());req=rec['request'];kind='open_attempt' if j==0 else('retry' if 'retry' in rid else 'same_original_section_read')
    logs.append({'question_id':q,'route':route,'query_index':'','request_utc':rec['started_utc'],'finished_utc':rec['finished_utc'],'query':'','engine':'search_service_web_run','response_length':req.get('response_length',''),'receipt_id':rid,'returned_count':'','engine_absolute_rank':'unknown','wall_seconds':rec['wall_seconds'],'event_type':kind,'observed_rank':'','url':s['url'],'title':s['title'],'ref_id':rec['results'][0]['ref_id'] if rec['results'] else'','selection':'opened' if not rec['isError'] else'failed','reason':'same original continuation does not add a unique document' if j else 'unique candidate original open','canonical_url':canonical(s['url']),'source_id':s['source_id'],'error':str(rec['isError'])})
  byid={}
  for c in rt['candidates']:
   e=[]
   for sid in c['source_ids']:
    s=source_by_id[sid]
    e += [{'source_id':sid,'url':s['url'],'section':section} for section in s['sections']]
   predicates=list(c['condition_findings']);missing=c.get('missing_conditions',[]);required=[]
   for pred in predicates:
    for x in e:required.append({'condition_id':pred,**x,'sufficient_for_condition':pred not in missing})
   obj={**c,'question_id':q,'route':route,'mandatory_predicates':predicates,'required_bundle':required,'returned_citations':c.get('returned_citations',e),'opened_evidence':e,'opened_complete':c.get('opened_complete',not missing),'cited_complete':c.get('cited_complete',not missing),'conflict_or_hold_reason':' | '.join(c['condition_findings'][pred] for pred in missing),'current_version':'; '.join(source_by_id[sid]['version'] for sid in c['source_ids']),'historical_version':c.get('historical_version','unknown'),'search_receipt_ids':rt['queries'],'source_ids':c['source_ids'],'empty_reason':'','canonical_target':c.get('canonical_target',c['target_name']),'behavior':c.get('behavior',c['proposed_use']),'use_boundary':c['proposed_use'],'return_frozen_utc':rt['completed_utc']}
   cs.append(obj);byid[c['candidate_id']]=obj
  for rank in range(1,4):
   cand=rt['return_candidate_ids'][rank-1] if rank<=len(rt['return_candidate_ids']) else None
   if cand:rets.append({**byid[cand],'rank':rank})
   else:rets.append({'question_id':q,'route':route,'rank':rank,'candidate_id':'','target_name':'','candidate_class':'empty','proposed_use':'','initial_named_target':False,'new_target':False,'new_use_in_known_target':False,'mandatory_predicates':[],'required_bundle':[],'returned_citations':[],'opened_evidence':[],'provider_status':'hold','current_version':'unknown','historical_version':'unknown','historical_availability':'unknown','opened_complete':False,'cited_complete':False,'conflict_or_hold_reason':'','researcher_inference':'','empty_reason':rt.get('empty_reason','조건 대응하는 직접 원문 후보 부족'),'first_seen_query':None,'first_seen_rank':None,'search_receipt_ids':rt['queries'],'source_ids':[],'return_frozen_utc':rt['completed_utc']})
 P.joinpath('sources-candidates.json').write_text(json.dumps(list(sdict.values()),ensure_ascii=False,indent=2)+'\n')
 for name,rows in [('candidates',cs),('returns',rets)]:P.joinpath(name+'.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
 if logs:
  keys=list(logs[0])
  with P.joinpath('search-log.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(logs)
 return {'routes':len(routes),'search_requests':sum(r['event_type']=='search_request' for r in logs),'sources':len(sdict),'candidates':len(cs),'returns':len(rets)}
if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False))
