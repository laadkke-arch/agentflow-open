"""Consolidate explicit collector ledgers; do not fetch or overwrite sealed A bytes."""
from pathlib import Path
import json,csv,hashlib,re,collections
from urllib.parse import urlsplit,urlunsplit
P=Path(__file__).resolve().parents[1]
def jl(f):return [json.loads(x) for x in (P/f).read_text().splitlines() if x.strip()]
def jo(f):return json.loads((P/f).read_text())
def dump(f,x): (P/f).write_text(json.dumps(x,ensure_ascii=False,indent=2))
def writecsv(f,rows):
 cols=list(dict.fromkeys(k for r in rows for k in r))
 with (P/f).open('w',newline='') as out:
  w=csv.DictWriter(out,fieldnames=cols,lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows)
def first(d,*keys,default=None):
 for k in keys:
  if d.get(k) is not None:return d[k]
 return default
source_files=['collectors/python/sources.jsonl','collectors/offline/sources.jsonl','collectors/cran/final/sources.jsonl','collectors/b/sources.jsonl','collectors/python/followup/sources.jsonl','collectors/offline/followup/sources.jsonl','collectors/cran/followup/sources.jsonl','collectors/cross/sources.jsonl','collectors/b/root-sources.jsonl','collectors/offline/b05/sources.jsonl','collectors/cross/b/sources.jsonl']
rows=[]
for fn in source_files:
 for n,r in enumerate(jl(fn),1):
  group=r.get('duplicate_group',r['source_id']);cat=first(r,'count_category','minimum_category','minimum_bucket','category',default='other_primary')
  if cat=='A_distribution':cat='A_original'
  counted=first(r,'count_minimum','counted_for_minimum',default=False)
  s={'source_id':r['source_id'],'kind':first(r,'kind','source_type','material_type',default='primary record'),'publisher':first(r,'publisher','author_or_publisher',default='미확인; see collector'),'original_url':r.get('original_url'),'version':first(r,'version','version_or_tag',default='미확인'),'publication_date':first(r,'publication_date','published_at',default='미확인'),'observed_at_utc':first(r,'observed_at_utc','checked_at_utc','observed_utc','UTC','fetched_at_utc',default='미확인'),'read_location':first(r,'read_location','directly_read_location',default='collector record'),'member':first(r,'distribution_member','member_path','member'),'findings':first(r,'findings','confirmed','verified',default='see collector record'),'limits':first(r,'limits','limitations','cannot_confirm',default='see collector record'),'questions':r.get('questions',[]),'reference_ids':first(r,'reference_ids','case_ids',default=[]),'duplicate_group':group,'count_minimum':bool(counted),'count_category':cat,'collector_requested_minimum':bool(counted),'collector_record':fn+':'+str(n),'sha256':first(r,'sha256','body_sha256','artifact_sha256','archive_sha256'),'member_sha256':r.get('member_sha256'),'publication_date_role':first(r,'publication_date_role','publication_role','published_at_basis',default='see collector record; no inference from mtime')}
  rows.append(s)
ids=[r['source_id'] for r in rows];assert len(ids)==len(set(ids)),[k for k,v in collections.Counter(ids).items() if v>1]
parent={i:i for i in ids}
def find(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(a,b):
 a,b=find(a),find(b)
 if a!=b:parent[b]=a
seen_group={};seen_url={}
for r in rows:
 sid=r['source_id'];g=r['duplicate_group'];u=r['original_url'] or ''
 if g in parent:union(sid,g)
 if g in seen_group:union(sid,seen_group[g])
 else:seen_group[g]=sid
 member=r['member']
 archive=bool(re.search(r'\.(?:tar\.gz|tar\.bz2|zip|deb|tgz)(?:\?|$)',u))
 if archive and not member:
  m=re.search(r'([\w./-]+\.html)',str(r['read_location']));member=m.group(1) if m else g
 # Same manuscript at same source URI: HTML/API duplicates and dated rereads are not new originals.
 key=u.replace('.json','')+('::'+str(member) if archive else '')
 if key and key in seen_url:union(sid,seen_url[key])
 else:seen_url[key]=sid
groups=collections.defaultdict(list)
for r in rows:groups[find(r['source_id'])].append(r)
dedup=[]
for grp,items in groups.items():
 counted=[r for r in items if r['count_minimum']]
 chosen=counted[0]['source_id'] if counted else None
 for r in items:
  r['minimum_counting_group']=grp;r['minimum_representative']=chosen
  r['collector_duplicate_group']=r['duplicate_group']
  r['duplicate_group']=('member-sha256:'+r['member_sha256']) if r['member_sha256'] else ('source-uri:'+str(r['original_url']) if 'absent' not in str(r['findings']).lower() and '멤버 없음' not in str(r['findings']) else 'absence-observation:'+r['source_id'])
  r['duplicate_group_role']='exact member bytes or same original manuscript URI; broad collector lineage is recorded separately'
  r['minimum_counting_group_role']='conservative minimum selection; may join different meaning states or member absences; not an identical-body assertion'
  if r['count_minimum'] and r['source_id']!=chosen:r['count_minimum']=False;r['global_exclusion_reason']='conservative minimum group already represented at '+chosen+'; this does not assert identical content'
 if len(items)>1:dedup.append({'minimum_counting_group':grp,'is_identical_body_assertion':False,'source_ids':[r['source_id'] for r in items],'minimum_representative':chosen})
(P/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));dump('evidence/source-deduplication.json',dedup)
source_map={r['source_id']:r for r in rows}
# Preserve A prefix verbatim, append separately selected B observations.
sealed=(P/'evidence/a-sealed.jsonl').read_bytes();assert hashlib.sha256(sealed).hexdigest()=='b3c2f68b905102f0fa682ab45a34c0f3401a69b61ba0a59327045e04a626d562'
A=[json.loads(x) for x in sealed.decode().splitlines()];amap={r['reference_id']:r for r in A}
case_files=['collectors/python/followup/cases.json','collectors/offline/followup/cases.json','collectors/cran/followup/cases.json','collectors/b/root-cases.json','collectors/offline/b05/cases.json','collectors/cross/b/cases.json']
cases=[]
for fn in case_files:
 for c in jo(fn):c['collector_case_file']=fn;cases.append(c)
assert len(cases)==18
L2={r['rid']:r for r in jo('evidence/masked/B-L2-input.json')};crossrefs=jl('collectors/cross/b/references.jsonl')
out=[];Brefs=[]
for c in sorted(cases,key=lambda x:x['reference_id']):
 rid=c['reference_id'];sample=rid[0];r=amap.get(rid,{});cur=c.get('current',c.get('current_http',{}));cur=cur if isinstance(cur,dict) else {'status_description':cur,'final_url':c.get('current_destination'),'section_evidence':c.get('current_section_presence')}
 verdict=c.get('verdict',c.get('purpose_judgment','보류').split(' — ')[0].strip());old=c.get('last_observed_old',c.get('last_old'));new=c.get('first_observed_new');bound=c.get('boundaries',[])
 change=bool(c.get('actual_consumer_href_changed',c.get('same_purpose_href_changed',False)) or any(b.get('same_frozen_purpose') and b.get('new_href') and b.get('new_href')!=b.get('old_href') for b in bound))
 sids=c.get('source_ids',[])
 if not sids:sids=[s['source_id'] for s in rows if rid in s['reference_ids']]
 purpose=first(r,'purpose',default=first(c,'purpose','frozen_purpose',default=L2.get(rid,{}).get('purpose')))
 unknown=c.get('unknowns',[])
 if not unknown:unknown=[{'reason':x,'last_verified':c.get('last_checked'),'next_minimum_source':c.get('next_material')} for x in c.get('unconfirmed',[])]
 raw=first(r,'raw_href',default=first(c,'raw_href','old_href',default=L2.get(rid,{}).get('URL')))
 nr={'reference_id':rid,'sample':sample,'route':r.get('route','B_event_first'),'consumer':r.get('consumer_project',c.get('consumer')),'version':r.get('consumer_version',c.get('original_version',L2.get(rid,{}).get('edition'))),'raw_href':raw,'resolved_url':r.get('resolved_url',raw),'link_text':r.get('link_text',c.get('link_text',L2.get(rid,{}).get('link_text'))),'purpose':purpose,'minimum_success':r.get('minimum_success',c.get('minimum_success')),'intent_unknown':r.get('intent_unknown'),'artifact_url':first(r,'artifact_url','archive_url',default=c.get('original_archive')),'artifact_sha256':first(r,'artifact_sha256','archive_sha256',default=c.get('original_archive_sha256')),'member':first(r,'member','member_path',default=c.get('original_member')),'member_sha256':r.get('member_sha256',c.get('original_member_sha256')),'context':r.get('surrounding_text',r.get('context')),'event_key':first(c,'upstream_event_key','event_key'),'verdict':verdict,'verdict_actor':'researcher applying sealed stated purpose at current observation','verdict_reason':first(c,'verdict_reason','rationale','purpose_judgment'),'current_http':cur,'last_old':old,'first_observed_new':new,'boundaries':bound,'same_purpose_href_changed':change,'dates':c.get('date_roles',{k:c.get(k) for k in ['upstream_effective','source_edit','merge','build','publication','reader_report']}),'strict_upstream_publication_eligible':False,'right_censored':False,'duplicate_of_A':'A-D04' if rid=='B05' else None,'query_count':first(c,'query_count','queries_used',default=0),'candidate_document_count':first(c,'candidate_document_count','candidate_document_families_used','candidate_families',default=0),'unknowns':unknown,'source_ids':sids,'collector_case_file':c['collector_case_file'],'raw_collector_case':c}
 if sample=='B':
  nr['minimum_success']=L2[rid]['minimum_success_and_intent_limit']
  nr['intent_unknown']='Combined purpose/intent limit supplied by extractor in evidence/masked/B-L2-input.json; '+L2[rid]['minimum_success_and_intent_limit']
  if rid=='B02':nr['dates']['publication']={'time':'2022-05-04T00:20:02Z','role':'CRAN DESCRIPTION Date/Publication of httr1.4.3 with actual built HTML','source_id':'B02-httr-1.4.3'}
  cr=next((x for x in crossrefs if x['reference_id']==rid),None)
  if cr:
   s=source_map[cr['source_id']];nr.update(artifact_url=s['original_url'],artifact_sha256=s['sha256'],member=cr.get('base_url'),context=cr.get('context_paraphrase'))
  if rid=='B05':
   base=amap['A-D04'];nr.update(artifact_url=base.get('artifact_url',base.get('archive_url')),artifact_sha256=base.get('artifact_sha256',base.get('archive_sha256')),member=base.get('member',base.get('member_path')),member_sha256=base['member_sha256'],context=base.get('surrounding_text'))
  if rid=='B04':
   ss=source_map['CB-S15'];nr.update(version='SphinxSitemap2.2.0 source / current HTML only',artifact_url=ss['original_url'],artifact_sha256=ss['sha256'],member=ss['member'] or 'sphinx-sitemap-2.2.0/README.rst',member_sha256=ss['member_sha256']);nr['dates']['source_distribution_publication']={'times':c.get('consumer_publication_dates'),'role':'PyPI source upload; not HTML publication'}
   nr['current_http']={'requested_url':raw,'final_url':None,'final_http_status':429,'status_description':'Original request redirected to a Google error/sorry response (302 then429); intended final content not observed. Separate canonical request returned200.','needed_section_present':None,'separately_opened_canonical_url':c.get('current_destination'),'separately_opened_canonical_status':200,'separately_opened_canonical_section_evidence':c.get('current_section_presence'),'evidence':['collectors/cross/b/downloads7.json:google75712','collectors/cross/b/downloads8.json:google-sitemapindex','CB-S20'],'interpretation':'Independent canonical GET is not the original request final destination; no original-path200 claim.'}
  nr['published_html_eligible']=rid!='B04';nr['exposure_media_limit']=c.get('artifact_form','actual distributed archive HTML' if rid in ['B02','B03','B05'] else 'see collector')
  bref={k:v for k,v in nr.items() if k not in ['raw_collector_case','dates','unknowns','current_http','boundaries']};bref.update(A_B_duplicate=rid=='B05',B_event_seal_commit='ffbce62e4c01459ebbfb006a5d6c67e425ed7c17',A_seal_unchanged=True,reference_selected_at='after B event seal; see direct-read timestamps in sources',raw_href_string_role='consumer HTML href except B04 source/currentHTML candidate; historicalHTML unconfirmed')
  Brefs.append(bref)
 out.append(nr)
(P/'references.jsonl').write_bytes(sealed+''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in Brefs).encode());dump('evidence/cases-normalized.json',out)
# Sampling frame: document exclusions and link exclusions have distinct units.
frame=[]
for fn,unit in [('collectors/python/frame.csv','link_or_selected_document'),('collectors/offline/frame.csv','document'),('collectors/cran/final/frame.csv','document')]:
 for r in csv.DictReader((P/fn).open()):frame.append({'unit':unit,'phase':'pre_A_seal','collector_frame':fn,'project':r.get('project'),'edition':first(r,'edition','version'),'date':first(r,'date','release_date','publication_utc'),'member':first(r,'member','member_path'),'disposition':first(r,'decision','disposition','status'),'reference_id':first(r,'reference_id','selected_reference_id','frame_id'),'details':r})
for r in jo('collectors/cran/final/candidate-archives.json'):
 if r['project'] not in ['knitr','rmarkdown','dplyr']:frame.append({'unit':'candidate_project_edition','phase':'pre_A_seal','collector_frame':'collectors/cran/final/candidate-archives.json','project':r['project'],'edition':r['name'],'date':r['date'],'disposition':'not_reached_after_first6_date_ordered_documents; not failure','details':r})
writecsv('frame.csv',frame)
ed=[]
for fn in ['collectors/python/followup/editions.csv','collectors/cran/followup/editions.csv','collectors/offline/followup/editions.csv','collectors/b/root-editions.csv','collectors/cross/b/editions.csv']:
 for r in csv.DictReader((P/fn).open()):
  if fn.endswith('cross/b/editions.csv'):
   s=source_map.get(r.get('source_id'),{});typ=s.get('kind','')
   if not any(k in typ.lower() for k in ['consumer','source package','source distribution','versioned','sdist','archive']):continue
  ed.append({'record_unit':'artifact inventory' if 'offline/followup' in fn else 'member or source receipt','collector_editions':fn,**r})
writecsv('editions.csv',ed)
chains=[];ints=[]
for c in out:
 rid=c['reference_id'];chains.append({'reference_id':rid,'sample':c['sample'],'event_key':c['event_key'],'source_ids':c['source_ids'],'upstream_and_consumer_clocks':c['dates'],'last_old':c['last_old'],'first_observed_new':c['first_observed_new'],'additional_boundaries':c['boundaries'],'http_status':first(c['current_http'],'final_http_status','status','status_description'),'final_url':c['current_http'].get('final_url'),'separately_opened_canonical_url':c['current_http'].get('separately_opened_canonical_url'),'separately_opened_canonical_status':c['current_http'].get('separately_opened_canonical_status'),'fragment_presence':first(c['current_http'],'fragment_presence','fragment_present','final_fragment_present'),'purpose_verdict':c['verdict'],'same_purpose_href_changed':c['same_purpose_href_changed'],'duplicate_of_A':c['duplicate_of_A'],'strict_eligible':False,'right_censored':False,'unknowns':c['unknowns']})
  # Strict row exists for every sealed attempt, including B without an eligible HTML pair.
 ints.append({'interval_id':rid+'-strict','reference_id':rid,'sample':c['sample'],'event_key':c['event_key'],'clock_pair':'upstream_effective→same_purpose_consumer_publication','start':None,'end':None,'eligible':False,'strict_eligible':False,'conditional_denominator':0,'seconds':None,'right_censored':False,'reason':'미확인: exact paired clocks/HTML or same purpose missing; details in chains','source_ids':c['source_ids'],'next_material':c['unknowns'][0] if c['unknowns'] else 'same-event publication evidence'})
for fn in ['collectors/cran/followup/intervals.json','collectors/python/followup/intervals.json','collectors/b/root-intervals.json']:
 for r in jo(fn):
  if ('strict' in r.get('interval_id','')) or r.get('clock_pair')=='upstream_effective→consumer_publication':continue
  rid=r['reference_id'];cc=next(c for c in out if c['reference_id']==rid);ss=[x for x in cc['source_ids'] if '-C' in x or x.endswith('SOURCE')];ee=cc.get('first_observed_new') or {};ee=ee.get('source_id');pairs=[x for x in [r.get('start_source'),r.get('end_source'),*(ss or []),ee] if x];elig=r.get('eligible_for_aux_source_publication',r.get('eligible',False));ints.append({'interval_id':r.get('interval_id',rid+'-'+r['clock_pair']),'reference_id':rid,'sample':rid[0],'event_key':cc['event_key'],'source_ids':list(dict.fromkeys(pairs or cc['source_ids'])),'clock_pair':r.get('clock_pair'),'start':r.get('start'),'end':r.get('end'),'eligible':elig,'strict_eligible':False,'seconds':r.get('seconds',r.get('seconds_nominal')),'right_censored':False,'collector_interval':fn,'details':r})
writecsv('chains.csv',chains);writecsv('intervals.csv',ints)
# Measured counts, not inferred failure/success rates.
counted=[s for s in rows if s['count_minimum']];ac=[x for x in out if x['sample']=='A'];bc=[x for x in out if x['sample']=='B'];rs=jo('collectors/cran/followup/summary.json')
archive_urls=set(r['url'] for r in jo('collectors/python/followup/archives.json'))
offline=list(csv.DictReader((P/'collectors/offline/followup/editions.csv').open()));cran=list(csv.DictReader((P/'collectors/cran/followup/editions.csv').open()))
archive_urls|={r['archive_url'] for r in offline if r['archive_read']=='True'};archive_urls|={r['url'] for r in cran if not r['error']}
present=sum(r['member_exists']=='True' for r in cran)+38+52
counts={'A_references':12,'A_distinct_documents':12,'A_projects':6,'A_routes':{'D':6,'R':6},'A_actual_archives_including_baseline':len(archive_urls),'A_member_state_observations':38+52+len(cran),'A_present_HTML_members_read':present,'A_missing_document_members':sum(r['member_exists']=='False' for r in cran),'A_same_purpose_href_changed_references':sum(c['same_purpose_href_changed'] for c in ac),'A_independent_source_correction_events':4,'A_verdicts':dict(collections.Counter(c['verdict'] for c in ac)),'B_attempts':6,'B_queries':sum(c['query_count'] for c in bc),'B_candidate_documents':sum(c['candidate_document_count'] for c in bc),'B_published_HTML_consumers_observed':sum(c['published_html_eligible'] for c in bc),'B_HTML_exposure_forms':{'actual_archives':3,'versioned_web_only':2,'historical_HTML_unconfirmed':1},'B_A_duplicates':1,'B_additional_independent_HTML_consumers':4,'B_same_purpose_href_changed_including_duplicate':sum(c['same_purpose_href_changed'] for c in bc),'B_same_purpose_href_changed_excluding_A_duplicate':sum(c['same_purpose_href_changed'] and not c['duplicate_of_A'] for c in bc),'B_verdicts':dict(collections.Counter(c['verdict'] for c in bc)),'strict_pairs_found_A_of12':0,'strict_pairs_found_B_of6':0,'conditional_eligible_denominator':0,'conditional_result':'해당 없음','right_censored':0,'same_medium_reader_failure_chains':0,'ancillary_reader_live_web_report':1,'aux_source_to_publication_A_reference_pairs':3,'aux_source_to_publication_A_independent_events':2,'aux_source_to_publication_B_reference_pairs':1,'source_ledger_rows':len(rows),'unique_minimum_originals':len(counted),'unique_minimum_by_category':dict(collections.Counter(s['count_category'] for s in counted)),'cross_field_pairs':2,'sqlite_read_editions':5,'sqlite_enumerated_editions':51,'sqlite_unread_editions':46,'A_seal_sha256':hashlib.sha256(sealed).hexdigest(),'count_units_note':'Rows/URLs/archives/manuscripts/events differ. Missing HTML member is an observed absence; unread edition is not absence. B05 is not independent.'}
dump('evidence/counts.json',counts)
writecsv('evidence/event-source-counts.csv',[{'reference_id':c['reference_id'],'event_key':c['event_key'],'linked_source_rows':len(c['source_ids']),'distinct_manuscript_groups':len({source_map[s]['duplicate_group'] for s in c['source_ids'] if s in source_map}),'independent_consumer_case':c['reference_id']!='B05' and c['reference_id']!='B04','duplicate_of_A':c['duplicate_of_A'],'source_ids':c['source_ids']} for c in out])
print(json.dumps(counts,ensure_ascii=False,indent=2))
