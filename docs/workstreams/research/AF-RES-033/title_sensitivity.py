"""Predeclared T02-title sensitivity. Keeps all original retrieval files intact."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import subprocess
import retrieval

ROOT=Path(__file__).resolve().parent

def main():
    original=retrieval.jsonlines(ROOT/'corpus.jsonl')
    inputs=retrieval.jsonlines(ROOT/'inputs.jsonl')
    corpus=deepcopy(original)
    target=next(d for d in corpus if d['candidate_id']=='T02')
    body=Path(target['cache_text_path']).read_text()
    assert retrieval.digest(body)==target['features']['source_text_sha256']
    alternate=body.split('\n',1)[1]
    assert retrieval.digest(alternate)=='72dfab28a68a892641bf7c84d85cd09900b1e6a459f2754931b8ae62e23d7afe'
    target['features']=retrieval.features(alternate)
    rows,runs,config=retrieval.rank(corpus,inputs)
    for row in rows:
        offset=1 if row['candidate_id']=='T02' else 0
        row['original_source_window_line_start']=row['window_line_start']+offset
        row['original_source_window_line_end']=row['window_line_end']+offset
    path=ROOT/'sensitivities';path.mkdir(exist_ok=True)
    retrieval.write_csv(path/'T02-title-excluded-rankings.csv',rows)
    orig=list(csv.DictReader((ROOT/'rankings.csv').open()))
    changes=[]
    for q in inputs:
        for route in ['S','R']:
            a=[r for r in orig if r['recipient_id']==q['recipient_id'] and r['route']==route]
            b=[r for r in rows if r['recipient_id']==q['recipient_id'] and r['route']==route]
            at=[r for r in a if r['returned_top3']=='True'];bt=[r for r in b if r['returned_top3']]
            changes.append({'recipient_id':q['recipient_id'],'route':route,
                'original_top3':[r['candidate_id'] for r in at],'title_excluded_top3':[r['candidate_id'] for r in bt],
                'top1_changed':at[0]['candidate_id']!=bt[0]['candidate_id'],
                'top3_set_changed':set(r['candidate_id'] for r in at)!=set(r['candidate_id'] for r in bt),
                'rank_order_changed':[r['candidate_id'] for r in a]!=[r['candidate_id'] for r in b],
                'original_returned_windows':[(r['candidate_id'],r['returned_window_id'],r['window_sha256']) for r in at],
                'title_excluded_returned_windows':[(r['candidate_id'],r['returned_window_id'],r['window_sha256']) for r in bt]})
    receipt={'checked_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'run_utc':datetime.now(timezone.utc).isoformat(),'predeclared_commit':'35a01fdaf359329253f7c73d721b857130e46d10',
        'original_corpus_sha256':retrieval.digest((ROOT/'corpus.jsonl').read_bytes()),
        'original_rankings_sha256':retrieval.digest((ROOT/'rankings.csv').read_bytes()),
        'inputs_sha256':retrieval.digest((ROOT/'inputs.jsonl').read_bytes()),
        'T02_alternate_body_sha256':retrieval.digest(alternate),
        'alteration':'Only T02 document title first line removed; features, IDF and window boundaries recomputed',
        'additional_searches':16,'not_part_of_original_16':True,'runs':runs,'changes':changes,
        'top1_changed':sum(x['top1_changed'] for x in changes),'top3_set_changed':sum(x['top3_set_changed'] for x in changes),
        'rank_order_changed':sum(x['rank_order_changed'] for x in changes),
        'T02_alternate_features':target['features']}
    (path/'T02-title-excluded-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['additional_searches','top1_changed','top3_set_changed','rank_order_changed']}))

if __name__=='__main__':main()
