"""Read-only reconciliation of frozen choices, joins, time windows and denominators.

--write saves the computed report. --check compares it with the committed report.
This validates records; it does not manufacture independent evidence or rerun apps.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta
import argparse, csv, io, json, subprocess, sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
PREFIX = 'docs/workstreams/research/AF-RES-105/'
STAGE1 = 'de11fb2b05c0e65cc1451826c720eebcbc3e52cd'
STAGE2 = '4a4aae107be25f71318dbb0c7b7cfa73506c5030'
CHRON = 'chronological'
AUX = 'explicit_statement_auxiliary'

def rows(name):
    return list(csv.DictReader((P / name).open()))

def stamp(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def frozen(sha, name):
    body = subprocess.check_output(['git', 'show', f'{sha}:{PREFIX}{name}'], cwd=ROOT, text=True)
    return list(csv.DictReader(io.StringIO(body)))

def calculate():
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)

    ledgers = {n: rows(n) for n in ['initial.csv', 'proposals.csv', 'followup.csv', 'returns.csv']}
    initial = {r['case_id']: r for r in ledgers['initial.csv']}
    proposals = {r['case_id']: r for r in ledgers['proposals.csv']}
    follow = {r['case_id']: r for r in ledgers['followup.csv']}
    returns = {r['case_id']: r for r in ledgers['returns.csv']}
    frame = rows('frame.csv')
    sources = [json.loads(line) for line in (P / 'sources.jsonl').read_text().splitlines() if line]
    source_index = {r['source_id']: r for r in sources}
    require(len(source_index) == len(sources), 'duplicate source IDs')
    for name, rr in ledgers.items():
        require(len(rr) == len({r['case_id'] for r in rr}) == 12, f'{name}: expected twelve distinct slots')
        require({r['case_id'] for r in rr} == set(initial), f'{name}: case join mismatch')
        for r in rr:
            for sid in json.loads(r.get('source_refs', '[]')):
                require(sid in source_index, f'{name}/{r["case_id"]}: unresolved source {sid}')
    frozen_initial = {r['case_id']: r for r in frozen(STAGE1, 'initial.csv')}
    initial_deltas = []
    for cid, old in frozen_initial.items():
        for key, value in old.items():
            if initial[cid].get(key) != value:
                initial_deltas.append({'case': cid, 'field': key, 'old': value, 'new': initial[cid].get(key)})
    require(not initial_deltas, 'chronological initial records changed after remote seal')
    frozen_proposals = {r['case_id']: r for r in frozen(STAGE2, 'proposals.csv')}
    proposal_deltas = []
    for cid, old in frozen_proposals.items():
        for key, value in old.items():
            if proposals[cid].get(key) != value:
                proposal_deltas.append({'case': cid, 'field': key, 'old': value, 'new': proposals[cid].get(key)})
    require(not proposal_deltas, 'proposal records changed after remote seal')

    recruitment = {}
    for site in ['blender', 'gis']:
        fr = [r for r in frame if r['stratum'] == CHRON and r['site'] == site]
        fr.sort(key=lambda r: (stamp(r['creation_utc']), int(r['question_id'])))
        require(len(fr) == 80, f'{site}: initial frame count')
        require([int(r['rank']) for r in fr] == list(range(1, 81)), f'{site}: creation/ID order differs from frozen rank')
        eligible = [r for r in fr if r['eligibility'] == 'eligible']
        selected = [r for r in fr if r['selected_slot'] in initial]
        require(len(selected) == 4, f'{site}: four chronological slots')
        require([r['question_id'] for r in selected] == [r['question_id'] for r in eligible[:4]], f'{site}: first four eligible not selected')
        recruitment[site] = {
            'read_initial_requests': len(fr), 'eligible': len(eligible),
            'excluded': len(fr) - len(eligible), 'selected': len(selected), 'vacant': 4 - len(selected),
            'first': {'id': fr[0]['question_id'], 'utc': fr[0]['creation_utc']},
            'last': {'id': fr[-1]['question_id'], 'utc': fr[-1]['creation_utc']},
            'selected_ranks': [int(r['rank']) for r in selected],
            'current_vs_initial_tag_differences': [r['question_id'] for r in fr if json.loads(r['current_tags']) != json.loads(r['initial_tags'])],
            'extension_used': False,
        }
    af = [r for r in frame if r['stratum'] == AUX]
    require(len(af) == 22, 'closed auxiliary match frame count')
    auxiliary_recruitment = {
        'screened_matched_events': len(af), 'by_site': dict(Counter(r['site'] for r in af)),
        'selected_case_ids': [r['selected_slot'] for r in af if r['selected_slot'] in initial],
        'selected': sum(r['selected_slot'] in initial for r in af),
        'vacant': 4 - sum(r['selected_slot'] in initial for r in af),
        'scope': 'closed indexed/available corpus; not exhaustive site-wide 2024 event census',
    }
    require(auxiliary_recruitment['selected'] == 4, 'four auxiliary slots')

    candidate_ids = [r['candidate_id'] for r in proposals.values()]
    episodes = [r['episode_id'] for r in follow.values()]
    require(len(set(candidate_ids)) == 12, 'candidate duplicated across cases')
    require(len(set(episodes)) == 12, 'question episode duplicated across cases')
    event_keys = []
    time_checks = []
    for cid, i in initial.items():
        p, f, r = proposals[cid], follow[cid], returns[cid]
        require(p['question_id'] == i['question_id'] == f['question_id'], f'{cid}: question join')
        require(p['candidate_id'] == f['candidate_id'] == r['candidate_id'], f'{cid}: candidate join')
        require(p['proposal_url'] == f['proposal_url'] == r['original_proposal_url'], f'{cid}: proposal URL join')
        start = stamp(p['proposal_utc'])
        end = stamp(f['window_end_utc'])
        require(end - start == timedelta(days=180), f'{cid}: follow-up end is not proposal plus 180 days')
        delay = (start - stamp(i['creation_utc'])).total_seconds()
        if i['stratum'] == CHRON:
            require(0 < delay <= 30 * 86400, f'{cid}: main first proposal outside 30 days')
        events = json.loads(f['author_events'])
        require(len(events) == int(f['author_event_count']), f'{cid}: author event total')
        for e in events:
            t = stamp(e.get('creation_utc', e.get('utc', '')))
            require(start <= t <= end, f'{cid}/{e["event_id"]}: follow-up outside window')
            speaker = e.get('speaker_public_user_id', e.get('speaker_user_id'))
            require(str(speaker) == i['owner_user_id'], f'{cid}/{e["event_id"]}: author ID mismatch')
            event_keys.append((i['site'], e.get('kind', 'comment'), str(e['event_id'])))
        for return_key, follow_key in [
            ('full_new_decidable_denominator', 'full_newness_decidable'),
            ('full_new_missing', 'full_newness_unknown'),
            ('changed_capability_new_numerator', 'changed_capability_new_explicit'),
            ('changed_capability_new_decidable', 'changed_capability_new_decidable'),
            ('changed_capability_new_missing', 'changed_capability_new_unknown'),
        ]:
            require(r[return_key] == f[follow_key], f'{cid}: return/follow-up denominator mismatch {return_key}')
        time_checks.append({'case': cid, 'proposal_delay_seconds': int(delay), 'followup_days': 180, 'owner_events_checked': len(events)})
    require(len(event_keys) == len(set(event_keys)), 'author event reused in selected episodes')

    counts = {}
    owner_keys = set()
    for st in [CHRON, AUX]:
        rr = [r for r in follow.values() if r['stratum'] == st]
        cc = [r['case_id'] for r in rr]
        known_owners = {(initial[c]['site'], initial[c]['owner_user_id']) for c in cc if initial[c]['owner_user_id'] not in ('', '미확인')}
        owner_keys.update(known_owners)
        def total(key):
            return sum(int(r[key]) for r in rr)
        counts[st] = {
            'slots': len(rr), 'unique_episodes': len({r['episode_id'] for r in rr}),
            'candidate_count': len({r['candidate_id'] for r in rr}),
            'verified_distinct_owner_ids': len(known_owners),
            'owner_identity_unknown_slots': sum(r['owner_identity'] == '미확인' for r in rr),
            'full_new_numerator': sum(r['full_new_awareness'] == 'explicit_new' for r in rr),
            'full_newness_decidable': total('full_newness_decidable'), 'full_newness_unknown': total('full_newness_unknown'),
            'changed_capability_new': total('changed_capability_new_explicit'),
            'changed_capability_decidable': total('changed_capability_new_decidable'),
            'changed_capability_unknown': total('changed_capability_new_unknown'),
            'fixed_proposal_execution_decidable': total('same_fixed_proposal_execution_decidable'),
            'fixed_proposal_execution_unknown': len(rr) - total('same_fixed_proposal_execution_decidable'),
            'fixed_proposal_success_numerator': sum(r['same_fixed_proposal_success'] == '1' for r in rr),
            'fixed_proposal_success_decidable': total('same_fixed_proposal_success_decidable'),
            'fixed_proposal_failure_reported': sum(r['same_fixed_proposal_success'] == '0' for r in rr),
            'learn_then_execute_numerator': sum(r['learn_then_same_operation_execute'] == '1' for r in rr),
            'learn_then_execute_decidable': total('learn_then_execute_decidable'),
            'return_actions': dict(Counter(returns[c]['action'] for c in cc)),
        }
    episode_overlap = sorted(set(r['episode_id'] for r in follow.values() if r['stratum'] == CHRON) & set(r['episode_id'] for r in follow.values() if r['stratum'] == AUX))
    require(not episode_overlap, 'cross-frame episode overlap')

    minimum = json.loads((P / 'evidence/source-counts.json').read_text())
    counted = [s for s in sources if s['counting']['counted_unique_primary_source']]
    lineages = [json.dumps(s['lineage'], ensure_ascii=False, sort_keys=True) if isinstance(s['lineage'], (dict, list)) else s['lineage'] for s in counted]
    require(len(lineages) == len(set(lineages)), 'counted work lineage duplicate')
    minimum_ids = [sid for group in minimum['mandatory_source_ids'].values() for sid in group]
    require(len(set(minimum_ids)) == 24, 'mandatory category allocation not 24 distinct works')
    for sid in minimum_ids:
        require(sid in source_index and source_index[sid]['counting']['counted_unique_primary_source'], f'mandatory work not counted: {sid}')
    for s in sources:
        for field in ['source_id', 'questions', 'opened_utc', 'publisher', 'lineage', 'version', 'location', 'observed', 'limits', 'status', 'counting']:
            require(field in s and s[field] not in (None, '', []), f'{s["source_id"]}: missing source field {field}')
        require(bool(s.get('original_url') or s.get('preserved_evidence') or s.get('reader_record')), f'{s["source_id"]}: neither original URL nor preservation location')
        if s['counting']['counted_unique_primary_source']:
            require(not any(token in s['status'].lower() for token in ['failed', 'failure', '404', '403']), f'failed response counted: {s["source_id"]}')
    require(len(counted) == minimum['conservatively_counted_unique_primary'], 'source total differs from source-counts.json')
    require(len(sources) == minimum['source_ledger_rows'], 'source row count differs from source-counts.json')

    return {
        'schema': 1, 'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
        'scope': 'ledger reconciliation; no empirical novelty rate, no external execution inferred',
        'frozen_records': {'initial_sha': STAGE1, 'initial_chronological_rows': len(frozen_initial), 'initial_changes': initial_deltas,
                           'proposal_sha': STAGE2, 'proposal_rows': len(frozen_proposals), 'proposal_changes': proposal_deltas},
        'recruitment': recruitment, 'auxiliary_recruitment': auxiliary_recruitment,
        'frame_rows': len(frame), 'counts': counts,
        'unique_selected_episodes': len(set(episodes)), 'unique_candidates': len(set(candidate_ids)),
        'verified_distinct_owner_ids_total': len(owner_keys), 'cross_frame_episode_overlap': episode_overlap,
        'author_events_unique': len(set(event_keys)), 'time_and_identity_checks': time_checks,
        'sources': {'ledger_rows': len(sources), 'counted_unique_primary': len(counted), 'mandatory_categories': minimum['mandatory_category_counts'],
                    'mandatory_source_ids': minimum['mandatory_source_ids'], 'mandatory_count': len(set(minimum_ids)), 'missing_required': 0,
                    'upstream_scope': minimum['upstream_scope'], 'counted_lineages': lineages},
        'inference_limits': [
            '0/0 full-operation novelty is not a zero-percent rate.',
            'Auxiliary cue-conditioned cases cannot estimate frequency of knowledge or learning.',
            'Main eight questions are not eight independent people: BL-T1 and BL-T2 share one verified owner.',
            'D1 reports, D2 source assertions and D3 researcher runs remain separate.',
            'Blender upstream math files were read; unavailable GN fixtures and author-history replication remain unperformed.',
        ],
    }

def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = ap.parse_args()
    report = calculate()
    target = P / 'evidence/reconciliation.json'
    if args.write:
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    else:
        if not target.exists() or json.loads(target.read_text()) != report:
            report['errors'].append('committed reconciliation differs from current records; inspect, do not silently overwrite')
            report['status'] = 'FAIL'
    print(json.dumps({'status': report['status'], 'errors': report['errors'], 'cases': report['unique_selected_episodes'],
                      'counted_primary': report['sources']['counted_unique_primary'], 'required_primary': report['sources']['mandatory_count'],
                      'counts': report['counts']}, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
