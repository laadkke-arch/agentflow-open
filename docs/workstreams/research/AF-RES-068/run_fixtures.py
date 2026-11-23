"""Install the three pinned npm distributions and run the four fixed series."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
CASES = ("A01", "A02", "L01", "L02")
FOAF = "http://xmlns.com/foaf/0.1/"


def utc():
    return datetime.now(timezone.utc).strftime("%FT%TZ")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def call(command, cwd, file, output):
    start = utc()
    p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    for name, content in (("stdout", p.stdout), ("stderr", p.stderr)):
        if content:
            (output / f"{file}.{name}").write_text(content, encoding="utf-8")
    return {"command": command, "cwd": str(cwd), "start_utc": start, "end_utc": utc(),
            "exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def install(pin, pkgdir, receipt_dir, use_locks):
    install_id = pin["package"] + "-" + pin["version"]
    pkgdir.mkdir()
    write_json(pkgdir / "package.json", {"private": True, "dependencies": {pin["package"]: pin["version"]}})
    receipt = {"package": pin["package"], "version": pin["version"], "pin": pin["pin"], "install_id": install_id}
    if use_locks:
        shutil.copyfile(use_locks / f"{install_id}-lock.json", pkgdir / "package-lock.json")
    else:
        receipt["lock"] = call(
            ["npm", "install", "--package-lock-only", "--ignore-scripts", "--no-audit", "--no-fund",
             "--registry=https://registry.npmjs.org", "--cache", str(pkgdir.parent / "npm-cache")],
            pkgdir, install_id + "-lock", receipt_dir)
        if receipt["lock"]["exit_code"]:
            return receipt, False
    lock = read_json(pkgdir / "package-lock.json")
    installed_record = lock["packages"]["node_modules/" + pin["package"]]
    receipt["lock_integrity"] = installed_record["integrity"]
    if installed_record["integrity"] != pin["dist"]["integrity"] or installed_record["resolved"] != pin["dist"]["tarball"]:
        receipt["error"] = "lock identity mismatches frozen npm metadata"
        return receipt, False
    try:
        with urlopen(pin["dist"]["tarball"], timeout=25) as r:
            payload = r.read()
        download = {"sha1": hashlib.sha1(payload).hexdigest(),
                    "integrity": "sha512-" + base64.b64encode(hashlib.sha512(payload).digest()).decode(),
                    "bytes": len(payload), "sha256": digest(payload)}
        receipt["download"] = download
        if download["sha1"] != pin["dist"]["shasum"] or download["integrity"] != pin["dist"]["integrity"]:
            receipt["error"] = "published tarball checksum mismatch"
            return receipt, False
    except OSError as error:
        receipt["error"] = str(error)
        return receipt, False
    shutil.copyfile(pkgdir / "package-lock.json", receipt_dir / f"{install_id}-lock.json")
    receipt["ci"] = call(
        ["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund",
         "--registry=https://registry.npmjs.org", "--cache", str(pkgdir.parent / "npm-cache")],
        pkgdir, install_id + "-ci", receipt_dir)
    receipt["package_json_version"] = (
        read_json(pkgdir / "node_modules" / pin["package"] / "package.json")["version"]
        if receipt["ci"]["exit_code"] == 0 else None)
    receipt["package_json_sha256"] = (
        digest((pkgdir / "node_modules" / pin["package"] / "package.json").read_bytes())
        if receipt["ci"]["exit_code"] == 0 else None)
    return receipt, receipt["ci"]["exit_code"] == 0 and receipt["package_json_version"] == pin["version"]


def dataset_values(dataset, predicate):
    return sorted([[q["object"]["termType"], q["object"]["value"]] for q in dataset
                   if q["predicate"]["value"] == predicate])


def match(fixture, arm, truth):
    expected = arm["expectation"]
    kind = fixture["kind"]
    observed = truth["observed"]
    if kind.startswith("ajv"):
        test = {"unchanged": observed["unchanged"] == expected["unchanged"]}
        if "compile_error_contains" in expected:
            test["strict_compile"] = expected["compile_error_contains"] in observed.get("error", "")
        else:
            test["valid"] = observed.get("valid") == expected["valid"]
        if "keyword" in expected:
            test["keyword"] = expected["keyword"] in {x["keyword"] for x in observed.get("errors") or []}
        return test
    if kind == "rdf":
        data = observed["dataset"]
        objects = dataset_values(data, expected["predicate"])
        test = {"objects": objects == expected["objects"], "quad_count": len(data) == expected["quad_count"],
                "unchanged": observed["unchanged"] == expected["unchanged"]}
        if "extra_predicate" in expected:
            test["extra"] = dataset_values(data, expected["extra_predicate"]) == expected["extra_objects"]
        if "reported_counterexample" in expected:
            test["matches_author_report_diagnostic"] = objects == expected["reported_counterexample"]
        return test
    data = observed["output"]
    given_key = "givenName" if "givenName" in data else FOAF + "givenName"
    family_key = "familyName" if "familyName" in data else FOAF + "familyName"
    return {"given_key": given_key == expected["given_key"], "family_key": family_key == expected["family_key"],
            "given": data.get(given_key) == expected["given"], "family": data.get(family_key) == expected["family"],
            "id": data.get("@id") == expected["id"], "mbox": data.get("mbox") == expected["mbox"],
            "unchanged": observed["unchanged"] == expected["unchanged"],
            "context_unchanged": observed["context_unchanged"]}


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--scratch", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--case", choices=CASES, action="append")
    cli.add_argument("--node", default="node", help="Node binary used by the fixture, separate from npm installer")
    cli.add_argument("--locks", type=Path, help="Optional original official npm dependency lock directory")
    args = cli.parse_args()
    scratch = args.scratch.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    runtime = output / "runtime"
    runtime.mkdir()
    pins = read_json(ROOT / "evidence/pins.json")
    seal = read_json(ROOT / "evidence/doc-seal.json")
    for name, sha in seal["files_sha256"].items():
        if digest((ROOT / name).read_bytes()) != sha:
            raise ValueError(f"Pre-run seal changed: {name}")
    receipts, pkgs, rows = [], {}, []
    for case in CASES:
        if args.case and case not in args.case:
            continue
        fixture_path = ROOT / "fixtures" / f"{case}.json"
        fixture = read_json(fixture_path)
        package = fixture["package"] + "@" + fixture["version"]
        pin = pins[package]
        if package not in pkgs:
            pkgdir = scratch / (pin["package"] + "-" + pin["version"])
            rec, ok = install(pin, pkgdir, runtime, args.locks)
            pkgs[package] = rec, ok, pkgdir
            receipts.append(rec)
        receipt, ok, pkgdir = pkgs[package]
        for arm in fixture["groups"]:
            group = arm["group"]
            row = {"case": case, "group": group, "variant": arm["variant"], "package": package,
                   "pin": pin["pin"], "input_location": "fixtures/" + fixture_path.name,
                   "fixture_sha256": digest(fixture_path.read_bytes()),
                   "input_sha256": digest(json.dumps(arm["input"], ensure_ascii=False, sort_keys=True,
                                                     separators=(",", ":")).encode()),
                   "options": arm["input"]["options"], "expectation": arm["expectation"],
                   "document_prediction": fixture["document_prediction"], "install_id": receipt["install_id"]}
            log = case + "-" + group
            if not ok:
                row.update(status="미실시", reason="frozen npm install failed", exit_code=None, stdout="", stderr="")
            else:
                result = call([args.node, str(ROOT / "fixtures/probe.cjs"), str(pkgdir), str(fixture_path), group],
                              scratch, log, runtime)
                row.update(result, status="ran", output_location=f"evidence/runtime/{log}.stdout")
                if result["exit_code"] == 0:
                    try:
                        row["observed"] = json.loads(result["stdout"])
                        row["checks"] = match(fixture, arm, row["observed"])
                        row["meets_expected"] = all(v for k, v in row["checks"].items()
                                                   if not k.endswith("_diagnostic"))
                    except (json.JSONDecodeError, KeyError, TypeError) as error:
                        row.update(status="parse_failed", reason=str(error))
                else:
                    row.update(status="process_failed", error_location=f"evidence/runtime/{log}.stderr")
            rows.append(row)
    node = subprocess.check_output([args.node, "-v"], text=True).strip()
    install_node = subprocess.check_output(["node", "-v"], text=True).strip()
    npm = subprocess.check_output(["npm", "-v"], text=True).strip()
    write_json(runtime / "package-identity.json", {"node": node, "installer_node": install_node, "npm": npm, "receipts": receipts})
    (output / "runs.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    for r in rows:
        print(r["case"],r["group"],r["status"],r["exit_code"],r.get("observed",{}).get("observed",{}).get("phase"),
              r.get("checks"), flush=True)


if __name__ == "__main__":
    main()
