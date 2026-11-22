#!/usr/bin/env python3
"""Rebuild observational search log and validate the frozen Cargo route records."""
import collections
import csv
import datetime as dt
import json
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

D = Path(__file__).resolve().parent
ROOT = D.parents[1]


def jl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def canonical(url):
    p = urlsplit(url)
    query = urlencode([(k, v) for k, v in parse_qsl(p.query)
                       if k not in {'highlight', 'source', 'trk', 'authuser', 'plain', 'activeTab', 'ref_type'}])
    path = p.path.replace('/stable/cargo/', '/cargo/')
    host = p.netloc.lower()
    if host == 'reproducible-builds.org':
        path = path.replace('/de/docs/', '/docs/')
    if host == 'web-dl.packagecloud.io':
        host = 'packagecloud.io'
    if 'maven.apache.org' in host and 'introduction-to-dependency-mechanism' in path:
        path = path.removesuffix('.html')
    if host == 'github.com' and path.startswith('/semver/semver/blob/') and path.endswith('/semver.md'):
        return 'https://semver.org/'
    if host == 'github.com' and '/github/docs/blob/' in path and path.endswith('/working-with-the-npm-registry.md'):
        return 'https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry'
    if host == 'clang.llvm.org' and 'CGDebugInfo_8cpp_source' in path:
        return 'https://llvm.googlesource.com/llvm-project.git/+/refs/heads/main/clang/lib/CodeGen/CGDebugInfo.cpp'
    path = path.replace('/%2B/', '/+/')
    return urlunsplit((p.scheme, host, path, query, ''))


def timestamp(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


def return_time(row):
    return row.get('returned_at', row.get('returned_at_utc'))


receipts = [json.loads(p.read_text()) for p in sorted((D / 'receipts').glob('CG-Q*.json'))]
searches = [r for r in receipts if r.get('query_index')]
opens = [r for r in receipts if not r.get('query_index')]
returns = jl(D / 'returns.jsonl')
candidates = jl(D / 'candidates.jsonl')
sources = json.loads((D / 'sources-candidates.json').read_text())
queries = {(q['question_id'], q['route']): q for q in jl(ROOT / 'queries.jsonl')
           if q['question_id'] in {'Q05', 'Q06', 'Q07', 'Q08'}}
rows = []
seen = {}
source_by_url = {canonical(s['source_url']): s['source_id'] for s in sources}
for r in sorted(searches, key=lambda x: (x['question_id'], x['route'], x['query_index'])):
    common = dict(question_id=r['question_id'], route=r['route'], query_index=r['query_index'],
                  request_utc=r['request_utc'], completed_utc=r['completed_utc'],
                  engine='system1_search_query', response_length='long',
                  query=r['request']['system1_search_query'][0]['q'], receipt_id=r['id'],
                  receipt_path='receipts/' + r['id'] + '.json',
                  raw_response_sha256=r['raw_response_sha256'],
                  provided_result_count=len(r['results']),
                  first_ten_result_count=min(10, len(r['results'])),
                  shortfall_to_ten=max(0, 10 - len(r['results'])), engine_absolute_rank='unknown',
                  tokens='unknown', billed_cost='unknown', human_hours='unknown')
    rows.append(dict(common, event_type='search_request', elapsed_ms=r['elapsed_ms'],
                     raw_request=json.dumps(r['request'], ensure_ascii=False)))
    for result in r['results']:
        url = result['url']
        canon = canonical(url)
        rank = result['observed_rank']
        key = (r['question_id'], r['route'], canon)
        duplicate_of = seen.get(key, '')
        hit_id = r['id'] + '-P' + str(rank)
        seen.setdefault(key, hit_id)
        disposition = result.get('disposition', 'not_opened_budget')
        rows.append(dict(common, event_type='search_result', observed_rank=rank,
                         url=url, canonical_source_url=canon, source_id=source_by_url.get(canon, ''),
                         title=result['title'], ref_id=result['ref_id'],
                         within_first_ten=rank <= 10, disposition=disposition,
                         disposition_detail=result.get('disposition_detail', ''),
                         duplicate_of=duplicate_of, duplicate_group=canon,
                         original_or_followup_exposure=('followup' in disposition or 'original_proposal' in disposition)))

for r in sorted(opens, key=lambda x: x['request_utc']):
    is_retry = '-RETRY' in r['id']
    body_status = r.get('status', r.get('outcome', 'unknown'))
    rows.append(dict(question_id=r['question_id'], route=r['route'], event_type='retry' if is_retry else 'open_attempt',
                     request_utc=r['request_utc'], completed_utc=r['completed_utc'], elapsed_ms=r['elapsed_ms'],
                     url=r['url'], canonical_source_url=canonical(r['url']), source_id=r['source_id'],
                     ref_id=r.get('response_ref', ''), disposition=body_status,
                     receipt_id=r['id'], receipt_path='receipts/' + r['id'] + '.json',
                     raw_request=json.dumps(r['request'], ensure_ascii=False), raw_response_sha256=r['raw_response_sha256'],
                     response_length=r['request']['response_length'], tokens='unknown', billed_cost='unknown', human_hours='unknown'))

fields = ['event_type', 'question_id', 'route', 'query_index', 'observed_rank', 'request_utc', 'completed_utc',
          'elapsed_ms', 'query', 'engine', 'response_length', 'provided_result_count', 'first_ten_result_count',
          'shortfall_to_ten', 'engine_absolute_rank', 'url', 'canonical_source_url', 'source_id', 'title', 'ref_id',
          'within_first_ten', 'disposition', 'disposition_detail', 'duplicate_of', 'duplicate_group',
          'original_or_followup_exposure', 'receipt_id', 'receipt_path', 'raw_request', 'raw_response_sha256',
          'tokens', 'billed_cost', 'human_hours']
with (D / 'search-log.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

route_stats = []
for key, query in sorted(queries.items()):
    q, route = key
    ss = sorted((r for r in searches if (r['question_id'], r['route']) == key), key=lambda r: r['query_index'])
    oo = [r for r in opens if (r['question_id'], r['route']) == key]
    rr = sorted((r for r in returns if (r['question_id'], r['route']) == key), key=lambda r: r['rank'])
    assert len(ss) == 3 and [r['request']['system1_search_query'][0]['q'] for r in ss] == query['query_strings'], key
    assert len(rr) == 3 and [r['rank'] for r in rr] == [1, 2, 3], key
    initial = [r for r in oo if '-RETRY' not in r['id']]
    retries = [r for r in oo if '-RETRY' in r['id']]
    assert len(initial) == 5 and len({canonical(r['url']) for r in initial}) == 5, key
    for retry in retries:
        assert any(r['url'] == retry['url'] for r in initial), retry['id']
    assert all(n <= 1 for n in collections.Counter(r['url'] for r in retries).values()), key
    assert all(timestamp(r['completed_utc']) <= timestamp(return_time(rr[0])) for r in oo + ss), key
    valid = [r for r in rr if r['new_target'] and r['provider_status'] == 'support' and r['opened_complete'] and r['cited_complete']]
    route_stats.append(dict(question_id=q, route=route, queries=3, offered_results=sum(len(r['results']) for r in ss),
                            selectable_results=sum(min(10, len(r['results'])) for r in ss), original_attempts=5,
                            retry_attempts=len(retries), returned_slots=3, valid_current=len(valid),
                            valid_historical=sum(r['historical_availability'] == 'supported' for r in valid),
                            held_slots=sum(r['provider_status'] == 'hold' for r in rr),
                            conflict_slots=sum(r['provider_status'] == 'conflict' for r in rr),
                            empty_slots=sum(r['candidate_id'] is None for r in rr),
                            returned_unique_urls=len({canonical(c['url']) for r in rr for c in r['returned_citations']}),
                            search_call_ms=sum(r['elapsed_ms'] for r in ss),
                            open_call_ms=sum(r['elapsed_ms'] for r in oo),
                            first_request_utc=min(r['request_utc'] for r in ss), returned_at=return_time(rr[0])))

for q in ['Q05', 'Q06', 'Q07', 'Q08']:
    first, second = ('G', 'R') if int(q[1:]) % 2 else ('R', 'G')
    earlier = next(r for r in route_stats if r['question_id'] == q and r['route'] == first)
    later = next(r for r in route_stats if r['question_id'] == q and r['route'] == second)
    assert timestamp(earlier['returned_at']) <= timestamp(later['first_request_utc']), q

stats = dict(rebuilt_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(), question_count=4, route_count=8,
             query_count=len(searches), original_open_attempts=40, retry_attempts=len(opens)-40,
             receipt_count=len(receipts), source_rows=len(sources),
             source_minimum_count=sum(s['count_in_minimum'] for s in sources),
             candidate_route_rows=len(candidates), union_candidate_count=len({c['candidate_id'] for c in candidates}),
             returned_slots=len(returns), route_stats=route_stats,
             cost_note='Sum of actual tool-call elapsed milliseconds, not elapsed human labor or total user-facing wall time. Calls within one route may overlap.',
             tokens='unknown', billed_cost='unknown', human_hours='unknown',
             independent_verdict='not yet performed', returns_frozen=True)
(D / 'search-statistics.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in stats.items() if k != 'route_stats'}, ensure_ascii=False, indent=2))
