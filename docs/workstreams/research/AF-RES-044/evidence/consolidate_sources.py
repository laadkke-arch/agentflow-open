"""Consolidate only active source ledgers; preserve failures and deduplicate works."""
from pathlib import Path
import json,re,collections
from urllib.parse import urldefrag,urlsplit,urlunsplit
ROOT=Path(__file__).resolve().parents[1]
ACTIVE=[('P','evidence/pandoc/sources-P.jsonl'),('V','evidence/vega/sources-V.jsonl'),('CF','evidence/crossfield/sources.jsonl'),('C2','evidence/crossfield/controls-exploration-sources.jsonl'),('R','evidence/root-sources.jsonl'),('VH2','evidence/vega/second-hop-sources.jsonl'),('PYREVIEW','evidence/pandoc/review-sources.jsonl'),('PYH2','evidence/pandoc/control-second-hop-sources.jsonl'),('CH2','evidence/crossfield/control-second-hop-sources.jsonl'),('C2RV','evidence/crossfield/control-second-hop-revalidated-sources.jsonl'),('FINAL','evidence/final-source-review.jsonl')]
REQUIRED=['source_id','original_url','pinned_url_or_version','publisher','event_or_publication_date','checked_utc','locator','source_kind','verified_fact','limitation','question_ids','case_ids','duplicate_group','counted']
def canonical(r):
    u=urldefrag(r.get('canonical_url',r['original_url']))[0]
    u=re.sub(r'https://api.github.com/repos/([^/]+/[^/]+)/issues/(\d+)(?:/comments)?$',r'https://github.com/\1/issues/\2',u)
    return u
rows=[];seen={};bykind=collections.Counter();core=0
for prefix,name in ACTIVE:
    for line,text in enumerate((ROOT/name).read_text().splitlines(),1):
        r=json.loads(text);missing=set(REQUIRED)-set(r)
        if missing:raise ValueError((name,line,missing))
        original_id=r['source_id'];r['source_id']=prefix+':'+original_id;r['lane_source_id']=original_id;r['source_record']={'file':name,'line':line}
        key=canonical(r);r['lane_duplicate_group']=r['duplicate_group'];r['duplicate_group']=key
        if r['counted']:
            if key in seen:r['counted']=False;r['count_exclusion']='Same original work already counted as '+seen[key]
            else:
                seen[key]=r['source_id'];bykind[r['source_kind']]+=1
                if prefix not in ['VH2','PYH2','CH2','PYREVIEW']:core+=1
        elif 'count_exclusion' not in r:r['count_exclusion']='Lane marked repeated observation, supplementary route audit, non-primary source, or failed access; see limitation.'
        if 'claim_type' not in r:r['claim_type']='direct source reading / author statement; interpretation qualified in limitation'
        rows.append(r)
assert len({r['source_id'] for r in rows})==len(rows)
(ROOT/'sources.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
counts={'active_ledger_rows':len(rows),'unique_counted_originals':len(seen),'core_unique_originals_without_second_hop':core,'additional_counted_second_hop_originals':len(seen)-core,'source_kinds':dict(bykind),'counted_originals':[{'source_id':r['source_id'],'url':r['original_url'],'kind':r['source_kind'],'locator':r['locator']} for r in rows if r['counted']],'active_ledgers':[n for _,n in ACTIVE],'excluded_archives':'*-v1/v2, original repeated captures and previous scope ledgers are not concatenated as active readings.'}
(ROOT/'evidence/source-count-audit.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in counts.items() if k not in ['counted_originals','active_ledgers']},ensure_ascii=False))
