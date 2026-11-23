"""Acquire an assertion-masked input view without printing expected states."""
from pathlib import Path
import re,json,hashlib,datetime,urllib.request
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
CACHE=ROOT/'.cache'/'yjs'; CACHE.mkdir(parents=True,exist_ok=True)
meta=json.loads((OUT/'metadata-freeze.json').read_text());sha=meta['sha'];path=meta['test_paths'][0]
u=f'https://raw.githubusercontent.com/yjs/yjs/{sha}/{path}'
raw=urllib.request.urlopen(u,timeout=30).read();(CACHE/'diagnostic-raw.js').write_bytes(raw)
s=raw.decode();masked=list(s);spans=[]
def erase(a,b,kind):
 for i in range(a,b):
  if masked[i]!='\n':masked[i]=' '
 spans.append({'start_line':s.count('\n',0,a)+1,'end_line':s.count('\n',0,b)+1,'kind':kind})
def skip_string(s,i):
 q=s[i];i+=1
 while i<len(s):
  if s[i]=='\\':i+=2;continue
  if s[i]==q:return i+1
  i+=1
 return i
i=0
while i<len(s):
 if s[i] in '\"\'`':i=skip_string(s,i);continue
 if s.startswith('//',i):
  j=s.find('\n',i);j=len(s) if j<0 else j;erase(i,j,'line_comment');i=j;continue
 if s.startswith('/*',i):
  j=s.find('*/',i+2);j=len(s) if j<0 else j+2;erase(i,j,'block_comment');i=j;continue
 i+=1
clean=''.join(masked)
pat=re.compile(r'\b(?:t\.(?:compare\w*|assert\w*)|ist|eq|deepEqual|strictEqual|assert\w*|expect)\s*\(')
for m in list(pat.finditer(clean)):
 a=m.start();i=m.end()-1;depth=0
 while i<len(clean):
  if clean[i] in '\"\'`':i=skip_string(clean,i);continue
  if clean[i]=='(':depth+=1
  elif clean[i]==')':
   depth-=1
   if depth==0:i+=1;break
  i+=1
 while i<len(clean) and clean[i] not in '\n;':i+=1
 if i<len(clean) and clean[i]==';':i+=1
 erase(a,i,'assertion_call')
clean=''.join(masked)
for m in re.finditer(r'(?m)^.*\b(?:expected\w*|snapshot\w*)\s*=.*$',clean,re.I):erase(m.start(),m.end(),'expected_assignment')
clean=''.join(masked)
functions=[]
ms=list(re.finditer(r'(?m)^export const (test\w+)\s*=',clean))
for i,m in enumerate(ms):
 end=ms[i+1].start() if i+1<len(ms) else len(s);f=clean[m.start():end];begin=s.count('\n',0,m.start())+1;finish=s.count('\n',0,end)+1
 assertions=[x for x in spans if x['kind']=='assertion_call' and begin<=x['start_line']<finish]
 row={'name':m.group(1),'start_line':begin,'end_line':finish-1,'undo_calls':len(re.findall(r'\.undo\(',f)),'redo_calls':len(re.findall(r'\.redo\(',f)),'edit_calls':len(re.findall(r'\.(?:insert|delete|set|format|push|unshift|applyDelta)\(',f)),'assertion_count':len(assertions)}
 functions.append(row)
sel=next((x for x in functions if (x['undo_calls'] or x['redo_calls']) and x['edit_calls']>=2 and x['assertion_count']),None)
if sel:
 lines=clean.splitlines();view='\n'.join(f'{i+1:04d} {line}' for i,line in enumerate(lines) if sel['start_line']<=i+1<=sel['end_line'])+'\n';(OUT/'diagnostic-input-masked.txt').write_text(view)
r={'recorded_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':u,'sha':sha,'raw_sha256':hashlib.sha256(raw).hexdigest(),'mask_policy':'All comments, whole assertion calls and expected/snapshot assignments removed before model sees input. Mechanical raw fetch is not model display.','functions':functions,'selected':sel,'masked_spans':spans,'expected_states_model_displayed':False}
(OUT/'diagnostic-mask-receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'recorded_UTC':r['recorded_UTC'],'selected':sel,'function_metadata':functions},indent=2))
