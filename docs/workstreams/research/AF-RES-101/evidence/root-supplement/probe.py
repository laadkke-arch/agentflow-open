"""Small, bounded controls; historical question inputs/runtimes are not fabricated.

Run after evidence/imagemagick/acquire_proposals.py has created its ignored cache.
Only the two frozen answer revision-1 bodies supply shell text. No eval is used.
"""
from pathlib import Path
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache/root-supplement/probes"
CACHE.mkdir(parents=True, exist_ok=True)
started = dt.datetime.now(dt.timezone.utc).isoformat()
commands = []


def run(name, argv, **kwargs):
    at = dt.datetime.now(dt.timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=CACHE, capture_output=True, timeout=40, **kwargs)
    rec = {"id": name, "utc": at, "argv": argv, "cwd": "owned .cache/root-supplement/probes",
           "exit_code": p.returncode,
           "stdout": p.stdout.decode("utf-8", "replace"),
           "stderr": p.stderr.decode("utf-8", "replace")}
    commands.append(rec)
    return p


versions = {name: run("version-" + name, cmd).stdout.decode().splitlines()[0]
            for name, cmd in [("imagemagick", ["magick", "-version"]), ("bash", ["bash", "--version"])]}
pixels = [(128, 128, 128), (255, 0, 0), (0, 0, 255), (130, 128, 128), (0, 255, 0)]
data = b"P6\n5 1\n255\n" + bytes(c for pixel in pixels for c in pixel)
(CACHE / "input.ppm").write_bytes(data)
base = ["magick", "input.ppm"]
tail = ["-alpha", "off", "-compose", "CopyOpacity", "-composite"]
for name, group, threshold in [("grouped-percent", True, "15%"),
                                ("ungrouped-percent", False, "15%"),
                                ("grouped-raw15", True, "15")]:
    ops = ["+clone", "-colorspace", "HCL", "-channel", "G", "-separate", "+channel", "-threshold", threshold]
    args = base + (["("] + ops + [")"] if group else ops) + tail + [name + ".png"]
    p = run(name, args)
    # A literal failure is an observation, not a reason to repair the candidate.

rgba = {}
for name in ["grouped-percent", "ungrouped-percent", "grouped-raw15"]:
    if not (CACHE / (name + ".png")).exists():
        rgba[name] = {"no_output": True, "reason": "literal command failed; see command stderr"}
        continue
    p = subprocess.run(["magick", name + ".png", "-depth", "8", "rgba:-"], cwd=CACHE,
                       capture_output=True, check=True)
    rgba[name] = [list(p.stdout[i:i+4]) for i in range(0, len(p.stdout), 4)]
    commands.append({"id": "read-" + name, "argv": ["magick", name + ".png", "-depth", "8", "rgba:-"],
                     "utc": dt.datetime.now(dt.timezone.utc).isoformat(), "exit_code": 0,
                     "stdout_bytes_sha256": hashlib.sha256(p.stdout).hexdigest(), "decoded_rgba": rgba[name]})

events = json.loads((ROOT / ".cache/imagemagick/stage2/non-op-30day-projection.json").read_text())
selected = {e["post_id"]: e for e in events if e.get("revision_number") == 1 and e["case_id"] == "IM-A2"}
shell = {}
for post_id, block_index in [(77797032, 0), (77797051, 2)]:
    e = selected[post_id]
    blocks = [html.unescape(s) for s in re.findall(r"<pre><code>(.*?)</code></pre>", e["body"], re.S)]
    literal = blocks[block_index]
    filename = f"answer-{post_id}-rev1.sh"
    (CACHE / filename).write_text(literal)
    p = run("literal-syntax-" + str(post_id), ["bash", "-n", filename])
    shell[str(post_id)] = {"revision_url": e["revision_url"], "revision_guid": e["revision_guid"],
                          "body_sha256": e["body_sha256"], "code_block_1based": block_index + 1,
                          "literal_script_sha256": hashlib.sha256(literal.encode()).hexdigest(),
                          "bash_syntax_exit": p.returncode}

# Capture argv after the actual answer's string interpolation. This is not an
# ImageMagick execution or a claim about Cygwin's unknown shell settings.
capture = 'import json,os,sys;open(os.environ["AF_RES_ARGV"],"w").write(json.dumps(sys.argv[1:]))'
prefix = "num=1\nval=300\ninput_image=input.png\ncoords=('HEADER' '10x10+0+0' '10x10+10+0')\n"
prefix += "convert() { python -c '" + capture + "' \"$@\"; }\n"
literal = (CACHE / "answer-77797032-rev1.sh").read_text()
(CACHE / "capture-c1.sh").write_text(prefix + literal)
env = dict(os.environ, AF_RES_ARGV=str(CACHE / "captured-argv.json"))
p = run("c1-interpolation-argv-only", ["bash", "capture-c1.sh"], env=env)
argv = json.loads((CACHE / "captured-argv.json").read_text())
shell["77797032"]["captured_argv"] = argv
shell["77797032"]["literal_backslash_parenthesis_tokens"] = [s for s in argv if s in [r"\(", r"\)"]]
shell["77797032"]["literal_double_quote_tokens"] = [s for s in argv if '"' in s]

result = {"started_utc": started, "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
          "versions": versions, "original_runtime": "IM-A1 version unknown; IM-A2 7.0.10-61/Cygwin NOT executed",
          "input": {"kind": "researcher-created 5x1 PPM; not the question image", "rgb": pixels,
                    "sha256": hashlib.sha256(data).hexdigest()},
          "rgba": rgba, "shell": shell,
          "not_run": {"ruby": "ruby/gem executable absent; QuickMagick/RMagick/Open3 candidate runtime not executed",
                      "original_image": "original input bytes unavailable; synthetic controls establish only the stated behavior"},
          "commands": commands}
(OUT / "probe-receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"versions": versions, "rgba": rgba,
                  "syntax_exits": {k:v["bash_syntax_exit"] for k,v in shell.items()},
                  "c1_literal_backslash_parenthesis_tokens": shell["77797032"]["literal_backslash_parenthesis_tokens"],
                  "c1_literal_quote_tokens": shell["77797032"]["literal_double_quote_tokens"]}, ensure_ascii=False, indent=2))
