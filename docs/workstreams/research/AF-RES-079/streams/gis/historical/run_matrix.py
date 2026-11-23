"""Replay the sealed GIS inputs in task-local historical GDAL environments."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("phase", choices=["g03", "g04", "arg"])
args = parser.parse_args()
planned = []


def plan(label, version, *arguments):
    short = version.replace(".", "")[:2]
    if args.phase == "g03" and version == "3.8.0":
        short = "38a10"
    command = ["cache/bin/micromamba", "--no-rc", "run", "-p", "envs/gdal" + short,
               "python", "../replay_gis.py", "--expected-version", version] + list(arguments)
    planned.append((label, command))


if args.phase == "g03":
    for version in ["3.7.0", "3.8.0"]:
        plan("env-" + version, version, "env")
    plan("g03-old-write", "3.7.0", "write-vector", "--fixture", "../inputs/vector.json",
         "--output", "runs/g03-old.parquet")
    for version, label in [("3.7.0", "g03-p1-old"), ("3.8.0", "g03-p1-new")]:
        plan(label, version, "inspect-vector", "--input", "runs/g03-old.parquet", "--driver", "Parquet")
    plan("g03-new-write", "3.8.0", "write-vector", "--fixture", "../inputs/vector.json",
         "--output", "runs/g03-new.parquet")
    plan("g03-p2-old-consumer", "3.7.0", "inspect-vector", "--input", "runs/g03-new.parquet", "--driver", "Parquet")
    for version in ["3.7.0", "3.8.0"]:
        plan("g03-invalid-compression-" + version, version, "write-vector", "--fixture",
             "../inputs/vector.json", "--output", "runs/invalid-compression-" + version + ".parquet",
             "--compression", "invalid")
        plan("g03-invalid-point-m-" + version, version, "write-vector", "--fixture",
             "../inputs/vector.json", "--output", "runs/invalid-point-m-" + version + ".parquet",
             "--point-m")
elif args.phase == "g04":
    plan("env-3.9.0", "3.9.0", "env")
    for label, version, encoding in [("old", "3.8.0", "GEOARROW"),
                                     ("new-same-name", "3.9.0", "GEOARROW"),
                                     ("new-alias", "3.9.0", "GEOARROW_INTERLEAVED")]:
        plan("g04-" + label + "-write", version, "write-vector", "--fixture",
             "../inputs/point-boundary.json", "--output", "runs/g04-" + label + ".parquet",
             "--encoding", encoding)
    for label, version, source in [("old-read", "3.8.0", "old"),
                                   ("new-reads-old", "3.9.0", "old"),
                                   ("old-reads-new-name", "3.8.0", "new-same-name"),
                                   ("old-reads-alias", "3.8.0", "new-alias"),
                                   ("new-reads-new-name", "3.9.0", "new-same-name"),
                                   ("new-reads-alias", "3.9.0", "new-alias")]:
        plan("g04-" + label, version, "inspect-vector", "--input",
             "runs/g04-" + source + ".parquet", "--driver", "Parquet")
    for version in ["3.8.0", "3.9.0"]:
        plan("g04-p1-wkb-" + version, version, "inspect-vector", "--input",
             "runs/g03-new.parquet", "--driver", "Parquet")
else:
    import struct
    (ROOT / "runs/arg-input").mkdir(parents=True, exist_ok=True)
    for name, values in [("sealed", [1, 2, 3, -9999]),
                         ("supplier-int16", [-32768, 2, -3, -4])]:
        (ROOT / ("runs/arg-input/" + name + ".arg")).write_bytes(struct.pack(">4h", *values))
        metadata = {"layer": name, "type": "arg", "datatype": "int16", "xmin": 0,
                    "ymin": 0, "xmax": 2, "ymax": 2, "cellwidth": 1, "cellheight": 1,
                    "rows": 2, "cols": 2}
        if name == "sealed":
            metadata["epsg"] = 4326
        (ROOT / ("runs/arg-input/" + name + ".json")).write_text(json.dumps(metadata))
    for version in ["3.7.0", "3.8.0", "3.9.0"]:
        plan("arg-default-" + version, version, "inspect-raster", "--input",
             "runs/arg-input/sealed.arg", "--driver", "ARG")
    plan("arg-opt-in-3.8.0", "3.8.0", "--arg-opt-in", "inspect-raster", "--input",
         "runs/arg-input/sealed.arg", "--driver", "ARG")
    plan("arg-sentinel-3.8.0", "3.8.0", "--arg-opt-in", "inspect-raster", "--input",
         "runs/arg-input/supplier-int16.arg", "--driver", "ARG")
    plan("arg-write-3.8.0", "3.8.0", "--arg-opt-in", "write-raster", "--output", "runs/new.arg")
    plan("arg-old-consumer", "3.7.0", "inspect-raster", "--input", "runs/new.arg", "--driver", "ARG")
    plan("arg-invalid-bands", "3.8.0", "--arg-opt-in", "write-raster", "--output",
         "runs/invalid-bands.arg", "--bands", "2")

result = []
for label, command in planned:
    process = subprocess.run([sys.executable, str(ROOT / "run_recorded.py"), label, "--"] + command,
                             cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    result.append({"label": label, "exit_code": process.returncode,
                   "receipt": label + ".json", "raw_output": label + ".log"})
    print(label, "exit", process.returncode, flush=True)
summary = {"phase": args.phase, "actor": "gis_evidence tool agent",
           "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "fixed_input_sha256": {str(path.relative_to(ROOT.parent)):
               hashlib.sha256(path.read_bytes()).hexdigest()
               for path in (ROOT.parent / "inputs").glob("*.json")},
           "runs": result,
           "note": "Nonzero exits include expected rejection probes; inspect each raw JSON before judging."}
(ROOT / ("matrix-" + args.phase + ".json")).write_text(json.dumps(summary, indent=2) + "\n")
