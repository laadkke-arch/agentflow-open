"""Read-only public sources and static package inspection for AF-RES-102 Q7.

No downloaded code is imported or executed. Cache is excluded from Git; receipts,
member hashes, reference attributes, and analysis are committed instead.
"""
from __future__ import annotations
import argparse
import base64
import configparser
import csv
import hashlib
import io
import json
from pathlib import Path
import posixpath
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'cache'
RECEIPTS = ROOT / 'receipts'
CACHE.mkdir(exist_ok=True)
RECEIPTS.mkdir(exist_ok=True)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(key, url, refresh=False):
    cache = CACHE / key
    receipt_path = RECEIPTS / (key + '.json')
    if cache.exists() and receipt_path.exists() and not refresh:
        return cache.read_bytes(), json.loads(receipt_path.read_text())
    started = now()
    req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-102-public-source-audit/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
            # Signed redirect query strings expire and are irrelevant to provenance.
            u = urllib.parse.urlsplit(r.url)
            final = urllib.parse.urlunsplit((u.scheme,u.netloc,u.path,'',''))
            rec = {'requested_url':url,'final_url_without_temporary_query':final,
                   'started_utc':started,'finished_utc':now(),'status':r.status,
                   'content_type':r.headers.get('Content-Type'),'bytes':len(data),
                   'sha256':sha(data),'etag':r.headers.get('ETag'),
                   'last_modified':r.headers.get('Last-Modified'),
                   'headers_subset':{k:r.headers.get(k) for k in ['Content-Length','Content-Disposition','X-GitHub-Request-Id'] if r.headers.get(k)}}
            cache.write_bytes(data)
    except Exception as e:
        rec = {'requested_url':url,'started_utc':started,'finished_utc':now(),
               'status':getattr(e,'code',None),'error':str(e),'countable':False}
        receipt_path.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
        raise
    receipt_path.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
    return data, rec


def member(z, path):
    data=z.read(path)
    return {'path':path,'bytes':len(data),'sha256':sha(data),'zip_crc32':f'{z.getinfo(path).CRC:08x}'}


def resolve(base, relative):
    u=urllib.parse.urlsplit(relative)
    if u.scheme or u.netloc:
        return relative
    if not u.path:
        return base
    return posixpath.normpath(posixpath.join(posixpath.dirname(base),urllib.parse.unquote(u.path)))


def inspect_epub(data):
    z=zipfile.ZipFile(io.BytesIO(data))
    ns={'c':'urn:oasis:names:tc:opendocument:xmlns:container','o':'http://www.idpf.org/2007/opf','h':'http://www.w3.org/1999/xhtml'}
    container=ET.fromstring(z.read('META-INF/container.xml'))
    rootfiles=[x.attrib for x in container.findall('.//c:rootfile',ns)]
    result={'package_sha256':sha(data),'member_count':len(z.namelist()),'members':[member(z,n) for n in z.namelist() if not n.endswith('/')],
            'mimetype':z.read('mimetype').decode(), 'container':member(z,'META-INF/container.xml'),'rootfiles':rootfiles,'renditions':[]}
    for rf in rootfiles:
        opf=rf['full-path']; xml=ET.fromstring(z.read(opf))
        manifest=[]
        for i in xml.findall('.//o:manifest/o:item',ns):
            d=dict(i.attrib); d['resolved_path']=resolve(opf,d['href']);d['present']=d['resolved_path'] in z.namelist()
            manifest.append(d)
        index={i['id']:i for i in manifest}
        spine=[]
        for i in xml.findall('.//o:spine/o:itemref',ns):
            d=dict(i.attrib);d['resolved_path']=index[d['idref']]['resolved_path'];spine.append(d)
        xhtml=[]
        for item in manifest:
            if item['media-type'] != 'application/xhtml+xml' or not item['present']:continue
            path=item['resolved_path'];root=ET.fromstring(z.read(path));refs=[]
            for el in root.iter():
                for attr in ['src','href','data','poster','{http://www.w3.org/1999/xlink}href']:
                    if attr in el.attrib:
                        val=el.attrib[attr];target=resolve(path,val)
                        refs.append({'element':el.tag.split('}')[-1],'element_id':el.get('id'),'attribute':attr,'literal':val,'resolved_path':target,'present':target in z.namelist()})
            xhtml.append({'path':path,'member':member(z,path),'in_spine':any(x['resolved_path']==path for x in spine),'properties':item.get('properties',''),'references':refs,
                          'title':''.join(root.find('.//h:title',ns).itertext()) if root.find('.//h:title',ns) is not None else None})
        result['renditions'].append({'opf':member(z,opf),'package_attributes':xml.attrib,'manifest':manifest,'spine':spine,'xhtml':xhtml,
                                  'manifest_not_spine':[i['resolved_path'] for i in manifest if i['media-type']=='application/xhtml+xml' and i['resolved_path'] not in [s['resolved_path'] for s in spine]],
                                  'nonlinear_spine':[s for s in spine if s.get('linear')=='no']})
    return result


def inspect_wheel(data):
    z=zipfile.ZipFile(io.BytesIO(data));names=z.namelist()
    record=next(x for x in names if x.endswith('.dist-info/RECORD'))
    entries=next(x for x in names if x.endswith('.dist-info/entry_points.txt'))
    rows=list(csv.reader(io.StringIO(z.read(record).decode())))
    checked=[]
    for path,digest,size in rows:
        payload=z.read(path)
        if digest:
            alg,expected=digest.split('=',1)
            actual=base64.urlsafe_b64encode(hashlib.new(alg,payload).digest()).decode().rstrip('=')
            ok=actual==expected
        else:alg=expected=actual=None;ok=None
        checked.append({'path':path,'hash_algorithm':alg,'record_digest':expected,'observed_digest':actual,'digest_matches':ok,'record_size':size,'observed_bytes':len(payload),'size_matches':str(len(payload))==size if size else None})
    parser=configparser.ConfigParser(interpolation=None);parser.optionxform=str;parser.read_string(z.read(entries).decode())
    ep=[]
    for group in parser.sections():
        for name,obj in parser.items(group):
            module,_,qual=obj.partition(':'); candidate=module.replace('.','/')+'.py';package=module.replace('.','/')+'/__init__.py'
            target=candidate if candidate in names else package if package in names else None
            ep.append({'group':group,'name':name,'object_reference':obj,'module_member':target,'module_present':target is not None,'attribute':qual,
                       'member':member(z,target) if target else None})
    return {'package_sha256':sha(data),'member_count':len(names),'members':[member(z,n) for n in names if not n.endswith('/')],
            'record':member(z,record),'record_entries':checked,'entry_points':member(z,entries),'entry_points_text':z.read(entries).decode(),'declared_entrypoints':ep,
            'zip_unlisted':sorted(set(names)-{r[0] for r in rows}),'audit_installed_package':False,'audit_executed_entrypoint':False,'audit_imported_package_code':False,
            'historical_installation_or_execution':'미확인: package metadata and a static inspection do not record an execution event'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['fetch','epub','wheel']);ap.add_argument('--key');ap.add_argument('--url');ap.add_argument('--refresh',action='store_true');a=ap.parse_args()
    if a.mode=='fetch':
        _,receipt=get(a.key,a.url,a.refresh);print(json.dumps(receipt,indent=2))
    elif a.mode=='epub':
        key=a.key or 'trees.epub'
        data,_=get(key,a.url or 'https://github.com/IDPF/epub3-samples/releases/download/20230704/'+key,a.refresh)
        result=inspect_epub(data);(ROOT/(key.removesuffix('.epub')+'-audit.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'members':result['member_count'],'rootfiles':result['rootfiles'],'renditions':[{'opf':x['opf'],'manifest_count':len(x['manifest']),'spine_count':len(x['spine']),'not_spine':x['manifest_not_spine'],'nonlinear':x['nonlinear_spine']} for x in result['renditions']]},indent=2))
    else:
        release,rec=get('build-1.2.2.post1.json','https://pypi.org/pypi/build/1.2.2.post1/json',a.refresh)
        release=json.loads(release);info=next(x for x in release['urls'] if x['filename'].endswith('.whl'))
        data,rec=get(info['filename'],info['url'],a.refresh);result=inspect_wheel(data)
        result.update({'pypi_declared_sha256':info['digests']['sha256'],'pypi_digest_matches':sha(data)==info['digests']['sha256'],'download_url':info['url'],'pypi_uploaded_utc':info['upload_time_iso_8601']})
        (ROOT/'wheel-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'members':result['member_count'],'RECORD_rows':len(result['record_entries']),'RECORD_hash_matches':sum(x['digest_matches'] is True for x in result['record_entries']),'entrypoints':result['declared_entrypoints'],'pypi_digest_matches':result['pypi_digest_matches']},indent=2))
