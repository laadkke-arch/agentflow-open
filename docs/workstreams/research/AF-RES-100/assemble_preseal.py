"""Assemble the sealed pre-outcome judgments and 16 comparisons from ledgers.

This never retrieves a question answer or changes frozen packet definitions.
Run after all readers and the separate availability audits have finished.
"""
from pathlib import Path
from collections import Counter
import argparse
import copy
import csv
import datetime
import hashlib
import io
import json

ROOT = Path(__file__).resolve().parent

def jl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]

def jsonl(rows):
    return ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows)

def outputs():
    packets = jl(ROOT / 'packets.jsonl')
    proto = json.loads((ROOT / 'protocol.json').read_text())
    initial = []
    for f in sorted((ROOT / 'evidence/readers').glob('R*/judgments.jsonl')):
        initial.extend(jl(f))
    assert len(initial) == 32
    by_initial = {j['packet_id']: j for j in initial}
    audits = {}
    for name in ['jq-availability.jsonl', 'pandoc-availability.jsonl']:
        for r in jl(ROOT / 'evidence/audit' / name):
            assert r['packet_id'] not in audits
            audits[r['packet_id']] = (name, r)
    assert len(audits) == 32
    ordered = []; final = []; changes = []
    for p in packets:
        j = by_initial[p['packet_id']]
        ordered.append(j)
        name, a = audits[p['packet_id']]
        assert a['initial_complete'] == j['complete']
        r = copy.deepcopy(j)
        r['initial_complete'] = j['complete']
        r['initial_judgment_recorded_utc'] = j['recorded_utc']
        r['evidence_availability'] = {
            'review_file': 'evidence/audit/' + name,
            'recorded_utc': a['recorded_utc'],
            'complete': a['availability_complete'],
            'classification': a['classification'],
            'initial_discovery': False,
            'independent_human_review': False,
        }
        if a['availability_complete'] != j['complete']:
            assert a.get('conditions')
            r['conditions'] = a['conditions']
            r['complete'] = a['availability_complete']
            r['recorded_utc'] = a['recorded_utc']
            changes.append({'packet_id': p['packet_id'], 'case_id': p['case_id'],
                            'before': j, 'after': r, 'reason': a.get('reason', a.get('notes'))})
        final.append(r)
    byj = {j['packet_id']: j for j in final}
    pairs = []
    for c in proto['cases']:
        for mode in ['F', 'S']:
            pa, pb = [next(p for p in packets if (p['case_id'], p['policy'], p['mode']) ==
                           (c['case_id'], policy, mode)) for policy in ['A', 'B']]
            a, b = byj[pa['packet_id']], byj[pb['packet_id']]
            comparable = c.get('stable_adjacent_resolved', True)
            result = ('both' if a['complete'] and b['complete'] else 'A_only' if a['complete']
                      else 'B_only' if b['complete'] else 'neither') if comparable else 'incomparable'
            pairs.append({'case_id': c['case_id'], 'question_id': c['question_id'],
                          'stratum': c['stratum'], 'mode': mode,
                          'A_packet': pa['packet_id'], 'B_packet': pb['packet_id'],
                          'A_complete': a['complete'], 'B_complete': b['complete'],
                          'A_conditions': ';'.join(x['id'] + ':' + x['status'] for x in a['conditions']),
                          'B_conditions': ';'.join(x['id'] + ':' + x['status'] for x in b['conditions']),
                          'comparable': comparable, 'result': result,
                          'exclusion_reason': '' if comparable else 'latest pre-question stable adjacent release not resolved; B slots3/4 empty',
                          'metric': 'packet-contained documentary sufficiency; not original-user runtime success'})
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(pairs[0])); writer.writeheader(); writer.writerows(pairs)
    return {
        'evidence/initial-judgments.jsonl': jsonl(ordered),
        'judgments.jsonl': jsonl(final),
        'evidence/audit/pre-outcome-changes.jsonl': jsonl(changes),
        'pairs.csv': stream.getvalue(),
    }, pairs, changes

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); args = ap.parse_args()
    files, pairs, changes = outputs()
    for name, body in files.items():
        target = ROOT / name
        if args.check:
            assert target.read_bytes() == body.encode(), 'reconstruction mismatch: ' + name
        else:
            target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(body.encode())
    print(json.dumps({'status': 'PASS', 'check_only': args.check, 'judgments': 32,
                      'comparisons': len(pairs), 'comparable': sum(p['comparable'] for p in pairs),
                      'pre_outcome_changes': len(changes),
                      'by_mode': {m: dict(Counter(p['result'] for p in pairs if p['mode'] == m)) for m in ['F','S']},
                      'files': {k: hashlib.sha256(v.encode()).hexdigest() for k,v in files.items()}}, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
