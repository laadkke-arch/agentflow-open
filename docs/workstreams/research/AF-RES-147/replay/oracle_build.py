"""Build the evaluator's oracle from fixed originals, outside the query path."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from xml.dom import minidom

ROOT = Path(__file__).resolve().parents[1]


def canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def child(node, name, attribute=None, value=None):
    if node is None:
        return None
    items = [n for n in node.childNodes if n.nodeName == name and
             (attribute is None or n.getAttribute(attribute) == value) and
             (n.getAttribute("alt") == "" or attribute == "alt")]
    if len(items) > 1:
        raise ValueError((name, attribute, value, len(items)))
    return next(iter(items), None)


def node_text(node):
    if node is None:
        return None
    return "".join(n.data for n in node.childNodes if n.nodeType == n.TEXT_NODE)


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_points(value):
    return " ".join(f"U+{ord(c):04X}" for c in value) if value is not None else ""


def source_url(archive, member, anchor=""):
    return f'https://github.com/{archive["repo"]}/blob/{archive["commit"]}/{member}{anchor}'


# Paths were traced in the original supplemental main-parent map and XML. This oracle
# uses explicitly audited ladders; the runtime independently resolves parent data.
AUDITED_LADDERS = {
    "en_ZA": ("en_ZA", "en_001", "en", "root"),
    "ar_EG": ("ar_EG", "ar", "root"),
    "de_DE": ("de_DE", "de", "root"),
    "en_US": ("en_US", "en", "root"),
}


def inspect_cldr(tree, cell, archive):
    trace = []
    selected = None
    for loc in AUDITED_LADDERS[cell["locale"]]:
        member = f"common/main/{loc}.xml"
        original = tree / member
        if not original.is_file():
            trace.append({"member": member, "state": "file_absent"})
            continue
        document = minidom.parse(str(original)).documentElement
        numbers = child(document, "numbers")
        symbols = child(numbers, "symbols", "numberSystem", cell["number_system"])
        literal = child(symbols, cell["role"])
        value = node_text(literal)
        line_no = None
        if literal is not None:
            # Locate the literal within its exact numbering-system block for a fixed link.
            lines = original.read_text(encoding="utf-8").splitlines()
            start = next(i for i, line in enumerate(lines)
                         if f'<symbols numberSystem="{cell["number_system"]}"' in line)
            stop = next(i for i in range(start, len(lines)) if "</symbols>" in lines[i])
            line_no = next(i + 1 for i in range(start, stop)
                           if re.search(rf'<{cell["role"]}(?:\s|>)', lines[i]))
        if value not in {None, "↑↑↑", "∅∅∅"}:
            state = "literal"
        elif child(symbols, "alias") is not None:
            raise ValueError(f"un-audited path alias: {loc}: {cell}")
        else:
            state = {None: "node_absent", "↑↑↑": "inherit", "∅∅∅": "blocked"}[value]
        trace.append({"member": member, "raw": value, "line": line_no, "state": state,
                      "draft": literal.getAttribute("draft") if literal else "",
                      "sha256": file_sha(original)})
        if state == "blocked":
            break
        if state == "literal":
            selected = (member, value, line_no)
            break
    sources = ["CLDR-SUPPLEMENTAL"] + [f'CLDR-XML-{archive["edition"]}']
    if selected is None:
        return {"availability": "absent", "raw_trace": canonical(trace),
                "effective_value": "", "code_points": "", "source_location": "",
                "fixed_url": source_url(archive, cell["member"]), "source_ids": ";".join(sources)}
    member, value, line_no = selected
    return {"availability": "available", "raw_trace": canonical(trace),
            "effective_value": canonical({"role": cell["role"], "symbol": value}),
            "code_points": code_points(value), "source_location": f'{member}#{cell["xpath"]}',
            "fixed_url": source_url(archive, member, f"#L{line_no}"), "source_ids": ";".join(sources)}


def offset_seconds(text):
    return (-1 if text[0] == "-" else 1) * (
        3600 * int(text[1:3]) + 60 * int(text[3:5]) + int(text[5:] or 0))


def inspect_tz(tree, prepared, cell, archive):
    zone = cell["zone"]
    member = cell["member"]
    instant = datetime.fromisoformat(cell["utc"])
    compiled = prepared / zone
    if not compiled.is_file():
        raise FileNotFoundError(compiled)
    command = ["date", f"--date=@{int(instant.timestamp())}", "+%::z|%Z"]
    raw = subprocess.check_output(command, text=True, encoding="utf-8",
                                  env={**os.environ, "LC_ALL": "C", "TZ": ":" + str(compiled)})
    offset, abbreviation = raw.strip().split("|")
    lines = (tree / member).read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.split()[:2] == ["Zone", zone])
    stop = next(i for i in range(start + 1, len(lines))
                if not lines[i] or not lines[i][0].isspace())
    trace = [{"line": n + 1, "raw": lines[n].split("#", 1)[0].strip()}
             for n in range(start, stop)]
    if zone == "Asia/Beirut":
        trace.extend({"line": n + 1, "raw": line.strip()} for n, line in enumerate(lines)
                     if (parts := line.split())[:2] == ["Rule", "Lebanon"] and
                     parts[2] in {"1993", "1999", "2023", "2024"})
    return {
        "availability": "available", "raw_trace": canonical(trace),
        "effective_value": canonical({"offset_seconds": offset_seconds(offset.replace(":", "")),
                                     "abbreviation": abbreviation}), "code_points": "",
        "source_location": f"{member}#Zone {zone}",
        "fixed_url": source_url(archive, member, f"#L{start+1}-L{stop}"),
        "source_ids": f'TZ-{member.upper()};TZ-NEWS-{archive["edition"]}',
    }


def date_patterns(tree, archive):
    member = "common/main/en.xml"
    root = minidom.parse(str(tree / member)).documentElement
    gregorian = child(child(child(root, "dates"), "calendars"), "calendar", "type", "gregorian")
    path = child(child(gregorian, "dateTimeFormats"), "availableFormats")
    patterns = []
    for node in path.childNodes:
        if node.nodeName == "dateFormatItem" and node.getAttribute("id") == "hm":
            patterns.append({"alt": node.getAttribute("alt"), "value": node_text(node),
                             "code_points": code_points(node_text(node))})
    return {"edition": archive["edition"], "file": source_url(archive, member),
            "selector": "dates/calendars/calendar[@type='gregorian']/dateTimeFormats/availableFormats/dateFormatItem[@id='hm']",
            "patterns": patterns}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--scratch", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--extras", type=Path, required=True)
    args = cli.parse_args()
    scratch = args.scratch.resolve()
    artifacts = json.loads((ROOT / "evidence" / "artifacts.json").read_text(encoding="utf8"))
    selection = json.loads((ROOT / "replay" / "selection.json").read_text(encoding="utf8"))
    rows = []
    extras = {"date_pattern": [], "same_role_value": [], "tz_aliases": [], "cldr_aliases": []}
    for family in selection["family_edition_order"]:
        for artifact in artifacts.values():
            if artifact["family"] != family:
                continue
            version = artifact["edition"]
            tree = scratch / artifact["source_relative"]
            prepared = scratch / "prepared" / family / version
            artifact["repo"] = {"tzdb": "eggert/tz", "cldr": "unicode-org/cldr"}[family]
            for cell in selection[family]:
                result = (inspect_tz(tree, prepared, cell, artifact) if family == "tzdb"
                          else inspect_cldr(tree, cell, artifact))
                rows.append({"family": family, "edition": version, "key": cell["id"],
                             "layer": cell["layer"], "pre_exposure": {
                                 "announced": "publisher-announced cell",
                                 "adjacent": ("same announcement names grouping too" if family == "cldr"
                                              else "nearby time fixed; exact value not opened"),
                                 "unopened": "sorted frozen key; exact source unopened",
                             }[cell["layer"]],
                             "selector": cell.get("xpath") or f'{cell["zone"]}@{cell["utc"]}',
                             "target_member": cell["member"], **result})
            if family == "cldr":
                extras["date_pattern"].append(date_patterns(tree, artifact))
                role_check = {**selection["cldr"][1], "locale": "en_US", "member": "common/main/en_US.xml"}
                extras["same_role_value"].append(
                    {"edition": version, "key": "en_US|latn|group",
                     **inspect_cldr(tree, role_check, artifact)})
                member = "common/supplemental/supplementalMetadata.xml"
                root = minidom.parse(str(tree / member)).documentElement
                alias = child(child(child(root, "metadata"), "alias"), "languageAlias", "type", "sh")
                extras["cldr_aliases"].append({"edition": version, "requested": "sh",
                                                "replacement": alias.getAttribute("replacement"),
                                                "url": source_url(artifact, member, "#L241")})
            else:
                link = next((i, l.split()[1:3]) for i, l in enumerate(
                    (tree / "backward").read_text(encoding="utf-8").splitlines(), 1)
                    if l.split()[:3] == ["Link", "Asia/Shanghai", "PRC"])
                extras["tz_aliases"].append({"edition": version, "target_alias": link[1],
                                             "tzif_same": file_sha(prepared / "PRC") ==
                                                          file_sha(prepared / "Asia/Shanghai"),
                                             "url": source_url(artifact, "backward", f"#L{link[0]}")})
    if len(rows) != 32 or len({(r["family"], r["edition"], r["key"]) for r in rows}) != 32:
        raise ValueError("frozen 32-cell oracle is incomplete or has duplicates")
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    args.extras.write_text(json.dumps(extras, ensure_ascii=False, indent=2) + "\n", encoding="utf8")


if __name__ == "__main__":
    main()
