"""Check extraction joins, arithmetic, query caps and temporary-download hashes.

This is the same extractor's mechanical self-check, not independent adjudication.
It reads temporary source bytes when available and never runs study participant code.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import subprocess

P = Path(__file__).resolve().parent
ROOT = P.parents[5]

def rows(name):
    return [json.loads(line) for line in (P / name).read_text().splitlines() if line]

ledger_files = sorted(P.glob('*.jsonl'))
parsed_counts = {f.name: len(rows(f.name)) for f in ledger_files}
sources = rows('sources.jsonl')
studies = rows('studies.jsonl')
effects = rows('effects.jsonl')
screening = rows('screening.jsonl')
walks = rows('citation-walks.jsonl')
queries = rows('searches-single.jsonl')
source_ids = {r['source_id'] for r in sources}
assert len(source_ids) == len(sources)
assert len({r['original_url'] for r in sources}) == len(sources)
assert len({r['comparison_id'] for r in effects}) == len(effects)
missing_sources = []
for r in studies + effects:
    missing_sources.extend(s for s in r['source_ids'] if s not in source_ids)
for r in screening:
    if r.get('source_id') is not None and r['source_id'] not in source_ids:
        missing_sources.append(r['source_id'])
for r in walks:
    for key in ['from_source', 'target_source_id']:
        if r.get(key) is not None and r[key] not in source_ids:
            missing_sources.append(r[key])
assert not missing_sources, missing_sources
notes = (P / 'notes.md').read_text()
assert all(claim in notes for r in sources for claim in r['claim_ids'])
arithmetic_checks = 0
for r in effects:
    if 'original_control' in r:
        c, t = r['original_control'], r['original_intervention']
        assert math.isclose(r['absolute_difference'], t - c, abs_tol=1e-10)
        assert math.isclose(r['ratio'], t / c, abs_tol=1e-10)
        assert math.isclose(r['percent_change'], 100 * (t / c - 1), abs_tol=1e-10)
        arithmetic_checks += 1
    if 'recalculated_interval' in r:
        b, se = r['original_report']['coefficient'], r['original_report']['standard_error']
        assert all(math.isclose(a, v, abs_tol=1e-10) for a, v in zip(r['recalculated_interval'], [math.exp(b - 1.96 * se), math.exp(b + 1.96 * se)]))
        arithmetic_checks += 1
assert [q['actual_returned'] for q in queries] == [17, 28, 29, 18]
for q in queries:
    assert len(q['queries']) == 1
    assert len(q['screened_returned_positions']) == q['actual_returned'] <= 30
    assert [r['returned_position'] for r in q['screened_returned_positions']] == list(range(1, q['actual_returned'] + 1))
    assert all(r.get('screening_decision') and r.get('reason') for r in q['screened_returned_positions'])

receipts = json.loads((P / 'download-receipts.json').read_text())
hash_verified, hash_not_available = [], []
for r in receipts['files']:
    fp = P / 'tmp' / r['file']
    if not fp.exists():
        hash_not_available.append(r['file'])
        continue
    assert hashlib.sha256(fp.read_bytes()).hexdigest() == r['sha256'], r['file']
    hash_verified.append(r['file'])
temporary_files = [p for p in (P / 'tmp').rglob('*') if p.is_file()]
git_ignored = subprocess.run(['git', 'check-ignore', '--stdin'], input='\n'.join(str(p.relative_to(ROOT)) for p in temporary_files) + '\n', text=True, capture_output=True, cwd=ROOT)
assert git_ignored.returncode == 0
assert len(git_ignored.stdout.splitlines()) == len(temporary_files)
assert not [p for p in P.iterdir() if p.is_file() and p.suffix in ['.pdf', '.txt', '.csv']]

counts = json.loads((P / 'strand-counts.json').read_text())
assert counts['software_primary_originals'] == 6
assert counts['independent_original_artifacts'] == 4
assert counts['included_study_families'] == 6
assert counts['included_experiments'] == 7
assert counts['experiments_by_grade'] == {'R': 3, 'Q': 3, 'O': 1, 'U': 0}
assert counts['effect_rows'] == len(effects) == 16
assert sum(r['disposition'] == 'include_primary_human' for r in screening) == 6
assert sum(r['disposition'] == 'include_independent_artifact' for r in screening) == 4
assert sum(r['disposition'] == 'exclude_no_human_task_execution' for r in screening) == 1
receipt = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'command': 'python -B docs/workstreams/research/AF-RES-034/streams/software-b/verify_strand.py',
    'exit_code': 0,
    'parsed_jsonl_row_counts': parsed_counts,
    'strand_counts': counts,
    'source_joins_missing': missing_sources,
    'claim_ids_present_in_notes': True,
    'effect_arithmetic_or_interval_checks': arithmetic_checks,
    'single_query_returned_counts': [q['actual_returned'] for q in queries],
    'single_query_all_results_within_cap_and_screened': True,
    'download_hashes_verified': hash_verified,
    'download_hashes_unavailable_locally': hash_not_available,
    'temporary_download_files_ignored_by_git': len(temporary_files),
    'downloaded_originals_outside_tmp': 0,
    'git_head_readonly_at_check': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip(),
    'review_type': 'same extractor mechanical self-check; not independent reading or human-study replication',
    'not_verified': ['native ACM/IEEE complete first-30 ranks', 'unavailable original participant timing records', 'original NCQ lint analysis execution', 'root integration and remote reread/session check']
}
(P / 'verification.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
