"""Replay supplementary windows and a synthetic recursive SQLite probe."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import tarfile

from select_passages import first_window, make_segment, occurrences, split_window

SQL = "f3d536d37825302e31ed0eddd811c689f38f85a3"
GRID = "804b7b0055e80dfaba091e7f32a4bca303e569e3"
WPT = "03d41fe0fe3338c66cb56644b8a1705fe2e7247b"
DEB = "https://deb.debian.org/debian/pool/main/s/sqlite3/sqlite3-doc_3.46.1-7%2Bdeb13u2_all.deb"
WPT_ROOT = f"https://raw.githubusercontent.com/web-platform-tests/wpt/{WPT}/css/css-grid/grid-items/"
URLS = {
    "sqlite-lang-with.html": DEB,
    "sqlite-with1.test": f"https://raw.githubusercontent.com/sqlite/sqlite/{SQL}/test/with1.test",
    "grid-1.bs": f"https://raw.githubusercontent.com/w3c/csswg-drafts/{GRID}/css-grid-1/Overview.bs",
    **{name: WPT_ROOT + name for name in (
        "grid-item-min-size-auto-overflow-001.html",
        "grid-item-minimum-size-single-axis-scroll-container.html",
        "grid-minimum-size-grid-items-012.html",
        "grid-minimum-size-grid-items-018.html",
    )},
}
SQL_TERMS = [
    ["recursive", "queue", "limit", "offset", "extracted"],
    ["order", "negative", "zero", "fifo", "recursive"],
]
SQL_STRESS_TERMS = [
    ["negative", "unlimited"],
    ["fifo", "undefined", "safety", "upper", "drain", "immediately", "practice"],
]
GRID_TERMS = [
    ["grid", "item", "minimum", "minmax", "auto"],
    ["scrollable", "overflow", "track", "flexible", "zero"],
]
SQL_MARKERS = [
    ("limit-cap", "The LIMIT clause, if present", "will ever be added to the recursive table in step 2b."),
    ("zero-negative", "A limit of zero means", "may be added to the recursive table."),
    ("orderby-controls-queue", "If an ORDER BY clause is present", "step 2a."),
    ("unordered-fifo-caveat", "then the order in which rows are extracted is undefined.", "since it might change.)"),
]
GRID_MARKERS = [
    ("overflow-and-track-exceptions", "To provide a more reasonable default <a>minimum size</a>", "is zero, as usual."),
    ("bare-flex-implies-auto-min", "When appearing outside a ''minmax()'' notation", "''minmax(auto, <<flex>>)'')."),
]
FIXTURE_MARKERS = {
    "sqlite-with1.test": [
        ("inner-limit-5", "do_catchsql_test 5.3 {", "} {0 {1 2 3 4 5}}"),
        ("order-limit-offset", "do_execsql_test 5.2.3 {", "} {2 20 3 30 4 40 4 40}"),
        ("inner-limit-zero-negative", "set I [list 1 2", "limit_test 9.9    -1 -1"),
    ],
    "grid-item-min-size-auto-overflow-001.html": [
        ("visible-vs-scrollable-positive-negative", "The test passes if", "doesn't have scrollbars."),
    ],
    "grid-item-minimum-size-single-axis-scroll-container.html": [
        ("axis-diff", "However, for a grid axis", "set to zero for that axis."),
        ("first-expected-pair", 'class="item x-scroller" data-expected-width=', 'data-expected-height="100">'),
        ("column-control", 'class="item y-scroller" data-expected-width="100"', 'data-expected-height="100">'),
    ],
    "grid-minimum-size-grid-items-012.html": [
        ("fixed-zero-minimum", "grid: minmax(0px, auto)", "minmax(0px, auto);"),
        ("expected-green", "Test passes if", "no red</strong>."),
    ],
    "grid-minimum-size-grid-items-018.html": [
        ("fixed-max-auto-min", "grid: minmax(auto, 500px)", "minmax(auto, 500px);"),
        ("expected-green", "Test passes if", "no red</strong>."),
    ],
}


def download(root):
    root.mkdir(parents=True, exist_ok=True)
    for artifact, url in URLS.items():
        target = root / artifact
        if target.exists():
            continue
        if artifact == "sqlite-lang-with.html":
            archive = root / "sqlite-doc.deb"
            subprocess.run(["curl", "-fsSL", "--max-time", "45", url, "-o", str(archive)], check=True)
            child = subprocess.Popen(["dpkg-deb", "--fsys-tarfile", str(archive)], stdout=subprocess.PIPE)
            with tarfile.open(fileobj=child.stdout, mode="r|") as collection:
                for item in collection:
                    if item.name == "./usr/share/doc/sqlite3/lang_with.html":
                        target.write_bytes(collection.extractfile(item).read())
            if child.wait() or not target.is_file():
                raise ValueError("SQLite doc payload not extracted")
        else:
            subprocess.run(["curl", "-fsSL", "--max-time", "35", url, "-o", str(target)], check=True)


def report(root, artifact, terms, markers, profile):
    data = (root / artifact).read_bytes()
    text = data.decode("utf-8")
    queries = [set(s) for s in terms]
    first, anchor = first_window(text, queries)
    split, search = split_window(text, queries, first)
    w1_hits = {token for a, b, token in occurrences(text, set.union(*queries)) if first[0] <= a < b <= first[1]}
    counts = [len(q & w1_hits) for q in queries]
    selected = {"W1": [first], "W2": split}
    checks = []
    for name, prefix, suffix in markers:
        start = text.index(prefix)
        end = text.index(suffix, start) + len(suffix)
        visible = {w: any(a <= start and end <= b for a, b in spans) for w, spans in selected.items()}
        checks.append({"id": name, "span": make_segment(data, text, start, end), "fully_visible_in_single_segment": visible})
    return {
        "artifact": artifact, "observed_input_url": URLS[artifact],
        "profile": profile, "source_sha256": hashlib.sha256(data).hexdigest(), "source_bytes": len(data),
        "query_tokens": terms, "W1_anchor": anchor, "budget_chars": first[1] - first[0],
        "objectives": {"W1": [min(counts), sum(counts)], "W2": search["objective"]},
        "display": {w: [make_segment(data, text, a, b) for a, b in spans] for w, spans in selected.items()},
        "reference_checks": checks,
    }


def runtime():
    start = datetime.now(timezone.utc).isoformat()
    results = {}
    conn = sqlite3.connect(":memory:")
    limited = "WITH RECURSIVE c(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM c WHERE x<5 LIMIT ?) SELECT x FROM c"
    for cap, expected in [(0, []), (-1, [1, 2, 3, 4, 5]), (3, [1, 2, 3])]:
        actual = [x[0] for x in conn.execute(limited, (cap,))]
        results[f"inner_limit_{cap}"] = {"sql": limited, "parameters": [cap], "expected": expected, "actual": actual}
    queue = (
        "WITH RECURSIVE c(id,level) AS (VALUES(1,0) UNION ALL "
        "SELECT e.child,c.level+1 FROM c JOIN e ON e.parent=c.id ORDER BY 2 {order}, 1 ASC) "
        "SELECT id FROM c"
    )
    conn.executescript("CREATE TABLE e(parent,child); INSERT INTO e VALUES (1,2),(1,3),(2,4),(3,5);")
    for order, expected in [("ASC", [1, 2, 3, 4, 5]), ("DESC", [1, 2, 4, 3, 5])]:
        statement = queue.format(order=order)
        actual = [x[0] for x in conn.execute(statement)]
        results[order] = {"sql": statement, "expected": expected, "actual": actual}
    if any(v["expected"] != v["actual"] for v in results.values()):
        raise ValueError("synthetic expectations failed")
    return {"started_utc": start, "finished_utc": datetime.now(timezone.utc).isoformat(),
            "sqlite_version": sqlite3.sqlite_version, "fixture": "synthetic; not upstream test harness",
            "passed": len(results), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cache", type=Path)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--sqlite-runtime", action="store_true")
    args = parser.parse_args()
    if args.download:
        download(args.cache)
    if args.sqlite_runtime:
        result = runtime()
    else:
        result = [
            report(args.cache, "sqlite-lang-with.html", SQL_TERMS, SQL_MARKERS, "full-document"),
            report(args.cache, "sqlite-lang-with.html", SQL_STRESS_TERMS, SQL_MARKERS, "posthoc-boundary-stress"),
            report(args.cache, "sqlite-with1.test", SQL_TERMS, FIXTURE_MARKERS["sqlite-with1.test"], "full-fixture"),
            report(args.cache, "grid-1.bs", GRID_TERMS, GRID_MARKERS, "full-document"),
            *[report(args.cache, name, GRID_TERMS, markers, "full-fixture")
              for name, markers in FIXTURE_MARKERS.items() if name != "sqlite-with1.test"],
        ]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
