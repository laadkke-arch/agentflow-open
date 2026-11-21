#!/usr/bin/env python3
"""Check actual Git ancestry and owned-path scope without modifying inputs."""
import argparse, datetime, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, text=True).strip())
PREFIX = ROOT.relative_to(REPO).as_posix() + '/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def ancestor(a, b):
    return subprocess.run(['git', 'merge-base', '--is-ancestor', a, b], cwd=REPO).returncode == 0

def first_addition(paths, source):
    commits = git('rev-list', '--reverse', source + '..HEAD', '--', *paths).decode().splitlines()
    return commits[0] if commits else None

def main(write):
    lock = json.loads((ROOT/'INPUT_LOCK.json').read_text())
    order = json.loads((ROOT/'runs/COMMIT_ORDER.json').read_text())
    source, first = lock['source_commit'], order['first_execution_commit']
    actual_first = first_addition([PREFIX+'runs/A/', PREFIX+'runs/P/'], source)
    errors, checks = [], []
    for row in order['checks']:
        passed = row['commit'] != first and ancestor(row['commit'], first)
        checks.append({'artifact': row['artifact'], 'commit': row['commit'],
                       'strict_ancestor_of_first_execution': passed})
        if not passed:
            errors.append('Preregistration ancestry: '+row['artifact'])
    if actual_first != first:
        errors.append('Recorded first execution commit differs from Git history')
    if not ancestor(source, first) or not ancestor(first, 'HEAD'):
        errors.append('Foundation/execution/HEAD ancestry failed')
    changed = git('diff', '--name-only', source, 'HEAD').decode().splitlines()
    outside = [p for p in changed if not p.startswith(PREFIX)]
    if outside:
        errors.append('Committed changes outside owned_path')
    copies = []
    for path, commit, old_path in [
        ('RULES_A.md', lock['fixed_inputs']['AF-RES-013'], lock['rules_a_source_path']),
        ('gold/RULES.md', lock['fixed_inputs']['AF-RES-014'],
         'docs/workstreams/research/AF-RES-014/qrels/RULES.md')]:
        passed = git('show', commit+':'+old_path) == (ROOT/path).read_bytes()
        copies.append({'path': path, 'source_commit': commit, 'source_path': old_path,
                       'byte_identical': passed})
        if not passed:
            errors.append('Copied rule differs: '+path)
    claim_order = None
    manifest = ROOT/'claims/verification-manifest.json'
    if manifest.exists():
        sample_commit = json.loads(manifest.read_text())['sample_commit']
        first_verified = first_addition([PREFIX+'claims/verified/'], source)
        sample_equal = git('show', sample_commit+':'+PREFIX+'claims/SAMPLE.json') == (ROOT/'claims/SAMPLE.json').read_bytes()
        before = None if first_verified is None else sample_commit != first_verified and ancestor(sample_commit, first_verified)
        claim_order = {'sample_commit': sample_commit, 'first_committed_verification': first_verified,
                       'sample_bytes_unchanged': sample_equal, 'strict_ancestor': before}
        if not sample_equal or before is False:
            errors.append('Sample/verification commit order failed')
    report = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'source_commit': source, 'head': git('rev-parse', 'HEAD').decode().strip(),
              'recorded_first_execution_commit': first, 'actual_first_execution_commit': actual_first,
              'preregistration_checks': checks, 'copied_rules': copies,
              'committed_changed_paths': len(changed), 'outside_owned_path': outside,
              'claim_sampling_order': claim_order, 'errors': errors,
              'method': 'Git ancestry and blob equality, never lexicographic SHA ordering. Working-tree cleanliness is checked separately after the final commit.'}
    if write:
        (ROOT/'analysis/commit-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true')
    main(parser.parse_args().write)
