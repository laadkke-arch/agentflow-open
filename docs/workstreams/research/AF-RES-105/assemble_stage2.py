"""Combine sealed reader records without changing the stage1 selection."""
import json,csv,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
load=lambda x:json.loads((P/x).read_text())
enc=lambda x:json.dumps(x,ensure_ascii=False) if isinstance(x,(dict,list)) else x
aux=load('evidence/blender-auxiliary/auxiliary-part.json')['cases']+load('evidence/qgis-auxiliary/auxiliary-part.json')['cases']
base=list(csv.DictReader((P/'initial.csv').open()));base=[r for r in base if r['stratum']=='chronological'];fields=list(base[0])
for c in aux:
 i=c['initial'];p=c['proposal'];row={k:'' for k in fields};row.update(case_id=c['case_id'],stratum='explicit_statement_auxiliary',site='blender' if c['case_id'].startswith('BL') else 'gis',frame_rank=c['match_pool_rank'],question_id=c['question_id'],creation_utc=i['initial_created_utc'],initial_revision_url=i['initial_revision_url'],original_url=f'https://{"blender" if c["case_id"].startswith("BL") else "gis"}.stackexchange.com/questions/{c["question_id"]}',owner_user_id=c['original_author_user_id'],goal=i['goal'],attempted_operation=i['actual_attempt'],author_version=i.get('author_version','미확인'),knowledge_units=i['known_unit'],source_refs=[c['case_id']+'-INITIAL'],body_sha256=i['body_sha256'],evidence_record='evidence/'+('blender' if c['case_id'].startswith('BL') else 'qgis')+'-auxiliary/auxiliary-part.json#cases/'+c['case_id'],missing=i['unknowns'],exposure='lexical statement deliberately exposed; before proposal initial reconstructed at stage2; never chronological efficacy denominator')
 base.append({k:enc(v) for k,v in row.items()})
with (P/'initial.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(base)
main=load('evidence/blender-proposals/proposals-part.json')['cases']+load('evidence/qgis-proposals/proposals-part.json')['cases']
rows=[]
for c in main:
 rows.append(dict(case_id=c['case_id'],stratum='chronological',question_id=c['question_id'],candidate_id=c['case_id']+'-P1',proposal_event_id=c['proposal_event_id'],proposal_kind=c['proposal_kind'],proposal_url=c['proposal_original_url'],proposal_immutable_url=c.get('proposal_immutable_url','미확인'),proposal_utc=c['proposal_creation_utc'],first_method=c.get('first_method',c.get('primary_method')),one_difference=c.get('delta_one_part',c.get('one_change_from_initial')),original_links=c.get('proposal_original_links',c.get('originally_attached_links',[])),researcher_later_links=[],prior_awareness='미확인',explicit_new_awareness='미확인',body_sha256=c.get('proposal_body_sha256',c.get('body_sha256')),evidence_record='evidence/'+('blender' if c['case_id'].startswith('BL') else 'qgis')+'-proposals/proposals-part.json#cases/'+c['case_id'],missing=c.get('missing',[]),exposure='no postproposal author evidence before stage2 seal'))
for c in aux:
 p=c['proposal'];rows.append(dict(case_id=c['case_id'],stratum='explicit_statement_auxiliary',question_id=c['question_id'],candidate_id=c['case_id']+'-P1',proposal_event_id=p['proposal_event_id'],proposal_kind=p['proposal_kind'],proposal_url=p['proposal_url'],proposal_immutable_url=p.get('proposal_immutable_url','미확인'),proposal_utc=p['proposal_utc'],first_method=p['first_method'],one_difference=p['single_difference'],original_links=p['original_links'],researcher_later_links=[],prior_awareness=p['preproposal_awareness'],explicit_new_awareness=p['explicit_new_awareness'],body_sha256=p['body_sha256'],evidence_record='evidence/'+('blender' if c['case_id'].startswith('BL') else 'qgis')+'-auxiliary/auxiliary-part.json#cases/'+c['case_id'],missing=p['limitations'],exposure='matching statement and antecedent deliberately exposed; later response not yet read'))
with (P/'proposals.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows([{k:enc(v) for k,v in r.items()} for r in rows])
frame=list(csv.DictReader((P/'frame.csv').open()));frame=[r for r in frame if r['stratum']=='chronological'];fields=list(frame[0])
for c in aux:
 i=c['initial'];row={k:'' for k in fields};row.update(site='blender' if c['case_id'].startswith('BL') else 'gis',stratum='explicit_statement_auxiliary',window='2024 statements in closed indexed/current-tag pool',rank=c['match_pool_rank'],question_id=c['question_id'],creation_utc=i['initial_created_utc'],initial_revision_guid=i['initial_revision_guid'],url=f'https://{"blender" if c["case_id"].startswith("BL") else "gis"}.stackexchange.com/questions/{c["question_id"]}',initial_immutable_url=i['initial_revision_url'],initial_tags=i.get('initial_tags',[]),eligibility='selected_lexical_auxiliary',reason=c['statement'].get('reason'),selected_slot=c['case_id'],body_sha256=i['body_sha256'],reading_scope=i['direct_read_scope'],initial_revision_url=i['initial_revision_url'],vacancy='no',source_locator=c['case_id']+'-INITIAL',initial_body_read='true');frame.append({k:enc(v) for k,v in row.items()})
with (P/'frame.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(frame)
# Stage1 source set retained by id; additional evidence cannot inflate same-episode totals.
old=[json.loads(x) for x in (P/'sources.jsonl').read_text().splitlines()];by={x['source_id']:x for x in old}
for name in ['blender-proposals','qgis-proposals','blender-auxiliary','qgis-auxiliary']:
 for line in (P/f'evidence/{name}/sources-part.jsonl').read_text().splitlines():
  s=json.loads(line)
  if 'source_id' not in s:
   s.update(source_id=s['id'],opened_utc=s['direct_opened_utc'],lineage=s['same_work_lineage'],version=s['version_section'],location=s['preserved_evidence'],observed=s['confirmed'],supports=[s['supports_or_counters']],refutes=[],counting=dict(counted_unique_primary_source=s['count_unique_primary'],category='auxiliary_request' if s['count_unique_primary'] else 'episode_duplicate',mandatory_minimum_category=False,reason=s['count_reason']))
  by[s['source_id']]=s
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in by.values()))
summary=dict(stage=2,chronological_slots=8,auxiliary_slots=4,unique_episodes=12,primary_candidates=12,auxiliary_match_pool=dict(blender=9,gis=13,overlap_with_chronological=0),vacancies=0,critical_limits=['QG-T1 question-author public ID absent: third-party identity 미확인','QG-K1 known-cue family does not establish preproposal knowledge','BL-N1 and QG-N1 statement referents differ from first thread proposal','No causal efficacy/prevalence estimates from auxiliary sample'],source_rows=len(by),screening_files=['evidence/blender-auxiliary/screening.json','evidence/qgis-auxiliary/screening.json'],frozen_initial_commit='de11fb2b05c0e65cc1451826c720eebcbc3e52cd')
(P/'evidence/auxiliary/stage2-reconciliation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
assert len(base)==12 and len(rows)==12 and len(frame)==164
assert len({r['question_id'] for r in rows})==12
print(json.dumps(summary,ensure_ascii=False))
