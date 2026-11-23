"""Recount public categorical responses; publish aggregates, never participant IDs.

Run from any working directory. Input bytes remain in ignored cache/aslett/.
Use --fetch to retrieve the fixed author commit before checking hashes.
No regression, significance test, or ordinal-to-binary conversion is performed.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
COMMIT = '7b4ffee080be622e06f6197bfd095a3e4faebd16'
RAW = f'https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/{COMMIT}/Data/'
INPUTS = {
    'Study_1_df_FM.csv': '437e164cfedba3e54647444e55800749ef8b06a5f0f665e44046b3f16f9da6da',
    'Search_Exp_Misl_False.csv': 'a3029e07b3d4a6fa325cec1b6b16e3987dbb9a01c9deddb81ef941da853c00a8',
    'Study_1_df_T.csv': 'd6c96fbed886374f19c573052ca3a2c4e02828298dc2360b221a7288fb050cb8',
    'Fact_Checker_Data_Master.csv': '32f1728082d4f30d308d981bff318d6af428448b8e417ae302bdfa5611b61ce8',
    'Study_5_df_FM.csv': 'e0d315b70bdae5215a08aea0e6d8b7480b62f852736d94f367f47b565aad9611',
    'Study_5_df_T.csv': '96d67d817c47a121a134f8f224df3e8263eb617466d5eb7d4d316bdad0ad8947',
}
NA = {'', 'NA'}


def read(name, fetch):
    path = BASE / 'cache' / 'aslett' / name
    if fetch:
        from retrieve import retrieve
        result = retrieve('aslett/' + name, RAW + name)
        assert result.get('status') == 200, result
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert INPUTS[name] is None or digest == INPUTS[name], (name, digest)
    try:
        text = data.decode('utf-8-sig')
        encoding = 'utf-8-sig'
    except UnicodeDecodeError:
        text = data.decode('cp1252')
        encoding = 'cp1252'
    rows = list(csv.DictReader(text.splitlines()))
    return rows, {'file': name, 'url': RAW + name, 'sha256': digest,
                  'bytes': len(data), 'records': len(rows), 'encoding': encoding}


def key(row):
    return row['ResponseId'], row['Article_day']


def complete(row, cols):
    return all(row[col] not in NA for col in cols)


def normalize(value):
    return {'T': 'T', 'True': 'T', 'FM': 'FM', 'Misl/False': 'FM',
            'CND': 'CND', 'NA': 'NA', '': 'NA'}[value]


def describe(rows, study, truth, sample, group, response='Evaluation'):
    treatment_col = 'Treat_Search' if study == 1 else 'Treatment'
    arm = [r for r in rows if r[treatment_col] == group]
    if response == 'Evaluation':
        counts = Counter(normalize(r[response]) for r in arm)
        observed = sum(counts[c] for c in ('T', 'FM', 'CND'))
        accepted = counts['T']
        correct = counts[truth]
        cnd, not_accepted = counts['CND'], counts['FM'] + counts['CND']
        unobserved = counts['NA']
    else:
        # The released author binary is categorical endorsement, not a threshold
        # of Four_Ordinal. It does not separate FM from CND when True_Dummy=0.
        counts = Counter(r[response] for r in arm)
        observed = counts['0'] + counts['1']
        accepted, not_accepted = counts['1'], counts['0']
        correct = accepted if truth == 'T' else None
        cnd, unobserved = None, sum(counts[v] for v in NA)
    return {
        'cohort': f'ASLETT2024-STUDY{study}', 'truth_key': truth,
        'sample': sample, 'assigned_condition': 'search_encouragement' if group == '1' else 'control',
        'assigned_people_N': None, 'assigned_truth_stratum_trials_N': None,
        'file_or_filter_trials_N': len(arm), 'observed_categorical_trials_N': observed,
        'acceptance_n': accepted, 'acceptance_N': observed,
        'final_correct_n': correct, 'final_correct_N': observed if correct is not None else None,
        'CND_n': cnd, 'not_accepted_n': not_accepted,
        'file_response_NA_n': unobserved,
        'assigned_missing_m': None, 'acceptance_bounds_assigned': None,
        'people_in_file_or_filter': len({r['ResponseId'] for r in arm}),
        'items_in_file_or_filter': len({r['Article_day'] for r in arm}),
        'interpretation': ('Original-condition descriptive comparison among observed outcomes. '
            'File NA is not assigned attrition: three of five daily items were presented; '
            'unrecorded entrants and attention exclusions are absent. No ITT N or missing bound.'
            if study == 1 else 'Author analysis file; categorical True_Dummy observed. '
            'Released binary 0 combines non-true judgments; false-claim accuracy and CND unknown.'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fetch', action='store_true')
    args = ap.parse_args()
    data, inputs = {}, []
    for name in INPUTS:
        data[name], receipt = read(name, args.fetch)
        inputs.append(receipt)
    fm = data['Study_1_df_FM.csv']
    rawfm = data['Search_Exp_Misl_False.csv']
    true = data['Study_1_df_T.csv']
    assert len({key(r) for r in fm}) == len(fm) == 3966
    assert len({key(r) for r in rawfm}) == len(rawfm) == 3966
    assert len({key(r) for r in true}) == len(true) == 10783
    rawbykey = {key(r): r for r in rawfm}
    assert {key(r) for r in fm} == set(rawbykey)
    for row in fm:
        raw = rawbykey[key(row)]
        assert row['Susc_FN'] == raw['Susc_FN'] == raw['True_Dummy']
        assert row['Treat_Search'] == raw['Treat_Search']
        choice = normalize(raw['Evaluation'])
        assert row['Susc_FN'] == ('NA' if choice == 'NA' else str(int(choice == 'T')))
    for row in true:
        choice = normalize(row['Evaluation'])
        assert row['True_Dummy'] == ('NA' if choice == 'NA' else str(int(choice == 'T')))
    fact = {r['Article_day']: r for r in data['Fact_Checker_Data_Master.csv']}
    truth_audit = []
    for rows, truth in ((rawfm, 'FM'), (true, 'T')):
        for item in sorted({r['Article_day'] for r in rows}):
            assert item in fact
            fr = fact[item]
            votes = Counter(normalize(fr[f'Pariticipant_{n}_Eval']) for n in range(1, 7))
            votes.pop('NA', None)
            modal = [k for k, v in votes.items() if v == max(votes.values())]
            assert modal == [truth], (item, truth, votes)
            truth_audit.append({'Article_day': item, 'author_key': truth,
                'professional_coder_votes': dict(votes),
                'independent_truth_verified': False,
                'original_claim_url': fr['link'],
                'source_row_record': list(fact).index(item) + 1})
    output = []
    fm_complete = [rawbykey[key(r)] for r in fm if complete(r, list(r))]
    fm_selected = ['Susc_FN', 'Treat_Search', 'Age', 'Dummy_Congruence',
                   'Education_Score', 'Gender', 'Income_Score', 'Article_day', 'ResponseId']
    assert {key(r) for r in fm_complete} == {key(r) for r in fm if complete(r, fm_selected)}
    true_selected = ['True_Dummy'] + fm_selected[1:]
    true_complete = [r for r in true if r['Article'] in {'1', '2', '3', '4', '5'}
                     and complete(r, true_selected)]
    for rows, truth, sample in [
        (rawfm, 'FM', 'all_observed_categorical_response'),
        (true, 'T', 'all_observed_categorical_response'),
        (fm_complete, 'FM', 'author_complete_case'),
        (true_complete, 'T', 'author_complete_case')]:
        for group in ('0', '1'):
            output.append(describe(rows, 1, truth, sample, group))
    study5_duplicate_audit = []
    for filename, truth in [('Study_5_df_FM.csv', 'FM'), ('Study_5_df_T.csv', 'T')]:
        keys = Counter(key(r) for r in data[filename])
        study5_duplicate_audit.append({'file': filename, 'rows': len(data[filename]),
            'unique_person_item_keys': len(keys),
            'repeated_person_item_keys': sum(v > 1 for v in keys.values()),
            'excess_rows_beyond_key': sum(v - 1 for v in keys.values()),
            'decision': 'retain author rows; repeated key is not silently called another unique trial'})
        for group in ('0', '1'):
            output.append(describe(data[filename], 5, truth, 'released_author_analysis_file',
                                   group, 'True_Dummy'))
    contrasts = []
    for i in range(0, len(output), 2):
        c, t = output[i:i + 2]
        a = 100 * (t['acceptance_n'] / t['acceptance_N'] - c['acceptance_n'] / c['acceptance_N'])
        f = None if c['final_correct_n'] is None else 100 * (
            t['final_correct_n'] / t['final_correct_N'] - c['final_correct_n'] / c['final_correct_N'])
        contrasts.append({'cohort': c['cohort'], 'truth_key': c['truth_key'], 'sample': c['sample'],
            'contrast': 'search_encouragement_minus_control', 'acceptance_difference_pp': a,
            'final_accuracy_difference_pp': f, 'inference': 'descriptive only; no independent-trial significance test'})
    result = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'author_commit': COMMIT,
              'inputs': inputs, 'join_audit': {'key': ['ResponseId', 'Article_day'],
              'FM_one_to_one_rows': 3966, 'FM_derived_binary_disagreements': 0,
              'true_derived_binary_disagreements': 0, 'author_truth_items_matched': len(truth_audit),
              'author_truth_modal_disagreements': 0,
              'study5_duplicate_audit': study5_duplicate_audit},
              'groups': output, 'contrasts': contrasts,
              'truth_items': truth_audit,
              'checks': {'FM_complete_case_control_N': len([r for r in fm_complete if r['Treat_Search'] == '0']),
                         'FM_complete_case_search_N': len([r for r in fm_complete if r['Treat_Search'] == '1'])}}
    assert result['checks'] == {'FM_complete_case_control_N': 1145, 'FM_complete_case_search_N': 1130}
    (BASE / 'aslett-aggregates.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (BASE / 'aslett-counts.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(output[0])); w.writeheader(); w.writerows(output)
    print(json.dumps({'groups': output, 'contrasts': contrasts, 'join_audit': result['join_audit']}, indent=2))


if __name__ == '__main__':
    main()
