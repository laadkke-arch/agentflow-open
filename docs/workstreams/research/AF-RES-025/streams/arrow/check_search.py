import json,csv,pathlib,collections
P=pathlib.Path(__file__).resolve().parent
def run():
 locked={(r['question_id'],r['route']):r['query_strings'] for r in map(json.loads,(P/'queries.jsonl').read_text().splitlines())}
 checks=[];summary=[];route_times=[]
 for f in sorted((P/'route-records').glob('*.json')):
  d=json.loads(f.read_text());q=d['question_id'];route=d['route']
  recs=[json.loads((P/'receipts'/f'{q}-{route}-q{i}.json').read_text()) for i in range(1,4)]
  op=[json.loads(x.read_text()) for x in sorted((P/'receipts').glob(f'{q}-{route}-o*.json'))]
  actual=[r['request']['system1_search_query'][0]['q'] for r in recs]
  checks.append(dict(question_id=q,route=route,queries_match_seal=actual==locked[(q,route)],slots=[x['rank'] for x in d['returns']],selected=len([x for x in d['selection'] if x['decision']=='selected_open']),all_selected_first10=all(x['observed_rank']<=10 for x in d['selection'] if x['decision']=='selected_open')))
  route_times.append(dict(question_id=q,route=route,started_utc=min(x['started_utc'] for x in recs),return_frozen_utc=d['completed_utc']))
  summary.append(dict(question_id=q,route=route,queries=len(recs),provided_results=sum(r['returned_count'] for r in recs),first10_results=sum(r['first10_count'] for r in recs),search_call_ms=sum(r['wall_ms'] for r in recs),opens=sum('retry_of' not in r for r in op),retries=sum('retry_of' in r for r in op),failed_open_calls=sum(r['is_error'] for r in op),open_call_ms=sum(r['wall_ms'] for r in op),valid_new_current=sum(x['new_target'] and x['provider_status']=='support' and x['opened_complete'] and x['cited_complete'] for x in d['returns']),empty_slots=sum(x['candidate_class']=='empty' for x in d['returns'])))
 assert all(x['queries_match_seal'] and x['slots']==[1,2,3] and x['selected']==5 and x['all_selected_first10'] for x in checks)
 rows=list(csv.DictReader((P/'search-log.csv').open()));assert not [r for r in rows if r['decision']=='pending']
 src=json.loads((P/'sources-candidates.json').read_text())
 out=dict(checks=checks,route_summary=summary,execution_order=sorted(route_times,key=lambda r:r['started_utc']),unique_direct_candidate_originals=len({s['lineage_id'] for s in src if s['count_in_minimum']}),source_rows=len(src),notes=['40 first open attempts plus2 retries; four failed calls. R recovered random.h independently; G evidence unchanged.','Call durations may overlap; summed call_ms is not human work time. Tokens, money, person-hours unknown.','Q02 G q2 rank11 and Q04 R q3 rank11..18 are over-cap metadata, not selectable.','Parser fixed omitted delimiter before Q04 R q3 rank16; first-ten selection and returns unaffected.','Q03/Q04 later original-project title/snippet exposures require sensitivity exclusions; no followup body opened.'])
 (P/'search-self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
