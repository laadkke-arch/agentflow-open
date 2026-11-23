"""Normalize source ledgers without inflating duplicate representations or events."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent

def values(row,*keys):
    for key in keys:
        if key in row and row[key] is not None: return row[key]
    return None

def arr(x):
    if x is None:return []
    return x if isinstance(x,list) else [x]

def main():
    normalized=[];seen_ids=set();seen_units=set()
    for f in sorted((P/'support').glob('sources_*.jsonl')):
        for lineno,line in enumerate(f.read_text().splitlines(),1):
            r=json.loads(line)
            sid=r['source_id'];assert sid not in seen_ids,sid;seen_ids.add(sid)
            url=values(r,'url','original_url')
            event=values(r,'independent_event_id','independent_work_id','event_id')
            count=values(r,'count_primary','counted_primary','counts_toward_material_minimum') is True
            reason=r.get('exclusion_reason','')
            # These API/history representations corroborate already-counted public pages.
            if sid in {'PL13','PL16','PL20','PL21','PL22'}:
                count=False;reason='same public platform event/history or metadata; conservative supplementary representation exclusion'
            if sid=='NR03':
                count=False;reason='same Pandoc frame rank23 R0 already counted; additional API representation'
            if 'comment' in r.get('kind','').lower():
                count=False;reason='comment evidence retained, excluded from minimum primary-unit count'
            unit=r.get('primary_unit') or url
            if count and unit in seen_units:
                count=False;reason='duplicate primary unit'
            if count:seen_units.add(unit)
            record=dict(source_id=sid,independent_event_id=event,kind=r['kind'],original_url=url,version=values(r,'version','version_locator','document_time') or 'current at direct read; no immutable revision identifier supplied',location=values(r,'location','locator','version_locator') or 'returned source record',direct_read_utc=r['direct_read_utc'],read_time_basis=r.get('read_time_basis','direct reading completion checkpoint, not network request start'),linked_questions=arr(values(r,'questions','question_ids','linked_q')),linked_cases=arr(values(r,'cases','case_id','linked_cases')),linked_claims=arr(values(r,'claims','claim_ids','linked_claims')) or arr(values(r,'evidence_relation','support_or_refutation')),confirmed_content=values(r,'confirmed','confirmed_content','verified_content'),observer=r.get('observer','researcher direct reading; original actor in linked record'),support_or_refutation=values(r,'evidence_relation','support_or_refutation') or dict(supports=r.get('supports'),refutes=r.get('refutes')),limitations=values(r,'limitations','limits','limits_unknowns') or 'source does not itself verify original-user execution',direct_read=True,count_primary=count,primary_unit=unit,exclusion_reason=reason,ledger_path=str(f.relative_to(P)),ledger_line=lineno)
            for key in ('commit','blob_sha','history_url','raw_sha256','snapshot_path','tool_ref','supplemental_location','supplemental_direct_read_utc','supplemental_stage','supplemental_confirmed'):
                if key in r:record[key]=r[key]
            assert url and event and record['confirmed_content'],sid
            normalized.append(record)
    (P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in normalized))
    primary=[x for x in normalized if x['count_primary']]
    print('source records',len(normalized),'primary units',len(primary),'independent events/works',len({x['independent_event_id'] for x in primary}))

if __name__=='__main__':main()
