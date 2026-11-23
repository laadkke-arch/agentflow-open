import sys,concurrent.futures,json,re
from html.parser import HTMLParser
from http_read import fetch,D
class Page(HTMLParser):
 def __init__(self): super().__init__();self.tags=[];self.chunks=[];self.title='';self.intitle=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));self.intitle=(tag=='title') or self.intitle
 def handle_endtag(self,tag):
  if tag=='title':self.intitle=False
 def handle_data(self,data):
  self.chunks.append(data)
  if self.intitle:self.title+=data

def one(j):
 key,url=j;txt,rec=fetch(url,key+'-html')
 if txt is None:return key,rec
 p=Page();p.feed(txt)
 scripts=re.findall(r'<script\b[^>]*>.*?</script>',txt,re.S|re.I)
 out={'retrieval':rec,'title':p.title,'canonical':[a['href'] for tag,a in p.tags if tag=='link' and a.get('rel')=='canonical'],'generator':[a.get('content') for tag,a in p.tags if tag=='meta' and a.get('name')=='generator'],'readthedocs_scripts':[s for s in scripts if 'readthedocs' in s.lower()],'version_markers':list(dict.fromkeys(re.findall(r'(?:Bandersnatch|bandersnatch|build|cibuildwheel)[^<\n]{0,60}(?:[0-9]+\.[0-9]+\.[0-9]+)',txt)))[:20],'page_ids':[a['id'] for tag,a in p.tags if 'id' in a],'internal_paths':[a['href'] for tag,a in p.tags if tag=='a' and 'href' in a and not a['href'].startswith(('http','mailto','javascript'))][:100],'version_context':[s.strip()[:200] for s in p.chunks if re.search(r'\b[0-9]+\.[0-9]+\.[0-9]+\b',s)][:20]}
 (D/(key+'-html-summary.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 return key,out
if __name__=='__main__':
 jobs=[('P1-latest','https://bandersnatch.readthedocs.io/en/latest/'),('P1-tag','https://bandersnatch.readthedocs.io/en/7.0.1/'),('P2-root','https://build.pypa.io/'),('P2-tag','https://build.pypa.io/en/1.3.0/'),('P3-stable','https://cibuildwheel.pypa.io/en/stable/'),('P3-tag','https://cibuildwheel.pypa.io/en/v3.3.0/'),('P3-legacy','https://cibuildwheel.pypa.io/en/1.x/')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
  for key,out in ex.map(one,jobs): print(key,json.dumps(out,ensure_ascii=False),flush=True)
