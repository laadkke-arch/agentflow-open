"""Canonicalize sealed research ledgers. No external requests or judgment changes."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import json
import subprocess
import retrieval

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]

def rows(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]

def write(path,data):
    path.write_text(''.join(json.dumps(d,ensure_ascii=False,sort_keys=True)+'\n' for d in data))

def digest(path):return sha256(path.read_bytes()).hexdigest()

def corpus():
    data=rows(ROOT/'donor/corpus_draft.jsonl')
    assert len(data)==18 and len({d['candidate_id'] for d in data})==18
    out=[]
    for source in sorted(data,key=lambda x:x['candidate_id']):
        d=dict(source)
        d['field']={'transit':'transport','public_transport':'transport','libraries':'library','stats':'statistics'}.get(d['field'],d['field'])
        p=Path(d['cache_text_path'])
        p=p if p.is_absolute() else REPO/p
        p=p.resolve()
        assert p.is_relative_to(ROOT),p
        raw=p.read_bytes();text=raw.decode('utf-8')
        expected=d.get('body_sha256',d.get('text_sha256'))
        assert expected==sha256(raw).hexdigest(),(d['candidate_id'],'cached body differs from selected hash')
        d['features']=retrieval.features(text)
        d['source_text_sha256']=d['features']['source_text_sha256']
        d['body_republication']='Full body is local analysis cache only unless separately licensed; exact score replay uses committed frequency vectors and offsets.'
        out.append(d)
    assert Counter(d['field'] for d in out)=={'library':6,'transport':6,'statistics':6}
    assert len({d['source_id'] for d in out})==18
    write(ROOT/'corpus.jsonl',out)
    receipt={'stage':'provider_corpus_frozen_before_recipient_body_go','created_utc':datetime.now(timezone.utc).isoformat(),
             'git_head_before_seal':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
             'corpus_file_sha256':digest(ROOT/'corpus.jsonl'),'documents':len(out),'fields':dict(Counter(d['field'] for d in out)),
             'documents_and_text_hashes':[{k:d[k] for k in ['candidate_id','source_id','url','source_text_sha256']} for d in out],
             'score_replay_available_without_cache':True,'semantic_body_reverification_requires_original_version_or_local_cache':True}
    (ROOT/'evidence/corpus-seal.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'corpus_rows':len(out),'sha256':receipt['corpus_file_sha256'],'windows':sum(len(d['features']['windows']) for d in out)},ensure_ascii=False))

def inputs():
    data=rows(ROOT/'recipient/inputs_draft.jsonl')
    assert len(data)==8 and len({d['recipient_id'] for d in data})==8
    assert Counter(d['repository'] for d in data)=={'rust-lang/rfcs':4,'kubernetes/enhancements':4}
    out=[]
    for d in sorted(data,key=lambda x:x['recipient_id']):
        d=dict(d)
        for route in ['s','r']:
            q=d['query_'+route]
            assert q and len(retrieval.raw_tokens(q))<=80
            computed=sha256(q.encode()).hexdigest()
            old=d.get('query_'+route+'_sha256')
            assert old is None or old==computed
            d['query_'+route+'_sha256']=computed
            d['query_'+route+'_token_count']=len(retrieval.raw_tokens(q))
        out.append(d)
    write(ROOT/'inputs.jsonl',out)
    receipt={'stage':'recipient_inputs_queries_frozen','created_utc':datetime.now(timezone.utc).isoformat(),
             'git_head_before_seal':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
             'inputs_file_sha256':digest(ROOT/'inputs.jsonl'),'recipients':8,
             'queries':[{'recipient_id':d['recipient_id'],'S':d['query_s_sha256'],'R':d['query_r_sha256']} for d in out]}
    (ROOT/'evidence/input-seal.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'input_rows':len(out),'sha256':receipt['inputs_file_sha256']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--corpus',action='store_true');p.add_argument('--inputs',action='store_true');a=p.parse_args()
    if a.corpus:corpus()
    if a.inputs:inputs()
