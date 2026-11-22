import urllib.request,json,datetime,pathlib,email,email.policy,re,concurrent.futures,sys
P=pathlib.Path(__file__).resolve().parent

def fetch(month):
 u=f'https://mail-archives.apache.org/mod_mbox/arrow-dev/{month}.mbox'
 p=P/'cache'/f'{month}.mbox'
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  if p.exists():b=p.read_bytes()
  else:
   with urllib.request.urlopen(u,timeout=45) as r:b=r.read()
   p.write_bytes(b)
  messages=re.split(br'(?m)^From (?=dev-return-)',b)[1:]
  rows=[]
  for ix,m in enumerate(messages):
   m=m[m.index(b'\n')+1:]
   e=email.message_from_bytes(m,policy=email.policy.default)
   s=str(e.get('Subject',''))
   if not re.match(r'(?i)\s*re:',s) and not e.get('In-Reply-To'):
    rows.append({'subject':s,'date':str(e.get('Date','')),'message_id':str(e.get('Message-ID','')),'ordinal':ix+1})
  out={'url':u,'utc':t,'messages':len(messages),'headers':rows}
  (P/f'mail-{month}-metadata.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
  return {'month':month,'messages':len(messages),'headers':rows}
 except Exception as e:return {'month':month,'url':u,'utc':t,'error':str(e)}
if __name__=='__main__':
 for result in concurrent.futures.ThreadPoolExecutor(4).map(fetch,sys.argv[1:]):print(json.dumps(result,ensure_ascii=False))
