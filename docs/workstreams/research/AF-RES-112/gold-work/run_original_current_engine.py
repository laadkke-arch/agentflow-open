"""Current installed engine only. Original historical engines are not installed here."""
import datetime,hashlib,json,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parent
version=subprocess.run(["godot","--version"],capture_output=True,text=True,check=True).stdout.strip()
rows=[]
for name,folder,scene in [("G2","G2/similar_resource",None),("G3-port4","G3-port4/ExportedEmbededResourcePropertyWontResetOnSceneReload","res://main.tscn")]:
    cwd=BASE/"examples"/folder
    inputs={str(f.relative_to(cwd)):hashlib.sha256(f.read_bytes()).hexdigest() for f in cwd.rglob("*") if f.is_file() and ".godot" not in f.parts and f.suffix in {".gd",".tres",".tscn",".godot"}}
    for action,tail in [("import",["--editor","--import","--quit"]),("run",["--quit-after","8"]+([scene] if scene else []))]:
        cmd=["godot","--headless","--path",str(cwd),*tail]
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            result=subprocess.run(cmd,capture_output=True,text=True,timeout=35)
            row={"check_id":name+"-"+action,"utc":start,"command":cmd,"version":version,"input_hashes":inputs,"exit_code":result.returncode,"stdout":result.stdout,"stderr":result.stderr}
        except subprocess.TimeoutExpired as exc:
            row={"check_id":name+"-"+action,"utc":start,"command":cmd,"version":version,"input_hashes":inputs,"exit_code":"timeout","stdout":str(exc.stdout),"stderr":str(exc.stderr)}
        rows.append(row)
(BASE/"examples"/"replayed-original-current-engine.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False,indent=2))
