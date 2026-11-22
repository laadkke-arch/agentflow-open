"""Read public HTML; persist link/position metadata, never a full source copy."""
import json, sys, urllib.request, urllib.parse, hashlib
from html.parser import HTMLParser
from datetime import datetime, timezone
from pathlib import Path

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.links=[]; self.current=None; self.parts=[]; self.h1=False
    def handle_starttag(self, tag, attrs):
        attr=dict(attrs)
        if tag not in {'meta','link','img','input','br','hr','source','wbr'}: self.stack.append((tag,attr))
        if tag=='h1': self.h1=True
        if tag=='a':
            self.current={'raw_href':attr.get('href',''),'label':'','html_line':self.getpos()[0], 'body':any(t=='article' for t,a in self.stack) or (any(t=='main' for t,a in self.stack) and not any(t in ('nav','aside') for t,a in self.stack)), 'after_h1':self.h1, 'text_index':len(self.parts)}
    def handle_endtag(self,tag):
        if tag=='a' and self.current:self.links.append(self.current);self.current=None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):
        self.parts.append(data)
        if self.current:self.current['label']+=data

def fetch(url):
    with urllib.request.urlopen(url,timeout=25) as r: raw=r.read();resolved=r.url;code=r.status
    p=Parser();p.feed(raw.decode('utf-8','replace'))
    for x in p.links:
        x['label']=' '.join(x['label'].split());x['resolved_href']=urllib.parse.urljoin(resolved,x['raw_href'])
    return {'requested_url':url,'resolved_url':resolved,'status':code,'checked_utc':datetime.now(timezone.utc).isoformat(),'html_sha256':hashlib.sha256(raw).hexdigest(),'links':[x for x in p.links if x['body'] and x['after_h1']]}

if __name__=='__main__':
    name,url=sys.argv[1:3];base=Path(__file__).parent/'raw-web';base.mkdir(parents=True,exist_ok=True)
    try:
        result=fetch(url);(base/(name+'.links.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        for i,x in enumerate(result['links'],1):
            if x['raw_href'].startswith(('http:','https:')):print(i,x)
        print('META',name,result['status'],result['checked_utc'],result['html_sha256'])
    except Exception as e:
        result={'requested_url':url,'checked_utc':datetime.now(timezone.utc).isoformat(),'error':type(e).__name__+': '+str(e)};(base/(name+'.failure.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result)
