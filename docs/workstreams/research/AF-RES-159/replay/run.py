#!/usr/bin/env python3
"""Compile original PO and replay GNU gettext and GLib queries in separate workspaces."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import gettext as python_gettext
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import time

from frame import po_rows
from seal import LANGUAGES, PRODUCTS, ROOT, encoded

DOMAINS = {"G": "gimp30", "I": "inkscape"}
LOCALES = {"ko": "ko_KR.UTF-8", "de": "de_DE.UTF-8"}
MISSING_CONTEXT = "AF-RES-159 controlled absent context"
PO_BASE = {
    "G": "https://gitlab.gnome.org/GNOME/gimp/-/blob/a77e8fd05d3d08a58650531a3700100f6a3216b7/po/",
    "I": "https://gitlab.com/inkscape/translations/-/blob/dd0592f12a5da07802a96b53293bbe12acdf45ff/",
}
PO_HASHES = {
    ("G", "ko"): "f2fff38b523c3ac78e6a9e48773f3321dcacb833bd6cdf5ea7c7512f629b9579",
    ("G", "de"): "8757f48b40709f92a8d3be1c32232833ada2872833be480469b94bcf29ceaae7",
    ("I", "ko"): "3d7af816d652468a60c78e36fb824739ec1ad1d8182fef52024c091e5fbaae1d",
    ("I", "de"): "c1d4de687e9394a8c34ea625ecf6de29866d6fe68cd7802bcbede8d8d59af9f3",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def emit(row):
    print(encoded(row).decode())


def run(argv, cwd, env):
    started = utc()
    begin = time.monotonic()
    proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True)
    info = dict(argv=[str(x) for x in argv], cwd=str(cwd), utc=started, exit=proc.returncode,
                ms=round(1000 * (time.monotonic() - begin), 3),
                stdout=proc.stdout.decode("utf-8"), stdout_sha256=sha(proc.stdout),
                stdout_bytes=len(proc.stdout), stdout_hex=proc.stdout.hex(),
                stderr=proc.stderr.decode("utf-8"), stderr_sha256=sha(proc.stderr))
    return info


def language_env(base, lang, locale_dir):
    return dict(base, LANGUAGE=lang, LC_ALL=LOCALES[lang], LANG=LOCALES[lang],
                TEXTDOMAINDIR=str(locale_dir))


def row_state(row):
    if row is None:
        return "absent"
    if row["obsolete"]:
        return "obsolete"
    if "fuzzy" in row["flags"]:
        return "fuzzy"
    if "msgid_plural" in row:
        return "plural"
    if not row["msgstr"]:
        return "empty"
    return "translated"


def po_index(path):
    rows = list(po_rows(path))
    inactive = {(row.get("msgctxt"), row["msgid"]): row for row in rows if row["obsolete"]}
    inactive.update({(row.get("msgctxt"), row["msgid"]): row for row in rows if not row["obsolete"]})
    header = dict(item.split(": ", 1) for item in rows[0]["msgstr"].splitlines() if ": " in item)
    selected_headers = ("Language", "Project-Id-Version", "POT-Creation-Date", "PO-Revision-Date",
                        "Content-Type", "Plural-Forms", "X-Generator")
    return inactive, {key: header[key] for key in selected_headers if key in header}, rows


def targets(layer):
    if layer == "supplement":
        with (ROOT / "evidence/supplement.csv").open(encoding="utf-8", newline="") as source:
            return list(csv.DictReader(source))
    with (ROOT / "calls.csv").open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def build_catalog(args, repeat, workspace, product, lang, env):
    sources = {"G": args.gimp, "I": args.inkscape}
    po_in = sources[product] / "po" / f"{lang}.po"
    local = workspace / "input" / product / po_in.name
    local.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(po_in, local)
    input_hash = sha(local.read_bytes())
    if input_hash != PO_HASHES[product, lang]:
        raise ValueError(f"unexpected pinned PO fingerprint: {po_in} {input_hash}")

    locale_dir = workspace / "compiled"
    mo = locale_dir / lang / "LC_MESSAGES" / (DOMAINS[product] + ".mo")
    mo.parent.mkdir(parents=True, exist_ok=True)
    # Strict validation is a separate observation. Publisher-style compilation below
    # uses ordinary msgfmt and retains the original catalog and flags.
    strict = run([args.msgfmt, "--check", "--statistics", "-o", os.devnull, local], workspace, env)
    compiled = run([args.msgfmt, "--statistics", "-o", mo, local], workspace, env)
    if compiled["exit"] != 0:
        emit(dict(row_type="compile_failure", repeat=repeat, product=product, language=lang,
                  po_sha256=input_hash, **compiled))
        raise RuntimeError("msgfmt failed")

    rows, header, all_rows = po_index(local)
    stats = Counter(row_state(row) for row in all_rows if row["msgid"])
    emit(dict(row_type="compile", repeat=repeat, product=product, language=lang,
              source_commit=PRODUCTS[product][2], domain=DOMAINS[product],
              po_url=f"{PO_BASE[product]}{lang}.po", po_sha256=input_hash,
              po_bytes=local.stat().st_size, headers=header, states=dict(stats),
              mo_sha256=sha(mo.read_bytes()), mo_bytes=mo.stat().st_size,
              mo_path=str(mo), validation=strict, **compiled))
    return mo, rows


def query(args, workspace, repeat, catalog_kind, catalog, product, lang, call, rows,
          probe, locale_dir, env, peer_context):
    domain = DOMAINS[product]
    msgid = call["msgid"]
    with catalog.open("rb") as data:
        mo_index = python_gettext.GNUTranslations(data)
    mo_bytes = catalog.read_bytes()
    env = language_env(env, lang, locale_dir)
    modes = [("context", call["context"]), ("plain", None)]
    if catalog_kind == "compiled" and args.phase == "main":
        modes.extend([("missing", MISSING_CONTEXT), ("ambient", None)])
        if peer_context is not None:
            modes.append(("wrong_live", peer_context))

    for mode, context in modes:
        row = rows.get((context, msgid)) if mode != "ambient" else None
        state = row_state(row) if mode != "ambient" else "unbound_domain"
        key = msgid if context is None else context + "\x04" + msgid
        # Entry presence is diagnostic only. Both observed outputs use public APIs.
        mo_has_key = key in mo_index._catalog if mode != "ambient" else False
        argv = [args.gettext] if mode == "ambient" else [args.gettext, "--domain", domain]
        if context is not None:
            argv += ["--context", context]
        argv += ["--", msgid]
        completed = run(argv, workspace, env)
        cross = run([probe, locale_dir, domain, mode, context or "", msgid], workspace, env)
        point = row["key_line"] if row else None
        po_url = f"{PO_BASE[product]}{lang}.po" + (f"#L{point}" if point else "")
        data = dict(product=product, language=lang, locale=LOCALES[lang], domain=domain,
                    effective_lookup_domain=domain if mode != "ambient" else "unset in CLI / messages in C",
                    mode=mode, context=context, msgid=msgid, layer=args.phase)
        emit(dict(
            row_type="lookup", repeat=repeat, catalog=catalog_kind, call_id=call["id"],
            source_commit=PRODUCTS[product][2], po_url=po_url, po_key_line=point,
            po_state=state, po_flags=row["flags"] if row else [],
            po_msgstr=row.get("msgstr") if row else None, po_refs=row["refs"] if row else [],
            mo_sha256=sha(mo_bytes), mo_has_key=mo_has_key,
            fallback_to_msgid=(not mo_has_key and completed["stdout"] == msgid),
            input_sha256=sha(encoded(data)), po_sha256=PO_HASHES[product, lang],
            glib=cross, **data, **completed,
        ))
        if completed["exit"] != 0 or cross["exit"] != 0:
            raise RuntimeError(f"lookup failed: {data}")


def run_workspace(args, repeat):
    run_targets = targets(args.phase)
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith("LC_") or k in ("LANGUAGE", "LANG", "TEXTDOMAIN", "TEXTDOMAINDIR"))}
    env.update(LANG="C.UTF-8", LC_ALL="C.UTF-8")
    with TemporaryDirectory(prefix=f"af159-{repeat}-") as temp:
        workspace = Path(temp)
        probe = workspace / "lookup"
        compile_probe = run(
            [args.cc, "-std=c99", "-Wall", "-Wextra", "-Werror",
             ROOT / "replay/lookup.c", "-Wl,-l:libglib-2.0.so.0", "-o", probe], workspace, env)
        emit(dict(row_type="probe_build", repeat=repeat, **compile_probe))
        if compile_probe["exit"] != 0:
            raise RuntimeError("GLib probe build failed")
        tools = {}
        tools["msgfmt"] = run([args.msgfmt, "--version"], workspace, env)["stdout"].splitlines()[0]
        tools["gettext"] = run([args.gettext, "--version"], workspace, env)["stdout"].splitlines()[0]
        tools["cc"] = run([args.cc, "--version"], workspace, env)["stdout"].splitlines()[0]
        tools["glib_package"] = run(
            ["dpkg-query", "-W", "-f=${Version}", "libglib2.0-0t64"], workspace, env)["stdout"]
        tools["libc"] = run(["getconf", "GNU_LIBC_VERSION"], workspace, env)["stdout"].strip()
        emit(dict(row_type="runtime", repeat=repeat, phase=args.phase, workspace=str(workspace), utc=utc(),
                  code_sha256=sha(Path(__file__).read_bytes()), tools=tools,
                  calls_sha256=sha((ROOT / ("calls.csv" if args.phase == "main"
                                           else "evidence/supplement.csv")).read_bytes()),
                  mo_sources=[str(root) for root in (args.shipped_gimp, args.shipped_inkscape) if root]))
        if tools["msgfmt"].split()[-1] != tools["gettext"].split()[-1]:
            raise RuntimeError("compilation and GNU query require the same suite version")
        for product in dict.fromkeys(row["id"][0] for row in run_targets):
            published = args.shipped_gimp if product == "G" else args.shipped_inkscape
            for lang in LANGUAGES:
                mo, rows = build_catalog(args, repeat, workspace, product, lang, env)
                for target in (row for row in run_targets if row["id"][0] == product):
                    if target.get("lang") not in (None, "", lang):
                        continue
                    peers = [row for row in run_targets if (
                        row["group"] == target["group"] and row["id"] != target["id"]
                    )]
                    peer = peers[0]["context"] if peers else None
                    query(args, workspace, repeat, "compiled", mo, product, lang,
                          target, rows, probe, workspace / "compiled", env, peer)
                    if not published:
                        continue
                    package_mo = published / lang / "LC_MESSAGES" / mo.name
                    if not package_mo.is_file():
                        raise FileNotFoundError(package_mo)
                    target_mo = workspace / "published" / lang / "LC_MESSAGES" / mo.name
                    target_mo.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(package_mo, target_mo)
                    query(args, workspace, repeat, "published", target_mo, product, lang,
                          target, rows, probe, workspace / "published", env, peer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gimp", required=True, type=Path)
    parser.add_argument("--inkscape", required=True, type=Path)
    parser.add_argument("--msgfmt", default="msgfmt")
    parser.add_argument("--gettext", default="gettext")
    parser.add_argument("--cc", default="cc")
    parser.add_argument("--shipped-gimp", type=Path, help="isolated directory containing LOCALE/LC_MESSAGES")
    parser.add_argument("--shipped-inkscape", type=Path, help="isolated directory containing LOCALE/LC_MESSAGES")
    parser.add_argument("--phase", choices=("main", "supplement"), default="main")
    parser.add_argument("--repeat", action="append", default=[])
    args = parser.parse_args()
    for repeat in args.repeat or ("W1", "W2"):
        run_workspace(args, repeat)


if __name__ == "__main__":
    main()
