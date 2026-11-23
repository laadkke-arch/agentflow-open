"""Seal 51 path judgments from the direct-read ledger, without provider execution."""
import hashlib,json,re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent
def load(path):return json.loads(path.read_text())
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(data):return hashlib.sha256(data).hexdigest()
NOW=datetime.now(timezone.utc).isoformat()
docs={r['source_id']:r for r in load(ROOT/'document-index.json')}
edges={(r['catalog_id'],r['path_id']):r for r in load(ROOT/'edge-index.json')}
notes={(r['case_id'],r['catalog_id']):r for r in load(ROOT/'decision-notes.json')}
requirements={r['case_id']:r for r in load(BASE/'requirements.json')}
assign=load(BASE/'evidence/path-assignment-schema.json')
features={r['catalog_id']:r for r in load(BASE/'evidence/features-schema/features.json')}
lineage=load(BASE/'inputs/af-res-056/source-lineage.json')

for d in docs.values():
    if d['status']=='window_ready':
        d['read_status']='directly_read';d['reader']='/root/features_schema'
        d['read_interval_utc']=['2026-11-23T03:57:00Z',NOW]
        text=(BASE/d['window_file']).read_text().removesuffix('\n')
        assert sha(text.encode())==d['window_sha256'],d['source_id']
        assert len(text.split())==d['display_word_count']<=500,d['source_id']
    elif d['status']=='empty_static_body':
        d['read_status']='source_shell_inspected_no_readable_body'
        d['read_interval_utc']=['2026-11-23T04:02:00Z',NOW]
    else:d['read_status']='not_read_access_failure'
    if d['source_id'].startswith('PS-SC-') and d['source_id'].endswith('-P1'):
        cid=d['source_id'][3:9]
        wm=load(BASE/'evidence/features-schema/windows'/f'{cid}.json')
        d['acquisition_utc']=wm['retrieved_utc']
dump(ROOT/'document-index.json',list(docs.values()))

def find_anchor(sid,anchor):
    d=docs[sid]
    text=(BASE/d['window_file']).read_text() if d.get('window_file') else ''
    words=list(re.finditer(r'\S+',text));normalized=' '.join(m[0] for m in words);wanted=' '.join(anchor.split())
    pos=normalized.find(wanted)
    if pos<0:return {'source_id':sid,'window_file':d.get('window_file'),'anchor':anchor,'anchor_found':False}
    token=sum(1 for m in re.finditer(r'\S+',normalized[:pos]))
    offset=words[token].start() if token<len(words) else len(text)
    return {'source_id':sid,'window_file':d['window_file'],'window_line':text[:offset].count('\n')+1,'anchor':anchor,'anchor_found':True}

def document_for_path(sid,original_override=None):
    d=docs[sid];provider=d['source_role'] in {'provider_document','same_provider_code','same_provider_translation'}
    return {'source_id':sid,'original_url':original_override or d['original_url'],'fixed_url':d.get('fixed_url'),
      'implementation_sha':d.get('implementation_sha') if provider else None,'source_commit':d.get('implementation_sha'),
      'version':d.get('version'),'version_scope':'implementation source document' if provider else 'document edition only; not implementation identity',
      'window_file':d.get('window_file'),'words':d.get('display_word_count',0),'status':d['read_status'],
      'hash':d.get('window_sha256'),'response_sha256':d.get('response_sha256'),'source_git_blob':d.get('source_blob'),
      'acquisition_utc':d.get('acquisition_utc'),'source_role':d['source_role'],'execution_evidence':False}

observations=[]
for a in assign:
    case,cid=a['case_id'],a['catalog_id'];n=notes[(case,cid)];r=requirements[case];initial='PS-'+cid+'-P1'
    for pid in ['P1','P2','P3']:
        edge=edges.get((cid,pid));second=edge['second_source_id'] if edge else None
        ds=[document_for_path(initial)]
        if second:ds.append(document_for_path(second,edge['selected_link']['resolved_url']))
        direct=[find_anchor(initial,anchor) for anchor in n['anchors']]
        assert all(e['anchor_found'] for e in direct),(case,cid,direct)
        if second:
            sd=docs[second]
            direct.append({'source_id':second,'window_file':sd.get('window_file'),'window_scope':'entire recorded window, at most500words','observed_scope':n.get(pid),'read_status':sd['read_status']})
        same=True;same_reason='P1 is one fixed implementation source commit.'
        if second:
            sd=docs[second]
            if second=='PS-SKEMA':same=False;same_reason='Everit and json-sKema are explicitly different implementations; do not join their clauses.'
            elif sd['source_role'] in {'provider_document','same_provider_code','same_provider_translation'} and sd.get('implementation_sha')==docs[initial].get('implementation_sha'):
                same=True;same_reason='Both readable documents are tied to exactly the same provider source commit.'
            else:same=None;same_reason='Follow-up is independent material, another dependency edition, a live unbound manual, or inaccessible; no joint implementation-edition proof.'
        elif pid!='P1':same_reason='No second link; only the same fixed first document is available.'
        conditional=n.get('C2_primary_status')=='supported_conditionally'
        env='unconfirmed_runtime_or_engine_substitution'
        if case in {'JS-1','JS-5'}:env='request_runtime_unspecified_candidate_dialect_recorded'
        if case=='JS-6' and cid=='SC-005':env='named_engine_matches_version_dialect_and_integration_unconfirmed'
        path_note=n.get(pid,'First fixed README window only.')
        obs={'case_id':case,'catalog_id':cid,'path_id':pid,'documents':ds,
          'C1_status':'unconfirmed','C2_status':n.get('C2_primary_status','unconfirmed'),
          'environment_status':env,'environment_evidence':n['environment'],
          'same_implementation_version':same,'same_implementation_version_reason':same_reason,
          'judgment':n.get('primary_judgment','unconfirmed'),
          'rationale':{'C1':n['C1'],'C2':n['C2'],'path_increment':path_note,'guard':r.get('guard')},
          'direct_evidence':direct,'primitive_capability_evidence':n['primitive'],
          'counterexample':{'text':n['counterexample'],'origin':'researcher contrast preserving frozen requirement predicates','execution':'not_run','observed_failure':False},
          'execution_status':'not_run; provider statements and example code only; no installation, test execution, or original-user success',
          'observed_utc':NOW,'stage3_sha':'5d01a6208edd9f8a20be7b31f7b545cef2200597',
          'first_link_policy':'frozen readable body order; no usefulness replacement',
          'selected_followup':edge['selected_link'] if edge else None,
          'path_progress':'P1_read' if pid=='P1' else ('selected_second_document_attempted_or_cached' if second else 'no_second_information_link'),
          'cost':{'logical_document_attempts':len(ds),'logical_readable_window_visits':sum(d['words']>0 for d in ds),
             'logical_display_words':sum(d['words'] for d in ds),'same_first_response_reused_across_combinations':True,
             'second_is_same_response_as_first':bool(second and docs[second].get('response_sha256')==docs[initial].get('response_sha256'))},
          'next_minimum_check':n['next_minimum'],
          'conditional_transfer':{'source_property':'bar','target_property':'id','unchanged_structure':'object.properties.<name>.type=string',
             'inference':True,'new_required_key_constraint_added':False,'literal_id_run_observed':False} if conditional else None,
          'strict_literal_example_sensitivity':{'C1_status':'unconfirmed','C2_status':'unconfirmed','judgment':'unconfirmed',
             'reason':'No literal id validation/result in the path. Primary admits only an ordinary property-name parameter substitution.'} if conditional else None}
        observations.append(obs)
assert len(observations)==51
assert len({(x['case_id'],x['catalog_id'],x['path_id']) for x in observations})==51
assert all(len(x['documents'])<=2 for x in observations)
assert all(x['catalog_id']!='SC-032' for x in observations)
dump(ROOT/'observations.json',observations)
seal={'frozen_utc':NOW,'phase':'after all allowed window readings and scope review; before root out-of-path execution diagnosis',
 'stage3_sha':'5d01a6208edd9f8a20be7b31f7b545cef2200597','observations_sha256':sha((ROOT/'observations.json').read_bytes()),
 'decision_notes_sha256':sha((ROOT/'decision-notes.json').read_bytes()),'document_index_sha256':sha((ROOT/'document-index.json').read_bytes()),
 'rows':51,'case_provider_pairs':17,'judgments':dict(Counter(x['judgment'] for x in observations)),
 'provider_execution_performed':False,'root_outside_path_diagnostic_results_seen':False,
 'primary_condition_transfer':'JS6/Ajv C2 only: bar→id ordinary property-name substitution, independent of C1. Three paths share the same P1 evidence.',
 'strict_literal_example_sensitivity':'Those three partial paths become unconfirmed; no other path changes.'}
dump(ROOT/'observations-seal.json',seal)
print(json.dumps(seal,ensure_ascii=False,indent=2))
