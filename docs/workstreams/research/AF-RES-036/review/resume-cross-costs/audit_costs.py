"""Read-only audit of the resumed checkpoint; writes only adjacent audit evidence."""
import collections
import csv
import hashlib
import io
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
REPO = next(p for p in OUT.parents if (p / '.git').exists())
OWNED = 'docs/workstreams/research/AF-RES-036/'
TARGET = 'f403243dbf5f097536a1fd9fda55dfce4382329a'
inputs = {}


def raw(name):
    data = subprocess.check_output(['git', 'show', f'{TARGET}:{OWNED}{name}'], cwd=REPO)
    inputs[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    return data


def jsonl(name):
    return [json.loads(x) for x in raw(name).decode().splitlines() if x.strip()]


def js(name):
    return json.loads(raw(name))


def csvrows(name):
    return list(csv.DictReader(io.StringIO(raw(name).decode())))


def units(attempts):
    a = [r for r in attempts if r.get('operation') == 'GET']
    return {
        'actual_GET_operations': len(a),
        'minimum_http_exchanges': sum(1 + len(r.get('redirect_chain', [])) for r in a),
        'received_final_body_bytes': sum(r.get('received_body_bytes') or 0 for r in a),
        'temporary_stored_bytes': sum(r.get('stored_bytes') or 0 for r in a),
        'elapsed_request_sum_seconds': round(sum(r.get('elapsed_seconds') or 0 for r in a), 6),
        'http_or_transport_failure_responses': sum(bool(r.get('error')) or (r.get('status') or 0) >= 400 for r in a),
        'empty_2xx_bodies': sum(200 <= (r.get('status') or 0) < 300 and not r.get('received_body_bytes') for r in a),
    }


attempts = jsonl('attempts.jsonl')
adjudication_attempts = jsonl('adjudicators/gnu/attempts.jsonl') + jsonl('adjudicators/bioc/attempts.jsonl')
costs = csvrows('costs.csv')
replay = csvrows('replay-costs.csv')
summaries = js('evidence/replay-summary.json')
retention_raw = raw('retention-options.jsonl')
retention_summary = js('evidence/retention-summary.json')
retention = [json.loads(x) for x in retention_raw.splitlines()]
first = units(attempts)
post = units(adjudication_attempts)
checks = []


def check(label, actual, expected):
    checks.append({'check': label, 'actual': actual, 'expected': expected, 'met': actual == expected})


check('all collection GET ids in costs exactly once', sorted(r['attempt_id'] for r in attempts if r.get('operation') == 'GET'), sorted(r['cost_id'] for r in costs if r['actual_requests'] == '1'))
check('actual byte cost sum', sum(int(r['received_body_bytes']) for r in costs if r['actual_requests'] == '1'), first['received_final_body_bytes'])
check('simulation excluded from actual cost rows', sum(r['actual_requests'] == '0' and r['round'] == '2' for r in costs), 48)
check('second visit simulation cells', len(replay), 48)
check('second visit actual requests', sum(int(r['actual_requests']) for r in replay), 0)
check('unique replay cells', len({(r['ref_ids'], r['task'], r['configuration']) for r in replay}), 48)

retention_sizes = collections.Counter()
for line in retention_raw.splitlines(keepends=True):
    retention_sizes[json.loads(line)['configuration']] += len(line)
check('serialized retention bytes recomputed', dict(retention_sizes), retention_summary['configuration_bytes'])
check('physical retention file bytes', len(retention_raw), retention_summary['physical_serialized_file_bytes'])
check('three configurations for each ref', sorted(collections.Counter(r['ref_id'] for r in retention).values()), [3] * 12)

all_gets = {r['attempt_id']: r for r in attempts if r.get('operation') == 'GET'}
recomputed = []
for summary in summaries:
    rs = [r for r in replay if r['task'] == summary['task'] and r['configuration'] == summary['configuration']]
    ids = set(a for r in rs for a in r['unit_attempt_ids'].split('|'))
    physical = units([all_gets[k] for k in sorted(ids)])
    logical = {
        'cases': len(rs),
        'logical_operations': sum(int(r['modeled_request_operations']) for r in rs),
        'logical_http_exchanges': sum(int(r['modeled_http_exchanges']) for r in rs),
        'logical_body_bytes': sum(int(r['modeled_body_bytes']) for r in rs),
        'operation_count_feasible_cases': sum(r['operation_count_within_budget'] == 'True' for r in rs),
        'strict_exchange_count_feasible_cases': sum(r['strict_exchange_count_within_budget'] == 'True' for r in rs),
        'concrete_serialized_example_bytes': sum(int(r['durable_stored_bytes']) for r in rs),
        'local_H_reads': sum(int(r['local_H_reads']) for r in rs),
    }
    for k, v in logical.items():
        check(f"{summary['task']}/{summary['configuration']}/{k}", v, summary[k])
    expected_physical = summary['shared_source_physical_lower_bound']
    for our, their in [('actual_GET_operations', 'operations'), ('minimum_http_exchanges', 'http_exchanges'), ('received_final_body_bytes', 'body_bytes'), ('elapsed_request_sum_seconds', 'first_visit_elapsed_proxy')]:
        check(f"{summary['task']}/{summary['configuration']}/physical/{their}", physical[our], expected_physical[their])
    recomputed.append({'task': summary['task'], 'configuration': summary['configuration'], **logical, 'physical_if_shared_and_unchanged': physical})

receipt = {
    'target_commit': TARGET,
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'audit_kind': 'separate internal context; original decisions and read-only checkpoint inspected; not blind reader experiment',
    'inputs': inputs,
    'collection_phase': first,
    'post_seal_adjudication_phase': post,
    'collection_and_adjudication_phases': units(attempts + adjudication_attempts),
    'recomputed_simulation': recomputed,
    'storage_examples': dict(retention_sizes),
    'storage_increment_C2_over_presealed_B': retention_sizes['C2_BH_with_provenance'] - retention_sizes['C1_B_presealed'],
    'storage_increment_C2_over_lean_context_link': retention_sizes['C2_BH_with_provenance'] - retention_sizes['C1_context_link_only'],
    'scope_correction_required': 'The checkpoint top-level 157 GET ledger omits 59 post-seal adjudication GETs. Preserve 157 as collection-only baseline and add criterion phase; do not call it whole-study total.',
    'not_measured': ['second visit responses and time', 'human or model reading labor and cost', 'wire bytes', 'C0 initial discovery', 'rediscovery in lean C1', 'live service retention cost', 'archive survival and future accessibility'],
    'checks': checks,
    'all_checks_passed': all(r['met'] for r in checks),
}
(OUT / 'cost-audit.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: receipt[k] for k in ['target_commit', 'collection_phase', 'post_seal_adjudication_phase', 'collection_and_adjudication_phases', 'storage_examples', 'all_checks_passed']}, ensure_ascii=False, indent=2))
raise SystemExit(0 if receipt['all_checks_passed'] else 1)
