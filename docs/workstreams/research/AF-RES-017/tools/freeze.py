"""Freeze A labels and a label-free packet before invoking the independent context."""
import json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parents[1]
if (P/'coding/coder-a.json').exists():raise SystemExit('A already frozen; never overwrite it.')
cases=json.loads((P/'cases/CASES.json').read_text());sources={s['id']:s for s in json.loads((P/'sources.json').read_text())['sources']}
axes=['missed_form','missed_contribution','missed_relation','legacy_S1','late_discovery_status']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(f):return hashlib.sha256((P/f).read_bytes()).hexdigest()
a={'review_type':'작업자 A coding, before internal separate review','model':'GPT-6 Astra Pro','frozen_at_utc':now,'codebook_sha256':sha('coding/CODEBOOK.md'),'cases_input_sha256':sha('cases/CASES.json'),'labels':[{'id':c['id'],**{k:c[k] for k in axes},'reason':c.get('summary',c.get('evidence_notes','See source records and selected scope.'))} for c in cases]}
(P/'coding/coder-a.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
records=[]
for c in sorted(cases,key=lambda x:hashlib.sha256(('AF-RES-017-20261121-1717'+x['id']).encode()).hexdigest()):
    facts=[]
    for sid in c['source_ids']:
        s=sources[sid]
        facts.append({'source_id':sid,'url':s['url'],'version_or_date':s['version_or_date'],'sections_read':s['sections_read'],'observed_content':s['confirmed'],'limits':s['limits']})
    records.append({'id':c['id'],'selected_scope':c['selected_scope'],'built':c['built'],'external_target':c['missed'],'need_statement':c['need_statement']['text'],'official_description':c['official_description'],'decision_date':c['decision_date'],'decision_date_basis':c.get('decision_date_kind',c.get('date_precision_note','Unspecified date evidence')),'discovery_or_assessment_date':c['discovery_date'],'reported_discovery_path':c['discovery_path'],'reported_initial_reason':c['miss_reason'],'evidence':facts})
packet={'purpose':'Internal separate review with no A labels/results. Evidence is shared worker extraction, not independently re-collected full originals. Code the explicitly selected scope.','seed':'AF-RES-017-20261121-1717','record_count':len(records),'records':records}
(P/'coding/blind-packet.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
diagnostics={'purpose':'Synthetic discrimination checks, excluded from the40cases and agreement denominator. Reject each unsupported claim using codebook boundaries.','items':[
{'id':'D01','facts':'Custom implementation was committed2014-01. Package first existed2013-01 but the required API first shipped2015-01. The team adopted that API2015-02.','claim':'The required solution existed at the2014decision and the team merely failed to discover it.'},
{'id':'D02','facts':'An ADR before implementation names the library, tests it, and rejects it because its license forbids the planned redistribution.','claim':'Custom implementation proves the team did not know the library.'},
{'id':'D03','facts':'A merged PR replaces200lines with a dependency. Neither discussion nor old code says whether the team knew the dependency before.','claim':'The200deletedlines are measured labor wasted because of ignorance.'},
{'id':'D04','facts':'A2026page reports100000downloads. The decision was2012. No2012popularity record is supplied.','claim':'The package was famous at the2012decision.'},
{'id':'D05','facts':'An accepted ADR says the team expects the migration to take six months. No start/end or completion record is supplied.','claim':'Six months is an observed migration cost.'},
{'id':'D06','facts':'A developer renames an existing identical flow-control procedure circuit breaker. The same states, thresholds, data flow, and recovery behavior existed before the new name.','claim':'The new electrical name proves a newly imported design structure.'},
{'id':'D07','facts':'The decision is2012-06. An archived official registry report dated2012-05 records100000downloads and200enterprise users.','claim':'There is no dated evidence at all of predecision adoption or prominence.'}
]}
(P/'coding/diagnostic-packet.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'A_rows':len(cases),'A_sha256':sha('coding/coder-a.json'),'packet_sha256':sha('coding/blind-packet.json'),'packet_bytes':(P/'coding/blind-packet.json').stat().st_size}))
