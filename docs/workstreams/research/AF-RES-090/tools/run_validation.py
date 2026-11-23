"""Run the unchanged repository gates at an immutable result SHA.

All temporary checkouts, test scratch and retained receipts stay in AF-RES-090.
The public GitHub origin is restored in the copy before --fetch checks.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

B = Path(__file__).resolve().parents[1]
REPO = B.parents[3]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('sha')
    a = p.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', a.sha):
        p.error('Expected a full immutable commit SHA')
    receipt_dir = B / 'evidence' / 'validation'
    receipt_dir.mkdir(exist_ok=True)
    temp = B / ('.verification-' + a.sha[:12])
    temp.mkdir()
    clone, scratch = temp / 'checkout', temp / 'scratch'
    scratch.mkdir()
    env = os.environ.copy()
    env.update(TMPDIR=str(scratch), TEMP=str(scratch), TMP=str(scratch), PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    records = []

    def run(name, argv, cwd, timeout):
        started = now()
        proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        files = {}
        for key, value in (('stdout', proc.stdout), ('stderr', proc.stderr)):
            path = receipt_dir / (name + '.' + key + '.log')
            path.write_text(value)
            files[key] = {'path': path.relative_to(B).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        record = {'name': name, 'target_sha': a.sha, 'command': argv, 'started_utc': started,
                  'completed_utc': now(), 'exit_code': proc.returncode, 'files': files}
        records.append(record)
        print(json.dumps({k: record[k] for k in ('name', 'target_sha', 'exit_code', 'completed_utc')}), flush=True)
        return proc

    try:
        clone_result = run('clone', ['git', 'clone', '--quiet', '--no-hardlinks', '--branch', 'work/research-af-res-090', '--single-branch', str(REPO), str(clone)], REPO, 120)
        if clone_result.returncode:
            raise RuntimeError('Validation clone failed')
        subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/laadkke-arch/agentflow-open.git'], cwd=clone, check=True)
        subprocess.run(['git', 'checkout', '--quiet', '-B', 'work/research-af-res-090', a.sha], cwd=clone, check=True)
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=clone, text=True).strip()
        if actual != a.sha:
            raise RuntimeError('Incorrect validation checkout')
        rel = 'docs/workstreams/research/AF-RES-090/'
        run('session-check', [sys.executable, '-B', '-m', 'workbench.session', 'check', rel + 'manifest.json', '--fetch'], clone, 120)
        run('research-ledgers', [sys.executable, '-B', rel + 'tools/validate_research.py'], clone, 120)
        run('python-stream', [sys.executable, '-B', rel + 'streams/python/validate.py'], clone, 60)
        run('common-cloud-check', [sys.executable, '-B', 'scripts/cloud_check.py', '--environment', 'chatgpt-work', '--fetch-contract', '--require-clean'], clone, 600)
        common = clone / '.workbench' / 'cloud-check.json'
        if common.exists():
            data = json.loads(common.read_text())
            shutil.copyfile(common, receipt_dir / 'common-cloud-receipt.json')
            for c in data.get('checks', []):
                for stream in ('stdout', 'stderr'):
                    source = clone / c[stream + '_log']
                    if source.exists():
                        shutil.copyfile(source, receipt_dir / ('common-' + c['name'] + '.' + stream + '.log'))
            for name in ('acceptance.json', 'check-0.log', 'check-1.log'):
                source = clone / '.workbench' / name
                if source.exists():
                    shutil.copyfile(source, receipt_dir / name)
        final_state = subprocess.check_output(['git', 'status', '--porcelain'], cwd=clone, text=True)
        result = {'checked_utc': now(), 'target_sha': a.sha,
                  'status': 'PASS' if all(r['exit_code'] == 0 for r in records) and not final_state else 'FAIL',
                  'checks': records, 'validation_checkout_clean_after': not bool(final_state),
                  'scratch_policy': 'Unchanged gates ran in a disposable clone and TMPDIR entirely under owned path. Original checkout shared files untouched by acceptance lab writes.',
                  'limits': 'Workbench and research consistency checks only. No R/Python project examples, animation, IIIF viewer or EPUB reader execution.'}
        (receipt_dir / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'status': result['status'], 'target_sha': a.sha, 'summary': 'evidence/validation/summary.json'}), flush=True)
        return 0 if result['status'] == 'PASS' else 1
    finally:
        shutil.rmtree(temp)


if __name__ == '__main__':
    raise SystemExit(main())
