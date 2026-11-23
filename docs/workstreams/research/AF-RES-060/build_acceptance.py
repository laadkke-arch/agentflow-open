"""Count acceptance evidence, preserving missing data and unperformed final gates."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,hashlib,subprocess

P=Path(__file__).resolve().parent
def rj(f):return json.loads((P/f).read_text())
def rc(f):return list(csv.DictReader((P/f).open(encoding='utf-8')))
plan=rj('evidence/acceptance-plan.json');metrics=rj('evidence/comparison-summary.json');sc=rj('evidence/source-counts.json');fr=rj('evidence/feature-freeze.json')
fs=rc('features.csv');paths=rc('paths.csv'); reqs=rj('requirements.json')
assert len(fs)==62 and len(paths)==84 and len(reqs)==12
assert hashlib.sha256((P/'features.csv').read_bytes()).hexdigest()==fr['sha256']['features.csv']
observed={}
def add(id,n,d,status,files,limit='',next_='none required for this bounded criterion'):
    observed[id]={'actual_numerator':n,'actual_denominator':d,'status':status,'evidence':files,'missing_or_limit':limit,'next_minimum_check':next_}
add('contract',1,1,'observed_pass',['manifest.json','evidence/start-receipt.json'],'Actual cloud executor ran command; web-pro is assigned role, not a separate UI actor.')
add('exact_inherited_core_files',9,9,'observed_pass',['evidence/input-byte-audit.json','inputs/af-res-056/'])
add('fixed_catalog',62,62,'observed_pass',['inputs/af-res-056/catalog.csv rows2-63'])
add('f0_replay',16,16,'observed_pass',['evidence/baseline-replay.json/checks','evidence/review/stage3-audit.json'])
add('stage1_before_feature_edit',1,1,'observed_pass',['evidence/publication-log.json stage1','SCOPE.md'],'Remote8781899 at03:19:24UTC precedes registered supplier reads.')
add('uniform_feature_attempts',62,62,'observed_pass',['features.csv rows2-63'],'54 nonempty,8 explicit blanks; no per-requirement editing.')
add('three_feature_cap',sum(len(json.loads(f['added_features_json']))<=3 for f in fs),62,'observed_pass',['features.csv added_features_json rows2-63'])
add('two_document_primary_cap',sum(int(f['primary_document_actions_attempted'])<=2 for f in fs),62,'registered_cap_pass_with_exposure_limit',['features.csv primary_document_actions_attempted','evidence/feature-freeze.json'],'Retries and discarded interpretation windows are separately recorded; no claim of zero extra exposure.')
add('primary_window_cap',75,75,'partial_due_to_extra_exposure',['evidence/feature-freeze.json','evidence/features-ld/','evidence/features-schema/'],'Registered75 windows each <=500; discarded interpretation views add1411 words before holdout.','A fresh independent replay can assess rule reproducibility; preserve original exposure.')
add('version_and_role_provenance',62,62,'partial',['features.csv implementation_sha/version_status/version_and_role_limits_json'],'All rows disclose pin or blank/limit; component releases, exact-day responses and some last-release claims unconfirmed.','Acquire component release and historical response provenance; do not replace frozen ranking input silently.')
add('acquisition_costs',62,62,'partial',['features.csv cost columns','evidence/feature-freeze.json','evidence/cost-audit.json'],'Metadata>=190 is retained-receipt lower bound; elapsed time/token/currency unmeasured.','Recover missing initial metadata/retry receipts for exact physical total.')
add('stage2_before_holdout',1,1,'observed_pass',['evidence/publication-log.json stage2','evidence/holdout/stage2-gate.json'],'Remote412192e at03:39:14UTC; selector gate03:39:42UTC, before first request body.')
add('current_tag_frame',35,40,'partial_target_pool_exhausted',['holdout.csv rows2-41','evidence/holdout/frame.json'],'Schema20/20,LD15/20 current-tag questions; five pool-exhausted positions preserved. Not a historical population.','No replacement by later/other-tag questions; separately preregister any broader frame.')
add('original_body_screening',35,40,'partial_target_pool_exhausted',['holdout.csv rows2-41','evidence/holdout/body-locations.json'],'All35 available revision1 bodies directly read; five frame positions absent, zero acquisition failures.','No invented bodies; revision grace-period edits remain outside available original record.')
add('new_requirement_slots',4,4,'observed_pass',['requirements.json JS-5/JS-6/LD-5/LD-6','evidence/holdout/selection-correction.json'],'First2 eligible per family; code-preservation C2 is distinguished from prose; correction before ranking.')
add('requirement_contracts',12,12,'observed_pass',['requirements.json all12 case IDs'],'Positive/near-negative fixtures are mostly researcher constructions, not execution evidence.')
add('new_vocabulary_frozen',1,1,'observed_pass',['vocabulary.csv rows2-60','evidence/requirements-freeze.json','evidence/holdout/vocabulary-amendment.json'],'LD5 dataset/Turtle IO mismatch withheld before new ranking.')
add('stage3_before_path_judgment',1,1,'observed_pass',['evidence/publication-log.json stage3','evidence/path-plan.json','evidence/review/stage3-audit.json'],'Remote5d01a620 at03:55:35UTC; inherited old judgments are explicitly prior exposure.')
add('four_way_comparisons',48,48,'observed_pass',['matches.csv rows2-49','RESULT.md first table rows1-48'],'All48 ranked; no missing requirement cells.')
add('three_slots',144,144,'observed_pass',['slots.csv rows2-145'],'18 filled,111 observed-no-match,15 matched-pool-exhausted; unknown judgments not empty slots.')
add('all_entered_displaced_candidates',28,28,'observed_pass',['evidence/path-plan.json/cases','evidence/candidate-verdicts.json','changes.csv rows2-13'],'All43 occurrences collapsed to28 unique pairs; includes ranks4+ and displaced candidates.')
add('same_path_conditions',84,84,'partial_protocol',['paths.csv rows2-85','evidence/comparison-summary.json','evidence/paths-ld/preview-exposure.json'],'84 provenance/judgment rows, same-path aggregation;81 strict budget-confirmed,2 overexposed and1 inherited boundary gap. Complete0,partial3,unconfirmed81.','Fresh bounded replication for two overexposed paths; original titleless JSON receipt for inherited gap.')
add('external_distinct_primary_works',sc['distinct_qualifying_works'],sc['distinct_qualifying_works'],'observed_threshold_pass',['sources.jsonl rows1-'+str(sc['source_events']),'evidence/source-counts.json','evidence/review/final-audit.json'],'Threshold22;113 deduplicated substantive works,95 new. Events and engines are separate.')
add('allocation_new_requests',4,4,'observed_pass',['sources.jsonl source_id H-SO-S01/H-SO-S02/H-SO-L01/H-SO-L03'],'35 screened request works,4 selected.')
add('allocation_suppliers',8,8,'observed_threshold_pass',['sources.jsonl F-SC-001/004/008/009/016/021/022 and F-LD-008','evidence/review/final-audit.json'],'Eight named different-provider exemplars;59 provider works total=57 listed+2 linked utility, not59 independent engines.')
add('allocation_standards_tests',7,7,'observed_threshold_pass',['sources.jsonl STD-SC-CORE07/VALID07,STD-LD-API11/FRAME11 plus suite/meta-schema/RFC6901','evidence/review/final-audit.json'],'Threshold4 fulfilled by four preregistered definition works; total7=6 reused+1 new.')
add('allocation_catalog_editorial',2,2,'observed_pass',['sources.jsonl CAT-SCHEMA-CONTRACT/CAT-LD-INDEX'],'Both reread existing works, no new-list reconstruction.')
add('allocation_authority_records',4,4,'observed_pass',['evidence/authority/record-observations.json','evidence/authority/sources.jsonl'],'LOC2+Getty2 actual new records; JSON/XML/HTML versions collapsed.')
add('q1_q7_refutations',7,7,'observed_pass',['SELF_CHECK.md Q1-Q7 table','RESULT.md sections4-10'],'Counterexample reasoning and author examples are not actual provider executions.')
add('result_first_tables',60,60,'observed_pass',['RESULT.md first table48 rows;second table12 rows'])
add('final_weakness_table',3,3,'observed_pass',['RESULT.md final table exactly3 body rows'])
add('cards',12,12,'observed_pass',['cards.md JS-1..JS-6 and LD-1..LD-6'],'Whole implementation0,conditional complement1,clarify/hold11; literal-only sensitivity changes conditional to hold.')
add('sensitivities',2,3,'partial_explicit_not_run',['evidence/sensitivity-summary.json','RESULT.md section9'],'Top4 and feature1 ranking executed; direct-link alternative separated and explicitly not run. Extra literal/unsafe-query diagnostics separate.','If direct-link gain is wanted, preregister a navigation intervention and fresh readers; do not attribute hypothetical gain to F1.')
add('source_ledger',165,165,'observed_pass',['sources.jsonl','evidence/review/final-audit.json'],'All165 qualifying events have normalized required fields and resolved counter/source IDs;193 total events include failures/metadata/internal input.')
for key,files in [('fixed_remote_result_reread',['evidence/verification/remote-reread.json']),('session_check_fetch',['evidence/verification/session-check.json'])]:
    receipt=P/files[0]
    if receipt.exists():
        rr=json.loads(receipt.read_text());ok=rr.get('all_equal',rr.get('exit_code')==0)
        add(key,2 if key=='fixed_remote_result_reread' and ok else 1 if ok else 0,2 if key=='fixed_remote_result_reread' else 1,'observed_pass' if ok else 'observed_failure',files,rr.get('interpretation','Actual command/read only; not semantic research certification.'))
    else:add(key,0,2 if key=='fixed_remote_result_reread' else 1,'pending_after_result_commit',files,'Will be performed against a fixed remote result commit before HANDOFF.','Execute and retain exact SHA/time/bytes or exit/stdout/stderr.')
add('owned_paths_only',1,1,'observed_pass',['manifest.json','evidence/verification/local-integrity.json'],'All recorded writes under owned path; dot-control unchanged. Rechecked at publication.')
add('handoff_last_single_file_commit',None,1,'deferred_to_final_commit_verification',['HANDOFF.md final standalone commit; final remote ref tool receipt'],'Cannot put its own commit SHA inside the same commit. Verified immediately after final publication; no claim before action.','Verify final commit changed exactly HANDOFF.md and local working tree has no uncommitted deliverables.')
assert set(observed)=={c['id'] for c in plan['criteria']}
criteria=[dict(c,**observed[c['id']]) for c in plan['criteria']]
verified_result=rj('evidence/verification/remote-reread.json').get('commit_sha') if (P/'evidence/verification/remote-reread.json').exists() else None
out={'task_id':'AF-RES-060','counted_utc':datetime.now(timezone.utc).isoformat(),'research_status':'partial_handoff','artifact_status':'result_published_and_reread; session check observed; final HANDOFF verification remains separate' if verified_result and (P/'evidence/verification/session-check.json').exists() else 'result_bundle_prepared; final publication/check gates separately observed','verified_result_commit':verified_result,'planned_criteria':len(criteria),'criteria':criteria,
'denominator_summary':metrics,'source_counts':{k:sc[k] for k in ['source_events','qualifying_direct_source_events','distinct_qualifying_works','distinct_new_works']},
'immutable_input_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['features.csv','requirements.json','vocabulary.csv','matches.csv','holdout.csv']},
'execution_status':{'ranking_replay':'performed','source_and_denominator_audit':'performed','supplier_install_or_behavior_tests':'not_run','original_user_success':'not_observed'},
'reviewers_and_scope':['root synthesis and fixed input/selected-body/standards/SC032/new path review','features_schema17pairs51paths','features_ld9pairs27paths','authority35holdout bodies+4actualauthority records+independentranking/source/denominator audit','LD secondary review4pairs12paths10windows; Schema secondary review6Ajv/Blaze windows; same model family, not blind human replication'],
'non_equivalence':'Files saved, machine contract checks passed, and research criteria fully met are separate claims.'}
(P/'evidence/acceptance-evidence.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
cost={'units':'do not add rows, works, actions, physical requests or words as if interchangeable','editor':fr,'paths':{'new_logical_document_actions':130,'inherited_logical_actions':5,'all_logical_actions':135,'new_registered_logical_words':51095,'inherited_known_words':2000,'inherited_unknown_windows':1,'all_known_registered_words':53095,'preview_unique_over_window_words':111,'preview_logical_excess_two_paths':222,'new_body_requests':29,'new_metadata_requests':6,'unique_window_sums_by_team':{'schema':9858,'ld':6518,'root':1168},'warning':'Team unique-window sums overlap shared HOME/spec/cache and are not a global deduplicated read-cost total.'},'F0_historical_creation_cost':'not_remeasured; inherited files/replay only','currency_tokens_wallclock':'not_measured'}
(P/'evidence/cost-audit.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'criteria':len(criteria),'research_status':out['research_status'],'pending':[c['id'] for c in criteria if c['status'].startswith('pending')]}))
