import pathlib,json,csv,datetime,hashlib,urllib.parse
from lxml import html
P=pathlib.Path(__file__).parent
plan=json.loads((P/'discovery-plan.json').read_text());receipt=json.loads((P/'docs-index-receipt.json').read_text());raw=(P/'docs-index.tmp.html').read_bytes();root=html.fromstring(raw)
allanchors=root.xpath('//a[@href]'); indexes={id(x):i for i,x in enumerate(allanchors,1)}
# lxml proxies are stable here because allanchors retains every element.
toc=root.xpath('//*[@id="toc"]')[0]; ul=toc.getnext()
while ul is not None and ul.tag!='ul':ul=ul.getnext()
anchors=ul.xpath('.//a[@href]');observations=[]
for j,a in enumerate(anchors,1):observations.append({'dom_anchor_index':indexes[id(a)],'toc_index':j,'raw_href':a.get('href'),'label':' '.join(a.text_content().split()),'resolved_url':urllib.parse.urljoin(receipt['url'],a.get('href'))})
(P/'toc-hrefs.json').write_text(json.dumps({'source_html_url':receipt['url'],'source_sha256':receipt['sha256'],'checked_utc':receipt['checked_utc'],'version':'미확인 (unversioned published HTML snapshot)','anchors':observations},ensure_ascii=False,indent=2)+'\n')
version_links=[{'href':a.get('href'),'label':' '.join(a.text_content().split())} for a in allanchors if any(s in a.get('href','').lower() for s in ['vega-lite-v4','/v4/','/4.']) or ('version' in a.text_content().lower())]
metadata=[];rows=[];selections=[]
for case in plan['cases']:
 matches=[]
 for a in anchors:
  label=' '.join(a.text_content().split())
  for tok in case['tokens']:
   if tok.casefold() in label.casefold():matches.append((len(tok),indexes[id(a)],tok,a,label))
 if not matches:raise ValueError('unhandled fallback must follow preregistration')
 matches.sort(key=lambda x:(-x[0],x[1]));score,idx,tok,a,label=matches[0]
 li=a.getparent()
 while li is not None and li.tag!='li':li=li.getparent()
 chosen=li.xpath('.//a[@href]')[:6]
 selections.append({'case_id':case['case_id'],'matched_token':tok,'matched_label':label,'matched_anchor_dom_index':idx,'scope':'matched immediate functional li subtree including child ul','scope_total_href_count':len(li.xpath('.//a[@href]')),'selected_first_n':len(chosen),'candidate_body_opened':False,'discovery_rule_effect':'literal-longest-token; generic token may win over shorter specific token; not corrected after seeing candidate suitability'})
 for rank in range(1,7):
  cid=f"{case['case_id']}-{rank}"; empty=rank>len(chosen)
  if empty: href=url=title=''; domidx=''; component=purpose=role='';up='';reason='범주 내 href 부족; 원순서대로 빈 슬롯 유지'
  else:
   b=chosen[rank-1];href=b.get('href');url=urllib.parse.urljoin(receipt['url'],href);title=' '.join(b.text_content().split());domidx=indexes[id(b)];component=urllib.parse.urlsplit(url).path.split('/')[-1].replace('.html','');purpose=title;role='configuration' if 'config' in title.lower() else 'example' if 'example' in title.lower() else 'reference';up='vega/vega-lite';reason='공식 호스트 /vega-lite/docs/ 와 Edit this page repository 링크로 상류 확인; 정확 배포 semver 미확인'
  r={'route':'V','case_id':case['case_id'],'candidate_id':cid,'slot':rank,'layer':'natural','empty_slot':empty,'url':url,'original_url':url,'raw_href':href,'source_html_url':receipt['url'],'source_html_sha256':receipt['sha256'],'source_html_version':'미확인 (unversioned published snapshot)','html_dom_anchor_index':domidx,'category_order':rank if not empty else '', 'category':label,'discovery_token':tok,'source_checked_utc':receipt['checked_utc'],'title':title,'upstream_key':up,'upstream_verified':not empty,'component':component,'purpose':purpose,'version':'미확인','roles':json.dumps([role],ensure_ascii=False) if role else '[]','identity_verified':False,'unknown_reason':reason,'candidate_read_status':'not_yet_read' if not empty else 'empty_slot','discovery_phase':'pool_frozen_before_candidate_body','historical_version_status':'V1 v4 schema evidence remains 미확인; no published v4 link found' if case['case_id']=='V1' else 'request_version_unspecified','label':'원문 보기' if not empty else '', 'description':''}
  rows.append(r)
  if not empty:metadata.append({'candidate_id':cid,'upstream':up,'upstream_evidence':receipt['url']+' ; Edit this page href https://github.com/vega/vega-lite/edit/next/site/docs/overview.md','component':component,'purpose':purpose,'version':'미확인','evidence_roles':[role],'display_metadata_source':'official TOC label / URL path only; no candidate body or gold used','identity_key_complete':False,'singleton_reason':'공개 HTML의 정확 semver 미확인','document_group':urllib.parse.urldefrag(url)[0]})
with (P/'pool-V.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
(P/'metadata-V.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
(P/'discovery-selections.json').write_text(json.dumps({'selections':selections,'actual_version_links_in_start_html':version_links,'version_inference':'none; never rewrote current href into historical URL'},ensure_ascii=False,indent=2)+'\n')
files=['requirements-V.json','frame-V.csv','discovery-plan.json','pool-V.csv','metadata-V.json','toc-hrefs.json','discovery-selections.json']
(P/'freeze-V.json').write_text(json.dumps({'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_bodies_read':False,'group_calculations_performed':False,'requirements_count':4,'slots_count':24,'nonempty_slots':sum(not r['empty_slot'] for r in rows),'sha256':{x:hashlib.sha256((P/x).read_bytes()).hexdigest() for x in files}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(selections,ensure_ascii=False,indent=2));print('nonempty',sum(not r['empty_slot'] for r in rows));print('pool frozen')
