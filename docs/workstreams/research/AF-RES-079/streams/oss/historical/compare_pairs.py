"""Join explicit before/after API mappings on the recorded identical inputs.

Values, serialized shape/dtype, exceptions, and warnings are separate measures.
No missing historical output is replaced with a current-version output.
"""
import csv
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
versions = ['1.4.1', '1.5.0', '1.5.4', '1.6.0']

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def bare_values(value):
    if isinstance(value, dict):
        if 'dtype' in value and 'value' in value:
            return bare_values(value['value'])
        if 'dtype' in value and 'values' in value:
            return bare_values(value['values'])
        return {k: bare_values(v) for k, v in value.items()}
    if isinstance(value, list):
        return [bare_values(x) for x in value]
    return value

by_version = {}
receipts = {}
for version in versions:
    path = root / ('scipy-' + version + '.jsonl')
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    receipt = json.loads(path.with_suffix('.receipt.json').read_text())
    assert len(rows) == receipt['rows'] == 50
    assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt['result_sha256']
    assert all(r['environment']['scipy'] == version for r in rows)
    assert all(r['environment']['numpy'] == '1.19.5' and r['environment']['python'] == '3.8.20' for r in rows)
    by_version[version] = {(r['event_id'], r['case'], r['api']): r for r in rows}
    receipts[version] = receipt
assert len({r['script_sha256'] for r in receipts.values()}) == 1
assert next(iter(receipts.values()))['script_sha256'] == hashlib.sha256((root.parent / 'probe.py').read_bytes()).hexdigest()

pairs = []

def pair(event, question, case, old_api, new_api, old_version='1.5.4', new_version='1.6.0',
         new_case=None, semantic_input=None, mapping=None):
    old = by_version[old_version][event, case, old_api]
    new = by_version[new_version][event, new_case or case, new_api]
    exact_input = canonical(old['input']) == canonical(new['input'])
    assert exact_input or semantic_input is not None, 'Unexplained input mismatch'
    old_value, new_value = old.get('output'), new.get('output')
    both_returned = old['outcome'] == new['outcome'] == 'returned'
    both_raised = old['outcome'] == new['outcome'] == 'exception'
    exception_type_equal = both_raised and old['exception']['type'] == new['exception']['type']
    representation_equal = both_returned and canonical(old_value) == canonical(new_value)
    values_equal = both_returned and canonical(bare_values(old_value)) == canonical(bare_values(new_value))
    if both_raised:
        state = 'SAME_EXCEPTION_TYPE' if exception_type_equal else 'DIFFERENT_EXCEPTION_TYPE'
    elif old['outcome'] != new['outcome']:
        state = 'RETURN_EXCEPTION_CHANGE'
    elif representation_equal:
        state = 'SAME_VALUE_SHAPE_DTYPE_REPRESENTATION'
    elif values_equal:
        state = 'SAME_NUMERIC_VALUES_DIFFERENT_SCALAR_OR_ARRAY_REPRESENTATION'
    else:
        state = 'DIFFERENT_VALUES_OR_OUTPUT_SHAPE'
    pair_id = event + '-' + question + '-' + case + ('-adapter' if new_case else '')
    row = {'pair_id': pair_id, 'event_id': event, 'question': question, 'case': case,
           'old_version': old_version, 'new_version': new_version, 'old_api': old_api, 'new_api': new_api,
           'old_row_id': old['observation_id'], 'new_row_id': new['observation_id'],
           'old_file': 'scipy-' + old_version + '.jsonl', 'new_file': 'scipy-' + new_version + '.jsonl',
           'old_input': old['input'], 'new_input': new['input'],
           'old_input_sha256': digest(old['input']), 'new_input_sha256': digest(new['input']),
           'exact_recorded_input_equal': exact_input,
           'semantic_input': semantic_input if semantic_input is not None else old['input'],
           'semantic_input_sha256': digest(semantic_input if semantic_input is not None else old['input']),
           'input_mapping': mapping or 'identical recorded input; only API identity changes for P2',
           'old_outcome': old['outcome'], 'new_outcome': new['outcome'],
           'old_output': old_value, 'new_output': new_value,
           'old_exception': old.get('exception'), 'new_exception': new.get('exception'),
           'numeric_values_equal': values_equal if both_returned else None,
           'output_shape_dtype_representation_equal': representation_equal if both_returned else None,
           'exception_type_equal': exception_type_equal if both_raised else None,
           'exception_message_equal': old['exception']['message'] == new['exception']['message'] if both_raised else None,
           'old_warnings': old.get('warnings'), 'new_warnings': new.get('warnings'),
           'warning_types_equal': ([w['type'] for w in old['warnings']] == [w['type'] for w in new['warnings']]) if 'warnings' in old and 'warnings' in new else None,
           'comparison': state, 'native_pair_observed': True,
           'environment': {'python': '3.8.20', 'numpy': '1.19.5', 'same_host': True},
           'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'limits': 'Only the exact recorded inputs are covered. Exceptions may suppress warning capture in the unchanged probe; null warnings are not evidence of no warning.'}
    pairs.append(row)

for case in ['normal', 'provider_axis', 'empty_2d', 'float32', 'invalid_axis', 'nan_raise']:
    pair('O01', 'P1', case, 'median_absolute_deviation', 'median_absolute_deviation', '1.4.1', '1.5.0')
    pair('O01', 'P2', case, 'median_absolute_deviation', 'median_abs_deviation', '1.4.1', '1.5.0')
pair('O01', 'P2', 'normal', 'median_absolute_deviation', 'median_abs_deviation', '1.4.1', '1.5.0',
     new_case='preserve_old_scale', semantic_input={'data': [1.0, 3.0, 2.0]},
     mapping='same numeric data; new scale explicitly set to1/1.4826 to preserve the old default')
for case in ['normal', 'reverse', 'empty', 'singleton', 'float32', 'complex', 'axis', 'invalid_axis', 'mismatched_x']:
    pair('O02', 'P1', case, 'trapz', 'trapz')
    pair('O02', 'P2', case, 'trapz', 'trapezoid')
pair('O02', 'P1', 'distribution_alias', 'stats.trapz', 'stats.trapz')
pair('O02', 'P2', 'distribution_alias', 'stats.trapz', 'stats.trapezoid')
for case, radius in [('normal', 1.1), ('exact_boundary', 1.0)]:
    pair('O03', 'P1', case, 'KDTree.query', 'KDTree.query')
    pair('O03', 'P2', case, 'KDTree.query', 'KDTree.query_ball_point',
         semantic_input={'points': [[0.0], [1.0], [2.0]], 'query': [0.0], 'radius': radius},
         mapping='same points/query/radius; old k=None,distance_upper_bound=r maps to new query_ball_point(r)')
pair('O03', 'P1', 'complex_query', 'query', 'query')
pair('O03', 'P2', 'complex_query', 'query', 'query_ball_point')
for case in ['provider', 'float32', 'complex', 'wrong_shape', 'empty']:
    pair('O04', 'P1', case, 'sum', 'sum')
    pair('O04', 'P2', case, 'sum', 'sum_labels')

(root / 'paired-observations.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n' for row in pairs))
fields = ['pair_id', 'event_id', 'question', 'case', 'old_version', 'new_version', 'old_api', 'new_api',
          'old_input_sha256', 'new_input_sha256', 'exact_recorded_input_equal', 'semantic_input_sha256',
          'comparison', 'numeric_values_equal', 'output_shape_dtype_representation_equal',
          'exception_type_equal', 'exception_message_equal', 'warning_types_equal']
with (root / 'paired-summary.csv').open('w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows({key: row[key] for key in fields} for row in pairs)
aggregate = {}
for event in ['O01', 'O02', 'O03', 'O04']:
    event_rows = [p for p in pairs if p['event_id'] == event]
    aggregate[event] = {'paired_comparisons': len(event_rows),
                        'by_question': {q: len([p for p in event_rows if p['question'] == q]) for q in ['P1', 'P2']},
                        'comparison_counts': {state: sum(p['comparison'] == state for p in event_rows)
                                              for state in sorted({p['comparison'] for p in event_rows})}}
summary = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'native_release_runs': 4, 'native_observations': 200, 'event_pairs_observed': 4,
           'paired_comparisons': len(pairs), 'exact_input_payload_pairs': sum(p['exact_recorded_input_equal'] for p in pairs),
           'explicit_parameter_mapping_pairs': sum(not p['exact_recorded_input_equal'] for p in pairs),
           'aggregate': aggregate, 'same_probe_sha256': next(iter(receipts.values()))['script_sha256'],
           'exit_code': 0, 'runner': 'oss_evidence agent via local tools.exec_command',
           'command': 'python -B docs/workstreams/research/AF-RES-079/streams/oss/historical/compare_pairs.py',
           'cwd': str(Path.cwd()),
           'limits': ['Sampled input behavior, not universal equivalence',
                      'simps and cumtrapz were in the same recruitment event but are not separately executed by this probe',
                      'Warnings preceding an exception are not preserved by the original probe; do not compare missing warning fields as no-warning evidence',
                      'The old stable files intentionally remain unchanged; this supplement supersedes their unexecuted-pair status only for these inputs']}
(root / 'paired-check.receipt.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False))
