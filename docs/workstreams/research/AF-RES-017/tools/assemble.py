"""Assemble owned research ledgers; never fetch or rewrite external records."""
import json
from pathlib import Path
import argparse

p=Path(__file__).resolve().parents[1]
args=argparse.ArgumentParser();args.add_argument('--methods',action='store_true');args=args.parse_args()
cases=[];sources=[];excluded=[];logs=[]
for lane in ['blogs','prs','root']+(['methods'] if args.methods else []):
    d=p/'evidence'/lane
    if (d/'draft-cases.json').exists():
        a=json.loads((d/'draft-cases.json').read_text());cases+=a if isinstance(a,list) else a['cases']
    s=json.loads((d/'sources.json').read_text());sources+=s if isinstance(s,list) else s['sources']
    if isinstance(s,dict):excluded+=s.get('excluded',[])
    if (d/'additional-sources.json').exists():sources+=json.loads((d/'additional-sources.json').read_text())
    logs.append({'lane':lane,'records':json.loads((d/'SEARCH_LOG.json').read_text())})
    if (d/'additional-searches.json').exists():logs.append({'lane':lane+'-additional','records':json.loads((d/'additional-searches.json').read_text())})
assert len({c['id'] for c in cases})==len(cases)
assert len({s['id'] for s in sources})==len(sources)
for c in cases:c.setdefault('coder_b',None)
(p/'cases/CASES.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
(p/'sources.json').write_text(json.dumps({'sources':sources,'excluded':excluded,'note':'Observed decision episodes and controls; eligibility is explicit and separate.'},ensure_ascii=False,indent=2)+'\n')
(p/'SEARCH_LOG.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'sources':len(sources),'excluded':len(excluded)},ensure_ascii=False))
