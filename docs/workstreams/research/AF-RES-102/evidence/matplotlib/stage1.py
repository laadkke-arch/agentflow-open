import sys,json,csv,re,hashlib,datetime,urllib.parse,base64,struct,concurrent.futures
from lxml import html
from fetch import get,ROOT
OLD_PUB='f3ac5407f8ffc861cae1ea87eddd06c63b222e4b'
OLD_SRC='c23ccdde6f0f8c071b09a88770e24452f2859e99'
OLD_BASE=f'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/{OLD_PUB}/3.6.3/'
def load(key):return json.loads((ROOT/'cache'/f'{key}.bin').read_bytes())
tree=load('old-edition-tree')['tree'];pubmap={x['path']:x for x in tree};src={x['path']:x for x in load('old-source-tree')['tree']}
paths=sorted(x['path'] for x in tree if x['type']=='blob' and x['path'].startswith('gallery/') and x['path'].endswith('.html'))
rows=[];n=0;reads=[]
for ix,path in enumerate(paths,1):
 row={'project':'Matplotlib','frame_path_rank':ix,'page_path':path,'eligible':'NO','eligible_rank':'','exclusion':'','old_section_path':'','old_title':'','purpose':'','old_asset_path':'','asset_kind':'','old_body_sha256':'','body_url':OLD_BASE+path,'body_receipt':'','source_path':'examples/'+path.removeprefix('gallery/').removesuffix('.html')+'.py','source_blob':'','tag_source_path':'','tag_source_blob':'','hash_key':'','hash_sha256':''}
 if path.endswith('/index.html') or path.endswith('/sg_execution_times.html'):
  row['exclusion']='gallery index or execution-time summary, not one explanatory example';rows.append(row);continue
 if path in ['gallery/animation/animation_demo.html','gallery/animation/pause_resume.html']:
  row['exclusion']='AF-RES-098 main logical example excluded by contract';rows.append(row);continue
 key='old-body-'+path.split('/')[-1].replace('.html','')
 cache=ROOT/'cache'/f'{key}.bin';rp=ROOT/'receipts'/f'{key}.json'
 if cache.exists():b=cache.read_bytes();rec=json.loads(rp.read_text())
 else:b,rec=get(key,OLD_BASE+path,'stage1 OLD exact-publication gallery body, before new path/body/payload exposure')
 row['body_receipt']=str(rp.relative_to(ROOT.parent.parent));row['old_body_sha256']=rec['sha256']
 if rec['status']!=200:row['exclusion']='access failure; eligibility unresolved';rows.append(row);continue
 t=html.fromstring(b);heads=t.xpath('//section[contains(@class,"sphx-glr-example-title")]/h1')
 if not heads:row['exclusion']='no gallery example section/h1';rows.append(row);continue
 sec=heads[0].getparent();title=heads[0].text_content().strip().rstrip('#').strip();frag=sec.get('id');text=' '.join(sec.text_content().split())
 imgs=sec.xpath('.//img');first=next((im for im in imgs if im.get('src') or (im.get('id','').startswith('_anim_img'))),None)
 row['old_section_path']=path+'#'+frag;row['old_title']=title;row['purpose']='Visual illustration for '+title
 row['tag_source_path']=row['source_path'];row['tag_source_blob']=src.get(row['source_path'],{}).get('sha','')
 refs=sec.xpath('.//div[contains(@class,"download-python")]//a/@href')
 row['source_path']=urllib.parse.urljoin(path,refs[0]) if refs else ''
 row['source_blob']=pubmap.get(row['source_path'],{}).get('sha','')
 obs={'path':path,'title':title,'section_id':frag,'section_start_line':sec.sourceline,'first_paragraph_excerpt':' '.join((' '.join(p.text_content() for p in sec.xpath('./p')[:1])).split()[:max(0,18-len(title.split()))]),'img_count':len(imgs),'source_count':len(sec.xpath('.//source')),'script_count':len(sec.xpath('.//script')),'base_hrefs':t.xpath('//base/@href'),'download_refs':sec.xpath('.//div[contains(@class,"download-python")]//a/@href'),'body_receipt':row['body_receipt']}
 if first is None:
  row['exclusion']='no first explanatory image/inline animation in scoped body';obs['decision']=row['exclusion'];reads.append(obs);rows.append(row);print(ix,path,'EXCLUDE',flush=True);continue
 srcuri=first.get('src')
 if srcuri and not srcuri.startswith('data:'):
  row['asset_kind']='external-relative' if not urllib.parse.urlparse(srcuri).scheme else 'external-absolute'
  row['old_asset_path']=urllib.parse.urljoin(path,srcuri)
  obs['first_reference']={k:v for k,v in first.attrib.items()};obs['first_reference_line']=first.sourceline
 else:
  row['asset_kind']='inline-js-data-png' if not srcuri else 'inline-data'
  row['old_asset_path']=''
  obs['first_reference']={k:v for k,v in first.attrib.items()};obs['first_reference_line']=first.sourceline
  s=b.decode();m=re.search(r'frames\[0\]\s*=\s*"(data:image/png;base64,.*?)";',s,re.S)
  if m:
   value=m.group(1).replace('\\\n','').replace('\\\r\n','');p=base64.b64decode(value.split(',',1)[1]);obs['inline_first_png']={'bytes':len(p),'sha256':hashlib.sha256(p).hexdigest(),'width':struct.unpack('>I',p[16:20])[0],'height':struct.unpack('>I',p[20:24])[0],'frame_assignment_line':s.count('\n',0,m.start())+1}
   obs['frame_assignment_count']=len(re.findall(r'frames\[\d+\]\s*=',s))
  else:obs['inline_unresolved']='No frames[0] data png extraction; inspect manually'
 n+=1;row['eligible']='YES';row['eligible_rank']=n;row['hash_key']='AF-RES-102|Matplotlib|'+row['old_section_path'];row['hash_sha256']=hashlib.sha256(row['hash_key'].encode()).hexdigest();obs['decision']='eligible';reads.append(obs);rows.append(row)
 print(ix,n,path,title,row['asset_kind'],row['old_asset_path'],flush=True)
 if n==40:break
with (ROOT/'frame.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'old-body-observations.json').write_text(json.dumps(reads,ensure_ascii=False,indent=2)+'\n')
general=sorted([r for r in rows if r['eligible']=='YES'],key=lambda r:r['hash_sha256'])[:2]
for i,r in enumerate(general,1):r['case_id']=f'MP-G{i}';r['stratum']='general';r['stratum_rank']=i
(ROOT/'selected-general.json').write_text(json.dumps({'selected_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hash_convention':'SHA256 UTF-8 literal AF-RES-102|Matplotlib| + site-relative page path + #fragment','selected':general},ensure_ascii=False,indent=2)+'\n')
print('GENERAL',[(r['case_id'],r['page_path'],r['hash_sha256']) for r in general],flush=True)
