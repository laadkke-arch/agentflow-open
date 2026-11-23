"""Read only ggplot2's old release and release-selection metadata.

Raw responses are an ephemeral cache; committed outputs retain receipts/excerpts.
This stage must not fetch 3.5.1 example bodies, assets, or deployment listings.
"""
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

OUT = Path(__file__).resolve().parent
CACHE = Path('/tmp/af098-ggplot2')
CACHE.mkdir(exist_ok=True)
OLD = '392175bbb00b04025aa5d17a0c18b3896adeb40f'
OLD_SOURCE = 'a6f1a7c845bfe056ef952b839d2fd65b888ab5cd'
REPO = 'https://api.github.com/repos/tidyverse/ggplot2'
RAW = 'https://raw.githubusercontent.com/tidyverse/ggplot2/'
receipts = []
sources = []
prior_receipts = {r['id']: r for r in json.loads((OUT/'stage1_receipts.json').read_text())} if (OUT/'stage1_receipts.json').exists() else {}

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({'from': req.full_url, 'status': code, 'to': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def get(sid, url, q='Q1', locator='', note='', category='release_record'):
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    h = Redirects()
    rec = {'id': sid, 'url': url, 'utc': started, 'redirects': h.chain}
    b = None
    try:
        cached = CACHE / (sid + '.bin')
        if cached.exists() and sid in prior_receipts and prior_receipts[sid]['url'] == url:
            b = cached.read_bytes()
            rec = prior_receipts[sid]
            started = rec['utc']
        else:
            with urllib.request.build_opener(h).open(url, timeout=45) as r:
                b = r.read()
                rec.update(status=r.status, final_url=r.url, mime=r.headers.get('Content-Type'),
                           bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
                (CACHE / (sid + '.bin')).write_bytes(b)
    except Exception as exc:
        rec.update(status=getattr(exc, 'code', None), error=f'{type(exc).__name__}: {exc}')
    receipts.append(rec)
    sources.append({'id': sid, 'q': [q], 'case_id': ['GG1','GG2'], 'url': url,
                    'fixed_url': url if OLD in url or OLD_SOURCE in url or '/tags/' in url else None,
                    'utc': started, 'publisher': 'tidyverse/ggplot2 maintainers',
                    'lineage': 'ggplot2 documentation', 'version': '3.5.0' if OLD in url or OLD_SOURCE in url else 'release metadata',
                    'locator': locator, 'observed': note, 'claim': '',
                    'limitations': 'Static public record; deployment message is not a signed build provenance statement.',
                    'counted': b is not None, 'dedup_basis': 'URL plus payload SHA within same work; failures excluded',
                    'category': category, 'sha256': rec.get('sha256'), 'bytes': rec.get('bytes'),
                    'receipt_id': sid})
    print(sid, rec.get('status'), rec.get('bytes'), flush=True)
    (OUT/'stage1_receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
    return b

def main():
    r = json.loads(get('GG-RELEASES', REPO+'/releases?per_page=100', locator='tag_name,published_at,prerelease'))
    released=[]
    for x in r:
        if '2022-' <= x['published_at'] < '2026-' and not x['prerelease']:
            released.append({k:x[k] for k in ['tag_name','published_at','html_url','target_commitish']})
    (OUT/'release-selection.json').write_text(json.dumps({'selection_basis':'GitHub release published_at, earliest stable x.y.0 in 2023–2025; first subsequent patch in same x.y series','releases':released,'old':'v3.5.0','new':'v3.5.1'},ensure_ascii=False,indent=2)+'\n')
    sources[-1]['observed']='v3.5.0: 2024-02-23T09:33:36Z; v3.5.1: 2024-04-23T10:21:20Z. v3.4.0 is 2022, 2023 releases are patches, v4.0.0 is later in 2025.'
    sources[-1]['claim']='Q1 selects 3.5.0 and 3.5.1 from public release dates.'
    dep = json.loads(get('GG-OLD-DEPLOYS', REPO+'/commits?sha=gh-pages&since=2024-02-22T00:00:00Z&until=2024-02-24T23:59:59Z&per_page=100', locator='commit.sha,committer.date,message'))
    dep=[{'sha':x['sha'],'date':x['commit']['committer']['date'],'message':x['commit']['message']} for x in dep]
    (OUT/'old-deploys.json').write_text(json.dumps(dep,ensure_ascii=False,indent=2)+'\n')
    sources[-1]['observed']=f'{OLD} deployed on 2024-02-23T09:46:05Z from source {OLD_SOURCE}.'
    tag=json.loads(get('GG-OLD-TAG',REPO+'/git/ref/tags/v3.5.0',locator='object.sha'))
    sources[-1]['observed']=f'v3.5.0 points to {tag["object"]["sha"]}.'
    yaml=get('GG-OLD-PKGDOWN',RAW+OLD+'/pkgdown.yml',locator='pkgdown,date,articles,last_built',category='build_record')
    if yaml:
        (OUT/'old-pkgdown-excerpt.txt').write_text(yaml.decode()[:5000])
        sources[-1]['observed']='pkgdown build metadata read; exact short metadata retained in old-pkgdown-excerpt.txt.'
    tree=json.loads(get('GG-OLD-TREE',REPO+'/git/trees/'+OLD+'?recursive=1',locator='tree entries under reference/',category='deployment_listing'))
    if tree.get('truncated'):raise RuntimeError('Old tree is truncated; cannot certify sorted frame')
    paths=sorted(x['path'] for x in tree['tree'] if x['type']=='blob' and x['path'].startswith('reference/') and x['path'].endswith('.html'))
    frame=[]; selected=[]; excerpts=[]
    for i,path in enumerate(paths,1):
        row={'project':'ggplot2','candidate_order':i,'release':'3.5.0','release_date':'2024-02-23T09:33:36Z','path':path,'status':'not_opened_after_first_two','reason':'Selection stops after first two eligible pages','case_id':''}
        if len(selected)<2:
            sid=f'GG-OLD-CAND-{i:03d}'
            b=get(sid,RAW+OLD+'/'+path,locator='Examples section; img/src/srcset/picture/source and download anchors',category='example_body')
            if b is None:row.update(status='access_failed',reason='Cannot treat inaccessible body as no image')
            else:
                text=b.decode('utf-8')
                # pkgdown's explicit Examples section is the target body, not header/nav art.
                m=re.search(r'<h2[^>]*id=["\'](?:ref-)?examples["\'][^>]*>',text,re.I)
                if not m:m=re.search(r'<div[^>]*id=["\']ref-examples["\'][^>]*>',text,re.I)
                example=text[m.start():] if m else ''
                srcs=re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)',example,re.I)
                srcs=[s for s in srcs if not re.match(r'(?i)(?:https?:|data:|//)',s)]
                if srcs:
                    case='GG'+str(len(selected)+1)
                    resource=urllib.parse.urljoin(path,srcs[0])
                    selected.append({'case_id':case,'project':'ggplot2','old_release':'3.5.0','new_release':'3.5.1','old_date':'2024-02-23T09:33:36Z','new_date':'2024-04-23T10:21:20Z','old_release_url':'https://github.com/tidyverse/ggplot2/releases/tag/v3.5.0','new_release_url':'https://github.com/tidyverse/ggplot2/releases/tag/v3.5.1','old_deploy_commit':OLD,'old_source_commit':OLD_SOURCE,'page_path':path,'old_section_uri':RAW+OLD+'/'+path+'#ref-examples','section':'Examples (#ref-examples / #examples)','old_src':srcs[0],'old_resource_path':resource,'old_resource_url':RAW+OLD+'/'+resource,'html_sha256':hashlib.sha256(b).hexdigest(),'html_bytes':len(b),'selection_order':i,'selection_transport':'official gh-pages publication tree at exact tag deploy','purpose':'Inspect and reuse the first rendered plot in the named reference Examples section; historic reader needs that edition of the section; publisher needs generation provenance separately.'})
                    row.update(status='selected',reason='Examples section directly refers to a named local image',case_id=case)
                else:row.update(status='excluded',reason='No named local image in explicit Examples section' if m else 'No Examples section')
                # Minimal attributes and nearby heading, not full copyrighted body.
                excerpts.append({'path':path,'examples_found':bool(m),'local_img_src':srcs,'title':re.findall(r'<title>(.*?)</title>',text,re.S)[:1],'version_tokens':re.findall(r'3\.5\.0(?:\.9000)?',text)[:3],'sha256':hashlib.sha256(b).hexdigest(),'html_bytes':len(b)})
                sources[-1]['observed']=f'Examples found={bool(m)}; local img src={srcs}; eligibility={row["status"]}.'
                sources[-1]['claim']='Sorted-frame eligibility and old section-to-image reference.'
        frame.append(row)
    with (OUT/'frame.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(frame[0]));w.writeheader();w.writerows(frame)
    (OUT/'selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    (OUT/'old-body-excerpts.json').write_text(json.dumps(excerpts,ensure_ascii=False,indent=2)+'\n')
    (OUT/'old-listing-summary.json').write_text(json.dumps({'tree_sha':tree['sha'],'truncated':tree.get('truncated',False),'entries':len(tree['tree']),'reference_html_count':len(paths),'selected':selected},ensure_ascii=False,indent=2)+'\n')
    (OUT/'sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in sources))
    print(json.dumps(selected,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
