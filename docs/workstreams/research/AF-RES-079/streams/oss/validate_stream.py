"""Check ledger references and distinguish source evidence from native pairs."""
import datetime
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
sources = [json.loads(x) for x in (root / 'sources.jsonl').read_text().splitlines()]
observations = [json.loads(x) for x in (root / 'observations.jsonl').read_text().splitlines()]
native = [json.loads(x) for x in (root / 'current-native.jsonl').read_text().splitlines()]
events = json.loads((root / 'events.json').read_text())
packet = json.loads((root / 'evidence-packet.json').read_text())
receipt = json.loads((root / 'current-native.receipt.json').read_text())
ids = {x['source_id'] for x in sources}
errors = []

def require(ok, message):
    if not ok:
        errors.append(message)

require(len(ids) == len(sources), 'source_id must be unique')
require({e['event_id'] for e in events} == {'O01', 'O02', 'O03', 'O04'}, 'natural sample changed')
for s in sources:
    for field in ['source_id', 'work_id', 'actual_opened_url', 'checked_utc',
                  'publisher', 'edition', 'section', 'finding', 'limitations',
                  'counterevidence', 'count_reason', 'fixed_location']:
        require(bool(s.get(field)), '{} missing {}'.format(s['source_id'], field))
    if s.get('counted_independent_work'):
        require(s['access_status'] == 'directly_read', 'counted unread source ' + s['source_id'])
for e in events:
    require(all(s in ids for s in e['sources']), 'unresolved event reference ' + e['event_id'])
    require(e['runtime_pair_observed'] is False, 'unexecuted historical pair marked observed')
    require(e['old_commit'] and e['new_commit'], 'missing fixed edition ' + e['event_id'])
    for q in ['P1', 'P2']:
        require(any(o['event_id'] == e['event_id'] and o['question'] == q for o in observations),
                'missing {} {}'.format(e['event_id'], q))
for o in observations:
    require(all(s in ids for s in o['evidence_source_ids']), 'unresolved observation reference ' + o['observation_id'])
require(packet['first_decision_and_repair_visible'] is False, 'masked packet exposes first decision')
require(len(native) == receipt['rows'] == 50, 'native row count differs from receipt')
require(all(x['historical_pair_claim'] is False for x in native), 'single-release probe claims paired evidence')
require(all(x['environment']['scipy'] == '1.17.0' for x in native), 'current version changed without review')
require(hashlib.sha256((root / 'probe.py').read_bytes()).hexdigest() == receipt['script_sha256'], 'probe hash mismatch')
require(hashlib.sha256((root / 'current-native.jsonl').read_bytes()).hexdigest() == receipt['result_sha256'], 'native result hash mismatch')
count = len({s['work_id'] for s in sources if s['counted_independent_work']})
require(count == 6, 'conservative original-work grouping changed')
out = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'runner': 'oss_evidence agent via local tools.exec_command',
       'command': 'python -B docs/workstreams/research/AF-RES-079/streams/oss/validate_stream.py',
       'cwd': str(Path.cwd()), 'exit_code': 1 if errors else 0, 'errors': errors,
       'natural_events': len(events), 'source_rows': len(sources),
       'counted_original_work_families': count, 'observation_rows': len(observations),
       'current_native_rows': len(native), 'historical_native_pairs_observed': 0,
       'limit': 'Structural reference, evidence-label and checksum checks only. This does not execute historical releases or independent rereview.'}
(root / 'validation.receipt.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False))
raise SystemExit(out['exit_code'])
