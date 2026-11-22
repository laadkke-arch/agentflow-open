import json,pathlib,csv,datetime
P=pathlib.Path(__file__).resolve().parent

def rebuild():
 sources={};candidates=[];returns=[];selection=[]
 for f in sorted((P/'route-records').glob('*.json')):
  r=json.loads(f.read_text())
  for s in r.get('sources',[]):
   sid=s['source_id']
   if sid in sources:
    old=sources[sid]
    obs=old.setdefault('version_observations',[])
    for seen in [old,s]:
     item={k:seen.get(k) for k in ['source_url','version','checked_utc','sections_read']}
     if item not in obs:obs.append(item)
    for key in ['related_questions','read_receipts']:
     old[key]=sorted(set(old.get(key,[])+s.get(key,[])))
    if s.get('count_in_minimum') and not old.get('count_in_minimum'):
     keep={k:old.get(k) for k in ['version_observations','related_questions','read_receipts']}
     old.update(s);old.update(keep)
   else:sources[sid]=s
  candidates.extend(r.get('candidates',[]));returns.extend(r.get('returns',[]));selection.extend(r.get('selection',[]))
 (P/'sources-candidates.json').write_text(json.dumps(list(sources.values()),ensure_ascii=False,indent=2))
 (P/'candidates.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in candidates))
 (P/'returns.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in returns))
 (P/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2))
 print(json.dumps({'source_rows':len(sources),'candidates':len(candidates),'return_slots':len(returns),'selections':len(selection)}))
if __name__=='__main__':rebuild()
