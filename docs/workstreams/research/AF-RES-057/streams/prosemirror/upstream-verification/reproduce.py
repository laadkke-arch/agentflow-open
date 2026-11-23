from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import urllib.request

here = Path(__file__).resolve().parent
owned = here.parents[2]
cache = owned / ".cache" / "prosemirror" / "upstream-verification"
cache.mkdir(parents=True, exist_ok=True)
fixture = json.loads((here / "source-fixture.json").read_text())
for item in fixture["copies"]:
    request = urllib.request.Request(item["source_url"], headers={"User-Agent": "AF-RES-057-reproduce"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != item["sha256"]:
        raise RuntimeError("Fixed source hash mismatch: " + item["source_url"])
    target = cache / item["fixture_path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
for name in ["package.json", "package-lock.json"]:
    shutil.copyfile(here / name, cache / name)
for command in [
    ["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
    ["npm", "run", "prepare"],
    ["npm", "test", "--", "--grep", "^history enables undo$"]
]:
    print("COMMAND", json.dumps(command), "CWD", cache, flush=True)
    subprocess.run(command, cwd=cache, check=True)
