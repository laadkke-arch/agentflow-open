"""Check actual frozen queries against source bytes and opening-event provenance.

No ranking is performed. The printed result omits query text so a semantic judge
can remain query/rank-blind while verifying the measurement inputs.
"""
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import retrieval

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]


def rows(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    inputs=rows(ROOT/'inputs.jsonl')
    targets={d['recipient_id']:d for d in rows(ROOT/'recipient/recipient_targets.jsonl')}
    assert len(inputs)==8 and {d['recipient_id'] for d in inputs}==set(targets)
    assert Counter(d['repository'] for d in inputs)=={'rust-lang/rfcs':4,'kubernetes/enhancements':4}
    assert Counter(d['target_scope'] for d in inputs)=={'whole_design':3,'partial_design':5}
    with (ROOT/'recipient/recipient_frame.csv').open() as f:
        frame={(r['repository'],int(r['pr_number'])):r for r in csv.DictReader(f)}
    archives={}
    for name in ['opening-archive-checks.jsonl','archive-recovery-checks.jsonl']:
        for d in rows(ROOT/'evidence'/name):
            if d['archive_complete'] and d['matching_event_count']==1:
                key=(d['repository'],int(d['pr_number']))
                m=d['matches'][0]
                assert m['action']=='opened' and m['pull_request_created_at']==frame[key]['created_at']
                archives[key]=m['head_sha']
    phrases=['seattle public library','denver public library','multnomah','toronto public library',
             'hennepin','vancouver public library','interlibrary loan','inter library loan',
             'king county metro','mbta','ttc','translink','trimet','sfmta',
             'office for national statistics','statistics canada','australian bureau of statistics',
             'bureau of labor statistics','bureau of economic analysis','stats nz',
             'release practice policy','release practices policy','error correction policy']
    checks=[]; failures=[]
    for d in inputs:
        rid=d['recipient_id']; key=(d['repository'],int(d['pr_number']))
        o=d['original_source']; path=Path(d['snapshot_path'])
        path=path if path.is_absolute() else REPO/path
        path=path.resolve(); assert path.is_relative_to(ROOT)
        raw=path.read_bytes(); body=raw.decode('utf-8')
        actual_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        c={'recipient_id':rid,'repository':key[0],'pr_number':key[1],
           'source_raw_sha256_matches':sha(raw)==o['raw_sha256'],
           'source_lf_sha256_matches':sha(raw.replace(b'\r\n',b'\n'))==o['canonical_lf_sha256'],
           'git_blob_sha_matches':actual_blob==o['git_blob_sha'],
           'opening_head_matches_archive':archives.get(key)==o['snapshot_commit_sha'],
           'fixed_target_unchanged':d['frozen_partial_target']==targets[rid]['frozen_partial_target'],
           'created_at_matches_frame':d.get('created_at')==frame[key]['created_at'],
           'immutable_url_binds_head_and_path':o['snapshot_commit_sha']+'/'+o['repository_path'] in o['immutable_url'],
           'target_predicate_ids':[p['id'] for p in d['frozen_partial_target']['mandatory_predicates']]}
        source_terms=set(retrieval.raw_tokens(body))
        for route in ['s','r']:
            q=d['query_'+route]; raw_terms=retrieval.raw_tokens(q)
            hits=[p for p in phrases if re.search(r'\b'+re.escape(p)+r'\b',q.lower())]
            qc={'raw_tokens':len(raw_terms),'effective_unique_terms':len(set(retrieval.tokens(q))),
                'nonempty':bool(raw_terms),'within_80_token_cap':len(raw_terms)<=80,
                'sha256_matches':sha(q.encode())==d['query_'+route+'_sha256'],
                'provider_specific_phrase_flags':hits}
            if route=='s':
                qc['tokens_absent_from_initial_markdown']=sorted(set(raw_terms)-source_terms)
            c[route.upper()]=qc
            if not qc['nonempty'] or not qc['within_80_token_cap'] or not qc['sha256_matches'] or hits:
                failures.append([rid,route,'query_check'])
            if route=='s' and qc['tokens_absent_from_initial_markdown']:
                failures.append([rid,route,'lexical_source_check_requires_review'])
        for k,v in c.items():
            if isinstance(v,bool) and not v:failures.append([rid,k])
        checks.append(c)
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),
            'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
            'inputs_sha256':sha((ROOT/'inputs.jsonl').read_bytes()),
            'targets_sha256':sha((ROOT/'recipient/recipient_targets.jsonl').read_bytes()),
            'documents':8,'query_pairs':8,'queries':16,'checks':checks,'failures':failures,
            'status':'passed' if not failures else 'needs_review',
            'limits':['Phrase screening is not proof of no conceptual leakage; source-only author context and read history are separate evidence.',
                      'S vocabulary check is lexical, not a semantic fidelity judgment. R fidelity requires source-grounded author review.',
                      'An opening-event head proves the submitted snapshot, not the earliest privately authored draft.']}
    (ROOT/'evidence/input-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'recipients':8,'queries':16,'failures':failures,
                      'raw_token_counts':{c['recipient_id']:{r:c[r]['raw_tokens'] for r in ['S','R']} for c in checks}},ensure_ascii=False))
    if failures:raise SystemExit(1)


if __name__=='__main__':main()
