#!/usr/bin/env python3
"""Join explicit exposure records; do not infer all host docs are later answers."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def jl(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]


def main():
    logs = list(csv.DictReader((BASE / 'search-log.csv').open()))
    rows = []
    def add(stream, raw, kind, qid, stage, receipt='', rank='', query='', url='', body=False, focal=False):
        match = [r for r in logs if r['stream'] == stream and r['question_id'] == qid
                 and (not receipt or r['receipt_id'] == receipt)
                 and (not query or r['query_index'] == str(query))
                 and (not rank or r['observed_rank'] == str(rank))
                 and (not raw.get('route') or r['route'] == raw['route'])]
        if not receipt and not query and not rank:
            match = []
        event = match[0] if len(match) == 1 else None
        rows.append({'exposure_id': raw.get('exposure_id', f'EXP-{len(rows)+1:03}'),
                     'stream': stream, 'question_id': qid or 'not_selected', 'route': raw.get('route', event['route'] if event else ''),
                     'stage': stage, 'exposure_kind': kind, 'url': url or (event['url'] if event else ''),
                     'observed_utc': raw.get('observed_utc', raw.get('checked_utc', raw.get('utc', event['finished_utc'] if event else 'unknown'))),
                     'query_index': query or (event['query_index'] if event else ''), 'observed_rank': rank,
                     'receipt_id': receipt or (event['receipt_id'] if event else ''),
                     'search_event_id': event['event_id'] if event else '', 'body_opened': body,
                     'focal_original_or_possible_followup': focal, 'raw_record': raw})
    for r in json.loads((BASE / 'streams/arrow/search-exposures.json').read_text()):
        add('arrow', r, 'possible_followup_search_excerpt', r['question_id'], 'candidate_search',
            query=r['query_index'], rank=r['observed_rank'], url=r.get('url', ''), focal=True)
    for r in json.loads((BASE / 'streams/arrow/exposures.json').read_text()):
        add('arrow', r, r['stage'], r['question_id'], 'sampling', url=r.get('source_url', ''), focal=r['question_id'].startswith('Q'))
    for r in jl(BASE / 'streams/cargo/exposures.jsonl'):
        qid = r.get('question_id', r.get('case_id'))
        if r.get('url') == 'https://github.com/rust-lang/rfcs/pull/3146':
            qid = 'Q08'  # final amended case; old record itself remains untouched
        stage = r.get('stage', 'unknown')
        focal = stage in ('candidate_search', 'candidate_open')
        rid = r.get('receipt_id', '')
        rank = r.get('observed_rank', '')
        if not rank and r.get('exposure_id') == 'CG-Q05-G-S3-P1':
            rank = 1
        add('cargo', r, r.get('exposure_kind', r.get('kind', 'unknown')), qid, stage,
            receipt=rid, rank=rank, url=r.get('url', ''), body=r.get('body_opened', r.get('body_read', False)), focal=focal)
    for r in csv.DictReader((BASE / 'streams/jupyter/search-exposures.csv').open()):
        kind = r['exposure_type']
        m = re.search(r'query(\d+)/rank(\d+)', r['unit'])
        add('jupyter', r, kind, r['question_id'], 'candidate_search' if m else 'shared_or_cross_question',
            query=m[1] if m else '', rank=m[2] if m else '', url=r['url'],
            body=kind in ('possible_followup_implementation', 'cross_question_provider_mechanism'),
            focal=kind == 'possible_followup_implementation')
    for r in csv.DictReader((BASE / 'streams/jupyter/exposures.csv').open()):
        add('jupyter', r, r['level'], r['question_id'], 'sampling', url=r['url'], focal=r['question_id'] == 'Q10')
    primary = sorted({r['question_id'] for r in rows if r['focal_original_or_possible_followup']
                      and r['stage'] in ('candidate_search', 'candidate_open')})
    metadata = sorted({r['question_id'] for r in rows if r['question_id'].startswith('Q')
                       and (r['stage'] == 'frame_metadata' or (r['stage'] == 'sampling' and r['focal_original_or_possible_followup']))})
    fields = list(rows[0])
    with (BASE / 'evidence/exposure-events.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in rows:
            w.writerow({**r, 'raw_record': json.dumps(r['raw_record'], ensure_ascii=False, sort_keys=True)})
    hits = [r for r in rows if r['focal_original_or_possible_followup'] and r['stage'] == 'candidate_search']
    result = {
        'exposure_records': len(rows),
        'focal_or_possible_later_answer_search_hit_records': len(hits),
        'search_hit_records_by_question': dict(Counter(r['question_id'] for r in hits)),
        'search_hit_unique_urls': len({r['url'] for r in hits if r['url']}),
        'primary_excluded_questions': primary,
        'primary_retained_questions': [f'Q{i:02}' for i in range(1, 13) if f'Q{i:02}' not in primary],
        'metadata_excluded_questions': metadata,
        'strict_retained_questions': [f'Q{i:02}' for i in range(1, 13) if f'Q{i:02}' not in set(primary + metadata)],
        'shared_context_questions': [f'Q{i:02}' for i in range(1, 13)],
        'limitations': 'Same-agent G/R sequential memory applies to every pair. Candidate names may have been known from training. Explicit focal exposure is counted separately from unrelated proposals, above-cap results and shared route memory. A current host implementation of uncertain lineage is conservatively counted when explicitly flagged. Retained does not mean proved unexposed to all prior knowledge.',
    }
    (BASE / 'evidence/exposure-summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
