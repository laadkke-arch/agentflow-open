"""Post-seal2 source reading, isolated from primary packet access and judgments."""
from pathlib import Path
import argparse, datetime, hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('file_id')
    ap.add_argument('--start',type=int);ap.add_argument('--end',type=int)
    ap.add_argument('--find');ap.add_argument('--context',type=int,default=250);ap.add_argument('--limit',type=int,default=5)
    a=ap.parse_args(); rows=[json.loads(s) for s in (ROOT/'corpus-files.jsonl').read_text().splitlines()]
    r=next(r for r in rows if r['file_id']==a.file_id)
    raw=(ROOT/r['cached_body']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256'];t=raw.decode('utf-8')
    if a.find:
        spans=[(max(0,m.start()-a.context),min(len(t),m.end()+a.context)) for m in list(re.finditer(a.find,t,re.I))[:a.limit]]
    else:
        start=0 if a.start is None else a.start;end=min(len(t),start+1200) if a.end is None else a.end;spans=[(start,end)]
    merged=[]
    for start,end in sorted(spans):
        assert 0<=start<=end<=len(t)
        if merged and start<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],end)
        else:merged.append([start,end])
    assert sum(b-a for a,b in merged)<=12000,'narrow display to avoid truncation'
    parts=[]
    for start,end in merged:
        bs,be=len(t[:start].encode()),len(t[:end].encode())
        parts.append({'char_start':start,'char_end':end,'byte_start':bs,'byte_end':be,
                      'line_start':t.count('\n',0,start)+1,'line_end':t.count('\n',0,max(start,end-1))+1,
                      'sha256':hashlib.sha256(raw[bs:be]).hexdigest(),'displayed_chars':end-start})
    ev={'file_id':r['file_id'],'url':r['url'],'version':r['version'],'sha256':r['sha256'],
        'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'segments':parts,
        'phase':'post-seal2 supplementary source audit','primary_judgment_contribution':False,
        'search_pattern':a.find,'matched_count_shown':len(spans),'source_bytes':len(raw)}
    log=ROOT/'evidence/resume2/postseal-access.jsonl'
    with log.open('a') as f:f.write(json.dumps(ev,ensure_ascii=False)+'\n')
    print(json.dumps(ev,ensure_ascii=False))
    for part in parts:
        print('CHARS',part['char_start'],part['char_end'],'LINES',part['line_start'],part['line_end'])
        print(t[part['char_start']:part['char_end']])

if __name__=='__main__':main()
