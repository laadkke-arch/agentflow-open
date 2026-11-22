import json, pathlib, datetime, re
P=pathlib.Path(__file__).resolve().parent
def raw(id, kind='opens'):
 return json.loads((P/'cache'/kind/(id+'.json')).read_text())
def source(sid,id,title,url,version,section,verified,limit,producer='Apache Software Foundation',date='원 발행일 미확인',lineage=None,count=True):
 return dict(source_id=sid,title=title,source_url=url,version=version,published_or_revised=date,checked_utc=raw(id)['ended_utc'],sections_read=section,verified_content=verified,limitations=limit,producer=producer,lineage_id=lineage or url,count_in_minimum=count,count_reason='직접 연 고유 공급자 원문. 같은 계보의 재열람은 한 번만 산입.' if count else '관측 실패 또는 동일 원문 중복',related_questions=[id[:3],'Q3','Q4','Q7'],source_role='provider',read_receipts=[id])
def cite(s,section=None,missing=None):
 d=dict(source_id=s['source_id'],url=s['source_url'],section=section or s['sections_read'])
 if missing:d['missing']=missing
 return d
def candidate(q,route,k,name,cls,use,known,status,version,bundles,cites,reason,first,complete=False,historical='unknown'):
 return dict(question_id=q,route=route,rank=None,candidate_id=k,target_name=name,candidate_class=cls,proposed_use=use,initial_named_target=known,new_target=not known,new_use_in_known_target=known,mandatory_predicates=list(bundles),required_bundle=bundles,returned_citations=cites,opened_evidence=cites,provider_status=status,current_version=version,historical_version='미확인' if historical=='unknown' else version,historical_availability=historical,opened_complete=complete,cited_complete=complete,conflict_or_hold_reason=reason,researcher_inference='공급자 기록을 최초 조건에 대응한 연구자의 사용 제안. 실제 통합 실행이나 도입 비용은 관측하지 않음.',empty_reason='',first_seen_query=first[0],first_seen_rank=first[1],search_receipt_ids=[f'{q}-{route}-q{first[0]}'],source_ids=sorted(set(c['source_id'] for c in cites)))
def empty(q,route,rank,reason):
 return dict(question_id=q,route=route,rank=rank,candidate_id='',target_name='',candidate_class='empty',proposed_use='',initial_named_target=False,new_target=False,new_use_in_known_target=False,mandatory_predicates=[],required_bundle={},returned_citations=[],opened_evidence=[],provider_status='hold',current_version='미확인',historical_version='미확인',historical_availability='unknown',opened_complete=False,cited_complete=False,conflict_or_hold_reason=reason,researcher_inference='',empty_reason=reason,first_seen_query=None,first_seen_rank=None,search_receipt_ids=[],source_ids=[])
def selection(q,route,selected,excluded={}):
 out=[]
 for qi in range(1,4):
  id=f'{q}-{route}-q{qi}';r=raw(id,'search');t='\n'.join(c.get('text','') for c in r['raw']['content'])
  matches=re.findall(r'^(.+?) \((https?://[^\n]+)\)\n【([^】]+)】',t,re.M)
  for rank,m in enumerate(matches,1):
   d=dict(receipt_id=id,observed_rank=rank)
   if rank>10:d.update(decision='excluded_over_ten',reason='provided after first ten; exposed but not selectable')
   elif (qi,rank) in selected:
    s,k,oi=selected[(qi,rank)];d.update(decision='selected_open',reason='first eligible primary original in locked query order',source_id=s,candidate_id=k,body_receipt=f'{q}-{route}-o{oi}')
   elif (qi,rank) in excluded:
    dec,reason=excluded[(qi,rank)];d.update(decision=dec,reason=reason)
   else:d.update(decision='not_opened_budget',reason='five unique original attempts consumed before this result')
   out.append(d)
 return out
def finish(q,route,sources,candidates,ordered,selected,excluded={},note=''):
 returns=[]
 for rank,c in enumerate(ordered,1):
  c['rank']=rank;returns.append(c)
 while len(returns)<3:returns.append(empty(q,route,len(returns)+1,'선택한 원문에서 다른 독립 대상/사용 경계를 확보하지 못함'))
 for c in candidates:c['original_rank']=c['rank']
 data=dict(question_id=q,route=route,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sources=sources,candidates=candidates,returns=returns,selection=selection(q,route,selected,excluded),near_miss=note,budget_observed=dict(queries=3,unique_original_opens=len(selected),retries=0,return_slots=3))
 (P/'route-records'/f'{q}-{route}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
