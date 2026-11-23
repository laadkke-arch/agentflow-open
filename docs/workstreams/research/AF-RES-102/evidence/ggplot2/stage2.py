from pathlib import Path
import sys,json,csv,hashlib,concurrent.futures
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D));import collect
ed=json.loads((D/'editions.json').read_text());fr=json.loads((D/'frame.json').read_text());gens=json.loads((D/'selected-general.json').read_text());eligible=[x for x in fr if x.get('eligible')]
items=[('new-tree-listing',collect.API+'git/trees/'+ed['new']['publication_sha']+'?recursive=1'),('new-source-tree-listing',collect.API+'git/trees/'+ed['new']['source_sha']+'?recursive=1')]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:read=list(ex.map(lambda x:collect.jget(*x),items))
nt,nr=read[0];st,sr=read[1]
paths={x['path'] for x in nt['tree']};source={x['path']:x for x in st['tree']}
complete=not nt.get('truncated');sourcecomplete=not st.get('truncated')
(D/'new-paths.json').write_text(json.dumps({'url':nr['url'],'accessed_utc':nr['accessed_utc'],'tree_sha':nt['sha'],'truncated':nt.get('truncated'),'paths':sorted(paths)},indent=2))
(D/'new-source-blobs.json').write_text(json.dumps({'url':sr['url'],'accessed_utc':sr['accessed_utc'],'tree_sha':st['sha'],'truncated':st.get('truncated'),'entries':[{'path':x['path'],'type':x['type'],'sha':x['sha']} for x in st['tree']]},indent=2))
signals=[]
for x in eligible:
 r=dict(x);p=x['old_resource_path'];sp=x['source_path']
 r.update(legacy_path_present=p in paths,old_source_path_present=sp in source,old_source_blob=x['source_blob'],new_source_blob=source.get(sp,{}).get('sha'),source_blob_changed=sp not in source or source[sp]['sha']!=x['source_blob'],new_page_path_present=x['page_path'] in paths,new_tree_complete=complete,new_source_tree_complete=sourcecomplete)
 signals.append(r)
signals.sort(key=lambda x:x['sorting_hash'])
selected=[];used=set()
for i,x in enumerate(gens,1):
 r=next(dict(t) for t in signals if t['section_path']==x['section_path']);r.update(case_id=f'GG-G{i}',stratum='general',slot=i);selected.append(r);used.add(r['section_path'])
for short,stratum,test in [('A','old_asset_absent',lambda r:not r['legacy_path_present'] and complete),('C','asset_retained_source_changed',lambda r:r['legacy_path_present'] and r['source_blob_changed'] and sourcecomplete)]:
 pool=[x for x in signals if x['section_path'] not in used and test(x)]
 for i in range(1,3):
  if i<=len(pool):
   r=dict(pool[i-1]);r.update(case_id=f'GG-{short}{i}',stratum=stratum,slot=i);selected.append(r);used.add(r['section_path'])
  else:selected.append({'case_id':f'GG-{short}{i}','project':'ggplot2','stratum':stratum,'slot':i,'vacant':True,'vacancy_reason':f'Only {len(pool)} eligible remaining cases meet this stratum within frozen first40; complete new deployment/source trees.'})
now=collect.utc()
for r in selected:
 if r.get('vacant'):
  r.update(prediction_U='미확인',prediction_utc=now,old_section_url='',new_provisional_section_url='',new_provisional_resource_url='')
 else:
  pred='YES' if r['legacy_path_present'] else 'NO' if complete else '미확인'
  r.update(vacant=False,prediction_U=pred,prediction_utc=now,old_section_url=collect.RAW+ed['old']['publication_sha']+'/'+r['section_path'],new_provisional_section_url=collect.RAW+ed['new']['publication_sha']+'/'+r['section_path'],new_provisional_resource_url=collect.RAW+ed['new']['publication_sha']+'/'+r['old_resource_path'],rule='Exact old resource relative path present => YES; absent in complete tree => NO; incomplete/ambiguous => 미확인.',alias_blind_spot='Does not inspect a renamed resource, embedded representation, purpose change or whether section actually references retained file.')
(D/'signals-stage2.json').write_text(json.dumps(signals,ensure_ascii=False,indent=2))
(D/'selected-stage2.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
keys=['case_id','project','stratum','slot','section_path','purpose','old_resource_path','source_path','old_source_blob','new_source_blob','legacy_path_present','source_blob_changed','new_page_path_present','prediction_U','prediction_utc','vacant','vacancy_reason','old_section_url','new_provisional_section_url','new_provisional_resource_url','sorting_hash','alias_blind_spot']
with (D/'predictions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(selected)
supp=[x for x in signals if x['section_path'] not in used][:20]
(D/'supplemental-order.json').write_text(json.dumps({'rule':'Remaining frozen first40, excluding selected main cases, same SHA256 ascending order, first20; supplemental only; do not reassign to main slots.','frozen_utc':now,'cases':[{k:r.get(k) for k in ['section_path','sorting_hash','purpose','old_resource_path','source_path','legacy_path_present','source_blob_changed']} for r in supp]},ensure_ascii=False,indent=2))
newreceipt=[nr,sr]
records=[]
for i, (r,key,category) in enumerate(zip(newreceipt,['new-tree-listing','new-source-tree-listing'],['deployment_listing','source_listing']),1):
 records.append({'source_id':f'GG-S2-{i:03}','questions':['Q2','Q3'],'cases':[x['case_id'] for x in selected],'original_url':r['url'],'fixed_url':r['url'],'accessed_utc':r['accessed_utc'],'publisher':'ggplot2 authors / tidyverse','lineage':'PUB-ggplot2','category':category,'version':'3.5.0','location':'recursive tree, truncated=false','sha256':r['sha256'],'observation':{'complete':complete if i==1 else sourcecomplete,'entries':len(nt['tree']) if i==1 else len(st['tree']),'visible_fields':'Path names/type only used for publication; path/type/blob used for source'},'claims_supported':['Complete path-level presence signal and source-change strata'],'claims_refuted':[],'limitations':'No next-version body/image/individual CI record inspected; path presence is only prediction input, not observed U.','countable':False,'duplicate_reason':'3.5.0 tree lineage inherited from 098; conservative exclusion from new-source minimum.','receipt':f'evidence/ggplot2/receipts/{key}.json'})
(D/'sources-stage2.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
report={'completed_utc':now,'new_deployment_tree_complete':complete,'new_source_tree_complete':sourcecomplete,'new_deployment_entries':len(nt['tree']),'new_source_entries':len(st['tree']),'frozen_frame_eligible':len(eligible),'old_resource_absent_count':sum(not x['legacy_path_present'] for x in signals),'retained_source_changed_count':sum(x['legacy_path_present'] and x['source_blob_changed'] for x in signals),'main_filled':sum(not x.get('vacant') for x in selected),'main_vacant':sum(bool(x.get('vacant')) for x in selected),'predictions':[{k:x.get(k) for k in ['case_id','section_path','prediction_U','vacant','vacancy_reason']} for x in selected],'exposure_log':[{'utc':nr['accessed_utc'],'url':nr['url'],'received_fields':'recursive Git tree paths/types/blob SHA/size; prediction code projected paths only; model did not view asset SHA/size','used':'exact relative path presence and next page names'},{'utc':sr['accessed_utc'],'url':sr['url'],'received_fields':'recursive source tree paths/types/blob SHA; no source body','used':'same-name man/*.Rd existence/blob comparison'}],'new_body_reads':0,'new_image_reads':0,'individual_ci_reads':0,'prior_exposure':'3.5.0 release/publication metadata was already in inherited 098 and stage1; main aes examples excluded.','ready_for_stage2_commit':True}
(D/'stage2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
