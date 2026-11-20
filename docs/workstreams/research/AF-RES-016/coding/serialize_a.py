#!/usr/bin/env python3
"""Serialize the researcher's handwritten TSV. Does not infer or revise labels."""
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
raw_path = BASE / 'coding/coder-a-raw.tsv'
with raw_path.open() as f:
    raw = list(csv.DictReader(f, delimiter='\t'))
units = json.loads((BASE / 'sample/units.json').read_text())['units']
assert len(raw) == len(units) == 198
assert {r['unit_id'] for r in raw} == {r['unit_id'] for r in units}
assert len({r['unit_id'] for r in raw}) == len(raw)
allowed = {
    'S1': {'product','component','principle','mixed','unknown'},
    'S2': {'whole','part','reference','comparison','none','mixed','unknown'},
    'form': {'app','service','library','framework','standard','document','pattern','research','data','mixed','unknown'},
    'confidence': {'high','medium','low'},
    'ambiguity': {'none','boundary','context','polysemy'},
}
rows = []
for r in raw:
    assert None not in r, r
    for k, values in allowed.items():
        assert r[k] in values, (r['unit_id'], k, r[k])
    assert r['reason'].strip()
    rows.append({
        'unit_id': r['unit_id'], 'S1': r['S1'], 'S2': r['S2'],
        'S3': {'form': r['form'], 'contribution': r['S2']},
        'confidence': r['confidence'], 'ambiguity': r['ambiguity'],
        'reason': r['reason'],
    })
result = {
    'coder': 'a', 'model': 'GPT-6 Astra Pro', 'human': False,
    'codebook_version': '1.0', 'input_packet': 'sample/units.json',
    'codebook_commit': '68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0',
    'sample_commit': '019f0fcc6ee07946cd337aa43fb708784dd67e5a',
    'read_prior_study_labels': True, 'read_coder_b': False,
    'raw_response': 'coding/coder-a-raw.tsv',
    'raw_sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
    'method': 'Researcher manually assigned each row; script only serializes fixed responses. S3 contribution is the same variable as S2.',
    'rows': rows,
}
(BASE / 'coding/coder-a.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'rows':len(rows),'sample_counts':{s:sum(u['sample']==s for u in units) for s in ('011','012','004')},'raw_sha256':result['raw_sha256']}, ensure_ascii=False))
