"""AF-RES-112 supplemental current-engine checks, not historical-version replications.
Inputs are downloaded original examples, see original-artifact-receipts.json.
Run from this directory after materializing examples with fetch_examples.py.
"""
import datetime, hashlib, json, re, shutil, subprocess
from pathlib import Path
B = Path(__file__).resolve().parent
R = B / "examples" / "controlled"
R.mkdir(parents=True, exist_ok=True)
records=[]
ACTUAL_VERSION=subprocess.run(["godot","--version"],capture_output=True,text=True,check=True).stdout.strip()
def run(case, cwd, args):
    cmd=["godot", "--headless", "--path", str(cwd), *args]
    hashes={str(p.relative_to(cwd)):hashlib.sha256(p.read_bytes()).hexdigest() for p in cwd.rglob("*") if p.is_file() and ".godot" not in p.parts and p.suffix in {".gd", ".tscn", ".tres", ".godot"}}
    row={"check_id":case,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"environment":"provided Linux; installed Godot " + ACTUAL_VERSION, "command":cmd,"input_hashes":hashes}
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
        row.update(exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
    except subprocess.TimeoutExpired as e:
        row.update(exit_code="timeout",stdout=str(e.stdout),stderr=str(e.stderr))
    records.append(row)
    print(json.dumps(row,ensure_ascii=False),flush=True)
# The original G2 Number/Sum project and frozen values are retained except explicit treatments.
for mode in ["all_ones_same_uid", "distinct_paths_no_uid"]:
    dest=R / ("G2_"+mode)
    shutil.copytree(B/"examples/G2/similar_resource",dest,ignore=shutil.ignore_patterns(".godot", "*.uid"),dirs_exist_ok=True)
    for f in dest.glob("*.tres"):
        text=f.read_text()
        if mode == "all_ones_same_uid":
            text=re.sub(r"value = [23]", "value = 1", text)
        else:
            text=re.sub(r' uid="uid://[^"]+"', '', text)
        f.write_text(text)
    if mode == "all_ones_same_uid":
        f=dest/"test.gd";f.write_text(f.read_text().replace("1 + 1 + 2 + 3", "1 + 1 + 1 + 1"))
    run("G2_"+mode+"_import",dest,["--editor","--import","--quit"])
    run("G2_"+mode+"_run",dest,["--quit-after","8"])
# This is the author's later Godot-4 attachment, not the original Godot-3 link.
dest=R/"G3_port4_local_false"
shutil.copytree(B/"examples/G3-port4/ExportedEmbededResourcePropertyWontResetOnSceneReload",dest,ignore=shutil.ignore_patterns(".godot", "*.uid"),dirs_exist_ok=True)
f=dest/"main.tscn";f.write_text(f.read_text().replace("resource_local_to_scene = true", "resource_local_to_scene = false"))
run("G3_port4_local_false_import",dest,["--editor","--import","--quit"])
run("G3_port4_local_false_run",dest,["--quit-after","8","res://main.tscn"])
# Small constructed G1 resource-lifetime distinction. No claim of executing Godot 3.4.2.
dest=R/"G1_constructed";dest.mkdir(exist_ok=True)
(dest/"project.godot").write_text('config_version=5\n[application]\nconfig/name="AF112-G1-constructed"\n')
for name,local in [("shared",False),("local",True),("dynamic",False)]:
    (dest/(name+".tscn")).write_text('[gd_scene load_steps=2 format=3]\n\n[sub_resource type="Curve2D" id="curve"]\nresource_local_to_scene = '+str(local).lower()+'\n\n[node name="Path" type="Path2D"]\ncurve = SubResource("curve")\n')
(dest/"check.gd").write_text('''extends SceneTree
const SHARED = preload("res://shared.tscn")
const LOCAL = preload("res://local.tscn")
func _init():
    call_deferred("check")
func check():
    var mode = OS.get_cmdline_user_args()[0]
    var held = null
    var packed = null
    if mode == "preload_shared": packed = SHARED
    elif mode == "preload_local": packed = LOCAL
    else: packed = load("res://dynamic.tscn")
    if mode == "load_held": held = packed
    var first = packed.instantiate()
    root.add_child(first)
    var before = first.curve.get_point_count()
    first.curve.add_point(Vector2(1, 2))
    first.queue_free()
    first = null
    packed = null
    await process_frame
    await process_frame
    if mode == "preload_shared": packed = SHARED
    elif mode == "preload_local": packed = LOCAL
    else: packed = load("res://dynamic.tscn")
    var second = packed.instantiate()
    root.add_child(second)
    print(JSON.stringify({"mode":mode,"initial_points":before,"new_instance_points":second.curve.get_point_count(),"local_to_scene":second.curve.resource_local_to_scene,"held_reference":held != null}))
    second.queue_free()
    quit()
''')
for mode in ["load_released", "preload_shared", "preload_local", "load_held"]:
    run("G1_constructed_"+mode,dest,["--script","res://check.gd","--",mode])
(B/"examples"/"replayed-controlled-current-engine.json").write_text(json.dumps(records,ensure_ascii=False,indent=2))
