#!/usr/bin/env python3
"""Replay AF-RES-227 from pinned source checkouts. See REPLAY.md."""
from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
GIT_PIN = ('v2.43.0', 'c089584ac8dedc3aa7c2c404839bc098050298a2', '564d0252ca632e0264ed670534a51d18a689ef5d')
BREEZY_PIN = ('v0.2.13', '3039783fde723950d36eeafa28b970a63ed59b7c', '834fad2d280fa0634d00d658c61c15d82031f519')
GIT_METHODS = ('patience', 'histogram', 'myers')
BREEZY = 'breezy-python'
METHODS = (*GIT_METHODS, BREEZY)
HEADER = re.compile(r'^@@ -([0-9]+)(?:,([0-9]+))? \+([0-9]+)(?:,([0-9]+))? @@(?: .*)?\n$')
ENCODING = 'utf-8'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')


def encode(value):
    return value.encode(ENCODING, errors='surrogateescape')


def decode(value):
    return value.decode(ENCODING, errors='surrogateescape')


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + '\n', encoding=ENCODING)


def save_jsonl(path, rows):
    with path.open('x', encoding=ENCODING, newline='\n') as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=True, separators=(',', ':')) + '\n')


def load_jsonl(path):
    with path.open(encoding=ENCODING) as file:
        return [json.loads(line) for line in file]


def clean_environment(directory):
    return {
        'PATH': os.defpath, 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC',
        'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
        'GIT_ATTR_NOSYSTEM': '1', 'GIT_CONFIG_COUNT': '0',
        'GIT_CEILING_DIRECTORIES': str(directory.parent),
        'HOME': str(directory / 'empty-home'), 'XDG_CONFIG_HOME': str(directory / 'empty-xdg'),
        'PYTHONHASHSEED': '0', 'PYTHONUTF8': '1', 'PYTHONDONTWRITEBYTECODE': '1',
    }


def capture(argv, directory, env, timeout=60):
    argv = [str(value) for value in argv]
    start = now()
    failure = None
    try:
        result = subprocess.run(argv, cwd=directory, env=env, capture_output=True, timeout=timeout)
        status, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as error:
        status, stdout, stderr = None, error.stdout or b'', error.stderr or b''
        failure = f'timeout after {timeout} seconds'
    except OSError as error:
        status, stdout, stderr = None, b'', b''
        failure = str(error)
    return {
        'started_utc': start, 'finished_utc': now(), 'cwd': str(directory),
        'argv': argv, 'environment': env, 'timeout_seconds': timeout, 'exit_code': status,
        'process_error': failure, 'stdout': decode(stdout), 'stderr': decode(stderr),
        'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr),
    }


@dataclass(frozen=True)
class Trial:
    case: str
    method: str
    context: int = 3
    indent: bool | None = True
    direction: str = 'forward'
    repeat: int = 1
    extra: tuple[str, ...] = ()


def make_side(lines):
    lf = [line + '\n' for line in lines]
    return {
        'original_elements': lines, 'original_elements_sha256': digest(encode(compact(lines))),
        'lf_elements': lf, 'lf_sha256': digest(encode(''.join(lf))),
    }


def load_cases():
    document = json.loads((HERE / 'inputs.json').read_bytes())
    cases = {}
    for case in document['cases']:
        for side in ('a', 'b'):
            expected = make_side(case[side]['original_elements'])
            for key, value in expected.items():
                if case[side][key] != value:
                    raise ValueError(f"input hash/projection mismatch for {case['case_id']}/{side}/{key}")
        cases[case['case_id']] = case
    return cases


def worker(argv):
    """Child process for exact Breezy API calls or stdlib comparison."""
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('case')
    parser.add_argument('method')
    parser.add_argument('context', type=int)
    parser.add_argument('--trace', action='store_true')
    args = parser.parse_args(argv)
    sys.path.insert(0, str(args.source))
    import difflib
    import patiencediff
    from patiencediff import _patiencediff_py as backend

    matcher_path = Path(backend.__file__).resolve()
    if patiencediff.__version__ != (0, 2, 13) or not matcher_path.is_relative_to(args.source):
        raise RuntimeError(f'wrong Breezy module: {matcher_path}')
    a, b = [decode(Path(name).read_bytes()).splitlines(keepends=True) for name in ('a', 'b')]
    original = json.loads(Path('original.json').read_bytes()) if args.case == 'R4' else [a, b]
    is_patience = args.method == BREEZY
    cls = backend.PatienceSequenceMatcher_py if is_patience else difflib.SequenceMatcher
    if args.trace:
        from trace_python import instrument
        sys.settrace(instrument(backend))

    try:
        blocks = cls(None, *original).get_matching_blocks()
        lf_blocks = cls(None, a, b).get_matching_blocks()
        if args.method == 'python-difflib':
            output = difflib.unified_diff(a, b, fromfile='a', tofile='b', n=args.context)
        elif args.method == 'breezy-default':
            output = patiencediff.unified_diff(a, b, fromfile='a', tofile='b', n=args.context)
        else:
            output = patiencediff.unified_diff(a, b, fromfile='a', tofile='b', n=args.context,
                                               sequencematcher=cls)
        sys.stdout.buffer.write(encode(''.join(output)))
    finally:
        sys.settrace(None)

    evidence = {
        'backend': f'{cls.__module__}.{cls.__name__}', 'pinned_module': str(matcher_path),
        'pinned_module_sha256': digest(matcher_path.read_bytes()),
        'blocks_original_0based': blocks, 'blocks_lf_0based': lf_blocks,
        'stdlib_difflib_sha256': digest(Path(difflib.__file__).read_bytes()),
    }
    if is_patience and args.case == 'R4':
        matches = []
        backend.recurse_matches_py(*original, 0, 0, len(a), len(b), matches, 10)
        evidence['r4_original_recurse_pairs_0based'] = matches
    save_json(Path('matching.json'), evidence)


def git_diff(binary, trial):
    algorithm = trial.method if trial.method in (*GIT_METHODS, 'minimal') else 'patience'
    args = [
        binary, '--no-pager', 'diff', '--no-index', '--no-ext-diff', '--no-textconv', '--no-color',
        f'--diff-algorithm={algorithm}', f'-U{trial.context}',
        '--indent-heuristic' if trial.indent else '--no-indent-heuristic',
    ]
    if trial.case == 'R1':
        args.append('--ignore-space-at-eol')
    return [*args, *trial.extra, '--', 'a', 'b']


def is_python_method(method):
    return method in (BREEZY, 'breezy-default', 'python-difflib')


def collect(args, cases, trials, label, *, trace=False):
    for ordinal, trial in enumerate(trials, start=1):
        case = cases[trial.case]
        a, b = (case['b'], case['a']) if trial.direction == 'reverse' else (case['a'], case['b'])
        with tempfile.TemporaryDirectory(prefix=f'{label}-{ordinal:03}-', dir=args.scratch) as temp:
            directory = Path(temp)
            for name, side in [('a', a), ('b', b)]:
                path = directory / name
                content = encode(''.join(side['lf_elements']))
                path.write_bytes(content)
                path.chmod(0o644)
                if digest(path.read_bytes()) != side['lf_sha256']:
                    raise RuntimeError(f'{trial.case}: file fingerprint mismatch')
            save_json(directory / 'original.json', [a['original_elements'], b['original_elements']])
            if is_python_method(trial.method):
                cmd = [sys.executable, '-B', '-S', HERE / 'run.py', '_worker', args.breezy_source,
                       trial.case, trial.method, trial.context]
                if trace and trial.method == BREEZY:
                    cmd.append('--trace')
            else:
                cmd = git_diff(args.git_source / 'git', trial)

            evidence = capture(cmd, directory, clean_environment(directory))
            status, stdout = evidence['exit_code'], evidence['stdout']
            matching = directory / 'matching.json'
            if is_python_method(trial.method):
                outcome = 'different' if stdout else 'same'
                if status != 0 or not matching.is_file():
                    outcome = 'run_error'
            else:
                outcome = {0: 'same', 1: 'different'}.get(status, 'run_error')
            yield {
                **asdict(trial), 'phase': label, 'ordinal': ordinal,
                'id': f'{label}/{ordinal:03}/{trial.case}/{trial.method}',
                'input_sha256': {'a': a['lf_sha256'], 'b': b['lf_sha256']},
                'original_elements_sha256': {'a': a['original_elements_sha256'], 'b': b['original_elements_sha256']},
                **evidence, 'outcome': outcome,
                'matching': json.loads(matching.read_bytes()) if matching.is_file() else None,
            }


def basic_trials(cases, repeats=2):
    for repeat in range(1, repeats + 1):
        for case in cases:
            for method in METHODS:
                yield Trial(case, method, indent=None if method == BREEZY else True, repeat=repeat)


def control_trials():
    for case in ('C1', 'C2', 'C3', 'C4'):
        for method in METHODS:
            for direction in ('forward', 'reverse'):
                for context in (0, 3):
                    for indent in ((None,) if method == BREEZY else (False, True)):
                        yield Trial(case, method, context, indent, direction)


def challenge_cases(cases):
    extras = [
        ('W1', ['a', 'b ', 'c'], ['a', 'b', 'c']),
        ('CE3', list('abcdefghijklmnop'), list('abcdefxydefghijklmnop')),
        ('CE4', ['A', '1', 'B'], ['X', '1', 'Y']),
        ('CE6', ['A', 'B', 'C'], ['B', 'C', 'A']),
        ('CE7', ['A', 'x', 'x', 'x'], ['x', 'x', 'x', 'A']),
    ]
    return {**cases, **{case: {'a': make_side(a), 'b': make_side(b)} for case, a, b in extras}}


def challenge_trials():
    for method in GIT_METHODS:
        yield Trial('W1', method)
        yield Trial('W1', method, extra=('--ignore-space-at-eol',))
    yield Trial('W1', BREEZY, indent=None)
    for case in ('C1', 'C2'):
        yield Trial(case, 'python-difflib', indent=None)
    for method in ('breezy-default', BREEZY, 'python-difflib'):
        yield Trial('CE3', method, indent=None)
    yield Trial('CE4', 'myers', 0, False)
    yield Trial('CE4', 'myers', 0, False, extra=('--inter-hunk-context=1',))
    yield Trial('CE6', 'patience', 0, False)
    yield Trial('CE6', 'anchored', 0, False, extra=('--anchored=A',))
    yield Trial('CE7', 'patience', 0, False)
    yield Trial('CE7', 'minimal', 0, False)
    for method in METHODS:
        yield Trial('R1', method, 0, None if method == BREEZY else False)


def source_identity(source, pin, env, allow_patch=False):
    tag, tagged_object, commit = pin
    cmd = ['/usr/bin/git', '-C', source, 'rev-parse', 'HEAD', f'refs/tags/{tag}']
    receipt = capture(cmd, source, env)
    if receipt['exit_code'] != 0 or receipt['stdout'].splitlines() != [commit, tagged_object]:
        raise RuntimeError(f'Unpinned checkout: {source} [{receipt["stdout"]} {receipt["stderr"]}]')
    status = capture(['/usr/bin/git', '-C', source, 'status', '--porcelain', '--untracked-files=no'], source, env)
    if status['exit_code'] != 0 or (status['stdout'] and not allow_patch):
        raise RuntimeError(f'Unexpected tracked changes: {source} [{status["stdout"]} {status["stderr"]}]')
    return {'tag': tag, 'tag_object': tagged_object, 'commit': commit,
            'identity_receipt': receipt, 'tracked_status_receipt': status}


def environment(args):
    directory = args.scratch
    env = clean_environment(directory)
    git = source_identity(args.git_source, GIT_PIN, env, allow_patch=args.phase == 'diagnostic')
    breezy = source_identity(args.breezy_source, BREEZY_PIN, env)
    binary = args.git_source / 'git'
    version = capture([binary, '--version', '--build-options'], directory, env)
    release_line = version['stdout'].splitlines()[:1]
    expected_versions = [['git version 2.43.0']]
    if args.phase == 'diagnostic':
        expected_versions.append(['git version 2.43.0.dirty'])
    if version['exit_code'] != 0 or release_line not in expected_versions:
        raise RuntimeError(f'Wrong binary: {version["stdout"]} {version["stderr"]}')
    git.update(binary_sha256=digest(binary.read_bytes()), version_receipt=version,
               compiler=capture(['/usr/bin/gcc', '--version'], directory, env),
               make=capture(['/usr/bin/make', '--version'], directory, env))
    breezy.update(
        backend='patiencediff._patiencediff_py.PatienceSequenceMatcher_py',
        module_sha256={str(p.relative_to(args.breezy_source)): digest(p.read_bytes()) for p in
                       (args.breezy_source/'patiencediff').glob('*.py')},
        c_extension_files=sorted(str(p.name) for p in (args.breezy_source/'patiencediff').glob('*.so')),
        install='Direct import of the pinned source checkout via worker, no compiled Breezy extension selected.',
    )
    return {
        'schema': 1, 'generated_utc': now(), 'phase': args.phase,
        'git': git, 'breezy': breezy,
        'python': {'executable': sys.executable, 'version': sys.version, 'implementation': platform.python_implementation()},
        'os': {'platform': platform.platform(), 'uname': list(platform.uname()),
               'libc': list(platform.libc_ver()), 'os_release': platform.freedesktop_os_release()},
        'inputs_file_sha256': digest((HERE / 'inputs.json').read_bytes()),
        'runner_sha256': digest(Path(__file__).read_bytes()),
        'environment_policy': 'See per-run environment dictionary. No inherited Git config or Python package path.',
        'bytes_policy': 'UTF-8 with surrogateescape for lossless stdout/stderr. Hashes are over captured bytes.',
    }


def public_suites(args):
    git_tests = [
        't4033-diff-patience.sh', 't4050-diff-histogram.sh',
        't4032-diff-inter-hunk-context.sh', 't4061-diff-indent.sh',
    ]
    for name in git_tests:
        with tempfile.TemporaryDirectory(prefix='public-git-', dir=args.scratch) as temp:
            env = clean_environment(Path(temp))
            command = ['/bin/sh', './' + name, f'--root={temp}']
            yield {'suite': name, **capture(command, args.git_source/'t', env, timeout=120)}
    with tempfile.TemporaryDirectory(prefix='public-breezy-', dir=args.scratch) as temp:
        directory = Path(temp)
        env = clean_environment(directory)
        env['PYTHONPATH'] = str(args.breezy_source)
        command = [sys.executable, '-B', '-S', '-m', 'unittest', '-v', 'patiencediff.test_patiencediff']
        yield {'suite': 'patiencediff.test_patiencediff', **capture(command, directory, env, timeout=120)}


def select_hunks(output):
    """Return raw hunks (header, body), isolating the engine's file header."""
    hunks = []
    for line in output.splitlines(keepends=True):
        if line.startswith('@@ '):
            if not HEADER.fullmatch(line):
                raise ValueError(f'invalid fixture hunk header {line!r}')
            hunks.append((line, []))
        elif hunks:
            if line[0] not in ' +-':
                raise ValueError(f'invalid fixture hunk line {line!r}')
            hunks[-1][1].append(line)
    if output and not hunks:
        raise ValueError('nonempty output without hunks in a text fixture')
    return hunks


def normalize_hunks(hunks, method):
    """Canonical zero-based start/length pairs and exact body, language-neutral header."""
    canonical = []
    for header, body in hunks:
        a_start, a_size, b_start, b_size = HEADER.fullmatch(header).groups()
        starts = (int(a_start), int(b_start))
        counts = tuple(1 if value is None else int(value) for value in (a_size, b_size))
        breezy_emitter = method in (BREEZY, 'breezy-default')
        offsets = [start - (size > 0 or breezy_emitter) for start, size in zip(starts, counts)]
        if any(offset < 0 for offset in offsets):
            raise ValueError(f'invalid starting offset {header!r}')
        if counts != (sum(s[0] != '+' for s in body), sum(s[0] != '-' for s in body)):
            raise ValueError(f'hunk body lengths disagree {header!r}')
        canonical.append([*offsets, *counts, body])
    return canonical


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--git-source', type=Path, required=True)
    parser.add_argument('--breezy-source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--phase', choices=('stock', 'diagnostic', 'challenges'), default='stock')
    args = parser.parse_args(argv)
    for field in ('git_source', 'breezy_source', 'out', 'scratch'):
        setattr(args, field, getattr(args, field).resolve())
    args.scratch.mkdir(parents=True, exist_ok=True)
    args.out.mkdir(parents=True, exist_ok=True)
    cases = load_cases()
    metadata = environment(args)
    if args.phase == 'stock':
        save_jsonl(args.out / 'base.jsonl', collect(args, cases, basic_trials(cases), 'base'))
        save_jsonl(args.out / 'controls.jsonl', collect(args, cases, control_trials(), 'controls'))
        save_jsonl(args.out / 'public.jsonl', public_suites(args))
        save_json(args.out.parent / 'environment.json', metadata)
        sources = ('base', 'controls', 'public')
    elif args.phase == 'diagnostic':
        save_jsonl(args.out / 'diagnostic-base.jsonl',
                   collect(args, cases, basic_trials(cases, repeats=1), 'diagnostic-base', trace=True))
        save_jsonl(args.out / 'diagnostic-controls.jsonl',
                   collect(args, cases, control_trials(), 'diagnostic-controls', trace=True))
        save_json(args.out / 'diagnostic-environment.json', metadata)
        sources = ('diagnostic-base', 'diagnostic-controls')
    else:
        save_jsonl(args.out / 'challenges.jsonl',
                   collect(args, challenge_cases(cases), challenge_trials(), 'challenges'))
        sources = ('challenges',)
    failed = 0
    for name in sources:
        rows = load_jsonl(args.out / f'{name}.jsonl')
        errors = sum(row['exit_code'] != 0 if name == 'public' else row['outcome'] == 'run_error'
                     for row in rows)
        failed += errors
        print(f'{name}: {len(rows)} receipts, {errors} errors')
    return int(failed != 0)


if __name__ == '__main__':
    if sys.argv[1:2] == ['_worker']:
        worker(sys.argv[2:])
    else:
        raise SystemExit(main(sys.argv[1:]))
