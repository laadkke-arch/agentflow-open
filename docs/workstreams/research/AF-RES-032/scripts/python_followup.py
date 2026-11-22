"""Inspect every stable 3.8 documentation archive; preserve observed bytes, not inferred deployment."""
from pathlib import Path
from datetime import datetime,timezone
import urllib.request,tarfile,io,json,hashlib,re,concurrent.futures,csv
from lxml import html
P=Path(__file__).resolve().parents[1]/'collectors/python/followup';(P/'cache').mkdir(parents=True,exist_ok=True);(P/'excerpts').mkdir(exist_ok=True)
def one(n):
    v=f'3.8.{n}';u=f'https://docs.python.org/ftp/python/doc/{v}/python-{v}-docs-html.tar.bz2';at=datetime.now(timezone.utc).isoformat();r={'version':v,'url':u,'observed_at_utc':at}
    try:
        res=urllib.request.urlopen(u,timeout=45);b=res.read();(P/'cache'/f'{v}.tar.bz2').write_bytes(b)
        r.update(status=res.status,final_url=res.url,bytes=len(b),archive_sha256=hashlib.sha256(b).hexdigest(),last_modified=res.headers.get('Last-Modified'),last_modified_role='server file metadata, not first publication')
        t=tarfile.open(fileobj=io.BytesIO(b)); docs=[]
        for name in ['about.html','bugs.html']:
            member=f'python-{v}-docs-html/{name}';x=t.extractfile(member).read();doc=html.fromstring(x);body=doc.xpath('//div[@class="body"]')[0]
            anchors=[]
            for a in body.xpath('.//a[starts-with(@href,"http")]'):
                txt=' '.join(a.itertext()).strip();href=a.get('href')
                if (name=='about.html' and 'reStructuredText' in txt) or (name=='bugs.html' and ('Documentation bugs' in txt or ('github.com/python/cpython/issues' in href))):
                    par=a
                    while par.getparent() is not None and par.tag not in ('p','dd','div','li'):par=par.getparent()
                    anchors.append({'href':href,'link_text':txt,'context':' '.join(par.itertext()).strip(),'html':html.tostring(par,encoding='unicode')})
            docs.append({'name':name,'member':member,'member_sha256':hashlib.sha256(x).hexdigest(),'anchors':anchors,'title':doc.xpath('//title')[0].text_content(),'body_sha256':hashlib.sha256(html.tostring(body)).hexdigest()})
            (P/'excerpts'/f'{v}-{name}.json').write_text(json.dumps(docs[-1],ensure_ascii=False,indent=2))
        r['documents']=docs
    except Exception as e:r['error']=repr(e)
    return r
if __name__=='__main__':
    rows=list(concurrent.futures.ThreadPoolExecutor(4).map(one,range(2,21)))
    (P/'archives.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    print(json.dumps([{'version':r['version'],'status':r.get('status'),'error':r.get('error'),'links':[(d['name'],[(a['link_text'],a['href']) for a in d['anchors']]) for d in r.get('documents',[])]} for r in rows],ensure_ascii=False,indent=2))
