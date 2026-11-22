import urllib.request,json,pathlib,datetime,hashlib,sys
from html.parser import HTMLParser
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.links=[]; self.depth=0; self.anchor=None
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'): self.depth+=1
        if tag=='a':
            href=dict(attrs).get('href'); self.anchor={'href':href,'text':''} if href else None
        if tag in ('p','div','section','h1','h2','h3','li','tr','br'): self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'): self.depth=max(0,self.depth-1)
        if tag=='a' and self.anchor:
            self.links.append(self.anchor); self.anchor=None
        if tag in ('p','div','section','h1','h2','h3','li','tr'): self.parts.append('\n')
    def handle_data(self,data):
        if not self.depth:
            self.parts.append(data)
            if self.anchor: self.anchor['text']+=data
url,stem=sys.argv[1:3]
assert '/' not in stem and '..' not in stem
r={'requested_url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
p=pathlib.Path(__file__).parent/(stem+'.html')
try:
    with urllib.request.urlopen(url,timeout=20) as res:
        raw=res.read(); r.update(status=res.status,resolved_url=res.url,content_type=res.headers.get('Content-Type'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    p.write_bytes(raw)
    parser=Parser();parser.feed(raw.decode('utf-8','replace'))
    txt='\n'.join(s.strip() for s in ''.join(parser.parts).splitlines() if s.strip())
    p.with_suffix('.txt').write_text(txt)
    r.update(outcome='success',initial_text=txt[:13000],links=[{'index':i,'text':v['text'].strip(),'href':v['href']} for i,v in enumerate(parser.links[:65])])
except Exception as exc:
    r.update(outcome='access_failed',error=str(exc),error_type=type(exc).__name__)
print(json.dumps(r,ensure_ascii=False))
