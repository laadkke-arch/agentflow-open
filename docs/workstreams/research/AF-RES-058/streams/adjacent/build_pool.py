import json,pathlib,re,urllib.request,datetime,concurrent.futures,html,hashlib
P=pathlib.Path(__file__).parent
records=json.load(open(P/'crossref-score-metadata.json'))
seen={}
for r in records:
 d=r['doi'];v=' '.join(r['venue'] or []);t=' '.join(r['title'] or [])
 if d in seen:seen[d]['discoveries'].append([r['query_id'],r['rank']]);continue
 rr=dict(r);rr['discoveries']=[[r['query_id'],r['rank']]];seen[d]=rr
# Fallback official ACL entries are title metadata only; this does not open PDFs.
for fn in sorted(P.glob('b*web*.json'))+sorted(P.glob('bacl_s1_*.json')):
 for rank,r in enumerate(json.load(open(fn))['results'],1):
  u=r['url'];m=re.match(r'https://aclanthology.org/([0-9A-Z][^/]*?)(?:\.pdf)?/?$',u)
  if not m:continue
  aid=m.group(1);year=int(('20'+aid[1:3]) if aid[0].isalpha() else aid[:4])
  if not 2015<=year<=2025:continue
  doi='10.18653/v1/'+aid.lower();title=r['title']
  if doi in seen:seen[doi]['discoveries'].append([fn.name,rank]);continue
  seen[doi]={'doi':doi,'title':[title],'venue':['ACL Anthology'],'event':{},'published':{'date-parts':[[year]]},'published_online':None,'published_print':None,'url':'https://aclanthology.org/'+aid+'/','discoveries':[[fn.name,rank]],'anthology_id':aid}
selected=[];audit=[]
# Topic-only screen: explanations/rationales or human advice/decision/judgment/reliance/trust. Machine-only factuality/evidence retrieval titles outside topical combination are excluded.
topic=re.compile(r'explan|rationale|human|advice|reliance|trust|crowd|guardian',re.I)
for r in seen.values():
 d=r['doi'];v=' '.join(r['venue'] or []);t=' '.join(r['title'] or [])
 venueok=(d.startswith(('10.18653/v1/','10.3115/v1/')) or any(z in v for z in ['Human Factors in Computing Systems','Intelligent User Interfaces','ACM SIGIR']))
 reason='candidate'
 if not venueok:reason='venue outside CHI/IUI/SIGIR/ACL'
 elif any(z in v for z in ['Extended Abstracts','Companion']):reason='companion/extended abstract rather than formal paper pool'
 elif not topic.search(t):reason='metadata title lacks explanation/rationale or human-advice decision topic; computational evidence/fact-checking alone'
 elif 'survey' in t.lower():reason='metadata identifies survey, not original experiment'
 rr={**r,'metadata_screen':reason}
 audit.append(rr)
 if reason=='candidate':selected.append(rr)
# Official landing metadata for all selected ACL papers; results/abstract content not extracted.
def aclmeta(r):
 d=r['doi'];aid=r.get('anthology_id',d.split('/v1/')[-1]);u='https://aclanthology.org/'+aid+'/'
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();entry={'query':'official candidate metadata','url':u,'utc':t,'exposure':'citation meta only; no PDF/abstract extraction'}
 try:
  b=urllib.request.urlopen(u,timeout=25).read();s=b.decode();entry.update(status=200,sha256=hashlib.sha256(b).hexdigest());(P/'_cache'/('meta-'+aid+'.html')).write_bytes(b)
  metas={html.unescape(m.group(1)):html.unescape(m.group(2)) for m in re.finditer(r'<meta\s+name="?([^"\s>]+)"?\s+content="([^"]*)"',s)}
  for k in ['citation_title','citation_publication_date','citation_doi','citation_conference_title','citation_pdf_url']:
   if k in metas:r[k]=metas[k]
  # Hugo often uses unquoted name but quoted content; separately reliable DOI link.
  dm=re.search(r'name=citation_doi content="?([^" >]+)',s)
  if dm:r['citation_doi']=dm.group(1)
  entry['meta']=metas
 except Exception as e:entry['error']=str(e)
 return r,entry
acl=[r for r in selected if r['doi'].startswith(('10.18653','10.3115'))]
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(aclmeta,acl))
with (P/'search-log.jsonl').open('a') as fp:
 for r,l in results:fp.write(json.dumps(l,ensure_ascii=False)+'\n')
for r in selected:
 parts=(r.get('published_online') or r.get('published') or {})['date-parts'][0];precision=len(parts)
 pd=r.get('citation_publication_date')
 if pd:
  a=re.split('[-/]',pd);parts=[int(x) for x in a if x.isdigit()];precision=len(parts)
 elif len(parts)<2:
  ep=r.get('event',{}).get('start',{}).get('date-parts',[[]])[0]
  if len(ep)>len(parts):parts=ep;precision=len(parts);r['date_source']='event month only, publication day unavailable'
 r['date_precision']=precision;r['sort_date']='-'.join(str(v).zfill(4 if i==0 else 2) for i,v in enumerate(parts+[1]*(3-len(parts))))
selected=sorted(selected,key=lambda r:(r['sort_date'],r['doi']))
for i,r in enumerate(selected,1):r['pool_rank']=i;r['method_screen_budget_status']='in_first30' if i<=30 else 'over_budget_not_reviewed'
(P/'metadata-screen.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
(P/'metadata.json').write_text(json.dumps({'rule':'R1; metadata title topical screen, results not used','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unique_metadata_count':len(seen),'topic_candidates':len(selected),'method_pool':selected[:30],'beyond_budget':selected[30:],'exposure':'search snippets/abstracts automatic; no deliberate results table or PDF yet'},ensure_ascii=False,indent=2))
for r in selected:print(r['pool_rank'],r['sort_date'],r['doi'],' '.join(r['title']),r.get('citation_title'))
