"""Assemble SC001–032 editorial evidence only; never reads requirements or matches."""
import csv, hashlib, json, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
NOW = datetime.now(timezone.utc).isoformat()
def read(path):
    return json.loads((ROOT / path).read_text())
def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def norm(s):
    return ' '.join(s.split())

catalog = {r['catalog_id']: r for r in csv.DictReader((BASE / 'inputs/af-res-056/catalog.csv').open())}
decisions = read('decisions.json')
versions = {r['id']: r for r in read('metadata/final-versions.json')}
docs = {r['id']: r for r in read('metadata/final-documents.json')}
pages = {r['id']: r for r in read('metadata/html-pages.json')}
follow = read('metadata/followup-documents.json')
lineage = json.loads((BASE / 'inputs/af-res-056/source-lineage.json').read_text())

# Mechanical receipt corrections before F1 freeze. Rendered text is unchanged.
window30 = read('windows/SC-030.json')
if window30['raw_sha256'] != pages['SC-030']['sha256']:
    window30['selected_container_serialization_sha256'] = window30['raw_sha256']
    window30['raw_sha256'] = pages['SC-030']['sha256']
    window30['container_note'] = 'main/article serialized by lxml before rendering; response body hash kept separately from selected-container hash'
    write('windows/SC-030.json', window30)
window25 = read('windows/SC-025.json')
window25['followup'] = {'text': 'URL under Erlang API Docs', 'href': follow[-1]['url'], 'classification': 'preceding heading establishes API purpose'}
window25['followup_attempt_result'] = 'HTTP 503; not read; no replacement'
write('windows/SC-025.json', window25)

attempts = []
def attempt(cid, kind, url, utc, success, evidence, note=''):
    attempts.append({'attempt_id': 'SC-A%03d' % (len(attempts) + 1), 'catalog_id': cid,
        'kind': kind, 'url': url, 'utc': utc, 'success': bool(success),
        'receipt': evidence, 'note': note, 'count_basis': 'retained request receipt'})

for r in read('metadata/releases.json'):
    attempt(r['id'], 'metadata-release', r['url'], r.get('at'), r.get('ok'), 'metadata/releases.json', str(r.get('error') or '')[:300])
initial_versions = read('metadata/versions.json')
for r in initial_versions:
    attempt(r['id'], 'metadata-commit', r['commit_url'], r.get('observed_at'), not r.get('error'), 'metadata/versions.json', str(r.get('error') or '')[:300])
for r in versions.values():
    if r['id'] not in {v['id'] for v in initial_versions}:
        attempt(r['id'], 'metadata-commit', r.get('commit_url') or ('https://api.github.com/repos/' + r['repo'] + '/commits/' + r['ref']), r.get('observed_at'), bool(r.get('commit')), 'metadata/final-versions.json')
for r in read('metadata/final-readme-paths.json'):
    if r.get('url'):
        attempt(r['id'], 'metadata-directory', r['url'], r.get('at'), not r.get('error'), 'metadata/final-readme-paths.json')
for name in ['metadata/additional-verification.json', 'metadata/additional-connector.json']:
    for r in read(name):
        attempt(r['catalog_id'], 'metadata-verification', r['url'], r['utc'], r.get('success', r.get('status') == 200), name, r.get('purpose', '') + ': ' + r.get('error', ''))
for r in docs.values():
    attempt(r['id'], 'document-initial', r['url'], r['at'], not r.get('error'), 'metadata/final-documents.json')
for r in pages.values():
    attempt(r['id'], 'document-initial', r['url'], r['at'], r.get('status') == 200, 'metadata/html-pages.json')
for r in follow:
    attempt(r['id'][:6], 'document-followup', r['url'], r['at'], not r.get('error'), 'metadata/followup-documents.json', r.get('error', ''))
(ROOT / 'acquisition-ledger.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in attempts))

def raw_info(cid):
    paths = list((ROOT / '_raw').glob(cid + '.*'))
    assert len(paths) == 1, (cid, paths)
    p = paths[0]
    raw = p.read_bytes()
    return {'path': str(p.relative_to(ROOT)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
        'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}

def term_location(w, term, anchor):
    words = list(re.finditer(r'\S+', w['rendered_text']))
    text = ' '.join(m[0] for m in words)
    a = text.index(norm(anchor))
    t = text.find(term, a, a + len(norm(anchor)))
    if t < 0:
        t = text.index(term)
    n = len(text[:t].split()) - (1 if t and not text[t-1].isspace() else 0)
    n = max(0, n)
    # Find the exact occurrence nearest the anchored normalized token span.
    pos = words[n].start()
    candidates = [m.start() for m in re.finditer(re.escape(term), w['rendered_text'])]
    if candidates:
        pos = min(candidates, key=lambda x: abs(x-pos))
    line = w['rendered_text'][:pos].count('\n') + 1
    structures = [s for s in w['structures'] if s['tag'] in {'li','code','h1','h2','h3','h4','h5','h6'} and term in norm(s['text'])]
    return {'source_id': 'F-' + w['id'], 'window_file': 'windows/' + w['id'] + '.txt',
        'window_line': line, 'window_word_approx': n + 1, 'anchor': anchor,
        'eligible_structure_tags': sorted({s['tag'] for s in structures}),
        'selection_rule': 'first provider-owned functional heading/list/API term in document order; normalized literal dedup only'}

features, sources = [], []
for decision in decisions:
    cid = decision['id']; c = catalog[cid]; w = read('windows/' + cid + '.json')
    v = versions.get(cid); page = pages.get(cid); raw = raw_info(cid)
    assert raw['sha256'] == w['raw_sha256'], cid
    if v:
        assert raw['git_blob'] == w['source_blob'], (cid, raw['git_blob'], w['source_blob'])
        prior = [s for s in lineage if 'github.com/' + v['repo'].casefold() + '/' in s.get('url', '').casefold() and not s.get('kind','').startswith('접근 실패')]
        release = v.get('metadata', {}).get('selected')
        version_kind = 'inherited_AF_RES_056_exact_commit' if v.get('pin') else ('official_release_commit' if release else 'last_commit_at_or_before_cutoff_formal_release_unconfirmed')
        version_label = v.get('ref') if release else ('fixed commit ' + v['commit'])
        work = prior[0]['work_id'] if prior else 'provider-' + v['repo'].casefold().replace('/', '--')
    else:
        prior=[]; release=None; version_kind = 'declared_version_live_page' if cid == 'SC-030' else 'implementation_edition_unconfirmed'
        version_label = '1.2.1 (page declaration)' if cid == 'SC-030' else None
        work = 'provider-pinery-json-essentials-com' if cid == 'SC-030' else 'provider-extendsclass-json-schema-validator'
    wn = [w] + [read('windows/' + r['id'] + '.json') for r in follow if r['id'].startswith(cid) and not r.get('error')]
    ats = [a for a in attempts if a['catalog_id'] == cid]
    meta = [a for a in ats if a['kind'].startswith('metadata')]
    doc = [a for a in ats if a['kind'].startswith('document')]
    provenance = [{**term_location(w, term, anchor), 'term': term, 'ordinal': i+1,
        'scope_and_exclusions': decision['notes'], 'concept_uri': None,
        'concept_relation': 'not asserted by feature editor; no synonym expansion'} for i,(term,anchor) in enumerate(decision['features'])]
    note=[]
    if cid in {'SC-001','SC-004'}: note.append('Selected repository release belongs to another package in this monorepo; component has fixed commit but its own release label is unconfirmed.')
    if cid=='SC-010': note.append('Latest selection unchanged after 200 release records across ten pages; older pages not exhausted. Publication-order global completeness remains unconfirmed.')
    if cid=='SC-015': note.append('Selected v0.32.0 README installation example says 0.25.0. Pin is source commit, not proof that copied install command installs that edition.')
    if cid=='SC-016': note.append('Selected v1.14.5 README installation example says 1.14.4. Dependency API page has no matching implementation edition.')
    if cid=='SC-026': note.append('Preferred README forms absent; README.adoc is the same-commit official introduction fallback, approved under SCOPE rule3; alpha status is explicit.')
    if cid=='SC-030': note.append('HTTP Last-Modified 2022-09-09 and page v1.2.1 declaration; historical exact-cutoff response not recovered.')
    if cid=='SC-002': note.append('Canonical repository ExodusOSS/schemasafe shares official repository id271425023 with the old destination.')
    if cid=='SC-013': note.append('Canonical repository dashpay/JSONSchemaValidation shares official repository id145044400 with the old destination.')
    engine_family = 'ajv' if cid in {'SC-005','SC-006','SC-011','SC-018'} else ('jschon-family' if cid in {'SC-027','SC-028'} else work)
    row={'catalog_id':cid,'posted_rank':int(c['posted_rank']),'title':c['title'],
        'original_destination_url':c['destination_url'],'f0_search_fields':json.loads(c['search_fields_json']),
        'added_features':[x[0] for x in decision['features']], 'feature_provenance':provenance,
        'f1_search_fields':json.loads(c['search_fields_json'])+[x[0] for x in decision['features']],
        'fixed_url':w['source_url'],'commit':v['commit'] if v else None,'version':version_label,
        'version_selection':version_kind,'selected_release':release,'cutoff_utc':'2026-11-23T01:27:17Z',
        'exact_day_response_confirmed':False,'role':decision['role'],'engine':decision['engine'],'engine_lineage':engine_family,
        'work_id':work,'previous_AF_RES_056_work_reuse':bool(prior),'previous_source_ids':[s['source_id'] for s in prior],
        'source_ids':['F-'+x['id'] for x in wn]+['F-'+r['id'] for r in follow if r['id'].startswith(cid) and r.get('error')],
        'windows':[{'source_id':'F-'+x['id'],'file':'windows/'+x['id']+'.txt','metadata_file':'windows/'+x['id']+'.json',
          'heading':x['first_heading'],'feature_section_found':x['feature_section_found'],'word_count':x['word_count'],
          'response_sha256':x['raw_sha256'],'window_sha256':x['rendered_text_sha256'],'line_count':len(x['rendered_text'].splitlines())} for x in wn],
        'cost':{'document_attempts':len(doc),'document_fetch_successes':sum(a['success'] for a in doc),'documents_directly_read':len(wn),
          'windows_directly_read':len(wn),'display_words_directly_read':sum(x['word_count'] for x in wn),
          'metadata_requests_with_retained_receipts':len(meta),'metadata_failures_with_retained_receipts':sum(not a['success'] for a in meta),
          'metadata_count_is_lower_bound':cid in {'SC-001','SC-002','SC-004','SC-010','SC-013'},
          'unrecorded_metadata_scope':'Earlier redirect/tag/release retry diagnostics may be missing request-by-request receipts.' if cid in {'SC-001','SC-002','SC-004','SC-010','SC-013'} else None},
        'blank_reason':decision.get('blank_reason'),'implementation_lacks_feature_claim':False,
        'exclusions_and_conditions':decision['notes'],'version_limitations':note,
        'attempt_ids':[a['attempt_id'] for a in ats],'raw_cache':raw,'freeze_phase':'before holdout question bodies and before F1 rankings'}
    features.append(row)
    sources.append({'source_id':'F-'+cid,'work_id':work,'kind':'supplier README/official introduction','lineage':engine_family,
        'questions':['Q2','Q6','Q7'],'cases':[cid],'original_url':c['destination_url'],'fixed_url':w['source_url'],
        'edition':{'commit':row['commit'],'release':version_label,'response_sha256':raw['sha256'],'git_blob':w['source_blob'],
          'last_modified':page.get('last_modified') if page else None},
        'retrieved_utc':w['retrieved_utc'],'read_utc_interval':['2026-11-23T03:23:00Z',NOW],
        'locus':{'window':'windows/'+cid+'.txt','heading':w['first_heading'],'display_words':w['word_count'],
          'line_count':len(w['rendered_text'].splitlines()),'term_locations':provenance},
        'confirmed':{'literal_feature_terms':row['added_features'],'role':row['role'],'author_claim_scope':decision['notes']},
        'limits':['Only selected max500 displayed words read; fetching full response does not mean whole-document reading.',
          'No installation, execution, user success, or C1/C2 adjudication performed here.']+note+([decision['blank_reason']] if decision.get('blank_reason') else []),
        'evidence_type':['direct_observation_of_published_text','author_statement_not_execution'],
        'counter_evidence_ids':['F-'+cid],
        'counter_evidence_locus':decision['notes'],'read_status':'direct_window_read',
        'previous_work_reuse':bool(prior),'previous_source_ids':row['previous_source_ids'],
        'external_original':True,'new_work_eligible':not bool(prior),'reader':'/root/features_schema','requested_document_budget':2})

for r in follow:
    cid=r['id'][:6]; ok=not r.get('error'); w=read('windows/'+r['id']+'.json') if ok else None
    work={'SC-006':'nodejs-modules-api','SC-016':'json-java-api','SC-025':'provider-for-get--jesse'}[cid]
    sources.append({'source_id':'F-'+r['id'],'work_id':work,'kind':'first allowed API follow-up','lineage':work,
        'questions':['Q2','Q7'],'cases':[cid],'original_url':r['url'],'fixed_url':r.get('final_url',r['url']),
        'edition':{'response_sha256':r.get('sha256'),'last_modified':r.get('last_modified'),'implementation_version':'unconfirmed or foreign dependency'},
        'retrieved_utc':r['at'],'read_utc_interval':['2026-11-23T03:26:00Z',NOW] if ok else None,
        'locus':{'window':'windows/'+r['id']+'.txt','display_words':w['word_count']} if ok else None,
        'confirmed': 'Node File modules describes runtime file resolution; none of these are ajv-cli-owned functions.' if cid=='SC-006' else ('JSON-java frames landing only; no Everit-owned feature or matching version established.' if cid=='SC-016' else 'HTTP503; content not read.'),
        'limits':['No third document opened. No term added from this follow-up.',r.get('error') or ('Frame/noscript landing only; fallback text does not prove API delivery.' if cid=='SC-016' else 'Foreign runtime API, not provider feature evidence.')],
        'evidence_type':['direct_observation_of_response' if ok else 'access_failure'],
        'counter_evidence_ids':['F-'+cid],'read_status':'direct_window_read' if ok else 'access_failed',
        'previous_work_reuse':False,'external_original':ok,'new_work_eligible':ok and cid=='SC-006',
        'reader':'/root/features_schema'})

write('features.json',features)
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in sources))
summary={'frozen_utc':NOW,'stage1_sha':'87818991045cfa221e1b52a9b50c7550301d037b','exposure':'no holdout body or F1 ranking read',
    'catalog_rows_attempted':len(features),'rows_with_added_features':sum(bool(r['added_features']) for r in features),
    'added_literal_terms':sum(len(r['added_features']) for r in features),'blank_rows':[r['catalog_id'] for r in features if not r['added_features']],
    'initial_documents_read':len(features),'followup_attempts':len(follow),'followup_documents_read':sum(not r.get('error') for r in follow),
    'document_attempts':sum(r['cost']['document_attempts'] for r in features),'document_successes':sum(r['cost']['document_fetch_successes'] for r in features),
    'initial_display_words':sum(read('windows/'+r['catalog_id']+'.json')['word_count'] for r in features),
    'total_display_words':sum(r['cost']['display_words_directly_read'] for r in features),
    'metadata_requests_lower_bound':sum(r['cost']['metadata_requests_with_retained_receipts'] for r in features),
    'metadata_failed_requests_lower_bound':sum(r['cost']['metadata_failures_with_retained_receipts'] for r in features),
    'provider_publications_directly_read':32,'provider_publications_reused_from_056':sum(r['previous_AF_RES_056_work_reuse'] for r in features),
    'provider_publications_newly_opened':sum(not r['previous_AF_RES_056_work_reuse'] for r in features),
    'known_shared_engine_groups':{'ajv':['SC-005','SC-006','SC-011','SC-018'],'jschon-family':['SC-027','SC-028']},
    'source_count_limit':'Publication count is not independent implementation count. SC020/028 seven-word pages establish identity only; SC031 dev instructions; SC016-D2 frame landing is excluded from substantive-new-work quota.',
    'missing_cost_scope':'Five exceptional rows have earlier metadata retry diagnostics not fully retained; metadata count is a lower bound, not elapsed-time or total-request measurement.',
    'validation':{'rows_exactly_SC001_to_032': [r['catalog_id'] for r in features]==['SC-%03d'%i for i in range(1,33)],
       'every_literal_anchor_in_read_window':True,'all_source_response_hashes_match_local_cache':True,'no_window_exceeds_500_words':all(x['word_count']<=500 for r in features for x in r['windows']),
       'no_row_exceeds_two_document_attempts':all(r['cost']['document_attempts']<=2 for r in features),
       'same_supplier_pins_preserved':all(versions[c]['commit']==versions[c]['pin'] for c in ['SC-005','SC-006','SC-032'])}}
write('summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
