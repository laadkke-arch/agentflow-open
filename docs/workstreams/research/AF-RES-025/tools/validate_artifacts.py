#!/usr/bin/env python3
"""Validate the experiment's denominators and auditable limits, not its thesis."""
import csv
import datetime as dt
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]


def jl(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]


def parse_time(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def check(result, condition, evidence):
    checks.append({'passed': bool(result), 'condition': condition, 'evidence': evidence})


checks = []
questions = {r['id']: r for r in jl(BASE / 'questions.jsonl')}
queries = jl(BASE / 'queries.jsonl')
search = list(csv.DictReader((BASE / 'search-log.csv').open()))
raw = jl(BASE / 'returns-raw.jsonl')
strict = jl(BASE / 'returns.jsonl')
sources = json.loads((BASE / 'sources.json').read_text())
reviews = [r for p in sorted((BASE / 'reviews').glob('*/reviews.jsonl')) for r in jl(p)]
packets = {r['blind_key']: r for r in jl(BASE / 'blind/packets.jsonl')}
scored = jl(BASE / 'evidence/scored-slots.jsonl')

check(set(questions) == {f'Q{i:02}' for i in range(1, 13)}, '12 fixed question IDs', 'questions.jsonl')
check(Counter(r['scope'] for r in questions.values()) == {'part': 6, 'whole': 6}, 'six whole and six part questions', 'questions.jsonl scope')
check(Counter(r.get('stream') for r in questions.values()) == {'arrow': 4, 'cargo': 4, 'jupyter': 4}, 'three ledgers, cap four each', 'questions.jsonl stream')
check(len(queries) == 24, '24 frozen routes', 'queries.jsonl')
check(len([r for r in search if r['event_type'] == 'search_request']) == 72, '72 actual search requests', 'search-log.csv')
check(len(raw) == len(strict) == 72, '72 slots in each preserved return format', 'returns-raw.jsonl; returns.jsonl')

for qid, q in sorted(questions.items()):
    path = ROOT / q['input_path']
    check(path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == q['input_sha256'], f'{qid} exact complete input hash', q['input_path'])
    pair = [r for r in queries if r['question_id'] == qid]
    check(len(pair) == 2 and {r['route'] for r in pair} == {'G', 'R'}, f'{qid} paired routes', 'queries.jsonl')
    check(len({r['input_sha256'] for r in pair}) == 1, f'{qid} byte-identical G/R input', 'queries.jsonl input_sha256')
    for field in ['engine', 'response_length', 'language', 'model', 'site_scope']:
        check(len({r[field] for r in pair}) == 1, f'{qid} same {field}', 'queries.jsonl')
    for route in ('G', 'R'):
        frozen = next(r for r in pair if r['route'] == route)
        actual = sorted((r for r in search if r['question_id'] == qid and r['route'] == route and r['event_type'] == 'search_request'), key=lambda r: int(r['query_index']))
        check([r['query'] for r in actual] == frozen['query_strings'], f'{qid}-{route} exact frozen query replay', 'queries.jsonl + search-log.csv')
        check(len(actual) <= 3, f'{qid}-{route} query budget', 'search-log.csv')
        opens = [r for r in search if r['question_id'] == qid and r['route'] == route and r['event_type'] == 'open_attempt']
        check(len(opens) <= 5, f'{qid}-{route} first open attempt budget includes failures', 'search-log.csv')
        retry = Counter(r['url'] for r in search if r['question_id'] == qid and r['route'] == route and r['event_type'] == 'retry')
        check(all(n <= 1 for n in retry.values()), f'{qid}-{route} at most one same URL retry', 'search-log.csv')
        for name, rows in [('raw', raw), ('strict', strict)]:
            slots = [r for r in rows if r['question_id'] == qid and r['route'] == route]
            check(sorted(r['rank'] for r in slots) == [1, 2, 3], f'{qid}-{route} {name} original three ranks retained', name + ' returns')
        ss = [r for r in strict if r['question_id'] == qid and r['route'] == route]
        urls = {urldefrag(c['url'])[0] for r in ss for c in r.get('returned_citations', []) if c.get('url')}
        check(len(urls) <= 3, f'{qid}-{route} strict final three source URL format', 'returns.jsonl')
        rr = {(r['question_id'], r['route'], r['rank']): r for r in raw}
        for row in ss:
            original = rr[(qid, route, row['rank'])]
            check(all(c in original.get('returned_citations', []) for c in row['returned_citations']), f'{qid}-{route}-{row["rank"]} no new or repaired citation in strict view', 'returns.jsonl')
            check(row.get('original_candidate_id') == original.get('candidate_id'), f'{qid}-{route}-{row["rank"]} no reranking in strict view', 'returns.jsonl')
    expected = 'G' if int(qid[1:]) % 2 else 'R'
    requests = sorted((r for r in search if r['question_id'] == qid and r['event_type'] == 'search_request'), key=lambda r: r['request_utc'])
    check(requests[0]['route'] == expected, f'{qid} odd/even execution order', 'search-log.csv request_utc')

# Local frozen input hashes are checked against remote seal receipts, not a claim
# that repository draft dates equal the search date.
q08 = [r for r in search if r['question_id'] == 'Q08' and r['event_type'] == 'search_request']
check(all(parse_time(r['request_utc']) > parse_time('2026-11-22T05:15:27Z') for r in q08), 'Q08 all searches after remote amendment confirmation', 'evidence/input-amendment-Q08.json; search-log.csv')
search_rows = [r for r in search if r['event_type'] == 'search_result']
selected_over = [r for r in search_rows if int(r['observed_rank']) > 10 and r['disposition'] in ('selected_open', 'opened', 'opened_failed_404', 'opened_failed_empty', 'opened_rewritten_summary', 'opened_same_lineage')]
check(not selected_over, 'no candidate selected from ranks above first ten supplied', [r['event_id'] for r in selected_over])
check(len(search_rows) == 633 and sum(int(r['observed_rank']) <= 10 for r in search_rows) == 616, 'raw result and eligible result denominators', 'search-log.csv')

check(len(reviews) == len(packets) == 93 and {r['blind_key'] for r in reviews} == set(packets), 'all masked union candidate keys read', 'blind/packets.jsonl; reviews/*/reviews.jsonl')
for r in reviews:
    expected_packages = {p['package_key'] for p in packets[r['blind_key']]['citation_packages']}
    check({p['package_key'] for p in r['package_reviews']} == expected_packages, r['blind_key'] + ' every original citation package judged', 'reviews')
    for p in r['package_reviews']:
        expected_conditions = {x['id'] for x in questions[r['question_id']]['mandatory_predicates']}
        check({x['condition_id'] for x in p['predicate_reviews']} == expected_conditions, p['package_key'] + ' every mandatory predicate judged', r['blind_key'])
        opened = all(x['support_in_original_opened'] for x in p['predicate_reviews'])
        cited = all(x['support_in_original_citations'] for x in p['predicate_reviews'])
        check(opened == p['opened_complete'] and cited == p['cited_complete'], p['package_key'] + ' conjunctive evidence arithmetic', r['blind_key'])
        check(all(not x['support_in_original_citations'] or x['support_in_original_opened'] for x in p['predicate_reviews']), p['package_key'] + ' citations never repair unopened proof', r['blind_key'])
check(len(scored) == 144, 'raw and strict scored rows preserve both denominators', 'evidence/scored-slots.jsonl')
check(all(not r['valid_current_new_target'] or (r['new_target'] and r['opened_complete'] and r['cited_complete'] and r['provider_status_cross_reader'] == 'support') for r in scored), 'validity is conjunctive, not any-intersection', 'evidence/scored-slots.jsonl')
check(len({r['source_id'] for r in sources}) == len(sources), 'source observation IDs unique', 'sources.json')
minimum = [r for r in sources if r['count_in_minimum']]
check(len({r['original_document_id'] for r in minimum}) == len(minimum), 'counted originals deduplicated', 'sources.json original_document_id')
check(len(minimum) >= 32, 'at least 32 direct original documents', 'sources.json count_in_minimum')
check(sum(r['source_role'] == 'initial_design' for r in minimum) == 12, '12 first-design originals in minimum', 'sources.json')
required = ['source_id', 'related_questions', 'source_url', 'published_or_revised', 'version', 'checked_utc', 'sections_read', 'verified_content', 'limitations', 'producer', 'lineage_id', 'count_in_minimum', 'count_reason']
check(all(all(k in r for k in required) for r in sources), 'every source has required observation and limit fields', 'sources.json')

protocol = json.loads((BASE / 'evidence/return-url-budget.json').read_text())
result = {'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'checks': checks,
          'checks_count': len(checks), 'passed_checks': sum(r['passed'] for r in checks),
          'artifact_integrity_passed': all(r['passed'] for r in checks),
          'known_protocol_deviations': {'raw_routes_over_three_source_urls': [r['question_id'] + '-' + r['route'] for r in protocol if r['original_exceeded_three_urls']],
                                       'route_word_leaked_blind_keys': json.loads((BASE / 'evidence/blinding-amendment.json').read_text())['leaked_keys'],
                                       'q08_prospectively_resealed_after_other_cases_started': True,
                                       'not_all_current_provider_urls_are_immutable': True},
          'interpretation': 'Computational integrity is separate from protocol acceptance. A passing check does not erase disclosed deviations or fill historical gaps.'}
(BASE / 'evidence/artifact-validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, ensure_ascii=False, indent=2))
if not result['artifact_integrity_passed']:
    for r in checks:
        if not r['passed']:
            print(json.dumps(r, ensure_ascii=False))
    raise SystemExit(1)
