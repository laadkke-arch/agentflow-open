"""Acquire pinned inputs, inspect six traineddata files, or replay component receipts."""

import argparse
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

from evidence import (
    PINS, capture, environment, matches_model, model_identity, read_jsonl,
    require_identity, tool, utc, write_csv, write_jsonl,
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


def record_headers(root, receipt_path):
    rows = []
    for pin in PINS["models"]:
        path = root / pin["asset_path"]
        found = model_identity(path)
        if not matches_model(found, pin):
            raise ValueError(f"header source mismatch: {pin['id']}")
        with path.open("rb") as stream:
            # Six pinned files use a little-endian 4-byte count and 24 8-byte offsets.
            header = stream.read(4 + 24 * 8)
        if len(header) != 196 or struct.unpack_from("<i", header)[0] != 24:
            raise ValueError(f"unexpected container format: {path}")
        rows.append({"id": pin["id"], "path": str(path), "identity": found, "utc": utc(),
                     "argv": sys.argv, "header_hex": header.hex()})
    write_jsonl(receipt_path, rows)


def file_offsets(header, file_size, components):
    raw = bytes.fromhex(header["header_hex"])
    offsets = struct.unpack_from("<24q", raw, 4)
    starts = [(idx, start) for idx, start in enumerate(offsets) if start >= 0]
    if [i for i, _ in starts] != [i for i, *_ in components]:
        raise ValueError(f"header and -d component indices differ: {header['id']}")
    ends = [start for _, start in starts[1:]] + [file_size]
    pairs = []
    for (_, name, size, reported), (_, start), end in zip(components, starts, ends):
        if end - start != size or start < len(raw):
            raise ValueError(f"header and -d component sizes differ: {header['id']} {name}")
        pairs.append((name, start, size, start - reported))
    return pairs


def summarize(raw, headers=()):
    headers_by_id = {header['id']: header for header in headers}
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
        physical = []
        if pin["id"] in headers_by_id:
            header = headers_by_id[pin["id"]]
            if header["identity"] != found:
                raise ValueError(f"header receipt identity differs: {pin['id']}")
            physical = file_offsets(header, found["bytes"], components)
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
            "directory_offsets_and_sizes_B": ";".join(
                f"{idx}:{name}@{offset}+{size}" for idx, name, size, offset in components
            ),
            "file_offsets_and_sizes_B": ";".join(f"{name}@{offset}+{size}" for name, offset, size, _ in physical),
            "file_minus_directory_offsets_B": ";".join(str(delta) for delta in sorted({value[3] for value in physical})),
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
    headers = sub.add_parser("headers")
    headers.add_argument("scratch", type=Path)
    headers.add_argument("receipts", type=Path)
    replay = sub.add_parser("replay")
    replay.add_argument("receipts", type=Path)
    replay.add_argument("output", type=Path)
    replay.add_argument("--headers", type=Path)
    args = parser.parse_args()
    if args.command == "fetch":
        acquire(args.scratch.resolve())
    elif args.command == "record":
        record(args.scratch.resolve(), args.receipts.resolve())
    elif args.command == "headers":
        record_headers(args.scratch.resolve(), args.receipts.resolve())
    else:
        headers = read_jsonl(args.headers) if args.headers else ()
        write_csv(args.output, summarize(read_jsonl(args.receipts), headers))


if __name__ == "__main__":
    main()
