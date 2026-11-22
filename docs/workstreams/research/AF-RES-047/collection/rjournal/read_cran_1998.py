"""Inspect publisher tarballs named by the fixed author's 1998 input manifest.

No source code is evaluated. Download URL mapping is a candidate mapping
from the author's local mirror path; HTTP success is recorded separately.
"""
import concurrent.futures,csv,datetime,hashlib,io,json,re,tarfile,urllib.request
from pathlib import Path
P=Path(__file__).resolve().parent
rows=list(csv.DictReader((P/'rstyle_1998_input_manifest.csv').open()))
def read(row):
    url='https://cran.r-project.org/src/contrib/'+row['path'].split('./cran/contrib/main/',1)[1]
    out={'package':row['pkg_name'],'declared_local_path':row['path'],'source_url':url,'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url_mapping_status':'candidate_canonical_mapping_from_local_manifest'}
    try:
        with urllib.request.urlopen(url,timeout=20) as r:
            b=r.read();out.update(final_url=r.url,status=r.status)
        out.update(size=len(b),sha256=hashlib.sha256(b).hexdigest(),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as t:
            out['members']=[];out['R_source_files']=[]
            for member in t.getmembers():
                if not member.isfile():continue
                out['members'].append(member.name)
                if '/R/' in member.name:
                    content=t.extractfile(member).read();text=content.decode('latin-1')
                    out['R_source_files'].append({'name':member.name,'size':len(content),'sha256':hashlib.sha256(content).hexdigest(),'rough_equal_function_tokens':len(re.findall(r'=\s*function\s*\(',text)),'limitation':'R source may contain comments/strings and syntax variants; this token count is a screening check, not the lintr feature or export-selection replication'})
            desc=[m for m in t.getmembers() if m.isfile() and m.name.endswith('/DESCRIPTION')]
            if desc:
                d=t.extractfile(desc[0]).read().decode('latin-1')
                out['description_package_version']=[line for line in d.splitlines() if line.startswith(('Package:','Version:','Date:'))]
    except Exception as e:out.update(error=repr(e),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    return out
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as x:result=list(x.map(read,rows))
(P/'cran_1998_publisher_receipts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for x in result:print(json.dumps({k:v for k,v in x.items() if k not in ('members','R_source_files')},ensure_ascii=False))
