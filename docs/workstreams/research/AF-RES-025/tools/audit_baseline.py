#!/usr/bin/env python3
"""Recount fixed AF-RES-021 citation coverage; never executes imported research code."""
import collections
import json
import pathlib
import subprocess

BASE = pathlib.Path(__file__).resolve().parents[1]
REPO = BASE.parents[3]
SHA = '29049a5f15b6ef7cd7431f59a059598db6f5d857'
ROOT = 'docs/workstreams/research/AF-RES-021/'

def rows(name):
    raw = subprocess.check_output(['git', 'show', SHA + ':' + ROOT + name], cwd=REPO, text=True)
    return [json.loads(line) for line in raw.splitlines() if line]

keys = {x['row']: x for x in rows('keys.jsonl')}
runs = rows('runs.jsonl')
out = []
for basis in ['official', 'history']:
    for budget in [1, 2, 4]:
        for mode in ['A', 'P', 'M']:
            selected = [r for r in runs if r['format'] == mode]
            counts = collections.Counter()
            differences = []
            for row in selected:
                key = keys[row['row']][basis]
                if key['verdict'] != 'support':
                    continue
                counts['support_denominator'] += 1
                pred = row['at'][str(budget)]
                opened = {e['id'] for e in row['opened'][:budget] if 'error' not in e}
                cited = set(pred['cited'])
                allowed = [set(g) for g in key['allowed']]
                old = pred['verdict'] == 'support' and any(g <= opened and g & cited for g in allowed)
                complete = pred['verdict'] == 'support' and any(g <= opened and g <= cited for g in allowed)
                counts['original_recovered'] += bool(old)
                counts['complete_citation_recovered'] += bool(complete)
                if bool(old) != bool(complete):
                    differences.append({'row': row['row'], 'opened': sorted(opened), 'cited': sorted(cited), 'allowed': key['allowed']})
            out.append({'basis': basis, 'budget': budget, 'format': mode, **counts, 'differences': differences})
result = {'fixed_input': SHA, 'scope': 'Arithmetic audit of fixed labels; no independent source truth recoding', 'rows': out}
print(json.dumps(result, ensure_ascii=False, indent=2))
