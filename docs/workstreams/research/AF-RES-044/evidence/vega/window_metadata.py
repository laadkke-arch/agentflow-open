"""Reproduce section-window metadata; no third-party full text is retained in outputs."""
import pathlib,json,csv,re,urllib.parse,hashlib
from lxml import html
P=pathlib.Path(__file__).parent
rows=[r for r in csv.DictReader((P/'pool-V.csv').open()) if r['url']]
receipts={r['url']:r for r in json.loads((P/'candidate-fetch-receipts.json').read_text())}
def collect(elements,doc,word_limit=None):
 words=[];links=[]
 def walk(e):
  if not isinstance(e.tag,str):return
  begin=len(words)
  if e.text:words.extend(e.text.split())
  for child in e:
   walk(child)
   if child.tail:words.extend(child.tail.split())
  end=len(words)
  if e.tag=='a' and e.get('href') and (word_limit is None or end<=word_limit):
   links.append({'raw_href':e.get('href'),'url':urllib.parse.urljoin(doc,e.get('href')),'label':' '.join(e.itertext()).strip(),'word_begin':begin,'word_end':end})
 for e in elements:walk(e)
 if word_limit is not None:words=words[:word_limit]
 return ' '.join(words),links
results=[]
for r in rows:
 doc,frag=urllib.parse.urldefrag(r['url']);rec=receipts[doc];root=html.fromstring((P/rec['local_temporary_filename']).read_bytes());main=root.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," page-content ")]')[0]
 for e in main.xpath('.//script|.//style|.//*[@class="edit-page"]|.//form'):e.drop_tree()
 children=list(main);h1=main.xpath('./h1')[0];after=children[children.index(h1)+1:]
 full,wholelinks=collect(after,doc)
 if frag:
  matches=main.xpath('.//*[@id=$id]',id=frag); exists=bool(matches);selected=[]
  if exists:
   start=matches[0];level=int(start.tag[1]) if re.fullmatch('h[1-6]',start.tag) else 6;e=start
   while e is not None:
    if e is not start and isinstance(e.tag,str) and re.fullmatch('h[1-6]',e.tag) and int(e.tag[1])<=level:break
    if isinstance(e.tag,str):selected.append(e)
    e=e.getnext()
  strict,links=collect(selected,doc);locator=f'#{frag}: actual h{level} to next heading of same/higher level' if exists else 'missing fragment'
 else:
  exists=True;strict,links=collect(after,doc,800);locator='first 800 whitespace tokens after h1, excluding h1, edit controls/scripts/style/form'
 results.append({'candidate_id':r['candidate_id'],'case_id':r['case_id'],'requested_url':r['url'],'final_document_url':rec['final_url'],'http_status':rec['http_status'],'html_sha256':rec['sha256'],'checked_utc':rec['checked_utc'],'fragment_exists':exists,'strict_locator':locator,'strict_word_count':len(strict.split()),'strict_text_sha256':hashlib.sha256(strict.encode()).hexdigest(),'strict_outgoing_hrefs':links,'full_document_word_count':len(full.split()),'full_document_text_sha256':hashlib.sha256(full.encode()).hexdigest(),'full_document_outgoing_hrefs':wholelinks,'actual_user_response':'미확인'})
(P/'windows-V.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('windows:',len(results),'; all fragment resolved:',all(r['fragment_exists'] for r in results))
for r in results:print(r['candidate_id'],r['strict_word_count'],'outgoing',len(r['strict_outgoing_hrefs']))
