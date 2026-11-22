from pathlib import Path
import json,urllib.request,urllib.error,hashlib,concurrent.futures,re
from datetime import datetime,timezone
from lxml import html
P=Path(__file__).resolve().parents[1]/'collectors/python/followup';(P/'cache').mkdir(exist_ok=True)
refs=[json.loads(x) for x in (P.parents[2]/'references.jsonl').read_text().splitlines()]
old=next(x['raw_href'] for x in refs if x['reference_id']=='A-D02')
jobs=[('P-U01','http://docutils.sourceforge.net/rst.html','reStructuredText|powerful|markup|readable'),('P-U02',old,'read.only|migrat|GitHub|Search|issue'),('P-U03','https://github.com/python/cpython/issues?q=is%3Aissue+is%3Aopen+label%3Adocs','docs|Issues|Open'),('P-U04','https://discuss.python.org/t/github-issues-migration-status-update/14573.json','read-only|officially completed'),('P-U05','https://discuss.python.org/t/github-issues-are-now-live/14967.json','no longer|read-only'),('P-U06','https://discuss.python.org/t/status-of-documentation-bug-tracker/14957.json','locked|documentation|updated'),('P-F01','https://www.python.org/doc/versions/','3.8.14|3.8.15'),('P-F02','https://www.python.org/downloads/release/python-3815/','Release date|source.only|documentation')]
def run(x):
 sid,u,pattern=x;steps=[]
 class Handler(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,req,fp,code,msg,headers,newurl):
   steps.append({'status':code,'from':req.full_url,'to':newurl});return super().redirect_request(req,fp,code,msg,headers,newurl)
 out={'source_id':sid,'url':u,'observed_at_utc':datetime.now(timezone.utc).isoformat(),'redirects':steps}
 try:
  r=urllib.request.build_opener(Handler).open(u,timeout=30);b=r.read();out.update(status=r.status,final_url=r.url,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b));(P/'cache'/f'{sid}.raw').write_bytes(b)
  if u.endswith('.json'):
   j=json.loads(b);posts=j['post_stream']['posts'];out['posts']=[{'post_number':p['post_number'],'created_at':p['created_at'],'updated_at':p['updated_at'],'username':p['username'],'body_text':html.fromstring(p['cooked']).text_content(),'raw_hrefs':html.fromstring(p['cooked']).xpath('//a/@href')} for p in posts if p['post_number']<=3]
  else:
   d=html.fromstring(b);out['title']=d.xpath('//title/text()');out['paragraphs']=[' '.join(el.text_content().split()) for el in d.xpath('//p|//li|//h1|//h2') if re.search(pattern,el.text_content(),re.I)][:25]
 except Exception as e:
  out['error']=repr(e);out['status']=getattr(e,'code',None)
 return out
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(run,jobs));(P/'primary-observations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(rows,ensure_ascii=False,indent=2))
