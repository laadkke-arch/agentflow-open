#!/usr/bin/env python3
"""Build the source-only frame from the main UI domains without opening ko/de PO."""
import argparse
import ast
from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory


FIELDS = re.compile(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?) ("(?:[^"\\]|\\.)*")$')
GLIB_KEYS = (
    "_", "N_", "Q_:1g", "C_:1c,2", "NC_:1c,2",
    "g_dcgettext:2", "g_dngettext:2,3", "g_dpgettext2:2c,3",
)
REF = re.compile(r'([^\s]+?):([0-9]+)(?=\s|$)')


def po_rows(path):
    """Yield the keys, original locations, flags, and translations of UTF-8 PO/POTs."""
    row = {"refs": [], "flags": [], "obsolete": False}
    field = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").split("\n") + [""], 1):
        if not raw.strip():
            if "msgid" in row:
                yield row
            row = {"refs": [], "flags": [], "obsolete": False}
            field = None
            continue
        line = raw
        if line.startswith("#~ "):
            row["obsolete"] = True
            line = line[3:]
        if line.startswith("#:"):
            row["refs"].extend(
                (path.removeprefix("../"), int(number)) for path, number in REF.findall(line[2:])
            )
        elif line.startswith("#,"):
            row["flags"].extend(re.findall(r'[^\s,]+', line[2:]))
        elif match := FIELDS.fullmatch(line):
            field, quoted = match.groups()
            row[field] = ast.literal_eval(quoted)
            if field == "msgid":
                row["msgid_line"] = number
                row.setdefault("key_line", number)
            if field == "msgctxt":
                row["key_line"] = number
        elif line.startswith('"') and field:
            row[field] += ast.literal_eval(line)
        elif not line.startswith("#"):
            raise ValueError(f"unrecognized PO syntax {path}:{number}")


def extract_gimp(source, xgettext, destination):
    listed = [
        line.strip() for line in (source / "po/POTFILES.in").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    # POTFILES can repeat a path. Keep the first occurrence, just as each file is read once.
    files = sorted(set(listed), key=str.encode)
    parts = {
        "C++": [item for item in files if Path(item).suffix in (".c", ".h", ".cpp")],
        "Glade": [item for item in files if item.endswith((".ui", ".ui.in.in"))],
        "AppData": [item for item in files if "appdata.xml" in item],
        "Desktop": [item for item in files if "desktop.in" in item],
    }
    used = {item for items in parts.values() for item in items}
    commands = []
    for language, paths in parts.items():
        if not paths:
            continue
        argv = [
            xgettext, "--from-code=UTF-8", f"--language={language}", "--force-po",
            "--no-wrap", "--output", str(destination),
        ]
        if destination.exists():
            argv.append("--join-existing")
        argv.extend(f"--keyword={key}" for key in GLIB_KEYS)
        argv.extend(paths)
        run = subprocess.run(argv, cwd=source, capture_output=True, check=True)
        commands.append({
            "argv_prefix": argv[:-len(paths)], "input_paths": len(paths),
            "exit": run.returncode, "stderr": run.stderr.decode(),
        })
    return {
        "listed": len(listed), "unique_paths": len(files), "omitted": sorted(set(files) - used),
        "commands": commands,
    }


def source_inventory(pot):
    grouped = defaultdict(list)
    plural = []
    for row in po_rows(pot):
        if row["obsolete"] or not row["msgid"]:
            continue
        refs = sorted(set(row["refs"]), key=lambda ref: (ref[0].encode(), ref[1]))
        explicit = row.get("msgctxt")
        key = {
            "context": explicit, "references": refs, "pot_line": row["key_line"],
            "generated_references": [ref for ref in refs if (
                ref[0].startswith(("build/", "_build/", "bld/"))
                or re.search(r'(?:\.svg|palettes|symbols|templates)\.h$', ref[0])
            )],
        }
        if "msgid_plural" in row:
            plural.append({"msgid": row["msgid"], "plural": row["msgid_plural"], **key})
            continue
        grouped[row["msgid"]].append(key)
    result = []
    for text in sorted(grouped, key=str.encode):
        contexts = sorted(grouped[text], key=lambda row: (row["context"] or "").encode())
        result.append({"msgid": text, "keys": contexts})
    return result, plural


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gimp", required=True, type=Path)
    parser.add_argument("--inkscape", required=True, type=Path, help="upstream source tarball tree")
    parser.add_argument("--xgettext", default="xgettext")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as workspace:
        gimp_pot = Path(workspace) / "gimp-source.pot"
        extraction = extract_gimp(args.gimp, args.xgettext, gimp_pot)
        inkscape_pot = args.inkscape / "po/inkscape.pot"
        for product, pot in (("G", gimp_pot), ("I", inkscape_pot)):
            entries, plural = source_inventory(pot)
            multi = []
            single = []
            for entry in entries:
                explicit = [key for key in entry["keys"] if key["context"]]
                if len(explicit) > 1:
                    multi.append(entry)
                elif len(explicit) == 1 and len(entry["keys"]) == 1:
                    single.append(entry)
            frame = {
                "source_entry_count": len(entries), "explicit_multicontext_groups": multi,
                "explicit_single_only_count": len(single), "single_controls": single[:2],
                "plural_exclusions": plural,
            }
            (args.output / f"{product}.json").write_text(
                json.dumps(frame, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        (args.output / "extraction.json").write_text(
            json.dumps(extraction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )


if __name__ == "__main__":
    main()
