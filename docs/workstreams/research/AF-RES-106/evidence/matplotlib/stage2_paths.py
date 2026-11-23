"""AF106 stage2: path/type metadata only. Never requests new HTML/assets/patches."""
from pathlib import Path
import csv,json,hashlib,datetime,subprocess,collections
ROOT=Path(__file__).resolve().parent
OLD='f3ac5407f8ffc861cae1ea87eddd06c63b222e4b';NEW='410d8388303fab638bbedbd1d2eace0e5efb0de9'
OLD_DOC='655f616e86e2c0f7724d7c88717d4ac4eb438c57';NEW_DOC='235131a6bc2527aee7eea370fd5f94564a48c20d'
NEWBASE=f'https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/{NEW}/3.7.0/'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(name):return json.loads((ROOT/name).read_text())
def writecsv(path,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
new=load('new-publication-tree.json');src=load('new-author-tree.json');oldsrc=load('old-author-tree.json')
assert not new['truncated'] and not src['truncated'] and not oldsrc['truncated']
pub={r['path']:r for r in new['tree']};authors={r['path']:r for r in src['tree']};oldauthors={r['path']:r for r in oldsrc['tree']}
rows=list(csv.DictReader((ROOT/'stage1-frame.csv').open()))
for r in rows:
    if r['eligible']!='YES': continue
    resource=r['old_resource_path'];r.update(new_tree_complete='YES',new_page_present='YES' if r['page_path'] in pub else 'NO',new_source_path_present='YES' if r['source_path'] in pub else 'NO',new_author_path_present='YES' if r['author_source_path'] in authors else 'NO',old_author_path_present='YES' if r['author_source_path'] in oldauthors else 'NO',new_source_blob=pub.get(r['source_path'],{}).get('sha',''),old_author_blob=oldauthors.get(r['author_source_path'],{}).get('sha',''),new_author_blob=authors.get(r['author_source_path'],{}).get('sha',''))
    r['legacy_path_present']='YES' if resource and resource in pub else ('NO' if resource else '미확인')
    r['download_path_disappeared']='YES' if r['source_path'] and r['source_path'] not in pub else 'NO'
    r['author_path_disappeared']='YES' if r['author_source_path'] in oldauthors and r['author_source_path'] not in authors else 'NO'
    r['source_blob_changed']='YES' if r['new_source_blob'] and r['source_blob']!=r['new_source_blob'] else 'NO'
    if r['legacy_path_present']=='NO': r['stratum']='A';r['signal']='old representative external resource absent from complete new publication tree'
    elif r['legacy_path_present']=='YES' and (r['new_page_present']=='NO' or r['new_source_path_present']=='NO' or r['author_path_disappeared']=='YES'):
        r['stratum']='M';r['signal']='resource retained; old body/download/author-source path absent'
    else:r['stratum']='G';r['signal']='neither A nor M; source blob change alone does not qualify M'
    r['tree_evidence_url']='https://api.github.com/repos/matplotlib/matplotlib.github.com/git/trees/94eb9c8195d36c3cc1a36876409629a115b5a9ae?recursive=1'
    r['source_tree_evidence_url']='https://api.github.com/repos/matplotlib/matplotlib/git/trees/'+NEW_DOC+'?recursive=1'
    r['path_signal_recorded_utc']=now
eligible=[r for r in rows if r['eligible']=='YES'];groups={k:sorted([r for r in eligible if r['stratum']==k],key=lambda r:(r['hash_sha256'],r['old_section_path'])) for k in ['A','M','G']}
pred=[]
for layer in ['A','M','G']:
    for ix in [1,2]:
        selected=groups[layer][ix-1] if len(groups[layer])>=ix else None
        base={'case_id':f'MP-{layer}{ix}','project':'Matplotlib','stratum':layer,'slot':ix,'vacant':'NO' if selected else 'YES','old_version':'3.6.3','new_version':'3.7.0','old_publication_sha':OLD,'new_publication_sha':NEW,'old_documented_source':OLD_DOC,'new_documented_source':NEW_DOC,'prediction_recorded_utc':now,'new_body_asset_patch_reads':0,'stratum_population':len(groups[layer]),'tree_evidence_url':'https://api.github.com/repos/matplotlib/matplotlib.github.com/git/trees/94eb9c8195d36c3cc1a36876409629a115b5a9ae?recursive=1','intentional_blind_spot':'Path-retained-but-unused => false positive; renamed/inline/different API successor => false negative; old fragment can disappear while page survives.','vacancy_reason':'' if selected else 'No eligible candidates under frozen A>M>G precedence in complete remaining479 frame; not prediction abstention'}
        if selected:
            base.update({k:selected[k] for k in ['page_path','old_section_path','old_resource_path','asset_kind','purpose_visual','purpose_api','source_path','author_source_path','source_blob','new_source_blob','new_page_present','new_source_path_present','new_author_path_present','download_path_disappeared','author_path_disappeared','legacy_path_present','hash_sha256','signal','body_receipt']})
            base.update(old_section_url=selected['body_url']+'#'+selected['fragment'],prediction_U=selected['legacy_path_present'],new_provisional_section_url=NEWBASE+selected['old_section_path'],new_provisional_resource_url=NEWBASE+selected['old_resource_path'] if selected['old_resource_path'] else '미확인',selected_rank=ix)
        else:base.update(prediction_U='미확인',page_path='',old_section_path='',old_resource_path='',purpose_visual='미확인',purpose_api='미확인',old_section_url='미확인',new_provisional_section_url='미확인',new_provisional_resource_url='미확인',hash_sha256='')
        pred.append(base)
writecsv(ROOT/'frame.csv',rows);writecsv(ROOT/'predictions.csv',pred)
selectedpages={p['page_path'] for p in pred if p['vacant']=='NO'}
remaining=sorted([r for r in eligible if r['page_path'] not in selectedpages],key=lambda r:(r['hash_sha256'],r['old_section_path']))
controls=remaining[:4];controlpages={r['page_path'] for r in controls}
directpages={r['page_path'] for r in rows if r['inspected_directly']=='YES'}
payloads=[r for r in remaining if r['page_path'] not in controlpages|directpages][:3]
extras={'selected_utc':now,'body_controls_rule':'remaining AF106 hash order after main, first4; not main confusion rates','body_controls':controls,'source_only_rule':'remaining same order excluding main, controls and any already direct-read body; first3 actual author/download source works, so distinct logical lineage from counted bodies','source_only':payloads}
(ROOT/'control-selection.json').write_text(json.dumps(extras,ensure_ascii=False,indent=2)+'\n')
events=[];event=None
for line in (ROOT/'source-change-metadata.txt').read_text().splitlines():
    if line.startswith('COMMIT '):
        a=line.split();event={'sha':a[1],'committer_date':a[2],'parents':a[3:],'changes':[]};events.append(event)
    elif line and event is not None:
        a=line.split('\t');event['changes'].append({'status':a[0],'old_path':a[1],'new_path':a[2] if len(a)>2 else ''})
oldpaths={r['author_source_path'] for r in eligible}
filtered=[]
for event in events:
    event['eligible_old_changes']=[x for x in event['changes'] if x['old_path'] in oldpaths]
    event['old_path_not_in_frozen_population']=[x for x in event['changes'] if x['old_path'] not in oldpaths]
    if event['eligible_old_changes']:
        dt=datetime.datetime.fromisoformat(event['committer_date'].replace('Z','+00:00')).astimezone(datetime.timezone.utc)
        event['committer_utc']=dt.isoformat();event['before_old_publication']=dt<datetime.datetime(2023,1,12,11,1,14,tzinfo=datetime.timezone.utc)
        event['is_merge']=len(event['parents'])>1
        event['main_overlap']=[r['case_id'] for r in pred if r.get('author_source_path') in [z['old_path'] for z in event['eligible_old_changes']]]
        event['event_lineage_key']='|'.join(sorted(x['old_path'] for x in event['eligible_old_changes']))
        event['event_url']='https://github.com/matplotlib/matplotlib/commit/'+event['sha']
        filtered.append(event)
filtered.sort(key=lambda e:(e['committer_utc'],e['sha']));selected=filtered[:10]
selection={'selected_utc':now,'scope':load('history-boundary.json'),'rule':'old..new DAG difference, first-parent diffs for merges; Git exact-blob rename detection100%; D/R events must involve author source path in old eligible479. Sort committer UTC thenSHA; max10. Old paths already aliases/absent excluded before outcome. Merge event repetitions remain explicit, not independent cases.','all_path_change_commits':len(events),'eligible_event_commits':len(filtered),'selected_count':len(selected),'selected_unique_path_event_lineages':len({e['event_lineage_key'] for e in selected}),'main_overlap_commits':sum(bool(e['main_overlap']) for e in selected),'selected':selected,'excluded_events':[e for e in events if not e['eligible_old_changes']],'new_content_exposure':{'new_bodies':0,'assets':0,'commit_messages':0,'patches':0}}
(ROOT/'supplemental-selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
summary={'recorded_utc':now,'project':'Matplotlib','population':len(eligible),'new_publication_entries':len(new['tree']),'new_author_tree_entries':len(src['tree']),'all_trees_complete':True,'stratum_populations':{k:len(v) for k,v in groups.items()},'selected_cases':[{k:x.get(k) for k in ['case_id','page_path','prediction_U','vacant']} for x in pred],'filled_pairs':sum(x['vacant']=='NO' for x in pred),'vacancies':sum(x['vacant']=='YES' for x in pred),'prediction_counts':dict(collections.Counter(x['prediction_U'] for x in pred if x['vacant']=='NO')),'eligible_removed_author_paths':[r['author_source_path'] for r in eligible if r['author_path_disappeared']=='YES'],'source_event_selection':'supplemental-selection.json','control_selection':'control-selection.json','first_new_tree_request_utc':load('receipts/new-publication-root-tree.json')['requested_utc'],'new_body_asset_message_patch_reads':0,'old_frozen_frame_sha256':hashlib.sha256((ROOT/'stage1-frame.csv').read_bytes()).hexdigest()}
(ROOT/'stage2-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2));print('events',len(selected),'controls',[r['page_path'] for r in controls],'sources',[r['page_path'] for r in payloads])
