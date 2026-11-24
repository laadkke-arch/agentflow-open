"""Reconstruct the mandatory tables and reconcile the sealed AF-RES-113 ledgers."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

P = Path(__file__).resolve().parent


def csvrows(name):
    with (P / name).open() as f:
        return list(csv.DictReader(f))


def jsonrows(name):
    return [json.loads(x) for x in (P / name).read_text().splitlines() if x]


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', '')


def table(headers, rows):
    return '\n'.join('| ' + ' | '.join(map(cell, r)) + ' |' for r in [headers, ['---'] * len(headers), *rows])


def link(label, url):
    return f'[{label}]({url})' if url else '공석'


def calculate():
    frame, bases, decisions, returns = map(csvrows, ['frame.csv', 'baselines.csv', 'decisions.csv', 'returns.csv'])
    requests, hops, sources = map(jsonrows, ['requests.jsonl', 'hops.jsonl', 'sources.jsonl'])
    tests, transfers = map(csvrows, ['verification-tests.csv', 'transfer.csv'])
    assert len(frame) == 120 and len(bases) == len(requests) == len(returns) == 6
    for project in ['librosa', 'scikit-image']:
        rs = [r for r in frame if r['stratum'] == project]
        if not rs and project == 'scikit-image':
            rs = [r for r in frame if r['stratum'] == 'skimage']
        assert len(rs) == 60
        assert [int(r['rank']) for r in rs] == list(range(1, 61))
        assert rs == sorted(rs, key=lambda r: (r['created_at'], int(r['number'])))
    statuses = Counter(r['status'] for r in frame)
    assert statuses['selected'] == 6 and statuses['excluded'] == 7
    slots = {f'R{i}-{arm}' for i in range(1, 7) for arm in 'AB'}
    assert len(hops) == len(decisions) == 12
    assert {h['slot_id'] for h in hops} == {d['decision_id'] for d in decisions} == slots
    assert sum(int(d['eligible_new_decisions']) for d in decisions) == 0
    assert sum(int(d['eligible_new_tests']) for d in decisions) == 0
    bmap = {r['request_id']: r for r in bases}
    for h in hops:
        assert (h['start_url'] or '') == bmap[h['request_id']]['start_url']
        assert h['characters_read'] <= 3000 and h['figures_read'] == 0 and h['additional_searches'] == 0
        assert h['explicit_opens'] in [0, 1]
    opened = [h for h in hops if h['explicit_opens']]
    assert {h['slot_id'] for h in opened} == {'R3-B', 'R4-A', 'R5-A'}
    assert all(h['characters_read'] == 3000 for h in opened)
    counted = [s for s in sources if s['unique_counted']]
    allocations = Counter(s['allocation'] for s in counted)
    assert allocations == {'request': 6, 'project': 8, 'method_original': 6, 'external': 4}
    assert len({s['work_id'] for s in counted}) == 24
    fields = Counter(s.get('external_field') for s in counted if s['allocation'] == 'external')
    assert sorted(fields.values()) == [2, 2]
    required = ['source_id', 'original_url', 'actual_url', 'work_id', 'event_id', 'author', 'edition', 'publication_date', 'checked_utc', 'section_read', 'confirmed', 'limitations', 'questions', 'ledger_rows', 'allocation', 'unique_counted', 'read_status', 'attempt_id']
    assert all(all(k in s for k in required) for s in sources)
    source_ids = {s['source_id'] for s in sources}
    assert len(source_ids) == len(sources)
    assert len(tests) == 21 and len(transfers) == 16
    assert len({t['test_id'] for t in tests}) == 21
    for r in tests + transfers:
        assert r['phase'] == 'postseal_verification'
        assert set(json.loads(r['source_ids'])) <= source_ids
    assert all(t['original_hop_credit'] == 'false' for t in tests)
    assert all(t['discovery_credit'] == 'false' and t['actual_adoption'] == 'unconfirmed' for t in transfers)
    grouped = [t for r in transfers for t in json.loads(r['test_ids'])]
    assert Counter(grouped) == Counter(t['test_id'] for t in tests)
    pairs = [r for r in bmap if all(next(h for h in hops if h['slot_id'] == r + '-' + arm)['actual_status'] == 'body_prefix_retrieved' for arm in 'AB')]
    assert not pairs
    assert all(r['comparison_category'] == '비교불가' for r in returns)
    census = {
        'status': 'PARTIAL', 'source_rows': len(sources),
        'distinct_original_source_addresses': len({s['original_url'] for s in sources}),
        'distinct_actual_source_addresses': len({s['actual_url'] for s in sources}),
        'declared_work_ids_all_records': len({s['work_id'] for s in sources}),
        'declared_event_ids_all_records': len({s['event_id'] for s in sources}),
        'recorded_source_read_attempt_ids': len({s['attempt_id'] for s in sources}),
        'unique_quota_works': len(counted), 'quota_by_allocation': dict(allocations),
        'external_fields': dict(fields), 'counted_source_ids': [s['source_id'] for s in counted],
        'natural_request_events': 6, 'frame_rows': 120, 'frame_statuses': dict(statuses),
        'formally_assessed': 13, 'batch_body_exposed': 22,
        'common_start_initial': 4, 'common_start_corrected': sum(bool(r['start_url']) for r in bases),
        'planned_slots': 12, 'eligible_link_addresses': 3, 'explicit_extra_opens': 3,
        'automatic_redirects': sum(len(h.get('receipt', {}).get('redirects', [])) for h in hops),
        'slot_statuses': dict(Counter(h['actual_status'] for h in hops)),
        'extra_characters_read': sum(h['characters_read'] for h in hops),
        'response_bytes': sum(h.get('receipt', {}).get('byte_count', 0) for h in hops),
        'summed_request_seconds_not_walltime': round(sum(h.get('receipt', {}).get('elapsed_seconds', 0) for h in hops), 6),
        'figures_read': 0, 'tokens': 'unobserved', 'money': 'unobserved',
        'new_choices_from_extra': 0, 'new_tests_from_extra': 0,
        'paired_readable_requests': pairs,
        'request_comparison': {'A만': 0, 'B만': 0, '양쪽': 0, '둘 다 없음': 0, '비교불가': 6},
        'effect_rate': None, 'initial_baseline_rows': len(jsonrows('evidence/common/baseline-tests.jsonl')),
        'postseal_test_rows': 21, 'postseal_semantic_groups': 16,
        'far_field_principle_discovery_credit': 0, 'verified_followup_adoptions': 0,
        'complete_target_library_executions': 0,
        'census_scope': 'Recorded ledger IDs, not independent experimental samples or all network requests. Same works/mirrors and failed reads are excluded from quota.'
    }
    t1 = []
    for r in bases:
        t1.append([r['request_id'] + ' / ' + r['stratum'], link('원글', r['issue_url']) + ' · 현재 snapshot / 고정 문서 ' + r['doc_version'], r['report_target_preserve'], r['report_known'], link(r['target_symbol'], r['start_url']), r['report_unconfirmed']])
    dmap = {r['decision_id']: r for r in decisions}
    t2 = []
    for h in hops:
        d = dmap[h['slot_id']]
        if h['planned_url']:
            dest = link('노출 링크', h['planned_url']) + ' → ' + link('도착', h.get('actual_url_canonical', h['actual_url'])) + ' · ' + ('초록/구독 preview' if h['actual_status'] == 'abstract_only' else 'main 첫3000자')
        else:
            dest = '공석: ' + ('공통 시작 미확정' if h['actual_status'] == 'vacant_start' else '적격 추가 href 없음')
        amount = f"{h['characters_read']}자 / 추가 {h['explicit_opens']}회 / 그림0"
        t2.append([h['slot_id'], dest, d['report_new'], d['report_input_expected'], d['report_source_checked'], d['report_limit'], amount])
    t3 = [[r['request_id'], r['availability'], r['comparison_category'], r['recommendation'] + ' · ' + link(r['return_section'], r['return_url']) + ' · ' + r['reason'], r['actual_followup']] for r in returns]
    text = '\n\n'.join([
        table(['요청·표본층', '원 글·판·URL', '목표 부분·보존 조건', '이미 아는 안', '공통 시작 절·URL', '미확인'], t1),
        table(['요청·경로', '노출된 링크→실제 도착 URL·절', '새 설계 선택 또는 시험', '구별 입력·두 예상값', '원전에서 확인한 내용', '반례·한계', '열람량'], t2),
        table(['고유 요청', '두 경로의 가용성', 'A만·B만·양쪽·둘 다 없음·비교불가', '반환할 링크·이유', '실제 후속 또는 미확인'], t3),
        '<!-- ANALYSIS -->\n\n' + (P / 'evidence/report-body.md').read_text().strip()
    ]) + '\n'
    return census, text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    census, result = calculate()
    canonical = json.dumps(census, ensure_ascii=False, indent=2) + '\n'
    if args.write:
        (P / 'RESULT.md').write_text(result)
        (P / 'evidence/source-census.json').write_text(canonical)
    else:
        assert (P / 'RESULT.md').read_text() == result, 'RESULT tables/body differ from ledgers'
        assert (P / 'evidence/source-census.json').read_text() == canonical, 'census differs'
    print(json.dumps({'check': 'PASS', **census}, ensure_ascii=False, indent=2))
