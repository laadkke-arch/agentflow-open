"""Normalize reviewed strand ledgers without erasing original denominators or caveats.
No network, no new data collection, no execution of downloaded study code.
"""
import csv,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STREAM=ROOT/'streams'
def js(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def read(kind):
 out=[]
 for p in sorted(STREAM.glob('*/'+kind+'*.jsonl')):
  for i,line in enumerate(p.read_text().splitlines(),1):
   if line.strip():
    x=json.loads(line);x['_provenance']=str(p.relative_to(ROOT))+':'+str(i);out.append(x)
 return out
def pick(x,*keys,default=None):
 for k in keys:
  if k in x and x[k] is not None:return x[k]
 return default
def write_jsonl(path,rows):path.write_text(''.join(js(r)+'\n' for r in rows))
def write_csv(path,rows,fields):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for row in rows:
   w.writerow({k:js(row.get(k)) if isinstance(row.get(k),(dict,list)) else row.get(k) for k in fields})

# These are canonical experiment IDs already present in software-b/studies.jsonl.
# In particular, NCQ's two cohorts must not be joined only by their shared family.
SWB_EFFECT_STUDY_IDS={
 'SWB-E01':'SWB-EXO-1',
 'SWB-E02':'SWB-EXO-1',
 'SWB-E03':'SWB-EXO-1',
 'SWB-E04':'SWB-EXO-1',
 'SWB-E05':'SWB-ACAR-1',
 'SWB-E06':'SWB-ACAR-1',
 'SWB-E07':'SWB-ACAR-1',
 'SWB-E08':'SWB-PROMPT-2',
 'SWB-E09':'SWB-PROMPT-2',
 'SWB-E10':'SWB-NCQ-1',
 'SWB-E11':'SWB-NCQ-2',
 'SWB-E12':'SWB-NCQ-2',
 'SWB-E13':'SWB-REST-1',
 'SWB-E14':'SWB-STRATH-1',
 'SWB-E15':'SWB-ACAR-1',
 'SWB-E16':'SWB-ACAR-1',
}
ROOT_EFFECT_STUDY_IDS={
 'Er-01':'UNAKITE2',
 'Er-02':'UNAKITE1',
 'Er-03':'CODEMEND-LAB',
 'Er-04':'STRATA-LAB',
}

def link_effect(out,effect,source_map,canonical_studies,studies_by_family):
 """Use existing experiment/claim IDs, retaining the basis of inferred joins."""
 cid=effect['comparison_id'];fam=effect['study_family']
 explicit=SWB_EFFECT_STUDY_IDS.get(cid,ROOT_EFFECT_STUDY_IDS.get(cid))
 eid=pick(effect,'study_id','experiment_id')
 if eid:
  assert explicit is None or eid==explicit,('conflicting explicit study ID',cid,eid,explicit)
  basis='effect_record'
 elif explicit:
  eid=explicit;basis='explicit_reviewed_canonical_map'
 else:
  candidates=studies_by_family.get(fam,set())
  assert len(candidates)==1,('ambiguous or absent canonical study',cid,fam,sorted(candidates))
  eid=next(iter(candidates));basis='unique_canonical_experiment_in_family'
 assert eid in canonical_studies,('unknown canonical study',cid,eid)
 study=canonical_studies[eid]
 assert study['study_family']==fam,('study family mismatch',cid,eid)
 assert set(out['source_ids']).issubset(study['source_ids']),('study source mismatch',cid,eid)
 out['study_id']=eid;out['study_link_basis']=basis
 if effect.get('claim_id'):
  claims=[effect['claim_id']];basis='effect.claim_id'
 elif effect.get('claim_ids'):
  claims=effect['claim_ids'];basis='effect.claim_ids'
 elif effect.get('claims'):
  claims=effect['claims'];basis='effect.claims'
 else:
  claims=[claim for sid in out['source_ids'] for claim in source_map[sid]['claim_ids']]
  basis='source_level_join'
 if isinstance(claims,str):claims=[claims]
 out['claim_ids']=list(dict.fromkeys(claims));out['claim_link_basis']=basis
 assert out['claim_ids'],('missing source/effect claims',cid)

def normalize_swb_study(out,study,arm):
 """Expose B's reported arm counts and timing without deriving missing counts."""
 if not study['study_family'].startswith('SWB-'):return
 out['arm_trials']=pick(arm,'trial_n','n_trials',default=out['arm_trials'])
 if out['arm_trials'] is None and len(study.get('arms',[]))==1:
  # Strathcona's eight reported trials all belong to its sole arm.
  out['arm_trials']=pick(study,'trials_analyzed',default=out['arm_trials'])
 arm_time={k:arm[k] for k in ['median_total_seconds','median_final_package_seconds'] if k in arm}
 if arm_time:
  out['time_result']={**out['time_result'],**arm_time}
  # Preserve the complete original arm in detail_json, but keep timing out of
  # the representative quality field. Completion counts remain quality data.
  out['quality_result']={k:v for k,v in out['quality_result'].items() if k not in arm_time}

def normalize_swb_effect(out,effect):
 """Restore B's source fields and apply the reviewed percent/point distinction."""
 if not effect['study_family'].startswith('SWB-'):return
 cid=effect['comparison_id'];assert cid in SWB_EFFECT_STUDY_IDS,('unmapped B effect',cid)
 original_report=effect.get('original_report',{})
 out['original_values']={**out['original_values'],**original_report}
 if 'original_counts' in effect:
  out['original_values']['original_counts']=effect['original_counts']
  out['recalculation_inputs']={**out['recalculation_inputs'],'original_counts':effect['original_counts']}
 if 'recalculated_interval' in effect:
  out['recalculation_inputs']={**out['recalculation_inputs'],**{k:original_report[k] for k in ['coefficient','standard_error']}}
  out['recalculated_result']={**out['recalculated_result'],'recalculated_interval':effect['recalculated_interval']}
 if cid in {'SWB-E08','SWB-E09'}:
  # BREV-03: 70/46 and 68/40 are percentage levels; only 24/28 are points.
  # detail_json retains the phase-3 raw record and its original unit wording.
  out['original_values']['unit']='percent'
  out['recalculation_inputs']={**out['recalculation_inputs'],'original_value_unit':'percent'}
  out['recalculated_result']={**out['recalculated_result'],'absolute_difference_unit':'percentage_points','ratio_unit':'dimensionless','percent_change_unit':'percent'}
 if cid=='SWB-E08':
  out['denominator']='12 people observed in each condition;24 task executions;12 paired participants'

def normalize_study_boundaries(out,study,arm):
 """Make missing measurements explicit, and retain unresolved source conflicts."""
 out['normalization_notes']=[]
 if study.get('denominator_conflict'):
  out['time_denominator']={'reported':study.get('denominator_all'),
   'status':study.get('denominator_all_status'),'conflict':study['denominator_conflict']}
  out['people_reported']=study.get('participants_reported')
  out['normalization_notes'].append('Body and arm-table totals conflict; no confirmed assignment/completion denominator imputed.')
 if out['study_id']=='SWB-EXO-1':
  vals=[533,1414,1832] if arm['arm']=='eXoaDocs' else [880,1503,1923]
  out['time_result']={'statistic':'published cumulative mean seconds among completers',
   'T1':vals[0],'T2':vals[1],'T3_T4_reported_group':vals[2],
   'n':'Table X per-time analysis denominator not given; not substituted from test passes',
   'effect_ids':['SWB-E01','SWB-E02','SWB-E03'],'locator':'Table X'}
 if out['time_result'] in ({},None,''):
  out['time_result']={'numeric_actual_time':'not reported or not recoverable from exact text',
   'source_description':out['time_method'],'budget_minutes_not_observed_duration':study.get('time_budget_minutes'),
   'limitations':out['limitations']}
  if out['study_id']=='SWB-REST-1':out['time_result']['reported_time_p']=.051

def normalize_other_effect_fields(out,effect,study):
 """Lift non-time observations and denominator caveats out of nested raw JSON."""
 out['normalization_notes']=[]
 if 'original_values' in effect:
  out['original_values']=effect['original_values']
  out['recalculation_inputs']={'published_input':effect['original_values'],
   'calculation_scope':effect.get('calculable'),'missing_or_boundary':effect.get('reason')}
  out['calculation_status']=str(effect.get('calculable')) if effect.get('calculable') else 'not_computable: '+effect.get('reason','')
 if not out['denominator']:
  inp=effect.get('input',{})
  input_counts={k:v for k,v in inp.items() if k.startswith('n') or 'assigned' in k or 'complete' in k or k=='participants'} if isinstance(inp,dict) else inp
  out['denominator']={'input_counts':input_counts,
   'study_reported':{k:study.get(k) for k in ['people_reported','people_enrolled','people_assigned','people_analyzed','people_completed','trials_reported']},
   'time_denominator':study.get('time_denominator'),
   'basis':'source-reported counts and status; no unreported arm/time denominator inferred'}
 if not out['noncompletion']:
  out['noncompletion']=study.get('noncompletion') or study.get('limitations') or 'not reported in available source'
 if not out['reversal_condition']:
  out['reversal_condition']={'calculation_limit':effect.get('reason'),'study_limit':study.get('limitations')}
 if not out['formula']:
  out['formula']='not computed; '+str(effect.get('reason') or out['calculation_status'])
 if not out['recalculation_inputs']:
  out['recalculation_inputs']={'not_computed_reason':effect.get('reason') or out['calculation_status']}
 if not out['recalculated_result']:
  out['recalculated_result']={'computed':False,'reason':effect.get('reason') or out['calculation_status']}

raw_sources=read('sources'); sources=[]; seen=set()
core={'software_primary','design_primary','learning_primary','artifact'}
for x in raw_sources:
 sid=x['source_id'];assert sid not in seen,sid;seen.add(sid)
 cat=x.get('count_category','unclassified')
 if cat=='original_artifact':cat='artifact'
 eligible=bool(x.get('count_minimum')) and cat in core
 s=dict(source_id=sid,type=pick(x,'type','material_type'),publisher=x.get('publisher'),title=x.get('title'),original_url=x.get('original_url'),fixed_url=x.get('fixed_url'),published=pick(x,'published','publication_date','published_date'),version=x.get('version'),checked_utc=pick(x,'checked_utc','verified_utc'),read_locator=pick(x,'read_locator','read_locators'),verified_content=pick(x,'verified_content','confirmed'),questions=x.get('questions',[]),claim_ids=pick(x,'claim_ids','claims',default=[]),limitations=x.get('limitations'),study_family=x.get('study_family'),duplicate_group=x.get('duplicate_group',x.get('study_family')),count_category=cat,count_minimum=eligible,minimum_decision='core category and substantive direct content' if eligible else 'not part of 10 software + 6 cross-domain + 8 artifact minimum',access_level=pick(x,'access_level','observation_grade','read_status'),content_sha256=pick(x,'content_sha256','download_sha256'),aliases=x.get('aliases',[]),strand_record=x['_provenance'],strand_details=x)
 sources.append(s)
source_map={s['source_id']:s for s in sources}
write_jsonl(ROOT/'sources.jsonl',sources)
studies=[]; raw_studies=read('studies')
for x in raw_studies:
 fam=x['study_family']; sid=pick(x,'source_id',default=(x.get('source_ids') or [None])[0]); assert sid in source_map,(fam,sid)
 eid=pick(x,'study_id','experiment_id',default=fam+'-E1')
 arms=x.get('arms') or [None]
 for j,arm in enumerate(arms):
  arm=arm or {};arm_name=pick(arm,'arm','id','name',default=x.get('arm','all/unspecified'))
  rowid=x.get('study_row_id') or eid+'-A'+str(j+1)
  out=dict(study_row_id=rowid,study_id=eid,study_family=fam,source_ids=x.get('source_ids',[sid]),source_url=source_map[sid]['fixed_url'],locator=pick(x,'locator','locations',default=source_map[sid]['read_locator']),field=source_map[sid]['count_category'],included_core=source_map[sid]['count_minimum'],comparison_grade=x.get('comparison_grade'),product_directness=pick(x,'directness','product_directness'),arm=arm_name,arm_n_assigned=pick(arm,'n_assigned','assigned','n',default=x.get('participants_arm')),arm_n_analyzed=pick(arm,'analyzed','n_assigned_analyzed'),arm_people_reported=pick(arm,'n_people','n_assigned_analyzed','analyzed','n_assigned','assigned',default=x.get('participants_arm')),people_reported=pick(x,'participants_total','participants_analyzed','participants_assigned'),people_enrolled=pick(x,'n_enrolled','participants_recruited'),people_assigned=pick(x,'participants_assigned_total','participants_assigned'),people_analyzed=x.get('participants_analyzed'),people_completed=pick(x,'participants_completed_total','denominator_complete'),trials_reported=pick(x,'trials_total','trials_analyzed','task_trials'),arm_trials=x.get('trials_arm'),teams=x.get('teams'),allocation_unit=x.get('allocation_unit'),assignment=pick(x,'assignment','randomization'),recruitment=x.get('recruitment'),exclusion=pick(x,'n_excluded_status','incompletion'),experience=pick(x,'expertise','experience'),prior_solution_knowledge=pick(x,'prior_solution_knowledge','prior_specific_solution_known','prior_knowledge'),prior_measure=x.get('prior_measure'),task=x.get('task'),intervention=pick(x,'intervention','permissions'),comparator=x.get('comparator'),cochanges=pick(x,'cointerventions','cochanges','changed_together'),timing=pick(x,'timing','timing_category'),exposure_open_adopt=pick(x,'link_display_open_adopt','exposed_read_adopted',default={'shown':x.get('shown'),'opened':x.get('opened'),'adopted':x.get('adopted')}),time_method=pick(x,'time_method','time_measurement'),time_start_end=pick(x,'time_start_end','time_stop_rule',default={'start':x.get('time_start'),'end':x.get('time_end')}),time_denominator=pick(x,'time_denominator','denominator_all'),time_result=pick(x,'time_reported',default=x.get('results',{})),quality_rule=pick(x,'quality_rule','quality_measure','quality_definition'),quality_result=pick(x,'observed_result',default=arm),quality_denominator=x.get('quality_denominator'),noncompletion=pick(x,'censoring','incompletion','time_stop_rule'),followup_rework=pick(x,'followup_rework','rework_window','post_adoption_rework_reason'),rework_effect=pick(x,'post_adoption_rework_value','post_adoption_rework_effect'),limitations=pick(x,'limitations','shared_caveat','causal_limit'),strand_record=x['_provenance'],detail_json={'study':x,'arm':arm})
  normalize_swb_study(out,x,arm)
  normalize_study_boundaries(out,x,arm)
  studies.append(out)
assert len({x['study_row_id'] for x in studies})==len(studies),'duplicate study row'
fields=list(studies[0]);write_csv(ROOT/'studies.csv',studies,fields)
canonical_studies={s['study_id']:s for s in studies}
studies_by_family=defaultdict(set)
for eid,study in canonical_studies.items():studies_by_family[study['study_family']].add(eid)
effects=[]
for x in read('effects'):
 sid=pick(x,'source_id',default=(x.get('source_ids') or [None])[0]);assert sid in source_map,(x.get('comparison_id'),sid)
 orig=pick(x,'original',default={k:x.get(k) for k in ['original_control','original_intervention','unit','statistic','time','quality'] if k in x})
 inputs=pick(x,'input',default={k:x.get(k) for k in ['original_control','original_intervention','n_intervention','n_control','n_all','n_complete','time','quality'] if k in x})
 result=pick(x,'result',default={k:x.get(k) for k in ['absolute_difference','ratio','percent_change','time_result','quality_results'] if k in x})
 out=dict(comparison_id=x['comparison_id'],study_family=x['study_family'],study_id=x.get('study_id'),source_ids=x.get('source_ids',[sid]),source_url=pick(x,'source_url',default=source_map[sid]['fixed_url']),locator=pick(x,'locator','read_locator'),outcome=pick(x,'outcome','measure',default='time and quality' if x.get('time') else 'reported non-time/qualitative outcome'),original_values=orig,recalculation_inputs=inputs,formula=pick(x,'formula','equations'),recalculated_result=result,denominator=pick(x,'denominator',default={k:x.get(k) for k in ['n_intervention','n_control','n_all','n_complete'] if k in x}),calculation_status=pick(x,'calculation_status','calculation',default='not_computable'),uncertainty=pick(x,'uncertainty',default=(x.get('time_result') or {}).get('ci_method')),noncompletion=pick(x,'noncompletion','missingness','missing'),reversal_condition=pick(x,'reversal_condition','limitations'),quality_caveat=pick(x,'quality_pair','quality_equivalence'),claim_ids=[x['claim_id']] if x.get('claim_id') else [],strand_record=x['_provenance'],detail_json=x)
 link_effect(out,x,source_map,canonical_studies,studies_by_family)
 normalize_other_effect_fields(out,x,canonical_studies[out['study_id']])
 normalize_swb_effect(out,x)
 effects.append(out)
assert len({x['comparison_id'] for x in effects})==len(effects),'duplicate effect'
write_csv(ROOT/'effects.csv',effects,list(effects[0]))
# Preserve every search/read attempt. Deduplicate identical IDs copied into summaries.
attempts=[];aid_seen={}
for x in read('attempts'):
 aid=x.get('attempt_id') or 'ATT-'+str(len(attempts)+1)
 if aid in aid_seen:
  if {k:v for k,v in x.items() if k!='_provenance'} != {k:v for k,v in aid_seen[aid].items() if k!='_provenance'}:
   x['attempt_id']=aid+'-copy'+str(len(attempts)+1)
  else:continue
 else:x['attempt_id']=aid
 aid_seen[x['attempt_id']]=x;attempts.append(x)
write_jsonl(ROOT/'attempts.jsonl',attempts)
screens=[]
for idx,x in enumerate(read('screening'),1):
 out=dict(screening_id=pick(x,'screening_id','screen_id',default='SCREEN-'+str(idx)),attempt_id=x.get('attempt_id'),source_id=pick(x,'source_id','fulltext_source_id'),study_family=x.get('study_family'),title=x.get('title'),url=x.get('url'),stage=pick(x,'stage',default='substantive_read' if x.get('full_text_read') else 'discovery'),decision=pick(x,'decision','disposition'),reason=x.get('reason'),query=x.get('query'),returned_rank=pick(x,'returned_order','returned_position','rank_returned'),strand_record=x['_provenance'],detail_json=x)
 screens.append(out)
# Root supplemental searches are discovered records, not primary readings; add first30 metadata.
for a in attempts:
 if not a.get('attempt_id','').startswith('ROOT-'):continue
 rs=pick(a,'results','returned_results',default=[])
 for k,x in enumerate(rs[:30],1):
  url=x.get('url');linked=next((s for s in sources if url in [s['fixed_url'],s['original_url']]+s.get('aliases',[])),None)
  screens.append(dict(screening_id=a['attempt_id']+'-R'+str(k),attempt_id=a['attempt_id'],source_id=linked['source_id'] if linked else None,study_family=linked['study_family'] if linked else None,title=x.get('title'),url=url,stage='D0_discovery',decision='source_linked' if linked else 'not_selected_for_fulltext_in_this_bounded_search',reason='supplemental discovery; no independent source count from search result',query=a.get('queries'),returned_rank=pick(x,'display_position','position',default=k),strand_record=a.get('_provenance'),detail_json=x))
assert len({x['screening_id'] for x in screens})==len(screens),'duplicate screening row'
write_csv(ROOT/'screening.csv',screens,list(screens[0]))
# Count experiments once, people are never summed across arm rows.
exp={};families=defaultdict(set)
for s in studies:
 if not s['included_core']:continue
 exp.setdefault(s['study_id'],s)
 families[s['study_family']].add(s['comparison_grade'])
family_classes={f:('direct_comparison' if 'R' in g else 'indirect_comparison' if g&{'Q','U'} else 'no_comparator') for f,g in families.items()}
cat_counts=Counter(s['count_category'] for s in sources if s['count_minimum'])
counts={'source_records_including_partial_and_discovery':len(sources),'source_record_count_note':'All source-ledger rows, including partial reads and discovery-only records; not a count of fully reviewed eligible originals.','minimum_eligible_unique_originals':sum(cat_counts.values()),'minimum_by_category':dict(cat_counts),'eligible_primary_families':len(families),'families_by_comparison_class':dict(Counter(family_classes.values())),'family_comparison_classes':family_classes,'experiments_by_comparison_grade':dict(Counter(s['comparison_grade'] for s in exp.values())),'eligible_experiments':len(exp),'source_rows':len(sources),'study_arm_rows':len(studies),'effect_rows':len(effects),'screening_rows':len(screens),'screening_unique_nonempty_urls':len(set(x['url'] for x in screens if x['url'])),'attempt_rows':len(attempts),'product_link_only_direct_families':len(set(s['study_family'] for s in studies if s['product_directness']=='L' and s['included_core'])),'post_adoption_rework_labor_compared_families':len(set(s['study_family'] for s in studies if s['rework_effect'] is not None and s['included_core'])),'classification_note':'R=within-study controlled/randomized or counterbalanced direct comparison; Q/U=indirect or allocation uncertain; O=no comparator. These are not product link-only effects. Family takes strongest available design; experiments counted separately.'}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in counts.items() if k!='family_comparison_classes'},ensure_ascii=False,indent=2))
