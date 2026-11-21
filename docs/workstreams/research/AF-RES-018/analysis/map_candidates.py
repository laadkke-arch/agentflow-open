#!/usr/bin/env python3
"""Prepare condition-hidden entity matching; preserve every manual mapping decision.

Exact names and exact canonical URLs suggest identity, not relevance. All proposed
matches and nonmatches still require a recorded review. Check probes are excluded
from the discovery pool used for retrieval metrics.
"""
from pathlib import Path
import argparse,collections,hashlib,json,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
def load(p,default=None):
    f=ROOT/p;return json.loads(f.read_text()) if f.exists() else default
def save(p,d):
    f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def name_key(s):return re.sub(r'[^\w]+',' ',str(s).casefold(),flags=re.UNICODE).strip()
def url_key(s):
    if not s:return None
    u=urllib.parse.urlsplit(s);host=u.netloc.casefold().removeprefix('www.')
    return urllib.parse.urlunsplit(('',host,u.path.rstrip('/'),u.query,''))
def rid(q,c,i):return 'R'+hashlib.sha256(f'18018|{q}|{c}|discovery|{i}'.encode()).hexdigest()[:16]
def material(available=False):
    gold=load('gold/answers.json');byq=collections.defaultdict(list)
    for g in gold:byq[g['query_id']].append(g)
    rows=[];key={}
    for dispatch in load('questions/dispatch.json')['order']:
        run=load(dispatch['output'])
        if not run or len(run.get('checks',[]))!=3:
            if available:continue
            raise AssertionError(('incomplete run',dispatch['output']))
        q=dispatch['qid'];cond=dispatch['condition']
        for i,c in enumerate(run['candidates']):
            row_id=rid(q,cond,i);names={g['entity_id'] for g in byq[q] if name_key(g['candidate'])==name_key(c['name'])}
            urls={g['entity_id'] for g in byq[q] if url_key(c.get('url')) and url_key(g.get('candidate_url'))==url_key(c['url'])}
            candidates={g['entity_id']:{'entity_id':g['entity_id'],'name':g['candidate'],'url':g.get('candidate_url')} for g in byq[q]}
            rows.append({'row_id':row_id,'qid':q,'name':c['name'],'url':c.get('url'),
                         'application_scope':c.get('application_scope'),
                         'reason':c.get('reason'),'caveat':c.get('constraints_or_caveat'),
                         'exact_name_suggestions':sorted(names),'exact_url_suggestions':sorted(urls),
                         'gold_entity_options':sorted(candidates.values(),key=lambda g:g['entity_id'])})
            key[row_id]={'condition':cond,'qid':q,'rank':c['rank'],'source_file':dispatch['output']}
    return rows,key
def main(prepare,finalize,available):
    rows,key=material(available)
    if prepare:
        rows.sort(key=lambda r:(r['qid'],r['row_id']))
        save('analysis/mapping-review-input.json',{'rule':'Identify the same named entity or explicitly included component. Do not infer relevance. Record empty matches for unjudged entities. Keep versions and composite scope; do not match by vendor/category alone. Assign the same pool_entity string to identical proposed entities across rows, and distinct strings to distinct combinations. No condition or answer grade supplied.','rows':rows})
        print(json.dumps({'rows':len(rows),'complete_runs':len({r['source_file'] for r in key.values()}),'partial':available}))
    if finalize:
        assert not available,'Final mapping requires complete runs'
        decisions=load('analysis/mapping-decisions.json');assert decisions is not None
        assert set(decisions)=={r['row_id'] for r in rows},'Missing or extra manual identity decisions'
        result=[]
        for r in rows:
            d=decisions[r['row_id']];options={g['entity_id'] for g in r['gold_entity_options']}
            assert set(d['gold_entity_ids'])<=options,r['row_id']
            assert d.get('pool_entity') and d.get('reason') and d.get('reviewer'),r['row_id']
            result.append({'row_id':r['row_id'],**key[r['row_id']],'candidate':r['name'],'url':r['url'],
                           **d,'gold_entities_added_after_freeze':False})
        save('analysis/candidate-mapping.json',result)
        print(json.dumps({'mapped_rows':len(result),'unjudged_rows':sum(not r['gold_entity_ids'] for r in result)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--finalize',action='store_true');p.add_argument('--available',action='store_true');a=p.parse_args();main(a.prepare,a.finalize,a.available)
