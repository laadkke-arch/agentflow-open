"""Join post-seal evidence without rewriting any frozen prediction/input file."""
from pathlib import Path
import csv
import importlib.util
import json
from datetime import datetime, timezone

P = Path(__file__).resolve().parent
CASES = ['YN1', 'YN2', 'YT1', 'PN1', 'PN2', 'PT1']
SEAL = '74dc9f887bc47bc0a92b9a75ea327ffa30aca70b'


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def load(name):
    return json.loads((P / name).read_text())


def normalize_and_count_sources():
    # Import only the source-normalization function. Never run pre-seal main().
    spec = importlib.util.spec_from_file_location('preseal_sources', P / 'assemble_preseal.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sources = module.normalize_sources()
    aliases = {
        'yjs-doc-implementation': 'yjs-undo-implementation',
        'P-W-TEST-BASIC-UNDO': 'P-W-HISTORY-TEST-SUITE',
        'P-W-TEST-EXCLUDED-CHANGES': 'P-W-HISTORY-TEST-SUITE',
        'P-W-TEST-MULTILEVEL': 'P-W-HISTORY-TEST-SUITE',
        'P-W-PATCH-892': 'P-W-ISSUE-892',
        'P-W-PATCH-984': 'P-W-ISSUE-984',
        'P-W-PATCH-1311': 'P-W-ISSUE-1311'
    }
    for r in sources:
        r['acquisition_work_id'] = r['work_id']
        if r['work_id'] in aliases:
            r['work_id'] = aliases[r['work_id']]
            r['genealogy_adjustment'] = 'Conservative post-seal counting only; no predictions or selected cases changed. See evidence/final-counts.json.'
        if not r['contrary_source_ids']:
            r['contrary_search_status'] = 'No distinct counter-source assigned to this acquisition; this is not evidence of no contradiction. See question-level searches and falsifiers in SELF_CHECK.md.'
    for stream, case, sid, work, sha, test in [
        ('yjs', 'YT1', 'Y-L-UPSTREAM', 'yjs-test-infinite-capture', '0a09ff854b2ecd942b3c0f0e741253a214cee1bf', 'testInfiniteCaptureTimeout'),
        ('prosemirror', 'PT1', 'P-L-UPSTREAM', 'P-W-HISTORY-TEST-SUITE', '554d6eedb76704d1db62d85768611ce4b611abd2', 'history enables undo')
    ]:
        file = P/'streams'/stream/'upstream-verification/verification.json'
        if not file.exists():
            continue
        v = json.loads(file.read_text())
        upstream_url = 'https://github.com/yjs/yjs/blob/'+sha+'/tests/undo-redo.tests.js#L49-L57' if stream == 'yjs' else 'https://github.com/ProseMirror/prosemirror-history/blob/'+sha+'/test/test-history.ts#L31-L38'
        sources.append({'source_id':sid, 'work_id':work, 'acquisition_work_id':work,
                        'kind_lineage':'researcher execution of original selected upstream test; same test genealogy',
                        'questions_cases':['Q6',case], 'original_url':upstream_url, 'fixed_url':upstream_url,
                        'version_date_hash':{'source_sha':sha, 'execution_receipt':str(file.relative_to(P))},
                        'opened_UTC':v.get('recorded_UTC',v.get('ended_UTC',datetime.now(timezone.utc).isoformat())),
                        'time_precision':'Execution start/end in original receipt; this is a later post-outcome verification.',
                        'location':test, 'findings':v,
                        'limits':'Local original-source runner; not historical author execution, public CI, a new prediction or an original opB/redo output. Test/dependency limitations are in the companion.',
                        'evidence_type':'observed researcher execution', 'contrary_source_ids':['Y-R-YT1-OLD'] if stream=='yjs' else ['P-E150-GROUP'],
                        'access_status':'direct_read_local_receipt', 'external_minimum_eligible':False,
                        'source_group':'self_execution', 'selected_request':False,
                        'reader':'same-model '+stream+' researcher; root reviewed companion',
                        'raw_record_path':str(file.relative_to(P))})
    (P / 'sources.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in sources))
    smap = {r['source_id']: r for r in sources}
    allocation = {
        'request_originals': ['Y-I157', 'Y-I204', 'P-I892', 'P-I1341'],
        'product_API_example_design': ['Y-DOC-ALPHA', 'Y-X789', 'P-API103', 'P-IR120'],
        'distinct_test_or_fix': ['Y-F431', 'Y-F390', 'Y-F392', 'Y-F454', 'P-FIX984', 'P-FIX1311'],
        'map_accounting_direct_cases': ['D04', 'D12', 'D03', 'D14'],
        'original_undo_research': ['D07', 'D08']
    }
    quota = []
    allocated = []
    category_limits = {
        'request_originals': 'Four selected request bodies were read; earliest authored revisions and complete original runtimes were not recovered. Issue/fix/author followups remain one episode.',
        'product_API_example_design': 'Versions of one API are one work; allocation uses README, a separate author drawing example, history API and inputrules API, without splitting implementation files.',
        'distinct_test_or_fix': 'Six distinct correction episodes for disjoint allocation; #892 is a seventh observed episode but already occupies a request slot. A patch need not contain a final-text assertion.',
        'map_accounting_direct_cases': 'Two map and two accounting cases. D14 is an authored failure report without numeric ledger; only three of four cases have numeric/object-state verification.',
        'original_undo_research': 'Two separately authored original research papers; policies and prototypes are not evidence of the two recipient products\' exact runtime behavior.'
    }
    for category, ids in allocation.items():
        works = [smap[i]['work_id'] for i in ids]
        assert all(smap[i]['external_minimum_eligible'] for i in ids)
        assert len(works) == len(set(works))
        allocated += works
        quota.append({'category': category, 'planned': len(ids), 'actual': len(works), 'unit': 'unique_primary_work',
                      'source_ids': ids, 'work_ids': works,
                      'limits': category_limits[category]})
    assert len(allocated) == len(set(allocated)) == 20
    eligible = [r for r in sources if r['external_minimum_eligible']]
    works = sorted({r['work_id'] for r in eligible})
    counts = {
        'generated_UTC': datetime.now(timezone.utc).isoformat(),
        'source_records': len(sources), 'eligible_acquisition_rows': len(eligible),
        'raw_unique_eligible_work_ids': len({r['acquisition_work_id'] for r in eligible}),
        'unique_primary_works': len(works), 'work_ids': works, 'aliases': aliases,
        'rationale': 'Merge same issue/fix/reproduction/CI episode, all revisions of one work, two Yjs implementation files, and undeclared-origin PM test groups. Never use fetch duplicates, search snippets, failures, metadata CI, input-only acquisition, or local executions for the external minimum.',
        'per_stream': {s: len({r['work_id'] for r in eligible if r['raw_record_path'] == 'streams/' + s + '/sources.jsonl'}) for s in ['yjs', 'prosemirror', 'donors']},
        'disjoint_minimum_allocation': quota, 'disjoint_allocation_unique_works': len(set(allocated)),
        'quota_summary': '4/4/6/4/2 (20개 서로 겹치지 않는 보수적 계보 배당); 별도 #892 수정은 요청 계보와 중복하여 추가 배당하지 않음',
        'all_distinct_fix_episodes': ['yjs-test-infinite-capture', 'yjs-issue-390', 'yjs-issue-392', 'yjs-forum-454', 'P-W-ISSUE-892', 'P-W-ISSUE-984', 'P-W-ISSUE-1311'],
        'donor_case_precision': {'direct_cases': 4, 'numeric_or_object_state_verified': 3,
                                 'author_report_without_numeric_ledger': 1, 'map_cases': 2, 'accounting_cases': 2},
        'source_ids_unique': len(smap) == len(sources),
        'reading_actor': 'same-model research team; root reread selected sources and ledgers, not an independent human panel',
        'study_verification_separate': '>=20 sources is not evidence that all six original output pairs have been verified.',
        'later_local_verification_rows': [r['source_id'] for r in sources if r['source_id'] in ['Y-L-UPSTREAM','P-L-UPSTREAM']],
        'independent_source_audit_scope': 'The donor audit counted130 original acquisition rows; two later original-test local executions, if present, are excluded from external works. Eligible112/unique66 is unchanged.'
    }
    (P / 'evidence/final-counts.json').write_text(json.dumps(counts, ensure_ascii=False, indent=2) + '\n')
    return counts


def build_observations():
    predictions = list(csv.DictReader((P / 'predictions.csv').open()))
    yjs = {r['case_id']: r for r in load('streams/yjs/observations.json')['cases']}
    pm = {r['case_id']: r for r in load('streams/prosemirror/observations.json')['cases']}
    source_rows = [json.loads(line) for line in (P / 'sources.jsonl').read_text().splitlines() if line]
    source_map = {r['source_id']: r for r in source_rows}
    outcomes = {}
    statuses = {
        'YN1': 'conditional researcher states match; original version/setup and exact public pair unconfirmed',
        'YN2': 'sealed abstention retained; observed gc=false success is post-seal evidence, not a newly predicted hit',
        'YT1': 'original opA declared expectation matches; opB/redo are researcher extensions; no public CI run obtained',
        'PN1': 'synthetic metadata states match; original collaboration/selection fault is a different comparison and remains unconfirmed',
        'PN2': 'non-abstaining minimal-fixture predictions match; opB redo and several boundary states were abstentions',
        'PT1': 'declared opA and synthetic states match; semantic answer exposure before seal prevents new-hit credit'
    }
    for case in CASES:
        if case.startswith('Y'):
            raw = yjs[case]
            replays = raw['researcher_replay']['results']
            normal_label = 'deletion' if case == 'YN2' else 'normal' if case == 'YN1' else ''
            normal = {}
            boundary = []
            for r in replays:
                label = r['label']
                obs = r['observations']
                if label in [normal_label + '-opA', normal_label + '-opB', 'opA', 'opB']:
                    op = 'A' if label.endswith('opA') else 'B'
                    normal[op] = {'before': obs['before'], 'undo': obs['afterUndo'], 'redo': obs['afterRedo'],
                                  'undo_depth_before': obs.get('undoDepth'), 'after_undo_depths': obs.get('afterUndoDepths')}
                else:
                    boundary.append(r)
            if case == 'YT1':
                boundary = [{'op': 'A' if r['label'] == 'opA' else 'B',
                             'repeated_first_undo': r['observations']['repeatedFirstUndo'],
                             'repeated_second_undo': r['observations']['repeatedSecondUndo']} for r in replays]
            ids = [raw['original_request']['source_id'], raw['researcher_replay']['source_id'], 'Y-CI-PROBES']
            ids += [r['source_id'] for r in [raw.get('public_test', {}), raw.get('author_execution', {})] if 'source_id' in r]
            outcomes[case] = {
                'normal': normal, 'boundary': boundary, 'public_test': raw.get('public_test'),
                'author_run': raw.get('author_execution'),
                'CI': {**raw['public_CI'], 'probe_scope': 'Diagnostic13.6.28 and fix commits7395229/a22b3cd/abf3fab; not direct probes of YN1 alpha or YN2 13.0.8 historical SHA. Exact endpoint list: streams/yjs/ci-probes.json.'},
                'version': raw.get('research_version', raw.get('surrogate_version')),
                'version_match': raw['version_verification'], 'raw_file': 'streams/yjs/observations.json',
                'run_file': raw['researcher_replay']['file'], 'source_ids': ids,
                'run_UTC': raw['researcher_replay']['receipt']['started_UTC'], 'main_variants': len(replays),
                'interpretation': raw['preservation_observation']
            }
        else:
            raw = pm[case]
            replays = raw['researcher_replays']
            normal = {}
            boundary = []
            for r in replays:
                if r['variant'] == 'normal':
                    normal[r['op']] = {'before': r['before'], 'undo': r['undo'], 'redo': r.get('redo')}
                else:
                    boundary.append(r)
            outcomes[case] = {
                'normal': normal, 'boundary': boundary,
                'public_test': raw.get('test_declared', raw.get('public_original')),
                'author_run': raw.get('author_run_status', raw.get('public_original', {}).get('requester_statement', '미확인')),
                'CI': raw['public_CI'], 'version': 'history1.0.3' if case == 'PN1' else 'history1.3.0/inputrules1.2.0' if case == 'PN2' else 'history1.5.0',
                'version_match': raw['replay_version_match'], 'raw_file': 'streams/prosemirror/observations.json',
                'run_file': 'streams/prosemirror/replay/results.json', 'source_ids': raw['source_ids'],
                'run_UTC': 'See streams/prosemirror/replay/run-receipt.json', 'main_variants': len(replays),
                'interpretation': raw['interpretation']
            }
    output = []
    for prediction in predictions:
        case, view = prediction['case_id'], prediction['view']
        o = outcomes[case]
        extra_sid = 'Y-L-UPSTREAM' if case == 'YT1' else 'P-L-UPSTREAM' if case == 'PT1' else None
        ids = o['source_ids'] + ([extra_sid] if extra_sid in source_map else [])
        urls = [source_map[i]['fixed_url'] or source_map[i]['original_url'] for i in ids]
        local_upstream = 'not applicable to this natural case'
        if case in ['YT1','PT1']:
            stream = 'yjs' if case == 'YT1' else 'prosemirror'
            companion = P/'streams'/stream/'upstream-verification/verification.json'
            local_upstream = {'file':str(companion.relative_to(P)), 'summary':json.loads(companion.read_text())} if companion.exists() else 'pending companion'
        output.append({
            'observation_id': case + '-' + view + '-OBS', 'prediction_id': prediction['prediction_id'],
            'case_id': case, 'view': view, 'layer': prediction['layer'], 'seal_commit': SEAL,
            'evidence_units': 'one case shared by three views; do not count repeated source/run rows as independent observations',
            'research_version': o['version'], 'version_match': dump(o['version_match']),
            'sealed_choice': prediction['choice'], 'sealed_normal': prediction['normal_prediction'],
            'sealed_boundary': prediction['boundary_prediction'], 'exposure_status': prediction['exposure_status'],
            'exposure_reference_time': 'Verbatim state at prediction seal, not a statement that assertions remain unopened now.',
            'normal_opA_observed': dump(o['normal']['A']), 'normal_opB_observed': dump(o['normal']['B']),
            'boundary_observed': dump(o['boundary']), 'public_test_declared': dump(o['public_test']),
            'public_CI': dump(o['CI']), 'author_execution_statement': dump(o['author_run']),
            'later_local_upstream_verification': dump(local_upstream),
            'source_ids': ';'.join(ids), 'source_urls': dump(urls),
            'raw_observation_file': o['raw_file'], 'research_run_file': o['run_file'], 'run_UTC': o['run_UTC'],
            'original_same_input_version_opA_opB_redo_public_pair': '미확인',
            'new_D_hit': '해당 없음: E/D same; original complete pairs unconfirmed',
            'comparison': statuses[case], 'interpretation': o['interpretation']
        })
    with (P / 'observations.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    # Machine-readable units and denominators. No abstention is converted into a success.
    pmap = {(r['case_id'], r['view']): r for r in predictions}
    keys = ['choice', 'opA_undo', 'opB_undo', 'opA_redo', 'opB_redo', 'preserved_other_edits', 'normal_prediction', 'boundary_prediction']
    equal = [c for c in CASES if all(pmap[(c, 'E')][k] == pmap[(c, 'D')][k] for k in keys)]
    comparison = {
        'generated_UTC': datetime.now(timezone.utc).isoformat(), 'seal_commit': SEAL,
        'E_D_same': {'numerator': len(equal), 'denominator': 6, 'unit': 'case', 'case_ids': equal, 'fields': keys},
        'E_D_different': {'numerator': 6-len(equal), 'denominator': 6, 'unit': 'case', 'status': 'observed_zero'},
        'conditional_new_correct': {'numerator': None, 'denominator': 0, 'unit': 'different_prediction_case_with_matching_unexposed_output', 'status': 'not_applicable'},
        'conditional_new_wrong': {'numerator': None, 'denominator': 0, 'unit': 'different_prediction_case_with_matching_unexposed_output', 'status': 'not_applicable'},
        'E_abstain_D_correct': {'observed_transitions': 0, 'eligible_conditional_denominator': 0, 'status': 'not_applicable'},
        'E_wrong_D_correct': {'observed_transitions': 0, 'eligible_conditional_denominator': 0, 'status': 'not_applicable'},
        'E_correct_D_wrong': {'observed_transitions': 0, 'eligible_conditional_denominator': 0, 'status': 'not_applicable'},
        'strata': {
            'natural': {'same': 4, 'total': 4, 'complete_public_pairs': 0, 'strict_retained_literal_eligible': 3},
            'diagnostic': {'same': 2, 'total': 2, 'declared_original_opA_read': 2, 'complete_public_pairs': 0,
                           'opA_unexposed_declared_match': 1, 'semantically_preexposed': 1}},
        'original_complete_public_pairs': {'numerator': 0, 'denominator': 6, 'unit': 'case', 'status': 'evidence_unconfirmed_not_accuracy'},
        'original_diagnostic_opA_expectations_read': {'numerator': 2, 'denominator': 2, 'unit': 'diagnostic_case'},
        'original_public_runner_executed': {'numerator': 0, 'unit': 'run', 'status': 'see_later_companions', 'scope':'local run of original public source, not remote public CI'},
        'researcher_main_variants': {'numerator': sum(o['main_variants'] for o in outcomes.values()), 'denominator': 26,
                                    'unit': 'scenario_operation', 'status': 'completed', 'accuracy_claim': False},
        'posthoc_variants': {'numerator': 8, 'unit': 'scenario_version', 'old_version_expected_exception_records': 3,
                            'main_prediction_denominator': False},
        'public_CI': {'matching_retained_run_records': 0, 'pass_status': '미확인',
                      'note': 'Empty endpoint result is not a failed run or proof no run ever happened.'},
        'case_comparisons': [{'case_id': c, 'comparison': statuses[c], 'main_variant_count': outcomes[c]['main_variants']} for c in CASES]
    }
    upstream = {}
    for stream in ['yjs','prosemirror']:
        file = P/'streams'/stream/'upstream-verification/verification.json'
        if file.exists():
            v = json.loads(file.read_text())
            upstream[stream] = {'file':str(file.relative_to(P)), 'status':v['status'],
                                'tests_selected':v['tests_selected'], 'tests_passed':v['tests_passed'],
                                'source_sha':v['source_sha'], 'execution_kind':v['execution_kind'], 'public_CI':False}
    comparison['original_public_runner_executed'] = {
        'numerator':sum(v['tests_passed'] for v in upstream.values()), 'denominator':2, 'unit':'selected_original_test_local_run',
        'status':'completed' if len(upstream)==2 and all(v['status']=='passed' for v in upstream.values()) else 'partial',
        'scope':'Later local execution of original public-source selected tests; no public CI or new prediction credit.',
        'not_in_main26_or_posthoc8':True, 'details':upstream}
    (P / 'evidence/comparison-counts.json').write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + '\n')
    return len(output)


if __name__ == '__main__':
    counts = normalize_and_count_sources()
    print(json.dumps({'observation_rows': build_observations(), 'source_rows': counts['source_records'], 'conservative_works': counts['unique_primary_works']}, ensure_ascii=False))
