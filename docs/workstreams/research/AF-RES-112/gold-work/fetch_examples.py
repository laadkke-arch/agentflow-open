"""Fetch only three preselected public original example archives; not a crawler."""
import datetime, hashlib, io, json, urllib.parse, urllib.request, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
INPUTS=[
 ("G2","https://github.com/godotengine/godot/files/7910066/similar_resource.zip","e016439485363faaff80376880e71c92b35d7bd390c7da0d5462ca9372f7f9ea"),
 ("G3","https://github.com/godotengine/godot/files/7944151/test.zip","7dfda91dcf0440abcc8769d86b884f69e86e681c935d0d2b1d899d8574da5734"),
 ("G3-port4","https://github.com/godotengine/godot/files/10096836/ExportedEmbededResourcePropertyWontResetOnSceneReload.zip","f93bef24f0439baab957ca975ea74d5b5c774ed05b0f7abd11d3979e5a7ad0ff"),
]
receipts=[]
for name,url,expected in INPUTS:
    with urllib.request.urlopen(url,timeout=45) as response:
        data=response.read()
        arrived=urllib.parse.urlsplit(response.url)._replace(query="").geturl()
        status=response.status
    actual=hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise RuntimeError(f"Input hash changed for {name}: {actual}; do not silently rerun a different input")
    files=[]
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            relative=Path(entry.filename)
            if relative.is_absolute() or ".." in relative.parts:
                raise RuntimeError("Unsafe archive member path")
            if not entry.filename.endswith((".gd",".tscn",".tres","project.godot")):
                continue
            if any(part in {".godot",".import"} for part in relative.parts):
                continue
            content=archive.read(entry)
            target=BASE/"examples"/name/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
            files.append({"path":entry.filename,"bytes":len(content),"sha256":hashlib.sha256(content).hexdigest()})
    receipts.append({"artifact_id":name,"original_url":url,"actual_arrival_url":arrived,"query_omitted":"ephemeral signed download query", "status":status,"sha256":actual,"bytes":len(data),"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"extracted_files":files})
(BASE/"examples"/"fetch-receipts.json").write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
print(json.dumps({"archives":len(receipts),"input_hashes_verified":True}))
