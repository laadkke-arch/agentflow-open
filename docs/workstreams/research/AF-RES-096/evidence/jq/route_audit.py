import pathlib,json,datetime
P=pathlib.Path(__file__).resolve().parents[2]
rows=[];errors=[]
for cid,order in [('J1',['A','B']),('J2',['B','A']),('J3',['A','B']),('J4',['B','A'])]:
 for route in order:
  d=P/'evidence/routes'/f'{cid}-{route}';j=json.loads((d/'judgment.json').read_text());ex=json.loads((d/'exposure.json').read_text());events=[json.loads(s) for s in (d/'access.jsonl').read_text().splitlines()];opens=[x for x in events if x['event']=='body_attempt'];nav=[x for x in events if x['event']=='section_navigation'];opened={x['file_id'] for x in opens if x['status']=='success'};expected=[x['file_id'] for x in ex['slots'] if not x['empty']]
  if [x['file_id'] for x in opens]!=expected:errors.append([cid,route,'open order'])
  if len(opens)>4:errors.append([cid,route,'overbudget'])
  if len(j['returned_sources'])>2:errors.append([cid,route,'overlinks'])
  if not set(j['used_file_ids']) <= opened:errors.append([cid,route,'unopened evidence'])
  returned={x['file_id'] for x in j['returned_sources']}
  if not set(j['used_file_ids']) <= returned:errors.append([cid,route,'used but not returned'])
  for source in j['returned_sources']:
   fid=source['file_id'];coverage=set()
   for n in nav:
    if n['file_id']==fid:coverage.update(range(n['start_line'],n['end_line']+1))
   for s in source['sections']:
    if not set(range(s['start'],s['end']+1))<=coverage:errors.append([cid,route,'unread returned range',fid,s['start'],s['end']])
  rows.append({'case_id':cid,'route':route,'attempts':len(opens),'failed':sum(x['status']!='success' for x in opens),'unused':4-len(opens),'returned':len(j['returned_sources']),'judgment':j['judgment'],'body_bytes':sum(x.get('bytes',0) for x in opens),'opened_file_ids':expected,'used_file_ids':j['used_file_ids'],'read_completed_utc':j['read_completed_utc'],'last_navigation_utc':max((x['utc'] for x in nav),default=None)})
out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'routes':rows,'body_attempts':sum(x['attempts'] for x in rows),'failed_attempts':sum(x['failed'] for x in rows),'errors':errors,'notes':['This audits source access/returned ranges; it does not run the proposed jq expressions.','Q4 search2 per route was executed by root; this audit does not recompute ranking.']}
(P/'evidence/jq/route-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
