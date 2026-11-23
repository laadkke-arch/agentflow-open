"""Verify research integrity separately from unmet research-completion gates.

Run from any directory; optional --output writes one receipt inside owned_path.
This does not run GDAL/SciPy/GeoPandas or certify scientific correctness.
"""
from pathlib import Path
import argparse,csv,datetime,hashlib,json,re,subprocess,sys
P=Path(__file__).resolve().parent
REPO=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=P,text=True).strip())
PREFIX=P.relative_to(REPO).as_posix()+'/'
SEAL='35d7e18024cced8cc81f9397b65e90e0e74bb907'
BASE='f736bd557fa4c40aecb6833165823196cfa42af2'
def j(path):return json.loads((P/path).read_text())
def jl(path):return [json.loads(l)for l in(P/path).read_text().splitlines()if l.strip()]
def csvrows(path):return list(csv.DictReader((P/path).open()))
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def check(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--require-handoff',action='store_true');args=parser.parse_args()
required=['RESULT.md','SCOPE.md','frame.csv','records.jsonl','proposals.csv','revisions.csv','sources.jsonl','attempts.jsonl','SELF_CHECK.md','REPRODUCE.md','manifest.json','evidence/preseal.json','evidence/denominators.json','evidence/rollback-receipt.json','patches/locations.json','streams/review/source-count-sensitivity.json']
if args.require_handoff:required.append('HANDOFF.md')
check('required_files',all((P/f).is_file()for f in required),[f for f in required if not(P/f).is_file()])
if not checks[-1]['pass']:raise SystemExit(json.dumps(checks,ensure_ascii=False))
records=jl('records.jsonl');sources=jl('sources.jsonl');proposals=csvrows('proposals.csv');revisions=csvrows('revisions.csv')
den=j('evidence/denominators.json');sc=j('evidence/source-counts.json');sens=j('streams/review/source-count-sensitivity.json');rollback=j('evidence/rollback-receipt.json')
core=[r for r in records if r['stratum']=='core'];selected=[r for r in core if r['status']=='SELECTED'];vacant=[r for r in core if r['status']=='VACANT']
expected={'G04-1','G04-2','G04-3','O02-1','O02-2','O02-3'}
check('six_original_slots',len(core)==6 and {r['record_id']for r in core}==expected)
check('selected_and_vacant_counts',len(selected)==den['core_selected']==2 and len(vacant)==den['core_vacant']==4)
check('one_independent_core_guide',len({r['lineage_id']for r in selected})==den['core_independent_downstream_guides']==1)
check('actual_consumer_builds_not_invented',den['actual_consumer_installed_builds']==0 and den['new_consumer_functional_executions']==0)
seal_results=[]
for f,h in j('evidence/preseal.json')['hashes'].items():
 local=(P/f).read_bytes();old=subprocess.check_output(['git','show',SEAL+':'+PREFIX+f],cwd=REPO)
 seal_results.append({'path':f,'expected_sha256':h,'working_sha256':sha(local),'sealed_blob_sha256':sha(old),'same':sha(local)==h==sha(old)})
check('sealed_protocol_records_frame_AB_unchanged',all(r['same']for r in seal_results),seal_results)
for rid in sorted(expected):
 ps=[r for r in proposals if r['record_id']==rid]
 check('AB_pair_'+rid,len(ps)==2 and {r['policy']for r in ps}=={'A','B'} and all(r['consumer_followup_read_before_proposal'].lower()=='false'for r in ps))
check('core_A_holds_two_actual_records',all(next(p for p in proposals if p['record_id']==r['record_id']and p['policy']=='A')['action']=='보류'for r in selected))
check('no_retroactive_AUX_G04_AB_pair',not any(p['record_id']=='AUX-G04-A1'for p in proposals))
check('core_revisions_cover_six_slots',{r['record_id']for r in revisions if r['stratum']=='core'}==expected)
check('core_AB_correctness_denominator_zero',den['core_correctness_comparison_denominator']==0 and all(r['correctness_denominator_eligible'].lower()=='false'for r in revisions))
ids={r['source_id']for r in sources}
check('unique_source_ids',len(ids)==len(sources),{'rows':len(sources),'ids':len(ids)})
fields=['source_id','lineage_id','source_type','url','fixed_version','direct_read_utc','questions','observed','limitations','opened_utc_precision']
missing=[{'source_id':r['source_id'],'fields':[f for f in fields if not r.get(f)]}for r in sources if any(not r.get(f)for f in fields)]
check('source_ledger_required_content',not missing,missing)
check('source_ledger_locations',all(r.get('location')or r.get('lines')for r in sources))
check('direct_read_not_attempt',all(r['directly_read']and r['url'].startswith('https://')for r in sources))
attempts=jl('attempts.jsonl');check('attempts_excluded',all(r.get('counts_minimum')is False for r in attempts),len(attempts))
unknown=[(r['record_id'],s)for r in records for s in r.get('source_ids',[])if s not in ids]
check('record_source_references',not unknown,unknown)
references=[]
for r in proposals:
 for sid in re.split(r'[;\s]+',r.get('source_ids','').strip()):
  if sid and sid not in ids and sid not in {'079-G04','old-search.json'}:references.append((r['proposal_id'],sid))
check('proposal_source_references',not references,references)
check('special_dependency_and_search_references_resolve',(P/'streams/root/dependency-observations.json').is_file()and(P/'streams/oss/old-search.json').is_file())
unknown=[]
for r in revisions:
 for sid in re.split(r'[;\s]+',r.get('source_ids','').strip()):
  if sid and sid not in ids and sid!='old-search.json':unknown.append((r['record_id'],sid))
check('revision_source_references',not unknown,unknown)
strict=set(sc['strict_lineage_ids']);mapping=sens['conservative_count_group_mapping'];groups={mapping.get(x,x)for x in strict};stress={sens['additional_stress_folds'].get(x,x)for x in groups}
check('material_counts',len(sources)==sc['direct_source_rows']==den['direct_source_rows']==124 and len(attempts)==sc['attempt_rows_excluded']==den['attempt_rows_not_counted']==33)
check('conservative_source_threshold',len(groups)==sens['conservative_count']==den['conservative_count_groups']==25 and len(stress)==sens['stronger_same_workflow_stress_count']==den['stronger_same_workflow_stress_groups']==23 and len(stress)>=20)
check('downstream_original_threshold',sc['downstream_guide_lineages']==den['downstream_guide_lineages']==11 and sc['downstream_guide_lineages']>=6)
ext=j('streams/external/evidence/counts-and-self-check.json')
check('external_events_and_two_endpoints',ext['actual_event_lineages']==den['external_actual_events']==5 and ext['library_authority_events']==2 and ext['scholarly_publishing_events']==3 and ext['two_endpoint_direct_reads']==5 and ext['historical_raw_before_after_pairs']==1)
check('no_duplicate_consumer_application_claim',ext['actual_duplicate_consumer_application_events']==den['external_actual_duplicate_consumer_application_events']==0)
patch_records=rollback['records'];check('research_patch_denominator',rollback['research_records']==2 and rollback['vacancy_patches']==0 and {r['record_id']for r in patch_records}=={r['record_id']for r in selected})
patch_results=[]
for r in patch_records:
 rid=r['record_id'];before=(P/'evidence/repairs/before'/f'{rid}.json').read_bytes();after=(P/'evidence/repairs/after'/f'{rid}.json').read_bytes();b=json.loads(before);a=json.loads(after)
 ok=(sha(before)==r['before_sha256']and sha(after)==r['after_sha256']and b['original_record_from_seal']==a['original_record_from_seal']and b['sealed_assessments']==a['sealed_assessments']and r['reversed_to_identical_bytes']and all(s['exit_code']==0 and s['byte_equal']for s in r['steps']))
 patch_results.append({'record_id':rid,'pass':ok,'before_sha256':sha(before),'after_sha256':sha(after)})
check('research_forward_reverse_bytes_and_old_citations',all(r['pass']for r in patch_results),patch_results)
loc=j('patches/locations.json')
check('publisher_and_research_IDs_distinct',all(r['research_patch_id'].startswith('RESEARCH-')and r['publisher_patch_id'].startswith('PUBLISHER-')and r['publisher_diff_is_separate']for r in loc))
check('patches_directory_only_diffs_and_locations',all(f.name=='locations.json'or f.name.endswith(('.forward.diff','.reverse.diff'))for f in(P/'patches').iterdir()))
fps=j('streams/gis/postseal/record-fingerprints.json')
view_checks=[]
for r in loc:
 for key,v in zip(['geopandas','first','latest'],r['actual_release_views']):view_checks.append(v['source_span_sha256']==fps[key][r['record_id']]['sha256']and v['consumer_commit']in v['source_url'])
check('three_editions_bidirectional_views',len(view_checks)==6 and all(view_checks))
for f in ['RESULT.md','SELF_CHECK.md']:
 txt=(P/f).read_text();check('Q1_to_Q8_'+f,all('Q'+str(i)in txt for i in range(1,9)))
 check('partial_and_no_zero_over_zero_rate_'+f,'PARTIAL'in txt and '산출 불가'in txt)
result=(P/'RESULT.md').read_text();check('required_table_order',result.index('## 표1.')<result.index('## 표2.')<result.index('## 표3.')<result.index('## 분모'))
last=result.split('## 결론을 바꿀 중요한 불일치·약점')[1]
check('exactly_three_final_weaknesses',len(re.findall(r'^\d\. \*\*',last,re.M))==3 and last.count('**다음 조사:**')==3)
broken=[]
for f in ['RESULT.md','SELF_CHECK.md','REPRODUCE.md']:
 for target in re.findall(r'\]\(([^)]+)\)',(P/f).read_text()):
  if '://'in target or target.startswith('#'):continue
  path=target.split('#')[0]
  if path=='HANDOFF.md'and not args.require_handoff:continue
  if not(P/path).exists():broken.append((f,target))
check('local_report_links',not broken,broken)
changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=REPO,text=True).splitlines()
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=REPO,text=True).splitlines()
outside=[f for f in changed+untracked if not f.startswith(PREFIX)]
check('owned_path_only',not outside,outside)
check('completion_gates_remain_partial',den['status']=='PARTIAL'and not den['completion_gates']['six_actual_original_instructions']and not den['completion_gates']['independent_correctness_denominator_nonzero'])
receipt={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'target_kind':'HEAD plus the explicitly hashed working files; exact final-commit rerun recorded in HANDOFF','checks':checks,'integrity_pass':all(r['pass']for r in checks),'integrity_check_count':len(checks),'research_completion_status':den['status'],'completion_gates':den['completion_gates'],'consumer_functional_tests_run':False,'exit_code':0 if all(r['pass']for r in checks)else 1}
if args.output:
 out=Path(args.output).resolve();out.relative_to(P);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2));sys.exit(receipt['exit_code'])
