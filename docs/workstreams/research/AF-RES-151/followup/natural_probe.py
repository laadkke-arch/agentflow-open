from pathlib import Path
import subprocess, tempfile, hashlib, json, os, platform, time
root=Path(__file__).resolve().parent
out={'platform':platform.platform(),'commands':[]}
def run(cwd,*args):
    t=time.monotonic(); p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=45,env={**os.environ,'GOPROXY':'off','GOTOOLCHAIN':'local','GO111MODULE':'off'});out['commands'].append({'cwd':str(cwd),'argv':args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'elapsed_s':round(time.monotonic()-t,3)});return p
with tempfile.TemporaryDirectory(dir=root) as d:
    p=Path(d);run(p,'git','--version');run(p,'git','init','-q','--object-format=sha1');seen={}
    for i in range(100000):
        b=f'AF151 {i}\n'.encode();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();k=h[:4]
        if k in seen:
            j,h1=seen[k];out['collision']={'prefix':k,'i':j,'j':i,'hashes':[h1,h]};break
        seen[k]=(i,h)
    for x in [j,i]:
        f=p/f'{x}.txt';f.write_text(f'AF151 {x}\n');run(p,'git','hash-object','-w',f.name)
    run(p,'git','rev-parse','--short=4',h1);run(p,'git','rev-parse','--short=4',h)
with tempfile.TemporaryDirectory(dir=root) as d:
    p=Path(d);run(p,'go','version');(p/'main.go').write_text('package main\nimport _ "embed"\nimport "fmt"\n//go:generate sh -c "exit 17"\n//go:embed hello.txt\nvar text string\nfunc main(){fmt.Println(text)}\n');(p/'hello.txt').write_text('AF151 local asset')
    run(p,'go','generate');run(p,'go','build','-o','probe','main.go');run(p,'./probe');(p/'hello.txt').unlink();run(p,'go','build','-o','missing','main.go')
(root/'receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
