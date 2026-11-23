"""Recount AF-RES-057 ledgers; structural integrity is not research completion."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
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
        check('observations_18_unique_views', len(observed)==18 and {(r['case_id'],r['view']) for r in observed}==expected, len(observed))
        check('observations_preserve_sealed_predictions', all(
            r['sealed_choice']==pred_map[(r['case_id'],r['view'])]['choice'] and
            r['sealed_normal']==pred_map[(r['case_id'],r['view'])]['normal_prediction'] and
            r['sealed_boundary']==pred_map[(r['case_id'],r['view'])]['boundary_prediction'] for r in observed),
            'Choice and normal/boundary JSON remain exact sealed strings; exposure reference time is separately labeled.')
        sources = [json.loads(line) for line in (ROOT / 'sources.jsonl').read_text().splitlines() if line.strip()]
        identifiers = [r['source_id'] for r in sources]
        check('source_ids_unique', len(identifiers) == len(set(identifiers)), len(identifiers))
        source_ids=set(identifiers)
        required=['source_id','work_id','kind_lineage','questions_cases','original_url','fixed_url','version_date_hash','opened_UTC','location','findings','limits','evidence_type','contrary_source_ids','access_status','external_minimum_eligible']
        missing_fields=[{'source_id':r['source_id'],'fields':[k for k in required if k not in r]} for r in sources if any(k not in r for k in required)]
        check('source_schema', not missing_fields, missing_fields)
        referred=set(r['source_id'] for r in cards)
        for r in observed:
            referred.update(r['source_ids'].split(';'))
        for r in sources:
            referred.update(r['contrary_source_ids'])
        check('source_references_resolve', referred <= source_ids, sorted(referred-source_ids))
        eligible = [r for r in sources if r.get('external_minimum_eligible') is True]
        works = sorted({r['work_id'] for r in eligible})
        output['source_counts'] = {'records': len(sources), 'eligible_records': len(eligible), 'unique_primary_works': len(works), 'work_ids': works}
        final_counts=json.loads((ROOT/'evidence/final-counts.json').read_text())
        check('source_counts_recomputed',len(sources)==final_counts['source_records'] and len(eligible)==final_counts['eligible_acquisition_rows'] and works==final_counts['work_ids'],output['source_counts'])
        allocation=[work for group in final_counts['disjoint_minimum_allocation'] for work in group['work_ids']]
        check('twenty_disjoint_role_allocation',len(allocation)==20 and len(set(allocation))==20 and set(allocation)<=set(works),allocation)
        check('actual_card_word_counts',all(len(r['display_window'].split())==int(r['word_count']) for r in cards),
              [{'card_id':r['card_id'],'recorded':int(r['word_count']),'actual':len(r['display_window'].split())} for r in cards])
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
        broken=[]
        for filename in ['RESULT.md','SELF_CHECK.md','return-cards.md']:
            for target in re.findall(r'\]\(([^)]+)\)',(ROOT/filename).read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                local=target.split('#',1)[0]
                if not (ROOT/local).exists():
                    broken.append({'file':filename,'target':target})
        check('report_local_links',not broken,broken)
        local_tests=[]
        for stream in ['yjs','prosemirror']:
            v=json.loads((ROOT/'streams'/stream/'upstream-verification/verification.json').read_text())
            local_tests.append({'stream':stream,'selected':v['tests_selected'],'passed':v['tests_passed'],'status':v['status'],'public_CI':v['public_CI']})
        check('two_original_tests_local_only',all(v['selected']==1 and v['passed']==1 and v['status']=='passed' and v['public_CI'] is False for v in local_tests),local_tests)
    output['checks'] = checks
    output['structural_pass'] = all(r['passed'] for r in checks)
    output['research_fully_satisfied'] = 'See acceptance-evidence.json; never inferred from structural_pass.'
    target = ROOT / 'evidence' / ('audit-' + args.phase + '.json')
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'phase': args.phase, 'structural_pass': output['structural_pass'], 'checks': len(checks), 'failed': [r['name'] for r in checks if not r['passed']], 'output': str(target)}, ensure_ascii=False))
    raise SystemExit(0 if output['structural_pass'] else 1)


if __name__ == '__main__':
    main()
