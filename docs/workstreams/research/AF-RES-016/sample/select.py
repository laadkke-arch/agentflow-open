#!/usr/bin/env python3
"""Recreate the frozen sample from exact Git objects; no network or model calls."""
import csv
import hashlib
import io
import json
from pathlib import Path
import random
import subprocess
from collections import Counter

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SEED = 2026112016
SHAS = {
    '001': '4d6208c08f6f2657865ba000d6768f6537e832b6',
    '002': '62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1',
    '003': 'b13db3931b4021ff9e1ac6e404590c09526c3087',
    '004': '2b798c7d2b7355b649691c18de196104ceabb0f0',
    '010': '0603f0d2990c7a501dbdfc45fbbba79155f505fc',
    '011': '478c301b693896e2c6d777f46ac441f071bfdfe8',
    '012': 'cb602858378db90adb1f085953016267f9afbd6d',
}
inputs = []


def read(task, name):
    path = f'docs/workstreams/research/AF-RES-{task}/{name}'
    data = subprocess.check_output(['git', 'show', f'{SHAS[task]}:{path}'], cwd=ROOT)
    inputs.append({'task': task, 'sha': SHAS[task], 'path': path,
                   'sha256': hashlib.sha256(data).hexdigest()})
    return data.decode()


def jread(task, name):
    return json.loads(read(task, name))


def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def uniq_text(parts):
    return ' / '.join(dict.fromkeys(p for p in parts if isinstance(p, str) and p))


def main():
    a = {x['id']: x for x in jread('011', 'evidence/reliability-original.json')['cases']}
    b = {x['id']: x for x in jread('011', 'evidence/reliability-blind.json')['cases']}
    jread('011', 'evidence/reliability-selection.json')
    final_cases = jread('011', 'CASES.json')
    mappings = jread('011', 'evidence/reliability-comparison-draft.json')['answers']['mapping']
    mappings = sorted(mappings, key=lambda x: (x['case_id'], x['original_index']))
    baseline, all_units = [], []
    for m in mappings:
        c = a[m['case_id']]
        aa = c['answers'][m['original_index']]
        bb = b[c['id']]['answers'][m['blind_index']]
        uid = f"011-{c['id']}-{m['original_index']+1:03d}"
        baseline.append({'unit_id': uid, 'cluster': c['id'], 'original_index': m['original_index'],
                         'blind_index': m['blind_index'], 'a': aa['role'], 'b': bb['role'],
                         'equal': aa['role'] == bb['role']})
        ev = bb.get('evidence', {})
        all_units.append({
            'unit_id': uid, 'sample': '011', 'cluster': c['id'],
            'candidate': aa.get('candidate') or aa.get('summary') or m['original_summary'],
            'candidate_description': uniq_text([aa.get('summary'), m.get('blind_summary'), ev.get('summary')]),
            'problem': c['question_summary'], 'constraints': c.get('constraints', []),
            'proposal': '기존 답이 이 문제에 제안한 후보 또는 방법. 세부 사용은 candidate_description 범위에서만 판단.',
            'configuration': '',
            'source': {'task_sha': SHAS['011'], 'path': 'evidence/reliability-original.json',
                       'case_id': c['id'], 'answer_index': m['original_index'],
                       'url': m['source_url'], 'locator': ev.get('locator', m['original_locator'])},
            'packet_limit': '고정된 원판 및 별도 코딩의 내용 요약만. 기존 역할·형식·반응·판정 필드는 제거.'
        })
    assert len(baseline) == 149 and sum(x['equal'] for x in baseline) == 75
    tail = [x for x in all_units if x['cluster'] == 'T047']
    rest = [x for x in all_units if x['cluster'] != 'T047']
    assert len(tail) == 66 and len(rest) == 83
    units = sorted(rest + random.Random(SEED).sample(tail, 37), key=lambda x: x['unit_id'])
    entries = sorted([json.loads(x) for x in read('012', 'corpus/entries.jsonl').splitlines() if x], key=lambda x: x['id'])
    queries = {x['id']: x for x in (json.loads(s) for s in read('012', 'queries/queries.jsonl').splitlines() if s)}
    qrels = list(csv.DictReader(io.StringIO(read('012', 'qrels/qrels.tsv')), delimiter='\t'))
    independent = list(csv.DictReader(io.StringIO(read('012', 'qrels/independent.tsv')), delimiter='\t'))
    picked = sorted(random.Random(SEED).sample(entries, 60), key=lambda x: x['id'])
    rngq = random.Random(SEED + 12)
    baseline012 = []
    for e in picked:
        qs = sorted({r['query_id'] for r in qrels if r['entry_id'] == e['id']})
        fallback = not qs
        qid = rngq.choice(qs or sorted(queries))
        q = queries[qid]
        uid = f"012-{e['id']}"
        units.append({'unit_id': uid, 'sample': '012', 'cluster': qid,
                      'candidate': e['name'],
                      'candidate_description': uniq_text([e['D-a']['ko'], e['D-b']['ko'], e['D-c']['ko']]),
                      'problem': q['ko'], 'constraints': [], 'proposal': '', 'configuration': '',
                      'source': {'task_sha': SHAS['012'], 'path': 'corpus/entries.jsonl', 'entry_id': e['id'],
                                 'query_id': qid, 'url': e['url']},
                      'packet_limit': 'D-a/b/c는 선행 연구자의 설명이며 역할·관련성 등급·질의 whole/part 메타라벨 제거.'})
        baseline012.append({'unit_id': uid, 'role': e['role'], 'query_id': qid, 'fallback_query': fallback,
                            'qrels': [r for r in qrels if r['entry_id'] == e['id'] and r['query_id'] == qid],
                            'independent': [r for r in independent if r['entry_id'] == e['id'] and r['query_id'] == qid]})
    cases = jread('004', 'CASES.json')
    expected = jread('004', 'EXPECTED.json')
    problems = {p['id']: p for p in cases['problems']}
    source_catalog = {s['id']: s for s in cases['source_catalog']}
    for row in cases['rows']:
        problem_key = row['problem_id']
        if problem_key not in problems:
            problem_key = next(v['base_problem_id'] for v in cases['controlled_variants'] if v['variant_row_id'] == row['row_id'])
        p = json.loads(json.dumps(problems[problem_key]))
        for v in cases.get('controlled_variants', []):
            if v['variant_row_id'] == row['row_id']:
                for h in p['hard_requirements']:
                    if h['id'] == v['changed_requirement_id']:
                        h['text'] = v['replacement']
                # The variant overrides the corresponding base given too; do
                # not hand the coders mutually contradictory idempotency facts.
                p['given'] = p['given'].replace(
                    'handler는 동일 ID의 결과를 중복 반영하지 않는 영속 멱등 처리를 이미 갖고 있다.',
                    '이 변형에서는 다음 P02-H3가 기본 handler 멱등성 given을 대체한다: ' + v['replacement'])
        units.append({'unit_id': '004-' + row['row_id'], 'sample': '004', 'cluster': problem_key,
                      'candidate': row['candidate'], 'candidate_description': row.get('use_scope', ''),
                      'problem': p['goal'] + '\n선택 범위: ' + p['target_part'] + '\ngiven: ' + p['given'] + '\n범위 밖: ' + p['out_of_scope'],
                      'constraints': p['hard_requirements'], 'proposal': row['proposal'],
                      'configuration': row['configuration'],
                      'source': {'task_sha': SHAS['004'], 'path': 'CASES.json', 'row_id': row['row_id'],
                                 'urls': [source_catalog[s]['url'] for s in row['source_ids']]},
                      'packet_limit': '합성 문제와 사용 제안. proposed_role 및 EXPECTED 판정은 제거. R18 요구 변형 적용.'})
    units.sort(key=lambda x: (x['sample'], x['unit_id']))
    assert Counter(x['sample'] for x in units) == {'011': 120, '012': 60, '004': 18}
    assert len({x['unit_id'] for x in units}) == 198
    selected = {x['unit_id'] for x in units}
    write('units.json', {'study': 'AF-RES-016', 'version': '1.0', 'label_blind_packet': True,
                         'coding_inputs': 'CODEBOOK.md and this file only', 'units': units})
    write('baseline.json', {'warning': 'NOT FOR CODER B. Historical labels only; never new coding truth.',
                            '011_all': baseline, '011_selected': [x for x in baseline if x['unit_id'] in selected],
                            '012_selected': baseline012, '004_expected': expected['rows']})
    write('selection.json', {'seed': SEED, 'query_seed': SEED + 12, 'algorithm': 'SCOPE.md §2; Python random.Random',
                             'inputs': inputs, 'source_commits': SHAS,
                             'counts': dict(Counter(x['sample'] for x in units)),
                             'clusters': {s: dict(Counter(x['cluster'] for x in units if x['sample'] == s)) for s in ['011', '012', '004']},
                             '011_original_agreement': {'agree': 75, 'n': 149},
                             '011_selected_original_agreement': {'agree': sum(x['equal'] for x in baseline if x['unit_id'] in selected), 'n': 120},
                             '012_population_n': len(entries), '012_selected_unique_entries': 60,
                             'selected_unit_ids': [x['unit_id'] for x in units],
                             'excluded_011_pairs': [x['unit_id'] for x in all_units if x['unit_id'] not in selected]})
    md = ['# 표본 목록', '', '선정은 sample/select.py, seed=2026112016. 과거 라벨은 baseline.json에 격리했다.', '',
          '| 단위 ID | 표본 | cluster | 후보/내용 요약 |', '|---|---|---|---|']
    for u in units:
        md.append('| ' + ' | '.join([u['unit_id'], u['sample'], u['cluster'], u['candidate'].replace('|', '/')]) + ' |')
    (OUT / 'LIST.md').write_text('\n'.join(md) + '\n')
    print(json.dumps({'units': len(units), 'counts': dict(Counter(x['sample'] for x in units)),
                      'old149': sum(x['equal'] for x in baseline),
                      'old120': sum(x['equal'] for x in baseline if x['unit_id'] in selected)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
