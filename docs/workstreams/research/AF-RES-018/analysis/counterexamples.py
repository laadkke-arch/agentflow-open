#!/usr/bin/env python3
"""Exhaustively locate the five requested counterexample families after judging.

Selectors preserve all matches. They do not choose a favorable anecdote or alter
the preregistered metrics; narrative interpretation still requires source review.
"""
import collections, datetime
from common import load, save

def main():
    pairs = collections.defaultdict(dict)
    for row in load('analysis/per_question.json'):
        pairs[row['qid']][row['condition']] = row
    checks = load('analysis/check-observations.json')
    check_by = {(r['qid'], r['condition'], r['check_id']): r for r in checks}
    judged = load('analysis/judge-consistency.json')['pairs']
    over_reject, new_a, cost_only = [], [], []
    for r in checks:
        if r['condition'] != 'P' or not r['positive']:
            continue
        other = check_by[(r['qid'], 'A', r['check_id'])]
        # Retained+uncertain is deliberately separate from an actual exclusion.
        if r['decision'] == 'exclude' or r['primary_label'] == 'INSUFFICIENT':
            over_reject.append({**r, 'A_decision': other['decision'],
                               'A_primary_label': other['primary_label'],
                               'case_kind': 'P exclusion' if r['decision'] == 'exclude' else 'P kept with independently judged insufficient evidence',
                               'source_files': [f'runs/P/{r["qid"]}.json', f'runs/A/{r["qid"]}.json']})
    for q, pair in sorted(pairs.items()):
        a, p = pair['A'], pair['P']
        if a['cohort'] == 'new':
            advantages = []
            for metric, higher in [('grade2_hit', True), ('gold_recall', True),
                                   ('primary_pool_recall', True), ('secondary_pool_recall', True),
                                   ('first_known_related_rank', False)]:
                av, pv = a.get(metric), p.get(metric)
                if av is not None and pv is not None and ((av > pv) if higher else (av < pv)):
                    advantages.append({'metric': metric, 'A': av, 'P': pv})
            if advantages:
                new_a.append({'qid': q, 'advantages': advantages,
                              'source_files': [f'runs/A/{q}.json', f'runs/P/{q}.json']})
        if a['whole_or_part'] == 'whole' and not a['must_present']:
            gains = []
            for metric, higher in [('grade2_hit', True), ('gold_recall', True),
                                   ('primary_pool_recall', True), ('first_known_related_rank', False),
                                   ('claim_error_rate', False)]:
                av, pv = a.get(metric), p.get(metric)
                if av is not None and pv is not None and ((pv > av) if higher else (pv < av)):
                    gains.append(metric)
            costs = []
            for metric in ['queries', 'normalized_document_budget', 'raw_response_words', 'recorded_active_seconds']:
                av, pv = a.get(metric), p.get(metric)
                if av is not None and pv is not None and pv > av:
                    costs.append({'metric': metric, 'A': av, 'P': pv})
            cost_only.append({'qid': q, 'observed_P_gain_metrics': gains,
                              'observed_P_cost_increases': costs,
                              'matches_no_observed_gain_with_cost_increase': not gains and bool(costs),
                              'limits': 'No observed gain is restricted to the listed measured quantities. Per-question sampled claim counts can be tiny; missingness is not equality.',
                              'source_files': [f'runs/A/{q}.json', f'runs/P/{q}.json']})
    families = [
        {'id': 'CE1', 'question': 'Does P exclude an actual external-record positive, or retain it with unresolved evidence?',
         'selector': 'condition=P AND eligible_positive AND (decision=exclude OR primary_label=INSUFFICIENT)',
         'matches': over_reject,
         'limits': 'Grade2 subset identifies adoption; grade1 is an unrebutted recommendation. Actual exclusion and uncertainty must not be merged.'},
        {'id': 'CE2', 'question': 'Does A outperform P in any new question?',
         'selector': 'cohort=new AND A improves any of grade2 hit, known-gold recall, independently judged recall, first known-related rank',
         'matches': new_a,
         'limits': 'These are question-level descriptive counterexamples, not causal estimates or a claim that all metrics favor A.'},
        {'id': 'CE3', 'question': 'Does P add measured cost without measured benefit on whole/no-must questions?',
         'selector': 'whole AND must=false; enumerate every question, P gains and P cost increases',
         'matches': cost_only,
         'limits': 'All eligible questions are retained, including failures to find the requested counterexample. Human review time is unmeasured.'},
        {'id': 'CE4', 'question': 'Do independently judged duplicate candidates receive different labels after normalization?',
         'selector': 'same qid and configured pool entity/check ID across A/P AND relevance or label differs',
         'matches': [r for r in judged if r['relevance_disagrees'] or r['label_disagrees']],
         'limits': 'Observed disagreement is not itself proof of format preference. Inspect differing versions, scope, qualifications, URLs and exact-payload status.'},
        {'id': 'CE5', 'question': 'Do structured techniques fail to improve, or impose costs, in other fields?',
         'selector': 'Pre-execution counterexample searches recorded in evidence/structured/SEARCH_LOG.json and evidence/evaluation/SEARCH_LOG.json',
         'matches': [{'source_id': sid, 'evidence_file': path, 'finding': finding} for sid, path, finding in [
             ('STR14', 'evidence/structured/evidence.md#1', 'Ontario surgery rollout did not show significant mortality or complication improvement.'),
             ('STR03/STR04', 'evidence/structured/evidence.md#1', 'ACH evidence coverage improved without established accuracy benefit; same50-person sample.'),
             ('STR12', 'evidence/structured/evidence.md#2', 'Expert ECG checklist error correction increased while time and output characters increased.'),
             ('EV07', 'evidence/evaluation/evidence.md#3', 'Sentence-level attribution judgments took longer without established quality improvement in the expert comparison.')]],
         'limits': 'Different interventions and outcome units; these studies do not estimate the AF-RES-018 treatment effect.'}
    ]
    save('analysis/counterexamples.json', {'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'families': families, 'selection_policy': 'Exhaustive selectors; retain nonmatches and measurement limits. Narrative examples require manual inspection of linked runs and evidence.'})
    print({f['id']: len(f['matches']) for f in families})

if __name__ == '__main__':
    main()
