#!/usr/bin/env python3
"""Replay the pinned FreshRSS CLI against disposable SQLite databases."""
import argparse
import csv
import hashlib
import json
import platform
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PIN = "b2c50115baa36c217e939ee3ea8ecfae52f91abd"
IMAGE = "af-res-228-runtime:20261124"
USER = "afres228"
GROUPS = ("main", "controls", "replay")
TABLES = ("category", "feed", "entry", "entrytmp", "tag", "entrytag")
SOURCE = Path("/src")
HERE = Path(__file__).resolve().parent
ENV = {"PATH": "/usr/bin:/bin", "TZ": "UTC", "LC_ALL": "C.UTF-8"}
READ_UNREAD = "user/1000000001/state/com.google/unread"
CONFLICT_LINK = "https://example-feed.test/articles/one-canonical-control"

PROBE = r"""
require 'cli/_cli.php';
cliInitUser($argv[1]);
echo json_encode([
    'freshrss' => FRESHRSS_VERSION,
    'data_path' => DATA_PATH,
    'db_engine' => FreshRSS_Context::systemConf()->db['type'],
    'reception' => FreshRSS_Context::userConf()->mark_when['reception'],
    'enabled_extensions' => FreshRSS_Context::userConf()->extensions_enabled,
], JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR), "\n";
"""

DRIFT = r"""
require 'cli/_cli.php';
cliInitUser($argv[1]);
$entries = FreshRSS_Factory::createEntryDao();
$tags = FreshRSS_Factory::createTagDao();
$first = $entries->searchIdByGuid(1, $argv[2]);
$second = $entries->searchIdByGuid(2, $argv[3]);
$design = null;
foreach (FreshRSS_Context::labels() as $tag) {
    if ($tag->name() === 'Design') { $design = $tag->id(); }
}
if ($first === null || $second === null || $design === null) {
    exit(1);
}
$local = $tags->addTag(['name' => 'LocalOnly']);
$result = [
    'mark_0001_unread' => $entries->markRead($first, false),
    'mark_0002_read' => $entries->markRead($second, true),
    'unstar_0001' => $entries->markFavorite($first, false),
    'detach_design_0002' => $tags->tagEntry($design, $second, false),
    'attach_local_0002' => $local && $tags->tagEntry($local, $second),
];
echo json_encode($result, JSON_THROW_ON_ERROR), "\n";
exit(in_array(false, $result, true) || in_array(0, $result, true) ? 1 : 0);
"""


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fingerprints(raw):
    return {
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "git_blob_sha1": hashlib.sha1(f"blob {len(raw)}\x00".encode() + raw).hexdigest(),
    }


def run_cmd(args, *, cwd=None, env=None, timeout=60):
    started = utc()
    try:
        result = subprocess.run(
            args, cwd=cwd, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
        return {
            "argv": args, "started_utc": started, "finished_utc": utc(),
            "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "argv": args, "started_utc": started, "finished_utc": utc(), "exit": 124,
            "stdout": (exc.stdout or b"").decode("utf-8", errors="replace"),
            "stderr": (exc.stderr or b"").decode("utf-8", errors="replace") + "\ntimeout\n",
        }


def php_case(receipt, stage, data, arguments, *, trace=False, expected_success=True):
    env = {**ENV, "DATA_PATH": str(data)}
    args = ["php", *arguments]
    if trace:
        trace_path = data.parent / f"{stage}.strace"
        args = ["strace", "-f", "-qq", "-yy", "-s", "256", "-e", "trace=%network",
                "-o", str(trace_path), *args]
    command = run_cmd(args, cwd=SOURCE, env=env)
    command["DATA_PATH"] = str(data)
    if trace:
        command["strace_network"] = trace_path.read_text(errors="replace") if trace_path.exists() else None
        command["app_log_files_after_command"] = {
            str(p.relative_to(data)): p.read_text(errors="replace")
            for p in sorted((data / "users").glob("*/log.txt"))
        }
    receipt["commands"][stage] = command
    if expected_success and command["exit"] != 0:
        raise RuntimeError(f"{stage}: {shlex.join(args)} exited {command['exit']}")
    return command


def schema(db):
    rows = db.execute(
        "SELECT sql FROM sqlite_schema WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' "
        "ORDER BY type = 'index', rowid"
    )
    return ";\n\n".join(row[0] for row in rows) + ";\n"


def snapshot(db_path):
    with sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True) as db:
        db.row_factory = sqlite3.Row

        def rows(sql):
            return [dict(row) for row in db.execute(sql)]

        ddl = schema(db)
        db_path_wal = db_path.with_name("db.sqlite-wal")
        return {
            "db_path": str(db_path),
            "db_sha256": hashlib.sha256(db_path.read_bytes()).hexdigest(),
            "wal_sha256": hashlib.sha256(db_path_wal.read_bytes()).hexdigest() if db_path_wal.exists() else None,
            "schema_sha256": hashlib.sha256(ddl.encode()).hexdigest(),
            "tables": [
                row["name"] for row in rows(
                    "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name"
                )
            ],
            "counts": {name: db.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0] for name in TABLES},
            "quick_check": db.execute("PRAGMA quick_check").fetchone()[0],
            "foreign_key_check": rows("PRAGMA foreign_key_check"),
            "categories": rows("SELECT id, name FROM category ORDER BY id"),
            "feeds": rows("SELECT id, url, name, website, category, cache_nbEntries, cache_nbUnreads, "
                          "lastUpdate FROM feed ORDER BY id"),
            "entries": rows(
                "SELECT e.id, e.id_feed, f.url AS feed_url, e.guid, e.title, e.link, e.is_read, "
                "e.is_favorite, e.tags AS entry_tags, e.date, e.lastSeen, e.lastModified, "
                "e.lastUserModified, lower(hex(e.hash)) AS row_hash "
                "FROM entry e LEFT JOIN feed f ON f.id=e.id_feed ORDER BY e.id_feed, e.guid"
            ),
            "tags": rows("SELECT id, name FROM tag ORDER BY id"),
            "entrytags": rows(
                "SELECT j.id_entry, j.id_tag, t.name FROM entrytag j JOIN tag t ON t.id=j.id_tag "
                "ORDER BY j.id_entry, j.id_tag"
            ),
        }


def case_plan(group, fixture_bytes):
    a, b = fixture_bytes["S02"], fixture_bytes["S03"]
    if group == "main":
        return [
            (f"{key}-r{int(setting)}", key, setting, [("first", name, raw), ("repeat", name, raw)])
            for key, raw, name in [("S02", a, "S02/starred.json"), ("S03", b, "S03/starred.json")]
            for setting in (False, True)
        ]

    def controlled(raw, change):
        obj = json.loads(raw)
        change(obj["items"])
        return json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"

    shared_guid = json.loads(a)["items"][0]["id"]
    collision = controlled(a, lambda items: items[1].update(id=shared_guid))
    if group == "replay":
        return [
            ("REPLAY-positive", "S02", True, [("first", "S02/starred.json", a)]),
            ("REPLAY-negative", "S02", False, [("first", "starred.json", collision)]),
        ]

    def keep_first(items):
        del items[1:]

    split_a = controlled(collision, keep_first)
    split_b = controlled(collision, lambda items: items.pop(0))
    clash = controlled(a, lambda items: items[0]["canonical"][0].update(href=CONFLICT_LINK))
    canonical_only = controlled(clash, lambda items: items[0].update(alternate=[]))

    def remove_star(items):
        categories = items[1]["categories"]
        items[1]["categories"] = [c for c in categories if not c.endswith("/state/com.google/starred")]

    no_star = controlled(b, remove_star)
    unread = controlled(a, lambda items: items[1]["categories"].append(READ_UNREAD))
    boolean_false = controlled(a, lambda items: items[1].update(read=False))
    singles = [
        ("C1-collision", "S02", False, "starred.json", collision),
        ("C2-conflict", "S02", False, "starred.json", clash),
        ("C2-canonical-only", "S02", False, "starred.json", canonical_only),
        ("C3-original-name", "S03", False, "starred-inoreader.json", b),
        ("C3-neutral-name", "S03", False, "transfer.json", b),
        ("C3-fallback-starred", "S03", False, "starred.json", no_star),
        ("C3-fallback-neutral", "S03", False, "transfer.json", no_star),
        ("C3-fallback-path", "S03", False, "starred-staging/transfer.json", no_star),
        ("C4-unread-token", "S02", True, "starred.json", unread),
        ("C4-boolean-false", "S02", True, "starred.json", boolean_false),
    ]
    return [
        (name, key, setting, [("first", filename, raw)]) for name, key, setting, filename, raw in singles
    ] + [
        ("C1-split", "S02", False, [
            ("first", "part1/starred.json", split_a), ("second", "part2/starred.json", split_b),
        ]),
        ("C5-state-drift", "S02", False, [
            ("first", "S02/starred.json", a), ("repeat", "S02/starred.json", a),
        ]),
    ]


def run_case(root, output, name, source_id, setting, imports):
    work = root / name
    data = work / "data"
    data.mkdir(parents=True)
    db = data / "users" / USER / "db.sqlite"
    receipt = {
        "run_id": name, "source_id": source_id, "receiver_expected": PIN,
        "requested_reception": setting, "commands": {}, "inputs": {}, "snapshots": {},
    }
    try:
        php_case(receipt, "prepare", data, ["cli/prepare.php"])
        php_case(receipt, "install", data, [
            "cli/do-install.php", f"--default-user={USER}", "--db-type=sqlite", "--auth-type=none",
            "--base-url=http://localhost", "--disable-update=true",
        ])
        custom = data / "config-user.custom.php"
        custom.write_text(f"<?php\nreturn ['mark_when' => ['reception' => {str(setting).lower()}]];\n")
        receipt["user_override"] = {"path": str(custom), "text": custom.read_text(), **fingerprints(custom.read_bytes())}
        php_case(receipt, "create_user", data, ["cli/create-user.php", f"--user={USER}", "--no-default-feeds"])
        loaded = php_case(receipt, "inspect_loaded_config", data, ["-r", PROBE, USER])
        receipt["effective_settings"] = json.loads(loaded["stdout"])
        if receipt["effective_settings"]["reception"] != setting:
            raise RuntimeError("loader did not see requested reception setting")
        baseline = snapshot(db)
        receipt["snapshots"]["baseline"] = baseline
        if baseline["counts"] != {"category": 1, "feed": 0, "entry": 0, "entrytmp": 0, "tag": 0, "entrytag": 0}:
            raise RuntimeError("database did not start empty")
        if name == "S02-r0":
            with sqlite3.connect(db.as_uri() + "?mode=ro", uri=True) as conn:
                (output / "schema.sql").write_text("-- Actual sqlite_schema before S02-r0 first import.\n" + schema(conn))
        for stage, filename, raw in imports:
            if name == "C5-state-drift" and stage == "repeat":
                before = json.loads(raw)["items"]
                php_case(receipt, "seed_user_changes", data, ["-r", DRIFT, USER, before[0]["id"], before[1]["id"]])
                receipt["snapshots"]["after_user_changes"] = snapshot(db)
            input_path = work / "input" / filename
            input_path.parent.mkdir(parents=True, exist_ok=True)
            input_path.write_bytes(raw)
            receipt["inputs"][stage] = {
                "path": str(input_path), "path_given_as_filename": str(input_path),
                "items": len(json.loads(raw)["items"]), **fingerprints(input_path.read_bytes()),
            }
            php_case(receipt, f"import_{stage}", data, [
                "cli/import-for-user.php", f"--user={USER}", f"--filename={input_path}",
            ], trace=True, expected_success=False)
            receipt["snapshots"][stage] = snapshot(db)
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
        receipt["error"] = str(exc)
    finally:
        write_json(output / f"{name}.json", receipt)
    return receipt


def observations(output, manifest, runs):
    files = {f["source_id"]: f for f in manifest["files"]}
    actual = []
    for run in runs:
        key = run["source_id"]
        for stage in ("first", "repeat"):
            state = run["snapshots"].get(stage)
            first = run["snapshots"].get("first")
            for item in files[key]["items"]:
                def find(snapshot_data):
                    if snapshot_data is None:
                        return None, [], "미확인"
                    candidates = [
                        e for e in snapshot_data["entries"]
                        if (e["feed_url"], e["guid"]) == (item["feed_url_from_stream_id"], item["id"])
                    ]
                    if len(candidates) != 1:
                        return None, [], f"{len(candidates)} matches"
                    entry = candidates[0]
                    tags = [rel for rel in snapshot_data["entrytags"] if rel["id_entry"] == entry["id"]]
                    return entry, tags, "1 match"

                entry, tags, matched = find(state)
                previous_entry, previous_tags, _ = find(first)
                compare = "initial" if stage == "first" else "미확인"
                if stage == "repeat" and entry is not None and previous_entry is not None:
                    diffs = [field for field, val in entry.items() if val != previous_entry[field]]
                    if tags != previous_tags:
                        diffs.append("entrytag")
                    compare = ",".join(diffs) or "equal"
                db_result = entry or {}
                actual.append({
                    "run_id": run["run_id"], "source_id": key, "input_pointer": item["json_pointer"],
                    "reception": run["requested_reception"], "round": stage,
                    "input_feed_url": item["feed_url_from_stream_id"], "input_id": item["id"],
                    "input_alternate": item["alternate"][0]["href"], "input_canonical": item["canonical"][0]["href"],
                    "input_read_token": item["read_token"], "input_unread_token": item["unread_token"],
                    "input_star_token": item["star_token"], "input_starred_property": item["starred_property"],
                    "input_label_tokens": json.dumps(item["label_tokens"]),
                    "key_join": matched, "db_feed_id": db_result.get("id_feed", "미확인"),
                    "db_guid": db_result.get("guid", "미확인"), "db_entry_id": db_result.get("id", "미확인"),
                    "db_link": db_result.get("link", "미확인"),
                    "db_is_read": db_result.get("is_read", "미확인"),
                    "db_is_favorite": db_result.get("is_favorite", "미확인"),
                    "db_tag_relations": json.dumps(tags) if entry is not None else "미확인",
                    "db_entry_tags": db_result.get("entry_tags", "미확인"),
                    "db_last_seen": db_result.get("lastSeen", "미확인"),
                    "changed_fields_vs_first": compare,
                    "receipt": f"receipts/{run['run_id']}.json",
                })
    with (output / "observed.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(actual[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(actual)


def container(group):
    manifest = json.loads((HERE / "inputs.json").read_text())
    fixture_bytes = {}
    for fixture in manifest["files"]:
        raw = (HERE / fixture["local_path"]).read_bytes()
        if any(fixture.get(key) != value for key, value in fingerprints(raw).items()):
            raise ValueError(f"{fixture['source_id']} bytes differ from pinned fixture")
        fixture_bytes[fixture["source_id"]] = raw
    output = Path("/out")
    packages = ["libsqlite3-0", "libcurl4t64", "php8.4-cli", "php8.4-common", "php8.4-curl", "php8.4-gmp",
                "php8.4-intl", "php8.4-mbstring", "php8.4-sqlite3", "php8.4-xml", "php8.4-zip", "python3", "strace"]
    environment = {
        "group": group, "utc": utc(), "platform": platform.platform(), "container_host": platform.node(),
        "os_release": Path("/etc/os-release").read_text(), "python": platform.python_version(),
        "python_sqlite": sqlite3.sqlite_version, "resolver": Path("/etc/resolv.conf").read_text(),
        "php": run_cmd(["php", "-v"], env=ENV),
        "php_modules": run_cmd(["php", "-m"], env=ENV),
        "php_pdo_sqlite_and_curl": run_cmd(["php", "-r", (
            "echo json_encode(['sqlite'=>(new PDO('sqlite::memory:'))->query('select sqlite_version()')"
            "->fetchColumn(),'curl'=>curl_version()['version'],'libxml'=>LIBXML_DOTTED_VERSION]);"
        )], env=ENV),
        "os_packages": run_cmd(["dpkg-query", "-W", *packages], env=ENV),
        "strace": run_cmd(["strace", "-V"], env=ENV),
        "bundled_simplepie": next(
            line.strip() for line in (SOURCE / "lib/simplepie/simplepie/src/SimplePie.php").read_text().splitlines()
            if "public const VERSION =" in line
        ),
    }
    write_json(output / "runtime.json", environment)
    with tempfile.TemporaryDirectory(prefix="afres228-") as temp:
        plan = case_plan(group, fixture_bytes)
        runs = [run_case(Path(temp), output, *case) for case in plan]
    if group == "main":
        observations(output, manifest, runs)
    failed = [
        run["run_id"] for run in runs if "error" in run or
        any(cmd["exit"] != 0 for cmd in run["commands"].values())
    ]
    print(json.dumps({"group": group, "cases": len(runs), "failed": failed}))
    return int(bool(failed))


def host(args):
    source = args.source.resolve()
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    if commit != PIN:
        raise ValueError(f"FreshRSS HEAD {commit} differs from {PIN}")
    image = json.loads(subprocess.check_output(["docker", "image", "inspect", args.image], text=True))[0]
    output = args.output.resolve()
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="af228-source-") as temporary:
        contents = Path(temporary) / "src"
        contents.mkdir()
        archived = subprocess.check_output(["git", "-C", str(source), "archive", commit])
        subprocess.run(["tar", "-xf", "-", "-C", str(contents)], input=archived, check=True)
        command = [
            "docker", "run", "--rm", "--network", "none", "--dns", "127.0.0.1",
            "--security-opt", "no-new-privileges",
            "--mount", f"type=bind,src={contents},dst=/src,readonly",
            "--mount", f"type=bind,src={HERE},dst=/study,readonly",
            "--mount", f"type=bind,src={output},dst=/out",
            image["Id"], "python3", "/study/run.py", "--inside", args.group,
        ]
        # This timeout is per container; individual FreshRSS commands also have a timeout.
        result = run_cmd(command, timeout=480)
        write_json(output / "container.json", {
            "group": args.group, "git_commit": commit,
            "git_archive_sha256": hashlib.sha256(archived).hexdigest(),
            "image_id": image["Id"], "arch": image["Architecture"], "os": image["Os"],
            **result,
        })
    print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], end="", file=sys.stderr)
    return result["exit"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=GROUPS)
    parser.add_argument("--source", type=Path, help="Git checkout of the exact receiver commit")
    parser.add_argument("--output", type=Path, help="New directory for the group's receipts")
    parser.add_argument("--image", default=IMAGE)
    parser.add_argument("--inside", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.inside:
        return container(args.group)
    if args.source is None or args.output is None:
        parser.error("--source and --output are required")
    return host(args)


if __name__ == "__main__":
    raise SystemExit(main())
