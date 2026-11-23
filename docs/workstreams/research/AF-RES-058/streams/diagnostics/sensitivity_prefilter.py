"""Compare observed Bansal pre/postfilter records for Single minus Conf.

Writes only sensitivities-prefilter.json (and ignored inputs with --download).
Never deduplicates ambiguous person/item keys or modifies the main aggregates.
"""
import argparse
import collections
import csv
import datetime as dt
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
PIN = '6cebab4ffd2b332ebec5e27e7632e7bf1c36ba5f'
EXPECTED = {
    'decision-result-prefilter.csv': '1074a05e0a4f113a1f8b8bfe8a887f455ad57dec5a4838fbe5357c85e3e84af6',
    'decision-result-filter.csv': '0cc48875d451e095db8307e7b2cf616d5ad2277e200c8d2579e07db174c1f9f0',
}
TASKS = ('amzbook', 'lsat', 'beer')
CONDITIONS = ('Conf.', 'Conf.+Single')
CORE = ('assignmentId', 'questionId', 'task', 'condition', 'pred', 'y', 'choice')


def sha(content):
    return hashlib.sha256(content).hexdigest()


def sign(value):
    return 'positive' if value > 0 else 'negative' if value < 0 else 'zero'


def aggregate(rows, task, condition, correct):
    group = [r for r in rows if r['task'] == task and r['condition'] == condition]
    xs = [r for r in group if (r['pred'] == r['y']) == correct]
    counts = collections.Counter(tuple(r[k] for k in CORE[:4]) for r in xs)
    ambiguous = {k for k, n in counts.items() if n > 1}
    a = sum(r['choice'] == r['pred'] for r in xs)
    c = sum(r['choice'] == r['y'] for r in xs)
    other = sum(r['choice'] != r['pred'] and r['choice'] != r['y'] for r in xs)
    assert xs and all(r[k] not in ('', None) for r in xs for k in CORE)
    assert (a == c) if correct else (a + c + other == len(xs))
    return {
        'D': len(xs), 'A': a, 'C': c, 'other_wrong_count': other,
        'person_keys_in_condition': len({r['assignmentId'] for r in group}),
        'condition_records': len(group),
        'ambiguous_keys_in_stratum': len(ambiguous),
        'ambiguous_records_in_stratum': sum(counts[k] for k in ambiguous),
        'missing_core_in_selected_records': 0,
        'A_rate': a / len(xs), 'C_rate': c / len(xs),
    }


def load(download):
    records = {}; receipts = []
    for name, expected in EXPECTED.items():
        url = f'https://raw.githubusercontent.com/uw-hai/Complementary-Performance/{PIN}/experiment-data/{name}'
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        if download:
            with urllib.request.urlopen(url, timeout=60) as response:
                content = response.read()
                status = response.status
            path = ROOT / '_cache' / 'sensitivity-inputs' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            method = 'downloaded pinned public author file'
        else:
            path = ROOT / '_cache' / 'bansal-data' / 'experiment-data' / name
            if not path.exists():
                path = ROOT / '_cache' / 'sensitivity-inputs' / name
            content = path.read_bytes()
            method = 'read previously cloned fixed public author file'
            status = None
        assert sha(content) == expected, 'Input content does not match pinned receipt: ' + name
        rows = list(csv.DictReader(io.StringIO(content.decode())))
        assert all(r[k] not in ('', None) for r in rows for k in CORE)
        records[name] = rows
        receipts.append({
            'file': name, 'url': url, 'read_utc': start,
            'sha256': sha(content), 'bytes': len(content), 'rows': len(rows),
            'http_status': status, 'method': method, 'columns': list(rows[0]),
            'missing_core_in_file': 0,
        })
    return records, receipts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    protected = {name: sha((ROOT / name).read_bytes()) for name in ('outcomes.json', 'contrasts.json')}
    published = json.loads((ROOT / 'outcomes.json').read_text())
    rows, receipts = load(args.download)
    contrasts = []
    for task in TASKS:
        for correct in (True, False):
            sets = {}
            for key, filename in (('prefilter', 'decision-result-prefilter.csv'), ('postfilter', 'decision-result-filter.csv')):
                control = aggregate(rows[filename], task, CONDITIONS[0], correct)
                intervention = aggregate(rows[filename], task, CONDITIONS[1], correct)
                da = Fraction(intervention['A'], intervention['D']) - Fraction(control['A'], control['D'])
                dc = Fraction(intervention['C'], intervention['D']) - Fraction(control['C'], control['D'])
                sets[key] = {
                    'control': control, 'intervention': intervention,
                    'delta_A_percentage_points': float(100 * da),
                    'delta_A_exact_fraction': str(da), 'delta_A_direction': sign(da),
                    'delta_C_percentage_points': float(100 * dc),
                    'delta_C_exact_fraction': str(dc), 'delta_C_direction': sign(dc),
                }
                if key == 'postfilter':
                    for condition, counts in zip(CONDITIONS, (control, intervention)):
                        original = next(r for r in published if
                            r['analysis_set'] == 'D01:author-filtered-records' and
                            r['dataset'] == task and r['condition'] == condition and
                            r['advice_correct'] == correct)
                        assert (counts['A'], counts['D'], counts['C']) == (
                            original['accept_count'], original['denominator'], original['correct_count'])
            contrasts.append({
                'study_id': 'D01', 'source_id': 'DI-BAN-DATA', 'task': task,
                'intervention': CONDITIONS[1], 'control': CONDITIONS[0],
                'advice_correct': correct, 'unit': 'observed published final-response record',
                **sets,
                'A_direction_changed_by_filter': sets['prefilter']['delta_A_direction'] != sets['postfilter']['delta_A_direction'],
                'C_direction_changed_by_filter': sets['prefilter']['delta_C_direction'] != sets['postfilter']['delta_C_direction'],
                'postfilter_matches_existing_main_cells': True,
            })
    after = {name: sha((ROOT / name).read_bytes()) for name in protected}
    assert protected == after
    result = {
        'study_id': 'D01', 'analysis': 'Observed prefilter sensitivity: Conf.+Single minus Conf. only',
        'actor': 'diagnostics assistant; Python standard library in provided cloud workspace',
        'command': 'python -B docs/workstreams/research/AF-RES-058/streams/diagnostics/sensitivity_prefilter.py' + (' --download' if args.download else ''),
        'started_utc': started, 'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_id': 'DI-BAN-DATA', 'input_receipts': receipts,
        'scope_notes': [
            'Prefilter and postfilter are separate observed public record sets; excluded postfilter records are not unmeasured counterfactuals.',
            'Public prefilter is not a complete original randomized assignment, recruitment, or screening roster.',
            'All repeated/ambiguous keys retained. No arbitrary deduplication; person-key counts do not repair ambiguous IDs.',
            'Descriptive record-level ratios only. Repeated trials are not independent participants; no causal claim for filtering itself.',
            'No new missing-data bounds, inferential tests, or modification to the main78outcomes/52contrasts.',
            'other_wrong_count is a third wrong answer only within the incorrect-advice stratum.',
        ],
        'contrasts': contrasts, 'contrast_count': len(contrasts),
        'A_direction_change_count': sum(r['A_direction_changed_by_filter'] for r in contrasts),
        'C_direction_change_count': sum(r['C_direction_changed_by_filter'] for r in contrasts),
        'main_files_unchanged': protected == after, 'main_file_sha256_before_and_after': protected,
        'status': 'completed',
    }
    (ROOT / 'sensitivities-prefilter.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({
        'status': 'completed', 'contrasts': len(contrasts),
        'acceptance_direction_changes': result['A_direction_change_count'],
        'main_files_unchanged': result['main_files_unchanged'],
        'summary': [{
            'task': r['task'], 'advice_correct': r['advice_correct'],
            'prefilter_delta_A_pp': r['prefilter']['delta_A_percentage_points'],
            'postfilter_delta_A_pp': r['postfilter']['delta_A_percentage_points'],
            'A_direction_changed': r['A_direction_changed_by_filter'],
        } for r in contrasts],
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
