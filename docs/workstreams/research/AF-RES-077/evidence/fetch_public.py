"""Bounded public-source retrieval. Records bytes, UTC, redirect and content hash.
Only called with preselected public source URLs; no credentials or account access.
"""
import argparse, datetime, hashlib, json, pathlib, urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out=[]; self.hidden=0; self.anchors=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in ('script','style'): self.hidden += 1
        if tag in ('p','div','section','h1','h2','h3','h4','h5','li','pre','br'): self.out.append('\n')
        if a.get('id'): self.anchors.append(a['id'])
    def handle_endtag(self,tag):
        if tag in ('script','style') and self.hidden: self.hidden-=1
        if tag in ('p','div','section','h1','h2','h3','h4','h5','li','pre'): self.out.append('\n')
    def handle_data(self,data):
        if not self.hidden:self.out.append(data)

def fetch(url, key):
    directory=ROOT/'reading'; directory.mkdir(exist_ok=True)
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    row={'id':key,'url':url,'utc':now,'actor':'root','operation':'open_public_original'}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-077 public-source research'})
        with urllib.request.urlopen(req,timeout=30) as r:
            raw=r.read(); row.update(status=r.status,landed_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        body=raw.decode('utf-8')
        if '<html' in body[:2000].lower() or '<!doctype html' in body[:2000].lower():
            parser=Text();parser.feed(body)
            body='\n'.join(x.strip() for x in ''.join(parser.out).splitlines() if x.strip())
            row['anchors']=parser.anchors
        (directory/(key+'.txt')).write_text(body)
        row['text_path']='reading/'+key+'.txt';row['text_characters']=len(body)
    except Exception as e:
        row.update(status='failed',error=str(e))
    with (directory/'receipts.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return row

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('key');p.add_argument('url');a=p.parse_args()
    print(json.dumps(fetch(a.url,a.key),ensure_ascii=False))
