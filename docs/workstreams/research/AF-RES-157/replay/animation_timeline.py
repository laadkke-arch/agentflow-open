"""Read Blender sequence metadata without evaluating or rendering external assets."""
import json
from pathlib import Path
import bpy

scene = bpy.context.scene
sequence_editor = scene.sequence_editor
if sequence_editor is None:
    raise ValueError("active scene has no video sequence")
strips = getattr(sequence_editor, "strips", None)
if strips is None:
    strips = sequence_editor.sequences
result = {
    "fps": scene.render.fps,
    "fps_base": scene.render.fps_base,
    "scene_start_frame": scene.frame_start,
    "scene_end_frame": scene.frame_end,
    "strips": [],
}
for sequence in strips:
    payload = getattr(sequence, "filepath", "")
    result["strips"].append({
        "name": sequence.name,
        "type": sequence.type,
        "channel": sequence.channel,
        "start_frame": int(sequence.frame_final_start),
        "end_frame_exclusive": int(sequence.frame_final_end),
        "source_file": Path(payload).name if payload else "",
        "muted": bool(sequence.mute),
    })
result["strips"].sort(key=lambda s: (s["start_frame"], s["channel"], s["name"]))
print("TIMELINE_JSON " + json.dumps(result, sort_keys=True, ensure_ascii=False))
