"""Post-seal single-message reading. Saves metadata/hashes, not email bodies."""
import argparse,concurrent.futures,hashlib,html,json,re,urllib.request
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
SEAL='68fc97fadceb46f9945a71fcc53730e29f6c62bf'

def clean(s):
 s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
 return html.unescape(re.sub('<[^>]*>','',s)).strip()

def read(entry):
 url=entry['url']; started=datetime.now(timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(url,timeout=30) as r: raw=r.read()
  s=raw.decode()
  headers={clean(a).rstrip(':'):clean(b) for a,b in re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>([\s\S]*?)</td>',s)}
  headers={k:headers.get(k) for k in ['From','To','Subject','Date','Message-ID']}
  body=re.search(r'<div class="message-content">([\s\S]*?)</div>',s).group(1)
  pars=[clean(t) for t in re.findall(r'<p>([\s\S]*?)</p>',body)]
  pars=[x for x in pars if x] or [clean(body)]
  text='\n\n'.join(pars)
  tail=s[s.find('</div>',s.find('<div class="message-content">'))+6:]
  m=re.search(r'In response to[\s\S]*?<a href="([^"]+)"',tail)
  return {**entry,'headers':headers,'started_utc':started,'checked_utc':datetime.now(timezone.utc).isoformat(),'seal_commit':SEAL,'html_sha256':hashlib.sha256(raw).hexdigest(),'body_sha256':hashlib.sha256(text.encode()).hexdigest(),'paragraph_count':len(pars),'reply_to_url':'https://www.postgresql.org'+m[1] if m and m[1].startswith('/') else m[1] if m else None,'body_links':re.findall(r'(?:href|src)="([^"]+)"',body),'read_body':{f'p{i+1}':v for i,v in enumerate(pars)}}
 except Exception as e:
  return {**entry,'started_utc':started,'seal_commit':SEAL,'error':type(e).__name__+': '+str(e)}

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--cases',required=True);args=a.parse_args();cases=args.cases.split(',')
 receipt=P/'t1-receipt.json'
 if not receipt.exists():receipt.write_text(json.dumps({'seal_commit':SEAL,'seal_remote_verification':'root reported exact-SHA t0-seal.json and 24 response rows reread','first_followup_body_request_started_utc':datetime.now(timezone.utc).isoformat(),'t0_initial_sha256':hashlib.sha256((P/'initial.jsonl').read_bytes()).hexdigest(),'t0_responses_sha256':hashlib.sha256((P/'frozen-responses.jsonl').read_bytes()).hexdigest(),'execution':'urllib single-message GET; no model/user message sent'},indent=2)+'\n')
 nav=json.loads((P/'navigation-metadata.json').read_text())
 entries=[{'case_id':n['case_id'],'url':x['message_id_url']} for n in nav if n['case_id'] in cases for x in n['navigation_metadata_only'] if x['message_id_url']!=n['root_url']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(read,entries))
 dest=P/('t1-captures-'+ '-'.join(cases)+'.json')
 dest.write_text(json.dumps([{k:v for k,v in r.items() if k!='read_body'} for r in rows],ensure_ascii=False,indent=2)+'\n')
 for r in rows:print(json.dumps(r,ensure_ascii=False,indent=2),flush=True)
