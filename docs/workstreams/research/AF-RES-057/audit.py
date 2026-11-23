"""Recount AF-RES-057 ledgers; structural integrity is not research completion."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CASES = ['YN1', 'YN2', 'YT1', 'PN1', 'PN2', 'PT1']
VIEWS = ['A', 'E', 'D']


def rows(name):
    with (ROOT / name).open(newline='') as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', choices=['sealed', 'final'], default='final')
    args = parser.parse_args()
    checks = []
    def check(name, condition, detail):
        checks.append({'name': name, 'passed': bool(condition), 'detail': detail})

    expected = {(case, view) for case in CASES for view in VIEWS}
    predictions = rows('predictions.csv')
    cards = rows('cards.csv')
    for name, data in [('predictions', predictions), ('cards', cards)]:
        keys = [(r['case_id'], r['view']) for r in data]
        check(name + '_18_unique_slots', len(keys) == 18 and set(keys) == expected, keys)
    card_map = {(r['case_id'], r['view']): r for r in cards}
    budgets = []
    for case in CASES:
        e, d = card_map[(case, 'E')], card_map[(case, 'D')]
        match = int(e['word_count']) == int(d['word_count']) <= 160 and int(e['figure_count']) == int(d['figure_count'])
        budgets.append({'case_id': case, 'E_words': int(e['word_count']), 'D_words': int(d['word_count']), 'match': match})
        check(case + '_budget', match, budgets[-1])
    frame = rows('frame.csv')
    natural = [r for r in frame if r['layer'] == 'natural' and r.get('issue_number')]
    selected = [r for r in frame if r['status'] == 'selected']
    check('six_selected_cases', {r['case_id'] for r in selected} == set(CASES), [r['case_id'] for r in selected])
    events = rows('events.csv')
    check('events_cover_cases', {r['case_id'] for r in events} == set(CASES), len(events))
    same_fields = ['choice', 'opA_undo', 'opB_undo', 'opA_redo', 'opB_redo', 'preserved_other_edits', 'normal_prediction', 'boundary_prediction']
    pred_map = {(r['case_id'], r['view']): r for r in predictions}
    same = [case for case in CASES if all(pred_map[(case, 'E')][k] == pred_map[(case, 'D')][k] for k in same_fields)]
    output = {'generated_UTC': datetime.now(timezone.utc).isoformat(), 'phase': args.phase,
              'units': {'cases': 6, 'natural_cases': 4, 'diagnostic_cases': 2, 'view_rows': 18,
                        'natural_bodies_read': len(natural), 'frame_rows': len(frame), 'event_rows': len(events)},
              'budgets': budgets, 'identical_E_D': {'numerator': len(same), 'denominator': 6, 'case_ids': same},
              'different_E_D': {'numerator': 6-len(same), 'denominator': 6},
              'conditional_denominator_note': 'Differences alone are not confirmed hits; exact unexposed outcomes are also required.'}
    if args.phase == 'final':
        observed = rows('observations.csv')
        check('observation_case_coverage', {r['case_id'] for r in observed} == set(CASES), len(observed))
        sources = [json.loads(line) for line in (ROOT / 'sources.jsonl').read_text().splitlines() if line.strip()]
        identifiers = [r['source_id'] for r in sources]
        check('source_ids_unique', len(identifiers) == len(set(identifiers)), len(identifiers))
        eligible = [r for r in sources if r.get('external_minimum_eligible') is True]
        works = sorted({r['work_id'] for r in eligible})
        output['source_counts'] = {'records': len(sources), 'eligible_records': len(eligible), 'unique_primary_works': len(works), 'work_ids': works}
        frozen = json.loads((ROOT / 'evidence' / 'prediction-freeze.json').read_text())
        for path, digest in frozen['file_sha256'].items():
            actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            check('sealed_unchanged:' + path, actual == digest, actual)
        text = (ROOT / 'RESULT.md').read_text()
        tables, current = [], []
        for line in text.splitlines():
            if line.startswith('|'):
                current.append(line)
            elif current:
                tables.append(current)
                current = []
        if current:
            tables.append(current)
        check('first_table_18_rows', len(tables) >= 2 and len(tables[0]) == 20, len(tables[0]) if tables else 0)
        check('second_table_6_rows', len(tables) >= 2 and len(tables[1]) == 8, len(tables[1]) if len(tables) >= 2 else 0)
        check('last_weakness_table_3_rows', bool(tables) and len(tables[-1]) == 5 and '불일치·약점' in tables[-1][0], len(tables[-1]) if tables else 0)
        self_check = (ROOT / 'SELF_CHECK.md').read_text()
        for q in range(1, 8):
            check('Q' + str(q) + '_result_and_selfcheck', 'Q' + str(q) in text and 'Q' + str(q) in self_check, 'presence only, semantic review separate')
    output['checks'] = checks
    output['structural_pass'] = all(r['passed'] for r in checks)
    output['research_fully_satisfied'] = 'See acceptance-evidence.json; never inferred from structural_pass.'
    target = ROOT / 'evidence' / ('audit-' + args.phase + '.json')
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'phase': args.phase, 'structural_pass': output['structural_pass'], 'checks': len(checks), 'failed': [r['name'] for r in checks if not r['passed']], 'output': str(target)}, ensure_ascii=False))
    raise SystemExit(0 if output['structural_pass'] else 1)


if __name__ == '__main__':
    main()
