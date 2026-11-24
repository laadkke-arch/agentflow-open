"""Generate the three UTF-8 JSON representations from the sealed selection."""
import argparse
import base64
import hashlib
import json
import re
import struct
from pathlib import Path
from urllib.parse import unquote, urlsplit


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n").encode()


def read_json(path):
    return json.loads(Path(path).read_bytes())


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def window_sha256(parts):
    return sha256(b"".join(struct.pack(">Q", len(part)) + part for part in parts))


def github_pointer(url):
    parsed = urlsplit(url)
    pieces = unquote(parsed.path).strip("/").split("/")
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(pieces) < 5:
        raise ValueError("expected a pinned GitHub blob link")
    owner, repo, kind, revision, *path = pieces
    if kind != "blob" or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("expected a full Git commit in the link")
    if any(not piece or piece in {".", ".."} for piece in pieces):
        raise ValueError("invalid GitHub path")
    ranges = []
    if parsed.fragment:
        match = re.fullmatch(r"L([1-9]\d*)(?:-L([1-9]\d*))?", parsed.fragment)
        if match is None:
            raise ValueError("unsupported GitHub line locator")
        ranges.append([int(match[1]), int(match[2] or match[1])])
    return {"repo": f"{owner}/{repo}", "revision": revision, "path": "/".join(path), "line_ranges": ranges}


def mirror_key(pointer):
    return "/".join(pointer[key] for key in ("repo", "revision", "path"))


def verify_mirror(root, inputs):
    paths = [p for p in root.rglob("*") if p.is_file() or p.is_symlink()]
    existing = {p.relative_to(root).as_posix(): p for p in paths}
    expected = {record["path"]: record for record in inputs["mirror_manifest"]}
    if not expected or len(expected) != len(inputs["mirror_manifest"]) or existing.keys() != expected.keys():
        raise ValueError("mirror path inventory differs from inputs.json")
    for key, path in existing.items():
        if path.is_symlink():
            raise ValueError(f"unexpected symlink: {key}")
        data = path.read_bytes()
        record = expected[key]
        if len(data) != record["bytes"] or sha256(data) != record["sha256"]:
            raise ValueError(f"mirror bytes differ from inputs.json: {key}")
    return len(paths)


def make_bundle(case, raw):
    pointer = github_pointer(case["url"])
    if mirror_key(pointer) != case["mirror_key"] or sha256(raw) != case["full_file_sha256"]:
        raise ValueError(f"source mismatch for {case['case_id']}")
    parts = [raw[loc["start_byte"]:loc["end_byte"]] for loc in case["locator"]]
    if sum(map(len, parts)) != case["excerpt_bytes"] or window_sha256(parts) != case["excerpt_sha256"]:
        raise ValueError(f"excerpt mismatch for {case['case_id']}")
    a = {"url": case["url"], "sentence": case["sentence"]}
    b = {**a, "type": case["evidence_type"], "revision": case["revision"], "relative_path": case["path"],
         "excerpt_sha256": case["excerpt_sha256"]}
    c = {**b, "locator": case["locator"],
         "excerpt_base64": [base64.b64encode(part).decode("ascii") for part in parts]}
    return {"A": a, "B": b, "C": c}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("inputs", "gold", "mirror", "out"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    inputs, gold = read_json(args.inputs), read_json(args.gold)
    if inputs["dependency"]["commit"] != gold["dependency"]:
        raise ValueError("gold and input dependency differ")
    mirrored = verify_mirror(args.mirror, inputs)
    args.out.mkdir(parents=True, exist_ok=True)
    records = []
    for case in gold["cases"]:
        values = make_bundle(case, (args.mirror / case["mirror_key"]).read_bytes())
        for scheme, value in values.items():
            path = f"{case['case_id']}.{scheme}.json"
            data = json_bytes(value)
            (args.out / path).write_bytes(data)
            records.append({"case_id": case["case_id"], "scheme": scheme, "file": path,
                            "bytes": len(data), "sha256": sha256(data)})
    manifest = {"inputs_sha256": sha256(args.inputs.read_bytes()), "gold_sha256": sha256(args.gold.read_bytes()),
                "mirror_files_verified": mirrored, "packages": records}
    (args.out / "package-manifest.json").write_bytes(json_bytes(manifest))
    print(f"verified {mirrored} mirror files, wrote {len(records)} packages")


if __name__ == "__main__":
    main()
