#!/usr/bin/env python3
"""Conservative 3-URL re-presentation; preserves original slots/citations separately."""
import hashlib
import json
import pathlib
import urllib.parse
from collections import defaultdict
BASE=pathlib.Path(__file__).resolve().parents[1]

def rows(p):return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
def urlkey(url):
    return urllib.parse.urldefrag(url or '')[0]
def jl(p,rs):p.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rs))
raw=[]
for stream in ['arrow','cargo','jupyter']:
    raw+=rows(BASE/'streams'/stream/'returns.jsonl')
groups=defaultdict(list)
for r in raw:groups[(r['question_id'],r['route'])].append(r)
strict=[];audit=[]
for (qid,route),items in sorted(groups.items()):
    allowed=[]
    original_urls=set()
    for r in sorted(items,key=lambda x:x['rank']):
        for c in r.get('returned_citations',[]):
            if isinstance(c,dict) and c.get('url'):
                u=urlkey(c['url']);original_urls.add(u)
                if u not in allowed and len(allowed)<3:allowed.append(u)
    for r in sorted(items,key=lambda x:x['rank']):
        s=dict(r)
        keep=[c for c in r.get('returned_citations',[]) if isinstance(c,dict) and urlkey(c.get('url')) in allowed]
        dropped=[c for c in r.get('returned_citations',[]) if c not in keep]
        s['original_candidate_id']=r.get('candidate_id')
        s['original_returned_citations']=r.get('returned_citations',[])
        s['returned_citations']=keep;s['dropped_citations_by_url_budget']=dropped
        s['return_budget_variant']='strict_three_source_urls'
        if not keep and r.get('candidate_id'):
            s['candidate_id']=None;s['candidate_class']='empty';s['empty_reason']='3-URL final-link budget consumed by earlier original ranks; raw candidate retained in original_candidate_id'
        s['citation_verdict_requires_rescore']=bool(dropped)
        strict.append(s)
    audit.append({'question_id':qid,'route':route,'original_unique_urls':len(original_urls),'strict_unique_urls':len(allowed),'allowed_urls':allowed,'original_exceeded_three_urls':len(original_urls)>3})
jl(BASE/'returns-raw.jsonl',raw);jl(BASE/'returns.jsonl',strict)
(BASE/'evidence'/'return-url-budget.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'raw_slots':len(raw),'strict_slots':len(strict),'routes':len(groups),'raw_routes_over_three_urls':sum(r['original_exceeded_three_urls'] for r in audit)},indent=2))
