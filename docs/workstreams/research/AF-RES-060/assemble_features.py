"""Normalize the two independently kept editing ledgers; never fetch or rank."""
from pathlib import Path
from datetime import datetime, timezone
import csv, json, hashlib, re

P = Path(__file__).resolve().parent
def j(x): return json.dumps(x, ensure_ascii=False, separators=(',', ':'))
def n(x): return re.sub(r'\s+', ' ', x.casefold().replace('-', ' ')).strip()
catalog = list(csv.DictReader((P/'inputs/af-res-056/catalog.csv').open()))
ledgers = {}
for owner in ['features-schema', 'features-ld']:
    for r in json.loads((P/'evidence'/owner/'features.json').read_text()):
        assert r['catalog_id'] not in ledgers
        ledgers[r['catalog_id']] = (owner,r)
assert set(ledgers) == {c['catalog_id'] for c in catalog}
rows=[]
for c in catalog:
    owner,r=ledgers[c['catalog_id']];cost=r['cost'];is_schema=owner=='features-schema'
    features=r.get('added_features',r.get('features',[]));assert len(features)<=3
    f0=json.loads(c['search_fields_json'])
    assert r['original_destination_url']==c['destination_url']
    evidence=r.get('feature_provenance',r.get('feature_evidence',[]))
    assert len(features)==len(evidence)
    for term,e in zip(features,evidence):
        window=P/'evidence'/owner/e['window_file']
        # Whitespace can differ after formatting; spelling remains literal.
        assert re.sub(r'\s+',' ',term) in re.sub(r'\s+',' ',window.read_text()), (c['catalog_id'],term)
    if is_schema:
        attempts=cost['document_attempts'];reads=cost['documents_directly_read'];windows=cost['windows_directly_read'];words=cost['display_words_directly_read']
        metadata=cost['metadata_requests_with_retained_receipts'];meta_status='lower_bound' if cost['metadata_count_is_lower_bound'] else 'complete_receipts'
        source_ids=r['source_ids'];version=r['version'];sha=r['commit'];version_status=r['version_selection']
        extra=0;blank=r['blank_reason'] or '';vlimits=r.get('version_limitations',[])
    else:
        attempts=cost.get('scheduled_document_actions',cost['logical_document_actions'])
        reads=(1 if r.get('window') else 0)+sum(1 for z in r.get('followup_ids',[]) if z!='DOTNETAPI')
        windows=reads;words=cost['logical_body_words'];metadata=cost['metadata_requests'];meta_status='recorded_requests'
        source_ids=[r['source_id']]+['F-LINK-'+z for z in r.get('followup_ids',[])];version=r['implementation_version'];sha=r['implementation_sha'];version_status=r['version_status']
        extra=cost['extra_interpretation_exposure_words'];blank=r['blank_reason'];vlimits=[r.get('editor_note','')]
    assert attempts<=2
    rows.append({
        'catalog_id':c['catalog_id'],'family':c['family'],'posted_rank':c['posted_rank'],'title':c['title'],
        'f0_fields_json':j(f0),'added_features_json':j(features),'f1_fields_json':j(f0+features),
        'literal_terms_added':len(features),'new_strings_beyond_f0':sum(n(t) not in {n(x) for x in f0} for t in features),
        'original_destination_url':c['destination_url'],'editor_fixed_url':r['fixed_url'],
        'implementation_sha':sha or '', 'implementation_version':version or '', 'version_status':version_status,
        'exact_day_response':'not_historical_response_proven; pinned_edition_or_explicit_limit',
        'role':r['role'],'engine_lineage':r['engine_lineage'],'feature_evidence_json':j(evidence),'source_ids_json':j(source_ids),
        'primary_document_actions_attempted':attempts,'logical_documents_read':reads,'logical_windows_read':windows,'logical_display_words':words,
        'metadata_requests_observed':metadata,'metadata_count_status':meta_status,'extra_interpretation_display_words':extra,
        'blank_reason':blank,'implementation_absence_judgment':'not_assessed; an empty field does not establish absent support',
        'version_and_role_limits_json':j(vlimits),'editor_ledger':f'evidence/{owner}/features.json'
    })
with (P/'features.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
summary={
    'assembled_utc':datetime.now(timezone.utc).isoformat(),'exposure':'no holdout metadata/body or F1 rankings opened',
    'rows':len(rows),'rows_nonempty':sum(x['literal_terms_added']>0 for x in rows),
    'literal_feature_names':sum(x['literal_terms_added'] for x in rows),'rows_with_new_strings_beyond_f0':sum(x['new_strings_beyond_f0']>0 for x in rows),
    'feature_names_beyond_f0_exact_fields':sum(x['new_strings_beyond_f0'] for x in rows),
    'blank_rows':[x['catalog_id'] for x in rows if not x['literal_terms_added']],
    'logical_document_actions_attempted':sum(x['primary_document_actions_attempted'] for x in rows),
    'logical_windows_read':sum(x['logical_windows_read'] for x in rows),
    'logical_display_words':sum(x['logical_display_words'] for x in rows),
    'metadata_requests_retained_lower_bound':sum(x['metadata_requests_observed'] for x in rows),
    'extra_interpretation_display_words':sum(x['extra_interpretation_display_words'] for x in rows),
    'limitations':['Per-row actions include shared responses and same-document fragment actions; do not equate their sum to unique fetched documents.', 'Metadata request count is a retained-receipt lower bound; some initial redirect/tag retries are missing.', 'Repeated cross-review of identical displayed windows is not a wall-clock/token billing measure. The main cost is the registered one-window-per-action reading budget; known discarded interpretation windows are separate.', 'Exact historical response at the F0 capture instant is not proved by a pinned release.'],
    'sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['features.csv','evidence/features-schema/features.json','evidence/features-ld/features.json']}
}
(P/'evidence/feature-freeze.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
