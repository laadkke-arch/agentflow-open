#!/usr/bin/env python3
"""Read public Apache Confluence revisions; print text without persisting article bodies."""
import argparse, datetime, hashlib, html, json, re, urllib.request
from html.parser import HTMLParser
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag in ['p','h1','h2','h3','h4','li','tr','td','br','pre']: self.parts.append('\n')
        if tag == 'a':
            a=dict(attrs)
            if 'href' in a: self.links.append(a['href'])
    def handle_data(self, value): self.parts.append(value)
def fetch(page_id, version):
    u=f'https://cwiki.apache.org/confluence/rest/api/content/{page_id}?expand=body.storage,history,version'
    if version: u+=f'&status=historical&version={version}'
    with urllib.request.urlopen(u, timeout=30) as r: data=r.read()
    j=json.loads(data); t=Text(); t.feed(j.get('body',{}).get('storage',{}).get('value',''))
    return {'url':u,'id':j.get('id'),'title':j.get('title'),'version':j.get('version'),'created':j.get('history',{}).get('createdDate'),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(data).hexdigest(),'text':re.sub(r'\n[ \t]*\n+', '\n\n', ''.join(t.parts)),'links':t.links}
if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('page_id'); a.add_argument('--version',type=int); args=a.parse_args()
    print(json.dumps(fetch(args.page_id,args.version),ensure_ascii=False,indent=2))
