"""Frozen AF-RES-033 BM25 and returned-window replay; Python stdlib only.

Source bodies remain in local cache when republication permission is unknown.
The committed corpus exports frequencies and offsets, enough to replay scores.
No query tuning, model call, web search, stemming or embedding is performed.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import math
import re
import subprocess
import time
import unicodedata

ROOT = Path(__file__).resolve().parent
STOP = set('a an and are as at be been being but by can could did do does for from had has have if in into is it its may might not of on or our should so than that the their them then there these they this those to was we were what when where which who will with would you your'.split())
PATTERN = re.compile(r'[a-z0-9]+')
K1 = 1.2
B = .75
WINDOW = 200

def raw_tokens(text):
    return PATTERN.findall(unicodedata.normalize('NFC', text).lower())

def tokens(text):
    return [x for x in raw_tokens(text) if x not in STOP]

def digest(raw):
    return sha256(raw if isinstance(raw, bytes) else raw.encode('utf-8')).hexdigest()

def jsonlines(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]

def features(text):
    normalized = unicodedata.normalize('NFC', text)
    lower = normalized.lower()
    matches = list(PATTERN.finditer(lower))
    windows = []
    for k in range(0, len(matches), WINDOW):
        ms = matches[k:k+WINDOW]
        start, end = ms[0].start(), ms[-1].end()
        window_text = lower[start:end]
        ws = [m.group() for m in ms if m.group() not in STOP]
        windows.append({
            'window_id': f'W{len(windows)+1:03d}',
            'raw_token_start_1based': k+1,
            'raw_token_end_1based': k+len(ms),
            'coordinate_space': 'Unicode NFC source text, then Python str.lower()',
            'lowercase_normalized_char_start_0based': start,
            'lowercase_normalized_char_end_exclusive': end,
            'text_line_start_1based': 1+lower[:start].count('\n'),
            'text_line_end_1based': 1+lower[:end].count('\n'),
            'normalized_window_sha256': digest(window_text),
            'length': len(ws), 'term_frequency': dict(sorted(Counter(ws).items())),
        })
    ts = [m.group() for m in matches if m.group() not in STOP]
    return {'source_text_sha256':digest(text), 'normalized_text_sha256':digest(normalized),
            'lowercase_normalized_text_sha256':digest(lower),
            'raw_token_count':len(matches), 'length':len(ts),
            'term_frequency':dict(sorted(Counter(ts).items())), 'windows':windows}

def score(query_terms, tf, length, avg_length, idf):
    total = 0.0
    for term in sorted(query_terms):
        freq = tf.get(term, 0)
        if freq:
            total += idf.get(term, 0.0) * freq * (K1+1) / (freq + K1*(1-B+B*length/avg_length))
    return total

def rank(corpus, inputs):
    n = len(corpus)
    assert n == 18 and len({d['candidate_id'] for d in corpus}) == 18, 'Need 18 unique candidates'
    assert len({d['source_id'] for d in corpus}) == 18, 'Candidate documents must be unique'
    assert Counter(d['field'] for d in corpus) == {'library':6,'transport':6,'statistics':6}, 'Need six per donor field'
    assert len(inputs) == 8 and len({q['recipient_id'] for q in inputs}) == 8, 'Need eight unique recipients'
    assert Counter(q['repository'] for q in inputs) == {'rust-lang/rfcs':4,'kubernetes/enhancements':4}, 'Need four per recipient repository'
    df = Counter(term for d in corpus for term in d['features']['term_frequency'])
    idf = {t: math.log(1+(n-c+.5)/(c+.5)) for t,c in df.items()}
    avg_length = sum(d['features']['length'] for d in corpus)/n
    windows = [w for d in corpus for w in d['features']['windows']]
    avg_window = sum(w['length'] for w in windows)/len(windows)
    rows=[]; runs=[]
    for q in inputs:
        for route in ['S','R']:
            query = q['query_'+route.lower()]
            assert len(raw_tokens(query)) <= 80, (q['recipient_id'],route)
            terms = set(tokens(query))
            start = time.perf_counter_ns()
            scores=[]
            for d in corpus:
                f=d['features']
                s=score(terms,f['term_frequency'],f['length'],avg_length,idf)
                scores.append((d,s))
            scores.sort(key=lambda pair: (-pair[1],pair[0]['candidate_id']))
            positive_count=sum(s>0 for d,s in scores)
            for i,(d,s) in enumerate(scores,1):
                ws=[(w,score(terms,w['term_frequency'],w['length'],avg_window,idf)) for w in d['features']['windows']]
                ws.sort(key=lambda pair:(-pair[1],pair[0]['raw_token_start_1based']))
                w,ws_score=ws[0] if ws else ({},0.0)
                rows.append({
                    'recipient_id':q['recipient_id'],'route':route,'rank':i,
                    'candidate_id':d['candidate_id'],'source_id':d['source_id'],
                    'score':format(s,'.17g'),'positive_score':s>0,'returned_top1':i<=1 and s>0,'returned_top3':i<=3 and s>0,
                    'query_sha256':digest(query),'source_text_sha256':d['features']['source_text_sha256'],
                    'best_window_id':w.get('window_id',''),
                    'returned_window_id':w.get('window_id','') if i<=3 and s>0 else '',
                    'window_score':format(ws_score,'.17g'),
                    'window_raw_token_start':w.get('raw_token_start_1based',''),'window_raw_token_end':w.get('raw_token_end_1based',''),
                    'window_line_start':w.get('text_line_start_1based',''),'window_line_end':w.get('text_line_end_1based',''),
                    'window_sha256':w.get('normalized_window_sha256',''),
                    'source_url':d['url'],'source_location':d.get('read_location',d.get('section','')),
                    'matched_query_terms':';'.join(sorted(terms & set(d['features']['term_frequency']))),
                })
            runs.append({'recipient_id':q['recipient_id'],'route':route,'query_sha256':digest(query),
                'raw_query_tokens':len(raw_tokens(query)),'unique_query_tokens_after_stopwords':len(terms),
                'scored_documents':n,'positive_documents':positive_count,'returned_documents':min(3,positive_count),
                'empty_result':positive_count==0,'elapsed_ns':time.perf_counter_ns()-start})
    return rows,runs,{'document_count':n,'avg_document_length':avg_length,'avg_window_length':avg_window,'window_count':len(windows),
                     'k1':K1,'b':B,'stopwords':sorted(STOP),'idf':idf,'token_pattern':PATTERN.pattern,'window_raw_tokens':WINDOW}

def write_csv(path, rows):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true')
    args=p.parse_args()
    corpus=jsonlines(ROOT/'corpus.jsonl');inputs=jsonlines(ROOT/'inputs.jsonl')
    rows,runs,config=rank(corpus,inputs)
    if args.check:
        with (ROOT/'rankings.csv').open() as f: existing=list(csv.DictReader(f))
        as_strings=[{k:str(v) for k,v in r.items()} for r in rows]
        assert as_strings==existing,'rankings differ from exact replay'
        print(json.dumps({'status':'passed','replayed_rows':len(rows),'searches':len(runs),'empty_searches':sum(r['empty_result'] for r in runs)}))
    else:
        write_csv(ROOT/'rankings.csv',rows)
        checked_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        receipt={'checked_out_commit':checked_head,'run_utc':datetime.now(timezone.utc).isoformat(),
                 'corpus_sha256':digest((ROOT/'corpus.jsonl').read_bytes()),'inputs_sha256':digest((ROOT/'inputs.jsonl').read_bytes()),
                 'algorithm_sha256':digest(Path(__file__).read_bytes()),'rankings_sha256':digest((ROOT/'rankings.csv').read_bytes()),
                 'runs':runs,'config':config}
        (ROOT/'evidence').mkdir(exist_ok=True)
        (ROOT/'evidence/retrieval-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'written_rows':len(rows),'searches':len(runs),'empty_searches':sum(r['empty_result'] for r in runs)}))

if __name__=='__main__': main()
