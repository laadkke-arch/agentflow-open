"""Restore committed dependency locks and repeat researcher inputs, never upstream CI.

Run from any directory with Python 3 and Node/npm installed:
  python -B path/to/replay/reproduce.py --install
Writes only the AF-RES-057 owned cache. No package lifecycle scripts are run.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
STREAM = HERE.parent
OWNED = STREAM.parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--install', action='store_true', help='npm ci using each committed lock')
parser.add_argument('--include-posthoc-sensitivity', action='store_true')
args = parser.parse_args()
tasks = [('YN1', '13.0.0-94', 8), ('YN2', '13.0.8', 4), ('YT1', '13.6.28', 2)]
if args.include_posthoc_sensitivity:
    tasks.append(('YT1-sensitivity-1308', '13.0.8', 2))
restored = set()
for label, version, expected_variants in tasks:
    project = OWNED / '.cache' / 'yjs' / 'reproduce' / version
    project.mkdir(parents=True, exist_ok=True)
    lock = json.loads((HERE / ('dependency-lock-' + version + '.json')).read_text())
    package = dict(lock['packages'][''])
    package['private'] = True
    (project / 'package.json').write_text(json.dumps(package, indent=2) + '\n')
    (project / 'package-lock.json').write_text(json.dumps(lock, indent=2) + '\n')
    if args.install and version not in restored:
        subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=project, check=True)
        restored.add(version)
    module = project / 'node_modules' / 'yjs'
    if not module.exists():
        raise SystemExit('Dependencies absent: rerun with --install')
    case = 'YT1' if label.startswith('YT1') else label
    command = ['node', str(STREAM / 'research_replay.cjs'), str(module), case]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    run = subprocess.run(command, capture_output=True, text=True)
    target = project / label
    target.with_suffix('.stdout.json').write_text(run.stdout)
    target.with_suffix('.stderr.txt').write_text(run.stderr)
    receipt = {'command': command, 'started_UTC': started,
               'ended_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'exit_code': run.returncode,
               'script_sha256': hashlib.sha256((STREAM / 'research_replay.cjs').read_bytes()).hexdigest(),
               'evidence_kind': 'researcher_replay', 'frozen_prediction': label != 'YT1-sensitivity-1308'}
    target.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    if run.returncode:
        raise SystemExit(f'{label}: Node exited {run.returncode}; see {target}')
    observed = json.loads(run.stdout)
    if len(observed['results']) != expected_variants or any(r['status'] != 'completed' for r in observed['results']):
        raise SystemExit(f'{label}: incomplete variants; see {target}')
    print(json.dumps({'label': label, 'variant_count': len(observed['results']),
                      'runtime': observed['runtime'], 'output': str(target.with_suffix('.stdout.json'))}))
