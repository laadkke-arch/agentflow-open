"""Validate delivered ledgers and report against recorded evidence, without HTTP.

Optional --output writes a receipt inside this task's owned path. This is a
research consistency check, not a substitute for workbench's common checks.
"""
from pathlib import Path
import argparse
import collections
import csv
import datetime
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parents[1]
REPO = B.parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    checks = []

    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})

    def js(p):
        return json.loads((B / p).read_text())

    sources = [json.loads(l) for l in (B / 'sources.jsonl').read_text().splitlines()]
    sids = {s['source_id']: s for s in sources}
    normal = js('evidence/normalized-traversals.json')
    norm = {x['traversal_id']: x for x in normal}
    with (B / 'targets.csv').open(newline='') as f:
        targets = list(csv.DictReader(f))
    with (B / 'traversals.csv').open(newline='') as f:
        traversals = list(csv.DictReader(f))
    counts = js('evidence/counts.json')
    check('97 unique ledger IDs', len(sources) == len(sids) == 97)
    check('8 target purposes', len(targets) == len({r['purpose_id'] for r in targets}) == 8)
    r2target = next(r for r in targets if r['purpose_id'] == 'R2-next')
    check('R2 final criterion retains prior interpretation', 'SVG/재생 payload' in r2target['success_criterion'] and 'prior_success_criterion' in r2target['selection_evidence'])
    check('16 traversal IDs', len(traversals) == len(norm) == 16)
    pairs = collections.defaultdict(set)
    for t in traversals:
        tid = t['traversal_id'].removeprefix('R-')
        n = norm[tid]
        pairs[t['purpose_id']].add(t['route'])
        check(tid + ': view budget', 1 <= int(t['view_count']) <= 2 and int(t['view_count']) == n['view_count'])
        check(tid + ': axis equality', all(t[a] == n[a] for a in ('target_body', 'followup_resource', 'same_version')))
        check(tid + ': strict equality', (t['strict_success'] == 'true') == n['strict_success'])
        check(tid + ': entity byte sum', int(t['response_body_bytes']) == sum(v['body_bytes'] for v in n['steps']))
        for i, v in enumerate(n['steps'], 1):
            prefix = 'view_' + str(i) + '_'
            receipt = js(t[prefix + 'receipt'])
            check(tid + f': view{i} receipt', all(receipt[k] == v[k] for k in ('status', 'final_url', 'body_bytes', 'sha256', 'retrieved_utc')))
            check(tid + f': view{i} CSV fidelity', t[prefix + 'sha256'] == v['sha256'] and t[prefix + 'retrieved_utc'] == v['retrieved_utc'] and t[prefix + 'final_url'] == v['final_url'])
    check('8 complete A/B pairs', len(pairs) == 8 and all(v == {'A', 'B'} for v in pairs.values()))
    check('22 opens and 1890350 entity bytes', sum(x['view_count'] for x in normal) == counts['primary_document_views'] == 22 and sum(x['response_bytes'] for x in normal) == counts['primary_response_entity_bytes'] == 1890350)
    check('3 strict body and zero strict followup', sum(x['strict_success'] for x in normal if x['purpose_kind'] == 'body') == 3 and sum(x['strict_success'] for x in normal if x['purpose_kind'] == 'next') == 0)
    check('R2 no payload/static split', all(x['followup_resource'] == 'no_explicit_path' and x['static_output'] == 'confirmed' and not x['strict_success'] for x in normal if x['purpose_id'] == 'R2-next'))
    check('P3 separate legacy subject', all('NOT identical' in x['same_version_subject'] and x['followup_resource'] == 'unconfirmed' for x in normal if x['purpose_id'] == 'P3-next'))
    required = ('source_id', 'work_id', 'lineage_id', 'original_url', 'published_utc', 'retrieved_utc', 'version', 'location', 'questions', 'cases', 'observation', 'fingerprint', 'support_refute', 'limitations', 'reread_url')
    for s in sources:
        check(s['source_id'] + ': ledger fields', all(k in s for k in required))
        for key in ('receipt_path', 'excerpt_path'):
            if s.get(key):
                check(s['source_id'] + ': ' + key, (B / s[key]).is_file())
        if s['eligible']:
            receipt = js(s['receipt_path'])
            check(s['source_id'] + ': eligible response', receipt['status'] == 200 and not s.get('duplicate_of'))
    eligible = [s for s in sources if s['eligible']]
    cats = collections.Counter(s['minimum_category'] for s in eligible)
    check('45 primary materials and 18 lineages', len(eligible) == 45 and len({x['lineage_id'] for x in eligible}) == 18)
    check('primary category minima', all(cats[k] >= v for k, v in {'publisher': 8, 'asset': 6, 'method': 6, 'cross': 4}.items()))
    digests = [s['fingerprint'].get('sha256') for s in eligible]
    check('no repeated eligible payload digest', len([d for d in digests if d]) == len(set(d for d in digests if d)))
    result = (B / 'RESULT.md').read_text()
    headings = ['## 표 1.', '## 표 2.', '## 표 3.', '## 모집·실행·비교 분모']
    positions = [result.find(h) for h in headings]
    check('required table order', all(p >= 0 for p in positions) and positions == sorted(positions))
    for i, expected in enumerate((8, 16, 8)):
        text = result[positions[i]:positions[i+1]]
        check('required table ' + str(i+1) + ' rows', len([l for l in text.splitlines() if l.startswith('| ')]) - 1 == expected)
    last = result.split('## 마지막:')[-1]
    check('exactly three final weaknesses', len([l for l in last.splitlines() if l.startswith('| ')]) - 1 == 3 and not re.search(r'^## ', last, re.M))
    check('report denominators', all(v in result for v in ['1,890,350', 'PARTIAL', '0/0 산출 불가', '고유 직접1차자료45건', '계보18개']))
    selfcheck = (B / 'SELF_CHECK.md').read_text()
    check('Q1-Q7 covered', all(f'Q{i}' in selfcheck for i in range(1, 8)))
    for name in ('RESULT.md', 'SELF_CHECK.md', 'cards.md'):
        body = (B / name).read_text()
        links = re.findall(r'\]\(([^)]+)\)', body)
        for target in links:
            if not re.match(r'https?://', target) and not target.startswith('#'):
                target = target.split('#')[0]
                check(name + ': local link ' + target, (B / target).is_file())
    base = js('manifest.json')['base_commit']
    changed = subprocess.check_output(['git', 'diff', '--name-only', base, 'HEAD'], cwd=REPO, text=True).splitlines()
    check('committed owned path only', all(p.startswith('docs/workstreams/research/AF-RES-090/') for p in changed))
    check('central control unchanged', 'docs/automation/dot-control.json' not in changed)
    report = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'target_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
              'worktree_clean': not bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO, text=True)),
              'input_state': 'Files actually present were checked; hashes below distinguish a precommit working tree from an immutable clean checkout.',
              'status': 'PASS' if all(c['passed'] for c in checks) else 'FAIL',
              'exit_code': 0 if all(c['passed'] for c in checks) else 1,
              'checks': len(checks), 'failed': [c for c in checks if not c['passed']],
              'delivered_input_hashes': {n: hashlib.sha256((B / n).read_bytes()).hexdigest() for n in ('RESULT.md', 'SELF_CHECK.md', 'cards.md', 'targets.csv', 'traversals.csv', 'sources.jsonl', 'assets.jsonl')},
              'scope': 'Ledger/report/receipt/scope consistency; not a repeat external access or example execution test.'}
    if args.output:
        target = (B / args.output).resolve()
        if not target.is_relative_to(B):
            raise ValueError('Receipt must be inside owned path')
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(report['exit_code'])


if __name__ == '__main__':
    main()
