"""Post-seal content retrieval and exact reference extraction; no prediction writes."""
from collect import *
from concurrent.futures import ThreadPoolExecutor
import struct

def section(path,b,edition):
 s=b.decode();m=re.search(r'<h2[^>]*id="(ref-examples|examples)"[^>]*>',s)
 if not m:raise ValueError('No Examples heading '+path)
 start=s.rfind('<div class="section level2"',0,m.start());end=len(s)
 if start>=0:
  depth=0
  for t in re.finditer(r'</?div\b[^>]*>',s[start:]):
   depth+=-1 if t.group().startswith('</') else 1
   if depth==0:end=start+t.end();break
 else:
  em=re.search(r'<h2\b',s[m.end():]);end=m.end()+em.start() if em else len(s)
 sec=s[m.end():end];ims=list(re.finditer(r'<img\b[^>]*>',sec));im=next(x for x in ims if not any(w in x.group().lower() for w in ['logo','badge']))
 aa=attrs(im.group());bases=re.findall(r'<base\b[^>]*>',s);base=next((attrs(t).get('href') for t in bases if attrs(t).get('href')),RAW+edition+'/'+path)
 code=re.sub(r'^Examples\s*','',clean(sec[:im.start()]));line=s[:m.start()].count('\n')+1
 links=list(dict.fromkeys(html.unescape(x) for x in re.findall(r'https://github.com/tidyverse/ggplot2/blob/[^/]+/([^"<>]+)',s) if x.startswith(('R/','man/'))))
 allimgs=[{'attrs':attrs(x.group()),'relative_to_page':urllib.parse.urljoin(path,attrs(x.group()).get('src','')),'line':s[:m.end()+x.start()].count('\n')+1} for x in ims]
 return {'fragment':m[1],'dom_ids':re.findall(r'\bid="([^"]+)"',s),'section_start_line':line,'section_end_line':s[:end].count('\n')+1,'first_image_line':s[:m.end()+im.start()].count('\n')+1,'first_example_code':code,'image_attributes':aa,'first_asset_url':urllib.parse.urljoin(base,aa.get('src','')),'first_asset_relative_path':urllib.parse.urljoin(path,aa.get('src','')),'base_tags':bases,'srcset':aa.get('srcset',''),'picture_elements':re.findall(r'<picture\b[^>]*>.*?</picture>',sec,re.S),'svg_count':len(re.findall(r'<svg\b',sec)),'data_uri_count':sec.count('data:image/'),'script_references':re.findall(r'<script[^>]+src="([^"]+)"',sec),'all_example_images':allimgs,'author_source_paths':links,'all_example_code_sha256':sha(clean(sec).encode()),'body_sha256':sha(b),'body_git_blob':gitsha(b),'raw_url':RAW+edition+'/'+path,'github_url':'https://github.com/tidyverse/ggplot2/blob/'+edition+'/'+path+'#L'+str(line),'original_dom_url':RAW+edition+'/'+path+'#'+m[1]}

def main():
 frame={r['page_path']:r for r in json.loads((D/'frame.json').read_text())}
 pr=json.loads((D/'predictions.json').read_text());sp=json.loads((D/'supplemental-selection.json').read_text())
 selected=[{'case_id':r['case_id'],'page_path':r['old_section_path'].split('#')[0],'group':'main'} for r in pr if r['vacant']=='NO']
 selected.extend({'case_id':r['case_id'],'page_path':r['page_path'],'group':'material_control'} for r in sp['minimum_material_controls'])
 selected.extend({'case_id':'GG-S'+str(i),'page_path':e['prespecified_representative_page'],'group':'supplemental','event_sha':e['sha']} for i,e in enumerate(sp['selected_events'],1))
 def tree(name):return {x['path']:x for x in json.loads((D/name).read_text())['tree'] if x['type']=='blob'}
 trees={'old':tree('old-tree.json'),'new':tree('new-publication-tree.json')};strees={'old':tree('old-source-tree.json'),'new':tree('new-source-tree.json')}
 jobs=[(r,w,pin,src) for r in selected for w,pin,src in [('old',OLD,OSRC),('new',NEW,NSRC)]]
 def job(j):
  r,w,pin,src=j;path=r['page_path'];stem=Path(path).stem;tr=trees[w];st=strees[w]
  body,bc=fetch(w+'-body-'+Path(path).name,RAW+pin+'/'+path);assert gitsha(body)==tr[path]['sha']
  d=section(path,body,pin);d.update(case_id=r['case_id'],group=r['group'],page_path=path,edition=w,version='3.4.0' if w=='old' else '3.5.0',body_receipt='evidence/ggplot2/receipts/'+w+'-body-'+Path(path).name+'.json',body_accessed_utc=bc['accessed_utc'],purpose_visual_original=frame[path]['purpose_visual'],purpose_api_original=frame[path]['purpose_api'])
  asset,ac=fetch(w+'-asset-'+stem+'.png',d['first_asset_url']);ap=d['first_asset_relative_path'];assert ap in tr and gitsha(asset)==tr[ap]['sha']
  d['payload']={'url':d['first_asset_url'],'relative_path':ap,'sha256':sha(asset),'git_blob':gitsha(asset),'bytes':len(asset),'format':'PNG' if asset.startswith(b'\x89PNG') else 'other','width':struct.unpack('>I',asset[16:20])[0] if asset.startswith(b'\x89PNG') else None,'height':struct.unpack('>I',asset[20:24])[0] if asset.startswith(b'\x89PNG') else None,'receipt':'evidence/ggplot2/receipts/'+w+'-asset-'+stem+'.png.json','accessed_utc':ac['accessed_utc']}
  (D/'payloads'/(w+'-'+stem+'.png')).write_bytes(asset)
  sourcepath='man/'+stem+'.Rd';sb,sc=fetch(w+'-man-'+stem+'.Rd',RAW+src+'/'+sourcepath);assert sourcepath in st and gitsha(sb)==st[sourcepath]['sha'];ss=sb.decode();ln=ss.splitlines()
  source={'path':sourcepath,'url':RAW+src+'/'+sourcepath,'sha256':sha(sb),'git_blob':gitsha(sb),'bytes':len(sb),'generated_header':next((x for x in ln if 'Please edit documentation in' in x),''),'examples_line':next((i+1 for i,x in enumerate(ln) if '\\examples{' in x),None),'receipt':'evidence/ggplot2/receipts/'+w+'-man-'+stem+'.Rd.json','accessed_utc':sc['accessed_utc'],'examples_text':ss[ss.find('\\examples{'):] if '\\examples{' in ss else ''}
  authors=[]
  for ap in re.findall(r'R/[^,\s]+',source['generated_header']):
   ab,rc=fetch(w+'-author-'+ap.replace('/','_'),RAW+src+'/'+ap);assert ap in st and gitsha(ab)==st[ap]['sha'];astr=ab.decode()
   authors.append({'path':ap,'url':RAW+src+'/'+ap,'sha256':sha(ab),'git_blob':gitsha(ab),'bytes':len(ab),'examples_marker_lines':[i+1 for i,x in enumerate(astr.splitlines()) if '@examples' in x],'receipt':'evidence/ggplot2/receipts/'+w+'-author-'+ap.replace('/','_')+'.json','accessed_utc':rc['accessed_utc']})
  d.update(render_source=source,author_sources=authors);savejson('details/'+w+'-'+stem+'.json',d)
  print(json.dumps({'case':r['case_id'],'edition':w,'page':path,'code':d['first_example_code'],'image':d['payload'],'source':sourcepath,'author_sources':[a['path'] for a in authors]},ensure_ascii=False),flush=True)
  return d
 for n in ['details','payloads']:(D/n).mkdir(exist_ok=True)
 result=list(ThreadPoolExecutor(max_workers=4).map(job,jobs))
 savejson('audit-extraction.json',{'postseal_commit':'8054c2221d4023ba03c904d96f13928219d36c3d','completed_utc':utc(),'selected':selected,'rows':result,'note':'Static extraction/retrieval only; final purpose/method judgments are separate actual readings.'})
if __name__=='__main__':main()
