import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
cases = [
    ("g03-p1-old", "gdal37", "3.7.0", "g03-old"),
    ("g03-p1-new", "gdal38a10", "3.8.0", "g03-old"),
    ("g03-p2-old-consumer", "gdal37", "3.7.0", "g03-new"),
    ("g04-p1-old", "gdal38", "3.8.0", "g03-new"),
    ("g04-p1-new", "gdal39", "3.9.0", "g03-new"),
    ("g04-old-encoding", "gdal38", "3.8.0", "g04-old"),
    ("g04-new-name-old-consumer", "gdal38", "3.8.0", "g04-new-same-name"),
    ("g04-new-name-new-consumer", "gdal39", "3.9.0", "g04-new-same-name"),
    ("g04-alias-old-consumer", "gdal38", "3.8.0", "g04-new-alias"),
    ("g04-alias-new-consumer", "gdal39", "3.9.0", "g04-new-alias"),
]
rows = []
for label, environment, version, file in cases:
    command = [sys.executable, str(ROOT / "run_recorded.py"), "contract-" + label, "--",
               "cache/bin/micromamba", "--no-rc", "run", "-p", "envs/" + environment,
               "python", "contract_details.py", "--expected-version", version,
               "--input", "runs/" + file + ".parquet"]
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rows.append({"label": label, "receipt": "contract-" + label + ".json",
                 "raw_output": "contract-" + label + ".log", "exit_code": result.returncode})
    print(label, "exit", result.returncode, flush=True)
(ROOT / "matrix-contract.json").write_text(json.dumps(rows, indent=2) + "\n")
