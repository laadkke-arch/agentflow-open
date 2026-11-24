import csv, io, json, subprocess, hashlib, platform, tempfile, pathlib, sys

def emit(name, inp, result):
    s=json.dumps(inp, ensure_ascii=False, sort_keys=True)
    print(json.dumps({'case':name,'input':inp,'input_sha256':hashlib.sha256(s.encode()).hexdigest(),'result':result},ensure_ascii=False,sort_keys=True))
def jq(name,args,stdin):
    p=subprocess.run(['jq',*args],input=stdin,text=True,capture_output=True)
    emit(name,{'argv':['jq',*args],'stdin':stdin},{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
print(json.dumps({'python':sys.version,'platform':platform.platform(),'jq':subprocess.check_output(['jq','--version'],text=True).strip()}))
records=json.dumps([{'id':'1','userId':'fa51531d'},{'id':'2','userId':'a167869a'}])
jq('J1-original',['-n','--stream','fromstream(1|truncate_stream(inputs)) | INDEX(.id)'],records)
jq('J1-two-arg',['-n','--stream','INDEX(fromstream(1|truncate_stream(inputs)); .id)'],records)
jq('J1-duplicate',['-n','--stream','INDEX(fromstream(1|truncate_stream(inputs)); .id)'],json.dumps([{'id':'1','v':1},{'id':'1','v':2}]))
yaml_string='apiVersion: v1\nkind: Namespace\nmetadata:\n  name: test\n'
jq('J2-JSON-not-YAML',['map(fromjson)'],json.dumps({'stuff.yaml':yaml_string}))
jq('J2-builtin',['-n','builtins | map(select(startswith("fromyaml/")))'], '')
try:
    import yaml
    emit('J2-external-safe-parser',yaml_string,{'version':yaml.__version__,'json_compatible':yaml.safe_load(yaml_string)})
except ImportError as e:
    emit('J2-external-safe-parser',yaml_string,{'unavailable':str(e)})
lines='not a cd cmd\ncd /ok\n'
jq('J3-original',['-nR','inputs|gsub("^(?!cd ).*$|^cd "; "")'],lines)
jq('J3-conditional',['-nR','inputs|if startswith("cd ") then .[3:] else "" end'],lines+'cd \ncd /a b\n')
for tail in ('','\r\n'):
    initial='a,b\r\n1,2'+tail
    with tempfile.TemporaryDirectory() as tmp:
        f=pathlib.Path(tmp)/'data.csv'; f.write_bytes(initial.encode())
        with f.open('a',newline='',encoding='utf-8') as w: csv.DictWriter(w,fieldnames=['a','b']).writerow({'a':'3','b':'4'})
        out=f.read_bytes().decode(); emit('P1-append',initial,{'after':out,'rows':list(csv.reader(io.StringIO(out,newline='')))})
for content in ['SEP=;\nHeader_Col1;Header_Col2;Header_Col3\nRow1_Col1;Row1_Col2;Row1_Col3\n','SEP=;\nordinary;value\n']:
    f=io.StringIO(content,newline=''); raw=list(csv.DictReader(f,delimiter=';')); f.seek(0); directive=next(f).rstrip('\r\n'); out=list(csv.DictReader(f,delimiter=directive[-1]))
    # second input intentionally ambiguous, not a claim of safe detection
    emit('P2-skip-vs-raw',content,{'raw_pairs':[list(r.items()) for r in raw],'explicit_skip':out})
for content in ['a,b,c\n1,,3\n','a,b,b\n1,,3\n','a,b,c\n1,\n\n','a,b,c\n1,,\n']:
    d=csv.DictReader(io.StringIO(content,newline='')); fieldnames=d.fieldnames; out=list(d); emit('P3-distinct-duplicate-short',content,{'header':fieldnames,'positional':list(csv.reader(io.StringIO(content,newline=''))),'dicts':out,'dict_lengths':[len(r) for r in out]})
