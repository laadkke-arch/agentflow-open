"""Validate and collect already written decisions without changing answers."""
import csv,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parents[1]
rows=[];receipts=[]
for n in range(1,5):
    reader=f'fresh-{n}';d=P/'readers'/reader
    assignments=json.loads((d/'assignment.json').read_text())['assignments']
    output=[json.loads(x) for x in (d/'output.jsonl').read_text().splitlines() if x.strip()]
    assert len(output)==12,(reader,len(output))
    for a,r in zip(assignments,output):
        assert r['ref_id']==a['case_id'] and r['view']==a['view'] and r['case_order']==a['case_order'],(reader,a)
        actual=hashlib.sha256((d/a['file']).read_bytes()).hexdigest()
        assert actual==a['file_sha256']==r['input_sha256'],(reader,r['ref_id'],'input hash')
        assert r['action'] in ('KEEP','REPLACE','HOLD')
        assert r['reader_id']==reader
        rows.append(r)
    receipts.append({'reader_id':reader,'rows':len(output),'output_sha256':hashlib.sha256((d/'output.jsonl').read_bytes()).hexdigest(),'input_matches':True,'parent_history':'none','receipt_path':str((d/'run-receipt.json').relative_to(P))})
assert len({(r['ref_id'],r['view']) for r in rows})==48
keys=list(dict.fromkeys(k for r in rows for k in r))
with (P/'decisions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,keys,lineterminator='\n');w.writeheader()
    for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
receipt={'recorded_utc':datetime.now(timezone.utc).isoformat(),'decisions':48,'cases':12,'views_per_case':4,'reader_receipts':receipts,'same_case_other_view_reported':sum(r['saw_same_case_other_view'] for r in rows),'prior_outcome_reported':sum(r['saw_prior_outcome'] for r in rows),'background_used_reported':sum(r['background_used'] for r in rows),'decisions_sha256':hashlib.sha256((P/'decisions.csv').read_bytes()).hexdigest(),'adjudication_not_yet_written':True}
(P/'evidence/decision-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False))
