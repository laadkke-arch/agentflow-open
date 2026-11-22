"""Independent, read-only HTTP/DOM navigation trials for fixed three-card views.

Each trial creates a new opener and empty cookie jar. It never imports evidence
from another trial. Same-document fragment navigation uses that trial's loaded
DOM, just as a page-local click does. No downloaded code is executed.
"""
from pathlib import Path
import json,hashlib,datetime,concurrent.futures,sys,threading
from urllib.request import build_opener,HTTPCookieProcessor
from urllib.error import HTTPError
from http.cookiejar import CookieJar
from urllib.parse import urldefrag,unquote,urljoin,urlparse
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence'
def readj(p):return json.loads((ROOT/p).read_text())
def readjl(p):return [json.loads(x) for x in (ROOT/p).read_text().splitlines()]
class Anchors(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if a.get('name'):self.ids.add(a['name'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])

def plan():
    outgoing={}
    for name in ['evidence/vega/second-hop-targets.json','evidence/pandoc/control-second-hop-targets.json','evidence/crossfield/control-second-hop-targets.json']:
        d=readj(name)
        for target in d['targets']:
            for occ in target['source_occurrences']:
                outgoing.setdefault(occ['candidate_id'],[]).append(dict(occ,url=target['url'],target_ledger=name))
    trials=[]
    def add(v,kind,card,steps,**kw):
        trials.append(dict(trial_id=f"{v['view_id']}-T{sum(t['view_id']==v['view_id'] for t in trials)+1:04d}",view_id=v['view_id'],case_id=v['case_id'],method=v['method'],kind=kind,start_card=card['slot'],start_candidate=card['candidate_id'],fresh_start=True,budget=2,steps=steps,actual_user_response='미확인',**kw))
    for v in readjl('views.jsonl'):
        cards=[c for c in v['cards'] if c['url']]
        for c in cards:
            add(v,'direct',c,[{'action':'open_representative','url':c['url'],'candidate_id':c['candidate_id'],'cost':1}])
            add(v,'siblings_only',c,[{'action':'open_sibling_list','url':None,'members':c['members'],'cost':1}])
            add(v,'representative_then_siblings',c,[{'action':'open_representative','url':c['url'],'candidate_id':c['candidate_id'],'cost':1},{'action':'open_sibling_list','url':None,'members':c['members'],'cost':1}])
            for mid,url in zip(c['members'],c['member_urls']):
                add(v,'sibling_member',c,[{'action':'open_sibling_list','url':None,'members':c['members'],'cost':1},{'action':'open_member','url':url,'candidate_id':mid,'cost':1}])
            for d in cards:
                if d is c:continue
                add(v,'two_representatives',c,[{'action':'open_representative','url':c['url'],'candidate_id':c['candidate_id'],'cost':1},{'action':'open_other_representative','url':d['url'],'candidate_id':d['candidate_id'],'cost':1}])
            for occ in outgoing.get(c['candidate_id'],[]):
                add(v,'actual_outgoing_href',c,[{'action':'open_representative','url':c['url'],'candidate_id':c['candidate_id'],'cost':1},{'action':'follow_actual_href','url':occ['url'],'raw_href':occ['raw_href'],'cost':1}],source_occurrence=occ)
    (E/'trial-plan.jsonl').write_text(''.join(json.dumps(t,ensure_ascii=False)+'\n' for t in trials))
    print(json.dumps({'trials':len(trials),'views_with_paths':len(set(t['view_id'] for t in trials)),'candidate_outgoing_occurrences':sum(map(len,outgoing.values()))}))
    return trials

def trial_run(t):
    result=dict(t,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),instrument='fresh HTTP opener / DOM fragment navigation, no script execution',arrivals=[],cost_used=0,completed=True)
    opener=build_opener(HTTPCookieProcessor(CookieJar()));loaded={};previous=None
    for step in t['steps']:
        result['cost_used']+=step['cost'];u=step['url']
        if not u:
            result['arrivals'].append({'action':step['action'],'source':'fixed serialized view','member_ids':step['members'],'success':True,'source_evidence_count':0});continue
        base,frag=urldefrag(u);entry={'action':step['action'],'requested_url':u,'candidate_id':step.get('candidate_id'),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        if step['action']=='follow_actual_href':
            entry['raw_href_exists_in_source']=bool(previous and step['raw_href'] in previous['links'])
            if not entry['raw_href_exists_in_source']:
                entry.update(success=False,reason='Frozen actual href absent in this trial source response; do not invent transition.');result['arrivals'].append(entry);result['completed']=False;break
        if not base.startswith(('http://','https://')):
            entry.update(success=False,reason='non-HTTP transition not executed');result['arrivals'].append(entry);result['completed']=False;break
        try:
            if base in loaded:
                doc=loaded[base];entry['transport']='same-document fragment navigation in this trial'
            else:
                with opener.open(base,timeout=18) as res:
                    raw=res.read();status=res.status;dest=res.geturl();typ=res.headers.get('content-type','')
                parser=Anchors();parser.feed(raw.decode('utf-8',errors='replace'))
                doc={'status':status,'final_document_url':dest,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'ids':parser.ids,'links':parser.links,'content_type':typ};loaded[base]=doc;entry['transport']='fresh HTTP GET'
            found=not frag or unquote(frag) in doc['ids']
            entry.update(http_status=doc['status'],final_document_url=doc['final_document_url'],html_sha256=doc['sha256'],response_bytes=doc['bytes'],fragment=frag,fragment_found=found,success=doc['status']==200 and found)
            if not found:entry['reason']='HTTP response loaded but the exact fragment is absent; unanchored fallback is not success.'
            previous=doc
        except Exception as ex:
            entry.update(http_status=getattr(ex,'code','미확인'),success=False,reason=type(ex).__name__+': '+str(ex));previous=None
        result['arrivals'].append(entry)
        if not entry['success']:
            result['completed']=False;break
    result['connectivity_success']=result['completed'];return result

def run():
    trials=readjl('evidence/trial-plan.jsonl');outfile=E/'trial-observations.jsonl'
    done=set()
    if outfile.exists():done={x['trial_id'] for x in readjl('evidence/trial-observations.jsonl')}
    pending=[t for t in trials if t['trial_id'] not in done]
    with outfile.open('a') as f, concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for i,result in enumerate(pool.map(trial_run,pending),1):
            f.write(json.dumps(result,ensure_ascii=False)+'\n');f.flush()
            if i%50==0:print(f'completed {len(done)+i}/{len(trials)} independent trials',flush=True)
    print('finished',len(trials),'trials',flush=True)

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='plan':plan()
    else:run()
