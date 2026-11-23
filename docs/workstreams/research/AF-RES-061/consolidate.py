"""Rebuild post-seal source indexes only; do not change predictions or raw runs."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess

P = Path(__file__).resolve().parent
OWN = 'docs/workstreams/research/AF-RES-061/'
INHERITED = '672366cdf4542d4ca9f579963d66c2745f4316ed'
SEAL = '02359364000057f69b00594d8b43571ac72df298'


def read_jsonl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    old = subprocess.check_output(['git', 'show', INHERITED + ':' + OWN + 'sources.jsonl'], text=True)
    inputs = [('sources.jsonl@' + INHERITED, [json.loads(s) for s in old.splitlines() if s.strip()])]
    for f in ['streams/graph/sources.jsonl', 'streams/android/sources.jsonl',
              'streams/react/sources.jsonl', 'streams/donors/sources.jsonl',
              'streams/final-audit/graph-sources.jsonl',
              'streams/final-audit/animation-sources.jsonl',
              'streams/final-audit/source-audit-sources.jsonl',
              'evidence/resume-sources.jsonl']:
        inputs.append((f, read_jsonl(P / f)))
    ignore = {'ledger_origin', 'ledger_origin_line', 'acquisition_refs', 'canonical_cases'}
    out = {}
    duplicates = 0
    raw = 0
    for f, rows in inputs:
        for line, r in enumerate(rows, 1):
            raw += 1
            key = r['source_id']
            payload = {k: v for k, v in r.items() if k not in ignore}
            if key in out:
                assert payload == {k: v for k, v in out[key].items() if k not in ignore}, key
                duplicates += 1
            else:
                out[key] = dict(r)
                out[key]['acquisition_refs'] = []
            out[key]['acquisition_refs'].append({'path': f, 'line': line})
    for r in out.values():
        r['canonical_cases'] = [s.replace('ANDROID-', 'AN-') for s in r.get('cases', [])]
    (P / 'sources.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in out.values()))
    log_paths = ['streams/graph/search-log.jsonl', 'streams/android/search-log.jsonl',
                 'streams/react/search-log.jsonl', 'streams/donors/search-log.jsonl',
                 'streams/final-audit/graph-search-log.jsonl',
                 'streams/final-audit/animation-search-log.jsonl',
                 'streams/final-audit/source-audit-search-log.jsonl',
                 'evidence/resume-search-log.jsonl']
    logs = []
    for f in log_paths:
        for line, r in enumerate(read_jsonl(P / f), 1):
            logs.append(dict(r, ledger_origin=f, ledger_origin_line=line))
    (P / 'search-log.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in logs))
    eligible = sorted({r['work_id'] for r in out.values() if r['count_eligible']})
    quota = json.loads((P / 'streams/final-audit/source-audit.json').read_text())['disjoint_allocation']
    allocations = [w for q in quota.values() for w in q['work_ids']]
    assert len(allocations) == len(set(allocations)) == len(eligible) == 31
    assert set(allocations) == set(eligible)
    counts = {
        'inherited_stage3_commit': INHERITED,
        'prediction_seal': SEAL,
        'record_unit': 'acquisition/source_id is distinct from work_id, case, participant and execution',
        'raw_source_rows_including_duplicate_root': raw,
        'identical_source_id_duplicates_merged': duplicates,
        'source_id_conflicts': 0,
        'canonical_source_records': len(out),
        'all_work_ids_including_excluded': len({r['work_id'] for r in out.values()}),
        'eligible_source_records': sum(bool(r['count_eligible']) for r in out.values()),
        'eligible_unique_primary_works': len(eligible),
        'eligible_work_ids': eligible,
        'disjoint_allocation': quota,
        'search_log_records': len(logs),
        'retained_implementations': 4,
        'retained_cases': 8,
        'stored_prediction_rows': 24,
        'available_prediction_views': 22,
        'missing_A_case_ids': ['GV-N', 'GV-B'],
        'available_A_B_case_count': 6,
        'operational_A_B_disagreements': {'observed': 0, 'denominator': 6, 'unit': 'case'},
        'differing_prediction_only_denominator': 0,
        'independent_original_outputs_among_differing_rows': {'located': 0, 'denominator': 0, 'rate': '해당 없음'},
        'independent_original_outputs_main_frame': {'located': 0, 'denominator': 8, 'existence_outside_reviewed_scope': '미확인'},
        'auxiliary_execution_main_rows': 6,
        'unexecuted_main_rows': ['GV-N', 'GV-B'],
        'human_designer_link_effect_experiment': '미실시',
        'participant_accounting': {
            'HEER-ROBERTSON-2007': 'same24 people in2 studies; not48',
            'DRAGICEVIC-2011': '12 main participants and4 pilot participation records; overlap unconfirmed',
            'pooled_unique_participants': '해당 없음; not pooled',
            'printed_trial_count_conflict': 'E003 printed2280 versus design product2880; no raw-data resolution'
        },
        'independent_output_quota_limit': 'HU/FR/Heer/Dragicevic are auxiliary independent works, not four same-version main-case outputs',
        'source_sha256': hashlib.sha256((P / 'sources.jsonl').read_bytes()).hexdigest()
    }
    dump(P / 'evidence/final-counts.json', counts)
    print(json.dumps({k: counts[k] for k in ['canonical_source_records', 'eligible_unique_primary_works', 'source_id_conflicts', 'search_log_records']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
