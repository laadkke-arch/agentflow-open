"""Run an explicitly supplied command and retain its real exit status and log."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--label', required=True)
parser.add_argument('--timeout', type=int, default=180)
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command
if command and command[0] == '--':
    command = command[1:]
root = Path(__file__).resolve().parent
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
env = os.environ.copy()
env['UV_CACHE_DIR'] = str(root / 'cache')
env['UV_PYTHON_INSTALL_DIR'] = str(root / 'python-downloads')
env['UV_PYTHON_BIN_DIR'] = str(root / 'python-downloads' / 'bin')
env['UV_NO_PROGRESS'] = '1'
env['PYTHONDONTWRITEBYTECODE'] = '1'
try:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env, timeout=args.timeout)
    output, code = result.stdout, result.returncode
    timed_out = False
except subprocess.TimeoutExpired as exc:
    output = exc.stdout or ''
    if isinstance(output, bytes):
        output = output.decode(errors='replace')
    code, timed_out = 124, True
except Exception as exc:
    output, code, timed_out = repr(exc), 125, False
(root / (args.label + '.log')).write_text(output)
receipt = {'label': args.label, 'started_utc': start,
           'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'command_argv': command, 'cwd': str(Path.cwd()), 'exit_code': code,
           'timed_out': timed_out, 'timeout_seconds': args.timeout,
           'environment_overrides': {k: env[k] for k in ['UV_CACHE_DIR', 'UV_PYTHON_INSTALL_DIR',
                                                        'UV_PYTHON_BIN_DIR', 'UV_NO_PROGRESS',
                                                        'PYTHONDONTWRITEBYTECODE']},
           'runner': 'oss_evidence agent via tools.exec_command',
           'output_log': args.label + '.log'}
(root / (args.label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
print(output[-6000:])
raise SystemExit(code)
