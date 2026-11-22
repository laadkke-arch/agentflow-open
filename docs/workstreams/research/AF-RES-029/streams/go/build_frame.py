#!/usr/bin/env python3
"""Reproduce the frozen AF-RES-029 Go metadata ordering, without issue bodies."""
import csv
import gzip
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
metadata_path = root / 'frame-metadata.json'
if metadata_path.exists():
    rows = json.loads(metadata_path.read_text())
else:
    rows = json.loads(gzip.decompress((root / 'frame-metadata.json.gz').read_bytes()))
for row in rows:
    row['seed'] = f"AF-RES-029|v1|go|{row['period']}|{row['canonical_id']}"
    row['sha256_order_key'] = hashlib.sha256(row['seed'].encode()).hexdigest()
rows.sort(key=lambda row: (row['period'], row['sha256_order_key'], row['canonical_id']))
counts = {}
for row in rows:
    period = row['period']
    counts[period] = counts.get(period, 0) + 1
    row['period_order'] = counts[period]
with (root / 'frame.csv').open('w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
for period in counts:
    print(period, counts[period])
    for row in [row for row in rows if row['period'] == period][:10]:
        print(json.dumps({key: row[key] for key in ['period_order', 'canonical_id', 'title', 'first_public_date', 'sha256_order_key']}))
