"""Download only two fixed public research archives, inspect in memory, execute nothing."""
import concurrent.futures, datetime, hashlib, io, json, pathlib, re, tarfile, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent

def inspect(spec):
    sid, record = spec
    j=json.loads((ROOT/'evidence'/f'{record}.json').read_text())
    file=j['files'][0]
    out={'id':sid,'record_id':j['id'],'request_url':file['links']['self'],'requested_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publisher_checksum':file['checksum'],'publisher_size':file['size']}
    try:
        with urllib.request.urlopen(out['request_url'],timeout=40) as r:
            b=r.read(4000001)
            out.update(http_status=r.status,final_url=r.url,response_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),md5=hashlib.md5(b).hexdigest(),body_complete=len(b)<4000001)
        out['publisher_checksum_equal']=file['checksum']=='md5:'+out['md5']
        if len(b)>=4000001: raise ValueError('bounded read exceeded')
        entries=[]
        with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as t:
            for e in t:
                x={'path':e.name,'size':e.size,'type':'file' if e.isfile() else 'directory' if e.isdir() else 'other','mtime':e.mtime}
                if e.isfile():
                    data=t.extractfile(e).read()
                    x['sha256']=hashlib.sha256(data).hexdigest()
                    if e.name.lower().endswith('setup.py'):
                        x['version_lines']=[l for l in data.decode('utf-8','replace').splitlines() if re.search(r'version\s*=',l)][:3]
                entries.append(x)
        out['members']=entries
        out['archive_retained']=False
    except Exception as e: out['error']=type(e).__name__+': '+str(e)
    out['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'evidence'/f'{sid}.manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    return {k:v for k,v in out.items() if k!='members'}|{'member_count':len(out.get('members',[]))}

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:
        for x in p.map(inspect,[('PR23','PR10'),('PR24','PR06')]):print(json.dumps(x),flush=True)
