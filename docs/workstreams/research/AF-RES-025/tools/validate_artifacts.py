#!/usr/bin/env python3
"""Validate the experiment's denominators and auditable limits, not its thesis."""
import csv
import datetime as dt
import hashlib
import json
import io
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[3]


def jl(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]


def parse_time(s):
    if s.endswith(' UTC'):
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=dt.timezone.utc)
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

# Late evidence may annotate history but cannot repair a frozen discovery score.
history = [r for path in sorted((BASE / 'followups').glob('*/candidate-history.jsonl')) for r in jl(path)]
decisions = [r for path in sorted((BASE / 'followups').glob('*/decisions.jsonl')) for r in jl(path)]
raw_candidates = {(r['question_id'], r['candidate_id']) for r in raw if r.get('candidate_id')}
check(len(history) == 66 and {(r['question_id'], r['candidate_id']) for r in history} == raw_candidates,
      'all 66 original returned union candidates have a distinct historical record', 'followups/*/candidate-history.jsonl')
check(len(decisions) == 12 and {r['question_id'] for r in decisions} == set(questions),
      'all 12 questions have post-seal decision observations', 'followups/*/decisions.jsonl')
check(Counter(r['historical_availability'] for r in history) == {'supported': 1, 'not_available': 19, 'unknown': 46},
      'history denominator includes the OGC boundary correction', 'candidate-history.jsonl; JP-AMEND-001')
source_ids = {r['source_id'] for r in sources}
for r in history:
    check(set(r.get('source_ids', [])) <= source_ids and bool(r.get('next_minimum_check')),
          f'{r["question_id"]}/{r["candidate_id"]} historical evidence references and resume input', 'candidate-history.jsonl')
for r in decisions:
    check(set(r.get('source_ids', [])) <= source_ids and bool(r.get('source_urls')),
          r['question_id'] + ' questioner decision evidence distinct from provider inference', 'decisions.jsonl')
roles = Counter(r['source_role'] for r in minimum)
check(roles['provider'] >= 4 and roles['followup_decision'] >= 4 and roles['provider'] + roles['historical_provider'] + roles['followup_decision'] >= 16,
      'provider/followup minimum and role separation', dict(roles))
check({r['source_id'] for r in minimum if r['source_role'] == 'supplemental_original'} == {'SP-L01','SP-L02','SP-M01','SP-M02'},
      'two library and two manufacturing original documents after primary seal', 'supplements/sources.json')
eligible_ids = {r['source_id'] for r in minimum}
check(len({r['candidate_id'] for r in raw if r.get('candidate_id') and set(r.get('source_ids', [])) & eligible_ids}) >= 8,
      'at least eight returned candidate targets with counted primary source observations', 'returns-raw + sources')
check(not ({'AR-C003','AR-C007','JP-H012','AR-H006','AR-H021'} & eligible_ids),
      'rewritten summary, metadata and overlapping patch exclusions retained', 'source-eligibility-overrides.json')
check(len({r['minimum_count_group_id'] for r in minimum}) == len(minimum),
      'only one minimum-count representative per conservative lineage group', 'sources.json')

seal = json.loads((BASE / 'evidence/primary-seal.json').read_text())
for rel, expected_hash in seal['files'].items():
    if rel in ('judgments.csv', 'evidence/recount-summary.json'):
        continue
    check(hashlib.sha256((BASE / rel).read_bytes()).hexdigest() == expected_hash,
          'primary sealed bytes unchanged: ' + rel, 'evidence/primary-seal.json')
old_judgments = list(csv.DictReader(io.StringIO(subprocess.check_output(
    ['git','show','d1f506b1dde91e706360846f4c2eac5baabe492e:docs/workstreams/research/AF-RES-025/judgments.csv'], cwd=ROOT, text=True))))
current_judgments = list(csv.DictReader((BASE / 'judgments.csv').open()))
def provider_projection(rows):
    return [{k:v for k,v in r.items() if k != 'questioner_followup_choice'} for r in rows]
check(provider_projection(old_judgments) == provider_projection(current_judgments),
      'all 337 provider judgments unchanged; only questioner followup column annotated', 'git show primary seal versus judgments.csv')
for r in sources:
    if r['observation_file'].startswith(('followups/','supplements/')):
        try:
            after = parse_time(r['checked_utc']) >= parse_time('2026-11-22T05:50:22Z')
        except (ValueError, TypeError):
            after = False
        check(after, r['source_id'] + ' followup/supplement read after remote primary seal', r['checked_utc'])

outcomes = list(csv.DictReader((BASE / 'evidence/discovery-open-outcomes.csv').open()))
check(len(outcomes) == 130 and Counter(r['outcome'] for r in outcomes) == {'body_returned':115,'summary_only':7,'access_failure':8},
      'raw receipt open-outcome reconciliation counts every actual call', 'discovery-open-outcomes.csv')
top1 = json.loads((BASE / 'evidence/literal-top1-summary.json').read_text())
check(len(top1['route_rows']) == 24 and all(not r['current_new_success'] for r in top1['route_rows']),
      'literal first URL sensitivity retains 24 route denominators and zero new successes', 'literal-top1-summary.json')
check(top1['qualifying_current_known_use_slots'] == ['Q11-G-1'],
      'first URL removes Q01 multi-document proof and retains Q11 one-file proof', 'literal-top1-summary.json')

result_text = (BASE / 'RESULT.md').read_text()
lines = result_text.splitlines()
headers = [x for x in lines if x.startswith('| ') and ' --- ' not in x]
expected_headers = [
    '| 질문 ID·전체/부분 | 최초 목적·이미 명시된 대안 | G 상위 3개와 근거 URL | R 상위 3개와 근거 URL | 근거를 완전히 인용한 신규 후보 | 승·무·패·미확인 |',
    '| 후보 ID·경로·순위 | 해당 부분과 제안 사용 | 필수 조건·당시 판 | 조건별 근거 URL·절 | 연 절·인용한 절 | 충돌·보류·후속 선택 |',
    '| 경로·예산·집단 | 질문·슬롯 분모 | 검증된 신규·공통·독점 | 근접 오답·빈 슬롯 | 조회·열람·비용 | 민감도·미확인 |',
    '| Q 번호·주장·적용 범위 | 근거 원문 URL·정확한 절 또는 실행 영수증 | 확인한 내용·분자·분모 | 반례를 찾은 곳과 결과 | 미확인·판단을 바꿀 최소 자료 |',
]
positions = [result_text.find(h) for h in expected_headers]
check(lines[0].startswith('# AF-RES-025') and next(x for x in lines[1:] if x.strip()) == expected_headers[0] and all(x >= 0 for x in positions) and positions == sorted(positions),
      'four mandatory result tables directly below title in required order', 'RESULT.md')
last_header = '| 중요한 불일치·약점 | 근거 ID·URL | 영향을 받는 결정 | 다음 조사 질문·찾을 자료·최소 확인 |'
last = result_text.rsplit(last_header,1)[-1].strip().splitlines()
check(last[0].startswith('| ---') and len(last[1:]) == 3 and all(x.startswith('| ') for x in last[1:]),
      'RESULT ends with exactly three weakness data rows', 'RESULT.md end')
check(not re.search(r'\{\{[^}]+\}\}', result_text), 'no unresolved report placeholders', 'RESULT.md')
for path in ['frame.csv','queries.jsonl','search-log.csv','candidates.csv','judgments.csv','pairs.csv','return-examples.md','SCOPE.md','sources.json','RESULT.md','PROGRESS.md','SELF_CHECK.md','pending-checks.md']:
    check((BASE/path).exists(), 'required deliverable exists: ' + path, path)
acceptance = json.loads((BASE/'evidence/acceptance-evidence.json').read_text())
check(isinstance(acceptance,list) and all(isinstance(r.get('met'),bool) and all(k in r for k in ('condition','evidence','note')) for r in acceptance),
      'acceptance rows preserve required schema and boolean values', 'evidence/acceptance-evidence.json')
check(any(not r['met'] and 'URL' in r['condition'] for r in acceptance),
      'original URL budget deviation remains unmet rather than hidden by strict sensitivity', 'acceptance-evidence.json')

# No private connector identity is part of a public research artifact.
public_paths = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--','docs/workstreams/research/AF-RES-025'],cwd=ROOT,text=True).splitlines()
leaks = []
for rel in set(public_paths):
    path = ROOT / rel
    if path.is_file():
        text = path.read_text(errors='replace')
        if re.search(r'link_[0-9a-f]{20,}', text):
            leaks.append(rel)
check(not leaks, 'public artifacts contain no private connector link ID', leaks)

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
