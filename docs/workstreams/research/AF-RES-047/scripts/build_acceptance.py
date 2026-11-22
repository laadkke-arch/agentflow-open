#!/usr/bin/env python3
"""Create an acceptance ledger that keeps unmet research conditions explicit."""
import csv
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / name).read_text())


def main():
    counts, summary, validation = load('source-count-summary.json'), load('analysis-summary.json'), load('evidence/validation.json')
    start, session = load('evidence/session-start.json'), load('evidence/session-check-before-result.json')
    items=[]
    def add(key,status,n,d,unit,evidence,reason='',next_step='',required=True):
        items.append({'id':key,'status':status,'numerator':n,'denominator':d,'unit':unit,
                      'evidence':evidence,'unmet_reason':reason or None,'minimum_followup':next_step or None,
                      'required_for_full_acceptance':required})
    add('owned_path','met',1,1,'repository scope check',['manifest.json allowed_paths','evidence/session-check-before-result.json stdout.outside_paths=[]','evidence/validation.json owned_path_only'])
    add('required_start_command','met',1,1,'actual command execution',['evidence/session-start.json','manifest.json created_at/integration/dependencies'])
    add('dependency_handoff_read','met',1,1,'fixed dependency',['evidence/input-receipt.json','SCOPE.md §1'],next_step='No same-round dependency waiting required.')
    add('model_environment_transparency','met',1,1,'manifest disclosure',['manifest.json research_context'],'', 'UI web-pro selector was not independently verified; no hidden model/backend claim.')
    add('first30_exposures_each','met',90,90,'metadata exposures, 30 per frame',['frame.csv data rows1–90','collection/rjournal/frame_all_metadata.json','collection/essd/issue1-receipt.json','collection/runs/frame-expanded-all.csv'])
    add('consumer_first_selection_strict','unmet',None,6,'cases with fully certified first-eligible ordering',['amendments.md A01/A02','collection/essd/frame-before-A01.csv','collection/essd/selection-amendment-A01.json'],
        'Initial ESSD selection conflated output-field lineage with eligibility; amendment remote commit followed publisher opening. Earlier ESSD5 third-party-input provenance remains uncertain; R Journal incidental early body exposures recorded.',
        'Resolve ESSD5 source producer/public availability, retain both cohorts; use an independent preregistered repeat for a strict prospective selection claim.')
    add('run_first_selection_strict','unmet',None,2,'cases with fully certified earliest eligible publication',['collection/runs/frame-first30.csv selected ranks5/18','collection/runs/frame-day-tie-amendment.json','collection/runs/findings.md'],
        'Earlier LivePublication actual run has unidentified public third-party input. Embedded datePublished/export dates are not independently established first publication dates.',
        'Identify LivePublication input producer/version and verify original public dates before claiming strict first2.')
    add('primary_slots','met',8,8,'case slots',['RESULT.md first table data rows1–8','consumers.csv data rows1–8','cases.json'])
    add('configurations','met',24,24,'case × A/B/C rows',['RESULT.md second table data rows1–24','readings.csv data rows1–24'])
    add('configuration_visibility_scoped','met',24,24,'evidence packets',['readings.csv visible_* and packet_boundary','amendments.md A07/A09','collection/rjournal/final-report-review.json','collection/runs/final-report-review.json'])
    add('C_missing_and_recipe_only_preserved','met',8,8,'C slots with explicit availability',['readings.csv C_slot_status','N-E01 C missing; RJ01/RJ03/N-E02 code-only; N-E00 output-only'])
    add('selected_exact_reported_value','partial',6,8,'cases with exact selected scalar/category',['consumers.csv reported_value','RJ01 Fig2 and N-E01 Fig5 remain non-keyed/exact-value missing'],
        'Two graphs do not provide an unambiguous first-point exact value. Alternative fields were not substituted.',
        'Obtain RJ01 source matrix/figure numeric output and N-E01 paired-point table.')
    add('direct_primary_minimum24','met',counts['quota_eligible_unique_works'],24,'unique directly read works in required roles',['source-count-summary.json quota_eligible_unique_works','sources.jsonl count_toward_minimum=true'])
    for category,n_required in counts['required_allocation'].items():
        add('quota_'+category,'met' if counts['allocation'].get(category,0)>=n_required else 'unmet',counts['allocation'].get(category,0),n_required,'unique works allocated once',['sources.jsonl minimum_category='+category,'source-count-summary.json allocation'])
    add('same_work_dedup','met',counts['conservative_unique_direct_works_admitted'],counts['conservative_unique_direct_works_admitted'],'admitted unique works',['evidence/validation.json admitted_work_unique','sources.jsonl work_id/duplicate_of; same_work_content_evidence_source_ids'])
    add('direct_read_vs_exposure_failure','met',1,1,'ledger distinction',['sources.jsonl access_status/count_reason','frame.csv exposure_type','ROOT-FINAL-03/04 failed reread rows'])
    add('first_open_UTC_exactness','partial',None,None,'individual first-open timestamps',['sources.jsonl time_precision/opened_utc/checked_utc','amendments.md A04','collection/essd/cases.json N-E02 publisher_first_attempted/opened'],
        'Some initial web opens were not clock-instrumented; later review timestamps and bounded intervals are not exact initial openings.',
        'Keep uncertainty; a prospective instrumented repeat is needed to remove this historical precision gap.')
    for layer,entry in [('natural',summary['natural_primary_after_A01']),('run_supplement',summary['execution_supplement'])]:
        for metric in ['publisher_exists','specific_usage','local_run_link','run_link','value_checked','candidate_value_checked']:
            add(f'observed_{layer}_{metric}','observed',entry[metric],entry['denominator'],'cases',['analysis-summary.json '+layer,'cases.json','readings.csv C'],required=False)
    add('authenticated_value_conditional_natural','not_applicable',0,0,'natural cases with publisher-correlated original input run',['analysis-summary.json natural_primary_after_A01.strict_value_given_authenticated_run=해당 없음'],
        'Natural-layer conditioning denominator is0. Do not report0% or infer any missing execution did not occur.',required=False)
    add('authenticated_value_conditional_run_supplement','observed',0,1,'supplement cases with publisher-correlated original input run',['analysis-summary.json execution_supplement.strict_value_given_authenticated_run','RUN02: original action + full R1 SHA + publisher MD5 line388'],
        'RUN02 input R is confirmed; selected CHROM value remains author-output reread, not independently checked V.',required=False)
    add('full_selected_FASTQ_comparison','met',1,1,'selected R1 input object with complete decoded comparison',['collection/runs/wetlab-full-fastq-execution-receipt.json exit0','collection/runs/wetlab-full-fastq-comparison.json','collection/runs/wetlab-full-checksum-revisit.json line388','amendments.md A10'],
        '', 'Acquisition/recompression time and other workflow inputs are outside the confirmed scope.')
    add('C_record_reread_count_separate','met',4,8,'cases with additional direct answer reread in C',['readings.csv record_reread','RJ02/N-E00/RUN01/RUN02 C; strictV remains0'])
    add('next_edition_slots_documented','met',8,8,'primary case comparison/absence slots',['contradictions.md §4','editions.csv','RESULT.md Q5 comparison table'])
    add('candidate_publisher_next_pair','observed',1,8,'cases with selected-field comparison of adjacent publisher candidates',['RJ03 R4.2.0→4.2.1; collection/rjournal/iris_value_comparison.json'],
        'Actual used edition is not identified. Author-output/crate pairs and simultaneous variants are separate.',required=False)
    add('strict_used_edition_next_pair','observed',0,1,'publisher-correlated original input objects with same-field next-publication comparison',['RUN02 original R1 representation matched publisher MD5','contradictions.md §4','collection/runs/wetlab-full-fastq-comparison.json'],
        'RUN02 input representation is authenticated in the stated record-based sense, but current gzip is not established as a dated next publisher edition and selected CHROM output is not independently compared.',required=False)
    add('same_value_multiple_editions','met',1,1,'required counterexample type',['RJ03 same iris.R bytes/Df; N-E00 author-output Group; AUX-EARTH-01 constant230Th'])
    add('same_value_different_row','met',1,1,'required counterexample type',['N-E00 auxiliary IOW Factors Baltic Sea!A148:B148','collection/essd/iow-edition-comparison.json sheet_comparisons[].same_numeric_cell_different_taxon_examples'])
    add('different_values_still_fit_narrow_purpose','met',1,1,'required counterexample type',['RJ03 UCI differing petals/SumSq but same3species Df2; purpose is limited statistics example','RESULT.md Q5'])
    add('metadata_correction_notice','met',1,1,'publisher-recorded metadata correction',['PANGAEA889928 Change history2021-09-24 authors list correction','collection/domain/findings.md §3'])
    add('metadata_only_payload_invariance','unmet',0,1,'empirical before/after payload pair',['contradictions.md §5'],
        'Correction notice exists, but pre/post payloads of that metadata-only event were not both retrieved. CPM33 primitive arrays do not prove every file property unchanged.',
        'Obtain authoritative payload snapshots immediately before/after the metadata-only correction.')
    add('different_URL_identical_bytes','met',1,1,'required empirical URL counterexample',['collection/domain/url-encoding-alias-check.json;9394bytes sameSHA','collection/runs/alias-provgen-receipts.json CAMELYON hostname alias'])
    add('stable_URL_same_bytes_unused_actual_run','unmet',0,1,'required empirical negative-use counterexample',['contradictions.md §3','RESULT.md Q6'],
        'No independent record proves a particular actual public analysis did not read the stable file. Future release timing and later preprocess do not establish that negative fact.',
        'Pair a stable publisher-object byte receipt with an actual run-exclusive input-read manifest or equivalent negative-use record.')
    add('five_item_removal','met',40,40,'case × evidence item removals',['sensitivity.csv','sensitivity-summary.json:17status changes,6already missing;external_run_link_changes=2;strict_value_positive_changes=0'])
    add('current_misuse_counterexamples','met',1,1,'documented rejection conditions',['IOW samecell differenttaxon/region; UCIpetalcorrection; N-E02 outputDOI156→235; CPM provenance edition mix','contradictions.md/RESULT.md Q5–Q7'])
    add('review_type_disclosed','met',1,1,'scope disclosure',['SELF_CHECK.md opening','collection/*/final-report-review.json'],
        '', 'External independent reader/adoption experiment was not performed and is not implied.')
    add('Q1_Q7_self_check','met',7,7,'questions with answer/reopened evidence/counterevidence/falsifier',['SELF_CHECK.md Q1–Q7','evidence/final-primary-reread.json','collection/review-reopens.jsonl'])
    add('mechanical_validation','met' if validation['status']=='passed' else 'unmet',validation['passed'],validation['total'],'requested structural invariants',['evidence/validation.json'])
    add('session_check_before_result','met' if session['exit_code']==0 else 'unmet',1 if session['exit_code']==0 else 0,1,'actual command run',['evidence/session-check-before-result.json'],required=True)
    add('fixed_result_remote_reread','pending',0,1,'post-commit fixedSHA reread',['to be recorded in evidence/fixed-result-reread.json after this result snapshot'],
        'Cannot truthfully self-embed a future commit hash or claim a reread before publication.',
        'Fetch RESULT.md and this ledger by their fixed result commit; preserve hashes/row counts in the following verification commit and HANDOFF.')
    add('final_handoff_single_commit','pending',0,1,'terminal HANDOFF-only commit',['to be verified against final commit diff'],
        'HANDOFF is intentionally written after fixed result reread and final session check.',
        'Publish HANDOFF.md alone as last commit; final diff and SHA in chat/ref.')
    value={'schema':1,'task_id':'AF-RES-047','generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'overall_research_acceptance':'partial','full_acceptance':False,
           'reason':'Source allocations and requested ledgers are present. Strict earliest-eligible/preregistration claims, exact first-open precision, exact values in2cases, metadata-only payload proof and negative-use counterexample remain limited/unmet.',
           'snapshot_semantics':'This ledger is fixed with RESULT. Post-commit reread and final HANDOFF outcomes are recorded later in evidence/fixed-result-reread.json, evidence/finalization-evidence.json and HANDOFF; pending here is temporal, not a false failure or a claim of completion.',
           'source_summary':counts,'case_summary':summary,'items':items}
    (ROOT/'evidence/acceptance-evidence.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'overall':value['overall_research_acceptance'],'criteria':len(items),'unmet_required':[i['id'] for i in items if i['required_for_full_acceptance'] and i['status'] in ['unmet','partial']]},ensure_ascii=False))


if __name__=='__main__':main()
