#!/usr/bin/env python3
"""Extract observed decisions from diagnostic stderr and compare stock stdout."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from analyze import reads
from run import BREEZY, HERE, compact, load_cases, save_json


def trial_key(row):
    return (row['case'], row['method'], row['direction'], row['context'], row['indent'],
            row['repeat'], tuple(row['extra']))


def positions(flags):
    orders = [[i for i, is_changed in enumerate(side, 1) if is_changed == '0'] for side in flags]
    return [list(pair) for pair in zip(*orders, strict=True)]


def integers(values):
    return list(map(int, values))


def c_trace(row):
    events = [line.split()[1:] for line in row['stderr'].splitlines() if line.startswith('AF227 ')]
    flags = {event[1]: event[2:4] for event in events if event[0] == 'flags'}
    pre, post = positions(flags['pre-compact']), positions(flags['post-compact'])
    method = row['method']
    scope, candidates, selected = [], [], []
    common = '범위 밖'
    if method == 'myers':
        classic = [integers(event[2:]) for event in events if event[:2] == ['M', 'classic']]
        scope = classic[0]
        branch = 'classic-direct'
        scan = 'forward/backward on reduced edit graph'
        root_unit = 'reduced graph split coordinates; no unique filter'
        candidates = [event[2:] for event in events if event[:2] == ['M', 'diagonal']]
        splits = [integers(event[2:]) for event in events if event[:2] == ['M','split']]
        selected = splits[0] if splits else []
    else:
        symbol = 'P' if method == 'patience' else 'H'
        relevant = [ev[1:] for ev in events if ev[0] == symbol]
        scope = integers(relevant[0][1:])
        root = []
        for event in relevant[1:]:
            if event[0] == 'scope':
                break
            root.append(event)
        candidates = [integers(ev[1:]) for ev in root if ev[0] == 'candidate']
        if method == 'patience':
            scan = 'A scan, B rank'
            root_unit = 'candidate A/B line pairs and pile0; selected A/B pairs'
            branch = next(ev[1] for ev in root if ev[0] == 'branch')
            selected = [integers(ev[1:]) for ev in root if ev[0] == 'selected']
            common = next((int(ev[1]) for ev in root if ev[0] == 'common'), '범위 밖')
        else:
            scan = 'A occurrence chain, B seeds increasing with block skips'
            root_unit = 'B seed, A start/end, B start/end, A rarity, won; selected inclusive A/B region'
            status, a1, a2, b1, b2 = next(integers(ev[1:]) for ev in root if ev[0] == 'result')
            branch = 'classic-fallback' if status == 1 else 'direct-no-region' if a1 == 0 else 'histogram-region'
            selected = [[i, j] for i, j in zip(range(a1, a2+1), range(b1,b2+1), strict=True)] if a1 else []
    return {
        'root_scope': scope, 'scan': scan, 'root_unit': root_unit,
        'common_presence': common, 'branch': branch, 'candidates': candidates, 'root_selection': selected,
        'classic_entered': any(ev[:2] == ['M','classic'] for ev in events),
        'pre_pairs': pre, 'post_pairs': post, 'flag_strings': flags,
    }


def py_trace(row):
    events = [json.loads(line.removeprefix('AF227PY ')) for line in row['stderr'].splitlines()
              if line.startswith('AF227PY ')]
    root_scope = events[0]['bounds0_half_open']
    root = []
    for event in events[1:]:
        if event['event'] == 'unique-result':
            selected = [[a+1,b+1] for a,b in event['pairs_local0']]
            break
        if event['event'] == 'unique-candidate':
            root.append([event['a_local0']+1,event['b_local0']+1,event['pile0']])
    else:
        raise ValueError(f"{row['id']}: root unique result missing")
    span = next(ev for ev in events if ev['event'] == 'recurse-return' and ev['bounds0_half_open'] == root_scope)
    pairs = [[a+1,b+1] for a,b in span['appended_pairs0']]
    return {
        'root_scope': root_scope, 'scan': 'B scan, A rank',
        'root_unit': 'candidate A/B pairs with pile0 and selected 1-based pairs; scope 0-based half-open',
        'common_presence': '범위 밖', 'branch': span['branch'], 'candidates': root, 'root_selection': selected,
        'classic_entered': False, 'pre_pairs': pairs, 'post_pairs': pairs, 'flag_strings': '범위 밖',
    }


def diagnostic_links(directory, cases):
    record = {}
    for name in ('base','controls'):
        originals = {trial_key(r):r for r in reads(directory/f'{name}.jsonl', cases)}
        for row in reads(directory/f'diagnostic-{name}.jsonl', cases):
            stock = originals[trial_key(row)]
            equal = (row['stdout'], row['exit_code'], row['matching']) == (
                stock['stdout'], stock['exit_code'], stock['matching'])
            trace = py_trace(row) if row['method'] == BREEZY else c_trace(row)
            rows_agree = trace['post_pairs'] == row['display_kept']
            key = (name, trial_key(row))
            if key in record:
                raise ValueError(f"{row['id']}: duplicate trace")
            record[key] = {
                'row': row, 'trace': trace, 'stock': stock, 'stock_same': equal, 'aligned': rows_agree,
            }
    return record


def write_anchors(path, record):
    with path.open('w', encoding='utf-8', newline='') as stream:
        columns = (
            'case','method','phase','direction','context','indent','root_scope','root_scan','root_candidate_unit',
            'root_common_presence','root_branch','root_candidates_in_order','root_selected','classic_entered_any_scope',
            'pre_compact_pairs_1based','post_compact_pairs_1based','change_masks','actual_hunk_headers',
            'display_pairs_1based','post_pairs_agree','stock_stdout_and_exit_and_blocks_match','diagnostic_receipt','stock_receipt',
        )
        result = csv.writer(stream, lineterminator='\n')
        result.writerow(columns)
        for value in record.values():
            row, trace = value['row'], value['trace']
            result.writerow((
                row['case'],row['method'],row['phase'],row['direction'],row['context'],
                '범위 밖' if row['indent'] is None else row['indent'], compact(trace['root_scope']), trace['scan'], trace['root_unit'],
                trace['common_presence'],trace['branch'],compact(trace['candidates']),compact(trace['root_selection']),
                trace['classic_entered'],compact(trace['pre_pairs']),compact(trace['post_pairs']),compact(trace['flag_strings']),
                compact(row['headers']),compact(row['display_kept']),value['aligned'],value['stock_same'],
                row['receipt_ref'],value['stock']['receipt_ref'],
            ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipts', type=Path, default=HERE/'receipts')
    parser.add_argument('--output', type=Path, default=HERE)
    args = parser.parse_args()
    cases = load_cases()
    record = diagnostic_links(args.receipts, cases)
    counts = Counter(name for name,_ in record)
    for name, planned in [('base',32), ('controls',112)]:
        if counts[name] != planned:
            raise ValueError(f'{name}: expected {planned} trace receipts, saw {counts[name]}')
    write_anchors(args.output/'anchors.csv', record)
    matches = {
        name: {field: sum(value[field] for (kind,_),value in record.items() if kind == name)
               for field in ('stock_same','aligned')}
        for name in counts
    }
    save_json(args.output/'receipts/diagnostic-comparison.json', {
        'observed_by_phase': counts, 'matches_by_phase': matches,
        'compaction_changed': [
            v['row']['id'] for v in record.values() if v['trace']['pre_pairs'] != v['trace']['post_pairs']],
        'differences': [v['row']['id'] for v in record.values() if not v['stock_same'] or not v['aligned']],
    })
    print(matches)


if __name__ == '__main__':
    main()
