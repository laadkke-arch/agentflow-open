"""Verify the preserved alternate coding without changing the primary judgments."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
OWNED = ROOT.parents[1]
REPO = OWNED.parents[3]
BASE = 'caa2a814727dd485ed0eb9bb8530d6b16fab9584'


def read(path):
    return json.loads(path.read_text())


def normalize(x):
    return {'gold_ids':sorted(m['gold_id'] if isinstance(m,dict) else m for m in x['gold_matches']),
        'L':x['L'],'E':x['E'],'H':{h['constraint_id']:h['value'] for h in x['H']},
        'T':x['T'],'label':x['label'],'date_status':x['date_status'],
        'historical_ids':sorted(x['strict_historical_gold_ids']),
        'nongold_useful':x['nongold_useful'],'nongold_historical_useful':x['nongold_historical_useful'],
        'near_miss':x['near_miss'],'broken_or_fake':x['broken_or_fake']}


def main():
    manifest=read(ROOT/'SNAPSHOT.json')
    for f in manifest['files']:
        data=(ROOT/'snapshot'/f['path']).read_bytes()
        assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256'],f['path']
    ledger=read(ROOT/'snapshot/JUDGMENTS.json')
    full={}
    for shard in ledger['detail_shards']:
        data=(ROOT/'snapshot'/shard['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==shard['sha256']
        rows=json.loads(data)['judgments']; assert len(rows)==shard['judgment_count']
        full[shard['path']]=rows
    alternate=[]
    for row in ledger['judgments']:
        path,pointer=row['details'].split('#'); item=full[path][int(pointer.rsplit('/',1)[-1])]
        assert normalize(row)==normalize(item)
        alternate.append(item)
    primary=read(OWNED/'JUDGMENTS.json')['judgments']
    key=lambda x:(x['baseline'],x['case_id'],x['rank'])
    li={key(x):x for x in alternate}; ri={key(x):x for x in primary}
    assert set(li)==set(ri) and len(li)==342
    counts=Counter(); changed=0
    for k in li:
        l,r=normalize(li[k]),normalize(ri[k])
        fields=[field for field in l if l[field]!=r[field]]
        counts.update(fields); changed+=bool(fields)
    comparison=read(ROOT/'COMPARISON.json')
    assert dict(counts)==comparison['changed_fields'] and changed==comparison['changed_rows']
    runs=sorted((OWNED/'runs').glob('*/*.json')); assert len(runs)==62
    for f in runs:
        previous=subprocess.check_output(['git','show',BASE+':'+str(f.relative_to(REPO))],cwd=REPO)
        assert f.read_bytes()==previous
    source_ledger=read(ROOT/'snapshot/sources.json')
    rows=list(source_ledger['sources']); failures=list(source_ledger['excluded'])
    for shard in source_ledger['source_shards']:
        data=(ROOT/'snapshot'/shard['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==shard['sha256']
        d=json.loads(data); rows+=d['sources']; failures+=d['excluded']
    assert len(rows)==1335 and len(failures)==342
    needed={'id','url','accessed_at_utc','source_type','title','version_or_date','sections_read','confirmed','limits','level','used_in'}
    assert all(needed<=set(r) for r in rows)
    result={'snapshot_files':len(manifest['files']),'snapshot_bytes':sum(f['bytes'] for f in manifest['files']),
        'preserved_runs':len(runs),'paired_judgments':len(li),'changed_rows':changed,'changed_fields':dict(counts),
        'alternate_source_records':len(rows),'alternate_excluded_attempts':len(failures),
        'integrity':'passed','consensus_adjudication':'not_performed','strict_acceptance':'blocked_SITE_CAP_CASES'}
    (ROOT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':
    main()
