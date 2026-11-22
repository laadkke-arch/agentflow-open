"""Normalize the three independently recorded frames without altering originals."""
import csv
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def write_lines(path, records):
    path.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in records))


def norm_predicate(p):
    return {
        **p,
        'id': p.get('id', p.get('predicate_id')),
        'predicate': p.get('predicate', p.get('requirement')),
    }


def normalize(q, stream):
    q = dict(q)
    q['id'] = q.get('id', q.get('question_id'))
    q['question_id'] = q['id']
    q['ledger'] = stream
    q['scope'] = q['whole_or_partial']
    q['initial_date'] = q.get('initial_date', q.get('initial_timestamp'))
    q['whole_must'] = [norm_predicate(p) for p in q['whole_must']]
    q['partial_must'] = [norm_predicate(p) for p in q['partial_must']]
    first = q.get('first_text', {})
    q['initial_text_file'] = q.get('initial_text_file', first.get('path'))
    q['initial_text_sha256'] = q.get('initial_text_sha256', first.get('sha256'))
    if not q['initial_text_file']:
        raise ValueError(f"{q['id']}: missing first text path")
    path = REPO / q['initial_text_file']
    if not path.exists():
        path = ROOT / 'streams' / stream / q['initial_text_file']
    if not path.exists():
        raise ValueError(f"{q['id']}: absent original {path}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if q['initial_text_sha256'] and actual != q['initial_text_sha256']:
        raise ValueError(f"{q['id']}: changed original")
    q['initial_text_file'] = str(path.relative_to(REPO))
    q['initial_text_sha256'] = actual
    q['neutral_query'] = q.get('neutral_query', q.get('initial_query'))
    q['a_queries'] = q.get('a_queries', q.get('A_queries'))
    if not q['neutral_query'] or len(q['a_queries']) != 2:
        raise ValueError(f"{q['id']}: need one common and two A queries")
    q['route_order'] = ['A', 'B'] if int(q['id'][1:]) % 2 else ['B', 'A']
    q['stream_original_record'] = f"streams/{stream}/questions.jsonl#{q['id']}"
    return q


def main():
    questions = []
    sources = []
    frames = []
    for stream in ('go', 'python', 'numpy'):
        folder = ROOT / 'streams' / stream
        questions += [normalize(q, stream) for q in lines(folder / 'questions.jsonl')]
        sources += lines(folder / 'sources.jsonl')
        frame_file = folder / 'frame.csv'
        if frame_file.exists():
            with frame_file.open() as f:
                rows = list(csv.DictReader(f))
        elif (folder / 'frame.jsonl').exists():
            rows = lines(folder / 'frame.jsonl')
        else:
            rows = lines(folder / 'metadata-frame.jsonl')
        for row in rows:
            frames.append({'ledger': stream, **row})
    questions.sort(key=lambda q: q['id'])
    assert [q['id'] for q in questions] == [f'Q{i:02}' for i in range(1, 13)]
    for stream in ('go', 'python', 'numpy'):
        group = [q for q in questions if q['ledger'] == stream]
        assert len(group) == 4
        assert sum(q['scope'] == 'whole' for q in group) == 2
        assert sum(q['scope'] == 'partial' for q in group) == 2
        for period in ('2021-2022', '2023-2024'):
            g = [q for q in group if q['period'] == period]
            assert sorted(q['scope'] for q in g) == ['partial', 'whole']
    for q in questions:
        for kind in ('whole_must', 'partial_must'):
            assert q[kind], (q['id'], kind)
            for p in q[kind]:
                assert p['id'] and p['predicate'] and p.get('falsifying_input'), (q['id'], p)
    write_lines(ROOT / 'questions.jsonl', questions)
    write_lines(ROOT / 'sources-initial.jsonl', sources)
    columns = ['ledger', 'canonical_id', 'title', 'period', 'selected_question_id',
               'first_public_date', 'period_order', 'sha256_order_key', 'details']
    selected = {(q['ledger'], q['canonical_id']): q['id'] for q in questions}
    with (ROOT / 'frame.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in frames:
            cid = row.get('canonical_id', row.get('id', ''))
            writer.writerow({
                'ledger': row['ledger'], 'canonical_id': cid,
                'title': row.get('title', ''), 'period': row.get('period', ''),
                'selected_question_id': selected.get((row['ledger'], cid), ''),
                'first_public_date': row.get('first_public_date', row.get('initial_date', row.get('created', ''))),
                'period_order': row.get('period_order', row.get('order', row.get('rank', ''))),
                'sha256_order_key': row.get('sha256_order_key', row.get('sampling_hash', row.get('hash', ''))),
                'details': json.dumps(row, ensure_ascii=False, separators=(',', ':')),
            })
    summary = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'questions': len(questions), 'frame_rows': len(frames),
        'whole': sum(q['scope'] == 'whole' for q in questions),
        'partial': sum(q['scope'] == 'partial' for q in questions),
        'whole_predicates': sum(len(q['whole_must']) for q in questions),
        'partial_predicates': sum(len(q['partial_must']) for q in questions),
        'initial_source_rows': len(sources),
        'queries': {'common': 12, 'A_additional': 24},
        'source_bytes_not_changed': True,
        'normalization': 'field aliases and deterministic aggregation only; original per-stream records retained',
    }
    (ROOT / 'evidence/input-assembly.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
