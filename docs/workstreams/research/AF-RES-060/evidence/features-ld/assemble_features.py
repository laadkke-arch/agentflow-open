from pathlib import Path
import json,csv,datetime,hashlib,re,sys
P=Path(__file__).parent
OWN=P.parents[1]
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
acq=json.loads((P/'acquisition.json').read_text())
for a in acq:
    if a.get('fetch_status')=='success':
        f=Path(a['raw_file']);t=f.read_text()
        if a.get('chars') is not None and len(t)==a['chars']+1 and t.endswith('\n'):f.write_text(t[:-1])
        b=f.read_bytes();actual=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
        a['local_git_blob']=actual;a['original_blob_equal']=actual==a.get('blob')
    if 'releases' in a:
        a['release_candidates_seen']=max(a.get('release_candidates_seen',0),len(a['releases']));a['releases']=a['releases'][:1]
(P/'acquisition.json').write_text(json.dumps(acq,ensure_ascii=False,indent=2)+'\n')
# Same cached source responses, corrected rendering. No new acquisition.
sys.path.insert(0,str(P));from render_windows import main,window
main()
windows={x['id']:x for x in json.loads((P/'window-metadata.json').read_text())}
follow=json.loads((P/'followups.json').read_text())
for a in follow:
    if a.get('fetch_status')=='success':
        raw=Path(a['raw_file']).read_text();frag=a['requested_url'].partition('#')[2]
        w=window(raw,'.html',frag or None)
        a.update({k:v for k,v in w.items() if k!='text'});(P/a['window_file']).write_text(w['text']+'\n');a['window_sha256']=hashlib.sha256(w['text'].encode()).hexdigest()
    a['actual_body_read_utc']=a.get('actual_body_read_utc') or (NOW if a.get('rendered_words',0) else None)
    a['read_time_precision']='completion recorded after direct reading; exact per-window UI timestamps not separately captured'
    a['contributes_provider_features']=False
    if a['id']=='RUSTAPI':a['read_status']='redirect_shell_only; target API body not read'
    elif a.get('fetch_status')=='failed':a['read_status']='access_failed'
    else:a['read_status']='directly_read_bounded_window'
(P/'followups.json').write_text(json.dumps(follow,ensure_ascii=False,indent=2)+'\n')
# The broad link detector is a candidate aid, not the final role-based selection.
for rid,w in windows.items():
    candidate=w.pop('first_api_features_link',None)
    w['heuristic_api_link_candidate']=candidate
    selected=next((f for f in follow if rid in f['catalog_ids']),None)
    w['first_api_features_link']=({'href':selected['requested_url'],'followup_id':selected['id'],'role':selected['role']} if selected else None)
    w['link_selection_note']='Human role review, before holdout/ranking: OpenApi product site, test cases, and sophia_api crate listing are not API/Features documents; rejected URLs were not fetched/read.'
(P/'window-metadata.json').write_text(json.dumps(list(windows.values()),ensure_ascii=False,indent=2)+'\n')

byid={x['id']:x for x in acq}
for id in ['LD-020','LD-021']:byid[id]=json.loads((P/(id+'-crate-metadata.json')).read_text())
catalog={x['catalog_id']:x for x in csv.DictReader((OWN/'inputs/af-res-056/catalog.csv').open())}
selections=json.loads((P/'manual-selections.json').read_text())
roles={
'SC-034':('suite','JsonSchema.Net.Generation | JsonSchema.Net.Api | JsonSchema.Net.Generation.DataAnnotations; distinct modules; selected package not guaranteed'),
'LD-004':('wrapper/façade','JSON-LD parser delegated to LD-002 jsonld-streaming-parser.js; other formats have other engines'),
'LD-012':('suite','dotNetRdf.Core | dotNetRdf.AspNet; distinct modules'),
'LD-014':('wrapper/CLI','jsonld.js plus jsonld-request, both directly named in first window'),
'LD-015':('CLI','Titanium related libraries linked under Resources; actual runtime delegation not established in allowed window'),
'LD-020':('meta-crate/suite','separate core crates; JSON-LD module is optional jsonld feature'),
'LD-022':('unknown','repository 404')
}
inherited={'LD-001':'SUP-JSONLDJS','LD-005':'SUP-PYLD','LD-014':'jsonld-cli-snapshot'}
metadata_n={x[0]:(1 if x[0] in inherited else 3) for x in selections};metadata_n.update({'SC-034':6,'LD-018':3,'LD-020':2,'LD-021':2,'LD-022':2})
extra_exposure={'LD-005':500,'LD-010':0,'LD-015':411,'SC-038':500}
eligible_occurrences={('SC-035','validate'):'schema.validate(json)',('SC-039','validate'):'schema.validate(myData)',('LD-004','parse'):'rdfParser.parse method',('LD-005','compact'):'jsonld.compact(doc, context)',('LD-011','JsonLdOptions'):'JsonLdOptions options =',('LD-011','compact'):'JsonLdProcessor.compact(jsonObject'}
out=[];sources=[]
for id,terms,kinds,note in selections:
    c=catalog[id];a=byid.get(id,{});w=windows.get(id);fs=[f for f in follow if id in f['catalog_ids']]
    text=(P/w['window_file']).read_text() if w else ''
    raw=Path(a['raw_file']).read_text() if a.get('raw_file') else ''
    proof=[]
    for order,(term,kind) in enumerate(zip(terms,kinds),1):
        needle=eligible_occurrences.get((id,term),term)
        pos=text.find(needle)
        if pos>=0:pos+=needle.find(term)
        assert pos>=0,(id,term)
        rawpos=raw.find(needle)
        if rawpos>=0:rawpos+=needle.find(term)
        proof.append({'order':order,'term':term,'original_spelling':term,'qualification':kind,'source_id':'F-'+id,'source_url':a.get('fixed_url'),'window_file':w['window_file'],'window_line':text[:pos].count('\n')+1,'window_word_position':len(text[:pos].split())+1,'raw_eligible_occurrence_line':raw[:rawpos].count('\n')+1 if rawpos>=0 else None,'raw_line_note':'eligible occurrence in bounded window, not arbitrary first substring or excluded CLI/comment','eligible_needle':needle,'concept_uri':None,'concept_relation':'original provider spelling only; no standardized alias inserted'})
    role,engine=roles.get(id,('implementation/library','No wrapper/delegation established in allowed window'))
    work=inherited.get(id,'supplier-'+(a.get('repo') or a.get('repository') or c['title']).lower().replace('https://github.com/','').replace('/','-').replace(' ','-'))
    follow_words=sum(f.get('rendered_words',0) for f in fs)
    item={'catalog_id':id,'family':c['family'],'posted_rank':int(c['posted_rank']),'original_destination_url':c['destination_url'],'f0_fields':json.loads(c['search_fields_json']),'features':terms,'feature_evidence':proof,'fixed_url':a.get('fixed_url'),'implementation_sha':a.get('sha'),'implementation_version':a.get('version'),'version_status':('inherited_056_pin' if id in inherited else ('formal_release_unconfirmed_fixed_commit' if a.get('version')=='formal-version-unconfirmed' else 'official_release_or_crate_version')) if a else 'unknown','same_day_version_confirmed':False,'version_day_limit':'cutoff-bounded release/commit selection or inherited pin; exact original catalog day linkage unconfirmed','role':role,'engine_lineage':engine,'source_id':'F-'+id,'work_id':work,'reused_056_work':id in inherited,'read_utc':NOW if w else None,'acquired_utc':a.get('read_utc'),'window':w,'followup_ids':[f['id'] for f in fs],'blank_reason':note if not terms else '', 'implementation_absence_judgment':'not_assessed; field absence is not capability absence','editor_note':note,'cost':{'metadata_requests':metadata_n[id],'provider_document_responses':1 if w else 0,'logical_document_actions':(1 if w else 0)+len(fs),'scheduled_document_actions':1+len(fs),'logical_body_words':(w['rendered_words'] if w else 0)+follow_words,'first_window_words':w['rendered_words'] if w else 0,'followup_window_words':follow_words,'extra_interpretation_exposure_words':extra_exposure.get(id,0),'read_budget_note':'Main figures count one eligible window per action; repeated displays and pre-correction windows are additional exposure, not hidden in the main budget','document_limit_exceeded':False,'extra_window_exposure':bool(extra_exposure.get(id,0))},'bounded_feature_edit_status':'completed' if w else 'attempted_source_unavailable'}
    out.append(item)
    sources.append({'source_id':'F-'+id,'work_id':work,'kind':'supplier_README_or_official_crate_introduction' if w else 'failed_supplier_acquisition','lineage':engine,'Q':['Q2','Q4','Q7'],'case_ids':[id],'original_url':c['destination_url'],'fixed_url':a.get('fixed_url'),'edition':a.get('sha') or a.get('version'),'retrieved_utc':a.get('read_utc') or NOW,'read_utc':NOW if w else None,'locus':(w['heading']+'; '+w['window_file']+'; '+str(w['rendered_words'])+' displayed words') if w else 'GitHub releases API and repository metadata both404','confirmed':('Stored original provider terms: '+', '.join(terms)+'. ' if terms else 'No eligible added field. ')+note,'scope_and_limits':'Direct bounded editing window only; no holdout requirements or rankings read. No implementation execution. F1 source URL is editorial audit, not a user shortcut. '+('Formal release unavailable; exact commit retained.' if a.get('version')=='formal-version-unconfirmed' else ''),'evidence_type':'author_statement_and_observed_text' if w else 'access_failure','counter_evidence_ids':[],'read_status':'direct_primary' if w else 'access_failed','existing_work_reused':id in inherited,'sha256':w['raw_sha256'] if w else None,'window_sha256':w['window_sha256'] if w else None,'required_allocation':'suppliers' if w else None,'reader':'features_ld'})
for f in follow:
    work= 'w3c-jsonld11-api' if f['id']=='API14' else ('w3c-jsonld11-api' if f['id'] in ['API14','API11','API11REMOTE','APICURRENT'] else ('nodejs-stream-docs' if f['id']=='NODESTREAM' else ('supplier-pchampin-sophia_rs' if f['id']=='SOPHIAAPI' else ('supplier-sagold-json-schema-library' if f['id']=='SC039METHODS' else ('supplier-timothee-haudebourg-json-ld' if f['id']=='RUSTAPI' else 'supplier-dotnetrdf-dotnetrdf')))))
    findings={'API14':'Expansion removes context; compaction applies context. Standard algorithms do not prove any supplier implementation.', 'API11':'Expansion/compaction, mode1.0/1.1 and @version distinct; feature definitions not supplier support.', 'API11REMOTE':'Document loader callback options, returned RemoteDocument and HTTP media-type constraints; not Titanium runtime evidence.', 'APICURRENT':'Linked current API resolves to JSON-LD1.1 feature definitions; not the supplier PHP implementation.', 'NODESTREAM':'Transform implements Readable/Writable; Node stream functions are inherited environment APIs rather than own JSON-LD operations.', 'DOTNETAPI':'Pinned README latest API link returned404; no body read.', 'SOPHIAAPI':'Meta-crate re-exports modules; jsonld, reasoner, sparql/xml have feature gates. A module export is not evidence of a particular user requirement.', 'RUSTAPI':'HTTP200 contains a redirect shell for json-ld0.23.0, not requested trait API body. Destination not followed beyond fixed allocation.', 'SC039METHODS':'Same README method API section includes addRemoteSchema and examples of $ref; stage2 first3 fields unchanged.'}[f['id']]
    sources.append({'source_id':'F-LINK-'+f['id'],'work_id':work,'kind':f['role'],'lineage':'API links reached from first bounded editing windows; same standard reused across supplier rows','Q':['Q2','Q3','Q7'],'case_ids':f['catalog_ids'],'original_url':f['requested_url'],'fixed_url':f.get('final_url',f['requested_url']),'edition':f.get('sha256') or 'same source cache / failed access','retrieved_utc':f['acquired_utc'],'read_utc':f.get('actual_body_read_utc'),'locus':f.get('heading') or 'access error','confirmed':findings,'scope_and_limits':'At most second logical document per row; no third document followed. Standard/other-engine/API-unbound findings do not enter provider feature fields.','evidence_type':'observed_document' if f.get('rendered_words',0) else 'access_failure','counter_evidence_ids':[],'read_status':f.get('read_status'),'existing_work_reused':f['id'] in ['API14','API11','API11REMOTE','APICURRENT'],'sha256':f.get('sha256'),'window_sha256':f.get('window_sha256'),'required_allocation':None,'reader':'features_ld'})
(P/'features.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
summary={'rows':len(out),'successful_provider_windows':sum(bool(x['window']) for x in out),'rows_added':sum(bool(x['features']) for x in out),'added_terms':sum(len(x['features']) for x in out),'empty_rows':[x['catalog_id'] for x in out if not x['features']],'metadata_requests':sum(x['cost']['metadata_requests'] for x in out),'logical_document_actions':sum(x['cost']['logical_document_actions'] for x in out),'logical_read_words':sum(x['cost']['logical_body_words'] for x in out),'provider_first_window_words':sum(x['cost']['first_window_words'] for x in out),'extra_interpretation_display_words':sum(x['cost']['extra_interpretation_exposure_words'] for x in out),'source_ledger_rows':len(sources),'no_holdout_or_ranking_read':True,'finalized_utc':NOW,'original_blob_equal':all(a.get('original_blob_equal') for a in acq if a.get('fetch_status')=='success')}
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

