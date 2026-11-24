#!/usr/bin/env python3
"""Turn lossless AF-RES-227 receipts into comparison units and tables."""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import json
from itertools import combinations
from pathlib import Path
import re

from run import (BREEZY, HERE, challenge_cases, compact, digest, encode, load_cases, load_jsonl,
                 normalize_hunks, save_json, select_hunks)


def align(row, case, canonical):
    """Validate displayed bytes against inputs and recover edit positions from the patch."""
    a, b = (case['a']['lf_elements'], case['b']['lf_elements'])
    if row['direction'] == 'reverse':
        a, b = b, a
    i = j = 0
    deletes, inserts, kept = [], [], []
    ignore_eol = '--ignore-space-at-eol' in row['argv']

    def equal(x, y):
        return x == y or (ignore_eol and x.rstrip(' \t\r\n\v\f') == y.rstrip(' \t\r\n\v\f'))

    def keep_gap(end_a, end_b):
        nonlocal i, j
        if end_a < i or end_b < j or end_a - i != end_b - j:
            raise ValueError(f"{row['id']}: invalid unchanged range {(i,j,end_a,end_b)}")
        while i < end_a:
            if not equal(a[i], b[j]):
                raise ValueError(f"{row['id']}: unexpected unequal unedited lines {(i+1,j+1)}")
            kept.append([i+1, j+1])
            i += 1
            j += 1

    for start_a, start_b, count_a, count_b, body in canonical:
        keep_gap(start_a, start_b)
        for line in body:
            marker, text = line[0], line[1:]
            if marker == ' ':
                if not equal(text, a[i]) or not equal(text, b[j]):
                    raise ValueError(f"{row['id']}: context bytes disagree with input")
                kept.append([i+1, j+1])
                i += 1
                j += 1
            elif marker == '-':
                if text != a[i]:
                    raise ValueError(f"{row['id']}: deleted bytes disagree with input")
                deletes.append(i+1)
                i += 1
            else:
                if text != b[j]:
                    raise ValueError(f"{row['id']}: added bytes disagree with input")
                inserts.append(j+1)
                j += 1
        if (i, j) != (start_a + count_a, start_b + count_b):
            raise ValueError(f"{row['id']}: body range mismatch")
    keep_gap(len(a), len(b))
    return deletes, inserts, kept


def reads(path, cases):
    rows = load_jsonl(path)
    for line, row in enumerate(rows, 1):
        for stream in ('stdout', 'stderr'):
            if digest(encode(row[stream])) != row[f'{stream}_sha256']:
                raise ValueError(f"invalid {stream} fingerprint: {path.name}:{line}")
        scenario = cases[row['case']]
        source_sides = ('b', 'a') if row['direction'] == 'reverse' else ('a', 'b')
        for side, source in zip(('a', 'b'), source_sides, strict=True):
            for receipt_key, expected_key in (('input_sha256', 'lf_sha256'),
                                              ('original_elements_sha256', 'original_elements_sha256')):
                if row[receipt_key][side] != scenario[source][expected_key]:
                    raise ValueError(f"{row['id']}: incorrect {side} input fingerprint")
        row['receipt_ref'] = f'receipts/{path.name}#L{line}'
        row['hunk_bytes'] = row['hunk_normalized'] = None
        row['headers'] = []
        if row['outcome'] == 'run_error':
            continue
        hunks = select_hunks(row['stdout'])
        canon = normalize_hunks(hunks, row['method'])
        row['hunk_bytes'] = ''.join(header + ''.join(body) for header, body in hunks)
        row['hunk_normalized'] = canon
        row['deleted_a'], row['inserted_b'], row['display_kept'] = align(row, scenario, canon)
        row['headers'] = [header.rstrip('\n') for header, _ in hunks]
        if row['matching']:
            a_blocks = row['matching']['blocks_original_0based']
            lf_blocks = row['matching']['blocks_lf_0based']
            if a_blocks != lf_blocks:
                raise ValueError(f"{row['id']}: different original and projected blocks")
            pairs = [[a+offset+1, b+offset+1] for a, b, length in lf_blocks for offset in range(length)]
            if pairs != row['display_kept']:
                raise ValueError(f"{row['id']}: display disagrees with observed matching blocks")
    return rows


def fixture_checks(rows, git_source):
    helper = (git_source/'t/lib-diff-alternative.sh').read_bytes().splitlines(keepends=True)
    fixture = {'R2': b''.join(helper[68:105]), 'R3': b''.join(helper[204:217])}
    checks = defaultdict(list)
    for row in rows:
        tag = (row['case'], row['method'])
        comparison = []
        if tag == ('R1', 'patience'):
            comparison.append(('F01', 'grep', bool(re.search(r'^\+.*X', row['stdout'], re.M)), 'plus line containing X'))
        if tag[0] in ('R2', 'R3') and tag[1] in ('patience', 'histogram'):
            data = fixture[tag[0]]
            expected_sha = digest(data)
            comparison.append(('F02' if tag[0] == 'R2' else 'F04', 'whole hunk bytes',
                               row['hunk_bytes'] == data.decode('utf-8'), expected_sha))
            if tag[0] == 'R2':
                comparison.append(('F03', 'line counts', (len(row['inserted_b']), len(row['deleted_a'])) == (10, 11),
                                   [10, 11]))
        if tag == ('R4', BREEZY):
            actual = row['matching']['r4_original_recurse_pairs_0based']
            expected = [[0, 0], [2, 2], [4, 4]]
            comparison.append(('F05', 'matching pairs original 0-based', actual == expected, expected))
        for assertion, unit, agrees, expected in comparison:
            checks[row['id']].append(
                {'fixture': assertion, 'comparison_unit': unit, 'match': agrees, 'expected_or_digest': expected,
                 'receipt_ref': row['receipt_ref']})
    return checks


def equal_methods(base):
    groups = defaultdict(list)
    for row in base:
        if row['outcome'] != 'run_error':
            groups[row['case'], row['repeat']].append(row)
    ties = defaultdict(lambda: {'full': [], 'hunk_bytes': [], 'hunk_normalized': []})
    for rows in groups.values():
        for r, s in combinations(rows, 2):
            for key, field in [('full', 'stdout'), ('hunk_bytes', 'hunk_bytes'), ('hunk_normalized', 'hunk_normalized')]:
                if r[field] == s[field]:
                    ties[r['id']][key].append(s['method'])
                    ties[s['id']][key].append(r['method'])
    return ties


def write_matrix(path, rows, cases, checks, ties, assessments=None):
    columns = (
        'phase', 'ordinal', 'case', 'method', 'repeat', 'direction', 'context', 'indent', 'extra', 'input_a_sha256',
        'input_b_sha256', 'exit', 'outcome', 'stdout_sha256', 'stderr_sha256', 'hunk_bytes_sha256',
        'hunk_semantic_sha256', 'hunk_headers', 'deleted_a_lines', 'inserted_b_lines', 'display_kept_pairs',
        'engine_matching_blocks_0based', 'full_stdout_tie_methods', 'hunk_bytes_tie_methods',
        'semantic_hunk_tie_methods', 'public_assertion_and_result', 'prediction_210_I_csv_line',
        'prediction_210_I_original', 'prediction_comparison', 'receipt',
    )
    with path.open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns, lineterminator='\n')
        writer.writeheader()
        for row in rows:
            prior = next((p for p in cases[row['case']].get('predictions_210', []) if p['stage'] == 'I-prediction'), {})
            equivalents = ties.get(row['id'], {})
            assessment = (assessments or {}).get((row['case'], row['method']), '미확인')
            units = checks.get(row['id'], []) if row['phase'] == 'base' else []
            hunk = row['hunk_bytes']
            writer.writerow({
                'phase': row['phase'], 'ordinal': row['ordinal'], 'case': row['case'], 'method': row['method'],
                'repeat': row['repeat'], 'direction': row['direction'], 'context': row['context'],
                'indent': '범위 밖' if row['indent'] is None else 'on' if row['indent'] else 'off',
                'extra': compact(row['extra']), 'input_a_sha256': row['input_sha256']['a'],
                'input_b_sha256': row['input_sha256']['b'], 'exit': row['exit_code'], 'outcome': row['outcome'],
                'stdout_sha256': row['stdout_sha256'], 'stderr_sha256': row['stderr_sha256'],
                'hunk_bytes_sha256': digest(encode(hunk)) if hunk is not None else '미확인',
                'hunk_semantic_sha256': digest(encode(compact(row['hunk_normalized']))) if hunk is not None else '미확인',
                'hunk_headers': compact(row['headers']), 'deleted_a_lines': compact(row.get('deleted_a')),
                'inserted_b_lines': compact(row.get('inserted_b')), 'display_kept_pairs': compact(row.get('display_kept')),
                'engine_matching_blocks_0based': compact(row['matching']['blocks_original_0based']) if row['matching'] else '미측정',
                'full_stdout_tie_methods': compact(equivalents.get('full', [])) if row['phase'] == 'base' else '범위 밖',
                'hunk_bytes_tie_methods': compact(equivalents.get('hunk_bytes', [])) if row['phase'] == 'base' else '범위 밖',
                'semantic_hunk_tie_methods': compact(equivalents.get('hunk_normalized', [])) if row['phase'] == 'base' else '범위 밖',
                'public_assertion_and_result': compact([(c['fixture'], c['match']) for c in units]) if units else '해당 공개 단언 없음',
                'prediction_210_I_csv_line': prior.get('source_csv_line', '범위 밖'),
                'prediction_210_I_original': prior.get('anchor_hunk_prediction', '범위 밖'),
                'prediction_comparison': assessment if row['direction'] == 'forward' and row['phase'] == 'base' else '기본 대조와 분리',
                'receipt': row['receipt_ref'],
            })


METHOD_LABELS = {'patience': 'Git patience', 'histogram': 'Git histogram', 'myers': 'Git Myers',
                 BREEZY: 'Breezy Python'}


def primary_table(rows, checks, ties, anchors=None, assessments=None):
    result = [
        '| 입력·방법 | 고정판·입력 지문 | 내부 앵커 또는 미측정 | 실제 hunk·종료 | 원영수증 주소 | 예측과 차이 |',
        '| --- | --- | --- | --- | --- | --- |',
    ]
    for r in rows:
        if r['repeat'] != 1:
            continue
        case, method = r['case'], r['method']
        m = r['matching']
        anchor = (anchors or {}).get((case, method))
        if anchor is None:
            anchor = f"blocks `{compact(m['blocks_original_0based'])}`" if m else '미측정'
        version = '0.2.13' if method == BREEZY else '2.43.0'
        fingerprint = f"`{r['input_sha256']['a'][:10]}…`/`{r['input_sha256']['b'][:10]}…`"
        values = ' · '.join(f'`{h}`' for h in r['headers']) or '0 hunk'
        values += f" · +{len(r['inserted_b'])}/−{len(r['deleted_a'])}, exit {r['exit_code']}"
        counterpart = rows[r['ordinal'] - 1 + 32]
        link = f"[1]({r['receipt_ref']}) · [2]({counterpart['receipt_ref']})"
        units = checks.get(r['id'], [])
        observed = ', '.join(f"{c['fixture']} {'일치' if c['match'] else '불일치'}" for c in units)
        verdict = (assessments or {}).get((case,method), '내부 해석 전')
        equivalence = ties[r['id']]['hunk_normalized']
        tie = ', '.join(METHOD_LABELS[m] for m in equivalence) if equivalence else '0 방법'
        diff = ' · '.join(filter(None, [observed, verdict, f'동률 {tie}']))
        result.append(f'| {case} · {METHOD_LABELS[method]} | {version} {fingerprint} | {anchor} | {values} | {link} | {diff} |')
    result += ['', '표 1의 한 행은 기준 정방향 입력과 방법 한 조합이다. 영수증 두 개는 반복 1·2다. '
               '지문은 A/B LF SHA-256 앞 10자리이며 전체 값은 [inputs.json](inputs.json)에 있다. '
               '표의 앵커와 pre 좌표는 1-based다. 원영수증의 Breezy blocks는 0-based이며 길이 0은 sentinel이다. '
               'Git exit 1은 차이 있음이다. '
               '동률은 같은 입력의 hunk 구간·본문이 일치한 다른 방법이다.', '']
    return '\n'.join(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--git-source', type=Path, required=True)
    parser.add_argument('--receipts', type=Path, default=HERE/'receipts')
    parser.add_argument('--output', type=Path, default=HERE)
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    cases = load_cases()
    base = reads(args.receipts/'base.jsonl', cases)
    controls = reads(args.receipts/'controls.jsonl', cases)
    if len(base) != 64 or len(controls) != 112:
        raise ValueError('incomplete receipt slots')
    checks = fixture_checks(base, args.git_source)
    ties = equal_methods(base)
    anchors, assessments = {}, {}
    rows = base + controls
    if args.final:
        from observe import diagnostic_links
        diagnostics = diagnostic_links(args.receipts, cases)
        for (phase, _), value in diagnostics.items():
            if phase != 'base':
                continue
            diag = value['row']
            trace = value['trace']
            branch = trace['branch']
            root_text = compact(trace['root_selection'])
            pre_text = compact(trace['pre_pairs'])
            if diag['method'] == 'myers':
                evidence = f'{branch}, pre {pre_text}'
            elif trace['root_selection']:
                evidence = f'{branch} {root_text}'
            else:
                evidence = f'{branch}, root 0'
                if trace['pre_pairs']:
                    evidence += f', pre {pre_text}'
            anchors[diag['case'], diag['method']] = f"[{evidence}]({diag['receipt_ref']})"
        with (HERE/'predictions-comparison.csv').open(encoding='utf-8', newline='') as file:
            for item in csv.DictReader(file):
                if item['stage'] != 'I-prediction':
                    continue
                for method, note in json.loads(item['method_comparison_notes_json']).items():
                    assessments[item['case'],method] = note
        cases = challenge_cases(cases)
        rows.extend(reads(args.receipts/'challenges.jsonl', cases))
        rows.extend(value['row'] for value in diagnostics.values())
    write_matrix(args.output/'matrix.csv', rows, cases, checks, ties, assessments)
    save_json(args.output/'receipts/public-crosschecks.json', checks)
    print(primary_table(base, checks, ties, anchors, assessments))


if __name__ == '__main__':
    main()
