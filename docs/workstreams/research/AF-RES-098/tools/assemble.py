"""Normalize the three independent audits without changing sealed predictions."""
import collections
import csv
import hashlib
import json
import pathlib
import urllib.parse

ROOT=pathlib.Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def first(row,*keys):
    return next((row[k] for k in keys if row.get(k)), '')

def source_family(row):
    u=row['url']; old=row['lineage']
    if 'asciicast' in u:return 'CAL-asciicast'
    if 'JamesIves' in u:return 'RULE-github-pages-deploy-action'
    if 'sphinx-gallery' in u:return 'RULE-sphinx-gallery'
    if 'sphinx-doc' in u:return 'RULE-sphinx-html-builder'
    if 'pkgdown' in u and 'ggplot2' not in u:return 'RULE-pkgdown'
    if 'CPython' in old:return 'PUB-cpython'
    if old.startswith('ggplot2'):return 'PUB-ggplot2'
    if old=='Matplotlib documentation':return 'PUB-matplotlib'
    return {'CD-COLE':'PUB-cole-epub','CD-CORPUS':'DATA-data-citation-corpus',
            'CD-EPUB-RULE':'RULE-epub','CD-DATACITE-SCHEMA':'RULE-datacite',
            'CD-ZENODO-RULE':'RULE-zenodo'}.get(old,old)

def assemble():
    cases={x['case_id']:x for x in json.loads((ROOT/'freeze.json').read_text())['cases']}
    rows=[]
    for group in ['matplotlib','cpython','ggplot2']:
        for x in read_csv(ROOT/'evidence'/group/'lineage.csv'):
            c=cases[x['case_id']]; new=x['version']==c['new_version']
            row={'case_id':x['case_id'],'project':c['project'],'edition':'new' if new else 'old',
                 'version':x['version'],'release_url':c['new_release_url'] if new else c['old_release_url'],
                 'source_url':x['source_url'],'source_sha256':first(x,'source_sha256','source_sha'),
                 'body_url':x['body_url'],'body_sha256':x['body_sha256'],
                 'section_locator':first(x,'body_locator','section_locator','section')+(' L'+x['section_line'] if x.get('section_line') else ''),
                 'literal_reference':first(x,'literal_reference','reference_uri','actual_ref'),
                 'base_uri':x['base_uri'],'payload_url':first(x,'payload_url','resolved_payload_uri'),
                 'payload_mime':first(x,'payload_mime','payload_mime_http'),
                 'payload_bytes':int(x['payload_bytes']),'payload_sha256':x['payload_sha256'],
                 'P_included':first(x,'included_P','P_included'),
                 'U_section_uses':first(x,'used_U','U_section_uses'),
                 'G_build_generated':first(x,'generated_G','G_this_build_generated','G_generated_this_build'),
                 'publication_record_url':first(x,'publication_url','publication_record_url','package_url'),
                 'generation_record_url':'',
                 'build_rule_urls':first(x,'build_rule_urls','generation_record_url'),
                 'limitation':first(x,'limitation','generation_limit','limits'),
                 'evidence':first(x,'evidence') or 'evidence/'+group+'/audit.json'}
            rows.append(row)
    order={x:i for i,x in enumerate(['MP1','MP2','PY1','PY2','GG1','GG2'])}
    rows.sort(key=lambda x:(order[x['case_id']],x['edition']=='new'))
    assert len(rows)==12 and len({(x['case_id'],x['version']) for x in rows})==12
    for cid,c in cases.items():
        assert {x['version'] for x in rows if x['case_id']==cid}=={c['old_version'],c['new_version']}
    for r in rows:
        assert all(r[k] for k in ['source_url','source_sha256','body_url','body_sha256','literal_reference','payload_url','payload_mime','payload_sha256','publication_record_url'])
        assert all(r[k] in {'YES','NO','UNKNOWN'} for k in ['P_included','U_section_uses','G_build_generated'])
    with (ROOT/'lineage.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    sources=[]
    for group in ['matplotlib','cpython','ggplot2','cross-domain','calibration']:
        for line in (ROOT/'evidence'/group/'sources.jsonl').read_text().splitlines():
            s=json.loads(line);s['ledger_origin']='evidence/'+group+'/sources.jsonl'
            if not s.get('case_id') and group=='cpython':s['case_id']=['PY1','PY2']
            s['canonical_lineage']=source_family(s)
            s['counted_by_author']=s.get('counted',False)
            s['counted']=bool(s.get('counted',False))
            sources.append(s)
    ids=[x['id'] for x in sources];assert len(ids)==len(set(ids))
    seen={}; duplicates=[]
    for s in sources:
        if s['counted'] and s.get('sha256'):
            # Conservatively count identical received bytes once across the merged ledger.
            digest=s['sha256']
            if digest in seen:
                s['counted']=False;s['global_duplicate_of']=seen[digest]
                s['dedup_basis']+='; merged ledger identical SHA256: '+seen[digest]
                duplicates.append([s['id'],seen[digest]])
            else:seen[digest]=s['id']
        for k in ['id','q','case_id','url','utc','publisher','lineage','version','locator','observed','claim','limitations','dedup_basis']:
            assert s.get(k), (s['id'],k)
    (ROOT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    counted=[s for s in sources if s['counted']]
    cats=collections.Counter(s['category'] for s in counted)
    families=collections.Counter(s['canonical_lineage'] for s in counted)
    pred=read_csv(ROOT/'predictions.csv');assert len(pred)==6
    pairs=[]
    for p in pred:
        r=next(x for x in rows if x['case_id']==p['case_id'] and x['edition']=='new')
        expected=p['prediction_U'];actual=r['U_section_uses']
        verdict='UNASSESSABLE' if actual=='UNKNOWN' else 'HELD' if expected in {'HOLD','UNKNOWN'} else 'TRUE' if expected==actual else 'FALSE_ATTRIBUTION' if expected=='YES' else 'MISSED_CONNECTION'
        pairs.append({'case_id':p['case_id'],'prediction_U':expected,'observed_U':actual,'verdict':verdict})
    totals=collections.Counter(x['verdict'] for x in pairs)
    counts={'source_rows':len(sources),'unique_primary_sources':len(counted),'categories':dict(cats),
            'canonical_source_families':dict(families),'source_family_count':len(families),
            'selected_publication_dataset_lineages':['PUB-matplotlib','PUB-cpython','PUB-ggplot2','PUB-cole-epub','DATA-data-citation-corpus'],
            'selected_publication_dataset_lineage_count':5,'calibration_lineages_excluded_from_new':1,
            'merged_same_byte_exclusions':duplicates,
            'minimums':{'all_primary':25,'example_bodies':10,'payloads':6,'publication_build_listing':5,'epub_spec_and_package':2,'data_rules_and_records':2},
            'observed_minimums':{'all_primary':len(counted),'example_bodies':cats['example_body'],
                                 'payloads':cats['payload']+cats['image_payload'],
                                 'publication_build_listing':sum(cats[k] for k in ['release_record','deployment_listing','publication_record','build_rule','distribution_record','build_record','publication']),
                                 'epub_spec_and_package':sum(s['category']=='epub' or s['canonical_lineage']=='RULE-epub' for s in counted),
                                 'data_rules_and_records':sum(s['canonical_lineage'] in {'DATA-data-citation-corpus','RULE-datacite','RULE-zenodo'} for s in counted)},
            'slots':len(rows),'pairs':pairs,'prediction_counts':dict(totals),'assessable_prediction_denominator':sum(x['verdict'] in ['TRUE','FALSE_ATTRIBUTION','MISSED_CONNECTION'] for x in pairs),
            'P':dict(collections.Counter(x['P_included'] for x in rows)),
            'U':dict(collections.Counter(x['U_section_uses'] for x in rows)),
            'G':dict(collections.Counter(x['G_build_generated'] for x in rows)),
            'limitations':'Unique source minimum is a conservative ledger count, not an independent experiment count. Empty job queries and calibration excluded. No human cost inference.'}
    for k,v in counts['minimums'].items():assert counts['observed_minimums'][k]>=v,(k,counts['observed_minimums'][k],v)
    (ROOT/'evidence/counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:counts[k] for k in ['source_rows','unique_primary_sources','source_family_count','observed_minimums','slots','prediction_counts','P','U','G']},ensure_ascii=False,indent=2))

if __name__=='__main__':assemble()
