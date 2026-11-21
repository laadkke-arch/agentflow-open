#!/usr/bin/env python3
"""Recompute audits and statistics from preserved observations, without new searches.

This does not reproduce a fresh model's stochastic web-search execution. It
validates the existing frozen inputs, runs, normalization/judgment coverage and
sampled fact checks, then recomputes their deterministic joins and estimates.
"""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    ['analysis/verify_inputs.py', '--write'],
    ['analysis/commit_audit.py', '--write'],
    ['analysis/run_inventory.py', '--write'],
    ['analysis/protocol_audit.py'],
    ['analysis/citation_audit.py', '--write'],
    ['analysis/map_candidates.py', '--finalize'],
    ['judging/batches.py', '--validate'],
    ['judging/reason_batches.py', '--combine'],
    ['claims/verification_batches.py', '--combine'],
    ['analysis/collect_run_evidence.py'],
    ['analysis/collect_judging_evidence.py'],
    ['analysis/source_inventory.py'],
    ['analysis/build_observations.py'],
    ['analysis/metrics.py'],
    ['analysis/source_order.py'],
    ['analysis/judge_consistency.py'],
    ['analysis/counterexamples.py'],
    ['analysis/finalize_search_log.py'],
]

def main(write):
    if not write:
        print(json.dumps({'root': str(ROOT), 'steps': STEPS,
                          'note': 'Pass --write after all required actual observations are present. This recomputes derived files and observation timestamps; it never requests new web/model output.'}, indent=2))
        return
    dispatch = json.loads((ROOT/'questions/dispatch.json').read_text())['order']
    required = [d['output'] for d in dispatch] + [
        'judging/key.json', 'judging/judge-manifest.json',
        'judging/reason-manifest.json', 'claims/verification-manifest.json',
        'claims/SAMPLE.json', 'claims/pool.json', 'claims/uncertainty.json',
        'analysis/mapping-decisions.json']
    missing = [p for p in required if not (ROOT/p).exists()]
    if missing:
        raise SystemExit('Required observations absent; no analysis run: '+json.dumps(missing))
    for args in STEPS:
        print('Running '+args[0], flush=True)
        subprocess.run([sys.executable, *args], cwd=ROOT, check=True)
    print('Completed recomputation from preserved observations. Narrative RESULT/SELF_CHECK/HANDOFF remain separately reviewed artifacts.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--write', action='store_true')
    main(parser.parse_args().write)
