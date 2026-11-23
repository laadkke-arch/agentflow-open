"""Observe the frozen SC032 links for the NEW JS-6 case only; no execution.

JS-4 inherits the AF056 windows and judgments unchanged.
"""
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import concurrent.futures,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
(HERE/'raw').mkdir(exist_ok=True);(HERE/'windows').mkdir(exist_ok=True)
sp=importlib.util.spec_from_file_location('ld_user_window',P/'evidence/paths-ld/prepare_paths.py')
mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
def now():return datetime.now(timezone.utc).isoformat()
def fetch(item):
    key,url=item;receipts=[];body=None;final=None
    for attempt in [url,url.replace('http:','https:',1)]:
        r={'requested_url':attempt,'utc':now()}
        try:
            with urlopen(Request(attempt,headers={'User-Agent':'AF-RES-060 bounded source observation'}),timeout=25) as response:
                body=response.read();final=response.url;r.update(status=response.status,final_url=final,content_type=response.headers.get('Content-Type'),sha256=hashlib.sha256(body).hexdigest())
            receipts.append(r);break
        except Exception as e:
            r.update(status=getattr(e,'code',None),error=str(e));receipts.append(r)
    d={'id':key,'original_url':url,'receipts':receipts,'final_url':final,'stage3_sha':'5d01a6208edd9f8a20be7b31f7b545cef2200597','case_id':'JS-6','catalog_id':'SC-032','existing_JS4_replaced':False}
    if body is None:d['status']='unavailable';return d
    suffix='.json' if key=='META' else '.html';raw=HERE/'raw'/(key+suffix);raw.write_bytes(body)
    text=body.decode('utf-8')
    if suffix=='.json':
        # Titleless code/JSON: preserve bytes as displayed, whitespace tokenization.
        parts=text.split();window=' '.join(parts[:500]);meta={'heading':'NO_HEADING_DOCUMENT_START','words':len(window.split()),'boundary':'First up to500 whitespace words of titleless JSON; original punctuation preserved.'}
    else:
        meta=mod.first_window(text,'.html');window=meta.pop('text');meta.pop('links',None)
    file=HERE/'windows'/(key+'.txt');file.write_text(window+'\n')
    d.update(status='fetched_window_pending_direct_read',raw_sha256=hashlib.sha256(body).hexdigest(),window_file=str(file.relative_to(P)),window_sha256=hashlib.sha256(window.encode()).hexdigest(),window=meta)
    return d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:rows=list(executor.map(fetch,[('HOME','http://json-schema.org/'),('META','http://json-schema.org/schema')]))
(HERE/'acquisition.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rows,ensure_ascii=False,indent=2))
