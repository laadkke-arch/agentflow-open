"""Prepare only the pinned, checksum-verified local jq 1.7.1 executable."""
import datetime,hashlib,json,pathlib,subprocess,urllib.request
O=pathlib.Path(__file__).resolve().parent;C=O/'_cache';C.mkdir(exist_ok=True)
BASE='https://github.com/jqlang/jq/releases/download/jq-1.7.1/'
PINNED='5942c9b0934e510ee61eb3e30273f1b3fe2590df93933a93d7c58b81d19c8ff5'
rows=[]
for name in ['sha256sum.txt','jq-linux-amd64']:
 p=C/name;u=BASE+name
 if not p.exists():
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'AF-RES-096-reproduction'}),timeout=50) as r:p.write_bytes(r.read())
 rows.append({'asset':name,'url':u,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
line=next(x for x in (C/'sha256sum.txt').read_text().splitlines() if x.split()[-1]=='jq-linux-amd64')
actual=hashlib.sha256((C/'jq-linux-amd64').read_bytes()).hexdigest()
assert line.split()[0]==actual==PINNED, 'Pinned executable/checksum mismatch'
(C/'jq-linux-amd64').chmod(0o700)
v=subprocess.run([str(C/'jq-linux-amd64'),'--version'],capture_output=True,text=True,check=True)
assert v.stdout.strip()=='jq-1.7.1'
print(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checksum_matches':True,'version':v.stdout.strip(),'assets':rows},ensure_ascii=False,indent=2))
