"""Assert equality on independently read container and accessor values."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
python = json.loads((root / "python-static.json").read_text())["entries"]
javascript = json.loads((root / "node-static.json").read_text())["entries"]
assert len(python) == len(javascript)
for a, b in zip(python, javascript, strict=True):
    for field in ("path", "bytes", "sha256", "glb", "geometry"):
        assert a[field] == b[field], (a["path"], field, a[field], b[field])
    print(f"equal {a['sha256']} {len(a['geometry'])} primitive(s) {a['path']}")
