"""AF106 stage 1. Only old publication bytes; no new edition requests."""
import csv, io, json, hashlib, datetime, urllib.request, urllib.parse, concurrent.futures, subprocess, re, ast
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[5]
OLD='f3ac5407f8ffc861cae1ea87eddd06c63b222e4b'
DOC='655f616e86e2c0f7724d7c88717d4ac4eb438c57'
BASE=f'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/{OLD}/3.6.3/'
PIN='092f4c5c56451bceb53e632f4bddf33db6cda168'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b): return hashlib.sha256(b).hexdigest()
def get(key,url):
    dest=ROOT/'.cache'/f'{key}.bin'; recpath=ROOT/'receipts'/f'{key}.json'
    if dest.exists() and recpath.exists(): return dest.read_bytes(),json.loads(recpath.read_text())
    rec={'url':url,'requested_utc':utc(),'phase':'stage1_old_only'}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF106-public-research'}),timeout=90) as r:
            b=r.read();rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
    except Exception as e: b=b'';rec.update(status=getattr(e,'code',None),error=str(e))
    rec.update(received_utc=utc(),bytes=len(b),sha256=digest(b));dest.write_bytes(b);recpath.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
    return b,rec
def inherited(path): return subprocess.check_output(['git','show',f'{PIN}:docs/workstreams/research/AF-RES-102/{path}'],cwd=REPO)
tree_url='https://api.github.com/repos/matplotlib/matplotlib.github.com/git/trees/3252e5b162258de399b9fa614b6854bd9da661f9?recursive=1'
b,rec=get('old-edition-tree',tree_url)
if not b:
    b=inherited('evidence/matplotlib/old-publication-tree.json')
    x=json.loads(b)
    if isinstance(x,list): tree=x
    else: tree=x.get('tree',[])
    complete=True
    rec['inherited_fallback']=True
else:
    x=json.loads(b);tree=x['tree'];complete=not x.get('truncated',True)
assert complete and len(tree)==9489,(complete,len(tree))
pubmap={r['path']:r for r in tree}
(ROOT/'old-publication-paths.json').write_text(json.dumps({'url':tree_url,'tree_sha':'3252e5b162258de399b9fa614b6854bd9da661f9','complete':complete,'entries':tree,'acquisition':rec},ensure_ascii=False,indent=2)+'\n')
oldframe=list(csv.DictReader(io.StringIO(inherited('frame.csv').decode())))
excluded={r['page_path']:'AF-RES-102 eligible first40 / inherited logical example' for r in oldframe if r['project']=='Matplotlib' and r['eligible']=='YES'}
excluded.update({f'gallery/animation/{n}.html':'AF-RES-098 previously scored logical example' for n in ['animation_demo','pause_resume']})
(ROOT/'exclusions.json').write_text(json.dumps({'research_pin':PIN,'paths':excluded,'alias_rule':'identical source path, same source blob, and same complete first-example code+payload identity are merged after old parsing; HBox already among40'},ensure_ascii=False,indent=2)+'\n')
paths=sorted(r['path'] for r in tree if r['type']=='blob' and r['path'].startswith('gallery/') and r['path'].endswith('.html'))
def scrape(path):
    row={'project':'Matplotlib','page_path':path,'eligible':'NO','exclusion':'','old_section_path':'','old_title':'','purpose_visual':'','purpose_api':'','purpose_extraction':'machine extracted from old author prose and calls; selected rows manually reviewed later','old_resource_path':'','asset_kind':'','source_path':'','author_source_path':'examples/'+path[len('gallery/'):-5]+'.py','source_blob':'','body_sha256':'','hash_sha256':'','body_url':BASE+path,'body_receipt':'','source_url':'','base_href':'','srcset':'','fragment':'','first_image_line':'','first_code_sha256':'','alias_of':'','access':'','inspected_directly':'NO'}
    if path in excluded: row['exclusion']=excluded[path];row['access']='inherited_exclusion';return row,None
    if path.endswith('/index.html') or path.endswith('/sg_execution_times.html'):
        row['exclusion']='index/execution summary not logical example';row['access']='tree_only';return row,None
    key='old-'+path.replace('/','_').replace('.html','')
    b,rec=get(key,BASE+path);row.update(body_sha256=rec['sha256'],body_receipt='evidence/matplotlib/receipts/'+key+'.json')
    if rec['status']!=200: row['exclusion']='access failure; eligibility unresolved';row['access']='FAILED';return row,None
    row['access']='automatic_html_read'
    row['old_git_blob_matches']=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==pubmap[path]['sha']
    t=html.fromstring(b);sec=t.xpath('//section[contains(@class,"sphx-glr-example-title")]')
    if not sec:
        redirs=t.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]/@content')
        target=re.split(r'url=',redirs[0],flags=re.I)[-1].strip() if redirs else ''
        row['exclusion']='old publication redirect alias' if target else 'no gallery title section'
        row['alias_of']=urllib.parse.urljoin(path,target) if target else ''
        return row,{'page_path':path,'redirect_target':row['alias_of'],'refresh_content':redirs,'automatic_only':True}
    sec=sec[0];frag=sec.get('id');title=' '.join(sec.xpath('./h1')[0].text_content().split()).rstrip('#').strip()
    text=' '.join(' '.join(sec.xpath('./p[not(contains(@class,"sphx-glr-timing"))]')[i].text_content().split()) for i in range(min(3,len(sec.xpath('./p[not(contains(@class,"sphx-glr-timing"))]')))))
    # Preserve full authored purpose in cache; only compact first prose is in the inventory.
    row.update(fragment=frag,old_section_path=path+'#'+frag,old_title=title,purpose_visual=title+' — '+text[:600])
    bases=t.xpath('//base/@href');row['base_href']=';'.join(bases)
    downloads=t.xpath('//div[contains(@class,"download-python")]//a/@href')
    row['source_path']=urllib.parse.urljoin(path,downloads[0]) if downloads else ''
    row['source_url']=BASE+row['source_path'] if row['source_path'] else ''
    row['source_blob']=pubmap.get(row['source_path'],{}).get('sha','')
    imgs=sec.xpath('.//img');first=next((v for v in imgs if v.get('src') or v.get('id','').startswith('_anim_img')),None)
    codes=sec.xpath('.//div[contains(@class,"highlight-python")]//pre | .//div[contains(@class,"highlight-default")]//pre')
    if not codes: codes=sec.xpath('.//div[contains(@class,"highlight")]//pre')
    codeparts=[]
    if first is not None:
        # Sphinx Gallery associates an output image with the immediately following code block.
        # Include preceding code setup and first following block, then stop before another output.
        for c in codes:
            codeparts.append(c.text_content())
            if c.sourceline>=first.sourceline: break
    else:
        # Download-only pages can start with an import-only block. Continue to the
        # first actionable example block, without absorbing a later example.
        for c in codes:
            codeparts.append(c.text_content())
            try: actionable=any(isinstance(n,ast.Call) for n in ast.walk(ast.parse(c.text_content())))
            except Exception: actionable=bool(re.search(r'[A-Za-z_]\w*\(',c.text_content()))
            if actionable: break
    code='\n'.join(codeparts);row['first_code_sha256']=digest(code.encode())
    calls=[]
    try:
        for n in ast.walk(ast.parse(code)):
            if isinstance(n,ast.Call):
                z=ast.unparse(n.func)
                if z not in calls: calls.append(z)
    except Exception: calls=re.findall(r'([A-Za-z_][A-Za-z_0-9.]+)\(',code)
    row['purpose_api']='; '.join(calls[:25])
    obs={'page_path':path,'title':title,'fragment':frag,'section_start_line':sec.sourceline,'section_end_line':sec.sourceline+html.tostring(sec).count(b'\n'),'code_calls':calls,'code':code,'first_prose':text,'base_hrefs':bases,'picture_count':len(sec.xpath('.//picture')),'source_element_count':len(sec.xpath('.//source')),'images':[{k:v for k,v in z.attrib.items() if not v.startswith('data:')} for z in imgs],'source_path':row['source_path'],'old_body_sha256':row['body_sha256'],'automatic_only':True}
    if not code or (first is None and not row['source_path']):
        row['exclusion']='no code' if not code else 'no linked Python source'
        return row,obs
    uri=first.get('src','') if first is not None else '';row['first_image_line']=first.sourceline if first is not None else ''
    row['srcset']=first.get('srcset','') if first is not None else ''
    if uri and not uri.startswith('data:'):
        row['old_resource_path']=urllib.parse.urljoin(path,uri);row['asset_kind']='external-relative' if not urllib.parse.urlparse(uri).scheme else 'external-absolute'
    elif first is not None: row['asset_kind']='inline-data' if uri else 'inline-js-data'
    else: row['asset_kind']='download-python';row['old_resource_path']=row['source_path']
    row['eligible']='YES';row['hash_sha256']=digest(('AF106|Matplotlib|'+row['old_section_path']).encode())
    obs['first_resource_ref']={k:v for k,v in first.attrib.items() if not v.startswith('data:')} if first is not None else {'download_python':row['source_path']}
    return row,obs
rows=[];observations=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    futs={ex.submit(scrape,p):p for p in paths}
    for i,f in enumerate(concurrent.futures.as_completed(futs),1):
        row,obs=f.result();rows.append(row)
        if obs: observations.append(obs)
        if i%50==0: print('old scanned',i,'/',len(paths),flush=True)
rows.sort(key=lambda x:x['page_path']);observations.sort(key=lambda x:x['page_path'])
seen={}
inherited_blobs={r.get('source_blob'):r['page_path'] for r in oldframe if r['project']=='Matplotlib' and r['eligible']=='YES' and r.get('source_blob')}
for row in rows:
    if row['eligible']!='YES': continue
    if row['source_blob'] in inherited_blobs:
        row['eligible']='NO';row['alias_of']=inherited_blobs[row['source_blob']];row['exclusion']='same source blob alias of inherited40';continue
    key=(row['source_blob'],row['first_code_sha256'],row['old_resource_path'])
    if key in seen:
        row['eligible']='NO';row['alias_of']=seen[key];row['exclusion']='same old source+code+payload alias'
    else: seen[key]=row['page_path']
fields=list(dict.fromkeys(k for r in rows for k in r))
with (ROOT/'stage1-frame.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
(ROOT/'old-observations.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
summary={'finished_utc':utc(),'project':'Matplotlib','old_version':'3.6.3','old_publication':OLD,'old_documented_source':DOC,'old_source_tag':'c23ccdde6f0f8c071b09a88770e24452f2859e99','tree_entries':len(tree),'tree_complete':complete,'all_gallery_html':len(paths),'inherited_eligible40':40,'eligible_remaining':sum(r['eligible']=='YES' for r in rows),'exclusion_counts':dict(Counter(r['exclusion'] for r in rows if r['eligible']!='YES')),'asset_kinds':dict(Counter(r['asset_kind'] for r in rows if r['eligible']=='YES')),'access_counts':dict(Counter(r['access'] for r in rows)),'all_received_body_blob_matches':all(r.get('old_git_blob_matches',True) for r in rows),'new_tree_reads':0,'new_body_reads':0,'new_diff_content_reads':0,'machine_html_reads_not_counted_unique_materials':sum(r['access']=='automatic_html_read' for r in rows),'direct_materials':0}
(ROOT/'stage1-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
