#!/usr/bin/env python3
"""Recount frozen returns, package-specific masked readings and later history.

The original candidate order/citations are immutable. Audit opens or historical
records can change interpretation, never the original returned citation set.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag

BASE = Path(__file__).resolve().parents[1]


def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def csvout(path, rows):
    if not rows:
        raise ValueError(f'No rows for {path}')
    fields = list(rows[0])
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in rows:
            w.writerow({k: json.dumps(r.get(k), ensure_ascii=False, sort_keys=True) if isinstance(r.get(k), (list, dict)) else r.get(k, '') for k in fields})


def loc(entry):
    return (urldefrag(entry.get('url') or '')[0], entry.get('section', ''))


def flatten_required(bundle):
    if isinstance(bundle, list):
        return bundle
    if isinstance(bundle, dict):
        return [e for v in bundle.values() for e in (v if isinstance(v, list) else [v]) if isinstance(e, dict)]
    return []


def bundle_location_coverage(row, field):
    needed = flatten_required(row.get('required_bundle', []))
    supplied = {loc(x) for x in row.get(field, []) if isinstance(x, dict)}
    return bool(needed) and all(x.get('url') and loc(x) in supplied and not x.get('missing') for x in needed)


def status(value):
    if value in ('supported', 'support'):
        return 'support'
    if value in ('conflict', 'contradicted', 'incompatible'):
        return 'conflict'
    return 'hold'


def main():
    qs = {r['id']: r for r in jl(BASE / 'questions.jsonl')}
    mapping = jl(BASE / 'evidence/blind-mapping.jsonl')
    m = {(r['question_id'], r['route'], r['rank'], r['return_budget_variant']): r
         for r in mapping if r['record_type'] == 'returned'}
    reviews = {}
    package = {}
    for path in sorted((BASE / 'reviews').glob('*/reviews.jsonl')):
        for r in jl(path):
            if r['blind_key'] in reviews:
                raise ValueError('Duplicate blind review: ' + r['blind_key'])
            reviews[r['blind_key']] = r
            for p in r['package_reviews']:
                package[(r['blind_key'], p['package_key'])] = p
    packets = {r['blind_key']: r for r in jl(BASE / 'blind/packets.jsonl')}
    if set(reviews) != set(packets):
        raise ValueError(f'Review keys differ: missing={sorted(set(packets)-set(reviews))}, extra={sorted(set(reviews)-set(packets))}')
    history = {}
    decisions = {}
    for path in sorted((BASE / 'followups').glob('*/candidate-history.jsonl')):
        for r in jl(path):
            history[(r['question_id'], r['candidate_id'])] = r
    for path in sorted((BASE / 'followups').glob('*/decisions.jsonl')):
        for r in jl(path):
            decisions[r['question_id']] = r
    exposure = json.loads((BASE / 'evidence/exposure-summary.json').read_text())
    blind_leak = set(json.loads((BASE / 'evidence/blinding-amendment.json').read_text())['leaked_keys'])
    source_map = json.loads((BASE / 'evidence/blind-source-map.json').read_text())
    reverse_source = defaultdict(list)
    for original, masked in source_map.items():
        reverse_source[masked].append(original)

    judgments = []
    for key, review in sorted(reviews.items()):
        qid = review['question_id']
        conditions = {c['id']: c for c in qs[qid]['mandatory_predicates']}
        for p in review['package_reviews']:
            if {r['condition_id'] for r in p['predicate_reviews']} != set(conditions):
                raise ValueError(f'Predicate coverage differs: {key}/{p["package_key"]}')
            for pr in p['predicate_reviews']:
                sid = pr.get('source_ids', [])
                judgments.append({
                    'judgment_id': f'{key}/{p["package_key"]}/{pr["condition_id"]}',
                    'blind_key': key, 'package_key': p['package_key'], 'question_id': qid,
                    'scope': qs[qid]['scope'], 'target_name': review.get('target_name', packets[key]['target_name']),
                    'proposed_use': review.get('proposed_boundary', packets[key]['proposed_uses']),
                    'condition_id': pr['condition_id'], 'mandatory_predicate': conditions[pr['condition_id']]['predicate'],
                    'predicate_subject': conditions[pr['condition_id']].get('subject', 'the actor at the proposed use boundary'),
                    'predicate_time': 'current discovery observation; historical availability separately checked',
                    'provider_status': status(pr.get('status')),
                    'provider_evidence_source_ids': sorted({original for s in sid for original in reverse_source.get(s, [s])}),
                    'provider_evidence_urls': pr.get('urls', []), 'provider_evidence_sections': pr.get('sections', []),
                    'original_opened_support': bool(pr.get('support_in_original_opened', False)),
                    'original_cited_support': bool(pr.get('support_in_original_citations', False)),
                    'reason': pr.get('reason', ''), 'counterexample': p.get('counterexample', review.get('notes', {})),
                    'reviewer': review['reviewer'], 'review_basis': pr.get('assessment_basis', 'see reviewer record'),
                    'fresh_audit_source_ids': pr.get('fresh_audit_source_ids', []),
                    'questioner_followup_choice': decisions.get(qid, {'status': '미확인', 'reason': 'followup record not yet added'}),
                    'researcher_inference': review.get('proposed_boundary', packets[key]['proposed_uses']),
                    'novelty_category_cross_reader': review.get('novelty_category', 'unknown'),
                    'route_word_exposure_before_remask': key in blind_leak,
                })
    csvout(BASE / 'judgments.csv', judgments)

    slots = []
    for variant, filename in [('raw_three_candidates', 'returns-raw.jsonl'), ('strict_three_source_urls', 'returns.jsonl')]:
        for r in jl(BASE / filename):
            qid, route, rank = r['question_id'], r['route'], r['rank']
            cid = r.get('candidate_id')
            mapped = m.get((qid, route, rank, variant)) if cid else None
            review = reviews[mapped['blind_key']] if mapped else {}
            p = package[(mapped['blind_key'], mapped['package_key'])] if mapped else {}
            prs = p.get('predicate_reviews', [])
            opened = bool(prs) and all(x.get('support_in_original_opened', False) for x in prs)
            cited = bool(prs) and all(x.get('support_in_original_citations', False) for x in prs)
            semantic_support = bool(prs) and all(status(x.get('status')) == 'support' for x in prs)
            provider = 'empty' if not cid else ('support' if semantic_support and opened else 'conflict' if any(status(x.get('status')) == 'conflict' for x in prs) else 'hold')
            h = history.get((qid, cid), {})
            hist = h.get('historical_availability', 'unknown')
            new_target = bool(cid and r.get('new_target'))
            known_use = bool(cid and r.get('new_use_in_known_target'))
            current_valid = new_target and provider == 'support' and opened and cited
            known_valid = known_use and not new_target and provider == 'support' and opened and cited
            slots.append({
                'slot_id': f'{qid}-{route}-{rank}', 'variant': variant, 'question_id': qid, 'scope': qs[qid]['scope'],
                'stream': qs[qid].get('stream', ''), 'route': route, 'original_rank': rank,
                'candidate_id': cid or '', 'raw_candidate_id': r.get('original_candidate_id', cid) or '',
                'duplicate_group': f'{qid}/{cid}' if cid else '', 'target_name': r.get('target_name', '') if cid else 'empty',
                'candidate_class': r.get('candidate_class', 'empty'), 'proposed_use': r.get('proposed_use', '') if cid else '',
                'canonical_target': r.get('canonical_target', r.get('target_name', '')) if cid else '',
                'behavior': r.get('behavior', r.get('proposed_use', '')) if cid else '',
                'use_boundary': r.get('use_boundary', r.get('proposed_use', '')) if cid else '',
                'new_target': new_target, 'new_use_in_known_target': known_use,
                'initial_named_target': bool(cid and r.get('initial_named_target')),
                'source_ids': r.get('source_ids', []) if cid else [], 'current_version': r.get('current_version', 'unknown'),
                'provider_status_self': r.get('provider_status', 'unknown') if cid else 'empty',
                'opened_complete_self': bool(cid and r.get('opened_complete')), 'cited_complete_self': bool(cid and r.get('cited_complete')),
                'provider_status_cross_reader': provider, 'opened_complete': opened, 'cited_complete': cited,
                'package_opened_complete_reported': p.get('opened_complete', False),
                'package_cited_complete_reported': p.get('cited_complete', False),
                'valid_current_new_target': current_valid, 'valid_current_known_new_use': known_valid,
                'historical_availability': hist, 'historical_evidence': h,
                'valid_historical_new_target': current_valid and hist == 'supported',
                'valid_historical_known_new_use': known_valid and hist == 'supported',
                'blind_key': mapped['blind_key'] if mapped else '', 'package_key': mapped['package_key'] if mapped else '',
                'original_returned_citations': r.get('returned_citations', []) if cid else [],
                'original_opened_evidence': r.get('opened_evidence', []) if cid else [],
                'declared_bundle_locations_opened': bool(cid and bundle_location_coverage(r, 'opened_evidence')),
                'declared_bundle_locations_cited': bool(cid and bundle_location_coverage(r, 'returned_citations')),
                'source_location_coverage_is_not_semantic_sufficiency': True,
                'missing_conditions': p.get('missing_conditions', []), 'counterexample': p.get('counterexample', ''),
                'empty_reason': r.get('empty_reason', '') if not cid else '',
                'primary_focal_exposure': qid in exposure['primary_excluded_questions'],
                'strict_metadata_exposure': qid in exposure['metadata_excluded_questions'],
                'route_word_leak': bool(mapped and mapped['blind_key'] in blind_leak),
            })
    # The required candidates.csv keeps the original 72 slots. Strict formatting
    # is a separate 72-row view, never a replacement or rank compaction.
    csvout(BASE / 'candidates.csv', [r for r in slots if r['variant'] == 'raw_three_candidates'])
    csvout(BASE / 'candidates-strict.csv', [r for r in slots if r['variant'] == 'strict_three_source_urls'])
    (BASE / 'evidence/scored-slots.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n' for r in slots))

    pairs = []
    for variant in ('raw_three_candidates', 'strict_three_source_urls'):
        for qid in sorted(qs):
            qrows = [r for r in slots if r['variant'] == variant and r['question_id'] == qid]
            by_route = {route: [r for r in qrows if r['route'] == route] for route in ('G', 'R')}
            sets = {route: {r['candidate_id'] for r in rs if r['candidate_id']} for route, rs in by_route.items()}
            row = {'pair_id': f'{qid}/{variant}', 'variant': variant, 'question_id': qid, 'scope': qs[qid]['scope'], 'question_denominator': 1, 'slot_denominator_G': 3, 'slot_denominator_R': 3}
            for route, rs in by_route.items():
                for temporal, label in [('current', 'current'), ('historical', 'historical')]:
                    field = f'valid_{temporal}_new_target'
                    row[f'{route}_{label}_valid_slots'] = sum(r[field] for r in rs)
                    row[f'{route}_{label}_top3_success'] = any(r[field] for r in rs)
                    row[f'{route}_{label}_top1_success'] = any(r[field] for r in rs if r['original_rank'] == 1)
                    row[f'{route}_{label}_known_new_use_slots'] = sum(r[f'valid_{temporal}_known_new_use'] for r in rs)
                for label in ('empty', 'hold', 'conflict'):
                    row[f'{route}_{label}_slots'] = sum(r['provider_status_cross_reader'] == label for r in rs)
            for k in (1, 3):
                g, r = row[f'G_current_top{k}_success'], row[f'R_current_top{k}_success']
                row[f'top{k}_outcome'] = 'R_win' if r and not g else 'G_win' if g and not r else 'tie_both_success' if g and r else 'tie_no_verified_success'
            row['all_returned_common_candidate_ids'] = sorted(sets['G'] & sets['R'])
            row['all_returned_G_exclusive_candidate_ids'] = sorted(sets['G'] - sets['R'])
            row['all_returned_R_exclusive_candidate_ids'] = sorted(sets['R'] - sets['G'])
            row['primary_focal_exposure'] = qid in exposure['primary_excluded_questions']
            row['strict_metadata_exposure'] = qid in exposure['metadata_excluded_questions']
            row['route_word_leak_question'] = any(r['route_word_leak'] for r in qrows)
            pairs.append(row)
    csvout(BASE / 'pairs.csv', pairs)

    metrics = []
    for variant in ('raw_three_candidates', 'strict_three_source_urls'):
        for group, keep in [('all', set(qs)), ('whole', {q for q in qs if qs[q]['scope'] == 'whole'}), ('part', {q for q in qs if qs[q]['scope'] == 'part'}), ('exclude_focal_exposure', set(exposure['primary_retained_questions'])), ('exclude_metadata_and_focal', set(exposure['strict_retained_questions'])), ('exclude_mask_leak_questions', {q for q in qs if not any(r['question_id'] == q and r['route_word_leak'] for r in slots)})]:
            for top in (1, 3):
                for route in ('G', 'R'):
                    rs = [r for r in slots if r['variant'] == variant and r['question_id'] in keep and r['route'] == route and r['original_rank'] <= top]
                    ids = {r['question_id'] for r in rs if r['valid_current_new_target']}
                    metrics.append({'variant': variant, 'group': group, 'route': route, 'top_k': top,
                                    'question_denominator': len(keep), 'slot_denominator': len(rs),
                                    'current_success_questions': len(ids), 'current_valid_slots': sum(r['valid_current_new_target'] for r in rs),
                                    'historical_success_questions': len({r['question_id'] for r in rs if r['valid_historical_new_target']}),
                                    'historical_valid_slots': sum(r['valid_historical_new_target'] for r in rs),
                                    'known_new_use_current_slots': sum(r['valid_current_known_new_use'] for r in rs),
                                    'known_new_use_historical_slots': sum(r['valid_historical_known_new_use'] for r in rs),
                                    'hold_slots': sum(r['provider_status_cross_reader'] == 'hold' for r in rs),
                                    'conflict_slots': sum(r['provider_status_cross_reader'] == 'conflict' for r in rs),
                                    'empty_slots': sum(not r['candidate_id'] for r in rs),
                                    'opened_complete_without_complete_citations': sum(r['opened_complete'] and not r['cited_complete'] for r in rs),
                                    'historical_unknown_nonempty_slots': sum(bool(r['candidate_id']) and r['historical_availability'] == 'unknown' for r in rs)})
    csvout(BASE / 'evidence/metrics.csv', metrics)
    summary = {'questions': len(qs), 'raw_slots': 72, 'strict_slots': 72, 'blind_keys': len(reviews), 'citation_packages': len(package),
               'condition_judgments': len(judgments), 'pairs': len(pairs), 'metrics_rows': len(metrics),
               'by_variant': {variant: {'provider_status': dict(Counter(r['provider_status_cross_reader'] for r in slots if r['variant'] == variant)),
                                         'self_status': dict(Counter(r['provider_status_self'] for r in slots if r['variant'] == variant)),
                                         'current_new_valid_slots': sum(r['valid_current_new_target'] for r in slots if r['variant'] == variant),
                                         'current_known_use_valid_slots': sum(r['valid_current_known_new_use'] for r in slots if r['variant'] == variant),
                                         'outcomes': dict(Counter(r['top3_outcome'] for r in pairs if r['variant'] == variant))}
                              for variant in ('raw_three_candidates', 'strict_three_source_urls')},
               'history_records': len(history), 'followup_decision_events': len(decisions),
               'unknown_is_not_absence': True, 'same_model_cross_reader_is_not_human_validation': True}
    dump(BASE / 'evidence/recount-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
