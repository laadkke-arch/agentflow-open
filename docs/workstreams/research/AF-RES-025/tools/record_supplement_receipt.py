#!/usr/bin/env python3
"""Record metadata and hash of an actual tool result without republishing it."""
import hashlib
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
payload = json.loads(sys.argv[1])
result = payload.pop('result')
encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
blocks = []
for item in result.get('content', []):
    if item.get('type') != 'text':
        continue
    for block in item['text'].split('--------------------------------------------------------------------------------'):
        refs = re.findall(r'【(turn\w+)】', block)
        if not refs:
            continue
        lines = block.strip().splitlines()
        blocks.append({'ref_ids': refs, 'header': lines[0],
                       'total_lines': int(re.search(r'Total lines: (\d+)', block)[1]) if re.search(r'Total lines: (\d+)', block) else None,
                       'observed_failure': 'Internal Error' in block or 'Failed to fetch' in block,
                       'rewritten_summary': 'rewritten summary' in block,
                       'not_found': 'No matching text found' in block})
receipt = {**payload, 'response_sha256': hashlib.sha256(encoded).hexdigest(),
           'hash_encoding': 'UTF-8 sorted compact JSON of complete tool result',
           'result_metadata': blocks, 'source_body_republished': False,
           'wall_time_precision': 'clock timestamps at one-second resolution; no per-operation milliseconds supplied',
           'tokens': 'unknown', 'billed_cost': 'unknown', 'human_hours_saved': 'unknown',
           'phase': 'supplemental_after_primary_seal', 'primary_seal_commit': 'd1f506b1dde91e706360846f4c2eac5baabe492e'}
folder = BASE / 'supplements/receipts'; folder.mkdir(parents=True, exist_ok=True)
(folder / (payload['receipt_id'] + '.json')).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'receipt_id': payload['receipt_id'], 'blocks': len(blocks), 'sha256': receipt['response_sha256']}))
