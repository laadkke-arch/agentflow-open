"""Verify the sealed N/H strings and, when available, their original source offsets.

The default performs local source-byte checks. --cards-only needs only committed
small artifacts. --download-missing performs measured public reacquisition;
current pages can legitimately fail the old whole-response hash on replay.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parents[1]
sys.path.insert(0, str(ROOT))
from parse_html import parse
sys.path.insert(0, str(TASK / 'scripts'))
from fetchlib import fetch

def sha(data):
    return hashlib.sha256(data).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('--cards-only', action='store_true')
parser.add_argument('--download-missing', action='store_true')
args = parser.parse_args()
components = [json.loads(x) for x in (ROOT / 'evidence-components.jsonl').read_text().splitlines()]
sources = {x['source_id']: x for x in map(json.loads, (ROOT / 'sources.jsonl').read_text().splitlines())}
attempts = {x['attempt_id']: x for x in map(json.loads, (ROOT / 'attempts.jsonl').read_text().splitlines())}
attempt_by_path = {x['stored_path']: x for x in attempts.values() if x.get('stored_path')}
memo = {}
checks = []

def original_file(span):
    relative = span['path']
    if relative in memo:
        return memo[relative]
    path = TASK / relative
    if path.exists():
        memo[relative] = path
        return path
    if not args.download_missing:
        raise SystemExit('Missing ' + relative + '; use --cards-only or --download-missing')
    if relative.endswith('/history/gawk-5.0.1/doc/gawk.info'):
        attempt = attempts['G-HGET006']
        raw, receipt = fetch(attempt['url'], ROOT / 'replay-nh', 'G-H06-REBUILD',
                             'reconstruct_historical_member', ['G03', 'G04'], 'gawk-5.0.1.tar.xz')
        assert sha(raw) == attempt['sha256'], 'Historical archive bytes changed'
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            body = archive.extractfile('gawk-5.0.1/doc/gawk.info').read()
        path = ROOT / 'replay-nh' / 'gawk-5.0.1.info'
        path.write_bytes(body)
    else:
        attempt = attempt_by_path[relative]
        suffix = Path(relative).suffix
        raw, receipt = fetch(attempt['url'], ROOT / 'replay-nh', attempt['attempt_id'] + '-REBUILD',
                             'reconstruct_NH_source', attempt.get('case_ids', []),
                             attempt['attempt_id'] + suffix)
        path = TASK / receipt['stored_path']
    memo[relative] = path
    return path

for row in components:
    rid = row['reference_id']
    assert row['decision_or_adjudication_written'] is False
    for name in ['N', 'H']:
        card = row[name]
        exact = (ROOT / 'components' / (rid + '-' + name + '.txt')).read_bytes()
        assert exact == card['text'].encode('utf8'), (rid, name, 'card bytes')
        assert sha(exact) == card['text_sha256'], (rid, name, 'card hash')
        assert len(exact) == card['text_bytes']
        assert len(card['text']) == card['text_chars'] <= 1600
        assert all(sid in sources for sid in card['source_ids'])
        assert card['text'] == '\n\n'.join(s['text'] for s in card['excerpts'])
        for span in card['excerpts']:
            assert span['source_id'] in card['source_ids']
            assert sha(span['text'].encode()) == span['text_sha256']
            assert len(span['text']) == span['text_chars'] <= 1600
            if not args.cards_only:
                path = original_file(span)
                raw = path.read_bytes()
                assert sha(raw) == span['source_sha256'], (rid, name, 'source bytes changed', span['path'])
                if span['normalization'].startswith('UTF-8 decode'):
                    normalized = raw.decode('utf8', errors='replace')
                else:
                    normalized = parse(path)['text']
                assert sha(normalized.encode()) == span['normalized_text_sha256']
                assert normalized[span['start_char']:span['end_char']] == span['text']
        checks.append({'reference_id': rid, 'component': name,
                       'sha256': sha(exact), 'chars': len(card['text']), 'utf8_bytes': len(exact),
                       'source_ids': card['source_ids'], 'matched': True,
                       'source_offsets_checked': not args.cards_only})

# B excerpts were sealed remotely before collection; reject accidental changes.
base_receipt = json.loads((ROOT / 'base-reconstruction-receipt.json').read_text())
for b in base_receipt['rows']:
    exact = (ROOT / 'base' / (b['reference_id'] + '.txt')).read_bytes()
    assert sha(exact) == b['B_context_sha256']

print(json.dumps({'check': 'source bytes → deterministic text → offsets → exact N/H component bytes',
                  'mode': 'cards-only' if args.cards_only else 'full-local-source',
                  'exit_code': 0, 'components_checked': len(checks),
                  'unique_source_files_checked': len(memo), 'B_unchanged': 6,
                  'source_id_joins': 'all matched', 'rows': checks}, ensure_ascii=False, indent=2))
