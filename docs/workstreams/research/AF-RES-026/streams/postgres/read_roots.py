"""Read only the body of single-message pages; never open a thread before sealing.

The whole HTML may contain reply-navigation metadata, which is not printed.
Only short metadata and hashes are saved; public email bodies are printed for reading,
not copied into the research repository.
"""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.request

ROOT=Path(__file__).resolve().parent
LEDGER='https://www.postgresql.org/list/pgsql-general/2022-01/'

def clean(s):
    s=re.sub(r'<br\s*/?>','\n',s,flags=re.I)
    return html.unescape(re.sub('<[^>]*>','',s)).strip()

def get(url):
    with urllib.request.urlopen(url,timeout=25) as r:
        return r.read(), r.headers.get('Date')

raw, fetched_server=get(LEDGER)
s=raw.decode()
roots=[]
for i,row in enumerate(re.findall(r'<tr[\s\S]*?</tr>',s)):
    m=re.search(r'<a href="(/message-id/[^"]+)">([\s\S]*?)</a>',row)
    if not m:continue
    title=clean(m[2])
    if re.match(r'(re|sv|aw):',title,re.I):continue
    roots.append({'ledger_row':i,'title':title,'url':'https://www.postgresql.org'+m[1]})

def one(entry):
    raw, server=get(entry['url']);s=raw.decode()
    headers={clean(a).rstrip(':'):clean(b) for a,b in re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>([\s\S]*?)</td>',s)}
    headers={k:headers.get(k) for k in ['From','To','Subject','Date','Message-ID']}
    body=re.search(r'<div class="message-content">([\s\S]*?)</div>',s).group(1)
    paragraphs=[clean(p) for p in re.findall(r'<p>([\s\S]*?)</p>',body)]
    if not paragraphs: paragraphs=[clean(body)]
    pars=[p for p in paragraphs if p]
    text='\n\n'.join(pars)
    return {**entry,'headers':headers,'checked_utc':datetime.now(timezone.utc).isoformat(),'fetch_http_date':server,'html_sha256':hashlib.sha256(raw).hexdigest(),'body_sha256':hashlib.sha256(text.encode()).hexdigest(),'body_hash_method':'UTF-8 of nonempty p elements; br->newline; other HTML tags removed; entities decoded; strip each; joined by two newlines','paragraph_count':len(pars),'read_body':{f'p{i+1}':p for i,p in enumerate(pars)}}

if __name__=='__main__':
    selected=roots[:8]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        data=list(ex.map(one,selected))
    (ROOT/'capture-index.json').write_text(json.dumps({'ledger_url':LEDGER,'ledger_sha256':hashlib.sha256(raw).hexdigest(),'ledger_http_date':fetched_server,'root_candidates':[x for x in roots[:8]],'captures':[{k:v for k,v in x.items() if k!='read_body'} for x in data]},ensure_ascii=False,indent=2)+'\n')
    for x in data:print(json.dumps(x,ensure_ascii=False,indent=2))
