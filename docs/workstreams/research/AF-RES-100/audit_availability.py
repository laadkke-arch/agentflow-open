"""Separate pre-outcome evidence audit, never an initial-reader access.

This may re-read a registered snippet to check a claim, but cannot broaden its
packet boundary. Its logs and costs are separate from the four reader accesses.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, re
import fcntl

ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('packet_id');ap.add_argument('slot',type=int)
    ap.add_argument('--start',type=int);ap.add_argument('--end',type=int);ap.add_argument('--find')
    ap.add_argument('--context',type=int,default=300);ap.add_argument('--limit',type=int,default=8)
    a=ap.parse_args();ps=[json.loads(l) for l in (ROOT/'packets.jsonl').read_text().splitlines()]
    p=next(p for p in ps if p['packet_id']==a.packet_id);s=next(s for s in p['slots'] if s['slot']==a.slot)
    if s['empty']:raise ValueError('empty research slot: no substitute source permitted')
    raw=(ROOT/s['cached_body']).read_bytes();assert hashlib.sha256(raw).hexdigest()==s['sha256'];t=raw.decode()
    lo,hi=s['char_start'],s['char_end']
    if a.find:
        if p['mode']!='F':raise ValueError('restricted snippets are audited by reading exact complete snippet')
        ms=list(re.finditer(a.find,t[lo:hi],re.I))[:a.limit]
        xs=[(max(lo,lo+m.start()-a.context),min(hi,lo+m.end()+a.context)) for m in ms]
    else:
        start=lo if a.start is None else a.start
        end=(hi if p['mode']=='S' else min(hi,start+1200)) if a.end is None else a.end
        xs=[(start,end)]
    merged=[]
    for start,end in sorted(xs):
        assert lo<=start<=end<=hi
        if merged and start<=merged[-1][1]:merged[-1][1]=max(end,merged[-1][1])
        else:merged.append([start,end])
    if sum(b-a for a,b in merged)>14000:raise ValueError('narrow audit display to <=14000 chars to avoid output truncation')
    segs=[]
    for start,end in merged:
        bs,be=len(t[:start].encode()),len(t[:end].encode())
        segs.append({'char_start':start,'char_end':end,'byte_start':bs,'byte_end':be,
                     'line_start':t.count('\n',0,start)+1,'line_end':t.count('\n',0,max(start,end-1))+1,
                     'displayed_chars':end-start,'sha256':hashlib.sha256(raw[bs:be]).hexdigest()})
    ev={'packet_id':p['packet_id'],'slot':a.slot,'file_id':s['file_id'],'url':s['url'],
        'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'separate evidence availability audit',
        'initial_reader_discovery':False,'source_sha256':s['sha256'],'segments':segs,
        'displayed_chars':sum(x['displayed_chars'] for x in segs)}
    log=ROOT/'evidence/audit/availability-access.jsonl';log.parent.mkdir(exist_ok=True,parents=True)
    with log.open('a') as f:
        fcntl.flock(f.fileno(),fcntl.LOCK_EX);f.write(json.dumps(ev,ensure_ascii=False)+'\n');f.flush();fcntl.flock(f.fileno(),fcntl.LOCK_UN)
    print(json.dumps(ev,ensure_ascii=False,indent=2))
    for v in segs:
        print('SOURCE CHARS',v['char_start'],v['char_end'],'BYTES',v['byte_start'],v['byte_end'])
        print(t[v['char_start']:v['char_end']])

if __name__=='__main__':main()
