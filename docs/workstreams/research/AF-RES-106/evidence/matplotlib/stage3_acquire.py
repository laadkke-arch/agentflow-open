"""Fetch outcome material only after parent confirms remote prediction seal."""
from pathlib import Path
import json,csv,urllib.request,urllib.parse,datetime,hashlib,concurrent.futures,re,subprocess,struct
from lxml import html
ROOT=Path(__file__).resolve().parent
OLD='f3ac5407f8ffc861cae1ea87eddd06c63b222e4b';NEW='410d8388303fab638bbedbd1d2eace0e5efb0de9'
DOC={'old':'655f616e86e2c0f7724d7c88717d4ac4eb438c57','new':'235131a6bc2527aee7eea370fd5f94564a48c20d'}
VERSION={'old':'3.6.3','new':'3.7.0'};PUB={'old':OLD,'new':NEW}
BASE={k:f'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/{PUB[k]}/{VERSION[k]}/' for k in PUB}
for d in ['payloads','diffs']:(ROOT/d).mkdir(exist_ok=True)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def get(key,url,case,kind):
    cp=ROOT/'.cache'/f'{key}.bin';rp=ROOT/'receipts'/f'{key}.json'
    if cp.exists() and rp.exists():return cp.read_bytes(),json.loads(rp.read_text())
    rec={'id':key,'url':url,'case':case,'kind':kind,'phase':'stage3_after_remote_prediction_seal','prediction_seal':'8054c2221d4023ba03c904d96f13928219d36c3d','requested_utc':utc()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF106-public-research'}),timeout=90) as r:
            b=r.read();rec.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
    except Exception as e:
        b=e.read() if hasattr(e,'read') else b'';rec.update(status=getattr(e,'code',None),error=str(e))
    rec.update(received_utc=utc(),bytes=len(b),sha256=sha(b));cp.write_bytes(b);rp.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');return b,rec
pubmaps={}
pubmaps['old']={x['path']:x for x in json.loads((ROOT/'old-publication-paths.json').read_text())['entries']}
pubmaps['new']={x['path']:x for x in json.loads((ROOT/'new-publication-tree.json').read_text())['tree']}
authormaps={k:{x['path']:x for x in json.loads((ROOT/(k+'-author-tree.json')).read_text())['tree']} for k in ['old','new']}
pred=list(csv.DictReader((ROOT/'predictions.csv').open()));controls=json.loads((ROOT/'control-selection.json').read_text());frame=list(csv.DictReader((ROOT/'frame.csv').open()))
cases=[dict(x,case_group='main') for x in pred if x['vacant']=='NO']
for i,x in enumerate(controls['body_controls'],1):cases.append(dict(x,case_id=f'MP-CONTROL{i}',case_group='control'))
aux=next(x for x in frame if x['page_path']=='gallery/pyplots/pyplot_mathtext.html');cases.append(dict(aux,case_id='MP-SUP1',case_group='supplemental'))
def page_read(case,edition):
    orig=case['page_path'];path=orig;cid=case['case_id'];hops=[]
    for hop in range(5):
        key=('old-'+path.replace('/','_').replace('.html','')) if edition=='old' else (f's3-{cid}-{edition}-body-{hop}')
        if edition=='old' and (ROOT/'.cache'/f'{key}.bin').exists():
            b=(ROOT/'.cache'/f'{key}.bin').read_bytes();rec=json.loads((ROOT/'receipts'/f'{key}.json').read_text());cached=True
        else:b,rec=get(key,BASE[edition]+path,cid,'body');cached=False
        hoprec={'path':path,'url':BASE[edition]+path,'receipt':'evidence/matplotlib/receipts/'+key+'.json','status':rec['status'],'body_sha256':rec['sha256'],'bytes':len(b),'cached_stage1':cached,'direct_read_utc':utc()}
        hops.append(hoprec)
        if rec['status']!=200:return {'case_id':cid,'edition':edition,'failure':rec,'hops':hops}
        t=html.fromstring(b);ref=t.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]/@content')
        if ref:
            target=re.split('url=',ref[0],flags=re.I)[-1].strip();resolved=urllib.parse.urljoin(path,target);hoprec['meta_refresh']=ref[0];hoprec['target']=resolved
            path=resolved.split('#',1)[0];continue
        break
    secs=t.xpath('//section[contains(@class,"sphx-glr-example-title")]')
    if not secs:return {'case_id':cid,'edition':edition,'hops':hops,'failure':'no gallery example title after redirects'}
    sec=secs[0];fragment=sec.get('id');heading=' '.join(sec.xpath('./h1')[0].text_content().split()).rstrip('#')
    images=sec.xpath('.//img');first=images[0] if images else None
    sources=t.xpath('//div[contains(@class,"download-python")]//a/@href');source_path=urllib.parse.urljoin(path,sources[0]) if sources else ''
    code='\n\n'.join(x.text_content() for x in sec.xpath('.//div[contains(@class,"highlight")]//pre'))
    obs={'case_id':cid,'case_group':case['case_group'],'edition':edition,'version':VERSION[edition],'publication_sha':PUB[edition],'documented_source_sha':DOC[edition],'original_page_path':orig,'page_path':path,'hops':hops,'body_url':BASE[edition]+path,'body_sha256':sha(b),'actual_fragment':fragment,'actual_section_url':BASE[edition]+path+'#'+fragment,'github_section_url':f'https://github.com/matplotlib/matplotlib.github.com/blob/{PUB[edition]}/{VERSION[edition]}/{path}#L{sec.sourceline}','section_start_line':sec.sourceline,'section_html_line_count':html.tostring(sec).count(b'\n')+1,'title':heading,'all_dom_ids':t.xpath('//@id'),'base_hrefs':t.xpath('//base/@href'),'picture_count':len(sec.xpath('.//picture')),'source_element_count':len(sec.xpath('.//source')),'object_embed_svg_count':len(sec.xpath('.//object|.//embed|.//svg')),'first_image_line':first.sourceline if first is not None else None,'source_path':source_path,'code':code,'prose':' '.join(' '.join(x.text_content().split()) for x in sec.xpath('./p')),'image_references':[dict(x.attrib) for x in images],'resources':[],'observed_utc':utc(),'scope':'static fixed HTML/code/resources; no browser or example execution'}
    sectionfile=ROOT/'observations'/f'{cid}-{edition}-section.html';sectionfile.write_bytes(html.tostring(sec,encoding='utf-8'));obs['section_snapshot']='evidence/matplotlib/observations/'+sectionfile.name
    urls=[]
    if first is not None:
        u=first.get('src','')
        if u and not u.startswith('data:'):urls.append(('primary',urllib.parse.urljoin(path,u)))
        for entry in first.get('srcset','').split(','):
            parts=entry.strip().split()
            if parts and not parts[0].startswith('data:'):
                resolved=urllib.parse.urljoin(path,parts[0])
                if resolved not in [x[1] for x in urls]:urls.append(('srcset '+(' '.join(parts[1:]) or '1x'),resolved))
    elif source_path:urls.append(('primary_download',source_path))
    for n,(role,respath) in enumerate(urls):
        k=f's3-{cid}-{edition}-payload-{n}';data,rr=get(k,BASE[edition]+respath,cid,'payload')
        ext=Path(respath).suffix or '.bin';saved=ROOT/'payloads'/f'{cid}-{edition}-{n}{ext}';saved.write_bytes(data)
        rr=dict(rr,role=role,path=respath,preserved_path='evidence/matplotlib/payloads/'+saved.name,tree_present=respath in pubmaps[edition],tree_blob=pubmaps[edition].get(respath,{}).get('sha',''),git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())
        if data.startswith(b'\x89PNG\r\n\x1a\n'):rr.update(width=struct.unpack('>I',data[16:20])[0],height=struct.unpack('>I',data[20:24])[0])
        obs['resources'].append(rr)
    if source_path:
        k=f's3-{cid}-{edition}-source';data,rr=get(k,BASE[edition]+source_path,cid,'published_source');saved=ROOT/'payloads'/f'{cid}-{edition}.py';saved.write_bytes(data)
        obs['published_source']=dict(rr,path=source_path,preserved_path='evidence/matplotlib/payloads/'+saved.name,git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),tree_blob=pubmaps[edition].get(source_path,{}).get('sha',''))
        author='examples/'+path.removeprefix('gallery/').removesuffix('.html')+'.py'
        obs['author_source_path']=author;obs['author_source_url']=f'https://raw.githubusercontent.com/matplotlib/matplotlib/{DOC[edition]}/{author}'
        if author in authormaps[edition] and case['case_group'] in ['main','supplemental']:
            data,ar=get(f's3-{cid}-{edition}-author',obs['author_source_url'],cid,'author_source');saved=ROOT/'payloads'/f'{cid}-{edition}-author.py';saved.write_bytes(data)
            obs['author_source']=dict(ar,path=author,preserved_path='evidence/matplotlib/payloads/'+saved.name,tree_blob=authormaps[edition][author]['sha'],git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),matches_published_source=sha(data)==obs['published_source']['sha256'])
    obs['old_fragment_in_final_html']=case['old_section_path'].split('#',1)[1] in obs['all_dom_ids']
    (ROOT/'observations'/f'{cid}-{edition}.json').write_text(json.dumps(obs,ensure_ascii=False,indent=2)+'\n');return obs
obs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    futs={ex.submit(page_read,c,ed):(c['case_id'],ed) for c in cases for ed in ['old','new']}
    for f in concurrent.futures.as_completed(futs):
        r=f.result();obs.append(r);print(r['case_id'],r['edition'],r.get('page_path'),r.get('actual_fragment'),r.get('failure',''),flush=True)
(ROOT/'stage3-materials.json').write_text(json.dumps({'prediction_seal':'8054c2221d4023ba03c904d96f13928219d36c3d','observed_utc':utc(),'cases':sorted(obs,key=lambda r:(r['case_id'],r['edition']))},ensure_ascii=False,indent=2)+'\n')
# Sources from different logical examples than directly counted bodies.
extra=[]
for ix,c in enumerate(controls['source_only'],1):
    for ed in ['old','new']:
        sp=c['source_path'];url=BASE[ed]+sp;key=f's3-MP-SOURCE{ix}-{ed}';b,rec=get(key,url,f'MP-SOURCE{ix}','independent_example_source');out=ROOT/'payloads'/f'MP-SOURCE{ix}-{ed}.py';out.write_bytes(b)
        extra.append(dict(rec,source_id=f'MP-SOURCE{ix}',edition=ed,old_logical_example=c['page_path'],source_path=sp,preserved_path='evidence/matplotlib/payloads/'+out.name,tree_present=sp in pubmaps[ed],tree_blob=pubmaps[ed].get(sp,{}).get('sha',''),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(ROOT/'independent-sources.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
# Read the six prespecified change commits; merge entries remain duplicate events.
supp=json.loads((ROOT/'supplemental-selection.json').read_text());patches=[]
for e in supp['selected']:
    cmd=['git','-C',str(ROOT/'.cache/source-history.git'),'show','--format=fuller','--find-renames=50%',e['sha'],'--','examples/','doc/conf.py','doc/users/prev_whats_new/','doc/users/whats_new.rst']
    start=utc();r=subprocess.run(cmd,capture_output=True,text=True);out=ROOT/'diffs'/(e['sha']+'.patch');out.write_text(r.stdout)
    patches.append(dict(e,command=cmd,start_utc=start,end_utc=utc(),exit_code=r.returncode,patch_sha256=sha(r.stdout.encode()),preserved_path='evidence/matplotlib/diffs/'+out.name,stderr=r.stderr))
(ROOT/'change-receipts.json').write_text(json.dumps(patches,ensure_ascii=False,indent=2)+'\n')
print('DONE',len(obs),'edition bodies',len(extra),'independent source approaches',len(patches),'change commits',flush=True)
