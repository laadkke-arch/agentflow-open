import json,sys,datetime,csv,urllib.parse,re,hashlib,io,concurrent.futures,struct
from pathlib import Path
from lxml import html
from html.parser import HTMLParser
from PIL import Image
from fetch import get,ROOT
E=json.load(open(ROOT/'editions.json'));S=json.load(open(ROOT/'selected-stage2.json'))['selected']
old_tree={x['path']:x for x in json.load(open(ROOT/'old-publication-tree.json'))['tree']}
new_tree={x['path']:x for x in json.load(open(ROOT/'cache/stage2-new-edition-tree.bin'))['tree']}
def cached(key,url,scope):
 p=ROOT/'cache'/f'{key}.bin';r=ROOT/'receipts'/f'{key}.json'
 if p.exists() and r.exists():return p.read_bytes(),json.load(open(r))
 return get(key,url,scope)
def image_info(b):
 im=Image.open(io.BytesIO(b));im.load();return {'format':im.format,'width':im.width,'height':im.height,'mode':im.mode,'metadata':dict(im.info),'pixel_sha256':hashlib.sha256(im.tobytes()).hexdigest()}
class SectionBounds(HTMLParser):
 def __init__(self,frag):
  super().__init__();self.frag=frag;self.depth=0;self.start=None;self.end=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='section':
   if self.depth:self.depth+=1
   elif a.get('id')==self.frag:self.depth=1;self.start=self.getpos()[0]
 def handle_endtag(self,tag):
  if tag=='section' and self.depth:
   self.depth-=1
   if self.depth==0:self.end=self.getpos()[0]
def audit(x,edition):
 if x['vacancy']:return {'case_id':x['case_id'],'edition':edition,'version':E[edition]['version'],'vacancy':True,'reason':x['vacancy_reason'],'P':'UNKNOWN','U':'UNKNOWN','G':'UNKNOWN'}
 path=x['page_path'];base=E[edition]['fixed_base_url'];key=('old-body-' if edition=='old' else 'main-new-body-')+Path(path).stem
 b,rec=cached(key,base+path,'stage3 precise '+edition+' main example body; post remote seal f1c5d6ff927fd5fbe108565598810ca7e94c5753')
 t=html.fromstring(b);frag=x['old_section_path'].split('#',1)[1];sec=(t.xpath('//*[@id=$id]',id=frag) or t.xpath('//section[contains(@class,"sphx-glr-example-title")]'))[0]
 text=b.decode();bounds=SectionBounds(sec.get('id'));bounds.feed(text);start=bounds.start;end=bounds.end;serialized=html.tostring(sec,encoding='unicode')
 heads=[{'tag':e.tag,'id':e.get('id'),'text':' '.join(e.text_content().split()).rstrip('#')} for e in sec.xpath('.//*[self::h1 or self::h2 or self::h3]')]
 imgs=[{'line':im.sourceline,'attributes':dict(im.attrib)} for im in sec.xpath('.//img')]
 srcsets=[{'line':el.sourceline,'tag':el.tag,'value':el.get('srcset')} for el in sec.xpath('.//*[@srcset]')]
 uri_forms={'base':t.xpath('//base/@href'),'img_count':len(imgs),'picture_count':len(sec.xpath('.//picture')),'source_count':len(sec.xpath('.//source')),'svg_count':len(sec.xpath('.//svg')),'script_count':len(sec.xpath('.//script')),'data_url_count':len(re.findall('data:',serialized)),'js_frame_assignments':len(re.findall(r'frames\[\d+\]',serialized))}
 first=next((i for i in imgs if i['attributes'].get('src') or i['attributes'].get('id','').startswith('_anim_img')),None)
 refs=[]
 if first and first['attributes'].get('src'):
  refs.append({'kind':'img src','literal':first['attributes']['src'],'line':first['line'],'density':'1x'})
  for value in first['attributes'].get('srcset','').split(','):
   tok=value.strip().split()
   if tok and tok[0]!=first['attributes']['src']:refs.append({'kind':'img srcset','literal':tok[0],'line':first['line'],'density':tok[1] if len(tok)>1 else '1x'})
 payloads=[]
 for i,ref in enumerate(refs):
  u=urllib.parse.urljoin(base+path,ref['literal']);p=urllib.parse.urljoin(path,ref['literal']);pk=f'main-{x["case_id"]}-{edition}-payload-{i}'
  # reuse precisely received old 1x payload; do not re-request
  reuse=('stage1-'+x['case_id']+'-payload') if x['case_id'].startswith('MP-G') else ('stage2-'+x['case_id']+'-old-payload')
  if edition=='old' and i==0:pk=reuse
  pb,pr=cached(pk,u,'stage3 actual scoped first figure '+ref['kind']);payloads.append({**ref,'path':p,'url':u,'final_url':pr['final_url'],'http_status':pr['status'],'bytes':len(pb),'sha256':pr['sha256'],'receipt':'evidence/matplotlib/receipts/'+pk+'.json','publication_tree_present':p in (old_tree if edition=='old' else new_tree),'image':image_info(pb)})
 downloads=sec.xpath('.//div[contains(@class,"download-python")]//a/@href')
 source=None
 if downloads:
  sp=urllib.parse.urljoin(path,downloads[0]);su=urllib.parse.urljoin(base+path,downloads[0]);sk=f'main-{x["case_id"]}-{edition}-source'
  if edition=='old':sk='stage1-'+x['case_id']+'-source' if x['case_id'].startswith('MP-G') else 'stage2-'+x['case_id']+'-old-source'
  sb,sr=cached(sk,su,'stage3 corresponding delivered Download Python source')
  source={'path':sp,'url':su,'bytes':len(sb),'sha256':sr['sha256'],'receipt':'evidence/matplotlib/receipts/'+sk+'.json','tree_blob':(old_tree if edition=='old' else new_tree).get(sp,{}).get('sha'),'lines':len(sb.splitlines()),'source_cache':sk}
 docver=re.findall(r'v3\.[67]\.\d+(?:-\d+-g[0-9a-f]+)?',text)
 return {'case_id':x['case_id'],'project':'Matplotlib','edition':edition,'version':E[edition]['version'],'vacancy':False,'section_url':base+path+'#'+sec.get('id'),'section_id':sec.get('id'),'old_fragment_present':bool(t.xpath('//*[@id=$id]',id=frag)),'section_lines':[start,end],'boundary':'section.sphx-glr-example-title containing h1; through matching closing section before following peer/footer','headings':heads,'purpose_frozen':x['purpose'],'body_url':rec['url'],'body_sha256':rec['sha256'],'body_bytes':rec['bytes'],'body_utc':rec['utc'],'body_receipt':'evidence/matplotlib/receipts/'+key+'.json','uri_forms':uri_forms,'images':imgs,'srcsets':srcsets,'first_payloads':payloads,'delivered_source':source,'doc_version_metadata':sorted(set(docver)),'legacy_asset_path':x['old_asset_path'],'legacy_path_P':'YES' if x['old_asset_path'] in (old_tree if edition=='old' else new_tree) else 'NO','P':'YES' if payloads and all(p['publication_tree_present'] and p['http_status']==200 for p in payloads) else 'UNKNOWN','U':'PENDING_SEMANTIC_READ','G':'UNKNOWN','G_missing_link':'No preserved exact invocation-to-output digest evidence yet.'}
if __name__=='__main__':
 jobs=[(x,e) for x in S for e in ['old','new']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  A=list(ex.map(lambda j:audit(*j),jobs))
 (ROOT/'main-audit-raw.json').write_text(json.dumps({'postseal_remote_commit':'f1c5d6ff927fd5fbe108565598810ca7e94c5753','records':A},ensure_ascii=False,indent=2)+'\n')
 for a in A:
  if a['vacancy']:print(a['case_id'],a['edition'],'VACANT');continue
  print(a['case_id'],a['edition'],a['section_lines'],a['uri_forms'],[(p['path'],p['bytes'],p['sha256'],p['image']['width'],p['image']['height']) for p in a['first_payloads']],a['doc_version_metadata'])
