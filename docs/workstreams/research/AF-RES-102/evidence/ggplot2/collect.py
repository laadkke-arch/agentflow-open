from pathlib import Path
import urllib.request, urllib.error, json, hashlib, re, csv, concurrent.futures, datetime, html, os
D=Path(__file__).resolve().parent
C=D/'cache';C.mkdir(exist_ok=True)
R=D/'receipts';R.mkdir(exist_ok=True)
(D/'.gitignore').write_text('cache/\n__pycache__/\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(key,url):
 p=C/key
 rp=R/(key+'.json')
 if p.exists() and rp.exists():return p.read_bytes(),json.loads(rp.read_text())
 start=utc()
 req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-102-public-evidence-research'})
 try:
  with urllib.request.urlopen(req,timeout=60) as q:
   b=q.read();x={'url':url,'final_url':q.url,'started_utc':start,'accessed_utc':utc(),'status':q.status,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'content_type':q.headers.get('Content-Type'),'headers':{k:q.headers.get(k) for k in ['Last-Modified','ETag','Content-Length']}}
  p.write_bytes(b)
 except Exception as e:
  x={'url':url,'started_utc':start,'accessed_utc':utc(),'error':repr(e),'status':getattr(e,'code',None)};rp.write_text(json.dumps(x,ensure_ascii=False,indent=2));raise
 rp.write_text(json.dumps(x,ensure_ascii=False,indent=2));return b,x
def jget(key,url):
 b,r=fetch(key,url);return json.loads(b),r
API='https://api.github.com/repos/tidyverse/ggplot2/'
RAW='https://raw.githubusercontent.com/tidyverse/ggplot2/'
OLD='57852124c86f770dd443fcf5064d30ea320a4731'
NEW='392175bbb00b04025aa5d17a0c18b3896adeb40f'
def clean(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
def parse_old(path,tree,sourcetree):
 key='old-'+path.replace('/','_')
 b,r=fetch(key,RAW+OLD+'/'+path);s=b.decode()
 result={'project':'ggplot2','page_path':path,'page_sha':tree[path]['sha'],'body_sha256':r['sha256'],'body_url':r['url'],'body_receipt':'evidence/ggplot2/receipts/'+key+'.json','read_utc':r['accessed_utc']}
 m=re.search(r'<h2[^>]*id="(ref-examples|examples)"[^>]*>',s)
 if not m:
  result.update(eligible=False,exclusion='No Examples heading');return result
 startdiv=s.rfind('<div class="section level2"',0,m.start())
 end=len(s)
 if startdiv>=0:
  depth=0
  for t in re.finditer(r'</?div\b[^>]*>',s[startdiv:]):
   depth += -1 if t.group(0).startswith('</') else 1
   if depth==0:
    end=startdiv+t.end();break
 else:
  endm=re.search(r'<h2\b',s[m.end():]);end=m.end()+endm.start() if endm else len(s)
 section=s[m.start():end]
 imgs=list(re.finditer(r'<img\b[^>]*>',section))
 img=next((z for z in imgs if not any(t in z.group(0).lower() for t in ['logo','badge'])),None)
 fragment=m.group(1)
 result.update(section_path=path+'#'+fragment,fragment=fragment,section_start_line=s[:m.start()].count('\n')+1,section_end_line=s[:end].count('\n')+1)
 if img is None:
  result.update(eligible=False,exclusion='No explanatory img in Examples section');return result
 src=re.search(r'\bsrc="([^"]+)"',img.group(0))
 if not src:
  result.update(eligible=False,exclusion='First explanatory img has no src');return result
 from urllib.parse import urljoin,urlparse
 asset=urljoin(path,html.unescape(src.group(1)))
 source_paths=re.findall(r'https://github.com/tidyverse/ggplot2/blob/[^/]+/([^"<>]+)',s)
 source_paths=[html.unescape(x) for x in source_paths if x.startswith(('R/','man/'))]
 source_path='man/'+Path(path).stem+'.Rd'
 result['author_source_links']=';'.join(source_paths)
 result['source_mapping_rule']='Rendered reference page maps to same-name man/*.Rd, all 40 exact paths present in old official source tree; author R links preserved separately.'
 before=section[max(0,img.start()-3500):img.start()]
 result.update(eligible=True,exclusion='',old_resource_path=asset,old_literal_reference=html.unescape(src.group(1)),old_img_tag=img.group(0),first_image_line=s[:m.start()+img.start()].count('\n')+1,purpose_excerpt=' '.join(clean(before).split()[-16:]),source_path=source_path,source_blob=sourcetree.get(source_path,{}).get('sha',''),resource_blob=tree.get(asset,{}).get('sha',''),sorting_hash=hashlib.sha256(('AF-RES-102|ggplot2|'+path+'#'+fragment).encode()).hexdigest())
 return result

def stage1():
 release_old,ro=jget('release-v3.4.0',API+'releases/tags/v3.4.0')
 release_new,rn=jget('release-v3.5.0',API+'releases/tags/v3.5.0')
 tagold,to=jget('tag-v3.4.0',API+'git/ref/tags/v3.4.0')
 tagnew,tn=jget('tag-v3.5.0',API+'git/ref/tags/v3.5.0')
 # Metadata-only projection; raw commit files are not printed or interpreted.
 oldcomm,oc=jget('publication-old',API+'git/commits/'+OLD)
 newcomm,nc=jget('publication-new-metadata',API+'git/commits/'+NEW)
 oldtree,ot=jget('old-tree',API+'git/trees/'+OLD+'?recursive=1')
 oldsource=tagold['object']['sha']
 if tagold['object']['type']=='tag':
  a,_=jget('tagobject-old',API+'git/tags/'+oldsource);oldsource=a['object']['sha']
 newsource=tagnew['object']['sha']
 if tagnew['object']['type']=='tag':
  a,_=jget('tagobject-new',API+'git/tags/'+newsource);newsource=a['object']['sha']
 sourceold,st=jget('old-source-tree',API+'git/trees/'+oldsource+'?recursive=1')
 tree={x['path']:x for x in oldtree['tree']};sourcetree={x['path']:x for x in sourceold['tree']}
 paths=sorted(p for p,x in tree.items() if p.startswith('reference/') and p.endswith('.html') and x['type']=='blob')
 rows=[];eligible=[]
 for path in paths:
  if path in ['reference/aes.html','reference/aes_colour_fill_alpha.html']:
   rows.append({'project':'ggplot2','page_path':path,'eligible':False,'exclusion':'Inherited AF-RES-098 logical main example'});continue
  rr=parse_old(path,tree,sourcetree);rows.append(rr)
  if rr['eligible']:
   rr['eligible_rank']=len(eligible)+1;eligible.append(rr)
  print(json.dumps({k:rr.get(k) for k in ['page_path','eligible','exclusion','old_resource_path','source_path','eligible_rank']},ensure_ascii=False),flush=True)
  if len(eligible)==40:break
 keys=list(dict.fromkeys(k for x in rows for k in x))
 with (D/'frame.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
 (D/'frame.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
 selected=sorted(eligible,key=lambda x:x['sorting_hash'])[:2]
 for i,x in enumerate(selected,1):x['case_id']='GG-G'+str(i);x['stratum']='general'
 (D/'selected-general.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
 editions={'project':'ggplot2','old':{'version':'3.4.0','source_sha':oldsource,'publication_sha':OLD,'source_release':release_old['html_url'],'published_at':release_old['published_at'],'publication_metadata':oldcomm,'base_url':RAW+OLD+'/','current_site_url_not_historical':'https://ggplot2.tidyverse.org/'},'new':{'version':'3.5.0','source_sha':newsource,'publication_sha':NEW,'source_release':release_new['html_url'],'published_at':release_new['published_at'],'publication_metadata':newcomm,'base_url':RAW+NEW+'/'},'old_tree_complete':not oldtree.get('truncated'),'old_source_tree_complete':not sourceold.get('truncated'),'old_tree_url':ot['url'],'old_source_tree_url':st['url'],'publication_selection_rule':'Earliest gh-pages deploy whose message names exact source tag commit; known 3.5.0 publication recovered from inherited 098 but only metadata opened at stage1. Raw fixed HTML is a preserved official publication file, not a rendered historic website.'}
 (D/'editions.json').write_text(json.dumps(editions,ensure_ascii=False,indent=2))
 (D/'old-tree-projection.json').write_text(json.dumps({'url':ot['url'],'sha':oldtree['sha'],'truncated':oldtree.get('truncated'),'tree':oldtree['tree']},indent=2))
 (D/'stage1.json').write_text(json.dumps({'completed_utc':utc(),'eligible_count':len(eligible),'considered_pages':len(rows),'all_old_reference_pages':len(paths),'general_sections':[x['section_path'] for x in selected],'sorting_rule':"SHA256(UTF8('AF-RES-102|ggplot2|'+relative_page+'#'+fragment)) ascending; first 40 eligible pages in lexical relative-page order; do not expand beyond the first40 for change strata.",'exposures':['new release metadata including source SHA, release description, event dates (not rendered examples)','new tag pointer SHA/type','new publication git-commit metadata: source SHA message, parent/tree SHA, author/date; no new tree, body, image or CI logs opened'],'new_body_or_asset_reads':0,'new_tree_reads':0},ensure_ascii=False,indent=2))
if __name__=='__main__':stage1()
