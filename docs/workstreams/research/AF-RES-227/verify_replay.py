#!/usr/bin/env python3
"""Compare archived receipts against a separately produced replay directory."""
import argparse
import json
from pathlib import Path
import re

from analyze import reads
from observe import trial_key
from run import HERE, challenge_cases, digest, encode, load_cases, load_jsonl, save_json

PLANNED = {'base': 64, 'controls': 112, 'challenges': 22, 'diagnostic-base': 32,
           'diagnostic-controls': 112, 'public': 5}


def receipt_equality(reference, replay, ignored_matching_keys=('pinned_module',)):
    matching = []
    for row in (reference, replay):
        matching.append({k:v for k,v in (row.get('matching') or {}).items() if k not in ignored_matching_keys})
    return (
        reference['cwd'] != replay['cwd']
        and all(reference[k] == replay[k] for k in
                ('exit_code', 'stdout', 'stderr', 'stdout_sha256', 'stderr_sha256', 'process_error'))
        and matching[0] == matching[1]
    )


def validate_streams(row):
    for stream in ('stdout', 'stderr'):
        if digest(encode(row[stream])) != row[f'{stream}_sha256']:
            raise ValueError(f"{row['argv']}: invalid {stream} hash")


def verify(reference_dir, replay_dir):
    cases = challenge_cases(load_cases())
    summary = {}
    for name, planned in PLANNED.items():
        original_path = reference_dir/f'{name}.jsonl'
        replay_path = replay_dir/f'{name}.jsonl'
        if name == 'public':
            originals, replays = load_jsonl(original_path), load_jsonl(replay_path)
        else:
            originals, replays = reads(original_path, cases), reads(replay_path, cases)
        if len(originals) != planned or len(replays) != planned:
            raise ValueError(f'{name}: expected {planned}, saw {len(originals)}/{len(replays)}')
        problems = []
        for ordinal, (original, replay) in enumerate(zip(originals, replays, strict=True), 1):
            if name == 'public':
                validate_streams(original)
                validate_streams(replay)
                # unittest runtime is an intentionally unstable field. TAP output and all
                # other captured fields must agree.
                normalized = lambda r: re.sub(r'(Ran [0-9]+ tests in )[\d.]+s', r'\g<1><elapsed>', r['stderr'])
                same = (
                    original['suite'] == replay['suite'] and original['exit_code'] == replay['exit_code'] == 0
                    and original['stdout'] == replay['stdout'] and normalized(original) == normalized(replay)
                    and (original['cwd'], original['argv']) != (replay['cwd'], replay['argv'])
                )
            else:
                same = (
                    trial_key(original) == trial_key(replay)
                    and original['input_sha256'] == replay['input_sha256']
                    and original['original_elements_sha256'] == replay['original_elements_sha256']
                    and original['outcome'] == replay['outcome'] != 'run_error'
                    and receipt_equality(original, replay)
                )
            if not same:
                problems.append(ordinal)
        summary[name] = {
            'planned': planned, 'observed': len(replays), 'missing': planned - len(replays),
            'equal': planned - len(problems), 'different_ordinals': problems,
            'replay_receipt_sha256': digest(replay_path.read_bytes()),
        }

    lis_rows = [json.loads((directory/'lis.json').read_bytes()) for directory in (reference_dir,replay_dir)]
    for row in lis_rows:
        validate_streams(row)
    summary['lis'] = {'planned': 1, 'observed': 1, 'missing': 0, 'equal': int(receipt_equality(*lis_rows))}
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, default=HERE/'receipts')
    parser.add_argument('--replay', type=Path, required=True)
    parser.add_argument('--replay-checkout', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    summary = verify(args.reference, args.replay)
    save_json(args.output, {
        'agentflow_replay_checkout': args.replay_checkout,
        'reference_and_replay': str(args.reference) + ' vs ' + str(args.replay),
        'comparison_policy': 'Literal stdout/stderr/exit for each trial; matching module path may differ. '
                             'Public suite comparison abstracts unittest elapsed time only.',
        'summary': summary,
    })
    print(summary)
    return int(any(row['equal'] != row['planned'] for row in summary.values()))


if __name__ == '__main__':
    raise SystemExit(main())
