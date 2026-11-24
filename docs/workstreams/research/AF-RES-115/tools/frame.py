"""Collect the chronological keyword frame from GitHub's public issue pages.

Usage: python -B tools/frame.py /tmp/af-res-115-scan
Only opening issue bodies are read. The temporary cache is not part of the bundle.
"""
import argparse
import concurrent.futures
import csv
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROJECTS = {
    "E": ("excalidraw/excalidraw", ("excalidraw", "json", "drawing")),
    "M": ("musescore/MuseScore", ("musicxml", "mxl", "mscx", "mscz")),
}
QUERY = "is:issue created:2022-01-01..2025-12-31 sort:created-asc"
EMBEDDED = re.compile(r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>', re.S)


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def page_url(repo, page):
    return f"https://github.com/{repo}/issues?" + urlencode({"q": QUERY, "page": page})


def fetch(url, attempts=3):
    for attempt in range(attempts):
        try:
            req = Request(url, headers={"User-Agent": "AF-RES-115 public source research"})
            with urlopen(req, timeout=25) as response:
                return response.url, response.read(), utc()
        except OSError:
            if attempt == attempts - 1:
                raise
            time.sleep(attempt + 1)


def payload(data):
    matches = (json.loads(v) for v in EMBEDDED.findall(data.decode("utf-8")))
    return next(v["payload"] for v in matches if v.get("payload"))


def read_issue(url):
    landed, data, opened = fetch(url)
    route = payload(data)["issueViewerRoute"]
    issue = route["data"]["repository"]["issue"]
    issue = {k: issue[k] for k in (
        "number", "databaseId", "createdAt", "updatedAt", "url", "title", "body",
        "bodyHTML", "bodyVersion", "duplicateOf", "labels", "author", "timelineItems",
    )}
    return {**issue, "landed": landed, "opened": opened}


def cached_issue(directory, item):
    issue_url = item["permalink"]
    disk = directory / f'{item["number"]}.json'
    if disk.exists():
        return json.loads(disk.read_text())
    try:
        issue = read_issue(issue_url)
    except (OSError, KeyError, ValueError, StopIteration) as err:
        return {
            "number": item["number"], "createdAt": item["createdAt"], "url": issue_url,
            "error": f"{type(err).__name__}: {err}", "opened": utc(),
        }
    disk.write_text(json.dumps(issue, ensure_ascii=False), encoding="utf-8")
    return issue


def collect(project, root):
    repo, words = PROJECTS[project]
    directory = root / project
    directory.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(words) + r")(?![A-Za-z0-9])", re.I)
    issues = {}
    lists = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for page in range(1, 41):
            url = page_url(repo, page)
            landed, data, opened = fetch(url)
            index = payload(data)["issuesIndexContentRoute"]
            assert index["pageInfo"]["currentPage"] == page
            items = [x["issue"] for x in index["results"]
                     if x["itemType"] == "REPO_ISSUES_DASHBOARD_ITEM_TYPE_ISSUE"]
            lists.append({"role": "issue-list", "project": project, "page": page,
                          "source_url": url, "landed": landed, "opened": opened,
                          "numbers": [i["number"] for i in items],
                          "count_in_query": index["pageInfo"]["totalCount"]})
            for issue in executor.map(lambda item: cached_issue(directory, item), items):
                number = issue["number"]
                # An issue may be displayed twice if the public search changed mid-run.
                if number in issues:
                    raise ValueError(f"{repo}: duplicate list issue {number}")
                issues[number] = issue
                if "body" in issue:
                    issue["keyword_matches"] = sorted({m.group().casefold() for m in pattern.finditer(issue["body"])})
            ordered = sorted(issues.values(), key=lambda x: (x["createdAt"], x.get("databaseId", 0)))
            matched = [v for v in ordered if v.get("keyword_matches")]
            print(project, page, len(ordered), len(matched), flush=True)
            if len(matched) >= 60 and ordered[-1]["createdAt"] > matched[59]["createdAt"]:
                break
            if page == index["pageInfo"]["totalPages"]:
                break
    return ordered, matched[:60], lists


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(lambda p: collect(p, args.cache), PROJECTS))
    fields = ["project", "scan_rank", "keyword_rank", "issue_number", "issue_id",
              "created_utc", "body_sha256", "keywords", "source_url", "landed",
              "opened_utc", "error"]
    with (args.cache / "scan.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fields)
        writer.writeheader()
        for project, (rows, matched, lists) in zip(PROJECTS, outcomes, strict=True):
            ranks = {item["number"]: rank for rank, item in enumerate(matched, 1)}
            for order, issue in enumerate(rows, 1):
                writer.writerow({
                    "project": project, "scan_rank": order,
                    "keyword_rank": ranks.get(issue["number"], ""),
                    "issue_number": issue["number"], "issue_id": issue.get("databaseId", ""),
                    "created_utc": issue["createdAt"],
                    "body_sha256": sha(issue["body"].encode()) if "body" in issue else "",
                    "keywords": ";".join(issue.get("keyword_matches", [])),
                    "source_url": issue["url"], "landed": issue.get("landed", ""),
                    "opened_utc": issue["opened"], "error": issue.get("error", ""),
                })
            (args.cache / f"{project}-lists.json").write_text(json.dumps(lists, indent=2) + "\n")


if __name__ == "__main__":
    main()
