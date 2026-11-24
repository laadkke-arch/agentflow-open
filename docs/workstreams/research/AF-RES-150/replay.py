"""Offline replay of the AF-RES-150 catalog observations."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sqlite3
from collections import Counter, defaultdict


QUESTIONS = ('F', 'L', 'T', 'A')
MISSING = 'MISSING'
HOLD = 'HOLD'
NONE = 'NONE'
MODEL_NAMES = ('A', 'B', 'C')
ABLATIONS = ('pin', 'route', 'alias', 'scope', 'authority', 'available', 'cancel')
CONTROL_ALTERNATES = {'C01.2', 'C02.2', 'C03.2', 'C04.2'}
FAULT_DAYS = ('9999-01-01', '9999-01-02')
HERE = Path(__file__).resolve().parent


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(packed(value).encode()).hexdigest()


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


def answer(value, *proof):
    return value, tuple(sorted(set(filter(None, proof))))


def time_key(event):
    return event['valid'], event.get('available', event['valid']), event['id']


def visible(event, cutoff):
    return event['valid'] <= cutoff and event.get('available', event['valid']) <= cutoff


def actor_answer(notes, unknown, proof):
    authorities = sorted({note['authority'] for note in notes if note.get('authority')})
    if authorities:
        return answer(' | '.join(authorities), *(note['proof'] for note in notes if note.get('authority')))
    if unknown:
        return answer(HOLD, *proof)
    return answer(NONE)


def recorded_answer(document, question):
    if document is None or not document['direct']:
        return answer(MISSING)
    if question == 'F':
        return answer(document['url'] + ' @ ' + document['pin'], document['proof']) if document.get('pin') else answer(MISSING)
    if question == 'T':
        return answer(document['feature'], document['proof']) if document.get('feature') else answer(MISSING)
    return answer(document['url'], document['proof'])


class InterruptedWrite(Exception):
    """Simulated interruption inside an uncommitted SQLite transaction."""


class Store:
    def __init__(self, path, model, ablation=''):
        self.path = path
        self.model = model
        self.ablation = ablation
        self.stats = defaultdict(Counter)
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE observations (case_id TEXT, item_key TEXT, body TEXT, '
                        'PRIMARY KEY (case_id, item_key)) WITHOUT ROWID')
        self.db.commit()

    def reopen(self):
        self.db.close()
        self.db = sqlite3.connect(self.path)

    def rows(self, case_id):
        rows = self.db.execute('SELECT body FROM observations WHERE case_id=? ORDER BY item_key', (case_id,))
        return [json.loads(body) for (body,) in rows]

    def put(self, case_id, key, row, *, replace=False):
        body = packed(row)
        if replace:
            self.db.execute('INSERT OR REPLACE INTO observations VALUES (?, ?, ?)', (case_id, key, body))
            return
        old = self.db.execute('SELECT body FROM observations WHERE case_id=? AND item_key=?', (case_id, key)).fetchone()
        if old is not None and old[0] != body:
            raise ValueError(f'event ID reused with different body: {case_id} {key}')
        self.db.execute('INSERT OR IGNORE INTO observations VALUES (?, ?, ?)', (case_id, key, body))

    def accept(self, case_id, event):
        if self.ablation == 'alternate' and event['id'] in CONTROL_ALTERNATES:
            return
        if self.model == 'C':
            if self.ablation == 'alias' and event['id'] == 'N06.4':
                return
            if self.ablation == 'cancel' and event.get('kind') == 'cancel':
                return
            row = dict(event)
            if self.ablation == 'route' and event['id'] == 'N05.3':
                row.update(kind='notice')
                del row['right'], row['scope']
            if self.ablation in {'pin', 'scope', 'authority', 'available'}:
                row.pop(self.ablation, None)
            self.put(case_id, event['id'], row)
            return

        if event['op'] == 'doc':
            columns = ('id', 'op', 'url', 'pin', 'feature', 'direct', 'proof')
            if self.model == 'A':
                row = {key: event[key] for key in columns}
                self.put(case_id, row['url'], row, replace=True)
            else:
                self.put(case_id, event['id'], dict(event))
            return

        docs = {row['id']: row for row in self.rows(case_id) if row['op'] == 'doc'}
        left = docs.get(event['left'])
        if left is None:
            return
        if self.model == 'A':
            right = docs.get(event['right'])
            if right and event['kind'] == 'alias' and event['transport']:
                row = dict(left, current_url=right['url'], current_proof=right['proof'],
                           transport_proof=event['proof'])
                self.put(case_id, row['url'], row, replace=True)
            return

        if event.get('authority') or event['kind'] in {'dispute', 'hold'}:
            notice = {key: event[key] for key in ('id', 'op', 'available', 'valid', 'proof', 'authority')}
            notice.update(group=left['group'], warning=event['kind'] in {'dispute', 'hold'})
            self.put(case_id, event['id'], notice)

    def deliver(self, case_id, events, *, interrupt=False):
        stats = self.stats[case_id]
        start = self.db.total_changes
        correction_writes = 0
        try:
            with self.db:
                for position, event in enumerate(events):
                    stats['attempts'] += 1
                    stats['correction_deliveries'] += int(event.get('correction', False))
                    before = self.db.total_changes
                    self.accept(case_id, event)
                    if event.get('correction'):
                        correction_writes += self.db.total_changes - before
                    if interrupt and position == 0:
                        raise InterruptedWrite
        except InterruptedWrite:
            stats['rollback_batches'] += 1
            stats['aborted_rows'] += self.db.total_changes - start
            return False
        stats['committed_writes'] += self.db.total_changes - start
        stats['correction_writes'] += correction_writes
        return True

    def view(self, case_id, cutoff):
        rows = self.rows(case_id)
        if self.model != 'A':
            rows = [row for row in rows if visible(row, cutoff)]
        documents = [row for row in rows if row['op'] == 'doc']
        edges = [row for row in rows if row['op'] == 'edge']
        if self.model == 'C':
            cancelled = {row['retracts'] for row in edges if row['kind'] == 'cancel'}
            edges = [row for row in edges if row['id'] not in cancelled and row['kind'] != 'cancel']
        return documents, edges

    def query(self, case_id, ref, question, cutoff):
        docs, edges = self.view(case_id, cutoff)
        if self.model == 'A':
            anchor = next((row for row in docs if row['url'] == ref['url']), None)
            if anchor is None or not anchor['direct']:
                return answer(MISSING)
            if question == 'A':
                return answer(NONE)
            if question == 'L' and anchor.get('current_url'):
                return answer(anchor['current_url'], anchor['current_proof'], anchor['transport_proof'])
            return recorded_answer(anchor, question)

        by_id = {row['id']: row for row in docs}
        anchor = by_id.get(ref['id'])
        if anchor is None:
            return answer(MISSING)
        if question in {'F', 'T'}:
            return recorded_answer(anchor, question)
        if self.model == 'B':
            group = [row for row in docs if row['group'] == anchor['group'] and row['direct']]
            notices = [row for row in edges if row['group'] == anchor['group']]
            warnings = [row for row in notices if row['warning']]
            if question == 'A':
                return actor_answer(notices, bool(warnings), (row['proof'] for row in warnings))
            if warnings:
                return answer(HOLD, *(row['proof'] for row in notices))
            if not group:
                return answer(MISSING)
            latest = max(group, key=time_key)
            if anchor['direct'] and latest['pin'] == anchor['pin']:
                return recorded_answer(anchor, 'L')
            return recorded_answer(latest, 'L')

        own_edges = [row for row in edges if row['left'] == anchor['id']]
        warnings = [row for row in own_edges if row['kind'] in {'dispute', 'hold', 'block'}]
        if question == 'A':
            return actor_answer(own_edges, bool(warnings), (row['proof'] for row in warnings))
        return self.read_location(anchor, by_id, edges)

    @staticmethod
    def read_location(anchor, documents, edges):
        point = anchor
        visited = set()
        proofs = []
        while point['id'] not in visited:
            visited.add(point['id'])
            outgoing = [row for row in edges if row['left'] == point['id']]
            if any(row['kind'] in {'dispute', 'hold', 'block'} for row in outgoing):
                return answer(HOLD, *proofs, *(row['proof'] for row in outgoing))
            candidates = [
                row for row in outgoing
                if (row['kind'] == 'route' or (row['kind'] == 'alias' and row['transport']))
                and row.get('scope') in {None, anchor['focus']}
                and row['right'] in documents
            ]
            if not candidates:
                if not point['direct']:
                    return answer(MISSING)
                return answer(point['url'], point['proof'], *proofs)
            latest = max(candidates, key=time_key)
            proofs.append(latest['proof'])
            point = documents[latest['right']]
        return answer(HOLD, *proofs)

    def pair(self, case_id, left, right, cutoff):
        docs, edges = self.view(case_id, cutoff)
        if self.model == 'A':
            by_url = {row['url']: row for row in docs}
            left_doc, right_doc = by_url.get(left['url']), by_url.get(right['url'])
            value = 'same' if left['url'] == right['url'] else 'distinct'
            extras = []
        else:
            by_id = {row['id']: row for row in docs}
            left_doc, right_doc = by_id.get(left['id']), by_id.get(right['id'])
            if self.model == 'B':
                value = 'same' if left_doc and right_doc and left_doc['group'] == right_doc['group'] else 'distinct'
                groups = {d['group'] for d in (left_doc, right_doc) if d}
                extras = [row['proof'] for row in edges if row['group'] in groups]
            else:
                references = {left['id'], right['id']}
                relationships = [row for row in edges if {row['left'], row.get('right')} == references]
                choices = [row for row in relationships if row['kind'] in {'alias', 'block'}]
                latest = max(choices, key=time_key) if choices else None
                value = 'same' if latest and latest['kind'] == 'alias' else 'distinct'
                extras = [row['proof'] for row in relationships]
        if left_doc is None or right_doc is None:
            return answer(MISSING)
        return answer(value, left_doc['proof'], right_doc['proof'], *extras)

    def costs(self, case_ids):
        records = self.db.execute('SELECT case_id, item_key, body FROM observations').fetchall()
        counts = defaultdict(Counter)
        for case_id, key, body in records:
            counts[case_id]['retained_rows'] += 1
            counts[case_id]['logical_bytes'] += sum(len(part.encode()) for part in (case_id, key, body))
        self.db.close()
        totals = self.empty_cost()
        details = []
        for case_id in sorted(case_ids):
            values = {**self.empty_cost(), **self.stats[case_id], **counts[case_id]}
            details.append(dict(case_id=case_id, sqlite_bytes='', **values))
            for field in totals:
                totals[field] += values[field]
        return [dict(case_id='ALL', sqlite_bytes=self.path.stat().st_size, **totals), *details]

    @staticmethod
    def empty_cost():
        return dict(attempts=0, correction_deliveries=0, committed_writes=0, correction_writes=0,
                    rollback_batches=0, aborted_rows=0, retained_rows=0, logical_bytes=0)


def verdict(expected, actual, mode):
    value, proof = actual
    if expected['value'] == MISSING:
        return 'unverified' if value == MISSING else 'unsupported'
    if value != expected['value']:
        if value == MISSING:
            return 'evidence_loss'
        if expected['value'] == HOLD:
            return 'unsupported'
        if mode == 'P' and value in {'same', 'distinct'}:
            return 'overmerge' if value == 'same' else 'oversplit'
        return 'wrong'
    if not set(expected['proof']).issubset(proof):
        return 'evidence_loss'
    return 'justified_hold' if value == HOLD else 'match'


def answer_row(case, model, scenario, checkpoint, question, cutoff, expectation, actual, events, urls):
    case_id = case['case_id']
    value, proof = actual
    return dict(scenario=scenario, model=model, case_id=case_id, checkpoint=checkpoint,
                row_id=f'{scenario}/{model}/{case_id}/{checkpoint}/{question}', query_id=question, cutoff=cutoff,
                expected=expectation['value'], actual=value, expected_sources=' '.join(expectation['proof']),
                actual_sources=' '.join(proof), expected_urls=packed([urls[s] for s in expectation['proof']]),
                actual_urls=packed([urls[s] for s in proof]), verdict=verdict(expectation, actual, question),
                delivered=' '.join(event['id'] for event in events))


def stage(store, case, scenario, name, cutoff, events, expected, questions, urls, *, pairs=False, anchor=None):
    docs = {row['id']: row for row in case['observations'] if row['op'] == 'doc'}
    anchor = docs[anchor or case['anchors']['original']]
    case_id = case['case_id']
    rows = [
        answer_row(case, store.model, scenario, name, q, cutoff, expected[q],
                   store.query(case_id, anchor, q, cutoff), events, urls)
        for q in questions
    ]
    if pairs:
        for pair in case['pairs']:
            actual = store.pair(case_id, docs[pair['left']], docs[pair['right']], cutoff)
            rows.append(answer_row(case, store.model, scenario, name, 'P', cutoff,
                                   pair['expected'], actual, events, urls))
    return rows


def fault_events(case):
    case_id = case['case_id']
    pair = case['pairs'][0]
    if case_id not in {'N04', 'N06'}:
        return []
    old, new = FAULT_DAYS
    base = dict(op='edge', left=pair['left'], right=pair['right'], authority=None, scope=None, correction=True)
    fault = dict(base, id=case_id+'.X1', kind='alias' if case_id == 'N04' else 'block',
                 transport=case_id == 'N04', available=old, valid=old, proof='X01')
    repair = dict(base, id=case_id+'.X2', kind='cancel', transport=False, retracts=fault['id'],
                  available=new, valid=new, proof='X02')
    return [fault, repair]


def reverse_edges(events):
    others = iter(reversed([event for event in events if event['op'] == 'edge']))
    return [next(others) if event['op'] == 'edge' else event for event in events]


def replay_case(store, case, scenario, questions, urls):
    case_id = case['case_id']
    pre, post = (case['checkpoints'][key] for key in ('pre', 'post'))
    original = case['anchors']['original']
    events = case['observations']
    early = [event for event in events if visible(event, pre)]
    if case['kind'] == 'stable':
        early = [event for event in early if event['id'] == original]
    late = [event for event in events if event not in early]
    store.deliver(case_id, early)
    result = stage(store, case, scenario, 'pre', pre, early, case['expected']['pre'], questions, urls)
    probes = case.get('probes', {})
    middle = probes.get('pre-announcement')
    if middle:
        arrived = [event for event in late if visible(event, middle['cutoff'])]
        store.deliver(case_id, arrived)
        early = early + arrived
        late = [event for event in late if event not in arrived]
        result.extend(stage(store, case, scenario, 'pre-announcement', middle['cutoff'], early,
                            middle['expected'], questions, urls))
    if scenario == 'reverse':
        late = reverse_edges(late)

    if scenario == 'interrupt' and case_id == 'N12':
        before = digest(store.rows(case_id))
        if store.deliver(case_id, late, interrupt=True):
            raise AssertionError('fault did not interrupt transaction')
        store.reopen()
        if before != digest(store.rows(case_id)):
            raise AssertionError('interrupted batch changed committed rows')
        result.extend(stage(store, case, scenario, 'interrupted', pre, early, case['expected']['pre'], questions, urls))

    store.deliver(case_id, late)
    received = early + late
    if scenario == 'duplicate':
        store.deliver(case_id, received)
        received += received

    result.extend(stage(store, case, scenario, 'post', post, received, case['expected']['post'], questions, urls, pairs=True))
    result.extend(stage(store, case, scenario, 'lookback', pre, received, case['expected']['pre'], questions, urls))
    if middle:
        result.extend(stage(store, case, scenario, 'announcement-lookback', middle['cutoff'], received,
                            middle['expected'], questions, urls))
    follow = probes.get('new-citation')
    if follow:
        result.extend(stage(store, case, scenario, 'new-citation', post, received, follow['expected'], questions,
                            urls, anchor=follow['anchor']))
    if scenario in {'bad-link', 'without-cancel'}:
        for event, checkpoint in zip(fault_events(case), ('injected', 'repaired')):
            store.deliver(case_id, [event])
            received = received + [event]
            result.extend(stage(store, case, scenario, checkpoint, event['valid'], received,
                                case['expected']['post'], questions, urls, pairs=True))
    return result


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def run(args):
    if args.out.exists() and any(args.out.iterdir()):
        raise SystemExit('output directory must be empty')
    args.out.mkdir(parents=True, exist_ok=True)
    cases = read_jsonl(args.cases)
    sources = read_jsonl(args.sources)
    urls = {row['source_id']: row['url'] for row in sources}
    urls.update(X01='[구성] 잘못 전달된 동일/분리 판단', X02='[구성] 그 판단만 취소')
    questions = tuple(reversed(QUESTIONS)) if args.reverse_queries else QUESTIONS
    scenarios = [('normal', name, '') for name in MODEL_NAMES]
    if args.suite == 'full':
        scenarios += [(scenario, name, '') for scenario in ('duplicate', 'reverse', 'interrupt', 'bad-link') for name in MODEL_NAMES]
        scenarios += [(f'without-{field}', 'C', field) for field in ABLATIONS]
        scenarios.append(('single-address', 'A', 'alternate'))
    answers, costs = [], []
    for scenario, name, field in scenarios:
        store = Store(args.out / f'{scenario}-{name}.sqlite3', name, field)
        for case in cases:
            answers.extend(replay_case(store, case, scenario, questions, urls))
        costs.extend(dict(scenario=scenario, model=name, **record) for record in store.costs([case['case_id'] for case in cases]))
    answers.sort(key=lambda row: row['row_id'])
    costs.sort(key=lambda row: (row['scenario'], row['model'], row['case_id']))
    write_csv(args.out / 'answers.csv', answers)
    write_csv(args.out / 'costs.csv', costs)
    print(f"{len(cases)} cases | {len(scenarios)} SQLite databases | {len(answers)} answers | {len(costs)} cost rows")
    print('answers sha256', hashlib.sha256((args.out / 'answers.csv').read_bytes()).hexdigest())
    print('costs sha256  ', hashlib.sha256((args.out / 'costs.csv').read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, default=HERE / 'cases.jsonl')
    parser.add_argument('--sources', type=Path, default=HERE / 'sources.jsonl')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--suite', choices=('main', 'full'), default='full')
    parser.add_argument('--reverse-queries', action='store_true')
    run(parser.parse_args())


if __name__ == '__main__':
    main()
