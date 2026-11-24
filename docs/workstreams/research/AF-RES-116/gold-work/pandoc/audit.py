"""Bounded public capture and actual display log for independent Pandoc gold reads."""
from pathlib import Path
from datetime import datetime, timezone
import urllib.request, urllib.parse, hashlib, json, gzip, time

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent

def now():
    return datetime.now(timezone.utc).isoformat()

def redact(url):
    if not url:
        return url
    p=urllib.parse.urlsplit(url)
    safe_api=(p.netloc=='api.github.com' and all(k in {'per_page','page','recursive','path','until','since','sha'} for k,_ in urllib.parse.parse_qsl(p.query)))
    return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,p.query if safe_api else ('[REDACTED_PUBLIC_ATTACHMENT_QUERY]' if p.query else ''),p.fragment))

def fetch(url,name,limit=5_000_000):
    out=ROOT/'snapshots'/name
    start=now();tic=time.monotonic()
    receipt={'original_url':redact(url),'started_utc':start,'output':str(out.relative_to(ROOT)),'status':None,'query_redaction':'Any URL query is redacted; public attachment transport metadata, not a credential publication.'}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-116-independent-gold-reader','Accept':'*/*'})
        with urllib.request.urlopen(req,timeout=45) as r:
            raw=r.read(limit+1)
            if len(raw)>limit:raise ValueError('bounded source exceeds limit')
            receipt.update(arrived_url=redact(r.url),status=r.status,content_type=r.headers.get('Content-Type'),last_modified=r.headers.get('Last-Modified'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        out.write_bytes(raw)
    except Exception as e:
        receipt.update(error_type=type(e).__name__,status=getattr(e,'code',None),arrived_url=redact(getattr(e,'url',None)))
        raw=None
    receipt.update(finished_utc=now(),wall_seconds=round(time.monotonic()-tic,6))
    out.with_name(out.name+'.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return raw,receipt

def display(source,sections,text,kind='documentary'):
    stamp=now()
    row={'display_utc':stamp,'source':source,'sections':sections,'kind':kind,'characters':len(text),'sha256':hashlib.sha256(text.encode()).hexdigest()}
    with (ROOT/'read-log.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    n=sum(1 for _ in (ROOT/'read-log.jsonl').open())
    (ROOT/'excerpts'/f'{n:03}.txt').write_text(text)
    print('ACTUAL_EXCERPT_DISPLAY_UTC',stamp,source,sections)
    print(text)

def corpus():
    return {d['id']:d for d in json.loads(gzip.decompress((BASE/'corpus.json.gz').read_bytes()))['documents'] if d['id'] in ['p2192','p383','p21403']}

def corpus_span(doc_id,start,end):
    d=corpus()[doc_id]
    display(doc_id,{'start':start,'end':end,'indexing':'Unicode code points, half-open'},d['text'][start:end])

def lines(name,start,end):
    s=(ROOT/'snapshots'/name).read_text().splitlines()
    display(name,{'line_start':start,'line_end_inclusive':end},'\n'.join(f'{i+1}: {s[i]}' for i in range(start-1,min(end,len(s)))))
