"""Read original Python offline HTML only; never dereference its external links."""
import pathlib, urllib.request, hashlib, tarfile, io, json, re
from datetime import datetime, timezone
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1]/'collectors'/'python'
ROOT.mkdir(parents=True,exist_ok=True)
CACHE=ROOT/'cache';CACHE.mkdir(exist_ok=True)
def now():return datetime.now(timezone.utc).isoformat()
def get(url,name):
    at=now()
    try:
        r=urllib.request.urlopen(url,timeout=45); b=r.read()
        rec={'url':url,'observed_at_utc':at,'status':r.status,'final_url':r.url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'headers':dict(r.headers)}
        (CACHE/name).write_bytes(b)
    except Exception as e:
        rec={'url':url,'observed_at_utc':at,'error':repr(e)};b=None
    with (ROOT/'access.jsonl').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
    return b,rec
class Text(HTMLParser):
    def __init__(self):super().__init__();self.out=[]
    def handle_data(self,d):self.out.append(d)
def plain(s):
    p=Text();p.feed(s);return re.sub(r'\s+',' ',' '.join(p.out)).strip()
def scan(b):
    s=b.decode('utf-8'); m=re.search(r'<div class="body"[^>]*>',s)
    if not m:return []
    s=s[m.end():];s=s.split('<div class="clearer">')[0]
    out=[]
    for a in re.finditer(r'<a\s[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',s,re.S):
        href=a.group(1);text=plain(a.group(2))
        # Keep candidates, including exclusion reasons, for human source reading.
        lo=s.rfind('<p',0,a.start());hi=s.find('</p>',a.end())
        context=plain(s[lo:hi+4]) if lo>=0 and hi>=0 else plain(s[max(0,a.start()-300):a.end()+300])
        out.append({'href':href,'link_text':text,'context':context,'html_fragment':s[lo:hi+4] if lo>=0 and hi>=0 else a.group(0)})
    return out
if __name__=='__main__':
    idx,idxrec=get('https://docs.python.org/ftp/python/doc/3.8.2/','index.html')
    release,relrec=get('https://www.python.org/downloads/release/python-382/','release.html')
    url='https://docs.python.org/ftp/python/doc/3.8.2/python-3.8.2-docs-html.tar.bz2'
    blob,rec=get(url,'python-3.8.2-docs-html.tar.bz2')
    if not blob:raise SystemExit('archive unavailable')
    t=tarfile.open(fileobj=io.BytesIO(blob)); candidates=[];frame=[]
    for mem in sorted(t.getmembers(),key=lambda m:m.name):
        if not mem.isfile() or not mem.name.endswith('.html'):continue
        b=t.extractfile(mem).read();links=scan(b)
        frame.append({'member':mem.name,'absolute_body_links':len(links)})
        if links:
            candidates.append({'member':mem.name,'member_sha256':hashlib.sha256(b).hexdigest(),'links':links,'archive':rec})
            (ROOT/(mem.name.split('/',1)[1].replace('/','__'))).write_bytes(b)
        if len(candidates)>=4:break
    (ROOT/'candidates.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2))
    (ROOT/'scan-frame.json').write_text(json.dumps(frame,ensure_ascii=False,indent=2))
    print(json.dumps([{'member':c['member'],'links':[{'href':x['href'],'text':x['link_text'],'context':x['context']} for x in c['links'][:6]]} for c in candidates],ensure_ascii=False,indent=2))
