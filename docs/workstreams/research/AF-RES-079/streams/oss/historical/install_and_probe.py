"""Prepare four separate wheel-only environments and run the unchanged probe."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
runner = root / 'run_recorded.py'
python38 = root / 'python-downloads/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8'
probe = root.parent / 'probe.py'
versions = ['1.4.1', '1.5.0', '1.5.4', '1.6.0']

def run(label, command, timeout=120):
    result = subprocess.run([sys.executable, '-B', str(runner), '--label', label,
                             '--timeout', str(timeout), '--', *map(str, command)],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(json.dumps({'label': label, 'exit_code': result.returncode}), flush=True)
    return result.returncode

def one(version):
    env = root / 'envs' / ('scipy-' + version)
    executable = env / 'bin/python'
    steps = []
    commands = [
        ('venv', ['uv', 'venv', str(env), '--python', str(python38), '--no-python-downloads', '--no-config']),
        ('wheels', ['uv', 'pip', 'install', '--python', str(executable), '--only-binary=:all:',
                    '--default-index', 'https://pypi.org/simple',
                    '--system-certs', '--no-config', 'numpy==1.19.5', 'scipy==' + version]),
        ('freeze', ['uv', 'pip', 'freeze', '--python', str(executable), '--no-config']),
        ('probe', [str(executable), '-B', str(probe), '--output', str(root / ('scipy-' + version + '.jsonl'))])]
    for phase, command in commands:
        if phase == 'venv' and executable.exists():
            steps.append({'phase': phase, 'exit_code': 0, 'reused_existing_isolated_environment': True,
                          'creation_receipt': version + '-venv.receipt.json'})
            continue
        code = run(version + '-' + phase, command)
        steps.append({'phase': phase, 'exit_code': code})
        if code != 0:
            break
    return {'scipy_version': version, 'environment': str(env), 'steps': steps,
            'complete': len(steps) == len(commands) and all(x['exit_code'] == 0 for x in steps)}

start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(one, versions))
summary = {'started_utc': start, 'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'python_version': '3.8.20', 'numpy_pin': '1.19.5', 'source_builds_allowed': False,
           'global_install': False, 'results': results,
           'runner': 'oss_evidence agent via local tools.exec_command'}
(root / 'installation-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
raise SystemExit(0 if all(x['complete'] for x in results) else 1)
