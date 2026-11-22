import json
import sys
from pathlib import Path
from datetime import datetime, timezone

folder = Path(__file__).resolve().parent
payload = json.load(sys.stdin)
now = datetime.now(timezone.utc).isoformat()
for record in payload.get('reads', []):
    record.setdefault('checked_utc', now)
    with (folder / 'reads.jsonl').open('a') as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + '\n')
for record in payload.get('judgments', []):
    with (folder / 'judgments.jsonl').open('a') as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + '\n')
for note in payload.get('notes', []):
    with (folder / 'reader-notes.md').open('a') as handle:
        handle.write(f'- {now}: {note}\n')
print(json.dumps({'appended_reads': len(payload.get('reads', [])), 'appended_judgments': len(payload.get('judgments', []))}))
