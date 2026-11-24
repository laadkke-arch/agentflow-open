"""Acquire pinned inputs, inspect six traineddata files, or replay component receipts."""

import argparse
from pathlib import Path
import re
import subprocess
import tempfile

from evidence import (
    PINS, capture, environment, matches_model, model_identity, read_jsonl,
    require_identity, tool, write_csv, write_jsonl,
)

LEGACY = ("unicharset", "inttemp", "pffmtable", "normproto")
LSTM = ("lstm", "lstm-unicharset", "lstm-recoder")
COMPONENT = re.compile(
    r"^(\d+):([\w-]+):size=(\d+), offset=(\d+)$", re.MULTILINE
)
NETWORK = re.compile(r"^LSTM: network=(.+), int_mode=([01]), recoding=([01]), (.+)$", re.MULTILINE)


def acquire(root):
    root.mkdir(parents=True, exist_ok=True)
    downloads = [
        (root / pin["asset_path"], pin["download_url"], pin) for pin in PINS["models"]
    ]
    downloads += [(root / pin["path"], pin["url"], pin) for pin in PINS["engine"]["packages"]]
    downloads += [(root / pin["path"], pin["download_url"], pin) for pin in PINS["hunspell"]["pair"]]
    for target, url, pin in downloads:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            with tempfile.TemporaryDirectory(dir=target.parent) as scratch:
                received = Path(scratch) / "download"
                subprocess.run(
                    ["curl", "--fail", "--silent", "--show-error", "--location", "--retry", "2",
                     "--max-time", "90", "--output", str(received), url], check=True
                )
                require_identity(received, pin)
                received.replace(target)
        require_identity(target, pin)
    for pin in PINS["engine"]["packages"]:
        subprocess.run(["dpkg-deb", "-x", str(root / pin["path"]), str(root / "root")], check=True)
    for pin in PINS["models"]:
        if not matches_model(model_identity(root / pin["asset_path"]), pin):
            raise ValueError(f"AF-RES-202 blob/size mismatch: {pin['id']}")


def command_text(receipt):
    return receipt["stdout"] + "\n" + receipt["stderr"]


def component_rows(receipt):
    if receipt is None:
        return []
    return [(int(index), name, int(size), int(offset))
            for index, name, size, offset in COMPONENT.findall(command_text(receipt))]


def record(root, receipt_path):
    for name in ("libtesseract", "leptonica"):
        tool(root, name)
    combine = tool(root, "combine_tessdata")
    env = environment(root)
    with tempfile.TemporaryDirectory(prefix="components-", dir=root) as tmp:
        cwd = Path(tmp)
        rows = []
        for pin in PINS["models"]:
            source = root / pin["asset_path"]
            row = {"id": pin["id"], "path": str(source), "identity": None, "directory": None,
                   "network": None, "config": None, "availability": "unavailable"}
            if source.is_file():
                found = model_identity(source)
                row["identity"] = found
                row["availability"] = "exact" if matches_model(found, pin) else "edition_mismatch"
                if row["availability"] == "exact":
                    row["directory"] = capture([combine, "-d", source], cwd, env)
                    row["network"] = capture([combine, "-l", source], cwd, env)
                    components = component_rows(row["directory"])
                    if "config" in {c[1] for c in components}:
                        target = cwd / f"{pin['id']}.config"
                        row["config"] = {
                            "extraction": capture([combine, "-e", source, target], cwd, env),
                            "text": target.read_bytes().decode("utf-8", "surrogateescape")
                            if target.is_file() else None,
                        }
            rows.append(row)
        write_jsonl(receipt_path, rows)


def summarize(raw):
    pins = {pin["id"]: pin for pin in PINS["models"]}
    rows = []
    for receipt in raw:
        pin = pins[receipt["id"]]
        found = receipt["identity"] or {}
        directory, network, config = (receipt[key] for key in ("directory", "network", "config"))
        components = component_rows(directory)
        names = {c[1] for c in components}
        info = NETWORK.search(command_text(network)) if network else None
        version = re.search(r"^Version:(.*)$", command_text(directory), re.MULTILINE) if directory else None
        config_text = (config["text"] or "") if config else ""
        settings = re.findall(r"^[ \t]*tessedit_load_sublangs[ \t]+(.*)$", config_text, re.MULTILINE)
        modes = re.findall(r"^[ \t]*tessedit_ocr_engine_mode[ \t]+(.*)$", config_text, re.MULTILINE)
        status = receipt["availability"]
        if status == "exact":
            status = "complete" if (
                directory["returncode"] == network["returncode"] == 0 and components and info
                and (config is None or (config["extraction"]["returncode"] == 0 and config["text"] is not None))
            ) else "inspection_incomplete"
        rows.append({
            "asset": pin["id"], "collection": pin["collection"], "language": pin["language"],
            "model_git_blob": found.get("git_blob"), "model_sha256": found.get("sha256"), "model_bytes": found.get("bytes"),
            "directory_exit": directory["returncode"] if directory else None,
            "network_exit": network["returncode"] if network else None,
            "container_version": version[1].strip() if version else "",
            "component_count": len(components),
            "component_offsets_and_sizes_B": ";".join(
                f"{idx}:{name}@{offset}+{size}" for idx, name, size, offset in components
            ),
            "legacy_present": ";".join(name for name in LEGACY if name in names),
            "legacy_absent": ";".join(name for name in LEGACY if name not in names) if components else "",
            "lstm_present": ";".join(name for name in LSTM if name in names),
            "lstm_absent": ";".join(name for name in LSTM if name not in names) if components else "",
            "network": info[1] if info else "", "int_mode": info[2] if info else "",
            "recoding": info[3] if info else "", "network_other": info[4] if info else "",
            "config_exit": config["extraction"]["returncode"] if config else None,
            "config": "present" if config else ("absent" if components else "unverified"),
            "config_oem": ";".join(modes),
            "sublangs": ";".join(settings) if settings else ("none specified" if components else "unverified"),
            "status": status, "receipt": f"receipts/components.jsonl#{pin['id']}",
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("scratch", type=Path)
    measure = sub.add_parser("record")
    measure.add_argument("scratch", type=Path)
    measure.add_argument("receipts", type=Path)
    replay = sub.add_parser("replay")
    replay.add_argument("receipts", type=Path)
    replay.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "fetch":
        acquire(args.scratch.resolve())
    elif args.command == "record":
        record(args.scratch.resolve(), args.receipts.resolve())
    else:
        write_csv(args.output, summarize(read_jsonl(args.receipts)))


if __name__ == "__main__":
    main()
