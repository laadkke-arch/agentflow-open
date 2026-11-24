"""Replay the upstream PR #334 array-p examples outside the frozen scalar population."""
import argparse
import json
import subprocess
from pathlib import Path

from common import ROOT, json_in, utc, write_json

INPUT = [500, 468, 454, 469]
VECTORS = [[0.25, 0.5, 0.75], [0.05, 0.25, 0.5, 0.75, 0.95]]
SCRIPT = """
const s = require("simple-statistics");
const [original, vectors] = JSON.parse(process.argv[1]);
function encode(value) {
    if (Array.isArray(value)) return Array.from({length: value.length}, (_, i) =>
        Object.hasOwn(value, i) ? encode(value[i]) : {type: "hole"});
    if (value === undefined) return {type: "undefined"};
    if (typeof value === "number" && !Number.isFinite(value)) return {type: "number", value: String(value)};
    if (value === null) return {type: "null"};
    return value;
}
const panels = vectors.map(p => {
    const a = original.slice();
    try { return {p, result: encode(s.quantile(a, p)), before: original, after: a}; }
    catch (error) { return {p, error: {name: error.name, code: error.code ?? null, message: error.message}, before: original, after: a}; }
});
process.stdout.write(JSON.stringify({loaded: require.resolve("simple-statistics"), panels}));
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence/posthoc-array-p.json")
    args = parser.parse_args()
    versions = json_in(ROOT / "evidence/roster.json")["published_order"]
    data = []
    for version in versions:
        observations = []
        for folder in (args.first, args.second):
            when = utc()
            result = subprocess.run(["node", "-e", SCRIPT, json.dumps([INPUT, VECTORS])],
                                    cwd=folder / version, capture_output=True, text=True, timeout=12, check=True)
            observations.append(json.loads(result.stdout) | {"observed_utc": when, "stderr": result.stderr})
        data.append({"version": version, "agree": observations[0]["panels"] == observations[1]["panels"],
                     "observations": observations})
    changed = [(left["version"], right["version"]) for left, right in zip(data, data[1:])
               if left["observations"][0]["panels"] != right["observations"][0]["panels"]]
    write_json(args.output, {"scope": "post hoc only; no changes to scalar-p analysis",
               "upstream": "https://github.com/simple-statistics/simple-statistics/pull/334",
               "input": INPUT, "vectors": VECTORS, "releases": data, "publish_transitions": changed})
    print("Array-p transitions after the primary freeze:", changed)


if __name__ == "__main__":
    main()
