"""Bounded falsifiers of frozen partial uses; never part of route scoring."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.metadata, inspect, json, shutil, subprocess, sys

P = Path(__file__).resolve().parent

def main():
    started = datetime.now(timezone.utc).isoformat()
    rows = []
    node = shutil.which('node')
    code = '''
const [a = null,b = null,c = null] = [10];
const [x,y] = [10,20,30];
const memory = new WebAssembly.Memory({initial:1,maximum:2});
const view = new DataView(memory.buffer);
view.setInt32(8,0x01020304,true);
const bytes = Array.from(new Uint8Array(memory.buffer,8,4));
const sameBuffer = view.buffer === memory.buffer;
let outOfBounds = null;
try {view.setInt32(memory.buffer.byteLength-2,1,true);}
catch(e) {outOfBounds=e.name;}
memory.grow(1);
let staleWrite = null;
try {view.setInt32(8,1,true);}catch(e) {staleWrite=e.name;}
console.log(JSON.stringify({node:process.version,padding:[a,b,c],truncation:[x,y],bytes,sameBuffer,outOfBounds,oldBufferBytes:view.buffer.byteLength,staleWrite}));
'''
    if node:
        r = subprocess.run([node,'-e',code],capture_output=True,text=True,timeout=20)
        rows.append({'id':'NC01-NC04-JS','command':[node,'-e',code],'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'limits':['Tests JavaScript semantics only; no Go binding or ABI offset is supplied.','The same Wasm-memory buffer is observed; no Go-generated module is executed.','Growing non-shared memory invalidates the earlier view; caller must refresh it.']})
    else:
        rows.append({'id':'NC01-NC04-JS','status':'unexecuted','reason':'Node not installed','next_command':'node -e <literal code in this script>'})
    try:
        import typing_extensions
        from typing import Annotated, get_args, get_type_hints
        Doc = typing_extensions.Doc
        first = '  first-name: keep spacing!\n'
        last = 'Last name (exact).'
        def subject(firstname: Annotated[str,Doc(first)], lastname: Annotated[str,Doc(last)]):
            """Preserved function docstring."""
            return firstname,lastname
        hints = get_type_hints(subject,include_extras=True)
        extracted = {k: [x.documentation for x in get_args(v)[1:] if isinstance(x,Doc)] for k,v in hints.items()}
        rows.append({'id':'Q07-SUPPLEMENTARY-DOC','package_version':importlib.metadata.version('typing_extensions'),'python':sys.version,'inputs':{'firstname':first,'lastname':last},'extracted':extracted,'strings_unchanged':extracted=={'firstname':[first],'lastname':[last]},'docstring':subject.__doc__,'constructor_sha256':hashlib.sha256(inspect.getsource(Doc).encode()).hexdigest(),'limits':['The installed 4.16.0 behavior is separate from the directly read official 4.15.0 source.','This is a post-seal missed-component probe and cannot fill empty A/B returns.','No editor adoption or full original typing.doc standard-library integration is established.']})
    except Exception as exc:
        rows.append({'id':'Q07-SUPPLEMENTARY-DOC','status':'error','exception':type(exc).__name__,'message':str(exc)})
    result={'stage':'post-route-seal supplementary falsification','started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'target_research_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'observations':rows,'route_success_effect':'none','new_installations':False}
    (P/'additional-runtime-probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
