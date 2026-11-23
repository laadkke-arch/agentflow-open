"""Join sealed stream records without converting vacancies into observations."""
from pathlib import Path
import csv, json, datetime, hashlib
P=Path(__file__).resolve().parent
readj=lambda p:[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
readc=lambda p:list(csv.DictReader(p.open(newline='')))
def writej(name,rows): (P/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
def writec(name,rows):
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader();w.writerows(rows)
records=[]
for stream in ['gis','oss']:
 for r in readj(P/'streams'/stream/'records.jsonl'):
  r['stream']=stream
  r.setdefault('stratum','core')
  r.setdefault('event',r.get('event_id'))
  r.setdefault('status','SELECTED' if r.get('selected') else 'VACANT')
  r.setdefault('old_tag',r.get('old_release'))
  r.setdefault('consumer',r.get('repository'))
  r.setdefault('original_source_url',r.get('url'))
  r.setdefault('slot',r.get('recruitment_slot'))
  records.append(r)
aux=readj(P/'streams/gis/auxiliary_records.jsonl')
for r in aux:
 r.update(stream='gis',stratum='auxiliary')
 r.setdefault('status','EXCLUDED_FROM_CORE');r.setdefault('event','G04')
records.extend(aux)
writej('records.jsonl',records)
proposals=[]
for r in readc(P/'streams/gis/proposals.csv'):
 r['stratum']='core';proposals.append(r)
for r in readc(P/'streams/oss/proposals.csv'):
 for policy in ['A','B']:
  proposals.append({'proposal_id':r['record_id']+'-'+policy,'record_id':r['record_id'],'policy':policy,'stratum':r['stratum'],'sealed_utc':r['sealed_before_followup'],'action':r[policy+'_action'],'proposed_repair':r[policy+'_proposed_change'],'applicable_version':r['applicable_versions'],'source_ids':r['evidence_ids'],'score_eligible':r['score_eligible'],'consumer_followup_read_before_proposal':False})
writec('proposals.csv',proposals)
frame=[]
for stream in ['gis','oss']:
 for r in readc(P/'streams'/stream/'frame.csv'):
  r['stream']=stream;r.setdefault('row_type','repository_or_candidate_search');frame.append(r)
for r in records:
 frame.append({'row_type':'reserved_slot' if r['stratum']=='core' else 'auxiliary_record','record_id':r['record_id'],'event_id':r.get('event'),'slot':r.get('slot'),'status':r['status'],'repository':r.get('consumer',r.get('repository')),'old_tag':r.get('old_tag',r.get('old_release')),'included':r['status']=='SELECTED','exclusion_or_gap':r.get('reason',r.get('missing',r.get('exclusion_reason',''))),'source_ids':';'.join(r.get('source_ids',[]))})
writec('frame.csv',frame)
sources=[]
for stream in ['root','gis','oss']:
 for r in readj(P/'streams'/stream/'sources.jsonl'):
  r['stream']=stream;sources.append(r)
writej('sources.jsonl',sources)
seal={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope_commit':'7b108414de50ff32f28d1fa3c03ef6f2492724e6','core_slots':6,'selected_core':sum(r['status']=='SELECTED' and r['stratum']=='core' for r in records),'vacant_core':sum(r['status']=='VACANT' and r['stratum']=='core' for r in records),'consumer_followup_content_read':False,'hashes':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['SCOPE.md','records.jsonl','frame.csv','proposals.csv']},'sources_and_auxiliary_are_not_extra_core_slots':True}
(P/'evidence/preseal.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(seal,ensure_ascii=False,indent=2))
