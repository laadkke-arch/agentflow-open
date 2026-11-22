"""Bounded exact-domain screen of already captured public discussion bodies.

This does not establish semantic citation absence, private knowledge, or causality.
It performs no network requests and never alters the sealed retrieval experiment.
"""
import json
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
DOMAINS=['spl.org','denverlibrary.org','multcolib.org','tpl.ca','hclib.org','vpl.ca',
    'ons.gov.uk','statcan.gc.ca','abs.gov.au','bls.gov','bea.gov','stats.govt.nz',
    'kingcounty.gov','mbta.com','ttc.ca','translink.ca','trimet.org','sfmta.com']
records=[];per=[];hits=[]
for rid in [f'R{i:02d}' for i in range(1,9)]:
    root=ROOT/'recipient/cache/outcomes'
    comments=[];inputs=[]
    for kind in ['issue_comments','review_comments','reviews']:
        files=sorted(root.glob(f'{rid}-{kind}-*.json'))
        assert files
        for path in files:
            rows=json.loads(path.read_text());assert isinstance(rows,list)
            comments+=rows
            inputs.append({'path':str(path.relative_to(ROOT)), 'sha256':sha256(path.read_bytes()).hexdigest(),'records':len(rows)})
    path=root/f'{rid}-pull.json';pull=json.loads(path.read_text())
    inputs.append({'path':str(path.relative_to(ROOT)),'sha256':sha256(path.read_bytes()).hexdigest(),'records':1})
    for row in comments+[pull]:
        body=(row.get('body') or '').lower()
        matching=[d for d in DOMAINS if d in body]
        if matching:hits.append({'recipient_id':rid,'html_url':row.get('html_url'),'domains':matching})
    per.append({'recipient_id':rid,'discussion_records':len(comments),
        'nonempty_discussion_bodies':sum(bool((r.get('body') or '').strip()) for r in comments),
        'current_pr_bodies':1,'inputs':inputs})
result={'scope':'Current PR body plus captured issue comments, review comments and review body field; all pages captured after retrieval seal a2ce15d10415c556574d1a65af77718a81052d01.',
    'matching':'lowercase body string; literal substring for any of 18 official issuer domains; includes subdomains but not institution aliases or semantic paraphrases.',
    'domains':DOMAINS,'per_recipient':per,
    'discussion_records':sum(x['discussion_records'] for x in per),
    'nonempty_discussion_bodies':sum(x['nonempty_discussion_bodies'] for x in per),
    'current_pr_bodies':8,'hits':hits,
    'not_established':['No prior private awareness','No indirect or paraphrased citation','No citation in every linked implementation file','No causal influence','No actual user adoption']}
assert result['discussion_records']==1315
assert result['nonempty_discussion_bodies']==913
(ROOT/'evidence/followup-citation-screen.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['discussion_records','nonempty_discussion_bodies','current_pr_bodies','hits']}))
