#!/usr/bin/env python3
"""Normalize committed discovery observations without inventing or rescoring them.

Input streams remain authoritative. Missing instrumentation is 'unknown'.
Document audit/followup costs are intentionally outside this discovery ledger.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag, urlsplit, urlunsplit

BASE = Path(__file__).resolve().parents[1]
STREAMS = ('arrow', 'cargo', 'jupyter')


def jsonl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def cell(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v


def write_csv(p, rows, fields):
    with p.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows({k: cell(r.get(k, '')) for k in fields} for r in rows)


def first(row, *names, default=''):
    for name in names:
        if name in row and row[name] not in (None, ''):
            return row[name]
    return default


def boolean(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in ('true', '1', 'yes')


def canonical_url(url):
    # Only remove fragment and a terminal slash. Queries may select a version.
    parts = urlsplit(urldefrag(url or '')[0])
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip('/'), parts.query, ''))


def main():
    observations = []
    route_cost = defaultdict(lambda: Counter())
    receipts_seen = set()
    for stream in STREAMS:
        p = BASE / 'streams' / stream
        with (p / 'search-log.csv').open() as f:
            raw = list(csv.DictReader(f))
        receipts = {}
        for f in sorted((p / 'receipts').glob('*.json')):
            receipt = json.loads(f.read_text())
            rid = first(receipt, 'receipt_id', 'id', default=f.stem)
            receipts[rid] = (receipt, str(f.relative_to(BASE)), hashlib.sha256(f.read_bytes()).hexdigest())
        for seq, row in enumerate(raw, 1):
            kind = row['event_type']
            rid = row.get('receipt_id', '')
            receipt, receipt_path, receipt_hash = receipts.get(rid, ({}, '', ''))
            qid, route = row['question_id'], row['route']
            count = first(row, 'provided_count', 'provided_result_count', 'returned_count')
            rank = row.get('observed_rank', '')
            within = kind == 'search_result' and bool(rank) and int(rank) <= 10
            wall_ms = first(row, 'wall_ms', 'elapsed_ms')
            if wall_ms == '' and row.get('wall_seconds'):
                wall_ms = round(float(row['wall_seconds']) * 1000)
            request = first(receipt, 'request', default={})
            if not request and row.get('raw_request'):
                request = json.loads(row['raw_request'])
            url = row.get('url', '')
            r = {
                'event_id': f'{stream}:{seq:04}', 'stream': stream, 'event_type': kind,
                'question_id': qid, 'route': route, 'query_index': row.get('query_index', ''),
                'observed_rank': rank, 'engine_absolute_rank': first(row, 'engine_absolute_rank', 'search_engine_absolute_rank', default='unknown'),
                'request_utc': first(row, 'request_utc', 'started_utc'),
                'finished_utc': first(row, 'completed_utc', 'ended_utc', 'finished_utc'),
                'wall_ms': wall_ms, 'query': row.get('query', ''),
                'engine': row.get('engine', ''), 'response_length': row.get('response_length', ''),
                'provided_count': count,
                'first_ten_count': min(10, int(count)) if kind == 'search_request' and count else '',
                'shortfall_to_ten': max(0, 10 - int(count)) if kind == 'search_request' and count else '',
                'within_first_ten': within if kind == 'search_result' else '',
                'url': url, 'canonical_source_url': first(row, 'canonical_source_url', 'canonical_url', default=canonical_url(url)),
                'title': row.get('title', ''), 'ref_id': row.get('ref_id', ''),
                'disposition': first(row, 'disposition', 'decision', 'selection'),
                'reason': first(row, 'disposition_detail', 'reason'),
                'duplicate_of': row.get('duplicate_of', ''), 'duplicate_group': row.get('duplicate_group', ''),
                'source_id': row.get('source_id', ''), 'candidate_id': row.get('candidate_id', ''),
                'original_or_followup_exposure': row.get('original_or_followup_exposure', ''),
                'failure_reported': first(row, 'failure', 'error', default=first(receipt, 'is_error', 'isError', default='unknown')),
                'retry_of': row.get('retry_of', ''), 'receipt_id': rid, 'receipt_path': receipt_path,
                'receipt_file_sha256': receipt_hash, 'raw_request': request,
                'raw_response_sha256': first(row, 'raw_response_sha256', default=receipt.get('raw_response_sha256', 'unknown')),
                'tokens': 'unknown', 'billed_cost': 'unknown', 'human_hours': 'unknown',
                'raw_log_path': str((p / 'search-log.csv').relative_to(BASE)), 'raw_row_number': seq + 1,
            }
            observations.append(r)
            c = route_cost[(qid, route)]
            c[kind] += 1
            if kind == 'search_request':
                c['provided_results'] += int(count)
                c['eligible_results'] += min(10, int(count))
                c['shortfall_to_ten'] += max(0, 10 - int(count))
                c['queries_short_of_ten'] += int(int(count) < 10)
                c['over_ten'] += max(0, int(count) - 10)
            if kind != 'search_result':
                if not receipt_path:
                    raise ValueError(f'Missing receipt {stream}/{rid}')
                if (stream, rid) in receipts_seen:
                    raise ValueError(f'Duplicate call receipt {stream}/{rid}')
                receipts_seen.add((stream, rid))
                if wall_ms != '':
                    c['search_wall_ms' if kind == 'search_request' else 'open_wall_ms'] += float(wall_ms)
            if kind == 'search_result':
                d = r['disposition'].lower()
                c['duplicate_results'] += int('duplicate' in d)
                c['exposure_marked_results'] += int('exposure' in d or 'followup' in d or 'original_proposal' in d)
    fields = list(observations[0])
    write_csv(BASE / 'search-log.csv', observations, fields)
    costs = [{'question_id': q, 'route': r, **dict(c)} for (q, r), c in sorted(route_cost.items())]
    all_fields = ['question_id', 'route'] + sorted({k for r in costs for k in r} - {'question_id', 'route'})
    write_csv(BASE / 'evidence' / 'discovery-costs.csv', costs, all_fields)
    totals = Counter()
    for c in route_cost.values():
        totals.update(c)
    summary = {'row_count': len(observations), 'route_count': len(costs), 'totals': dict(totals),
               'wall_time_meaning': 'Sum of instrumented request durations; parallel requests may overlap. Not elapsed project time or human labor.',
               'absolute_search_ranking': 'unknown; observed_rank is only order supplied by this tool response',
               'cost_tokens': 'unknown', 'billed_cost': 'unknown', 'human_hours_saved': 'unknown',
               'raw_content_policy': 'Raw request and response hash plus returned metadata are preserved. Third-party full result text is not republished.'}
    dump(BASE / 'evidence' / 'discovery-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
