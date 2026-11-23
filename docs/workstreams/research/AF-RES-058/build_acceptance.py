"""Emit research acceptance evidence, separate from storage/contract success."""
import json
from pathlib import Path
from datetime import datetime, timezone
B=Path(__file__).resolve().parent
out=json.loads((B/'evidence/outcome-ledger.json').read_text())
con=json.loads((B/'evidence/contrast-ledger.json').read_text())
counts=json.loads((B/'evidence/source-counts.json').read_text())
conditions=[]
for r in out:
    if r['row_type']!='outcome':continue
    conditions.append({
        'outcome_id':r['record_id'],'case_id':r['case_id'],'stratum':r['stratum'],
        'condition':r['condition'],'advice_truth':r['advice_truth'],
        'allocation_unit':r['allocation_unit'],'analysis_set':r['analysis_set'],'dataset':r['dataset'],
        'planned':{'people':r['planned_people'],'advice_truth_trials':r['planned_D'],
                   'accept_n':None,'final_correct_n':None,'note':'Plans did not specify outcome successes; derived design denominators are not observed rows.'},
        'actual':{'analyzed_people_or_keys':r['analyzed_people'],'people_basis':r['people_basis'],
                  'judgeable_trials':r['observed_D'],'accept_n':r['accept_n'],'accept_D':r['accept_D'],
                  'final_correct_n':r['final_correct_n'],'final_correct_D':r['final_correct_D'],
                  'third_wrong_n':r['third_wrong_n'],'missing_in_file':r['missing_final_n'],
                  'original_assigned_missing':r['original_assigned_missing'],
                  'skipped':r['skipped'],'withdrawn':r['withdrawn'],'excluded_people':r['exclusions_people']},
        'advice_provided':r['advice_provided'],'pre_advice_answer':r['pre_advice'],
        'actual_reading':r['actual_reading'],'model_only_acceptance_percent':r['model_acceptance_percent'],
        'status':r['status'],'grade':r['grade'],'source_ids':r['source_ids'],
        'file':r['source_file'],'row_1_based':r['source_row'],'locator':r['locator'],
        'deficit':r['limits'],'next_minimum_input':r['next_input'] or '해당 source_file의 reason/limits와 reproduce.md에 적힌 원키·정오·최종답 또는 사전 종점 규약'}
    )
requirements=[
 {'id':'external_deep_works','planned':20,'actual':counts['unique_deep_primary_works'],'status':'PASS','basis':'sources.jsonl + evidence/works.csv; unique lineage, no search/internal/toy items'},
 {'id':'eight_table_positions','planned':8,'actual':8,'status':'PASS','basis':'RESULT.md table1 including explicit vacancies'},
 {'id':'eight_filled_studies','planned':8,'actual':6,'status':'FAIL_current_quantity','basis':'A03/A04 unfilled; diagnostic studies not substituted'},
 {'id':'selected_formal_papers','planned':8,'actual':5,'poster_separate':1,'status':'FAIL_current_quantity'},
 {'id':'separate_experiment_protocols_or_tools','planned':4,'actual_strict':2,'source_model_tools_separate':3,'status':'PARTIAL','basis':'Do not inflate with non-experiment repositories or count three Vasconcelos registrations separately'},
 {'id':'author_data_packages','planned':4,'actual':4,'status':'PASS','basis':'A01, D01, D03, D04; one package counted once'},
 {'id':'counter_or_adjacent_independent_papers','planned':4,'actual':7,'status':'PASS','basis':'D01–D07; within-paper experiments/reused people not added'},
 {'id':'primary_integer_acceptance_cells','planned':'correct and wrong by condition for all selected studies','actual':0,'status':'PARTIAL','basis':'44 primary outcome rows retain missing or structurally absent endpoint; no model inversion'},
 {'id':'at_least_one_public_denominator_hand_check','planned':1,'actual':2,'status':'PASS','basis':'D04 author Fig3/4 matched to raw 1600 rows/arm and A01 five-category counts sum50; more design checks separately'},
 {'id':'actual_stimulus_pair','planned':'at least one actual pair; report all inspected scope','actual':'A01 TA/TAB example; A02 poster; B03 two explanations; D03 Clear2/BB2; D06 Fig6','status':'PASS_limited_scope','basis':'No claim all items/assignments or external-link-reading assignment recovered'},
 {'id':'Q1_Q7_evidence_and_countersearch','planned':7,'actual':7,'status':'PASS_with_unidentified_answers','basis':'SELF_CHECK.md and RESULT.md Q1–Q7'},
 {'id':'frozen_remote_reopen_and_contract_check','planned':True,'actual':None,'status':'pending_after_result_commit','basis':'Will be observed at fixed result SHA and recorded in evidence/final-verification.json and final HANDOFF; not preclaimed'}
]
record={
 'schema':1,'task_id':'AF-RES-058','generated_utc':datetime.now(timezone.utc).isoformat(),
 'actor':'root assistant in shared workspace; explicit peer-review scope in SELF_CHECK.md',
 'research_status':'PARTIAL','all_requirements_satisfied':False,
 'product_claim_accepted':'설명 제공의 성과는 정권고 수락·오권고 수락·최종 정답을 분리해야 한다; 전체 정확도 상승만으로 오류 선별 개선을 판정하지 않는다.',
 'product_claim_withheld':'같은 소프트웨어 후보의 원문 링크를 실제 읽으면 틀린 권고를 더 잘 거른다.',
 'source_counts':counts,'requirements':requirements,
 'slots':[{ 'case_id':c,'status':'unfilled' if c in ('A03','A04') else 'selected_with_access_limit' if c=='A02' else 'selected',
            'primary_integer_acceptance_identified':False} for c in ('A01','A02','A03','A04','B01','B02','B03','B04')],
 'conditions':conditions,
 'missingness_records':[{'outcome_id':r['record_id'],'case_id':r['case_id'],'condition':r['condition'],'analysis_set':r['analysis_set'],'dataset':r['dataset'],'missing_in_file':r['missing_final_n'],'original_assigned_missing':r['original_assigned_missing'],'limits':r['limits'],'source_file':r['source_file'],'source_row':r['source_row']} for r in out if r['row_type']=='missingness'],
 'contrast_file':'evidence/contrast-ledger.json','contrast_rows':len(con),
 'primary_contrast_rows':sum(r['stratum'] in 'AB' for r in con),
 'diagnostic_observed_contrasts':sum(r['delta_accept_pp_observed'] is not None for r in con),
 'reversal_inputs':['A first-four eligibility and A02 formal paper','A01 deployed assignment/impression/docID and truth cutoff','B03 inclusion mask/weights/corrected integer crosstab','B04 item-period-condition/expert key/final responses','same-candidate assigned source-link reading and actual exposure, with pre-answer and final choice'],
 'verification_note':'This file is frozen before final remote re-open/session check; actual later receipt does not silently rewrite research status.'
}
(B/'evidence/acceptance-evidence.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'research_status':record['research_status'],'condition_rows':len(conditions),'missing_rows':len(record['missingness_records']),'source_works':counts['unique_deep_primary_works']}))
