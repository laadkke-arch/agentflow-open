#!/usr/bin/env python3
"""Bounded, logged searches and source opens for AF-RES-092 (no network/model calls)."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'evidence' / '_cache'
LOG = ROOT / 'searches.jsonl'
PLAN = json.loads((ROOT / 'search_plan.json').read_text())
REPOS = {
    'jq': ('jqlang/jq', '71c2ab509a8628dbbad4bc7b3f98a64aa90d3297'),
    'pandoc': ('jgm/pandoc', 'c3038dcd54152c4e18e49db31676b79ee7cc29b2'),
    'rmarkdown': ('rstudio/rmarkdown', '561be5a7c7fde2b76a5649624d0c56373b8d86fa'),
    'fontspec': ('latex3/fontspec', 'a4be8a1359997e72612532882acaa64bb86e0566'),
    'eisvogel': ('Wandmalfarbe/pandoc-latex-template', 'cd58c398c7fbcca53ae891759e3bced71b37d84c'),
    'quarto': ('quarto-dev/quarto-cli', '466d959674507930685b2c977e878495932152ba'),
    'bbt': ('retorquere/zotero-better-bibtex', '0fcbd1ba96b8ec61fb4704ca7e2a32d89d5cc390'),
    'csl': ('citation-style-language/documentation', 'ea75983cc9f409a88ede93878d9525a734dbeb63'),
}

def utc():
    return datetime.now(timezone.utc).isoformat()

def append(obj):
    with LOG.open('a') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')

def events():
    return [json.loads(x) for x in LOG.read_text().splitlines()] if LOG.exists() else []

def priority(path):
    if path in ('MANUAL.txt', 'docs/content/manual/v1.7/manual.yml'):
        return 0
    if path.startswith(('doc/', 'docs/', 'site/', 'documentation/')) or path.endswith(('.md', '.rst')):
        return 1
    if path.startswith(('test/', 'tests/')):
        return 3
    return 2

def search(plan, number):
    assert number in (1, 2)
    old = events()
    assert not any(x['event'] == 'search' and x['case_id'] == plan['case_id'] and x['route'] == plan['route'] and x['query_number'] == number for x in old), 'search already executed'
    started = utc(); tick = time.monotonic(); rows = []; failures = []
    for repo_index, repo in enumerate(plan['repositories']):
        if repo not in REPOS or not (CACHE / repo).is_dir():
            failures.append({'repository': repo, 'error': 'frozen corpus unavailable; no substitute current source searched'})
            continue
        name, sha = REPOS[repo]
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=CACHE / repo, text=True).strip()
        assert head == sha, (repo, head, sha)
        paths = ['docs/content/manual/v1.7/manual.yml', 'src', 'tests'] if repo == 'jq' else ['MANUAL.txt', 'doc', 'src', 'data', 'test'] if repo == 'pandoc' else ['.']
        paths = [p for p in paths if (CACHE / repo / p).exists()]
        cmd = ['rg', '--json', '-i', '--glob', '!.git/**', '--glob', '!node_modules/**', '--glob', '!vendor/**', '--', plan['queries'][number-1], *paths]
        result = subprocess.run(cmd, cwd=CACHE / repo, capture_output=True, text=True)
        if result.returncode not in (0, 1):
            failures.append({'repository': repo, 'error': result.stderr, 'exit_code': result.returncode})
        for line in result.stdout.split('\n'):
            if not line:
                continue
            v = json.loads(line)
            if v['type'] != 'match':
                continue
            d = v['data']; path = d['path'].get('text', '').removeprefix('./')
            snippet = d['lines'].get('text', '').rstrip('\n')
            if not path:
                continue
            rows.append({'repository': repo, 'repo_index': repo_index, 'path': path, 'line': d['line_number'], 'snippet': snippet[:600], 'snippet_truncated': len(snippet)>600, 'url': f'https://github.com/{name}/blob/{sha}/{path}#L{d["line_number"]}', 'priority': priority(path)})
    rows.sort(key=lambda r: (r['repo_index'], r['priority'], r['path'], r['line']))
    visible = [{**r, 'rank': i+1} for i, r in enumerate(rows[:40])]
    e = {'event': 'search', 'case_id': plan['case_id'], 'route': plan['route'], 'query_number': number, 'query': plan['queries'][number-1], 'repositories': plan['repositories'], 'started_utc': started, 'finished_utc': utc(), 'elapsed_seconds': round(time.monotonic()-tick, 4), 'matches_total': len(rows), 'exposed': visible, 'exposed_count': len(visible), 'unexposed_count': max(0, len(rows)-40), 'failures': failures, 'backend': 'fixed official corpus rg --json -i', 'search_budget_used': 1, 'source_open_budget_used': 0}
    # Preserve ranks/URLs/fingerprints without reproducing whole upstream lines.
    persisted = {**e, 'exposed': [{k:v for k,v in r.items() if k != 'snippet'} | {'snippet_sha256':hashlib.sha256(r['snippet'].encode()).hexdigest()} for r in visible]}
    append(persisted)
    print(json.dumps({k:v for k,v in e.items() if k!='exposed'}, ensure_ascii=False))
    for r in visible:
        print(f"{r['rank']}. {r['repository']}/{r['path']}:{r['line']} {r['snippet'][:230]}")

def open_source(plan, repo, path, ranges):
    assert repo in plan['repositories'] and repo in REPOS
    old = [x for x in events() if x['event']=='open' and x['case_id']==plan['case_id'] and x['route']==plan['route']]
    opened = {x['repository']+'/'+x['path'] for x in old}
    new = repo+'/'+path not in opened
    assert len(opened) < 4 or not new, 'four-source limit reached'
    name, sha = REPOS[repo]; f = (CACHE / repo / path).resolve()
    assert f.is_relative_to((CACHE/repo).resolve())
    data = f.read_bytes(); lines = data.decode().splitlines()
    views=[]
    for spec in ranges.split(','):
        a,b = map(int, spec.split('-'))
        assert 1 <= a <= b <= len(lines), (a,b,len(lines))
        views.append({'first_line':a,'last_line':b,'url':f'https://github.com/{name}/blob/{sha}/{path}#L{a}-L{b}'})
    e={'event':'open','case_id':plan['case_id'],'route':plan['route'],'repository':repo,'path':path,'sha':sha,'url':f'https://github.com/{name}/blob/{sha}/{path}','read_utc':utc(),'file_sha256':hashlib.sha256(data).hexdigest(),'file_bytes':len(data),'line_count':len(lines),'views':views,'new_source':new,'distinct_open_ordinal':len(opened)+int(new),'source_open_budget_used':int(new),'memory_note':'same investigator; this route independently selects and opens this file, not independent blind reading'}
    append(e);print(json.dumps(e,ensure_ascii=False))
    for v in views:
        print('\nVIEW '+v['url'])
        for i in range(v['first_line'],v['last_line']+1):
            print(f'{i}: {lines[i-1]}')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('case');ap.add_argument('route',choices=['A','B']);ap.add_argument('action',choices=['search','open','close']);ap.add_argument('--query',type=int);ap.add_argument('--repo');ap.add_argument('--path');ap.add_argument('--lines');ap.add_argument('--reason');args=ap.parse_args()
    plan=next(x for x in PLAN['plans'] if x['case_id']==args.case and x['route']==args.route)
    if args.action=='search':search(plan,args.query)
    elif args.action=='open':open_source(plan,args.repo,args.path,args.lines)
    else:
        prior=[x for x in events() if x.get('case_id')==args.case and x.get('route')==args.route]
        searches=sum(x['event']=='search' for x in prior);opened=len({x['repository']+'/'+x['path'] for x in prior if x['event']=='open'})
        row={'event':'close','case_id':args.case,'route':args.route,'closed_utc':utc(),'searches_used':searches,'sources_opened':opened,'unused_searches':2-searches,'unused_source_opens':4-opened,'stop_reason':args.reason,'answer_exposure':'none before pre-outcome seal'}
        append(row);print(json.dumps(row,ensure_ascii=False))

if __name__=='__main__':main()
