"""List-only prediction; never open a new example or asset blob."""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import urllib.request

OUT=Path(__file__).resolve().parent
CACHE=Path('/tmp/af098-ggplot2')
API='https://api.github.com/repos/tidyverse/ggplot2'
receipts=[]

def fetch(sid,url):
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    with urllib.request.urlopen(url,timeout=45) as r:
        b=r.read()
        receipts.append({'id':sid,'url':url,'utc':stamp,'status':r.status,
            'final_url':r.url,'mime':r.headers.get('Content-Type'),'bytes':len(b),
            'sha256':hashlib.sha256(b).hexdigest(),'redirects':[] if r.url==url else [{'from':url,'to':r.url,'intermediate_statuses':'not captured'}]})
    (CACHE/(sid+'.bin')).write_bytes(b)
    return json.loads(b)

tag=fetch('GG-NEW-TAG-META',API+'/git/ref/tags/v3.5.1')
tag_sha=tag['object']['sha']
assert tag['object']['type']=='commit'
commits=fetch('GG-NEW-DEPLOY-DATES',API+'/commits?sha=gh-pages&since=2024-04-23T00:00:00Z&until=2024-04-23T23:59:59Z&per_page=100')
# Project only publication commit SHA/date. Do not display or use commit messages,
# trees, patches, authors' bodies, or workflow records in making the prediction.
dates=sorted([{'sha':x['sha'],'utc':x['commit']['committer']['date']} for x in commits],key=lambda x:x['utc'])
assert len(commits)<100, 'date listing may be incomplete'
publication=[x for x in dates if x['utc']>='2024-04-23T10:21:20Z'][0]
tree_url=API+'/git/trees/'+publication['sha']+'?recursive=1'
tree=fetch('GG-NEW-TREE-LIST',tree_url)
paths=[x['path'] for x in tree['tree'] if x['type']=='blob']
complete=not tree.get('truncated',True)
rows=[]
for case in json.loads((OUT/'selected.json').read_text()):
    path=case['old_resource_path']
    exact=paths.count(path)
    basename=path.rsplit('/',1)[-1]
    others=[p for p in paths if p!=path and p.rsplit('/',1)[-1]==basename]
    pred='UNKNOWN' if not complete else 'YES' if exact==1 else 'HOLD' if exact>1 or others else 'NO'
    rows.append({'case_id':case['case_id'],'project':'ggplot2','old_release':'3.5.0','new_release':'3.5.1',
      'logical_resource':case['purpose'],'old_section_uri':case['old_section_uri'],'old_asset_path':path,
      'new_listing_url':tree_url,'new_snapshot_sha':publication['sha'],'listing_utc':receipts[-1]['utc'],
      'listing_complete':complete,'tree_entries':len(tree['tree']),'exact_path_count':exact,
      'other_same_basename_paths':json.dumps(others),'sealed_prediction':pred,
      'prediction_target':'Same next-edition section uses the fixed logical resource',
      'exposure':'Only release tag object SHA, publication SHA/date projection, and deployed path names inspected. Blob SHA/size not used. New bodies/assets/CI not opened.',
      'edition_identity_limit':'First gh-pages snapshot on release date at/after published_at; exact 3.5.1 source/deploy mapping deliberately unverified before prediction.'})
with (OUT/'predictions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'stage1_commit':'c0d31ca194e47fe69bc51dc0ef85d6e346b50774','new_tag_source_sha':tag_sha,
 'publication_date_candidates':dates,'selected_snapshot':publication,
 'snapshot_rule':'first gh-pages publication commit timestamp at or after v3.5.1 published_at on 2024-04-23',
 'complete':complete,'tree_entries':len(tree['tree']),'file_paths':len(paths),
 'metadata_documents_opened':2,'list_documents_opened':1,'total_requests':3,
 'contents_not_read':['new example HTML','new PNG payloads','new pkgdown.yml','new source examples','workflow or CI logs','deploy commit messages'],
 'automatic_metadata_not_used':['blob SHA','size','tree URL per entry'],
 'prior_metadata_exposure':'Release list and release notes used only for dates in stage1; exact selected example changes unseen.',
 'predictions':rows,'receipts':receipts}
(OUT/'stage2-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (OUT/'sources.jsonl').open('a') as f:
    for r in receipts:
        obj={'id':r['id'],'q':['Q2'],'case_id':['GG1','GG2'],'url':r['url'],'fixed_url':r['url'] if publication['sha'] in r['url'] or '/tags/v3.5.1' in r['url'] else None,
          'utc':r['utc'],'publisher':'tidyverse/ggplot2 maintainers','lineage':'ggplot2 documentation','version':'3.5.1 publication candidate',
          'locator':'projected SHA/date fields' if r['id']!='GG-NEW-TREE-LIST' else 'tree[].path, type; truncated',
          'observed':('tag SHA '+tag_sha if r['id']=='GG-NEW-TAG-META' else json.dumps(dates) if r['id']=='GG-NEW-DEPLOY-DATES' else f'complete={complete}; entries={len(tree["tree"])}; reference/aes-1.png count={paths.count("reference/aes-1.png")}; reference/aes_colour_fill_alpha-1.png count={paths.count("reference/aes_colour_fill_alpha-1.png")}'),
          'claim':'Path-only prediction input; does not establish section use or byte generation.',
          'limitations':'Snapshot identity selected by date is not yet corroborated with its source/deploy message; blob metadata not used.',
          'counted':True,'dedup_basis':'Distinct publication metadata/list response; one listing is one source, not per member.',
          'category':'deployment_listing' if r['id']=='GG-NEW-TREE-LIST' else 'release_record',
          'sha256':r['sha256'],'bytes':r['bytes'],'receipt_id':r['id']}
        f.write(json.dumps(obj,ensure_ascii=False)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
