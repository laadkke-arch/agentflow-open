"""Stage2: path/type/time only; no new HTML, payload, source text or commit message."""
from collect import *
from collections import Counter
rows=json.loads((D/'stage1-frame.json').read_text())
nt=json.loads((D/'new-publication-tree.json').read_text());ns=json.loads((D/'new-source-tree.json').read_text())
assert nt.get('truncated') is False and ns.get('truncated') is False
np={x['path']:x for x in nt['tree'] if x['type']=='blob'}
nsp={x['path']:x for x in ns['tree'] if x['type']=='blob'}
osp={x['path']:x for x in json.loads((D/'old-source-tree.json').read_text())['tree'] if x['type']=='blob'}
old_author={x['page_path']:x for x in json.loads((D/'old-author-source-map.json').read_text())['rows']}
now=utc();groups={x:[] for x in ['A','M','G']}
for r in rows:
 if r['eligible']!='YES':
  r.update(signal_stratum='',signal_exclusion=r['exclusion']);continue
 asset=r['old_resource_path']
 a=asset in np if asset else None
 p=r['page_path'] in np
 oldsrc_known=r['source_path'] in osp
 source_present=r['source_path'] in nsp if oldsrc_known else None
 verified=[x for x in old_author[r['page_path']]['confirmed_author_source_set'] if x['status']=='YES']
 disappeared=[x['path'] for x in verified if x['path'] in osp and x['path'] not in nsp]
 st='A' if a is False else ('M' if a is True and (not p or source_present is False or disappeared) else 'G')
 r.update(signal_stratum=st,new_legacy_asset_present='YES' if a else ('NO' if a is False else '미확인'),new_old_page_present='YES' if p else 'NO',old_source_known='YES' if oldsrc_known else '미확인',new_old_source_present='YES' if source_present else ('NO' if source_present is False else '미확인'),confirmed_author_source_set_json=json.dumps([x['path'] for x in verified]),confirmed_author_disappeared_paths_json=json.dumps(disappeared),author_source_evidence='evidence/ggplot2/old-author-source-map.json',source_definition_amendment_commit='1ddac4cec4532121598c3ad3deac4450fc5ac6a5',new_legacy_asset_blob=np.get(asset,{}).get('sha',''),new_old_page_blob=np.get(r['page_path'],{}).get('sha',''),new_old_source_blob=nsp.get(r['source_path'],{}).get('sha',''),signal_read_utc=now,new_tree_evidence_url=API+'git/trees/'+NEW+'?recursive=1',new_source_tree_evidence_url=API+'git/trees/'+NSRC+'?recursive=1')
 aps=list(dict.fromkeys(x for x in r.get('author_source_links','').split(';') if x))
 author=[]
 for ap in aps:
  path=ap.split('#')[0]
  candidates=[p for p in nsp if p.lower()==path.lower()] if path not in nsp else []
  author.append({'old_literal_path':ap,'old_path_present':path in osp,'new_exact_path_present':path in nsp,'case_insensitive_path_candidates':candidates,'meaning':'Path-only candidates; not a confirmed semantic rename until content/diff audit'})
 r['author_path_signals_json']=json.dumps(author,ensure_ascii=False)
 groups[st].append(r)
for g in groups:groups[g].sort(key=lambda r:(r['hash_sha256'],r['old_section_path']))
selected=[];predictions=[]
for st in ['A','M','G']:
 for num in [1,2]:
  case='GG-'+st+str(num)
  if len(groups[st])<num:
   predictions.append({'case_id':case,'project':'ggplot2','stratum':st,'slot':num,'vacant':'YES','old_section_path':'','old_section_url':'','purpose_visual':'미확인','purpose_api':'미확인','old_resource_path':'','signal':'Complete new path sets contain no eligible candidate in this stratum','new_tree_evidence_url':API+'git/trees/'+NEW+'?recursive=1','provisional_return_url':'미확인','provisional_payload_url':'미확인','prediction_U':'미확인','prediction_utc':now,'hash_sha256':'','countercondition':'No candidate is not a predicted NO; no false positive/negative can be measured for this slot.','limitation':'결원: candidate_count='+str(len(groups[st])),'frame_evidence':'evidence/ggplot2/frame.csv','signal_receipt':'evidence/ggplot2/receipts/new-publication-tree.json.json'})
   continue
  r=groups[st][num-1];selected.append(r['page_path']);r['selected_case_id']=case
  prediction='YES' if r['new_legacy_asset_present']=='YES' else ('NO' if r['new_legacy_asset_present']=='NO' else '미확인')
  predictions.append({'case_id':case,'project':'ggplot2','stratum':st,'slot':num,'vacant':'NO','old_section_path':r['old_section_path'],'old_section_url':r['body_url']+'#'+r['old_fragment'],'purpose_visual':r['purpose_visual'],'purpose_api':r['purpose_api'],'old_resource_path':r['old_resource_path'],'signal':'Legacy asset='+r['new_legacy_asset_present']+'; old page='+r['new_old_page_present']+'; canonical old man source='+r['new_old_source_present']+'; confirmed author source paths absent='+r['confirmed_author_disappeared_paths_json'],'new_tree_evidence_url':r['new_tree_evidence_url'],'provisional_return_url':RAW+NEW+'/'+r['old_section_path'],'provisional_payload_url':RAW+NEW+'/'+r['old_resource_path'],'prediction_U':prediction,'prediction_utc':now,'hash_sha256':r['hash_sha256'],'countercondition':'A retained asset can cease to be referenced or change purpose; absent asset can gain a renamed/inline successor. Actual fragment and method may differ; no new body has been opened.','limitation':'미확인: new DOM/ref use, visual/API purpose, live display and historical G','frame_evidence':'evidence/ggplot2/frame.csv','signal_receipt':'evidence/ggplot2/receipts/new-publication-tree.json.json'})
for name,data in [('frame.csv',rows),('predictions.csv',predictions)]:
 keys=list(dict.fromkeys(k for r in data for k in r))
 with (D/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(data)
savejson('frame.json',rows);savejson('predictions.json',predictions)
# Events are all deletion/rename-type tree changes under the author R/man roots.
# This intentionally includes internal helpers; membership is a path signal, not proof of a deleted reader example.
events=[]
for block in (D/'source-history-exact-renames.txt').read_text().split('@@')[1:]:
 lines=block.strip().splitlines();commit,dt=lines[0].split('|')
 paths=[]
 for ln in lines[1:]:
  if not ln.strip():continue
  bits=ln.split('\t');paths.append({'status':bits[0],'paths':bits[1:]})
 events.append({'sha':commit,'committer_datetime':dt,'committer_utc':datetime.datetime.fromisoformat(dt).astimezone(datetime.timezone.utc).isoformat(),'changes':paths,'url':'https://github.com/tidyverse/ggplot2/commit/'+commit,'metadata_only':True})
events.sort(key=lambda x:(x['committer_utc'],x['sha']))
tracked={}
for page,mapping in old_author.items():
 if mapping['render_source_exists']:tracked.setdefault(mapping['render_source_path'],[]).append(page)
 for a in mapping['confirmed_author_source_set']:
  if a['status']=='YES':tracked.setdefault(a['path'],[]).append(page)
example_events=[];context_events=[]
for e in events:
 linked=[]
 for ch in e['changes']:
  oldpath=ch['paths'][0]
  if oldpath in tracked:
   linked.append({'change':ch,'old_example_pages':tracked[oldpath]})
   if ch['status'].startswith('R') and len(ch['paths'])==2:tracked.setdefault(ch['paths'][1],[]).extend(tracked[oldpath])
 e['linked_example_changes']=linked
 if linked:example_events.append(e)
 else:context_events.append(e)
remaining=sorted((r for r in rows if r['eligible']=='YES' and r['page_path'] not in selected),key=lambda r:(r['hash_sha256'],r['old_section_path']))
controls=[]
for ix,r in enumerate(remaining[:max(0,7-len(selected))],1):
 controls.append({'case_id':'GG-X'+str(ix),'page_path':r['page_path'],'old_section_path':r['old_section_path'],'hash_sha256':r['hash_sha256'],'purpose_visual':r['purpose_visual'],'purpose_api':r['purpose_api'],'allocation':'independent_payload_or_source','why':'Prespecified minimum-material control; remaining hashes give seven distinct logical examples including four main cases. All three controls are separate logical lineages from four main example bodies; not pooled into main confusion counts.'})
all_linked=set();seen=set();row_by_page={x['page_path']:x for x in rows}
for e in example_events:
 pages=sorted({p for ch in e['linked_example_changes'] for p in ch['old_example_pages']})
 e['unique_old_example_pages']=pages
 e['main_overlap']=[{'page_path':p,'case_id':row_by_page[p]['selected_case_id']} for p in pages if p in selected]
 e['prior_event_overlap_pages']=sorted(set(pages)&seen)
 eligible_reps=[row_by_page[p] for p in pages if p not in selected and p not in {x['page_path'] for x in controls}]
 eligible_reps.sort(key=lambda x:(x['hash_sha256'],x['old_section_path']))
 e['prespecified_representative_page']=eligible_reps[0]['page_path'] if eligible_reps else None
 e['independence_note']='One official change event, not one independent logical example; linked pages and main/prior-event overlaps are explicit. Only listed representative plus already selected main/control cases receive detailed body tracing.'
 seen.update(pages);all_linked.update(pages)
savejson('supplemental-selection.json',{'frozen_utc':now,'scope':'Exact old..new source DAG commits; DR metadata under R/man; only changes linked to an OLD eligible example via confirmed Rd/author source set enter the supplemental example-event denominator. Exact R100 path chains connect later deletion. Non-example helper events are separately bounded official-change context materials.','old_source_sha':OSRC,'new_source_sha':NSRC,'ordering':'committer UTC ascending then SHA ascending','metadata_count_all':len(events),'example_source_event_count':len(example_events),'unique_old_example_pages_linked':len(all_linked),'unique_old_example_pages_outside_main':len(all_linked-set(selected)),'maximum_open_commits':10,'selected_events':example_events[:10],'unselected_event_count':max(0,len(example_events)-10),'official_change_context_events':context_events,'metadata_receipt':'evidence/ggplot2/source-history-exact-renames-receipt.json','minimum_material_controls':controls,'new_body_reads':0,'commit_message_or_patch_reads':0})
summary={'completed_utc':now,'eligible':sum(r['eligible']=='YES' for r in rows),'full_page_rows':len(rows),'stratum_candidates':{g:len(v) for g,v in groups.items()},'pair_slots':6,'filled_pairs':len(selected),'vacant_pairs':6-len(selected),'selected':selected,'prediction_counts':dict(Counter(r['prediction_U'] for r in predictions if r['vacant']=='NO')),'vacancy_ids':[r['case_id'] for r in predictions if r['vacant']=='YES'],'new_tree_complete':True,'new_source_tree_complete':True,'first_new_tree_request_utc':json.loads((R/'new-publication-tree.json.json').read_text())['started_utc'],'new_body_or_asset_reads':0,'commit_message_or_patch_reads':0,'source_history_metadata_event_count':len(events),'supplemental_example_source_events':len(example_events),'official_change_context_events':len(context_events),'minimum_material_control_count':len(controls),'main_M_definition':'Amended confirmed render-man or author-documentation-source set; generated Rd header+examples connects author sources. Bare implementation links do not qualify.','amendment_commit':'1ddac4cec4532121598c3ad3deac4450fc5ac6a5','prior_definition_snapshot':'evidence/ggplot2/sensitivity-man-only/','old_source_mapping_confirmed':67,'old_source_mapping_unknown':1}
savejson('stage2-summary.json',summary)
ledger=[json.loads(l) for l in (D/'sources.jsonl').read_text().splitlines() if l.strip()]
ledger=list({x['id']:x for x in ledger if x['id'] not in ['GG106-INHERITED-new-publication-tree','GG106-INHERITED-new-source-tree']}.values())
for key,pin in [('new-publication-tree',NEW),('new-source-tree',NSRC)]:
 rc=json.loads((R/(key+'.json.json')).read_text())
 ledger.append({'id':'GG106-INHERITED-'+key,'questions':['Q2','Q3'],'original_url':rc['url'],'immutable_url':rc['url'],'preserved_location':'evidence/ggplot2/'+key+'.json','accessed_utc':rc['accessed_utc'],'publisher':'tidyverse/ggplot2','work_lineage':'Inherited fixed 3.5.0 publication/source tree event','edition':'3.5.0','fingerprints':{'sha256':rc['sha256']},'observed':'Complete tree, only path/type/blob metadata read before prediction seal; no body content','supports':'Path denominator and A/M/G partition','limits':'Path existence does not settle reference, purpose, fragment or generation','status':'계승','category':'publication_record','countable':False,'count_reason':'Same fixed publication/source work previously counted by102; reacquisition not new source.'})
(D/'sources-stage2.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in ledger))
(D/'sources.jsonl').write_text((D/'sources-stage2.jsonl').read_text())
print(json.dumps(summary,ensure_ascii=False,indent=2));print('controls',[(x['case_id'],x['page_path']) for x in controls]);print('events',[x['sha'] for x in events])
