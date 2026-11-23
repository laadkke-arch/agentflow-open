"""Project GitHub issue description or metadata from a saved anonymous HTML page."""

import argparse
import json
from pathlib import Path
import re
import sys

from verify_events import ROOT, body_hashes


def git_hub_description(page, target):
    script_pattern = r'<script\b[^>]*type="application/json"[^>]*>(.*?)</script>'
    payloads = [
        json.loads(script)["payload"]["issueViewerRoute"]["data"]["repository"]
        for script in re.findall(script_pattern, page, re.S)
        if '"issueViewerRoute":' in script
    ]
    repo, = payloads
    issue = repo["issue"]
    repo_id = re.search(r'name="octolytics-dimension-repository_id" content="(\d+)"', page)
    url = f"https://github.com/{target['repo']}/issues/{target['number']}"
    assert repo_id and int(repo_id[1]) == target["repo_id"]
    assert (issue["databaseId"], issue["id"], issue["number"], issue["createdAt"], issue["url"]) == (
        target["issue_id"], target["issue_node"], target["number"], target["created_utc"], url
    )
    assert issue["author"]["login"].casefold() == target["author"].casefold()
    return issue


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case")
    parser.add_argument("html", type=Path)
    parser.add_argument("--body", action="store_true", help="write the body to a private stream for reading")
    args = parser.parse_args()
    targets = {row["case"]: row for row in json.loads((ROOT / "fixtures/targets.json").read_text())}
    issue = git_hub_description(args.html.read_text(), targets[args.case])
    if args.body:
        sys.stdout.buffer.write(issue["body"].encode("utf-8"))
    else:
        print(json.dumps({
            "id": issue["id"], "url": issue["url"], "created_utc": issue["createdAt"],
            "updated_utc": issue["updatedAt"], "last_edited_at": issue.get("lastEditedAt"),
            "last_user_content_edit": issue.get("lastUserContentEdit"),
            "github_body_version": issue.get("bodyVersion"),
            **body_hashes(issue["body"]),
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
