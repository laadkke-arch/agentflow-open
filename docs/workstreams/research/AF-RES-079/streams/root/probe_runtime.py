"""Small current-environment controls; these are not historical paired runs."""
import datetime
import hashlib
import importlib
import importlib.util
import io
import json
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = []

def record(case, name, call, expected):
    try:
        value = call()
        outcome = {"value": value, "exception": None}
    except Exception as exc:
        outcome = {"value": None, "exception": type(exc).__name__, "message": str(exc)}
    rows.append({"run_id": name, "event_id": case, "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 "actor": "root", "location": "ChatGPT cloud Linux sandbox",
                 "python": sys.version, "platform": platform.platform(),
                 "run_kind": "current_environment_only", "historical_pair_executed": False,
                 "expected": expected, "actual": outcome})

record("C03", "C03-runtime-import-imp", lambda: importlib.import_module("imp").__name__, "ModuleNotFoundError in Python>=3.12")
record("C03", "C03-runtime-find-spec", lambda: {"type": type(importlib.util.find_spec("json")).__name__, "name": importlib.util.find_spec("json").name}, "ModuleSpec, not the old file/path/description tuple")
record("C03", "C03-runtime-missing-spec", lambda: importlib.util.find_spec("_af079_no_such_module_20261123"), "None for absent module; old imp.find_module documentation specifies ImportError")

def png_round_trip():
    import PIL
    from PIL import Image
    image = Image.new("RGB", (2, 1))
    image.putdata([(255, 0, 0), (0, 255, 0)])
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    raw = buffer.getvalue()
    reopened = Image.open(io.BytesIO(raw))
    return {"pillow_version": PIL.__version__, "mode": reopened.mode,
            "size": list(reopened.size), "pixels": list(reopened.getdata()),
            "png_sha256": hashlib.sha256(raw).hexdigest()}

record("C02", "C02-runtime-png", png_round_trip, "RGB 2x1 and two ordered pixel triples")
record("C02", "C02-runtime-old-top-level-import", lambda: importlib.import_module("Image").__name__, "No Image top-level module in the current Pillow environment")

def invalid_image():
    from PIL import Image
    return Image.open(io.BytesIO(b"not an image")).format

record("C02", "C02-runtime-invalid-image", invalid_image, "UnidentifiedImageError; not an assertion about PIL1.1.7's exact exception class")
(ROOT / "runtime-observations.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
print(json.dumps({"rows": len(rows), "all_inputs_local_public": True, "historical_pair_runs": 0, "output": "runtime-observations.jsonl"}))
