"""Post-seal candidate, merge-diff and current version-URL verification.
Sealed recruitment and predictions are read, never changed.
"""
from pathlib import Path
import json,hashlib,datetime,urllib.request,urllib.parse,concurrent.futures,zipfile,subprocess,re
from lxml import html
R=Path(__file__).resolve().parent
P='410d8388303fab638bbedbd1d2eace0e5efb0de9'
B=f'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/{P}/3.7.0/'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def get(key,url,cid,kind):
 cp=R/'.cache'/f'{key}.bin';rp=R/'receipts'/f'{key}.json'
 if cp.exists() and rp.exists():return cp.read_bytes(),json.loads(rp.read_text())
 x={'id':key,'url':url,'case':cid,'kind':kind,'phase':'stage3_after_remote_prediction_seal','prediction_seal':'8054c2221d4023ba03c904d96f13928219d36c3d','requested_utc':utc()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AF106-public-research'}),timeout=45) as z:b=z.read();x.update(status=z.status,final_url=z.url,content_type=z.headers.get('Content-Type'))
 except Exception as e:b=e.read() if hasattr(e,'read') else b'';x.update(status=getattr(e,'code',None),error=str(e))
 x.update(received_utc=utc(),bytes=len(b),sha256=sha(b));cp.write_bytes(b);rp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return b,x
# Candidate examples that match the original barchart objective's distinctive words/data.
z=zipfile.ZipFile(R/'.cache/new-gallery-python.zip')
paths=['units/bar_unit_demo.py','statistics/barchart_demo.py','subplots_axes_and_figures/figure_title.py','lines_bars_and_markers/hat_graph.py','event_handling/pong_sgskip.py','lines_bars_and_markers/bar_colors.py','lines_bars_and_markers/horizontal_barchart_distribution.py','lines_bars_and_markers/bar_label_demo.py','pie_and_polar_charts/bar_of_pie.py','misc/demo_agg_filter.py']
cands=[]
for p in paths:
 b=z.read(p);out=R/'observations'/('candidate-'+p.replace('/','_'));out.write_bytes(b)
 page='gallery/'+p.removesuffix('.py')+'.html';key='s3-candidate-'+p.replace('/','_').removesuffix('.py')
 hb,rec=get(key,B+page,'MP-G2','negative_successor_candidate_body')
 if rec['status']!=200:cands.append(dict(rec,page_path=page,logical_code_path=p));continue
 t=html.fromstring(hb);sec=t.xpath('//section[contains(@class,"sphx-glr-example-title")]')[0]
 section=html.tostring(sec,encoding='utf-8');sp=R/'observations'/(key+'-section.html');sp.write_bytes(section)
 code='\n\n'.join(x.text_content() for x in sec.xpath('.//div[contains(@class,"highlight")]//pre'))
 cands.append(dict(rec,page_path=page,actual_fragment=sec.get('id'),github_section_url=f'https://github.com/matplotlib/matplotlib.github.com/blob/{P}/3.7.0/{page}#L{sec.sourceline}',logical_code_path=p,source_in_bundle_sha256=sha(b),code=code,prose=' '.join(' '.join(x.text_content().split()) for x in sec.xpath('./p')),preserved_section='evidence/matplotlib/observations/'+sp.name,preserved_bundle_source='evidence/matplotlib/observations/'+out.name))
 print('CANDIDATE',p,rec['status'],flush=True)
(R/'barchart-successor-candidates.json').write_text(json.dumps(cands,ensure_ascii=False,indent=2)+'\n')
# The first git show returned no merge patch: preserve it and explicitly retry against first parent.
merges=[]
for sh in ['dbe0ee669262350aaae877bf7c83c9e9909cd8c4','7ffc3e4a6a057d6117529163187592816830e9cf','ebba21ad5e0403e3c4df15ca5e7f631428fd5e4d']:
 cmd=['git','-C',str(R/'.cache/source-history.git'),'show','--format=fuller','--diff-merges=first-parent','--find-renames=50%',sh,'--','examples/']
 start=utc();r=subprocess.run(cmd,capture_output=True,text=True);p=R/'diffs'/(sh+'.first-parent.patch');p.write_text(r.stdout)
 merges.append(dict(sha=sh,command=cmd,start_utc=start,end_utc=utc(),exit_code=r.returncode,patch_sha256=sha(r.stdout.encode()),preserved_path='evidence/matplotlib/diffs/'+p.name,bytes=p.stat().st_size,stderr=r.stderr,reason='default git show gave empty merge patch; first-parent diff needed; duplicate event, count0'))
(R/'merge-diff-receipts.json').write_text(json.dumps(merges,ensure_ascii=False,indent=2)+'\n')
# Current version site checked against immutable section + associated byte payload, not browser execution.
materials=json.loads((R/'stage3-materials.json').read_text())['cases']
def live(x):
 cid=x['case_id'];ed=x['edition'];url=f"https://matplotlib.org/{x['version']}/{x['page_path']}";k=f's3-live-{cid}-{ed}'
 b,r=get(k,url,cid,'live_version_body');o=dict(r,edition=ed,fixed_body_url=x['body_url'],expected_fragment=x['actual_fragment'],matched_static_section=False,browser_execution='미실시')
 if r['status']==200:
  t=html.fromstring(b);s=t.xpath('//*[@id=$i]',i=x['actual_fragment'])
  if s:
   code='\n\n'.join(y.text_content() for y in s[0].xpath('.//div[contains(@class,"highlight")]//pre'));imgs=[dict(y.attrib) for y in s[0].xpath('.//img')]
   o.update(fragment_present=True,code_sha256=sha(code.encode()),fixed_code_sha256=sha(x['code'].encode()),code_equal=(code==x['code']),image_references_equal=(imgs==x['image_references']),images=imgs)
   o['matched_static_section']=o['code_equal'] and o['image_references_equal']
  else:o['fragment_present']=False
  resource=x['resources'][0];pb,pr=get(k+'-payload',f"https://matplotlib.org/{x['version']}/{resource['path']}",cid,'live_version_payload')
  o['payload_receipt']=pr;o['payload_equal_fixed']=pr['status']==200 and pr['sha256']==resource['sha256'];o['recommended_url']=url+'#'+x['actual_fragment'] if o['matched_static_section'] and o['payload_equal_fixed'] else '미확인'
 print('LIVE',cid,ed,r['status'],o.get('matched_static_section'),o.get('payload_equal_fixed'),flush=True);return o
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:live_results=list(e.map(live,[x for x in materials if x['case_group']=='main']))
(R/'live-url-verification.json').write_text(json.dumps(live_results,ensure_ascii=False,indent=2)+'\n')
print('DONE',flush=True)
