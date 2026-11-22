"""Deterministic text + link positions, preserves source lines and raw href."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib,json,sys

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=''; self.links=[]; self.link=None; self.ignore=0; self.title=''; self.intitle=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('script','style','nav'): self.ignore+=1
        if self.ignore: return
        if tag=='title':self.intitle=True
        if tag in ('p','div','br','h1','h2','h3','h4','li','dt','dd','pre','tr'):self.text+='\n'
        if tag=='a' and 'href' in d:
            self.link={'href':d['href'],'start':len(self.text),'source_line':self.getpos()[0]}
    def handle_endtag(self,tag):
        if tag in ('script','style','nav') and self.ignore: self.ignore-=1;return
        if self.ignore:return
        if tag=='title': self.intitle=False
        if tag=='a' and self.link:
            self.link.update(end=len(self.text),link_text=self.text[self.link['start']:])
            self.links.append(self.link);self.link=None
        if tag in ('p','div','h1','h2','h3','h4','li','dt','dd','pre','tr'):self.text+='\n'
    def handle_data(self,data):
        if self.ignore:return
        self.text+=data
        if self.intitle:self.title+=data

def parse(path):
    path=Path(path); raw=path.read_bytes();d=Document();d.feed(raw.decode('utf-8',errors='replace'))
    return {'member_path':str(path),'member_sha256':hashlib.sha256(raw).hexdigest(),
            'title':d.title,'text':d.text,'links':d.links,'normalization':'HTMLParser convert_charrefs, omit script/style/nav, newline block markers; utf8 replacement decode'}

if __name__=='__main__':
    result=parse(sys.argv[1]);target=Path(sys.argv[2]);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('text','links')},ensure_ascii=False))
    for link in result['links']:
        if link['href'].startswith(('http://','https://','ftp://')):
            print(json.dumps({**link,'context':result['text'][max(0,link['start']-250):link['end']+500]},ensure_ascii=False))
