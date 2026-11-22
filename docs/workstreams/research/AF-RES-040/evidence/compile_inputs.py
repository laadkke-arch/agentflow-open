"""Normalize the two frozen observer ledgers without changing sampled URLs/order."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent


def jread(path):
    return json.loads(path.read_text())


def emit(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    reqs, candidates, pairs, corrections = [], [], [], []
    files = {}
    for route, letter in [('gdal', 'G'), ('sphinx', 'S')]:
        path = P / 'evidence' / route / ('coding-' + letter + '.json')
        files[str(path.relative_to(P))] = hashlib.sha256(path.read_bytes()).hexdigest()
        data = jread(path)
        reqs.extend(data['requirements'])
        candidates.extend(data['candidates'])
        labels = {'같은 구현·용도': 'same_implementation_use', '대체 가능하나 별도 구현': 'substitutable_distinct_implementation',
                  '같은 프로젝트의 다른 기능': 'same_project_different_function', '상호 보완 증거': 'complementary_evidence', '미확인': 'unknown'}
        for original_pair in data.get('relation_pairs', []):
            pair = dict(original_pair)
            pair['left_id'] = pair.get('left_id', pair.get('left_candidate_id'))
            pair['right_id'] = pair.get('right_id', pair.get('right_candidate_id'))
            pair['original_relation_label'] = pair['relation']
            pair['relation'] = labels.get(pair['relation'], pair['relation'])
            pair['substitution_scope'] = pair.get('substitution_scope', pair.get('direction_scope', '미확인'))
            pair['limitation'] = pair.get('limitation', pair.get('limitations', '미확인'))
            pair['basis_sources'] = pair.get('basis_sources', ';'.join(pair.get('source_ids', [])))
            pair['coding_origin'] = str(path.relative_to(P))
            pairs.append(pair)
        corrections.extend(data.get('correction_log', []))
    # G coding omits empty slots; restore them from the frozen 48-row pool.
    pool = list(csv.DictReader((P / 'pool.csv').open()))
    byid = {c['candidate_id']: c for c in candidates}
    normalized = []
    for row in pool:
        cid = row['candidate_id']
        if row['url']:
            c = dict(byid[cid])
            assert c['url'] == row['url'], ('URL drift', cid)
            assert c['description'] == row['description'], ('card text drift', cid)
            assert int(c['rank']) == int(row['rank']), ('rank drift', cid)
        else:
            c = {'candidate_id': cid, 'case_id': row['case_id'], 'rank': int(row['rank']), 'url': '',
                 'title': '', 'description': '', 'upstream_key': '', 'upstream_verified': False,
                 'implementation': '', 'component': '', 'purpose': '', 'version': '미확인',
                 'identity_verified': False, 'evidence_roles': [], 'atoms': [], 'version_relaxed_atoms': [],
                 'unknowns': ['사전 경로의 후보 부족; 빈 슬롯'], 'document_group': 'empty:' + cid}
        c['source_ids'] = c.get('source_ids', [c['source_id']] if c.get('source_id') else [])
        c['locator'] = c.get('discovery_locator', row.get('discovery_locator', ''))
        c['rank'] = int(c['rank'])
        normalized.append(c)
    for req in reqs:
        req['original_url'] = req.get('original_url', req.get('source_url'))
        req['required_version'] = req.get('required_version', req.get('version', '미확인'))
        req['request_type'] = req.get('request_type', 'contract_required')
    assert len(reqs) == 8 and len(normalized) == 48
    assert len(pairs) == 85, ('nonempty pairs', len(pairs))
    emit(P / 'evidence/analysis-input.json', {
        'schema': 1, 'source': 'manual source-bounded coding, normalized after frozen input commit',
        'pool_remote_sha': 'b406236564be8dc6435912912ba67e5d16c98102',
        'input_files_sha256': files, 'requirements': reqs, 'candidates': normalized,
        'relation_pairs': pairs, 'coding_corrections': corrections,
        'classification_limit': 'internal single observer per route; root spot checks; no human or blind repeated coding'})

    sources = []
    for relative in ['gdal/sources-G.jsonl', 'sphinx/sources-S.jsonl', 'crossfield/sources-X.jsonl', 'root/sources-R.jsonl']:
        for line in (P / 'evidence' / relative).read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                record['observer_ledger'] = 'evidence/' + relative
                sources.append(record)
    needed = {'source_id', 'original_url', 'pinned_url_or_version', 'publisher', 'published_or_event_date',
              'checked_utc', 'locator', 'source_kind', 'verified_fact', 'limitation', 'question_ids',
              'case_ids', 'duplicate_group', 'counted'}
    assert all(needed <= s.keys() for s in sources)
    assert len({s['source_id'] for s in sources}) == len(sources)
    counted_groups = [s['duplicate_group'] for s in sources if s['counted']]
    assert len(set(counted_groups)) == len(counted_groups), 'duplicate counted group'
    (P / 'sources.jsonl').write_text(''.join(json.dumps(s, ensure_ascii=False) + '\n' for s in sources))
    counted = [s for s in sources if s['counted']]
    def category(s):
        k = s['source_kind']
        if k == 'consumer_request': return 'consumer'
        if k in ('supplier_manual', 'supplier_document', 'supplier_doc'): return 'supplier'
        if k.startswith('library_'): return 'library'
        if k.startswith('music_'): return 'music'
        if k in ('identity_source', 'identity_release', 'source_record', 'distribution_record'): return 'identity'
        return 'other'
    categories = Counter(category(s) for s in counted)
    source_ids = {s['source_id'] for s in sources}
    assert all(set(c['source_ids']) <= source_ids for c in normalized)
    facts = {'source_rows': len(sources), 'counted_unique_documents': len(counted),
             'excluded_rows': len(sources) - len(counted), 'exclusive_categories': dict(categories),
             'source_kinds_counted': dict(Counter(s['source_kind'] for s in counted)),
             'pool_slots': len(pool), 'filled_pool_slots': sum(bool(c['url']) for c in normalized),
             'unique_pool_urls': len({c['url'] for c in normalized if c['url']}),
             'fixed_pool_documents': len({c['document_group'] for c in normalized if c['url']}),
             'unique_original_documents_in_pool': len({next(s['duplicate_group'] for s in sources if s['source_id'] == c['source_ids'][0]) for c in normalized if c['url']}),
             'required_atoms': sum(len(r['required_atoms']) for r in reqs),
             'nonempty_relation_pairs': len(pairs),
             'unconfirmed_identity_candidates': sum(not c['identity_verified'] for c in normalized if c['url']),
             'multiple_candidate_versions_within_case': sum(len({c['version'] for c in normalized if c['case_id'] == r['case_id'] and c['url']}) > 1 for r in reqs),
             'minimums': {'consumer': 8, 'supplier': 8, 'identity': 4, 'library': 2, 'music': 2}}
    facts['minimum_source_mix_met'] = all(categories[k] >= v for k, v in facts['minimums'].items())
    emit(P / 'evidence/source-counts.json', facts)
    print(json.dumps(facts, ensure_ascii=False))


if __name__ == '__main__':
    main()
