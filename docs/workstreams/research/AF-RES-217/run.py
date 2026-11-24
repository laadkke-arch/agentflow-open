"""Record isolated Tesseract runs and controls, or replay their raw receipts."""

import argparse
from collections import Counter
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

from evidence import (
    HERE, PINS, capture, environment, identity, matches_model, model_identity, read_jsonl,
    require_identity, tool, utc, write_csv, write_jsonl,
)

MODELS = {model["id"]: model for model in PINS["models"]}
SELF = Path(__file__).resolve()
OPEN = re.compile(
    r'\b(?:open|openat|openat2)\(.*?"([^"]+\.(?:traineddata|png|aff|dic))".*\)\s+= '
    r'(-?\d+)(?:<([^>]+)>)?(?: ([A-Z][A-Z0-9_]+))?'
)
READ = re.compile(
    r'\b(?:read|pread64|readv)\(\d+<([^>]+)>,.*\)\s+= ([1-9]\d*)'
)
FAILED_LANGUAGE = re.compile(r"Failed loading language '([^']*)'")
TRACE_CALLS = "open,openat,openat2,read,pread64,readv"
INIT_ERROR = "Could not initialize tesseract."
PROCESS_ERROR = "Error during processing."


def api_probe(library, data, language, oem):
    """Run only Init using the public C ABI in a separate Python process."""
    lib = ctypes.CDLL(str(library))
    handle_t = ctypes.c_void_p
    char_array = ctypes.POINTER(ctypes.c_char_p)

    def sig(function, returns, *args):
        call = getattr(lib, function)
        call.restype, call.argtypes = returns, args
        return call

    create = sig("TessBaseAPICreate", handle_t)
    delete = sig("TessBaseAPIDelete", None, handle_t)
    init = sig("TessBaseAPIInit2", ctypes.c_int, handle_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
    languages = sig("TessBaseAPIGetLoadedLanguagesAsVector", char_array, handle_t)
    requested = sig("TessBaseAPIGetInitLanguagesAsString", ctypes.c_char_p, handle_t)
    path_used = sig("TessBaseAPIGetDatapath", ctypes.c_char_p, handle_t)
    get_int = sig("TessBaseAPIGetIntVariable", ctypes.c_int, handle_t, ctypes.c_char_p,
                  ctypes.POINTER(ctypes.c_int))
    free_languages = sig("TessDeleteTextArray", None, char_array)
    handle = create()
    if not handle:
        raise RuntimeError("TessBaseAPICreate returned null")
    try:
        code = init(handle, os.fsencode(data), language.encode(), oem)
        result = {"init": code, "requested_string": None, "loaded_languages": [], "data_path": None,
                  "effective_oem": None}
        if code == 0:
            vector = languages(handle)
            try:
                index = 0
                while vector[index]:
                    result["loaded_languages"].append(vector[index].decode())
                    index += 1
            finally:
                free_languages(vector)
            result.update(requested_string=requested(handle).decode(), data_path=os.fsdecode(path_used(handle)))
            mode = ctypes.c_int()
            if get_int(handle, b"tessedit_ocr_engine_mode", ctypes.byref(mode)):
                result["effective_oem"] = mode.value
        print(json.dumps(result))
    finally:
        delete(handle)


def place(root, directory, model_ids):
    directory.mkdir()
    inventory = {}
    for model_id in model_ids:
        pin = MODELS[model_id]
        source = root / pin["asset_path"]
        target = directory / pin["file"]
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copyfile(source, target)
        inventory[str(target)] = {"asset": model_id, **model_identity(target)}
    return inventory


def tracer(args, raw, group, run_id, argv, cwd, env, stdin=None):
    relative = Path(group + "-trace") / f"{run_id}.txt"
    target = raw / relative
    target.parent.mkdir(exist_ok=True)
    if target.exists():
        raise FileExistsError(target)
    traced = [args.strace, "-f", "-qq", "-s", "96", "-yy", "-e", f"trace={TRACE_CALLS}", "-o", target]
    result = capture([*traced, "--", *argv], cwd, env, stdin)
    return {**result, "program_argv": list(map(str, argv)), "trace": relative.as_posix(),
            "trace_identity": identity(target) if target.is_file() else None}


def tesseract_run(args, group, run_id, model_ids, language, oem, *,
                  repeat=1, page="page", alternate=(), missing=False, synthetic=False, api=False):
    root, raw = args.scratch, args.receipts
    build = PINS["engine"]["build_id"]
    image_pin = PINS[page]
    image_source = require_identity(HERE / image_pin["path"], image_pin)
    prefix_kind = "C_ABI" if api else "Tesseract"
    base = {"id": run_id, "group": group, "tool": prefix_kind, "build": build, "assets": list(model_ids),
            "language": language, "oem": oem, "repeat": repeat, "input_kind": page if not api else None}
    with tempfile.TemporaryDirectory(prefix=f"{run_id}-", dir=root) as space:
        cwd = Path(space)
        directory = cwd / "models"
        inventory = {}
        staged_state = "exact"
        if not missing:
            try:
                inventory = place(root, directory, model_ids)
            except FileNotFoundError as exc:
                return {**base, "cwd": str(cwd), "staged_state": "unavailable",
                        "staging_error": str(exc), "utc": utc()}
        if any(not matches_model({k: v for k, v in item.items() if k != "asset"}, MODELS[item["asset"]])
               for item in inventory.values()):
            return {**base, "cwd": str(cwd), "staged_state": "edition_mismatch", "inventory": inventory, "utc": utc()}
        if synthetic:
            target = directory / "eng.traineddata"
            target.write_bytes(bytes.fromhex(PINS["synthetic_bad_model"]["hex"]))
            inventory[str(target)] = {"asset": "synthetic", **model_identity(target)}
            staged_state = "synthetic"
        alt = cwd / "alternate" if alternate else None
        alternate_inventory = place(root, alt, alternate) if alt else {}
        image = cwd / "input.png"
        if not api:
            shutil.copyfile(image_source, image)
            require_identity(image, image_pin)
        if api:
            argv = [sys.executable, "-B", SELF, "probe-init", tool(root, "libtesseract"), directory, language, oem]
        else:
            argv = [tool(root, "tesseract"), image, "stdout", "--tessdata-dir", directory, "-l", language,
                    "--oem", oem, "--psm", PINS["page"]["psm"], "--dpi", PINS["page"]["dpi_cli"]]
        before = sorted(path.name for path in directory.iterdir()) if directory.is_dir() else None
        result = tracer(args, raw, group, run_id, argv, cwd, environment(root, alt))
        after = sorted(path.name for path in directory.iterdir()) if directory.is_dir() else None
        identities_after = {name: model_identity(Path(name)) for name in inventory}
        alternate_after = {name: model_identity(Path(name)) for name in alternate_inventory}
        return {
            **base, "staged_state": staged_state, "tessdata_dir": str(directory),
            "inventory": inventory, "inventory_after": identities_after, "alt_inventory": alternate_inventory,
            "alt_inventory_after": alternate_after, "files_before": before, "files_after": after,
            "input_path": str(image) if not api else None, "input": identity(image) if not api else None,
            "strace": {"path": str(args.strace), **identity(args.strace)}, **result,
        }


def hunspell_run(args, run_id, omit=None):
    root = args.scratch
    with tempfile.TemporaryDirectory(prefix=f"{run_id}-", dir=root) as space:
        cwd = Path(space)
        directory = cwd / "dict"
        directory.mkdir()
        inventory = {}
        for pin in PINS["hunspell"]["pair"]:
            if pin["suffix"] != omit:
                original = require_identity(root / pin["path"], pin)
                staged = directory / pin["name"]
                shutil.copyfile(original, staged)
                inventory[str(staged)] = identity(staged)
        stdin = PINS["hunspell"]["synthetic_stdin"].encode()
        argv = [tool(root, "hunspell"), "-d", directory / "en_GB", "-i", "UTF-8", "-p", "/dev/null", "-l"]
        receipt = tracer(args, args.receipts, "controls", run_id, argv, cwd, environment(root), stdin)
        return {
            "id": run_id, "group": "controls", "tool": "Hunspell", "build": "Hunspell 1.7.1-1 amd64",
            "assets": [Path(name).name for name in inventory], "language": "en_GB", "repeat": 1,
            "input_kind": "synthetic_stdin", "input": {"bytes": len(stdin), "sha256": hashlib.sha256(stdin).hexdigest()},
            "stdin": stdin.decode(), "tessdata_dir": str(directory), "inventory": inventory,
            "strace": {"path": str(args.strace), **identity(args.strace)}, **receipt,
        }


def record(args):
    for name in ("tesseract", "libtesseract", "leptonica"):
        tool(args.scratch, name)
    args.receipts.mkdir(parents=True, exist_ok=True)
    path = args.receipts / f"{args.group}.jsonl"
    if path.exists():
        raise FileExistsError(path)
    if args.group == "main":
        def main_rows():
            for model in PINS["models"]:
                for oem in (0, 1):
                    for repeat in (1, 2):
                        slot = f"{model['id']}-OEM{oem}"
                        yield tesseract_run(args, "main", f"{slot}-R{repeat}", (model["id"],),
                                            model["language"], oem, repeat=repeat)
        write_jsonl(path, main_rows())
    else:
        tool(args.scratch, "libhunspell")
        def control_rows():
            yield tesseract_run(args, "controls", "CT01", (), "eng", 1, missing=True)
            yield tesseract_run(args, "controls", "CT02", (), "eng", 1, synthetic=True)
            yield tesseract_run(args, "controls", "CT03", ("A01",), "eng", 0, alternate=("A05",))
            yield tesseract_run(args, "controls", "CT04", ("A05",), "eng", 0, alternate=("A01",))
            yield tesseract_run(args, "controls", "CT05", ("A05",), "eng", 1, page="blank")
            yield tesseract_run(args, "controls", "CT06", ("A05",), "eng+ara", 1)
            yield tesseract_run(args, "controls", "CT07", ("A05", "A06"), "eng+ara", 1)
            yield hunspell_run(args, "CT08")
            yield hunspell_run(args, "CT09", omit="aff")
            yield hunspell_run(args, "CT10", omit="dic")
            yield tesseract_run(args, "controls", "API-A01-OEM0", ("A01",), "eng", 0, api=True)
            yield tesseract_run(args, "controls", "API-A05-OEM0", ("A05",), "eng", 0, api=True)
            yield tesseract_run(args, "controls", "API-CT06", ("A05",), "eng+ara", 1, api=True)
            yield tesseract_run(args, "controls", "API-CT07", ("A05", "A06"), "eng+ara", 1, api=True)
        write_jsonl(path, control_rows())


def accessed(receipts, row):
    if not row.get("trace_identity"):
        return [], Counter()
    path = require_identity(receipts / row["trace"], row["trace_identity"])
    opens, reads = [], Counter()
    for line in path.read_text(encoding="utf-8", errors="surrogateescape").splitlines():
        call = OPEN.search(line)
        if call:
            arg, fd, real, errno = call.groups()
            opens.append((arg, int(fd), real or arg, errno or ""))
        call = READ.search(line)
        if call:
            reads[call[1]] += int(call[2])
    return opens, reads


def judge_cli(row, model_reads, model_opens, input_read):
    err = row.get("stderr", "")
    status = row.get("returncode")
    if row.get("staged_state") in ("edition_mismatch", "unavailable"):
        return None, "not_reached", [], row["staged_state"]
    if row.get("capture_error") or not row.get("trace_identity"):
        return None, "unverified", [], "environment_failure"
    init = -1 if INIT_ERROR in err else (0 if status == 0 or PROCESS_ERROR in err else None)
    processing = "not_reached" if init == -1 else ("complete" if status == 0 else "unverified")
    if row.get("files_before") != row.get("files_after"):
        return init, processing, [], "staged_directory_changed"
    if any(row["inventory_after"].get(path) != {k: v for k, v in ident.items() if k != "asset"}
           for path, ident in row["inventory"].items()):
        return init, processing, [], "staged_bytes_changed"
    requested = row["language"].split("+")
    expected = {str(Path(row["tessdata_dir"]) / (lang + ".traineddata")): lang for lang in requested}
    if not model_opens or any(real not in expected for _, _, real, _ in model_opens) or model_reads.keys() - expected.keys():
        return init, processing, [], "path_unverified"
    if init == -1:
        if "legacy) engine requested, but components are not present" in err and set(model_reads) == set(expected):
            return init, processing, [], "legacy_components_missing"
        if "Error opening data file" in err:
            if model_reads:
                return init, processing, [], "model_parse_rejected"
            if all(fd < 0 and errno == "ENOENT" for _, fd, _, errno in model_opens):
                return init, processing, [], "model_path_missing"
        return init, processing, [], "other_init_failure"
    if init is None:
        return init, processing, [], "unclassified_failure"
    failed = set(FAILED_LANGUAGE.findall(err))
    loaded = [lang for path, lang in expected.items() if model_reads.get(path) and lang not in failed]
    if not loaded:
        return init, processing, loaded, "path_unverified"
    if "LSTM requested, but not present" in err:
        return init, processing, loaded, "mode_fallback"
    if status != 0:
        return init, "failed", loaded, "page_processing_failed"
    if not input_read:
        return init, "unverified", loaded, "input_read_unverified"
    if requested != loaded or failed:
        return init, processing, loaded, "partial_language_success"
    return init, processing, loaded, "initialized"


def summarize(receipts, row):
    opens, reads = accessed(receipts, row)
    ext = (".aff", ".dic") if row["tool"] == "Hunspell" else (".traineddata",)
    model_opens = [entry for entry in opens if entry[0].endswith(ext)]
    model_reads = {path: n for path, n in reads.items() if path.endswith(ext)}
    status, out, err = row.get("returncode"), row.get("stdout", ""), row.get("stderr", "")
    input_read = reads.get(row.get("input_path"), 0)
    options = None
    if row["tool"] == "C_ABI":
        options = json.loads(out) if status == 0 and out else None
        init = options["init"] if options is not None else None
        loaded = options["loaded_languages"] if options is not None else []
        processing = "not_requested"
        verdict = "api_measured" if options is not None else "api_unverified"
    elif row["tool"] == "Hunspell":
        init, processing, loaded = None, "spell_list" if status == 0 else "not_completed", []
        verdict = "spell_result" if status == 0 and not err else "spell_diagnostic"
    else:
        init, processing, loaded, verdict = judge_cli(row, model_reads, model_opens, input_read)
    raw = out.encode("utf-8", "surrogateescape")
    inventory = row.get("inventory", {})
    attempts = dict.fromkeys(f"{arg}={'OK' if fd >= 0 else errno or 'ERROR'}" for arg, fd, _, errno in model_opens)
    opened = dict.fromkeys(real for _, fd, real, _ in model_opens if fd >= 0)
    return {
        "run_id": row["id"], "scope": "validation" if row["tool"] == "C_ABI" else row["group"], "tool": row["tool"],
        "build": row["build"], "asset_ids": ";".join(row["assets"]), "language": row["language"], "oem": row.get("oem"),
        "repeat": row["repeat"], "input_kind": row.get("input_kind"), "input_sha256": (row.get("input") or {}).get("sha256"),
        "cwd": row.get("cwd"), "specified_dir": row.get("tessdata_dir"),
        "prefix_env": row.get("environment", {}).get("TESSDATA_PREFIX", ""), "input_read_B": input_read,
        "opened_paths": ";".join(opened), "attempts": ";".join(attempts),
        "bytes_read_by_path": ";".join(f"{path}={n}" for path, n in model_reads.items()),
        "opened_fingerprints": ";".join(f"{path}={inventory[path]['sha256']}" for path in opened if path in inventory),
        "init": init, "loaded_languages": ";".join(loaded), "processing": processing, "exit": status,
        "stdout_B": len(raw), "stdout_sha256": hashlib.sha256(raw).hexdigest(),
        "stdout_nonblank": bool(out.strip()), "stdout_text": out, "stderr_text": err, "verdict": verdict,
        "effective_oem_api": options["effective_oem"] if options else None, "trace": row.get("trace"),
        "receipt": f"receipts/{row['group']}.jsonl#{row['id']}",
    }


def replay(receipts, output):
    rows = []
    for group in ("main", "controls"):
        path = receipts / f"{group}.jsonl"
        if path.is_file():
            rows.extend(summarize(receipts, raw) for raw in read_jsonl(path))
    if not rows:
        raise ValueError("receipts are empty")
    write_csv(output, rows)
    print(json.dumps({scope: dict(Counter(r["verdict"] for r in rows if r["scope"] == scope))
                      for scope in sorted({row["scope"] for row in rows})}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    measure = sub.add_parser("record")
    measure.add_argument("group", choices=("main", "controls"))
    measure.add_argument("scratch", type=Path)
    measure.add_argument("receipts", type=Path)
    measure.add_argument("--strace", type=Path, default=Path("/usr/bin/strace"))
    reproduce = sub.add_parser("replay")
    reproduce.add_argument("receipts", type=Path)
    reproduce.add_argument("output", type=Path)
    probe = sub.add_parser("probe-init")
    probe.add_argument("library", type=Path)
    probe.add_argument("directory", type=Path)
    probe.add_argument("language")
    probe.add_argument("oem", type=int)
    args = parser.parse_args()
    if args.command == "record":
        args.scratch, args.receipts, args.strace = args.scratch.resolve(), args.receipts.resolve(), args.strace.resolve()
        record(args)
    elif args.command == "replay":
        replay(args.receipts, args.output)
    else:
        api_probe(args.library, args.directory, args.language, args.oem)


if __name__ == "__main__":
    main()
