"""Attach original network receipts to cached-reader projections without claiming a rerequest."""
import json,hashlib,re
from pathlib import Path
P=Path(__file__).resolve().parent;idx={}
for f in (P/'evidence').glob('*/acquisition.jsonl'):
 for line in f.read_text().splitlines():
  try:r=json.loads(line);cache=P/r.get('cache','_missing')
  except Exception:continue
  if not cache.is_file() or cache.suffix!='.json':continue
  try:o=json.loads(cache.read_text())
  except Exception:continue
  if not isinstance(o,dict):continue
  url=r.get('url','');site='blender' if 'site=blender' in url else 'gis' if 'site=gis' in url else None
  if not site:continue
  for i,item in enumerate(o.get('items',[])):
   if not isinstance(item,dict) or 'body' not in item:continue
   h=hashlib.sha256(item['body'].encode()).hexdigest();key=(site,h)
   idx.setdefault(key,dict(api_url=url,opened_utc=r.get('opened_utc'),response_sha256=r.get('sha256'),cache=r.get('cache'),json_pointer=f'/items/{i}/body',receipt=str(f.relative_to(P))))
paths=[P/'evidence/auxiliary-followup/sources-part.jsonl',P/'evidence/blender-auxiliary/sources-part.jsonl',P/'evidence/auxiliary-counter/sources-part.jsonl']
count=0
for path in paths:
 out=[]
 for line in path.read_text().splitlines():
  s=json.loads(line);site='blender' if 'blender.stackexchange' in s.get('original_url','') else 'gis' if 'gis.stackexchange' in s.get('original_url','') else None;fp=s.get('fingerprint',{});h=fp.get('body_sha256',fp.get('body_utf8_sha256',fp.get('initial_body_sha256')))
  r=idx.get((site,h))
  if r:
   s['original_network_receipt']=r;s['opened_utc']=r['opened_utc'];s['reader_read_utc_window']={'from':'2026-11-23T23:49:08.391264Z' if 'blender-auxiliary' in str(path) else '2026-11-24T00:04:06Z','through':'2026-11-24T00:25:00Z','precision':'actual API acquisition exact; later cached text reading bounded, not timed exactly'};count+=1
  out.append(s)
 path.write_text(''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in out))
print('network receipts attached',count)
