"""Compare primary and clean-profile artifacts while keeping unobserved cells explicit."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECEIPTS = ROOT / 'receipts'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalized(obj):
    # API completion time is expected to differ. Array, selector and node order are preserved.
    return {key: value for key, value in obj.items() if key != 'timestamp'}


def canonical_fingerprint(obj):
    return digest(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))


def compare_axe(primary_path, replay_path):
    primary, replay = load(primary_path), load(replay_path)
    norm_a, norm_b = normalized(primary), normalized(replay)
    first_case = load(primary_path.with_suffix('.case.json'))
    second_case = load(replay_path.with_suffix('.case.json'))
    return {
        'first': primary_path.relative_to(ROOT).as_posix(),
        'second': replay_path.relative_to(ROOT).as_posix(),
        'rawSha256': [digest(p.read_bytes()) for p in (primary_path, replay_path)],
        'rawEqual': primary_path.read_bytes() == replay_path.read_bytes(),
        'rawChangedFields': sorted(k for k in primary.keys() | replay.keys() if primary.get(k) != replay.get(k)),
        'timestamp': [primary['timestamp'], replay['timestamp']],
        'normalizedEqual': norm_a == norm_b,
        'normalizedSha256': [canonical_fingerprint(d) for d in (norm_a, norm_b)],
        'sameInputs': all(
            first_case[k] == second_case[k]
            for k in ('inputSha256', 'axeSha256', 'mode', 'options', 'runtimeAxeVersion', 'domBefore')
        ),
    }


def anchor_controls():
    a = RECEIPTS / 'pages/controls'
    b = RECEIPTS / 'replay/anchor-controls'
    return {
        path.stem: {
            'rawEqual': path.read_bytes() == (b / path.name).read_bytes(),
            'sameDocument': load(path)['artifactSha256'] == load(b / path.name)['artifactSha256'],
            'first': path.relative_to(ROOT).as_posix(),
            'second': (b / path.name).relative_to(ROOT).as_posix(),
        }
        for path in sorted(a.glob('*--*.json'))
    }


def origins():
    policy = load(RECEIPTS / 'replay/network.json')
    return {
        path.stem: {
            'firstObserved': load(path)['observed'],
            'stage': 'origin HTML bytes and Chromium navigation',
            'replayStatus': policy['originReplayStatus'],
            'normalizedEqual': None,
            'firstReceipt': path.relative_to(ROOT).as_posix(),
        }
        for path in sorted((RECEIPTS / 'pages/browser').glob('*--*.json'))
    }


def main():
    replay = RECEIPTS / 'replay'
    before = RECEIPTS / 'runs'
    after = replay / 'axe'
    version = ['chromium', 'node', 'driver', 'parse5', 'contextOptions', 'inputSha256']
    a, b = (load(directory / 'environment.json') for directory in (before, after))
    comparison = {
        'replaySource': (replay / 'source.commit').read_text().strip(),
        'sameEnvironment': {field: a[field] == b[field] for field in version},
        'axe': {
            path.stem: compare_axe(path, after / path.name)
            for path in sorted(before.glob('*--default.json'))
        },
        'anchorControls': anchor_controls(),
        'originAnchors': origins(),
    }
    print(json.dumps(comparison, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
