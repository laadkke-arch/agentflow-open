from pathlib import Path
from datetime import datetime,timezone
import json,urllib.request,hashlib,concurrent.futures
from lxml import html
P=Path(__file__).resolve().parents[1]/'collectors/b';(P/'cache').mkdir(parents=True,exist_ok=True)
events=[
('B01','2020-01-24','Yarn','yarn-classic-docs-2020','https://yarnpkg.com/blog/release/2.0','https://yarnpkg.com/','https://classic.yarnpkg.com/','Future Plans: old website→classic, next→main, expected by Feb1. This is a plan, not an observed switch timestamp.'),
('B02','2020-07-02','GitHub','github-docs-unification-2020','https://github.blog/engineering/engineering-principles/how-we-launched-docs-github-com/','https://developer.github.com/','https://docs.github.com/','Product docs unified; /v3→/rest/reference mapping, blanket redirects still future in this post. Site move and all redirect activation are different clocks.'),
('B03','2020-11-04','curl / Daniel Stenberg','curl-domain-2020','https://daniel.haxx.se/blog/2020/11/04/the-journey-to-a-curl-domain/','https://curl.haxx.se/','https://curl.se/','Starting November4 new official home. Old domain remains; automatic redirects not yet enabled. Domain migration does not establish a failure event.'),
('B04','2020-11-11','Google Search Central','google-help-consolidation-2020','https://developers.google.com/search/blog/2020/11/goodbye-google-webmasters','https://support.google.com/webmasters','https://developers.google.com/search','Search Console usage help stays, crawling/indexing/Search guidance moves to Search Central over next few days. Old/new root URIs are actual article hrefs; not every old article is transferred.'),
('B05','2022-06-17','IETF / Robert Sparks','ietf-tools-final-transition-2022','https://www.ietf.org/blog/finalizing-ietf-tools-transition/','https://tools.ietf.org/','https://datatracker.ietf.org/','Final transition upcoming over weeks, links to plan; RFC-Editor canonical sentence added2026-10-29 must not be treated as2022 evidence. May overlap A-D04 only if same consumer+RFC4180 purpose.'),
('B06','2022-06-21','HashiCorp / Geoffrey Grosenbach','hashicorp-developer-beta-2022','https://www.hashicorp.com/en/blog/new-hashicorp-developer-site-is-now-in-public-beta','https://learn.hashicorp.com/','https://developer.hashicorp.com/','Public beta mirror of Vault/Waypoint content available today. Existing learn/product sites and new mirror coexist; this is not evidence of blanket old-link failure.')]
def read(t):
    rid,date,pub,key,url,old,new,note=t;at=datetime.now(timezone.utc).isoformat();d={'reference_id':rid,'sample':'B','announcement_date':date,'date_precision':'day; timezone unprovided','publisher':pub,'event_key':key,'announcement_url':url,'old_uri':old,'new_uri':new,'event_scope':note,'queries_limit':3,'candidate_documents_limit':5,'consumer_search_started':False,'source_ids':[f'B-U{rid[1:]}'],'selected_order':int(rid[1:]),'A_duplicate_status':'pending exact consumer-purpose-event join','prior_exposure_note':'Provisional excluded CRAN curl4.3.1 new URI was read before B event selection; it will not be used as B consumer. No old→new consumer success chain was known.' if rid=='B03' else ('Incidental gh changelog search snippet appeared in official event discovery; not opened, not a proved published manual pair.' if rid=='B02' else None)}
    try:
        r=urllib.request.urlopen(url,timeout=35);b=r.read();(P/'cache'/f'{rid}.html').write_bytes(b);doc=html.fromstring(b)
        d.update(observed_at_utc=at,status=r.status,sha256=hashlib.sha256(b).hexdigest(),final_url=r.url,body_text_evidence=' '.join(doc.text_content().split()))
        # Preserve target-domain links as a compact primary-source extraction.
        d['relevant_notice_hrefs']=[a.get('href') for a in doc.xpath('//a[@href]') if any(k in a.get('href') for k in ['yarnpkg','developer.github.com','help.github.com','docs.github.com','curl.se','curl.haxx','support.google.com/webmasters','developers.google.com/search','tools.ietf.org','datatracker.ietf.org','hashicorp.com','vaultproject.io'])]
    except Exception as e:
        if rid=='B03':
            d.update(observed_at_utc=at,status=None,sha256=None,final_url=url,body_text_evidence='Directly opened and read via web search-service; shell GET returned503. See event_scope for observed content; no raw response byte hash available.',shell_error=repr(e),read_method='search-service direct open; independent shell failed')
        else:d.update(observed_at_utc=at,error=repr(e))
    return d
rows=list(concurrent.futures.ThreadPoolExecutor(4).map(read,events))
assert all('error' not in r for r in rows),[(r['reference_id'],r.get('error')) for r in rows]
for r in rows:
    text=r.pop('body_text_evidence');(P/'cache'/f"{r['reference_id']}.txt").write_text(text)
    r['sealed_at_utc']=datetime.now(timezone.utc).isoformat()
(P/'b-sealed.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
sources=[]
for r in rows:
    sources.append({'source_id':r['source_ids'][0],'kind':'official_migration_announcement','publisher':r['publisher'],'original_url':r['announcement_url'],'version':r['announcement_date'],'publication_date':r['announcement_date'],'observed_at_utc':r['observed_at_utc'],'read_location':{'B01':'Future Plans / legacy codebase','B02':'Scripting the content migration; Redirecting all the things','B03':'curl.se is the new home','B04':'Centralizing help information to one site; Consolidating blogs','B05':'Final transition paragraphs;2026 update note','B06':'Introducing new Developer Site; mirror public beta'}[r['reference_id']],'findings':r['event_scope'],'limits':'Announcement day is not automatically exact effective time, consumer publication, or reader access. First-public date of current editable rendering is not independently established.','questions':['Q3','Q5','Q6'],'reference_ids':[r['reference_id']],'duplicate_group':r['event_key']+'-notice','count_minimum':True,'count_category':'upstream','sha256':r['sha256']})
(P/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
receipt={'sealed_at_utc':datetime.now(timezone.utc).isoformat(),'selection_window':'2020-01-01/2024-12-31','selection':'six earliest qualified directly read official migration notices in the documented search pool; chronological date then publisher/URL','consumer_query_limit':3,'consumer_document_limit':5,'selection_condition':'not chosen for known consumer correction; success0 acceptable','known_prior_exposures':{r['reference_id']:r['prior_exposure_note'] for r in rows if r['prior_exposure_note']},'sha256':hashlib.sha256((P/'b-sealed.jsonl').read_bytes()).hexdigest(),'events':6,'pending_remote_gate':True,'unselected_candidates':['Microsoft Learn2022-09-17 later than sixth eligible notice','OpenSSL2024 no dated original migration notice obtained','RedHat2024 no dated original migration notice obtained','Rust site migration search result was older historical release text,2020–24 eligibility not established','Netlify2024 site customer-domain move not documentation publishing event','packaging2022 proposal without completed URI change evidence']}
(P/'seal-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
