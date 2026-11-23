"""AF-RES-060 deterministic ranking replay; no HTTP, no provider execution."""
from pathlib import Path
from datetime import datetime, timezone
import csv, json, re, hashlib, argparse

P = Path(__file__).resolve().parent

def readcsv(path):
    return list(csv.DictReader(path.open(encoding='utf-8', newline='')))

def writecsv(path, rows, columns=None):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns or list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)

def norm(s):
    return re.sub(r'\s+', ' ', s.casefold().replace('-', ' ')).strip()

def terms_for(case_id, mode, vocab):
    out=[]; seen=set()
    for v in vocab:
        if v['case_id'] != case_id or v['method'] not in (['L,V'] if mode=='L' else ['L,V','V']):
            continue
        n=norm(v['target_term'])
        if n not in seen:
            out.append({'mapping_id':v['mapping_id'],'term':v['target_term'],'normalized':n});seen.add(n)
    return out

def rank(req, terms, catalog, features=None, feature_limit=3):
    out=[];seen=set()
    for row in catalog:
        if row['family'] != req['domain']:
            continue
        fields=json.loads(row['search_fields_json'])
        if features is not None:
            fields+=features.get(row['catalog_id'],[])[:feature_limit]
        hits=[]
        for t in terms:
            for i,f in enumerate(fields):
                if re.search(r'(?<!\w)'+re.escape(t['normalized'])+r'(?!\w)',norm(f)):
                    hits.append({'mapping_id':t['mapping_id'],'term':t['term'],'field_index':i,'field_value':f,'field_kind':'F0' if i<len(json.loads(row['search_fields_json'])) else 'F1'})
        if hits and row['destination_url'] not in seen:
            out.append({'catalog_id':row['catalog_id'],'posted_rank':int(row['posted_rank']),'url':row['destination_url'],'hits':hits})
            seen.add(row['destination_url'])
    return out

def baseline():
    inp=P/'inputs/af-res-056';vocab=readcsv(inp/'vocabulary.csv');cat=readcsv(inp/'catalog.csv')
    reqs={r['case_id']:r for r in json.loads((inp/'requirements.json').read_text())}
    rows=[]
    for expected in readcsv(inp/'matches.csv'):
        actual=rank(reqs[expected['case_id']],terms_for(expected['case_id'],expected['method'],vocab),cat)
        old=json.loads(expected['all_matches_json'])
        for x in actual:
            for h in x['hits']:h.pop('field_kind')
        rows.append({'comparison_id':expected['comparison_id'],'expected_ids':[x['catalog_id'] for x in old],'actual_ids':[x['catalog_id'] for x in actual],'complete_match_rows_equal':old==actual,'terms_equal':json.loads(expected['terms_json'])==terms_for(expected['case_id'],expected['method'],vocab)})
    result={'utc':datetime.now(timezone.utc).isoformat(),'rows':len(cat),'schema_rows':sum(x['family']=='JSON Schema' for x in cat),'ld_rows':sum(x['family']=='JSON-LD' for x in cat),'comparisons':len(rows),'all_equal':all(x['complete_match_rows_equal'] and x['terms_equal'] for x in rows),'checks':rows,'execution_scope':'literal match/order replay only; not implementation behavior'}
    (P/'evidence/baseline-replay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
    assert result['all_equal']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline-only',action='store_true');args=ap.parse_args()
    baseline()
    if args.baseline_only:return
    reqs=json.loads((P/'requirements.json').read_text());vocab=readcsv(P/'vocabulary.csv');cat=readcsv(P/'inputs/af-res-056/catalog.csv');fs=readcsv(P/'features.csv')
    features={x['catalog_id']:json.loads(x['added_features_json']) for x in fs}
    assert len(reqs)==12 and len(cat)==62 and len(fs)==62
    matches=[];slots=[];sens=[]
    for r in reqs:
        for f in ['F0','F1']:
            for m in ['L','V']:
                cid=r['case_id']+'-'+m+'-'+f; ts=terms_for(r['case_id'],m,vocab);performed=r.get('status','selected')=='selected'
                all_=rank(r,ts,cat,None if f=='F0' else features) if performed else []
                reason=('not_run_missing_requirement' if not performed else 'observed_no_match' if not all_ else 'matched_pool_exhausted' if len(all_)<3 else '')
                matches.append({'comparison_id':cid,'case_id':r['case_id'],'layer':r['layer'],'query':m,'fields':f,'status':'ranked' if performed else 'not_run','terms_json':json.dumps(ts,ensure_ascii=False),'catalog_rows':sum(c['family']==r['domain'] for c in cat),'all_matches_json':json.dumps(all_,ensure_ascii=False),'total_matches':len(all_) if performed else '', 'top3_ids_json':json.dumps([x['catalog_id'] for x in all_[:3]]),'top3_original_ranks_json':json.dumps([x['posted_rank'] for x in all_[:3]]),'unfilled_slots':3-len(all_[:3]),'unfilled_reason':reason})
                for n in range(1,4):
                    x=all_[n-1] if len(all_)>=n else None
                    slots.append({'slot_id':cid+'-S'+str(n),'comparison_id':cid,'case_id':r['case_id'],'layer':r['layer'],'query':m,'fields':f,'slot':n,'catalog_id':x['catalog_id'] if x else '', 'posted_rank':x['posted_rank'] if x else '', 'destination_url':x['url'] if x else '', 'display_status':'filled' if x else 'not_run' if not performed else 'empty','empty_reason':'' if x else reason,'judgment':'pending_path_observation' if x else 'not_run' if not performed else 'not_applicable_empty','displacement':''})
                if performed:
                    one=rank(r,ts,cat,None if f=='F0' else features,1)
                    sens.append({'comparison_id':cid,'top4': [x['catalog_id'] for x in all_[:4]],'one_feature_all':[x['catalog_id'] for x in one],'one_feature_top3':[x['catalog_id'] for x in one[:3]]})
    writecsv(P/'matches.csv',matches);writecsv(P/'slots.csv',slots)
    (P/'evidence/ranking-sensitivity.json').write_text(json.dumps(sens,ensure_ascii=False,indent=2)+'\n')
    plan={}
    for row in matches:
        for candidate_rank, hit in enumerate(json.loads(row['all_matches_json']), 1):
            key=row['case_id']+'::'+hit['catalog_id']
            entry=plan.setdefault(key,{'case_id':row['case_id'],'catalog_id':hit['catalog_id'],'destination_url':hit['url'],'comparison_ids':[], 'ranks':{},'paths':['P1 first README window','P2 first README + first information link','P3 first README + second information link'],'maximum_documents_each':2,'stage':'frozen_before_destination_condition_judgment'})
            entry['comparison_ids'].append(row['comparison_id'])
            entry['ranks'][row['comparison_id']]=candidate_rank
    (P/'evidence/path-plan.json').write_text(json.dumps({'cases':list(plan.values()),'ranking_inputs_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['requirements.json','vocabulary.csv','features.csv','matches.csv']},'logical_scope':'all unique case/provider matches, including newly entered lower ranks and displaced F0 candidates; primary top3 and rank4 sensitivity remain separated'},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'comparisons':len(matches),'slots':len(slots),'filled_slots':sum(x['display_status']=='filled' for x in slots),'unique_case_provider_all':len(plan)},ensure_ascii=False))

if __name__=='__main__':main()
