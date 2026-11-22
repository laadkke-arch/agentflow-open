"""Concrete storage examples; no decision view or presealed card is altered."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def readl(n):return [json.loads(x) for x in (P/n).read_text().splitlines() if x.strip()]
def enc(v):return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
A={a['attempt_id']:a for a in readl('attempts.jsonl') if a.get('operation')=='GET'}
C={c['ref_id']:c for c in readl('components.jsonl')}
U={u['ref_id']:u for u in json.loads((P/'evidence/replay-units.json').read_text())}
PK={(r['ref_id'],r['view']):r for r in readl('packets.jsonl')}
records=[];units=[]
for r in readl('references.jsonl'):
    rid=r['ref_id'];b=PK[(rid,'B')]['parts']['B'];h=C[rid]['H']
    lean={'ref_id':rid,'configuration':'C1_context_link_only','original_href':r['original_href'],
        'link_text':r['link_text'],'context':r['context'],'purpose':r['minimal_purpose']}
    baseline={'ref_id':rid,'configuration':'C1_B_presealed','B':b,'B_sha256':hashlib.sha256(b.encode()).hexdigest()}
    hist={**baseline,'configuration':'C2_BH_with_provenance','H':h['text'],'H_sha256':h['sha256'],
        'H_source_ids':h['source_ids'],'H_spans':[{k:v for k,v in s.items() if k!='text'} for s in h['spans']],
        'historical_retrieval_units':[{k:A[aid].get(k) for k in ['attempt_id','url','final_url','sha256','received_body_bytes','finished_utc']} for aid in U[rid]['H_attempt_ids']],
        'acquisition_utc_is_not_event_date':True,'preserves_full_archive':False}
    row={'ref_id':rid,'B_text_bytes':len(b.encode()),'H_text_bytes':len(h['text'].encode()),'serialized':{}}
    for record in [lean,baseline,hist]:
        data=enc(record); row['serialized'][record['configuration']]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        records.append(record)
    row['lean_path_rediscovery']='unmeasured; archive edition/member and historical source locators are not retained unless literal in the citation context'
    units.append(row)
(P/'retention-options.jsonl').write_bytes(b''.join(enc(r) for r in records))
summary={'record_units':units,'physical_serialized_file_bytes':(P/'retention-options.jsonl').stat().st_size,
    'configuration_bytes':{k:sum(r['serialized'][k]['bytes'] for r in units) for k in ['C1_context_link_only','C1_B_presealed','C2_BH_with_provenance']},
    'all_B_logical_text_bytes':sum(r['B_text_bytes'] for r in units),'all_H_logical_text_bytes':sum(r['H_text_bytes'] for r in units),
    'definition_limit':'C1_B_presealed is stronger than context+link only; original distribution/edition/member is already in B. No observed reader contrast isolates removing that metadata.',
    'cost_limit':'Serialized bytes are measured for these concrete files, not database/storage-engine/model/human cost. H excerpt retention does not preserve an entire historical source or original N query timestamp.'}
(P/'evidence/retention-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='record_units'},ensure_ascii=False))
