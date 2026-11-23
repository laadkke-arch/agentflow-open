import json,re,base64,hashlib,urllib.parse,concurrent.futures,ast,datetime
from pathlib import Path
from lxml import html
from audit_main import cached,image_info,SectionBounds
from fetch import ROOT
E=json.load(open(ROOT/'editions.json'));F=json.load(open(ROOT/'supplemental-order.json'))['selected']
def ast_fingerprint(s):
 try:
  t=ast.parse(s)
  class Strip(ast.NodeTransformer):
   def visit_Expr(self,n):
    if isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):return None
    return self.generic_visit(n)
  return hashlib.sha256(ast.dump(Strip().visit(t),include_attributes=False).encode()).hexdigest()
 except Exception as e:return 'parse-error:'+str(e)
def one(x,edition):
 p=x['page_path'];base=E[edition]['fixed_base_url'];key=('old-body-' if edition=='old' else 'supp-new-body-')+Path(p).stem
 b,rec=cached(key,base+p,'stage3 fixed supplemental order: '+edition+' scoped example body')
 t=html.fromstring(b);sec=t.xpath('//section[contains(@class,"sphx-glr-example-title")]')[0];s=b.decode();h=sec.xpath('./h1')[0]
 sbounds=SectionBounds(sec.get('id'));sbounds.feed(s)
 imgs=sec.xpath('.//img');first=next((im for im in imgs if im.get('src') or im.get('id','').startswith('_anim_img')),None)
 body={'url':rec['url'],'sha256':rec['sha256'],'bytes':len(b),'utc':rec['utc'],'receipt':'evidence/matplotlib/receipts/'+key+'.json','section_id':sec.get('id'),'section_url':rec['url']+'#'+sec.get('id'),'section_lines':[sbounds.start,sbounds.end],'title':' '.join(h.text_content().split()).rstrip('#'),'image_count':len(imgs),'picture_count':len(sec.xpath('.//picture')),'source_count':len(sec.xpath('.//source')),'script_count':len(sec.xpath('.//script')),'base':t.xpath('//base/@href'),'data_URI_count':s.count('data:image/'),'old_fragment_present':bool(t.xpath('//*[@id=$v]',v=x['old_section_path'].split('#')[1]))}
 first_data=None
 if first is not None:
  literal=first.get('src')
  if literal and not literal.startswith('data:'):
   pk=f'supp-{x["supplemental_id"]}-{edition}-payload';url=urllib.parse.urljoin(rec['url'],literal);pb,pr=cached(pk,url,'supplemental actual first figure payload')
   first_data={'kind':'external','literal_src':literal,'srcset':first.get('srcset'),'line':first.sourceline,'url':url,'path':urllib.parse.urljoin(p,literal),'bytes':len(pb),'sha256':pr['sha256'],'utc':pr['utc'],'receipt':'evidence/matplotlib/receipts/'+pk+'.json','image':image_info(pb)}
  else:
   m=re.search(r'frames\[0\]\s*=\s*"(data:image/png;base64,.*?)"',s,re.S)
   if m:
    value=m.group(1).replace('\\\n','').replace('\\\r\n','');pb=base64.b64decode(value.split(',',1)[1]);js=[{'line':i,'expression':line.strip()[:180]} for i,line in enumerate(s.splitlines(),1) if ('this.frames' in line or '.src =' in line or 'new Animation(' in line or 'img_id =' in line)]
    first_data={'kind':'inline-JS-data-PNG','literal_prefix':'frames[0] = data:image/png;base64,','line':s.count('\n',0,m.start())+1,'img_id':first.get('id'),'img_line':first.sourceline,'url':rec['url']+'#'+sec.get('id'),'path':None,'bytes':len(pb),'sha256':hashlib.sha256(pb).hexdigest(),'utc':rec['utc'],'receipt':body['receipt'],'image':image_info(pb),'frame_count':len(re.findall(r'frames\[\d+\]\s*=',s)),'JS_connection':js}
   else:first_data={'kind':'unresolved-inline','img_line':first.sourceline,'img_id':first.get('id')}
 source=None;dl=sec.xpath('.//div[contains(@class,"download-python")]//a/@href')
 if dl:
  u=urllib.parse.urljoin(rec['url'],dl[0]);sk=f'supp-{x["supplemental_id"]}-{edition}-source';b2,r2=cached(sk,u,'supplemental corresponding delivered Python source')
  source={'url':u,'path':urllib.parse.urljoin(p,dl[0]),'sha256':r2['sha256'],'bytes':len(b2),'utc':r2['utc'],'receipt':'evidence/matplotlib/receipts/'+sk+'.json','cache_key':sk,'ast_without_docstrings_sha256':ast_fingerprint(b2.decode())}
 oldpath=x['old_asset_path'];resolved=[]
 for im in imgs:
  if im.get('src'):resolved.append(urllib.parse.urljoin(p,im.get('src')))
  for val in im.get('srcset','').split(','):
   if val.strip():resolved.append(urllib.parse.urljoin(p,val.strip().split()[0]))
 return {'body':body,'first_figure':first_data,'source':source,'legacy_path_ref_count':sum(v==oldpath for v in resolved) if oldpath else None,'legacy_path_applicable':bool(oldpath),'all_img_refs':[{'line':im.sourceline,'src':im.get('src'),'id':im.get('id')} for im in imgs]}
def pair(x):
 a=one(x,'old');b=one(x,'new');d={'id':x['supplemental_id'],'rank':x['supplemental_rank'],'frame_path':x['page_path'],'old':a,'new':b,'old_source_path':x['source_path'],'comparison':{'source_bytes_same':bool(a['source'] and b['source'] and a['source']['sha256']==b['source']['sha256']),'operational_AST_same':bool(a['source'] and b['source'] and a['source']['ast_without_docstrings_sha256']==b['source']['ast_without_docstrings_sha256']),'first_payload_bytes_same':bool(a['first_figure'].get('sha256') and b['first_figure'].get('sha256') and a['first_figure']['sha256']==b['first_figure']['sha256']),'first_payload_pixels_same':bool(a['first_figure'].get('image',{}).get('pixel_sha256') and b['first_figure'].get('image',{}).get('pixel_sha256') and a['first_figure']['image']['pixel_sha256']==b['first_figure']['image']['pixel_sha256']),'fragment_same':a['body']['section_id']==b['body']['section_id']},'logical_U':'PENDING_MANUAL_REVIEW','legacy_reference_U':'YES' if b['legacy_path_ref_count'] else 'NOT_APPLICABLE_INLINE' if not b['legacy_path_applicable'] else 'NO','inherited_work_exclusion':'098 explicitly read animate_decay3.7.0 inline example; preserve supplemental slot but do not count work/payload as new' if Path(x['page_path']).stem=='animate_decay' else ''}
 print(d['id'],d['frame_path'],d['comparison'],'legacy-ref',d['legacy_reference_U'],flush=True);return d
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:D=list(ex.map(pair,F))
(ROOT/'supplemental-audit-raw.json').write_text(json.dumps({'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_order_source':'supplemental-order.json sealed f1c5d6ff927fd5fbe108565598810ca7e94c5753','pairs':D},ensure_ascii=False,indent=2)+'\n')
