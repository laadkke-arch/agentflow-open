import urllib.request,urllib.parse,json,hashlib,datetime,time,re,pathlib
P=pathlib.Path(__file__).parent
LOG=P/'search-log.jsonl'
def fetch(url,role):
    at=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'AF-RES-063 public source audit','Accept':'application/vnd.github+json'})
        with urllib.request.urlopen(req,timeout=30) as r: raw=r.read(); status=r.status; final=r.url
        data=json.loads(raw)
        record={'opened_utc':at,'role':role,'url':url,'final_url':final,'status':status,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    except Exception as e:
        record={'opened_utc':at,'role':role,'url':url,'status':'failed','error':str(e)}
        with LOG.open('a') as f:f.write(json.dumps(record)+'\n')
        raise
    with LOG.open('a') as f:f.write(json.dumps(record)+'\n')
    return data,record

def search(q,page=1):
    url='https://api.github.com/search/issues?'+urllib.parse.urlencode({'q':q,'sort':'created','order':'asc','per_page':100,'page':page})
    return fetch(url,'title-only search; body not displayed or used')
def title(x):
    return {k:x.get(k) for k in ['number','title','created_at','updated_at','html_url','state']}|{'author':x['user']['login'],'is_pr':'pull_request' in x}
if __name__=='__main__':
    base='repo:moment/moment-timezone is:issue created:2021-01-01..2025-12-31'
    keywords={};errors=[]
    for word in ['timezone','"time zone"','tzdata','DST','offset','daylight']:
        try:
            d,r=search(base+' '+word+' in:title')
            keywords[word]={'total_count':d.get('total_count'),'incomplete':d.get('incomplete_results'),'items':[title(x) for x in d['items']],'receipt':r}
        except Exception as e:errors.append({'keyword':word,'error':str(e)})
    (P/'keyword-title-lists.json').write_text(json.dumps({'queries':keywords,'errors':errors},ensure_ascii=False,indent=2)+'\n')
    allrows=[]
    d,r=search(base)
    allrows.extend([title(x) for x in d['items']])
    total=d.get('total_count')
    for page in range(2,min(10,(total+99)//100)+1):
        d,r=search(base,page);allrows.extend([title(x) for x in d['items']])
    pat=re.compile(r'timezone|time[\s_-]+zone|tzdata|\bDST\b|offset|daylight',re.I)
    matches=sorted([x for x in allrows if not x['is_pr'] and pat.search(x['title'])],key=lambda x:(x['created_at'],x['number']))
    union={x['number'] for q in keywords.values() for x in q['items']}
    fixed={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_total':total,'scanned_title_count':len(allrows),'matched_title_count':len(matches),'all_title_census':allrows,'first30':matches[:30],'missing_from_keyword_queries':[x for x in matches[:30] if x['number'] not in union],'query_deviation':'Keyword-less full five-year census used in one search under 1000 results, no monthly split required; includes all title rows and does not read bodies.'}
    (P/'title-frame-seal.json').write_text(json.dumps(fixed,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in fixed.items() if k!='all_title_census'},ensure_ascii=False,indent=2))
