"""Independent AI review of stages 1/2; only brief receipts are retained.

Run from the repository root with python -B. This script changes no git state,
does not touch original evidence, and does not count review rereads as sources.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen
import collections
import csv
import io
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[5]
BASE = "docs/workstreams/research/AF-RES-098/"
STAGE1 = "c0d31ca194e47fe69bc51dc0ef85d6e346b50774"
STAGE2 = "0df9ea9edbcee995d631eef54b65fd43f73c245f"
OLD_GG = "392175bbb00b04025aa5d17a0c18b3896adeb40f"


def gitfile(rev, path):
    return subprocess.check_output(["git", "show", rev + ":" + BASE + path], cwd=REPO)


def parse_csv(b):
    return list(csv.DictReader(io.StringIO(b.decode())))


class Attributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.downloads = []
        self.base = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("img", "source"):
            self.images.append({"line": self.getpos()[0], "tag": tag,
                                **{k: a[k] for k in ("src", "srcset", "alt", "class") if k in a}})
        if tag == "base":
            self.base.append(a)
        if tag == "a" and re.search(r"\.(?:png|svg|jpe?g|gif|csv|dat|jsonl?|xml|bin|zip|txt)(?:$|[#?])", a.get("href", ""), re.I):
            self.downloads.append({"line": self.getpos()[0], "href": a["href"]})


def fetch(item):
    key, url = item
    record = {"id": key, "url": url, "utc": datetime.now(timezone.utc).isoformat(),
              "counted_as_new_research_source": False,
              "scope": "Independent reread; original-source counts do not increase."}
    try:
        with urlopen(url, timeout=45) as response:
            b = response.read()
            record.update(status=response.status, final_url=response.url,
                          mime=response.headers.get("Content-Type"), bytes=len(b),
                          sha256=sha256(b).hexdigest())
        if key in ("MPL-RELEASES", "GG-RELEASES"):
            data = json.loads(b)
            stable = [x for x in data if not x.get("prerelease") and not x.get("draft")
                      and re.fullmatch(r"v?\d+\.\d+\.\d+", x["tag_name"])]
            candidates = sorted([x for x in stable if re.fullmatch(r"v?\d+\.\d+\.0", x["tag_name"])
                                 and "2023-01-01" <= x["published_at"] < "2026-01-01"], key=lambda x: x["published_at"])
            first = candidates[0]
            series = first["tag_name"].rsplit(".", 1)[0] + "."
            patches = sorted([x for x in stable if x["tag_name"].startswith(series)
                              and x["tag_name"] != first["tag_name"] and x["published_at"] > first["published_at"]],
                             key=lambda x: x["published_at"])
            record.update(release_rows=len(data), earliest_candidate={k: first[k] for k in ("tag_name", "published_at", "html_url")},
                          first_patch={k: patches[0][k] for k in ("tag_name", "published_at", "html_url")},
                          pagination_scope="per_page=100; confirms entries through the 2022 predecessor; no claim about omitted older records")
        elif key.startswith("GG-OLD-"):
            s = b.decode()
            parser = Attributes()
            parser.feed(s)
            record.update(all_document_image_attributes=parser.images, all_document_file_links=parser.downloads,
                          base_elements=parser.base,
                          examples_heading_lines=[i for i, line in enumerate(s.splitlines(), 1)
                                                  if re.search(r'id=[\"\'](?:ref-)?examples[\"\']', line)],
                          scope_note="Scanned the entire old HTML, including attributes outside Examples, to challenge the narrower selector. Common logo/lifecycle art is identified separately.")
        else:
            s = b.decode()
            excerpt = []
            lines = s.splitlines()
            for i, line in enumerate(lines, 1):
                if any(x in line for x in ("Python 3.11.0", "Python 3.12.0", "Python 3.13.0", "Python 3.14.0", "first maintenance")) or re.search(r"Release [Dd]ate", line):
                    excerpt.append({"line": i, "text": re.sub(r"<[^>]+>", " ", line).strip()[:220]})
                    if "release-number" in line and i < len(lines):
                        excerpt.append({"line": i + 1, "text": re.sub(r"<[^>]+>", " ", lines[i]).strip()[:220]})
            record["short_release_locators"] = excerpt
    except Exception as exc:
        record.update(status=getattr(exc, "code", None), error=f"{type(exc).__name__}: {exc}")
    return record


def main():
    audit = {"utc": datetime.now(timezone.utc).isoformat(), "reviewer": "separate AI agent /root/cross_domain; not a human reviewer",
             "self_authored_Q6_excluded": True, "stage1": STAGE1, "stage2": STAGE2,
             "unchanged_selection_files": {}, "frame_checks": {}, "source_ledger_checks": {}}
    for name in ("SCOPE.md", "freeze.json", "frame.csv"):
        a, b = gitfile(STAGE1, name), gitfile(STAGE2, name)
        audit["unchanged_selection_files"][name] = {"byte_equal": a == b, "sha256": sha256(b).hexdigest()}
    sealed = gitfile(STAGE2, "predictions.csv")
    working = (REPO / BASE / "predictions.csv").read_bytes()
    audit["prediction_csv"] = {"rows": len(parse_csv(sealed)), "values": collections.Counter(x["prediction_U"] for x in parse_csv(sealed)),
                               "sealed_sha256": sha256(sealed).hexdigest(), "working_sha256": sha256(working).hexdigest(),
                               "working_equal_after_CRLF_normalization": sealed.replace(b"\r\n", b"\n") == working.replace(b"\r\n", b"\n")}
    for project in ("matplotlib", "cpython", "ggplot2"):
        rows = parse_csv(gitfile(STAGE2, f"evidence/{project}/frame.csv"))
        path_key = next(k for k in ("relative_path", "path", "relative_page") if k in rows[0])
        case_key = next((k for k in ("case_id", "example_id") if k in rows[0]), None)
        paths = [x[path_key] for x in rows]
        audit["frame_checks"][project] = {"rows": len(rows), "sorted_lexicographically": paths == sorted(paths),
            "unique_paths": len(set(paths)), "selected": [{"ordinal": i, "path": x[path_key], "case_id": x.get(case_key, "see frozen selection")}
                                                         for i, x in enumerate(rows, 1) if x.get(case_key) or x.get("status") == "selected"]}
    for stage in (STAGE1, STAGE2):
        rows = [json.loads(x) for x in gitfile(stage, "sources.jsonl").decode().splitlines()]
        counted = [x for x in rows if x.get("counted")]
        hashes = collections.defaultdict(list)
        for x in counted:
            if x.get("sha256"):
                hashes[(x.get("lineage"), x["sha256"])].append(x["id"])
        audit["source_ledger_checks"][stage] = {"rows": len(rows), "counted": len(counted),
            "categories": collections.Counter(x.get("category") for x in counted),
            "same_lineage_same_sha_duplicates": [ids for ids in hashes.values() if len(ids) > 1],
            "empty_claim": [x["id"] for x in counted if not x.get("claim")],
            "missing_required_specifics": [{"id": x["id"], "fields": [k for k in ("url", "utc", "publisher", "lineage", "locator", "observed", "limitations", "dedup_basis") if not x.get(k)]}
                                          for x in counted if any(not x.get(k) for k in ("url", "utc", "publisher", "lineage", "locator", "observed", "limitations", "dedup_basis"))]}
    (OUT / "selection-review.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    urls = [("MPL-RELEASES", "https://api.github.com/repos/matplotlib/matplotlib/releases?per_page=100"),
            ("GG-RELEASES", "https://api.github.com/repos/tidyverse/ggplot2/releases?per_page=100"),
            ("PY-RELEASE-LIST", "https://www.python.org/downloads/"),
            ("PY-3120", "https://www.python.org/downloads/release/python-3120/"),
            ("PY-3121", "https://www.python.org/downloads/release/python-3121/")]
    for path in ("absoluteGrob", "add_theme", "aes", "aes_", "aes_all", "aes_auto", "aes_colour_fill_alpha"):
        urls.append(("GG-OLD-" + path, f"https://raw.githubusercontent.com/tidyverse/ggplot2/{OLD_GG}/reference/{path}.html"))
    with ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(fetch, urls))
    (OUT / "selection-rereads.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"audit": audit, "rereads": [{"id": x["id"], "status": x.get("status"), "bytes": x.get("bytes"), "error": x.get("error")} for x in records]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
