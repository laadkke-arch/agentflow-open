"""Public read-only acquisition helpers. Full responses stay in ignored cache.

Use per-reader directories and do not print later revisions before the seals.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import urllib.parse
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
INITIAL_FILTER = '7W-GLRnw_MC-oFjiXW2Yp.*Kixtw9X1Cp_B-Jb'

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def fetch(url, reader, key, binary=False):
    cache = ROOT / '.cache' / reader
    evidence = ROOT / 'evidence' / reader
    cache.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    destination = cache / (key + ('.bin' if binary else '.json'))
    started = utc()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AF-RES-105 public-source audit'})
        with urllib.request.urlopen(req, timeout=40) as response:
            data = response.read()
            status = response.status
            ctype = response.headers.get('Content-Type', '')
            final_url = response.url
        destination.write_bytes(data)
        receipt = {'url': url, 'final_url': final_url, 'opened_utc': started,
                   'ended_utc': utc(), 'http_status': status, 'content_type': ctype,
                   'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                   'cache': str(destination.relative_to(ROOT)), 'key': key}
        if not binary:
            obj = json.loads(data)
            receipt.update({k: obj[k] for k in ('has_more','quota_remaining','backoff','error_id','error_message') if k in obj})
        else:
            obj = data
    except Exception as error:
        receipt = {'url':url, 'opened_utc':started, 'ended_utc':utc(),
                   'error_type':type(error).__name__, 'error':str(error), 'key':key}
        obj = None
    with (evidence / 'acquisition.jsonl').open('a') as out:
        out.write(json.dumps(receipt,ensure_ascii=False)+'\n')
    if obj is None:
        raise RuntimeError(receipt)
    if isinstance(obj,dict) and ('error_id' in obj or 'backoff' in obj):
        raise RuntimeError('API error/backoff recorded; stop and coordinate: '+json.dumps(receipt))
    return obj, receipt

def se(path, params, reader, key):
    return fetch('https://api.stackexchange.com/2.3/'+path+'?'+urllib.parse.urlencode(params),reader,key)

def initial_frame(site, tag, reader, half=1):
    lo, hi = (1704067200,1719791999) if half==1 else (1719792000,1735689599)
    obj, receipt = se('questions', {'site':site,'tagged':tag,'fromdate':lo,'todate':hi,
                         'sort':'creation','order':'asc','pagesize':80,'page':1,
                         'filter':INITIAL_FILTER},reader,f'frame-h{half}')
    items=sorted(obj['items'],key=lambda x:(x['creation_date'],x['question_id']))
    if len(items)==80:
        boundary=items[-1]['creation_date']
        ties,tie_receipt=se('questions',{'site':site,'tagged':tag,'fromdate':boundary-1,'todate':boundary+1,
                                     'sort':'creation','order':'asc','pagesize':100,'page':1,
                                     'filter':INITIAL_FILTER},reader,f'frame-h{half}-boundary')
        if ties.get('has_more'):
            raise RuntimeError('More than100 creation-time ties; do not claim first80 until all ties resolved')
        by_id={x['question_id']:x for x in items+[t for t in ties['items'] if t['creation_date']==boundary]}
        if not any(t['question_id']==items[-1]['question_id'] for t in ties['items']):
            raise RuntimeError('Boundary query omits known last item; resolve with masked next-page metadata')
        items=sorted(by_id.values(),key=lambda x:(x['creation_date'],x['question_id']))[:80]
    # Only the custom filter fields are exposed; no answer metadata exists here.
    (ROOT/'.cache'/reader/f'frame-h{half}-masked.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
    return items, receipt

def initial_revisions(ids,site,reader,label):
    selected={}
    receipts=[]
    page=1
    while True:
        obj, receipt=se('posts/'+';'.join(map(str,ids))+'/revisions',
                         {'site':site,'pagesize':100,'page':page,'filter':INITIAL_FILTER},
                         reader,f'{label}-revisions-page{page}')
        receipts.append(receipt)
        for item in obj['items']:
            if item.get('revision_number')==1:
                # Metadata-only revisions can share a first revision number.
                key=str(item['post_id'])
                previous=selected.get(key,{})
                if previous and previous.get('revision_guid')!=item.get('revision_guid'):
                    raise RuntimeError('Conflicting revision1 GUIDs; preserve conflict instead of overwriting')
                previous.update(item)
                selected[key]=previous
        if not obj.get('has_more'):
            break
        page+=1
        if page>12:
            raise RuntimeError('Unexpected revision paging >12; record partial instead of silently truncating')
    p=ROOT/'.cache'/reader/(label+'-initial-only.json')
    p.write_text(json.dumps(selected,ensure_ascii=False,indent=2))
    return selected,receipts

if __name__=='__main__':
    print('Import helpers; no automatic network calls.')
