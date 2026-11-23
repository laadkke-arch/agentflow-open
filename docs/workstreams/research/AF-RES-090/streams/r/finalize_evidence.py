"""Synthesize only receipts already retrieved; no additional web requests."""
import collections,datetime,hashlib,html,io,json,re,sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from http_evidence import now,save_excerpt
ROOT=Path(__file__).parent;E=ROOT/'evidence';RAW=E/'raw'
def rec(i):return json.loads((E/(i+'.receipt.json')).read_text())
def data(i):return (RAW/(i+'.bin')).read_bytes()
def text(i):return data(i).decode('utf-8','replace')
def safe_receipt(r):
 allowed={'content-type','content-length','etag','last-modified','date','server','cache-control','location','x-github-request-id','x-content-type-options','content-disposition'}
 removed=[k for k in r.get('headers',{}) if k.lower() not in allowed]
 r['headers']={k:v for k,v in r.get('headers',{}).items() if k.lower() in allowed}
 if removed:r['header_redaction']={'reason':'Retain only response identity/type/cache evidence; exclude cookies and unrelated policy/session headers.','removed_header_names':removed}
 return r
for f in E.glob('*.receipt.json'):
 r=safe_receipt(json.loads(f.read_text()));f.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
tr=json.loads((ROOT/'traversals.json').read_text())
for row in tr['traversals']:
 row['steps']=[safe_receipt(x) for x in row['steps']]
(ROOT/'traversals.json').write_text(json.dumps(tr,ensure_ascii=False,indent=2)+'\n')
sources=[json.loads(l) for l in (ROOT/'sources.jsonl').read_text().splitlines()]
initial={x['source_id'] for x in sources}
observations={
 'R1-GENERATED-TREE':('supporting_manifest','R1-generated-tree','R1-publisher','1.1.12 generated commit45e0d9eb','Complete recursive tree has56 entries, truncated=false; no inst/extdata/data.zip. Generated documentation preservation does not imply example package file in this tree.',True,None),
 'R1-SOURCE-TREE':('supporting_manifest','R1-source-tree','R1-publisher','1.1.12 source a4c6ec37','Complete recursive tree121 entries, truncated=false; inst/extdata/data.zip is blob ff6fcff564072e5f7b4050c58de0dee696c68e88,929bytes.',True,None),
 'R2-GENERATED-TREE':('supporting_manifest','R2-generated-tree','R2-publisher','2.3.1 generated92fecbc0','Complete recursive tree442 entries, truncated=false; reference/init_knitr_engine.html and pkgdown.js exist, inst/examples/hello.R absent.',True,None),
 'R2-SOURCE-TREE':('supporting_manifest','R2-source-tree','R2-publisher','2.3.1 sourcef992b26f','Complete recursive tree209 entries, truncated=false; inst/examples/hello.R is f1a18139c84a82addbded8a7b5738c36fb02fce1,22bytes.',True,None),
 'R1-DATA-ZIP':('followup_resource','R1-data-zip','R1-publisher','sourcea4c6ec37','929byte ZIP contains iris.csv,mtcars.csv,airquality.csv. Direct Git blob digest matches source-tree listing. Contents include rows printed in generated example. Auxiliary source-package read, not the frozen first-followup destination.',True,None),
 'R2-HELLO-FIXED':('followup_resource','R2-hello-example','R2-publisher','sourcef992b26f','22byte R script prints Hello world; direct Git blob digest equals source tree listing. Read via manually assembled fixed-source URL outside main reader budget.',True,None),
 'R2-HELLO-WEB-LITERAL':('failure','R2-hello-web','R2-publisher','current service','Literal ../inst/examples/hello.R from Casting a script from a file, when manually resolved against article URL, gives404. Original text is not an HTML anchor. Inline displayed Hello world remains in article. This is not a failing live hyperlink and is not the frozen SVG target.',False,None),
 'R2-REFERENCE-FIXED':('followup_resource','R2-init-reference','R2-publisher','generated92fecbc0;2.3.1','Reference API page identifies2.3.1 and init_knitr_engine echo/same_process/timeout/startup/record_env/echo_input/interactive parameters. It is linked later under Showing the code, outside frozen Using SVG files target.',True,None),
 'R2-REFERENCE-CURRENT':('followup_resource','R2-init-reference','R2-publisher','current2.3.1','10917bytes and SHA256 equal fixed reference page. One checked additional document, not proof of every linked asset.',False,'R2-REFERENCE-FIXED'),
 'R2-PKGDOWN-FIXED':('followup_resource','R2-pkgdown-runtime','R2-publisher','generated92fecbc0','4406byte script adds navbar/TOC/tooltips/clipboard behavior. Read bytes only; did not execute JavaScript. Fixed tree lists blob5fccd9c0e29f0b54aa7d0092fa31571eb205562a, verified against bytes.',True,None),
 'R2-PKGDOWN-CURRENT':('followup_resource','R2-pkgdown-runtime','R2-publisher','current service','4406bytes and SHA256 match fixed script, a counterexample to assuming all assets behind identical HTML must drift.',False,'R2-PKGDOWN-FIXED'),
 'R2-RMD-FIXED':('publisher_source','R2-vignette-source','R2-publisher','2.3.1 sourcef992b26f','4419byte source uses chunk header options, including cache=TRUE and code=readLines("../inst/examples/hello.R").',True,None),
 'R2-RMD-HEAD':('publisher_source','R2-vignette-source','R2-publisher','HEAD later pinneda0076449','4440byte linked moving source differs from selected2.3.1 original; code chunk options use #| YAML lines. Existing identical generated HTML still links this moving HEAD source.',True,None),
 'R2-RMD-HEAD-PINNED':('publisher_source','R2-vignette-source','R2-publisher','a0076449feec11c835ff46f7934fe75232f7d759','Pinned current source bytes equal preceding HEAD response, tying observed source drift to an explicit commit without claiming history of the rendered site.',False,'R2-RMD-HEAD'),
 'R2-SOURCE-HEAD-COMMIT':('supporting_manifest','R2-current-commit','R2-publisher','a0076449feec11c835ff46f7934fe75232f7d759','GitHub current HEAD commit is a0076449feec11c835ff46f7934fe75232f7d759; containing commit committer timestamp2025-12-01T10:58:43Z. This is not the Rmd file modification date.',True,None),
 'R1-SYSTEMFILE-OFFICIAL':('followup_resource','R-base-systemfile','R-base-manual','R-devel base4.6.0','Official R manual says system.file locates files within installed packages; empty string when absent unless mustWork=TRUE. Footer base4.6.0. Does not identify the R version used to generate archive1.1.12.',True,None),
}
for f in sorted(E.glob('*.receipt.json')):
 r=json.loads(f.read_text());i=r['source_id']
 if i in initial:continue
 if i in observations:
  category,work,lineage,version,obs,eligible,dup=observations[i]
 else:
  # Executed main reader observations. Repeated entry manifestations are not new sources.
  traversal=next(x for x in tr['traversals'] if any(s['source_id']==i for s in x['steps']))
  category='reader_observation';case=traversal['case_id'];lineage=case+'-publisher';version=traversal['entry_version'];work=case+'-ARTICLE';eligible=False
  dup=case+'-FIXED-HTML' if traversal['route']=='B' or case=='R2' else case+'-ENTRY-A'
  obs='; '.join(traversal['observations'])
  if i.endswith('-2'):
   category='followup_resource';work='R-base-systemfile';lineage='R-base-manual';version='unversioned rdrr R base help';dup='R1-SYSTEMFILE-OFFICIAL';obs='Actual second reader view follows system.file href to rdrr operation help; purpose content read. R release not pinned by originating document; current mirror is not a same-build provenance proof. Official counterpart independently read; counted only once as one manual work.'
  elif r['status']!=200:
   category='failure';dup=None;obs='HTTP503 with GitHub Unicorn error HTML. Title Unicorn! · GitHub and service-error message; no explicit rate/access restriction language. Envoy header and GitHub request ID do not establish fault origin. Stop reader path here; earlier200 does not repair this row.'
 src={'source_id':i,'work_id':work,'lineage_id':lineage,'category':category,'original_url':r['requested_url'],'published_utc':('2025-12-01T10:58:43Z' if i=='R2-SOURCE-HEAD-COMMIT' else None),'retrieved_utc':r['retrieved_utc'],'version':version,'location':r['requested_url'].split('.com/')[-1] if '.com/' in r['requested_url'] else r['requested_url'],'questions':['Q3','Q4','Q5','Q6'],'cases':['R1' if 'R1' in i else 'R2'],'observation':obs,'excerpt':("We're having a really bad day." if r['status']==503 else 'print("Hello world!")' if i=='R2-HELLO-FIXED' else '#| cache: true' if i in ['R2-RMD-HEAD','R2-RMD-HEAD-PINNED'] else 'system.file(..., package = "base", lib.loc = NULL, mustWork = FALSE)' if 'SYSTEMFILE' in i else None),'fingerprint':{'sha256':r['sha256'],'git_blob_sha1':r['git_blob_sha1'],'body_bytes':r['body_bytes'],'content_type':r['content_type']},'support_refute':'supports/refutes bounded path/content relation as stated; no whole-site inference','limitations':'Public HTTP receipt only. No R/JS execution, no historical-serving claim. Supplementary source/manifest reads are outside main reader budget. '+('Excluded duplicate/repeated manifestation or failed response.' if not eligible else ''),'reread_url':r['requested_url'],'eligible':eligible and r['status']==200,'duplicate_of':dup,'receipt_path':'streams/r/evidence/'+f.name,'excerpt_path':'streams/r/evidence/'+i+'.excerpt.json'}
 sources.append(src);save_excerpt(E,i,obs,[src['excerpt']] if src['excerpt'] else [])
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
# Tree integrity, source/package and current/fixed comparisons.
comparisons=[]
for a,b in [('R2-FIXED-HTML','R2-ENTRY-A'),('R2-REFERENCE-FIXED','R2-REFERENCE-CURRENT'),('R2-PKGDOWN-FIXED','R2-PKGDOWN-CURRENT'),('R2-RMD-FIXED','R2-RMD-HEAD'),('R2-RMD-HEAD','R2-RMD-HEAD-PINNED')]:
 comparisons.append({'left':a,'right':b,'equal':data(a)==data(b),'left_sha256':rec(a)['sha256'],'right_sha256':rec(b)['sha256'],'scope':'actual response entity bytes only'})
(E/'R-resource-comparisons.json').write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n')
assets=[]
for i,treeid,path in [('R1-FIXED-HTML','R1-GENERATED-TREE','reference/archive_read.html'),('R1-DATA-ZIP','R1-SOURCE-TREE','inst/extdata/data.zip'),('R2-FIXED-HTML','R2-GENERATED-TREE','articles/asciicast-demo.html'),('R2-HELLO-FIXED','R2-SOURCE-TREE','inst/examples/hello.R'),('R2-REFERENCE-FIXED','R2-GENERATED-TREE','reference/init_knitr_engine.html'),('R2-PKGDOWN-FIXED','R2-GENERATED-TREE','pkgdown.js')]:
 tree=json.loads(text(treeid));entry=next(x for x in tree['tree'] if x['path']==path);r=rec(i)
 assets.append({'asset_id':i,'source_id':i,'file':path,'anchor':'#ref-usage/#ref-examples' if i=='R1-FIXED-HTML' else '#example/#using-svg-files' if i=='R2-FIXED-HTML' else None,'sha256':r['sha256'],'bytes':r['body_bytes'],'mime':r['content_type'],'hosting_url':r['final_url'],'directly_read':True,'reader_budget':'auxiliary source/tree comparison, not main reader success','manual_path_reconstruction':i in ['R1-DATA-ZIP','R2-HELLO-FIXED'],'publisher_tree_source':treeid,'publisher_blob_sha1':entry['sha'],'computed_blob_sha1':r['git_blob_sha1'],'blob_matches':entry['sha']==r['git_blob_sha1'],'tree_truncated':tree['truncated'],'same_commit_exists':True,'limit':'Source-package tree for data.zip/hello.R differs from generated-document tree; file presence is not two-view reader reachability.'})
frozen=json.loads((ROOT/'freeze.json').read_text())['R2']
assets.append({'asset_id':'R2-INLINE-STATIC','source_id':'R2-FIXED-HTML','file':'articles/asciicast-demo.html','anchor':'#using-svg-files','sha256':frozen['first_inline_sha256'],'bytes':frozen['first_inline_bytes'],'mime':'inline HTML pre text','hosting_url':rec('R2-ENTRY-A')['final_url'],'directly_read':True,'reader_budget':'contained in entry;0 extra views','manual_path_reconstruction':False,'same_commit_exists':True,'inline_payload_count':2,'resource_kind':'static output','svg_or_replay':'no_explicit_path','limit':'No SVG XML, cast JSON or player resource in this selected section. Static output is not replay execution.'})
assets.append({'asset_id':'R1-FIRST-REFERENCE','source_id':'R-R1-next-A-2','file':'R base system.file help','anchor':None,'sha256':rec('R-R1-next-A-2')['sha256'],'bytes':rec('R-R1-next-A-2')['body_bytes'],'mime':rec('R-R1-next-A-2')['content_type'],'hosting_url':rec('R-R1-next-A-2')['final_url'],'directly_read':True,'reader_budget':'R1-next-A second view; B-next blocked at first503','manual_path_reconstruction':False,'same_commit_exists':'not_applicable external manual','same_version':'unconfirmed','limit':'Source href absolute but unversioned; archive release does not identify specific R manual version.'})
assets.append({'asset_id':'R2-LITERAL-HELLO-WEB','source_id':'R2-HELLO-WEB-LITERAL','file':'inst/examples/hello.R','anchor':'#casting-a-script-from-a-file','sha256':rec('R2-HELLO-WEB-LITERAL')['sha256'],'bytes':rec('R2-HELLO-WEB-LITERAL')['body_bytes'],'mime':rec('R2-HELLO-WEB-LITERAL')['content_type'],'hosting_url':rec('R2-HELLO-WEB-LITERAL')['final_url'],'directly_read':False,'response_read':True,'reader_budget':'supplementary outside frozen SVG target','manual_path_reconstruction':True,'same_commit_exists':False,'http_status':404,'limit':'No live HTML href; local R-relative string manually interpreted as web path. Generated tree lacks file; source tree contains it.'})
(ROOT/'assets.jsonl').write_text(''.join(json.dumps(a,ensure_ascii=False)+'\n' for a in assets))
with zipfile.ZipFile(io.BytesIO(data('R1-DATA-ZIP'))) as z:
 members=[{'name':n,'bytes':len(z.read(n)),'sha256':hashlib.sha256(z.read(n)).hexdigest(),'header':z.read(n).decode().splitlines()[0]} for n in z.namelist()]
(E/'R1-zip-members.json').write_text(json.dumps({'source_id':'R1-DATA-ZIP','members':members,'counting':'ZIP is one externally retrieved resource; member extraction is not three extra external sources.'},ensure_ascii=False,indent=2)+'\n')
status_counts={axis:dict(collections.Counter(r[axis] for r in tr['traversals'])) for axis in ['target_body','followup_resource','same_version']}
summary={'recorded_utc':now(),'traversals':len(tr['traversals']),'pairs':len(tr['traversals'])//2,'reader_views':sum(r['views'] for r in tr['traversals']),'reader_response_bytes':sum(r['direct_response_bytes'] for r in tr['traversals']),'reader_status_counts':dict(collections.Counter(s['status'] for r in tr['traversals'] for s in r['steps'])),'axis_counts':status_counts,'source_rows':len(sources),'eligible_unique_materials':sum(s['eligible'] for s in sources),'eligible_categories':dict(collections.Counter(s['category'] for s in sources if s['eligible'])),'lineages':sorted({s['lineage_id'] for s in sources if s['eligible']}),'all_receipt_requests':len(list(E.glob('*.receipt.json'))),'all_receipt_bytes':sum(rec(p.name.replace('.receipt.json',''))['body_bytes'] for p in E.glob('*.receipt.json')),'notes':['Independent traversals include three503 entries; initial/browser200 not substituted.','source counts exclude repeated reader entries, mirrors,403/404/503 and duplicate current/fixed bytes.','inline static success differs from actual SVG/replay absence.']}
(E/'R-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
