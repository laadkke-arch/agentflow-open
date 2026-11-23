"""Normalize source records and deduplicate credited works; no network access."""
from pathlib import Path
import json
import re
from collections import Counter

ROOT=Path(__file__).resolve().parent
FILES=[
 'evidence/python/sources.jsonl','evidence/python/catalog-sources.jsonl',
 'evidence/python/observation-sources.jsonl','evidence/python/release-test-sources.jsonl',
 'evidence/markdown/sources.jsonl','evidence/markdown/observation-sources.jsonl',
 'evidence/markdown/release-test-sources.jsonl','evidence/crossfield/sources.jsonl',
 'evidence/additional-source-status.jsonl']
REQUESTS={'PY-I564','PY-I574','M-ISS-941','M-ISS-955'}
LISTS={'PY-LIST','PY-RULE','M-LIST-PRIMARY','M-LIST-RULES'}
CROSS={'X01','X02','X03','X04'}
SUPPLIERS={'PY-O01','PY-O03','PY-O05','PY-O14',
           'M-VENDOR-PARSE','M-VENDOR-STRINGIFY','M-VENDOR-CLI','M-VENDOR-MDAST'}
RELEASE_TESTS={'PY-T01','PY-T02','M-RELEASE-15','M-TEST-UTILITY'}
FAILURE_MINIMUM={
 'PY-F01':'The same tree/main URL response and exact arrival at the observed revision; a different pinned README does not recover that path.',
 'M-FAIL-941':'Original sandbox package.json/lockfile and pipeline source for issue941; resolve the literal react-stringify10.0.2 identity.',
 'M-FAIL-955':'Original sandbox package.json/lockfile and pipeline source for issue955; reproduce the raw span/pre/code HTML strings.'}

def choose(d,*keys,default=''):
    for k in keys:
        if k in d and d[k] not in (None,'',[]):return d[k]
    return default

def normalize(d,origin,line):
    sid=choose(d,'source_id','id')
    if not sid:raise ValueError(f'Missing source ID {origin}:{line}')
    url=choose(d,'url','source_url','requested_url')
    kind=choose(d,'source_type','type','material_type','kind')
    raw_allocation=choose(d,'allocation','allotment','quota_category')
    direct=choose(d,'direct_open','directly_opened',default=False)
    if isinstance(direct,str):direct=direct.lower() in ('true','yes','read','opened')
    work=choose(d,'work_id','authored_work_id',default=sid)
    # The routing README and its later exact arrival remain one authored work.
    if work in ('remark-readme','remark-root-readme') or re.search(r'(?:raw.githubusercontent.com/remarkjs/remark/[^/]+/readme\.md|github.com/remarkjs/remark/blob/[^/]+/readme\.md)$',url):
        work='remarkjs/remark:readme.md'
    allocation='background'
    if sid in REQUESTS:allocation='user_request'
    elif sid in LISTS:allocation='catalog_rule'
    elif sid in CROSS:allocation='crossfield'
    elif sid in RELEASE_TESTS:allocation='release_test'
    elif sid in SUPPLIERS:allocation='supplier_doc'
    duplicate=choose(d,'duplicate_of',default=None)
    limit=choose(d,'limitations','limitation')
    failure=choose(d,'error','failure',default=None)
    if not direct and failure is None:
        failure=choose(d,'observed','finding',default=limit)
        if sid.startswith('PY-INV-'):failure=limit
    finding=choose(d,'finding','observed','checked_content','summary',default='미확인: no original content obtained' if not direct else '')
    locator=choose(d,'locator','section','lines','source_lines',default='Exact URL retrieval attempt; no content locator obtained' if not direct else '')
    minimum=choose(d,'minimum_material_to_change_answer','minimum_to_change_answer','minimum_to_change',default=FAILURE_MINIMUM.get(sid))
    attempt=choose(d,'attempt','attempts',default=('Direct open of the exact URL; details in origin row' if not direct else None))
    if sid=='M-FAIL-955':
        limit='No attachment source read. Original package.json and pipeline are required for the raw HTML requirements in M-N2. The origin row reused the NM1 template label; this normalization corrects that label only.'
    return dict(source_id=sid,question_ids=choose(d,'question_ids',default=[]),
        requirement_ids=choose(d,'requirement_ids','case_ids',default=[]),
        publisher=choose(d,'publisher','author'),work_id=work,material_kind=kind,
        allocation=allocation,original_allocation=raw_allocation,url=url,
        retrieval_url=choose(d,'retrieval_url','api_url','final_url'),
        checked_utc=choose(d,'checked_utc','verified_utc','fetched_utc','fetched_at','utc'),
        version=choose(d,'version','version_sha','commit','tag'),
        sha=choose(d,'sha','blob_sha','sha256','body_sha256'),
        locator=locator,finding=finding,limitations=limit,
        stance=choose(d,'stance',default='unconfirmed'),duplicate_of=duplicate,
        evidence_lineage=choose(d,'evidence_lineage','evidence_parent','lineage',default=[]),
        direct_open=bool(direct),counts_in_minimum=False,
        failure=failure,attempt=attempt,minimum_material_to_change=minimum,
        retrieval_refs=choose(d,'retrieval_refs','response_refs',default=[]),
        content_sha256=choose(d,'content_sha256','source_sha256','body_sha256',default=None),
        checked_utc_basis=choose(d,'checked_utc_basis',default='recorded direct retrieval or source review time'),
        origin_file=origin,origin_line=line)

rows=[]
seen_ids=set()
for name in FILES:
    path=ROOT/name
    if not path.exists():continue
    for line,s in enumerate(path.read_text().splitlines(),1):
        if not s.strip():continue
        r=normalize(json.loads(s),name,line)
        if r['source_id'] in seen_ids:raise ValueError('Repeated source ID '+r['source_id'])
        seen_ids.add(r['source_id']);rows.append(r)

credited={}
for r in rows:
    if r['allocation']=='background' or not r['direct_open'] or r['duplicate_of']:continue
    if r['work_id'] in credited:
        r['duplicate_of']=credited[r['work_id']]
        continue
    credited[r['work_id']]=r['source_id'];r['counts_in_minimum']=True

with (ROOT/'sources.jsonl').open('w') as f:
    for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
counts=Counter(r['allocation'] for r in rows if r['counts_in_minimum'])
all_unique={r['work_id'] for r in rows if r['direct_open'] and not r['duplicate_of']}
summary={'ledger_rows':len(rows),'direct_unique_work_ids':len(all_unique),
    'minimum_credited_works':sum(counts.values()),'allocation_counts':dict(counts),
    'allocation_targets':{'user_request':4,'catalog_rule':4,'supplier_doc':8,'release_test':4,'crossfield':4},
    'credited_source_ids':[r['source_id'] for r in rows if r['counts_in_minimum']],
    'failed_rows':sum(not r['direct_open'] for r in rows),
    'credit_rule':'Conservative fixed24: four requests, four catalog/rule works, eight supplier works, four release/test works, four crossfield records. Extra AWS feature pages, homepage, Compose and integration tests remain directly read background. Root README routing/arrival is one work.',
    'note':'A source credit is not a successful candidate or independent implementation. Same work cannot fill multiple categories. Screened but unselected issues remain background.'}
(ROOT/'evidence/source-counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
