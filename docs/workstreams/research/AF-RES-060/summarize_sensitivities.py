"""Post-primary sensitivity accounting. No edits to frozen query/feature inputs."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv, json
from replay import rank, norm, terms_for

P=Path(__file__).resolve().parent
def rc(f): return list(csv.DictReader((P/f).open(encoding='utf-8')))
reqs=json.loads((P/'requirements.json').read_text()); vocab=rc('vocabulary.csv')
catalog=rc('inputs/af-res-056/catalog.csv'); features={x['catalog_id']:json.loads(x['added_features_json']) for x in rc('features.csv')}
matches=rc('matches.csv'); frozen=json.loads((P/'evidence/ranking-sensitivity.json').read_text())
verdict={(v['case_id'],v['catalog_id']):v['judgment'] for v in json.loads((P/'evidence/candidate-verdicts.json').read_text())}
index={m['comparison_id']:m for m in matches}
rows=[]
for s in frozen:
    m=index[s['comparison_id']]; original=json.loads(m['top3_ids_json'])
    for name,key,cap in [('top4','top4',4),('feature1','one_feature_top3',3)]:
        chosen=s[key]; counts=Counter(verdict[(m['case_id'],x)] for x in chosen)
        rows.append({'comparison_id':s['comparison_id'],'case_id':m['case_id'],'layer':m['layer'],'query':m['query'],'fields':m['fields'],'sensitivity':name,'slot_cap':cap,'displayed':chosen,'new_vs_primary_top3':[x for x in chosen if x not in original],'removed_vs_primary_top3':[x for x in original if x not in chosen], 'judgments':dict(counts),'accuracy':'not_estimable'})
summaries=[]
for name in ['top4','feature1']:
    for layer in ['existing_tuning','new_holdout','all']:
        for f in ['F0','F1']:
            for q in ['L','V']:
                rr=[r for r in rows if r['sensitivity']==name and (layer=='all' or r['layer']==layer) and r['fields']==f and r['query']==q]
                counts=Counter()
                for r in rr: counts.update(r['judgments'])
                summaries.append({'sensitivity':name,'layer':layer,'query':q,'fields':f,'requirements':len(rr),'nonempty_cases':sum(bool(r['displayed']) for r in rr),'filled_slots':sum(len(r['displayed']) for r in rr),'judgments':dict(counts)})

# These are intentionally invalid query expansions, never replacements for the main vocabulary.
# Split the inherited pipe list into separate terms only in this explicitly posthoc diagnostic.
unsafe=[]
for r in reqs:
    base=terms_for(r['case_id'],'V',vocab)
    variants={}
    if any(t['normalized']=='validation' for t in base):
        variants['derived_Validator']=[{'mapping_id':'SENS-Validator','term':'Validator','normalized':norm('Validator')}]
    held=[v for v in vocab if v['case_id']==r['case_id'] and v['method']=='withhold']
    additions=[]
    for v in held:
        for term in v['target_term'].split('|'):
            additions.append({'mapping_id':v['mapping_id'],'term':term.strip(),'normalized':norm(term)})
    if additions: variants['all_withheld_relations_as_if_synonyms']=additions
    for label,extra in variants.items():
        for f in ['F0','F1']:
            matched=rank(r,base+extra,catalog,None if f=='F0' else features)
            primary=rank(r,base,catalog,None if f=='F0' else features)
            new=[x['catalog_id'] for x in matched if x['catalog_id'] not in {y['catalog_id'] for y in primary}]
            unsafe.append({'case_id':r['case_id'],'variant':label,'fields':f,'added_terms':extra,'total_matches':len(matched),'top3':[x['catalog_id'] for x in matched[:3]],'new_vs_main_V':new,'outside_primary_pair_plan':[x for x in new if (r['case_id'],x) not in verdict],'truth_judgment':'not_performed_for_new_pairs','claim_limit':'Retrieval inflation and definition/role counterexamples only; not an observed implementation false-positive rate.'})

out={'created_utc':datetime.now(timezone.utc).isoformat(),'phase':'after frozen primary observations; no new provider source or execution','rows':rows,'summaries':summaries,'unsafe_query_expansion':unsafe,
 'literal_only':{'primary_partial_pairs':1,'sensitivity_partial_pairs':0,'complete_pairs_both':0,'affected_pair':'JS-6::SC-005','reason':'Only bar→id ordinary property-name transfer was inferred; no literal id execution in the permitted window.'},
 'audit_source_direct_link':{'status':'not_run','primary_original_destinations_unchanged':True,'reason':'Opening an editor source or changing first/second-link order would alter navigation, not just indexed fields. Outside-budget editor evidence is retained separately and no causal direct-link gain is claimed.'},
 'runtime_substitution':{'status':'semantic_counterexample_only','examples':['LD-6 R HTML script extraction is not a synonym for expansion/framing in another runtime.','LD-3 Ruby framing label does not establish the requested jsonld.js filtering and field preservation.'],'accuracy':'not_estimable; no new off-plan executions'},
 'cost_limit':'feature1 is a ranking truncation of already acquired three-name records, not a measured cheaper editing run; top4 reuses already observed lower-rank paths.'}
(P/'evidence/sensitivity-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cells':len(rows),'unsafe_cells':len(unsafe),'top4_added_slots':sum(len(x['new_vs_primary_top3']) for x in rows if x['sensitivity']=='top4'),'feature1_filled_slots':sum(len(x['displayed']) for x in rows if x['sensitivity']=='feature1')},ensure_ascii=False))
