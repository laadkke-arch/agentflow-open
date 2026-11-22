"""Recompute AF-RES-040 views and losses from frozen, manually evidenced coding.

No network or product execution. Evidence truth is not established by this script.
Run from any directory with Python 3.12+: python -B evidence/recount.py [--check-only]
All outputs stay inside the task directory. Original input order is preserved.
"""
import argparse
from collections import Counter
import csv
import hashlib
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def signature(c, remove_version=False):
    return (c.get('upstream_key'), c.get('implementation'), c.get('component'),
            c.get('purpose'), None if remove_version else c.get('version'),
            tuple(sorted(c.get('evidence_roles', []))), c.get('scope_key', ''))


def key(c, arm, variant):
    if arm == 'A':
        return ('url', c['url'])
    if arm == 'B':
        return ('upstream', c['upstream_key']) if c.get('upstream_verified') else ('single', c['candidate_id'])
    if variant == 'unknown_merge' and not c.get('identity_verified') and c.get('upstream_verified'):
        # Treat unconfirmed identity as mergeable only when every recorded
        # positive attribute still agrees. Do not erase purpose or evidence role.
        return ('unconfirmed_matching_attributes',) + signature(c)
    if not c.get('identity_verified'):
        return ('single', c['candidate_id'])
    return ('semantic',) + signature(c, variant == 'version_group_relaxed')


def grouped(cs, arm, variant='strict'):
    groups = []
    keys = []
    for c in cs:
        if not c.get('url'):
            continue
        k = key(c, arm, variant)
        if k not in keys:
            keys.append(k)
            groups.append({'representative_id': c['candidate_id'], 'members': [], 'first_rank': c['rank']})
        groups[keys.index(k)]['members'].append(c['candidate_id'])
    return groups


def support_sets(req, cs, relaxed=False):
    support = {a['atom_id']: [] for a in req['required_atoms']}
    for c in cs:
        for atom in c.get('version_relaxed_atoms', c.get('atoms', [])) if relaxed else c.get('atoms', []):
            support.setdefault(atom, []).append([c['candidate_id']])
    explicit = req.get('atom_support_sets_relaxed', req.get('atom_support_sets', [])) if relaxed else req.get('atom_support_sets', [])
    for row in explicit:
        support.setdefault(row['atom_id'], []).extend(row['required_candidate_sets'])
    return support


def supported_atoms(support, visible):
    return {atom for atom, sets in support.items() if any(set(s).issubset(visible) for s in sets)}


def available_paths(paths, visible):
    return {p['path_id'] for p in paths if any(set(s).issubset(visible) for s in p['required_candidate_sets'])}


def closure(seed_ids, cs):
    # A fragment is a locator, not an access restriction on the opened document.
    docs = {c['document_group'] for c in cs if c['candidate_id'] in seed_ids}
    return {c['candidate_id'] for c in cs if c['document_group'] in docs and c.get('url')}


def build_view(req, cs, arm):
    gs = grouped(cs, arm)
    byid = {c['candidate_id']: c for c in cs}
    cards = []
    for n in range(3):
        if n >= len(gs):
            cards.append({'position': n + 1, 'empty': True, 'direct_links': [], 'description': '', 'description_budget': 80})
            continue
        g = gs[n]
        c = byid[g['representative_id']]
        cards.append({'position': n + 1, 'empty': False, 'candidate_id': c['candidate_id'],
                      'title': c['title'], 'description': c['description'],
                      'description_length': len(c['description']), 'description_budget': 80,
                      'direct_links': [c['url']], 'card_component': c['component'],
                      'hidden_members': g['members'][1:]})
    reps = {g['representative_id'] for g in gs[:3]}
    return {'case_id': req['case_id'], 'arm': arm,
            'input_order': [c['candidate_id'] for c in cs],
            'input_urls': [c['url'] for c in cs],
            'input_sha256': hashlib.sha256(dump(cs).encode()).hexdigest(),
            'budget': {'rows': 3, 'direct_links_per_row': 1, 'description_char_limit': 80, 'additional_clicks': 0},
            'cards': cards, 'all_groups': gs, 'cutoff_groups': gs[3:],
            'unfilled_pool_slots': [c['candidate_id'] for c in cs if not c.get('url')],
            'opened_document_groups': sorted({c['document_group'] for c in cs if c['candidate_id'] in reps}),
            'reachable_candidate_sections_without_extra_click': sorted(closure(reps, cs)),
            'observation_type': 'document-based reconstruction; no human click/adoption observation'}


def loss(req, cs, arm, variant='strict', clicks=0):
    gs = grouped(cs, arm, variant)
    byid = {c['candidate_id']: c for c in cs}
    representatives = [g['representative_id'] for g in gs[:3]]
    visible_seed = set(representatives)
    representative_accessible = closure(visible_seed, cs)
    if clicks:
        visible_seed = {i for g in gs[:3] for i in g['members']}
    accessible = closure(visible_seed, cs)
    all_ids = {c['candidate_id'] for c in cs if c.get('url')}
    relaxed = variant == 'version_requirement_relaxed'
    support = support_sets(req, cs, relaxed)
    required = {a['atom_id'] for a in req['required_atoms']}
    pool_atoms = supported_atoms(support, all_ids) & required
    got_atoms = supported_atoms(support, accessible) & required
    paths = req.get('eligible_paths_relaxed', req.get('eligible_paths', [])) if relaxed else req.get('eligible_paths', [])
    pool_paths = available_paths(paths, all_ids)
    got_paths = available_paths(paths, accessible)
    a_groups = grouped(cs, 'A')
    a_accessible = closure({g['representative_id'] for g in a_groups[:3]}, cs)
    a_paths = available_paths(paths, a_accessible)
    original_sigs = [signature(byid[i]) for i in representatives]
    distinct_sigs = set(original_sigs)
    false_pairs = [(a, b) for g in gs for a, b in combinations(g['members'], 2)
                   if signature(byid[a]) != signature(byid[b])]
    merged_hidden = {i for g in gs[:3] for i in g['members'][1:]}
    merge_possible = supported_atoms(support, closure(set(representatives) | merged_hidden, cs)) & required
    atom_complement_sets = {tuple(sorted({byid[i]['document_group'] for i in s}))
                              for a, sets in support.items() if a in required for s in sets
                              if len({byid[i]['document_group'] for i in s}) > 1}
    partial_complement_sets = {tuple(sorted({byid[i]['document_group'] for i in s}))
                              for p in req.get('partial_paths', []) for s in p['required_candidate_sets']
                              if len({byid[i]['document_group'] for i in s}) > 1}
    complement_sets = sorted(atom_complement_sets | partial_complement_sets)
    accessible_docs = {byid[i]['document_group'] for i in accessible}
    return {'case_id': req['case_id'], 'arm': arm, 'variant': variant, 'additional_clicks': clicks,
            'representative_ids': representatives, 'representative_urls': [byid[i]['url'] for i in representatives],
            'visible_card_components': [byid[i]['component'] for i in representatives],
            'hidden_card_components': sorted({byid[i]['component'] for i in all_ids - set(representatives)}),
            'opened_document_groups': sorted({byid[i]['document_group'] for i in visible_seed}),
            'click_model': 'one sibling-list expansion per displayed group, then all member originals assumed readable (upper bound)' if clicks else 'representative originals only',
            'actual_clicks_measured': False,
            'sibling_list_only_preserved_atoms': sorted(supported_atoms(support, representative_accessible) & required),
            'sibling_list_only_path_ids': sorted(available_paths(paths, representative_accessible)),
            'additional_source_documents_assumed': len({byid[i]['document_group'] for i in accessible} - {byid[i]['document_group'] for i in representative_accessible}),
            'accessible_sections': sorted(accessible), 'preserved_atoms': sorted(got_atoms),
            'pool_supported_atoms': sorted(pool_atoms), 'hidden_required_atoms': sorted(pool_atoms - got_atoms),
            'unsupported_required_atoms': sorted(required - pool_atoms),
            'merge_hidden_required_atoms': sorted(merge_possible - got_atoms),
            'required_atoms_n': len(required), 'preserved_atoms_n': len(got_atoms),
            'pool_supported_atoms_n': len(pool_atoms),
            'functional_duplicate_slots': len(original_sigs) - len(distinct_sigs),
            'same_document_repeat_slots': len(representatives) - len({byid[i]['document_group'] for i in representatives}),
            'heterogeneous_merged_pairs': false_pairs,
            'heterogeneous_merged_pairs_n': len(false_pairs),
            'returned_eligible_paths_vs_A': sorted(got_paths - a_paths),
            'returned_atoms_vs_A': sorted(got_atoms - supported_atoms(support, a_accessible)),
            'eligible_paths_n': len(pool_paths), 'preserved_paths_n': len(got_paths),
            'eligible_path_ids': sorted(pool_paths), 'preserved_path_ids': sorted(got_paths),
            'conditional_path_recall': len(got_paths) / len(pool_paths) if pool_paths else '해당 없음',
            'conditional_atom_recall': len(got_atoms) / len(pool_atoms) if pool_atoms else '해당 없음',
            'answerability': 'documented' if got_paths else ('partial' if got_atoms else 'unknown'),
            'complementary_sets_n': len(complement_sets),
            'single_atom_complementary_sets_n': len(atom_complement_sets),
            'partial_path_complementary_sets_n': len(partial_complement_sets),
            'preserved_complementary_sets_n': sum(set(s).issubset(accessible_docs) for s in complement_sets),
            'unknowns': req.get('unknowns', []),
            'user_clicks_adoption': '미확인'}


def relations(req, cs, coded_pairs):
    result = []
    for a, b in combinations(cs, 2):
        present = bool(a.get('url') and b.get('url'))
        same_project = present and a.get('upstream_verified') and b.get('upstream_verified') and a['upstream_key'] == b['upstream_key']
        coded = next((p for p in coded_pairs if p['left_id'] == a['candidate_id'] and p['right_id'] == b['candidate_id']), {})
        rel = coded.get('relation', 'unknown')
        ab = coded.get('left_to_right', 'unknown')
        ba = coded.get('right_to_left', 'unknown')
        # Evidence navigation equivalence is separate from software substitution.
        result.append({'case_id': req['case_id'], 'left_id': a['candidate_id'], 'right_id': b['candidate_id'],
                       'left_url': a.get('url', ''), 'right_url': b.get('url', ''),
                       'address_relation': 'identical' if present and a['url'] == b['url'] else ('different' if present else 'empty_slot'),
                       'same_fixed_document': present and a.get('document_group') == b.get('document_group'),
                       'project_relation': 'same_verified_upstream' if same_project else 'distinct_or_unconfirmed',
                       'left_component': a.get('component'), 'right_component': b.get('component'),
                       'left_version': a.get('version'), 'right_version': b.get('version'),
                       'left_roles': a.get('evidence_roles', []), 'right_roles': b.get('evidence_roles', []),
                       'relation': rel, 'left_to_right': ab, 'right_to_left': ba,
                       'substitution_scope': coded.get('substitution_scope', '미확인; 문자열 키로 대체 가능성을 추정하지 않음'),
                       'evidence_sources': sorted(set(a.get('source_ids', []) + b.get('source_ids', []))),
                       'evidence_locators': [a.get('locator', ''), b.get('locator', '')],
                       'coded_basis': coded.get('basis_locator', coded.get('basis', '')),
                       'coded_basis_sources': coded.get('basis_sources', ''),
                       'coding_origin': coded.get('coding_origin', 'route_observer') if coded else 'not_coded_empty_or_unknown',
                       'unknown': coded.get('limitation', '실행 호환·소비자 채택 미확인') if present else '빈 후보 슬롯'})
    return result


def csv_bytes(rows):
    import io
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows({k: dump(v) if isinstance(v, (dict, list)) else v for k, v in r.items()} for r in rows)
    return buf.getvalue().encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    inp = json.loads((ROOT / 'evidence/analysis-input.json').read_text())
    views, losses, rels = [], [], []
    checks = []
    for req in inp['requirements']:
        cs = sorted([c for c in inp['candidates'] if c['case_id'] == req['case_id']], key=lambda c: c['rank'])
        assert [c['rank'] for c in cs] == list(range(1, 7)), (req['case_id'], 'pool ranks')
        for arm in ('A', 'B', 'C'):
            view = build_view(req, cs, arm)
            assert len(view['cards']) == 3
            assert all(len(c['direct_links']) <= 1 and len(c['description']) <= 80 for c in view['cards'])
            recovered = sorted((i for g in view['all_groups'] for i in g['members']), key=lambda i: next(c['rank'] for c in cs if c['candidate_id'] == i))
            assert recovered == [c['candidate_id'] for c in cs if c.get('url')]
            views.append(view)
            losses.append(loss(req, cs, arm))
            losses.append(loss(req, cs, arm, clicks=1))
        losses.extend([loss(req, cs, 'C', 'unknown_merge'),
                       loss(req, cs, 'C', 'version_group_relaxed'),
                       loss(req, cs, 'C', 'version_requirement_relaxed')])
        rels.extend(relations(req, cs, inp.get('relation_pairs', [])))
        checks.append({'case_id': req['case_id'], 'same_pool_all_arms': True, 'budget_equal': True, 'all_members_restorable': True})
    assert len(views) == 24 and len(losses) == 72 and len(rels) == 120
    baseline = [r for r in losses if r['variant'] == 'strict' and r['additional_clicks'] == 0]
    summaries = {}
    for arm in ('A', 'B', 'C'):
        rows = [r for r in baseline if r['arm'] == arm]
        summaries[arm] = {'cases': len(rows), 'answerability': dict(Counter(r['answerability'] for r in rows)),
                          'eligible_requirement_denominator': sum(r['eligible_paths_n'] > 0 for r in rows),
                          'eligible_paths_denominator': sum(r['eligible_paths_n'] for r in rows),
                          'preserved_paths_n': sum(r['preserved_paths_n'] for r in rows),
                          'pool_supported_atoms_n': sum(r['pool_supported_atoms_n'] for r in rows),
                          'preserved_atoms_n': sum(r['preserved_atoms_n'] for r in rows),
                          'functional_duplicate_slots': sum(r['functional_duplicate_slots'] for r in rows),
                          'same_document_repeat_slots': sum(r['same_document_repeat_slots'] for r in rows),
                          'heterogeneous_merged_pairs': sum(r['heterogeneous_merged_pairs_n'] for r in rows),
                          'merge_hidden_atoms_n': sum(len(r['merge_hidden_required_atoms']) for r in rows),
                          'returned_eligible_paths_vs_A': sum(len(r['returned_eligible_paths_vs_A']) for r in rows)}
    pairs = {}
    paired_detail = []
    for a, b in combinations(('A', 'B', 'C'), 2):
        pairs[a + '_' + b] = Counter()
        for case in [r['case_id'] for r in inp['requirements']]:
            x = next(r for r in baseline if r['arm'] == a and r['case_id'] == case)
            y = next(r for r in baseline if r['arm'] == b and r['case_id'] == case)
            sign = 'tie' if x['preserved_atoms_n'] == y['preserved_atoms_n'] else (a + '_more' if x['preserved_atoms_n'] > y['preserved_atoms_n'] else b + '_more')
            pairs[a + '_' + b][sign] += 1
            xa, ya = set(x['preserved_atoms']), set(y['preserved_atoms'])
            possible = set(x['pool_supported_atoms']) | set(y['pool_supported_atoms'])
            paired_detail.append({'case_id': case, 'pair': a + '_' + b,
                                  'both_preserved_atoms': sorted(xa & ya), 'left_only_atoms': sorted(xa - ya),
                                  'right_only_atoms': sorted(ya - xa), 'neither_preserved_pool_atoms': sorted(possible - xa - ya),
                                  'pool_atom_denominator': len(possible),
                                  'left_complete': x['answerability'] == 'documented', 'right_complete': y['answerability'] == 'documented',
                                  'eligible_path_requirement': x['eligible_paths_n'] > 0,
                                  'left_answerability': x['answerability'], 'right_answerability': y['answerability'],
                                  'equal_atom_count': len(xa) == len(ya), 'same_atom_set': xa == ya})
    summary = {'views_n': len(views), 'loss_rows_n': len(losses), 'relation_rows_n': len(rels), 'per_arm': summaries,
               'paired_atom_comparison_all_8': pairs, 'paired_details': paired_detail, 'case_checks': checks,
               'limitations': ['manual evidence labels; no human usability observation', 'whole opened document is accessible; line anchors do not impose reading limits']}
    outputs = {'views.jsonl': ''.join(dump(v) + '\n' for v in views).encode(),
               'losses.csv': csv_bytes(losses), 'relations.csv': csv_bytes(rels),
               'evidence/recount-summary.json': (json.dumps(summary, ensure_ascii=False, indent=2) + '\n').encode()}
    for path, data in outputs.items():
        target = ROOT / path
        if args.check_only:
            assert target.read_bytes() == data, 'recount mismatch: ' + path
        else:
            target.write_bytes(data)
    print(json.dumps({'status': 'passed', 'mode': 'check-only' if args.check_only else 'write',
                      'counts': {k: summary[k] for k in ('views_n', 'loss_rows_n', 'relation_rows_n')},
                      'input_sha256': hashlib.sha256((ROOT / 'evidence/analysis-input.json').read_bytes()).hexdigest(),
                      'outputs_sha256': {k: hashlib.sha256(v).hexdigest() for k, v in outputs.items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
