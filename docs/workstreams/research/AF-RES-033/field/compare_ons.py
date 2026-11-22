"""Read-only comparison of ONS MYE3 original and corrected source workbooks."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import openpyxl

ROOT=Path(__file__).resolve().parent
paths=[ROOT/'cache/F04-v1.xlsx',ROOT/'cache/F04-v2.xlsx']
books=[openpyxl.load_workbook(p,read_only=True,data_only=True) for p in paths]
tables=[{row[0].value:row for row in w['MYE3'].iter_rows(min_row=9) if isinstance(row[0].value,str) and len(row[0].value)==9} for w in books]
assert tables[0].keys()==tables[1].keys()
changes=[];samples=[]
for code,old in tables[0].items():
    new=tables[1][code]
    assert [c.value for c in old[:3]]==[c.value for c in new[:3]],code
    for i,(a,b) in enumerate(zip(old,new)):
        if a.value!=b.value:
            changes.append({'code':code,'name':old[1].value,'geography':old[2].value,'cell':a.coordinate,'old':a.value,'corrected':b.value})
    if code in ['K04000001','E92000001','E12000001','E06000047']:
        samples.append({'code':code,'name':old[1].value,'cells':[c.coordinate for c in old[7:10]],
                        'old_inflow_outflow_net':[c.value for c in old[7:10]],
                        'corrected_inflow_outflow_net':[c.value for c in new[7:10]]})
notice=[{'row':i,'text':' | '.join(str(v) for v in row if v is not None)} for i,row in enumerate(books[1]['Correction notice'].iter_rows(values_only=True),1) if any(v is not None for v in row)]
result={'source_id':'F04','checked_utc':datetime.now(timezone.utc).isoformat(),
        'read_only':True,'sheet':'MYE3','keyed_rows':len(tables[0]),'headers':[c.value for c in books[0]['MYE3'][8]],
        'file_hashes':{p.name:sha256(p.read_bytes()).hexdigest() for p in paths},
        'changed_cells':len(changes),'changed_rows':len(set(c['code'] for c in changes)),
        'changed_columns':dict(Counter(''.join(x for x in c['cell'] if x.isalpha()) for c in changes)),
        'samples':samples,'changes':changes,'correction_notice_locations':['Correction notice!A1:A3'],
        'correction_notice_excerpt':'This error did not impact net internal migration or population totals.',
        'correction_date':'2023-12-19',
        'boundary':'Only the keyed MYE3 table was compared; not all workbook sheets and not a rerun of ONS estimation.'}
(ROOT/'ons-correction-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for w in books:w.close()
print(json.dumps({k:result[k] for k in ['keyed_rows','changed_cells','changed_rows','changed_columns','samples','correction_notice_locations','correction_date']},ensure_ascii=False,indent=2))
