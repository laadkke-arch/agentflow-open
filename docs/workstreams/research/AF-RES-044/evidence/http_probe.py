"""Read-only study helper; no execution of downloaded content. Owned AF-RES-044."""
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urldefrag,unquote,urljoin
import hashlib,datetime,re
class Node:
 def __init__(self,tag,attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[];self.start=0;self.end=0
 def walk(self):
  yield self
  for x in self.children:
   if isinstance(x,Node):yield from x.walk()
 def text(self):
  if self.tag in ('script','style','svg'):return ''
  return ' '.join(x.text() if isinstance(x,Node) else x for x in self.children)
class DOM(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.root=Node('document');self.stack=[self.root];self.nodes=[self.root];self.a_count=0
 def handle_starttag(self,t,a):
  n=Node(t,a,self.stack[-1]);n.start=len(self.nodes);self.nodes.append(n);self.stack[-1].children.append(n)
  if t=='a' and 'href' in n.attrs:self.a_count+=1;n.attrs['_dom_index']=self.a_count
  if t not in ('meta','link','img','input','br','hr','area','base','col','embed','param','source','track','wbr'):self.stack.append(n)
  else:n.end=len(self.nodes)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:
    for n in self.stack[i:]:n.end=len(self.nodes)
    self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
 def finish(self):
  for n in self.stack:n.end=len(self.nodes)
 def main(self):
  for sel in (lambda n:n.tag=='main',lambda n:n.tag=='article',lambda n:n.attrs.get('role')=='main',lambda n:n.tag=='body'):
   found=next((n for n in self.nodes if sel(n)),None)
   if found:return found
  return self.root
 def links(self,scope=None):
  return [dict(raw_href=n.attrs['href'],dom_index=n.attrs['_dom_index'],label=' '.join(n.text().split())) for n in (scope or self.root).walk() if n.tag=='a' and 'href' in n.attrs]
 def window(self,url):
  frag=unquote(urldefrag(url)[1]); main=self.main(); result={'fragment':frag,'main_tag':main.tag,'main_attrs':main.attrs,'fragment_found':None}
  if frag:
   target=next((n for n in self.nodes if n.attrs.get('id')==frag or n.attrs.get('name')==frag),None)
   if not target:return dict(result,fragment_found=False,scope_locator='missing fragment',text='',links=[])
   result['fragment_found']=True
   # An actual target section element includes its child headings/paragraphs; a dt uses its own dd; other target uses the nearest section.
   if target.tag=='section':scope=target
   elif target.tag in ('dt','dd'):
    scope=target
    while scope.parent and scope.tag!='section':scope=scope.parent
   else:
    scope=target
    while scope.parent and scope.tag not in ('section','article','main','body') and scope.parent!=self.root:scope=scope.parent
   text=' '.join(scope.text().split());links=self.links(scope)
   if scope.tag in ('main','article','body') and target.tag in ('h1','h2','h3','h4','h5','h6'):
    level=int(target.tag[1]);end=next((n.start for n in self.nodes if n.start>target.start and n.tag in ('h1','h2','h3','h4','h5','h6') and int(n.tag[1])<=level),scope.end)
    chunks=[];links=[]
    # Read direct top-level siblings until the next equal-or-higher heading.
    siblings=target.parent.children;go=False
    for n in siblings:
     if n is target:go=True
     if go and isinstance(n,Node):
      if n.start>=end:break
      chunks.append(n.text());links.extend(self.links(n))
    text=' '.join(' '.join(chunks).split())
   return dict(result,scope_locator=scope.tag+'#'+str(scope.attrs.get('id',frag)),text=text,links=links)
  hs=next((n for n in main.walk() if n.tag=='h1'),None)
  if hs:
   # Strip everything before first h1 within chosen content surface.
   full=main.text();title=hs.text();pos=full.find(title);full=full[pos+len(title):] if pos>=0 else full
  else:full=main.text()
  words=[]; positions={}
  def collect(n):
   begin=len(words)
   if n.tag not in ('script','style','svg'):
    for x in n.children:
     if isinstance(x,Node):collect(x)
     else:words.extend(x.split())
   positions[id(n)]=(begin,len(words))
  collect(main)
  start=positions[id(hs)][1] if hs else 0
  text=' '.join(words[start:start+800]); links=[]
  for n in main.walk():
   if n.tag=='a' and 'href' in n.attrs:
    b,e=positions[id(n)]
    if start<=b<start+800 and e<=start+800:links.append(dict(raw_href=n.attrs['href'],dom_index=n.attrs['_dom_index'],label=' '.join(n.text().split()),word_begin=b-start,word_end=e-start))
  return dict(result,scope_locator='first 800 words after first h1 in '+main.tag,text=text,links=links)
def fetch(url):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();out={'requested_url':url,'checked_utc':now}
 try:
  with urlopen(urldefrag(url)[0],timeout=25) as r:raw=r.read();out.update(status=r.status,final_document_url=r.geturl(),content_type=r.headers.get('content-type'))
  out['sha256']=hashlib.sha256(raw).hexdigest();dom=DOM();dom.feed(raw.decode('utf-8',errors='replace'));dom.finish();out['window']=dom.window(url);out['all_links']=dom.links();out['full_text']=' '.join(dom.main().text().split());return out
 except Exception as e:return dict(out,status='failed',error=type(e).__name__+': '+str(e),window={'text':'','links':[],'fragment_found':False})
