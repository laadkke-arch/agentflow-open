"""Read fixed corpus sections after seal2, separately from packet budgets.

These displays cannot revise the remotely sealed pre-outcome judgments.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, re

ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('file_id');ap.add_argument('--find')
    ap.add_argument('--start',type=int,default=0);ap.add_argument('--end',type=int)
    ap.add_argument('--context',type=int,default=280);ap.add_argument('--limit',type=int,default=4)
    a=ap.parse_args()
    rows=[json.loads(x) for x in (ROOT/'corpus-files.jsonl').read_text().splitlines()]
    d=next(x for x in rows if x['file_id']==a.file_id)
    raw=(ROOT/d['cached_body']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['sha256'];text=raw.decode()
    if a.find:
        hits=list(re.finditer(a.find,text,re.I))
        ranges=[(max(0,m.start()-a.context),min(len(text),m.end()+a.context)) for m in hits[:a.limit]]
    else:
        hits=[];ranges=[(a.start,min(len(text),a.end if a.end is not None else a.start+1200))]
    merged=[]
    for start,end in ranges:
        assert 0<=start<=end<=len(text)
        if merged and start<=merged[-1][1]:merged[-1][1]=max(end,merged[-1][1])
        else:merged.append([start,end])
    assert sum(b-a for a,b in merged)<=14000, 'narrow display'
    segments=[]
    for start,end in merged:
        ba,bb=len(text[:start].encode()),len(text[:end].encode())
        segments.append({'char_start':start,'char_end':end,'byte_start':ba,'byte_end':bb,
                         'line_start':text.count('\n',0,start)+1,'line_end':text.count('\n',0,max(start,end-1))+1,
                         'sha256':hashlib.sha256(raw[ba:bb]).hexdigest()})
    event={'file_id':a.file_id,'url':d['url'],'archive_url':d['archive_url'],
           'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'phase':'post-seal2 supplemental/displacement reading',
           'seal2_commit':'5d81bcbeb5f1248fc1dd2ce2d825cf6467353673',
           'body_sha256':d['sha256'],'query':a.find,'total_matches':len(hits) if a.find else None,
           'segments':segments,'read_chars':sum(b-a for a,b in merged),'initial_evidence':False}
    target=ROOT/'evidence/supplemental/reads.jsonl';target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
    print(json.dumps(event,ensure_ascii=False))
    for s in segments:
        print(f"LINES {s['line_start']}..{s['line_end']} CHARS {s['char_start']}..{s['char_end']} BYTES {s['byte_start']}..{s['byte_end']}")
        print(text[s['char_start']:s['char_end']])

if __name__=='__main__':main()
