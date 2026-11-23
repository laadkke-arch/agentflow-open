"""Fetch four pinned D3 source files for provenance comparison, not a test oracle."""
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = "156712c8c3285d77cb487e1685c5adafcd0394a4"
FILES = {
    "manyBody.js": "edf38785ee810d47df5cc58dd1fdb626b3aa99e891c7266b73ea334614386186",
    "simulation.js": "08f83028ea58a5de3f98c9d57eeebc1fed2fda1b129098d0a68e318ba2cdc0dc",
    "jiggle.js": "26641b82cae7d49d6eb865c4d9b66a6af2eb3021705a0b80af737a4883cc494a",
    "lcg.js": "7e1aaa1836a35ab82c6153c88342b3e61933336d4f6b1e55e82fda13ac23e5df",
}
(ROOT / "cache").mkdir(exist_ok=True)
for name, expected in FILES.items():
    url = f"https://raw.githubusercontent.com/d3/d3-force/{COMMIT}/src/{name}"
    with urllib.request.urlopen(url, timeout=40) as response:
        data = response.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise RuntimeError(f"Pinned source hash mismatch for {name}: {digest}")
    (ROOT / "cache" / ("d3-src__" + name)).write_bytes(data)
    print(name, digest)
