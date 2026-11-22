#!/usr/bin/env python3
"""Delete every final source URL except the first, without repairing citations.

This is distinct from retaining the first candidate's multi-URL proof bundle.
It mechanically removes evidence using the already sealed condition readings.
"""
import csv
import datetime
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urldefrag

BASE = Path(__file__).resolve().parents[1]


def jl(p):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def u(url):
    return urldefrag(url or '')[0]


def main():
    slots = [r for r in jl(BASE / 'evidence/scored-slots.jsonl') if r['variant'] == 'strict_three_source_urls']
    reviews = {(r['blind_key'], p['package_key']): p for f in (BASE / 'reviews').glob('*/reviews.jsonl') for r in jl(f) for p in r['package_reviews']}
    grouped = defaultdict(list)
    for r in slots:
        grouped[(r['question_id'], r['route'])].append(r)
    rows = []
    pairs = []
    for (qid, route), rs in sorted(grouped.items()):
        rs.sort(key=lambda r: r['original_rank'])
        first_url = next((u(c['url']) for r in rs for c in r['original_returned_citations'] if c.get('url')), '')
        these = []
        for r in rs:
            kept = [c for c in r['original_returned_citations'] if u(c['url']) == first_url]
            p = reviews.get((r['blind_key'], r['package_key']), {})
            predicates = []
            for pr in p.get('predicate_reviews', []):
                evidence = pr.get('original_evidence', [])
                urls = {u(e['url']) for e in evidence if isinstance(e, dict) and e.get('url')}
                if not urls:
                    urls = {u(x) for x in pr.get('urls', []) if x}
                complete = bool(pr.get('support_in_original_citations')) and bool(urls) and urls <= {first_url}
                predicates.append({'condition_id': pr['condition_id'], 'original_cited_support': pr.get('support_in_original_citations', False),
                                   'required_original_source_urls': sorted(urls), 'retained_support': complete})
            complete = bool(predicates) and all(p['retained_support'] for p in predicates)
            row = {'question_id': qid, 'route': route, 'original_rank': r['original_rank'], 'candidate_id': r['candidate_id'],
                   'first_source_url': first_url, 'retained_citations': kept, 'condition_coverage': predicates,
                   'cited_complete_with_first_url_only': complete,
                   'valid_current_new_target': bool(r['valid_current_new_target'] and complete),
                   'valid_current_known_new_use': bool(r['valid_current_known_new_use'] and complete),
                   'valid_historical_new_target': bool(r['valid_historical_new_target'] and complete),
                   'valid_historical_known_new_use': bool(r['valid_historical_known_new_use'] and complete),
                   'empty_after_link_deletion': not kept, 'original_predicate_judgments_revised': False}
            rows.append(row); these.append(row)
        pairs.append({'question_id': qid, 'route': route, 'question_denominator': 1, 'source_url_denominator': int(bool(first_url)),
                      'current_new_success': any(x['valid_current_new_target'] for x in these),
                      'current_known_use_success': any(x['valid_current_known_new_use'] for x in these),
                      'historical_new_success': any(x['valid_historical_new_target'] for x in these),
                      'historical_known_use_success': any(x['valid_historical_known_new_use'] for x in these)})
    with (BASE / 'evidence/literal-top1-slots.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v for k, v in r.items()})
    result = {'definition': 'Retain only first distinct final source URL in original rank/citation order; all sections already cited on that URL remain. Do not rerank or add proof. This is a post-discovery mechanical sensitivity, distinct from top1 candidate.',
              'route_rows': pairs, 'by_route': {route: {'questions': 12, 'current_new_success': sum(r['current_new_success'] for r in pairs if r['route'] == route),
                                                     'current_known_use_success': sum(r['current_known_use_success'] for r in pairs if r['route'] == route),
                                                     'historical_new_success': sum(r['historical_new_success'] for r in pairs if r['route'] == route),
                                                     'historical_known_use_success': sum(r['historical_known_use_success'] for r in pairs if r['route'] == route)} for route in ('G', 'R')},
              'qualifying_current_known_use_slots': [f'{r["question_id"]}-{r["route"]}-{r["original_rank"]}' for r in rows if r['valid_current_known_new_use']]}
    (BASE / 'evidence/literal-top1-summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'by_route': result['by_route'], 'qualifying_known_slots': result['qualifying_current_known_use_slots']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
