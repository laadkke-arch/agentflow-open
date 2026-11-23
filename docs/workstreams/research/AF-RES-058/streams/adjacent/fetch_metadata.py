import urllib.request,urllib.parse,json,pathlib,datetime,time,hashlib
P=pathlib.Path(__file__).parent
qs=['explanation advice reliance decision','rationale classification human decision','evidence fact checking recommendation','explanation recommendation acceptance']
rows=[]
for i,q in enumerate(qs):
 params={'query.bibliographic':q,'filter':'from-pub-date:2015-01-01,until-pub-date:2025-12-31,type:proceedings-article','sort':'score','order':'desc','rows':100,'offset':0};url='https://api.crossref.org/works?'+urllib.parse.urlencode(params);t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 d={'query':q,'request_url':url,'utc':t,'sort':'score desc','pages':1,'rows':100,'rule':'R1','exposure':'metadata titles/abstracts; not result tables'}
 try:
  res=urllib.request.urlopen(url,timeout=35);raw=res.read();data=json.loads(raw);d.update(status=res.status,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));(P/'_cache'/f'score-{i}.json').write_bytes(raw)
  for rank,it in enumerate(data['message']['items'],1):
   rows.append({'query_id':'BCR'+str(i+1),'rank':rank,'doi':it.get('DOI'),'title':it.get('title'),'venue':it.get('container-title'),'event':it.get('event'),'published':it.get('published'),'published_online':it.get('published-online'),'published_print':it.get('published-print'),'url':it.get('URL'),'score':it.get('score')})
 except Exception as e:d['error']=str(e)
 with (P/'search-log.jsonl').open('a') as fp:fp.write(json.dumps(d,ensure_ascii=False)+'\n')
 print(json.dumps(d));time.sleep(.7)
(P/'crossref-score-metadata.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows:
 v=str(r['venue']).lower();title=str(r['title']).lower()
 if any(s in v for s in ['human factors','intelligent user','research and development in information retrieval','computational linguistics','empirical methods','north american chapter']):print(json.dumps(r,ensure_ascii=False))
