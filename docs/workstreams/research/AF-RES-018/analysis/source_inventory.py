#!/usr/bin/env python3
"""Audit original methods/comparison readings separately from question samples."""
from pathlib import Path
import collections,json,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
required={'id','url','accessed_at_utc','source_type','title','version_or_date',
          'sections_read','confirmed','limits','level','used_in'}
sources=[];excluded=[];errors=[]
for sub in ['evaluation','structured']:
    d=json.loads((ROOT/'evidence'/sub/'sources.json').read_text())
    for row in d['sources']:
        miss=sorted(required-set(row))
        if miss:errors.append({'id':row.get('id'),'missing':miss})
        row=dict(row);row['counted_as']='methods_comparison';row['ledger']='evidence/'+sub+'/sources.json'
        sources.append(row)
    excluded.extend(d.get('excluded',[]))
def site(url):
    h=urllib.parse.urlsplit(url).hostname or ''
    if h.endswith('.umn.edu'):return 'umn.edu'
    if h.endswith('.ncbi.nlm.nih.gov'):return 'ncbi.nlm.nih.gov'
    return h.removeprefix('www.')
groups=collections.defaultdict(list)
for r in sources:groups[site(r['url'])].append(r['id'])
count=sum(min(3,len(v)) for v in groups.values())
method_count=len(sources)
for ledger in ['gold/draft-a/sources.json','gold/draft-b/sources.json','questions/new-draft/sources-draft.json',
               'analysis/mapping-evidence.json','evidence/citation-resolution.json','evidence/run-readings.json','evidence/judging-readings.json','evidence/claim-readings.json']:
    path=ROOT/ledger
    if not path.exists():continue
    data=json.loads(path.read_text())
    for row in data['sources']:
        row=dict(row);row.setdefault('counted_as','question_or_check_evidence_not_methods');row['ledger']=ledger
        miss=sorted(required-set(row))
        if miss:errors.append({'id':row.get('id'),'missing':miss})
        sources.append(row)
    excluded.extend(data.get('excluded',[]))
fixed=ROOT/'evidence/input-reading.json'
if fixed.exists():sources.extend(json.loads(fixed.read_text()))
ids=[r['id'] for r in sources]
root_audit=ROOT/'evidence/root-rechecks.json'
if root_audit.exists():
    root_data=json.loads(root_audit.read_text())
    excluded.extend(root_data.get('excluded',[]))
    for recheck in root_data.get('readings',[]):
        matches=[r for r in sources if r['id']==recheck['source_id']]
        if len(matches)==1:matches[0].setdefault('root_rechecks',[]).append(recheck)
if len(ids)!=len(set(ids)):errors.append({'duplicate_ids':[k for k,v in collections.Counter(ids).items() if v>1]})
out={'sources':sources,'excluded':excluded,
     'counting':{'direct_methods_readings':method_count,'site_capped_count':count,
                 'minimum':25,'by_site':dict(groups),'errors':errors,
                 'total_source_records':len(sources),
                 'different_fields':5,
                 'independence_note':'STR03/STR04 share the same 50 analysts. Literature count is not independent experiments.'}}
(ROOT/'sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out['counting'],ensure_ascii=False,indent=2))
raise SystemExit(bool(errors) or count<25)
