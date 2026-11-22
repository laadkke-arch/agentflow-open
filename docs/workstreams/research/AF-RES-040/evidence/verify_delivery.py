"""Read-only validation of AF-RES-040 evidence and review artifacts.

This does not execute GDAL, Sphinx, Docker, users, or external compatibility tests.
Use --output only to save a validation receipt inside the owned path.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

P = Path(__file__).resolve().parent.parent
REPO = P.parents[3]
OWNED = 'docs/workstreams/research/AF-RES-040/'
BASE = 'de544231bc72fa6f2ddb3e91f9c0e8d16a0d1f62'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()


def readj(path):
    return json.loads((P / path).read_text())


def jsonl(path):
    return [json.loads(x) for x in (P / path).read_text().splitlines() if x.strip()]


def readcsv(path):
    return list(csv.DictReader((P / path).open()))


def sha(path):
    return hashlib.sha256((P / path).read_bytes()).hexdigest()


def table_blocks(text):
    lines = text.splitlines()
    blocks = []
    current = []
    for n, line in enumerate(lines, 1):
        if line.startswith('|'):
            current.append((n, line))
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output')
    ap.add_argument('--final', action='store_true')
    args = ap.parse_args()
    checks = []
    def check(name, ok, evidence):
        checks.append({'id': name, 'passed': bool(ok), 'evidence': evidence})

    freeze = readj('evidence/pool-freeze.json')
    mismatches = [f for f, h in freeze['files_sha256'].items() if sha(f) != h]
    check('six_frozen_input_hashes_unchanged', not mismatches, {'files': freeze['files_sha256'], 'mismatches': mismatches})
    manifest = readj('manifest.json')
    check('assigned_branch_and_fixed_dependencies', git('branch', '--show-current') == 'work/research-af-res-040' and
          manifest['base_commit'] == BASE and {d['commit'] for d in manifest['dependencies']} ==
          {'b13db3931b4021ff9e1ac6e404590c09526c3087', '856e6b40ae12d43197a6f02f7bf6ab7a7506fd35'},
          {'head': git('rev-parse', 'HEAD'), 'branch': git('branch', '--show-current'), 'base': manifest['base_commit']})
    changed = set(git('diff', '--name-only', BASE, 'HEAD').splitlines())
    changed.update(git('ls-files', '--others', '--modified', '--exclude-standard').splitlines())
    changed.discard('')
    outside = sorted(x for x in changed if not x.startswith(OWNED))
    check('owned_path_only', not outside, {'changed_files_n': len(changed), 'outside': outside})
    control = 'docs/automation/dot-control.json'
    control_blob = git('rev-parse', BASE + ':' + control)
    check('dot_control_unchanged', git('hash-object', control) == control_blob and git('rev-parse', 'HEAD:' + control) == control_blob,
          {'base_blob': control_blob, 'working_blob': git('hash-object', control)})
    check('preregistered_scope_unchanged', git('rev-parse', '2ccbf7ab660d6e16dab637eea40867cbc4f83499:' + OWNED + 'SCOPE.md') ==
          git('hash-object', OWNED + 'SCOPE.md'), 'Original SCOPE kept; changes are appended in amendments.jsonl.')

    frame, pool = readcsv('frame.csv'), readcsv('pool.csv')
    selected = [r for r in frame if r['selection'] == 'selected']
    frame_ok = len(frame) == 60 and len(selected) == 8
    for route in ('G', 'S'):
        rs = [r for r in frame if r['route'] == route]
        frame_ok &= len(rs) == 30 and [int(r['frame_rank']) for r in rs] == list(range(1, 31))
        frame_ok &= [(r['created_at'], int(r['issue_number'])) for r in rs] == sorted((r['created_at'], int(r['issue_number'])) for r in rs)
        frame_ok &= sum(r['selection'] == 'selected' for r in rs) == 4
    check('frame_60_ordered_exposures_8_selected', frame_ok, {'rows': len(frame), 'selected': [r['case_id'] for r in selected]})
    check('pool_48_39_read_9_empty', len(pool) == 48 and sum(bool(r['url']) for r in pool) == 39 and
          all(r['read_status'] in ('direct_read', 'direct_full_relevant_section') for r in pool if r['url']),
          {'slots': len(pool), 'filled': sum(bool(r['url']) for r in pool), 'statuses': dict(Counter(r['read_status'] for r in pool))})

    src = jsonl('sources.jsonl')
    required = {'source_id', 'original_url', 'pinned_url_or_version', 'publisher', 'published_or_event_date', 'checked_utc', 'locator',
                'source_kind', 'verified_fact', 'limitation', 'question_ids', 'case_ids', 'duplicate_group', 'counted'}
    counted = [s for s in src if s['counted']]
    check('source_schema_ids_and_unique_counted_groups', all(required <= s.keys() for s in src) and
          len({s['source_id'] for s in src}) == len(src) and len({s['duplicate_group'] for s in counted}) == len(counted),
          {'source_rows': len(src), 'counted_unique': len(counted), 'mandatory_keys': len(required)})
    facts = readj('evidence/source-counts.json')
    check('minimum_source_count_and_mix', len(counted) >= 24 and facts['counted_unique_documents'] == len(counted) and
          facts['source_rows'] == len(src) and all(facts['exclusive_categories'][k] >= n for k, n in facts['minimums'].items()), facts)

    inp = readj('evidence/analysis-input.json')
    c_by = {c['candidate_id']: c for c in inp['candidates']}
    p_by = {c['candidate_id']: c for c in pool}
    original_coding = {}
    for route, letter in [('gdal','G'), ('sphinx','S')]:
        original_coding.update({c['candidate_id']: c for c in readj(f'evidence/{route}/coding-{letter}.json')['candidates']})
    source_ids = {s['source_id'] for s in src}
    check('all_candidate_sources_resolve', all(set(c['source_ids']) <= source_ids for c in c_by.values()), {'candidates': len(c_by)})
    views = jsonl('views.jsonl')
    input_ok = len(views) == 24 and len({(v['case_id'], v['arm']) for v in views}) == 24
    budget_ok = True
    recover_ok = True
    text_ok = True
    actual_lengths = []
    recovered_slots = 0
    for v in views:
        ordered = sorted((c for c in c_by.values() if c['case_id'] == v['case_id']), key=lambda c: c['rank'])
        input_ok &= v['input_order'] == [c['candidate_id'] for c in ordered]
        input_ok &= v['input_urls'] == [c['url'] for c in ordered]
        budget_ok &= v['budget'] == {'rows': 3, 'direct_links_per_row': 1, 'description_char_limit': 80, 'additional_clicks': 0}
        budget_ok &= len(v['cards']) == 3
        recovered = [i for g in v['all_groups'] for i in g['members']] + v['unfilled_pool_slots']
        recovered = sorted(recovered, key=lambda i: c_by[i]['rank'])
        recover_ok &= recovered == [c['candidate_id'] for c in ordered] and len(set(recovered)) == 6
        for cid in recovered:
            c, raw = c_by[cid], p_by[cid]
            recover_ok &= c['url'] == raw['url'] and c['description'] == raw['description'] and c['rank'] == int(raw['rank'])
            if c['url']:
                # Sampling metadata and later source-based coding are different
                # layers. S pool deliberately left semantic fields empty. Restore
                # the frozen row and the coded row independently via member ID.
                origin = original_coding[cid]
                recover_ok &= all(c[k] == origin[k] for k in ('implementation', 'component', 'purpose', 'version', 'upstream_key', 'evidence_roles', 'document_group'))
                recover_ok &= all(not raw[k] or c[k] == raw[k] for k in ('implementation', 'component', 'purpose', 'version', 'upstream_key'))
            recovered_slots += 1
        for g in v['all_groups']:
            recover_ok &= g['representative_id'] == min(g['members'], key=lambda i: c_by[i]['rank'])
        for card in v['cards']:
            budget_ok &= len(card['direct_links']) <= 1 and len(card['description']) <= 80
            if card['empty']:
                text_ok &= not card['direct_links'] and not card['description']
            else:
                c = c_by[card['candidate_id']]
                text_ok &= card['direct_links'] == [c['url']] and card['description'] == c['description'] and card['title'] == c['title']
                actual_lengths.append(len(card['description']))
    check('24_views_same_original_inputs', input_ok, {'views': len(views), 'case_arm_pairs': len({(v['case_id'], v['arm']) for v in views})})
    check('equal_declared_budget_and_candidate_text', budget_ok and text_ok,
          {'cards': len(views) * 3, 'description_length_min': min(actual_lengths), 'description_length_max': max(actual_lengths),
           'literal_equal_length': len(set(actual_lengths)) == 1, 'interpretation': 'same limit only; literal equal-length requirement unmet'})
    check('restore_members_order_urls_and_semantic_metadata', recover_ok, {'restored_slot_observations': recovered_slots,
          'metadata_source': 'frozen pool row and original route coding row independently restored by member ID; initial S semantic blanks remain in pool; coding corrections retained'})

    rels = readcsv('relations.csv')
    manual = {(r['left_id'], r['right_id']): r for r in inp['relation_pairs']}
    mismatched = []
    unknown_empty = 0
    for r in rels:
        pair = manual.get((r['left_id'], r['right_id']))
        if pair:
            if any(r[k] != pair[k] for k in ('relation', 'left_to_right', 'right_to_left')):
                mismatched.append([r['left_id'], r['right_id']])
        elif all(r[k] == 'unknown' for k in ('relation', 'left_to_right', 'right_to_left')):
            unknown_empty += 1
    check('manual_85_pairs_and_35_unknown_empty_pairs', len(rels) == 120 and len(manual) == 85 and not mismatched and unknown_empty == 35,
          {'rows': len(rels), 'manual_pairs': len(manual), 'unknown_empty_pairs': unknown_empty, 'mismatched': mismatched})

    losses = readcsv('losses.csv')
    counts = Counter((r['variant'], r['additional_clicks']) for r in losses)
    check('loss_variants_have_separate_denominators', len(losses) == 72 and counts ==
          {('strict', '0'): 24, ('strict', '1'): 24, ('unknown_merge', '0'): 8, ('version_group_relaxed', '0'): 8, ('version_requirement_relaxed', '0'): 8},
          {'rows': len(losses), 'by_variant': {str(k): v for k, v in counts.items()}})
    check('zero_eligible_denominators_are_not_percentages', all(r['conditional_path_recall'] == '해당 없음' for r in losses if int(r['eligible_paths_n']) == 0),
          {'zero_eligible_rows': sum(int(r['eligible_paths_n']) == 0 for r in losses)})
    b = {(r['case_id'], r['arm']): r for r in losses if r['variant'] == 'strict' and r['additional_clicks'] == '0'}
    per = {arm: sum(int(b[case, arm]['preserved_atoms_n']) for case in ('G1', 'G2', 'G3', 'G4', 'S1', 'S2', 'S3', 'S4')) for arm in 'ABC'}
    check('reported_partial_contrast_and_counterexample', per == {'A': 8, 'B': 6, 'C': 8} and
          json.loads(b['G2', 'B']['hidden_required_atoms']) == ['G2.A2'] and json.loads(b['S1', 'B']['hidden_required_atoms']) == ['S1-A1'] and
          all(json.loads(b['G4', arm]['preserved_atoms']) == ['G4.A2'] for arm in 'ABC'),
          {'preserved_atoms': per, 'complete_answerable': {arm: sum(b[case, arm]['answerability'] == 'documented' for case in ('G1','G2','G3','G4','S1','S2','S3','S4')) for arm in 'ABC'}})
    result = (P / 'RESULT.md').read_text()
    blocks = table_blocks(result)
    first_after_title = next(x for x in result.splitlines()[1:] if x.strip())
    check('required_tables_first_and_last_weakness_table', first_after_title.startswith('| 요구 ID·목적·판 |') and
          len(blocks[0]) == 12 and len(blocks[1]) == 26 and blocks[1][0][1].startswith('| 요구 ID | 방식 |') and
          len(blocks[-1]) == 5 and all(f'W{i}.' in blocks[-1][i+1][1] for i in range(1,4)) and
          result.rstrip().endswith(blocks[-1][-1][1]),
          {'table_1_lines': [blocks[0][0][0], blocks[0][-1][0]], 'table_1_rows': len(blocks[0])-2,
           'table_2_lines': [blocks[1][0][0], blocks[1][-1][0]], 'table_2_rows': len(blocks[1])-2,
           'last_table_lines': [blocks[-1][0][0], blocks[-1][-1][0]], 'last_table_rows': len(blocks[-1])-2})
    check('table_2_contains_all_exact_representative_urls', all(all(u in blocks[1][n+2][1] for u in json.loads(r['representative_urls']))
          for n, r in enumerate([b[case, arm] for case in ('G1','G2','G3','G4','S1','S2','S3','S4') for arm in 'ABC'])), '24 rows match exact representative link targets from losses.csv.')
    check('source_totals_explained_in_report', f'전체 조사 고유 원문{len(counted)}개' in result and
          f'전체 원장{len(src)}행 중{len(src)-len(counted)}행' in result, {'reported_counted': len(counted), 'rows': len(src)})
    ac_path = P / 'evidence/acceptance-evidence.json'
    if ac_path.exists():
        ac = readj('evidence/acceptance-evidence.json')
        badrefs = []
        for c in ac['criteria']:
            for e in c['evidence']:
                f = P / e['file']
                if not f.exists() or not (1 <= e['start_line'] <= e['end_line'] <= len(f.read_text().splitlines())):
                    badrefs.append([c['id'], e])
        check('acceptance_references_and_candid_status', not badrefs and ac['status'] == 'REVIEW_READY_WITH_GAPS' and
              all(isinstance(c['met'], bool) and 'numerator' in c and 'denominator' in c and 'reason' in c for c in ac['criteria']) and
              all(not next(c for c in ac['criteria'] if c['id'] == name)['met'] for name in
                  ('raw_href_prospective_sampling', 'literal_equal_description_length', 'uniform_directional_scope')),
              {'criteria': len(ac['criteria']), 'invalid_refs': badrefs})

    proc = subprocess.run([sys.executable, '-B', str(P/'evidence/recount.py'), '--check-only'], cwd=REPO, text=True, capture_output=True)
    check('recount_byte_identical', proc.returncode == 0, {'exit_code': proc.returncode, 'stdout': proc.stdout.strip(), 'stderr': proc.stderr.strip()})
    required_files = ['manifest.json', 'SCOPE.md', 'sources.jsonl', 'frame.csv', 'pool.csv', 'relations.csv', 'views.jsonl',
                      'losses.csv', 'RESULT.md', 'SELF_CHECK.md', 'evidence/acceptance-evidence.json']
    check('pre_handoff_deliverables_exist', all((P/f).is_file() for f in required_files), required_files)
    if args.final:
        check('handoff_is_final_separate_commit', (P/'HANDOFF.md').is_file() and
              git('diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').splitlines() == [OWNED+'HANDOFF.md'],
              {'head': git('rev-parse','HEAD'), 'changed': git('diff-tree','--no-commit-id','--name-only','-r','HEAD').splitlines()})
        check('working_tree_clean', not git('status', '--porcelain'), {'status': git('status', '--porcelain')})
        hb = table_blocks((P/'HANDOFF.md').read_text())
        check('handoff_same_three_priority_weaknesses', len(hb[-1]) == 5 and all(f'W{i}.' in hb[-1][i+1][1] for i in range(1,4)),
              {'last_table_rows': len(hb[-1])-2})

    receipt = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'status': 'passed' if all(c['passed'] for c in checks) else 'failed',
               'head_before_handoff_or_final': git('rev-parse','HEAD'), 'scope': 'artifact consistency only; scientific gaps remain',
               'checks_passed': sum(c['passed'] for c in checks), 'checks_total': len(checks), 'checks': checks,
               'input_sha256': {f: sha(f) for f in ['RESULT.md','SELF_CHECK.md','sources.jsonl','frame.csv','pool.csv','views.jsonl','relations.csv','losses.csv','evidence/analysis-input.json','evidence/recount.py']}}
    if args.output:
        dest = (P / args.output).resolve()
        if not dest.is_relative_to(P):
            raise ValueError('receipt must stay under owned path')
        dest.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(receipt if receipt['status'] == 'failed' else {k: receipt[k] for k in ['status','head_before_handoff_or_final','checks_passed','checks_total','scope']}, ensure_ascii=False))
    return 0 if receipt['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
