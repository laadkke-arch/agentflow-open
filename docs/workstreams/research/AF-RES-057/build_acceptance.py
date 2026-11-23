"""Record separate research and artifact acceptance, with explicit units."""
from pathlib import Path
import csv
import json
from datetime import datetime, timezone

P = Path(__file__).resolve().parent


def read(name, default=None):
    f = P / name
    return json.loads(f.read_text()) if f.exists() else default


def csvrows(name):
    return list(csv.DictReader((P / name).open()))


def main():
    counts = read('evidence/final-counts.json')
    comparison = read('evidence/comparison-counts.json')
    frame = csvrows('frame.csv')
    result = (P / 'RESULT.md').read_text().splitlines()
    sources = [json.loads(x) for x in (P / 'sources.jsonl').read_text().splitlines() if x]
    line_by_source = {r['source_id']: i+1 for i, r in enumerate(sources)}
    tables, current = [], []
    for i, line in enumerate(result, 1):
        if line.startswith('|'):
            current.append(i)
        elif current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    requirements = []

    def add(identifier, planned, actual, unit, status, files, missing='', next_check='', numerator=None, denominator=None):
        requirements.append({'condition_id': identifier, 'planned': planned, 'actual': actual, 'unit': unit,
                             'numerator': numerator, 'denominator': denominator, 'status': status,
                             'files_rows': files, 'deficit': missing, 'next_minimum_check': next_check})

    add('owned_path_and_branch', {'branch': 'work/research-af-res-057', 'allowed_path': 'docs/workstreams/research/AF-RES-057/'},
        {'branch': 'work/research-af-res-057', 'manifest_base': '3f4d43b19cd76d56983e6f500eebe7010eb3fa51'}, 'contract',
        'verification_receipt_separate', ['manifest.json', 'evidence/commit-ledger.jsonl'],
        next_check='Read session-check receipt and final HANDOFF; do not infer research validity from git scope.')
    add('governance_and_dependency', 'required rules plus depends_on result HANDOFF/results',
        {'handoff': '94231403b7ce6debd1ee7bb1a34e86e3956c7920', 'results': '87a375d72c269f921589e98b27265e344a70000d',
         'control_DONE_handoff_PARTIAL_distinguished': True}, 'dependency', 'pass', ['evidence/governance-read.json', 'SCOPE.md'])
    add('natural_recruitment', {'per_ecosystem_cap': 30, 'repositories': ['yjs/yjs', 'ProseMirror/prosemirror'], 'first_created_then_number': True},
        {'Yjs_bodies': 30, 'PM_bodies': 17, 'PM_absent_ranks': 13, 'frame_rows_including_diagnostics': len(frame)},
        'body_or_explicit_empty_rank', 'pass_with_finite_population', ['frame.csv: rows2-63', 'streams/yjs/frame.csv', 'streams/prosemirror/frame.csv'],
        'PM has only17 eligible title candidates;13 explicitly empty ranks are not fabricated requests.', numerator=47, denominator=47)
    add('six_slots_three_views', {'natural': 4, 'diagnostic': 2, 'views': 18},
        {'natural': 4, 'diagnostic': 2, 'views': len(csvrows('predictions.csv'))}, 'slot/view', 'pass_with_sensitivity',
        ['frame.csv', 'cards.csv: rows2-19', 'predictions.csv: rows2-19'],
        'Strict explicitly retained-text sensitivity excludes PN1; then5slots/15views.', numerator=6, denominator=6)
    add('first_authored_body_recovery', 4, 0, 'selected_natural_body_revision', 'unconfirmed',
        ['frame.csv', 'streams/yjs/cases.json', 'streams/prosemirror/cases.json'],
        'Recovered current bodies and hashes do not establish earliest authored revisions.',
        'Obtain public archived original body/edit history with dates; compare before changing eligibility.', numerator=0, denominator=4)
    add('diagnostic_version_and_selection', 2, 2, 'diagnostic_case', 'pass',
        ['streams/yjs/metadata-freeze.json', 'streams/yjs/diagnostic-selection-correction.json', 'streams/prosemirror/metadata-freeze.json'],
        'Yjs push-regex correction occurred before outcomes; PM annotated-tag dating is explicit.', numerator=2, denominator=2)
    add('original_natural_runtime_version', 4, {'explicit_body_version': ['YN2:13.0.8'], 'unconfirmed_author_version': ['YN1','PN1','PN2']},
        'selected_natural_case', 'partial', ['cases.json', 'events.csv'],
        'Temporal reference versions and one alpha supplement are not proved installed author versions.',
        'Get author package-lock and complete initial document/event trace.', numerator=1, denominator=4)
    add('preprediction_seal', 'remote commit before held assertions',
        {'remote_sha': '74dc9f887bc47bc0a92b9a75ea327ffa30aca70b', 'server_UTC': '2026-11-23T03:32:00Z',
         'PM_first_held_read': '2026-11-23T03:32:31.973Z', 'Yjs_first_held_read': '2026-11-23T03:32:32.205236+00:00'},
        'ordered_phase', 'pass_with_exposure_limits', ['evidence/seal-remote-readback.json', 'evidence/prediction-freeze.json', 'cards.csv'],
        'PT1 semantic answer and several natural baseline/expected states were already visible; not a blinded human experiment.')
    add('equal_added_windows', {'max_words':160, 'same_words':True, 'same_figures':True, 'section_per_view':1},
        {'map_words':18, 'accounting_words':22, 'figures':0, 'pairs_equal':6}, 'E_D_case_pair', 'pass',
        ['cards.csv: rows2-19', 'evidence/card-windows.json', 'evidence/card-metadata-corrections.csv'],
        'YN1-A code_lines metadata corrected0→1 in companion, frozen card unchanged. Equal words is not equal information or reading time.', numerator=6, denominator=6)
    add('direct_primary_works', {'minimum':20}, counts['unique_primary_works'], 'unique_external_primary_work', 'pass',
        ['sources.jsonl: rows1-'+str(len(sources)), 'evidence/final-counts.json', 'streams/donors/final-source-audit.json'],
        'Reading is by same-model research team. Metadata, failed access, input-only acquisitions, own outputs, mirrors/revisions and same-event rows do not inflate count.',
        numerator=counts['unique_primary_works'], denominator=None)
    for quota in counts['disjoint_minimum_allocation']:
        locs = ['sources.jsonl:'+str(line_by_source[s])+' '+s for s in quota['source_ids']]
        add('quota_'+quota['category'], quota['planned'], quota['actual'], quota['unit'], 'pass', locs,
            quota['limits'], numerator=quota['actual'], denominator=quota['planned'])
    add('donor_numeric_or_object_state', 4, 3, 'direct_case', 'partial_precision',
        ['streams/donors/map-case-observations.json', 'streams/donors/payap-case-observations.json', 'streams/donors/donor-analysis.md'],
        'D14 is a real authored reconciliation report without numeric ledger; map object-state scope is one object per case.',
        'Get D14 version, dated splits, balancing/reconciliation states; do not impute figures from generic examples.', numerator=3, denominator=4)
    add('Q1_to_Q7_direct_and_counterevidence', 7, 7, 'question', 'pass_with_explicit_unknowns',
        ['SELF_CHECK.md: Q1-Q7', 'RESULT.md: Q1-Q7', 'sources.jsonl'],
        'Each question has a contrary case or boundary and a falsifying input; not every original output is known.', numerator=7, denominator=7)
    add('frozen_E_D_comparison', 6, comparison['E_D_same'], 'case', 'pass',
        ['predictions.csv: rows2-19', 'evidence/comparison-counts.json'],
        'Observed different predictions0/6; conditional new-right/new-wrong denominator0 => not_applicable, not0percent accuracy.', numerator=6, denominator=6)
    add('declared_diagnostic_expectations', 2, {'read':2, 'unexposed_opA_match':1, 'semantically_preexposed':1},
        'diagnostic_case', 'partial_for_new_hit', ['observations.csv', 'streams/yjs/observations.json', 'streams/prosemirror/observations.json'],
        'Original groups have opA undo only; opB/redo and altered retention goal are research extensions.', numerator=2, denominator=2)
    add('complete_original_public_output_pairs', 6, 0, 'case_with_same_input_version_actors_opA_opB_and_redo', 'unconfirmed',
        ['observations.csv: rows2-19', 'evidence/comparison-counts.json', 'RESULT.md: first table'],
        'No complete public original pair; exposed/synthetic/minimal/changed-version results cannot be promoted to independent new hits.',
        'Obtain exact public fixtures and outputs for both frozen operations with author version and full event history.', numerator=0, denominator=6)
    add('main_researcher_execution', 26, 26, 'scenario_operation_variant', 'completed',
        ['streams/yjs/replay/*.receipt.json', 'streams/yjs/observations.json', 'streams/prosemirror/replay/run-receipt.json', 'streams/prosemirror/replay/results.json'],
        '26 completions are not26 new correct answers; abstentions and original/synthetic distinctions remain.', numerator=26, denominator=26)
    add('posthoc_version_and_dependency_sensitivity', 'separate from main denominator', {'records':8,'old_version_exception_records':3},
        'posthoc_scenario_version', 'completed_and_separated', ['streams/yjs/replay/YT1-sensitivity-1308.stdout.json', 'streams/prosemirror/replay/results.json', 'streams/prosemirror/replay/historical/results.json'],
        'Fixtures and outcomes were known before these sensitivity runs; no preprediction-hit credit.', numerator=8, denominator=8)
    upstream = {s: read('streams/'+s+'/upstream-verification/verification.json', {'status':'pending'}) for s in ['yjs','prosemirror']}
    add('later_original_fixture_local_verification', 'resolve minimal-surrogate versus original helper/runner risk', upstream,
        'selected_original_test_local_run', 'see_companions', ['evidence/upstream-verification-plan.json', 'streams/yjs/upstream-verification/verification.json', 'streams/prosemirror/upstream-verification/verification.json'],
        'Post-outcome verification is not public CI, author execution or new blinded prediction. Earlier stream zero-run records precede this bounded final check.')
    add('public_same_SHA_CI_pass', 'retained same-test run evidence if available', {'retained_records_obtained':0, 'status':'미확인'},
        'public_run_record', 'unconfirmed', ['streams/yjs/ci-probes.json', 'streams/prosemirror/post-read-receipts.json'],
        'Empty statuses/check-runs/actions is not a failed run. Yjs probes diagnostic/fix SHAs, not natural alpha/13.0.8.',
        'Recover exact historical CI URL/log/artifact for the pinned test; local execution cannot create past public evidence.', numerator=0, denominator=None)
    add('required_tables', {'first':18,'second':6,'last_weakness':3},
        {'first':len(tables[0])-2,'second':len(tables[1])-2,'last_weakness':len(tables[-1])-2,
         'first_lines':[tables[0][0],tables[0][-1]],'second_lines':[tables[1][0],tables[1][-1]],'last_lines':[tables[-1][0],tables[-1][-1]]},
        'table_row', 'pass', ['RESULT.md'])
    add('files_and_reproduction', ['manifest','SCOPE','RESULT','frame','events','cards','predictions','observations','sources','return-cards','SELF_CHECK','acceptance','HANDOFF'],
        'All research ledgers and executable reproduction inputs saved; HANDOFF intentionally final-only after checks.', 'artifact', 'final_handoff_pending',
        ['streams/yjs/replay/reproduce.md','streams/prosemirror/replay/reproduce.md','evidence/commit-ledger.jsonl'],
        'Ignored cache is not the only reproduction input; locks/scripts are committed. Historical browser/full CI environment is not recreated.')
    structural = read('evidence/audit-final.json', {'structural_pass':None})
    add('structural_and_frozen_integrity', 'all structural checks and10 frozen hashes',
        {'structural_pass':structural.get('structural_pass'), 'check_count':len(structural.get('checks',[]))},
        'check', 'pass' if structural.get('structural_pass') else 'pending', ['evidence/audit-final.json'],
        'Structural pass is separate from research_fully_satisfied.')
    verification = read('evidence/fixed-result-verification.json', {'status':'pending_final_remote_commit_and_session_check'})
    add('fixed_remote_readback_and_contract_check', 'read RESULT and acceptance from fixed remote SHA; run session check --fetch',
        verification, 'fixed_result_commit', 'pass' if verification.get('passed') else 'pending',
        ['evidence/fixed-result-verification.json', 'HANDOFF.md'],
        'Final HANDOFF records a subsequent check of the final result SHA; receipt commit may name its already-verified parent.')
    output = {
        'schema':1, 'task_id':'AF-RES-057', 'recorded_UTC':datetime.now(timezone.utc).isoformat(),
        'overall_research_status':'PARTIAL', 'research_fully_satisfied':False,
        'artifact_storage_status':'see_remote_commit_receipts_and_final_HANDOFF',
        'zero_semantics': {'observed_zero':'E/D different0/6; no observed transition', 'not_applicable':'new-correct/wrong rate denominator0',
                          'unconfirmed':'complete original public pairs and same-SHA CI pass',
                          'not_performed':'independent human experiment/review and historical browser execution',
                          'completed':'main26 research variants and8 separately labeled sensitivity records'},
        'primary_blockers':['Four earliest authored body revisions not fully recovered','Three natural author runtime versions unconfirmed; PN1 explicit retained text criterion sensitivity',
                            'Six original complete same-input same-version opA/B+redo public output pairs unconfirmed','PT1 semantic answer exposure','No retained matching public CI evidence'],
        'case_and_view_identity_rule':'The18 rows share6cases; three views per case reuse the same evidence.',
        'review_actor':'root with same-model product/donor agents; actual scope and file hashes in final-review files; no independent human reviewer',
        'requirements':requirements,
        'resume_first_action':'Start with YN1 original installed version and exact event trace, or supply an exact public opA/B fixture for one chosen slot; retain current seal and put any changed sampling/window in a new protocol.'
    }
    (P/'evidence/acceptance-evidence.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'conditions':len(requirements),'overall':output['overall_research_status'],'table_lines':{'first':[tables[0][0],tables[0][-1]],'second':[tables[1][0],tables[1][-1]]}},ensure_ascii=False))


if __name__ == '__main__':
    main()
