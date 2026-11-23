"""Render the frozen editing windows; no retrieval or holdout input is read."""
import json, os, re, subprocess, hashlib
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlparse

ROOT=Path(__file__).resolve().parent
ALLOW={'features','feature','supported features','functionality','capabilities','operations','api','api reference','public api'}
BLOCK={'p','div','section','article','main','ul','ol','li','pre','table','tr','td','th','h1','h2','h3','h4','h5','h6','br','hr','blockquote','dt','dd'}
TRACK={'a','li','code','h1','h2','h3','h4','h5','h6'}
class Visible(HTMLParser):
 def __init__(self): super().__init__();self.parts=[];self.visible_pos=0;self.stack=[];self.items=[];self.hide=0
 def add(self,t): self.parts.append(t);self.visible_pos+=len(t)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in {'script','style','nav','footer'}:self.hide+=1
  if self.hide:return
  if t in BLOCK:self.add('\n')
  if a.get('id'):self.items.append({'tag':'anchor','start':self.visible_pos,'end':self.visible_pos,'attrs':a})
  if t in TRACK:self.stack.append((t,self.visible_pos,a))
 def handle_endtag(self,t):
  if t in {'script','style','nav','footer'}:self.hide=max(0,self.hide-1);return
  if self.hide:return
  if t in TRACK:
   for i in range(len(self.stack)-1,-1,-1):
    k,s,a=self.stack[i]
    if k==t:self.items.append({'tag':t,'start':s,'end':self.visible_pos,'attrs':a});self.stack.pop(i);break
  if t in BLOCK:self.add('\n')
 def handle_data(self,t):
  if not self.hide:self.add(t)

def rendered(f):
 text=f.read_text()
 if f.suffix in {'.md','.markdown'}:
  cmd=[os.environ.get('CODEX_PRIMARY_RUNTIME_NODE','node'),'-e',"const fs=require('fs');const m=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/marked');process.stdout.write(m.parse(fs.readFileSync(0,'utf8')));"]
  return subprocess.check_output(cmd,input=text,text=True)
 if f.suffix=='.rst':return subprocess.check_output(['pandoc','-f','rst','-t','html'],input=text,text=True)
 if f.suffix=='.adoc':
  # Deterministic conversion of observed README.adoc constructs before marked.
  text=re.sub(r'^image::?.*$', '', text, flags=re.M)
  text=re.sub(r'^(?:\[source[^\]]*\]|\+)\s*$', '', text, flags=re.M)
  text=re.sub(r'^----\s*$', '```', text, flags=re.M)
  text=re.sub(r'^(=+)\s+', lambda m:'#'*len(m[1])+' ', text, flags=re.M)
  text=re.sub(r'(https?://[^\s\[]+)\[([^]]+)\]',lambda m:'['+re.sub(r'\s+',' ',m[2])+']('+m[1]+')',text,flags=re.S)
  text=re.sub(r'link:([^\s\[]+)\[([^]]+)\]',r'[\2](\1)',text)
  cmd=[os.environ.get('CODEX_PRIMARY_RUNTIME_NODE','node'),'-e',"const fs=require('fs');const m=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/marked');process.stdout.write(m.parse(fs.readFileSync(0,'utf8')));"]
  return subprocess.check_output(cmd,input=text,text=True)
 return text

def make(d):
 f=ROOT/'_raw'/f"{d['id']}.{d['path'].split('.')[-1]}"
 h=rendered(f);p=Visible();p.feed(h);s=''.join(p.parts)
 headings=sorted((x for x in p.items if x['tag'].startswith('h')),key=lambda x:x['start'])
 def norm(t):return re.sub(r'^\s*[\d.]+\s*','',t.strip().rstrip(':').casefold())
 section=next((x for x in headings if norm(s[x['start']:x['end']]) in ALLOW),None)
 first=section or (headings[0] if headings else None)
 start=first['start'] if first else 0
 fragment=urlparse(d['url']).fragment
 if d['id'].endswith('-D2') and fragment:
  anchor=next((x for x in p.items if x['attrs'].get('id')==fragment),None)
  if anchor:
   containing=next((x for x in headings if x['start']<=anchor['start']<=x['end']),None)
   first=containing or first;start=containing['start'] if containing else anchor['start'];section=None
 words=list(re.finditer(r'\S+',s[start:]));n=min(500,len(words));end=start+words[n-1].end() if n else start
 win=s[start:end].strip();items=[]
 for x in sorted(p.items,key=lambda x:(x['start'],x['end'])):
  if start<=x['start']<end:
   items.append({**x,'text':s[x['start']:min(x['end'],end)].strip(),'clipped':x['end']>end})
 links=[{'text':x['text'],'href':urljoin(d['url'],x['attrs']['href'])} for x in items if x['tag']=='a' and 'href' in x['attrs']]
 # Only explicit API/Features labels/paths. The first qualifying link is immutable.
 nxt=next((x for x in links if re.search(r'\b(api|features)\b',x['text'],re.I) or re.search(r'[/#](api|features)([/#?.-]|$)',x['href'],re.I)),None) if not section else None
 r={'id':d['id'],'source_url':d['url'],'retrieved_utc':d['at'],'source_blob':d.get('blob'),'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'format':f.suffix,'renderer':'marked HTML + HTMLParser; RST=pandoc; AsciiDoc documented minimal title/paragraph/link/list mapping','first_heading':s[first['start']:first['end']] if first else None,'feature_section_found':bool(section),'word_count':n,'word_limit':500,'rendered_text_sha256':hashlib.sha256(win.encode()).hexdigest(),'character_range':[start,end],'links':links,'followup':nxt,'structures':items,'rendered_text':win}
 (ROOT/'windows').mkdir(exist_ok=True)
 (ROOT/'windows'/f"{d['id']}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'windows'/f"{d['id']}.txt").write_text(win+'\n')
 return {k:v for k,v in r.items() if k not in {'rendered_text','structures'}}

if __name__=='__main__':
 ds=json.loads((ROOT/'metadata/final-documents.json').read_text());summary=[]
 for d in sorted(ds,key=lambda x:x['id']):
  if d.get('blob') or d.get('path'):summary.append(make(d))
 (ROOT/'metadata/window-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([{'id':x['id'],'heading':x['first_heading'],'words':x['word_count'],'followup':x['followup']} for x in summary],ensure_ascii=False,indent=2))
