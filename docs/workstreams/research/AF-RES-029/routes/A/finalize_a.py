"""Route A only: preserve attempts and serialize a pre-bounded original return once."""
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('af_res_029_protocol', BASE / 'protocol.py')
protocol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(protocol)

def write_new(path, value, jsonl=False):
    if path.exists():
        raise ValueError('refusing overwrite: ' + str(path))
    data = ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in value) if jsonl else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.write_text(data, encoding='utf-8')

def run(qid):
    path = BASE / 'routes' / 'A' / qid
    decision = json.loads((path / 'decision.json').read_text())
    packet_input = json.loads((BASE / 'route-inputs' / 'A' / (qid + '.json')).read_text())
    receipts = []
    for p in sorted(path.glob('*.json')):
        if re.fullmatch(r'(search|open)-\d+\.json', p.name):
            r = json.loads(p.read_text())
            r['receipt_path'] = str(p.relative_to(BASE))
            receipts.append(r)
    assessments = {a['receipt']: a for a in decision.get('receipt_assessments', [])}
    for r in receipts:
        if r['receipt_path'] in assessments:
            r['body_assessment'] = assessments[r['receipt_path']]
    budget = {
        'navigation': sum(r['navigation_debit'] for r in receipts),
        'body_opens': sum(r['body_open_debit'] for r in receipts),
        'body_successes': sum(r['body_open_debit'] for r in receipts if r['status'] == 'readable_excerpt' and r.get('body_assessment', {}).get('body_usable', True)),
        'body_failures_or_unusable': sum(r['body_open_debit'] for r in receipts if r['status'] != 'readable_excerpt' or not r.get('body_assessment', {}).get('body_usable', True)),
        'common_reuse_count': len(decision.get('common_reuse', [])),
        'common_reuse_additional_calls': 0,
        'server_transfer_bytes': '미계측',
        'token_cost': '미계측',
        'local_utf8_response_json_bytes': sum(r['local_utf8_response_json_bytes'] for r in receipts),
    }
    sources = decision['sources']
    exposures = decision['exposures']
    hits = []
    for r in receipts:
        if r['operation_type'] != 'navigation_search':
            continue
        rank = 0
        for content in r['response'].get('content', []):
            if content.get('type') != 'text':
                continue
            for block in re.split(r'-{10,}\n', content['text']):
                ref = re.search(r'【(turn[^】]+)】', block)
                if not ref:
                    continue
                rank += 1
                before = block[:ref.start()].strip()
                url_match = re.search(r'\((https?://[^\n]+)\)\s*$', before)
                url = url_match.group(1) if url_match else None
                hit = {
                    'source_id': r['receipt_id'] + '-r' + str(rank).zfill(3),
                    'kind': 'search_snippet_attempt_only',
                    'publisher': urlsplit(url).netloc if url else 'unparsed search header',
                    'original_url': url,
                    'version_date': 'search metadata only; original edition unverified',
                    'checked_utc': r['ended_utc'],
                    'directly_read_sections': [],
                    'verified_finding': 'Discovery result only; not used as original evidence.',
                    'limitations': 'Original body not established by search response; provided position is not a certified global search rank.',
                    'question_id': qid, 'route': 'A', 'stage': 'route_search_discovery',
                    'receipt': r['receipt_path'],
                    'duplicate_group': url or ref.group(1),
                    'counted_eligibility': False,
                    'provided_rank': rank,
                    'ref_id': ref.group(1),
                    'title_header': before,
                }
                hits.append(hit)
                sources.append(hit)
                if url and (re.search(r'/pep-|/nep-|/issues/|/pull/|/RFCs/|/rfc/', url, re.I) or 'proposal' in before.lower()):
                    exposures.append({
                        'question_id': qid, 'route': 'A', 'stage': 'route_search_discovery',
                        'kind': 'incidental_proposal_or_followup_search_exposure',
                        'source_id': hit['source_id'], 'url': url,
                        'receipt': r['receipt_path'],
                        'description': 'Proposal/followup-like result title or snippet appeared in the permitted literal search. It was not opened or used as body evidence; frozen purpose and queries were unchanged.',
                    })
    ended = datetime.now(timezone.utc).isoformat()
    context = {
        'worker': 'route_a',
        'isolation': 'Separate Route A worker; no Route B results or other route judgments supplied or read.',
        'authorized_initial_batch_inputs': ['Q01','Q03','Q05','Q07','Q09','Q11'],
        'subsequent_input_authorization': decision.get('subsequent_input_authorization'),
        'common_commit': '5543465bd18542d3994280ebaab3487ae04a1e04',
        'initial_questions_commit': '3475576d56b4307bd75964b9a27dc2a60093efbf',
        'same_worker_prior_questions': decision.get('prior_questions', []),
        'cross_question_memory': True,
        'independent_human_reading': False,
        'sampled_current_proposals_opened': False,
    }
    packet = {
        'question_id': qid, 'route': 'A',
        'budget': budget, 'candidates': decision['candidates'],
        'started_utc': decision['started_utc'], 'ended_utc': ended,
        'context': context,
    }
    # This is the first and only final-return serialization, with no clipping/reordering.
    try:
        return_sha256 = protocol.write_return(path / 'return.json', packet)
    except Exception as exc:
        write_new(path / 'serialization-rejected.json', {'attempted_packet': packet, 'error': str(exc), 'utc': ended})
        raise
    route = {
        'question_id': qid, 'route': 'A',
        'started_utc': decision['started_utc'], 'ended_utc': ended,
        'elapsed_ms': int((datetime.fromisoformat(ended) - datetime.fromisoformat(decision['started_utc'].replace('Z','+00:00'))).total_seconds()*1000),
        'tool_elapsed_ms_sum': sum(r['elapsed_ms'] for r in receipts),
        'budget': budget,
        'calls': [{k:v for k,v in r.items() if k not in ('response','source_version','provided_result_order')} for r in receipts],
        'common_reuse': decision.get('common_reuse', []),
        'selection_rationale': decision['selection_rationale'],
        'receipt_assessments': decision.get('receipt_assessments', []),
        'empty_resource_explanation': decision.get('empty_resource_explanation'),
        'failures': [r['receipt_path'] for r in receipts if r['status'] in ('failure','failed_or_unusable_body','metadata_or_unusable_body') or not r.get('body_assessment', {}).get('body_usable', True)],
        'context': context,
        'return_sha256': return_sha256,
        'returned_candidate_count': len(packet['candidates']),
        'provided_search_results': len(hits),
        'search_rank_note': 'search_hits.jsonl enumerates every result in actual returned order including reddit refs; numeric suffixes are not substituted for supplied order.',
    }
    write_new(path / 'route.json', route)
    write_new(path / 'sources.jsonl', sources, True)
    write_new(path / 'exposures.jsonl', exposures, True)
    write_new(path / 'search_hits.jsonl', hits, True)
    print(json.dumps({'question_id':qid, 'path':str(path.relative_to(BASE)), 'candidate_count':len(packet['candidates']), 'calls':len(receipts), 'budget':budget, 'elapsed_ms':route['elapsed_ms'], 'return_sha256':return_sha256}))

if __name__ == '__main__':
    run(sys.argv[1])
