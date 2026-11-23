"""Produce source and cost ledgers without changing the sealed observations."""
import hashlib,json
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent.parent
def load(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
obs=load(ROOT/'observations.json');seal=load(ROOT/'observations-seal.json')
assert sha((ROOT/'observations.json').read_bytes())==seal['observations_sha256']
docs=load(ROOT/'document-index.json');byid={d['source_id']:d for d in docs}
feat=load(BASE/'evidence/features-schema/features.json')
work_by_commit={f['commit']:f for f in feat if f.get('commit')}
prior=load(BASE/'inputs/af-res-056/source-lineage.json')
uses=defaultdict(list)
for o in obs:
 for d in o['documents']:uses[d['source_id']].append({'case_id':o['case_id'],'catalog_id':o['catalog_id'],'path_id':o['path_id'],'original_url':d['original_url']})
summaries={
 'PS-SUITE':'177-word introduction: language-agnostic test data, implementer-provided language harness, validation and annotation suites. No selected-provider case result.',
 'PS-CFW-UNSUPPORTED':'First500 whitespace words of same-commit TypeScript code enumerate optional idn-email/idn-hostname exclusions. The enum/data-membership conditions are not addressed in this window.',
 'PS-IMHONGLU-KR':'Same-commit Korean translation; required/optional static field inference, schema classes, defaults and parse/safeParse. No variable-terminal-array or employee conditional example.',
 'PS-BENCH':'Legacy draft6 performance/failure/side-effect table; declares Ajv6.12.6 and other versions,884tests/run, and excludes advanced-feature assessment. This is not a result for the selected ajv-cli commit or user cases.',
 'PS-AJV-DRAFT04':'draft04 requires Ajv>=8.5.0 plus ajv-draft-04; cannot mix drafts in that instance. Scalar type examples and nullable/enum distinction; no data property named type or columns/pii example.',
 'PS-RFC8927':'Requested original Datatracker URL returned HTTP403; body not read.',
 'PS-BOWTIE':'Original URL redirects to bowtie.report.435-byte static response contains app div and JS/CSS assets; no readable body. Dynamic table not observed; assets not followed.',
 'PS-CORE-LATEST':'Original latest/json-schema-core.html URL returned HTTP404; no substitute standard URL opened.',
 'PS-JEDISON-DOCS':'119-word Introduction describes frontend form generation and backend validation workflow; no type/id or dynamic-column mechanism and no exact implementation edition binding.',
 'PS-RFC6901':'First500 words show RFC6901 April2013 identification, abstract defining a pointer to a JSON value, status/license material and table of contents. No provider support proof.',
 'PS-BLAZE4J-OVERVIEW':'Same-commit Overview window repeats scalar string and enum examples and completes a registered-schema $ref example. This is schema reference, not dynamic instance name membership.',
 'PS-BLAZE4J-FEATURES':'Same-commit Features window shows scalar string/enum and HTTP/classpath schema resolvers. Adding an object/properties/items structure would be a further inference.',
 'PS-EVERIT-WHEN':'Same-commit When to use section gives org.json/Jackson choices, Maven examples and draft selection. Installation example1.14.4 differs from selected release1.14.5.',
 'PS-SKEMA':'Different successor engine: object name/email scalar-type schema, URI registration, read/write examples. Selected source is v0.32.0 while README install says0.25.0. Cannot join these clauses to Everit.',
 'PS-HOME':'500-word current homepage introduction and community/events. Same root-owned HTTP response reused; no implementation-specific support.'}
special_work={'PS-SUITE':'JSON-SCHEMA-TEST-SUITE','PS-BENCH':'json-schema-benchmark','PS-AJV-DRAFT04':'SUP-AJV',
 'PS-RFC8927':'rfc8927','PS-BOWTIE':'bowtie-comparison-ui','PS-CORE-LATEST':'json-schema-core',
 'PS-JEDISON-DOCS':'provider-germanbisurgi--jedison','PS-RFC6901':'rfc6901','PS-HOME':'JSONSCHEMA-HOMEPAGE'}
sources=[]
for d in docs:
 sid=d['source_id'];f=work_by_commit.get(d.get('implementation_sha'))
 work=special_work.get(sid) or (f['work_id'] if f else 'unresolved-'+sid)
 earlier=[p['source_id'] for p in prior if p['work_id']==work and '실패' not in p.get('kind','')]
 first_060_reuse=bool(f) or sid in {'PS-AJV-DRAFT04','PS-JEDISON-DOCS','PS-HOME'}
 content=summaries.get(sid)
 related=[o for o in obs if any(x['source_id']==sid for x in o['documents'])]
 if not content:
  content='; '.join(dict.fromkeys(p for o in related for p in o['primitive_capability_evidence']))
 if d.get('window_file'):
  text=(BASE/d['window_file']).read_text();line_count=len(text.splitlines())
 else:line_count=0
 retrieved=d.get('acquisition_utc')
 if not retrieved and f:retrieved=load(BASE/'evidence/features-schema/windows'/f"{f['catalog_id']}.json")['retrieved_utc']
 successful=d['status']=='window_ready'
 source={'source_id':sid,'work_id':work,'kind':d['source_role'],'lineage':{'same_work_prior_056':bool(earlier),
  'prior_source_ids':earlier,'same_work_prior_060':first_060_reuse,
  'engine_family':'Blaze' if sid in {'PS-SC-008-P1','PS-BLAZE4J-OVERVIEW','PS-BLAZE4J-FEATURES'} else (f['engine_lineage'] if f else None),
  'new_engine_lineage_observation':'P1 introduction explicitly names Blaze backend; F1 field table unchanged.' if sid=='PS-SC-008-P1' else None},
  'questions':['Q4','Q5','Q6','Q7'],'cases':sorted({x['case_id'] for x in uses[sid]}),'uses':uses[sid],
  'original_url':d['original_url'],'original_urls_observed':sorted({x['original_url'] for x in uses[sid]}),
  'fixed_url':d.get('fixed_url'),'fixed_edition':{'source_commit':d.get('implementation_sha'),'version_label':d.get('version'),
   'source_git_blob':d.get('source_blob'),'response_sha256':d.get('response_sha256'),'last_modified':d.get('last_modified'),
   'implementation_binding':'independent/reference/unknown' if d['source_role'] not in {'provider_document','same_provider_code','same_provider_translation'} else 'provider source edition; execution not verified'},
  'retrieved_utc':retrieved,'read_utc_interval':d.get('read_interval_utc'),
  'locus':{'window_file':d.get('window_file'),'heading':d.get('heading'),'anchor':d.get('anchor'),'display_words':d.get('display_word_count',0),
   'window_sha256':d.get('window_sha256'),'line_count':line_count},
  'confirmed':content,'limits':['Only this selected max500-word window was directly read; fetched whole responses are not whole-document readings.',
    'Source claims/examples are distinct from actual provider execution or original-user success.',
    'No third document or more useful later link was substituted.',
    'HTML is static cached-response text with declared semantic chrome removed; external CSS/JavaScript is not executed.'],
  'observation_author_statement_inference':{'observation':'actual displayed-window text or recorded HTTP failure',
    'author_statement':'support and example behavior remain provider statements',
    'inference':'JS6/Ajv C2 conditional ordinary-name transfer bar→id only' if sid=='PS-SC-005-P1' else 'case-specific conditions are not inferred from primitive/general compliance'},
  'counter_evidence_ids':[sid],
  'counter_evidence_summary':list(dict.fromkeys(o['counterexample']['text'] for o in related)),
  'read_status':'direct_window_read' if successful else ('shell_only_no_readable_body' if d['status']=='empty_static_body' else 'access_failed'),
  'external_original':successful,'previous_work_reuse':bool(earlier),'new_work_eligible':successful and not earlier and not first_060_reuse,
  'reader':'/root/features_schema','source_statement_not_execution':True}
 sources.append(source)
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))

counts=Counter(o['judgment'] for o in obs)
best={}
for o in obs:
 key=(o['case_id'],o['catalog_id']);best[key]='partial' if o['judgment']=='partial' else best.get(key,'unconfirmed')
windows=[d for d in docs if d['status']=='window_ready']
http=load(ROOT/'acquisition-http.json');gh=load(ROOT/'acquisition-github.json');early=load(ROOT/'acquisition-github-early.json')
summary={'frozen_observations_sha256':seal['observations_sha256'],'observations_frozen_utc':seal['frozen_utc'],
 'finalized_utc':datetime.now(timezone.utc).isoformat(),'stage3_sha':seal['stage3_sha'],'case_provider_pairs':17,'primary_providers':12,'paths':51,
 'path_judgments':{k:counts.get(k,0) for k in ['complete','partial','confirmed_wrong','unconfirmed']},
 'best_pair_judgments':dict(Counter(best.values())),'strict_literal_sensitivity':{'complete':0,'partial':0,'confirmed_wrong':0,'unconfirmed':51},
 'accuracy':'not_calculable:0 fully verified complete/confirmed-wrong paths; partial and unconfirmed are not negatives',
 'unique_source_views':len(docs),'readable_source_windows':len(windows),'source_shell_only':sum(d['status']=='empty_static_body' for d in docs),
 'unique_failed_destinations':sum(d['status']=='access_failed' for d in docs),
 'distinct_successful_response_hashes':len({d['response_sha256'] for d in docs if d.get('response_sha256')}),
 'unique_window_display_words':sum(d['display_word_count'] for d in windows),
 'logical_document_attempts':sum(o['cost']['logical_document_attempts'] for o in obs),
 'logical_readable_window_visits':sum(o['cost']['logical_readable_window_visits'] for o in obs),
 'logical_display_words':sum(o['cost']['logical_display_words'] for o in obs),
 'logical_paths_without_second_link':sum(o['path_progress']=='no_second_information_link' for o in obs),
 'logical_failed_second_document_visits':sum(len(o['documents'])==2 and o['documents'][1]['status']=='not_read_access_failure' for o in obs),
 'logical_empty_shell_second_visits':sum(len(o['documents'])==2 and o['documents'][1]['status']=='source_shell_inspected_no_readable_body' for o in obs),
 'this_agent_network_requests':len(http)+len(gh)+len(early)+1,
 'this_agent_network_request_breakdown':{'http_document_requests':len(http),'github_base64_document_requests':len(gh),
  'github_duplicate_text_document_requests':sum(x['type']=='duplicate_document_acquisition' for x in early),
  'github_metadata_requests':sum(x['type']=='metadata' for x in early)+1},
 'shared_root_home_network_request':{'count':1,'already_charged_to_root':True,'response_sha256':byid['PS-HOME']['response_sha256']},
 'extra_first_document_network_requests':0,'first_responses_reused_from_stage2':12,
 'source_work_count_direct_read':len({s['work_id'] for s in sources if s['read_status']=='direct_window_read'}),
 'new_work_ids_in_this_path_phase':sorted({s['work_id'] for s in sources if s['new_work_eligible']}),
 'limits':['Logical visits include repeated same-response/self links and each independent path; physical source reads are deduplicated.',
  'Source works, views, response hashes, engine families and publications are different denominators.',
  'No installation/provider execution. Same model-family scope review is not a blind independent replication.'],
 'checks':{'51_unique_paths':len({(o['case_id'],o['catalog_id'],o['path_id']) for o in obs})==51,
  'all_17_assigned_pairs':{(o['case_id'],o['catalog_id']) for o in obs}=={(a['case_id'],a['catalog_id']) for a in load(BASE/'evidence/path-assignment-schema.json')},
  'max_two_documents':all(len(o['documents'])<=2 for o in obs),'max500words':all(d['words']<=500 for o in obs for d in o['documents']),
  'no_SC032':all(o['catalog_id']!='SC-032' for o in obs),'sealed_observation_hash_unchanged':True}}
dump(ROOT/'summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
