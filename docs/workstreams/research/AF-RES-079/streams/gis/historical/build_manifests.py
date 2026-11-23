"""Collect only task-local installed package provenance and binary capabilities."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
environments = {}
for environment in sorted((ROOT / "envs").glob("gdal*")):
    rows = []
    for metadata in sorted((environment / "conda-meta").glob("*.json")):
        package = json.loads(metadata.read_text())
        rows.append({key: package.get(key) for key in
                     ("name", "version", "build", "build_number", "subdir", "url",
                      "fn", "sha256", "md5", "depends")})
    environments[environment.name] = rows
    lines = ["# Task-local environment provenance; current conda-forge artifacts", "@EXPLICIT"]
    for package in rows:
        if package["url"]:
            lines.append(package["url"] + "#" + (package["md5"] or ""))
    (ROOT / (environment.name + "-explicit.txt")).write_text("\n".join(lines) + "\n")
record = {"actor": "gis_evidence tool agent", "checked_utc":
          datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "scope": "Binary rebuilds and dependencies are part of the observed condition; not release-day official binary validation or GDAL-only causal isolation.",
          "environments": environments}
(ROOT / "environment-packages.json").write_text(json.dumps(record, indent=2) + "\n")
print({name: len(packages) for name, packages in environments.items()})
