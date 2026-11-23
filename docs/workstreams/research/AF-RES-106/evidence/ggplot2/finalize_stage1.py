from collect import *
from concurrent.futures import ThreadPoolExecutor

rows=json.loads((D/'stage1-frame.json').read_text())
eligible=sorted((r for r in rows if r['eligible']=='YES'),key=lambda x:(x['hash_sha256'],x['old_section_path']))
chosen=eligible[:4]
def get(r):
 b,rc=fetch('old-body-'+Path(r['page_path']).name,r['body_url'])
 assert sha(b)==r['body_sha256'] and gitsha(b)==r['body_blob']
 return r,b,rc
observations=[];ledger=[]
for r,b,rc in ThreadPoolExecutor(max_workers=4).map(get,chosen):
 p=Path(r['page_path']).stem
 r['direct_detail_read']='YES'
 r['body_receipt']='evidence/ggplot2/receipts/old-body-'+Path(r['page_path']).name+'.json'
 loc={'start_line':r['section_start_line'],'end_line':r['section_end_line'],'first_image_line':r['first_image_line'],'fragment':r['old_fragment'],'first_image_attrs':r['old_img_tag'],'first_example_code':r['first_example_code'],'base_tags':r['old_base_tags'],'picture_count':r['old_picture_count'],'svg_count':r['old_svg_count']}
 savejson('old-detail-'+p+'.json',loc)
 observations.append({'page_path':r['page_path'],'raw_read_utc':rc['accessed_utc'],'original_html_read':'Exact original h2 id and first plotted code/image tag reviewed, not a search preview. Remote bytes rechecked against archive and Git blob.','purpose_visual':r['visual_purpose'],'purpose_api':r['method_purpose'],'executable_runtime':'미확인; code was read, not run','receipt':r['body_receipt'],'detail':'evidence/ggplot2/old-detail-'+p+'.json'})
 ledger.append({'id':'GG106-OLD-BODY-'+p,'questions':['Q1','Q2','Q3'],'cases':[],'original_url':r['body_url'],'immutable_url':r['body_url'],'preserved_location':'evidence/ggplot2/old-detail-'+p+'.json','accessed_utc':rc['accessed_utc'],'publisher':'tidyverse/ggplot2 authors','work_lineage':'ggplot2 logical example '+r['page_path'],'edition':'3.4.0','location':loc,'fingerprints':{'git_blob':r['body_blob'],'sha256':r['body_sha256']},'observed':r['visual_purpose']+' / '+r['method_purpose'],'supports':'Old eligible logical example has explanation, executable code and linked first plot at actual DOM id.','refutes':'Page title alone is not the first example API; scale_shape/stat_unique first examples use default geom_point.','limits':'Static HTML and code only; actual execution/display and historical generation are 미확인. New edition unopened.','status':'신규','category':'example_body','countable':True,'count_reason':'One distinct old logical example, same work across editions will count once; archive itself is not also counted.','receipt':r['body_receipt']})
for r in rows:
 r['purpose_visual']=r.get('visual_purpose','')
 r['purpose_api']=r.get('method_purpose','')
 r['author_source_path']=r.get('author_source_links','')
 r.setdefault('body_receipt','evidence/ggplot2/old-archive-receipt.json')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (D/'stage1-frame.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
savejson('stage1-frame.json',rows)
savejson('stage1-original-html-review.json',{'reviewed_utc':utc(),'selection':'First four remaining OLD logical examples by AF106 hash only; minimum-material controls, not final main strata','observations':observations,'separate_reviewer':False})
summary=json.loads((D/'stage1-summary.json').read_text());summary.update(direct_detail_read_count=4,detail_review_paths=[r['page_path'] for r in chosen],completed_utc=utc(),old_source_missing_but_eligible=[r['page_path'] for r in eligible if not r.get('source_blob')],additional_source_download_examples=0,code_only_excluded_note='The 21 Examples pages without plot have no independently linked executable-example download. Generic author R/Rd source links are not counted as runnable download examples.')
savejson('stage1-summary.json',summary)
for key,name,url in [('old-archive','old-archive-receipt.json','https://codeload.github.com/tidyverse/ggplot2/tar.gz/'+OLD),('old-tree','old-tree-receipt.json',API+'git/trees/'+OLD+'?recursive=1'),('old-source-tree','receipts/old-source-tree.json.json',API+'git/trees/'+OSRC+'?recursive=1')]:
 rc=json.loads((D/name).read_text())
 ledger.append({'id':'GG106-INHERITED-'+key,'questions':['Q1','Q2'],'original_url':url,'immutable_url':url,'preserved_location':'evidence/ggplot2/'+name,'accessed_utc':rc.get('accessed_utc',rc.get('utc_end')),'publisher':'tidyverse/ggplot2','work_lineage':'ggplot2 3.4.0 fixed publication/source event inherited from AF-RES-102','edition':'3.4.0','fingerprints':{'sha256':rc['sha256']},'observed':'Complete fixed old archive/tree reacquired and compared; machine-scanned195 reference HTML; not195 directly read independent sources.','supports':'Explicit complete old path denominator','limits':'No execution or new-edition information','status':'계승','category':'publication_record','countable':False,'count_reason':'Same inherited fixed publication/source event; reacquisition is not new research material.'})
(D/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in ledger))
print(json.dumps(summary,ensure_ascii=False,indent=2))
