"""Recompute OLD author-source evidence only; never opens NEW content."""
from collect import *
rows=json.loads((D/'stage1-frame.json').read_text())
tree={x['path']:x for x in json.loads((D/'old-source-tree.json').read_text())['tree'] if x['type']=='blob'}
with tarfile.open(C/'old-source.tar.gz') as ar:
 fs={m.name.split('/',1)[1]:ar.extractfile(m).read() for m in ar.getmembers() if m.isfile()}
assert set(tree)==set(fs)
out=[]
for r in rows:
 if r['eligible']!='YES':continue
 p=r['source_path'];e={'page_path':r['page_path'],'old_section_path':r['old_section_path'],'render_source_path':p,'render_source_exists':p in fs,'render_source_url':RAW+OSRC+'/'+p,'old_html_source_links':r['author_source_links'],'confirmed_author_source_set':[],'status':'미확인'}
 if p in fs:
  b=fs[p];s=b.decode();assert gitsha(b)==tree[p]['sha'];lines=s.splitlines()
  h=next((x for x in lines if 'Please edit documentation in' in x),'');sources=re.findall(r'R/[^,\s]+',h)
  e.update(render_git_blob=tree[p]['sha'],render_sha256=sha(b),generated_header=h,header_line=next((i+1 for i,x in enumerate(lines) if 'Please edit documentation in' in x),None),Rd_examples_present='\\examples{' in s,Rd_examples_line=next((i+1 for i,x in enumerate(lines) if '\\examples{' in x),None))
  for a in sources:
   if a not in fs:continue
   aa=fs[a];ass=aa.decode()
   e['confirmed_author_source_set'].append({'path':a,'source_url':RAW+OSRC+'/'+a,'git_blob':tree[a]['sha'],'sha256':sha(aa),'also_old_html_source_link':a in r['author_source_links'].split(';'),'R_examples_marker_count':len(re.findall(r'@examples\b',ass)),'basis':'Generated Rd explicitly names authored documentation source and has executable examples; not a bare implementation-file link','status':'YES' if '\\examples{' in s else '미확인'})
  e['status']='YES' if e['Rd_examples_present'] and any(x['status']=='YES' for x in e['confirmed_author_source_set']) else '미확인'
 out.append(e)
savejson('old-author-source-map.json',{'read_utc':utc(),'scope':'All68 eligible OLD example pages; only old source archive and old HTML/source-tree evidence','old_source_archive_file_count':len(fs),'archive_paths_equal_old_source_tree':True,'rows':out,'new_content_reads':0,'confirmed':sum(x['status']=='YES' for x in out),'unknown':sum(x['status']!='YES' for x in out),'source_minimum_count':0,'count_reason':'Machine source correspondence scan; no claim of68 direct independently reviewed works'})
