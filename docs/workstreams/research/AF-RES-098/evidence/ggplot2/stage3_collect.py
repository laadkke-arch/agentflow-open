"""Post-seal byte/DOM/publication audit. Does not build or run examples."""
import concurrent.futures
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import struct
import urllib.request
import urllib.error
import urllib.parse
from lxml import html

OUT=Path(__file__).resolve().parent
CACHE=Path('/tmp/af098-ggplot2')
RAW='https://raw.githubusercontent.com/tidyverse/ggplot2/'
API='https://api.github.com/repos/tidyverse/ggplot2'
OLD='392175bbb00b04025aa5d17a0c18b3896adeb40f'
NEW='3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c'
SOURCES={'3.5.0':'a6f1a7c845bfe056ef952b839d2fd65b888ab5cd','3.5.1':'8fa3974166aa998f1c61ae77e67886bbb94d8065'}

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):self.chain=[]
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        self.chain.append({'from':req.full_url,'status':code,'to':newurl})
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(job):
    sid,url,category,version,case=job
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    h=Redirects();b=None
    rec={'id':sid,'url':url,'utc':stamp,'category':category,'version':version,'case_id':case,'redirects':h.chain}
    try:
        with urllib.request.build_opener(h).open(url,timeout=45) as r:
            b=r.read();rec.update(status=r.status,final_url=r.url,mime=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
            (CACHE/(sid+'.bin')).write_bytes(b)
    except Exception as exc:rec.update(status=getattr(exc,'code',None),error=f'{type(exc).__name__}: {exc}')
    print(sid,rec.get('status'),rec.get('bytes'),flush=True)
    return rec

cases=json.loads((OUT/'selected.json').read_text())
jobs=[]
for case in cases:
    cid=case['case_id'];source_path='R/aes.R' if cid=='GG1' else 'R/aes-colour-fill-alpha.R'
    jobs.append((cid+'-NEW-BODY',RAW+NEW+'/'+case['page_path'],'example_body','3.5.1',cid))
    for version,pub in [('3.5.0',OLD),('3.5.1',NEW)]:
        label='OLD' if version=='3.5.0' else 'NEW'
        jobs.append((cid+'-'+label+'-PNG',RAW+pub+'/'+case['old_resource_path'],'image_payload',version,cid))
        jobs.append((cid+'-'+label+'-SOURCE',RAW+SOURCES[version]+'/'+source_path,'example_source',version,cid))
jobs += [('GG-NEW-PKGDOWN',RAW+NEW+'/pkgdown.yml','build_record','3.5.1','GG1;GG2')]
for version,source in SOURCES.items():
    label='OLD' if version=='3.5.0' else 'NEW'
    jobs.append(('GG-'+label+'-WORKFLOW',RAW+source+'/.github/workflows/pkgdown.yaml','build_rule',version,'GG1;GG2'))
    jobs.append(('GG-'+label+'-ACTIONS',API+'/actions/runs?head_sha='+source+'&per_page=100','publication_run',version,'GG1;GG2'))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:receipts=list(ex.map(fetch,jobs))
(OUT/'stage3-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
recmap={r['id']:r for r in receipts}
trees={'3.5.0':json.loads((CACHE/'GG-OLD-TREE.bin').read_text()),'3.5.1':json.loads((CACHE/'GG-NEW-TREE-LIST.bin').read_text())}
rows=[];details=[]
for case in cases:
    cid=case['case_id']
    for version,pub in [('3.5.0',OLD),('3.5.1',NEW)]:
        label='OLD' if version=='3.5.0' else 'NEW'
        body_sid=('GG-OLD-CAND-003' if cid=='GG1' else 'GG-OLD-CAND-007') if label=='OLD' else cid+'-NEW-BODY'
        body_path=CACHE/(body_sid+'.bin')
        png_rec=recmap[cid+'-'+label+'-PNG']
        b=body_path.read_bytes() if body_path.exists() else None
        base_url=RAW+pub+'/'+case['page_path']
        tree=html.fromstring(b) if b else None
        section_nodes=tree.xpath('//*[@id="ref-examples"]/parent::*') if tree is not None else []
        section=section_nodes[0] if section_nodes else None
        base_nodes=tree.xpath('//base/@href') if tree is not None else []
        effective_base=urllib.parse.urljoin(base_url,base_nodes[0]) if base_nodes else base_url
        refs=[]
        if section is not None:
            for node in section.iter():
                attrs={k:v for k,v in node.attrib.items() if k in ['src','srcset','href','data','poster','type']}
                if attrs:refs.append({'tag':node.tag,'line':node.sourceline,'attributes':attrs})
        imgs=section.xpath('.//img') if section is not None else []
        first=imgs[0] if imgs else None
        src=first.get('src') if first is not None else None
        resolved=urllib.parse.urljoin(effective_base,src) if src else None
        pb=(CACHE/(cid+'-'+label+'-PNG.bin')).read_bytes() if png_rec.get('status')==200 else None
        signature='PNG' if pb and pb[:8]==b'\x89PNG\r\n\x1a\n' else 'unknown'
        dimensions=list(struct.unpack('>II',pb[16:24])) if signature=='PNG' else None
        entry=next((x for x in trees[version]['tree'] if x['path']==case['old_resource_path']),None)
        blob=hashlib.sha1(b'blob '+str(len(pb)).encode()+b'\0'+pb).hexdigest() if pb else None
        blob_match=bool(entry and blob==entry['sha'])
        versions=re.findall(r'(?<![\d.])3\.5\.[01](?:\.9000)?(?![\d.])',b.decode()) if b else []
        details.append({'case_id':cid,'version':version,'publication_commit':pub,'body_url':base_url,'body_sha256':hashlib.sha256(b).hexdigest() if b else None,
          'body_bytes':len(b) if b else None,'body_version_tokens':sorted(set(versions)),'base_elements':base_nodes,'effective_base':effective_base,
          'section':'h2#ref-examples parent div.section.level2','section_line':section.sourceline if section is not None else None,
          'section_refs':refs,'first_image':dict(first.attrib) if first is not None else None,
          'counts':{name:len(section.xpath(expr)) if section is not None else None for name,expr in {'img':'.//img','source':'.//source','picture':'.//picture','figcaption':'.//figcaption','inline_svg':'.//*[local-name()="svg"]','script':'.//script','data_uri':'.//*[@src[starts-with(.,"data:")]]'}.items()},
          'payload':{'url':resolved,'mime':png_rec.get('mime'),'bytes':len(pb) if pb else None,'sha256':hashlib.sha256(pb).hexdigest() if pb else None,'signature':signature,'dimensions':dimensions,'git_blob_sha':blob,'tree_blob_matches':blob_match},
          'limits':'Static document parsing and direct HTTP bytes; no browser execution or example execution. No output-specific generation attestation found in this collection.'})
        source_path='R/aes.R' if cid=='GG1' else 'R/aes-colour-fill-alpha.R'
        rows.append({'case_id':cid,'version':version,'source_url':RAW+SOURCES[version]+'/'+source_path,'source_sha':recmap[cid+'-'+label+'-SOURCE'].get('sha256'),
          'body_url':base_url+'#ref-examples','body_sha256':hashlib.sha256(b).hexdigest() if b else '',
          'section':'h2#ref-examples','section_line':section.sourceline if section is not None else '',
          'base_uri':effective_base,'ref_type':'img/src','actual_ref':src,'payload_url':resolved,
          'payload_mime':png_rec.get('mime'),'payload_bytes':len(pb) if pb else '',
          'payload_sha256':hashlib.sha256(pb).hexdigest() if pb else '',
          'P_included':'YES' if blob_match else 'UNKNOWN','U_section_uses':'YES' if resolved==png_rec['url'] and pb else 'UNKNOWN',
          'G_generated_this_build':'UNKNOWN','publication_record_url':'https://github.com/tidyverse/ggplot2/commit/'+pub,
          'generation_record_url':'','limits':'Deploy source linkage, version metadata and matching blob prove publication/use only; no payload-specific build digest/attestation.'})
with (OUT/'lineage.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'audit.json').write_text(json.dumps({'stage2_seal':'0df9ea9edbcee995d631eef54b65fd43f73c245f','checked_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'rows':details},ensure_ascii=False,indent=2)+'\n')
with (OUT/'sources.jsonl').open('a') as f:
    for r in receipts:
        obj={'id':r['id'],'q':['Q3','Q4'],'case_id':r['case_id'].split(';'),'url':r['url'],'fixed_url':r['url'],
         'utc':r['utc'],'publisher':'tidyverse/ggplot2 maintainers','lineage':'ggplot2 documentation','version':r['version'],
         'locator':'h2#ref-examples and first img' if r['category']=='example_body' else 'payload' if r['category']=='image_payload' else 'source/build/publication metadata',
         'observed':'Direct response retained temporarily; content observations summarized in audit.json and stage3.md after reading.',
         'claim':'Publication, section use and generation are separate propositions.',
         'limitations':'No example execution. Build logs/artifact provenance require separate confirmation.',
         'counted':r.get('status')==200,'dedup_basis':'Provisional; final merge deduplicates same work plus identical bytes.',
         'category':r['category'],'sha256':r.get('sha256'),'bytes':r.get('bytes'),'receipt_id':r['id']}
        if r.get('error'):obj['observed']=r['error'];obj['limitations']='Access failure is not file absence.'
        f.write(json.dumps(obj,ensure_ascii=False)+'\n')
print(json.dumps({'rows':rows,'receipt_count':len(receipts),'failed':[r for r in receipts if r.get('status')!=200]},ensure_ascii=False,indent=2))
