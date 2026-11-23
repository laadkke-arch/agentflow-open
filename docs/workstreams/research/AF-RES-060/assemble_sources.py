"""Keep source-event rows, normalize their schema, and count works separately."""
from pathlib import Path
from datetime import datetime, timezone
import json, re, collections

P=Path(__file__).resolve().parent
files=[P/'evidence'/x/'sources.jsonl' for x in ['root-sources','authority','features-schema','features-ld','holdout','paths-schema','paths-ld','root-paths','sensitivities']]
feature_rows=[]
for owner in ['features-schema','features-ld']:
    feature_rows += json.loads((P/'evidence'/owner/'features.json').read_text())
provider_ids={r['catalog_id']:'supplier-'+r['fixed_url'].split('github.com/')[-1].split('/blob/')[0].casefold().replace('/','--') if 'github.com/' in (r['fixed_url'] or '') else 'supplier-'+r['catalog_id'] for r in feature_rows}
provider_work_aliases={r['work_id']:provider_ids[r['catalog_id']] for r in feature_rows}

def canonical(s):
    u=(s['version_url'] or s['original_url'] or '').lower();sid=s['source_id'];wid=s['work_id']
    m=re.fullmatch(r'F-(SC-\d+|LD-\d+)',sid)
    if m:return provider_ids[m[1]]
    if wid in provider_work_aliases:return provider_work_aliases[wid]
    if ('json-ld' in u and ('api' in u or '/json-ld.org/spec/latest/json-ld-api' in u)) and ('w3.org/' in u or 'json-ld.org/' in u):return 'spec-jsonld-api'
    if ('json-ld11-framing' in u or 'json-ld-framing' in u) and ('w3.org/' in u or 'json-ld.org/' in u):return 'spec-jsonld-framing'
    if 'draft-handrews-json-schema-validation-01' in u:return 'spec-jsonschema-validation-07'
    if 'draft-handrews-json-schema-01' in u:return 'spec-jsonschema-core-07'
    if 'draft-zyp-json-schema-04' in u:return 'spec-jsonschema-core-07'
    if sid in ['P-SC-038-D2','P-SC032-META']:return 'jsonschema-normative-metaschema'
    if 'nodejs.org/api/' in u or 'nodejs.org/docs/' in u:return 'manual-nodejs-api'
    if 'api.stackexchange.com/docs' in u:return 'manual-stackexchange-api'
    if 'loc.gov/marc/authority/' in u:return 'editorial-marc-authority-format'
    if 'getty.edu' in u and ('guidelines' in u or '/aat' in u and 'subjectid=' not in u and 'vocab.getty.edu/aat/' not in u):return 'editorial-getty-aat-guidelines'
    return wid

rows=[];ids=set()
for p in files:
    if not p.exists():continue
    for line in p.read_text().splitlines():
        if not line.strip():continue
        a=json.loads(line);sid=a['source_id'];assert sid not in ids,(sid,str(p));ids.add(sid)
        s=dict(a)
        s.update(
            source_id=sid,work_id=a.get('work_id',sid),kind=a.get('kind','unspecified'),lineage=a.get('lineage',a.get('work_id','')),
            questions=a.get('questions',a.get('Q',[])),cases=a.get('cases',a.get('case_ids',a.get('catalog_ids',[]))),
            original_url=a.get('original_url',a.get('url','')),version_url=a.get('version_url',a.get('fixed_url',a.get('original_url',a.get('url','')))),
            version_date_or_hash=a.get('version_date_or_hash',a.get('edition',a.get('fixed_edition',a.get('version',a.get('sha256',a.get('body_sha256','')))))),
            opened_utc=a.get('opened_utc') or a.get('read_utc') or a.get('read_utc_interval') or a.get('retrieved_utc',''),
            location=a.get('location',a.get('locus','')),confirmed=a.get('confirmed',a.get('checked',a.get('finding',''))),
            limits=a.get('limits',a.get('scope_and_limits',a.get('scope_and_limit',''))),observation_type=a.get('observation_type',a.get('evidence_type',a.get('observation_author_statement_inference',''))),
            opposing_source_ids=a.get('opposing_source_ids',a.get('counter_evidence_ids',[])),read_status=a.get('read_status',a.get('access_status','not_recorded')),
            previous_work_reuse=a.get('previous_work_reuse',a.get('existing_work_reused',a.get('new_external_work') is False)),
            external_primary=a.get('external_primary',not sid.startswith('IN056-')),
            source_ledger=str(p.relative_to(P)),
        )
        s['canonical_work_id']=canonical(s)
        s['new_work_for_060']=a.get('new_work_for_060',a.get('new_external_work',not s['previous_work_reuse']))
        status=s['read_status']
        read=status in ['read','opened_and_read','direct_primary','direct_window_read','directly_read_bounded_window','cache_failed_web_read_succeeded','read_original_body','direct_read','bounded_web_reader_primary_document_excerpt'] or status.startswith('directly_read')
        s['qualifying_direct_read']=bool(s['external_primary'] and read)
        if sid in ['P-LD-008-D2','P-LD-008-D3']:
            s['qualifying_direct_read']=False;s['quota_exclusion']='Front matter or package metadata only; observed and costed, but excluded from substantive primary-work quota. A current-study reuse flag alone is not a read exclusion.'
        if sid in ['F-SC-020','F-SC-028','F-SC-031','F-SC-033','F-SC-016-D2']:
            s['qualifying_direct_read']=False;s['quota_exclusion']='Identity/link/development-instruction-only window; kept in editing cost, excluded from substantive primary-work quota.'
        rows.append(s)
(P/'sources.jsonl').write_text(''.join(json.dumps(s,ensure_ascii=False,separators=(',',':'))+'\n' for s in rows))
qualified=[s for s in rows if s['qualifying_direct_read']]
works=collections.defaultdict(list)
for s in qualified:works[s['canonical_work_id']].append(s)
summary={
    'counted_utc':datetime.now(timezone.utc).isoformat(),'source_events':len(rows),'qualifying_direct_source_events':len(qualified),
    'distinct_qualifying_works':len(works),'distinct_new_works':sum(not any(s['previous_work_reuse'] for s in w) for w in works.values()),
    'works':[{'canonical_work_id':k,'source_ids':[s['source_id'] for s in v],'previous_work_reuse':any(s['previous_work_reuse'] for s in v),'kinds':sorted(set(s['kind'] for s in v))} for k,v in sorted(works.items())],
    'limitations':['Unique documents, source events, supplier rows, and independent engines have different denominators.', 'A failed retrieval/search snippet/internal input never counts toward 22.', 'Additional engine-family collapse is reported separately; README authorship is not independence of executable engines.'],
}
(P/'evidence/source-counts.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['works','limitations']},ensure_ascii=False))
