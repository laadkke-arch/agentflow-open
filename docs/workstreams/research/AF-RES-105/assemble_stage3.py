"""Combine attributed follow-up facts; no read of additional external material."""
import json,csv,datetime
from pathlib import Path
P=Path(__file__).resolve().parent;J=lambda x:json.loads((P/x).read_text());enc=lambda x:json.dumps(x,ensure_ascii=False) if isinstance(x,(list,dict)) else x
initial={r['case_id']:r for r in csv.DictReader((P/'initial.csv').open())};props={r['case_id']:r for r in csv.DictReader((P/'proposals.csv').open())};rows=[]
for name in ['blender','qgis','auxiliary']:
 for c in J(f'evidence/{name}-followup/followup-part.json')['cases']:
  cid=c['case_id'];p=props[cid];i=initial[cid];aux=name=='auxiliary';ev=c.get('owner_events',c.get('author_events',[]));window=c.get('window',c.get('followup_window',{}));end=c.get('window_end_utc',window.get('end_utc'));cap=aux and bool(c.get('new_unit_explicit'));exe=aux and bool(c.get('main_execution_observed'))
  owner=i['owner_user_id'] or '미확인';known='미확인';new='미확인'
  if name=='blender':summary=c['execution'];versions=c['versions'];acceptance=c['current_acceptance'];counter=c['opposing_observation'];sources=c['source_refs']
  elif name=='qgis':summary=c['selected_proposal_author_execution'];versions=c['version_partition'];acceptance='current metadata separately in evidence/endorsements/current-metadata.json; not dated180day evidence';counter=c['counter_observations'];sources=c['source_refs']
  else:summary={k:c[k] for k in ['knowledge','execution','result','counter']};versions={'author':'미확인','official_or_runtime':'see evidence/auxiliary-official and Blender sources; do not backfill'};acceptance='see evidence/auxiliary-followup/current-endorsements.json; current badge time 미확인';counter=c['counter'];sources=c['source_refs']
  row=dict(case_id=cid,stratum=p['stratum'],episode_id=f'{i["site"]}:{i["question_id"]}',candidate_id=p['candidate_id'],question_id=i['question_id'],owner_user_id=owner,owner_identity='미확인' if owner=='미확인' else 'public_numeric_ID_matched',proposal_url=p['proposal_url'],proposal_utc=p['proposal_utc'],window_end_utc=end,author_events=ev,author_event_count=len(ev),author_comment_count=sum('comment' in x.get('kind',x.get('event_kind','comment')) for x in ev),author_question_revision_count=sum(x.get('kind')=='question_revision' for x in ev),author_self_answer_count=c.get('author_self_answers_count',c.get('self_answer_count',c.get('coverage',{}).get('owner_self_answers',0))),full_prior_awareness=known,full_new_awareness=new,full_newness_decidable=0,full_newness_unknown=1,changed_capability_new_explicit=int(cap),changed_capability_new_decidable=int(cap),changed_capability_new_unknown=0 if cap else 1,same_fixed_proposal_execution='D1 trial report; failed to add point' if exe else '미확인',same_fixed_proposal_execution_decidable=int(exe),same_fixed_proposal_success=0 if exe else '미확인',same_fixed_proposal_success_decidable=int(exe),learn_then_same_operation_execute='미확인',learn_then_execute_decidable=0,evidence_summary=summary,current_acceptance_or_votes=acceptance,versions=versions,counterevidence=counter,source_refs=sources,evidence_record=f'evidence/{name}-followup/followup-part.json#cases/{cid}')
  # Blender owner events do not have kind, but are both comments. No revisions omitted here.
  rows.append({k:enc(v) for k,v in row.items()})
assert set(r['case_id'] for r in rows)==set(initial)
with (P/'followup.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
minimum={
'chronological_requests':['BL-T1-INITIAL','BL-T2-INITIAL','BL-T3-INITIAL','BL-T4-INITIAL','QG-INIT-473575','QG-INIT-473591','QG-INIT-473594','QG-INIT-473611'],
'blender_official':['BL-O1','BL-O2','BL-O3','BL-O4'],
'qgis_official':['QG-T-O-LABELING','QG-T-O-EXPRESSION','QG-T-O-VRT','QG-T-O-WARP'],
'blender_upstream':['BL-U1','BL-U2'],
'qgis_upstream':['QG-T-U-EXPRESSION','QG-T-U-GDAL'],
'calc':['CD-CALC-MAN','CD-CALC-FORMULA'],
'audacity':['CD-AUD-ENVELOPE-364','CD-AUD-ISSUE2371']}
sources={s['source_id']:s for s in [json.loads(l) for l in (P/'sources.jsonl').read_text().splitlines()]};minimumids=[sid for ids in minimum.values() for sid in ids]
assert len(minimumids)==24 and len(set(minimumids))==24
for sid in minimumids:assert sources[sid]['counting']['counted_unique_primary_source'],sid
counted=[s for s in sources.values() if s['counting']['counted_unique_primary_source']];extra=[s['source_id'] for s in counted if s['source_id'] not in minimumids]
result=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_ledger_rows=len(sources),conservatively_counted_unique_primary=len(counted),required_minimum=24,mandatory_category_counts={k:len(v) for k,v in minimum.items()},mandatory_source_ids=minimum,additional_counted_source_ids=extra,additional_counted=len(extra),missing_required_source_count=0,screened_chronological_requests=160,selected_chronological_requests=8,screened_not_selected_chronological_requests=152,auxiliary_closed_matches=22,selected_auxiliary_requests=4,case_vs_source_limit='12 selected independent question episodes, not12differentpeople; sameeventrevisions/comments/images do not addindependentworks',upstream_scope='4distinctupstreamtestfiles directlyread, notexecuted; Blenderlow-levelmath tests, QGISexpression/commandgeneration tests; not full GN/raster end-to-end fixture coverage',failed_node_fixture_count=2,failed_node_fixtures_counted=False,native_probe_counted_as_external_sources=False)
(P/'evidence/source-counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('followup rows12; counts',json.dumps(result['mandatory_category_counts']), 'total',len(counted))
