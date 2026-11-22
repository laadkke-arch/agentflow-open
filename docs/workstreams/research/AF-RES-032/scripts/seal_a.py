"""Assemble A without dereferencing any sampled destination."""
from pathlib import Path
import json,csv,hashlib
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1]
inputs=[P/'collectors/python/references.jsonl',P/'collectors/offline/references.jsonl',P/'collectors/cran/final/references.jsonl']
rows=[]
for p in inputs:
    for ln in p.read_text().splitlines():
        r=json.loads(ln)
        def first(*ks):
            return next((r[k] for k in ks if k in r and r[k] is not None),None)
        r['artifact_url']=first('artifact_url','archive_url')
        r['artifact_id']=first('artifact_id','archive_id')
        r['artifact_sha256']=first('artifact_sha256','archive_sha256')
        r['member']=first('member','member_path')
        r['consumer_version']=first('consumer_version','consumer_edition')
        r['document_title']=first('document_title','consumer_document_title')
        r['base_url']=first('base_url','document_base_url')
        r['purpose']=first('purpose','click_purpose')
        r['purpose_type']=first('purpose_type','purpose_kind','purpose_class')
        r['minimum_success']=first('minimum_success','minimum_success_condition')
        r['intent_unknown']=first('intent_unknown','purpose_unknown')
        r['original_collector_path']=str(p.relative_to(P))
        r['publication_date_value']=first('publication_utc','consumer_release_date')
        r['purpose_known_at_seal']=True
        rows.append(r)
assert len(rows)==12,len(rows)
assert len({r['reference_id'] for r in rows})==12
assert len({(r['consumer_project'],r['consumer_version'],r['member']) for r in rows})==12
counts={x:sum(r['consumer_project']==x for r in rows) for x in {r['consumer_project'] for r in rows}}
assert len(counts)>=6 and max(counts.values())<=2,counts
assert all(sum(r['route']==x for r in rows)==6 for x in ['D','R'])
assert all(r['artifact_sha256'] and r['member_sha256'] and r['raw_href'] and r['purpose'] for r in rows)
at=datetime.now(timezone.utc).isoformat()
for r in rows:r['global_seal_prepared_at_utc']=at
rows.sort(key=lambda r:r['reference_id'])
out=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows)
(P/'references.jsonl').write_text(out)
(P/'evidence/a-sealed.jsonl').write_text(out)
frows=[]
for n,r in enumerate(sorted(rows,key=lambda r:(r['publication_date_value'],r['artifact_url'],r['member'])),1):
    frows.append({'sampling_order':n,'reference_id':r['reference_id'],'route':r['route'],'consumer_project':r['consumer_project'],'publication_date_value':r['publication_date_value'],'artifact_url':r['artifact_url'],'member':r['member'],'disposition':'selected','reason':'predeclared route quotas; date/archive/member order; project max2','collector':r['original_collector_path']})
with (P/'frame.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(frows[0]));w.writeheader();w.writerows(frows)
receipt={'prepared_at_utc':at,'A_references':12,'distinct_documents':12,'projects':counts,'routes':{'D':6,'R':6},'sha256':hashlib.sha256(out.encode()).hexdigest(),'inputs':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'all_current_and_future_outcomes_unopened':True,'method_deviation':'preseal project-order provisional R sample replaced with date-order before upstream exposure; evidence/preseal-order-correction.md','remote_seal':'pending; downstream reading prohibited until root remotely verifies commit'}
(P/'evidence/a-seal-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
