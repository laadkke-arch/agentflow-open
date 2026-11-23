"""AF-RES-106 staged, public evidence collection. Stage1 opens only OLD content.
Run from any directory with Python standard library; no package install required.
"""
from pathlib import Path
import urllib.request, urllib.error, urllib.parse, json, hashlib, csv, io
import subprocess, tarfile, re, html, datetime

D=Path(__file__).resolve().parent
C=D/'.cache'; C.mkdir(exist_ok=True)
R=D/'receipts'; R.mkdir(exist_ok=True)
OLD='57852124c86f770dd443fcf5064d30ea320a4731'
NEW='392175bbb00b04025aa5d17a0c18b3896adeb40f'
OSRC='63125db184b6e7d5516007574b5d15acbfd8f470'
NSRC='a6f1a7c845bfe056ef952b839d2fd65b888ab5cd'
INHERIT='092f4c5c56451bceb53e632f4bddf33db6cda168'
RAW='https://raw.githubusercontent.com/tidyverse/ggplot2/'
API='https://api.github.com/repos/tidyverse/ggplot2/'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def gitsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def savejson(name,x): (D/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fetch(key,url):
 p=C/key; q=R/(key+'.json')
 if p.exists() and q.exists(): return p.read_bytes(),json.loads(q.read_text())
 st=utc()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-106-public-research'})
  with urllib.request.urlopen(req,timeout=55) as r:
   b=r.read(); rec={'url':url,'final_url':r.url,'started_utc':st,'accessed_utc':utc(),'status':r.status,'bytes':len(b),'sha256':sha(b),'content_type':r.headers.get('Content-Type')}
  p.write_bytes(b)
 except Exception as e:
  rec={'url':url,'started_utc':st,'accessed_utc':utc(),'status':getattr(e,'code',None),'error':repr(e)}
  q.write_text(json.dumps(rec,indent=2)+'\n'); raise
 q.write_text(json.dumps(rec,indent=2)+'\n');return b,rec
def clean(s): return html.unescape(re.sub('<[^>]+>','',s)).strip()
def attrs(s): return {m[0]:html.unescape(m[2]) for m in re.findall(r'([\w-]+)\s*=\s*([\"\'])(.*?)\2',s,re.S)}
def stage1():
 tree=json.loads((D/'old-tree.json').read_text()); assert tree.get('truncated') is False
 tb={x['path']:x for x in tree['tree'] if x['type']=='blob'}
 b,src_receipt=fetch('old-source-tree.json',API+'git/trees/'+OSRC+'?recursive=1')
 src=json.loads(b); assert src.get('truncated') is False
 savejson('old-source-tree.json',src)
 sm={x['path']:x for x in src['tree'] if x['type']=='blob'}
 prior=subprocess.check_output(['git','show',INHERIT+':docs/workstreams/research/AF-RES-102/frame.csv'],cwd=D).decode()
 priorrows=[x for x in csv.DictReader(io.StringIO(prior)) if x['project']=='ggplot2' and x['eligible']=='YES']
 excluded={x['page_path']:'AF-RES-102 first40 eligible logical example' for x in priorrows}
 excluded.update({'reference/aes.html':'Inherited corrected AF-RES-098 logical example','reference/aes_colour_fill_alpha.html':'Inherited corrected AF-RES-098 logical example'})
 savejson('inherited-exclusions.json',{'input_commit':INHERIT,'prior_eligible_40':[x['page_path'] for x in priorrows],'extra_exclusions':{k:v for k,v in excluded.items() if '098' in v},'logical_alias_rule':'Same documented Examples body/resources/code identity is excluded even through an alias path; title/method family alone does not make two independent examples identical.'})
 rows=[]; members={}; rawhtml={}
 with tarfile.open(C/'old-publication.tar.gz','r:gz') as ar:
  for m in ar.getmembers():
   if not m.isfile():continue
   p=m.name.split('/',1)[1]
   members[p]=m.size
   if p.startswith('reference/') and p.endswith('.html'):
    rawhtml[p]=ar.extractfile(m).read()
 old_dir=C/'old';old_dir.mkdir(exist_ok=True)
 paths=sorted(p for p in tb if p.startswith('reference/') and p.endswith('.html'))
 assert set(paths)==set(rawhtml)
 # Keep complete file inventory; no individual archived file is counted as a directly read source.
 savejson('old-archive-inventory.json',{'archive_receipt':'old-archive-receipt.json','root':'','members':members,'git_tree_all_blobs':len(tb),'archive_file_count':len(members),'path_set_equal':set(tb)==set(members),'reference_pages':paths})
 for ix,p in enumerate(paths,1):
  b=rawhtml[p];s=b.decode('utf-8');assert gitsha(b)==tb[p]['sha']
  (old_dir/Path(p).name).write_bytes(b)
  title=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
  desc=re.search(r'<meta name="description" content="([^"]+)"',s)
  r={'project':'ggplot2','page_rank':ix,'page_path':p,'old_version':'3.4.0','old_publication_sha':OLD,'body_url':RAW+OLD+'/'+p,'body_blob':tb[p]['sha'],'body_sha256':sha(b),'archive_receipt':'evidence/ggplot2/old-archive-receipt.json','machine_scan':'YES','direct_detail_read':'NO','eligible':'NO','exclusion':'','title':clean(title[1]) if title else '', 'description':html.unescape(desc[1]) if desc else ''}
  m=re.search(r'<h2[^>]*id="(ref-examples|examples)"[^>]*>',s)
  if not m:
   r['exclusion']=excluded.get(p,'No Examples heading');rows.append(r);continue
  start=s.rfind('<div class="section level2"',0,m.start());end=len(s)
  if start>=0:
   depth=0
   for t in re.finditer(r'</?div\b[^>]*>',s[start:]):
    depth+= -1 if t.group().startswith('</') else 1
    if depth==0:end=start+t.end();break
  else:
   em=re.search(r'<h2\b',s[m.end():]);end=m.end()+em.start() if em else len(s)
  sec=s[m.end():end];fragment=m[1]
  r.update(old_fragment=fragment,old_section_path=p+'#'+fragment,section_start_line=s[:m.start()].count('\n')+1,section_end_line=s[:end].count('\n')+1)
  im=next((x for x in re.finditer(r'<img\b[^>]*>',sec) if not any(w in x.group().lower() for w in ('logo','badge'))),None)
  if not im:
   r['exclusion']=excluded.get(p,'No explanatory image in Examples');rows.append(r);continue
  a=attrs(im.group());srcattr=a.get('src','')
  before=sec[:im.start()]
  # Strip output spans and retain code in .r-in nodes (the prefix is valid text even if HTML tags remain open).
  code=clean(before);code=re.sub(r'^Examples\s*','',code);code=re.sub(r'^\s*\n','',code)
  calls=list(dict.fromkeys(re.findall(r'\b([A-Za-z][\w.:]*)\s*\(',code)))
  external=not srcattr.startswith('data:')
  resolved=urllib.parse.urljoin(p,srcattr)
  source='man/'+Path(p).stem+'.Rd'
  source_links=[html.unescape(x) for x in re.findall(r'https://github.com/tidyverse/ggplot2/blob/[^/]+/([^"<>]+)',s) if x.startswith(('R/','man/'))]
  r.update(old_resource_path=resolved if external else '',asset_kind='external' if external else 'inline',old_literal_reference=srcattr if external else srcattr.split(',')[0],old_srcset=a.get('srcset',''),old_img_tag=im.group() if external else '[inline data URI omitted]',old_base_tags=';'.join(re.findall(r'<base\b[^>]*>',s)),old_picture_count=len(re.findall(r'<picture\b',sec)),old_svg_count=len(re.findall(r'<svg\b',sec)),first_image_line=s[:m.end()+im.start()].count('\n')+1,first_example_code=code,method_purpose='; '.join(calls),visual_purpose='First plotted result in '+r['title']+'; '+re.sub(r'\s+',' ',code),source_path=source,source_blob=sm.get(source,{}).get('sha',''),author_source_links=';'.join(dict.fromkeys(source_links)),old_resource_blob=tb.get(resolved,{}).get('sha',''),hash_sha256=sha(('AF106|ggplot2|'+p+'#'+fragment).encode()))
  if p in excluded:r['exclusion']=excluded[p]
  elif not code.strip():r['exclusion']='No executable-code prefix for first plotted example'
  elif external and resolved not in tb:r['exclusion']='Resource outside complete publication tree; access not yet confirmed'
  else:r['eligible']='YES'
  if source not in sm:r['source_mapping_limit']='미확인: canonical same-name man path absent already in OLD source; do not treat this as NEW disappearance'
  rows.append(r)
 # Exact code/resource duplicates of inherited examples are aliases, even if a different URL survives.
 inherited=[x for x in rows if x['page_path'] in excluded and x.get('first_example_code')]
 for r in rows:
  if r['eligible']!='YES':continue
  alias=next((p for p in inherited if r.get('first_example_code')==p.get('first_example_code') and r.get('old_resource_blob')==p.get('old_resource_blob')),None)
  if alias:r.update(eligible='NO',exclusion='Alias of inherited '+alias['page_path'])
 # Manual alias adjudications, based jointly on rendered payload and exact final graphical call.
 alias_map={'reference/layer.html':'reference/aes.html','reference/scale_continuous.html':'reference/aes.html','reference/theme_get.html':'reference/facet_null.html'}
 for r in rows:
  if r['page_path'] in alias_map:
   target=next(x for x in rows if x['page_path']==alias_map[r['page_path']])
   assert r['old_resource_blob']==target['old_resource_blob']
   r.update(eligible='NO',exclusion='Inherited logical-example alias: '+alias_map[r['page_path']],alias_basis='Same first graphical call/data/aes/geom_point and identical old payload; contextual page topic is not a new first-example method.')
 within_alias_map={'reference/geom_rug.html':'reference/geom_point.html','reference/gg-add.html':'reference/geom_smooth.html','reference/scale_hue.html':'reference/scale_brewer.html','reference/scale_viridis.html':'reference/scale_brewer.html'}
 for r in rows:
  if r['page_path'] in within_alias_map:
   target=next(x for x in rows if x['page_path']==within_alias_map[r['page_path']])
   assert r['old_resource_blob']==target['old_resource_blob']
   r.update(eligible='NO',exclusion='Within-frame logical alias: '+within_alias_map[r['page_path']],alias_basis='Identical first plotted data/aesthetics/geometry calls and old payload; assignment versus direct expression is the same graphical method; keep lexically first page. Full first-code pairs are preserved in old-logical-alias-audit.json. Different concrete calls such as stat_identity remain distinct.')
 purposes=json.loads((D/'old-purpose-annotations.json').read_text()) if (D/'old-purpose-annotations.json').exists() else {}
 for r in rows:
  if r['page_path'] in purposes:
   r.update(visual_purpose=purposes[r['page_path']][0],method_purpose=purposes[r['page_path']][1],purpose_annotation='Analyst reading of old rendered code; not inferred from NEW content')
 keys=list(dict.fromkeys(k for x in rows for k in x))
 with (D/'stage1-frame.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
 savejson('stage1-frame.json',rows)
 from collections import Counter
 elig=[r for r in rows if r['eligible']=='YES']
 summary={'completed_utc':utc(),'project':'ggplot2','publication_sha':OLD,'source_sha':OSRC,'old_root':'','reference_page_count':len(paths),'old_tree_complete':True,'archive_all_blob_paths_equal_tree':set(tb)==set(members),'all_reference_html_git_blob_verified':len(rows),'remaining_eligible':len(elig),'inline_only_eligible':sum(r.get('asset_kind')=='inline' for r in elig),'excluded_by_reason':dict(Counter(r['exclusion'] for r in rows if r['eligible']=='NO')),'access_failures':0,'automatic_html_scans':len(rows),'direct_detail_read_count':0,'new_tree_reads':0,'new_body_reads':0,'hash_formula':"SHA256(UTF8('AF106|ggplot2|'+old_section_path))",'inherited_exclusions':'inherited-exclusions.json','stage1_data_origin':'One fixed old codeload archive, paths/hash checked against complete fixed Git tree. Source tree metadata only.'}
 savejson('stage1-summary.json',summary)
 print(json.dumps(summary,ensure_ascii=False,indent=2))
 for r in elig:print(r['page_path'],r['old_resource_path'],r['method_purpose'])
if __name__=='__main__':stage1()
