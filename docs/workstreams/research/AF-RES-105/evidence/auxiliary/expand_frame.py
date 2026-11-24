"""Expose every frozen auxiliary match in frame.csv; selection is unchanged."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parents[2];rows=list(csv.DictReader((P/'frame.csv').open()));oldaux={r['selected_slot']:r for r in rows if r['stratum']=='explicit_statement_auxiliary'};chrono=[r for r in rows if r['stratum']=='chronological'];fields=list(rows[0])+['frame_unit','statement_event_id','statement_utc','statement_url','statement_family','statement_body_sha256','source_refs']
for r in chrono:r.update(frame_unit='question_initial_revision',statement_event_id='해당없음',statement_utc='해당없음',statement_url='해당없음',statement_family='해당없음',statement_body_sha256='해당없음',source_refs=r.get('source_locator',''))
meta=json.loads((P/'.cache/auxiliary/engine-metadata-pool.json').read_text());maps={s:{q['question_id']:q for q in v['potential_additional_questions']} for s,v in meta.items()};aux=[]
for site,reader in [('blender','blender'),('gis','qgis')]:
 data=json.loads((P/f'evidence/{reader}-auxiliary/screening.json').read_text());screen=data if isinstance(data,list) else data['rows']
 for s in screen:
  q=s['question_id'];dec=s['decision'];cid=dec[9:] if dec.startswith('selected_') else '';r=dict(oldaux[cid]) if cid in oldaux else {k:'미확인' for k in fields};m=maps[site].get(q,{})
  r.update(site=site,stratum='explicit_statement_auxiliary',window='2024 statement; frozen indexed/current-tag pool',rank=s.get('rank',s.get('rank_in_closed_gis_match_pool')),question_id=q,eligibility=dec,reason=s['reason'],selected_slot=cid or '해당없음',vacancy='no_slot_vacancy' if cid else 'not_a_selected_slot',frame_unit='matched_author_cue_event',statement_event_id=s['event_id'],statement_utc=s['event_created_utc'],statement_url=s['event_url'],statement_family=json.dumps(s['lexicon_hits'],ensure_ascii=False),statement_body_sha256=s.get('body_sha256',s.get('statement_body_sha256')),reading_scope=s.get('context_scope',s.get('read_boundary','matching statement and recorded context')),source_refs=('BL-AUX-STATEMENT-' if site=='blender' else 'QG-AUX-E')+str(s['event_id']))
  r['url']=m.get('link',f'https://{site}.stackexchange.com/questions/{q}');r['original_url']=r['url'];r['current_tags']=json.dumps(m.get('tags',json.loads(next((x['current_tags'] for x in chrono if str(x['question_id'])==str(q)),'[]'))),ensure_ascii=False)
  if not cid:r['initial_body_read']='false; only indicated statement/context read';r['initial_images_read']='미확인';r['image_status']='not needed for this screening decision';r['source_locator']=f'evidence/{reader}-auxiliary/screening.json event{s["event_id"]}'
  aux.append(r)
with (P/'frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(chrono+aux)
assert len(chrono)==160 and len(aux)==22 and sum(r['selected_slot']!='해당없음' for r in aux)==4
print('frame rows',len(chrono)+len(aux),'chrono160,auxiliarymatched22,selectedaux4')
