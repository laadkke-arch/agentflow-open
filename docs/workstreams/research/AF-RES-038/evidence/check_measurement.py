"""Classify author-created boundary fixtures. No participant/time simulation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def classify(row):
    if not row['t0_adopted']:
        if row['t1_observed']:
            return 'initial_work_continuation'
        return 'pre_adoption_abandonment'
    if not row['t1_observed']:
        return 'followup_missing'
    if row['mixed_cost_unseparable']:
        return 'mixed_unseparable'
    if row['changed_decision'] and row['trigger'] == 'new':
        return 'new_requirement_excluded'
    if row['changed_decision'] and row['trigger'] == 'original':
        return 'card_error_repair' if row['card_error'] else 'original_requirement_repair'
    if not row['changed_decision']:
        if row['final_quality'] is None or row['final_quality'] == 'unverified':
            return 'retained_unverified'
        return 'retained_correct' if row['final_quality'] == 'pass' else 'retained_incorrect'
    return 'unverified'


def main():
    src = ROOT / 'measurement-fixtures.jsonl'
    rows = [json.loads(line) for line in src.read_text().splitlines() if line]
    results = []
    for row in rows:
        actual = classify(row)
        assert row['record_kind'] == 'AUTHOR_CREATED_EXAMPLE_NOT_HUMAN'
        assert all(row[key] is None for key in ['active_seconds', 'repair_active_seconds', 'provider_active_seconds', 'first_acceptance_utc'])
        results.append({'fixture_id': row['fixture_id'], 'expected': row['expected_classification'],
                        'actual': actual, 'match': actual == row['expected_classification'],
                        'all_assigned_denominator_included': row['assigned'],
                        'adopter_denominator_included': row['t0_adopted'],
                        'known_final_quality': row['final_quality'],
                        'total_labor': None, 'repair_labor': None,
                        'boundary_note': row['expected_denominator_note']})
    result = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'reader': 'author-written deterministic classifier; not an independent human judgment',
              'input_sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'input_count': len(rows),
              'matching': sum(r['match'] for r in results), 'human_participants': 0,
              'synthetic_human_durations': 0, 'effect_estimates_computed': False, 'results': results,
              'limitation': 'Confirms the written category rules on constructed boundary cases. It does not establish measurement reliability, labor savings, or causal identification in people.'}
    (ROOT / 'measurement-check.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['input_count', 'matching', 'human_participants', 'synthetic_human_durations']}, ensure_ascii=False))
    if not all(r['match'] for r in results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
