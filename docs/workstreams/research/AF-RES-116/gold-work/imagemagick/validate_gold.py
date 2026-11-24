"""Check exact corpus offsets, source hashes, provenance links and quota accounting."""
from pathlib import Path
from datetime import datetime, timezone
import json, gzip, hashlib, collections, re
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
def run():
    docs={d['id']:d for d in json.loads(gzip.decompress((ROOT/'corpus.json.gz').read_bytes()))['documents']}
    gold=json.loads((BASE/'gold.json').read_text())
    sources=[json.loads(x) for x in (BASE/'sources-imagemagick.jsonl').read_text().splitlines()]
    intervals=json.loads((BASE/'minimal-intervals.json').read_text())
    targets=json.loads((BASE/'target-spans.json').read_text())
    identifiers={s['source_id'] for s in sources}
    assert len(identifiers)==len(sources)
    checks={}
    for s in intervals:
        d=docs[s['doc_id']]
        assert s['small_quote'] in d['text'][s['start']:s['end']]
        assert s['source_sha256']==d['source_sha']
        assert hashlib.sha256((ROOT/d['source_file']).read_bytes()).hexdigest()==d['source_sha']
    checks['corpus_intervals_exact']=len(intervals)
    for case in gold['cases']:
        assert case['original_request_source_id'] in identifiers
        for r in case['outside_corpus_requirements']:
            assert all(s in identifiers for s in r['source_ids']),r
        for s in case['minimal_supporting_intervals']:
            assert s in intervals
    checks['gold_case_references_valid']=len(gold['cases'])
    for case in targets['cases']:
        for t in case['related_operation_targets']:
            d=docs[t['doc_id']]
            assert d['text'][t['start']:t['end']]==t['body_text']
            assert t['end']>t['start']
            assert t['source_sha256']==d['source_sha']
        assert all(s in identifiers for s in case['decisive_answer_target']['source_ids'])
    checks['target_spans_exact']=len(targets['cases'])
    for s in sources:
        p=BASE/s['snapshot_path']
        if not p.exists():p=ROOT/s['snapshot_path']
        assert p.exists(),s['snapshot_path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==s['source_sha256'],s['source_id']
        assert s['read_utc'] and s['checked_utc']
    checks['source_rows_hash_and_read_utc_valid']=len(sources)
    counts=collections.Counter(s['allocation'] for s in sources if s['unique_counted'])
    assert counts=={'definition':4,'regression':3}
    checks['allocation']=dict(counts)
    expected={c['case_id']:c for c in json.loads((ROOT/'cases.json').read_text())['cases'] if c['case_id'] in ['I1','I2','I3']}
    for c in gold['cases']:
        assert c['original_body_sha256']==expected[c['case_id']]['original_body_sha256']
    checks['original_body_hashes_match_sealed_cases']=3
    leaks=[]
    for p in BASE.rglob('*'):
        if p.is_file() and p.suffix in ['.json','.jsonl','.md','.txt','.html','.py']:
            text=p.read_text(errors='replace')
            if re.search(r'X-Amz-(?:Signature|Credential)=|[?&](?:sig|jwt|token)=',text,re.I):
                leaks.append(str(p.relative_to(BASE)))
    assert not leaks,leaks
    checks['saved_signing_query_values']=0
    checks['unavailable_i3_recovered_success']=False
    checks['historical_target_runtime_executed']=False
    report={'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'exit_code':0,'earlier_validation_finding':'First integrity pass detected two public screenshot signing queries in discussion-7848 HTML. Removed queries; receipt and ledger now distinguish fetched and stored SHA. The substantive text is unchanged. Recheck passed.','scope':'JSON/offset/source/receipt consistency and observed-input provenance only. Not fixed-viewer reachability, historical runtime, original author adoption or recipient results.'}
    (BASE/'validation-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
