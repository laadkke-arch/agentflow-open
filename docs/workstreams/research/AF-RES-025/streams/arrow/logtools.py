import json,pathlib,re,hashlib,csv,sys,datetime
P=pathlib.Path(__file__).resolve().parent
FIELDS=['receipt_id','event_type','question_id','route','query_index','observed_rank','started_utc','ended_utc','wall_ms','query','engine','response_length','provided_count','search_engine_absolute_rank','url','title','ref_id','eligible_first10','decision','reason','source_id','candidate_id','body_receipt','failure','retry_of']
def parse_search(rec):
 text='\n'.join(x.get('text','') for x in rec['raw'].get('content',[]) if x.get('type')=='text')
 # Result delimiters can be omitted after PDF snippets; the cited header is the
 # observed tool-result boundary. This preserves every provided output rank.
 out=[]
 for rank,m in enumerate(re.finditer(r'^(.+?) \((https?://[^\n]+)\)\n【([^】]+)】',text,re.M),1):
  out.append({'provided_rank':rank,'title':m.group(1),'url':m.group(2),'ref_id':m.group(3),'within_first10':rank<=10})
 return out

def rebuild():
 rows=[]
 for f in sorted((P/'cache'/'search').glob('*.json')):
  rec=json.loads(f.read_text());results=parse_search(rec)
  req=rec['request'];query=req['system1_search_query'][0]['q']
  receipt={k:v for k,v in rec.items() if k!='raw'};receipt['results']=results;receipt['returned_count']=len(results);receipt['first10_count']=min(10,len(results));receipt['shortfall_to_ten']=max(0,10-len(results));receipt['raw_response_sha256']=hashlib.sha256(json.dumps(rec['raw'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();receipt['hash_serialization']='JSON UTF-8 sorted keys compact separators; actual tool response kept untracked cache';receipt['search_engine_absolute_rank']='unknown';receipt['cost_tokens']='unknown';receipt['cost_money']='unknown'
  (P/'receipts').mkdir(exist_ok=True)
  (P/'receipts'/(f.stem+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
  base={'receipt_id':rec['receipt_id'],'question_id':rec['question_id'],'route':rec['route'],'query_index':rec['query_index'],'started_utc':rec['started_utc'],'ended_utc':rec['ended_utc'],'wall_ms':rec['wall_ms'],'query':query,'engine':'system1_search_query','response_length':'long','provided_count':len(results),'search_engine_absolute_rank':'unknown'}
  rows.append(dict(base,event_type='search_request',decision='executed'))
  for item in results:rows.append(dict(base,event_type='search_result',observed_rank=item['provided_rank'],url=item['url'],title=item['title'],ref_id=item['ref_id'],eligible_first10=item['within_first10'],decision='pending' if item['within_first10'] else 'outside_first10',reason='' if item['within_first10'] else 'provided beyond query cap; not selected'))
 for f in sorted((P/'cache'/'opens').glob('*.json')):
  rec=json.loads(f.read_text());rawtext='\n'.join(x.get('text','') for x in rec['raw'].get('content',[]) if x.get('type')=='text')
  receipt={k:v for k,v in rec.items() if k!='raw'};receipt['raw_response_sha256']=hashlib.sha256(json.dumps(rec['raw'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();receipt['hash_serialization']='JSON UTF-8 sorted keys compact separators';receipt['result_header']=rawtext.split('\n')[0] if rawtext else '';receipt['is_error']=bool(rec['raw'].get('isError')) or bool(re.search(r'Failed to fetch|Internal Error|is not safe to open|error fetching',rawtext,re.I));receipt['cost_tokens']='unknown';receipt['cost_money']='unknown'
  ref=rec['request']['open'][0]['ref_id']
  url=ref
  if not ref.startswith('http'):
   for sf in sorted((P/'cache'/'search').glob('*.json')):
    matches=[x for x in parse_search(json.loads(sf.read_text())) if x['ref_id']==ref]
    if matches:url=matches[0]['url'];break
  receipt['requested_url']=url
  (P/'receipts'/(f.stem+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
  rows.append({'receipt_id':rec['receipt_id'],'event_type':'retry' if 'retry_of' in rec else 'open_attempt','question_id':rec['question_id'],'route':rec['route'],'started_utc':rec['started_utc'],'ended_utc':rec['ended_utc'],'wall_ms':rec['wall_ms'],'url':url,'ref_id':ref,'body_receipt':rec['receipt_id'],'failure':receipt['is_error'],'retry_of':rec.get('retry_of',''),'decision':'attempted'})
 decisions={}
 if (P/'selection.json').exists():
  for d in json.loads((P/'selection.json').read_text()):decisions[(d['receipt_id'],d['observed_rank'])]=d
 for r in rows:
  if r['event_type']=='search_result':
   d=decisions.get((r['receipt_id'],r['observed_rank']))
   if d:r.update({k:v for k,v in d.items() if k in FIELDS})
 with (P/'search-log.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore');w.writeheader();w.writerows(rows)
 print(json.dumps({'rows':len(rows),'search_requests':sum(r['event_type']=='search_request' for r in rows),'search_results':sum(r['event_type']=='search_result' for r in rows),'open_attempts':sum(r['event_type']=='open_attempt' for r in rows),'retries':sum(r['event_type']=='retry' for r in rows)}))
if __name__=='__main__':rebuild()
