#!/usr/bin/env python3
"""Preserve phase-specific measured costs and reconcile raw open outcomes."""
import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((BASE / rel).read_text())


rows = list(csv.DictReader((BASE / 'search-log.csv').open()))
outcomes = []
for row in rows:
    if row['event_type'] not in ('open_attempt', 'retry', 'same_original_section_read'):
        continue
    receipt = load(row['receipt_path'])
    status = receipt.get('open_status', receipt.get('status', ''))
    header = json.dumps({'header': receipt.get('result_header'), 'results': receipt.get('results', [])}, ensure_ascii=False)
    failure = bool(receipt.get('is_error') or receipt.get('isError') or receipt.get('failure') or status in ('failed','failure'))
    summary = 'rewritten summary' in header.lower() or status == 'opened_rewritten_summary' or receipt.get('original_body_verified') is False
    outcome = 'access_failure' if failure else 'summary_only' if summary else 'body_returned' if (status == 'opened' or receipt.get('is_error') is False or receipt.get('isError') is False) else 'unknown'
    outcomes.append({'event_id': row['event_id'], 'stream': row['stream'], 'question_id': row['question_id'],
                     'route': row['route'], 'event_type': row['event_type'], 'receipt_id': row['receipt_id'],
                     'receipt_path': row['receipt_path'], 'url': row['url'], 'outcome': outcome,
                     'normalized_failure_reported': row['failure_reported'],
                     'basis': 'raw receipt open_status/error/failure/returned-header/original-body marker; no inference of semantic sufficiency'})
with (BASE / 'evidence/discovery-open-outcomes.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(outcomes[0])); w.writeheader(); w.writerows(outcomes)

by_route = {route: {kind: dict(Counter(r['outcome'] for r in outcomes if r['route'] == route and (kind == 'all' or r['event_type'] == kind)))
                    for kind in ('all','open_attempt','retry','same_original_section_read')} for route in ('G','R')}
phases = {
    'discovery': {'source': 'evidence/discovery-summary.json', 'observations': load('evidence/discovery-summary.json'),
                  'open_outcomes_by_route': by_route, 'open_outcomes_total': dict(Counter(r['outcome'] for r in outcomes)),
                  'failure_field_limitation': 'Normalized failure_reported alone has unknown Cargo fields. Raw-receipt reconciliation above is required; summary_only is distinct from access failure.'},
    'masked_audit_arrow': {'source': 'reviews/arrow-by-cargo/summary.json', 'observations': load('reviews/arrow-by-cargo/summary.json')},
    'masked_audit_cargo': {'source': 'reviews/cargo-by-jupyter/costs.json', 'observations': load('reviews/cargo-by-jupyter/costs.json')},
    'masked_audit_jupyter': {'source': 'reviews/jupyter-by-arrow/README.md §直接再열람과 비용',
                             'observations': {'requests': 19, 'web_open': 18, 'http_get': 1, 'unique_urls_attempted': 13, 'unique_urls_body_read': 12,
                                              'failed_requests': 3, 'sum_measured_request_wall_ms': 17539, 'search_requests': 0}},
    'followup_arrow': {'source': 'followups/arrow/cost-summary.json', 'observations': load('followups/arrow/cost-summary.json')},
    'followup_cargo': {'source': 'followups/cargo/cost-summary.json', 'observations': load('followups/cargo/cost-summary.json')},
    'followup_jupyter': {'source': 'followups/jupyter/costs.json', 'observations': load('followups/jupyter/costs.json')},
    'supplements': {'source': 'supplements/costs.json', 'observations': load('supplements/costs.json')},
}
result = {'phases': phases,
          'sampling_and_input_recovery_cost': 'metadata requests and receipts are retained in streams; no comparable complete wall-time total was instrumented',
          'tokens': 'not exposed', 'billed_cost': 'not exposed', 'human_hours_saved': 'unobserved',
          'sum_is_not_elapsed_time': True,
          'no_grand_total_of_incompatible_units': True,
          'interpretation': 'Do not add API commands, web tool calls, source documents and returned result counts as the same cost unit. Post-seal audits never consume or repair the original discovery budget.'}
(BASE / 'evidence/cost-summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'open_requests': len(outcomes), 'outcomes': result['phases']['discovery']['open_outcomes_total'], 'by_route': by_route}, ensure_ascii=False, indent=2))
