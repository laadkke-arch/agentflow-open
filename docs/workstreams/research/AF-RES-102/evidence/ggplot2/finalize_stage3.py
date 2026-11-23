from pathlib import Path
import sys,json,csv,hashlib,re,datetime,collections,difflib
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import collect
obs=json.loads((D/'audit-observations.json').read_text());full=json.loads((D/'cache/audit-full.json').read_text());selected=json.loads((D/'selected-stage2.json').read_text());ed=json.loads((D/'editions.json').read_text());frame=json.loads((D/'frame.json').read_text());bysection={x.get('section_path'):x for x in frame if x.get('eligible')};bycase={}
for x in obs:bycase.setdefault(x['case_id'],{})[x['edition']]=x
oldtree={x['path']:x for x in json.loads((D/'cache/old-tree').read_text())['tree']};newtree={x['path']:x for x in json.loads((D/'cache/new-tree-listing').read_text())['tree']}
def examples(s):
 i=s.find('\\examples{')
 if i<0:return ''
 start=i+len('\\examples{');depth=1
 for k,c in enumerate(s[start:],start):
  if c=='{':depth+=1
  elif c=='}':
   depth-=1
   if depth==0:return s[start:k]
 return s[start:]
def sourceblock(x):return examples((D/'cache'/(x['edition']+'-source-'+Path(x['source_path']).name)).read_text())
for x in obs:
 for p in x['payloads']:
  if p.get('cache'):
   b=(D/p['cache']).read_bytes();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();tree=oldtree if x['edition']=='old' else newtree
   p.update(git_blob_sha=h,published_tree_blob=tree.get(p['relative_path'],{}).get('sha'),blob_matches_publication=h==tree.get(p['relative_path'],{}).get('sha'))
 page=x['body_url'].split(x['publication_sha']+'/')[1]
 bodytext=(D/'cache'/(x['edition']+'-'+page.replace('/','_'))).read_text()
 x['body_displayed_version']=re.search('title="Released version">([^<]+)',bodytext).group(1)
 x['generator_version_label']=re.search('pkgdown</a> ([0-9.]+)',bodytext).group(1).rstrip('.')
 assert x['body_displayed_version']==x['version']
 assert all(p['blob_matches_publication'] for p in x['payloads'])
 x.update(P='YES',U='YES',G='미확인',legacy_path_P='YES',legacy_path_U='YES',purpose=bysection[x['body_url'].split(ed[x['edition']]['publication_sha']+'/')[1]+'#ref-examples']['purpose'],source_examples_block_sha256=hashlib.sha256(sourceblock(x).encode()).hexdigest(),static_reference_scope='Exact Examples enclosing div; every img/source/picture/script/object/embed/iframe examined; base tag resolved. Browser runtime not executed.',generation_limitation='Exact source+publication SHA runs/checks/status and bounded release-date runs return zero records; no actual job/output digest manifest binds these bytes to fresh generation. Not evidence of no historical generation.')
mainrows=[]
for s in selected:
 for edition in ['old','new']:
  if s.get('vacant'):
   mainrows.append({'case_id':s['case_id'],'project':'ggplot2','stratum':s['stratum'],'edition':edition,'version':ed[edition]['version'],'vacant':True,'P':'미확인','U':'미확인','G':'미확인','legacy_path_P':'미확인','limitation':s['vacancy_reason'],'evidence':'evidence/ggplot2/stage2.json'});continue
  x=bycase[s['case_id']][edition];p=x['payloads'][0]
  r={'case_id':s['case_id'],'project':'ggplot2','stratum':s['stratum'],'edition':edition,'version':x['version'],'vacant':False,'body_url':x['body_url'],'section_url':x['section_url'],'section_locator':x['section_locator'],'literal_reference':x['first_literal_reference'],'base_uri':x['base_url'],'payload_url':p['url'],'payload_mime':p['mime'],'payload_bytes':p['bytes'],'payload_sha256':p['sha256'],'P':x['P'],'U':x['U'],'G':x['G'],'legacy_path_P':'YES','legacy_path_U':'YES','source_url':x['source_url'],'source_sha256':x['source_sha256'],'publication_url':'https://github.com/tidyverse/ggplot2/commit/'+x['publication_sha'],'evidence':'evidence/ggplot2/audit.json','receipt':p['receipt'],'body_receipt':x['body_receipt'],'source_receipt':x['source_receipt'],'limitation':x['generation_limitation'],'purpose':x['purpose'],'width':p['width'],'height':p['height'],'first_image_line':x['first_image']['line'],'first_new_body_utc':x['body_utc'],'payload_utc':p['utc'],'source_examples_block_sha256':x['source_examples_block_sha256']}
  mainrows.append(r)
keys=['case_id','project','stratum','edition','version','vacant','body_url','section_url','section_locator','literal_reference','base_uri','payload_url','payload_mime','payload_bytes','payload_sha256','P','U','G','legacy_path_P','legacy_path_U','source_url','source_sha256','publication_url','evidence','receipt','body_receipt','source_receipt','limitation','purpose','width','height','first_image_line','first_new_body_utc','payload_utc','source_examples_block_sha256']
with (D/'lineage.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(mainrows)
manual={
'GG-G1':{'source_diff':'Only roxygen origin filename changes R/scale-expansion.r to .R; executable examples block identical.','visual':'Both PNGs show cylinder categories 4,6,8, bars at approximately 11,7,14 with no lower expansion and upper headroom. Purpose preserved; byte equality not claimed.'},
'GG-G2':{'source_diff':'R origin filename case, aesthetic hyperlinks, computed-variable descriptions and seealso link change; examples block and first geom_point recipe identical.','visual':'Both PNGs show same city/highway-mileage point-cloud structure; first figure is baseline geom_point, not the subsequent count-size figure.'},
'GG-C1':{'source_diff':'Only R/annotation-custom.r to .R in the roxygen-origin comment; examples block identical.','visual':'Both PNGs show rounded rectangle grob filling a blank Cartesian panel; same demonstration role.'},
'GG-C2':{'source_diff':'R origin filename case and computed-variable documentation formatting change; examples block identical.','visual':'Both PNGs show diamonds carat histogram. Some visible bin heights differ; the fixed first-example purpose and input code remain the same, not a claim of numeric-output identity.'}}
comparisons=[]
for case,v in bycase.items():
 a,b=v['old'],v['new'];pa,pb=a['payloads'][0],b['payloads'][0]
 c={'case_id':case,'page_path':a['body_url'].split(ed['old']['publication_sha']+'/')[1],'purpose_frozen':a['purpose'],'old_section':a['section_url'],'new_section':b['section_url'],'old_section_locator':a['section_locator'],'new_section_locator':b['section_locator'],'old_reference':a['first_literal_reference'],'new_first_reference':b['first_literal_reference'],'legacy_reference_count_new':b['legacy_reference_count'],'logical_U':'YES','legacy_resource_U':'YES','same_payload_bytes':pa['sha256']==pb['sha256'],'old_payload_sha256':pa['sha256'],'new_payload_sha256':pb['sha256'],'examples_block_identical':sourceblock(a)==sourceblock(b),'old_source_url':a['source_url'],'new_source_url':b['source_url'],'main':not case.startswith('GG-S'),'semantic_basis':'Exact current section references figure, first code recipe/caption and frozen purpose compared to old source; no succession inferred from filename/hash alone.'}
 c.update(manual.get(case,{}))
 if case=='GG-S13':c.update(semantic_basis='Frozen purpose is horizontal diamonds boxplot; new preferred first recipe swaps aesthetics. Exact old coord_flip recipe continues in second block with author same-plot comment; no frozen purpose broadened.',old_recipe_at_new_first=False,old_recipe_successor='reference/coord_flip-2.png',new_second_payload_url=collect.RAW+ed['new']['publication_sha']+'/reference/coord_flip-2.png',new_second_payload_sha256='5b83ffa8756ebf4b4fc3cad479388874578dc018d6dc72915b90660d4020d563',new_first_and_second_same_bytes=True,mechanism_return_section='Examples L145–149 (second block); first block L140–143 is preferred swapped-aesthetics recipe.',change_record=collect.RAW+ed['new']['source_sha']+'/NEWS.md',change_record_location='L49–51',exact_counterexample_types=['④'],near_miss='Old name remains and old/new bytes differ: not exact② or③. Within new edition identical image bytes illustrate different code mechanisms.')
 comparisons.append(c)
compsmain=[x for x in comparisons if x['main']]
assert all(x['examples_block_identical'] for x in compsmain)
first_new_body=min(x['body_utc'] for x in obs if x['edition']=='new');first_new_payload=min(p['utc'] for x in obs if x['edition']=='new' for p in x['payloads'])
audit={'project':'ggplot2','completed_utc':collect.utc(),'prediction_seal_remote':'f1c5d6ff927fd5fbe108565598810ca7e94c5753','first_new_body_utc':first_new_body,'first_new_payload_utc':first_new_payload,'main_slots':12,'main_filled_slots':8,'main_vacant_slots':4,'observations':obs,'comparisons':comparisons,'main_visual_review':{'performed':True,'observer':'ggplot2 agent, actual view_image calls','images':8,'notes':manual,'limits':'Visual role inspection, not a pixel-equality test or a browser/plot execution.'},'G_search':'evidence/ggplot2/build-search.json','generation':'All 8 real main edition positions G=미확인; package inclusion and section use do not prove a fresh generation run.','not_executed':['R example execution','browser rendering/JavaScript execution','historical build reproduction'],'counterexample_scope':'Main4 plus separately sealed remaining20; no auxiliary promotion into main; absent stratum remains two vacant pairs.'}
(D/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
(D/'supplemental-audit.json').write_text(json.dumps({'scope':'fixed20 from supplemental-order.json','comparisons':[x for x in comparisons if not x['main']],'type1':{'searched':20,'found':0,'reason':'Every examined new exact Examples includes original resource path; all URI forms enumerated.'},'type2':{'searched_frame_paths':40,'absent_old_paths':0,'found':0,'reason':'No old first resource absent in complete next tree. No absence-conditioned U test possible; mechanism-level relocated block in coord_flip is near-miss only.'},'type3':{'same_name_hash_pairs_in_supplement':1,'found_purpose_changes':0,'reason':'fortify.lm identical bytes and same diagnostic purpose; new coord_flip first/second same bytes use distinct methods but names differ and old/new bytes differ.'},'type4':{'main_found':4,'supplement_found':19,'reason':'Changed PNG bytes, exact section/source purpose continuation; actual numeric output identity not claimed.'},'cross_example_same_bytes':[{'examples':['facet_null','benchplot'],'old_sha256':'e7e1e2f4b8ce0895758bfbb39f6ba6631295d1a4d7ccea6ba11313c23c77604b','new_sha256':'d135eeef7c86412b16c65fcaa0df29607ae214a7c6b32373a485fdf33691e4e8','interpretation':'Same scatter image is used as a faceting default explanation and benchmark output. Different page functions are established by source/context, not by bytes.'}]},ensure_ascii=False,indent=2))
# Sources: preserve sealed ledgers, make conservative final accounting explicit.
sources=[]
for name in ['sources-stage1.jsonl','sources-stage2.jsonl']:
 for l in (D/name).read_text().splitlines():
  q=json.loads(l)
  if q['category']=='example_source':q.update(countable=False,duplicate_reason='Direct Rd source is the same reference-example work as counted rendered body; final conservative merge, sealed stage1 retained.')
  sources.append(q)
seen_urls={x['original_url']:x for x in sources};counted_image_sha={};counted_body_pages=set()
for q in sources:
 if q['category']=='example_body' and q['countable']:counted_body_pages.add(q['original_url'].split(ed['old']['publication_sha']+'/')[-1])
def add(r,category,observation,case,countable,duplicate='',location='',publisher='ggplot2 authors / tidyverse',family='PUB-ggplot2',version='',questions=None):
 sid='GG-S3-'+str(len([x for x in sources if x['source_id'].startswith('GG-S3-')])+1).zfill(3)
 q={'source_id':sid,'questions':questions or ['Q4','Q5','Q6','Q7'],'cases':[case] if case else [],'original_url':r['url'],'fixed_url':r['url'],'accessed_utc':r['accessed_utc'],'publisher':publisher,'lineage':family,'category':category,'version':version,'location':location,'sha256':r.get('sha256'),'observation':observation,'claims_supported':['Publication/section/source distinction or counterexample observation as stated'],'claims_refuted':['Path/hash alone proves logical use or fresh generation'],'limitations':'Directly read at fixed version; does not prove browser execution or actual historical generation run.','countable':countable,'duplicate_reason':duplicate,'receipt':r.get('receipt','')}
 sources.append(q);return q
for x in obs:
 page=x['body_url'].split(x['publication_sha']+'/')[1]
 br=json.loads((D/'receipts'/Path(x['body_receipt']).name).read_text());br['receipt']=x['body_receipt']
 observation={'purpose':x['purpose'],'section':x['section_locator'],'first_ref':x['first_literal_reference'],'legacy_refs':x['legacy_reference_count'],'other_uri_forms':{k:x[k] for k in ['script_count','picture_count','inline_svg_count','data_uri_count']},'first_code_and_source_read':True}
 if x['body_url'] in seen_urls:
  q=seen_urls[x['body_url']];q.update(cases=sorted(set(q['cases']+[x['case_id']])),observation=observation)
  if page not in counted_body_pages:q.update(countable=True,duplicate_reason='');counted_body_pages.add(page)
 else:
  add(br,'example_body',observation,x['case_id'],page not in counted_body_pages,'Same reference-page work across editions; paired access retained.' if page in counted_body_pages else '',x['section_locator'],version=x['version']);counted_body_pages.add(page)
 sr=json.loads((D/'receipts'/Path(x['source_receipt']).name).read_text());sr['receipt']=x['source_receipt']
 if sr['url'] not in seen_urls:add(sr,'example_source',{'source_file':x['source_path'],'example_block_sha256':x['source_examples_block_sha256'],'same_work_as_body':x['body_url']},x['case_id'],False,'Rendered-body/source same example work; conservatively not counted twice.','\\examples block',version=x['version'])
 for p in x['payloads']:
  pr=json.loads((D/'receipts'/Path(p['receipt']).name).read_text());pr['receipt']=p['receipt']
  # A logical first illustration contributes one work across versions; same bytes across pages also merge.
  oldsha=bycase[x['case_id']]['old']['payloads'][0]['sha256'];isfirst=(x['edition']=='old' and oldsha not in counted_image_sha)
  add(pr,'image_payload',{'format':p['signature'],'bytes':p['bytes'],'dimensions':[p['width'],p['height']],'purpose':x['purpose'],'git_blob_matches':p['blob_matches_publication'],'legacy_usage':'YES'},x['case_id'],isfirst,'' if isfirst else 'Same illustration work across versions or identical bytes already counted on another page.',x['first_literal_reference'],version=x['version'])
  if isfirst:counted_image_sha[oldsha]=x['case_id']
# Additional mechanism successor exactly duplicates new first payload; preserve observation, no new count.
pr=json.loads((D/'receipts/new-coord-flip-second.json').read_text());pr['receipt']='evidence/ggplot2/receipts/new-coord-flip-second.json';add(pr,'image_payload',{'new_second_exact_old_recipe':'coord_flip()','same_bytes_as_new_first':True},'GG-S13',False,'Same bytes as new coord_flip first image; not new source.','Examples second image L149',version='3.5.0')
# Inspected release/build/source-distribution evidence.
build=json.loads((D/'build-search.json').read_text())
for b in build:
 rr=json.loads((D/'receipts'/Path(b['receipt']).name).read_text());rr['receipt']=b['receipt'];key=b['key']
 if key.endswith(('-runs','-checks','-status')):
  add(rr,'build_search',{'query_scope':b['url'],'total_count':b.get('total_count'),'state':b.get('state'),'result':'No retained run/check/status records returned in queried scope; historical absence not inferred.'},'',False,'Empty job/status search is scope evidence, not a unique positive primary material.',version='3.4.0' if key.startswith('old') else '3.5.0');continue
 if key.endswith('distribution'):
  add(rr,'distribution_record',{'source_package_member_count':b['members'],'read_members':b['read_members'],'generated_reference_html_members':b['html_reference_members'],'role':'Official source distribution, not website publication or generation log.'},'',key.startswith('old'),'Same source-package work across editions.' if key.startswith('new') else '',location='tar member names and 5 selected members',version='3.4.0' if key.startswith('old') else '3.5.0');continue
 if 'workflow' in key:
  add(rr,'build_rule',{'invoke':'pkgdown::build_site_github_pages(new_process=FALSE, install=FALSE)','deploy':'docs folder → gh-pages; clean:false','limitations':'Rule and dependency declaration, not actual invocation/output manifest.'},'',key.startswith('old'),'Same workflow work across versions / new version already inherited in098.' if key.startswith('new') else '',location='Build site and Deploy steps, L35–47',version='3.4.0' if key.startswith('old') else '3.5.0')
 else:add(rr,'publication_config',{'observed':'Version metadata and development:auto/source configuration read; full digest preserved.'},'',False,'Supporting source configuration for same publication event.',location='Version / development.mode lines',version='3.4.0' if key.startswith('old') else '3.5.0')
for key,category,ob,count,loc,pub,fam,ver in [
 ('new-news','change_record','coord_flip superseded; recommendation swaps x/y or uses orientation; author @teunbrand references #5130.',True,'L49–51','ggplot2 authors / tidyverse','PUB-ggplot2','3.5.0'),
 ('deploy-old-readme','build_rule','folder designates deployment source; clean deletes destination-only files; clean:false disables this removal. Does not prove selected image was copied or generated.',True,'folder L126; clean L144','JamesIves/github-pages-deploy-action maintainers','RULE-github-pages-deploy-action','4.1.4'),
 ('deploy-new-readme','build_rule','Same clean:false semantics; current selected workflow declares v4.4.1.',False,'folder L110; clean L129','JamesIves/github-pages-deploy-action maintainers','RULE-github-pages-deploy-action','v4.4.1')]:
 rr=json.loads((D/'receipts'/(key+'.json')).read_text());rr['receipt']='evidence/ggplot2/receipts/'+key+'.json';add(rr,category,ob,'GG-S13' if key=='new-news' else '',count,'' if count else 'Same rule work across versions / inherited rule.',loc,pub,fam,ver)
for v in ['v2.0.6','v2.0.7']:
 for fn,loc,ob in [('R_build.R','build_site defaults and build_site_local reference call','build_site lazy default FALSE; passes lazy into build_reference.'),('R_build-github.R','L19–35','Wrapper cleans local output by default then invokes build_site; separate from gh-pages deploy clean:false.'),('R_build-reference.R','L199–205,268–272,359–365','Copies man/figures; reference topic uses man/*.Rd; lazy skip and run_examples are distinct paths.')]:
  key='pkgdown-'+v+'-'+fn;rr=json.loads((D/'receipts'/(key+'.json')).read_text());rr['receipt']='evidence/ggplot2/receipts/'+key+'.json';add(rr,'build_rule',ob,'',v=='v2.0.6','Same code-work across versions (two files byte-identical); inherited later rule.' if v=='v2.0.7' else '',loc,'r-lib/pkgdown maintainers','RULE-pkgdown',v)
(D/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
returns=[]
for s in selected:
 if s.get('vacant'):returns.append({'case_id':s['case_id'],'decision':'유보','vacant':True,'reason':s['vacancy_reason'],'history_url':'','current_url':'','reproduce_url':''});continue
 a,b=bycase[s['case_id']]['old'],bycase[s['case_id']]['new']
 returns.append({'case_id':s['case_id'],'decision':'두 판 병기','history_url':a['section_url'],'history_payload':a['payloads'][0]['url'],'current_url':b['section_url'],'current_payload':b['payloads'][0]['url'],'current_means':'Selected3.5.0, not latest2026 website','reproduce_url':b['source_url'],'reproduce_publication_url':'https://github.com/tidyverse/ggplot2/commit/'+b['publication_sha'],'reproduce_workflow_url':collect.RAW+ed['new']['source_sha']+'/.github/workflows/pkgdown.yaml','generation_missing':'Historical run id + input/environment lock + per-output digest bound to selected PNG; not available','section_to_read':'#ref-examples / first figure and preceding code','cheap_check':'For explanation read fixed section; image reuse adds its linked PNG. G enquiry additionally needs actual run/output evidence.','warning':'이 링크는 선택한3.5.0 발행판의 HTML 소스/그림이며, 최신사이트나 당시 생성빌드 재현을 보장하지 않습니다.'})
(D/'returns.json').write_text(json.dumps(returns,ensure_ascii=False,indent=2))
counts={'main_pairs_filled':4,'main_pair_vacancies':2,'main_positions':12,'main_actual_positions':8,'P':{'YES':8,'미확인_vacant':4},'U':{'YES':8,'미확인_vacant':4},'G':{'미확인':8,'미확인_vacant':4},'strata':{'general':{'TP':2,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':0,'positive_denominator':2,'negative_denominator':0},'old_asset_absent':{'TP':0,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':2,'positive_denominator':0,'negative_denominator':0},'asset_retained_source_changed':{'TP':2,'FP':0,'FN':0,'TN':0,'abstention':0,'vacancy':0,'positive_denominator':2,'negative_denominator':0}},'source_rows':len(sources),'countable_primary':sum(x['countable'] for x in sources),'countable_categories':dict(collections.Counter(x['category'] for x in sources if x['countable'])),'supplement_pairs':20,'main_byte_changed':4,'supplement_byte_changed':19,'supplement_same_bytes':1,'first_new_body_utc':first_new_body,'first_new_payload_utc':first_new_payload}
(D/'counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2));print(json.dumps(counts,ensure_ascii=False,indent=2))
