#!/usr/bin/env python3
"""Describe cross-condition duplicate judgments; do not infer causal format bias."""
import collections, itertools, json
from common import ROOT, load, save

def main():
    key = load('judging/key.json')['rows']
    mapping = {r['row_id']: r for r in load('analysis/candidate-mapping.json')}
    normalized = {}
    for path in sorted((ROOT/'judging/normalized').glob('*.json')):
        normalized.update({r['row_id']: r for r in json.loads(path.read_text())['rows']})
    judgments = collections.defaultdict(dict)
    for path in sorted((ROOT/'judging/blind-raw').glob('*.json')):
        value = json.loads(path.read_text())
        for row in value['rows']:
            assert row['row_id'] not in judgments[value['judge_id']]
            judgments[value['judge_id']][row['row_id']] = row
    groups = collections.defaultdict(lambda: collections.defaultdict(list))
    for rid, k in key.items():
        entity = mapping[rid]['pool_entity'] if k['kind'] == 'discovery' else k['check_id']
        groups[(k['qid'], k['kind'], entity)][k['condition']].append(rid)
    rows, summary = [], []
    for judge, verdicts in judgments.items():
        for (qid, kind, entity), conditions in groups.items():
            for a, p in itertools.product(conditions['A'], conditions['P']):
                if a not in verdicts or p not in verdicts:
                    continue
                left, right = normalized[a], normalized[p]
                ja, jp = verdicts[a], verdicts[p]
                exact = all(left.get(f) == right.get(f) for f in ['name', 'url', 'reason'])
                rows.append({'judge': judge, 'qid': qid, 'kind': kind, 'entity': entity,
                             'A_row_id': a, 'P_row_id': p,
                             'identical_name_url_reason': exact,
                             'A_reason_words': len(left['reason'].split()),
                             'P_reason_words': len(right['reason'].split()),
                             'A_normalized': left, 'P_normalized': right,
                             'A_relevance': str(ja['relevance']), 'P_relevance': str(jp['relevance']),
                             'A_label': ja['label'], 'P_label': jp['label'],
                             'relevance_disagrees': str(ja['relevance']) != str(jp['relevance']),
                             'label_disagrees': ja['label'] != jp['label'],
                             'A_must_violations': ja['must_violations'], 'P_must_violations': jp['must_violations'],
                             'A_judge_reason': ja['reason'], 'P_judge_reason': jp['reason']})
        selected = [r for r in rows if r['judge'] == judge]
        exact_rows = [r for r in selected if r['identical_name_url_reason']]
        all_judged = list(verdicts.values())
        for kind in ['discovery', 'check']:
            subset = [r for r in all_judged if key[r['row_id']]['kind'] == kind]
            counts = collections.Counter(r['label'] for r in subset)
            summary.append({'judge': judge, 'kind': kind, 'judged_rows': len(subset),
                            'label_counts': dict(counts),
                            'largest_label_share': max(counts.values())/len(subset) if subset else None,
                            'note': 'Check rows include frozen unrelated and strict-near-miss probes, so concentration has a separate discrimination check.'})
        summary.append({'judge': judge, 'cross_condition_duplicate_pairs': len(selected),
                        'relevance_disagreements': sum(r['relevance_disagrees'] for r in selected),
                        'label_disagreements': sum(r['label_disagrees'] for r in selected),
                        'identical_payload_pairs': len(exact_rows),
                        'identical_payload_relevance_disagreements': sum(r['relevance_disagrees'] for r in exact_rows),
                        'identical_payload_label_disagreements': sum(r['label_disagrees'] for r in exact_rows)})
    save('analysis/judge-consistency.json', {'summary': summary, 'pairs': rows,
         'limits': 'Different reasons, qualifications, URLs or declared application scopes can legitimately change a judgment. Even identical-payload disagreement is observed inconsistency, not identification of an A/P format effect; presentation order was not counterfactually rerun. Multiple matches form descriptive pairs, not independent observations.'})
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    main()
