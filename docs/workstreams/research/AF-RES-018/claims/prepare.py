#!/usr/bin/env python3
"""Create extraction packets and combine literal-provenance claim inventories.

Packet IDs conceal condition labels; raw answer formatting may still suggest a
condition. Extractors enumerate assertions, not truth. Verification begins only
after the combined pool and seeded sample are committed.
"""
from pathlib import Path
import argparse,collections,hashlib,json,random
ROOT=Path(__file__).resolve().parents[1]
def load(p,default=None):
    f=ROOT/p;return json.loads(f.read_text()) if f.exists() else default
def save(p,d):
    f=ROOT/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prepare():
    packets=[];key={}
    for d in load('questions/dispatch.json')['order']:
        run=load(d['output']);assert run and len(run.get('checks',[]))==3,('unfinished',d['output'])
        run_id='X'+hashlib.sha256(('18018|'+d['condition']+'|'+d['qid']).encode()).hexdigest()[:16]
        key[run_id]={'condition':d['condition'],'qid':d['qid'],'source_file':d['output'],
                     'raw_response_sha256':hashlib.sha256(run['raw_response'].encode()).hexdigest()}
        packets.append({'run_id':run_id,'qid':d['qid'],'raw_response':run['raw_response'],
                        'candidate_links':[{'name':c['name'],'url':c.get('url'),'evidence_opened':c.get('evidence_opened')} for c in run['candidates']],
                        'opened_urls':[r['url'] for r in run['opened_documents']]})
    rng=random.Random(18018);rng.shuffle(packets);manifest=[]
    for start in range(0,len(packets),8):
        number=start//8+1;file=f'claims/extract-inputs/batch-{number:02d}.json';runs=packets[start:start+8]
        save(file,{'rule':'Read claims/RULES.md. Exhaustively enumerate atomic candidate facts in the frozen raw_response, without checking truth. Exclude question restatements, recommendations and explicit uncertainty from facts; inventory uncertainties separately. Give an exact source_quote for every item. Map an actually supplied URL when present, distinguishing homepage_only, claim_specific and none. Do not infer facts from external knowledge or from the query/document logs. Deduplicate repeated facts within a run. Return reviewed_runs, facts, uncertainties and omissions/limits. No gold or other files.','runs':runs})
        manifest.append({'batch':number,'input':file,'output':f'claims/extracted/batch-{number:02d}.json','run_ids':[r['run_id'] for r in runs]})
    save('claims/extraction-key.json',key);save('claims/extraction-manifest.json',manifest)
    print(json.dumps({'runs':len(packets),'batches':len(manifest)}))
def combine():
    key=load('claims/extraction-key.json');manifest=load('claims/extraction-manifest.json')
    pool=[];uncertainty=[];coverage=[]
    for batch in manifest:
        extracted=load(batch['output']);assert extracted,('missing extraction',batch['output'])
        reviewed=extracted['reviewed_runs'];reviewed=[r['run_id'] if isinstance(r,dict) else r for r in reviewed]
        assert set(reviewed)==set(batch['run_ids']),('unreviewed run',batch['output'])
        for field,target in [('facts',pool),('uncertainties',uncertainty)]:
            for item in extracted.get(field,[]):
                k=key[item['run_id']];assert item['run_id'] in batch['run_ids']
                raw=load(k['source_file'])['raw_response']
                assert hashlib.sha256(raw.encode()).hexdigest()==k['raw_response_sha256']
                assert item.get('source_quote') and item['source_quote'] in raw,('nonliteral extraction',item)
                assert item.get('candidate') and item.get('reference_kind') in ['homepage_only','claim_specific','none'],item
                if item['reference_kind']=='none':assert not item.get('supplied_urls'),item
                target.append({**item,**k,'extractor':extracted.get('extractor'),'extraction_file':batch['output']})
        coverage.append({'batch':batch['batch'],'reviewed_runs':reviewed,'facts':len(extracted.get('facts',[])),
                         'uncertainties':len(extracted.get('uncertainties',[])),
                         'omissions_or_limits':extracted.get('omissions_or_limits',[])})
    seen=[r for b in coverage for r in b['reviewed_runs']];assert len(seen)==len(set(seen))==len(key)
    save('claims/pool.json',pool);save('claims/uncertainty.json',uncertainty);save('claims/extraction-coverage.json',coverage)
    print(json.dumps({'facts':len(pool),'uncertainty_items':len(uncertainty),'reviewed_runs':len(seen),
                      'facts_by_condition':dict(collections.Counter(c['condition'] for c in pool))}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--combine',action='store_true');a=p.parse_args()
    if a.prepare:prepare()
    if a.combine:combine()
