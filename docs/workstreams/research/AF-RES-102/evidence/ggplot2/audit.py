from pathlib import Path
import sys,json,re,csv,html,hashlib,concurrent.futures,struct,urllib.parse,base64
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import collect
ed=json.loads((D/'editions.json').read_text());selected=json.loads((D/'selected-stage2.json').read_text());supp=json.loads((D/'supplemental-order.json').read_text())['cases'];frame=json.loads((D/'frame.json').read_text());frameby={x.get('section_path'):x for x in frame if x.get('eligible')}
RAW=collect.RAW

def attrs(tag):
 return {k:html.unescape(a or b or c) for k,a,b,c in re.findall(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))',tag)}
def section(s):
 m=re.search(r'<h2[^>]*id="(ref-examples|examples)"[^>]*>',s)
 if not m:return None
 startdiv=s.rfind('<div class="section level2"',0,m.start());end=len(s)
 if startdiv>=0:
  depth=0
  for t in re.finditer(r'</?div\b[^>]*>',s[startdiv:]):
   depth+=-1 if t.group(0).startswith('</') else 1
   if depth==0:end=startdiv+t.end();break
 else:
  endm=re.search(r'<h2\b',s[m.end():]);end=m.end()+endm.start() if endm else len(s)
 return m.start(),end,s[m.start():end]
def pnginfo(b):
 if not b.startswith(b'\x89PNG\r\n\x1a\n'):return {'signature':'not PNG'}
 w,h=struct.unpack('>II',b[16:24]);return {'signature':'PNG','width':w,'height':h}
def read_case(t):
 caseid,case,edition=t
 ep=ed[edition];page=case['section_path'].split('#')[0];url=RAW+ep['publication_sha']+'/'+page
 key=('old-' if edition=='old' else 'new-')+page.replace('/','_')
 b,r=collect.fetch(key,url);s=b.decode('utf-8');sec=section(s)
 rr={'case_id':caseid,'edition':edition,'version':ep['version'],'body_url':url,'section_url':url+'#ref-examples','body_sha256':r['sha256'],'body_receipt':'evidence/ggplot2/receipts/'+key+'.json','body_utc':r['accessed_utc'],'source_path':case['source_path'],'source_url':RAW+ep['source_sha']+'/'+case['source_path'],'source_sha':ep['source_sha'],'publication_sha':ep['publication_sha'],'section_present':sec is not None,'old_resource_path':case['old_resource_path']}
 if sec is None:return rr
 start,end,txt=sec
 rr.update(section_locator=f'L{s[:start].count(chr(10))+1}–L{s[:end].count(chr(10))+1}',section_sha256=hashlib.sha256(txt.encode()).hexdigest(),base_tags=[attrs(t.group(0)) for t in re.finditer(r'<base\b[^>]*>',s)],section_uri_attributes=[{'tag':t.group(0).split()[0].lstrip('<'),'attrs':attrs(t.group(0)),'line':s[:start+t.start()].count('\n')+1} for t in re.finditer(r'<(?:img|source|picture|script|object|embed|iframe)\b[^>]*>',txt)],script_count=len(re.findall('<script\\b',txt)),picture_count=len(re.findall('<picture\\b',txt)),inline_svg_count=len(re.findall('<svg\\b',txt)),data_uri_count=len(re.findall('data:image/',txt)))
 images=[x for x in rr['section_uri_attributes'] if x['tag']=='img' and not any(y in x['attrs'].get('src','').lower() for y in ['logo','badge'])]
 rr['section_image_count']=len(images)
 rr['legacy_reference_count']=sum(urllib.parse.urljoin(page,x['attrs'].get('src',''))==case['old_resource_path'] for x in images)
 if images:
  im=images[0];src=im['attrs'].get('src','');imstart=next(m.start() for m in re.finditer(r'<img\b[^>]*>',txt) if attrs(m.group(0)).get('src')==src)
  rawbefore=collect.clean(txt[:imstart])
  rr.update(first_image=im,first_literal_reference=src,first_resource_path=urllib.parse.urljoin(page,src),first_image_context_preview=rawbefore[-1800:],first_image_context_digest=hashlib.sha256(rawbefore.encode()).hexdigest())
  base=urllib.parse.urljoin(url,rr['base_tags'][0]['href']) if rr['base_tags'] and 'href' in rr['base_tags'][0] else url
  rr['base_url']=base
  targets=[('src',src)]
  if im['attrs'].get('srcset'):
   targets += [('srcset',x.strip().split()[0]) for x in im['attrs']['srcset'].split(',')]
  # Picture sources, if any, retained and inspected as alternatives rather than silently omitted.
  for x in rr['section_uri_attributes']:
   if x['tag']=='source':
    targets += [('picture_source',z.strip().split()[0]) for z in x['attrs'].get('srcset','').split(',') if z.strip()]
  payloads=[]
  for j,(kind,target) in enumerate(targets):
   if target.startswith('data:'):
    meta,data=target.split(',',1);pb=base64.b64decode(data) if ';base64' in meta else urllib.parse.unquote_to_bytes(data);pr={'status':'embedded','bytes':len(pb),'sha256':hashlib.sha256(pb).hexdigest(),'accessed_utc':r['accessed_utc'],'content_type':meta.split(';')[0][5:]};pu=url+'#'+f'embedded-first-{j}';pk=None
   else:
    pu=urllib.parse.urljoin(base,target);pk=f'{edition}-payload-'+hashlib.sha256(pu.encode()).hexdigest()[:20];pb,pr=collect.fetch(pk,pu)
   payloads.append({'kind':kind,'literal':target,'url':pu,'relative_path':urllib.parse.urljoin(page,target),'status':pr['status'],'mime':pr['content_type'],'bytes':pr['bytes'],'sha256':pr['sha256'],'utc':pr['accessed_utc'],'receipt':f'evidence/ggplot2/receipts/{pk}.json' if pk else rr['body_receipt'],'cache':str((D/'cache'/pk).relative_to(D)) if pk else None,**pnginfo(pb)})
  rr['payloads']=payloads
 sk=f'{edition}-source-'+Path(case['source_path']).name
 sb,srec=collect.fetch(sk,rr['source_url']);ss=sb.decode()
 rr.update(source_sha256=srec['sha256'],source_receipt=f'evidence/ggplot2/receipts/{sk}.json',source_utc=srec['accessed_utc'],source_blob=hashlib.sha1(b'blob '+str(len(sb)).encode()+b'\0'+sb).hexdigest(),source_example_text=ss.split('\\examples{',1)[1] if '\\examples{' in ss else '')
 return rr

def run():
 cases=[(x['case_id'],x) for x in selected if not x.get('vacant')]+[(f'GG-S{i:02}',frameby[x['section_path']]) for i,x in enumerate(supp,1)]
 jobs=[(caseid,case,edition) for caseid,case in cases for edition in ['old','new']]
 out=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
  futures={ex.submit(read_case,j):j for j in jobs}
  for f in concurrent.futures.as_completed(futures):
   j=futures[f]
   try:
    r=f.result();out.append(r);print(json.dumps({'case':r['case_id'],'edition':r['edition'],'section':r['section_locator'],'first':r.get('first_literal_reference'),'legacy_refs':r.get('legacy_reference_count'),'images':r.get('section_image_count'),'sha':r.get('payloads',[{}])[0].get('sha256')},ensure_ascii=False),flush=True)
   except Exception as e:out.append({'case_id':j[0],'edition':j[2],'error':repr(e)});print('ERROR',j[0],j[2],repr(e),flush=True)
 out.sort(key=lambda x:(x['case_id'],x['edition']))
 # Full content previews/source are working inputs, not published evidence.
 (D/'cache'/'audit-full.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 compact=[]
 for x in out:
  y={k:v for k,v in x.items() if k not in ['first_image_context_preview','source_example_text']}
  y['source_examples_sha256']=hashlib.sha256(x.get('source_example_text','').encode()).hexdigest()
  compact.append(y)
 (D/'audit-observations.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2))
 if any(x.get('error') for x in out):raise SystemExit(1)
if __name__=='__main__':run()
