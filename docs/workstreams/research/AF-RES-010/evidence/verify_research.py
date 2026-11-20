"""Audit AF-RES-010's recorded evidence and ownership, without external searches.

From the repository root:
  PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-010/evidence/verify_research.py --output docs/workstreams/research/AF-RES-010/evidence/verification-report.json

This checks provenance, count boundaries and recorded judgment consistency. It
does not reproduce the cited experiments or execute a P1/P2 implementation.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve()
OWNED = HERE.parents[1]
ROOT = next(p for p in HERE.parents if (p / '.git').exists())
PREFIX = OWNED.relative_to(ROOT).as_posix() + '/'
BASE = '1eca580bf9ddc153f7c9691e30bd727eb7d0ce06'
P_INPUT = '62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1'
T_INPUT = '2b798c7d2b7355b649691c18de196104ceabb0f0'
SCOPE_COMMIT = 'ebcca564df68377cc116634dcdab1695be69c0e8'
checks = []


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def read(name):
    return json.loads((OWNED / name).read_text(encoding='utf-8'))


def check(name, ok, detail):
    checks.append({'check': name, 'passed': bool(ok), 'detail': detail})


def utc(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.tzinfo is not None and dt.utcoffset().total_seconds() == 0
    except (ValueError, TypeError, AttributeError):
        return False


parser = argparse.ArgumentParser()
parser.add_argument('--output')
args = parser.parse_args()
output = Path(args.output).resolve() if args.output else None
if output and not output.is_relative_to(OWNED):
    parser.error('output must remain under the task owned_path')

mandatory = ['SCOPE.md', 'sources.json', 'SEARCH_LOG.json', 'REPRESENTATIONS.md',
             'EVIDENCE.md', 'TRANSFER_CASES.md', 'RETRIAL.md', 'COST.md', 'SELF_CHECK.md']
check('required_pre_handoff_artifacts', all((OWNED / f).is_file() for f in mandatory), mandatory)

scope = (OWNED / 'SCOPE.md').read_text()
original = git('show', P_INPUT + ':docs/workstreams/research/AF-RES-002/PROTOCOL.md')
paragraphs = re.findall(r'^> (.+)$', original, re.M)
copies = re.findall(r'^> (.+)$', scope, re.M)
check('P1_P2_verbatim', copies == paragraphs and len(copies) == 2,
      {'sha': P_INPUT, 'paragraphs': len(copies), 'comparison': 'exact Unicode equality'})
required_lines = [line for line in original.splitlines()
                  if line.startswith(('- 고정 필수 조건:', '- 아직 정하지 않음:', '- 금지된 축약:'))]
check('fixed_constraints_verbatim', all(line in scope for line in required_lines),
      {'exact_lines': len(required_lines)})
check('SCOPE_unchanged_since_preregistration',
      git('show', SCOPE_COMMIT + ':' + PREFIX + 'SCOPE.md') == scope,
      {'scope_commit': SCOPE_COMMIT})

ledger = read('sources.json')
background = ledger['sources']
candidates = ledger['retrial_sources']
body = [s for s in background if s['level'] == 'D1']
required = {'id', 'url', 'accessed_at_utc', 'source_type', 'title', 'version_or_date',
            'sections_read', 'confirmed', 'limits', 'level', 'used_in'}
bad_fields = {s['id']: sorted(k for k in required if not s.get(k))
              for s in background + candidates if any(not s.get(k) for k in required)}
check('source_required_fields', not bad_fields, bad_fields)
bad_dates = [s['id'] for s in background + candidates if not utc(s['accessed_at_utc'])]
check('source_UTC_timestamps', not bad_dates, bad_dates)
check('background_minimum_32_body', len(body) >= 32, {'body': len(body), 'observation': len(background) - len(body)})
peer = [s for s in body if s.get('peer_reviewed')]
mr = [s for s in peer if s.get('methods_results_read')]
check('peer_reviewed_methods_results_minimum_12', len(mr) >= 12,
      {'peer_reviewed_total': len(peer), 'methods_results_read': len(mr),
       'ids': [s['id'] for s in mr], 'boundary': 'papers read, not independent experiments or replications'})
primary = [s for s in body if s.get('primary_representation_or_system_document')]
check('primary_representation_system_minimum_6', len(primary) >= 6, [s['id'] for s in primary])
original_transfer = [s for s in body if s.get('original_author_transfer')]
case_ids = {c for s in original_transfer for c in s.get('case_ids', [])}
check('original_author_transfer_minimum_8', len(original_transfer) >= 8 and len(case_ids) >= 8,
      {'works': len(original_transfer), 'cases': sorted(case_ids), 'work_ids': [s['id'] for s in original_transfer]})
all_sources = background + candidates
for field in ['id', 'url']:
    duplicates = [k for k, n in Counter(s[field] for s in all_sources).items() if n > 1]
    check('source_unique_' + field, not duplicates, duplicates)
check('Q5_separate_body_count', len(candidates) == 24 and all(
    s['level'] == 'D1' and s.get('count_toward_32_body_sources') is False for s in candidates),
    {'candidate_body_sources': len(candidates), 'excluded_from_background': True})
check('observation_excluded_from_body_minimum',
      all(s.get('count_toward_32_body_sources') is False for s in background if s['level'] != 'D1'),
      [s['id'] for s in background if s['level'] != 'D1'])

log = read('SEARCH_LOG.json')
plan = read('evidence/query-plan.json')['queries']
plan_map = {q['id']: q for q in plan}
web = [q for q in log['queries'] if q['system'].startswith('general_web')]
native = [q for q in log['queries'] if q['system'].startswith('AskNature')]
planned_native = [q for q in native if not q['id'].endswith('-RECHECK')]
groups = Counter((q['problem'], q['representation']) for q in web)
check('64_distinct_queries_8_each', len(web) == 64 and len({q['query'] for q in web}) == 64
      and len(groups) == 8 and set(groups.values()) == {8},
      {'total': len(web), 'unique_strings': len({q['query'] for q in web}),
       'groups': {'/'.join(k): v for k, v in groups.items()}})
check('executed_query_strings_match_plan', all(q['query'] == plan_map[q['id']]['query'] for q in web),
      'SCOPE froze rules and counts; query-plan exact strings are linked to execution, not claimed in the SCOPE commit')
check('R0_keeps_original_text', all(q['query'] in paragraphs[int(q['problem'][1])-1]
      for q in web if q['representation'] == 'R0') and all(
      next(q for q in web if q['id'] == p + '-R0-01')['query'] == paragraphs[i]
      for i, p in enumerate(['P1', 'P2'])), 'full paragraph once and seven exact contiguous quotations per problem')
check('native_selection_matches_first_and_fifth', len(planned_native) == 16 and
      {q['parent_query'] for q in planned_native} == {q['id'] for q in plan if q['native_search_repeat']},
      {'planned': len(planned_native), 'control': len(log['control_runs']), 'retry': len(native) - len(planned_native)})
valid_native = [q for q in planned_native if q['execution_status'] == 'results_observed']
check('two_actual_search_systems', len(web) == 64 and len(valid_native) == 15,
      {'web_observations': len(web), 'native_valid': len(valid_native),
       'native_with_links': sum(bool(q['results']) for q in valid_native),
       'native_without_links': sum(not q['results'] for q in valid_native),
       'native_total_attempts_with_control': len(native) + len(log['control_runs'])})
check('search_fields_and_times', all(utc(q['requested_at_utc']) and
      all(k in q for k in ['representation', 'query', 'system', 'results', 'opened', 'judgments',
                           'preserved_constraints', 'lost_or_unqueried_constraints', 'execution_status']) and
      all(hit.get('title') and hit.get('url') for hit in q['results']) for q in log['queries']),
      'Every query records result window, opening outcomes and projection losses')
failed_native = [q for q in native if q['execution_status'] != 'results_observed']
check('invalid_results_not_treated_as_empty', all('검증 실패' in q['screening_decision']
      and not q['results'] and not q['judgments'] for q in failed_native), [q['id'] for q in failed_native])

judgments = read('evidence/p1-judgments.json')['judgments'] + read('evidence/p2-judgments.json')['judgments']
source_map = {s['id']: s for s in candidates}
query_map = {q['id']: q for q in log['queries']}
t_values = {'not_needed', 'mapped', 'analogy_only', 'unknown'}
t_fields = ['mapping', 'bridge', 'excluded', 'counterexample', 'minimum_next_check']
check('T_axis_required_fields', len(judgments) == 25 and all(j['T'] in t_values and
      all(j.get(k) for k in t_fields) for j in judgments), {'rows': len(judgments), 'protocol': T_INPUT})
check('all_opened_candidates_have_T_judgments', {s for j in judgments for s in j['source_ids']} == set(source_map),
      {'judged_source_ids': sorted({s for j in judgments for s in j['source_ids']})})
link_errors = []
for j in judgments:
    for qid in j['query_ids']:
        q = query_map.get(qid)
        if not q or j['candidate_id'] not in {x['candidate_id'] for x in q['judgments']}:
            link_errors.append([j['candidate_id'], qid, 'missing judgment link'])
        elif not set(j['source_ids']).issubset({o['source_id'] for o in q['opened']}):
            link_errors.append([j['candidate_id'], qid, 'missing opened source link'])
check('query_judgment_source_links', not link_errors, link_errors)
check('bucket_T_consistency', all(
    (j['bucket'] != 'new_candidate' or (j['T'] == 'mapped' and j['label'] == 'CONDITIONAL_TRANSFER')) and
    (j['bucket'] != 'surface_false_positive' or (j['T'] == 'analogy_only' and j['label'] == 'SURFACE_OR_CONSTRAINT_MISMATCH')) and
    (j['bucket'] != 'near_miss' or (j['T'] == 'mapped' and j['label'] == 'SURFACE_OR_CONSTRAINT_MISMATCH'))
    for j in judgments), 'Relation correspondence and constraint violation remain separate')
counts = read('evidence/comparison-counts.json')
mismatches = []
for row in counts['rows']:
    relevant = [j for j in judgments if j['problem'] == row['problem'] and row['representation'] in j['representations']]
    for bucket in ['new_candidate', 'surface_false_positive', 'near_miss', 'insufficient', 'rediscovery', 'technical_support']:
        actual = len({j['family'] for j in relevant if j['bucket'] == bucket})
        if actual != row[bucket]:
            mismatches.append([row['problem'], row['representation'], bucket, actual, row[bucket]])
    actual_open = len({s for j in relevant for s in j['source_ids']})
    if actual_open != row['distinct_opened_sources']:
        mismatches.append([row['problem'], row['representation'], 'opened', actual_open])
check('comparison_independently_recomputed', not mismatches, mismatches)
family_counts = {b: len({(j['problem'], j['family']) for j in judgments if j['bucket'] == b})
                 for b in ['new_candidate', 'surface_false_positive', 'near_miss']}
check('conservative_family_totals', family_counts == {'new_candidate': 7, 'surface_false_positive': 8, 'near_miss': 3}, family_counts)
gao_misuse = next(j for j in judgments if j['candidate_id'] == 'RP2-C05-M')
check('review_fix_GAO_use_setting_consistent', '남기지 않는' in gao_misuse['explicit_setting'] and
      gao_misuse['requirement_scope_notes']['preserve_conflicting_changes'].startswith('violated_by_proposed_use') and
      gao_misuse['requirement_scope_notes']['inspect_and_resolve_conflicts'].startswith('violated_by_proposed_use'),
      'Misuse row now separately states silent overwrite, discarded alternatives and violated requirements')

retrial = (OWNED / 'RETRIAL.md').read_text()
cards = re.findall(r'^### 5\.([1-7]) .+$', retrial, re.M)
check('Q7_at_least_6_explanation_cards', len(set(cards)) >= 6, {'cards': len(set(cards))})
self_check = (OWNED / 'SELF_CHECK.md').read_text()
question_table = self_check.split('## 1. 질문별 내용 점검', 1)[1].split('\n## 2.', 1)[0]
question_rows = [line for line in question_table.splitlines() if re.match(r'^\| Q[1-8] ', line)]
check('SELF_CHECK_Q1_to_Q8_complete_rows', len(question_rows) == 8 and all(
      len(line.split('|')) == 7 and all(c.strip() for c in line.split('|')[1:-1]) for line in question_rows),
      'Eight content rows with answer, source kinds or experiment table, counterevidence and uncertainty; semantic review is separate')
missing_links = []
for path in OWNED.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
            continue
        target = link.split('#')[0]
        if target and not (path.parent / target).exists():
            missing_links.append([path.name, target])
check('local_document_links_exist', not missing_links, missing_links)
changed = set(git('diff', '--name-only', BASE).splitlines()) | set(git('ls-files', '--others', '--exclude-standard').splitlines())
outside = sorted(p for p in changed if not p.startswith(PREFIX))
check('owned_path_only', not outside, {'outside_paths': outside, 'task_paths': len(changed)})
whitespace = subprocess.run(['git', 'diff', '--check', BASE, '--', PREFIX], cwd=ROOT,
                            capture_output=True, text=True)
check('git_diff_check', whitespace.returncode == 0, whitespace.stdout + whitespace.stderr)

input_files = [p for p in OWNED.rglob('*') if p.is_file() and
               p.name not in {'SELF_CHECK.md', 'HANDOFF.md', 'verification-report.json', 'session-check.json'} and
               '__pycache__' not in p.parts]
hashes = {p.relative_to(OWNED).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(input_files)}
aggregate = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
report = {'status': 'passed' if all(c['passed'] for c in checks) else 'failed',
          'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'checked_git_head': git('rev-parse', 'HEAD').strip(),
          'scope_commit': SCOPE_COMMIT, 'source_commit': BASE,
          'input_sha256': aggregate, 'input_file_sha256': hashes,
          'boundary': 'Recorded research consistency and ownership audit; no paper reproduction, live search rerun or P1/P2 implementation test',
          'checks': checks}
if output:
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'checks': len(checks),
                  'failed': [c for c in checks if not c['passed']],
                  'input_sha256': aggregate, 'checked_git_head': report['checked_git_head']}, ensure_ascii=False))
sys.exit(0 if report['status'] == 'passed' else 1)
